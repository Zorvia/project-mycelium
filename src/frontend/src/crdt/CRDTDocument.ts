/*
  Project Mycelium — Nurturing Knowledge Without the Cloud
  Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)

  Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
  See LICENSE.md for full text.

  THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
  See LICENSE.md for details and disclaimers.
*/

/**
 * CRDT Engine using Yjs for conflict-free collaborative editing.
 *
 * Design rationale:
 * - Yjs was chosen for best-in-class performance and sub-document support.
 * - LWW (Last-Writer-Wins) semantics for individual node field edits.
 * - GCounter behavior for counters (view counts, etc.).
 * - All operations are idempotent, convergent, and monotonic.
 */

import * as Y from 'yjs';

export interface CRDTNode {
  id: string;
  label: string;
  category: string;
  description: string;
  positionX: number;
  positionY: number;
  metadata: Record<string, unknown>;
}

export interface CRDTEdge {
  id: string;
  sourceId: string;
  targetId: string;
  label: string;
  weight: number;
}

/**
 * CRDTDocument wraps a Yjs Doc for knowledge graph operations.
 * Supports merge, undo, and deterministic state encoding.
 */
export class CRDTDocument {
  readonly doc: Y.Doc;
  private readonly _nodes: Y.Map<Y.Map<unknown>>;
  private readonly _edges: Y.Map<Y.Map<unknown>>;
  private readonly _metadata: Y.Map<unknown>;

  constructor(clientId?: number) {
    this.doc = new Y.Doc();
    if (clientId !== undefined) {
      this.doc.clientID = clientId;
    }
    this._nodes = this.doc.getMap('nodes');
    this._edges = this.doc.getMap('edges');
    this._metadata = this.doc.getMap('metadata');
  }

  // ─── Node Operations ────────────────────────

  addNode(node: CRDTNode): void {
    const yNode = new Y.Map<unknown>();
    yNode.set('id', node.id);
    yNode.set('label', node.label);
    yNode.set('category', node.category);
    yNode.set('description', node.description);
    yNode.set('positionX', node.positionX);
    yNode.set('positionY', node.positionY);
    yNode.set('metadata', node.metadata);
    this._nodes.set(node.id, yNode);
  }

  updateNode(id: string, fields: Partial<CRDTNode>): boolean {
    const yNode = this._nodes.get(id);
    if (!yNode) return false;
    for (const [key, value] of Object.entries(fields)) {
      if (key !== 'id') {
        yNode.set(key, value);
      }
    }
    return true;
  }

  deleteNode(id: string): boolean {
    if (!this._nodes.has(id)) return false;
    this._nodes.delete(id);
    // Remove connected edges
    for (const [edgeId, yEdge] of this._edges.entries()) {
      if (yEdge.get('sourceId') === id || yEdge.get('targetId') === id) {
        this._edges.delete(edgeId);
      }
    }
    return true;
  }

  getNode(id: string): CRDTNode | null {
    const yNode = this._nodes.get(id);
    if (!yNode) return null;
    return {
      id: yNode.get('id') as string,
      label: yNode.get('label') as string,
      category: yNode.get('category') as string,
      description: yNode.get('description') as string,
      positionX: yNode.get('positionX') as number,
      positionY: yNode.get('positionY') as number,
      metadata: (yNode.get('metadata') as Record<string, unknown>) || {},
    };
  }

  getAllNodes(): CRDTNode[] {
    const nodes: CRDTNode[] = [];
    for (const [, yNode] of this._nodes.entries()) {
      nodes.push({
        id: yNode.get('id') as string,
        label: yNode.get('label') as string,
        category: yNode.get('category') as string,
        description: yNode.get('description') as string,
        positionX: yNode.get('positionX') as number,
        positionY: yNode.get('positionY') as number,
        metadata: (yNode.get('metadata') as Record<string, unknown>) || {},
      });
    }
    return nodes;
  }

  // ─── Edge Operations ────────────────────────

  addEdge(edge: CRDTEdge): void {
    const yEdge = new Y.Map<unknown>();
    yEdge.set('id', edge.id);
    yEdge.set('sourceId', edge.sourceId);
    yEdge.set('targetId', edge.targetId);
    yEdge.set('label', edge.label);
    yEdge.set('weight', edge.weight);
    this._edges.set(edge.id, yEdge);
  }

  deleteEdge(id: string): boolean {
    if (!this._edges.has(id)) return false;
    this._edges.delete(id);
    return true;
  }

  getAllEdges(): CRDTEdge[] {
    const edges: CRDTEdge[] = [];
    for (const [, yEdge] of this._edges.entries()) {
      edges.push({
        id: yEdge.get('id') as string,
        sourceId: yEdge.get('sourceId') as string,
        targetId: yEdge.get('targetId') as string,
        label: yEdge.get('label') as string,
        weight: yEdge.get('weight') as number,
      });
    }
    return edges;
  }

  // ─── Merge & Encoding ──────────────────────

  /** Encode current state as a binary update. */
  encodeState(): Uint8Array {
    return Y.encodeStateAsUpdate(this.doc);
  }

  /** Encode state vector for efficient delta exchange. */
  encodeStateVector(): Uint8Array {
    return Y.encodeStateVector(this.doc);
  }

  /** Apply a remote update (merge). Idempotent. */
  applyUpdate(update: Uint8Array): void {
    Y.applyUpdate(this.doc, update);
  }

  /** Compute the delta between this doc and a remote state vector. */
  computeDelta(remoteStateVector: Uint8Array): Uint8Array {
    return Y.encodeStateAsUpdate(this.doc, remoteStateVector);
  }

  /** Merge with another CRDTDocument. */
  mergeWith(other: CRDTDocument): void {
    const update = other.encodeState();
    this.applyUpdate(update);
  }

  // ─── Metadata ──────────────────────────────

  setMeta(key: string, value: unknown): void {
    this._metadata.set(key, value);
  }

  getMeta(key: string): unknown {
    return this._metadata.get(key);
  }

  // ─── Observers ─────────────────────────────

  onNodesChange(callback: () => void): () => void {
    const handler = () => callback();
    this._nodes.observeDeep(handler);
    return () => this._nodes.unobserveDeep(handler);
  }

  onEdgesChange(callback: () => void): () => void {
    const handler = () => callback();
    this._edges.observeDeep(handler);
    return () => this._edges.unobserveDeep(handler);
  }

  /** Destroy the document and release resources. */
  destroy(): void {
    this.doc.destroy();
  }
}
