/*
  Project Mycelium — Nurturing Knowledge Without the Cloud
  Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)

  Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
  See LICENSE.md for full text.

  THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
  See LICENSE.md for details and disclaimers.
*/

import { describe, it, expect } from 'vitest';
import { DEMO_NODES, DEMO_EDGES } from '../../src/demoData';
import { CATEGORY_COLORS } from '../../src/types';

describe('Demo Data', () => {
  it('should have at least 25 nodes', () => {
    expect(DEMO_NODES.length).toBeGreaterThanOrEqual(25);
  });

  it('should have at least 20 edges', () => {
    expect(DEMO_EDGES.length).toBeGreaterThanOrEqual(20);
  });

  it('every node should have required fields', () => {
    for (const node of DEMO_NODES) {
      expect(node.id).toBeTruthy();
      expect(node.label).toBeTruthy();
      expect(node.category).toBeTruthy();
      expect(typeof node.positionX).toBe('number');
      expect(typeof node.positionY).toBe('number');
    }
  });

  it('every edge should reference existing nodes', () => {
    const nodeIds = new Set(DEMO_NODES.map((n) => n.id));
    for (const edge of DEMO_EDGES) {
      expect(nodeIds.has(edge.sourceId)).toBe(true);
      expect(nodeIds.has(edge.targetId)).toBe(true);
    }
  });

  it('should have no duplicate node IDs', () => {
    const ids = DEMO_NODES.map((n) => n.id);
    expect(new Set(ids).size).toBe(ids.length);
  });

  it('should have no duplicate edge IDs', () => {
    const ids = DEMO_EDGES.map((e) => e.id);
    expect(new Set(ids).size).toBe(ids.length);
  });

  it('all categories should have a color defined', () => {
    const cats = new Set(DEMO_NODES.map((n) => n.category));
    for (const cat of cats) {
      expect(CATEGORY_COLORS[cat]).toBeTruthy();
    }
  });
});
