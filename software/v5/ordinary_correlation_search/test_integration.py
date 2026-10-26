"""One changed-boundary local check: overlay, controls, query CLI, inert kit.

No Lean, source authoring, real mathematical admission, sockets or old campaign.
The independent control suite supplies mechanical query inputs; the actual
installed entry prepares a spec, not a proof. All outputs are fresh and retained.
"""
from __future__ import annotations

import time
START, CPU = time.monotonic(), time.process_time()
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PREFIX = "software/v5/ordinary_correlation_search/"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def check():
    need(time.monotonic() - START < 120 and time.process_time() - CPU < 45,
         "CORRELATION_INTEGRATION_ORIGINAL_ALLOWANCE")


def read(path, maximum=2*MIB):
    check()
    size = path.stat().st_size
    need(0 < size <= maximum, "INTEGRATION_READ_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size, "INTEGRATION_READ_CHANGED")
    return raw


def pin(raw):
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def save(path, value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=False, allow_nan=False).encode("utf-8")
    need(len(raw) <= 2*MIB, "INTEGRATION_SAVE_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)


def child(args, label, tokens, report, timeout=25, result_path=None):
    check()
    need(120 - (time.monotonic() - START) > timeout, "INTEGRATION_NO_CHILD_ROOM")
    argv = [sys.executable, "-I", "-S", "-B", *map(str, tokens)]
    save(args.output / (label + "-COMMAND.json"), {"argv": argv, "cwd": str(ROOT), "timeout": timeout})
    with (args.output / (label + "-stdout.txt")).open("xb") as out, \
            (args.output / (label + "-stderr.txt")).open("xb") as err:
        result = subprocess.run(argv, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=out,
            stderr=err, timeout=timeout, creationflags=subprocess.CREATE_NO_WINDOW)
    need(result.returncode == 0 and (args.output / (label + "-stderr.txt")).stat().st_size == 0,
         label + ":CHILD_FAILED")
    value = json.loads(read(result_path or args.output / (label + "-stdout.txt")))
    report.setdefault("children", {})[label] = {"result": value, "exit_code": result.returncode, "reaped": True}
    return value


def run(args, report):
    selected = args.source_root / PREFIX
    overlay_path = selected / "OVERLAY.json"
    assembled = child(args, "assemble", [selected / "assemble.py", "--source-root", args.source_root,
        "--base-package", args.base_package, "--base-profile-sha256", args.base_profile_sha256,
        "--base-receipt", args.base_receipt, "--base-receipt-sha256", args.base_receipt_sha256,
        "--overlay", overlay_path, "--overlay-sha256", pin(read(overlay_path))["sha256"],
        "--output", args.output / "assembled", "--wall-seconds", "20", "--cpu-seconds", "15"], report)
    package = args.output / "assembled/package"
    old = json.loads(read(args.base_package / "PROFILE.json"))
    profile = json.loads(read(package / "PROFILE.json"))
    overlay = json.loads(read(overlay_path))["files"]
    changed = {"query.py", "run.py", "support/discovery/ordinary_export_adapter.py"}
    need(assembled["files_excluding_profile"] == 154 and assembled["auxiliary_files"] == 117 and
         set(profile["files"]) == set(old["files"]) and
         {name for name in old["files"] if old["files"][name] != profile["files"][name]} == changed,
         "EXACT_THREE_RUNTIME_ROLE_CHANGE")
    need(profile["installation_manifest_sha256"] == old["installation_manifest_sha256"] and
         read(package / "installation/INSTALLATION.json") == read(args.base_package / "installation/INSTALLATION.json"),
         "NATIVE_INSTALLATION_UNCHANGED")
    expected = dict(old["files"])
    install = json.loads(read(package / "installation/INSTALLATION.json"))
    expected.update({"installation/" + name: item for name, item in install["files"].items()
                     if not name.startswith(("python_runtime/", "lean_runtime/"))})
    expected.update(json.loads(read(args.base_receipt))["documentation_files"])
    expected.update(overlay)
    expected["installation/INSTALLATION.json"] = pin(read(package / "installation/INSTALLATION.json"))
    expected["PROFILE.json"] = pin(read(package / "PROFILE.json"))
    actual_names = {path.relative_to(package).as_posix() for path in package.rglob("*") if path.is_file()}
    need(len(expected) == 155 and actual_names == set(expected), "EXACT_PACKAGE_CENSUS")
    for name, expected_pin in expected.items():
        need(pin(read(package / name, 128*MIB)) == expected_pin, "PACKAGE_PIN:" + name)
    report["cases"].append("fresh155-file-package-three-runtime-deltas-no-native-change")
    controls = child(args, "controls", [selected / "test_correlation.py",
        "--source-root", args.source_root, "--package", package,
        "--profile-sha256", assembled["profile_sha256"],
        "--adapter-sha256", overlay["support/discovery/ordinary_export_adapter.py"]["sha256"],
        "--output", args.output / "controls"], report, timeout=35,
        result_path=args.output / "controls/RESULT.json")
    need(controls.get("status") == "PASS", "FOCUSED_CONTROLS_FAILED")
    count = controls["query_fixture"]["context_count"]
    need(type(count) is int and 0 <= count <= 4096, "CONTROL_QUERY_COUNT")
    query_output = args.output / "public-query"
    launched = child(args, "query", [package / "run.py", "--profile-sha256", assembled["profile_sha256"],
        "--python-runtime", args.python_runtime, "--lean-runtime", args.lean_runtime,
        "--diagnostics", args.output / "query-diagnostics", "--wall-seconds", "35", "--cpu-seconds", "15",
        "--memory-mib", "512", "--active-processes", "3", "--stdout-bytes", str(MIB),
        "--stderr-bytes", str(MIB), "query", "--native-type", args.output / "controls/query-native.json",
        "--bindings", args.output / "controls/query-bindings.json", "--conclusion-context-binders", str(count),
        "--output", query_output], report, timeout=45)
    result = json.loads(read(query_output / "RESULT.json"))
    specs = json.loads(read(query_output / "SPECS.json"))
    index_case = next(item["detail"] for item in controls["groups"]
                      if item["case"] == "retained_type_independent_goal_and_same_feature_nonmatch")
    namespace_case = next(item["detail"] for item in controls["groups"]
                          if item["case"] == "fresh_namespace_exact_mode_and_complete_record_binding")
    need(launched.get("ok") is True and result.get("ok") is True and
         result.get("mathematical_acceptance") is False and result["search_mode"] == "conclusion-correlation" and
         result["conclusion_context_binders"] == count and specs == result["specs"] and len(specs) == 1 and
         specs[0]["value"] == "separate" and specs[0]["profile_id"] == result["search_profile"],
         "PUBLIC_CORRELATION_QUERY_RESULT")
    need(result["features"] == [index_case["query_feature"]] and
         result["namespace"] == namespace_case["new_namespace"], "PUBLIC_QUERY_INDEX_KEY_BINDING")
    report["cases"].append("actual-supervised-manual-query-one-correlation-spec")
    request = {"action": "find", "contacts": {"local-test-only": {
        "host": "127.0.0.1", "port": 38191, "tls": False, "ca_file": None, "ca_sha256": None, "server_name": None}},
        "providers": ["local-test-only"], "specs": specs,
        "limits": {"providers": 1, "snapshots": 1, "requests": 4, "pages": 2,
                   "examined": 32, "candidates": 8, "bytes": 2*MIB, "wall_ms": 1000, "inflight": 1},
        "offer": {"max_bytes": 65536, "max_expanded_bytes": 65536, "max_age_ms": 60000},
        "page": {"scanned": 16, "matches": 8, "bytes": 65536, "timeout_ms": 1000,
                 "record_probes": 256, "node_reads": 100000, "hash_calls": 2000000, "sql_vm_steps": 1000000},
        "operation_output": str(args.output / "never-launched-find")}
    request_path = args.output / "request.json"
    save(request_path, request)
    prepared = child(args, "prepare", [selected / "prepare_selected.py", "--package", package,
        "--profile-sha256", assembled["profile_sha256"], "--request", request_path,
        "--output", args.output / "prepared"], report)
    need(prepared["interface"] == "conclusion-correlation-v1" and
         prepared["mathematical_acceptance"] is False and prepared["native_artifacts_checked"] is False and
         prepared["preparation"]["commands_executed"] == 0 and
         prepared["preparation"]["protected_state_opened"] is False and
         not (args.output / "never-launched-find").exists(), "INERT_PREPARATION_ONLY")
    report["cases"].append("actual-selected-kit-accepts-query-without-network-or-state")
    for name, expected_pin in expected.items():
        need(pin(read(package / name, 128*MIB)) == expected_pin, "FINAL_PACKAGE_PIN:" + name)
    report.update(profile_sha256=assembled["profile_sha256"], package=str(package),
                  installation_manifest_sha256=profile["installation_manifest_sha256"],
                  query_spec=specs[0], focused_control_groups=len(controls.get("groups", [])))


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for name in ("source-root", "base-package", "base-receipt", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    for name in ("base-profile-sha256", "base-receipt-sha256"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize, "ISOLATED_CANONICAL_PROFILE")
    need(args.output.is_absolute() and args.output.is_relative_to(ROOT / "experiments/v5-local-checks") and
         not args.output.exists() and args.output.parent.resolve(strict=True) == args.output.parent,
         "FRESH_INTEGRATION_OUTPUT")
    args.output.mkdir()
    report = {"passed": False, "cases": [], "mathematical_acceptance": False,
              "scope": "CORRELATION_METADATA_INDEX_QUERY_AND_FILE_ONLY_INTEGRATION_NOT_GROWTH"}
    try:
        run(args, report)
        check()
        report["passed"] = True
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error)[:2000])
        raise
    finally:
        report.update(wall_seconds=time.monotonic()-START, controller_cpu_seconds=time.process_time()-CPU)
        save(args.output / "RESULT.json", report)
        print(json.dumps(report, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
