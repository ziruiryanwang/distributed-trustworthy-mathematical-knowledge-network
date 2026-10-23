"""Focused V2 catalog storage controls; root selects execution separately.

All names, source support claims and snapshot bytes are synthetic and unproved.
Private activation/commit calls test storage contracts ONLY: this harness does
not establish their eligible-importer or actual-clean-Lean-worker preconditions.
No V1 store, translator, Lean, network or certificate code is run. Output lives
under a required fresh --store-root and is retained, including refused states.
"""
from pathlib import Path
import argparse
from copy import copy, deepcopy
import hashlib
import os
import sqlite3
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ordinary_evidence as E
import ordinary_semantics as S
import portable_catalog as C
import local_catalog as L
import semantic_identity_checks as F


LIMITS = C.Limits(max_roots=8, max_operations=8, max_names=4096,
    max_manifest_bytes=2*1024*1024, max_artifact_bytes=1024*1024,
    max_total_artifact_bytes=16*1024*1024, max_db_pages=1024,
    max_batch_bytes=4*1024*1024, max_batch_units=8)


def ensure(ok, code):
    if not ok:
        raise AssertionError(code)


def refuses(marker, action):
    try:
        action()
    except C.CatalogError as exc:
        ensure(marker == str(exc), "WRONG_REFUSAL:" + str(exc))
    else:
        raise AssertionError("MISSING_REFUSAL:" + marker)


def report(label):
    print("PORTABLE_CATALOG_CHECK " + label + " PASS storage_only=true", flush=True)


def key(label):
    return hashlib.sha256(label.encode("ascii")).hexdigest()


def write_fresh(path, raw):
    L.ordinary(path, fresh=True)
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def profile():
    return {"schema": L.PROFILE, "kernel_support": "6"*64,
        "adapter_support": "7"*64, "basis_receiver_support": "8"*64,
        "basis_seed": L.SEED, "basis_inventory": L.INVENTORY,
        "expression_format": E.EXPR_FORMAT, "declaration_format": E.UNIT_FORMAT,
        "axiom_policy": "FIXED_BASIS_NO_NEW_AXIOM_UNSAFE_SORRY",
        "snapshot_format": "LEAN_4_34_MODULEDATA_NO_EXTENSIONS_NO_IR"}


