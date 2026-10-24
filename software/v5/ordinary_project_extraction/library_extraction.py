"""Explicit installed-Std or approved-project inputs, not acceptance.

Reuse retained authoring, the existing complete-proof extractor, protected
point lookups, and the unchanged portable completion planner. No source build,
remote binary, replay of accepted proofs, automatic admission or parent rebase.
Private artifacts are owner-trusted local inputs; the named runtime pins and
project-selection hash do not authenticate their transitive artifact contents.
Project mode is explicit, locally pinned and distinct from the preserved Std mode.
"""
from __future__ import annotations

import json
import math
import os
from pathlib import Path
import re
import time

import ordinary_admission as A
import ordinary_contribution as G
import portable_candidate as B
import library_completion as L
import retained_preparation as R
import supervised_library_exchange as X

MIB = 1024**2
EXPORTER_MAXIMUM_BYTES = 32*MIB
LIMITS = B.Limits(max_bundle_bytes=4*MIB, max_units=32, max_bindings=4096,
                  max_targets=32, max_total_nodes=131072, max_evidence_bytes=4*MIB)


def selected_exporter(exporter, profile, check):
    """Resolve only the approved local package's fixed executable role.

    The profile was selected by the operator and verified by the public loader;
    candidate/peer data cannot supply this pin or a different executable path.
    """
    profile.verify(check)
    source = A.C.ordinary(Path(__file__).absolute())
    executable = A.C.ordinary(Path(exporter))
    A.need(executable == source.parent.parent/"bin/MissingImportExporter.exe" and
           any(path == source for path, _, _ in profile.file_pins),
           "EXTRACTION_LOCAL_PACKAGE_ROLE")
    pins = [(size, digest) for path, size, digest in profile.file_pins if path == executable]
    A.need(len(pins) == 1, "EXTRACTION_SELECTED_EXECUTABLE")
    size, digest = pins[0]
    A.need(type(size) is int and 0 < size <= EXPORTER_MAXIMUM_BYTES,
           "EXTRACTION_EXECUTABLE_SIZE")
    A.C.hexid(digest)
    raw = A.C.read_bounded(executable, size)
    A.need(len(raw) == size and A.sha(raw) == digest, "EXTRACTION_EXECUTABLE_PIN")
    return executable, {"bytes": size, "sha256": digest}


def selected_modules(modules, *, installed_std=True):
    """Structured module identifiers; only explicit project mode drops Std."""
    A.need(type(installed_std) is bool, "EXTRACTION_MODULE_MODE")
    A.E._array(modules, maximum=16)
    A.need(bool(modules), "EXTRACTION_MODULES_EMPTY")
    result, seen = [], set()
    for name in modules:
        key = A.E.name_key(name)
        A.need(len(key) <= 4096 and 1 <= len(name) <= 16 and key not in seen and
               (not installed_std or name[0] == [0, {"$bytes": [83, 116, 100]}]),
               "EXTRACTION_UNIQUE_INSTALLED_STD_MODULE" if installed_std else
               "EXTRACTION_UNIQUE_PROJECT_MODULE")
        # Lean maps Name string components to filesystem path components.
        # Formal name validity alone permits '..', separators and numeric
        # components; none may escape its selected artifact root here.
        for component in name:
            A.need(component[0] == 0, "EXTRACTION_MODULE_IDENTIFIER")
            encoded = bytes(component[1]["$bytes"])
            # Our ordinary public modules use DMKNBridge_ + a 64-hex digest
            # (75 bytes). Preserve the Std bound; project mode admits these
            # already-generated modules without renaming compiled artifacts.
            A.need(1 <= len(encoded) <= (64 if installed_std else 96) and encoded.isascii(),
                   "EXTRACTION_MODULE_IDENTIFIER")
            part = encoded.decode("ascii")
            A.need(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", part) is not None and
                   not os.path.isreserved(part), "EXTRACTION_MODULE_IDENTIFIER")
        result.append(A.E.strict_json(key)); seen.add(key)
    A.need(len(A.E.canonical_json(result)) <= 65536, "EXTRACTION_MODULE_BYTES")
    return result


