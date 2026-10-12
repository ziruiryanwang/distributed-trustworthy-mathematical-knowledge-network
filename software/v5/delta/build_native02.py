"""Fresh driver successor using a current-profile native checker, no guest/prover.

Uses the adopted telemetry-aware Windows Job supervisor. Only its own remaining
exact pinned MSVC telemetry processes may be closed after successful compilation.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
SOURCE = ROOT / "software/v5/delta"
RUN = HERE / "delta-native-build-02"
ATTEMPT = HERE / "delta-native-build-02-attempt.json"
PROPOSAL = SOURCE / "NATIVE-BUILD02-PROPOSAL.json"
PROPOSAL_SHA = "b0d037459b950c3cbabd1c2554aebf1fe9611820598d370eb40f4d69e700885d"
PRIOR = ROOT / "experiments/general-checker-guest-01/prepare.py"
PRIOR_SHA = "af2d128e831c0bbc3056c516c803fdeab56f69d2a96ca7355a8b22e06f8be529"


def need(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def save(path, value):
    with path.open("xb") as stream:
        stream.write((json.dumps(value, sort_keys=True, indent=2) + "\n").encode())


def load(name, path, digest):
    need(sha(path) == digest, "HELPER_PIN:" + str(path))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    started, cpu = time.monotonic(), time.process_time()
    need(Path.cwd() == ROOT and Path(__file__).resolve() == SOURCE / "build_native02.py",
         "CANONICAL_ROOT")
    need(os.name == "nt" and sys.dont_write_bytecode and sys.flags.ignore_environment
         and sys.flags.no_site and sys.flags.no_user_site and len(sys.argv) == 3,
         "ISOLATED_CALL")
    selection = Path(sys.argv[1]).resolve(strict=True)
    need(selection.is_relative_to(HERE) and selection.stat().st_size <= 65536
         and sha(selection) == sys.argv[2], "EXACT_SELECTION")
    chosen = json.loads(selection.read_bytes())
    need(set(chosen) == {"schema", "authorizes_compile_only", "driver_sha256", "proposal_sha256"}
         and chosen["schema"] == "DMKN_V5_DELTA_BUILD_SELECTION_V1"
         and chosen["authorizes_compile_only"] is True
         and chosen["proposal_sha256"] == PROPOSAL_SHA
         and sha(Path(__file__)) == chosen["driver_sha256"], "EXACT_SCOPE")
    need(sha(PROPOSAL) == PROPOSAL_SHA, "PROPOSAL_PIN")
    proposal = json.loads(PROPOSAL.read_bytes())
    need(proposal["name"] == "delta-native-build-02"
         and proposal["limits"] == {"stdout_bytes":1048576,"stderr_bytes":1048576,
             "cpu_seconds":240,"wall_seconds":300,"memory_mib":3072,"active_processes":6},
         "PROPOSAL_LIMITS")
    q = load("delta_prior", PRIOR, PRIOR_SHA)
    a = load("delta_artifacts", q.CRYPTO / "artifacts.py", q.HELPERS["artifacts.py"])
    p = load("delta_provision", q.CRYPTO / "provision_build.py", q.HELPERS["provision_build.py"])
    c = load("delta_census", q.CRYPTO / "continue_build03.py", q.HELPERS["continue_build03.py"])
    r = load("delta_phase", ROOT / "experiments/scale-equation-01/runtime.py", q.RUNTIME_SHA)
    p.a, c.a, c.p, c.HERE = a, a, p, HERE
    # Tighter combined log cap implies each proposed stream cap.
    r.LOG_LIMIT = 1048576
    need(Path(sys.executable).resolve() == p.PYTHON and sha(p.PYTHON) == p.PYTHON_SHA
         and sha(p.PYTHON.parent / "python314.dll") == p.PYTHON_DLL_SHA, "PYTHON_PIN")
    need(sha(p.HELPERS / "run_stage.py") == p.HELPER_SHA
         and sha(p.HELPERS / "domains.py") == p.DOMAINS_SHA, "JOB_HELPERS")
    sys.path.insert(0, str(p.HELPERS))
    import run_stage
    import domains
    need(Path(run_stage.__file__).resolve() == p.HELPERS / "run_stage.py"
         and Path(domains.__file__).resolve() == p.HELPERS / "domains.py", "JOB_ORIGIN")
    c.h = run_stage

    def check_inputs():
        need(sha(selection) == sys.argv[2] and sha(PROPOSAL) == PROPOSAL_SHA
             and sha(Path(__file__)) == chosen["driver_sha256"], "SELECTION_CHANGED")
        for relative, pin in proposal["source_pins"].items():
            path = ROOT / relative
            need(path.resolve(strict=True).is_relative_to(ROOT)
                 and path.stat().st_size == pin["bytes"] and sha(path) == pin["sha256"],
                 "SOURCE_PIN:" + relative)
        for name, digest in proposal["runtime_pins_rechecked"].items():
            need(sha(Path(name)) == digest, "RUNTIME_PIN:" + name)
        need(sha(PRIOR) == PRIOR_SHA, "PRIOR_CHANGED")
        for name, digest in q.HELPERS.items():
            need(sha(q.CRYPTO / name) == digest, "HELPER_CHANGED:" + name)
        need(sha(ROOT / "experiments/scale-equation-01/runtime.py") == q.RUNTIME_SHA
             and sha(p.HELPERS / "run_stage.py") == p.HELPER_SHA
             and sha(p.HELPERS / "domains.py") == p.DOMAINS_SHA
             and sha(p.PYTHON) == p.PYTHON_SHA
             and sha(p.PYTHON.parent / "python314.dll") == p.PYTHON_DLL_SHA,
             "CONTROLLER_RUNTIME_CHANGED")
        need(time.monotonic()-started <= 300 and time.process_time()-cpu <= 60,
             "CONTROLLER_ENVELOPE")

    check_inputs()
    need(not RUN.exists(), "FRESH_BUILD_OUTPUT")
    RUN.mkdir()
    (RUN / "commands").mkdir()
    sources = dict(proposal["source_pins"])
    sources["software/v5/delta/build_native02.py"] = {
        "bytes":Path(__file__).stat().st_size,"sha256":chosen["driver_sha256"]}
    sources["software/v5/delta/NATIVE-BUILD02-PROPOSAL.json"] = {
        "bytes":PROPOSAL.stat().st_size,"sha256":PROPOSAL_SHA}
    save(RUN / "selection.json", chosen)

    class Budget:
        def __init__(self):
            self.run, self.peak = RUN, {"working_bytes":0,"entries":0}
        def refresh(self):
            need(time.monotonic()-started <= 300 and time.process_time()-cpu <= 60,
                 "CONTROLLER_ENVELOPE")
            data = c.census(RUN)
            need(data["working_bytes"] <= 1024**3 and data["entries"] <= 8192,
                 "BUILD_OUTPUT_ENVELOPE")
            for name in self.peak:
                self.peak[name] = max(self.peak[name], data[name])
            self.current = data

    budget, phase = Budget(), None
    result = {"status":"FAIL","scope":"NATIVE_DRIVER_COMPILE_ONLY",
        "guest_calls":0,"proof_calls":0,"network_calls":0,"dependency_rebuilds":0,
        "proposal_sha256":PROPOSAL_SHA,"selection_sha256":sys.argv[2],
        "limits":proposal["limits"],"stricter_phase_wall_seconds":240,
        "combined_log_bytes":1048576,"started_utc":p.utc(),
        "timing_scope":"PRE_REPORT_WRITE_AND_EXIT_TAILS_EXCLUDED"}
    try:
        # Preserve the source-relative module layout; never compile the mutable tree.
        for relative, pin in sources.items():
            dest = RUN / "source" / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            with dest.open("xb") as stream:
                stream.write((ROOT / relative).read_bytes())
            need(dest.stat().st_size == pin["bytes"] and sha(dest) == pin["sha256"],
                 "SNAPSHOT_PIN")
        env, environment = p.environment(RUN, c.OLD / "rust")
        env["VCToolsUserTelemetryOptOut"] = "1"
        environment["environment_keys_only"] = sorted(env)
        save(RUN / "environment-profile.json", environment)
        save(RUN / "source-map.json", sources)
        argv = [arg.replace("{snapshot}", str(RUN / "source")).replace("{output}", str(RUN))
                for arg in proposal["argv"]]

        def exact_job(seconds, _memory, active_processes):
            need(seconds == 240 and active_processes == 8, "ADOPTED_JOB_CALL_SHAPE")
            return run_stage.Job(240, 3072, active_processes=6)

        budget.refresh()
        phase = r.phase_class(p, a)("delta-native-compile", RUN, budget, env, exact_job, 240)
        phase.invoke("compile-driver", argv, ROOT, allow_build_telemetry=True)
        executable = RUN / "native_delta.exe"
        need(executable.is_file(), "NATIVE_DRIVER_OUTPUT")
        result.update(status="PASS_DELTA_NATIVE_DRIVER_BUILD_ONLY", executable=a.pin(executable))
    except BaseException as error:
        result["error"] = type(error).__name__ + ": " + str(error)[:4000]
    finally:
        if phase is not None:
            try:
                phase.close()
            except BaseException as error:
                result["status"], result["cleanup_error"] = "FAIL_CLEANUP", str(error)[:2000]
            result["job"], result["commands"] = phase.final_stats, phase.commands
        try:
            check_inputs()
            need(json.loads((RUN / "selection.json").read_bytes()) == chosen, "SAVED_SELECTION_CHANGED")
            need(c.file_map(RUN / "source") == sources, "SNAPSHOT_CHANGED")
            budget.refresh()
            result["final_storage"] = budget.current
        except BaseException as error:
            result["status"], result["final_check_error"] = "FAIL_FINAL_CHECK", str(error)[:3000]
        result.update(controller_cpu_seconds=time.process_time()-cpu,
                      wall_seconds=time.monotonic()-started, sampled_peaks=budget.peak,
                      finished_utc=p.utc())
        save(RUN / "RESULT.json", result)
    print(json.dumps({k:result.get(k) for k in ("status","error","wall_seconds")}))
    return 0 if result["status"] == "PASS_DELTA_NATIVE_DRIVER_BUILD_ONLY" else 1


def attempt():
    started, cpu = time.monotonic(), time.process_time()
    need(Path.cwd() == ROOT and Path(__file__).resolve() == SOURCE / "build_native02.py",
         "CANONICAL_ATTEMPT_ROOT")
    need(not ATTEMPT.exists(), "FRESH_ATTEMPT")
    result = {"status":"FAIL_PREALLOCATION","allocation_preexisted":RUN.exists(),
              "scope":"OUTER_CONTROLLER_COST_INCLUDES_MAIN_NOT_WORKER",
              "timing_scope":"PRE_ATTEMPT_REPORT_WRITE_AND_EXIT_TAILS_EXCLUDED"}
    code = 1
    try:
        code = main()
        result["status"] = "RETURNED_PASS" if code == 0 else "RETURNED_FAILURE"
    except BaseException as error:
        result["error"] = type(error).__name__ + ": " + str(error)[:4000]
    finally:
        result.update(exit_code=code,controller_cpu_seconds=time.process_time()-cpu,
                      controller_wall_seconds=time.monotonic()-started)
        if not result["allocation_preexisted"] and (RUN / "RESULT.json").is_file():
            result["worker_cost_evidence"] = {"path":str(RUN / "RESULT.json"),
                                              "sha256":sha(RUN / "RESULT.json")}
        save(ATTEMPT, result)
    print(json.dumps({"attempt":str(ATTEMPT),"status":result["status"],"exit_code":code}))
    return code


if __name__ == "__main__":
    raise SystemExit(attempt())
