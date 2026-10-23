"""New snapshot boundary only; reuses exact successful compiled core05.

Owner-selected immutable runner under Run-V5-Check supervision. No peer source,
basis adoption, certificates, network, or repeat of the passed core campaigns.
"""
from pathlib import Path
import json
import os
import subprocess
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LEAN = ROOT / "software/runtime/lean-4.34.0-windows/bin/lean.exe"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    source = Path(__file__).resolve().parent
    output, previous = map(Path, sys.argv[1:])
    if not all(path.is_absolute() and path.is_relative_to(ROOT / "experiments/v5-local-checks")
               for path in (source, output, previous)):
        raise ValueError("IMMUTABLE_LOCAL_PATHS_REQUIRED")
    old_sources = previous.parent / "sources/software/v5/ordinary_lean"
    for module in ("OriginalExpr", "OriginalDecl", "CheckedExtension"):
        if (source / (module + ".lean")).read_bytes() != (old_sources / (module + ".lean")).read_bytes():
            raise ValueError("CHANGED_COMPILED_PREREQUISITE:" + module)
    build = output / "lean-build"
    build.mkdir()
    env = dict(os.environ)
    for key in ("LEAN_PATH", "LEAN_SYSROOT", "LEAN_SRC_PATH"):
        env.pop(key, None)
    env["LEAN_PATH"] = os.pathsep.join(map(str, (build, previous)))
    steps = []
    calls = [
        ("compile-snapshot", ["-o", build / "LocalSnapshot.olean", source / "LocalSnapshot.lean"]),
        ("snapshot-controls", ["--run", source / "LocalSnapshotChecks.lean",
                               LEAN.parent.parent, output / "snapshot-fixture"]),
    ]
    for label, arguments in calls:
        start = time.monotonic()
        argv = [str(LEAN), "-R", str(source), *map(str, arguments)]
        try:
            completed = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, timeout=75)
        except subprocess.TimeoutExpired as error:
            (output / (label + ".stdout.txt")).write_bytes(error.stdout or b"")
            (output / (label + ".stderr.txt")).write_bytes(error.stderr or b"")
            raise
        (output / (label + ".stdout.txt")).write_bytes(completed.stdout)
        (output / (label + ".stderr.txt")).write_bytes(completed.stderr)
        row = {"name": label, "argv": argv, "exit_code": completed.returncode,
               "wall_seconds": time.monotonic() - start}
        print(json.dumps(row), flush=True)
        if completed.returncode:
            print(completed.stdout.decode("utf-8", errors="replace"), flush=True)
            print(completed.stderr.decode("utf-8", errors="replace"), flush=True)
            raise RuntimeError("FAILED:" + label)
        if label == "snapshot-controls":
            text = completed.stdout.decode("utf-8")
            wanted = ["two-chained-deltas-without-intermediate-restore",
                      "exact-map-restore-without-ancestor-checking",
                      "restored-theorem-supports-new-consumer-proof", "incomplete-import-plan",
                      "wrong-parent-plan", "existing-output-refused", "uninitialized-parent-refused"]
            markers = [line.removeprefix("SNAPSHOT_CHECK_PASS ") for line in text.splitlines()
                       if line.startswith("SNAPSHOT_CHECK_PASS ")]
            complete = ("SNAPSHOT_CHECKS_COMPLETE conditionalFixtureOnly=true "
                        "protectedCatalog=false basisAdoption=false publicDeployment=false")
            if markers != wanted or text.splitlines().count(complete) != 1:
                raise RuntimeError("INCOMPLETE_SNAPSHOT_CONTROLS")
        steps.append(row)
    result = {"status": "PASS", "steps": steps,
              "claims": "LOCAL_SNAPSHOT_CONTROLS_CONDITIONAL_PARENT_NOT_BASIS_OR_DEPLOYMENT"}
    (output / "CHECKS.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
