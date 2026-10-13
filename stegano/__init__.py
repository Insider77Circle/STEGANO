"""STEGANO — invisible-Unicode steganography toolkit for LLM red-team research.

Encoders hide payloads in invisible Unicode channels; decoders recover them;
the detector finds hidden content; the sanitizer removes it.

Channel modules register themselves via :mod:`stegano.channels`.
"""

__version__ = "0.2.0"
__all__ = ["channels", "__version__"]
