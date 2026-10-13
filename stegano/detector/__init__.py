"""Invisible-character detector.

Range-based scan over the known steganographic code-point sets, with a
false-positive whitelist for subdivision flag emoji (enhancement 2):
England/Scotland/Wales flags are legitimate tag-block sequences and must
not trip tag detection.
"""

from __future__ import annotations

from dataclasses import dataclass

# Code-point sets per category.
ZERO_WIDTH = frozenset({0x200B, 0x200C, 0x200D, 0xFEFF})
BIDI = frozenset({0x200E, 0x200F, 0x202A, 0x202B, 0x202C, 0x202D, 0x202E,
                  0x2066, 0x2067, 0x2068, 0x2069})

# Invisible format characters (cf. cleaner-code invisible scanner):
# soft hyphen, combining grapheme joiner, Arabic letter mark,
# Mongolian vowel separator, word joiner, function application,
# invisible times / separator / plus.
FORMAT_INVISIBLE = frozenset({0x00AD, 0x034F, 0x061C, 0x180E,
                              0x2060, 0x2061, 0x2062, 0x2063, 0x2064})

# Spacing lookalikes usable for whitespace steganography (cf. cleaner-code):
# NBSP + U+2000..U+200A + narrow NBSP + medium mathematical space +
# ideographic space.
SPACING_VARIANT = frozenset({0x00A0, 0x202F, 0x205F, 0x3000} |
                            set(range(0x2000, 0x200B)))

# Private Use Areas (Glassworm-style payloads hide in PUA code points;
# cf. cleaner-code steganography scanner).
PUA_RANGES = ((0xE000, 0xF8FF), (0xF0000, 0xFFFFD), (0x100000, 0x10FFFD))

# Legitimate tag-block uses: subdivision flags = U+1F3F4 + tag letters +
# U+E007F. Whitelisted so tag detection doesn't false-positive on them.
_FLAG_SEQUENCES = (
    "🏴\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F",
    "🏴\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F",
    "🏴\U000E0067\U000E0062\U000E0077\U000E006C\U000E0073\U000E007F",
)


def _flag_spans(text: str) -> list[tuple[int, int]]:
    """Character-index spans covered by whitelisted flag sequences."""
    spans: list[tuple[int, int]] = []
    for seq in _FLAG_SEQUENCES:
        start = 0
        while True:
            i = text.find(seq, start)
            if i == -1:
                break
            spans.append((i, i + len(seq)))
            start = i + 1
    return spans


def _in_range(cp: int, lo: int, hi: int) -> bool:
    return lo <= cp <= hi


def categorize(cp: int) -> str | None:
    """Return the stego category for a code point, or None if clean."""
    if cp in ZERO_WIDTH:
        return "zero_width"
    if _in_range(cp, 0xFE00, 0xFE0F):
        return "variation_selector"
    if cp in BIDI:
        return "bidi_control"
    if _in_range(cp, 0xE0000, 0xE007F):
        return "tag_block"
    if _in_range(cp, 0xE0100, 0xE01EF):
        return "variation_selector_supplement"
    if cp in FORMAT_INVISIBLE:
        return "format_invisible"
    if cp in SPACING_VARIANT:
        return "spacing_variant"
    for lo, hi in PUA_RANGES:
        if _in_range(cp, lo, hi):
            return "private_use"
    return None


@dataclass
class Finding:
    char: str
    codepoint: int
    category: str
    index: int

    def __str__(self) -> str:  # pragma: no cover - display helper
        return f"U+{self.codepoint:04X} [{self.category}] at index {self.index}"


def scan(text: str, whitelist_flags: bool = True) -> list[Finding]:
    """Return one finding per invisible/stego code point in *text*.

    With *whitelist_flags* (default), subdivision flag emoji sequences are
    skipped so legitimate tag-block use doesn't false-positive.
    """
    spans = _flag_spans(text) if whitelist_flags else []

    def _whitelisted(i: int) -> bool:
        return any(s <= i < e for s, e in spans)

    findings: list[Finding] = []
    for i, ch in enumerate(text):
        if _whitelisted(i):
            continue
        cat = categorize(ord(ch))
        if cat is not None:
            findings.append(Finding(char=ch, codepoint=ord(ch),
                                   category=cat, index=i))
    return findings


def report(text: str) -> dict:
    """Summary report: counts per category, payload estimate, encoding guess."""
    findings = scan(text)
    by_category: dict[str, int] = {}
    for f in findings:
        by_category[f.category] = by_category.get(f.category, 0) + 1
    # Rough payload estimate: assume ~8 invisible chars per hidden byte
    # (bit channels) — a lower bound for nibble channels.
    guess = None
    if by_category:
        top = max(by_category, key=lambda k: by_category[k])
        guess = {"zero_width": "zero-width bit encoding",
                 "bidi_control": "bidi bit encoding",
                 "variation_selector": "variation-selector nibble encoding",
                 "tag_block": "tag-block nibble encoding"}.get(top)
    return {
        "total_chars": len(text),
        "invisible_chars": len(findings),
        "by_category": by_category,
        "whitelisted_flag_sequences": len(_flag_spans(text)),
        "payload_estimate_chars": len(findings) // 8 if findings else 0,
        "encoding_guess": guess,
    }
