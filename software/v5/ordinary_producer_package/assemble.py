"""File-only consolidated producer successor from retained reference assembly03.

Two reviewed Python payloads change; three producer roles and a usage note are
added. Installation/native checker bytes stay exact; the added exporter is an
exact retained binary. No compiler, owner open, snapshot copy or acceptance occurs.
The enclosing selected Job contains this cooperative controller. Failure keeps
partial output, and PROFILE.json is published last.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import importlib.util
import json
import math
import os
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
PREFIX = "software/v5/ordinary_producer_package/"
NAME = "ordinary-producer-assembly-01"
BASE = LOCAL/"ordinary-reference-assembly-03/package"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
BUILDER = "software/v5/ordinary_package/build.py"
BUILDER_SHA = "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5"
BASE_PROFILE = "a10e1f3ae0e1ac04cfa01240c9c07c3ca2d3da91616a3ca34b1f28b88adadbbc"
BASE_RECEIPT = "75f7f7c048208b337082c9b0529b02ac4fb6547d143ca178eacb73ba971da202"
INSTALLATION = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
IMPLEMENTATION = "fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df"
SOURCES = {
    "owner.py": PREFIX+"owner.py",
    "profile.py": PREFIX+"profile.py",
    "authoring/py/baseline_production.py": PREFIX+"baseline_production.py",
    "authoring/py/baseline_worker.py": "software/v5/ordinary_baseline/baseline_worker.py",
    "PRODUCER.md": PREFIX+"README.md",
}
EXPORTER_SOURCE = "experiments/v5-local-checks/ordinary-baseline-native-build-04/build/objects/BaselineExporter.exe"
EXPORTER_ROLE = "authoring/bin/BaselineExporter.exe"
EXPORTER_PIN = {"bytes": 809472, "sha256": "2adcffad1ad4967f093e1acc6c31295c2519e7f9cbf35d04bee37d8580cc3c4f"}
OVERLAYS = {"owner.py", "profile.py"}
ADDITIONS = {"authoring/py/baseline_production.py", "authoring/py/baseline_worker.py",
             EXPORTER_ROLE, "PRODUCER.md"}
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def hexid(value):
    need(type(value) is str and len(value) == 64 and
         all(c in "0123456789abcdef" for c in value), "PRODUCER_ASSEMBLY_HEX")
    return value


def encoded(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True,
                      allow_nan=False, separators=(",", ":")).encode("ascii")


def helper():
    path = ROOT/BUILDER
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(0 < len(raw) <= 2*MIB and hashlib.sha256(raw).hexdigest() == BUILDER_SHA,
         "PRODUCER_ASSEMBLY_HELPER_PIN")
    name = "_producer_preserved_builder"
    need(name not in sys.modules, "PRODUCER_ASSEMBLY_PRELOADED_HELPER")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    module.ordinary(path)
    return module


def relative(value):
    need(type(value) is str and 0 < len(value) <= 1024 and "\\" not in value,
         "PRODUCER_ASSEMBLY_RELATIVE")
    path = PurePosixPath(value)
    need(path.parts and not path.is_absolute() and path.as_posix() == value and
         all(part not in (".", "..") and not part.endswith((".", " ")) and
             not os.path.isreserved(part) and not any(ord(c) < 32 or c in ':*?"<>|' for c in part)
             for part in path.parts), "PRODUCER_ASSEMBLY_RELATIVE")
    return path


def tree(B, root, check):
    actual, pending, entries = set(), [(B.ordinary(root, directory=True), 0)], 0
    while pending:
        directory, depth = pending.pop(); check()
        with os.scandir(directory) as rows:
            for row in rows:
                check(); entries += 1
                need(entries <= 512, "PRODUCER_ASSEMBLY_TREE_BOUND")
                path = Path(row.path)
                if row.is_dir(follow_symlinks=False):
                    need(depth < 8, "PRODUCER_ASSEMBLY_TREE_DEPTH")
                    pending.append((B.ordinary(path, directory=True), depth+1))
                else:
                    actual.add(B.ordinary(path).relative_to(root).as_posix())
    return actual


def inspect_inputs(B, check, source_root):
    """Read exact bounded files; no package code or owner state is imported."""
    source_root = B.ordinary(source_root, directory=True)
    pins = {}

    def keep(path, expected=None, maximum=128*MIB):
        actual = B.pin(path, check, maximum)
        need(expected is None or actual == expected or actual["sha256"] == expected,
             "PRODUCER_ASSEMBLY_INPUT_PIN:"+str(path))
        need(pins.setdefault(str(path), actual) == actual, "PRODUCER_ASSEMBLY_PIN_CONFLICT")
        return actual

    def document(path, digest, *, diagnostic=False):
        pin = keep(path, digest, 2*MIB)
        with path.open("rb") as stream:
            raw = stream.read(2*MIB+1)
        need({"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()} == pin,
             "PRODUCER_ASSEMBLY_DOCUMENT_CHANGED")
        def pairs(items):
            doc = {}
            for key, value in items:
                need(key not in doc, "PRODUCER_ASSEMBLY_DUPLICATE_KEY"); doc[key] = value
            return doc
        def reject(_):
            raise ValueError("PRODUCER_ASSEMBLY_JSON_NUMBER")
        def number(text):
            value = float(text)
            need(diagnostic and math.isfinite(value), "PRODUCER_ASSEMBLY_JSON_NUMBER")
            return value
        return json.loads(raw, object_pairs_hook=pairs, parse_float=number, parse_constant=reject)

    old = document(BASE/"PROFILE.json", BASE_PROFILE)
    receipt = document(BASE/"ASSEMBLY.json", BASE_RECEIPT, diagnostic=True)
    manifest = document(BASE/"installation/INSTALLATION.json", INSTALLATION)
    need(old["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and len(old["files"]) == 137 and
         old["installation_manifest_sha256"] == INSTALLATION and
         receipt["schema"] == "DMKN_ORDINARY_REFERENCE_SUCCESSOR_ASSEMBLY_V1" and
         receipt["status"] == "ASSEMBLED_NOT_ADOPTED" and receipt["profile_sha256"] == BASE_PROFILE and
         receipt["installation_manifest_sha256"] == INSTALLATION and
         receipt["implementation_id"] == IMPLEMENTATION and receipt["files_excluding_profile"] == 165,
         "PRODUCER_ASSEMBLY_PREDECESSOR")
    selected = {}
    for logical, expected in old["files"].items():
        path = BASE.joinpath(*relative(logical).parts)
        selected[logical] = (path, keep(path, expected))
    runtimes = {"python_runtime": PYTHON, "lean_runtime": LEAN}
    for logical, expected in manifest["files"].items():
        parts = relative(logical).parts
        if parts[0] in runtimes:
            keep(runtimes[parts[0]].joinpath(*parts[1:]), expected)
        else:
            path = BASE/"installation"/logical
            selected["installation/"+logical] = (path, keep(path, expected))
    selected["installation/INSTALLATION.json"] = (
        BASE/"installation/INSTALLATION.json", pins[str(BASE/"installation/INSTALLATION.json")])
    need(len(selected) == 165 and tree(B, BASE, check) == set(selected) | {"PROFILE.json", "ASSEMBLY.json"},
         "PRODUCER_ASSEMBLY_PREDECESSOR_CENSUS")
    predecessor = dict(selected)
    source_pins = {}
    for logical, filename in SOURCES.items():
        need((logical in old["files"]) == (logical in OVERLAYS), "PRODUCER_ASSEMBLY_ROLE_SELECTION")
        source = source_root.joinpath(*relative(filename).parts)
        pin = keep(source, maximum=2*MIB); source_pins[logical] = pin
        selected[logical] = (source, pin)
    native = ROOT/EXPORTER_SOURCE
    native_pin = keep(native, EXPORTER_PIN, 32*MIB)
    source_pins[EXPORTER_ROLE] = native_pin
    selected[EXPORTER_ROLE] = (native, native_pin)
    added = sorted(set(selected)-set(predecessor))
    changed = sorted(name for name in set(selected) & set(predecessor)
                     if selected[name][1] != predecessor[name][1])
    need(changed == sorted(OVERLAYS) and added == sorted(ADDITIONS) and len(selected) == 169 and
         len({name.casefold() for name in selected}) == len(selected) and len(pins) <= 256 and
         sum(pin["bytes"] for _, pin in selected.values()) <= 80*MIB,
         "PRODUCER_ASSEMBLY_EXACT_TWO_OVERLAYS_FOUR_ADDITIONS")
    return {"pins": pins, "old": old, "selected": selected, "predecessor": predecessor,
            "source_pins": source_pins, "changed": changed, "added": added,
            "unchanged": sorted(set(predecessor)-set(changed))}


def assemble(args):
    started, cpu = time.monotonic(), time.process_time()
    def check():
        need(time.monotonic()-started < 75 and time.process_time()-cpu < 45,
             "PRODUCER_ASSEMBLY_ORIGINAL_ALLOWANCE")
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and
         Path(sys.executable).resolve() == PYTHON/"python.exe", "PRODUCER_ASSEMBLY_CONTEXT")
    B = helper(); expected_map = hexid(args.payload_map_sha256)
    source_root = B.ordinary(Path(args.source_root), directory=True)
    output = B.ordinary(Path(args.output), directory=True, fresh=True)
    need(output == LOCAL/NAME/"package" and Path(__file__).resolve() == source_root/PREFIX/"assemble.py" and
         not source_root.is_relative_to(output), "PRODUCER_ASSEMBLY_OUTPUT")
    inputs = inspect_inputs(B, check, source_root)
    need(hashlib.sha256(encoded(inputs["source_pins"])).hexdigest() == expected_map,
         "PRODUCER_ASSEMBLY_REVIEWED_MAP")
    for filename in inputs["pins"]:
        path = Path(filename)
        need(not path.is_relative_to(output) and not output.is_relative_to(path),
             "PRODUCER_ASSEMBLY_OVERLAP")
    own_pin = B.pin(Path(__file__).resolve(), check, 2*MIB)
    output.mkdir(); phase = "COPYING"
    try:
        for logical, (source, expected) in sorted(inputs["selected"].items()):
            destination = output/logical
            pending, parent = [], destination.parent
            while not parent.exists():
                need(parent.is_relative_to(output), "PRODUCER_ASSEMBLY_COPY_DIRECTORY")
                pending.append(parent); parent = parent.parent
            B.ordinary(parent, directory=True)
            for directory in reversed(pending):
                B.ordinary(directory, directory=True, fresh=True).mkdir()
            B.ordinary(source); B.ordinary(destination, fresh=True)
            size, digest = 0, hashlib.sha256()
            with source.open("rb") as incoming, destination.open("xb") as outgoing:
                while block := incoming.read(MIB):
                    check(); size += len(block)
                    need(size <= expected["bytes"], "PRODUCER_ASSEMBLY_COPY_GREW")
                    digest.update(block); outgoing.write(block)
                outgoing.flush(); os.fsync(outgoing.fileno())
            need({"bytes": size, "sha256": digest.hexdigest()} == expected and
                 B.pin(destination, check, 128*MIB) == expected, "PRODUCER_ASSEMBLY_COPY_CHANGED")
        phase = "FINAL_VERIFY"
        for filename, expected in inputs["pins"].items():
            need(B.pin(Path(filename), check, 128*MIB) == expected, "PRODUCER_ASSEMBLY_INPUT_CHANGED")
        for logical, (_, expected) in inputs["selected"].items():
            need(B.pin(output/logical, check, 128*MIB) == expected, "PRODUCER_ASSEMBLY_OUTPUT_CHANGED")
        need(tree(B, output, check) == set(inputs["selected"]), "PRODUCER_ASSEMBLY_OUTPUT_CENSUS")
        auxiliary = dict(inputs["old"]["files"])
        # The usage document belongs to the complete assembly map, not to an
        # executable helper role or the loader's import-path census.
        auxiliary.update({name: pin for name, pin in inputs["source_pins"].items()
                          if name != "PRODUCER.md"})
        descriptor = encoded(dict(inputs["old"], files=auxiliary))
        need(len(auxiliary) == 140 and
             set(auxiliary) == set(inputs["old"]["files"]) | (ADDITIONS-{"PRODUCER.md"}) and
             len(descriptor) <= 2*MIB, "PRODUCER_ASSEMBLY_PROFILE")
        result = {"schema": "DMKN_ORDINARY_PRODUCER_ASSEMBLY_V1", "status": "ASSEMBLED_NOT_ADOPTED",
            "base_profile_sha256": BASE_PROFILE, "base_receipt_sha256": BASE_RECEIPT,
            "profile_sha256": hashlib.sha256(descriptor).hexdigest(),
            "installation_manifest_sha256": INSTALLATION, "implementation_id": IMPLEMENTATION,
            "files_excluding_profile": 169, "copied_bytes": sum(pin["bytes"] for _, pin in inputs["selected"].values()),
            "reviewed_payload_map_sha256": expected_map, "source_payloads": inputs["source_pins"],
            "source_mapping": SOURCES, "retained_native_mapping": {EXPORTER_ROLE: EXPORTER_SOURCE},
            "payloads": {name: pin for name, (_, pin) in inputs["selected"].items()},
            "assembler": own_pin, "added": inputs["added"],
            "changed": inputs["changed"], "unchanged": inputs["unchanged"],
            "wall_seconds_before_commit": time.monotonic()-started,
            "cpu_seconds_before_commit": time.process_time()-cpu,
            "claim": "FILE_ONLY_CONSOLIDATED_PRODUCER_NO_NATIVE_EXECUTION_OR_MATHEMATICAL_ACCEPTANCE"}
        B.save_json(output/"ASSEMBLY.json", result)
        B.fresh_bytes(output/".PROFILE.pending", descriptor)
        check(); B.ordinary(output/"PROFILE.json", fresh=True)
        (output/".PROFILE.pending").rename(output/"PROFILE.json")
        return result
    except BaseException as error:
        try:
            B.save_json(output/"ASSEMBLY-FAILURE.json", {"phase": phase, "error_type": type(error).__name__,
                "error": str(error)[:2000], "wall_seconds": time.monotonic()-started,
                "cpu_seconds": time.process_time()-cpu, "retention": "PARTIAL_FILES_PRESERVED_NO_RETRY"})
        except BaseException:
            pass
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("source-root", "output", "payload-map-sha256"):
        parser.add_argument("--"+name, required=True)
    print(json.dumps(assemble(parser.parse_args()), sort_keys=True, allow_nan=False), flush=True)


