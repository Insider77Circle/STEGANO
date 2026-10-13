"""Variation-selector channel decoder."""

from __future__ import annotations

VS_BASE = 0xFE00


def decode(text: str) -> str:
    """Filter to VS1..VS16, pair nibbles back into bytes."""
    nibbles = [ord(ch) - VS_BASE for ch in text if VS_BASE <= ord(ch) <= VS_BASE + 15]
    raw = bytearray()
    for i in range(0, len(nibbles) - 1, 2):
        raw.append((nibbles[i] << 4) | nibbles[i + 1])
    return raw.decode("utf-8", errors="replace")
