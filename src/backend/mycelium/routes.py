# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""API routes for the knowledge graph."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from mycelium.database import get_db
from mycelium.schemas import (
    EdgeCreate,
    EdgeResponse,
    GraphCreate,
    GraphExport,
    GraphResponse,
    GraphUpdate,
    NodeCreate,
    NodeResponse,
    NodeUpdate,
    SearchQuery,
    SearchResult,
)
from mycelium.services import GraphService

router = APIRouter(tags=["graph"])


def _get_service(session: AsyncSession = Depends(get_db)) -> GraphService:
    return GraphService(session)


# ─── Graphs ─────────────────────────────────────

@router.post("/graphs", response_model=GraphResponse, status_code=status.HTTP_201_CREATED)
async def create_graph(
    data: GraphCreate, service: GraphService = Depends(_get_service)
):
    """Create a new knowledge graph."""
    graph = await service.create_graph(data)
    stats = await service.get_stats(graph.id)
    return GraphResponse(
        id=graph.id,
        name=graph.name,
        description=graph.description,
        created_at=graph.created_at,
        updated_at=graph.updated_at,
        node_count=stats["node_count"],
        edge_count=stats["edge_count"],
        metadata=graph.metadata_,
    )


@router.get("/graphs", response_model=list[GraphResponse])
async def list_graphs(service: GraphService = Depends(_get_service)):
    """List all knowledge graphs."""
    graphs = await service.list_graphs()
    result = []
    for graph in graphs:
        stats = await service.get_stats(graph.id)
        result.append(
            GraphResponse(
                id=graph.id,
                name=graph.name,
                description=graph.description,
                created_at=graph.created_at,
                updated_at=graph.updated_at,
                node_count=stats["node_count"],
                edge_count=stats["edge_count"],
                metadata=graph.metadata_,
            )
        )
    return result


@router.get("/graphs/{graph_id}", response_model=GraphResponse)
async def get_graph(graph_id: str, service: GraphService = Depends(_get_service)):
    """Retrieve a specific knowledge graph."""
    graph = await service.get_graph(graph_id)
    if graph is None:
        raise HTTPException(status_code=404, detail="Graph not found")
    stats = await service.get_stats(graph.id)
    return GraphResponse(
        id=graph.id,
        name=graph.name,
        description=graph.description,
        created_at=graph.created_at,
        updated_at=graph.updated_at,
        node_count=stats["node_count"],
        edge_count=stats["edge_count"],
        metadata=graph.metadata_,
    )


@router.patch("/graphs/{graph_id}", response_model=GraphResponse)
async def update_graph(
    graph_id: str, data: GraphUpdate, service: GraphService = Depends(_get_service)
):
    """Update a knowledge graph."""
    graph = await service.update_graph(graph_id, data)
    if graph is None:
        raise HTTPException(status_code=404, detail="Graph not found")
    stats = await service.get_stats(graph.id)
    return GraphResponse(
        id=graph.id,
        name=graph.name,
        description=graph.description,
        created_at=graph.created_at,
        updated_at=graph.updated_at,
        node_count=stats["node_count"],
        edge_count=stats["edge_count"],
        metadata=graph.metadata_,
    )


