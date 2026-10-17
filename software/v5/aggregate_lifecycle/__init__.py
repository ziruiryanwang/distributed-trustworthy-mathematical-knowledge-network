"""Explicit bounded sealing lifecycle; bookkeeping never grants admission."""
from .producer import LifecycleProducer

__all__ = ("LifecycleProducer",)
