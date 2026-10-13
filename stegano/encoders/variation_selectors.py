"""Variation-selector nibble channel.

Each payload byte is split into two nibbles; nibble *n* (0-15) maps to
U+FE00+n (VS1..VS16). Two invisible chars per byte. Decoding filters the
text to VS1..VS16 and pairs them back into bytes.
"""

from __future__ import annotations

VS_BASE = 0xFE00  # VS1
VS_CHARS = tuple(chr(VS_BASE + n) for n in range(16))
ALPHABET = frozenset(VS_CHARS)


def encode(payload: str) -> str:
    """Encode *payload* as variation-selector nibble pairs."""
    out: list[str] = []
    for byte in payload.encode("utf-8"):
        out.append(chr(VS_BASE + (byte >> 4)))
        out.append(chr(VS_BASE + (byte & 0x0F)))
    return "".join(out)

