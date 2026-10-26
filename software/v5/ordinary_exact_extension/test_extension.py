"""One retained, warranted theorem module extension above the existing anchor.

Source-only until root selects the bounded outer Job. The sole owner operation
is export-module; no initialization, intake, query, reopen, proof or network.
Saved files are checked as evidence, never imported to create owner authority.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "software/v5/ordinary_exact_extension"
LOCAL = ROOT / "experiments/v5-local-checks"
PACKAGE = LOCAL / "exact-module-assembly01/assembled/package"
OWNER = LOCAL / "concept-recipient-init-01"
SIDECAR = OWNER / "catalog/module-anchors-v1"
BUNDLE = LOCAL / "concept-theory-b-export-01/bundle"
PYTHON = Path(r"D:\Python314\python.exe")
LEAN = ROOT / "software/runtime/lean-4.34.0-windows"
HELPER = ROOT / "software/v5/ordinary_fair_search/assemble.py"
HELPER_SHA = "9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30"
PROFILE = "bde63019d1a6ac2bccd8e0c245a405ad3ca551d0606c01a5193fee6897c60346"
INSTALLATION = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
IMPLEMENTATION = "fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df"
SEMANTIC = "9108f44dba66e2a26a06f65566e143e3185e3f8237e156a4e5c826222a308ad7"
FOUNDATION = "884f408f0e7d647a1b72714cfa78685804dea9e07289a67176692cfbfe2c8282"
STORE = "dbaa21256e87cbbf12e1694e183b8d3d25c290af9c73da54395fa4e3923f6b09"
CONTEXT = "03de3aa800949731dfc0823d8661374c9f216262211c9bfe1ac6afd930421e20"
ANCHOR = "79db183e7c154929cb8aca320082854ddde304466a3dd901da071aac425f9325"
ANCHOR_SHA = "d0714947d7cd9259928d5782a0c10360a6dc3ff80efea057a561222121227005"
SUPPORT = "2edb66adf970b9436741d462ada285a4182886fc4382e04527ecd5579dd11231"
MANIFEST = "680cd98f8d1d31ef251b1e78b1cdae7a60bbe2b733e95193b0fe52cb9855c302"
CUSTODY_LIMITS_SHA = "abf5b2dc515a06691194c47e7a320a7fdeaedbbaa18ec45e074807649968ecbe"
TARGET_ID = "0be846200d7809eaa68cf06cf23ef362052d4d3f4a5db4892c7f369691393e83"
TARGET_EXPORT = "fb3598ea1e9b841c081a756f1aaeb144a1f4d7154ba5b9503644d5971017b20c"
UNREACHED = "cde627fdcccf8557e5a024aa6d11ad8d87ed5bdaa16dd9e1686dc5338f4c5503"
DELTA = set("""
0be846200d7809eaa68cf06cf23ef362052d4d3f4a5db4892c7f369691393e83
316faac92e6c291b008e45400ff2dc02ac14387aa4125c485c9559926a1dc8bd
334dc29ffdcbfec4c81821219c012a6cf75eae5275fcfaf21ebb4802eda85b47
3c6910cd23fbe1b3fc25f59c5bc9725d85be376ce3706f3d9f19042fc4926cc1
403dd4d8878342f863c80ee40311a1829a3bf94c59a003d68ddd524ede5f35b9
4e5d75835deffefd244162b5e4b8a4506d379789ab24ede3e437ff68bff42495
5e2cc02e6782bb25c8e4762e1d05e2bf173eb3b83c16341de10df5be1e1e6828
6c1c048c551a8adf702becc62de810104f6f9d9b797cb5ed19c3b19bbf602651
74ca5a6c5da73bb4b508c7c4f5c54bc37bb84001c1a981d2db4e0f2fed2a0248
7c2ee3b4d6cddfef885a3f9c3e50ad5633839b04d557a1f035779a2fe3369ad7
855f65751bd4aff4ab5a3277e26075740d793399c1779f67f6911155cd0934a0
97db919ff949e12703421c851ff2ca7d49384c2a6fcabbb8f0ec4c69f210e039
983ef00fc799290ca801fed6b289f86fc29e14ed89f336512512f56a4d762dc0
9f4613c9d45a69e9cf3b5567c9a30a246bfb0f78a833b6fddd4381d23ed6e1f2
a0b29aaae8fa06706da67ff08a11c93b20dad19944e8d3fffc1ae7a6b3fa5aa3
ad7ee98ecdd54e60be2572b4ae53cd04f9cc8cbb817142fba6b72dc6ab5c7c11
b8ed61f423a062172fe69ae86558a7bbe33a8d72c873ebe88024f7474cfab792
bfe6f58604a6d2341a87cdcda0c45a43e036218146d4e2f05ec7e73b276ff339
c310159d9971e37a1f1ee7c7130c5090414cca3d76b46fa2fb78acd1c3a1941b
d22cd00ddae13d7300e4a581f2c078d94bdf839cca55dbe168463f85d2c4d3a2
d56252db145686f8fb17bae7311d6c88646ecf0a246b569dfdd4e87d0ea29d65
dd459cf984e8ebc10b1696c0e56d12032acd710b52e271c5104c474456acffaa
e03bb18c1b79317fc108c6d7083a21e6e7731540bdbfec565b7f2c7015855f62
edd2a3f9f35c68d05d662f5c5b1261053c3efe07328cb236b826b1426d3464b2
f0ad4098cb62dcac9bd4ded30d58e5d9fda8fe4f5d38ed9755ceccf91051fa0e
f89cb0b045313cb2bc102d7b063100024e55218f628a1b0c81e13bed8299ddb3
""".split())
EVENTS = {"request.json", "inventory.json", "anchor-plan.json", "native-report.json",
          "native-report.json.pending", "native-report.json.phases.jsonl", "SUPERVISION.json"}
SUFFIXES = (".olean", ".olean.server", ".olean.private", ".ir.sig", ".ir")
MIB = 1024**2
START, CPU = time.monotonic(), time.process_time()


def need(ok, code):
    if not ok:
        raise ValueError("EXACT_EXTENSION_" + code)


def check():
    need(time.monotonic()-START < 160 and time.process_time()-CPU < 20, "ALLOWANCE")


def name(text):
    return [[0, {"$bytes": list(part.encode("ascii"))}] for part in text.split(".")]


def load(module_name, path, raw):
    need(module_name not in sys.modules, "MODULE_ALREADY_LOADED")
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("package", "profile-sha256", "custody-limits", "output"):
        parser.add_argument("--"+key, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and Path(sys.executable) == PYTHON and
         sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and
         not sys.flags.optimize, "EXECUTION_PROFILE")
    helper_raw = HELPER.read_bytes()
    need(hashlib.sha256(helper_raw).hexdigest() == HELPER_SHA, "HELPER_PIN")
    H = load("_exact_extension_files", HELPER, helper_raw)
    output = H.ordinary(Path(args.output), directory=True, fresh=True)
    need(output.parent.parent == LOCAL and output.name == "extension" and
         H.ordinary(Path(args.package), directory=True) == PACKAGE and
         args.profile_sha256 == PROFILE, "SELECTED_PATHS")
    limits_path = H.ordinary(Path(args.custody_limits))
    for protected in (PACKAGE, OWNER, BUNDLE, LEAN, PYTHON.parent, HERE, limits_path):
        need(not output.is_relative_to(protected) and not protected.is_relative_to(output), "OUTPUT_OVERLAP")
    pins = {}

    def selected(path, expected=None, maximum=128*MIB):
        check()
        if H.ordinary(path).stat().st_size == 0:
            with path.open("rb") as stream:
                need(stream.read(1) == b"", "EMPTY_FILE_CHANGED")
            actual = {"bytes": 0, "sha256": H.digest(b"")}
        else:
            actual = H.pin(path, check, maximum)
        if expected is not None:
            need(actual == expected if type(expected) is dict else
                 actual["sha256"] == expected, "PIN:"+str(path))
        need(path not in pins or pins[path] == actual, "CHANGED:"+str(path))
        pins[path] = actual
        return actual

    def document(path, expected=None):
        pin = selected(path, expected, 2*MIB)
        return H.read_json(path, pin["sha256"], check)[0]

    def census(directory, expected=None):
        files, dirs, todo, entries = {}, set(), [H.ordinary(directory, directory=True)], 0
        while todo:
            for path in todo.pop().iterdir():
                check(); entries += 1
                need(entries <= 256, "CENSUS_BOUND")
                relative = H.relative(path.relative_to(directory).as_posix())
                if path.is_dir():
                    need(len(path.relative_to(directory).parts) <= 6, "CENSUS_DEPTH")
                    dirs.add(relative); todo.append(H.ordinary(path, directory=True))
                else:
                    files[relative] = selected(path)
        want_dirs = {p.as_posix() for f in files for p in Path(f).parents if p != Path(".")}
        need(dirs == want_dirs and (expected is None or set(files) == set(expected)), "EXACT_CENSUS")
        return files

    selected(HELPER, HELPER_SHA)
    own = selected(HERE / "test_extension.py")
    need(selected(Path(__file__).absolute()) == own, "RUNNING_SOURCE")
    selected(HERE / "PLAN.md")
    selected(limits_path, CUSTODY_LIMITS_SHA)
    profile = document(PACKAGE / "PROFILE.json", PROFILE)
    need(profile["installation_manifest_sha256"] == INSTALLATION, "INSTALLATION")
    installed = document(PACKAGE / "installation/INSTALLATION.json", INSTALLATION)
    for logical, pin in profile["files"].items():
        selected(PACKAGE / H.relative(logical), pin)
    for logical, pin in installed["files"].items():
        H.relative(logical)
        path = (PYTHON.parent / logical.split("/", 1)[1] if logical.startswith("python_runtime/") else
                LEAN / logical.split("/", 1)[1] if logical.startswith("lean_runtime/") else
                PACKAGE / "installation" / logical)
        selected(path, pin)
    H.census(PACKAGE / "authoring/helpers", {p.removeprefix("authoring/helpers/")
        for p in profile["files"] if p.startswith("authoring/helpers/")}, check)
    for module_name in ("ordinary_evidence", "ordinary_semantics"):
        path = PACKAGE / "installation/py" / (module_name+".py")
        pin = selected(path, installed["files"]["py/"+module_name+".py"])
        raw = path.read_bytes()
        need(len(raw) == pin["bytes"] and H.digest(raw) == pin["sha256"], "CODEC_READ_PIN")
        load(module_name, path, raw)  # Pinned stateless identity codecs only.
    S = sys.modules["ordinary_semantics"]
    parent_path = SIDECAR / "records" / (ANCHOR+".json")
    parent = document(parent_path, ANCHOR_SHA)
    need(parent["schema"] == "DMKN_LOCAL_MODULE_ANCHOR_V1" and
         parent["parent_anchor_id"] == "" and parent["support_id"] == SUPPORT and
         parent["source_context_root"] == CONTEXT and len(parent["units"]) == 10,
         "PARENT_RECORD")
    parent_ids = {u["unit_id"] for u in parent["units"]}
    parent_names = [r["name"] for u in parent["units"] for r in u["outputs"]]
    tags = [u["realization"] for u in parent["units"]]
    need(len(parent_ids) == 10 and len(parent_names) == 21 and tags.count("added") == 6 and
         tags.count("installed-exact-nontheorem") == 4 and UNREACHED in parent_ids and
         len(DELTA) == 26 and not parent_ids & DELTA, "PARENT_PARTITION")
    prior = census(SIDECAR)
    need(len(prior) == 16, "PRIOR_SIDECAR_SIXTEEN")
    manifest = document(BUNDLE / "manifest.json", MANIFEST)
    manifest_units = {r["unit_id"]: r for batch in manifest["batches"] for r in batch}
    units, evidence_bytes = {}, 0
    for identity in sorted(DELTA):
        pin = manifest_units[identity]
        units[identity] = document(BUNDLE / "units" / (identity+".json"),
            {"bytes": pin["raw_bytes"], "sha256": pin["raw_sha256"]})["unit"]
        evidence_bytes += pin["raw_bytes"]
    target = {"name": name("RepairTheory.ClosureBridge.same_constraints_same_run"),
              "unit_id": TARGET_ID, "export_id": TARGET_EXPORT}
    need(evidence_bytes == 212098 and units[TARGET_ID][2][0][0] == target["name"] and
         S.export_id(SEMANTIC, TARGET_ID, target["name"]) == TARGET_EXPORT, "EXACT_TARGET")
    output.mkdir()
    completed, phase = False, "PUBLIC_CALL"
    try:
        H.fresh_bytes(output / "PRIOR-SIDECAR.json", H.canonical(prior))
        H.fresh_bytes(output / "targets.json", H.canonical([target]))
        module_dir = output / "module"
        argv = [str(PYTHON), "-I", "-S", "-B", str(PACKAGE / "owner.py"), "export-module",
            "--profile-sha256", PROFILE, "--python-runtime", str(PYTHON.parent), "--lean-runtime", str(LEAN),
            "--wall-seconds", "120", "--cpu-seconds", "70", "--memory-mib", "1536",
            "--catalog", str(OWNER / "catalog"), "--custody", str(OWNER / "custody"),
            "--store-id", STORE, "--custody-limits", str(limits_path), "--parent-root", CONTEXT,
            "--module-targets", str(output / "targets.json"), "--module-anchor", ANCHOR,
            "--output", str(module_dir)]
        H.fresh_bytes(output / "COMMAND.json", H.canonical({"argv": argv, "cwd": str(ROOT)}))
        with (output / "stdout.json").open("xb") as out, (output / "stderr.txt").open("xb") as err:
            code = subprocess.call(argv, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=out,
                                   stderr=err, creationflags=subprocess.CREATE_NO_WINDOW)
        need(code == 0 and H.ordinary(output / "stderr.txt").stat().st_size == 0, "OWNER_FAILED")
        phase = "EVIDENCE"
        response = document(output / "stdout.json")
        need(response["ok"] is True and response["operation"] == "export-module" and
             response["catalog"] == str(OWNER / "catalog") and
             response["custody"] == str(OWNER / "custody") and
             response["store_id"] == STORE and response["profile_sha256"] == PROFILE and
             response["implementation_id"] == IMPLEMENTATION and
             response.get("close_errors", []) == [], "OWNER_RESPONSE")
        cost = response["cost"]
        need(all(type(cost[k]) in (int, float) and math.isfinite(cost[k]) and cost[k] >= 0
                 for k in ("wall_seconds", "controller_cpu_seconds", "worker_cpu_seconds")) and
             cost["wall_seconds"] <= 120 and
             cost["controller_cpu_seconds"]+cost["worker_cpu_seconds"] <= 70, "OWNER_FINAL_BUDGET")
        result = response["result"]
        module = document(module_dir / "MODULE.json")
        need({k: v for k, v in result.items() if k not in {"manifest_path", "supported_runtime"}} == module and
             result["manifest_path"] == str(module_dir / "MODULE.json") and result["supported_runtime"] == {
                "claim": "EXACT_SELECTED_LOCAL_RUNTIME_NOT_DOWNSTREAM_PROJECT_VALIDATION",
                "implementation_id": IMPLEMENTATION, "installation_manifest_sha256": INSTALLATION,
                "lean_executable": str(LEAN / "bin/lean.exe"), "lean_runtime": str(LEAN),
                "lean_executable_pin": installed["files"]["lean_runtime/bin/lean.exe"]}, "MODULE_RESPONSE")
        selection = document(module_dir / "SELECTION.json")
        request = document(module_dir / "request.json")
        plan = document(module_dir / "anchor-plan.json")
        report = document(module_dir / "native-report.json", module["report_sha256"])
        selected(module_dir / "inventory.json", installed["files"]["foundation/inventory.json"])
        ordered = request["unit_ids"]
        cuts = sorted(parent_ids - {UNREACHED})
        need(len(ordered) == 26 and set(ordered) == DELTA and request["units"] == [units[i] for i in ordered] and
             module["ordered_unit_ids"] == selection["ordered_unit_ids"] == ordered and
             module["cut_unit_ids"] == selection["cut_unit_ids"] == cuts and
             module["fetch_calls"] == selection["fetch_calls"] == 26 and
             selection["acquired_bytes"] == 212098 and selection["acquired_nodes"] == 4376, "DELTA")
        parent_parts = [{"bytes": p["bytes"], "sha256": p["sha256"],
                         "path": str(SIDECAR / H.relative(p["path"]))} for p in parent["artifact_parts"]]
        need(plan == {"schema": "DMKN_LOCAL_MODULE_ANCHOR_PLAN_V1", "anchor_id": ANCHOR,
             "support_id": SUPPORT, "bindings": parent["units"], "modules": [{"anchor_id": ANCHOR,
                "module_name": parent["module_name"], "direct_imports": parent["direct_imports"],
                "added_names": parent["added_names"], "artifact_parts": parent_parts}]}, "FULL_PARENT_PLAN")
        for role, filename in (("request", "request.json"), ("inventory", "inventory.json"),
                               ("anchor_plan", "anchor-plan.json")):
            need(selection["input_pins"][role] == pins[module_dir / filename], "INPUT_PINS")
        key_input = {"support_id": SUPPORT, "parent_anchor_id": ANCHOR, "targets": [target]}
        key = H.digest(b"DMKN-ORDINARY-ANCHORED-MODULE-V1\0" + H.canonical(key_input))
        module_text = "DMKNBridge_"+key
        need(selection["key_input"] == key_input and selection["cache_key"] == module["cache_key"] == key and
             selection["source_context_root"] == CONTEXT and selection["anchor_id"] == ANCHOR and
             request == {"schema": "DMKN_ORDINARY_MODULE_REQUEST_V2", "semantic_id": SEMANTIC,
                "foundation_id": FOUNDATION, "context_root": CONTEXT, "module_name": name(module_text),
                "targets": [target["name"]], "unit_ids": ordered, "units": [units[i] for i in ordered],
                "anchor_id": ANCHOR, "anchor_plan_sha256": pins[module_dir / "anchor-plan.json"]["sha256"]},
             "REQUEST_BINDING")
        need(module["status"] == "CHECKED_AND_REGISTERED_LOCAL_MODULE_ANCHOR" and
             module["policy"] == "ORDINARY_EXACT_INSTALLED_PUBLIC_MODULE_V2" and module["native_calls"] == 1 and
             module["source_context_root"] == CONTEXT and module["parent_anchor_id"] == ANCHOR and
             module["semantic_id"] == SEMANTIC and module["foundation_id"] == FOUNDATION and
             module["targets"] == [target] and module["module_name"] == module_text and
             module["new_catalog_acceptance"] is False, "MODULE_IDENTITY")
        need(report["schema"] == "DMKN_ORDINARY_MODULE_OUTPUT_V3" and report["assurance"] ==
             "LOCAL_CHECKED_ANCHORED_MODULE_CONTROLLER_BOUND_IDENTITIES" and report["checking_passes"] == 2 and
             report["basis_rows"] == 581 and report["anchor_names"] == parent_names and
             report["direct_imports"] == [parent["module_name"]] and
             all(report[k] == request[k] for k in ("semantic_id", "foundation_id", "context_root",
                 "module_name", "targets", "unit_ids", "anchor_id", "anchor_plan_sha256")), "NATIVE_BINDING")
        matched = report["matched_unit_indices"]
        need(type(matched) is list and all(type(i) is int and 0 <= i < 26 for i in matched) and
             matched == sorted(set(matched)) and len(matched) < 26, "MATCHED_INDICES")
        added_rows = [r for i, u in enumerate(request["units"]) if i not in matched for r in u[2]]
        matched_rows = [r for i, u in enumerate(request["units"]) if i in matched for r in u[2]]
        rows = [r for u in request["units"] for r in u[2]]
        need(report["inventories"] == rows and report["names"] == [r[0] for r in rows] and
             report["added_inventories"] == added_rows and report["matched_inventories"] == matched_rows and
             report["units_checked"] == module["units_checked"] == 26-len(matched) and
             report["units_matched"] == module["units_matched"] == len(matched) and
             module["matched_unit_indices"] == matched and
             report["added_names"] == module["added_names"] == [r[0] for r in added_rows] and
             report["matched_names"] == module["matched_names"] == [r[0] for r in matched_rows], "ACTUAL_PARTITION")
        pending = document(module_dir / "native-report.json.pending")
        need(pending["schema"] == "DMKN_ORDINARY_MODULE_PENDING_V3" and pending["assurance"] ==
             "LOCAL_CHECKED_ANCHORED_MODULE_PENDING_REREADS" and
             dict(pending, schema=report["schema"], assurance=report["assurance"]) == report, "PENDING_PROMOTION")
        trace_path = module_dir / "native-report.json.phases.jsonl"
        selected(trace_path, maximum=65536)
        trace = [json.loads(line) for line in trace_path.read_bytes().splitlines()]
        need(trace == [{"schema": "DMKN_ORDINARY_MODULE_PHASE_TRACE_V1", "phase": p,
                       "event": event, "exit_code": code} for p in ("build", "reread-private", "reread-exported")
                      for event, code in (("STARTED", None), ("EXITED", 0))], "FRESH_NATIVE_PHASES")
        supervision = document(module_dir / "SUPERVISION.json")
        job = supervision["final_job"]
        need(supervision["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and
             supervision["child_exit_code"] == 0 and supervision["direct_child_reaped"] is True and
             supervision["job_closed"] is True and supervision["cleanup_errors"] == [] and
             supervision["termination_requested"] is False and job["active_processes"] == 0 and
             job["terminated_processes"] == 0 and
             job["cpu_seconds"] == module["native_cpu_seconds"] == response["cost"]["worker_cpu_seconds"],
             "NATIVE_CLOSURE")
        allowance = supervision["limits"]
        need(allowance["memory_mib"] == 1536 and allowance["active_processes"] == 4 and
             1 <= allowance["wall_seconds"] < 120 and 1 <= allowance["cpu_seconds"] < 70 and
             allowance["stdout_bytes"] == allowance["stderr_bytes"] == MIB, "NONRENEWED_NATIVE_LIMITS")
        measured = ((job["cpu_seconds"], allowance["cpu_seconds"]),
                    (supervision["wall_seconds_through_cleanup"], allowance["wall_seconds"]),
                    (job["peak_job_private_commit_bytes"], allowance["memory_mib"]*MIB))
        need(all(type(value) in (int, float) and math.isfinite(value) and 0 <= value <= cap
                 for value, cap in measured), "NATIVE_ACTUAL_RESOURCE_FIT")
        expected_argv = [str(PYTHON), "-I", "-S", "-B", str(PACKAGE / "module_worker.py"),
            str(LEAN / "bin/lean.exe"), str(PACKAGE / "module/OrdinaryModule.lean"),
            os.pathsep.join(str(PACKAGE / p) for p in profile["helper_paths"]), str(LEAN),
            str(module_dir / "inventory.json"), str(module_dir / "request.json"),
            str(module_dir / "anchor-plan.json"), str(module_dir / "modules" / (module_text+".olean")),
            str(module_dir / "native-report.json")]
        need(supervision["argv"] == expected_argv and supervision["cwd"] == str(module_dir) and
             document(module_dir / "supervision/command.json") ==
             {"argv": expected_argv, "cwd": str(module_dir), "limits": allowance} and
             supervision["observed_logs"] == {"stdout_bytes": 0, "stderr_bytes": 0}, "NATIVE_COMMAND")
        for filename in ("stdout.txt", "stderr.txt"):
            need(H.ordinary(module_dir / "supervision" / filename).stat().st_size == 0, "NATIVE_LOG")
        phase = "REGISTERED_CHILD"
        child_id = H.hexid(module["anchor_id"])
        need(child_id != ANCHOR, "NEW_CHILD_ID")
        child_path = SIDECAR / "records" / (child_id+".json")
        child = document(child_path)
        need(H.digest(b"DMKN-LOCAL-MODULE-ANCHOR-V1\0"+child_path.read_bytes()) == child_id, "CHILD_RECORD_ID")
        operation = H.hexid(child["operation_id"])
        op_rel = "operations/"+operation
        child_units = [{"unit_id": identity, "realization": "added" if i not in matched else
                       "installed-singleton-theorem" if unit[2][0][1] == 2 else "installed-exact-nontheorem",
                       "outputs": [{"name": r[0], "export_id": S.export_id(SEMANTIC, identity, r[0]),
                           "kind": r[1], "level_params": r[2], "inventory_sha256": H.digest(H.canonical(r))}
                           for r in unit[2]]} for i, (identity, unit) in enumerate(zip(ordered, request["units"]))]
        parts = []
        need(set(module["artifact_parts"]) == {module_text+s for s in SUFFIXES}, "ARTIFACT_NAMES")
        for suffix in SUFFIXES:
            filename = module_text+suffix
            pin = selected(module_dir / "modules" / filename, module["artifact_parts"][filename], 64*MIB)
            relative = op_rel+"/modules/"+filename
            selected(SIDECAR / relative, pin, 64*MIB)
            parts.append(dict(pin, path=relative))
        need(report["artifact_parts"] == [{"path": str(module_dir / "modules" / (module_text+s)),
             "bytes": module["artifact_parts"][module_text+s]["bytes"]} for s in SUFFIXES], "REPORT_PARTS")
        event_pins = {}
        for filename in EVENTS:
            pin = selected(module_dir / filename, maximum=8*MIB)
            relative = op_rel+"/events/"+filename
            selected(SIDECAR / relative, pin, 8*MIB)
            event_pins[filename] = dict(pin, path=relative)
        need(child == {"schema": parent["schema"], "store_binding": parent["store_binding"],
            "support_id": SUPPORT, "operation_id": operation, "source_context_root": CONTEXT,
            "parent_anchor_id": ANCHOR, "module_name": name(module_text), "direct_imports": [parent["module_name"]],
            "targets": [target], "materialization_key": key, "artifact_parts": parts, "units": child_units,
            "added_names": report["added_names"], "matched_names": report["matched_names"],
            "event_files": event_pins}, "EXACT_CHILD_RECORD")
        expected_dirs = [str(Path(parent_parts[0]["path"]).parent), str(SIDECAR / op_rel / "modules")]
        need(module["import_directories"] == expected_dirs and module["module_directory"] == expected_dirs[-1],
             "TWO_MEMBER_CHAIN")
        need(document(SIDECAR / op_rel / "RESERVATION.json") == {
            "schema": "DMKN_LOCAL_MODULE_RESERVATION_V1", "operation_id": operation,
            "store_binding": parent["store_binding"], "support_id": SUPPORT, "parent_anchor_id": ANCHOR,
            "selection": {"source_context_root": CONTEXT, "targets": [target], "materialization_key": key,
                          **selection["input_pins"]}}, "RESERVATION")
        need(document(SIDECAR / op_rel / "CLOSED.json") == {
            "schema": "DMKN_LOCAL_MODULE_OPERATION_CLOSED_V1", "operation_id": operation,
            "store_binding": parent["store_binding"], "reason": "LIVE_GENERATION_CLEAN_BEFORE_COMMIT"}, "CLOSED")
        expected_new = {"records/"+child_id+".json", op_rel+"/RESERVATION.json", op_rel+"/CLOSED.json"}
        expected_new.update(p["path"] for p in parts)
        expected_new.update(p["path"] for p in event_pins.values())
        after = census(SIDECAR, set(prior) | expected_new)
        need(len(expected_new) == 15 and len(after) == 31 and
             all(after[p] == pin for p, pin in prior.items()), "PRIOR_SIDECAR_PRESERVED")
        phase = "FINAL_PINS"
        module_files = EVENTS | {"MODULE.json", "SELECTION.json", "supervision/command.json",
                               "supervision/stdout.txt", "supervision/stderr.txt"}
        module_files |= {"modules/"+module_text+s for s in SUFFIXES}
        census(module_dir, module_files)
        root_files = {"PRIOR-SIDECAR.json", "targets.json", "COMMAND.json", "stdout.json", "stderr.txt"}
        root_files |= {"module/"+p for p in module_files}
        census(output, root_files)
        for path, pin in tuple(pins.items()):
            selected(path, pin)
        H.fresh_bytes(output / "PINS.json", H.canonical({str(path): pin for path, pin in pins.items()}))
        summary = {"status": "PASS_EXACT_ANCHORED_EXTENSION", "response": response,
            "parent_anchor_id": ANCHOR, "child_anchor_id": child_id, "delta_units": 26,
            "acquired_bytes": 212098, "cut_unit_ids": cuts, "parent_units": 10, "parent_names": 21,
            "prior_sidecar_files_unchanged": 16, "registered_chain_units": 36,
            "checking_passes": 2, "native_phases": trace, "native_supervision": supervision,
            "wall_seconds": time.monotonic()-START, "controller_cpu_seconds": time.process_time()-CPU,
            "claim": "ONE_LOCAL_ANCHOR_EXTENSION_NOT_NEW_MATHEMATICS_OR_GROWTH",
            "outer_closure": "REQUIRES_ROOT_RUNNER_RESULT_AND_INDEPENDENT_OUTCOME"}
        raw = H.canonical(summary)
        H.fresh_bytes(output / ".RESULT.pending", raw)
        need(H.pin(output / ".RESULT.pending", check, 2*MIB) ==
             {"bytes": len(raw), "sha256": H.digest(raw)}, "RESULT_READBACK")
        census(output, root_files | {"PINS.json", ".RESULT.pending"})
        check(); H.ordinary(output / "RESULT.json", fresh=True)
        (output / ".RESULT.pending").rename(output / "RESULT.json")
        completed = True
        print(json.dumps({"status": summary["status"], "anchor_id": child_id}), flush=True)
    except BaseException as error:
        if not completed:
            try:
                H.fresh_bytes(output / "FAILURE.json", H.canonical({"phase": phase,
                    "error_type": type(error).__name__, "error": str(error)[:2000],
                    "retention": "PRESERVED_NO_RETRY_NO_NEW_ALLOWANCE"}))
            except BaseException:
                pass
        raise


if __name__ == "__main__":
    main()
