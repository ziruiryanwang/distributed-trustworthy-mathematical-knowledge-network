"""One supervised approved-local-library export to an inert baseline bundle.

No mathematical owner/catalog is opened or altered. Runtime and package support
are already owner-adopted inputs, not peer choices. The project-selection pin
authenticates paths/modules, not their transitive artifact contents. Extraction
is not a hostile-artifact sandbox or mathematical acceptance. The finite Python
controller is cooperatively bounded unless its caller also supplies an outer Job.
"""
from __future__ import annotations

import json
import math
import os
from pathlib import Path
import time

import ordinary_admission as A
import ordinary_contribution as G
import library_extraction as X
import baseline_bundle as B


MIB = 1024**2
REQUEST_SCHEMA = "DMKN_ORDINARY_BASELINE_EXPORT_REQUEST_V1"
EXECUTABLE_MAXIMUM = 32*MIB
NATIVE_WRITER_MAXIMUM = 64*MIB
METADATA_MAXIMUM = 2*MIB


class ProductionError(RuntimeError):
    """Retained failure information; never an acceptance or rollback assertion."""

    def __init__(self, report):
        self.report = report
        super().__init__("BASELINE_PRODUCTION_"+report["phase"]+": "+report["error"])


def _operational_bytes(value, maximum=METADATA_MAXIMUM):
    raw = json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False,
                     separators=(",", ":")).encode("ascii")
    A.need(0 < len(raw) <= maximum, "BASELINE_PRODUCTION_METADATA_BOUND")
    return raw


def _finite_nonnegative_cpu(value):
    if type(value) not in (int, float):
        return False
    try:
        return math.isfinite(value) and value >= 0
    except (OverflowError, ValueError):
        return False


def _write_exact(path, raw, maximum, check):
    check()
    A.need(type(raw) is bytes and 0 < len(raw) <= maximum, "BASELINE_PRODUCTION_WRITE_BOUND")
    path = A.C.ordinary(path, fresh=True)
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    check()
    A.need(A.C.read_bounded(path, maximum) == raw, "BASELINE_PRODUCTION_WRITE_READBACK")
    check()
    return {"bytes": len(raw), "sha256": A.sha(raw)}


def _targets(targets, inventory_raw, limits, check):
    A.E._array(targets, maximum=limits.max_targets)
    A.need(bool(targets), "BASELINE_PRODUCTION_TARGETS_REQUIRED")
    inventory = A.E._array(A._writer_json(inventory_raw, MIB), 581)
    basis = {A.E.name_key(A.E._array(row, 5)[0]) for row in inventory}
    A.need(len(basis) == 581, "BASELINE_PRODUCTION_BASIS_CENSUS")
    result, seen, count = [], set(), 2
    for name in targets:
        check()
        key = A.E.name_key(name)
        A.need(key not in seen and key not in basis, "BASELINE_PRODUCTION_UNIQUE_NONBASIS_TARGET")
        count += len(key)+int(bool(result))
        A.need(count <= MIB, "BASELINE_PRODUCTION_TARGET_BYTES")
        seen.add(key)
        result.append(A.E.strict_json(key))
    return result


def _selected_support(installation, profile, check):
    A.need(type(installation) is A.NativeInstallation and type(profile) is G.AuthoringProfile and
           G.A is A and X.A is A and X.G is G and B.E is A.E and B.S is A.S and
           B.PE is A.PE and B.C is G.B,
           "BASELINE_PRODUCTION_LOADED_SUPPORT")
    A.need(profile.installation_manifest_sha256 == installation.manifest_sha256,
           "BASELINE_PRODUCTION_INSTALLATION_BINDING")
    profile.verify(check)
    source = A.C.ordinary(Path(__file__).absolute())
    package = source.parent.parent
    worker = A.C.ordinary(source.parent/"baseline_worker.py")
    executable = A.C.ordinary(package/"bin/BaselineExporter.exe")
    # The profile fixes these roles. No peer record, request or caller filename
    # can substitute a different native program or environment-setting worker.
    pins = {A.C.ordinary(path): (size, digest) for path, size, digest in profile.file_pins}
    required = {source, worker, executable}
    required.update(A.C.ordinary(Path(module.__file__).absolute()) for module in
                    (B, X, X.G, X.B, X.L, X.R, X.X))
    A.need(required <= set(pins) and Path(B.__file__).absolute().parent == source.parent and
           Path(X.__file__).absolute().parent == source.parent,
           "BASELINE_PRODUCTION_PACKAGE_ROLES")
    A.need(0 < pins[executable][0] <= EXECUTABLE_MAXIMUM and 0 < pins[worker][0] <= MIB,
           "BASELINE_PRODUCTION_PROGRAM_BOUND")
    return worker, executable, pins[executable], package


