# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""Unit tests for utility functions — uses temp dirs, no real weights."""

from __future__ import annotations

import zipfile
from pathlib import Path

import pytest

from mycelium.ai.deepseek_adapter.utils import (
    ensure_cache_dir,
    enforce_max_cache,
    extract_zip_atomically,
    get_cache_size_bytes,
)


# ---------------------------------------------------------------------------
# Cache directory tests
# ---------------------------------------------------------------------------


class TestEnsureCacheDir:
    """Tests for ensure_cache_dir."""

    def test_creates_dir(self, tmp_path: Path) -> None:
        target = tmp_path / "cache" / "nested"
        result = ensure_cache_dir(target)
        assert result.exists()
        assert result.is_dir()

    def test_idempotent(self, tmp_path: Path) -> None:
        target = tmp_path / "cache"
        ensure_cache_dir(target)
        ensure_cache_dir(target)  # second call should not fail
        assert target.exists()


class TestGetCacheSizeBytes:
    """Tests for get_cache_size_bytes."""

    def test_empty_dir(self, tmp_path: Path) -> None:
        assert get_cache_size_bytes(tmp_path) == 0

    def test_with_files(self, tmp_path: Path) -> None:
        (tmp_path / "a.txt").write_bytes(b"hello")
        (tmp_path / "b.txt").write_bytes(b"world!")
        assert get_cache_size_bytes(tmp_path) == 11

    def test_nonexistent(self, tmp_path: Path) -> None:
        assert get_cache_size_bytes(tmp_path / "nope") == 0


class TestEnforceMaxCache:
    """Tests for enforce_max_cache — warning only, no deletion."""

    def test_under_limit(self, tmp_path: Path) -> None:
        # Should not raise or warn
        enforce_max_cache(tmp_path, max_bytes=999999)

    def test_over_limit_logs_warning(self, tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
        (tmp_path / "big.bin").write_bytes(b"X" * 100)
        import logging

        with caplog.at_level(logging.WARNING):
            enforce_max_cache(tmp_path, max_bytes=10)
        assert "exceeds maximum" in caplog.text


# ---------------------------------------------------------------------------
# Zip extraction tests
# ---------------------------------------------------------------------------


class TestExtractZipAtomically:
    """Tests for atomic zip extraction."""

    def _make_zip(self, tmp_path: Path, name: str = "model.zip") -> Path:
        zip_path = tmp_path / name
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("model/a.txt", b"content_a")
            zf.writestr("model/b.txt", b"content_b")
        return zip_path

    def test_basic_extraction(self, tmp_path: Path) -> None:
        zip_path = self._make_zip(tmp_path)
        target = tmp_path / "cache"
        result = extract_zip_atomically(zip_path, target)
        assert result.exists()
        assert (result / "a.txt").read_bytes() == b"content_a"
        assert (result / "b.txt").read_bytes() == b"content_b"

    def test_idempotent(self, tmp_path: Path) -> None:
        zip_path = self._make_zip(tmp_path)
        target = tmp_path / "cache"
        r1 = extract_zip_atomically(zip_path, target)
        r2 = extract_zip_atomically(zip_path, target)
        assert r1 == r2

    def test_selective_extraction(self, tmp_path: Path) -> None:
        zip_path = self._make_zip(tmp_path, name="selective.zip")
        target = tmp_path / "cache2"
        result = extract_zip_atomically(
            zip_path, target, required_names=["a.txt"]
        )
        assert (result / "a.txt").exists()
        assert not (result / "b.txt").exists()

    def test_no_temp_dir_on_success(self, tmp_path: Path) -> None:
        zip_path = self._make_zip(tmp_path)
        target = tmp_path / "cache3"
        extract_zip_atomically(zip_path, target)
        # Ensure no .tmp_ directories remain
        temps = list(target.glob(".tmp_*"))
        assert temps == []

    def test_corrupt_zip(self, tmp_path: Path) -> None:
        bad = tmp_path / "bad.zip"
        bad.write_bytes(b"not a zip")
        with pytest.raises(zipfile.BadZipFile):
            extract_zip_atomically(bad, tmp_path / "out")
