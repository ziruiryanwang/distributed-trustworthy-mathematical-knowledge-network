"""Bounded owner-selected base-index projection, never mathematical admission.

Prepare separately, then serve one retained latest cut with the original
workspace's custody. Calls and workspace ownership are trusted-owner serialized.
No catalogue scan, profile fallback, proof copying, issuer or process is created.
"""
from copy import deepcopy
import hashlib
from importlib import import_module
import json
import math
import time

from discovery import authenticated_index as A
from discovery import formal_features as F
from discovery.discovery_store import LIMITS as INDEX_LIMITS, Store, ordinary
from discovery.module_export_adapter import ModuleExportAdapter
from modules import codec as C

PREPARE_SCHEMA = "DMKN_V5_BASE_PROJECTION_PREPARE_V1"
VIEW_SCHEMA = "DMKN_V5_BASE_PROJECTION_VIEW_V1"
RESULT_SCHEMA = "DMKN_V5_BASE_PROJECTION_RESULT_V1"
COVERAGE = "OWNER_SELECTED_RETAINED_EXPORTS_NOT_ALL_SOURCE_PUBLICATIONS"
MIB = 1024**2
MAX_REPORT = 65536
MAX_EXPORT = 16*MIB
WORK_KEYS = ("node_reads", "node_writes", "new_nodes", "index_hash_steps",
             "node_selects", "node_cache_hits")
WORKSPACE_MODULES = frozenset(("client.workspace_atomic", "client.workspace_mixed",
    "client.workspace_evidence", "client.workspace_staged", "client.workspace_validated"))
BORROW_ATTRIBUTE = "_base_projection_borrow"


def _error(error):
    return {"type": type(error).__name__, "message": str(error)[:500]}


def _tick(deadline):
    if deadline is not None:
        F.need(time.monotonic() < deadline, "PROJECTION_DEADLINE")


def _index_limits(value):
    F.fields(value, INDEX_LIMITS)
    for key, (low, high) in INDEX_LIMITS.items():
        F.uint(value[key], low, high, "PROJECTION_INDEX_LIMIT:"+key)
    return dict(value)


def validate_selector(selector):
    """Pure, closed preflight; no workspace, target or supplied code is opened."""
    F.fields(selector, ("schema", "index_limits", "expected_snapshot_id"))
    F.need(selector["schema"] == VIEW_SCHEMA, "PROJECTION_VIEW_SCHEMA")
    limits = _index_limits(selector["index_limits"])
    return {"schema": VIEW_SCHEMA, "index_limits": limits,
            "expected_snapshot_id": F.hexid(selector["expected_snapshot_id"])}


def _workspace(workspace):
    cls = type(workspace)
    F.need(cls.__module__ in WORKSPACE_MODULES, "PROJECTION_WORKSPACE_TYPE")
    F.need(cls is import_module(cls.__module__).Workspace, "PROJECTION_WORKSPACE_TYPE")
    workspace._active()
    F.need(not workspace._poisoned and workspace._client is None and not workspace._grants,
           "PROJECTION_WORKSPACE_BUSY_OR_POISONED")
    F.need(workspace.db is not None and workspace._lock is not None
           and not workspace._lock.closed, "PROJECTION_WORKSPACE_NOT_OWNED")
    F.need(all(store is not None and store.db is not None
               for store in (workspace.modules, workspace.packets, workspace.index)),
           "PROJECTION_SOURCE_STORE_CLOSED")
    # Presence is not enough: a directly closed SQLite connection must refuse.
    workspace.db.execute("SELECT 1").fetchone()
    F.need(workspace.modules.foundation == workspace.adapter.foundation
           and workspace.modules.policy == workspace.adapter.policy
           and workspace.index.namespace == workspace.adapter.namespace,
           "PROJECTION_SOURCE_ADAPTER_BINDING")
    return ordinary(workspace.root)


def _work(store):
    value = getattr(store, "work", None)
    if type(value) is not dict or any(type(value.get(k)) is not int or value[k] < 0
                                      for k in WORK_KEYS):
        return None
    return {key: value[key] for key in WORK_KEYS}


