"""Native-free finite-hosting contracts; synthetic supervisor evidence only.

Real retained files and owner locks, mocked transport/committed-view lookup.
No process, socket, checker or successful real service/acceptance claim.
Root alone runs this suite under its separately bounded test supervisor.
"""
from contextlib import ExitStack
from copy import deepcopy
import importlib.util
import io
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

if not (os.name == "nt" and sys.dont_write_bytecode and sys.flags.ignore_environment
        and sys.flags.no_site and sys.flags.no_user_site):
    raise RuntimeError("WINDOWS_PYTHON_PROFILE")

INSTALL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(INSTALL / "py"))
import capacity as C
import storage as S
import domains as D
import node as N
import supervise as V
import hosting as H
import inspect_context as I

owner_spec = importlib.util.spec_from_file_location("hosting_test_owner", INSTALL / "manage.py")
OWNER = importlib.util.module_from_spec(owner_spec)
owner_spec.loader.exec_module(OWNER)
if Path(OWNER.__file__).resolve() != INSTALL / "manage.py":
    raise RuntimeError("OWNER_MODULE_ORIGIN")

MODULES = ((C, "capacity"), (S, "storage"), (D, "domains"), (N, "node"),
           (V, "supervise"), (H, "hosting"), (I, "inspect_context"))
for module, name in MODULES:
    if Path(module.__file__).resolve() != INSTALL / "py" / (name + ".py"):
        raise RuntimeError("PRODUCT_MODULE_ORIGIN")


class HostingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parent = H.safe(Path(os.environ.get("DTMKN_TEST_ROOT", "")))
        S.require(parent.is_dir() and not parent.is_relative_to(INSTALL)
                  and not INSTALL.is_relative_to(parent), "EXTERNAL_TEST_ROOT")
        cls.parent = parent

    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="hosting-" + self._testMethodName + "-", dir=self.parent))
        self.scratch, self.state = self.root / "scratch", self.root / "state"
        self.scratch.mkdir()
        self.state.mkdir()
        self.config = {"config_id": "d" * 64, "clients": ["alice"]}
        self.config_path = self.root / "config.json"
        H.save_new(self.config_path, self.config)
        self.domains = SimpleNamespace(scratch=self.scratch, state=self.state, install=INSTALL,
                                       require_write=self.require_write)
        self.grant = {"schema": 1, "profile": H.PROFILE, "id": "supply-one", "config": "d" * 64,
            "client": "alice", "view": "view:" + "e" * 64, "catalog_sha256": "f" * 64,
            "port": 48591, "max_sessions": 2, "seconds": 1, "max_requests": 2, "max_bytes": 1024}
        self.inputs = [{"path": str(self.root / ("synthetic-source-" + str(i))),
                        "bytes": 1, "sha256": str(i % 10) * 64} for i in range(15)]
        self.stack, self.calls, self.mode = ExitStack(), [], "success"
        self.stack.enter_context(patch.object(V, "Transport", self.transport))
        self.stack.enter_context(patch.object(subprocess, "Popen", self.forbidden))
        self.stack.enter_context(patch.object(socket, "socket", self.forbidden))
        self.stack.enter_context(patch.object(I, "load_checker", self.forbidden))
        self.stack.enter_context(patch.object(N.Dispatcher, "checking", self.forbidden))

    def require_write(self, path):
        self.assertTrue(path.is_relative_to(self.scratch) and path != self.scratch)
        return path

    def forbidden(self, *args, **kwargs):
        raise AssertionError("PROCESS_SOCKET_CHECKER_FORBIDDEN")

    def run_host(self, grant=None, inputs=None):
        return H.run_grant(self.config, self.domains, self.config_path, grant or self.grant,
                           inputs or self.inputs, SimpleNamespace())

    def transport(self, python, worker, config, state, cases, runner, limits):
        def call(name, raw):
            request = S.decode(raw)
            self.calls.append(request)
            slots = sorted((self.scratch / "hosting" / "slots").glob("*.json"))
            slot = S.decode(S.read(slots[-1], 16384))
            self.assertEqual(slot["request"], request)
            self.assertEqual(slot["charge"], H.charge(self.grant))
            self.assertFalse((self.scratch / "hosting" / "done" / slots[-1].name).exists())
            if self.mode == "crash_before_receipt":
                raise RuntimeError("SYNTHETIC_CONTROLLER_CRASH")
            directory = cases / name
            directory.mkdir()
            H.save_new(directory / "request.json", request)
            result = {"status": "SERVICE_STOPPED", "session": request["session"], "view": request["view"],
                "catalog_sha256": self.grant["catalog_sha256"], "mathematicalAcceptance": False,
                "native_stages": 0, "observations": {"checker_loaded": False, "native_stages": 0,
                    "mathematicalAcceptance": False, "bind_host": "127.0.0.1", "port": request["port"],
                    "stop_reason": "SESSION_LIMIT", "elapsed_seconds": 1.0, "cpu_seconds": 0.01}}
            if self.mode == "catalog_change":
                result["catalog_sha256"] = "0" * 64
            if self.mode == "service_error":
                result["observations"]["last_error"] = "PEER_UNAVAILABLE"
            H.save_new(directory / "stdout.txt", result)
            stdout = S.encode(result)
            event = {"request_sha256": S.digest(raw), "response_sha256": S.digest(stdout),
                     "checker_loaded": False, "native_stages": 0}
            H.save_new(directory / "event.json", event)
            receipt = {"schema": 1, "name": "serve", "status": "TRANSPORT_COMPLETE", "native_acceptance": False,
                "limits": dict(V.DEFAULTS, **{key: value for key, value in limits.items() if key != "pins"}),
                "wall_limit_seconds": limits["wall_seconds"], "pins": limits["pins"],
                "request_sha256": S.digest(raw), "job_created_before_process": True,
                "attach_resume_returned": True, "direct_child_reaped": True, "final_active_zero": True,
                "job_closed": True, "pid": 1234, "returncode": 0,
                "initial_job": {"active_processes": 0}, "final_job": {"active_processes": 0, "total_processes": 1},
                "files": {name: {"present": True, "bytes": len(data), "sha256": S.digest(data)}
                          for name, data in (("request.json", raw), ("stdout.txt", stdout),
                                             ("event.json", S.encode(event)))}}
            if self.mode == "unquiescent":
                receipt["final_active_zero"] = False
                receipt["final_job"]["active_processes"] = 1
            if self.mode == "wrong_request":
                receipt["request_sha256"] = "0" * 64
            if self.mode == "transport_failure":
                receipt["status"], receipt["returncode"] = "TRANSPORT_FAILED", 1
            if self.mode == "event_row_missing":
                receipt["files"].pop("event.json")
            if self.mode == "event_row_mismatch":
                receipt["files"]["event.json"]["sha256"] = "0" * 64
            H.save_new(directory / "supervisor.json", receipt)
            if self.mode == "crash_after_receipt":
                raise RuntimeError("SYNTHETIC_CONTROLLER_CRASH")
            if self.mode == "transport_failure":
                raise V.SupervisorFailure("SYNTHETIC_TRANSPORT_FAILURE", receipt)
            return {"returncode": 0, "stdout": stdout, "event": event}
        return call

    def test_01_reserve_before_launch_and_exhaustion(self):
        result = self.run_host()
        self.assertEqual(result["status"], "HOST_GRANT_EXHAUSTED")
        self.assertEqual(result["reserved"], result["authorized"])
        self.assertEqual(result["reserved"]["cpu_seconds"], 240)
        self.assertEqual(len(self.calls), 2)
        self.assertEqual(self.run_host(), result)
        self.assertEqual(len(self.calls), 2)

    def test_02_restart_after_receipt_does_not_repeat(self):
        self.mode = "crash_after_receipt"
        with self.assertRaisesRegex(RuntimeError, "SYNTHETIC_CONTROLLER_CRASH"):
            self.run_host()
        self.mode = "success"
        result = self.run_host()
        self.assertEqual(result["status"], "HOST_GRANT_EXHAUSTED")
        self.assertEqual([row["session"] for row in self.calls], ["host-supply-one-0001", "host-supply-one-0002"])

    def test_03_missing_receipt_blocks_restart_and_new_grant(self):
        self.mode = "crash_before_receipt"
        with self.assertRaises(RuntimeError):
            self.run_host()
        self.mode = "success"
        for grant in (self.grant, dict(self.grant, id="another")):
            with self.assertRaises(S.Refusal) as caught:
                self.run_host(grant)
            self.assertEqual(caught.exception.code, "HOST_PRIOR_RECEIPT_MISSING")
        self.assertEqual(len(self.calls), 1)

    def test_04_active_job_blocks_restart(self):
        self.mode = "unquiescent"
        with self.assertRaises(S.Refusal) as caught:
            self.run_host()
        self.assertEqual(caught.exception.code, "HOST_PRIOR_QUIESCENCE_UNCERTAIN")
        self.mode = "success"
        with self.assertRaises(S.Refusal):
            self.run_host()
        self.assertEqual(len(self.calls), 1)

    def test_05_quiescent_failure_halts_without_refund(self):
        self.mode = "transport_failure"
        result = self.run_host()
        self.assertEqual(result["status"], "HOST_HALTED")
        self.assertEqual(result["reserved"]["sessions"], 1)
        self.assertEqual(result["reserved"]["cpu_seconds"], 120)
        self.mode = "success"
        self.assertEqual(self.run_host(), result)
        self.assertEqual(len(self.calls), 1)

    def test_06_changed_grant_or_sources_refuse(self):
        self.run_host()
        for grant in (dict(self.grant, max_sessions=3), dict(self.grant, view="view:other"),
                      dict(self.grant, port=48592)):
            with self.assertRaises(S.Refusal) as caught:
                self.run_host(grant)
            self.assertEqual(caught.exception.code, "HOST_GRANT_CHANGED")
        changed = deepcopy(self.inputs)
        changed[0]["sha256"] = "a" * 64
        with self.assertRaises(S.Refusal):
            self.run_host(inputs=changed)
        self.assertEqual(len(self.calls), 2)

    def test_07_receipt_request_mismatch_blocks(self):
        self.mode = "wrong_request"
        with self.assertRaises(S.Refusal) as caught:
            self.run_host()
        self.assertEqual(caught.exception.code, "HOST_PRIOR_REQUEST_BINDING")
        self.assertEqual(len(self.calls), 1)

    def test_08_wrong_catalog_halts(self):
        self.mode = "catalog_change"
        self.assertEqual(self.run_host()["status"], "HOST_HALTED")
        self.assertEqual(len(self.calls), 1)

    def test_09_service_error_halts(self):
        self.mode = "service_error"
        self.assertEqual(self.run_host()["status"], "HOST_HALTED")
        self.assertEqual(len(self.calls), 1)

    def test_10_controller_lock_blocks_concurrent_writer(self):
        root = self.scratch / "hosting"
        with S.owner_lock(root):
            with self.assertRaises(S.Refusal) as caught:
                self.run_host()
            self.assertEqual(caught.exception.code, "BUSY")
        self.assertEqual(self.calls, [])

    def test_11_grant_schema_and_limits(self):
        self.assertEqual(H.parse_grant(S.encode(self.grant), self.config), self.grant)
        bad = [dict(self.grant, config="0" * 64), dict(self.grant, client="mallory"),
               dict(self.grant, id="../escape"), dict(self.grant, id="con"),
               dict(self.grant, max_sessions=129), dict(self.grant, seconds=True),
               dict(self.grant, seconds=361), dict(self.grant, port=0),
               dict(self.grant, max_bytes=256 * H.MIB + 1), dict(self.grant, extra=1)]
        for value in bad:
            with self.assertRaises(S.Refusal):
                H.parse_grant(S.encode(value), self.config)
        self.assertFalse((self.scratch / "hosting").exists())

    def test_12_committed_view_preflight_is_read_only(self):
        control = SimpleNamespace(record=lambda *args: {"kind": "peer_view", "mathematicalAcceptance": False,
            "catalog": {"sha256": self.grant["catalog_sha256"]}}, close=lambda: None)
        with patch.object(I, "ReadOnlyControl", return_value=control) as constructor:
            H.validate_view(self.config, self.domains, self.grant)
            self.assertEqual(constructor.call_count, 1)
            with self.assertRaises(S.Refusal):
                H.validate_view(self.config, self.domains, dict(self.grant, catalog_sha256="0" * 64))
        self.assertFalse((self.scratch / "hosting").exists())

    def test_13_new_explicit_grant_after_clean_exhaustion(self):
        self.run_host()
        another = dict(self.grant, id="supply-two", max_sessions=1)
        result = self.run_host(another)
        self.assertEqual(result["status"], "HOST_GRANT_EXHAUSTED")
        self.assertEqual(result["reserved"]["sessions"], 1)
        self.assertEqual(len(self.calls), 3)
        self.assertEqual(len(list((self.scratch / "hosting" / "slots").glob("*.json"))), 3)

    def test_14_truncated_reservation_blocks_all_launch(self):
        root = self.scratch / "hosting"
        for name in ("grants", "slots", "done"):
            (root / name).mkdir(parents=True, exist_ok=True)
        with (root / "slots" / "000001.json").open("xb") as stream:
            stream.write(b'{"schema":')
        with self.assertRaises(S.Refusal):
            self.run_host()
        self.assertEqual(self.calls, [])

    def test_15_completed_receipt_missing_blocks(self):
        self.run_host()
        path = self.scratch / "services" / "host-supply-one-0001" / "cases" / "serve" / "supervisor.json"
        path.rename(path.with_name("retained-original-supervisor.json"))
        with self.assertRaises(S.Refusal) as caught:
            self.run_host()
        self.assertEqual(caught.exception.code, "HOST_COMPLETED_RECEIPT_MISSING")
        self.assertEqual(len(self.calls), 2)

    def test_16_completed_receipt_changed_blocks(self):
        self.run_host()
        path = self.scratch / "services" / "host-supply-one-0001" / "cases" / "serve" / "supervisor.json"
        original = V.strict_json(S.read(path, 65536))
        path.rename(path.with_name("retained-original-supervisor.json"))
        H.save_new(path, dict(original, status="TRANSPORT_FAILED"))
        with self.assertRaises(S.Refusal) as caught:
            self.run_host()
        self.assertEqual(caught.exception.code, "HOST_COMPLETED_RECEIPT_CHANGED")
        self.assertEqual(len(self.calls), 2)

    def test_17_missing_event_receipt_row_blocks(self):
        self.mode = "event_row_missing"
        with self.assertRaises(S.Refusal) as caught:
            self.run_host()
        self.assertEqual(caught.exception.code, "HOST_PRIOR_FILE_BINDING")
        self.assertEqual(len(self.calls), 1)

    def test_18_changed_event_receipt_row_blocks(self):
        self.mode = "event_row_mismatch"
        with self.assertRaises(S.Refusal) as caught:
            self.run_host()
        self.assertEqual(caught.exception.code, "HOST_PRIOR_FILE_BINDING")
        self.assertEqual(len(self.calls), 1)

    def test_19_public_host_cli_routes_exact_arguments(self):
        grant_path = self.root / "owner-grant.json"
        H.save_new(grant_path, self.grant)
        result = {"status": "HOST_GRANT_EXHAUSTED", "mathematicalAcceptance": False}
        output = io.BytesIO()
        with patch.object(sys, "argv", [str(INSTALL / "manage.py"), "host", "--config",
                                       str(self.config_path), "--grant", str(grant_path)]), \
                patch.object(sys, "stdout", SimpleNamespace(buffer=output)), \
                patch.object(H, "invoke_host", return_value=result) as invoke:
            self.assertEqual(OWNER.main(), 0)
        self.assertEqual(S.decode(output.getvalue()), result)
        args = invoke.call_args.args[0]
        self.assertEqual((args.command, args.config, args.grant), ("host", self.config_path, grant_path))
        self.assertEqual(invoke.call_args.kwargs, {"owner_entrypoint": INSTALL / "manage.py"})
        self.assertEqual(self.calls, [])

    def tearDown(self):
        self.stack.close()
        H.save_new(self.root / "report.json", {"test": self._testMethodName,
            "synthetic_supervisor_evidence": True, "mocked_transport": True,
            "real_services": 0, "native_executions": 0, "mathematicalAcceptance": False,
            "calls": len(self.calls), "retained": str(self.root)})


if __name__ == "__main__":
    unittest.main()
