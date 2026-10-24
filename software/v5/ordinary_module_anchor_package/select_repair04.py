"""Select one-file native guard and changed-boundary integration; no old run retry."""
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
PREFIX = "software/v5/ordinary_module_anchor_package/"
OLD = LOCAL/"ordinary-module-anchor-assembly-03/package"
NEW = LOCAL/"ordinary-module-anchor-assembly-04/package"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("phase", choices=("assembly", "native"))
    args = parser.parse_args()
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "REPAIR_SELECTION_CONTEXT")
    builder = ROOT/"software/v5/ordinary_package/build.py"
    with builder.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() ==
         "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5", "REPAIR_BUILDER_PIN")
    spec = importlib.util.spec_from_file_location("_repair_selector_builder", builder)
    B = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(builder), "exec"), B.__dict__)
    deadline = time.monotonic()+60
    def check():
        need(time.monotonic() < deadline, "REPAIR_SELECTION_DEADLINE")
    def pin(path, maximum=128*MIB):
        return B.pin(path, check, maximum)["sha256"]
    template = LOCAL/"ordinary-module-anchor-native-03.selection.json"
    with template.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() ==
         "c7adf47b588478de428539d088c64e40c55a750fe7219c01f2cf6e9029066f79", "REPAIR_TEMPLATE_PIN")
    old = json.loads(raw)
    runtime = {}
    for name, expected in old["runtime_pins"].items():
        path = Path(name)
        target = NEW/path.relative_to(OLD) if args.phase == "native" and path.is_relative_to(OLD) else path
        actual = pin(target)
        if target == path:
            need(actual == expected, "REPAIR_UNCHANGED_RUNTIME:"+name)
        elif path.name not in ("PROFILE.json", "ASSEMBLY.json") and path != OLD/"module/OrdinaryModule.lean":
            need(actual == expected, "REPAIR_EXACT_ONE_PAYLOAD:"+name)
        runtime[str(target)] = actual
    names = ["tools/Run-V5-Check.py", PREFIX+"select_repair04.py"]
    prefix = [r"D:\Python314\python.exe", "-I", "-S", "-B"]
    if args.phase == "assembly":
        native = "software/v5/ordinary_module_anchor/OrdinaryModule04.lean"
        names += [PREFIX+"assemble04.py", PREFIX+"assemble.py", native,
                  "software/v5/ordinary_query_context/query.py", "software/v5/ordinary_package/build.py"]
        argv = prefix+["{snapshot}/"+PREFIX+"assemble04.py", "--output", "{output}/package",
                       "--native-sha256", pin(ROOT/native, 2*MIB)]
        limits = dict(wall_seconds=90, cpu_seconds=50, memory_mib=512, active_processes=2,
                      stdout_bytes=MIB, stderr_bytes=MIB)
    else:
        names += [PREFIX+"native_check04.py", "software/v5/ordinary_distribution/relocated_smoke.py"]
        argv = prefix+["{snapshot}/"+PREFIX+"native_check04.py", "--package", str(NEW),
            "--profile-sha256", pin(NEW/"PROFILE.json", 2*MIB),
            "--assembly-sha256", pin(NEW/"ASSEMBLY.json", 2*MIB),
            "--python-runtime", r"D:\Python314", "--lean-runtime", str(ROOT/"software/runtime/lean-4.34.0-windows"),
            "--output", "{output}/native", "--wall-seconds", "240", "--cpu-seconds", "140", "--memory-mib", "1536"]
        limits = old["limits"]
        saved = LOCAL/"ordinary-current-relocated-smoke-01/smoke/catalog/module-anchors-v1"
        # Preserve every current registry byte, including all closed failures and A.
        held = []
        for directory, dirs, files in os.walk(saved, followlinks=False):
            check()
            need(len(dirs)+len(files) <= 64, "REPAIR_SIDECAR_DIRECTORY_BOUND")
            for entry in dirs:
                B.ordinary(Path(directory)/entry, directory=True)
            for entry in files:
                held.append(Path(directory)/entry)
                need(len(held) <= 32, "REPAIR_SIDECAR_FILE_BOUND")
        need(len(held) == 20, "REPAIR_EXPECTED_PRESERVED_SIDECAR")
        for path in held:
            runtime[str(path)] = pin(path, 2*MIB)
    sources = {name: pin(ROOT/name, 2*MIB) for name in names}
    if args.phase == "assembly":
        for name, digest in sources.items():
            if name != "tools/Run-V5-Check.py":
                runtime[str(ROOT/name)] = digest
    need(len(runtime) <= 256, "REPAIR_RUNTIME_BOUND")
    name = "ordinary-module-anchor-"+args.phase+"-04"
    target = LOCAL/(name+".selection.json")
    B.ordinary(target, fresh=True); B.ordinary(LOCAL/name, directory=True, fresh=True)
    selection = dict(schema="DMKN_V5_LOCAL_CHECK_V1", name=name, sources=sources,
                     runtime_pins=runtime, argv=argv, limits=limits)
    raw = json.dumps(selection, sort_keys=True, separators=(",", ":")).encode("ascii")
    B.fresh_bytes(target, raw)
    print(json.dumps({"selection": str(target), "sha256": hashlib.sha256(raw).hexdigest(),
                      "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()
