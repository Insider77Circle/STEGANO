"""Zero-width bit channel.

Bit encoding over invisible format characters (mirrors the original
Stegano-Prompt scheme):
  '0' -> U+200B ZERO WIDTH SPACE
  '1' -> U+200C ZERO WIDTH NON-JOINER
Payload is UTF-8 bytes, 8 chars per byte, terminated by U+FEFF
(ZERO WIDTH NO-BREAK SPACE) so a decoder can stop mid-carrier.
"""

from __future__ import annotations

ZERO = "​"   # U+200B
ONE = "‌"    # U+200C
TERMINATOR = "﻿"  # U+FEFF

ALPHABET = frozenset({ZERO, ONE, TERMINATOR})


def encode(payload: str) -> str:
    """Encode *payload* as a zero-width bit string."""
    bits = "".join(f"{byte:08b}" for byte in payload.encode("utf-8"))
    return "".join(ONE if bit == "1" else ZERO for bit in bits) + TERMINATOR

