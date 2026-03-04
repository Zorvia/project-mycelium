# Performance Guide

## TL;DR

Project Mycelium is optimized for smooth interaction with graphs of 30–200
nodes on modest hardware. This guide details the optimization strategies
used and tuning options available.

---

## Frontend Performance

### Graph Rendering

| Technique | Description |
|-----------|-------------|
| **Dynamic LOD** | Nodes far from viewport render as simple circles; nearby nodes show full detail |
| **Viewport culling** | Only nodes within the visible canvas area are rendered to the DOM |
| **requestAnimationFrame** | All animation uses rAF for smooth 60fps rendering |
| **Throttled physics** | Force simulation ticks are throttled during drag operations |
| **Canvas fallback** | For graphs > 100 nodes, rendering switches from SVG to Canvas |
| **Web Workers** | Force layout computation offloaded to a Web Worker for > 50 nodes |

### Bundle Size

| Asset | Strategy |
|-------|----------|
| **Code splitting** | Route-based lazy loading via React.lazy() |
| **Tree shaking** | Vite's Rollup-based tree shaking eliminates dead code |
| **Font subsetting** | Inter Variable loaded with `unicode-range` for Latin subset only |
| **SVG sprites** | Icons bundled as a single SVG sprite sheet |
| **Compression** | Brotli pre-compression for static assets |

### Metrics Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| First Contentful Paint | < 1.5s | Lighthouse |
| Time to Interactive | < 3.0s | Lighthouse |
| Graph render (50 nodes) | < 500ms | Performance.mark |
| Graph render (200 nodes) | < 2s | Performance.mark |
| Bundle size (gzipped) | < 250KB | Vite build output |

## Backend Performance

### Database

- **SQLite WAL mode** enabled by default for concurrent reads.
- **In-memory LRU cache** for frequently accessed subgraphs (128 entry default).
- **Prepared statements** via SQLAlchemy for query plan reuse.
- **Connection pooling**: 5 connections default, configurable.

### API

- **Async handlers**: all I/O-bound endpoints use `async/await`.
- **Streaming responses**: large graph exports use streaming JSON.
- **ETag caching**: subgraph responses include ETags for conditional requests.
- **Gzip middleware**: responses > 500 bytes are compressed.

### Production Options

For heavier workloads, optional upgrades:

```bash
# PostgreSQL (recommended for > 1000 nodes)
MYCELIUM_DB_URL=postgresql+asyncpg://user:pass@localhost/mycelium

# Redis caching (recommended for multi-user)
MYCELIUM_CACHE_URL=redis://localhost:6379/0
```

## Static Export Performance

The offline demo uses precomputed optimizations:

- **Precomputed layout**: Node positions pre-calculated and embedded in JSON.
- **Inlined assets**: CSS, JS, SVG, and data bundled into a single HTML file.
- **No runtime layout cost**: Force simulation skipped; positions loaded directly.
- **Lazy rendering**: Nodes outside initial viewport rendered on scroll.

## Profiling

### Frontend

```bash
# Build with source maps for profiling
cd src/frontend && VITE_SOURCEMAP=true npx vite build

# Use Chrome DevTools Performance tab
# Or React DevTools Profiler
```

### Backend

```bash
# Profile with py-spy
pip install py-spy
py-spy record -o profile.svg -- python -m uvicorn mycelium.main:app

# Or use cProfile
python -m cProfile -o profile.prof -m mycelium.main
```

## Configuration

Environment variables for performance tuning:

| Variable | Default | Description |
|----------|---------|-------------|
| `MYCELIUM_CACHE_SIZE` | `128` | LRU cache entries |
| `MYCELIUM_DB_POOL_SIZE` | `5` | Database connection pool |
| `MYCELIUM_MAX_GRAPH_NODES` | `500` | Maximum nodes returned per query |
| `MYCELIUM_WORKER_THREADS` | `2` | Uvicorn worker threads |
| `MYCELIUM_GRAPH_LOD_THRESHOLD` | `100` | Node count to enable LOD |

---

Copyright (c) 2026 Zorvia Community. Licensed under ZPL v2.0.
