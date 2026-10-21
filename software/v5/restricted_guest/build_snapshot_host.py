"""One retained snapshot-host link against the exact RC native libraries.

The unchanged host keeps native preflight and real boundary receipt verification.
No host execution, guest execution, proof, SDK rebuild or stage-host link occurs.
Run only after root selects the exact finite compile-only input.
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
SOURCE = ROOT / "software/v5/restricted_guest"
OLD = HERE / "small-aggregate-snapshot-host-build-01"
NATIVE = HERE / "restricted-composition-build-02"
RUST = ROOT / "experiments/scale-crypto-01/runs/run-01/rust"
SUPPORT = ROOT / "software/v5/modules/native/proof_validation/control.py"
SUPPORT_SHA = "91e25c3a3244a106c01ce18da63b07a163b0d07e53eddcf5376b399ee22a9ca1"
PASS = "PASS_RC_SNAPSHOT_HOST_ONE_LINK_ONLY"
SCHEMA = "DMKN_V5_RC_SNAPSHOT_HOST_BUILD_V1"
RECORDS = {
    OLD / "RESULT.json": "7ad07e35602092833d9f40e7f0775f0b4eceb451e52853875bd5baeaf63f78b1",
    OLD / "compile-command.json": "d47042dd268c8235ed10b33bdb1f0154aa082f05125b63911de56a2504b172d6",
    OLD / "environment-profile.json": "c21f2e7e8bdafe77cedae218a35bbcdd5e2b0c3d3505b04837392851204964f6",
    OLD / "INPUT-MAP.json": "91f26a1052f22410925bf6d94328295d266c09236ce948c24cddd2aa546c809f",
    HERE / (OLD.name + "-selection.json"): "e4493418256735529f7fc19ed606ea459bf35b613b57680d2e0a31a7b858e4bd",
    HERE / (OLD.name + "-attempt.json"): "ad8c83612eb399062e1656c92487d32a3833e004e33e4250dce1ea24c4ce3fea",
    NATIVE / "RESULT.json": "24e8ebf8f774e22ec19c7172dca0a56efb81ad653e609445ae0e5d030e2233dd",
    NATIVE / "source-map.json": "32e95e4b67377ac2f8b6cf1b7087a006c675c15db98f954415ab996f7393ac04",
    NATIVE / "compile-commands.json": "50460299a3ccabae56d4ec83173c31c360d19003951d972fbc052b079825359a",
    HERE / (NATIVE.name + "-selection.json"): "659c780e902b69cfb039b854abae05d6a570c389f463dc8bfc6fff9bfa455244",
    HERE / (NATIVE.name + "-attempt.json"): "cd176fb134beaa59ad5d4289083be72ba92fdb956ef8dc231196d4fab1ccfdc9",
}
LIBRARIES = {
    "libdmkn_rc_relation.rlib": {"bytes": 1719004,
        "sha256": "1bdfd6a0943b6a09248ae99aefd793b63384a957bf8d98c0cd8d8b430fd04a0b"},
    "libdmkn_aggregate_relation.rlib": {"bytes": 1050594,
        "sha256": "be8bdcb4c815e5c610145e5fea28a6d6601fe8dd9ae8cd04f3bf35c5b9dbcbba"},
}
RUST_SOURCES = {
    "software/v5/aggregate_small/aggregate_host.rs": {"bytes": 20755,
        "sha256": "6644d9a03f25a59089fd735b0e2f2229ec8940dedbe2502568dfd8c6a36d9c25"},
    "software/v5/aggregate/receipt.rs": {"bytes": 3631,
        "sha256": "41db7677d40af4fd779159e8442724bff7842b7f4e5745411e5846d8e7678254"},
}
SOURCE_SET = set(RUST_SOURCES) | {"software/v5/restricted_guest/build_snapshot_host.py"}
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


def expected_runtime(prior_map):
    """Exact prior finite map, with old aggregate removed and two RC libs added."""
    selected = dict(prior_map["runtime_pins"])
    need(len(selected) == 1071, "PRIOR_1071_RUNTIME_MAP")
    previous = HERE / "proof-validation-integration-build-01/libdmkn_aggregate_relation.rlib"
    need(str(previous) in selected, "OLD_AGGREGATE_LIBRARY_PRESENT")
    del selected[str(previous)]
    for name, pin in LIBRARIES.items():
        need(str(NATIVE / name) not in selected, "NEW_RC_LIBRARY_EDGE")
        selected[str(NATIVE / name)] = pin["sha256"]
    need(len(selected) == 1072, "EXACT_RC_RUNTIME_COUNT")
    return selected


def main():
    started, cpu = time.monotonic(), time.process_time()
    finalizing = False

    def envelope():
        cap = LIMITS["controller_cpu_seconds"] if finalizing else LIMITS["ordinary_controller_cpu_seconds"]
        need(time.monotonic() - started <= LIMITS["total_wall_seconds"]
             and time.process_time() - cpu <= cap, "ONE_TOTAL_CLOCK_AND_CONTROLLER_RESERVE")

    need(os.name == "nt" and Path.cwd() == ROOT and Path(__file__).resolve() == SOURCE / "build_snapshot_host.py"
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize and len(sys.argv) == 3, "EXACT_OWNER_INVOCATION")
    selection = Path(sys.argv[1]).resolve(strict=True)
    need(selection.parent == HERE and selection.stat().st_size <= 2 * 1024**2
         and sha(selection) == sys.argv[2], "EXACT_SELECTION")
    chosen = read(selection)
    need(set(chosen) == {"schema", "name", "authorizes_compile_only", "sources", "runtime_pins", "limits"}
         and chosen["schema"] == SCHEMA and chosen["name"] == "restricted-snapshot-host-build-01"
         and chosen["authorizes_compile_only"] is True and chosen["limits"] == LIMITS, "SELECTION_FIELDS")
    need(type(chosen["sources"]) is dict and set(chosen["sources"]) == SOURCE_SET
         and all(chosen["sources"][name] == pin for name, pin in RUST_SOURCES.items()), "THREE_SOURCE_CLOSURE")
    for path, digest in RECORDS.items():
        envelope()
        need(sha(path) == digest, "RETAINED_BUILD_RECORD:" + str(path))
    prior, native = read(OLD / "RESULT.json"), read(NATIVE / "RESULT.json")
    prior_map = read(OLD / "INPUT-MAP.json")
    prior_selection = read(HERE / (OLD.name + "-selection.json"))
    command = read(OLD / "compile-command.json")
    need(prior["status"] == "PASS_SMALL_AGGREGATE_SNAPSHOT_HOST_ONE_LINK_ONLY"
         and prior["commands"][0]["argv"] == command and len(prior["commands"]) == 1
         and prior_selection["runtime_pins"] == prior_map["runtime_pins"], "ACTUAL_RETAINED_HOST_RECIPE")
    need(native["status"] == "PASS_RC_THREE_COMPILES_ONLY" and len(native["commands"]) == 3
         and all(row["status"] == "COMMAND_COMPLETED" and row["exit_code"] == 0
                 and row["cleanup_errors"] == [] for row in native["commands"])
         and read(NATIVE / "source-map.json") == read(HERE / (NATIVE.name + "-selection.json"))["sources"],
         "ACTUAL_RC_NATIVE_BUILD")
    for name, pin in LIBRARIES.items():
        need(native["outputs"][name] == {"path": str(NATIVE / name), **pin}, "RC_LIBRARY_BUILD_BINDING")
    need(chosen["runtime_pins"] == expected_runtime(prior_map), "EXACT_SELECTED_1072_RUNTIME")

    h = load("rc_host_support", SUPPORT, SUPPORT_SHA)
    old = h.load("rc_host_prior_build", h.PREDECESSOR, h.PREDECESSOR_SHA)
    q = h.load("rc_host_prior", old.PRIOR, old.PRIOR_SHA)
    a = h.load("rc_host_artifacts", q.CRYPTO / "artifacts.py", q.HELPERS["artifacts.py"])
    p = h.load("rc_host_provision", q.CRYPTO / "provision_build.py", q.HELPERS["provision_build.py"])
    c = h.load("rc_host_census", q.CRYPTO / "continue_build03.py", q.HELPERS["continue_build03.py"])
    r = h.load("rc_host_phase", ROOT / "experiments/scale-equation-01/runtime.py", q.RUNTIME_SHA)
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
    helper_pins = {Path(path): digest for path, digest in prior_map["helper_pins"].items()}
    need(helper_pins[SUPPORT] == SUPPORT_SHA and helper_pins[h.PREDECESSOR] == h.PREDECESSOR_SHA
         and helper_pins[old.PRIOR] == old.PRIOR_SHA, "UNCHANGED_HELPER_GRAPH")
    host_binaries = read(OLD / "environment-profile.json")["host_binaries"]
    run, attempt = HERE / chosen["name"], HERE / (chosen["name"] + "-attempt.json")
    need(not run.exists() and not attempt.exists(), "FRESH_RC_HOST_BUILD")

    def check_inputs(*, include_runtime=True):
        for path, digest in {**RECORDS, **helper_pins, selection: sys.argv[2]}.items():
            envelope()
            need(path.is_file() and path.resolve(strict=True) == path and sha(path) == digest,
                 "RECORD_OR_HELPER_CHANGED:" + str(path))
        for root, result in ((OLD, prior), (NATIVE, native)):
            need(not (root / "FINALIZATION-FAILED.json").exists()
                 and result["selection_sha256"] == RECORDS[HERE / (root.name + "-selection.json")]
                 and result["job"]["active_processes"] == result["job"]["terminated_processes"] == 0
                 and read(HERE / (root.name + "-attempt.json")) == {
                     "status": result["status"], "result_sha256": RECORDS[root / "RESULT.json"]},
                 "RETAINED_BUILD_FINALIZATION")
        for relative, pin in chosen["sources"].items():
            envelope()
            need(type(pin) is dict and set(pin) == {"bytes", "sha256"}
                 and type(pin["bytes"]) is int and 0 < pin["bytes"] <= 1024**2
                 and re.fullmatch(r"[0-9a-f]{64}", pin["sha256"]), "SOURCE_PIN_FIELDS")
            path = ROOT / relative
            need(path.is_file() and path.resolve(strict=True) == path
                 and path.stat().st_size == pin["bytes"] and sha(path) == pin["sha256"], "SOURCE_PIN:" + relative)
        if include_runtime:
            total = 0
            for name, digest in chosen["runtime_pins"].items():
                envelope()
                path = Path(name)
                need(path.is_absolute() and path.is_file() and path.resolve(strict=True) == path
                     and sha(path) == digest, "RUNTIME_PIN:" + name)
                total += path.stat().st_size
            need(total == 2322344899, "EXACT_RETAINED_RUNTIME_BYTES")
        envelope()

    check_inputs()
    run.mkdir()
    phase = None
    result = {"schema": "DMKN_V5_RC_SNAPSHOT_HOST_BUILD_RESULT_V1", "status": "FAIL",
        "selection_sha256": sys.argv[2], "limits": LIMITS, "runtime_pin_count": 1072,
        "runtime_pin_bytes": 2322344899, "retained_host_result_sha256": RECORDS[OLD / "RESULT.json"],
        "rc_native_result_sha256": RECORDS[NATIVE / "RESULT.json"],
        "backend_rebuilds": 0, "relation_rebuilds": 0, "checker_rebuilds": 0,
        "host_calls": 0, "guest_calls": 0, "proof_calls": 0, "network_calls": 0,
        "authority": "HOST_COMPILE_ONLY_NOT_ADMISSION"}

    class Budget:
        def __init__(self):
            self.peak, self.current = {"working_bytes": 0, "entries": 0}, {}

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
        raw = selection.read_bytes()
        need(hashlib.sha256(raw).hexdigest() == sys.argv[2], "SELECTION_COPY_CHANGED")
        with (run / "selection.json").open("xb") as stream:
            stream.write(raw)
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

        replace("small_aggregate_host", "restricted_snapshot_host")
        replace(OLD / "source/software/v5/aggregate_small/aggregate_host.rs",
                snapshot / "software/v5/aggregate_small/aggregate_host.rs")
        replace(OLD / "small_aggregate_host.exe", run / "restricted_snapshot_host.exe")
        replace("dmkn_aggregate_relation=" + str(HERE / "proof-validation-integration-build-01/libdmkn_aggregate_relation.rlib"),
                "dmkn_aggregate_relation=" + str(NATIVE / "libdmkn_aggregate_relation.rlib"))
        command += ["-L", "dependency=" + str(NATIVE), "--extern",
                    "dmkn_rc_relation=" + str(NATIVE / "libdmkn_rc_relation.rlib"),
                    "-C", "metadata=dmkn_rc_snapshot01"]
        need("lto=fat" in command and "--test" not in command and command.count("--extern") == 8,
             "EXACT_RC_HOST_RECIPE")
        for index, argument in enumerate(command):
            if argument == "--extern":
                need(command[index + 1].split("=", 1)[1] in chosen["runtime_pins"], "PINNED_DIRECT_LIBRARY")
        h.save(run / "compile-command.json", command)
        h.save(run / "INPUT-MAP.json", {"sources": chosen["sources"], "runtime_pins": chosen["runtime_pins"],
            "records": {str(path): digest for path, digest in RECORDS.items()},
            "helper_pins": {str(path): digest for path, digest in helper_pins.items()},
            "trust_boundary": "Retained trusted libraries/tools plus Windows system DLLs; not hermetic/sandboxed"})
        env, environment = p.environment(run, RUST)
        need(environment["host_binaries"] == host_binaries, "UNCHANGED_ENVIRONMENT_TOOL_OBSERVATIONS")
        env["VCToolsUserTelemetryOptOut"] = "1"
        environment["environment_keys_only"], environment["explicit_environment"] = sorted(env), env
        h.save(run / "environment-profile.json", environment)
        check_inputs(include_runtime=False)

        class InclusiveJob(run_stage.Job):
            def stats(self):
                measured = super().stats()
                if not finalizing:
                    need(measured["cpu_seconds"] <= LIMITS["worker_cpu_seconds"], "INCLUSIVE_WORKER_CPU_LIMIT")
                return measured

        def exact_job(seconds, memory, active_processes):
            need((seconds, memory, active_processes) == (300, 4096, 8), "RETAINED_PHASE_SHAPE")
            return InclusiveJob(240, 3072, active_processes=6)

        budget.refresh()
        phase = r.phase_class(p, a)("restricted-snapshot-host-link", run, budget, env, exact_job, 300)
        phase.invoke("restricted-snapshot-host", command, ROOT, allow_build_telemetry=True)
        result.update(status=PASS, executable=a.pin(run / "restricted_snapshot_host.exe"))
    except BaseException as error:
        result["error"] = type(error).__name__ + ": " + str(error)[:4000]
    finally:
        finalizing = True
        if phase is not None:
            try:
                phase.close()
                need(phase.final_stats["active_processes"] == phase.final_stats["terminated_processes"] == 0
                     and phase.final_stats["cpu_seconds"] <= LIMITS["worker_cpu_seconds"], "FINAL_OWNED_QUIESCENCE")
            except BaseException as error:
                result.update(status="FAIL_CLEANUP", cleanup_error=str(error)[:2000])
            result["job"], result["commands"] = getattr(phase, "final_stats", None), phase.commands
        try:
            check_inputs()
            need(sha(run / "selection.json") == sys.argv[2]
                 and c.file_map(run / "source") == chosen["sources"], "FINAL_SELECTED_SNAPSHOT")
            budget.refresh()
        except BaseException as error:
            result.update(status="FAIL_FINAL_CHECK", final_error=str(error)[:3000])
        result.update(controller_cpu_seconds=time.process_time() - cpu, wall_seconds=time.monotonic() - started,
            output_census=budget.current, sampled_peaks=budget.peak,
            accounting="CONTROLLER_DISJOINT_FROM_INCLUSIVE_WORKER_JOB;FINAL_REPORT_EXIT_TAIL_EXCLUDED")
        h.save(run / "RESULT.json", result)
        h.save(attempt, {"status": result["status"], "result_sha256": sha(run / "RESULT.json")})
        try:
            budget.refresh()
        except BaseException as error:
            result.update(status="FAIL_FINALIZATION", finalization_error=str(error)[:3000])
            h.save(run / "FINALIZATION-FAILED.json", {"status": "FAIL_FINALIZATION", "overrides_result_and_attempt": True,
                "result_sha256": sha(run / "RESULT.json"), "error": str(error)[:3000]})
    print(json.dumps({key: result.get(key) for key in ("status", "error", "wall_seconds")}))
    return 0 if result["status"] == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
