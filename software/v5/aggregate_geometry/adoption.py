"""Adopt one exact po17 snapshot link over an already audited refined backend.

Owner-selected local build evidence, not mathematics or an independent compiler
correctness proof. The build rebinds its complete compiler runtime; layout owners
pin its evidence and four actual refined libraries without rereading that 2GiB
toolchain on every operation. No old stage executable is adopted or invoked.
"""
from pathlib import Path
import re

from production import producer as P

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
OLD = ROOT/"experiments/v5-local-checks/prover-allocation-build-01"
SCHEMA = "DMKN_V5_GEOMETRY17_SNAPSHOT_HOST_BUILD"
PASS = "PASS_GEOMETRY17_SNAPSHOT_HOST_ONE_LINK_ONLY"
NAMES = ("risc0_circuit_rv32im", "risc0_zkvm", "dmkn_module_relation", "dmkn_aggregate_relation")
SOURCE_SET = {"software/v5/aggregate_geometry/"+name for name in ("build_snapshot.py", "aggregate_host.rs")}
SOURCE_SET.add("software/v5/aggregate/receipt.rs")
RETAINED = {
    "result": ("RESULT.json", "ac259e9db55275a0a8404e9cf881fd3779f2e7259ccfe134c8e93e3b180b4102"),
    "commands": ("compile-commands.json", "55ead9865ee0c2dcbb4ee667bc99a24bb9afe6ec095f0a3c2b91913d8293e03e"),
    "environment": ("environment-profile.json", "ae9c06c986ab9f325fb5624d6d9b39392383c98093e60168e023d3b84c407b05"),
    "selection": ("selection.json", "7a548b3f74c0c5bbe8bc2ba68e408a3dfdf22addefb9410b1a25f5d8be5d13ff")}
EXTRA_RECORDS = {
    OLD/"source-map.json": "dc7cfeba823551159f93f9add5ac10031a335079de6682d886dd792646f75f3f",
    OLD/"INPUT-MAP.json": "91d7d7fb56353eb19671a09d7e70686a110e100beefbf51f2be48c362d03f63f",
    OLD.parent/"prover-allocation-build-01-attempt.json":
        "2c61fd2ca46d86fe2d179f8728483bb5c1c207f248ab83f4bc4db4f273afb1e6"}
COUNTS = {"backend_rust_crate_rebuilds": 0, "relation_rust_crate_rebuilds": 0,
    "snapshot_host_links": 1, "stage_host_links": 0, "checker_rebuilds": 0,
    "native_circuit_rebuilds": 0, "guest_rebuilds": 0, "host_calls": 0,
    "guest_calls": 0, "proof_calls": 0, "network_calls": 0}
LIMITS = {"worker_cpu_seconds": 240, "worker_wall_seconds": 300, "memory_mib": 2048,
    "active_processes": 6, "ordinary_controller_cpu_seconds": 40, "controller_cpu_seconds": 60,
    "total_wall_seconds": 420, "fresh_output_bytes": 536870912, "fresh_output_entries": 8192,
    "command_log_bytes": 1048576}
RESULT_FIELDS = ("schema", "status", "selection_sha256", "limits", "retained_result_sha256",
    "retained_commands_sha256", "retained_environment_sha256", "retained_selection_sha256",
    "runtime_pin_count", "runtime_pin_bytes", "refined_libraries", *COUNTS, "authority",
    "source_map_sha256", "commands_sha256", "environment_sha256", "input_map_sha256",
    "executable", "job", "commands", "controller_cpu_seconds", "wall_seconds",
    "output_census", "sampled_peaks", "accounting")


def _closed(job):
    P.require(type(job) is dict and type(job.get("active_processes")) is int
              and job["active_processes"] == 0 and type(job.get("terminated_processes")) is int
              and job["terminated_processes"] == 0, "GEOMETRY17_CLOSED_BUILD_JOB")
    return P.number(job["cpu_seconds"])


def _read_named(owner, root, name, expected, table):
    pin = P.file_pin(root/name)
    P.require(pin["sha256"] == expected, "GEOMETRY17_BUILD_RECORD_HASH:"+name)
    owner._add(table, pin, 2*P.MIB)
    return P.parse(owner._read(pin, 2*P.MIB)), pin


