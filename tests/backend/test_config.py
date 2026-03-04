# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""Tests for configuration loading."""

from __future__ import annotations

import os
import pytest
from mycelium.config import load_config


class TestConfig:
    """Configuration tests."""

    def test_defaults(self) -> None:
        cfg = load_config()
        assert cfg.env in ("development", "production", "test")
        assert cfg.host == "0.0.0.0"
        assert cfg.port == 8000

    def test_env_override(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("MYCELIUM_ENV", "test")
        monkeypatch.setenv("MYCELIUM_PORT", "9000")
        cfg = load_config()
        assert cfg.env == "test"
        assert cfg.port == 9000

    def test_db_url_default(self) -> None:
        cfg = load_config()
        assert "sqlite" in cfg.db_url
