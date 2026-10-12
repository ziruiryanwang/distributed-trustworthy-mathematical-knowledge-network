"""One exact aggregate-host link against retained SDK and selected new rlibs.

No backend/Cargo/checker rebuild, host execution, guest, proof or networking.
Root supplies source/artifact/runtime pins and a separate finite selection.
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
SOURCE = ROOT / "software/v5/aggregate_host"
SUPPORT = ROOT / "software/v5/modules/native/proof_validation/control.py"
SUPPORT_SHA = "91e25c3a3244a106c01ce18da63b07a163b0d07e53eddcf5376b399ee22a9ca1"
OLD = HERE / "module-host-build-03"
OLD_RESULT_SHA = "6e01679707da8d58e286f7c756e698b1870aeab250d3bccda7a9099e1b8344e7"
SOURCE_SET = {"software/v5/aggregate_host/build.py",
              "software/v5/aggregate_host/aggregate_host.rs", "software/v5/aggregate/receipt.rs"}


def need(value, reason):
    if not value:
        raise ValueError(reason)


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def load(name, path, digest):
    need(sha(path) == digest, "HELPER_PIN:" + str(path))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    started, cpu = time.monotonic(), time.process_time()
    need(os.name == "nt" and Path.cwd() == ROOT
         and Path(__file__).resolve() == SOURCE / "build.py"
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize and len(sys.argv) == 3, "EXACT_OWNER_INVOCATION")
    selection = Path(sys.argv[1]).resolve(strict=True)
    need(selection.parent == HERE and selection.stat().st_size <= 2 * 1024**2
         and sha(selection) == sys.argv[2], "EXACT_SELECTION")
    chosen = json.loads(selection.read_bytes())
    need(set(chosen) == {"schema", "name", "authorizes_compile_only", "sources",
                         "integrated_result", "runtime_pins"}
         and chosen["schema"] == "DMKN_V5_AGGREGATE_HOST_BUILD_V1"
         and chosen["authorizes_compile_only"] is True
         and type(chosen["name"]) is str
         and re.fullmatch(r"aggregate-host-build-[0-9]{2}", chosen["name"]), "SELECTION_FIELDS")
    need(type(chosen["sources"]) is dict and set(chosen["sources"]) == SOURCE_SET,
         "THREE_SOURCE_CLOSURE")
    need(type(chosen["runtime_pins"]) is dict and 1 <= len(chosen["runtime_pins"]) <= 8192,
         "BOUNDED_EXACT_RUNTIME_MAP")
    integrated = chosen["integrated_result"]
    need(set(integrated) == {"path", "bytes", "sha256"}, "INTEGRATED_RESULT_FIELDS")
    result_path = Path(integrated["path"])
    need(result_path.is_absolute() and result_path.resolve(strict=True) == result_path
         and result_path.parent.parent == HERE and result_path.name == "RESULT.json"
         and re.fullmatch(r"proof-validation-integration-build-[0-9]{2}", result_path.parent.name)
         and result_path.stat().st_size == integrated["bytes"]
         and sha(result_path) == integrated["sha256"], "EXACT_INTEGRATED_BUILD")
    built = json.loads(result_path.read_bytes())
    need(built["status"] == "PASS_PROOF_VALIDATION_FOUR_COMPILES_ONLY"
         and built["job"]["active_processes"] == 0
         and built["job"]["terminated_processes"] == 0, "ADOPTED_INTEGRATED_BUILD")
    need(sha(OLD / "RESULT.json") == OLD_RESULT_SHA, "RETAINED_HOST_RECIPE")
    prior = json.loads((OLD / "RESULT.json").read_bytes())
    need(prior["status"] == "PASS_MODULE_HOST_COMPILE_ONLY" and len(prior["commands"]) == 1,
         "ONE_RETAINED_SUCCESSFUL_HOST_COMPILE")
    h = load("aggregate_host_support", SUPPORT, SUPPORT_SHA)
    old = h.load("aggregate_host_prior_build", h.PREDECESSOR, h.PREDECESSOR_SHA)
    q = h.load("aggregate_host_prior", old.PRIOR, old.PRIOR_SHA)
    a = h.load("aggregate_host_artifacts", q.CRYPTO / "artifacts.py", q.HELPERS["artifacts.py"])
    p = h.load("aggregate_host_provision", q.CRYPTO / "provision_build.py", q.HELPERS["provision_build.py"])
    c = h.load("aggregate_host_census", q.CRYPTO / "continue_build03.py", q.HELPERS["continue_build03.py"])
    r = h.load("aggregate_host_phase", ROOT / "experiments/scale-equation-01/runtime.py", q.RUNTIME_SHA)
    p.a, c.a, c.p, c.HERE = a, a, p, HERE
    r.LOG_LIMIT = 1048576
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

    def check_inputs():
        need(time.monotonic() - started <= 600 and time.process_time() - cpu <= 120,
             "HOST_BUILD_TOTAL_ENVELOPE")
        need(sha(selection) == sys.argv[2] and sha(SUPPORT) == SUPPORT_SHA
             and sha(h.PREDECESSOR) == h.PREDECESSOR_SHA
             and sha(old.PRIOR) == old.PRIOR_SHA
             and sha(OLD / "RESULT.json") == OLD_RESULT_SHA, "BUILD_SOURCE_IDENTITY")
        need(result_path.stat().st_size == integrated["bytes"]
             and sha(result_path) == integrated["sha256"]
             and not (result_path.parent / "FINALIZATION-FAILED.json").exists(), "INTEGRATED_FINAL_RESULT")
        marker = json.loads((HERE / (result_path.parent.name + "-attempt.json")).read_bytes())
        need(marker == {"status": built["status"], "result_sha256": integrated["sha256"]},
             "INTEGRATED_FINALIZATION_MARKER")
        for name, pin in built["outputs"].items():
            need(a.pin(result_path.parent / name) == pin, "INTEGRATED_ARTIFACT:" + name)
        for relative, pin in chosen["sources"].items():
            need(set(pin) == {"bytes", "sha256"}, "SOURCE_PIN_FIELDS")
            path = ROOT / relative
            need(path.stat().st_size == pin["bytes"] and sha(path) == pin["sha256"], "SOURCE_PIN:" + relative)
        for name, digest in chosen["runtime_pins"].items():
            path = Path(name)
            need(path.is_absolute() and path.resolve(strict=True) == path
                 and path.is_file() and sha(path) == digest, "RUNTIME_PIN:" + name)
        for name, digest in q.HELPERS.items():
            need(sha(q.CRYPTO / name) == digest, "SUPERVISOR_HELPER_PIN")
        need(sha(ROOT / "experiments/scale-equation-01/runtime.py") == q.RUNTIME_SHA
             and sha(p.HELPERS / "run_stage.py") == p.HELPER_SHA
             and sha(p.HELPERS / "domains.py") == p.DOMAINS_SHA
             and sha(p.PYTHON) == p.PYTHON_SHA
             and sha(p.PYTHON.parent / "python314.dll") == p.PYTHON_DLL_SHA, "SUPERVISOR_RUNTIME_PINS")

    check_inputs()
    need(not run.exists() and not attempt.exists(), "FRESH_HOST_BUILD")
    run.mkdir()
    (run / "commands").mkdir()
    h.save(run / "selection.json", chosen)
    phase = None
    result = {"schema": "DMKN_V5_AGGREGATE_HOST_BUILD_RESULT_V1", "status": "FAIL",
              "selection_sha256": sys.argv[2], "backend_rebuilds": 0, "relation_rebuilds": 0,
              "host_calls": 0, "guest_calls": 0, "proof_calls": 0, "network_calls": 0,
              "authority": "HOST_COMPILE_ONLY_NOT_ADMISSION"}

    class Budget:
        def __init__(self):
            self.peak = {"working_bytes": 0, "entries": 0}
            self.current = {}

        def refresh(self):
            need(time.monotonic() - started <= 600 and time.process_time() - cpu <= 120,
                 "HOST_BUILD_TOTAL_ENVELOPE")
            self.current = c.census(run)
            need(self.current["working_bytes"] <= 1024**3 and self.current["entries"] <= 8192,
                 "HOST_BUILD_OUTPUT_ENVELOPE")
            for key in self.peak:
                self.peak[key] = max(self.peak[key], self.current[key])

    budget = Budget()
    try:
        snapshot = run / "source"
        for relative, pin in chosen["sources"].items():
            target = snapshot / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream:
                stream.write((ROOT / relative).read_bytes())
            need(target.stat().st_size == pin["bytes"] and sha(target) == pin["sha256"], "EXACT_SNAPSHOT")
        h.save(run / "source-map.json", chosen["sources"])
        command = list(prior["commands"][0]["argv"])

        def replace(before, after):
            need(command.count(str(before)) == 1, "EXACT_RECIPE_SUBSTITUTION:" + str(before))
            command[command.index(str(before))] = str(after)

        replace("module_host", "aggregate_host")
        replace(OLD / "source/src/bin/module_host.rs", snapshot / "software/v5/aggregate_host/aggregate_host.rs")
        replace(OLD / "module_host.exe", run / "aggregate_host.exe")
        need("lto=fat" in command and "--test" not in command and command.count("--extern") == 5,
             "RETAINED_EXACT_HOST_RECIPE")
        command += ["-L", "dependency=" + str(result_path.parent), "-L",
                    "dependency=" + str(ROOT / "experiments/general-checker-01/build-01/target/release/deps")]
        for name in ("dmkn_module_relation", "dmkn_aggregate_relation"):
            command += ["--extern", name + "=" + str(result_path.parent / ("lib" + name + ".rlib"))]
        # All explicit direct libraries are among the selected immutable inputs.
        for index, argument in enumerate(command):
            if argument == "--extern":
                path = command[index + 1].split("=", 1)[1]
                need(path in chosen["runtime_pins"], "UNPINNED_DIRECT_LIBRARY:" + path)
        need(command[0] in chosen["runtime_pins"], "UNPINNED_COMPILER")
        h.save(run / "compile-command.json", command)
        env, environment = p.environment(run, c.OLD / "rust")
        env["VCToolsUserTelemetryOptOut"] = "1"
        environment["environment_keys_only"] = sorted(env)
        h.save(run / "environment-profile.json", environment)

        def exact_job(seconds, _memory, active_processes):
            need(seconds == 240 and active_processes == 8, "ADOPTED_PHASE_SHAPE")
            return run_stage.Job(240, 3072, active_processes=6)

        budget.refresh()
        phase = r.phase_class(p, a)("aggregate-host-link", run, budget, env, exact_job, 240)
        phase.invoke("aggregate-host", command, ROOT, allow_build_telemetry=True)
        result.update(status="PASS_AGGREGATE_HOST_ONE_LINK_ONLY", executable=a.pin(run / "aggregate_host.exe"))
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
            check_inputs()
            need(json.loads((run / "selection.json").read_bytes()) == chosen, "SAVED_SELECTION_PIN")
            need(c.file_map(run / "source") == chosen["sources"], "FINAL_SOURCE_SNAPSHOT")
            budget.refresh()
        except BaseException as error:
            result.update(status="FAIL_FINAL_CHECK", final_error=str(error)[:3000])
        result.update(controller_cpu_seconds=time.process_time() - cpu,
                      wall_seconds=time.monotonic() - started, output_census=budget.current,
                      sampled_peaks=budget.peak,
                      accounting="CONTROLLER_DISJOINT_FROM_INCLUSIVE_WORKER_JOB;REPORT_EXIT_TAIL_EXCLUDED")
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
    return 0 if result["status"] == "PASS_AGGREGATE_HOST_ONE_LINK_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
