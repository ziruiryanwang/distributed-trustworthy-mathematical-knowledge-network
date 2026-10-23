"""Selected owner A: installed basis -> ordinary source -> new checked units.

Root selects/pins this runner, auxiliary support, template and helper paths.
This is orchestration, not a checker or an importer. The installed public API
alone promotes native events. Fresh output persists on failure; no retry,
existing-store migration, network service, library replay or cleanup is implicit.
Run with the selected isolated Python (-I -S -B) under an outer hard supervisor.
Authoring source is owner-approved code; Windows Job containment is not a sandbox.
"""
from pathlib import Path
import argparse
import hashlib
import importlib
import json
import math
import os
import re
import subprocess
import sys
import time

MIB = 1024**2
CUSTODY_LIMITS = {"objects": 32, "exports": 128, "logical_bytes": 8*MIB, "db_pages": 4096}


def need(ok, code):
    if not ok:
        raise ValueError(code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    raw = value if type(value) is bytes else json.dumps(
        value, sort_keys=True, ensure_ascii=True, allow_nan=False, indent=2).encode("ascii")
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    return {"bytes": len(raw), "sha256": sha(raw)}


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ("output", "installation", "manifest-sha256", "python-runtime", "lean-runtime",
                "support-root", "helper-paths", "template", "target", "store-id"):
        parser.add_argument("--"+key, required=True)
    parser.add_argument("--basis-target", default="Eq")
    for key in ("wall-seconds", "cpu-seconds", "memory-mib"):
        parser.add_argument("--"+key, required=True, type=int)
    return parser.parse_args()


def author_worker(args):
    """Fixed local compile command inside the selected supervisor's child Job."""
    need(len(args) == 5 and os.name == "nt" and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "PRODUCER_AUTHOR_WORKER_PROFILE")
    lean, source, build, helpers_raw, candidate = args
    paths = [Path(lean), Path(source), Path(build), Path(candidate)]
    helpers = [Path(part) for part in helpers_raw.split(os.pathsep)]
    need(all(path.is_absolute() for path in [*paths, *helpers]) and 1 <= len(helpers) <= 8,
         "PRODUCER_AUTHOR_WORKER_PATHS")
    need(paths[0].is_file() and paths[1].is_file() and paths[2].is_dir() and
         all(path.is_dir() for path in helpers) and not os.path.lexists(paths[3]),
         "PRODUCER_AUTHOR_WORKER_INPUTS")
    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith(("LEAN", "PYTHON")) and key.upper() != "PATH"}
    env["LEAN_PATH"] = os.pathsep.join(map(str, helpers))
    env["PATH"] = os.pathsep.join((str(Path(sys.executable).parent), str(paths[0].parent)))
    argv = [lean, "-DElab.async=false", "-R", str(paths[1].parent),
            "-o", str(paths[2]/"OrdinaryProducer.olean"), source]
    return subprocess.call(argv, cwd=Path.cwd(), env=env, stdin=subprocess.DEVNULL,
                           creationflags=subprocess.CREATE_NO_WINDOW)


