"""Synthetic preparation plumbing tests; no host, Lean, crypto or admission.

Except for the explicit constructor contract, fixtures bypass owner/Producer
constructors and replace only process execution. Fake capsules and receipts are
visibly nonproof bytes. A mocked SourceOperation below has no ImportSession,
ReceiptVerifier or VerifiedModule. No positive verification handle is fabricated.
Only a separately root-selected outer runner may execute these controls.
"""
from copy import deepcopy
import argparse
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from preparation import owner as O
from production import producer as P
from modules import codec as C

OUTPUT = None


def journal(spec, words, rank):
    s = C.summarize(spec)
    return (b"DMKNM002"+struct.pack("<I", 2)+b"".join(struct.pack("<I", x) for x in words)
        +bytes.fromhex(s["foundation"]+s["policy"]+C.summary_id(s)+s["group_root"])
        +struct.pack("<IQ", s["group_count"], rank))


def spec(name):
    return {"schema": C.SPEC_SCHEMA, "foundation": "02"*32, "policy": "03"*32,
        "groups": [{"kind": "ordinary", "declarations": [{"name": [["s", name]],
            "kind": "theorem", "universes": 0, "type": ["sort", ["zero"]],
            "value_hash": None, "meta": {}}]}]}


def fake_child(parent=False):
    local = spec("SyntheticLocal")
    words = [int.from_bytes(bytes.fromhex("01"*4), "little")]*8
    parents, receipts = [], []
    if parent:
        base = spec("SyntheticParent")
        raw = journal(base, words, 0)
        parents = [{"journal": list(raw), "openings": [C.group_opening(base, 0)]}]
        receipts = [{"module": C.module_id(base), "journal": raw,
                     "receipt": b"SYNTHETIC_NOT_A_RECEIPT"}]
    return {"status": "UNTRUSTED_PROVER_REQUEST_NOT_CHILD_ADMISSION",
        "input": {"schema": "DMKN_CERTIFIED_MODULES_V2", "image": words,
            "rank": int(parent), "local_spec": local, "rows": [], "parents": parents, "bodies": []},
        "parent_receipts": receipts, "source_sha256": "04"*32, "roots": [[['s', 'SyntheticLocal']]],
        "local_module": C.module_id(local), "local_groups": 1, "parent_selection_binding": "05"*32,
        "mathematical_acceptance": False}


class FakeSupervisor:
    def __init__(self):
        self.calls, self.mode, self.mutate = [], None, None

    def absolute(self, value, *, directory=False, fresh=False):
        p = Path(value)
        P.require(p.is_absolute() and p.resolve() == p, "FAKE_ABSOLUTE")
        P.require(not p.exists() if fresh else (p.is_dir() if directory else p.is_file()), "FAKE_EXISTENCE")
        return p

    # Same Path-only contract as the actual adopted supervisor.
    def overlap(self, a, b): return a.is_relative_to(b) or b.is_relative_to(a)
    def limits_checked(self, limits): return dict(limits)
    def bounded_read(self, path, limit):
        raw = Path(path).read_bytes(); P.require(len(raw) <= limit, "FAKE_READ_BOUND"); return raw

    def supervise(self, argv, cwd, evidence, limits, job):
        self.calls.append((list(argv), dict(limits)))
        if self.mode == "raise": raise RuntimeError("SYNTHETIC_UNKNOWN_PROCESS_OUTCOME")
        evidence.mkdir()
        if argv[1] == "prepare":
            raw = Path(argv[3]).read_bytes(); value = C.parse_json(raw)
            Path(argv[4]).write_bytes(struct.pack("<I", len(raw))+raw)
            Path(argv[5]).write_bytes(journal(value["local_spec"], value["image"], value["rank"]))
            stdout = P.encoded({"status": "PREPARED_ONLY_NOT_CERTIFIED", "image": value["image"],
                "module": C.module_id(value["local_spec"]), "rank": value["rank"], "mathematical_admission": False})
        elif argv[1] == "stage":
            raw = struct.pack("<I", 3)+b"SYNTHETIC_NOT_A_PROVING_CAPSULE"
            Path(argv[9]).write_bytes(raw)
            stdout = ("REAL_EXECUTION_SNAPSHOT_NOT_APPLICATION_CERTIFICATE schema=3 snapshot_bytes="
                +str(len(raw))+" segments=2 assumptions="+argv[10]+" binding="+"06"*32).encode()
        else:
            config = P.parse(Path(argv[-3]).read_bytes())
            out = Path(config["output_directory"]); out.mkdir()
            export = b"SYNTHETIC_NOT_A_NATIVE_EXPORT"
            (out/"EXPORT.json").write_bytes(export)
            (out/"module.ndjson").write_bytes(b"SYNTHETIC_NOT_NATIVE_ROWS")
            result = {"schema": "DMKN_OWNER_LEAN_WORKER_RESULT_V1", "status": "PASS_NATIVE_EXPORT_ONLY",
                "request_sha256": config["request"]["sha256"], "executable_sha256": config["executable"]["sha256"],
                "config_sha256": argv[-1], "worker_sha256": config["worker"]["sha256"],
                "export_sha256": P.hash_bytes(export), "export_bytes": len(export),
                "deadline_monotonic": config["deadline_monotonic"], "native_return_code": 0,
                "native_timed_out": False, "direct_child_reaped": True,
                "outer_job_closure_required": True, "mathematical_acceptance": False}
            if self.mode == "wrong-worker": result["worker_sha256"] = "09"*32
            Path(config["report_path"]).write_bytes(P.encoded(result))
            stdout = b""
        (evidence/"stdout.txt").write_bytes(stdout)
        (evidence/"stderr.txt").write_bytes(b"")
        if self.mutate is not None: self.mutate()
        return {"status": "COMMAND_EXITED_ZERO_AND_CLOSED", "child_exit_code": 0,
            "direct_child_reaped": True, "job_closed": True, "cleanup_errors": [],
            "termination_requested": False, "final_job": {"active_processes": 0,
                "terminated_processes": 0, "cpu_seconds": 100 if self.mode == "overshoot" else 1}}


