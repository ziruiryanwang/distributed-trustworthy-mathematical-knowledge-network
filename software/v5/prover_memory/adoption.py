"""Adopt one exact five-compile allocation-refined host build.

These owner-pinned records establish build identity, not mathematical truth.
The build operation rebinds its compiler/runtime inputs; ordinary proof owners
do not repeatedly scan that toolchain. The receiver still checks the receipt.
"""
from pathlib import Path, PurePosixPath
import re

from production import producer as P

SOURCE_SHA = "c93a45a6a558718c931c39b121e9bcffa7d464ecaa1d5b0e80185efd6cace710"
SCHEMA = "DMKN_V5_PROVER_ALLOCATION_BUILD"
PASS = "PASS_PROVER_ALLOCATION_FIVE_STEP_COMPILE_ONLY"
NAMES = ("risc0_circuit_rv32im", "risc0_zkvm", "dmkn_module_relation",
         "dmkn_aggregate_relation", "small_aggregate_stage_host")
COUNTS = {"backend_rust_crate_rebuilds": 2, "relation_rust_crate_rebuilds": 2,
          "stage_host_links": 1, "checker_rebuilds": 0, "native_circuit_rebuilds": 0,
          "guest_rebuilds": 0, "host_calls": 0, "guest_calls": 0,
          "proof_calls": 0, "network_calls": 0}
LIMITS = {"worker_cpu_seconds": 240, "worker_wall_seconds": 300, "memory_mib": 2048,
          "active_processes": 6, "total_worker_cpu_seconds": 1200,
          "ordinary_controller_cpu_seconds": 120, "controller_cpu_seconds": 180,
          "total_wall_seconds": 1800, "fresh_output_bytes": 1073741824,
          "fresh_output_entries": 8192, "command_log_bytes": 1048576}
ADAPTERS = {"software/v5/prover_memory/"+name for name in
            ("build.py", "SOURCE.json", "preflight.patch", "BUILD-RECIPE.md")}
RESULT_FIELDS = ("schema", "status", "selection_sha256", "descriptor_sha256", "patch_sha256",
    "limits", "runtime_pin_count", "runtime_pin_bytes", *COUNTS, "authority", "source_map_sha256",
    "commands_sha256", "environment_sha256", "input_map_sha256", "outputs", "executable", "job", "commands", "controller_cpu_seconds",
    "wall_seconds", "output_census", "sampled_peaks", "accounting")


def _relative(root, relative):
    P.require(type(relative) is str and "\\" not in relative and ":" not in relative,
              "REFINEMENT_RELATIVE_PATH")
    parts = PurePosixPath(relative).parts
    P.require(parts and all(x not in ("", ".", "..") for x in parts)
              and PurePosixPath(*parts).as_posix() == relative
              and not PurePosixPath(relative).is_absolute(), "REFINEMENT_RELATIVE_PATH")
    return root.joinpath(*parts)


def _content(pin):
    P.fields(pin, ("bytes", "sha256"))
    P.uint(pin["bytes"], 8*P.MIB); P.digest(pin["sha256"])
    return pin


def _closed_job(job):
    P.require(type(job) is dict and type(job.get("active_processes")) is int
              and job["active_processes"] == 0 and type(job.get("terminated_processes")) is int
              and job["terminated_processes"] == 0, "REFINEMENT_BUILD_JOB_CLOSURE")
    return P.number(job["cpu_seconds"])


