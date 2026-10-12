"""One serde-only compile and twelve private syntax groups; root selection only.

Borrow the retained compiler recipe and bounded Job supervisor. No native
checker/module rebuild, kernel checking, guest, proof, receipt or network call.
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
HERE = ROOT/"experiments/v5-local-checks"
SOURCE = ROOT/"software/v5/modules/native/proof_validation"
PREDECESSOR = ROOT/"software/v5/aggregate/build_native.py"
PREDECESSOR_SHA = "4b77bad55119746df2e66cf7b8336b62ee1db8bfa4dca7152b6c1512b4ad892a"
COMMANDS = HERE/"aggregate-native-build-01/compile-commands.json"
COMMANDS_SHA = "1f80c02b5049dbb5bdb22fea28ff52d8def582871b27366dd1cd98a73be5e232"
FRESH = ("module_correspondence.rs", "correspondence_controls.rs", "control_root.rs", "control.py")
TESTS = {
    "all_expression_constructors_references_and_shared_children_match",
    "zero_and_all_level_constructors_match",
    "constants_validate_levels_before_reference_and_charge_failed_prefix",
    "projection_reference_then_index_then_child_order_matches",
    "sibling_failures_preserve_left_to_right_evaluation",
    "binder_styles_zero_name_and_nondependent_checks_match",
    "malformed_tags_shapes_indices_and_level_backreferences_match",
    "identical_reference_subroutine_keeps_owner_and_foundation_refusals",
    "work_and_depth_limits_preserve_entry_and_failed_child_charge",
    "consecutive_proofs_retain_shared_cumulative_work_state",
    "complete_inventory_is_checked_before_reachable_proof_syntax",
    "theorem_call_and_imported_early_return_remain_structural_only",
}


def need(value, reason):
    if not value: raise ValueError(reason)


def sha(path):
    with path.open("rb") as stream: return hashlib.file_digest(stream,"sha256").hexdigest()


def save(path, value):
    with path.open("xb") as stream:
        stream.write((json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+"\n").encode())


def load(name, path, digest):
    need(sha(path) == digest,"HELPER_PIN:"+str(path))
    spec = importlib.util.spec_from_file_location(name,path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def main():
    started,cpu = time.monotonic(),time.process_time()
    need(os.name == "nt" and Path.cwd() == ROOT and Path(__file__).resolve() == SOURCE/"control.py"
        and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
        and not sys.flags.optimize and len(sys.argv) == 3,"ISOLATED_CANONICAL_PROOF_SYNTAX_CONTROL")
    selection = Path(sys.argv[1]).resolve(strict=True)
    need(selection.is_relative_to(HERE) and selection.stat().st_size <= 65536
        and sha(selection) == sys.argv[2],"EXACT_SYNTAX_SELECTION")
    chosen = json.loads(selection.read_bytes())
    need(set(chosen) == {"schema","name","authorizes_serde_compile_and_syntax_tests","sources"}
        and chosen["schema"] == "DMKN_V5_PROOF_VALIDATION_CONTROLS_V1"
        and chosen["authorizes_serde_compile_and_syntax_tests"] is True
        and type(chosen["name"]) is str and re.fullmatch(r"proof-validation-controls-[0-9]{2}",chosen["name"]),
        "SYNTAX_SELECTION_FIELDS")
    expected = {"software/v5/modules/native/proof_validation/"+name for name in FRESH}
    need(type(chosen["sources"]) is dict and set(chosen["sources"]) == expected,"EXACT_FOUR_SOURCES")
    old = load("proof_syntax_prior_build",PREDECESSOR,PREDECESSOR_SHA)
    q = load("proof_syntax_prior",old.PRIOR,old.PRIOR_SHA)
    a = load("proof_syntax_artifacts",q.CRYPTO/"artifacts.py",q.HELPERS["artifacts.py"])
    p = load("proof_syntax_provision",q.CRYPTO/"provision_build.py",q.HELPERS["provision_build.py"])
    c = load("proof_syntax_census",q.CRYPTO/"continue_build03.py",q.HELPERS["continue_build03.py"])
    r = load("proof_syntax_phase",ROOT/"experiments/scale-equation-01/runtime.py",q.RUNTIME_SHA)
    p.a,c.a,c.p,c.HERE = a,a,p,HERE; r.LOG_LIMIT = 1048576
    need(Path(sys.executable).resolve() == p.PYTHON and sha(p.PYTHON) == p.PYTHON_SHA
        and sha(p.PYTHON.parent/"python314.dll") == p.PYTHON_DLL_SHA,"PINNED_PYTHON")
    need(sha(p.HELPERS/"run_stage.py") == p.HELPER_SHA and sha(p.HELPERS/"domains.py") == p.DOMAINS_SHA,
        "PINNED_JOB_HELPERS")
    sys.path.insert(0,str(p.HELPERS))
    import run_stage
    import domains
    need(Path(run_stage.__file__).resolve() == p.HELPERS/"run_stage.py"
        and Path(domains.__file__).resolve() == p.HELPERS/"domains.py","JOB_ORIGIN")
    c.h = run_stage
    need(sha(old.RECIPE) == old.RECIPE_SHA and sha(COMMANDS) == COMMANDS_SHA,"RETAINED_COMPILER_RECIPE")
    recipe = json.loads(old.RECIPE.read_bytes())
    run = HERE/chosen["name"]; attempt = HERE/(chosen["name"]+"-attempt.json")

    def check_inputs():
        need(time.monotonic()-started <= 300 and time.process_time()-cpu <= 60,"SYNTAX_CONTROLLER_ENVELOPE")
        need(sha(selection) == sys.argv[2] and sha(PREDECESSOR) == PREDECESSOR_SHA
            and sha(old.PRIOR) == old.PRIOR_SHA and sha(old.RECIPE) == old.RECIPE_SHA
            and sha(COMMANDS) == COMMANDS_SHA,"RETAINED_PINS_CHANGED")
        for relative,pin in chosen["sources"].items():
            need(set(pin) == {"bytes","sha256"},"SOURCE_PIN_FIELDS")
            path = ROOT/relative
            need(path.stat().st_size == pin["bytes"] and sha(path) == pin["sha256"],"SOURCE_PIN:"+relative)
        for name,digest in recipe["runtime_pins_rechecked"].items(): need(sha(Path(name)) == digest,"RUNTIME_PIN:"+name)
        for name,digest in q.HELPERS.items(): need(sha(q.CRYPTO/name) == digest,"HELPER_CHANGED:"+name)
        need(sha(ROOT/"experiments/scale-equation-01/runtime.py") == q.RUNTIME_SHA
            and sha(p.HELPERS/"run_stage.py") == p.HELPER_SHA and sha(p.HELPERS/"domains.py") == p.DOMAINS_SHA
            and sha(p.PYTHON) == p.PYTHON_SHA and sha(p.PYTHON.parent/"python314.dll") == p.PYTHON_DLL_SHA,
            "CONTROLLER_RUNTIME_CHANGED")

    check_inputs()
    need(not run.exists() and not attempt.exists(),"FRESH_SYNTAX_CONTROL")
    run.mkdir(); (run/"commands").mkdir(); save(run/"selection.json",chosen)
    phase = None
    result = {"schema":"DMKN_V5_PROOF_VALIDATION_CONTROL_RESULT_V1","status":"FAIL",
        "selection_sha256":sys.argv[2],"checker_rebuilds":0,"module_relation_rebuilds":0,
        "native_kernel_calls":0,"guest_calls":0,"proof_calls":0,"network_calls":0,
        "authority":"SYNTAX_DIFFERENTIAL_ONLY_NOT_MATHEMATICAL_ADMISSION"}

    class Budget:
        def __init__(self): self.peak = {"working_bytes":0,"entries":0}; self.current = {}
        def refresh(self):
            need(time.monotonic()-started <= 300 and time.process_time()-cpu <= 60,"SYNTAX_TOTAL_ENVELOPE")
            self.current = c.census(run)
            need(self.current["working_bytes"] <= 256*1024**2 and self.current["entries"] <= 1024,"SYNTAX_OUTPUT_ENVELOPE")
            for key in self.peak: self.peak[key] = max(self.peak[key],self.current[key])

    budget = Budget()
    try:
        snapshot = run/"source"
        for relative,pin in chosen["sources"].items():
            target = snapshot/relative; target.parent.mkdir(parents=True,exist_ok=True)
            with target.open("xb") as stream: stream.write((ROOT/relative).read_bytes())
            need(target.stat().st_size == pin["bytes"] and sha(target) == pin["sha256"],"SOURCE_SNAPSHOT_PIN")
        save(run/"source-map.json",chosen["sources"])
        retained = json.loads(COMMANDS.read_bytes())
        need(retained[0][0] == "module-relation","RETAINED_MODULE_RECIPE")
        original = retained[0][1]
        need(original.count("--crate-name") == 1 and original.count("--extern") == 4,"EXACT_RECIPE_SHAPE")
        # Retain compiler/linker/options and dependency search locations, but
        # do not link the native checker, module relation or proof-system crate.
        command = original[:original.index("--crate-name")]
        need("lto=fat" not in command and "lto=fat" in recipe["argv"],"RETAINED_FAT_LTO_RECIPE")
        command[1:1] = ["-C","lto=fat"]
        output = run/"proof_validation_tests.exe"
        command += ["--crate-name","dmkn_proof_validation_controls","--test",
            str(snapshot/"software/v5/modules/native/proof_validation/control_root.rs"),"-o",str(output)]
        for crate in ("serde","serde_json"):
            externs = [original[i+1] for i,value in enumerate(original[:-1])
                if value == "--extern" and original[i+1].startswith(crate+"=")]
            need(len(externs) == 1,"EXACT_SERDE_EXTERN:"+crate)
            command += ["--extern",externs[0]]
        commands = [("serde-compile",command),("syntax-controls",[str(output),"--test-threads=1"])]
        save(run/"compile-and-test-commands.json",commands)
        env,environment = p.environment(run,c.OLD/"rust")
        env["VCToolsUserTelemetryOptOut"] = "1"; environment["environment_keys_only"] = sorted(env)
        save(run/"environment-profile.json",environment)

        def exact_job(seconds,_memory,active_processes):
            need(seconds == 120 and active_processes == 8,"ADOPTED_PHASE_CALL_SHAPE")
            return run_stage.Job(120,1536,active_processes=6)

        budget.refresh(); phase = r.phase_class(p,a)("syntax-compile-and-test",run,budget,env,exact_job,120)
        phase.invoke(*commands[0],ROOT,allow_build_telemetry=True)
        binary = a.pin(output)
        logs = phase.invoke(*commands[1],ROOT)
        need(a.pin(output) == binary,"TEST_BINARY_CHANGED")
        text = logs.read_text(encoding="utf-8")
        names = re.findall(r"^test module_correspondence::correspondence_controls::([a-z0-9_]+) \.\.\. ok$",text,re.MULTILINE)
        need(len(names) == 12 and set(names) == TESTS and
            "test result: ok. 12 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out;" in text,
            "EXACT_TWELVE_SYNTAX_GROUPS")
        result.update(status="PASS_SERDE_ONLY_TWELVE_SYNTAX_GROUPS",outputs={output.name:binary},tests=sorted(names))
    except BaseException as error: result["error"] = type(error).__name__+": "+str(error)[:4000]
    finally:
        if phase is not None:
            try: phase.close()
            except BaseException as error: result.update(status="FAIL_CLEANUP",cleanup_error=str(error)[:2000])
            result["job"],result["commands"] = phase.final_stats,phase.commands
        try:
            check_inputs()
            need(json.loads((run/"selection.json").read_bytes()) == chosen,"SAVED_SELECTION_CHANGED")
            need(c.file_map(run/"source") == chosen["sources"],"SOURCE_SNAPSHOT_CHANGED")
            budget.refresh()
        except BaseException as error: result.update(status="FAIL_FINAL_CHECK",final_error=str(error)[:3000])
        result.update(controller_cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-started,
            output_census=budget.current,sampled_peaks=budget.peak,
            accounting="CONTROLLER_DISJOINT_FROM_INCLUSIVE_WORKER_JOB;FINAL_REPORT_EXIT_TAIL_EXCLUDED")
        save(run/"RESULT.json",result); save(attempt,{"status":result["status"],"result_sha256":sha(run/"RESULT.json")})
        try: budget.refresh()
        except BaseException as error:
            result.update(status="FAIL_FINALIZATION",finalization_error=str(error)[:3000])
            save(run/"FINALIZATION-FAILED.json",{"status":"FAIL_FINALIZATION","overrides_result_and_attempt":True,
                "result_sha256":sha(run/"RESULT.json"),"error":str(error)[:3000]})
    print(json.dumps({key:result.get(key) for key in ("status","error","wall_seconds")}))
    return 0 if result["status"] == "PASS_SERDE_ONLY_TWELVE_SYNTAX_GROUPS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
