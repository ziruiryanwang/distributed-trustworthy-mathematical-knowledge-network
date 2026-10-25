"""Protected local grounded-cut events; source candidate, not peer authority.

Load only through the pinned cut bootstrap in a clean approved owner process.
The OS, approved code, immutable support, serialized owner access and absence of
whole-state rollback are premises. Never run peer Python/Lean source here.
Public return remains inert ordinary V2 evidence. No scratch snapshot is retained.
"""
from dataclasses import dataclass
import hashlib
import os
import secrets

import ordinary_evidence as E
import ordinary_semantics as S
import ordinary_admission as A
import portable_evidence as PE
import portable_catalog as P
import cut_map as M
import cut_summary as Q
import cut_catalog as K
import source_anchor as H
import cut_runtime as R

MIB = 1024**2
INTENT = "DMKN_GROUNDED_CUT_COMMIT_INTENT_V1"


def need(ok, code):
    if not ok:
        raise ValueError("GROUNDED_CONTROLLER_" + code)


@dataclass(frozen=True)
class MigrationLimits:
    max_units: int = 65536
    max_names: int = 262144
    max_acquired_bytes: int = 512 * MIB
    max_nodes: int = 40000000

    def __post_init__(self):
        for name, cap in (("max_units", 65536), ("max_names", 262144),
                          ("max_acquired_bytes", 512 * MIB), ("max_nodes", 40000000)):
            need(type(getattr(self, name)) is int and 0 < getattr(self, name) <= cap,
                 "MIGRATION_LIMIT")


def _claim(runtime, budget, allowance):
    need(type(runtime) is R.CutRuntime and type(budget) is A.OperationBudget and
         type(allowance) is M.Allowance, "APPROVED_TYPES")
    budget.claim()
    runtime.verify(budget.check)


def _basis(runtime, check):
    check()
    seed = runtime.base.installation.read("seed", MIB)
    inventory = runtime.base.installation.read("inventory", MIB)
    need(hashlib.sha256(seed).hexdigest() == S.SEED and
         hashlib.sha256(inventory).hexdigest() == S.INVENTORY, "FIXED_BASIS_BYTES")
    seed_doc, rows = A._writer_json(seed, MIB), A._writer_json(inventory, MIB)
    names = seed_doc[2]
    need(type(names) is list and len(names) == 581 and
         [row[0] for row in rows] == names, "FIXED_BASIS_CENSUS")
    basis = {E.name_key(name): S.basis_symbol_id(S.semantic_id(), S.foundation_id(), name)
             for name in names}
    need(len(basis) == 581, "FIXED_BASIS_DUPLICATE")
    check()
    return basis, len(seed) + len(inventory)


def _disjoint(paths):
    for i, left in enumerate(paths):
        for right in paths[i + 1:]:
            need(not left.is_relative_to(right) and not right.is_relative_to(left),
                 "STATE_SUPPORT_CALL_OVERLAP")


def _paths(runtime, directory, source, custody, call_directory, *, create):
    target = P.ordinary(directory, directory=True, fresh=create)
    call = P.ordinary(call_directory, directory=True, fresh=True)
    need(type(custody) is runtime.base.O.OrdinaryStore and
         custody.semantic_id == runtime.semantic_id, "APPROVED_CUSTODY")
    paths = [target, P.ordinary(source, directory=True),
             P.ordinary(custody.root, directory=True), call, runtime.root, runtime.base.root]
    paths.extend(runtime.base.installation.runtime_roots.values())
    _disjoint(paths)
    return target, call


def _blob(catalog, schema, **fields):
    return catalog.put_summary(E.canonical_json(dict(schema=schema, **fields)))


def _record(catalog, *, kind, parent, map_root, request_id, unit_id,
            frontier_summary, result_summary, event_summary):
    return dict(schema=K.ROOT_SCHEMA, **catalog._identity, kind=kind, parent=parent,
                map_root=map_root, request_id=request_id, unit_id=unit_id,
                frontier_summary=frontier_summary, result_summary=result_summary,
                event_summary=event_summary)


def _commit(catalog, record, call, check):
    """Persist exact proposed root BEFORE COMMIT; never replay on ambiguous reply."""
    check()
    raw = catalog._record(record)
    candidate = hashlib.sha256(K.ROOT_DOMAIN + raw).hexdigest()
    intent = E.canonical_json(dict(schema=INTENT, directory=str(catalog._root),
                                  candidate_root=candidate, record=record))
    need(len(intent) <= 128 * 1024, "INTENT_BOUND")
    P.PortableCatalog._write_fresh(call / "COMMIT-INTENT.json", intent)
    need(P.read_bounded(call / "COMMIT-INTENT.json", 128 * 1024) == intent,
         "INTENT_CHANGED")
    check()
    result = catalog._commit_root(record)
    need(result == candidate, "COMMIT_IDENTITY")
    # No post-COMMIT fallible file writes are needed to discover the outcome.
    return {"local_root": result, "origin": "grounded-cut", "kind": record["kind"],
            "request_id": record["request_id"], "support_id": record["support_id"]}


