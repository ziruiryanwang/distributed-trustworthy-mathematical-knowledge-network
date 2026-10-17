"""Stable owner for generic mixed-tail sealing over the retained po18 scheduler.

New profile/snapshot adoption, not a reinterpretation of historical COST_SCREEN
records. Native hosts, stage graphs, reservations and receipt semantics are reused.
An enclosing owner must bound imports, construction, refusals and finalization.
"""
from __future__ import annotations

from pathlib import Path
import sys
import time

from aggregate_small import producer as S
from production import producer as P
from aggregate_claims import bindings as B
from aggregate_claims.prepare_mixed import prepare_mixed_seal
from mixed_claims.packet import Envelope
from . import snapshot as N

PROFILE_SCHEMA = "DMKN_AGGREGATE_LIFECYCLE_PROFILE_V1"
PROFILE_DOMAIN = b"DMKN-AGGREGATE-LIFECYCLE-PROFILE-V1\0"
SOURCE_MODULES = (
    "aggregate_lifecycle", "aggregate_lifecycle.producer", "aggregate_lifecycle.snapshot",
    "aggregate_small", "aggregate_small.producer", "production", "production.producer",
    "aggregate_claims", "aggregate_claims.bindings", "aggregate_claims.input",
    "aggregate_claims.prepare_mixed", "mixed_claims", "mixed_claims.packet",
    "delta", "delta.packet", "delta.receiver", "delta_claims", "delta_claims.claims",
    "delta_claims.receiver", "admission", "admission.bindings", "admission.verifier",
    "modules", "modules.codec")


def source_paths():
    """Exact ordinary source closure, including package-initializer imports."""
    root = Path(__file__).resolve().parents[1]
    result = []
    for name in SOURCE_MODULES:
        module = sys.modules.get(name)
        P.require(module is not None, "LIFECYCLE_REQUIRED_MODULE:"+name)
        relative = name.replace(".", "/")
        expected = root/(relative+".py" if "." in name else relative+"/__init__.py")
        P.require(Path(getattr(module, "__file__", "")).resolve() == expected,
                  "LIFECYCLE_SOURCE_ORIGIN:"+name)
        result.append(expected)
    return tuple(result)


