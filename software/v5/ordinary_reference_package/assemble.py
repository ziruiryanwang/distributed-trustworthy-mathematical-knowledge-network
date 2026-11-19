"""File-only successor for protected ordinary-library registration and delta reuse.

Preserve the exact preview package and native acceptance installation. Copy only
explicitly selected fresh sources and successful retained native artifacts.
Separate legacy reference helpers from modern ordinary authoring. No compiler,
Lean import, owner/custody open, admission, registration or network call occurs.
This controller is cooperative; the root-selected enclosing Job supplies hard
process limits. Failure retains partial files; PROFILE.json is committed last.
"""
from pathlib import Path
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
PREFIX = "software/v5/ordinary_reference_package/"
NAME = "ordinary-reference-assembly-01"
BASE = LOCAL/"ordinary-preview-assembly-01/package"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
BUILDER = "software/v5/ordinary_package/build.py"
BUILDER_SHA = "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5"
BASE_PROFILE = "ab04e72440bcd09381a81d4b721d1103fa2e62bc260fa6c0434e6c568419016f"
BASE_RECEIPT = "6e09d2b255d8321bd522291276e03f10729cbc4f57536a57b29b63ab67a528bc"
BASE_OWNER = "2d4de791436d86810ef192e6a776cdbc0b45076f8c0bc75458e35e005cb6cbbe"
BASE_LOADER = "8f690bd50b5ded03da309ad7c42850954aac80d889650442cbba3110028ee48d"
SOURCES = {
    "owner.py": PREFIX+"owner.py",
    "profile.py": PREFIX+"profile.py",
    **{"reference/"+name+".py": "software/v5/ordinary_baseline/"+name+".py" for name in
       ("baseline_bundle", "baseline_intake", "baseline_snapshot", "snapshot_reopen", "reference_request")},
    "reference/reference_report.py": "software/v5/ordinary_baseline/reference_report02.py",
    **{"reference/"+name+".py": "software/v5/ordinary_reference/"+name+".py" for name in
       ("protected_metadata", "reference_store", "reference_closure", "reference_registration",
        "reference_module", "reference_match_worker", "reference_module_worker",
        "reference_authoring", "reference_author_worker")},
    "reference/ReferenceModule.lean": "software/v5/ordinary_reference/ReferenceModule.lean",
    "reference/ReferenceEnvironment.lean": "software/v5/ordinary_reference/ReferenceEnvironment.lean",
    "reference/ReferenceSource.lean": "software/v5/ordinary_reference/ReferenceSource02.lean",
}
CORE_BUILD = LOCAL/"ordinary-baseline-native-build-04"
MATCH_BUILD = LOCAL/"ordinary-reference-native-build-05"
SOURCE_BUILD = LOCAL/"ordinary-reference-source-continuation-01"
PARTIAL_BUILD = LOCAL/"ordinary-reference-source-build-01"
PARTIAL_PROVENANCE = {
    "RESULT.json": "cbe0bdd69220a1793321b291b36b55cee73c9cee9722c50f75835eddd494750d",
    "selection.json": "aa6026c11c205472b8bc800c6af477c720da0f5a119f5dda362258d93af1c0fe",
    "build/BUILD-FAILURE.json": "4c51dd23ff0c59084591b4573d249ffcd5eaf5eed992b0aa58e47c44473a54ab",
    "build/INPUTS.json": "3e8de58e928004d3aa92bad124f430ccf4d437cd1b89e3cbbe15f561fa42ea69",
}
ENVIRONMENT_PIN = {"bytes": 2378696,
    "sha256": "a082feb7bfcf3b28199c4438baafc11e3e00b4ad37af07e3507473e1e452c698"}
