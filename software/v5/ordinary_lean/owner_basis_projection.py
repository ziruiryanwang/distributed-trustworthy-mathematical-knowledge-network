"""Pure selected-basis projection for authenticated ordinary owner requests.

Not receiver acceptance or a new basis/profile. The controller authenticates
the original complete prepared request and exact fixed inventory first. This
helper changes only header basis_rows; every group byte and all identities stay
unchanged. Needed transparent semantics remain exact. No IO or source execution.
"""
from collections import deque
from dataclasses import dataclass
import hashlib
import json

import ordinary_evidence as E
import owner_request as R


class ProjectionError(ValueError):
    pass


def need(ok, reason):
    if not ok:
        raise ProjectionError(reason)


@dataclass(frozen=True)
class Projected:
    header: bytes
    # Exact E.name_key bytes, not lossy dotted display names.
    selected_basis_names: tuple[bytes, ...]
    omitted_basis_names: tuple[bytes, ...]
    # Non-generated optional units: generated units can be present OR missing,
    # so no claim about their actual owner membership is inferred here.
    materialized_units: int
    generated_units: int
    scanned_nodes: int
    payload_bytes: int


def _key(*parts):
    return E.name_key([[0, {"$bytes": list(part.encode("utf-8"))}] for part in parts])


_NAT_ROOTS = frozenset(_key(*parts) for parts in
                      (("Nat",), ("Nat", "zero"), ("Nat", "succ")))
_STRING_ROOTS = _NAT_ROOTS | frozenset(_key(*parts) for parts in
    (("String",), ("String", "ofList"), ("Char",), ("Char", "ofNat"),
     ("List", "nil"), ("List", "cons")))


class _Scan:
    """One request-wide syntax-work bound, never reset per group or basis row."""

    def __init__(self):
        self.nodes = 0
        self.edges = 0

    def charge(self, count):
        self.nodes += count
        need(self.nodes <= 20000000, "PROJECTION_NODE_BOUND")

    def found(self, refs):
        self.edges += len(refs)
        need(self.edges <= 262144, "PROJECTION_EDGE_BOUND")
        return refs

    def literals(self, nodes):
        refs = set()
        # Shape validation is performed by the ordinary DAG validator, or the
        # exact fixed-inventory digest in the legacy case, before this scan.
        self.charge(len(nodes))
        for node in nodes:
            if node[0] == 7:
                refs.update(_NAT_ROOTS)
            elif node[0] == 9:
                refs.update(_STRING_ROOTS)
        return refs

    def ordinary_dag(self, packet, params):
        refs, count = E._dag_references(packet, params, E.DEFAULT_LIMITS)
        self.charge(count)
        refs.update(self.literals(packet[2]))
        return refs

    def ordinary_row(self, row):
        own, kind, params_raw, packet, details = E._array(row, 5)
        E.name_key(own)
        E._uint(kind, 6)
        need(kind in (1, 3, 4, 5, 6), "PROJECTION_EXACT_ROW_KIND")
        E._array(details, {1: 3, 3: 3, 4: 8, 5: 5, 6: 8}[kind])
        params = E._names(params_raw, E.DEFAULT_LIMITS.max_params,
                          E.DEFAULT_LIMITS, params=True)
        refs = self.ordinary_dag(packet, params)
        if kind in (1, 3):
            refs.update(self.ordinary_dag(details[0], params))
        elif kind == 4:
            refs.update(E.name_key(n) for n in details[2] + details[3])
        elif kind == 5:
            refs.add(E.name_key(details[0]))
        else:
            refs.update(E.name_key(n) for n in details[0])
            for constructor, _, rhs in details[5]:
                refs.add(E.name_key(constructor))
                refs.update(self.ordinary_dag(rhs, params))
        return self.found(refs)

    def legacy_dag(self, packet):
        # This representation is used ONLY after exact fixed-inventory pinning.
        levels, nodes, _ = packet
        self.charge(len(levels) + len(nodes))
        refs = self.literals(nodes)
        for node in nodes:
            if node[0] in (2, 8):
                local = node[1]
                need(len(local) == 2 and local[0] == 6, "PROJECTION_LEGACY_LOCAL_REF")
                refs.add(E.name_key(local[1]))
        return refs

    def basis_row(self, row):
        _, kind, _, packet, details = row
        refs = self.legacy_dag(packet)
        if kind in (1, 3):
            refs.update(self.legacy_dag(details[0]))
        elif kind == 4:
            refs.update(E.name_key(n) for n in details[2] + details[3])
        elif kind == 5:
            refs.add(E.name_key(details[0]))
        elif kind == 6:
            refs.update(E.name_key(n) for n in details[0])
            for constructor, _, rhs in details[5]:
                refs.add(E.name_key(constructor))
                refs.update(self.legacy_dag(rhs))
        # Theorem kind2: type only. Fixed axiom/quotient kinds0/7: type and
        # pinned metadata, neither has an executable body to traverse.
        return self.found(refs)

    def construction(self, unit):
        census = E.inspect_unit(unit)
        self.charge(census.total_nodes)
        refs = set(census.external_names)
        descriptor, inventory = unit[1], unit[2]
        # inspect_unit includes all explicit references, but implicit literal
        # support deliberately remains a parent-profile duty in that validator.
        dags = []
        if descriptor[0] < 3:
            dags.extend((descriptor[3], descriptor[4]))
        else:
            need(all(row[1] in (4, 5, 6) for row in inventory),
                 "PROJECTION_GENERATED_RECORD_KIND")
            for _, type_dag, constructors in descriptor[3]:
                dags.append(type_dag)
                dags.extend(packet for _, packet in constructors)
        for _, kind, _, type_dag, details in inventory:
            dags.append(type_dag)
            if kind in (1, 2, 3):
                dags.append(details[0])
            elif kind == 6:
                dags.extend(rhs for _, _, rhs in details[5])
        for packet in dags:
            refs.update(self.literals(packet[2]))
        return self.found(refs), census.expected_names