def _census(output, expected, maximum, check):
    """Exact bounded output state at this observation, not a hard disk quota."""
    pending, seen, total, entries = [output], set(), 0, 0
    allowed_directories = {output/"units", output/"supervision"}
    while pending:
        directory = A.C.ordinary(pending.pop(), directory=True)
        with os.scandir(directory) as listing:
            for item in listing:
                check()
                entries += 1
                A.need(entries <= len(expected)+len(allowed_directories),
                       "BASELINE_PRODUCTION_OUTPUT_CENSUS_BOUND")
                path = Path(item.path)
                if item.is_dir(follow_symlinks=False):
                    A.need(path in allowed_directories, "BASELINE_PRODUCTION_UNEXPECTED_DIRECTORY")
                    pending.append(A.C.ordinary(path, directory=True))
                else:
                    path = A.C.ordinary(path)
                    relative = path.relative_to(output).as_posix()
                    A.need(relative in expected and relative not in seen,
                           "BASELINE_PRODUCTION_UNEXPECTED_FILE")
                    size = path.stat().st_size
                    A.need(0 <= size <= expected[relative], "BASELINE_PRODUCTION_OUTPUT_FILE_BOUND")
                    seen.add(relative)
                    total += size
                    A.need(total <= maximum, "BASELINE_PRODUCTION_SPOOL_BOUND")
    A.need(seen == set(expected), "BASELINE_PRODUCTION_MISSING_OUTPUT")
    return {"files": len(seen), "bytes": total}


