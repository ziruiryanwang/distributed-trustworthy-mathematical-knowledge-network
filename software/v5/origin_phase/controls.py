"""Native-free origin-phase controls with real resolves and trust records.

The verifier shells exercise the actual selected _active implementation only.
They have no constructor adoption, executable, receive call or mathematical
handle. Path.resolve counters delegate to the actual original implementation.
"""
import ast
from contextlib import ExitStack
from contextvars import copy_context
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
MAP_PATH = PROJECT/"experiments/v5-local-checks/distribution-validation-01-input.json"
MAP_SHA = "d11abac9a9c5a5ac7d7b22efbf26bb04fcad1e886f19a2195d42060dd44ab565"
REPLACEMENTS = {
    "v5/admission/pin_phase.py": "c00e1259488415b390b651eab307a91ee5db1966a57f4c236ac054c2445bac21",
    "v5/admission/verifier.py": "32289cac1c8db4f8a778f5347c4ba843f5e5510d2891b1b8184cc5e6edfc1d80",
}
OUTPUT = CODE = C = T = PP = V = None
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
            path = SOURCE/"origin_phase"/logical[3:]
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
    def __init__(self, events, owner=None):
        self.events, self.owner = events, owner
        self.calls, self.used, self.cap = 0, 0, 10
        self.after = None

    def __call__(self):
        self.calls += 1
        self.events.append("active")
        if self.used >= self.cap:
            raise GuardExpired("ORIGINAL_CONTROLLER_BUDGET_EXPIRED")
        if self.owner is not None:
            self.owner._active()
        if self.after is not None:
            self.after()


