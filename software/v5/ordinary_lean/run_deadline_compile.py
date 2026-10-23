"""Finite successor of selected wrapper compilation, with an explicit total wall cap.

The original 45-second-per-module adapter and failed output stay unchanged.
This owner-only tool compiles exactly the selected new modules, reuses pinned
prerequisites and never retries. The outer selected Job provides hard containment.
"""
from pathlib import Path
import json
import math
import os
import re
import subprocess
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
LEAN = ROOT / "software/runtime/lean-4.34.0-windows/bin/lean.exe"


def main():
    started = time.monotonic()
    source = Path(__file__).resolve().parent
    output = Path(sys.argv[1])
    previous = [Path(part) for part in sys.argv[2].split(os.pathsep)]
    seconds = int(sys.argv[3])
    modules = sys.argv[4:]
    if (Path.cwd() != ROOT or not source.is_relative_to(LOCAL) or
        source.parents[2] != output / "sources" or not 1 <= seconds <= 180 or
        not 1 <= len(modules) <= 8 or len(modules) != len(set(modules)) or
        not all(re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", module) for module in modules) or
        not all(path.is_absolute() and path.is_relative_to(LOCAL) and path.is_dir() for path in previous)):
        raise ValueError("SELECTED_IMMUTABLE_COMPILE_INPUTS")
    deadline = started + seconds
    build = output / "lean-build"
    build.mkdir()
    env = dict(os.environ)
    for key in ("LEAN_PATH", "LEAN_SYSROOT", "LEAN_SRC_PATH"):
        env.pop(key, None)
    env["LEAN_PATH"] = os.pathsep.join(map(str, [build, *previous]))
    steps = []
    for module in modules:
        remaining = math.floor(deadline-time.monotonic())
        if remaining < 1:
            raise RuntimeError("SELECTED_COMPILE_DEADLINE")
        argv = [str(LEAN), "-DElab.async=false", "-R", str(source), "-o",
                str(build / (module + ".olean")), str(source / (module + ".lean"))]
        module_started = time.monotonic()
        with (output / (module + ".stdout.txt")).open("xb") as stdout, \
             (output / (module + ".stderr.txt")).open("xb") as stderr:
            result = subprocess.run(argv, cwd=ROOT, env=env, stdout=stdout,
                                    stderr=stderr, timeout=remaining)
        step = {"module": module, "argv": argv, "exit_code": result.returncode,
                "wall_seconds": time.monotonic()-module_started}
        print(json.dumps(step), flush=True)
        if result.returncode:
            raise RuntimeError("SELECTED_COMPILE_FAILED:"+module)
        if time.monotonic() >= deadline:
            raise RuntimeError("SELECTED_COMPILE_DEADLINE")
        steps.append(step)
    result = {"status": "PASS_SELECTED_NEW_MODULE_COMPILE", "steps": steps,
              "original_total_seconds": seconds,
              "claims": "COMPILATION_NOT_OWNER_USE_OR_MATHEMATICAL_ACCEPTANCE"}
    with (output / "COMPILE-RESULT.json").open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2)
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