def fixture(name):
    root = OUTPUT/name; root.mkdir(); install = root/"install"; install.mkdir()
    def saved(name, raw):
        path = install/name; path.write_bytes(raw); return P.file_pin(path)
    host = saved("host.exe", b"SYNTHETIC_NOT_AN_EXECUTABLE")
    profile = {"schema": O.SCHEMA,
        "producer": {"host": host, "python": saved("python.exe", b"SYNTHETIC_NOT_PYTHON"),
            "image_id": "01"*32, "foundation": "02"*32, "policy": "03"*32},
        "image": saved("image.bin", b"SYNTHETIC_NOT_IMAGE"), "worker": saved("worker.py", b"NOT_EXECUTED"),
        "native_executable": saved("frontend.exe", b"SYNTHETIC_NOT_NATIVE"),
        "lean_root": str(install), "lean_runtime_pins": [], "source_pins": []}
    producer = P.Producer.__new__(P.Producer)
    producer.profile = profile["producer"]; producer._profile_raw = P.encoded(producer.profile)
    producer._pins = {}; producer._install = install; producer._A = FakeSupervisor(); producer._Job = object
    producer._closed = False; producer._busy = False; producer._attempt_open = False
    owner = O.OwnerPreparation.__new__(O.OwnerPreparation)
    owner._started = O.time.monotonic(); owner._cpu_started = O.time.process_time()
    owner._closed = owner._busy = owner._unknown = False
    owner._calls = 0; owner._worker_charge = 0.0; owner._history = []; owner._last_failure = None
    owner._allowance = {"allowance_id": "07"*32, "operations": 8, "worker_cpu_seconds": 40,
        "controller_cpu_seconds": 60, "wall_seconds": 600, "output_bytes": 512*P.MIB, "output_entries": 256}
    owner._deadline = owner._started+600
    owner._profile = profile; owner._profile_raw = P.encoded(profile)
    owner._P, owner._A, owner._Job, owner._lean_root = producer, producer._A, object, install
    owner._pins = {row["path"]: row for row in (host, profile["image"], profile["worker"],
                                               profile["native_executable"], profile["producer"]["python"])}
    owner._controls = {}; owner._output = root/"owner"; owner._output.mkdir()
    return owner, root


def source_fixture(owner):
    # Exact class with intentionally mocked methods; no actual live session,
    # verifier or handle is constructed or registered by these unit tests.
    op = O.SourceOperation.__new__(O.SourceOperation)
    op._origin_session = object()
    p = owner._profile["producer"]
    op._origin_verifier = SimpleNamespace(_image=p["image_id"], _foundation=p["foundation"], _policy=p["policy"])
    op._deadline = owner._deadline; op.invalid = False
    def active():
        P.require(not op.invalid and O.time.monotonic() < op._deadline, "SYNTHETIC_SOURCE_EXPIRED")
    op._active = active
    raw = b"SYNTHETIC_SOURCE_REQUEST"
    op.prepare = lambda: {"status": "OWNER_SOURCE_REQUIRES_SUPERVISED_LEAN_AND_FINAL_RELATION",
        "request": raw, "request_sha256": P.hash_bytes(raw), "mathematical_acceptance": False}
    op.finish = lambda raw: fake_child()
    return op