def _latest(index, deadline=None):
    _tick(deadline)
    status = index.status()
    _tick(deadline)
    snapshot = index.snapshot()
    _tick(deadline)
    identifier = A.snapshot_id(snapshot)
    F.need(identifier == status["latest"] and snapshot["namespace"] == index.namespace
           and snapshot["local_cut"] == status["seq"], "PROJECTION_LATEST_BINDING")
    _tick(deadline)
    return {"snapshot_id": identifier, "local_cut": snapshot["local_cut"]}


class ProjectionCleanupError(RuntimeError):
    def __init__(self, cleanup):
        self.cleanup = deepcopy(cleanup)
        super().__init__("PROJECTION_CLEANUP_FAILED")


class ProjectionOpenError(RuntimeError):
    def __init__(self, error, work, cleanup):
        self.cause = _error(error)
        self.work = deepcopy(work)
        self.cleanup = deepcopy(cleanup)
        super().__init__("PROJECTION_OPEN_FAILED:"+self.cause["message"])


class ProjectionView:
    """One borrow and one actual Store; close before the original workspace.

    The owner must not reserve a client, close the workspace or mutate either
    index during the borrow. The token prevents duplicate helper opens, not
    arbitrary same-process code. Cleanup failure remains a failed operation.
    """
    def __init__(self, workspace, limits, *, create, expected=None, deadline=None):
        _tick(deadline)
        root = _workspace(workspace)
        F.need(getattr(workspace, BORROW_ATTRIBUTE, None) is None,
               "PROJECTION_ALREADY_BORROWED")
        self._workspace, self._token = workspace, object()
        self.closed, self._close_errors = False, []
        self.index = None
        self.constructor_work = None
        self._descriptor = None
        # Acquire before target construction. Retain a real, partially initialized
        # Store so even a constructor's own failing close can be cleaned up.
        setattr(workspace, BORROW_ATTRIBUTE, self._token)
        try:
            adapter = ModuleExportAdapter(C, workspace.modules.foundation, workspace.modules.policy)
            path = ordinary(root/"base-projection-index", fresh=create)
            _tick(deadline)
            self.index = Store.__new__(Store)
            self.index.db = None
            try:
                Store.__init__(self.index, path, adapter, limits, create=create)
            finally:
                self.constructor_work = _work(self.index)
            _tick(deadline)
            selected = _latest(self.index, deadline)
            F.need(expected is None or selected["snapshot_id"] == expected,
                   "PROJECTION_EXPECTED_LATEST")
            self._descriptor = {"schema": VIEW_SCHEMA, "path": str(path),
                "namespace": self.index.namespace, "index_limits": dict(limits),
                **selected, "source_namespace": workspace.index.namespace,
                "coverage": COVERAGE, "mathematical_acceptance": False}
        except BaseException as error:
            try:
                cleanup = self.close()
            except ProjectionCleanupError as tail:
                cleanup = tail.cleanup
            raise ProjectionOpenError(error, self.constructor_work, cleanup) from error

    def descriptor(self):
        F.need(not self.closed and self._descriptor is not None, "PROJECTION_VIEW_CLOSED")
        return deepcopy(self._descriptor)

    def assert_current(self):
        F.need(not self.closed, "PROJECTION_VIEW_CLOSED")
        _workspace(self._workspace)
        F.need(getattr(self._workspace, BORROW_ATTRIBUTE, None) is self._token,
               "PROJECTION_BORROW_CHANGED")
        selected = _latest(self.index)
        F.need(selected == {key: self._descriptor[key] for key in ("snapshot_id", "local_cut")},
               "PROJECTION_SELECTED_CUT_CHANGED")
        return self.descriptor()

    def close(self):
        if not self.closed:
            if self.index is not None:
                try:
                    self.index.close()
                except BaseException as error:
                    self._close_errors.append({"component": "projection", **_error(error)})
                # A failing Store.close must not skip a best-effort direct DB close.
                if getattr(self.index, "db", None) is not None:
                    try:
                        self.index.db.close()
                        self.index.db = None
                    except BaseException as error:
                        self._close_errors.append({"component": "projection_db", **_error(error)})
            known_closed = self.index is None or getattr(self.index, "db", None) is None
            if known_closed:
                if getattr(self._workspace, BORROW_ATTRIBUTE, None) is self._token:
                    setattr(self._workspace, BORROW_ATTRIBUTE, None)
                    self.closed = True
                else:
                    self._close_errors.append({"component": "projection_borrow",
                        "type": "OwnershipChanged", "message": "PROJECTION_BORROW_CHANGED"})
            if not self.closed and not self._close_errors:
                self._close_errors.append({"component": "projection", "type": "CleanupUncertain",
                                           "message": "PROJECTION_CLEANUP_UNCERTAIN"})
        if self._close_errors:
            self._workspace._poisoned = True
            raise ProjectionCleanupError({"closed": self.closed, "errors": self._close_errors})
        return {"closed": True}


