"""Focused pure/synthetic controls: ZERO native, proof, build or admission calls.

Run only in root's selected snapshot and enclosing Job. The fake constructor
bypasses build/image adoption and _snapshot; it is NOT a real producer profile.
All fixture data and outcomes remain beneath the fresh --output directory.
The two retained assembly JSON files are read-only exact regression inputs.
No legacy test module is imported and no legacy test campaign is rerun.
"""
from copy import deepcopy
import argparse
from pathlib import Path
import struct
import sys
import unittest

SNAPSHOT_V5 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SNAPSHOT_V5))
from aggregate_production import producer as A
from production import producer as P

OUTPUT = None
FAKE_CALLS = []
TEST_COUNT = 10
ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
ASSEMBLY = ROOT/"experiments/v5-local-checks/proof-memo-image-assembly-01"
RETAINED = {
    "RESULT.json": (2282, "50de313fbc8f20b3f48d971f3183bf66f1079cafe18af460538b414d715a2f4e"),
    "selection.json": (23126, "60b1955f8b7f70b9238693ffb9c31018dc19a2089d6aec13b3238d2810f33600"),
}


def write_bytes(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)
    return A.file_pin(path)


def fake_checkpoint(key, binding):
    kind, index = key.split(":")
    payload = b"SYNTHETIC_NOT_AN_SDK_PROOF"
    return (b"DMKNAP01"+struct.pack("<I", 1)+bytes.fromhex(binding)
            +struct.pack("<Q", len(kind))+kind.encode("ascii")
            +struct.pack("<IQ", int(index), len(payload))+payload)


def fake_header(support, relation):
    return (b"DMKNA002"+struct.pack("<I", 2)
            +bytes.fromhex(support["image_id"]+relation+support["foundation"]+support["policy"])
            +bytes.fromhex("05"*32)+struct.pack("<IQQ", 1, 0, 1))


def stdout_record(key, session, support, artifact):
    kind, index = key.split(":")
    finish = kind == "finish"
    return {"schema": "DMKN_AGGREGATE_PROOF_STAGE_V1",
        "status": "REAL_AGGREGATE_RECEIPT_FINISHED" if finish else
                  "REAL_AGGREGATE_CHECKPOINT_NOT_APPLICATION_RECEIPT",
        "kind": kind, "index": int(index), "aggregate_image": support["image_id"],
        "header_sha256": session["expected"]["sha256"], "capsule_binding": session["capsule_binding"],
        "session_binding": session["session_binding"], "segments": session["segments"],
        "assumptions": session["assumptions"], "output_bytes": artifact["bytes"],
        "output_sha256": artifact["sha256"], "application_receipt_created": finish,
        "guest_execute_calls": 0, "proof_stage_calls": 0 if finish else 1,
        "mathematical_admission": False}


def clean_process(cpu=1):
    return {"status": "COMMAND_EXITED_ZERO_AND_CLOSED", "child_exit_code": 0,
        "direct_child_reaped": True, "job_closed": True, "cleanup_errors": [],
        "termination_requested": False,
        "final_job": {"cpu_seconds": cpu, "active_processes": 0, "terminated_processes": 0}}


class FakeSupport:
    """File identity only. No installation, image, SDK or cryptographic adoption."""
    def _check(self, pins):
        for pin in pins.values():
            P.require(P.file_pin(Path(pin["path"])) == pin, "SYNTHETIC_PIN_CHANGED")

    def _read(self, pin, maximum):
        P.pin_fields(pin, maximum)
        self._check({pin["path"]: pin})
        return Path(pin["path"]).read_bytes()

    def close(self):
        pass


