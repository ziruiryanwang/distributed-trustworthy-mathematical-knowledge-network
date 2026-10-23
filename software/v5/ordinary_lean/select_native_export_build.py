"""File-only one-shot selection for native exporter code generation/linking."""
from pathlib import Path
import hashlib
import json

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
RUNTIME = ROOT / "software/runtime/lean-4.34.0-windows"
MODULES = ("OriginalExpr", "OriginalDecl", "CheckedExtension", "BootstrapSupport",
           "OrdinaryExport", "NativeOwnerExporter")


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    if Path.cwd() != ROOT:
        raise ValueError("CANONICAL_ROOT_REQUIRED")
    prior_path = LOCAL / "ordinary-owner-export-01/selection.json"
    if sha(prior_path) != "293dc9befaafc41a6324cb71903136d9eced11a21537f2086738a7c35ce115ff":
        raise ValueError("PRIOR_SELECTION_IDENTITY")
    prior = json.loads(prior_path.read_bytes())
    names = ["tools/Run-V5-Check.py", "software/v5/ordinary_lean/run_native_export_build.py",
             "software/v5/ordinary_lean/select_native_export_build.py"]
    names += ["software/v5/ordinary_lean/" + module + ".lean" for module in MODULES]
    pins = {p: digest for p, digest in prior["runtime_pins"].items()
            if Path(p).parent == RUNTIME / "bin" or Path(p).parent == Path(r"D:\Python314")}
    for name in ("leanc.exe", "clang.exe", "ld.lld.exe", "lld.exe", "libclang-cpp.dll",
                 "libLLVM-22.dll", "zlib1.dll", "libLake_shared.dll"):
        path = RUNTIME / "bin" / name
        pins[str(path)] = sha(path)
    # Imported upstream code comes from the installed libraries, not a rebuild.
    # This remains selected-build evidence, explicitly not a hermetic toolchain.
    for name in ("libLake_shared.dll.a", "libInit_shared.dll.a", "libleanshared_2.dll.a",
                 "libleanshared_1.dll.a", "libleanshared.dll.a", "libleanmanifest.a"):
        path = RUNTIME / "lib/lean" / name
        pins[str(path)] = sha(path)
    for path, digest in pins.items():
        if sha(Path(path)) != digest:
            raise ValueError("CHANGED_BUILD_RUNTIME:" + path)
    # Preserve the actual reviewed custom helper source bytes.
    for module in MODULES[:-1]:
        old = next(p for p in prior["runtime_pins"] if p.endswith("/" + module + ".lean")
                   or p.endswith("\\" + module + ".lean"))
        if sha(ROOT / "software/v5/ordinary_lean" / (module + ".lean")) != prior["runtime_pins"][old]:
            raise ValueError("CHANGED_CUSTOM_HELPER:" + module)
    value = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": "ordinary-native-export-build-01",
        "sources": {name: sha(ROOT / name) for name in names}, "runtime_pins": pins,
        "argv": [r"D:\Python314\python.exe", "-I", "-S", "-B",
                 r"{snapshot}\software\v5\ordinary_lean\run_native_export_build.py", "{output}"],
        "limits": {"cpu_seconds": 120, "wall_seconds": 180, "memory_mib": 1536,
                   "active_processes": 6, "stdout_bytes": 1048576, "stderr_bytes": 1048576}}
    raw = (json.dumps(value, indent=2) + "\n").encode()
    output = LOCAL / "ordinary-native-export-build-01-selection.json"
    with output.open("xb") as stream:
        stream.write(raw)
    print(output)
    print(hashlib.sha256(raw).hexdigest())


if __name__ == "__main__":
    main()
