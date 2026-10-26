"""Focused progress controls; mathematical admissions and protected stores are doubles.

Actual intake loops, path validation and exclusive/fsync record writes are used.
No native operation, database, network, actual owner or mathematical acceptance.
"""
from pathlib import Path
import argparse
from contextlib import ExitStack
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
import socket
import sqlite3
import stat
import subprocess
import sys
import time
import math
from types import ModuleType, SimpleNamespace as NS
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
PACKAGE = LOCAL / "parse-reuse-package01/distribution/package"
START, CPU = time.monotonic(), time.process_time()
MIB = 1024**2
PARENT, SEMANTIC = "a"*64, "c"*64
PINS = {
    "installation/py/ordinary_evidence.py": "fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6",
    "installation/py/ordinary_semantics.py": "ee601536f53640a2695e51d37d3e87e6746604ed6433cb3ace9349ae1aedf915",
    "installation/py/portable_evidence.py": "f8ea819bdd9344d696cef2725888828125b2ef5d1b60d2c31a0412657a62cbd8",
    "installation/py/local_catalog.py": "860a9d731290b2a7fbacd4852bb68185516329ee42845648f4ba3c3856d7c751",
    "installation/py/portable_catalog.py": "aeaf0c7d507baa6b63d401c432ca71557bf29b6b576b1f6cd8381e4e87c7473e",
    "reference/baseline_intake.py": "9b243232603206b3a0925f639a0b8b1a6cbf0de8ca093ad4aa3642c595ff1142",
}


def need(ok, code):
    if not ok:
        raise AssertionError("INTAKE_PROGRESS_CONTROL_"+code)


def check():
    need(time.monotonic()-START < 45 and time.process_time()-CPU < 30, "FINITE_ALLOWANCE")


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def source(name, path, digest=None):
    raw = path.read_bytes()
    need(len(raw) <= MIB and (digest is None or sha(raw) == digest), "SOURCE_PIN:"+str(path))
    module = importlib.util.module_from_spec(importlib.util.spec_from_file_location(name, path))
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def refusal(action, code=None):
    try:
        action()
    except Exception as error:
        if code is not None:
            need(code in str(error), "EXPECTED_REFUSAL:"+code+":"+str(error))
        return error
    raise AssertionError("INTAKE_PROGRESS_CONTROL_EXPECTED_REFUSAL")


class DiagnosticFailure(OSError):
    pass


class OriginalAdmitFailure(ValueError):
    pass


class LimitsDouble:
    """Only metadata ceilings needed by the actual intake loop, not a parser."""
    def __init__(self):
        for key in ("units", "bytes", "nodes", "names", "edges", "binding_bytes"):
            setattr(self, "max_"+key, 64*MIB)
        self.max_batches = 64


class OrdinaryStoreDouble:
    pass


class OrdinaryAdmissionDouble:
    pass


