"""Focused native-free tests of incremental conditional-observation reuse.

Structural shells bypass constructor adoption. The real receiver/parser/binder,
source pins, trust records, graph checks and filesystem readbacks are exercised.
Native stdout and process reports are explicitly fabricated inert transcripts:
passing these controls is NOT mathematical checking or measured worker benefit.
No predecessor test/helper or external mathematical fixture is imported.
"""
from contextlib import ExitStack
import hashlib
import importlib
import json
import os
from pathlib import Path
import socket
import stat
import subprocess
import sys
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SOURCE = Path(__file__).resolve().parents[1]
MAP = PROJECT/"experiments/v5-local-checks/distribution-terminal-i-01-input.json"
MAP_SHA = "d3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0"
REPLACEMENTS = {
    "v5/admission/pin_phase.py": ("standalone_validation/admission/pin_phase.py",
        "ac7ed2285f2c15630a482817828cf4784ca807c6ec700b4a17bfe3e561eee881"),
    "v5/mixed_claims/imports_atomic.py": ("standalone_validation/mixed_claims/imports_atomic.py",
        "8a8313376d736f25a45b6089f491373bc7e0206aa77b539dbff077fc4eb92595"),
    "v5/mixed_claims/receiver.py": ("incremental_native/mixed_claims/receiver.py",
        "5436569971c272b129fbaec480d51d57a1ec521d43fd4d4ad14133b786691d5b"),
}
NAMES = (
    "mixed_claims", "mixed_claims.packet", "mixed_claims.receiver",
    "admission", "admission.verifier", "admission.bindings", "admission.pin_phase",
    "aggregate_claims", "aggregate_claims.aggregate_admission", "aggregate_claims.admission_binding",
    "aggregate_claims.bindings", "modules", "modules.codec", "delta", "delta.packet",
    "delta.receiver", "delta_claims", "delta_claims.receiver", "delta_claims.claims",
    "production", "production.producer",
)
OUTPUT = CODE = C = T = PP = V = M = B = P = EXPECTED = None
SOURCES, OBSERVED, FORBIDDEN = {}, {}, []
EXECUTED = "NATIVE_EXECUTED_CONDITIONAL_CHECK"
REUSED = "SAME_OWNER_REUSED_CONDITIONAL_CHECK_NO_EXECUTION"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def write_new(path, raw):
    with path.open("xb") as stream:
        if stream.write(raw) != len(raw):
            raise AssertionError("CONTROL_SHORT_WRITE")


def stage(output):
    raw = MAP.read_bytes()
    if sha(raw) != MAP_SHA:
        raise ValueError("CURRENT_BASIS_MAP_CHANGED")
    basis = json.loads(raw)["sdk_sources"]
    if len(basis) != 114 or not set(REPLACEMENTS) <= set(basis):
        raise ValueError("CURRENT_BASIS_MAP_SHAPE")
    code = output/"selected-code"
    code.mkdir()
    for logical, row in sorted(basis.items()):
        if logical in REPLACEMENTS:
            relative, expected = REPLACEMENTS[logical]
            path = SOURCE/relative
            raw = path.read_bytes()
            size = len(raw)
        else:
            path = SOURCE/Path(row["path"]).relative_to(PROJECT/"software/v5")
            expected, size = row["sha256"], row["bytes"]
            raw = path.read_bytes()
        if not 0 < size <= 2*1024**2 or len(raw) != size or sha(raw) != expected:
            raise ValueError("SELECTED_SOURCE_CHANGED:"+logical)
        target = code/logical
        target.parent.mkdir(parents=True, exist_ok=True)
        write_new(target, raw)
        if target.read_bytes() != raw:
            raise ValueError("SELECTED_COPY_CHANGED")
        SOURCES[logical] = dict(source=str(path), bytes=size, sha256=expected)
    if any(name in sys.modules for name in ("admission", "mixed_claims", "modules")):
        raise ValueError("EARLY_PRODUCT_IMPORT")
    sys.path[:0] = [str(code/"v5"), str(code/"portable")]
    return code


def origins():
    return {name: CODE/"v5"/(name.replace(".", "/")+
            ("/__init__.py" if "." not in name else ".py")) for name in NAMES}


