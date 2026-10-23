"""Selected new workflow-module compilation only, no old-suite repetition."""
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
    output, core, snapshots = map(Path, sys.argv[1:])
    for path in (source, output, core, snapshots):
        if not path.is_absolute() or not path.is_relative_to(ROOT / "experiments/v5-local-checks"):
            raise ValueError("IMMUTABLE_LOCAL_PATHS_REQUIRED")
    for previous, modules in [(core, ("OriginalExpr", "OriginalDecl", "CheckedExtension")),
                              (snapshots, ("LocalSnapshot",))]:
        old = previous.parent / "sources/software/v5/ordinary_lean"
        for module in modules:
            if (source / (module + ".lean")).read_bytes() != (old / (module + ".lean")).read_bytes():
                raise ValueError("CHANGED_COMPILED_PREREQUISITE:" + module)
    build = output / "lean-build"
    build.mkdir()
    env = dict(os.environ)
    for key in ("LEAN_PATH", "LEAN_SYSROOT", "LEAN_SRC_PATH"):
        env.pop(key, None)
    env["LEAN_PATH"] = os.pathsep.join(map(str, (build, core, snapshots)))
    steps = []
    for module in ("BootstrapSupport", "OrdinaryExport", "BasisSnapshot", "OrdinaryWorkflowWorker"):
        start = time.monotonic()
        argv = [str(LEAN), "-R", str(source), "-o", str(build / (module + ".olean")),
                str(source / (module + ".lean"))]
        try:
            completed = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, timeout=75)
        except subprocess.TimeoutExpired as error:
            (output / (module + ".stdout.txt")).write_bytes(error.stdout or b"")
            (output / (module + ".stderr.txt")).write_bytes(error.stderr or b"")
            raise
        (output / (module + ".stdout.txt")).write_bytes(completed.stdout)
        (output / (module + ".stderr.txt")).write_bytes(completed.stderr)
        row = {"module": module, "argv": argv, "exit_code": completed.returncode,
               "wall_seconds": time.monotonic() - start}
        print(json.dumps(row), flush=True)
        if completed.returncode:
            print(completed.stdout.decode("utf-8", errors="replace"), flush=True)
            print(completed.stderr.decode("utf-8", errors="replace"), flush=True)
            raise RuntimeError("FAILED_COMPILE:" + module)
        steps.append(row)
    result = {"status": "PASS", "steps": steps,
              "claims": "SOURCE_COMPILATION_ONLY_NO_NATIVE_WORKFLOW_EXECUTED"}
    (output / "WORKFLOW-BUILD.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
