# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""
Public API — ``initialize()``, ``Adapter``, and inference methods.

This is the stable entry point for the rest of Mycelium.  All other
sub-modules are implementation details.
"""

from __future__ import annotations

import logging
import threading
from collections.abc import Generator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from mycelium.ai.deepseek_adapter.config import AdapterConfig
from mycelium.ai.deepseek_adapter.detect import detect_model_files
from mycelium.ai.deepseek_adapter.loader import load_model, resolve_device, unload_model
from mycelium.ai.deepseek_adapter.utils import (
    enforce_max_cache,
    ensure_cache_dir,
    extract_zip_atomically,
)
from mycelium.ai.deepseek_adapter.verify import run_verification

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Module-level singleton registry (for idempotent initialize)
# ---------------------------------------------------------------------------

_lock = threading.Lock()
_instances: dict[str, "Adapter"] = {}


# ---------------------------------------------------------------------------
# Adapter
# ---------------------------------------------------------------------------


@dataclass
class Adapter:
    """DeepSeek R1 Distill (Qwen-7B) inference adapter.

    Do **not** instantiate directly — use :func:`initialize` instead.

    Attributes:
        config: Frozen adapter configuration.
        model_dir: Resolved directory containing model files.
        loaded: Whether the model is loaded and ready for inference.
        device: Resolved device string (``"cpu"`` or ``"cuda"``).
        shard_hashes: SHA-256 hex digests of each shard file.
    """

    config: AdapterConfig
    model_dir: Path
    loaded: bool = False
    device: str = "cpu"
    shard_hashes: dict[str, str] = field(default_factory=dict)
    _model: Any = field(default=None, repr=False)
    _tokenizer: Any = field(default=None, repr=False)
    _shard_names: list[str] = field(default_factory=list, repr=False)

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def status(self) -> dict[str, Any]:
        """Return canonical adapter status dict.

        Returns:
            Dict with keys:

            - ``loaded`` (bool): model ready for inference.
            - ``device`` (str): ``"cpu"`` or ``"cuda"``.
            - ``files`` (list[str]): absolute paths of shard files.
            - ``shards`` (int): number of shard files.
            - ``sha256`` (dict): filename → hex digest.
            - ``cache_dir`` (str): resolved cache directory.
        """
        files = [str(self.model_dir / s) for s in self._shard_names]
        return {
            "loaded": self.loaded,
            "device": self.device,
            "files": files,
            "shards": len(self._shard_names),
            "sha256": dict(self.shard_hashes),
            "cache_dir": str(self.config.resolved_cache_dir),
        }

    # ------------------------------------------------------------------
    # Inference — synchronous
    # ------------------------------------------------------------------

    def predict(
        self,
        prompt: str,
        *,
        max_tokens: int = 256,
        temperature: float = 0.0,
        top_p: float = 0.95,
    ) -> str:
        """Generate a completion for *prompt* (synchronous, blocking).

        Args:
            prompt: User prompt text.
            max_tokens: Maximum new tokens to generate.
            temperature: Sampling temperature.  ``0.0`` ≈ greedy.
            top_p: Nucleus sampling threshold.

        Returns:
            Generated text string.

        Raises:
            RuntimeError: If the model is not loaded.
        """
        self._ensure_loaded()

        import torch

        messages = [{"role": "user", "content": prompt}]
        input_text = self._tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs = self._tokenizer(input_text, return_tensors="pt")
        input_ids = inputs["input_ids"].to(self._model.device)
        attention_mask = inputs.get("attention_mask")
        if attention_mask is not None:
            attention_mask = attention_mask.to(self._model.device)

        gen_kwargs: dict[str, Any] = {
            "input_ids": input_ids,
            "max_new_tokens": max_tokens,
            "do_sample": temperature > 0,
            "pad_token_id": self._tokenizer.eos_token_id,
        }
        if attention_mask is not None:
            gen_kwargs["attention_mask"] = attention_mask
        if temperature > 0:
            gen_kwargs["temperature"] = temperature
            gen_kwargs["top_p"] = top_p

        with torch.no_grad():
            outputs = self._model.generate(**gen_kwargs)

        # Decode only the newly generated tokens
        new_tokens = outputs[0][input_ids.shape[1]:]
        result = self._tokenizer.decode(new_tokens, skip_special_tokens=True)
        return result.strip()

    # ------------------------------------------------------------------
    # Inference — streaming generator
    # ------------------------------------------------------------------

    def generate_stream(
        self,
        prompt: str,
        *,
        max_tokens: int = 256,
        temperature: float = 0.0,
        top_p: float = 0.95,
    ) -> Generator[str, None, None]:
        """Generate tokens one-at-a-time as a streaming generator.

        This is **opt-in** — use :meth:`predict` for simpler use cases.
        Each yielded string is a single decoded token (or sub-word piece).

        Trade-offs vs ``predict()``:
          - Lower time-to-first-token.
          - Allows incremental display in UIs.
          - Slightly higher overhead per token due to repeated forward passes.

        Args:
            prompt: User prompt text.
            max_tokens: Maximum new tokens to generate.
            temperature: Sampling temperature.
            top_p: Nucleus sampling threshold.

        Yields:
            Individual decoded token strings.

        Raises:
            RuntimeError: If the model is not loaded.
        """
        self._ensure_loaded()

        import torch

        messages = [{"role": "user", "content": prompt}]
        input_text = self._tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs = self._tokenizer(input_text, return_tensors="pt")
        input_ids = inputs["input_ids"].to(self._model.device)
        attention_mask = inputs.get("attention_mask")
        if attention_mask is not None:
            attention_mask = attention_mask.to(self._model.device)

        eos_id = self._tokenizer.eos_token_id
        past_key_values = None
        generated_ids = input_ids

        for _ in range(max_tokens):
            with torch.no_grad():
                if past_key_values is not None:
                    model_inputs = {
                        "input_ids": generated_ids[:, -1:],
                        "past_key_values": past_key_values,
                        "use_cache": True,
                    }
                    if attention_mask is not None:
                        model_inputs["attention_mask"] = attention_mask
                else:
                    model_inputs = {
                        "input_ids": generated_ids,
                        "use_cache": True,
                    }
                    if attention_mask is not None:
                        model_inputs["attention_mask"] = attention_mask

                outputs = self._model(**model_inputs)

            logits = outputs.logits[:, -1, :]
            past_key_values = outputs.past_key_values

            if temperature > 0:
                logits = logits / temperature
                probs = torch.softmax(logits, dim=-1)
                # Top-p filtering
                sorted_probs, sorted_indices = torch.sort(probs, descending=True)
                cumulative = torch.cumsum(sorted_probs, dim=-1)
                mask = cumulative - sorted_probs > top_p
                sorted_probs[mask] = 0.0
                sorted_probs /= sorted_probs.sum(dim=-1, keepdim=True)
                next_token = sorted_indices[
                    0, torch.multinomial(sorted_probs[0], 1)
                ].unsqueeze(0)
            else:
                next_token = logits.argmax(dim=-1, keepdim=True)

            if next_token.item() == eos_id:
                break

            generated_ids = torch.cat([generated_ids, next_token], dim=-1)
            if attention_mask is not None:
                attention_mask = torch.cat(
                    [attention_mask, torch.ones_like(next_token)], dim=-1
                )

            token_str = self._tokenizer.decode(
                next_token[0], skip_special_tokens=True
            )
            if token_str:
                yield token_str

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def shutdown(self) -> None:
        """Release model and free GPU memory.

        After shutdown, you must call :func:`initialize` again to use the
        adapter.  The singleton registry is cleared for this source path.
        """
        if self._model is not None:
            unload_model(self._model)
            self._model = None
            self._tokenizer = None
            self.loaded = False
            self.device = "cpu"
            logger.info("Adapter shut down.")

        # Remove from singleton registry
        key = str(self.config.resolved_model_source)
        with _lock:
            _instances.pop(key, None)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _ensure_loaded(self) -> None:
        if not self.loaded or self._model is None:
            raise RuntimeError(
                "Model is not loaded. Call initialize() first, "
                "or check adapter.status()['loaded']."
            )


# ---------------------------------------------------------------------------
# Public factory
# ---------------------------------------------------------------------------


def initialize(
    model_source: str | Path,
    *,
    cache_dir: str | None = None,
    device: str = "auto",
    checksums_file: str | None = None,
    max_cache_bytes: int | None = None,
    min_free_bytes: int | None = None,
) -> Adapter:
    """Initialize the DeepSeek adapter (idempotent).

    If an adapter for the same *model_source* is already initialized, the
    existing instance is returned.

    Args:
        model_source: Path to directory or ``.zip`` containing model files.
        cache_dir: Override cache directory (default ``~/.mycelium/ai_cache``).
        device: ``"cpu"``, ``"cuda"``, or ``"auto"`` (default).
        checksums_file: Optional path to JSON checksums file.
        max_cache_bytes: Override maximum cache size.
        min_free_bytes: Override minimum free-disk threshold.

    Returns:
        A ready-to-use :class:`Adapter` instance.

    Raises:
        FileNotFoundError: If required model files are missing.
        ValueError: On checksum mismatch.
        OSError: On insufficient disk space.
        ImportError: If AI dependencies are not installed.
    """
    source_path = Path(model_source).expanduser().resolve()
    key = str(source_path)

    with _lock:
        if key in _instances and _instances[key].loaded:
            logger.info("Returning existing adapter for %s", source_path.name)
            return _instances[key]

    # Build config
    kwargs: dict[str, Any] = {"model_source": str(source_path)}
    if cache_dir is not None:
        kwargs["cache_dir"] = cache_dir
    if checksums_file is not None:
        kwargs["checksums_file"] = checksums_file
    if max_cache_bytes is not None:
        kwargs["max_cache_bytes"] = max_cache_bytes
    if min_free_bytes is not None:
        kwargs["min_free_bytes"] = min_free_bytes
    kwargs["device"] = device

    config = AdapterConfig(**kwargs)

    # 1. Detect
    logger.info("Detecting model files ...")
    detection = detect_model_files(config)
    detection.raise_on_error()

    # 2. Resolve model directory (extract zip if needed)
    if detection.is_zip:
        cache = ensure_cache_dir(config.resolved_cache_dir)
        all_files = (
            detection.shards
            + detection.config_files
            + detection.tokenizer_files
        )
        model_dir = extract_zip_atomically(
            source_path, cache, required_names=all_files
        )
    else:
        model_dir = source_path

    # 3. Verify
    logger.info("Running verification ...")
    hashes = run_verification(
        config, model_dir, detection.shards
    )

    # 4. Cache enforcement
    enforce_max_cache(config.resolved_cache_dir, config.max_cache_bytes)

    # 5. Load model
    logger.info("Loading model ...")
    resolved_device = resolve_device(config.device)
    model, tokenizer = load_model(model_dir, config)

    # 6. Build adapter
    adapter = Adapter(
        config=config,
        model_dir=model_dir,
        loaded=True,
        device=resolved_device,
        shard_hashes=hashes,
        _model=model,
        _tokenizer=tokenizer,
        _shard_names=list(detection.shards),
    )

    with _lock:
        _instances[key] = adapter

    logger.info("Adapter initialized successfully (device=%s).", resolved_device)
    return adapter
