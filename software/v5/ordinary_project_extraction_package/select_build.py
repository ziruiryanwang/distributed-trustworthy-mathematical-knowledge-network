"""Select one changed-native compile/link and three-payload assembly; no launch."""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PREFIX = "software/v5/ordinary_project_extraction_package/"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def main():
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "PROJECT_BUILD_SELECTION_CONTEXT")
    need(len(sys.argv) == 2, "PROJECT_BUILD_ASSEMBLER_SHA_REQUIRED")
    path = ROOT/PREFIX/"assemble.py"
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() == sys.argv[1], "PROJECT_BUILD_ASSEMBLER_PIN")
    spec = importlib.util.spec_from_file_location("_selected_project_assembler", path)
    H = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(path), "exec"), H.__dict__)
    started = time.monotonic()
    deadline = started+60

    def check():
        need(time.monotonic() < deadline, "PROJECT_BUILD_SELECTION_DEADLINE")

    S, B = H.helpers()
    _, _, pins, _, sources = H.inspect_inputs(S, B, check, deadline)
    need(sources[PREFIX+"assemble.py"]["sha256"] == sys.argv[1], "PROJECT_BUILD_ASSEMBLER_CHANGED")
    source_hashes = {name: pin["sha256"] for name, pin in sources.items()}
    runner = "tools/Run-V5-Check.py"
    source_hashes[runner] = B.pin(ROOT/runner, check, 2*MIB)["sha256"]
    runtime = {str(path): pin["sha256"] for path, pin in pins.items()}
    need(len(runtime) < 256 and len(source_hashes) <= 256, "PROJECT_BUILD_SELECTION_PIN_BOUND")
    target = H.LOCAL/(H.NAME+".selection.json")
    B.ordinary(target, fresh=True); B.ordinary(H.LOCAL/H.NAME, directory=True, fresh=True)
    selection = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": H.NAME,
        "sources": source_hashes, "runtime_pins": runtime,
        "argv": [str(H.RUNTIMES["python_runtime"]/"python.exe"), "-I", "-S", "-B",
            "{snapshot}/"+PREFIX+"assemble.py", "--source-root", "{snapshot}",
            "--output", "{output}/integration"],
        "limits": {"wall_seconds": 180, "cpu_seconds": 120, "memory_mib": 1536,
            "active_processes": 6, "stdout_bytes": MIB, "stderr_bytes": MIB}}
    # Bind original inputs again before committing the single finite selection.
    for path, expected in pins.items():
        need(B.pin(path, check, 512*MIB) == expected, "PROJECT_BUILD_SELECTION_FINAL_PIN")
    raw = json.dumps(selection, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("ascii")
    B.fresh_bytes(target, raw)
    print(json.dumps({"selection": str(target), "sha256": hashlib.sha256(raw).hexdigest(),
        "runtime": "NOT_STARTED", "runtime_pin_count": len(runtime)}, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
