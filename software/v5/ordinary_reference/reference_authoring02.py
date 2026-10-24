"""Ordinary owner-approved source over a protected library, then real admission.

Compilation preserves original authoring extensions through Lean's artifact map.
It confers no warrant. A separate exporter cuts only at the warranted public
frontier; the existing binder and admission core check the new mathematics.
Imported elaborator code and source are owner-approved, not security-sandboxed.
"""
from pathlib import Path
import json
import math
import os
import re
import time

import ordinary_admission as A
import ordinary_contribution as G
import portable_candidate as B
import portable_preview as PP
import supervised_library_exchange as X
import reference_registration as RG
import reference_store as K

MIB = 1024**2


def module_text(name):
    A.E.name_key(name)
    A.need(type(name) is list and 1 <= len(name) <= 16, "REFERENCE_AUTHOR_MODULE_NAME")
    parts = []
    for row in name:
        A.need(row[0] == 0, "REFERENCE_AUTHOR_MODULE_STRING")
        value = bytes(row[1]["$bytes"]).decode("ascii")
        A.need(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{0,95}", value) is not None,
               "REFERENCE_AUTHOR_MODULE_IDENTIFIER")
        parts.append(value)
    return ".".join(parts)


def formal_module(text):
    A.need(type(text) is str and re.fullmatch(r"DMKNAuthor_[0-9a-f]{64}", text) is not None,
           "REFERENCE_AUTHOR_FRESH_MODULE_NAME")
    return [[0, {"$bytes": list(text.encode("ascii"))}]]


def parts_for(base):
    return (base, Path(str(base)+".server"), Path(str(base)+".private"),
            base.with_suffix(".ir.sig"), base.with_suffix(".ir"))


def compiler_artifact_path(text):
    """Spell an already authenticated ordinary artifact for the Win32 compiler.

    Lean's frontend setup reader does not add the extended namespace for deep
    artifact names. This is a spelling of the same file, not an alternate path
    authority. Keep dot/space-ended or noncanonical forms unchanged: prefixing
    them can change Win32's referent. Snapshot metadata itself is never rewritten.
    """
    A.need(type(text) is str and 0 < len(text) <= 32768 and "\x00" not in text,
           "REFERENCE_AUTHOR_ARTIFACT_PATH_TEXT")
    if os.name != "nt" or re.match(r"^[A-Z]:\\", text) is None:
        return text
    parts = text[3:].split("\\")
    if any(not part or part in (".", "..") or part.endswith((".", " ")) or "/" in part
           for part in parts):
        return text
    native = "\\\\?\\"+text
    A.need(len(native) <= 32768, "REFERENCE_AUTHOR_NATIVE_PATH_BOUND")
    return native


def setup_document(reference, parent, module):
    """Use existing exact paths, never manufacture a LEAN_PATH snapshot tree."""
    replay = A.E.strict_json(reference.snapshot.replay_raw, A.E.Limits(max_bytes=16*MIB))
    artifacts = {module_text(row["module"]): row["parts"] for row in replay["artifacts"]}
    A.need(len(artifacts) == len(replay["artifacts"]), "REFERENCE_AUTHOR_ORIGINAL_MODULE_COLLISION")
    imports = list(replay["modules"])
    if parent is not None:
        generated = A.E.strict_json(parent.generated_plan_raw, A.E.Limits(max_bytes=4*MIB))
        for row in generated["modules"]:
            name = module_text(row["module_name"])
            A.need(name not in artifacts, "REFERENCE_AUTHOR_GENERATED_MODULE_COLLISION")
            paths = [part["path"] for part in row["artifact_parts"]]
            A.need(len(paths) == 5, "REFERENCE_AUTHOR_GENERATED_PARTS")
            artifacts[name] = [paths[:3], paths[3:]]
        imports = [K.module_name(parent.module_name)]
    A.need(module not in artifacts, "REFERENCE_AUTHOR_OUTPUT_MODULE_COLLISION")
    artifacts = {name: [[compiler_artifact_path(path) for path in row] for row in matrix]
                 for name, matrix in artifacts.items()}
    return {"name": module, "package": None, "isModule": True,
        "imports": [{"module": module_text(name), "importAll": False, "isExported": True, "isMeta": False}
                    for name in imports],
        "importArts": artifacts, "dynlibs": [], "plugins": [], "options": {"Elab.async": False}}, imports


