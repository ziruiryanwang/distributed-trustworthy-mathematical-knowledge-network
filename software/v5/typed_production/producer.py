"""Typed-image adoption over the unchanged aggregate lifecycle and scheduler.

The fresh composite profile is never temporarily represented as an old profile.
Only installation and snapshot adoption differ; receipt rules, reservations,
stage selection, prior charges and first-failure stopping remain inherited.
"""
from pathlib import Path
import sys

from production import producer as P
from aggregate_small import producer as S
from aggregate_lifecycle import producer as L
from aggregate_lifecycle import snapshot as N
from aggregate_claims import bindings as B
from . import host_adoption as H
from . import image_adoption as I
from . import snapshot_adoption as R

PROFILE_SCHEMA = "DMKN_TYPED_AGGREGATE_LIFECYCLE_PROFILE_V1"
PROFILE_DOMAIN = b"DMKN-TYPED-AGGREGATE-LIFECYCLE-PROFILE-V1\0"
TYPED_MODULES = ("typed_production", "typed_production.producer",
                 "typed_production.snapshot_adoption", "typed_production.host_adoption",
                 "typed_production.image_adoption")
SOURCE_MODULES = (*L.SOURCE_MODULES, *TYPED_MODULES)


def source_paths():
    """Exact 29-module ordinary closure, also required in support runtime pins."""
    root = Path(__file__).resolve().parents[1]
    paths = list(L.source_paths())
    for name in TYPED_MODULES:
        relative = name.replace(".", "/")
        expected = root/(relative+".py" if "." in name else relative+"/__init__.py")
        module = sys.modules.get(name)
        P.require(module is not None
                  and Path(getattr(module, "__file__", "")).resolve() == expected,
                  "TYPED_SOURCE_ORIGIN:"+name)
        paths.append(expected)
    return tuple(paths)


def _evidence_kind(pins):
    P.require(type(pins) is dict, "TYPED_SNAPSHOT_EVIDENCE_OBJECT")
    keys = set(pins)
    if keys == set(R.EVIDENCE_FIELDS):
        return "retained"
    P.require(keys == set(N.EVIDENCE_FIELDS), "TYPED_SNAPSHOT_EVIDENCE_FIELDS")
    return "generic"


class TypedLifecycleProducer(L.LifecycleProducer):
    """Exact retained general36 adoption followed by ordinary generic snapshots.

Profile has schema/base_profile/source_pins/snapshot_host_build. Its base profile
uses aggregate_small's grammar with the selected corrected stage build and typed
image adoption records. It is local owner configuration, never a peer request.
"""
    def __init__(self, profile):
        P.fields(profile, ("schema", "base_profile", "source_pins", "snapshot_host_build"))
        P.require(profile["schema"] == PROFILE_SCHEMA, "TYPED_PROFILE_SCHEMA")
        raw = P.encoded(profile)
        P.require(len(raw) <= P.MIB, "TYPED_PROFILE_BYTES")
        self._lifecycle_profile = P.parse(raw)
        self._lifecycle_raw = raw
        self._lifecycle_id = P.hash_bytes(PROFILE_DOMAIN+raw)
        self._lifecycle_ready = False
        try:
            # L's constructor requires its old schema/source-count. Initialize
            # its small, explicit state here without changing the base scheduler.
            S.AggregateProducer.__init__(self, self._lifecycle_profile["base_profile"])
            P.require(self.profile["relation_image"] == B.RELATION_IMAGE
                      and self.support["foundation"] == B.FOUNDATION
                      and self.support["policy"] == B.POLICY
                      and self.support["image_id"] == I.IMAGE_ID,
                      "TYPED_MATHEMATICAL_PROFILE")
            B._adopted_image(self.support["image_id"])
            sources = self._lifecycle_profile["source_pins"]
            P.require(type(sources) is list and len(sources) == len(SOURCE_MODULES)
                      and {P.pin_fields(pin, P.MIB) for pin in sources} == set(source_paths()),
                      "TYPED_EXACT_SOURCE_PINS")
            for pin in sources:
                self._add(self._pins, pin, P.MIB)
            builds = self._lifecycle_profile["snapshot_host_build"]
            self._snapshot_host = self._adopt_host_build(builds, self._pins, "snapshot")
            self._snapshot_build_pins = P.parse(P.encoded(builds))
            self.profile_id = self._lifecycle_id
            self._lifecycle_ready = True
            P.require(sum(pin["bytes"] for pin in self._pins.values()) <= S.READ_LIMIT,
                      "TYPED_INSTALLATION_ENVELOPE")
            self._check(self._pins)
        except BaseException:
            self._closed = True
            if hasattr(self, "_support"):
                self._support.close()
            raise

    def _check(self, pins):
        super()._check(pins)
        if self._lifecycle_ready:
            source_paths()
        for path in getattr(self, "_refinement_empty_evidence", ()):
            self._A.absolute(path)
            P.require(path.stat().st_size == 0, "TYPED_EMPTY_EVIDENCE_CHANGED")

    def _adopt_host_build(self, pins, table, role):
        if role != "stage":
            return S.AggregateProducer._adopt_host_build(self, pins, table, role)
        # This runs during the base constructor, before lifecycle readiness.
        runtime = self.support["runtime_pins"]
        by_path = {P.pin_fields(pin): pin for pin in runtime}
        P.require(len(by_path) == len(runtime), "TYPED_DUPLICATE_RUNTIME_PIN")
        for path in source_paths():
            P.require(path in by_path, "TYPED_SOURCE_NOT_SELECTED:"+str(path))
            self._add(table, by_path[path], P.MIB)
        return H.adopt_build(self, pins, table)

    def _adopt_image(self):
        I.adopt_image(self)

    def _snapshot(self, session, expected, inputs):
        # Select by distinct record grammar before validation. A failed path
        # never falls back to a different schema or an older adoption rule.
        if _evidence_kind(session["snapshot_evidence"]) == "retained":
            R.adopt(self, session, expected, inputs)
        else:
            N.adopt(self, session, expected, inputs)

    def production_request(self, snapshot_evidence, *, allowance_id, budget, checkpoints,
                           prior_attempts, output_directory, stage_limit, carried_external_costs):
        """No-output request construction/preflight; does not fund or dispatch."""
        P.require(not self._closed and not self._busy, "TYPED_CLOSED_OR_BUSY")
        if _evidence_kind(snapshot_evidence) == "generic":
            return super().production_request(snapshot_evidence, allowance_id=allowance_id,
                budget=budget, checkpoints=checkpoints, prior_attempts=prior_attempts,
                output_directory=output_directory, stage_limit=stage_limit,
                carried_external_costs=carried_external_costs)
        session = R.session_from_evidence(self, snapshot_evidence, {})
        session["snapshot_evidence"] = P.parse(P.encoded(snapshot_evidence))
        request = P.parse(P.encoded({"schema": S.PREFIX+"REQUEST_V1", "allowance_id": allowance_id,
            "session": session, "checkpoints": checkpoints, "output_directory": str(output_directory),
            "stage_limit": stage_limit, "budget": budget, "prior_attempts": prior_attempts,
            "carried_external_costs": carried_external_costs}))
        self.preflight(request)
        return request
