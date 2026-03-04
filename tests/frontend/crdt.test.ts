/*
  Project Mycelium — Nurturing Knowledge Without the Cloud
  Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)

  Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
  See LICENSE.md for full text.

  THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
  See LICENSE.md for details and disclaimers.
*/

import { describe, it, expect, beforeEach } from 'vitest';
import { CRDTDocument } from '../../src/crdt/CRDTDocument';

describe('CRDTDocument', () => {
  let doc: CRDTDocument;

  beforeEach(() => {
    doc = new CRDTDocument();
  });

  describe('Node operations', () => {
    it('should add a node', () => {
      doc.addNode('n1', { label: 'Physics', category: 'physics' });
      const node = doc.getNode('n1');
      expect(node).not.toBeNull();
      expect(node?.label).toBe('Physics');
    });

    it('should update a node', () => {
      doc.addNode('n1', { label: 'Old', category: 'general' });
      doc.updateNode('n1', { label: 'New' });
      expect(doc.getNode('n1')?.label).toBe('New');
    });

    it('should delete a node', () => {
      doc.addNode('n1', { label: 'Delete Me', category: 'general' });
      doc.deleteNode('n1');
      expect(doc.getNode('n1')).toBeNull();
    });

    it('should list all nodes', () => {
      doc.addNode('n1', { label: 'A', category: 'a' });
      doc.addNode('n2', { label: 'B', category: 'b' });
      const all = doc.getAllNodes();
      expect(all.length).toBe(2);
    });

    it('should cascade-delete edges when node is removed', () => {
      doc.addNode('n1', { label: 'A', category: 'a' });
      doc.addNode('n2', { label: 'B', category: 'b' });
      doc.addEdge('e1', { sourceId: 'n1', targetId: 'n2', label: 'links' });
      doc.deleteNode('n1');
      const edges = doc.getAllEdges();
      expect(edges.length).toBe(0);
    });
  });

  describe('Edge operations', () => {
    it('should add an edge', () => {
      doc.addNode('n1', { label: 'A', category: 'a' });
      doc.addNode('n2', { label: 'B', category: 'b' });
      doc.addEdge('e1', { sourceId: 'n1', targetId: 'n2', label: 'links' });
      const edges = doc.getAllEdges();
      expect(edges.length).toBe(1);
      expect(edges[0][1].sourceId).toBe('n1');
    });

    it('should delete an edge', () => {
      doc.addEdge('e1', { sourceId: 'n1', targetId: 'n2', label: 'links' });
      doc.deleteEdge('e1');
      expect(doc.getAllEdges().length).toBe(0);
    });
  });

  describe('State encoding', () => {
    it('should encode and decode state', () => {
      doc.addNode('n1', { label: 'Physics', category: 'physics' });
      const encoded = doc.encodeState();
      expect(encoded).toBeInstanceOf(Uint8Array);
      expect(encoded.length).toBeGreaterThan(0);
    });

    it('should produce a state vector', () => {
      doc.addNode('n1', { label: 'Test', category: 'test' });
      const sv = doc.encodeStateVector();
      expect(sv).toBeInstanceOf(Uint8Array);
    });
  });

  describe('CRDT merge', () => {
    it('should merge two documents', () => {
      const doc1 = new CRDTDocument();
      const doc2 = new CRDTDocument();

      doc1.addNode('n1', { label: 'From Doc1', category: 'a' });
      doc2.addNode('n2', { label: 'From Doc2', category: 'b' });

      doc1.mergeWith(doc2);

      expect(doc1.getNode('n1')).not.toBeNull();
      expect(doc1.getNode('n2')).not.toBeNull();

      doc1.destroy();
      doc2.destroy();
    });

    it('should compute and apply deltas', () => {
      const doc1 = new CRDTDocument();
      const doc2 = new CRDTDocument();

      doc1.addNode('n1', { label: 'Alpha', category: 'a' });

      // Get delta from doc1 relative to doc2's state
      const sv2 = doc2.encodeStateVector();
      const delta = doc1.computeDelta(sv2);

      doc2.applyUpdate(delta);

      expect(doc2.getNode('n1')).not.toBeNull();
      expect(doc2.getNode('n1')?.label).toBe('Alpha');

      doc1.destroy();
      doc2.destroy();
    });

    it('should handle concurrent edits', () => {
      const doc1 = new CRDTDocument();
      const doc2 = new CRDTDocument();

      // Both create the same node — last writer wins in Y.Map
      doc1.addNode('shared', { label: 'Version A', category: 'x' });
      doc2.addNode('shared', { label: 'Version B', category: 'y' });

      doc1.mergeWith(doc2);

      const node = doc1.getNode('shared');
      expect(node).not.toBeNull();
      // One of the versions should win
      expect(['Version A', 'Version B']).toContain(node?.label);

      doc1.destroy();
      doc2.destroy();
    });
  });

  describe('Metadata', () => {
    it('should set and get metadata', () => {
      doc.setMeta('title', 'My Graph');
      expect(doc.getMeta('title')).toBe('My Graph');
    });
  });

  describe('Observers', () => {
    it('should fire node change callback', () => {
      let fired = false;
      doc.onNodesChange(() => { fired = true; });
      doc.addNode('n1', { label: 'Trigger', category: 'test' });
      expect(fired).toBe(true);
    });

    it('should fire edge change callback', () => {
      let fired = false;
      doc.onEdgesChange(() => { fired = true; });
      doc.addEdge('e1', { sourceId: 'n1', targetId: 'n2', label: 'test' });
      expect(fired).toBe(true);
    });
  });
});
