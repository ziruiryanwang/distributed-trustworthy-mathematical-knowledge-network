"""One selected real owner export. No mathematical admission or old rebuilds.

Reuses the already compiled ReadFootprint fixture and new reviewed worker.
The outer selection pins worker dependencies, producer module and inventory.
This is a diagnostic integration driver, not the public node controller.
"""
from pathlib import Path
import json
import os
import subprocess
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LEAN = ROOT / "software/runtime/lean-4.34.0-windows/bin/lean.exe"
METHODS = ROOT / "experiments/v5-local-checks/ordinary-library-controls-01/lean-build"
INVENTORY = ROOT / "software/assets/foundation/seed-inventory-json.json"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    source = Path(__file__).resolve().parent
    output, built, core, snapshots = map(Path, sys.argv[1:])
    for path in (source, output, built, core, snapshots):
        if not path.is_absolute() or not path.is_relative_to(ROOT / "experiments/v5-local-checks"):
            raise ValueError("IMMUTABLE_LOCAL_PATHS_REQUIRED")
    previous = built.parent / "sources/software/v5/ordinary_lean/OrdinaryWorkflowWorker.lean"
    if (source / "OrdinaryWorkflowWorker.lean").read_bytes() != previous.read_bytes():
        raise ValueError("CHANGED_COMPILED_WORKER_SOURCE")
    env = dict(os.environ)
    for key in ("LEAN_PATH", "LEAN_SYSROOT", "LEAN_SRC_PATH"):
        env.pop(key, None)
    env["LEAN_PATH"] = os.pathsep.join(map(str, (built, core, snapshots)))
    bundle = output / "owner-export.json"
    argv = [str(LEAN), "-R", str(source), "--run", str(source / "OrdinaryWorkflowWorker.lean"),
            "export", str(LEAN.parent.parent), str(METHODS), str(INVENTORY), str(bundle)]
    start = time.monotonic()
    try:
        completed = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, timeout=120)
    except subprocess.TimeoutExpired as error:
        (output / "owner-export.stdout.txt").write_bytes(error.stdout or b"")
        (output / "owner-export.stderr.txt").write_bytes(error.stderr or b"")
        raise
    (output / "owner-export.stdout.txt").write_bytes(completed.stdout)
    (output / "owner-export.stderr.txt").write_bytes(completed.stderr)
    if completed.returncode:
        print(completed.stdout.decode("utf-8", errors="replace"), flush=True)
        print(completed.stderr.decode("utf-8", errors="replace"), flush=True)
        raise RuntimeError("OWNER_EXPORT_FAILED")
    # Output of this exact trusted local writer, not a peer JSON parser. All
    # eventual evidence envelopes still face the separate strict raw reader.
    if not 0 < bundle.stat().st_size <= 64 * 1024 * 1024:
        raise ValueError("OWNER_BUNDLE_BYTE_BOUND")
    value = json.loads(bundle.read_bytes())
    if value.get("schema") != "DMKN_ORDINARY_EXPORT_BUNDLE_V1" or not value.get("units"):
        raise ValueError("OWNER_BUNDLE_SCHEMA_OR_EMPTY")
    result = {"status": "PASS_INERT_EXPORT_ONLY", "argv": argv,
              "wall_seconds": time.monotonic() - start, "bundle_bytes": bundle.stat().st_size,
              "stats": value["stats"], "target_count": len(value["targets"]),
              "basis_names": len(value["basis_names"]), "unit_count": len(value["units"]),
              "claims": "REAL_OWNER_SOURCE_CLOSURE_NOT_CHECKED_RECEIVER_ADMISSION_OR_GROWTH"}
    (output / "EXPORT-RESULT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
