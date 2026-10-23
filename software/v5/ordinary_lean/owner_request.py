"""Prepare a bounded ordinary authoring request from protected local warrants.

Internal conditional plumbing, NOT acceptance. `warranted_symbol` must be a
stable lookup in an eligible protected catalog context chosen by the owner.
An arbitrary callback/dictionary cannot provide that precondition. Evidence
retrieval and owner-presence hints may be wrong: exact identity checks and the
Lean helper refuse mismatches; they never issue catalog warrants.

Traversal follows selected semantic dependencies, not every theorem's proof
ancestry. Existing theorem rows contain only types. Missing declarations carry
their actual construction data. Final contributed mathematics still crosses the
independent checked-extension boundary. No source execution or binary loading.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import hashlib
import json

import ordinary_evidence as E

GROUP_FORMAT = "DMKN_OWNER_GROUP_V1"
REQUEST_FORMAT = "DMKN_OWNER_REQUEST_V1"
SEED = "a0acdc706f5e42dca21950c14db2307a18955c63ff953019aaff413d0a976001"
INVENTORY = "c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0"


class RequestError(ValueError):
    pass


def need(ok, code):
    if not ok:
        raise RequestError(code)


@dataclass(frozen=True)
class Limits:
    max_groups: int = 8192
    max_rows: int = 65536
    max_targets: int = 1024
    max_group_bytes: int = 8 * 1024**2
    max_payload_bytes: int = 64 * 1024**2
    max_acquired_bytes: int = 128 * 1024**2
    max_acquired_nodes: int = 20000000
    max_edges: int = 262144

    def __post_init__(self):
        need(all(type(x) is int and 0 < x <= (1 << 32) - 1
                 for x in vars(self).values()), "REQUEST_LIMIT_CONFIGURATION")


@dataclass(frozen=True)
class PreparedRequest:
    """Immutable request bytes; their existence does not establish a warrant."""
    header: bytes
    groups: tuple[bytes, ...]
    evidence_ids: tuple[str, ...]
    acquired_bytes: int
    acquired_nodes: int
    payload_bytes: int
    materialized_units: int


def _semantic_refs(row):
    """References needed for correspondence, omitting opaque theorem values."""
    name, kind, params_raw, packet, details = row
    params = E._names(params_raw, E.DEFAULT_LIMITS.max_params, E.DEFAULT_LIMITS, params=True)
    refs, _ = E._dag_references(packet, params, E.DEFAULT_LIMITS)
    if kind in (1, 3):
        found, _ = E._dag_references(details[0], params, E.DEFAULT_LIMITS)
        refs.update(found)
    elif kind == 4:
        refs.update(E.name_key(n) for n in details[2] + details[3])
    elif kind == 5:
        refs.add(E.name_key(details[0]))
    elif kind == 6:
        refs.update(E.name_key(n) for n in details[0])
        for constructor, _, rhs in details[5]:
            refs.add(E.name_key(constructor))
            found, _ = E._dag_references(rhs, params, E.DEFAULT_LIMITS)
            refs.update(found)
    return refs


def prepare(*, profile_id, context_id, basis_id, inventory_raw, targets,
            warranted_symbol, fetch_evidence, owner_absent, limits=Limits()):
    """Prepare one selected closure via exact point lookups, no global census.

    Callbacks take an original encoded name; fetch_evidence additionally takes
    its exact warranted symbol ID and returns bounded raw inert evidence.
    owner_absent(name) is only a planning hint; actual Lean membership is checked
    again. A partial-group hint refuses. Failed retrievals/bytes need the caller's
    aggregate transport/deadline grant: this function does not govern network IO.

    Current integration retrieves retained full evidence for selected groups.
    It does not promise proof-free network acquisition of every existing theorem
    interface. A future accepted-header store can avoid those local proof reads;
    no private proof ancestry is included in the prepared existing-theorem rows.
    """
    need(type(limits) is Limits, "REQUEST_LIMIT_CONFIGURATION")
    for value in (profile_id, context_id, basis_id):
        E._hex(value)
    expected_basis = E._digest("ordinary-basis-root-v1", [profile_id, SEED, INVENTORY])
    need(basis_id == expected_basis, "REQUEST_FIXED_BASIS_ID")
    need(type(inventory_raw) is bytes and len(inventory_raw) <= 1024**2 and
         hashlib.sha256(inventory_raw).hexdigest() == INVENTORY, "REQUEST_FIXED_INVENTORY")
    # Only the exact fixed owner-selected bytes reach this noncanonical reader.
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
        symbol = E.basis_symbol_id(profile_id, basis_id, name)
        warranted(name, symbol)
        basis[key] = symbol
        projected = row[:4] + [[]] if row[1] == 2 else row
        basis_rows.append([symbol, projected])
    target_keys, target_rows, queue = set(), [], deque()
    E._array(targets, maximum=limits.max_targets)
    need(bool(targets), "REQUEST_TARGETS_EMPTY")
    scheduled = set(basis)

    def schedule(name, symbol):
        key = E.name_key(name)
        warranted(name, symbol)
        if key not in scheduled:
            need(len(scheduled) < limits.max_rows, "REQUEST_SELECTED_NAME_BOUND")
            scheduled.add(key)
            queue.append((name, symbol))

    for target in targets:
        name, symbol = E._array(target, 2)
        key = E.name_key(name)
        need(key not in target_keys, "REQUEST_DUPLICATE_TARGET")
        target_keys.add(key)
        target_rows.append([name, warranted(name, symbol)])
        schedule(name, symbol)

    groups, names_to_unit = {}, {}
    acquired_bytes, acquired_nodes, payload_bytes, rows_count, edge_count = 0, 0, 0, len(basis), 0
    materialized = 0
    while queue:
        wanted_name, wanted_symbol = queue.popleft()
        wanted_key = E.name_key(wanted_name)
        if wanted_key in names_to_unit:
            continue
        need(len(groups) < limits.max_groups, "REQUEST_GROUP_BOUND")
        raw = fetch_evidence(wanted_name, wanted_symbol)
        need(type(raw) is bytes and len(raw) <= E.DEFAULT_LIMITS.max_bytes,
             "REQUEST_EVIDENCE_BYTE_BOUND")
        acquired_bytes += len(raw)
        need(acquired_bytes <= limits.max_acquired_bytes, "REQUEST_ACQUISITION_BOUND")
        evidence = E.read_evidence(raw)
        acquired_nodes += evidence.census.total_nodes
        need(acquired_nodes <= limits.max_acquired_nodes, "REQUEST_ACQUISITION_NODE_BOUND")
        doc, unit_id = evidence.document, evidence.unit_id
        need(doc["profile_id"] == profile_id, "REQUEST_EVIDENCE_PROFILE")
        unit = doc["unit"]
        own = {E.name_key(row[0]): row[0] for row in unit[2]}
        need(wanted_key in own and E.export_id(profile_id, unit_id, wanted_name) == wanted_symbol,
             "REQUEST_EVIDENCE_TARGET_BINDING")
        need(unit_id not in groups and not (set(own) & (set(basis) | set(names_to_unit))),
             "REQUEST_OVERLAPPING_UNIT")
        rows_count += len(own)
        need(rows_count <= limits.max_rows, "REQUEST_ROW_BOUND")
        imports = {E.name_key(name): (name, symbol) for name, symbol in doc["imports"]}
        for name, symbol in imports.values():
            warranted(name, symbol)
        hints = []
        for name in own.values():
            warranted(name, E.export_id(profile_id, unit_id, name))
            hint = owner_absent(name)
            need(type(hint) is bool, "REQUEST_OWNER_HINT_TYPE")
            hints.append(hint)
        need(all(hints) or not any(hints), "REQUEST_PARTIAL_OWNER_GROUP_HINT")
        missing, generated = all(hints), unit[1][0] == 3
        needs_unit = missing or generated
        materialized += int(missing)
        refs, rows = set(), []
        for row in unit[2]:
            name, kind = row[0], row[1]
            symbol = E.export_id(profile_id, unit_id, name)
            rows.append([name, 0 if kind == 2 else 1, symbol,
                         [row[2], row[3]] if kind == 2 else row])
            refs.update(_semantic_refs(row))
        refs.difference_update(own)
        if missing:
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
        # Retain compact prepared packets, not discarded theorem proof graphs.
        del evidence, doc, unit, raw, own, imports, refs, rows, row

    # Dependency-order only the selected group graph; no all-library passes.
    dependencies, dependents = {}, {}
    for unit_id, (_, refs) in groups.items():
        dep = set()
        for key in refs:
            if key not in basis:
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
    header = E.canonical_json({"schema": REQUEST_FORMAT, "profile_id": profile_id,
        "context_id": context_id, "basis_id": basis_id, "basis_rows": basis_rows,
        "targets": target_rows, "group_count": len(ordered)})
    payload_bytes += len(header)
    need(payload_bytes <= limits.max_payload_bytes, "REQUEST_PAYLOAD_BYTE_BOUND")
    return PreparedRequest(header, tuple(groups[unit][0] for unit in ordered),
                           tuple(ordered), acquired_bytes, acquired_nodes,
                           payload_bytes, materialized)