def open_view(workspace, selector):
    """Reopen only the fixed base index at its exact authenticated latest cut."""
    selector = validate_selector(selector)
    return ProjectionView(workspace, selector["index_limits"], create=False,
                          expected=selector["expected_snapshot_id"])


def _parameters(context, started):
    from .serve_workspace import MODES
    params = dict(context.parameters)
    F.fields(params, ("schema", "mode", "workspace_path", "workspace_config", "create",
                      "index_limits", "exports", "limits"))
    F.need(params["schema"] == PREPARE_SCHEMA, "PROJECTION_PREPARE_SCHEMA")
    F.need(type(params["mode"]) is str and params["mode"] in MODES, "PROJECTION_MODE")
    F.need(type(params["workspace_config"]) is dict, "PROJECTION_WORKSPACE_CONFIG")
    F.need(type(params["create"]) is bool, "PROJECTION_CREATE")
    params["index_limits"] = _index_limits(params["index_limits"])
    F.fields(params["limits"], ("export_bytes", "wall_seconds"))
    F.uint(params["limits"]["export_bytes"], MAX_EXPORT, 64*MIB, "PROJECTION_EXPORT_ALLOWANCE")
    wall = params["limits"]["wall_seconds"]
    F.need(type(wall) in (int, float) and math.isfinite(wall) and 0 < wall <= 300,
           "PROJECTION_WALL_LIMIT")
    F.need(type(context.deadline) in (int, float) and math.isfinite(context.deadline),
           "PROJECTION_OUTER_DEADLINE")
    deadline = min(started+wall, context.deadline-5)
    _tick(deadline)
    exports = params["exports"]
    F.need(type(exports) is list and 1 <= len(exports) <= 64, "PROJECTION_SELECTION_COUNT")
    identifiers, encoded_bytes = [], 2
    for locator in exports:
        F.fields(locator, ("module_id", "relative_name", "group_index"))
        F.hexid(locator["module_id"])
        C.validate_name(locator["relative_name"])
        F.uint(locator["group_index"], 0, 4095, "PROJECTION_GROUP_INDEX")
        encoded_bytes += len(C.canonical(locator))+1
        F.need(encoded_bytes <= MAX_REPORT+1, "PROJECTION_SELECTION_BYTES")
        identifiers.append(C.export_id(locator["module_id"], locator["relative_name"]))
    F.need(len(set(identifiers)) == len(identifiers), "PROJECTION_DUPLICATE_EXPORT")
    selection = C.canonical(exports)
    F.need(len(selection) <= MAX_REPORT, "PROJECTION_SELECTION_BYTES")
    F.need(type(params["workspace_path"]) is str, "PROJECTION_WORKSPACE_PATH")
    path = ordinary(params["workspace_path"])
    run, work = ordinary(context.run), ordinary(context.location_workspace)
    F.need(work != run and work.is_relative_to(run), "PROJECTION_OUTPUT_SCOPE")
    for value in (context.installation, run, context.sources_v5,
                  context.sources_portable, context.sources_owner):
        root = ordinary(value)
        F.need(not path.is_relative_to(root) and not root.is_relative_to(path),
               "PROJECTION_WORKSPACE_DISJOINT")
    output = ordinary(work/"base-projection-result.json", fresh=True, directory=False)
    _tick(deadline)
    return deepcopy(params), path, output, identifiers, hashlib.sha256(selection).hexdigest(), deadline


