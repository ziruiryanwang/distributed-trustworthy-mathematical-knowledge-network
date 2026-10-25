"""One selected real two-law grounded-cut workflow, never an automatic campaign.

Run only inside root's finite whole-operation supervisor. All state is fresh;
the retained theory bundle is inert input, not an accepted native environment.
No certificate, source authoring, network, return adapter, retry or fallback.
"""
from __future__ import annotations

import argparse
import hashlib
import heapq
import importlib.util
import json
import math
import os
from pathlib import Path
import secrets
import stat
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PYTHON = Path(r"D:\Python314")
LEAN = ROOT / "software/runtime/lean-4.34.0-windows"
PROFILE = "9c41b9a3fe36f7283af130ac6ef290e82c2a78c432980b2bea75ccdcf197a6d4"
BUNDLE = "680cd98f8d1d31ef251b1e78b1cdae7a60bbe2b733e95193b0fe52cb9855c302"
FIRST = "403dd4d8878342f863c80ee40311a1829a3bf94c59a003d68ddd524ede5f35b9"
SECOND = "0be846200d7809eaa68cf06cf23ef362052d4d3f4a5db4892c7f369691393e83"
FIRST_EXPORT = "f2fa586cebc1ea3a305b51af3ab81ce5ac6eb89775e880bf45c9dd4109bd40c1"
MIB = 1024**2
CUSTODY = {"objects": 128, "exports": 512, "logical_bytes": 16*MIB, "db_pages": 4096}


def need(ok, code):
    if not ok:
        raise ValueError("CUT_RECURSIVE_" + code)


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
             (getattr(info, "st_file_attributes", 0) & 0x400), "REDIRECTED_PATH")
        need(stat.S_ISDIR(info.st_mode) if item != path or directory else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "PATH_KIND")
    need(not fresh, "FRESH_PATH_REQUIRED")
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
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def load(name, path, raw):
    need(name not in sys.modules, "PRELOADED_MODULE")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    return module


def encoded_name(last):
    return [[0, {"$bytes": list(part.encode("ascii"))}]
            for part in ("RepairTheory", "ClosureBridge", last)]


