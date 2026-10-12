"""One root-selected resolver-cache repair, with a finite selected input closure.

Private Cargo state and a fresh target; retained SDK/std/compiler are read-only.
This is a bounded trusted-build workflow, not a hostile-build-script sandbox.
No guest execution, image adoption, receipt production, or network fetch occurs.
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
import tomllib

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
SOURCE = ROOT / "software/v5/bounded_parse_guest"
OLD = HERE / "aggregate-guest-build-01"
COMPILE = HERE / "aggregate-guest-compile-01"
PREP = ROOT / "experiments/general-checker-guest-03/prepare-03"
NATIVE = HERE / "bounded-parse-native-build-02"
COMPARISON = HERE / "bounded-parse-native-compare-01"
FAILED = HERE / "bounded-parse-guest-build-01"
FAILED_ATTEMPT = HERE / "bounded-parse-guest-build-01-attempt.json"
STD = ROOT / "experiments/general-checker-guest-02/prepare-01/std-candidate"
LIBRARY = STD / "lib/rustlib/src/rust/library"
RUST = ROOT / "experiments/scale-crypto-01/runs/run-01/rust"
HOST = ROOT / "experiments/general-checker-guest-01/host-prepare-01"
SDK = HOST / "candidate/risc0-3bbcd44d6459b9ef6ac0df3846dc9215514934e8"
LLVM = ROOT / "software/runtime/lean-4.34.0-windows/bin"
COMMON = ROOT / "experiments/general-checker-guest-03/common03.py"
COMMON_SHA = "97116bd269dd784b9216833f6e0c0bf38e9d08c55af5927511a13b26194133d7"
RECIPE = ROOT / "software/v5/delta/NATIVE-BUILD02-PROPOSAL.json"
LOCK = OLD / "project/software/v5/aggregate_guest/Cargo.lock"
NATIVE_PASS = "PASS_BOUNDED_PARSE_TWO_REMAINING_LINKS_ONLY"
COMPARISON_PASS = "PASS_BOUNDED_PARSE_TEN_CONTROLS_TWO_NATIVE_DIFFERENTIALS"
PASS = "PASS_BOUNDED_PARSE_EXACT_GRAPH_GUEST_BUILD_ONLY"
RECORDS = {
    FAILED / "RESULT.json": "1f97e4d5c3a6f0c9d704970adcc91a128eb237d541fa71365a99690c1c58d8e8",
    FAILED / "commands/offline-bounded-graph/command.json": "024431af99a84c2ff4ea404f5a671174c224c3452c355467c64475b3c8409c55",
    FAILED / "commands/offline-bounded-graph/stderr.txt": "a54f0ca1f3b418c6a04ed5833b4d5f8d9d11daeb525c80fdf4013b8de872767a",
    FAILED / "selection.json": "be47024a42da96b5d33dcbea8e9ffcc4f2d81be50cc30a1f58ff0b2d4da0e41d",
    FAILED_ATTEMPT: "3ea21a5d9200340ec10763da83e42290b68cc6142b87f94a42f2bb5166411af2",
    COMPILE / "SOURCE-MAP.json": "75c710e3ee13f63cb6ef44da8656caa53c300bf649317d2b5669d8b9cde06ce0",
    COMPILE / "environment-profile.json": "7e1b195a0e075eec9ba8f0d7f8e65c83a9a3cebfc3332e7910d9909be2581ff5",
    OLD / "commands/offline-aggregate-graph/stdout.txt": "2cc441345c1cf3cc16e9dd21cca1bf2130319dbfa1124ad3ddb1d6507f2f4609",
    LOCK: "13381f3226dfb40e766fda448adaa4a75f407da0d31114964d1278991a6f1b7c",
    LIBRARY / "Cargo.lock": "207129d8edc2cb762f8556dce440012854d28ca2d8774852fb00ee0a32191fc5",
    PREP / "CARGO-HOME.json": "474c01d941c61e37e744bd0bdd74e2193c46cc3b3ff320fcef449230570f3ab4",
    NATIVE / "RESULT.json": "026770a3a3f1a74e04b872a13b4572471048362514c52ca2aea2179d7e8ba3b1",
    NATIVE / "source-map.json": "5eed690e54ab6a42f8cc3da93c93901aae18c4c5ad441851df072dfd91f81f54",
    NATIVE / "selection.json": "c979e61ee56d9a8eed083971df2dde7d2cb6842999e17a2b46545eee487953aa",
    HERE / "bounded-parse-native-build-02-selection.json": "15cea3f094621d1d1e8901219db2caa2eb4e9ea2951232008e9e21503895640f",
    COMPARISON / "RESULT.json": "ddd411125b809fda24be93280329f6d7b7bd3d4b32ac5cbd71beab46e4948a20",
    RECIPE: "b0d037459b950c3cbabd1c2554aebf1fe9611820598d370eb40f4d69e700885d",
    COMMON: COMMON_SHA,
    ROOT / "experiments/general-checker-guest-02/common_build02.py":
        "f28d18457b2ef465b14c44dd2fec15d4386f640f9bbdf627398d5dcf46a7f11c",
}
PRODUCTION = {"software/v5/bounded_parse/" + name + ".rs" for name in (
    "canonical", "module_relation", "module_lib", "census", "aggregate_relation", "aggregate_lib")}
REUSED = {"software/v5/modules/receipt/src/" + name + ".rs" for name in (
    "input", "foundation_static", "foundation_data", "commitments", "journal", "policy")}
REUSED.update({"software/v5/aggregate_claims/" + name + ".rs" for name in ("header", "membership", "wire")})
REUSED.update({"software/v5/modules/native/checker/src/" + name + ".rs" for name in (
    "debug_printer", "demand", "env", "expr", "inductive", "level", "module", "name",
    "parser", "pretty_printer", "quot", "tc", "unique_hasher", "util")})
REUSED.update({"software/v5/modules/native/proof_validation/lib.rs",
               "software/v5/modules/native/proof_validation/module_correspondence.rs",
               "software/v5/aggregate/main.rs"})
OWN = {"software/v5/bounded_parse_guest/" + name for name in (
    "Cargo.toml", "module/Cargo.toml", "checker/Cargo.toml", "graph.py",
    "cache_resolver.py", "build_resolver.py")}
SDK_ROOTS = ("risc0/binfmt/", "risc0/build_kernel/", "risc0/circuit/keccak/",
    "risc0/circuit/recursion/", "risc0/circuit/rv32im/", "risc0/circuit/rv32im-sys/",
    "risc0/core/", "risc0/groth16/", "risc0/zkos/common/", "risc0/zkos/v1compat/",
    "risc0/zkp/", "risc0/zkvm/", "risc0/zkvm/platform/")
LIMITS = {"worker_cpu_seconds": 480, "worker_wall_seconds": 600, "memory_mib": 4096,
    "active_processes": 8, "controller_cpu_seconds": 90, "ordinary_controller_cpu_seconds": 70,
    "total_wall_seconds": 780, "fresh_output_bytes": 3*1024**3,
    "fresh_output_entries": 32768, "command_log_bytes": 32*1024**2}


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
        allowed = LIMITS["controller_cpu_seconds"] if finalizing else LIMITS["ordinary_controller_cpu_seconds"]
        need(time.process_time() - cpu <= allowed and time.monotonic() - started <= LIMITS["total_wall_seconds"],
             "CONTROLLER_ENVELOPE_WITH_FINALIZATION_RESERVE")

    need(os.name == "nt" and Path.cwd() == ROOT and Path(__file__).resolve() == SOURCE / "build_resolver.py"
         and sys.dont_write_bytecode and sys.flags.isolated and sys.flags.no_site
         and not sys.flags.optimize and len(sys.argv) == 3, "ISOLATED_CANONICAL_GUEST_BUILD")
    clearance = Path(sys.argv[1]).resolve(strict=True)
    need(clearance.is_relative_to(HERE) and clearance.stat().st_size <= 65536
         and sha(clearance) == sys.argv[2], "EXACT_GUEST_SELECTION_PIN")
    selected = read(clearance)
    need(set(selected) == {"schema", "name", "sources", "limits", "native_comparison",
        "authorizes_guest_build_and_owned_telemetry_cleanup"}
        and selected["schema"] == "DMKN_V5_BOUNDED_PARSE_RESOLVER_GUEST_BUILD_V1"
        and selected["authorizes_guest_build_and_owned_telemetry_cleanup"] is True
        and selected["limits"] == LIMITS and type(selected["name"]) is str
        and selected["name"] == "bounded-parse-guest-build-02", "GUEST_SELECTION_FIELDS")
    need(type(selected["sources"]) is dict and set(selected["sources"]) == PRODUCTION | REUSED | OWN
         and len(selected["sources"]) == 38 and len(PRODUCTION | REUSED) == 32, "EXACT_38_SOURCE_SET")
    for path, digest in RECORDS.items():
        envelope()
        need(sha(path) == digest, "RETAINED_RECORD_PIN:" + str(path))
    failed = read(FAILED / "RESULT.json")
    need(failed["status"] == "FAIL" and failed["error"] ==
         "RuntimeError: UNEXPECTED_CHILD_EXIT offline-bounded-graph"
         and failed["selection_sha256"] == RECORDS[FAILED / "selection.json"]
         and failed["job"]["cpu_seconds"] == 0.75
         and failed["controller_cpu_seconds"] == 19.375
         and failed["wall_seconds"] == 89.82956409989856
         and failed["job"]["active_processes"] == failed["job"]["terminated_processes"] == 0
         and len(failed["commands"]) == 1
         and failed["commands"][0]["label"] == "offline-bounded-graph"
         and failed["commands"][0]["exit_code"] == 101
         and all(failed[key] == 0 for key in ("guest_calls", "proof_calls", "receipt_calls",
                                             "image_assembly_calls", "network_fetch_commands")),
         "EXACT_RETAINED_RESOLVER_FAILURE_AND_COSTS")
    failed_selection = read(FAILED / "selection.json")
    inherited = PRODUCTION | REUSED | {name for name in OWN if not name.endswith(
        ("cache_resolver.py", "build_resolver.py"))}
    need(failed_selection["schema"] == "DMKN_V5_BOUNDED_PARSE_GUEST_BUILD_V1"
         and failed_selection["name"] == FAILED.name
         and len(inherited) == 36
         and all(selected["sources"][name] == failed_selection["sources"][name] for name in inherited),
         "UNCHANGED_32_RUST_THREE_MANIFESTS_AND_GRAPH")
    failure_evidence = {
        "result": {"path": str(FAILED / "RESULT.json"), "sha256": RECORDS[FAILED / "RESULT.json"]},
        "attempt_sha256": RECORDS[FAILED_ATTEMPT],
        "command_sha256": RECORDS[FAILED / "commands/offline-bounded-graph/command.json"],
        "stderr_sha256": RECORDS[FAILED / "commands/offline-bounded-graph/stderr.txt"],
        "selection_sha256": RECORDS[FAILED / "selection.json"],
        "status": failed["status"], "worker_cpu_seconds": failed["job"]["cpu_seconds"],
        "controller_cpu_seconds": failed["controller_cpu_seconds"],
        "wall_seconds": failed["wall_seconds"],
        "accounting": "PRESERVED_PREDECESSOR_COSTS_NOT_ERASED_OR_RENEWED_BY_SUCCESSOR",
    }
    comparison_pin = selected["native_comparison"]
    need(comparison_pin == {"path": str(COMPARISON / "RESULT.json"), "bytes": 8960,
                           "sha256": RECORDS[COMPARISON / "RESULT.json"]}, "EXACT_NATIVE_COMPARISON_PIN")
    old_map = read(COMPILE / "SOURCE-MAP.json")
    native_map = read(NATIVE / "source-map.json")
    for relative in REUSED:
        need(selected["sources"][relative] == old_map["project"][relative], "UNCHANGED_GUEST_SOURCE:" + relative)
    for relative in PRODUCTION:
        need(selected["sources"][relative] == native_map[relative], "NATIVE_PRODUCTION_SOURCE:" + relative)
    for relative in REUSED & set(native_map):
        need(selected["sources"][relative] == native_map[relative], "NATIVE_REUSED_SOURCE:" + relative)
    native, compared = read(NATIVE / "RESULT.json"), read(COMPARISON / "RESULT.json")
    need(native["status"] == NATIVE_PASS and compared["status"] == COMPARISON_PASS
         and compared["build_result"] == {"path": str(NATIVE / "RESULT.json"), "bytes": 18078,
                                         "sha256": RECORDS[NATIVE / "RESULT.json"]}, "NATIVE_COMPARISON_LINEAGE")
    need(read(NATIVE / "selection.json")["sources"] == native_map, "NATIVE_MAP_SELECTION_LINEAGE")
    native_selection = HERE / "bounded-parse-native-build-02-selection.json"
    need(sha(native_selection) == native["selection_sha256"]
         and read(native_selection) == read(NATIVE / "selection.json"), "NATIVE_SELECTION_HASH_AND_SAVED_VALUE")
    run = HERE / selected["name"]
    attempt = HERE / (selected["name"] + "-attempt.json")
    need(not run.exists() and not attempt.exists(), "FRESH_GUEST_OUTPUT")
    g = load("bounded_guest_graph", SOURCE / "graph.py", selected["sources"]["software/v5/bounded_parse_guest/graph.py"]["sha256"])
    cache = load("bounded_guest_resolver_cache", SOURCE / "cache_resolver.py",
                 selected["sources"]["software/v5/bounded_parse_guest/cache_resolver.py"]["sha256"])
    k = load("bounded_guest_common", COMMON, COMMON_SHA)
    k.held.HERE = HERE
    q, a, p, c, r, job = k.helpers()
    r.LOG_LIMIT = LIMITS["command_log_bytes"]
    a.DISK_LIMIT, a.ENTRY_LIMIT = LIMITS["fresh_output_bytes"], LIMITS["fresh_output_entries"]
    old_graph = read(OLD / "commands/offline-aggregate-graph/stdout.txt")
    lock_bytes, std_lock = LOCK.read_bytes(), (LIBRARY / "Cargo.lock").read_bytes()
    g.canonical_graph(old_graph)
    seed, cache_selection = cache.cache_inputs(
        old_graph, lock_bytes, std_lock, read(PREP / "CARGO-HOME.json")["seed_map"])
    sdk_map = {name: pin for name, pin in old_map["retained"]["sdk_map"].items()
               if name.startswith(SDK_ROOTS) or Path(name).name == "Cargo.toml"
               or name in {"Cargo.lock", ".cargo/config.toml", "rust-toolchain.toml"}}
    rust_map = {name: pin for name, pin in old_map["retained"]["runtime"].items()
                if name in {"bin/cargo.exe", "bin/rustc.exe", "lib/rustlib/x86_64-pc-windows-msvc/bin/rust-lld.exe"}
                or (name.startswith("bin/") and name.endswith(".dll"))
                or (name.startswith("lib/rustlib/x86_64-pc-windows-msvc/lib/") and name.endswith((".rlib", ".rmeta")))}
    need(old_map["retained"]["sdk"] == str(SDK)
         and len(sdk_map) == 982 and sum(pin["bytes"] for pin in sdk_map.values()) == 43906906,
         "EXACT_GRAPH_SDK_INPUT_MAP")
    need(len(old_map["std"]) == 2192 and sum(pin["bytes"] for pin in old_map["std"].values()) == 37544099,
         "EXACT_STD_INPUT_MAP")
    need(len(rust_map) == 27 and sum(pin["bytes"] for pin in rust_map.values()) == 423009292,
         "EXACT_COMPILER_RUNTIME_MAP")
    # Bind all helper code loaded by the retained supervisor, without invoking
    # any old full-tree provenance or cache-census routine.
    digests = dict(RECORDS)
    digests.update({ROOT / "experiments/general-checker-guest-01/prepare.py": k.held.HOST_PREPARE_SHA,
        ROOT / "experiments/scale-equation-01/runtime.py": q.RUNTIME_SHA,
        p.PYTHON: p.PYTHON_SHA, p.PYTHON.parent / "python314.dll": p.PYTHON_DLL_SHA,
        p.HELPERS / "run_stage.py": p.HELPER_SHA, p.HELPERS / "domains.py": p.DOMAINS_SHA,
        r.VCTIP: r.VCTIP_SHA, clearance: sys.argv[2]})
    digests.update({q.CRYPTO / name: digest for name, digest in q.HELPERS.items()})
    profile = read(COMPILE / "environment-profile.json")
    exact_inputs = {}

    def include(path, pin):
        need(set(pin) == {"bytes", "sha256"} and type(pin["bytes"]) is int
             and 0 <= pin["bytes"] <= 512*1024**2 and re.fullmatch(r"[0-9a-f]{64}", pin["sha256"]), "INPUT_PIN_SCHEMA")
        need(path.is_absolute() and (str(path) not in exact_inputs or exact_inputs[str(path)] == pin), "INPUT_PIN_CONFLICT")
        exact_inputs[str(path)] = dict(pin)

    for base, rows in ((ROOT, selected["sources"]), (SDK, sdk_map), (STD, old_map["std"]),
                       (RUST, rust_map), (PREP / "cargo-home", seed)):
        for relative, pin in rows.items():
            a.safe_parts(relative)
            include(base / relative, pin)
    # Only the retained 98 C: host-tool/library pins, not unrelated native rlibs.
    recipe = read(RECIPE)
    host_pins = {Path(name): digest for name, digest in recipe["runtime_pins_rechecked"].items()
                if Path(name).drive.lower() == "c:"}
    need(len(host_pins) == 98, "EXACT_HOST_LINK_INPUT_SET")
    digests.update(host_pins)
    for path, digest in digests.items():
        envelope()
        include(path, {"bytes": path.stat().st_size, "sha256": digest})
    for name in ("bin/cargo-fmt.exe", "bin/rustfmt.exe"):
        include(HOST / "fmt" / name, profile["additional_tool_pins"]["rustfmt"][name])
    for pin in [*profile["additional_tool_pins"]["clang"].values(), *profile["host_binaries"]]:
        include(Path(pin["path"]), {key: pin[key] for key in ("bytes", "sha256")})
    lock_relative = "software/v5/bounded_parse_guest/Cargo.lock"
    project_map = {**selected["sources"], lock_relative: {"bytes": len(lock_bytes), "sha256": RECORDS[LOCK]}}
    project, wrapper = run / "project", run / "project/software/v5/bounded_parse_guest"
    absent_configs = sorted({str(base / ".cargo" / name)
                             for base in (wrapper, *wrapper.parents) for name in ("config", "config.toml")}
                            | {str(run / "cargo-home" / name) for name in ("config", "config.toml")})
    snapshot_ready = cache_ready = False

    def bind(path, pin):
        envelope()
        need(path.resolve(strict=True) == path and path.is_file(), "EXACT_INPUT_PATH:" + str(path))
        a.regular_stat(path, allow_hardlinks=True)
        need(path.stat().st_size == pin["bytes"] and sha(path) == pin["sha256"], "INPUT_CHANGED:" + str(path))
        envelope()

    def rebind():
        need(not (FAILED / "FINALIZATION-FAILED.json").exists()
             and read(FAILED_ATTEMPT) == {"status": "FAIL",
                 "result_sha256": RECORDS[FAILED / "RESULT.json"]}, "RETAINED_FAILED_OPERATION_FINALIZATION")
        for name in absent_configs:
            need(not Path(name).exists(), "UNSELECTED_CARGO_CONFIG:" + name)
        for name, pin in exact_inputs.items():
            bind(Path(name), pin)
        for retained, status in ((NATIVE, NATIVE_PASS), (COMPARISON, COMPARISON_PASS)):
            need(not (retained / "FINALIZATION-FAILED.json").exists()
                 and read(HERE / (retained.name + "-attempt.json")) == {
                     "status": status, "result_sha256": RECORDS[retained / "RESULT.json"]}, "ADOPTED_NATIVE_FINALIZATION")
        if snapshot_ready:
            for relative, pin in project_map.items():
                bind(project / relative, pin)
            need(c.file_map(project) == project_map, "NO_UNSELECTED_PROJECT_INPUT")
            need(sha(run / "selection.json") == sys.argv[2], "SAVED_SELECTION_CHANGED")
        if cache_ready:
            for relative, pin in seed.items():
                bind(run / "cargo-home" / relative, pin)

    rebind()
    run.mkdir()

    class Budget(a.Budget):
        def check(self):
            envelope()
            need(self.current["entries"] <= LIMITS["fresh_output_entries"], "FRESH_OUTPUT_ENTRY_LIMIT")
            super().check()
        def refresh(self):
            envelope()
            self.current = {key: value for key, value in c.census(run).items()
                            if key in ("working_bytes", "retained_archive_bytes", "entries")}
            self.check()

    budget = Budget(run, started + LIMITS["total_wall_seconds"])
    phase = None
    result = {"schema": "DMKN_V5_BOUNDED_PARSE_RESOLVER_GUEST_BUILD_RESULT_V1", "status": "FAIL",
        "predecessor_failure": failure_evidence, "resolver_cache_selection": cache_selection,
        "selection_sha256": sys.argv[2], "limits": LIMITS, "guest_calls": 0, "proof_calls": 0,
        "receipt_calls": 0, "image_assembly_calls": 0, "network_fetch_commands": 0,
        "authority": "NEW_GUEST_ELF_ONLY_NOT_IMAGE_OR_MATHEMATICAL_ADMISSION", "started_utc": p.utc()}
    try:
        (run / "commands").mkdir()
        raw = clearance.read_bytes()
        need(hashlib.sha256(raw).hexdigest() == sys.argv[2], "SELECTION_COPY_CHANGED")
        with (run / "selection.json").open("xb") as stream:
            stream.write(raw)
        c.copy_map(ROOT, project, selected["sources"], budget)
        budget.precharge(len(lock_bytes))
        with (wrapper / "Cargo.lock").open("xb") as stream:
            stream.write(lock_bytes)
        snapshot_ready = True
        # The four lib/main targets must be exact fresh snapshot files, even
        # though Cargo's graph retains lexical `..` in src_path.
        targets = []
        for relative in ("Cargo.toml", "module/Cargo.toml", "checker/Cargo.toml"):
            manifest = wrapper / relative
            metadata = tomllib.loads(manifest.read_text(encoding="utf-8"))
            for target in [metadata["lib"], *metadata.get("bin", [])]:
                path = (manifest.parent / target["path"]).resolve(strict=True)
                need(path.is_relative_to(project) and path.relative_to(project).as_posix() in project_map,
                     "LOCAL_TARGET_OUTSIDE_SELECTED_SNAPSHOT")
                targets.append(str(path))
        need(len(targets) == len(set(targets)) == 4, "EXACT_FOUR_LOCAL_SOURCE_TARGETS")
        a.save(run / "INPUT-MAP.json", {"inputs": exact_inputs, "sdk_packages": list(SDK_ROOTS),
            "absent_cargo_configuration": absent_configs,
            "sdk_file_count": len(sdk_map), "std_file_count": len(old_map["std"]),
            "compiler_file_count": len(rust_map), "cache_file_count": len(seed),
            "trust_boundary": "Retained trusted toolchain/build scripts plus Windows OS/system DLLs; not hermetic or sandboxed"})
        a.save(run / "CACHE-SELECTION.json", cache_selection)
        a.save(run / "SOURCE-MAP.json", {"project": project_map, "targets": targets,
            "native_result_sha256": RECORDS[NATIVE / "RESULT.json"],
            "native_comparison_sha256": RECORDS[COMPARISON / "RESULT.json"]})
        env, evidence = p.environment(run, RUST)
        env.update({"CXX": str(LLVM / "clang.exe"), "CXXFLAGS": "--target=x86_64-pc-windows-msvc",
            "CARGO_NET_OFFLINE": "true", "VCToolsUserTelemetryOptOut": "1",
            "__CARGO_TESTS_ONLY_SRC_ROOT": str(LIBRARY),
            "CARGO_TARGET_RISCV32IM_RISC0_ZKVM_ELF_LINKER": profile["guest_linker"]})
        env["PATH"] = os.pathsep.join((str(HOST / "fmt/bin"), str(LLVM), env["PATH"]))
        flags = list(profile["guest_rustflags"])
        need(flags[-2:] == ["-C", "link-arg=-Map=" + str(COMPILE / "guest-link.map")], "EXACT_OLD_MAP_FLAG")
        flags[-1] = "link-arg=-Map=" + str(run / "guest-link.map")
        env["CARGO_ENCODED_RUSTFLAGS"] = "\x1f".join(flags)
        evidence.update(environment_keys_only=sorted(env), guest_rustflags=flags,
            explicit_environment=env, fresh_target=True, offline=True, verbose_commands=True,
            std_library=str(LIBRARY), selected_input_map_sha256=sha(run / "INPUT-MAP.json"))
        a.save(run / "environment-profile.json", evidence)
        c.copy_map(PREP / "cargo-home", run / "cargo-home", seed, budget)
        cache_ready = True
        rebind()

        class InclusiveJob(job.Job):
            def stats(self):
                measured = super().stats()
                # The native Job cap is user CPU time. Enforce the selected
                # inclusive kernel+user cap at every retained phase poll too.
                # Finalization must still read over-budget stats for cleanup
                # and evidence; its explicit final check refuses them.
                if not finalizing:
                    need(measured["cpu_seconds"] <= 480, "SHARED_INCLUSIVE_WORKER_CPU_LIMIT")
                return measured

        def exact_job(seconds, memory, active_processes):
            need(seconds == 600 and memory == 4096 and active_processes == 8, "SHARED_JOB_PROFILE")
            return InclusiveJob(480, 4096, active_processes=8)

        phase = r.phase_class(p, a)("bounded-parse-guest-build", run, budget, env, exact_job, 600)
        argv = [RUST / "bin/cargo.exe", "build", "--release", "--manifest-path", wrapper / "Cargo.toml",
            "--bin", g.BINARY, "--target", g.TARGET, "-Z", "build-std=alloc,core,proc_macro,panic_abort,std",
            "-Z", "build-std-features=compiler-builtins-mem", "--locked", "--offline"]
        graph_out = phase.invoke("offline-bounded-graph", argv + ["--unit-graph", "-Z", "unstable-options"], wrapper)
        graph = read(graph_out)
        comparison = g.verify_graph(old_graph, graph, run)
        a.save(run / "UNIT-GRAPH.json", graph)
        a.save(run / "GRAPH-COMPARISON.json", comparison)
        rebind()
        output = phase.invoke("build-bounded-guest", argv + ["-vv", "--message-format=json"], wrapper,
                              allow_build_telemetry=True)
        binaries, finished = set(), []
        for line in output.read_text(encoding="utf-8").splitlines():
            envelope()
            row = json.loads(line)
            if row.get("reason") == "build-finished":
                finished.append(row.get("success"))
            if row.get("reason") == "compiler-artifact" and row.get("target", {}).get("name") == g.BINARY and row.get("executable"):
                need(row["target"]["kind"] == ["bin"] and row["profile"]["test"] is False
                     and row["profile"]["overflow_checks"] is True
                     and Path(row["target"]["src_path"]).resolve() == project / "software/v5/aggregate/main.rs",
                     "EXACT_GUEST_ARTIFACT")
                binary = Path(row["executable"]).resolve(strict=True)
                need(binary.is_relative_to(run / "target" / g.TARGET / "release"), "ARTIFACT_ESCAPE")
                binaries.add(binary)
        need(len(binaries) == 1 and finished == [True], "ONE_COMPLETED_GUEST_ELF")
        binary = next(iter(binaries))
        link_map = run / "guest-link.map"
        need(link_map.is_file() and link_map.stat().st_size <= 32*1024**2, "LINK_MAP_BOUND")
        symbols = link_map.read_text(encoding="utf-8")
        need(re.search(r"\b_start\b", symbols) and re.search(r"\b__start\b", symbols), "SDK_STARTUP_SYMBOLS")
        artifact = {"user_elf": a.pin(binary), "elf_headers": k.elf_summary(binary), "link_map": a.pin(link_map)}
        a.save(run / "ARTIFACT.json", artifact)
        result.update(status=PASS, artifact=artifact, graph_comparison=comparison)
    except BaseException as error:
        result["error"] = type(error).__name__ + ": " + str(error)[:4000]
    finally:
        finalizing = True
        if phase is not None:
            try:
                phase.close()
                need(phase.final_stats["cpu_seconds"] <= 480 and phase.final_stats["active_processes"] == 0,
                     "SHARED_JOB_FINAL_BUDGET")
            except BaseException as error:
                result.update(status="FAIL_CLEANUP", cleanup_error=str(error)[:2000])
            result["job"], result["commands"] = phase.final_stats, phase.commands
        try:
            rebind()
            # Only the new cache tree is inspected for unexpected archives;
            # no retained-history or SDK census occurs at finalization.
            if cache_ready:
                archive_names = {path.relative_to(run / "cargo-home").as_posix()
                                 for path in (run / "cargo-home/registry/cache").rglob("*.crate")}
                need(archive_names == {name for name in seed if name.endswith(".crate")}, "NO_UNSELECTED_ARCHIVES")
            budget.refresh()
        except BaseException as error:
            result.update(status="FAIL_FINAL_CHECK", final_check_error=str(error)[:3000])
        result.update(sampled_peaks=budget.peak, output_census=budget.current,
            controller_cpu_seconds=time.process_time() - cpu, wall_seconds=time.monotonic() - started,
            finished_utc=p.utc(), accounting="CONTROLLER_DISJOINT_FROM_INCLUSIVE_WORKER_JOB;FINAL_REPORT_EXIT_TAIL_EXCLUDED")
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
