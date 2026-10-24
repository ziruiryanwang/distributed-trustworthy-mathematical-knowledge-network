"""Prepare separate bounded assembly/native checks for the syntax-only successor."""
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
OLD = LOCAL/"ordinary-module-anchor-assembly-01/package"
NEW = LOCAL/"ordinary-module-anchor-assembly-02/package"
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
    template = LOCAL/"ordinary-module-anchor-native-01.selection.json"
    with template.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() ==
         "6719f6e513cfffe18c71c7b170d63f737be89c4ab19204124cd1e3af90318b2b", "REPAIR_TEMPLATE_PIN")
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
    names = ["tools/Run-V5-Check.py", PREFIX+"select_repair.py"]
    prefix = [r"D:\Python314\python.exe", "-I", "-S", "-B"]
    if args.phase == "assembly":
        native = "software/v5/ordinary_module_anchor/OrdinaryModule02.lean"
        names += [PREFIX+"assemble02.py", PREFIX+"assemble.py", native, "software/v5/ordinary_package/build.py"]
        argv = prefix+["{snapshot}/"+PREFIX+"assemble02.py", "--output", "{output}/package",
                       "--native-sha256", pin(ROOT/native, 2*MIB)]
        limits = dict(wall_seconds=90, cpu_seconds=50, memory_mib=512, active_processes=2,
                      stdout_bytes=MIB, stderr_bytes=MIB)
    else:
        names += [PREFIX+"native_check02.py", "software/v5/ordinary_distribution/relocated_smoke.py"]
        argv = prefix+["{snapshot}/"+PREFIX+"native_check02.py", "--package", str(NEW),
            "--profile-sha256", pin(NEW/"PROFILE.json", 2*MIB),
            "--assembly-sha256", pin(NEW/"ASSEMBLY.json", 2*MIB),
            "--python-runtime", r"D:\Python314", "--lean-runtime", str(ROOT/"software/runtime/lean-4.34.0-windows"),
            "--output", "{output}/native", "--wall-seconds", "240", "--cpu-seconds", "140", "--memory-mib", "1536"]
        limits = old["limits"]
        saved = LOCAL/"ordinary-current-relocated-smoke-01/smoke/catalog/module-anchors-v1"
        operation = saved/"operations/f08b3ae81225416bbdbfe37f0ebeeea20e3628cf31696ee558622b2ed6b6733b"
        for path in (saved/"STORE.json", operation/"RESERVATION.json", operation/"CLOSED.json"):
            runtime[str(path)] = pin(path, 2*MIB)
    sources = {name: pin(ROOT/name, 2*MIB) for name in names}
    if args.phase == "assembly":
        for name, digest in sources.items():
            if name != "tools/Run-V5-Check.py":
                runtime[str(ROOT/name)] = digest
    need(len(runtime) <= 256, "REPAIR_RUNTIME_BOUND")
    name = "ordinary-module-anchor-"+args.phase+"-02"
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
