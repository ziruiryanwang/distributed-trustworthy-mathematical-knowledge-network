"""File-only selection for genuine checked-basis and selected-library admission."""
from pathlib import Path
import hashlib
import json

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    if Path.cwd() != ROOT:
        raise ValueError("CANONICAL_ROOT_REQUIRED")
    old = LOCAL / "ordinary-owner-export-01/selection.json"
    if digest(old) != "293dc9befaafc41a6324cb71903136d9eced11a21537f2086738a7c35ce115ff":
        raise ValueError("PRIOR_SELECTION_IDENTITY")
    value = json.loads(old.read_bytes())
    actual = LOCAL / "ordinary-native-owner-export-01"
    outcome = json.loads((actual / "RESULT.json").read_bytes())
    if (outcome["selection_sha256"] != "f3bcecc034b57a94378eec1dd8c4557e5d9022616f429a3d6e5210772e8f29d9"
            or outcome["result"]["status"] != "COMMAND_EXITED_ZERO_AND_CLOSED"):
        raise ValueError("ACTUAL_EXPORT_NOT_SUCCESSFUL")
    summary = json.loads((actual / "EXPORT-RESULT.json").read_bytes())
    if summary["status"] != "PASS_INERT_NATIVE_EXPORT_ONLY" or summary["unit_count"] != 2852:
        raise ValueError("ACTUAL_EXPORT_CENSUS")
    value["name"] = "ordinary-native-admission-01"
    modules = ("OriginalExpr", "OriginalDecl", "CheckedExtension", "LocalSnapshot",
               "BootstrapSupport", "OrdinaryExport", "BasisSnapshot", "OrdinaryWorkflowWorker")
    paths = ["tools/Run-V5-Check.py"]
    paths += ["software/v5/ordinary_lean/" + module + ".lean" for module in modules]
    paths += ["software/v5/ordinary_lean/" + name for name in (
        "ordinary_evidence.py", "local_catalog.py", "run_native_admission.py", "select_native_admission.py")]
    value["sources"] = {p: digest(ROOT / p) for p in paths}
    value["runtime_pins"] = {p: sha for p, sha in value["runtime_pins"].items()
                             if "ordinary-library-controls-01" not in p}
    for path in (actual / "owner-export.json", actual / "RESULT.json", actual / "EXPORT-RESULT.json",
                 ROOT / "software/assets/foundation/seed-verified.json"):
        value["runtime_pins"][str(path)] = digest(path)
    for path, sha in value["runtime_pins"].items():
        if digest(Path(path)) != sha:
            raise ValueError("CHANGED_ADMISSION_PREREQUISITE:" + path)
    value["argv"] = [r"D:\Python314\python.exe", "-I", "-S", "-B",
        r"{snapshot}\software\v5\ordinary_lean\run_native_admission.py", "{output}",
        str(LOCAL / "ordinary-workflow-build-01/lean-build"),
        str(LOCAL / "ordinary-library-controls-05/lean-build"),
        str(LOCAL / "ordinary-snapshot-controls-01/lean-build"), str(actual / "owner-export.json")]
    # Aggregate basis + all selected batches, not a reset per batch. Same memory
    # cap as export; child scopes independently bounded by reviewed controller.
    value["limits"] = {"cpu_seconds": 480, "wall_seconds": 540, "memory_mib": 1536,
                       "active_processes": 4, "stdout_bytes": 1048576, "stderr_bytes": 1048576}
    raw = (json.dumps(value, indent=2) + "\n").encode()
    target = LOCAL / "ordinary-native-admission-01-selection.json"
    with target.open("xb") as stream:
        stream.write(raw)
    print(target)
    print(hashlib.sha256(raw).hexdigest())


if __name__ == "__main__":
    main()
