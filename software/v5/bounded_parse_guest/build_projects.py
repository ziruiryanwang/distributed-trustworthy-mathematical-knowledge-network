"""Three new guest project compiles using a strict copied retained-library view.

No Cargo, graph rerun, cache/source-tree copy, dependency compile, guest or proof.
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
SOURCE = ROOT / "software/v5/bounded_parse_guest"
SNAPSHOT = HERE / "bounded-parse-guest-build-02"
OLD = HERE / "aggregate-guest-compile-01"
OLD_GRAPH = HERE / "aggregate-guest-build-01/commands/offline-aggregate-graph/stdout.txt"
RUST = ROOT / "experiments/scale-crypto-01/runs/run-01/rust"
COMMON = ROOT / "experiments/general-checker-guest-03/common03.py"
COMMON_SHA = "97116bd269dd784b9216833f6e0c0bf38e9d08c55af5927511a13b26194133d7"
GRAPH_SHA = "090744c1b479474399912c2180e8cca8e1e12afe050689f6c310af4c57136c87"
PASS = "PASS_BOUNDED_PARSE_THREE_PROJECT_COMPILES_ONLY"
ADAPTERS = {"software/v5/bounded_parse_guest/build_projects.py",
            "software/v5/bounded_parse_guest/recipes.py"}
LIMITS = {"worker_cpu_seconds": 240, "worker_wall_seconds": 300, "memory_mib": 4096,
    "active_processes": 6, "ordinary_controller_cpu_seconds": 40, "controller_cpu_seconds": 60,
    "total_wall_seconds": 420, "fresh_output_bytes": 512*1024**2,
    "fresh_output_entries": 4096, "command_log_bytes": 8*1024**2}
RECORDS = {
    SNAPSHOT / "RESULT.json": "792ed5825ae3110dc3ddc1a85b49636b63469f5e4cb1d662e70d8ddf27d6b4b6",
    SNAPSHOT / "FINALIZATION-FAILED.json": "36c6f5c6b7084dbb08d461c008ea8b39e71e80bf95cc90860e455936b637cf55",
    SNAPSHOT / "selection.json": "a537fdbc9bf27b9a0832bb14a72aa07aad4d96abe9cc6bb433473a58935c16e2",
    SNAPSHOT / "SOURCE-MAP.json": "1ca936d624d91d7d395ac89f7535e1564473ee62e05a6f357e754b6d2c93281b",
    SNAPSHOT / "UNIT-GRAPH.json": "142224e56a81b3d73960a0aa5c5f80360658ccf0f1bff06883152cbfe92511fe",
    SNAPSHOT / "GRAPH-COMPARISON.json": "36b0bd9bc55a15adca6f8e878bda3b2529d015fe841075aa3f2d30e771780bc5",
    OLD / "commands/build-aggregate-guest/stdout.txt": "8e54baefabfa6abc5461af0b6a9b126960203df9bf4e45ae9a9feccd4ad0328b",
    OLD / "commands/build-aggregate-guest/command.json": "d914a4fe3a605a9de832c275b8b51b9abdfdba7a973d2204673eab5490cb6f05",
    OLD / "FINALIZATION-FAILED.json": "d0d6d8980c492d43a8927825aa153271543fa18d960305db5bde1e51c323dd54",
    OLD / "SOURCE-MAP.json": "75c710e3ee13f63cb6ef44da8656caa53c300bf649317d2b5669d8b9cde06ce0",
    OLD / "environment-profile.json": "7e1b195a0e075eec9ba8f0d7f8e65c83a9a3cebfc3332e7910d9909be2581ff5",
    OLD_GRAPH: "2cc441345c1cf3cc16e9dd21cca1bf2130319dbfa1124ad3ddb1d6507f2f4609",
    COMMON: COMMON_SHA,
}


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

    need(os.name == "nt" and Path.cwd() == ROOT and Path(__file__).resolve() == SOURCE / "build_projects.py"
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize and len(sys.argv) == 3, "ISOLATED_CANONICAL_DIRECT_BUILD")
    clearance = Path(sys.argv[1]).resolve(strict=True)
    need(clearance.parent == HERE and clearance.stat().st_size <= 1024**2
         and sha(clearance) == sys.argv[2], "EXACT_DIRECT_SELECTION")
    chosen = read(clearance)
    need(set(chosen) == {"schema", "name", "adapters", "retained_artifacts", "limits",
         "authorizes_three_compiles_and_retained_artifact_adoption"}
         and chosen["schema"] == "DMKN_V5_BOUNDED_PARSE_DIRECT_PROJECT_BUILD_V1"
         and chosen["name"] == "bounded-parse-direct-build-01" and chosen["limits"] == LIMITS
         and chosen["authorizes_three_compiles_and_retained_artifact_adoption"] is True
         and type(chosen["adapters"]) is dict and set(chosen["adapters"]) == ADAPTERS, "SELECTION_FIELDS")
    for path, digest in RECORDS.items():
        envelope()
        need(sha(path) == digest, "RETAINED_EVIDENCE_PIN:" + str(path))
    failed, override = read(SNAPSHOT / "RESULT.json"), read(SNAPSHOT / "FINALIZATION-FAILED.json")
    need(failed["status"] == "FAIL" and override["status"] == "FAIL_FINALIZATION"
         and override["overrides_result_and_attempt"] is True
         and override["result_sha256"] == RECORDS[SNAPSHOT / "RESULT.json"]
         and failed["job"]["active_processes"] == 0 and failed["job"]["cpu_seconds"] == 190.21875
         and failed["controller_cpu_seconds"] == 88.640625, "RETAINED_FAILURE_NOT_RELABELLED")
    old_command = read(OLD / "commands/build-aggregate-guest/command.json")
    need(old_command["status"] == "COMMAND_COMPLETED" and old_command["exit_code"] == 0
         and old_command["job_after"]["active_processes"] == 0
         and old_command["job_after"]["terminated_processes"] == 0, "COMPLETED_OLD_COMPILER_CHILD_ONLY")
    project_map = read(SNAPSHOT / "SOURCE-MAP.json")["project"]
    selected_source = read(SNAPSHOT / "selection.json")["sources"]
    lock_relative = "software/v5/bounded_parse_guest/Cargo.lock"
    need(set(project_map) == set(selected_source) | {lock_relative} and len(project_map) == 39
         and all(project_map[name] == pin for name, pin in selected_source.items()), "UNCHANGED_39_FILE_SNAPSHOT")
    source_roots = {name: pin for name, pin in project_map.items()
                    if name.endswith(".rs") and not name.startswith("software/v5/modules/native/")}
    need(len(source_roots) == 16, "EXACT_16_COMPILER_READ_PROJECT_FILES")
    plan = load("direct_guest_recipes", SOURCE / "recipes.py",
                chosen["adapters"]["software/v5/bounded_parse_guest/recipes.py"]["sha256"])
    g = load("direct_guest_graph", SNAPSHOT / "project/software/v5/bounded_parse_guest/graph.py", GRAPH_SHA)
    graph = read(SNAPSHOT / "UNIT-GRAPH.json")
    comparison = g.verify_graph(read(OLD_GRAPH), graph, SNAPSHOT)
    need(comparison == read(SNAPSHOT / "GRAPH-COMPARISON.json"), "ADOPT_ONLY_RETAINED_EXACT_GRAPH")
    raw_rows = (OLD / "commands/build-aggregate-guest/stdout.txt").read_text(encoding="utf-8").splitlines()
    # This exact pinned non-verbose predecessor is all JSON. Never use the
    # mixed plain/JSON -vv output from failed02 with this parser.
    retained_files, libraries = plan.dependencies([json.loads(line) for line in raw_rows if line])
    need(type(chosen["retained_artifacts"]) is dict
         and set(chosen["retained_artifacts"]) == set(retained_files), "EXACT_238_ADOPTED_LIBRARY_FILES")
    run, attempt = HERE / chosen["name"], HERE / (chosen["name"] + "-attempt.json")
    need(not run.exists() and not attempt.exists(), "FRESH_DIRECT_OUTPUT")
    recipes = plan.commands(graph, run, retained_files, libraries, read(OLD / "environment-profile.json")["guest_rustflags"])
    old_map = read(OLD / "SOURCE-MAP.json")
    checker_sources = {name: pin for name, pin in project_map.items()
                       if name.startswith("software/v5/modules/native/") and name.endswith(".rs")}
    need(len(checker_sources) == 16 and all(old_map["project"][name] == pin
         for name, pin in checker_sources.items()), "UNCHANGED_16_REUSED_CHECKER_SOURCE_BINDINGS")
    compiler = {name: pin for name, pin in old_map["retained"]["runtime"].items()
        if name in {"bin/rustc.exe", "lib/rustlib/x86_64-pc-windows-msvc/bin/rust-lld.exe"}
        or (name.startswith("bin/") and name.endswith(".dll"))
        or (name.startswith("lib/rustlib/x86_64-pc-windows-msvc/lib/") and name.endswith((".rlib", ".rmeta")))}
    need(len(compiler) == 26 and sum(pin["bytes"] for pin in compiler.values()) == 395093004,
         "EXACT_26_COMPILER_INPUTS_NO_CARGO")
    k = load("direct_guest_common", COMMON, COMMON_SHA)
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
        p.HELPERS / "run_stage.py": p.HELPER_SHA, p.HELPERS / "domains.py": p.DOMAINS_SHA}
    digests.update({q.CRYPTO / name: digest for name, digest in q.HELPERS.items()})
    exact = {}

    def include(path, pin):
        need(path.is_absolute() and type(pin) is dict and set(pin) == {"bytes", "sha256"}
             and type(pin["bytes"]) is int and 0 < pin["bytes"] <= 512*1024**2
             and re.fullmatch(r"[0-9a-f]{64}", pin["sha256"]), "INPUT_PIN")
        need(str(path) not in exact or exact[str(path)] == pin, "INPUT_PIN_CONFLICT")
        exact[str(path)] = dict(pin)

    for base, rows in ((ROOT, chosen["adapters"]), (SNAPSHOT / "project", project_map), (RUST, compiler)):
        for relative, pin in rows.items():
            a.safe_parts(relative)
            include(base / relative, pin)
    for name, pin in chosen["retained_artifacts"].items():
        include(Path(name), pin)
    need(sum(pin["bytes"] for pin in chosen["retained_artifacts"].values()) == 320499420
         and sum(chosen["retained_artifacts"][name]["bytes"] for name in retained_files
                 if retained_files[name].startswith("libraries/")) == 281325788, "EXACT_LIBRARY_VIEW_BYTES")
    for path, digest in digests.items():
        include(path, {"bytes": path.stat().st_size, "sha256": digest})
    copied = False
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
        need(c.file_map(SNAPSHOT / "project") == project_map, "UNCHANGED_COMPLETE_SOURCE_SNAPSHOT")
        if copied:
            for relative, pin in copy_map.items():
                bind(run / "retained" / relative, pin)
            need(c.file_map(run / "retained") == copy_map, "NO_UNSELECTED_SAME_NAME_LIBRARY")
            need(sha(run / "selection.json") == sys.argv[2], "SAVED_SELECTION_CHANGED")

    rebind()
    run.mkdir()
    phase = None
    result = {"schema": "DMKN_V5_BOUNDED_PARSE_DIRECT_PROJECT_BUILD_RESULT_V1", "status": "FAIL",
        "selection_sha256": sys.argv[2], "limits": LIMITS,
        "source_snapshot": str(SNAPSHOT / "project"),
        "source_map_sha256": RECORDS[SNAPSHOT / "SOURCE-MAP.json"],
        "predecessor_status": "FAIL_FINALIZATION", "predecessor_result_sha256": RECORDS[SNAPSHOT / "RESULT.json"],
        "predecessor_worker_cpu_seconds": 190.21875,
        "predecessor_recorded_controller_cpu_seconds": 88.640625,
        "predecessor_controller_cpu_lower_bound_exclusive": 90,
        "predecessor_tail_exact_cpu_unknown": True, "cargo_calls": 0, "graph_commands": 0,
        "dependency_compiles": 0, "checker_compiles": 0, "guest_calls": 0, "proof_calls": 0,
        "image_assembly_calls": 0, "network_calls": 0,
        "authority": "THREE_RECONSTRUCTED_PROFILE_PROJECT_COMPILES_ONLY"}

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
        a.save(run / "SOURCE-MAP.json", {"source_snapshot": str(SNAPSHOT / "project"),
            "project": project_map, "compiler_read_sources": source_roots, "adapters": chosen["adapters"]})
        a.save(run / "RECIPES.json", {"schema": "DMKN_V5_DIRECT_PROJECT_RECIPES_V1",
            "basis": "RECONSTRUCTED_EQUIVALENT_PROFILE_NOT_CAPTURED_CARGO_ARGV", "recipes": recipes})
        a.save(run / "GRAPH-COMPARISON.json", {"schema": "DMKN_V5_RETAINED_GRAPH_PROJECTION_V1",
            "retained_graph_sha256": RECORDS[SNAPSHOT / "UNIT-GRAPH.json"], "comparison": comparison,
            "new_compilation_units": [item["name"] for item in recipes], "new_cargo_graph_commands": 0})
        env, environment = p.environment(run, RUST)
        # The selected roots and expanded SDK/json macros read no Cargo env.
        # serde_derive's version token is already baked into the retained DLL.
        # Keep the complete private invocation environment recorded nonetheless.
        environment.update(explicit_environment=env, source_snapshot=str(SNAPSHOT / "project"),
                           cargo_invocations=0, copied_artifact_files=238, copied_artifact_bytes=320499420)
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
        phase = r.phase_class(p, a)("bounded-parse-direct-projects", run, budget, env, exact_job, 300)
        outputs = {}
        for index, recipe in enumerate(recipes):
            phase.invoke(("module", "aggregate", "guest")[index], recipe["argv"], ROOT)
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
        result.update(status=PASS, compiler_calls=3, outputs=outputs, artifact=artifact)
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