def graph(base, cut, bundle, check):
    """Read exact inert bytes; compute closure and unsupported-shape refusal first."""
    A, E, S, PE = base.A, base.A.E, base.A.S, base.A.PE
    B, Q = base.baseline_intake.B, cut.controller.Q
    manifest_raw = read(bundle / "manifest.json", 2*MIB, check)
    manifest = B.read_manifest(manifest_raw, BUNDLE, check_budget=check)
    need(manifest.unit_count == 106 and manifest.evidence_bytes == 822414, "BUNDLE_CENSUS")
    basis, _ = cut.controller._basis(cut.support, check)
    units, exports, pins = {}, {}, {}
    for batch in manifest.batches:
        for entry in batch:
            raw = read(bundle / entry.relative_path, entry.raw_bytes, check)
            need(pin(raw) == {"bytes": entry.raw_bytes, "sha256": entry.raw_sha256}, "INPUT_PIN")
            item = PE.read_evidence(raw)
            need(item.unit_id == entry.unit_id and item.document["semantic_id"] == manifest.semantic_id,
                 "INPUT_IDENTITY")
            units[item.unit_id], pins[item.unit_id] = item, pin(raw)
            for row in item.document["unit"][2]:
                key = E.name_key(row[0])
                need(key not in basis and key not in exports, "INPUT_NAME_COLLISION")
                exports[key] = (S.export_id(manifest.semantic_id, item.unit_id, row[0]), item.unit_id)
    dependencies = {}
    for uid, item in units.items():
        check()
        parents = set()
        for name, symbol in item.document["imports"]:
            key = E.name_key(name)
            if key in basis:
                need(basis[key] == symbol, "INPUT_BASIS_BINDING")
            else:
                need(key in exports and exports[key][0] == symbol, "INPUT_IMPORT_BINDING")
                parents.add(exports[key][1])
        need(uid not in parents, "INPUT_SELF_DEPENDENCY")
        dependencies[uid] = parents
    selected, pending = set(), [FIRST, SECOND]
    while pending:
        check()
        uid = pending.pop()
        if uid not in selected:
            need(uid in units, "TARGET_MISSING")
            selected.add(uid)
            pending.extend(dependencies[uid] - selected)
    need(len(selected) == 36 and FIRST in dependencies[SECOND] and
         SECOND not in dependencies[FIRST], "EXACT_RECURSIVE_GRAPH")
    old = selected - {FIRST, SECOND}
    need(all(not (dependencies[uid] & {FIRST, SECOND}) for uid in old), "EXCLUDED_TARGET_PREREQUISITE")
    remaining = {uid: len(dependencies[uid]) for uid in selected}
    users = {uid: [] for uid in selected}
    for uid in selected:
        for parent in dependencies[uid]:
            users[parent].append(uid)
    ready = [uid for uid, count in remaining.items() if not count]
    heapq.heapify(ready)
    ordered = []
    while ready:
        check()
        uid = heapq.heappop(ready)
        ordered.append(uid)
        for child in sorted(users[uid]):
            remaining[child] -= 1
            if remaining[child] == 0:
                heapq.heappush(ready, child)
    need(len(ordered) == len(selected), "INPUT_DEPENDENCY_CYCLE")
    target_names = [encoded_name("run_extensive"), encoded_name("same_constraints_same_run")]
    target_exports = []
    for uid, name in zip((FIRST, SECOND), target_names):
        item = units[uid]
        need(item.document["unit"][1][0] == 1 and len(item.document["unit"][2]) == 1 and
             item.document["unit"][2][0][0] == name, "EXACT_TARGET_NAME")
        target_exports.append(S.export_id(manifest.semantic_id, uid, name))
    need(target_exports[0] == FIRST_EXPORT, "FIRST_EXPORT")
    # Pure feasibility only: these ungrounded projected summaries never enter a catalog.
    projected = {uid: Q.project(units[uid].raw) for uid in selected}
    expected = []
    for uid, earlier in ((FIRST, old), (SECOND, old | {FIRST})):
        by_name = {key: (symbol, projected[value].summary_id)
                   for value in earlier for key, symbol in projected[value].bindings}
        summaries = {projected[value].summary_id: projected[value].raw for value in earlier}
        prepared = Q.prepare(units[uid].raw, semantic_id=manifest.semantic_id, basis=basis,
            lookup=lambda name: by_name.get(E.name_key(name)),
            read_summary=lambda digest: summaries[digest], check=check)
        expected.append({"concrete_sha256": [pin(raw)["sha256"] for raw in prepared.concrete_units],
            "signature_sha256": [pin(raw)["sha256"] for raw in prepared.signature_rows],
            "new_unit_sha256": pin(prepared.new_unit)["sha256"],
            "frontier": [[name.hex(), symbol, digest] for name, symbol, digest in prepared.frontier],
            "preparation": vars(prepared.stats)})
    first_key = E.name_key(target_names[0])
    first_summary = projected[FIRST]
    need([first_key.hex(), FIRST_EXPORT, first_summary.summary_id] in expected[1]["frontier"],
         "SECOND_EXPECTED_FIRST_SIGNATURE")
    report = {"manifest_sha256": BUNDLE, "bundle_units_read": manifest.unit_count,
        "bundle_bytes_read": manifest.evidence_bytes, "closure_units": len(selected),
        "closure_bytes": sum(pins[uid]["bytes"] for uid in selected),
        "prerequisite_units": len(old), "prerequisite_bytes": sum(pins[uid]["bytes"] for uid in old),
        "concrete_units": sum(projected[uid].kind == "concrete" for uid in selected),
        "theorem_units": sum(projected[uid].kind == "theorem" for uid in selected),
        "ordered_units": ordered, "dependencies": {uid: sorted(dependencies[uid]) for uid in ordered},
        "unit_pins": {uid: pins[uid] for uid in ordered}, "target_exports": target_exports,
        "first_summary_sha256": first_summary.summary_id,
        "feasibility_only_not_grounding": expected}
    need((report["closure_bytes"], report["prerequisite_bytes"], report["concrete_units"],
          report["theorem_units"]) == (274177, 244463, 20, 16), "EXACT_SELECTED_CENSUS")
    return report, tuple(units[uid].raw for uid in ordered if uid in old), \
        {FIRST: units[FIRST].raw, SECOND: units[SECOND].raw}, target_names