class FakeSupervisor:
    def __init__(self, session, support):
        self.session, self.support = session, support
        self.calls, self.mode = [], None

    def absolute(self, value, *, directory=False, fresh=False):
        path = Path(value)
        P.require(path.is_absolute() and path.resolve() == path, "SYNTHETIC_ABSOLUTE")
        P.require(not path.exists() if fresh else
                  (path.is_dir() if directory else path.is_file()), "SYNTHETIC_EXISTENCE")
        return path

    def overlap(self, left, right):
        return left.is_relative_to(right) or right.is_relative_to(left)

    def bounded_read(self, path, maximum):
        raw = Path(path).read_bytes()
        P.require(0 < len(raw) <= maximum, "SYNTHETIC_READ_LIMIT")
        return raw

    def save_new(self, path, value):
        write_bytes(Path(path), P.encoded(value))
        if self.mode == "finalization" and value.get("schema") == A.PREFIX+"ATTEMPT_V1":
            # Deliberate corruption only of this test's new control document,
            # after its apparent PASS report was saved. No retained data changes.
            request = Path(path).parent/"request.json"
            with request.open("ab") as stream:
                stream.write(b" ")

    def supervise(self, argv, cwd, evidence, limits, job):
        kind, index, artifact = argv[8], int(argv[9]), Path(argv[10])
        key = P.stage_key(kind, index)
        reservation = P.parse((artifact.parent/"reservation.json").read_bytes())
        P.require(reservation["argv"] == argv and reservation["limits"] == limits
                  and reservation["worker_reserved"] == limits["cpu_seconds"],
                  "SYNTHETIC_DURABLE_RESERVATION_BEFORE_CALL")
        self.calls.append((list(argv), dict(limits)))
        FAKE_CALLS.append({"stage": key, "mode": self.mode, "argv": list(argv)})
        if self.mode == "raise":
            raise RuntimeError("SYNTHETIC_SUPERVISOR_INTERRUPTION")
        raw = (b"SYNTHETIC_NOT_A_RECEIPT" if kind == "finish" else
               fake_checkpoint(key, self.session["capsule_binding"]))
        pin = write_bytes(artifact, raw)
        evidence.mkdir()
        self.save_new(evidence/"stdout.txt", stdout_record(key, self.session, self.support, pin))
        with (evidence/"stderr.txt").open("xb"):
            pass
        result = clean_process()
        if self.mode == "nonzero":
            result.update(status="COMMAND_FAILED", child_exit_code=1)
        elif self.mode == "missing_cpu":
            del result["final_job"]["cpu_seconds"]
        return result


def fake_owner(install, support, image, session):
    owner = A.AggregateProducer.__new__(A.AggregateProducer)
    owner.profile = {"schema": "SYNTHETIC_CONSTRUCTOR_BYPASS_NOT_ADOPTION",
        "support_profile": deepcopy(support), "relation_image": "02"*32,
        "source_pins": [], "host_build": {}, "image_adoption": {}}
    owner._raw = P.encoded(owner.profile)
    owner.profile_id = P.hash_bytes(owner._raw)
    owner._pins = {support["host"]["path"]: support["host"]}
    owner._support, owner._install = FakeSupport(), install
    owner._A, owner._Job = FakeSupervisor(session, support), object
    owner._image = image
    owner._closed = owner._busy = owner._attempt_open = False
    owner._history, owner._last_call_failure = {}, None
    # Only the retained screen/adoption boundary is bypassed. Request parsing,
    # pinning, graph, budgets, stages, history and finalization are real code.
    owner._snapshot = lambda selected, expected, inputs: None
    return owner


