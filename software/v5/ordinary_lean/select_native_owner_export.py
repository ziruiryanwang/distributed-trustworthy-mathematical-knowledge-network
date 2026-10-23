"""Prepare a fresh actual-export selection only after native build completion."""
from pathlib import Path
import hashlib
import json

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
BIN = ROOT / "software/runtime/lean-4.34.0-windows/bin"


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
    build = LOCAL / "ordinary-native-export-build-01"
    report = json.loads((build / "RESULT.json").read_bytes())
    if report["selection_sha256"] != "ac56b4084629a357a85223c3115bb6988a40b3733f417d51353a0dc7630fde6f" or report["result"]["status"] != "COMMAND_EXITED_ZERO_AND_CLOSED":
        raise ValueError("ACTUAL_BUILD_NOT_SUCCESSFUL")
    built = json.loads((build / "BUILD-RESULT.json").read_bytes())
    executable = build / "native-build/NativeOwnerExporter.exe"
    if built["status"] != "PASS_NATIVE_EXPORTER_BUILD_ONLY" or digest(executable) != built["executable_sha256"]:
        raise ValueError("BUILT_EXECUTABLE_BINDING")
    value["name"] = "ordinary-native-owner-export-01"
    value["sources"] = {rel: digest(ROOT / rel) for rel in (
        "tools/Run-V5-Check.py", "software/v5/ordinary_lean/run_native_owner_export.py",
        "software/v5/ordinary_lean/select_native_owner_export.py")}
    value["runtime_pins"] = {p: sha for p, sha in value["runtime_pins"].items()
        if Path(p).parent in (BIN, Path(r"D:\Python314")) or
        "ordinary-library-controls-01" in p or Path(p).name == "seed-inventory-json.json"}
    for path in (executable, BIN / "libLake_shared.dll", build / "selection.json", build / "RESULT.json", build / "BUILD-RESULT.json"):
        value["runtime_pins"][str(path)] = digest(path)
    for path, sha in value["runtime_pins"].items():
        if digest(Path(path)) != sha:
            raise ValueError("CHANGED_EXPORT_INPUT:" + path)
    value["argv"] = [r"D:\Python314\python.exe", "-I", "-S", "-B",
                     r"{snapshot}\software\v5\ordinary_lean\run_native_owner_export.py", "{output}"]
    raw = (json.dumps(value, indent=2) + "\n").encode()
    target = LOCAL / "ordinary-native-owner-export-01-selection.json"
    with target.open("xb") as stream:
        stream.write(raw)
    print(target)
    print(hashlib.sha256(raw).hexdigest())


if __name__ == "__main__":
    main()
