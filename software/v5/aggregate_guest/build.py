"""Fresh offline aggregate guest graph/build; root exact selection required.

Uses the retained RV32/build-std recipe and fresh target, not Windows rlibs or
an old target cache. Two Cargo calls only: graph validation, then compilation.
No image assembly, guest execution, receipt verification, proving or network.
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
HERE = ROOT/"experiments/v5-local-checks"
SOURCE = ROOT/"software/v5/aggregate_guest"
PRIOR = ROOT/"experiments/general-checker-guest-03"
PREP = PRIOR/"prepare-03"
BASE = HERE/"guest-build-05"
NATIVE = HERE/"proof-validation-integration-build-01"
COMMON_SHA = "97116bd269dd784b9216833f6e0c0bf38e9d08c55af5927511a13b26194133d7"
BASE_PINS = {
    "RESULT.json":"49d9dccffee46fc245f09c71a66bcaa38e19b8834d505b838239c095139cb2bb",
    "SOURCE-MAP.json":"df3d2f881ad0b2460e2b39c45720147c157fadb1eb38646a2a4649202cf7f8f3",
    "UNIT-GRAPH.json":"976c1748172bb7e8c79f0793cfb22800551f5cedab92d35daf279efa3973bc26",
    "project/modules/receipt/Cargo.lock":"548ba68f7d20017a676471308a8a433e099b455d4a969789003249731d48ea0a",
    "selection.json":"5da04eb9fa61bb667efa2afe35157a86a2bfde6be05a3c0f64f7fc99e27fb74a",
}
NATIVE_MAP_SHA = "a5693f19236bb8051e476d9f61d8d2449cbcd023054a1e9c8606607049957f2a"
NATIVE_RESULT_SHA = "55ba9a702360dd10a6b9bea00f481d5066553a1b8debcb10ca43bbcab4de4069"
ENTRY = "software/v5/aggregate/main.rs"
ENTRY_SHA = "d7b9b93843b683215e0556e585bc5ea241c672fe4c2a89cc07afa41afb81acad"
OVERLAYS = {"software/v5/aggregate_guest/"+name for name in ("Cargo.toml","checker/Cargo.toml","module/Cargo.toml")}
OWN = {"software/v5/aggregate_guest/graph.py","software/v5/aggregate_guest/build.py"}
LIMITS = {"worker_cpu_seconds":1800,"wall_seconds":1800,"memory_mib":4096,
    "active_processes":8,"combined_working_bytes":16*1024**3}
PASS = "PASS_OPTIMIZED_EXACT_WARRANT_AGGREGATE_GUEST_BUILD_ONLY"


def need(value,reason):
    if not value: raise RuntimeError(reason)


def sha(path):
    with path.open("rb") as stream: return hashlib.file_digest(stream,"sha256").hexdigest()


def read(path): return json.loads(path.read_bytes())


def load(name,path,digest):
    need(sha(path) == digest,"MODULE_PIN:"+str(path))
    spec = importlib.util.spec_from_file_location(name,path)
    module = importlib.util.module_from_spec(spec); sys.modules[name] = module
    spec.loader.exec_module(module); return module


def main():
    started,cpu = time.monotonic(),time.process_time()
    need(os.name == "nt" and Path.cwd() == ROOT and Path(__file__).resolve() == SOURCE/"build.py"
        and sys.dont_write_bytecode and sys.flags.isolated and sys.flags.no_site
        and not sys.flags.optimize and len(sys.argv) == 3,"ISOLATED_CANONICAL_GUEST_BUILD")
    clearance = Path(sys.argv[1]).resolve(strict=True)
    need(clearance.is_relative_to(HERE) and clearance.stat().st_size <= 1024**2
        and sha(clearance) == sys.argv[2],"EXACT_GUEST_SELECTION_PIN")
    selected = read(clearance)
    need(set(selected) == {"schema","name","sources","limits","native_comparison",
        "authorizes_guest_build_and_owned_telemetry_cleanup"}
        and selected["schema"] == "DMKN_V5_AGGREGATE_GUEST_BUILD_V1"
        and selected["authorizes_guest_build_and_owned_telemetry_cleanup"] is True
        and selected["limits"] == LIMITS and type(selected["name"]) is str
        and re.fullmatch(r"aggregate-guest-build-[0-9]{2}",selected["name"]),"EXACT_GUEST_BUILD_SELECTION")
    for name,digest in BASE_PINS.items(): need(sha(BASE/name) == digest,"ADOPTED_GUEST_RECORD:"+name)
    need(sha(NATIVE/"source-map.json") == NATIVE_MAP_SHA and sha(NATIVE/"RESULT.json") == NATIVE_RESULT_SHA,
        "ADOPTED_OPTIMIZED_NATIVE_CHAIN")
    native_map = read(NATIVE/"source-map.json")
    rust_map = {name:pin for name,pin in native_map.items() if name.endswith(".rs")}
    need(len(rust_map) == 32 and type(selected["sources"]) is dict
        and set(selected["sources"]) == set(rust_map) | {ENTRY} | OVERLAYS | OWN
        and len(selected["sources"]) == 38,"EXACT_33_RUST_THREE_MANIFEST_TWO_ADAPTER_SOURCES")
    for name,pin in rust_map.items(): need(selected["sources"][name] == pin,"UNCHANGED_ADOPTED_NATIVE_SOURCE:"+name)
    need(selected["sources"][ENTRY]["sha256"] == ENTRY_SHA,"UNCHANGED_AGGREGATE_ENTRY")
    need(sum(pin["bytes"] for pin in selected["sources"].values()) <= 16*1024**2,"SOURCE_TOTAL_BOUND")
    comparison_pin = selected["native_comparison"]
    need(set(comparison_pin) == {"path","bytes","sha256"},"NATIVE_COMPARISON_PIN_FIELDS")
    comparison = Path(comparison_pin["path"])
    need(comparison.is_absolute() and comparison.resolve(strict=True) == comparison
        and comparison.parent.parent == HERE and comparison.name == "RESULT.json"
        and re.fullmatch(r"proof-validation-native-compare-[0-9]{2}",comparison.parent.name),"EXACT_NATIVE_COMPARISON_PATH")
    old_selection = read(BASE/"selection.json")
    preparation_pins = old_selection["preparation_sha256"]
    need(set(preparation_pins) == {"RESULT.json","SOURCE-MAP.json","LOCKS.json","UNIT-GRAPH.json",
        "DEPENDENCIES.json","CARGO-HOME.json","environment-profile.json","GRAPH-DELTA.json"},"EXACT_ADOPTED_PREPARATION")
    run = HERE/selected["name"]; attempt = HERE/(selected["name"]+"-attempt.json")

    def source_pins():
        need(time.monotonic()-started <= 1800 and time.process_time()-cpu <= 180,"GUEST_CONTROLLER_ENVELOPE")
        need(sha(clearance) == sys.argv[2],"SELECTION_CHANGED")
        for relative,pin in selected["sources"].items():
            need(set(pin) == {"bytes","sha256"} and type(pin["bytes"]) is int and 0 < pin["bytes"] <= 2*1024**2,
                "SOURCE_RECORD")
            path = ROOT/relative
            need(path.resolve(strict=True) == path and path.is_file()
                and path.stat().st_size == pin["bytes"] and sha(path) == pin["sha256"],"SOURCE_PIN:"+relative)
        for name,digest in BASE_PINS.items(): need(sha(BASE/name) == digest,"ADOPTED_RECORD_CHANGED:"+name)
        for name,digest in preparation_pins.items(): need(sha(PREP/name) == digest,"ADOPTED_PREPARATION_CHANGED:"+name)
        need(sha(PRIOR/"common03.py") == COMMON_SHA and sha(NATIVE/"source-map.json") == NATIVE_MAP_SHA
            and sha(NATIVE/"RESULT.json") == NATIVE_RESULT_SHA,"ADOPTED_HELPER_NATIVE_CHANGED")
        need(comparison.stat().st_size == comparison_pin["bytes"] and sha(comparison) == comparison_pin["sha256"]
            and not (comparison.parent/"FINALIZATION-FAILED.json").exists(),"NATIVE_COMPARISON_CHANGED")
        observed = read(comparison)
        need(observed["status"] == "PASS_TWO_RETAINED_NATIVE_DIFFERENTIALS"
            and observed["build_result"]["sha256"] == NATIVE_RESULT_SHA
            and read(HERE/(comparison.parent.name+"-attempt.json")) ==
                {"status":observed["status"],"result_sha256":comparison_pin["sha256"]},"ADOPTED_NATIVE_COMPARISON_PASS")

    source_pins()
    need(not run.exists() and not attempt.exists(),"FRESH_GUEST_BUILD")
    delta = load("aggregate_guest_graph",SOURCE/"graph.py",selected["sources"]["software/v5/aggregate_guest/graph.py"]["sha256"])
    k = load("aggregate_guest_common",PRIOR/"common03.py",COMMON_SHA)
    k.held.HERE,k.held.PREP,k.held.BUILD = HERE,run,run
    q,a,p,c,r,job = k.helpers()
    need(read(BASE/"RESULT.json")["status"] == "PASS_NEW_MODULE_GUEST_CROSS_BUILD_ONLY"
        and read(PREP/"RESULT.json")["status"] == "PASS_OFFLINE_RUINT_COMPATIBILITY_PREPARATION_ONLY",
        "ADOPTED_CLOSED_BASELINES")
    maps,locks = read(PREP/"SOURCE-MAP.json"),read(PREP/"LOCKS.json")
    seed = read(PREP/"CARGO-HOME.json")["seed_map"]
    baseline_map = read(BASE/"SOURCE-MAP.json")
    old_graph = read(BASE/"UNIT-GRAPH.json")
    state = maps["retained"]; library = k.LIBRARY
    project = run/"project"; wrapper = project/"software/v5/aggregate_guest"
    lock_bytes = delta.repin_lock((BASE/"project/modules/receipt/Cargo.lock").read_bytes())
    project_map = {**selected["sources"],"software/v5/aggregate_guest/Cargo.lock":
        {"bytes":len(lock_bytes),"sha256":hashlib.sha256(lock_bytes).hexdigest()}}
    snapshot_ready = False

    def rebind():
        source_pins()
        need(c.file_map(PREP/"project/guest") == maps["wrapper"]
            and c.file_map(PREP/"project/checker") == maps["checker"]
            and c.file_map(k.STDROOT) == maps["std"],"ADOPTED_PREPARATION_SOURCES")
        need(c.file_map(BASE/"project/modules/receipt") == baseline_map["wrapper"]
            and c.file_map(BASE/"project/modules/native/checker") == baseline_map["checker"],"ADOPTED_GUEST_SOURCES")
        need(a.pin(PREP/"project/guest/Cargo.lock") == locks["guest_after"]
            and a.pin(library/"Cargo.lock") == locks["std_after"],"ADOPTED_PREPARATION_LOCKS")
        need(k.cache_seed_map(c,PREP/"cargo-home") == seed and k.retained(c) == state,"RETAINED_SEED_SDK_RUNTIME")
        k.held.build_tools(c)
        if snapshot_ready:
            need(c.file_map(project) == project_map and sha(run/"selection.json") == sys.argv[2],"FRESH_PROJECT_CHANGED")

    rebind()
    run.mkdir(); a.DISK_LIMIT = LIMITS["combined_working_bytes"]
    retained = {key:0 for key in ("working_bytes","retained_archive_bytes","entries")}

    class Budget(a.Budget):
        def refresh(self):
            need(time.monotonic()-started <= 1800 and time.process_time()-cpu <= 180,"GUEST_TOTAL_ENVELOPE")
            measured = c.census(self.run)
            counters = ("working_bytes","retained_archive_bytes","entries")
            need(all(type(row[key]) is int and row[key] >= 0 for row in (measured,retained) for key in counters),
                "NUMERIC_CENSUS_COUNTERS")
            self.current = {key:measured[key]+retained[key] for key in counters}
            self.current["working_bytes"] += 3*1024**3
            self.current["retained_archive_bytes"] += 192*1024**2
            self.current["entries"] += 30000
            need(self.current["entries"] <= a.ENTRY_LIMIT,"COMBINED_ENTRY_LIMIT")
            self.check()

    budget = Budget(run,started+1800)
    phase = None
    result = {"schema":"DMKN_V5_AGGREGATE_GUEST_BUILD_RESULT_V1","status":"FAIL",
        "selection_sha256":sys.argv[2],"started_utc":p.utc(),"guest_executions":0,"proof_calls":0,
        "image_assembly_calls":0,"network_fetch_commands":0,"host_backend_builds":0,
        "scope":"OPTIMIZED_EXACT_WARRANT_AGGREGATE_GUEST_ELF_ONLY"}
    try:
        saved_scope = c.HERE
        try: c.HERE = PRIOR; retained = c.census(PREP); result["retained_preparation_census"] = retained
        finally: c.HERE = saved_scope
        budget.refresh(); (run/"commands").mkdir()
        raw_selection = clearance.read_bytes()
        need(hashlib.sha256(raw_selection).hexdigest() == sys.argv[2],"SELECTION_COPY_PIN")
        budget.precharge(len(raw_selection))
        with (run/"selection.json").open("xb") as stream: stream.write(raw_selection)
        c.copy_map(ROOT,project,selected["sources"],budget)
        budget.precharge(len(lock_bytes))
        with (wrapper/"Cargo.lock").open("xb") as stream: stream.write(lock_bytes)
        snapshot_ready = True
        a.save(run/"SOURCE-MAP.json",{"project":project_map,"std":maps["std"],"std_root":str(k.STDROOT),
            "retained":state,"origin":str(PREP),"baseline":str(BASE)})
        env,evidence = k.environment(p,c,run,library)
        env["CARGO_NET_OFFLINE"] = "true"
        c.copy_map(PREP/"cargo-home",run/"cargo-home",seed,budget)
        evidence.update(cargo_offline=True,fresh_source=str(project),no_old_build_target_reused=True)
        a.save(run/"environment-profile.json",evidence)
        rebind()
        phase = r.phase_class(p,a)("aggregate-guest-cross-build",run,budget,env,job.Job,1800)
        argv = [c.OLD/"rust/bin/cargo.exe","build","--release","--manifest-path",wrapper/"Cargo.toml",
            "--bin",delta.BINARY,"--target",delta.TARGET,"-Z","build-std=alloc,core,proc_macro,panic_abort,std",
            "-Z","build-std-features=compiler-builtins-mem","--locked","--offline"]
        graph_output = phase.invoke("offline-aggregate-graph",argv+["--unit-graph","-Z","unstable-options"],wrapper)
        graph = read(graph_output)
        graph_comparison = delta.verify_delta(old_graph,graph,BASE,run)
        a.save(run/"UNIT-GRAPH.json",graph); a.save(run/"GRAPH-COMPARISON.json",graph_comparison)
        rebind()
        output = phase.invoke("build-aggregate-guest",argv+["--message-format=json"],wrapper,allow_build_telemetry=True)
        binaries = set(); finished = []
        for line in output.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            if row.get("reason") == "build-finished": finished.append(row.get("success"))
            if row.get("reason") == "compiler-artifact" and row.get("target",{}).get("name") == delta.BINARY and row.get("executable"):
                need(row["target"]["kind"] == ["bin"] and row["profile"]["test"] is False
                    and row["profile"]["overflow_checks"] is True
                    and Path(row["target"]["src_path"]).resolve() == project/ENTRY,"EXACT_AGGREGATE_GUEST_ARTIFACT")
                binary = Path(row["executable"]).resolve(strict=True)
                need(binary.is_relative_to(run/"target"/delta.TARGET/"release"),"ARTIFACT_ESCAPE")
                binaries.add(binary)
        need(len(binaries) == 1 and finished == [True],"ONE_COMPLETED_AGGREGATE_GUEST_ELF")
        binary = next(iter(binaries)); link_map = run/"guest-link.map"
        need(link_map.is_file() and link_map.stat().st_size <= 32*1024**2,"LINK_MAP_BOUND")
        symbols = link_map.read_text(encoding="utf-8")
        need(re.search(r"\b_start\b",symbols) and re.search(r"\b__start\b",symbols),"SDK_STARTUP_SYMBOLS")
        artifact = {"user_elf":a.pin(binary),"elf_headers":k.elf_summary(binary),"link_map":a.pin(link_map),
            "scope":"New aggregate guest ELF only; no image adoption/execution/proof"}
        a.save(run/"ARTIFACT.json",artifact)
        result.update(status=PASS,artifact=artifact,graph_delta=graph_comparison)
    except BaseException as error: result["error"] = type(error).__name__+": "+str(error)[:4000]
    finally:
        if phase is not None:
            try: phase.close()
            except BaseException as error: result.update(status="FAIL_CLEANUP",cleanup_error=str(error)[:2000])
            result["job"],result["commands"] = phase.final_stats,phase.commands
        try:
            rebind()
            for name,pin in k.registry_archives(run/"cargo-home").items(): need(seed.get(name) == pin,"OFFLINE_ARCHIVE_CHANGED_OR_ADDED")
            budget.refresh(); result["new_final_storage"] = c.census(run)
        except BaseException as error: result.update(status="FAIL_FINAL_CHECK",final_check_error=str(error)[:2000])
        result.update(sampled_reserved_peaks=budget.peak,controller_cpu_seconds=time.process_time()-cpu,
            wall_seconds=time.monotonic()-started,finished_utc=p.utc(),
            accounting="CONTROLLER_DISJOINT_FROM_INCLUSIVE_WORKER_JOB;FINAL_REPORT_EXIT_TAIL_EXCLUDED")
        if result["wall_seconds"] > 1800: result["status"] = "FAIL_TOTAL_WALL_LIMIT"
        a.save(run/"RESULT.json",result)
        a.save(attempt,{"status":result["status"],"result_sha256":sha(run/"RESULT.json")})
        try: budget.refresh()
        except BaseException as error:
            result.update(status="FAIL_FINALIZATION",finalization_error=str(error)[:3000])
            a.save(run/"FINALIZATION-FAILED.json",{"status":"FAIL_FINALIZATION","overrides_result_and_attempt":True,
                "result_sha256":sha(run/"RESULT.json"),"error":str(error)[:3000]})
    print(json.dumps({key:result.get(key) for key in ("status","error","wall_seconds")}))
    return 0 if result["status"] == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
