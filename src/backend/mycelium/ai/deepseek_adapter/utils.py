# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""
Utility functions — atomic extraction, file permissions, path helpers.
"""

from __future__ import annotations

import logging
import os
import platform
import shutil
import stat
import uuid
import zipfile
from pathlib import Path

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Atomic extraction from zip
# ---------------------------------------------------------------------------


def extract_zip_atomically(
    zip_path: Path,
    target_dir: Path,
    *,
    required_names: list[str] | None = None,
) -> Path:
    """Extract files from a zip archive using an atomic rename strategy.

    Extraction flow:
      1. Create a temporary directory ``target_dir/.tmp_<uuid>``.
      2. Extract files into the temporary directory.
      3. ``os.replace()`` the temporary directory to the final path.

    If extraction fails at any point the temporary directory is cleaned up.

    Args:
        zip_path: Path to the ``.zip`` archive.
        target_dir: Parent directory for the final extracted folder.
        required_names: Optional list of filenames to extract (all if *None*).

    Returns:
        Path to the final extracted directory.

    Raises:
        zipfile.BadZipFile: If the archive is corrupt.
        OSError: On filesystem errors.
    """
    target_dir.mkdir(parents=True, exist_ok=True)

    final_dir = target_dir / zip_path.stem
    if final_dir.exists():
        logger.info("Extracted directory already exists: %s", _safe_path(final_dir))
        return final_dir

    tmp_name = f".tmp_{uuid.uuid4().hex}"
    tmp_dir = target_dir / tmp_name

    try:
        tmp_dir.mkdir(parents=True, exist_ok=False)
        logger.info("Extracting zip to temporary directory ...")

        with zipfile.ZipFile(zip_path, "r") as zf:
            members = zf.namelist()
            for member in members:
                basename = Path(member).name
                if not basename:
                    continue  # skip directories
                if required_names is not None and basename not in required_names:
                    continue

                dest = tmp_dir / basename
                with zf.open(member) as src, open(dest, "wb") as dst:
                    shutil.copyfileobj(src, dst)

                _set_owner_only(dest)

        # Atomic rename
        os.replace(str(tmp_dir), str(final_dir))
        logger.info("Extraction complete: %s", _safe_path(final_dir))
        return final_dir

    except BaseException:
        # Clean up partial extraction
        if tmp_dir.exists():
            shutil.rmtree(tmp_dir, ignore_errors=True)
            logger.warning("Cleaned up partial extraction at %s", _safe_path(tmp_dir))
        raise


# ---------------------------------------------------------------------------
# File permissions
# ---------------------------------------------------------------------------


def _set_owner_only(path: Path) -> None:
    """Set file permissions to owner-read/write only (Unix) or skip (Windows)."""
    if platform.system() != "Windows":
        try:
            path.chmod(stat.S_IRUSR | stat.S_IWUSR)
        except OSError:
            pass  # best-effort


# ---------------------------------------------------------------------------
# Cache management
# ---------------------------------------------------------------------------


def ensure_cache_dir(cache_dir: Path) -> Path:
    """Create cache directory if it doesn't exist and return it.

    Args:
        cache_dir: Target cache directory path.

    Returns:
        Resolved cache directory path.
    """
    cache_dir = cache_dir.expanduser().resolve()
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def get_cache_size_bytes(cache_dir: Path) -> int:
    """Compute total size in bytes of all files under *cache_dir*.

    Args:
        cache_dir: Directory to measure.

    Returns:
        Total size in bytes.
    """
    total = 0
    if not cache_dir.exists():
        return total
    for entry in cache_dir.rglob("*"):
        if entry.is_file():
            try:
                total += entry.stat().st_size
            except OSError:
                pass
    return total


def enforce_max_cache(cache_dir: Path, max_bytes: int) -> None:
    """Check if cache exceeds *max_bytes* and log a warning.

    Does not delete anything automatically — future LRU cleanup can be
    added here as an extension point.

    Args:
        cache_dir: Target cache directory.
        max_bytes: Maximum allowed cache bytes.
    """
    current = get_cache_size_bytes(cache_dir)
    if current > max_bytes:
        logger.warning(
            "Cache exceeds maximum: %s bytes (limit %s bytes). "
            "Consider cleaning %s manually.",
            f"{current:,}",
            f"{max_bytes:,}",
            _safe_path(cache_dir),
        )


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------


def _safe_path(path: Path) -> str:
    """Return a logging-safe string for *path* (redact home dir)."""
    try:
        home = Path.home()
        if path.is_relative_to(home):
            return "~/" + str(path.relative_to(home)).replace("\\", "/")
    except (ValueError, RuntimeError):
        pass
    return str(path).replace("\\", "/")
