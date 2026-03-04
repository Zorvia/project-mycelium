# Deployment Guide

## TL;DR

Project Mycelium supports static hosting (Netlify, Vercel, Cloudflare Pages)
for the frontend and container hosting (Render, Docker) for the full-stack app.

---

## Quick Reference

| Platform | Type | Cost | Setup Time |
|----------|------|------|------------|
| Netlify | Static | Free | 5 min |
| Vercel | Static | Free | 5 min |
| Cloudflare Pages | Static | Free | 5 min |
| Render | Full-stack | Free tier | 10 min |
| Docker | Self-hosted | Free | 5 min |

---

## 1. Static Export (Frontend Only)

Build the static demo that runs entirely offline:

```bash
# Build the frontend
cd src/frontend && npm run build

# Or generate the single-file demo
python scripts/export_demo.py
# Output: demo/mycelium_demo.html
```

### Netlify

1. Create a new site on [netlify.com](https://netlify.com).
2. Connect your GitHub repository.
3. Configure build settings:

**netlify.toml** (included in repo):

```toml
[build]
  base = "src/frontend"
  command = "npm run build"
  publish = "dist"

[build.environment]
  NODE_VERSION = "20"

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Content-Security-Policy = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; connect-src 'self' ws: wss:; worker-src 'self' blob:"
```

### Vercel

1. Import the repository on [vercel.com](https://vercel.com).
2. Set the root directory to `src/frontend`.
3. Framework preset: **Vite**.

**vercel.json** (included in repo):

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-Content-Type-Options", "value": "nosniff" }
      ]
    }
  ]
}
```

### Cloudflare Pages

1. Create a new project on [pages.cloudflare.com](https://pages.cloudflare.com).
2. Connect your GitHub repository.
3. Build settings:
   - **Build command**: `cd src/frontend && npm run build`
   - **Build output**: `src/frontend/dist`
   - **Node version**: `20`

---

## 2. Full-Stack Deployment

### Render

1. Create a new **Web Service** on [render.com](https://render.com).
2. Connect your GitHub repository.
3. Configure:
   - **Environment**: Docker
   - **Docker Command**: (auto-detected from Dockerfile)
   - **Port**: 8000

**Environment Variables:**

```
MYCELIUM_ENV=production
MYCELIUM_DB_URL=sqlite:///data/mycelium.db
MYCELIUM_SECRET_KEY=<generate-a-random-key>
```

### Docker (Self-Hosted)

```bash
# Build
docker build -t mycelium:demo .

# Run
docker run -d \
  --name mycelium \
  -p 8000:8000 \
  -v mycelium-data:/app/data \
  mycelium:demo

# Verify
curl http://localhost:8000/health
# → {"status":"ok"}
```

### Docker Compose

```bash
docker compose up -d
```

---

## 3. Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MYCELIUM_ENV` | No | `development` | Environment mode |
| `MYCELIUM_DB_URL` | No | `sqlite:///data/mycelium.db` | Database URL |
| `MYCELIUM_SECRET_KEY` | Prod | (generated) | Secret for CSRF tokens |
| `MYCELIUM_CORS_ORIGINS` | No | `http://localhost:3000` | CORS allowed origins |
| `MYCELIUM_LOG_LEVEL` | No | `info` | Logging level |

---

## 4. Health Checks

All deployments expose a health endpoint:

```
GET /health → {"status": "ok", "version": "1.0.0"}
```

---

## 5. SSL/TLS

- **Netlify/Vercel/Cloudflare**: automatic HTTPS.
- **Render**: automatic HTTPS.
- **Docker self-hosted**: use a reverse proxy (Caddy, nginx) with Let's Encrypt.

---

Copyright (c) 2026 Zorvia Community. Licensed under ZPL v2.0.
