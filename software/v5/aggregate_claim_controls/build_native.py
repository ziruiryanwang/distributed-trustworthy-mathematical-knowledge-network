"""One test-only compile correcting a malformed-fixture expectation.

Reuses the retained module/checker rlib and exact compiler recipe. No Cargo,
module/checker rebuild, tests, guest, proof, receipt operation or networking.
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
SOURCE = ROOT/"software/v5/aggregate_claim_controls"
OLD = HERE/"aggregate-native-build-01"
PREDECESSOR = ROOT/"software/v5/aggregate/build_native.py"
PREDECESSOR_SHA = "4b77bad55119746df2e66cf7b8336b62ee1db8bfa4dca7152b6c1512b4ad892a"
FRESH = ("refusal.rs", "build_native.py")
SHARED = {
    "software/v5/aggregate/census.rs":"f6ab62fe777482acb913972a34689eeaec16ed99fedae584cc6b62f6e4ba18df",
    "software/v5/aggregate_parse_once/census.rs":"88e9796bbb5493187f541d40e7c777afa8bfd4059929a9a2a1f118cfae815b04",
}
RETAINED = {
    "RESULT.json":"8e60e4315158eb85ce63110234d9e179f88df6ecf8502abe8bc2b158abe5eb91",
    "source-map.json":"82c4dc73df29c9a4b6638ef1dd872ad8a0ccfeb66f97f89c5923ada93494f0d6",
    "compile-commands.json":"1f80c02b5049dbb5bdb22fea28ff52d8def582871b27366dd1cd98a73be5e232",
    "libdmkn_module_relation.rlib":"3d37e6dc700a7e789f8c0aa5f732ae6a7a4d8f46fd3ec9293f9d19bd35b31c0e",
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
    need(os.name == "nt" and Path.cwd() == ROOT and Path(__file__).resolve() == SOURCE/"build_native.py"
        and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
        and not sys.flags.optimize and len(sys.argv) == 3,"ISOLATED_CANONICAL_CLAIMS_BUILD")
    selection = Path(sys.argv[1]).resolve(strict=True)
    need(selection.is_relative_to(HERE) and selection.stat().st_size <= 65536
        and sha(selection) == sys.argv[2],"EXACT_BUILD_SELECTION")
    chosen = json.loads(selection.read_bytes())
    need(set(chosen) == {"schema","name","authorizes_compile_only","sources"}
        and chosen["schema"] == "DMKN_V5_AGGREGATE_REFUSAL_BUILD_V1"
        and chosen["authorizes_compile_only"] is True and type(chosen["name"]) is str
        and re.fullmatch(r"aggregate-refusal-build-[0-9]{2}",chosen["name"]),"BUILD_SELECTION_FIELDS")
    expected = {"software/v5/aggregate_claim_controls/"+name for name in FRESH}
    expected.update(SHARED)
    need(type(chosen["sources"]) is dict and set(chosen["sources"]) == expected,"EXACT_SOURCE_SET")
    old = load("claims_build_predecessor",PREDECESSOR,PREDECESSOR_SHA)
    q = load("claims_build_prior",old.PRIOR,old.PRIOR_SHA)
    a = load("claims_build_artifacts",q.CRYPTO/"artifacts.py",q.HELPERS["artifacts.py"])
    p = load("claims_build_provision",q.CRYPTO/"provision_build.py",q.HELPERS["provision_build.py"])
    c = load("claims_build_census",q.CRYPTO/"continue_build03.py",q.HELPERS["continue_build03.py"])
    r = load("claims_build_phase",ROOT/"experiments/scale-equation-01/runtime.py",q.RUNTIME_SHA)
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
    need(sha(old.RECIPE) == old.RECIPE_SHA,"RETAINED_RECIPE")
    recipe = json.loads(old.RECIPE.read_bytes())
    for name,digest in RETAINED.items(): need(sha(OLD/name) == digest,"RETAINED_INPUT:"+name)
    old_sources = json.loads((OLD/"source-map.json").read_bytes())
    for relative,digest in SHARED.items():
        need(chosen["sources"][relative]["sha256"] == digest,"UNCHANGED_SHARED_SOURCE:"+relative)
        if relative.startswith("software/v5/aggregate/"):
            need(chosen["sources"][relative] == old_sources[relative],"RETAINED_SHARED_SOURCE:"+relative)
    run = HERE/chosen["name"]; attempt = HERE/(chosen["name"]+"-attempt.json")

    def check_inputs():
        need(time.monotonic()-started <= 600 and time.process_time()-cpu <= 60,"BUILD_CONTROLLER_ENVELOPE")
        need(sha(selection) == sys.argv[2] and sha(PREDECESSOR) == PREDECESSOR_SHA
            and sha(old.RECIPE) == old.RECIPE_SHA and sha(old.PRIOR) == old.PRIOR_SHA
            and sha(old.CHECKER) == old.CHECKER_SHA,"BUILD_RETAINED_SOURCE_PINS")
        for relative,pin in chosen["sources"].items():
            need(set(pin) == {"bytes","sha256"},"SOURCE_PIN_FIELDS")
            path = ROOT/relative
            need(path.stat().st_size == pin["bytes"] and sha(path) == pin["sha256"],"SOURCE_PIN:"+relative)
        for name,digest in RETAINED.items(): need(sha(OLD/name) == digest,"RETAINED_CHANGED:"+name)
        need(c.file_map(OLD/"source") == old_sources,"RETAINED_SOURCE_SNAPSHOT")
        for name,digest in recipe["runtime_pins_rechecked"].items(): need(sha(Path(name)) == digest,"RUNTIME_PIN:"+name)
        for name,digest in q.HELPERS.items(): need(sha(q.CRYPTO/name) == digest,"BUILD_HELPER_PIN")
        need(sha(ROOT/"experiments/scale-equation-01/runtime.py") == q.RUNTIME_SHA
            and sha(p.HELPERS/"run_stage.py") == p.HELPER_SHA and sha(p.HELPERS/"domains.py") == p.DOMAINS_SHA
            and sha(p.PYTHON) == p.PYTHON_SHA and sha(p.PYTHON.parent/"python314.dll") == p.PYTHON_DLL_SHA,
            "BUILD_CONTROLLER_RUNTIME_CHANGED")

    check_inputs()
    need(not run.exists() and not attempt.exists(),"FRESH_CLAIMS_BUILD")
    run.mkdir(); (run/"commands").mkdir(); save(run/"selection.json",chosen)
    phase = None
    result = {"schema":"DMKN_V5_AGGREGATE_REFUSAL_BUILD_RESULT_V1","status":"FAIL",
        "selection_sha256":sys.argv[2],"module_relation_rebuilds":0,"checker_rebuilds":0,"aggregate_relation_rebuilds":0,
        "test_calls":0,"guest_calls":0,"proof_calls":0,"network_calls":0,
        "authority":"COMPILE_ONLY_NOT_ADMISSION","retained_input_pins":RETAINED}

    class Budget:
        def __init__(self): self.peak = {"working_bytes":0,"entries":0}; self.current = {}
        def refresh(self):
            need(time.monotonic()-started <= 600 and time.process_time()-cpu <= 60,"BUILD_TOTAL_ENVELOPE")
            self.current = c.census(run)
            need(self.current["working_bytes"] <= 1024**3 and self.current["entries"] <= 8192,"BUILD_OUTPUT_ENVELOPE")
            for key in self.peak: self.peak[key] = max(self.peak[key],self.current[key])

    budget = Budget()
    try:
        snapshot = run/"source"
        for relative,pin in chosen["sources"].items():
            target = snapshot/relative; target.parent.mkdir(parents=True,exist_ok=True)
            with target.open("xb") as stream: stream.write((ROOT/relative).read_bytes())
            need(target.stat().st_size == pin["bytes"] and sha(target) == pin["sha256"],"SOURCE_SNAPSHOT_PIN")
        save(run/"source-map.json",chosen["sources"])
        prior = json.loads((OLD/"RESULT.json").read_bytes())
        need(prior["status"] == "FAIL" and len(prior["commands"]) == 3
            and prior["commands"][0]["status"] == "COMMAND_COMPLETED"
            and prior["commands"][0]["exit_code"] == 0,"RETAINED_MODULE_RLIB_SUCCESS")
        commands = json.loads((OLD/"compile-commands.json").read_bytes())
        need([row[0] for row in commands] == ["module-relation","aggregate-relation","aggregate-tests","aggregate-driver"]
            and "lto=fat" in recipe["argv"],"EXACT_RETAINED_RECIPE")
        selected = []
        for label,original in commands[2:3]:
            command = list(original)
            is_driver = label == "aggregate-driver"
            original_source = OLD/"source/software/v5/aggregate"/("native.rs" if is_driver else "lib.rs")
            fresh_source = snapshot/"software/v5/aggregate_claim_controls/refusal.rs"
            need(command.count(str(original_source)) == 1 and command.count("-o") == 1
                and "lto=fat" not in command,"ONLY_SELECTED_COMPILE_CHANGES")
            command[command.index(str(original_source))] = str(fresh_source)
            index = command.index("-o")+1
            output_name = {"aggregate-relation":"libdmkn_aggregate_relation.rlib",
                "aggregate-tests":"aggregate_tests.exe","aggregate-driver":"native_aggregate.exe"}[label]
            need(Path(command[index]) == OLD/output_name,"RETAINED_EXACT_OUTPUT")
            command[index] = str(run/"refusal_tests.exe")
            if is_driver:
                before = "dmkn_aggregate_relation="+str(OLD/"libdmkn_aggregate_relation.rlib")
                need(command.count(before) == 1,"DRIVER_EXACT_AGGREGATE_BINDING")
                command[command.index(before)] = "dmkn_aggregate_relation="+str(run/"libdmkn_aggregate_relation.rlib")
            if label != "aggregate-relation": command[1:1] = ["-C","lto=fat"]
            selected.append((label,command))
        save(run/"compile-commands.json",selected)
        env,environment = p.environment(run,c.OLD/"rust")
        env["VCToolsUserTelemetryOptOut"] = "1"; environment["environment_keys_only"] = sorted(env)
        save(run/"environment-profile.json",environment)

        def exact_job(seconds,_memory,active_processes):
            need(seconds == 240 and active_processes == 8,"ADOPTED_PHASE_CALL_SHAPE")
            return run_stage.Job(240,3072,active_processes=6)

        budget.refresh(); phase = r.phase_class(p,a)("claims-compile",run,budget,env,exact_job,240)
        for label,command in selected: phase.invoke(label,command,ROOT,allow_build_telemetry=True)
        result.update(status="PASS_ONE_CORRECTED_TEST_COMPILE_ONLY",outputs={name:a.pin(run/name)
            for name in ("refusal_tests.exe",)})
    except BaseException as error: result["error"] = type(error).__name__+": "+str(error)[:4000]
    finally:
        if phase is not None:
            try: phase.close()
            except BaseException as error: result.update(status="FAIL_CLEANUP",cleanup_error=str(error)[:2000])
            result["job"],result["commands"] = phase.final_stats,phase.commands
        try:
            check_inputs()
            need(json.loads((run/"selection.json").read_bytes()) == chosen,"SAVED_SELECTION_CHANGED")
            need(c.file_map(run/"source") == chosen["sources"],"BUILD_SNAPSHOT_CHANGED")
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
    return 0 if result["status"] == "PASS_ONE_CORRECTED_TEST_COMPILE_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
