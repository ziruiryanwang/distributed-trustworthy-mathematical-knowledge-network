"""Link-only successor: reuse both successful rlibs and the exact prior snapshot.

Restores the retained recipe's fat LTO for LLVM-bitcode-only dependencies. The
failed predecessor remains FAIL; neither successful relation library is rebuilt.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT/"experiments/v5-local-checks"
SOURCE = ROOT/"software/v5/aggregate"
OLD = HERE/"aggregate-native-build-01"
RUN = HERE/"aggregate-native-build-02"
ATTEMPT = HERE/"aggregate-native-build-02-attempt.json"
PREDECESSOR = SOURCE/"build_native.py"
PREDECESSOR_SHA = "4b77bad55119746df2e66cf7b8336b62ee1db8bfa4dca7152b6c1512b4ad892a"
RETAINED = {
    "RESULT.json":"8e60e4315158eb85ce63110234d9e179f88df6ecf8502abe8bc2b158abe5eb91",
    "source-map.json":"82c4dc73df29c9a4b6638ef1dd872ad8a0ccfeb66f97f89c5923ada93494f0d6",
    "compile-commands.json":"1f80c02b5049dbb5bdb22fea28ff52d8def582871b27366dd1cd98a73be5e232",
    "libdmkn_module_relation.rlib":"3d37e6dc700a7e789f8c0aa5f732ae6a7a4d8f46fd3ec9293f9d19bd35b31c0e",
    "libdmkn_aggregate_relation.rlib":"268f00c6f62f1c826d63546dc7d44ef0544721f0996732491f60f1799813c1e4",
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
    need(os.name == "nt" and Path.cwd() == ROOT and Path(__file__).resolve() == SOURCE/"build_native02.py"
        and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
        and not sys.flags.optimize and len(sys.argv) == 3,"ISOLATED_CANONICAL_LINK")
    selection = Path(sys.argv[1]).resolve(strict=True)
    need(selection.is_relative_to(HERE) and selection.stat().st_size <= 65536
        and sha(selection) == sys.argv[2],"EXACT_LINK_SELECTION")
    chosen = json.loads(selection.read_bytes())
    need(set(chosen) == {"schema","authorizes_link_only","driver_sha256"}
        and chosen["schema"] == "DMKN_V5_AGGREGATE_LINK_V1" and chosen["authorizes_link_only"] is True
        and sha(Path(__file__)) == chosen["driver_sha256"],"LINK_SELECTION_SCOPE")
    old = load("aggregate_link_predecessor",PREDECESSOR,PREDECESSOR_SHA)
    q = load("aggregate_link_prior",old.PRIOR,old.PRIOR_SHA)
    a = load("aggregate_link_artifacts",q.CRYPTO/"artifacts.py",q.HELPERS["artifacts.py"])
    p = load("aggregate_link_provision",q.CRYPTO/"provision_build.py",q.HELPERS["provision_build.py"])
    c = load("aggregate_link_census",q.CRYPTO/"continue_build03.py",q.HELPERS["continue_build03.py"])
    r = load("aggregate_link_phase",ROOT/"experiments/scale-equation-01/runtime.py",q.RUNTIME_SHA)
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
    for name,digest in RETAINED.items(): need(sha(OLD/name) == digest,"RETAINED_LINK_INPUT:"+name)
    sources = json.loads((OLD/"source-map.json").read_bytes())

    def check_inputs():
        need(time.monotonic()-started <= 600 and time.process_time()-cpu <= 60,"LINK_CONTROLLER_ENVELOPE")
        need(sha(selection) == sys.argv[2] and sha(Path(__file__)) == chosen["driver_sha256"]
            and sha(PREDECESSOR) == PREDECESSOR_SHA and sha(old.RECIPE) == old.RECIPE_SHA
            and sha(old.PRIOR) == old.PRIOR_SHA and sha(old.CHECKER) == old.CHECKER_SHA,"LINK_SOURCE_PINS")
        for name,digest in RETAINED.items(): need(sha(OLD/name) == digest,"RETAINED_CHANGED:"+name)
        need(c.file_map(OLD/"source") == sources,"RETAINED_SOURCE_SNAPSHOT")
        for name,digest in recipe["runtime_pins_rechecked"].items(): need(sha(Path(name)) == digest,"LINK_RUNTIME_PIN")
        for name,digest in q.HELPERS.items(): need(sha(q.CRYPTO/name) == digest,"LINK_HELPER_PIN")
        need(sha(ROOT/"experiments/scale-equation-01/runtime.py") == q.RUNTIME_SHA
            and sha(p.HELPERS/"run_stage.py") == p.HELPER_SHA and sha(p.HELPERS/"domains.py") == p.DOMAINS_SHA
            and sha(p.PYTHON) == p.PYTHON_SHA and sha(p.PYTHON.parent/"python314.dll") == p.PYTHON_DLL_SHA,
            "LINK_CONTROLLER_RUNTIME_CHANGED")

    check_inputs()
    need(not RUN.exists() and not ATTEMPT.exists(),"FRESH_LINK_ALLOCATION")
    RUN.mkdir(); (RUN/"commands").mkdir(); save(RUN/"selection.json",chosen)
    with (RUN/"build_native02.py").open("xb") as stream: stream.write(Path(__file__).read_bytes())
    phase = None
    result = {"schema":"DMKN_V5_AGGREGATE_LINK_RESULT_V1","status":"FAIL","selection_sha256":sys.argv[2],
        "relation_rebuilds":0,"checker_rebuilds":0,"test_calls":0,"guest_calls":0,"proof_calls":0,
        "network_calls":0,"authority":"LINK_ONLY_NOT_ADMISSION","retained_input_pins":RETAINED}

    class Budget:
        def __init__(self): self.peak = {"working_bytes":0,"entries":0}; self.current = {}
        def refresh(self):
            need(time.monotonic()-started <= 600 and time.process_time()-cpu <= 60,"LINK_TOTAL_ENVELOPE")
            self.current = c.census(RUN)
            need(self.current["working_bytes"] <= 1024**3 and self.current["entries"] <= 8192,"LINK_OUTPUT_ENVELOPE")
            for key in self.peak: self.peak[key] = max(self.peak[key],self.current[key])

    budget = Budget()
    try:
        prior = json.loads((OLD/"RESULT.json").read_bytes())
        need(prior["status"] == "FAIL" and len(prior["commands"]) == 3
            and all(row["status"] == "COMMAND_COMPLETED" and row["exit_code"] == 0
                for row in prior["commands"][:2]) and prior["commands"][2]["status"] == "FAILED",
            "RETAINED_SUCCESSFUL_RLIBS_WITH_FAILED_LINK")
        commands = json.loads((OLD/"compile-commands.json").read_bytes())
        need([row[0] for row in commands] == ["module-relation","aggregate-relation","aggregate-tests","aggregate-driver"]
            and "lto=fat" in recipe["argv"],"EXACT_PRIOR_LINK_RECIPE")
        selected = []
        for label,original in commands[2:]:
            command = list(original)
            need("lto=fat" not in command and command.count("-o") == 1,"LINK_CHANGE_ONLY_LTO_AND_OUTPUT")
            index = command.index("-o")+1
            expected = OLD/("aggregate_tests.exe" if label == "aggregate-tests" else "native_aggregate.exe")
            need(Path(command[index]) == expected,"PRIOR_EXACT_LINK_OUTPUT")
            command[index] = str(RUN/expected.name)
            command[1:1] = ["-C","lto=fat"]
            selected.append((label,command))
        save(RUN/"compile-commands.json",selected)
        env,environment = p.environment(RUN,c.OLD/"rust")
        env["VCToolsUserTelemetryOptOut"] = "1"; environment["environment_keys_only"] = sorted(env)
        save(RUN/"environment-profile.json",environment)

        def exact_job(seconds,_memory,active_processes):
            need(seconds == 240 and active_processes == 8,"ADOPTED_PHASE_CALL_SHAPE")
            return run_stage.Job(240,3072,active_processes=6)

        budget.refresh(); phase = r.phase_class(p,a)("aggregate-link",RUN,budget,env,exact_job,240)
        for label,command in selected: phase.invoke(label,command,ROOT,allow_build_telemetry=True)
        result.update(status="PASS_AGGREGATE_FINAL_LINKS_ONLY",outputs={name:a.pin(RUN/name)
            for name in ("aggregate_tests.exe","native_aggregate.exe")})
    except BaseException as error: result["error"] = type(error).__name__+": "+str(error)[:4000]
    finally:
        if phase is not None:
            try: phase.close()
            except BaseException as error: result.update(status="FAIL_CLEANUP",cleanup_error=str(error)[:2000])
            result["job"],result["commands"] = phase.final_stats,phase.commands
        try:
            check_inputs()
            need(sha(RUN/"build_native02.py") == chosen["driver_sha256"]
                and json.loads((RUN/"selection.json").read_bytes()) == chosen,"LINK_SAVED_CONTROL_CHANGED")
            budget.refresh()
        except BaseException as error: result.update(status="FAIL_FINAL_CHECK",final_error=str(error)[:3000])
        result.update(controller_cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-started,
            output_census=budget.current,sampled_peaks=budget.peak,
            accounting="CONTROLLER_DISJOINT_FROM_INCLUSIVE_WORKER_JOB;FINAL_REPORT_EXIT_TAIL_EXCLUDED")
        save(RUN/"RESULT.json",result); save(ATTEMPT,{"status":result["status"],"result_sha256":sha(RUN/"RESULT.json")})
        try: budget.refresh()
        except BaseException as error:
            result.update(status="FAIL_FINALIZATION",finalization_error=str(error)[:3000])
            save(RUN/"FINALIZATION-FAILED.json",{"status":"FAIL_FINALIZATION","overrides_result_and_attempt":True,
                "result_sha256":sha(RUN/"RESULT.json"),"error":str(error)[:3000]})
    print(json.dumps({key:result.get(key) for key in ("status","error","wall_seconds")}))
    return 0 if result["status"] == "PASS_AGGREGATE_FINAL_LINKS_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
