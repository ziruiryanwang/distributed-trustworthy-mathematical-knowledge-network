"""Local checked module realization from one already warranted owner context.

No new catalog acceptance, network, downloaded binary, source authoring or
certificate. Cold export checks the selected complete proof closure. Explicit
warm export cuts only at an exact locally registered modern module chain, and
checks the remaining delta in both private and public views. A committed local
realization record is not a transferable trust token or a peer-binary authority.
"""
from pathlib import Path
import json
import math
import os
import time

import ordinary_admission as A
import ordinary_contribution as G
import portable_preview as PP
import module_closure as M
import anchor_store as K

MIB = 1024**2
POLICY = "ORDINARY_EXACT_INSTALLED_PUBLIC_MODULE_V2"
EVENT_FILES = ("request.json", "inventory.json", "anchor-plan.json", "native-report.json",
               "native-report.json.pending", "native-report.json.phases.jsonl", "SUPERVISION.json")


def support_descriptor(installation, profile, source, worker):
    """Narrow, exact compatibility identity; full profile verification is separate.

    The installed manifest commits core/codec/supervisor/runtime bytes. These
    are the actual loaded auxiliary dependencies, not name-only peer choices.
    Changes to separate query/discovery-only payloads do not invalidate modules;
    changing the shared pinned owner/loader call path still does, deliberately.
    """
    pins = {path: (size, digest) for path, size, digest in profile.file_pins}
    package = profile.author_worker_script.parent
    required = {"controller": Path(__file__).absolute(), "collector": Path(M.__file__).absolute(),
        "store": Path(K.__file__).absolute(), "native": source, "worker": worker,
        "owner": package/"owner.py", "profile": package/"profile.py"}
    for role, module in (("contribution", G), ("preview", PP),
            ("owner_request", G.R), ("legacy_request", G.R.V1),
            ("candidate", G.B), ("ordinary_preview", PP.P)):
        required[role] = Path(module.__file__).absolute()
    A.need(K.A is A and K.M is M and G.PP is PP and
           all(path in pins for path in required.values()), "MODULE_EXPORT_SUPPORT_PINS")
    names = ("OriginalExpr", "OriginalDecl", "CheckedExtension", "BootstrapSupport",
             "OwnerRebind", "OrdinaryExport")
    suffixes = (".olean", ".olean.server", ".olean.private", ".ir.sig", ".ir")
    helpers, found = [], set()
    for index, directory in enumerate(profile.helper_paths):
        for name in names:
            for suffix in suffixes:
                path = directory/(name+suffix)
                if path in pins:
                    A.need((name, suffix) not in found, "MODULE_EXPORT_AMBIGUOUS_NATIVE_HELPER")
                    found.add((name, suffix))
                    helpers.append([str(index)+"/"+name+suffix, *pins[path]])
    A.need(found == {(name, suffix) for name in names for suffix in suffixes},
           "MODULE_EXPORT_NATIVE_HELPER_PARTS")
    return A.E.canonical_json({"schema": "DMKN_LOCAL_MODULE_ANCHOR_SUPPORT_V1",
        "installation_manifest_sha256": installation.manifest_sha256,
        "semantic_id": installation.semantic_id, "foundation_id": A.S.foundation_id(),
        "implementation_id": installation.implementation_id, "policy": POLICY,
        "sources": {role: {"bytes": pins[path][0], "sha256": pins[path][1]}
                    for role, path in required.items()}, "native_helpers": sorted(helpers)})


def cleanup_known(supervision):
    """Clean failure is not uncertain cleanup and must not poison the sidecar."""
    return (type(supervision) is dict and supervision.get("job_closed") is True and
        supervision.get("direct_child_reaped") is True and supervision.get("cleanup_errors") == [] and
        type(supervision.get("final_job")) is dict and
        supervision["final_job"].get("active_processes") == 0)


