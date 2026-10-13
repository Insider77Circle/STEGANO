"""Tag-block channel (U+E0000-U+E007F).

Each payload byte is split into two nibbles; nibble *n* maps to the tag
character U+E0000+n. Tag characters are invisible in every major renderer
yet are tokenized by LLMs, making this the highest-stealth text channel.
Terminated by U+E007F CANCEL TAG.

Note: subdivision flag emoji (England/Scotland/Wales) are legitimate tag
sequences — decoders treat any tag run as payload, but the *detector*
whitelists flag sequences to avoid false positives (see detector).
"""

from __future__ import annotations

TAG_BASE = 0xE0000
CANCEL_TAG = ""  # U+E007F

ALPHABET = frozenset(chr(TAG_BASE + n) for n in range(0x80)) | {CANCEL_TAG}


def encode(payload: str) -> str:
    """Encode *payload* as tag-block nibble pairs + CANCEL TAG."""
    out: list[str] = []
    for byte in payload.encode("utf-8"):
        out.append(chr(TAG_BASE + (byte >> 4)))
        out.append(chr(TAG_BASE + (byte & 0x0F)))
    out.append(CANCEL_TAG)
    return "".join(out)