class LifecycleProducer(S.AggregateProducer):
    """Explicit successor with stable installation and preserved base profile.

    profile = {schema, base_profile, source_pins, snapshot_host_build}.
    The inherited base profile and internal stage-request grammar stay unchanged.
    Composite profile identity prevents old or changed-owner allowance continuation.
    Only the retained zero-backend-rebuild host-adoption grammar is supported here;
    a resource-refined host needs a separately selected adoption successor.
    """
    def __init__(self, profile):
        P.fields(profile, ("schema", "base_profile", "source_pins", "snapshot_host_build"))
        P.require(profile["schema"] == PROFILE_SCHEMA, "LIFECYCLE_PROFILE_SCHEMA")
        raw = P.encoded(profile)
        P.require(len(raw) <= P.MIB, "LIFECYCLE_PROFILE_BYTES")
        self._lifecycle_profile = P.parse(raw)
        self._lifecycle_raw = raw
        self._lifecycle_id = P.hash_bytes(PROFILE_DOMAIN+raw)
        self._lifecycle_ready = False
        try:
            super().__init__(self._lifecycle_profile["base_profile"])
            P.require(self.profile["relation_image"] == B.RELATION_IMAGE
                      and self.support["foundation"] == B.FOUNDATION
                      and self.support["policy"] == B.POLICY, "LIFECYCLE_MATHEMATICAL_PROFILE")
            B._adopted_image(self.support["image_id"])
            sources = self._lifecycle_profile["source_pins"]
            P.require(type(sources) is list and len(sources) == len(SOURCE_MODULES)
                      and {P.pin_fields(pin, P.MIB) for pin in sources} == set(source_paths()),
                      "LIFECYCLE_EXACT_SOURCE_PINS")
            for pin in sources:
                self._add(self._pins, pin, P.MIB)
            builds = self._lifecycle_profile["snapshot_host_build"]
            self._snapshot_host = self._adopt_host_build(builds, self._pins, "snapshot")
            self._snapshot_build_pins = P.parse(P.encoded(builds))
            self.profile_id = self._lifecycle_id
            self._lifecycle_ready = True
            P.require(sum(pin["bytes"] for pin in self._pins.values()) <= S.READ_LIMIT,
                      "LIFECYCLE_INSTALLATION_ENVELOPE")
            self._check(self._pins)
        except BaseException:
            self._closed = True
            if hasattr(self, "_support"):
                self._support.close()
            raise

    def _check(self, pins):
        super()._check(pins)
        if self._lifecycle_ready:
            P.require(P.encoded(self._lifecycle_profile) == self._lifecycle_raw
                      and self.profile_id == self._lifecycle_id
                      and P.encoded(self.profile) == P.encoded(self._lifecycle_profile["base_profile"]),
                      "LIFECYCLE_PROFILE_MUTATED")
            source_paths()
            self._no_override(self._snapshot_build_pins.values())

    def profile_document(self):
        """Fresh owner-profile data for explicit caller pinning; performs no write."""
        self._check(self._pins)
        return P.parse(self._lifecycle_raw)

    def prepare(self, packet_bytes, exact_journal, *, envelope: Envelope):
        P.require(not self._closed and not self._busy, "LIFECYCLE_CLOSED_OR_BUSY")
        self._check(self._pins)
        result = prepare_mixed_seal(packet_bytes, exact_journal,
            adopted_image=self.support["image_id"], envelope=envelope)
        self._check(self._pins)
        return result

    def snapshot(self, prepared, *, configuration, selection):
        """One selected layout, no proof. Caller later supplies completed outer pin."""
        P.require(not self._closed and not self._busy, "LIFECYCLE_CLOSED_OR_BUSY")
        self._busy = True
        started, cpu = time.monotonic(), time.process_time()
        self._last_call_failure = None
        try:
            return N.execute(self, prepared, configuration, selection, started, cpu)
        except BaseException as error:
            self._last_call_failure = {
                "scope": "SNAPSHOT_REFUSAL_NOT_DURABLE_BUDGET_LEDGER",
                "controller_cpu_seconds": time.process_time()-cpu,
                "wall_seconds": time.monotonic()-started,
                "attempt_directory_created": self._attempt_open,
                "error": type(error).__name__+": "+str(error)[:2000]}
            if self._attempt_open:
                self._closed = True
            raise
        finally:
            self._busy = False

    def _snapshot(self, session, expected, inputs):
        N.adopt(self, session, expected, inputs)

    def preflight(self, request):
        """Validate one ordinary stage request and quote; no output or host call."""
        P.require(not self._closed and not self._busy, "LIFECYCLE_CLOSED_OR_BUSY")
        self._busy = True
        try:
            sid, inputs, inventory, nodes, output, prior, envelope = self._request(P.parse(P.encoded(request)))
            self._check(self._pins); self._check(inputs)
            P.require(not output.exists(), "LIFECYCLE_PREFLIGHT_OUTPUT_CREATED")
            return {"schema": "DMKN_AGGREGATE_LIFECYCLE_PREFLIGHT_V1",
                "status": "PASS_REQUEST_PREFLIGHT_ONLY", "profile_id": self.profile_id,
                "session_id": sid, "selected_stages": [{"key": k, "dependencies": list(d)} for k,d in nodes],
                "retained_checkpoint_count": len(inventory), "prior_allowance_charges": prior,
                "full_path_envelope": envelope, "host_calls": 0, "proof_calls": 0,
                "mathematical_admission": False, "funding": False}
        finally:
            self._busy = False

    def production_request(self, snapshot_evidence, *, allowance_id, budget, checkpoints,
                           prior_attempts, output_directory, stage_limit, carried_external_costs):
        """Construct and validate a request. No funding, execution or auto-renewal."""
        P.require(not self._closed and not self._busy, "LIFECYCLE_CLOSED_OR_BUSY")
        P.fields(snapshot_evidence, N.EVIDENCE_FIELDS)
        result = P.parse(self._read(snapshot_evidence["result"], P.MIB))
        N.result_shape(result, self.profile_id)
        session = P.parse(P.encoded(result["session"]))
        session["snapshot_evidence"] = P.parse(P.encoded(snapshot_evidence))
        request = {"schema": S.PREFIX+"REQUEST_V1", "allowance_id": allowance_id,
            "session": session, "checkpoints": checkpoints, "output_directory": str(output_directory),
            "stage_limit": stage_limit, "budget": budget, "prior_attempts": prior_attempts,
            "carried_external_costs": carried_external_costs}
        request = P.parse(P.encoded(request))
        self.preflight(request)
        return request
