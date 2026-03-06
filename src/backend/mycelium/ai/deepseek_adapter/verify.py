# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""
Model verification — streaming SHA-256 checksums and disk-space checks.

All hashing is performed in streaming fashion to avoid loading entire weight
files into memory.
"""

from __future__ import annotations

import hashlib
import json
import logging
import shutil
from pathlib import Path
from typing import IO, Protocol

from mycelium.ai.deepseek_adapter.config import (
    HASH_ALGORITHM,
    HASH_CHUNK_SIZE,
    AdapterConfig,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# IO abstraction (for testability)
# ---------------------------------------------------------------------------


class HashIOProtocol(Protocol):
    """Minimal IO interface for streaming hash computation."""

    def open_read(self, path: Path) -> IO[bytes]: ...   # noqa: E704
    def file_size(self, path: Path) -> int: ...          # noqa: E704


class RealHashIO:
    """Standard IO implementation for hashing."""

    def open_read(self, path: Path) -> IO[bytes]:
        return open(path, "rb")  # noqa: SIM115

    def file_size(self, path: Path) -> int:
        return path.stat().st_size


# ---------------------------------------------------------------------------
# Streaming hash
# ---------------------------------------------------------------------------


def compute_sha256(
    path: Path,
    *,
    io: HashIOProtocol | None = None,
    chunk_size: int = HASH_CHUNK_SIZE,
) -> str:
    """Compute SHA-256 hex digest of a file using streaming IO.

    Args:
        path: File to hash.
        io: Optional IO abstraction (defaults to real IO).
        chunk_size: Bytes per read chunk (default 8 MiB).

    Returns:
        Lowercase hex digest string.
    """
    if io is None:
        io = RealHashIO()

    h = hashlib.new(HASH_ALGORITHM)
    with io.open_read(path) as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def compute_hashes_for_shards(
    source_dir: Path,
    shard_names: list[str],
    *,
    io: HashIOProtocol | None = None,
) -> dict[str, str]:
    """Compute SHA-256 for each shard file.

    Args:
        source_dir: Directory containing shard files.
        shard_names: List of shard filenames.
        io: Optional IO abstraction.

    Returns:
        Dict mapping filename → hex digest.
    """
    result: dict[str, str] = {}
    for name in shard_names:
        path = source_dir / name
        logger.info("Computing %s hash for %s ...", HASH_ALGORITHM, name)
        digest = compute_sha256(path, io=io)
        result[name] = digest
        logger.info("  %s = %s", name, digest)
    return result


# ---------------------------------------------------------------------------
# Checksum verification
# ---------------------------------------------------------------------------


def load_checksums(checksums_path: Path) -> dict[str, str]:
    """Load expected checksums from a JSON file.

    Expected format::

        {
            "model-00001-of-000002.safetensors": "abcdef...",
            "model-00002-of-000002.safetensors": "123456..."
        }

    Args:
        checksums_path: Path to JSON checksums file.

    Returns:
        Dict mapping filename → expected hex digest.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        ValueError: If the file isn't valid JSON or has wrong structure.
    """
    if not checksums_path.exists():
        raise FileNotFoundError(
            f"Checksums file not found: {checksums_path}. "
            "If you don't have checksums, remove 'checksums_file' from config."
        )

    try:
        data = json.loads(checksums_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Checksums file is not valid JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("Checksums file must contain a JSON object (dict).")

    return {str(k): str(v).lower().strip() for k, v in data.items()}


def verify_checksums(
    actual: dict[str, str],
    expected: dict[str, str],
) -> list[str]:
    """Compare actual SHA-256 hashes against expected values.

    Args:
        actual: Dict mapping filename → computed hex digest.
        expected: Dict mapping filename → expected hex digest.

    Returns:
        List of error strings.  Empty list means all checksums match.
    """
    errors: list[str] = []
    for filename, expected_hash in expected.items():
        if filename not in actual:
            errors.append(
                f"Checksum for '{filename}' expected but file was not hashed. "
                "Ensure the file is present and listed in detection."
            )
            continue
        if actual[filename] != expected_hash:
            errors.append(
                f"Checksum mismatch for '{filename}':\n"
                f"    expected: {expected_hash}\n"
                f"    actual:   {actual[filename]}\n"
                f"  Remediation: re-download this shard or verify the "
                f"checksums file is correct."
            )
    return errors


# ---------------------------------------------------------------------------
# Disk space check
# ---------------------------------------------------------------------------


def check_disk_space(
    target_dir: Path,
    min_free_bytes: int,
) -> None:
    """Verify that sufficient free disk space is available.

    Args:
        target_dir: Directory whose filesystem is checked.
        min_free_bytes: Minimum required free bytes.

    Raises:
        OSError: If free space is below the threshold, with an actionable
            message including required and available byte counts.
    """
    # Ensure the directory (or a parent) exists for the check
    check_path = target_dir
    while not check_path.exists():
        check_path = check_path.parent

    usage = shutil.disk_usage(check_path)
    if usage.free < min_free_bytes:
        raise OSError(
            f"Insufficient disk space on '{check_path.drive or check_path.anchor}'.\n"
            f"  Required:  {min_free_bytes:,} bytes "
            f"({min_free_bytes / (1024**3):.1f} GB)\n"
            f"  Available: {usage.free:,} bytes "
            f"({usage.free / (1024**3):.1f} GB)\n"
            f"  Free up at least {(min_free_bytes - usage.free):,} bytes "
            f"and retry."
        )

    logger.info(
        "Disk space check passed: %.1f GB free (need %.1f GB)",
        usage.free / (1024**3),
        min_free_bytes / (1024**3),
    )


def run_verification(
    config: AdapterConfig,
    source_dir: Path,
    shard_names: list[str],
    *,
    io: HashIOProtocol | None = None,
) -> dict[str, str]:
    """Run full verification: disk space, hashes, and checksum comparison.

    Args:
        config: Adapter configuration.
        source_dir: Directory containing the model files.
        shard_names: Shard filenames to verify.
        io: Optional IO abstraction.

    Returns:
        Dict mapping filename → computed SHA-256 hex digest.

    Raises:
        OSError: On insufficient disk space.
        ValueError: On checksum mismatch.
        FileNotFoundError: On missing checksums file (when configured).
    """
    # 1. Disk space
    check_disk_space(config.resolved_cache_dir, config.min_free_bytes)

    # 2. Compute hashes
    hashes = compute_hashes_for_shards(source_dir, shard_names, io=io)

    # 3. Compare if checksums file provided
    if config.checksums_file:
        checksums_path = Path(config.checksums_file).expanduser().resolve()
        expected = load_checksums(checksums_path)
        errors = verify_checksums(hashes, expected)
        if errors:
            raise ValueError(
                "Checksum verification failed:\n  • "
                + "\n  • ".join(errors)
            )
        logger.info("All checksums verified successfully.")
    else:
        logger.info(
            "No checksums_file configured; printing computed hashes "
            "for manual verification."
        )
        for name, digest in hashes.items():
            logger.info("  %s  %s", digest, name)

    return hashes
