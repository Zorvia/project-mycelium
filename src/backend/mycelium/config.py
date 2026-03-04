# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""Application configuration with environment variable support."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = ROOT_DIR / "data"


@dataclass(frozen=True)
class Config:
    """Immutable application configuration."""

    env: str = field(default_factory=lambda: os.getenv("MYCELIUM_ENV", "development"))
    db_url: str = field(
        default_factory=lambda: os.getenv(
            "MYCELIUM_DB_URL", f"sqlite+aiosqlite:///{DATA_DIR / 'mycelium.db'}"
        )
    )
    secret_key: str = field(
        default_factory=lambda: os.getenv(
            "MYCELIUM_SECRET_KEY", "dev-secret-change-in-production"
        )
    )
    cors_origins: list[str] = field(
        default_factory=lambda: os.getenv(
            "MYCELIUM_CORS_ORIGINS", "http://localhost:3000"
        ).split(",")
    )
    log_level: str = field(
        default_factory=lambda: os.getenv("MYCELIUM_LOG_LEVEL", "info")
    )
    cache_size: int = field(
        default_factory=lambda: int(os.getenv("MYCELIUM_CACHE_SIZE", "128"))
    )
    db_pool_size: int = field(
        default_factory=lambda: int(os.getenv("MYCELIUM_DB_POOL_SIZE", "5"))
    )
    max_graph_nodes: int = field(
        default_factory=lambda: int(os.getenv("MYCELIUM_MAX_GRAPH_NODES", "500"))
    )
    admin_enabled: bool = field(
        default_factory=lambda: os.getenv("MYCELIUM_ADMIN_ENABLED", "false").lower()
        == "true"
    )
    p2p_enabled: bool = field(
        default_factory=lambda: os.getenv("MYCELIUM_P2P_ENABLED", "true").lower()
        == "true"
    )
    chunk_size: int = field(
        default_factory=lambda: int(os.getenv("MYCELIUM_CHUNK_SIZE", str(256 * 1024)))
    )
    data_dir: Path = field(default_factory=lambda: DATA_DIR)

    @property
    def is_production(self) -> bool:
        return self.env == "production"

    @property
    def is_development(self) -> bool:
        return self.env == "development"


def get_config() -> Config:
    """Create configuration from environment variables."""
    return Config()


# Alias for backward compatibility with seed script
load_config = get_config
