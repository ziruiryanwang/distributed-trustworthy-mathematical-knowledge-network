"""Prepare one fresh pure/inert project-extraction control; no test launch."""
from pathlib import Path
import ast
import hashlib
import importlib.util
import json
import os
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
PREFIX = "software/v5/ordinary_project_extraction_package/"
NAME = "ordinary-project-extraction-controls-01"
PYTHON = Path(r"D:\Python314")
CONTROLS_SHA = "8c28917cebd047173dc1c70c7103e6c8922dfb4c8857ed36d3765c26beb31e5d"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def main():
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and len(sys.argv) == 1,
         "PROJECT_SELECTION_PROCESS")
    builder = ROOT/"software/v5/ordinary_package/build.py"
    with builder.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() ==
         "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5", "PROJECT_SELECTION_BUILDER")
    spec = importlib.util.spec_from_file_location("_project_control_selection_builder", builder)
    B = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(builder), "exec"), B.__dict__)
    deadline, runtime = time.monotonic()+60, {}
    def check():
        need(time.monotonic() < deadline, "PROJECT_SELECTION_DEADLINE")
    def pin(path, expected=None):
        digest = B.pin(path, check, 128*MIB)["sha256"]
        need(expected is None or digest == expected, "PROJECT_SELECTION_PIN:"+str(path))
        runtime[str(path)] = digest
        return digest
    template = LOCAL/"ordinary-module-anchor-native-02.selection.json"
    expected = "bf253a11b52a5f84c157a1165f69d869636a5aa960217db2c8e99faa69b2f752"
    pin(template, expected)
    with template.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() == expected, "PROJECT_SELECTION_TEMPLATE_CHANGED")
    # Only the same three explicitly selected Python runtime files; no Lean,
    # package, owner-state or project-artifact dependency is selected here.
    python_pins = {name: digest for name, digest in json.loads(raw)["runtime_pins"].items()
                   if Path(name).is_relative_to(PYTHON)}
    need(set(python_pins) == {str(PYTHON/name) for name in
        ("python.exe", "python3.dll", "python314.dll")}, "PROJECT_SELECTION_PYTHON_CENSUS")
    for name, digest in python_pins.items():
        pin(Path(name), digest)
    controls = ROOT/PREFIX/"controls.py"
    pin(controls, CONTROLS_SHA)
    with controls.open("rb") as stream:
        raw = stream.read(MIB+1)
    need(hashlib.sha256(raw).hexdigest() == CONTROLS_SHA, "PROJECT_SELECTION_CONTROLS_CHANGED")
    tree = ast.parse(raw, filename=str(controls))
    tables = [node.value for node in tree.body if isinstance(node, ast.Assign) and
              any(isinstance(target, ast.Name) and target.id == "PINS" for target in node.targets)]
    need(len(tables) == 1, "PROJECT_SELECTION_CONTROL_PINS")
    pins = ast.literal_eval(tables[0])
    need(set(pins) == {"evidence", "controller", "owner"}, "PROJECT_SELECTION_SOURCE_CENSUS")
    for relative, digest in pins.values():
        pin(ROOT/relative, digest)
    pin(builder)
    names = ["tools/Run-V5-Check.py", PREFIX+"select_controls.py", PREFIX+"controls.py",
             *(relative for relative, _ in pins.values())]
    sources = {name: pin(ROOT/name) for name in names}
    need(sources[PREFIX+"controls.py"] == CONTROLS_SHA and len(runtime) <= 256,
         "PROJECT_SELECTION_SOURCE_CHANGED")
    destination = LOCAL/(NAME+".selection.json")
    B.ordinary(destination, fresh=True)
    B.ordinary(LOCAL/NAME, directory=True, fresh=True)
    selection = dict(schema="DMKN_V5_LOCAL_CHECK_V1", name=NAME, sources=sources, runtime_pins=runtime,
        argv=[str(PYTHON/"python.exe"), "-I", "-S", "-B", "{snapshot}/"+PREFIX+"controls.py",
              "--output", "{output}/controls"],
        limits=dict(wall_seconds=60, cpu_seconds=35, memory_mib=512, active_processes=2,
                    stdout_bytes=MIB, stderr_bytes=MIB))
    raw = json.dumps(selection, sort_keys=True, separators=(",", ":")).encode("ascii")
    B.fresh_bytes(destination, raw)
    print(json.dumps({"selection": str(destination), "sha256": hashlib.sha256(raw).hexdigest(),
                      "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()
