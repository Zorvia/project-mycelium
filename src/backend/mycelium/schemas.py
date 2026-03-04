# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""Pydantic schemas for API request/response validation."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


# ─── Graph ───────────────────────────────────────────

class GraphCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    metadata: dict[str, Any] | None = None


class GraphUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    metadata: dict[str, Any] | None = None


class GraphResponse(BaseModel):
    id: str
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime
    node_count: int = 0
    edge_count: int = 0
    metadata: dict[str, Any] | None = None

    model_config = {"from_attributes": True}


# ─── Node ────────────────────────────────────────────

class NodeCreate(BaseModel):
    label: str = Field(..., min_length=1, max_length=255)
    category: str = Field(default="default", max_length=100)
    description: str | None = None
    position_x: float | None = None
    position_y: float | None = None
    metadata: dict[str, Any] | None = None


class NodeUpdate(BaseModel):
    label: str | None = Field(None, min_length=1, max_length=255)
    category: str | None = Field(None, max_length=100)
    description: str | None = None
    position_x: float | None = None
    position_y: float | None = None
    metadata: dict[str, Any] | None = None


class NodeResponse(BaseModel):
    id: str
    graph_id: str
    label: str
    category: str
    description: str | None
    position_x: float | None
    position_y: float | None
    cid: str | None
    metadata: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ─── Edge ────────────────────────────────────────────

class EdgeCreate(BaseModel):
    source_id: str
    target_id: str
    label: str = "related_to"
    weight: float = 1.0
    metadata: dict[str, Any] | None = None


class EdgeResponse(BaseModel):
    id: str
    graph_id: str
    source_id: str
    target_id: str
    label: str
    weight: float
    metadata: dict[str, Any] | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Search ──────────────────────────────────────────

class SearchQuery(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    graph_id: str | None = None
    category: str | None = None
    limit: int = Field(default=20, ge=1, le=100)


class SearchResult(BaseModel):
    nodes: list[NodeResponse]
    total: int


# ─── Export ──────────────────────────────────────────

class GraphExport(BaseModel):
    graph: GraphResponse
    nodes: list[NodeResponse]
    edges: list[EdgeResponse]


# ─── Health ──────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "1.0.0"
