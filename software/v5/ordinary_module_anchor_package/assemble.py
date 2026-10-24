"""File-only local module-anchor successor of the audited ordinary query package.

Six auxiliary payloads change and one registry helper is added. Existing native
admission installation, compiled helpers and other payloads remain unchanged; no state,
module construction, network or native executable build runs during assembly.
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
BASE_LOADER_SHA = "ea809c3607b8fae7dc97cb0774cf58db33703795ba0af7bca385c543cf17df98"
BASE_PROFILE_SHA = "2b8ac8cad152dde90a1b51d19dd1a821305bd7242b601c10eaa7a39f0db572f5"
PREFIX = "software/v5/ordinary_module_anchor_package/"
BRIDGE = "software/v5/ordinary_module_anchor/"
SOURCES = {"owner.py": PREFIX+"owner.py", "profile.py": PREFIX+"profile.py",
           "authoring/py/anchor_store.py": BRIDGE+"anchor_store.py",
           "authoring/py/module_closure.py": BRIDGE+"module_closure.py",
           "authoring/py/module_export.py": BRIDGE+"module_export.py",
           "module_worker.py": BRIDGE+"module_worker.py",
           "module/OrdinaryModule.lean": BRIDGE+"OrdinaryModule.lean"}


def need(condition, code):
    if not condition:
        raise ValueError(code)


def bootstrap(path, name, expected):
    # Source path and selected entrypoint bytes are owner-approved. Remaining
    # path/census checks use the preserved builder and profile helpers below.
    need(name not in sys.modules, "LIBRARY_ASSEMBLY_PRELOADED")
    need(path.is_absolute() and path.is_file() and path.stat().st_size <= 2*MIB,
         "LIBRARY_ASSEMBLY_BOOTSTRAP_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() == expected, "LIBRARY_ASSEMBLY_BOOTSTRAP_PIN")
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
         sys.dont_write_bytecode and not sys.flags.optimize, "LIBRARY_ASSEMBLY_PYTHON")
    need(type(args.wall_seconds) is int and 10 <= args.wall_seconds <= 600 and
         type(args.cpu_seconds) is int and 5 <= args.cpu_seconds <= 600,
         "LIBRARY_ASSEMBLY_FINITE_ALLOWANCE")
    deadline = started+args.wall_seconds

    def check():
        need(time.monotonic() < deadline and
             time.process_time()-cpu_started < args.cpu_seconds, "LIBRARY_ASSEMBLY_ALLOWANCE")

    root, base = Path(args.source_root), Path(args.base_package)
    need(args.base_profile_sha256 == BASE_PROFILE_SHA, "ANCHOR_ASSEMBLY_SELECTED_BASE")
    B = bootstrap(root/BUILDER, "_dmkn_library_preserved_builder", BUILDER_SHA)
    root, base = B.ordinary(root, directory=True), B.ordinary(base, directory=True)
    output = B.ordinary(args.output, directory=True, fresh=True)
    runtimes = {"python_runtime": B.ordinary(args.python_runtime, directory=True),
                "lean_runtime": B.ordinary(args.lean_runtime, directory=True)}
    need(Path(sys.executable).resolve() == runtimes["python_runtime"]/"python.exe",
         "LIBRARY_ASSEMBLY_RUNNING_PYTHON")
    for path in (base, *runtimes.values()):
        need(not output.is_relative_to(path) and not path.is_relative_to(output),
             "LIBRARY_ASSEMBLY_OUTPUT_OVERLAP")
    need(not root.is_relative_to(output), "LIBRARY_ASSEMBLY_SOURCE_OVERLAP")
    check()
    need(B.pin(base/"owner.py", check, 2*MIB)["sha256"] == BASE_OWNER_SHA and
         B.pin(base/"profile.py", check, 2*MIB)["sha256"] == BASE_LOADER_SHA,
         "LIBRARY_ASSEMBLY_BASE_LOADER_VERSION")
    owner = bootstrap(base/"owner.py", "_dmkn_library_base_owner", BASE_OWNER_SHA)
    loader = owner.bootstrap(base, args.base_profile_sha256, check)
    loaded = loader.load(base, args.base_profile_sha256, runtimes, deadline, check_parent=check)
    old = loaded.descriptor
    source_pins = {logical: B.pin(root/relative, check, 2*MIB)
                   for logical, relative in SOURCES.items()}
    own_pin = B.pin(root/PREFIX/"assemble.py", check, 2*MIB)
    need(B.pin(Path(__file__).absolute(), check, 2*MIB) == own_pin,
         "LIBRARY_ASSEMBLY_RUNNING_SOURCE")
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
    predecessor = dict(selected)
    for logical, relative in SOURCES.items():
        selected[logical] = (root/relative, source_pins[logical])
    added = sorted(set(selected)-set(predecessor))
    changed = sorted(name for name in set(selected) & set(predecessor)
                     if selected[name][1] != predecessor[name][1])
    unchanged = sorted(name for name in set(selected) & set(predecessor)
                       if selected[name][1] == predecessor[name][1])
    need(len(predecessor) == 133 and len(selected) == 134 and
         added == ["authoring/py/anchor_store.py"] and len(changed) == 6 and len(unchanged) == 127 and
         set(changed) == set(SOURCES)-set(added), "ANCHOR_ASSEMBLY_EXACT_DELTA")
    need(len(selected) <= 512 and len({name.casefold() for name in selected}) == len(selected),
         "LIBRARY_ASSEMBLY_CENSUS")
    need(sum(pin["bytes"] for _, pin in selected.values()) <= 768*MIB,
         "LIBRARY_ASSEMBLY_TOTAL_BOUND")
    for name, (source, expected) in selected.items():
        loader.relative(name)
        need(not source.is_relative_to(output), "LIBRARY_ASSEMBLY_SELECTED_OVERLAP")
        need(B.pin(source, check, 128*MIB) == expected, "LIBRARY_ASSEMBLY_INPUT_PIN")
    output.mkdir()
    phase = "COPYING"
    try:
        for name, (source, expected) in sorted(selected.items()):
            check()
            target = output/name
            missing, parent = [], target.parent
            while not parent.exists():
                need(parent.is_relative_to(output), "LIBRARY_ASSEMBLY_DIRECTORY")
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
                    need(count <= expected["bytes"], "LIBRARY_ASSEMBLY_SOURCE_GREW")
                    digest.update(block); out.write(block)
                out.flush(); os.fsync(out.fileno())
            need(count == expected["bytes"] and digest.hexdigest() == expected["sha256"],
                 "LIBRARY_ASSEMBLY_SOURCE_CHANGED")
            need(B.pin(target, check, 128*MIB) == expected, "LIBRARY_ASSEMBLY_COPY_CHANGED")
        phase = "FINAL_VERIFY"
        for name, (source, expected) in selected.items():
            need(B.pin(source, check, 128*MIB) == expected and
                 B.pin(output/name, check, 128*MIB) == expected, "LIBRARY_ASSEMBLY_FINAL_PIN")
        auxiliary = dict(old["files"])
        auxiliary.update(source_pins)
        descriptor = dict(old, files=auxiliary)
        raw = loaded.A.E.canonical_json(descriptor)
        need(len(raw) <= 2*MIB, "LIBRARY_ASSEMBLY_PROFILE_BOUND")
        result = {"status": "ASSEMBLED_NOT_ADOPTED", "base_profile_sha256": args.base_profile_sha256,
            "profile_sha256": hashlib.sha256(raw).hexdigest(),
            "installation_manifest_sha256": old["installation_manifest_sha256"],
            "implementation_id": loaded.installation.implementation_id,
            "files_excluding_profile": len(selected),
            "copied_bytes": sum(pin["bytes"] for _, pin in selected.values()),
            "changed_or_added": source_pins, "assembler": own_pin,
            "added": added, "changed": changed, "unchanged": unchanged,
            "wall_seconds_before_commit": time.monotonic()-started,
            "cpu_seconds_before_commit": time.process_time()-cpu_started,
            "claim": "FILE_ONLY_SUCCESSOR_NO_NATIVE_BUILD_STATE_OR_MATHEMATICAL_ACCEPTANCE"}
        # A separate assembly receipt is not on any package import path.
        B.save_json(output/"ASSEMBLY.json", result)
        B.fresh_bytes(output/".PROFILE.pending", raw)
        check(); B.ordinary(output/"PROFILE.json", fresh=True)
        (output/".PROFILE.pending").rename(output/"PROFILE.json")
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
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("source-root", "base-package", "base-profile-sha256", "python-runtime",
                 "lean-runtime", "output"):
        parser.add_argument("--"+name, required=True)
    for name in ("wall-seconds", "cpu-seconds"):
        parser.add_argument("--"+name, required=True, type=int)
    print(json.dumps(assemble(parser.parse_args()), sort_keys=True, allow_nan=False))

