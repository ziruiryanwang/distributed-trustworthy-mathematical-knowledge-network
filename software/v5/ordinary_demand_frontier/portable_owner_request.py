"""Portable V2/V3 owner request over an eligible protected local context.

Same selected semantic traversal/group grammar as owner_request; only explicit
S/F/context-root labels and portable evidence/symbol identities differ. Callbacks
are trusted controller operations with one parent IO/deadline budget, not peer
warrants. Scratch authoring and request generation never grant acceptance.
"""
from __future__ import annotations

from collections import deque
import hashlib
import json

import ordinary_evidence as E
import ordinary_semantics as S
import portable_evidence as PE
import owner_request as V1

GROUP_FORMAT = V1.GROUP_FORMAT
REQUEST_FORMAT = "DMKN_OWNER_REQUEST_V2"
FRONTIER_REQUEST_FORMAT = "DMKN_OWNER_REQUEST_V3"
Limits = V1.Limits
PreparedRequest = V1.PreparedRequest
RequestError = V1.RequestError
need = V1.need


def prepare(*, semantic_id, foundation_id, context_root, inventory_raw, targets,
            warranted_symbol, fetch_evidence, owner_absent, limits=Limits(),
            frontier_root=None, frontier_symbol=None):
    """Prepare portable selected groups without changing the raw unit grammar.

    warranted_symbol(name) must lookup the owner's exact active V2 context.
    fetch_evidence(name, ExportID) returns complete retained portable evidence;
    any remote locator/acquisition is bounded separately by that same owner's
    parent grant. owner_absent(name) is only a hint, rechecked by Lean. Names
    claimed present as well as missing must already be warranted at the receiver.
    S/F are semantic descriptors, not implementation IDs or local basis roots.
    An optional frontier is an optimistic same-owner ancestor selected and
    authenticated by the controller. Only reached exact bindings stop traversal;
    native construction must find them in the approved frontend or fail closed.
    They are interpretation labels, never an installed-semantics correspondence.
    """
    need(type(limits) is Limits, "REQUEST_LIMIT_CONFIGURATION")
    frontier_mode = frontier_root is not None or frontier_symbol is not None
    need(not frontier_mode or (type(frontier_root) is str and callable(frontier_symbol)),
         "REQUEST_FRONTIER_CONFIGURATION")
    if frontier_mode:
        E._hex(frontier_root)
        # V3 is the narrow contribution protocol. A caller may lower ceilings,
        # but inherited general-purpose V2 defaults cannot enlarge this lane.
        ceilings = {"max_groups": 32, "max_rows": 4096, "max_targets": 32,
            "max_group_bytes": 1024**2, "max_payload_bytes": 4*1024**2,
            "max_acquired_bytes": 4*1024**2, "max_acquired_nodes": 131072,
            "max_edges": 32768}
        limits = Limits(**{key: min(getattr(limits, key), ceiling)
                           for key, ceiling in ceilings.items()})
    for value in (semantic_id, foundation_id, context_root):
        E._hex(value)
    need(semantic_id == S.semantic_id() and foundation_id == S.foundation_id(),
         "PORTABLE_REQUEST_SEMANTICS_FOUNDATION")
    need(type(inventory_raw) is bytes and len(inventory_raw) <= 1024**2 and
         hashlib.sha256(inventory_raw).hexdigest() == S.INVENTORY, "REQUEST_FIXED_INVENTORY")
    inventory = json.loads(inventory_raw)
    need(type(inventory) is list and len(inventory) == 581, "REQUEST_FIXED_BASIS_CENSUS")

    def warranted(name, expected=None):
        E.name_key(name)
        actual = warranted_symbol(name)
        need(type(actual) is str, "REQUEST_UNWARRANTED_NAME")
        E._hex(actual)
        need(expected is None or actual == expected, "REQUEST_WARRANTED_ID_MISMATCH")
        return actual

    basis, basis_rows = {}, []
    for row in inventory:
        name = row[0]
        key = E.name_key(name)
        need(key not in basis, "REQUEST_DUPLICATE_BASIS_NAME")
        symbol = S.basis_symbol_id(semantic_id, foundation_id, name)
        warranted(name, symbol)
        basis[key] = symbol
        projected = row[:4] + [[]] if row[1] == 2 else row
        basis_rows.append([symbol, projected])
    target_keys, target_rows, queue = set(), [], deque()
    E._array(targets, maximum=limits.max_targets)
    need(bool(targets), "REQUEST_TARGETS_EMPTY")
    scheduled, frontier = set(basis), {}
    rows_count = len(basis)
    if frontier_mode:
        need(rows_count <= limits.max_rows, "REQUEST_ROW_BOUND")

    def schedule(name, symbol):
        nonlocal rows_count
        key = E.name_key(name)
        warranted(name, symbol)
        if key not in scheduled:
            need(len(scheduled) < limits.max_rows, "REQUEST_SELECTED_NAME_BOUND")
            scheduled.add(key)
            if frontier_mode:
                inherited = frontier_symbol(name)
                need(inherited is None or type(inherited) is str, "REQUEST_FRONTIER_SYMBOL_TYPE")
                if inherited is not None:
                    E._hex(inherited)
                    need(inherited == symbol, "REQUEST_FRONTIER_ID_MISMATCH")
                    rows_count += 1
                    need(rows_count <= limits.max_rows, "REQUEST_ROW_BOUND")
                    frontier[key] = inherited
                    return
            queue.append((name, symbol))

    for target in targets:
        name, symbol = E._array(target, 2)
        key = E.name_key(name)
        need(key not in target_keys, "REQUEST_DUPLICATE_TARGET")
        target_keys.add(key)
        target_rows.append([name, warranted(name, symbol)])
        schedule(name, symbol)

    groups, names_to_unit = {}, {}
    acquired_bytes, acquired_nodes, payload_bytes, edge_count = 0, 0, 0, 0
    materialized = 0
    while queue:
        wanted_name, wanted_symbol = queue.popleft()
        wanted_key = E.name_key(wanted_name)
        if wanted_key in names_to_unit:
            continue
        need(len(groups) < limits.max_groups, "REQUEST_GROUP_BOUND")
        raw = fetch_evidence(wanted_name, wanted_symbol)
        need(type(raw) is bytes and len(raw) <= PE.DEFAULT_LIMITS.max_bytes, "REQUEST_EVIDENCE_BYTE_BOUND")
        acquired_bytes += len(raw)
        need(acquired_bytes <= limits.max_acquired_bytes, "REQUEST_ACQUISITION_BOUND")
        evidence = PE.read_evidence(raw)
        acquired_nodes += evidence.census.total_nodes
        need(acquired_nodes <= limits.max_acquired_nodes, "REQUEST_ACQUISITION_NODE_BOUND")
        doc, unit_id = evidence.document, evidence.unit_id
        need(doc["semantic_id"] == semantic_id, "PORTABLE_REQUEST_EVIDENCE_SEMANTICS")
        unit = doc["unit"]
        own = {E.name_key(row[0]): row[0] for row in unit[2]}
        need(wanted_key in own and S.export_id(semantic_id, unit_id, wanted_name) == wanted_symbol,
             "REQUEST_EVIDENCE_TARGET_BINDING")
        need(unit_id not in groups and not (set(own) & (set(basis) | set(names_to_unit) | set(frontier))),
             "REQUEST_OVERLAPPING_UNIT")
        rows_count += len(own)
        need(rows_count <= limits.max_rows, "REQUEST_ROW_BOUND")
        imports = {E.name_key(name): (name, symbol) for name, symbol in doc["imports"]}
        for name, symbol in imports.values():
            warranted(name, symbol)
        hints = []
        for name in own.values():
            warranted(name, S.export_id(semantic_id, unit_id, name))
            hint = owner_absent(name)
            need(type(hint) is bool, "REQUEST_OWNER_HINT_TYPE")
            hints.append(hint)
        need(all(hints) or not any(hints), "REQUEST_PARTIAL_OWNER_GROUP_HINT")
        missing, generated = all(hints), unit[1][0] == 3
        # The unchanged native mode-0 path constructs only an accepted theorem's
        # signature. Its old proof and proof-only dependencies are unnecessary
        # even when the local authoring environment lacks this theorem name.
        signature_only = len(own) == 1 and unit[2][0][1] == 2
        needs_unit = generated or (missing and not signature_only)
        materialized += int(missing)
        refs, rows = set(), []
        for row in unit[2]:
            name, kind = row[0], row[1]
            symbol = S.export_id(semantic_id, unit_id, name)
            rows.append([name, 0 if kind == 2 else 1, symbol,
                         [row[2], row[3]] if kind == 2 else row])
            refs.update(V1._semantic_refs(row))
        refs.difference_update(own)
        if missing and not signature_only:
            refs.update(evidence.census.external_names)
        need(refs <= set(imports), "REQUEST_SEMANTIC_REFERENCE_WITHOUT_EXACT_IMPORT")
        edge_count += len(refs)
        need(edge_count <= limits.max_edges, "REQUEST_EDGE_BOUND")
        packet = E.canonical_json([GROUP_FORMAT, rows, [unit] if needs_unit else []])
        need(len(packet) <= limits.max_group_bytes, "REQUEST_GROUP_BYTE_BOUND")
        payload_bytes += len(packet)
        need(payload_bytes <= limits.max_payload_bytes, "REQUEST_PAYLOAD_BYTE_BOUND")
        groups[unit_id] = (packet, tuple(sorted(refs)))
        for key in own:
            names_to_unit[key] = unit_id
        for key in sorted(refs):
            schedule(*imports[key])
        del evidence, doc, unit, raw, own, imports, refs, rows, row

    dependencies, dependents = {}, {}
    for unit_id, (_, refs) in groups.items():
        dep = set()
        for key in refs:
            if key not in basis and key not in frontier:
                need(key in names_to_unit, "REQUEST_UNCLOSED_DEPENDENCY")
                dep.add(names_to_unit[key])
        need(unit_id not in dep, "REQUEST_SELF_DEPENDENCY")
        dependencies[unit_id] = len(dep)
        for parent in dep:
            dependents.setdefault(parent, []).append(unit_id)
    ready = deque(sorted(unit for unit, count in dependencies.items() if count == 0))
    ordered = []
    while ready:
        unit = ready.popleft()
        ordered.append(unit)
        for child in sorted(dependents.get(unit, [])):
            dependencies[child] -= 1
            if dependencies[child] == 0:
                ready.append(child)
    need(len(ordered) == len(groups), "REQUEST_CYCLIC_SEMANTIC_CLOSURE")
    header_document = {"schema": REQUEST_FORMAT, "semantic_id": semantic_id,
        "foundation_id": foundation_id, "context_root": context_root, "basis_rows": basis_rows,
        "targets": target_rows, "group_count": len(ordered)}
    if frontier_mode:
        # Stable structured-name order, with no names from unvisited ancestors.
        need(not (set(frontier) & (set(basis) | set(names_to_unit))), "REQUEST_FRONTIER_OUTPUT_OVERLAP")
        header_document.update(schema=FRONTIER_REQUEST_FORMAT, frontier_root=frontier_root,
            frontier_labels=[[E.strict_json(key), frontier[key]] for key in sorted(frontier)])
    header = E.canonical_json(header_document)
    # Match the unchanged bounded Lean header reader before any native work.
    need(len(header) <= 1024**2, "PORTABLE_REQUEST_HEADER_BYTE_BOUND")
    payload_bytes += len(header)
    need(payload_bytes <= limits.max_payload_bytes, "REQUEST_PAYLOAD_BYTE_BOUND")
    return PreparedRequest(header, tuple(groups[unit][0] for unit in ordered),
                           tuple(ordered), acquired_bytes, acquired_nodes,
                           payload_bytes, materialized)
