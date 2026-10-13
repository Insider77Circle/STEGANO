"""Bidirectional-control bit channel.

Bit encoding over direction-formatting characters that render invisibly
in most contexts:
  '0' -> U+200E LEFT-TO-RIGHT MARK
  '1' -> U+200F RIGHT-TO-LEFT MARK
Terminated by U+202C POP DIRECTIONAL FORMATTING.
"""

from __future__ import annotations

ZERO = "‎"  # U+200E LRM
ONE = "‏"   # U+200F RLM
TERMINATOR = "‬"  # U+202C PDF

ALPHABET = frozenset({ZERO, ONE, TERMINATOR})


def encode(payload: str) -> str:
    """Encode *payload* as a bidi-control bit string."""
    bits = "".join(f"{byte:08b}" for byte in payload.encode("utf-8"))
    return "".join(ONE if bit == "1" else ZERO for bit in bits) + TERMINATOR