class Model:
    """Tiny inert unit projections; no evidence validity is asserted."""
    def __init__(self, output, label, count, modules, *, admit_fail=None, preflight_fail=None,
                 reuse_all=False):
        self.E, self.C, self.P = modules
        self.trace, self.admit_fail, self.preflight_fail = [], admit_fail, preflight_fail
        self.reuse_all = reuse_all
        self.raws = tuple(("synthetic-unit-%02d" % i).encode() for i in range(count))
        self.entries = tuple(NS(relative_path="u%02d.bin" % i, raw_bytes=len(raw))
                             for i, raw in enumerate(self.raws))
        self.manifest = NS(semantic_id=SEMANTIC, batches=tuple((entry,) for entry in self.entries),
                           unit_count=count, evidence_bytes=sum(map(len, self.raws)), sha256="d"*64)
        self.base = output/label
        self.base.mkdir()
        self.directory = self.base/"owner"
        self.directory.mkdir()
        self.bundle = self.base/"bundle"
        self.bundle.mkdir()
        for entry, raw in zip(self.entries, self.raws):
            (self.bundle/entry.relative_path).write_bytes(raw)
        self.owner = OrdinaryAdmissionDouble()
        self.owner.directory = self.directory
        self.owner.installation = NS(semantic_id=SEMANTIC, root=self.base/"installation",
                                    runtime_roots={"python": self.base/"python"})
        store = OrdinaryStoreDouble()
        store.root = self.base/"custody"
        store.db = NS(execute=lambda *args: NS(fetchone=lambda: None))
        store._export_locators = lambda item, check: [("e"*64, b"inert-locator")]
        store.limits = {key: 64*MIB for key in ("objects", "exports", "logical_bytes")}
        store.status = lambda: {"counts": dict(objects=0, exports=0, logical_bytes=0)}
        self.owner.evidence_store = store
        self.context = {"local_root": PARENT, "semantic_id": SEMANTIC, "bindings": {},
                        "modules": [], "basis_module": [[0, {"$bytes": [66]}]],
                        "root_module": [[0, {"$bytes": [82]}]]}
        self.owner.catalog = NS(_active=lambda: None, _grant=None, _limits=self.C.Limits(),
                               _db=NS(execute=self.catalog_query), context=self.get_context)
        self.owner.preflight, self.owner.admit = self.preflight, self.admit
        self.admit_calls = 0
        self.last_operation = None

    def catalog_query(self, query):
        return NS(fetchone=lambda: (0, 0) if "count(*)," in query else (0,))

    def get_context(self, root):
        self.trace.append(("context", root))
        need(root == PARENT, "MODEL_CONTEXT")
        return deepcopy(self.context)

    def read_manifest(self, raw, digest, **kwargs):
        self.trace.append(("manifest", raw, digest))
        return self.manifest

    def validate_batch(self, entries, raws, **kwargs):
        self.trace.append(("read", tuple(raws)))
        return NS(units=len(raws), bytes=sum(map(len, raws)), nodes=1, names=1, edges=0,
                  binding_bytes=10)

    def plan(self, context, raws, limits, check):
        self.trace.append(("plan", tuple(raws)))
        parsed = {}
        for raw in raws:
            index = self.raws.index(raw)
            name = [[0, {"$bytes": list(("N%d" % index).encode())}]]
            parsed[raw] = NS(raw=raw, unit_id=sha(raw), document={"unit": [None, None, [[name]]]})
        return NS(status="READY", ordered_units=() if self.reuse_all else tuple(raws),
                  reused_unit_ids=tuple(sha(raw) for raw in raws) if self.reuse_all else ()), parsed

    def preflight(self, root, raws, *, budget):
        self.trace.append(("preflight", root, tuple(raws)))
        self.last_operation = budget
        status = "NEEDS" if self.admit_calls == self.preflight_fail else "READY"
        return NS(status=status, raws=tuple(raws))

    def admit(self, root, plan, operation):
        self.trace.append(("admit", root, plan.raws))
        index = self.admit_calls
        self.admit_calls += 1
        operation.worker_cpu = 0.0 if self.reuse_all else 1.25
        if index == self.admit_fail:
            raise OriginalAdmitFailure("ORIGINAL_SYNTHETIC_ADMIT_FAILURE")
        return {"status": "REUSED" if self.reuse_all else "CHECKED",
                "local_root": PARENT if self.reuse_all else sha(("root-%d" % index).encode()),
                "units_checked": 0 if self.reuse_all else len(plan.raws)}

    def patches(self, stack, A, B):
        stack.enter_context(patch.object(A, "_plan_with_parsed", self.plan))
        stack.enter_context(patch.object(B, "read_manifest", self.read_manifest))
        stack.enter_context(patch.object(B, "validate_batch", self.validate_batch))


def budget_for(module):
    # Fixed observed clock avoids timing comparisons; outer harness remains timed.
    module.time = NS(monotonic=lambda: 100.0, process_time=lambda: 10.0)
    return module.IntakeBudget(360, 20000, 64)


