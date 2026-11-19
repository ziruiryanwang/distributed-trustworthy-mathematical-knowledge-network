"""Pin one repaired-source compiler command, without running it."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PREFIX = "software/v5/ordinary_reference/"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--build-sha256", required=True)
    parser.add_argument("--source-sha256", required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "SOURCE_CONTINUATION_SELECTION_CONTEXT")
    for value in vars(args).values():
        need(len(value) == 64 and all(c in "0123456789abcdef" for c in value), "SOURCE_CONTINUATION_SELECTION_HASH")
    path = ROOT/PREFIX/"build_reference_source_continuation.py"
    with path.open("rb") as handle:
        raw = handle.read(2*MIB+1)
    need(0 < len(raw) <= 2*MIB and hashlib.sha256(raw).hexdigest() == args.build_sha256,
         "SOURCE_CONTINUATION_SELECTION_PIN")
    spec = importlib.util.spec_from_file_location("_source_continuation_selection", path)
    C = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(path), "exec"), C.__dict__)
    deadline = time.monotonic()+60

    def check():
        need(time.monotonic() < deadline, "SOURCE_CONTINUATION_SELECTION_DEADLINE")

    H = C.base(); B = H.helper()
    inputs, reused, runtime, sources = C.inspect_inputs(H, B, check)
    need(sources[C.FRESH[0]]["sha256"] == args.build_sha256 and
         sources[C.FRESH[2]]["sha256"] == args.source_sha256 and len(sources) == 11 and
         len(reused) == 12 and len(runtime) == 23, "SOURCE_CONTINUATION_SELECTION_SCOPE")
    destination = H.LOCAL/(C.NAME+".selection.json")
    B.ordinary(destination, fresh=True); B.ordinary(H.LOCAL/C.NAME, directory=True, fresh=True)
    selection = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": C.NAME,
        "sources": {key: value["sha256"] for key, value in sources.items()},
        "runtime_pins": {key: value["sha256"] for key, value in inputs.items()},
        "argv": [str(H.PYTHON/"python.exe"), "-I", "-S", "-B", "{snapshot}/"+C.FRESH[0],
                 "--source-root", "{snapshot}", "--output", "{output}/build"],
        "limits": {"wall_seconds": 90, "cpu_seconds": 60, "memory_mib": 1536,
                   "active_processes": 4, "stdout_bytes": MIB, "stderr_bytes": MIB}}
    for filename, expected in inputs.items():
        need(B.pin(Path(filename), check, 512*MIB) == expected, "SOURCE_CONTINUATION_SELECTION_FINAL_PIN")
    raw = json.dumps(selection, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("ascii")
    need(len(raw) <= MIB, "SOURCE_CONTINUATION_SELECTION_BYTES")
    B.fresh_bytes(destination, raw)
    need(B.pin(destination, check, MIB) == {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()},
         "SOURCE_CONTINUATION_SELECTION_READBACK")
    print(json.dumps({"selection": str(destination), "sha256": hashlib.sha256(raw).hexdigest(),
                      "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()