def fixture(directory, *, omit_last_snapshot=False):
    """Make two synthetic records, NOT an eligible legacy mathematical source."""
    implementation = F.implementation()
    implementation_raw = E.canonical_json(implementation)
    store_id = key(directory.name)
    catalog, grant = C.PortableCatalog._create_importing(directory,
        implementation_raw, store_id, limits=LIMITS, seconds=120,
        output_bytes=4*1024*1024)
    try:
        s, f = catalog.semantic_id, catalog.foundation_id
        source_profile = profile()
        source_profile_id = L.digest("ordinary-native-profile-v1", source_profile)
        source_basis = L.digest("ordinary-basis-root-v1", [source_profile_id, L.SEED, L.INVENTORY])
        source_request = L.digest("ordinary-batch-v1", [key("inert-source-unit")])
        source_child = L.digest("ordinary-extension-root-v1",
            [source_profile_id, source_basis, source_request])
        source_roots = [source_basis, source_child]
        names = sorted([F.name("Nat")] + [F.name("SyntheticBasis"+str(i)) for i in range(580)],
                       key=E.name_key)
        source_support = sorted(source_profile[k] for k in C.SOURCE_SUPPORT_FIELDS)
        translation_support = "9"*64
        retained = sorted(set(source_support + [translation_support] +
                              [implementation[k] for k in C.SUPPORT_FIELDS]))
        audit_raw = E.canonical_json({"synthetic_storage_only": True})
        correspondence_raw = E.canonical_json({"synthetic_not_a_correspondence_proof": True})
        write_fresh(grant.directory / "audit.json", audit_raw)
        write_fresh(grant.directory / "correspondence.json", correspondence_raw)
        records, mapped_parent, source_parent = [], "", ""
        for ordinal, source_root in enumerate(source_roots):
            basis = ordinal == 0
            kind = "basis" if basis else "extension"
            old_bindings = ([[n, E.basis_symbol_id(source_profile_id, source_basis, n)] for n in names]
                if basis else [[F.name("SyntheticRetainedDeclaration"), key("source-export")]])
            bindings = ([[n, S.basis_symbol_id(s, f, n)] for n in names] if basis else
                        [[F.name("SyntheticRetainedDeclaration"), key("portable-export")]])
            snapshot = ("SYNTHETIC STORAGE CONTROL; NOT LEAN; slot="+str(ordinal)).encode("ascii")
            original = {"root": source_root, "profile_id": source_profile_id, "kind": kind,
                "parent": source_parent, "operation": key("source-operation-"+str(ordinal)),
                "request_hash": (L.digest("ordinary-fixed-basis-request-v1", [L.SEED, L.INVENTORY])
                                 if basis else source_request),
                "artifact_bytes": len(snapshot), "artifact_sha256": C.sha(snapshot),
                "bindings": old_bindings}
            original_raw = E.canonical_json(original)
            subdir = grant.directory / str(ordinal)
            subdir.mkdir()
            write_fresh(subdir / "source-record.json", original_raw)
            if not (omit_last_snapshot and ordinal == 1):
                write_fresh(subdir / "chunk.olean", snapshot)
            new_root = C.legacy_root_id(s, f, store_id, grant.identifier, source_root, mapped_parent)
            units = [] if basis else [key("inert-portable-unit")]
            record = {"schema": C.ROOT_SCHEMA, "local_root": new_root,
                "parent_root": mapped_parent, "kind": kind, "semantic_id": s, "foundation_id": f,
                "input_unit_ids": units,
                "request_hash": C.basis_request_id(s, f) if basis else C.batch_id(units),
                "bindings": bindings,
                "snapshot": {"module_name": L.module_name(source_root),
                    "parent_module": L.module_name(source_parent) if source_parent else [],
                    "relative_path": "imports/"+grant.identifier+"/"+str(ordinal)+"/chunk.olean",
                    "artifact_bytes": len(snapshot), "artifact_sha256": C.sha(snapshot),
                    "writer_origin": "retained-v1-check"},
                "origin": "legacy-translation",
                "provenance": {"import_id": grant.identifier, "ordinal": ordinal,
                    "source_store_id": key("synthetic-source-store"), "source_profile_id": source_profile_id,
                    "source_root": source_root, "source_parent_root": source_parent,
                    "source_record_sha256": C.sha(original_raw), "source_operation_id": original["operation"],
                    "source_check_support": source_support, "translation_support": translation_support}}
            records.append(E.canonical_json(record))
            mapped_parent, source_parent = new_root, source_root
        manifest = {"schema": C.IMPORT_SCHEMA, "import_id": grant.identifier,
            "semantic_id": s, "foundation_id": f, "implementation_id": catalog.implementation_id,
            "store_id": store_id, "source_store_id": key("synthetic-source-store"),
            "source_profile": source_profile, "source_selected_root": source_child,
            "source_manifest_sha256": key("synthetic-source-manifest"),
            "correspondence_sha256": C.sha(correspondence_raw),
            "translation_support": translation_support, "source_check_support": source_support,
            "retained_support": retained,
            "roots": [[E.strict_json(raw)["local_root"], C.sha(raw)] for raw in records],
            "audit": {"relative_path": "imports/"+grant.identifier+"/audit.json",
                "artifact_bytes": len(audit_raw), "artifact_sha256": C.sha(audit_raw)}}
        return {"catalog": catalog, "grant": grant, "records": records, "manifest": manifest,
                "implementation_raw": implementation_raw, "store_id": store_id,
                "source_roots": source_roots, "directory": directory}
    except BaseException:
        catalog.close()
        raise


def reopen(item, implementation_raw=None):
    return C.PortableCatalog.open(item["directory"], implementation_raw or item["implementation_raw"],
                                  item["store_id"], limits=LIMITS)


def activate(item, callback, *, records=None, manifest=None, grant=None):
    return item["catalog"]._activate_import(grant or item["grant"],
        item["records"] if records is None else records,
        E.canonical_json(item["manifest"] if manifest is None else manifest), source_recheck=callback)


