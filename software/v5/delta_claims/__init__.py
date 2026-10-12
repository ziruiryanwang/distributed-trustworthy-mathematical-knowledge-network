"""Exact-warrant delta authority; no aggregate-frontier reinterpretation."""
from .receiver import DeltaVerifier, VerifiedDelta
from delta.packet import Envelope, DeltaError

__all__ = ["DeltaVerifier", "VerifiedDelta", "Envelope", "DeltaError"]
