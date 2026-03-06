# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""
Model detection — locate and validate the presence of all required model files.

Works with both directory sources and ``.zip`` archives.  Detection never
extracts or reads weight data; it only inspects file names and sizes.
"""

from __future__ import annotations

import logging
import re
import zipfile
from pathlib import Path
from typing import Protocol

from mycelium.ai.deepseek_adapter.config import (
    EXPECTED_SHARDS,
    REQUIRED_CONFIG_FILES,
    SHARD_PATTERN,
    TOKENIZER_FILES,
    AdapterConfig,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Filesystem abstraction (for testability)
# ---------------------------------------------------------------------------


class FileSystemProtocol(Protocol):
    """Minimal filesystem interface used by detection logic."""

    def exists(self, path: Path) -> bool: ...          # noqa: E704
    def is_dir(self, path: Path) -> bool: ...          # noqa: E704
    def is_file(self, path: Path) -> bool: ...         # noqa: E704
    def list_dir(self, path: Path) -> list[str]: ...   # noqa: E704


class RealFileSystem:
    """Standard filesystem implementation."""

    def exists(self, path: Path) -> bool:
        return path.exists()

    def is_dir(self, path: Path) -> bool:
        return path.is_dir()

    def is_file(self, path: Path) -> bool:
        return path.is_file()

    def list_dir(self, path: Path) -> list[str]:
        return [p.name for p in path.iterdir()]


# ---------------------------------------------------------------------------
# Detection result
# ---------------------------------------------------------------------------


class DetectionResult:
    """Container for model detection results.

    Attributes:
        source_path: Resolved path to model directory or zip.
        is_zip: Whether the source is a zip archive.
        shards: List of shard filenames found.
        config_files: List of config filenames found.
        tokenizer_files: List of tokenizer filenames found.
        missing: List of missing required filenames.
        errors: List of human-readable error strings.
    """

    __slots__ = (
        "source_path", "is_zip", "shards", "config_files",
        "tokenizer_files", "missing", "errors",
    )

    def __init__(self) -> None:
        self.source_path: Path = Path()
        self.is_zip: bool = False
        self.shards: list[str] = []
        self.config_files: list[str] = []
        self.tokenizer_files: list[str] = []
        self.missing: list[str] = []
        self.errors: list[str] = []

    @property
    def ok(self) -> bool:
        """Return *True* if all required files were detected with no errors."""
        return not self.missing and not self.errors

    def raise_on_error(self) -> None:
        """Raise ``FileNotFoundError`` if detection found problems."""
        if not self.ok:
            parts = self.errors + [f"Missing: {f}" for f in self.missing]
            raise FileNotFoundError(
                "Model detection failed:\n  • " + "\n  • ".join(parts)
            )


# ---------------------------------------------------------------------------
# Core detection
# ---------------------------------------------------------------------------


def _validate_shard_set(shard_names: list[str]) -> list[str]:
    """Return list of error strings if the shard set is incomplete."""
    errors: list[str] = []
    pattern = re.compile(SHARD_PATTERN)
    matched = [s for s in shard_names if pattern.match(s)]

    if not matched:
        errors.append("No safetensors shard files found.")
        return errors

    # Parse total count from first match
    parts = matched[0].rsplit("-of-", 1)
    if len(parts) == 2:
        expected_total = int(parts[1].replace(".safetensors", ""))
        if len(matched) != expected_total:
            errors.append(
                f"Incomplete shard set: found {len(matched)} of "
                f"{expected_total} expected shards.  "
                f"Present: {sorted(matched)}"
            )
    return errors


def detect_model_files(
    config: AdapterConfig,
    *,
    fs: FileSystemProtocol | None = None,
) -> DetectionResult:
    """Detect and validate the presence of all required model files.

    Args:
        config: Adapter configuration.
        fs: Optional filesystem abstraction (defaults to real filesystem).

    Returns:
        A ``DetectionResult`` indicating what was found and any problems.
    """
    if fs is None:
        fs = RealFileSystem()

    result = DetectionResult()
    source = config.resolved_model_source
    result.source_path = source

    if not fs.exists(source):
        result.errors.append(
            f"Model source does not exist: {_redact_path(source)}"
        )
        return result

    if config.is_zip_source:
        return _detect_in_zip(source, result)

    if not fs.is_dir(source):
        result.errors.append(
            f"Model source is not a directory or .zip: {_redact_path(source)}"
        )
        return result

    return _detect_in_directory(source, result, fs)


def _detect_in_directory(
    source: Path,
    result: DetectionResult,
    fs: FileSystemProtocol,
) -> DetectionResult:
    """Check a directory for required model files."""
    result.is_zip = False
    try:
        entries = set(fs.list_dir(source))
    except OSError as exc:
        result.errors.append(f"Cannot list directory: {exc}")
        return result

    # Shards
    for shard in EXPECTED_SHARDS:
        if shard in entries:
            result.shards.append(shard)
        else:
            result.missing.append(shard)

    shard_errors = _validate_shard_set(result.shards)
    result.errors.extend(shard_errors)

    # Config
    for cfg_file in REQUIRED_CONFIG_FILES:
        if cfg_file in entries:
            result.config_files.append(cfg_file)
        else:
            result.missing.append(cfg_file)

    # Tokenizer (at least one)
    found_tokenizer = [t for t in TOKENIZER_FILES if t in entries]
    if found_tokenizer:
        result.tokenizer_files = found_tokenizer
    else:
        result.missing.append("tokenizer (one of: " + ", ".join(TOKENIZER_FILES) + ")")

    logger.info(
        "Detection complete: %d shards, %d config, %d tokenizer files",
        len(result.shards),
        len(result.config_files),
        len(result.tokenizer_files),
    )
    return result


def _detect_in_zip(zip_path: Path, result: DetectionResult) -> DetectionResult:
    """Check inside a zip archive for required model files (no extraction)."""
    result.is_zip = True
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            names = set(zf.namelist())
            # Flatten: strip one level of directory if present
            basename_set: set[str] = set()
            for name in names:
                parts = Path(name).parts
                if len(parts) > 1:
                    basename_set.add(parts[-1])
                else:
                    basename_set.add(name)
    except (zipfile.BadZipFile, OSError) as exc:
        result.errors.append(f"Cannot read zip archive: {exc}")
        return result

    # Use the same checks as directory
    for shard in EXPECTED_SHARDS:
        if shard in basename_set:
            result.shards.append(shard)
        else:
            result.missing.append(shard)

    shard_errors = _validate_shard_set(result.shards)
    result.errors.extend(shard_errors)

    for cfg_file in REQUIRED_CONFIG_FILES:
        if cfg_file in basename_set:
            result.config_files.append(cfg_file)
        else:
            result.missing.append(cfg_file)

    found_tokenizer = [t for t in TOKENIZER_FILES if t in basename_set]
    if found_tokenizer:
        result.tokenizer_files = found_tokenizer
    else:
        result.missing.append("tokenizer (one of: " + ", ".join(TOKENIZER_FILES) + ")")

    logger.info(
        "Zip detection complete: %d shards, %d config, %d tokenizer files",
        len(result.shards),
        len(result.config_files),
        len(result.tokenizer_files),
    )
    return result


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _redact_path(path: Path) -> str:
    """Redact user-home prefix from path for safe logging."""
    try:
        home = Path.home()
        if path.is_relative_to(home):
            return "~/" + str(path.relative_to(home)).replace("\\", "/")
    except (ValueError, RuntimeError):
        pass
    return str(path).replace("\\", "/")
