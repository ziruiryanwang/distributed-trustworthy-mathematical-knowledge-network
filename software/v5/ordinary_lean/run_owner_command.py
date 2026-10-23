"""Reuse the compiled owner command, then export from the existing project env.

No method recompilation, receiver admission, proof certificate or memory retry.
Runs only from the exact outer supervisor's immutable source snapshot.
"""
from pathlib import Path
import json
import os
import subprocess
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
LEAN = ROOT / "software/runtime/lean-4.34.0-windows/bin/lean.exe"
BUILT = LOCAL / "ordinary-workflow-build-01/lean-build"
CORE = LOCAL / "ordinary-library-controls-05/lean-build"
METHODS = LOCAL / "ordinary-library-controls-01/lean-build"
COMMAND = LOCAL / "ordinary-owner-command-01/lean-build"
INVENTORY = ROOT / "software/assets/foundation/seed-inventory-json.json"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    source = Path(__file__).resolve().parent
    output = Path(sys.argv[1])
    if (len(sys.argv) != 2 or not source.is_relative_to(LOCAL)
            or not output.is_absolute() or not output.is_relative_to(LOCAL)):
        raise ValueError("IMMUTABLE_LOCAL_PATHS_REQUIRED")
    prior = COMMAND.parent / "sources/software/v5/ordinary_lean/OwnerExportCommand.lean"
    if (source / "OwnerExportCommand.lean").read_bytes() != prior.read_bytes():
        raise ValueError("CHANGED_COMPILED_OWNER_COMMAND")
    env = dict(os.environ)
    for key in ("LEAN_PATH", "LEAN_SYSROOT", "LEAN_SRC_PATH"):
        env.pop(key, None)
    # Lean resolves namespace directories before the complete module path.
    # Put the actual examples provider before core05's empty examples directory.
    env["LEAN_PATH"] = os.pathsep.join(map(str, (COMMAND, BUILT, METHODS, CORE)))
    steps = []

    def run(label, argv):
        start = time.monotonic()
        # Direct log files retain flushed phase diagnostics even on outer kill.
        with (output / (label + ".stdout.txt")).open("xb") as stdout, \
                (output / (label + ".stderr.txt")).open("xb") as stderr:
            child = subprocess.run(argv, cwd=ROOT, env=env, stdout=stdout,
                                   stderr=stderr, timeout=120)
        row = {"phase": label, "exit_code": child.returncode,
               "wall_seconds": time.monotonic()-start, "argv": argv}
        steps.append(row)
        print(json.dumps(row), flush=True)
        if child.returncode:
            raise RuntimeError("OWNER_COMMAND_FAILED:" + label)

    bundle = output / "owner-export.json"
    driver = output / "OwnerProjectExport.lean"
    # A legacy (no `module`) owner header intentionally requests actual private
    # theorem bodies throughout the already-built transitive import closure.
    text = ("import examples.ReadFootprint\nimport OwnerExportCommand\n\n"
            "#ordinary_export DMKN.ReadFootprint.readsOnly_insertMany\n  "
            + json.dumps(INVENTORY.as_posix()) + "\n  "
            + json.dumps(bundle.as_posix()) + "\n")
    with driver.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(text)
    run("owner-command", [str(LEAN), "-R", str(output), str(driver)])
    if not 0 < bundle.stat().st_size <= 64*1024*1024:
        raise ValueError("OWNER_BUNDLE_BYTE_BOUND")
    # Trusted local writer output only; receiver raw canonical validation is
    # separate and must still happen before mathematical admission.
    value = json.loads(bundle.read_bytes())
    if value.get("schema") != "DMKN_ORDINARY_EXPORT_BUNDLE_V1" or not value.get("units"):
        raise ValueError("OWNER_BUNDLE_SCHEMA_OR_EMPTY")
    result = {"status": "PASS_INERT_OWNER_COMMAND_EXPORT_ONLY", "steps": steps,
              "bundle_bytes": bundle.stat().st_size, "stats": value["stats"],
              "target_count": len(value["targets"]), "basis_names": len(value["basis_names"]),
              "unit_count": len(value["units"]),
              "claims": "REAL_OWNER_SOURCE_CLOSURE_NOT_CHECKED_ADMISSION_OR_GROWTH"}
    with (output / "EXPORT-RESULT.json").open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