def bootstrap(runtime, native, selected_root, custody, directory, call_directory, *,
              store_id, epoch, budget, allowance, limits=K.Limits(),
              migration=MigrationLimits()):
    """Once, from a locked eligible local native lineage and exact retained claims.

    The original native owner remains open/locked; this does not acquire it twice.
    Full context validation and original proof-unit reads are charged setup work.
    A failed BOOTSTRAPPING store cannot silently resume or become a warrant.
    """
    _claim(runtime, budget, allowance)
    need(type(migration) is MigrationLimits and type(native) is P.PortableCatalog,
         "BOOTSTRAP_TYPES")
    need(budget.output_bytes >= 128 * 1024, "BOOTSTRAP_CALL_SPOOL_BOUND")
    binding, context = H.capture(native, selected_root, check=budget.check)
    need(context["implementation_id"] == runtime.base.installation.implementation_id,
         "NATIVE_IMPLEMENTATION")
    target, call = _paths(runtime, directory, native._root, custody, call_directory, create=True)
    basis, _ = _basis(runtime, budget.check)
    full = context["bindings"]
    need(len(full) <= migration.max_names and
         all(full.get(name) == symbol for name, symbol in basis.items()), "SOURCE_BASIS")

    def check():
        budget.check()
        native._active()
        need(native._lock is not None and not native._lock.closed, "NATIVE_LOCK_LOST")
        budget.check()

    catalog = K.CutCatalog.open(target, store_id=store_id, support_id=runtime.support_id,
        epoch=epoch, source_binding_raw=binding, check=check, create=True, limits=limits)
    try:
        call.mkdir()
        catalog._begin(allowance)
        map_root, covered, units = M.EMPTY_ROOT, set(), set()
        acquired, nodes = 0, 0
        for key, symbol in full.items():
            check()
            if key in basis or key in covered:
                continue
            need(len(units) < migration.max_units, "MIGRATION_UNIT_BOUND")
            locator_raw = custody.get_locator(runtime.semantic_id, symbol, 32768, check_budget=check)
            acquired += len(locator_raw)
            need(acquired < migration.max_acquired_bytes, "MIGRATION_BYTE_BOUND")
            locator = E.strict_json(locator_raw, E.Limits(max_bytes=32768))
            need(E.name_key(locator["export_name"]) == key and
                 locator["semantic_id"] == runtime.semantic_id, "LOCATOR_NAME")
            unit_id = P.hexid(locator["unit_id"])
            need(unit_id not in units, "MIGRATION_PARTIAL_GROUP")
            raw = custody.get_evidence(runtime.semantic_id, unit_id,
                min(Q.Limits().syntax.max_bytes, migration.max_acquired_bytes - acquired),
                check_budget=check)
            acquired += len(raw)
            evidence = PE.read_evidence(raw)
            need(evidence.unit_id == unit_id and
                 evidence.document["semantic_id"] == runtime.semantic_id, "MIGRATION_UNIT_ID")
            nodes += evidence.census.total_nodes
            need(nodes <= migration.max_nodes, "MIGRATION_NODE_BOUND")
            for name, imported in evidence.document["imports"]:
                need(full.get(E.name_key(name)) == imported, "MIGRATION_IMPORT")
            projected = Q.project(raw)
            need(dict(projected.bindings).get(key) == symbol, "MIGRATION_DEMANDED_EXPORT")
            for name, export in projected.bindings:
                need(name not in basis and name not in covered and full.get(name) == export,
                     "MIGRATION_EXACT_GROUP")
            digest = catalog.put_summary(projected.raw)
            need(digest == projected.summary_id, "SUMMARY_DOMAIN")
            for name, export in projected.bindings:
                map_root = catalog._insert(map_root, name, E.canonical_json([export, digest]))
                covered.add(name)
            units.add(unit_id)
        need(len(covered) + len(basis) == len(full), "MIGRATION_COMPLETE_COVERAGE")
        request_id = secrets.token_hex(32)
        frontier = _blob(catalog, "DMKN_CUT_BOOTSTRAP_FRONTIER_V1", source_root=selected_root,
                         bindings=len(covered), units=len(units))
        result = _blob(catalog, "DMKN_CUT_BOOTSTRAP_RESULT_V1", map_root=map_root)
        event = _blob(catalog, "DMKN_CUT_NATIVE_DERIVATION_EVENT_V1", request_id=request_id,
            source_root=selected_root, source_binding_sha256=hashlib.sha256(binding).hexdigest(),
            acquired_bytes=acquired, encoded_nodes=nodes)
        record = _record(catalog, kind="native-bootstrap", parent="", map_root=map_root,
            request_id=request_id, unit_id="", frontier_summary=frontier,
            result_summary=result, event_summary=event)
        runtime.verify(check)
        return _commit(catalog, record, call, check)
    finally:
        catalog.close()


