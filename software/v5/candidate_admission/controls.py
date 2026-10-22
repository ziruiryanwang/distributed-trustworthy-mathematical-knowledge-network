"""Focused candidate-nonacceptance controls, selected and launched only by root.

Structural report and real own-output checks; no cryptographic assertion.
All product imports are staged from the operation's exact source snapshot.
"""
from copy import deepcopy
import asyncio
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from types import MethodType, SimpleNamespace
import unittest
from unittest.mock import patch

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MAP = PROJECT/"experiments/v5-local-checks/distribution-exact-packet-01-input.json"
MAP_SHA = "328c21bb585881d654f1a23f1704fbaa277ee865f7adb1250cf6c19b85647561"
SUPERVISOR = PROJECT/"product-local/v4-library-commons-02/commons-v4/operator/commons.py"
SUPERVISOR_SHA = "6ea16154f4533e80d2e4e27e12fb6fa0ab7abfa0ff2c52cfb7479c1a35a8c1c9"
SELF = "software/v5/candidate_admission/controls.py"
OVERLAYS = {
    "v5/delta/custody.py": "software/v5/offer_enumeration/delta/custody.py",
    "v5/admission/clean_refusal.py": "software/v5/candidate_admission/admission/clean_refusal.py",
    "v5/admission/verifier.py": "software/v5/candidate_admission/admission/verifier.py",
    "v5/aggregate_claims/aggregate_admission.py": "software/v5/candidate_admission/aggregate_claims/aggregate_admission.py",
    "v5/client/workspace_evidence.py": "software/v5/candidate_admission/client/workspace_evidence.py",
    "v5/client/managed_owner.py": "software/v5/candidate_admission/client/managed_owner.py",
}
SELECTED = ("test_01_report_conjuncts_and_nonmutation", "test_02_actual_output_bounds_and_nonmutation",
            "test_03_terminal_facade_noninterference_and_positive_cache",
            "test_04_public_trial_dispatch_and_fatal_final_guard",
            "test_05_i_owner_refusal_transition_with_explicit_worker_double",
            "test_06_a_owner_refusal_transition_with_explicit_worker_double")
OBSERVED, FORBIDDEN, SOURCE_ROWS = {}, [], {}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def ordinary(path):
    need(path.is_absolute() and path.resolve() == path and all(
        not item.is_symlink() and not item.is_junction() for item in (path, *path.parents)),
        "CANDIDATE_CONTROL_ORDINARY")
    return path


def write_new(path, data):
    with path.open("xb") as stream:
        stream.write(data)


def forbidden(*args, **kwargs):
    FORBIDDEN.append("FORBIDDEN_PROCESS")
    raise AssertionError(FORBIDDEN[-1])


