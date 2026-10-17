"""Narrow stage-build adoption successors; existing snapshot rules are unchanged.

The inherited profile grammar remains explicit owner data. New stage/build and
adapter source pins change its identity; the old owner rejects the new build
schema. Nothing here changes images, receipt verification or stage scheduling.
"""
from pathlib import Path
import sys

from production import producer as P
from aggregate_small.producer import AggregateProducer
from aggregate_lifecycle.producer import LifecycleProducer, source_paths
from .adoption import adopt_build


def required_source_paths():
    """Loaded closure that must be pinned in the support runtime map."""
    root = Path(__file__).resolve().parents[1]
    extra = []
    for name in ("prover_memory", "prover_memory.adoption", "prover_memory.producer"):
        relative = name.replace(".", "/")
        path = root/(relative+".py" if "." in name else relative+"/__init__.py")
        module = sys.modules.get(name)
        P.require(module is not None and Path(getattr(module, "__file__", "")).resolve() == path,
                  "REFINEMENT_SOURCE_ORIGIN:"+name)
        extra.append(path)
    return (*source_paths(), *extra)


class _RefinedHost:
    def __init__(self, profile):
        try:
            super().__init__(profile)
        except BaseException:
            self._closed = True
            if hasattr(self, "_support"):
                self._support.close()
            raise

    def _check(self, pins):
        super()._check(pins)
        for path in getattr(self, "_refinement_empty_evidence", ()):
            self._A.absolute(path)
            P.require(path.stat().st_size == 0, "REFINEMENT_EMPTY_EVIDENCE_CHANGED")

    def _adopt_host_build(self, pins, table, role):
        if role != "stage":
            return super()._adopt_host_build(pins, table, role)
        # Constructor calls this before optional lifecycle fields are ready.
        # Bind the whole imported closure, not just the three new source files.
        runtime = self.support["runtime_pins"]
        by_path = {P.pin_fields(pin): pin for pin in runtime}
        P.require(len(by_path) == len(runtime), "REFINEMENT_DUPLICATE_RUNTIME_PIN")
        for path in required_source_paths():
            P.require(path in by_path, "REFINEMENT_SOURCE_NOT_SELECTED:"+str(path))
            self._add(table, by_path[path], P.MIB)
        return adopt_build(self, pins, table)


class RefinedAggregateProducer(_RefinedHost, AggregateProducer):
    """Refined stage host plus the retained completed-layout adoption grammar."""


class RefinedLifecycleProducer(_RefinedHost, LifecycleProducer):
    """Refined stage host plus the new generic selected-target lifecycle."""
