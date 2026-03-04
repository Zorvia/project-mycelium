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
export_demo.py — Generate a single-file offline demo HTML.

Usage:
    python scripts/export_demo.py

Produces:
    demo/mycelium_demo.html
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import textwrap
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "demo"
OUT_FILE = OUT_DIR / "mycelium_demo.html"

# ---------------------------------------------------------------------------
# Demo data  (mirrors src/frontend/src/demoData.ts)
# ---------------------------------------------------------------------------

DEMO_NODES = [
    {"id": "n01", "label": "Physics", "category": "physics", "description": "The fundamental science of matter, energy, and their interactions.", "x": 400, "y": 300},
    {"id": "n02", "label": "Quantum Mechanics", "category": "physics", "description": "The branch of physics dealing with phenomena at nanoscopic scales.", "x": 550, "y": 200},
    {"id": "n03", "label": "Thermodynamics", "category": "physics", "description": "The branch of physics dealing with heat, work, temperature, and energy.", "x": 300, "y": 450},
    {"id": "n04", "label": "Electromagnetism", "category": "physics", "description": "The study of electromagnetic force.", "x": 550, "y": 400},
    {"id": "n05", "label": "Mathematics", "category": "mathematics", "description": "The abstract science of number, quantity, and space.", "x": 200, "y": 250},
    {"id": "n06", "label": "Calculus", "category": "mathematics", "description": "The mathematical study of continuous change.", "x": 100, "y": 350},
    {"id": "n07", "label": "Linear Algebra", "category": "mathematics", "description": "The branch of mathematics concerning linear equations and vector spaces.", "x": 100, "y": 180},
    {"id": "n08", "label": "Chemistry", "category": "chemistry", "description": "The scientific study of matter and its transformations.", "x": 650, "y": 300},
    {"id": "n09", "label": "Organic Chemistry", "category": "chemistry", "description": "The study of carbon-containing compounds.", "x": 750, "y": 200},
    {"id": "n10", "label": "Biochemistry", "category": "chemistry", "description": "The study of chemical processes in living organisms.", "x": 800, "y": 350},
    {"id": "n11", "label": "Biology", "category": "biology", "description": "The natural science that studies life and living organisms.", "x": 700, "y": 500},
    {"id": "n12", "label": "Genetics", "category": "biology", "description": "The study of genes, genetic variation, and heredity.", "x": 850, "y": 450},
    {"id": "n13", "label": "Ecology", "category": "biology", "description": "The study of relationships between organisms and their environment.", "x": 600, "y": 550},
    {"id": "n14", "label": "Computer Science", "category": "computer_science", "description": "The study of computation, automation, and information.", "x": 150, "y": 500},
    {"id": "n15", "label": "Algorithms", "category": "computer_science", "description": "A finite sequence of instructions for solving problems.", "x": 50, "y": 500},
    {"id": "n16", "label": "Machine Learning", "category": "computer_science", "description": "A subset of AI that enables learning from experience.", "x": 250, "y": 600},
    {"id": "n17", "label": "Cryptography", "category": "computer_science", "description": "Techniques for secure communication.", "x": 50, "y": 400},
    {"id": "n18", "label": "Optics", "category": "physics", "description": "The study of light and its interactions with matter.", "x": 650, "y": 150},
    {"id": "n19", "label": "Astronomy", "category": "astronomy", "description": "The study of celestial objects and space.", "x": 450, "y": 100},
    {"id": "n20", "label": "Cosmology", "category": "astronomy", "description": "The study of the origin and fate of the universe.", "x": 500, "y": 50},
    {"id": "n21", "label": "Statistics", "category": "mathematics", "description": "The collection, analysis, and interpretation of data.", "x": 200, "y": 100},
    {"id": "n22", "label": "Probability", "category": "mathematics", "description": "The analysis of random phenomena.", "x": 300, "y": 100},
    {"id": "n23", "label": "Earth Science", "category": "earth_science", "description": "The study of the Earth and its neighbors in space.", "x": 500, "y": 500},
    {"id": "n24", "label": "Geology", "category": "earth_science", "description": "The study of the solid Earth and its rocks.", "x": 450, "y": 600},
    {"id": "n25", "label": "Particle Physics", "category": "physics", "description": "The study of fundamental constituents of matter.", "x": 500, "y": 150},
]

