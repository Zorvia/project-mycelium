#!/usr/bin/env python3
# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""
seed_demo_data.py — Seed the backend SQLite database with demo data.

Usage:
    python scripts/seed_demo_data.py
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

# Add backend to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src" / "backend"))

from mycelium.config import load_config
from mycelium.database import init_db, close_db, get_session
from mycelium.models import Graph, Node, Edge

# ---------------------------------------------------------------------------
# Demo data
# ---------------------------------------------------------------------------

GRAPH = {
    "id": "demo-graph-001",
    "name": "Science Knowledge Graph",
    "description": "A demonstration knowledge graph spanning physics, mathematics, chemistry, biology, and computer science. Perfect for exploring cross-disciplinary connections.",
}

NODES = [
    {"id": "n01", "label": "Physics", "category": "physics", "description": "The fundamental science of matter, energy, and their interactions.", "position_x": 400.0, "position_y": 300.0},
    {"id": "n02", "label": "Quantum Mechanics", "category": "physics", "description": "The branch of physics dealing with phenomena at nanoscopic scales.", "position_x": 550.0, "position_y": 200.0},
    {"id": "n03", "label": "Thermodynamics", "category": "physics", "description": "The branch of physics dealing with heat, work, temperature, and energy.", "position_x": 300.0, "position_y": 450.0},
    {"id": "n04", "label": "Electromagnetism", "category": "physics", "description": "The study of electromagnetic force.", "position_x": 550.0, "position_y": 400.0},
    {"id": "n05", "label": "Mathematics", "category": "mathematics", "description": "The abstract science of number, quantity, and space.", "position_x": 200.0, "position_y": 250.0},
    {"id": "n06", "label": "Calculus", "category": "mathematics", "description": "The mathematical study of continuous change.", "position_x": 100.0, "position_y": 350.0},
    {"id": "n07", "label": "Linear Algebra", "category": "mathematics", "description": "Linear equations, vector spaces, and matrices.", "position_x": 100.0, "position_y": 180.0},
    {"id": "n08", "label": "Chemistry", "category": "chemistry", "description": "The scientific study of matter and its transformations.", "position_x": 650.0, "position_y": 300.0},
    {"id": "n09", "label": "Organic Chemistry", "category": "chemistry", "description": "The study of carbon-containing compounds.", "position_x": 750.0, "position_y": 200.0},
    {"id": "n10", "label": "Biochemistry", "category": "chemistry", "description": "Chemical processes in living organisms.", "position_x": 800.0, "position_y": 350.0},
    {"id": "n11", "label": "Biology", "category": "biology", "description": "The natural science that studies life and living organisms.", "position_x": 700.0, "position_y": 500.0},
    {"id": "n12", "label": "Genetics", "category": "biology", "description": "The study of genes, genetic variation, and heredity.", "position_x": 850.0, "position_y": 450.0},
    {"id": "n13", "label": "Ecology", "category": "biology", "description": "Relationships between organisms and their environment.", "position_x": 600.0, "position_y": 550.0},
    {"id": "n14", "label": "Computer Science", "category": "computer_science", "description": "The study of computation, automation, and information.", "position_x": 150.0, "position_y": 500.0},
    {"id": "n15", "label": "Algorithms", "category": "computer_science", "description": "Finite sequences of instructions for solving problems.", "position_x": 50.0, "position_y": 500.0},
    {"id": "n16", "label": "Machine Learning", "category": "computer_science", "description": "A subset of AI that enables learning from experience.", "position_x": 250.0, "position_y": 600.0},
    {"id": "n17", "label": "Cryptography", "category": "computer_science", "description": "Techniques for secure communication.", "position_x": 50.0, "position_y": 400.0},
    {"id": "n18", "label": "Optics", "category": "physics", "description": "The study of light and its interactions with matter.", "position_x": 650.0, "position_y": 150.0},
    {"id": "n19", "label": "Astronomy", "category": "astronomy", "description": "The study of celestial objects and space.", "position_x": 450.0, "position_y": 100.0},
    {"id": "n20", "label": "Cosmology", "category": "astronomy", "description": "The study of the origin and fate of the universe.", "position_x": 500.0, "position_y": 50.0},
    {"id": "n21", "label": "Statistics", "category": "mathematics", "description": "Collection, analysis, and interpretation of data.", "position_x": 200.0, "position_y": 100.0},
    {"id": "n22", "label": "Probability", "category": "mathematics", "description": "The analysis of random phenomena.", "position_x": 300.0, "position_y": 100.0},
    {"id": "n23", "label": "Earth Science", "category": "earth_science", "description": "The study of the Earth and its neighbors in space.", "position_x": 500.0, "position_y": 500.0},
    {"id": "n24", "label": "Geology", "category": "earth_science", "description": "The study of the solid Earth and its rocks.", "position_x": 450.0, "position_y": 600.0},
    {"id": "n25", "label": "Particle Physics", "category": "physics", "description": "The study of fundamental constituents of matter.", "position_x": 500.0, "position_y": 150.0},
]

