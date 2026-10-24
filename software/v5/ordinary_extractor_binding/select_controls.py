"""File-only selection of one pure executable-binding check; never runs it."""
from pathlib import Path
import hashlib
import json
import os
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PREFIX = "software/v5/ordinary_extractor_binding/"
NAME = "ordinary-extractor-binding-controls-01"


def main():
    if not (Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and
            sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize):
        raise ValueError("CANONICAL_ISOLATED_SELECTION")
    local = ROOT/"experiments/v5-local-checks"
    target = local/(NAME+".selection.json")
    if target.exists() or (local/NAME).exists():
        raise ValueError("FRESH_SELECTION_REQUIRED")
    paths = ["tools/Run-V5-Check.py", PREFIX+"select_controls.py",
             PREFIX+"pin_controls.py", PREFIX+"library_extraction.py"]
    sources = {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in paths}
    if sources[PREFIX+"library_extraction.py"] != "28ff83c5a8561b9f5250e9be08b34744aedd23757765feb174e1504d700308aa":
        raise ValueError("SELECTED_HELPER_PIN")
    runtime = {}
    # Named local interpreter pins, not a hermetic standard-library claim.
    for name in ("python.exe", "python314.dll", "python3.dll"):
        path = Path(r"D:\Python314")/name
        with path.open("rb") as stream:
            runtime[str(path)] = hashlib.file_digest(stream, "sha256").hexdigest()
    plan = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": NAME, "sources": sources,
        "runtime_pins": runtime,
        "argv": [r"D:\Python314\python.exe", "-I", "-S", "-B",
                 "{snapshot}/"+PREFIX+"pin_controls.py", "--output", "{output}"],
        "limits": {"wall_seconds": 35, "cpu_seconds": 20, "memory_mib": 256,
                   "active_processes": 2, "stdout_bytes": 1048576, "stderr_bytes": 1048576}}
    raw = json.dumps(plan, sort_keys=True, separators=(",", ":")).encode("ascii")
    with target.open("xb") as stream:
        stream.write(raw)
    print(json.dumps({"selection": str(target), "sha256": hashlib.sha256(raw).hexdigest(),
                      "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()
