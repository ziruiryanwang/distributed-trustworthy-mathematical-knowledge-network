"""Two retained native inputs against a separately adopted rebuilt checker.

No baseline rerun, authoring, receipt verification, guest or proof operation.
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
SOURCE = ROOT/"software/v5/modules/native/proof_validation/integration"
SUPPORT = ROOT/"software/v5/modules/native/proof_validation/control.py"
SUPPORT_SHA = "91e25c3a3244a106c01ce18da63b07a163b0d07e53eddcf5376b399ee22a9ca1"
BASELINE = HERE/"aggregate-claims-controls-02/evidence"
BASELINE_PINS = {
    "actual-two-delta.bin":(215540,"7e21d092206b08a9a71231045b8152df4179ee6575cdc5e3afc704ef03c0be58"),
    "invalid-proof.bin":(215539,"bfea350f79ed86d25a5e16fbc55dc705620f80ac8b429779b2aa26f8c312f2f1"),
    "actual-two-delta/stdout.txt":(4444,"01d7c9cc45a16f520980e80672f90c0a97a69e31e344f748910df5abb24ffd0b"),
    "invalid-proof/stdout.txt":(98,"42d71010ea316cdbce83b22f2ce5ef77ced0dda6a980802091de6bb15134205d"),
    "invalid-proof/stderr.txt":(318,"c4607ce26de1d507914b60d63a4a1e61f25e8633a5bfe94ba9ab927901da54f9"),
    "RESULT.json":(7341,"0ea351dd244c37dd42b94c0dfb915c60602f97022a144fc2034032708d675bd1"),
}


def need(value,reason):
    if not value: raise ValueError(reason)


def sha(path):
    with path.open("rb") as stream: return hashlib.file_digest(stream,"sha256").hexdigest()


def load(name,path,digest):
    need(sha(path) == digest,"HELPER_PIN:"+str(path))
    spec = importlib.util.spec_from_file_location(name,path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def main():
    started,cpu = time.monotonic(),time.process_time()
    need(os.name == "nt" and Path.cwd() == ROOT and Path(__file__).resolve() == SOURCE/"compare.py"
        and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
        and not sys.flags.optimize and len(sys.argv) == 3,"ISOLATED_CANONICAL_NATIVE_COMPARISON")
    selection = Path(sys.argv[1]).resolve(strict=True)
    need(selection.is_relative_to(HERE) and selection.stat().st_size <= 65536
        and sha(selection) == sys.argv[2],"EXACT_COMPARISON_SELECTION")
    chosen = json.loads(selection.read_bytes())
    need(set(chosen) == {"schema","name","authorizes_two_native_calls","source","build_result"}
        and chosen["schema"] == "DMKN_V5_PROOF_VALIDATION_COMPARISON_V1"
        and chosen["authorizes_two_native_calls"] is True and type(chosen["name"]) is str
        and re.fullmatch(r"proof-validation-native-compare-[0-9]{2}",chosen["name"]),"COMPARISON_SELECTION_FIELDS")
    need(set(chosen["source"]) == {"bytes","sha256"},"SOURCE_PIN_FIELDS")
    need(set(chosen["build_result"]) == {"path","bytes","sha256"},"BUILD_RESULT_PIN_FIELDS")
    build_result = Path(chosen["build_result"]["path"])
    need(build_result.is_absolute() and build_result.resolve(strict=True) == build_result
        and build_result.parent.parent == HERE and build_result.name == "RESULT.json"
        and re.fullmatch(r"proof-validation-integration-build-[0-9]{2}",build_result.parent.name),"EXACT_BUILD_RESULT_PATH")
    need(build_result.stat().st_size == chosen["build_result"]["bytes"]
        and sha(build_result) == chosen["build_result"]["sha256"],"EXACT_BUILD_RESULT_PIN")
    built = json.loads(build_result.read_bytes())
    need(built["schema"] == "DMKN_V5_PROOF_VALIDATION_INTEGRATION_BUILD_RESULT_V1"
        and built["status"] == "PASS_PROOF_VALIDATION_FOUR_COMPILES_ONLY","SUCCESSFUL_FRESH_BUILD")
    native = build_result.parent/"native_aggregate.exe"
    need(set(built["outputs"]) == {"libnanoda_lib.rlib","libdmkn_module_relation.rlib",
        "libdmkn_aggregate_relation.rlib","native_aggregate.exe"},"EXACT_FOUR_BUILD_OUTPUTS")
    h = load("proof_compare_support",SUPPORT,SUPPORT_SHA)
    old = h.load("proof_compare_prior_build",h.PREDECESSOR,h.PREDECESSOR_SHA)
    q = h.load("proof_compare_prior",old.PRIOR,old.PRIOR_SHA)
    a = h.load("proof_compare_artifacts",q.CRYPTO/"artifacts.py",q.HELPERS["artifacts.py"])
    p = h.load("proof_compare_provision",q.CRYPTO/"provision_build.py",q.HELPERS["provision_build.py"])
    c = h.load("proof_compare_census",q.CRYPTO/"continue_build03.py",q.HELPERS["continue_build03.py"])
    r = h.load("proof_compare_phase",ROOT/"experiments/scale-equation-01/runtime.py",q.RUNTIME_SHA)
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
    need(sha(old.RECIPE) == old.RECIPE_SHA,"RETAINED_RUNTIME_RECIPE")
    recipe = json.loads(old.RECIPE.read_bytes())
    run = HERE/chosen["name"]; attempt = HERE/(chosen["name"]+"-attempt.json")

    def check_inputs():
        need(time.monotonic()-started <= 300 and time.process_time()-cpu <= 60,"COMPARISON_CONTROLLER_ENVELOPE")
        need(sha(selection) == sys.argv[2] and sha(SUPPORT) == SUPPORT_SHA
            and sha(h.PREDECESSOR) == h.PREDECESSOR_SHA and sha(old.PRIOR) == old.PRIOR_SHA
            and sha(old.RECIPE) == old.RECIPE_SHA,"SUPPORT_PINS_CHANGED")
        need((SOURCE/"compare.py").stat().st_size == chosen["source"]["bytes"]
            and sha(SOURCE/"compare.py") == chosen["source"]["sha256"],"COMPARISON_SOURCE_PIN")
        need(build_result.stat().st_size == chosen["build_result"]["bytes"]
            and sha(build_result) == chosen["build_result"]["sha256"]
            and not (build_result.parent/"FINALIZATION-FAILED.json").exists(),"BUILD_RESULT_CHANGED")
        marker = json.loads((HERE/(build_result.parent.name+"-attempt.json")).read_bytes())
        need(marker == {"status":built["status"],"result_sha256":sha(build_result)},"BUILD_FINALIZATION_MARKER")
        for name,pin in built["outputs"].items():
            need(pin == a.pin(build_result.parent/name),"BUILD_OUTPUT_CHANGED:"+name)
        for name,(size,digest) in BASELINE_PINS.items():
            need((BASELINE/name).stat().st_size == size and sha(BASELINE/name) == digest,"RETAINED_BASELINE_PIN:"+name)
        need(json.loads((BASELINE/"RESULT.json").read_bytes())["status"] == "PASS_REMAINING_EXACT_WARRANT_NATIVE_BOUNDARIES",
            "RETAINED_BASELINE_PASS")
        for name,digest in recipe["runtime_pins_rechecked"].items(): need(sha(Path(name)) == digest,"RUNTIME_PIN:"+name)
        for name,digest in q.HELPERS.items(): need(sha(q.CRYPTO/name) == digest,"HELPER_CHANGED:"+name)
        need(sha(ROOT/"experiments/scale-equation-01/runtime.py") == q.RUNTIME_SHA
            and sha(p.HELPERS/"run_stage.py") == p.HELPER_SHA and sha(p.HELPERS/"domains.py") == p.DOMAINS_SHA
            and sha(p.PYTHON) == p.PYTHON_SHA and sha(p.PYTHON.parent/"python314.dll") == p.PYTHON_DLL_SHA,
            "CONTROLLER_RUNTIME_CHANGED")

    check_inputs()
    need(not run.exists() and not attempt.exists(),"FRESH_NATIVE_COMPARISON")
    run.mkdir(); (run/"commands").mkdir(); h.save(run/"selection.json",chosen)
    with (run/"source.py").open("xb") as stream: stream.write((SOURCE/"compare.py").read_bytes())
    phase = None
    result = {"schema":"DMKN_V5_PROOF_VALIDATION_COMPARISON_RESULT_V1","status":"FAIL",
        "selection_sha256":sys.argv[2],"build_result":chosen["build_result"],"baseline_reruns":0,
        "author_calls":0,"receipt_calls":0,"guest_calls":0,"proof_calls":0,"network_calls":0,
        "authority":"NATIVE_CONDITIONAL_DIFFERENTIAL_NOT_CERTIFICATION","mathematical_admission":False}

    class Budget:
        def __init__(self): self.peak = {"working_bytes":0,"entries":0}; self.current = {}
        def refresh(self):
            need(time.monotonic()-started <= 300 and time.process_time()-cpu <= 60,"COMPARISON_TOTAL_ENVELOPE")
            self.current = c.census(run)
            need(self.current["working_bytes"] <= 16*1024**2 and self.current["entries"] <= 128,"COMPARISON_OUTPUT_ENVELOPE")
            for key in self.peak: self.peak[key] = max(self.peak[key],self.current[key])

    budget = Budget()
    try:
        env,environment = p.environment(run,c.OLD/"rust")
        h.save(run/"environment-profile.json",environment)

        def exact_job(seconds,_memory,active_processes):
            need(seconds == 60 and active_processes == 8,"ADOPTED_PHASE_CALL_SHAPE")
            return run_stage.Job(60,1536,active_processes=2)

        budget.refresh(); phase = r.phase_class(p,a)("retained-native-comparison",run,budget,env,exact_job,60)
        comparisons = []
        for name,code in (("actual-two-delta",0),("invalid-proof",2)):
            output = phase.invoke(name,[str(native),"check",str(BASELINE/(name+".bin"))],ROOT,expected_codes=(code,))
            actual = output.read_bytes(); expected = (BASELINE/name/"stdout.txt").read_bytes()
            need(actual == expected,"EXACT_NATIVE_STDOUT_DIFFERENTIAL:"+name)
            parsed = json.loads(actual)
            need(parsed["mathematical_admission"] is False,"NO_NATIVE_ADMISSION")
            if name == "actual-two-delta":
                need(parsed["status"] == "CHECKED_CONDITIONAL_AGGREGATE_NOT_ADMISSION"
                    and parsed["edges"] == 3 and len(parsed["members"]) == 3,"ACTUAL_TWO_DELTA_CONCLUSION")
            else:
                need(parsed == {"status":"REFUSED","reason":"CHECKER_PANIC_OR_UNRESOLVED_DEMAND",
                    "mathematical_admission":False},"EXACT_NATIVE_REFUSAL")
                diagnostic = (output.parent/"stderr.txt").read_text(encoding="utf-8")
                need("tc.rs:945:" in diagnostic and "assertion failed: self.def_eq(u, v)" in diagnostic,
                    "RETAINED_NATIVE_TYPE_ERROR_NOT_SETUP_REFUSAL")
            comparisons.append({"input":name,"exit_code":code,"stdout_byte_identical":True,
                "stdout_sha256":sha(output),"input_sha256":sha(BASELINE/(name+".bin"))})
        result.update(status="PASS_TWO_RETAINED_NATIVE_DIFFERENTIALS",comparisons=comparisons)
    except BaseException as error: result["error"] = type(error).__name__+": "+str(error)[:4000]
    finally:
        if phase is not None:
            try: phase.close()
            except BaseException as error: result.update(status="FAIL_CLEANUP",cleanup_error=str(error)[:2000])
            result["job"],result["commands"] = phase.final_stats,phase.commands
        try:
            check_inputs()
            need(json.loads((run/"selection.json").read_bytes()) == chosen,"SAVED_SELECTION_CHANGED")
            need((run/"source.py").stat().st_size == chosen["source"]["bytes"]
                and sha(run/"source.py") == chosen["source"]["sha256"],"SOURCE_SNAPSHOT_CHANGED")
            budget.refresh()
        except BaseException as error: result.update(status="FAIL_FINAL_CHECK",final_error=str(error)[:3000])
        result.update(controller_cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-started,
            output_census=budget.current,sampled_peaks=budget.peak,
            accounting="CONTROLLER_DISJOINT_FROM_INCLUSIVE_WORKER_JOB;FINAL_REPORT_EXIT_TAIL_EXCLUDED")
        h.save(run/"RESULT.json",result); h.save(attempt,{"status":result["status"],"result_sha256":sha(run/"RESULT.json")})
        try: budget.refresh()
        except BaseException as error:
            result.update(status="FAIL_FINALIZATION",finalization_error=str(error)[:3000])
            h.save(run/"FINALIZATION-FAILED.json",{"status":"FAIL_FINALIZATION","overrides_result_and_attempt":True,
                "result_sha256":sha(run/"RESULT.json"),"error":str(error)[:3000]})
    print(json.dumps({key:result.get(key) for key in ("status","error","wall_seconds")}))
    return 0 if result["status"] == "PASS_TWO_RETAINED_NATIVE_DIFFERENTIALS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
