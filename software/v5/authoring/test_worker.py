"""Native-free controls of the owner worker, never a mathematical admission test.

Root selects a fresh --out below experiments. Fixtures and reports are retained;
there is no cleanup, native execution, receipt, positive handle or forged proof.
Every Popen is mocked. Tiny fake executable/DLL bytes test exact file binding only.
"""
from pathlib import Path
from unittest import mock
import argparse
import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
# The supervisor executes an immutable source copy below the evidence directory;
# that copy's ancestors are not the project root or fresh-output authority.
PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
spec = importlib.util.spec_from_file_location("owner_lean_worker", HERE / "worker.py")
worker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(worker)
OUTPUT = None


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def put(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)


def pin(path):
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


class FakeProcess:
    def __init__(self, args, on_wait=None, code=0, timeout=False, cleanup_fails=False):
        self.args, self.on_wait, self.code = args, on_wait, code
        self.timeout, self.cleanup_fails = timeout, cleanup_fails
        self.waits, self.kills, self.complete = [], 0, False

    def wait(self, timeout):
        self.waits.append(timeout)
        if self.kills:
            if self.cleanup_fails:
                raise subprocess.TimeoutExpired(self.args, timeout)
            self.complete = True
            return -9
        if self.timeout:
            raise subprocess.TimeoutExpired(self.args, timeout)
        if self.on_wait:
            self.on_wait()
        self.complete = True
        return self.code

    def kill(self):
        self.kills += 1

    def poll(self):
        return self.code if self.complete else None


