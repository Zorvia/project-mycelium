# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""
Integration tests — require real model files.

Gated by the ``MYCELIUM_MODEL_PATH`` environment variable.
Set it to the directory containing the DeepSeek-R1-Distill-Qwen-7B files.

Example::

    set MYCELIUM_MODEL_PATH=C:\\Users\\Laptop\\DeepSeek-R1-Distill-Qwen-7B
    pytest tests/backend/deepseek_adapter/test_integration.py -v
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

# Skip entire module if model path not set
MODEL_PATH = os.environ.get("MYCELIUM_MODEL_PATH")
pytestmark = pytest.mark.skipif(
    MODEL_PATH is None,
    reason="MYCELIUM_MODEL_PATH not set — skipping integration tests",
)


@pytest.fixture(scope="module")
def adapter():
    """Initialize the adapter once for all integration tests."""
    from mycelium.ai.deepseek_adapter import initialize

    a = initialize(MODEL_PATH, device="auto")
    yield a
    a.shutdown()


class TestIntegration:
    """Integration tests with real model files."""

    def test_status_loaded(self, adapter) -> None:
        status = adapter.status()
        assert status["loaded"] is True
        assert status["shards"] == 2
        assert len(status["files"]) == 2
        assert len(status["sha256"]) == 2
        assert status["device"] in ("cpu", "cuda")

    def test_predict_nonempty(self, adapter) -> None:
        result = adapter.predict("Hello", max_tokens=8)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_generate_stream(self, adapter) -> None:
        tokens = list(adapter.generate_stream("Hi", max_tokens=5))
        assert len(tokens) > 0
        assert all(isinstance(t, str) for t in tokens)

    def test_shutdown_and_reinitialize(self) -> None:
        from mycelium.ai.deepseek_adapter import initialize

        a1 = initialize(MODEL_PATH, device="auto")
        assert a1.status()["loaded"] is True
        a1.shutdown()
        assert a1.status()["loaded"] is False

        # Re-initialize should work cleanly
        a2 = initialize(MODEL_PATH, device="auto")
        assert a2.status()["loaded"] is True
        a2.shutdown()
