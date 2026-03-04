# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""SQLAlchemy database models for the knowledge graph."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    JSON,
    LargeBinary,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, relationship


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _uuid() -> str:
    return str(uuid.uuid4())


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


class Graph(Base):
    """A knowledge graph container."""

    __tablename__ = "graphs"

    id = Column(String(36), primary_key=True, default=_uuid)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=_utcnow, nullable=False)
    updated_at = Column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow, nullable=False
    )
    crdt_state = Column(LargeBinary, nullable=True)
    metadata_ = Column("metadata", JSON, nullable=True, default=dict)

    nodes = relationship("Node", back_populates="graph", cascade="all, delete-orphan")
    edges = relationship("Edge", back_populates="graph", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Graph id={self.id!r} name={self.name!r}>"


class Node(Base):
    """A node in the knowledge graph."""

    __tablename__ = "nodes"
    __table_args__ = (
        Index("ix_nodes_graph_category", "graph_id", "category"),
        Index("ix_nodes_label", "label"),
    )

    id = Column(String(36), primary_key=True, default=_uuid)
    graph_id = Column(
        String(36), ForeignKey("graphs.id", ondelete="CASCADE"), nullable=False
    )
    label = Column(String(255), nullable=False)
    category = Column(String(100), nullable=True, default="default")
    description = Column(Text, nullable=True)
    position_x = Column(Float, nullable=True)
    position_y = Column(Float, nullable=True)
    cid = Column(String(64), nullable=True)
    chunk_ids = Column(JSON, nullable=True, default=list)
    metadata_ = Column("metadata", JSON, nullable=True, default=dict)
    created_at = Column(DateTime(timezone=True), default=_utcnow, nullable=False)
    updated_at = Column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow, nullable=False
    )

    graph = relationship("Graph", back_populates="nodes")
    outgoing_edges = relationship(
        "Edge",
        foreign_keys="Edge.source_id",
        back_populates="source",
        cascade="all, delete-orphan",
    )
    incoming_edges = relationship(
        "Edge",
        foreign_keys="Edge.target_id",
        back_populates="target",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Node id={self.id!r} label={self.label!r}>"


class Edge(Base):
    """An edge connecting two nodes in the knowledge graph."""

    __tablename__ = "edges"
    __table_args__ = (
        Index("ix_edges_source_target", "source_id", "target_id"),
        Index("ix_edges_graph", "graph_id"),
    )

    id = Column(String(36), primary_key=True, default=_uuid)
    graph_id = Column(
        String(36), ForeignKey("graphs.id", ondelete="CASCADE"), nullable=False
    )
    source_id = Column(
        String(36), ForeignKey("nodes.id", ondelete="CASCADE"), nullable=False
    )
    target_id = Column(
        String(36), ForeignKey("nodes.id", ondelete="CASCADE"), nullable=False
    )
    label = Column(String(255), nullable=True, default="related_to")
    weight = Column(Float, nullable=True, default=1.0)
    metadata_ = Column("metadata", JSON, nullable=True, default=dict)
    created_at = Column(DateTime(timezone=True), default=_utcnow, nullable=False)

    graph = relationship("Graph", back_populates="edges")
    source = relationship("Node", foreign_keys=[source_id], back_populates="outgoing_edges")
    target = relationship("Node", foreign_keys=[target_id], back_populates="incoming_edges")

    def __repr__(self) -> str:
        return f"<Edge {self.source_id!r} -> {self.target_id!r}>"


class Chunk(Base):
    """A content-addressed data chunk."""

    __tablename__ = "chunks"

    cid = Column(String(64), primary_key=True)
    data = Column(LargeBinary, nullable=False)
    size = Column(Float, nullable=False)
    encrypted = Column(String(5), nullable=False, default="false")
    created_at = Column(DateTime(timezone=True), default=_utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Chunk cid={self.cid!r} size={self.size}>"
