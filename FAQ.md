# Frequently Asked Questions

## TL;DR

40+ questions answered across four categories: Judges, Teachers,
Developers, and Admins.

---

## For Judges

### 1. What is Project Mycelium?
A local-first, peer-to-peer knowledge graph application that works entirely
offline. It enables users to explore, create, and share knowledge without
any cloud dependency.

### 2. Why is it called "Mycelium"?
Mycelium is the underground network of fungi that connects trees and plants,
sharing nutrients without a central hub — just like our P2P knowledge network.

### 3. What problem does it solve?
Knowledge tools today require cloud accounts, exposing user data to corporate
servers. Mycelium keeps all data on the user's device while enabling
collaboration through P2P sync.

### 4. How is this different from existing tools?
Unlike Notion, Roam, or Obsidian Sync, Mycelium requires no account, no
server, and no subscription. It uses CRDTs for conflict-free collaboration
and content-addressed storage for data integrity.

### 5. What makes the technology innovative?
The combination of CRDTs (Yjs) for offline-first sync, content-addressed
storage (SHA-256 CIDs) for integrity, and on-device AI (WebLLM) for
privacy-preserving intelligence.

### 6. Can I try it right now?
Yes! Open `demo/mycelium_demo.html` in any modern browser. No
installation needed.

### 7. Is this production-ready?
The core functionality is production-quality with comprehensive tests,
documentation, and deployment guides. It's designed to be maintained and
extended by the Zorvia community.

### 8. What's the license?
Zorvia Public License v2.0 (ZPL v2.0) — a permissive open-source license
requiring attribution and header preservation.

### 9. How does the AI work without the cloud?
WebLLM runs small language models entirely in the browser using WebGPU. No
data is sent to external servers. A deterministic fallback summarizer works
on all devices.

### 10. What is the target audience?
Students, researchers, educators, and anyone who wants to organize knowledge
privately and collaboratively.

---

## For Teachers

### 11. Can I use this in my classroom?
Absolutely. Mycelium runs offline, making it perfect for classrooms with
limited or no internet. Students can explore knowledge graphs and
collaborate via local network P2P.

### 12. Do students need accounts?
No. Mycelium is account-free. Students simply open the application.

### 13. Can students collaborate on the same graph?
Yes, using peer-to-peer sync over a local network. Edits merge automatically
using CRDTs, even if students work offline and reconnect later.

### 14. Is it safe for students?
Yes. No data leaves the device. There's no cloud, no tracking, no analytics.
All content stays local unless the user explicitly joins a P2P session.

### 15. Can I create custom knowledge graphs?
Yes. The graph editor supports adding nodes, edges, and annotations. You
can also import data from JSON files.

### 16. Does it work on school computers?
It runs in any modern browser (Chrome, Firefox, Edge, Safari). No
installation required for the static demo.

### 17. Can I export student work?
Yes. Graphs can be exported as PNG, SVG, or JSON for grading and archiving.

### 18. Is there a guided tour for first-time users?
Yes. A built-in onboarding tour walks through the key features in 30
seconds. Presenter mode provides step-by-step guidance for demonstrations.

### 19. What subjects work best with knowledge graphs?
Science, history, literature, biology, computer science — any subject with
interconnected concepts benefits from graph visualization.

### 20. Can I customize the content?
Yes. Edit the seed data JSON or use the UI to create custom graphs. The
data format is simple and documented.

---

## For Developers

### 21. What's the tech stack?
Frontend: React + TypeScript + Vite + D3.js + TailwindCSS.
Backend: Python 3.11+ + FastAPI + SQLAlchemy + SQLite.
Sync: Yjs (CRDT) + WebRTC.
AI: WebLLM (optional).

### 22. How do I set up the dev environment?
```bash
git clone https://github.com/Zorvia/project-mycelium.git
cd project-mycelium
cd src/frontend && npm ci && cd ../..
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
npm run dev
```

### 23. How is the project structured?
```
src/backend/    — Python FastAPI backend
src/frontend/   — React TypeScript frontend
data/           — Demo data and databases
demo/           — Static export output
docs/           — Extended documentation
scripts/        — Build, seed, and verify scripts
tests/          — Unit, integration, and E2E tests
ci/             — CI/CD workflows
deploy/         — Deployment configuration
```

