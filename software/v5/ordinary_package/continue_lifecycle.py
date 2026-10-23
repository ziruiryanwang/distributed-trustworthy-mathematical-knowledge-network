"""Selected caller-visibility correction on the existing initialized owner.

No build, initialization, state copy or automatic retry. --select writes a fresh
finite plan only; --run performs exactly contribute and reopen/status under the
outer selected Job. All original failed-operation evidence remains untouched.
"""
from pathlib import Path
import hashlib
import json
import math
import os
import subprocess
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
ORIGINAL = LOCAL/"ordinary-package-lifecycle-01"
NAME = "ordinary-package-lifecycle-continuation-01"
PREFIX = "software/v5/ordinary_package/"
PYTHON = Path(r"D:\Python314\python.exe")
MIB = 1024**2


def need(condition, code):
    if not condition:
        raise ValueError(code)


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def save(path, value):
    raw = json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False,
                     separators=(",", ":")).encode("ascii")
    with path.open("xb") as stream:
        stream.write(raw)
    return hashlib.sha256(raw).hexdigest()


def previous():
    result = json.loads((ORIGINAL/"LIFECYCLE-RESULT.json").read_bytes())
    need(result["status"] == "FAILED" and result["phase"] == "CONTRIBUTE" and
         [row["label"] for row in result["calls"]] == ["wrong-profile", "init", "contribute"],
         "CONTINUATION_EXACT_PRIOR_OUTCOME")
    initial = result["calls"][1]["result"]
    failed = result["calls"][2]["result"]
    need(initial["ok"] is True and initial["result"]["basis"]["status"] == "CHECKED" and
         failed["ok"] is False and failed["accepted"] is None and
         failed["detail"]["phase"] == "AUTHORING" and
         failed["detail"]["error"] == "CONTRIBUTION_AUTHORING_NOT_CLEAN",
         "CONTINUATION_EXISTING_BASIS_NO_EXTENSION")
    return initial


def select():
    need(Path.cwd() == ROOT, "CONTINUATION_CANONICAL_SELECTION")
    original_selection = LOCAL/"ordinary-package-lifecycle-01.selection.json"
    need(sha(original_selection) == "adf5d883fd81b25e293715276f10de1a58240206d2d13089efd748e648f872c7",
         "CONTINUATION_PRIOR_SELECTION")
    initial = previous()
    plan = json.loads(original_selection.read_bytes())
    path = LOCAL/(NAME+".selection.json")
    need(not path.exists() and not (LOCAL/NAME).exists(), "CONTINUATION_FRESH_SELECTION")
    runtime = dict(plan["runtime_pins"])
    retained = [ORIGINAL/name for name in ("LIFECYCLE-RESULT.json", "CallerBody.lean",
        "acquired.json", "outputs.json", "custody-limits.json", "catalog/ADOPTION.json")]
    for file in retained:
        need(file.is_file() and file.stat().st_size <= 2*MIB, "CONTINUATION_RETAINED_BOUND")
        runtime[str(file)] = sha(file)
    for file, expected in runtime.items():
        need(sha(Path(file)) == expected, "CONTINUATION_UNCHANGED_PACKAGE_AND_INPUT")
    sources = {"tools/Run-V5-Check.py", PREFIX+"continue_lifecycle.py"}
    selection = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": NAME,
        "sources": {relative: sha(ROOT/relative) for relative in sorted(sources)},
        "runtime_pins": runtime,
        "argv": [str(PYTHON), "-I", "-S", "-B",
            r"{snapshot}\software\v5\ordinary_package\continue_lifecycle.py", "--run", "{output}",
            plan["argv"][plan["argv"].index("--package")+1], initial["profile_sha256"]],
        "limits": {"cpu_seconds": 100, "wall_seconds": 150, "memory_mib": 1792,
                   "active_processes": 8, "stdout_bytes": MIB, "stderr_bytes": MIB}}
    pin = save(path, selection)
    print(json.dumps({"selection": str(path), "sha256": pin, "runtime": "NOT_STARTED"}))


