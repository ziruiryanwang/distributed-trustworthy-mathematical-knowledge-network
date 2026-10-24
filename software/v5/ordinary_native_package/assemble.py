"""File-only native-first distribution from explicitly selected pinned inputs.

No product modules, compiler, owner state or network are executed. This is not a
clean-source compiler build. All existing acceptance/native bytes are preserved;
only two facade roles change and five baseline roles are added. The caller must
provide outer process containment for hard limits; controller bounds cooperate.
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

MIB = 1024**2
PREFIX = "software/v5/ordinary_native_package/"
BUILDER = "software/v5/ordinary_package/build.py"
BUILDER_SHA = "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5"
BASE_PROFILE = "ab04e72440bcd09381a81d4b721d1103fa2e62bc260fa6c0434e6c568419016f"
BASE_RECEIPT = "6e09d2b255d8321bd522291276e03f10729cbc4f57536a57b29b63ab67a528bc"
INSTALLATION = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
IMPLEMENTATION = "fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df"
EXPORTER_ROLE = "authoring/bin/BaselineExporter.exe"
EXPORTER_PIN = {"bytes": 809472,
    "sha256": "2adcffad1ad4967f093e1acc6c31295c2519e7f9cbf35d04bee37d8580cc3c4f"}
SOURCES = {
    "owner.py": PREFIX+"owner.py", "profile.py": PREFIX+"profile.py",
    "authoring/py/baseline_production.py": "software/v5/ordinary_producer_package/baseline_production.py",
    "authoring/py/baseline_worker.py": "software/v5/ordinary_baseline/baseline_worker.py",
    "reference/baseline_bundle.py": "software/v5/ordinary_baseline/baseline_bundle.py",
    "reference/baseline_intake.py": "software/v5/ordinary_baseline/baseline_intake.py",
}
DOCUMENTS = {"README.md": PREFIX+"README.md",
             "PRODUCER.md": "software/v5/ordinary_producer_package/README.md"}
OVERLAYS = {"owner.py", "profile.py"}
ADDITIONS = (set(SOURCES)-OVERLAYS) | {EXPORTER_ROLE}


def need(ok, code):
    if not ok:
        raise ValueError(code)


def hexid(value):
    need(type(value) is str and len(value) == 64 and
         all(char in "0123456789abcdef" for char in value), "NATIVE_ASSEMBLY_HASH")
    return value


def encoded(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True,
                      allow_nan=False, separators=(",", ":")).encode("ascii")


def helper(source_root):
    """Load only exact adopted stdlib file helpers, never product support."""
    path = Path(source_root)/BUILDER
    need(path.is_absolute(), "NATIVE_ASSEMBLY_HELPER_ABSOLUTE")
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(0 < len(raw) <= 2*MIB and hashlib.sha256(raw).hexdigest() == BUILDER_SHA,
         "NATIVE_ASSEMBLY_HELPER_PIN")
    name = "_native_assembly_file_helper"
    need(name not in sys.modules, "NATIVE_ASSEMBLY_PRELOADED_HELPER")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    module.ordinary(path)
    return module


def relative(value):
    need(type(value) is str and 0 < len(value) <= 1024 and "\\" not in value,
         "NATIVE_ASSEMBLY_RELATIVE")
    path = PurePosixPath(value)
    need(path.parts and not path.is_absolute() and path.as_posix() == value and
         all(part not in (".", "..") and not part.endswith((".", " ")) and
             not os.path.isreserved(part) and
             not any(ord(char) < 32 or char in ':*?"<>|' for char in part)
             for part in path.parts), "NATIVE_ASSEMBLY_RELATIVE")
    return path


def tree(B, root, check):
    actual, pending, entries = set(), [(B.ordinary(root, directory=True), 0)], 0
    while pending:
        directory, depth = pending.pop()
        check()
        with os.scandir(directory) as listing:
            for row in listing:
                check()
                entries += 1
                need(entries <= 512, "NATIVE_ASSEMBLY_TREE_BOUND")
                path = Path(row.path)
                if row.is_dir(follow_symlinks=False):
                    need(depth < 8, "NATIVE_ASSEMBLY_TREE_DEPTH")
                    pending.append((B.ordinary(path, directory=True), depth+1))
                else:
                    actual.add(B.ordinary(path).relative_to(root).as_posix())
    return actual


def inspect_inputs(B, args, check):
    """Read/pin all bounded inputs and return a complete map without writing.

    A root selector may use this same census to prepare its finite allocation.
    No package code or owner state is imported. Paths are explicit local choices.
    """
    source_root = B.ordinary(Path(args.source_root), directory=True)
    base = B.ordinary(Path(args.base_package), directory=True)
    runtimes = {name: B.ordinary(Path(getattr(args, name)), directory=True)
                for name in ("python_runtime", "lean_runtime")}
    need(Path(sys.executable).resolve() == runtimes["python_runtime"]/"python.exe",
         "NATIVE_ASSEMBLY_SELECTED_PYTHON")
    pins = {}

    def keep(path, expected=None, maximum=128*MIB):
        pin = B.pin(path, check, maximum)
        need(expected is None or pin == expected or pin["sha256"] == expected,
             "NATIVE_ASSEMBLY_INPUT_PIN:"+str(path))
        need(pins.setdefault(str(path), pin) == pin, "NATIVE_ASSEMBLY_PIN_CONFLICT")
        return pin

    def document(path, digest, diagnostic=False):
        pin = keep(path, digest, 2*MIB)
        with path.open("rb") as stream:
            raw = stream.read(2*MIB+1)
        need({"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()} == pin,
             "NATIVE_ASSEMBLY_DOCUMENT_CHANGED")
        def pairs(items):
            result = {}
            for key, value in items:
                need(key not in result, "NATIVE_ASSEMBLY_DUPLICATE_KEY")
                result[key] = value
            return result
        def reject(_):
            raise ValueError("NATIVE_ASSEMBLY_JSON_NUMBER")
        def number(text):
            value = float(text)
            need(diagnostic and math.isfinite(value), "NATIVE_ASSEMBLY_JSON_NUMBER")
            return value
        return json.loads(raw, object_pairs_hook=pairs, parse_float=number,
                          parse_constant=reject)

    old = document(base/"PROFILE.json", BASE_PROFILE)
    receipt = document(base/"ASSEMBLY.json", BASE_RECEIPT, True)
    manifest = document(base/"installation/INSTALLATION.json", INSTALLATION)
    mapping = document(source_root/PREFIX/"source-map.json", hexid(args.source_map_sha256))
    need(type(mapping) is dict and set(mapping) == {"schema", "source_payloads", "retained_payloads", "documentation"}
         and mapping["schema"] == "DMKN_ORDINARY_NATIVE_ASSEMBLY_MAP_V1",
         "NATIVE_ASSEMBLY_MAP_FIELDS")
    need(old["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and len(old["files"]) == 106 and
         old["installation_manifest_sha256"] == INSTALLATION and
         receipt["status"] == "ASSEMBLED_NOT_ADOPTED" and
         receipt["profile_sha256"] == BASE_PROFILE and
         receipt["installation_manifest_sha256"] == INSTALLATION and
         receipt["implementation_id"] == IMPLEMENTATION and receipt["files_excluding_profile"] == 134,
         "NATIVE_ASSEMBLY_PREDECESSOR")
    keep(source_root/BUILDER, BUILDER_SHA, 2*MIB)
    keep(source_root/PREFIX/"assemble.py", maximum=2*MIB)
    selected = {}
    for logical, expected in old["files"].items():
        path = base.joinpath(*relative(logical).parts)
        selected[logical] = (path, keep(path, expected))
    for logical, expected in manifest["files"].items():
        parts = relative(logical).parts
        if parts[0] in runtimes:
            keep(runtimes[parts[0]].joinpath(*parts[1:]), expected)
        else:
            path = base/"installation"/logical
            selected["installation/"+logical] = (path, keep(path, expected))
    selected["installation/INSTALLATION.json"] = (
        base/"installation/INSTALLATION.json", pins[str(base/"installation/INSTALLATION.json")])
    need(len(selected) == 134 and
         tree(B, base, check) == set(selected) | {"PROFILE.json", "ASSEMBLY.json"},
         "NATIVE_ASSEMBLY_PREDECESSOR_CENSUS")
    predecessor, source_pins = dict(selected), {}
    for category, roles in (("source_payloads", SOURCES), ("documentation", DOCUMENTS)):
        rows = mapping[category]
        need(type(rows) is dict and set(rows) == set(roles), "NATIVE_ASSEMBLY_MAP_ROLES")
        for logical, filename in roles.items():
            row = rows[logical]
            need(type(row) is dict and set(row) == {"source", "bytes", "sha256"} and
                 row["source"] == filename and type(row["bytes"]) is int and
                 0 < row["bytes"] <= 2*MIB, "NATIVE_ASSEMBLY_MAP_SOURCE")
            expected = {"bytes": row["bytes"], "sha256": hexid(row["sha256"])}
            path = source_root.joinpath(*relative(filename).parts)
            source_pins[logical] = keep(path, expected, 2*MIB)
            selected[logical] = (path, source_pins[logical])
    need(mapping["retained_payloads"] == {EXPORTER_ROLE: EXPORTER_PIN},
         "NATIVE_ASSEMBLY_EXPORTER_SELECTION")
    exporter = B.ordinary(Path(args.exporter))
    selected[EXPORTER_ROLE] = (exporter, keep(exporter, EXPORTER_PIN, 32*MIB))
    source_pins[EXPORTER_ROLE] = EXPORTER_PIN
    changed = sorted(name for name in set(predecessor) & set(selected)
                     if predecessor[name][1] != selected[name][1])
    added = sorted(set(selected)-set(predecessor))
    need(changed == sorted(OVERLAYS) and added == sorted(ADDITIONS | set(DOCUMENTS)) and
         len(selected) == 141 and len({name.casefold() for name in selected}) == 141 and
         len(pins) <= 256 and sum(pin["bytes"] for _, pin in selected.values()) <= 80*MIB,
         "NATIVE_ASSEMBLY_EXACT_DELTA")
    return {"pins": pins, "old": old, "selected": selected, "predecessor": predecessor,
            "source_pins": source_pins, "changed": changed, "added": added,
            "unchanged": sorted(set(predecessor)-set(changed)), "base": base,
            "source_root": source_root, "runtimes": runtimes}


def assemble(args):
    started, cpu = time.monotonic(), time.process_time()
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "NATIVE_ASSEMBLY_CONTEXT")
    need(type(args.wall_seconds) is int and 10 <= args.wall_seconds <= 600 and
         type(args.cpu_seconds) is int and 5 <= args.cpu_seconds <= 600,
         "NATIVE_ASSEMBLY_FINITE_ALLOWANCE")
    def check():
        need(time.monotonic()-started < args.wall_seconds and
             time.process_time()-cpu < args.cpu_seconds, "NATIVE_ASSEMBLY_ALLOWANCE")
    B = helper(args.source_root)
    output = B.ordinary(Path(args.output), directory=True, fresh=True)
    need(Path(__file__).absolute() == Path(args.source_root)/PREFIX/"assemble.py",
         "NATIVE_ASSEMBLY_RUNNING_SOURCE")
    inputs = inspect_inputs(B, args, check)
    for path in (inputs["base"], *inputs["runtimes"].values()):
        need(not output.is_relative_to(path) and not path.is_relative_to(output),
             "NATIVE_ASSEMBLY_DIRECTORY_OVERLAP")
    need(not inputs["source_root"].is_relative_to(output), "NATIVE_ASSEMBLY_SOURCE_OVERLAP")
    for name in inputs["pins"]:
        path = Path(name)
        need(not path.is_relative_to(output) and not output.is_relative_to(path),
             "NATIVE_ASSEMBLY_FILE_OVERLAP")
    output.mkdir()
    phase = "COPYING"
    try:
        for logical, (source, expected) in sorted(inputs["selected"].items()):
            target = output/logical
            missing, parent = [], target.parent
            while not parent.exists():
                need(parent.is_relative_to(output), "NATIVE_ASSEMBLY_COPY_DIRECTORY")
                missing.append(parent)
                parent = parent.parent
            B.ordinary(parent, directory=True)
            for directory in reversed(missing):
                B.ordinary(directory, directory=True, fresh=True).mkdir()
            B.ordinary(source)
            B.ordinary(target, fresh=True)
            size, digest = 0, hashlib.sha256()
            with source.open("rb") as incoming, target.open("xb") as outgoing:
                while block := incoming.read(MIB):
                    check()
                    size += len(block)
                    need(size <= expected["bytes"], "NATIVE_ASSEMBLY_COPY_GREW")
                    digest.update(block)
                    outgoing.write(block)
                outgoing.flush()
                os.fsync(outgoing.fileno())
            need({"bytes": size, "sha256": digest.hexdigest()} == expected and
                 B.pin(target, check, 128*MIB) == expected, "NATIVE_ASSEMBLY_COPY_CHANGED")
        phase = "FINAL_VERIFY"
        for name, expected in inputs["pins"].items():
            need(B.pin(Path(name), check, 128*MIB) == expected, "NATIVE_ASSEMBLY_INPUT_CHANGED")
        for logical, (_, expected) in inputs["selected"].items():
            need(B.pin(output/logical, check, 128*MIB) == expected, "NATIVE_ASSEMBLY_OUTPUT_CHANGED")
        need(tree(B, output, check) == set(inputs["selected"]), "NATIVE_ASSEMBLY_OUTPUT_CENSUS")
        auxiliary = dict(inputs["old"]["files"])
        auxiliary.update({name: pin for name, pin in inputs["source_pins"].items() if name not in DOCUMENTS})
        need(len(auxiliary) == 111 and set(auxiliary) == set(inputs["old"]["files"]) | ADDITIONS,
             "NATIVE_ASSEMBLY_PROFILE_ROLES")
        descriptor = encoded(dict(inputs["old"], files=auxiliary))
        need(len(descriptor) <= 2*MIB, "NATIVE_ASSEMBLY_PROFILE_BOUND")
        result = {"schema": "DMKN_ORDINARY_NATIVE_ASSEMBLY_V1", "status": "ASSEMBLED_NOT_ADOPTED",
            "base_profile_sha256": BASE_PROFILE, "base_receipt_sha256": BASE_RECEIPT,
            "profile_sha256": hashlib.sha256(descriptor).hexdigest(),
            "installation_manifest_sha256": INSTALLATION, "implementation_id": IMPLEMENTATION,
            "source_map_sha256": args.source_map_sha256,
            "files_excluding_profile": len(inputs["selected"]), "profile_files": len(auxiliary),
            "copied_bytes": sum(pin["bytes"] for _, pin in inputs["selected"].values()),
            "payloads": {name: pin for name, (_, pin) in inputs["selected"].items()},
            "source_mapping": SOURCES, "documentation_mapping": DOCUMENTS,
            "source_payloads": inputs["source_pins"],
            "assembler": inputs["pins"][str(inputs["source_root"]/PREFIX/"assemble.py")],
            "added": inputs["added"], "changed": inputs["changed"], "unchanged": inputs["unchanged"],
            "wall_seconds_before_commit": time.monotonic()-started,
            "cpu_seconds_before_commit": time.process_time()-cpu,
            "claim": "FILE_ONLY_NATIVE_FIRST_ASSEMBLY_NOT_SOURCE_BUILD_OR_MATHEMATICAL_ACCEPTANCE"}
        B.save_json(output/"ASSEMBLY.json", result)
        B.fresh_bytes(output/".PROFILE.pending", descriptor)
        check()
        B.ordinary(output/"PROFILE.json", fresh=True)
        (output/".PROFILE.pending").rename(output/"PROFILE.json")
        return result
    except BaseException as error:
        try:
            B.save_json(output/"ASSEMBLY-FAILURE.json", {"phase": phase,
                "error_type": type(error).__name__, "error": str(error)[:2000],
                "wall_seconds": time.monotonic()-started, "cpu_seconds": time.process_time()-cpu,
                "retention": "PARTIAL_FILES_PRESERVED_NO_RETRY"})
        except BaseException:
            pass
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("source-root", "base-package", "exporter", "python-runtime", "lean-runtime",
                 "output", "source-map-sha256"):
        parser.add_argument("--"+name, required=True)
    for name in ("wall-seconds", "cpu-seconds"):
        parser.add_argument("--"+name, required=True, type=int)
    print(json.dumps(assemble(parser.parse_args()), sort_keys=True, allow_nan=False), flush=True)
