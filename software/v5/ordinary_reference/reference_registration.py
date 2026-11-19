"""Register an exact ordinary-library realization under an existing checked owner.

No new mathematical admission, certificate, network or source elaboration occurs.
The original library is explicitly owner-approved input. A current protected
context must already warrant the complete selected mathematical closure. The
controller makes one immutable snapshot and performs one live native match;
only its clean, fully bound event can reach the private record-last commit.
"""
from pathlib import Path
import json
import math
import time

import ordinary_admission as A
import ordinary_contribution as G
import baseline_bundle as B
import baseline_snapshot as S
import snapshot_reopen as V
import reference_request as Q
import reference_report as R
import protected_metadata as PM
import reference_store as K

MIB = 1024**2
POLICY = "DMKN_ORDINARY_EXACT_REFERENCE_ABSTRACT_SINGLETON_CLOSED_PUBLIC_BASIS_V1"


def cleanup_known(event):
    return (type(event) is dict and event.get("job_closed") is True and
            event.get("direct_child_reaped") is True and event.get("cleanup_errors") == [] and
            type(event.get("final_job")) is dict and event["final_job"].get("active_processes") == 0)


def support_descriptor(installation, profile, matcher, worker):
    """Common reference/delta support identity; profile verification is separate.

    The installed facade supplies these files from one verified profile. This
    function is not a public API for nominating unverified native executables.
    Future delta source roles must exist before live registration is available;
    the same descriptor then applies to registration and subsequent reuse.
    """
    A.need(type(profile) is G.AuthoringProfile and
           profile.installation_manifest_sha256 == installation.manifest_sha256,
           "REFERENCE_SUPPORT_PROFILE")
    pins = {path: (size, digest) for path, size, digest in profile.file_pins}
    here, package = Path(__file__).absolute().parent, profile.author_worker_script.parent
    A.need(worker == here/"reference_match_worker.py" and matcher.name == "OrdinaryReferenceBase05.exe",
           "REFERENCE_SUPPORT_SELECTED_MATCHER")
    required = {"registration": Path(__file__).absolute(), "match_worker": worker,
                "owner": package/"owner.py", "profile": package/"profile.py"}
    for role, module in (("store", K), ("protected_metadata", PM), ("request", Q),
            ("report", R), ("snapshot", S), ("reopen", V), ("bundle", B),
            ("project_selection", S.X), ("project_bundle", S.X.B), ("contribution", G)):
        required[role] = Path(module.__file__).absolute()
    for role, name in (("delta_native", "ReferenceModule.lean"),
            ("delta_worker", "reference_module_worker.py"), ("closure", "reference_closure.py"),
            ("delta_controller", "reference_module.py")):
        required[role] = here/name
    A.need(all(path in pins for path in (*required.values(), matcher)), "REFERENCE_SUPPORT_PINS")
    helpers = [["matcher/"+matcher.name, *pins[matcher]]]
    native_names = {"OriginalExpr", "OriginalDecl", "CheckedExtension", "BootstrapSupport",
                    "OwnerRebind", "OrdinaryExport", "BaselineArtifactCore04"}
    suffixes = (".olean", ".olean.server", ".olean.private", ".ir.sig", ".ir")
    native_files = {name+suffix for name in native_names for suffix in suffixes}
    found = set()
    for index, directory in enumerate(profile.helper_paths):
        for path, size, digest in profile.file_pins:
            if path.parent == directory and path.name in native_files:
                A.need(path.name not in found, "REFERENCE_SUPPORT_AMBIGUOUS_NATIVE_HELPER")
                found.add(path.name)
                helpers.append([str(index)+"/"+path.relative_to(directory).as_posix(), size, digest])
    A.need({name+".olean" for name in native_names} <= found and
           1 < len(helpers) <= 64 and len({row[0] for row in helpers}) == len(helpers),
           "REFERENCE_SUPPORT_HELPERS")
    return A.E.canonical_json({"schema": "DMKN_LOCAL_ORDINARY_REALIZATION_SUPPORT_V1",
        "installation_manifest_sha256": installation.manifest_sha256,
        "semantic_id": installation.semantic_id, "foundation_id": A.S.foundation_id(),
        "implementation_id": installation.implementation_id, "policy": POLICY,
        "sources": {role: {"bytes": pins[path][0], "sha256": pins[path][1]}
                    for role, path in required.items()}, "native_helpers": sorted(helpers)})


class RegistrationError(RuntimeError):
    def __init__(self, phase, error, native_cpu, conservative_charge):
        self.report = {"phase": phase, "error_type": type(error).__name__, "error": str(error)[:2048],
            "native_cpu_seconds": native_cpu, "conservative_cpu_reservation_charged": conservative_charge,
            "new_catalog_acceptance": False,
            "retention": "PRESERVE_PARTIAL_REFERENCE_NO_AUTOMATIC_RETRY"}
        super().__init__("REFERENCE_REGISTRATION_"+phase+": "+str(error))


