/*
  Project Mycelium — Nurturing Knowledge Without the Cloud
  Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)

  Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
  See LICENSE.md for full text.

  THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
  See LICENSE.md for details and disclaimers.
*/

/** Shared TypeScript types for the Project Mycelium frontend. */

export interface GraphNode {
  id: string;
  graphId: string;
  label: string;
  category: string;
  description: string | null;
  positionX: number | null;
  positionY: number | null;
  cid: string | null;
  metadata: Record<string, unknown> | null;
  createdAt: string;
  updatedAt: string;
  // Runtime (D3)
  x?: number;
  y?: number;
  fx?: number | null;
  fy?: number | null;
  vx?: number;
  vy?: number;
}

export interface GraphEdge {
  id: string;
  graphId: string;
  sourceId: string;
  targetId: string;
  label: string;
  weight: number;
  metadata: Record<string, unknown> | null;
  createdAt: string;
  // Runtime (D3)
  source?: GraphNode | string;
  target?: GraphNode | string;
}

export interface Graph {
  id: string;
  name: string;
  description: string | null;
  createdAt: string;
  updatedAt: string;
  nodeCount: number;
  edgeCount: number;
  metadata: Record<string, unknown> | null;
}

export interface SearchResult {
  nodes: GraphNode[];
  total: number;
}

export interface HealthStatus {
  status: string;
  version: string;
}

// ─── UI State ──────────────────────────────────

export type ThemeMode = 'dark' | 'light';

export interface AppState {
  theme: ThemeMode;
  selectedNodeId: string | null;
  searchQuery: string;
  presenterMode: boolean;
  presenterStep: number;
  sidebarOpen: boolean;
  graphId: string | null;
  onboardingComplete: boolean;
}

// ─── Category colors for graph nodes ───────────

export const CATEGORY_COLORS: Record<string, string> = {
  physics: '#6D9BF1',
  chemistry: '#A78BFA',
  biology: '#34D399',
  mathematics: '#F59E0B',
  computer_science: '#EF4444',
  earth_science: '#22C55E',
  astronomy: '#818CF8',
  engineering: '#FB923C',
  medicine: '#EC4899',
  default: '#94A3B8',
};

// ─── Presenter Steps ───────────────────────────

export interface PresenterStep {
  id: string;
  title: string;
  description: string;
  highlight?: string; // CSS selector to highlight
  action?: () => void;
}