def stage(output):
    selection = json.loads((output/"selection.json").read_bytes())
    pins, snapshot = selection["sources"], output/"sources"
    need(len(pins) == 137 and Path(__file__).resolve() == snapshot/SELF,
         "CANDIDATE_CONTROL_SNAPSHOT")
    need(hashlib.sha256((snapshot/SELF).read_bytes()).hexdigest() == pins[SELF],
         "CANDIDATE_CONTROL_SELF_PIN")
    raw = ordinary(MAP).read_bytes()
    need(len(raw) == 2813358 and hashlib.sha256(raw).hexdigest() == MAP_SHA,
         "CANDIDATE_CONTROL_MAP_PIN")
    basis = json.loads(raw)["sdk_sources"]
    need(len(basis) == 129 and not set(OVERLAYS)-set(basis)-{"v5/admission/clean_refusal.py"},
         "CANDIDATE_CONTROL_OVERLAY_KEYS")
    code = output/"selected-code"; code.mkdir()
    for logical in sorted(set(basis) | set(OVERLAYS)):
        if logical in OVERLAYS:
            relative = OVERLAYS[logical]
            expected = pins[relative]
        else:
            row = basis[logical]
            relative = Path(row["path"]).relative_to(PROJECT).as_posix()
            expected = row["sha256"]
            need(pins[relative] == expected, "CANDIDATE_CONTROL_BASE_SOURCE_PIN")
        data = ordinary(snapshot/relative).read_bytes()
        need(0 < len(data) <= 2*1024**2 and hashlib.sha256(data).hexdigest() == expected,
             "CANDIDATE_CONTROL_SELECTED_SOURCE_PIN")
        target = code/logical; target.parent.mkdir(parents=True, exist_ok=True)
        write_new(target, data)
        need(target.read_bytes() == data, "CANDIDATE_CONTROL_STAGING_READBACK")
        SOURCE_ROWS[logical] = dict(source=relative, bytes=len(data), sha256=expected)
    need(len(SOURCE_ROWS) == 130 and not any(name in sys.modules for name in
         ("admission", "aggregate_claims", "client", "modules")), "CANDIDATE_CONTROL_IMPORT_ORDER")
    sys.path[:0] = [str(code/"v5"), str(code/"portable")]
    need(hashlib.sha256(ordinary(SUPERVISOR).read_bytes()).hexdigest() == SUPERVISOR_SHA,
         "CANDIDATE_CONTROL_SUPERVISOR_PIN")
    spec = importlib.util.spec_from_file_location("candidate_controls_supervisor", SUPERVISOR)
    module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def report_fixture(directory):
    limits = dict(cpu_seconds=2, wall_seconds=10, memory_mib=64, active_processes=2,
                  stdout_bytes=16384, stderr_bytes=16384)
    argv = ["X:\\owner-adopted\\verifier.exe", "receive"]
    job = dict(user_cpu_seconds=0.25, kernel_cpu_seconds=0.25, cpu_seconds=0.5,
               active_processes=0, total_processes=1, terminated_processes=0,
               peak_job_private_commit_bytes=1024)
    return dict(schema="DMKN_V4_OWNER_COMMAND_REPORT_V1", status="COMMAND_FAILED",
        authority="LOCAL_OPERATION_REPORT_NOT_MATHEMATICAL_ACCEPTANCE", argv=argv,
        cwd=str(directory), limits=limits, child_exit_code=1, direct_child_reaped=True,
        final_job=job, last_observed_job=deepcopy(job), job_closed=True, cleanup_errors=[],
        termination_requested=False,
        cpu_scope="NATIVE_JOB_USER_TIME_LIMIT_AND_SAMPLED_JOB_USER_PLUS_KERNEL;WRAPPER_SEPARATE",
        limits_scope="WALL_TOTAL_CPU_AND_LOG_CAPS_SAMPLED_NOT_HARD_DISK_CAPS",
        observed_logs=dict(stdout_bytes=0, stderr_bytes=2), service_orderly_stop_sent=False,
        wrapper_supervision_cpu_seconds=0.1, wall_seconds_through_cleanup=0.5)


