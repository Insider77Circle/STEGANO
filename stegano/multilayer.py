"""Multi-layer payloads (enhancement 5).

Layer 1 (visible-ish): acrostic — the first letters of consecutive words
spell the payload. Stripping invisible characters leaves this intact.
Layer 2 (invisible): a tag-block encoding of the payload woven through the
same text. Stripping the acrostic words leaves the tag channel intact.

Either layer surviving is enough to recover the message.
"""

from __future__ import annotations

from stegano import channels

# Word bank for acrostic generation: letter -> word starting with it.
_WORDS: dict[str, str] = {
    "a": "amber", "b": "bright", "c": "clear", "d": "daily", "e": "every",
    "f": "fresh", "g": "great", "h": "happy", "i": "inner", "j": "joint",
    "k": "kind", "l": "light", "m": "morning", "n": "noble", "o": "open",
    "p": "peaceful", "q": "quiet", "r": "rapid", "s": "silent", "t": "timely",
    "u": "united", "v": "vivid", "w": "warm", "x": "xenial", "y": "young",
    "z": "zealous",
    "0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
    "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine",
    " ": "—",
}


def encode_acrostic(payload: str) -> str:
    """Encode *payload* as an acrostic sentence (first letters spell it)."""
    words: list[str] = []
    for ch in payload.lower():
        if ch not in _WORDS:
            raise ValueError(f"acrostic has no word for {ch!r}")
        words.append(_WORDS[ch])
    # Capitalize first word for naturalness.
    words[0] = words[0].capitalize()
    return " ".join(words) + "."


def decode_acrostic(text: str) -> str:
    """Recover the payload from first letters of words."""
    letters: list[str] = []
    for word in text.split():
        w = word.strip(".,!?;:")
        if w == "—":  # the space token
            letters.append(" ")
            continue
        first = w[0].lower()
        if first in _WORDS:
            letters.append(first)
    return "".join(letters).upper()


def encode_layered(payload: str) -> str:
    """Acrostic text carrying an invisible tag-block copy of the payload."""
    acrostic = encode_acrostic(payload)
    tag = channels.get("tag_block")
    return channels.embed(acrostic, tag.encode(payload), position="end")


def decode_layered(text: str) -> dict[str, str]:
    """Recover both layers: {'acrostic': ..., 'tag_block': ...}."""
    tag = channels.get("tag_block")
    return {
        "acrostic": decode_acrostic(text),
        "tag_block": tag.decode(text),
    }