def untouched_quarantine(item):
    """Inspect only after the owner handle is closed; no recovery/migration."""
    refuses("PORTABLE_CATALOG_IMPORTING", lambda: reopen(item))
    uri = (item["directory"] / "catalog.sqlite").as_uri() + "?mode=ro"
    db = sqlite3.connect(uri, uri=True)
    try:
        ensure(all(db.execute("SELECT count(*) FROM " + table).fetchone() == (0,)
                   for table in ("roots", "operations", "imports")), "PARTIAL_ROWS_SURVIVED")
        raw = bytes(db.execute("SELECT activation FROM meta WHERE id=1").fetchone()[0])
        ensure(E.strict_json(raw)["state"] == "IMPORTING", "PREACTIVATION_NOT_QUARANTINED")
    finally:
        db.close()


def importing_control(root):
    item = fixture(root / "interrupted-before-activation")
    catalog = item["catalog"]
    try:
        selected = item["manifest"]["roots"][-1][0]
        refuses("PORTABLE_CATALOG_IMPORTING", lambda: catalog.context(selected))
        refuses("PORTABLE_CATALOG_IMPORTING", lambda: catalog.reserve_basis([]))
        refuses("PORTABLE_CATALOG_IMPORTING", lambda: catalog.reserve_extension(selected, []))
    finally:
        catalog.close()
    untouched_quarantine(item)
    report("importing_unavailable_and_closed_pre_activation")


def activation_and_grant_control(root):
    item = fixture(root / "activated")
    catalog = item["catalog"]
    calls = []
    try:
        selected = activate(item, lambda: calls.append("synthetic-storage-event"))
        ensure(len(calls) == 2 and selected == item["manifest"]["roots"][-1][0], "ACTIVATION_CALLBACKS")
        before = catalog.context(selected)
        expected_modules = [L.module_name(value) for value in item["source_roots"]]
        ensure(before["root_module"] == expected_modules[-1] and
               before["basis_module"] == expected_modules[0] and len(before["bindings"]) == 582 and
               [row["module_name"] for row in before["modules"]] == expected_modules and
               before["modules"][-1]["parent_module"] == expected_modules[0] and
               before["root_module"] != L.module_name(selected) and
               before["retained_support"] == item["manifest"]["retained_support"], "IMPORTED_MODULE_ORIGIN")
        refuses("PORTABLE_LIVE_IMPORT_REQUIRED", lambda: activate(item, lambda: None))
        catalog.close()
        catalog = reopen(item)
        ensure(catalog.context(selected) == before, "REOPEN_CONTEXT_CHANGED")
        raw = F.evidence(catalog.semantic_id)
        grant = catalog.reserve_extension(selected, [raw], seconds=120, output_bytes=4096)
        ensure(grant.parent_module_raw == E.canonical_json(expected_modules[-1]) and
               grant.parent_plan_raw == E.canonical_json(before["modules"]) and
               grant.input_unit_ids == (S.portable_unit_id(raw),), "NEW_GRANT_PARENT_PLAN")
        refuses("CATALOG_LIVE_GRANT_REQUIRED", lambda: catalog._commit_checked(copy(grant)))
        for field, bad in (("parent_plan_raw", b"[]"), ("parent_module_raw", b"[]"),
                           ("input_unit_ids", (key("wrong-input-unit"),))):
            original = getattr(grant, field)
            setattr(grant, field, bad)
            try:
                refuses("CATALOG_LIVE_GRANT_REQUIRED", lambda: catalog._commit_checked(grant))
            finally:
                setattr(grant, field, original)
        # Deliberate private storage-only commit; NO clean native event exists.
        write_fresh(grant.directory / "chunk.olean", b"SYNTHETIC NATIVE OUTPUT; NOT LEAN")
        child = catalog._commit_checked(grant)
        after = catalog.context(child)
        ensure(after["modules"][:-1] == before["modules"] and len(after["bindings"]) == 583 and
               after["modules"][-1]["parent_module"] == expected_modules[-1] and
               after["root_module"] == L.module_name(child), "NATIVE_CHILD_LOST_IMPORTED_PARENT")
        catalog.close()
        catalog = reopen(item)
        ensure(catalog.context(child) == after, "CHILD_REOPEN_CHANGED")
    finally:
        catalog.close()
    report("complete_activation_original_modules_and_bound_child_plan")
    return item, child