class AuthoringError(RuntimeError):
    def __init__(self, phase, error, accepted, native_cpu, conservative_charge):
        self.report = {"phase": phase, "error_type": type(error).__name__, "error": str(error)[:2048],
            "accepted": accepted, "native_cpu_seconds": native_cpu,
            "conservative_cpu_reservation_charged": conservative_charge,
            "retention": "PRESERVE_ACCEPTED_STATE_AND_ALL_AUTHORING_OUTPUT_NO_AUTOMATIC_RETRY"}
        super().__init__("REFERENCE_AUTHORING_"+phase+": "+str(error))


def contribute_reference(owner, parent_root, source_body, output_names, *, reference_id,
                         parent_delta_id="", output_directory, profile, matcher, match_worker_script,
                         author_worker_script, exporter_source, parent_deadline,
                         make_budget, account_worker_cpu, check_parent):
    """Compile, extract and admit once under one nonrenewing parent ledger.

    Per-stage budgets must come from that same parent's *remaining* allowance.
    The real owner lock remains held throughout. No approved project is edited.
    New extension metadata remains in the owner's retained author artifact; only
    mathematical proof units enter portable publication and delta materialization.
    """
    A.need(type(owner) is A.OrdinaryAdmission and type(profile) is G.AuthoringProfile and
           G.A is A and G.B is B and G.PP is PP and X.A is A and K.A is A and RG.A is A and RG.K is K and
           type(parent_deadline) in (int, float) and math.isfinite(parent_deadline) and
           all(callable(f) for f in (make_budget, account_worker_cpu, check_parent)),
           "REFERENCE_AUTHORING_CONFIGURATION")
    started = time.monotonic()
    phase, current, output, accepted = "INPUTS", None, None, None
    native_cpu, conservative_charge, native_calls = 0.0, 0, 0
    accounting, accounting_errors = [], []
    admission_entered = False
    written_bytes = 0

    def check():
        check_parent()
        A.need(time.monotonic() < parent_deadline, "REFERENCE_AUTHORING_PARENT_DEADLINE")
        if current is not None:
            current.check()

    def operation():
        check_parent()
        budget = make_budget()
        A.need(type(budget) is A.OperationBudget and not budget.claimed and budget.worker_cpu == 0 and
               budget.deadline <= parent_deadline and budget.output_bytes >= 4*MIB and budget.log_bytes <= MIB,
               "REFERENCE_AUTHORING_REMAINING_BUDGET")
        budget.check()
        return budget

    def save(path, value, maximum):
        nonlocal written_bytes
        check()
        raw = value if type(value) is bytes else json.dumps(value, sort_keys=True, ensure_ascii=True,
            allow_nan=False, separators=(",", ":")).encode("ascii")
        A.need(0 < len(raw) <= maximum and written_bytes+len(raw) <= 48*MIB,
               "REFERENCE_AUTHORING_METADATA_BOUND")
        A.P.PortableCatalog._write_fresh(path, raw)
        written_bytes += len(raw)
        A.need(A.C.read_bounded(path, maximum) == raw, "REFERENCE_AUTHORING_METADATA_READBACK")
        return raw

    def charge(seconds, reservation, *, complete):
        """Never mask a stage's original error while settling its allowance.

        A failed admission can leave worker_cpu at its initialized zero even
        after native entry. Reserve that stage's full allowance unless its
        return or supervisor establishes complete accounting. This is a charge,
        not a claim that the reserved processor time was actually consumed.
        """
        nonlocal native_cpu, conservative_charge
        observed = type(seconds) in (int, float) and math.isfinite(seconds) and seconds >= 0
        if observed:
            native_cpu += seconds
        complete = complete and observed
        charged = seconds if complete else reservation
        if not complete:
            conservative_charge += reservation
        accounting.append({"phase": phase, "observed_worker_cpu_seconds": seconds if observed else None,
            "accounting_complete": complete, "charged_cpu_seconds": charged,
            "scope": "MEASURED_NATIVE_CPU" if complete else "PARTIAL_OR_UNKNOWN_FULL_RESERVATION_CHARGED"})
        try:
            account_worker_cpu(charged)
        except BaseException as error:
            accounting_errors.append({"phase": phase, "error_type": type(error).__name__,
                                      "error": str(error)[:2048]})

    def require_accounted():
        A.need(not accounting_errors and all(row["accounting_complete"] for row in accounting),
               "REFERENCE_AUTHORING_INCOMPLETE_CPU_ACCOUNTING")

    try:
        current = operation()
        A.C.hexid(parent_root); A.C.hexid(reference_id)
        A.need(type(parent_delta_id) is str, "REFERENCE_AUTHORING_PARENT_ID")
        if parent_delta_id:
            A.C.hexid(parent_delta_id)
        body, names = G._source(source_body), G._outputs(output_names)
        installation, custody = owner.installation, owner.evidence_store
        A.need(profile.installation_manifest_sha256 == installation.manifest_sha256,
               "REFERENCE_AUTHORING_INSTALLATION")
        profile.verify(check)
        here = Path(__file__).absolute().parent
        worker, exporter = A.C.ordinary(Path(author_worker_script)), A.C.ordinary(Path(exporter_source))
        pins = {path: (size, digest) for path, size, digest in profile.file_pins}
        required = (Path(__file__).absolute(), worker, exporter, here/"ReferenceEnvironment.lean")
        A.need(worker == here/"reference_author_worker.py" and exporter == here/"ReferenceSource.lean" and
               all(path in pins for path in required), "REFERENCE_AUTHORING_SELECTED_SUPPORT")
        support = RG.support_descriptor(installation, profile, A.C.ordinary(Path(matcher)),
                                         A.C.ordinary(Path(match_worker_script)))
        store = K.open_for_owner(owner, support, check)
        context = owner.catalog.context(parent_root)
        parent = store.load_delta(parent_delta_id, context, check) if parent_delta_id else None
        reference = parent.reference if parent is not None else store.load_reference(reference_id, context, check)
        A.need(reference.reference_id == reference_id, "REFERENCE_AUTHORING_PARENT_REFERENCE")
        for name in names:
            A.need(A.E.name_key(name) not in context["bindings"], "REFERENCE_AUTHORING_OUTPUT_ALREADY_WARRANTED")
        output = A.C.ordinary(Path(output_directory), directory=True, fresh=True)
        protected = (installation.root, owner.catalog._root, custody.root,
                     *installation.runtime_roots.values(), *profile.helper_paths)
        A.need(all(not output.is_relative_to(path) and not path.is_relative_to(output) for path in protected) and
               all(not path.is_relative_to(output) for path in pins), "REFERENCE_AUTHORING_OUTPUT_OVERLAP")
        output.mkdir()
        source_root, module_dir, exchange_dir = (output/name for name in ("source", "modules", "extraction"))
        for path in (source_root, module_dir, exchange_dir):
            path.mkdir()
        key = A.sha(b"DMKN-ORDINARY-REFERENCE-AUTHOR-V1\0"+A.E.canonical_json({
            "reference_id": reference_id, "parent_delta_id": parent_delta_id, "context_root": parent_root,
            "source_sha256": A.sha(body), "targets": names}))
        module = "DMKNAuthor_"+key
        name = formal_module(module)
        setup, imports = setup_document(reference, parent, module)
        setup_path, source = output/"setup.json", source_root/(module+".lean")
        setup_raw = save(setup_path, setup, 16*MIB)
        header = "module\nprelude\n"+"".join("public import "+module_text(item)+"\n" for item in imports)
        generated_source = header.encode("ascii")+b"\npublic section\n\n"+body+b"\n"
        save(source, generated_source, 2*MIB)
        generated_raw = (parent.generated_plan_raw if parent is not None else A.E.canonical_json({
            "schema": K.GENERATED_PLAN_SCHEMA, "reference_id": reference_id,
            "support_id": store.support_id, "delta_id": "", "modules": [], "bindings": []}))
        generated_path = output/"generated-plan.json"
        save(generated_path, generated_raw, 4*MIB)
        plan_raw = store.plan(reference, {"path": str(generated_path), "bytes": len(generated_raw),
            "sha256": A.sha(generated_raw)}, parent_delta_id=parent_delta_id)
        plan_path, inventory_path = output/"reference-plan.json", output/"inventory.json"
        save(plan_path, plan_raw, MIB)
        inventory_raw = installation.read("inventory", MIB)
        save(inventory_path, inventory_raw, MIB)
        artifact, author_report = module_dir/(module+".olean"), output/"author-report.json"

        def unchanged():
            check()
            profile.verify(check)
            current_context = owner.catalog.context(parent_root)
            observed_parent = store.load_delta(parent_delta_id, current_context, check) if parent is not None else None
            observed = (observed_parent.reference if observed_parent is not None
                        else store.load_reference(reference_id, current_context, check))
            A.need(observed == reference, "REFERENCE_AUTHORING_REFERENCE_CHANGED")
            if parent is not None:
                # The reference comparison above alone is not a generated-chain check.
                A.need(observed_parent == parent,
                       "REFERENCE_AUTHORING_GENERATED_CHANGED")
            for path, raw, maximum in ((source, generated_source, 2*MIB), (setup_path, setup_raw, 16*MIB),
                    (plan_path, plan_raw, MIB), (generated_path, generated_raw, 4*MIB),
                    (inventory_path, inventory_raw, MIB)):
                A.need(A.C.read_bounded(path, maximum) == raw, "REFERENCE_AUTHORING_INPUT_CHANGED")

        phase = "COMPILE_OWNER_SOURCE"
        argv = [str(installation.path("python")), "-I", "-S", "-B", str(worker),
            str(installation.path("lean")), str(source_root), str(source), str(setup_path), str(artifact), str(author_report)]
        current.claim()
        allowance = installation._supervisor.limits_checked(current.allowance(parent_deadline))
        supervision = None
        try:
            native_calls += 1
            supervision = installation._supervisor.supervise(argv, output, output/"authoring-supervision",
                allowance, installation._job_module.Job)
        finally:
            final = supervision.get("final_job") if type(supervision) is dict else None
            cpu = final.get("cpu_seconds") if type(final) is dict else None
            if type(cpu) in (int, float) and math.isfinite(cpu) and cpu >= 0:
                current.worker_cpu += cpu
            complete = (type(final) is dict and final.get("active_processes") == 0 and
                        final.get("total_processes", 0) >= 1 and
                        supervision.get("direct_child_reaped") is True)
            charge(cpu, allowance["cpu_seconds"], complete=complete)
        require_accounted()
        save(output/"AUTHORING-SUPERVISION.json", supervision, MIB)
        A.need(A._clean_worker(supervision) and
               A.C.ordinary(output/"authoring-supervision/stderr.txt").stat().st_size == 0,
               "REFERENCE_AUTHORING_COMPILER_NOT_CLEAN")
        unchanged()
        compiled = A._writer_json(A.C.read_bounded(A.C.ordinary(author_report), MIB), MIB)
        A.need(type(compiled) is dict and set(compiled) == {"schema", "assurance", "module_name", "source_root",
               "source", "setup", "artifact_parts"} and
               compiled["schema"] == "DMKN_ORDINARY_REFERENCE_AUTHOR_OUTPUT_V1" and
               compiled["assurance"] == "OWNER_APPROVED_SOURCE_OUTPUT_NOT_MATHEMATICAL_ACCEPTANCE" and
               compiled["module_name"] == module and compiled["source_root"] == str(source_root) and
               compiled["source"] == {"path": str(source), "bytes": len(generated_source), "sha256": A.sha(generated_source)} and
               compiled["setup"] == {"path": str(setup_path), "bytes": len(setup_raw), "sha256": A.sha(setup_raw)},
               "REFERENCE_AUTHORING_COMPILE_REPORT")
        parts = parts_for(artifact)
        A.need(type(compiled["artifact_parts"]) is list and len(compiled["artifact_parts"]) == 5 and
               {path.name for path in module_dir.iterdir()} == {path.name for path in parts},
               "REFERENCE_AUTHORING_PART_CENSUS")
        total = 0
        for path, row in zip(parts, compiled["artifact_parts"]):
            A.need(type(row) is dict and set(row) == {"path", "bytes", "sha256"} and row["path"] == str(path),
                   "REFERENCE_AUTHORING_PART_PIN")
            actual = K.file_pin(path, 64*MIB-total, check)
            A.need(row == {"path": str(path), **actual}, "REFERENCE_AUTHORING_PART_CHANGED")
            total += actual["bytes"]
        request = {"schema": "DMKN_ORDINARY_REFERENCE_SOURCE_REQUEST_V1",
            "semantic_id": installation.semantic_id, "foundation_id": A.S.foundation_id(),
            "context_root": parent_root, "reference_id": reference_id, "parent_delta_id": parent_delta_id,
            "reference_plan_sha256": A.sha(plan_raw), "module_name": name, "targets": names,
            "artifact_parts": compiled["artifact_parts"]}
        request_path, candidate_path = output/"source-request.json", output/"candidate.json"
        request_raw = save(request_path, request, MIB)
        current = operation()
        phase = "EXTRACT_NEW_MATHEMATICS"
        usable = set(reference.usable_basis_keys)
        frontier = {key: identity for key, identity in reference.warrant_bindings if key in usable}
        for units in (reference.public_frontier, () if parent is None else parent.frontier):
            for _, outputs in units:
                for key, identity in outputs:
                    A.need(key not in frontier and context["bindings"].get(key) == identity,
                           "REFERENCE_AUTHORING_FRONTIER")
                    frontier[key] = identity

        def lookup(key):
            check()
            identity = frontier.get(key)
            if identity is not None:
                A.need(context["bindings"].get(key) == identity, "REFERENCE_AUTHORING_BOUNDARY_WARRANT")
            return identity

        sysroot = installation.runtime_roots["lean_runtime"]
        env = {key: value for key, value in os.environ.items()
               if not key.upper().startswith(("LEAN", "PYTHON")) and key.upper() != "PATH"}
        env["PATH"] = str(sysroot/"bin")
        env["LEAN_PATH"] = os.pathsep.join(map(str, (sysroot/"lib/lean", *profile.helper_paths)))
        argv = [str(installation.path("lean")), "-DElab.async=false", "-R", str(here), "--run", str(exporter),
                str(sysroot), str(inventory_path), str(request_path), str(plan_path), str(candidate_path)]
        extraction_accounted = False
        try:
            native_calls += 1
            done, answers, protocol_bytes, extraction_supervision = X.exchange(argv, env=env, cwd=output,
                output=exchange_dir, lookup=lookup, parse=A._writer_json, name_key=A.E.name_key,
                budget=current, parent_deadline=parent_deadline, check_parent=check_parent,
                job_type=installation._job_module.Job)
            extraction_accounted = extraction_supervision.get("accounting_complete") is True
        except X.ExchangeError as error:
            extraction_accounted = error.report.get("accounting_complete") is True
            raise
        finally:
            if current.claimed:
                charge(current.worker_cpu, current.cpu_seconds, complete=extraction_accounted)
        require_accounted()
        unchanged()
        for path, expected in zip(parts, compiled["artifact_parts"]):
            A.need(K.file_pin(path, expected["bytes"], check) == {k: expected[k] for k in ("bytes", "sha256")},
                   "REFERENCE_AUTHORING_EXTRACTED_ARTIFACT_CHANGED")
        A.need(A.C.read_bounded(request_path, MIB) == request_raw, "REFERENCE_AUTHORING_REQUEST_CHANGED")
        raw = A.C.read_bounded(A.C.ordinary(candidate_path), 4*MIB)
        candidate = A._writer_json(raw, 4*MIB)
        A.need(len(raw) == done["output_bytes"] and 1 <= done["units"] <= 32 and
               type(candidate) is dict and type(candidate.get("units")) is list and
               len(candidate["units"]) == done["units"] and candidate.get("unresolved_imports") == [],
               "REFERENCE_AUTHORING_CANDIDATE_DONE")
        bindings = {}
        for row in A.E._array(candidate.get("boundary_imports"), maximum=4096):
            boundary_name, identity = A.E._array(row, 2)
            key = A.E.name_key(boundary_name)
            A.C.hexid(identity)
            A.need(key not in bindings and answers.get(key) == identity == frontier.get(key) == context["bindings"].get(key),
                   "REFERENCE_AUTHORING_REACHED_BOUNDARY")
            bindings[key] = identity
        current = operation()
        phase = "BIND_AND_ADMIT"
        bound = B.bind_candidate(raw, semantic_id=installation.semantic_id, foundation_id=A.S.foundation_id(),
            context_root=parent_root, expected_targets=names, prepared_bindings=bindings,
            warranted_symbol=lambda name: context["bindings"].get(A.E.name_key(name)), check_budget=check,
            limits=B.Limits(max_bundle_bytes=4*MIB, max_units=32, max_bindings=4096,
                            max_targets=32, max_total_nodes=131072, max_evidence_bytes=4*MIB))
        A.need(bound.status == "READY", "REFERENCE_AUTHORING_CANDIDATE_NOT_READY")
        published = G.publication_targets(installation.semantic_id, bound.raw_units, names)
        plan = owner.preflight(parent_root, bound.raw_units, budget=current,
            limits=A.PreflightLimits(max_units=32, max_bytes=4*MIB, max_nodes=131072, max_names=4096, max_edges=32768))
        A.need(plan.status == "READY", "REFERENCE_AUTHORING_PREFLIGHT_NOT_READY")
        try:
            admission_entered = True
            accepted = owner.admit(parent_root, plan, current)
        finally:
            charge(current.worker_cpu, current.cpu_seconds, complete=accepted is not None)
        require_accounted()
        A.need(accepted["status"] == "CHECKED" and accepted["units_checked"] == len(bound.raw_units),
               "REFERENCE_AUTHORING_NEW_CHECK_REQUIRED")
        save(output/"ADMISSION.json", accepted, MIB)
        phase = "PUBLICATION_BYTES"
        (output/"previews").mkdir(); (output/"evidence").mkdir()
        items = {item.unit_id: item for item in map(A.PE.read_evidence, bound.raw_units)}
        previews, evidence_rows = [], []
        for target in published:
            check()
            item = items[target["unit_id"]]
            preview = PP.preview_from_evidence(item.raw, target["name"])
            PP.resolve(preview, item.raw)
            custody.put_preview(preview, before_commit=check)
            path = output/"previews"/(target["export_id"]+".json")
            save(path, preview, MIB)
            A.need(custody.get_preview(A.sha(preview), len(preview), check_budget=check) == preview,
                   "REFERENCE_AUTHORING_PREVIEW_READBACK")
            previews.append({**target, "file": str(path), "bytes": len(preview), "sha256": A.sha(preview)})
        for item in items.values():
            path = output/"evidence"/(item.unit_id+".json")
            save(path, item.raw, 4*MIB)
            evidence_rows.append({"unit_id": item.unit_id, "file": str(path), "bytes": len(item.raw), "sha256": A.sha(item.raw)})
        result = {"status": "CHECKED_REFERENCE_SOURCE_CONTRIBUTION", "parent_root": parent_root,
            "local_root": accepted["local_root"], "reference_id": reference_id, "parent_delta_id": parent_delta_id,
            "module_name": module, "targets": published, "units": evidence_rows, "previews": previews,
            "admission": accepted, "lookup_count": done["lookups"], "protocol_bytes": protocol_bytes,
            "source_and_extraction_native_calls": native_calls,
            "admission_native_calls": "ACCOUNTED_BY_EXISTING_ADMISSION_CORE",
            "native_cpu_seconds": native_cpu, "wall_seconds": time.monotonic()-started,
            "cpu_accounting": accounting,
            "original_proofs_reconstructed_for_authoring": False,
            "author_artifacts": compiled["artifact_parts"],
            "metadata_scope": "ORIGINAL_EXTENSIONS_IMPORTED_NEW_EXTENSIONS_RETAINED_ONLY_IN_LOCAL_AUTHOR_ARTIFACT",
            "trust": "REAL_NEW_UNIT_ADMISSION_NOT_COMPILER_OR_SAVED_REPORT_AUTHORITY"}
        save(output/"RESULT.json", result, MIB)
        return result
    except BaseException as error:
        failure = AuthoringError(phase, error, accepted, native_cpu, conservative_charge)
        failure.report.update(cpu_accounting=accounting, accounting_errors=accounting_errors,
            admission_entered=admission_entered,
            possible_unreported_commit=admission_entered and accepted is None,
            recovery=("QUERY_PROTECTED_OWNER_STATUS_DO_NOT_RETRY_ADMISSION"
                      if admission_entered and accepted is None else "PRESERVE_ALL_OUTPUTS_NO_AUTOMATIC_RETRY"))
        if isinstance(getattr(error, "report", None), dict):
            failure.report["stage_detail"] = error.report
        if output is not None:
            try:
                save(output/"FAILURE.json", failure.report, MIB)
            except BaseException:
                pass
        raise failure from error

