"""Finite inert controls for the selected pin-phase seam; no math-owner import."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest


HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "_selected_pin_phase", HERE/"admission/pin_phase.py")
PP = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PP)
OUTPUT = None
PIN = {"bytes": 7, "sha256": "ab"*32}


class Fixture:
    def __init__(self):
        self.path = (HERE/"never-opened-inert-pin").resolve()
        self.pin = dict(PIN)
        self.checks = 0
        self.active_calls = 0
        self.live = True
        # A stable function identity, as with the actual module-level pin().
        self.checker = self.check

    def check(self, path):
        if path != self.path:
            raise ValueError("UNEXPECTED_INERT_PATH")
        self.checks += 1
        return dict(self.pin)

    def active(self):
        self.active_calls += 1
        if not self.live:
            raise ValueError("ORIGINAL_ACTIVE_FAILURE")


class Controls(unittest.TestCase):
    def test_seventeen_shared_checks_become_two(self):
        f = Fixture()
        with PP.phase(f.active):
            for unused in range(17):
                self.assertTrue(PP.check_pin(f.checker, f.path, PIN))
            self.assertEqual(f.checks, 1)
        self.assertEqual(f.checks, 2)
        self.assertGreaterEqual(f.active_calls, 38)

    def test_no_cross_phase_or_public_call_cache(self):
        f = Fixture()
        with PP.phase(f.active):
            self.assertTrue(PP.check_pin(f.checker, f.path, PIN))
        f.pin["sha256"] = "cd"*32
        with PP.phase(f.active):
            self.assertFalse(PP.check_pin(f.checker, f.path, PIN))
        self.assertFalse(PP.check_pin(f.checker, f.path, PIN))
        self.assertEqual(f.checks, 4)

    def test_final_sweep_detects_changed_bytes(self):
        f = Fixture()
        with self.assertRaisesRegex(PP.PinPhaseError, "FINAL_PIN_CHANGED"):
            with PP.phase(f.active):
                self.assertTrue(PP.check_pin(f.checker, f.path, PIN))
                f.pin["bytes"] += 1
        self.assertFalse(PP.check_pin(f.checker, f.path, PIN))
        self.assertEqual(f.checks, 3)

    def test_nested_success_uses_independent_scope(self):
        f = Fixture()
        with PP.phase(f.active):
            self.assertTrue(PP.check_pin(f.checker, f.path, PIN))
            with PP.phase(f.active):
                self.assertTrue(PP.check_pin(f.checker, f.path, PIN))
                self.assertTrue(PP.check_pin(f.checker, f.path, PIN))
            self.assertEqual(f.checks, 3)
            self.assertTrue(PP.check_pin(f.checker, f.path, PIN))
            self.assertEqual(f.checks, 3)
        self.assertEqual(f.checks, 4)

    def test_nested_failure_and_body_exception_restore_scope(self):
        f = Fixture()
        with PP.phase(f.active):
            self.assertTrue(PP.check_pin(f.checker, f.path, PIN))
            with self.assertRaisesRegex(ValueError, "BODY_FAILURE"):
                with PP.phase(f.active):
                    self.assertTrue(PP.check_pin(f.checker, f.path, PIN))
                    raise ValueError("BODY_FAILURE")
            self.assertEqual(f.checks, 2)
            self.assertTrue(PP.check_pin(f.checker, f.path, PIN))
        self.assertEqual(f.checks, 3)
        with self.assertRaisesRegex(ValueError, "OUTER_FAILURE"):
            with PP.phase(f.active):
                self.assertTrue(PP.check_pin(f.checker, f.path, PIN))
                raise ValueError("OUTER_FAILURE")
        self.assertTrue(PP.check_pin(f.checker, f.path, PIN))
        self.assertEqual(f.checks, 5)

    def test_conflicting_expected_pin_refused(self):
        f = Fixture()
        for key, value in (("bytes", 8), ("sha256", "ef"*32)):
            with self.assertRaisesRegex(PP.PinPhaseError, "EXPECTED_CONFLICT"):
                with PP.phase(f.active):
                    self.assertTrue(PP.check_pin(f.checker, f.path, PIN))
                    PP.check_pin(f.checker, f.path, {**PIN, key: value})

    def test_conflicting_checker_identity_refused(self):
        f = Fixture()
        other = lambda path: f.check(path)
        with self.assertRaisesRegex(PP.PinPhaseError, "CHECKER_CONFLICT"):
            with PP.phase(f.active):
                self.assertTrue(PP.check_pin(f.checker, f.path, PIN))
                PP.check_pin(other, f.path, PIN)
        self.assertEqual(f.checks, 1)

    def test_failed_comparison_not_cached(self):
        f = Fixture()
        f.pin["sha256"] = "00"*32
        with PP.phase(f.active):
            self.assertFalse(PP.check_pin(f.checker, f.path, PIN))
            self.assertFalse(PP.check_pin(f.checker, f.path, PIN))
            f.pin = dict(PIN)
            self.assertTrue(PP.check_pin(f.checker, f.path, PIN))
        self.assertEqual(f.checks, 4)

    def test_active_failure_blocks_cached_hit_and_final_exit(self):
        for final_only in (False, True):
            f = Fixture()
            with self.assertRaisesRegex(ValueError, "ORIGINAL_ACTIVE_FAILURE"):
                with PP.phase(f.active):
                    self.assertTrue(PP.check_pin(f.checker, f.path, PIN))
                    f.live = False
                    if not final_only:
                        PP.check_pin(f.checker, f.path, PIN)
            self.assertEqual(f.checks, 1)
            f.live = True
            self.assertTrue(PP.check_pin(f.checker, f.path, PIN))
            self.assertEqual(f.checks, 2)

    def test_expected_pin_snapshot_is_not_mutable_alias(self):
        f = Fixture()
        supplied = dict(PIN)
        with self.assertRaisesRegex(PP.PinPhaseError, "EXPECTED_CONFLICT"):
            with PP.phase(f.active):
                self.assertTrue(PP.check_pin(f.checker, f.path, supplied))
                supplied["bytes"] += 1
                PP.check_pin(f.checker, f.path, supplied)
        self.assertEqual(f.checks, 1)

    def test_integrated_scope_and_pin_seams_from_source(self):
        # Parse, do not execute/import, the three actual selected SDK successors.
        def method(relative, cls, name):
            tree = ast.parse((HERE/relative).read_bytes())
            owner = next(node for node in tree.body
                         if isinstance(node, ast.ClassDef) and node.name == cls)
            return next(node for node in owner.body
                        if isinstance(node, ast.FunctionDef) and node.name == name)

        def calls(node):
            return [ast.unparse(item.func) for item in ast.walk(node)
                    if isinstance(item, ast.Call)]

        live = method("mixed_claims/imports_atomic.py", "MixedImportSession", "_live")
        contexts = [item for item in ast.walk(live) if isinstance(item, ast.With)]
        self.assertEqual(len(contexts), 1)
        self.assertEqual(ast.unparse(contexts[0].items[0].context_expr),
                         "PP.phase(self._active)")
        self.assertEqual(calls(contexts[0]), ["PP.phase", "self._live_phase"])
        phase = method("mixed_claims/imports_atomic.py", "MixedImportSession", "_live_phase")
        self.assertFalse(any(isinstance(node, (ast.Await, ast.Yield, ast.YieldFrom))
                             for node in ast.walk(phase)))
        for expected in ("self._active", "owner._check_install", "owner._check_live",
                         "owner._check", "self._snapshot"):
            self.assertIn(expected, calls(phase))
        for relative, cls, name in (
                ("admission/verifier.py", "ReceiptVerifier", "_check_install"),
                ("mixed_claims/receiver.py", "MixedDeltaVerifier", "_check")):
            actual = calls(method(relative, cls, name))
            self.assertIn("PP.check_pin", actual)
            self.assertIn("self._active", actual)
        source = (HERE/"admission/verifier.py").read_text(encoding="utf-8")
        self.assertIn('self._pin_phase_origin in self._pins', source)
        self.assertIn('"ADMISSION_PIN_PHASE_SOURCE_ORIGIN"', source)
        self.assertIn('self._manifest_raw', source)


def main():
    global OUTPUT
    if len(sys.argv) != 3 or sys.argv[1] != "--output":
        raise ValueError("OUTPUT_REQUIRED")
    OUTPUT = Path(sys.argv[2])
    if not OUTPUT.is_absolute() or not OUTPUT.is_dir() or OUTPUT.is_symlink():
        raise ValueError("EXISTING_ORDINARY_OUTPUT_REQUIRED")
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
    names = ("admission/pin_phase.py", "admission/verifier.py",
             "mixed_claims/receiver.py", "mixed_claims/imports_atomic.py",
             "test_pin_phase.py")
    report = {
        "status": "PASS" if result.wasSuccessful() else "FAIL",
        "tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
        "scope": "INERT_PIN_PHASE_AND_PARSED_INTEGRATION_NOT_MATH_AUTHORITY",
        "sources": {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                    for name in names},
        "common_pin_calls": 17, "expected_successful_phase_hash_checks": 2,
        "native_calls": 0, "proof_calls": 0, "math_owner_imports": 0,
    }
    with (OUTPUT/"controls.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True, indent=2)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