def _marker(directory, store_id, epoch, runtime, limits):
    directory = P.ordinary(directory, directory=True)
    raw = P.read_bounded(directory / "ADOPTION.json", 512 * 1024)
    doc = E.strict_json(raw, E.Limits(max_bytes=512 * 1024))
    need(type(doc) is dict and doc.get("schema") == K.SCHEMA and
         doc.get("store_id") == P.hexid(store_id) and doc.get("epoch") == P.hexid(epoch) and
         doc.get("support_id") == runtime.support_id, "EXPECTED_LOCAL_IDENTITY")
    value = doc.get("source_binding_hex")
    binding = H._raw_hex(value, H.MAX_BINDING)
    anchor_doc, _, _ = H.parse_binding(binding)
    need(doc.get("source_binding_sha256") == hashlib.sha256(binding).hexdigest() and
         anchor_doc["implementation_id"] == runtime.base.installation.implementation_id,
         "SOURCE_SUPPORT_BINDING")
    # Exact entire marker, including limits, is checked by CutCatalog.open.
    return directory, binding, anchor_doc


def extend(runtime, directory, parent_root, raw_new, custody, call_directory, *,
           store_id, epoch, budget, allowance, limits=K.Limits(), preparation=Q.Limits()):
    """One actual new theorem over earlier committed members, no implicit fallback."""
    _claim(runtime, budget, allowance)
    target, binding, anchor_doc = _marker(directory, store_id, epoch, runtime, limits)
    _, call = _paths(runtime, target, anchor_doc["directory"], custody, call_directory, create=False)
    basis, fixed_bytes = _basis(runtime, budget.check)
    with H.SourceAnchor.open(binding, check=budget.check) as anchor:
        catalog = K.CutCatalog.open(target, store_id=store_id, support_id=runtime.support_id,
            epoch=epoch, source_binding_raw=binding, check=anchor.check, limits=limits)
        try:
            catalog._begin(allowance)
            parent = catalog.root(P.hexid(parent_root))

            def lookup(name):
                raw = catalog.lookup(parent_root, E.name_key(name))
                if raw is None:
                    return None
                row = E.strict_json(raw, E.Limits(max_bytes=4096))
                need(type(row) is list and len(row) == 2, "MAP_VALUE")
                return P.hexid(row[0]), P.hexid(row[1])

            prepared = Q.prepare(raw_new, semantic_id=runtime.semantic_id, basis=basis,
                lookup=lookup, read_summary=catalog.read_summary, check=anchor.check,
                limits=preparation)
            request_id = secrets.token_hex(32)
            packet = E.canonical_json(dict(schema="DMKN_GROUNDED_CUT_BASIS_REQUEST_V1",
                request_id=request_id,
                concrete_units=[E.strict_json(raw) for raw in prepared.concrete_units],
                signature_rows=[E.strict_json(raw) for raw in prepared.signature_rows],
                new_unit=E.strict_json(prepared.new_unit)))
            # Reserve the bounded runtime-inserted authenticated descriptor.
            need(len(packet) + fixed_bytes + 256 * 1024 <= 64 * MIB,
                 "WHOLE_PACKET_BYTE_BOUND")
            need(len(packet) + 256 * 1024 + 18 * MIB + 2 * budget.log_bytes + 128 * 1024 <=
                 budget.output_bytes, "COMPLETE_CALL_SPOOL_BOUND")
            # Separate inert public custody; it is never used as local truth.
            held = custody.put_evidence(raw_new, before_commit=anchor.check)
            need(held["semantic_id"] == runtime.semantic_id and
                 held["identity"] == prepared.new_summary.unit_id and
                 held["raw_sha256"] == hashlib.sha256(raw_new).hexdigest() and
                 held["raw_bytes"] == len(raw_new) and held["mathematical_acceptance"] is False,
                 "CUSTODY_BINDING")
            need(custody.get_evidence(runtime.semantic_id, prepared.new_summary.unit_id,
                 len(raw_new), check_budget=anchor.check) == raw_new, "CUSTODY_READBACK")
            try:
                report_raw, observation, authenticated_packet = runtime.check_packet(
                    packet, call, budget, anchor=anchor)
            except R.UncertainWorker:
                marker = target / "WITHDRAWN"
                if not os.path.lexists(marker):
                    P.PortableCatalog._write_fresh(marker, b"GROUNDED_CUT_WORKER_CLEANUP_UNCERTAIN")
                raise
            anchor.check()
            need(catalog.root(parent_root) == parent, "PARENT_CHANGED")
            for name, symbol, digest in prepared.frontier:
                need(catalog.lookup(parent_root, name) == E.canonical_json([symbol, digest]),
                     "FRONTIER_CHANGED")
            for name in prepared.absent_names:
                need(name not in basis and catalog.lookup(parent_root, name) is None,
                     "GLOBAL_NAME_NOT_FRESH")
            digest = catalog.put_summary(prepared.new_summary.raw)
            need(digest == prepared.new_summary.summary_id, "NEW_SUMMARY_BINDING")
            map_root = parent["map_root"]
            for name, symbol in prepared.new_summary.bindings:
                map_root = catalog._insert(map_root, name, E.canonical_json([symbol, digest]))
            frontier = _blob(catalog, "DMKN_CUT_SELECTED_FRONTIER_V1", parent=parent_root,
                names=[[name.hex(), symbol, value] for name, symbol, value in prepared.frontier])
            event = _blob(catalog, "DMKN_CUT_CLEAN_CHECK_EVENT_V1", request_id=request_id,
                request_sha256=hashlib.sha256(authenticated_packet).hexdigest(),
                basis_artifact_bytes=anchor._doc["basis"]["artifact_bytes"],
                basis_hash_bytes=anchor._doc["basis"]["artifact_bytes"],
                report_sha256=hashlib.sha256(report_raw).hexdigest(),
                observation=observation, preparation=vars(prepared.stats))
            record = _record(catalog, kind="theorem-cut", parent=parent_root, map_root=map_root,
                request_id=request_id, unit_id=prepared.new_summary.unit_id,
                frontier_summary=frontier, result_summary=digest, event_summary=event)
            return _commit(catalog, record, call, anchor.check)
        finally:
            catalog.close()


