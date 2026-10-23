"""Focused public module CLI controls with explicit inert/mock fixtures.

Load the exact selected package once, then prohibit real owner/custody opens,
database access, child processes, native checking and networking. Synthetic
target IDs test routing/validation only; they do not constitute mathematics.
One original 50 wall / 30 CPU seconds covers loading and every control. Root
selects the package, output and outer containment separately; no execution is
selected by authoring this file.
"""
from __future__ import annotations

import time
START_WALL, START_CPU = time.monotonic(), time.process_time()
import argparse
from contextlib import ExitStack
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
import sqlite3
import stat
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import patch

MIB = 1024**2
PARENT, STORE = "3"*64, "4"*64
FORBIDDEN_ATTEMPTS = []


def need(condition, code):
    if not condition:
        raise AssertionError(code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


class Allowance:
    deadline = START_WALL+50

    def check(self):
        need(time.monotonic() < self.deadline and time.process_time()-START_CPU < 30,
             "MODULE_PUBLIC_CONTROL_ORIGINAL_ALLOWANCE")


def forbidden(label):
    def refuse(*_, **__):
        FORBIDDEN_ATTEMPTS.append(label)
        raise AssertionError("MODULE_PUBLIC_CONTROL_FORBIDDEN:"+label)
    return refuse


def read(path, maximum=2*MIB):
    need(path.is_absolute() and ".." not in path.parts, "MODULE_PUBLIC_CONTROL_ABSOLUTE")
    for part in (*reversed(path.parents), path):
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not
             getattr(info, "st_file_attributes", 0) & 0x400, "MODULE_PUBLIC_CONTROL_REDIRECT")
        need(stat.S_ISDIR(info.st_mode) if part != path else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "MODULE_PUBLIC_CONTROL_REGULAR")
    size = path.stat().st_size
    need(0 < size <= maximum, "MODULE_PUBLIC_CONTROL_FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size and path.stat().st_size == size, "MODULE_PUBLIC_CONTROL_CHANGED")
    return raw


def save(path, value):
    raw = value if type(value) is bytes else json.dumps(value, sort_keys=True,
        ensure_ascii=True, allow_nan=False, separators=(",", ":")).encode("ascii")
    need(0 < len(raw) <= MIB, "MODULE_PUBLIC_CONTROL_OUTPUT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)
    return sha(raw)


def selected_package(args, allowance):
    root = Path(args.package)
    raw = read(root/"PROFILE.json")
    need(sha(raw) == args.profile_sha256, "MODULE_PUBLIC_CONTROL_PROFILE_PIN")
    descriptor = json.loads(raw)
    path, name = root/"owner.py", "_module_public_controls_owner"
    source, pin = read(path), descriptor["files"]["owner.py"]
    need(len(source) == pin["bytes"] and sha(source) == pin["sha256"] and
         name not in sys.modules, "MODULE_PUBLIC_CONTROL_OWNER_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    owner = importlib.util.module_from_spec(spec)
    sys.modules[name] = owner
    exec(compile(source, str(path), "exec"), owner.__dict__)
    loader = owner.bootstrap(root, args.profile_sha256, allowance.check)
    loaded = loader.load(root, args.profile_sha256,
        {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
        allowance.deadline, check_parent=allowance.check)
    need(loaded.module_export.A is loaded.A and loaded.module_export.G is loaded.G and
         loaded.G.A is loaded.A, "MODULE_PUBLIC_CONTROL_SHARED_CORE")
    return owner, loaded


def controls(args, cli, loaded, output, allowance):
    A, G, X, installation = loaded.A, loaded.G, loaded.module_export, loaded.installation
    fixture = output/"fixture"
    fixture.mkdir()
    catalog, custody = fixture/"mock-catalog", fixture/"mock-custody"
    catalog.mkdir(); custody.mkdir()
    name = [[0, {"$bytes": list(part.encode("ascii"))}]
            for part in ("PublicControl", "synthetic")]
    unit = "1"*64
    targets = [{"name": name, "unit_id": unit,
                "export_id": A.S.export_id(installation.semantic_id, unit, name)}]
    limits = {key: bounds[0] for key, bounds in loaded.O.STORE_LIMITS.items()}
    files = {
        "limits.json": limits, "targets.json": targets, "empty.json": [],
        "bad-json.json": b"[", "wrong-shape.json": {},
        "duplicate.json": targets+targets, "too-many.json": targets*33,
        "wrong-identity.json": [dict(targets[0], export_id="0"*64)],
        "too-large.json": b" "*65537,
        "mock-catalog/ADOPTION.json": {"schema": A.P.SCHEMA, "store_id": STORE,
            "implementation": installation.doc["implementation"], "limits": vars(A.P.Limits())}}
    fixture_pins = {key: save(fixture/key, value) for key, value in files.items()}
    destination = fixture/"not-created-export"

    def cli_args(**changes):
        values = dict(operation="export-module", profile_sha256=args.profile_sha256,
            python_runtime=args.python_runtime, lean_runtime=args.lean_runtime,
            catalog=str(catalog), custody=str(custody), store_id=STORE,
            custody_limits=str(fixture/"limits.json"), wall_seconds=50, cpu_seconds=30,
            memory_mib=256, catalog_limits=None, parent_root=PARENT,
            source=None, acquired_targets=None, module_targets=str(fixture/"targets.json"),
            output_names=None, output=str(destination), project_authoring=None,
            project_authoring_sha256=None, candidate=None, candidate_sha256=None,
            supplement=None, supplement_sha256=None, prepared_bindings=None,
            prepared_bindings_sha256=None, retained_contribution=None,
            retained_request_sha256=None, retained_candidate_sha256=None, library_modules=None,
            context_root=None, after_root="", limit=32)
        return SimpleNamespace(**(values | changes))

    def fake_load(*positional, **keywords):
        allowance.check()
        need(positional[:3] == (loaded.root, args.profile_sha256,
             {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime}) and
             positional[3] == cli.START_WALL+50 and callable(keywords["check_parent"]),
             "MODULE_PUBLIC_CONTROL_REUSED_LOADER")
        return loaded

    fake_loader = SimpleNamespace(load=fake_load)

    def fake_bootstrap(*positional):
        allowance.check()
        need(positional[:2] == (loaded.root, args.profile_sha256) and
             callable(positional[2]), "MODULE_PUBLIC_CONTROL_REUSED_BOOTSTRAP")
        return fake_loader

    def invoke(**changes):
        allowance.check()
        with patch.object(cli, "bootstrap", fake_bootstrap):
            result = cli.run(cli_args(**changes))
        allowance.check()
        return result

    def refused(changes, code):
        result = invoke(**changes)
        need(result["ok"] is False and result["phase"] == "SUPPORT" and
             result["error"] == code and result["accepted"] is None and
             result["cost"]["worker_cpu_seconds"] == 0 and
             "result" not in result and "module_export" not in result,
             "MODULE_PUBLIC_CONTROL_PREOPEN_REFUSAL:"+str(result))

    def argument_exclusivity():
        # Exercise the real argument parser without opening state or running CLI main.
        argv = [str(loaded.root/"owner.py"), "export-module"]
        for key, value in vars(cli_args()).items():
            if key != "operation" and value is not None:
                argv.extend(("--"+key.replace("_", "-"), str(value)))
        with patch.object(sys, "argv", argv):
            parsed = cli.arguments()
        need(vars(parsed) == vars(cli_args()), "MODULE_PUBLIC_CONTROL_REAL_ARGUMENT_PARSER")
        cases = [({"module_targets": None}, "OWNER_MODULE_EXPORT_ARGUMENTS"),
            ({"parent_root": None}, "OWNER_OPERATION_ARGUMENTS"),
            ({"output": None}, "OWNER_OPERATION_ARGUMENTS"),
            ({"source": "unused"}, "OWNER_CONTRIBUTION_ARGUMENTS"),
            ({"acquired_targets": "unused"}, "OWNER_CONTRIBUTION_ARGUMENTS"),
            ({"output_names": "unused"}, "OWNER_OUTPUT_NAME_ARGUMENT"),
            ({"candidate": "unused"}, "OWNER_COMPLETION_ARGUMENTS"),
            ({"library_modules": "unused"}, "OWNER_EXTRACTION_ARGUMENTS"),
            ({"project_authoring": "unused", "project_authoring_sha256": "0"*64},
             "OWNER_PROJECT_AUTHORING_ARGUMENTS"),
            ({"catalog_limits": "unused"}, "OWNER_INIT_LIMITS_ONLY"),
            ({"context_root": PARENT}, "OWNER_STATUS_ARGUMENTS_ONLY"),
            ({"operation": "status", "parent_root": None, "output": None},
             "OWNER_MODULE_EXPORT_ARGUMENTS")]
        for changes, code in cases:
            refused(changes, code)

    def targets_before_owner():
        for filename, code in (("empty.json", "OWNER_MODULE_EXPORT_TARGETS_EMPTY"),
                ("bad-json.json", "ADMISSION_WRITER_UNTERMINATED"),
                ("wrong-shape.json", "CONTRIBUTION_ACQUIRED_COUNT"),
                ("duplicate.json", "CONTRIBUTION_DUPLICATE_ACQUIRED"),
                ("too-many.json", "CONTRIBUTION_ACQUIRED_COUNT"),
                ("wrong-identity.json", "CONTRIBUTION_ACQUIRED_EXPORT_BINDING"),
                ("too-large.json", "CATALOG_FILE_BOUND")):
            refused({"module_targets": str(fixture/filename)}, code)

    prototype = {"status": "MOCK_EXPORT_NO_MATHEMATICAL_CHECK",
        "module_name": "DMKNBridge_"+"5"*64, "targets": targets,
        "source_context_root": PARENT, "artifact_parts": {},
        "new_catalog_acceptance": False, "claim": "SYNTHETIC_CONTROL_NO_MODULE_FILES"}

    def mocked(mode, *, measured=0.25, charge=0.25):
        events, forwarded, state = [], [], {"export_complete": False}

        def close_owner():
            events.append("close-owner")
            if mode == "close-failure":
                raise RuntimeError("MOCK_OWNER_CLOSE_FAILURE")

        mock_owner = SimpleNamespace(close=close_owner)
        mock_custody = SimpleNamespace(close=lambda: events.append("close-custody"))

        def open_custody(*positional, **keywords):
            need(positional == (custody, installation.semantic_id, limits) and
                 keywords == {"create": False}, "MODULE_PUBLIC_CONTROL_CUSTODY_FORWARDING")
            events.append("mock-custody")
            return mock_custody

        def open_owner(*positional, **keywords):
            need(positional == (installation, catalog, STORE, mock_custody) and
                 set(keywords) == {"create", "limits"} and keywords["create"] is False and
                 vars(keywords["limits"]) == vars(A.P.Limits()),
                 "MODULE_PUBLIC_CONTROL_OWNER_FORWARDING")
            events.append("mock-owner")
            return mock_owner

        def export(*positional, **keywords):
            allowance.check()
            need(positional == (mock_owner, PARENT, targets) and positional[2] is not targets and
                 set(keywords) == {"output_directory", "profile", "native_source", "worker_script",
                    "parent_deadline", "make_budget", "account_worker_cpu", "check_parent"} and
                 keywords["output_directory"] == destination and keywords["profile"] is loaded.profile and
                 keywords["native_source"] == loaded.root/"module/OrdinaryModule.lean" and
                 keywords["worker_script"] == loaded.root/"module_worker.py" and
                 keywords["parent_deadline"] == cli.START_WALL+50,
                 "MODULE_PUBLIC_CONTROL_EXPORT_FORWARDING")
            for key in ("make_budget", "account_worker_cpu", "check_parent"):
                need(callable(keywords[key]), "MODULE_PUBLIC_CONTROL_CALLBACK:"+key)
            keywords["check_parent"]()
            # Real allowance creation only; no claim/stage/process is invoked.
            budget = keywords["make_budget"]()
            need(type(budget) is A.OperationBudget and not budget.claimed and budget.worker_cpu == 0 and
                 budget.deadline <= keywords["parent_deadline"] and 0 < budget.cpu_seconds < 30 and
                 budget.memory_mib == 256, "MODULE_PUBLIC_CONTROL_DERIVED_ALLOWANCE")
            keywords["account_worker_cpu"](charge/2)
            keywords["account_worker_cpu"](charge/2)
            keywords["check_parent"]()
            forwarded.append("exact-paths-profile-targets-and-original-allowance")
            events.append("mock-export")
            if mode == "export-failure":
                raise X.ModuleExportError("MOCK_NATIVE", RuntimeError("MOCK_EXPORT_FAILURE"),
                                          measured, 0 if measured is not None else charge)
            state["export_complete"] = True
            return copy.deepcopy(prototype)

        original_check = cli.Allowance.check

        def check_with_post_export_failure(current):
            allowance.check()
            original_check(current)
            if state["export_complete"]:
                raise RuntimeError("MOCK_POST_EXPORT_REPORT_FAILURE")

        with ExitStack() as mocks:
            mocks.enter_context(patch.object(loaded.O, "OrdinaryStore", open_custody))
            mocks.enter_context(patch.object(A.OrdinaryAdmission, "open", open_owner))
            mocks.enter_context(patch.object(X, "export_module", export))
            if mode == "report-failure":
                mocks.enter_context(patch.object(cli.Allowance, "check", check_with_post_export_failure))
            result = invoke()
        need(events == ["mock-custody", "mock-owner", "mock-export", "close-owner", "close-custody"] and
             len(forwarded) == 1 and result["cost"]["worker_cpu_seconds"] == charge,
             "MODULE_PUBLIC_CONTROL_ORDER_CLOSURE_AND_MOCK_CHARGE")
        return result

    def success_fields(result):
        payload = result["result"]
        need(all(payload[key] == value for key, value in prototype.items()) and
             payload["module_directory"] == str(destination/"modules") and
             payload["manifest_path"] == str(destination/"MODULE.json") and
             payload["supported_runtime"] == {
                "installation_manifest_sha256": installation.manifest_sha256,
                "implementation_id": installation.implementation_id,
                "lean_runtime": str(installation.runtime_roots["lean_runtime"]),
                "lean_executable": str(installation.path("lean")),
                "lean_executable_pin": installation.doc["files"][installation.doc["roles"]["lean"]],
                "claim": "EXACT_SELECTED_LOCAL_RUNTIME_NOT_DOWNSTREAM_PROJECT_VALIDATION"} and
             result["operation"] == "export-module" and result["profile_sha256"] == args.profile_sha256,
             "MODULE_PUBLIC_CONTROL_PUBLIC_RESULT")

    def forwarding_success():
        result = mocked("success")
        need(result["ok"] is True and "close_errors" not in result,
             "MODULE_PUBLIC_CONTROL_SUCCESS")
        success_fields(result)

    def exporter_failure():
        for measured, charge in ((0.25, 0.25), (None, 0.5)):
            result = mocked("export-failure", measured=measured, charge=charge)
            expected = X.ModuleExportError("MOCK_NATIVE", RuntimeError("MOCK_EXPORT_FAILURE"),
                measured, 0 if measured is not None else charge).report
            need(result["ok"] is False and result["phase"] == "EXPORT_MODULE" and
                 result["accepted"] is None and result["detail"] == expected and
                 "result" not in result and "module_export" not in result and
                 result["retention"] == "EXISTING_ACCEPTED_STATE_AND_ALL_PARTIAL_OUTPUTS_PRESERVED_NO_RETRY",
                 "MODULE_PUBLIC_CONTROL_EXPORT_FAILURE_DETAIL")

    def close_failure():
        result = mocked("close-failure")
        need(result["ok"] is False and result["close_errors"] == [{"component": "owner",
             "error_type": "RuntimeError", "error": "MOCK_OWNER_CLOSE_FAILURE"}],
             "MODULE_PUBLIC_CONTROL_CLOSE_FAILURE")
        success_fields(result)

    def reporting_failure():
        result = mocked("report-failure")
        need(result["ok"] is False and result["phase"] == "EXPORT_MODULE" and
             result["error"] == "MOCK_POST_EXPORT_REPORT_FAILURE" and
             result["module_export"] == prototype and result["accepted"] is None,
             "MODULE_PUBLIC_CONTROL_COMPLETED_EXPORT_RETAINED")

    def preserved_fixture_and_no_output():
        need(not destination.exists() and
             {key: sha(read(fixture/key)) for key in files} == fixture_pins,
             "MODULE_PUBLIC_CONTROL_FIXTURE_PRESERVED_NO_MODULE_OUTPUT")

    return [("real-parser-and-operation-exclusivity", argument_exclusivity),
            ("target-refusals-before-any-owner-open", targets_before_owner),
            ("mock-forwarding-derived-budget-and-public-fields", forwarding_success),
            ("mock-export-failure-measured-and-unknown-charge-detail", exporter_failure),
            ("successful-mock-export-owner-close-failure", close_failure),
            ("successful-mock-export-reporting-failure", reporting_failure),
            ("inert-fixture-preservation-no-module-output", preserved_fixture_and_no_output)]


def main(args):
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "MODULE_PUBLIC_CONTROL_PYTHON")
    allowance, rows = Allowance(), []
    with ExitStack() as guards:
        for obj, method, label in ((sqlite3, "connect", "database"),
                (subprocess, "Popen", "child-process"),
                (socket.socket, "connect", "socket-connect"),
                (socket.socket, "connect_ex", "socket-connect-ex"),
                (socket.socket, "bind", "socket-bind"),
                (socket.socket, "listen", "socket-listen"),
                (socket.socket, "sendto", "socket-sendto")):
            guards.enter_context(patch.object(obj, method, forbidden(label)))
        cli, loaded = selected_package(args, allowance)
        for obj, method, label in ((loaded.O, "OrdinaryStore", "real-custody"),
                (loaded.A.OrdinaryAdmission, "open", "real-owner"),
                (loaded.A.OrdinaryAdmission, "initialize", "initialization"),
                (loaded.A.OrdinaryAdmission, "preflight", "preflight"),
                (loaded.A.OrdinaryAdmission, "admit", "admission"),
                (loaded.module_export, "export_module", "real-module-export"),
                (loaded.installation._supervisor, "supervise", "native-supervision"),
                (loaded.peer_api.H, "exchange", "peer-exchange"),
                (loaded.peer_api.H.Provider, "start", "peer-provider")):
            guards.enter_context(patch.object(obj, method, forbidden(label)))
        output = loaded.A.C.ordinary(Path(args.output), directory=True)
        for protected in (loaded.root, *loaded.installation.runtime_roots.values()):
            need(not output.is_relative_to(protected) and not protected.is_relative_to(output),
                 "MODULE_PUBLIC_CONTROL_OUTPUT_OVERLAP")
        for group, control in controls(args, cli, loaded, output, allowance):
            allowance.check()
            try:
                control(); allowance.check()
                rows.append({"group": group, "ok": True})
            except BaseException as error:
                rows.append({"group": group, "ok": False, "error_type": type(error).__name__,
                             "error": str(error)[:1000]})
        loaded.profile.verify(allowance.check)
    report = {"ok": len(rows) == 7 and all(row["ok"] for row in rows) and not FORBIDDEN_ATTEMPTS,
        "groups": rows, "profile_sha256": args.profile_sha256,
        "implementation_id": loaded.installation.implementation_id,
        "native_operations": 0, "real_owner_opens": 0, "real_custody_opens": 0,
        "forbidden_attempts": FORBIDDEN_ATTEMPTS,
        "mock_worker_charges_are_not_measurements": True,
        "wall_seconds": time.monotonic()-START_WALL,
        "controller_cpu_seconds": time.process_time()-START_CPU,
        "claim": "SYNTHETIC_CLI_AND_EXPLICIT_MOCKS_NOT_NATIVE_EXPORT_OR_MATHEMATICAL_ACCEPTANCE"}
    allowance.check()
    save(output/"PUBLIC-CONTROLS.json", report)
    print(json.dumps(report, sort_keys=True, allow_nan=False), flush=True)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for argument in ("package", "profile-sha256", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+argument, required=True)
    raise SystemExit(main(parser.parse_args()))
