# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""
Adapter configuration — typed settings for model detection, loading, and caching.

Settings are resolved in priority order:
  1. Explicit keyword arguments to ``initialize()``
  2. Environment variables (``MYCELIUM_AI_*``)
  3. Defaults defined here
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: Expected model shard filenames (order matters for detection).
EXPECTED_SHARDS: Final[tuple[str, ...]] = (
    "model-00001-of-000002.safetensors",
    "model-00002-of-000002.safetensors",
)

#: Required non-weight files that must accompany the shards.
REQUIRED_CONFIG_FILES: Final[tuple[str, ...]] = (
    "config.json",
)

#: Tokenizer files — at least one must be present.
TOKENIZER_FILES: Final[tuple[str, ...]] = (
    "tokenizer.json",
    "tokenizer_config.json",
    "tokenizer.model",
)

#: Shard naming regex for detection.
SHARD_PATTERN: Final[str] = r"^model-\d{5}-of-\d{5,6}\.safetensors$"

#: Default cache directory (under user home).
DEFAULT_CACHE_DIR: Final[str] = os.path.join("~", ".mycelium", "ai_cache")

#: Minimum free disk bytes before extraction (default 1 GB).
DEFAULT_MIN_FREE_BYTES: Final[int] = 1_073_741_824

#: Maximum cache size (default 32 GB).
DEFAULT_MAX_CACHE_BYTES: Final[int] = 34_359_738_368

#: Hash algorithm used for verification.
HASH_ALGORITHM: Final[str] = "sha256"

#: Streaming hash read chunk size (8 MiB).
HASH_CHUNK_SIZE: Final[int] = 8 * 1024 * 1024


# ---------------------------------------------------------------------------
# Configuration dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AdapterConfig:
    """Immutable adapter configuration.

    Attributes:
        model_source: Path to directory or ``.zip`` containing model files.
        cache_dir: Directory for extracted/cached model files.
        device: Target device — ``"cpu"``, ``"cuda"``, or ``"auto"``
            (auto-detect GPU, fall back to CPU).
        use_zip_streaming: If *True* and *model_source* is a zip, attempt to
            stream weights directly from the archive (experimental).
        max_cache_bytes: Maximum total bytes allowed in *cache_dir*.
        min_free_bytes: Minimum free disk space required before extraction.
        checksums_file: Optional path to a file with expected SHA-256 hashes.
    """

    model_source: str = field(
        default_factory=lambda: os.getenv("MYCELIUM_AI_MODEL_SOURCE", "")
    )
    cache_dir: str = field(
        default_factory=lambda: os.getenv("MYCELIUM_AI_CACHE_DIR", DEFAULT_CACHE_DIR)
    )
    device: str = field(
        default_factory=lambda: os.getenv("MYCELIUM_AI_DEVICE", "auto")
    )
    use_zip_streaming: bool = False
    max_cache_bytes: int = DEFAULT_MAX_CACHE_BYTES
    min_free_bytes: int = DEFAULT_MIN_FREE_BYTES
    checksums_file: str | None = None

    # ------------------------------------------------------------------
    # Derived helpers
    # ------------------------------------------------------------------

    @property
    def resolved_cache_dir(self) -> Path:
        """Return *cache_dir* with ``~`` expanded and resolved."""
        return Path(self.cache_dir).expanduser().resolve()

    @property
    def resolved_model_source(self) -> Path:
        """Return *model_source* with ``~`` expanded and resolved."""
        return Path(self.model_source).expanduser().resolve()

    @property
    def is_zip_source(self) -> bool:
        """Return *True* if *model_source* points to a ``.zip`` file."""
        return self.resolved_model_source.suffix.lower() == ".zip"
