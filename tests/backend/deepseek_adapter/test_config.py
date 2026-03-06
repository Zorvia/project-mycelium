# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""Unit tests for config module — no real model files needed."""

from __future__ import annotations

from pathlib import Path

from mycelium.ai.deepseek_adapter.config import (
    DEFAULT_CACHE_DIR,
    DEFAULT_MAX_CACHE_BYTES,
    DEFAULT_MIN_FREE_BYTES,
    EXPECTED_SHARDS,
    REQUIRED_CONFIG_FILES,
    TOKENIZER_FILES,
    AdapterConfig,
)


class TestAdapterConfig:
    """Tests for AdapterConfig dataclass."""

    def test_defaults(self) -> None:
        cfg = AdapterConfig(model_source="/tmp/model")
        assert cfg.device == "auto"
        assert cfg.min_free_bytes == DEFAULT_MIN_FREE_BYTES
        assert cfg.max_cache_bytes == DEFAULT_MAX_CACHE_BYTES
        assert cfg.use_zip_streaming is False
        assert cfg.checksums_file is None

    def test_resolved_model_source(self) -> None:
        cfg = AdapterConfig(model_source="/tmp/test_model")
        resolved = cfg.resolved_model_source
        assert isinstance(resolved, Path)
        assert resolved.is_absolute()

    def test_resolved_cache_dir_expands_tilde(self) -> None:
        cfg = AdapterConfig(model_source="/tmp/m", cache_dir="~/test_cache")
        resolved = cfg.resolved_cache_dir
        assert "~" not in str(resolved)
        assert resolved.is_absolute()

    def test_is_zip_source_true(self) -> None:
        cfg = AdapterConfig(model_source="/tmp/model.zip")
        assert cfg.is_zip_source is True

    def test_is_zip_source_false(self) -> None:
        cfg = AdapterConfig(model_source="/tmp/model_dir")
        assert cfg.is_zip_source is False

    def test_expected_shards_count(self) -> None:
        assert len(EXPECTED_SHARDS) == 2

    def test_required_config_files(self) -> None:
        assert "config.json" in REQUIRED_CONFIG_FILES

    def test_tokenizer_files(self) -> None:
        assert "tokenizer.json" in TOKENIZER_FILES

    def test_frozen(self) -> None:
        cfg = AdapterConfig(model_source="/tmp/m")
        try:
            cfg.device = "cpu"  # type: ignore[misc]
            assert False, "Should not be mutable"
        except AttributeError:
            pass
