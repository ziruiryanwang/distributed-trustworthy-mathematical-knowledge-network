"""Pure delta closure above a caller-authenticated local whole-unit frontier.

This helper grants no authority and opens no storage. Only the controller's
protected registered module may supply AnchorFrontier; a peer or copied manifest
cannot. Unanchored dependencies retain complete portable evidence and use the
unchanged admission planner. Existing basis/anchor proof terms are not decoded.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import hashlib
import json

MIB = 1024**2
REQUEST_SCHEMA = "DMKN_ORDINARY_MODULE_REQUEST_V2"


class ClosureError(ValueError):
    """Preparation failure, not a mathematical-invalidity verdict."""


def need(condition, code):
    if not condition:
        raise ClosureError(code)


@dataclass(frozen=True)
class Limits:
    max_targets: int = 32
    max_units: int = 32
    max_unit_bytes: int = 4*MIB
    max_total_bytes: int = 4*MIB
    max_request_bytes: int = 4*MIB
    max_nodes: int = 131072
    max_names: int = 4096
    max_edges: int = 32768

    def __post_init__(self):
        for key, ceiling in (("max_targets", 32), ("max_units", 32),
                ("max_unit_bytes", 4*MIB), ("max_total_bytes", 4*MIB),
                ("max_request_bytes", 4*MIB), ("max_nodes", 131072),
                ("max_names", 4096), ("max_edges", 32768)):
            value = getattr(self, key)
            need(type(value) is int and 1 <= value <= ceiling,
                 "MODULE_CLOSURE_LIMIT:"+key)


@dataclass(frozen=True)
class AnchorFrontier:
    """Immutable caller-authenticated whole groups, not a checking receipt."""
    anchor_id: str
    units: tuple[tuple[str, tuple[tuple[bytes, str], ...]], ...]


@dataclass(frozen=True)
class Closure:
    request: bytes | None
    inventory: bytes
    ordered_evidence: tuple[bytes, ...]
    ordered_unit_ids: tuple[str, ...]
    target_bindings: tuple[tuple[bytes, str, str], ...]
    basis_bindings: tuple[tuple[bytes, str], ...]
    acquired_bytes: int
    acquired_nodes: int
    output_names: int
    import_edges: int
    fetch_calls: int
    warrant_lookups: int
    anchor_id: str
    cut_unit_ids: tuple[str, ...]

    @property
    def status(self):
        return ("REUSED_LOCAL_MODULE_ANCHOR" if self.request is None
                else "READY_FOR_NATIVE_MODULE_RECHECK")

    @property
    def mathematical_acceptance(self):
        return False


def collect_closure(*, admission_api, semantic_id, foundation_id, context_root,
                    inventory_raw, targets, module_name, warranted_symbol,
                    fetch_evidence, check_budget, anchor_frontier=AnchorFrontier("", ()),
                    anchor_plan_sha256, limits=Limits()):
    """Collect the new delta; all frontier bindings must still be warranted.

    The API/callbacks are the same trusted local seams as the predecessor. The
    caller authenticates frontier origin/completeness and the exact native plan.
    Every frontier output is independently checked against the selected context
    once, even if traversal does not reach it. No old proof is fetched or decoded.
    The 32-unit / 4-MiB ceilings apply only to acquired unanchored work.
    """
    A = admission_api
    E, S, PE = A.E, A.S, A.PE
    need(type(limits) is Limits and type(anchor_frontier) is AnchorFrontier and
         all(callable(value) for value in (warranted_symbol, fetch_evidence,
              check_budget, A._plan)), "MODULE_CLOSURE_CONFIGURATION")
    need(S.E is E and PE.E is E and PE.S is S, "MODULE_CLOSURE_SHARED_SEMANTICS")
    check_budget()
    for value in (semantic_id, foundation_id, context_root, anchor_plan_sha256):
        E._hex(value)
    need(semantic_id == S.semantic_id() and foundation_id == S.foundation_id(),
         "MODULE_CLOSURE_SELECTED_FOUNDATION")
    need(type(inventory_raw) is bytes and len(inventory_raw) <= MIB and
         hashlib.sha256(inventory_raw).hexdigest() == S.INVENTORY,
         "MODULE_CLOSURE_FIXED_INVENTORY")
    inventory = json.loads(inventory_raw)
    need(type(inventory) is list and len(inventory) == 581,
         "MODULE_CLOSURE_FIXED_BASIS_CENSUS")
    module_key = E.name_key(module_name)
    need(len(module_name) == 1 and module_name[0][0] == 0, "MODULE_CLOSURE_MODULE_NAME")
    module_part = bytes(module_name[0][1]["$bytes"])
    need(len(module_part) == 75 and module_part.startswith(b"DMKNBridge_") and
         all(byte in b"0123456789abcdef" for byte in module_part[11:]),
         "MODULE_CLOSURE_MODULE_NAME")
    need(type(targets) is list and 1 <= len(targets) <= limits.max_targets,
         "MODULE_CLOSURE_TARGET_COUNT")
    target_raw = E.canonical_json(targets)
    need(len(target_raw) <= 65536, "MODULE_CLOSURE_TARGET_BYTES")
    selected = E.strict_json(target_raw, E.Limits(max_bytes=65536))
    module_name = E.strict_json(module_key)
    basis, warrants = {}, {}
    warrant_lookups = 0

    def warranted(name, expected):
        nonlocal warrant_lookups
        check_budget()
        key = E.name_key(name)
        E._hex(expected)
        if key not in warrants:
            actual = warranted_symbol(E.strict_json(key))
            warrant_lookups += 1
            check_budget()
            need(actual is not None, "MODULE_CLOSURE_NOT_WARRANTED")
            E._hex(actual)
            warrants[key] = actual
        need(warrants[key] == expected, "MODULE_CLOSURE_WARRANT_MISMATCH")
        return key

    for row in inventory:
        check_budget()
        E._array(row, 5)
        name = row[0]
        key = E.name_key(name)
        need(key not in basis, "MODULE_CLOSURE_DUPLICATE_BASIS_NAME")
        identity = S.basis_symbol_id(semantic_id, foundation_id, name)
        warranted(name, identity)
        basis[key] = identity

    frontier = anchor_frontier
    need(type(frontier.units) is tuple and len(frontier.units) <= 1024 and
         type(frontier.anchor_id) is str and bool(frontier.anchor_id) == bool(frontier.units),
         "MODULE_CLOSURE_ANCHOR_SHAPE")
    if frontier.anchor_id:
        E._hex(frontier.anchor_id)
    anchored, anchor_units, frontier_bytes = {}, set(), 0
    for entry in frontier.units:
        check_budget()
        need(type(entry) is tuple and len(entry) == 2, "MODULE_CLOSURE_ANCHOR_UNIT")
        unit, outputs = entry
        E._hex(unit)
        need(unit not in anchor_units and type(outputs) is tuple and
             1 <= len(outputs) <= 16384, "MODULE_CLOSURE_ANCHOR_UNIT")
        anchor_units.add(unit)
        for output in outputs:
            need(type(output) is tuple and len(output) == 2, "MODULE_CLOSURE_ANCHOR_OUTPUT")
            key, identity = output
            need(type(key) is bytes and 0 < len(key) <= MIB,
                 "MODULE_CLOSURE_ANCHOR_NAME_BYTES")
            frontier_bytes += len(key)+128
            need(frontier_bytes <= 4*MIB and len(anchored) < 16384,
                 "MODULE_CLOSURE_ANCHOR_BOUND")
            name = E.strict_json(key, E.Limits(max_bytes=MIB))
            need(E.name_key(name) == key and key not in basis and key not in anchored,
                 "MODULE_CLOSURE_ANCHOR_NAME_CONFLICT")
            E._hex(identity)
            need(S.export_id(semantic_id, unit, name) == identity,
                 "MODULE_CLOSURE_ANCHOR_EXPORT_BINDING")
            warranted(name, identity)
            anchored[key] = (identity, unit)

    queue, scheduled, expected_units, target_bindings = deque(), {}, {}, []
    reached = set()

    def schedule(name, identity):
        key = warranted(name, identity)
        if key in basis:
            need(basis[key] == identity, "MODULE_CLOSURE_CHANGED_BASIS_IMPORT")
            return
        if key in anchored:
            expected, unit = anchored[key]
            need(expected == identity, "MODULE_CLOSURE_ANCHOR_IMPORT_CONFLICT")
            need(key not in expected_units or expected_units[key] == unit,
                 "MODULE_CLOSURE_SELECTED_UNIT_CHANGED")
            reached.add(unit)
            return
        if key in scheduled:
            need(scheduled[key] == identity, "MODULE_CLOSURE_IMPORT_ID_CONFLICT")
        else:
            need(len(scheduled) < limits.max_names, "MODULE_CLOSURE_SCHEDULE_BOUND")
            scheduled[key] = identity
            queue.append((key, identity))

    for row in selected:
        need(type(row) is dict and set(row) == {"name", "export_id", "unit_id"},
             "MODULE_CLOSURE_TARGET_FIELDS")
        name, identity, unit = row["name"], row["export_id"], row["unit_id"]
        key = E.name_key(name)
        E._hex(identity); E._hex(unit)
        need(key not in expected_units, "MODULE_CLOSURE_DUPLICATE_TARGET")
        need(key not in basis, "MODULE_CLOSURE_NONBASIS_TARGET_REQUIRED")
        need(S.export_id(semantic_id, unit, name) == identity,
             "MODULE_CLOSURE_TARGET_EXPORT_BINDING")
        expected_units[key] = unit
        target_bindings.append((key, identity, unit))
        schedule(name, identity)

    units, name_units = {}, {}
    acquired_bytes = acquired_nodes = output_names = import_edges = fetch_calls = 0
    while queue:
        check_budget()
        key, identity = queue.popleft()
        if key in name_units:
            need(key not in expected_units or name_units[key] == expected_units[key],
                 "MODULE_CLOSURE_SELECTED_UNIT_CHANGED")
            continue
        need(len(units) < limits.max_units, "MODULE_CLOSURE_UNIT_BOUND")
        remaining = min(limits.max_unit_bytes, limits.max_total_bytes-acquired_bytes)
        need(remaining > 0, "MODULE_CLOSURE_ACQUISITION_BOUND")
        raw = fetch_evidence(E.strict_json(key), identity, remaining)
        fetch_calls += 1
        check_budget()
        need(raw is not None, "MODULE_CLOSURE_EVIDENCE_UNAVAILABLE")
        need(type(raw) is bytes and 0 < len(raw) <= remaining,
             "MODULE_CLOSURE_EVIDENCE_BYTES")
        acquired_bytes += len(raw)
        item = PE.read_evidence(raw, E.Limits(max_bytes=remaining,
            max_unit_nodes=limits.max_nodes, max_exprs=limits.max_nodes,
            max_levels=limits.max_nodes, max_inventory=limits.max_names,
            max_imports=limits.max_edges))
        doc, unit = item.document, item.unit_id
        need(doc["semantic_id"] == semantic_id, "MODULE_CLOSURE_EVIDENCE_SEMANTICS")
        own = {E.name_key(row[0]): row[0] for row in doc["unit"][2]}
        need(key in own and S.export_id(semantic_id, unit, E.strict_json(key)) == identity,
             "MODULE_CLOSURE_ACTUAL_TARGET_BINDING")
        need(unit not in units and unit not in anchor_units and
             not set(own).intersection(basis) and not set(own).intersection(anchored) and
             not set(own).intersection(name_units), "MODULE_CLOSURE_OVERLAPPING_GROUP")
        acquired_nodes += item.census.total_nodes
        output_names += len(own)
        import_edges += len(doc["imports"])
        need(acquired_nodes <= limits.max_nodes and output_names <= limits.max_names and
             import_edges <= limits.max_edges, "MODULE_CLOSURE_AGGREGATE_CENSUS")
        for own_key, own_name in own.items():
            warranted(own_name, S.export_id(semantic_id, unit, own_name))
            need(own_key not in expected_units or expected_units[own_key] == unit,
                 "MODULE_CLOSURE_SELECTED_UNIT_CHANGED")
            name_units[own_key] = unit
        units[unit] = raw
        for import_name, import_id in doc["imports"]:
            schedule(import_name, import_id)

    check_budget()
    if not units:
        need(bool(frontier.anchor_id) and bool(reached), "MODULE_CLOSURE_EMPTY_WITHOUT_ANCHOR")
        return Closure(None, inventory_raw, (), (), tuple(target_bindings),
            tuple(sorted(basis.items())), 0, 0, 0, 0, 0, warrant_lookups,
            frontier.anchor_id, tuple(sorted(reached)))
    # The restricted input prevents the planner from classifying unanchored
    # owner-warranted units as reused. Do not pass the entire owner context.
    bindings = dict(basis)
    bindings.update({key: value[0] for key, value in anchored.items()})
    plan = A._plan({"semantic_id": semantic_id, "local_root": context_root,
        "bindings": bindings}, tuple(units.values()),
        A.PreflightLimits(max_units=limits.max_units, max_bytes=limits.max_total_bytes,
            max_nodes=limits.max_nodes, max_names=limits.max_names,
            max_edges=limits.max_edges), check_budget)
    need(plan.status == "READY" and not plan.missing and not plan.reused_unit_ids and
         len(plan.ordered_units) == len(units), "MODULE_CLOSURE_FRONTIER_ONLY_PLAN")
    raw_to_id = {raw: identity for identity, raw in units.items()}
    ordered_ids = tuple(raw_to_id[raw] for raw in plan.ordered_units)
    request = E.canonical_json({"schema": REQUEST_SCHEMA, "semantic_id": semantic_id,
        "foundation_id": foundation_id, "context_root": context_root,
        "module_name": module_name, "targets": [row["name"] for row in selected],
        "unit_ids": list(ordered_ids), "units": [json.loads(raw)["unit"] for raw in plan.ordered_units],
        "anchor_id": frontier.anchor_id, "anchor_plan_sha256": anchor_plan_sha256})
    need(len(request) <= limits.max_request_bytes, "MODULE_CLOSURE_REQUEST_BYTES")
    check_budget()
    return Closure(request, inventory_raw, tuple(plan.ordered_units), ordered_ids,
        tuple(target_bindings), tuple(sorted(basis.items())), acquired_bytes,
        acquired_nodes, output_names, import_edges, fetch_calls, warrant_lookups,
        frontier.anchor_id, tuple(sorted(reached)))
