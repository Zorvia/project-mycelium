# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""
DeepSeek R1 Distill (Qwen-7B) Adapter for Project Mycelium.

Provides local, offline inference using the DeepSeek-R1-Distill-Qwen-7B model.
No network access is required or performed at runtime.

Quick start::

    from mycelium.ai.deepseek_adapter import initialize

    adapter = initialize("path/to/DeepSeek-R1-Distill-Qwen-7B")
    print(adapter.status())
    result = adapter.predict("Explain knowledge graphs.", max_tokens=128)
    print(result)
    adapter.shutdown()
"""

from mycelium.ai.deepseek_adapter.api import Adapter, initialize

__all__ = ["Adapter", "initialize"]
