"""Select one finite thin-delta integration only after actual A export review.

This selector reads inert files and writes fresh selection metadata. It does not
open an owner, compile, register, intake, materialize or launch the workflow.
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
PREFIX = "software/v5/ordinary_thin_delta/"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("workflow-sha256", "profile-sha256", "assembly-sha256", "bundle-manifest-sha256"):
        parser.add_argument("--"+name, required=True)
    parser.add_argument("--bundle-directory", required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "THIN_SELECTION_CONTEXT")
    for value in (args.workflow_sha256, args.profile_sha256, args.assembly_sha256, args.bundle_manifest_sha256):
        need(len(value) == 64 and all(c in "0123456789abcdef" for c in value), "THIN_SELECTION_HASH")
    path = ROOT/PREFIX/"integrate.py"
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(0 < len(raw) <= 2*MIB and hashlib.sha256(raw).hexdigest() == args.workflow_sha256, "THIN_SELECTION_SOURCE_PIN")
    name = "_selected_thin_integration"
    need(name not in sys.modules, "THIN_SELECTION_PRELOADED")
    spec = importlib.util.spec_from_file_location(name, path)
    W = importlib.util.module_from_spec(spec); sys.modules[name] = W
    exec(compile(raw, str(path), "exec"), W.__dict__)
    started, cpu = time.monotonic(), time.process_time()

    def check():
        need(time.monotonic()-started < 60 and time.process_time()-cpu < 40, "THIN_SELECTION_ALLOWANCE")

    h = W.helpers()
    need(Path(sys.executable).resolve() == W.PYTHON/"python.exe", "THIN_SELECTION_PYTHON")
    target = W.LOCAL/(W.NAME+".selection.json")
    h.ordinary(target, fresh=True); h.ordinary(W.LOCAL/W.NAME, directory=True, fresh=True)
    inspected = W.inspect_static(h, args, check)
    names = (PREFIX+"integrate.py", PREFIX+"select_integration.py",
             "software/v5/ordinary_distribution/relocated_smoke.py", "tools/Run-V5-Check.py")
    sources = {name: h.pin(ROOT/name, check, 2*MIB)["sha256"] for name in names}
    need(sources[PREFIX+"integrate.py"] == args.workflow_sha256 and
         sources["software/v5/ordinary_distribution/relocated_smoke.py"] == W.HELPER_SHA, "THIN_SELECTION_REVIEWED_SOURCE")
    runtime = {path: pin["sha256"] for path, pin in inspected["pins"].items()}
    selection = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": W.NAME, "sources": sources, "runtime_pins": runtime,
        "argv": [str(W.PYTHON/"python.exe"), "-I", "-S", "-B", "{snapshot}/"+PREFIX+"integrate.py",
            "--profile-sha256", args.profile_sha256, "--assembly-sha256", args.assembly_sha256,
            "--bundle-directory", str(inspected["bundle_directory"]),
            "--bundle-manifest-sha256", args.bundle_manifest_sha256, "--output", "{output}/workflow",
            "--wall-seconds", "500", "--cpu-seconds", "350", "--memory-mib", "1536"],
        "limits": {"wall_seconds": 600, "cpu_seconds": 450, "memory_mib": 1792,
                   "active_processes": 8, "stdout_bytes": 4*MIB, "stderr_bytes": MIB}}
    for path, expected in inspected["pins"].items():
        need(h.pin(Path(path), check, 128*MIB) == expected, "THIN_SELECTION_INPUT_CHANGED")
    for name, expected in sources.items():
        need(h.pin(ROOT/name, check, 2*MIB)["sha256"] == expected, "THIN_SELECTION_SOURCE_CHANGED")
    raw = h.canonical(selection)
    need(len(raw) <= MIB, "THIN_SELECTION_SIZE")
    pin = h.save(target, raw)
    need(h.pin(target, check, MIB) == pin, "THIN_SELECTION_READBACK")
    print(json.dumps({"selection": str(target), "sha256": pin["sha256"], "runtime_pin_count": len(runtime),
        "public_owner_calls": 4, "ordinary_compile_calls": 1, "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()
