/*
  Project Mycelium — Nurturing Knowledge Without the Cloud
  Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)

  Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
  See LICENSE.md for full text.

  THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
  See LICENSE.md for details and disclaimers.
*/

/** API client for communicating with the Project Mycelium backend. */

import type { Graph, GraphNode, GraphEdge, SearchResult, HealthStatus } from './types';

const BASE_URL = '/api';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || `Request failed: ${res.status}`);
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

// ─── Graphs ────────────────────────────────────

export const api = {
  // Health
  health: () => fetch('/health').then(r => r.json()) as Promise<HealthStatus>,

  // Graphs
  listGraphs: () => request<Graph[]>('/graphs'),
  getGraph: (id: string) => request<Graph>(`/graphs/${id}`),
  createGraph: (data: { name: string; description?: string }) =>
    request<Graph>('/graphs', { method: 'POST', body: JSON.stringify(data) }),
  deleteGraph: (id: string) =>
    request<void>(`/graphs/${id}`, { method: 'DELETE' }),

  // Nodes
  listNodes: (graphId: string) =>
    request<GraphNode[]>(`/graphs/${graphId}/nodes`),
  createNode: (graphId: string, data: Partial<GraphNode>) =>
    request<GraphNode>(`/graphs/${graphId}/nodes`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  deleteNode: (nodeId: string) =>
    request<void>(`/nodes/${nodeId}`, { method: 'DELETE' }),

  // Edges
  listEdges: (graphId: string) =>
    request<GraphEdge[]>(`/graphs/${graphId}/edges`),
  createEdge: (graphId: string, data: Partial<GraphEdge>) =>
    request<GraphEdge>(`/graphs/${graphId}/edges`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  deleteEdge: (edgeId: string) =>
    request<void>(`/edges/${edgeId}`, { method: 'DELETE' }),

  // Search
  search: (query: string, graphId?: string) =>
    request<SearchResult>('/search', {
      method: 'POST',
      body: JSON.stringify({ query, graph_id: graphId }),
    }),

  // Export
  exportGraph: (graphId: string) =>
    request<{ graph: Graph; nodes: GraphNode[]; edges: GraphEdge[] }>(
      `/graphs/${graphId}/export`,
    ),
};
