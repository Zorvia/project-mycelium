# Presenter Guide

## TL;DR

This guide helps you present Project Mycelium in 60–90 seconds. Follow the
script, use presenter mode, and anticipate judge questions.

---

## 60-Second Script

> "Project Mycelium is a local-first, peer-to-peer knowledge graph that
> works entirely offline — no cloud required.
>
> [Click: Open graph explorer]
>
> Here you see a knowledge graph of scientific concepts. Each node is a
> topic, each edge is a relationship. Everything is stored locally on
> your device using content-addressed storage — like Git for knowledge.
>
> [Click: Select a node]
>
> When I click a node, I get a detailed view with an AI-generated
> explanation — and that AI runs entirely in your browser using WebLLM.
> No data leaves your device.
>
> [Click: Show P2P sync]
>
> Multiple users can collaborate peer-to-peer using CRDTs. Edits merge
> automatically, even after offline periods, with mathematical
> guarantees of convergence.
>
> [Click: Show encryption]
>
> All data is encrypted with AES-256-GCM before sharing. Keys stay
> on your device. Privacy by design.
>
> Project Mycelium — nurturing knowledge without the cloud."

---

## Elevator Pitch Card

**One line:** A local-first, P2P knowledge graph with offline AI and
zero cloud dependency.

**Three bullets:**
1. **Private**: All data stays on your device; AES-256 encrypted.
2. **Collaborative**: CRDT-based sync means edits merge without conflicts.
3. **Intelligent**: On-device AI explains concepts without sending data anywhere.

---

## 5 Slides

### Slide 1: Title
- Project Mycelium
- "Nurturing Knowledge Without the Cloud"
- Zorvia Community | ZPL v2.0

### Slide 2: The Problem
- Knowledge tools require cloud accounts
- Data locked in corporate silos
- Privacy concerns with AI assistants
- No offline access

### Slide 3: Our Solution
- Local-first: everything on your device
- P2P sync: collaborate without servers
- Content-addressed: Git-like integrity
- On-device AI: WebLLM in your browser

### Slide 4: Technical Architecture
- Frontend: React + TypeScript + D3.js
- Backend: FastAPI + SQLite
- Sync: Yjs CRDTs + WebRTC
- AI: WebLLM (WebGPU)
- Storage: SHA-256 content addressing

### Slide 5: Demo & Impact
- Works offline (open demo/mycelium_demo.html)
- Open source under ZPL v2.0
- Designed for education and research
- "Try it now — no account needed"

---

## 3-Minute Demo Path

1. **0:00–0:30** — Open the app, show dark theme, explain the graph
2. **0:30–1:00** — Click a node, show detail pane, click "Explain"
3. **1:00–1:30** — Search for a topic, show autocomplete, navigate
4. **1:30–2:00** — Show presenter mode, auto-advance through steps
5. **2:00–2:30** — Demonstrate P2P: show two browser tabs syncing
6. **2:30–3:00** — Show encryption badge, privacy notice, wrap up

---

## Presenter Mode

Activate presenter mode from the UI:

1. Press `Ctrl+Shift+P` or click the **Presenter** button.
2. The UI enters full-screen minimal mode.
3. Press **→** or **Space** to advance steps.
4. Press **Esc** to exit.
5. Steps highlight relevant UI areas with overlay annotations.

---

## 6 Likely Q&A

### Q1: "How is this different from Notion/Obsidian?"
**A:** Those tools store data in the cloud or require accounts. Mycelium is
truly local-first with P2P sync — no server, no account, no cloud.

### Q2: "How do you handle conflicts when users edit offline?"
**A:** We use CRDTs (Conflict-free Replicated Data Types) via Yjs. Edits
merge automatically with mathematical guarantees of convergence.

### Q3: "Is the AI actually running locally?"
**A:** Yes, using WebLLM with WebGPU. For devices without GPU support, we
provide a deterministic template-based summarizer as a fallback.

### Q4: "What about security?"
**A:** All chunks are encrypted with AES-256-GCM before any P2P sharing.
Keys are derived locally and never transmitted. No data leaves the device
without explicit user consent.

### Q5: "Can this scale to large knowledge graphs?"
**A:** The graph explorer handles 200+ nodes with dynamic level-of-detail
rendering. For larger datasets, we use viewport culling and Canvas fallback.

### Q6: "What license is this under?"
**A:** The Zorvia Public License v2.0 (ZPL v2.0) — a permissive open-source
license that requires attribution and header preservation.

---

Copyright (c) 2026 Zorvia Community. Licensed under ZPL v2.0.