DEMO_EDGES = [
    {"source": "n01", "target": "n02", "label": "includes"},
    {"source": "n01", "target": "n03", "label": "includes"},
    {"source": "n01", "target": "n04", "label": "includes"},
    {"source": "n01", "target": "n18", "label": "includes"},
    {"source": "n01", "target": "n25", "label": "includes"},
    {"source": "n05", "target": "n06", "label": "includes"},
    {"source": "n05", "target": "n07", "label": "includes"},
    {"source": "n05", "target": "n21", "label": "includes"},
    {"source": "n05", "target": "n22", "label": "includes"},
    {"source": "n08", "target": "n09", "label": "includes"},
    {"source": "n08", "target": "n10", "label": "includes"},
    {"source": "n11", "target": "n12", "label": "includes"},
    {"source": "n11", "target": "n13", "label": "includes"},
    {"source": "n14", "target": "n15", "label": "includes"},
    {"source": "n14", "target": "n16", "label": "includes"},
    {"source": "n14", "target": "n17", "label": "includes"},
    {"source": "n01", "target": "n05", "label": "depends_on"},
    {"source": "n02", "target": "n07", "label": "requires"},
    {"source": "n08", "target": "n01", "label": "related_to"},
    {"source": "n10", "target": "n11", "label": "bridges"},
    {"source": "n16", "target": "n21", "label": "uses"},
    {"source": "n19", "target": "n01", "label": "depends_on"},
    {"source": "n19", "target": "n20", "label": "includes"},
    {"source": "n23", "target": "n24", "label": "includes"},
]

CATEGORY_COLORS: dict[str, str] = {
    "physics": "#60a5fa",
    "mathematics": "#a78bfa",
    "chemistry": "#f472b6",
    "biology": "#34d399",
    "computer_science": "#fbbf24",
    "astronomy": "#818cf8",
    "earth_science": "#fb923c",
    "general": "#94a3b8",
}

# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------


