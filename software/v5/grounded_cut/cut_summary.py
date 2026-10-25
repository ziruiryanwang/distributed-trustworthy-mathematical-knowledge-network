"""Inert exact projections and bounded selected closure, never local warrants.

Controllers ground stored summaries in earlier checked events, bind a stable
eligible root/epoch, and supervise callbacks. No database or native I/O here.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import hashlib

import ordinary_evidence as E
import ordinary_semantics as S
import portable_evidence as PE


SCHEMA = "DMKN_GROUNDED_CUT_SUMMARY_V1"
_DOMAIN = b"DMKN-GROUNDED-CUT-SUMMARY-V1\0"


class SummaryError(ValueError):
    pass


def need(ok, code):
    if not ok:
        raise SummaryError(code)


@dataclass(frozen=True)
class Limits:
    syntax: E.Limits = E.DEFAULT_LIMITS
    max_summary_bytes: int = 8 * 1024**2
    max_groups: int = 1024
    max_names: int = 65536
    max_lookups: int = 65536
    max_edges: int = 262144
    max_acquired_bytes: int = 64 * 1024**2
    max_nodes: int = 20000000
    max_payload_bytes: int = 64 * 1024**2

    def __post_init__(self):
        need(type(self.syntax) is E.Limits, "CUT_SUMMARY_SYNTAX_LIMITS")
        for key, value in vars(self).items():
            if key != "syntax":
                need(type(value) is int and 1 <= value <= (1 << 32) - 1,
                     "CUT_SUMMARY_LIMIT_CONFIGURATION")
        need(self.max_summary_bytes <= self.syntax.max_bytes,
             "CUT_SUMMARY_JSON_BYTE_LIMIT")


@dataclass(frozen=True)
class Projected:
    raw: bytes
    summary_id: str
    semantic_id: str
    unit_id: str
    kind: str
    bindings: tuple[tuple[bytes, str], ...]


@dataclass(frozen=True)
class Stats:
    input_bytes: int
    acquired_bytes: int
    acquired_summaries: int
    demanded_names: int
    lookup_calls: int
    edges: int
    encoded_nodes: int
    payload_bytes: int


@dataclass(frozen=True)
class Prepared:
    concrete_units: tuple[bytes, ...]
    signature_rows: tuple[bytes, ...]
    new_unit: bytes
    new_summary: Projected
    frontier: tuple[tuple[bytes, str, str], ...]
    absent_names: tuple[bytes, ...]
    stats: Stats


def _limits(limits):
    need(type(limits) is Limits, "CUT_SUMMARY_LIMIT_CONFIGURATION")


def _pairs(rows, limits, maximum):
    result = {}
    for row in E._array(rows, maximum=maximum):
        name, symbol = E._array(row, 2)
        key = E.name_key(name, limits.syntax)
        E._hex(symbol)
        need(key not in result, "CUT_SUMMARY_DUPLICATE_NAME")
        result[key] = (name, symbol)
    need(list(result) == sorted(result), "CUT_SUMMARY_NAME_ORDER")
    return result


def _theorem(unit):
    descriptor, inventory = unit[1], unit[2]
    need(descriptor[0] == 1 and len(inventory) == 1 and inventory[0][1] == 2,
         "CUT_SUMMARY_SINGLE_THEOREM")
    row = inventory[0]
    need(descriptor[1:5] == [row[0], row[2], row[3], row[4][0]] and
         descriptor[5] == row[4][1], "CUT_SUMMARY_THEOREM_INVENTORY")
    return row


def _concrete(unit):
    need(unit[1][0] in (0, 2, 3) and all(row[1] != 2 for row in unit[2]),
         "CUT_SUMMARY_CONCRETE_KIND")


def _projected(raw, doc, bindings):
    return Projected(raw, hashlib.sha256(_DOMAIN + raw).hexdigest(),
                     doc["semantic_id"], doc["unit_id"], doc["kind"],
                     tuple((key, pair[1]) for key, pair in bindings.items()))


def _project(evidence, limits):
    doc, unit = evidence.document, evidence.document["unit"]
    semantic, unit_id = doc["semantic_id"], evidence.unit_id
    by_name = {E.name_key(row[0], limits.syntax): row[0] for row in unit[2]}
    bindings = {key: (by_name[key], S.export_id(semantic, unit_id, by_name[key], limits.syntax))
                for key in sorted(by_name)}
    imports = {E.name_key(name, limits.syntax): (name, symbol)
               for name, symbol in doc["imports"]}
    if unit[1][0] == 1:
        row = _theorem(unit)
        params = E._names(row[2], limits.syntax.max_params, limits.syntax, params=True)
        refs, _ = E._dag_references(row[3], params, limits.syntax)
        need(not (refs & set(bindings)), "CUT_SUMMARY_SELF_TYPE_REFERENCE")
        need(refs <= set(imports), "CUT_SUMMARY_TYPE_IMPORT_MISSING")
        selected_imports = [list(imports[key]) for key in sorted(refs)]
        kind, payload = "theorem", [row[2], row[3]]
    else:
        _concrete(unit)
        kind, payload, selected_imports = "concrete", unit, doc["imports"]
    summary = {"schema": SCHEMA, "semantic_id": semantic, "unit_id": unit_id,
               "kind": kind, "bindings": [list(pair) for pair in bindings.values()],
               "imports": selected_imports, "payload": payload}
    raw = E.canonical_json(summary)
    need(len(raw) <= limits.max_summary_bytes, "CUT_SUMMARY_BYTE_BOUND")
    return _projected(raw, summary, bindings)


def project(raw_v2, *, limits=Limits()):
    """Project a bounded V2 claim, not a warrant or authorization to store it."""
    _limits(limits)
    return _project(PE.read_evidence(raw_v2, limits.syntax), limits)


def _read(raw, expected_id, limits):
    need(type(raw) is bytes and 0 < len(raw) <= limits.max_summary_bytes,
         "CUT_SUMMARY_BYTE_BOUND")
    if expected_id is not None:
        need(hashlib.sha256(_DOMAIN + raw).hexdigest() == E._hex(expected_id),
             "CUT_SUMMARY_HASH")
    doc = E.strict_json(raw, limits.syntax)
    need(type(doc) is dict and set(doc) == {
        "schema", "semantic_id", "unit_id", "kind", "bindings", "imports", "payload"},
        "CUT_SUMMARY_FIELDS")
    need(doc["schema"] == SCHEMA, "CUT_SUMMARY_SCHEMA")
    semantic, unit_id = E._hex(doc["semantic_id"]), E._hex(doc["unit_id"])
    bindings = _pairs(doc["bindings"], limits, limits.syntax.max_inventory)
    imports = _pairs(doc["imports"], limits, limits.syntax.max_imports)
    need(bool(bindings) and not (set(bindings) & set(imports)), "CUT_SUMMARY_NAME_OVERLAP")
    for name, symbol in bindings.values():
        need(S.export_id(semantic, unit_id, name, limits.syntax) == symbol,
             "CUT_SUMMARY_EXPORT_BINDING")
    if doc["kind"] == "theorem":
        need(len(bindings) == 1, "CUT_SUMMARY_SINGLE_SIGNATURE")
        params_raw, packet = E._array(doc["payload"], 2)
        params = E._names(params_raw, limits.syntax.max_params, limits.syntax, params=True)
        refs, nodes = E._dag_references(packet, params, limits.syntax)
        need(tuple(sorted(refs)) == tuple(imports), "CUT_SUMMARY_TYPE_IMPORT_CENSUS")
    else:
        need(doc["kind"] == "concrete", "CUT_SUMMARY_KIND")
        original = E.canonical_json({"schema": PE.SCHEMA, "semantic_id": semantic,
                                     "imports": doc["imports"], "unit": doc["payload"]})
        evidence = PE.read_evidence(original, limits.syntax)
        _concrete(evidence.document["unit"])
        need(evidence.unit_id == unit_id and evidence.census.expected_names == tuple(bindings),
             "CUT_SUMMARY_CONCRETE_ID_CENSUS")
        nodes = evidence.census.total_nodes
    return _projected(raw, doc, bindings), doc, nodes


def read(raw_summary, *, expected_id=None, limits=Limits()):
    """Validate canonical syntax/census/identity, never establish grounding."""
    _limits(limits)
    return _read(raw_summary, expected_id, limits)[0]


def prepare(raw_new, *, semantic_id, basis, lookup, read_summary, check, limits=Limits()):
    """Prepare one new theorem over controller-bound, stable eligible summaries.

    lookup(encoded_name) -> (symbol_id, summary_id) | None.
    read_summary(summary_id) -> bytes, already I/O-bounded by the controller.
    check() charges/checks the shared outer deadline/resource grant. Callbacks
    must not fetch arbitrary ancestry or infer warrants from their own inputs.
    """
    _limits(limits)
    need(E._hex(semantic_id) == S.semantic_id(), "CUT_SUMMARY_UNSUPPORTED_SEMANTICS")
    need(type(basis) is dict and len(basis) == 581, "CUT_SUMMARY_FIXED_BASIS_PRECONDITION")
    need(all(callable(fn) for fn in (lookup, read_summary, check)), "CUT_SUMMARY_CALLBACKS")
    check()
    evidence = PE.read_evidence(raw_new, limits.syntax)
    need(evidence.document["semantic_id"] == semantic_id, "CUT_SUMMARY_NEW_SEMANTICS")
    _theorem(evidence.document["unit"])
    projected = _project(evidence, limits)
    new_keys = tuple(key for key, _ in projected.bindings)
    resolved, basis_seen, groups, names_to_summary, units = {}, set(), {}, {}, {}
    pending, scheduled = deque(), set()
    acquired_bytes, nodes, edges, lookup_calls = 0, evidence.census.total_nodes, 0, 0
    need(nodes <= limits.max_nodes, "CUT_SUMMARY_NODE_BOUND")

    def resolve(name):
        nonlocal lookup_calls
        key = E.name_key(name, limits.syntax)
        if key in basis:
            basis_seen.add(key)
            need(len(basis_seen) + len(resolved) <= limits.max_names, "CUT_SUMMARY_NAME_BOUND")
            return key, (E._hex(basis[key]), None)
        if key not in resolved:
            need(len(basis_seen) + len(resolved) < limits.max_names, "CUT_SUMMARY_NAME_BOUND")
            need(lookup_calls < limits.max_lookups, "CUT_SUMMARY_LOOKUP_BOUND")
            lookup_calls += 1
            check()
            result = lookup(name)
            check()
            if result is not None:
                need(type(result) in (tuple, list) and len(result) == 2,
                     "CUT_SUMMARY_LOOKUP_SHAPE")
                result = (E._hex(result[0]), E._hex(result[1]))
            resolved[key] = result
        return key, resolved[key]

    def schedule(name, symbol):
        key, actual = resolve(name)
        need(actual is not None and actual[0] == symbol, "CUT_SUMMARY_UNGROUNDED_IMPORT")
        if actual[1] is not None and actual[1] not in scheduled:
            need(len(scheduled) < limits.max_groups, "CUT_SUMMARY_GROUP_BOUND")
            scheduled.add(actual[1])
            pending.append((name, symbol, actual[1]))
        return key

    new_name = evidence.document["unit"][2][0][0]
    key, existing = resolve(new_name)
    need(key not in basis and existing is None, "CUT_SUMMARY_NEW_NAME_NOT_FRESH")
    edges += len(evidence.document["imports"])
    need(edges <= limits.max_edges, "CUT_SUMMARY_EDGE_BOUND")
    for name, symbol in evidence.document["imports"]:
        schedule(name, symbol)

    while pending:
        check()
        wanted_name, wanted_symbol, digest = pending.popleft()
        raw = read_summary(digest)
        check()
        need(type(raw) is bytes and 0 < len(raw) <= limits.max_summary_bytes,
             "CUT_SUMMARY_BYTE_BOUND")
        acquired_bytes += len(raw)
        need(acquired_bytes <= limits.max_acquired_bytes, "CUT_SUMMARY_ACQUISITION_BOUND")
        selected, doc, count = _read(raw, digest, limits)
        nodes += count
        need(nodes <= limits.max_nodes, "CUT_SUMMARY_NODE_BOUND")
        need(selected.semantic_id == semantic_id, "CUT_SUMMARY_OLD_SEMANTICS")
        wanted_key = E.name_key(wanted_name, limits.syntax)
        own = dict(selected.bindings)
        need(own.get(wanted_key) == wanted_symbol, "CUT_SUMMARY_DEMANDED_BINDING")
        need(selected.unit_id not in units, "CUT_SUMMARY_UNIT_ALIAS")
        units[selected.unit_id] = digest
        for name, symbol in doc["bindings"]:
            own_key, actual = resolve(name)
            need(own_key not in basis and actual == (symbol, digest),
                 "CUT_SUMMARY_WHOLE_GROUP_BINDING")
            need(own_key not in names_to_summary, "CUT_SUMMARY_GROUP_OVERLAP")
            names_to_summary[own_key] = digest
        edges += len(doc["imports"])
        need(edges <= limits.max_edges, "CUT_SUMMARY_EDGE_BOUND")
        groups[digest] = (selected, doc)
        for name, symbol in doc["imports"]:
            schedule(name, symbol)

    # A second imported name may resolve to an already-scheduled digest. Check
    # every demanded membership, not just the first name that fetched a group.
    for key, actual in resolved.items():
        if actual is not None:
            need(names_to_summary.get(key) == actual[1], "CUT_SUMMARY_DEMANDED_GROUP_MEMBER")

    dependencies, dependents = {}, {}
    for digest, (selected, doc) in groups.items():
        check()
        parents = set()
        for name, _ in doc["imports"]:
            key = E.name_key(name, limits.syntax)
            if key in basis:
                continue
            need(key in names_to_summary, "CUT_SUMMARY_UNCLOSED_IMPORT")
            parent = names_to_summary[key]
            need(selected.kind != "concrete" or groups[parent][0].kind != "theorem",
                 "CUT_SUMMARY_CONCRETE_NEEDS_OLD_THEOREM")
            parents.add(parent)
        need(digest not in parents, "CUT_SUMMARY_SELF_DEPENDENCY")
        dependencies[digest] = len(parents)
        for parent in parents:
            dependents.setdefault(parent, []).append(digest)
    ready = deque(sorted(key for key, value in dependencies.items() if value == 0))
    ordered = []
    while ready:
        check()
        digest = ready.popleft()
        ordered.append(digest)
        for child in sorted(dependents.get(digest, [])):
            dependencies[child] -= 1
            if dependencies[child] == 0:
                ready.append(child)
    need(len(ordered) == len(groups), "CUT_SUMMARY_CYCLIC_CLOSURE")
    concrete, signatures = [], []
    new_unit = E.canonical_json(evidence.document["unit"])
    payload_bytes = len(new_unit)
    for digest in ordered:
        check()
        selected, doc = groups[digest]
        if selected.kind == "concrete":
            raw = E.canonical_json(doc["payload"])
            concrete.append(raw)
        else:
            name, symbol = doc["bindings"][0]
            raw = E.canonical_json([name, 0, symbol, doc["payload"]])
            signatures.append(raw)
        payload_bytes += len(raw)
        need(payload_bytes <= limits.max_payload_bytes, "CUT_SUMMARY_PAYLOAD_BOUND")
    need(payload_bytes <= limits.max_payload_bytes, "CUT_SUMMARY_PAYLOAD_BOUND")
    frontier = tuple((key, value[0], value[1]) for key, value in sorted(resolved.items())
                     if value is not None)
    check()
    return Prepared(tuple(concrete), tuple(signatures), new_unit, projected, frontier, new_keys,
                    Stats(len(raw_new), acquired_bytes, len(groups), len(resolved) + len(basis_seen),
                          lookup_calls, edges, nodes, payload_bytes))
