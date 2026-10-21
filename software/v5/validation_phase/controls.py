"""Real-record, native-free controls for one synchronous validation scope.

Local policy fixtures are not adopted mathematical executables or warrants.
Every counted persisted read delegates to the real selected trust._read.
"""
import ast
from contextlib import ExitStack
from contextvars import copy_context
from copy import deepcopy
import hashlib
import importlib
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import unittest
from unittest.mock import patch

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SOURCE = Path(__file__).resolve().parents[1]
MAP_PATH = PROJECT/"experiments/v5-local-checks/distribution-body-custody-01-input.json"
MAP_SHA = "995525c5cbf2746718cbf583a3e3e401bc56c2f88d1cef8664ffeb1b644454be"
REPLACEMENTS = {
    "v5/admission/pin_phase.py": "76b54eb04fa2a66ec598b8c6d668e675d8bd483809f8fa66448fa7319b82a9ce",
    "v5/admission/trust.py": "c997d2a83ae5246dec9ff30eeca72e405ec0f66c0a307e53e0521eef66fae6d0",
}
OUTPUT = CODE = C = T = PP = None
SOURCE_COPIES = {}
OBSERVED = {}
FORBIDDEN = []


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def stage_sources(output):
    raw = MAP_PATH.read_bytes()
    if sha(raw) != MAP_SHA:
        raise ValueError("BASIS_MAP_CHANGED")
    basis = json.loads(raw)["sdk_sources"]
    if len(basis) != 114:
        raise ValueError("BASIS_MAP_COUNT")
    code = output/"selected-code"
    code.mkdir()
    for logical, row in sorted(basis.items()):
        if logical in REPLACEMENTS:
            path = SOURCE/"validation_phase"/logical[3:]
            expected = REPLACEMENTS[logical]
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
        with target.open("xb") as stream:
            if stream.write(raw) != len(raw):
                raise ValueError("SOURCE_SHORT_WRITE")
        if target.read_bytes() != raw:
            raise ValueError("SOURCE_COPY_CHANGED")
        SOURCE_COPIES[logical] = dict(source=str(path), bytes=len(raw), sha256=sha(raw))
    for name in ("admission", "modules", "client", "mixed_claims"):
        if name in sys.modules:
            raise ValueError("EARLY_PRODUCT_IMPORT")
    sys.path[:0] = [str(code/"v5"), str(code/"portable")]
    return code


def support():
    return {"schema": "DMKN_LOCAL_TRUST_SUPPORT_V1", "identities": {
        "relation_image": "11"*32, "aggregate_image": None,
        "foundation": "22"*32, "policy": "33"*32,
        "receipt_scheme": "resolved-succinct-poseidon2"},
        "roles": {"inert/control.py": {"bytes": 1, "sha256": sha(b"x")}}}


class GuardExpired(RuntimeError):
    pass


class Guard:
    def __init__(self, events, binding=None):
        self.events, self.binding = events, binding
        self.calls, self.now, self.deadline = 0, 0, 10
        self.after = None

    def __call__(self):
        self.calls += 1
        self.events.append("active")
        if self.now >= self.deadline:
            raise GuardExpired("ORIGINAL_RESOURCE_OR_DEADLINE_EXPIRED")
        if self.binding is not None:
            T.check_binding(self.binding)
        if self.after is not None:
            self.after()


