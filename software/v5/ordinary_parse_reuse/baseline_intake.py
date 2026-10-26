"""Finite strict baseline intake over the existing local owner.

The entire manifest is planned before any checking call. Planning bindings are
hypotheses, never warrants. Each real batch is independently preflighted/admitted
against the last confirmed protected root. No report replay, retry, certificate,
source execution, baseline trust waiver or ordinary-project registration.

The controller is cooperative: a public caller must supervise this process for
hard whole-operation limits. Native children retain existing Job containment.
Calls are serialized under the existing owner's lock; no hostile in-process
caller, support mutation or external database mutation is supported.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math
import time

import ordinary_admission as A
from transport import ordinary_acquisition as O
import baseline_bundle as B

MIB = 1024**2


@dataclass(frozen=True)
class CallLimits:
    """Trusted per-batch reservations; never taken from a peer manifest."""
    cpu_seconds: int = 60
    output_bytes: int = 64*MIB
    log_bytes: int = MIB
    max_spool_bytes: int = 2*1024*MIB

    def __post_init__(self):
        for name, low, high in (("cpu_seconds", 2, 200000),
                ("output_bytes", 1, 1024*MIB), ("log_bytes", 1, 8*MIB),
                ("max_spool_bytes", 1, 2*1024*MIB)):
            A.P.uint(getattr(self, name), low, high, "BASELINE_CALL_LIMIT:"+name)


class IntakeBudget:
    """One invocation: finite deadline and nonrefundable native reservations.

    Reserved CPU is authorization accounting, not measured consumption. The full
    child CPU grant stays charged even on exceptions/missing accounting. Reserving
    the whole batch cap (including reuse) deliberately favors simple sound bounds
    over best possible utilization. Controller CPU is additionally charged live.
    """
    def __init__(self, wall_seconds, cpu_seconds, memory_mib, *, active_processes=4):
        A.P.uint(wall_seconds, 35, 3600, "BASELINE_WALL_ALLOCATION")
        A.P.uint(cpu_seconds, 4, 200000, "BASELINE_CPU_ALLOCATION")
        A.P.uint(memory_mib, 1, 8192, "BASELINE_MEMORY_ALLOCATION")
        A.P.uint(active_processes, 2, 8, "BASELINE_PROCESS_ALLOCATION")
        self.started, self.cpu_started = time.monotonic(), time.process_time()
        self.deadline = self.started+wall_seconds
        self.cpu_seconds, self.memory_mib = cpu_seconds, memory_mib
        self.active_processes, self.claimed = active_processes, False
        self.reserved_cpu, self.observed_worker_cpu = 0, 0.0

    def check(self):
        A.need(time.monotonic() < self.deadline and
               time.process_time()-self.cpu_started+self.reserved_cpu < self.cpu_seconds,
               "BASELINE_INVOCATION_EXHAUSTED")

    def claim(self):
        A.need(not self.claimed, "BASELINE_BUDGET_ALREADY_USED")
        self.claimed = True
        self.check()

    def capacity(self, batches, calls):
        self.check()
        A.need(time.process_time()-self.cpu_started+self.reserved_cpu+
               batches*calls.cpu_seconds < self.cpu_seconds,
               "BASELINE_AGGREGATE_CPU_RESERVATION")

    def operation(self, calls):
        self.capacity(1, calls)
        wall = math.floor(self.deadline-time.monotonic())-3
        A.need(wall >= 30, "BASELINE_REMAINING_WALL")
        budget = A.OperationBudget(wall, calls.cpu_seconds, self.memory_mib,
            active_processes=self.active_processes, output_bytes=calls.output_bytes,
            log_bytes=calls.log_bytes)
        budget.deadline = min(budget.deadline, self.deadline)
        self.reserved_cpu += calls.cpu_seconds
        self.check()
        return budget

    def report(self):
        return {"wall_seconds": time.monotonic()-self.started,
            "controller_cpu_seconds": time.process_time()-self.cpu_started,
            "native_cpu_reservation_seconds": self.reserved_cpu,
            "observed_worker_cpu_seconds": self.observed_worker_cpu,
            "worker_cpu_accounting": "PARTIAL_CORE_OBSERVATION_NO_COMPLETENESS_CLAIM",
            "controller_containment": "COOPERATIVE_REQUIRES_OUTER_SUPERVISOR"}


class IntakeError(RuntimeError):
    def __init__(self, report):
        self.report = report
        super().__init__(report["error"])


def _read_batch(directory, entries, limits, check):
    raw_units = []
    for entry in entries:
        check()
        path = A.C.ordinary(directory/entry.relative_path)
        raw_units.append(A.C.read_bounded(path, entry.raw_bytes))
    raws = tuple(raw_units)
    census = B.validate_batch(entries, raws, limits=limits, check_budget=check)
    return raws, census


def _custody_increment(store, item, check):
    """Exact logical quota addition for unchanged OrdinaryStore._put.

    Existing rows are revalidated, not guessed from their key. No write occurs.
    The later real admit still stages/readbacks every supplied unit.
    """
    check()
    row = store.db.execute(
        "SELECT length(raw),raw_sha256 FROM objects WHERE kind='evidence' AND identity=?",
        (item.unit_id,)).fetchone()
    locators = store._export_locators(item, check)
    if row is not None:
        A.need(row == (len(item.raw), A.sha(item.raw)) and
               store.get_evidence(store.semantic_id, item.unit_id, len(item.raw),
                                  check_budget=check) == item.raw,
               "BASELINE_CUSTODY_EXISTING_BYTES")
        for export, locator_raw in locators:
            check()
            held = store.db.execute("SELECT unit_id,locator FROM exports WHERE export_id=?",
                                    (export,)).fetchone()
            A.need(held == (item.unit_id, locator_raw), "BASELINE_CUSTODY_EXISTING_LOCATOR")
        return 0, 0, 0
    return (1, len(locators), len(item.raw)+len("evidence")+128+
            sum(128+len(raw) for _, raw in locators))


def _catalog_capacity(owner, new_batches, final_names, output_bytes, check):
    check()
    catalog = owner.catalog
    catalog._active()
    A.need(catalog._grant is None, "BASELINE_CATALOG_OPERATION_ACTIVE")
    roots = catalog._db.execute("SELECT count(*) FROM roots").fetchone()[0]
    operations, reserved = catalog._db.execute(
        "SELECT count(*),COALESCE(sum(reserved_bytes),0) FROM operations").fetchone()
    imported = catalog._db.execute(
        "SELECT COALESCE(sum(reserved_bytes),0) FROM imports").fetchone()[0]
    limits = catalog._limits
    A.need(roots+new_batches <= limits.max_roots and
           operations+new_batches <= limits.max_operations and
           reserved+imported+new_batches*output_bytes <= limits.max_total_artifact_bytes and
           final_names <= limits.max_names and
           (new_batches == 0 or output_bytes <= limits.max_artifact_bytes),
           "BASELINE_CATALOG_CAPACITY")


def _plan_all(owner, context, manifest, directory, limits, calls, budget):
    """Discard each batch's proof bytes; retain only a bounded binding projection."""
    check = budget.check
    check()
    A.need(manifest.semantic_id == context["semantic_id"] == owner.installation.semantic_id,
           "BASELINE_SEMANTICS")
    projection = {"local_root": context["local_root"], "semantic_id": context["semantic_id"],
                  "bindings": dict(context["bindings"])}
    totals = dict(units=0, bytes=0, nodes=0, names=0, edges=0, binding_bytes=2)
    additions = dict(objects=0, exports=0, logical_bytes=0)
    new_batches = 0
    batch_metadata = []
    plan_bytes = len(A.E.canonical_json(context["modules"]))
    # Future operation paths use 64-hex local tokens. Bound their JSON encoding
    # (including escaping/non-ASCII) with the actual protected directory spelling.
    future_path = str(owner.directory/"operations"/("f"*64)/"chunk.olean")
    future_name = A.C.module_name("f"*64)
    root_name_bound = max((context["root_module"], future_name),
                          key=lambda name: len(A.E.canonical_json(name)))
    worker_plan_overhead = len(A.E.canonical_json({"basis_module": context["basis_module"],
        "root_module": root_name_bound, "modules": []}))-2
    future_module = {"module_name": future_name, "path": future_path,
        "parent_module": future_name, "artifact_bytes": calls.output_bytes,
        "names_count": owner.catalog._limits.max_names}
    module_bound = len(A.E.canonical_json(future_module))+1
    for entries in manifest.batches:
        check()
        raws, census = _read_batch(directory, entries, limits, check)
        previous_names = totals["names"]
        for key in totals:
            value = getattr(census, key)
            if key == "binding_bytes":
                value += -2+int(bool(previous_names and census.names))
            totals[key] += value
            maximum = getattr(limits, "max_"+key)
            A.need(totals[key] <= maximum, "BASELINE_AGGREGATE_"+key.upper())
        plan, parsed = A._plan_with_parsed(projection, raws, A.PreflightLimits(), check)
        A.need(plan.status == "READY", "BASELINE_FORWARD_OR_MISSING_DEPENDENCY")
        added_bindings = []
        for raw in plan.ordered_units:
            check()
            for row in parsed[raw].document["unit"][2]:
                name = row[0]
                symbol = A.S.export_id(manifest.semantic_id, parsed[raw].unit_id, name)
                key = A.E.name_key(name)
                A.need(key not in projection["bindings"], "BASELINE_PROJECTION_CONFLICT")
                projection["bindings"][key] = symbol
                added_bindings.append([name, symbol])
        new = bool(plan.ordered_units)
        if new:
            new_batches += 1
            A.need(len(plan.ordered_units) <= owner.catalog._limits.max_batch_units and
                   sum(map(len, plan.ordered_units)) <= owner.catalog._limits.max_batch_bytes,
                   "BASELINE_CATALOG_BATCH_CAPACITY")
            binding_raw = A.E.canonical_json(added_bindings)
            A.need(len(binding_raw) <= owner.catalog._limits.max_manifest_bytes//2,
                   "BASELINE_CATALOG_BINDING_CAPACITY")
            # Exact schema overhead is < 8 KiB with fixed-size root/operation IDs;
            # input IDs add at most 67 bytes each. This conservative bound avoids
            # a late known manifest-size refusal without fabricating future roots.
            A.need(len(binding_raw)+67*len(plan.ordered_units)+8192 <=
                   owner.catalog._limits.max_manifest_bytes,
                   "BASELINE_CATALOG_RECORD_CAPACITY")
            A.need(plan_bytes <= owner.catalog._limits.max_manifest_bytes,
                   "BASELINE_CATALOG_PLAN_CAPACITY")
            A.need(plan_bytes+worker_plan_overhead <= 16*MIB,
                   "BASELINE_NATIVE_PLAN_CAPACITY")
            plan_bytes += module_bound
        for raw in raws:
            check()
            increment = _custody_increment(owner.evidence_store, parsed[raw], check)
            for key, value in zip(additions, increment):
                additions[key] += value
        batch_metadata.append({"new_units": len(plan.ordered_units),
            "reused_units": len(plan.reused_unit_ids)})
        # The concrete custody locator helper only reads the private parse.
        # Drop all proof-tree aliases before the next batch. A Python loop row
        # otherwise retains its last full inventory declaration after the loop.
        row = None
        del plan, parsed, raws, raw, row, added_bindings
    check()
    A.need(totals["units"] == manifest.unit_count and
           totals["bytes"] == manifest.evidence_bytes, "BASELINE_MANIFEST_TOTALS")
    counts = owner.evidence_store.status()["counts"]
    A.need(all(counts[key]+value <= owner.evidence_store.limits[key]
               for key, value in additions.items()), "BASELINE_CUSTODY_CAPACITY")
    _catalog_capacity(owner, new_batches, len(projection["bindings"]), calls.output_bytes, check)
    budget.capacity(len(manifest.batches), calls)
    # Retained admission-call files, separately from the reserved native snapshot.
    # This is a conservative authorization reservation, not a hard filesystem quota.
    spool_reservation = new_batches*(128*MIB+2*calls.log_bytes)
    A.need(spool_reservation <= calls.max_spool_bytes, "BASELINE_SPOOL_RESERVATION")
    return {"census": totals, "batches": batch_metadata,
            "native_launches": new_batches, "custody_additions": additions,
            "snapshot_reservation_bytes": new_batches*calls.output_bytes,
            "call_spool_reservation_bytes": spool_reservation,
            "planning_only_not_a_warrant": True}


