"""Focused resource-profile controls; no host, proof, build or legacy test calls.

Real V2 constructor validation and request/identity/lineage code are exercised.
Retained loader, build/image adoption, snapshot adoption and a saved history
fixture are explicitly synthetic. Run only under root's selected enclosing Job.
"""
from copy import deepcopy
import argparse
from pathlib import Path
import struct
import sys
import unittest
from unittest.mock import patch

SNAPSHOT_V5 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SNAPSHOT_V5))
from aggregate_resources import producer as A
from production import producer as P

OUTPUT = None
TEST_COUNT = 7
FORWARDED = []


def write_bytes(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)
    return P.file_pin(path)


class NoHostSupervisor:
    """Only file-policy helpers; a host invocation is an immediate test error."""
    def __init__(self, memory_ceiling):
        self.CEILINGS = {"memory_mib": memory_ceiling}
        self.capture_memory = None

    def absolute(self, value, *, directory=False, fresh=False):
        path = Path(value)
        P.require(path.is_absolute() and path.resolve() == path, "SYNTHETIC_ABSOLUTE")
        P.require(not path.exists() if fresh else
                  (path.is_dir() if directory else path.is_file()), "SYNTHETIC_EXISTENCE")
        return path

    def overlap(self, left, right):
        return left.is_relative_to(right) or right.is_relative_to(left)

    def save_new(self, path, value):
        write_bytes(Path(path), P.encoded(value))

    def supervise(self, argv, cwd, evidence, limits, job):
        if self.capture_memory is None:
            raise AssertionError("NO_HOST_CALL_AUTHORIZED_BY_RESOURCE_CONTROLS")
        P.require(limits["memory_mib"] == self.capture_memory, "EXACT_FORWARDED_MEMORY")
        reservation_path = Path(argv[10]).parent/"reservation.json"
        reservation = P.parse(reservation_path.read_bytes())
        P.require(reservation["argv"] == argv and reservation["limits"] == limits,
                  "EXACT_DURABLE_FORWARDED_RESERVATION")
        FORWARDED.append({"limits": deepcopy(limits), "argv": list(argv),
                          "reservation": P.file_pin(reservation_path),
                          "scope": "SYNTHETIC_CAPTURE_NO_PROCESS_STARTED"})
        self.capture_memory = None
        # Stop immediately without a native process or a fake proof artifact.
        return {"status": "COMMAND_FAILED", "child_exit_code": 1,
            "direct_child_reaped": True, "job_closed": True, "cleanup_errors": [],
            "termination_requested": False,
            "final_job": {"cpu_seconds": 0, "active_processes": 0, "terminated_processes": 0}}


class SyntheticSupport:
    """Read-only file identities, not real retained-supervisor adoption."""
    def __init__(self, install, memory_ceiling):
        self._A = NoHostSupervisor(memory_ceiling)
        self._Job = object
        self._install = install
        self._pins = {}

    def _check(self, pins):
        for pin in pins.values():
            P.require(P.file_pin(Path(pin["path"])) == pin, "SYNTHETIC_PIN_CHANGED")

    def _read(self, pin, maximum):
        P.pin_fields(pin, maximum)
        self._check({pin["path"]: pin})
        return Path(pin["path"]).read_bytes()

    def close(self):
        pass