class Controls(unittest.TestCase):
    def owner_fixture(self, kind, mode):
        """Actual owner methods/helper; explicit constructor, worker and trust doubles.

        No minted handle is claimed genuine. Only negative/control transitions run.
        """
        root = OUTPUT/("owner-"+kind+"-"+mode); root.mkdir()
        install = root/"install"; install.mkdir()
        cls = IV.ReceiptVerifier if kind == "I" else AV.AggregateReceiptVerifier
        owner = cls.__new__(cls)
        prior = object(); member = object()
        owner._handles = {prior: b"existing-inert-handle"}
        owner._members = {member: b"existing-inert-member"}
        owner._member_cache = {b"prior": member}
        owner._deadline = time.monotonic()+60
        owner._busy = owner._closed = False
        owner._caps = (10, 1024**2, 20); owner._used = [0, 0, 0]
        owner._output_reserved = [0, 0]; owner._output_caps = (8*1024**2, 256)
        owner._foundation, owner._policy = B.FOUNDATION, B.POLICY
        owner._image = B.RELATION_IMAGE if kind == "I" else "11"*32
        owner._profile_id = "33"*32
        owner._install, owner._manifest = install, install/"manifest.json"
        owner._pins = {}; owner._executable = install/"inert-verifier-not-executed.exe"
        owner._job = object()
        fresh = []
        def active():
            need(not owner._closed and time.monotonic() < owner._deadline, "EXPLICIT_OWNER_INACTIVE")
        def fresh_guard():
            fresh.append("fresh-post-worker")
            active()
            if mode == "changed_trust": raise ValueError("EXPLICIT_TRUST_CHANGE")
        owner._active = active
        owner._check_install = owner._check_live = active
        owner._fresh_install_check = owner._fresh_live_check = fresh_guard
        def supervise(argv, cwd, evidence, limits, job, *, started):
            evidence.mkdir()
            write_new(evidence/"stdout.txt", b"accepted-looking" if mode == "stdout" else b"")
            write_new(evidence/"stderr.txt", b"x\n")
            report = report_fixture(cwd)
            report.update(argv=list(argv), cwd=str(cwd), limits=deepcopy(limits))
            if mode == "exit2": report["child_exit_code"] = 2
            if mode == "stdout": report["observed_logs"]["stdout_bytes"] = 16
            if mode == "overrun":
                report["final_job"].update(user_cpu_seconds=2.0, kernel_cpu_seconds=0.0, cpu_seconds=2.0)
                report["last_observed_job"] = deepcopy(report["final_job"])
            if mode == "changed_input": (evidence.parent/"receipt.bin").write_bytes(b"different")
            if mode == "changed_header": (evidence.parent/"header.bin").write_bytes(b"different")
            return report
        def save_new(path, value):
            SUP.save_new(path, value)
            if mode == "late_refusal_io" and path.name == "refusal.json":
                owner._deadline = time.monotonic()-1
        owner._supervisor = SimpleNamespace(limits_checked=SUP.limits_checked,
            absolute=SUP.absolute, overlap=SUP.overlap, bounded_read=SUP.bounded_read,
            supervise=supervise, save_new=save_new)
        data = self.facade_fixture()
        statement = data.summary if kind == "I" else data.header
        return SimpleNamespace(owner=owner, prior=prior, member=member, statement=statement,
                               output=root/"attempt", fresh=fresh)

    def facade_fixture(self):
        """Real selected method bodies, explicit inert owner/store/authority doubles."""
        spec = dict(schema=C.SPEC_SCHEMA, foundation=B.FOUNDATION, policy=B.POLICY,
            groups=[dict(kind="ordinary", declarations=[dict(name=[["s", "trialFixture"]],
                kind="theorem", universes=0, type=["sort", ["zero"]], value_hash=None, meta={})])])
        summary = C.summarize(spec)
        exact = EXPECTED(summary, 0, B.RELATION_IMAGE)
        image = "11"*32
        profile = EC.public_profile(image, terminal_i=True)
        charges, inputs, calls, issued = [], [], [], {}
        old_token, old_handle, session, context, view = object(), object(), object(), object(), object()
        old_staged = {object(): (b"old-selected-data", False)}
        client = SimpleNamespace(_receipt_cache={}, _aggregate_cache={}, _packet_cache={},
            _profiles=("I-profile", "A-profile", "mixed-profile"), _aggregate_image=image,
            _counts=dict(admission_submissions=0, same_live_hits=0),
            _session=session, _context=context, _selection_view=view, _staged=old_staged,
            _warrants={old_token: old_handle}, _busy=False, _closed=False, fatal=[],
            grant=SimpleNamespace(directory=OUTPUT/"fake-owner-outputs", remaining_seconds=lambda: 60,
                deadline=time.monotonic()+60, _cpu=time.process_time(),
                _limits={"controller_cpu_seconds": 60}),
            workspace=SimpleNamespace(_envelope=ENV(), config=dict(terminal_receipt_bytes=4096,
                                                                   wire_profile=profile)))
        class Issuer:
            def __init__(self, kind):
                self.kind, self._handles = kind, {old_handle: b"prior-live-fixture"}
                self._deadline = client.grant.deadline
            def try_receive(self, raw, statement, output, **limits):
                calls.append((self.kind, "trial", raw))
                if raw == b"bad": return None
                handle = object(); self._handles[handle] = raw
                return handle
            def receive(self, raw, statement, output, **limits):
                calls.append((self.kind, "strict", raw))
                if raw == b"bad": raise ValueError("EXPLICIT_STRICT_ISSUER_REFUSAL")
                handle = object(); self._handles[handle] = raw
                return handle
            def select_member(self, handle, journal, index, siblings):
                calls.append((self.kind, "member", journal)); return handle
        client.receipt, client.aggregate = Issuer("I"), Issuer("A-member")
        client._origin_owners = (client.receipt, client.aggregate, None, None)
        client._budget = SimpleNamespace(verification=lambda size, cpu: charges.append((size, cpu)))
        client._charge = lambda raw: inputs.append(raw)
        def issue(kind, handle, raw):
            token = object()
            live = dict(module=C.summary_id(summary), summary=summary, journal=exact,
                        profile_id=client._profiles[0 if kind == "I" else 1],
                        receipt_sha256=hashlib.sha256(raw).hexdigest())
            issued[token] = (kind, handle, raw, live)
            client._warrants[token] = issued[token]
            return token
        client._issue = issue
        client._warrant = lambda token: issued[token]
        client._aggregate_fact = lambda handle, raw, header: dict(header=header,
            receipt_sha256=hashlib.sha256(raw).hexdigest(), receipt_bytes=len(raw), profile_id="A-profile")
        for name in ("_inspect", "_expected", "_admit_i", "_admit_a_member", "_admit_evidence"):
            setattr(client, name, MethodType(getattr(FE.CommonsClient, name), client))
        client._terminal_trial_result = FE.CommonsClient._terminal_trial_result
        packet = lambda receipt: EP.pack_terminal_i(exact, receipt, aggregate_image=image,
                                                    envelope=ENV(), terminal_i=True)
        header = (B.MAGIC + B.VERSION.to_bytes(4, "little") + bytes.fromhex(image)
            + bytes.fromhex(B.RELATION_IMAGE) + bytes.fromhex(B.FOUNDATION) + bytes.fromhex(B.POLICY)
            + B.commitment([exact]) + (1).to_bytes(4, "little") + (0).to_bytes(8, "little")
            + (1).to_bytes(8, "little"))
        client._enter = lambda: setattr(client, "_busy", True)
        client._active = lambda: None
        client._census = lambda: None
        client._fail = lambda error: client.fatal.append(type(error).__name__+":"+str(error))
        return SimpleNamespace(client=client, summary=summary, exact=exact, packet=packet,
            header=header, image=image, calls=calls, charges=charges, inputs=inputs,
            old_token=old_token, old_handle=old_handle, session=session, context=context,
            view=view, staged=old_staged)

    def test_01_report_conjuncts_and_nonmutation(self):
        good = report_fixture(OUTPUT)
        original = deepcopy(good)
        def check(value):
            return CR.validate_report(value, argv=good["argv"], cwd=Path(good["cwd"]), limits=good["limits"])
        self.assertIsNone(check(good)); self.assertEqual(good, original)
        cases = []
        def add(name, path, value):
            bad = deepcopy(good); at = bad
            for key in path[:-1]: at = at[key]
            at[path[-1]] = value
            cases.append((name, bad))
        for key, values in {
            "schema": ["wrong"], "authority": ["wrong"], "status": ["RESOURCE_LIMIT", "COMMAND_EXITED_ZERO_AND_CLOSED"],
            "child_exit_code": [True, 0, 2, -1, 0xC0000005], "direct_child_reaped": [False, 1],
            "job_closed": [False, 1], "termination_requested": [True, 0],
            "cleanup_errors": [["bad"], ()], "service_orderly_stop_sent": [True, 0],
            "wrapper_supervision_cpu_seconds": [True, -1, float("inf"), 61],
            "wall_seconds_through_cleanup": [True, -1, float("nan"), 11],
            "argv": [["other"]], "cwd": [str(OUTPUT)+"-other"], "final_job": [None],
        }.items():
            for number, value in enumerate(values): add(key+str(number), [key], value)
        add("error_field_even_empty", ["error"], "")
        add("unknown_field", ["new_field"], 1)
        add("limits_changed", ["limits", "cpu_seconds"], 3)
        for key, values in {
            "active_processes": [True, 1, -1], "terminated_processes": [False, 1, -1],
            "total_processes": [True, 0], "cpu_seconds": [True, -1, float("inf"), 3, 0.75],
            "user_cpu_seconds": [True, -1, float("nan")], "kernel_cpu_seconds": [True, -1],
            "peak_job_private_commit_bytes": [True, -1, 64*1024**2+1],
        }.items():
            for number, value in enumerate(values):
                bad = deepcopy(good)
                bad["final_job"][key] = value; bad["last_observed_job"][key] = value
                cases.append((key+str(number), bad))
        add("job_observation_changed", ["last_observed_job", "total_processes"], 2)
        for key in ("stdout_bytes", "stderr_bytes"):
            for number, value in enumerate((True, -1, 16385)):
                add(key+str(number), ["observed_logs", key], value)
        for key in good:
            bad = deepcopy(good); del bad[key]; cases.append(("missing_"+key, bad))
        for name, bad in cases:
            with self.subTest(case=name), self.assertRaises(ValueError): check(bad)
        many = deepcopy(good)
        many["final_job"]["total_processes"] = many["last_observed_job"]["total_processes"] = 5
        self.assertIsNone(check(many))  # cumulative total is not simultaneous active count
        OBSERVED[self._testMethodName] = dict(refusals=len(cases), nonmutating=True,
                                            cumulative_process_total_not_active_cap=True)

    def test_02_actual_output_bounds_and_nonmutation(self):
        directory = OUTPUT/"own-output"; directory.mkdir(); (directory/"command").mkdir()
        write_new(directory/"command/stdout.txt", b"")
        write_new(directory/"command/stderr.txt", b"x\n")
        for name in ("request.json", "process.json", "refusal.json"):
            write_new(directory/name, b"{}\n")
        report = report_fixture(directory)
        captured = {p.relative_to(directory).as_posix(): p.read_bytes()
                    for p in directory.rglob("*") if p.is_file()}
        calls = []
        def check(value=report, byte_cap=1024**2, entry_cap=32, active=None):
            return CR.validate_output(SUP, directory, value, byte_cap=byte_cap,
                entry_cap=entry_cap, active=active or (lambda: calls.append("active")))
        self.assertIsNone(check()); self.assertTrue(calls)
        self.assertEqual(captured, {p.relative_to(directory).as_posix(): p.read_bytes()
                                   for p in directory.rglob("*") if p.is_file()})
        with self.assertRaises(ValueError): check(byte_cap=1)
        with self.assertRaises(ValueError): check(entry_cap=1)
        altered = deepcopy(report); altered["observed_logs"]["stderr_bytes"] = 1
        with self.assertRaises(ValueError): check(value=altered)
        altered = deepcopy(report); altered["observed_logs"]["stdout_bytes"] = 1
        with self.assertRaises(ValueError): check(value=altered)
        def expired(): raise RuntimeError("TEST_ACTIVE_WITHDRAWAL")
        with self.assertRaisesRegex(RuntimeError, "TEST_ACTIVE_WITHDRAWAL"): check(active=expired)
        OBSERVED[self._testMethodName] = dict(real_ordinary_output=True, input_nonmutation=True,
            byte_and_entry_refusals=True, log_length_refusals=True, active_failure_propagates=True)

    def test_03_terminal_facade_noninterference_and_positive_cache(self):
        f = self.facade_fixture(); client = f.client
        before = dict(client._warrants)
        staged_before = dict(client._staged)
        result = client._admit_evidence(f.packet(b"bad"), f.summary, f.exact,
                                       1, 1, 20, 64, terminal_trial=True)
        self.assertEqual(result["status"], "NOT_ADMITTED"); self.assertNotIn("warrant", result)
        self.assertEqual(client._warrants, before)
        self.assertFalse(client._receipt_cache or client._aggregate_cache or client._packet_cache)
        self.assertEqual(f.charges, [(3, 1)])
        self.assertEqual(client._counts["admission_submissions"], 1)
        self.assertIs(client._session, f.session); self.assertIs(client._context, f.context)
        self.assertIs(client._selection_view, f.view); self.assertIs(client._staged, f.staged)
        self.assertEqual(client._staged, staged_before)
        self.assertEqual(client.receipt._handles, {f.old_handle: b"prior-live-fixture"})
        positive = client._admit_evidence(f.packet(b"good"), f.summary, f.exact,
                                          1, 1, 20, 64, terminal_trial=True)
        self.assertEqual(positive["status"], "ADMITTED")
        calls = list(f.calls); charges = list(f.charges)
        ordinary = client._admit_evidence(f.packet(b"good"), f.summary, f.exact, 1, 1, 20, 64)
        self.assertIs(ordinary, positive["warrant"])
        self.assertEqual(f.calls, calls); self.assertEqual(f.charges, charges)
        self.assertIs(client._warrants[f.old_token], f.old_handle)
        self.assertIs(client._session, f.session); self.assertIs(client._staged, f.staged)
        self.assertEqual(client._staged, staged_before)
        with self.assertRaisesRegex(ValueError, "EXACT_J_MISMATCH"):
            client._admit_evidence(f.packet(b"good"), f.summary,
                                  EXPECTED(f.summary, 1, B.RELATION_IMAGE), 1, 1, 20, 64, terminal_trial=True)
        self.assertEqual(f.calls, calls)
        # Real header/member validation precedes the explicit fake A issuer.
        self.assertIsNone(client._admit_a_member(b"bad", f.header, f.exact, 0, [], 1, 20, 64, trial=True))
        self.assertFalse(client._aggregate_cache)
        calls = list(f.calls)
        corrupted = f.header[:140]+bytes([f.header[140] ^ 1])+f.header[141:]
        with self.assertRaises(ValueError):
            client._admit_a_member(b"good-a", corrupted, f.exact, 0, [], 1, 20, 64, trial=True)
        self.assertEqual(f.calls, calls)
        accepted_a = client._admit_a_member(b"good-a", f.header, f.exact, 0, [], 1, 20, 64, trial=True)
        charges = list(f.charges)
        client._admit_a_member(b"good-a", f.header, f.exact, 0, [], 1, 20, 64)
        self.assertEqual(f.charges, charges); self.assertIn(accepted_a, client._warrants)
        self.assertIs(client._session, f.session); self.assertIs(client._staged, f.staged)
        self.assertEqual(client._staged, staged_before)
        # Only unsupported dispatch is doubled; no fake mixed packet is claimed valid.
        inspect = client._inspect
        client._inspect = lambda raw: ("mixed", f.summary, f.exact, {})
        calls = list(f.calls)
        unsupported = client._admit_evidence(b"explicit-mixed-dispatch-double", f.summary, f.exact,
                                            1, 1, 20, 64, terminal_trial=True)
        self.assertEqual(unsupported["status"], "UNSUPPORTED_TRIAL_FORM")
        self.assertEqual(f.calls, calls); client._inspect = inspect
        OBSERVED[self._testMethodName] = dict(scope="REAL_METHODS_AND_BINDINGS_WITH_EXPLICIT_ISSUER_AUTHORITY_DOUBLES",
            clean_i_and_a_refusal=True, positive_live_cache_dispatch=True, old_state_identity_preserved=True,
            exact_journal_and_member_refusals=True, mixed_dispatch_double=True,
            charged_verification_attempts=len(f.charges), real_verifications=0)

    def test_04_public_trial_dispatch_and_fatal_final_guard(self):
        f = self.facade_fixture(); client = f.client; raw = f.packet(b"bad")
        client._store = lambda method, *args: method(*args)
        client.workspace.packets = SimpleNamespace(get=lambda digest, size: raw,
                                                   inspect=lambda module, value: (f.summary, {}))
        local = MethodType(FE.CommonsClient.try_admit_terminal_local, client)
        result = local(C.summary_id(f.summary), hashlib.sha256(raw).hexdigest(), len(raw),
                       expected_exact_journal=f.exact, receipt_cpu_seconds=1, wall_seconds=20, memory_mib=64)
        self.assertEqual(result["status"], "NOT_ADMITTED"); self.assertFalse(client.fatal)
        observed = []
        async def acquire(candidate, entry, **kwargs):
            observed.append((candidate, entry, kwargs)); return {"status": "NOT_ADMITTED"}
        client._acquire_packet = acquire
        candidate, entry = object(), {"packet_sha256": "22"*32, "packet_bytes": 3}
        for name, offered in (("try_acquire_terminal", True), ("try_acquire_terminal_exact", False)):
            returned = asyncio.run(getattr(FE.CommonsClient, name)(client, candidate, entry,
                expected_exact_journal=f.exact, receipt_cpu_seconds=1, wall_seconds=20, memory_mib=64))
            self.assertEqual(returned["status"], "NOT_ADMITTED")
            self.assertIs(observed[-1][0], candidate)
            self.assertEqual(observed[-1][2]["bodies"], ())
            self.assertIs(observed[-1][2]["terminal_trial"], True)
            self.assertIs(observed[-1][2]["offered"], offered)
        def expired(): raise ValueError("EXPLICIT_FINAL_OWNER_WITHDRAWAL")
        client._active = expired
        with self.assertRaisesRegex(ValueError, "EXPLICIT_FINAL_OWNER_WITHDRAWAL"):
            local(C.summary_id(f.summary), hashlib.sha256(raw).hexdigest(), len(raw),
                  receipt_cpu_seconds=1, wall_seconds=20, memory_mib=64)
        self.assertEqual(len(client.fatal), 1); self.assertFalse(client._busy)
        client._active = lambda: None
        with self.assertRaisesRegex(ValueError, "EXPLICIT_STRICT_ISSUER_REFUSAL"):
            FE.CommonsClient.admit_receipt(client, b"bad", f.summary,
                                         cpu_seconds=1, wall_seconds=20, memory_mib=64)
        self.assertEqual(len(client.fatal), 2)
        # Exercise both *actual* trial wrappers after their final blocking census.
        # State/acquisition remain explicit doubles; no real waiting or expiry.
        for asynchronous in (False, True):
            for mode in ("authority", "deadline", "owner_deadline", "controller_cpu"):
                late = self.facade_fixture(); current = late.client
                current._store = lambda method, *args: method(*args)
                current.workspace.packets = SimpleNamespace(get=lambda digest, size: raw,
                    inspect=lambda module, value: (late.summary, {}))
                current._acquire_packet = acquire
                withdrawn = [False]
                def active(): need(not withdrawn[0], "EXPLICIT_POST_CENSUS_AUTHORITY")
                def census():
                    if mode == "authority": withdrawn[0] = True
                    elif mode == "deadline": current.grant.deadline = time.monotonic()-1
                    elif mode == "owner_deadline": current._origin_owners[0]._deadline = time.monotonic()-1
                    else: current.grant._cpu = time.process_time()-100
                current._active, current._census = active, census
                with self.subTest(asynchronous=asynchronous, mode=mode), self.assertRaises(ValueError):
                    if asynchronous:
                        asyncio.run(FE.CommonsClient.try_acquire_terminal_exact(current, candidate, entry,
                            receipt_cpu_seconds=1, wall_seconds=20, memory_mib=64))
                    else:
                        FE.CommonsClient.try_admit_terminal_local(current, C.summary_id(late.summary),
                            hashlib.sha256(raw).hexdigest(), len(raw), receipt_cpu_seconds=1,
                            wall_seconds=20, memory_mib=64)
                self.assertEqual(len(current.fatal), 1); self.assertFalse(current._busy)
        OBSERVED[self._testMethodName] = dict(scope="REAL_PUBLIC_DECORATORS_WITH_EXPLICIT_STATE_AND_ACQUISITION_DOUBLES",
            local_trial_normal_return=True, offered_exact_dispatch=True,
            final_guard_and_old_api_failures_fatal=True, contexts_not_reset=True,
            post_census_authority_deadline_controller_refusals=8)

    def owner_cases(self, kind):
        clean = self.owner_fixture(kind, "clean"); owner = clean.owner
        before = dict(owner._handles), dict(owner._members), dict(owner._member_cache)
        result = owner.try_receive(b"bad", clean.statement, clean.output,
                                   cpu_seconds=1, wall_seconds=10, memory_mib=64)
        self.assertIsNone(result); self.assertFalse(owner._closed or owner._busy)
        self.assertEqual((owner._handles, owner._members, owner._member_cache), before)
        self.assertEqual(owner._used, [1, 3, 1]); self.assertGreaterEqual(len(clean.fresh), 2)
        self.assertTrue((clean.output/"refusal.json").is_file())
        self.assertFalse((clean.output/"binding.json").exists())
        if kind == "A": self.assertEqual(owner._output_reserved, [3+B.HEADER_BYTES+1024**2, 32])
        cases = ["exit2", "stdout", "overrun", "changed_input", "changed_trust", "late_refusal_io"]
        if kind == "A": cases.append("changed_header")
        for mode in cases:
            f = self.owner_fixture(kind, mode)
            with self.subTest(kind=kind, mode=mode), self.assertRaises(ValueError):
                f.owner.try_receive(b"bad", f.statement, f.output,
                                    cpu_seconds=1, wall_seconds=10, memory_mib=64)
            self.assertTrue(f.owner._closed); self.assertFalse(f.owner._busy or f.owner._handles)
            self.assertEqual(f.owner._used, [1, 3, 1])
            if kind == "A": self.assertFalse(f.owner._members or f.owner._member_cache)
        strict = self.owner_fixture(kind, "strict")
        with self.assertRaises(ValueError):
            strict.owner.receive(b"bad", strict.statement, strict.output,
                                 cpu_seconds=1, wall_seconds=10, memory_mib=64)
        self.assertFalse((strict.output/"refusal.json").exists())
        self.assertEqual(strict.owner._used, [1, 3, 1])
        # Preserve predecessor distinction: strict A revokes; strict I leaves
        # closure to its ordinary client wrapper. Neither silently returns None.
        self.assertEqual(strict.owner._closed, kind == "A")
        return dict(kind=kind, clean_none_retains_registry=True, fatal_cases=cases,
                    strict_contract_preserved=True, all_attempt_charges_retained=True,
                    scope="ACTUAL_OWNER_METHODS_WITH_EXPLICIT_WORKER_AND_TRUST_DOUBLES",
                    actual_child_processes=0, actual_cryptographic_verifications=0)

    def test_05_i_owner_refusal_transition_with_explicit_worker_double(self):
        OBSERVED[self._testMethodName] = self.owner_cases("I")

    def test_06_a_owner_refusal_transition_with_explicit_worker_double(self):
        OBSERVED[self._testMethodName] = self.owner_cases("A")