def adopt_build(owner, pins, table):
    records = owner._records(pins, ("result", "attempt", "selection", "source_map", "command"), table)
    result, selection, sources, command = (records[k] for k in ("result", "selection", "source_map", "command"))
    P.fields(result, RESULT_FIELDS)
    P.fields(selection, ("schema", "name", "authorizes_compile_only", "sources", "runtime_pins", "limits"))
    P.require(selection["schema"] == SCHEMA+"_V1" and result["schema"] == SCHEMA+"_RESULT_V1"
              and selection["authorizes_compile_only"] is True and result["status"] == PASS
              and result["selection_sha256"] == pins["selection"]["sha256"]
              and P.encoded(selection["limits"]) == P.encoded(LIMITS)
              and P.encoded(result["limits"]) == P.encoded(LIMITS)
              and result["authority"] == "SNAPSHOT_HOST_ONE_LINK_ONLY_NOT_MATHEMATICAL_ADMISSION",
              "GEOMETRY17_BUILD_SCOPE")
    for key, expected in COUNTS.items():
        P.require(type(result[key]) is int and result[key] == expected, "GEOMETRY17_LINK_ONLY_COUNTS")
    P.require(P.encoded(records["attempt"]) == P.encoded({"status": PASS,
              "result_sha256": pins["result"]["sha256"]}), "GEOMETRY17_ATTEMPT_BINDING")
    run = Path(pins["result"]["path"]).parent
    P.require(type(selection["name"]) is str
              and re.fullmatch(r"geometry17-snapshot-host-build-[0-9]{2}", selection["name"])
              and run.name == selection["name"] and run.parent == OLD.parent,
              "GEOMETRY17_EXACT_BUILD_DIRECTORY")
    for key, filename in (("result", "RESULT.json"), ("source_map", "source-map.json"),
                          ("command", "compile-command.json")):
        P.require(Path(pins[key]["path"]) == run/filename, "GEOMETRY17_BUILD_RECORD_PATH")
    P.require(Path(pins["attempt"]["path"]) == run.parent/(run.name+"-attempt.json"),
              "GEOMETRY17_BUILD_ATTEMPT_PATH")
    P.require(result["source_map_sha256"] == pins["source_map"]["sha256"]
              and result["commands_sha256"] == pins["command"]["sha256"], "GEOMETRY17_BUILD_RECORD_BINDINGS")
    P.fields(sources, SOURCE_SET)
    P.require(P.encoded(sources) == P.encoded(selection["sources"]), "GEOMETRY17_EXACT_SOURCE_MAP")
    for relative, content in sources.items():
        P.fields(content, ("bytes", "sha256"))
        owner._add(table, {"path": str(run/"source"/relative), **content}, P.MIB)

    old, retained_pins = {}, []
    for role, (filename, expected) in RETAINED.items():
        P.require(result["retained_"+role+"_sha256"] == expected, "GEOMETRY17_RETAINED_BUILD_BINDING")
        old[role], pin = _read_named(owner, OLD, filename, expected, table)
        retained_pins.append(pin)
    for path, expected in EXTRA_RECORDS.items():
        value, pin = _read_named(owner, path.parent, path.name, expected, table)
        retained_pins.append(pin)
        if path.name.endswith("-attempt.json"):
            P.require(value == {"status": "PASS_PROVER_ALLOCATION_FIVE_STEP_COMPILE_ONLY",
                      "result_sha256": RETAINED["result"][1]}, "GEOMETRY17_RETAINED_ATTEMPT")
    owner._retained_build_pins = tuple(retained_pins)
    P.require(old["result"]["status"] == "PASS_PROVER_ALLOCATION_FIVE_STEP_COMPILE_ONLY"
              and old["result"]["commands_sha256"] == RETAINED["commands"][1]
              and old["result"]["environment_sha256"] == RETAINED["environment"][1]
              and old["result"]["selection_sha256"] == RETAINED["selection"][1]
              and _closed(old["result"]["job"]) <= 1200, "GEOMETRY17_ACTUAL_REFINED_BUILD")
    libraries = {name: old["result"]["outputs"][name] for name in NAMES}
    P.require(P.encoded(libraries) == P.encoded(result["refined_libraries"]),
              "GEOMETRY17_EXACT_FOUR_REFINED_LIBRARIES")
    for pin in libraries.values():
        owner._add(table, pin, 64*P.MIB)

    prior_command = old["commands"][-1]
    P.fields(prior_command, ("name", "argv"))
    P.require(prior_command["name"] == "small_aggregate_stage_host", "GEOMETRY17_RETAINED_FINAL_LINK")
    expected_command = list(prior_command["argv"])
    replacements = (
        ("small_aggregate_stage_host", "geometry17_aggregate_host"),
        ("metadata=dmkn_auxwords_a53940b67580e215_small_aggregate_stage_host", "metadata=dmkn_geometry17_aggregate_host"),
        (str(OLD/"source/stage/software/v5/aggregate_small/stage_host.rs"),
         str(run/"source/software/v5/aggregate_geometry/aggregate_host.rs")),
        (str(OLD/"small_aggregate_stage_host.exe"), str(run/"geometry17_aggregate_host.exe")))
    for before, after in replacements:
        P.require(expected_command.count(before) == 1, "GEOMETRY17_UNIQUE_RECIPE_SUBSTITUTION")
        expected_command[expected_command.index(before)] = after
    P.require(P.encoded(command) == P.encoded(expected_command), "GEOMETRY17_EXACT_ONE_LINK_RECIPE")
    for name in NAMES[1:]:
        P.require(command.count(name+"="+libraries[name]["path"]) == 1, "GEOMETRY17_DIRECT_REFINED_EDGE")
    P.require(command.count("dependency="+str(OLD/"lib")) == 1
              and old["commands"][1]["argv"].count(
                  NAMES[0]+"="+libraries[NAMES[0]]["path"]) == 1,
              "GEOMETRY17_TRANSITIVE_REFINED_CIRCUIT_EDGE")
    P.require(type(result["commands"]) is list and len(result["commands"]) == 1,
              "GEOMETRY17_EXACTLY_ONE_COMPILER_COMMAND")
    actual = result["commands"][0]
    P.require(actual["argv"] == command and actual["cwd"] == str(ROOT)
              and actual["label"] == "geometry17-aggregate-snapshot-host"
              and actual["status"] == "COMMAND_COMPLETED" and type(actual["exit_code"]) is int
              and actual["exit_code"] == 0 and actual["cleanup_errors"] == []
              and _closed(actual["job_before"]) == 0
              and _closed(actual["job_after"]) <= LIMITS["worker_cpu_seconds"]
              and P.number(actual["wall_seconds"]) <= LIMITS["worker_wall_seconds"],
              "GEOMETRY17_CLEAN_ONE_LINK_COMPLETION")
    P.require(P.pin_fields(result["executable"]) == run/"geometry17_aggregate_host.exe",
              "GEOMETRY17_EXACT_EXECUTABLE_PATH")
    owner._add(table, result["executable"])

    environment, _ = _read_named(owner, run, "environment-profile.json", result["environment_sha256"], table)
    input_map, _ = _read_named(owner, run, "INPUT-MAP.json", result["input_map_sha256"], table)
    expected_env = {key: value.replace(str(OLD), str(run))
                    for key, value in old["environment"]["step_environments"]["small_aggregate_stage_host"].items()}
    P.fields(environment, ("cargo_jobs", "environment_keys_only", "explicit_environment", "host_binaries",
                          "include_directories", "library_directories", "no_inherited_environment", "rayon_threads"))
    P.require(P.encoded(environment["explicit_environment"]) == P.encoded(expected_env)
              and environment["environment_keys_only"] == sorted(expected_env)
              and environment["no_inherited_environment"] is True
              and environment["cargo_jobs"] == old["environment"]["cargo_jobs"]
              and environment["rayon_threads"] == old["environment"]["rayon_threads"]
              and environment["include_directories"] == old["environment"]["include_directories"]
              and environment["library_directories"] == old["environment"]["library_directories"]
              and P.encoded(environment["host_binaries"]) == P.encoded(old["environment"]["host_binaries"]),
              "GEOMETRY17_EXACT_COMPILER_ENVIRONMENT")
    P.fields(input_map, ("sources", "runtime_pins", "refined_libraries", "records", "helper_pins", "trust_boundary"))
    expected_records = {str(OLD/filename): expected for role, (filename, expected) in RETAINED.items()
                        if role != "selection"}
    expected_records[str(OLD.parent/"prover-allocation-build-01-selection.json")] = RETAINED["selection"][1]
    expected_records.update({str(path): expected for path, expected in EXTRA_RECORDS.items()})
    P.require(P.encoded(input_map["sources"]) == P.encoded(sources)
              and P.encoded(input_map["refined_libraries"]) == P.encoded(libraries)
              and P.encoded(input_map["runtime_pins"]) == P.encoded(selection["runtime_pins"])
              and P.encoded(input_map["records"]) == P.encoded(expected_records)
              and input_map["trust_boundary"] ==
                  "Pinned retained refined libraries and trusted tools plus Windows system DLLs; not hermetic/sandboxed",
              "GEOMETRY17_EXACT_BUILD_INPUT_MAP")
    helpers = input_map["helper_pins"]
    P.require(type(helpers) is dict and 1 <= len(helpers) <= 64, "GEOMETRY17_HELPER_MAP_BOUND")
    for path, expected in helpers.items():
        P.require(type(path) is str and Path(path).is_absolute(), "GEOMETRY17_HELPER_PATH")
        P.digest(expected)
    runtime = selection["runtime_pins"]
    expected_runtime = old["selection"]["runtime_pins"]
    P.require(P.encoded(runtime) == P.encoded(expected_runtime)
              and type(result["runtime_pin_count"]) is int and result["runtime_pin_count"] == len(runtime)
              and type(result["runtime_pin_bytes"]) is int
              and result["runtime_pin_count"] == 1071 and result["runtime_pin_bytes"] == 2320491997,
              "GEOMETRY17_DERIVED_TOOLCHAIN_CLOSURE")
    P.require(_closed(actual["job_after"]) <= _closed(result["job"]) <= LIMITS["worker_cpu_seconds"]
              and P.number(actual["inclusive_cpu_delta"]) == actual["job_after"]["cpu_seconds"]
              and P.number(result["controller_cpu_seconds"]) <= LIMITS["controller_cpu_seconds"]
              and P.number(result["wall_seconds"]) <= LIMITS["total_wall_seconds"],
              "GEOMETRY17_TOTAL_BUILD_LIMITS")
    for census in (result["output_census"], result["sampled_peaks"]):
        P.uint(census["working_bytes"], LIMITS["fresh_output_bytes"])
        P.uint(census["entries"], LIMITS["fresh_output_entries"])
    owner._check(table)
    owner._no_override((*pins.values(), *retained_pins))
    return result["executable"]