def run(output, package, profile):
    started = time.monotonic()
    deadline = started+120
    output, package = Path(output), Path(package)
    need(output.is_absolute() and output.is_dir() and package.is_absolute() and package.is_dir(),
         "CONTINUATION_PATHS")
    initial = previous()
    need(initial["profile_sha256"] == profile and sha(package/"PROFILE.json") == profile,
         "CONTINUATION_PROFILE")
    body = (ORIGINAL/"CallerBody.lean").read_bytes()
    needle = b"def applyTwice "
    need(body.count(needle) == 1 and b"@[expose]" not in body, "CONTINUATION_EXACT_CALLER_EDIT")
    corrected = body.replace(needle, b"@[expose]\n"+needle, 1)
    source = output/"CallerExposedBody.lean"
    with source.open("xb") as stream:
        stream.write(corrected)
    calls, phase = [], "CONTRIBUTE"
    report = {"status": "FAILED", "prior_outcome_sha256": sha(ORIGINAL/"LIFECYCLE-RESULT.json"),
        "caller_source_sha256": hashlib.sha256(corrected).hexdigest(),
        "authority": "LOCAL_PACKAGE_CONTINUATION_NOT_FINAL_V5"}

    def call(operation, extra):
        wall = min(90, math.floor(deadline-time.monotonic())-5)
        need(wall >= 40, "CONTINUATION_ORIGINAL_DEADLINE")
        argv = [str(PYTHON), "-I", "-S", "-B", str(package/"owner.py"), operation,
            "--profile-sha256", profile, "--python-runtime", str(PYTHON.parent),
            "--lean-runtime", str(ROOT/"software/runtime/lean-4.34.0-windows"),
            "--catalog", initial["catalog"], "--custody", initial["custody"],
            "--store-id", initial["store_id"], "--custody-limits", str(ORIGINAL/"custody-limits.json"),
            "--wall-seconds", str(wall), "--cpu-seconds", "60", "--memory-mib", "1536", *extra]
        save(output/(operation+".command.json"), argv)
        with (output/(operation+".stdout")).open("xb") as stdout, \
             (output/(operation+".stderr")).open("xb") as stderr:
            child = subprocess.run(argv, cwd=output, stdin=subprocess.DEVNULL,
                stdout=stdout, stderr=stderr, timeout=deadline-time.monotonic(),
                creationflags=subprocess.CREATE_NO_WINDOW, check=False)
        raw, errors = (output/(operation+".stdout")).read_bytes(), (output/(operation+".stderr")).read_bytes()
        need(len(raw) <= 4*MIB and len(errors) <= MIB, "CONTINUATION_REPLY_BOUND")
        result = json.loads(raw)
        calls.append({"operation": operation, "exit_code": child.returncode, "result": result,
                      "stdout_sha256": hashlib.sha256(raw).hexdigest()})
        need(not errors and child.returncode == 0 and result["ok"] is True,
             "CONTINUATION_PUBLIC_COMMAND:"+operation)
        need(result["implementation_id"] == initial["implementation_id"] and
             result["store_id"] == initial["store_id"], "CONTINUATION_SAME_OWNER")
        return result

    try:
        basis = initial["result"]["basis"]["local_root"]
        value = call("contribute", ["--parent-root", basis, "--source", str(source),
            "--acquired-targets", str(ORIGINAL/"acquired.json"),
            "--output-names", str(ORIGINAL/"outputs.json"), "--output", str(output/"contribution")])
        result = value["result"]
        need(result["parent_root"] == basis and result["local_root"] != basis and
             result["admission"]["status"] == "CHECKED" and result["admission"]["units_checked"] == 2 and
             [row["name"] for row in result["targets"]] == json.loads((ORIGINAL/"outputs.json").read_bytes()),
             "CONTINUATION_EXACT_NEW_OUTPUTS")
        need(len(result["units"]) == 2 and len(result["previews"]) == 2, "CONTINUATION_PUBLICATION_CENSUS")
        for row in [*result["units"], *result["previews"]]:
            path = Path(row["file"])
            need(path.is_relative_to(output/"contribution") and path.stat().st_size == row["bytes"] and
                 sha(path) == row["sha256"], "CONTINUATION_PUBLICATION_PIN")
        phase = "REOPEN_STATUS"
        reopened = call("status", ["--context-root", result["local_root"]])
        status = reopened["result"]
        need({row["local_root"] for row in status["roots"]} == {basis, result["local_root"]} and
             status["has_more"] is False and status["selected_context"]["local_root"] == result["local_root"] and
             status["selected_context"]["modules"] == 2 and reopened["cost"]["worker_cpu_seconds"] == 0,
             "CONTINUATION_PERSISTENT_CONTEXT")
        report.update(status="PASS_CORRECTED_CALLER_AND_PERSISTENT_REOPEN", basis_root=basis,
            local_root=result["local_root"], targets=result["targets"],
            claim="SAME_OWNER_NO_BUILD_INIT_OR_STATE_COPY_FIRST_FAILURE_REMAINS_CHARGED")
        return 0
    except BaseException as error:
        report.update(phase=phase, error_type=type(error).__name__, error=str(error))
        raise
    finally:
        report.update(calls=calls, wall_seconds=time.monotonic()-started,
                      cost_scope="Outer Job includes all child CPU; do not add nested reports twice")
        save(output/"CONTINUATION-RESULT.json", report)
        print(json.dumps({"status": report["status"], "calls": len(calls)}), flush=True)


if __name__ == "__main__":
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,
         "CONTINUATION_PYTHON")
    if sys.argv[1:] == ["--select"]:
        select()
    else:
        need(len(sys.argv) == 5 and sys.argv[1] == "--run", "CONTINUATION_ARGUMENTS")
        raise SystemExit(run(*sys.argv[2:]))
