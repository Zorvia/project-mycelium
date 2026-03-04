<div align="center">

<img src="https://stav.org.au/wp-content/uploads/2023/11/cropped-cropped-STAV_Logo_small-1.png" alt="Project Logo" width="200" />

<br />

# Project Mycelium

### *Nurturing Knowledge — Without the Cloud*

**A local-first, peer-to-peer knowledge graph with offline AI, CRDT sync, encrypted content-addressed storage — and zero cloud dependency.**

[![CI](https://github.com/Zorvia/project-mycelium/actions/workflows/ci.yml/badge.svg)](https://github.com/Zorvia/project-mycelium/actions/workflows/ci.yml)
[![License: ZPL v2.0](https://img.shields.io/badge/License-ZPL%20v2.0-blue.svg)](LICENSE.md)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python\&logoColor=white)](https://python.org)
[![Node 18+](https://img.shields.io/badge/Node.js-18%2B-339933?logo=nodedotjs\&logoColor=white)](https://nodejs.org)

</div>

---

> Like fungal networks connecting a forest underground, **Project Mycelium** links knowledge privately and resiliently — on your device, between peers, and without a central server.

---

## TL;DR — Run the demo in seconds

```bash
# Clone and run — one command
git clone https://github.com/Zorvia/project-mycelium.git
cd project-mycelium && npm run dev

# Frontend → http://localhost:3000
# Backend  → http://localhost:8000
# API docs → http://localhost:8000/docs
```

**No server? No problem.** Open `demo/mycelium_demo.html` in any browser — no install, no internet, no signup.

<details>
<summary><strong>Other quick options</strong></summary>

```bash
# Docker (backend + frontend)
docker build -t mycelium:demo .
docker run -p 8000:8000 mycelium:demo

# Export static demo
python scripts/export_demo.py  # → demo/mycelium_demo.html

# Seed demo DB
python scripts/seed_demo_data.py
```

</details>

---

## Why this exists

* **Privacy-first** — Your notes stay local (SQLite). No accounts, no cloud tracking.
* **Resilient collaboration** — Peer-to-peer sync (WebRTC + Yjs) with automatic CRDT merges.
* **Offline intelligence** — On-device WebLLM gives explanations without sending your data anywhere.
* **Secure by default** — Content-addressed storage (SHA-256) + AES-256-GCM for shared content.
* **Educational focus** — Map concepts, collaborate offline, and ask AI to explain ideas.

---

## Core Principles

|                Principle | What it means                                               |
| -----------------------: | ----------------------------------------------------------- |
|      🖥️ **Local-first** | Data lives on *your* device (SQLite). You own it.           |
|      🌐 **Peer-to-peer** | Collaborate directly over WebRTC — no server required.      |
|        🤖 **Offline AI** | WebLLM runs on-device for private concept explanations.     |
|         🔐 **Encrypted** | AES-256-GCM for shared data; authenticated, tamper-evident. |
|     ♻️ **Conflict-free** | Yjs CRDTs merge concurrent edits automatically.             |
| 🧩 **Content-addressed** | SHA-256 CIDs: content identity follows content.             |

---

## Architecture (at a glance)

```mermaid
graph TB
    subgraph "🖥️ Your Device"
        UI["React UI<br/>Graph Explorer + Components"]
        AI["WebLLM<br/>On-Device AI"]
        CRDT["Yjs CRDT<br/>Conflict-Free Sync"]
        API["FastAPI<br/>REST Backend"]
        DB["SQLite<br/>Local Database"]
        CHUNK["Chunking Engine<br/>SHA-256 + AES-256-GCM"]
    end

    subgraph "🌐 Peer Network (Optional)"
        P1["Peer A"]
        P2["Peer B"]
        P3["Peer C"]
    end

    UI --> API
    UI --> AI
    UI --> CRDT
    API --> CHUNK
    API --> DB
    CHUNK --> DB
    CRDT <-->|"WebRTC DataChannel"| P1
    CRDT <-->|"WebRTC"| P2
    P1 <-->|"Gossip"| P3

    style UI fill:#6D9BF1,stroke:#334,color:#fff
    style AI fill:#A78BFA,stroke:#334,color:#fff
    style CRDT fill:#34D399,stroke:#334,color:#111
    style API fill:#F59E0B,stroke:#334,color:#111
    style DB fill:#94A3B8,stroke:#334,color:#111
    style CHUNK fill:#EF4444,stroke:#334,color:#fff
```

---

## Demo Knowledge Graph

```mermaid
graph LR
    Physics((Physics)) --> QM(Quantum<br/>Mechanics)
    Physics --> Thermo(Thermo-<br/>dynamics)
    Physics --> EM(Electro-<br/>magnetism)
    Physics --> Optics(Optics)
    Physics --> Particle(Particle<br/>Physics)
    Physics --> Relativity(Relativity)
    Physics --> Wave(Wave<br/>Theory)

    Math((Mathematics)) --> Calc(Calculus)
    Math --> LinAlg(Linear<br/>Algebra)
    Math --> Stats(Statistics)
    Math --> Prob(Probability)
    Math --> Topology(Topology)
    Math --> NumTheory(Number<br/>Theory)
    Math --> GraphTh(Graph<br/>Theory)

    Chem((Chemistry)) --> OrgChem(Organic<br/>Chemistry)
    Chem --> Biochem(Biochemistry)

    Bio((Biology)) --> Genetics(Genetics)
    Bio --> Ecology(Ecology)
    Bio --> Neuro(Neuro-<br/>science)
    Bio --> MolBio(Molecular<br/>Biology)
    Bio --> Evolution(Evolution)

    CS((Computer<br/>Science)) --> Algo(Algorithms)
    CS --> ML(Machine<br/>Learning)
    CS --> Crypto(Cryptography)
    CS --> InfoTheory(Information<br/>Theory)

    Astro((Astronomy)) --> Cosmo(Cosmology)

    Earth((Earth<br/>Science)) --> Geology(Geology)
    Earth --> Climate(Climate<br/>Science)

    Physics -.->|depends_on| Math
    QM -.->|requires| LinAlg
    Chem -.->|related_to| Physics
    Biochem -.->|bridges| Bio
    ML -.->|uses| Stats
    ML -.->|uses| Prob
    Crypto -.->|uses| NumTheory
    Astro -.->|depends_on| Physics
    GraphTh -.->|applied_in| CS
    Genetics -.->|related_to| MolBio
    InfoTheory -.->|related_to| Prob

    style Physics fill:#6D9BF1,stroke:#334,color:#fff
    style Math fill:#A78BFA,stroke:#334,color:#fff
    style Chem fill:#34D399,stroke:#334,color:#111
    style Bio fill:#22C55E,stroke:#334,color:#111
    style CS fill:#F59E0B,stroke:#334,color:#111
    style Astro fill:#EF4444,stroke:#334,color:#fff
    style Earth fill:#94A3B8,stroke:#334,color:#111
```

---

## Quick Start

```bash
# Clone
git clone https://github.com/Zorvia/project-mycelium.git
cd project-mycelium

# Frontend
cd src/frontend
npm ci
cd ../..

# Python
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Seed demo DB
python scripts/seed_demo_data.py

# Run
npm run dev
```

Open `http://localhost:3000` for frontend, `http://localhost:8000/docs` for backend API.

---

## License

**[Zorvia Public License v2.0](LICENSE.md)**

---

<div align="center">

```
        ◉───────◉───────◉
       ╱ ╲     ╱ ╲     ╱ ╲
      ◉   ◉───◉   ◉───◉   ◉
       ╲ ╱     ╲ ╱     ╲ ╱
        ◉───────◉───────◉
```

**Project Mycelium** — Nurturing Knowledge Without the Cloud

Built with care by the Zorvia Community · [Getting Started](#tl-dr) · [Documentation](#documentation) · [Contributing](CONTRIBUTING.md)

</div>
