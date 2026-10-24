"""Pin final reviewed sources for one narrow native build; never launch it."""
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
    for key in ("build-sha256", "exporter-sha256", "core-sha256", "collector-sha256", "reference-sha256"):
        parser.add_argument("--"+key, required=True)
    args = parser.parse_args()
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "BASELINE_BUILD_SELECTION_CONTEXT")
    for digest in vars(args).values():
        need(len(digest) == 64 and all(c in "0123456789abcdef" for c in digest), "BASELINE_BUILD_SELECTION_HASH")
    path = ROOT/PREFIX/"build_native04.py"
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(len(raw) <= 2*MIB and hashlib.sha256(raw).hexdigest() == args.build_sha256,
         "BASELINE_BUILD_SELECTION_ADAPTER_PIN")
    spec = importlib.util.spec_from_file_location("_selected_baseline_native_build", path)
    H = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(path), "exec"), H.__dict__)
    deadline = time.monotonic()+60

    def check():
        need(time.monotonic() < deadline, "BASELINE_BUILD_SELECTION_DEADLINE")

    B = H.helper()
    pins, shared, runtime_tools, sources, exporter = H.inspect_inputs(B, check)
    required_sources = {PREFIX+"build_native04.py": args.build_sha256,
        PREFIX+"BaselineExporter.lean": args.exporter_sha256,
        PREFIX+"BaselineArtifactCore04.lean": args.core_sha256,
        PREFIX+"BaselineArtifacts04.lean": args.collector_sha256,
        PREFIX+"OrdinaryReferenceBase04.lean": args.reference_sha256}
    for name, digest in required_sources.items():
        need(sources[name]["sha256"] == digest, "BASELINE_BUILD_SELECTION_REVIEWED_SOURCE:"+name)
    need(len(shared) == 10 and len(exporter) == 3 and len(runtime_tools) == 23 and len(sources) == 8,
         "BASELINE_BUILD_SELECTION_EXACT_SCOPE")
    source_hashes = {name: pin["sha256"] for name, pin in sources.items()}
    runtime = {str(path): pin["sha256"] for path, pin in pins.items()}
    need(len(runtime) <= 64, "BASELINE_BUILD_SELECTION_PIN_BOUND")
    target = H.LOCAL/(H.NAME+".selection.json")
    B.ordinary(target, fresh=True); B.ordinary(H.LOCAL/H.NAME, directory=True, fresh=True)
    selection = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": H.NAME,
        "sources": source_hashes, "runtime_pins": runtime,
        "argv": [str(H.RUNTIMES["python_runtime"]/"python.exe"), "-I", "-S", "-B",
                 "{snapshot}/"+PREFIX+"build_native04.py", "--source-root", "{snapshot}",
                 "--output", "{output}/build"],
        "limits": {"wall_seconds": 240, "cpu_seconds": 180, "memory_mib": 1536,
                   "active_processes": 6, "stdout_bytes": MIB, "stderr_bytes": MIB}}
    # The selector reads the final currently reviewed matcher, not a draft hash
    # remembered when this adapter was authored. Bind all inputs again before
    # creating the one fresh finite selection; no compiler is run here.
    for path, expected in pins.items():
        need(B.pin(path, check, 512*MIB) == expected, "BASELINE_BUILD_SELECTION_FINAL_PIN")
    raw = json.dumps(selection, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("ascii")
    need(len(raw) <= MIB, "BASELINE_BUILD_SELECTION_BYTES")
    B.fresh_bytes(target, raw)
    need(B.pin(target, check, MIB) == {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()},
         "BASELINE_BUILD_SELECTION_READBACK")
    print(json.dumps({"selection": str(target), "sha256": hashlib.sha256(raw).hexdigest(),
                      "runtime": "NOT_STARTED", "runtime_pin_count": len(runtime)}, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
