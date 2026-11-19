"""One diagnostic exported import of the preserved02 snapshot; no acceptance."""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PREFIX = "software/v5/ordinary_baseline/"
LOCAL = ROOT/"experiments/v5-local-checks"
NAME = "ordinary-reference-view-probe-01"
OLD = LOCAL/"ordinary-baseline-native-workflow-02"
BUILD = LOCAL/"ordinary-reference-view-probe-build-01"
MIB = 1024**2
UTILITY_SHA = "4ed662dfdfe04172ce74d2b2f0ad460b4a6ef09bf171eaa27ed9e8abdd72ad56"
FIXED = {
    "RESULT.json": "8461abd6cd7a4d971bb22c9058133fa51065b9eeb24ea383d1d89d9f0e0c8fab",
    "selection.json": "9ed0c25ff7a3ade3a72dfa5889c6a8f6aa48e580b04093e911a4dfa2ffcba9cc",
    "workflow/WORKFLOW-FAILURE.json": "63ed0081ca3c16f74931850dea4510dfab5417afea677be84b9e7ca97dd7b3dd",
    "workflow/inventory.json": "c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0",
    "workflow/test-only-reference-request.json": "638b89e486f3b66e2c9089ac721274351aa29cd48ddb358f00a95faebc1395d2",
    "workflow/snapshot/prepared-manifest.json": "f47f738be2fc3e6497e7cd839d4c9f61674e9c6d951f863105be50877ff21238",
    "workflow/snapshot/replay-request.json": "117e97e8769aa80d5540f059def78b1b923a1317e14f0c654d98948745a599f0",
}
SOURCES = {
    "baseline_snapshot.py": "ab2a0adcdd0b632d14fe2ec7058f9ef496b788760eff4ddd4852d01d11dd3468",
    "snapshot_reopen.py": "74bb337025bacbde6274bf72ca06d37c23e7b16dca46750b333f363c7a1774d7",
    "native_workflow02.py": UTILITY_SHA,
}


def need(ok, code):
    if not ok:
        raise ValueError(code)


def utility(path):
    # This is the frozen helper module only; its workflow main is never called.
    import hashlib
    import importlib.util
    raw = path.read_bytes()
    need(len(raw) <= MIB and hashlib.sha256(raw).hexdigest() == UTILITY_SHA, "PROBE_UTILITY_PIN")
    spec = importlib.util.spec_from_file_location("_probe_frozen_utilities", path)
    H = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = H
    exec(compile(raw, str(path), "exec"), H.__dict__)
    return H


