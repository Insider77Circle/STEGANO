"""Zero-width channel decoder."""

from __future__ import annotations

ZERO = "​"   # U+200B
ONE = "‌"    # U+200C
TERMINATOR = "﻿"  # U+FEFF


def decode(text: str) -> str:
    """Extract zero-width bits; stop at the first U+FEFF terminator."""
    bits: list[str] = []
    for ch in text:
        if ch == TERMINATOR:
            break
        if ch == ZERO:
            bits.append("0")
        elif ch == ONE:
            bits.append("1")
    raw = bytearray()
    bitstr = "".join(bits)
    for i in range(0, len(bitstr) - 7, 8):
        raw.append(int(bitstr[i:i + 8], 2))
    return raw.decode("utf-8", errors="replace")
