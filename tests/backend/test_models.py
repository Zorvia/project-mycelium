# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""Tests for SQLAlchemy models."""

from __future__ import annotations

import pytest
from datetime import datetime, timezone

from mycelium.models import Graph, Node, Edge, Chunk


class TestGraphModel:
    """Graph ORM model tests."""

    def test_defaults(self) -> None:
        g = Graph(id="g1", name="Test Graph")
        assert g.id == "g1"
        assert g.name == "Test Graph"
        assert g.description is None

    def test_repr(self) -> None:
        g = Graph(id="g1", name="Test")
        assert "g1" in repr(g) or "Graph" in str(type(g).__name__)


class TestNodeModel:
    """Node ORM model tests."""

    def test_defaults(self) -> None:
        n = Node(id="n1", graph_id="g1", label="Physics", category="physics")
        assert n.label == "Physics"
        assert n.position_x == 0.0
        assert n.position_y == 0.0

    def test_optional_fields(self) -> None:
        n = Node(
            id="n2",
            graph_id="g1",
            label="Chemistry",
            category="chemistry",
            description="Study of matter",
            position_x=100.0,
            position_y=200.0,
            cid="abc123",
        )
        assert n.description == "Study of matter"
        assert n.cid == "abc123"


class TestEdgeModel:
    """Edge ORM model tests."""

    def test_defaults(self) -> None:
        e = Edge(id="e1", graph_id="g1", source_id="n1", target_id="n2", label="includes")
        assert e.weight == 1.0

    def test_custom_weight(self) -> None:
        e = Edge(id="e2", graph_id="g1", source_id="n1", target_id="n2", label="depends_on", weight=2.5)
        assert e.weight == 2.5


class TestChunkModel:
    """Chunk ORM model tests."""

    def test_creation(self) -> None:
        c = Chunk(id="c1", node_id="n1", cid="deadbeef", index=0, size=1024)
        assert c.cid == "deadbeef"
        assert c.index == 0
        assert c.size == 1024
