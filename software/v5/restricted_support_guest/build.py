"""Three guest compiles: native-qualified support core, aggregate, entry.

Adopt only successful guest03 module/Nanoda artifacts and its filtered library
view. No module/checker/SDK rebuild, Cargo, execution, proof or image adoption.
Historical failures and their exact original/saved selection bytes stay frozen.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import re
import shutil
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
SOURCE = ROOT / "software/v5/restricted_support_guest"
PRIOR = HERE / "restricted-guest-build-03"
TYPED = HERE / "typed-guest-build-01"
NATIVE = HERE / "restricted-support-build-01"
CONTROL = HERE / "restricted-support-controls-01"
ORIGINAL = HERE / "aggregate-guest-compile-01"
RUST = ROOT / "experiments/scale-crypto-01/runs/run-01/rust"
COMMON = ROOT / "experiments/general-checker-guest-03/common03.py"
COMMON_SHA = "97116bd269dd784b9216833f6e0c0bf38e9d08c55af5927511a13b26194133d7"
PASS = "PASS_RC_SUPPORT_GUEST_THREE_CRATE_COMPILES_ONLY"
ADAPTERS = {"software/v5/restricted_support_guest/" + name for name in ("build.py", "recipes.py")}
FRESH = {"software/v5/restricted_support/" + name for name in ("lib.rs", "syntax.rs", "typing.rs")}
REUSED = {"software/v5/restricted_composition/" + name for name in (
    "relation.rs", "foundation02.rs", "aggregate_lib.rs", "aggregate_relation.rs", "census.rs", "wire.rs")}
REUSED.update({"software/v5/aggregate_claims/" + name for name in ("header.rs", "membership.rs")})
REUSED.add("software/v5/aggregate/main.rs")
PRODUCTION = FRESH | REUSED
LIMITS = {"worker_cpu_seconds": 240, "worker_wall_seconds": 300, "memory_mib": 4096,
    "active_processes": 6, "ordinary_controller_cpu_seconds": 40, "controller_cpu_seconds": 60,
    "total_wall_seconds": 420, "fresh_output_bytes": 256 * 1024**2,
    "fresh_output_entries": 2048, "command_log_bytes": 8 * 1024**2}
RECORDS = {
    PRIOR / "RESULT.json": "44f808cdd24c2707d114675bf77a4126a805865eaae825666db0c9403e354273",
    PRIOR / "selection.json": "d110cb21351b2f07461986d971533a895011ab0da695e07c6b62175e7de85bf3",
    HERE / "restricted-guest-build-03-selection.json": "d110cb21351b2f07461986d971533a895011ab0da695e07c6b62175e7de85bf3",
    HERE / "restricted-guest-build-03-attempt.json": "c904c5fa4dce1258f1e527ea736b54823736df7073d573df3c5a644b8aec898b",
    PRIOR / "RECIPES.json": "f2c120697cde3569a5c4faf021b92096af95baa1e1ea683d11592763b24c8e74",
    PRIOR / "SOURCE-MAP.json": "7d1586b530cd1382bd5c40b75a71d804319b5f9da31ec1798dd7c34e41fcff1e",
    PRIOR / "INPUT-MAP.json": "ec9838b580641d17b25f2965fc39a11e97946d1b3f4ad959d4531f4a8480980d",
    ORIGINAL / "FINALIZATION-FAILED.json": "d0d6d8980c492d43a8927825aa153271543fa18d960305db5bde1e51c323dd54",
    NATIVE / "RESULT.json": "e26e29de72363e5c0873b9e0c307d3efaaeca4cc5e02144821446b1a06225392",
    NATIVE / "selection.json": "a6bbb29061cc301a85e258a5c9f84c6c0bd8be644ff84b389d23b6575b47e0f5",
    HERE / "restricted-support-build-01-selection.json": "a6bbb29061cc301a85e258a5c9f84c6c0bd8be644ff84b389d23b6575b47e0f5",
    HERE / "restricted-support-build-01-attempt.json": "6a1d3ff7651fa08603eb53a7f88b58dab37438912d3a36dd53d8ef6d233271a0",
    NATIVE / "source-map.json": "8920956edbe83cb4208add39feb7edf906b3c38ce5c095e5ba10f71ebcf988e7",
    CONTROL / "RESULT.json": "b1ebc2538329c08fe67509f5d50ea0ead4ac8a174973506f493d160840a27da0",
    CONTROL / "command/stdout.txt": "b9ac046a12a5131d67343596dbee9c48ad0c418fda51c2c20146af1610e6f081",
    CONTROL / "selection.json": "6f855719615335d5bb88221e90c170a5892d5ded441be0e28e2178a3d687ab35",
    HERE / "restricted-support-controls-01-selection.json": "6f855719615335d5bb88221e90c170a5892d5ded441be0e28e2178a3d687ab35",
    COMMON: COMMON_SHA,
}
MODULE_ARTIFACTS = {
    "libdmkn_module_relation.rlib": {"bytes":2349740, "sha256":"d70c585aead8afe869ce96eadde46ef7d8f31efe1bdbb717955adcff8efa4f76"},
    "libdmkn_module_relation.rmeta": {"bytes":830551, "sha256":"6b879d8fff8c09c858e0ff4f51a442a3cae33aa3551c062cf55479025ef77828"},
}
NANODA_ARTIFACTS = {
    "libnanoda_lib-7f1af4fb875deccc.rlib": {"bytes":6360054, "sha256":"8ec342c7f606b9ccf34cdd5fbf4bf86cd75f6239fd2cd025c7d837d442cf5fde"},
    "libnanoda_lib-7f1af4fb875deccc.rmeta": {"bytes":2446327, "sha256":"d5266e9ea875433bff5b2c4f084ee48f64be6d5bb6104316a44096a85cc7d62e"},
}
CONTROL_NAMES = """support_leaf_and_local_atomic support_app_union support_binder_domain_body
support_identity_interning_charge reject_unknown_support_id reject_unknown_child_id
open_closed_tree_constant_work open_direct_bvar open_nested_capture_sensitive
reject_open_larger_bvar reject_open_nested_larger_bvar open_closed_nested_binder_identity
close_direct_local close_nested_capture_sensitive close_outside_local_interval
close_inside_interval_absent close_distinct_local_node_same_serial local_type_is_atomic_for_both
depth128_closed_tree reject_depth129_open reject_depth129_close reject_open_deep_closed_child
reject_exhausted_open_budget open_exact_two_work_units reject_one_unit_open_budget
reject_partial_metadata_construction reject_nonlocal_close_target references_still_reject_unknown_constant
first_exact_baseline_j_parents_census second_exact_baseline_j_parents_census""".split()
REFUSALS = [name for name in CONTROL_NAMES if name.startswith("reject_")
            or name == "references_still_reject_unknown_constant"]


def need(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def load(name, path, digest):
    need(sha(path) == digest, "HELPER_PIN:" + str(path))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def clean_commands(report, labels):
    rows = report["commands"]
    need(report["compiler_calls"] == len(labels) == len(rows)
         and [row["label"] for row in rows] == labels
         and all(type(row.get("pid")) is int and row["status"] == "COMMAND_COMPLETED"
                 and row["exit_code"] == 0 and row["cleanup_errors"] == []
                 and row["job_after"]["active_processes"] == row["job_after"]["terminated_processes"] == 0
                 for row in rows)
         and report["job"]["active_processes"] == report["job"]["terminated_processes"] == 0,
         "ACTUAL_CLEAN_COMPILE_COMMANDS")


def main():
    started, cpu = time.monotonic(), time.process_time()
    finalizing = False

    def envelope():
        cap = LIMITS["controller_cpu_seconds"] if finalizing else LIMITS["ordinary_controller_cpu_seconds"]
        need(time.process_time() - cpu <= cap and time.monotonic() - started <= LIMITS["total_wall_seconds"],
             "RC_SUPPORT_GUEST_TOTAL_ENVELOPE")

    need(os.name == "nt" and Path.cwd() == ROOT and Path(__file__).resolve() == SOURCE / "build.py"
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize and len(sys.argv) == 3, "ISOLATED_CANONICAL_SUPPORT_GUEST_BUILD")
    selection = Path(sys.argv[1]).resolve(strict=True)
    need(selection == HERE / "restricted-support-guest-build-01-selection.json"
         and selection.stat().st_size <= 65536 and sha(selection) == sys.argv[2], "EXACT_GUEST_SELECTION")
    selection_raw = selection.read_bytes()
    need(hashlib.sha256(selection_raw).hexdigest() == sys.argv[2], "STABLE_SELECTION_BYTES")
    chosen = json.loads(selection_raw)
    need(set(chosen) == {"schema", "name", "adapters", "production_sources", "native_adoption", "limits",
         "authorizes_three_compiles_and_retained_artifact_adoption"}
         and chosen["schema"] == "DMKN_V5_RC_SUPPORT_GUEST_THREE_CRATE_BUILD_V1"
         and chosen["name"] == "restricted-support-guest-build-01" and chosen["limits"] == LIMITS
         and chosen["authorizes_three_compiles_and_retained_artifact_adoption"] is True
         and set(chosen["adapters"]) == ADAPTERS and set(chosen["production_sources"]) == PRODUCTION,
         "EXACT_SUPPORT_GUEST_SELECTION_FIELDS")
    for path, digest in RECORDS.items():
        envelope(); need(sha(path) == digest, "RETAINED_RECORD:" + str(path))
    k = load("support_guest_common", COMMON, COMMON_SHA)
    k.held.HERE = HERE
    q, a, p, c, r, job = k.helpers()
    a.DISK_LIMIT, a.ENTRY_LIMIT, r.LOG_LIMIT = (
        LIMITS["fresh_output_bytes"], LIMITS["fresh_output_entries"], LIMITS["command_log_bytes"])
    need(Path(sys.executable).resolve() == p.PYTHON and sha(p.PYTHON) == p.PYTHON_SHA
         and sha(p.PYTHON.parent / "python314.dll") == p.PYTHON_DLL_SHA, "PINNED_PYTHON")
    exact = {}

    def include(path, pin):
        need(path.is_absolute() and type(pin) is dict and set(pin) == {"bytes", "sha256"}
             and type(pin["bytes"]) is int and 0 < pin["bytes"] <= 512 * 1024**2
             and re.fullmatch(r"[0-9a-f]{64}", pin["sha256"]), "INPUT_PIN")
        need(str(path) not in exact or exact[str(path)] == pin, "CONFLICTING_INPUT_PIN")
        exact[str(path)] = dict(pin)

    digests = {**RECORDS, selection:sys.argv[2],
        ROOT / "experiments/general-checker-guest-02/common_build02.py":
            "f28d18457b2ef465b14c44dd2fec15d4386f640f9bbdf627398d5dcf46a7f11c",
        ROOT / "experiments/general-checker-guest-01/prepare.py":k.held.HOST_PREPARE_SHA,
        ROOT / "experiments/scale-equation-01/runtime.py":q.RUNTIME_SHA,
        p.PYTHON:p.PYTHON_SHA, p.PYTHON.parent / "python314.dll":p.PYTHON_DLL_SHA,
        p.HELPERS / "run_stage.py":p.HELPER_SHA, p.HELPERS / "domains.py":p.DOMAINS_SHA,
        r.VCTIP:r.VCTIP_SHA}
    digests.update({q.CRYPTO / name:digest for name,digest in q.HELPERS.items()})
    for path, digest in digests.items():
        include(path, {"bytes":path.stat().st_size, "sha256":digest})
    for relative, pin in chosen["adapters"].items():
        a.safe_parts(relative); include(ROOT / relative, pin)

    adoption = chosen["native_adoption"]
    need(type(adoption) is dict and set(adoption) == {"build", "controls_outer", "controls_inner"},
         "EXACT_NATIVE_ADOPTION_RECORDS")
    for key, path in (("build", NATIVE / "RESULT.json"), ("controls_outer", CONTROL / "RESULT.json"),
                      ("controls_inner", CONTROL / "command/stdout.txt")):
        need(adoption[key] == {"path":str(path), "bytes":path.stat().st_size, "sha256":RECORDS[path]},
             "EXACT_NATIVE_ADOPTION_PIN:" + key)
    native, outer, tested = read(NATIVE / "RESULT.json"), read(CONTROL / "RESULT.json"), read(CONTROL / "command/stdout.txt")
    native_map, native_selection = read(NATIVE / "source-map.json"), read(NATIVE / "selection.json")
    controls_selection = read(CONTROL / "selection.json")
    need(native["schema"] == "DMKN_V5_RC_SUPPORT_BUILD_RESULT_V1"
         and native["status"] == "PASS_RC_SUPPORT_TWO_COMPILES_ONLY"
         and native["selection_sha256"] == RECORDS[NATIVE / "selection.json"]
         and native_selection["sources"] == native_map and len(native_map) == 8
         and read(HERE / "restricted-support-build-01-attempt.json") == {
             "status":native["status"], "result_sha256":RECORDS[NATIVE / "RESULT.json"]}
         and all(native[name] == 0 for name in ("checker_rebuilds", "module_rebuilds", "dependency_rebuilds",
             "baseline_rebuilds", "aggregate_rebuilds", "test_calls", "native_calls", "guest_calls", "proof_calls", "network_calls")),
         "ACTUAL_NATIVE_SUPPORT_BUILD")
    clean_commands(native, ["support-core", "support-controls"])
    control_job = outer["result"]
    need(outer["schema"] == "DMKN_V5_LOCAL_CHECK_RESULT_V1"
         and outer["selection_sha256"] == RECORDS[CONTROL / "selection.json"]
         and control_job["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and control_job["child_exit_code"] == 0
         and control_job["direct_child_reaped"] is True and control_job["job_closed"] is True
         and control_job["termination_requested"] is False and control_job["cleanup_errors"] == []
         and control_job["final_job"]["active_processes"] == control_job["final_job"]["terminated_processes"] == 0,
         "ACTUAL_CLEAN_NATIVE_CONTROLS_OUTER")
    binary = NATIVE / "restricted_support_controls.exe"
    binary_pin = native["outputs"][binary.name]
    need(binary_pin["path"] == str(binary)
         and controls_selection["runtime_pins"][str(binary)] == binary_pin["sha256"]
         and controls_selection["runtime_pins"][str(NATIVE / "RESULT.json")] == RECORDS[NATIVE / "RESULT.json"]
         and all(controls_selection["sources"][name] == pin["sha256"] for name,pin in native_map.items()),
         "CONTROL_BINARY_AND_QUALIFIED_NATIVE_SOURCE_BINDING")
    include(binary, {field:binary_pin[field] for field in ("bytes", "sha256")})
    need(tested["schema"] == "DMKN_RC_SUPPORT_CONTROLS_V1" and tested["status"] == "PASS"
         and tested["errors"] == [] and tested["executed_count"] == len(CONTROL_NAMES) == 30
         and [row["name"] for row in tested["executed"]] == CONTROL_NAMES
         and all(row["status"] == "PASS" for row in tested["executed"])
         and tested["expected_refusals"] == REFUSALS and len(REFUSALS) == 12
         and tested["crypto_produced"] is False and tested["global_growth_claim"] is False
         and tested["guest_calls"] == tested["proof_calls"] == 0
         and tested["authority"] == "NATIVE_CONDITIONAL_CONTROLS_NOT_RECEIPT_AUTHORITY",
         "ACTUAL_THIRTY_NATIVE_SUPPORT_CONTROLS_NOT_CERTIFICATION")
    for row, expected_j in zip(tested["executed"][-2:], (
            "0ba261cd27c816223aa56bc6cbe217e67f48264b8d1c707326095492620a1657",
            "dce99babfd2e4e579c2981e6461e4b80c2f794da53b0959eb7494ee1f7c82d86")):
        detail = row["detail"]
        need(detail["journal_sha256"] == expected_j and detail["parent_count"] == 1
             and detail["support_work"] < detail["baseline_work"]
             and detail["signed_work_removed"] == detail["baseline_work"] - detail["support_work"],
             "EXACT_NATIVE_ENDPOINT_AND_WORK_DISCRIMINATOR")

    prior, prior_map, prior_inputs = read(PRIOR / "RESULT.json"), read(PRIOR / "SOURCE-MAP.json"), read(PRIOR / "INPUT-MAP.json")
    retained_recipes = read(PRIOR / "RECIPES.json")
    need(prior["schema"] == "DMKN_V5_RC_GUEST_FOUR_CRATE_BUILD_RESULT_V1"
         and prior["status"] == "PASS_RC_GUEST_FOUR_CRATE_COMPILES_ONLY"
         and prior["selection_sha256"] == RECORDS[PRIOR / "selection.json"] and prior["module_compiles"] == 1
         and read(HERE / "restricted-guest-build-03-attempt.json") == {
             "status":prior["status"], "result_sha256":RECORDS[PRIOR / "RESULT.json"]}
         and prior_map["project"] == prior_map["compiler_read_sources"]
         and prior_map["project"] == read(PRIOR / "selection.json")["production_sources"]
         and len(prior_map["project"]) == 21
         and [row["argv"] for row in prior["commands"]] == [row["argv"] for row in retained_recipes["recipes"]],
         "ACTUAL_SUCCESSFUL_GUEST03_ADOPTION")
    clean_commands(prior, ["module", "rc-core", "aggregate", "guest"])
    module_argv = retained_recipes["recipes"][0]["argv"]
    project_externs = [module_argv[index + 1] for index,arg in enumerate(module_argv) if arg == "--extern"
                      and module_argv[index + 1].startswith(("dmkn_", "nanoda_lib="))]
    need(project_externs == ["nanoda_lib=" + str(PRIOR / "retained/projects/libnanoda_lib-7f1af4fb875deccc.rlib")],
         "RETAINED_MODULE_HAS_NO_RC_OR_AGGREGATE_DEPENDENCY")
    need(read(ORIGINAL / "FINALIZATION-FAILED.json") == {"status":"FAIL_FINALIZATION",
         "overrides_result_and_attempt":True, "result_sha256":"81cce68d9b20f22b12d12d5d698084eb8eb101493de71c6e35cd6acb7b44f47a",
         "error":"REMAINING_TOTAL_ENVELOPE"}, "ORIGINAL_FAILED_OPERATION_PRESERVED")
    project_map = {name:native_map[name] for name in FRESH}
    project_map.update({name:prior_map["project"][name] for name in REUSED})
    need(chosen["production_sources"] == project_map and len(project_map) == 12
         and all(project_map[name] == native_map[name] for name in REUSED & set(native_map)),
         "EXACT_NATIVE_QUALIFIED_TWELVE_SOURCE_CLOSURE")
    for relative,pin in project_map.items():
        a.safe_parts(relative); include(ROOT / relative, pin)
    for name,pin in MODULE_ARTIFACTS.items():
        need(prior["outputs"][name] == {"path":str(PRIOR / "outputs" / name), **pin}, "ADOPTED_MODULE_ARTIFACT")
        include(PRIOR / "outputs" / name, pin)
    need(prior_inputs["copied_project_artifacts"] == NANODA_ARTIFACTS, "ADOPTED_NANODA_PAIR")
    for name,pin in NANODA_ARTIFACTS.items():
        include(PRIOR / "retained/projects" / name, pin)
    copied = prior_inputs["existing_dependency_files"]
    need(prior_inputs["existing_dependency_view"] == str(TYPED / "retained")
         and len(copied) == 236 and sum(pin["bytes"] for pin in copied.values()) == 311693039,
         "EXACT_EXISTING_236_LIBRARY_VIEW")
    for relative,pin in copied.items():
        parts = Path(relative).parts
        need(len(parts) == 2 and parts[0] in ("libraries", "macros")
             and "dmkn_" not in parts[1] and "nanoda" not in parts[1], "FILTERED_LIBRARY_RELATIVE_PATH")
        include(TYPED / "retained" / relative, pin)
    compiler = {name:pin for name,pin in prior_inputs["inputs"].items() if Path(name).is_relative_to(RUST)}
    need(len(compiler) == 26 and sum(pin["bytes"] for pin in compiler.values()) == 395093004,
         "EXACT_RETAINED_26_COMPILER_INPUTS")
    for name,pin in compiler.items():
        include(Path(name), pin)
    plan = load("support_guest_recipes", SOURCE / "recipes.py",
                chosen["adapters"]["software/v5/restricted_support_guest/recipes.py"]["sha256"])
    run, attempt = HERE / chosen["name"], HERE / (chosen["name"] + "-attempt.json")
    need(not run.exists() and not attempt.exists() and not run.is_symlink() and not run.is_junction()
         and not attempt.is_symlink(), "FRESH_SUPPORT_GUEST_OUTPUT")
    recipes = plan.commands(retained_recipes, run)
    source_copied, module_copied = False, False

    def bind(path, pin):
        envelope()
        need(path.resolve(strict=True) == path and path.is_file(), "CANONICAL_INPUT_PATH")
        a.regular_stat(path, allow_hardlinks=True)
        need(path.stat().st_size == pin["bytes"] and sha(path) == pin["sha256"], "INPUT_CHANGED:" + str(path))
        envelope()

    def rebind():
        for name,pin in exact.items():
            bind(Path(name), pin)
        for directory in (NATIVE, CONTROL, PRIOR, TYPED):
            need(not (directory / "FINALIZATION-FAILED.json").exists(), "NO_OVERRIDING_FINALIZATION_FAILURE")
        need(c.file_map(TYPED / "retained") == copied, "NO_EXTRA_RETAINED_SAME_NAME_LIBRARIES")
        need(c.file_map(PRIOR / "retained/projects") == NANODA_ARTIFACTS, "EXACT_EXISTING_NANODA_VIEW")
        if source_copied:
            need(c.file_map(run / "project") == project_map, "EXACT_GUEST_SOURCE_SNAPSHOT")
            need(sha(run / "selection.json") == sys.argv[2], "SAVED_SELECTION_CHANGED")
        if module_copied:
            need(c.file_map(run / "retained/modules") == MODULE_ARTIFACTS, "EXACT_TWO_ADOPTED_MODULE_ARTIFACT_VIEW")

    rebind()
    run.mkdir()
    phase = None
    report = {"schema":"DMKN_V5_RC_SUPPORT_GUEST_THREE_CRATE_BUILD_RESULT_V1", "status":"FAIL",
        "selection_sha256":sys.argv[2], "limits":LIMITS, "source_snapshot":str(run / "project"),
        "native_adoption":adoption, "selected_source_files":12, "production_source_closure_files":12,
        "original_operation_effective_status":"FAIL_FINALIZATION",
        "retained_module_adoption":{"path":str(PRIOR / "RESULT.json"), "sha256":RECORDS[PRIOR / "RESULT.json"]},
        "retained_nanoda_adoption":{"path":str(PRIOR / "RESULT.json"), "sha256":RECORDS[PRIOR / "RESULT.json"]},
        "source_closure_scope":"DECLARED_STATIC_SOURCE_CLOSURE_NOT_DEPINFO_OBSERVATION",
        "cargo_calls":0, "graph_commands":0, "dependency_compiles":0, "compiler_calls":0,
        "checker_compiles":0, "module_compiles":0, "guest_calls":0, "proof_calls":0,
        "image_assembly_calls":0, "network_calls":0,
        "authority":"THREE_RECONSTRUCTED_PROFILE_CRATE_COMPILES_ONLY"}

    class Budget:
        def __init__(self):
            self.current, self.peak = {}, {"working_bytes":0, "entries":0}
        def refresh(self):
            envelope(); self.current = c.census(run)
            need(self.current["working_bytes"] <= LIMITS["fresh_output_bytes"]
                 and self.current["entries"] <= LIMITS["fresh_output_entries"], "FRESH_OUTPUT_ENVELOPE")
            for key in self.peak:
                self.peak[key] = max(self.peak[key], self.current[key])
    budget = Budget()
    try:
        (run / "commands").mkdir(); (run / "outputs").mkdir()
        with (run / "selection.json").open("xb") as stream:
            need(stream.write(selection_raw) == len(selection_raw), "EXACT_SELECTION_COPY")
        for relative,pin in project_map.items():
            target = run / "project" / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            with (ROOT / relative).open("rb") as source, target.open("xb") as dest:
                shutil.copyfileobj(source, dest, 1024**2)
            bind(target, pin)
        source_copied = True
        (run / "retained/modules").mkdir(parents=True)
        for name,pin in MODULE_ARTIFACTS.items():
            target = run / "retained/modules" / name
            with (PRIOR / "outputs" / name).open("rb") as source, target.open("xb") as dest:
                shutil.copyfileobj(source, dest, 1024**2)
            bind(target, pin)
        module_copied = True
        rebind()
        a.save(run / "INPUT-MAP.json", {"inputs":exact, "existing_dependency_view":str(TYPED / "retained"),
            "existing_dependency_files":copied, "copied_module_artifacts":MODULE_ARTIFACTS,
            "existing_nanoda_view":str(PRIOR / "retained/projects"), "existing_nanoda_files":NANODA_ARTIFACTS})
        a.save(run / "SOURCE-MAP.json", {"source_snapshot":str(run / "project"), "project":project_map,
            "compiler_read_sources":project_map, "adapters":chosen["adapters"]})
        a.save(run / "RECIPES.json", {"schema":"DMKN_V5_RC_SUPPORT_GUEST_THREE_CRATE_RECIPES_V1",
            "basis":"RECONSTRUCTED_EQUIVALENT_PROFILE_NOT_CAPTURED_CARGO_ARGV", "recipes":recipes})
        env, environment = p.environment(run, RUST)
        env["VCToolsUserTelemetryOptOut"] = "1"
        environment.update(explicit_environment=env, source_snapshot=str(run / "project"),
            cargo_invocations=0, existing_dependency_files=236, existing_nanoda_files=2, copied_artifact_files=2,
            copied_artifact_bytes=sum(pin["bytes"] for pin in MODULE_ARTIFACTS.values()))
        a.save(run / "environment-profile.json", environment)

        class InclusiveJob(job.Job):
            def stats(self):
                measured = super().stats()
                if not finalizing:
                    need(measured["cpu_seconds"] <= 240, "SHARED_INCLUSIVE_CPU")
                return measured

        def exact_job(seconds, memory, active_processes):
            need(seconds == 300 and memory == 4096 and active_processes == 8, "RETAINED_PHASE_SHAPE")
            return InclusiveJob(240, 4096, active_processes=6)

        budget.refresh()
        phase = r.phase_class(p,a)("rc-support-guest-three-crates", run, budget, env, exact_job, 300)
        outputs = {}
        for recipe in recipes:
            phase.invoke(recipe["label"], recipe["argv"], ROOT, allow_build_telemetry=True)
            for name in (recipe["output"], recipe["metadata_output"]):
                if name is not None:
                    path = Path(name)
                    need(path.is_file() and path.parent == run / "outputs", "EXACT_GUEST_OUTPUT")
                    outputs[path.name] = a.pin(path)
        binary, link_map = Path(recipes[-1]["output"]), run / "guest-link.map"
        need(len(outputs) == 5 and link_map.is_file() and link_map.stat().st_size <= 32*1024**2, "FIVE_OUTPUTS_AND_LINK_MAP_BOUND")
        symbols = link_map.read_text(encoding="utf-8")
        need(re.search(r"\b_start\b", symbols) and re.search(r"\b__start\b", symbols), "SDK_STARTUP_SYMBOLS")
        artifact = {"user_elf":a.pin(binary), "elf_headers":k.elf_summary(binary), "link_map":a.pin(link_map)}
        a.save(run / "ARTIFACT.json", artifact)
        report.update(status=PASS, outputs=outputs, artifact=artifact)
    except BaseException as error:
        report["error"] = type(error).__name__ + ": " + str(error)[:4000]
    finally:
        finalizing = True
        if phase is not None:
            try:
                phase.close()
                need(phase.final_stats["active_processes"] == phase.final_stats["terminated_processes"] == 0
                     and phase.final_stats["cpu_seconds"] <= 240, "FINAL_CLEAN_BOUNDED_JOB")
            except BaseException as error:
                report.update(status="FAIL_CLEANUP", cleanup_error=str(error)[:2000])
            report["job"], report["commands"] = getattr(phase, "final_stats", None), phase.commands
            report["compiler_calls"] = sum(type(row.get("pid")) is int for row in phase.commands)
            report["module_compiles"] = sum(row.get("label") == "module" and type(row.get("pid")) is int
                                            for row in phase.commands)
        try:
            rebind(); budget.refresh()
            if report["status"] == PASS:
                clean_commands(report, ["rc-core", "aggregate", "guest"])
                need(report["compiler_calls"] == 3 and report["module_compiles"] == 0, "THREE_COMPILERS_NO_MODULE_REBUILD")
        except BaseException as error:
            report.update(status="FAIL_FINAL_CHECK", final_error=str(error)[:3000])
        report.update(controller_cpu_seconds=time.process_time()-cpu, wall_seconds=time.monotonic()-started,
            output_census=budget.current, sampled_peaks=budget.peak,
            accounting="DISJOINT_CONTROLLER_WORKER;FINAL_REPORT_EXIT_TAIL_EXCLUDED")
        a.save(run / "RESULT.json", report)
        a.save(attempt, {"status":report["status"], "result_sha256":sha(run / "RESULT.json")})
        try:
            budget.refresh()
        except BaseException as error:
            report.update(status="FAIL_FINALIZATION", finalization_error=str(error)[:3000])
            a.save(run / "FINALIZATION-FAILED.json", {"status":"FAIL_FINALIZATION", "overrides_result_and_attempt":True,
                "result_sha256":sha(run / "RESULT.json"), "error":str(error)[:3000]})
    print(json.dumps({key:report.get(key) for key in ("status", "error", "wall_seconds")}))
    return 0 if report["status"] == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