class PathAudit:
    """Read-only parent instrumentation, not isolation or a substitute for checking."""
    def __init__(self, base, native, bundle):
        A, O = base.A, base.O
        self.phase, self.allowed_unit = "", ""
        self.native, self.bundle = native, bundle
        self.allowed_native = {native / name for name in ("owner.lock", "ADOPTION.json", "catalog.sqlite")}
        self.calls, self.opens, self.violations = {}, {}, []
        self.forbidden = {A.OrdinaryAdmission.open.__func__.__code__,
            A.OrdinaryAdmission._execute.__code__, A.P.PortableCatalog.open.__func__.__code__,
            A.P.PortableCatalog._open.__func__.__code__, A.P.PortableCatalog.context.__code__,
            A.P.PortableCatalog._artifact.__code__, O.OrdinaryStore.get_locator.__code__}
        self.evidence = O.OrdinaryStore.get_evidence.__code__
        need(sys.getprofile() is None, "EXISTING_PROFILE_HOOK")
        sys.addaudithook(self.audit)

    def deny(self, reason):
        if len(self.violations) < 32:
            self.violations.append({"phase": self.phase, "reason": reason})
        raise AssertionError("CUT_RECURSIVE_FORBIDDEN_" + reason)

    def profile(self, frame, event, arg):
        if self.phase and event == "call":
            if frame.f_code in self.forbidden:
                self.deny(frame.f_code.co_name)
            if frame.f_code is self.evidence:
                uid = frame.f_locals["unit_id"]
                if uid != self.allowed_unit:
                    self.deny("OLD_PROOF_CUSTODY:" + str(uid))
                self.calls[self.phase] = self.calls.get(self.phase, 0) + 1

    def audit(self, event, arguments):
        if not self.phase or event not in ("open", "sqlite3.connect") or not arguments:
            return
        value = arguments[0]
        if not isinstance(value, (str, bytes, os.PathLike)):
            return
        text = os.fsdecode(value)
        # SourceAnchor's read-only SQLite URI is the one permitted native DB open.
        if event == "sqlite3.connect" and text == (self.native / "catalog.sqlite").as_uri() + "?mode=ro":
            key = self.phase + ":source-anchor-sqlite"
            self.opens[key] = self.opens.get(key, 0) + 1
            return
        path = Path(text).absolute()
        if path.is_relative_to(self.bundle):
            self.deny("RETAINED_BUNDLE_READ")
        if path.is_relative_to(self.native):
            if path not in self.allowed_native:
                self.deny("NATIVE_ANCESTRY_READ:" + str(path))
            key = self.phase + ":" + path.name
            self.opens[key] = self.opens.get(key, 0) + 1

    def begin(self, phase, allowed_unit=""):
        need(not self.phase, "AUDIT_ALREADY_ACTIVE")
        self.phase, self.allowed_unit = phase, allowed_unit
        sys.setprofile(self.profile)

    def end(self):
        sys.setprofile(None)
        self.phase, self.allowed_unit = "", ""


