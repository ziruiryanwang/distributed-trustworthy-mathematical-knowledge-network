"""Complete retained inert authoring output through ordinary local admission.

No source is executed, no parent is copied/rebased, and no compiler success flag
grants authority. A caller explicitly selects the original candidate, target and
prepared-binding data, and a proof-complete supplement for its missing names.
Only the unchanged ordinary receiver can accept the combined new declarations.
This API does not acquire or extract the supplement, nor publish to an index.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
import time

import ordinary_admission as A
import ordinary_contribution as G
import portable_candidate as B
import portable_preview as PP
import library_completion as L

MIB = 1024**2


def complete_source(owner, parent_root, candidate_raw, supplement_raw, *,
                    expected_targets, prepared_bindings, output_directory,
                    parent_deadline, make_budget, account_worker_cpu, check_parent):
    """Check one combined batch without repeating successful authoring.

    Inputs are explicit owner selections, not authentication by file name or by
    a remote success report. Each originally claimed identity must still match
    both its prepared binding and the real selected protected context. Supplying
    different input bytes or a different parent is a new caller operation.

    Caller owns the open owner/custody and exclusive lifecycle. Budget callbacks
    derive from one original allowance (including any earlier extraction), not
    a replenished grant. The selected package/OS/storage are trusted; cooperative
    controller checks need an external supervisor for hard process containment.
    """
    A.need(type(owner) is A.OrdinaryAdmission and G.A is A and
           type(parent_deadline) in (int, float) and math.isfinite(parent_deadline)
           and callable(make_budget) and callable(account_worker_cpu) and
           callable(check_parent), "COMPLETION_OWNER_CONFIGURATION")
    A.C.hexid(parent_root)
    installation, custody = owner.installation, owner.evidence_store
    started = time.monotonic()
    budget = output = accepted = None
    phase, native_cpu = "INPUTS", 0.0

    def check():
        check_parent()
        A.need(time.monotonic() < parent_deadline, "COMPLETION_PARENT_DEADLINE")
        if budget is not None:
            budget.check()

    def save(name, value):
        raw = value if type(value) is bytes else json.dumps(value, sort_keys=True,
            ensure_ascii=True, allow_nan=False, indent=2).encode("ascii")
        A.P.PortableCatalog._write_fresh(output/name, raw)
        return {"bytes": len(raw), "sha256": A.sha(raw)}

    try:
        check()
        names = G._outputs(expected_targets)
        A.need(type(candidate_raw) is bytes and type(supplement_raw) is bytes and
               0 < len(candidate_raw) and 0 < len(supplement_raw) and
               len(candidate_raw)+len(supplement_raw) <= 4*MIB,
               "COMPLETION_COMBINED_INPUT_BYTES")
        A.need(type(prepared_bindings) is dict and len(prepared_bindings) <= 4096,
               "COMPLETION_PREPARED_MAP_BOUND")
        prepared_rows, prepared_bytes = [], 0
        for key, identity in prepared_bindings.items():
            check()
            A.need(type(key) is bytes and 0 < len(key) <= 65536,
                   "COMPLETION_PREPARED_NAME_BYTES")
            name = A.E.strict_json(key)
            A.need(A.E.name_key(name) == key, "COMPLETION_CANONICAL_PREPARED_NAME")
            A.E._hex(identity)
            prepared_bytes += len(key)+70
            A.need(prepared_bytes <= MIB, "COMPLETION_PREPARED_BYTES")
            prepared_rows.append([name, identity])
        budget = make_budget()
        A.need(type(budget) is A.OperationBudget and not budget.claimed and
               budget.worker_cpu == 0 and budget.deadline <= parent_deadline,
               "COMPLETION_REMAINING_OPERATION_BUDGET")
        check()
        context = owner.catalog.context(parent_root)

        def warranted(name):
            check()
            return context["bindings"].get(A.E.name_key(name))

        phase = "PLANNING"
        plan = L.complete_candidate(candidate_raw, supplement_raw,
            semantic_id=installation.semantic_id, foundation_id=A.S.foundation_id(),
            context_root=parent_root, expected_targets=names,
            prepared_bindings=prepared_bindings, warranted_symbol=warranted,
            limits=B.Limits(max_bundle_bytes=4*MIB, max_units=32,
                max_bindings=4096, max_targets=32, max_total_nodes=131072,
                max_evidence_bytes=4*MIB), check_budget=check)
        A.need(plan.status == "READY" and not plan.mathematical_acceptance,
               "COMPLETION_PLAN_NOT_READY")
        published = G.publication_targets(installation.semantic_id, plan.raw_units, names)
        items = [A.PE.read_evidence(raw) for raw in plan.raw_units]
        output = A.C.ordinary(Path(output_directory), directory=True, fresh=True)
        output.mkdir()
        save("candidate.json", candidate_raw)
        save("supplement.json", supplement_raw)
        save("SELECTION.json", {"parent_root": parent_root,
            "semantic_id": installation.semantic_id, "foundation_id": A.S.foundation_id(),
            "candidate_sha256": A.sha(candidate_raw), "supplement_sha256": A.sha(supplement_raw),
            "expected_targets": names,
            "prepared_bindings": prepared_rows,
            "mathematical_acceptance": False})
        phase = "PREFLIGHT"
        checked_plan = owner.preflight(parent_root, plan.raw_units, budget=budget,
            limits=A.PreflightLimits(max_units=32, max_bytes=4*MIB, max_nodes=131072,
                                     max_names=4096, max_edges=32768))
        A.need(checked_plan.status == "READY", "COMPLETION_PREFLIGHT_NEEDS")
        phase = "ADMISSION"
        try:
            accepted = owner.admit(parent_root, checked_plan, budget)
        finally:
            native_cpu += budget.worker_cpu
            account_worker_cpu(budget.worker_cpu)
        save("ADMISSION.json", accepted)
        A.need(accepted["status"] == "CHECKED" and
               accepted["units_checked"] == len(items), "COMPLETION_NEW_CHECK_REQUIRED")
        phase = "PUBLICATION_BYTES"
        for part in ("previews", "evidence"):
            A.C.ordinary(output/part, directory=True, fresh=True).mkdir()
        by_unit = {item.unit_id: item for item in items}
        previews, units = [], []
        for target in published:
            check()
            item = by_unit[target["unit_id"]]
            preview = PP.preview_from_evidence(item.raw, target["name"])
            PP.resolve(preview, item.raw)
            custody.put_preview(preview, before_commit=check)
            filename = "previews/"+target["export_id"]+".json"
            pin = save(filename, preview)
            A.need(custody.get_preview(pin["sha256"], pin["bytes"], check_budget=check) == preview,
                   "COMPLETION_PREVIEW_CUSTODY_READBACK")
            previews.append({**target, "file": str(output/filename), **pin})
        for item in items:
            check()
            filename = "evidence/"+item.unit_id+".json"
            units.append({"unit_id": item.unit_id, "file": str(output/filename),
                          **save(filename, item.raw)})
        result = {"status": "CHECKED_COMPLETION_WITH_DURABLE_PUBLICATION_BYTES",
            "parent_root": parent_root, "local_root": accepted["local_root"],
            "semantic_id": installation.semantic_id,
            "implementation_id": installation.implementation_id,
            "candidate_sha256": A.sha(candidate_raw), "supplement_sha256": A.sha(supplement_raw),
            "targets": published, "units": units, "previews": previews, "admission": accepted,
            "native_cpu_seconds": native_cpu, "wall_seconds": time.monotonic()-started,
            "claim": "LOCAL_CHECKED_COMPLETION_NOT_SOURCE_EXECUTION_OR_PEER_ACCEPTANCE"}
        check()
        save("RESULT.json", result)
        return result
    except BaseException as error:
        failure = G.ContributionError("COMPLETION_"+phase, error, accepted, native_cpu)
        if output is not None:
            try:
                save("FAILURE.json", failure.report)
            except BaseException as log_error:
                failure.report["failure_log_error"] = {
                    "error_type": type(log_error).__name__, "error": str(log_error)}
        raise failure from error