class Fixture:
    def __init__(self, name, ceiling=8192):
        self.directory = OUTPUT/name
        self.directory.mkdir()
        self.install = self.directory/"synthetic-inputs"
        self.install.mkdir()

        def saved(name, raw):
            return write_bytes(self.install/name, raw)

        support = {"schema": "SYNTHETIC_SUPPORT_NOT_ADOPTED",
            "host": saved("host.fake", b"NOT_AN_EXECUTABLE"),
            "image_id": "01"*32, "foundation": "03"*32, "policy": "04"*32}
        self.image = saved("image.fake", b"SYNTHETIC_IMAGE_NOT_ADOPTED")
        self.profile = {"schema": A.PREFIX+"PROFILE_V2", "support_profile": support,
            "source_pins": [P.file_pin(Path(A.__file__).resolve().parent/name)
                            for name in A.SOURCE_NAMES],
            "relation_image": "02"*32, "host_build": {}, "image_adoption": {},
            "stage_memory_ceiling_mib": ceiling}
        header = (b"DMKNA002"+struct.pack("<I", 2)
            +bytes.fromhex(support["image_id"]+self.profile["relation_image"]
                          +support["foundation"]+support["policy"])
            +bytes.fromhex("05"*32)+struct.pack("<IQQ", 1, 0, 1))
        session = {"image": self.image,
            "wire": saved("wire.bin", b"DMKNAI02"+struct.pack("<I", 2)
                          +bytes.fromhex(support["image_id"])),
            "expected": saved("header.bin", header),
            "capsule": saved("capsule.bin", b"DMKNAS01"+struct.pack("<I", 1)
                             +bytes.fromhex("06"*32)),
            "parents": [], "session_binding": "06"*32, "capsule_binding": "07"*32,
            "cycles": 1 << 26, "po2": 19, "segments": 1, "assumptions": 0,
            "snapshot_evidence": {"synthetic": saved("screen.fake", b"NOT_AN_ADOPTED_SCREEN")}}
        per_kind = dict(cpu_seconds=1, wall_seconds=10, memory_mib=1,
                        active_processes=1, stdout_bytes=4096, stderr_bytes=4096,
                        output_bytes=4096)
        self.request = {"schema": A.PREFIX+"REQUEST_V1", "allowance_id": "08"*32,
            "session": session, "checkpoints": [],
            "output_directory": str(self.directory/"not-executed"), "stage_limit": 1,
            "budget": dict(worker_cpu_seconds=40, controller_cpu_seconds=60,
                wall_seconds=60, output_bytes=64*P.MIB, output_entries=256,
                stages={kind: dict(per_kind) for kind in P.KINDS}),
            "prior_attempts": [], "carried_external_costs": dict(worker_cpu_seconds=0,
                controller_cpu_seconds=0, wall_seconds=0, scope="SYNTHETIC_RESOURCE_CONTROL")}

    def owner(self, profile=None, *, supervisor_ceiling=8192):
        selected = deepcopy(self.profile if profile is None else profile)
        image = self.image
        # Run the actual new constructor. Only inherited installation adoption
        # and build/image adoption are mocked; profile/source checks remain real.
        with patch.object(P, "Producer", lambda value: SyntheticSupport(self.install, supervisor_ceiling)), \
             patch.object(A.AggregateProducer, "_adopt_build", lambda owner: None), \
             patch.object(A.AggregateProducer, "_adopt_image", lambda owner: setattr(owner, "_image", image)):
            owner = A.AggregateProducer(selected)
        owner._snapshot = lambda session, expected, inputs: None
        return owner


def synthetic_history(owner, fixture):
    """Exact prior-record shape for lineage validation, never an executed PASS."""
    session_id = owner._request(deepcopy(fixture.request))[0]
    # The production request validator only reads the fields populated below.
    # Remaining exact-schema fields intentionally have null values: this is not
    # a counterfeit operational report, nor constructor/proof adoption evidence.
    report = {key: None for key in A.ATTEMPT_FIELDS}
    report.update(schema=A.PREFIX+"ATTEMPT_V1", status="PASS_SELECTED_PREFIX_ONLY",
        profile_id=owner.profile_id, session_id=session_id,
        allowance_id=fixture.request["allowance_id"], prior_attempts=[],
        budget=deepcopy(fixture.request["budget"]),
        carried_external_costs=deepcopy(fixture.request["carried_external_costs"]),
        closure_accounting_known=True, final_binding_validated=True,
        application_receipt_created=False, receipt=None, retained_checkpoints=[],
        worker_cpu_charge_this_attempt=0, controller_cpu_seconds=0, wall_seconds=0,
        output_charge_this_attempt=0, entry_charge_this_attempt=0,
        authority="SYNTHETIC_LINEAGE_FIXTURE_NOT_AN_EXECUTED_ATTEMPT")
    return write_bytes(fixture.directory/"synthetic-prior.json", P.encoded(report))


