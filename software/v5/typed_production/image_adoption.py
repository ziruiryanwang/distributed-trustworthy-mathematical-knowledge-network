"""Adopt the exact retained typed guest build and assembled A* image.

This is an owner-selected historical evidence bridge, not a generic image
registry or mathematical/cryptographic verification. It neither rebuilds nor
executes any artifact. The selected image remains independently checked by the
stage host and, ultimately, by a receipt consumer.
"""
from pathlib import Path, PurePosixPath
import re

from production import producer as P

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
IMAGE_ID = "9d5072a67f5ab2c4f9468df03c2424d71c457021c4b442d7739c5a3d51ba2865"
RECORDS = {
    "result": {"relative_path": "experiments/v5-local-checks/typed-guest-image-assembly-01/assembly/RESULT.json",
        "bytes": 1749, "sha256": "4c26d075d850ff38a0922dbbdfad00303d16b49dee41f71a859f3777166e530c"},
    "outer": {"relative_path": "experiments/v5-local-checks/typed-guest-image-assembly-01/RESULT.json",
        "bytes": 2268, "sha256": "174878e768ed578e0a4f239de8423591ebf4ea34f09213e52c84aff46362b33b"},
    "selection": {"relative_path": "experiments/v5-local-checks/typed-guest-image-assembly-01/selection.json",
        "bytes": 24056, "sha256": "d911dbfd934b5e43c2743403076afd47794185a593f225582f1bfb73ab025362"},
    "guest_build": {"relative_path": "experiments/v5-local-checks/typed-guest-build-01/RESULT.json",
        "bytes": 32917, "sha256": "b1b4f7a82aabddc5dd3349a4f82ba79e846517a6db94c3a3d911702c7d6576a4"},
    "guest_selection": {"relative_path": "experiments/v5-local-checks/typed-guest-build-01/selection.json",
        "bytes": 266700, "sha256": "bab4fd3e335683be859a1f38843b415eff13a2dcb9c215c931ae1d6f463911e3"},
    "guest_source_map": {"relative_path": "experiments/v5-local-checks/typed-guest-build-01/SOURCE-MAP.json",
        "bytes": 12526, "sha256": "a05c6e910664260b05c4c875ea0df6545a4dd969b608f22a3b9585e590885356"},
    "artifact": {"relative_path": "experiments/v5-local-checks/typed-guest-build-01/ARTIFACT.json",
        "bytes": 1220, "sha256": "f1d732f34287a63096f816fcc62f0724a470f6dc3dc725ae6b816787e08800ff"},
    "guest_attempt": {"relative_path": "experiments/v5-local-checks/typed-guest-build-01-attempt.json",
        "bytes": 147, "sha256": "b807f0c299f40fa509a63099d2e75b4a92bf941062c60376bcf378a9657dc6e7"},
    "guest_recipes": {"relative_path": "experiments/v5-local-checks/typed-guest-build-01/RECIPES.json",
        "bytes": 22823, "sha256": "fa11546f7fe58c752f58830429760c3958566ca36b6da7051fe2142306fa0ac5"},
    "assembly_command": {"relative_path": "experiments/v5-local-checks/typed-guest-image-assembly-01/assembly/COMMAND.json",
        "bytes": 19000, "sha256": "9aa845df63ab85be75b4d54d2f3be94ee23d2dcd9580c825f662f9e3e60d2145"},
}
BUILD_PASS = "PASS_TYPED_GUEST_FOUR_CRATE_COMPILES_ONLY"
PROJECTS = ("nanoda_lib", "dmkn_module_relation", "dmkn_aggregate_relation", "dmkn-aggregate-claim-guest")
LABELS = ("checker", "module", "aggregate", "guest")
LIMITS = {"worker_cpu_seconds": 240, "worker_wall_seconds": 300, "memory_mib": 4096,
    "active_processes": 6, "ordinary_controller_cpu_seconds": 40, "controller_cpu_seconds": 60,
    "total_wall_seconds": 420, "fresh_output_bytes": 512*P.MIB,
    "fresh_output_entries": 4096, "command_log_bytes": 8*P.MIB}


def _relative(base, name):
    P.require(type(name) is str and "\\" not in name and ":" not in name, "TYPED_IMAGE_RELATIVE_PATH")
    path = PurePosixPath(name)
    P.require(path.parts and not path.is_absolute() and all(x not in ("", ".", "..") for x in path.parts)
              and path.as_posix() == name, "TYPED_IMAGE_RELATIVE_PATH")
    return base.joinpath(*path.parts)