def fixture(name, *, segments=2, assumptions=1):
    directory = OUTPUT/name
    directory.mkdir()
    install = directory/"synthetic-inputs"
    install.mkdir()
    def saved(name, raw):
        return write_bytes(install/name, raw)
    support = {"host": saved("host.fake", b"NOT_AN_EXECUTABLE"),
               "image_id": "01"*32, "foundation": "03"*32, "policy": "04"*32}
    session = {"image": saved("image.bin", b"SYNTHETIC_IMAGE"),
        "wire": saved("wire.bin", b"DMKNAI02"+struct.pack("<I", 2)+bytes.fromhex(support["image_id"])),
        "expected": saved("header.bin", fake_header(support, "02"*32)),
        "capsule": saved("capsule.bin", b"DMKNAS01"+struct.pack("<I", 1)+bytes.fromhex("06"*32)),
        "parents": [saved("parent-"+str(i)+".bin", ("SYNTHETIC_PARENT_"+str(i)).encode())
                    for i in range(assumptions)],
        "session_binding": "06"*32, "capsule_binding": "07"*32,
        "cycles": 1 << 26, "po2": 19, "segments": segments, "assumptions": assumptions,
        "snapshot_evidence": {"synthetic": saved("screen.fake", b"NOT_A_SCREEN_ADOPTION")}}
    owner = fake_owner(install, support, session["image"], session)
    selected = dict(cpu_seconds=4, wall_seconds=20, memory_mib=64, active_processes=1,
                    stdout_bytes=4096, stderr_bytes=4096, output_bytes=4096)
    request = {"schema": A.PREFIX+"REQUEST_V1", "allowance_id": "08"*32,
        "session": session, "checkpoints": [], "output_directory": str(directory/"attempt-1"),
        "stage_limit": 392, "budget": dict(worker_cpu_seconds=40, controller_cpu_seconds=60,
            wall_seconds=60, output_bytes=64*P.MIB, output_entries=256,
            stages={kind: dict(selected) for kind in P.KINDS}),
        "prior_attempts": [], "carried_external_costs": dict(worker_cpu_seconds=10,
            controller_cpu_seconds=1, wall_seconds=2, scope="SYNTHETIC_CARRIED_COSTS_ONLY")}
    return owner, request, directory


