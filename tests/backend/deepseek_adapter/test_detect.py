# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""Unit tests for model detection — uses dummy files, no real weights."""

from __future__ import annotations

import zipfile
from pathlib import Path

import pytest

from mycelium.ai.deepseek_adapter.config import (
    EXPECTED_SHARDS,
    REQUIRED_CONFIG_FILES,
    TOKENIZER_FILES,
    AdapterConfig,
)
from mycelium.ai.deepseek_adapter.detect import (
    DetectionResult,
    FileSystemProtocol,
    _validate_shard_set,
    detect_model_files,
)


# ---------------------------------------------------------------------------
# Mock filesystem
# ---------------------------------------------------------------------------


class MockFS:
    """In-memory filesystem mock for testing."""

    def __init__(self, files: dict[str, list[str]]) -> None:
        """files: mapping of dir-path-string → list of filenames."""
        self._files = files

    def exists(self, path: Path) -> bool:
        return str(path) in self._files

    def is_dir(self, path: Path) -> bool:
        return str(path) in self._files

    def is_file(self, path: Path) -> bool:
        return False  # We only mock directories for detection

    def list_dir(self, path: Path) -> list[str]:
        return self._files.get(str(path), [])


# ---------------------------------------------------------------------------
# Shard validation tests
# ---------------------------------------------------------------------------


class TestValidateShardSet:
    """Tests for _validate_shard_set."""

    def test_complete_set(self) -> None:
        errors = _validate_shard_set(list(EXPECTED_SHARDS))
        assert errors == []

    def test_empty(self) -> None:
        errors = _validate_shard_set([])
        assert len(errors) == 1
        assert "No safetensors" in errors[0]

    def test_incomplete(self) -> None:
        errors = _validate_shard_set(["model-00001-of-000002.safetensors"])
        assert len(errors) == 1
        assert "Incomplete" in errors[0]

    def test_invalid_names(self) -> None:
        errors = _validate_shard_set(["random_file.bin"])
        assert len(errors) == 1


# ---------------------------------------------------------------------------
# Detection result tests
# ---------------------------------------------------------------------------


class TestDetectionResult:
    """Tests for DetectionResult."""

    def test_ok_when_no_issues(self) -> None:
        r = DetectionResult()
        r.shards = list(EXPECTED_SHARDS)
        r.config_files = list(REQUIRED_CONFIG_FILES)
        r.tokenizer_files = ["tokenizer.json"]
        assert r.ok is True

    def test_not_ok_with_missing(self) -> None:
        r = DetectionResult()
        r.missing = ["config.json"]
        assert r.ok is False

    def test_raise_on_error(self) -> None:
        r = DetectionResult()
        r.missing = ["config.json"]
        with pytest.raises(FileNotFoundError, match="config.json"):
            r.raise_on_error()


# ---------------------------------------------------------------------------
# Full detection tests (directory)
# ---------------------------------------------------------------------------


class TestDetectDirectory:
    """Test detection against mock directory filesystem."""

    def _make_config(self, path: str) -> AdapterConfig:
        return AdapterConfig(model_source=path)

    def test_all_files_present(self) -> None:
        path = "/mock/model"
        files = {
            path: list(EXPECTED_SHARDS) + list(REQUIRED_CONFIG_FILES) + ["tokenizer.json"],
        }
        cfg = AdapterConfig(model_source=path)
        result = detect_model_files(cfg, fs=MockFS(files))
        assert result.ok
        assert len(result.shards) == 2
        assert len(result.config_files) == 1
        assert "tokenizer.json" in result.tokenizer_files

    def test_missing_shard(self) -> None:
        path = "/mock/model"
        files = {
            path: ["model-00001-of-000002.safetensors", "config.json", "tokenizer.json"],
        }
        cfg = AdapterConfig(model_source=path)
        result = detect_model_files(cfg, fs=MockFS(files))
        assert not result.ok
        assert "model-00002-of-000002.safetensors" in result.missing

    def test_missing_config(self) -> None:
        path = "/mock/model"
        files = {
            path: list(EXPECTED_SHARDS) + ["tokenizer.json"],
        }
        cfg = AdapterConfig(model_source=path)
        result = detect_model_files(cfg, fs=MockFS(files))
        assert not result.ok
        assert "config.json" in result.missing

    def test_missing_tokenizer(self) -> None:
        path = "/mock/model"
        files = {
            path: list(EXPECTED_SHARDS) + list(REQUIRED_CONFIG_FILES),
        }
        cfg = AdapterConfig(model_source=path)
        result = detect_model_files(cfg, fs=MockFS(files))
        assert not result.ok
        assert any("tokenizer" in m for m in result.missing)

    def test_nonexistent_source(self) -> None:
        cfg = AdapterConfig(model_source="/nonexistent/path")
        result = detect_model_files(cfg, fs=MockFS({}))
        assert not result.ok
        assert any("does not exist" in e for e in result.errors)


# ---------------------------------------------------------------------------
# Detection tests (zip)
# ---------------------------------------------------------------------------


class TestDetectZip:
    """Test detection against real temporary zip files."""

    def test_valid_zip(self, tmp_path: Path) -> None:
        zip_path = tmp_path / "model.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            for shard in EXPECTED_SHARDS:
                zf.writestr(f"model/{shard}", b"DUMMY")
            for cfg in REQUIRED_CONFIG_FILES:
                zf.writestr(f"model/{cfg}", b"{}")
            zf.writestr("model/tokenizer.json", b"{}")

        cfg = AdapterConfig(model_source=str(zip_path))
        result = detect_model_files(cfg)
        assert result.ok
        assert result.is_zip

    def test_incomplete_zip(self, tmp_path: Path) -> None:
        zip_path = tmp_path / "model.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("model/model-00001-of-000002.safetensors", b"DUMMY")
            zf.writestr("model/config.json", b"{}")

        cfg = AdapterConfig(model_source=str(zip_path))
        result = detect_model_files(cfg)
        assert not result.ok

    def test_corrupt_zip(self, tmp_path: Path) -> None:
        zip_path = tmp_path / "bad.zip"
        zip_path.write_bytes(b"not a zip")

        cfg = AdapterConfig(model_source=str(zip_path))
        result = detect_model_files(cfg)
        assert not result.ok
        assert any("Cannot read zip" in e for e in result.errors)
