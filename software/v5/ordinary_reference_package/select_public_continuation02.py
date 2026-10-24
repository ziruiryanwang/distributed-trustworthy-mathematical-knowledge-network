"""Select one five-call retained-owner continuation; no owner or compiler is run here.

The caller supplies independently reviewed workflow and actual package pins.
All child calls share a single finite parent envelope. No failed/old run renews.
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
    for name in ("workflow-sha256", "profile-sha256", "assembly-sha256"):
        parser.add_argument("--"+name, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "REFERENCE_WORKFLOW_SELECTION_CONTEXT")
    for digest in vars(args).values():
        need(len(digest) == 64 and all(c in "0123456789abcdef" for c in digest),
             "REFERENCE_WORKFLOW_SELECTION_HASH")
    path = ROOT/PREFIX/"public_continuation02.py"
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(0 < len(raw) <= 2*MIB and hashlib.sha256(raw).hexdigest() == args.workflow_sha256,
         "REFERENCE_WORKFLOW_SELECTION_SOURCE_PIN")
    module_name = "_selected_reference_public_workflow"
    need(module_name not in sys.modules, "REFERENCE_WORKFLOW_SELECTION_PRELOADED")
    spec = importlib.util.spec_from_file_location(module_name, path)
    W = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = W
    try:
        exec(compile(raw, str(path), "exec"), W.__dict__)
    except BaseException:
        del sys.modules[module_name]
        raise
    started, cpu = time.monotonic(), time.process_time()

    def check():
        need(time.monotonic()-started < 60 and time.process_time()-cpu < 40,
             "REFERENCE_WORKFLOW_SELECTION_ALLOWANCE")

    h = W.helpers()
    need(Path(sys.executable).resolve() == W.PYTHON/"python.exe", "REFERENCE_WORKFLOW_SELECTION_PYTHON")
    target = W.LOCAL/(W.NAME+".selection.json")
    h.ordinary(target, fresh=True)
    h.ordinary(W.LOCAL/W.NAME, directory=True, fresh=True)
    inspected = W.inspect_static(h, args.profile_sha256, args.assembly_sha256, check)
    names = (PREFIX+"public_continuation02.py", PREFIX+"select_public_continuation02.py",
             "software/v5/ordinary_distribution/relocated_smoke.py", "tools/Run-V5-Check.py")
    sources = {name: h.pin(ROOT/name, check, 2*MIB)["sha256"] for name in names}
    need(sources[PREFIX+"public_continuation02.py"] == args.workflow_sha256 and
         sources["software/v5/ordinary_distribution/relocated_smoke.py"] == W.HELPER_SHA,
         "REFERENCE_WORKFLOW_SELECTION_REVIEWED_SOURCES")
    runtime = {filename: pin["sha256"] for filename, pin in inspected["pins"].items()}
    need(len(runtime) <= 256, "REFERENCE_WORKFLOW_SELECTION_INPUT_COUNT")
    selection = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": W.NAME,
        "sources": sources, "runtime_pins": runtime,
        "argv": [str(W.PYTHON/"python.exe"), "-I", "-S", "-B",
            "{snapshot}/"+PREFIX+"public_continuation02.py",
            "--profile-sha256", args.profile_sha256, "--assembly-sha256", args.assembly_sha256,
            "--output", "{output}/workflow", "--wall-seconds", "420", "--cpu-seconds", "260",
            "--memory-mib", "1536"],
        "limits": {"wall_seconds": 480, "cpu_seconds": 320, "memory_mib": 1792,
                   "active_processes": 8, "stdout_bytes": 4*MIB, "stderr_bytes": MIB}}
    for filename, expected in inspected["pins"].items():
        need(h.pin(Path(filename), check, 128*MIB) == expected, "REFERENCE_WORKFLOW_SELECTION_INPUT_CHANGED")
    for name, digest in sources.items():
        need(h.pin(ROOT/name, check, 2*MIB)["sha256"] == digest, "REFERENCE_WORKFLOW_SELECTION_SOURCE_CHANGED")
    raw = h.canonical(selection)
    need(len(raw) <= MIB, "REFERENCE_WORKFLOW_SELECTION_SIZE")
    expected = h.save(target, raw)
    need(h.pin(target, check, MIB) == expected, "REFERENCE_WORKFLOW_SELECTION_READBACK")
    print(json.dumps({"selection": str(target), "sha256": expected["sha256"],
        "runtime_pin_count": len(runtime), "public_calls": 5, "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()

