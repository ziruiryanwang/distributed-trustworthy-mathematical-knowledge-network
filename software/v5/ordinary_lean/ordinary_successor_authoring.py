"""One owner-invoked successor above an already checked acquired method.

Caller opens the installed core and selects/pins these auxiliary helpers,
template, retained compiler helpers and frozen author-worker script. This
function neither opens/copies/initializes a catalog nor starts a network role.
Only OrdinaryAdmission.admit grants the new mathematical warrant. Every output
is fresh; accepted state and partial evidence survive later publication failure.
"""
from pathlib import Path
import json
import math
import os
import time

import ordinary_admission as A
import portable_owner_request as R
import portable_candidate as B
import portable_preview as PP

E, P, S, PE, need = A.E, A.P, A.S, A.PE, A.need
MIB = 1024**2
SUCCESSOR = "DMKN.PortableMethod.stable_threefold"


def author_successor(owner, parent_root, discovered_target, *, output_directory,
                     template_path, helper_paths, author_worker_script,
                     parent_deadline, make_budget, account_worker_cpu, check_parent):
    """Use open B and its custody; return JSON-compatible new contribution data.

    discovered_target is exactly {name, export_id, unit_id}. make_budget()
    supplies a fresh one-use OperationBudget from the caller's remaining parent
    allocation. account_worker_cpu(seconds) charges the caller's shared native
    CPU ledger, including on refused events. check_parent() guards that original
    wall/CPU allocation. These are trusted owner callbacks, not peer authority.
    The caller retains both owner and custody lifecycle responsibilities.
    """
    need(type(owner) is A.OrdinaryAdmission and type(parent_deadline) in (int, float)
         and math.isfinite(parent_deadline) and callable(make_budget)
         and callable(account_worker_cpu) and callable(check_parent), "SUCCESSOR_OWNER_CONFIGURATION")
    P.fields(discovered_target, ("name", "export_id", "unit_id"), "SUCCESSOR_DISCOVERED_TARGET")
    target_name, target_id, target_unit = (discovered_target[key] for key in ("name", "export_id", "unit_id"))
    target_key = E.name_key(target_name)
    A.C.hexid(target_id); A.C.hexid(target_unit)
    installation, custody = owner.installation, owner.evidence_store
    need(S.export_id(installation.semantic_id, target_unit, target_name) == target_id,
         "SUCCESSOR_DISCOVERED_EXPORT_BINDING")
    started = time.monotonic()
    current = None

    def check():
        check_parent()
        need(time.monotonic() < parent_deadline, "SUCCESSOR_PARENT_DEADLINE")
        if current is not None:
            current.check()

    def operation():
        check_parent()
        value = make_budget()
        need(type(value) is A.OperationBudget and not value.claimed and value.worker_cpu == 0
             and value.deadline <= parent_deadline, "SUCCESSOR_REMAINING_OPERATION_BUDGET")
        value.check()
        return value

    current = operation()  # Request preparation is inside the authoring allocation.
    check()
    output = A.C.ordinary(Path(output_directory), directory=True, fresh=True)
    output.mkdir()

    def save(name, value):
        raw = value if type(value) is bytes else json.dumps(
            value, sort_keys=True, ensure_ascii=True, allow_nan=False, indent=2).encode("ascii")
        P.PortableCatalog._write_fresh(output/name, raw)
        return {"bytes": len(raw), "sha256": A.sha(raw)}

    phase, accepted, native_cpu = "REQUEST", None, 0.0
    try:
        context = owner.catalog.context(parent_root)
        check()
        need(context["bindings"].get(target_key) == target_id, "SUCCESSOR_TARGET_NOT_WARRANTED")
        helpers = [A.C.ordinary(Path(path), directory=True) for path in helper_paths]
        need(1 <= len(helpers) <= 8 and len(set(helpers)) == len(helpers), "SUCCESSOR_HELPER_PATHS")
        worker = A.C.ordinary(Path(author_worker_script))
        template = A.C.read_bounded(A.C.ordinary(Path(template_path)), MIB)
        request_dir, source_dir, build_dir = (output/part for part in ("owner-request", "owner-source", "lean-build"))
        for path in (request_dir, source_dir, build_dir):
            A.C.ordinary(path, directory=True, fresh=True).mkdir()
        fetched = []

        def warranted(name):
            check()
            return context["bindings"].get(E.name_key(name))

        def evidence(name, identity):
            check()
            need(warranted(name) == identity, "SUCCESSOR_EVIDENCE_NOT_WARRANTED")
            locator = PP.read_locator(E.strict_json(custody.get_locator(
                installation.semantic_id, identity, 4096, check_budget=check)))
            need(locator["semantic_id"] == installation.semantic_id and
                 E.name_key(locator["export_name"]) == E.name_key(name) and
                 S.export_id(installation.semantic_id, locator["unit_id"], name) == identity,
                 "SUCCESSOR_EXACT_LOCAL_LOCATOR")
            if identity == target_id:
                need(locator["unit_id"] == target_unit, "SUCCESSOR_DISCOVERED_UNIT_CHANGED")
            raw = custody.get_evidence(installation.semantic_id, locator["unit_id"], MIB,
                                      check_budget=check)
            item = PE.read_evidence(raw)
            need(item.unit_id == locator["unit_id"] and item.document["semantic_id"] == installation.semantic_id
                 and any(E.name_key(row[0]) == E.name_key(name) for row in item.document["unit"][2]),
                 "SUCCESSOR_EXACT_LOCAL_EVIDENCE")
            fetched.append({"name": name, "export_id": identity, "unit_id": item.unit_id,
                            "bytes": len(raw), "sha256": A.sha(raw)})
            check()
            return raw

        prepared = R.prepare(semantic_id=installation.semantic_id, foundation_id=S.foundation_id(),
            context_root=parent_root, inventory_raw=installation.read("inventory", MIB),
            targets=[[target_name, target_id]], warranted_symbol=warranted,
            fetch_evidence=evidence, owner_absent=lambda name: True,
            limits=R.Limits(max_groups=8, max_rows=4096, max_targets=1, max_group_bytes=MIB,
                max_payload_bytes=4*MIB, max_acquired_bytes=4*MIB,
                max_acquired_nodes=131072, max_edges=32768))
        header = E.strict_json(prepared.header, E.Limits(max_bytes=MIB))
        bindings = {E.name_key(row[1][0]): row[0] for row in header["basis_rows"]}
        request_pins = {"header.json": save("owner-request/header.json", prepared.header)}
        for index, raw in enumerate(prepared.groups):
            check()
            packet = E.strict_json(raw, E.Limits(max_bytes=MIB))
            for name, mode, identity, payload in packet[1]:
                key = E.name_key(name)
                need(key not in bindings and warranted(name) == identity, "SUCCESSOR_PREPARED_BINDING")
                bindings[key] = identity
            filename = f"group-{index:05d}.json"
            request_pins[filename] = save("owner-request/"+filename, raw)
        need(bindings.get(target_key) == target_id, "SUCCESSOR_PREPARED_TARGET")
        candidate = output/"candidate.json"
        generated = template
        for sentinel, value in {"__DMKN_REQUEST_DIRECTORY__": str(request_dir),
                "__DMKN_SEMANTIC_ID__": installation.semantic_id, "__DMKN_CONTEXT_ROOT__": parent_root,
                "__DMKN_FOUNDATION_ID__": S.foundation_id(), "__DMKN_CANDIDATE_OUTPUT__": str(candidate)}.items():
            need(value.isascii() and len(value) <= 32768 and all(ord(c) >= 32 for c in value),
                 "SUCCESSOR_LEAN_STRING")
            token = ('"'+sentinel+'"').encode("ascii")
            need(generated.count(token) == 1, "SUCCESSOR_TEMPLATE_SENTINEL:"+sentinel)
            generated = generated.replace(token, json.dumps(value).encode("ascii"))
        # Reuse the frozen producer shim's private output filename; no A module
        # is imported and this scratch artifact never enters B's native catalog.
        source = source_dir/"OrdinaryProducer.lean"
        source_pin = save("owner-source/OrdinaryProducer.lean", generated)
        save("REQUEST.json", {"parent_root": parent_root, "acquired_target": discovered_target,
            "request_files": request_pins, "groups": len(prepared.groups), "fetched": fetched,
            "payload_bytes": prepared.payload_bytes, "acquired_bytes": prepared.acquired_bytes,
            "template_sha256": A.sha(template), "generated_source": source_pin,
            "mathematical_acceptance": False})
        phase = "AUTHORING"
        check(); current.claim()
        argv = [str(installation.path("python")), "-I", "-S", "-B", str(worker), "--author-worker",
                str(installation.path("lean")), str(source), str(build_dir),
                os.pathsep.join(map(str, helpers)), str(candidate)]
        supervision = installation._supervisor.supervise(argv, output, output/"authoring-supervision",
            installation._supervisor.limits_checked(current.allowance(parent_deadline)), installation._job_module.Job)
        final_job = supervision.get("final_job")
        if type(final_job) is dict and type(final_job.get("cpu_seconds")) in (int, float):
            current.worker_cpu += final_job["cpu_seconds"]
            native_cpu += final_job["cpu_seconds"]
            account_worker_cpu(final_job["cpu_seconds"])
        save("AUTHORING-SUPERVISION.json", supervision)
        need(A._clean_worker(supervision), "SUCCESSOR_AUTHORING_NOT_CLEAN")
        need(A.C.ordinary(output/"authoring-supervision/stderr.txt").stat().st_size == 0,
             "SUCCESSOR_AUTHORING_STDERR")
        check()
        need(A.C.read_bounded(source, MIB) == generated, "SUCCESSOR_SOURCE_CHANGED")
        for filename, pin in request_pins.items():
            check()
            raw = A.C.read_bounded(request_dir/filename, MIB)
            need({"bytes": len(raw), "sha256": A.sha(raw)} == pin, "SUCCESSOR_REQUEST_CHANGED")
        current = operation()  # Parent ledger already includes authoring CPU.
        phase = "BINDING"
        successor_name = [[0, {"$bytes": list(part.encode("ascii"))}] for part in SUCCESSOR.split(".")]
        bound = B.bind_candidate(A.C.read_bounded(A.C.ordinary(candidate), 4*MIB),
            semantic_id=installation.semantic_id, foundation_id=S.foundation_id(), context_root=parent_root,
            expected_targets=[successor_name], prepared_bindings=bindings, warranted_symbol=warranted,
            check_budget=check, limits=B.Limits(max_bundle_bytes=4*MIB, max_units=8,
                max_bindings=4096, max_targets=1, max_total_nodes=131072, max_evidence_bytes=4*MIB))
        need(bound.status == "READY", "SUCCESSOR_CANDIDATE_NEEDS_INTERPRETATIONS")
        items = [PE.read_evidence(raw) for raw in bound.raw_units]
        need(any(any(E.name_key(name) == target_key and identity == target_id
                     for name, identity in item.document["imports"]) for item in items),
             "SUCCESSOR_ACQUIRED_METHOD_NOT_USED")
        plans = owner.preflight(parent_root, bound.raw_units, budget=current,
            limits=A.PreflightLimits(max_units=8, max_bytes=4*MIB, max_nodes=131072,
                                     max_names=4096, max_edges=32768))
        need(plans.status == "READY", "SUCCESSOR_PREFLIGHT_NEEDS")
        phase = "ADMISSION"
        try:
            accepted = owner.admit(parent_root, plans, current)
        finally:
            native_cpu += current.worker_cpu
            account_worker_cpu(current.worker_cpu)
        save("ADMISSION.json", accepted)
        need(accepted["status"] == "CHECKED" and accepted["units_checked"] == len(items),
             "SUCCESSOR_NEW_CHECK_REQUIRED")
        phase = "PUBLICATION_BYTES"
        check()
        selected = [item for item in items if any(E.name_key(row[0]) == E.name_key(successor_name)
                    for row in item.document["unit"][2])]
        need(len(selected) == 1, "SUCCESSOR_EXACT_OUTPUT_TARGET")
        preview = PP.preview_from_evidence(selected[0].raw, successor_name)
        PP.resolve(preview, selected[0].raw)
        custody.put_preview(preview, before_commit=check)
        preview_pin = save("preview.json", preview)
        need(custody.get_preview(preview_pin["sha256"], preview_pin["bytes"], check_budget=check) == preview,
             "SUCCESSOR_PREVIEW_CUSTODY_READBACK")
        unit_dir = A.C.ordinary(output/"evidence", directory=True, fresh=True)
        unit_dir.mkdir()
        units = [{"unit_id": item.unit_id, "file": str(unit_dir/(item.unit_id+".json")),
                  **save("evidence/"+item.unit_id+".json", item.raw)} for item in items]
        result = {"status": "CHECKED_SUCCESSOR_WITH_DURABLE_PUBLICATION_BYTES",
            "parent_root": parent_root, "local_root": accepted["local_root"],
            "semantic_id": installation.semantic_id, "implementation_id": installation.implementation_id,
            "target": {"name": successor_name, "unit_id": selected[0].unit_id,
                       "export_id": S.export_id(installation.semantic_id, selected[0].unit_id, successor_name)},
            "acquired_method": discovered_target, "units": units,
            "preview": {"file": str(output/"preview.json"), **preview_pin},
            "admission": accepted, "authoring_supervision": str(output/"AUTHORING-SUPERVISION.json"),
            "request_groups": len(prepared.groups), "request_acquired_bytes": prepared.acquired_bytes,
            "native_cpu_seconds": native_cpu, "wall_seconds": time.monotonic()-started,
            "claim": "LOCAL_CHECKED_SUCCESSOR_NOT_INDEX_PUBLICATION_OR_PEER_ACCEPTANCE"}
        check(); save("RESULT.json", result)
        return result
    except BaseException as error:
        save("FAILURE.json", {"phase": phase, "error_type": type(error).__name__, "error": str(error),
            "accepted": accepted, "native_cpu_seconds": native_cpu,
            "retention": "CALLER_OWNS_LIFECYCLE_ACCEPTED_STATE_AND_PARTIAL_OUTPUTS_PRESERVED"})
        raise