class AggregateControls(unittest.TestCase):
    def test_retained_outer_placeholders_exactly_match_runner(self):
        records, pins = {}, {}
        for name, (size, digest) in RETAINED.items():
            path = ASSEMBLY/name
            pin = P.file_pin(path)
            self.assertEqual((pin["bytes"], pin["sha256"]), (size, digest))
            records[name], pins[name] = P.parse(path.read_bytes()), pin
        outer, selection = records["RESULT.json"], records["selection.json"]
        owner = A.AggregateProducer.__new__(A.AggregateProducer)
        self.assertTrue(any("{snapshot}" in x for x in selection["argv"]))
        self.assertTrue(any("{output}" in x for x in selection["argv"]))
        owner._local_outer(outer, selection, pins["selection.json"], pins["RESULT.json"])
        wrong = deepcopy(outer)
        wrong["result"]["argv"][-1] = selection["argv"][-1]
        with self.assertRaisesRegex(ValueError, "OUTER_EXACT_SELECTED_ARGV"):
            owner._local_outer(wrong, selection, pins["selection.json"], pins["RESULT.json"])
        # The runner does not expand {root}; preserve the literal if selected.
        literal, literal_outer = deepcopy(selection), deepcopy(outer)
        literal["argv"].append("{root}")
        literal_outer["result"]["argv"].append("{root}")
        literal_pin = {**pins["selection.json"], "bytes": len(P.encoded(literal)),
                       "sha256": P.hash_bytes(P.encoded(literal))}
        literal_outer["selection_sha256"] = literal_pin["sha256"]
        owner._local_outer(literal_outer, literal, literal_pin, pins["RESULT.json"])

    def test_graph_boundary_and_finish_retains_segments(self):
        self.assertIs(A.graph, P.graph)  # Integration, not a new graph implementation.
        self.assertEqual(A.graph(1, 0), [("segment:0", ()), ("lift:0", ("segment:0",)),
                                       ("finish:0", ("segment:0", "lift:0"))])
        nodes = A.graph(128, 8)
        self.assertEqual(len(nodes), 392)
        self.assertEqual(nodes[-1], ("finish:0", tuple("segment:"+str(i) for i in range(128))+("resolve:7",)))
        plan = A.missing_plan(2, 1, {"resolve:0"})
        self.assertEqual(plan, [("segment:0", ()), ("segment:1", ()),
                               ("finish:0", ("segment:0", "segment:1", "resolve:0"))])
        with self.assertRaises(ValueError):
            A.missing_plan(1, 0, {"finish:0"})

    def test_aggregate_checkpoint_71_bytes_and_old_schema_refusal(self):
        raw = fake_checkpoint("segment:0", "07"*32)
        A.checkpoint_header(raw[:71], len(raw), "07"*32, "segment:0")
        for prefix, count, binding, key in (
            (raw[:70], len(raw), "07"*32, "segment:0"),
            (raw[:71], len(raw)+1, "07"*32, "segment:0"),
            (raw[:71], len(raw), "09"*32, "segment:0"),
            (raw[:71], len(raw), "07"*32, "lift:0"),
            (struct.pack("<I", 5)+raw[12:], len(raw)-8, "07"*32, "segment:0"),
            (fake_checkpoint("finish:0", "07"*32)[:71], len(fake_checkpoint("finish:0", "07"*32)), "07"*32, "finish:0")):
            with self.subTest(key=key, count=count, prefix=len(prefix)):
                with self.assertRaises(ValueError):
                    A.checkpoint_header(prefix, count, binding, key)

    def test_exact_stage_json_header_and_parent_argv(self):
        owner, request, directory = fixture("formats", assumptions=2)
        session = request["session"]
        raw = Path(session["expected"]["path"]).read_bytes()
        A.header(raw, owner.support, owner.profile["relation_image"])
        for changed in (raw[:-1], b"DMKNA001"+raw[8:], raw[:184]+bytes(8)):
            with self.assertRaises(ValueError):
                A.header(changed, owner.support, owner.profile["relation_image"])
        artifact = session["capsule"]
        row = stdout_record("segment:0", session, owner.support, artifact)
        self.assertEqual(A.stage_output(P.encoded(row), "segment:0", session, owner.support, artifact), row)
        for key, bad in (("index", False), ("proof_stage_calls", True),
                         ("application_receipt_created", 0), ("output_sha256", "00"*32)):
            changed = {**row, key: bad}
            with self.subTest(field=key):
                with self.assertRaises(ValueError):
                    A.stage_output(P.encoded(changed), "segment:0", session, owner.support, artifact)
        duplicate = P.encoded(row).rstrip()[:-1]+b',"index":0}'
        with self.assertRaisesRegex(ValueError, "DUPLICATE_JSON_KEY"):
            A.stage_output(duplicate, "segment:0", session, owner.support, artifact)
        target = directory/"future.checkpoint"
        deps = [session["wire"], session["expected"]]
        argv = A.stage_argv("host", owner.support["image_id"], session, "join:1", target, deps)
        self.assertEqual(argv, ["host", "stage", owner.support["image_id"],
            session["image"]["path"], session["wire"]["path"], session["expected"]["path"],
            str(session["cycles"]), str(session["po2"]), "join", "1", str(target), "2",
            *[pin["path"] for pin in session["parents"]], session["capsule"]["path"],
            *[pin["path"] for pin in deps]])

    def test_complete_synthetic_dispatch_is_not_admission(self):
        owner, request, directory = fixture("complete")
        result = owner.run(request)
        self.assertEqual(result["status"], "PASS_FINISHED_RECEIPT_ARTIFACT")
        self.assertFalse(result["mathematical_admission"])
        self.assertEqual((result["host_calls_attempted"], result["prover_stages_attempted"],
                          result["reported_proof_stage_calls"], result["guest_execute_calls"]), (7, 6, 6, 0))
        self.assertEqual(result["worker_cpu_charge_this_attempt"], 7)
        self.assertEqual([tuple(call[0][8:10]) for call in owner._A.calls],
            [("segment", "0"), ("lift", "0"), ("segment", "1"), ("lift", "1"),
             ("join", "1"), ("resolve", "0"), ("finish", "0")])
        finish = owner._A.calls[-1][0]
        self.assertEqual([Path(x).parent.name for x in finish[14:]],
                         ["segment-0", "segment-1", "resolve-0"])
        self.assertEqual(len(result["retained_checkpoints"]), 6)
        self.assertTrue(result["final_binding_validated"])
        self.assertEqual(len(result["control_documents"]), 2)

    def test_first_failure_and_unknown_cpu_keep_charges(self):
        for mode in ("nonzero", "raise", "missing_cpu"):
            owner, request, directory = fixture(mode)
            owner._A.mode = mode
            result = owner.run(request)
            self.assertEqual(result["status"], "FAIL")
            self.assertEqual(len(owner._A.calls), 1)
            self.assertEqual(result["host_calls_attempted"], 1)
            self.assertEqual(result["prover_stages_attempted"], 1)
            self.assertEqual(result["reported_proof_stage_calls"], 0)
            self.assertFalse(result["application_receipt_created"])
            self.assertEqual(result["retained_checkpoints"], [])
            self.assertEqual(result["worker_cpu_charge_this_attempt"], 1 if mode == "nonzero" else 4)
            self.assertEqual(result["closure_accounting_known"], mode == "nonzero")
            self.assertEqual(owner.report()["closed"], mode != "nonzero")

    def test_unfunded_reservations_refuse_before_host(self):
        for bound in ("worker", "output"):
            owner, request, directory = fixture("reserve-"+bound)
            if bound == "worker": request["budget"]["worker_cpu_seconds"] = 3
            else: request["budget"]["output_bytes"] = 4*P.MIB
            result = owner.run(request)
            self.assertEqual(result["status"], "FAIL")
            self.assertEqual(owner._A.calls, [])
            self.assertEqual(result["host_calls_attempted"], 0)
            self.assertEqual(result["worker_cpu_charge_this_attempt"], 0)
            self.assertFalse(result["full_path_envelope"]["full_path_fits_requested_envelopes"])
            self.assertGreaterEqual(result["output_charge_this_attempt"], A.TAIL_BYTES)
            self.assertGreaterEqual(result["entry_charge_this_attempt"], A.TAIL_ENTRIES)

    def test_finalization_marker_overrides_saved_pass(self):
        owner, request, directory = fixture("finalization")
        request["stage_limit"] = 1
        owner._A.mode = "finalization"
        with self.assertRaisesRegex(ValueError, "FINALIZATION_FAILED"):
            owner.run(request)
        attempt = directory/"attempt-1"
        saved = P.parse((attempt/"RESULT.json").read_bytes())
        self.assertEqual(saved["status"], "PASS_SELECTED_PREFIX_ONLY")
        marker = P.parse((attempt/"FINALIZATION-FAILED.json").read_bytes())
        self.assertTrue(marker["overrides_result"])
        self.assertTrue(owner.report()["closed"])
        with self.assertRaisesRegex(ValueError, "FINALIZATION_OVERRIDE"):
            owner._no_override([P.file_pin(attempt/"RESULT.json")])

    def test_complete_lineage_and_prior_success_cannot_disappear(self):
        owner, request, directory = fixture("lineage")
        request["stage_limit"] = 2
        first = owner.run(request)
        self.assertEqual(first["status"], "PASS_SELECTED_PREFIX_ONLY")
        omitted = deepcopy(request)
        omitted["output_directory"] = str(directory/"omitted")
        with self.assertRaisesRegex(ValueError, "LIVE_ALLOWANCE_HISTORY_MISSING"):
            owner.run(omitted)
        second = deepcopy(request)
        second.update(output_directory=str(directory/"attempt-2"),
                      prior_attempts=[P.file_pin(directory/"attempt-1/RESULT.json")],
                      checkpoints=deepcopy(first["retained_checkpoints"]))
        lost = deepcopy(second)
        lost["checkpoints"].pop()
        with self.assertRaisesRegex(ValueError, "PRIOR_SUCCESS_MUST_BE_RETAINED"):
            owner.run(lost)
        changed = deepcopy(second)
        changed["carried_external_costs"]["scope"] = "ALTERED_COST_LINEAGE"
        with self.assertRaisesRegex(ValueError, "COMPLETE_SAME_ALLOWANCE_LINEAGE"):
            owner.run(changed)
        result = owner.run(second)
        self.assertEqual(result["prior_allowance_worker_charge"], 2)
        self.assertEqual(result["worker_cpu_charge_this_attempt"], 2)
        self.assertEqual(len(result["retained_checkpoints"]), 4)
        third = deepcopy(second)
        third.update(output_directory=str(directory/"attempt-3"),
                     prior_attempts=[P.file_pin(directory/"attempt-2/RESULT.json")],
                     checkpoints=result["retained_checkpoints"])
        # A fresh synthetic process has no in-memory history, but persisted
        # predecessor chaining must still reject omission of the first attempt.
        fresh = fake_owner(owner._install, owner.support, owner._image, request["session"])
        with self.assertRaisesRegex(ValueError, "COMPLETE_SAME_ALLOWANCE_LINEAGE"):
            fresh.run(third)
        self.assertEqual(fresh._A.calls, [])

    def test_ordered_parents_and_budget_are_session_lineage(self):
        owner, request, directory = fixture("parent-lineage", assumptions=2)
        request["stage_limit"] = 1
        first = owner.run(request)
        next_request = deepcopy(request)
        next_request.update(output_directory=str(directory/"attempt-2"),
            prior_attempts=[P.file_pin(directory/"attempt-1/RESULT.json")],
            checkpoints=first["retained_checkpoints"])
        for change in ("parents", "budget"):
            altered = deepcopy(next_request)
            if change == "parents": altered["session"]["parents"].reverse()
            else: altered["budget"]["worker_cpu_seconds"] += 1
            with self.subTest(change=change):
                with self.assertRaisesRegex(ValueError, "COMPLETE_SAME_ALLOWANCE_LINEAGE"):
                    owner.run(altered)
        self.assertEqual(len(owner._A.calls), 1)
        self.assertFalse((directory/"attempt-2").exists())


