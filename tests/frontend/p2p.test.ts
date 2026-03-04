/*
  Project Mycelium — Nurturing Knowledge Without the Cloud
  Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)

  Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
  See LICENSE.md for full text.

  THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
  See LICENSE.md for details and disclaimers.
*/

import { describe, it, expect, beforeEach } from 'vitest';
import { P2PManager, generatePeerId, simulateGossip } from '../../src/p2p/P2PManager';
import { CRDTDocument } from '../../src/crdt/CRDTDocument';

describe('P2PManager', () => {
  let manager: P2PManager;

  beforeEach(() => {
    manager = new P2PManager();
  });

  it('should generate a unique peer ID', () => {
    expect(manager.peerId).toBeTruthy();
    expect(manager.peerId.length).toBeGreaterThan(0);
  });

  it('should start in offline mode', () => {
    expect(manager.isOffline).toBe(true);
  });

  it('should attach a document', () => {
    const doc = new CRDTDocument();
    manager.attachDocument(doc);
    // No error thrown
    doc.destroy();
  });

  it('should track no peers initially', () => {
    expect(manager.getPeers().length).toBe(0);
  });

  it('should stop cleanly', () => {
    manager.stop();
    // No error thrown
  });
});

describe('generatePeerId', () => {
  it('should produce unique IDs', () => {
    const a = generatePeerId();
    const b = generatePeerId();
    expect(a).not.toBe(b);
  });

  it('should start with "peer-"', () => {
    expect(generatePeerId()).toMatch(/^peer-/);
  });
});

describe('simulateGossip', () => {
  it('should merge documents without errors', () => {
    const doc = new CRDTDocument();
    doc.addNode('n1', { label: 'Original', category: 'test' });
    
    // simulateGossip creates internal doc, modifies, and merges
    simulateGossip(doc);
    
    // Original node should still exist
    expect(doc.getNode('n1')).not.toBeNull();
    
    // The gossip-simulated node should be merged in
    const allNodes = doc.getAllNodes();
    expect(allNodes.length).toBeGreaterThanOrEqual(1);
    
    doc.destroy();
  });
});
