"""Outbound exfiltration demo (enhancement 6).

The inbound direction hides instructions *for* the model. This module is
the reverse: hiding a secret *inside* model-style output text, so the
secret exfiltrates invisibly inside an otherwise innocent-looking response.
"""

from __future__ import annotations

from stegano import channels


def hide_secret(carrier: str, secret: str, channel: str = "tag_block",
                position: str | int = "middle") -> str:
    """Embed *secret* invisibly inside *carrier* text."""
    ch = channels.get(channel)
    return channels.embed(carrier, ch.encode(secret), position)


def extract_secret(stego_text: str, channel: str = "tag_block") -> str:
    """Recover the hidden secret from carrier text."""
    return channels.get(channel).decode(stego_text)


def demo() -> tuple[str, str]:
    """Return (innocent_looking_response, recovered_secret) demo pair."""
    carrier = ("Here is the summary you asked for. Revenue grew 4% quarter "
               "over quarter, driven by strength in the enterprise segment. "
               "No anomalies were detected in the audit logs.")
    secret = "EXFIL: customer_db_snapshot_2026-10-13"
    stego = hide_secret(carrier, secret)
    return stego, extract_secret(stego)