def witness(name, parents=(), rank=0, rows=()):
    spec = {"schema": C.SPEC_SCHEMA, "foundation": B.FOUNDATION, "policy": B.POLICY,
        "groups": [{"kind": "ordinary", "declarations": [{"kind": "theorem",
            "name": [["s", name]], "universes": 0, "type": ["sort", ["zero"]],
            "value_hash": None, "meta": {}}]}]}
    summary = C.summarize(spec)
    exact = EXPECTED(summary, rank, B.RELATION_IMAGE)
    return {"schema": "DMKN_CERTIFIED_MODULES_V2", "image": M.journal(exact)["image"],
        "rank": rank, "local_spec": spec, "rows": list(rows), "bodies": [],
        "parents": [{"journal": list(parent), "openings": []} for parent in parents]}, exact


def packet(*items):
    return C.canonical({"schema": P.SCHEMA, "claims": [], "frontiers": [], "deltas": list(items)})


def support():
    return {"schema": T.SUPPORT_SCHEMA, "identities": {"relation_image": B.RELATION_IMAGE,
        "aggregate_image": None, "foundation": B.FOUNDATION, "policy": B.POLICY,
        "receipt_scheme": "resolved-succinct-poseidon2"},
        "roles": {"inert/control": {"bytes": 1, "sha256": sha(b"x")}}}


