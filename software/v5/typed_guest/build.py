"""Four typed guest compiles using a strict copied retained-library view.

No Cargo, graph rerun, SDK/std/dependency compile, guest execution or proof.
Failed operations remain failed. Retained dependency adoption is explicit.
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
SOURCE = ROOT / "software/v5/typed_guest"
PRIOR = HERE / "bounded-parse-direct-build-01"
CONTROLS = HERE / "typed-rows-controls-01"
NATIVE = HERE / "typed-rows-build-02"
SNAPSHOT = HERE / "bounded-parse-guest-build-02"
OLD = HERE / "aggregate-guest-compile-01"
RUST = ROOT / "experiments/scale-crypto-01/runs/run-01/rust"
COMMON = ROOT / "experiments/general-checker-guest-03/common03.py"
COMMON_SHA = "97116bd269dd784b9216833f6e0c0bf38e9d08c55af5927511a13b26194133d7"
PASS = "PASS_TYPED_GUEST_FOUR_CRATE_COMPILES_ONLY"
ADAPTERS = {"software/v5/typed_guest/build.py",
            "software/v5/typed_guest/recipes.py"}
LIMITS = {"worker_cpu_seconds": 240, "worker_wall_seconds": 300, "memory_mib": 4096,
    "active_processes": 6, "ordinary_controller_cpu_seconds": 40, "controller_cpu_seconds": 60,
    "total_wall_seconds": 420, "fresh_output_bytes": 512*1024**2,
    "fresh_output_entries": 4096, "command_log_bytes": 8*1024**2}
RECORDS = {
    PRIOR / "RESULT.json": "694d205b63082ecd02536eb70b16ae08a271f06d66d5df95f296a51a607ce22b",
    PRIOR / "selection.json": "3f92ea98aa873580929a446635e426717f6d0efe1a1b1a91e272e21ab7eb9bc6",
    PRIOR / "SOURCE-MAP.json": "35387a79067d4868e02076c71c9128b1695fe0371524493f87e28de51fa19c3e",
    PRIOR / "RECIPES.json": "e6fc21c18e114cc280f7a5fe9bba3beafedae31309e87f940c970ec89ec38510",
    PRIOR / "INPUT-MAP.json": "1977a89a3936ecd3916f889f52b6590e215897df1c377213c073498e82fb353c",
    SNAPSHOT / "UNIT-GRAPH.json": "142224e56a81b3d73960a0aa5c5f80360658ccf0f1bff06883152cbfe92511fe",
    OLD / "commands/build-aggregate-guest/stdout.txt": "8e54baefabfa6abc5461af0b6a9b126960203df9bf4e45ae9a9feccd4ad0328b",
    OLD / "SOURCE-MAP.json": "75c710e3ee13f63cb6ef44da8656caa53c300bf649317d2b5669d8b9cde06ce0",
    OLD / "environment-profile.json": "7e1b195a0e075eec9ba8f0d7f8e65c83a9a3cebfc3332e7910d9909be2581ff5",
    NATIVE / "RESULT.json": "add627e4fe4bdc102c79eeea745233d95cbfd56f48f58b118fe276adb6c00794",
    NATIVE / "source-map.json": "c0d929c6cea7d3b27744abd88ff6d2f29e899627033680db2b60772196df2e9d",
    NATIVE / "selection.json": "b4da69c0b7b925415931f11adb31c690d2f0ae18f57edddc4b74fcbd44d57cb4",
    HERE / "typed-rows-build-02-selection.json": "0eaf0bd562b1d501412e415394d4ce33acb2c20c44df028bca64bbdfa24846a3",
    HERE / "typed-rows-build-02-attempt.json": "9581679aee618dafd95781bbd6570c1e2c043294f0971e2d0361c3539c534e2f",
    CONTROLS / "RESULT.json": "bbdceb54b828f79c017481da542d4a2834763932b3c07da4fab544c34dd41b72",
    CONTROLS / "evidence/RESULT.json": "daeb9f2f242ef1a027d54c1b16a330b1a4e0e63e6dce0d797eeb88bc8084c71e",
    CONTROLS / "selection.json": "4c648a97e777e0c2bcdf547f80107fb9bcdcea8e7a265c07874fe7c6ce361700",
    COMMON: COMMON_SHA,
}
TYPED_SOURCES = {"software/v5/typed_rows/" + name + ".rs" for name in (
    "rows", "decode", "checker_lib", "module_correspondence", "parser",
    "foundation_static", "module_relation", "module_lib", "census",
    "aggregate_relation", "aggregate_lib")}
REUSED_SOURCES = {"software/v5/modules/receipt/src/" + name + ".rs" for name in (
    "input", "foundation_data", "commitments", "journal", "policy")}
REUSED_SOURCES.update({"software/v5/aggregate_claims/" + name + ".rs"
                      for name in ("header", "membership", "wire")})
REUSED_SOURCES.update({"software/v5/bounded_parse/" + name + ".rs"
                      for name in ("canonical", "module_relation", "census")})
REUSED_SOURCES.add("software/v5/modules/native/proof_memo/module_correspondence.rs")
REUSED_SOURCES.update({"software/v5/modules/native/checker/src/" + name + ".rs" for name in (
    "debug_printer", "demand", "env", "expr", "inductive", "level", "module", "name",
    "pretty_printer", "quot", "tc", "unique_hasher", "util")})
ENTRY = "software/v5/aggregate/main.rs"
SUPPORT_ONLY = "software/v5/bounded_parse/census.rs"



def need(value, reason):
    if not value:
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
             "DIRECT_BUILD_TOTAL_ENVELOPE")

    need(os.name == "nt" and Path.cwd() == ROOT and Path(__file__).resolve() == SOURCE / "build.py"
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize and len(sys.argv) == 3, "ISOLATED_CANONICAL_DIRECT_BUILD")
    clearance = Path(sys.argv[1]).resolve(strict=True)
    need(clearance.parent == HERE and clearance.stat().st_size <= 1024**2
         and sha(clearance) == sys.argv[2], "EXACT_DIRECT_SELECTION")
    chosen = read(clearance)
    need(set(chosen) == {"schema", "name", "adapters", "production_sources",
         "retained_artifacts", "limits", "authorizes_four_compiles_and_retained_artifact_adoption"}
         and chosen["schema"] == "DMKN_V5_TYPED_GUEST_FOUR_CRATE_BUILD_V1"
         and chosen["name"] == "typed-guest-build-01" and chosen["limits"] == LIMITS
         and chosen["authorizes_four_compiles_and_retained_artifact_adoption"] is True
         and type(chosen["adapters"]) is dict and set(chosen["adapters"]) == ADAPTERS, "SELECTION_FIELDS")
    for path, digest in RECORDS.items():
        envelope()
        need(sha(path) == digest, "RETAINED_EVIDENCE_PIN:" + str(path))
    prior = read(PRIOR / "RESULT.json")
    need(prior["status"] == "PASS_BOUNDED_PARSE_THREE_PROJECT_COMPILES_ONLY"
         and prior["job"]["active_processes"] == prior["job"]["terminated_processes"] == 0
         and not (PRIOR / "FINALIZATION-FAILED.json").exists(), "ADOPTED_CLOSED_PRIOR_BUILD")
    native = read(NATIVE / "RESULT.json")
    need(native["status"] == "PASS_TYPED_ROWS_FOUR_COMPILES_ONLY"
         and native["job"]["active_processes"] == native["job"]["terminated_processes"] == 0
         and native["selection_sha256"] == RECORDS[HERE / "typed-rows-build-02-selection.json"]
         and not (NATIVE / "FINALIZATION-FAILED.json").exists()
         and read(HERE / "typed-rows-build-02-attempt.json") == {
             "status": native["status"], "result_sha256": RECORDS[NATIVE / "RESULT.json"]},
         "ADOPTED_CLOSED_TYPED_NATIVE_BUILD")
    native_selection = read(NATIVE / "selection.json")
    need(native_selection == read(HERE / "typed-rows-build-02-selection.json"),
         "EXACT_NATIVE_SELECTION_SEMANTICS")
    outer, inner = read(CONTROLS / "RESULT.json"), read(CONTROLS / "evidence/RESULT.json")
    need(outer["result"]["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED"
         and outer["result"]["child_exit_code"] == 0
         and outer["result"]["direct_child_reaped"] is True
         and outer["result"]["job_closed"] is True
         and outer["result"]["termination_requested"] is False
         and outer["result"]["final_job"]["active_processes"] == 0
         and outer["result"]["final_job"]["terminated_processes"] == 0
         and outer["selection_sha256"] == RECORDS[CONTROLS / "selection.json"]
         and inner["status"] == "PASS" and inner["exit_code"] == 0
         and inner["guest_calls"] == inner["proof_calls"] == 0
         and len(inner["passed_tests"]) == len(set(inner["passed_tests"])) == 8
         and inner["test_binary_sha256"] == native["outputs"]["typed_rows_tests.exe"]["sha256"],
         "ADOPTED_EIGHT_TYPED_NATIVE_CONTROLS_ONLY")
    prior_map = read(PRIOR / "SOURCE-MAP.json")
    need(prior_map["source_snapshot"] == str(SNAPSHOT / "project"),
         "EXACT_RETAINED_SOURCE_ORIGIN")
    native_map = read(NATIVE / "source-map.json")
    need(native_map == native_selection["sources"] and len(native_map) == 39,
         "EXACT_ADOPTED_TYPED_NATIVE_SOURCE_MAP")
    project_map = {name: pin for name, pin in native_map.items()
                   if name in TYPED_SOURCES | REUSED_SOURCES}
    need(set(project_map) == TYPED_SOURCES | REUSED_SOURCES and len(project_map) == 36,
         "EXACT_36_TYPED_AND_FALLBACK_SOURCES")
    project_map[ENTRY] = prior_map["project"][ENTRY]
    need(chosen["production_sources"] == project_map and len(project_map) == 37,
         "EXACT_37_SELECTED_PRODUCTION_SOURCES")
    # The native differential census is selected retained support, not a
    # production compiler-read claim. Every actual guest source is still pinned.
    source_roots = {name: pin for name, pin in project_map.items() if name != SUPPORT_ONLY}
    source_inputs = {name: ROOT / name for name in project_map}
    plan = load("typed_guest_recipes", SOURCE / "recipes.py",
                chosen["adapters"]["software/v5/typed_guest/recipes.py"]["sha256"])
    graph = read(SNAPSHOT / "UNIT-GRAPH.json")
    raw_rows = (OLD / "commands/build-aggregate-guest/stdout.txt").read_text(encoding="utf-8").splitlines()
    # This exact pinned non-verbose predecessor is all JSON. Never use the
    # mixed plain/JSON -vv output from failed02 with this parser.
    retained_files, libraries = plan.dependencies([json.loads(line) for line in raw_rows if line])
    adopted_artifacts = read(PRIOR / "selection.json")["retained_artifacts"]
    need(type(chosen["retained_artifacts"]) is dict
         and set(chosen["retained_artifacts"]) == set(retained_files)
         and all(adopted_artifacts.get(name) == pin for name, pin in chosen["retained_artifacts"].items()),
         "EXACT_236_ADOPTED_LIBRARY_FILES")
    run, attempt = HERE / chosen["name"], HERE / (chosen["name"] + "-attempt.json")
    need(not run.exists() and not attempt.exists(), "FRESH_DIRECT_OUTPUT")
    recipes = plan.commands(graph, run, retained_files, libraries, read(OLD / "environment-profile.json")["guest_rustflags"])
    old_map = read(OLD / "SOURCE-MAP.json")
    compiler = {name: pin for name, pin in old_map["retained"]["runtime"].items()
        if name in {"bin/rustc.exe", "lib/rustlib/x86_64-pc-windows-msvc/bin/rust-lld.exe"}
        or (name.startswith("bin/") and name.endswith(".dll"))
        or (name.startswith("lib/rustlib/x86_64-pc-windows-msvc/lib/") and name.endswith((".rlib", ".rmeta")))}
    need(len(compiler) == 26 and sum(pin["bytes"] for pin in compiler.values()) == 395093004,
         "EXACT_26_COMPILER_INPUTS_NO_CARGO")
    k = load("typed_guest_common", COMMON, COMMON_SHA)
    k.held.HERE = HERE
    q, a, p, c, r, job = k.helpers()
    a.DISK_LIMIT, a.ENTRY_LIMIT, r.LOG_LIMIT = (
        LIMITS["fresh_output_bytes"], LIMITS["fresh_output_entries"], LIMITS["command_log_bytes"])
    digests = {**RECORDS, clearance: sys.argv[2],
        ROOT / "experiments/general-checker-guest-02/common_build02.py":
            "f28d18457b2ef465b14c44dd2fec15d4386f640f9bbdf627398d5dcf46a7f11c",
        ROOT / "experiments/general-checker-guest-01/prepare.py": k.held.HOST_PREPARE_SHA,
        ROOT / "experiments/scale-equation-01/runtime.py": q.RUNTIME_SHA,
        p.PYTHON: p.PYTHON_SHA, p.PYTHON.parent / "python314.dll": p.PYTHON_DLL_SHA,
        p.HELPERS / "run_stage.py": p.HELPER_SHA, p.HELPERS / "domains.py": p.DOMAINS_SHA,
        r.VCTIP: r.VCTIP_SHA}
    digests.update({q.CRYPTO / name: digest for name, digest in q.HELPERS.items()})
    exact = {}

    def include(path, pin):
        need(path.is_absolute() and type(pin) is dict and set(pin) == {"bytes", "sha256"}
             and type(pin["bytes"]) is int and 0 < pin["bytes"] <= 512*1024**2
             and re.fullmatch(r"[0-9a-f]{64}", pin["sha256"]), "INPUT_PIN")
        need(str(path) not in exact or exact[str(path)] == pin, "INPUT_PIN_CONFLICT")
        exact[str(path)] = dict(pin)

    for base, rows in ((ROOT, chosen["adapters"]), (RUST, compiler)):
        for relative, pin in rows.items():
            a.safe_parts(relative)
            include(base / relative, pin)
    for name, pin in project_map.items():
        include(source_inputs[name], pin)
    for name, pin in chosen["retained_artifacts"].items():
        include(Path(name), pin)
    need(sum(pin["bytes"] for pin in chosen["retained_artifacts"].values()) == 311693039
         and sum(chosen["retained_artifacts"][name]["bytes"] for name in retained_files
                 if retained_files[name].startswith("libraries/")) == 272519407, "EXACT_LIBRARY_VIEW_BYTES")
    for path, digest in digests.items():
        include(path, {"bytes": path.stat().st_size, "sha256": digest})
    copied, source_copied = False, False
    copy_map = {relative: chosen["retained_artifacts"][name] for name, relative in retained_files.items()}

    def bind(path, pin):
        envelope()
        need(path.resolve(strict=True) == path and path.is_file(), "CANONICAL_INPUT_PATH")
        a.regular_stat(path, allow_hardlinks=True)
        need(path.stat().st_size == pin["bytes"] and sha(path) == pin["sha256"], "INPUT_CHANGED:" + str(path))
        envelope()

    def rebind():
        for name, pin in exact.items():
            bind(Path(name), pin)
        need(not (PRIOR / "FINALIZATION-FAILED.json").exists()
             and not (NATIVE / "FINALIZATION-FAILED.json").exists(),
             "ADOPTED_BUILDS_HAVE_NO_OVERRIDE")
        if source_copied:
            need(c.file_map(run / "project") == project_map, "EXACT_37_SOURCE_SNAPSHOT")
        if copied:
            for relative, pin in copy_map.items():
                bind(run / "retained" / relative, pin)
            need(c.file_map(run / "retained") == copy_map, "NO_UNSELECTED_SAME_NAME_LIBRARY")
            need(sha(run / "selection.json") == sys.argv[2], "SAVED_SELECTION_CHANGED")

    rebind()
    run.mkdir()
    phase = None
    result = {"schema": "DMKN_V5_TYPED_GUEST_FOUR_CRATE_BUILD_RESULT_V1", "status": "FAIL",
        "selection_sha256": sys.argv[2], "limits": LIMITS,
        "source_snapshot": str(run / "project"),
        "prior_build_result_sha256": RECORDS[PRIOR / "RESULT.json"],
        "prior_source_map_sha256": RECORDS[PRIOR / "SOURCE-MAP.json"],
        "native_typed_build_result_sha256": RECORDS[NATIVE / "RESULT.json"],
        "native_typed_source_map_sha256": RECORDS[NATIVE / "source-map.json"],
        "functional_control_result_sha256": RECORDS[CONTROLS / "evidence/RESULT.json"],
        "control_outer_result_sha256": RECORDS[CONTROLS / "RESULT.json"],
        "control_outer_status": "COMMAND_EXITED_ZERO_AND_CLOSED",
        "functional_controls_disposition": "EIGHT_ADOPTED_NATIVE_COMPARISONS_NOT_GUEST_PERFORMANCE",
        "selected_source_files": 37, "production_source_closure_files": 36,
        "support_only_sources": [SUPPORT_ONLY],
        "source_closure_scope": "DECLARED_STATIC_SOURCE_CLOSURE_NOT_DEPINFO_OBSERVATION",
        "cargo_calls": 0, "graph_commands": 0, "dependency_compiles": 0, "compiler_calls": 0,
        "checker_compiles": 0, "guest_calls": 0, "proof_calls": 0,
        "image_assembly_calls": 0, "network_calls": 0,
        "authority": "FOUR_RECONSTRUCTED_PROFILE_CRATE_COMPILES_ONLY"}

    class Budget:
        def __init__(self):
            self.current, self.peak = {}, {"working_bytes": 0, "entries": 0}
        def refresh(self):
            envelope()
            self.current = c.census(run)
            envelope()
            need(self.current["working_bytes"] <= LIMITS["fresh_output_bytes"]
                 and self.current["entries"] <= LIMITS["fresh_output_entries"], "FRESH_OUTPUT_LIMIT")
            for key in self.peak:
                self.peak[key] = max(self.peak[key], self.current[key])

    budget = Budget()
    try:
        (run / "commands").mkdir()
        (run / "outputs").mkdir()
        raw_selection = clearance.read_bytes()
        need(hashlib.sha256(raw_selection).hexdigest() == sys.argv[2], "SELECTION_COPY_CHANGED")
        with (run / "selection.json").open("xb") as stream:
            stream.write(raw_selection)
        for name, pin in project_map.items():
            envelope()
            target = run / "project" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            with source_inputs[name].open("rb") as source, target.open("xb") as dest:
                shutil.copyfileobj(source, dest, 1024**2)
            bind(target, pin)
        source_copied = True
        need(c.file_map(run / "project") == project_map, "EXACT_PRODUCTION_SOURCE_MIRROR")
        for name, relative in retained_files.items():
            envelope()
            target = run / "retained" / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            with Path(name).open("rb") as source, target.open("xb") as dest:
                shutil.copyfileobj(source, dest, 1024**2)
            bind(target, chosen["retained_artifacts"][name])
        copied = True
        need(c.file_map(run / "retained") == copy_map, "EXACT_FILTERED_COPY_VIEW")
        a.save(run / "INPUT-MAP.json", {"inputs": exact, "copied_artifacts": copy_map})
        a.save(run / "SOURCE-MAP.json", {"source_snapshot": str(run / "project"),
            "project": project_map, "compiler_read_sources": source_roots, "adapters": chosen["adapters"]})
        a.save(run / "RECIPES.json", {"schema": "DMKN_V5_TYPED_GUEST_FOUR_CRATE_RECIPES_V1",
            "basis": "RECONSTRUCTED_EQUIVALENT_PROFILE_NOT_CAPTURED_CARGO_ARGV", "recipes": recipes})
        a.save(run / "GRAPH-COMPARISON.json", {"schema": "DMKN_V5_TYPED_GUEST_RETAINED_GRAPH_PROJECTION_V1",
            "retained_graph_sha256": RECORDS[SNAPSHOT / "UNIT-GRAPH.json"],
            "source_changes": sorted(TYPED_SOURCES), "package_feature_profile_edge_changes": 0,
            "new_compilation_units": [item["name"] for item in recipes], "new_cargo_graph_commands": 0})
        env, environment = p.environment(run, RUST)
        env["VCToolsUserTelemetryOptOut"] = "1"
        # The selected roots and expanded SDK/json macros read no Cargo env.
        # serde_derive's version token is already baked into the retained DLL.
        # Keep the complete private invocation environment recorded nonetheless.
        environment.update(explicit_environment=env, source_snapshot=str(run / "project"),
                           cargo_invocations=0, copied_artifact_files=236, copied_artifact_bytes=311693039)
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
        phase = r.phase_class(p, a)("typed-guest-four-crates", run, budget, env, exact_job, 300)
        outputs = {}
        for index, recipe in enumerate(recipes):
            phase.invoke(("checker", "module", "aggregate", "guest")[index], recipe["argv"], ROOT,
                         allow_build_telemetry=True)
            for name in (recipe["output"], recipe["metadata_output"]):
                if name is not None:
                    path = Path(name)
                    need(path.is_file() and path.parent == run / "outputs", "EXACT_PROJECT_OUTPUT")
                    outputs[path.name] = a.pin(path)
        binary = Path(recipes[-1]["output"])
        link_map = run / "guest-link.map"
        need(link_map.is_file() and link_map.stat().st_size <= 32*1024**2, "LINK_MAP_BOUND")
        symbols = link_map.read_text(encoding="utf-8")
        need(re.search(r"\b_start\b", symbols) and re.search(r"\b__start\b", symbols), "SDK_STARTUP_SYMBOLS")
        artifact = {"user_elf": a.pin(binary), "elf_headers": k.elf_summary(binary), "link_map": a.pin(link_map)}
        a.save(run / "ARTIFACT.json", artifact)
        result.update(status=PASS, compiler_calls=4, checker_compiles=1, outputs=outputs, artifact=artifact)
    except BaseException as error:
        result["error"] = type(error).__name__ + ": " + str(error)[:4000]
    finally:
        finalizing = True
        if phase is not None:
            try:
                phase.close()
                need(phase.final_stats["active_processes"] == 0
                     and phase.final_stats["terminated_processes"] == 0
                     and phase.final_stats["cpu_seconds"] <= 240, "FINAL_JOB_CLEAN_AND_WITHIN_LIMIT")
            except BaseException as error:
                result.update(status="FAIL_CLEANUP", cleanup_error=str(error)[:2000])
            result["job"], result["commands"] = getattr(phase, "final_stats", None), phase.commands
            # Preserve actual launched counts even if a later command fails.
            launched = [row for row in phase.commands if type(row.get("pid")) is int]
            result["compiler_calls"] = len(launched)
            result["checker_compiles"] = sum(row["label"] == "checker" for row in launched)
        try:
            rebind()
            budget.refresh()
        except BaseException as error:
            result.update(status="FAIL_FINAL_CHECK", final_check_error=str(error)[:3000])
        result.update(controller_cpu_seconds=time.process_time() - cpu,
            wall_seconds=time.monotonic() - started, output_census=budget.current, sampled_peaks=budget.peak,
            accounting="DISJOINT_CONTROLLER_WORKER;FINAL_REPORT_EXIT_TAIL_EXCLUDED")
        a.save(run / "RESULT.json", result)
        a.save(attempt, {"status": result["status"], "result_sha256": sha(run / "RESULT.json")})
        try:
            budget.refresh()
        except BaseException as error:
            result.update(status="FAIL_FINALIZATION", finalization_error=str(error)[:3000])
            a.save(run / "FINALIZATION-FAILED.json", {"status": "FAIL_FINALIZATION",
                "overrides_result_and_attempt": True, "result_sha256": sha(run / "RESULT.json"),
                "error": str(error)[:3000]})
    print(json.dumps({key: result.get(key) for key in ("status", "error", "wall_seconds")}))
    return 0 if result["status"] == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