CORE_PROVENANCE = {
    "build/BUILD.json": "5811c38b872b094c284579241d9c90d463432ac35dc96d0ae6008b5b7df76213",
    "RESULT.json": "f997200b7abb83d13a0682261858b576d9938031c0368292bc5b5ec2b17632ec",
    "selection.json": "0de88c987ff006d5f7a070996c3d01f7aa34cd7d6f880e180c3e51e47d213ac4",
}
MATCH_PROVENANCE = {
    "build/BUILD.json": "12d2708d8f636dca4c163e2aa733ddfb49d2c437193657d999a5413c593a3111",
    "RESULT.json": "19f5936d91cf501ada9c1bd2d15de318106d799194ded1cc514570c726ec5095",
    "selection.json": "e5cdf8a52f6dace0518a42fc88b461caab5edda9ed0caaf91183cc07af9f8226",
}
SHARED = ("OriginalExpr", "OriginalDecl", "CheckedExtension", "BootstrapSupport", "OrdinaryExport")
PARTS = (".olean", ".olean.private", ".olean.server", ".ir", ".ir.sig")
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def hexid(value):
    need(type(value) is str and len(value) == 64 and
         all(c in "0123456789abcdef" for c in value), "REFERENCE_ASSEMBLY_HEX")
    return value


def encoded(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True,
                      allow_nan=False, separators=(",", ":")).encode("ascii")


