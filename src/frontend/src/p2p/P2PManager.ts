/*
  Project Mycelium — Nurturing Knowledge Without the Cloud
  Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)

  Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
  See LICENSE.md for full text.

  THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
  See LICENSE.md for details and disclaimers.
*/

/**
 * P2P networking layer using WebRTC DataChannels.
 *
 * In production: connects to peers via WebRTC with LAN multicast discovery.
 * In offline demo: simulates gossip locally within a single page.
 */

import { CRDTDocument } from '../crdt/CRDTDocument';

export type PeerStatus = 'disconnected' | 'connecting' | 'connected';

export interface PeerInfo {
  id: string;
  status: PeerStatus;
  lastSeen: number;
}

export interface P2PConfig {
  peerId: string;
  offline?: boolean; // true for static demo mode
}

/**
 * P2PManager handles peer discovery and CRDT sync.
 * In offline mode, it simulates gossip between local documents.
 */
export class P2PManager {
  readonly peerId: string;
  private readonly _offline: boolean;
  private readonly _peers = new Map<string, PeerInfo>();
  private _document: CRDTDocument | null = null;
  private _onPeersChange?: (peers: PeerInfo[]) => void;
  private _onSyncComplete?: () => void;

  constructor(config: P2PConfig) {
    this.peerId = config.peerId;
    this._offline = config.offline ?? false;
  }

  /** Attach a CRDT document for sync. */
  setDocument(doc: CRDTDocument): void {
    this._document = doc;
  }

  /** Register a callback for peer status changes. */
  onPeersChange(callback: (peers: PeerInfo[]) => void): void {
    this._onPeersChange = callback;
  }

  /** Register a callback for sync completion. */
  onSyncComplete(callback: () => void): void {
    this._onSyncComplete = callback;
  }

  /** Start the P2P manager. */
  async start(): Promise<void> {
    if (this._offline) {
      console.log('[P2P] Running in offline simulation mode');
      return;
    }
    console.log(`[P2P] Starting peer ${this.peerId}`);
    // In a full implementation, this would:
    // 1. Set up WebRTC peer connections
    // 2. LAN multicast for discovery
    // 3. Exchange Yjs state vectors and deltas
  }

  /** Stop the P2P manager and disconnect all peers. */
  async stop(): Promise<void> {
    this._peers.clear();
    this._notifyPeersChange();
    console.log(`[P2P] Stopped peer ${this.peerId}`);
  }

  /** Get all known peers. */
  getPeers(): PeerInfo[] {
    return Array.from(this._peers.values());
  }

  /**
   * Simulate a local gossip exchange (for offline demo).
   * This demonstrates CRDT merge without actual network.
   */
  simulateGossip(remoteDoc: CRDTDocument): void {
    if (!this._document) {
      console.warn('[P2P] No document attached');
      return;
    }

    // Simulate peer appearing
    const remotePeerId = `sim-${Date.now()}`;
    this._peers.set(remotePeerId, {
      id: remotePeerId,
      status: 'connected',
      lastSeen: Date.now(),
    });
    this._notifyPeersChange();

    // Exchange state vectors
    const localSV = this._document.encodeStateVector();
    const remoteSV = remoteDoc.encodeStateVector();

    // Compute deltas
    const localDelta = this._document.computeDelta(remoteSV);
    const remoteDelta = remoteDoc.computeDelta(localSV);

    // Apply deltas (merge)
    this._document.applyUpdate(remoteDelta);
    remoteDoc.applyUpdate(localDelta);

    // Notify sync
    this._onSyncComplete?.();

    // Simulate disconnect after a moment
    setTimeout(() => {
      this._peers.set(remotePeerId, {
        id: remotePeerId,
        status: 'disconnected',
        lastSeen: Date.now(),
      });
      this._notifyPeersChange();
    }, 2000);
  }

  private _notifyPeersChange(): void {
    this._onPeersChange?.(this.getPeers());
  }

  /** Destroy and clean up. */
  destroy(): void {
    this.stop();
  }
}

/**
 * Generate a random peer ID.
 */
export function generatePeerId(): string {
  const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
  let id = 'peer-';
  for (let i = 0; i < 8; i++) {
    id += chars[Math.floor(Math.random() * chars.length)];
  }
  return id;
}
