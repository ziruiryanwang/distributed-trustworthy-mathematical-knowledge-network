"""Select one finite file-only reference package assembly; never launch it.

The caller supplies reviewed assembler and complete fresh-payload-map hashes.
Every source is snapshotted by the existing outer runner before assembly. All
retained package/native inputs are exact runtime pins, not rediscovered paths.
"""
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
    parser.add_argument("--assemble-sha256", required=True)
    parser.add_argument("--payload-map-sha256", required=True)
    for name in ("source-build-sha256", "source-result-sha256", "source-selection-sha256"):
        parser.add_argument("--"+name, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "REFERENCE_ASSEMBLY_SELECTION_CONTEXT")
    for value in vars(args).values():
        need(len(value) == 64 and all(c in "0123456789abcdef" for c in value),
             "REFERENCE_ASSEMBLY_SELECTION_HASH")
    path = ROOT/PREFIX/"assemble.py"
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(0 < len(raw) <= 2*MIB and hashlib.sha256(raw).hexdigest() == args.assemble_sha256,
         "REFERENCE_ASSEMBLY_SELECTION_ADAPTER_PIN")
    name = "_selected_reference_package_assembler"
    need(name not in sys.modules, "REFERENCE_ASSEMBLY_SELECTION_PRELOADED")
    spec = importlib.util.spec_from_file_location(name, path)
    S = importlib.util.module_from_spec(spec)
    sys.modules[name] = S
    try:
        exec(compile(raw, str(path), "exec"), S.__dict__)
    except BaseException:
        del sys.modules[name]
        raise
    started, cpu = time.monotonic(), time.process_time()

    def check():
        need(time.monotonic()-started < 60 and time.process_time()-cpu < 40,
             "REFERENCE_ASSEMBLY_SELECTION_ALLOWANCE")

    B = S.helper()
    need(Path(sys.executable).resolve() == S.PYTHON/"python.exe", "REFERENCE_ASSEMBLY_SELECTION_PYTHON")
    target = S.LOCAL/(S.NAME+".selection.json")
    B.ordinary(target, fresh=True)
    B.ordinary(S.LOCAL/S.NAME, directory=True, fresh=True)
    source_provenance = {"build/BUILD.json": args.source_build_sha256,
                         "RESULT.json": args.source_result_sha256,
                         "selection.json": args.source_selection_sha256}
    inputs = S.inspect_inputs(B, check, ROOT, source_provenance)
    payload_hash = hashlib.sha256(S.encoded(inputs["source_pins"])).hexdigest()
    need(payload_hash == args.payload_map_sha256, "REFERENCE_ASSEMBLY_SELECTION_REVIEWED_MAP")
    source_names = {PREFIX+"assemble.py", PREFIX+"select_assembly.py", S.BUILDER,
                    "tools/Run-V5-Check.py", *S.SOURCES.values()}
    sources = {relative: B.pin(ROOT/relative, check, 2*MIB)["sha256"]
               for relative in sorted(source_names)}
    need(sources[PREFIX+"assemble.py"] == args.assemble_sha256 and
         sources[S.BUILDER] == S.BUILDER_SHA and len(sources) == 24 and
         all(sources[relative] == inputs["source_pins"][logical]["sha256"]
             for logical, relative in S.SOURCES.items()), "REFERENCE_ASSEMBLY_SELECTION_SOURCES")
    runtime = {path: value["sha256"] for path, value in inputs["pins"].items()}
    runtime[str(ROOT/S.BUILDER)] = sources[S.BUILDER]
    need(len(runtime) <= 256, "REFERENCE_ASSEMBLY_SELECTION_RUNTIME_CENSUS")
    selection = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": S.NAME,
        "sources": sources, "runtime_pins": runtime,
        "argv": [str(S.PYTHON/"python.exe"), "-I", "-S", "-B",
                 "{snapshot}/"+PREFIX+"assemble.py", "--source-root", "{snapshot}",
                 "--output", "{output}/package", "--payload-map-sha256", payload_hash,
                 "--source-build-sha256", args.source_build_sha256,
                 "--source-result-sha256", args.source_result_sha256,
                 "--source-selection-sha256", args.source_selection_sha256],
        "limits": {"wall_seconds": 90, "cpu_seconds": 50, "memory_mib": 512,
                   "active_processes": 2, "stdout_bytes": MIB, "stderr_bytes": MIB}}
    for filename, expected in inputs["pins"].items():
        need(B.pin(Path(filename), check, 128*MIB) == expected,
             "REFERENCE_ASSEMBLY_SELECTION_INPUT_CHANGED")
    for relative, digest in sources.items():
        need(B.pin(ROOT/relative, check, 2*MIB)["sha256"] == digest,
             "REFERENCE_ASSEMBLY_SELECTION_SOURCE_CHANGED")
    raw = S.encoded(selection)
    need(len(raw) <= MIB, "REFERENCE_ASSEMBLY_SELECTION_BYTES")
    B.fresh_bytes(target, raw)
    digest = hashlib.sha256(raw).hexdigest()
    need(B.pin(target, check, MIB) == {"bytes": len(raw), "sha256": digest},
         "REFERENCE_ASSEMBLY_SELECTION_READBACK")
    print(json.dumps({"selection": str(target), "sha256": digest,
        "payload_map_sha256": payload_hash, "runtime_pin_count": len(runtime),
        "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()
