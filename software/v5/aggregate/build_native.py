"""Compile-only aggregate source controller; root supplies exact finite selection.

Four thin Rust artifacts reuse retained native checker/dependencies. No Cargo,
checker rebuild, test execution, guest, proof, receipt admission or networking.
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
SOURCE = ROOT / "software/v5/aggregate"
RECIPE = ROOT / "software/v5/delta/NATIVE-BUILD02-PROPOSAL.json"
RECIPE_SHA = "b0d037459b950c3cbabd1c2554aebf1fe9611820598d370eb40f4d69e700885d"
PRIOR = ROOT / "experiments/general-checker-guest-01/prepare.py"
PRIOR_SHA = "af2d128e831c0bbc3056c516c803fdeab56f69d2a96ca7355a8b22e06f8be529"
CHECKER = HERE / "native-library-02/libnanoda_lib.rlib"
CHECKER_SHA = "ba6d0db2e614c2bb032ca5d92d97d31a7ebfe87f85fa6cce6fe5549483b7c651"
AGGREGATE = ("lib.rs", "header.rs", "membership.rs", "wire.rs", "census.rs",
             "relation.rs", "tests.rs", "graph_controls.rs", "native.rs", "build_native.py")
RELATION = ("lib.rs", "canonical.rs", "input.rs", "foundation_static.rs", "foundation_data.rs",
            "commitments.rs", "journal.rs", "policy.rs", "relation.rs")


def need(value, reason):
    if not value: raise ValueError(reason)


def sha(path):
    with path.open("rb") as stream: return hashlib.file_digest(stream, "sha256").hexdigest()


def save(path, value):
    with path.open("xb") as stream:
        stream.write((json.dumps(value, sort_keys=True, indent=2, allow_nan=False)+"\n").encode())


def load(name, path, digest):
    need(sha(path) == digest, "HELPER_PIN:"+str(path))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    started, cpu = time.monotonic(), time.process_time()
    need(os.name == "nt" and Path.cwd() == ROOT and Path(__file__).resolve() == SOURCE/"build_native.py"
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize and len(sys.argv) == 3, "ISOLATED_CANONICAL_BUILD")
    selection = Path(sys.argv[1]).resolve(strict=True)
    need(selection.is_relative_to(HERE) and selection.stat().st_size <= 65536
         and sha(selection) == sys.argv[2], "EXACT_BUILD_SELECTION")
    chosen = json.loads(selection.read_bytes())
    need(set(chosen) == {"schema", "name", "authorizes_compile_only", "sources"}
         and chosen["schema"] == "DMKN_V5_AGGREGATE_BUILD_V1"
         and chosen["authorizes_compile_only"] is True
         and type(chosen["name"]) is str and re.fullmatch(r"aggregate-native-build-[0-9]{2}", chosen["name"]),
         "BUILD_SELECTION_FIELDS")
    expected = {"software/v5/aggregate/"+name for name in AGGREGATE}
    expected.update("software/v5/modules/receipt/src/"+name for name in RELATION)
    need(type(chosen["sources"]) is dict and set(chosen["sources"]) == expected, "EXACT_BUILD_SOURCE_SET")
    need(sha(RECIPE) == RECIPE_SHA and sha(CHECKER) == CHECKER_SHA, "RETAINED_RECIPE_CHECKER")
    recipe = json.loads(RECIPE.read_bytes())
    q = load("aggregate_prior", PRIOR, PRIOR_SHA)
    a = load("aggregate_artifacts", q.CRYPTO/"artifacts.py", q.HELPERS["artifacts.py"])
    p = load("aggregate_provision", q.CRYPTO/"provision_build.py", q.HELPERS["provision_build.py"])
    c = load("aggregate_census", q.CRYPTO/"continue_build03.py", q.HELPERS["continue_build03.py"])
    r = load("aggregate_phase", ROOT/"experiments/scale-equation-01/runtime.py", q.RUNTIME_SHA)
    p.a, c.a, c.p, c.HERE = a, a, p, HERE
    r.LOG_LIMIT = 1048576
    need(Path(sys.executable).resolve() == p.PYTHON and sha(p.PYTHON) == p.PYTHON_SHA
         and sha(p.PYTHON.parent/"python314.dll") == p.PYTHON_DLL_SHA, "PINNED_PYTHON")
    need(sha(p.HELPERS/"run_stage.py") == p.HELPER_SHA and sha(p.HELPERS/"domains.py") == p.DOMAINS_SHA,
         "PINNED_JOB_HELPERS")
    sys.path.insert(0, str(p.HELPERS))
    import run_stage
    import domains
    need(Path(run_stage.__file__).resolve() == p.HELPERS/"run_stage.py"
         and Path(domains.__file__).resolve() == p.HELPERS/"domains.py", "JOB_ORIGIN")
    c.h = run_stage
    run = HERE/chosen["name"]
    attempt = HERE/(chosen["name"]+"-attempt.json")

    def check_inputs():
        need(time.monotonic()-started <= 600 and time.process_time()-cpu <= 60, "BUILD_CONTROLLER_ENVELOPE")
        need(sha(selection) == sys.argv[2] and sha(RECIPE) == RECIPE_SHA
             and sha(PRIOR) == PRIOR_SHA and sha(CHECKER) == CHECKER_SHA, "BUILD_PINS_CHANGED")
        for relative, pin in chosen["sources"].items():
            need(set(pin) == {"bytes", "sha256"}, "BUILD_SOURCE_PIN_FIELDS")
            path = ROOT/relative
            need(path.stat().st_size == pin["bytes"] and sha(path) == pin["sha256"], "BUILD_SOURCE_PIN:"+relative)
        for name, digest in recipe["runtime_pins_rechecked"].items():
            need(sha(Path(name)) == digest, "BUILD_RUNTIME_PIN:"+name)
        for name, digest in q.HELPERS.items(): need(sha(q.CRYPTO/name) == digest, "BUILD_HELPER_CHANGED")
        need(sha(ROOT/"experiments/scale-equation-01/runtime.py") == q.RUNTIME_SHA
             and sha(p.HELPERS/"run_stage.py") == p.HELPER_SHA and sha(p.HELPERS/"domains.py") == p.DOMAINS_SHA
             and sha(p.PYTHON) == p.PYTHON_SHA and sha(p.PYTHON.parent/"python314.dll") == p.PYTHON_DLL_SHA,
             "BUILD_CONTROLLER_RUNTIME_CHANGED")

    check_inputs()
    need(not run.exists() and not attempt.exists(), "FRESH_AGGREGATE_BUILD")
    run.mkdir(); (run/"commands").mkdir()
    save(run/"selection.json", chosen)
    phase = None
    result = {"schema":"DMKN_AGGREGATE_BUILD_RESULT_V1", "status":"FAIL",
        "selection_sha256":sys.argv[2], "proof_calls":0, "guest_calls":0, "test_calls":0,
        "checker_rebuilds":0, "network_calls":0, "authority":"COMPILE_ONLY_NOT_ADMISSION"}

    class Budget:
        def __init__(self): self.peak = {"working_bytes":0, "entries":0}; self.current = {}
        def refresh(self):
            need(time.monotonic()-started <= 600 and time.process_time()-cpu <= 60, "BUILD_TOTAL_ENVELOPE")
            self.current = c.census(run)
            need(self.current["working_bytes"] <= 1024**3 and self.current["entries"] <= 8192, "BUILD_OUTPUT_ENVELOPE")
            for key in self.peak: self.peak[key] = max(self.peak[key], self.current[key])

    budget = Budget()
    try:
        snapshot = run/"source"
        for relative, pin in chosen["sources"].items():
            target = snapshot/relative; target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream: stream.write((ROOT/relative).read_bytes())
            need(target.stat().st_size == pin["bytes"] and sha(target) == pin["sha256"], "BUILD_SNAPSHOT_PIN")
        save(run/"source-map.json", chosen["sources"])
        env, environment = p.environment(run, c.OLD/"rust")
        env["VCToolsUserTelemetryOptOut"] = "1"
        environment["environment_keys_only"] = sorted(env)
        save(run/"environment-profile.json", environment)
        old = recipe["argv"]
        search, externs = [], {}
        for index, arg in enumerate(old[:-1]):
            if arg == "-L": search.extend([arg, old[index+1]])
            if arg == "--extern":
                name, value = old[index+1].split("=",1); externs[name] = value
        need(Path(externs["nanoda_lib"]) == CHECKER, "COMPILE_CURRENT_CHECKER")
        linker = next(arg for arg in old if arg.startswith("linker="))
        common = [old[0], "--edition=2021", "--target", "x86_64-pc-windows-msvc",
            "-C", "overflow-checks=yes", "-C", "panic=unwind", "-C", "opt-level=2",
            "-C", "embed-bitcode=yes", "-C", linker, "-C", "link-arg=/DEBUG:NONE", *search,
            "-L", "dependency="+str(CHECKER.parent), "-L", "dependency="+str(run)]

        def argv(name, source, output, dependencies, test=False):
            command = [*common, "--crate-name", name]
            command.extend(["--test"] if test else ["--crate-type", "rlib" if output.endswith(".rlib") else "bin"])
            command.extend([str(snapshot/source), "-o", str(run/output)])
            for key, value in dependencies.items(): command.extend(["--extern", key+"="+str(value)])
            return command

        module = run/"libdmkn_module_relation.rlib"
        aggregate = run/"libdmkn_aggregate_relation.rlib"
        selected = [
            ("module-relation", argv("dmkn_module_relation", "software/v5/modules/receipt/src/lib.rs",
                module.name, externs)),
            ("aggregate-relation", argv("dmkn_aggregate_relation", "software/v5/aggregate/lib.rs",
                aggregate.name, {"dmkn_module_relation":module, "serde_json":externs["serde_json"]})),
            ("aggregate-tests", argv("dmkn_aggregate_relation_tests", "software/v5/aggregate/lib.rs",
                "aggregate_tests.exe", {"dmkn_module_relation":module, "serde_json":externs["serde_json"]}, True)),
            ("aggregate-driver", argv("native_aggregate", "software/v5/aggregate/native.rs",
                "native_aggregate.exe", {"dmkn_module_relation":module, "dmkn_aggregate_relation":aggregate,
                    "serde_json":externs["serde_json"]})),
        ]
        save(run/"compile-commands.json", selected)

        def exact_job(seconds, _memory, active_processes):
            need(seconds == 240 and active_processes == 8, "ADOPTED_PHASE_CALL_SHAPE")
            return run_stage.Job(240, 3072, active_processes=6)

        budget.refresh()
        phase = r.phase_class(p,a)("aggregate-compile",run,budget,env,exact_job,240)
        for label, command in selected: phase.invoke(label,command,ROOT,allow_build_telemetry=True)
        result.update(status="PASS_AGGREGATE_THIN_COMPILES_ONLY", outputs={name:a.pin(run/name)
            for name in (module.name, aggregate.name, "aggregate_tests.exe", "native_aggregate.exe")})
    except BaseException as error:
        result["error"] = type(error).__name__+": "+str(error)[:4000]
    finally:
        if phase is not None:
            try: phase.close()
            except BaseException as error: result.update(status="FAIL_CLEANUP", cleanup_error=str(error)[:2000])
            result["job"], result["commands"] = phase.final_stats, phase.commands
        try:
            check_inputs()
            need(json.loads((run/"selection.json").read_bytes()) == chosen, "SAVED_SELECTION_CHANGED")
            need(c.file_map(run/"source") == chosen["sources"], "BUILD_SNAPSHOT_CHANGED")
            budget.refresh()
        except BaseException as error: result.update(status="FAIL_FINAL_CHECK",final_error=str(error)[:3000])
        result.update(controller_cpu_seconds=time.process_time()-cpu, wall_seconds=time.monotonic()-started,
            output_census=budget.current, sampled_peaks=budget.peak,
            accounting="CONTROLLER_DISJOINT_FROM_INCLUSIVE_WORKER_JOB;FINAL_REPORT_EXIT_TAIL_EXCLUDED")
        save(run/"RESULT.json", result)
        save(attempt, {"status":result["status"],"result_sha256":sha(run/"RESULT.json")})
        try:
            # Final writes consume the original allocation too. Immutable PASS
            # reports are overridden explicitly rather than rewritten on failure.
            budget.refresh()
        except BaseException as error:
            result.update(status="FAIL_FINALIZATION",finalization_error=str(error)[:3000])
            save(run/"FINALIZATION-FAILED.json", {"status":"FAIL_FINALIZATION",
                "overrides_result_and_attempt":True,"result_sha256":sha(run/"RESULT.json"),
                "error":str(error)[:3000]})
    print(json.dumps({key:result.get(key) for key in ("status","error","wall_seconds")}))
    return 0 if result["status"] == "PASS_AGGREGATE_THIN_COMPILES_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
