"""Finish only two links after the preserved cfg(test) packaging failure.

Reuse three successful rlibs. No successful compilation or test is repeated.
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
SOURCE = ROOT / "software/v5/bounded_parse"
SUPPORT = ROOT / "software/v5/modules/native/proof_validation/control.py"
SUPPORT_SHA = "91e25c3a3244a106c01ce18da63b07a163b0d07e53eddcf5376b399ee22a9ca1"
PRIOR = HERE / "proof-validation-integration-build-01"
FAILED = HERE / "bounded-parse-native-build-01"
FAILED_RECORDS = {
    "RESULT.json": "4780ae9f43aca7dea221c6f32ede060ea0ab96d42e9750830606f0fff9bd9695",
    "source-map.json": "2d2e9bcc29c19d84fe8530434eee5f35e937194f3f8e4ab50821092378695c42",
    "compile-commands.json": "5a5e7bef3468bc719797e8f08e9326a36b131ea0b6313d019dbf2d66a1df3a94",
    "libnanoda_lib.rlib": "c0c0b10ba18adf5c20496d751cc9cbbc911677fafe64461d963dadc53a37c4a2",
    "libdmkn_module_relation.rlib": "a20dfa506e70b5d781d8dbb087b151702be019c338c29f6654ebbe2a1b13315f",
    "libdmkn_aggregate_relation.rlib": "0d90f603ffdc21c76fbdc2262380d18daa46d66152c5fa5d6bb4ece4c7f99830",
}
RECORDS = {
    "compile-commands.json": "b779d874b2b766730b8854dae6fe8fa70ed609cbc8d8392307819123f9d52f7d",
    "source-map.json": "a5693f19236bb8051e476d9f61d8d2449cbcd023054a1e9c8606607049957f2a",
    "RESULT.json": "55ba9a702360dd10a6b9bea00f481d5066553a1b8debcb10ca43bbcab4de4069",
    "libnanoda_lib.rlib": "c0c0b10ba18adf5c20496d751cc9cbbc911677fafe64461d963dadc53a37c4a2",
}
FRESH = {"software/v5/bounded_parse/" + name for name in (
    "canonical.rs", "module_relation.rs", "module_lib.rs", "census.rs",
    "aggregate_relation.rs", "aggregate_lib.rs", "controls.rs", "build.py",
    "controls_root.rs", "build_remaining.py")}
REUSED = {"software/v5/modules/receipt/src/" + name + ".rs" for name in (
    "input", "foundation_static", "foundation_data", "commitments", "journal", "policy")}
REUSED.update({"software/v5/aggregate_claims/" + name + ".rs" for name in ("header", "membership", "wire")})
REUSED.update(("software/v5/aggregate_parse_once/census.rs", "software/v5/aggregate/native.rs"))
OUTPUTS = ("libnanoda_lib.rlib", "libdmkn_module_relation.rlib",
           "libdmkn_aggregate_relation.rlib", "aggregate_tests.exe", "native_aggregate.exe")


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


def main():
    started, cpu = time.monotonic(), time.process_time()
    need(os.name == "nt" and Path.cwd() == ROOT and Path(__file__).resolve() == SOURCE / "build_remaining.py"
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize and len(sys.argv) == 3, "ISOLATED_CANONICAL_BUILD")
    selection = Path(sys.argv[1]).resolve(strict=True)
    need(selection.is_relative_to(HERE) and selection.stat().st_size <= 65536
         and sha(selection) == sys.argv[2], "EXACT_BUILD_SELECTION")
    chosen = json.loads(selection.read_bytes())
    need(set(chosen) == {"schema", "name", "authorizes_compile_only", "sources"}
         and chosen["schema"] == "DMKN_V5_BOUNDED_PARSE_REMAINING_BUILD_V1"
         and chosen["authorizes_compile_only"] is True and type(chosen["name"]) is str
         and chosen["name"] == "bounded-parse-native-build-02", "SELECTION_FIELDS")
    need(type(chosen["sources"]) is dict and set(chosen["sources"]) == FRESH | REUSED, "EXACT_SOURCES")
    h = load("bounded_build_support", SUPPORT, SUPPORT_SHA)
    old = h.load("bounded_prior_build", h.PREDECESSOR, h.PREDECESSOR_SHA)
    q = h.load("bounded_prior", old.PRIOR, old.PRIOR_SHA)
    a = h.load("bounded_artifacts", q.CRYPTO / "artifacts.py", q.HELPERS["artifacts.py"])
    p = h.load("bounded_provision", q.CRYPTO / "provision_build.py", q.HELPERS["provision_build.py"])
    c = h.load("bounded_census", q.CRYPTO / "continue_build03.py", q.HELPERS["continue_build03.py"])
    r = h.load("bounded_phase", ROOT / "experiments/scale-equation-01/runtime.py", q.RUNTIME_SHA)
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
        need(chosen["sources"][relative] == prior_map[relative], "UNCHANGED_REUSED_SOURCE:" + relative)
    for name, digest in FAILED_RECORDS.items():
        need(sha(FAILED / name) == digest, "FAILED_OPERATION_PIN:" + name)
    failed_result = json.loads((FAILED / "RESULT.json").read_bytes())
    need(failed_result["status"] == "FAIL"
         and [row["label"] for row in failed_result["commands"]] ==
             ["module-relation", "aggregate-relation", "aggregate-tests"]
         and [row["exit_code"] for row in failed_result["commands"]] == [0, 0, 1]
         and failed_result["job"]["active_processes"] == 0
         and failed_result["job"]["cpu_seconds"] == 17.234375
         and failed_result["controller_cpu_seconds"] == 2.03125, "RETAINED_FAILURE_AND_SPEND")
    failed_map = json.loads((FAILED / "source-map.json").read_bytes())
    need(set(failed_map) == (FRESH | REUSED) - {
        "software/v5/bounded_parse/controls_root.rs", "software/v5/bounded_parse/build_remaining.py"},
        "EXACT_UNCHANGED_NINETEEN_SOURCES")
    for relative, pin in failed_map.items():
        need(chosen["sources"][relative] == pin, "UNCHANGED_USED_SOURCE:" + relative)
    run = HERE / chosen["name"]
    attempt = HERE / (chosen["name"] + "-attempt.json")

    def check_inputs():
        need(time.monotonic() - started <= 330 and time.process_time() - cpu <= 25, "CONTROLLER_ENVELOPE")
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
        for name, digest in FAILED_RECORDS.items():
            need(sha(FAILED / name) == digest, "FAILED_OPERATION_CHANGED:" + name)
        need(not (FAILED / "FINALIZATION-FAILED.json").exists()
             and json.loads((HERE / (FAILED.name + "-attempt.json")).read_bytes()) == {
                 "status": "FAIL", "result_sha256": FAILED_RECORDS["RESULT.json"]},
             "PRESERVED_FAILURE_FINALIZATION")
        need(c.file_map(FAILED / "source") == failed_map, "ORIGINAL_SNAPSHOT_CHANGED")
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
    result = {"schema": "DMKN_V5_BOUNDED_PARSE_REMAINING_BUILD_RESULT_V1", "status": "FAIL",
        "selection_sha256": sys.argv[2], "checker_rebuilds": 0, "dependency_rebuilds": 0,
        "test_calls": 0, "native_calls": 0, "guest_calls": 0, "proof_calls": 0,
        "network_calls": 0, "authority": "TWO_REMAINING_LINKS_ONLY_NOT_ADMISSION",
        "carried_failure": {"result_sha256": FAILED_RECORDS["RESULT.json"],
            "worker_cpu_seconds": 17.234375, "controller_cpu_seconds": 2.03125},
        "production_rlib_rebuilds": 0}

    class Budget:
        def __init__(self):
            self.peak = {"working_bytes": 0, "entries": 0}
            self.current = {}
        def refresh(self):
            need(time.monotonic() - started <= 330 and time.process_time() - cpu <= 25, "BUILD_TOTAL_ENVELOPE")
            self.current = c.census(run)
            need(self.current["working_bytes"] + c.census(FAILED)["working_bytes"] <= 1024**3
                 and self.current["entries"] <= 4096, "COMBINED_OUTPUT_ENVELOPE")
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
        for name in OUTPUTS[:3]:
            with (run / name).open("xb") as stream:
                stream.write((FAILED / name).read_bytes())
            need(sha(run / name) == FAILED_RECORDS[name], "REUSED_RLIB_COPY:" + name)
        retained = json.loads((FAILED / "compile-commands.json").read_bytes())
        need([row[0] for row in retained] ==
             ["module-relation", "aggregate-relation", "aggregate-tests", "aggregate-driver"],
             "EXACT_FAILED_COMMAND_LABELS")
        selected = []
        for label in ("aggregate-tests", "aggregate-driver"):
            original = list(dict(retained)[label])
            command = [arg.replace(str(FAILED), str(run)) for arg in original]
            need(not any(str(FAILED) in arg for arg in command), "NO_OLD_PROJECT_LINK")
            if label == "aggregate-tests":
                replace_once(command, snapshot / "software/v5/bounded_parse/aggregate_lib.rs",
                             snapshot / "software/v5/bounded_parse/controls_root.rs")
                replace_once(command, "dmkn_aggregate_relation", "dmkn_bounded_parse_controls")
                command += ["--extern", "dmkn_aggregate_relation=" + str(run / "libdmkn_aggregate_relation.rlib")]
            need("lto=fat" in command, "RETAINED_BINARY_FAT_LTO")
            selected.append((label, command))
        h.save(run / "compile-commands.json", selected)
        env, environment = p.environment(run, c.OLD / "rust")
        env["VCToolsUserTelemetryOptOut"] = "1"
        environment["environment_keys_only"] = sorted(env)
        h.save(run / "environment-profile.json", environment)

        def exact_job(seconds, _memory, active_processes):
            need(seconds == 210 and active_processes == 8, "PHASE_CALL_SHAPE")
            return run_stage.Job(150, 3072, active_processes=6)

        budget.refresh()
        phase = r.phase_class(p, a)("bounded-parse-remaining-links", run, budget, env, exact_job, 210)
        for label, command in selected:
            phase.invoke(label, command, ROOT, allow_build_telemetry=True)
        result.update(status="PASS_BOUNDED_PARSE_TWO_REMAINING_LINKS_ONLY",
                      outputs={name: a.pin(run / name) for name in OUTPUTS})
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
            for name in OUTPUTS[:3]:
                need(sha(run / name) == FAILED_RECORDS[name], "REUSED_RLIB_CHANGED:" + name)
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
    return 0 if result["status"] == "PASS_BOUNDED_PARSE_TWO_REMAINING_LINKS_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
