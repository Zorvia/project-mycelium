# Contributing to Project Mycelium

Thank you for your interest in contributing to Project Mycelium! This guide
will help you get started.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

### Prerequisites

- **Node.js** >= 18.0.0
- **Python** >= 3.11
- **Git**

### Development Setup

```bash
# Clone the repository
git clone https://github.com/Zorvia/project-mycelium.git
cd project-mycelium

# Install frontend dependencies
cd src/frontend && npm ci && cd ../..

# Install backend dependencies
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Seed demo data
python scripts/seed_demo_data.py

# Start development servers
npm run dev
```

## How to Contribute

### Reporting Bugs

1. Check existing issues for duplicates.
2. Open a new issue with the **Bug Report** template.
3. Include: steps to reproduce, expected behavior, actual behavior, screenshots.

### Suggesting Features

1. Open a discussion in the **Ideas** category.
2. Describe the use case and proposed solution.
3. Wait for community feedback before opening a PR.

### Pull Requests

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes with tests.
4. Ensure all tests pass:
   ```bash
   npm run test
   npm run lint
   ```
5. Add the Zorvia header to all new source files.
6. Open a Pull Request against `main`.

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(graph): add clustering algorithm for large graphs
fix(crdt): resolve merge conflict in LWW register
docs(readme): update installation steps
test(p2p): add gossip protocol convergence test
```

## Code Standards

### TypeScript/React

- Use functional components with hooks.
- Follow the design system tokens.
- All components must be keyboard-accessible.
- Add JSDoc comments for public APIs.

### Python

- Follow PEP 8 with Ruff formatting.
- Type hints required for all functions.
- Docstrings in Google style.
- Async-first where I/O is involved.

### File Headers

Every source file must include the Zorvia header:

```
/*
  Project Mycelium — Nurturing Knowledge Without the Cloud
  Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)

  Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
  See LICENSE.md for full text.

  THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
  See LICENSE.md for details and disclaimers.
*/
```

For Python, use `#` comment style.

## Review Process

1. At least one maintainer review is required.
2. CI must pass (lint, unit tests, E2E, build).
3. Accessibility concerns must be addressed.
4. Documentation must be updated if applicable.

## Community

- **Discussions**: GitHub Discussions
- **Issues**: GitHub Issues
- **License**: ZPL v2.0

Thank you for helping nurture knowledge without the cloud! 🍄
