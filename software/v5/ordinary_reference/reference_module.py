"""Materialize already warranted new mathematics over a local original library.

This is not admission, public binary acceptance, or arbitrary source execution.
The real owner's lock protects current warrants and exact local realizations.
One budget covers loading, acquisition, native checks, rereads and commit.
"""
from pathlib import Path
import json
import math
import os
import time

import ordinary_admission as A
import ordinary_contribution as G
import portable_preview as PP
import reference_closure as M
import reference_store as K
import reference_registration as RG

MIB = 1024**2
REPORT_FIELDS = {"schema", "assurance", "semantic_id", "context_root", "foundation_id",
    "module_name", "targets", "unit_ids", "reference_id", "parent_delta_id", "reference_plan_sha256",
    "direct_imports", "names", "inventories", "added_names", "added_inventories",
    "matched_unit_indices", "matched_names", "matched_inventories", "units_checked", "units_matched",
    "checking_passes", "basis_rows", "usable_basis_rows", "reference_public_units",
    "reference_public_names", "generated_names", "artifact_parts"}


def bind_report(report, request, reference, generated_frontier, direct_imports):
    """Exact event-output binding, not independent verification of mathematics."""
    A.need(type(report) is dict and set(report) == REPORT_FIELDS and
           report["schema"] == "DMKN_ORDINARY_REFERENCE_MODULE_OUTPUT_V1" and
           report["assurance"] == "LOCAL_CHECKED_REFERENCE_MODULE_CONTROLLER_BOUND_IDENTITIES" and
           all(report[field] == request[field] for field in ("semantic_id", "context_root", "foundation_id",
               "module_name", "targets", "unit_ids", "reference_id", "parent_delta_id", "reference_plan_sha256")) and
           report["direct_imports"] == direct_imports, "REFERENCE_MODULE_REPORT_BINDING")
    counts = {"checking_passes": 2, "basis_rows": 581,
        "usable_basis_rows": len(reference.usable_basis_keys),
        "reference_public_units": len(reference.public_frontier),
        "reference_public_names": sum(len(outputs) for _, outputs in reference.public_frontier),
        "generated_names": sum(len(outputs) for _, outputs in generated_frontier),
        "units_checked": len(request["units"]), "units_matched": 0}
    A.need(all(type(report[key]) is int and report[key] == value for key, value in counts.items()) and
           all(report[key] == [] for key in ("matched_unit_indices", "matched_names", "matched_inventories")),
           "REFERENCE_MODULE_REPORT_COUNTS")
    rows = [row for unit in request["units"] for row in unit[2]]
    A.need(report["inventories"] == rows == report["added_inventories"] and
           report["names"] == [row[0] for row in rows] == report["added_names"],
           "REFERENCE_MODULE_REPORT_NEW_INVENTORIES")


class ModuleError(RuntimeError):
    def __init__(self, phase, error, native_cpu, conservative_charge):
        self.report = {"phase": phase, "error_type": type(error).__name__, "error": str(error)[:2048],
            "native_cpu_seconds": native_cpu, "conservative_cpu_reservation_charged": conservative_charge,
            "new_catalog_acceptance": False, "retention": "PARTIAL_DELTA_PRESERVED_NO_AUTOMATIC_RETRY"}
        super().__init__("REFERENCE_MODULE_"+phase+": "+str(error))


