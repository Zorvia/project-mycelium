# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | Yes       |
| < 1.0   | No        |

## Reporting a Vulnerability

**Do not open a public issue for security vulnerabilities.**

Please report security vulnerabilities by emailing:

**aaryadevv8@gmail.com**

Or use GitHub's private vulnerability reporting feature on our repository.

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Impact assessment
- Suggested fix (if any)

### Response Timeline

- **Acknowledgment**: within 48 hours
- **Initial assessment**: within 5 business days
- **Fix timeline**: depends on severity (critical: 7 days, high: 14 days, medium: 30 days)

## Security Architecture

### Data at Rest

- All user content is stored locally in SQLite.
- Chunk encryption uses **AES-256-GCM** with per-seed keys.
- Keys derived via **PBKDF2-SHA256** (600,000 iterations) or **HKDF**.
- Key material never leaves the local device.

### Data in Transit (P2P)

- WebRTC DataChannels use **DTLS** encryption.
- Content chunks are encrypted before transmission.
- Peer identity verified via public key fingerprints.

### Local AI

- WebLLM runs entirely in-browser (WebGPU/WASM).
- No data is sent to external services.
- No telemetry or analytics by default.

### Web Security

- **CSP**: strict Content-Security-Policy headers.
- **XSS**: React's built-in escaping + DOMPurify for user content.
- **CSRF**: SameSite cookies + CSRF tokens on state-changing endpoints.
- **Injection**: parameterized queries via SQLAlchemy ORM.
- **Admin endpoints**: disabled by default in demo/static export.

### Dependencies

- Regular `npm audit` and `pip-audit` scans.
- Dependabot enabled for automated updates.
- Lock files committed for reproducible builds.

## Privacy

- Offline-first: no cloud dependency.
- No data leaves the device unless the user explicitly joins a P2P session.
- Consent modal required before any P2P connection.
- No cookies, trackers, or analytics.

## Disclosure Policy

We follow responsible disclosure. Security researchers who report valid
vulnerabilities will be credited in our NOTICE.md (with their permission).

---

Copyright (c) 2026 Zorvia Community. Licensed under ZPL v2.0.
