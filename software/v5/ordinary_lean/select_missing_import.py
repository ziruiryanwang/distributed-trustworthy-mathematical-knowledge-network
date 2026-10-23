"""File-only fresh selection; does not execute the selected operation."""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
PYTHON = r"D:\Python314\python.exe"
LOWER_PINS = {
    "OriginalExpr.olean": "435d330a5c3bac37aa7b9bfcdd0a548fc3af0593bf53b6a10645e7cc5001eafd",
    "OriginalExpr.o": "354c0d29e3a98c42d12123f18dbe6c23880e4f7d0d92d9cf5359d31720083fcb",
    "OriginalDecl.olean": "565821e2a3bbbdd9fd8f912ec69985e3906806cee7c358d9420f6c553f3b82da",
    "OriginalDecl.o": "41e7aabd1e80967a05eb4f4e996513ae7aabfd00cc0415afb5a96eff3f3c580f",
    "CheckedExtension.olean": "9b34b26e6ab1560390b0f8a8ddc32fd5c21107df4e84b6be828cfcbe87372298",
    "CheckedExtension.o": "9ca258256d302c5d636e54b4c217ff1b5c03dfa095f6c5cf71ab244e1fefc66c",
    "BootstrapSupport.olean": "e6cf0c191da107ac9cef526e393b598e41bfd7470a8a3cf063a70dcc4d39f63a",
    "BootstrapSupport.o": "bee6a91e6d15a5eb9e9baa0026796e83b72bab7ec38ca424d77a75f8ea00b3fc",
}


def need(ok, code):
    if not ok:
        raise ValueError(code)


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    need(Path.cwd() == ROOT and len(sys.argv) in (3, 4), "MODE_NAME_OPTIONAL_BUILD_REQUIRED")
    mode, name = sys.argv[1:3]
    need(mode in ("build", "complete") and re.fullmatch(r"ordinary-[a-z0-9-]+", name), "MODE_NAME")
    output = LOCAL / (name + ".selection.json")
    need(not output.exists() and not (LOCAL / name).exists(), "FRESH_OPERATION_REQUIRED")
    prior_path = LOCAL / "ordinary-native-export-build-01/selection.json"
    need(sha(prior_path) == "ac56b4084629a357a85223c3115bb6988a40b3733f417d51353a0dc7630fde6f", "RETAINED_BUILD")
    prior = json.loads(prior_path.read_bytes())
    pins = dict(prior["runtime_pins"])
    files = ["tools/Run-V5-Check.py", "software/v5/ordinary_lean/select_missing_import.py"]
    if mode == "build":
        need(len(sys.argv) == 3, "BUILD_ARGUMENT_COUNT")
        result_path = prior_path.parent / "RESULT.json"
        result = json.loads(result_path.read_bytes())
        need(result["selection_sha256"] == sha(prior_path) and
             result["result"]["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED", "CLEAN_RETAINED_BUILD")
        for path in (prior_path, result_path):
            pins[str(path)] = sha(path)
        for filename, expected in LOWER_PINS.items():
            path = prior_path.parent / "native-build" / filename
            need(sha(path) == expected, "RETAINED_PAIRED_ARTIFACT_CHANGED")
            pins[str(path)] = expected
        files += ["software/v5/ordinary_lean/" + x for x in
                  ("run_missing_import_build.py", "OrdinaryExport.lean", "MissingImportExporter.lean")]
        argv = [PYTHON, "-I", "-S", "-B",
                r"{snapshot}\software\v5\ordinary_lean\run_missing_import_build.py", "{output}"]
        active = 6
    else:
        need(len(sys.argv) == 4 and re.fullmatch(r"ordinary-[a-z0-9-]+", sys.argv[3]), "BUILD_NAME_REQUIRED")
        build = LOCAL / sys.argv[3]
        build_selection, build_result, report = (json.loads((build / x).read_bytes()) for x in
                                               ("selection.json", "RESULT.json", "BUILD-RESULT.json"))
        need(build_result["selection_sha256"] == sha(build / "selection.json") and
             build_result["result"]["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and
             report["status"] == "PASS_MISSING_IMPORT_BUILD_ONLY", "CLEAN_NEW_BUILD_REQUIRED")
        executable = build / "native-build/MissingImportExporter.exe"
        need(sha(executable) == report["executable_sha256"] and
             executable.stat().st_size == report["executable_bytes"], "BUILT_EXECUTABLE_PIN")
        for path in (build / "selection.json", build / "RESULT.json", build / "BUILD-RESULT.json", executable):
            pins[str(path)] = sha(path)
        origin = LOCAL / "ordinary-native-admission-01"
        old_path = origin / "selection.json"
        need(sha(old_path) == "ab2f655448242587880129e62cca4bc5dc74638c1e8699e30b4a9f67e26fce5f", "OLD_CHECKER_SELECTION")
        old = json.loads(old_path.read_bytes())
        pins[str(old_path)] = sha(old_path)
        for helper in ("ordinary_evidence.py", "run_native_admission.py"):
            path = origin / "sources/software/v5/ordinary_lean" / helper
            expected = old["sources"]["software/v5/ordinary_lean/" + helper]
            need(sha(path) == expected, "RETAINED_HELPER_SOURCE")
            pins[str(path)] = expected
        database = LOCAL / "ordinary-native-recovery-01/native-recovery/catalog/catalog.sqlite"
        need(sha(database) == "bcb94ff9695f4d360205eaf8f81151f1cf70437c0e6c434b48f6993d893980e9", "PARENT_DATABASE_PIN")
        pins[str(database)] = sha(database)
        consumer = LOCAL / "ordinary-owner-consumer-05"
        candidate = consumer / "consumer-export.json"
        need(sha(candidate) == "a7f6f86bb28f10427d599bcfa2a3984ae66c418ad0a9bad18e37b90f10372975", "CANDIDATE05_PIN")
        pins[str(candidate)] = sha(candidate)
        files += ["software/v5/ordinary_lean/run_missing_import_completion.py"]
        argv = [PYTHON, "-I", "-S", "-B",
                r"{snapshot}\software\v5\ordinary_lean\run_missing_import_completion.py",
                "{output}", str(executable), str(candidate)]
        active = 3
    for path, expected in pins.items():
        need(sha(Path(path)) == expected, "RUNTIME_CHANGED:" + path)
    selection = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": name,
        "sources": {relative: sha(ROOT / relative) for relative in files}, "runtime_pins": pins, "argv": argv,
        "limits": {"cpu_seconds": 120, "wall_seconds": 150, "memory_mib": 1536,
                   "active_processes": active, "stdout_bytes": 1048576, "stderr_bytes": 1048576}}
    raw = (json.dumps(selection, indent=2) + "\n").encode()
    with output.open("xb") as stream:
        stream.write(raw)
    print(json.dumps({"selection": str(output), "sha256": hashlib.sha256(raw).hexdigest(), "execution": "NOT_STARTED"}))


if __name__ == "__main__":
    main()