def main():
    global OUTPUT, CR, SUP, C, B, FE, EP, EC, ENV, EXPECTED, IV, AV
    need(len(sys.argv) == 3 and sys.argv[1] == "--output", "CANDIDATE_CONTROL_OUTPUT")
    OUTPUT = ordinary(Path(sys.argv[2]))
    need(OUTPUT.is_dir() and OUTPUT.is_relative_to(PROJECT) and os.name == "nt"
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize, "CANDIDATE_CONTROL_ISOLATED_WINDOWS")
    SUP = stage(OUTPUT)
    with patch.object(subprocess, "Popen", forbidden), patch.object(os, "system", forbidden):
        from admission import clean_refusal
        from admission import verifier
        from modules import codec
        from aggregate_claims import bindings
        from aggregate_claims import aggregate_admission
        from client import workspace_evidence
        from evidence_network import packet, custody
        from mixed_claims.packet import Envelope
        from delta_claims.claims import expected_journal
        CR = clean_refusal
        C, B, FE, EP, EC, ENV, EXPECTED = codec, bindings, workspace_evidence, packet, custody, Envelope, expected_journal
        IV, AV = verifier, aggregate_admission
        result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(Controls(name) for name in SELECTED))
    passed = result.wasSuccessful() and result.testsRun == len(SELECTED) and not result.skipped and not FORBIDDEN
    report = dict(schema="DMKN_V5_CANDIDATE_ADMISSION_CONTROLS_V1", status="PASS" if passed else "FAIL",
        tests_run=result.testsRun, failures=len(result.failures), errors=len(result.errors), skipped=len(result.skipped),
        selected=list(SELECTED), sources=SOURCE_ROWS, observations=OBSERVED, forbidden_calls=FORBIDDEN,
        scope="REAL_REPORT_OUTPUT_AND_SELECTED_FACADE_METHODS_WITH_EXPLICIT_OWNER_DOUBLES", mathematical_acceptance=False,
        native_calls=0, proof_calls=0, actual_cryptographic_verifications=0,
        owner_method_calls_use_explicit_supervisor_and_trust_doubles=True, source_map_sha256=MAP_SHA)
    write_new(OUTPUT/"candidate-admission-controls-result.json",
              json.dumps(report, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()+b"\n")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