class PreparationControls(unittest.TestCase):
    def test_child_structural_parent_binding_only(self):
        owner, unused = fixture("parent-bindings")
        child = fake_child(True)
        self.assertEqual(owner._child(child)[0]["input"]["rank"], 1)
        for label in ("rank", "schema", "journal", "module"):
            bad = deepcopy(child)
            if label == "rank": bad["input"]["rank"] = 0
            elif label == "schema": bad["input"]["schema"] = "DMKN_CERTIFIED_MODULES_V1"
            elif label == "journal": bad["parent_receipts"][0]["journal"] = b"not-journal"
            else: bad["parent_receipts"][0]["module"] = "09"*32
            with self.assertRaises(ValueError): owner._child(bad)
        self.assertEqual(owner._A.calls, [])

    def test_synthetic_parent_snapshot_direct_handoff(self):
        owner, unused = fixture("parent-snapshot")
        result = owner.snapshot(fake_child(True), "one", cycles=2**25, po2=18,
                                prepare_cpu_seconds=4, cpu_seconds=4)
        self.assertEqual(result["status"], "UNTRUSTED_PROVER_CAPSULE_PREPARED")
        self.assertFalse(result["mathematical_acceptance"])
        self.assertEqual(result["session"]["assumptions"], 1)
        self.assertEqual([a[0][1] for a in owner._A.calls], ["prepare", "stage"])
        args = owner._A.calls[1][0]
        self.assertEqual(args[7:9], ["snapshot", "0"])
        self.assertEqual(args[10:], ["1", result["session"]["parents"][0]["path"]])
        self.assertEqual(owner.report()["worker_cpu_charge"], 2)

    def test_shared_worker_allowance_never_renews(self):
        owner, unused = fixture("allowance")
        owner._allowance["worker_cpu_seconds"] = 6
        owner.snapshot(fake_child(), "one", cycles=100, po2=12, prepare_cpu_seconds=4, cpu_seconds=4)
        with self.assertRaisesRegex(ValueError, "PREPARATION_WORKER_RESERVATION"):
            owner.snapshot(fake_child(), "two", cycles=100, po2=12, prepare_cpu_seconds=4, cpu_seconds=4)
        self.assertEqual(len(owner._A.calls), 3)
        self.assertEqual(owner.report()["worker_cpu_charge"], 3)
        self.assertTrue(owner.report()["closed"])

    def test_unknown_and_overshoot_preserved(self):
        for mode, charge in (("raise", 4), ("overshoot", 100)):
            owner, unused = fixture(mode); owner._A.mode = mode
            with self.assertRaises(Exception):
                owner.snapshot(fake_child(), "one", cycles=100, po2=12, prepare_cpu_seconds=4, cpu_seconds=4)
            self.assertEqual(owner.report()["worker_cpu_charge"], charge)
            self.assertEqual(owner.report()["unknown_worker_accounting"], mode == "raise")
            self.assertTrue(owner.report()["closed"])
            self.assertTrue((owner._output/"one/prepare-reservation.json").is_file())

    def test_author_worker_binding_and_no_authority(self):
        owner, unused = fixture("author")
        result = owner.author(source_fixture(owner), "one", cpu_seconds=4, wall_seconds=60)
        self.assertEqual(result["status"], "UNTRUSTED_CHILD_REQUEST_PREPARED")
        self.assertFalse(result["child"]["mathematical_acceptance"])
        self.assertEqual(len(owner._A.calls), 1)
        argv = owner._A.calls[0][0]
        self.assertEqual(argv[1:4], ["-I", "-S", "-B"])
        bad, unused = fixture("wrong-worker"); bad._A.mode = "wrong-worker"
        with self.assertRaisesRegex(ValueError, "PREPARATION_WORKER_RETURN_BINDING"):
            bad.author(source_fixture(bad), "one", cpu_seconds=4, wall_seconds=60)

    def test_final_original_source_liveness(self):
        owner, unused = fixture("late-source"); op = source_fixture(owner)
        original_save = owner._save
        def save(path, value):
            original_save(path, value)
            if path.name == "RESULT.json" and value.get("status") == "UNTRUSTED_CHILD_REQUEST_PREPARED":
                op.invalid = True
        owner._save = save
        with self.assertRaisesRegex(ValueError, "SYNTHETIC_SOURCE_EXPIRED"):
            owner.author(op, "one", cpu_seconds=4, wall_seconds=60)
        self.assertTrue((owner._output/"one/FINALIZATION-FAILED.json").is_file())
        self.assertTrue(owner.report()["closed"])

    def test_original_deadline_and_no_unfunded_snapshot(self):
        owner, unused = fixture("deadline")
        owner._A.mutate = lambda: setattr(owner, "_deadline", O.time.monotonic()-1)
        with self.assertRaisesRegex(ValueError, "PREPARATION_ORIGINAL_DEADLINE"):
            owner.snapshot(fake_child(), "one", cycles=100, po2=12, prepare_cpu_seconds=4, cpu_seconds=4)
        self.assertEqual(len(owner._A.calls), 1)
        fresh, unused = fixture("bad-stage-cap")
        with self.assertRaises(ValueError):
            fresh.snapshot(fake_child(), "one", cycles=100, po2=12, cpu_seconds=1201)
        self.assertEqual(fresh._A.calls, [])
        # Method metadata/fsync is inside the relative wall cap too, not a free
        # period before an internally renewed per-method deadline.
        for kind in ("author", "snapshot"):
            late, unused = fixture("metadata-"+kind); op = source_fixture(late)
            clock = [O.time.monotonic()]; original_save = late._save
            def save(path, value):
                original_save(path, value)
                if path.name == "operation.json": clock[0] += 61
            late._save = save
            with patch.object(O.time, "monotonic", side_effect=lambda: clock[0]):
                with self.assertRaisesRegex(ValueError, "PREPARATION_"+kind.upper()+"_TOTAL_WALL"):
                    if kind == "author": late.author(op, "one", cpu_seconds=4, wall_seconds=60)
                    else: late.snapshot(fake_child(), "one", cycles=100, po2=12, wall_seconds=60)
            self.assertEqual(late._A.calls, [])

    def test_storage_reservation_and_demand_no_launch(self):
        owner, unused = fixture("storage")
        # More than96MiB is needed for native NDJSON+EXPORT and request+reports.
        owner._allowance["output_bytes"] = 96*P.MIB
        with self.assertRaisesRegex(ValueError, "PREPARATION_OUTPUT_RESERVATION"):
            owner.author(source_fixture(owner), "one", cpu_seconds=4, wall_seconds=60)
        self.assertEqual(owner._A.calls, [])
        fresh, unused = fixture("demand"); op = source_fixture(fresh)
        op.prepare = lambda: {"status": "NEED_AUTHORING_CONTEXT_DATA", "demands": [],
                             "mathematical_acceptance": False}
        out = fresh.author(op, "one", cpu_seconds=4, wall_seconds=60)
        self.assertEqual(out["status"], "NEED_AUTHORING_CONTEXT_DATA")
        self.assertEqual(fresh._A.calls, [])
        self.assertFalse(fresh.report()["closed"])

    def test_constructor_path_types_with_mock_loader(self):
        owner, root = fixture("constructor")
        lean = root/"lean"; (lean/"bin").mkdir(parents=True); (lean/"lib/lean").mkdir(parents=True)
        runtime = []
        for name in ("libInit_shared.dll", "libleanshared.dll", "libleanshared_1.dll", "libleanshared_2.dll", "libc++.dll"):
            path = lean/"bin"/name; path.write_bytes(b"SYNTHETIC_NOT_A_DLL"); runtime.append(P.file_pin(path))
        profile = deepcopy(owner._profile)
        base = Path(O.__file__).resolve().parents[1]
        profile["worker"] = P.file_pin(base/"authoring/worker.py")
        profile["source_pins"] = [P.file_pin(base/name) for name in O.REQUIRED_SOURCES]
        profile["lean_root"] = str(lean); profile["lean_runtime_pins"] = runtime
        # The real OwnerPreparation constructor runs; only the frozen Producer
        # loader is replaced. Thus this is NOT adopted runtime qualification.
        with patch.object(O, "Producer", return_value=owner._P):
            actual = O.OwnerPreparation(profile, owner._allowance, str(root/"constructed"))
        self.assertFalse(actual.report()["closed"])
        self.assertEqual(actual._A.calls, [])
        actual.close()


def main():
    global OUTPUT
    parser = argparse.ArgumentParser(); parser.add_argument("--output", required=True)
    args = parser.parse_args(); OUTPUT = Path(args.output)
    P.require(OUTPUT.is_absolute() and OUTPUT.resolve() == OUTPUT and not OUTPUT.exists(), "FRESH_TEST_OUTPUT")
    OUTPUT.mkdir()
    tests = unittest.defaultTestLoader.loadTestsFromTestCase(PreparationControls)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    record = {"schema": "DMKN_V5_SYNTHETIC_PREPARATION_CONTROLS_V1", "tests": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "native_calls": 0,
        "real_supervisor_calls": 0, "guest_executions": 0, "positive_handles_created": 0,
        "cryptographic_proofs": 0, "mathematical_acceptance": False}
    with (OUTPUT/"CONTROL-RESULT.json").open("xb") as stream: stream.write(P.encoded(record))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__": raise SystemExit(main())