def bootstrap(path, name, expected):
    """Only root-selected preserved stdlib support; never run its main function."""
    need(name not in sys.modules and path.is_absolute() and path.is_file(),
         "REFERENCE_ASSEMBLY_BOOTSTRAP")
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(0 < len(raw) <= 2*MIB and hashlib.sha256(raw).hexdigest() == hexid(expected),
         "REFERENCE_ASSEMBLY_BOOTSTRAP_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        exec(compile(raw, str(path), "exec"), module.__dict__)
    except BaseException:
        del sys.modules[name]
        raise
    return module


def helper():
    return bootstrap(ROOT/BUILDER, "_reference_assembly_preserved_builder", BUILDER_SHA)


def inspect_inputs(B, check, source_root, source_provenance):
    """Exact source/provenance inventory only; no new package module is imported."""
    source_root = B.ordinary(source_root, directory=True)
    need(type(source_provenance) is dict and
         set(source_provenance) == {"build/BUILD.json", "RESULT.json", "selection.json"},
         "REFERENCE_ASSEMBLY_SOURCE_PROVENANCE")
    for digest in source_provenance.values():
        hexid(digest)
    pins = {}

    def keep(path, expected=None, maximum=128*MIB):
        path = B.ordinary(path)
        value = B.pin(path, check, maximum)
        need(expected is None or value == expected or value["sha256"] == expected,
             "REFERENCE_ASSEMBLY_INPUT_PIN:"+str(path))
        need(str(path) not in pins or pins[str(path)] == value, "REFERENCE_ASSEMBLY_PIN_CONFLICT")
        pins[str(path)] = value
        return value

    def document(path, digest, *, integer_only=False):
        expected = keep(path, digest, 2*MIB)
        with path.open("rb") as stream:
            raw = stream.read(2*MIB+1)
        need({"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()} == expected,
             "REFERENCE_ASSEMBLY_DOCUMENT_CHANGED")
        if integer_only:
            return loader.owner_json(raw)
        # Exact pinned operational receipts carry fractional wall/CPU times.
        # They are diagnostics, never unpinned owner-policy input documents.
        def pairs(rows):
            value = {}
            for key, item in rows:
                need(key not in value, "REFERENCE_ASSEMBLY_DUPLICATE_KEY")
                value[key] = item
            return value
        def number(text):
            value = float(text)
            need(math.isfinite(value), "REFERENCE_ASSEMBLY_NONFINITE_NUMBER")
            return value
        def reject(_):
            raise ValueError("REFERENCE_ASSEMBLY_JSON_CONSTANT")
        return json.loads(raw, object_pairs_hook=pairs, parse_float=number, parse_constant=reject)

    keep(BASE/"owner.py", BASE_OWNER, 2*MIB)
    keep(BASE/"profile.py", BASE_LOADER, 2*MIB)
    owner = bootstrap(BASE/"owner.py", "_reference_assembly_base_owner", BASE_OWNER)
    loader = owner.bootstrap(BASE, BASE_PROFILE, check)
    old = document(BASE/"PROFILE.json", BASE_PROFILE, integer_only=True)
    receipt = document(BASE/"ASSEMBLY.json", BASE_RECEIPT)
    need(old["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
         old["helper_paths"] == ["authoring/helpers"] and old["author_worker"] == "author_worker.py" and
         len(old["files"]) == 106 and receipt["profile_sha256"] == BASE_PROFILE and
         receipt["status"] == "ASSEMBLED_NOT_ADOPTED" and receipt["files_excluding_profile"] == 134,
         "REFERENCE_ASSEMBLY_BASE_PROFILE")
    manifest = document(BASE/"installation/INSTALLATION.json", old["installation_manifest_sha256"], integer_only=True)
    selected = {}
    for logical, expected in old["files"].items():
        path = BASE.joinpath(*loader.relative(logical).parts)
        selected[logical] = (path, keep(path, expected))
    for directory in ("authoring/helpers", "authoring/py", "authoring/bin", "support", "module"):
        loader.census(BASE/directory, (name[len(directory)+1:] for name in old["files"]
                      if name.startswith(directory+"/")), check)
    runtimes = {"python_runtime": PYTHON, "lean_runtime": LEAN}
    for logical, expected in manifest["files"].items():
        parts = loader.relative(logical).parts
        if parts[0] in runtimes:
            keep(runtimes[parts[0]].joinpath(*parts[1:]), expected)
        else:
            path = BASE/"installation"/logical
            selected["installation/"+logical] = (path, keep(path, expected))
    manifest_path = BASE/"installation/INSTALLATION.json"
    selected["installation/INSTALLATION.json"] = (manifest_path, pins[str(manifest_path)])
    need(len(selected) == 134, "REFERENCE_ASSEMBLY_BASE_CENSUS")
    predecessor = dict(selected)

    def build_documents(directory, provenance, count, schema, status):
        docs = {name: document(directory/name, digest) for name, digest in provenance.items()}
        result, selection, build = docs["RESULT.json"], docs["selection.json"], docs["build/BUILD.json"]
        event = result["result"]
        need(result["schema"] == "DMKN_V5_LOCAL_CHECK_RESULT_V1" and
             result["selection_sha256"] == provenance["selection.json"] and
             selection["schema"] == "DMKN_V5_LOCAL_CHECK_V1" and selection["name"] == directory.name and
             event["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and event["child_exit_code"] == 0 and
             event["direct_child_reaped"] is True and event["job_closed"] is True and
             event["cleanup_errors"] == [] and event["termination_requested"] is False and
             event["final_job"]["active_processes"] == event["final_job"]["terminated_processes"] == 0 and
             build["schema"] == schema and build["status"] == status and
             build["mathematical_acceptance"] is False and len(build["completed_commands"]) == count and
             all(row["exit_code"] == 0 for row in build["completed_commands"]),
             "REFERENCE_ASSEMBLY_RETAINED_BUILD")
        need(set(build["metadata"]) == {"INPUTS.json", "NATIVE-OUTPUTS.json"},
             "REFERENCE_ASSEMBLY_BUILD_METADATA")
        metadata = {name: document(directory/"build"/name, expected["sha256"])
                    for name, expected in build["metadata"].items()}
        need(all(pins[str(directory/"build"/name)] == expected
                 for name, expected in build["metadata"].items()), "REFERENCE_ASSEMBLY_METADATA_PIN")
        return build, metadata["NATIVE-OUTPUTS.json"]

    core, core_outputs = build_documents(CORE_BUILD, CORE_PROVENANCE, 9,
        "DMKN_ORDINARY_BASELINE_NATIVE_BUILD_V1", "BUILT_CANDIDATES_NOT_INSTALLED_OR_ADOPTED")
    match, match_outputs = build_documents(MATCH_BUILD, MATCH_PROVENANCE, 3,
        "DMKN_ORDINARY_REFERENCE_NATIVE_BUILD_V1", "BUILT_CANDIDATE_NOT_INSTALLED_OR_ADOPTED")
    need(core_outputs == core["all_candidate_outputs"] and match_outputs == match["generated_outputs"],
         "REFERENCE_ASSEMBLY_NATIVE_OUTPUT_MAP")
    artifacts = {}
    for name in (*SHARED, "BaselineArtifactCore04"):
        filename = name+".olean"
        path = CORE_BUILD/"build"/("shared" if name in SHARED else "objects")/filename
        expected = core["shared_objects"][filename] if name in SHARED else core_outputs[filename]
        reused = match["reused_support"][filename]
        need(Path(reused["path"]) == path and
             {key: reused[key] for key in ("bytes", "sha256")} == expected,
             "REFERENCE_ASSEMBLY_MATCHER_SHARED_SUPPORT")
        artifacts["reference/helpers/"+filename] = (path, keep(path, expected, 32*MIB))
    for suffix in PARTS:
        filename = "OwnerRebind"+suffix
        logical = "authoring/helpers/"+filename
        artifacts["reference/helpers/"+filename] = predecessor[logical]
    matcher_name = "OrdinaryReferenceBase05.exe"
    matcher_path = MATCH_BUILD/"build/objects"/matcher_name
    matcher_pin = keep(matcher_path, match_outputs[matcher_name], 32*MIB)
    need(matcher_pin["sha256"] == "918aebc5f3f20f305d7c684ff6c1200c164c1503712eaa2e3657fce697bd4aab" and
         match["executable"] == dict(matcher_pin, path=str(matcher_path)),
         "REFERENCE_ASSEMBLY_MATCHER_IDENTITY")
    artifacts["reference/"+matcher_name] = (matcher_path, matcher_pin)
    source_pins = {logical: keep(source_root/relative, maximum=2*MIB)
                   for logical, relative in SOURCES.items()}
    # These three pins are supplied only after root adopts an actual clean build.
    # A filename, planned build or a saved compiler log cannot substitute for it.
    author, author_outputs = build_documents(SOURCE_BUILD, source_provenance, 1,
        "DMKN_ORDINARY_REFERENCE_SOURCE_CONTINUATION_V1",
        "COMPILED_SOURCE_CANDIDATE_REUSING_PARTIAL_ENVIRONMENT_NOT_EXECUTED")
    need(author_outputs == author["generated_outputs"] and
         set(author_outputs) == {"ReferenceSource02.olean"} and
         author["partial_provenance"] == PARTIAL_PROVENANCE,
         "REFERENCE_ASSEMBLY_SOURCE_BUILD_OUTPUTS")
    keep(SOURCE_BUILD/"build/objects/ReferenceSource02.olean", author_outputs["ReferenceSource02.olean"], 32*MIB)
    for name in ("ReferenceEnvironment", "ReferenceSource"):
        logical = "reference/"+name+".lean"
        need(author["source_files"][SOURCES[logical]] == source_pins[logical],
             "REFERENCE_ASSEMBLY_COMPILED_SOURCE_PIN")
    helper_names = {name+".olean" for name in (*SHARED, "BaselineArtifactCore04")} | {
        "OwnerRebind"+suffix for suffix in PARTS}
    need(set(author["reused_support"]) == helper_names | {"ReferenceEnvironment.olean"},
         "REFERENCE_ASSEMBLY_SOURCE_BUILD_HELPER_CENSUS")
    for name in sorted(helper_names):
        expected = artifacts["reference/helpers/"+name][1]
        reused = author["reused_support"][name]
        need(type(reused) is dict and set(reused) == {"path", "bytes", "sha256"} and
             {key: reused[key] for key in ("bytes", "sha256")} == expected,
             "REFERENCE_ASSEMBLY_SOURCE_BUILD_HELPER_COMPATIBILITY")
        path = Path(reused["path"])
        need(path == LOCAL/"ordinary-reference-module-build-01/build/support"/name,
             "REFERENCE_ASSEMBLY_SOURCE_BUILD_HELPER_LOCATION")
        keep(path, expected, 32*MIB)
    partial = {name: document(PARTIAL_BUILD/name, digest) for name, digest in PARTIAL_PROVENANCE.items()}
    event = partial["RESULT.json"]["result"]
    failure = partial["build/BUILD-FAILURE.json"]
    need(partial["RESULT.json"]["selection_sha256"] == PARTIAL_PROVENANCE["selection.json"] and
         partial["selection.json"]["name"] == PARTIAL_BUILD.name and
         event["status"] == "COMMAND_FAILED" and event["child_exit_code"] == 1 and
         event["direct_child_reaped"] is True and event["job_closed"] is True and
         event["cleanup_errors"] == [] and event["termination_requested"] is False and
         event["final_job"]["active_processes"] == event["final_job"]["terminated_processes"] == 0 and
         failure["phase"] == "ReferenceSource-compile" and
         failure["error"] == "REFERENCE_SOURCE_BUILD_COMPILE_FAILED" and
         [(row["phase"], row["exit_code"]) for row in failure["completed_commands"]] ==
         [("ReferenceEnvironment-compile", 0), ("ReferenceSource-compile", 1)],
         "REFERENCE_ASSEMBLY_PRESERVED_PARTIAL_FAILURE")
    environment_path = PARTIAL_BUILD/"build/objects/ReferenceEnvironment.olean"
    environment_source = SOURCES["reference/ReferenceEnvironment.lean"]
    environment_source_pin = source_pins["reference/ReferenceEnvironment.lean"]
    need(author["reused_support"]["ReferenceEnvironment.olean"] ==
         dict(ENVIRONMENT_PIN, path=str(environment_path)) and
         partial["selection.json"]["sources"][environment_source] == environment_source_pin["sha256"] and
         partial["build/INPUTS.json"]["source_snapshots"][environment_source] ==
         dict(environment_source_pin, path=str(PARTIAL_BUILD/"sources"/environment_source)),
         "REFERENCE_ASSEMBLY_PARTIAL_ENVIRONMENT_BINDING")
    keep(PARTIAL_BUILD/"sources"/environment_source, environment_source_pin, 2*MIB)
    keep(PARTIAL_BUILD/"build/source/ReferenceEnvironment.lean", environment_source_pin, 2*MIB)
    artifacts["reference/helpers/ReferenceEnvironment.olean"] = (
        environment_path, keep(environment_path, ENVIRONMENT_PIN, 32*MIB))
    need(len(SOURCES) == 20 and len(artifacts) == 13, "REFERENCE_ASSEMBLY_NEW_PAYLOAD_CENSUS")
    selected.update(artifacts)
    selected.update({logical: (source_root/relative, source_pins[logical])
                     for logical, relative in SOURCES.items()})
    added = sorted(set(selected)-set(predecessor))
    changed = sorted(name for name in set(selected) & set(predecessor)
                     if selected[name][1] != predecessor[name][1])
    unchanged = sorted(name for name in set(selected) & set(predecessor)
                       if selected[name][1] == predecessor[name][1])
    need(len(selected) == 165 and len(added) == 31 and changed == ["owner.py", "profile.py"] and
         len(unchanged) == 132 and len({name.casefold() for name in selected}) == len(selected),
         "REFERENCE_ASSEMBLY_EXACT_DELTA")
    need(sum(pin["bytes"] for _, pin in selected.values()) <= 768*MIB and len(pins) <= 256,
         "REFERENCE_ASSEMBLY_TOTAL_BOUND")
    for logical in selected:
        loader.relative(logical)
    return {"pins": pins, "selected": selected, "predecessor": predecessor,
            "source_pins": source_pins, "artifacts": artifacts, "old": old,
            "implementation_id": receipt["implementation_id"],
            "added": added, "changed": changed, "unchanged": unchanged}


def assemble(args):
    started, cpu_started = time.monotonic(), time.process_time()

    def check():
        need(time.monotonic()-started < 75 and time.process_time()-cpu_started < 45,
             "REFERENCE_ASSEMBLY_ORIGINAL_ALLOWANCE")

    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and
         Path(sys.executable).resolve() == PYTHON/"python.exe", "REFERENCE_ASSEMBLY_CONTEXT")
    expected_map = hexid(args.payload_map_sha256)
    B = helper()
    source_root = B.ordinary(Path(args.source_root), directory=True)
    output = B.ordinary(Path(args.output), directory=True, fresh=True)
    need(output == LOCAL/NAME/"package" and Path(__file__).resolve() == source_root/PREFIX/"assemble.py" and
         not source_root.is_relative_to(output), "REFERENCE_ASSEMBLY_OUTPUT_LOCATION")
    source_provenance = {"build/BUILD.json": hexid(args.source_build_sha256),
                         "RESULT.json": hexid(args.source_result_sha256),
                         "selection.json": hexid(args.source_selection_sha256)}
    inputs = inspect_inputs(B, check, source_root, source_provenance)
    need(hashlib.sha256(encoded(inputs["source_pins"])).hexdigest() == expected_map,
         "REFERENCE_ASSEMBLY_REVIEWED_PAYLOAD_MAP")
    for path in inputs["pins"]:
        selected_path = Path(path)
        need(not selected_path.is_relative_to(output) and not output.is_relative_to(selected_path),
             "REFERENCE_ASSEMBLY_INPUT_OUTPUT_OVERLAP")
    own_pin = B.pin(Path(__file__).resolve(), check, 2*MIB)
    output.mkdir()
    phase = "COPYING"
    try:
        for logical, (source, expected) in sorted(inputs["selected"].items()):
            check()
            destination = output/logical
            pending, parent = [], destination.parent
            while not parent.exists():
                need(parent.is_relative_to(output), "REFERENCE_ASSEMBLY_COPY_DIRECTORY")
                pending.append(parent); parent = parent.parent
            B.ordinary(parent, directory=True)
            for directory in reversed(pending):
                B.ordinary(directory, directory=True, fresh=True).mkdir()
            B.ordinary(source); B.ordinary(destination, fresh=True)
            size, digest = 0, hashlib.sha256()
            with source.open("rb") as incoming, destination.open("xb") as outgoing:
                while block := incoming.read(MIB):
                    check(); size += len(block)
                    need(size <= expected["bytes"], "REFERENCE_ASSEMBLY_COPY_GREW")
                    digest.update(block); outgoing.write(block)
                outgoing.flush(); os.fsync(outgoing.fileno())
            need({"bytes": size, "sha256": digest.hexdigest()} == expected and
                 B.pin(destination, check, 128*MIB) == expected, "REFERENCE_ASSEMBLY_COPY_CHANGED")
        phase = "FINAL_VERIFY"
        for filename, expected in inputs["pins"].items():
            need(B.pin(Path(filename), check, 128*MIB) == expected, "REFERENCE_ASSEMBLY_INPUT_CHANGED")
        for logical, (_, expected) in inputs["selected"].items():
            need(B.pin(output/logical, check, 128*MIB) == expected, "REFERENCE_ASSEMBLY_OUTPUT_CHANGED")
        auxiliary = dict(inputs["old"]["files"])
        auxiliary.update(inputs["source_pins"])
        auxiliary.update({name: pin for name, (_, pin) in inputs["artifacts"].items()})
        need(len(auxiliary) == 137, "REFERENCE_ASSEMBLY_PROFILE_CENSUS")
        descriptor_raw = encoded(dict(inputs["old"], files=auxiliary))
        need(len(descriptor_raw) <= 2*MIB, "REFERENCE_ASSEMBLY_PROFILE_BOUND")
        result = {"schema": "DMKN_ORDINARY_REFERENCE_ASSEMBLY_V1", "status": "ASSEMBLED_NOT_ADOPTED",
            "base_profile_sha256": BASE_PROFILE, "base_receipt_sha256": BASE_RECEIPT,
            "profile_sha256": hashlib.sha256(descriptor_raw).hexdigest(),
            "installation_manifest_sha256": inputs["old"]["installation_manifest_sha256"],
            "implementation_id": inputs["implementation_id"], "files_excluding_profile": 165,
            "copied_bytes": sum(pin["bytes"] for _, pin in inputs["selected"].values()),
            "reviewed_payload_map_sha256": expected_map, "source_payloads": inputs["source_pins"],
            "source_mapping": SOURCES, "retained_artifacts": {name: {"path": str(path), **pin}
                for name, (path, pin) in inputs["artifacts"].items()},
            "core_provenance": CORE_PROVENANCE, "matcher_provenance": MATCH_PROVENANCE,
            "source_provenance": source_provenance,
            "partial_environment_provenance": PARTIAL_PROVENANCE,
            "assembler": own_pin, "added": inputs["added"], "changed": inputs["changed"],
            "unchanged": inputs["unchanged"],
            "wall_seconds_before_commit": time.monotonic()-started,
            "cpu_seconds_before_commit": time.process_time()-cpu_started,
            "claim": "FILE_ONLY_EXACT_SUPPORT_SUCCESSOR_NO_NATIVE_OWNER_OR_MATHEMATICAL_ACCEPTANCE"}
        B.save_json(output/"ASSEMBLY.json", result)
        B.fresh_bytes(output/".PROFILE.pending", descriptor_raw)
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
    for name in ("source-root", "output", "payload-map-sha256", "source-build-sha256",
                 "source-result-sha256", "source-selection-sha256"):
        parser.add_argument("--"+name, required=True)
    print(json.dumps(assemble(parser.parse_args()), sort_keys=True, allow_nan=False), flush=True)
