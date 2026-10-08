"""Root-selected finite v5 guest cross-build, with exact offline graph delta.

No launch without a hash-pinned explicit selection. Reuses reviewed retained
toolchain/supervision, never old build targets, guest execution or proving.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SOURCE = ROOT / "software/v5/modules/receipt"
CHECKER = ROOT / "software/v5/modules/native/checker"
PRIOR = ROOT / "experiments/general-checker-guest-03"
PREP = PRIOR / "prepare-03"
COMMON_SHA = "97116bd269dd784b9216833f6e0c0bf38e9d08c55af5927511a13b26194133d7"
ADOPTED = {"RESULT.json", "SOURCE-MAP.json", "LOCKS.json", "UNIT-GRAPH.json",
           "DEPENDENCIES.json", "CARGO-HOME.json", "environment-profile.json", "GRAPH-DELTA.json"}
WRAPPER = {"Cargo.toml", "src/lib.rs", "src/main.rs", "src/canonical.rs",
           "src/input.rs",
           "src/commitments.rs", "src/journal.rs", "src/policy.rs", "src/relation.rs",
           "src/bin/receipt_native.rs"}
OWN = {"build_guest.py", "guest_graph.py", "GUEST-BUILD-PLAN.md"}
PASS = "PASS_NEW_MODULE_GUEST_CROSS_BUILD_ONLY"


def need(condition, reason):
    if not condition:
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


def main():
    started, cpu = time.monotonic(), time.process_time()
    need(os.name == "nt" and Path.cwd() == ROOT and Path(__file__).resolve() == SOURCE / "build_guest.py"
         and sys.dont_write_bytecode and sys.flags.isolated and sys.flags.no_site
         and not sys.flags.optimize and len(sys.argv) == 3, "ISOLATED_CANONICAL_INVOCATION")
    clearance = Path(sys.argv[1]).resolve(strict=True)
    need(clearance.is_relative_to(ROOT / "experiments") and clearance.stat().st_size <= 1024**2
         and sha(clearance) == sys.argv[2], "EXACT_SELECTION_PIN")
    selected = read(clearance)
    need(set(selected) == {"schema", "name", "sources", "preparation_sha256", "limits",
                          "authorizes_guest_build_and_owned_telemetry_cleanup"}
         and selected["schema"] == "DMKN_V5_GUEST_BUILD_V1"
         and selected["authorizes_guest_build_and_owned_telemetry_cleanup"] is True,
         "EXACT_BUILD_SELECTION")
    need(type(selected["name"]) is str and re.fullmatch(r"guest-build-[0-9]{2}", selected["name"]), "RUN_NAME")
    run = ROOT / "experiments/v5-local-checks" / selected["name"]
    need(not run.exists(), "FRESH_BUILD_ALLOCATION")
    need(selected["limits"] == {"worker_cpu_seconds": 1800, "wall_seconds": 1800,
         "memory_mib": 4096, "active_processes": 8, "combined_working_bytes": 16 * 1024**3},
         "EXACT_FINITE_GUEST_BUILD_LIMITS")
    need(set(selected["preparation_sha256"]) == ADOPTED, "EXACT_PREPARATION_RECORDS")
    need(type(selected["sources"]) is dict and 1 <= len(selected["sources"]) <= 256, "SOURCE_COUNT")
    wrapper, checker, own = {}, {}, {}
    for relative, row in selected["sources"].items():
        parts = PurePosixPath(relative).parts
        need(parts and all(part not in (".", "..") for part in parts)
             and not PurePosixPath(relative).is_absolute(), "SAFE_SELECTED_PATH")
        path = ROOT.joinpath(*parts).resolve(strict=True)
        need(path == ROOT.joinpath(*parts) and path.is_file(), "NO_SOURCE_ALIAS")
        need(set(row) == {"bytes", "sha256"} and type(row["bytes"]) is int
             and 0 < row["bytes"] <= 2 * 1024**2, "SOURCE_RECORD")
        if path.is_relative_to(SOURCE):
            local = path.relative_to(SOURCE).as_posix()
            if local in WRAPPER: wrapper[local] = row
            elif local in OWN: own[local] = row
            else: need(False, "UNSELECTED_RECEIPT_BUILD_SOURCE:" + local)
        elif path.is_relative_to(CHECKER):
            local = path.relative_to(CHECKER).as_posix()
            need(local.startswith("src/") and local.endswith(".rs")
                 or local in {"Cargo.toml", "LICENSE", "LICENSE-APACHE", "LICENSE-MIT"},
                 "CHECKER_SOURCE_SCOPE")
            checker[local] = row
        else: need(False, "SOURCE_OUTSIDE_SELECTED_V5_SCOPE")
    need(set(wrapper) == WRAPPER and set(own) == OWN
         and {"Cargo.toml", "src/lib.rs", "src/module.rs", "src/demand.rs",
              "src/module_correspondence.rs"}.issubset(checker), "COMPLETE_NEW_RELATION_SLICE")
    need(sum(row["bytes"] for row in selected["sources"].values()) <= 16 * 1024**2, "SOURCE_TOTAL_BOUND")

    def source_pins():
        need(sha(clearance) == sys.argv[2], "SELECTION_CHANGED")
        for relative, row in selected["sources"].items():
            path = ROOT / relative
            need(path.stat().st_size == row["bytes"] and sha(path) == row["sha256"], "SOURCE_CHANGED:" + relative)
        for name, digest in selected["preparation_sha256"].items():
            need(sha(PREP / name) == digest, "PREPARATION_CHANGED:" + name)
        need(sha(PRIOR / "common03.py") == COMMON_SHA, "HELD_COMMON_CHANGED")

    source_pins()
    delta = load("v5_guest_graph", SOURCE / "guest_graph.py", own["guest_graph.py"]["sha256"])
    k = load("v5_guest_held_common03", PRIOR / "common03.py", COMMON_SHA)
    k.held.HERE, k.held.PREP, k.held.BUILD = run.parent, run, run
    q, a, p, c, r, job = k.helpers()
    prior = read(PREP / "RESULT.json")
    need(prior["status"] == "PASS_OFFLINE_RUINT_COMPATIBILITY_PREPARATION_ONLY"
         and prior["job"]["active_processes"] == 0
         and prior["compiler_workloads"] == prior["guest_executions"] == prior["proof_calls"] == 0,
         "ADOPTED_PREPARATION_CLOSED")
    maps, locks = read(PREP / "SOURCE-MAP.json"), read(PREP / "LOCKS.json")
    seed, old_graph = read(PREP / "CARGO-HOME.json")["seed_map"], read(PREP / "UNIT-GRAPH.json")
    library = k.LIBRARY
    # The first rebind below computes and checks the actual retained map before
    # any allocation/copy/command. Do not compute that same full map twice here.
    state = maps["retained"]
    project = run / "project"
    fresh_wrapper, fresh_checker = project / "modules/receipt", project / "modules/native/checker"
    lock_bytes = delta.repin_lock((PREP / "project/guest/Cargo.lock").read_bytes())
    built_wrapper = {**wrapper, "Cargo.lock": {"bytes": len(lock_bytes),
                     "sha256": hashlib.sha256(lock_bytes).hexdigest()}}
    snapshot_ready = False

    def rebind():
        source_pins()
        need(c.file_map(PREP / "project/guest") == maps["wrapper"]
             and c.file_map(PREP / "project/checker") == maps["checker"]
             and c.file_map(k.STDROOT) == maps["std"], "ADOPTED_SOURCE_CHANGED")
        need(a.pin(PREP / "project/guest/Cargo.lock") == locks["guest_after"]
             and a.pin(library / "Cargo.lock") == locks["std_after"], "ADOPTED_LOCK_CHANGED")
        need(k.cache_seed_map(c, PREP / "cargo-home") == seed and k.retained(c) == state,
             "RETAINED_SEED_SDK_RUNTIME_CHANGED")
        k.held.build_tools(c)
        if snapshot_ready:
            need(c.file_map(fresh_wrapper) == built_wrapper and c.file_map(fresh_checker) == checker,
                 "FRESH_BUILD_SOURCE_CHANGED")
            need(c.file_map(run / "build-source") == own, "BUILD_ADAPTER_SNAPSHOT_CHANGED")
            need(sha(run / "selection.json") == sys.argv[2], "SAVED_SELECTION_CHANGED")

    rebind()
    run.mkdir()
    a.DISK_LIMIT = selected["limits"]["combined_working_bytes"]
    retained = {key: 0 for key in ("working_bytes", "retained_archive_bytes", "entries")}

    class Budget(a.Budget):
        def refresh(self):
            measured = c.census(self.run)
            # census also returns nonnumeric metadata (notably pruned_aliases).
            # Budget.current/peak accept exactly these THREE numeric counters,
            # as in the adopted collection build adapter; never iterate its
            # whole census schema or suppress alias information as if it were 0.
            counters = ("working_bytes", "retained_archive_bytes", "entries")
            need(all(type(record[key]) is int and record[key] >= 0
                     for record in (measured, retained) for key in counters), "NUMERIC_CENSUS_COUNTERS")
            self.current = {key: measured[key] + retained[key] for key in counters}
            self.current["working_bytes"] += 3 * 1024**3
            self.current["retained_archive_bytes"] += 192 * 1024**2
            self.current["entries"] += 30000
            need(self.current["entries"] <= a.ENTRY_LIMIT, "COMBINED_ENTRY_LIMIT")
            self.check()

    budget = Budget(run, started + 1800)
    phase = None
    result = {"status": "FAIL", "scope": "NEW_MODULE_GUEST_BUILD_ONLY", "started_utc": p.utc(),
              "selection": a.pin(clearance), "guest_executions": 0, "proof_calls": 0,
              "image_assembly_calls": 0, "network_fetch_commands": 0, "host_backend_builds": 0}
    try:
        saved_scope = c.HERE
        try:
            c.HERE = PRIOR
            retained = c.census(PREP)
            result["retained_census"] = retained
        finally:
            c.HERE = saved_scope
        budget.refresh()
        (run / "commands").mkdir()
        selection_bytes = clearance.read_bytes()
        need(hashlib.sha256(selection_bytes).hexdigest() == sys.argv[2], "SELECTION_COPY_PIN")
        budget.precharge(len(selection_bytes))
        with (run / "selection.json").open("xb") as stream:
            stream.write(selection_bytes)
        c.copy_map(SOURCE, fresh_wrapper, wrapper, budget)
        c.copy_map(CHECKER, fresh_checker, checker, budget)
        c.copy_map(SOURCE, run / "build-source", own, budget)
        budget.precharge(len(lock_bytes))
        with (fresh_wrapper / "Cargo.lock").open("xb") as stream:
            stream.write(lock_bytes)
        snapshot_ready = True
        a.save(run / "SOURCE-MAP.json", {"wrapper": built_wrapper, "checker": checker,
               "build_source": own, "std": maps["std"], "std_root": str(k.STDROOT),
               "retained": state, "origin": str(PREP)})
        env, evidence = k.environment(p, c, run, library)
        env["CARGO_NET_OFFLINE"] = "true"
        c.copy_map(PREP / "cargo-home", run / "cargo-home", seed, budget)
        evidence.update(cargo_offline=True, fresh_source=str(project), no_old_build_target_reused=True)
        a.save(run / "environment-profile.json", evidence)
        rebind()
        phase = r.phase_class(p, a)("v5-guest-cross-build", run, budget, env, job.Job, 1800)
        argv = [c.OLD / "rust/bin/cargo.exe", "build", "--release", "--manifest-path",
                fresh_wrapper / "Cargo.toml", "--bin", delta.NEW_BINARY, "--target", delta.TARGET,
                "-Z", "build-std=alloc,core,proc_macro,panic_abort,std",
                "-Z", "build-std-features=compiler-builtins-mem", "--locked", "--offline"]
        graph_output = phase.invoke("offline-graph-delta", argv + ["--unit-graph", "-Z", "unstable-options"], fresh_wrapper)
        graph = read(graph_output)
        comparison = delta.verify_delta(old_graph, graph, PREP, run)
        a.save(run / "UNIT-GRAPH.json", graph)
        a.save(run / "GRAPH-COMPARISON.json", comparison)
        rebind()
        output = phase.invoke("build-new-module-guest", argv + ["--message-format=json"], fresh_wrapper,
                              allow_build_telemetry=True)
        binaries = set()
        finished = []
        for line in output.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            if row.get("reason") == "build-finished": finished.append(row.get("success"))
            if row.get("reason") == "compiler-artifact" and row.get("target", {}).get("name") == delta.NEW_BINARY and row.get("executable"):
                need(row["target"]["kind"] == ["bin"] and row["profile"]["test"] is False
                     and row["profile"]["overflow_checks"] is True
                     and Path(row["target"]["src_path"]).resolve() == fresh_wrapper / "src/main.rs", "EXACT_NEW_GUEST_ARTIFACT")
                binary = Path(row["executable"]).resolve(strict=True)
                need(binary.is_relative_to(run / "target" / delta.TARGET / "release"), "ARTIFACT_ESCAPE")
                binaries.add(binary)
        need(len(binaries) == 1 and finished == [True], "ONE_COMPLETED_NEW_GUEST_ELF")
        binary = next(iter(binaries))
        link_map = run / "guest-link.map"
        need(link_map.is_file() and link_map.stat().st_size <= 32 * 1024**2, "LINK_MAP_BOUND")
        symbols = link_map.read_text(encoding="utf-8")
        need(re.search(r"\b_start\b", symbols) and re.search(r"\b__start\b", symbols), "SDK_STARTUP_SYMBOLS")
        artifact = {"user_elf": a.pin(binary), "elf_headers": k.elf_summary(binary), "link_map": a.pin(link_map),
                    "scope": "NEW guest ELF only, no image adoption/execution/proof"}
        a.save(run / "ARTIFACT.json", artifact)
        result.update(status=PASS, artifact=artifact, graph_delta=comparison)
    except BaseException as error:
        result["error"] = type(error).__name__ + ": " + str(error)[:4000]
    finally:
        if phase is not None:
            try: phase.close()
            except BaseException as error:
                result.update(status="FAIL_CLEANUP", cleanup_error=str(error)[:2000])
            result["job"], result["commands"] = phase.final_stats, phase.commands
        try:
            rebind()
            for name, row in k.registry_archives(run / "cargo-home").items():
                need(seed.get(name) == row, "OFFLINE_ARCHIVE_CHANGED_OR_ADDED")
            budget.refresh()
            result["new_final_storage"] = c.census(run)
        except BaseException as error:
            result.update(status="FAIL_FINAL_CHECK", final_check_error=str(error)[:2000])
        result.update(sampled_reserved_peaks=budget.peak, controller_cpu_seconds=time.process_time() - cpu,
                      wall_seconds=time.monotonic() - started, finished_utc=p.utc())
        if result["wall_seconds"] > 1800: result["status"] = "FAIL_TOTAL_WALL_LIMIT"
        a.save(run / "RESULT.json", result)
    print(json.dumps({key: result.get(key) for key in ("status", "error", "wall_seconds")}))
    return 0 if result["status"] == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