@router.delete("/graphs/{graph_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_graph(graph_id: str, service: GraphService = Depends(_get_service)):
    """Delete a knowledge graph."""
    if not await service.delete_graph(graph_id):
        raise HTTPException(status_code=404, detail="Graph not found")


# ─── Nodes ──────────────────────────────────────

@router.post(
    "/graphs/{graph_id}/nodes",
    response_model=NodeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_node(
    graph_id: str, data: NodeCreate, service: GraphService = Depends(_get_service)
):
    """Create a new node in a graph."""
    node = await service.create_node(graph_id, data)
    return NodeResponse(
        id=node.id,
        graph_id=node.graph_id,
        label=node.label,
        category=node.category,
        description=node.description,
        position_x=node.position_x,
        position_y=node.position_y,
        cid=node.cid,
        metadata=node.metadata_,
        created_at=node.created_at,
        updated_at=node.updated_at,
    )


@router.get("/graphs/{graph_id}/nodes", response_model=list[NodeResponse])
async def list_nodes(
    graph_id: str,
    category: str | None = None,
    limit: int = 500,
    service: GraphService = Depends(_get_service),
):
    """List nodes in a graph."""
    nodes = await service.list_nodes(graph_id, category=category, limit=limit)
    return [
        NodeResponse(
            id=n.id,
            graph_id=n.graph_id,
            label=n.label,
            category=n.category,
            description=n.description,
            position_x=n.position_x,
            position_y=n.position_y,
            cid=n.cid,
            metadata=n.metadata_,
            created_at=n.created_at,
            updated_at=n.updated_at,
        )
        for n in nodes
    ]


@router.get("/nodes/{node_id}", response_model=NodeResponse)
async def get_node(node_id: str, service: GraphService = Depends(_get_service)):
    """Retrieve a specific node."""
    node = await service.get_node(node_id)
    if node is None:
        raise HTTPException(status_code=404, detail="Node not found")
    return NodeResponse(
        id=node.id,
        graph_id=node.graph_id,
        label=node.label,
        category=node.category,
        description=node.description,
        position_x=node.position_x,
        position_y=node.position_y,
        cid=node.cid,
        metadata=node.metadata_,
        created_at=node.created_at,
        updated_at=node.updated_at,
    )


@router.patch("/nodes/{node_id}", response_model=NodeResponse)
async def update_node(
    node_id: str, data: NodeUpdate, service: GraphService = Depends(_get_service)
):
    """Update a node."""
    node = await service.update_node(node_id, data)
    if node is None:
        raise HTTPException(status_code=404, detail="Node not found")
    return NodeResponse(
        id=node.id,
        graph_id=node.graph_id,
        label=node.label,
        category=node.category,
        description=node.description,
        position_x=node.position_x,
        position_y=node.position_y,
        cid=node.cid,
        metadata=node.metadata_,
        created_at=node.created_at,
        updated_at=node.updated_at,
    )


@router.delete("/nodes/{node_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_node(node_id: str, service: GraphService = Depends(_get_service)):
    """Delete a node."""
    if not await service.delete_node(node_id):
        raise HTTPException(status_code=404, detail="Node not found")


# ─── Edges ──────────────────────────────────────

@router.post(
    "/graphs/{graph_id}/edges",
    response_model=EdgeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_edge(
    graph_id: str, data: EdgeCreate, service: GraphService = Depends(_get_service)
):
    """Create an edge between two nodes."""
    edge = await service.create_edge(graph_id, data)
    return EdgeResponse(
        id=edge.id,
        graph_id=edge.graph_id,
        source_id=edge.source_id,
        target_id=edge.target_id,
        label=edge.label,
        weight=edge.weight,
        metadata=edge.metadata_,
        created_at=edge.created_at,
    )


@router.get("/graphs/{graph_id}/edges", response_model=list[EdgeResponse])
async def list_edges(
    graph_id: str, service: GraphService = Depends(_get_service)
):
    """List edges in a graph."""
    edges = await service.list_edges(graph_id)
    return [
        EdgeResponse(
            id=e.id,
            graph_id=e.graph_id,
            source_id=e.source_id,
            target_id=e.target_id,
            label=e.label,
            weight=e.weight,
            metadata=e.metadata_,
            created_at=e.created_at,
        )
        for e in edges
    ]


@router.delete("/edges/{edge_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_edge(edge_id: str, service: GraphService = Depends(_get_service)):
    """Delete an edge."""
    if not await service.delete_edge(edge_id):
        raise HTTPException(status_code=404, detail="Edge not found")


# ─── Search ─────────────────────────────────────

@router.post("/search", response_model=SearchResult)
async def search_nodes(
    query: SearchQuery, service: GraphService = Depends(_get_service)
):
    """Search nodes by label."""
    nodes = await service.search_nodes(
        query.query, graph_id=query.graph_id, limit=query.limit
    )
    return SearchResult(
        nodes=[
            NodeResponse(
                id=n.id,
                graph_id=n.graph_id,
                label=n.label,
                category=n.category,
                description=n.description,
                position_x=n.position_x,
                position_y=n.position_y,
                cid=n.cid,
                metadata=n.metadata_,
                created_at=n.created_at,
                updated_at=n.updated_at,
            )
            for n in nodes
        ],
        total=len(nodes),
    )


# ─── Export ─────────────────────────────────────

@router.get("/graphs/{graph_id}/export", response_model=GraphExport)
async def export_graph(
    graph_id: str, service: GraphService = Depends(_get_service)
):
    """Export a complete graph with all nodes and edges."""
    graph = await service.get_graph(graph_id)
    if graph is None:
        raise HTTPException(status_code=404, detail="Graph not found")
    stats = await service.get_stats(graph.id)
    nodes = await service.list_nodes(graph_id)
    edges = await service.list_edges(graph_id)
    return GraphExport(
        graph=GraphResponse(
            id=graph.id,
            name=graph.name,
            description=graph.description,
            created_at=graph.created_at,
            updated_at=graph.updated_at,
            node_count=stats["node_count"],
            edge_count=stats["edge_count"],
            metadata=graph.metadata_,
        ),
        nodes=[
            NodeResponse(
                id=n.id,
                graph_id=n.graph_id,
                label=n.label,
                category=n.category,
                description=n.description,
                position_x=n.position_x,
                position_y=n.position_y,
                cid=n.cid,
                metadata=n.metadata_,
                created_at=n.created_at,
                updated_at=n.updated_at,
            )
            for n in nodes
        ],
        edges=[
            EdgeResponse(
                id=e.id,
                graph_id=e.graph_id,
                source_id=e.source_id,
                target_id=e.target_id,
                label=e.label,
                weight=e.weight,
                metadata=e.metadata_,
                created_at=e.created_at,
            )
            for e in edges
        ],
    )
