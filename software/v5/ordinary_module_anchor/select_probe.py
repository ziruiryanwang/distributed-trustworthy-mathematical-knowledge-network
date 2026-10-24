"""Select the three-process saved-artifact Windows-path discriminator only."""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
PREFIX = "software/v5/ordinary_module_anchor/"
NAME = "ordinary-module-anchor-long-path-01"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def main():
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and len(sys.argv) == 1, "PROBE_SELECTION_CONTEXT")
    builder = ROOT/"software/v5/ordinary_package/build.py"
    with builder.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() ==
         "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5", "PROBE_BUILDER_PIN")
    spec = importlib.util.spec_from_file_location("_path_probe_builder", builder)
    B = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(builder), "exec"), B.__dict__)
    deadline = time.monotonic()+60
    def check():
        need(time.monotonic() < deadline, "PROBE_SELECTION_DEADLINE")
    def pin(path):
        return B.pin(path, check, 128*MIB)["sha256"]
    with (LOCAL/"ordinary-module-anchor-native-02.selection.json").open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() ==
         "bf253a11b52a5f84c157a1165f69d869636a5aa960217db2c8e99faa69b2f752", "PROBE_TEMPLATE_PIN")
    runtime = json.loads(raw)["runtime_pins"]
    for name, digest in runtime.items():
        need(pin(Path(name)) == digest, "PROBE_RUNTIME_CHANGED")
    probe = ROOT/PREFIX/"long_path_probe.py"
    with probe.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() ==
         "dba7aa027d8e2fe7259f185283b16e76b2622ac9363902ead6403fd47d3d93b1", "PROBE_LAUNCHER_PIN")
    spec = importlib.util.spec_from_file_location("_selected_path_probe", probe)
    P = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(probe), "exec"), P.__dict__)
    for suffix, size, digest in P.PARTS:
        path = P.DIRECTORY/(P.MODULE+suffix)
        need(B.pin(path, check, MIB) == {"bytes": size, "sha256": digest}, "PROBE_SAVED_ARTIFACT_PIN")
        runtime[str(path)] = digest
    names = ["tools/Run-V5-Check.py", PREFIX+"select_probe.py", PREFIX+"long_path_probe.py",
             PREFIX+"LongPathProbe.lean", PREFIX+"LongPathConsumer.lean"]
    sources = {name: pin(ROOT/name) for name in names}
    for name, digest in sources.items():
        runtime[str(ROOT/name)] = digest
    need(len(runtime) <= 256, "PROBE_RUNTIME_BOUND")
    target = LOCAL/(NAME+".selection.json")
    B.ordinary(target, fresh=True); B.ordinary(LOCAL/NAME, directory=True, fresh=True)
    selection = dict(schema="DMKN_V5_LOCAL_CHECK_V1", name=NAME, sources=sources, runtime_pins=runtime,
        argv=[r"D:\Python314\python.exe", "-I", "-S", "-B", "{snapshot}/"+PREFIX+"long_path_probe.py",
              "--output", "{output}/PROBE.json"],
        limits=dict(wall_seconds=100, cpu_seconds=50, memory_mib=2048, active_processes=4,
                    stdout_bytes=MIB, stderr_bytes=MIB))
    raw = json.dumps(selection, sort_keys=True, separators=(",", ":")).encode("ascii")
    B.fresh_bytes(target, raw)
    print(json.dumps({"selection": str(target), "sha256": hashlib.sha256(raw).hexdigest(),
                      "runtime": "NOT_STARTED"}))


if __name__ == "__main__":
    main()
