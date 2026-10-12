"""Compile once from the preserved aggregate graph/source; root selection only.

Correct exactly four expected lexical source paths, retain whole-graph equality,
and do not repeat the successful offline graph command. Prior evidence is inert.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
SOURCE = ROOT / "software/v5/aggregate_guest"
FAILED = HERE / "aggregate-guest-build-01"
FAILED_PINS = {
    "RESULT.json": "231c94114e625a59371fdb1208aa7ae2838c9c35c9b8877b80bead4e7ad7e0ac",
    "SOURCE-MAP.json": "52c5166f2d41b7922a8916182ebbcbdc40e0dba2833899602273159654d0084b",
    "environment-profile.json": "200cb6c3e5a40e2154ba508c6bb665f76d517a392e6566a8f7a4c19fe3ee335f",
    "selection.json": "011ac45c532756eba74a573f66a06e1a2f0e78ba1219aed2bdd6bef8a3d67f70",
    "commands/offline-aggregate-graph/stdout.txt": "2cc441345c1cf3cc16e9dd21cca1bf2130319dbfa1124ad3ddb1d6507f2f4609",
}
ATTEMPT_SHA = "afbe7c3b9e4ae4b69484a5e9bdbab8ab1c62ab5427f736b10af5f2e58f2eeb6a"
BUILD_SHA = "4e986f7d2b6d6560b81e98a5d490d9488795ef64111300d12cf264e036c60038"
GRAPH_SHA = "2bbab886704aaa72ba4c6415b4187a1f5b0e699b6f3d61c512f16ea0d425af31"
LIMITS = {"worker_cpu_seconds": 1794, "controller_cpu_seconds": 134,
          "wall_seconds": 1653, "memory_mib": 4096, "active_processes": 8,
          "combined_working_bytes": 16 * 1024**3}
PASS = "PASS_OPTIMIZED_EXACT_WARRANT_AGGREGATE_GUEST_COMPILE_ONLY"


def need(value, reason):
    if not value:
        raise RuntimeError(reason)


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def load(name, path, digest):
    need(sha(path) == digest, "MODULE_PIN:" + str(path))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def corrected_graph(delta, old_graph, saved_graph, base):
    expected = delta.expected_delta(old_graph, base, FAILED)
    project = FAILED / "project/software/v5"
    overlay = project / "aggregate_guest"
    pairs = {
        "dmkn_module_relation": (project / "modules/receipt/src/lib.rs",
                                 overlay / "module/../../modules/receipt/src/lib.rs"),
        "nanoda_lib": (project / "modules/native/proof_validation/lib.rs",
                       overlay / "checker/../../modules/native/proof_validation/lib.rs"),
        "dmkn-aggregate-claim-guest": (project / "aggregate/main.rs", overlay / "../aggregate/main.rs"),
        "dmkn_aggregate_relation": (project / "aggregate_claims/lib.rs", overlay / "../aggregate_claims/lib.rs"),
    }
    changes = []
    for name, (resolved, lexical) in pairs.items():
        units = [unit for unit in expected["units"] if unit["target"]["name"] == name]
        need(len(units) == 1 and units[0]["target"]["src_path"] == str(resolved), "EXACT_FOUR_OLD_PATH_FIELDS")
        need(lexical.resolve(strict=True) == resolved and resolved.resolve(strict=True) == resolved,
             "LEXICAL_PATH_IS_EXACT_PINNED_SOURCE")
        units[0]["target"]["src_path"] = str(lexical)
        changes.append({"target": name, "old_expected": str(resolved), "corrected_expected": str(lexical)})
    actual = delta.normalize_cache(saved_graph, FAILED / "cargo-home")
    need(delta.canonical_graph(expected) == delta.canonical_graph(actual), "EXACT_FULL_RETAINED_GRAPH_AFTER_FOUR_FIELDS")
    json_units = [unit for unit in actual["units"] if unit["pkg_id"] ==
                  "registry+https://github.com/rust-lang/crates.io-index#serde_json@1.0.151"]
    need(json_units and all(unit["features"] == ["default", "std"] for unit in json_units),
         "VALUE_IDENTITY_REQUIRES_EXACT_SERDE_JSON_DEFAULT_STD")
    return {"status": "EXACT_FOUR_LEXICAL_FIELDS_WITH_FULL_GRAPH_EQUALITY", "changes": changes,
            "units": len(saved_graph["units"]), "new_graph_calls": 0,
            "external_package_feature_profile_or_edge_changes": 0}


def main():
    started, cpu = time.monotonic(), time.process_time()
    need(os.name == "nt" and Path.cwd() == ROOT and Path(__file__).resolve() == SOURCE / "compile_only.py"
         and sys.dont_write_bytecode and sys.flags.isolated and sys.flags.no_site
         and not sys.flags.optimize and len(sys.argv) == 3, "ISOLATED_CANONICAL_COMPILE_ONLY")
    clearance = Path(sys.argv[1]).resolve(strict=True)
    need(clearance.is_relative_to(HERE) and clearance.stat().st_size <= 1024**2
         and sha(clearance) == sys.argv[2], "EXACT_COMPILE_SELECTION_PIN")
    selected = read(clearance)
    need(set(selected) == {"schema", "name", "source", "limits", "authorizes_compile_and_owned_telemetry_cleanup"}
         and selected["schema"] == "DMKN_V5_AGGREGATE_GUEST_COMPILE_V1"
         and selected["authorizes_compile_and_owned_telemetry_cleanup"] is True
         and selected["limits"] == LIMITS and type(selected["name"]) is str
         and re.fullmatch(r"aggregate-guest-compile-[0-9]{2}", selected["name"]), "EXACT_COMPILE_ONLY_SELECTION")
    own_pin = selected["source"]
    need(set(own_pin) == {"bytes", "sha256"} and type(own_pin["bytes"]) is int
         and 0 < own_pin["bytes"] <= 1024**2, "EXACT_ADAPTER_PIN")

    def record_pins():
        need(time.monotonic() - started <= LIMITS["wall_seconds"]
             and time.process_time() - cpu <= LIMITS["controller_cpu_seconds"], "REMAINING_CONTROLLER_ENVELOPE")
        need(sha(clearance) == sys.argv[2] and (SOURCE / "compile_only.py").stat().st_size == own_pin["bytes"]
             and sha(SOURCE / "compile_only.py") == own_pin["sha256"], "SELECTION_ADAPTER_CHANGED")
        for name, digest in FAILED_PINS.items():
            need(sha(FAILED / name) == digest, "FROZEN_GRAPH_PREFIX:" + name)
        need(sha(HERE / "aggregate-guest-build-01-attempt.json") == ATTEMPT_SHA
             and not (FAILED / "FINALIZATION-FAILED.json").exists(), "FROZEN_FAILURE_MARKER")
        need(sha(SOURCE / "build.py") == BUILD_SHA and sha(SOURCE / "graph.py") == GRAPH_SHA,
             "FROZEN_BUILD_GRAPH_SOURCE")

    record_pins()
    prior = load("aggregate_compile_predecessor", SOURCE / "build.py", BUILD_SHA)
    delta = load("aggregate_compile_graph", SOURCE / "graph.py", GRAPH_SHA)
    failed = read(FAILED / "RESULT.json")
    need(failed["status"] == "FAIL" and failed["error"] == "ValueError: UNSELECTED_FULL_AGGREGATE_GUEST_GRAPH_DELTA"
         and failed["job"]["active_processes"] == 0 and len(failed["commands"]) == 1
         and failed["commands"][0]["label"] == "offline-aggregate-graph"
         and failed["commands"][0]["exit_code"] == 0 and failed["commands"][0]["cleanup_errors"] == []
         and failed["guest_executions"] == failed["proof_calls"] == failed["image_assembly_calls"] == 0,
         "EXACT_UNCOMPILED_CLOSED_GRAPH_PREFIX")
    need(failed["job"]["cpu_seconds"] + LIMITS["worker_cpu_seconds"] <= 1800
         and failed["controller_cpu_seconds"] + LIMITS["controller_cpu_seconds"] <= 180
         and failed["wall_seconds"] + LIMITS["wall_seconds"] <= 1800, "NO_ORIGINAL_BUDGET_RENEWAL")
    project = FAILED / "project"
    wrapper = project / "software/v5/aggregate_guest"
    frozen_map = read(FAILED / "SOURCE-MAP.json")
    frozen_selection = read(FAILED / "selection.json")
    need(len(frozen_selection["sources"]) == 38
         and set(frozen_map["project"]) == set(frozen_selection["sources"]) | {"software/v5/aggregate_guest/Cargo.lock"}
         and all(frozen_map["project"][name] == pin for name, pin in frozen_selection["sources"].items()),
         "UNCHANGED_38_SOURCE_AND_LOCK_SNAPSHOT")
    for name, digest in prior.BASE_PINS.items():
        need(sha(prior.BASE / name) == digest, "ADOPTED_BASE_RECORD:" + name)
    old_graph = read(prior.BASE / "UNIT-GRAPH.json")
    saved_graph = read(FAILED / "commands/offline-aggregate-graph/stdout.txt")
    graph_comparison = corrected_graph(delta, old_graph, saved_graph, prior.BASE)
    run = HERE / selected["name"]
    attempt = HERE / (selected["name"] + "-attempt.json")
    need(not run.exists() and not attempt.exists(), "FRESH_COMPILE_OUTPUT")
    k = load("aggregate_compile_common", prior.PRIOR / "common03.py", prior.COMMON_SHA)
    k.held.HERE, k.held.PREP, k.held.BUILD = HERE, run, run
    q, a, p, c, r, job = k.helpers()
    preparation_pins = read(prior.BASE / "selection.json")["preparation_sha256"]
    maps, locks = read(prior.PREP / "SOURCE-MAP.json"), read(prior.PREP / "LOCKS.json")
    seed = read(prior.PREP / "CARGO-HOME.json")["seed_map"]
    state, library = maps["retained"], k.LIBRARY

    def rebind():
        record_pins()
        for name, digest in prior.BASE_PINS.items():
            need(sha(prior.BASE / name) == digest, "BASE_RECORD_CHANGED:" + name)
        for name, digest in preparation_pins.items():
            need(sha(prior.PREP / name) == digest, "PREPARATION_RECORD_CHANGED:" + name)
        need(sha(prior.PRIOR / "common03.py") == prior.COMMON_SHA, "COMMON_CHANGED")
        need(c.file_map(project) == frozen_map["project"], "UNCHANGED_REUSED_PROJECT_AND_LOCK")
        need(c.file_map(k.STDROOT) == maps["std"] and a.pin(library / "Cargo.lock") == locks["std_after"],
             "UNCHANGED_STD_AND_LOCK")
        need(k.cache_seed_map(c, prior.PREP / "cargo-home") == seed and k.retained(c) == state,
             "UNCHANGED_SEED_SDK_RUNTIME")
        k.held.build_tools(c)
        comparison = frozen_selection["native_comparison"]
        need(sha(Path(comparison["path"])) == comparison["sha256"]
             and sha(prior.NATIVE / "RESULT.json") == prior.NATIVE_RESULT_SHA
             and sha(prior.NATIVE / "source-map.json") == prior.NATIVE_MAP_SHA, "ADOPTED_NATIVE_CHAIN_CHANGED")

    rebind()
    run.mkdir()
    a.DISK_LIMIT = LIMITS["combined_working_bytes"]
    retained = {key: 0 for key in ("working_bytes", "retained_archive_bytes", "entries")}

    class Budget(a.Budget):
        def refresh(self):
            need(time.monotonic() - started <= LIMITS["wall_seconds"]
                 and time.process_time() - cpu <= LIMITS["controller_cpu_seconds"], "REMAINING_TOTAL_ENVELOPE")
            measured = c.census(self.run)
            counters = ("working_bytes", "retained_archive_bytes", "entries")
            need(all(type(row[key]) is int and row[key] >= 0 for row in (measured, retained) for key in counters),
                 "NUMERIC_CENSUS_COUNTERS")
            self.current = {key: measured[key] + retained[key] for key in counters}
            self.current["working_bytes"] += 3 * 1024**3
            self.current["retained_archive_bytes"] += 192 * 1024**2
            self.current["entries"] += 30000
            need(self.current["entries"] <= a.ENTRY_LIMIT, "COMBINED_ENTRY_LIMIT")
            self.check()

    budget = Budget(run, started + LIMITS["wall_seconds"])
    phase = None
    result = {"schema": "DMKN_V5_AGGREGATE_GUEST_COMPILE_RESULT_V1", "status": "FAIL",
              "selection_sha256": sys.argv[2], "started_utc": p.utc(), "guest_executions": 0,
              "proof_calls": 0, "image_assembly_calls": 0, "network_fetch_commands": 0,
              "host_backend_builds": 0, "new_graph_calls": 0,
              "scope": "ONE_AGGREGATE_GUEST_COMPILE_FROM_RETAINED_GRAPH_ONLY",
              "predecessor_result": {"path": str(FAILED / "RESULT.json"), "sha256": FAILED_PINS["RESULT.json"]},
              "predecessor_graph": {"path": str(FAILED / "commands/offline-aggregate-graph/stdout.txt"),
                                    "sha256": FAILED_PINS["commands/offline-aggregate-graph/stdout.txt"]},
              "prior_charged": {"worker_cpu_seconds": failed["job"]["cpu_seconds"],
                                "controller_cpu_seconds": failed["controller_cpu_seconds"],
                                "wall_seconds": failed["wall_seconds"]}}
    try:
        saved_scope = c.HERE
        try:
            c.HERE = prior.PRIOR
            prep_census = c.census(prior.PREP)
        finally:
            c.HERE = saved_scope
        failed_census = c.census(FAILED)
        retained = {key: prep_census[key] + failed_census[key] for key in retained}
        result["retained_preparation_census"], result["retained_failed_census"] = prep_census, failed_census
        budget.refresh()
        (run / "commands").mkdir()
        raw_selection = clearance.read_bytes()
        need(hashlib.sha256(raw_selection).hexdigest() == sys.argv[2], "SELECTION_COPY_PIN")
        budget.precharge(len(raw_selection))
        with (run / "selection.json").open("xb") as stream:
            stream.write(raw_selection)
        a.save(run / "SOURCE-MAP.json", {"reused_project": str(project), "project": frozen_map["project"],
               "controller": {"path": str(SOURCE / "compile_only.py"), **own_pin},
               "std": maps["std"], "retained": state})
        a.save(run / "GRAPH-COMPARISON.json", graph_comparison)
        env, evidence = k.environment(p, c, run, library)
        env["CARGO_NET_OFFLINE"] = "true"
        c.copy_map(prior.PREP / "cargo-home", run / "cargo-home", seed, budget)
        evidence.update(cargo_offline=True, reused_immutable_source=str(project),
                        no_old_build_target_reused=True, no_graph_command_repeated=True)
        a.save(run / "environment-profile.json", evidence)
        rebind()
        phase = r.phase_class(p, a)("aggregate-guest-compile-only", run, budget, env, job.Job,
                                   LIMITS["worker_cpu_seconds"])
        argv = [c.OLD / "rust/bin/cargo.exe", "build", "--release", "--manifest-path", wrapper / "Cargo.toml",
                "--bin", delta.BINARY, "--target", delta.TARGET,
                "-Z", "build-std=alloc,core,proc_macro,panic_abort,std",
                "-Z", "build-std-features=compiler-builtins-mem", "--locked", "--offline", "--message-format=json"]
        output = phase.invoke("build-aggregate-guest", argv, wrapper, allow_build_telemetry=True)
        binaries, finished = set(), []
        for line in output.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            if row.get("reason") == "build-finished":
                finished.append(row.get("success"))
            if row.get("reason") == "compiler-artifact" and row.get("target", {}).get("name") == delta.BINARY and row.get("executable"):
                need(row["target"]["kind"] == ["bin"] and row["profile"]["test"] is False
                     and row["profile"]["overflow_checks"] is True
                     and Path(row["target"]["src_path"]).resolve() == project / prior.ENTRY,
                     "EXACT_AGGREGATE_GUEST_ARTIFACT")
                binary = Path(row["executable"]).resolve(strict=True)
                need(binary == run / "target" / delta.TARGET / "release" / delta.BINARY, "EXACT_FRESH_ARTIFACT_PATH")
                binaries.add(binary)
        need(len(binaries) == 1 and finished == [True], "ONE_COMPLETED_AGGREGATE_GUEST_ELF")
        binary, link_map = next(iter(binaries)), run / "guest-link.map"
        need(link_map.is_file() and link_map.stat().st_size <= 32 * 1024**2, "LINK_MAP_BOUND")
        symbols = link_map.read_text(encoding="utf-8")
        need(re.search(r"\b_start\b", symbols) and re.search(r"\b__start\b", symbols), "SDK_STARTUP_SYMBOLS")
        artifact = {"user_elf": a.pin(binary), "elf_headers": k.elf_summary(binary), "link_map": a.pin(link_map),
                    "scope": "New aggregate ELF only; no image adoption/execution/proof"}
        a.save(run / "ARTIFACT.json", artifact)
        result.update(status=PASS, artifact=artifact, graph_delta=graph_comparison)
    except BaseException as error:
        result["error"] = type(error).__name__ + ": " + str(error)[:4000]
    finally:
        if phase is not None:
            try:
                phase.close()
            except BaseException as error:
                result.update(status="FAIL_CLEANUP", cleanup_error=str(error)[:2000])
            result["job"], result["commands"] = phase.final_stats, phase.commands
        try:
            rebind()
            for name, pin in k.registry_archives(run / "cargo-home").items():
                need(seed.get(name) == pin, "OFFLINE_ARCHIVE_CHANGED_OR_ADDED")
            budget.refresh()
            result["new_final_storage"] = c.census(run)
        except BaseException as error:
            result.update(status="FAIL_FINAL_CHECK", final_check_error=str(error)[:2000])
        result.update(sampled_reserved_peaks=budget.peak, controller_cpu_seconds=time.process_time() - cpu,
                      wall_seconds=time.monotonic() - started, finished_utc=p.utc(),
                      accounting="CONTROLLER_DISJOINT_FROM_INCLUSIVE_WORKER_JOB;FINAL_REPORT_EXIT_TAIL_EXCLUDED")
        if result["wall_seconds"] > LIMITS["wall_seconds"]:
            result["status"] = "FAIL_TOTAL_WALL_LIMIT"
        a.save(run / "RESULT.json", result)
        a.save(attempt, {"status": result["status"], "result_sha256": sha(run / "RESULT.json")})
        try:
            budget.refresh()
        except BaseException as error:
            result.update(status="FAIL_FINALIZATION", finalization_error=str(error)[:3000])
            a.save(run / "FINALIZATION-FAILED.json", {"status": "FAIL_FINALIZATION", "overrides_result_and_attempt": True,
                   "result_sha256": sha(run / "RESULT.json"), "error": str(error)[:3000]})
    print(json.dumps({key: result.get(key) for key in ("status", "error", "wall_seconds")}))
    return 0 if result["status"] == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
