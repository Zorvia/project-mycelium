# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""Tests for Pydantic schemas."""

from __future__ import annotations

import pytest
from pydantic import ValidationError
from mycelium.schemas import (
    GraphCreate,
    GraphUpdate,
    NodeCreate,
    NodeUpdate,
    EdgeCreate,
    SearchQuery,
    HealthResponse,
)


class TestGraphSchemas:
    """Graph create / update schema tests."""

    def test_graph_create_minimal(self) -> None:
        g = GraphCreate(name="Test")
        assert g.name == "Test"
        assert g.description is None

    def test_graph_create_full(self) -> None:
        g = GraphCreate(name="Full", description="A full graph")
        assert g.description == "A full graph"

    def test_graph_update_partial(self) -> None:
        u = GraphUpdate(name="Updated")
        assert u.name == "Updated"
        assert u.description is None


class TestNodeSchemas:
    """Node create / update schema tests."""

    def test_node_create_minimal(self) -> None:
        n = NodeCreate(label="Physics", category="physics")
        assert n.position_x == 0.0
        assert n.position_y == 0.0

    def test_node_create_full(self) -> None:
        n = NodeCreate(
            label="Chemistry",
            category="chemistry",
            description="Study of matter",
            position_x=42.0,
            position_y=99.0,
        )
        assert n.position_x == 42.0

    def test_node_update_partial(self) -> None:
        u = NodeUpdate(label="New Label")
        assert u.label == "New Label"
        assert u.category is None

    def test_node_create_empty_label_rejected(self) -> None:
        with pytest.raises(ValidationError):
            NodeCreate(label="", category="physics")


class TestEdgeSchemas:
    """Edge create schema tests."""

    def test_edge_create(self) -> None:
        e = EdgeCreate(source_id="n1", target_id="n2", label="includes")
        assert e.weight == 1.0

    def test_edge_create_custom_weight(self) -> None:
        e = EdgeCreate(source_id="n1", target_id="n2", label="depends_on", weight=3.0)
        assert e.weight == 3.0


class TestSearchQuery:
    """Search query schema tests."""

    def test_defaults(self) -> None:
        q = SearchQuery(query="test")
        assert q.limit == 20

    def test_custom_limit(self) -> None:
        q = SearchQuery(query="physics", limit=5)
        assert q.limit == 5


class TestHealthResponse:
    """Health response schema tests."""

    def test_construction(self) -> None:
        h = HealthResponse(status="ok", version="1.0.0")
        assert h.status == "ok"
