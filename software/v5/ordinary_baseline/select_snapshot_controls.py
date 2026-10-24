"""Select one finite synthetic-artifact snapshot control; never launch it."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
PREFIX = "software/v5/ordinary_baseline/"
PACKAGE = LOCAL/"ordinary-preview-assembly-01/package"
NAME = "ordinary-baseline-snapshot-controls-01"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--controls-sha256", required=True)
    parser.add_argument("--snapshot-sha256", required=True)
    args = parser.parse_args()
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "SNAPSHOT_SELECTION_CONTEXT")
    for digest in vars(args).values():
        need(len(digest) == 64 and all(c in "0123456789abcdef" for c in digest), "SNAPSHOT_SELECTION_HASH")
    builder = ROOT/"software/v5/ordinary_package/build.py"
    raw = builder.read_bytes()
    need(hashlib.sha256(raw).hexdigest() ==
         "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5", "SNAPSHOT_SELECTION_BUILDER")
    spec = importlib.util.spec_from_file_location("_snapshot_selection_builder", builder)
    B = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(builder), "exec"), B.__dict__)
    deadline, runtime = time.monotonic()+60, {}

    def check():
        need(time.monotonic() < deadline, "SNAPSHOT_SELECTION_DEADLINE")

    def pin(path, expected=None):
        value = B.pin(path, check, 128*MIB)["sha256"]
        need(expected is None or value == expected, "SNAPSHOT_SELECTION_PIN:"+str(path))
        runtime[str(path)] = value
        return value

    template = LOCAL/"ordinary-preview-public-01.selection.json"
    template_hash = "613e28c8da5fde5d5e570e46d52bfe94cb56b6fa2b0c6037f26592095796c5c7"
    pin(template, template_hash)
    raw = template.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == template_hash, "SNAPSHOT_SELECTION_TEMPLATE_CHANGED")
    # Only frozen package/runtime bytes survive, not state or old allowances.
    selected = {name: digest for name, digest in json.loads(raw)["runtime_pins"].items()
                if any(Path(name).is_relative_to(root) for root in (PACKAGE, PYTHON, LEAN))}
    need(len(selected) >= 140, "SNAPSHOT_SELECTION_RUNTIME_CENSUS")
    for name, digest in selected.items():
        pin(Path(name), digest)
    expected = {PREFIX+"snapshot_controls.py": args.controls_sha256,
                PREFIX+"baseline_snapshot.py": args.snapshot_sha256}
    sources = {name: pin(ROOT/name, digest) for name, digest in expected.items()}
    for name in (PREFIX+"select_snapshot_controls.py", "tools/Run-V5-Check.py"):
        sources[name] = pin(ROOT/name)
    pin(builder)
    need(len(runtime) <= 256, "SNAPSHOT_SELECTION_PIN_COUNT")
    destination = LOCAL/(NAME+".selection.json")
    B.ordinary(destination, fresh=True); B.ordinary(LOCAL/NAME, directory=True, fresh=True)
    selection = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": NAME,
        "sources": sources, "runtime_pins": runtime,
        "argv": [str(PYTHON/"python.exe"), "-I", "-S", "-B", "{snapshot}/"+PREFIX+"snapshot_controls.py",
                 "--package", str(PACKAGE), "--output", "{output}/controls"],
        "limits": {"wall_seconds": 60, "cpu_seconds": 35, "memory_mib": 768, "active_processes": 2,
                   "stdout_bytes": MIB, "stderr_bytes": MIB}}
    raw = json.dumps(selection, sort_keys=True, separators=(",", ":")).encode("ascii")
    B.fresh_bytes(destination, raw)
    print(json.dumps({"selection": str(destination), "sha256": hashlib.sha256(raw).hexdigest(),
                      "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()