def validate_partition(request, report):
    """Bind matched/added accounting to complete selected request units.

    This is report validation, not proof checking. Native private full matching,
    public compatibility and both exact rereads remain required before this call.
    """
    units, indices = request["units"], report["matched_unit_indices"]
    A.need(type(indices) is list and len(indices) < len(units) and
           all(type(i) is int and 0 <= i < len(units) for i in indices) and
           indices == sorted(set(indices)), "MODULE_EXPORT_MATCHED_INDICES")
    selected = set(indices)
    added, matched = [], []
    for index, unit in enumerate(units):
        if index in selected:
            # Derive the family from the protected unit, not a report label.
            # Full installed equality and group completeness remain native /
            # authenticated accepted-unit premises, not report assertions.
            K.matched_realization(unit)
            matched.extend(unit[2])
        else:
            added.extend(unit[2])
    A.need(type(report["units_checked"]) is int and type(report["units_matched"]) is int and
           report["units_checked"] == len(units)-len(indices) and
           report["units_matched"] == len(indices) and
           report["added_names"] == [row[0] for row in added] and
           report["added_inventories"] == added and
           report["matched_names"] == [row[0] for row in matched] and
           report["matched_inventories"] == matched,
           "MODULE_EXPORT_MATCHED_ADDED_PARTITION")


class ModuleExportError(RuntimeError):
    def __init__(self, phase, error, native_cpu, conservative_charge):
        self.report = {"phase": phase, "error_type": type(error).__name__,
            "error": str(error), "native_cpu_seconds": native_cpu,
            "conservative_cpu_reservation_charged": conservative_charge,
            "new_catalog_acceptance": False,
            "retention": "PARTIAL_EXPORT_RETAINED_UNCOMMITTED_NO_RETRY"}
        super().__init__("MODULE_EXPORT_"+phase+": "+str(error))


