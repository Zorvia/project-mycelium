# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""Content-addressed storage: chunking, hashing, and encryption."""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


CHUNK_SIZE = 256 * 1024  # 256 KB
PBKDF2_ITERATIONS = 600_000
AES_KEY_LENGTH = 32  # 256 bits
NONCE_LENGTH = 12  # 96 bits for GCM


@dataclass(frozen=True)
class ContentChunk:
    """A content-addressed chunk of data."""

    cid: str
    data: bytes
    size: int
    index: int


@dataclass(frozen=True)
class EncryptedChunk:
    """An encrypted content chunk."""

    cid: str
    ciphertext: bytes
    nonce: bytes
    size: int
    index: int


def compute_cid(data: bytes) -> str:
    """Compute the Content Identifier (SHA-256 hex digest) for data."""
    return hashlib.sha256(data).hexdigest()


def chunk_data(data: bytes, chunk_size: int = CHUNK_SIZE) -> list[ContentChunk]:
    """Split data into content-addressed chunks.

    Args:
        data: Raw bytes to chunk.
        chunk_size: Maximum size of each chunk in bytes.

    Returns:
        List of ContentChunk objects with CIDs.
    """
    chunks: list[ContentChunk] = []
    for i in range(0, len(data), chunk_size):
        chunk_bytes = data[i : i + chunk_size]
        cid = compute_cid(chunk_bytes)
        chunks.append(
            ContentChunk(
                cid=cid,
                data=chunk_bytes,
                size=len(chunk_bytes),
                index=len(chunks),
            )
        )
    return chunks


def create_cid_manifest(chunks: list[ContentChunk]) -> dict:
    """Create a deterministic CID manifest for a set of chunks.

    Returns:
        Dictionary with root CID and chunk CIDs.
    """
    chunk_cids = [c.cid for c in chunks]
    manifest_data = "|".join(chunk_cids).encode("utf-8")
    root_cid = compute_cid(manifest_data)
    return {
        "root_cid": root_cid,
        "chunks": [
            {"cid": c.cid, "size": c.size, "index": c.index} for c in chunks
        ],
        "total_size": sum(c.size for c in chunks),
        "chunk_count": len(chunks),
    }


def derive_key(seed: str, salt: bytes | None = None) -> tuple[bytes, bytes]:
    """Derive an AES-256 key from a seed using PBKDF2.

    Args:
        seed: Passphrase or seed string.
        salt: Optional salt bytes; generated if not provided.

    Returns:
        Tuple of (key, salt).
    """
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=AES_KEY_LENGTH,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    key = kdf.derive(seed.encode("utf-8"))
    return key, salt


def encrypt_chunk(chunk: ContentChunk, key: bytes) -> EncryptedChunk:
    """Encrypt a content chunk with AES-256-GCM.

    Args:
        chunk: The plaintext chunk.
        key: AES-256 key (32 bytes).

    Returns:
        EncryptedChunk with ciphertext and nonce.
    """
    nonce = os.urandom(NONCE_LENGTH)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, chunk.data, None)
    encrypted_cid = compute_cid(ciphertext)
    return EncryptedChunk(
        cid=encrypted_cid,
        ciphertext=ciphertext,
        nonce=nonce,
        size=len(ciphertext),
        index=chunk.index,
    )


def decrypt_chunk(encrypted: EncryptedChunk, key: bytes) -> bytes:
    """Decrypt an AES-256-GCM encrypted chunk.

    Args:
        encrypted: The encrypted chunk.
        key: AES-256 key (32 bytes).

    Returns:
        Decrypted plaintext bytes.
    """
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(encrypted.nonce, encrypted.ciphertext, None)