def adopt_build(owner, pins, table):
    records = owner._records(pins, ("result", "attempt", "selection", "source_map", "command"), table)
    result, selected, sources = (records[k] for k in ("result", "selection", "source_map"))
    P.fields(result, RESULT_FIELDS)
    P.fields(selected, ("schema", "name", "authorizes_compile_only", "sources", "runtime_pins", "limits"))
    P.require(selected["schema"] == SCHEMA+"_V1" and result["schema"] == SCHEMA+"_RESULT_V1"
              and selected["authorizes_compile_only"] is True and result["status"] == PASS
              and result["selection_sha256"] == pins["selection"]["sha256"]
              and P.encoded(selected["limits"]) == P.encoded(LIMITS)
              and P.encoded(result["limits"]) == P.encoded(LIMITS), "REFINEMENT_BUILD_SCOPE")
    for key, value in COUNTS.items():
        P.require(type(result[key]) is int and result[key] == value, "REFINEMENT_REBUILD_COUNTS")
    P.require(P.encoded(records["attempt"]) == P.encoded({"status": PASS,
              "result_sha256": pins["result"]["sha256"]}), "REFINEMENT_ATTEMPT_BINDING")
    root = Path(pins["result"]["path"]).parent
    P.require(type(selected["name"]) is str and re.fullmatch(r"prover-allocation-build-[0-9]{2}", selected["name"])
              and root.name == selected["name"], "REFINEMENT_BUILD_NAME")
    for role, name in (("result", "RESULT.json"), ("source_map", "source-map.json"),
                       ("command", "compile-commands.json")):
        P.require(Path(pins[role]["path"]) == root/name, "REFINEMENT_RECORD_PATH")
    P.require(Path(pins["attempt"]["path"]) == root.parent/(root.name+"-attempt.json"),
              "REFINEMENT_ATTEMPT_PATH")
    P.require(result["source_map_sha256"] == pins["source_map"]["sha256"]
              and result["commands_sha256"] == pins["command"]["sha256"], "REFINEMENT_RECORD_DIGESTS")
    P.fields(selected["sources"], ADAPTERS)
    P.fields(sources, ("adapters", "files"))
    P.require(P.encoded(sources["adapters"]) == P.encoded(selected["sources"])
              and type(sources["files"]) is dict and 1 <= len(sources["files"]) <= 512,
              "REFINEMENT_SOURCE_MAP")
    empty_evidence = []
    for relative, pin in sources["files"].items():
        _content(pin)
        path = _relative(root, relative)
        if pin["bytes"] == 0:
            # file_pin deliberately rejects empty executable inputs. The retained
            # empty build-script output is nonexecutable evidence, checked separately.
            P.require(relative.startswith("source/evidence/") and pin["sha256"] == P.hash_bytes(b""),
                      "REFINEMENT_EMPTY_EVIDENCE_ONLY")
            owner._A.absolute(path)
            P.require(path.stat().st_size == 0, "REFINEMENT_EMPTY_EVIDENCE_CHANGED")
            empty_evidence.append(path)
        else:
            owner._add(table, {"path": str(path), **pin}, 8*P.MIB)
    owner._refinement_empty_evidence = tuple(empty_evidence)
    for relative, pin in selected["sources"].items():
        _content(pin)
        P.require(sources["files"].get("source/adapters/"+relative) == pin,
                  "REFINEMENT_ADAPTER_SNAPSHOT")
    descriptor_relative = "source/adapters/software/v5/prover_memory/SOURCE.json"
    descriptor_pin = {"path": str(_relative(root, descriptor_relative)), **sources["files"][descriptor_relative]}
    P.require(descriptor_pin["sha256"] == SOURCE_SHA and result["descriptor_sha256"] == SOURCE_SHA,
              "REFINEMENT_REVIEWED_DESCRIPTOR")
    descriptor = P.parse(owner._read(descriptor_pin, P.MIB))
    preserved = descriptor["preserved"]
    P.require(preserved["aggregate_image"] == owner.support["image_id"]
              and preserved["individual_image"] == owner.profile["relation_image"]
              and preserved["foundation"] == owner.support["foundation"]
              and preserved["policy"] == owner.support["policy"], "REFINEMENT_UNCHANGED_MATHEMATICS")
    P.require(result["patch_sha256"] == descriptor["patch"]["sha256"]
              and selected["sources"][descriptor["patch"]["path"]]["sha256"] == result["patch_sha256"],
              "REFINEMENT_EXACT_PATCH")
    expected_files = {"source/adapters/"+relative: pin for relative, pin in selected["sources"].items()}
    for inventory in descriptor["sdk_source_inventories"]:
        for item in inventory["files"]:
            expected = {k: item[k] for k in ("bytes", "sha256")}
            if item["path"] == "risc0/circuit/rv32im/src/prove/preflight.rs":
                expected = {k: descriptor["expected_patched"][k] for k in ("bytes", "sha256")}
            expected_files["source/sdk/"+item["path"]] = expected
    sdk_prefix = descriptor["source"]["path"].removesuffix("risc0/circuit/rv32im/src/prove/preflight.rs")
    old_environment = None
    old_build_root = None
    retained_runtime = None
    for index, item in enumerate(descriptor["retained_records"]):
        content = {k: item[k] for k in ("bytes", "sha256")}
        evidence = "source/evidence/"+str(index).zfill(2)+"-"+PurePosixPath(item["path"]).name
        expected_files[evidence] = content
        if item["path"].startswith(sdk_prefix):
            expected_files["source/sdk/"+item["path"][len(sdk_prefix):]] = content
        if item["path"].endswith("/preflight_opt_gen.rs"):
            expected_files["generated/rv32im/preflight_opt_gen.rs"] = content
        if item["path"].endswith("small-aggregate-stage-host-build-01/environment-profile.json"):
            old_environment = P.parse(owner._read({"path": str(_relative(root, evidence)), **content}, P.MIB))
            old_build_root = str(Path(descriptor["canonical_root"])/PurePosixPath(item["path"]).parent)
        if item["path"].endswith("small-aggregate-stage-host-build-01/selection.json"):
            retained_runtime = P.parse(owner._read({"path": str(_relative(root, evidence)), **content}, P.MIB))["runtime_pins"]
        for old, fresh in (("proof-validation-integration-build-01/source-map.json", "integration"),
                           ("small-aggregate-stage-host-build-01/source-map.json", "stage")):
            if item["path"].endswith(old):
                pin = {"path": str(_relative(root, evidence)), **content}
                original_map = P.parse(owner._read(pin, P.MIB))
                P.require(type(original_map) is dict and 1 <= len(original_map) <= 256,
                          "REFINEMENT_RETAINED_SOURCE_MAP")
                for relative, row in original_map.items():
                    _relative(root, relative); _content(row)
                    expected_files["source/"+fresh+"/"+relative] = row
    P.require(P.encoded(expected_files) == P.encoded(sources["files"]), "REFINEMENT_EXACT_DERIVED_SOURCE_MAP")
    steps = descriptor["compiler_recipe"]["ordered_steps"]
    P.require(tuple(step["name"] for step in steps) == NAMES, "REFINEMENT_COMPILE_ORDER")
    commands = [{"name": step["name"], "argv": [arg.replace("${RUN}", str(root))
                 for arg in step["argv_template"]]} for step in steps]
    P.require(P.encoded(commands) == P.encoded(records["command"])
              and type(result["commands"]) is list and len(result["commands"]) == 5,
              "REFINEMENT_EXACT_FIVE_COMMANDS")
    P.fields(result["outputs"], NAMES)
    for step, command, actual in zip(steps, commands, result["commands"]):
        pin = result["outputs"][step["name"]]
        P.require(str(P.pin_fields(pin)) == step["output_template"].replace("${RUN}", str(root)),
                  "REFINEMENT_EXACT_OUTPUT_PATH")
        owner._add(table, pin)
        P.require(type(actual) is dict and actual.get("argv") == command["argv"]
                  and actual.get("cwd") == descriptor["canonical_root"]
                  and actual.get("label") == step["name"] and actual.get("status") == "COMMAND_COMPLETED"
                  and type(actual.get("exit_code")) is int and actual["exit_code"] == 0
                  and actual.get("cleanup_errors") == [], "REFINEMENT_CLEAN_COMPILE")
        P.require(_closed_job(actual["job_after"]) <= LIMITS["worker_cpu_seconds"]
                  and P.number(actual["wall_seconds"]) <= LIMITS["worker_wall_seconds"],
                  "REFINEMENT_PHASE_LIMITS")
        for dependency in step["depends_on"]:
            required = dependency+"="+result["outputs"][dependency]["path"]
            P.require(command["argv"].count(required) == 1, "REFINEMENT_NEW_LIBRARY_EDGE")
    P.require(result["executable"] == result["outputs"][NAMES[-1]], "REFINEMENT_STAGE_EXECUTABLE")
    auxiliary = {}
    for field, filename in (("environment_sha256", "environment-profile.json"), ("input_map_sha256", "INPUT-MAP.json")):
        P.digest(result[field])
        pin = P.file_pin(root/filename)
        P.require(pin["sha256"] == result[field], "REFINEMENT_BUILD_AUXILIARY_RECORD")
        owner._add(table, pin, 2*P.MIB)
        auxiliary[field] = P.parse(owner._read(pin, 2*P.MIB))
    environment, input_map = auxiliary["environment_sha256"], auxiliary["input_map_sha256"]
    P.require(old_environment is not None and type(old_environment.get("explicit_environment")) is dict,
              "REFINEMENT_RETAINED_ENVIRONMENT")
    base_env = {key: value.replace(old_build_root, str(root))
                for key, value in old_environment["explicit_environment"].items()}
    base_env.update(VCToolsUserTelemetryOptOut="1", CARGO_NET_OFFLINE="true")
    expected_environments = {}
    for step in steps:
        env = {key: value for key, value in base_env.items() if key != "OUT_DIR"
               and not key.startswith("CARGO_PKG_") and key not in ("CARGO_MANIFEST_DIR", "CARGO_MANIFEST_PATH")}
        env.update({key: value.replace("${RUN}", str(root)) for key, value in step["environment_overlay"].items()})
        expected_environments[step["name"]] = env
    P.require(P.encoded(environment.get("explicit_environment")) == P.encoded(base_env)
              and P.encoded(environment.get("step_environments")) == P.encoded(expected_environments)
              and environment.get("environment_keys_only") == sorted(base_env)
              and environment.get("no_inherited_environment") is True
              and P.encoded(environment.get("host_binaries")) == P.encoded(old_environment["host_binaries"]),
              "REFINEMENT_EXACT_COMPILER_ENVIRONMENTS")
    P.fields(input_map, ("source_inputs", "runtime_pins", "helper_pins", "trust_boundary"))
    P.require(P.encoded(input_map["runtime_pins"]) == P.encoded(selected["runtime_pins"])
              and P.encoded(selected["runtime_pins"]) == P.encoded(retained_runtime),
              "REFINEMENT_EXACT_RETAINED_RUNTIME_MAP")
    phase_jobs = result["job"].get("phase_jobs")
    P.require(type(phase_jobs) is list and len(phase_jobs) == 5, "REFINEMENT_FIVE_CLOSED_JOBS")
    for name, phase, command in zip(NAMES, phase_jobs, result["commands"]):
        P.fields(phase, ("name", "stats"))
        P.require(phase["name"] == name and _closed_job(phase["stats"]) <= LIMITS["worker_cpu_seconds"]
                  and _closed_job(command["job_before"]) == 0
                  and command["job_after"]["cpu_seconds"] <= phase["stats"]["cpu_seconds"]
                  and P.number(command["inclusive_cpu_delta"]) == command["job_after"]["cpu_seconds"],
                  "REFINEMENT_SERIAL_PHASE_ACCOUNTING")
    for key in ("cpu_seconds", "user_cpu_seconds", "kernel_cpu_seconds", "active_processes",
                "total_processes", "terminated_processes"):
        P.require(P.number(result["job"][key]) == sum(P.number(phase["stats"][key]) for phase in phase_jobs),
                  "REFINEMENT_EXACT_JOB_TOTALS")
    P.require(P.number(result["job"]["peak_job_private_commit_bytes"]) == max(
              P.number(phase["stats"]["peak_job_private_commit_bytes"]) for phase in phase_jobs),
              "REFINEMENT_SERIAL_JOB_PEAK")
    for census in (result["output_census"], result["sampled_peaks"]):
        P.uint(census["working_bytes"], LIMITS["fresh_output_bytes"])
        P.uint(census["entries"], LIMITS["fresh_output_entries"])
    P.require(_closed_job(result["job"]) <= LIMITS["total_worker_cpu_seconds"]
              and P.number(result["controller_cpu_seconds"]) <= LIMITS["controller_cpu_seconds"]
              and P.number(result["wall_seconds"]) <= LIMITS["total_wall_seconds"], "REFINEMENT_TOTAL_LIMITS")
    P.require(type(result["runtime_pin_count"]) is int and result["runtime_pin_count"] == 1071
              and type(result["runtime_pin_bytes"]) is int and result["runtime_pin_bytes"] == 2320491997
              and type(selected["runtime_pins"]) is dict and len(selected["runtime_pins"]) == 1071,
              "REFINEMENT_RETAINED_RUNTIME_MANIFEST")
    owner._check(table)
    owner._no_override(pins.values())
    return result["executable"]
