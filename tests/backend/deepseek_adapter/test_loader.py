# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""Unit tests for the loader module — no real model files required."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest


class TestResolveDevice:
    """Tests for device resolution logic."""

    def test_cpu_explicit(self) -> None:
        with patch.dict("sys.modules", {"torch": MagicMock()}):
            from mycelium.ai.deepseek_adapter.loader import resolve_device

            result = resolve_device("cpu")
        assert result == "cpu"

    def test_auto_no_cuda(self) -> None:
        mock_torch = MagicMock()
        mock_torch.cuda.is_available.return_value = False
        with patch.dict("sys.modules", {"torch": mock_torch}):
            from mycelium.ai.deepseek_adapter import loader

            # Force reimport
            import importlib

            importlib.reload(loader)
            result = loader.resolve_device("auto")
        assert result == "cpu"

    def test_auto_with_cuda(self) -> None:
        mock_torch = MagicMock()
        mock_torch.cuda.is_available.return_value = True
        with patch.dict("sys.modules", {"torch": mock_torch}):
            from mycelium.ai.deepseek_adapter import loader

            import importlib

            importlib.reload(loader)
            result = loader.resolve_device("auto")
        assert result == "cuda"

    def test_cuda_unavailable_raises(self) -> None:
        mock_torch = MagicMock()
        mock_torch.cuda.is_available.return_value = False
        with patch.dict("sys.modules", {"torch": mock_torch}):
            from mycelium.ai.deepseek_adapter import loader

            import importlib

            importlib.reload(loader)
            with pytest.raises(RuntimeError, match="CUDA is not available"):
                loader.resolve_device("cuda")
