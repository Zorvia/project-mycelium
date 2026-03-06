# DeepSeek R1 Distill (Qwen-7B) Adapter

Local, offline inference adapter for **DeepSeek-R1-Distill-Qwen-7B** inside Project Mycelium.

> **No network access** is required or performed at runtime.  All operations are local-first.

---

## Required Model Files

Place the following files in a single directory (or `.zip` archive):

| File | Size (approx.) | Required |
|------|----------------|----------|
| `model-00001-of-000002.safetensors` | ~9.9 GB | **Yes** |
| `model-00002-of-000002.safetensors` | ~4.3 GB | **Yes** |
| `config.json` | ~0.5 KB | **Yes** |
| `tokenizer.json` | ~7 MB | **Yes** (at least one tokenizer file) |
| `tokenizer_config.json` | ~2 KB | Recommended |
| `generation_config.json` | ~0.2 KB | Optional |

### Placement

Place files inside the project tree (gitignored) or any local path:

```
Project Mycelium/
├── DeepSeek-R1-Distill-Qwen-7B/    ← place model files here
│   ├── model-00001-of-000002.safetensors
│   ├── model-00002-of-000002.safetensors
│   ├── config.json
│   ├── tokenizer.json
│   └── tokenizer_config.json
└── src/
    └── backend/
        └── mycelium/
            └── ai/
                └── deepseek_adapter/
```

> **Security:** Model weight files (`.safetensors`) are excluded from git via `.gitignore`.
> Never commit them to version control.

---

## Installation

Install the AI optional dependencies:

```bash
pip install -e ".[ai]"
```

This installs `torch`, `transformers`, `safetensors`, and `accelerate`.

---

## Quick Start

```python
from mycelium.ai.deepseek_adapter import initialize

# Initialize (idempotent — returns existing adapter if already loaded)
adapter = initialize("path/to/DeepSeek-R1-Distill-Qwen-7B")

# Check status
print(adapter.status())
# {
#   "loaded": True,
#   "device": "cuda",
#   "files": [".../model-00001-of-000002.safetensors", ...],
#   "shards": 2,
#   "sha256": {"model-00001-of-000002.safetensors": "abc...", ...},
#   "cache_dir": "~/.mycelium/ai_cache"
# }

# Synchronous inference
result = adapter.predict("Explain knowledge graphs.", max_tokens=128)
print(result)

# Streaming inference (opt-in)
for token in adapter.generate_stream("Hello!", max_tokens=64):
    print(token, end="", flush=True)

# Release resources
adapter.shutdown()
```

---

## API Reference

### `initialize(model_source, *, cache_dir=None, device="auto", ...)`

Factory function — returns an `Adapter` instance.  Idempotent: repeated calls
with the same `model_source` return the existing adapter.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model_source` | `str \| Path` | — | Path to model directory or `.zip` |
| `cache_dir` | `str \| None` | `~/.mycelium/ai_cache` | Cache directory |
| `device` | `str` | `"auto"` | `"cpu"`, `"cuda"`, or `"auto"` |
| `checksums_file` | `str \| None` | `None` | Path to SHA-256 checksums JSON |
| `max_cache_bytes` | `int \| None` | 32 GB | Maximum cache size |
| `min_free_bytes` | `int \| None` | 1 GB | Minimum free disk space |

### `Adapter.predict(prompt, *, max_tokens=256, temperature=0.0, top_p=0.95)`

Synchronous text generation.  Returns the generated string.

### `Adapter.generate_stream(prompt, *, max_tokens=256, temperature=0.0, top_p=0.95)`

Generator yielding individual tokens.  Opt-in streaming alternative to `predict()`.

**Trade-offs:**
- Lower time-to-first-token
- Suitable for incremental UI display
- Slightly higher per-token overhead

### `Adapter.status()`

Returns a dict with: `loaded`, `device`, `files`, `shards`, `sha256`, `cache_dir`.

### `Adapter.shutdown()`

Releases model from memory, clears GPU cache.  After shutdown, call `initialize()` again.

---

## Verification

### SHA-256 Checksums

The adapter computes SHA-256 for each shard using streaming I/O (no full-file RAM load).

If a `checksums_file` is provided, hashes are compared automatically.  On mismatch,
a clear error with expected vs actual hex and remediation steps is raised.

Without a checksums file, computed hashes are logged for manual verification:

```bash
python -c "
from mycelium.ai.deepseek_adapter import initialize
a = initialize('path/to/model')
for name, digest in a.status()['sha256'].items():
    print(f'{digest}  {name}')
"
```

### Disk Space

Before any extraction (zip sources), the adapter checks free disk space against
`min_free_bytes`.  If insufficient, it raises `OSError` with required and available
byte counts.

---

## Safe File Handling Checklist

When moving or copying large model files:

1. **Copy** files to the destination (do not move yet)
2. **Verify** SHA-256 matches at the destination
3. **Delete** the source copy only after verification
4. Never create more than one extra copy at a time
5. Use the adapter's built-in verification to confirm integrity

---

## Configuration

See [`config.yaml`](config.yaml) for all available keys.  Values can be set via:

1. Keyword arguments to `initialize()` (highest priority)
2. Environment variables (`MYCELIUM_AI_MODEL_SOURCE`, `MYCELIUM_AI_CACHE_DIR`, `MYCELIUM_AI_DEVICE`)
3. Defaults in `config.py`

---

## Testing

### Unit Tests (no model files needed)

```bash
pytest tests/backend/deepseek_adapter/ --ignore=tests/backend/deepseek_adapter/test_integration.py -v
```

### Integration Tests (require model files)

```bash
# Windows
set MYCELIUM_MODEL_PATH=C:\Users\Laptop\DeepSeek-R1-Distill-Qwen-7B
pytest tests/backend/deepseek_adapter/test_integration.py -v

# Linux/macOS
MYCELIUM_MODEL_PATH=/path/to/model pytest tests/backend/deepseek_adapter/test_integration.py -v
```

---

## Architecture

```
mycelium/ai/deepseek_adapter/
├── __init__.py      # Public exports: initialize, Adapter
├── api.py           # Adapter class, initialize() factory
├── config.py        # AdapterConfig dataclass, constants
├── config.yaml      # Configuration template
├── detect.py        # Model file detection (dir and zip)
├── loader.py        # torch/transformers model loading
├── utils.py         # Atomic extraction, cache management
├── verify.py        # SHA-256 streaming hashes, disk checks
└── README.md        # This file
```