def export_module(owner, parent_root, targets, *, output_directory, profile,
                  native_source, worker_script, parent_deadline, make_budget,
                  account_worker_cpu, check_parent, module_anchor=""):
    """One bounded fresh export; the caller retains the owner lock throughout.

    `profile` is the existing adopted AuthoringProfile, augmented with exact pins
    for this module, module_closure, module_worker and OrdinaryModule.lean. No
    metadata from the evidence chooses support code or the installed runtime.
    The callback budget is derived from the original enclosing allowance.
    The success manifest is written only after complete native/event/file checks.
    """
    A.need(type(owner) is A.OrdinaryAdmission and G.A is A and PP.PE is A.PE and
           type(profile) is G.AuthoringProfile and
           type(parent_deadline) in (int, float) and math.isfinite(parent_deadline) and
           all(callable(f) for f in (make_budget, account_worker_cpu, check_parent)),
           "MODULE_EXPORT_OWNER_CONFIGURATION")
    A.C.hexid(parent_root)
    installation, custody = owner.installation, owner.evidence_store
    A.need(profile.installation_manifest_sha256 == installation.manifest_sha256,
           "MODULE_EXPORT_PROFILE_INSTALLATION")
    started = time.monotonic()
    phase, output, budget, native_cpu, conservative_charge = "INPUTS", None, None, 0.0, 0
    store = parent = grant = committed = None
    native_entered, supervision = False, None

    def check():
        check_parent()
        A.need(time.monotonic() < parent_deadline, "MODULE_EXPORT_PARENT_DEADLINE")
        if budget is not None:
            budget.check()

    def save(name, value):
        raw = value if type(value) is bytes else json.dumps(value, sort_keys=True,
            ensure_ascii=True, allow_nan=False, separators=(",", ":")).encode("ascii")
        A.need(len(raw) <= 8*MIB, "MODULE_EXPORT_METADATA_BOUND")
        A.P.PortableCatalog._write_fresh(output/name, raw)
        return {"bytes": len(raw), "sha256": A.sha(raw)}

    try:
        check()
        selected = sorted(G._acquired(installation.semantic_id, targets),
                          key=lambda row: A.E.name_key(row["name"]))
        A.need(bool(selected), "MODULE_EXPORT_TARGETS_EMPTY")
        source, worker = A.C.ordinary(Path(native_source)), A.C.ordinary(Path(worker_script))
        profile.verify(check)
        pins = {path: (size, digest) for path, size, digest in profile.file_pins}
        required = {"native": source, "worker": worker,
                    "controller": Path(__file__).absolute(), "closure": Path(M.__file__).absolute()}
        A.need(all(path in pins for path in required.values()), "MODULE_EXPORT_SUPPORT_PINS")
        destination = A.C.ordinary(Path(output_directory), directory=True, fresh=True)
        protected = [installation.root, owner.catalog._root, custody.root,
                     *installation.runtime_roots.values(), *profile.helper_paths]
        for directory in protected:
            A.need(not destination.is_relative_to(directory) and not directory.is_relative_to(destination),
                   "MODULE_EXPORT_OUTPUT_OVERLAP")
        A.need(all(not path.is_relative_to(destination) for path in pins), "MODULE_EXPORT_SUPPORT_OVERLAP")
        context = owner.catalog.context(parent_root)
        A.need(context["semantic_id"] == installation.semantic_id and
               context["foundation_id"] == A.S.foundation_id(), "MODULE_EXPORT_CONTEXT")
        A.need(type(module_anchor) is str, "MODULE_EXPORT_ANCHOR_ID")
        if module_anchor:
            A.C.hexid(module_anchor)
        phase = "ANCHOR"
        store = K.open_for_owner(owner, support_descriptor(installation, profile, source, worker), check)
        parent = store.load(module_anchor, context, check) if module_anchor else None
        plan_raw = store.plan(parent)
        plan = A._writer_json(plan_raw, 4*MIB)
        key_input = {"support_id": store.support_id, "parent_anchor_id": module_anchor,
                     "targets": selected}
        key = A.sha(b"DMKN-ORDINARY-ANCHORED-MODULE-V1\0"+A.E.canonical_json(key_input))
        module_text = "DMKNBridge_"+key
        module_name = [[0, {"$bytes": list(module_text.encode("ascii"))}]]

        def warranted(name):
            check()
            return context["bindings"].get(A.E.name_key(name))

        def evidence(name, identity, maximum):
            check()
            A.need(warranted(name) == identity, "MODULE_EXPORT_NOT_WARRANTED")
            locator = PP.read_locator(A.E.strict_json(custody.get_locator(
                installation.semantic_id, identity, 4096, check_budget=check)))
            A.need(locator["semantic_id"] == installation.semantic_id and
                   A.E.name_key(locator["export_name"]) == A.E.name_key(name) and
                   A.S.export_id(installation.semantic_id, locator["unit_id"], name) == identity,
                   "MODULE_EXPORT_EXACT_LOCAL_LOCATOR")
            raw = custody.get_evidence(installation.semantic_id, locator["unit_id"], maximum,
                                      check_budget=check)
            # The collector verifies complete actual bytes and every import;
            # custody has not supplied mathematical authority.
            return raw

        phase = "CLOSURE"
        closure = M.collect_closure(admission_api=A, semantic_id=installation.semantic_id,
            foundation_id=A.S.foundation_id(), context_root=parent_root,
            inventory_raw=installation.read("inventory", MIB), targets=selected,
            module_name=module_name, warranted_symbol=warranted, fetch_evidence=evidence,
            check_budget=check, anchor_frontier=M.AnchorFrontier("", ()) if parent is None else parent.frontier,
            anchor_plan_sha256=A.sha(plan_raw))
        if closure.request is None:
            A.need(parent is not None and not closure.ordered_unit_ids and not closure.ordered_evidence and
                   closure.fetch_calls == 0, "MODULE_EXPORT_EMPTY_DELTA_ANCHOR_REQUIRED")
            profile.verify(check)
            parent = store.load(module_anchor, owner.catalog.context(parent_root), check)
            output = destination
            output.mkdir()
            result = {"status": "REUSED_LOCAL_MODULE_ANCHOR", "anchor_id": parent.anchor_id,
                "cache_key": parent.materialization_key, "policy": POLICY,
                "semantic_id": installation.semantic_id, "foundation_id": A.S.foundation_id(),
                "source_context_root": parent_root, "module_name": parent.module_name,
                "module_directory": str(parent.module_directory),
                "import_directories": [str(path) for path in parent.import_directories],
                "targets": selected, "ordered_unit_ids": [], "cut_unit_ids": list(closure.cut_unit_ids),
                "fetch_calls": 0, "native_calls": 0, "native_cpu_seconds": 0.0,
                "wall_seconds": time.monotonic()-started, "new_catalog_acceptance": False,
                "trust": "EXACT_PROTECTED_LOCAL_REGISTRATION_NOT_PEER_BINARY_AUTHORITY"}
            save("MODULE.json", result)
            return result
        budget = make_budget()
        A.need(type(budget) is A.OperationBudget and not budget.claimed and budget.worker_cpu == 0 and
               budget.deadline <= parent_deadline, "MODULE_EXPORT_REMAINING_BUDGET")
        check()
        output = destination
        output.mkdir()
        artifacts = output/"modules"
        artifacts.mkdir()
        input_pins = {"request": save("request.json", closure.request),
                      "inventory": save("inventory.json", closure.inventory),
                      "anchor_plan": save("anchor-plan.json", plan_raw)}
        save("SELECTION.json", {"cache_key": key, "key_input": key_input,
            "source_context_root": parent_root, "input_pins": input_pins,
            "ordered_unit_ids": list(closure.ordered_unit_ids),
            "anchor_id": module_anchor, "cut_unit_ids": list(closure.cut_unit_ids),
            "acquired_bytes": closure.acquired_bytes, "acquired_nodes": closure.acquired_nodes,
            "fetch_calls": closure.fetch_calls, "warrant_lookups": closure.warrant_lookups,
            "claim": "SELECTED_INPUTS_NOT_COMPLETED_MODULE"})
        grant = store.reserve(parent, {"source_context_root": parent_root, "targets": selected,
            "materialization_key": key, **input_pins}, check, deadline=parent_deadline)
        artifact, report_path = artifacts/(module_text+".olean"), output/"native-report.json"
        argv = [str(installation.path("python")), "-I", "-S", "-B", str(worker),
            str(installation.path("lean")), str(source),
            os.pathsep.join(map(str, profile.helper_paths)),
            str(installation.runtime_roots["lean_runtime"]), str(output/"inventory.json"),
            str(output/"request.json"), str(output/"anchor-plan.json"), str(artifact), str(report_path)]
        phase = "NATIVE_MODULE"
        budget.claim()
        allowance = installation._supervisor.limits_checked(budget.allowance(parent_deadline))
        try:
            native_entered = True
            supervision = installation._supervisor.supervise(argv, output, output/"supervision",
                allowance, installation._job_module.Job)
        finally:
            # Persist uncertainty before accounting/logging callbacks can fail.
            # The marker is safety bookkeeping, even when the time budget expired.
            try:
                if not cleanup_known(supervision):
                    store.mark_blocked(grant, "NATIVE_CLEANUP_UNCERTAIN", lambda: None)
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
        save("SUPERVISION.json", supervision)
        A.need(native_cpu is not None and A._clean_worker(supervision), "MODULE_EXPORT_NATIVE_NOT_CLEAN")
        A.need(A.C.ordinary(output/"supervision/stderr.txt").stat().st_size == 0,
               "MODULE_EXPORT_NATIVE_DIAGNOSTIC")
        check()
        phase = "VALIDATE_OUTPUT"
        report_raw = A.C.read_bounded(A.C.ordinary(report_path), 8*MIB)
        report = A._writer_json(report_raw, 8*MIB)
        request = A.E.strict_json(closure.request, A.E.Limits(max_bytes=4*MIB))
        expected_fields = {"schema", "assurance", "semantic_id", "context_root", "foundation_id",
            "module_name", "targets", "unit_ids", "names", "inventories",
            "matched_unit_indices", "matched_names", "matched_inventories", "added_names",
            "added_inventories", "units_checked", "units_matched", "checking_passes",
            "basis_rows", "artifact_parts", "anchor_id", "anchor_plan_sha256", "direct_imports", "anchor_names"}
        direct_imports = [[[0, {"$bytes": list(b"Init")}]]] if parent is None else [
            [[0, {"$bytes": list(parent.module_name.encode("ascii"))}]]]
        anchor_names = [row["name"] for unit in plan["bindings"] for row in unit["outputs"]]
        A.need(type(report) is dict and set(report) == expected_fields and
               report["schema"] == "DMKN_ORDINARY_MODULE_OUTPUT_V3" and
               report["assurance"] == "LOCAL_CHECKED_ANCHORED_MODULE_CONTROLLER_BOUND_IDENTITIES" and
               all(report[field] == request[field] for field in ("semantic_id", "context_root",
                   "foundation_id", "module_name", "targets", "unit_ids", "anchor_id", "anchor_plan_sha256")) and
               report["direct_imports"] == direct_imports and report["anchor_names"] == anchor_names and
               report["checking_passes"] == 2 and report["basis_rows"] == 581,
               "MODULE_EXPORT_REPORT_BINDING")
        rows = [row for unit in request["units"] for row in unit[2]]
        A.need(report["inventories"] == rows and report["names"] == [row[0] for row in rows],
               "MODULE_EXPORT_EXACT_INVENTORIES")
        validate_partition(request, report)
        parts = [artifact, Path(str(artifact)+".server"), Path(str(artifact)+".private"),
                 artifact.with_suffix(".ir.sig"), artifact.with_suffix(".ir")]
        A.need(type(report["artifact_parts"]) is list and len(report["artifact_parts"]) == 5 and
               {p.name for p in artifacts.iterdir()} == {p.name for p in parts}, "MODULE_EXPORT_PARTS_CENSUS")
        total, artifact_pins = 0, {}
        for path, row in zip(parts, report["artifact_parts"]):
            check()
            A.need(type(row) is dict and set(row) == {"path", "bytes"} and
                   Path(row["path"]) == path and type(row["bytes"]) is int and
                   0 < row["bytes"] <= 64*MIB-total, "MODULE_EXPORT_PART_BINDING")
            raw = A.C.read_bounded(A.C.ordinary(path), row["bytes"])
            A.need(len(raw) == row["bytes"], "MODULE_EXPORT_PART_SIZE")
            total += len(raw)
            artifact_pins[path.name] = {"bytes": len(raw), "sha256": A.sha(raw)}
        profile.verify(check)
        A.need(A.C.read_bounded(output/"request.json", 4*MIB) == closure.request and
               A.C.read_bounded(output/"inventory.json", MIB) == closure.inventory and
               A.C.read_bounded(output/"anchor-plan.json", 4*MIB) == plan_raw,
               "MODULE_EXPORT_INPUT_CHANGED")
        check()
        phase = "REGISTER_ANCHOR"
        event_files = {}
        for name in EVENT_FILES:
            check()
            raw = A.C.read_bounded(A.C.ordinary(output/name), 8*MIB)
            event_files[name] = {"path": output/name, "bytes": len(raw), "sha256": A.sha(raw)}
        committed = store._commit_generated(grant, {"request": closure.request, "report": report,
            "artifact_parts": [{"path": path, **artifact_pins[path.name]} for path in parts],
            "event_files": event_files}, check)
        result = {"status": "CHECKED_AND_REGISTERED_LOCAL_MODULE_ANCHOR", "cache_key": key,
            "anchor_id": committed.anchor_id, "parent_anchor_id": module_anchor,
            "policy": POLICY, "semantic_id": installation.semantic_id,
            "foundation_id": A.S.foundation_id(), "source_context_root": parent_root,
            "module_name": module_text, "targets": selected,
            "module_directory": str(committed.module_directory),
            "import_directories": [str(path) for path in committed.import_directories],
            "cut_unit_ids": list(closure.cut_unit_ids), "fetch_calls": closure.fetch_calls, "native_calls": 1,
            "ordered_unit_ids": list(closure.ordered_unit_ids), "artifact_parts": artifact_pins,
            "matched_unit_indices": report["matched_unit_indices"],
            "units_matched": report["units_matched"], "units_checked": report["units_checked"],
            "matched_names": report["matched_names"], "added_names": report["added_names"],
            "report_sha256": A.sha(report_raw), "native_cpu_seconds": native_cpu,
            "wall_seconds": time.monotonic()-started, "new_catalog_acceptance": False,
            "trust": "LOCAL_GENERATION_FROM_WARRANTED_EVIDENCE_NOT_REMOTE_BINARY_AUTHORITY",
            "scope": "EXACT_LOCAL_ANCHOR_AND_CHECKED_DELTA_NO_PEER_BINARY_OR_EXECUTABLE_IR_OR_NOTATION"}
        save("MODULE.json", result)
        return result
    except BaseException as error:
        failure = ModuleExportError(phase, error, native_cpu, conservative_charge)
        if grant is not None and committed is None and (not native_entered or cleanup_known(supervision)):
            try:
                store.abandon(grant, "CLEAN_FAILED_EXPORT")
            except BaseException as closure_error:
                failure.report["anchor_closure_error"] = str(closure_error)
                failure.report["retention"] = "UNRESOLVED_ANCHOR_OPERATION_RETAINED_NO_RETRY"
        if isinstance(error, (K.AnchorCommitUnknown, K.AnchorCommittedError)):
            failure.report["anchor_commit"] = error.report
            failure.report["anchor_id"] = error.anchor_id
            failure.report["retention"] = (
                "COMMIT_UNKNOWN_EXACT_ID_LOOKUP_REQUIRED_NO_RETRY" if isinstance(error, K.AnchorCommitUnknown)
                else "COMMITTED_ANCHOR_PRESERVED_DESPITE_REPORTING_FAILURE")
        if committed is not None:
            failure.report["committed_anchor_id"] = committed.anchor_id
            failure.report["retention"] = "COMMITTED_ANCHOR_PRESERVED_DESPITE_REPORTING_FAILURE"
        if output is not None:
            try:
                save("FAILURE.json", failure.report)
            except BaseException:
                pass
        raise failure from error