def invoke(module, model, A, B, *, record_failure=None):
    with ExitStack() as stack:
        model.patches(stack, A, B)
        if record_failure is not None:
            original = module._Progress.record

            def record(writer, event, **kwargs):
                if record_failure(event, kwargs):
                    raise DiagnosticFailure("SYNTHETIC_DIAGNOSTIC_FAILURE:"+event)
                return original(writer, event, **kwargs)

            stack.enter_context(patch.object(module._Progress, "record", record))
        return module.intake(model.owner, PARENT, model.bundle, b"synthetic-manifest", "d"*64,
                             budget=budget_for(module), calls=module.CallLimits(output_bytes=1024))


def records(model):
    attempts = sorted((model.directory/"intake-diagnostics").iterdir())
    need(len(attempts) == 1 and attempts[0].is_dir(), "ONE_FRESH_ATTEMPT")
    files = sorted(attempts[0].iterdir())
    need(all(p.is_file() for p in files), "RECORD_FILES_ONLY")
    return files, [json.loads(p.read_bytes()) for p in files]


def projection(report):
    return {key: value for key, value in report.items() if key != "progress_directory"}


def run_controls(output):
    forbidden_calls, groups = [], []

    def forbidden(*args, **kwargs):
        forbidden_calls.append("FORBIDDEN")
        raise AssertionError("INTAKE_PROGRESS_FORBIDDEN_EXTERNAL_OPERATION")

    with ExitStack() as barrier:
        for obj, attribute in ((subprocess, "Popen"), (subprocess, "run"),
                (subprocess, "call"), (os, "system"), (sqlite3, "connect"), (socket, "socket")):
            barrier.enter_context(patch.object(obj, attribute, forbidden))
        loaded = {}
        for name in ("ordinary_evidence", "ordinary_semantics", "portable_evidence",
                     "local_catalog", "portable_catalog"):
            relative = "installation/py/"+name+".py"
            loaded[name] = source(name, PACKAGE/relative, PINS[relative])
        E, C, P = (loaded[name] for name in
                   ("ordinary_evidence", "local_catalog", "portable_catalog"))
        barrier.enter_context(patch.object(C.LocalCatalog, "open", forbidden))
        barrier.enter_context(patch.object(P.PortableCatalog, "open", forbidden))
        A, B, O, transport = (ModuleType(name) for name in
                             ("ordinary_admission", "baseline_bundle",
                              "transport.ordinary_acquisition", "transport"))
        A.C, A.E, A.P, A.S = C, E, P, loaded["ordinary_semantics"]
        A.need, A.sha = C.need, sha
        A.OrdinaryAdmission, O.OrdinaryStore = OrdinaryAdmissionDouble, OrdinaryStoreDouble
        A.PreflightLimits, A._plan_with_parsed = NS, forbidden
        A.OperationBudget = lambda wall, cpu, memory, **kw: NS(deadline=100.0+wall, worker_cpu=0.0)
        B.Limits, B.DEFAULT_LIMITS = LimitsDouble, LimitsDouble()
        B.read_manifest, B.validate_batch = forbidden, forbidden
        transport.ordinary_acquisition = O
        barrier.enter_context(patch.dict(sys.modules, {"ordinary_admission": A,
            "baseline_bundle": B, "transport": transport, "transport.ordinary_acquisition": O}))
        before = source("_intake_progress_before", PACKAGE/"reference/baseline_intake.py",
                        PINS["reference/baseline_intake.py"])
        after = source("_intake_progress_after", Path(__file__).parent/"baseline_intake.py")
        modules = E, C, P

        # Actual loops, tiny inert projections. The default no-sink planner stays pure.
        prior = Model(output, "before", 2, modules)
        current = Model(output, "after", 2, modules)
        old_report = invoke(before, prior, A, B)
        new_report = invoke(after, current, A, B)
        need(old_report == projection(new_report) and prior.trace == current.trace, "UNCHANGED_INTAKE")
        need([event[0] for event in current.trace] ==
             ["manifest", "context", "read", "plan", "read", "plan",
              "read", "preflight", "admit", "read", "preflight", "admit"], "CALL_ORDER")
        no_sink = Model(output, "no-sink", 2, modules)
        with ExitStack() as local:
            no_sink.patches(local, A, B)
            args = (no_sink.owner, no_sink.context, no_sink.manifest, no_sink.bundle, B.Limits())
            a = before._plan_all(*args, before.CallLimits(output_bytes=1024), budget_for(before))
            no_sink.trace.clear()
            b = after._plan_all(*args, after.CallLimits(output_bytes=1024), budget_for(after))
        need(a == b and not (no_sink.directory/"intake-diagnostics").exists(), "NO_SINK_DEFAULT")
        groups.append({"name": "unchanged_calls_and_no_sink", "batches": 2,
                       "reads": 4, "plans": 2, "preflights": 2, "admits": 2})

        files, rows = records(current)
        need(new_report["progress_directory"] == str(files[0].parent), "SUCCESS_DIAGNOSTIC_LOCATION")
        expected_events = ["ENTRY", "METADATA_BATCH_BEGIN", "METADATA_BATCH_END",
            "METADATA_BATCH_BEGIN", "METADATA_BATCH_END", "METADATA_COMPLETE"]
        one_batch = ["BATCH_READ_BEGIN", "BATCH_READ_END", "BATCH_PREFLIGHT_BEGIN",
                     "BATCH_PREFLIGHT_END", "ADMIT_INTENT", "BATCH_CONFIRMED"]
        expected_events += one_batch*2+["COMPLETE"]
        expected_batches = [None, 0, 0, 1, 1, None]+[0]*6+[1]*6+[None]
        need([row["event"] for row in rows] == expected_events, "EXACT_EVENT_SEQUENCE")
        expected_fields = {"schema", "authority", "sequence", "event", "batch", "selected_root",
            "manifest_sha256", "selected_root_validated", "last_confirmed_root", "confirmed_batches",
            "possible_unreported_commit", "wall_seconds", "controller_cpu_seconds",
            "native_cpu_reservation_seconds", "observed_worker_cpu_seconds", "worker_cpu_accounting"}
        confirmed_count, confirmed_root = 0, PARENT
        for index, (file, row) in enumerate(zip(files, rows)):
            if row["event"] == "BATCH_CONFIRMED":
                confirmed_root = sha(("root-%d" % confirmed_count).encode())
                confirmed_count += 1
            need(row["batch"] == expected_batches[index] and
                 row["confirmed_batches"] == confirmed_count and
                 row["selected_root_validated"] == (index != 0) and
                 row["last_confirmed_root"] == (confirmed_root if index else None) and
                 row["manifest_sha256"] == ("d"*64 if index else None), "EXACT_RECORD_PREFIX")
            need(set(row) == expected_fields and file.name == f"{index:04d}-{row['event']}.json",
                 "EXACT_RECORD_FIELDS_AND_FILENAME")
            need(row["schema"] == "DMKN_BASELINE_INTAKE_PROGRESS_V1" and
                 row["authority"] == "DIAGNOSTIC_OBSERVATION_NOT_WARRANT_OR_RESUME_CURSOR" and
                 row["worker_cpu_accounting"] == "PARTIAL_OBSERVATION_NOT_COMPLETE_MEASURED_CPU" and
                 row["sequence"] == index and row["selected_root"] == PARENT, "RECORD_IDENTITY")
            need(all(value is None or type(value) in (str, int, float, bool) for value in row.values()),
                 "SCALAR_RECORD")
            for field in ("wall_seconds", "controller_cpu_seconds", "native_cpu_reservation_seconds",
                          "observed_worker_cpu_seconds"):
                need(type(row[field]) in (int, float) and math.isfinite(row[field]) and row[field] >= 0,
                     "FINITE_COST_OBSERVATION")
                need(index == 0 or row[field] >= rows[index-1][field], "MONOTONE_COST_OBSERVATION")
            need(len(file.read_bytes()) <= 2048 and file.read_bytes() == E.canonical_json(row),
                 "EXACT_BOUNDED_CANONICAL_RECORD")
        need(rows[0]["last_confirmed_root"] is None and not rows[0]["selected_root_validated"] and
             all(not row["possible_unreported_commit"] for row in rows), "SUCCESS_UNCERTAINTY")
        confirmed_rows = [row for row in rows if row["event"] == "BATCH_CONFIRMED"]
        need([r["confirmed_batches"] for r in confirmed_rows] == [1, 2] and
             [r["observed_worker_cpu_seconds"] for r in confirmed_rows] == [0.0, 1.25] and
             rows[-1]["observed_worker_cpu_seconds"] == 2.5, "PARTIAL_ACCOUNTING_BOUNDARY")
        groups.append({"name": "exact_scalar_progress", "records": len(rows)})

        # Maximum batch count uses all-reused doubles, within the original spool cap.
        captured, original_init = [], after._Progress.__init__
        def capture(writer, *args):
            original_init(writer, *args)
            captured.append(writer)
        maximum = Model(output, "max-batches", 64, modules, reuse_all=True)
        with patch.object(after._Progress, "__init__", capture):
            maximum_report = invoke(after, maximum, A, B)
        max_files, max_rows = records(maximum)
        need(len(max_rows) == 515 and maximum.admit_calls == 64 and
             maximum_report["local_root"] == PARENT and
             maximum_report["planning"]["native_launches"] == 0, "MAXIMUM_PATH")
        need((after.PROGRESS_MAX_RECORDS, after.PROGRESS_MAX_RECORD_BYTES, after.PROGRESS_MAX_BYTES) ==
             (516, 2048, 1056768), "DERIVED_LIMITS")
        writer = captured[0]
        writer.record("FAILED")  # Artificial final slot: a direct writer guard control only.
        refusal(lambda: writer.record("FAILED"), "BASELINE_PROGRESS_BOUND")
        need(writer.sequence == 516 and len(list(writer.directory.iterdir())) == 516 and
             writer.bytes_reserved <= 1056768, "NO_RECORD_AFTER_CAP")
        cap_model = Model(output, "byte-caps", 1, modules)
        cap_writer = after._Progress(cap_model.directory, PARENT, budget_for(after), after.CallLimits())
        with patch.object(E, "canonical_json", lambda value: b"x"*2049):
            refusal(lambda: cap_writer.record("ENTRY"), "BASELINE_PROGRESS_BOUND")
        cap_writer.bytes_reserved = after.PROGRESS_MAX_BYTES
        refusal(lambda: cap_writer.record("ENTRY"), "BASELINE_PROGRESS_BOUND")
        need(cap_writer.sequence == 0 and not list(cap_writer.directory.iterdir()), "BYTE_CAP_PREWRITE")
        spool_model = Model(output, "spool-cap", 1, modules)
        with ExitStack() as local:
            spool_model.patches(local, A, B)
            cap_calls = after.CallLimits(output_bytes=1024, max_spool_bytes=130*MIB)
            args = (spool_model.owner, spool_model.context, spool_model.manifest, spool_model.bundle,
                    B.Limits(), cap_calls)
            after._plan_all(*args, budget_for(after))
            refusal(lambda: after._plan_all(*args, budget_for(after), progress=lambda *args: None),
                    "BASELINE_SPOOL_RESERVATION")
        groups.append({"name": "derived_record_byte_spool_bounds", "maximum_path_records": 515,
                       "maximum_records": 516, "maximum_record_bytes": 2048,
                       "maximum_total_bytes": 1056768})

        path_model = Model(output, "path-controls", 1, modules)
        with patch.object(after.secrets, "token_hex", lambda count: "1"*32):
            path_writer = after._Progress(path_model.directory, PARENT, budget_for(after), after.CallLimits())
            path_writer.record("ENTRY")
            held = {p.name: p.read_bytes() for p in path_writer.directory.iterdir()}
            refusal(lambda: after._Progress(path_model.directory, PARENT, budget_for(after), after.CallLimits()),
                    "CATALOG_FRESH_REQUIRED")
            need(held == {p.name: p.read_bytes() for p in path_writer.directory.iterdir()}, "NO_OVERWRITE")
        file_model = Model(output, "nondirectory", 1, modules)
        (file_model.directory/"intake-diagnostics").write_bytes(b"retained-not-directory")
        refusal(lambda: after._Progress(file_model.directory, PARENT, budget_for(after), after.CallLimits()),
                "CATALOG_DIRECTORY_REQUIRED")
        constructor_error = refusal(lambda: invoke(after, file_model, A, B))
        need(constructor_error.report["progress_directory"] is None and not file_model.trace and
             constructor_error.report["last_confirmed_root"] is None and
             (file_model.directory/"intake-diagnostics").read_bytes() == b"retained-not-directory",
             "SINK_CONSTRUCTION_FAILURE_HAS_NO_COMPLETED_LOCATION")
        redirect_model = Model(output, "redirect-check-double", 1, modules)
        redirected = redirect_model.directory/"intake-diagnostics"
        redirected.mkdir()
        original_stat = Path.lstat
        def redirected_stat(path, *args, **kwargs):
            if path == redirected:
                return NS(st_mode=stat.S_IFLNK, st_file_attributes=0x400)
            return original_stat(path, *args, **kwargs)
        with patch.object(Path, "lstat", redirected_stat):
            refusal(lambda: after._Progress(redirect_model.directory, PARENT, budget_for(after), after.CallLimits()),
                    "CATALOG_REDIRECTED_PATH")
        io_model = Model(output, "fsync-failure", 1, modules)
        io_writer = after._Progress(io_model.directory, PARENT, budget_for(after), after.CallLimits())
        with patch.object(P.os, "fsync", side_effect=DiagnosticFailure("FSYNC_FAILED")):
            refusal(lambda: io_writer.record("ENTRY"), "FSYNC_FAILED")
        partial = (io_writer.directory/"0000-ENTRY.json").read_bytes()
        need(bool(partial) and io_writer.sequence == 1, "FAILED_WRITE_RETAINED_AND_CHARGED")
        io_writer.record("FAILED")
        need((io_writer.directory/"0000-ENTRY.json").read_bytes() == partial and
             (io_writer.directory/"0001-FAILED.json").is_file(), "NO_FAILED_WRITE_REUSE")
        groups.append({"name": "ordinary_fresh_exclusive_partial_paths", "redirect_stat_is_double": True,
                       "fsync_failure_is_injected": True})

        root0, root1 = (sha(("root-%d" % index).encode()) for index in (0, 1))
        for index in (0, 1):
            model = Model(output, "before-admit-%d" % index, 2, modules)
            error = refusal(lambda: invoke(after, model, A, B, record_failure=
                lambda event, kw: event == "ADMIT_INTENT" and kw["batch"] == index))
            need(isinstance(error, after.IntakeError) and isinstance(error.__cause__, DiagnosticFailure),
                 "PRE_ADMIT_ORIGINAL_CAUSE")
            report = error.report
            need(model.admit_calls == index and len(report["batches"]) == index and
                 report["last_confirmed_root"] == (PARENT if index == 0 else root0) and
                 not report["possible_unreported_commit"], "PRE_ADMIT_PREFIX")
        entry_model = Model(output, "entry-failure", 1, modules)
        entry_error = refusal(lambda: invoke(after, entry_model, A, B,
            record_failure=lambda event, kw: event == "ENTRY"))
        need(entry_error.report["last_confirmed_root"] is None and not entry_model.trace and
             not entry_error.report["selected_root_validated"], "NO_CONTEXT_BEFORE_ENTRY")
        groups.append({"name": "pre_admission_diagnostic_failure", "cases": 3})

        for event, count in (("BATCH_CONFIRMED", 1), ("COMPLETE", 2)):
            model = Model(output, "after-return-"+event.lower(), 2, modules)
            error = refusal(lambda: invoke(after, model, A, B,
                record_failure=lambda name, kw: name == event))
            report = error.report
            need(model.admit_calls == count and len(report["batches"]) == count and
                 report["last_confirmed_root"] == (root0 if count == 1 else root1) and
                 not report["possible_unreported_commit"] and
                 report["resources"]["observed_worker_cpu_seconds"] == count*1.25 and
                 isinstance(error.__cause__, DiagnosticFailure), "POST_RETURN_PREFIX_COST_CAUSE")
            _, failure_rows = records(model)
            need(Path(report["progress_directory"]).parent == model.directory/"intake-diagnostics",
                 "FAILURE_DIAGNOSTIC_LOCATION")
            need(failure_rows[-1]["event"] == "FAILED" and
                 failure_rows[-1]["confirmed_batches"] == count, "POST_RETURN_FAILED_RECORD")
        groups.append({"name": "post_return_and_terminal_failure_preserve_prefix", "cases": 2})

        for terminal_fails in (False, True):
            model = Model(output, "original-error-%s" % terminal_fails, 2, modules, admit_fail=1)
            error = refusal(lambda: invoke(after, model, A, B,
                record_failure=lambda event, kw: terminal_fails and event == "FAILED"))
            report = error.report
            need(isinstance(error.__cause__, OriginalAdmitFailure) and
                 report["error_type"] == "OriginalAdmitFailure" and
                 report["error"] == "ORIGINAL_SYNTHETIC_ADMIT_FAILURE" and
                 report["last_confirmed_root"] == root0 and len(report["batches"]) == 1 and
                 report["possible_unreported_commit"] and model.admit_calls == 2 and
                 report["resources"]["observed_worker_cpu_seconds"] == 2.5,
                 "ORIGINAL_ERROR_AND_UNCERTAIN_SECOND_COMMIT")
            _, failure_rows = records(model)
            need(failure_rows[-1]["event"] == ("ADMIT_INTENT" if terminal_fails else "FAILED"),
                 "TERMINAL_WRITE_FAILURE_NOT_INVENTED")
            if not terminal_fails:
                need(failure_rows[-1]["possible_unreported_commit"], "FAILED_RECORD_UNCERTAINTY")
        old_failure = Model(output, "old-preflight-failure", 2, modules, preflight_fail=1)
        new_failure = Model(output, "new-preflight-failure", 2, modules, preflight_fail=1)
        old_error = refusal(lambda: invoke(before, old_failure, A, B))
        new_error = refusal(lambda: invoke(after, new_failure, A, B))
        need(old_error.report == projection(new_error.report) and old_failure.trace == new_failure.trace and
             not new_error.report["possible_unreported_commit"], "UNCHANGED_PREFLIGHT_FAILURE")
        metadata = Model(output, "metadata-failure", 2, modules)
        metadata_error = refusal(lambda: invoke(after, metadata, A, B,
            record_failure=lambda event, kw: event == "METADATA_BATCH_END"))
        need(metadata_error.report["phase"] == "METADATA_PREFLIGHT" and metadata.admit_calls == 0 and
             metadata_error.report["last_confirmed_root"] == PARENT and
             not metadata_error.report["possible_unreported_commit"], "METADATA_NOT_COMMIT")
        groups.append({"name": "original_error_uncertainty_and_existing_refusals", "cases": 4})
        check()
        need(not forbidden_calls and len(groups) == 7, "ALL_GROUPS_AND_NO_FORBIDDEN_CALLS")
        return {"status": "PASS_FOCUSED_INTAKE_PROGRESS_INERT_CONTROLS", "groups": groups,
                "group_count": len(groups), "forbidden_calls": forbidden_calls,
                "authority": "SYNTHETIC_ADMISSION_CATALOG_CUSTODY_MANIFEST_NO_MATHEMATICAL_ACCEPTANCE",
                "mathematical_acceptance": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize, "PROCESS")
    output = Path(args.output)
    need(output == LOCAL/"intake-progress-controls01/controls" and output.parent.is_dir()
         and not os.path.lexists(output), "FRESH_EXACT_OUTPUT")
    output.mkdir()
    try:
        report = run_controls(output)
    except BaseException as error:
        report = {"status": "FAIL", "error_type": type(error).__name__, "error": str(error),
                  "mathematical_acceptance": False}
    report.update(wall_seconds=time.monotonic()-START, cpu_seconds=time.process_time()-CPU)
    raw = encoded(report)
    need(len(raw) <= MIB, "REPORT_BOUND")
    with (output/"RESULT.json").open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    print(json.dumps(report, sort_keys=True), flush=True)
    return 0 if report["status"] == "PASS_FOCUSED_INTAKE_PROGRESS_INERT_CONTROLS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
