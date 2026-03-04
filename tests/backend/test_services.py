# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""Tests for the GraphService (CRUD operations)."""

from __future__ import annotations

import asyncio
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from mycelium.models import Base
from mycelium.services import GraphService
from mycelium.schemas import GraphCreate, NodeCreate, NodeUpdate, EdgeCreate


@pytest_asyncio.fixture
async def session():
    """Create an in-memory SQLite async session for testing."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as sess:
        yield sess

    await engine.dispose()


@pytest_asyncio.fixture
async def service(session: AsyncSession):
    """Create a GraphService bound to the test session."""
    return GraphService(session)


@pytest.mark.asyncio
class TestGraphCRUD:
    """Graph create / read / update / delete."""

    async def test_create_graph(self, service: GraphService) -> None:
        g = await service.create_graph(GraphCreate(name="Test", description="A test graph"))
        assert g.name == "Test"
        assert g.id is not None

    async def test_get_graph(self, service: GraphService) -> None:
        created = await service.create_graph(GraphCreate(name="G"))
        fetched = await service.get_graph(created.id)
        assert fetched is not None
        assert fetched.name == "G"

    async def test_get_nonexistent(self, service: GraphService) -> None:
        fetched = await service.get_graph("nonexistent")
        assert fetched is None

    async def test_list_graphs(self, service: GraphService) -> None:
        await service.create_graph(GraphCreate(name="A"))
        await service.create_graph(GraphCreate(name="B"))
        graphs = await service.list_graphs()
        assert len(graphs) >= 2

    async def test_delete_graph(self, service: GraphService) -> None:
        g = await service.create_graph(GraphCreate(name="ToDelete"))
        deleted = await service.delete_graph(g.id)
        assert deleted is True
        assert await service.get_graph(g.id) is None


@pytest.mark.asyncio
class TestNodeCRUD:
    """Node create / read / update / delete."""

    async def test_create_node(self, service: GraphService) -> None:
        g = await service.create_graph(GraphCreate(name="G"))
        n = await service.create_node(g.id, NodeCreate(label="Physics", category="physics"))
        assert n.label == "Physics"
        assert n.graph_id == g.id

    async def test_update_node(self, service: GraphService) -> None:
        g = await service.create_graph(GraphCreate(name="G"))
        n = await service.create_node(g.id, NodeCreate(label="Old", category="general"))
        updated = await service.update_node(n.id, NodeUpdate(label="New"))
        assert updated is not None
        assert updated.label == "New"

    async def test_delete_node(self, service: GraphService) -> None:
        g = await service.create_graph(GraphCreate(name="G"))
        n = await service.create_node(g.id, NodeCreate(label="X", category="general"))
        deleted = await service.delete_node(n.id)
        assert deleted is True

    async def test_list_nodes(self, service: GraphService) -> None:
        g = await service.create_graph(GraphCreate(name="G"))
        await service.create_node(g.id, NodeCreate(label="A", category="physics"))
        await service.create_node(g.id, NodeCreate(label="B", category="chemistry"))
        nodes = await service.list_nodes(g.id)
        assert len(nodes) == 2


@pytest.mark.asyncio
class TestEdgeCRUD:
    """Edge create / read / delete."""

    async def test_create_edge(self, service: GraphService) -> None:
        g = await service.create_graph(GraphCreate(name="G"))
        n1 = await service.create_node(g.id, NodeCreate(label="A", category="general"))
        n2 = await service.create_node(g.id, NodeCreate(label="B", category="general"))
        e = await service.create_edge(g.id, EdgeCreate(source_id=n1.id, target_id=n2.id, label="links"))
        assert e.source_id == n1.id
        assert e.target_id == n2.id

    async def test_delete_edge(self, service: GraphService) -> None:
        g = await service.create_graph(GraphCreate(name="G"))
        n1 = await service.create_node(g.id, NodeCreate(label="A", category="general"))
        n2 = await service.create_node(g.id, NodeCreate(label="B", category="general"))
        e = await service.create_edge(g.id, EdgeCreate(source_id=n1.id, target_id=n2.id, label="links"))
        deleted = await service.delete_edge(e.id)
        assert deleted is True

    async def test_list_edges(self, service: GraphService) -> None:
        g = await service.create_graph(GraphCreate(name="G"))
        n1 = await service.create_node(g.id, NodeCreate(label="A", category="general"))
        n2 = await service.create_node(g.id, NodeCreate(label="B", category="general"))
        await service.create_edge(g.id, EdgeCreate(source_id=n1.id, target_id=n2.id, label="links"))
        edges = await service.list_edges(g.id)
        assert len(edges) == 1


@pytest.mark.asyncio
class TestSearch:
    """Search functionality tests."""

    async def test_search_by_label(self, service: GraphService) -> None:
        g = await service.create_graph(GraphCreate(name="G"))
        await service.create_node(g.id, NodeCreate(label="Quantum Mechanics", category="physics"))
        await service.create_node(g.id, NodeCreate(label="Biology", category="biology"))
        results = await service.search_nodes(g.id, "quantum")
        assert len(results) >= 1
        assert any("Quantum" in r.label for r in results)


@pytest.mark.asyncio
class TestStats:
    """Graph statistics tests."""

    async def test_graph_stats(self, service: GraphService) -> None:
        g = await service.create_graph(GraphCreate(name="G"))
        n1 = await service.create_node(g.id, NodeCreate(label="A", category="physics"))
        n2 = await service.create_node(g.id, NodeCreate(label="B", category="chemistry"))
        await service.create_edge(g.id, EdgeCreate(source_id=n1.id, target_id=n2.id, label="links"))
        stats = await service.get_stats(g.id)
        assert stats["node_count"] == 2
        assert stats["edge_count"] == 1
