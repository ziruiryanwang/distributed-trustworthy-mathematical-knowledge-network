"""Selected package-only CLI boundary check, not part of the public package.

One expected wrong-profile refusal, fresh initialization, one caller-authored
multi-output contribution, and reopen/status. No old state, experimental helper
imports, peer traffic, certificate, retry or useful-growth claim. A separate
outer Windows Job must bound this entire validation process tree.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
import time

MIB = 1024**2


def need(condition, message):
    if not condition:
        raise ValueError(message)


def save(path, document):
    raw = json.dumps(document, sort_keys=True, ensure_ascii=True,
                     allow_nan=False, separators=(",", ":")).encode("ascii")
    with path.open("xb") as stream:
        stream.write(raw)
    return hashlib.sha256(raw).hexdigest()


def encoded_name(name):
    return [[0, {"$bytes": list(part.encode("ascii"))}] for part in name.split(".")]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("package", "profile-sha256", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+name, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    deadline = started + 210
    package, output = Path(args.package), Path(args.output)
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "VALIDATION_PYTHON")
    need(package.is_absolute() and output.is_absolute() and package.is_dir() and
         output.is_dir() and not output.is_relative_to(package) and
         not package.is_relative_to(output), "VALIDATION_DISJOINT_ROOTS")
    profile_raw = (package/"PROFILE.json").read_bytes()
    need(hashlib.sha256(profile_raw).hexdigest() == args.profile_sha256,
         "VALIDATION_PROFILE_PIN")
    catalog, custody = output/"catalog", output/"custody"
    need(not catalog.exists() and not custody.exists(), "VALIDATION_FRESH_OWNER")
    custody_limits = output/"custody-limits.json"
    save(custody_limits, {"objects": 512, "exports": 4096,
         "logical_bytes": 128*MIB, "db_pages": 16384})
    store_id = hashlib.sha256(b"ordinary-package-persistent-cli-boundary-01").hexdigest()
    calls, phase = [], "WRONG_PROFILE"
    report = {"status": "FAILED", "authority": "LOCAL_PACKAGE_BOUNDARY_NOT_FINAL_V5"}

    def call(operation, label, extra=(), *, profile=None, expected_ok=True):
        remaining = math.floor(deadline-time.monotonic())-5
        need(remaining >= 40, "VALIDATION_ORIGINAL_DEADLINE")
        argv = [str(Path(args.python_runtime)/"python.exe"), "-I", "-S", "-B",
            str(package/"owner.py"), operation,
            "--profile-sha256", profile or args.profile_sha256,
            "--python-runtime", args.python_runtime, "--lean-runtime", args.lean_runtime,
            "--catalog", str(catalog), "--custody", str(custody), "--store-id", store_id,
            "--custody-limits", str(custody_limits),
            "--wall-seconds", str(min(remaining, 120)), "--cpu-seconds", "90",
            "--memory-mib", "1536", *extra]
        save(output/(label+".command.json"), argv)
        begin = time.monotonic()
        with (output/(label+".stdout")).open("xb") as stdout, \
             (output/(label+".stderr")).open("xb") as stderr:
            child = subprocess.run(argv, cwd=output, stdin=subprocess.DEVNULL,
                stdout=stdout, stderr=stderr, timeout=deadline-time.monotonic(),
                creationflags=subprocess.CREATE_NO_WINDOW, check=False)
        raw = (output/(label+".stdout")).read_bytes()
        errors = (output/(label+".stderr")).read_bytes()
        need(len(raw) <= 4*MIB and len(errors) <= MIB, "VALIDATION_REPLY_BOUND")
        result = json.loads(raw)
        calls.append({"label": label, "returncode": child.returncode,
            "wall_seconds": time.monotonic()-begin,
            "stdout_sha256": hashlib.sha256(raw).hexdigest(),
            "stderr_sha256": hashlib.sha256(errors).hexdigest(), "result": result})
        need(not errors, "VALIDATION_UNEXPECTED_STDERR")
        need(result["ok"] is expected_ok and child.returncode == (0 if expected_ok else 1),
             "VALIDATION_OPERATION_RESULT:"+label)
        return result

    try:
        refused = call("init", "wrong-profile", profile="0"*64, expected_ok=False)
        need(refused["phase"] == "SUPPORT" and refused["error"] == "OWNER_PROFILE_PIN" and
             refused["accepted"] is None and not catalog.exists() and not custody.exists(),
             "VALIDATION_REFUSAL_BEFORE_STATE")
        phase = "INITIALIZE"
        initial = call("init", "init")
        basis = initial["result"]["basis"]["local_root"]
        need(initial["result"]["basis"]["status"] == "CHECKED", "VALIDATION_BASIS")
        source = output/"CallerBody.lean"
        with source.open("xb") as stream:
            stream.write(b"namespace CommonsPackageExample\n\n"
                b"def applyTwice {a : Type u} (f : a -> a) (x : a) : a := f (f x)\n\n"
                b"theorem applyTwice_eq {a : Type u} (f : a -> a) (x : a) :\n"
                b"    applyTwice f x = f (f x) := rfl\n\n"
                b"end CommonsPackageExample\n")
        acquired, names = output/"acquired.json", output/"outputs.json"
        save(acquired, [])
        selected_names = [encoded_name("CommonsPackageExample."+name)
                          for name in ("applyTwice", "applyTwice_eq")]
        save(names, selected_names)
        phase = "CONTRIBUTE"
        contributed = call("contribute", "contribute", (
            "--parent-root", basis, "--source", str(source), "--acquired-targets", str(acquired),
            "--output-names", str(names), "--output", str(output/"contribution")))
        result = contributed["result"]
        need(result["parent_root"] == basis and result["local_root"] != basis and
             result["admission"]["status"] == "CHECKED" and
             result["admission"]["units_checked"] == 2 and
             [row["name"] for row in result["targets"]] == selected_names and
             len(result["units"]) == 2 and len(result["previews"]) == 2,
             "VALIDATION_TWO_NEW_OUTPUTS")
        for row in [*result["units"], *result["previews"]]:
            path = Path(row["file"])
            need(path.is_relative_to(output/"contribution"), "VALIDATION_PUBLICATION_PATH")
            raw = path.read_bytes()
            need(len(raw) == row["bytes"] and hashlib.sha256(raw).hexdigest() == row["sha256"],
                 "VALIDATION_PUBLICATION_BYTES")
        phase = "REOPEN_STATUS"
        reopened = call("status", "reopen-status", ("--context-root", result["local_root"]))
        status = reopened["result"]
        need({row["local_root"] for row in status["roots"]} == {basis, result["local_root"]} and
             status["has_more"] is False and
             status["selected_context"]["local_root"] == result["local_root"] and
             status["selected_context"]["modules"] == 2 and
             reopened["cost"]["worker_cpu_seconds"] == 0 and
             all(row["implementation_id"] == initial["implementation_id"]
                 for row in (contributed, reopened)), "VALIDATION_PERSISTENT_REOPEN")
        need((package/"PROFILE.json").read_bytes() == profile_raw, "VALIDATION_PROFILE_CHANGED")
        report.update(status="PASS_LOCAL_PACKAGE_CLI_BOUNDARY", basis_root=basis,
            local_root=result["local_root"], targets=result["targets"],
            implementation_id=initial["implementation_id"], store_id=store_id,
            claim="NO_EXPERIMENT_HELPER_IMPORT_OR_STATE_COPY_NOT_A_GROWTH_BENCHMARK")
        return 0
    except BaseException as error:
        report.update(phase=phase, error_type=type(error).__name__, error=str(error))
        raise
    finally:
        report.update(calls=calls, wall_seconds=time.monotonic()-started,
            cost_scope="Outer Job includes all subprocess CPU; nested costs are not added twice")
        save(output/"LIFECYCLE-RESULT.json", report)
        print(json.dumps({"status": report["status"], "calls": len(calls),
                          "wall_seconds": report["wall_seconds"]}), flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