def run(args):
    started, cpu_started = time.monotonic(), time.process_time()
    need(120 <= args.wall_seconds <= 1800 and 30 <= args.cpu_seconds <= 1800 and
         768 <= args.memory_mib <= 4096, "FINITE_ALLOCATION")
    deadline = started + args.wall_seconds
    budgets, events, phase = [], [], "LOAD_SUPPORT"
    def used_cpu():
        return time.process_time() - cpu_started + sum(b.worker_cpu for b in budgets)
    def check():
        need(time.monotonic() < deadline and used_cpu() < args.cpu_seconds, "ORIGINAL_ALLOWANCE")
    source = ordinary(args.source_root, directory=True)
    base_path = ordinary(args.base_package, directory=True)
    addition = ordinary(args.addition, directory=True)
    bundle = ordinary(args.bundle, directory=True)
    output = ordinary(args.output, directory=True, fresh=True)
    need(source.is_relative_to(ROOT / "experiments") and output.is_relative_to(ROOT / "experiments") and
         Path(__file__).absolute() == source / "recursive_workflow.py", "SELECTED_PATHS")
    paths = (source, base_path, addition, bundle, output, PYTHON, LEAN)
    for i, left in enumerate(paths):
        for right in paths[i+1:]:
            need(not left.is_relative_to(right) and not right.is_relative_to(left), "PATH_OVERLAP")
    profile_raw = read(base_path / "PROFILE.json", 2*MIB, check)
    need(pin(profile_raw)["sha256"] == PROFILE, "PROFILE_PIN")
    descriptor = json.loads(profile_raw)
    owner_raw = read(base_path / "owner.py", 2*MIB, check)
    need(pin(owner_raw) == descriptor["files"]["owner.py"], "OWNER_PIN")
    owner = load("_dmkn_recursive_owner", base_path / "owner.py", owner_raw)
    loader = owner.bootstrap(base_path, PROFILE, check)
    base = loader.load(base_path, PROFILE, {"python_runtime": PYTHON, "lean_runtime": LEAN},
                       deadline, check_parent=check)
    A, E, P, O = base.A, base.A.E, base.A.P, base.O
    manifest_raw = read(addition / "CUT-SUPPORT.json", 2*MIB, check)
    need(pin(manifest_raw)["sha256"] == P.hexid(args.support_sha256), "CUT_SUPPORT_PIN")
    manifest = E.strict_json(manifest_raw, E.Limits(max_bytes=2*MIB))
    boot_raw = read(addition / "cut_bootstrap.py", 2*MIB, check)
    need(pin(boot_raw) == manifest["files"]["cut_bootstrap.py"], "CUT_BOOTSTRAP_PIN")
    boot = load("cut_bootstrap", addition / "cut_bootstrap.py", boot_raw)
    cut = boot.load(addition, args.support_sha256, base, check=check)
    T, K, M, H = cut.controller, cut.controller.K, cut.controller.M, cut.controller.H
    output.mkdir()
    native_path, custody_path, cut_path = (output / part for part in ("native", "custody", "cut"))
    native_id, store_id, epoch = (secrets.token_hex(32) for _ in range(3))
    native_limits = P.Limits(max_roots=4, max_operations=4, max_names=4096,
        max_manifest_bytes=2*MIB, max_artifact_bytes=64*MIB,
        max_total_artifact_bytes=256*MIB, max_db_pages=4096,
        max_batch_bytes=2*MIB, max_batch_units=64)
    cut_limits = K.Limits(max_db_pages=4096, max_roots=8, max_summaries=128,
        max_summary_bytes=2*MIB, max_total_summary_bytes=16*MIB,
        max_root_bytes=16384, max_total_root_bytes=MIB,
        max_nodes=8192, max_total_node_bytes=16*MIB)
    native = custody = None
    audit = None
    def save(name, doc):
        raw = E.canonical_json(doc)
        need(len(raw) <= 2*MIB, "REPORT_BOUND")
        P.PortableCatalog._write_fresh(output / name, raw)
        need(P.read_bounded(output / name, 2*MIB) == raw, "REPORT_CHANGED")
        return pin(raw)
    def allocate():
        check()
        wall = min(3600, math.floor(deadline - time.monotonic()) - 5)
        cpu = math.floor(args.cpu_seconds - used_cpu()) - 1
        need(wall >= 30 and cpu >= 2, "INSUFFICIENT_REMAINING_ALLOWANCE")
        budget = A.OperationBudget(wall, cpu, args.memory_mib, active_processes=4,
                                    output_bytes=64*MIB, log_bytes=MIB)
        need(budget.deadline < deadline, "CHILD_DEADLINE")
        budgets.append(budget)
        return budget
    def invoke(label, function):
        nonlocal phase
        phase = label
        budget = allocate()
        before, cpu = time.monotonic(), time.process_time()
        allowance = M.Allowance(200000, 20000, 64*MIB, 32*MIB)
        try:
            result = function(budget, allowance)
        except BaseException as error:
            events.append({"phase": label, "outcome": "FAILED_OR_UNCERTAIN",
                "error": (type(error).__name__ + ":" + str(error))[:2048],
                "wall_seconds": time.monotonic()-before, "controller_cpu_seconds": time.process_time()-cpu,
                "known_worker_cpu_seconds": budget.worker_cpu, "logical_io": vars(allowance)})
            raise
        events.append({"phase": label, "outcome": "RETURNED", "result": result,
            "wall_seconds": time.monotonic()-before, "controller_cpu_seconds": time.process_time()-cpu,
            "known_worker_cpu_seconds": budget.worker_cpu, "logical_io": vars(allowance)})
        save("EVENT-" + str(len(events)) + ".json", events[-1])
        check()
        return result
    def open_cut(callback):
        target, binding, _ = T._marker(cut_path, store_id, epoch, cut.support, cut_limits)
        with H.SourceAnchor.open(binding, check=check) as anchor:
            catalog = K.CutCatalog.open(target, store_id=store_id, support_id=cut.support.support_id,
                epoch=epoch, source_binding_raw=binding, check=anchor.check, limits=cut_limits)
            try:
                catalog._begin(M.Allowance(10000, 0, 16*MIB, 0))
                return callback(catalog)
            finally:
                catalog.close()
    try:
        phase = "EXACT_GRAPH_AND_INERT_FEASIBILITY"
        graph_doc, prerequisites, targets, target_names = graph(base, cut, bundle, check)
        save("INPUT-GRAPH.json", graph_doc)
        limits_pin = save("CUSTODY-LIMITS.json", CUSTODY)
        targets_pin = save("RETURN-TARGETS.json", graph_doc["target_exports"])
        save("STATE-IDENTITIES.json", {"native_store_id": native_id, "cut_store_id": store_id,
            "cut_epoch": epoch, "support_id": cut.support.support_id,
            "support_manifest_sha256": args.support_sha256, "base_profile_sha256": PROFILE,
            "native_limits": vars(native_limits), "cut_limits": {
                key: vars(value) if key == "map_limits" else value for key, value in vars(cut_limits).items()}})
        custody = O.OrdinaryStore(custody_path, A.S.semantic_id(), CUSTODY, create=True)
        native = A.OrdinaryAdmission.open(base.installation, native_path, native_id,
                                         custody, create=True, limits=native_limits)
        initial = invoke("NATIVE_BASIS", lambda budget, _: native.initialize(budget))
        need(initial["status"] == "CHECKED" and initial["units_checked"] == 456, "ACTUAL_BASIS")
        def admit(budget, _):
            plan = native.preflight(initial["local_root"], prerequisites, budget=budget)
            need(plan.status == "READY" and len(plan.ordered_units) == 34 and
                 not plan.reused_unit_ids, "ACTUAL_PREREQUISITES_READY")
            return native.admit(initial["local_root"], plan, budget)
        accepted = invoke("NATIVE_PREREQUISITES", admit)
        need(accepted["status"] == "CHECKED" and accepted["units_checked"] == 34 and
             set(accepted["retained_unit_ids"]) == set(graph_doc["ordered_units"]) - {FIRST, SECOND},
             "ACTUAL_PREREQUISITE_CENSUS")
        context = native.catalog.context(accepted["local_root"])
        need(all(E.name_key(name) not in context["bindings"] for name in target_names),
             "TARGET_ALREADY_IN_NATIVE")
        del context
        grounded = invoke("NATIVE_TO_CUT_DERIVATION", lambda budget, allowance: T.bootstrap(
            cut.support, native.catalog, accepted["local_root"], custody, cut_path,
            output / "bootstrap-call", store_id=store_id, epoch=epoch,
            budget=budget, allowance=allowance, limits=cut_limits,
            migration=T.MigrationLimits(max_units=64, max_names=4096,
                max_acquired_bytes=2*MIB, max_nodes=100000)))
        native.close()
        native = None
        custody.close()
        custody = None
        del prerequisites
        audit = PathAudit(base, native_path, bundle)
        audit.begin("INITIAL_REOPEN")
        try:
            def initial_cut(catalog):
                record = catalog.root(grounded["local_root"])
                need(record["kind"] == "native-bootstrap" and all(
                    catalog.lookup(grounded["local_root"], E.name_key(name)) is None
                    for name in target_names), "GROUNDED_TARGET_ABSENCE")
            open_cut(initial_cut)
        finally:
            audit.end()
        parent = grounded["local_root"]
        for index, uid in enumerate((FIRST, SECOND)):
            # No live native/cut/custody handle or scratch snapshot crosses this boundary.
            custody = O.OrdinaryStore(custody_path, A.S.semantic_id(), CUSTODY)
            call = output / ("cut-call-" + str(index+1))
            audit.begin("CUT_" + str(index+1), uid)
            try:
                checked = invoke("CUT_" + str(index+1), lambda budget, allowance: T.extend(
                    cut.support, cut_path, parent, targets[uid], custody, call,
                    store_id=store_id, epoch=epoch, budget=budget, allowance=allowance,
                    limits=cut_limits))
                need(checked["kind"] == "theorem-cut" and checked["origin"] == "grounded-cut",
                     "ACTUAL_CUT_RESULT")
                custody.close()
                custody = None
                # Diagnostic saved packet comparison does not confer authority.
                packet_raw = read(call / "request.json", 64*MIB, check)
                packet = E.strict_json(packet_raw, E.Limits(max_bytes=64*MIB))
                expected = graph_doc["feasibility_only_not_grounding"][index]
                need([pin(E.canonical_json(value))["sha256"] for value in packet["concrete_units"]]
                     == expected["concrete_sha256"] and
                     [pin(E.canonical_json(value))["sha256"] for value in packet["signature_rows"]]
                     == expected["signature_sha256"] and
                     pin(E.canonical_json(packet["new_unit"]))["sha256"] == expected["new_unit_sha256"],
                     "ACTUAL_PACKET_SEMANTICS")
                def inspect(catalog):
                    record = catalog.root(checked["local_root"])
                    frontier = E.strict_json(catalog.read_summary(record["frontier_summary"]))
                    need(record["parent"] == parent and record["unit_id"] == uid and
                         frontier["names"] == expected["frontier"], "ACTUAL_COMMITTED_FRONTIER")
                    if index == 1:
                        row = [E.name_key(target_names[0]).hex(), FIRST_EXPORT, graph_doc["first_summary_sha256"]]
                        need(row in frontier["names"] and any(signature[0] == target_names[0] and
                            signature[2] == FIRST_EXPORT for signature in packet["signature_rows"]),
                            "REAL_RECURSIVE_INTERFACE_USE")
                        need(all(unit[1][0] != 1 for unit in packet["concrete_units"]), "OLD_THEOREM_BODY_PACKET")
                    return record["result_summary"]
                digest = open_cut(inspect)
                if index == 0:
                    need(digest == graph_doc["first_summary_sha256"], "ACTUAL_FIRST_SUMMARY")
            finally:
                audit.end()
                if custody is not None:
                    custody.close()
                    custody = None
            parent = checked["local_root"]
            del targets[uid], packet, packet_raw
        # Reopen from the durable exact intent; no native worker or event replay.
        audit.begin("RESOLVE")
        try:
            resolved = invoke("RESOLVE_SECOND", lambda budget, allowance: T.resolve(
                cut.support, cut_path, output / "cut-call-2", store_id=store_id, epoch=epoch,
                budget=budget, allowance=allowance, limits=cut_limits))
            need(resolved["disposition"] == "COMMITTED" and resolved["local_root"] == parent and
                 resolved["reexecuted"] is False, "EXACT_DURABLE_RESOLUTION")
        finally:
            audit.end()
        phase = "SEPARATE_INERT_CUSTODY_AUDIT"
        custody = O.OrdinaryStore(custody_path, A.S.semantic_id(), CUSTODY)
        verified_bytes = 0
        for uid in graph_doc["ordered_units"]:
            expected_pin = graph_doc["unit_pins"][uid]
            held = custody.get_evidence(A.S.semantic_id(), uid, expected_pin["bytes"], check_budget=check)
            need(pin(held) == expected_pin and A.PE.read_evidence(held).unit_id == uid, "FINAL_CUSTODY_IDENTITY")
            verified_bytes += len(held)
        need(custody.status()["counts"]["objects"] == 36, "FINAL_CUSTODY_CENSUS")
        custody.close()
        custody = None
        need(not audit.violations and audit.calls == {"CUT_1": 1, "CUT_2": 1}, "PATH_AUDIT")
        cut.support.verify(check)
        check()
        result = {"schema": "DMKN_GROUNDED_CUT_RECURSIVE_WORKFLOW_V1",
            "status": "TWO_REAL_RECURSIVE_CUTS_REQUIRES_OUTER_CLOSURE_AUDIT",
            "events": events, "final_local_root": parent, "source_native_root": accepted["local_root"],
            "cut_store_id": store_id, "cut_epoch": epoch, "support_id": cut.support.support_id,
            "native_check_events": 2, "cut_check_events": 2, "proof_certificates": 0,
            "path_audit": {"allowed_new_custody_reads": audit.calls, "native_identity_opens": audit.opens,
                "violations": audit.violations, "scope": "PYTHON_PARENT_PATHS_AND_APPROVED_FIXED_WORKER_SOURCE_NOT_OS_TRACE"},
            "final_custody_audit": {"units": 36, "bytes": verified_bytes,
                "scope": "SEPARATE_CHARGED_FULL_CUSTODY_READ_NOT_CUT_CHECK_INPUT"},
            "return_handoff": {"custody": str(custody_path), "custody_limits": limits_pin,
                "selected_exports": targets_pin, "adapter_invoked": False,
                "meaning": "INERT_CUSTODY_ONLY_NOT_TRANSFERABLE_WARRANT"},
            "wall_seconds": time.monotonic()-started, "controller_cpu_seconds": time.process_time()-cpu_started,
            "known_worker_cpu_seconds": sum(b.worker_cpu for b in budgets),
            "inclusive_cpu_and_closure": "USE_ENCLOSING_JOB_WITHOUT_DOUBLE_COUNTING",
            "speedup_or_growth_claim": False}
        save("WORKFLOW.json", result)
        print(json.dumps({"status": result["status"], "final_local_root": parent}, sort_keys=True), flush=True)
    except BaseException as error:
        if audit is not None:
            audit.end()
        try:
            save("WORKFLOW-FAILURE.json", {"phase": phase, "error": (type(error).__name__+":"+str(error))[:2048],
                "events": events, "wall_seconds": time.monotonic()-started,
                "controller_cpu_seconds": time.process_time()-cpu_started,
                "known_worker_cpu_seconds": sum(b.worker_cpu for b in budgets),
                "possible_commit": "CONSULT_EXACT_DURABLE_INTENTS_NO_AUTOMATIC_RETRY",
                "retention": "ALL_PARTIAL_STATE_AND_EVIDENCE_RETAINED"})
        except BaseException:
            pass
        raise
    finally:
        if custody is not None:
            custody.close()
        if native is not None:
            native.close()


def main():
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and
         Path(sys.executable).resolve() == PYTHON / "python.exe", "PINNED_PROCESS")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("source-root", "base-package", "addition", "support-sha256", "bundle", "output"):
        parser.add_argument("--" + name, required=True)
    for name in ("wall-seconds", "cpu-seconds", "memory-mib"):
        parser.add_argument("--" + name, required=True, type=int)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