class Controls(unittest.TestCase):
    def setUp(self):
        self.root = OUTPUT/self._testMethodName
        self.root.mkdir()
        self.serial = 0
        self.fixtures = []
        self.a, self.ja = witness("A")
        self.b, self.jb = witness("B", (self.ja,), 1)
        self.c, self.jc = witness("C", (self.jb,), 2)

    def tearDown(self):
        for fixture in self.fixtures:
            fixture.mixed.close()
            fixture.issuer.close()
        self.assertIsNone(PP._CURRENT.get())
        self.assertIsNone(PP._ORIGIN_PHASE.get())
        self.assertIsNone(T._VALIDATION_PHASE.get())

    def fixture(self):
        self.serial += 1
        root = self.root/str(self.serial)
        root.mkdir()
        domain = T.TrustDomain.create(root/"trust", sha(str(root).encode()), support())
        binding = domain.bind()
        native = root/"INERT-NOT-EXECUTABLE.txt"
        write_new(native, b"TEST-ONLY: native checking is simulated, never executed.\n")
        trust_path = CODE/"v5/admission/trust.py"
        pins = {path: dict(bytes=len(path.read_bytes()), sha256=sha(path.read_bytes()))
                for path in (*origins().values(), trust_path, native)}
        calls, reads = [], []
        state = SimpleNamespace(fail_at=None, output_mutator=None, input_mutator=False,
                                packet_read_mutator=False)

        def absolute(value, directory=False, fresh=False):
            path = Path(value)
            if not path.is_absolute() or ".." in path.parts:
                raise AssertionError("CONTROL_ABSOLUTE_PATH")
            for part in reversed((path, *path.parents)):
                if not part.exists():
                    if part != path or not fresh:
                        raise AssertionError("CONTROL_MISSING_PATH")
                    continue
                info = part.lstat()
                if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
                    raise AssertionError("CONTROL_REDIRECTED_PATH")
            if fresh:
                if path.exists():
                    raise AssertionError("CONTROL_FRESH_PATH")
            elif (path.is_dir() if directory else path.is_file()) is not True:
                raise AssertionError("CONTROL_PATH_KIND")
            return path

        def pin(path):
            absolute(path)
            raw = path.read_bytes()
            return dict(bytes=len(raw), sha256=sha(raw))

        def read(path, bound):
            absolute(path)
            with path.open("rb") as stream:
                raw = stream.read(bound+1)
            if len(raw) > bound:
                raise AssertionError("CONTROL_READ_BOUND")
            reads.append(str(path))
            if state.packet_read_mutator and path.name == "packet.json":
                return raw+b" "
            return raw

        def supervise(argv, cwd, command, limits, job):
            # A fabricated exact-binding transcript, never an actual process.
            self.assertEqual(argv[:3], [str(native), "check", B.RELATION_IMAGE])
            self.assertEqual(cwd, root)
            self.assertIs(job, issuer._job)
            raw = read(Path(argv[3]), 16*P.MIB)
            item = C.parse_json(raw)
            own = EXPECTED(C.summarize(item["local_spec"]), item["rank"], B.RELATION_IMAGE)
            transcript = {"schema": "DMKN_NATIVE_DELTA_CONCLUSION_V1",
                "status": "CHECKED_CONDITIONAL_RELATION_NOT_ADMISSION", "input_sha256": sha(raw),
                "input_bytes": len(raw), "journal": list(own),
                "parents": [parent["journal"] for parent in item["parents"]],
                "mathematical_admission": False}
            calls.append(dict(witness_sha256=sha(raw), witness_bytes=len(raw), limits=dict(limits)))
            if state.output_mutator is not None:
                state.output_mutator(transcript)
            command.mkdir()
            write_new(command/"stdout.txt", C.canonical(transcript))
            if state.input_mutator:
                # Deliberate mutation of this fresh control operation only.
                with Path(argv[3]).open("ab") as stream:
                    stream.write(b" ")
            return {"status": "COMMAND_EXITED_ZERO_AND_CLOSED", "child_exit_code":
                7 if state.fail_at == len(calls) else 0, "direct_child_reaped": True,
                "job_closed": True, "cleanup_errors": [], "termination_requested": False,
                "wall_seconds_through_cleanup": 0.5,
                "final_job": {"cpu_seconds": 0.25, "active_processes": 0, "terminated_processes": 0},
                "control_evidence": "FABRICATED_PROCESS_TRANSCRIPT_NO_PROCESS_EXECUTED"}

        supervisor = SimpleNamespace(absolute=absolute, pin=pin, bounded_read=read,
            limits_checked=lambda limits: dict(limits), supervise=supervise)
        issuer = object.__new__(V.ReceiptVerifier)
        issuer._closed, issuer._busy, issuer._handles = False, False, {}
        issuer._deadline = time.monotonic()+300
        issuer._trust_binding = issuer._trust_original_binding = binding
        issuer._trust_module, issuer._trust_origin = T, trust_path
        issuer._trust_identity, issuer._trust_domain = domain.identity(), domain
        issuer._image, issuer._foundation, issuer._policy = B.RELATION_IMAGE, B.FOUNDATION, B.POLICY
        issuer._caps, issuer._used = (1, 1, 1), [0, 0, 0]
        issuer._install, issuer._manifest = root, root/"manifest.json"
        issuer._manifest_raw = b'{"inert":true}'
        write_new(issuer._manifest, issuer._manifest_raw)
        issuer._loaded_pins, issuer._pins = {}, dict(pins)
        issuer._supervisor, issuer._job = supervisor, object()
        issuer._pin_phase_origin = CODE/"v5/admission/pin_phase.py"
        issuer._profile_id = sha((str(root)+"I").encode())
        mixed = object.__new__(M.MixedDeltaVerifier)
        mixed._owners = mixed._origins = issuer, None
        mixed._profiles = issuer._profile_id, None
        mixed._image, mixed._foundation, mixed._policy = B.RELATION_IMAGE, B.FOUNDATION, B.POLICY
        mixed._aggregate_image = None
        mixed._donor, mixed._A, mixed._Job = issuer, supervisor, issuer._job
        mixed._started, mixed._cpu_started = time.monotonic(), time.process_time()
        mixed._caps = (32, 8*P.MIB, 3600, 120, 300, 256*P.MIB, 4096)
        mixed._deadline = issuer._deadline
        mixed._closed = mixed._busy = False
        mixed._used, mixed._observed_worker = [0, 0, 0], 0.0
        mixed._handles, mixed._cache, mixed._native_memo = {}, {}, {}
        mixed._native_checks = mixed._native_reuses = 0
        mixed._envelope = P.Envelope()
        mixed._pins, mixed._required_origins = dict(pins), origins()
        mixed._native = native
        mixed._profile_id = mixed._origin_profile = sha((str(root)+"mixed").encode())
        mixed._output = root/"receiver"
        mixed._output.mkdir()
        mixed._owner_raw = b'{"inert-owner":true}'
        write_new(mixed._output/"owner.json", mixed._owner_raw)
        result = SimpleNamespace(mixed=mixed, issuer=issuer, calls=calls, reads=reads,
                                 state=state, domain=domain, native=native)
        self.fixtures.append(result)
        mixed._check()
        return result

    def receive(self, f, *items):
        return f.mixed.receive(packet(*items), C.summarize(items[-1]["local_spec"]),
            native_cpu_seconds=3, receipt_cpu_seconds=3, wall_seconds=60, memory_mib=64)

    def denied(self, f, items, reason):
        with self.assertRaisesRegex(Exception, reason):
            self.receive(f, *items)
        self.assertTrue(f.mixed._closed)
        self.assertEqual(f.mixed._native_memo, {})
        self.assertEqual(f.mixed._handles, {})
        self.assertFalse(f.issuer._closed)

    def result(self, f, number):
        return C.parse_json((f.mixed._output/str(number)/"RESULT.json").read_bytes())

    def observe(self, **values):
        OBSERVED[self._testMethodName] = values

    def test_prefix_extension_exact_hits_and_honest_files(self):
        f = self.fixture()
        handles = [self.receive(f, self.a), self.receive(f, self.a, self.b),
                   self.receive(f, self.a, self.b, self.c)]
        self.assertEqual(len(f.calls), 3)
        report = f.mixed.report()
        self.assertEqual((report["native_check_attempts"], report["native_reuse_observations"]), (3, 3))
        self.assertEqual(report["retained_native_records"], 3)
        self.assertEqual(report["retained_native_witness_bytes"], sum(len(C.canonical(w)) for w in (self.a,self.b,self.c)))
        for number, items in enumerate(((self.a,), (self.a,self.b), (self.a,self.b,self.c)), 1):
            result = self.result(f, number)
            self.assertEqual(result["authority"], "SAVED_REPORT_NOT_TRANSFERABLE_PROOF")
            self.assertEqual([row["observation"] for row in result["native_observations"]],
                             [REUSED]*(number-1)+[EXECUTED])
            self.assertEqual(f.mixed.export_packet(handles[number-1]), packet(*items))
            for index, row in enumerate(result["native_observations"]):
                raw = C.canonical(items[index])
                self.assertEqual((row["index"],row["witness_sha256"],row["witness_bytes"]),
                                 (index,sha(raw),len(raw)))
                exists = index == number-1
                for name in (f"delta-{index}.json",f"process-{index}.json",f"native-{index}"):
                    self.assertEqual((f.mixed._output/str(number)/name).exists(), exists)
        self.assertEqual(f.mixed.describe(handles[-1])["journal"], self.jc)
        self.observe(simulated_native_attempts=3,reused_observations=3,full_packets_retained=3,
                     hit_native_files=0,actual_native_calls=0)

    def test_same_journal_changed_witness_misses_but_current_child_can_hit(self):
        f = self.fixture()
        self.receive(f, self.a, self.b)
        changed, same = witness("A", rows=(0,))
        self.assertEqual(same, self.ja)
        self.assertNotEqual(C.canonical(changed), C.canonical(self.a))
        handle = self.receive(f, changed, self.b)
        self.assertEqual(len(f.calls), 3)
        self.assertEqual([r["observation"] for r in self.result(f,2)["native_observations"]], [EXECUTED,REUSED])
        self.assertEqual(f.mixed.describe(handle)["journal"], self.jb)
        self.assertNotIn(C.canonical(self.a), f.mixed._native_memo)
        self.assertIn(C.canonical(changed), f.mixed._native_memo)
        self.observe(same_J_changed_bytes_is_miss=True,child_reused_after_current_parent_established=True)

    def test_current_missing_parent_cannot_be_supplied_by_memo(self):
        f = self.fixture()
        self.receive(f, self.a, self.b)
        before = f.mixed.report()
        self.denied(f, (self.b,), "MIXED_MISSING_OR_FORWARD_PARENT")
        self.assertEqual(len(f.calls), 2)
        after = f.mixed.report()
        self.assertEqual(after["attempts"], before["attempts"]+1)
        self.assertEqual(after["reserved_worker_cpu"], before["reserved_worker_cpu"])
        self.assertEqual(after["native_reuse_observations"], 0)
        self.observe(parser_rejected_missing_current_parent=True,no_cached_premise_authority=True,
                     native_or_hit_observation_after_bad_packet=0)

    def test_record_bindings_conclusion_and_foreign_owner_are_exact(self):
        cases = ((0,object()), (1,"0"*64), (2,"0"*64), (3,"0"*64),
                 (4,"0"*64), (5,(self.ja,)), (6,1))
        for position, bad in cases:
            with self.subTest(position=position):
                f = self.fixture(); self.receive(f,self.a)
                key = C.canonical(self.a)
                record = list(f.mixed._native_memo[key]); record[position] = bad
                f.mixed._native_memo[key] = tuple(record)
                self.denied(f,(self.a,),"MIXED_NATIVE_MEMO_BINDING")
                self.assertEqual(len(f.calls),1)
        other, other_j = witness("OTHER")
        for target in (other_j,EXPECTED(C.summarize(self.a["local_spec"]),1,B.RELATION_IMAGE)):
            f = self.fixture(); self.receive(f,self.a)
            key = C.canonical(self.a); record = list(f.mixed._native_memo[key]); record[-1] = target
            f.mixed._native_memo[key] = tuple(record)
            self.denied(f,(self.a,),"MIXED_NATIVE_MEMO_CONCLUSION")
        foreign, receiver = self.fixture(),self.fixture()
        self.receive(foreign,self.a)
        record = list(foreign.mixed._native_memo[C.canonical(self.a)])
        record[1] = receiver.mixed._profile_id # Isolate exact self, not merely profile mismatch.
        receiver.mixed._native_memo[C.canonical(self.a)] = tuple(record)
        self.denied(receiver,(self.a,),"MIXED_NATIVE_MEMO_BINDING")
        self.assertFalse(foreign.mixed._closed)
        self.assertEqual(len(foreign.mixed._native_memo),1)
        foreign.mixed._check()
        self.observe(binding_mutations=7,conclusion_mutations=2,foreign_record_refused=True,
                     foreign_owner_remains_live=True)

    def test_failed_prefix_readback_and_finalization_never_promote(self):
        x, unused = witness("X")
        for mode in ("second_miss","packet_readback","after_result"):
            with self.subTest(mode=mode):
                f = self.fixture(); self.receive(f,x)
                if mode == "second_miss":
                    f.state.fail_at = 3
                    self.denied(f,(self.a,self.b),"NATIVE_OR_FRONTIER_REJECTED")
                    self.assertFalse((f.mixed._output/"2/RESULT.json").exists())
                elif mode == "packet_readback":
                    f.state.packet_read_mutator = True
                    self.denied(f,(self.a,self.b),"MIXED_PACKET_CHANGED")
                    self.assertFalse((f.mixed._output/"2/RESULT.json").exists())
                else:
                    original = M.MixedDeltaVerifier._save
                    def save(owner,path,value):
                        original(owner,path,value)
                        if owner is f.mixed and path.name == "RESULT.json":
                            owner._deadline = 0
                    with patch.object(M.MixedDeltaVerifier,"_save",save):
                        self.denied(f,(self.a,self.b),"MIXED_ORIGINAL_DEADLINE")
                    self.assertEqual(self.result(f,2)["status"],"MIXED_BOUND_BEFORE_LIVE_PROMOTION")
                self.assertEqual(f.mixed.report()["retained_native_records"],0)
                self.assertEqual(f.mixed.report()["reserved_worker_cpu"],9)
                self.assertEqual(f.mixed.report()["native_check_attempts"],3)
                self.assertTrue((f.mixed._output/"2/FINALIZATION-FAILED.json").is_file())
        self.observe(failure_modes=3,old_and_pending_memos_revoked=True,saved_result_not_live_authority=True)

    def test_last_successful_replacement_cold_owner_and_close(self):
        f = self.fixture(); x, unused = witness("X")
        self.receive(f,self.a); self.receive(f,x); self.receive(f,self.a)
        self.assertEqual(len(f.calls),3)
        self.assertEqual(set(f.mixed._native_memo),{C.canonical(self.a)})
        fresh = self.fixture()
        self.assertEqual(fresh.mixed._native_memo,{})
        self.receive(fresh,self.a)
        self.assertEqual(len(fresh.calls),1)
        self.assertEqual(fresh.mixed.report()["native_reuse_observations"],0)
        f.mixed.close()
        self.denied(f,(self.a,),"MIXED_CLOSED_OR_CHANGED_ORIGIN")
        self.assertEqual(len(f.calls),3)
        self.observe(last_packet_only=True,fresh_owner_cold=True,closed_owner_denied=True,
                     no_report_restoration_api_used=True)

    def test_retention_tiny_bounds_and_skip_causes_only_later_miss(self):
        retain = M.MixedDeltaVerifier._retain_native
        records = {}; marker = object()
        count = retain(records,0,b"abc",marker,2,5)
        self.assertEqual(count,3)
        self.assertEqual(retain(records,count,b"abc",object(),2,5),3)
        self.assertIs(records[b"abc"],marker)
        count = retain(records,count,b"de",marker,2,5)
        self.assertEqual(count,5)
        self.assertEqual(retain(records,count,b"f",marker,3,5),5)
        self.assertNotIn(b"f",records)
        self.assertEqual(retain(records,count,b"g",marker,2,99),5)
        hard = {}; count = 0
        for number in range(17):
            count = retain(hard,count,bytes([number]),marker,100,100)
        self.assertEqual((len(hard),count),(16,16))
        no_large_allocation = {}
        self.assertEqual(retain(no_large_allocation,16*P.MIB,b"z",marker,100,32*P.MIB),16*P.MIB)
        self.assertEqual(no_large_allocation,{})
        f = self.fixture()
        # Test-only retention limit, not a changed parser/owner envelope.
        def retain_one(records,count,raw,record,entry_cap,byte_cap):
            return retain(records,count,raw,record,1,byte_cap)
        with patch.object(M.MixedDeltaVerifier,"_retain_native",staticmethod(retain_one)):
            self.receive(f,self.a,self.b)
        self.assertEqual(set(f.mixed._native_memo),{C.canonical(self.a)})
        self.receive(f,self.a,self.b)
        self.assertEqual((len(f.calls),f.mixed.report()["native_reuse_observations"]),(3,1))
        self.assertEqual(len(f.mixed._native_memo),2)
        self.observe(tiny_byte_and_entry_caps=True,hard_entry_cap=16,
            hard_byte_arithmetic_checked_without_large_allocation=True,skipped_record_only_later_miss=True)

    def test_original_reservations_limits_and_observation_accounting(self):
        f = self.fixture()
        raw = packet(self.a,self.b)
        self.receive(f,self.a,self.b)
        self.receive(f,self.a,self.b)
        report = f.mixed.report()
        self.assertEqual((report["attempts"],report["submitted_bytes"],report["reserved_worker_cpu"]),
                         (2,2*len(raw),12))
        self.assertEqual(report["observed_success_worker_cpu"],0.5) # Simulated, not measured CPU.
        self.assertEqual((report["native_check_attempts"],report["native_reuse_observations"]),(2,2))
        for call in f.calls:
            self.assertEqual((call["limits"]["cpu_seconds"],call["limits"]["active_processes"],
                              call["limits"]["memory_mib"]),(3,2,64))
        self.assertEqual(self.result(f,2)["native_observations"][0]["observation"],REUSED)
        # Full packet CPU reservation still refuses an all-hit packet.
        f.mixed._caps = (*f.mixed._caps[:2],12,*f.mixed._caps[3:])
        self.denied(f,(self.a,self.b),"MIXED_CPU_ALLOWANCE")
        self.assertEqual(f.mixed.report()["attempts"],3)
        self.assertEqual(f.mixed.report()["submitted_bytes"],3*len(raw))
        self.assertEqual(f.mixed.report()["reserved_worker_cpu"],12)
        self.assertEqual(len(f.calls),2)
        # Conservative output reservation applies even if every witness is warm.
        out = self.fixture(); self.receive(out,self.a)
        out.mixed._caps = (*out.mixed._caps[:5],P.MIB,out.mixed._caps[6])
        self.denied(out,(self.a,),"MIXED_OUTPUT_CAP")
        self.assertEqual((len(out.calls),out.mixed.report()["reserved_worker_cpu"]),(1,6))
        self.observe(full_graph_reservations_on_hits=True,failed_attempt_bytes_retained=True,
            simulated_worker_cpu_not_incremented_on_hits=True,output_reserve_still_applies=True,
            actual_worker_cpu_measured=False)

    def test_miss_exact_input_parent_and_conclusion_binding_refusals(self):
        cases = (
            ("input_digest",lambda result: result.update(input_sha256="0"*64),"NATIVE_EXACT_INPUT"),
            ("parent",lambda result: result.update(parents=[list(self.ja)]),"NATIVE_EXACT_PARENTS"),
            ("conclusion",lambda result: result.update(journal=list(self.jb)),"NATIVE_OWN_ADOPTED_CONCLUSION"),
        )
        for label, mutate, reason in cases:
            with self.subTest(label=label):
                f = self.fixture(); f.state.output_mutator = mutate
                self.denied(f,(self.a,),reason)
                self.assertEqual((len(f.calls),f.mixed.report()["native_check_attempts"]),(1,1))
                self.assertEqual(f.mixed.report()["native_reuse_observations"],0)
        f = self.fixture(); f.state.input_mutator = True
        self.denied(f,(self.a,),"MIXED_NATIVE_INPUT_CHANGED")
        self.assertEqual(len(f.calls),1)
        self.observe(real_bind_native_refusals=3,actual_input_readback_refusal=True,
                     rejected_transcripts_seed_no_memo=True)


