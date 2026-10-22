"""Release-owned constructor over unchanged generic lifecycle and scheduler.

New schemas explicitly give the inherited pin-map slots artifact-reference
meaning. No historical build-result records are created or reopened.
"""
from pathlib import Path
import sys

from production import producer as P
from aggregate_small import producer as S
from aggregate_lifecycle import producer as L
from aggregate_claims import bindings as B
from . import adoption as A

PROFILE_SCHEMA = "DMKN_RELEASE_AGGREGATE_LIFECYCLE_PROFILE_V1"
BASE_PROFILE_SCHEMA = "DMKN_RELEASE_AGGREGATE_OWNER_PROFILE_V1"
PROFILE_DOMAIN = b"DMKN-RELEASE-AGGREGATE-LIFECYCLE-PROFILE-V1\0"
SOURCE_MODULES = A.SOURCE_MODULES


def source_paths():
    root = Path(__file__).resolve().parents[1]
    result = []
    for name in SOURCE_MODULES:
        relative = name.replace(".", "/")
        expected = root/(relative+".py" if "." in name else relative+"/__init__.py")
        module = sys.modules.get(name)
        P.require(module is not None
                  and Path(getattr(module, "__file__", "")).resolve() == expected,
                  "RELEASE_SOURCE_ORIGIN:"+name)
        result.append(expected)
    return tuple(result)


class ReleaseLifecycleProducer(L.LifecycleProducer):
    """Finite owner; release adoption does not authorize a stage or mathematics."""
    def __init__(self, profile):
        self._closed = False; self._busy = False; self._attempt_open = False
        self._history = {}; self._last_call_failure = None
        self._lifecycle_ready = False
        try:
            P.fields(profile, ("schema", "base_profile", "source_pins", "snapshot_host_build", "release"))
            P.require(profile["schema"] == PROFILE_SCHEMA, "RELEASE_PROFILE_SCHEMA")
            raw = P.encoded(profile)
            P.require(len(raw) <= P.MIB, "RELEASE_PROFILE_BYTES")
            self._lifecycle_profile = P.parse(raw)
            self._lifecycle_raw = raw
            self._lifecycle_id = P.hash_bytes(PROFILE_DOMAIN+raw)
            self.profile = P.parse(P.encoded(self._lifecycle_profile["base_profile"]))
            P.fields(self.profile, ("schema", "support_profile", "source_pins", "relation_image",
                                    "host_build", "image_adoption", "stage_memory_ceiling_mib"))
            P.require(self.profile["schema"] == BASE_PROFILE_SCHEMA,
                      "RELEASE_BASE_PROFILE_SCHEMA")
            self._raw = P.encoded(self.profile)
            self.profile_id = self._lifecycle_id
            sources = self._lifecycle_profile["source_pins"]
            P.require(type(sources) is list and len(sources) == len(SOURCE_MODULES)
                      and {P.pin_fields(pin, P.MIB) for pin in sources} == set(source_paths()),
                      "RELEASE_EXACT_SOURCE_ORIGINS")
            adopted = A.load(self._lifecycle_profile["release"], sources, self.support)
            P.require(Path(__file__).resolve().parents[1] == adopted.root/"sdk/v5",
                      "RELEASE_SOURCE_ROOT")
            base_sources = self.profile["source_pins"]
            P.require(type(base_sources) is list and len(base_sources) == 2
                      and {P.pin_fields(pin, P.MIB) for pin in base_sources} ==
                        {Path(S.__file__).resolve().parent/name for name in S.SOURCE_NAMES}
                      and all(adopted.pins.get(pin["path"]) == pin for pin in base_sources),
                      "RELEASE_EXACT_SCHEDULER_SOURCES")
            P.require(self.profile["relation_image"] == B.RELATION_IMAGE,
                      "RELEASE_INDIVIDUAL_RELATION")
            B._adopted_image(self.support["image_id"])
            common = {"release": adopted.manifest_pin, "descriptor": adopted.descriptor_pin}
            expected_host = {**common, "stage_host": adopted.roles["stage_host"]}
            expected_image = {**common, "guest_image": adopted.roles["guest_image"]}
            expected_snapshot = {**common, "snapshot_host": adopted.roles["snapshot_host"]}
            P.require(self.profile["host_build"] == expected_host
                      and self.profile["image_adoption"] == expected_image
                      and self._lifecycle_profile["snapshot_host_build"] == expected_snapshot,
                      "RELEASE_EXACT_ARTIFACT_REFERENCE_MAPS")
            # No old S/L/T constructor or build-adoption method is invoked.
            self._support = P.Producer(self.support)
            self._A, self._Job = self._support._A, self._support._Job
            # S/N use this as both immutable output-exclusion root and host cwd.
            # All host/input/output argv are absolute; support retains its own
            # base root for loading supervisor/runtime files. New evidence binds
            # the full release cwd, never reinterpreting an old snapshot.
            self._install = adopted.root
            P.uint(self.profile["stage_memory_ceiling_mib"], 8192, 1)
            supervisor_memory = self._A.CEILINGS["memory_mib"]
            P.require(type(supervisor_memory) is int
                      and self.profile["stage_memory_ceiling_mib"] <= supervisor_memory,
                      "RELEASE_SUPERVISOR_MEMORY_CEILING")
            self._pins = dict(self._support._pins)
            for pin in adopted.pins.values():
                self._add(self._pins, pin)
            P.require(self._pins == adopted.pins, "RELEASE_EXACT_CONSTRUCTED_CLOSURE")
            self._image = dict(adopted.roles["guest_image"])
            self._snapshot_host = dict(adopted.roles["snapshot_host"])
            self._snapshot_build_pins = P.parse(P.encoded(expected_snapshot))
            self._installation_pins_raw = P.encoded(self._pins)
            self._lifecycle_ready = True
            self._check(self._pins)
        except BaseException as primary:
            self._closed = True
            if hasattr(self, "_support"):
                try:
                    self._support.close()
                except BaseException as cleanup:
                    raise BaseExceptionGroup("RELEASE_CONSTRUCTION_AND_CLOSE_FAILED", [primary, cleanup]) from None
            raise

    def _check(self, pins):
        # Preserves S's exact raw/profile check and L's profile_id, inner/outer,
        # original24 source-origin and _snapshot_build_pins no-override checks.
        super()._check(pins)
        if self._lifecycle_ready:
            source_paths()
            P.require(self._install == Path(self._lifecycle_profile["release"]["root"])
                      and P.encoded(self._pins) == self._installation_pins_raw
                      and self._image == self.profile["image_adoption"]["guest_image"]
                      and self._snapshot_host == self._lifecycle_profile["snapshot_host_build"]["snapshot_host"]
                      and self._snapshot_build_pins == self._lifecycle_profile["snapshot_host_build"],
                      "RELEASE_RUNTIME_BINDING_MUTATED")
            P.require(len(self._pins) <= A.INSTALLATION_PIN_LIMIT
                      and sum(pin["bytes"] for pin in self._pins.values()) <= S.READ_LIMIT,
                      "RELEASE_INSTALLATION_BOUND")
            self._no_override(self.profile["host_build"].values())
            self._no_override(self.profile["image_adoption"].values())

    def _adopt_build(self):
        raise P.ProductionError("RELEASE_HISTORICAL_ADOPTION_FORBIDDEN")

    def _adopt_host_build(self, pins, table, role):
        raise P.ProductionError("RELEASE_HISTORICAL_ADOPTION_FORBIDDEN")

    def _adopt_image(self):
        raise P.ProductionError("RELEASE_HISTORICAL_ADOPTION_FORBIDDEN")
