"""Assemble the adopted three-crate support RC guest; no compile, guest run or proof.

Reuse the frozen assembler's pure utilities and retained binary/kernel. The
independently adopted new build owns old provenance; do not traverse old Cargo
failures or rehash compiler/dependency libraries here. Inner success still needs
the owner's clean outer-supervision adoption.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
RUN = HERE / "restricted-support-guest-build-01"
HELPER_SHA = "220f54cf19fb9bebfd61674df332113a9e0f98bbd003bcecb5a268738048ca01"
BUILD_PASS = "PASS_RC_SUPPORT_GUEST_THREE_CRATE_COMPILES_ONLY"
ASSEMBLY_PASS = "PASS_NEW_AGGREGATE_IMAGE_ASSEMBLY_ONLY"
PROJECTS = ["dmkn_rc_relation", "dmkn_aggregate_relation", "dmkn-aggregate-claim-guest"]
LABELS = ["rc-core", "aggregate", "guest"]
ADAPTERS = {"software/v5/restricted_support_guest/build.py", "software/v5/restricted_support_guest/recipes.py"}
MIB = 1024**2


def main():
    if not (os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated
            and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize):
        raise ValueError("CANONICAL_ISOLATED_OWNER_INVOCATION")
    invoked = Path(__file__).resolve(strict=True)
    relative = invoked.relative_to(HERE).parts
    if not (len(relative) == 6 and relative[1:] == (
            "sources", "software", "v5", "restricted_support_guest", "assemble.py")
            and re.fullmatch(r"[a-z0-9][a-z0-9-]{0,95}", relative[0])):
        raise ValueError("EXACT_OWNER_SOURCE_SNAPSHOT")
    helper_path = invoked.parents[1] / "bounded_parse_guest/assemble.py"
    if helper_path.stat().st_size != 17931 or hashlib.sha256(helper_path.read_bytes()).hexdigest() != HELPER_SHA:
        raise ValueError("FROZEN_ASSEMBLY_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("typed_frozen_assembly_helpers", helper_path)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    need, pin, ordinary, save = helper.need, helper.pin, helper.ordinary, helper.save
    parser = argparse.ArgumentParser()
    parser.add_argument("--guest-result", required=True)
    parser.add_argument("--guest-result-sha256", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    need(re.fullmatch(r"[0-9a-f]{64}", args.guest_result_sha256), "ADOPTED_RESULT_DIGEST")
    result_path, output = Path(args.guest_result), Path(args.output)
    need(result_path == RUN / "RESULT.json", "EXACT_THREE_CRATE_RESULT")
    need(output.parent == HERE / relative[0] and output.name == "assembly", "SELECTED_ASSEMBLY_OUTPUT")
    ordinary(output, fresh=True)
    inputs = {}

    def remember(path, maximum=64*MIB, expected=None, allow_empty=False):
        observed = pin(path, maximum, allow_empty=allow_empty)
        need(expected is None or observed == expected, "EXACT_INPUT_PIN:" + str(path))
        value = (observed, maximum, allow_empty)
        need(path not in inputs or inputs[path] == value, "CONSISTENT_INPUT_PIN")
        inputs[path] = value
        return observed

    def record(path, expected_hash=None):
        observed = remember(path, 2*MIB)
        need(expected_hash is None or observed["sha256"] == expected_hash, "EXACT_RECORD_DIGEST")
        with path.open("rb") as stream:
            raw = stream.read(2*MIB + 1)
        need(len(raw) == observed["bytes"] and hashlib.sha256(raw).hexdigest() == observed["sha256"],
             "RECORD_CHANGED_DURING_READ")
        value = json.loads(raw, object_pairs_hook=helper.unique_object)
        need(type(value) is dict, "JSON_OBJECT_RECORD")
        return value

    failure_marker = RUN / "FINALIZATION-FAILED.json"

    def no_failure():
        need(not failure_marker.exists() and not failure_marker.is_symlink()
             and not failure_marker.is_junction(), "NO_OVERRIDING_BUILD_FINALIZATION_FAILURE")

    no_failure()
    remember(helper_path, 2*MIB, {"bytes":17931, "sha256":HELPER_SHA})
    built = record(result_path, args.guest_result_sha256)
    need(built["schema"] == "DMKN_V5_RC_SUPPORT_GUEST_THREE_CRATE_BUILD_RESULT_V1"
         and built["status"] == BUILD_PASS and built["job"]["active_processes"] == 0
         and built["job"]["terminated_processes"] == 0
         and type(built["compiler_calls"]) is int and built["compiler_calls"] == 3
         and type(built["checker_compiles"]) is int and built["checker_compiles"] == 0
         and type(built["module_compiles"]) is int and built["module_compiles"] == 0
         and all(type(built[name]) is int and built[name] == 0 for name in
             ("cargo_calls", "graph_commands", "dependency_compiles", "guest_calls", "proof_calls",
              "image_assembly_calls", "network_calls")), "ADOPTED_THREE_CRATE_BUILD_ONLY")
    need(record(HERE / (RUN.name + "-attempt.json")) ==
         {"status":BUILD_PASS, "result_sha256":args.guest_result_sha256}, "EXACT_TERMINAL_ATTEMPT")
    selected = record(RUN / "selection.json", built["selection_sha256"])
    need(set(selected) == {"schema", "name", "adapters", "production_sources", "native_adoption",
                          "limits", "authorizes_three_compiles_and_retained_artifact_adoption"}
         and selected["schema"] == "DMKN_V5_RC_SUPPORT_GUEST_THREE_CRATE_BUILD_V1"
         and selected["name"] == RUN.name
         and selected["authorizes_three_compiles_and_retained_artifact_adoption"] is True
         and set(selected["adapters"]) == ADAPTERS and selected["limits"] == built["limits"],
         "EXACT_ADOPTED_BUILD_SELECTION")
    need(built["native_adoption"] == selected["native_adoption"], "EXACT_BUILD_NATIVE_ADOPTION")
    limits = {"worker_cpu_seconds":240, "worker_wall_seconds":300, "memory_mib":4096,
        "active_processes":6, "ordinary_controller_cpu_seconds":40, "controller_cpu_seconds":60,
        "total_wall_seconds":420, "fresh_output_bytes":256*MIB,
        "fresh_output_entries":2048, "command_log_bytes":8*MIB}
    need(selected["limits"] == limits and 0 <= built["job"]["cpu_seconds"] <= 240
         and 0 <= built["controller_cpu_seconds"] <= 60 and 0 <= built["wall_seconds"] <= 420,
         "CLOSED_BUILD_WITHIN_UNCHANGED_ENVELOPE")
    source_map = record(RUN / "SOURCE-MAP.json")
    input_map = record(RUN / "INPUT-MAP.json")
    production = selected["production_sources"]
    need(type(production) is dict and len(production) == 12
         and set(production) == {
             "software/v5/restricted_support/" + name for name in ("lib.rs", "syntax.rs", "typing.rs")
         } | {"software/v5/restricted_composition/" + name for name in (
             "foundation02.rs", "relation.rs", "aggregate_lib.rs", "aggregate_relation.rs", "census.rs", "wire.rs")}
         | {"software/v5/aggregate_claims/header.rs", "software/v5/aggregate_claims/membership.rs",
            "software/v5/aggregate/main.rs"}, "EXACT_12_SOURCE_CLOSURE")
    need(built["selected_source_files"] == built["production_source_closure_files"] == 12,
         "ACTUAL_TWELVE_SOURCE_BUILD")
    need(source_map == {"source_snapshot":str(RUN / "project"), "project":production,
                        "compiler_read_sources":production, "adapters":selected["adapters"]}
         and built["source_snapshot"] == str(RUN / "project"), "EXACT_REACHABLE_PRODUCTION_MAP")
    need(set(input_map) == {"inputs", "existing_dependency_view", "existing_dependency_files",
                           "copied_module_artifacts", "existing_nanoda_view", "existing_nanoda_files"}
         and input_map["existing_dependency_view"] == str(HERE / "typed-guest-build-01/retained")
         and len(input_map["existing_dependency_files"]) == 236
         and len(input_map["copied_module_artifacts"]) == 2
         and input_map["existing_nanoda_view"] == str(HERE / "restricted-guest-build-03/retained/projects")
         and len(input_map["existing_nanoda_files"]) == 2, "EXACT_RECORDED_DEPENDENCY_VIEW")
    retained = {"path":str(HERE / "restricted-guest-build-03/RESULT.json"),
                "sha256":"44f808cdd24c2707d114675bf77a4126a805865eaae825666db0c9403e354273"}
    need(built["retained_module_adoption"] == built["retained_nanoda_adoption"] == retained,
         "ACTUAL_SUCCESSFUL_RETAINED_MODULE_AND_NANODA")
    module_artifacts = {
        "libdmkn_module_relation.rlib": {"bytes":2349740,
            "sha256":"d70c585aead8afe869ce96eadde46ef7d8f31efe1bdbb717955adcff8efa4f76"},
        "libdmkn_module_relation.rmeta": {"bytes":830551,
            "sha256":"6b879d8fff8c09c858e0ff4f51a442a3cae33aa3551c062cf55479025ef77828"}}
    need(input_map["copied_module_artifacts"] == module_artifacts, "EXACT_COPIED_MODULE_PAIR")
    for name, expected in module_artifacts.items():
        remember(RUN / "retained/modules" / name, 8*MIB, expected)
    need(set(selected["native_adoption"]) == {"build", "controls_outer", "controls_inner"},
         "EXACT_NATIVE_ADOPTION_ROLES")
    for role, native in selected["native_adoption"].items():
        need(set(native) == {"path", "bytes", "sha256"}, "NATIVE_ADOPTION_PIN")
        path = Path(native["path"])
        expected_path = {
            "build": HERE / "restricted-support-build-01/RESULT.json",
            "controls_outer": HERE / "restricted-support-controls-01/RESULT.json",
            "controls_inner": HERE / "restricted-support-controls-01/command/stdout.txt",
        }[role]
        need(path == expected_path, "EXACT_NATIVE_ADOPTION_PATH")
        remember(path, 2*MIB, {key:native[key] for key in ("bytes", "sha256")})
        need(input_map["inputs"].get(str(path)) == {key:native[key] for key in ("bytes", "sha256")},
             "NATIVE_ADOPTION_BUILD_BINDING")
    for base, entries in ((RUN / "project", production), (ROOT, selected["adapters"])):
        for name, expected in entries.items():
            rel = Path(name)
            need(not rel.is_absolute() and ".." not in rel.parts, "SOURCE_RELATIVE_PATH")
            remember(base / rel, 2*MIB, expected)
            if base == ROOT:
                need(input_map["inputs"].get(str(base / rel)) == expected, "USED_BUILD_ADAPTER_BINDING")
    recipes = record(RUN / "RECIPES.json")
    need(recipes["schema"] == "DMKN_V5_RC_SUPPORT_GUEST_THREE_CRATE_RECIPES_V1"
         and recipes["basis"] == "RECONSTRUCTED_EQUIVALENT_PROFILE_NOT_CAPTURED_CARGO_ARGV"
         and type(recipes["recipes"]) is list and len(recipes["recipes"]) == 3
         and [row["name"] for row in recipes["recipes"]] == PROJECTS,
         "THREE_RECORDED_NEW_CRATE_RECIPES")
    commands = built["commands"]
    need(type(commands) is list and len(commands) == 3
         and [row["label"] for row in commands] == LABELS, "EXACT_COMMAND_ORDER")
    for label, command, recipe in zip(LABELS, commands, recipes["recipes"]):
        need(command["status"] == "COMMAND_COMPLETED" and command["exit_code"] == 0
             and type(command["pid"]) is int and command["pid"] > 0
             and command["cleanup_errors"] == [] and command["job_after"]["active_processes"] == 0
             and command["job_after"]["terminated_processes"] == 0
             and command["argv"] == recipe["argv"], "SUCCESSFUL_CLOSED_MATCHED_COMMAND")
        directory = RUN / "commands" / label
        need(record(directory / "command.json") == command, "EXACT_ACTUAL_COMMAND_RECORD")
        need(type(command["logs"]) is list and len(command["logs"]) == 2
             and {row["path"] for row in command["logs"]} ==
                 {str(directory / "stdout.txt"), str(directory / "stderr.txt")}, "EXACT_BUILD_LOG_PATHS")
        for log in command["logs"]:
            need(set(log) == {"path", "bytes", "sha256"}, "BUILD_LOG_PIN_SHAPE")
            remember(Path(log["path"]), 8*MIB,
                     {key:log[key] for key in ("bytes", "sha256")}, allow_empty=True)
    expected_outputs = {"dmkn-aggregate-claim-guest"}
    expected_outputs.update("lib" + crate + ext for crate in PROJECTS[:2] for ext in (".rlib", ".rmeta"))
    need(type(built["outputs"]) is dict and set(built["outputs"]) == expected_outputs, "EXACT_FIVE_BUILD_OUTPUTS")
    for name, item in built["outputs"].items():
        path = RUN / "outputs" / name
        need(set(item) == {"path", "bytes", "sha256"} and item["path"] == str(path), "EXACT_BUILD_OUTPUT_PATH")
        remember(path, 64*MIB, {key:item[key] for key in ("bytes", "sha256")})
    for index, recipe in enumerate(recipes["recipes"]):
        name = PROJECTS[index]
        expected = RUN / "outputs" / (name if index == 2 else "lib" + name + ".rlib")
        metadata = None if index == 2 else str(RUN / "outputs" / ("lib" + name + ".rmeta"))
        need(recipe["output"] == str(expected) and recipe["metadata_output"] == metadata,
             "EXACT_RECIPE_OUTPUTS")
        argv = recipe["argv"]
        source_relative = ("restricted_support/lib.rs", "restricted_composition/aggregate_lib.rs",
                           "aggregate/main.rs")[index]
        source_path = RUN / "project/software/v5" / source_relative
        searches = [argv[i + 1] for i, word in enumerate(argv) if word == "-L"]
        externs = [argv[i + 1] for i, word in enumerate(argv) if word == "--extern"]
        project_externs = {word.split("=", 1)[0]:word.split("=", 1)[1]
                           for word in externs if word.startswith("dmkn_")}
        project_expected = {"dmkn_module_relation":str(RUN / "retained/modules/libdmkn_module_relation.rlib")}
        if index == 1:
            project_expected["dmkn_rc_relation"] = str(RUN / "outputs/libdmkn_rc_relation.rlib")
        if index == 2:
            project_expected["dmkn_aggregate_relation"] = str(RUN / "outputs/libdmkn_aggregate_relation.rlib")
        identity = "dmkn_v5_rc_support_guest01_" + name.replace("-", "_")
        need(recipe["source"] == str(source_path) and argv.count(str(source_path)) == 1
             and recipe["fresh_metadata"] == identity and argv.count("metadata=" + identity) == 1
             and searches == ["dependency=" + str(path) for path in (
                 RUN / "outputs", HERE / "typed-guest-build-01/retained/libraries",
                 HERE / "typed-guest-build-01/retained/macros",
                 HERE / "restricted-guest-build-03/retained/projects", RUN / "retained/modules")]
             and len(externs) == (10 if index == 0 else 11) and project_externs == project_expected,
             "ACTUAL_SOURCE_AND_NEW_CORE_LINK_BINDING")
    artifact = record(RUN / "ARTIFACT.json")
    need(artifact == built["artifact"] and set(artifact) == {"user_elf", "elf_headers", "link_map"}, "EXACT_ARTIFACT_RECORD")
    user, link_map = RUN / "outputs/dmkn-aggregate-claim-guest", RUN / "guest-link.map"
    need(artifact["user_elf"] == built["outputs"][user.name]
         and set(artifact["link_map"]) == {"path", "bytes", "sha256"}
         and artifact["link_map"]["path"] == str(link_map), "EXACT_ELF_AND_MAP")
    remember(link_map, 32*MIB, {key:artifact["link_map"][key] for key in ("bytes", "sha256")})
    driver = record(helper.DRIVER_HOME / "RESULT.json", helper.DRIVER_RESULT_SHA)
    need(driver["status"] == "PASS_DRIVER_COMPILE_ONLY", "ADOPTED_RETAINED_ASSEMBLER")
    executable = Path(driver["executable"]["path"])
    need(executable.parent == helper.DRIVER_HOME, "EXACT_ASSEMBLER_HOME")
    remember(executable, 128*MIB, {key:driver["executable"][key] for key in ("bytes", "sha256")})
    remember(helper.KERNEL, 64*MIB, helper.KERNEL_PIN)

    def rebind():
        no_failure()
        for path, (expected, maximum, empty) in inputs.items():
            need(pin(path, maximum, allow_empty=empty) == expected, "SELECTED_INPUT_CHANGED:" + str(path))
        no_failure()

    rebind()
    output.mkdir()
    image = output / "aggregate_image.bin"
    argv = [str(executable), "assemble", str(user), str(helper.KERNEL), str(image)]
    save(output / "COMMAND.json", {"argv":argv, "cwd":str(ROOT), "timeout_seconds":60,
        "selected_inputs":[{"path":str(path), **value[0]} for path, value in inputs.items()],
        "guest_result_sha256":args.guest_result_sha256, "absent_failure_marker":str(failure_marker),
        "authority":"ASSEMBLY_ONLY_NOT_ADMISSION"})
    report = {"schema":"DMKN_V5_RC_SUPPORT_GUEST_IMAGE_ASSEMBLY_RESULT_V1", "status":"FAIL_RC_SUPPORT_GUEST_IMAGE_ASSEMBLY",
        "assembler_calls":0, "guest_executions":0, "proof_calls":0, "mathematical_admission":False,
        "guest_build_result":{"path":str(result_path), **inputs[result_path][0]},
        "artifact_record":{"path":str(RUN / "ARTIFACT.json"), **inputs[RUN / "ARTIFACT.json"][0]},
        "selection_sha256":built["selection_sha256"],
        "authority":"INNER_ASSEMBLY_ONLY_OWNER_MUST_ADOPT_CLEAN_OUTER_COMPLETION"}
    try:
        rebind()
        environment = {key:value for key, value in os.environ.items() if not key.upper().startswith("RISC0_")}
        report["assembler_calls"] = 1
        with (output / "stdout.txt").open("xb") as stdout, (output / "stderr.txt").open("xb") as stderr:
            process = subprocess.run(argv, cwd=ROOT, env=environment, stdin=subprocess.DEVNULL,
                stdout=stdout, stderr=stderr, timeout=60, check=False, creationflags=subprocess.CREATE_NO_WINDOW)
        report["exit_code"] = process.returncode
        stdout_pin = pin(output / "stdout.txt", 65536)
        stderr_pin = pin(output / "stderr.txt", 65536, allow_empty=True)
        need(process.returncode == 0 and stderr_pin["bytes"] == 0, "ASSEMBLER_ZERO_WITHOUT_DIAGNOSTICS")
        with (output / "stdout.txt").open("rb") as stream:
            raw = stream.read(65537)
        need(len(raw) == stdout_pin["bytes"] and hashlib.sha256(raw).hexdigest() == stdout_pin["sha256"],
             "ASSEMBLER_STDOUT_CHANGED")
        match = re.fullmatch(rb"COMBINED_IMAGE image_id=([0-9a-f]{64}) bytes=([0-9]+)\r?\n?", raw)
        need(match is not None, "EXACT_ASSEMBLER_IMAGE_RECORD")
        image_pin = pin(image)
        need(int(match[2]) == image_pin["bytes"], "ACTUAL_IMAGE_BYTE_COUNT")
        report.update(status=ASSEMBLY_PASS, image={"path":str(image), **image_pin},
                      image_id=match[1].decode("ascii"), image_id_origin="ACTUAL_PINNED_ASSEMBLER_NOT_FILE_SHA256")
    except BaseException as error:
        report["error"] = type(error).__name__ + ": " + str(error)[:2000]
    try:
        rebind()
        if report["status"] == ASSEMBLY_PASS:
            need(pin(image) == {key:report["image"][key] for key in ("bytes", "sha256")}, "ASSEMBLED_IMAGE_CHANGED")
        report["logs"] = [{"path":str(output / name), **pin(output / name, 65536, allow_empty=True)}
            for name in ("stdout.txt", "stderr.txt") if (output / name).exists()]
    except BaseException as error:
        report.update(status="FAIL_FINAL_BINDING", final_error=type(error).__name__ + ": " + str(error)[:2000])
    save(output / "RESULT.json", report)
    print(json.dumps(report, allow_nan=False), flush=True)
    return 0 if report["status"] == ASSEMBLY_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
