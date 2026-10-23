"""Generate native code for six small local helpers; never rebuild Lean/Std.

Separate from actual owner export so a later workflow can reuse this executable.
The selected outer Job bounds the complete build, including compiler children.
"""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
BIN = ROOT / "software/runtime/lean-4.34.0-windows/bin"
MODULES = ("OriginalExpr", "OriginalDecl", "CheckedExtension", "BootstrapSupport",
           "OrdinaryExport", "NativeOwnerExporter")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    source, output = Path(__file__).resolve().parent, Path(sys.argv[1])
    if not source.is_relative_to(LOCAL) or not output.is_absolute() or not output.is_relative_to(LOCAL):
        raise ValueError("IMMUTABLE_SELECTED_BUILD_REQUIRED")
    build = output / "native-build"
    build.mkdir()
    env = {k: v for k, v in os.environ.items() if not k.upper().startswith(("LEAN", "PYTHON"))}
    env["LEAN_PATH"] = str(build)
    env["PATH"] = str(BIN) + os.pathsep + env.get("PATH", "")
    steps = []

    def run(label, argv):
        start = time.monotonic()
        with (output / (label + ".stdout.txt")).open("xb") as stdout, \
                (output / (label + ".stderr.txt")).open("xb") as stderr:
            result = subprocess.run(argv, cwd=ROOT, env=env, stdout=stdout, stderr=stderr, timeout=120)
        row = {"phase": label, "exit_code": result.returncode,
               "wall_seconds": time.monotonic()-start, "argv": argv}
        print(json.dumps(row), flush=True)
        steps.append(row)
        if result.returncode:
            raise RuntimeError("NATIVE_EXPORT_BUILD_FAILED:" + label)

    for module in MODULES:
        run(module + "-codegen", [str(BIN / "lean.exe"), "-R", str(source),
            "-o", str(build / (module + ".olean")), "-c", str(build / (module + ".c")),
            str(source / (module + ".lean"))])
        run(module + "-object", [str(BIN / "leanc.exe"), "-c", "-O0",
            str(build / (module + ".c")), "-o", str(build / (module + ".o"))])
    executable = build / "NativeOwnerExporter.exe"
    run("native-link", [str(BIN / "leanc.exe"), "-leanshared",
        *[str(build / (module + ".o")) for module in MODULES], "-o", str(executable)])
    if not executable.is_file():
        raise ValueError("MISSING_NATIVE_EXPORT_EXECUTABLE")
    raw = executable.read_bytes()
    result = {"status": "PASS_NATIVE_EXPORTER_BUILD_ONLY", "steps": steps,
              "executable_bytes": len(raw), "executable_sha256": hashlib.sha256(raw).hexdigest(),
              "claims": "NATIVE_BUILD_NOT_ACTUAL_EXPORT_OR_ADMISSION"}
    with (output / "BUILD-RESULT.json").open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