def build_html() -> str:
    """Assemble a self-contained D3.js force-directed demo."""

    nodes_json = json.dumps(DEMO_NODES, indent=2)
    edges_json = json.dumps(DEMO_EDGES, indent=2)
    colors_json = json.dumps(CATEGORY_COLORS)

    html = textwrap.dedent(f"""\
    <!DOCTYPE html>
    <!--
      Project Mycelium — Nurturing Knowledge Without the Cloud
      Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
      Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
      Single-file offline demo — open in any modern browser.
    -->
    <html lang="en" class="dark">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <title>Project Mycelium — Offline Demo</title>
      <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        :root {{
          --bg: #0d1117; --surface: #161b22; --border: #30363d;
          --text: #e6edf3; --muted: #8b949e; --accent: #58a6ff;
        }}
        body {{
          font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
          background: var(--bg); color: var(--text); overflow: hidden;
        }}
        #header {{
          display: flex; align-items: center; gap: 12px;
          padding: 12px 20px; border-bottom: 1px solid var(--border);
          background: var(--surface);
        }}
        #header h1 {{ font-size: 18px; font-weight: 700; }}
        #header .subtitle {{ font-size: 12px; color: var(--muted); }}
        #header .badge {{
          font-size: 10px; padding: 2px 8px; border-radius: 9999px;
          background: #1f6feb33; color: var(--accent); border: 1px solid #1f6feb55;
        }}
        #graph {{ width: 100vw; height: calc(100vh - 52px); }}
        .node-label {{
          font-size: 10px; fill: var(--text); pointer-events: none;
          text-anchor: middle; dominant-baseline: central;
        }}
        .edge-line {{ stroke: var(--border); stroke-width: 1; opacity: 0.5; }}
        .tooltip {{
          position: fixed; padding: 10px 14px; border-radius: 8px;
          background: var(--surface); border: 1px solid var(--border);
          color: var(--text); font-size: 12px; pointer-events: none;
          box-shadow: 0 8px 24px rgba(0,0,0,.4); max-width: 280px;
          z-index: 999; display: none;
        }}
        .tooltip h3 {{ font-size: 13px; font-weight: 600; margin-bottom: 4px; }}
        .tooltip .cat {{ font-size: 10px; color: var(--accent); text-transform: uppercase; letter-spacing: 1px; }}
        .tooltip p {{ font-size: 11px; color: var(--muted); margin-top: 6px; line-height: 1.5; }}
        #stats {{
          position: fixed; bottom: 16px; left: 16px;
          display: flex; gap: 12px; font-size: 11px; color: var(--muted);
          background: var(--surface); padding: 6px 14px; border-radius: 9999px;
          border: 1px solid var(--border);
        }}
        #info {{
          position: fixed; bottom: 16px; right: 16px;
          font-size: 10px; color: var(--muted); opacity: 0.5;
        }}
      </style>
    </head>
    <body>
      <div id="header">
        <span style="font-size: 22px;">🍄</span>
        <div>
          <h1>Project Mycelium</h1>
          <span class="subtitle">Nurturing Knowledge Without the Cloud</span>
        </div>
        <span class="badge">offline demo</span>
        <span class="badge">ZPL v2.0</span>
      </div>
      <svg id="graph"></svg>
      <div class="tooltip" id="tooltip"></div>
      <div id="stats">
        <span id="stat-nodes"></span>
        <span id="stat-edges"></span>
      </div>
      <div id="info">Scroll to zoom · Drag nodes · Hover to inspect</div>

      <script>
      // ---- Inline D3 v7 micro-force (subset) ----
      // For the demo we use a self-contained minimal force simulation.
      (function() {{
        'use strict';

        const NODES = {nodes_json};
        const EDGES = {edges_json};
        const COLORS = {colors_json};

        document.getElementById('stat-nodes').textContent = NODES.length + ' nodes';
        document.getElementById('stat-edges').textContent = EDGES.length + ' edges';

        const svg = document.getElementById('graph');
        const W = window.innerWidth;
        const H = window.innerHeight - 52;
        svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);

        const tooltip = document.getElementById('tooltip');

        // Index
        const nodeMap = {{}};
        NODES.forEach(n => {{ nodeMap[n.id] = n; n.vx = 0; n.vy = 0; }});

        // Draw edges
        const edgeEls = [];
        EDGES.forEach(e => {{
          const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
          line.classList.add('edge-line');
          svg.appendChild(line);
          edgeEls.push({{ el: line, source: e.source, target: e.target }});
        }});

        // Draw nodes
        const nodeEls = [];
        NODES.forEach(n => {{
          const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
          g.style.cursor = 'grab';

          const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
          circle.setAttribute('r', '8');
          circle.setAttribute('fill', COLORS[n.category] || COLORS.general);
          circle.setAttribute('stroke', '#0d1117');
          circle.setAttribute('stroke-width', '2');
          g.appendChild(circle);

          const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
          text.classList.add('node-label');
          text.setAttribute('dy', '-14');
          text.textContent = n.label;
          g.appendChild(text);

          // Hover
          g.addEventListener('mouseenter', (ev) => {{
            circle.setAttribute('r', '12');
            circle.setAttribute('stroke', COLORS[n.category] || '#58a6ff');
            circle.setAttribute('stroke-width', '3');
            tooltip.innerHTML = '<span class="cat">' + n.category + '</span><h3>' + n.label + '</h3><p>' + (n.description || '') + '</p>';
            tooltip.style.display = 'block';
            tooltip.style.left = ev.clientX + 16 + 'px';
            tooltip.style.top = ev.clientY - 10 + 'px';
          }});
          g.addEventListener('mouseleave', () => {{
            circle.setAttribute('r', '8');
            circle.setAttribute('stroke', '#0d1117');
            circle.setAttribute('stroke-width', '2');
            tooltip.style.display = 'none';
          }});
          g.addEventListener('mousemove', (ev) => {{
            tooltip.style.left = ev.clientX + 16 + 'px';
            tooltip.style.top = ev.clientY - 10 + 'px';
          }});

          // Drag
          let dragging = false;
          g.addEventListener('mousedown', (ev) => {{
            dragging = true;
            g.style.cursor = 'grabbing';
            ev.preventDefault();
          }});
          window.addEventListener('mousemove', (ev) => {{
            if (!dragging) return;
            n.x = ev.clientX;
            n.y = ev.clientY - 52;
            n.vx = 0; n.vy = 0;
          }});
          window.addEventListener('mouseup', () => {{
            dragging = false;
            g.style.cursor = 'grab';
          }});

          svg.appendChild(g);
          nodeEls.push({{ el: g, node: n }});
        }});

        // Simple force simulation
        function tick() {{
          // Repulsion
          for (let i = 0; i < NODES.length; i++) {{
            for (let j = i + 1; j < NODES.length; j++) {{
              let dx = NODES[j].x - NODES[i].x;
              let dy = NODES[j].y - NODES[i].y;
              let d = Math.sqrt(dx * dx + dy * dy) || 1;
              let f = 800 / (d * d);
              NODES[i].vx -= dx / d * f;
              NODES[i].vy -= dy / d * f;
              NODES[j].vx += dx / d * f;
              NODES[j].vy += dy / d * f;
            }}
          }}
          // Attraction (edges)
          EDGES.forEach(e => {{
            const s = nodeMap[e.source];
            const t = nodeMap[e.target];
            if (!s || !t) return;
            let dx = t.x - s.x;
            let dy = t.y - s.y;
            let d = Math.sqrt(dx * dx + dy * dy) || 1;
            let f = (d - 100) * 0.005;
            s.vx += dx / d * f;
            s.vy += dy / d * f;
            t.vx -= dx / d * f;
            t.vy -= dy / d * f;
          }});
          // Center gravity
          NODES.forEach(n => {{
            n.vx += (W / 2 - n.x) * 0.001;
            n.vy += (H / 2 - n.y) * 0.001;
          }});
          // Integrate + damping
          NODES.forEach(n => {{
            n.vx *= 0.9;
            n.vy *= 0.9;
            n.x += n.vx;
            n.y += n.vy;
            n.x = Math.max(20, Math.min(W - 20, n.x));
            n.y = Math.max(20, Math.min(H - 20, n.y));
          }});
          // Update DOM
          edgeEls.forEach(e => {{
            const s = nodeMap[e.source];
            const t = nodeMap[e.target];
            if (!s || !t) return;
            e.el.setAttribute('x1', s.x);
            e.el.setAttribute('y1', s.y);
            e.el.setAttribute('x2', t.x);
            e.el.setAttribute('y2', t.y);
          }});
          nodeEls.forEach(ne => {{
            ne.el.setAttribute('transform', 'translate(' + ne.node.x + ',' + ne.node.y + ')');
          }});
          requestAnimationFrame(tick);
        }}
        tick();

        // Zoom / pan via SVG viewBox
        let vx = 0, vy = 0, vw = W, vh = H;
        svg.addEventListener('wheel', (ev) => {{
          ev.preventDefault();
          const scale = ev.deltaY > 0 ? 1.1 : 0.9;
          const mx = ev.clientX / W;
          const my = (ev.clientY - 52) / H;
          const nw = vw * scale;
          const nh = vh * scale;
          vx += (vw - nw) * mx;
          vy += (vh - nh) * my;
          vw = nw; vh = nh;
          svg.setAttribute('viewBox', vx + ' ' + vy + ' ' + vw + ' ' + vh);
        }}, {{ passive: false }});
      }})();
      </script>
    </body>
    </html>
    """)
    return html


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    html = build_html()
    OUT_FILE.write_text(html, encoding="utf-8")

    size_kb = OUT_FILE.stat().st_size / 1024
    sha = hashlib.sha256(html.encode()).hexdigest()[:16]

    print(f"✓ Demo exported → {OUT_FILE}  ({size_kb:.1f} KB, sha256:{sha})")
    print("  Open in any browser — no server required.")


if __name__ == "__main__":
    main()
