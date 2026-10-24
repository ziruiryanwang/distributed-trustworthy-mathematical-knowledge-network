"""Two-call native type-query discriminator; no owner, search or acceptance.

Requires root's finite outer Windows Job selection. Reuses retained compiled
OriginalExpr; compiles only OwnerQueryCommand, then the instrumented fixture.
All partial files are retained. No automatic retry or whole-library rebuild.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
LEAN = ROOT / "software/runtime/lean-4.34.0-windows"
PYTHON = Path(r"D:\Python314\python.exe")
PROFILE_SHA = "192dfee12ac186fbdac0634212b28c1c6324222da2b035f8f295ec764303a68d"
COMMAND_SHA = "d488268d3e5118dcd121b504f051d3875d7e4d3d52badaf7198c9c86093fe59b"
QUERY_SHA = "7901236768784a399f9ae5c56b374d040bce56536b0a47a6ee85093440cabcee"
SUPERVISOR_SHA = "6ea16154f4533e80d2e4e27e12fb6fa0ab7abfa0ff2c52cfb7479c1a35a8c1c9"
MIB = 1024**2


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def load(name, path, expected):
    need(name not in sys.modules and path.is_absolute() and
         path.resolve(strict=True).is_relative_to(ROOT), "QUERY_NATIVE_IMPORT_PATH")
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(0 < len(raw) <= 2*MIB and digest(raw) == expected, "QUERY_NATIVE_IMPORT_PIN")
    module = importlib.util.module_from_spec(importlib.util.spec_from_file_location(name, path))
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def lean_child(arguments):
    need(len(arguments) == 3, "QUERY_NATIVE_CHILD_ARGUMENTS")
    output, helpers, source = map(Path, arguments)
    need(output.is_relative_to(LOCAL) and source.parent == output and
         source.name in {"OwnerQueryCommand.lean", "QueryNativeFixture.lean"},
         "QUERY_NATIVE_CHILD_SCOPE")
    env = {k: v for k, v in os.environ.items()
           if not k.upper().startswith(("LEAN", "PYTHON")) and k.upper() != "PATH"}
    env["LEAN_PATH"] = os.pathsep.join((str(output), str(helpers), str(LEAN/"lib/lean")))
    env["PATH"] = os.pathsep.join((str(PYTHON.parent), str(LEAN/"bin")))
    return subprocess.call([str(LEAN/"bin/lean.exe"), "-DElab.async=false", "-R", str(output),
        "-o", str(source.with_suffix(".olean")), str(source)], cwd=output, env=env,
        stdin=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)


def main():
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and
         Path(sys.executable).resolve() == PYTHON, "QUERY_NATIVE_CONTEXT")
    if sys.argv[1:2] == ["--lean-child"]:
        return lean_child(sys.argv[2:])
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--package", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    need(Path.cwd() == ROOT, "QUERY_NATIVE_CANONICAL_CWD")
    package, output, sources = Path(args.package), Path(args.output), Path(__file__).resolve().parent
    A = load("_query_native_supervisor", package/"installation/supervisor/commons.py", SUPERVISOR_SHA)
    A.absolute(package, directory=True)
    A.absolute(output, directory=True, fresh=True)
    need(package.is_relative_to(LOCAL) and output.is_relative_to(LOCAL) and
         not A.overlap(package, output), "QUERY_NATIVE_FRESH_DISJOINT")
    profile_raw = A.bounded_read(package/"PROFILE.json", 2*MIB)
    need(digest(profile_raw) == PROFILE_SHA, "QUERY_NATIVE_PROFILE_PIN")
    profile = A.strict(profile_raw)
    manifest_raw = A.bounded_read(package/"installation/INSTALLATION.json", 2*MIB)
    need(digest(manifest_raw) == profile["installation_manifest_sha256"], "QUERY_NATIVE_MANIFEST_PIN")
    manifest = A.strict(manifest_raw)
    pins = {}

    def hold(path, expected=None):
        actual = A.pin(path)
        need(expected is None or actual == expected, "QUERY_NATIVE_FILE_PIN:"+str(path))
        need(pins.setdefault(str(path), actual) == actual, "QUERY_NATIVE_FILE_CHANGED")
        return actual

    def installed(logical):
        path = package/"installation"/Path(*A.safe_relative(logical))
        hold(path, manifest["files"][logical])
        return path

    def author(logical):
        path = package/Path(*A.safe_relative(logical))
        hold(path, profile["files"][logical])
        return path

    def write(path, raw):
        A.absolute(path, fresh=True)
        need(type(raw) is bytes and len(raw) <= MIB, "QUERY_NATIVE_WRITE_BOUND")
        with path.open("xb") as stream:
            stream.write(raw)
        hold(path)

    hold(package/"PROFILE.json"); hold(package/"installation/INSTALLATION.json")
    load("domains", installed("supervisor/domains.py"), manifest["files"]["supervisor/domains.py"]["sha256"])
    J = load("_query_native_job", installed("supervisor/run_stage.py"),
             manifest["files"]["supervisor/run_stage.py"]["sha256"])
    installed("supervisor/commons.py")
    for suffix in (".olean", ".olean.private", ".olean.server", ".ir", ".ir.sig"):
        author("authoring/helpers/OriginalExpr"+suffix)
    command = A.bounded_read(sources/"OwnerQueryCommand.lean", MIB)
    need(digest(command) == COMMAND_SHA, "QUERY_NATIVE_COMMAND_PIN")
    template = A.bounded_read(sources/"QueryNativeFixture.lean", MIB)
    need(template.count(b"__QUERY_OUTPUT__") == 1, "QUERY_NATIVE_FIXTURE_MARKER")
    for filename in ("OwnerQueryCommand.lean", "QueryNativeFixture.lean", "formal_query.py", "native_query_check.py"):
        hold(sources/filename)
    output.mkdir()
    query_path = output/"query.json"
    fixture = template.replace(b"__QUERY_OUTPUT__", str(query_path).replace("\\", "/").encode("ascii"))
    write(output/"OwnerQueryCommand.lean", command)
    write(output/"QueryNativeFixture.lean", fixture)
    started, cpu_started, charged = time.monotonic(), time.process_time(), 0.0
    report = {"status": "FAILED", "calls": [], "acceptance": False,
              "claim": "TYPE_EXTRACTION_COMPATIBILITY_ONLY_NOT_DISCOVERY_OR_USEFUL_GROWTH"}
    A.save_new(output/"INPUTS.json", {"pins": pins, "profile_sha256": PROFILE_SHA,
        "inner_allowance": {"wall_seconds": 80, "cpu_seconds": 50, "memory_mib": 1536}})
    try:
        for filename in ("OwnerQueryCommand.lean", "QueryNativeFixture.lean"):
            wall = math.floor(80-(time.monotonic()-started))-10
            cpu = math.floor(50-charged-(time.process_time()-cpu_started))-10
            limits = {"wall_seconds": min(35, wall), "cpu_seconds": min(20, cpu),
                      "memory_mib": 1536, "active_processes": 4,
                      "stdout_bytes": MIB, "stderr_bytes": MIB}
            need(wall >= 5 and cpu >= 2, "QUERY_NATIVE_REMAINING_ALLOWANCE")
            event = {"file": filename, "cpu_complete": False, "charged_cpu_seconds": limits["cpu_seconds"]}
            report["calls"].append(event)
            charged += limits["cpu_seconds"]
            record = A.supervise([str(PYTHON), "-I", "-S", "-B", str(Path(__file__).resolve()),
                "--lean-child", str(output), str(package/"authoring/helpers"), str(output/filename)],
                output, output/(Path(filename).stem+"-supervision"), limits, J.Job)
            event["supervision"] = record
            final = record.get("final_job", {})
            actual = final.get("cpu_seconds")
            need(type(actual) in (float, int) and math.isfinite(actual) and actual >= 0,
                 "QUERY_NATIVE_UNKNOWN_CPU_FULL_GRANT_CHARGED")
            charged += actual-limits["cpu_seconds"]
            event.update(cpu_complete=True, charged_cpu_seconds=actual)
            need(record["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and record["child_exit_code"] == 0 and
                 record["direct_child_reaped"] and record["job_closed"] and not record["cleanup_errors"] and
                 not record["termination_requested"] and final["active_processes"] == 0 and
                 final["terminated_processes"] == 0 and actual <= limits["cpu_seconds"] and
                 record["wall_seconds_through_cleanup"] <= limits["wall_seconds"], "QUERY_NATIVE_COMMAND_FAILED")
            need(all(record["observed_logs"][key] == 0 for key in ("stdout_bytes", "stderr_bytes")),
                 "QUERY_NATIVE_UNEXPECTED_DIAGNOSTIC")
            for suffix in (".olean", ".olean.private", ".olean.server", ".ir", ".ir.sig"):
                part = output/(Path(filename).stem+suffix)
                need(hold(part)["bytes"] > 0, "QUERY_NATIVE_EMPTY_ARTIFACT")

        modules = {}
        for name, path in (("ordinary_evidence", installed("py/ordinary_evidence.py")),
                          ("ordinary_semantics", installed("py/ordinary_semantics.py")),
                          ("ordinary_preview", author("authoring/py/ordinary_preview.py")),
                          ("portable_evidence", installed("py/portable_evidence.py")),
                          ("portable_preview", author("authoring/py/portable_preview.py"))):
            modules[name] = load(name, path, pins[str(path)]["sha256"])
        Q = load("formal_query", sources/"formal_query.py", QUERY_SHA)
        E, S = modules["ordinary_evidence"], modules["ordinary_semantics"]
        raw = A.bounded_read(query_path, MIB)
        parsed = Q.read_native_type(raw)
        name = lambda text: [[0, {"$bytes": list(text.encode("ascii"))}]]
        need(parsed["universe_params"] == [name("u"), name("v")] and
             Q.reference_names(raw) == [name("Eq")], "QUERY_NATIVE_EXACT_PARAMS_REFERENCES")
        exprs, current, binders = parsed["type"][2], parsed["type"][3], []
        while exprs[current][0] == 5:
            node = exprs[current]
            binders.append([node[1], node[2]])
            current = node[4]
        need(binders == [[name(label), flag] for label, flag in
                         (("A", 1), ("B", 0), ("f", 0), ("g", 0), ("a", 0))],
             "QUERY_NATIVE_SECTION_CLOSURE_OR_UNUSED_VARIABLE")
        inventory = installed("foundation/inventory.json")
        rows = E.strict_json(A.bounded_read(inventory, MIB))
        need(sum(row[0] == name("Eq") for row in rows) == 1, "QUERY_NATIVE_EQ_NOT_KNOWN_BASIS")
        bindings = E.canonical_json([[name("Eq"), S.basis_symbol_id(S.semantic_id(), S.foundation_id(), name("Eq"))]])
        query = Q.bind_native_type(raw, bindings, semantic_id=S.semantic_id())
        write(output/"bound-query.json", query)
        write(output/"bindings.json", bindings)
        hold(query_path)
        spec = Q.query_spec(query)
        for path, expected in pins.items():
            need(A.pin(Path(path)) == expected, "QUERY_NATIVE_FINAL_PIN")
        need(time.monotonic()-started <= 80 and time.process_time()-cpu_started+charged <= 50,
             "QUERY_NATIVE_FINAL_ALLOWANCE")
        report.update(status="PASS_NATIVE_TYPE_ONLY_QUERY", query_sha256=digest(raw),
                      spec=spec, section_binders=binders, type_nodes=parsed["type_nodes"],
                      no_query_declaration_inserted=True, no_proof_supplied=True, pins=pins,
                      compiled_command_artifacts={suffix: pins[str(output/("OwnerQueryCommand"+suffix))]
                          for suffix in (".olean", ".olean.private", ".olean.server", ".ir", ".ir.sig")})
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error)[:2000])
    report.update(wall_seconds=time.monotonic()-started,
                  controller_cpu_seconds=time.process_time()-cpu_started,
                  charged_inclusive_child_cpu_seconds=charged,
                  retention="ALL_PARTIAL_OUTPUTS_RETAINED_NO_RETRY")
    A.save_new(output/"NATIVE-QUERY-RESULT.json", report)
    print(json.dumps({"status": report["status"]}), flush=True)
    return 0 if report["status"] == "PASS_NATIVE_TYPE_ONLY_QUERY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
