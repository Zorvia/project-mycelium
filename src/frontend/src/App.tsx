/*
  Project Mycelium — Nurturing Knowledge Without the Cloud
  Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)

  Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
  See LICENSE.md for full text.

  THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
  See LICENSE.md for details and disclaimers.
*/

import React, { useState, useCallback, useMemo, useEffect, useRef } from 'react';
import { GraphCanvas } from './graph';
import {
  SearchBar,
  Modal,
  NodeCard,
  Button,
  Icon,
  Switch,
  Tooltip,
} from './components';
import { CRDTDocument } from './crdt';
import { P2PManager } from './p2p';
import { createLLMAdapter } from './ai';
import { useTheme, useKeyboard, useReducedMotion } from './hooks';
import { DEMO_NODES, DEMO_EDGES } from './demoData';
import type { GraphNode, GraphEdge, SearchResult } from './types';

/* ------------------------------------------------------------------ */
/*  Main Application                                                   */
/* ------------------------------------------------------------------ */

export default function App() {
  /* ---- Theme ---- */
  const { theme, toggle: toggleTheme } = useTheme();
  const reducedMotion = useReducedMotion();

  /* ---- State ---- */
  const [nodes, setNodes] = useState<GraphNode[]>(DEMO_NODES);
  const [edges, setEdges] = useState<GraphEdge[]>(DEMO_EDGES);
  const [selected, setSelected] = useState<GraphNode | null>(null);
  const [detailOpen, setDetailOpen] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [presenterMode, setPresenterMode] = useState(false);
  const [peerCount, setPeerCount] = useState(0);
  const [syncStatus, setSyncStatus] = useState<'idle' | 'syncing' | 'done'>('idle');
  const [explanation, setExplanation] = useState('');
  const [explaining, setExplaining] = useState(false);
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);

  /* ---- Refs ---- */
  const crdtRef = useRef<CRDTDocument | null>(null);
  const p2pRef = useRef<P2PManager | null>(null);
  const llmRef = useRef(createLLMAdapter());

  /* ---- Init CRDT + P2P ---- */
  useEffect(() => {
    const doc = new CRDTDocument();
    crdtRef.current = doc;

    // Seed CRDT from demo data
    DEMO_NODES.forEach((n) =>
      doc.addNode(n.id, {
        label: n.label,
        category: n.category,
        description: n.description ?? '',
        positionX: n.positionX ?? 0,
        positionY: n.positionY ?? 0,
      }),
    );
    DEMO_EDGES.forEach((e) =>
      doc.addEdge(e.id, {
        sourceId: e.sourceId,
        targetId: e.targetId,
        label: e.label,
        weight: e.weight,
      }),
    );

    // Wire observers
    doc.onNodesChange(() => {
      const allNodes = doc.getAllNodes();
      setNodes(
        allNodes.map(([id, data]) => ({
          id,
          graphId: 'demo-graph-001',
          label: String(data.label ?? ''),
          category: String(data.category ?? 'general'),
          description: data.description != null ? String(data.description) : null,
          positionX: Number(data.positionX ?? 0),
          positionY: Number(data.positionY ?? 0),
          cid: null,
          metadata: null,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        })),
      );
    });

    doc.onEdgesChange(() => {
      const allEdges = doc.getAllEdges();
      setEdges(
        allEdges.map(([id, data]) => ({
          id,
          graphId: 'demo-graph-001',
          sourceId: String(data.sourceId ?? ''),
          targetId: String(data.targetId ?? ''),
          label: String(data.label ?? ''),
          weight: Number(data.weight ?? 1),
          metadata: null,
          createdAt: new Date().toISOString(),
        })),
      );
    });

    // P2P
    const p2p = new P2PManager();
    p2p.attachDocument(doc);
    p2pRef.current = p2p;

    return () => {
      doc.destroy();
      p2p.stop();
    };
  }, []);

  /* ---- Search ---- */
  const handleSearch = useCallback(
    (query: string) => {
      if (!query.trim()) {
        setSearchResults([]);
        return;
      }
      const q = query.toLowerCase();
      const results: SearchResult[] = nodes
        .filter(
          (n) =>
            n.label.toLowerCase().includes(q) ||
            (n.description ?? '').toLowerCase().includes(q) ||
            n.category.toLowerCase().includes(q),
        )
        .map((n) => ({
          nodeId: n.id,
          label: n.label,
          category: n.category,
          score: n.label.toLowerCase().startsWith(q) ? 1 : 0.5,
          snippet: n.description ?? '',
        }));
      setSearchResults(results);
    },
    [nodes],
  );

  const handleSelectResult = useCallback(
    (result: SearchResult) => {
      const node = nodes.find((n) => n.id === result.nodeId) ?? null;
      setSelected(node);
      setDetailOpen(!!node);
      setSearchResults([]);
    },
    [nodes],
  );

  /* ---- Node selection ---- */
  const handleNodeClick = useCallback(
    (nodeId: string) => {
      const node = nodes.find((n) => n.id === nodeId) ?? null;
      setSelected(node);
      setDetailOpen(!!node);
      setExplanation('');
    },
    [nodes],
  );

  /* ---- Explain ---- */
  const handleExplain = useCallback(async () => {
    if (!selected) return;
    setExplaining(true);
    try {
      const adapter = llmRef.current;
      const text = await adapter.explain(selected.label, selected.description ?? '');
      setExplanation(text);
    } catch {
      setExplanation('Unable to generate explanation.');
    } finally {
      setExplaining(false);
    }
  }, [selected]);

  /* ---- P2P Gossip Demo ---- */
  const handleGossipDemo = useCallback(async () => {
    const p2p = p2pRef.current;
    if (!p2p) return;
    setSyncStatus('syncing');
    setPeerCount(1);
    await new Promise((r) => setTimeout(r, 600));
    try {
      const { simulateGossip } = await import('./p2p');
      const doc = crdtRef.current;
      if (doc) {
        simulateGossip(doc);
        setPeerCount(2);
      }
    } catch {
      /* no-op */
    }
    setSyncStatus('done');
    setTimeout(() => setSyncStatus('idle'), 2000);
  }, []);

  /* ---- Keyboard shortcuts ---- */
  useKeyboard('Escape', () => {
    setDetailOpen(false);
    setSidebarOpen(false);
  });
  useKeyboard('/', () => {
    const el = document.querySelector<HTMLInputElement>('[data-search-input]');
    el?.focus();
  });
  useKeyboard('p', () => setPresenterMode((v) => !v));

  /* ---- Stats ---- */
  const stats = useMemo(
    () => ({
      nodes: nodes.length,
      edges: edges.length,
      categories: new Set(nodes.map((n) => n.category)).size,
    }),
    [nodes, edges],
  );

  /* ---- LLM info ---- */
  const llmName = llmRef.current.name;
  const llmLocal = llmRef.current.isLocal;

  return (
    <div className="relative flex h-screen w-screen overflow-hidden bg-surface text-on-surface">
      {/* ---- Sidebar ---- */}
      <aside
        className={`
          absolute inset-y-0 left-0 z-30 flex w-72 flex-col
          border-r border-border bg-surface-alt
          transition-transform duration-300 ease-out-expo
          ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
          lg:relative lg:translate-x-0
        `}
        aria-label="Sidebar"
      >
        {/* Branding */}
        <div className="flex items-center gap-3 border-b border-border px-4 py-4">
          <span className="text-2xl" role="img" aria-label="Mycelium logo">
            🍄
          </span>
          <div>
            <h1 className="text-lg font-bold tracking-tight text-on-surface">
              Mycelium
            </h1>
            <p className="text-xs text-muted">Knowledge without the cloud</p>
          </div>
        </div>

        {/* Stats */}
        <div className="flex gap-4 border-b border-border px-4 py-3 text-xs text-muted">
          <span>{stats.nodes} nodes</span>
          <span>{stats.edges} edges</span>
          <span>{stats.categories} topics</span>
        </div>

        {/* Controls */}
        <div className="flex flex-col gap-3 overflow-y-auto px-4 py-4">
          {/* Theme toggle */}
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">Dark mode</span>
            <Switch
              checked={theme === 'dark'}
              onChange={toggleTheme}
              label="Toggle dark mode"
            />
          </div>

          {/* Presenter mode */}
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">Presenter</span>
            <Switch
              checked={presenterMode}
              onChange={() => setPresenterMode((v) => !v)}
              label="Toggle presenter mode"
            />
          </div>

          {/* P2P status */}
          <div className="flex items-center gap-2 text-sm">
            <Icon name="sync" size={16} />
            <span>
              {peerCount} peer{peerCount !== 1 ? 's' : ''}
            </span>
            {syncStatus === 'syncing' && (
              <span className="animate-pulse text-accent">syncing…</span>
            )}
            {syncStatus === 'done' && (
              <span className="text-green-400">✓ synced</span>
            )}
          </div>

          {/* Gossip demo button */}
          <Button
            variant="secondary"
            size="sm"
            onClick={handleGossipDemo}
            disabled={syncStatus === 'syncing'}
          >
            <Icon name="sync" size={14} />
            Simulate P2P Gossip
          </Button>

          {/* LLM info */}
          <div className="mt-2 flex items-center gap-2 text-xs text-muted">
            <Icon name="ai" size={14} />
            <span>
              {llmName} {llmLocal ? '(local)' : '(remote)'}
            </span>
          </div>

          {/* Offline badge */}
          <div className="flex items-center gap-2 text-xs text-muted">
            <Icon name="offline" size={14} />
            <span>Offline-first</span>
          </div>

          {/* Privacy badge */}
          <div className="flex items-center gap-2 text-xs text-green-400">
            <Icon name="lock" size={14} />
            <span>Data stays on-device</span>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-auto border-t border-border px-4 py-3 text-[10px] text-muted">
          Project Mycelium · ZPL v2.0 · Zorvia Community
        </div>
      </aside>

      {/* ---- Main content ---- */}
      <main className="relative flex flex-1 flex-col">
        {/* Top bar */}
        <header className="flex items-center gap-3 border-b border-border bg-surface-alt/80 px-4 py-2 backdrop-blur-sm">
          {/* Menu button (mobile) */}
          <button
            className="rounded-md p-1.5 hover:bg-white/10 lg:hidden"
            onClick={() => setSidebarOpen((v) => !v)}
            aria-label="Toggle sidebar"
          >
            <Icon name="menu" size={20} />
          </button>

          {/* Search */}
          <div className="flex-1">
            <SearchBar
              nodes={nodes}
              onSelect={handleSelectResult}
            />
          </div>

          {/* Theme toggle (desktop inline) */}
          <Tooltip content={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}>
            <button
              className="hidden rounded-md p-1.5 hover:bg-white/10 lg:block"
              onClick={toggleTheme}
              aria-label="Toggle theme"
            >
              <Icon name={theme === 'dark' ? 'sun' : 'moon'} size={18} />
            </button>
          </Tooltip>

          {/* Presenter toggle */}
          <Tooltip content="Presenter mode (P)">
            <button
              className={`rounded-md p-1.5 hover:bg-white/10 ${presenterMode ? 'text-accent' : ''}`}
              onClick={() => setPresenterMode((v) => !v)}
              aria-label="Toggle presenter mode"
            >
              <Icon name="presenter" size={18} />
            </button>
          </Tooltip>

          {/* Settings placeholder */}
          <Tooltip content="Settings">
            <button
              className="rounded-md p-1.5 hover:bg-white/10"
              onClick={() => setSidebarOpen((v) => !v)}
              aria-label="Settings"
            >
              <Icon name="settings" size={18} />
            </button>
          </Tooltip>
        </header>

        {/* Graph canvas */}
        <div className="relative flex-1">
          <GraphCanvas
            nodes={nodes}
            edges={edges}
            onNodeClick={handleNodeClick}
            selectedNodeId={selected?.id ?? null}
            presenterMode={presenterMode}
          />

          {/* Bottom-left stats pill */}
          <div className="absolute bottom-4 left-4 flex items-center gap-3 rounded-full bg-surface-alt/90 px-4 py-2 text-xs text-muted shadow-lg backdrop-blur-sm">
            <span className="flex items-center gap-1">
              <Icon name="graph" size={12} />
              {stats.nodes}
            </span>
            <span className="h-3 w-px bg-border" />
            <span>{stats.edges} links</span>
            <span className="h-3 w-px bg-border" />
            <span className="flex items-center gap-1">
              <span
                className={`h-2 w-2 rounded-full ${
                  syncStatus === 'syncing'
                    ? 'animate-pulse bg-yellow-400'
                    : 'bg-green-400'
                }`}
              />
              {peerCount} peer{peerCount !== 1 ? 's' : ''}
            </span>
          </div>

          {/* Keyboard shortcut hint */}
          <div className="absolute bottom-4 right-4 text-[10px] text-muted/50">
            <kbd className="rounded border border-border bg-surface-alt px-1">/</kbd> search
            &nbsp;
            <kbd className="rounded border border-border bg-surface-alt px-1">P</kbd> present
            &nbsp;
            <kbd className="rounded border border-border bg-surface-alt px-1">Esc</kbd> close
          </div>
        </div>
      </main>

      {/* ---- Mobile sidebar overlay ---- */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-20 bg-black/50 lg:hidden"
          onClick={() => setSidebarOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* ---- Node Detail Modal ---- */}
      <Modal
        open={detailOpen}
        onClose={() => {
          setDetailOpen(false);
          setExplanation('');
        }}
        title={selected?.label ?? 'Node Detail'}
      >
        {selected && (
          <NodeCard
            node={selected}
            onExplain={handleExplain}
            explanation={explanation}
            explaining={explaining}
          />
        )}
      </Modal>
    </div>
  );
}
