<div align="center" style="background:#0a0e14;padding:20px;border-radius:16px">


<img src="Mycelium.png" alt="Project Mycelium Logo" width="200" />

# 🌐 Project Mycelium

**A local-first, peer-to-peer knowledge graph with offline AI, CRDT sync, and encrypted storage — zero cloud dependency.**

<p>
<img src="https://img.shields.io/github/actions/workflow/status/Zorvia/project-mycelium/ci.yml?style=for-the-badge&logo=github&logoColor=white&color=0d1a2b&label=build">
<img src="https://img.shields.io/github/v/release/Zorvia/project-mycelium?style=for-the-badge&logo=semantic-release&logoColor=white&color=0d1a2b&label=version">
<img src="https://img.shields.io/github/license/Zorvia/project-mycelium?style=for-the-badge&logo=open-source-initiative&logoColor=white&color=0d1a2b">
<img src="https://img.shields.io/github/last-commit/Zorvia/project-mycelium?style=for-the-badge&logo=github&logoColor=white&color=0d1a2b">
</p>

</div>

---

## ✦ Overview

Project Mycelium is designed for **private, offline knowledge management** with:

* **Local-first storage** – SQLite + content-addressed SHA-256 + AES-256-GCM
* **Peer-to-peer collaboration** – WebRTC mesh network, conflict-free edits
* **Offline AI explanations** – WebLLM on-device intelligence
* **Interactive graph** – D3.js visualization of nodes and connections

> Like fungal mycelium, ideas propagate underground — resilient, private, and interconnected.

---

## ✦ Features

<details>
<summary>Click to expand features</summary>

* **Local-first & encrypted storage** – Keep data on your device with AES-256-GCM.
* **CRDT sync** – Yjs ensures safe, conflict-free peer collaboration.
* **On-device AI** – WebLLM explains concepts without internet or cloud.
* **Interactive visualizations** – D3.js graphs for exploring knowledge networks.
* **Static offline demo** – Open `demo/mycelium_demo.html` anywhere.

</details>

---

## ✦ Quick Start

### Clone & Run

```bash
git clone https://github.com/Zorvia/project-mycelium.git
cd project-mycelium
npm run dev
```

* Frontend → [http://localhost:3000](http://localhost:3000)
* Backend  → [http://localhost:8000](http://localhost:8000)
* API docs → [http://localhost:8000/docs](http://localhost:8000/docs)

### Offline Demo

```bash
python scripts/export_demo.py
# Open demo/mycelium_demo.html in any browser
```

### Docker

```bash
docker build -t mycelium:demo .
docker run -p 8000:8000 mycelium:demo
# Visit http://localhost:8000
```

---

## ✦ Architecture

```mermaid
graph LR
    subgraph "🖥️ Device"
        UI["React UI<br/>Graph Explorer"]
        AI["WebLLM AI"]
        CRDT["Yjs CRDT"]
        API["FastAPI Backend"]
        DB["SQLite DB"]
        CHUNK["Chunking + AES-256-GCM"]
    end

    subgraph "🌐 Peer Network"
        P1["Peer A"]
        P2["Peer B"]
    end

    UI --> API
    UI --> AI
    UI --> CRDT
    API --> CHUNK --> DB
    CRDT <-->|WebRTC| P1
    CRDT <-->|WebRTC| P2
```

<details>
<summary>Data Flow</summary>

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant Storage

    User->>Frontend: Create node "Quantum Mechanics"
    Frontend->>Backend: POST /api/graphs/{id}/nodes
    Backend->>Storage: Chunk & encrypt data
    Storage-->>Backend: SHA-256 content ID
    Backend-->>Frontend: Node created
    Frontend->>Frontend: Update CRDT
    Frontend-->>User: Node appears on graph ✓
```

</details>

---

## ✦ Demo Knowledge Graph

```mermaid
graph LR
Physics((Physics)) --> QM(Quantum<br/>Mechanics)
Physics --> Thermo(Thermo-<br/>dynamics)
Math((Mathematics)) --> Calc(Calculus)
Math --> LinAlg(Linear<br/>Algebra)
Physics -.->|depends_on| Math
QM -.->|requires| LinAlg
Chem((Chemistry)) --> OrgChem(Organic<br/>Chemistry)
Bio((Biology)) --> Genetics(Genetics)
CS((Computer Science)) --> ML(Machine<br/>Learning)
ML -.->|uses| Stats((Statistics))
```

<details>
<summary>ASCII fallback (terminals)</summary>

```
Physics ──► Quantum Mechanics
Math    ──► Calculus
Physics depends_on Math
Quantum Mechanics requires Linear Algebra
```

</details>

---

## ✦ Project Structure

```bash
project-mycelium/
├── src/
│   ├── backend/
│   └── frontend/
├── scripts/
├── demo/
├── docs/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── package.json
├── requirements.txt
└── LICENSE.md
```

---

## ✦ Philosophy

* **Your data is yours** – no cloud, no accounts, fully encrypted
* **Knowledge should be free** – open-source, educational, and collaborative
* **Privacy by default** – encryption is standard

---

## ✦ Contributing

* Clear, maintainable code
* Respect project architecture & style
* All contributions welcome

Repository: [GitHub](https://github.com/Zorvia/project-mycelium)

---

## ✦ License

[Zorvia Public License v2.0](LICENSE.md)

```text
Copyright (c) 2026 Zorvia Community

Permission granted to use, copy, modify, and distribute under ZPL v2.0
```

---

<div align="center">

```text
        ◉───────◉───────◉
       ╱ ╲     ╱ ╲     ╱ ╲
      ◉   ◉───◉   ◉───◉   ◉
       ╲ ╱     ╲ ╱     ╲ ╱
        ◉───────◉───────◉
```

**Project Mycelium** — Nurturing Knowledge Without the Cloud
Built by the Zorvia Community

</div>

---

