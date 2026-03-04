# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)

# ──────────────────────────────────────────────
# Stage 1: Frontend Build
# ──────────────────────────────────────────────
FROM node:20-alpine AS frontend-build
WORKDIR /app
COPY src/frontend/package.json src/frontend/package-lock.json* ./
RUN npm ci --prefer-offline
COPY src/frontend/ .
RUN npm run build

# ──────────────────────────────────────────────
# Stage 2: Backend Runtime
# ──────────────────────────────────────────────
FROM python:3.12-slim AS runtime

LABEL maintainer="Zorvia Community <https://github.com/Zorvia>"
LABEL description="Project Mycelium — Nurturing Knowledge Without the Cloud"
LABEL license="ZPL-2.0"

# Security: run as non-root user
RUN groupadd -r mycelium && useradd -r -g mycelium -m mycelium

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY src/backend/ src/backend/
COPY scripts/ scripts/
COPY data/ data/

# Copy built frontend
COPY --from=frontend-build /app/dist/ src/frontend/dist/

# Seed demo data
RUN python scripts/seed_demo_data.py

# Switch to non-root user
USER mycelium

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run the application
CMD ["python", "-m", "uvicorn", "mycelium.main:app", "--host", "0.0.0.0", "--port", "8000"]
