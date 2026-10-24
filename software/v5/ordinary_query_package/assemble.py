"""File-only combined query/matched-theorem successor of the audited package.

Five source payloads change; two source payloads and five selected compiled query
companions are added. The other 121 payloads and native installation stay exact.
Root selects saved native-query receipts after audit; status is not authority.
No compilation, state, network or mathematical acceptance. PROFILE commits last.
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
PREFIX = "software/v5/ordinary_query_package/"
SOURCES = {
    "profile.py": PREFIX+"profile.py",
    "query.py": PREFIX+"query.py",
    "authoring/py/formal_query.py": "software/v5/ordinary_formal_query/formal_query.py",
    "support/discovery/ordinary_export_adapter.py":
        "software/v5/ordinary_formal_query/discovery/ordinary_export_adapter.py",
    "authoring/py/module_export.py": "software/v5/ordinary_module_matching/module_export.py",
    "module_worker.py": "software/v5/ordinary_module_matching/module_worker.py",
    "module/OrdinaryModule.lean": "software/v5/ordinary_module_matching/OrdinaryModule02.lean",
}
QUERY_SOURCE = "software/v5/ordinary_formal_query/OwnerQueryCommand02.lean"
SUFFIXES = (".olean", ".olean.private", ".olean.server", ".ir", ".ir.sig")
RECEIPTS_SCHEMA = "DMKN_ORDINARY_QUERY_COMPILED_INPUTS_V2"
RECEIPT_NAMES = {"RESULT.json", "selection.json", "native/INPUTS.json", "native/OwnerQueryCommand.lean",
                 "native/NATIVE-QUERY-RESULT.json"} | {
                     "native/OwnerQueryCommand"+suffix for suffix in SUFFIXES}
POSTCHECK_NAMES = {"RESULT.json", "selection.json", "postcheck/REPORT.json",
                   "postcheck/bound-query.json", "postcheck/bindings.json"}
POSTCHECK_SOURCE = "software/v5/ordinary_formal_query/native_query_finish.py"
POSTCHECK_SOURCE_SHA = "40b2b17e0c536c1987199970f5db795ab9d9e1826c95d2075636fcfa46fc0dd3"
BASE_PACKAGE = "experiments/v5-local-checks/ordinary-current-relocated-smoke-01-payload"
BASE_PROFILE_SHA = "192dfee12ac186fbdac0634212b28c1c6324222da2b035f8f295ec764303a68d"
SOURCE_MAP = "software/v5/ordinary_distribution/source-map03.json"
RECIPES = {
    SOURCE_MAP: "ed257d953aef1a7f3a3784f15fece746a6f8e5ee862ecc9ab6e479551fcdf96b",
    "software/v5/ordinary_distribution/build03.py":
        "209918712c9094b0eb3c52b483ecea0ab441131f2751500dbab5c0a0cf9cdb81",
}


def need(condition, code):
    if not condition:
        raise ValueError(code)


def bootstrap(path, name, expected):
    # Source path and selected entrypoint bytes are owner-approved. Remaining
    # path/census checks use the preserved builder and profile helpers below.
    need(name not in sys.modules, "QUERY_ASSEMBLY_PRELOADED")
    need(path.is_absolute() and path.is_file() and path.stat().st_size <= 2*MIB,
         "QUERY_ASSEMBLY_BOOTSTRAP_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() == expected, "QUERY_ASSEMBLY_BOOTSTRAP_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        exec(compile(raw, str(path), "exec"), module.__dict__)
    except BaseException:
        del sys.modules[name]
        raise
    return module


def clean_record(record, exit_code):
    """Check saved process outcome only; no process is started by assembly."""
    expected = "COMMAND_EXITED_ZERO_AND_CLOSED" if exit_code == 0 else "COMMAND_FAILED"
    final, limits = record.get("final_job"), record.get("limits")
    need(record.get("status") == expected and record.get("child_exit_code") == exit_code and
         record.get("direct_child_reaped") is True and record.get("job_closed") is True and
         record.get("cleanup_errors") == [] and record.get("termination_requested") is False and
         type(final) is dict and final.get("active_processes") == 0 and
         final.get("terminated_processes") == 0 and type(final.get("total_processes")) is int and
         final["total_processes"] >= 1 and type(limits) is dict,
         "QUERY_ASSEMBLY_SAVED_PROCESS_CLOSURE")
    for field, value in (("cpu_seconds", final.get("cpu_seconds")),
                         ("wall_seconds", record.get("wall_seconds_through_cleanup"))):
        cap = limits.get(field)
        need(type(value) in (int, float) and math.isfinite(value) and
             type(cap) is int and 0 <= value <= cap, "QUERY_ASSEMBLY_SAVED_RESOURCE_LIMIT")
    for field in ("stdout_bytes", "stderr_bytes"):
        value, cap = record.get("observed_logs", {}).get(field), limits.get(field)
        need(type(value) is int and type(cap) is int and 0 <= value <= cap,
             "QUERY_ASSEMBLY_SAVED_LOG_LIMIT")
    return final["cpu_seconds"]


def assemble(args):
    started, cpu_started = time.monotonic(), time.process_time()
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "QUERY_ASSEMBLY_PYTHON")
    need(type(args.wall_seconds) is int and 10 <= args.wall_seconds <= 600 and
         type(args.cpu_seconds) is int and 5 <= args.cpu_seconds <= 600,
         "QUERY_ASSEMBLY_FINITE_ALLOWANCE")
    deadline = started+args.wall_seconds

    def check():
        need(time.monotonic() < deadline and
             time.process_time()-cpu_started < args.cpu_seconds, "QUERY_ASSEMBLY_ALLOWANCE")

    root, base = Path(args.source_root), Path(args.base_package)
    B = bootstrap(root/BUILDER, "_dmkn_query_preserved_builder", BUILDER_SHA)
    root, base = B.ordinary(root, directory=True), B.ordinary(base, directory=True)
    output = B.ordinary(args.output, directory=True, fresh=True)
    runtimes = {"python_runtime": B.ordinary(args.python_runtime, directory=True),
                "lean_runtime": B.ordinary(args.lean_runtime, directory=True)}
    need(Path(sys.executable).resolve() == runtimes["python_runtime"]/"python.exe",
         "QUERY_ASSEMBLY_RUNNING_PYTHON")
    for path in (base, *runtimes.values()):
        need(not output.is_relative_to(path) and not path.is_relative_to(output),
             "QUERY_ASSEMBLY_OUTPUT_OVERLAP")
    need(not root.is_relative_to(output), "QUERY_ASSEMBLY_SOURCE_OVERLAP")
    need(base == root/BASE_PACKAGE and args.base_profile_sha256 == BASE_PROFILE_SHA,
         "QUERY_ASSEMBLY_AUDITED_BASE")
    recipe_pins = {name: B.pin(root/name, check, 2*MIB) for name in RECIPES}
    need(all(recipe_pins[name]["sha256"] == expected for name, expected in RECIPES.items()),
         "QUERY_ASSEMBLY_RECIPE_PIN")
    with (root/SOURCE_MAP).open("rb") as stream:
        map_raw = stream.read(2*MIB+1)
    need(hashlib.sha256(map_raw).hexdigest() == RECIPES[SOURCE_MAP],
         "QUERY_ASSEMBLY_MAP_CHANGED")
    mapping = json.loads(map_raw)
    check()
    need(B.pin(base/"owner.py", check, 2*MIB)["sha256"] == BASE_OWNER_SHA and
         B.pin(base/"profile.py", check, 2*MIB)["sha256"] == BASE_LOADER_SHA,
         "QUERY_ASSEMBLY_BASE_LOADER_VERSION")
    owner = bootstrap(base/"owner.py", "_dmkn_query_base_owner", BASE_OWNER_SHA)
    loader = owner.bootstrap(base, args.base_profile_sha256, check)
    loaded = loader.load(base, args.base_profile_sha256, runtimes, deadline, check_parent=check)
    old = loaded.descriptor
    source_pins = {logical: B.pin(root/relative, check, 2*MIB)
                   for logical, relative in SOURCES.items()}
    need(all(mapping["copies"].get(logical) == relative and
             source_pins[logical] == mapping["sources"][relative]
             for logical, relative in SOURCES.items()), "QUERY_ASSEMBLY_SELECTED_HELPER")
    own_pin = B.pin(root/PREFIX/"assemble.py", check, 2*MIB)
    need(B.pin(Path(__file__).absolute(), check, 2*MIB) == own_pin,
         "QUERY_ASSEMBLY_RUNNING_SOURCE")
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

    # The owner-selected receipt set is an artifact selection, not independent
    # audit authority. Root must inspect the saved outcome before selecting it.
    receipt_path = B.ordinary(args.query_receipts)
    receipt_pin = B.pin(receipt_path, check, 2*MIB)
    need(receipt_pin["sha256"] == loader.hexid(args.query_receipts_sha256),
         "QUERY_ASSEMBLY_RECEIPT_PIN")
    with receipt_path.open("rb") as stream:
        receipt_raw = stream.read(2*MIB+1)
    need(hashlib.sha256(receipt_raw).hexdigest() == args.query_receipts_sha256,
         "QUERY_ASSEMBLY_RECEIPT_CHANGED")
    receipt = loader.owner_json(receipt_raw)
    need(set(receipt) == {"schema", "run", "postcheck_run", "base_profile_sha256",
                         "source_sha256", "files", "postcheck_files"} and
         receipt["schema"] == RECEIPTS_SCHEMA and receipt["base_profile_sha256"] == BASE_PROFILE_SHA and
         receipt["source_sha256"] == mapping["sources"][QUERY_SOURCE]["sha256"] and
         type(receipt["files"]) is dict and set(receipt["files"]) == RECEIPT_NAMES and
         type(receipt["postcheck_files"]) is dict and set(receipt["postcheck_files"]) == POSTCHECK_NAMES,
         "QUERY_ASSEMBLY_RECEIPT_SCHEMA")
    query_run = B.ordinary(receipt["run"], directory=True)
    postcheck_run = B.ordinary(receipt["postcheck_run"], directory=True)
    need(query_run.is_relative_to(root/"experiments/v5-local-checks") and
         postcheck_run.is_relative_to(root/"experiments/v5-local-checks") and
         all(not a.is_relative_to(b) and not b.is_relative_to(a)
             for a, b in ((output, query_run), (output, postcheck_run), (query_run, postcheck_run))),
         "QUERY_ASSEMBLY_QUERY_RUN")
    receipt_files = {}
    for name, expected in receipt["files"].items():
        path = query_run/loader.relative(name)
        need(B.pin(path, check, 128*MIB) == expected, "QUERY_ASSEMBLY_QUERY_RECEIPT_FILE")
        receipt_files[name] = (path, expected)
    postcheck_files = {}
    for name, expected in receipt["postcheck_files"].items():
        path = postcheck_run/loader.relative(name)
        need(B.pin(path, check, 2*MIB) == expected, "QUERY_ASSEMBLY_POSTCHECK_RECEIPT_FILE")
        postcheck_files[name] = (path, expected)
    def operational_json(name, files=receipt_files):
        path, expected = files[name]
        need(expected["bytes"] <= 2*MIB, "QUERY_ASSEMBLY_OPERATIONAL_JSON_BOUND")
        with path.open("rb") as stream:
            raw = stream.read(2*MIB+1)
        need(len(raw) == expected["bytes"] and hashlib.sha256(raw).hexdigest() == expected["sha256"],
             "QUERY_ASSEMBLY_OPERATIONAL_JSON_CHANGED")
        # Saved supervision contains fractional timings, unlike inert math JSON.
        return json.loads(raw)
    outer, selection, inputs, native = [operational_json(name) for name in
        ("RESULT.json", "selection.json", "native/INPUTS.json", "native/NATIVE-QUERY-RESULT.json")]
    post_outer, post_selection, post = [operational_json(name, postcheck_files) for name in
        ("RESULT.json", "selection.json", "postcheck/REPORT.json")]
    selected_source = query_run/"sources"/QUERY_SOURCE
    post_source = postcheck_run/"sources"/POSTCHECK_SOURCE
    # The original harness failed AFTER two successful native calls. Never
    # rewrite that whole-run failure or treat the postcheck as another compile.
    clean_record(outer["result"], 1)
    clean_record(post_outer["result"], 0)
    need(outer["schema"] == post_outer["schema"] == "DMKN_V5_LOCAL_CHECK_RESULT_V1" and
         outer["selection_sha256"] == receipt["files"]["selection.json"]["sha256"] and
         post_outer["selection_sha256"] == receipt["postcheck_files"]["selection.json"]["sha256"] and
         native["status"] == "FAILED" and native["error_type"] == "EvidenceError" and
         native["error"] == "JSON_LEXICAL_TOKEN" and native["acceptance"] is False and
         inputs["profile_sha256"] == BASE_PROFILE_SHA and
         selection["sources"][QUERY_SOURCE] == receipt["source_sha256"] and
         receipt["files"]["native/OwnerQueryCommand.lean"] == mapping["sources"][QUERY_SOURCE] and
         inputs["pins"].get(str(query_run/"native/OwnerQueryCommand.lean")) == mapping["sources"][QUERY_SOURCE] and
         B.pin(selected_source, check, 2*MIB) == mapping["sources"][QUERY_SOURCE],
         "QUERY_ASSEMBLY_QUERY_SOURCE_AND_OUTCOME")
    call_names = ["OwnerQueryCommand.lean", "QueryNativeFixture.lean"]
    need(type(native["calls"]) is list and len(native["calls"]) == 2 and
         [call["file"] for call in native["calls"]] == call_names,
         "QUERY_ASSEMBLY_NATIVE_CALL_CENSUS")
    for call in native["calls"]:
        record = call["supervision"]
        actual_cpu = clean_record(record, 0)
        need(call["cpu_complete"] is True and call["charged_cpu_seconds"] == actual_cpu and
             record["cwd"] == str(query_run/"native") and
             record["observed_logs"] == {"stdout_bytes": 0, "stderr_bytes": 0},
             "QUERY_ASSEMBLY_NATIVE_CALL_SUCCESS")
    need(post["schema"] == "DMKN_ORDINARY_QUERY_SAVED_POSTCHECK_V1" and
         post["status"] == "PASS_SAVED_NATIVE_QUERY_POSTCHECK" and
         post["original_run_status"] == "FAILED" and
         post["original_failure"] == "JSON_LEXICAL_TOKEN_FIXED_INVENTORY_NOT_INERT_ENVELOPE" and
         post["original_run"] == str(query_run) and
         post["original_selection_sha256"] == receipt["files"]["selection.json"]["sha256"] and
         post["original_result_pin"] == receipt["files"]["RESULT.json"] and
         post["original_native_result_pin"] == receipt["files"]["native/NATIVE-QUERY-RESULT.json"] and
         post["source_command_pin"] == mapping["sources"][QUERY_SOURCE] and
         post["profile_sha256"] == BASE_PROFILE_SHA and post["successful_native_calls"] == call_names and
         post["acceptance"] is False and type(post["native_calls_performed"]) is int and
         post["native_calls_performed"] == 0 and
         post_selection["sources"][POSTCHECK_SOURCE] == POSTCHECK_SOURCE_SHA and
         B.pin(post_source, check, 2*MIB)["sha256"] == POSTCHECK_SOURCE_SHA and
         post["bound_query_pin"] == receipt["postcheck_files"]["postcheck/bound-query.json"] and
         post["bindings_pin"] == receipt["postcheck_files"]["postcheck/bindings.json"] and
         type(post["pins"]) is dict and
         all(post["pins"].get(str(path)) == expected for path, expected in receipt_files.values()),
         "QUERY_ASSEMBLY_SEPARATE_POSTCHECK_BINDING")
    query_parser_source = query_run/"sources"/SOURCES["authoring/py/formal_query.py"]
    need(post["pins"].get(str(selected_source)) == mapping["sources"][QUERY_SOURCE] and
         post["pins"].get(str(query_parser_source)) == source_pins["authoring/py/formal_query.py"] and
         post["pins"].get(str(base/"PROFILE.json")) == B.pin(base/"PROFILE.json", check, 2*MIB),
         "QUERY_ASSEMBLY_POSTCHECK_SOURCE_AND_PROFILE")
    # Only OriginalExpr's five already-approved companions are needed by this
    # command. Bind the exact helper bytes actually selected by the native test.
    for suffix in SUFFIXES:
        helper = base/"authoring/helpers"/("OriginalExpr"+suffix)
        expected = old["files"]["authoring/helpers/OriginalExpr"+suffix]
        need(inputs["pins"].get(str(helper)) == expected and
             post["pins"].get(str(helper)) == expected and
             B.pin(helper, check, 128*MIB) == expected,
             "QUERY_ASSEMBLY_QUERY_HELPER_BINDING")
    generated = {}
    need(set(post["compiled_command_artifacts"]) == set(SUFFIXES),
         "QUERY_ASSEMBLY_QUERY_COMPANION_CENSUS")
    for suffix in SUFFIXES:
        name = "native/OwnerQueryCommand"+suffix
        path, expected = receipt_files[name]
        need(post["compiled_command_artifacts"][suffix] == expected and expected["bytes"] > 0,
             "QUERY_ASSEMBLY_QUERY_COMPANION_PIN")
        generated["authoring/helpers/OwnerQueryCommand"+suffix] = (path, expected)
    loader.census(base, (*original, "PROFILE.json"), check)
    for logical, relative in SOURCES.items():
        need(logical not in selected or selected[logical][1] != source_pins[logical],
             "QUERY_ASSEMBLY_REAL_CHANGE")
        selected[logical] = (root/relative, source_pins[logical])
    need(not set(generated) & set(selected), "QUERY_ASSEMBLY_GENERATED_COLLISION")
    selected.update(generated)
    expected_names = set(mapping["copies"]) | {
        "installation/INSTALLATION.json", mapping["extractor_output"]}
    expected_names.update("installation/lean-lib/"+row["module"]+".olean"
                          for row in mapping["lanes"]["receiver"])
    expected_names.update("authoring/helpers/"+row["module"]+suffix
        for row in (*mapping["lanes"]["authoring"], *mapping["lanes"]["query"])
        for suffix in mapping["authoring_suffixes"])
    need(set(selected) == expected_names and len(selected) == 133 and len(old["files"]) == 98 and
         len(set(selected)-set(original)) == 7 and set(original) <= set(selected) and
         sum(selected[name][1] != original[name][1] for name in original) == 5 and
         all(selected[name][1] == mapping["sources"][source]
             for name, source in mapping["copies"].items()), "QUERY_ASSEMBLY_EXACT_DELTA")
    need(len(selected) <= 512 and len({name.casefold() for name in selected}) == len(selected),
         "QUERY_ASSEMBLY_CENSUS")
    need(sum(pin["bytes"] for _, pin in selected.values()) <= 768*MIB,
         "QUERY_ASSEMBLY_TOTAL_BOUND")
    for name, (source, expected) in selected.items():
        loader.relative(name)
        need(not source.is_relative_to(output), "QUERY_ASSEMBLY_SELECTED_OVERLAP")
        need(B.pin(source, check, 128*MIB) == expected, "QUERY_ASSEMBLY_INPUT_PIN")
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
                need(parent.is_relative_to(output), "QUERY_ASSEMBLY_DIRECTORY")
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
                    need(count <= expected["bytes"], "QUERY_ASSEMBLY_SOURCE_GREW")
                    digest.update(block); out.write(block)
                out.flush(); os.fsync(out.fileno())
            need(count == expected["bytes"] and digest.hexdigest() == expected["sha256"],
                 "QUERY_ASSEMBLY_SOURCE_CHANGED")
            need(B.pin(target, check, 128*MIB) == expected, "QUERY_ASSEMBLY_COPY_CHANGED")
        phase = "FINAL_VERIFY"
        for name, (source, expected) in selected.items():
            need(B.pin(source, check, 128*MIB) == expected and
                 B.pin(package/name, check, 128*MIB) == expected, "QUERY_ASSEMBLY_FINAL_PIN")
        for name, (source, expected) in original.items():
            need(B.pin(source, check, 128*MIB) == expected, "QUERY_ASSEMBLY_BASE_CHANGED")
        for name, expected in installed["files"].items():
            parts = loader.relative(name).parts
            if parts[0] in runtimes:
                need(B.pin(runtimes[parts[0]].joinpath(*parts[1:]), check, 128*MIB) == expected,
                     "QUERY_ASSEMBLY_RUNTIME_CHANGED")
        need(B.pin(receipt_path, check, 2*MIB) == receipt_pin and
             B.pin(selected_source, check, 2*MIB) == mapping["sources"][QUERY_SOURCE] and
             B.pin(post_source, check, 2*MIB)["sha256"] == POSTCHECK_SOURCE_SHA,
             "QUERY_ASSEMBLY_RECEIPT_OR_QUERY_SOURCE_CHANGED")
        for path, expected in receipt_files.values():
            need(B.pin(path, check, 128*MIB) == expected, "QUERY_ASSEMBLY_QUERY_RECEIPT_CHANGED")
        for path, expected in postcheck_files.values():
            need(B.pin(path, check, 2*MIB) == expected, "QUERY_ASSEMBLY_POSTCHECK_RECEIPT_CHANGED")
        for name, expected in recipe_pins.items():
            need(B.pin(root/name, check, 2*MIB) == expected, "QUERY_ASSEMBLY_RECIPE_CHANGED")
        need(B.pin(root/PREFIX/"assemble.py", check, 2*MIB) == own_pin and
             B.pin(Path(__file__).absolute(), check, 2*MIB) == own_pin and
             B.pin(root/BUILDER, check, 2*MIB)["sha256"] == BUILDER_SHA and
             B.pin(base/"PROFILE.json", check, 2*MIB)["sha256"] == BASE_PROFILE_SHA,
             "QUERY_ASSEMBLY_ENTRYPOINT_OR_BASE_CHANGED")
        loader.census(base, (*original, "PROFILE.json"), check)
        loader.census(package, selected, check)
        auxiliary = dict(old["files"])
        auxiliary.update(source_pins)
        auxiliary.update({name: pin for name, (_, pin) in generated.items()})
        descriptor = dict(old, files=auxiliary)
        raw = loaded.A.E.canonical_json(descriptor)
        need(len(raw) <= 2*MIB, "QUERY_ASSEMBLY_PROFILE_BOUND")
        need(set(old["files"]) < set(auxiliary) and len(auxiliary) == 105,
             "QUERY_ASSEMBLY_AUXILIARY_DELTA")
        result = {"status": "ASSEMBLED_NOT_ADOPTED", "package": str(package), "base_profile_sha256": args.base_profile_sha256,
            "profile_sha256": hashlib.sha256(raw).hexdigest(),
            "installation_manifest_sha256": old["installation_manifest_sha256"],
            "implementation_id": loaded.installation.implementation_id,
            "files_excluding_profile": len(selected),
            "copied_bytes": sum(pin["bytes"] for _, pin in selected.values()),
            "changed_or_added": dict(source_pins, **{name: pin for name, (_, pin) in generated.items()}),
            "unchanged_payloads": 121, "assembler": own_pin,
            "query_receipts": {"path": str(receipt_path), **receipt_pin},
            "original_native_run_status": "FAILED",
            "reused_native_calls": call_names,
            "postcheck_status": post["status"], "postcheck_run": str(postcheck_run),
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
                 "lean-runtime", "output", "query-receipts", "query-receipts-sha256"):
        parser.add_argument("--"+name, required=True)
    for name in ("wall-seconds", "cpu-seconds"):
        parser.add_argument("--"+name, required=True, type=int)
    print(json.dumps(assemble(parser.parse_args()), sort_keys=True, allow_nan=False))
