# Project Mycelium

**Nurturing Knowledge Without the Cloud**

> A local-first, peer-to-peer knowledge graph with offline AI,
> CRDT sync, content-addressed storage, and zero cloud dependency.

## TL;DR

```bash
# One-command setup
git clone https://github.com/Zorvia/project-mycelium.git
cd project-mycelium
npm run setup   # installs everything, seeds data, starts dev servers
# Open http://localhost:3000
```

Or try the offline demo: open `demo/mycelium_demo.html` in any browser.

---

## What is Project Mycelium?

Project Mycelium is a privacy-first knowledge graph application that runs
entirely on your device. No accounts, no cloud, no subscriptions.

**Key Features:**

- **Local-first** — All data stays on your device in SQLite
- **Peer-to-peer sync** — Collaborate without servers using WebRTC + CRDTs
- **On-device AI** — WebLLM explains concepts in your browser
- **Content-addressed** — SHA-256 hashing ensures data integrity
- **Encrypted** — AES-256-GCM encryption for P2P sharing
- **Offline** — Works without internet; syncs when reconnected

## Screenshots

> *Dark theme graph explorer with force-directed layout*

```
┌─────────────────────────────────────────────┐
│  ☰  Project Mycelium      🔍  ◐  ⚙       │
├─────────────────────────────────────────────┤
│                                             │
│       ◉ Physics ─── ◉ Quantum              │
│      ╱    │          │    ╲                 │
│  ◉ Math   │      ◉ Particle    ◉ Optics   │
│      ╲    │     ╱    │                      │
│       ◉ Energy ─── ◉ Wave                  │
│           │              │                   │
│       ◉ Thermo      ◉ Light                │
│                                             │
├─────────────────────────────────────────────┤
│  📊 30 nodes  │  42 edges  │  🔒 Encrypted │
└─────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

- **Node.js** >= 18
- **Python** >= 3.11

### Development

```bash
# Frontend
cd src/frontend && npm ci

# Backend
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Seed demo data
python scripts/seed_demo_data.py

# Start dev servers (frontend:3000, backend:8000)
npm run dev
```

### Production Build

```bash
# Build frontend
npm run build

# Export static demo
python scripts/export_demo.py

# Docker
docker build -t mycelium:demo .
docker run -p 8000:8000 mycelium:demo
```

## Project Structure

```
project-mycelium/
├── src/
│   ├── backend/          # Python FastAPI backend
│   │   └── mycelium/ # Main package
│   └── frontend/         # React TypeScript frontend
│       └── src/
│           ├── components/  # UI component library
│           ├── crdt/        # CRDT engine (Yjs)
│           ├── p2p/         # WebRTC peer networking
│           ├── ai/          # WebLLM adapter
│           ├── graph/       # Graph explorer (D3.js)
│           └── store/       # State management
├── data/                 # Demo data and databases
├── demo/                 # Static export output
├── docs/                 # Extended documentation
├── scripts/              # Build and utility scripts
├── tests/                # All test suites
├── ci/                   # GitHub Actions workflows
└── deploy/               # Deployment configurations
```

## Documentation

| Document | Description |
|----------|-------------|
| [DEPLOYMENT.md](DEPLOYMENT.md) | Deploy to Netlify, Vercel, Cloudflare, Render, Docker |
| [PRESENTER.md](PRESENTER.md) | 60s script, 5 slides, demo path, Q&A |
| [FAQ.md](FAQ.md) | 40+ questions for judges, teachers, devs, admins |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design, diagrams, tech decisions |
| [DESIGN.md](docs/DESIGN.md) | Design tokens, components, accessibility |
| [PERFORMANCE.md](PERFORMANCE.md) | Optimization strategies and tuning |
| [SECURITY.md](SECURITY.md) | Security architecture and policies |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React, TypeScript, Vite, D3.js, TailwindCSS |
| Backend | Python 3.11+, FastAPI, SQLAlchemy, SQLite |
| Sync | Yjs (CRDT), WebRTC DataChannels |
| AI | WebLLM (WebGPU), deterministic fallback |
| Storage | SHA-256 content addressing, AES-256-GCM encryption |
| Tests | Vitest, pytest, Playwright |
| CI/CD | GitHub Actions, Docker |

## License

Licensed under the [Zorvia Public License v2.0](LICENSE.md) (ZPL v2.0).

Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)

---

*Project Mycelium — like the underground network that connects a forest,
we connect knowledge without a central server.*
