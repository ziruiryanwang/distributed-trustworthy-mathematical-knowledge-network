"""Two thin native compiles for derived-support RC; never execute controls.

Reuse adopted compiler/dependencies and the original RC rlib as an explicit
differential alias. No old-core, aggregate, checker, guest or SDK rebuild.
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
SOURCE = ROOT / "software/v5/restricted_support"
BASE = HERE / "restricted-composition-build-02"
HELPER = ROOT / "software/v5/restricted_composition/build02.py"
HELPER_SHA = "0a7c986b1e012c8d5a0259373c77f9c902737f6122f743ddcd5c250eb86b510b"
BASE_RESULT_SHA = "24e8ebf8f774e22ec19c7172dca0a56efb81ad653e609445ae0e5d030e2233dd"
BASE_SELECTION_SHA = "659c780e902b69cfb039b854abae05d6a570c389f463dc8bfc6fff9bfa455244"
BASE_MAP_SHA = "32e95e4b67377ac2f8b6cf1b7087a006c675c15db98f954415ab996f7393ac04"
BASE_RLIB_SHA = "1bdfd6a0943b6a09248ae99aefd793b63384a957bf8d98c0cd8d8b430fd04a0b"
FRESH = {"software/v5/restricted_support/" + name for name in (
    "lib.rs", "syntax.rs", "typing.rs", "controls.rs", "controls_root.rs", "build.py")}
REUSED = {"software/v5/restricted_composition/" + name for name in ("relation.rs", "foundation02.rs")}
OUTPUTS = ("libdmkn_rc_relation.rlib", "restricted_support_controls.exe")
PASS = "PASS_RC_SUPPORT_TWO_COMPILES_ONLY"
MIB = 1024**2


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


def commands(b, retained, snapshot, run):
    need([row[0] for row in retained] == ["checker", "module-relation", "aggregate-relation", "aggregate-driver"],
         "EXACT_RETAINED_COMMAND_LABELS")
    base = list(dict(retained)["aggregate-relation"])
    need(base[base.index("--crate-name") + 1] == "dmkn_aggregate_relation"
         and base[base.index("--crate-type") + 1] == "rlib"
         and "dmkn_module_relation=" + str(b.PRIOR / "libdmkn_module_relation.rlib") in base,
         "EXACT_ADOPTED_MODULE_DEPENDENCY")
    selected = []
    for label, crate, source, output, kind in (
            ("support-core", "dmkn_rc_relation", "lib.rs", OUTPUTS[0], "rlib"),
            ("support-controls", "dmkn_rc_support_controls", "controls_root.rs", OUTPUTS[1], "bin")):
        command = list(base)
        command[command.index("--crate-name") + 1] = crate
        command[command.index("--crate-type") + 1] = kind
        b.replace_once(command, b.PRIOR / "source/software/v5/aggregate_claims/lib.rs",
                       snapshot / "software/v5/restricted_support" / source)
        b.replace_once(command, b.PRIOR / "libdmkn_aggregate_relation.rlib", run / output)
        command += ["-C", "metadata=dmkn_rc_support01_" + crate, "-L", "dependency=" + str(run)]
        if label == "support-controls":
            command += ["--extern", "dmkn_rc_relation=" + str(run / OUTPUTS[0]),
                        "--extern", "dmkn_rc_baseline=" + str(BASE / OUTPUTS[0]), "-C", "lto=fat"]
        need("--test" not in command and not any(arg.startswith("dmkn_aggregate_relation=") for arg in command),
             "TWO_COMPILES_NO_AGGREGATE_OR_AUTORUN")
        selected.append((label, command))
    return selected


def main():
    started, cpu = time.monotonic(), time.process_time()
    need(os.name == "nt" and Path.cwd() == ROOT and Path(__file__).resolve() == SOURCE / "build.py"
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize and len(sys.argv) == 3, "CANONICAL_ISOLATED_SUPPORT_BUILD")
    selection = Path(sys.argv[1]).resolve(strict=True)
    need(selection == HERE / "restricted-support-build-01-selection.json"
         and selection.stat().st_size <= 65536 and sha(selection) == sys.argv[2], "EXACT_SUPPORT_SELECTION")
    selection_raw = selection.read_bytes()
    need(hashlib.sha256(selection_raw).hexdigest() == sys.argv[2], "STABLE_SELECTION_READ")
    chosen = json.loads(selection_raw)
    need(set(chosen) == {"schema", "name", "authorizes_compile_only", "sources"}
         and chosen["schema"] == "DMKN_V5_RC_SUPPORT_BUILD_V1"
         and chosen["name"] == "restricted-support-build-01" and chosen["authorizes_compile_only"] is True
         and type(chosen["sources"]) is dict and set(chosen["sources"]) == FRESH | REUSED,
         "EXACT_EIGHT_SOURCE_BUILD_SELECTION")
    b = load("support_retained_build", HELPER, HELPER_SHA)
    h = b.load("support_build_helpers", b.SUPPORT, b.SUPPORT_SHA)
    old = h.load("support_prior_build", h.PREDECESSOR, h.PREDECESSOR_SHA)
    q = h.load("support_prior", old.PRIOR, old.PRIOR_SHA)
    a = h.load("support_artifacts", q.CRYPTO / "artifacts.py", q.HELPERS["artifacts.py"])
    p = h.load("support_provision", q.CRYPTO / "provision_build.py", q.HELPERS["provision_build.py"])
    c = h.load("support_census", q.CRYPTO / "continue_build03.py", q.HELPERS["continue_build03.py"])
    r = h.load("support_phase", ROOT / "experiments/scale-equation-01/runtime.py", q.RUNTIME_SHA)
    p.a, c.a, c.p, c.HERE = a, a, p, HERE
    r.LOG_LIMIT = MIB
    need(Path(sys.executable).resolve() == p.PYTHON and sha(p.PYTHON) == p.PYTHON_SHA
         and sha(p.PYTHON.parent / "python314.dll") == p.PYTHON_DLL_SHA, "PINNED_PYTHON")
    need(sha(p.HELPERS / "run_stage.py") == p.HELPER_SHA
         and sha(p.HELPERS / "domains.py") == p.DOMAINS_SHA, "PINNED_JOB_HELPERS")
    sys.path.insert(0, str(p.HELPERS))
    import run_stage
    import domains
    need(Path(run_stage.__file__).resolve() == p.HELPERS / "run_stage.py"
         and Path(domains.__file__).resolve() == p.HELPERS / "domains.py", "JOB_HELPER_ORIGIN")
    c.h = run_stage
    fixed = {HELPER:HELPER_SHA, BASE / "RESULT.json":BASE_RESULT_SHA,
        HERE / "restricted-composition-build-02-selection.json":BASE_SELECTION_SHA,
        BASE / "source-map.json":BASE_MAP_SHA, BASE / OUTPUTS[0]:BASE_RLIB_SHA,
        b.SUPPORT:b.SUPPORT_SHA, h.PREDECESSOR:h.PREDECESSOR_SHA,
        old.PRIOR:old.PRIOR_SHA, old.RECIPE:old.RECIPE_SHA,
        ROOT / "experiments/scale-equation-01/runtime.py":q.RUNTIME_SHA,
        p.HELPERS / "run_stage.py":p.HELPER_SHA, p.HELPERS / "domains.py":p.DOMAINS_SHA,
        p.PYTHON:p.PYTHON_SHA, p.PYTHON.parent / "python314.dll":p.PYTHON_DLL_SHA}
    fixed.update({b.PRIOR / name:digest for name,digest in b.RECORDS.items()})
    for path, digest in fixed.items():
        need(sha(path) == digest, "ADOPTED_RECORD:" + str(path))
    baseline = json.loads((BASE / "RESULT.json").read_bytes())
    prior = json.loads((b.PRIOR / "RESULT.json").read_bytes())
    baseline_map = json.loads((BASE / "source-map.json").read_bytes())
    baseline_selection = json.loads((HERE / "restricted-composition-build-02-selection.json").read_bytes())
    need(baseline["schema"] == "DMKN_V5_RC_NATIVE_BUILD_RESULT_V1"
         and baseline["status"] == "PASS_RC_THREE_COMPILES_ONLY"
         and baseline["selection_sha256"] == BASE_SELECTION_SHA
         and baseline_selection["sources"] == baseline_map
         and baseline["outputs"][OUTPUTS[0]] == {"path":str(BASE / OUTPUTS[0]),
              "bytes":1719004, "sha256":BASE_RLIB_SHA}
         and baseline["job"]["active_processes"] == baseline["job"]["terminated_processes"] == 0
         and prior["status"] == "PASS_PROOF_VALIDATION_FOUR_COMPILES_ONLY", "ADOPTED_BASELINE_AND_MODULE")
    for relative in REUSED:
        need(chosen["sources"][relative] == baseline_map[relative], "FROZEN_SEMANTIC_SOURCE:" + relative)
    recipe = json.loads(old.RECIPE.read_bytes())
    run = HERE / chosen["name"]
    attempt = HERE / (chosen["name"] + "-attempt.json")

    def check_inputs():
        need(time.monotonic() - started <= 360 and time.process_time() - cpu <= 30, "CONTROLLER_ENVELOPE")
        for path, digest in {**fixed, selection:sys.argv[2]}.items():
            need(sha(path) == digest, "INPUT_CHANGED:" + str(path))
        for directory, status, result_sha in ((BASE, baseline["status"], BASE_RESULT_SHA),
                (b.PRIOR, prior["status"], b.RECORDS["RESULT.json"])):
            need(not (directory / "FINALIZATION-FAILED.json").exists()
                 and json.loads((HERE / (directory.name + "-attempt.json")).read_bytes()) ==
                 {"status":status, "result_sha256":result_sha}, "RETAINED_FINALIZATION")
        for relative, pin in chosen["sources"].items():
            need(set(pin) == {"bytes", "sha256"} and (ROOT / relative).stat().st_size == pin["bytes"]
                 and sha(ROOT / relative) == pin["sha256"], "SOURCE_PIN:" + relative)
        for name, digest in recipe["runtime_pins_rechecked"].items():
            need(sha(Path(name)) == digest, "RUNTIME_PIN:" + name)
        for name, digest in q.HELPERS.items():
            need(sha(q.CRYPTO / name) == digest, "HELPER_PIN:" + name)

    check_inputs()
    need(not run.exists() and not attempt.exists() and not run.is_symlink()
         and not run.is_junction() and not attempt.is_symlink(), "FRESH_SUPPORT_BUILD")
    run.mkdir(); (run / "commands").mkdir()
    with (run / "selection.json").open("xb") as stream:
        need(stream.write(selection_raw) == len(selection_raw), "EXACT_SELECTION_COPY")
    phase = None
    result = {"schema":"DMKN_V5_RC_SUPPORT_BUILD_RESULT_V1", "status":"FAIL",
        "selection_sha256":sys.argv[2], "baseline_result_sha256":BASE_RESULT_SHA,
        "baseline_library":baseline["outputs"][OUTPUTS[0]], "source_files":8,
        "checker_rebuilds":0, "module_rebuilds":0, "dependency_rebuilds":0,
        "baseline_rebuilds":0, "aggregate_rebuilds":0, "test_calls":0,
        "native_calls":0, "guest_calls":0, "proof_calls":0, "network_calls":0,
        "authority":"TWO_COMPILES_ONLY_NOT_ADMISSION"}

    class Budget:
        def __init__(self):
            self.peak, self.current = {"working_bytes":0, "entries":0}, {}
        def refresh(self):
            need(time.monotonic()-started <= 360 and time.process_time()-cpu <= 30, "TOTAL_BUILD_ENVELOPE")
            self.current = c.census(run)
            need(self.current["working_bytes"] <= 128*MIB and self.current["entries"] <= 1024, "FRESH_OUTPUT_ENVELOPE")
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
            need(target.stat().st_size == pin["bytes"] and sha(target) == pin["sha256"], "EXACT_SOURCE_SNAPSHOT")
        h.save(run / "source-map.json", chosen["sources"])
        selected = commands(b, json.loads((b.PRIOR / "compile-commands.json").read_bytes()), snapshot, run)
        h.save(run / "compile-commands.json", selected)
        env, environment = p.environment(run, c.OLD / "rust")
        env["VCToolsUserTelemetryOptOut"] = "1"
        environment["environment_keys_only"] = sorted(env)
        h.save(run / "environment-profile.json", environment)

        def exact_job(seconds, _memory, active_processes):
            need(seconds == 240 and active_processes == 8, "RETAINED_PHASE_CALL_SHAPE")
            return run_stage.Job(180, 1024, active_processes=6)

        budget.refresh()
        phase = r.phase_class(p, a)("rc-support-native", run, budget, env, exact_job, 240)
        for label, command in selected:
            phase.invoke(label, command, ROOT, allow_build_telemetry=True)
        result.update(status=PASS, outputs={name:a.pin(run / name) for name in OUTPUTS})
    except BaseException as error:
        result["error"] = type(error).__name__ + ": " + str(error)[:4000]
    finally:
        if phase is not None:
            try:
                phase.close()
            except BaseException as error:
                result.update(status="FAIL_CLEANUP", cleanup_error=str(error)[:2000])
            result["job"], result["commands"] = phase.final_stats, phase.commands
        result["compiler_calls"] = len(result.get("commands", []))
        try:
            check_inputs()
            need(sha(run / "selection.json") == sys.argv[2], "EXACT_SAVED_SELECTION_BYTES")
            need(c.file_map(run / "source") == chosen["sources"], "SOURCE_SNAPSHOT_CHANGED")
            budget.refresh()
        except BaseException as error:
            result.update(status="FAIL_FINAL_CHECK", final_error=str(error)[:3000])
        result.update(controller_cpu_seconds=time.process_time()-cpu, wall_seconds=time.monotonic()-started,
            output_census=budget.current, sampled_peaks=budget.peak,
            accounting="DISJOINT_CONTROLLER_AND_INCLUSIVE_WORKER_JOB;FINAL_REPORT_EXIT_TAIL_EXCLUDED")
        h.save(run / "RESULT.json", result)
        h.save(attempt, {"status":result["status"], "result_sha256":sha(run / "RESULT.json")})
        try:
            budget.refresh()
        except BaseException as error:
            result.update(status="FAIL_FINALIZATION", finalization_error=str(error)[:3000])
            h.save(run / "FINALIZATION-FAILED.json", {"status":"FAIL_FINALIZATION", "overrides_result_and_attempt":True,
                "result_sha256":sha(run / "RESULT.json"), "error":str(error)[:3000]})
    print(json.dumps({key:result.get(key) for key in ("status", "error", "wall_seconds")}))
    return 0 if result["status"] == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
