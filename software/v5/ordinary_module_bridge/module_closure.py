"""Pure selected full-proof closure for an ordinary Lean module builder.

No owner open, filesystem, process, network, native import or acceptance occurs
here. The trusted controller injects its selected admission module and callbacks
over ONE eligible immutable owner context. Custody is not a warrant. All reached
nonbasis declarations retain their complete original portable evidence; theorem
interfaces are never substituted for proofs.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import hashlib
import json

MIB = 1024**2
REQUEST_SCHEMA = "DMKN_ORDINARY_MODULE_REQUEST_V1"


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
class Closure:
    """Immutable inert bytes. Native rechecking/module writing is still required."""
    request: bytes
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

    @property
    def status(self):
        return "READY_FOR_NATIVE_MODULE_RECHECK"

    @property
    def mathematical_acceptance(self):
        return False


def collect_closure(*, admission_api, semantic_id, foundation_id, context_root,
                    inventory_raw, targets, module_name, warranted_symbol,
                    fetch_evidence, check_budget, limits=Limits()):
    """Collect exactly selected proof dependencies above the fixed basis.

    admission_api is the controller's already selected ordinary_admission module
    (A.E/A.S/A.PE and A._plan). It is not loaded from candidate metadata. Callbacks:

    * warranted_symbol(encoded_name) -> exact current SymbolID or None, from the
      caller's one protected context, never from custody or a peer assertion.
    * fetch_evidence(encoded_name, exact_ExportID, maximum_bytes) -> immutable
      complete evidence bytes or None (unavailable). The callback must enforce
      the read/acquisition bound BEFORE allocation, share the caller's original
      I/O/deadline budget, and validate any local/remote locator it follows.
      This function independently validates the resulting actual bytes/IDs.
    * check_budget() -> raises when the original allowance expires.

    Targets are [{name, export_id, unit_id}, ...], with at least one nonbasis
    target. Basis-only use should import approved Init without this bridge.
    No whole-context enumeration occurs. Callback exceptions are propagated;
    absence of authority and unavailable evidence have distinct errors, and
    neither is reported as mathematical invalidity. Failed work is not retried.
    """
    A = admission_api
    E, S, PE = A.E, A.S, A.PE
    need(type(limits) is Limits and all(callable(value) for value in
         (warranted_symbol, fetch_evidence, check_budget, A._plan)), "MODULE_CLOSURE_CONFIGURATION")
    need(S.E is E and PE.E is E and PE.S is S, "MODULE_CLOSURE_SHARED_SEMANTICS")
    check_budget()
    for value in (semantic_id, foundation_id, context_root):
        E._hex(value)
    need(semantic_id == S.semantic_id() and foundation_id == S.foundation_id(),
         "MODULE_CLOSURE_SELECTED_FOUNDATION")
    need(type(inventory_raw) is bytes and len(inventory_raw) <= MIB and
         hashlib.sha256(inventory_raw).hexdigest() == S.INVENTORY, "MODULE_CLOSURE_FIXED_INVENTORY")
    inventory = json.loads(inventory_raw)
    need(type(inventory) is list and len(inventory) == 581, "MODULE_CLOSURE_FIXED_BASIS_CENSUS")
    # A fixed, single-component normal-import name. No paths, private prefixes,
    # user code or aliases are accepted in this native builder field.
    module_key = E.name_key(module_name)
    need(len(module_name) == 1 and module_name[0][0] == 0, "MODULE_CLOSURE_MODULE_NAME")
    module_part = bytes(module_name[0][1]["$bytes"])
    need(len(module_part) == 75 and module_part.startswith(b"DMKNBridge_") and
         all(byte in b"0123456789abcdef" for byte in module_part[11:]), "MODULE_CLOSURE_MODULE_NAME")
    need(type(targets) is list and 1 <= len(targets) <= limits.max_targets,
         "MODULE_CLOSURE_TARGET_COUNT")
    # Freeze caller-owned mutable values before the first external callback.
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
            # Callback receives an independent structured value, never a live
            # unit-document list whose mutation could change the collected proof.
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
    # Keep the exact full inventory, including theorem values and kind-7 rows.
    # This is not portable_owner_request's theorem-signature projection.
    queue, scheduled, expected_units, target_bindings = deque(), {}, {}, []

    def schedule(name, identity):
        key = warranted(name, identity)
        if key in basis:
            need(basis[key] == identity, "MODULE_CLOSURE_CHANGED_BASIS_IMPORT")
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
        need(S.export_id(semantic_id, unit, name) == identity, "MODULE_CLOSURE_TARGET_EXPORT_BINDING")
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
        need(type(raw) is bytes and 0 < len(raw) <= remaining, "MODULE_CLOSURE_EVIDENCE_BYTES")
        acquired_bytes += len(raw)
        item = PE.read_evidence(raw, E.Limits(max_bytes=remaining,
            max_unit_nodes=limits.max_nodes, max_exprs=limits.max_nodes,
            max_levels=limits.max_nodes, max_inventory=limits.max_names, max_imports=limits.max_edges))
        doc, unit = item.document, item.unit_id
        need(doc["semantic_id"] == semantic_id, "MODULE_CLOSURE_EVIDENCE_SEMANTICS")
        own = {E.name_key(row[0]): row[0] for row in doc["unit"][2]}
        need(key in own and S.export_id(semantic_id, unit, E.strict_json(key)) == identity,
             "MODULE_CLOSURE_ACTUAL_TARGET_BINDING")
        need(unit not in units and not set(own).intersection(basis) and
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
        # Traverse ALL direct imports, including proof-only imports. The
        # existing reader has checked their exact ordered name census.
        for import_name, import_id in doc["imports"]:
            schedule(import_name, import_id)

    check_budget()
    # Pure inert structural planning ONLY. The actual eligible owner context
    # warranted every input above; this deliberately restricted dictionary
    # cannot be passed to owner adoption or used as a checking receipt. Normal
    # full-context preflight would mark all units reused and not rebuild them.
    foundation_only_plan_input = {"semantic_id": semantic_id, "local_root": context_root,
                                  "bindings": dict(basis)}
    plan = A._plan(foundation_only_plan_input, tuple(units.values()),
        A.PreflightLimits(max_units=limits.max_units, max_bytes=limits.max_total_bytes,
            max_nodes=limits.max_nodes, max_names=limits.max_names, max_edges=limits.max_edges), check_budget)
    need(plan.status == "READY" and not plan.missing and not plan.reused_unit_ids and
         len(plan.ordered_units) == len(units), "MODULE_CLOSURE_FOUNDATION_ONLY_PLAN")
    # Existing planner supplies collision/group/import checks and deterministic
    # topological order. Do not duplicate its dependency algorithm here.
    raw_to_id = {raw: identity for identity, raw in units.items()}
    ordered_ids = tuple(raw_to_id[raw] for raw in plan.ordered_units)
    ordered_payloads = [json.loads(raw)["unit"] for raw in plan.ordered_units]
    request = E.canonical_json({"schema": REQUEST_SCHEMA, "semantic_id": semantic_id,
        "foundation_id": foundation_id, "context_root": context_root,
        "module_name": module_name, "targets": [row["name"] for row in selected],
        "unit_ids": list(ordered_ids), "units": ordered_payloads})
    need(len(request) <= limits.max_request_bytes, "MODULE_CLOSURE_REQUEST_BYTES")
    check_budget()
    return Closure(request, inventory_raw, tuple(plan.ordered_units), ordered_ids,
        tuple(target_bindings), tuple(sorted(basis.items())), acquired_bytes,
        acquired_nodes, output_names, import_edges, fetch_calls, warrant_lookups)