class WorkerTests(unittest.TestCase):
    def setUp(self):
        self.case = OUTPUT / self._testMethodName
        self.case.mkdir()
        self.root = self.case / "lean"
        (self.root / "bin").mkdir(parents=True)
        (self.root / "lib/lean").mkdir(parents=True)
        self.operation = self.case / "operation"
        self.operation.mkdir()
        self.exe = self.case / "NeverExecuted.exe"
        self.request = self.operation / "request.json"
        put(self.exe, b"not an executable; mock-only fixture\n")
        put(self.request, b"untrusted worker test request\n")
        runtime = []
        for name in sorted(worker.REQUIRED_DLLS):
            path = self.root / "bin" / name
            put(path, ("mock-only " + name).encode())
            runtime.append(pin(path))
        self.now = 100.0
        self.clock = mock.patch.object(worker.time, "monotonic", side_effect=lambda: self.now)
        self.clock.start()
        self.addCleanup(self.clock.stop)
        self.config = {"schema": worker.SCHEMA, "worker": pin(Path(worker.__file__).resolve()),
                       "executable": pin(self.exe), "lean_root": str(self.root),
                       "runtime_pins": runtime, "request": pin(self.request),
                       "output_directory": str(self.operation / "frontend"),
                       "report_path": str(self.operation / "worker-result.json"),
                       "deadline_monotonic": 130.0}
        self.config_path = self.operation / "worker-config.json"
        # Safety backstop: an unconfigured test can never launch native code.
        self.launch = mock.patch.object(worker.subprocess, "Popen", side_effect=AssertionError("UNMOCKED_NATIVE_CALL"))
        self.Popen = self.launch.start()
        self.addCleanup(self.launch.stop)

    def parse(self, config=None):
        return worker.parse_configuration(encoded(self.config if config is None else config),
                                          worker_path=Path(worker.__file__))

    def persist(self):
        raw = encoded(self.config)
        put(self.config_path, raw)
        return hashlib.sha256(raw).hexdigest()

    def export(self, raw=b'{"untrusted_mock_export":true}'):
        out = Path(self.config["output_directory"])
        out.mkdir()
        put(out / "EXPORT.json", raw)
        # Native has another output; export_bytes must not be called total bytes.
        put(out / "module.ndjson", b"mock-only secondary output\n")

    def install_process(self, **kwargs):
        captured = {}
        def launch(args, **options):
            captured.update(args=args, options=options)
            child = FakeProcess(args, **kwargs)
            captured["child"] = child
            return child
        self.Popen.side_effect = launch
        return captured

    def execute(self):
        sha = self.persist()
        result = worker.run(self.config_path, sha)
        self.assertEqual(result, json.loads(Path(self.config["report_path"]).read_bytes()))
        self.assertFalse(result["mathematical_acceptance"])
        self.assertTrue(result["outer_job_closure_required"])
        return result

    def test_minimal_runtime_and_exact_schema(self):
        self.assertEqual(len(self.parse()["runtime_pins"]), 5)
        extra = copy.deepcopy(self.config)
        extra["arbitrary_command"] = "refused"
        with self.assertRaisesRegex(ValueError, "WORKER_CONFIG_FIELDS"):
            self.parse(extra)
        self.Popen.assert_not_called()

    def test_strict_json_duplicate_and_nonfinite(self):
        for raw, reason in [(b'{"x":1,"x":2}', "WORKER_DUPLICATE_KEY"),
                            (b'{"x":NaN}', "WORKER_NONFINITE_JSON"),
                            (b'{"x":Infinity}', "WORKER_NONFINITE_JSON")]:
            with self.subTest(raw=raw), self.assertRaisesRegex(ValueError, reason):
                worker.strict_json(raw)
        self.Popen.assert_not_called()

    def test_deadline_is_finite_original_and_bounded(self):
        for deadline in [100.0, 99.0, 701.0, True]:
            bad = copy.deepcopy(self.config)
            bad["deadline_monotonic"] = deadline
            with self.subTest(deadline=deadline), self.assertRaisesRegex(ValueError, "WORKER_FINITE_EFFECTIVE_DEADLINE"):
                self.parse(bad)
        self.Popen.assert_not_called()

    def test_self_selection_cannot_be_redirected(self):
        bad = copy.deepcopy(self.config)
        bad["worker"]["path"] = str(self.case / "other-worker.py")
        with self.assertRaisesRegex(ValueError, "WORKER_SELF_SELECTION"):
            self.parse(bad)
        self.Popen.assert_not_called()

    def test_runtime_missing_duplicate_or_foreign_refuses(self):
        missing = copy.deepcopy(self.config)
        missing["runtime_pins"].pop()
        duplicate = copy.deepcopy(self.config)
        duplicate["runtime_pins"].append(duplicate["runtime_pins"][0])
        foreign = copy.deepcopy(self.config)
        foreign["runtime_pins"].append(pin(self.exe))
        for value in [missing, duplicate, foreign]:
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "WORKER_RUNTIME_"):
                self.parse(value)
        self.Popen.assert_not_called()

    def test_conflicting_paths_refuse_before_subprocess(self):
        variants = []
        for field, value in [("output_directory", str(self.request)),
                             ("report_path", str(self.request)),
                             ("report_path", str(self.case / "not-a-sibling.json")),
                             ("output_directory", "relative")]:
            bad = copy.deepcopy(self.config)
            bad[field] = value
            variants.append(bad)
        for bad in variants:
            with self.subTest(config=bad), self.assertRaises(ValueError):
                self.parse(bad)
        self.Popen.assert_not_called()

    def test_config_digest_refuses_before_subprocess(self):
        self.persist()
        with self.assertRaisesRegex(ValueError, "WORKER_CONFIG_PIN"):
            worker.run(self.config_path, "0" * 64)
        self.Popen.assert_not_called()

    def test_wrong_worker_hash_refuses_before_subprocess(self):
        self.config["worker"]["sha256"] = "0" * 64
        report = self.execute()
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["error"], "WORKER_FILE_PIN")
        self.Popen.assert_not_called()

    def test_mutated_input_refuses_before_subprocess(self):
        sha = self.persist()
        # Deliberate same-length input mutation of this fresh test fixture only.
        self.request.write_bytes(b"X" * self.config["request"]["bytes"])
        report = worker.run(self.config_path, sha)
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["error"], "WORKER_FILE_PIN")
        self.Popen.assert_not_called()

    def test_exact_invocation_environment_and_export_binding(self):
        captured = self.install_process(on_wait=self.export)
        with mock.patch.dict(os.environ, {"LEAN_PATH": "bad", "LEAN_SYSROOT": "bad", "CC": "bad", "PATH": "retained"}, clear=True):
            report = self.execute()
        self.assertEqual(captured["args"], [str(self.exe), str(self.request), self.config["output_directory"]])
        options = captured["options"]
        self.assertEqual(set(options), {"cwd", "stdin", "env"})
        self.assertEqual(options["cwd"], str(self.operation))
        self.assertEqual(options["stdin"], subprocess.DEVNULL)
        self.assertEqual(options["env"], {"LEAN_SYSROOT": str(self.root),
                         "PATH": str(self.root / "bin") + os.pathsep + "retained"})
        self.assertEqual(report["status"], "PASS_NATIVE_EXPORT_ONLY")
        self.assertEqual(report["native_logs"], "INHERITED_OUTER_SUPERVISOR")
        raw = (Path(self.config["output_directory"]) / "EXPORT.json").read_bytes()
        self.assertEqual(report["export_sha256"], hashlib.sha256(raw).hexdigest())
        self.assertEqual(report["export_bytes"], len(raw))
        self.assertEqual(report["worker_sha256"], self.config["worker"]["sha256"])
        self.assertEqual(report["deadline_monotonic"], 130.0)
        self.assertEqual(captured["child"].waits, [30.0])

    def test_native_refusal_remains_failure(self):
        captured = self.install_process(code=7)
        report = self.execute()
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["error"], "WORKER_NATIVE_REFUSED")
        self.assertEqual(report["native_return_code"], 7)
        self.assertTrue(report["direct_child_reaped"])
        self.assertEqual(captured["child"].kills, 0)

    def test_timeout_kills_and_reaps_direct_child(self):
        captured = self.install_process(timeout=True)
        report = self.execute()
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["error"], "WORKER_NATIVE_DEADLINE")
        self.assertTrue(report["native_timed_out"])
        self.assertTrue(report["direct_child_reaped"])
        self.assertEqual(captured["child"].kills, 1)
        self.assertEqual(captured["child"].waits, [30.0, 5])

    def test_spawn_latency_does_not_renew_deadline(self):
        captured = {}
        def launch(args, **options):
            self.now = 131.0
            captured["child"] = FakeProcess(args)
            return captured["child"]
        self.Popen.side_effect = launch
        report = self.execute()
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(report["native_timed_out"])
        self.assertEqual(captured["child"].kills, 1)
        self.assertEqual(captured["child"].waits, [5])  # Cleanup only, no renewed native time.
        self.assertEqual(report["deadline_monotonic"], 130.0)

    def test_late_success_is_refused(self):
        def late():
            self.export()
            self.now = 131.0
        self.install_process(on_wait=late)
        report = self.execute()
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["error"], "WORKER_ORIGINAL_DEADLINE")
        self.assertIsNone(report["export_sha256"])

    def test_post_native_input_mutation_is_refused(self):
        def mutate():
            self.export()
            self.request.write_bytes(b"Y" * self.config["request"]["bytes"])
        self.install_process(on_wait=mutate)
        report = self.execute()
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["error"], "WORKER_FILE_PIN")

    def test_post_native_configuration_mutation_is_refused(self):
        def mutate():
            self.export()
            self.config_path.write_bytes(self.config_path.read_bytes() + b" ")
        self.install_process(on_wait=mutate)
        report = self.execute()
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["error"], "WORKER_CONFIG_CHANGED")

    def test_missing_export_is_refused(self):
        self.install_process()
        report = self.execute()
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["error"], "WORKER_EXPORT_FILE_BOUND")

    def test_export_cap_is_enforced(self):
        self.install_process(on_wait=lambda: self.export(b"X" * 17))
        # Reduced test-only ceiling exercises the actual refusal without a16MiB fixture.
        with mock.patch.object(worker, "MAX_EXPORT", 16):
            report = self.execute()
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["error"], "WORKER_EXPORT_FILE_BOUND")

    def test_cleanup_failure_is_not_clean_closure(self):
        self.install_process(timeout=True, cleanup_fails=True)
        report = self.execute()
        self.assertEqual(report["status"], "FAIL")
        self.assertFalse(report["direct_child_reaped"])
        self.assertIn("cleanup_error", report)
        self.assertTrue(report["outer_job_closure_required"])

    def test_report_write_is_exclusive(self):
        target = self.operation / "occupied.json"
        put(target, b"preserve")
        with self.assertRaises(FileExistsError):
            worker.write_report(target, {"test": True})
        self.assertEqual(target.read_bytes(), b"preserve")
        self.Popen.assert_not_called()


def main():
    global OUTPUT
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    OUTPUT = Path(args.out)
    if not (OUTPUT.is_absolute() and OUTPUT.resolve() == OUTPUT
            and OUTPUT.is_relative_to(PROJECT / "experiments") and not OUTPUT.exists()):
        raise ValueError("FRESH_CANONICAL_EXPERIMENT_OUTPUT_REQUIRED")
    OUTPUT.mkdir(parents=True)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(WorkerTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    summary = {"schema": "DMKN_OWNER_LEAN_WORKER_NATIVE_FREE_TEST_V1",
               "status": "PASS" if result.wasSuccessful() else "FAIL",
               "tests_run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
               "native_processes": 0, "mathematical_acceptance": False,
               "worker": pin(Path(worker.__file__).resolve()), "harness": pin(Path(__file__).resolve()),
               "scope": "mocked subprocess control flow and file bindings only; retained fixtures; no real Lean or Job qualification"}
    put(OUTPUT / "RESULT.json", encoded(summary))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