def _retain(owner, pin, maximum=8*P.MIB, allow_empty=False):
    P.fields(pin, ("path", "bytes", "sha256"))
    P.uint(pin["bytes"], maximum); P.digest(pin["sha256"])
    if pin["bytes"] == 0:
        P.require(allow_empty and pin["sha256"] == P.hash_bytes(b""), "TYPED_EMPTY_LOG_ONLY")
        path = Path(pin["path"])
        owner._A.absolute(path)
        P.require(path.stat().st_size == 0, "TYPED_EMPTY_LOG_CHANGED")
        existing = getattr(owner, "_refinement_empty_evidence", ())
        owner._refinement_empty_evidence = tuple(dict.fromkeys((*existing, path)))
    else:
        owner._add(owner._pins, pin, maximum)


def _closed(job):
    P.require(type(job) is dict and type(job.get("active_processes")) is int
              and job["active_processes"] == 0 and type(job.get("terminated_processes")) is int
              and job["terminated_processes"] == 0, "TYPED_BUILD_JOB_CLOSURE")
    return P.number(job["cpu_seconds"])


def adopt_image(owner):
    pins = owner.profile["image_adoption"]
    P.fields(pins, RECORDS)
    for role, expected in RECORDS.items():
        path = _relative(ROOT, expected["relative_path"])
        P.require(P.pin_fields(pins[role], 2*P.MIB) == path
                  and pins[role]["bytes"] == expected["bytes"]
                  and pins[role]["sha256"] == expected["sha256"], "TYPED_EXACT_RETAINED_IMAGE_RECORD")
    r = owner._records(pins, RECORDS, owner._pins)
    owner._local_outer(r["outer"], r["selection"], pins["selection"], pins["outer"])
    result, guest = r["result"], r["guest_build"]
    P.fields(result, ("artifact_record", "assembler_calls", "authority", "exit_code", "guest_build_result",
        "guest_executions", "image", "image_id", "image_id_origin", "logs", "mathematical_admission",
        "proof_calls", "schema", "selection_sha256", "status"))
    P.require(result["schema"] == "DMKN_V5_TYPED_GUEST_IMAGE_ASSEMBLY_RESULT_V1"
              and result["status"] == "PASS_NEW_AGGREGATE_IMAGE_ASSEMBLY_ONLY"
              and result["image_id"] == owner.support["image_id"] == IMAGE_ID
              and result["image_id_origin"] == "ACTUAL_PINNED_ASSEMBLER_NOT_FILE_SHA256"
              and result["mathematical_admission"] is False
              and result["guest_build_result"] == pins["guest_build"]
              and result["artifact_record"] == pins["artifact"], "TYPED_ADOPTED_IMAGE_ASSEMBLY")
    for name, value in (("assembler_calls", 1), ("exit_code", 0), ("guest_executions", 0), ("proof_calls", 0)):
        P.require(type(result[name]) is int and result[name] == value, "TYPED_ASSEMBLY_SCOPE")
    build_root = Path(pins["guest_build"]["path"]).parent
    assembly_root = Path(pins["result"]["path"]).parent
    outer_root = Path(pins["outer"]["path"]).parent
    P.require(guest["schema"] == "DMKN_V5_TYPED_GUEST_FOUR_CRATE_BUILD_RESULT_V1"
              and guest["status"] == BUILD_PASS
              and guest["selection_sha256"] == result["selection_sha256"] == pins["guest_selection"]["sha256"]
              and guest["artifact"] == r["artifact"]
              and r["guest_attempt"] == {"status": BUILD_PASS, "result_sha256": pins["guest_build"]["sha256"]},
              "TYPED_GUEST_BUILD_CHAIN")
    for name, value in (("compiler_calls", 4), ("checker_compiles", 1), ("cargo_calls", 0),
                        ("graph_commands", 0), ("dependency_compiles", 0), ("guest_calls", 0),
                        ("proof_calls", 0), ("image_assembly_calls", 0), ("network_calls", 0)):
        P.require(type(guest[name]) is int and guest[name] == value, "TYPED_BUILD_SCOPE")
    P.require(_closed(guest["job"]) <= LIMITS["worker_cpu_seconds"]
              and P.number(guest["controller_cpu_seconds"]) <= LIMITS["controller_cpu_seconds"]
              and P.number(guest["wall_seconds"]) <= LIMITS["total_wall_seconds"], "TYPED_BUILD_LIMITS")
    selection, sources = r["guest_selection"], r["guest_source_map"]
    P.fields(selection, ("schema", "name", "adapters", "production_sources", "retained_artifacts",
                        "authorizes_four_compiles_and_retained_artifact_adoption", "limits"))
    P.fields(sources, ("source_snapshot", "project", "compiler_read_sources", "adapters"))
    P.require(selection["schema"] == "DMKN_V5_TYPED_GUEST_FOUR_CRATE_BUILD_V1"
              and selection["name"] == build_root.name
              and selection["authorizes_four_compiles_and_retained_artifact_adoption"] is True
              and P.encoded(selection["limits"]) == P.encoded(guest["limits"]) == P.encoded(LIMITS)
              and sources["source_snapshot"] == guest["source_snapshot"] == str(build_root/"project")
              and sources["project"] == selection["production_sources"]
              and sources["adapters"] == selection["adapters"], "TYPED_SOURCE_MAP_CHAIN")
    P.require(type(sources["project"]) is dict and len(sources["project"]) == 37
              and "software/v5/bounded_parse/census.rs" in sources["project"]
              and sources["compiler_read_sources"] == {key: value for key, value in sources["project"].items()
                  if key != "software/v5/bounded_parse/census.rs"}
              and type(selection["retained_artifacts"]) is dict and len(selection["retained_artifacts"]) == 236,
              "TYPED_DECLARED_SOURCE_CLOSURE")
    P.fields(sources["adapters"], ("software/v5/typed_guest/build.py", "software/v5/typed_guest/recipes.py"))
    command = r["assembly_command"]
    P.fields(command, ("argv", "cwd", "timeout_seconds", "selected_inputs", "guest_result_sha256",
                       "absent_failure_marker", "authority"))
    P.require(type(command["selected_inputs"]) is list and len(command["selected_inputs"]) == 70,
              "TYPED_ASSEMBLY_INPUT_COUNT")
    selected_inputs = {}
    for pin in command["selected_inputs"]:
        P.fields(pin, ("path", "bytes", "sha256"))
        P.uint(pin["bytes"], 128*P.MIB); P.digest(pin["sha256"])
        owner._A.absolute(Path(pin["path"]))
        P.require(pin["path"] not in selected_inputs, "TYPED_DUPLICATE_ASSEMBLY_INPUT")
        selected_inputs[pin["path"]] = pin

    def selected(pin, maximum=8*P.MIB, allow_empty=False):
        P.require(selected_inputs.get(pin["path"]) == pin, "TYPED_ASSEMBLY_INPUT_LINK")
        _retain(owner, pin, maximum, allow_empty)

    for role in ("guest_build", "guest_selection", "guest_source_map", "artifact", "guest_attempt", "guest_recipes"):
        selected(pins[role])
    for base, entries in ((build_root/"project", sources["project"]), (ROOT, sources["adapters"])):
        for relative, pin in entries.items():
            P.fields(pin, ("bytes", "sha256"))
            selected({"path": str(_relative(base, relative)), **pin}, 2*P.MIB)
    for relative, sha in r["selection"]["sources"].items():
        pin = P.file_pin(_relative(outer_root/"sources", relative))
        P.require(pin["sha256"] == sha, "TYPED_ASSEMBLY_ADAPTER_SNAPSHOT")
        _retain(owner, pin, 2*P.MIB)
    recipes = r["guest_recipes"]
    P.fields(recipes, ("schema", "basis", "recipes"))
    P.require(recipes["schema"] == "DMKN_V5_TYPED_GUEST_FOUR_CRATE_RECIPES_V1"
              and recipes["basis"] == "RECONSTRUCTED_EQUIVALENT_PROFILE_NOT_CAPTURED_CARGO_ARGV"
              and type(recipes["recipes"]) is list and len(recipes["recipes"]) == 4
              and [row["name"] for row in recipes["recipes"]] == list(PROJECTS)
              and type(guest["commands"]) is list and len(guest["commands"]) == 4,
              "TYPED_FOUR_RECIPES")
    expected_outputs = {PROJECTS[-1]} | {"lib"+name+ext for name in PROJECTS[:3] for ext in (".rlib", ".rmeta")}
    P.fields(guest["outputs"], expected_outputs)
    for label, recipe, actual in zip(LABELS, recipes["recipes"], guest["commands"]):
        P.require(actual["label"] == label and actual["status"] == "COMMAND_COMPLETED"
                  and type(actual["exit_code"]) is int and actual["exit_code"] == 0
                  and actual["cleanup_errors"] == [] and actual["argv"] == recipe["argv"]
                  and actual["cwd"] == str(ROOT) and type(actual["pid"]) is int and actual["pid"] > 0
                  and _closed(actual["job_after"]) <= LIMITS["worker_cpu_seconds"]
                  and P.number(actual["wall_seconds"]) <= LIMITS["worker_wall_seconds"], "TYPED_CLOSED_COMPILE")
        saved = selected_inputs[str(build_root/"commands"/label/"command.json")]
        selected(saved)
        P.require(P.parse(owner._read(saved, 2*P.MIB)) == actual, "TYPED_ACTUAL_COMMAND_RECORD")
        P.require(type(actual["logs"]) is list and len(actual["logs"]) == 2
                  and {pin["path"] for pin in actual["logs"]} ==
                      {str(build_root/"commands"/label/name) for name in ("stdout.txt", "stderr.txt")},
                  "TYPED_BUILD_LOG_PATHS")
        for pin in actual["logs"]:
            selected(pin, 8*P.MIB, True)
        name = recipe["name"]
        binary = name == PROJECTS[-1]
        output = str(build_root/"outputs"/(name if binary else "lib"+name+".rlib"))
        metadata = None if binary else str(build_root/"outputs"/("lib"+name+".rmeta"))
        P.require(recipe["output"] == output and recipe["metadata_output"] == metadata, "TYPED_RECIPE_OUTPUTS")
    # Old compiler/library inputs remain exactly committed build provenance.
    # They are not executed by a producer and need not be rescanned each stage.
    for name, pin in guest["outputs"].items():
        P.require(P.pin_fields(pin, 64*P.MIB) == build_root/"outputs"/name
                  and selected_inputs.get(pin["path"]) == pin, "TYPED_OUTPUT_LINEAGE")
    artifact = r["artifact"]
    P.fields(artifact, ("user_elf", "elf_headers", "link_map"))
    P.require(artifact["user_elf"] == guest["outputs"][PROJECTS[-1]]
              and artifact["elf_headers"]["bytes"] == artifact["user_elf"]["bytes"]
              and artifact["elf_headers"]["sha256"] == artifact["user_elf"]["sha256"]
              and P.pin_fields(artifact["link_map"], 32*P.MIB) == build_root/"guest-link.map",
              "TYPED_ELF_ARTIFACT_CHAIN")
    selected(artifact["user_elf"], 64*P.MIB); selected(artifact["link_map"], 32*P.MIB)
    argv = command["argv"]
    P.require(type(argv) is list and len(argv) == 5 and argv[1] == "assemble"
              and argv[2] == artifact["user_elf"]["path"]
              and argv[4] == result["image"]["path"] == str(assembly_root/"aggregate_image.bin")
              and argv[0] in selected_inputs and argv[3] in selected_inputs
              and command["cwd"] == str(ROOT) and type(command["timeout_seconds"]) is int
              and command["timeout_seconds"] == 60 and command["guest_result_sha256"] == pins["guest_build"]["sha256"]
              and command["absent_failure_marker"] == str(build_root/"FINALIZATION-FAILED.json"),
              "TYPED_EXACT_ASSEMBLY_COMMAND")
    outer_argv = r["outer"]["result"]["argv"]
    P.require(outer_argv.count("--guest-result") == outer_argv.count("--guest-result-sha256") == 1
              and outer_argv[outer_argv.index("--guest-result")+1] == pins["guest_build"]["path"]
              and outer_argv[outer_argv.index("--guest-result-sha256")+1] == pins["guest_build"]["sha256"],
              "TYPED_OUTER_EXACT_BUILD")
    P.require(type(result["logs"]) is list and len(result["logs"]) == 2
              and [pin["path"] for pin in result["logs"]] ==
                  [str(assembly_root/name) for name in ("stdout.txt", "stderr.txt")]
              and result["logs"][1]["bytes"] == 0, "TYPED_ASSEMBLY_LOGS")
    for pin in result["logs"]:
        _retain(owner, pin, 65536, True)
    match = re.fullmatch(rb"COMBINED_IMAGE image_id=([0-9a-f]{64}) bytes=([0-9]+)\r?\n?",
                         owner._read(result["logs"][0], 65536))
    P.require(match is not None and match[1].decode("ascii") == IMAGE_ID
              and int(match[2]) == result["image"]["bytes"], "TYPED_ASSEMBLER_IMAGE_ID_NOT_FILE_HASH")
    _retain(owner, result["image"], 64*P.MIB)
    owner._no_override(pins.values())
    owner._check(owner._pins)
    owner._image = dict(result["image"])
