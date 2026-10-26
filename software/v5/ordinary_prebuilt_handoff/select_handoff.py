"""Prepare one finite prebuilt relocation/query selection; never launch it."""
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
PREFIX = "software/v5/ordinary_prebuilt_handoff/"
PACKAGE = LOCAL / "multi-source-package01/suite/assembled/package"
ASSEMBLY = PACKAGE.parent / "ASSEMBLY.json"
PROFILE_SHA = "ca257419f464c2e9d968011983673160377f743ebbe2a27e2399b510dce1ce67"
INSTALL_SHA = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
ASSEMBLY_SHA = "ec5ab7709aba2c4a896fa1898e925effb8f7a95f17bdb300c55307fcc5c10d6c"
SOURCE = LOCAL / "commons-source-controls01/suite/relocated"
SOURCE_SHA = "f5134135204f980b90df449a3a9a07bfed61fd9ff6b9fd5b5dde305b00cd2861"
QUERY = LOCAL / "ordinary-query-public-01/public/query-local/native-type.json"
BINDINGS = LOCAL / "ordinary-query-public-01/public/fixtures/known-bindings.json"
QUERY_SHA = "226bb411b2a7255eabc522f482afd2c199877ad624737fddf7b27ec0f8658480"
BINDINGS_SHA = "0ebd5b6de9942a1f9359e23c4d7a36219d30bd71af69c73813de8cfd03d95f2f"
HELPER = "software/v5/ordinary_fair_search/assemble.py"
HELPER_SHA = "9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT / "software/runtime/lean-4.34.0-windows"
MIB = 1024**2


def need(condition, message):
    if not condition:
        raise ValueError("PREBUILT_SELECTION_" + message)


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("name", "packer-sha256", "test-sha256"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize, "PROCESS")
    need(re.fullmatch(r"prebuilt-handoff[0-9]{2}", args.name), "NAME")
    need(all(re.fullmatch(r"[0-9a-f]{64}", value) for value in
             (args.packer_sha256, args.test_sha256)), "PINS")
    helper_path = ROOT / HELPER
    with helper_path.open("rb") as stream:
        raw = stream.read(2*MIB + 1)
    need(hashlib.sha256(raw).hexdigest() == HELPER_SHA, "HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_prebuilt_selection_files", helper_path)
    H = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(helper_path), "exec"), H.__dict__)
    started, cpu, runtime = time.monotonic(), time.process_time(), {}

    def check():
        need(time.monotonic()-started < 60 and time.process_time()-cpu < 30, "ALLOWANCE")

    def pin(path, expected=None):
        value = H.pin(path, check)
        need(expected is None or value == expected, "PIN:" + str(path))
        runtime[str(path)] = value["sha256"]
        return value

    def document(path, expected):
        doc, value = H.read_json(path, expected, check)
        runtime[str(path)] = value["sha256"]
        return doc, value

    profile, profile_pin = document(PACKAGE / "PROFILE.json", PROFILE_SHA)
    installation, install_pin = document(PACKAGE / "installation/INSTALLATION.json", INSTALL_SHA)
    assembly, _ = document(ASSEMBLY, ASSEMBLY_SHA)
    need(profile["installation_manifest_sha256"] == INSTALL_SHA and
         assembly["profile_sha256"] == PROFILE_SHA and
         assembly["installation_manifest_sha256"] == INSTALL_SHA, "ASSOCIATION")
    need(len(profile["files"]) == 117 and len(assembly["documentation_files"]) == 8 and
         set(installation["files"]) == H.INST_FILES | H.RUNTIME_FILES, "ROLES")
    files = dict(profile["files"])
    for name, value in installation["files"].items():
        if name in H.INST_FILES:
            files["installation/" + name] = value
        else:
            category, relative = name.split("/", 1)
            pin({"python_runtime": PYTHON, "lean_runtime": LEAN}[category] / H.relative(relative), value)
    files.update(assembly["documentation_files"])
    files.update({"PROFILE.json": profile_pin, "installation/INSTALLATION.json": install_pin})
    need(len(files) == 154 and sum(value["bytes"] for value in files.values()) == 39148493,
         "EXACT_PAYLOAD")
    H.census(PACKAGE, files, check)
    for name, value in files.items():
        pin(PACKAGE / H.relative(name), H.pin_shape(value))
    source_manifest, _ = document(SOURCE / "COMMONS-SOURCE-MANIFEST.json", SOURCE_SHA)
    # Source companions are associated, not reverified, repacked or executed.
    need(type(source_manifest) is dict and type(source_manifest.get("files")) is dict,
         "SOURCE_ASSOCIATION")
    pin(SOURCE / "README.md", source_manifest["files"]["README.md"])
    need(pin(QUERY)["sha256"] == QUERY_SHA and pin(BINDINGS)["sha256"] == BINDINGS_SHA,
         "QUERY_INPUTS")
    source_names = ["tools/Run-V5-Check.py", HELPER] + [PREFIX + name for name in
        ("CONTRACT.md", "README.md", "pack_handoff.py", "test_handoff.py",
         "TEST-PLAN.md", "select_handoff.py")]
    sources = {name: pin(ROOT / name)["sha256"] for name in source_names}
    need(sources[HELPER] == HELPER_SHA and
         sources[PREFIX + "pack_handoff.py"] == args.packer_sha256 and
         sources[PREFIX + "test_handoff.py"] == args.test_sha256, "APPROVED_SOURCE_PINS")
    need(len(runtime) <= 256, "RUNTIME_PIN_COUNT")
    destination = LOCAL / (args.name + ".selection.json")
    H.ordinary(destination, fresh=True)
    H.ordinary(LOCAL / args.name, directory=True, fresh=True)
    selection = dict(schema="DMKN_V5_LOCAL_CHECK_V1", name=args.name, sources=sources,
        runtime_pins=runtime, argv=[str(PYTHON / "python.exe"), "-I", "-S", "-B",
            "{snapshot}/" + PREFIX + "test_handoff.py", "--package", str(PACKAGE),
            "--assembly-receipt", str(ASSEMBLY), "--packer-sha256", args.packer_sha256,
            "--source-handoff", str(SOURCE), "--output", "{output}/suite"],
        limits=dict(wall_seconds=180, cpu_seconds=90, memory_mib=768,
                    active_processes=3, stdout_bytes=2*MIB, stderr_bytes=MIB))
    raw = H.canonical(selection)
    check()
    H.fresh_bytes(destination, raw)
    print(json.dumps({"selection": str(destination), "sha256": H.digest(raw),
                      "runtime_pins": len(runtime), "status": "PREPARED_NOT_EXECUTED"}), flush=True)


if __name__ == "__main__":
    main()
