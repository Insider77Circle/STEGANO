"""Tag-block channel decoder."""

from __future__ import annotations

TAG_BASE = 0xE0000
CANCEL_TAG = ""  # U+E007F


def decode(text: str) -> str:
    """Collect tag chars (stop at CANCEL TAG), pair nibbles into bytes."""
    nibbles: list[int] = []
    for ch in text:
        cp = ord(ch)
        if ch == CANCEL_TAG:
            break
        if TAG_BASE <= cp < TAG_BASE + 0x80:
            nibbles.append(cp - TAG_BASE)
    raw = bytearray()
    for i in range(0, len(nibbles) - 1, 2):
        raw.append((nibbles[i] << 4) | nibbles[i + 1])
    return raw.decode("utf-8", errors="replace")
