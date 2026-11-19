"""Pin a reviewed three-command diagnostic probe build; never launch it."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PREFIX = "software/v5/ordinary_baseline/"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--build-sha256", required=True)
    parser.add_argument("--probe-sha256", required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "REFERENCE_PROBE_SELECTION_CONTEXT")
    for value in vars(args).values():
        need(len(value) == 64 and all(c in "0123456789abcdef" for c in value), "REFERENCE_PROBE_SELECTION_HASH")
    path = ROOT/PREFIX/"build_reference_probe.py"
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(len(raw) <= 2*MIB and hashlib.sha256(raw).hexdigest() == args.build_sha256,
         "REFERENCE_PROBE_SELECTION_ADAPTER_PIN")
    spec = importlib.util.spec_from_file_location("_selected_reference_probe_build", path)
    H = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(path), "exec"), H.__dict__)
    deadline = time.monotonic()+60

    def check():
        need(time.monotonic() < deadline, "REFERENCE_PROBE_SELECTION_DEADLINE")

    B = H.helper()
    inputs, reused, runtime, sources = H.inspect_inputs(B, check)
    need(sources[PREFIX+"build_reference_probe.py"]["sha256"] == args.build_sha256 and
         sources[PREFIX+H.PROBE+".lean"]["sha256"] == args.probe_sha256 and
         len(sources) == 5 and len(reused) == 12 and len(runtime) == 23,
         "REFERENCE_PROBE_SELECTION_REVIEWED_SCOPE")
    destination = H.LOCAL/(H.NAME+".selection.json")
    B.ordinary(destination, fresh=True); B.ordinary(H.LOCAL/H.NAME, directory=True, fresh=True)
    selection = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": H.NAME,
        "sources": {key: value["sha256"] for key, value in sources.items()},
        "runtime_pins": {key: value["sha256"] for key, value in inputs.items()},
        "argv": [str(H.PYTHON/"python.exe"), "-I", "-S", "-B",
                 "{snapshot}/"+PREFIX+"build_reference_probe.py", "--source-root", "{snapshot}",
                 "--output", "{output}/build"],
        "limits": {"wall_seconds": 120, "cpu_seconds": 60, "memory_mib": 1536,
                   "active_processes": 4, "stdout_bytes": MIB, "stderr_bytes": MIB}}
    for path, expected in inputs.items():
        need(B.pin(Path(path), check, 512*MIB) == expected, "REFERENCE_PROBE_SELECTION_FINAL_PIN")
    raw = json.dumps(selection, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("ascii")
    need(len(raw) <= MIB, "REFERENCE_PROBE_SELECTION_BYTES")
    B.fresh_bytes(destination, raw)
    need(B.pin(destination, check, MIB) == {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()},
         "REFERENCE_PROBE_SELECTION_READBACK")
    print(json.dumps({"selection": str(destination), "sha256": hashlib.sha256(raw).hexdigest(),
                      "runtime_pin_count": len(inputs), "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()
