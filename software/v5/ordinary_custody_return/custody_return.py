"""Bounded inert custody-to-bundle handoff; never mathematical acceptance.

Load through the approved ordinary package first. The caller owns support and
custody, serializes access, and supplies one original operation-budget callback.
No source execution, catalog, peer, certificate, or native worker is used here.
"""
from __future__ import annotations

from collections import deque
from dataclasses import replace
import hashlib
import heapq
import os
from pathlib import Path
import sys

import ordinary_admission as A
import baseline_bundle as B
import portable_preview as PP
from transport import ordinary_acquisition as O

E, S, PE = A.E, A.S, A.PE
Limits = B.Limits
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError("CUSTODY_RETURN_" + code)


def _separate(left, right):
    need(not left.is_relative_to(right) and not right.is_relative_to(left),
         "OUTPUT_OR_SUPPORT_OVERLAP")


def _write(path, raw, maximum, check):
    check()
    need(type(raw) is bytes and 0 < len(raw) <= maximum, "OUTPUT_BYTES")
    A.C.ordinary(path, fresh=True)
    with path.open("xb") as stream:
        need(stream.write(raw) == len(raw), "OUTPUT_SHORT_WRITE")
        stream.flush()
        os.fsync(stream.fileno())
    check()
    need(A.C.read_bounded(path, maximum) == raw, "OUTPUT_CHANGED")


def _basis(loaded, check):
    check()
    raw = loaded.installation.read("inventory", MIB)
    need(hashlib.sha256(raw).hexdigest() == S.INVENTORY, "FIXED_INVENTORY_PIN")
    rows = E._array(A._writer_json(raw, MIB), 581)
    result = {}
    for row in rows:
        check()
        name = E._array(row, 5)[0]
        key = E.name_key(name)
        need(key not in result, "FIXED_BASIS_DUPLICATE")
        result[key] = S.basis_symbol_id(S.semantic_id(), S.foundation_id(), name)
    need(len(result) == 581, "FIXED_BASIS_CENSUS")
    return result


