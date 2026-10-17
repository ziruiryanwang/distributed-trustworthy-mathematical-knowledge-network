"""One exact small-segment stage-host link; unchanged retained SDK and native libraries.

Only crate name, source path and output path change from the successful snapshot
host command. No Cargo/backend/checker/relation rebuild or host/guest/proof call.
This is owner-controlled trusted building, not a hostile-code sandbox.
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
SOURCE = ROOT / "software/v5/aggregate_small"
SUPPORT = ROOT / "software/v5/modules/native/proof_validation/control.py"
SUPPORT_SHA = "91e25c3a3244a106c01ce18da63b07a163b0d07e53eddcf5376b399ee22a9ca1"
OLD = HERE / "aggregate-host-build-01"
OLD_SELECTION = HERE / "aggregate-host-build-01-selection.json"
OLD_ATTEMPT = HERE / "aggregate-host-build-01-attempt.json"
RUST = ROOT / "experiments/scale-crypto-01/runs/run-01/rust"
PASS = "PASS_SMALL_AGGREGATE_STAGE_HOST_ONE_LINK_ONLY"
RECORDS = {
    OLD / "RESULT.json": "4cdb12b5e3aeaebcfef5e0370bd445f24ff6779b196ca69cbab60f9d57002a75",
    OLD / "compile-command.json": "acc215837499107a01bfe60544dceeb40ff19ad4d67f93252867bbf30f3de96b",
    OLD / "environment-profile.json": "34525808d26848e9582ad5ada38ff66fae2205f79ae0421a33f72fbd67af4e18",
    OLD_SELECTION: "b8c64994f64c66eaa8a90612d5fa0f3ebcad4ce053e86f4f8fe485408cadbb8b",
    OLD_ATTEMPT: "cdc489e3d1dcd73bcb4ab782fd10138ccaaf452725976c2f38ac644348590ee2",
}
SOURCE_SET = {"software/v5/aggregate_small/build_stage.py",
              "software/v5/aggregate_small/stage_host.rs", "software/v5/aggregate/receipt.rs"}
RUST_SOURCES = {
    "software/v5/aggregate/receipt.rs": {
        "bytes": 3631, "sha256": "41db7677d40af4fd779159e8442724bff7842b7f4e5745411e5846d8e7678254"},
}
LIMITS = {"worker_cpu_seconds": 240, "worker_wall_seconds": 300, "memory_mib": 3072,
          "active_processes": 6, "ordinary_controller_cpu_seconds": 40,
          "controller_cpu_seconds": 60, "total_wall_seconds": 420,
          "fresh_output_bytes": 512 * 1024**2, "fresh_output_entries": 8192,
          "command_log_bytes": 1024**2}


def need(value, reason):
    if not value:
        raise ValueError(reason)


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


def runtime_subset(prior_selection, command):
    """Filter only pinned map keys: no retained-tree discovery or library edits."""
    need(type(prior_selection["runtime_pins"]) is dict
         and len(prior_selection["runtime_pins"]) == 3142, "EXACT_PRIOR_RUNTIME_MAP")
    directories = {Path(command[i + 1].split("=", 1)[1])
                   for i, item in enumerate(command) if item == "-L"}
    need(len(directories) == 14 and command.count("--extern") == 7, "EXACT_RETAINED_LINK_INPUTS")
    suffixes = {".rlib", ".rmeta", ".dll", ".lib", ".a"}
    selected = {}
    for name, digest in prior_selection["runtime_pins"].items():
        path = Path(name)
        keep = (path.drive.lower() == "c:"
                or (path.parent in directories and path.suffix in suffixes)
                or path == RUST / "bin/rustc.exe"
                or (path.parent == RUST / "bin" and path.suffix == ".dll")
                or (path.parent == RUST / "lib/rustlib/x86_64-pc-windows-msvc/lib"
                    and path.suffix in suffixes))
        if keep:
            need(type(digest) is str and re.fullmatch(r"[0-9a-f]{64}", digest), "RUNTIME_DIGEST")
            selected[name] = digest
    need(len(selected) == 1071
         and sum(Path(name).drive.lower() == "c:" for name in selected) == 98
         and sum(Path(name).is_relative_to(RUST) for name in selected) == 25,
         "EXACT_FILTERED_RUNTIME_SET")
    for index, argument in enumerate(command):
        if argument == "--extern":
            need(command[index + 1].split("=", 1)[1] in selected, "UNPINNED_DIRECT_LIBRARY")
        if argument.startswith("linker="):
            need(argument.split("=", 1)[1] in selected, "UNPINNED_LINKER")
    need(command[0] == str(RUST / "bin/rustc.exe") and command[0] in selected, "UNPINNED_COMPILER")
    return selected


def main():
    started, cpu = time.monotonic(), time.process_time()
    finalizing = False

    def envelope():
        cap = LIMITS["controller_cpu_seconds"] if finalizing else LIMITS["ordinary_controller_cpu_seconds"]
        need(time.monotonic() - started <= LIMITS["total_wall_seconds"]
             and time.process_time() - cpu <= cap, "ONE_TOTAL_CLOCK_AND_CONTROLLER_RESERVE")

    need(os.name == "nt" and Path.cwd() == ROOT
         and Path(__file__).resolve() == SOURCE / "build_stage.py"
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize and len(sys.argv) == 3, "EXACT_OWNER_INVOCATION")
    selection = Path(sys.argv[1]).resolve(strict=True)
    need(selection.parent == HERE and selection.stat().st_size <= 2 * 1024**2
         and sha(selection) == sys.argv[2], "EXACT_SELECTION")
    chosen = read(selection)
    need(set(chosen) == {"schema", "name", "authorizes_compile_only", "sources",
                         "runtime_pins", "limits"}
         and chosen["schema"] == "DMKN_V5_SMALL_AGGREGATE_STAGE_HOST_BUILD_V1"
         and chosen["authorizes_compile_only"] is True
         and type(chosen["name"]) is str
         and re.fullmatch(r"small-aggregate-stage-host-build-[0-9]{2}", chosen["name"])
         and chosen["limits"] == LIMITS, "SELECTION_FIELDS")
    need(type(chosen["sources"]) is dict and set(chosen["sources"]) == SOURCE_SET
         and all(chosen["sources"][name] == pin for name, pin in RUST_SOURCES.items()),
         "THREE_SOURCE_CLOSURE_WITH_UNCHANGED_RECEIPT")
    for path, digest in RECORDS.items():
        envelope()
        need(sha(path) == digest, "RETAINED_RECIPE_RECORD:" + str(path))
    prior, old_selection = read(OLD / "RESULT.json"), read(OLD_SELECTION)
    command = read(OLD / "compile-command.json")
    need(prior["status"] == "PASS_AGGREGATE_HOST_ONE_LINK_ONLY"
         and prior["selection_sha256"] == RECORDS[OLD_SELECTION]
         and prior["job"]["active_processes"] == prior["job"]["terminated_processes"] == 0
         and len(prior["commands"]) == 1 and prior["commands"][0]["argv"] == command,
         "EXACT_SUCCESSFUL_UNCHANGED_HOST_RECIPE")
    expected_runtime = runtime_subset(old_selection, command)
    need(chosen["runtime_pins"] == expected_runtime, "EXACT_1071_RUNTIME_PINS_NO_LIBRARY_REPLACEMENT")

    h = load("aggregate_stage_support", SUPPORT, SUPPORT_SHA)
    old = h.load("aggregate_stage_prior_build", h.PREDECESSOR, h.PREDECESSOR_SHA)
    q = h.load("aggregate_stage_prior", old.PRIOR, old.PRIOR_SHA)
    a = h.load("aggregate_stage_artifacts", q.CRYPTO / "artifacts.py", q.HELPERS["artifacts.py"])
    p = h.load("aggregate_stage_provision", q.CRYPTO / "provision_build.py", q.HELPERS["provision_build.py"])
    c = h.load("aggregate_stage_census", q.CRYPTO / "continue_build03.py", q.HELPERS["continue_build03.py"])
    r = h.load("aggregate_stage_phase", ROOT / "experiments/scale-equation-01/runtime.py", q.RUNTIME_SHA)
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
    need(not run.exists() and not attempt.exists(), "FRESH_STAGE_HOST_BUILD")
    helper_pins = {
        SUPPORT: SUPPORT_SHA, h.PREDECESSOR: h.PREDECESSOR_SHA, old.PRIOR: old.PRIOR_SHA,
        ROOT / "experiments/scale-equation-01/runtime.py": q.RUNTIME_SHA,
        p.PYTHON: p.PYTHON_SHA, p.PYTHON.parent / "python314.dll": p.PYTHON_DLL_SHA,
        p.HELPERS / "run_stage.py": p.HELPER_SHA,
        p.HELPERS / "domains.py": p.DOMAINS_SHA, r.VCTIP: r.VCTIP_SHA,
    }
    helper_pins.update({q.CRYPTO / name: digest for name, digest in q.HELPERS.items()})
    # The unchanged environment helper observes cl/rc as well as the linker.
    # Only link.exe is a compile subprocess here, but bind all three metadata
    # inputs to the retained environment record rather than silently adopting.
    host_binaries = read(OLD / "environment-profile.json")["host_binaries"]
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
             and read(OLD_ATTEMPT) == {"status": prior["status"],
                 "result_sha256": RECORDS[OLD / "RESULT.json"]}, "ADOPTED_PRIOR_FINALIZATION")
        for relative, pin in chosen["sources"].items():
            envelope()
            need(type(pin) is dict and set(pin) == {"bytes", "sha256"}
                 and type(pin["bytes"]) is int and 0 < pin["bytes"] <= 1024**2
                 and re.fullmatch(r"[0-9a-f]{64}", pin["sha256"]), "SOURCE_PIN_FIELDS")
            path = ROOT / relative
            need(path.resolve(strict=True) == path and path.is_file()
                 and path.stat().st_size == pin["bytes"] and sha(path) == pin["sha256"], "SOURCE_PIN:" + relative)
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
    result = {"schema": "DMKN_V5_SMALL_AGGREGATE_STAGE_HOST_BUILD_RESULT_V1", "status": "FAIL",
              "selection_sha256": sys.argv[2], "limits": LIMITS,
              "retained_command_sha256": RECORDS[OLD / "compile-command.json"],
              "retained_result_sha256": RECORDS[OLD / "RESULT.json"],
              "runtime_pin_count": 1071, "runtime_pin_bytes": 2320491997,
              "backend_rebuilds": 0, "relation_rebuilds": 0, "checker_rebuilds": 0,
              "host_calls": 0, "guest_calls": 0, "proof_calls": 0, "network_calls": 0,
              "authority": "HOST_COMPILE_ONLY_NOT_ADMISSION"}

    class Budget:
        def __init__(self):
            self.peak = {"working_bytes": 0, "entries": 0}
            self.current = {}

        def refresh(self):
            envelope()
            self.current = c.census(run)
            envelope()
            need(self.current["working_bytes"] <= LIMITS["fresh_output_bytes"]
                 and self.current["entries"] <= LIMITS["fresh_output_entries"], "HOST_BUILD_OUTPUT_ENVELOPE")
            for key in self.peak:
                self.peak[key] = max(self.peak[key], self.current[key])

    budget = Budget()
    try:
        (run / "commands").mkdir()
        raw_selection = selection.read_bytes()
        need(hashlib.sha256(raw_selection).hexdigest() == sys.argv[2], "SELECTION_COPY_CHANGED")
        with (run / "selection.json").open("xb") as stream:
            stream.write(raw_selection)
        snapshot = run / "source"
        for relative, pin in chosen["sources"].items():
            envelope()
            target = snapshot / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream:
                stream.write((ROOT / relative).read_bytes())
            need(target.stat().st_size == pin["bytes"] and sha(target) == pin["sha256"], "EXACT_SNAPSHOT")
        h.save(run / "source-map.json", chosen["sources"])

        def replace(before, after):
            need(command.count(str(before)) == 1, "EXACT_RECIPE_SUBSTITUTION:" + str(before))
            command[command.index(str(before))] = str(after)

        replace("aggregate_host", "small_aggregate_stage_host")
        replace(OLD / "source/software/v5/aggregate_host/aggregate_host.rs",
                snapshot / "software/v5/aggregate_small/stage_host.rs")
        replace(OLD / "aggregate_host.exe", run / "small_aggregate_stage_host.exe")
        need("lto=fat" in command and "--test" not in command and command.count("--extern") == 7,
             "RETAINED_EXACT_HOST_RECIPE")
        h.save(run / "compile-command.json", command)
        h.save(run / "INPUT-MAP.json", {"sources": chosen["sources"],
            "runtime_pins": chosen["runtime_pins"],
            "records": {str(path): digest for path, digest in RECORDS.items()},
            "helper_pins": {str(path): digest for path, digest in helper_pins.items()},
            "trust_boundary": "Retained trusted libraries/tools plus Windows system DLLs; not hermetic/sandboxed"})
        env, environment = p.environment(run, RUST)
        need(environment["host_binaries"] == host_binaries, "UNCHANGED_ENVIRONMENT_TOOL_OBSERVATIONS")
        env["VCToolsUserTelemetryOptOut"] = "1"
        environment["environment_keys_only"] = sorted(env)
        environment["explicit_environment"] = env
        h.save(run / "environment-profile.json", environment)
        # The large immutable runtime map is hashed before preparation and in
        # finalization. Recheck only small records/sources here, not a third
        # duplicate read of the same 2.32 GB before this one compiler call.
        check_inputs(include_runtime=False)

        class InclusiveJob(run_stage.Job):
            def stats(self):
                measured = super().stats()
                if not finalizing:
                    need(measured["cpu_seconds"] <= LIMITS["worker_cpu_seconds"], "INCLUSIVE_WORKER_CPU_LIMIT")
                return measured

        def exact_job(seconds, memory, active_processes):
            need(seconds == 300 and memory == 4096 and active_processes == 8, "RETAINED_PHASE_SHAPE")
            return InclusiveJob(240, 3072, active_processes=6)

        budget.refresh()
        phase = r.phase_class(p, a)("small-aggregate-stage-host-link", run, budget, env, exact_job, 300)
        phase.invoke("small-aggregate-stage-host", command, ROOT, allow_build_telemetry=True)
        result.update(status=PASS, executable=a.pin(run / "small_aggregate_stage_host.exe"))
    except BaseException as error:
        result["error"] = type(error).__name__ + ": " + str(error)[:4000]
    finally:
        finalizing = True
        if phase is not None:
            try:
                phase.close()
                need(phase.final_stats["active_processes"] == 0
                     and phase.final_stats["terminated_processes"] == 0
                     and phase.final_stats["cpu_seconds"] <= LIMITS["worker_cpu_seconds"],
                     "FINAL_WORKER_QUIESCENCE_AND_INCLUSIVE_BUDGET")
            except BaseException as error:
                result.update(status="FAIL_CLEANUP", cleanup_error=str(error)[:2000])
            result["job"] = getattr(phase, "final_stats", None)
            result["commands"] = phase.commands
        try:
            check_inputs()
            need(sha(run / "selection.json") == sys.argv[2], "SAVED_SELECTION_PIN")
            need(c.file_map(run / "source") == chosen["sources"], "FINAL_SOURCE_SNAPSHOT")
            budget.refresh()
        except BaseException as error:
            result.update(status="FAIL_FINAL_CHECK", final_error=str(error)[:3000])
        result.update(controller_cpu_seconds=time.process_time() - cpu,
                      wall_seconds=time.monotonic() - started, output_census=budget.current,
                      sampled_peaks=budget.peak,
                      accounting="CONTROLLER_DISJOINT_FROM_INCLUSIVE_WORKER_JOB;FINAL_REPORT_EXIT_TAIL_EXCLUDED")
        h.save(run / "RESULT.json", result)
        h.save(attempt, {"status": result["status"], "result_sha256": sha(run / "RESULT.json")})
        try:
            budget.refresh()
        except BaseException as error:
            result.update(status="FAIL_FINALIZATION", finalization_error=str(error)[:3000])
            h.save(run / "FINALIZATION-FAILED.json", {"status": "FAIL_FINALIZATION",
                   "overrides_result_and_attempt": True, "result_sha256": sha(run / "RESULT.json"),
                   "error": str(error)[:3000]})
    print(json.dumps({key: result.get(key) for key in ("status", "error", "wall_seconds")}))
    return 0 if result["status"] == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())