def resolve(runtime, directory, call_directory, *, store_id, epoch, budget, allowance,
            limits=K.Limits()):
    """Resolve exact durable intent by root PK; NEVER replay a check or commit.

    A hot journal, incomplete bootstrap, withdrawn support or lost intent refuses;
    it does not mean NOT_COMMITTED and does not authorize retry. This API handles
    lost replies around a fully durable SQLite commit, not arbitrary disk recovery.
    """
    _claim(runtime, budget, allowance)
    target, binding, _ = _marker(directory, store_id, epoch, runtime, limits)
    call = P.ordinary(call_directory, directory=True)
    raw = P.read_bounded(call / "COMMIT-INTENT.json", 128 * 1024)
    doc = E.strict_json(raw, E.Limits(max_bytes=128 * 1024))
    need(type(doc) is dict and set(doc) == {"schema", "directory", "candidate_root", "record"}
         and doc["schema"] == INTENT and doc["directory"] == str(target), "INTENT_IDENTITY")
    candidate = P.hexid(doc["candidate_root"])
    with H.SourceAnchor.open(binding, check=budget.check) as anchor:
        catalog = K.CutCatalog.open(target, store_id=store_id, support_id=runtime.support_id,
            epoch=epoch, source_binding_raw=binding, check=anchor.check, limits=limits)
        try:
            catalog._begin(allowance)
            expected = catalog._record(doc["record"])
            need(hashlib.sha256(K.ROOT_DOMAIN + expected).hexdigest() == candidate,
                 "INTENT_ROOT_HASH")
            actual = catalog._read("roots", candidate, limits.max_root_bytes, K.ROOT_DOMAIN, True)
            need(actual is None or actual == expected, "COMMITTED_RECORD_CHANGED")
            if actual is not None:
                need(catalog.root(candidate) == doc["record"], "COMMITTED_IDENTITY")
            anchor.check()
            return {"disposition": "COMMITTED" if actual is not None else "NOT_COMMITTED",
                    "local_root": candidate, "request_id": doc["record"]["request_id"],
                    "reexecuted": False}
        finally:
            catalog.close()