def register_reference(owner, parent_root, targets, bundle_directory, manifest_raw, manifest_sha256,
                       project_selection_raw, project_selection_sha256,
                       artifact_report_raw, artifact_report_sha256, *, profile, matcher, worker_script,
                       parent_deadline, make_budget, account_worker_cpu, check_parent):
    """One selected operation; caller retains its real owner's lock throughout.

    Setup, snapshot copying, request validation, matching and commit all consume
    the same original budget. A reusable caller-supplied saved report is never an
    input. `artifact_report_raw` is only an inert locator for an approved project;
    it is not a correspondence or mathematical acceptance report.
    """
    A.need(type(owner) is A.OrdinaryAdmission and type(profile) is G.AuthoringProfile and
           G.A is A and Q.A is A and Q.B is B and S.A is A and V.A is A and V.S is S and
           R.A is A and R.Q is Q and R.S is S and K.A is A and K.R is R and
           K.P is PM and PM.A is A and K.Q is Q and K.V is V and
           R.SCHEMA == "DMKN_ORDINARY_REFERENCE_BASE_REPORT_V2" and
           type(parent_deadline) in (int, float) and math.isfinite(parent_deadline) and
           all(callable(f) for f in (make_budget, account_worker_cpu, check_parent)),
           "REFERENCE_REGISTRATION_CONFIGURATION")
    started = time.monotonic()
    phase, store, grant, budget, committed = "INPUTS", None, None, None, None
    supervision, native_entered, native_cpu, conservative_charge = None, False, 0.0, 0

    def check():
        check_parent()
        A.need(time.monotonic() < parent_deadline, "REFERENCE_REGISTRATION_PARENT_DEADLINE")
        if budget is not None:
            budget.check()

    def exact(raw, digest, maximum, code):
        check()
        A.C.hexid(digest)
        A.need(type(raw) is bytes and 0 < len(raw) <= maximum and A.sha(raw) == digest, code)
        return {"bytes": len(raw), "sha256": digest}

    def save_json(path, value, maximum=MIB):
        check()
        raw = json.dumps(value, sort_keys=True, ensure_ascii=True,
                         allow_nan=False, separators=(",", ":")).encode("ascii")
        A.need(0 < len(raw) <= maximum, "REFERENCE_REGISTRATION_METADATA_BOUND")
        A.P.PortableCatalog._write_fresh(path, raw)
        A.need(A.C.read_bounded(path, maximum) == raw, "REFERENCE_REGISTRATION_METADATA_READBACK")

    try:
        check()
        budget = make_budget()
        A.need(type(budget) is A.OperationBudget and not budget.claimed and budget.worker_cpu == 0 and
               budget.deadline <= parent_deadline and budget.output_bytes >= R.MAX_REPORT and
               budget.log_bytes <= MIB,
               "REFERENCE_REGISTRATION_ORIGINAL_BUDGET")
        check()
        A.C.hexid(parent_root)
        installation = owner.installation
        A.need(profile.installation_manifest_sha256 == installation.manifest_sha256,
               "REFERENCE_REGISTRATION_INSTALLATION")
        matcher, worker = A.C.ordinary(Path(matcher)), A.C.ordinary(Path(worker_script))
        profile.verify(check)
        selected_targets = A.E.strict_json(A.E.canonical_json(targets), A.E.Limits(max_bytes=MIB))
        selected = {"source_context_root": parent_root, "targets": selected_targets,
            "project_selection": exact(project_selection_raw, project_selection_sha256, MIB,
                                       "REFERENCE_REGISTRATION_PROJECT_PIN"),
            "bundle_manifest": exact(manifest_raw, manifest_sha256, 2*MIB,
                                     "REFERENCE_REGISTRATION_BUNDLE_PIN"),
            "artifact_report": exact(artifact_report_raw, artifact_report_sha256, S.MAX_REPORT,
                                     "REFERENCE_REGISTRATION_ARTIFACT_REPORT_PIN")}
        bundle_directory = A.C.ordinary(Path(bundle_directory), directory=True)
        context = owner.catalog.context(parent_root)
        A.need(context["semantic_id"] == installation.semantic_id and
               context["foundation_id"] == A.S.foundation_id(), "REFERENCE_REGISTRATION_CONTEXT")
        # Check the approved project/bundle syntax before creating protected state.
        S.X.selected_project(project_selection_raw, project_selection_sha256, check)
        B.read_manifest(manifest_raw, manifest_sha256, check_budget=check)
        check()
        support = support_descriptor(installation, profile, matcher, worker)
        store = K.open_for_owner(owner, support, check)
        grant = store.reserve_reference(selected, check, deadline=min(parent_deadline, budget.deadline))
        phase = "PREPARE_FINAL_SNAPSHOT"
        prepared = S.prepare_snapshot(installation,
            project_selection_raw=project_selection_raw, project_selection_sha256=project_selection_sha256,
            report_raw=artifact_report_raw, report_sha256=artifact_report_sha256,
            output_directory=grant.directory/"snapshot", spool_bytes=S.MAX_ARTIFACTS+S.METADATA_RESERVATION,
            check_budget=check)
        snapshot = V.read_snapshot(prepared.directory, prepared.manifest_sha256,
                                   installation.manifest_sha256, check_budget=check)
        phase = "CURRENT_WARRANTED_REQUEST"
        request = Q.prepare_request(owner, parent_root, bundle_directory, manifest_raw, manifest_sha256,
            targets=selected_targets, snapshot_id=snapshot.manifest_sha256,
            support_id=store.support_id, check_budget=check)
        inputs = store.bind_reference_inputs(grant, request, snapshot, check)
        A.need(inputs.snapshot_id == snapshot.manifest_sha256 and inputs.request_sha256 == request.sha256,
               "REFERENCE_REGISTRATION_BOUND_INPUTS")
        profile.verify(check)
        phase = "LIVE_NATIVE_CORRESPONDENCE"
        argv = [str(installation.path("python")), "-I", "-S", "-B", str(worker), str(matcher),
                str(installation.runtime_roots["lean_runtime"]/"bin"), str(inputs.inventory_path),
                str(inputs.replay_path), str(inputs.request_path), str(inputs.report_path)]
        budget.claim()
        allowance = installation._supervisor.limits_checked(budget.allowance(parent_deadline))
        try:
            native_entered = True
            supervision = installation._supervisor.supervise(argv, grant.directory,
                grant.directory/"supervision", allowance, installation._job_module.Job)
        finally:
            # Persist uncertain cleanup before a callback or exhausted allowance
            # can prevent safety bookkeeping. This does not renew native work.
            try:
                if not cleanup_known(supervision):
                    store.mark_blocked(grant, "NATIVE_CLEANUP_UNCERTAIN")
            finally:
                final = supervision.get("final_job") if type(supervision) is dict else None
                cpu = final.get("cpu_seconds") if type(final) is dict else None
                if type(cpu) in (int, float) and math.isfinite(cpu) and cpu >= 0:
                    native_cpu = cpu
                    budget.worker_cpu += cpu
                    account_worker_cpu(cpu)
                else:
                    native_cpu, conservative_charge = None, allowance["cpu_seconds"]
                    account_worker_cpu(conservative_charge)
        save_json(inputs.supervision_path, supervision)
        A.need(native_cpu is not None and A._clean_worker(supervision), "REFERENCE_REGISTRATION_NATIVE_NOT_CLEAN")
        phase = "BIND_LIVE_OUTPUT"
        report_raw = A.C.read_bounded(A.C.ordinary(inputs.report_path), R.MAX_REPORT)
        bound = R.bind_report(report_raw, A.sha(report_raw), request=request,
                              replay_request_raw=snapshot.replay_raw, check_budget=check)
        profile.verify(check)
        final_snapshot = V.read_snapshot(snapshot.directory, snapshot.manifest_sha256,
                                        installation.manifest_sha256, check_budget=check)
        A.need(final_snapshot == snapshot and
               A.C.read_bounded(inputs.request_path, Q.MAX_REQUEST) == request.raw and
               A.C.read_bounded(inputs.inventory_path, MIB) == request.inventory_raw,
               "REFERENCE_REGISTRATION_INPUT_CHANGED")
        phase = "PROTECTED_COMMIT"
        committed = store._commit_reference(grant, {"bound_report": bound,
            "snapshot": final_snapshot, "supervision": supervision, "report_raw": report_raw}, check)
        return {"status": "REGISTERED_LOCAL_ORIGINAL_REFERENCE", "reference_id": committed.reference_id,
            "source_context_root": parent_root, "snapshot_id": snapshot.manifest_sha256,
            "support_id": store.support_id, "public_units": len(bound.public_unit_ids),
            "public_names": len(bound.public_bindings), "usable_basis_names": len(bound.usable_basis_keys),
            "native_calls": 1, "native_cpu_seconds": native_cpu,
            "wall_seconds": time.monotonic()-started, "new_catalog_acceptance": False,
            "trust": "PROTECTED_LOCAL_CURRENT_WARRANTS_AND_LIVE_MATCH_NOT_PEER_CERTIFICATE"}
    except BaseException as error:
        failure = RegistrationError(phase, error, native_cpu, conservative_charge)
        if grant is not None and committed is None and (not native_entered or cleanup_known(supervision)):
            try:
                store.abandon(grant, "CLEAN_FAILED_REFERENCE_REGISTRATION")
            except BaseException as closure_error:
                failure.report["closure_error"] = str(closure_error)[:1024]
                failure.report["retention"] = "UNRESOLVED_REFERENCE_RETAINED_NO_RETRY"
        # The store's committed/unknown-commit exceptions carry exact recovery
        # metadata. Do not replace that disposition with a generic failure.
        if isinstance(getattr(error, "report", None), dict):
            failure.report["store_disposition"] = error.report
        if committed is not None:
            failure.report["committed_reference_id"] = committed.reference_id
            failure.report["retention"] = "COMMITTED_REFERENCE_PRESERVED_DESPITE_REPORTING_FAILURE"
        if grant is not None:
            try:
                save_json(grant.directory/"FAILURE.json", failure.report)
            except BaseException:
                pass
        raise failure from error
