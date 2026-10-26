"""One proof-free question over the adopted received AllClosure module.

TEST ONLY: run once only after root selects this source and a finite outer Job.
No export, intake, proof, helper build, search/provider or direct owner-state read.
The public query command opens real owner state and may settle reservations.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time
from types import ModuleType

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
PACKAGE = LOCAL / "exact-module-assembly01/assembled/package"
PUBLIC_RUN = LOCAL / "exact-module-public01"
PUBLIC = PUBLIC_RUN / "public"
COLD = PUBLIC / "cold-module"
OWNER = LOCAL / "concept-recipient-init-01"
PYTHON = Path(r"D:\Python314\python.exe")
LEAN = ROOT / "software/runtime/lean-4.34.0-windows"
HERE = ROOT / "software/v5/ordinary_received_query"
HELPER = ROOT / "software/v5/ordinary_fair_search/assemble.py"
HELPER_SHA = "9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30"
CUSTODY_LIMITS = PUBLIC_RUN / "sources/software/v5/concept_episode/CUSTODY-LIMITS.json"
PROFILE = "bde63019d1a6ac2bccd8e0c245a405ad3ca551d0606c01a5193fee6897c60346"
INSTALLATION = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
STORE = "dbaa21256e87cbbf12e1694e183b8d3d25c290af9c73da54395fa4e3923f6b09"
CONTEXT = "03de3aa800949731dfc0823d8661374c9f216262211c9bfe1ac6afd930421e20"
SEMANTIC = "9108f44dba66e2a26a06f65566e143e3185e3f8237e156a4e5c826222a308ad7"
FOUNDATION = "884f408f0e7d647a1b72714cfa78685804dea9e07289a67176692cfbfe2c8282"
IMPLEMENTATION = "fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df"
ANCHOR = "79db183e7c154929cb8aca320082854ddde304466a3dd901da071aac425f9325"
MODULE = "DMKNBridge_1a3b16fc61d27a93a3187cc140d70cdc05c59b24816cf114bc4f3a1e93fac1cf"
ALL_CLOSURE = "RepairTheory.ClosureBridge.AllClosure"
TARGET_UNIT = "52c32f0b4de89b9fed93bd099499dd7d029c6bc62e5de32bfeeaa25b08c9e3dd"
TARGET_EXPORT = "c29570a4552bf5c00725aa451bada64d9faa780d39a7e050fb5853af9ab1b4ba"
PUBLIC_PINS = {
    PUBLIC_RUN / "RESULT.json": "e111dfd60898684907771cd7df569cd2d3431cfcd7ad79fde4fd3813076bd0f0",
    PUBLIC / "RESULT.json": "319e6104ba46bcc2ae1035e6419e615def52339ce95b4bc716766f5811fa78f4",
    PUBLIC / "cold-stdout.json": "0806e4720a5305d7665b2a006a840b5f32fe3134aeddbd61c9803507915f8c5a",
    COLD / "MODULE.json": "171908ae18b36415dbd89fb355ff224977e6ee43ef3efe6f38d2e80849b36442",
    COLD / "request.json": "0d582fd771aa7e983043f1219441c0ac08f1584bf79ea965fe84b210810835ee",
    COLD / "native-report.json": "a30107f7ecc95a8e75e9fac9c8008bf940439d20da4526cc48386182a62efff9",
    COLD / "inventory.json": "c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0",
    COLD / "anchor-plan.json": "68b6c3602e9e70a4b90296dbba57c3c5807b509fc21f93116da3a2eafe1780fe",
    CUSTODY_LIMITS: "abf5b2dc515a06691194c47e7a320a7fdeaedbbaa18ec45e074807649968ecbe",
}
MIB = 1024**2
START, CPU = time.monotonic(), time.process_time()
LEAN_LIMITS = dict(wall_seconds=35, cpu_seconds=25, memory_mib=1536,
                   active_processes=2, stdout_bytes=MIB, stderr_bytes=MIB)
QUERY_LIMITS = dict(wall_seconds=45, cpu_seconds=25, memory_mib=1024,
                    active_processes=2, stdout_bytes=MIB, stderr_bytes=MIB)
LAUNCHER_LIMITS = dict(QUERY_LIMITS, wall_seconds=55, cpu_seconds=35, active_processes=3)


def need(ok, code):
    if not ok:
        raise ValueError("RECEIVED_QUERY_" + code)


def check():
    need(time.monotonic()-START < 120 and time.process_time()-CPU < 25, "ALLOWANCE")


def load(name, path, raw):
    need(name not in sys.modules, "PRELOADED_MODULE:" + name)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def name(text):
    return [[0, {"$bytes": list(part.encode("ascii"))}] for part in text.split(".")]


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and Path(sys.executable) == PYTHON and
         sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and
         not sys.flags.optimize, "EXECUTION_PROFILE")
    helper_raw = HELPER.read_bytes()
    need(hashlib.sha256(helper_raw).hexdigest() == HELPER_SHA, "HELPER_PIN")
    H = load("_received_query_files", HELPER, helper_raw)
    output = H.ordinary(Path(args.output), directory=True, fresh=True)
    # Root owns the fresh enclosing run; this fresh child keeps its evidence together.
    need(output.parent.parent == LOCAL and output.name == "query", "FRESH_OUTPUT_DOMAIN")
    pins = {}

    def selected(path, expected=None, maximum=128*MIB):
        actual = H.pin(path, check, maximum)
        if expected is not None:
            need(actual == expected if type(expected) is dict else
                 actual["sha256"] == expected, "INPUT_PIN:" + str(path))
        if path in pins:
            need(pins[path] == actual, "INPUT_CHANGED:" + str(path))
        pins[path] = actual
        return actual

    def read(path, expected=None):
        pin = selected(path, expected, 2*MIB)
        raw = H.ordinary(path).read_bytes()
        need(len(raw) == pin["bytes"] and H.digest(raw) == pin["sha256"], "READ_CHANGED")
        return raw

    def document(path, expected=None):
        raw = read(path, expected)
        value, _ = H.read_json(path, H.digest(raw), check)
        return value

    def source(module, path):
        return load(module, path, read(path, pins[path]))

    selected(HELPER, HELPER_SHA)
    selected(HERE / "test_query.py")
    need(selected(Path(__file__).absolute()) == pins[HERE / "test_query.py"], "RUNNING_SOURCE")
    selected(HERE / "PLAN.md"); selected(HERE / "CONTRACT.md")
    profile = document(PACKAGE / "PROFILE.json", PROFILE)
    need(profile["installation_manifest_sha256"] == INSTALLATION, "INSTALLATION_ID")
    installed = document(PACKAGE / "installation/INSTALLATION.json", INSTALLATION)
    # Reuse the selected maps; do not maintain another package/runtime manifest.
    for logical, pin in profile["files"].items():
        selected(PACKAGE / H.relative(logical), pin)
    helper_parts = {logical.removeprefix("authoring/helpers/") for logical in profile["files"]
                    if logical.startswith("authoring/helpers/")}
    H.census(PACKAGE / "authoring/helpers", helper_parts, check)
    for logical, pin in installed["files"].items():
        H.relative(logical)
        if logical.startswith("python_runtime/"):
            path = PYTHON.parent / logical.split("/", 1)[1]
        elif logical.startswith("lean_runtime/"):
            path = LEAN / logical.split("/", 1)[1]
        else:
            path = PACKAGE / "installation" / logical
        selected(path, pin)
    for path, sha in PUBLIC_PINS.items():
        selected(path, sha)

    R = source("_received_query_launcher", PACKAGE / "run.py")
    supervisor, Job = R.load_supervision(R.bind_support(PACKAGE, PROFILE, PYTHON.parent, check))

    def clean(report, limits=None):
        need(R.operational_result(report)["ok"] and
             report.get("termination_requested") is False, "UNCLEAN_CHILD")
        if limits is not None:
            need(report["limits"] == limits and
                 report["wall_seconds_through_cleanup"] <= limits["wall_seconds"] and
                 report["final_job"]["cpu_seconds"] <= limits["cpu_seconds"] and
                 all(report["observed_logs"][key] <= limits[key]
                     for key in ("stdout_bytes", "stderr_bytes")), "CHILD_ENVELOPE")

    outer_prior = document(PUBLIC_RUN / "RESULT.json")
    clean(outer_prior["result"])
    prior = document(PUBLIC / "RESULT.json")
    cold = document(PUBLIC / "cold-stdout.json")
    module = document(COLD / "MODULE.json")
    request = document(COLD / "request.json")
    native = document(COLD / "native-report.json")
    returned_module = cold["result"]
    need(prior["status"] == "PASS_EXACT_MODULE_COLD_AND_REOPEN" and
         prior["calls"][0] == cold and cold["ok"] is True and
         cold["profile_sha256"] == PROFILE and cold["store_id"] == STORE and
         {key: value for key, value in returned_module.items()
          if key not in {"manifest_path", "supported_runtime"}} == module and
         returned_module["manifest_path"] == str(COLD / "MODULE.json") and
         returned_module["supported_runtime"] == {
             "claim": "EXACT_SELECTED_LOCAL_RUNTIME_NOT_DOWNSTREAM_PROJECT_VALIDATION",
             "implementation_id": IMPLEMENTATION, "installation_manifest_sha256": INSTALLATION,
             "lean_executable": str(LEAN / "bin/lean.exe"),
             "lean_executable_pin": installed["files"]["lean_runtime/bin/lean.exe"],
             "lean_runtime": str(LEAN)}, "ADOPTED_PUBLIC_CHAIN")
    need(module["status"] == "CHECKED_AND_REGISTERED_LOCAL_MODULE_ANCHOR" and
         module["source_context_root"] == CONTEXT and module["anchor_id"] == ANCHOR and
         module["module_name"] == MODULE and module["semantic_id"] == SEMANTIC and
         module["foundation_id"] == FOUNDATION and module["new_catalog_acceptance"] is False and
         module["report_sha256"] == PUBLIC_PINS[COLD / "native-report.json"], "MODULE_IDENTITY")
    need(request["unit_ids"] == module["ordered_unit_ids"] == native["unit_ids"] and
         len(request["unit_ids"]) == len(request["units"]) == 10 and
         request["context_root"] == CONTEXT and request["semantic_id"] == SEMANTIC and
         request["foundation_id"] == FOUNDATION and request["module_name"] == name(MODULE) and
         request["anchor_id"] == "" and request["anchor_plan_sha256"] ==
         PUBLIC_PINS[COLD / "anchor-plan.json"] and
         native["semantic_id"] == SEMANTIC and native["module_name"] == name(MODULE),
         "ACTUAL_COLD_REQUEST")
    parts = module["artifact_parts"]
    need(set(parts) == {MODULE + suffix for suffix in
         (".olean", ".olean.private", ".olean.server", ".ir", ".ir.sig")}, "MODULE_PARTS")
    H.census(COLD / "modules", parts, check)
    for filename, pin in parts.items():
        selected(COLD / "modules" / H.relative(filename), pin)

    # These are inert codecs only; the harness never imports an owner/catalog API.
    for module_name in ("ordinary_evidence", "ordinary_semantics", "portable_evidence"):
        source(module_name, PACKAGE / "installation/py" / (module_name + ".py"))
    for module_name in ("ordinary_preview", "portable_preview", "formal_query"):
        source(module_name, PACKAGE / "authoring/py" / (module_name + ".py"))
    need("discovery" not in sys.modules, "PRELOADED_DISCOVERY")
    discovery = ModuleType("discovery"); discovery.__path__ = []
    sys.modules["discovery"] = discovery
    for module_name in ("formal_features", "ordinary_export_adapter"):
        setattr(discovery, module_name, source("discovery." + module_name,
                PACKAGE / "support/discovery" / (module_name + ".py")))
    E, S, Q = (sys.modules[key] for key in
               ("ordinary_evidence", "ordinary_semantics", "formal_query"))
    adapter = discovery.ordinary_export_adapter
    need(S.foundation_id() == FOUNDATION and S.semantic_id() == SEMANTIC and
         S.implementation_id(H.canonical(installed["implementation"])) == IMPLEMENTATION,
         "INTERPRETATION_IDS")
    basis = {}
    # The exact pinned legacy inventory has a final LF, unlike inert canonical ASTs.
    for row in json.loads(read(COLD / "inventory.json")):
        key = E.name_key(row[0])
        need(key not in basis, "DUPLICATE_BASIS_NAME")
        basis[key] = S.basis_symbol_id(SEMANTIC, FOUNDATION, row[0])
    need(len(basis) == 581, "BASIS_CENSUS")
    realized, flattened = {}, []
    for unit_id, unit in zip(request["unit_ids"], request["units"], strict=True):
        for row in unit[2]:
            key = E.name_key(row[0])
            need(key not in realized and key not in basis, "DUPLICATE_REALIZED_NAME")
            realized[key] = {"name": row[0], "unit_id": unit_id,
                             "export_id": S.export_id(SEMANTIC, unit_id, row[0])}
            flattened.append(row)
    need(len(realized) == 21 and native["inventories"] == flattened and
         native["names"] == [row[0] for row in flattened], "REALIZED_CENSUS")
    need(realized[E.name_key(name(ALL_CLOSURE))] == {
         "name": name(ALL_CLOSURE), "unit_id": TARGET_UNIT, "export_id": TARGET_EXPORT} and
         module["targets"] == [realized[E.name_key(name(ALL_CLOSURE))]], "REALIZED_TARGET")

    output.mkdir()
    phase, completed = "SOURCE", []
    try:
        native_dir = output / "native"; native_dir.mkdir()
        type_path = native_dir / "type.json"
        source_path = native_dir / "Query.lean"
        # Match the existing basis-query source generator's Lean path quoting.
        source_raw = ("module\npublic import Init\npublic import " + MODULE +
            "\npublic meta import OwnerQueryCommand\npublic section\nuniverse u\n\n" +
            "#ordinary_type_query [u] " + json.dumps(type_path.as_posix(), ensure_ascii=False) + " :\n" +
            "  forall {T : Type u} (o : RepairTheory.ClosureBridge.OrderData T)\n" +
            "    (r : RepairTheory.Repair T) (rs : List (RepairTheory.Repair T)),\n" +
            "    RepairTheory.ClosureBridge.AllClosure o (List.cons r rs) ->\n" +
            "    RepairTheory.ClosureBridge.AllClosure o rs\n").encode("utf-8")
        H.fresh_bytes(source_path, source_raw); selected(source_path)
        lean_path = [COLD / "modules", PACKAGE / "authoring/helpers", LEAN / "lib/lean"]
        for path in lean_path:
            H.ordinary(path, directory=True)
        original_environment = supervisor.child_environment

        def environment(cwd):
            env = original_environment(cwd)
            env["PATH"] = os.pathsep.join(map(str, (PYTHON.parent, PYTHON.parent / "DLLs", LEAN / "bin")))
            env["LEAN_PATH"] = os.pathsep.join(map(str, lean_path))
            return env

        def command(label, argv, limits):
            check()
            supervisor.child_environment = environment
            try:
                report = supervisor.supervise(argv, ROOT, output / (label + "-child"), limits, Job)
            finally:
                supervisor.child_environment = original_environment
            report_raw = H.canonical(report)
            H.fresh_bytes(output / (label + "-SUPERVISION.json"), report_raw)
            need(read(output / (label + "-SUPERVISION.json")) == report_raw, "CHILD_REPORT_READBACK")
            clean(report, limits)
            need(report["observed_logs"]["stderr_bytes"] == 0, "CHILD_STDERR")
            completed.append(label)
            return report

        phase = "LEAN_TYPE_EXTRACTION"
        lean_argv = [str(LEAN / "bin/lean.exe"), "-j", "1", "-DElab.async=false",
            "-R", str(native_dir), str(source_path)]
        H.fresh_bytes(output / "IMPORT-SELECTION.json", H.canonical({
            "module_name": MODULE, "artifact_parts": parts, "lean_path": list(map(str, lean_path)),
            "public_copy": str(COLD / "modules"), "source": pins[source_path],
            "premise": "ROOT_ADOPTED_PUBLIC01_PUBLIC_COPY_EQUALS_REGISTERED_ARTIFACTS"}))
        lean_report = command("lean", lean_argv, LEAN_LIMITS)
        H.census(native_dir, ("Query.lean", "type.json"), check)
        native_raw = read(type_path)
        Q.read_native_type(native_raw)
        refs = Q.reference_names(native_raw)
        expected_names = {E.name_key(name(value)) for value in
            ("List", "List.cons", "RepairTheory.Repair", "RepairTheory.ClosureBridge.OrderData", ALL_CLOSURE)}
        need({E.name_key(value) for value in refs} == expected_names and len(refs) == 5,
             "SELECTED_QUESTION_REFERENCES")
        expected_bindings, nonbasis = [], []
        for value in refs:
            key = E.name_key(value)
            if key in basis:
                symbol = basis[key]
            else:
                need(key in realized, "REFERENCE_NOT_IN_REALIZED_CLOSURE")
                symbol = realized[key]["export_id"]
                nonbasis.append(realized[key])
            expected_bindings.append([value, symbol])
        need(len(nonbasis) == 3, "NONBASIS_CENSUS")
        bindings_raw = E.canonical_json(expected_bindings)

        phase = "PUBLIC_CONTEXT_QUERY"
        envelope, query_output = output / "query-envelope", output / "query"
        argv = [str(PYTHON), "-I", "-S", "-B", str(PACKAGE / "run.py"),
            "--profile-sha256", PROFILE, "--python-runtime", str(PYTHON.parent),
            "--lean-runtime", str(LEAN), "--diagnostics", str(envelope)]
        for key, value in QUERY_LIMITS.items():
            argv += ["--" + key.replace("_", "-"), str(value)]
        argv += ["query", "--", "--native-type", str(type_path), "--context-root", CONTEXT,
            "--catalog", str(OWNER / "catalog"), "--custody", str(OWNER / "custody"),
            "--store-id", STORE, "--custody-limits", str(CUSTODY_LIMITS), "--output", str(query_output)]
        launcher_report = command("query-launcher", argv, LAUNCHER_LIMITS)
        run = document(envelope / "RUN.json")
        need(run["ok"] is True and run["status"] == "CLI_EXITED_ZERO" and
             run["schema"] == "DMKN_ORDINARY_BOUNDED_OPERATION_V1" and run["tool"] == "query" and
             run["installation_manifest_sha256"] == INSTALLATION and
             run["profile_sha256"] == PROFILE and run["limits"] == QUERY_LIMITS and
             run["diagnostics"] == str(envelope) and
             document(output / "query-launcher-child/stdout.txt") == run, "PUBLIC_LAUNCHER_RESULT")
        inner_supervision = document(envelope / "SUPERVISION.json")
        clean(inner_supervision, QUERY_LIMITS)
        need(inner_supervision["observed_logs"]["stderr_bytes"] == 0, "QUERY_STDERR")
        result = document(query_output / "RESULT.json")
        need(document(envelope / "child/stdout.txt") == result and result["ok"] is True and
             result["operation"] == "prepare-query" and result["mathematical_acceptance"] is False and
             result["binding_mode"] == "selected-local-context" and
             result["interpretation"] == "SELECTED_RECEIVER_CONTEXT_NOT_PROJECT_EQUIVALENCE" and
             "close_errors" not in result and result["profile_sha256"] == PROFILE and
             result["context_selection"] == {"semantic_id": SEMANTIC, "foundation_id": FOUNDATION,
                 "implementation_id": IMPLEMENTATION, "store_id": STORE,
                 "context_root": CONTEXT, "reference_count": 5}, "INNER_QUERY_RESULT")
        phase = "EXACT_BINDING_AUDIT"
        actual_bindings = read(query_output / "BINDINGS.json")
        need(actual_bindings == bindings_raw, "EXACT_REALIZED_BINDINGS")
        expected_query = Q.bind_native_type(native_raw, bindings_raw, semantic_id=SEMANTIC)
        spec = Q.query_spec(expected_query)
        namespace = adapter.namespace_for(SEMANTIC)
        need(read(query_output / "QUERY.json") == expected_query and
             read(query_output / "SPECS.json") == E.canonical_json([spec]) and
             result["query_sha256"] == H.digest(expected_query) and
             result["native_type_sha256"] == H.digest(native_raw) and
             result["bindings_sha256"] == H.digest(bindings_raw) and
             result["specs"] == [spec] and result["namespace"] == namespace and
             result["features"] == adapter.compile_query(namespace, [spec]) and
             result["key_profile"] == Q.PROFILE_ID, "QUERY_OUTPUT_CORRESPONDENCE")
        H.census(query_output, ("RESULT.json", "BINDINGS.json", "QUERY.json", "SPECS.json"), check)
        phase = "FINAL_RECHECK"
        H.census(native_dir, ("Query.lean", "type.json"), check)
        H.census(COLD / "modules", parts, check)
        H.census(PACKAGE / "authoring/helpers", helper_parts, check)
        for path, pin in pins.items():
            need(H.pin(path, check) == pin, "FINAL_PIN:" + str(path))
        H.fresh_bytes(output / "PINS.json", H.canonical({str(path): pin for path, pin in pins.items()}))
        summary = {"status": "PASS_RECEIVED_CONCEPT_PROOF_FREE_QUERY", "profile_sha256": PROFILE,
            "source_context_root": CONTEXT, "anchor_id": ANCHOR, "module_name": MODULE,
            "received_export_bindings": nonbasis, "basis_references": 2, "reference_count": 5,
            "query": result, "completed_children": completed,
            "lean_job_cpu_seconds": lean_report["final_job"]["cpu_seconds"],
            "query_launcher_job_cpu_seconds": launcher_report["final_job"]["cpu_seconds"],
            "controller_cpu_seconds": time.process_time()-CPU, "wall_seconds": time.monotonic()-START,
            "cost_scope": "QUERY_LAUNCHER_JOB_INCLUDES_PUBLIC_QUERY_CHILD;DO_NOT_DOUBLE_COUNT",
            "authority": "TEST_EVIDENCE_REQUIRES_CLEAN_ROOT_ENVELOPE_AND_INDEPENDENT_ADOPTION",
            "claim": "ONE_RECEIVED_CONCEPT_QUESTION_NOT_PROOF_SEARCH_GROWTH_OR_NONEMPTY_ANCHOR_PLAN"}
        raw = H.canonical(summary)
        H.fresh_bytes(output / ".RESULT.pending", raw)
        need(H.pin(output / ".RESULT.pending", check, 2*MIB) ==
             {"bytes": len(raw), "sha256": H.digest(raw)}, "RESULT_READBACK")
        check(); H.ordinary(output / "RESULT.json", fresh=True)
        (output / ".RESULT.pending").rename(output / "RESULT.json")
        print(json.dumps({"status": summary["status"]}), flush=True)
    except BaseException as error:
        H.fresh_bytes(output / "FAILURE.json", H.canonical({"phase": phase,
            "error_type": type(error).__name__, "error": str(error)[:2000],
            "completed_children": completed, "wall_seconds": time.monotonic()-START,
            "controller_cpu_seconds": time.process_time()-CPU, "retention": "PRESERVED_NO_RETRY"}))
        raise


if __name__ == "__main__":
    main()
