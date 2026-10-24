"""Prepare one fresh focused context-query selection; no test/native launch."""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
PREFIX = "software/v5/ordinary_query_context/"
NAME = "ordinary-context-query-controls-01"
PYTHON = Path(r"D:\Python314")
HELPERS = ROOT/"software/v5/ordinary_lean"
FORMAL_QUERY = ROOT/"software/v5/ordinary_formal_query/formal_query.py"
FIXTURES = LOCAL/"ordinary-query-public-01/public"
CONTROLS_SHA = "bd253397494a63faa6139222667f78789ba7124f301df62f0eaed9ab2592f549"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def main():
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and len(sys.argv) == 1,
         "CONTEXT_SELECTION_PROCESS")
    builder = ROOT/"software/v5/ordinary_package/build.py"
    with builder.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() ==
         "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5",
         "CONTEXT_SELECTION_BUILDER_PIN")
    spec = importlib.util.spec_from_file_location("_context_selection_builder", builder)
    B = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(builder), "exec"), B.__dict__)
    deadline, runtime = time.monotonic()+60, {}
    def check():
        need(time.monotonic() < deadline, "CONTEXT_SELECTION_DEADLINE")
    def pin(path, expected=None):
        digest = B.pin(path, check, 128*MIB)["sha256"]
        need(expected is None or digest == expected, "CONTEXT_SELECTION_PIN:"+str(path))
        runtime[str(path)] = digest
        return digest
    template = LOCAL/"ordinary-module-anchor-native-02.selection.json"
    expected = "bf253a11b52a5f84c157a1165f69d869636a5aa960217db2c8e99faa69b2f752"
    pin(template, expected)
    with template.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() == expected, "CONTEXT_SELECTION_TEMPLATE_CHANGED")
    # Retain only the already-selected Python runtime pins: this control does
    # not load a package, Lean, native artifacts or any owner state. This remains
    # explicit-runtime selection, not a hermetic Python/OS integrity argument.
    python_pins = {name: digest for name, digest in json.loads(raw)["runtime_pins"].items()
                   if Path(name).is_relative_to(PYTHON)}
    need(set(python_pins) == {str(PYTHON/name) for name in
                             ("python.exe", "python3.dll", "python314.dll")},
         "CONTEXT_SELECTION_PYTHON_CENSUS")
    for name, digest in python_pins.items():
        pin(Path(name), digest)
    controls = ROOT/PREFIX/"controls.py"
    pin(controls, CONTROLS_SHA)
    with controls.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() == CONTROLS_SHA, "CONTEXT_SELECTION_CONTROLS_CHANGED")
    spec = importlib.util.spec_from_file_location("_selected_context_controls", controls)
    C = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(controls), "exec"), C.__dict__)
    paths = {key: HELPERS/(key+".py") for key in list(C.PINS)[:5]}
    paths.update(formal_query=FORMAL_QUERY, _context_query_entry=ROOT/PREFIX/"query.py")
    for key, digest in C.PINS.items():
        pin(paths[key], digest)
    for name, digest in C.FIXTURE_PINS.items():
        pin(FIXTURES/name, digest)
    pin(builder)
    names = ["tools/Run-V5-Check.py", PREFIX+"select_controls.py", PREFIX+"controls.py", PREFIX+"query.py"]
    sources = {name: pin(ROOT/name) for name in names}
    need(sources[PREFIX+"controls.py"] == CONTROLS_SHA and
         sources[PREFIX+"query.py"] == C.PINS["_context_query_entry"], "CONTEXT_SELECTION_SOURCE_CHANGED")
    need(len(runtime) <= 256, "CONTEXT_SELECTION_RUNTIME_BOUND")
    destination = LOCAL/(NAME+".selection.json")
    B.ordinary(destination, fresh=True); B.ordinary(LOCAL/NAME, directory=True, fresh=True)
    selection = dict(schema="DMKN_V5_LOCAL_CHECK_V1", name=NAME, sources=sources, runtime_pins=runtime,
        argv=[str(PYTHON/"python.exe"), "-I", "-S", "-B", "{snapshot}/"+PREFIX+"controls.py",
              "--helpers", str(HELPERS), "--formal-query", str(FORMAL_QUERY),
              "--fixtures", str(FIXTURES), "--output", "{output}/controls"],
        limits=dict(wall_seconds=60, cpu_seconds=35, memory_mib=512, active_processes=2,
                    stdout_bytes=MIB, stderr_bytes=MIB))
    raw = json.dumps(selection, sort_keys=True, separators=(",", ":")).encode("ascii")
    B.fresh_bytes(destination, raw)
    print(json.dumps({"selection": str(destination), "sha256": hashlib.sha256(raw).hexdigest(),
                      "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()