class ResourceControls(unittest.TestCase):
    def test_v2_requires_explicit_field_and_exact_schema(self):
        fixture = Fixture("schema")
        owner = fixture.owner()
        self.assertEqual(owner.profile["stage_memory_ceiling_mib"], 8192)
        for kind in ("missing", "legacy-without-field", "legacy-with-field", "extra"):
            profile = deepcopy(fixture.profile)
            if kind in ("missing", "legacy-without-field"):
                del profile["stage_memory_ceiling_mib"]
            if kind.startswith("legacy"):
                profile["schema"] = A.PREFIX+"PROFILE_V1"
            if kind == "extra":
                profile["default_resource_upgrade"] = True
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                fixture.owner(profile)

    def test_profile_memory_is_exact_integer_in_one_to_8192(self):
        fixture = Fixture("integers")
        for value in (1, 4096, 8192):
            profile = {**fixture.profile, "stage_memory_ceiling_mib": value}
            self.assertEqual(fixture.owner(profile).profile["stage_memory_ceiling_mib"], value)
        for value in (True, False, 0, -1, 8193, 1.0, 8192.0, "8192", None):
            with self.subTest(value=repr(value)), self.assertRaises(ValueError):
                fixture.owner({**fixture.profile, "stage_memory_ceiling_mib": value})

    def test_adopted_supervisor_ceiling_is_not_assumed(self):
        fixture = Fixture("supervisor", ceiling=4096)
        self.assertEqual(fixture.owner(supervisor_ceiling=4096).profile["stage_memory_ceiling_mib"], 4096)
        with self.assertRaises(ValueError):
            fixture.owner({**fixture.profile, "stage_memory_ceiling_mib": 4097}, supervisor_ceiling=4096)
        for invalid in (True, 8192.0, "8192", None):
            with self.subTest(ceiling=repr(invalid)), self.assertRaises(ValueError):
                fixture.owner(supervisor_ceiling=invalid)
        self.assertEqual(fixture.owner({**fixture.profile, "stage_memory_ceiling_mib": 6144},
                                       supervisor_ceiling=6144).profile["stage_memory_ceiling_mib"], 6144)

    def test_each_stage_memory_uses_profile_without_global_mutation(self):
        fixture = Fixture("requests", ceiling=5120)
        original_common = deepcopy(P.COMMON)
        self.assertEqual(original_common["memory_mib"], 4096)
        owner = fixture.owner()
        request = deepcopy(fixture.request)
        for kind in P.KINDS:
            request["budget"]["stages"][kind]["memory_mib"] = 5120
        owner._request(request)
        for kind in P.KINDS:
            for value in (5121, True, 5120.0, 0):
                changed = deepcopy(request)
                changed["budget"]["stages"][kind]["memory_mib"] = value
                with self.subTest(kind=kind, value=repr(value)), self.assertRaises(ValueError):
                    owner._request(changed)
        # The new memory policy cannot raise retained process/log ceilings.
        for field in ("active_processes", "stdout_bytes"):
            changed = deepcopy(request)
            changed["budget"]["stages"]["segment"][field] = P.COMMON[field]+1
            with self.subTest(unchanged_field=field), self.assertRaises(ValueError):
                owner._request(changed)
        self.assertEqual(P.COMMON, original_common)
        self.assertFalse(Path(request["output_directory"]).exists())

    def test_whole_profile_identity_and_live_mutation(self):
        fixture = Fixture("identity", ceiling=4096)
        original = fixture.owner()
        different = fixture.owner({**fixture.profile, "stage_memory_ceiling_mib": 8192})
        self.assertEqual(original.profile_id, P.hash_bytes(P.encoded(original.profile)))
        self.assertEqual(different.profile_id, P.hash_bytes(P.encoded(different.profile)))
        self.assertNotEqual(original.profile_id, different.profile_id)
        original.profile["stage_memory_ceiling_mib"] = 8192
        with self.assertRaisesRegex(ValueError, "AGGREGATE_PROFILE_MUTATED"):
            original._check({})

    def test_selected_memory_reaches_supervisor_without_allocating_it(self):
        fixture = Fixture("forwarding", ceiling=8192)
        owner = fixture.owner()
        request = deepcopy(fixture.request)
        request["budget"]["stages"]["segment"]["memory_mib"] = 6144
        before = len(FORWARDED)
        owner._A.capture_memory = 6144
        result = owner.run(request)
        self.assertEqual(len(FORWARDED), before+1)
        self.assertEqual(FORWARDED[-1]["limits"]["memory_mib"], 6144)
        self.assertEqual(FORWARDED[-1]["limits"]["active_processes"], 1)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["host_calls_attempted"], 1)  # One synthetic dispatch only.
        self.assertEqual(result["reported_proof_stage_calls"], 0)
        self.assertFalse(result["application_receipt_created"])
        self.assertFalse(result["mathematical_admission"])

    def test_incompatible_profile_and_budget_cannot_rebind_history(self):
        fixture = Fixture("history", ceiling=4096)
        old = fixture.owner()
        prior = synthetic_history(old, fixture)
        continuation = deepcopy(fixture.request)
        continuation["prior_attempts"] = [prior]
        # Positive validator control with unchanged whole profile and budget.
        old._request(deepcopy(continuation))
        upgraded = fixture.owner({**fixture.profile, "stage_memory_ceiling_mib": 8192})
        with self.assertRaisesRegex(ValueError, "COMPLETE_SAME_ALLOWANCE_LINEAGE"):
            upgraded._request(deepcopy(continuation))
        changed_budget = deepcopy(continuation)
        changed_budget["budget"]["stages"]["segment"]["memory_mib"] = 2
        with self.assertRaisesRegex(ValueError, "COMPLETE_SAME_ALLOWANCE_LINEAGE"):
            old._request(changed_budget)
        self.assertEqual(P.file_pin(Path(prior["path"])), prior)
        self.assertFalse(Path(continuation["output_directory"]).exists())


