"""Three thin native compiles for RC0; no dependency rebuild or execution.

Uses retained original relation/checker libraries only as explicit dependencies.
The RC path never invokes them; the separate controls binary will compare W.
Root must review/select a fresh bounded invocation before this entry is run.
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
SOURCE = ROOT / "software/v5/restricted_composition"
SUPPORT = ROOT / "software/v5/modules/native/proof_validation/control.py"
SUPPORT_SHA = "91e25c3a3244a106c01ce18da63b07a163b0d07e53eddcf5376b399ee22a9ca1"
PRIOR = HERE / "proof-validation-integration-build-01"
RECORDS = {
    "compile-commands.json": "b779d874b2b766730b8854dae6fe8fa70ed609cbc8d8392307819123f9d52f7d",
    "source-map.json": "a5693f19236bb8051e476d9f61d8d2449cbcd023054a1e9c8606607049957f2a",
    "RESULT.json": "55ba9a702360dd10a6b9bea00f481d5066553a1b8debcb10ca43bbcab4de4069",
    "libnanoda_lib.rlib": "c0c0b10ba18adf5c20496d751cc9cbbc911677fafe64461d963dadc53a37c4a2",
    "libdmkn_module_relation.rlib": "10efaf57720635b0c347487194283117599ecb3be326b4c51b3c9dbcc144a4bf",
}
FRESH = {"software/v5/restricted_composition/" + name for name in (
    "lib02.rs", "syntax.rs", "foundation02.rs", "typing.rs", "relation.rs", "census.rs",
    "wire.rs", "aggregate_relation.rs", "aggregate_lib.rs", "controls.rs", "controls_root02.rs",
    "build02.py", "fixtures.py")}
REUSED = {"software/v5/aggregate_claims/" + name for name in ("header.rs", "membership.rs")}
OUTPUTS = ("libdmkn_rc_relation.rlib", "libdmkn_aggregate_relation.rlib", "restricted_controls.exe")


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


def replace_once(command, before, after):
    need(command.count(str(before)) == 1, "EXACT_RECIPE_REPLACEMENT:" + str(before))
    command[command.index(str(before))] = str(after)


def commands(retained, snapshot, run):
    need([row[0] for row in retained] == ["checker", "module-relation", "aggregate-relation", "aggregate-driver"],
         "EXACT_RETAINED_COMMAND_LABELS")
    base = list(dict(retained)["aggregate-relation"])
    need(base[base.index("--crate-name") + 1] == "dmkn_aggregate_relation"
         and base[base.index("--crate-type") + 1] == "rlib"
         and "dmkn_module_relation=" + str(PRIOR / "libdmkn_module_relation.rlib") in base,
         "EXACT_AGGREGATE_RECIPE")
    selected = []
    for label, crate, source, output, kind in (
            ("rc-core", "dmkn_rc_relation", "lib02.rs", OUTPUTS[0], "rlib"),
            ("rc-aggregate", "dmkn_aggregate_relation", "aggregate_lib.rs", OUTPUTS[1], "rlib"),
            ("rc-controls", "dmkn_rc_controls", "controls_root02.rs", OUTPUTS[2], "bin")):
        command = list(base)
        command[command.index("--crate-name") + 1] = crate
        command[command.index("--crate-type") + 1] = kind
        replace_once(command, PRIOR / "source/software/v5/aggregate_claims/lib.rs",
                     snapshot / "software/v5/restricted_composition" / source)
        replace_once(command, PRIOR / "libdmkn_aggregate_relation.rlib", run / output)
        command += ["-C", "metadata=dmkn_rc02_" + crate, "-L", "dependency=" + str(run)]
        if label != "rc-core":
            command += ["--extern", "dmkn_rc_relation=" + str(run / OUTPUTS[0])]
        if label == "rc-controls":
            command += ["--extern", "dmkn_aggregate_relation=" + str(run / OUTPUTS[1]), "-C", "lto=fat"]
        need("--test" not in command, "CONTROL_IS_EXPLICIT_BINARY_NOT_AUTORUN")
        selected.append((label, command))
    return selected


def main():
    started, cpu = time.monotonic(), time.process_time()
    need(os.name == "nt" and Path.cwd() == ROOT and Path(__file__).resolve() == SOURCE / "build02.py"
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize and len(sys.argv) == 3, "ISOLATED_CANONICAL_RC_BUILD")
    selection = Path(sys.argv[1]).resolve(strict=True)
    need(selection.is_relative_to(HERE) and selection.stat().st_size <= 65536
         and sha(selection) == sys.argv[2], "EXACT_BUILD_SELECTION")
    chosen = json.loads(selection.read_bytes())
    need(set(chosen) == {"schema", "name", "authorizes_compile_only", "sources"}
         and chosen["schema"] == "DMKN_V5_RC_NATIVE_BUILD_V1"
         and chosen["name"] == "restricted-composition-build-02"
         and chosen["authorizes_compile_only"] is True, "SELECTION_FIELDS")
    need(type(chosen["sources"]) is dict and set(chosen["sources"]) == FRESH | REUSED, "EXACT_SOURCES")
    h = load("rc_build_support", SUPPORT, SUPPORT_SHA)
    old = h.load("rc_prior_build", h.PREDECESSOR, h.PREDECESSOR_SHA)
    q = h.load("rc_prior", old.PRIOR, old.PRIOR_SHA)
    a = h.load("rc_artifacts", q.CRYPTO / "artifacts.py", q.HELPERS["artifacts.py"])
    p = h.load("rc_provision", q.CRYPTO / "provision_build.py", q.HELPERS["provision_build.py"])
    c = h.load("rc_census", q.CRYPTO / "continue_build03.py", q.HELPERS["continue_build03.py"])
    r = h.load("rc_phase", ROOT / "experiments/scale-equation-01/runtime.py", q.RUNTIME_SHA)
    p.a, c.a, c.p, c.HERE = a, a, p, HERE
    r.LOG_LIMIT = 1048576
    need(Path(sys.executable).resolve() == p.PYTHON and sha(p.PYTHON) == p.PYTHON_SHA
         and sha(p.PYTHON.parent / "python314.dll") == p.PYTHON_DLL_SHA, "PINNED_PYTHON")
    need(sha(p.HELPERS / "run_stage.py") == p.HELPER_SHA
         and sha(p.HELPERS / "domains.py") == p.DOMAINS_SHA, "PINNED_JOB_HELPERS")
    sys.path.insert(0, str(p.HELPERS))
    import run_stage
    import domains
    need(Path(run_stage.__file__).resolve() == p.HELPERS / "run_stage.py"
         and Path(domains.__file__).resolve() == p.HELPERS / "domains.py", "JOB_ORIGIN")
    c.h = run_stage
    for name, digest in RECORDS.items():
        need(sha(PRIOR / name) == digest, "RETAINED_RECORD:" + name)
    need(sha(old.RECIPE) == old.RECIPE_SHA, "RETAINED_RUNTIME_RECIPE")
    recipe = json.loads(old.RECIPE.read_bytes())
    prior_map = json.loads((PRIOR / "source-map.json").read_bytes())
    prior_result = json.loads((PRIOR / "RESULT.json").read_bytes())
    need(prior_result["status"] == "PASS_PROOF_VALIDATION_FOUR_COMPILES_ONLY"
         and not (PRIOR / "FINALIZATION-FAILED.json").exists(), "RETAINED_CHECKER_BUILD")
    for relative in REUSED:
        need(chosen["sources"][relative] == prior_map[relative], "UNCHANGED_SHARED_SOURCE:" + relative)
    run = HERE / chosen["name"]
    attempt = HERE / (chosen["name"] + "-attempt.json")

    def check_inputs():
        need(time.monotonic() - started <= 360 and time.process_time() - cpu <= 30, "CONTROLLER_ENVELOPE")
        for path, digest in [(selection, sys.argv[2]), (SUPPORT, SUPPORT_SHA),
                (h.PREDECESSOR, h.PREDECESSOR_SHA), (old.PRIOR, old.PRIOR_SHA), (old.RECIPE, old.RECIPE_SHA),
                (ROOT / "experiments/scale-equation-01/runtime.py", q.RUNTIME_SHA),
                (p.HELPERS / "run_stage.py", p.HELPER_SHA), (p.HELPERS / "domains.py", p.DOMAINS_SHA),
                (p.PYTHON, p.PYTHON_SHA), (p.PYTHON.parent / "python314.dll", p.PYTHON_DLL_SHA)]:
            need(sha(path) == digest, "PIN_CHANGED:" + str(path))
        for name, digest in RECORDS.items():
            need(sha(PRIOR / name) == digest, "RETAINED_RECORD_CHANGED:" + name)
        need(not (PRIOR / "FINALIZATION-FAILED.json").exists()
             and json.loads((HERE / (PRIOR.name + "-attempt.json")).read_bytes()) == {
                 "status": prior_result["status"], "result_sha256": RECORDS["RESULT.json"]},
             "RETAINED_BUILD_FINALIZATION")
        for relative, pin in chosen["sources"].items():
            need(set(pin) == {"bytes", "sha256"} and (ROOT / relative).stat().st_size == pin["bytes"]
                 and sha(ROOT / relative) == pin["sha256"], "SOURCE_PIN:" + relative)
        for name, digest in recipe["runtime_pins_rechecked"].items():
            need(sha(Path(name)) == digest, "RUNTIME_PIN:" + name)
        for name, digest in q.HELPERS.items():
            need(sha(q.CRYPTO / name) == digest, "HELPER_CHANGED:" + name)

    check_inputs()
    need(not run.exists() and not attempt.exists(), "FRESH_BUILD")
    run.mkdir()
    (run / "commands").mkdir()
    h.save(run / "selection.json", chosen)
    phase = None
    result = {"schema": "DMKN_V5_RC_NATIVE_BUILD_RESULT_V1", "status": "FAIL",
        "selection_sha256": sys.argv[2], "checker_rebuilds": 0, "module_rebuilds": 0,
        "dependency_rebuilds": 0, "test_calls": 0, "native_calls": 0, "guest_calls": 0,
        "proof_calls": 0, "network_calls": 0, "authority": "COMPILE_ONLY_NOT_ADMISSION"}

    class Budget:
        def __init__(self):
            self.peak = {"working_bytes": 0, "entries": 0}
            self.current = {}
        def refresh(self):
            need(time.monotonic() - started <= 360 and time.process_time() - cpu <= 30, "BUILD_TOTAL_ENVELOPE")
            self.current = c.census(run)
            need(self.current["working_bytes"] <= 512 * 1024**2 and self.current["entries"] <= 2048,
                 "OUTPUT_ENVELOPE")
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
            need(target.stat().st_size == pin["bytes"] and sha(target) == pin["sha256"], "SNAPSHOT_PIN")
        h.save(run / "source-map.json", chosen["sources"])
        selected = commands(json.loads((PRIOR / "compile-commands.json").read_bytes()), snapshot, run)
        h.save(run / "compile-commands.json", selected)
        env, environment = p.environment(run, c.OLD / "rust")
        env["VCToolsUserTelemetryOptOut"] = "1"
        environment["environment_keys_only"] = sorted(env)
        h.save(run / "environment-profile.json", environment)

        def exact_job(seconds, _memory, active_processes):
            need(seconds == 240 and active_processes == 8, "PHASE_CALL_SHAPE")
            return run_stage.Job(180, 1024, active_processes=6)

        budget.refresh()
        phase = r.phase_class(p, a)("rc-native-compile", run, budget, env, exact_job, 240)
        for label, command in selected:
            phase.invoke(label, command, ROOT, allow_build_telemetry=True)
        result.update(status="PASS_RC_THREE_COMPILES_ONLY", outputs={name: a.pin(run / name) for name in OUTPUTS})
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
            need(json.loads((run / "selection.json").read_bytes()) == chosen, "SAVED_SELECTION_CHANGED")
            need(c.file_map(run / "source") == chosen["sources"], "SNAPSHOT_CHANGED")
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
    return 0 if result["status"] == "PASS_RC_THREE_COMPILES_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
