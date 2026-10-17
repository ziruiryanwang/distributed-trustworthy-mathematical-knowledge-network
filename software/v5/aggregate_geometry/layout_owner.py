"""Pinned layout-only owner; no inherited proof dispatch or allowance ledger.

The retained Producer is composed solely for its selected installation loader,
pin checks and Job supervisor. No stage owner is constructed. Its private run
method is never invoked here. Local configuration/build records are not proofs.
"""
from __future__ import annotations

from pathlib import Path
import sys
import time

from production import producer as P
from aggregate_small import producer as S
from aggregate_claims import bindings as B
from aggregate_claims.prepare_mixed import prepare_mixed_seal
from mixed_claims.packet import Envelope
from . import adoption, snapshot

PROFILE_SCHEMA = "DMKN_GEOMETRY17_LAYOUT_PROFILE_V1"
PROFILE_DOMAIN = b"DMKN-GEOMETRY17-LAYOUT-PROFILE-V1\0"
SOURCE_MODULES = (
    "aggregate_geometry", "aggregate_geometry.layout_owner", "aggregate_geometry.adoption",
    "aggregate_geometry.snapshot", "aggregate_small", "aggregate_small.producer",
    "production", "production.producer", "aggregate_claims", "aggregate_claims.bindings",
    "aggregate_claims.input", "aggregate_claims.prepare_mixed", "mixed_claims", "mixed_claims.packet",
    "delta", "delta.packet", "delta.receiver", "delta_claims", "delta_claims.claims",
    "delta_claims.receiver", "admission", "admission.bindings", "admission.verifier",
    "modules", "modules.codec")


def source_paths():
    root = Path(__file__).resolve().parents[1]
    result = []
    for name in SOURCE_MODULES:
        relative = name.replace(".", "/")
        expected = root/(relative+".py" if "." in name else relative+"/__init__.py")
        module = sys.modules.get(name)
        P.require(module is not None and Path(getattr(module, "__file__", "")).resolve() == expected,
                  "GEOMETRY17_SOURCE_ORIGIN:"+name)
        result.append(expected)
    return tuple(result)


class LayoutOwner:
    """Generic prepare/snapshot/close only. No run, preflight or proof request API.

    An enclosing finite owner must bound imports, construction, refusals and
    finalization. snapshot returns untrusted execution data, not a certificate.
    """
    _add = S.AggregateProducer._add
    _read = S.AggregateProducer._read
    _records = S.AggregateProducer._records
    _no_override = S.AggregateProducer._no_override
    _local_outer = S.AggregateProducer._local_outer
    _adopt_image = S.AggregateProducer._adopt_image

    def __init__(self, profile):
        P.fields(profile, ("schema", "support_profile", "source_pins", "relation_image",
                           "snapshot_host_build", "image_adoption"))
        P.require(profile["schema"] == PROFILE_SCHEMA, "GEOMETRY17_PROFILE_SCHEMA")
        raw = P.encoded(profile)
        P.require(len(raw) <= P.MIB, "GEOMETRY17_PROFILE_BYTES")
        self.profile = P.parse(raw)
        self._raw = raw
        self.profile_id = P.hash_bytes(PROFILE_DOMAIN+raw)
        self._closed = False
        self._busy = False
        self._attempt_open = False
        self._last_call_failure = None
        try:
            self._support = P.Producer(self.profile["support_profile"])
            self._A, self._Job = self._support._A, self._support._Job
            self._install = self._support._install
            self._pins = dict(self._support._pins)
            P.require(self.profile["relation_image"] == B.RELATION_IMAGE
                      and self.support["foundation"] == B.FOUNDATION
                      and self.support["policy"] == B.POLICY, "GEOMETRY17_MATHEMATICAL_PROFILE")
            B._adopted_image(self.support["image_id"])
            selected = self.profile["source_pins"]
            P.require(type(selected) is list and len(selected) == len(SOURCE_MODULES)
                      and {P.pin_fields(pin, P.MIB) for pin in selected} == set(source_paths()),
                      "GEOMETRY17_EXACT_SOURCE_CLOSURE")
            for pin in selected:
                self._add(self._pins, pin, P.MIB)
            self._snapshot_host = adoption.adopt_build(self, self.profile["snapshot_host_build"], self._pins)
            P.require(self._snapshot_host == self.support["host"], "GEOMETRY17_SELECTED_SNAPSHOT_HOST")
            self._adopt_image()
            # Separate ordinary source/profile pins from the large compiler map:
            # the selected build rebinds that map, not every layout operation.
            P.require(sum(pin["bytes"] for pin in self._pins.values()) <= 512*P.MIB,
                      "GEOMETRY17_INSTALLATION_BYTE_ENVELOPE")
            P.require(len(self._pins)+12 <= snapshot.RUNTIME_PIN_LIMIT,
                      "GEOMETRY17_PROSPECTIVE_OUTER_PIN_ENVELOPE")
            self._check(self._pins)
        except BaseException:
            self._closed = True
            if hasattr(self, "_support"):
                self._support.close()
            raise

    @property
    def support(self):
        return self.profile["support_profile"]

    def _check(self, pins):
        P.require(P.encoded(self.profile) == self._raw
                  and self.profile_id == P.hash_bytes(PROFILE_DOMAIN+self._raw),
                  "GEOMETRY17_PROFILE_MUTATED")
        self._support._check(pins)
        source_paths()
        for group in ("snapshot_host_build", "image_adoption"):
            self._no_override(self.profile[group].values())
        self._no_override(getattr(self, "_retained_build_pins", ()))

    def profile_document(self):
        self._check(self._pins)
        return P.parse(self._raw)

    def prepare(self, packet_bytes, exact_journal, *, envelope: Envelope):
        P.require(not self._closed and not self._busy, "GEOMETRY17_CLOSED_OR_BUSY")
        self._check(self._pins)
        result = prepare_mixed_seal(packet_bytes, exact_journal,
            adopted_image=self.support["image_id"], envelope=envelope)
        self._check(self._pins)
        return result

    def snapshot(self, prepared, *, configuration, selection):
        P.require(not self._closed and not self._busy, "GEOMETRY17_CLOSED_OR_BUSY")
        self._busy = True
        started, cpu = time.monotonic(), time.process_time()
        self._last_call_failure = None
        try:
            return snapshot.execute(self, prepared, configuration, selection, started, cpu)
        except BaseException as error:
            self._last_call_failure = {
                "scope": "LAYOUT_REFUSAL_NOT_DURABLE_BUDGET_LEDGER",
                "controller_cpu_seconds": time.process_time()-cpu,
                "wall_seconds": time.monotonic()-started,
                "attempt_directory_created": self._attempt_open,
                "error": type(error).__name__+": "+str(error)[:2000]}
            if self._attempt_open:
                self._closed = True
            raise
        finally:
            self._busy = False

    def close(self):
        P.require(not self._busy, "GEOMETRY17_BUSY")
        self._closed = True
        self._support.close()

    def report(self):
        return {"closed": self._closed, "busy": self._busy, "last_call_failure": self._last_call_failure,
                "authority": "LOCAL_LAYOUT_OBSERVATION_NOT_PROOF_OR_COMPLETE_PROCESS_COST"}
