# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""Unit tests for verification module — uses dummy files, no real weights."""

from __future__ import annotations

import io
import json
from pathlib import Path

import pytest

from mycelium.ai.deepseek_adapter.config import AdapterConfig
from mycelium.ai.deepseek_adapter.verify import (
    check_disk_space,
    compute_sha256,
    load_checksums,
    verify_checksums,
)


# ---------------------------------------------------------------------------
# Mock IO for hash tests
# ---------------------------------------------------------------------------


class MockHashIO:
    """Mock IO that returns deterministic content."""

    def __init__(self, content: bytes = b"test content") -> None:
        self._content = content

    def open_read(self, path: Path) -> io.BytesIO:
        return io.BytesIO(self._content)

    def file_size(self, path: Path) -> int:
        return len(self._content)


# ---------------------------------------------------------------------------
# SHA-256 tests
# ---------------------------------------------------------------------------


class TestComputeSha256:
    """Tests for streaming SHA-256 computation."""

    def test_known_hash(self) -> None:
        """SHA-256 of b'hello' is well-known."""
        import hashlib

        expected = hashlib.sha256(b"hello").hexdigest()
        result = compute_sha256(Path("dummy"), io=MockHashIO(b"hello"))
        assert result == expected

    def test_empty_content(self) -> None:
        import hashlib

        expected = hashlib.sha256(b"").hexdigest()
        result = compute_sha256(Path("dummy"), io=MockHashIO(b""))
        assert result == expected

    def test_large_content(self) -> None:
        """Test with content larger than default chunk size."""
        import hashlib

        content = b"A" * (10 * 1024 * 1024)  # 10 MiB
        expected = hashlib.sha256(content).hexdigest()
        result = compute_sha256(
            Path("dummy"), io=MockHashIO(content), chunk_size=1024 * 1024
        )
        assert result == expected


# ---------------------------------------------------------------------------
# Checksum loading tests
# ---------------------------------------------------------------------------


class TestLoadChecksums:
    """Tests for loading checksum files."""

    def test_valid_json(self, tmp_path: Path) -> None:
        checksums = {
            "model-00001-of-000002.safetensors": "aabbcc",
            "model-00002-of-000002.safetensors": "ddeeff",
        }
        f = tmp_path / "checksums.json"
        f.write_text(json.dumps(checksums), encoding="utf-8")
        result = load_checksums(f)
        assert result["model-00001-of-000002.safetensors"] == "aabbcc"

    def test_missing_file(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            load_checksums(tmp_path / "nope.json")

    def test_invalid_json(self, tmp_path: Path) -> None:
        f = tmp_path / "bad.json"
        f.write_text("not json", encoding="utf-8")
        with pytest.raises(ValueError, match="not valid JSON"):
            load_checksums(f)

    def test_wrong_structure(self, tmp_path: Path) -> None:
        f = tmp_path / "list.json"
        f.write_text("[1, 2, 3]", encoding="utf-8")
        with pytest.raises(ValueError, match="JSON object"):
            load_checksums(f)


# ---------------------------------------------------------------------------
# Checksum comparison tests
# ---------------------------------------------------------------------------


class TestVerifyChecksums:
    """Tests for checksum comparison."""

    def test_matching(self) -> None:
        actual = {"a.safetensors": "abc123"}
        expected = {"a.safetensors": "abc123"}
        errors = verify_checksums(actual, expected)
        assert errors == []

    def test_mismatch(self) -> None:
        actual = {"a.safetensors": "abc123"}
        expected = {"a.safetensors": "wrong"}
        errors = verify_checksums(actual, expected)
        assert len(errors) == 1
        assert "mismatch" in errors[0].lower()

    def test_missing_from_actual(self) -> None:
        actual = {}
        expected = {"a.safetensors": "abc123"}
        errors = verify_checksums(actual, expected)
        assert len(errors) == 1
        assert "not hashed" in errors[0]


# ---------------------------------------------------------------------------
# Disk space tests
# ---------------------------------------------------------------------------


class TestCheckDiskSpace:
    """Tests for disk space verification."""

    def test_sufficient_space(self, tmp_path: Path) -> None:
        """Should not raise if space is sufficient (tmpdir always has some)."""
        check_disk_space(tmp_path, min_free_bytes=1)

    def test_insufficient_space(self, tmp_path: Path) -> None:
        """Request absurdly large space to trigger failure."""
        with pytest.raises(OSError, match="Insufficient disk space"):
            check_disk_space(tmp_path, min_free_bytes=2**62)

    def test_nonexistent_dir_walks_up(self, tmp_path: Path) -> None:
        """Should walk up to find an existing parent."""
        deep = tmp_path / "a" / "b" / "c"
        check_disk_space(deep, min_free_bytes=1)
