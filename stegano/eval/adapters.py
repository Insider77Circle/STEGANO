"""Model adapters for the evaluation harness (enhancement 9).

The adapter interface lets Darell plug in real model APIs later; the mock
adapters run fully offline. Mocks measure *decodeability* — whether a
payload survives inside prompt text and can be recovered — which is the
offline-measurable half of "will the model obey it". Real obey rates need
real models.
"""

from __future__ import annotations

from typing import Protocol

from stegano import channels
from stegano.sanitizer import sanitize


class ModelAdapter(Protocol):
    """Interface real model clients must implement."""

    name: str

    def query(self, prompt: str) -> str:
        """Send *prompt*, return the model's text response."""
        ...


class MockAdapter:
    """Simulated vulnerable model: obeys the first decodable instruction.

    Scans the prompt with every registered channel decoder; the first
    channel yielding a non-empty payload "wins" and the mock returns
    ``OBEYED: <payload>``. Otherwise returns a benign refusal string.
    """

    name = "mock-vulnerable"

    def query(self, prompt: str) -> str:
        for ch_name in channels.names():
            if ch_name == "homoglyph":
                continue  # substitution has no delimiter; skip in mocks
            payload = channels.get(ch_name).decode(prompt)
            if payload.strip():
                return f"OBEYED: {payload}"
        return "no instruction found"


class MockDefendedAdapter:
    """Simulated defended model: sanitizes input before 'reading' it."""

    name = "mock-defended"

    def query(self, prompt: str) -> str:
        clean = sanitize(prompt, policy="strip")
        inner = MockAdapter()
        result = inner.query(clean)
        if result.startswith("OBEYED"):
            return "no instruction found (sanitized)"
        return result
