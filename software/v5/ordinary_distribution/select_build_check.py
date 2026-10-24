"""Select one clean-input current build, without launching a compiler or owner.

Validation-only: immutable local source staging and a finite outer selection.
The staged source tree has no experiments, installed payloads or old generated
objects. This is an exact-input build boundary, not an OS filesystem sandbox.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
PREFIX = "software/v5/ordinary_distribution/"
BASE = "software/v5/ordinary_package/build.py"
BASE_SHA = "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT / "software/runtime/lean-4.34.0-windows"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "SELECTION_DUPLICATE_KEY")
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--name", required=True)
    parser.add_argument("--builder-sha256", required=True)
    parser.add_argument("--map-sha256", required=True)
    args = parser.parse_args()
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "CANONICAL_ISOLATED_SELECTION")
    need(re.fullmatch(r"[a-z0-9][a-z0-9-]{0,49}", args.name) is not None and
         all(re.fullmatch(r"[0-9a-f]{64}", pin) is not None
             for pin in (args.builder_sha256, args.map_sha256)), "SELECTION_ARGUMENTS")
    deadline = time.monotonic() + 90

    def check():
        need(time.monotonic() < deadline, "SELECTION_DEADLINE")

    # Reuse only the unchanged, previously reviewed path/pin helpers. Its main
    # guard is not entered; the current builder is never imported by this selector.
    base_raw = (ROOT / BASE).read_bytes()
    need(hashlib.sha256(base_raw).hexdigest() == BASE_SHA, "BASE_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_distribution_selection_base", ROOT / BASE)
    B = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = B
    exec(compile(base_raw, str(ROOT / BASE), "exec"), B.__dict__)
    selection = B.ordinary(LOCAL / (args.name + ".selection.json"), fresh=True)
    receipt = B.ordinary(LOCAL / (args.name + ".inputs.json"), fresh=True)
    clean = B.ordinary(LOCAL / (args.name + "-source"), directory=True, fresh=True)
    B.ordinary(LOCAL / args.name, directory=True, fresh=True)
    map_path, builder_path = ROOT / PREFIX / "source-map.json", ROOT / PREFIX / "build.py"
    map_pin, builder_pin = B.pin(map_path, check, 2*MIB), B.pin(builder_path, check, 2*MIB)
    need(map_pin["sha256"] == args.map_sha256 and builder_pin["sha256"] == args.builder_sha256,
         "REVIEWED_CURRENT_SOURCE_PINS")
    raw = map_path.read_bytes()
    need(len(raw) == map_pin["bytes"] and hashlib.sha256(raw).hexdigest() == args.map_sha256,
         "MAP_READ_CHANGED")
    mapping = json.loads(raw, object_pairs_hook=unique)
    need(mapping["schema"] == "DMKN_ORDINARY_DISTRIBUTION_SOURCE_MAP_V1" and
         len(mapping["sources"]) == 67 and mapping["base_inputs"] == list(B.SOURCE_FILES),
         "EXACT_CURRENT_SOURCE_MAP")
    sources = dict(mapping["sources"])
    sources[PREFIX + "build.py"] = builder_pin
    sources[PREFIX + "source-map.json"] = map_pin
    need(len(sources) == 69 and len({p.casefold() for p in sources}) == 69 and
         sum(pin["bytes"] for pin in sources.values()) <= 16*MIB, "CLEAN_SOURCE_CENSUS")
    original_pins = {}
    for relative, pin in sources.items():
        path = ROOT / relative
        need(path.is_relative_to(ROOT / "software/v5") or
             path in (ROOT / "software/assets/foundation/seed-verified.json",
                      ROOT / "software/assets/foundation/seed-inventory-json.json"),
             "CLEAN_SOURCE_SCOPE")
        B.ordinary(path)
        need(B.pin(path, check, 2*MIB) == pin, "CLEAN_SOURCE_PIN:" + relative)
        original_pins[str(path)] = pin["sha256"]
    runtime = {}
    runtime_map = {key: {"bytes": size, "sha256": sha}
                   for key, (size, sha) in B.RUNTIME_PINS.items()}
    need(not set(runtime_map) & set(mapping["native_runtime_pins"]), "RUNTIME_DUPLICATES")
    runtime_map.update(mapping["native_runtime_pins"])
    for logical, pin in runtime_map.items():
        category, relative = logical.split("/", 1)
        path = {"python_runtime": PYTHON, "lean_runtime": LEAN}[category] / relative
        need(B.pin(path, check) == pin, "CLEAN_BUILD_RUNTIME_PIN")
        runtime[str(path)] = pin["sha256"]
    clean.mkdir()
    for relative, pin in sorted(sources.items()):
        check()
        source, target = ROOT / relative, clean / relative
        raw = source.read_bytes()
        need({"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()} == pin,
             "CLEAN_SOURCE_READ_CHANGED")
        target.parent.mkdir(parents=True, exist_ok=True)
        B.ordinary(target.parent, directory=True)
        B.fresh_bytes(target, raw)
        need(B.pin(target, check, 2*MIB) == pin, "CLEAN_SOURCE_COPY_PIN")
        runtime[str(target)] = pin["sha256"]
    need({p.relative_to(clean).as_posix() for p in clean.rglob("*") if p.is_file()} == set(sources),
         "CLEAN_SOURCE_EXACT_TREE")
    runtime.update(original_pins)
    B.save_json(receipt, {"schema": "DMKN_ORDINARY_CLEAN_BUILD_INPUTS_V1",
        "source_root": str(clean), "files": sources, "runtimes": runtime_map,
        "claim": "EXACT_STAGED_SOURCE_INPUTS_NO_OLD_GENERATED_ARTIFACTS_NOT_OS_SANDBOX"})
    runtime[str(receipt)] = B.pin(receipt, check, 2*MIB)["sha256"]
    selected = ("tools/Run-V5-Check.py", PREFIX + "select_build_check.py",
                PREFIX + "build.py", PREFIX + "source-map.json")
    plan = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": args.name,
        "sources": {name: B.pin(ROOT / name, check, 2*MIB)["sha256"] for name in selected},
        "runtime_pins": runtime,
        "argv": [str(PYTHON / "python.exe"), "-I", "-S", "-B",
            r"{snapshot}\software\v5\ordinary_distribution\build.py",
            "--source-root", str(clean), "--python-runtime", str(PYTHON),
            "--lean-runtime", str(LEAN), "--output", r"{output}\distribution",
            "--wall-seconds", "480", "--cpu-seconds", "360", "--memory-mib", "2048"],
        "limits": {"wall_seconds": 540, "cpu_seconds": 440, "memory_mib": 2304,
                   "active_processes": 8, "stdout_bytes": MIB, "stderr_bytes": MIB}}
    need(len(runtime) <= 256 and plan["sources"][PREFIX + "build.py"] == args.builder_sha256 and
         plan["sources"][PREFIX + "source-map.json"] == args.map_sha256, "SELECTION_FINAL_BINDING")
    check()
    B.save_json(selection, plan)
    print(json.dumps({"selection": str(selection), "sha256": B.pin(selection, check, MIB)["sha256"],
        "source_root": str(clean), "source_files": len(sources), "runtime_pins": len(runtime),
        "runtime": "NOT_STARTED"}), flush=True)


if __name__ == "__main__":
    main()