def run(args):
    started, cpu_started = time.monotonic(), time.process_time()
    need(60 <= args.wall_seconds <= 3600 and 4 <= args.cpu_seconds <= 200000 and
         1 <= args.memory_mib <= 8192, "PRODUCER_FINITE_ALLOCATION")
    deadline, native_cpu = started+args.wall_seconds, 0.0

    def live():
        need(time.monotonic() < deadline and
             time.process_time()-cpu_started+native_cpu < args.cpu_seconds,
             "PRODUCER_PARENT_BUDGET")

    # The actual installed modules must win over auxiliary workspace siblings.
    # NativeInstallation.open checks every loaded core file against its roles.
    installation_path = Path(args.installation)
    need(installation_path.is_absolute() and (installation_path/"py").is_dir(),
         "PRODUCER_INSTALLATION_PATH")
    sys.path.insert(0, str(installation_path/"py"))
    A = importlib.import_module("ordinary_admission")
    C, E, P, S, PE = A.C, A.E, A.P, A.S, A.PE
    install = A.NativeInstallation.open(installation_path,
        C.read_bounded(C.ordinary(installation_path/"INSTALLATION.json"), 2*MIB),
        args.manifest_sha256,
        runtime_roots={"python_runtime": Path(args.python_runtime), "lean_runtime": Path(args.lean_runtime)})
    live()
    output = C.ordinary(Path(args.output), directory=True)
    support = C.ordinary(Path(args.support_root), directory=True)
    ordinary_support = C.ordinary(support/"ordinary_lean", directory=True)
    # These selected helpers produce inert authoring data/custody, not acceptance.
    sys.path.extend((str(ordinary_support), str(support)))
    R = importlib.import_module("portable_owner_request")
    B = importlib.import_module("portable_candidate")
    O = importlib.import_module("transport.ordinary_acquisition")
    need(Path(R.__file__).resolve() == ordinary_support/"portable_owner_request.py" and
         Path(B.__file__).resolve() == ordinary_support/"portable_candidate.py" and
         Path(O.__file__).resolve() == support/"transport/ordinary_acquisition.py",
         "PRODUCER_SELECTED_AUXILIARY_SUPPORT")
    helpers = [C.ordinary(Path(part), directory=True) for part in args.helper_paths.split(os.pathsep)]
    need(1 <= len(helpers) <= 8 and len(set(helpers)) == len(helpers), "PRODUCER_HELPER_PATHS")
    template_path = C.ordinary(Path(args.template))
    template = C.read_bounded(template_path, MIB)
    C.hexid(args.store_id)
    limits = P.Limits(max_roots=8, max_operations=8, max_names=4096,
        max_manifest_bytes=2*MIB, max_artifact_bytes=64*MIB,
        max_total_artifact_bytes=128*MIB, max_db_pages=8192,
        max_batch_bytes=4*MIB, max_batch_units=8)
    save(output/"PRODUCER-INPUTS.json", {"schema": "DMKN_ORDINARY_API_PRODUCER_INPUTS_V1",
        "arguments": vars(args), "template_pin": {"bytes": len(template), "sha256": sha(template)},
        "implementation_id": install.implementation_id, "semantic_id": install.semantic_id,
        "foundation_id": S.foundation_id(), "catalog_limits": vars(limits),
        "custody_limits": CUSTODY_LIMITS,
        "support_authority": "EXACT_OWNER_SELECTION_REQUIRED_NOT_INFERRED_FROM_PATHS"})

    def directory(name):
        path = C.ordinary(output/name, directory=True, fresh=True)
        path.mkdir()
        return path

    def budget():
        live()
        wall = math.floor(deadline-time.monotonic())
        cpu = math.floor(args.cpu_seconds-(time.process_time()-cpu_started)-native_cpu)
        need(wall >= 30 and cpu >= 2, "PRODUCER_STAGE_REMAINING_ALLOCATION")
        result = A.OperationBudget(wall, cpu, args.memory_mib, output_bytes=64*MIB)
        # Narrowing never renews the enclosing original deadline.
        result.deadline = min(result.deadline, deadline)
        return result

    def encoded_name(text):
        need(type(text) is str and len(text) <= 512 and
             re.fullmatch(r"[A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)*", text),
             "PRODUCER_SELECTED_NAME")
        return [[0, {"$bytes": list(part.encode("ascii"))}] for part in text.split(".")]

    custody = owner = None
    phase = "INITIALIZATION"
    results = {}
    try:
        custody = O.OrdinaryStore(output/"custody", install.semantic_id, CUSTODY_LIMITS, create=True)
        owner = A.OrdinaryAdmission.open(install, output/"catalog", args.store_id,
                                        custody, create=True, limits=limits)
        current_budget = budget()
        try:
            results["basis"] = owner.initialize(current_budget)
        finally:
            native_cpu += current_budget.worker_cpu
        save(output/"BASIS-RESULT.json", results["basis"])
        parent = results["basis"]["local_root"]
        context = owner.catalog.context(parent)
        live()
        phase = "AUTHORING_REQUEST"
        request_dir, source_dir, build_dir = directory("owner-request"), directory("owner-source"), directory("lean-build")
        target, basis_target = encoded_name(args.target), encoded_name(args.basis_target)

        def warranted(name):
            live()
            return context["bindings"].get(E.name_key(name))

        basis_symbol = warranted(basis_target)
        need(basis_symbol is not None, "PRODUCER_BASIS_TARGET_ABSENT")

        def no_evidence(name, symbol):
            raise ValueError("PRODUCER_BASIS_ONLY_REQUEST_FETCH")

        prepared = R.prepare(semantic_id=install.semantic_id, foundation_id=S.foundation_id(),
            context_root=parent, inventory_raw=install.read("inventory", MIB),
            targets=[[basis_target, basis_symbol]], warranted_symbol=warranted,
            fetch_evidence=no_evidence, owner_absent=lambda name: False)
        need(not prepared.groups and not prepared.evidence_ids and prepared.acquired_bytes == 0,
             "PRODUCER_BASIS_ONLY_REQUEST")
        header = E.strict_json(prepared.header, E.Limits(max_bytes=MIB))
        prepared_bindings = {E.name_key(row[1][0]): row[0] for row in header["basis_rows"]}
        need(len(prepared_bindings) == 581 and header["group_count"] == 0,
             "PRODUCER_EXACT_BASIS_REQUEST")
        request_pin = save(request_dir/"header.json", prepared.header)
        candidate_path = output/"candidate.json"
        generated = template
        for sentinel, value in {
                "__DMKN_REQUEST_DIRECTORY__": str(request_dir),
                "__DMKN_SEMANTIC_ID__": install.semantic_id,
                "__DMKN_CONTEXT_ROOT__": parent,
                "__DMKN_FOUNDATION_ID__": S.foundation_id(),
                "__DMKN_CANDIDATE_OUTPUT__": str(candidate_path)}.items():
            # JSON and Lean agree on these explicitly bounded ASCII strings.
            need(value.isascii() and len(value) <= 32768 and all(ord(c) >= 32 for c in value),
                 "PRODUCER_LEAN_STRING")
            token = ('"'+sentinel+'"').encode("ascii")
            need(generated.count(token) == 1, "PRODUCER_TEMPLATE_SENTINEL:"+sentinel)
            generated = generated.replace(token, json.dumps(value, ensure_ascii=True).encode("ascii"))
        source_path = source_dir/"OrdinaryProducer.lean"
        source_pin = save(source_path, generated)
        save(output/"AUTHORING-INPUTS.json", {"request_header": request_pin,
            "generated_source": source_pin, "parent_root": parent,
            "targets": [target], "request_targets": [[basis_target, basis_symbol]],
            "helper_paths": list(map(str, helpers)), "group_count": 0,
            "mathematical_acceptance": False})
        phase = "AUTHORING_EXPORT"
        author_budget = budget()
        author_budget.claim()
        argv = [str(install.path("python")), "-I", "-S", "-B", str(Path(__file__).resolve()),
            "--author-worker", str(install.path("lean")), str(source_path), str(build_dir),
            os.pathsep.join(map(str, helpers)), str(candidate_path)]
        supervision = install._supervisor.supervise(argv, output, output/"authoring-supervision",
            install._supervisor.limits_checked(author_budget.allowance(deadline)), install._job_module.Job)
        final_job = supervision.get("final_job")
        if type(final_job) is dict and type(final_job.get("cpu_seconds")) in (int, float):
            native_cpu += final_job["cpu_seconds"]
        save(output/"AUTHORING-SUPERVISION.json", supervision)
        need(A._clean_worker(supervision), "PRODUCER_AUTHORING_EVENT_NOT_CLEAN")
        need(C.ordinary(output/"authoring-supervision/stderr.txt").stat().st_size == 0,
             "PRODUCER_AUTHORING_STDERR")
        live()
        need(C.read_bounded(request_dir/"header.json", MIB) == prepared.header and
             C.read_bounded(source_path, MIB) == generated, "PRODUCER_AUTHORED_INPUT_CHANGED")
        phase = "CANDIDATE_BINDING"
        contribution_budget = budget()  # Includes binding/preflight, never starts at native launch.
        raw = C.read_bounded(C.ordinary(candidate_path), 4*MIB)
        bound = B.bind_candidate(raw, semantic_id=install.semantic_id, foundation_id=S.foundation_id(),
            context_root=parent, expected_targets=[target], prepared_bindings=prepared_bindings,
            warranted_symbol=warranted, check_budget=contribution_budget.check,
            limits=B.Limits(max_bundle_bytes=4*MIB, max_units=8, max_bindings=4096,
                max_targets=1, max_total_nodes=131072, max_evidence_bytes=4*MIB))
        save(output/"CANDIDATE-BINDING.json", {"status": bound.status,
            "candidate_pin": {"bytes": len(raw), "sha256": sha(raw)},
            "missing_names": [E.strict_json(name) for name in bound.missing_names],
            "units": len(bound.raw_units), "looked_up_names": bound.looked_up_names,
            "total_nodes": bound.total_nodes, "mathematical_acceptance": False})
        need(bound.status == "READY", "PRODUCER_CANDIDATE_UNRESOLVED")
        evidence_dir, units = directory("evidence"), []
        for unit_raw in bound.raw_units:
            contribution_budget.check()
            item = PE.read_evidence(unit_raw)
            filename = item.unit_id+".json"
            pin = save(evidence_dir/filename, unit_raw)
            units.append({"unit_id": item.unit_id, "file": "evidence/"+filename, **pin,
                "exports": [{"name": row[0], "export_id": S.export_id(install.semantic_id, item.unit_id, row[0])}
                            for row in item.document["unit"][2]]})
        plan = owner.preflight(parent, bound.raw_units, budget=contribution_budget,
            limits=A.PreflightLimits(max_units=8, max_bytes=4*MIB, max_nodes=131072,
                                     max_names=4096, max_edges=32768))
        save(output/"PREFLIGHT.json", {"status": plan.status,
            "missing": [[E.strict_json(name), identity] for name, identity in plan.missing],
            "new_units": len(plan.ordered_units), "reused_unit_ids": list(plan.reused_unit_ids)})
        need(plan.status == "READY", "PRODUCER_PREFLIGHT_MISSING")
        phase = "CONTRIBUTION_ADMISSION"
        try:
            results["contribution"] = owner.admit(parent, plan, contribution_budget)
        finally:
            native_cpu += contribution_budget.worker_cpu
        save(output/"CONTRIBUTION-RESULT.json", results["contribution"])
        live()
        need(results["contribution"]["status"] == "CHECKED" and
             results["contribution"]["units_checked"] == len(units), "PRODUCER_NEW_CONTRIBUTION_REQUIRED")
        target_rows = [{"name": exported["name"], "export_id": exported["export_id"],
                        "unit_id": unit["unit_id"]}
                       for unit in units for exported in unit["exports"]
                       if E.name_key(exported["name"]) == E.name_key(target)]
        need(len(target_rows) == 1, "PRODUCER_EXACT_ACCEPTED_TARGET")
        state = {"schema": "DMKN_ORDINARY_API_OWNER_STATE_V1", "store_id": args.store_id,
            "installation": str(install.root), "installation_manifest_sha256": install.manifest_sha256,
            "implementation_id": install.implementation_id, "semantic_id": install.semantic_id,
            "foundation_id": S.foundation_id(), "catalog": str(output/"catalog"),
            "custody": str(output/"custody"), "catalog_limits": vars(limits),
            "custody_limits": CUSTODY_LIMITS, "basis_root": parent,
            "local_root": results["contribution"]["local_root"], "target": target_rows[0], "units": units,
            "request": {"directory": str(request_dir), "header": request_pin, "group_count": 0,
                        "authoring_inputs": str(output/"AUTHORING-INPUTS.json")},
            "authority": "LOCAL_STATE_POINTERS_NOT_TRANSFERABLE_WARRANTS"}
        save(output/"OWNER-STATE.json", state)
        phase = "COMPLETE"
        return {"status": "CHECKED_ORDINARY_SOURCE_CONTRIBUTION", "phase": phase,
            "basis_root": parent, "local_root": state["local_root"], "new_units": len(units),
            "native_cpu_seconds": native_cpu, "controller_cpu_seconds": time.process_time()-cpu_started,
            "known_cpu_seconds": native_cpu+time.process_time()-cpu_started,
            "wall_seconds": time.monotonic()-started,
            "claims": "NOT_DISCOVERY_PEER_ACCEPTANCE_GROWTH_OR_DEPLOYABLE_V5"}
    except BaseException as error:
        save(output/"PRODUCER-FAILURE.json", {"status": "FAILED", "phase": phase,
            "error_type": type(error).__name__, "error": str(error),
            "completed_stages": results, "native_cpu_seconds": native_cpu,
            "controller_cpu_seconds": time.process_time()-cpu_started,
            "wall_seconds": time.monotonic()-started,
            "retention": "PARTIAL_STATE_PRESERVED_NO_RETRY"})
        raise
    finally:
        if owner is not None:
            owner.close()
        if custody is not None:
            custody.close()


def main():
    args = parse_args()
    result = run(args)
    save(Path(args.output)/"PRODUCER-RESULT.json", result)
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == "__main__":
    if sys.argv[1:2] == ["--author-worker"]:
        raise SystemExit(author_worker(sys.argv[2:]))
    main()
