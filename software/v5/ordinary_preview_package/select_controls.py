"""Select one finite preview control run; never launch it."""
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
PREFIX = "software/v5/ordinary_preview_package/"
PACKAGE = LOCAL/"ordinary-project-extraction-build-01/integration/package"
FIXTURE = LOCAL/"ordinary-project-extraction-public-01/project/completion/previews/d0c7be50520d2b91b72e43308b8f1ec75022b32c37fe9561381f4aef879fff1a.json"
NAME = "ordinary-preview-controls-01"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("controls-sha256", "api-sha256", "entry-sha256"):
        parser.add_argument("--"+key, required=True)
    args = parser.parse_args()
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode and not sys.flags.optimize, "PREVIEW_SELECTION_CONTEXT")
    for digest in vars(args).values():
        need(len(digest) == 64 and all(c in "0123456789abcdef" for c in digest), "PREVIEW_SELECTION_HASH")
    builder = ROOT/"software/v5/ordinary_package/build.py"
    data = builder.read_bytes()
    need(hashlib.sha256(data).hexdigest() ==
         "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5", "PREVIEW_SELECTION_BUILDER")
    spec = importlib.util.spec_from_file_location("_preview_selection_builder", builder)
    B = importlib.util.module_from_spec(spec)
    exec(compile(data, str(builder), "exec"), B.__dict__)
    until, runtime = time.monotonic()+60, {}
    def check():
        need(time.monotonic() < until, "PREVIEW_SELECTION_DEADLINE")
    def pin(path, expected=None):
        value = B.pin(path, check, 128*MIB)["sha256"]
        need(expected is None or value == expected, "PREVIEW_SELECTION_PIN:"+str(path))
        runtime[str(path)] = value
        return value
    template = LOCAL/"ordinary-project-extraction-public-01.selection.json"
    template_hash = "2f298613971e2ffbb33c818061195a5ac4d7fd7359d38a9ed3b7c0497b857dfe"
    pin(template, template_hash)
    data = template.read_bytes()
    need(hashlib.sha256(data).hexdigest() == template_hash, "PREVIEW_SELECTION_TEMPLATE_CHANGED")
    # Reuse only immutable supported package/runtime pins, not the owner state
    # or prior harness. The actual control loader independently checks the map.
    selected = {name: digest for name, digest in json.loads(data)["runtime_pins"].items()
                if any(Path(name).is_relative_to(root) for root in (PACKAGE, PYTHON, LEAN))}
    need(len(selected) >= 140, "PREVIEW_SELECTION_RUNTIME_CENSUS")
    for name, digest in selected.items():
        pin(Path(name), digest)
    pin(FIXTURE, "362292c8237bd4cf0f9127ed5575723f188b51efa7ab0a784ac0bf1c1489193c")
    expected = {PREFIX+"controls.py": args.controls_sha256, PREFIX+"peer_api.py": args.api_sha256,
                PREFIX+"peer.py": args.entry_sha256}
    sources = {name: pin(ROOT/name, digest) for name, digest in expected.items()}
    for name in (PREFIX+"select_controls.py", "tools/Run-V5-Check.py"):
        sources[name] = pin(ROOT/name)
    need(len(runtime) <= 256, "PREVIEW_SELECTION_PIN_COUNT")
    destination = LOCAL/(NAME+".selection.json")
    B.ordinary(destination, fresh=True); B.ordinary(LOCAL/NAME, directory=True, fresh=True)
    selection = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": NAME, "sources": sources,
        "runtime_pins": runtime,
        "argv": [str(PYTHON/"python.exe"), "-I", "-S", "-B", "{snapshot}/"+PREFIX+"controls.py",
                 "--package", str(PACKAGE), "--preview", str(FIXTURE), "--output", "{output}/controls"],
        "limits": {"wall_seconds": 60, "cpu_seconds": 35, "memory_mib": 768, "active_processes": 2,
                   "stdout_bytes": MIB, "stderr_bytes": MIB}}
    data = json.dumps(selection, sort_keys=True, separators=(",", ":")).encode("ascii")
    B.fresh_bytes(destination, data)
    print(json.dumps({"selection": str(destination), "sha256": hashlib.sha256(data).hexdigest(),
                      "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()
