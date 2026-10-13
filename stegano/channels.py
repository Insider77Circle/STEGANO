"""Channel registry — the plugin point for encodings.

Every channel is a named pair of ``encode(payload: str) -> str`` and
``decode(text: str) -> str`` callables.

Adding a new channel:
  1. Add ``stegano/encoders/<name>.py`` with ``encode(payload) -> str``.
  2. Add ``stegano/decoders/<name>.py`` with ``decode(text) -> str``.
  3. Add one entry to ``_BUILTIN`` below.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Channel:
    """A named steganographic channel (encoder + decoder pair)."""

    name: str
    description: str
    encode: Callable[[str], str]
    decode: Callable[[str], str]


_CHANNELS: dict[str, Channel] = {}


def register(channel: Channel) -> Channel:
    """Register a channel. Returns the channel for decorator use."""
    _CHANNELS[channel.name] = channel
    return channel


def get(name: str) -> Channel:
    """Return the channel registered under *name* (KeyError if unknown)."""
    return _CHANNELS[name]


def names() -> list[str]:
    """Registered channel names, in registration order."""
    return list(_CHANNELS.keys())


def embed(carrier: str, encoded_payload: str, position: str | int = "middle") -> str:
    """Insert an already-encoded payload into carrier text.

    position: "start" | "middle" | "end" | an integer index.
    """
    if position == "start":
        idx = 0
    elif position == "middle":
        idx = len(carrier) // 2
    elif position == "end":
        idx = len(carrier)
    else:
        idx = max(0, min(int(position), len(carrier)))
    return carrier[:idx] + encoded_payload + carrier[idx:]


# name -> (description, encoder module, decoder module)
_BUILTIN: tuple[tuple[str, str, str, str], ...] = (
    ("zero_width", "Bit channel over U+200B/U+200C, U+FEFF-terminated",
     "stegano.encoders.zero_width", "stegano.decoders.zero_width"),
    ("variation_selectors", "Nibble channel over VS1..VS16 (U+FE00-U+FE0F)",
     "stegano.encoders.variation_selectors", "stegano.decoders.variation_selectors"),
    ("bidi", "Bit channel over U+200E/U+200F, U+202C-terminated",
     "stegano.encoders.bidi", "stegano.decoders.bidi"),
    ("tag_block", "Nibble channel over Unicode tag block, U+E007F-terminated",
     "stegano.encoders.tag_block", "stegano.decoders.tag_block"),
    ("homoglyph", "Confusable-substitution channel (injective core table)",
     "stegano.encoders.homoglyph", "stegano.decoders.homoglyph"),
)


def _register_builtin_channels() -> None:
    import importlib

    for name, description, enc_mod, dec_mod in _BUILTIN:
        enc = importlib.import_module(enc_mod)
        dec = importlib.import_module(dec_mod)
        register(Channel(name=name, description=description,
                         encode=enc.encode, decode=dec.decode))


_register_builtin_channels()
