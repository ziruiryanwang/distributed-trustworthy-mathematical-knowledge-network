"""Local sidecar storage contracts under explicit INERT owner/event fixtures.

No owner lock is acquired, no admission/database/native/network operation runs,
and dummy artifact bytes are not Lean modules. Constructing exact-class test
owners bypasses catalog eligibility deliberately; this tests state mechanics,
not the live mathematical authority supplied by the production controller.
"""
from __future__ import annotations

import argparse
from contextlib import ExitStack
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
import sqlite3
import subprocess
import sys
import time
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HELPER = ROOT/"software/v5/ordinary_module_bridge/closure_controls.py"
HELPER_SHA = "8015039fff02678d74adda770042309fb6a3a54085e8b787594414430163dc7f"
MIB = 1024**2


def need(condition, code):
    if not condition:
        raise AssertionError(code)


def helper():
    with HELPER.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() == HELPER_SHA, "ANCHOR_STORAGE_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_anchor_storage_helpers", HELPER)
    value = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = value
    exec(compile(raw, str(HELPER), "exec"), value.__dict__)
    return value


def controls(A, K, loaded, H, output, handles):
    E, S, PE = A.E, A.S, A.PE
    inventory = loaded.installation.read("inventory", MIB)
    semantic, foundation = S.semantic_id(), S.foundation_id()
    raws = {Path(path).stem: H.read(H.LOCAL/path, MIB) for path in H.FIXTURES}
    need({path: H.sha(raws[Path(path).stem]) for path in H.FIXTURES} == H.FIXTURES,
         "ANCHOR_STORAGE_FIXTURE_PINS")
    items = {unit: PE.read_evidence(raw) for unit, raw in raws.items()}
    mapping = {E.name_key(row[0]): S.basis_symbol_id(semantic, foundation, row[0])
               for row in json.loads(inventory)}
    targets = {}
    for unit, item in items.items():
        need(unit == item.unit_id and len(item.document["unit"][2]) == 1,
             "ANCHOR_STORAGE_SINGLETON_FIXTURE")
        name = item.document["unit"][2][0][0]
        target = {"name": name, "unit_id": unit, "export_id": S.export_id(semantic, unit, name)}
        targets[unit] = target
        mapping[E.name_key(name)] = target["export_id"]
    support_value = {"schema": K.SUPPORT_SCHEMA,
        "installation_manifest_sha256": loaded.installation.manifest_sha256,
        "semantic_id": semantic, "foundation_id": foundation,
        "implementation_id": loaded.installation.implementation_id,
        "policy": "INERT_STORAGE_CONTROL_NOT_A_SELECTED_MODULE_IMPORTER",
        "sources": {"inert_test": {"bytes": 1, "sha256": "1"*64}},
        "native_helpers": [["inert_fixture_not_code", 1, "2"*64]]}
    support = E.canonical_json(support_value)

    def fresh(label):
        directory = output/label
        directory.mkdir()
        catalog_path = directory/"catalog"
        catalog_path.mkdir()
        owner = A.OrdinaryAdmission.__new__(A.OrdinaryAdmission)
        catalog = A.P.PortableCatalog.__new__(A.P.PortableCatalog)
        catalog._root = catalog_path
        catalog._marker = E.canonical_json({"schema": "INERT_TEST_ADOPTION_NOT_CATALOG"})
        catalog._activation_raw = E.canonical_json({"schema": "INERT_TEST_ACTIVATION_NOT_CATALOG"})
        catalog._store_id = H.sha(label.encode("ascii"))
        A.P.PortableCatalog._write_fresh(catalog_path/"ADOPTION.json", catalog._marker)
        A.P.PortableCatalog._write_fresh(catalog_path/"owner.lock", b"x")
        catalog._lock = (catalog_path/"owner.lock").open("r+b")
        handles.append(catalog._lock)
        context = {"local_root": H.PARENT, "semantic_id": semantic, "foundation_id": foundation,
            "implementation_id": loaded.installation.implementation_id, "bindings": dict(mapping)}
        # Explicit authority stubs, not calls into real catalog/database logic.
        catalog._active = lambda: None
        def get_context(root):
            need(root == H.PARENT, "ANCHOR_STORAGE_INERT_CONTEXT_ROOT")
            return copy.deepcopy(context)
        catalog.context = get_context
        owner.catalog, owner.installation = catalog, loaded.installation
        store = K.open_for_owner(owner, support, H.check)
        return directory, owner, store, context

    def request(store, parent, unit):
        selected = [copy.deepcopy(targets[unit])]
        parent_id = "" if parent is None else parent.anchor_id
        key = K.materialization_key(store.support_id, parent_id, selected)
        plan = store.plan(parent)
        value = {"schema": K.M.REQUEST_SCHEMA, "semantic_id": semantic,
            "foundation_id": foundation, "context_root": H.PARENT,
            "module_name": H.name("DMKNBridge_"+key), "targets": [selected[0]["name"]],
            "unit_ids": [unit], "units": [items[unit].document["unit"]],
            "anchor_id": parent_id, "anchor_plan_sha256": H.sha(plan)}
        raw = E.canonical_json(value)
        pins = {"source_context_root": H.PARENT, "targets": selected,
            "materialization_key": key,
            "request": {"bytes": len(raw), "sha256": H.sha(raw)},
            "inventory": {"bytes": len(inventory), "sha256": H.sha(inventory)},
            "anchor_plan": {"bytes": len(plan), "sha256": H.sha(plan)}}
        return raw, plan, pins

    def prepare(directory, store, parent=None, unit=None):
        unit = H.TWICE if unit is None else unit
        raw, plan, pins = request(store, parent, unit)
        grant = store.reserve(parent, pins, H.check, deadline=time.monotonic()+30)
        generation = directory/("generation-"+grant.identifier)
        generation.mkdir()
        parsed = E.strict_json(raw)
        report = {key: copy.deepcopy(parsed[key]) for key in ("semantic_id", "foundation_id",
            "context_root", "module_name", "targets", "unit_ids", "anchor_id", "anchor_plan_sha256")}
        report.update(checking_passes=2, matched_unit_indices=[], matched_names=[],
                      added_names=[row[0] for row in parsed["units"][0][2]])
        parts = []
        text = "DMKNBridge_"+pins["materialization_key"]
        for suffix in K.PART_SUFFIXES:
            path = generation/(text+suffix)
            inert = ("NOT_A_LEAN_MODULE_STORAGE_CONTROL:"+suffix).encode("ascii")
            A.P.PortableCatalog._write_fresh(path, inert)
            parts.append({"path": path, "bytes": len(inert), "sha256": H.sha(inert)})
        event_bytes = {"request.json": raw, "inventory.json": inventory, "anchor-plan.json": plan,
            "native-report.json": E.canonical_json(report),
            "native-report.json.pending": b'{"fixture":"INERT_NO_NATIVE_EVENT"}',
            "native-report.json.phases.jsonl": b'{"fixture":"INERT_NO_PHASES"}\n',
            "SUPERVISION.json": b'{"fixture":"INERT_NO_SUPERVISOR"}'}
        events = {}
        for name, data in event_bytes.items():
            path = generation/name
            A.P.PortableCatalog._write_fresh(path, data)
            events[name] = {"path": path, "bytes": len(data), "sha256": H.sha(data)}
        return grant, {"request": raw, "report": report, "artifact_parts": parts, "event_files": events}

    def publish(directory, store, parent=None, unit=None):
        grant, live = prepare(directory, store, parent, unit)
        return store._commit_generated(grant, live, H.check)

    def rejected(call, fragment=None):
        try:
            call()
        except (ValueError, RuntimeError, OSError) as error:
            need(fragment is None or fragment in str(error), "ANCHOR_STORAGE_WRONG_REFUSAL:"+str(error))
            return error
        raise AssertionError("ANCHOR_STORAGE_MISSING_REFUSAL:"+str(fragment))

    def commit_last_and_warm_without_event_reads():
        directory, owner, store, context = fresh("commit-last")
        grant, live = prepare(directory, store)
        rename = K.os.rename
        observed = []
        def checked_rename(source, destination):
            need(not destination.exists() and source == grant.directory/"record.staged.json" and
                 (grant.directory/"CLOSED.json").is_file(), "ANCHOR_STORAGE_COMMIT_ORDER")
            need(len(list((grant.directory/"modules").iterdir())) == 5 and
                 len(list((grant.directory/"events").iterdir())) == 7,
                 "ANCHOR_STORAGE_COMPLETE_BEFORE_COMMIT")
            observed.append(True)
            return rename(source, destination)
        with patch.object(K.os, "rename", checked_rename):
            view = store._commit_generated(grant, live, H.check)
        need(observed == [True] and view.frontier.units[0][0] == H.TWICE,
             "ANCHOR_STORAGE_COMMITTED_VIEW")
        fresh_store = K.open_for_owner(owner, support, H.check)
        bounded = A.C.read_bounded
        def no_event_reads(path, maximum):
            need("events" not in Path(path).parts, "ANCHOR_STORAGE_OLD_PROOF_EVENT_READ")
            return bounded(path, maximum)
        with patch.object(A.C, "read_bounded", no_event_reads), patch.object(PE, "read_evidence", H.forbidden), \
                patch.object(E, "inspect_unit", H.forbidden):
            again = fresh_store.load(view.anchor_id, context, H.check)
        need(again == view, "ANCHOR_STORAGE_WARM_IDENTITY")
        child = publish(directory, fresh_store, view, H.TWICE_EQ)
        need(len(child.records) == len(child.import_directories) == 2 and
             {unit for unit, _ in child.frontier.units} == {H.TWICE, H.TWICE_EQ},
             "ANCHOR_STORAGE_CHILD_CHAIN")

    def no_manifest_or_uncommitted_adoption():
        directory, owner, store, _ = fresh("uncommitted")
        grant, live = prepare(directory, store)
        need(not list((store.root/"records").iterdir()), "ANCHOR_STORAGE_NO_EARLY_RECORD")
        A.P.PortableCatalog._write_fresh(directory/"MODULE.json", b'{"status":"PASS"}')
        rejected(lambda: store.load("e"*64, owner.catalog.context(H.PARENT), H.check))
        rejected(lambda: K.open_for_owner(owner, support, H.check))
        foreign = copy.copy(grant)
        rejected(lambda: store._commit_generated(foreign, live, H.check), "LIVE_GRANT_REQUIRED")
        store.abandon(grant, "INERT_NO_CHILD_STARTED")
        K.open_for_owner(owner, support, H.check)

    def artifact_and_context_corruption():
        directory, owner, store, context = fresh("artifact-corrupt")
        view = publish(directory, store)
        changed = copy.deepcopy(context)
        del changed["bindings"][E.name_key(targets[H.TWICE]["name"])]
        rejected(lambda: store.load(view.anchor_id, changed, H.check), "CURRENT_CONTEXT_MISMATCH")
        changed["bindings"][E.name_key(targets[H.TWICE]["name"])]= "0"*64
        rejected(lambda: store.load(view.anchor_id, changed, H.check), "CURRENT_CONTEXT_MISMATCH")
        # Compact groups must remain whole, nonoverlapping and identity-bound.
        # The registration event supplies completeness; these pure schema checks
        # do not invent authenticity for a newly hashed caller-created record.
        record = E.strict_json(view.records[0])
        repeated = copy.deepcopy(record["units"])
        repeated[0]["outputs"].append(copy.deepcopy(repeated[0]["outputs"][0]))
        rejected(lambda: store._units(repeated), "OUTPUT_NAME_CONFLICT")
        repeated = copy.deepcopy(record["units"])*2
        rejected(lambda: store._units(repeated), "DUPLICATE_UNIT")
        altered = copy.deepcopy(record["units"])
        altered[0]["outputs"][0]["export_id"] = "0"*64
        rejected(lambda: store._units(altered), "OUTPUT_EXPORT_BINDING")
        artifact = view.module_directory/(view.module_name+".olean.private")
        with artifact.open("ab") as stream:
            stream.write(b"CORRUPT")
        rejected(lambda: store.load(view.anchor_id, context, H.check), "FILE_SIZE")

    def record_and_foreign_support_refusals():
        directory, owner, store, context = fresh("record-support")
        view = publish(directory, store)
        alternative = copy.deepcopy(support_value)
        alternative["policy"] += "_DIFFERENT"
        foreign = K.open_for_owner(owner, E.canonical_json(alternative), H.check)
        rejected(lambda: foreign.load(view.anchor_id, context, H.check), "RECORD_SUPPORT")
        path = store.root/"records"/(view.anchor_id+".json")
        with path.open("ab") as stream:
            stream.write(b" ")
        rejected(lambda: store.load(view.anchor_id, context, H.check), "RECORD_ADDRESS")
        _, other_owner, other_store, other_context = fresh("foreign-owner")
        rejected(lambda: other_store.load(view.anchor_id, other_context, H.check))

    def missing_part_and_orphan_capacity():
        directory, owner, store, context = fresh("missing-part")
        view = publish(directory, store)
        artifact = view.module_directory/(view.module_name+".ir")
        artifact.rename(artifact.with_name(artifact.name+".preserved-missing"))
        rejected(lambda: store.load(view.anchor_id, context, H.check))
        directory2, owner2, store2, _ = fresh("orphan-capacity")
        grant, _ = prepare(directory2, store2)
        orphan = grant.directory/"orphan.bin"
        A.P.PortableCatalog._write_fresh(orphan, b"x"*19)
        store2.abandon(grant, "INERT_NO_CHILD_STARTED")
        total, count = store2._census(H.check)
        need(count == 1 and total >= 19, "ANCHOR_STORAGE_ORPHAN_CHARGED")
        raw, plan, pins = request(store2, None, H.TWICE)
        with patch.dict(K.LIMITS, {"max_operations": 1}):
            rejected(lambda: store2.reserve(None, pins, H.check, deadline=time.monotonic()+20), "CAPACITY")
        with patch.dict(K.LIMITS, {"max_store_bytes": total+K.LIMITS["max_operation_bytes"]-1}):
            rejected(lambda: store2.reserve(None, pins, H.check, deadline=time.monotonic()+20), "CAPACITY")

    def metadata_refusal_does_not_poison_reopen():
        directory, owner, store, _ = fresh("metadata-refusal")
        grant, live = prepare(directory, store)
        # No huge allocations: inflated pins must be refused before any copy.
        for pin in live["event_files"].values():
            pin["bytes"] = 8*MIB
        rejected(lambda: store._commit_generated(grant, live, H.check), "COPY_CAPACITY")
        need(not (grant.directory/"modules").exists() and not (grant.directory/"events").exists(),
             "ANCHOR_STORAGE_CAPACITY_BEFORE_WRITE")
        store.abandon(grant, "CLEAN_CAPACITY_REFUSAL")
        K.open_for_owner(owner, support, H.check)

    def ambiguous_commit_is_not_retried_or_abandoned():
        directory, owner, store, context = fresh("commit-unknown")
        grant, live = prepare(directory, store)
        original = K.os.rename
        def publish_then_error(source, destination):
            original(source, destination)
            raise OSError("INERT_SIMULATED_POST_RENAME_ERROR")
        with patch.object(K.os, "rename", publish_then_error):
            error = rejected(lambda: store._commit_generated(grant, live, H.check), "COMMIT_UNKNOWN")
        need(type(error) is K.AnchorCommitUnknown and error.report["anchor_id"] == error.anchor_id,
             "ANCHOR_STORAGE_UNKNOWN_DETAIL")
        committed_path = store.root/"records"/(error.anchor_id+".json")
        before = H.sha(H.read(committed_path, 2*MIB))
        store.abandon(grant, "MUST_NOT_REVOKE")
        need(H.sha(H.read(committed_path, 2*MIB)) == before, "ANCHOR_STORAGE_UNKNOWN_PRESERVED")
        reopened = K.open_for_owner(owner, support, H.check)
        need(reopened.load(error.anchor_id, context, H.check).anchor_id == error.anchor_id,
             "ANCHOR_STORAGE_EXACT_LOOKUP_RESOLVES")

    def uncertain_cleanup_and_incomplete_store():
        directory, owner, store, _ = fresh("cleanup-unknown")
        grant, _ = prepare(directory, store)
        # Even without BLOCKED, the pending reservation refuses reopening.
        rejected(lambda: K.open_for_owner(owner, support, H.check))
        store.mark_blocked(grant, "INERT_UNCERTAIN_CLEANUP", H.forbidden)
        rejected(lambda: K.open_for_owner(owner, support, H.check), "BLOCKED")
        need(not (grant.directory/"CLOSED.json").exists(), "ANCHOR_STORAGE_UNKNOWN_NOT_CLOSED")
        directory2, owner2, store2, _ = fresh("incomplete-marker")
        marker = store2.root/"STORE.json"
        marker.rename(marker.with_name("STORE.preserved.json"))
        rejected(lambda: K.open_for_owner(owner2, support, H.check))

    return [("commit-last-warm-no-proof-read-and-child-chain", commit_last_and_warm_without_event_reads),
        ("no-manifest-uncommitted-or-foreign-live-grant", no_manifest_or_uncommitted_adoption),
        ("missing-current-warrant-and-artifact-corruption", artifact_and_context_corruption),
        ("record-address-support-and-foreign-owner-refusals", record_and_foreign_support_refusals),
        ("missing-artifact-orphan-and-capacity-accounting", missing_part_and_orphan_capacity),
        ("precopy-metadata-refusal-remains-reopenable", metadata_refusal_does_not_poison_reopen),
        ("ambiguous-postrename-commit-preserved-exact-lookup", ambiguous_commit_is_not_retried_or_abandoned),
        ("uncertain-cleanup-and-incomplete-store-refuse", uncertain_cleanup_and_incomplete_store)]


