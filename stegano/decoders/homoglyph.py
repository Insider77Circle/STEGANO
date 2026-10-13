"""Homoglyph channel decoder (reverses the core confusables table)."""

from __future__ import annotations

from stegano.encoders.homoglyph import REVERSE


def decode(text: str) -> str:
    """Map confusables back to their ASCII sources."""
    return "".join(REVERSE.get(ch, ch) for ch in text)