def produce_bundle(installation, profile, *, project_selection_raw,
                   project_selection_sha256, targets, output_directory, budget,
                   limits=B.DEFAULT_LIMITS):
    """Exactly one selected producer allocation; return inert manifest locators.

    `budget` is a fresh OperationBudget created before calling this function.
    Here output_bytes authorizes the complete finite producer spool, not an
    admission snapshot. Never enlarge the supplied allowance. The caller may
    charge budget.worker_cpu to a larger original envelope; on unknown native
    accounting it contains the full native reservation, never a fictitious zero.
    """
    A.need(type(budget) is A.OperationBudget and not budget.claimed and budget.worker_cpu == 0,
           "BASELINE_PRODUCTION_FRESH_BUDGET")
    A.need(type(limits) is B.Limits, "BASELINE_PRODUCTION_LIMITS")
    limits.__post_init__()
    budget.claim()
    started, phase, output = time.monotonic(), "INPUTS", None
    native_entered, native_grant, native_cpu, supervision = False, 0, 0.0, None
    accounting_complete, closure_known = True, True
    manifest_attempted = False

    def check():
        budget.check()

    try:
        check()
        # The current native exporter/worker has a fixed writer ceiling. A
        # caller-lowered binder bound refuses later; it cannot reserve less
        # than the output the already-selected native producer may leave.
        required_spool = (NATIVE_WRITER_MAXIMUM+limits.max_bytes+limits.max_manifest_bytes+
                          12*MIB+2*budget.log_bytes)
        A.need(budget.output_bytes >= required_spool, "BASELINE_PRODUCTION_SPOOL_RESERVATION")
        project, project_paths = X.selected_project(project_selection_raw,
            project_selection_sha256, check)
        worker, executable, executable_pin, package = _selected_support(installation, profile, check)
        inventory_raw = installation.read("inventory", MIB)
        A.need(A.sha(inventory_raw) == A.S.INVENTORY, "BASELINE_PRODUCTION_FIXED_INVENTORY")
        names = _targets(targets, inventory_raw, limits, check)
        request_raw = A.E.canonical_json({"schema": REQUEST_SCHEMA,
            "project_search_paths": project["project_search_paths"],
            "modules": project["modules"], "targets": names})
        A.need(len(request_raw) <= MIB, "BASELINE_PRODUCTION_REQUEST_BOUND")
        destination = A.C.ordinary(Path(output_directory), directory=True, fresh=True)
        for selected in (package, installation.root, *installation.runtime_roots.values(),
                         *profile.helper_paths, *project_paths):
            selected = A.C.ordinary(selected, directory=True)
            A.need(not destination.is_relative_to(selected) and not selected.is_relative_to(destination),
                   "BASELINE_PRODUCTION_OUTPUT_SUPPORT_OVERLAP")
        check()
        output = destination
        output.mkdir()
        units_directory = A.C.ordinary(output/"units", directory=True, fresh=True)
        units_directory.mkdir()
        expected = {"project-selection.json": MIB, "inventory.json": MIB, "request.json": MIB,
                    "SELECTION.json": METADATA_MAXIMUM, "writer.json": limits.max_writer_bytes,
                    "supervision-result.json": MIB, "supervision/command.json": MIB,
                    "supervision/stdout.txt": budget.log_bytes,
                    "supervision/stderr.txt": budget.log_bytes}
        pins = {}
        pins["project_selection"] = _write_exact(output/"project-selection.json",
            project_selection_raw, MIB, check)
        pins["inventory"] = _write_exact(output/"inventory.json", inventory_raw, MIB, check)
        pins["request"] = _write_exact(output/"request.json", request_raw, MIB, check)
        _write_exact(output/"SELECTION.json", _operational_bytes({
            "schema": "DMKN_ORDINARY_BASELINE_PRODUCTION_SELECTION_V1",
            "assurance": "APPROVED_LOCAL_EXTRACTION_NOT_MATHEMATICAL_ACCEPTANCE",
            "installation_manifest_sha256": installation.manifest_sha256,
            "project_selection_sha256": project_selection_sha256,
            "executable": {"bytes": executable_pin[0], "sha256": executable_pin[1]},
            "request": pins["request"], "inventory": pins["inventory"],
            "limits": vars(limits), "spool_reservation_bytes": budget.output_bytes,
            "minimum_spool_authorization_bytes": required_spool,
            "project_boundary": "OWNER_APPROVED_PATHS_AND_MODULES_NOT_TRANSITIVE_ARTIFACT_PINS"
        }), METADATA_MAXIMUM, check)

        phase = "NATIVE_EXTRACTION"
        sysroot = installation.runtime_roots["lean_runtime"]
        argv = [str(installation.path("python")), "-I", "-S", "-B", str(worker),
                str(sysroot), str(executable_pin[0]), executable_pin[1],
                pins["inventory"]["sha256"], pins["request"]["sha256"]]
        A.need(sum(len(part)+3 for part in argv) <= 30000, "BASELINE_PRODUCTION_ARGV_BOUND")
        supervisor = installation._supervisor
        allowance = supervisor.limits_checked(budget.allowance(budget.deadline))
        native_grant = allowance["cpu_seconds"]
        native_entered, accounting_complete, closure_known = True, False, False
        try:
            supervision = supervisor.supervise(argv, output, output/"supervision",
                allowance, installation._job_module.Job)
        finally:
            final = supervision.get("final_job") if type(supervision) is dict else None
            value = final.get("cpu_seconds") if type(final) is dict else None
            accounting_complete = _finite_nonnegative_cpu(value)
            native_cpu = value if accounting_complete else None
            # No exception or absent final measurement can turn a launch into
            # free work. Unknown accounting stops; its full reservation remains.
            budget.worker_cpu += value if accounting_complete else native_grant
            closure_known = (type(supervision) is dict and type(final) is dict and
                supervision.get("direct_child_reaped") is True and
                supervision.get("job_closed") is True and supervision.get("cleanup_errors") == [] and
                final.get("active_processes") == 0)
        # Preserve the actual returned observation without treating it as a
        # replayable success token. Failure diagnostics use their own bounded path.
        supervisor.save_new(output/"supervision-result.json", supervision)
        A.need(accounting_complete, "BASELINE_PRODUCTION_UNKNOWN_CPU_RESERVATION_RETAINED")
        A.need(closure_known and A._clean_worker(supervision), "BASELINE_PRODUCTION_NATIVE_EVENT_NOT_CLEAN")
        A.need(A.C.ordinary(output/"supervision/stdout.txt").stat().st_size == 0 and
               A.C.ordinary(output/"supervision/stderr.txt").stat().st_size <= budget.log_bytes,
               "BASELINE_PRODUCTION_NATIVE_DIAGNOSTICS")
        check()

        phase = "BINDING"
        for filename, raw in (("project-selection.json", project_selection_raw),
                              ("inventory.json", inventory_raw), ("request.json", request_raw)):
            check()
            A.need(A.C.read_bounded(output/filename, MIB) == raw, "BASELINE_PRODUCTION_INPUT_CHANGED")
        for path in project_paths:
            check()
            A.C.ordinary(path, directory=True)
        writer_raw = A.C.read_bounded(output/"writer.json", limits.max_writer_bytes)
        pins["writer"] = {"bytes": len(writer_raw), "sha256": A.sha(writer_raw)}
        bound = B.bind_writer(writer_raw, inventory_raw, names, limits=limits, check_budget=check)
        phase = "WRITE_EVIDENCE"
        for entries, raws in zip(bound.manifest.batches, bound.batches):
            A.need(len(entries) == len(raws), "BASELINE_PRODUCTION_INTERNAL_BATCH")
            for entry, raw in zip(entries, raws):
                check()
                pin = _write_exact(output.joinpath(*entry.relative_path.split("/")),
                                   raw, limits.max_unit_bytes, check)
                A.need(pin == {"bytes": entry.raw_bytes, "sha256": entry.raw_sha256},
                       "BASELINE_PRODUCTION_INTERNAL_ENTRY")
                expected[entry.relative_path] = entry.raw_bytes

        phase = "FINALIZE_INPUTS"
        profile.verify(check)
        A.need(installation.read("inventory", MIB) == inventory_raw,
               "BASELINE_PRODUCTION_SELECTED_INVENTORY_CHANGED")
        # This only checks selected directory shape, not all project artifacts.
        for path in project_paths:
            check()
            A.C.ordinary(path, directory=True)
        target_rows = [{"name": A.E.strict_json(target.name), "export_id": target.export_id,
                        "unit_id": target.unit_id} for target in bound.targets]
        manifest_pin = {"bytes": len(bound.manifest.raw), "sha256": bound.manifest.sha256}
        prepared = {
            "schema": "DMKN_ORDINARY_BASELINE_PRODUCTION_OBSERVATION_V1",
            "status": "PREPARED_FOR_MANIFEST_WRITE_NOT_COMPLETION",
            "semantic_id": bound.manifest.semantic_id, "mathematical_acceptance": False,
            "manifest": manifest_pin, "targets": target_rows, "pins": pins,
            "census": vars(bound.census), "batches": len(bound.batches),
            "native_cpu_seconds": native_cpu, "native_cpu_charge": budget.worker_cpu,
            "native_accounting_complete": accounting_complete,
            "native_closure_known": closure_known,
            "controller_cpu_seconds_before_manifest": time.process_time()-budget.cpu_started,
            "wall_seconds_before_manifest": time.monotonic()-started,
            "spool_reservation_bytes": budget.output_bytes,
            "retention": "CALLER_OWNS_COMPLETE_AND_PARTIAL_OUTPUT_LIFECYCLE",
            "next_step": "EXPLICIT_STRICT_INTAKE_NOT_AUTOMATIC_ADMISSION",
        }
        _write_exact(output/"PRODUCTION.json", _operational_bytes(prepared), METADATA_MAXIMUM, check)
        expected["PRODUCTION.json"] = METADATA_MAXIMUM
        _census(output, expected, budget.output_bytes, check)
        check()
        phase = "MANIFEST_WRITE"
        manifest_attempted = True
        _write_exact(output/"manifest.json", bound.manifest.raw, limits.max_manifest_bytes, check)
        expected["manifest.json"] = limits.max_manifest_bytes
        final_census = _census(output, expected, budget.output_bytes, check)
        check()
        # No required file is written after the manifest. A late exception may
        # leave it present; recovery must inspect exact bytes, never saved PASS.
        return {**prepared, "status": "PRODUCED_INERT_BASELINE_NOT_ACCEPTED",
                "output_directory": str(output), "manifest_path": str(output/"manifest.json"),
                "final_spool": final_census,
                "controller_cpu_seconds": time.process_time()-budget.cpu_started,
                "wall_seconds": time.monotonic()-started}
    except BaseException as error:
        report = {"schema": "DMKN_ORDINARY_BASELINE_PRODUCTION_FAILURE_V1", "phase": phase,
            "error_type": type(error).__name__, "error": str(error)[:2048],
            "mathematical_acceptance": False, "native_entered": native_entered,
            "native_cpu_seconds": native_cpu, "native_cpu_charge": budget.worker_cpu,
            "native_grant_cpu_seconds": native_grant, "native_accounting_complete": accounting_complete,
            "native_closure_known": closure_known, "manifest_write_attempted": manifest_attempted,
            "manifest_may_exist": manifest_attempted,
            "retry": "NONE_NEW_EXPLICIT_OPERATION_REQUIRED",
            "retention": "ALL_OUTPUTS_PRESERVED_NO_SUCCESS_OR_ROLLBACK_INFERRED"}
        if output is not None:
            # A diagnostic may follow a failed/uncertain manifest write. It is
            # not a required bundle payload or mathematical completion marker.
            try:
                raw = _operational_bytes(report, 65536)
                path = A.C.ordinary(output/"FAILURE.json", fresh=True)
                with path.open("xb") as stream:
                    stream.write(raw)
                    stream.flush()
                    os.fsync(stream.fileno())
            except BaseException:
                pass
        raise ProductionError(report) from error