def binding_control(root):
    item = fixture(root / "refused-bindings")
    catalog = item["catalog"]
    called = []
    callback = lambda: called.append(True)
    try:
        refuses("PORTABLE_LIVE_IMPORT_REQUIRED", lambda: activate(item, callback, grant=copy(item["grant"])))
        refuses("PORTABLE_IMPORT_ROOT_MANIFEST", lambda: activate(item, callback, records=item["records"][:-1]))
        changed = deepcopy(item["manifest"])
        changed["roots"][-1][1] = key("wrong-root-record-hash")
        refuses("PORTABLE_IMPORT_ROOT_MANIFEST", lambda: activate(item, callback, manifest=changed))
        changed = deepcopy(item["manifest"])
        changed["retained_support"] = changed["retained_support"][:-1]
        refuses("PORTABLE_RETAINED_SUPPORT", lambda: activate(item, callback, manifest=changed))
        changed = deepcopy(item["manifest"])
        changed["source_check_support"] = changed["source_check_support"][:-1]
        refuses("PORTABLE_SOURCE_SUPPORT_OMISSION", lambda: activate(item, callback, manifest=changed))
        ensure(not called, "INVALID_IMPORT_REACHED_SOURCE_RECHECK")
    finally:
        catalog.close()
    untouched_quarantine(item)
    missing = fixture(root / "missing-selected-snapshot", omit_last_snapshot=True)
    try:
        refuses("CATALOG_MISSING_PATH", lambda: activate(missing, callback))
        ensure(not called, "MISSING_FILE_REACHED_SOURCE_RECHECK")
    finally:
        missing["catalog"].close()
    untouched_quarantine(missing)
    report("complete_manifest_support_and_snapshot_required")


def interrupted_transaction_control(root):
    item = fixture(root / "interrupted-inside-activation")
    calls = []
    def second_recheck_fails():
        calls.append(True)
        if len(calls) == 2:
            raise RuntimeError("SYNTHETIC_SOURCE_BECAME_INELIGIBLE")
    try:
        refuses("CATALOG_TRANSACTION_UNCERTAIN_REOPEN_REQUIRED",
                lambda: activate(item, second_recheck_fails))
        ensure(len(calls) == 2, "DID_NOT_REACH_IN_TRANSACTION_RECHECK")
        refuses("CATALOG_CLOSED", lambda: item["catalog"].context(item["manifest"]["roots"][-1][0]))
    finally:
        item["catalog"].close()
    untouched_quarantine(item)
    report("failed_live_recheck_rolls_back_and_invalidates_authority")


def support_and_withdrawal_control(item, child):
    changed = E.strict_json(item["implementation_raw"])
    changed["controller_support"] = key("different-controller")
    refuses("CATALOG_ADOPTION", lambda: reopen(item, E.canonical_json(changed)))
    catalog = reopen(item)
    try:
        catalog.context(child)
        write_fresh(item["directory"] / "WITHDRAWN", b"SYNTHETIC TEST: retained support withdrawn")
        refuses("CATALOG_WITHDRAWN", lambda: catalog.context(child))
        refuses("CATALOG_WITHDRAWN", lambda: catalog.reserve_extension(child, []))
    finally:
        catalog.close()
    refuses("CATALOG_WITHDRAWN", lambda: reopen(item))
    report("changed_implementation_and_active_support_withdrawal_refused")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store-root", required=True)
    args = parser.parse_args()
    ensure(os.name == "nt", "WINDOWS_ONLY_STORAGE_CONTROLS")
    root = L.ordinary(Path(args.store_root), directory=True, fresh=True)
    root.mkdir()
    print("SYNTHETIC_STORAGE_ONLY mathematical_acceptance=false migration_qualified=false", flush=True)
    importing_control(root)
    item, child = activation_and_grant_control(root)
    binding_control(root)
    interrupted_transaction_control(root)
    support_and_withdrawal_control(item, child)
    print("PORTABLE_CATALOG_ALL_PASS groups=5 mathematical_acceptance=false migration_qualified=false", flush=True)


if __name__ == "__main__":
    main()