def main(args):
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,
         "ANCHOR_STORAGE_PYTHON")
    H, results, handles = helper(), [], []
    try:
        with ExitStack() as guards:
            for target, attr in ((sqlite3, "connect"), (subprocess, "Popen"),
                                 (socket.socket, "connect"), (socket.socket, "connect_ex")):
                guards.enter_context(patch.object(target, attr, H.forbidden))
            loaded = H.selected_package(args)
            for operation in ("open", "preflight", "admit", "initialize"):
                guards.enter_context(patch.object(loaded.A.OrdinaryAdmission, operation, H.forbidden))
            output = loaded.A.C.ordinary(Path(args.output), directory=True)
            base = Path(__file__).absolute().parent
            collector = H.load_source(base/"module_closure.py", args.collector_sha256,
                                      "_anchor_storage_collector")
            guards.enter_context(patch.dict(sys.modules, {"module_closure": collector}))
            store = H.load_source(base/"anchor_store.py", args.store_sha256, "_anchor_storage_store")
            for label, call in controls(loaded.A, store, loaded, H, output, handles):
                H.check()
                try:
                    call()
                    results.append({"group": label, "ok": True})
                except BaseException as error:
                    results.append({"group": label, "ok": False, "error_type": type(error).__name__,
                                    "error": str(error)[:1000]})
            for relative, digest in H.FIXTURES.items():
                need(H.sha(H.read(H.LOCAL/relative, MIB)) == digest, "ANCHOR_STORAGE_SAVED_CHANGED")
        report = {"ok": len(results) == 8 and all(row["ok"] for row in results), "groups": results,
            "store_sha256": args.store_sha256, "collector_sha256": args.collector_sha256,
            "owner_opens": 0, "native_operations": 0,
            "claim": "INERT_OWNER_EVENT_AND_NONLEAN_ARTIFACT_STORAGE_CONTROLS_NOT_MATHEMATICAL_AUTHORITY"}
        H.save(output/"STORAGE-CONTROLS.json", report)
        print(json.dumps(report, sort_keys=True, allow_nan=False), flush=True)
        return 0 if report["ok"] else 1
    finally:
        for handle in handles:
            handle.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("package", "profile-sha256", "python-runtime", "lean-runtime", "output",
                 "collector-sha256", "store-sha256"):
        parser.add_argument("--"+name, required=True)
    raise SystemExit(main(parser.parse_args()))