def _save(path, report):
    raw = json.dumps(report, sort_keys=True, ensure_ascii=False, separators=(",", ":"),
                     allow_nan=False).encode("utf-8")
    F.need(len(raw) <= MAX_REPORT, "PROJECTION_REPORT_BOUND")
    with path.open("xb") as stream:
        F.need(stream.write(raw) == len(raw), "PROJECTION_REPORT_SHORT_WRITE")


def prepare(context):
    """Materialize one explicit batch; stop at first failure, never retry/repair.

    Preflight raises without opening workspace/target. A missing valid terminal
    report means UNKNOWN batch outcome, including hard kills and report failures.
    Store work counters are not total CPU, disk bytes or mathematical proof cost.
    """
    started, cpu = time.monotonic(), time.process_time()
    params, path, output, identifiers, selection_hash, deadline = _parameters(context, started)
    from .serve_workspace import _types, _close_workspace
    Workspace, unused_provider = _types(params["mode"])
    workspace = view = None
    entered_admit = False
    report = {"schema": RESULT_SCHEMA, "status": "FAILED", "error": None,
        "mode": params["mode"], "workspace_path": str(path), "create": params["create"],
        "selection_sha256": selection_hash, "export_ids": identifiers,
        "source_namespace": None, "target": {"path": str(path/"base-projection-index"),
            "namespace": None, "index_limits": params["index_limits"]},
        "initial": None, "attempted": 0, "acknowledged": [],
        "last_acknowledged_snapshot": None, "snapshot_id": None, "local_cut": None,
        "current_export_id": None, "outcome": "STOPPED_BEFORE_CURRENT_ADMIT",
        "submitted_export_bytes": 0, "export_bytes_limit": params["limits"]["export_bytes"],
        "byte_scope": "CONSERVATIVE_SUBMITTED_EXPORT_READ_ALLOWANCE_NOT_PHYSICAL_IO_OR_RAM",
        "store_work": {"known_totals": {key: 0 for key in WORK_KEYS}, "samples": [], "unknown": []},
        "cleanup": {"projection_closed": False, "workspace_closed": False, "errors": []},
        "started": started, "deadline": deadline, "outer_deadline": context.deadline,
        "coverage": COVERAGE, "mathematical_acceptance": False,
        "unknowns": ["enclosing_Job_total_supplied_by_caller", "final_report_and_exit_tail",
                     "store_counters_exclude_custody_decode_adapter_and_other_controller_work"],
        "hard_containment": "ORIGINAL_CALLER_JOB;DEADLINE_CHECKS_DO_NOT_PREEMPT_SYNCHRONOUS_WORK"}

    def capture(phase, value):
        report["store_work"]["samples"].append({"phase": phase, "work": value})
        if value is None:
            report["store_work"]["unknown"].append(phase)
        else:
            for key in WORK_KEYS:
                report["store_work"]["known_totals"][key] += value[key]

    try:
        _tick(deadline)
        workspace = Workspace.open(path, params["workspace_config"], create=False)
        _tick(deadline)
        report["source_namespace"] = workspace.index.namespace
        try:
            view = ProjectionView(workspace, params["index_limits"], create=params["create"],
                                  deadline=deadline)
        except ProjectionOpenError as error:
            capture("constructor", error.work)
            report["cleanup"]["projection_closed"] = error.cleanup["closed"]
            report["cleanup"]["errors"].extend(error.cleanup.get("errors", []))
            raise
        capture("constructor", view.constructor_work)
        descriptor = view.descriptor()
        report["target"]["namespace"] = descriptor["namespace"]
        report["initial"] = {key: descriptor[key] for key in ("snapshot_id", "local_cut")}
        for locator, identifier in zip(params["exports"], identifiers):
            report["current_export_id"] = identifier
            _tick(deadline)
            F.need(report["submitted_export_bytes"]+MAX_EXPORT <= params["limits"]["export_bytes"],
                   "PROJECTION_EXPORT_ALLOWANCE_EXHAUSTED")
            report["submitted_export_bytes"] += MAX_EXPORT
            report["attempted"] += 1
            opening, unused = workspace.modules.get_group(locator["module_id"],
                locator["relative_name"], locator["group_index"])
            _tick(deadline)
            raw = view.index.adapter.encode_opening(locator["module_id"], locator["relative_name"], opening)
            F.need(type(raw) is bytes and 0 < len(raw) <= MAX_EXPORT, "PROJECTION_EXPORT_BYTE_BOUND")
            report["submitted_export_bytes"] -= MAX_EXPORT-len(raw)
            _tick(deadline)
            entered_admit = True
            previous_work = getattr(view.index, "work", None)
            try:
                result = view.index.admit(raw, expected_id=identifier)
            finally:
                # Every real admit starts a fresh work dictionary. If entry
                # failed before that reset, do not charge the prior primitive
                # a second time or pretend the failing operation cost zero.
                measured = (_work(view.index) if getattr(view.index, "work", None)
                            is not previous_work else None)
                capture("admit:"+str(report["attempted"]), measured)
            F.need(type(result["new"]) is bool and result["record"]["object_id"] == identifier,
                   "PROJECTION_ADMIT_RESULT")
            item = {"export_id": identifier, "new": result["new"],
                    "record_id": F.hexid(result["record_id"]),
                    "snapshot_id": F.hexid(result["snapshot_id"])}
            report["acknowledged"].append(item)
            report["last_acknowledged_snapshot"] = item["snapshot_id"]
            entered_admit = False
            report["current_export_id"] = None
            del raw, opening, result
            _tick(deadline)
        selected = _latest(view.index, deadline)
        F.need(selected["snapshot_id"] == report["last_acknowledged_snapshot"],
               "PROJECTION_FINAL_ACKNOWLEDGED_CUT")
        report.update(selected)
        report["outcome"], report["status"] = "ALL_ACKNOWLEDGED", "PASS"
    except BaseException as error:
        report["error"] = _error(error)
        if entered_admit:
            report["outcome"] = "COMMIT_OUTCOME_UNKNOWN"
        elif len(report["acknowledged"]) == len(identifiers):
            report["outcome"] = "ALL_ACKNOWLEDGED_CUT_UNCONFIRMED"
            report["snapshot_id"], report["local_cut"] = None, None
        if isinstance(error, ProjectionOpenError):
            report["error"]["cause"] = error.cause
    finally:
        errors = report["cleanup"]["errors"]
        if view is not None:
            try:
                report["cleanup"]["projection_closed"] = view.close()["closed"]
            except ProjectionCleanupError as error:
                report["cleanup"]["projection_closed"] = error.cleanup["closed"]
                errors.extend(error.cleanup["errors"])
            except BaseException as error:
                errors.append({"component": "projection", **_error(error)})
        if workspace is not None:
            report["cleanup"]["workspace_closed"] = _close_workspace(workspace, errors)
        if errors or not all(report["cleanup"][key] for key in ("projection_closed", "workspace_closed")):
            report["status"] = "FAILED"
        report["finished"] = time.monotonic()
        report["observed_process_cpu_seconds"] = time.process_time()-cpu
        report["observed_wall_seconds"] = report["finished"]-started
        if report["finished"] >= context.deadline:
            report["status"] = "FAILED"
            errors.append({"component": "deadline", "type": "DeadlineExceeded",
                           "message": "PROJECTION_ORIGINAL_DEADLINE_EXHAUSTED"})
        _save(output, report)
    return report


def main(context):
    return 0 if prepare(context)["status"] == "PASS" else 1
