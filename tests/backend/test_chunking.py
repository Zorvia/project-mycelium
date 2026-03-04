# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""Tests for content-addressing / chunking / encryption."""

from __future__ import annotations

import os
import pytest
from mycelium.chunking import (
    compute_cid,
    chunk_data,
    create_cid_manifest,
    derive_key,
    encrypt_chunk,
    decrypt_chunk,
)


class TestComputeCid:
    """SHA-256 content identifier tests."""

    def test_deterministic(self) -> None:
        data = b"hello mycelium"
        assert compute_cid(data) == compute_cid(data)

    def test_hex_length(self) -> None:
        cid = compute_cid(b"test")
        assert len(cid) == 64  # SHA-256 hex

    def test_different_data_different_cid(self) -> None:
        assert compute_cid(b"a") != compute_cid(b"b")

    def test_empty_data(self) -> None:
        cid = compute_cid(b"")
        assert isinstance(cid, str) and len(cid) == 64


class TestChunkData:
    """Fixed-size chunking tests."""

    def test_small_data_single_chunk(self) -> None:
        chunks = chunk_data(b"small")
        assert len(chunks) == 1
        assert chunks[0] == b"small"

    def test_exact_boundary(self) -> None:
        data = b"x" * (256 * 1024)
        chunks = chunk_data(data, chunk_size=256 * 1024)
        assert len(chunks) == 1

    def test_multiple_chunks(self) -> None:
        data = b"y" * (256 * 1024 + 1)
        chunks = chunk_data(data, chunk_size=256 * 1024)
        assert len(chunks) == 2
        assert b"".join(chunks) == data

    def test_reassembly(self) -> None:
        data = os.urandom(1_000_000)
        chunks = chunk_data(data, chunk_size=256 * 1024)
        assert b"".join(chunks) == data


class TestCidManifest:
    """Manifest generation tests."""

    def test_manifest_has_correct_length(self) -> None:
        data = b"manifest test data " * 1000
        manifest = create_cid_manifest(data, chunk_size=256)
        chunks = chunk_data(data, chunk_size=256)
        assert len(manifest) == len(chunks)

    def test_manifest_entries_are_unique(self) -> None:
        data = b"a" * 100 + b"b" * 100
        manifest = create_cid_manifest(data, chunk_size=100)
        # First two chunks are different, so CIDs should differ
        assert manifest[0] != manifest[1]


class TestDeriveKey:
    """PBKDF2 key derivation tests."""

    def test_key_length(self) -> None:
        key = derive_key("password", b"salt1234salt1234")
        assert len(key) == 32  # 256 bits

    def test_deterministic(self) -> None:
        salt = b"deterministic-sa"
        k1 = derive_key("pass", salt)
        k2 = derive_key("pass", salt)
        assert k1 == k2

    def test_different_passwords(self) -> None:
        salt = b"abcdefghijklmnop"
        k1 = derive_key("alpha", salt)
        k2 = derive_key("beta", salt)
        assert k1 != k2


class TestEncryption:
    """AES-256-GCM encryption round-trip tests."""

    def test_round_trip(self) -> None:
        key = derive_key("secret", b"0123456789abcdef")
        plaintext = b"Project Mycelium — private data"
        ct, nonce = encrypt_chunk(plaintext, key)
        recovered = decrypt_chunk(ct, key, nonce)
        assert recovered == plaintext

    def test_ciphertext_differs(self) -> None:
        key = derive_key("key", b"saltsaltsaltsalt")
        pt = b"same data"
        ct1, _ = encrypt_chunk(pt, key)
        ct2, _ = encrypt_chunk(pt, key)
        # Different random nonces → different ciphertext
        assert ct1 != ct2

    def test_wrong_key_fails(self) -> None:
        key1 = derive_key("right", b"saltsaltsaltsalt")
        key2 = derive_key("wrong", b"saltsaltsaltsalt")
        ct, nonce = encrypt_chunk(b"secret", key1)
        with pytest.raises(Exception):
            decrypt_chunk(ct, key2, nonce)

    def test_empty_plaintext(self) -> None:
        key = derive_key("k", b"saltsaltsaltsalt")
        ct, nonce = encrypt_chunk(b"", key)
        assert decrypt_chunk(ct, key, nonce) == b""
