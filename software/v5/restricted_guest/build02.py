"""Three RC guest compiles, reusing adopted target libraries without rebuild.

Root must separately select a fresh invocation after actual native controls.
No Cargo, checker/SDK rebuild, guest execution, proof or image adoption occurs.
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
SOURCE = ROOT / "software/v5/restricted_guest"
TYPED = HERE / "typed-guest-build-01"
ORIGINAL = HERE / "aggregate-guest-compile-01"
NATIVE = HERE / "restricted-composition-build-02"
CONTROL = HERE / "restricted-composition-controls-01"
RUST = ROOT / "experiments/scale-crypto-01/runs/run-01/rust"
TYPED_HELPER = ROOT / "software/v5/typed_guest/build.py"
TYPED_HELPER_SHA = "95903977ce10180480587163102a3c7c4ce98df9191dee93072be71747b2a9ba"
PASS = "PASS_RC_GUEST_THREE_CRATE_COMPILES_ONLY"
ADAPTERS = {"software/v5/restricted_guest/" + name for name in ("build02.py", "recipes02.py")}
PRODUCTION = {"software/v5/restricted_composition/" + name for name in (
    "lib02.rs", "syntax.rs", "foundation02.rs", "typing.rs", "relation.rs",
    "aggregate_lib.rs", "aggregate_relation.rs", "census.rs", "wire.rs")}
PRODUCTION.update({"software/v5/aggregate_claims/" + name for name in ("header.rs", "membership.rs")})
ENTRY = "software/v5/aggregate/main.rs"
PRODUCTION.add(ENTRY)
LIMITS = {"worker_cpu_seconds": 240, "worker_wall_seconds": 300, "memory_mib": 4096,
    "active_processes": 6, "ordinary_controller_cpu_seconds": 40, "controller_cpu_seconds": 60,
    "total_wall_seconds": 420, "fresh_output_bytes": 256 * 1024**2,
    "fresh_output_entries": 2048, "command_log_bytes": 8 * 1024**2}
RECORDS = {
    TYPED / "RESULT.json": "b1b4f7a82aabddc5dd3349a4f82ba79e846517a6db94c3a3d911702c7d6576a4",
    TYPED / "INPUT-MAP.json": "f2942f0462044b79d7cc37edf387772d6e442cc0cebd3c3dde342182c6dfa12c",
    TYPED / "SOURCE-MAP.json": "a05c6e910664260b05c4c875ea0df6545a4dd969b608f22a3b9585e590885356",
    TYPED / "RECIPES.json": "fa11546f7fe58c752f58830429760c3958566ca36b6da7051fe2142306fa0ac5",
    TYPED / "selection.json": "bab4fd3e335683be859a1f38843b415eff13a2dcb9c215c931ae1d6f463911e3",
    HERE / "typed-guest-build-01-attempt.json": "b807f0c299f40fa509a63099d2e75b4a92bf941062c60376bcf378a9657dc6e7",
    ORIGINAL / "RESULT.json": "81cce68d9b20f22b12d12d5d698084eb8eb101493de71c6e35cd6acb7b44f47a",
    ORIGINAL / "SOURCE-MAP.json": "75c710e3ee13f63cb6ef44da8656caa53c300bf649317d2b5669d8b9cde06ce0",
    HERE / "aggregate-guest-compile-01-attempt.json": "5e0b848fbd32c7b3dd58962658d90c3fb76771a2a3d58229acb7f9a1e63251b0",
    HERE / "proof-validation-integration-build-01/source-map.json":
        "a5693f19236bb8051e476d9f61d8d2449cbcd023054a1e9c8606607049957f2a",
    TYPED_HELPER: TYPED_HELPER_SHA,
}
PROJECT_ARTIFACTS = {
    "libdmkn_module_relation-c98240db3a2d8c8d.rlib": {"bytes":2349140, "sha256":"fd75a524f44440099b7472700f2c31015fd48fba1a3f70a9e0ca32a183918fd4"},
    "libdmkn_module_relation-c98240db3a2d8c8d.rmeta": {"bytes":830820, "sha256":"2c46b5e0a3f18610f0ab1235f34426492249a47b2c08c3529b029bfa15a5c740"},
    "libnanoda_lib-7f1af4fb875deccc.rlib": {"bytes":6360054, "sha256":"8ec342c7f606b9ccf34cdd5fbf4bf86cd75f6239fd2cd025c7d837d442cf5fde"},
    "libnanoda_lib-7f1af4fb875deccc.rmeta": {"bytes":2446327, "sha256":"d5266e9ea875433bff5b2c4f084ee48f64be6d5bb6104316a44096a85cc7d62e"},
}


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


def main():
    started, cpu = time.monotonic(), time.process_time()
    finalizing = False

    def envelope():
        cap = LIMITS["controller_cpu_seconds"] if finalizing else LIMITS["ordinary_controller_cpu_seconds"]
        need(time.process_time() - cpu <= cap and time.monotonic() - started <= LIMITS["total_wall_seconds"],
             "RC_BUILD_TOTAL_ENVELOPE")

    need(os.name == "nt" and Path.cwd() == ROOT and Path(__file__).resolve() == SOURCE / "build02.py"
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize and len(sys.argv) == 3, "ISOLATED_CANONICAL_RC_GUEST_BUILD")
    selection = Path(sys.argv[1]).resolve(strict=True)
    need(selection.parent == HERE and selection.stat().st_size <= 65536 and sha(selection) == sys.argv[2],
         "EXACT_GUEST_SELECTION")
    chosen = read(selection)
    need(set(chosen) == {"schema", "name", "adapters", "production_sources", "native_adoption", "limits",
         "authorizes_three_compiles_and_retained_artifact_adoption"}
         and chosen["schema"] == "DMKN_V5_RC_GUEST_THREE_CRATE_BUILD_V1"
         and chosen["name"] == "restricted-guest-build-02" and chosen["limits"] == LIMITS
         and chosen["authorizes_three_compiles_and_retained_artifact_adoption"] is True
         and set(chosen["adapters"]) == ADAPTERS and set(chosen["production_sources"]) == PRODUCTION,
         "EXACT_RC_GUEST_SELECTION_FIELDS")
    for path, digest in RECORDS.items():
        envelope(); need(sha(path) == digest, "RETAINED_RECORD:" + str(path))
    t = load("rc_retained_build_helpers", TYPED_HELPER, TYPED_HELPER_SHA)
    k = load("rc_guest_common", t.COMMON, t.COMMON_SHA)
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

    digests = {**RECORDS, selection:sys.argv[2], t.COMMON:t.COMMON_SHA,
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
    records = {}
    for key, expected in (("build", NATIVE / "RESULT.json"),
            ("controls_outer", CONTROL / "RESULT.json"), ("controls_inner", CONTROL / "evidence/result.json")):
        pin = adoption[key]
        need(type(pin) is dict and set(pin) == {"path", "bytes", "sha256"} and pin["path"] == str(expected),
             "EXACT_NATIVE_ADOPTION_PATH:" + key)
        include(expected, {field:pin[field] for field in ("bytes", "sha256")})
        need(expected.stat().st_size == pin["bytes"] and sha(expected) == pin["sha256"], "NATIVE_ADOPTION_PIN")
        records[key] = read(expected)
    native, outer, inner = records["build"], records["controls_outer"], records["controls_inner"]
    need(native["status"] == "PASS_RC_THREE_COMPILES_ONLY"
         and native["job"]["active_processes"] == native["job"]["terminated_processes"] == 0
         and all(native[name] == 0 for name in ("checker_rebuilds", "module_rebuilds", "dependency_rebuilds",
                                               "test_calls", "native_calls", "guest_calls", "proof_calls", "network_calls")),
         "ACTUAL_CLEAN_NATIVE_BUILD")
    result = outer["result"]
    need(result["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and result["child_exit_code"] == 0
         and result["direct_child_reaped"] is True and result["job_closed"] is True
         and result["termination_requested"] is False
         and result["final_job"]["active_processes"] == result["final_job"]["terminated_processes"] == 0,
         "ACTUAL_CLEAN_NATIVE_CONTROLS_OUTER")
    tested = inner["native"]
    cases = tested["executed"]
    names = [case["name"] for case in cases]
    refusals = tested["expected_refusals"]
    need(inner["schema"] == "DMKN_RC_CONTROL_RUN_V1" and inner["status"] == "PASS" and inner["exit_code"] == 0
         and inner["test_binary_sha256"] == native["outputs"]["restricted_controls.exe"]["sha256"]
         and all(inner[name] == 0 for name in ("guest_calls", "proof_calls", "network_calls"))
         and tested["schema"] == "DMKN_RC0_CONTROLS_V1" and tested["status"] == "PASS" and tested["errors"] == []
         and tested["executed_count"] == len(names) == len(set(names)) == 40
         and all(case["status"] == "PASS" for case in cases)
         and len(refusals) == len(set(refusals)) == 26 and set(refusals) <= set(names)
         and {"first_exact_original_refinement", "second_exact_original_refinement", "exact_foundation_signature_projection",
              "raw_imax_zero_comparison_is_root_only", "conditional_two_delta_target_closure"} <= set(names)
         and tested["crypto_produced"] is False and tested["global_growth_claim"] is False,
         "ACTUAL_RC_NATIVE_CONTROLS_NOT_CERTIFICATION")
    for path in (NATIVE / "source-map.json", NATIVE / "selection.json",
            HERE / (NATIVE.name + "-selection.json"),
            HERE / (NATIVE.name + "-attempt.json"), CONTROL / "selection.json"):
        # These exact records are cross-bound below to the already selected
        # terminal results, never adopted because they merely exist.
        include(path, {"bytes":path.stat().st_size, "sha256":sha(path)})
    native_selection = read(NATIVE / "selection.json")
    native_map = read(NATIVE / "source-map.json")
    need(sha(HERE / (NATIVE.name + "-selection.json")) == native["selection_sha256"]
         and native_selection == read(HERE / (NATIVE.name + "-selection.json"))
         and native_map == native_selection["sources"]
         and read(HERE / (NATIVE.name + "-attempt.json")) == {
             "status":native["status"], "result_sha256":adoption["build"]["sha256"]}
         and sha(CONTROL / "selection.json") == outer["selection_sha256"], "NATIVE_SAVED_SELECTION_BINDING")
    old_map = read(ORIGINAL / "SOURCE-MAP.json")
    project_map = {name:native_map[name] for name in PRODUCTION if name != ENTRY}
    project_map[ENTRY] = old_map["project"][ENTRY]
    need(chosen["production_sources"] == project_map, "EXACT_QUALIFIED_12_SOURCE_CLOSURE")
    original_native_map = read(HERE / "proof-validation-integration-build-01/source-map.json")
    for name in ("canonical", "commitments", "journal", "policy", "relation", "lib"):
        relative = "software/v5/modules/receipt/src/" + name + ".rs"
        need(original_native_map[relative] == old_map["project"][relative], "NATIVE_GUEST_RETAINED_MODULE_SOURCE:" + name)
    for relative, pin in project_map.items():
        a.safe_parts(relative); include(ROOT / relative, pin)

    typed_result, original_result = read(TYPED / "RESULT.json"), read(ORIGINAL / "RESULT.json")
    for directory, observed, expected_status in ((TYPED, typed_result, "PASS_TYPED_GUEST_FOUR_CRATE_COMPILES_ONLY"),
            (ORIGINAL, original_result, "PASS_OPTIMIZED_EXACT_WARRANT_AGGREGATE_GUEST_COMPILE_ONLY")):
        need(observed["status"] == expected_status and observed["job"]["active_processes"] == 0
             and observed["job"]["terminated_processes"] == 0
             and read(HERE / (directory.name + "-attempt.json")) == {
                 "status":expected_status, "result_sha256":RECORDS[directory / "RESULT.json"]}, "ADOPTED_RETAINED_BUILD")
    typed_inputs = read(TYPED / "INPUT-MAP.json")
    copied = typed_inputs["copied_artifacts"]
    need(len(copied) == 236 and sum(pin["bytes"] for pin in copied.values()) == 311693039,
         "EXACT_EXISTING_236_LIBRARY_VIEW")
    for relative, pin in copied.items():
        parts = Path(relative).parts
        need(len(parts) == 2 and parts[0] in ("libraries", "macros"), "FILTERED_LIBRARY_RELATIVE_PATH")
        include(TYPED / "retained" / relative, pin)
    original_libdir = ORIGINAL / "target/riscv32im-risc0-zkvm-elf/release/deps"
    for name, pin in PROJECT_ARTIFACTS.items():
        include(original_libdir / name, pin)
    compiler = {name:pin for name,pin in old_map["retained"]["runtime"].items()
        if name in {"bin/rustc.exe", "lib/rustlib/x86_64-pc-windows-msvc/bin/rust-lld.exe"}
        or (name.startswith("bin/") and name.endswith(".dll"))
        or (name.startswith("lib/rustlib/x86_64-pc-windows-msvc/lib/") and name.endswith((".rlib", ".rmeta")))}
    need(len(compiler) == 26 and sum(pin["bytes"] for pin in compiler.values()) == 395093004,
         "EXACT_RETAINED_26_COMPILER_INPUTS")
    for name,pin in compiler.items():
        a.safe_parts(name); include(RUST / name, pin)
    plan = load("rc_guest_recipes", SOURCE / "recipes02.py", chosen["adapters"]["software/v5/restricted_guest/recipes02.py"]["sha256"])
    run, attempt = HERE / chosen["name"], HERE / (chosen["name"] + "-attempt.json")
    need(not run.exists() and not attempt.exists(), "FRESH_RC_GUEST_OUTPUT")
    recipes = plan.commands(read(TYPED / "RECIPES.json"), run)
    source_copied, project_copied = False, False

    def bind(path, pin):
        envelope()
        need(path.resolve(strict=True) == path and path.is_file(), "CANONICAL_INPUT_PATH")
        a.regular_stat(path, allow_hardlinks=True)
        need(path.stat().st_size == pin["bytes"] and sha(path) == pin["sha256"], "INPUT_CHANGED:" + str(path))
        envelope()

    def rebind():
        for name,pin in exact.items():
            bind(Path(name), pin)
        for directory in (NATIVE, TYPED, ORIGINAL, CONTROL):
            need(not (directory / "FINALIZATION-FAILED.json").exists(), "NO_OVERRIDING_FINALIZATION_FAILURE")
        need(c.file_map(TYPED / "retained") == copied, "NO_EXTRA_RETAINED_SAME_NAME_LIBRARIES")
        if source_copied:
            need(c.file_map(run / "project") == project_map, "EXACT_GUEST_SOURCE_SNAPSHOT")
            need(sha(run / "selection.json") == sys.argv[2], "SAVED_SELECTION_CHANGED")
        if project_copied:
            need(c.file_map(run / "retained/projects") == PROJECT_ARTIFACTS, "EXACT_FOUR_PROJECT_ARTIFACT_VIEW")

    rebind()
    run.mkdir()
    phase = None
    report = {"schema":"DMKN_V5_RC_GUEST_THREE_CRATE_BUILD_RESULT_V1", "status":"FAIL",
        "selection_sha256":sys.argv[2], "limits":LIMITS, "source_snapshot":str(run / "project"),
        "native_adoption":adoption, "selected_source_files":12, "production_source_closure_files":12,
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
        raw_selection = selection.read_bytes()
        need(hashlib.sha256(raw_selection).hexdigest() == sys.argv[2], "SELECTION_COPY_CHANGED")
        with (run / "selection.json").open("xb") as stream:
            stream.write(raw_selection)
        for relative,pin in project_map.items():
            target = run / "project" / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            with (ROOT / relative).open("rb") as source, target.open("xb") as dest:
                shutil.copyfileobj(source, dest, 1024**2)
            bind(target, pin)
        source_copied = True
        (run / "retained/projects").mkdir(parents=True)
        for name,pin in PROJECT_ARTIFACTS.items():
            target = run / "retained/projects" / name
            with (original_libdir / name).open("rb") as source, target.open("xb") as dest:
                shutil.copyfileobj(source, dest, 1024**2)
            bind(target, pin)
        project_copied = True
        rebind()
        a.save(run / "INPUT-MAP.json", {"inputs":exact, "existing_dependency_view":str(TYPED / "retained"),
            "existing_dependency_files":copied, "copied_project_artifacts":PROJECT_ARTIFACTS})
        a.save(run / "SOURCE-MAP.json", {"source_snapshot":str(run / "project"), "project":project_map,
            "compiler_read_sources":project_map, "adapters":chosen["adapters"]})
        a.save(run / "RECIPES.json", {"schema":"DMKN_V5_RC_GUEST_THREE_CRATE_RECIPES_V1",
            "basis":"RECONSTRUCTED_EQUIVALENT_PROFILE_NOT_CAPTURED_CARGO_ARGV", "recipes":recipes})
        env, environment = p.environment(run, RUST)
        env["VCToolsUserTelemetryOptOut"] = "1"
        environment.update(explicit_environment=env, source_snapshot=str(run / "project"),
            cargo_invocations=0, existing_dependency_files=236, copied_artifact_files=4,
            copied_artifact_bytes=sum(pin["bytes"] for pin in PROJECT_ARTIFACTS.values()))
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
        phase = r.phase_class(p,a)("rc-guest-three-crates", run, budget, env, exact_job, 300)
        outputs = {}
        for recipe in recipes:
            phase.invoke(recipe["label"], recipe["argv"], ROOT, allow_build_telemetry=True)
            for name in (recipe["output"], recipe["metadata_output"]):
                if name is not None:
                    path = Path(name)
                    need(path.is_file() and path.parent == run / "outputs", "EXACT_GUEST_OUTPUT")
                    outputs[path.name] = a.pin(path)
        binary, link_map = Path(recipes[-1]["output"]), run / "guest-link.map"
        need(link_map.is_file() and link_map.stat().st_size <= 32*1024**2, "LINK_MAP_BOUND")
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
        try:
            rebind(); budget.refresh()
            if report["status"] == PASS:
                need(report["compiler_calls"] == 3, "THREE_ACTUALLY_LAUNCHED_COMPILERS")
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
