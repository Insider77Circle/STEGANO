"""Homoglyph substitution channel (stage-1 core table).

Replaces ASCII letters/digits with visually confusable Unicode lookalikes.
The mapping is injective (one confusable per source char) so decoding is
exact. Characters with no mapping pass through unchanged.

Enhancement 3: the core table is expanded with a curated TR39-style set.
This is a *curated subset* of Unicode TR39 confusables (the full table has
7000+ pairs and would bloat the package); each entry below is a
well-documented Cyrillic/Greek/Armenian/Latin confusable.
"""

from __future__ import annotations

# Source ASCII -> confusable lookalike. Curated subset; injective by design.
CONFUSABLES: dict[str, str] = {
    "a": "а",  # CYRILLIC SMALL LETTER A
    "c": "с",  # CYRILLIC SMALL LETTER ES
    "e": "е",  # CYRILLIC SMALL LETTER IE
    "i": "і",  # CYRILLIC SMALL LETTER BYELORUSSIAN-UKRAINIAN I
    "j": "ј",  # CYRILLIC SMALL LETTER JE
    "o": "о",  # CYRILLIC SMALL LETTER O
    "p": "р",  # CYRILLIC SMALL LETTER ER
    "s": "ѕ",  # CYRILLIC SMALL LETTER DZE
    "x": "х",  # CYRILLIC SMALL LETTER HA
    "y": "у",  # CYRILLIC SMALL LETTER U
    "A": "А",  # CYRILLIC CAPITAL LETTER A
    "B": "В",  # CYRILLIC CAPITAL LETTER VE
    "C": "С",  # CYRILLIC CAPITAL LETTER ES
    "E": "Е",  # CYRILLIC CAPITAL LETTER IE
    "H": "Н",  # CYRILLIC CAPITAL LETTER EN
    "K": "К",  # CYRILLIC CAPITAL LETTER KA
    "M": "М",  # CYRILLIC CAPITAL LETTER EM
    "O": "О",  # CYRILLIC CAPITAL LETTER O
    "P": "Р",  # CYRILLIC CAPITAL LETTER ER
    "T": "Т",  # CYRILLIC CAPITAL LETTER TE
    "X": "Х",  # CYRILLIC CAPITAL LETTER HA
    "0": "Ο",  # GREEK CAPITAL LETTER OMICRON
    "3": "З",  # CYRILLIC CAPITAL LETTER ZE
}

# Enhancement 3 — TR39-style expansion (curated subset, injective).
TR39_EXTRA: dict[str, str] = {
    "b": "в",  # CYRILLIC SMALL LETTER VE
    "d": "ԁ",  # CYRILLIC SMALL LETTER KOMI DE
    "f": "ƒ",  # LATIN SMALL LETTER F WITH HOOK
    "g": "ɡ",  # LATIN SMALL LETTER SCRIPT G
    "h": "һ",  # CYRILLIC SMALL LETTER SHHA
    "k": "κ",  # GREEK SMALL LETTER KAPPA
    "l": "ӏ",  # CYRILLIC SMALL LETTER PALOCHKA
    "m": "м",  # CYRILLIC SMALL LETTER EM
    "t": "τ",  # GREEK SMALL LETTER TAU
    "u": "υ",  # GREEK SMALL LETTER UPSILON
    "v": "ν",  # GREEK SMALL LETTER NU
    "w": "ԝ",  # CYRILLIC SMALL LETTER WE
    "z": "ᴢ",  # LATIN LETTER SMALL CAPITAL Z
    "D": "Ԁ",  # CYRILLIC CAPITAL LETTER KOMI DE
    "F": "Ϝ",  # GREEK LETTER DIGAMMA
    "G": "Ԍ",  # CYRILLIC CAPITAL LETTER KOMI GJE
    "I": "І",  # CYRILLIC CAPITAL LETTER BYELORUSSIAN-UKRAINIAN I
    "J": "Ј",  # CYRILLIC CAPITAL LETTER JE
    "N": "Ν",  # GREEK CAPITAL LETTER NU
    "Q": "Ԛ",  # CYRILLIC CAPITAL LETTER QA
    "S": "Ѕ",  # CYRILLIC CAPITAL LETTER DZE
    "U": "Ү",  # CYRILLIC CAPITAL LETTER STRAIGHT U
    "V": "Ѵ",  # CYRILLIC CAPITAL LETTER IZHITSA
    "W": "Ԝ",  # CYRILLIC CAPITAL LETTER WE
    "Y": "Υ",  # GREEK CAPITAL LETTER UPSILON
    "Z": "Ζ",  # GREEK CAPITAL LETTER ZETA
    "1": "𝟙",  # MATHEMATICAL BOLD DIGIT ONE
    "2": "Ƨ",  # LATIN CAPITAL LETTER TONE TWO
    "6": "б",  # CYRILLIC SMALL LETTER BE
    "!": "ǃ",  # LATIN LETTER RETROFLEX CLICK
    "?": "ʔ",  # LATIN LETTER GLOTTAL STOP
    ".": "。",  # IDEOGRAPHIC FULL STOP
    ",": "、",  # IDEOGRAPHIC COMMA
    ":": "ː",  # MODIFIER LETTER TRIANGULAR COLON
    ";": ";",  # GREEK QUESTION MARK
}

CONFUSABLES.update(TR39_EXTRA)

REVERSE: dict[str, str] = {v: k for k, v in CONFUSABLES.items()}
assert len(REVERSE) == len(CONFUSABLES), "confusable table must be injective"


def encode(payload: str) -> str:
    """Substitute confusables for mapped ASCII characters."""
    return "".join(CONFUSABLES.get(ch, ch) for ch in payload)

