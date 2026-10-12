"""Four finite native compiles for the reviewed correspondence successor.

Root supplies exact source selection. Rebuild the checker once, then the two
dependent rlibs and native driver. No test/native execution, Cargo, guest/proof.
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
NATIVE = HERE/"native-library-02"
MODULE = HERE/"aggregate-native-build-01"
CLAIMS = HERE/"aggregate-claims-build-02"
CHECKS = HERE/"proof-validation-controls-01"
RECORDS = {
    "native-library-02/selection.json":"7941f68e3615e7bb1119aa0083ce0cc73525e4b8e978f72ab4e596ba446b2cae",
    "native-library-02/command/command.json":"c07ca843fb34615dd4519c6197b6531b3185c42bf335ba0870ec6c3af46608aa",
    "aggregate-native-build-01/source-map.json":"82c4dc73df29c9a4b6638ef1dd872ad8a0ccfeb66f97f89c5923ada93494f0d6",
    "aggregate-native-build-01/compile-commands.json":"1f80c02b5049dbb5bdb22fea28ff52d8def582871b27366dd1cd98a73be5e232",
    "aggregate-claims-build-02/source-map.json":"66a1e67c3c86b7756c785c2914b1228978e220ac198e2873b37737d4f9ac474c",
    "aggregate-claims-build-02/compile-commands.json":"712a998a8a62c3fbff1289b69d02bb075a663fd6b6eec8e25e229fa04a6d7f3c",
    "aggregate-claims-build-02/RESULT.json":"06fd5deac8e66853daa72e35b819fa4766943e708264c98166a67ff7c8111ba2",
    "proof-validation-controls-01/source-map.json":"780c143f932735cb3bfa64af0ef99e011bfc9325bd159831d3c152bf241800ef",
    "proof-validation-controls-01/RESULT.json":"9855b711053e35438c7b5f8e66662e389e06d366734524297cafde46d84650e2",
}
CHECKER_NAMES = ("debug_printer", "demand", "env", "expr", "inductive", "level", "module",
    "name", "parser", "pretty_printer", "quot", "tc", "unique_hasher", "util")
MODULE_NAMES = ("lib", "canonical", "input", "foundation_static", "foundation_data",
    "commitments", "journal", "policy", "relation")
CHECKER_PATHS = {"software/v5/modules/native/checker/src/"+name+".rs" for name in CHECKER_NAMES}
MODULE_PATHS = {"software/v5/modules/receipt/src/"+name+".rs" for name in MODULE_NAMES}
CLAIMS_PATHS = {"software/v5/aggregate_claims/"+name+".rs" for name in ("lib","header","membership","relation","wire")}
CLAIMS_PATHS.update(("software/v5/aggregate_parse_once/census.rs","software/v5/aggregate/native.rs"))
CORRESPONDENCE = "software/v5/modules/native/proof_validation/module_correspondence.rs"
FRESH_PATHS = {"software/v5/modules/native/proof_validation/lib.rs",
    "software/v5/modules/native/proof_validation/integration/build.py"}
SOURCE_PATHS = CHECKER_PATHS | MODULE_PATHS | CLAIMS_PATHS | FRESH_PATHS | {CORRESPONDENCE}


def need(value, reason):
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
    need(os.name == "nt" and Path.cwd() == ROOT and Path(__file__).resolve() == SOURCE/"build.py"
        and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
        and not sys.flags.optimize and len(sys.argv) == 3,"ISOLATED_CANONICAL_INTEGRATION_BUILD")
    selection = Path(sys.argv[1]).resolve(strict=True)
    need(selection.is_relative_to(HERE) and selection.stat().st_size <= 65536
        and sha(selection) == sys.argv[2],"EXACT_INTEGRATION_SELECTION")
    chosen = json.loads(selection.read_bytes())
    need(set(chosen) == {"schema","name","authorizes_compile_only","sources"}
        and chosen["schema"] == "DMKN_V5_PROOF_VALIDATION_INTEGRATION_BUILD_V1"
        and chosen["authorizes_compile_only"] is True and type(chosen["name"]) is str
        and re.fullmatch(r"proof-validation-integration-build-[0-9]{2}",chosen["name"]),"BUILD_SELECTION_FIELDS")
    need(len(SOURCE_PATHS) == 33 and type(chosen["sources"]) is dict
        and set(chosen["sources"]) == SOURCE_PATHS,"EXACT_32_RUST_AND_CONTROLLER_SOURCES")
    h = load("proof_integration_support",SUPPORT,SUPPORT_SHA)
    old = h.load("proof_integration_prior_build",h.PREDECESSOR,h.PREDECESSOR_SHA)
    q = h.load("proof_integration_prior",old.PRIOR,old.PRIOR_SHA)
    a = h.load("proof_integration_artifacts",q.CRYPTO/"artifacts.py",q.HELPERS["artifacts.py"])
    p = h.load("proof_integration_provision",q.CRYPTO/"provision_build.py",q.HELPERS["provision_build.py"])
    c = h.load("proof_integration_census",q.CRYPTO/"continue_build03.py",q.HELPERS["continue_build03.py"])
    r = h.load("proof_integration_phase",ROOT/"experiments/scale-equation-01/runtime.py",q.RUNTIME_SHA)
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
    for relative,digest in RECORDS.items(): need(sha(HERE/relative) == digest,"RETAINED_RECORD:"+relative)
    need(sha(old.RECIPE) == old.RECIPE_SHA,"RETAINED_RUNTIME_RECIPE")
    recipe = json.loads(old.RECIPE.read_bytes())
    native_selection = json.loads((NATIVE/"selection.json").read_bytes())
    module_map = json.loads((MODULE/"source-map.json").read_bytes())
    claims_map = json.loads((CLAIMS/"source-map.json").read_bytes())
    checked_map = json.loads((CHECKS/"source-map.json").read_bytes())
    need(json.loads((CHECKS/"RESULT.json").read_bytes())["status"] == "PASS_SERDE_ONLY_TWELVE_SYNTAX_GROUPS"
        and json.loads((CLAIMS/"RESULT.json").read_bytes())["status"] == "PASS_CLAIMS_V2_THREE_THIN_COMPILES_ONLY",
        "RETAINED_PREREQUISITE_RESULTS")
    for relative in CHECKER_PATHS:
        need(chosen["sources"][relative]["sha256"] == native_selection["sources"][relative],"UNCHANGED_CHECKER_SOURCE")
    for paths,mapping in ((MODULE_PATHS,module_map),(CLAIMS_PATHS,claims_map),({CORRESPONDENCE},checked_map)):
        for relative in paths: need(chosen["sources"][relative] == mapping[relative],"EXACT_ADOPTED_SOURCE:"+relative)
    run = HERE/chosen["name"]; attempt = HERE/(chosen["name"]+"-attempt.json")

    def check_inputs():
        need(time.monotonic()-started <= 600 and time.process_time()-cpu <= 60,"BUILD_CONTROLLER_ENVELOPE")
        need(sha(selection) == sys.argv[2] and sha(SUPPORT) == SUPPORT_SHA
            and sha(h.PREDECESSOR) == h.PREDECESSOR_SHA and sha(old.PRIOR) == old.PRIOR_SHA
            and sha(old.RECIPE) == old.RECIPE_SHA,"SUPPORT_PINS_CHANGED")
        for relative,digest in RECORDS.items(): need(sha(HERE/relative) == digest,"RECORD_CHANGED:"+relative)
        for relative,pin in chosen["sources"].items():
            need(set(pin) == {"bytes","sha256"},"SOURCE_PIN_FIELDS")
            path = ROOT/relative
            need(path.stat().st_size == pin["bytes"] and sha(path) == pin["sha256"],"SOURCE_PIN:"+relative)
        for name,digest in recipe["runtime_pins_rechecked"].items(): need(sha(Path(name)) == digest,"RUNTIME_PIN:"+name)
        for name,digest in native_selection["runtime_pins"].items(): need(sha(Path(name)) == digest,"CHECKER_RUNTIME_PIN:"+name)
        for name,digest in q.HELPERS.items(): need(sha(q.CRYPTO/name) == digest,"HELPER_CHANGED:"+name)
        need(sha(ROOT/"experiments/scale-equation-01/runtime.py") == q.RUNTIME_SHA
            and sha(p.HELPERS/"run_stage.py") == p.HELPER_SHA and sha(p.HELPERS/"domains.py") == p.DOMAINS_SHA
            and sha(p.PYTHON) == p.PYTHON_SHA and sha(p.PYTHON.parent/"python314.dll") == p.PYTHON_DLL_SHA,
            "CONTROLLER_RUNTIME_CHANGED")

    check_inputs()
    need(not run.exists() and not attempt.exists(),"FRESH_INTEGRATION_BUILD")
    run.mkdir(); (run/"commands").mkdir(); h.save(run/"selection.json",chosen)
    phase = None
    result = {"schema":"DMKN_V5_PROOF_VALIDATION_INTEGRATION_BUILD_RESULT_V1","status":"FAIL",
        "selection_sha256":sys.argv[2],"test_calls":0,"native_calls":0,"guest_calls":0,"proof_calls":0,
        "network_calls":0,"dependency_rebuilds":0,"authority":"COMPILE_ONLY_NOT_ADMISSION"}

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
        h.save(run/"source-map.json",chosen["sources"])
        selected = []
        checker = list(json.loads((NATIVE/"command/command.json").read_bytes())["argv"])

        def replace_once(command,before,after):
            need(command.count(str(before)) == 1,"EXACT_RECIPE_REPLACEMENT:"+str(before))
            command[command.index(str(before))] = str(after)

        replace_once(checker,NATIVE/"sources/software/v5/modules/native/checker/src/lib.rs",
            snapshot/"software/v5/modules/native/proof_validation/lib.rs")
        replace_once(checker,NATIVE/"libnanoda_lib.rlib",run/"libnanoda_lib.rlib")
        need(checker.count("--extern") == 8 and "--test" not in checker,"UNCHANGED_CHECKER_RECIPE")
        selected.append(("checker",checker))
        module_commands = json.loads((MODULE/"compile-commands.json").read_bytes())
        claims_commands = json.loads((CLAIMS/"compile-commands.json").read_bytes())
        need([row[0] for row in module_commands] == ["module-relation","aggregate-relation","aggregate-tests","aggregate-driver"]
            and [row[0] for row in claims_commands] == ["aggregate-relation","aggregate-tests","aggregate-driver"],"RETAINED_COMMAND_LABELS")
        transforms = [
            ("module-relation",module_commands[0][1],MODULE,"software/v5/modules/receipt/src/lib.rs","libdmkn_module_relation.rlib"),
            ("aggregate-relation",claims_commands[0][1],CLAIMS,"software/v5/aggregate_claims/lib.rs","libdmkn_aggregate_relation.rlib"),
            ("aggregate-driver",claims_commands[2][1],CLAIMS,"software/v5/aggregate/native.rs","native_aggregate.exe"),
        ]
        old_search = {"dependency="+str(path) for path in (NATIVE,MODULE,CLAIMS)}
        for label,original,old_run,source_relative,output_name in transforms:
            command = list(original)
            replace_once(command,old_run/"source"/source_relative,snapshot/source_relative)
            replace_once(command,old_run/output_name,run/output_name)
            if label == "module-relation":
                replace_once(command,"nanoda_lib="+str(NATIVE/"libnanoda_lib.rlib"),"nanoda_lib="+str(run/"libnanoda_lib.rlib"))
            else:
                replace_once(command,"dmkn_module_relation="+str(MODULE/"libdmkn_module_relation.rlib"),
                    "dmkn_module_relation="+str(run/"libdmkn_module_relation.rlib"))
            if label == "aggregate-driver":
                replace_once(command,"dmkn_aggregate_relation="+str(CLAIMS/"libdmkn_aggregate_relation.rlib"),
                    "dmkn_aggregate_relation="+str(run/"libdmkn_aggregate_relation.rlib"))
                need("lto=fat" in command,"RETAINED_DRIVER_FAT_LTO")
            rewritten = []; index = 0; inserted = False
            while index < len(command):
                if command[index] == "-L" and command[index+1] in old_search:
                    if not inserted: rewritten.extend(("-L","dependency="+str(run))); inserted = True
                    index += 2
                else: rewritten.append(command[index]); index += 1
            need(inserted and not any(value in old_search for value in rewritten)
                and "--test" not in rewritten,"ONLY_FRESH_PROJECT_DEPENDENCY_PATH")
            selected.append((label,rewritten))
        h.save(run/"compile-commands.json",selected)
        env,environment = p.environment(run,c.OLD/"rust")
        env["VCToolsUserTelemetryOptOut"] = "1"; environment["environment_keys_only"] = sorted(env)
        h.save(run/"environment-profile.json",environment)

        def exact_job(seconds,_memory,active_processes):
            need(seconds == 240 and active_processes == 8,"ADOPTED_PHASE_CALL_SHAPE")
            return run_stage.Job(240,3072,active_processes=6)

        budget.refresh(); phase = r.phase_class(p,a)("integration-compile",run,budget,env,exact_job,240)
        for label,command in selected: phase.invoke(label,command,ROOT,allow_build_telemetry=True)
        result.update(status="PASS_PROOF_VALIDATION_FOUR_COMPILES_ONLY",outputs={name:a.pin(run/name)
            for name in ("libnanoda_lib.rlib","libdmkn_module_relation.rlib","libdmkn_aggregate_relation.rlib","native_aggregate.exe")})
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
        h.save(run/"RESULT.json",result); h.save(attempt,{"status":result["status"],"result_sha256":sha(run/"RESULT.json")})
        try: budget.refresh()
        except BaseException as error:
            result.update(status="FAIL_FINALIZATION",finalization_error=str(error)[:3000])
            h.save(run/"FINALIZATION-FAILED.json",{"status":"FAIL_FINALIZATION","overrides_result_and_attempt":True,
                "result_sha256":sha(run/"RESULT.json"),"error":str(error)[:3000]})
    print(json.dumps({key:result.get(key) for key in ("status","error","wall_seconds")}))
    return 0 if result["status"] == "PASS_PROOF_VALIDATION_FOUR_COMPILES_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