EDGES = [
    {"id": "e01", "source": "n01", "target": "n02", "label": "includes", "weight": 1.5},
    {"id": "e02", "source": "n01", "target": "n03", "label": "includes", "weight": 1.5},
    {"id": "e03", "source": "n01", "target": "n04", "label": "includes", "weight": 1.5},
    {"id": "e04", "source": "n01", "target": "n18", "label": "includes", "weight": 1.0},
    {"id": "e05", "source": "n01", "target": "n25", "label": "includes", "weight": 1.0},
    {"id": "e06", "source": "n05", "target": "n06", "label": "includes", "weight": 1.5},
    {"id": "e07", "source": "n05", "target": "n07", "label": "includes", "weight": 1.5},
    {"id": "e08", "source": "n05", "target": "n21", "label": "includes", "weight": 1.0},
    {"id": "e09", "source": "n05", "target": "n22", "label": "includes", "weight": 1.0},
    {"id": "e10", "source": "n08", "target": "n09", "label": "includes", "weight": 1.5},
    {"id": "e11", "source": "n08", "target": "n10", "label": "includes", "weight": 1.5},
    {"id": "e12", "source": "n11", "target": "n12", "label": "includes", "weight": 1.5},
    {"id": "e13", "source": "n11", "target": "n13", "label": "includes", "weight": 1.5},
    {"id": "e14", "source": "n14", "target": "n15", "label": "includes", "weight": 1.5},
    {"id": "e15", "source": "n14", "target": "n16", "label": "includes", "weight": 1.5},
    {"id": "e16", "source": "n14", "target": "n17", "label": "includes", "weight": 1.0},
    {"id": "e17", "source": "n01", "target": "n05", "label": "depends_on", "weight": 2.0},
    {"id": "e18", "source": "n02", "target": "n07", "label": "requires", "weight": 1.5},
    {"id": "e19", "source": "n08", "target": "n01", "label": "related_to", "weight": 1.0},
    {"id": "e20", "source": "n10", "target": "n11", "label": "bridges", "weight": 1.5},
    {"id": "e21", "source": "n16", "target": "n21", "label": "uses", "weight": 1.5},
    {"id": "e22", "source": "n19", "target": "n01", "label": "depends_on", "weight": 1.5},
    {"id": "e23", "source": "n19", "target": "n20", "label": "includes", "weight": 1.5},
    {"id": "e24", "source": "n23", "target": "n24", "label": "includes", "weight": 1.5},
]


async def seed() -> None:
    """Insert demo data into the database."""
    cfg = load_config()
    await init_db(cfg)

    async with get_session() as session:
        # Check if graph already exists
        from sqlalchemy import select
        result = await session.execute(select(Graph).where(Graph.id == GRAPH["id"]))
        existing = result.scalar_one_or_none()
        if existing:
            print(f"⚠  Graph '{GRAPH['id']}' already exists — skipping seed.")
            await close_db()
            return

        # Insert graph
        graph = Graph(id=GRAPH["id"], name=GRAPH["name"], description=GRAPH["description"])
        session.add(graph)

        # Insert nodes
        for n in NODES:
            node = Node(
                id=n["id"],
                graph_id=GRAPH["id"],
                label=n["label"],
                category=n["category"],
                description=n["description"],
                position_x=n["position_x"],
                position_y=n["position_y"],
            )
            session.add(node)

        # Insert edges
        for e in EDGES:
            edge = Edge(
                id=e["id"],
                graph_id=GRAPH["id"],
                source_id=e["source"],
                target_id=e["target"],
                label=e["label"],
                weight=e["weight"],
            )
            session.add(edge)

        await session.commit()
        print(f"✓ Seeded {len(NODES)} nodes + {len(EDGES)} edges into '{GRAPH['name']}'")

    await close_db()


def main() -> None:
    asyncio.run(seed())


if __name__ == "__main__":
    main()