SELECTED = (
    "test_prefix_extension_exact_hits_and_honest_files",
    "test_same_journal_changed_witness_misses_but_current_child_can_hit",
    "test_current_missing_parent_cannot_be_supplied_by_memo",
    "test_record_bindings_conclusion_and_foreign_owner_are_exact",
    "test_failed_prefix_readback_and_finalization_never_promote",
    "test_last_successful_replacement_cold_owner_and_close",
    "test_retention_tiny_bounds_and_skip_causes_only_later_miss",
    "test_original_reservations_limits_and_observation_accounting",
    "test_miss_exact_input_parent_and_conclusion_binding_refusals",
)


def forbidden(*args, **kwargs):
    FORBIDDEN.append("FORBIDDEN_PROCESS_NETWORK_OR_RECEIPT_CALL")
    raise AssertionError("FORBIDDEN_PROCESS_NETWORK_OR_RECEIPT_CALL")


def main():
    global OUTPUT,CODE,C,T,PP,V,M,B,P,EXPECTED
    if len(sys.argv) != 3 or sys.argv[1] != "--output":
        raise ValueError("OUTPUT_REQUIRED")
    OUTPUT = Path(sys.argv[2])
    if not OUTPUT.is_absolute() or not OUTPUT.is_dir() or OUTPUT.is_symlink():
        raise ValueError("EXISTING_ORDINARY_OUTPUT_REQUIRED")
    CODE = stage(OUTPUT)
    with ExitStack() as guard:
        for target,name in ((subprocess,"Popen"),(os,"system"),(socket.socket,"__init__")):
            guard.enter_context(patch.object(target,name,forbidden))
        C = importlib.import_module("modules.codec")
        T = importlib.import_module("admission.trust")
        PP = importlib.import_module("admission.pin_phase")
        V = importlib.import_module("admission.verifier")
        M = importlib.import_module("mixed_claims.receiver")
        B = importlib.import_module("aggregate_claims.bindings")
        P = importlib.import_module("mixed_claims.packet")
        EXPECTED = importlib.import_module("delta_claims.claims").expected_journal
        for name,path in origins().items():
            if name not in sys.modules or Path(sys.modules[name].__file__).resolve() != path:
                raise ValueError("SELECTED_MODULE_ORIGIN:"+name)
        guard.enter_context(patch.object(V.ReceiptVerifier,"receive",forbidden))
        guard.enter_context(patch.object(M.AggregateReceiptVerifier,"receive",forbidden))
        result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(Controls(name) for name in SELECTED))
    passed = result.wasSuccessful() and result.testsRun == 9 and not result.skipped and not FORBIDDEN
    report = dict(schema="DMKN_INCREMENTAL_NATIVE_CONTROLS_V1",status="PASS" if passed else "FAIL",
        scope="REAL_RECEIVER_BINDING_GUARDS_WITH_FABRICATED_NATIVE_TRANSCRIPTS_NOT_MATHEMATICS",
        tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),
        selected=list(SELECTED),observations=OBSERVED,sources=SOURCES,forbidden_calls=FORBIDDEN,
        actual_native_calls=0,actual_network_calls=0,actual_proof_calls=0,
        simulated_worker_cpu_is_not_measurement=True,constructor_adoption_exercised=False,
        mathematical_acceptance=False,full_cost_growth_claim=False)
    write_new(OUTPUT/"controls-result.json",json.dumps(report,sort_keys=True,
        separators=(",",":"),allow_nan=False).encode()+b"\n")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
