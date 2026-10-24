"""Focused producer-controller controls, never native export or acceptance.

Use real installed codecs, project grammar, profiles, budgets, file operations
and the fresh binder/controller. The supervisor and its native writer response
are explicit doubles. Source locations and executable bytes are a synthetic
package-role fixture, not an installed or executable product. No owner, catalog,
database, real worker, subprocess or network operation is permitted.
"""
from pathlib import Path
import argparse
from contextlib import ExitStack
from dataclasses import replace
import hashlib
import importlib.util
import json
import os
import socket
import sqlite3
import subprocess
import sys
import time
from types import SimpleNamespace as NS
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
PROFILE = "ab04e72440bcd09381a81d4b721d1103fa2e62bc260fa6c0434e6c568419016f"
MIB = 1024**2
START, CPU = time.monotonic(), time.process_time()
FIXTURES = (
    ("ordinary-package-lifecycle-continuation-01/contribution/evidence/"
     "25ae588e95228a64196a576aa9c9dd78249c23b0c26189c5671a434b93afa1b3.json",
     "c7266a3047afcf59059b7884853b4d6b9be4244509f260e78dd072973f9704aa"),
    ("ordinary-package-lifecycle-continuation-01/contribution/evidence/"
     "c4639e6e5f70e259ea1611adba8e168aa74dbfb91f98e2512cd465f82705e61e.json",
     "88c8b3b9da6bfd39fff9c827a1bec8b51ce4289c949c9d7507bfad5e53bc421f"),
    ("ordinary-peer-reciprocal-02/B-contribution/evidence/"
     "d52aed3d1d0f94b8ee2236a7ee84435c983c9523dca0f100f4369c183c3d4e51.json",
     "d0bb18c957c41f3f15d0b47b4eda2f41b8c1f72107d5065929625228a63558ae"),
)


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def check():
    need(time.monotonic()-START < 45 and time.process_time()-CPU < 25,
         "PRODUCTION_CONTROLS_ORIGINAL_ALLOWANCE")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def read(path, maximum=2*MIB):
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) <= maximum, "PRODUCTION_CONTROLS_READ_BOUND")
    return raw