class Controls(unittest.TestCase):
    def setUp(self):
        self.root = OUTPUT/self._testMethodName
        self.root.mkdir()
        self.serial, self.reads, self.events = 0, [], []
        self.after_read = None
        self.original_read = T._read

        def counted(path):
            self.reads.append(str(path))
            self.events.append("read:"+str(path))
            result = self.original_read(path)
            if self.after_read is not None:
                self.after_read(path)
            return result

        self.read_patch = patch.object(T, "_read", counted)
        self.read_patch.start()
        self.assertIsNone(PP._CURRENT.get())
        self.assertIsNone(T._VALIDATION_PHASE.get())

    def tearDown(self):
        self.read_patch.stop()
        self.assertIsNone(PP._CURRENT.get())
        self.assertIsNone(T._VALIDATION_PHASE.get())

    def domain(self, label="domain"):
        self.serial += 1
        path = self.root/(label+"-"+str(self.serial))
        identifier = sha(str(path).encode())
        domain = T.TrustDomain.create(path, identifier, support())
        binding = domain.bind()
        return domain, binding, path, identifier

    def reset(self):
        self.reads.clear()
        self.events.clear()

    def observation(self, **value):
        OBSERVED[self._testMethodName] = value

    def assert_denied(self, domain, binding):
        self.assertTrue(domain._denied)
        with self.assertRaisesRegex(C.StructureError, "TRUST_DENIAL_LATCHED"):
            T.check_binding(binding)

    def pin(self):
        self.serial += 1
        path = self.root/("pin-"+str(self.serial))
        path.write_bytes(b"actual immutable fixture pin")
        expected = dict(bytes=path.stat().st_size, sha256=sha(path.read_bytes()))
        calls = []

        def checker(actual):
            self.assertEqual(actual, path)
            calls.append(str(actual))
            self.events.append("pin:"+str(actual))
            raw = actual.read_bytes()
            return dict(bytes=len(raw), sha256=sha(raw))

        return path, expected, checker, calls

    def test_repeated_checks_and_original_active(self):
        domain, binding, unused, unused_id = self.domain()
        second = domain.bind()
        identity = domain.identity()
        self.reset()
        for number in range(17):
            self.assertEqual(T.check_binding((binding, second)[number % 2]), identity)
        outside = len(self.reads)
        self.assertEqual(outside, 17)
        self.reset()
        guard = Guard(self.events)
        with PP.phase(guard):
            for number in range(17):
                result = T.check_binding((binding, second)[number % 2])
                self.assertEqual(result, identity)
                result["domain_id"] = "ff"*32
            self.assertEqual(len(self.reads), 1)
        self.assertEqual(len(self.reads), 2)
        simple_reads = len(self.reads)
        self.reset()
        guard = Guard(self.events, binding)
        path, expected, checker, calls = self.pin()
        with PP.phase(guard):
            for unused in range(17):
                self.assertTrue(PP.check_pin(checker, path, expected))
        self.assertEqual(len(self.reads), 2)
        self.assertEqual(len(calls), 2)
        self.assertGreaterEqual(guard.calls, 38)
        self.observation(outside_reads=outside, simple_phase_reads=simple_reads,
            trust_in_original_active_reads=len(self.reads), original_active_calls=guard.calls,
            pin_checks=len(calls), result_copy_isolated=True)

    def test_independent_domains_and_alias_objects(self):
        first, b1, path1, id1 = self.domain("first")
        second, b2, path2, unused = self.domain("second")
        alias = T.TrustDomain.open(path1, id1, T.support_id(support()))
        ba = alias.bind()
        self.assertEqual(first.identity()["support_id"], second.identity()["support_id"])
        self.reset()
        with PP.phase(Guard(self.events)):
            for unused in range(5):
                for binding in (b1, b2, ba):
                    T.check_binding(binding)
        self.assertEqual(len(self.reads), 6)
        self.assertEqual(self.reads.count(str(path1)), 4)
        self.assertEqual(self.reads.count(str(path2)), 2)
        self.observation(exact_domain_objects=3, persisted_paths=2, real_reads=6)

    def test_per_call_binding_guards(self):
        domain, binding, unused, unused_id = self.domain()
        other, foreign, unused, unused_id = self.domain()
        fake = object.__new__(T.TrustBinding)
        fake._domain = domain
        self.reset()
        with PP.phase(Guard(self.events)):
            original = T.check_binding(binding)
            for bad in (None, object()):
                with self.assertRaisesRegex(C.StructureError, "TRUST_EXACT_REGISTERED_BINDING"):
                    T.check_binding(bad)
            for bad in (foreign, fake):
                with self.assertRaisesRegex(C.StructureError, "TRUST_UNREGISTERED_BINDING"):
                    domain.check(bad)
            self.assertEqual(T.check_binding(binding), original)
            self.assertFalse(domain._denied)
        self.assertEqual(len(self.reads), 2)
        self.observation(refusals=4, original_binding_still_live=True, real_reads=2)

    def test_outside_scope_and_repeated_scopes(self):
        domain, binding, path, unused = self.domain()
        self.reset()
        for unused in range(2):
            with PP.phase(Guard(self.events)):
                T.check_binding(binding)
        T.check_binding(binding)
        self.assertEqual(len(self.reads), 5)
        (path/"WITHDRAWN").write_bytes(b"")
        with self.assertRaisesRegex(C.StructureError, "TRUST_WITHDRAWN"):
            T.check_binding(binding)
        self.assertEqual(len(self.reads), 6)
        with self.assertRaisesRegex(C.StructureError, "TRUST_DENIAL_LATCHED"):
            with PP.phase(Guard(self.events)):
                T.check_binding(binding)
        self.assert_denied(domain, binding)
        self.observation(two_scopes_and_ordinary_reads=5, next_real_read_detected_marker=True)

    def test_nested_scopes_and_body_exceptions(self):
        unused, binding, unused_path, unused_id = self.domain()
        self.reset()
        with PP.phase(Guard(self.events)):
            T.check_binding(binding)
            with PP.phase(Guard(self.events)):
                T.check_binding(binding)
                T.check_binding(binding)
            self.assertEqual(len(self.reads), 3)
            T.check_binding(binding)
        self.assertEqual(len(self.reads), 4)
        self.reset()
        with PP.phase(Guard(self.events)):
            T.check_binding(binding)
            with self.assertRaisesRegex(ValueError, "INNER_BODY_FAILURE"):
                with PP.phase(Guard(self.events)):
                    T.check_binding(binding)
                    raise ValueError("INNER_BODY_FAILURE")
            T.check_binding(binding)
        self.assertEqual(len(self.reads), 3)
        with self.assertRaisesRegex(ValueError, "OUTER_BODY_FAILURE"):
            with PP.phase(Guard(self.events)):
                T.check_binding(binding)
                raise ValueError("OUTER_BODY_FAILURE")
        T.check_binding(binding)
        self.assertEqual(len(self.reads), 5)
        closed_domain, closed_binding, unused_path, unused_id = self.domain("closed-context")
        with PP.phase(Guard(self.events)):
            T.check_binding(closed_binding)
            held_context = copy_context()
        with self.assertRaisesRegex(C.StructureError, "TRUST_PHASE_CLOSED"):
            held_context.run(T.check_binding, closed_binding)
        self.assert_denied(closed_domain, closed_binding)
        self.observation(nested_success_reads=4, nested_body_failure_reads=3,
            subsequent_failed_scope_and_fresh_read=2, contexts_restored=True,
            copied_context_cannot_reuse_closed_phase=True)

    def test_observed_nested_denial_is_not_hidden(self):
        domain, binding, path, unused = self.domain()
        record = path/"ADOPTION.json"
        raw = record.read_bytes()
        self.reset()
        with self.assertRaisesRegex(C.StructureError, "TRUST_DENIAL_LATCHED"):
            with PP.phase(Guard(self.events)):
                T.check_binding(binding)
                record.write_bytes(raw+b"\n")
                with self.assertRaisesRegex(C.StructureError, "TRUST_ADOPTION_CHANGED"):
                    with PP.phase(Guard(self.events)):
                        T.check_binding(binding)
                record.write_bytes(raw)
                self.assert_denied(domain, binding)
        self.assert_denied(domain, binding)
        self.observation(observed_nested_tamper_latched=True, restoration_does_not_revive=True)

    def test_changed_adoption_bytes_and_record_identity(self):
        cases = []
        for kind in ("bytes", "record_identity"):
            domain, binding, path, unused = self.domain(kind)
            record = path/"ADOPTION.json"
            raw, old_key = record.read_bytes(), (record.stat().st_dev, record.stat().st_ino)
            self.reset()
            with self.assertRaisesRegex(C.StructureError, "TRUST_ADOPTION_CHANGED"):
                with PP.phase(Guard(self.events)):
                    T.check_binding(binding)
                    if kind == "bytes":
                        record.write_bytes(raw+b"\n")
                    else:
                        record.rename(path/"original-adoption-preserved.json")
                        record.write_bytes(raw)
                        self.assertNotEqual((record.stat().st_dev, record.stat().st_ino), old_key)
            reads = len(self.reads)
            self.assertEqual(reads, 2)
            record.write_bytes(raw)
            self.assert_denied(domain, binding)
            cases.append(dict(kind=kind, reads=reads, sticky_after_restore=True))
        self.observation(cases=cases)

    def test_changed_in_memory_generation(self):
        cases = []
        for key in ("_path", "_raw", "_directory_key", "_record_key", "_identity"):
            domain, binding, path, unused = self.domain(key)
            original = deepcopy(getattr(domain, key))
            self.reset()
            with self.assertRaisesRegex(C.StructureError, "TRUST_PHASE_GENERATION_CHANGED"):
                with PP.phase(Guard(self.events)):
                    T.check_binding(binding)
                    if key == "_path":
                        domain._path = path/"not-the-original-domain"
                    elif key == "_raw":
                        domain._raw = original+b"\n"
                    elif key == "_identity":
                        domain._identity["domain_id"] = "fe"*32
                    else:
                        setattr(domain, key, (original[0], original[1]+1))
                    T.check_binding(binding)
            setattr(domain, key, original)
            self.assert_denied(domain, binding)
            self.assertEqual(len(self.reads), 1)
            cases.append(key)
        self.observation(changed_generation_fields=cases, all_latched=True)

    def test_persisted_withdrawal_and_pin_sweep_order(self):
        domain, binding, path, unused = self.domain("body-marker")
        self.reset()
        with self.assertRaisesRegex(C.StructureError, "TRUST_WITHDRAWN"):
            with PP.phase(Guard(self.events)):
                T.check_binding(binding)
                (path/"WITHDRAWN").write_bytes(b"partial")
        self.assertEqual(len(self.reads), 2)
        self.assert_denied(domain, binding)
        domain, binding, path, unused = self.domain("pin-final-marker")
        pin_path, expected, real_checker, pin_calls = self.pin()
        def checker(actual):
            value = real_checker(actual)
            if len(pin_calls) == 2:
                (path/"WITHDRAWN").write_bytes(b"")
                self.events.append("marker-during-final-pin")
            return value
        self.reset()
        with self.assertRaisesRegex(C.StructureError, "TRUST_WITHDRAWN"):
            with PP.phase(Guard(self.events)):
                T.check_binding(binding)
                self.assertTrue(PP.check_pin(checker, pin_path, expected))
        self.assertEqual(len(pin_calls), 2)
        self.assertEqual(len(self.reads), 2)
        self.assertLess(self.events.index("marker-during-final-pin"),
                        max(i for i, event in enumerate(self.events) if event.startswith("read:")))
        self.assert_denied(domain, binding)
        self.observation(final_trust_after_pin=True, real_reads=2, pin_checks=2,
            event_trace=list(self.events))

    def test_explicit_withdrawal_immediate(self):
        domain, binding, path, unused = self.domain()
        identity = domain.identity()
        self.reset()
        with self.assertRaisesRegex(C.StructureError, "TRUST_DENIAL_LATCHED"):
            with PP.phase(Guard(self.events)):
                T.check_binding(binding)
                domain.withdraw("selected inert control withdrawal")
                self.assert_denied(domain, binding)
        marker = C.parse_json((path/"WITHDRAWN").read_bytes(), C.Limits(max_bytes=16384))
        self.assertEqual(marker["adoption"], identity)
        self.assertEqual(marker["schema"], "DMKN_LOCAL_TRUST_WITHDRAWN_V1")
        self.assert_denied(domain, binding)
        self.observation(immediate_denial=True, persisted_exact_adoption=True)

    def test_first_read_failure_latches_without_cache(self):
        domain, binding, path, unused = self.domain()
        record = path/"ADOPTION.json"
        raw = record.read_bytes()
        record.rename(path/"missing-record-preserved.json")
        self.reset()
        with self.assertRaises(FileNotFoundError):
            with PP.phase(Guard(self.events)):
                T.check_binding(binding)
        self.assertEqual(len(self.reads), 1)
        record.write_bytes(raw)
        self.assert_denied(domain, binding)
        self.observation(failed_first_read=1, restored_record_not_cached_success=True)

    def test_deadline_hits_and_final_read_cost(self):
        failures = []
        for position in ("cached_hit", "pin_exit", "after_final_read"):
            unused, binding, path, unused_id = self.domain(position)
            pin_path, expected, checker, unused_calls = self.pin()
            guard = Guard(self.events, binding)
            self.reset()
            if position == "after_final_read":
                def cross(actual):
                    if actual == path and self.reads.count(str(path)) == 2:
                        guard.now = guard.deadline
                        self.events.append("clock-crossed-after-real-final-read")
                self.after_read = cross
            try:
                with self.assertRaisesRegex(GuardExpired, "ORIGINAL_RESOURCE_OR_DEADLINE_EXPIRED"):
                    with PP.phase(guard):
                        T.check_binding(binding)
                        self.assertTrue(PP.check_pin(checker, pin_path, expected))
                        if position != "after_final_read":
                            guard.now = guard.deadline
                        if position == "cached_hit":
                            PP.check_pin(checker, pin_path, expected)
            finally:
                self.after_read = None
            self.assertEqual(guard.deadline, 10)
            if position == "after_final_read":
                crossing = self.events.index("clock-crossed-after-real-final-read")
                self.assertIn("active", self.events[crossing+1:])
            T.check_binding(binding)
            failures.append(dict(position=position, reads=len(self.reads),
                original_deadline=guard.deadline, active_calls=guard.calls))
        self.observation(cases=failures, deadline_renewals=0)

    def test_finalization_rejects_new_domain(self):
        unused, binding, path, unused_id = self.domain("first")
        other, other_binding, other_path, unused_id = self.domain("late")
        guard = Guard(self.events, binding)
        final_read_done = [False]
        def signal(actual):
            if actual == path and self.reads.count(str(path)) == 2:
                final_read_done[0] = True
        def late_touch():
            if final_read_done[0]:
                T.check_binding(other_binding)
        self.reset()
        self.after_read, guard.after = signal, late_touch
        try:
            with self.assertRaisesRegex(C.StructureError, "TRUST_PHASE_NEW_DOMAIN_DURING_FINALIZATION"):
                with PP.phase(guard):
                    T.check_binding(binding)
        finally:
            self.after_read = None
        self.assertTrue(final_read_done[0])
        self.assertEqual(self.reads.count(str(other_path)), 0)
        self.assert_denied(other, other_binding)
        self.observation(late_domain_refused=True, late_domain_disk_reads=0)

    def test_pin_conflicts_freshness_and_source_scope(self):
        unused, binding, unused_path, unused_id = self.domain()
        path, expected, checker, calls = self.pin()
        self.reset()
        with self.assertRaisesRegex(PP.PinPhaseError, "PIN_PHASE_EXPECTED_CONFLICT"):
            with PP.phase(Guard(self.events, binding)):
                self.assertTrue(PP.check_pin(checker, path, expected))
                PP.check_pin(checker, path, {**expected, "bytes": expected["bytes"]+1})
        with self.assertRaisesRegex(PP.PinPhaseError, "PIN_PHASE_CHECKER_CONFLICT"):
            with PP.phase(Guard(self.events, binding)):
                self.assertTrue(PP.check_pin(checker, path, expected))
                PP.check_pin(lambda p: checker(p), path, expected)
        with self.assertRaisesRegex(PP.PinPhaseError, "PIN_PHASE_FINAL_PIN_CHANGED"):
            with PP.phase(Guard(self.events, binding)):
                self.assertTrue(PP.check_pin(checker, path, expected))
                path.write_bytes(b"changed fixture")
        before = len(calls)
        with PP.phase(Guard(self.events, binding)):
            self.assertFalse(PP.check_pin(checker, path, expected))
            self.assertFalse(PP.check_pin(checker, path, expected))
        self.assertEqual(len(calls)-before, 2)
        self.assertFalse(PP.check_pin(checker, path, expected))
        tree = ast.parse((CODE/"v5/mixed_claims/imports_atomic.py").read_bytes())
        cls = next(node for node in tree.body if isinstance(node, ast.ClassDef)
                   and node.name == "MixedImportSession")
        live = next(node for node in cls.body if isinstance(node, ast.FunctionDef) and node.name == "_live")
        body = next(node for node in cls.body if isinstance(node, ast.FunctionDef) and node.name == "_live_phase")
        contexts = [ast.unparse(item.context_expr) for node in ast.walk(live)
                    if isinstance(node, ast.With) for item in node.items]
        self.assertIn("PP.phase(self._active)", contexts)
        self.assertFalse(any(isinstance(node, (ast.Await, ast.Yield, ast.YieldFrom))
                             for node in ast.walk(body)))
        calls_in_body = [ast.unparse(node.func) for node in ast.walk(body) if isinstance(node, ast.Call)]
        for name in ("self._active", "owner._check_install", "owner._check_live", "owner._check", "self._snapshot"):
            self.assertIn(name, calls_in_body)
        self.observation(expected_and_checker_conflicts_refused=True, final_pin_change_refused=True,
            failed_pin_not_cached=True, original_synchronous_import_scope_unchanged=True)


