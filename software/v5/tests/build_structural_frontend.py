"""Finite structural differential link; reuse dependencies without backend rebuild.

Owner selection only. Reuse the reviewed Job/owned-telemetry lifecycle, pin a
bounded retained native-runtime map, and preserve selected source snapshots. This
links the harness but does not run it or execute a mathematical guest.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
SELF = ROOT / "software/v5/tests/build_structural_frontend.py"
RUN = HERE / "structural-frontend-build-01"
ATTEMPT = HERE / "structural-frontend-build-01-attempt.json"
REFERENCE = HERE / "receipt-native-build-01-selection.json"
REFERENCE_SHA = "b9e1b2d77bc8af80a31fe543b251dfc5790b5296613173ed115a43df4e634bf5"
SOURCES = {"software/v5/tests/build_structural_frontend.py",
    "software/v5/tests/structural_frontend_differential.rs", "software/v5/tests/STRUCTURAL-FRONTEND-PLAN.md",
    "software/v5/modules/receipt/generate_foundation_static.py",
    *{"software/v5/modules/receipt/src/" + name for name in
      ("foundation_static.rs", "foundation_data.rs", "input.rs", "canonical.rs", "relation.rs",
       "main.rs", "lib.rs", "bin/receipt_native.rs", "commitments.rs", "journal.rs", "policy.rs")},
    *{"software/v5/modules/native/checker/src/" + name + ".rs" for name in
      ("lib", "debug_printer", "demand", "env", "expr", "inductive", "level", "module",
       "module_correspondence", "name", "parser", "pretty_printer", "quot", "tc", "unique_hasher", "util")}}
DEPS = ROOT / "experiments/general-checker-01/build-01/target/release/deps"
EXTERNS = {name: DEPS / filename for name, filename in {
    "indexmap": "libindexmap-9eaaa603bb190ed4.rlib",
    "num_bigint": "libnum_bigint-c5c13f7fb9dd726f.rlib",
    "num_integer": "libnum_integer-04ee8a9ec8e49c7a.rlib",
    "num_traits": "libnum_traits-7c9867555cfaf665.rlib",
    "rustc_hash": "librustc_hash-02ff40f9af9d7c16.rlib",
    "semver": "libsemver-226430743f1c7e33.rlib",
    "serde": "libserde-d2875ea8be5e26d6.rlib",
    "serde_json": "libserde_json-d8d8d972d853b6e4.rlib"}.items()}
PRIOR = ROOT / "experiments/general-checker-guest-01/prepare.py"
PRIOR_SHA = "af2d128e831c0bbc3056c516c803fdeab56f69d2a96ca7355a8b22e06f8be529"
LIMITS = {"worker_seconds": 180, "wall_seconds": 300, "memory_mib": 4096,
          "active_processes": 8, "combined_working_bytes": 6 * 1024**3}


def need(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def load(name, path, digest):
    need(sha(path) == digest, "HELPER_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    started, cpu = time.monotonic(), time.process_time()
    need(os.name == "nt" and Path.cwd() == ROOT and Path(__file__).resolve() == SELF
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize and len(sys.argv) == 3, "CANONICAL_ISOLATED_INVOCATION")
    selection = Path(sys.argv[1])
    need(selection.is_absolute() and selection.resolve(strict=True) == selection
         and selection.parent == HERE and selection.stat().st_size <= 65536
         and sha(selection) == sys.argv[2], "EXACT_SELECTION")
    selected = json.loads(selection.read_bytes())
    need(set(selected) == {"schema", "authorizes_compile_only_and_owned_telemetry_cleanup",
         "sources", "limits", "runtime_reference_sha256"}
         and selected["schema"] == "DMKN_STRUCTURAL_FRONTEND_BUILD_V1"
         and selected["authorizes_compile_only_and_owned_telemetry_cleanup"] is True
         and set(selected["sources"]) == SOURCES and selected["limits"] == LIMITS
         and selected["runtime_reference_sha256"] == REFERENCE_SHA, "SELECTED_BUILD_SCOPE")
    need(sha(REFERENCE) == REFERENCE_SHA, "ADOPTED_RUNTIME_REFERENCE")
    for name, record in selected["sources"].items():
        path = ROOT / name
        need(set(record) == {"bytes", "sha256"} and type(record["bytes"]) is int
             and 0 < record["bytes"] <= 2**20 and path.stat().st_size == record["bytes"]
             and sha(path) == record["sha256"], "SOURCE_PIN:" + name)
    q = load("_diff_prior", PRIOR, PRIOR_SHA)
    a = load("_diff_artifacts", q.CRYPTO / "artifacts.py", q.HELPERS["artifacts.py"])
    p = load("_diff_provision", q.CRYPTO / "provision_build.py", q.HELPERS["provision_build.py"])
    c = load("_diff_census", q.CRYPTO / "continue_build03.py", q.HELPERS["continue_build03.py"])
    phase_path = ROOT / "experiments/scale-equation-01/runtime.py"
    r = load("_diff_runtime", phase_path, q.RUNTIME_SHA)
    p.a, c.a, c.p, c.HERE = a, a, p, HERE
    a.DISK_LIMIT = LIMITS["combined_working_bytes"]
    need(Path(sys.executable).resolve() == p.PYTHON and sha(p.PYTHON) == p.PYTHON_SHA
         and sha(p.PYTHON.parent / "python314.dll") == p.PYTHON_DLL_SHA, "EXACT_PYTHON_ORIGIN")
    need(sha(p.HELPERS / "run_stage.py") == p.HELPER_SHA
         and sha(p.HELPERS / "domains.py") == p.DOMAINS_SHA, "JOB_HELPERS")
    sys.path.insert(0, str(p.HELPERS))
    import run_stage
    import domains
    need(Path(run_stage.__file__).resolve() == p.HELPERS / "run_stage.py"
         and Path(domains.__file__).resolve() == p.HELPERS / "domains.py", "JOB_HELPER_ORIGINS")
    c.h = run_stage

    # Reuse the exact explicit native-wrapper/compiler map. The narrower link
    # below needs only eight checker dependencies and Windows system libraries.
    reference = json.loads(REFERENCE.read_bytes())
    runtime = reference["runtime_pins"]
    need(1 <= len(runtime) <= 256 and all(str(path) in runtime for path in EXTERNS.values()),
         "BOUNDED_NATIVE_RUNTIME_MAP")

    def runtime_pins():
        pins = {}
        for name, digest in runtime.items():
            path = Path(name)
            a.regular_stat(path, allow_hardlinks=True)
            need(path.is_absolute() and path.resolve(strict=True) == path and path.is_file()
                 and path.stat().st_size <= 512 * 1024**2 and sha(path) == digest,
                 "EXPLICIT_RUNTIME_PIN:" + name)
            pins[name] = {"bytes": path.stat().st_size, "sha256": digest}
        need(sum(row["bytes"] for row in pins.values()) <= 2 * 1024**3, "RUNTIME_TOTAL_BOUND")
        return pins

    held_runtime = runtime_pins()
    need(not RUN.exists(), "FRESH_BUILD_ALLOCATION")
    RUN.mkdir()
    reserve = sum(row["bytes"] for row in held_runtime.values()) + 2 * 1024**3

    class Budget(a.Budget):
        def refresh(self):
            observed = c.census(self.run)
            self.current = {key: observed[key] for key in ("working_bytes", "retained_archive_bytes", "entries")}
            self.current["working_bytes"] += reserve
            self.current["retained_archive_bytes"] += 192 * 1024**2
            self.current["entries"] += len(held_runtime) + 30000
            need(self.current["entries"] <= a.ENTRY_LIMIT, "COMBINED_ENTRY_BOUND")
            self.check()

    budget = Budget(RUN, started + LIMITS["wall_seconds"])
    phase = None
    result = {"status": "FAIL", "scope": "STRUCTURAL_FRONTEND_COMPILE_ONLY",
              "selection": a.pin(selection), "started_utc": p.utc(), "test_calls": 0,
              "kernel_calls": 0, "guest_executions": 0, "proof_calls": 0, "network_calls": 0,
              "runtime_pin_scope": "BOUNDED_RETAINED_NATIVE_MAP_NOT_HERMETIC_SEARCH_DIRECTORY_OR_OS_PROOF"}
    try:
        budget.refresh()
        (RUN / "commands").mkdir()
        c.copy_map(ROOT, RUN / "source", selected["sources"], budget)
        with (RUN / "selection.json").open("xb") as stream:
            stream.write(selection.read_bytes())
        env, environment = p.environment(RUN, c.OLD / "rust")
        env["VCToolsUserTelemetryOptOut"] = "1"
        environment["environment_keys_only"] = sorted(env)
        a.save(RUN / "environment-profile.json", environment)
        a.save(RUN / "LINK-INPUTS.json", {"runtime_reference": a.pin(REFERENCE),
            "runtime_pins": held_runtime, "externs": {key: a.pin(path) for key, path in EXTERNS.items()},
            "source_map": selected["sources"], "dependency_search_path": str(DEPS),
            "scope": result["runtime_pin_scope"]})
        executable = RUN / "structural_frontend.exe"
        compiler = c.OLD / "rust/bin/rustc.exe"
        need(str(compiler) in runtime and env["CARGO_TARGET_X86_64_PC_WINDOWS_MSVC_LINKER"] in runtime,
             "SELECTED_COMPILER_LINKER")
        linker = env["CARGO_TARGET_X86_64_PC_WINDOWS_MSVC_LINKER"]
        argv = [str(compiler), "--edition=2021", "--target", "x86_64-pc-windows-msvc",
                "--crate-type", "bin", "--crate-name", "structural_frontend",
                "-C", "overflow-checks=yes", "-C", "panic=unwind", "-C", "opt-level=2",
                "-C", "linker=" + linker, "-C", "link-arg=/DEBUG:NONE",
                str(RUN / "source/software/v5/tests/structural_frontend_differential.rs"),
                "-o", str(executable), "-L", "dependency=" + str(DEPS)]
        # Only the retained Windows system-library search paths, no RISC0/backend.
        retained = reference["argv"]
        for index, argument in enumerate(retained[:-1]):
            if argument == "-L" and retained[index+1].startswith(r"native=C:\Program Files"):
                argv.extend(["-L", retained[index+1]])
        for name, path in EXTERNS.items():
            argv.extend(["--extern", name + "=" + str(path)])
        phase = r.phase_class(p, a)("structural-frontend-compile", RUN, budget, env,
                                     run_stage.Job, LIMITS["worker_seconds"])
        phase.invoke("compile-harness", argv, ROOT, allow_build_telemetry=True)
        need(executable.is_file(), "ACTUAL_HARNESS_EXECUTABLE")
        result.update(status="PASS_STRUCTURAL_FRONTEND_COMPILE_ONLY", executable=a.pin(executable))
    except BaseException as error:
        result["error"] = type(error).__name__ + ": " + str(error)[:3000]
    finally:
        if phase is not None:
            try:
                phase.close()
            except BaseException as error:
                result.update(status="FAIL_CLEANUP", cleanup_error=str(error)[:2000])
            result["job"], result["commands"] = phase.final_stats, phase.commands
        try:
            need(sha(selection) == sys.argv[2] and sha(REFERENCE) == REFERENCE_SHA
                 and sha(PRIOR) == PRIOR_SHA, "SELECTED_INPUTS_CHANGED")
            need(runtime_pins() == held_runtime, "EXPLICIT_RUNTIME_CHANGED")
            need(c.file_map(RUN / "source") == selected["sources"], "SNAPSHOT_CHANGED")
            need(sha(RUN / "selection.json") == sys.argv[2], "SAVED_SELECTION_CHANGED")
            for name, record in selected["sources"].items():
                need((ROOT / name).stat().st_size == record["bytes"]
                     and sha(ROOT / name) == record["sha256"], "SOURCE_CHANGED")
            for name, digest in q.HELPERS.items():
                need(sha(q.CRYPTO / name) == digest, "HELPER_CHANGED")
            need(sha(phase_path) == q.RUNTIME_SHA and sha(p.HELPERS / "run_stage.py") == p.HELPER_SHA
                 and sha(p.HELPERS / "domains.py") == p.DOMAINS_SHA
                 and sha(p.PYTHON) == p.PYTHON_SHA
                 and sha(p.PYTHON.parent / "python314.dll") == p.PYTHON_DLL_SHA, "SUPERVISOR_CHANGED")
            budget.refresh()
            result["final_storage"] = c.census(RUN)
        except BaseException as error:
            result.update(status="FAIL_FINAL_BINDING", binding_error=str(error)[:3000])
        result.update(controller_cpu_seconds=time.process_time() - cpu,
                      wall_seconds=time.monotonic() - started,
                      sampled_reserved_peaks=budget.peak, finished_utc=p.utc())
        if result["wall_seconds"] > LIMITS["wall_seconds"]:
            result["status"] = "FAIL_TOTAL_WALL_LIMIT"
        a.save(RUN / "RESULT.json", result)
    print(json.dumps({key: result.get(key) for key in ("status", "error", "wall_seconds")}))
    return 0 if result["status"] == "PASS_STRUCTURAL_FRONTEND_COMPILE_ONLY" else 1


def attempt():
    started, cpu = time.monotonic(), time.process_time()
    need(Path.cwd() == ROOT and Path(__file__).resolve() == SELF and not ATTEMPT.exists(),
         "FRESH_CANONICAL_ATTEMPT")
    report = {"schema": "DMKN_STRUCTURAL_FRONTEND_BUILD_ATTEMPT_V1", "status": "FAIL_PREALLOCATION",
              "allocation_preexisted": RUN.exists(), "worker_cost_evidence": None}
    code = 1
    try:
        code = main()
        report["status"] = "RETURNED_PASS" if code == 0 else "RETURNED_FAILURE"
    except BaseException as error:
        report["error"] = type(error).__name__ + ": " + str(error)[:3000]
        report["status"] = "FAIL_AFTER_ALLOCATION" if RUN.exists() else "FAIL_PREALLOCATION"
    finally:
        result_path = RUN / "RESULT.json"
        if not report["allocation_preexisted"] and result_path.is_file():
            report["worker_cost_evidence"] = {"path": str(result_path),
                "bytes": result_path.stat().st_size, "sha256": sha(result_path)}
        report.update(exit_code=code, controller_cpu_seconds=time.process_time() - cpu,
            controller_wall_seconds=time.monotonic() - started,
            scope="Outer controller includes main controller; do not sum. Worker CPU is separate in run result.")
        with ATTEMPT.open("xb") as stream:
            stream.write((json.dumps(report, sort_keys=True, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({"attempt": str(ATTEMPT), "status": report["status"], "exit_code": code}))
    return code


if __name__ == "__main__":
    raise SystemExit(attempt())