def main():
    global OUTPUT
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    OUTPUT = Path(args.output)
    P.require(OUTPUT.is_absolute() and OUTPUT.resolve() == OUTPUT and not OUTPUT.exists(),
              "FRESH_RESOURCE_CONTROL_OUTPUT")
    OUTPUT.mkdir()
    origins = {}
    for name in ("aggregate_resources", "aggregate_resources.producer", "production", "production.producer"):
        path = Path(sys.modules[name].__file__).resolve()
        P.require(path.is_relative_to(SNAPSHOT_V5), "SELECTED_RESOURCE_IMPORT_ORIGIN")
        origins[name] = P.file_pin(path)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ResourceControls)
    P.require(suite.countTestCases() == TEST_COUNT, "EXACT_RESOURCE_CONTROL_COUNT")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    success = result.wasSuccessful() and result.testsRun == TEST_COUNT and not result.skipped
    report = {"schema": "DMKN_V5_SYNTHETIC_RESOURCE_PROFILE_CONTROLS_V1",
        "status": "PASS_SYNTHETIC_RESOURCE_CONTROLS_ONLY" if success else "FAIL",
        "tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
        "skipped": len(result.skipped), "selected_imports": origins,
        "native_host_calls": 0, "cryptographic_proofs": 0, "guest_executions": 0,
        "build_calls": 0, "actual_native_attempts": 0, "mathematical_admission": False,
        "synthetic_supervisor_calls": len(FORWARDED),
        "mocked_boundaries": ["retained_loader_and_supervisor_adoption", "host_build_adoption",
            "image_adoption", "snapshot_adoption", "saved_history_fixture_not_executed"],
        "scope": "V2_PROFILE_REQUEST_IDENTITY_LINEAGE_ONLY_NOT_PROVER_MEMORY_FEASIBILITY"}
    write_bytes(OUTPUT/"CONTROL-RESULT.json", P.encoded(report))
    write_bytes(OUTPUT/"FORWARDED-LIMITS.json", P.encoded(FORWARDED))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