def intake(owner, parent_root, bundle_directory, manifest_raw, manifest_sha256, *,
           budget, limits=B.Limits(), calls=CallLimits()):
    """Read exact inert files and admit a finite confirmed prefix, once.

    Any eligible protected root can be selected, regardless of prior attempt
    ancestry. Reuse follows exact complete identities, not a saved cursor.
    Ordinary authoring correspondence/registration remains a separate operation.
    """
    A.need(type(owner) is A.OrdinaryAdmission and type(owner.evidence_store) is O.OrdinaryStore and
           type(budget) is IntakeBudget and type(limits) is B.Limits and
           type(calls) is CallLimits, "BASELINE_INTAKE_CONFIGURATION")
    A.C.hexid(parent_root)
    budget.claim()
    phase, position, entered = "INPUTS", None, False
    confirmed, observations, planned = parent_root, [], None
    parent_validated = False
    manifest = None
    try:
        directory = A.C.ordinary(Path(bundle_directory), directory=True)
        # Refuse selection inside mutable owner state/support, and vice versa.
        for other in (owner.directory, owner.evidence_store.root, owner.installation.root,
                      *owner.installation.runtime_roots.values()):
            A.need(not directory.is_relative_to(other) and not other.is_relative_to(directory),
                   "BASELINE_INPUT_STATE_OR_SUPPORT_OVERLAP")
        manifest = B.read_manifest(manifest_raw, manifest_sha256,
                                   limits=limits, check_budget=budget.check)
        phase = "METADATA_PREFLIGHT"
        # Mark the selected root confirmed only after the real context validator.
        context = owner.catalog.context(parent_root)
        parent_validated = True
        planned = _plan_all(owner, context, manifest, directory, limits, calls, budget)
        del context
        for position, entries in enumerate(manifest.batches):
            phase, entered = "BATCH_PREFLIGHT", False
            budget.check()
            raws, _ = _read_batch(directory, entries, limits, budget.check)
            operation = budget.operation(calls)
            try:
                actual = owner.preflight(confirmed, raws, budget=operation)
                A.need(actual.status == "READY", "BASELINE_ACTUAL_MISSING_DEPENDENCY")
                budget.check()
                phase, entered = "ADMIT", True
                result = owner.admit(confirmed, actual, operation)
                # Result is from the live owner call, never an input receipt.
                A.need(result["status"] in ("CHECKED", "REUSED"), "BASELINE_ACTUAL_STATUS")
                A.C.hexid(result["local_root"])
                confirmed = result["local_root"]
                entered = False
                observations.append({"batch": position, "status": result["status"],
                    "local_root": confirmed, "units_checked": result["units_checked"]})
            finally:
                # This number is explicitly partial observation, not a refund or
                # proof of zero work if _execute lacks final native accounting.
                if (type(operation.worker_cpu) in (int, float) and
                        math.isfinite(operation.worker_cpu) and operation.worker_cpu >= 0):
                    budget.observed_worker_cpu += operation.worker_cpu
            budget.check()
            del actual, raws
        return {"status": "BASELINE_INTAKE_COMPLETE", "manifest_sha256": manifest.sha256,
            "selected_root": parent_root, "local_root": confirmed,
            "batches": observations, "planning": planned, "resources": budget.report(),
            "ordinary_library_registered": False, "peer_transferable_warrant": False}
    except Exception as error:
        raise IntakeError({"status": "BASELINE_INTAKE_STOPPED", "phase": phase,
            "manifest_sha256": manifest_sha256, "selected_root": parent_root,
            "selected_root_validated": parent_validated,
            "last_confirmed_root": confirmed if parent_validated else None,
            "failed_batch": position, "batches": observations,
            "possible_unreported_commit": entered,
            "recovery": "EXPLICIT_PROTECTED_STATUS_AND_CONTEXT_SELECTION_NO_AUTOMATIC_RETRY",
            "error_type": type(error).__name__, "error": str(error)[:4096],
            "resources": budget.report(), "ordinary_library_registered": False}) from error

