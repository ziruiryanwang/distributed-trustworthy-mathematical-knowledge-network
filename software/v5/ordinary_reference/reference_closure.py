"""New proof closure above a protected original library and generated deltas.

Pure preparation, not admission or reference authentication. The caller must
load the reference and generated frontier through the real protected owner.
Old proof bodies are neither fetched nor decoded. Inaccessible original names
cannot be smuggled back as new work; only its warranted public frontier and
closed usable basis may terminate new dependencies.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import hashlib
import json

MIB = 1024**2
REQUEST_SCHEMA = "DMKN_ORDINARY_REFERENCE_MODULE_REQUEST_V1"


class ClosureError(ValueError):
    """Operational preparation refusal, not a mathematical invalidity verdict."""


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
            need(type(value) is int and 1 <= value <= ceiling, "REFERENCE_CLOSURE_LIMIT:"+key)


@dataclass(frozen=True)
class Frontier:
    reference_id: str
    parent_delta_id: str
    original_units: tuple[tuple[str, tuple[tuple[bytes, str], ...]], ...]
    generated_units: tuple[tuple[str, tuple[tuple[bytes, str], ...]], ...]
    usable_basis_keys: tuple[bytes, ...]
    original_warrants: tuple[tuple[bytes, str], ...]


@dataclass(frozen=True)
class Closure:
    request: bytes | None
    inventory: bytes
    ordered_evidence: tuple[bytes, ...]
    ordered_unit_ids: tuple[str, ...]
    target_bindings: tuple[tuple[bytes, str, str], ...]
    acquired_bytes: int
    acquired_nodes: int
    output_names: int
    import_edges: int
    fetch_calls: int
    warrant_lookups: int
    cut_unit_ids: tuple[str, ...]


def collect_closure(*, admission_api, semantic_id, foundation_id, context_root,
                    inventory_raw, targets, module_name, warranted_symbol,
                    fetch_evidence, check_budget, frontier, reference_plan_sha256,
                    limits=Limits()):
    """Collect only new complete units, cutting at exact warranted public units.

    The original frontier has independent library bounds; the 32-unit/4-MiB
    limits apply only to new work. Full fixed-basis warrants are checked, but
    only the reference's closed usable subset authorizes an external name.
    """
    A = admission_api
    E, S, PE = A.E, A.S, A.PE
    need(type(limits) is Limits and type(frontier) is Frontier and
         all(callable(f) for f in (warranted_symbol, fetch_evidence, check_budget, A._plan)) and
         S.E is E and PE.E is E and PE.S is S, "REFERENCE_CLOSURE_CONFIGURATION")
    limits.__post_init__()
    check = check_budget
    check()
    for value in (semantic_id, foundation_id, context_root, frontier.reference_id, reference_plan_sha256):
        E._hex(value)
    need(type(frontier.parent_delta_id) is str, "REFERENCE_CLOSURE_PARENT_ID")
    if frontier.parent_delta_id:
        E._hex(frontier.parent_delta_id)
    need(semantic_id == S.semantic_id() and foundation_id == S.foundation_id(),
         "REFERENCE_CLOSURE_SELECTED_FOUNDATION")
    need(type(inventory_raw) is bytes and len(inventory_raw) <= MIB and
         hashlib.sha256(inventory_raw).hexdigest() == S.INVENTORY,
         "REFERENCE_CLOSURE_FIXED_INVENTORY")
    inventory = json.loads(inventory_raw)
    need(type(inventory) is list and len(inventory) == 581, "REFERENCE_CLOSURE_BASIS_CENSUS")
    module_key = E.name_key(module_name)
    need(len(module_name) == 1 and module_name[0][0] == 0, "REFERENCE_CLOSURE_MODULE_NAME")
    part = bytes(module_name[0][1]["$bytes"])
    need(len(part) == 75 and part.startswith(b"DMKNBridge_") and
         all(n in b"0123456789abcdef" for n in part[11:]), "REFERENCE_CLOSURE_MODULE_NAME")
    need(type(targets) is list and 1 <= len(targets) <= limits.max_targets,
         "REFERENCE_CLOSURE_TARGET_COUNT")
    target_raw = E.canonical_json(targets)
    need(len(target_raw) <= 65536, "REFERENCE_CLOSURE_TARGET_BYTES")
    selected = E.strict_json(target_raw, E.Limits(max_bytes=65536))
    module_name = E.strict_json(module_key)
    warrants, warrant_lookups = {}, 0

    def warranted(name, identity):
        nonlocal warrant_lookups
        check()
        key = E.name_key(name)
        E._hex(identity)
        if key not in warrants:
            actual = warranted_symbol(E.strict_json(key))
            warrant_lookups += 1
            check()
            need(actual is not None, "REFERENCE_CLOSURE_NOT_WARRANTED")
            E._hex(actual)
            warrants[key] = actual
        need(warrants[key] == identity, "REFERENCE_CLOSURE_WARRANT_MISMATCH")
        return key

    all_basis = {}
    for row in inventory:
        E._array(row, 5)
        identity = S.basis_symbol_id(semantic_id, foundation_id, row[0])
        key = warranted(row[0], identity)
        need(key not in all_basis, "REFERENCE_CLOSURE_DUPLICATE_BASIS")
        all_basis[key] = identity
    usable = frontier.usable_basis_keys
    need(type(usable) is tuple and len(usable) <= 581 and len(set(usable)) == len(usable) and
         all(type(key) is bytes and key in all_basis for key in usable),
         "REFERENCE_CLOSURE_USABLE_BASIS")
    basis = {key: all_basis[key] for key in usable}
    need(type(frontier.original_warrants) is tuple and
         581 < len(frontier.original_warrants) <= 262144+581,
         "REFERENCE_CLOSURE_ORIGINAL_WARRANT_CENSUS")
    reserved, reserved_bytes = {}, 0
    for row in frontier.original_warrants:
        check()
        need(type(row) is tuple and len(row) == 2, "REFERENCE_CLOSURE_ORIGINAL_WARRANT")
        key, identity = row
        need(type(key) is bytes and 0 < len(key) <= MIB and key not in reserved,
             "REFERENCE_CLOSURE_ORIGINAL_WARRANT_KEY")
        reserved_bytes += len(key)+128
        need(reserved_bytes <= 32*MIB, "REFERENCE_CLOSURE_ORIGINAL_WARRANT_BYTES")
        name = E.strict_json(key, E.Limits(max_bytes=MIB))
        need(E.name_key(name) == key, "REFERENCE_CLOSURE_ORIGINAL_WARRANT_KEY")
        warranted(name, identity)
        reserved[key] = identity
    need(all(reserved.get(key) == identity for key, identity in all_basis.items()),
         "REFERENCE_CLOSURE_ORIGINAL_BASIS_WARRANTS")

    anchored, anchor_units = {}, set()
    for units, original, max_units, max_names, max_bytes in (
            (frontier.original_units, True, 8192, 262144, 32*MIB),
            (frontier.generated_units, False, 1024, 16384, 4*MIB)):
        need(type(units) is tuple and len(units) <= max_units,
             "REFERENCE_CLOSURE_FRONTIER_UNIT_BOUND")
        names = size = 0
        for entry in units:
            check()
            need(type(entry) is tuple and len(entry) == 2, "REFERENCE_CLOSURE_FRONTIER_UNIT")
            unit, outputs = entry
            E._hex(unit)
            need(unit not in anchor_units and type(outputs) is tuple and 0 < len(outputs) <= max_names,
                 "REFERENCE_CLOSURE_FRONTIER_UNIT")
            anchor_units.add(unit)
            for output in outputs:
                need(type(output) is tuple and len(output) == 2, "REFERENCE_CLOSURE_FRONTIER_OUTPUT")
                key, identity = output
                need(type(key) is bytes and 0 < len(key) <= MIB and key not in all_basis and
                     key not in anchored, "REFERENCE_CLOSURE_FRONTIER_NAME")
                names += 1
                size += len(key)+128
                need(names <= max_names and size <= max_bytes, "REFERENCE_CLOSURE_FRONTIER_BOUND")
                name = E.strict_json(key, E.Limits(max_bytes=MIB))
                need(E.name_key(name) == key and S.export_id(semantic_id, unit, name) == identity,
                     "REFERENCE_CLOSURE_FRONTIER_IDENTITY")
                need((reserved.get(key) == identity) if original else (key not in reserved),
                     "REFERENCE_CLOSURE_FRONTIER_ORIGIN")
                warranted(name, identity)
                anchored[key] = (identity, unit)
    need(bool(frontier.parent_delta_id) == bool(frontier.generated_units),
         "REFERENCE_CLOSURE_GENERATED_PARENT")

    queue, scheduled, expected_units, target_bindings, reached = deque(), {}, {}, [], set()

    def schedule(name, identity):
        key = warranted(name, identity)
        if key in basis:
            need(basis[key] == identity, "REFERENCE_CLOSURE_BASIS_IMPORT")
            return
        if key in anchored:
            expected, unit = anchored[key]
            need(expected == identity and (key not in expected_units or expected_units[key] == unit),
                 "REFERENCE_CLOSURE_FRONTIER_IMPORT")
            reached.add(unit)
            return
        need(key not in reserved, "REFERENCE_CLOSURE_PRIVATE_OR_UNUSABLE_IMPORT")
        if key in scheduled:
            need(scheduled[key] == identity, "REFERENCE_CLOSURE_IMPORT_CONFLICT")
        else:
            need(len(scheduled) < limits.max_names, "REFERENCE_CLOSURE_SCHEDULE_BOUND")
            scheduled[key] = identity
            queue.append((key, identity))

    for row in selected:
        need(type(row) is dict and set(row) == {"name", "export_id", "unit_id"},
             "REFERENCE_CLOSURE_TARGET_FIELDS")
        name, identity, unit = row["name"], row["export_id"], row["unit_id"]
        key = E.name_key(name)
        E._hex(identity); E._hex(unit)
        need(key not in expected_units and key not in all_basis and
             S.export_id(semantic_id, unit, name) == identity, "REFERENCE_CLOSURE_TARGET_BINDING")
        expected_units[key] = unit
        target_bindings.append((key, identity, unit))
        schedule(name, identity)

    units, name_units = {}, {}
    acquired_bytes = acquired_nodes = output_names = import_edges = fetch_calls = 0
    while queue:
        check()
        key, identity = queue.popleft()
        if key in name_units:
            need(key not in expected_units or name_units[key] == expected_units[key],
                 "REFERENCE_CLOSURE_SELECTED_UNIT_CHANGED")
            continue
        need(len(units) < limits.max_units, "REFERENCE_CLOSURE_UNIT_BOUND")
        maximum = min(limits.max_unit_bytes, limits.max_total_bytes-acquired_bytes)
        need(maximum > 0, "REFERENCE_CLOSURE_ACQUISITION_BOUND")
        raw = fetch_evidence(E.strict_json(key), identity, maximum)
        fetch_calls += 1
        check()
        need(type(raw) is bytes and 0 < len(raw) <= maximum, "REFERENCE_CLOSURE_EVIDENCE_BYTES")
        acquired_bytes += len(raw)
        item = PE.read_evidence(raw, E.Limits(max_bytes=maximum, max_unit_nodes=limits.max_nodes,
            max_exprs=limits.max_nodes, max_levels=limits.max_nodes,
            max_inventory=limits.max_names, max_imports=limits.max_edges))
        doc, unit = item.document, item.unit_id
        need(doc["semantic_id"] == semantic_id, "REFERENCE_CLOSURE_EVIDENCE_SEMANTICS")
        own = {E.name_key(row[0]): row[0] for row in doc["unit"][2]}
        need(key in own and S.export_id(semantic_id, unit, E.strict_json(key)) == identity,
             "REFERENCE_CLOSURE_ACTUAL_TARGET_BINDING")
        need(unit not in units and unit not in anchor_units and not set(own).intersection(reserved) and
             not set(own).intersection(anchored) and not set(own).intersection(name_units),
             "REFERENCE_CLOSURE_OVERLAPPING_GROUP")
        acquired_nodes += item.census.total_nodes
        output_names += len(own)
        import_edges += len(doc["imports"])
        need(acquired_nodes <= limits.max_nodes and output_names <= limits.max_names and
             import_edges <= limits.max_edges, "REFERENCE_CLOSURE_AGGREGATE_CENSUS")
        for own_key, own_name in own.items():
            warranted(own_name, S.export_id(semantic_id, unit, own_name))
            need(own_key not in expected_units or expected_units[own_key] == unit,
                 "REFERENCE_CLOSURE_SELECTED_UNIT_CHANGED")
            name_units[own_key] = unit
        units[unit] = raw
        for name, symbol in doc["imports"]:
            schedule(name, symbol)
    check()
    if not units:
        need(bool(reached), "REFERENCE_CLOSURE_EMPTY_WITHOUT_FRONTIER")
        return Closure(None, inventory_raw, (), (), tuple(target_bindings), 0, 0, 0, 0, 0,
                       warrant_lookups, tuple(sorted(reached)))
    bindings = dict(basis)
    bindings.update({key: value[0] for key, value in anchored.items()})
    plan = A._plan({"semantic_id": semantic_id, "local_root": context_root, "bindings": bindings},
        tuple(units.values()), A.PreflightLimits(max_units=limits.max_units, max_bytes=limits.max_total_bytes,
            max_nodes=limits.max_nodes, max_names=limits.max_names, max_edges=limits.max_edges), check)
    need(plan.status == "READY" and not plan.missing and not plan.reused_unit_ids and
         len(plan.ordered_units) == len(units), "REFERENCE_CLOSURE_FRONTIER_ONLY_PLAN")
    raw_to_id = {raw: identity for identity, raw in units.items()}
    ordered_ids = tuple(raw_to_id[raw] for raw in plan.ordered_units)
    request = E.canonical_json({"schema": REQUEST_SCHEMA, "semantic_id": semantic_id,
        "foundation_id": foundation_id, "context_root": context_root, "module_name": module_name,
        "targets": [row["name"] for row in selected], "unit_ids": list(ordered_ids),
        "units": [json.loads(raw)["unit"] for raw in plan.ordered_units],
        "reference_id": frontier.reference_id, "parent_delta_id": frontier.parent_delta_id,
        "reference_plan_sha256": reference_plan_sha256})
    need(len(request) <= limits.max_request_bytes, "REFERENCE_CLOSURE_REQUEST_BYTES")
    check()
    return Closure(request, inventory_raw, tuple(plan.ordered_units), ordered_ids, tuple(target_bindings),
        acquired_bytes, acquired_nodes, output_names, import_edges, fetch_calls, warrant_lookups,
        tuple(sorted(reached)))