class Controls(unittest.TestCase):
    def setUp(self):
        self.root = OUTPUT/self._testMethodName
        self.root.mkdir()
        self.serial, self.events, self.resolves, self.reads = 0, [], [], []
        self.after_resolve = self.after_read = None
        self.real_resolve = Path.resolve
        self.real_read = T._read
        self.trust_file = T.__file__
        self.trust_origin = self.real_resolve(Path(T.__file__))
        self.watched = {str(Path(T.__file__))}

        def counted_resolve(path, *args, **kwargs):
            key = str(path)
            watched = key in self.watched
            if watched:
                self.resolves.append(key)
                self.events.append("resolve:"+key)
            resolved = self.real_resolve(path, *args, **kwargs)
            if watched and self.after_resolve is not None:
                self.after_resolve(path, resolved)
            return resolved

        def counted_read(path):
            self.reads.append(str(path))
            self.events.append("read:"+str(path))
            result = self.real_read(path)
            if self.after_read is not None:
                self.after_read(path)
            return result

        self.resolve_patch = patch.object(Path, "resolve", counted_resolve)
        self.read_patch = patch.object(T, "_read", counted_read)
        self.resolve_patch.start()
        self.read_patch.start()
        self.assert_scopes_restored()

    def tearDown(self):
        self.resolve_patch.stop()
        self.read_patch.stop()
        self.assertEqual(T.__file__, self.trust_file)
        self.assertIs(sys.modules.get("admission.trust"), T)
        self.assert_scopes_restored()

    def assert_scopes_restored(self):
        self.assertIsNone(PP._CURRENT.get())
        self.assertIsNone(PP._ORIGIN_PHASE.get())
        self.assertIsNone(T._VALIDATION_PHASE.get())

    def reset(self):
        self.events.clear()
        self.resolves.clear()
        self.reads.clear()

    def observation(self, **values):
        OBSERVED[self._testMethodName] = values

    def fixture(self, label):
        self.serial += 1
        path = self.root/(label+"-"+str(self.serial)+".py")
        path.write_bytes(b"# inert origin fixture; never imported\n")
        exact = self.real_resolve(path)
        self.watched.add(str(path))
        return path, exact

    def owner(self, label="domain"):
        self.serial += 1
        path = self.root/(label+"-"+str(self.serial))
        domain = T.TrustDomain.create(path, sha(str(path).encode()), support())
        binding = domain.bind()
        owner = object.__new__(V.ReceiptVerifier)
        owner._closed, owner._busy, owner._handles = False, False, {}
        owner._deadline = V.time.monotonic()+3600
        owner._trust_binding = owner._trust_original_binding = binding
        owner._trust_module, owner._trust_origin = T, self.trust_origin
        owner._trust_identity = domain.identity()
        owner._trust_domain = domain
        # No verifier executable, receive operation or live mathematical handle.
        self.assertNotIn("_executable", owner.__dict__)
        self.assertEqual(owner._handles, {})
        return owner, domain, binding, path

    def pin(self):
        path, unused = self.fixture("pin")
        expected = dict(bytes=path.stat().st_size, sha256=sha(path.read_bytes()))
        calls = []

        def checker(actual):
            self.assertEqual(actual, path)
            calls.append(str(actual))
            self.events.append("pin:"+str(actual))
            raw = actual.read_bytes()
            return dict(bytes=len(raw), sha256=sha(raw))

        return path, expected, checker, calls

    def test_actual_active_reuse_preserves_original_guards(self):
        owner, unused, unused_binding, unused_path = self.owner()
        self.reset()
        for unused in range(17):
            owner._active()
        self.assertEqual(len(self.resolves), 17)
        self.assertEqual(len(self.reads), 17)
        path, expected, checker, pin_calls = self.pin()
        guard = Guard(self.events, owner)
        self.reset()
        with PP.phase(guard):
            for unused in range(17):
                self.assertTrue(PP.check_pin(checker, path, expected))
            self.assertEqual(len(self.resolves), 1)
        self.assertEqual(len(self.resolves), 2)
        self.assertEqual(len(pin_calls), 2)
        # Original phase makes 40 guards; the final-origin sweep adds two.
        self.assertEqual(guard.calls, 42)
        self.assertEqual(len(self.reads), 4)
        self.assertFalse(owner._closed)
        self.assertEqual(owner._handles, {})
        self.observation(ordinary_resolves=17, phased_resolves=2,
            active_callbacks=guard.calls, retained_original_callbacks=40,
            added_final_origin_callbacks=2,
            real_trust_reads=len(self.reads), real_pin_reads=len(pin_calls))

    def test_ordinary_and_separate_scopes_are_fresh(self):
        owner, unused, unused_binding, unused_path = self.owner()
        self.reset()
        for unused in range(2):
            with PP.phase(Guard(self.events, owner)):
                for unused in range(4):
                    owner._active()
        self.assertEqual(len(self.resolves), 4)
        owner._active()
        owner._active()
        self.assertEqual(len(self.resolves), 6)
        self.observation(independent_scopes=2, phase_resolves=4, ordinary_resolves=2)

    def test_positive_only_helper_and_argument_guards(self):
        path, exact = self.fixture("source")
        wrong, unused = self.fixture("wrong")
        self.reset()
        guard = Guard(self.events)
        with PP.phase(guard):
            self.assertFalse(PP.check_origin(str(path), wrong))
            self.assertFalse(PP.check_origin(str(path), wrong))
            self.assertTrue(PP.check_origin(str(path), exact))
            self.assertTrue(PP.check_origin(str(path), exact))
            self.assertEqual(len(self.resolves), 3)
        self.assertEqual(len(self.resolves), 4)
        with self.assertRaisesRegex(PP.PinPhaseError, "ORIGIN_PHASE_INTERNAL_ARGUMENT"):
            PP.check_origin(path, exact)
        with self.assertRaisesRegex(PP.PinPhaseError, "ORIGIN_PHASE_INTERNAL_ARGUMENT"):
            PP.check_origin(str(path), Path("relative-expected.py"))
        self.observation(failed_observations_resolved_twice=True,
            first_success_and_final_resolved=True, real_resolves=4)

    def test_actual_origin_object_registration_and_binding_changes(self):
        cases = []
        wrong, unused = self.fixture("different-real-module")
        for change in ("file", "expected", "module_object", "registration", "binding", "identity"):
            owner, domain, binding, unused_path = self.owner(change)
            other_binding = domain.bind()
            self.reset()
            try:
                with self.assertRaises((C.StructureError, PP.PinPhaseError)):
                    with PP.phase(Guard(self.events, owner)):
                        owner._active()
                        if change == "file":
                            T.__file__ = str(wrong)
                        elif change == "expected":
                            owner._trust_origin = wrong
                        elif change == "module_object":
                            owner._trust_module = object()
                        elif change == "registration":
                            sys.modules["admission.trust"] = object()
                        elif change == "binding":
                            owner._trust_binding = other_binding
                        else:
                            owner._trust_identity = {**owner._trust_identity, "domain_id": "ff"*32}
                        owner._active()
            finally:
                T.__file__ = self.trust_file
                sys.modules["admission.trust"] = T
            self.assertTrue(owner._closed)
            self.assertEqual(owner._handles, {})
            cases.append(dict(change=change, real_resolves=len(self.resolves), revoked=True))
        self.observation(cases=cases, no_issuer_or_binding_check_cached=True)

    def test_unregistered_binding_and_withdrawal_are_not_cached(self):
        cases = []
        for change in ("unregistered", "withdrawn"):
            owner, domain, binding, unused = self.owner(change)
            self.reset()
            with self.assertRaisesRegex(C.StructureError,
                                        "TRUST_UNREGISTERED_BINDING|TRUST_DENIAL_LATCHED"):
                with PP.phase(Guard(self.events, owner)):
                    owner._active()
                    if change == "unregistered":
                        domain._bindings.remove(binding)
                    else:
                        domain.withdraw("inert origin control withdrawal")
                    owner._active()
            self.assertTrue(owner._closed)
            self.assertEqual(len(self.resolves), 1)
            cases.append(dict(change=change, actual_active_refused=True, resolves=1))
        self.observation(cases=cases)

    def test_relative_paths_resolve_on_every_call(self):
        first, second = self.root/"first", self.root/"second"
        first.mkdir(); second.mkdir()
        (first/"origin.py").write_bytes(b"# first\n")
        (second/"origin.py").write_bytes(b"# second\n")
        expected = self.real_resolve(first/"origin.py")
        self.watched.add("origin.py")
        original = Path.cwd()
        self.reset()
        try:
            os.chdir(first)
            with PP.phase(Guard(self.events)):
                self.assertTrue(PP.check_origin("origin.py", expected))
                self.assertTrue(PP.check_origin("origin.py", expected))
                os.chdir(second)
                self.assertFalse(PP.check_origin("origin.py", expected))
                os.chdir(first)
            self.assertEqual(self.resolves.count("origin.py"), 4)
        finally:
            os.chdir(original)
        self.observation(relative_calls=3, actual_relative_resolves=4,
            changed_cwd_refused=True, final_fresh_read=True)

    def test_nested_exceptions_and_closed_copied_context(self):
        path, exact = self.fixture("nested")
        self.reset()
        with PP.phase(Guard(self.events)):
            self.assertTrue(PP.check_origin(str(path), exact))
            with PP.phase(Guard(self.events)):
                self.assertTrue(PP.check_origin(str(path), exact))
                self.assertTrue(PP.check_origin(str(path), exact))
            self.assertEqual(len(self.resolves), 3)
            self.assertTrue(PP.check_origin(str(path), exact))
        self.assertEqual(len(self.resolves), 4)
        self.reset()
        with PP.phase(Guard(self.events)):
            self.assertTrue(PP.check_origin(str(path), exact))
            with self.assertRaisesRegex(ValueError, "BODY_FAILURE"):
                with PP.phase(Guard(self.events)):
                    self.assertTrue(PP.check_origin(str(path), exact))
                    failed_copy = copy_context()
                    raise ValueError("BODY_FAILURE")
            self.assertTrue(PP.check_origin(str(path), exact))
            successful_copy = copy_context()
        self.assertEqual(len(self.resolves), 3)
        for saved in (failed_copy, successful_copy):
            with self.assertRaisesRegex(PP.PinPhaseError, "ORIGIN_PHASE_CLOSED"):
                saved.run(PP.check_origin, str(path), exact)
        self.assertEqual(len(self.resolves), 3)
        self.assertTrue(PP.check_origin(str(path), exact))
        self.assertEqual(len(self.resolves), 4)
        self.observation(nested_success_resolves=4, nested_failure_resolves=3,
            closed_contexts_refused=2, next_ordinary_resolve=True)

    def test_final_origin_follows_pin_and_trust_sweeps(self):
        owner, unused, unused_binding, trust_path = self.owner()
        pin_path, expected, checker, pin_calls = self.pin()
        self.reset()
        with PP.phase(Guard(self.events, owner)):
            self.assertTrue(PP.check_pin(checker, pin_path, expected))
        self.assertEqual(len(pin_calls), 2)
        self.assertEqual(len(self.resolves), 2)
        pin_positions = [i for i, value in enumerate(self.events) if value == "pin:"+str(pin_path)]
        trust_positions = [i for i, value in enumerate(self.events) if value == "read:"+str(trust_path)]
        origin_positions = [i for i, value in enumerate(self.events)
                            if value == "resolve:"+str(Path(self.trust_file))]
        self.assertLess(pin_positions[1], trust_positions[1])
        self.assertLess(trust_positions[1], origin_positions[1])
        self.assertIn("active", self.events[origin_positions[1]+1:])
        self.observation(event_trace=list(self.events), final_order="PIN_THEN_TRUST_THEN_ORIGIN",
            real_trust_reads=len(self.reads), real_origin_resolves=2)

    def test_real_final_origin_change_refuses(self):
        first, second = self.root/"first", self.root/"second"
        first.mkdir(); second.mkdir()
        (first/"origin.py").write_bytes(b"# first\n")
        (second/"origin.py").write_bytes(b"# second\n")
        expected = self.real_resolve(first/"origin.py")
        self.watched.add("origin.py")
        original = Path.cwd()
        self.reset()
        try:
            os.chdir(first)
            with self.assertRaisesRegex(PP.PinPhaseError, "ORIGIN_PHASE_FINAL_ORIGIN_CHANGED"):
                with PP.phase(Guard(self.events)):
                    self.assertTrue(PP.check_origin("origin.py", expected))
                    os.chdir(second)
            self.assertEqual(self.resolves.count("origin.py"), 2)
        finally:
            os.chdir(original)
        self.observation(actual_filesystem_resolution_changed=True,
            no_resolver_return_mock=True, final_success_refused=True, real_resolves=2)

    def test_final_callbacks_cannot_introduce_new_origin(self):
        owner, unused, unused_binding, unused_path = self.owner()
        late, exact = self.fixture("late")
        guard = Guard(self.events, owner)

        def introduce():
            state = PP._ORIGIN_PHASE.get()
            if state is not None and state.finalizing:
                PP.check_origin(str(late), exact)

        guard.after = introduce
        self.reset()
        with self.assertRaisesRegex(PP.PinPhaseError, "ORIGIN_PHASE_NEW_ORIGIN_DURING_FINALIZATION"):
            with PP.phase(guard):
                owner._active()
        self.assertNotIn(str(late), self.resolves)
        self.observation(late_origin_refused_before_resolution=True)

    def test_deadline_and_controller_budget_after_final_resolve(self):
        cases = []
        for point in ("cached_deadline", "final_deadline", "final_controller", "final_withdrawn"):
            owner, domain, unused_binding, unused_path = self.owner(point)
            guard = Guard(self.events, owner)
            self.reset()

            def cross(path, resolved):
                if str(path) == str(Path(self.trust_file)) and len(self.resolves) == 2:
                    if point == "final_deadline":
                        owner._deadline = 0
                    elif point == "final_controller":
                        guard.used = guard.cap
                    elif point == "final_withdrawn":
                        domain.withdraw("inert withdrawal after actual final origin resolve")
                    self.events.append("budget-crossed-after-real-final-resolve")

            self.after_resolve = cross
            try:
                with self.assertRaises((C.StructureError, GuardExpired)):
                    with PP.phase(guard):
                        owner._active()
                        if point == "cached_deadline":
                            owner._deadline = 0
                            owner._active()
            finally:
                self.after_resolve = None
            if point != "cached_deadline":
                self.assertEqual(len(self.resolves), 2)
                cross_at = self.events.index("budget-crossed-after-real-final-resolve")
                self.assertIn("active", self.events[cross_at+1:])
            if point != "final_controller":
                self.assertTrue(owner._closed)
            cases.append(dict(point=point, real_resolves=len(self.resolves), active_calls=guard.calls))
        self.observation(cases=cases, renewed_deadlines_or_budgets=0)

    def test_final_trust_change_and_pin_failure_not_masked(self):
        owner, domain, binding, trust_path = self.owner("withdrawn-at-pin")
        pin_path, expected, original_checker, pin_calls = self.pin()

        def withdraw_at_final_pin(path):
            value = original_checker(path)
            if len(pin_calls) == 2:
                (trust_path/"WITHDRAWN").write_bytes(b"")
            return value

        self.reset()
        with self.assertRaisesRegex(C.StructureError, "TRUST_WITHDRAWN"):
            with PP.phase(Guard(self.events, owner)):
                self.assertTrue(PP.check_pin(withdraw_at_final_pin, pin_path, expected))
        self.assertEqual(len(self.resolves), 1)
        self.assertTrue(domain._denied)
        with self.assertRaisesRegex(C.StructureError, "TRUST_DENIAL_LATCHED"):
            owner._active()
        self.assertTrue(owner._closed)

        owner2, unused, unused_binding, unused_path = self.owner("pin-changed")
        path2, expected2, checker2, calls2 = self.pin()
        self.reset()
        with self.assertRaisesRegex(PP.PinPhaseError, "PIN_PHASE_FINAL_PIN_CHANGED"):
            with PP.phase(Guard(self.events, owner2)):
                self.assertTrue(PP.check_pin(checker2, path2, expected2))
                path2.write_bytes(b"different pin bytes")
        self.assertEqual(len(calls2), 2)
        self.assertEqual(len(self.resolves), 1)
        self.observation(persisted_withdrawal_and_pin_change_refused=True,
            failed_scopes_skip_origin_success_sweep=True)

    def test_module_change_during_final_trust_read_is_observed(self):
        owner, unused, unused_binding, path = self.owner()
        wrong, unused = self.fixture("different-origin-at-trust-tail")

        def mutate_after_final_read(actual):
            if actual == path and self.reads.count(str(path)) == 2:
                T.__file__ = str(wrong)
                self.events.append("module-file-changed-after-final-trust-read")

        self.reset()
        self.after_read = mutate_after_final_read
        try:
            with self.assertRaisesRegex(C.StructureError, "ADMISSION_TRUST_SOURCE_ORIGIN"):
                with PP.phase(Guard(self.events, owner)):
                    owner._active()
        finally:
            self.after_read = None
            T.__file__ = self.trust_file
        self.assertTrue(owner._closed)
        self.assertIn(str(wrong), self.resolves)
        self.observation(changed_current_module_string_resolved_and_refused=True,
            original_module_restored=True)

    def test_resolution_exceptions_and_unchanged_scope_source(self):
        path, exact = self.fixture("exception")

        def fail_after_real_resolution(actual, resolved):
            if actual == path:
                raise OSError("INJECTED_FAILURE_AFTER_ACTUAL_RESOLVE")

        self.reset()
        self.after_resolve = fail_after_real_resolution
        try:
            with PP.phase(Guard(self.events)):
                for unused in range(2):
                    with self.assertRaisesRegex(OSError, "INJECTED_FAILURE_AFTER_ACTUAL_RESOLVE"):
                        PP.check_origin(str(path), exact)
        finally:
            self.after_resolve = None
        self.assertEqual(len(self.resolves), 2)
        self.assertTrue(PP.check_origin(str(path), exact))
        self.assertEqual(len(self.resolves), 3)

        tree = ast.parse((CODE/"v5/admission/pin_phase.py").read_bytes())
        helper = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                      and node.name == "check_origin")
        self.assertFalse(any(isinstance(node, (ast.Await, ast.Yield, ast.YieldFrom))
                             for node in ast.walk(helper)))
        self.assertEqual([item.arg for item in helper.args.args], ["module_file", "expected"])
        self.assertFalse(any(isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                             and node.func.id == "active" for node in ast.walk(helper)))
        original = ast.parse((CODE/"v5/mixed_claims/imports_atomic.py").read_bytes())
        cls = next(node for node in original.body if isinstance(node, ast.ClassDef)
                   and node.name == "MixedImportSession")
        live = next(node for node in cls.body if isinstance(node, ast.FunctionDef) and node.name == "_live")
        contexts = [ast.unparse(item.context_expr) for node in ast.walk(live)
                    if isinstance(node, ast.With) for item in node.items]
        self.assertIn("PP.phase(self._active)", contexts)
        self.observation(injected_post_resolve_errors_not_cached=True, delegated_real_resolves=3,
            helper_has_no_callback_or_async_api=True, existing_import_phase_unchanged=True)


