"""Root-selected file-only plans for changed generic contribution boundaries.

No compilation, mathematical acceptance or source-store mutation here. Used
inputs stay frozen. Each mode creates a fresh, non-overwriting selection for the
existing bounded supervisor; root reviews and separately launches it.
"""
from pathlib import Path
import hashlib
import json
import os
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
PREFIX = "software/v5/ordinary_lean/"


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read(name):
    return json.loads((LOCAL/name).read_bytes())


def fresh(path, document, *, canonical=False):
    raw = json.dumps(document, sort_keys=True, ensure_ascii=True, allow_nan=False,
                     separators=(",", ":") if canonical else None).encode("ascii")
    with path.open("xb") as stream: stream.write(raw)
    return hashlib.sha256(raw).hexdigest()


def main():
    if Path.cwd() != ROOT or sys.argv[1:] not in (["build"], ["controls"], ["actual"]):
        raise ValueError("CANONICAL_EXACT_GENERIC_SELECTION")
    mode = sys.argv[1]
    build_base = read("ordinary-portable-authoring-build-02.selection.json")
    receiver = read("ordinary-api-receiver-02.selection.json")
    receiver_args = receiver["argv"]

    def arg(flag): return receiver_args[receiver_args.index("--"+flag)+1]

    name = "ordinary-generic-contribution-"+mode+"-01"
    path = LOCAL/(name+".selection.json")
    if path.exists() or (LOCAL/name).exists(): raise ValueError("FRESH_GENERIC_SELECTION_REQUIRED")
    sources = ["tools/Run-V5-Check.py", PREFIX+"select_generic_contribution.py"]
    runtime = {}
    if mode == "build":
        sources += [PREFIX+"run_deadline_compile.py", PREFIX+"PortableContributionExportCommand.lean"]
        runtime = dict(build_base["runtime_pins"])
        prior = LOCAL/"ordinary-portable-authoring-build-02/lean-build"
        for file in prior.iterdir():
            if not file.is_file() or file.is_symlink(): raise ValueError("GENERIC_BUILD_SUPPORT_CENSUS")
            runtime[str(file)] = sha(file)
        helpers = str(prior)+os.pathsep+build_base["argv"][6]
        argv = [r"D:\Python314\python.exe", "-I", "-S", "-B",
            r"{snapshot}\software\v5\ordinary_lean\run_deadline_compile.py", "{output}",
            helpers, "120", "PortableContributionExportCommand"]
        limits = dict(cpu_seconds=90, wall_seconds=150, memory_mib=1536, active_processes=3,
                      stdout_bytes=1048576, stderr_bytes=1048576)
    elif mode == "controls":
        sources += [PREFIX+file for file in (
            "ordinary_contribution.py", "ordinary_contribution_checks.py", "ordinary_admission.py",
            "ordinary_evidence.py", "ordinary_semantics.py", "portable_evidence.py",
            "local_catalog.py", "portable_catalog.py", "portable_owner_request.py",
            "owner_request.py", "portable_candidate.py", "portable_preview.py", "ordinary_preview.py")]
        runtime = {key: value for key, value in build_base["runtime_pins"].items()
                   if key.startswith("D:\\Python314\\")}
        argv = [r"D:\Python314\python.exe", "-I", "-S", "-B",
                r"{snapshot}\software\v5\ordinary_lean\ordinary_contribution_checks.py"]
        limits = dict(cpu_seconds=30, wall_seconds=60, memory_mib=256, active_processes=2,
                      stdout_bytes=1048576, stderr_bytes=1048576)
    else:
        sources += [relative for relative in receiver["sources"]
                    if relative != "tools/Run-V5-Check.py" and relative not in (
                        PREFIX+"run_ordinary_api_receiver.py", PREFIX+"ordinary_successor_authoring.py",
                        PREFIX+"examples/PortableMethodSuccessor.lean")]
        sources += [PREFIX+"ordinary_contribution.py", PREFIX+"run_generic_contribution.py",
                    PREFIX+"examples/GenericContributionBody.lean"]
        # Root-selected retained dependency/support pins, not a proof from a
        # saved successful result. Native wrapper's new build is selected below.
        runtime = dict(receiver["runtime_pins"])
        new_build = LOCAL/"ordinary-generic-contribution-build-01/lean-build"
        for file in new_build.iterdir():
            if not file.is_file() or file.is_symlink(): raise ValueError("GENERIC_NEW_BUILD_CENSUS")
            runtime[str(file)] = sha(file)
        helpers = [str(new_build), *arg("helper-paths").split(os.pathsep)]
        original = LOCAL/"ordinary-api-receiver-02"
        directories, files = [], {}
        def visit(directory):
            if directory.is_symlink() or len(directories) >= 128:
                raise ValueError("GENERIC_PARENT_DIRECTORY_BOUND")
            directories.append(directory.relative_to(original).as_posix())
            with os.scandir(directory) as entries:
                for entry in entries:
                    path = Path(entry.path)
                    if entry.is_symlink() or getattr(entry.stat(follow_symlinks=False), "st_file_attributes", 0)&0x400:
                        raise ValueError("GENERIC_PARENT_REPARSE_POINT")
                    if entry.is_dir(follow_symlinks=False): visit(path)
                    elif entry.is_file(follow_symlinks=False):
                        if len(files) >= 512 or path.stat().st_size > 64*1024**2:
                            raise ValueError("GENERIC_PARENT_FILE_BOUND")
                        digest = sha(path)
                        files[path.relative_to(original).as_posix()] = {"bytes": path.stat().st_size, "sha256": digest}
                        runtime[str(path)] = digest
                    else: raise ValueError("GENERIC_PARENT_SPECIAL_FILE")
        visit(original/"catalog"); visit(original/"custody")
        result = read("ordinary-api-receiver-02/RECEIVER-RESULT.json")
        acquired = [result["successor"]["acquired_method"], result["successor"]["target"]]
        def encoded_name(label):
            return [[0, {"$bytes": list(part.encode("ascii"))}] for part in label.split(".")]
        plan = {"schema": "DMKN_GENERIC_CONTRIBUTION_LOCAL_PLAN_V1",
            "installation": arg("installation"), "manifest_sha256": arg("manifest-sha256"),
            "runtime_roots": {"python_runtime": arg("python-runtime"), "lean_runtime": arg("lean-runtime")},
            "source_directory": str(original), "directories": sorted(directories), "files": files,
            "parent_root": result["local_root"], "store_id": result["store_id"],
            "custody_limits": result["custody_limits"], "helper_paths": helpers,
            "source_body": PREFIX+"examples/GenericContributionBody.lean", "acquired_targets": acquired,
            "output_names": [encoded_name("CommonsExample.Transformations."+suffix)
                             for suffix in ("composeFour", "preservesFour")],
            "wall_seconds": 180, "cpu_seconds": 100, "memory_mib": 1536}
        plan_path = LOCAL/(name+".plan.json")
        plan_pin = fresh(plan_path, plan, canonical=True)
        runtime[str(plan_path)] = plan_pin
        argv = [r"D:\Python314\python.exe", "-I", "-S", "-B",
                r"{snapshot}\software\v5\ordinary_lean\run_generic_contribution.py",
                "--output", "{output}", "--plan", str(plan_path), "--plan-sha256", plan_pin]
        limits = dict(cpu_seconds=115, wall_seconds=210, memory_mib=1792, active_processes=6,
                      stdout_bytes=1048576, stderr_bytes=1048576)
    for file, expected in runtime.items():
        if sha(Path(file)) != expected: raise ValueError("GENERIC_RETAINED_RUNTIME_CHANGED:"+file)
    value = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": name,
        "sources": {relative: sha(ROOT/relative) for relative in sources},
        "runtime_pins": runtime, "argv": argv, "limits": limits}
    if len(runtime)>256 or len(value["sources"]) != len(sources): raise ValueError("GENERIC_SOURCE_CENSUS")
    pin = fresh(path, value)
    print(json.dumps({"selection": str(path), "sha256": pin, "runtime": "NOT_STARTED"}))


if __name__ == "__main__":
    main()
