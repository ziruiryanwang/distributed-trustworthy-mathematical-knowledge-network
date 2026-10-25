"""File-only state-free concept inspection successor of native-src01.

Replace exactly peer.py and peer_api.py, selected by caller-provided reviewed
hashes. All 139 other payloads, native artifacts and owner semantics
stay unchanged. No build, owner operation or network call runs. Commit the new
profile last. Assembly alone is not qualification or mathematical acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time

MIB = 1024**2
BUILDER = "software/v5/ordinary_package/build.py"
BUILDER_SHA = "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5"
BASE_OWNER_SHA = "56ef042f652fcb88cae7d16ab74883016a469e2e82777c1a173f842f5ef8245a"
BASE_LOADER_SHA = "d63ea79f527e5519c19afcf1b98ae262b6eabb662fe454d30b1a4a75722ed8a6"
BASE_PROFILE_SHA = "fc45893cef624978f0ab5212d0e1e172ff7c71f821124daa8751727bf7123ef6"
BASE_DOCS = {
    "README.md": {"bytes": 8523, "sha256": "f425e20490191f3609b72e87ed877e791277568c9a6e094b13feca548d457a86"},
    "PRODUCER.md": {"bytes": 5051, "sha256": "8904e3e83c0d93880f488c4df0a003b0e499389cdf4bc4915d10b466ca8d4b45"},
}
PREFIX = "software/v5/ordinary_symbol_inspection/"
SOURCES = {"peer.py": PREFIX+"peer.py", "peer_api.py": PREFIX+"peer_api.py"}


def need(condition, code):
    if not condition:
        raise ValueError(code)


def hexid(value):
    need(type(value) is str and len(value) == 64 and
         all(c in "0123456789abcdef" for c in value), "PREVIEW_ASSEMBLY_HASH")
    return value


def bootstrap(path, name, expected):
    # Entrypoint/source bytes and the local OS are owner-selected premises.
    # Remaining path checks reuse the exact preserved builder and loader.
    need(name not in sys.modules, "PREVIEW_ASSEMBLY_PRELOADED")
    need(path.is_absolute() and path.is_file() and path.stat().st_size <= 2*MIB,
         "PREVIEW_ASSEMBLY_BOOTSTRAP_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() == expected, "PREVIEW_ASSEMBLY_BOOTSTRAP_PIN")
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
         sys.dont_write_bytecode and not sys.flags.optimize, "PREVIEW_ASSEMBLY_PYTHON")
    need(type(args.wall_seconds) is int and 10 <= args.wall_seconds <= 600 and
         type(args.cpu_seconds) is int and 5 <= args.cpu_seconds <= 600,
         "PREVIEW_ASSEMBLY_FINITE_ALLOWANCE")
    need(args.base_profile_sha256 == BASE_PROFILE_SHA, "PREVIEW_ASSEMBLY_SELECTED_BASE")
    reviewed = {"peer.py": hexid(args.peer_sha256),
                "peer_api.py": hexid(args.peer_api_sha256)}
    deadline = started+args.wall_seconds

    def check():
        need(time.monotonic() < deadline and
             time.process_time()-cpu_started < args.cpu_seconds, "PREVIEW_ASSEMBLY_ALLOWANCE")

    root, base = Path(args.source_root), Path(args.base_package)
    B = bootstrap(root/BUILDER, "_dmkn_preview_preserved_builder", BUILDER_SHA)
    root, base = B.ordinary(root, directory=True), B.ordinary(base, directory=True)
    output = B.ordinary(args.output, directory=True, fresh=True)
    runtimes = {"python_runtime": B.ordinary(args.python_runtime, directory=True),
                "lean_runtime": B.ordinary(args.lean_runtime, directory=True)}
    need(Path(sys.executable).resolve() == runtimes["python_runtime"]/"python.exe",
         "PREVIEW_ASSEMBLY_RUNNING_PYTHON")
    for path in (base, *runtimes.values()):
        need(not output.is_relative_to(path) and not path.is_relative_to(output),
             "PREVIEW_ASSEMBLY_OUTPUT_OVERLAP")
    need(not root.is_relative_to(output), "PREVIEW_ASSEMBLY_SOURCE_OVERLAP")
    check()
    need(B.pin(base/"owner.py", check, 2*MIB)["sha256"] == BASE_OWNER_SHA and
         B.pin(base/"profile.py", check, 2*MIB)["sha256"] == BASE_LOADER_SHA,
         "PREVIEW_ASSEMBLY_BASE_IDENTITY")
    owner = bootstrap(base/"owner.py", "_dmkn_preview_base_owner", BASE_OWNER_SHA)
    loader = owner.bootstrap(base, args.base_profile_sha256, check)
    loaded = loader.load(base, args.base_profile_sha256, runtimes, deadline, check_parent=check)
    old = loaded.descriptor
    source_pins = {logical: B.pin(root/relative, check, 2*MIB)
                   for logical, relative in SOURCES.items()}
    need(all(source_pins[name]["sha256"] == reviewed[name] for name in SOURCES),
         "PREVIEW_ASSEMBLY_REVIEWED_SOURCE")
    own_pin = B.pin(root/PREFIX/"assemble.py", check, 2*MIB)
    need(B.pin(Path(__file__).absolute(), check, 2*MIB) == own_pin,
         "PREVIEW_ASSEMBLY_RUNNING_SOURCE")
    installed_raw = loader.bounded(base/"installation/INSTALLATION.json", 2*MIB)
    installed = loader.owner_json(installed_raw)
    selected = {name: (base/name, pin) for name, pin in old["files"].items()}
    for name, pin in installed["files"].items():
        loader.relative(name)
        if name.split("/", 1)[0] in runtimes:
            continue
        selected["installation/"+name] = (base/"installation"/name, pin)
    selected["installation/INSTALLATION.json"] = (base/"installation/INSTALLATION.json",
        {"bytes": len(installed_raw), "sha256": old["installation_manifest_sha256"]})
    # Native-src01 has no ASSEMBLY receipt. Its profile+installation select the
    # executable payloads; these independent fixed pins select its two documents.
    for name, pin in BASE_DOCS.items():
        need(name not in selected, "INSPECTION_ASSEMBLY_DOCUMENT_COLLISION")
        selected[name] = (base/name, pin)
    predecessor = dict(selected)
    loader.census(base, set(predecessor) | {"PROFILE.json"}, check)
    for logical, relative in SOURCES.items():
        selected[logical] = (root/relative, source_pins[logical])
    added = sorted(set(selected)-set(predecessor))
    changed = sorted(name for name in set(selected) & set(predecessor)
                     if selected[name][1] != predecessor[name][1])
    unchanged = sorted(name for name in set(selected) & set(predecessor)
                       if selected[name][1] == predecessor[name][1])
    need(len(old["files"]) == 111 and len(predecessor) == len(selected) == 141 and not added and
         changed == sorted(SOURCES) and len(unchanged) == 139,
         "PREVIEW_ASSEMBLY_EXACT_DELTA")
    need(len({name.casefold() for name in selected}) == len(selected),
         "PREVIEW_ASSEMBLY_CENSUS")
    need(sum(pin["bytes"] for _, pin in selected.values()) <= 768*MIB,
         "PREVIEW_ASSEMBLY_TOTAL_BOUND")
    for name, (source, expected) in selected.items():
        loader.relative(name)
        need(not source.is_relative_to(output), "PREVIEW_ASSEMBLY_SELECTED_OVERLAP")
        need(B.pin(source, check, 128*MIB) == expected, "PREVIEW_ASSEMBLY_INPUT_PIN")
    output.mkdir()
    phase = "COPYING"
    try:
        for name, (source, expected) in sorted(selected.items()):
            check()
            target = output/name
            missing, parent = [], target.parent
            while not parent.exists():
                need(parent.is_relative_to(output), "PREVIEW_ASSEMBLY_DIRECTORY")
                missing.append(parent); parent = parent.parent
            B.ordinary(parent, directory=True)
            for directory in reversed(missing):
                B.ordinary(directory, directory=True, fresh=True).mkdir()
            B.ordinary(source); B.ordinary(target, fresh=True)
            digest, count = hashlib.sha256(), 0
            with source.open("rb") as inp, target.open("xb") as out:
                while block := inp.read(MIB):
                    check(); count += len(block)
                    need(count <= expected["bytes"], "PREVIEW_ASSEMBLY_SOURCE_GREW")
                    digest.update(block); out.write(block)
                out.flush(); os.fsync(out.fileno())
            need(count == expected["bytes"] and digest.hexdigest() == expected["sha256"],
                 "PREVIEW_ASSEMBLY_SOURCE_CHANGED")
            need(B.pin(target, check, 128*MIB) == expected, "PREVIEW_ASSEMBLY_COPY_CHANGED")
        phase = "FINAL_VERIFY"
        for source, expected in predecessor.values():
            need(B.pin(source, check, 128*MIB) == expected, "PREVIEW_ASSEMBLY_BASE_CHANGED")
        need(B.pin(base/"PROFILE.json", check, 2*MIB)["sha256"] == BASE_PROFILE_SHA,
             "PREVIEW_ASSEMBLY_BASE_DESCRIPTOR_CHANGED")
        loader.census(base, set(predecessor) | {"PROFILE.json"}, check)
        for name, (source, expected) in selected.items():
            need(B.pin(source, check, 128*MIB) == expected and
                 B.pin(output/name, check, 128*MIB) == expected, "PREVIEW_ASSEMBLY_FINAL_PIN")
        auxiliary = dict(old["files"])
        auxiliary.update(source_pins)
        descriptor = dict(old, files=auxiliary)
        raw = loaded.A.E.canonical_json(descriptor)
        need(len(raw) <= 2*MIB, "PREVIEW_ASSEMBLY_PROFILE_BOUND")
        result = {"status": "ASSEMBLED_NOT_ADOPTED", "base_profile_sha256": BASE_PROFILE_SHA,
            "base_document_pins": BASE_DOCS,
            "profile_sha256": hashlib.sha256(raw).hexdigest(),
            "installation_manifest_sha256": old["installation_manifest_sha256"],
            "implementation_id": loaded.installation.implementation_id,
            "files_excluding_profile": len(selected),
            "copied_bytes": sum(pin["bytes"] for _, pin in selected.values()),
            "changed_or_added": source_pins, "reviewed_sources": reviewed, "assembler": own_pin,
            "payloads": {name: pin for name, (_, pin) in sorted(selected.items())},
            "added": added, "changed": changed, "unchanged": unchanged,
            "wall_seconds_before_commit": time.monotonic()-started,
            "cpu_seconds_before_commit": time.process_time()-cpu_started,
            "claim": "FILE_ONLY_SUCCESSOR_NO_NATIVE_BUILD_STATE_OR_MATHEMATICAL_ACCEPTANCE"}
        B.save_json(output/"ASSEMBLY.json", result)
        B.fresh_bytes(output/".PROFILE.pending", raw)
        loader.census(output, set(selected) | {"ASSEMBLY.json", ".PROFILE.pending"}, check)
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
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("source-root", "base-package", "base-profile-sha256", "peer-sha256",
                 "peer-api-sha256", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+name, required=True)
    for name in ("wall-seconds", "cpu-seconds"):
        parser.add_argument("--"+name, required=True, type=int)
    print(json.dumps(assemble(parser.parse_args()), sort_keys=True, allow_nan=False))
