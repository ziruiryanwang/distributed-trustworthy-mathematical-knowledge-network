"""One actual export using the selected already-built native helper."""
from pathlib import Path
import json
import os
import subprocess
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
SYSROOT = ROOT / "software/runtime/lean-4.34.0-windows"
EXECUTABLE = LOCAL / "ordinary-native-export-build-01/native-build/NativeOwnerExporter.exe"
METHODS = LOCAL / "ordinary-library-controls-01/lean-build"
INVENTORY = ROOT / "software/assets/foundation/seed-inventory-json.json"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    output = Path(sys.argv[1])
    if not Path(__file__).resolve().is_relative_to(LOCAL) or not output.is_absolute() or not output.is_relative_to(LOCAL):
        raise ValueError("IMMUTABLE_LOCAL_PATH_REQUIRED")
    env = {k: v for k, v in os.environ.items() if not k.upper().startswith(("LEAN", "PYTHON"))}
    env["PATH"] = str(SYSROOT / "bin") + os.pathsep + env.get("PATH", "")
    bundle = output / "owner-export.json"
    argv = list(map(str, (EXECUTABLE, SYSROOT, METHODS, INVENTORY, bundle)))
    start = time.monotonic()
    with (output / "native-export.stdout.txt").open("xb") as stdout, \
            (output / "native-export.stderr.txt").open("xb") as stderr:
        child = subprocess.run(argv, cwd=ROOT, env=env, stdout=stdout, stderr=stderr, timeout=120)
    if child.returncode:
        raise RuntimeError("NATIVE_OWNER_EXPORT_FAILED:" + str(child.returncode))
    if not 0 < bundle.stat().st_size <= 64*1024*1024:
        raise ValueError("OWNER_BUNDLE_BYTE_BOUND")
    value = json.loads(bundle.read_bytes())  # bounded selected local writer, not peer parser
    if value.get("schema") != "DMKN_ORDINARY_EXPORT_BUNDLE_V1" or not value.get("units"):
        raise ValueError("OWNER_BUNDLE_SCHEMA_OR_EMPTY")
    result = {"status": "PASS_INERT_NATIVE_EXPORT_ONLY", "argv": argv,
              "wall_seconds": time.monotonic()-start, "bundle_bytes": bundle.stat().st_size,
              "stats": value["stats"], "target_count": len(value["targets"]),
              "basis_names": len(value["basis_names"]), "unit_count": len(value["units"]),
              "claims": "REAL_OWNER_SOURCE_CLOSURE_NOT_CHECKED_ADMISSION_OR_GROWTH"}
    with (output / "EXPORT-RESULT.json").open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
