"""One source-selected shared-setup comparison; no automatic execution/retry.

SETUP -> OLD -> RESTORED -> NATIVE run serially in isolated processes. Only a
fresh shared native catalog is used. Saved descriptors identify that local state;
actual catalog/controller validation, not a descriptor, supplies its authority.
Run only under the root-selected original enclosing Windows Job allocation.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import secrets
import sqlite3
import stat
import sys
import time

BOOT, BOOT_CPU = time.monotonic(), time.process_time()
ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PYTHON = Path(r"D:\Python314")
LEAN = ROOT / "software/runtime/lean-4.34.0-windows"
BASE = ROOT / "experiments/v5-local-checks/bounded-investigator-src01/distribution/package"
BUNDLE = ROOT / "experiments/v5-local-checks/concept-theory-b-export-01/bundle"
OLD = ROOT / "experiments/v5-local-checks/grounded-cut-build01/distribution/addition"
RESTORED = ROOT / "experiments/v5-local-checks/grounded-cut-basis-build01/distribution/addition"
PROFILE = "9c41b9a3fe36f7283af130ac6ef290e82c2a78c432980b2bea75ccdcf197a6d4"
OLD_SUPPORT = "8bdcd6bd93b2d3b10d5c1ef01b995893e0c417da57bd848412ddcc0b912e5135"
NEW_SUPPORT = "8c82b587fe81c6da4021d30b67206d967a0ff0f8a953d1f6e6d7441ea51b0028"
GRAPH_SOURCE = "d8c143bfd345abde7302097977a5e9655071257b66ac9f3cc40b0e4bf1288b1a"
MIB = 1024**2
NATIVE_LIMITS = dict(max_roots=8, max_operations=8, max_names=4096,
    max_manifest_bytes=2*MIB, max_artifact_bytes=64*MIB,
    max_total_artifact_bytes=256*MIB, max_db_pages=4096,
    max_batch_bytes=2*MIB, max_batch_units=64)
CUSTODY = dict(objects=128, exports=512, logical_bytes=16*MIB, db_pages=4096)
ORDER = ("SETUP", "OLD", "RESTORED", "NATIVE")
PHASES = {
    "SETUP": {"CUT_SUPPORT_FOR_PURE_GRAPH", "FIXTURE_GRAPH", "COMMON_NATIVE_SETUP",
              "COMMON_PARENT_AUDIT", "FIXTURE_HANDOFF_WRITE"},
    "OLD": {"CUT_SUPPORT_LOAD", "SHARED_INPUT_LOAD", "CUSTODY_ISOLATION",
            "SHARED_PARENT_PRE_AUDIT", "CUT_DERIVATION", "CUT_1", "CUT_2", "POST_RESULT_AUDIT"},
    "RESTORED": {"CUT_SUPPORT_LOAD", "SHARED_INPUT_LOAD", "CUSTODY_ISOLATION",
                 "SHARED_PARENT_PRE_AUDIT", "CUT_DERIVATION", "CUT_1", "CUT_2", "POST_RESULT_AUDIT"},
    "NATIVE": {"SHARED_INPUT_LOAD", "SEQUENTIAL_CUSTODY_ISOLATION", "BATCH_CUSTODY_ISOLATION",
               "SHARED_PARENT_PRE_AUDIT", "NATIVE_1", "NATIVE_2", "NATIVE_BATCH", "POST_RESULT_AUDIT"},
}


def need(ok, code):
    if not ok:
        raise ValueError("BASIS_COMPARE_" + code)


def ordinary(path, *, directory=False, fresh=False):
    path = Path(path)
    need(path.is_absolute() and ".." not in path.parts and len(path.parts) <= 128 and
         len(str(path)) <= 32768, "ABSOLUTE_PATH")
    for item in (*reversed(path.parents), path):
        try:
            info = item.lstat()
        except FileNotFoundError:
            need(item == path and fresh, "MISSING_PATH")
            return path
        need(not stat.S_ISLNK(info.st_mode) and not
             (getattr(info, "st_file_attributes", 0) & 0x400), "PATH_REDIRECTION")
        need(stat.S_ISDIR(info.st_mode) if item != path or directory else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "PATH_KIND")
    need(not fresh, "FRESH_REQUIRED")
    return path


def read(path, maximum, check):
    check()
    path = ordinary(path)
    size = path.stat().st_size
    need(0 < size <= maximum, "READ_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    need(len(raw) == size, "READ_CHANGED")
    check()
    return raw


def pin(raw):
    return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def load(identifier, path, raw):
    need(identifier not in sys.modules, "MODULE_ALREADY_LOADED")
    spec = importlib.util.spec_from_file_location(identifier, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[identifier] = module
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    return module


def operational_json(raw):
    """Own bounded measurement output; floats are not mathematical evidence."""
    def reject_constant(value):
        raise ValueError("BASIS_COMPARE_NONFINITE_OPERATIONAL_JSON:"+value)
    return json.loads(raw, parse_constant=reject_constant)


class Run:
    def __init__(self, args):
        need(30 <= args.wall_seconds <= 360 and 2 <= args.cpu_seconds <= 240 and
             args.memory_mib == 1280, "ORIGINAL_FINITE_CEILING")
        self.args, self.events, self.budgets, self.child_cpu = args, [], [], 0.0
        self.deadline = BOOT + args.wall_seconds
        if args.deadline is not None:
            need(math.isfinite(args.deadline) and BOOT < args.deadline <= self.deadline,
                 "PARENT_DEADLINE")
            self.deadline = args.deadline
        self.phase, self.base, self.graph_module = "SOURCE_AND_SUPPORT_LOAD", None, None
        self.output = ordinary(args.output, directory=True, fresh=True)
        self.source = ordinary(args.source_root, directory=True)
        need(self.output.is_relative_to(ROOT / "experiments") and
             self.source.is_relative_to(ROOT / "experiments") and
             Path(__file__).absolute() == self.source / "compare_workflow.py", "SELECTED_SOURCE_OUTPUT")
        inputs = (self.source, BASE, BUNDLE, OLD, RESTORED, PYTHON, LEAN, self.output)
        for i, left in enumerate(inputs):
            for right in inputs[i+1:]:
                need(not left.is_relative_to(right) and not right.is_relative_to(left), "PATH_OVERLAP")
        helper_path = self.source.parent / "grounded_cut/recursive_workflow.py"
        helper_raw = read(helper_path, 2*MIB, self.check)
        need(pin(helper_raw)["sha256"] == GRAPH_SOURCE, "PURE_GRAPH_SOURCE_PIN")
        self.graph_module = load("_dmkn_compare_graph", helper_path, helper_raw)
        profile_raw = read(BASE / "PROFILE.json", 2*MIB, self.check)
        need(pin(profile_raw)["sha256"] == PROFILE, "PROFILE_PIN")
        descriptor = json.loads(profile_raw)
        owner_raw = read(BASE / "owner.py", 2*MIB, self.check)
        need(pin(owner_raw) == descriptor["files"]["owner.py"], "OWNER_PIN")
        owner = load("_dmkn_compare_owner", BASE / "owner.py", owner_raw)
        loader = owner.bootstrap(BASE, PROFILE, self.check)
        self.base = loader.load(BASE, PROFILE, dict(python_runtime=PYTHON, lean_runtime=LEAN),
                                self.deadline, check_parent=self.check)
        self.A, self.E, self.P, self.O = self.base.A, self.base.A.E, self.base.A.P, self.base.O
        self.output.mkdir()
        self.load_cost = dict(wall_seconds=time.monotonic()-BOOT,
                              controller_cpu_seconds=time.process_time()-BOOT_CPU)

    def used_cpu(self):
        return time.process_time()-BOOT_CPU + self.child_cpu + sum(b.worker_cpu for b in self.budgets)

    def check(self):
        need(time.monotonic() < self.deadline and self.used_cpu() < self.args.cpu_seconds,
             "ORIGINAL_ALLOWANCE")

    def save(self, name, value):
        raw = self.E.canonical_json(value)
        need(len(raw) <= 2*MIB, "REPORT_BOUND")
        self.P.PortableCatalog._write_fresh(self.output / name, raw)
        return pin(raw)

    def allocate(self):
        self.check()
        wall = math.floor(self.deadline-time.monotonic())-5
        cpu = math.floor(self.args.cpu_seconds-self.used_cpu())-1
        need(wall >= 30 and cpu >= 2, "INSUFFICIENT_ORIGINAL_REMAINDER")
        budget = self.A.OperationBudget(wall, cpu, self.args.memory_mib, active_processes=4,
                                       output_bytes=64*MIB, log_bytes=MIB)
        need(budget.deadline < self.deadline, "OPERATION_DEADLINE")
        self.budgets.append(budget)
        return budget

    def interval(self, label, function):
        self.check()
        self.phase = label
        before, cpu, worker = time.monotonic(), time.process_time(), sum(b.worker_cpu for b in self.budgets)
        event = dict(phase=label)
        try:
            value = function()
            event.update(outcome="RETURNED", result=value)
        except BaseException as error:
            event.update(outcome="FAILED_OR_UNCERTAIN", error=(type(error).__name__+":"+str(error))[:2048])
            raise
        finally:
            event.update(wall_seconds=time.monotonic()-before,
                         controller_cpu_seconds=time.process_time()-cpu,
                         known_worker_cpu_seconds=sum(b.worker_cpu for b in self.budgets)-worker)
            event["interval_cpu_seconds"] = event["controller_cpu_seconds"] + event["known_worker_cpu_seconds"]
            self.events.append(event)
            self.save("EVENT-"+str(len(self.events))+".json", event)
        self.check()
        return value

    def cut(self, lane):
        addition, identity = (OLD, OLD_SUPPORT) if lane in ("SETUP", "OLD") else (RESTORED, NEW_SUPPORT)
        raw = read(addition / "CUT-SUPPORT.json", 2*MIB, self.check)
        need(pin(raw)["sha256"] == identity, "CUT_SUPPORT_PIN")
        manifest = self.E.strict_json(raw, self.E.Limits(max_bytes=2*MIB))
        boot_raw = read(addition / "cut_bootstrap.py", 2*MIB, self.check)
        need(pin(boot_raw) == manifest["files"]["cut_bootstrap.py"], "CUT_BOOTSTRAP_PIN")
        boot = load("cut_bootstrap", addition / "cut_bootstrap.py", boot_raw)
        return boot.load(addition, identity, self.base, check=self.check)

    def native(self, shared, custody):
        return self.A.OrdinaryAdmission.open(self.base.installation, Path(shared["native_path"]),
            shared["native_store_id"], custody, limits=self.P.Limits(**NATIVE_LIMITS))

    def shared(self):
        need(self.args.shared is not None and self.args.shared_sha256 is not None, "SHARED_DESCRIPTOR_REQUIRED")
        path = ordinary(self.args.shared)
        need(path.parent.name == "SETUP" and path.parent.parent == self.output.parent,
             "FRESH_SHARED_SIBLING_ONLY")
        raw = read(path, 2*MIB, self.check)
        need(pin(raw)["sha256"] == self.args.shared_sha256, "SHARED_DESCRIPTOR_PIN")
        doc = self.E.strict_json(raw, self.E.Limits(max_bytes=2*MIB))
        need(type(doc) is dict and set(doc) == {"schema", "native_path", "native_store_id",
            "basis_root", "prerequisite_root", "native_limits", "custody_limits", "graph",
            "native_records", "target_names", "inputs"} and
            doc["schema"] == "DMKN_FIXED_BASIS_COMPARE_SHARED_V1" and
            doc["native_limits"] == NATIVE_LIMITS and doc["custody_limits"] == CUSTODY and
            Path(doc["native_path"]) == path.parent / "native", "SHARED_DESCRIPTOR_FIELDS")
        G = self.graph_module
        graph = doc["graph"]
        need(graph["manifest_sha256"] == G.BUNDLE and graph["closure_units"] == 36 and
             graph["prerequisite_units"] == 34 and graph["closure_bytes"] == 274177 and
             graph["prerequisite_bytes"] == 244463 and
             doc["target_names"] == [G.encoded_name("run_extensive"), G.encoded_name("same_constraints_same_run")],
             "SHARED_EXACT_WORKLOAD")
        inputs = {}
        need(set(doc["inputs"]) == set(graph["ordered_units"]) and len(doc["inputs"]) == 36,
             "SHARED_INPUT_CENSUS")
        for uid in graph["ordered_units"]:
            self.P.hexid(uid)
            input_raw = read(path.parent / "inputs" / (uid+".json"), MIB, self.check)
            need(pin(input_raw) == doc["inputs"][uid] == graph["unit_pins"][uid] and
                 self.A.PE.read_evidence(input_raw).unit_id == uid, "SHARED_INPUT_PIN")
            inputs[uid] = input_raw
        return doc, inputs

    def preopen(self, shared, expected_roots):
        """Prevent hidden recovery before the ordinary writer-capable owner open."""
        self.check()
        root = ordinary(shared["native_path"], directory=True)
        need(not os.path.lexists(root / "WITHDRAWN"), "SHARED_WITHDRAWN")
        path = ordinary(root / "catalog.sqlite")
        need(0 < path.stat().st_size <= NATIVE_LIMITS["max_db_pages"]*4096, "SHARED_DB_BOUND")
        need(all(not os.path.lexists(str(path)+suffix) for suffix in ("-wal", "-shm", "-journal")),
             "SHARED_RECOVERY_FORBIDDEN")
        db = sqlite3.connect(path.as_uri()+"?mode=ro", uri=True, isolation_level=None, timeout=1)
        try:
            for pragma in ("trusted_schema=OFF", "query_only=ON", "mmap_size=0"):
                db.execute("PRAGMA "+pragma)
            need(db.execute("SELECT count(*) FROM roots").fetchone()[0] == expected_roots and
                 db.execute("SELECT count(*) FROM operations").fetchone()[0] == expected_roots and
                 db.execute("SELECT count(*) FROM operations WHERE state!='COMMITTED'").fetchone()[0] == 0,
                 "SHARED_EXACT_CLEAN_OPERATIONS")
        finally:
            db.close()
        self.check()

    def populate(self, path, inputs):
        G = self.graph_module
        custody = self.O.OrdinaryStore(path, self.A.S.semantic_id(), CUSTODY, create=True)
        try:
            for uid, raw in inputs.items():
                if uid in (G.FIRST, G.SECOND):
                    continue
                value = custody.put_evidence(raw, before_commit=self.check)
                need(value["identity"] == uid and value["mathematical_acceptance"] is False and
                     custody.get_evidence(self.A.S.semantic_id(), uid, len(raw), check_budget=self.check) == raw,
                     "ISOLATED_INERT_CUSTODY")
            need(custody.status()["counts"]["objects"] == 34, "PREREQUISITE_ONLY_CUSTODY")
        finally:
            custody.close()
        return dict(objects=34, targets=0, mathematical_acceptance=False)

    def inspect_native(self, shared, custody_path, *, expected_roots, endpoints=()):
        self.preopen(shared, expected_roots)
        custody = self.O.OrdinaryStore(custody_path, self.A.S.semantic_id(), CUSTODY)
        native = None
        try:
            native = self.native(shared, custody)
            context = native.catalog.context(shared["prerequisite_root"])
            need(context["basis_root"] == shared["basis_root"] and
                 all(self.E.name_key(n) not in context["bindings"] for n in shared["target_names"]),
                 "SHARED_PREREQUISITE_CONTEXT")
            for root_id, expected in shared["native_records"].items():
                raw, _ = native.catalog._root_row(root_id)
                need(pin(raw) == expected, "SHARED_COMMITTED_ROW_CHANGED")
            for root_id, number in endpoints:
                current = native.catalog.context(root_id)
                for name, export in zip(shared["target_names"][:number], shared["graph"]["target_exports"][:number]):
                    need(current["bindings"].get(self.E.name_key(name)) == export, "NATIVE_EXACT_ENDPOINT")
            return dict(shared_prerequisite_unchanged=True, exact_native_roots=expected_roots,
                        endpoints=[list(item) for item in endpoints])
        finally:
            if native is not None:
                native.close()
            custody.close()

    def audit_custody(self, path, shared):
        custody = self.O.OrdinaryStore(path, self.A.S.semantic_id(), CUSTODY)
        total = 0
        try:
            for uid, expected in shared["inputs"].items():
                raw = custody.get_evidence(self.A.S.semantic_id(), uid, expected["bytes"], check_budget=self.check)
                need(pin(raw) == expected and self.A.PE.read_evidence(raw).unit_id == uid, "FINAL_INERT_CUSTODY")
                total += len(raw)
            need(custody.status()["counts"]["objects"] == 36 and total == 274177, "FINAL_CUSTODY_CENSUS")
            return dict(units=36, bytes=total, mathematical_acceptance=False)
        finally:
            custody.close()


def setup(run):
    G, A, E, P = run.graph_module, run.A, run.E, run.P
    run.interval("CUT_SUPPORT_FOR_PURE_GRAPH", lambda: load_cut_record(run, "SETUP"))
    # The actual support object is retained separately; interval output is inert.
    cut = run.loaded_cut
    graph_result = []
    def fixture_graph():
        graph_result.extend(G.graph(run.base, cut, BUNDLE, run.check))
        return run.save("INPUT-GRAPH.json", graph_result[0])
    run.interval("FIXTURE_GRAPH", fixture_graph)
    graph, prerequisites, targets, names = graph_result
    native_path, custody_path = run.output / "native", run.output / "setup-custody"
    native_id = secrets.token_hex(32)
    shared = dict(schema="DMKN_FIXED_BASIS_COMPARE_SHARED_V1", native_path=str(native_path),
        native_store_id=native_id, native_limits=NATIVE_LIMITS, custody_limits=CUSTODY,
        graph=graph, target_names=names, inputs={}, native_records={})
    def actual_setup():
        custody = run.O.OrdinaryStore(custody_path, A.S.semantic_id(), CUSTODY, create=True)
        native = None
        try:
            native = A.OrdinaryAdmission.open(run.base.installation, native_path, native_id, custody,
                                             create=True, limits=P.Limits(**NATIVE_LIMITS))
            initial = native.initialize(run.allocate())
            need(initial["status"] == "CHECKED" and initial["units_checked"] == 456, "ACTUAL_BASIS")
            budget = run.allocate()
            plan = native.preflight(initial["local_root"], prerequisites, budget=budget)
            need(plan.status == "READY" and len(plan.ordered_units) == 34 and not plan.reused_unit_ids,
                 "ACTUAL_PREREQUISITES_READY")
            accepted = native.admit(initial["local_root"], plan, budget)
            need(accepted["status"] == "CHECKED" and accepted["units_checked"] == 34 and
                 set(accepted["retained_unit_ids"]) == set(graph["ordered_units"])-{G.FIRST, G.SECOND},
                 "ACTUAL_PREREQUISITES_CHECKED")
            shared.update(basis_root=initial["local_root"], prerequisite_root=accepted["local_root"])
            for root_id in (initial["local_root"], accepted["local_root"]):
                raw, _ = native.catalog._root_row(root_id)
                shared["native_records"][root_id] = pin(raw)
            return dict(initial=initial, accepted=accepted)
        finally:
            if native is not None:
                native.close()
            custody.close()
    run.interval("COMMON_NATIVE_SETUP", actual_setup)
    run.interval("COMMON_PARENT_AUDIT", lambda: run.inspect_native(shared, custody_path, expected_roots=2))
    def write_handoff():
        inputs = {A.PE.read_evidence(raw).unit_id: raw for raw in prerequisites}
        inputs.update(targets)
        directory = run.output / "inputs"
        directory.mkdir()
        for uid in graph["ordered_units"]:
            run.check()
            need(pin(inputs[uid]) == graph["unit_pins"][uid], "PREPARED_INPUT_BINDING")
            P.PortableCatalog._write_fresh(directory / (uid+".json"), inputs[uid])
            shared["inputs"][uid] = pin(inputs[uid])
        return run.save("SHARED.json", shared)
    run.interval("FIXTURE_HANDOFF_WRITE", write_handoff)
    return dict(mathematical_worker_events=2, selected_parent=shared["prerequisite_root"],
                shared_descriptor=pin(read(run.output / "SHARED.json", 2*MIB, run.check)))


def load_cut_record(run, lane):
    run.loaded_cut = run.cut(lane)
    return dict(support_id=run.loaded_cut.support.support_id,
                support_manifest_sha256=run.loaded_cut.support.manifest_sha)


def load_shared_record(run):
    run.shared_state, run.shared_inputs = run.shared()
    return dict(units=len(run.shared_inputs), bytes=sum(map(len, run.shared_inputs.values())),
                selected_parent=run.shared_state["prerequisite_root"])


def cut_lane(run):
    lane, G = run.args.stage, run.graph_module
    run.interval("CUT_SUPPORT_LOAD", lambda: load_cut_record(run, lane))
    cut = run.loaded_cut
    T, K, M, H = cut.controller, cut.controller.K, cut.controller.M, cut.controller.H
    run.interval("SHARED_INPUT_LOAD", lambda: load_shared_record(run))
    shared, inputs = run.shared_state, run.shared_inputs
    custody_path, target = run.output / "custody", run.output / "cut"
    store_id, epoch = secrets.token_hex(32), secrets.token_hex(32)
    limits = K.Limits(max_db_pages=4096, max_roots=8, max_summaries=128,
        max_summary_bytes=2*MIB, max_total_summary_bytes=16*MIB, max_root_bytes=16384,
        max_total_root_bytes=MIB, max_nodes=8192, max_total_node_bytes=16*MIB)
    run.save("CUT-IDENTITIES.json", dict(store_id=store_id, epoch=epoch,
        limits={key: vars(value) if key == "map_limits" else value for key, value in vars(limits).items()}))
    run.interval("CUSTODY_ISOLATION", lambda: run.populate(custody_path, inputs))
    run.interval("SHARED_PARENT_PRE_AUDIT", lambda: run.inspect_native(shared, custody_path, expected_roots=2))
    def derive():
        budget = run.allocate()
        allowance = M.Allowance(200000, 20000, 64*MIB, 32*MIB)
        custody = run.O.OrdinaryStore(custody_path, run.A.S.semantic_id(), CUSTODY)
        native = None
        try:
            native = run.native(shared, custody)
            return T.bootstrap(cut.support, native.catalog, shared["prerequisite_root"], custody,
                target, run.output / "bootstrap-call", store_id=store_id, epoch=epoch,
                budget=budget, allowance=allowance, limits=limits,
                migration=T.MigrationLimits(max_units=64, max_names=4096, max_acquired_bytes=2*MIB, max_nodes=100000))
        finally:
            if native is not None:
                native.close()
            custody.close()
    grounded = run.interval("CUT_DERIVATION", derive)
    parent, endpoints = grounded["local_root"], []
    for i, uid in enumerate((G.FIRST, G.SECOND)):
        call = run.output / ("cut-call-"+str(i+1))
        def contribute():
            budget = run.allocate()
            allowance = M.Allowance(200000, 20000, 64*MIB, 32*MIB)
            custody = run.O.OrdinaryStore(custody_path, run.A.S.semantic_id(), CUSTODY)
            try:
                return T.extend(cut.support, target, parent, inputs[uid], custody, call,
                    store_id=store_id, epoch=epoch, budget=budget, allowance=allowance, limits=limits)
            finally:
                custody.close()
        result = run.interval("CUT_"+str(i+1), contribute)
        need(result["kind"] == "theorem-cut" and result["origin"] == "grounded-cut", "ACTUAL_CUT_RESULT")
        endpoints.append(dict(parent=parent, root=result["local_root"], uid=uid, call=str(call)))
        parent = result["local_root"]
    def audit():
        _, binding, _ = T._marker(target, store_id, epoch, cut.support, limits)
        checked = []
        with H.SourceAnchor.open(binding, check=run.check) as anchor:
            catalog = K.CutCatalog.open(target, store_id=store_id, support_id=cut.support.support_id,
                epoch=epoch, source_binding_raw=binding, check=anchor.check, limits=limits)
            try:
                catalog._begin(M.Allowance(10000, 0, 16*MIB, 0))
                for i, endpoint in enumerate(endpoints):
                    packet = run.E.strict_json(read(Path(endpoint["call"]) / "request.json", 64*MIB, run.check),
                                               run.E.Limits(max_bytes=64*MIB))
                    report = run.A._writer_json(read(Path(endpoint["call"]) / "report.json", 16*MIB, run.check), 16*MIB)
                    expected = shared["graph"]["feasibility_only_not_grounding"][i]
                    need([pin(run.E.canonical_json(x))["sha256"] for x in packet["concrete_units"]] == expected["concrete_sha256"] and
                         [pin(run.E.canonical_json(x))["sha256"] for x in packet["signature_rows"]] == expected["signature_sha256"] and
                         pin(run.E.canonical_json(packet["new_unit"]))["sha256"] == expected["new_unit_sha256"],
                         "MATCHED_CUT_PACKET_SEMANTICS")
                    record = catalog.root(endpoint["root"])
                    frontier = run.E.strict_json(catalog.read_summary(record["frontier_summary"]))
                    need(record["parent"] == endpoint["parent"] and record["unit_id"] == endpoint["uid"] and
                         frontier["names"] == expected["frontier"], "ACTUAL_COMMITTED_FRONTIER")
                    if i == 0:
                        need(record["result_summary"] == shared["graph"]["first_summary_sha256"], "FIRST_SUMMARY")
                    else:
                        need(any(row[0] == shared["target_names"][0] and row[2] == G.FIRST_EXPORT
                                 for row in packet["signature_rows"]) and
                             all(unit[1][0] != 1 for unit in packet["concrete_units"]), "RECURSIVE_SIGNATURE_NOT_ANCESTRAL_PROOF")
                    need(report["counts"]["kernel_calls"] == ((481, 490) if lane == "OLD" else (25, 34))[i],
                         "EXPECTED_FIXED_BASIS_KERNEL_DELTA")
                    checked.append(dict(root=endpoint["root"], counts=report["counts"],
                                        packet_semantics=expected))
            finally:
                catalog.close()
        return dict(endpoints=checked, custody=run.audit_custody(custody_path, shared),
                    source=run.inspect_native(shared, custody_path, expected_roots=2))
    audit_result = run.interval("POST_RESULT_AUDIT", audit)
    return dict(mathematical_worker_events=2, selected_parent=shared["prerequisite_root"],
                final_root=parent, audit=audit_result)


def native_lane(run):
    G = run.graph_module
    run.interval("SHARED_INPUT_LOAD", lambda: load_shared_record(run))
    shared, inputs = run.shared_state, run.shared_inputs
    sequential, batched = run.output / "sequential-custody", run.output / "batch-custody"
    run.interval("SEQUENTIAL_CUSTODY_ISOLATION", lambda: run.populate(sequential, inputs))
    run.interval("BATCH_CUSTODY_ISOLATION", lambda: run.populate(batched, inputs))
    run.interval("SHARED_PARENT_PRE_AUDIT", lambda: run.inspect_native(shared, sequential, expected_roots=2))
    def admit(parent, identities, custody_path):
        budget = run.allocate()
        custody = run.O.OrdinaryStore(custody_path, run.A.S.semantic_id(), CUSTODY)
        native = None
        try:
            native = run.native(shared, custody)
            plan = native.preflight(parent, tuple(inputs[uid] for uid in identities), budget=budget)
            need(plan.status == "READY" and len(plan.ordered_units) == len(identities) and not plan.reused_unit_ids,
                 "NATIVE_READY_NO_REUSED_TARGETS")
            accepted = native.admit(parent, plan, budget)
            need(accepted["status"] == "CHECKED" and accepted["units_checked"] == len(identities) and
                 set(accepted["retained_unit_ids"]) == set(identities), "ACTUAL_NATIVE_CONTINUATION")
            return accepted
        finally:
            if native is not None:
                native.close()
            custody.close()
    first = run.interval("NATIVE_1", lambda: admit(shared["prerequisite_root"], (G.FIRST,), sequential))
    second = run.interval("NATIVE_2", lambda: admit(first["local_root"], (G.SECOND,), sequential))
    batch = run.interval("NATIVE_BATCH", lambda: admit(shared["prerequisite_root"], (G.FIRST, G.SECOND), batched))
    need(len({shared["prerequisite_root"], first["local_root"], second["local_root"], batch["local_root"]}) == 4,
         "DISTINCT_NATIVE_BRANCH_ROOTS")
    audit = run.interval("POST_RESULT_AUDIT", lambda: dict(
        native=run.inspect_native(shared, sequential, expected_roots=5,
            endpoints=((first["local_root"], 1), (second["local_root"], 2), (batch["local_root"], 2))),
        sequential_custody=run.audit_custody(sequential, shared), batch_custody=run.audit_custody(batched, shared)))
    return dict(mathematical_worker_events=3, selected_parent=shared["prerequisite_root"],
                sequential_root=second["local_root"], batch_root=batch["local_root"], audit=audit)


def event_total(report, labels):
    selected = [event for event in report["events"] if event["phase"] in labels]
    need(len(selected) == len(labels) and {event["phase"] for event in selected} == set(labels) and
         all(event["outcome"] == "RETURNED" for event in selected),
         "MEASURED_INTERVAL_CENSUS")
    need(all(type(event[key]) in (int, float) and math.isfinite(event[key]) and event[key] >= 0
             for event in selected for key in ("wall_seconds", "controller_cpu_seconds",
                 "known_worker_cpu_seconds", "interval_cpu_seconds")), "FINITE_MEASURED_COSTS")
    return {key: sum(event[key] for event in selected) for key in
            ("wall_seconds", "controller_cpu_seconds", "known_worker_cpu_seconds", "interval_cpu_seconds")}


def finite_cost(value, label):
    need(type(value) in (int, float) and math.isfinite(value) and value >= 0, label)
    return value


def add_cost(*costs):
    return {key: sum(cost[key] for cost in costs) for key in ("cpu_seconds", "wall_seconds")}


def phase_cost(report, labels):
    total = event_total(report, labels)
    return dict(cpu_seconds=total["interval_cpu_seconds"], wall_seconds=total["wall_seconds"])


def stage_accounting(stage, report, observation):
    """Partition observed work, never sum nested workers onto inclusive Job CPU."""
    need(len(report["events"]) == len(PHASES[stage]) and
         {event["phase"] for event in report["events"]} == PHASES[stage], "EXACT_PHASE_PARTITION")
    total = event_total(report, PHASES[stage])
    for event in report["events"]:
        need(abs(event["interval_cpu_seconds"] - event["controller_cpu_seconds"] -
                 event["known_worker_cpu_seconds"]) <= 1e-9, "INTERVAL_CPU_DECOMPOSITION")
    load = report["source_and_base_load"]
    base_cost = dict(cpu_seconds=finite_cost(load["controller_cpu_seconds"], "BASE_LOAD_CPU"),
                     wall_seconds=finite_cost(load["wall_seconds"], "BASE_LOAD_WALL"))
    job_cpu = finite_cost(observation["final_job"]["cpu_seconds"], "STAGE_JOB_CPU")
    wall = finite_cost(observation["wall_seconds_through_cleanup"], "STAGE_WALL")
    supervision_cpu = finite_cost(observation["wrapper_supervision_cpu_seconds"], "SUPERVISION_CPU")
    reported_cpu = finite_cost(report["controller_cpu_seconds"], "REPORTED_CONTROLLER_CPU")
    reported_worker = finite_cost(report["known_worker_cpu_seconds"], "REPORTED_WORKER_CPU")
    reported_wall = finite_cost(report["wall_seconds"], "REPORTED_WALL")
    need(reported_cpu + 0.1 >= base_cost["cpu_seconds"] + total["controller_cpu_seconds"] and
         abs(reported_worker - total["known_worker_cpu_seconds"]) <= 0.1 and
         reported_wall + 1e-6 >= base_cost["wall_seconds"] + total["wall_seconds"] and
         wall + 1e-6 >= reported_wall, "PHASE_PARTITION_RECONCILIATION")
    # Includes interpreter startup before BOOT, uninstrumented controller/report
    # work, helper overhead outside known worker accounts, exit and Job closure.
    cpu_residual = job_cpu - base_cost["cpu_seconds"] - total["interval_cpu_seconds"]
    wall_residual = wall - base_cost["wall_seconds"] - total["wall_seconds"]
    need(cpu_residual >= -0.1 and wall_residual >= -1e-6, "NEGATIVE_LIFECYCLE_RESIDUAL")
    return dict(source_and_base_load=base_cost,
        measured_phases={label: phase_cost(report, {label}) for label in sorted(PHASES[stage])},
        inclusive_job_cpu_seconds=job_cpu, whole_stage_wall_seconds=wall,
        supervisor_parent_cpu_seconds=supervision_cpu,
        peak_job_private_commit_bytes=observation["final_job"]["peak_job_private_commit_bytes"],
        lifecycle_residual_signed=dict(cpu_seconds=cpu_residual, wall_seconds=wall_residual),
        conservative_nonnegative_residual=dict(cpu_seconds=max(0.0, cpu_residual),
                                               wall_seconds=max(0.0, wall_residual)),
        reconciliation_rounding_charge=dict(cpu_seconds=max(0.0, -cpu_residual),
                                           wall_seconds=max(0.0, -wall_residual)),
        accounting="BASE_LOAD+ALL_PHASES+SIGNED_RESIDUAL=LIVE_STAGE_JOB_CPU_AND_WALL;SUPERVISOR_CPU_IS_PARENT_ONLY")


def standalone_accounts(reports, accounting):
    """Observed phase attributions, not measured or predicted independent cold runs."""
    common = dict(source_and_base_load=accounting["SETUP"]["source_and_base_load"],
                  native_setup_and_prerequisite_retention=phase_cost(reports["SETUP"], {"COMMON_NATIVE_SETUP"}))
    routes = {"OLD": ("OLD", {"CUT_1", "CUT_2"}),
              "RESTORED": ("RESTORED", {"CUT_1", "CUT_2"}),
              "NATIVE_SEQUENTIAL": ("NATIVE", {"NATIVE_1", "NATIVE_2"}),
              "NATIVE_BATCH": ("NATIVE", {"NATIVE_BATCH"})}
    accounts = {}
    for name, (stage, continuation_labels) in routes.items():
        report, observed = reports[stage], accounting[stage]
        components = dict(common,
            route_source_and_base_load=observed["source_and_base_load"],
            route_input_validation=phase_cost(report, {"SHARED_INPUT_LOAD"}),
            continuation_including_commit_retention_and_close=phase_cost(report, continuation_labels))
        selected = {"SHARED_INPUT_LOAD", *continuation_labels}
        if stage != "NATIVE":
            components.update(cut_support_load=phase_cost(report, {"CUT_SUPPORT_LOAD"}),
                              actual_cut_derivation=phase_cost(report, {"CUT_DERIVATION"}))
            selected.update({"CUT_SUPPORT_LOAD", "CUT_DERIVATION"})
        measured = add_cost(*components.values())
        residual = add_cost(accounting["SETUP"]["conservative_nonnegative_residual"],
                            observed["conservative_nonnegative_residual"])
        # Supervisor CPU is a subset of coordinator CPU, not of either stage Job.
        # The NATIVE supervisor covers both branches. Do not attribute its unknown
        # branch share as an exact native-only charge or silently call it free.
        supervision = dict(cpu_seconds=accounting["SETUP"]["supervisor_parent_cpu_seconds"] +
                            observed["supervisor_parent_cpu_seconds"], wall_seconds=0.0)
        accounts[name] = dict(measured_required_components=components,
            measured_required_total=measured,
            available_observed_lifecycle_residual=residual,
            available_observed_parent_supervision=supervision,
            all_residual_charged_total=add_cost(measured, residual, supervision),
            attribution_range=dict(minimum=measured, maximum=add_cost(measured, residual, supervision)),
            range_meaning="ALLOCATION_OF_OBSERVED_SHARED_RESIDUAL_NOT_A_COLD_RUNTIME_BOUND;NO_POINT_WINNER_FROM_OVERLAP",
            excluded_explicit_phase_costs={label: phase_cost(report, {label})
                for label in sorted(PHASES[stage] - selected)},
            prerequisite_custody="ONE_REAL_RETENTION_IN_COMMON_SETUP;LANE_POPULATION_IS_ADDITIONAL_BENCHMARK_ISOLATION",
            lifecycle="COMMON_SETUP_PROCESS_THEN_FRESH_CONTINUATION_PROCESS;NOT_OPTIMAL_SINGLE_PROCESS_COLD_USE",
            residual_policy="REPORT_ALL;NO_SILENT_DISCARD;NATIVE_BRANCH_ALLOCATION_UNOBSERVED",
            future_retention="NO_HORIZON_PRICE_OR_FUTURE_REPAIR_COST_MEASURED;NO_LIFETIME_BENEFIT_CLAIM")
    return dict(alternatives=accounts,
        common_benchmark_only_phases={label: phase_cost(reports["SETUP"], {label})
            for label in sorted(PHASES["SETUP"] - {"COMMON_NATIVE_SETUP"})},
        summation_rule="MUTUALLY_EXCLUSIVE_ATTRIBUTIONS;NEVER_SUM_ALTERNATIVES_TO_FORM_THE_EXPERIMENT_BILL",
        retention=dict(prerequisite_units=34, prerequisite_claim_bytes=244463,
            final_units=36, final_claim_bytes=274177, new_target_claim_bytes=29714,
            byte_scope="EXACT_INERT_CLAIM_PAYLOAD_ONLY;NOT_ALL_DISK_IO_OR_DATABASE_ALLOCATION",
            required_writes="COMMON_NATIVE_SETUP,CUT_DERIVATION,AND_CONTRIBUTION_INTERVALS_INCLUDE_ACTUAL_PERSISTENCE_AND_HANDLE_CLOSURE",
            extra_isolation="FOUR_ADDITIONAL_PREREQUISITE_POPULATIONS_REMAIN_CHARGED_IN_ACTUAL_JOB_BILL"))


def coordinator(run):
    reports, observations, handoff = {}, {}, None
    supervisor, Job = run.base.installation._supervisor, run.base.installation._job_module.Job
    for stage in ORDER:
        run.phase = "ISOLATED_"+stage
        run.check()
        wall = math.floor(run.deadline-time.monotonic())-24
        cpu = math.floor(run.args.cpu_seconds-run.used_cpu())-1
        need(wall >= 60 and cpu >= 2, "NO_REMAINING_STAGE_ALLOCATION")
        stage_deadline = time.monotonic()+wall-5
        output = run.output / stage
        argv = [str(PYTHON / "python.exe"), "-I", "-S", "-B", str(run.source / "compare_workflow.py"),
            "--source-root", str(run.source), "--output", str(output), "--stage", stage,
            "--wall-seconds", str(wall), "--cpu-seconds", str(cpu), "--memory-mib", "1280",
            "--deadline", repr(stage_deadline)]
        if stage != "SETUP":
            argv += ["--shared", str(run.output / "SETUP/SHARED.json"), "--shared-sha256", handoff]
        limits = supervisor.limits_checked(dict(wall_seconds=wall, cpu_seconds=cpu, memory_mib=1280,
                                                active_processes=4, stdout_bytes=MIB, stderr_bytes=MIB))
        observation = supervisor.supervise(argv, ROOT, run.output / (stage+"-supervision"), limits, Job)
        supervisor.save_new(run.output / (stage+"-observation.json"), observation)
        observations[stage] = observation
        final = observation.get("final_job")
        known_cpu = final.get("cpu_seconds") if type(final) is dict else None
        need(type(known_cpu) in (float, int) and math.isfinite(known_cpu) and known_cpu >= 0,
             "UNKNOWN_CHILD_CPU_ABORT")
        run.child_cpu += known_cpu
        need(run.A._clean_worker(observation) and
             ordinary(run.output / (stage+"-supervision/stderr.txt")).stat().st_size == 0,
             "UNCLEAN_STAGE_ABORT")
        raw = read(output / "STAGE.json", 2*MIB, run.check)
        report = operational_json(raw)
        need(report["schema"] == "DMKN_FIXED_BASIS_COMPARE_STAGE_V1" and report["stage"] == stage and
             report["status"] == "RETURNED_REQUIRES_ENCLOSING_CLOSURE" and
             report["result"]["mathematical_worker_events"] == (3 if stage == "NATIVE" else 2),
             "STAGE_REPORT_BINDING")
        need(final["total_processes"] >= 1+2*report["result"]["mathematical_worker_events"] and
             known_cpu + 0.1 >= report["known_worker_cpu_seconds"] + report["controller_cpu_seconds"],
             "NESTED_JOB_ACCOUNTING")
        reports[stage] = report
        if stage == "SETUP":
            handoff = pin(read(output / "SHARED.json", 2*MIB, run.check))["sha256"]
            need(handoff == report["result"]["shared_descriptor"]["sha256"], "LIVE_SETUP_HANDOFF_PIN")
        else:
            need(report["result"]["selected_parent"] == reports["SETUP"]["result"]["selected_parent"],
                 "ALL_LANES_EXACT_PARENT")
    warm = {"OLD": event_total(reports["OLD"], {"CUT_1", "CUT_2"}),
            "RESTORED": event_total(reports["RESTORED"], {"CUT_1", "CUT_2"}),
            "NATIVE_SEQUENTIAL": event_total(reports["NATIVE"], {"NATIVE_1", "NATIVE_2"}),
            "NATIVE_BATCH": event_total(reports["NATIVE"], {"NATIVE_BATCH"})}
    old, restored = warm["OLD"]["interval_cpu_seconds"], warm["RESTORED"]["interval_cpu_seconds"]
    need(old > 0, "NONZERO_COMPARATOR_CPU")
    accounting = {stage: stage_accounting(stage, reports[stage], observations[stage]) for stage in ORDER}
    supervisor_cpu = sum(value["supervisor_parent_cpu_seconds"] for value in accounting.values())
    coordinator_cpu = time.process_time()-BOOT_CPU
    need(coordinator_cpu + 0.1 >= supervisor_cpu, "COORDINATOR_SUPERVISION_SUBSET")
    return dict(schema="DMKN_FIXED_BASIS_COMPARE_V1", order=list(ORDER), mathematical_worker_events=9,
        shared_setup=event_total(reports["SETUP"], {"COMMON_NATIVE_SETUP"}), warm_continuation=warm,
        migrations={lane: event_total(reports[lane], {"CUT_DERIVATION"}) for lane in ("OLD", "RESTORED")},
        old_to_restored_cpu_fraction=restored/old, material_cpu_margin_met=restored <= 0.8*old,
        threshold_meaning="PROSPECTIVE_ENGINEERING_MARGIN_NOT_STATISTICAL_OR_PUBLIC_ADOPTION",
        stage_reports=reports, stage_observations=observations,
        stage_accounting=accounting, standalone_attributable_use=standalone_accounts(reports, accounting),
        experiment_known_inclusive_stage_cpu_seconds=run.child_cpu,
        coordinator_cpu_seconds=coordinator_cpu, wall_seconds=time.monotonic()-BOOT,
        coordinator_supervision_cpu_subset=supervisor_cpu,
        experiment_known_cpu_before_final_report=run.child_cpu+coordinator_cpu,
        complete_experiment_cpu="USE_OUTER_JOB;DO_NOT_ADD_NESTED_WORKER_CPU_AGAIN",
        experiment_reconciliation="INNER_STAGE_JOBS+COORDINATOR_CPU_IS_A_PRE_REPORT_SUBTOTAL;OUTER_JOB_ALSO_COVERS_COORDINATOR_STARTUP_FINAL_OUTPUT_AND_EXIT;OUTER_WRAPPER_SEPARATE",
        standalone_accounting="EXPLICIT_PHASE_ATTRIBUTION_WITH_ALL_OBSERVED_RESIDUAL;NO_INDEPENDENT_COLD_OR_LIFETIME_MEASUREMENT",
        adoption="REQUIRES_INDEPENDENT_ACTUAL_AUDIT_AND_ROOT_COST_DECISION", speedup_or_growth_claim=False)


def main():
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and
         Path(sys.executable).resolve() == PYTHON / "python.exe" and
         sys.getprofile() is None and sys.gettrace() is None,
         "PINNED_UNPROFILED_PROCESS")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for flag in ("source-root", "output"):
        parser.add_argument("--"+flag, required=True)
    for flag in ("wall-seconds", "cpu-seconds", "memory-mib"):
        parser.add_argument("--"+flag, type=int, required=True)
    parser.add_argument("--stage", choices=("COORDINATOR", *ORDER), default="COORDINATOR")
    parser.add_argument("--shared")
    parser.add_argument("--shared-sha256")
    parser.add_argument("--deadline", type=float)
    args = parser.parse_args()
    need((args.stage == "COORDINATOR" and args.deadline is None and args.shared is None and
          args.shared_sha256 is None and args.wall_seconds == 360 and args.cpu_seconds == 240) or
         (args.stage in ORDER and args.deadline is not None), "COORDINATOR_OR_CHILD_ALLOCATION")
    run = Run(args)
    try:
        if args.stage == "COORDINATOR":
            result = coordinator(run)
            run.save("COMPARISON.json", result)
        else:
            result = setup(run) if args.stage == "SETUP" else native_lane(run) if args.stage == "NATIVE" else cut_lane(run)
            run.check()
            run.save("STAGE.json", dict(schema="DMKN_FIXED_BASIS_COMPARE_STAGE_V1", stage=args.stage,
                status="RETURNED_REQUIRES_ENCLOSING_CLOSURE", result=result, events=run.events,
                source_and_base_load=run.load_cost, wall_seconds=time.monotonic()-BOOT,
                controller_cpu_seconds=time.process_time()-BOOT_CPU,
                known_worker_cpu_seconds=sum(b.worker_cpu for b in run.budgets),
                speedup_or_growth_claim=False))
        print(json.dumps(dict(status="RETURNED_REQUIRES_ENCLOSING_CLOSURE", stage=args.stage)), flush=True)
    except BaseException as error:
        try:
            run.save("FAILURE.json", dict(stage=args.stage, phase=run.phase,
                error=(type(error).__name__+":"+str(error))[:2048], events=run.events,
                known_child_cpu_seconds=run.child_cpu, known_worker_cpu_seconds=sum(b.worker_cpu for b in run.budgets),
                controller_cpu_seconds=time.process_time()-BOOT_CPU, wall_seconds=time.monotonic()-BOOT,
                possible_commit="CONSULT_DURABLE_STATE_NO_RETRY", retention="ALL_PARTIAL_STATE_AND_COST_RETAINED"))
        except BaseException:
            pass
        raise


if __name__ == "__main__":
    main()