def selected_project(raw, expected_sha256, check):
    """Validate an explicit local selection; its pin is not artifact authority.

    Return exact selected strings plus ordinary checked directory Paths. Raw
    components are inspected before Path normalization. This currently supported
    Windows lane rejects UNC/device namespaces and does not recursively census
    artifact contents or claim to sandbox local private artifact deserialization.
    """
    A.need(callable(check) and type(raw) is bytes and 0 < len(raw) <= MIB,
           "EXTRACTION_PROJECT_SELECTION_BOUND")
    A.C.hexid(expected_sha256)
    check()
    A.need(A.sha(raw) == expected_sha256, "EXTRACTION_PROJECT_SELECTION_PIN")
    selection = A.E.strict_json(raw, A.E.Limits(max_bytes=MIB))
    A.need(type(selection) is dict and set(selection) == {
        "schema", "project_search_paths", "modules"} and
        selection["schema"] == "DMKN_ORDINARY_TRUSTED_PROJECT_EXTRACTION_V1",
        "EXTRACTION_PROJECT_SELECTION_FIELDS")
    paths = A.E._array(selection["project_search_paths"], maximum=16)
    A.need(bool(paths) and os.name == "nt", "EXTRACTION_PROJECT_WINDOWS_ROOTS")
    checked, seen = [], set()
    for raw_path in paths:
        check()
        A.need(type(raw_path) is str and 0 < len(raw_path.encode("utf-8")) <= 32768 and
               re.match(r"^[A-Za-z]:[\\/]", raw_path) is not None and
               all(ord(char) >= 32 for char in raw_path) and ";" not in raw_path,
               "EXTRACTION_PROJECT_ROOT_GRAMMAR")
        components = [part for part in re.split(r"[\\/]", raw_path[3:]) if part]
        A.need(len(components)+1 <= 128 and
               all(part not in (".", "..") for part in components),
               "EXTRACTION_PROJECT_ROOT_COMPONENTS")
        path = Path(raw_path)
        A.need(path not in seen, "EXTRACTION_DUPLICATE_PROJECT_ROOT")
        checked.append(A.C.ordinary(path, directory=True))
        seen.add(path)
    modules = selected_modules(selection["modules"], installed_std=False)
    check()
    return {"schema": selection["schema"],
            "project_search_paths": list(paths), "modules": modules}, tuple(checked)