SELECTED = (
    "test_repeated_checks_and_original_active",
    "test_independent_domains_and_alias_objects",
    "test_per_call_binding_guards",
    "test_outside_scope_and_repeated_scopes",
    "test_nested_scopes_and_body_exceptions",
    "test_observed_nested_denial_is_not_hidden",
    "test_changed_adoption_bytes_and_record_identity",
    "test_changed_in_memory_generation",
    "test_persisted_withdrawal_and_pin_sweep_order",
    "test_explicit_withdrawal_immediate",
    "test_first_read_failure_latches_without_cache",
    "test_deadline_hits_and_final_read_cost",
    "test_finalization_rejects_new_domain",
    "test_pin_conflicts_freshness_and_source_scope",
)


def forbidden(*args, **kwargs):
    FORBIDDEN.append("FORBIDDEN_NATIVE_OR_NETWORK_CALL")
    raise AssertionError("FORBIDDEN_NATIVE_OR_NETWORK_CALL")


def main():
    global OUTPUT, CODE, C, T, PP
    if len(sys.argv) != 3 or sys.argv[1] != "--output":
        raise ValueError("OUTPUT_REQUIRED")
    OUTPUT = Path(sys.argv[2])
    if not OUTPUT.is_absolute() or not OUTPUT.is_dir() or OUTPUT.is_symlink():
        raise ValueError("EXISTING_ORDINARY_OUTPUT_REQUIRED")
    CODE = stage_sources(OUTPUT)
    suite = unittest.TestSuite(Controls(name) for name in SELECTED)
    with ExitStack() as guard:
        guard.enter_context(patch.object(subprocess, "Popen", forbidden))
        guard.enter_context(patch.object(os, "system", forbidden))
        guard.enter_context(patch.object(socket.socket, "__init__", forbidden))
        C = importlib.import_module("modules.codec")
        T = importlib.import_module("admission.trust")
        PP = importlib.import_module("admission.pin_phase")
        for module, name in ((C, "modules/codec.py"), (T, "admission/trust.py"), (PP, "admission/pin_phase.py")):
            if Path(module.__file__).resolve() != CODE/"v5"/name:
                raise ValueError("SELECTED_MODULE_ORIGIN")
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    passed = result.wasSuccessful() and result.testsRun == len(SELECTED) and not result.skipped and not FORBIDDEN
    report = dict(schema="DMKN_V5_VALIDATION_PHASE_CONTROLS_V1",
        status="PASS" if passed else "FAIL", scope="REAL_LOCAL_TRUST_RECORDS_NOT_MATHEMATICAL_AUTHORITY",
        tests=result.testsRun, failures=len(result.failures), errors=len(result.errors),
        skipped=len(result.skipped), selected=list(SELECTED), observations=OBSERVED,
        sources=SOURCE_COPIES, forbidden_calls=FORBIDDEN,
        native_calls=0, network_calls=0, proof_calls=0, mathematical_acceptance=False)
    with (OUTPUT/"controls-result.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True, separators=(",", ":"), allow_nan=False)
        stream.write("\n")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
