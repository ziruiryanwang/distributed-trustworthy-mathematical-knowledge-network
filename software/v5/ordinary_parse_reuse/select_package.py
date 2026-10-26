"""Select one file-only package after adopted focused controls; never execute it."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
PREFIX = "software/v5/ordinary_parse_reuse/"
PACKAGE = LOCAL / "current-release-build01/distribution/package"
PROFILE_SHA = "7c41db618e17dd9b296df6aa566d2673b72edd859023bcfb7369e11925685541"
RELEASE_SHA = "821796aa5b4996edd3f34babdb3be186d8321e0b3b4208b1e3f18705400caf78"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT / "software/runtime/lean-4.34.0-windows"
START, CPU = time.monotonic(), time.process_time()
MIB = 1024**2


def need(ok, reason):
    if not ok:
        raise ValueError("PARSE_PACKAGE_SELECTION_"+reason)


def check():
    need(time.monotonic()-START < 60 and time.process_time()-CPU < 30, "ALLOWANCE")


def ordinary(path, *, fresh=False, directory=False):
    need(path.is_absolute() and ".." not in path.parts, "PATH")
    for entry in (*reversed(path.parents), path):
        try:
            info = entry.lstat()
        except FileNotFoundError:
            need(fresh and entry == path, "MISSING_PARENT_OR_INPUT")
            return path
        need(not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0)&0x400,
             "REDIRECT")
        need(stat.S_ISDIR(info.st_mode) if entry != path or directory else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "ORDINARY_FILE_OR_DIRECTORY")
    need(not fresh, "OUTPUT_EXISTS")
    return path


def pin(path):
    check(); ordinary(path)
    size = path.stat().st_size
    need(0 <= size <= 512*MIB, "FILE_BOUND")
    digest, count = hashlib.sha256(), 0
    with path.open("rb") as stream:
        while block := stream.read(MIB):
            check(); count += len(block); need(count <= size, "FILE_GREW")
            digest.update(block)
    need(count == ordinary(path).stat().st_size == size, "FILE_CHANGED")
    return {"bytes": size, "sha256": digest.hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--controls-result-sha256", required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and
         Path(sys.executable).resolve() == PYTHON/"python.exe", "PROCESS")
    destination = ordinary(LOCAL/"parse-reuse-package01.selection.json", fresh=True)
    ordinary(LOCAL/"parse-reuse-package01", directory=True, fresh=True)
    external = {}

    def retain(path, expected=None):
        result = pin(path)
        need(expected is None or expected == result or expected == result["sha256"], "INPUT_PIN")
        key = str(path)
        need(key not in external or external[key] == result, "PIN_OVERLAP")
        external[key] = result
        return result

    def document(path, expected=None):
        selected = retain(path, expected)
        need(selected["bytes"] <= 2*MIB, "JSON_BOUND")
        raw = path.read_bytes()
        need(len(raw) == selected["bytes"] and hashlib.sha256(raw).hexdigest() == selected["sha256"],
             "JSON_CHANGED")
        return json.loads(raw)

    release = document(ROOT/"software/v5/ordinary_current_release/release.json", RELEASE_SHA)
    profile = document(PACKAGE/"PROFILE.json", PROFILE_SHA)
    baseline = dict(release["prebuilt"]["files"])
    for name in ("authoring/bin/BaselineExporter.exe", "authoring/bin/MissingImportExporter.exe"):
        baseline[name] = profile["files"][name]
    baseline["PROFILE.json"] = external[str(PACKAGE/"PROFILE.json")]
    need(len(baseline) == 154, "PACKAGE_COUNT")
    found = set()
    for directory, folders, files in os.walk(ordinary(PACKAGE, directory=True)):
        for folder in folders:
            ordinary(Path(directory)/folder, directory=True)
        for name in files:
            path = Path(directory)/name
            relative = path.relative_to(PACKAGE).as_posix()
            need(relative in baseline and relative not in found, "PACKAGE_CENSUS")
            found.add(relative); retain(path, baseline[relative])
    need(found == set(baseline), "PACKAGE_COMPLETE")
    runtimes = release["build"]["runtime_pins"]
    need(len(runtimes) == 23, "RUNTIME_CENSUS")
    for key, expected in runtimes.items():
        category, name = key.split("/", 1)
        retain({"python_runtime": PYTHON, "lean_runtime": LEAN}[category]/name, expected)
    run = LOCAL/"parse-reuse-controls01"
    result = document(run/"RESULT.json", args.controls_result_sha256)
    selection = document(run/"selection.json", result["selection_sha256"])
    actual = result["result"]
    need(selection["name"] == "parse-reuse-controls01" and
         actual["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and actual["child_exit_code"] == 0 and
         actual["direct_child_reaped"] is True and actual["job_closed"] is True and
         actual["cleanup_errors"] == [] and actual["termination_requested"] is False and
         actual["final_job"]["active_processes"] == actual["final_job"]["terminated_processes"] == 0 and
         retain(run/"command/stderr.txt")["bytes"] == 0, "UNCLEAN_CONTROLS")
    controls = document(run/"controls/RESULT.json")
    need(document(run/"command/stdout.txt") == controls and
         controls["status"] == "PASS_FOCUSED_PARSE_REUSE_INERT_CONTROLS" and
         controls["forbidden_calls"] == [] and controls["mathematical_acceptance"] is False,
         "CONTROLS_RESULT")
    names = ["tools/Run-V5-Check.py", PREFIX+"assemble.py", PREFIX+"select_package.py",
        PREFIX+"INSTALLATION-PLAN.md", PREFIX+"ordinary_admission.py", PREFIX+"baseline_intake.py",
        "software/v5/ordinary_fair_search/assemble.py", "software/v5/ordinary_lean/ordinary_installation.py"]
    names += ["software/v5/ordinary_lean/"+name+".py" for name in
        "ordinary_admission ordinary_evidence ordinary_semantics portable_evidence portable_catalog local_catalog".split()]
    sources = {name: pin(ROOT/name) for name in names}
    for name in ("ordinary_admission.py", "baseline_intake.py"):
        need(sources[PREFIX+name]["sha256"] == selection["sources"][PREFIX+name], "TESTED_SOURCE_CHANGED")
    need(sources["tools/Run-V5-Check.py"]["sha256"] ==
         "44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651" and
         len(sources) == 14 and len(external) == 183, "EXACT_SELECTION_CENSUS")
    selected = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": "parse-reuse-package01",
        "sources": {name: value["sha256"] for name, value in sources.items()},
        "runtime_pins": {name: value["sha256"] for name, value in external.items()},
        "argv": [str(PYTHON/"python.exe"), "-I", "-S", "-B",
            r"{snapshot}\software\v5\ordinary_parse_reuse\assemble.py",
            "--admission-sha256", sources[PREFIX+"ordinary_admission.py"]["sha256"],
            "--intake-sha256", sources[PREFIX+"baseline_intake.py"]["sha256"],
            "--output", r"{output}\distribution"],
        "limits": {"wall_seconds": 180, "cpu_seconds": 90, "memory_mib": 768,
                   "active_processes": 1, "stdout_bytes": MIB, "stderr_bytes": MIB}}
    for name, expected in external.items():
        need(pin(Path(name)) == expected, "FINAL_EXTERNAL_PIN")
    for name, expected in sources.items():
        need(pin(ROOT/name) == expected, "FINAL_SOURCE_PIN")
    raw = json.dumps(selected, sort_keys=True, separators=(",", ":")).encode("ascii")
    check()
    with ordinary(destination, fresh=True).open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    need(destination.read_bytes() == raw, "SELECTION_READBACK")
    print(json.dumps({"selection": str(destination), "sha256": hashlib.sha256(raw).hexdigest(),
        "sources": len(sources), "external_pins": len(external), "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()
