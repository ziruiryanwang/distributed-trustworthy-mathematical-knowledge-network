"""Select one finite inert producer-controller control; never launch it."""
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
NAME = "ordinary-baseline-production-controls-01"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
MIB = 1024**2
FIXTURES = {
    "ordinary-package-lifecycle-continuation-01/contribution/evidence/"
    "25ae588e95228a64196a576aa9c9dd78249c23b0c26189c5671a434b93afa1b3.json":
        "c7266a3047afcf59059b7884853b4d6b9be4244509f260e78dd072973f9704aa",
    "ordinary-package-lifecycle-continuation-01/contribution/evidence/"
    "c4639e6e5f70e259ea1611adba8e168aa74dbfb91f98e2512cd465f82705e61e.json":
        "88c8b3b9da6bfd39fff9c827a1bec8b51ce4289c949c9d7507bfad5e53bc421f",
    "ordinary-peer-reciprocal-02/B-contribution/evidence/"
    "d52aed3d1d0f94b8ee2236a7ee84435c983c9523dca0f100f4369c183c3d4e51.json":
        "d0bb18c957c41f3f15d0b47b4eda2f41b8c1f72107d5065929625228a63558ae",
}


def need(ok, code):
    if not ok:
        raise ValueError(code)


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("controls-sha256", "bundle-sha256", "production-sha256", "worker-sha256"):
        parser.add_argument("--"+key, required=True)
    args = parser.parse_args()
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "PRODUCTION_SELECTION_CONTEXT")
    for digest in vars(args).values():
        need(len(digest) == 64 and all(c in "0123456789abcdef" for c in digest), "PRODUCTION_SELECTION_HASH")
    builder = ROOT/"software/v5/ordinary_package/build.py"
    raw = builder.read_bytes()
    need(hashlib.sha256(raw).hexdigest() ==
         "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5", "PRODUCTION_SELECTION_BUILDER")
    spec = importlib.util.spec_from_file_location("_production_selection_builder", builder)
    B = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(builder), "exec"), B.__dict__)
    deadline, runtime = time.monotonic()+60, {}

    def check():
        need(time.monotonic() < deadline, "PRODUCTION_SELECTION_DEADLINE")

    def pin(path, expected=None):
        value = B.pin(path, check, 128*MIB)["sha256"]
        need(expected is None or value == expected, "PRODUCTION_SELECTION_PIN:"+str(path))
        runtime[str(path)] = value
        return value

    template = LOCAL/"ordinary-preview-public-01.selection.json"
    template_hash = "613e28c8da5fde5d5e570e46d52bfe94cb56b6fa2b0c6037f26592095796c5c7"
    pin(template, template_hash)
    raw = template.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == template_hash, "PRODUCTION_SELECTION_TEMPLATE_CHANGED")
    # Retain only immutable package/runtime bytes, never old state or allowances.
    selected = {name: digest for name, digest in json.loads(raw)["runtime_pins"].items()
                if any(Path(name).is_relative_to(root) for root in (PACKAGE, PYTHON, LEAN))}
    need(len(selected) >= 140, "PRODUCTION_SELECTION_RUNTIME_CENSUS")
    for name, digest in selected.items():
        pin(Path(name), digest)
    for relative, digest in FIXTURES.items():
        pin(LOCAL/relative, digest)
    expected = {PREFIX+"production_controls.py": args.controls_sha256,
                PREFIX+"baseline_bundle.py": args.bundle_sha256,
                PREFIX+"baseline_production.py": args.production_sha256,
                PREFIX+"baseline_worker.py": args.worker_sha256}
    sources = {name: pin(ROOT/name, digest) for name, digest in expected.items()}
    for name in (PREFIX+"select_production_controls.py", "tools/Run-V5-Check.py"):
        sources[name] = pin(ROOT/name)
    pin(builder)
    need(len(runtime) <= 256, "PRODUCTION_SELECTION_PIN_COUNT")
    destination = LOCAL/(NAME+".selection.json")
    B.ordinary(destination, fresh=True); B.ordinary(LOCAL/NAME, directory=True, fresh=True)
    selection = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": NAME,
        "sources": sources, "runtime_pins": runtime,
        "argv": [str(PYTHON/"python.exe"), "-I", "-S", "-B", "{snapshot}/"+PREFIX+"production_controls.py",
                 "--package", str(PACKAGE), "--output", "{output}/controls"],
        "limits": {"wall_seconds": 60, "cpu_seconds": 35, "memory_mib": 768, "active_processes": 2,
                   "stdout_bytes": MIB, "stderr_bytes": MIB}}
    raw = json.dumps(selection, sort_keys=True, separators=(",", ":")).encode("ascii")
    B.fresh_bytes(destination, raw)
    print(json.dumps({"selection": str(destination), "sha256": hashlib.sha256(raw).hexdigest(),
                      "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()
