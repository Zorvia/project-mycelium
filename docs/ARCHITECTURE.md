# Architecture

## TL;DR

Project Mycelium is a local-first, peer-to-peer knowledge graph with four
layers: Storage, Sync, Intelligence, and Presentation. All data stays on
the user's device unless explicitly shared.

---

## System Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                     │
│  React + TypeScript + D3.js + TailwindCSS                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐  │
│  │  Graph   │ │  Search  │ │  Detail  │ │ Presenter  │  │
│  │ Explorer │ │  + Auto  │ │   Pane   │ │   Mode     │  │
│  └──────────┘ └──────────┘ └──────────┘ └────────────┘  │
├─────────────────────────────────────────────────────────┤
│                   Intelligence Layer                     │
│  ┌──────────────────┐  ┌───────────────────────────┐    │
│  │  WebLLM Adapter  │  │  Stub Summarizer          │    │
│  │  (WebGPU model)  │  │  (deterministic fallback) │    │
│  └──────────────────┘  └───────────────────────────┘    │
├─────────────────────────────────────────────────────────┤
│                      Sync Layer                          │
│  ┌──────────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │  Yjs CRDT    │  │  WebRTC  │  │  Gossip Protocol │  │
│  │  Documents   │  │  Data Ch │  │  (LAN discovery) │  │
│  └──────────────┘  └──────────┘  └──────────────────┘  │
├─────────────────────────────────────────────────────────┤
│                    Storage Layer                          │
│  ┌──────────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │   SQLite /   │  │  Content │  │  AES-256-GCM     │  │
│  │  PostgreSQL  │  │  Address │  │  Encryption      │  │
│  └──────────────┘  └──────────┘  └──────────────────┘  │
│                                                          │
│  FastAPI + SQLAlchemy (Python 3.11+)                     │
└─────────────────────────────────────────────────────────┘
```

---

## Network Topology

### Mesh (Our Approach)

```
    ┌────┐         ┌────┐
    │ P1 │─────────│ P2 │
    └──┬─┘         └─┬──┘
       │    ╲    ╱    │
       │     ╲  ╱     │
       │      ╲╱      │
       │      ╱╲      │
       │     ╱  ╲     │
       │    ╱    ╲    │
    ┌──┴─┐         ┌─┴──┐
    │ P3 │─────────│ P4 │
    └────┘         └────┘

  ✓ No single point of failure
  ✓ Works offline
  ✓ Direct peer connections
  ✓ Data stays between peers
```

### Star (Traditional Cloud)

```
         ┌────────┐
         │ Server │
         └───┬────┘
        ╱    │    ╲
       ╱     │     ╲
    ┌────┐ ┌────┐ ┌────┐
    │ C1 │ │ C2 │ │ C3 │
    └────┘ └────┘ └────┘

  ✗ Single point of failure
  ✗ Requires internet
  ✗ Data on corporate servers
  ✗ Privacy concerns
```

---

## Sequence Diagrams

### Upload Flow

```
User              Frontend           Backend           Storage
 │                   │                  │                  │
 │  Create Node      │                  │                  │
 │──────────────────>│                  │                  │
 │                   │  POST /nodes     │                  │
 │                   │─────────────────>│                  │
 │                   │                  │  Chunk (256KB)   │
 │                   │                  │─────────────────>│
 │                   │                  │  SHA-256 CID     │
 │                   │                  │<─────────────────│
 │                   │                  │  Encrypt (AES)   │
 │                   │                  │─────────────────>│
 │                   │                  │  Store chunk     │
 │                   │                  │<─────────────────│
 │                   │  200 + CID       │                  │
 │                   │<─────────────────│                  │
 │                   │  CRDT Update     │                  │
 │                   │  (Yjs encode)    │                  │
 │  Confirmation     │                  │                  │
 │<──────────────────│                  │                  │
```

### Gossip / P2P Sync

```
Peer A              Peer B              Peer C
  │                   │                   │
  │  WebRTC Connect   │                   │
  │──────────────────>│                   │
  │  DTLS Handshake   │                   │
  │<─────────────────>│                   │
  │                   │                   │
  │  Yjs State Vec    │                   │
  │──────────────────>│                   │
  │  Yjs State Vec    │                   │
  │<──────────────────│                   │
  │                   │                   │
  │  Missing Updates  │                   │
  │──────────────────>│                   │
  │  Missing Updates  │                   │
  │<──────────────────│                   │
  │                   │                   │
  │  CRDT Merged ✓    │                   │
  │                   │  Gossip forward   │
  │                   │──────────────────>│
  │                   │  Yjs State Vec    │
  │                   │<─────────────────>│
  │                   │  CRDT Merged ✓    │
  │                   │                   │
```

### Encryption / Key Flow

```
User               Key Store            Crypto            Storage
 │                    │                    │                  │
 │  Derive Key        │                    │                  │
 │───────────────────>│                    │                  │
 │                    │  PBKDF2(seed,salt) │                  │
 │                    │───────────────────>│                  │
 │                    │  AES-256 Key       │                  │
 │                    │<───────────────────│                  │
 │                    │  Store locally     │                  │
 │                    │                    │                  │
 │  Encrypt Chunk     │                    │                  │
 │───────────────────>│                    │                  │
 │                    │  AES-GCM(key,iv)   │                  │
 │                    │───────────────────>│                  │
 │                    │  Ciphertext + Tag  │                  │
 │                    │<───────────────────│                  │
 │                    │                    │  Store           │
 │                    │                    │─────────────────>│
 │  CID returned      │                    │                  │
 │<───────────────────│                    │                  │
```

---

## Data Model

```
┌──────────────────────┐
│       Graph          │
├──────────────────────┤
│ id: UUID             │
│ name: string         │
│ created_at: datetime │
│ updated_at: datetime │
│ crdt_state: bytes    │
└──────┬───────────────┘
       │ 1:N
       │
┌──────┴───────────────┐      ┌──────────────────────┐
│       Node           │      │       Edge           │
├──────────────────────┤      ├──────────────────────┤
│ id: UUID             │      │ id: UUID             │
│ graph_id: FK         │      │ source_id: FK(Node)  │
│ label: string        │      │ target_id: FK(Node)  │
│ category: string     │      │ label: string        │
│ description: text    │      │ weight: float        │
│ metadata: JSON       │      │ metadata: JSON       │
│ position_x: float    │      └──────────────────────┘
│ position_y: float    │
│ cid: string          │
│ chunk_ids: JSON      │
└──────────────────────┘
```

---

## Technology Decisions

| Decision | Choice | Reasoning |
|----------|--------|-----------|
| **CRDT** | Yjs | Best-in-class performance, wide adoption, sub-document support |
| **Transport** | WebRTC | Browser-native, NAT traversal, encrypted by default |
| **Storage** | SQLite | Zero-config, serverless, perfect for local-first |
| **Hashing** | SHA-256 | Industry standard, Web Crypto API support |
| **Encryption** | AES-256-GCM | Authenticated encryption, hardware acceleration |
| **Frontend** | React + TS | Ecosystem, hiring pool, type safety |
| **Graph Viz** | D3.js | Most flexible, force-directed layouts, SVG/Canvas |
| **Build** | Vite | Fast HMR, optimized builds, ESM-native |
| **API** | FastAPI | Async-first, auto-docs, Pydantic validation |
| **AI** | WebLLM | On-device inference, WebGPU acceleration, privacy |

---

Copyright (c) 2026 Zorvia Community. Licensed under ZPL v2.0.
