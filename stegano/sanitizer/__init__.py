"""Sanitizer — invisible-character handling policies (enhancement 8).

Two policies:
  "strip" — remove invisible characters, return clean text.
  "block" — raise :class:`BlockedInput` if any invisible content is found.

Callers choose per context: e.g. strip tool results (keep the pipeline
flowing) but block direct user input (fail closed).
"""

from __future__ import annotations

from stegano.detector import categorize, scan

# Categories the stripper removes.
STRIP_CATEGORIES = frozenset({
    "zero_width",
    "variation_selector",
    "variation_selector_supplement",
    "bidi_control",
    "tag_block",
})

POLICIES = ("strip", "block")


class BlockedInput(Exception):
    """Raised by the "block" policy when hidden content is detected."""


def strip(text: str, categories: frozenset[str] | None = None) -> str:
    """Remove invisible chars in *categories* (default: all known)."""
    cats = STRIP_CATEGORIES if categories is None else categories
    return "".join(ch for ch in text if categorize(ord(ch)) not in cats)


def sanitize(text: str, policy: str = "strip",
             categories: frozenset[str] | None = None) -> str:
    """Apply *policy* to *text*.

    - "strip": return text with invisible characters removed.
    - "block": return text unchanged if clean, else raise BlockedInput.
    """
    if policy not in POLICIES:
        raise ValueError(f"unknown policy {policy!r}; expected one of {POLICIES}")
    findings = scan(text)
    if not findings:
        return text
    if policy == "strip":
        return strip(text, categories)
    raise BlockedInput(
        f"blocked: {len(findings)} invisible character(s) detected "
        f"({', '.join(sorted({f.category for f in findings}))})"
    )


def is_clean(text: str) -> bool:
    """True when the detector finds no hidden content."""
    return not scan(text)