def main():
    global OUTPUT
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    OUTPUT = Path(args.output)
    P.require(OUTPUT.is_absolute() and OUTPUT.resolve() == OUTPUT and not OUTPUT.exists(),
              "FRESH_SYNTHETIC_OUTPUT_REQUIRED")
    OUTPUT.mkdir()
    origins = {}
    for name in ("aggregate_production", "aggregate_production.producer", "production", "production.producer"):
        path = Path(sys.modules[name].__file__).resolve()
        P.require(path.is_relative_to(SNAPSHOT_V5), "CONTROL_SELECTED_IMPORT_ORIGIN")
        origins[name] = P.file_pin(path)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(AggregateControls)
    P.require(suite.countTestCases() == TEST_COUNT, "EXACT_CONTROL_COUNT")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    success = result.wasSuccessful() and result.testsRun == TEST_COUNT and not result.skipped
    report = {"schema": "DMKN_V5_SYNTHETIC_AGGREGATE_PRODUCER_CONTROLS_V1",
        "status": "PASS_SYNTHETIC_CONTROLS_ONLY" if success else "FAIL", "tests": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
        "selected_imports": origins, "fake_supervisor_calls": len(FAKE_CALLS),
        "native_host_calls": 0, "guest_executions": 0, "cryptographic_proofs": 0,
        "build_calls": 0, "mathematical_admission": False, "constructor_adoption_tested": False,
        "mocked_boundaries": ["constructor_build_image_adoption", "complete_snapshot_adoption", "supervisor"],
        "retained_read_only_inputs": {name: {"bytes": size, "sha256": digest}
                                      for name, (size, digest) in RETAINED.items()}}
    write_bytes(OUTPUT/"CONTROL-RESULT.json", P.encoded(report))
    write_bytes(OUTPUT/"FAKE-CALLS.json", P.encoded(FAKE_CALLS))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
