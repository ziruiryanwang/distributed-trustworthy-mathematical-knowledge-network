"""Select the bounded file-only three-overlay successor; never launch it."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PREFIX = "software/v5/ordinary_reference_package/"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("assemble-sha256", "payload-map-sha256"):
        parser.add_argument("--"+name, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "REFERENCE_SUCCESSOR_SELECTION_CONTEXT")
    for value in vars(args).values():
        need(len(value) == 64 and all(c in "0123456789abcdef" for c in value),
             "REFERENCE_SUCCESSOR_SELECTION_HASH")
    path = ROOT/PREFIX/"assemble02.py"
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(0 < len(raw) <= 2*MIB and hashlib.sha256(raw).hexdigest() == args.assemble_sha256,
         "REFERENCE_SUCCESSOR_SELECTION_ADAPTER_PIN")
    name = "_selected_reference_successor_assembler"
    need(name not in sys.modules, "REFERENCE_SUCCESSOR_SELECTION_PRELOADED")
    spec = importlib.util.spec_from_file_location(name, path)
    S = importlib.util.module_from_spec(spec); sys.modules[name] = S
    exec(compile(raw, str(path), "exec"), S.__dict__)
    started, cpu = time.monotonic(), time.process_time()
    def check():
        need(time.monotonic()-started < 60 and time.process_time()-cpu < 40,
             "REFERENCE_SUCCESSOR_SELECTION_ALLOWANCE")
    B = S.helper()
    need(Path(sys.executable).resolve() == S.PYTHON/"python.exe", "REFERENCE_SUCCESSOR_SELECTION_PYTHON")
    target = S.LOCAL/(S.NAME+".selection.json")
    B.ordinary(target, fresh=True); B.ordinary(S.LOCAL/S.NAME, directory=True, fresh=True)
    inputs = S.inspect_inputs(B, check, ROOT)
    payload_hash = hashlib.sha256(S.encoded(inputs["source_pins"])).hexdigest()
    need(payload_hash == args.payload_map_sha256, "REFERENCE_SUCCESSOR_SELECTION_REVIEWED_MAP")
    names = {PREFIX+"assemble02.py", PREFIX+"select_assembly02.py", S.BUILDER,
             "tools/Run-V5-Check.py", *S.SOURCES.values()}
    sources = {relative: B.pin(ROOT/relative, check, 2*MIB)["sha256"] for relative in sorted(names)}
    need(len(sources) == 7 and sources[PREFIX+"assemble02.py"] == args.assemble_sha256 and
         sources[S.BUILDER] == S.BUILDER_SHA and all(sources[filename] == inputs["source_pins"][logical]["sha256"]
             for logical, filename in S.SOURCES.items()), "REFERENCE_SUCCESSOR_SELECTION_SOURCES")
    runtime = {path: pin["sha256"] for path, pin in inputs["pins"].items()}
    runtime[str(ROOT/S.BUILDER)] = S.BUILDER_SHA
    need(len(runtime) <= 256, "REFERENCE_SUCCESSOR_SELECTION_RUNTIME_CENSUS")
    selection = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": S.NAME, "sources": sources,
        "runtime_pins": runtime,
        "argv": [str(S.PYTHON/"python.exe"), "-I", "-S", "-B", "{snapshot}/"+PREFIX+"assemble02.py",
                 "--source-root", "{snapshot}", "--output", "{output}/package", "--payload-map-sha256", payload_hash],
        "limits": {"wall_seconds": 90, "cpu_seconds": 50, "memory_mib": 512,
                   "active_processes": 2, "stdout_bytes": MIB, "stderr_bytes": MIB}}
    for filename, expected in inputs["pins"].items():
        need(B.pin(Path(filename), check, 128*MIB) == expected, "REFERENCE_SUCCESSOR_SELECTION_INPUT_CHANGED")
    for filename, digest in sources.items():
        need(B.pin(ROOT/filename, check, 2*MIB)["sha256"] == digest, "REFERENCE_SUCCESSOR_SELECTION_SOURCE_CHANGED")
    raw = S.encoded(selection); need(len(raw) <= MIB, "REFERENCE_SUCCESSOR_SELECTION_BYTES")
    B.fresh_bytes(target, raw)
    digest = hashlib.sha256(raw).hexdigest()
    need(B.pin(target, check, MIB) == {"bytes": len(raw), "sha256": digest}, "REFERENCE_SUCCESSOR_SELECTION_READBACK")
    print(json.dumps({"selection": str(target), "sha256": digest, "payload_map_sha256": payload_hash,
                      "runtime_pin_count": len(runtime), "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()
