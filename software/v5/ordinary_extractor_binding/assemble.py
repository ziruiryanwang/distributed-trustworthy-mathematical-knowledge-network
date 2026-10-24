"""File-only extractor-role binding successor of the audited current source build.

Exactly one authoring helper changes. All 125 other payloads and the installed
implementation remain byte-identical. No state, native build or extraction.
The receipt stays outside the exact runtime package; PROFILE is committed last.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
import time

MIB = 1024**2
BUILDER = "software/v5/ordinary_package/build.py"
BUILDER_SHA = "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5"
BASE_OWNER_SHA = "c28ba23d5fafc9dfefd39e1db1f96759dd584e9c8ca0dab010bceb9e56b316de"
BASE_LOADER_SHA = "da073981a01de3b464934a06bd7743b70bc7dd14d20ac9388b72294c04c99a54"
PREFIX = "software/v5/ordinary_extractor_binding/"
SOURCES = {"authoring/py/library_extraction.py": PREFIX+"library_extraction.py"}
BASE_PACKAGE = "experiments/v5-local-checks/ordinary-current-source-build-01/distribution/package"
BASE_PROFILE_SHA = "3f3c0de037fd03907d661e428b6cc3592848ec8b66cc0e6fdbf579b0fb603026"
SOURCE_MAP = "software/v5/ordinary_distribution/source-map02.json"
RECIPES = {
    SOURCE_MAP: "805785e79e9dd8d566709bb785b5f176adda96db2f08bed4f47f0eecd7e945e0",
    "software/v5/ordinary_distribution/build02.py":
        "0a419be2e295ea2a36284256236369e7ccf99e6f19f0aa741d021483454a18ee",
}


def need(condition, code):
    if not condition:
        raise ValueError(code)


def bootstrap(path, name, expected):
    # Source path and selected entrypoint bytes are owner-approved. Remaining
    # path/census checks use the preserved builder and profile helpers below.
    need(name not in sys.modules, "EXTRACTOR_ASSEMBLY_PRELOADED")
    need(path.is_absolute() and path.is_file() and path.stat().st_size <= 2*MIB,
         "EXTRACTOR_ASSEMBLY_BOOTSTRAP_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() == expected, "EXTRACTOR_ASSEMBLY_BOOTSTRAP_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        exec(compile(raw, str(path), "exec"), module.__dict__)
    except BaseException:
        del sys.modules[name]
        raise
    return module


def assemble(args):
    started, cpu_started = time.monotonic(), time.process_time()
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "EXTRACTOR_ASSEMBLY_PYTHON")
    need(type(args.wall_seconds) is int and 10 <= args.wall_seconds <= 600 and
         type(args.cpu_seconds) is int and 5 <= args.cpu_seconds <= 600,
         "EXTRACTOR_ASSEMBLY_FINITE_ALLOWANCE")
    deadline = started+args.wall_seconds

    def check():
        need(time.monotonic() < deadline and
             time.process_time()-cpu_started < args.cpu_seconds, "EXTRACTOR_ASSEMBLY_ALLOWANCE")

    root, base = Path(args.source_root), Path(args.base_package)
    B = bootstrap(root/BUILDER, "_dmkn_extractor_preserved_builder", BUILDER_SHA)
    root, base = B.ordinary(root, directory=True), B.ordinary(base, directory=True)
    output = B.ordinary(args.output, directory=True, fresh=True)
    runtimes = {"python_runtime": B.ordinary(args.python_runtime, directory=True),
                "lean_runtime": B.ordinary(args.lean_runtime, directory=True)}
    need(Path(sys.executable).resolve() == runtimes["python_runtime"]/"python.exe",
         "EXTRACTOR_ASSEMBLY_RUNNING_PYTHON")
    for path in (base, *runtimes.values()):
        need(not output.is_relative_to(path) and not path.is_relative_to(output),
             "EXTRACTOR_ASSEMBLY_OUTPUT_OVERLAP")
    need(not root.is_relative_to(output), "EXTRACTOR_ASSEMBLY_SOURCE_OVERLAP")
    need(base == root/BASE_PACKAGE and args.base_profile_sha256 == BASE_PROFILE_SHA,
         "EXTRACTOR_ASSEMBLY_AUDITED_BASE")
    recipe_pins = {name: B.pin(root/name, check, 2*MIB) for name in RECIPES}
    need(all(recipe_pins[name]["sha256"] == expected for name, expected in RECIPES.items()),
         "EXTRACTOR_ASSEMBLY_RECIPE_PIN")
    with (root/SOURCE_MAP).open("rb") as stream:
        map_raw = stream.read(2*MIB+1)
    need(hashlib.sha256(map_raw).hexdigest() == RECIPES[SOURCE_MAP],
         "EXTRACTOR_ASSEMBLY_MAP_CHANGED")
    mapping = json.loads(map_raw)
    check()
    need(B.pin(base/"owner.py", check, 2*MIB)["sha256"] == BASE_OWNER_SHA and
         B.pin(base/"profile.py", check, 2*MIB)["sha256"] == BASE_LOADER_SHA,
         "EXTRACTOR_ASSEMBLY_BASE_LOADER_VERSION")
    owner = bootstrap(base/"owner.py", "_dmkn_extractor_base_owner", BASE_OWNER_SHA)
    loader = owner.bootstrap(base, args.base_profile_sha256, check)
    loaded = loader.load(base, args.base_profile_sha256, runtimes, deadline, check_parent=check)
    old = loaded.descriptor
    source_pins = {logical: B.pin(root/relative, check, 2*MIB)
                   for logical, relative in SOURCES.items()}
    need(all(mapping["copies"].get(logical) == relative and
             source_pins[logical] == mapping["sources"][relative]
             for logical, relative in SOURCES.items()), "EXTRACTOR_ASSEMBLY_SELECTED_HELPER")
    own_pin = B.pin(root/PREFIX/"assemble.py", check, 2*MIB)
    need(B.pin(Path(__file__).absolute(), check, 2*MIB) == own_pin,
         "EXTRACTOR_ASSEMBLY_RUNNING_SOURCE")
    installed_raw = loader.bounded(base/"installation/INSTALLATION.json", 2*MIB)
    installed = loader.owner_json(installed_raw)
    selected = {name: (base/name, pin) for name, pin in old["files"].items()}
    # Logical installation runtime attachments are external, not package files.
    for name, pin in installed["files"].items():
        loader.relative(name)
        if name.split("/", 1)[0] in runtimes:
            continue
        selected["installation/"+name] = (base/"installation"/name, pin)
    selected["installation/INSTALLATION.json"] = (base/"installation/INSTALLATION.json",
        {"bytes": len(installed_raw), "sha256": old["installation_manifest_sha256"]})
    original = dict(selected)
    loader.census(base, (*original, "PROFILE.json"), check)
    for logical, relative in SOURCES.items():
        need(logical in selected and selected[logical][1] != source_pins[logical],
             "EXTRACTOR_ASSEMBLY_ONE_REAL_CHANGE")
        selected[logical] = (root/relative, source_pins[logical])
    expected_names = set(mapping["copies"]) | {
        "installation/INSTALLATION.json", mapping["extractor_output"]}
    expected_names.update("installation/lean-lib/"+row["module"]+".olean"
                          for row in mapping["lanes"]["receiver"])
    expected_names.update("authoring/helpers/"+row["module"]+suffix
        for row in mapping["lanes"]["authoring"] for suffix in mapping["authoring_suffixes"])
    need(set(selected) == expected_names and len(selected) == 126 and len(old["files"]) == 98 and
         sum(selected[name][1] != original[name][1] for name in selected) == 1 and
         all(selected[name][1] == mapping["sources"][source]
             for name, source in mapping["copies"].items()), "EXTRACTOR_ASSEMBLY_EXACT_DELTA")
    need(len(selected) <= 512 and len({name.casefold() for name in selected}) == len(selected),
         "EXTRACTOR_ASSEMBLY_CENSUS")
    need(sum(pin["bytes"] for _, pin in selected.values()) <= 768*MIB,
         "EXTRACTOR_ASSEMBLY_TOTAL_BOUND")
    for name, (source, expected) in selected.items():
        loader.relative(name)
        need(not source.is_relative_to(output), "EXTRACTOR_ASSEMBLY_SELECTED_OVERLAP")
        need(B.pin(source, check, 128*MIB) == expected, "EXTRACTOR_ASSEMBLY_INPUT_PIN")
    output.mkdir()
    package = output/"package"
    package.mkdir()
    phase = "COPYING"
    try:
        for name, (source, expected) in sorted(selected.items()):
            check()
            target = package/name
            missing, parent = [], target.parent
            while not parent.exists():
                need(parent.is_relative_to(output), "EXTRACTOR_ASSEMBLY_DIRECTORY")
                missing.append(parent); parent = parent.parent
            B.ordinary(parent, directory=True)
            for directory in reversed(missing):
                B.ordinary(directory, directory=True, fresh=True).mkdir()
            # Stream large compiled helpers; never hold the whole package in RAM.
            B.ordinary(source); B.ordinary(target, fresh=True)
            digest, count = hashlib.sha256(), 0
            with source.open("rb") as inp, target.open("xb") as out:
                while block := inp.read(MIB):
                    check(); count += len(block)
                    need(count <= expected["bytes"], "EXTRACTOR_ASSEMBLY_SOURCE_GREW")
                    digest.update(block); out.write(block)
                out.flush(); os.fsync(out.fileno())
            need(count == expected["bytes"] and digest.hexdigest() == expected["sha256"],
                 "EXTRACTOR_ASSEMBLY_SOURCE_CHANGED")
            need(B.pin(target, check, 128*MIB) == expected, "EXTRACTOR_ASSEMBLY_COPY_CHANGED")
        phase = "FINAL_VERIFY"
        for name, (source, expected) in selected.items():
            need(B.pin(source, check, 128*MIB) == expected and
                 B.pin(package/name, check, 128*MIB) == expected, "EXTRACTOR_ASSEMBLY_FINAL_PIN")
        for name, (source, expected) in original.items():
            need(B.pin(source, check, 128*MIB) == expected, "EXTRACTOR_ASSEMBLY_BASE_CHANGED")
        for name, expected in installed["files"].items():
            parts = loader.relative(name).parts
            if parts[0] in runtimes:
                need(B.pin(runtimes[parts[0]].joinpath(*parts[1:]), check, 128*MIB) == expected,
                     "EXTRACTOR_ASSEMBLY_RUNTIME_CHANGED")
        for name, expected in recipe_pins.items():
            need(B.pin(root/name, check, 2*MIB) == expected, "EXTRACTOR_ASSEMBLY_RECIPE_CHANGED")
        need(B.pin(root/PREFIX/"assemble.py", check, 2*MIB) == own_pin and
             B.pin(Path(__file__).absolute(), check, 2*MIB) == own_pin and
             B.pin(root/BUILDER, check, 2*MIB)["sha256"] == BUILDER_SHA and
             B.pin(base/"PROFILE.json", check, 2*MIB)["sha256"] == BASE_PROFILE_SHA,
             "EXTRACTOR_ASSEMBLY_ENTRYPOINT_OR_BASE_CHANGED")
        loader.census(base, (*original, "PROFILE.json"), check)
        loader.census(package, selected, check)
        auxiliary = dict(old["files"])
        auxiliary.update(source_pins)
        descriptor = dict(old, files=auxiliary)
        raw = loaded.A.E.canonical_json(descriptor)
        need(len(raw) <= 2*MIB, "EXTRACTOR_ASSEMBLY_PROFILE_BOUND")
        need(set(auxiliary) == set(old["files"]) and len(auxiliary) == 98,
             "EXTRACTOR_ASSEMBLY_AUXILIARY_DELTA")
        result = {"status": "ASSEMBLED_NOT_ADOPTED", "package": str(package), "base_profile_sha256": args.base_profile_sha256,
            "profile_sha256": hashlib.sha256(raw).hexdigest(),
            "installation_manifest_sha256": old["installation_manifest_sha256"],
            "implementation_id": loaded.installation.implementation_id,
            "files_excluding_profile": len(selected),
            "copied_bytes": sum(pin["bytes"] for _, pin in selected.values()),
            "changed_or_added": source_pins, "unchanged_payloads": 125, "assembler": own_pin,
            "source_recipes": recipe_pins, "payloads": {name: pin for name, (_, pin) in selected.items()},
            "wall_seconds_before_commit": time.monotonic()-started,
            "cpu_seconds_before_commit": time.process_time()-cpu_started,
            "claim": "FILE_ONLY_SUCCESSOR_NO_NATIVE_BUILD_STATE_OR_MATHEMATICAL_ACCEPTANCE"}
        # A separate assembly receipt is not on any package import path.
        B.save_json(output/"ASSEMBLY.json", result)
        B.fresh_bytes(package/".PROFILE.pending", raw)
        check(); B.ordinary(package/"PROFILE.json", fresh=True)
        (package/".PROFILE.pending").rename(package/"PROFILE.json")
        return result
    except BaseException as error:
        try:
            B.save_json(output/"ASSEMBLY-FAILURE.json", {"phase": phase,
                "error_type": type(error).__name__, "error": str(error)[:2000],
                "wall_seconds": time.monotonic()-started,
                "cpu_seconds": time.process_time()-cpu_started,
                "retention": "PARTIAL_FILES_PRESERVED_NO_RETRY"})
        except BaseException:
            pass
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("source-root", "base-package", "base-profile-sha256", "python-runtime",
                 "lean-runtime", "output"):
        parser.add_argument("--"+name, required=True)
    for name in ("wall-seconds", "cpu-seconds"):
        parser.add_argument("--"+name, required=True, type=int)
    print(json.dumps(assemble(parser.parse_args()), sort_keys=True, allow_nan=False))