def write(path, raw):
    check()
    need(type(raw) is bytes and len(raw) <= 2*MIB, "PRODUCTION_CONTROLS_WRITE_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)


def module(name, path, expected=None):
    raw = read(path)
    need(expected is None or sha(raw) == expected, "PRODUCTION_CONTROLS_SOURCE_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    exec(compile(raw, str(path), "exec"), value.__dict__)
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--package", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "PRODUCTION_CONTROLS_PROCESS")
    package, output = Path(args.package), Path(args.output)
    need(output.is_absolute() and output.resolve().is_relative_to(LOCAL) and
         output.parent.is_dir() and not os.path.lexists(output), "PRODUCTION_CONTROLS_OUTPUT")
    profile_raw = read(package/"PROFILE.json")
    need(sha(profile_raw) == PROFILE, "PRODUCTION_CONTROLS_PROFILE")
    descriptor = json.loads(profile_raw)
    base = module("_production_control_owner", package/"owner.py",
                  descriptor["files"]["owner.py"]["sha256"])
    loader = base.bootstrap(package, PROFILE, check)
    loaded = loader.load(package, PROFILE, {"python_runtime": Path(r"D:\Python314"),
        "lean_runtime": ROOT/"software/runtime/lean-4.34.0-windows"},
        START+45, check_parent=check)
    source = Path(__file__).resolve().parent
    B = module("baseline_bundle", source/"baseline_bundle.py")
    P = module("_baseline_production_controls_subject", source/"baseline_production.py")
    A, G, X, O = P.A, P.G, P.X, loaded.O
    need(A is loaded.A and G is loaded.G and X is loaded.library_extraction and
         P.B is B and B.E is A.E and B.PE is A.PE, "PRODUCTION_CONTROLS_SHARED_SUPPORT")
    inventory_raw = loaded.installation.read("inventory", MIB)
    inventory = A._writer_json(inventory_raw, MIB)
    raws = []
    for relative, expected in FIXTURES:
        raw = read(LOCAL/relative, MIB)
        need(sha(raw) == expected, "PRODUCTION_CONTROLS_FIXTURE_PIN")
        raws.append(raw)
    raws = tuple(raws)
    items = tuple(A.PE.read_evidence(raw) for raw in raws)
    units = [item.document["unit"] for item in items]
    target = units[-1][2][0][0]
    writer = encoded({"schema": B.WRITER_SCHEMA, "assurance": B.WRITER_ASSURANCE,
        "targets": [target], "basis_names": [row[0] for row in inventory], "units": units,
        "stats": {"source_records": 584, "selected_units": 3,
            "dependency_edges": sum(len(item.document["imports"]) for item in items),
            "scan_nodes": sum(item.census.total_nodes for item in items),
            "unit_json_bytes": sum(len(A.E.canonical_json(unit)) for unit in units)}})
    output.mkdir()
    support, cases_directory, project = output/"synthetic-support", output/"cases", output/"project"
    for path in (support, cases_directory, project):
        path.mkdir()
    py, binary, helpers = support/"py", support/"bin", support/"helpers"
    for path in (py, binary, helpers):
        path.mkdir()
    locations = {P: py/"baseline_production.py", B: py/"baseline_bundle.py",
                 X: py/"library_extraction.py"}
    for imported, destination in locations.items():
        write(destination, read(Path(imported.__file__)))
    worker, executable = py/"baseline_worker.py", binary/"BaselineExporter.exe"
    write(worker, read(source/"baseline_worker.py"))
    # A fixture filename, never an executable or an input to a real subprocess.
    write(executable, b"INERT_NONEXECUTABLE_PRODUCER_ROLE_FIXTURE\n")
    required = set(locations.values()) | {worker, executable}
    required.update(Path(imported.__file__).absolute() for imported in
        (G, G.R, G.B, G.PP, G.R.V1, G.PP.P, X.G, X.B, X.L, X.R, X.X))
    pins = tuple((path, len(data), sha(data)) for path in sorted(required)
                 for data in (read(path),))
    # Real profile verification over a small synthetic support map. It is not
    # adoption of this fixture or a claim that its helper directory can run Lean.
    profile = G.AuthoringProfile(loaded.installation.manifest_sha256, (helpers,), worker, pins)
    project_raw = A.E.canonical_json({"schema": "DMKN_ORDINARY_TRUSTED_PROJECT_EXTRACTION_V1",
        "project_search_paths": [str(project)],
        "modules": [[[0, {"$bytes": list(b"ProductionControl")}]]]})
    cases, forbidden_calls = [], []
    real_supervisor = loaded.installation._supervisor

    def forbidden(*_, **__):
        forbidden_calls.append("FORBIDDEN")
        raise AssertionError("PRODUCTION_CONTROLS_FORBIDDEN_EXTERNAL_OPERATION")

    def run_case(label, *, mode="clean", selected_profile=None, limits=None,
                 spool=160*MIB, expected_error=None, expected_native=1):
        check()
        chosen = profile if selected_profile is None else selected_profile
        limits = B.Limits() if limits is None else limits
        destination = cases_directory/label
        native, writes = [], []
        installation = A.NativeInstallation.__new__(A.NativeInstallation)
        installation.__dict__.update(loaded.installation.__dict__)

        def supervise(argv, cwd, evidence, allowance, job_class):
            check()
            need(cwd == destination and evidence == destination/"supervision" and
                 job_class is forbidden, "PRODUCTION_CONTROLS_SUPERVISOR_ROLE")
            need(argv[:5] == [str(installation.path("python")), "-I", "-S", "-B", str(worker)] and
                 argv[5] == str(installation.runtime_roots["lean_runtime"]) and
                 argv[6:8] == [str(executable.stat().st_size), sha(read(executable))] and
                 argv[8:] == [sha(inventory_raw), sha(read(destination/"request.json"))],
                 "PRODUCTION_CONTROLS_BOUND_NATIVE_COMMAND")
            need(read(destination/"inventory.json") == inventory_raw and
                 read(destination/"project-selection.json") == project_raw,
                 "PRODUCTION_CONTROLS_EXACT_NATIVE_INPUTS")
            native.append({"allowance": dict(allowance), "mode": mode})
            evidence.mkdir()
            real_supervisor.save_new(evidence/"command.json", {"argv": argv, "limits": allowance})
            write(evidence/"stdout.txt", b"")
            write(evidence/"stderr.txt", b"INERT_SUPERVISOR_CONTROL\n")
            if mode not in ("unclean-no-writer", "clean-no-writer"):
                write(destination/"writer.json", writer)
            if mode == "supervisor-exception":
                raise ValueError("INJECTED_SUPERVISOR_ACCOUNTING_LOSS")
            return {"status": "COMMAND_EXITED_ZERO_AND_CLOSED", "child_exit_code":
                    1 if mode == "unclean-no-writer" else 0,
                "direct_child_reaped": True, "job_closed": True, "cleanup_errors": [],
                "termination_requested": False,
                "final_job": {"cpu_seconds": None if mode == "unknown-cpu" else 0.125,
                    "active_processes": 0, "terminated_processes": 0}}

        installation._supervisor = NS(supervise=supervise,
            limits_checked=real_supervisor.limits_checked, save_new=real_supervisor.save_new)
        installation._job_module = NS(Job=forbidden)
        budget = A.OperationBudget(40, 20, 128, active_processes=2, output_bytes=spool)
        original_write = P._write_exact

        def observed_write(path, raw, maximum, checker):
            result = original_write(path, raw, maximum, checker)
            writes.append(Path(path).relative_to(destination).as_posix())
            if mode == "late-manifest" and Path(path).name == "manifest.json":
                raise ValueError("INJECTED_LATE_MANIFEST_UNCERTAINTY")
            return result

        with patch.object(P, "_write_exact", observed_write):
            try:
                result = P.produce_bundle(installation, chosen, project_selection_raw=project_raw,
                    project_selection_sha256=sha(project_raw), targets=[target],
                    output_directory=destination, budget=budget, limits=limits)
                need(expected_error is None, "PRODUCTION_CONTROLS_EXPECTED_FAILURE:"+label)
            except P.ProductionError as error:
                result = error.report
                need(expected_error is not None and expected_error in result["error"],
                     "PRODUCTION_CONTROLS_WRONG_FAILURE:"+label+":"+str(result))
        need(budget.claimed and len(native) == expected_native and result["mathematical_acceptance"] is False,
             "PRODUCTION_CONTROLS_COUNT_AND_AUTHORITY:"+label)
        if not native:
            need(budget.worker_cpu == 0 and not destination.exists() and not writes,
                 "PRODUCTION_CONTROLS_PREFLIGHT_NO_OUTPUT_OR_NATIVE:"+label)
        elif mode in ("unknown-cpu", "supervisor-exception"):
            need(budget.worker_cpu == native[0]["allowance"]["cpu_seconds"] and
                 result["native_accounting_complete"] is False and not (destination/"manifest.json").exists(),
                 "PRODUCTION_CONTROLS_FULL_UNKNOWN_RESERVATION:"+label)
        else:
            need(budget.worker_cpu == 0.125, "PRODUCTION_CONTROLS_KNOWN_CPU_CHARGE:"+label)
        if expected_error is None or mode == "late-manifest":
            manifest_raw = read(destination/"manifest.json")
            manifest = B.read_manifest(manifest_raw, sha(manifest_raw))
            materialized = tuple(read(destination/entry.relative_path) for batch in manifest.batches
                                 for entry in batch)
            need(materialized == raws and writes[-1] == "manifest.json" and
                 all("units/"+item.unit_id+".json" in writes for item in items),
                 "PRODUCTION_CONTROLS_EXACT_UNITS_MANIFEST_LAST:"+label)
            prepared = json.loads(read(destination/"PRODUCTION.json"))
            need(prepared["status"] == "PREPARED_FOR_MANIFEST_WRITE_NOT_COMPLETION" and
                 prepared["mathematical_acceptance"] is False,
                 "PRODUCTION_CONTROLS_SAVED_REPORT_NOT_SUCCESS:"+label)
        if expected_error is None:
            need(result["status"] == "PRODUCED_INERT_BASELINE_NOT_ACCEPTED" and
                 not (destination/"FAILURE.json").exists() and
                 result["manifest"]["sha256"] == sha(read(destination/"manifest.json")),
                 "PRODUCTION_CONTROLS_LIVE_INERT_RESULT")
        elif native:
            failure = json.loads(read(destination/"FAILURE.json"))
            need(failure == result and failure["retry"] == "NONE_NEW_EXPLICIT_OPERATION_REQUIRED",
                 "PRODUCTION_CONTROLS_FAILURE_PRESERVED:"+label)
            if mode == "late-manifest":
                need(failure["manifest_write_attempted"] and failure["manifest_may_exist"] and
                     (destination/"manifest.json").exists(), "PRODUCTION_CONTROLS_MANIFEST_UNCERTAINTY")
            else:
                need(not failure["manifest_write_attempted"] and
                     not (destination/"manifest.json").exists(), "PRODUCTION_CONTROLS_NO_PREMATURE_MANIFEST")
        cases.append({"case": label, "expected_error": expected_error,
            "native_double_calls": len(native), "native_double_events": native,
            "worker_cpu_charge_is_simulated": True, "worker_cpu_charge": budget.worker_cpu,
            "written_payload_order": writes, "result": result})

    with ExitStack() as stack:
        for obj, attribute in ((sqlite3, "connect"), (subprocess, "Popen"), (socket, "socket"),
                (A.OrdinaryAdmission, "open"), (A.OrdinaryAdmission, "_execute"),
                (A.P.PortableCatalog, "open"), (A.P.PortableCatalog, "_commit_checked"),
                (O.OrdinaryStore, "__init__"), (O.OrdinaryStore, "put_evidence")):
            stack.enter_context(patch.object(obj, attribute, forbidden))
        for imported, location in locations.items():
            stack.enter_context(patch.object(imported, "__file__", str(location)))
        run_case("undersized-default-spool", spool=64*MIB, expected_native=0,
                 expected_error="BASELINE_PRODUCTION_SPOOL_RESERVATION")
        run_case("lowered-bind-limit-still-reserves-native-writer", spool=32*MIB,
                 limits=B.Limits(max_writer_bytes=65536, max_bytes=MIB, max_manifest_bytes=65536),
                 expected_native=0, expected_error="BASELINE_PRODUCTION_SPOOL_RESERVATION")
        absent_role = replace(profile, file_pins=tuple(pin for pin in pins if pin[0] != executable))
        run_case("unselected-executable-role", selected_profile=absent_role, expected_native=0,
                 expected_error="BASELINE_PRODUCTION_PACKAGE_ROLES")
        bad_pin = replace(profile, file_pins=tuple((path, size, "0"*64 if path == worker else digest)
                                                 for path, size, digest in pins))
        run_case("worker-pin-mismatch", selected_profile=bad_pin, expected_native=0,
                 expected_error="CONTRIBUTION_PROFILE_CHANGED")
        run_case("one-inert-export-exact-bundle-manifest-last")
        run_case("unknown-native-cpu-keeps-whole-grant", mode="unknown-cpu",
                 expected_error="BASELINE_PRODUCTION_UNKNOWN_CPU_RESERVATION_RETAINED")
        run_case("supervisor-exception-keeps-whole-grant", mode="supervisor-exception",
                 expected_error="INJECTED_SUPERVISOR_ACCOUNTING_LOSS")
        run_case("unclean-native-does-not-read-missing-writer", mode="unclean-no-writer",
                 expected_error="BASELINE_PRODUCTION_NATIVE_EVENT_NOT_CLEAN")
        run_case("clean-native-without-writer-is-not-output", mode="clean-no-writer",
                 expected_error="CATALOG_MISSING_PATH")
        run_case("late-manifest-uncertainty-preserves-files", mode="late-manifest",
                 expected_error="INJECTED_LATE_MANIFEST_UNCERTAINTY")
        need(not forbidden_calls, "PRODUCTION_CONTROLS_NO_FORBIDDEN_SIDE_EFFECT")
    check()
    report = {"status": "PASS_REAL_PRODUCER_CONTROLLER_INERT_NATIVE_DOUBLE", "cases": cases,
        "case_count": len(cases), "forbidden_calls": forbidden_calls, "profile_sha256": PROFILE,
        "mathematical_acceptance": False,
        "scope": "REAL_FILES_PINS_CODECS_BUDGETS_SYNTHETIC_PACKAGE_AND_NATIVE_RESPONSE",
        "not_qualified": "NATIVE_WORKER_EXPORTER_BUILD_EXECUTION_INSTALLATION_OR_ADMISSION",
        "wall_seconds": time.monotonic()-START, "controller_cpu_seconds": time.process_time()-CPU}
    raw = encoded(report)
    need(len(raw) <= MIB, "PRODUCTION_CONTROLS_REPORT_BOUND")
    write(output/"RESULT.json", raw)
    print(json.dumps({"status": report["status"], "case_count": len(cases)}), flush=True)


if __name__ == "__main__":
    main()
