"""One selected po17 snapshot-host link using the retained corrected libraries.

No execution on import, Cargo, library rebuild, host invocation or proof. This
is an owner-controlled trusted compilation, not a hostile-source sandbox.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import re
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
SOURCE = ROOT / "software/v5/aggregate_geometry"
OLD = HERE / "prover-allocation-build-01"
OLD_SELECTION = HERE / "prover-allocation-build-01-selection.json"
OLD_ATTEMPT = HERE / "prover-allocation-build-01-attempt.json"
RUST = ROOT / "experiments/scale-crypto-01/runs/run-01/rust"
SUPPORT = ROOT / "software/v5/modules/native/proof_validation/control.py"
SUPPORT_SHA = "91e25c3a3244a106c01ce18da63b07a163b0d07e53eddcf5376b399ee22a9ca1"
SCHEMA = "DMKN_V5_GEOMETRY17_SNAPSHOT_HOST_BUILD"
PASS = "PASS_GEOMETRY17_SNAPSHOT_HOST_ONE_LINK_ONLY"
OLD_PASS = "PASS_PROVER_ALLOCATION_FIVE_STEP_COMPILE_ONLY"
NAMES = ("risc0_circuit_rv32im", "risc0_zkvm", "dmkn_module_relation",
         "dmkn_aggregate_relation", "small_aggregate_stage_host")
RECORDS = {
    OLD / "RESULT.json": "ac259e9db55275a0a8404e9cf881fd3779f2e7259ccfe134c8e93e3b180b4102",
    OLD / "compile-commands.json": "55ead9865ee0c2dcbb4ee667bc99a24bb9afe6ec095f0a3c2b91913d8293e03e",
    OLD / "environment-profile.json": "ae9c06c986ab9f325fb5624d6d9b39392383c98093e60168e023d3b84c407b05",
    OLD / "source-map.json": "dc7cfeba823551159f93f9add5ac10031a335079de6682d886dd792646f75f3f",
    OLD / "INPUT-MAP.json": "91d7d7fb56353eb19671a09d7e70686a110e100beefbf51f2be48c362d03f63f",
    OLD_SELECTION: "7a548b3f74c0c5bbe8bc2ba68e408a3dfdf22addefb9410b1a25f5d8be5d13ff",
    OLD_ATTEMPT: "2c61fd2ca46d86fe2d179f8728483bb5c1c207f248ab83f4bc4db4f273afb1e6",
}
SOURCE_SET = {"software/v5/aggregate_geometry/build_snapshot.py",
              "software/v5/aggregate_geometry/aggregate_host.rs", "software/v5/aggregate/receipt.rs"}
RECEIPT = {"bytes": 3631, "sha256": "41db7677d40af4fd779159e8442724bff7842b7f4e5745411e5846d8e7678254"}
COUNTS = {"backend_rust_crate_rebuilds": 0, "relation_rust_crate_rebuilds": 0,
          "snapshot_host_links": 1, "stage_host_links": 0, "checker_rebuilds": 0,
          "native_circuit_rebuilds": 0, "guest_rebuilds": 0,
          "host_calls": 0, "guest_calls": 0, "proof_calls": 0, "network_calls": 0}
LIMITS = {"worker_cpu_seconds": 240, "worker_wall_seconds": 300, "memory_mib": 1536,
          "active_processes": 6, "ordinary_controller_cpu_seconds": 40,
          "controller_cpu_seconds": 60, "total_wall_seconds": 420,
          "fresh_output_bytes": 536870912, "fresh_output_entries": 8192,
          "command_log_bytes": 1048576}


def need(value, reason):
    if not value:
        raise ValueError(reason)


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def pairs(items):
    value = {}
    for key, item in items:
        need(key not in value, "DUPLICATE_JSON_FIELD")
        value[key] = item
    return value


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def read(path):
    need(path.stat().st_size <= 2 * 1024**2, "ADMIN_INPUT_BYTES")
    return json.loads(path.read_bytes(), object_pairs_hook=pairs,
                      parse_constant=lambda value: need(False, "NONFINITE_JSON"))


def save(path, value):
    with path.open("xb") as stream:
        stream.write((json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode())


def pin(path):
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha(path)}


def check_pin(path, expected):
    need(type(expected) is dict and set(expected) == {"bytes", "sha256"}
         and type(expected["bytes"]) is int and expected["bytes"] > 0
         and type(expected["sha256"]) is str
         and re.fullmatch(r"[0-9a-f]{64}", expected["sha256"]), "PIN_FIELDS")
    need(path.is_absolute() and path.resolve(strict=True) == path and path.is_file()
         and path.stat().st_size == expected["bytes"] and sha(path) == expected["sha256"],
         "FILE_PIN:" + str(path))


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
        need(time.monotonic() - started <= LIMITS["total_wall_seconds"]
             and time.process_time() - cpu <= cap, "ONE_TOTAL_CLOCK_AND_CONTROLLER_RESERVE")

    need(os.name == "nt" and Path.cwd() == ROOT
         and Path(__file__).resolve() == SOURCE / "build_snapshot.py"
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize and len(sys.argv) == 3, "EXACT_OWNER_INVOCATION")
    selection = Path(sys.argv[1]).resolve(strict=True)
    need(selection.parent == HERE and re.fullmatch(r"[0-9a-f]{64}", sys.argv[2])
         and sha(selection) == sys.argv[2], "EXACT_SELECTION")
    chosen = read(selection)
    need(set(chosen) == {"schema", "name", "authorizes_compile_only", "sources", "runtime_pins", "limits"}
         and chosen["schema"] == SCHEMA + "_V1" and chosen["authorizes_compile_only"] is True
         and type(chosen["name"]) is str
         and re.fullmatch(r"geometry17-snapshot-host-build-[0-9]{2}", chosen["name"])
         and encoded(chosen["limits"]) == encoded(LIMITS), "SELECTION_FIELDS")
    need(type(chosen["sources"]) is dict and set(chosen["sources"]) == SOURCE_SET
         and encoded(chosen["sources"]["software/v5/aggregate/receipt.rs"]) == encoded(RECEIPT),
         "THREE_SOURCE_CLOSURE_WITH_UNCHANGED_RECEIPT")
    for path, digest in RECORDS.items():
        envelope()
        need(path.resolve(strict=True) == path and sha(path) == digest, "RETAINED_BUILD_RECORD:" + str(path))
    prior, old_selection = read(OLD / "RESULT.json"), read(OLD_SELECTION)
    old_commands = read(OLD / "compile-commands.json")
    old_environment = read(OLD / "environment-profile.json")
    need(prior["status"] == OLD_PASS and prior["schema"] == "DMKN_V5_PROVER_ALLOCATION_BUILD_RESULT_V1"
         and prior["selection_sha256"] == RECORDS[OLD_SELECTION]
         and prior["commands_sha256"] == RECORDS[OLD / "compile-commands.json"]
         and prior["environment_sha256"] == RECORDS[OLD / "environment-profile.json"]
         and prior["source_map_sha256"] == RECORDS[OLD / "source-map.json"]
         and prior["input_map_sha256"] == RECORDS[OLD / "INPUT-MAP.json"]
         and prior["job"]["active_processes"] == prior["job"]["terminated_processes"] == 0
         and len(prior["commands"]) == len(old_commands) == 5
         and tuple(row["name"] for row in old_commands) == NAMES, "EXACT_SUCCESSFUL_REFINED_BUILD")
    for actual, planned in zip(prior["commands"], old_commands):
        need(actual["argv"] == planned["argv"] and actual["cwd"] == str(ROOT)
             and actual["status"] == "COMMAND_COMPLETED" and actual["exit_code"] == 0
             and actual["cleanup_errors"] == [] and actual["job_after"]["active_processes"] == 0
             and actual["job_after"]["terminated_processes"] == 0, "RETAINED_FIVE_CLEAN_COMMANDS")
    refined = {name: prior["outputs"][name] for name in NAMES[:4]}
    need(len({item["path"] for item in refined.values()}) == 4, "DISTINCT_REFINED_LIBRARIES")
    for name, item in refined.items():
        need(set(item) == {"path", "bytes", "sha256"}
             and Path(item["path"]) == OLD / "lib" / ("lib" + name + "-a53940b67580e215.rlib"),
             "EXACT_REFINED_LIBRARY_PATH")
    # The first library is a transitive edge of corrected zkvm, not a fourth
    # direct --extern on the host. Preserve and bind the actual old command DAG.
    for index, dependencies in ((1, NAMES[:1]), (2, NAMES[1:2]), (3, NAMES[2:3]), (4, NAMES[1:4])):
        for dependency in dependencies:
            need(old_commands[index]["argv"].count(dependency + "=" + refined[dependency]["path"]) == 1,
                 "RETAINED_REFINED_LIBRARY_EDGE")
    need(type(old_selection["runtime_pins"]) is dict and len(old_selection["runtime_pins"]) == 1071
         and chosen["runtime_pins"] == old_selection["runtime_pins"], "EXACT_UNCHANGED_1071_RUNTIME_MAP")
    command = list(old_commands[-1]["argv"])
    need(command[0] == str(RUST / "bin/rustc.exe") and command[0] in chosen["runtime_pins"]
         and command.count("dependency=" + str(OLD / "lib")) == 1, "EXACT_COMPILER_AND_REFINED_SEARCH_PATH")
    for index, arg in enumerate(command):
        if arg == "--extern":
            library = command[index + 1].split("=", 1)[1]
            need(library in chosen["runtime_pins"] or library in {row["path"] for row in refined.values()},
                 "PINNED_DIRECT_LIBRARY")
        if arg.startswith("linker="):
            need(arg.split("=", 1)[1] in chosen["runtime_pins"], "PINNED_LINKER")

    h = load("geometry_snapshot_support", SUPPORT, SUPPORT_SHA)
    old = h.load("geometry_snapshot_prior_build", h.PREDECESSOR, h.PREDECESSOR_SHA)
    q = h.load("geometry_snapshot_prior", old.PRIOR, old.PRIOR_SHA)
    a = h.load("geometry_snapshot_artifacts", q.CRYPTO / "artifacts.py", q.HELPERS["artifacts.py"])
    p = h.load("geometry_snapshot_provision", q.CRYPTO / "provision_build.py", q.HELPERS["provision_build.py"])
    c = h.load("geometry_snapshot_census", q.CRYPTO / "continue_build03.py", q.HELPERS["continue_build03.py"])
    r = h.load("geometry_snapshot_phase", ROOT / "experiments/scale-equation-01/runtime.py", q.RUNTIME_SHA)
    p.a, c.a, c.p, c.HERE = a, a, p, HERE
    r.LOG_LIMIT = LIMITS["command_log_bytes"]
    need(Path(sys.executable).resolve() == p.PYTHON and sha(p.PYTHON) == p.PYTHON_SHA
         and sha(p.PYTHON.parent / "python314.dll") == p.PYTHON_DLL_SHA, "PINNED_BUILD_PYTHON")
    need(sha(p.HELPERS / "run_stage.py") == p.HELPER_SHA
         and sha(p.HELPERS / "domains.py") == p.DOMAINS_SHA, "PINNED_JOB_HELPERS")
    sys.path.insert(0, str(p.HELPERS))
    import run_stage
    import domains
    need(Path(run_stage.__file__).resolve() == p.HELPERS / "run_stage.py"
         and Path(domains.__file__).resolve() == p.HELPERS / "domains.py", "JOB_ORIGIN")
    c.h = run_stage
    run = HERE / chosen["name"]
    attempt = HERE / (chosen["name"] + "-attempt.json")
    need(not run.exists() and not attempt.exists(), "FRESH_SNAPSHOT_HOST_BUILD")
    helper_pins = {
        SUPPORT: SUPPORT_SHA, h.PREDECESSOR: h.PREDECESSOR_SHA, old.PRIOR: old.PRIOR_SHA,
        ROOT / "experiments/scale-equation-01/runtime.py": q.RUNTIME_SHA,
        p.PYTHON: p.PYTHON_SHA, p.PYTHON.parent / "python314.dll": p.PYTHON_DLL_SHA,
        p.HELPERS / "run_stage.py": p.HELPER_SHA,
        p.HELPERS / "domains.py": p.DOMAINS_SHA, r.VCTIP: r.VCTIP_SHA,
    }
    helper_pins.update({q.CRYPTO / name: digest for name, digest in q.HELPERS.items()})
    host_binaries = old_environment["host_binaries"]
    need(len(host_binaries) == 3 and [Path(item["path"]).name for item in host_binaries]
         == ["cl.exe", "link.exe", "rc.exe"], "EXACT_ENVIRONMENT_OBSERVATION_TOOLS")
    for item in host_binaries:
        helper_pins[Path(item["path"])] = item["sha256"]

    def check_inputs(*, include_runtime=True):
        for path, digest in {**RECORDS, **helper_pins, selection: sys.argv[2]}.items():
            envelope()
            need(path.is_file() and path.resolve(strict=True) == path and sha(path) == digest,
                 "RECORD_OR_HELPER_CHANGED:" + str(path))
        need(not (OLD / "FINALIZATION-FAILED.json").exists()
             and read(OLD_ATTEMPT) == {"status": OLD_PASS, "result_sha256": RECORDS[OLD / "RESULT.json"]},
             "ADOPTED_PRIOR_FINALIZATION")
        for relative, expected in chosen["sources"].items():
            envelope()
            check_pin(ROOT / relative, expected)
            need(expected["bytes"] <= 1024**2, "SOURCE_BYTES")
        for item in refined.values():
            envelope()
            check_pin(Path(item["path"]), {key: item[key] for key in ("bytes", "sha256")})
        if include_runtime:
            runtime_bytes = 0
            for name, digest in chosen["runtime_pins"].items():
                envelope()
                path = Path(name)
                need(path.is_absolute() and path.resolve(strict=True) == path and path.is_file()
                     and sha(path) == digest, "RUNTIME_PIN:" + name)
                runtime_bytes += path.stat().st_size
            need(runtime_bytes == 2320491997, "EXACT_RETAINED_RUNTIME_BYTES")
        envelope()

    check_inputs()
    run.mkdir()
    phase = None
    result = {"schema": SCHEMA + "_RESULT_V1", "status": "FAIL",
              "selection_sha256": sys.argv[2], "limits": LIMITS,
              "retained_result_sha256": RECORDS[OLD / "RESULT.json"],
              "retained_commands_sha256": RECORDS[OLD / "compile-commands.json"],
              "retained_environment_sha256": RECORDS[OLD / "environment-profile.json"],
              "retained_selection_sha256": RECORDS[OLD_SELECTION],
              "runtime_pin_count": 1071, "runtime_pin_bytes": 2320491997,
              "refined_libraries": refined, **{key: 0 for key in COUNTS},
              "authority": "SNAPSHOT_HOST_ONE_LINK_ONLY_NOT_MATHEMATICAL_ADMISSION",
              "source_map_sha256": None, "commands_sha256": None,
              "environment_sha256": None, "input_map_sha256": None, "executable": None}

    class Budget:
        def __init__(self):
            self.peak = {"working_bytes": 0, "entries": 0}
            self.current = {}

        def refresh(self):
            envelope()
            self.current = c.census(run)
            envelope()
            need(self.current["working_bytes"] <= LIMITS["fresh_output_bytes"]
                 and self.current["entries"] <= LIMITS["fresh_output_entries"], "BUILD_OUTPUT_ENVELOPE")
            for key in self.peak:
                self.peak[key] = max(self.peak[key], self.current[key])

    budget = Budget()

    def verify_snapshot():
        need(c.file_map(run / "source") == chosen["sources"], "EXACT_SOURCE_SNAPSHOT")
        if result["executable"] is not None:
            item = result["executable"]
            check_pin(Path(item["path"]), {key: item[key] for key in ("bytes", "sha256")})

    try:
        (run / "commands").mkdir()
        raw_selection = selection.read_bytes()
        need(hashlib.sha256(raw_selection).hexdigest() == sys.argv[2], "SELECTION_COPY_CHANGED")
        with (run / "selection.json").open("xb") as stream:
            stream.write(raw_selection)
        snapshot = run / "source"
        for relative, expected in chosen["sources"].items():
            envelope()
            raw = (ROOT / relative).read_bytes()
            need(len(raw) == expected["bytes"] and hashlib.sha256(raw).hexdigest() == expected["sha256"],
                 "SOURCE_COPY_REBIND")
            target = snapshot / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream:
                stream.write(raw)
            check_pin(target, expected)
        save(run / "source-map.json", chosen["sources"])

        def replace(before, after):
            need(command.count(str(before)) == 1, "EXACT_RECIPE_SUBSTITUTION:" + str(before))
            command[command.index(str(before))] = str(after)

        replace("small_aggregate_stage_host", "geometry17_aggregate_host")
        replace("metadata=dmkn_auxwords_a53940b67580e215_small_aggregate_stage_host",
                "metadata=dmkn_geometry17_aggregate_host")
        replace(OLD / "source/stage/software/v5/aggregate_small/stage_host.rs",
                snapshot / "software/v5/aggregate_geometry/aggregate_host.rs")
        replace(OLD / "small_aggregate_stage_host.exe", run / "geometry17_aggregate_host.exe")
        need("lto=fat" in command and "--test" not in command and command.count("--extern") == 7,
             "RETAINED_HOST_RECIPE_ONLY_FOUR_SUBSTITUTIONS")
        save(run / "compile-command.json", command)
        save(run / "INPUT-MAP.json", {"sources": chosen["sources"], "runtime_pins": chosen["runtime_pins"],
             "refined_libraries": refined, "records": {str(path): digest for path, digest in RECORDS.items()},
             "helper_pins": {str(path): digest for path, digest in helper_pins.items()},
             "trust_boundary": "Pinned retained refined libraries and trusted tools plus Windows system DLLs; not hermetic/sandboxed"})
        env, environment = p.environment(run, RUST)
        need(environment["host_binaries"] == host_binaries, "UNCHANGED_ENVIRONMENT_TOOLS")
        env = {key: value for key, value in env.items() if key != "OUT_DIR"
               and not key.startswith("CARGO_PKG_") and key not in ("CARGO_MANIFEST_DIR", "CARGO_MANIFEST_PATH")}
        env.update(VCToolsUserTelemetryOptOut="1", CARGO_NET_OFFLINE="true")
        expected_env = {key: value.replace(str(OLD), str(run))
                        for key, value in old_environment["step_environments"][NAMES[-1]].items()}
        need(env == expected_env, "EXACT_RETAINED_LAST_COMMAND_ENVIRONMENT")
        environment.update(explicit_environment=env, environment_keys_only=sorted(env), no_inherited_environment=True)
        save(run / "environment-profile.json", environment)
        for field, filename in (("source_map_sha256", "source-map.json"), ("commands_sha256", "compile-command.json"),
                                ("input_map_sha256", "INPUT-MAP.json"), ("environment_sha256", "environment-profile.json")):
            result[field] = sha(run / filename)
        verify_snapshot()
        # Immutable runtime is checked at start and finalization, not a redundant
        # third2.32GB scan immediately before the only compiler call.
        check_inputs(include_runtime=False)

        class InclusiveJob(run_stage.Job):
            def stats(self):
                measured = super().stats()
                if not finalizing:
                    need(measured["cpu_seconds"] <= LIMITS["worker_cpu_seconds"], "INCLUSIVE_WORKER_CPU")
                return measured

        def exact_job(seconds, memory, active_processes):
            need((seconds, memory, active_processes) == (300, 4096, 8), "RETAINED_PHASE_CONSTRUCTOR")
            return InclusiveJob(240, 1536, active_processes=6)

        budget.refresh()
        phase = r.phase_class(p, a)("geometry17-aggregate-snapshot-host-link", run, budget, env, exact_job, 300)
        phase.invoke("geometry17-aggregate-snapshot-host", command, ROOT, allow_build_telemetry=True)
        result.update(status=PASS, executable=pin(run / "geometry17_aggregate_host.exe"), snapshot_host_links=1)
    except BaseException as error:
        result["error"] = type(error).__name__ + ": " + str(error)[:4000]
    finally:
        finalizing = True
        if phase is not None:
            try:
                phase.close()
                need(phase.final_stats["active_processes"] == phase.final_stats["terminated_processes"] == 0
                     and phase.final_stats["cpu_seconds"] <= LIMITS["worker_cpu_seconds"], "FINAL_WORKER_CLOSURE")
            except BaseException as error:
                result.update(status="FAIL_CLEANUP", cleanup_error=str(error)[:2000])
        result["job"] = getattr(phase, "final_stats", None)
        result["commands"] = phase.commands if phase is not None else []
        try:
            check_inputs()
            need(sha(run / "selection.json") == sys.argv[2], "FINAL_SELECTION_COPY")
            verify_snapshot()
            for field, filename in (("source_map_sha256", "source-map.json"), ("commands_sha256", "compile-command.json"),
                                    ("input_map_sha256", "INPUT-MAP.json"), ("environment_sha256", "environment-profile.json")):
                need(sha(run / filename) == result[field], "FINAL_RECORD_PIN:" + filename)
            if result["status"] == PASS:
                need(len(result["commands"]) == 1 and result["commands"][0]["argv"] == command
                     and result["commands"][0]["status"] == "COMMAND_COMPLETED"
                     and result["commands"][0]["exit_code"] == 0
                     and result["commands"][0]["cleanup_errors"] == []
                     and all(result[key] == value for key, value in COUNTS.items()), "ONE_CLEAN_LINK_ONLY")
            budget.refresh()
        except BaseException as error:
            result.update(status="FAIL_FINAL_CHECK", final_error=str(error)[:3000])
        result.update(controller_cpu_seconds=time.process_time() - cpu, wall_seconds=time.monotonic() - started,
                      output_census=budget.current, sampled_peaks=budget.peak,
                      accounting="CONTROLLER_DISJOINT_FROM_INCLUSIVE_WORKER_JOB;FINAL_REPORT_EXIT_TAIL_EXCLUDED")
        save(run / "RESULT.json", result)
        save(attempt, {"status": result["status"], "result_sha256": sha(run / "RESULT.json")})
        try:
            budget.refresh()
        except BaseException as error:
            result["status"] = "FAIL_FINALIZATION"
            save(run / "FINALIZATION-FAILED.json", {"status": "FAIL_FINALIZATION", "overrides_result_and_attempt": True,
                 "result_sha256": sha(run / "RESULT.json"), "error": str(error)[:3000]})
    print(json.dumps({key: result.get(key) for key in ("status", "error", "wall_seconds")}))
    return 0 if result["status"] == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
