# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""Graph service: CRUD operations and query logic."""

from __future__ import annotations

from functools import lru_cache
from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from mycelium.models import Edge, Graph, Node
from mycelium.schemas import (
    EdgeCreate,
    GraphCreate,
    GraphUpdate,
    NodeCreate,
    NodeUpdate,
)
from mycelium.chunking import chunk_data, compute_cid, create_cid_manifest


class GraphService:
    """Service layer for graph operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # ─── Graph CRUD ────────────────────────────────

    async def create_graph(self, data: GraphCreate) -> Graph:
        """Create a new knowledge graph."""
        graph = Graph(
            name=data.name,
            description=data.description,
            metadata_=data.metadata or {},
        )
        self._session.add(graph)
        await self._session.flush()
        return graph

    async def get_graph(self, graph_id: str) -> Graph | None:
        """Retrieve a graph by ID."""
        result = await self._session.execute(
            select(Graph)
            .options(selectinload(Graph.nodes), selectinload(Graph.edges))
            .where(Graph.id == graph_id)
        )
        return result.scalar_one_or_none()

    async def list_graphs(self) -> Sequence[Graph]:
        """List all graphs."""
        result = await self._session.execute(select(Graph).order_by(Graph.updated_at.desc()))
        return result.scalars().all()

    async def update_graph(self, graph_id: str, data: GraphUpdate) -> Graph | None:
        """Update a graph's metadata."""
        graph = await self.get_graph(graph_id)
        if graph is None:
            return None
        if data.name is not None:
            graph.name = data.name
        if data.description is not None:
            graph.description = data.description
        if data.metadata is not None:
            graph.metadata_ = data.metadata
        await self._session.flush()
        return graph

    async def delete_graph(self, graph_id: str) -> bool:
        """Delete a graph and all its nodes/edges."""
        graph = await self.get_graph(graph_id)
        if graph is None:
            return False
        await self._session.delete(graph)
        await self._session.flush()
        return True

    # ─── Node CRUD ─────────────────────────────────

    async def create_node(self, graph_id: str, data: NodeCreate) -> Node:
        """Create a new node in a graph."""
        # Compute CID from content
        content = f"{data.label}:{data.category}:{data.description or ''}".encode()
        cid = compute_cid(content)
        chunks = chunk_data(content)
        manifest = create_cid_manifest(chunks)

        node = Node(
            graph_id=graph_id,
            label=data.label,
            category=data.category,
            description=data.description,
            position_x=data.position_x,
            position_y=data.position_y,
            cid=cid,
            chunk_ids=[c["cid"] for c in manifest["chunks"]],
            metadata_=data.metadata or {},
        )
        self._session.add(node)
        await self._session.flush()
        return node

    async def get_node(self, node_id: str) -> Node | None:
        """Retrieve a node by ID."""
        result = await self._session.execute(select(Node).where(Node.id == node_id))
        return result.scalar_one_or_none()

    async def list_nodes(
        self, graph_id: str, category: str | None = None, limit: int = 500
    ) -> Sequence[Node]:
        """List nodes in a graph, optionally filtered by category."""
        q = select(Node).where(Node.graph_id == graph_id)
        if category:
            q = q.where(Node.category == category)
        q = q.limit(limit).order_by(Node.label)
        result = await self._session.execute(q)
        return result.scalars().all()

    async def update_node(self, node_id: str, data: NodeUpdate) -> Node | None:
        """Update a node's properties."""
        node = await self.get_node(node_id)
        if node is None:
            return None
        for field_name in ("label", "category", "description", "position_x", "position_y"):
            value = getattr(data, field_name, None)
            if value is not None:
                setattr(node, field_name, value)
        if data.metadata is not None:
            node.metadata_ = data.metadata
        # Recompute CID
        content = f"{node.label}:{node.category}:{node.description or ''}".encode()
        node.cid = compute_cid(content)
        await self._session.flush()
        return node

    async def delete_node(self, node_id: str) -> bool:
        """Delete a node and its edges."""
        node = await self.get_node(node_id)
        if node is None:
            return False
        await self._session.delete(node)
        await self._session.flush()
        return True

    async def search_nodes(
        self, query: str, graph_id: str | None = None, limit: int = 20
    ) -> Sequence[Node]:
        """Search nodes by label (case-insensitive)."""
        q = select(Node).where(Node.label.ilike(f"%{query}%"))
        if graph_id:
            q = q.where(Node.graph_id == graph_id)
        q = q.limit(limit).order_by(Node.label)
        result = await self._session.execute(q)
        return result.scalars().all()

    # ─── Edge CRUD ─────────────────────────────────

    async def create_edge(self, graph_id: str, data: EdgeCreate) -> Edge:
        """Create an edge between two nodes."""
        edge = Edge(
            graph_id=graph_id,
            source_id=data.source_id,
            target_id=data.target_id,
            label=data.label,
            weight=data.weight,
            metadata_=data.metadata or {},
        )
        self._session.add(edge)
        await self._session.flush()
        return edge

    async def list_edges(self, graph_id: str) -> Sequence[Edge]:
        """List all edges in a graph."""
        result = await self._session.execute(
            select(Edge).where(Edge.graph_id == graph_id).order_by(Edge.created_at)
        )
        return result.scalars().all()

    async def delete_edge(self, edge_id: str) -> bool:
        """Delete an edge."""
        result = await self._session.execute(select(Edge).where(Edge.id == edge_id))
        edge = result.scalar_one_or_none()
        if edge is None:
            return False
        await self._session.delete(edge)
        await self._session.flush()
        return True

    # ─── Statistics ────────────────────────────────

    async def get_stats(self, graph_id: str) -> dict:
        """Get statistics for a graph."""
        node_count = await self._session.execute(
            select(func.count()).select_from(Node).where(Node.graph_id == graph_id)
        )
        edge_count = await self._session.execute(
            select(func.count()).select_from(Edge).where(Edge.graph_id == graph_id)
        )
        categories = await self._session.execute(
            select(Node.category, func.count())
            .where(Node.graph_id == graph_id)
            .group_by(Node.category)
        )
        return {
            "node_count": node_count.scalar() or 0,
            "edge_count": edge_count.scalar() or 0,
            "categories": dict(categories.all()),
        }
