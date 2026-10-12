"""Assemble one adopted bounded-parse guest ELF with the retained kernel.

Source-snapshot-only adapter under the owner's finite local-check Job. No build,
guest session, receipt or proof is produced. Inner success never overrides failed
outer supervision or finalization. Existing snapshot.py consumes the generic
assembly-only fields; new provenance does not borrow the old failure lineage.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
SNAPSHOT_SUFFIX = ("sources", "software", "v5", "bounded_parse_guest", "assemble.py")
DRIVER_HOME = ROOT / "experiments/general-checker-guest-02/driver-build-04"
DRIVER_RESULT_SHA = "d89626da253ade06a4482d6e7f4a7e9aac0f93d360a2eab2f1b39ba25cc8c43a"
KERNEL = ROOT / ("experiments/general-checker-guest-01/host-prepare-01/original/"
                "risc0-3bbcd44d6459b9ef6ac0df3846dc9215514934e8/risc0/zkos/v1compat/elfs/v1compat.elf")
KERNEL_PIN = {"bytes": 58736,
              "sha256": "9dd8af014a24db3752b9beda71c837f553ff361fc1bca83cc79584bd38ac9de5"}
BUILD_PASS = "PASS_BOUNDED_PARSE_THREE_PROJECT_COMPILES_ONLY"
ASSEMBLY_PASS = "PASS_NEW_AGGREGATE_IMAGE_ASSEMBLY_ONLY"
SCHEMA = "DMKN_V5_BOUNDED_PARSE_IMAGE_ASSEMBLY_RESULT_V1"
PROJECT_NAMES = ["dmkn_module_relation", "dmkn_aggregate_relation", "dmkn-aggregate-claim-guest"]
BUILD_ADAPTERS = {"software/v5/bounded_parse_guest/build_projects.py",
                  "software/v5/bounded_parse_guest/recipes.py"}
SOURCE_RUN = HERE / "bounded-parse-guest-build-02"
SOURCE_MAP_SHA = "1ca936d624d91d7d395ac89f7535e1564473ee62e05a6f357e754b6d2c93281b"
SOURCE_SELECTION_SHA = "a537fdbc9bf27b9a0832bb14a72aa07aad4d96abe9cc6bb433473a58935c16e2"
SOURCE_GRAPH_SHA = "142224e56a81b3d73960a0aa5c5f80360658ccf0f1bff06883152cbfe92511fe"
SOURCE_COMPARISON_SHA = "36b0bd9bc55a15adca6f8e878bda3b2529d015fe841075aa3f2d30e771780bc5"
FAILED_RESULT_SHA = "792ed5825ae3110dc3ddc1a85b49636b63469f5e4cb1d662e70d8ddf27d6b4b6"
FAILED_OVERRIDE_SHA = "36c6f5c6b7084dbb08d461c008ea8b39e71e80bf95cc90860e455936b637cf55"
MIB = 1024**2
FILE_LIMIT = 64 * MIB
RECORD_LIMIT = 2 * MIB
LOG_LIMIT = 65536


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def ordinary(path, fresh=False):
    need(path.is_absolute() and ".." not in path.parts, "ABSOLUTE_NORMALIZED_PATH")
    if fresh:
        need(not path.exists() and not path.is_symlink() and not path.is_junction(), "FRESH_PATH")
        first = path.parent
    else:
        first = path
    need(first.resolve(strict=True) == first, "EXACT_RESOLVED_PATH")
    for item in (first, *first.parents):
        info = item.lstat()
        need(not info.st_file_attributes & 0x400, "NO_REPARSE_ANCESTRY")
        if item != path or fresh:
            need(item.is_dir(), "ORDINARY_PARENT")


def pin(path, maximum=FILE_LIMIT, allow_empty=False):
    ordinary(path)
    need(path.is_file(), "ORDINARY_FILE")
    size = path.stat().st_size
    need((size >= 0 if allow_empty else size > 0) and size <= maximum, "FILE_SIZE_BOUND")
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    need(path.stat().st_size == size, "FILE_CHANGED_DURING_HASH")
    return {"bytes": size, "sha256": digest}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def save(path, value):
    raw = (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")
    need(len(raw) <= RECORD_LIMIT, "OUTPUT_RECORD_BOUND")
    ordinary(path, fresh=True)
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def main():
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated
         and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "CANONICAL_ISOLATED_OWNER_INVOCATION")
    invoked = Path(__file__).resolve(strict=True)
    need(invoked.is_relative_to(HERE), "OWNER_JOB_SOURCE_SNAPSHOT_ROOT")
    relative = invoked.relative_to(HERE).parts
    need(len(relative) == 6 and relative[1:] == SNAPSHOT_SUFFIX
         and re.fullmatch(r"[a-z0-9][a-z0-9-]{0,95}", relative[0]), "EXACT_OWNER_SOURCE_SNAPSHOT")
    parser = argparse.ArgumentParser()
    parser.add_argument("--guest-result", required=True)
    parser.add_argument("--guest-result-sha256", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    need(re.fullmatch(r"[0-9a-f]{64}", args.guest_result_sha256), "ADOPTED_RESULT_DIGEST")
    build_result, output = Path(args.guest_result), Path(args.output)
    need(build_result.name == "RESULT.json" and build_result.parent.parent == HERE
         and build_result.parent.name == "bounded-parse-direct-build-01",
         "EXACT_NEW_GUEST_BUILD_RESULT")
    need(output.parent == HERE / relative[0] and output.name == "assembly", "SELECTED_FRESH_ASSEMBLY_DESTINATION")
    ordinary(output, fresh=True)
    run = build_result.parent
    failure_marker = run / "FINALIZATION-FAILED.json"
    inputs = {}

    def remember(path, maximum=FILE_LIMIT, expected=None):
        observed = pin(path, maximum)
        need(expected is None or observed == expected, "EXACT_INPUT_PIN:" + str(path))
        need(path not in inputs or inputs[path] == (observed, maximum), "CONSISTENT_INPUT_PIN")
        inputs[path] = (observed, maximum)
        return observed

    def record(path, expected_hash=None):
        observed = remember(path, RECORD_LIMIT)
        need(expected_hash is None or observed["sha256"] == expected_hash, "EXACT_RECORD_DIGEST")
        with path.open("rb") as stream:
            raw = stream.read(RECORD_LIMIT + 1)
        need(len(raw) == observed["bytes"] and hashlib.sha256(raw).hexdigest() == observed["sha256"],
             "RECORD_CHANGED_DURING_READ")
        value = json.loads(raw, object_pairs_hook=unique_object)
        need(type(value) is dict, "JSON_OBJECT_RECORD")
        return value

    def no_failure():
        need(not failure_marker.exists() and not failure_marker.is_symlink()
             and not failure_marker.is_junction(), "NO_OVERRIDING_BUILD_FINALIZATION_FAILURE")

    no_failure()
    built = record(build_result, args.guest_result_sha256)
    need(built["schema"] == "DMKN_V5_BOUNDED_PARSE_DIRECT_PROJECT_BUILD_RESULT_V1"
         and built["status"] == BUILD_PASS and built["job"]["active_processes"] == 0
         and built["job"]["terminated_processes"] == 0
         and type(built["compiler_calls"]) is int and built["compiler_calls"] == 3
         and all(type(built[name]) is int and built[name] == 0 for name in
                 ("cargo_calls", "graph_commands", "dependency_compiles", "checker_compiles",
                  "guest_calls", "proof_calls", "image_assembly_calls", "network_calls")),
         "ADOPTED_SUCCESSFUL_CLOSED_GUEST_BUILD_ONLY")
    need(type(built["commands"]) is list and len(built["commands"]) == 3
         and [row["label"] for row in built["commands"]] == ["module", "aggregate", "guest"]
         and all(row["status"] == "COMMAND_COMPLETED" and row["exit_code"] == 0
                 and row["cleanup_errors"] == [] and row["job_after"]["active_processes"] == 0
                 and row["job_after"]["terminated_processes"] == 0
                 for row in built["commands"]), "EXACT_THREE_SUCCESSFUL_CLOSED_BUILD_COMMANDS")
    attempt = HERE / (run.name + "-attempt.json")
    need(record(attempt) == {"status": BUILD_PASS, "result_sha256": args.guest_result_sha256},
         "EXACT_TERMINAL_BUILD_ATTEMPT")
    selected = record(run / "selection.json", built["selection_sha256"])
    need(selected["schema"] == "DMKN_V5_BOUNDED_PARSE_DIRECT_PROJECT_BUILD_V1"
         and selected["name"] == run.name
         and selected["authorizes_three_compiles_and_retained_artifact_adoption"] is True
         and set(selected["adapters"]) == BUILD_ADAPTERS and selected["limits"] == built["limits"],
         "EXACT_ADOPTED_BUILD_SELECTION")
    need(0 <= built["job"]["cpu_seconds"] <= selected["limits"]["worker_cpu_seconds"] == 240
         and 0 <= built["controller_cpu_seconds"] <= selected["limits"]["controller_cpu_seconds"] == 60
         and 0 <= built["wall_seconds"] <= selected["limits"]["total_wall_seconds"] == 420,
         "SUCCESSFUL_DIRECT_BUILD_WITHIN_RECORDED_LIMITS")
    artifact = record(run / "ARTIFACT.json")
    graph = record(run / "GRAPH-COMPARISON.json")
    need(artifact == built["artifact"], "EXACT_ARTIFACT_RECORD")
    # The completed new operation adopted, rather than reran, the retained
    # exact graph and source snapshot. Failed02 remains failed independently.
    failed = record(SOURCE_RUN / "RESULT.json", FAILED_RESULT_SHA)
    failed_override = record(SOURCE_RUN / "FINALIZATION-FAILED.json", FAILED_OVERRIDE_SHA)
    need(failed["status"] == "FAIL" and failed_override["status"] == "FAIL_FINALIZATION"
         and failed_override["overrides_result_and_attempt"] is True
         and failed_override["result_sha256"] == FAILED_RESULT_SHA
         and built["predecessor_status"] == "FAIL_FINALIZATION"
         and built["predecessor_result_sha256"] == FAILED_RESULT_SHA,
         "FAILED02_LINEAGE_PRESERVED_NOT_PROMOTED")
    prior_selection = record(SOURCE_RUN / "selection.json", SOURCE_SELECTION_SHA)
    prior_map = record(SOURCE_RUN / "SOURCE-MAP.json", SOURCE_MAP_SHA)
    record(SOURCE_RUN / "UNIT-GRAPH.json", SOURCE_GRAPH_SHA)
    comparison = record(SOURCE_RUN / "GRAPH-COMPARISON.json", SOURCE_COMPARISON_SHA)
    need(graph == {"schema": "DMKN_V5_RETAINED_GRAPH_PROJECTION_V1",
                  "retained_graph_sha256": SOURCE_GRAPH_SHA, "comparison": comparison,
                  "new_compilation_units": PROJECT_NAMES, "new_cargo_graph_commands": 0}
         and comparison["status"] == "EXACT_297_UNITS_TWO_CHANGED_LIB_ROOTS_AND_PROJECT_CACHE_RELOCATION"
         and comparison["old_units"] == comparison["new_units"] == 297
         and comparison["package_feature_profile_edge_changes"] == 0, "EXACT_RETAINED_GRAPH_PROJECTION")
    source_map = record(run / "SOURCE-MAP.json")
    input_map = record(run / "INPUT-MAP.json")
    recipes = record(run / "RECIPES.json")
    project = prior_map["project"]
    compiler_sources = {name: value for name, value in project.items()
                        if name.endswith(".rs") and not name.startswith("software/v5/modules/native/")}
    need(built["source_snapshot"] == str(SOURCE_RUN / "project")
         and built["source_map_sha256"] == SOURCE_MAP_SHA
         and len(project) == 39 and set(project) == set(prior_selection["sources"]) | {
             "software/v5/bounded_parse_guest/Cargo.lock"}
         and all(project[name] == value for name, value in prior_selection["sources"].items())
         and len(compiler_sources) == 16
         and source_map == {"source_snapshot": str(SOURCE_RUN / "project"), "project": project,
                            "compiler_read_sources": compiler_sources, "adapters": selected["adapters"]},
         "EXACT_39_FILE_SOURCE_SNAPSHOT_AND_DIRECT_ADAPTERS")
    need(recipes["schema"] == "DMKN_V5_DIRECT_PROJECT_RECIPES_V1"
         and recipes["basis"] == "RECONSTRUCTED_EQUIVALENT_PROFILE_NOT_CAPTURED_CARGO_ARGV"
         and type(recipes["recipes"]) is list and len(recipes["recipes"]) == 3
         and [row["name"] for row in recipes["recipes"]] == PROJECT_NAMES
         and all(command["argv"] == recipe["argv"] for command, recipe in
                 zip(built["commands"], recipes["recipes"])), "THREE_RECORDED_ACTUAL_RECIPE_COMMANDS")
    need(set(input_map) == {"inputs", "copied_artifacts"}
         and len(input_map["copied_artifacts"]) == 238
         and len(selected["retained_artifacts"]) == 238
         and all(input_map["inputs"].get(name) == value
                 for name, value in selected["retained_artifacts"].items()),
         "SELECTED_RETAINED_LIBRARY_INPUT_RECORD")
    # Rebind small exact project sources and adapters, not the whole SDK or
    # copied dependency tree. Independent adoption owns the actual-build audit.
    for base, rows in ((SOURCE_RUN / "project", project), (ROOT, selected["adapters"])):
        for name, expected in rows.items():
            relative_path = Path(name)
            need(not relative_path.is_absolute() and ".." not in relative_path.parts,
                 "SELECTED_SOURCE_RELATIVE_PATH")
            source = base / relative_path
            need(input_map["inputs"].get(str(source)) == expected, "SELECTED_SOURCE_INPUT_BINDING")
            remember(source, RECORD_LIMIT, expected)
    user_pin, map_pin = artifact["user_elf"], artifact["link_map"]
    need(set(user_pin) == set(map_pin) == {"path", "bytes", "sha256"}, "EXACT_ARTIFACT_PIN_SHAPE")
    user, link_map = Path(user_pin["path"]), Path(map_pin["path"])
    need(user == run / "outputs/dmkn-aggregate-claim-guest" and link_map == run / "guest-link.map"
         and built["outputs"][user.name] == user_pin
         and recipes["recipes"][-1]["output"] == str(user), "EXACT_SELECTED_ELF_AND_LINK_MAP")
    remember(user, FILE_LIMIT, {key: user_pin[key] for key in ("bytes", "sha256")})
    remember(link_map, 32 * MIB, {key: map_pin[key] for key in ("bytes", "sha256")})
    driver = record(DRIVER_HOME / "RESULT.json", DRIVER_RESULT_SHA)
    need(driver["status"] == "PASS_DRIVER_COMPILE_ONLY", "ADOPTED_EXISTING_ASSEMBLER")
    executable = Path(driver["executable"]["path"])
    need(executable.parent == DRIVER_HOME, "EXACT_ASSEMBLER_HOME")
    remember(executable, 128 * MIB, {key: driver["executable"][key] for key in ("bytes", "sha256")})
    remember(KERNEL, FILE_LIMIT, KERNEL_PIN)

    def rebind():
        no_failure()
        for path, (expected, maximum) in inputs.items():
            need(pin(path, maximum) == expected, "SELECTED_INPUT_CHANGED:" + str(path))
        no_failure()

    rebind()
    output.mkdir()
    image = output / "aggregate_image.bin"
    command = [str(executable), "assemble", str(user), str(KERNEL), str(image)]
    source_records = [{"path": str(path), **observed} for path, (observed, _) in inputs.items()]
    save(output / "COMMAND.json", {"argv": command, "cwd": str(ROOT), "timeout_seconds": 60,
         "selected_inputs": source_records, "guest_result_sha256": args.guest_result_sha256,
         "absent_failure_marker": str(failure_marker), "authority": "ASSEMBLY_ONLY_NOT_ADMISSION"})
    report = {"schema": SCHEMA, "status": "FAIL_BOUNDED_PARSE_IMAGE_ASSEMBLY",
        "assembler_calls": 0, "guest_executions": 0, "proof_calls": 0, "mathematical_admission": False,
        "guest_build_result": {"path": str(build_result), **inputs[build_result][0]},
        "artifact_record": {"path": str(run / "ARTIFACT.json"), **inputs[run / "ARTIFACT.json"][0]},
        "selection_sha256": built["selection_sha256"],
        "predecessor_failure": {"status": built["predecessor_status"], "result_sha256": FAILED_RESULT_SHA,
            "override_sha256": FAILED_OVERRIDE_SHA, "source_snapshot_reused": built["source_snapshot"],
            "failed_build_is_not_assembly_prerequisite_success": True},
        "authority": "INNER_ASSEMBLY_ONLY_OWNER_MUST_ADOPT_CLEAN_OUTER_COMPLETION"}
    try:
        rebind()
        environment = {key: value for key, value in os.environ.items() if not key.upper().startswith("RISC0_")}
        report["assembler_calls"] = 1
        with (output / "stdout.txt").open("xb") as stdout, (output / "stderr.txt").open("xb") as stderr:
            actual = subprocess.run(command, cwd=ROOT, env=environment, stdin=subprocess.DEVNULL,
                                    stdout=stdout, stderr=stderr, timeout=60, check=False,
                                    creationflags=subprocess.CREATE_NO_WINDOW)
        report["exit_code"] = actual.returncode
        stdout_pin = pin(output / "stdout.txt", LOG_LIMIT)
        stderr_pin = pin(output / "stderr.txt", LOG_LIMIT, allow_empty=True)
        need(actual.returncode == 0 and stderr_pin["bytes"] == 0, "ASSEMBLER_ZERO_WITHOUT_DIAGNOSTICS")
        with (output / "stdout.txt").open("rb") as stream:
            raw = stream.read(LOG_LIMIT + 1)
        need(len(raw) == stdout_pin["bytes"] and hashlib.sha256(raw).hexdigest() == stdout_pin["sha256"],
             "ASSEMBLER_STDOUT_CHANGED")
        match = re.fullmatch(rb"COMBINED_IMAGE image_id=([0-9a-f]{64}) bytes=([0-9]+)\r?\n?", raw)
        need(match is not None, "EXACT_ASSEMBLER_IMAGE_RECORD")
        image_pin = pin(image)
        need(int(match[2]) == image_pin["bytes"], "ACTUAL_IMAGE_BYTE_COUNT")
        report.update(status=ASSEMBLY_PASS, image={"path": str(image), **image_pin},
                      image_id=match[1].decode("ascii"),
                      image_id_origin="ACTUAL_PINNED_ASSEMBLER_NOT_FILE_SHA256")
    except BaseException as error:
        report["error"] = type(error).__name__ + ": " + str(error)[:2000]
    try:
        rebind()
        if report["status"] == ASSEMBLY_PASS:
            need(pin(image) == {key: report["image"][key] for key in ("bytes", "sha256")},
                 "ASSEMBLED_IMAGE_CHANGED_BEFORE_FINALIZATION")
        logs = []
        for name in ("stdout.txt", "stderr.txt"):
            path = output / name
            if path.exists():
                logs.append({"path": str(path), **pin(path, LOG_LIMIT, allow_empty=True)})
        report["logs"] = logs
    except BaseException as error:
        report.update(status="FAIL_FINAL_BINDING", final_error=type(error).__name__ + ": " + str(error)[:2000])
    save(output / "RESULT.json", report)
    print(json.dumps(report, allow_nan=False), flush=True)
    return 0 if report["status"] == ASSEMBLY_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