def write_bundle(loaded, custody, export_ids, *, policy, output,
                 limits=Limits(), check):
    """Return ordinary file-bundle metadata; retain partial output on failure.

    ``loaded`` is the exact approved ordinary profile.load namespace; ``custody``
    is its already-open OrdinaryStore. ``export_ids`` are exact portable exports.
    selected-units acquires no dependency units. closed-basis follows every proof
    import until the pinned basis. Both preserve complete generated groups and
    expose exact imports not supplied by the emitted units in obligations.json.

    ``check`` must charge one original finite wall/CPU allowance, never reset it.
    All caps are operation-wide. They bound data, not hard process RSS/time.
    This API neither opens nor closes custody and performs no logical DB writes.
    Existing custody opening/recovery policy is the caller's responsibility.
    """
    need(callable(check) and type(limits) is Limits, "CONFIGURATION")
    limits.__post_init__()
    check()
    semantic = S.semantic_id()
    need(loaded.A is A and loaded.O is O and
         sys.modules.get("ordinary_admission") is A and
         sys.modules.get("baseline_bundle") is B and
         loaded.baseline_intake.B is B and B.E is E and B.S is S and B.PE is PE,
         "APPROVED_MODULE_GRAPH")
    need(type(custody) is O.OrdinaryStore and custody.db is not None and
         custody.semantic_id == semantic == loaded.installation.semantic_id,
         "CUSTODY_SEMANTICS")
    need(policy in ("selected-units", "closed-basis"), "EXPLICIT_POLICY")
    need(type(export_ids) in (list, tuple) and 0 < len(export_ids) <= limits.max_targets,
         "TARGET_COUNT")
    targets = tuple(E._hex(value) for value in export_ids)
    target_set = set(targets)
    need(len(target_set) == len(targets), "DUPLICATE_TARGET")
    root = A.C.ordinary(Path(output), directory=True, fresh=True)
    store_root = A.C.ordinary(custody.root, directory=True)
    protected = (A.C.ordinary(loaded.root, directory=True),
                 A.C.ordinary(Path(__file__).absolute().parent, directory=True),
                 *(A.C.ordinary(path, directory=True)
                   for path in loaded.installation.runtime_roots.values()))
    for other in (store_root, *protected):
        _separate(root, other)
    for other in protected:
        _separate(store_root, other)
    basis = _basis(loaded, check)
    check()
    root.mkdir()
    (root / "units").mkdir()

    # One binding per exact structured name across all selected outputs/imports.
    # Distinct names include unresolved obligations, not only emitted outputs.
    bindings, providers, exports, units, imports = {}, {}, {}, {}, {}
    totals = {"units": 0, "evidence_bytes": 0, "locator_bytes": 0,
              "nodes": 0, "edges": 0, "names": 0, "binding_bytes": 0}

    def bind(key, symbol):
        check()
        if key in bindings:
            need(bindings[key] == symbol, "CONFLICTING_NAME_BINDING")
            return
        need(key not in basis or basis[key] == symbol, "FIXED_BASIS_BINDING")
        size = len(key) + 64
        need(totals["names"] < limits.max_names and
             totals["binding_bytes"] + size <= limits.max_binding_bytes,
             "DISTINCT_NAME_OR_BINDING_BOUND")
        bindings[key] = symbol
        totals["names"] += 1
        totals["binding_bytes"] += size

    pending = deque((identity, None) for identity in targets)
    queued = set(targets)
    target_rows = {}
    while pending:
        check()
        identity, expected_key = pending.popleft()
        if identity in exports:
            key, uid = exports[identity]
            need(expected_key is None or key == expected_key, "CACHED_EXPORT_NAME")
        else:
            # Refuse before another lookup when its finite byte allowance is gone.
            locator_room = min(O.LOCATOR_MAX,
                               limits.max_binding_bytes - totals["locator_bytes"])
            need(locator_room > 0, "LOCATOR_BYTE_BOUND")
            raw_locator = custody.get_locator(semantic, identity, locator_room,
                                               check_budget=check)
            totals["locator_bytes"] += len(raw_locator)
            locator = PP.read_locator(E.strict_json(raw_locator, PP.DEFAULT_LIMITS.codec))
            key, uid = E.name_key(locator["export_name"]), locator["unit_id"]
            need(locator["semantic_id"] == semantic and
                 S.export_id(semantic, uid, locator["export_name"]) == identity and
                 (expected_key is None or expected_key == key), "LOCATOR_BINDING")
            bind(key, identity)
            if uid not in units:
                room = min(limits.max_unit_bytes, limits.max_bytes-totals["evidence_bytes"])
                nodes = limits.max_nodes-totals["nodes"]
                edges = limits.max_edges-totals["edges"]
                need(totals["units"] < limits.max_units and room > 0 and nodes > 0,
                     "ACQUISITION_BOUND")
                raw = custody.get_evidence(semantic, uid, room, check_budget=check)
                # The existing codec applies reduced byte/node/import ceilings.
                # Zero remaining edges still permits an import-free unit; the
                # exact zero check follows its bounded parse, before another read.
                codec = replace(E.DEFAULT_LIMITS, max_bytes=room,
                    max_unit_nodes=min(E.DEFAULT_LIMITS.max_unit_nodes, nodes),
                    max_imports=max(1, min(E.DEFAULT_LIMITS.max_imports, edges)))
                parsed = PE.read_evidence(raw, codec)
                check()
                need(parsed.unit_id == uid and parsed.document["semantic_id"] == semantic,
                     "UNIT_BINDING")
                imported = tuple((E.name_key(name), symbol)
                                 for name, symbol in parsed.document["imports"])
                need(len(imported) <= edges, "IMPORT_EDGE_BOUND")
                outputs = parsed.document["unit"][2]
                need(key in parsed.census.expected_names, "LOCATOR_OUTPUT_ABSENT")
                for row in outputs:
                    check()
                    out_key = E.name_key(row[0])
                    symbol = S.export_id(semantic, uid, row[0])
                    need(out_key not in basis and out_key not in providers, "DUPLICATE_OUTPUT")
                    bind(out_key, symbol)
                    providers[out_key] = uid
                    need(symbol not in exports, "EXPORT_COLLISION")
                    exports[symbol] = (out_key, uid)
                for name, symbol in imported:
                    bind(name, symbol)
                totals["units"] += 1
                totals["evidence_bytes"] += len(raw)
                totals["nodes"] += parsed.census.total_nodes
                totals["edges"] += len(imported)
                units[uid], imports[uid] = raw, imported
                _write(root / "units" / (uid + ".json"), raw, limits.max_unit_bytes, check)
                if policy == "closed-basis":
                    for name, symbol in imported:
                        check()
                        if name not in basis and symbol not in queued:
                            need(len(queued) < limits.max_targets + limits.max_names,
                                 "LOOKUP_COUNT_BOUND")
                            queued.add(symbol)
                            pending.append((symbol, name))
            need(exports.get(identity) == (key, uid), "WHOLE_GROUP_EXPORT_BINDING")
        if identity in target_set:
            target_rows[identity] = {"name": E.strict_json(key),
                                     "export_id": identity, "unit_id": uid}

    # Dependency edges refer to exact shared name bindings. Kahn's algorithm
    # avoids a Python recursion-depth limit for long, otherwise bounded chains.
    successors = {uid: set() for uid in units}
    indegree, unresolved, fixed = {}, {}, {}
    for uid, rows in imports.items():
        check()
        predecessors = set()
        for name, symbol in rows:
            check()
            if name in providers:
                predecessors.add(providers[name])
            elif name in basis:
                need(basis[name] == symbol, "FIXED_BASIS_BINDING")
                fixed[name] = symbol
            else:
                unresolved[name] = symbol
        indegree[uid] = len(predecessors)
        for predecessor in predecessors:
            successors[predecessor].add(uid)
    need(policy != "closed-basis" or not unresolved, "CLOSURE_UNRESOLVED")
    ready = [uid for uid, count in indegree.items() if not count]
    heapq.heapify(ready)
    ordered = []
    while ready:
        check()
        uid = heapq.heappop(ready)
        ordered.append(uid)
        for successor in successors[uid]:
            check()
            indegree[successor] -= 1
            if not indegree[successor]:
                heapq.heappush(ready, successor)
    need(len(ordered) == len(units), "DEPENDENCY_CYCLE")
    batches = B.split_units([units[uid] for uid in ordered], limits=limits, check_budget=check)
    manifest = B.make_manifest(batches, limits=limits, check_budget=check)
    need(len(target_rows) == len(targets), "TARGET_CENSUS")
    obligations = E.canonical_json({"schema": "DMKN_ORDINARY_RETURN_OBLIGATIONS_V1",
        "assurance": "INERT_CLAIMS_NOT_MATHEMATICAL_ACCEPTANCE", "policy": policy,
        "semantic_id": semantic, "bundle_manifest_sha256": manifest.sha256,
        "targets": [target_rows[identity] for identity in targets],
        "fixed_basis": [[E.strict_json(name), symbol] for name, symbol in sorted(fixed.items())],
        "receiver_parent": [[E.strict_json(name), symbol]
                            for name, symbol in sorted(unresolved.items())],
        "census": totals})
    _write(root / "obligations.json", obligations, limits.max_binding_bytes, check)
    # Existing intake uses exact manifest entries; it does not scan/census the
    # bundle directory. The advisory obligations file is not an admission input.
    _write(root / "manifest.json", manifest.raw, limits.max_manifest_bytes, check)
    return {"status": "INERT_BUNDLE_WRITTEN", "mathematical_acceptance": False,
            "policy": policy, "bundle_directory": str(root),
            "bundle_manifest": str(root / "manifest.json"),
            "bundle_manifest_sha256": manifest.sha256,
            "obligations": str(root / "obligations.json"),
            "obligations_sha256": hashlib.sha256(obligations).hexdigest(),
            "remaining_receiver_imports": len(unresolved), "census": totals}