### 24. How do CRDTs work in this project?
We use Yjs documents for collaborative editing. Each user's edits are encoded
as CRDT operations that merge deterministically. The LWW (Last Writer Wins)
register resolves concurrent edits to the same field.

### 25. How does content addressing work?
Files are split into 256KB chunks. Each chunk is hashed with SHA-256 to
produce a Content Identifier (CID). The CID manifest ensures integrity
and deduplication. The seeder produces deterministic CIDs on every run.

### 26. How does the P2P layer work?
WebRTC DataChannels transport encrypted chunks between peers. Discovery
uses LAN multicast in development. The static demo simulates gossip locally.

### 27. Can I add a new CRDT type?
Yes. The CRDT module is extensible. Implement the `CRDTDocument` interface
and register it in the merge engine. See `src/frontend/src/crdt/` for
examples.

### 28. How do I run tests?
```bash
npm run test          # All tests
npm run test:frontend # Frontend unit tests (vitest)
npm run test:backend  # Backend unit tests (pytest)
npm run test:e2e      # End-to-end (Playwright)
```

### 29. How do I build the static demo?
```bash
python scripts/export_demo.py
# Output: demo/mycelium_demo.html
```

### 30. How do I deploy with Docker?
```bash
docker build -t mycelium:demo .
docker run -p 8000:8000 mycelium:demo
```

### 31. Can I use PostgreSQL instead of SQLite?
Yes. Set `MYCELIUM_DB_URL=postgresql+asyncpg://user:pass@host/db`.
See DEPLOYMENT.md for details.

### 32. How do I add a new UI component?
Create the component in `src/frontend/src/components/`, following the
design system tokens. Add a Storybook story and accessibility tests.
See DESIGN.md for the component pattern.

### 33. What's the bundle size?
Target is < 250KB gzipped. Vite's tree shaking and code splitting keep
the bundle lean. Run `npx vite build --report` for details.

### 34. How do I contribute?
See CONTRIBUTING.md. Fork, branch, make changes with tests, open a PR.

### 35. Where is the API documentation?
FastAPI auto-generates OpenAPI docs at `/docs` (Swagger) and `/redoc`.

---

## For Admins

### 36. What are the system requirements?
- **Browser**: Chrome 90+, Firefox 90+, Edge 90+, Safari 15+
- **Node.js**: 18+ (for development)
- **Python**: 3.11+ (for backend)
- **RAM**: 512MB minimum, 2GB recommended
- **Disk**: < 100MB for the application

### 37. How do I back up data?
Data is stored in SQLite at `data/mycelium.db`. Copy this file to back up.
Content chunks are in `data/chunks/`.

### 38. Is there an admin panel?
Admin endpoints are available but disabled by default for security. Enable
with `MYCELIUM_ADMIN_ENABLED=true` (not recommended for public deployments).

### 39. How do I monitor the application?
Health endpoint at `/health` returns status and version. Structured JSON
logging to stdout. Compatible with any log aggregation tool.

### 40. How do I update?
Pull the latest code and rebuild:
```bash
git pull
cd src/frontend && npm ci && npm run build && cd ../..
pip install -r requirements.txt
```

### 41. Can I run multiple instances?
Yes. Each instance uses its own SQLite database. For shared databases,
use PostgreSQL.

### 42. What about GDPR compliance?
Mycelium stores all data locally. No personal data is transmitted to
external servers. Users control their data entirely.

### 43. How do I reset the demo data?
```bash
python scripts/seed_demo_data.py --reset
```

### 44. Can I restrict P2P access?
Yes. P2P is opt-in only. Users must explicitly click "Join Network" and
accept the consent modal. You can disable P2P entirely with
`MYCELIUM_P2P_ENABLED=false`.

### 45. What ports does it use?
- **3000**: Frontend dev server (Vite)
- **8000**: Backend API server (Uvicorn)
- **6006**: Storybook (optional)

---

Copyright (c) 2026 Zorvia Community. Licensed under ZPL v2.0.
