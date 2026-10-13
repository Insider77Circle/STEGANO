"""Tokenizer-survival predictor — EXPERIMENTAL (enhancement 10).

**Research-grade heuristic, not a measurement.** Estimates whether a
payload's invisible characters would survive common tokenizer pipelines
before reaching a model. "Survival" here means the characters are still
present (as tokens) after tokenization — a prerequisite for the model to
"see" the hidden payload.

Heuristic basis (documented, not measured in this repo):
- ``raw``: no preprocessing — everything survives (1.0).
- ``tiktoken`` (GPT-style BPE): format characters (Cf) are generally
  encoded as standalone tokens and survive; astral-plane tag characters
  are UTF-8 byte-split then BPE-merged, surviving as tokens. Homoglyphs
  are ordinary letters and always survive.
- ``sentencepiece+nfkc``: SentencePiece pipelines commonly apply NFKC
  normalization first. NFKC leaves most format chars intact, but many
  production pipelines additionally strip Unicode category Cf — hence the
  discount. Tag-block (astral) characters are less commonly stripped.
- ``aggressive``: a sanitizing pipeline that strips all format/default-
  ignorable code points — near-total removal.

Use this as a pre-flight *estimate* only. Real survival must be measured
against the actual tokenizer + preprocessing stack.
"""

from __future__ import annotations

EXPERIMENTAL = True

# category -> pipeline -> estimated survival probability (heuristic)
_SURVIVAL: dict[str, dict[str, float]] = {
    "zero_width":               {"raw": 1.0, "tiktoken": 0.95,
                                 "sentencepiece+nfkc": 0.50, "aggressive": 0.05},
    "variation_selector":       {"raw": 1.0, "tiktoken": 0.95,
                                 "sentencepiece+nfkc": 0.50, "aggressive": 0.05},
    "bidi_control":             {"raw": 1.0, "tiktoken": 0.90,
                                 "sentencepiece+nfkc": 0.45, "aggressive": 0.05},
    "tag_block":                {"raw": 1.0, "tiktoken": 0.90,
                                 "sentencepiece+nfkc": 0.70, "aggressive": 0.10},
    "variation_selector_supplement": {"raw": 1.0, "tiktoken": 0.90,
                                 "sentencepiece+nfkc": 0.50, "aggressive": 0.05},
    "format_invisible":           {"raw": 1.0, "tiktoken": 0.95,
                                 "sentencepiece+nfkc": 0.50, "aggressive": 0.05},
    "spacing_variant":            {"raw": 1.0, "tiktoken": 1.0,
                                 "sentencepiece+nfkc": 0.90, "aggressive": 0.30},
    "private_use":                {"raw": 1.0, "tiktoken": 0.90,
                                 "sentencepiece+nfkc": 0.70, "aggressive": 0.10},
    "homoglyph":                {"raw": 1.0, "tiktoken": 1.0,
                                 "sentencepiece+nfkc": 1.0, "aggressive": 1.0},
}

PIPELINES = ("raw", "tiktoken", "sentencepiece+nfkc", "aggressive")


def _char_category(ch: str) -> str:
    from stegano.detector import categorize
    from stegano.encoders.homoglyph import REVERSE

    cat = categorize(ord(ch))
    if cat is not None:
        return cat
    if ch in REVERSE:
        return "homoglyph"
    return "visible"


def predict(text: str, pipeline: str = "tiktoken") -> dict:
    """Estimate per-character survival of *text* through *pipeline*.

    Returns ``{"pipeline", "experimental", "chars": [...], "survival_rate"}``.
    """
    if pipeline not in PIPELINES:
        raise ValueError(f"unknown pipeline {pipeline!r}; expected one of {PIPELINES}")
    chars: list[dict] = []
    for ch in text:
        cat = _char_category(ch)
        prob = _SURVIVAL.get(cat, {"raw": 1.0}).get(pipeline, 1.0)
        chars.append({"char": f"U+{ord(ch):04X}", "category": cat,
                      "survival": prob})
    rate = sum(c["survival"] for c in chars) / len(chars) if chars else 1.0
    return {
        "pipeline": pipeline,
        "experimental": True,
        "chars": chars,
        "survival_rate": round(rate, 3),
    }