def extract_retained(owner, parent_root, retained_directory, *, request_sha256,
                     candidate_sha256, modules=None, project_selection_raw=None,
                     project_selection_sha256=None, exporter, profile,
                     output_directory, parent_deadline, make_budget,
                     account_worker_cpu, check_parent):
    """Produce pinned inputs consumable by existing `complete`, exactly once.

    Owner/package/runtime/executable selections are local trusted controller
    inputs. Candidate, request and supplement are inert. One current owner
    holds the real parent throughout; no names from the candidate become
    warranted without checking. Caller derives make_budget from its original
    allowance and charges extraction plus later admission if composing them.
    Separate CLI calls are separate explicit operations, not free retries.
    """
    A.need(type(owner) is A.OrdinaryAdmission and G.A is A and X.A is A and
           type(profile) is G.AuthoringProfile and
           type(parent_deadline) in (int, float) and math.isfinite(parent_deadline) and
           all(callable(f) for f in (make_budget, account_worker_cpu, check_parent)),
           "EXTRACTION_OWNER_CONFIGURATION")
    for value in (parent_root, request_sha256, candidate_sha256):
        A.C.hexid(value)
    started = time.monotonic()
    budget = output = None
    phase = "INPUTS"
    native_cpu, conservative_cpu_charge = 0.0, 0

    def check():
        check_parent()
        A.need(time.monotonic() < parent_deadline, "EXTRACTION_PARENT_DEADLINE")
        if budget is not None:
            budget.check()

    def save(filename, value):
        raw = value if type(value) is bytes else A.E.canonical_json(value)
        A.P.PortableCatalog._write_fresh(output/filename, raw)
        return {"bytes": len(raw), "sha256": A.sha(raw)}

    try:
        check()
        project_mode = modules is None
        if project_mode:
            A.need(project_selection_raw is not None and project_selection_sha256 is not None,
                   "EXTRACTION_PROJECT_SELECTION_REQUIRED")
            project, project_paths = selected_project(
                project_selection_raw, project_selection_sha256, check)
            modules = project["modules"]
        else:
            A.need(project_selection_raw is None and project_selection_sha256 is None,
                   "EXTRACTION_EXCLUSIVE_MODE")
            modules = selected_modules(modules)
            project, project_paths = None, ()
        source = A.C.ordinary(Path(retained_directory), directory=True)
        destination = A.C.ordinary(Path(output_directory), directory=True, fresh=True)
        for path in (source, owner.installation.root, *owner.installation.runtime_roots.values(),
                     *project_paths):
            A.need(not destination.is_relative_to(path) and not path.is_relative_to(destination),
                   "EXTRACTION_OUTPUT_SUPPORT_OVERLAP")
        # The calling public facade additionally separates output from catalog
        # and custody. No paths inside metadata are followed here.
        request_raw = A.C.read_bounded(A.C.ordinary(source/"REQUEST.json"), MIB)
        candidate_raw = A.C.read_bounded(A.C.ordinary(source/"candidate.json"), 4*MIB)
        A.need(A.sha(request_raw) == request_sha256 and A.sha(candidate_raw) == candidate_sha256,
               "EXTRACTION_RETAINED_INPUT_PIN")
        request = R._metadata_json(request_raw, check)
        A.need(type(request) is dict and type(request.get("groups")) is int and
               0 <= request["groups"] <= 32, "EXTRACTION_RETAINED_GROUP_COUNT")
        header_raw = A.C.read_bounded(A.C.ordinary(source/"owner-request/header.json"), MIB)
        groups, payload_bytes = [], len(header_raw)
        for index in range(request["groups"]):
            check()
            raw = A.C.read_bounded(A.C.ordinary(source/"owner-request"/f"group-{index:05d}.json"), MIB)
            payload_bytes += len(raw)
            A.need(payload_bytes <= 4*MIB, "EXTRACTION_RETAINED_PAYLOAD_BOUND")
            groups.append(raw)
        targets_raw = A.C.read_bounded(A.C.ordinary(source/"targets.json"), 65536)
        context = owner.catalog.context(parent_root)

        def warranted(name):
            check()
            return context["bindings"].get(A.E.name_key(name))

        prepared = R.reconstruct_preparation(request_raw, header_raw, tuple(groups), targets_raw,
            semantic_id=owner.installation.semantic_id, foundation_id=A.S.foundation_id(),
            context_root=parent_root, warranted_symbol=warranted, check_budget=check)
        bindings = dict(prepared.bindings)
        names = [A.E.strict_json(key) for key in prepared.output_names]
        phase = "BINDING"
        initial = B.bind_candidate(candidate_raw, semantic_id=owner.installation.semantic_id,
            foundation_id=A.S.foundation_id(), context_root=parent_root,
            expected_targets=names, prepared_bindings=bindings, warranted_symbol=warranted,
            limits=LIMITS, check_budget=check)
        A.need(initial.status == "NEEDS_LOCAL_INTERPRETATIONS" and initial.missing_names,
               "EXTRACTION_NOT_NEEDED")
        missing = [A.E.strict_json(key) for key in initial.missing_names]
        A.need(len(missing) <= 32, "EXTRACTION_MISSING_TARGET_BOUND")
        # The existing binder does not expose the original unit count in a
        # NEEDS result. One bounded reread prevents provably futile extraction.
        original = A._writer_json(candidate_raw, 4*MIB)
        capacity = {"units": LIMITS.max_units-len(original["units"]),
                    "bytes": LIMITS.max_bundle_bytes-len(candidate_raw),
                    "encoded_nodes": LIMITS.max_total_nodes-initial.total_nodes}
        A.need(all(type(value) is int and value > 0 for value in capacity.values()),
               "EXTRACTION_NO_SUPPLEMENT_CAPACITY")
        phase = "SUPPORT"
        executable, executable_pin = selected_exporter(exporter, profile, check)
        budget = make_budget()
        A.need(type(budget) is A.OperationBudget and not budget.claimed and
               budget.worker_cpu == 0 and budget.deadline <= parent_deadline,
               "EXTRACTION_REMAINING_BUDGET")
        check()
        output = destination
        output.mkdir()
        pins = {"candidate": save("candidate.json", candidate_raw),
                "targets": save("targets.json", targets_raw),
                "prepared_bindings": save("prepared-bindings.json",
                    [[A.E.strict_json(key), value] for key, value in prepared.bindings])}
        extraction_request = {"schema": "DMKN_ORDINARY_MISSING_IMPORT_REQUEST_V1",
            "profile_id": owner.installation.semantic_id, "basis_id": A.S.foundation_id(),
            "context_id": parent_root, "modules": modules, "targets": missing}
        if project_mode:
            pins["project_selection"] = save("project-selection.json", project_selection_raw)
            extraction_request.update(
                schema="DMKN_ORDINARY_PROJECT_MISSING_IMPORT_REQUEST_V1",
                project_search_paths=project["project_search_paths"],
                project_selection_sha256=project_selection_sha256, capacity=capacity)
        extraction_request_raw = A.E.canonical_json(extraction_request)
        A.need(len(extraction_request_raw) <= MIB, "EXTRACTION_REQUEST_BYTES")
        pins["extraction_request"] = save("request.json", extraction_request_raw)
        selection_record = {"parent_root": parent_root, "original_request_sha256": request_sha256,
            "original_candidate_sha256": candidate_sha256, "modules": modules,
            "missing_targets": missing, "prepared_input_bytes": prepared.input_bytes,
            "prepared_parent_lookups": prepared.parent_lookups,
            "executable_pin": executable_pin,
            "assurance": "SELECTED_LOCAL_INPUTS_NOT_MATHEMATICAL_ACCEPTANCE"}
        if project_mode:
            selection_record.update(
                project_selection_sha256=project_selection_sha256,
                project_search_paths=project["project_search_paths"], capacity=capacity,
                trust_boundary="OWNER_APPROVED_LOCAL_PROJECT_PRIVATE_ARTIFACTS_NOT_PEER_BINARIES")
        save("SELECTION.json", selection_record)
        sysroot = owner.installation.runtime_roots["lean_runtime"]
        env = {key: value for key, value in os.environ.items()
               if not key.upper().startswith(("LEAN", "PYTHON")) and key.upper() != "PATH"}
        env["PATH"] = str(sysroot/"bin")

        def lookup(key):
            check()
            # exchange has already parsed/validated the structured name.
            return context["bindings"].get(key)

        phase = "NATIVE_EXTRACTION"
        try:
            done, answers, protocol_bytes, supervision = X.exchange(
                [str(executable), str(sysroot), str(output/"request.json"), str(output/"supplement.json")],
                env=env, cwd=output, output=output, lookup=lookup, parse=A._writer_json,
                name_key=A.E.name_key, budget=budget, parent_deadline=parent_deadline,
                check_parent=check_parent, job_type=owner.installation._job_module.Job)
        finally:
            # This is the single parent-ledger charge, also on native failure.
            # The exchange report preserves any incomplete-accounting failure;
            # such a failure can never continue to completion/admission.
            if budget.claimed:
                if math.isfinite(budget.worker_cpu) and budget.worker_cpu >= 0:
                    native_cpu = budget.worker_cpu
                    account_worker_cpu(native_cpu)
                else:
                    native_cpu = None
                    conservative_cpu_charge = budget.cpu_seconds
                    account_worker_cpu(conservative_cpu_charge)
                    raise ValueError("EXTRACTION_UNKNOWN_NATIVE_CPU_RESERVATION_CHARGED")
        check()
        phase = "VALIDATE_SUPPLEMENT"
        # Directory-shape revalidation is not a transitive artifact pin. The
        # selected strings remain exact in request/metadata and are not rewritten.
        for path in project_paths:
            check()
            A.C.ordinary(path, directory=True)
        remaining = capacity["bytes"]
        A.need(0 < done["output_bytes"] <= remaining and
               done["units"] <= (capacity["units"] if project_mode else 32),
               "EXTRACTION_PUBLIC_OUTPUT_BOUND")
        raw = A.C.read_bounded(A.C.ordinary(output/"supplement.json"), remaining)
        A.need(len(raw) == done["output_bytes"], "EXTRACTION_DONE_OUTPUT_BYTES")
        supplement = A._writer_json(raw, remaining)
        A.need(type(supplement) is dict and type(supplement.get("units")) is list and
               len(supplement["units"]) == done["units"] and type(supplement.get("stats")) is dict and
               supplement["stats"].get("lookup_count") == done["lookups"], "EXTRACTION_DONE_CENSUS")
        for row in A.E._array(supplement.get("boundary_imports"), maximum=4096):
            name, identity = A.E._array(row, 2)
            key = A.E.name_key(name)
            A.E._hex(identity)
            A.need(answers.get(key) == identity and context["bindings"].get(key) == identity,
                   "EXTRACTION_REPLY_BOUNDARY_BINDING")
        A.need(all(key in answers and answers[key] is None for key in initial.missing_names),
               "EXTRACTION_MISSING_LOOKUPS_REQUIRED")
        # Reuse all combined-lane, portable-label and graph checks. This is
        # bounded repeated planning; the returned plan is still not a warrant.
        plan = L.complete_candidate(candidate_raw, raw, semantic_id=owner.installation.semantic_id,
            foundation_id=A.S.foundation_id(), context_root=parent_root,
            expected_targets=names, prepared_bindings=bindings, warranted_symbol=warranted,
            limits=LIMITS, check_budget=check)
        A.need(plan.status == "READY" and not plan.mathematical_acceptance,
               "EXTRACTION_COMBINED_PLAN")
        profile.verify(check)
        pins["supplement"] = {"bytes": len(raw), "sha256": A.sha(raw)}
        result = {"status": "EXTRACTED_COMPLETION_INPUTS_NOT_ACCEPTED", "parent_root": parent_root,
            "pins": pins, "missing_targets": missing, "supplemental_units": plan.supplemental_units,
            "consumer_units": plan.consumer_units, "lookups": done["lookups"],
            "protocol_bytes": protocol_bytes, "native_cpu_seconds": native_cpu,
            "executable_pin": executable_pin,
            "wall_seconds": time.monotonic()-started,
            "next_operation": "EXPLICIT_COMPLETE_WITH_THESE_INPUTS_AND_SAME_PARENT",
            "mathematical_acceptance": False,
            "trust_boundary": "OWNER_TRUSTED_INSTALLED_STD_PRIVATE_ARTIFACTS_NOT_PEER_BINARIES"}
        if project_mode:
            result.update(project_selection_sha256=project_selection_sha256,
                project_search_paths=project["project_search_paths"], modules=modules,
                capacity=capacity,
                trust_boundary="OWNER_APPROVED_LOCAL_PROJECT_PRIVATE_ARTIFACTS_NOT_PEER_BINARIES")
        # Human/controller metadata includes Boolean fields, not peer evidence.
        A.P.PortableCatalog._write_fresh(output/"EXTRACTION-RESULT.json",
            json.dumps(result, sort_keys=True, ensure_ascii=True, allow_nan=False).encode("ascii"))
        check()
        return result
    except BaseException as error:
        failure = G.ContributionError("EXTRACTION_"+phase, error, None, native_cpu)
        failure.report["native_accounting_complete"] = native_cpu is not None
        failure.report["conservative_cpu_reservation_charged"] = conservative_cpu_charge
        if output is not None:
            try:
                A.P.PortableCatalog._write_fresh(output/"FAILURE.json",
                    json.dumps(failure.report, sort_keys=True, ensure_ascii=True,
                               allow_nan=False).encode("ascii"))
            except BaseException:
                pass
        raise failure from error