SELECTED = (
    "test_actual_active_reuse_preserves_original_guards",
    "test_ordinary_and_separate_scopes_are_fresh",
    "test_positive_only_helper_and_argument_guards",
    "test_actual_origin_object_registration_and_binding_changes",
    "test_unregistered_binding_and_withdrawal_are_not_cached",
    "test_relative_paths_resolve_on_every_call",
    "test_nested_exceptions_and_closed_copied_context",
    "test_final_origin_follows_pin_and_trust_sweeps",
    "test_real_final_origin_change_refuses",
    "test_final_callbacks_cannot_introduce_new_origin",
    "test_deadline_and_controller_budget_after_final_resolve",
    "test_final_trust_change_and_pin_failure_not_masked",
    "test_module_change_during_final_trust_read_is_observed",
    "test_resolution_exceptions_and_unchanged_scope_source",
)


def forbidden(*args, **kwargs):
    FORBIDDEN.append("FORBIDDEN_NATIVE_OR_NETWORK_CALL")
    raise AssertionError("FORBIDDEN_NATIVE_OR_NETWORK_CALL")


def main():
    global OUTPUT, CODE, C, T, PP, V
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
        V = importlib.import_module("admission.verifier")
        for module, name in ((C, "modules/codec.py"), (T, "admission/trust.py"),
                             (PP, "admission/pin_phase.py"), (V, "admission/verifier.py")):
            if Path(module.__file__).resolve() != CODE/"v5"/name:
                raise ValueError("SELECTED_MODULE_ORIGIN")
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    passed = result.wasSuccessful() and result.testsRun == len(SELECTED) and not result.skipped and not FORBIDDEN
    report = dict(schema="DMKN_V5_ORIGIN_PHASE_CONTROLS_V1", status="PASS" if passed else "FAIL",
        scope="ACTUAL_ACTIVE_REAL_LOCAL_TRUST_RECORDS_NO_MATHEMATICAL_AUTHORITY",
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
