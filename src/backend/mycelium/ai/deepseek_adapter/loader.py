# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""
Model loader — load tokenizer and weights via ``transformers`` + ``safetensors``.

This module isolates all heavy imports (``torch``, ``transformers``) behind a
single ``load_model()`` entry point so that the rest of the adapter can be
imported and tested without those dependencies.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from mycelium.ai.deepseek_adapter.config import AdapterConfig

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Type aliases (avoid top-level torch/transformers import)
# ---------------------------------------------------------------------------

ModelAndTokenizer = tuple[Any, Any]  # (PreTrainedModel, PreTrainedTokenizerBase)


# ---------------------------------------------------------------------------
# Device resolution
# ---------------------------------------------------------------------------


def resolve_device(device: str) -> str:
    """Resolve device string to a concrete device.

    Args:
        device: ``"cpu"``, ``"cuda"``, or ``"auto"``.

    Returns:
        ``"cpu"`` or ``"cuda"`` (or ``"cuda:N"`` if multiple GPUs).

    Raises:
        RuntimeError: If ``"cuda"`` is requested but unavailable.
    """
    import torch

    if device == "auto":
        if torch.cuda.is_available():
            logger.info("Auto-detected CUDA device.")
            return "cuda"
        logger.info("CUDA not available; falling back to CPU.")
        return "cpu"

    if device.startswith("cuda"):
        if not torch.cuda.is_available():
            raise RuntimeError(
                f"Device '{device}' requested but CUDA is not available. "
                "Install a CUDA-enabled PyTorch build or use device='cpu'."
            )
        return device

    return "cpu"


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------


def load_model(
    model_dir: Path,
    config: AdapterConfig,
) -> ModelAndTokenizer:
    """Load tokenizer and model weights from *model_dir*.

    Uses ``transformers.AutoModelForCausalLM`` with ``safetensors`` backend.
    Memory-saving options are applied automatically:
      - ``low_cpu_mem_usage=True``
      - ``device_map="auto"`` when CUDA is available
      - ``torch_dtype`` from model config (typically ``bfloat16``)

    Args:
        model_dir: Directory containing model files (config.json,
            tokenizer files, safetensors shards).
        config: Adapter configuration.

    Returns:
        Tuple of ``(model, tokenizer)``.

    Raises:
        ImportError: If ``torch`` or ``transformers`` are not installed.
        RuntimeError: On loading errors.
    """
    try:
        import torch  # noqa: F811
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as exc:
        raise ImportError(
            "The DeepSeek adapter requires 'torch', 'transformers', and "
            "'safetensors' packages.  Install them with:\n"
            "  pip install mycelium[ai]\n"
            f"Original error: {exc}"
        ) from exc

    device = resolve_device(config.device)
    model_path = str(model_dir)

    logger.info("Loading tokenizer from %s ...", model_dir.name)
    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        local_files_only=True,
        trust_remote_code=False,
    )

    logger.info("Loading model from %s (device=%s) ...", model_dir.name, device)

    load_kwargs: dict[str, Any] = {
        "pretrained_model_name_or_path": model_path,
        "local_files_only": True,
        "trust_remote_code": False,
        "low_cpu_mem_usage": True,
        "use_safetensors": True,
    }

    if device.startswith("cuda"):
        load_kwargs["device_map"] = "auto"
        load_kwargs["torch_dtype"] = torch.bfloat16
    else:
        # CPU: load in float32 for compatibility; bf16 can be used if
        # the CPU supports it (extension point for future optimization).
        load_kwargs["torch_dtype"] = torch.float32

    model = AutoModelForCausalLM.from_pretrained(**load_kwargs)

    if device == "cpu":
        model = model.cpu()

    model.eval()
    logger.info("Model loaded successfully (dtype=%s).", model.dtype)
    return model, tokenizer


# ---------------------------------------------------------------------------
# Resource cleanup
# ---------------------------------------------------------------------------


def unload_model(model: Any) -> None:
    """Release model from memory and free GPU cache if applicable.

    Args:
        model: The loaded model instance.
    """
    try:
        import torch

        del model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            logger.info("CUDA cache cleared.")
    except ImportError:
        del model

    logger.info("Model unloaded.")
