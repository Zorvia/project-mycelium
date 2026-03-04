# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""FastAPI application — main entry point."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles

from mycelium import __version__
from mycelium.config import get_config
from mycelium.database import close_db, init_db
from mycelium.routes import router

config = get_config()

logging.basicConfig(
    level=getattr(logging, config.log_level.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("mycelium")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events."""
    logger.info("Starting Project Mycelium v%s", __version__)
    config.data_dir.mkdir(parents=True, exist_ok=True)
    await init_db()
    logger.info("Database initialized")
    yield
    await close_db()
    logger.info("Shutdown complete")


app = FastAPI(
    title="Project Mycelium",
    description="Nurturing Knowledge Without the Cloud — API",
    version=__version__,
    license_info={"name": "ZPL-2.0", "url": "https://github.com/Zorvia/project-mycelium/blob/main/LICENSE.md"},
    lifespan=lifespan,
    docs_url="/docs" if config.is_development else None,
    redoc_url="/redoc" if config.is_development else None,
)

# ─── Middleware ──────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=500)

# ─── Routes ─────────────────────────────────────

app.include_router(router, prefix="/api")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": __version__}


# ─── Static Files (production) ──────────────────

frontend_dist = Path(__file__).parent.parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="static")