def project(header_raw: bytes, groups: tuple[bytes, ...], *, inventory_raw: bytes) -> Projected:
    """Select exactly the reachable fixed-basis semantic closure.

    Inputs are the immutable original complete request, not peer-selected
    warrants. Already prepared groups are not regenerated. `inventory_raw` is
    the small fixed seed-inventory-json.json, not an evidence-directory scan.
    Returned names retain original inventory order. No omitted name is treated
    as an authoring boundary merely because the full basis ID remains present.
    """
    need(type(header_raw) is bytes and 0 < len(header_raw) <= 1048576,
         "PROJECTION_HEADER_BOUND")
    need(type(groups) is tuple and len(groups) <= 8192, "PROJECTION_GROUP_BOUND")
    need(all(type(raw) is bytes and 0 < len(raw) <= 8388608 for raw in groups),
         "PROJECTION_GROUP_BYTES")
    need(len(header_raw) + sum(map(len, groups)) <= 67108864, "PROJECTION_PAYLOAD_BOUND")
    need(type(inventory_raw) is bytes and len(inventory_raw) <= 1048576 and
         hashlib.sha256(inventory_raw).hexdigest() == R.INVENTORY,
         "PROJECTION_FIXED_INVENTORY")
    inventory = json.loads(inventory_raw)
    need(type(inventory) is list and len(inventory) == 581, "PROJECTION_FIXED_CENSUS")
    header = E.strict_json(header_raw)
    need(type(header) is dict and set(header) == {"schema", "profile_id", "context_id",
         "basis_id", "basis_rows", "targets", "group_count"}, "PROJECTION_HEADER_FIELDS")
    need(header["schema"] == R.REQUEST_FORMAT, "PROJECTION_HEADER_SCHEMA")
    profile, context, basis = (E._hex(header[key]) for key in
                               ("profile_id", "context_id", "basis_id"))
    need(basis == E._digest("ordinary-basis-root-v1", [profile, R.SEED, R.INVENTORY]),
         "PROJECTION_BASIS_ID")
    need(type(header["group_count"]) is int and header["group_count"] == len(groups),
         "PROJECTION_GROUP_CENSUS")
    fixed = {}
    expected_rows = []
    for row in inventory:
        key = E.name_key(row[0])
        need(key not in fixed, "PROJECTION_DUPLICATE_FIXED_NAME")
        projected = row[:4] + [[]] if row[1] == 2 else row
        entry = [E.basis_symbol_id(profile, basis, row[0]), projected]
        expected_rows.append(entry)
        fixed[key] = entry
    need(header["basis_rows"] == expected_rows, "PROJECTION_ORIGINAL_FULL_BASIS_REQUIRED")
    targets = E._array(header["targets"], maximum=1024)
    need(bool(targets), "PROJECTION_TARGETS_EMPTY")
    scan, needed, selected_rows = _Scan(), set(), {}
    materialized, generated, row_count = 0, 0, len(fixed)
    for raw in groups:
        marker, rows, optional = E._array(E.strict_json(raw), 3)
        need(marker == R.GROUP_FORMAT, "PROJECTION_GROUP_FORMAT")
        E._array(rows, maximum=65536)
        E._array(optional, maximum=1)
        need(bool(rows), "PROJECTION_GROUP_EMPTY")
        row_count += len(rows)
        need(row_count <= 65536, "PROJECTION_ROW_BOUND")
        group_names = set()
        for raw_row in rows:
            name, mode, symbol, payload = E._array(raw_row, 4)
            key = E.name_key(name)
            E._hex(symbol)
            need(key not in fixed and key not in selected_rows and key not in group_names,
                 "PROJECTION_OVERLAPPING_NAME")
            group_names.add(key)
            selected_rows[key] = symbol
            E._uint(mode, 1)
            if mode == 0:
                params_raw, packet = E._array(payload, 2)
                params = E._names(params_raw, E.DEFAULT_LIMITS.max_params,
                                  E.DEFAULT_LIMITS, params=True)
                needed.update(scan.found(scan.ordinary_dag(packet, params)))
            else:
                need(E.name_key(E._array(payload, 5)[0]) == key, "PROJECTION_ROW_NAME")
                needed.update(scan.ordinary_row(payload))
        if optional:
            refs, names = scan.construction(optional[0])
            need(set(names) == group_names, "PROJECTION_UNIT_GROUP_CENSUS")
            needed.update(refs)
            if optional[0][1][0] == 3:
                generated += 1
            else:
                materialized += 1
    target_keys = set()
    for target in targets:
        name, symbol = E._array(target, 2)
        key = E.name_key(name)
        E._hex(symbol)
        need(key not in target_keys, "PROJECTION_DUPLICATE_TARGET")
        target_keys.add(key)
        expected = fixed[key][0] if key in fixed else selected_rows.get(key)
        need(expected == symbol, "PROJECTION_TARGET_BINDING")
        if key in fixed:
            needed.add(key)
    need(needed <= set(fixed) | set(selected_rows), "PROJECTION_UNBOUND_GROUP_REFERENCE")
    queue, retained = deque(sorted(needed & set(fixed))), set()
    while queue:
        key = queue.popleft()
        if key in retained:
            continue
        retained.add(key)
        refs = scan.basis_row(fixed[key][1])
        need(refs <= set(fixed), "PROJECTION_UNCLOSED_FIXED_BASIS")
        queue.extend(sorted(refs - retained))
    # The unchanged Lean command currently requires at least one basis row.
    # Refuse an empty closure instead of inventing an unrelated root.
    need(bool(retained), "PROJECTION_EMPTY_BASIS_UNSUPPORTED")
    selected = tuple(key for key in fixed if key in retained)
    omitted = tuple(key for key in fixed if key not in retained)
    changed = dict(header)
    changed["basis_rows"] = [fixed[key] for key in selected]
    result = E.canonical_json(changed)
    need(len(result) <= 1048576, "PROJECTION_RESULT_HEADER_BOUND")
    return Projected(result, selected, omitted, materialized, generated,
                     scan.nodes, len(result) + sum(map(len, groups)))
