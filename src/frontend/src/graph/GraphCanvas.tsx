/*
  Project Mycelium — Nurturing Knowledge Without the Cloud
  Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)

  Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
  See LICENSE.md for full text.

  THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
  See LICENSE.md for details and disclaimers.
*/

/**
 * GraphCanvas: D3.js force-directed graph explorer with dark theme,
 * pan/zoom, node selection, LOD rendering, and accessibility.
 */

import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import type { GraphNode, GraphEdge } from '../types';
import { CATEGORY_COLORS } from '../types';
import { useReducedMotion } from '../hooks';

interface GraphCanvasProps {
  nodes: GraphNode[];
  edges: GraphEdge[];
  onNodeClick?: (node: GraphNode) => void;
  selectedNodeId?: string | null;
  presenterMode?: boolean;
  width?: number;
  height?: number;
}

interface SimNode extends d3.SimulationNodeDatum {
  id: string;
  label: string;
  category: string;
  description: string | null;
  graphId: string;
  cid: string | null;
  metadata: Record<string, unknown> | null;
  positionX: number | null;
  positionY: number | null;
  createdAt: string;
  updatedAt: string;
}

interface SimLink extends d3.SimulationLinkDatum<SimNode> {
  id: string;
  label: string;
  weight: number;
}

export const GraphCanvas: React.FC<GraphCanvasProps> = ({
  nodes,
  edges,
  onNodeClick,
  selectedNodeId,
  presenterMode = false,
  width: propWidth,
  height: propHeight,
}) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState({ width: propWidth || 800, height: propHeight || 600 });
  const reducedMotion = useReducedMotion();
  const simulationRef = useRef<d3.Simulation<SimNode, SimLink> | null>(null);

  // Responsive sizing
  useEffect(() => {
    if (propWidth && propHeight) {
      setDimensions({ width: propWidth, height: propHeight });
      return;
    }
    const container = containerRef.current;
    if (!container) return;
    const observer = new ResizeObserver(([entry]) => {
      const { width, height } = entry.contentRect;
      setDimensions({ width: Math.max(width, 400), height: Math.max(height, 300) });
    });
    observer.observe(container);
    return () => observer.disconnect();
  }, [propWidth, propHeight]);

  // Main D3 render
  useEffect(() => {
    const svgEl = svgRef.current;
    if (!svgEl) return;
    const svg = d3.select(svgEl);

    const { width, height } = dimensions;

    // Clear previous
    svg.selectAll('*').remove();

    // Root group for zoom/pan
    const g = svg.append('g');

    // Zoom behavior
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.1, 4])
      .on('zoom', (event) => {
        g.attr('transform', event.transform);
      });
    (svg as any).call(zoom);

    // Prepare simulation data
    const simNodes: SimNode[] = nodes.map((n) => ({
      ...n,
      x: n.positionX ?? undefined,
      y: n.positionY ?? undefined,
    }));

    const nodeMap = new Map(simNodes.map((n) => [n.id, n]));

    const simLinks: SimLink[] = edges
      .filter((e) => nodeMap.has(e.sourceId) && nodeMap.has(e.targetId))
      .map((e) => ({
        id: e.id,
        source: e.sourceId,
        target: e.targetId,
        label: e.label,
        weight: e.weight,
      }));

    // Force simulation
    const simulation = d3
      .forceSimulation<SimNode>(simNodes)
      .force(
        'link',
        d3
          .forceLink<SimNode, SimLink>(simLinks)
          .id((d) => d.id)
          .distance(80)
          .strength(0.5),
      )
      .force('charge', d3.forceManyBody().strength(-200).distanceMax(300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide(30))
      .alphaDecay(reducedMotion ? 1 : 0.02);

    simulationRef.current = simulation;

    // Edges
    const linkGroup = g.append('g').attr('class', 'links');
    const links = linkGroup
      .selectAll<SVGLineElement, SimLink>('line')
      .data(simLinks)
      .join('line')
      .attr('stroke', 'var(--color-border)')
      .attr('stroke-width', (d) => Math.max(1, d.weight))
      .attr('stroke-opacity', 0.6);

    // Edge labels (on hover area)
    const linkLabels = linkGroup
      .selectAll<SVGTextElement, SimLink>('text')
      .data(simLinks)
      .join('text')
      .text((d) => d.label)
      .attr('font-size', '10px')
      .attr('fill', 'var(--color-text-disabled)')
      .attr('text-anchor', 'middle')
      .attr('dy', -4)
      .attr('opacity', 0);

    // Nodes
    const nodeGroup = g.append('g').attr('class', 'nodes');
    const nodeElements = nodeGroup
      .selectAll<SVGGElement, SimNode>('g')
      .data(simNodes)
      .join('g')
      .attr('cursor', 'pointer')
      .attr('role', 'button')
      .attr('tabindex', '0')
      .attr('aria-label', (d) => `Node: ${d.label}, Category: ${d.category}`)
      .on('click', (_event, d) => {
        if (onNodeClick) onNodeClick(d as unknown as GraphNode);
      })
      .on('keydown', (event, d) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          if (onNodeClick) onNodeClick(d as unknown as GraphNode);
        }
      })
      .call(
        d3
          .drag<SVGGElement, SimNode>()
          .on('start', (event, d) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
          })
          .on('drag', (event, d) => {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on('end', (event, d) => {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          }),
      );

    // Node circles
    nodeElements
      .append('circle')
      .attr('r', presenterMode ? 14 : 10)
      .attr('fill', (d) => CATEGORY_COLORS[d.category] || CATEGORY_COLORS.default)
      .attr('stroke', 'var(--color-surface)')
      .attr('stroke-width', 2)
      .attr('class', 'transition-all duration-fast');

    // Selection ring
    nodeElements
      .append('circle')
      .attr('r', presenterMode ? 18 : 14)
      .attr('fill', 'none')
      .attr('stroke', (d) =>
        d.id === selectedNodeId ? 'rgb(var(--color-primary))' : 'transparent',
      )
      .attr('stroke-width', 2)
      .attr('class', 'selection-ring');

    // Node labels
    nodeElements
      .append('text')
      .text((d) => d.label)
      .attr('dy', presenterMode ? 28 : 22)
      .attr('text-anchor', 'middle')
      .attr('font-size', presenterMode ? '13px' : '11px')
      .attr('font-weight', '500')
      .attr('fill', 'var(--color-text-medium)')
      .attr('pointer-events', 'none');

    // Hover effects
    nodeElements
      .on('mouseenter', function (_, d) {
        d3.select(this)
          .select('circle:first-child')
          .transition()
          .duration(100)
          .attr('r', presenterMode ? 17 : 13)
          .attr('filter', 'drop-shadow(0 0 6px rgba(109,155,241,0.4))');
        // Show connected edge labels
        linkLabels
          .filter(
            (l) =>
              (l.source as SimNode).id === d.id ||
              (l.target as SimNode).id === d.id,
          )
          .transition()
          .duration(100)
          .attr('opacity', 1);
      })
      .on('mouseleave', function () {
        d3.select(this)
          .select('circle:first-child')
          .transition()
          .duration(100)
          .attr('r', presenterMode ? 14 : 10)
          .attr('filter', 'none');
        linkLabels.transition().duration(200).attr('opacity', 0);
      });

    // Double-click to center
    nodeElements.on('dblclick', (event, d) => {
      event.stopPropagation();
      (svg.transition().duration(500) as any).call(
        zoom.transform,
        d3.zoomIdentity
          .translate(width / 2, height / 2)
          .scale(1.5)
          .translate(-(d.x ?? 0), -(d.y ?? 0)),
      );
    });

    // Tick
    simulation.on('tick', () => {
      links
        .attr('x1', (d) => (d.source as SimNode).x ?? 0)
        .attr('y1', (d) => (d.source as SimNode).y ?? 0)
        .attr('x2', (d) => (d.target as SimNode).x ?? 0)
        .attr('y2', (d) => (d.target as SimNode).y ?? 0);

      linkLabels
        .attr('x', (d) => (((d.source as SimNode).x ?? 0) + ((d.target as SimNode).x ?? 0)) / 2)
        .attr('y', (d) => (((d.source as SimNode).y ?? 0) + ((d.target as SimNode).y ?? 0)) / 2);

      nodeElements.attr('transform', (d) => `translate(${d.x ?? 0},${d.y ?? 0})`);
    });

    // Initial zoom to fit
    const initialZoom = d3.zoomIdentity.translate(0, 0).scale(0.9);
    (svg as any).call(zoom.transform, initialZoom);

    return () => {
      simulation.stop();
    };
  }, [nodes, edges, dimensions, selectedNodeId, presenterMode, onNodeClick, reducedMotion]);

  // Update selection ring when selectedNodeId changes
  useEffect(() => {
    const svgEl = svgRef.current;
    if (!svgEl) return;
    const svg = d3.select(svgEl);
    svg.selectAll('.selection-ring').attr('stroke', function () {
      const el = this as Element;
      if (!el.parentNode) return 'transparent';
      const parent = d3.select(el.parentNode as Element);
      const datum = parent.datum() as SimNode | undefined;
      return datum?.id === selectedNodeId
        ? 'rgb(var(--color-primary))'
        : 'transparent';
    });
  }, [selectedNodeId]);

  return (
    <div
      ref={containerRef}
      className="w-full h-full bg-surface rounded-xl border border-border overflow-hidden"
      role="application"
      aria-label="Knowledge graph explorer. Use Tab to navigate between nodes, Enter to select, and drag to rearrange."
    >
      <svg
        ref={svgRef}
        width={dimensions.width}
        height={dimensions.height}
        className="w-full h-full"
        aria-label="Interactive knowledge graph visualization"
      >
        <defs>
          <filter id="glow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur" />
            <feMerge>
              <feMergeNode in="coloredBlur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>
      </svg>
    </div>
  );
};
