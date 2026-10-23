"""Small owner-selected build/control driver; outer Windows Job bounds all children.

Run only an immutable Run-V5-Check snapshot. Never consumes peer source.
No certificate production, networking, package installation or accepted catalog.
"""
from concurrent.futures import ThreadPoolExecutor
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
    output = Path(sys.argv[1]).resolve()
    lane = sys.argv[2] if len(sys.argv) >= 3 else "all"
    if lane not in ("all", "core", "admission"):
        raise ValueError("SELECTED_LANE")
    if not source.is_relative_to(ROOT / "experiments/v5-local-checks"):
        raise ValueError("IMMUTABLE_SNAPSHOT_REQUIRED")
    if not output.is_relative_to(ROOT / "experiments/v5-local-checks"):
        raise ValueError("LOCAL_OUTPUT_REQUIRED")
    if lane == "admission":
        if len(sys.argv) != 4:
            raise ValueError("SELECTED_COMPILED_PREREQUISITES_REQUIRED")
        build = Path(sys.argv[3]).resolve()
        if not build.is_relative_to(ROOT / "experiments/v5-local-checks"):
            raise ValueError("LOCAL_BUILD_REQUIRED")
        previous_sources = build.parent / "sources/software/v5/ordinary_lean"
        for module in ("OriginalExpr", "OriginalDecl", "CheckedExtension"):
            if (source / (module + ".lean")).read_bytes() != (previous_sources / (module + ".lean")).read_bytes():
                raise ValueError("CHANGED_COMPILED_PREREQUISITE:" + module)
    else:
        build = output / "lean-build"
        build.mkdir()
        (build / "examples").mkdir()
    env = dict(os.environ)
    for key in ("LEAN_PATH", "LEAN_SYSROOT", "LEAN_SRC_PATH"):
        env.pop(key, None)
    env["LEAN_PATH"] = str(build)
    steps = []

    def call(name, arguments):
        started = time.monotonic()
        argv = [str(LEAN), "-R", str(source), *map(str, arguments)]
        try:
            completed = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, timeout=75)
        except subprocess.TimeoutExpired as error:
            (output / (name + ".stdout.txt")).write_bytes(error.stdout or b"")
            (output / (name + ".stderr.txt")).write_bytes(error.stderr or b"")
            raise
        (output / (name + ".stdout.txt")).write_bytes(completed.stdout)
        (output / (name + ".stderr.txt")).write_bytes(completed.stderr)
        result = {"name": name, "argv": argv, "exit_code": completed.returncode,
                  "wall_seconds": time.monotonic() - started}
        print(json.dumps(result), flush=True)
        if completed.returncode:
            print(completed.stdout.decode("utf-8", errors="replace"), flush=True)
            print(completed.stderr.decode("utf-8", errors="replace"), flush=True)
            raise RuntimeError("FAILED:" + name)
        return result

    def compile_one(module):
        return call("compile-" + module.replace("/", "-"),
                    ["-o", build / (module + ".olean"), source / (module + ".lean")])

    # Independent ordinary workflow compilation overlaps the codec/checker lane.
    def method_lane():
        first = compile_one("examples/ReadFootprint")
        second = compile_one("examples/ReadFootprintConsumer")
        return [first, second]

    if lane == "admission":
        steps.append(call("admission-controls", ["--run", source / "AdmissionChecks.lean",
                                                LEAN.parent.parent]))
    else:
        with ThreadPoolExecutor(max_workers=1) as pool:
            methods = pool.submit(method_lane) if lane == "all" else None
            for module in ("OriginalExpr", "OriginalDecl", "CheckedExtension"):
                steps.append(compile_one(module))
            steps.append(call("codec-controls", ["--run", source / "CodecChecks.lean"]))
            if (source / "AdmissionChecks.lean").is_file():
                steps.append(call("admission-controls", ["--run", source / "AdmissionChecks.lean",
                                                        LEAN.parent.parent]))
            if methods is not None:
                steps.extend(methods.result())
    result = {"status": "PASS", "steps": steps,
              "claims": "SOURCE_COMPILE_AND_SELECTED_CONTROLS_NOT_NETWORK_ADMISSION_OR_GROWTH"}
    (output / "CHECKS.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