def inspect_build(H, B, authorized, source_sha, check):
    pins = {}

    def pin(path, expected, maximum=128*MIB):
        value = B.pin(B.ordinary(path), check, maximum)
        need(value == expected or value["sha256"] == expected, "PROBE_BUILD_PIN:"+str(path))
        pins[str(path)] = value
        return value

    def document(relative, expected):
        path = BUILD/relative
        value = pin(path, expected, 2*MIB)
        raw = H.read(path)
        need(H.sha(raw) == value["sha256"], "PROBE_BUILD_DOCUMENT_CHANGED")
        return json.loads(raw)

    build = document("build/BUILD.json", authorized["build"])
    result = document("RESULT.json", authorized["result"])
    selection = document("selection.json", authorized["selection"])
    event = result["result"]
    need(result["selection_sha256"] == authorized["selection"] and
         event["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and event["child_exit_code"] == 0 and
         event["job_closed"] is True and event["direct_child_reaped"] is True and
         event["cleanup_errors"] == [] and event["termination_requested"] is False and
         event["final_job"]["active_processes"] == event["final_job"]["terminated_processes"] == 0,
         "PROBE_BUILD_CLEAN_RESULT")
    need(build["schema"] == "DMKN_ORDINARY_REFERENCE_NATIVE_BUILD_V1" and
         build["status"] == "BUILT_CANDIDATE_NOT_INSTALLED_OR_ADOPTED" and
         build["mathematical_acceptance"] is False and
         len(build["completed_commands"]) == 3 and
         all(row["exit_code"] == 0 for row in build["completed_commands"]), "PROBE_BUILD_SCOPE")
    source = build["source"]
    need(source["sha256"] == source_sha and
         Path(source["path"]).name == "ReferenceViewProbe.lean" and
         selection["sources"][PREFIX+"ReferenceViewProbe.lean"] == source_sha, "PROBE_BUILD_SOURCE")
    pin(ROOT/PREFIX/"ReferenceViewProbe.lean", source_sha, MIB)
    pin(Path(source["path"]), {key: source[key] for key in ("bytes", "sha256")}, MIB)
    for path, value in build["inputs"].items():
        pin(Path(path), value, 512*MIB)
    executable = build["executable"]
    path = Path(executable["path"])
    need(path.is_relative_to(BUILD) and path.name == "ReferenceViewProbe.exe", "PROBE_EXECUTABLE_ROLE")
    pin(path, {key: executable[key] for key in ("bytes", "sha256")}, 32*MIB)
    return path, pins


def validate_report(A, report, inventory, request, snapshot):
    expected = [{"name": row[0], "origin": "basis", "expected_kind": row[1]} for row in inventory]
    expected += [{"name": row[0], "origin": "selected", "expected_kind": row[1]}
                 for unit in request["units"] for row in unit["unit"][2]]
    need(set(report) == {"schema", "assurance", "basis_count", "selected_count", "exported_module_count", "exported_module_names",
        "import_count", "frontend_missing", "kernel_missing", "frontend_axioms", "kernel_axioms", "rows"}
        and report["schema"] == "DMKN_ORDINARY_REFERENCE_VIEW_PROBE_V1" and
        report["assurance"] == "DIAGNOSTIC_ONLY_NO_CORRESPONDENCE_OR_ACCEPTANCE", "PROBE_REPORT_FIELDS")
    for field, value in (("basis_count",581), ("selected_count",9), ("import_count",1)):
        need(type(report[field]) is int and report[field] == value, "PROBE_REPORT_CENSUS")
    need(type(report["exported_module_count"]) is int and 1 <= report["exported_module_count"] <= 650,
         "PROBE_REPORT_MODULE_CENSUS")
    names = report["exported_module_names"]
    need(type(names) is list and len(names) == report["exported_module_count"], "PROBE_REPORT_MODULE_NAMES")
    keys = [A.E.name_key(name) for name in names]
    roots = {A.E.name_key(row["module"]) for row in A.E.strict_json(snapshot.root_imports_raw)}
    need(len(set(keys)) == len(keys) and roots <= set(keys) <= set(snapshot.module_keys), "PROBE_REPORT_MODULE_COVERAGE")
    rows = report["rows"]
    need(type(rows) is list and len(rows) == len(expected) == 590, "PROBE_REPORT_ROWS")
    counts = {key: 0 for key in ("frontend_missing", "kernel_missing", "frontend_axioms", "kernel_axioms")}
    kinds = {"axiom", "definition", "theorem", "opaque", "inductive", "constructor", "recursor", "quotient"}
    for row, label in zip(rows, expected):
        need(type(row) is dict and set(row) == {"expected", "frontend", "kernel"} and row["expected"] == label,
             "PROBE_REPORT_EXPECTED_NAME")
        for view in ("frontend", "kernel"):
            facts = row[view]
            need(type(facts) is dict and type(facts.get("present")) is int and facts["present"] in (0,1),
                 "PROBE_REPORT_PRESENCE")
            if not facts["present"]:
                need(set(facts) == {"present"}, "PROBE_REPORT_ABSENT_FIELDS")
                counts[view+"_missing"] += 1
                continue
            need(set(facts) == {"present", "kind", "unsafe", "partial", "group_count", "singleton_group"} and
                 facts["kind"] in kinds and all(type(facts[key]) is int and facts[key] in (0,1)
                 for key in ("unsafe", "partial")), "PROBE_REPORT_PRESENT_FIELDS")
            count, single = facts["group_count"], facts["singleton_group"]
            need((count == "not_applicable" and single == "not_applicable") or (type(count) is int and 0 <= count <= 4096 and
                 type(single) is int and single in (0,1) and (single == 0 or count == 1)),
                 "PROBE_REPORT_GROUP")
            counts[view+"_axioms"] += int(facts["kind"] == "axiom")
    need(all(type(report[key]) is int and report[key] == value for key,value in counts.items()),
         "PROBE_REPORT_COUNTS")
    return counts


def main(args):
    started, cpu = time.monotonic(), time.process_time()
    deadline = started+80
    def check():
        need(time.monotonic() < deadline and time.process_time()-cpu < 40, "PROBE_ORIGINAL_ALLOWANCE")
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "PROBE_PROCESS_CONTEXT")
    source_root = Path(args.source_root)
    need(Path(__file__).resolve() == source_root/PREFIX/"probe_workflow.py", "PROBE_SOURCE_LOCATION")
    H = utility(source_root/PREFIX/"native_workflow02.py")
    B = H.helper()
    output = B.ordinary(Path(args.output), directory=True, fresh=True)
    need(output == LOCAL/NAME/"probe" and Path(sys.executable).resolve() == H.PYTHON/"python.exe",
         "PROBE_LOCATIONS")
    authorized = {key: getattr(args, "build_"+key+"_sha256") for key in ("result", "selection")}
    authorized["build"] = args.build_sha256
    executable, build_pins = inspect_build(H, B, authorized, args.probe_sha256, check)
    for relative,digest in FIXED.items():
        need(B.pin(OLD/relative, check, 2*MIB)["sha256"] == digest, "PROBE_RETAINED_INPUT_PIN")
    for name,digest in SOURCES.items():
        need(B.pin(source_root/PREFIX/name,check,MIB)["sha256"] == digest, "PROBE_SOURCE_PIN")
    profile = H.read(H.PACKAGE/"PROFILE.json")
    need(H.sha(profile) == H.PROFILE, "PROBE_PROFILE")
    descriptor = json.loads(profile)
    owner = H.module("_probe_owner", H.PACKAGE/"owner.py", descriptor["files"]["owner.py"]["sha256"])
    loader = owner.bootstrap(H.PACKAGE,H.PROFILE,check)
    loaded = loader.load(H.PACKAGE,H.PROFILE,{"python_runtime":H.PYTHON,"lean_runtime":H.LEAN},deadline,check_parent=check)
    A = loaded.A
    S = H.module("baseline_snapshot",source_root/PREFIX/"baseline_snapshot.py",SOURCES["baseline_snapshot.py"])
    V = H.module("snapshot_reopen",source_root/PREFIX/"snapshot_reopen.py",SOURCES["snapshot_reopen.py"])
    need(S.A is A and V.A is A and V.S is S, "PROBE_SHARED_CODECS")
    output.mkdir()
    phase = "SNAPSHOT_REVALIDATION"
    def snapshot():
        return V.read_snapshot(OLD/"workflow/snapshot",FIXED["workflow/snapshot/prepared-manifest.json"],
            loaded.installation.manifest_sha256,check_budget=check)
    try:
        before = snapshot()
        inventory_raw = H.read(OLD/"workflow/inventory.json",MIB)
        request_raw = H.read(OLD/"workflow/test-only-reference-request.json",MIB)
        need(inventory_raw == loaded.installation.read("inventory",MIB), "PROBE_FIXED_INVENTORY")
        env = {key:value for key,value in os.environ.items() if not key.upper().startswith(
            ("LEAN","PYTHON","RUST","CARGO","NODE","RISC0")) and key.upper() not in ("PATH","VIRTUAL_ENV")}
        env["PATH"] = str(H.LEAN/"bin")
        report_path = output/"view-report.json"
        argv = [str(executable),str(OLD/"workflow/inventory.json"),str(OLD/"workflow/snapshot/replay-request.json"),
                str(OLD/"workflow/test-only-reference-request.json"),str(report_path)]
        phase = "ONE_EXPORTED_IMPORT"
        event = subprocess.run(argv,cwd=output,env=env,stdin=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW,timeout=max(.001,deadline-time.monotonic()))
        check()
        need(event.returncode == 0, "PROBE_NATIVE_FAILED")
        report_raw = H.read(report_path,MIB)
        report = A._writer_json(report_raw,MIB)
        counts = validate_report(A,report,A._writer_json(inventory_raw,MIB),A.E.strict_json(request_raw),before)
        phase = "FINAL_INPUT_REVALIDATION"
        need(snapshot() == before, "PROBE_SNAPSHOT_CHANGED")
        for relative,digest in FIXED.items():
            need(B.pin(OLD/relative,check,2*MIB)["sha256"] == digest, "PROBE_FINAL_RETAINED_PIN")
        for path,pin in build_pins.items():
            need(B.pin(Path(path),check,512*MIB) == pin, "PROBE_FINAL_BUILD_PIN")
        summary = {"schema":"DMKN_ORDINARY_REFERENCE_VIEW_PROBE_WORKFLOW_V1", "status":"DIAGNOSTIC_COMPLETED",
            "mathematical_acceptance":False,"protected_reference_registered":False,"native_calls":1,
            "snapshot_manifest_sha256":before.manifest_sha256,"report_sha256":H.sha(report_raw),
            "argv":argv,"observations":counts,"wall_seconds":time.monotonic()-started,
            "controller_cpu_seconds":time.process_time()-cpu,"closure_and_inclusive_cpu":"ONLY_OUTER_JOB_RESULT"}
        B.fresh_bytes(output/"PROBE.json",H.encoded(summary))
        need({path.name for path in output.iterdir()} == {"view-report.json","PROBE.json"}, "PROBE_OUTPUT_CENSUS")
        print(json.dumps(summary),flush=True)
    except BaseException as error:
        B.fresh_bytes(output/"PROBE-FAILURE.json",H.encoded({"phase":phase,"error":str(error)[:2048],
            "mathematical_acceptance":False,"retention":"PRESERVED_NO_AUTOMATIC_RETRY"}))
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for name in ("source-root","output","build-sha256","build-result-sha256","build-selection-sha256","probe-sha256"):
        parser.add_argument("--"+name,required=True)
    main(parser.parse_args())