def export_delta(owner, parent_root, targets, *, reference_id, parent_delta_id="", profile,
                 matcher, match_worker_script, native_source, worker_script,
                 parent_deadline, make_budget, account_worker_cpu, check_parent):
    """One protected all-new delta; the caller retains the real owner lock.

    The shared reference/delta support descriptor is computed from a fully
    verified installed profile. Saved reports, copied records and unverified
    peer binaries are not registration or mathematical authority.
    """
    A.need(type(owner) is A.OrdinaryAdmission and type(profile) is G.AuthoringProfile and
           G.A is A and PP.PE is A.PE and K.A is A and RG.A is A and RG.G is G and RG.K is K and
           type(parent_deadline) in (int, float) and math.isfinite(parent_deadline) and
           all(callable(f) for f in (make_budget, account_worker_cpu, check_parent)),
           "REFERENCE_MODULE_CONFIGURATION")
    started = time.monotonic()
    phase, store, grant, budget, committed = "INPUTS", None, None, None, None
    native_entered, supervision, native_cpu, conservative_charge = False, None, 0.0, 0

    def check():
        check_parent()
        A.need(time.monotonic() < parent_deadline, "REFERENCE_MODULE_PARENT_DEADLINE")
        if budget is not None:
            budget.check()

    def save_json(path, value):
        check()
        raw = json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False,
                         separators=(",", ":")).encode("ascii")
        A.need(0 < len(raw) <= MIB, "REFERENCE_MODULE_METADATA_BOUND")
        A.P.PortableCatalog._write_fresh(path, raw)
        A.need(A.C.read_bounded(path, MIB) == raw, "REFERENCE_MODULE_METADATA_READBACK")

    try:
        check()
        budget = make_budget()
        A.need(type(budget) is A.OperationBudget and not budget.claimed and budget.worker_cpu == 0 and
               budget.deadline <= parent_deadline and budget.output_bytes >= 8*MIB and budget.log_bytes <= MIB,
               "REFERENCE_MODULE_ORIGINAL_BUDGET")
        check()
        A.C.hexid(parent_root); A.C.hexid(reference_id)
        A.need(type(parent_delta_id) is str, "REFERENCE_MODULE_PARENT_ID")
        if parent_delta_id:
            A.C.hexid(parent_delta_id)
        installation, custody = owner.installation, owner.evidence_store
        A.need(profile.installation_manifest_sha256 == installation.manifest_sha256,
               "REFERENCE_MODULE_INSTALLATION")
        profile.verify(check)
        here = Path(__file__).absolute().parent
        source, worker = A.C.ordinary(Path(native_source)), A.C.ordinary(Path(worker_script))
        A.need(source == here/"ReferenceModule.lean" and worker == here/"reference_module_worker.py" and
               Path(M.__file__).absolute() == here/"reference_closure.py" and
               Path(RG.__file__).absolute() == here/"reference_registration.py",
               "REFERENCE_MODULE_SELECTED_SUPPORT")
        matcher, match_worker = A.C.ordinary(Path(matcher)), A.C.ordinary(Path(match_worker_script))
        support = RG.support_descriptor(installation, profile, matcher, match_worker)
        selected = sorted(G._acquired(installation.semantic_id, targets), key=lambda row: A.E.name_key(row["name"]))
        A.need(0 < len(selected) <= 32, "REFERENCE_MODULE_TARGETS")
        context = owner.catalog.context(parent_root)
        A.need(context["semantic_id"] == installation.semantic_id and
               context["foundation_id"] == A.S.foundation_id(), "REFERENCE_MODULE_CONTEXT")
        store = K.open_for_owner(owner, support, check)
        phase = "PROTECTED_REFERENCE"
        parent = store.load_delta(parent_delta_id, context, check) if parent_delta_id else None
        reference = parent.reference if parent is not None else store.load_reference(reference_id, context, check)
        A.need(reference.reference_id == reference_id and reference.support_id == store.support_id,
               "REFERENCE_MODULE_PARENT_REFERENCE")
        generated = parent.frontier if parent is not None else ()
        frontier = M.Frontier(reference_id, parent_delta_id, reference.public_frontier, generated,
                              reference.usable_basis_keys, reference.warrant_bindings)
        covered = {key: (identity, unit) for unit, outputs in (*reference.public_frontier, *generated)
                   for key, identity in outputs}
        A.need(all(context["bindings"].get(A.E.name_key(row["name"])) == row["export_id"] for row in selected),
               "REFERENCE_MODULE_CURRENT_TARGET_WARRANTS")
        if all(covered.get(A.E.name_key(row["name"])) == (row["export_id"], row["unit_id"]) for row in selected):
            check()
            return {"status": "REUSED_LOCAL_ORDINARY_REALIZATION", "reference_id": reference_id,
                "delta_id": parent_delta_id, "support_id": store.support_id, "source_context_root": parent_root,
                "snapshot_id": reference.snapshot.manifest_sha256,
                "replay_request": str(reference.snapshot.directory/"replay-request.json"),
                "targets": selected, "fetch_calls": 0, "native_calls": 0, "native_cpu_seconds": 0.0,
                "wall_seconds": time.monotonic()-started, "new_catalog_acceptance": False,
                "trust": "PROTECTED_LOCAL_REALIZATION_NOT_TRANSFERABLE_AUTHORITY"}
        phase = "RESERVE_AND_COLLECT_DELTA"
        grant = store.reserve_delta(reference, parent, {"source_context_root": parent_root, "targets": selected},
                                    check, deadline=min(parent_deadline, budget.deadline))
        plan = store.prepare_delta_plan(grant, check)

        def warranted(name):
            check()
            return context["bindings"].get(A.E.name_key(name))

        def evidence(name, identity, maximum):
            check()
            A.need(warranted(name) == identity, "REFERENCE_MODULE_NOT_WARRANTED")
            locator = PP.read_locator(A.E.strict_json(custody.get_locator(
                installation.semantic_id, identity, 4096, check_budget=check)))
            A.need(locator["semantic_id"] == installation.semantic_id and
                   A.E.name_key(locator["export_name"]) == A.E.name_key(name) and
                   A.S.export_id(installation.semantic_id, locator["unit_id"], name) == identity,
                   "REFERENCE_MODULE_EXACT_LOCAL_LOCATOR")
            return custody.get_evidence(installation.semantic_id, locator["unit_id"], maximum, check_budget=check)

        closure = M.collect_closure(admission_api=A, semantic_id=installation.semantic_id,
            foundation_id=A.S.foundation_id(), context_root=parent_root,
            inventory_raw=installation.read("inventory", MIB), targets=selected,
            module_name=K.module_name(plan.module_name), warranted_symbol=warranted, fetch_evidence=evidence,
            check_budget=check, frontier=frontier, reference_plan_sha256=plan.reference_plan_sha256)
        A.need(closure.request is not None and bool(closure.ordered_unit_ids), "REFERENCE_MODULE_NONEMPTY_DELTA")
        inputs = store.bind_delta_inputs(grant, closure.request, closure.inventory, check)
        A.need(inputs.plan == plan and inputs.request_sha256 == A.sha(closure.request),
               "REFERENCE_MODULE_BOUND_INPUTS")
        profile.verify(check)
        phase = "LIVE_NATIVE_DELTA"
        argv = [str(installation.path("python")), "-I", "-S", "-B", str(worker),
            str(installation.path("lean")), str(source), os.pathsep.join(map(str, profile.helper_paths)),
            str(installation.runtime_roots["lean_runtime"]), str(inputs.inventory_path),
            str(inputs.request_path), str(plan.reference_plan_path), str(plan.output_path), str(plan.report_path)]
        budget.claim()
        allowance = installation._supervisor.limits_checked(budget.allowance(parent_deadline))
        try:
            native_entered = True
            supervision = installation._supervisor.supervise(argv, grant.directory,
                grant.directory/"supervision", allowance, installation._job_module.Job)
        finally:
            try:
                if not RG.cleanup_known(supervision):
                    store.mark_blocked(grant, "NATIVE_DELTA_CLEANUP_UNCERTAIN")
            finally:
                final = supervision.get("final_job") if type(supervision) is dict else None
                value = final.get("cpu_seconds") if type(final) is dict else None
                if type(value) in (int, float) and math.isfinite(value) and value >= 0:
                    native_cpu = value
                    budget.worker_cpu += value
                    account_worker_cpu(value)
                else:
                    native_cpu, conservative_charge = None, allowance["cpu_seconds"]
                    account_worker_cpu(conservative_charge)
        save_json(plan.supervision_path, supervision)
        A.need(native_cpu is not None and A._clean_worker(supervision), "REFERENCE_MODULE_NATIVE_NOT_CLEAN")
        A.need(A.C.ordinary(grant.directory/"supervision/stderr.txt").stat().st_size == 0,
               "REFERENCE_MODULE_NATIVE_DIAGNOSTIC")
        phase = "BIND_LIVE_OUTPUT"
        report_raw = A.C.read_bounded(A.C.ordinary(plan.report_path), 8*MIB)
        report = A._writer_json(report_raw, 8*MIB)
        request = A.E.strict_json(closure.request, A.E.Limits(max_bytes=4*MIB))
        direct_imports = ([K.module_name(parent.module_name)] if parent is not None else
            [row["module"] for row in A.E.strict_json(reference.snapshot.root_imports_raw)])
        bind_report(report, request, reference, generated, direct_imports)
        output = plan.output_path
        parts = (output, Path(str(output)+".server"), Path(str(output)+".private"),
                 output.with_suffix(".ir.sig"), output.with_suffix(".ir"))
        A.need(type(report["artifact_parts"]) is list and len(report["artifact_parts"]) == 5 and
               {path.name for path in output.parent.iterdir()} == {path.name for path in parts},
               "REFERENCE_MODULE_PART_CENSUS")
        total, artifact_pins = 0, {}
        for path, row in zip(parts, report["artifact_parts"]):
            A.need(type(row) is dict and set(row) == {"path", "bytes"} and Path(row["path"]) == path and
                   type(row["bytes"]) is int and 0 < row["bytes"] <= 64*MIB-total,
                   "REFERENCE_MODULE_PART_BINDING")
            pin = K.file_pin(path, row["bytes"], check)
            A.need(pin["bytes"] == row["bytes"], "REFERENCE_MODULE_PART_SIZE")
            total += pin["bytes"]
            artifact_pins[path.name] = pin
        profile.verify(check)
        A.need(A.C.read_bounded(inputs.request_path, 4*MIB) == closure.request and
               A.C.read_bounded(inputs.inventory_path, MIB) == closure.inventory and
               A.C.read_bounded(plan.reference_plan_path, MIB) == plan.reference_plan_raw,
               "REFERENCE_MODULE_INPUT_CHANGED")
        phase = "PROTECTED_COMMIT"
        committed = store._commit_delta(grant, {"report_raw": report_raw, "report": report,
                                                "supervision": supervision}, check)
        return {"status": "CHECKED_AND_REGISTERED_LOCAL_REFERENCE_DELTA", "reference_id": reference_id,
            "delta_id": committed.delta_id, "parent_delta_id": parent_delta_id, "support_id": store.support_id,
            "source_context_root": parent_root, "snapshot_id": reference.snapshot.manifest_sha256,
            "module_name": committed.module_name, "module_directory": str(committed.module_directory),
            "generated_import_directories": [str(path) for path in committed.import_directories],
            "original_replay_request": str(reference.snapshot.directory/"replay-request.json"),
            "targets": selected, "cut_unit_ids": list(closure.cut_unit_ids),
            "ordered_unit_ids": list(closure.ordered_unit_ids), "fetch_calls": closure.fetch_calls,
            "acquired_bytes": closure.acquired_bytes, "acquired_nodes": closure.acquired_nodes,
            "artifact_parts": artifact_pins, "report_sha256": A.sha(report_raw),
            "worker_calls": 1, "native_calls": 3,
            "native_cpu_seconds": native_cpu, "wall_seconds": time.monotonic()-started,
            "new_catalog_acceptance": False,
            "trust": "LOCAL_GENERATION_FROM_CURRENT_WARRANTS_NOT_REMOTE_BINARY_AUTHORITY"}
    except BaseException as error:
        failure = ModuleError(phase, error, native_cpu, conservative_charge)
        if grant is not None and committed is None and (not native_entered or RG.cleanup_known(supervision)):
            try:
                store.abandon(grant, "CLEAN_FAILED_REFERENCE_DELTA")
            except BaseException as closure_error:
                failure.report["closure_error"] = str(closure_error)[:1024]
                failure.report["retention"] = "UNRESOLVED_DELTA_RETAINED_NO_RETRY"
        if isinstance(getattr(error, "report", None), dict):
            failure.report["store_disposition"] = error.report
        if committed is not None:
            failure.report["committed_delta_id"] = committed.delta_id
            failure.report["retention"] = "COMMITTED_DELTA_PRESERVED_DESPITE_REPORTING_FAILURE"
        if grant is not None:
            try:
                save_json(grant.directory/"FAILURE.json", failure.report)
            except BaseException:
                pass
        raise failure from error
