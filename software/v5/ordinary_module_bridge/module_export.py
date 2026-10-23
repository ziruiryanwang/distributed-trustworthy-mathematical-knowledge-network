"""Local full-proof module export from one already warranted owner context.

No new catalog acceptance, network, downloaded binary, source authoring or
certificate. First export pays the selected complete proof closure. Its output
is a locally generated ordinary Lean module, not a transferable trust token.
Automatic cache lookup and previously generated module boundaries are not yet
implemented; the context-independent key is reserved for exact local reuse.
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

MIB = 1024**2
POLICY = "DMKN_ORDINARY_INIT_FULL_PROOF_PUBLIC_MODULE_V1"


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
                  account_worker_cpu, check_parent):
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
        # Relevant helper bytes, not the whole owner-context history or absolute
        # installation paths. Target IDs recursively bind exact import identities.
        helper_pins = []
        for index, directory in enumerate(profile.helper_paths):
            for path, pin in pins.items():
                if path.is_relative_to(directory):
                    helper_pins.append([index, path.relative_to(directory).as_posix(), *pin])
        key_input = {"policy": POLICY, "semantic_id": installation.semantic_id,
            "foundation_id": A.S.foundation_id(), "implementation_id": installation.implementation_id,
            "sources": {role: list(pins[path]) for role, path in required.items()},
            "helpers": sorted(helper_pins), "targets": selected}
        key = A.sha(b"DMKN-ORDINARY-MODULE-CACHE-V1\0"+A.E.canonical_json(key_input))
        module_text = "DMKNBridge_"+key
        module_name = [[0, {"$bytes": list(module_text.encode("ascii"))}]]
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
            check_budget=check)
        budget = make_budget()
        A.need(type(budget) is A.OperationBudget and not budget.claimed and budget.worker_cpu == 0 and
               budget.deadline <= parent_deadline, "MODULE_EXPORT_REMAINING_BUDGET")
        check()
        output = destination
        output.mkdir()
        artifacts = output/"modules"
        artifacts.mkdir()
        input_pins = {"request": save("request.json", closure.request),
                      "inventory": save("inventory.json", closure.inventory)}
        save("SELECTION.json", {"cache_key": key, "key_input": key_input,
            "source_context_root": parent_root, "input_pins": input_pins,
            "ordered_unit_ids": list(closure.ordered_unit_ids),
            "acquired_bytes": closure.acquired_bytes, "acquired_nodes": closure.acquired_nodes,
            "fetch_calls": closure.fetch_calls, "warrant_lookups": closure.warrant_lookups,
            "claim": "SELECTED_INPUTS_NOT_COMPLETED_MODULE"})
        artifact, report_path = artifacts/(module_text+".olean"), output/"native-report.json"
        argv = [str(installation.path("python")), "-I", "-S", "-B", str(worker),
            str(installation.path("lean")), str(source),
            os.pathsep.join(map(str, profile.helper_paths)),
            str(installation.runtime_roots["lean_runtime"]), str(output/"inventory.json"),
            str(output/"request.json"), str(artifact), str(report_path)]
        phase = "NATIVE_MODULE"
        budget.claim()
        allowance = installation._supervisor.limits_checked(budget.allowance(parent_deadline))
        supervision = None
        try:
            supervision = installation._supervisor.supervise(argv, output, output/"supervision",
                allowance, installation._job_module.Job)
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
            "module_name", "targets", "unit_ids", "names", "inventories", "units_checked",
            "checking_passes", "basis_rows", "artifact_parts"}
        A.need(type(report) is dict and set(report) == expected_fields and
               report["schema"] == "DMKN_ORDINARY_MODULE_OUTPUT_V1" and
               report["assurance"] == "LOCAL_CHECKED_MODULE_CONTROLLER_BOUND_IDENTITIES" and
               all(report[field] == request[field] for field in ("semantic_id", "context_root",
                   "foundation_id", "module_name", "targets", "unit_ids")) and
               report["units_checked"] == len(closure.ordered_evidence) and
               report["checking_passes"] == 2 and report["basis_rows"] == 581,
               "MODULE_EXPORT_REPORT_BINDING")
        rows = [row for unit in request["units"] for row in unit[2]]
        A.need(report["inventories"] == rows and report["names"] == [row[0] for row in rows],
               "MODULE_EXPORT_EXACT_INVENTORIES")
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
               A.C.read_bounded(output/"inventory.json", MIB) == closure.inventory,
               "MODULE_EXPORT_INPUT_CHANGED")
        check()
        result = {"status": "CHECKED_PROOF_COMPLETE_LOCAL_MODULE", "cache_key": key,
            "policy": POLICY, "semantic_id": installation.semantic_id,
            "foundation_id": A.S.foundation_id(), "source_context_root": parent_root,
            "module_name": module_text, "targets": selected,
            "ordered_unit_ids": list(closure.ordered_unit_ids), "artifact_parts": artifact_pins,
            "report_sha256": A.sha(report_raw), "native_cpu_seconds": native_cpu,
            "wall_seconds": time.monotonic()-started, "new_catalog_acceptance": False,
            "trust": "LOCAL_GENERATION_FROM_WARRANTED_EVIDENCE_NOT_REMOTE_BINARY_AUTHORITY",
            "scope": "INIT_ONLY_PROOF_USE_NO_EXECUTABLE_IR_OR_NOTATION_RECONSTRUCTION"}
        save("MODULE.json", result)
        return result
    except BaseException as error:
        failure = ModuleExportError(phase, error, native_cpu, conservative_charge)
        if output is not None:
            try:
                save("FAILURE.json", failure.report)
            except BaseException:
                pass
        raise failure from error
