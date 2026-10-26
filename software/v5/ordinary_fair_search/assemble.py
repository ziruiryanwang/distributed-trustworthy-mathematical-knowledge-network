"""File-only fair-search overlay of an explicitly approved ordinary package.

Run with Python -I -S -B. No product imports, compilers, network or state access.
The selected base must have the bounded-investigator role map. A fresh source
build may supply different native bytes through its explicit selected manifests.
Immutable owner-approved storage is assumed; this is not a hostile-writer lock.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import stat
import sys
import time

MIB = 1024**2
PREFIX = "software/v5/ordinary_fair_search/"
OWNER_SHA = "56ef042f652fcb88cae7d16ab74883016a469e2e82777c1a173f842f5ef8245a"
LOADER_SHA = "6b77a4a4198e0e6495ddf7bf4e8b6a1ee2985d7e9ec4a0aea46208f7c7eec1e5"
BUILDER_SHA = "79a056932d5720e9ab964ee50a01d1b04569a60a5e6445df0070a2b6556b42f9"
SOURCE_MAP_SHA = "e9b7a873c8e509651833de51e5bd6beda130c74fdf7391859a8661c08426396a"
DOCUMENTS = {
    "LAUNCHER.md": {"bytes": 6797, "sha256": "759dcd6c656d9f3c91a0b2a7c0befa982211249f44339b3a37b4b834929bfe8e"},
    "PRODUCER.md": {"bytes": 5051, "sha256": "8904e3e83c0d93880f488c4df0a003b0e499389cdf4bc4915d10b466ca8d4b45"},
    "README.md": {"bytes": 12189, "sha256": "d9c18e50bda2e4149235b6dfa468e7587eb2789a95309f0752ac79a4ada4610a"},
    "RECEIVE-POLICY.md": {"bytes": 5534, "sha256": "d912e971106d7ad22e477466fbd2b5f0dc0d079e70a25d6e1bebfca83cac588d"},
}
OVERLAY = {
    "profile.py": ("profile.py", "828031e82f3dd43865d189587affa61dd6f8abe5b8667d45da0673949a069743"),
    "peer_api.py": ("peer_api.py", "06663bcda04345cb9ea38ca422d7545b5736a208c2d79742bebc095f5409b7e5"),
    "support/transport/fair_exchange.py": ("fair_exchange.py", "3fe626b2dc4e63c345e54a517b1b37eea6eedada6d0fbb497aa18745a93eb828"),
    "support/discovery/fair_search.py": ("fair_search.py", "2567fcb2308c7e477c08b958a3661348eee682c5a98ce2389dd9add02d48e652"),
    "README.md": ("README.md", "c3d8642b6fe9ece1b12c3a313910d14c52442b78a94c8af1b44dbe0901115aa5"),
}
NATIVE = "OriginalExpr OriginalDecl CheckedExtension BootstrapSupport OwnerRebind OwnerConstruction OwnerUseCommand OrdinaryExport SuccessorExport SuccessorExportCommand PortableOwnerConstructCommand PortableConstructExportCommand PortableContributionExportCommand OwnerQueryCommand".split()
AUTHOR = "ordinary_contribution portable_owner_request owner_request portable_candidate portable_preview ordinary_preview library_completion completion_api retained_preparation supervised_library_exchange library_extraction module_closure anchor_store module_export formal_query baseline_production baseline_worker".split()
SUPPORT = "transport/ordinary_acquisition.py transport/http_provider.py transport/authoring_offers.py transport/clients.py discovery/formal_features.py discovery/discovery_store.py discovery/authenticated_index.py discovery/summary_wire.py custody/module_store.py discovery/ordinary_export_adapter.py discovery/search_session.py discovery/discovery_query.py discovery/candidate_query.py".split()
BASE_AUX = set("author_worker.py module_worker.py owner.py peer.py peer_api.py profile.py query.py run.py module/OrdinaryModule.lean authoring/bin/BaselineExporter.exe authoring/bin/MissingImportExporter.exe reference/baseline_bundle.py reference/baseline_intake.py".split())
BASE_AUX.update("authoring/py/" + name + ".py" for name in AUTHOR)
BASE_AUX.update("support/" + name for name in SUPPORT)
BASE_AUX.update("authoring/helpers/" + name + suffix for name in NATIVE
                for suffix in (".olean", ".olean.private", ".olean.server", ".ir", ".ir.sig"))
INST_NATIVE = "BasisSnapshot BootstrapSupport CheckedExtension LocalSnapshot OrdinaryExport OrdinaryWorkflowWorker OriginalDecl OriginalExpr".split()
INST_FILES = set("foundation/inventory.json foundation/seed.json py/local_catalog.py py/ordinary_admission.py py/ordinary_evidence.py py/ordinary_semantics.py py/portable_catalog.py py/portable_evidence.py supervisor/commons.py supervisor/domains.py supervisor/run_stage.py".split())
INST_FILES.update("lean-" + kind + "/" + name + suffix for name in INST_NATIVE
                  for kind, suffix in (("lib", ".olean"), ("src", ".lean")))
RUNTIME_FILES = set("python_runtime/python.exe python_runtime/python3.dll python_runtime/python314.dll lean_runtime/bin/lean.exe lean_runtime/bin/libInit_shared.dll lean_runtime/bin/libc++.dll lean_runtime/bin/libleanshared.dll lean_runtime/bin/libleanshared_1.dll lean_runtime/bin/libleanshared_2.dll".split())


def need(ok, code):
    if not ok:
        raise ValueError("FAIR_ASSEMBLY_" + code)


def hexid(value):
    need(type(value) is str and len(value) == 64 and
         all(c in "0123456789abcdef" for c in value), "HASH")
    return value


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def relative(name):
    need(type(name) is str and 0 < len(name) <= 1024, "RELATIVE_PATH")
    path = PurePosixPath(name)
    need(not path.is_absolute() and path.as_posix() == name and path.parts and
         len(path.parts) <= 8 and all(part not in (".", "..") and
             not part.endswith((".", " ")) and not os.path.isreserved(part) and
             not any(ord(c) < 32 or c in ':*?"<>|\\' for c in part)
             for part in path.parts), "RELATIVE_PATH")
    return name


def ordinary(value, *, directory=False, fresh=False):
    path = Path(value)
    need(path.is_absolute() and len(path.parts) <= 128 and len(str(path)) <= 32768
         and ".." not in path.parts and path != Path(path.anchor) and
         not str(path).startswith(("\\\\", "//")), "ABSOLUTE_LOCAL_PATH")
    need(len(path.drive) == 2 and path.drive[0].isalpha() and path.drive[1] == ":",
         "LOCAL_DRIVE")
    for name in path.parts[1:]:
        relative(name)
    for part in (*reversed(path.parents), path):
        try:
            info = part.lstat()
        except FileNotFoundError:
            need(fresh and part == path, "MISSING_PARENT_OR_INPUT")
            return path
        need(not stat.S_ISLNK(info.st_mode) and
             not (getattr(info, "st_file_attributes", 0) & 0x400), "REDIRECTED_PATH")
        if part != path or directory:
            need(stat.S_ISDIR(info.st_mode), "DIRECTORY")
        else:
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "SINGLE_FILE")
    need(not fresh, "OUTPUT_EXISTS")
    return path


def pin_shape(pin):
    need(type(pin) is dict and set(pin) == {"bytes", "sha256"} and
         type(pin["bytes"]) is int and 0 < pin["bytes"] <= 128*MIB, "PIN_SHAPE")
    hexid(pin["sha256"])
    return pin


def pin(path, check, maximum=128*MIB):
    check(); path = ordinary(path)
    length = path.stat().st_size
    need(0 < length <= maximum, "FILE_BOUND")
    count, hashed = 0, hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(MIB):
            check(); count += len(block)
            need(count <= length, "FILE_GREW")
            hashed.update(block)
    need(ordinary(path).stat().st_size == count == length, "FILE_CHANGED")
    return {"bytes": count, "sha256": hashed.hexdigest()}


def read_json(path, expected_sha, check):
    expected = pin(path, check, 2*MIB)
    need(expected["sha256"] == hexid(expected_sha), "JSON_PIN")
    with ordinary(path).open("rb") as stream:
        raw = stream.read(2*MIB + 1)
    need(len(raw) == expected["bytes"] and digest(raw) == expected_sha, "JSON_CHANGED")
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "JSON_DUPLICATE")
            result[key] = value
        return result
    def finite(value):
        result = float(value)
        need(math.isfinite(result), "JSON_NONFINITE")
        return result
    def reject(_):
        raise ValueError("FAIR_ASSEMBLY_JSON_NONFINITE")
    doc = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                     parse_float=finite, parse_constant=reject)
    need(type(doc) is dict, "JSON_OBJECT")
    check()
    return doc, expected


def census(root, names, check):
    actual, entries, pending = set(), 0, [(ordinary(root, directory=True), 0)]
    while pending:
        directory, depth = pending.pop()
        with os.scandir(directory) as listing:
            for entry in listing:
                check(); entries += 1
                need(entries <= 512, "CENSUS_BOUND")
                path = Path(entry.path)
                if entry.is_dir(follow_symlinks=False):
                    need(depth < 8, "CENSUS_DEPTH")
                    pending.append((ordinary(path, directory=True), depth + 1))
                else:
                    actual.add(relative(ordinary(path).relative_to(root).as_posix()))
    need(actual == set(names) and len({n.casefold() for n in actual}) == len(actual),
         "EXACT_CENSUS")


def fresh_bytes(path, raw):
    need(0 < len(raw) <= 2*MIB, "OUTPUT_JSON_BOUND")
    with ordinary(path, fresh=True).open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())


def assemble(args):
    started, cpu_started = time.monotonic(), time.process_time()
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "PYTHON")
    need(type(args.wall_seconds) is int and 10 <= args.wall_seconds <= 600 and
         type(args.cpu_seconds) is int and 5 <= args.cpu_seconds <= 600, "ALLOWANCE")
    def check():
        need(time.monotonic() - started < args.wall_seconds and
             time.process_time() - cpu_started < args.cpu_seconds, "ALLOWANCE_EXHAUSTED")

    root = ordinary(args.source_root, directory=True)
    base = ordinary(args.base_package, directory=True)
    receipt_path = ordinary(args.base_build_receipt)
    output = ordinary(args.output, directory=True, fresh=True)
    for selected in (base, receipt_path):
        need(not selected.is_relative_to(output) and not output.is_relative_to(selected),
             "OUTPUT_OVERLAP")
    need(not root.is_relative_to(output), "SOURCE_OVERLAP")
    old, old_pin = read_json(base/"PROFILE.json", args.base_profile_sha256, check)
    receipt, receipt_pin = read_json(receipt_path, args.base_build_receipt_sha256, check)
    need(set(old) == {"schema", "installation_manifest_sha256", "helper_paths",
                     "author_worker", "files"} and
         old["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
         old["helper_paths"] == ["authoring/helpers"] and
         old["author_worker"] == "author_worker.py" and
         type(old["files"]) is dict and set(old["files"]) == BASE_AUX and
         len(BASE_AUX) == 113, "BASE_PROFILE_LAYOUT")
    need(receipt.get("status") == "BUILT_NOT_ADOPTED" and
         receipt.get("claim") == "SOURCE_BUILD_AND_ASSEMBLY_NOT_OWNER_OR_MATHEMATICAL_ACCEPTANCE" and
         receipt.get("profile_sha256") == args.base_profile_sha256 and
         receipt.get("installation_manifest_sha256") == old["installation_manifest_sha256"] and
         receipt.get("source_map_sha256") == SOURCE_MAP_SHA and
         type(receipt.get("builder")) is dict and
         receipt["builder"].get("sha256") == BUILDER_SHA and
         receipt.get("auxiliary_files") == 113 and
         receipt.get("files_excluding_profile") == 145 and
         receipt.get("documentation_files") == DOCUMENTS, "BUILD_RECEIPT_BINDING")
    installed, installed_pin = read_json(base/"installation/INSTALLATION.json",
                                        old["installation_manifest_sha256"], check)
    need(installed.get("schema") == "DMKN_ORDINARY_NATIVE_INSTALLATION_V1" and
         type(installed.get("files")) is dict and
         set(installed["files"]) == INST_FILES | RUNTIME_FILES and
         len(INST_FILES) == 27 and type(installed.get("implementation")) is dict,
         "INSTALLATION_LAYOUT")
    implementation = digest(b"DMKN-ORDINARY-IMPLEMENTATION-CLAIM-V1\0" +
                            canonical(installed["implementation"]))
    need(receipt.get("implementation_id") == implementation, "IMPLEMENTATION_BINDING")
    baseline = dict(old["files"])
    baseline.update({"installation/" + name: value for name, value in installed["files"].items()
                     if name in INST_FILES})
    baseline["installation/INSTALLATION.json"] = installed_pin
    baseline.update(DOCUMENTS)
    baseline["PROFILE.json"] = old_pin
    for value in installed["files"].values():
        pin_shape(value)  # External runtime pins remain inert, not opened here.
    need(len(baseline) == 146 and sum(pin_shape(p)["bytes"] for p in baseline.values())
         <= 768*MIB, "BASE_MAP_BOUND")
    need(baseline["owner.py"]["sha256"] == OWNER_SHA and
         baseline["profile.py"]["sha256"] == LOADER_SHA, "BASE_VERSION")
    census(base, baseline, check)
    for name, expected in baseline.items():
        need(pin(base/relative(name), check) == expected, "BASE_INPUT_PIN")

    overlay = {}
    for name, (source_name, expected_sha) in OVERLAY.items():
        source = root/PREFIX/source_name
        need(not source.is_relative_to(output), "OVERLAY_OVERLAP")
        source_pin = pin(source, check, 2*MIB)
        need(source_pin["sha256"] == expected_sha, "OVERLAY_SOURCE_PIN")
        overlay[name] = (source, source_pin)
    own_pin = pin(root/PREFIX/"assemble.py", check, 2*MIB)
    need(pin(Path(__file__).absolute(), check, 2*MIB) == own_pin, "RUNNING_SOURCE")
    selected = {name: (base/name, value) for name, value in baseline.items()
                if name != "PROFILE.json"}
    selected.update(overlay)
    need(len(selected) == 147 and sum(p["bytes"] for _, p in selected.values())
         <= 768*MIB, "SUCCESSOR_MAP_BOUND")
    auxiliary = dict(old["files"])
    auxiliary.update({name: p for name, (_, p) in overlay.items() if name != "README.md"})
    need(len(auxiliary) == 115, "SUCCESSOR_PROFILE_COUNT")
    descriptor = dict(old, files=auxiliary)
    raw = canonical(descriptor)
    need(len(raw) <= 2*MIB, "PROFILE_BOUND")

    check(); ordinary(output, directory=True, fresh=True).mkdir()
    package, phase = output/"package", "CREATE_PACKAGE"
    try:
        ordinary(package, directory=True, fresh=True).mkdir()
        phase = "COPY"
        for name, (source, expected) in sorted(selected.items()):
            check(); target = package/relative(name)
            parent = package
            for segment in target.relative_to(package).parts[:-1]:
                parent = parent/segment
                if not parent.exists():
                    ordinary(parent, directory=True, fresh=True).mkdir()
                ordinary(parent, directory=True)
            count, hashed = 0, hashlib.sha256()
            with ordinary(source).open("rb") as inp, ordinary(target, fresh=True).open("xb") as out:
                while block := inp.read(MIB):
                    check(); count += len(block)
                    need(count <= expected["bytes"], "SOURCE_GREW")
                    hashed.update(block); out.write(block)
                out.flush(); os.fsync(out.fileno())
            need(count == expected["bytes"] and hashed.hexdigest() == expected["sha256"],
                 "SOURCE_CHANGED")
        phase = "FINAL_INPUT_OUTPUT_CHECK"
        census(base, baseline, check)
        for name, expected in baseline.items():
            need(pin(base/name, check) == expected, "BASE_FINAL_PIN")
        need(pin(receipt_path, check, 2*MIB) == receipt_pin and
             pin(root/PREFIX/"assemble.py", check, 2*MIB) == own_pin, "SELECTION_CHANGED")
        for name, (source, expected) in selected.items():
            need(pin(source, check) == expected and pin(package/name, check) == expected,
                 "FINAL_PIN")
        census(package, selected, check)
        phase = "PROFILE_COMMIT"
        fresh_bytes(package/".PROFILE.pending", raw)
        check(); ordinary(package/"PROFILE.json", fresh=True)
        (package/".PROFILE.pending").rename(package/"PROFILE.json")
        need(pin(package/"PROFILE.json", check, 2*MIB) ==
             {"bytes": len(raw), "sha256": digest(raw)}, "PROFILE_COMMIT_PIN")
        census(package, set(selected) | {"PROFILE.json"}, check)
        result = {"status": "ASSEMBLED_NOT_ADOPTED", "package": str(package),
            "base_profile_sha256": args.base_profile_sha256,
            "base_build_receipt": receipt_pin, "profile_sha256": digest(raw),
            "installation_manifest_sha256": old["installation_manifest_sha256"],
            "implementation_id": implementation, "assembler": own_pin,
            "files_excluding_profile": len(selected), "auxiliary_files": len(auxiliary),
            "documentation_files": {name: selected[name][1] for name in DOCUMENTS},
            "changed_or_added": {name: p for name, (_, p) in overlay.items()},
            "unchanged_payloads": 142,
            "copied_bytes": sum(p["bytes"] for _, p in selected.values()),
            "wall_seconds_before_receipt": time.monotonic()-started,
            "cpu_seconds_before_receipt": time.process_time()-cpu_started,
            "claim": "FILE_ONLY_SUCCESSOR_NO_NATIVE_BUILD_STATE_OR_MATHEMATICAL_ACCEPTANCE"}
        phase = "EXTERNAL_RECEIPT"
        check(); fresh_bytes(output/"ASSEMBLY.json", canonical(result))
        check()
        return result
    except BaseException as error:
        try:
            fresh_bytes(output/"ASSEMBLY-FAILURE.json", canonical({"phase": phase,
                "error_type": type(error).__name__, "error": str(error)[:2000],
                "wall_seconds": time.monotonic()-started,
                "cpu_seconds": time.process_time()-cpu_started,
                "retention": "PARTIAL_FILES_PRESERVED_NO_RETRY"}))
        except BaseException:
            pass
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for field in ("source-root", "base-package", "base-profile-sha256",
                  "base-build-receipt", "base-build-receipt-sha256", "output"):
        parser.add_argument("--" + field, required=True)
    for field in ("wall-seconds", "cpu-seconds"):
        parser.add_argument("--" + field, required=True, type=int)
    print(json.dumps(assemble(parser.parse_args()), sort_keys=True, allow_nan=False))
