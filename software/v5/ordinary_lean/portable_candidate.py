"""Bind an owner's inert candidate to exact portable evidence, NOT acceptance.

This is local authoring policy, never a peer-evidence import rule. Claimed IDs
must survive unchanged. Only explicitly unclaimed names may receive the owner's
chosen protected-context interpretation. The resulting complete units still
require the independent ordinary admission core. No network/native/file I/O.
"""
from __future__ import annotations

from dataclasses import dataclass
import json

import ordinary_evidence as E
import ordinary_semantics as S
import portable_evidence as PE

SCHEMA = "DMKN_ORDINARY_CANDIDATE_BUNDLE_V2"
ASSURANCE = "INERT_OWNER_EXPORT_NOT_MATHEMATICAL_ACCEPTANCE"


def need(condition, code):
    if not condition:
        raise ValueError(code)


@dataclass(frozen=True)
class Limits:
    max_bundle_bytes: int = 64 * 1024**2
    max_units: int = 1024
    max_bindings: int = 65536
    max_targets: int = 1024
    max_total_nodes: int = 2097152
    max_evidence_bytes: int = 64 * 1024**2

    def __post_init__(self):
        need(all(type(x) is int and 0 < x <= 2**32-1 for x in vars(self).values()),
             "CANDIDATE_LIMIT_CONFIGURATION")


@dataclass(frozen=True)
class BoundCandidate:
    status: str
    context_root: str
    raw_units: tuple[bytes, ...]
    missing_names: tuple[bytes, ...]
    targets: tuple[bytes, ...]
    looked_up_names: int
    total_nodes: int

    @property
    def mathematical_acceptance(self):
        return False


def _writer_json(raw, maximum):
    """The existing bounded Lean-writer grammar, without canonical-key demand.

    Writer output is not portable evidence yet. Depth/numeric bounds precede the
    general JSON parser; duplicate keys are rejected. Exact raw units are then
    canonically encoded, never trusted because a local compiler wrote them.
    """
    need(type(raw) is bytes and 0 < len(raw) <= maximum, "CANDIDATE_WRITER_BYTES")
    stack, quoted, escaped, i = [], False, False, 0
    while i < len(raw):
        byte = raw[i]
        if quoted:
            need(byte >= 32, "CANDIDATE_WRITER_STRING_CONTROL")
            if escaped:
                escaped = False
            elif byte == 92:
                escaped = True
            elif byte == 34:
                quoted = False
            i += 1
            continue
        if byte == 34:
            quoted = True
        elif byte in (91, 123):
            stack.append(byte)
            need(len(stack) <= 64, "CANDIDATE_WRITER_DEPTH")
        elif byte in (93, 125):
            need(stack and stack.pop() == (91 if byte == 93 else 123), "CANDIDATE_WRITER_BRACKETS")
        elif 48 <= byte <= 57:
            start = i
            while i < len(raw) and 48 <= raw[i] <= 57:
                i += 1
                need(i-start <= 20, "CANDIDATE_WRITER_INTEGER_DIGITS")
            token = raw[start:i]
            need((len(token) == 1 or token[0] != 48) and
                 (len(token) < 20 or token <= b"18446744073709551615"), "CANDIDATE_WRITER_UINT64")
            continue
        else:
            need(byte in (9, 10, 13, 32, 44, 58), "CANDIDATE_WRITER_TOKEN")
        i += 1
    need(not quoted and not escaped and not stack, "CANDIDATE_WRITER_UNTERMINATED")

    def pairs(rows):
        found = {}
        for key, value in rows:
            need(key not in found, "CANDIDATE_WRITER_DUPLICATE_KEY")
            found[key] = value
        return found

    def reject(_):
        raise ValueError("CANDIDATE_WRITER_NONINTEGER")

    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                          parse_float=reject, parse_constant=reject)
    except (UnicodeError, RecursionError, json.JSONDecodeError) as exc:
        raise ValueError("CANDIDATE_WRITER_SYNTAX") from exc


def bind_candidate(raw, *, semantic_id, foundation_id, context_root,
                   expected_targets, prepared_bindings, warranted_symbol,
                   limits=Limits(), check_budget=None):
    """Return READY evidence or all missing local-interpretation names together.

    `warranted_symbol(encoded_name)` must be a stable point lookup in the owner's
    protected selected context, returning its exact ID or None. Arbitrary maps do
    not satisfy that premise. `prepared_bindings` is the exact authenticated
    scratch request's bytes-name->ID map, not a remotely supplied claim. No whole
    accepted-library enumeration occurs here. These premises affect candidate
    interpretation; only actual admission can confer a mathematical warrant.

    The exporter supplies dependency-ordered complete units. A forward reference,
    duplicate output or existing-name collision refuses, without native work.
    Missing names are NOT exact remote locators and are never used to overwrite
    an already claimed ID. Larger acquisition is an explicit caller decision.
    """
    need(type(limits) is Limits, "CANDIDATE_LIMIT_CONFIGURATION")
    need(semantic_id == S.semantic_id() and foundation_id == S.foundation_id(),
         "CANDIDATE_SELECTED_SEMANTICS")
    E._hex(context_root)
    need(type(prepared_bindings) is dict and len(prepared_bindings) <= limits.max_bindings,
         "CANDIDATE_PREPARED_BINDING_BOUND")

    def check():
        if check_budget is not None:
            check_budget()

    check()
    doc = _writer_json(raw, limits.max_bundle_bytes)
    check()
    need(type(doc) is dict and set(doc) == {"schema", "assurance", "semantic_id", "foundation_id",
         "context_root", "targets", "boundary_imports", "unresolved_imports", "units", "stats"},
         "CANDIDATE_BUNDLE_FIELDS")
    need(doc["schema"] == SCHEMA and doc["assurance"] == ASSURANCE and
         doc["semantic_id"] == semantic_id and doc["foundation_id"] == foundation_id and
         doc["context_root"] == context_root, "CANDIDATE_BUNDLE_CONTEXT")
    targets = E._array(doc["targets"], maximum=limits.max_targets)
    E._array(expected_targets, maximum=limits.max_targets)
    target_keys = tuple(E.name_key(name) for name in targets)
    need(bool(targets) and targets == expected_targets and len(set(target_keys)) == len(target_keys),
         "CANDIDATE_EXACT_TARGETS")
    claimed = E._array(doc["boundary_imports"], maximum=limits.max_bindings)
    unresolved = E._array(doc["unresolved_imports"], maximum=limits.max_bindings)
    need(len(claimed)+len(unresolved) <= limits.max_bindings, "CANDIDATE_AGGREGATE_BINDING_BOUND")
    units = E._array(doc["units"], maximum=limits.max_units)
    need(bool(units), "CANDIDATE_UNITS_REQUIRED")
    stats = doc["stats"]
    need(type(stats) is dict and set(stats) == {"source_records_enumerated", "selected_units",
         "dependency_edges", "scan_nodes", "unit_json_bytes", "boundary_imports", "unresolved_imports"},
         "CANDIDATE_STATISTICS_FIELDS")
    for value in stats.values():
        E._uint(value)
    need(stats["selected_units"] == len(units) and stats["boundary_imports"] == len(claimed) and
         stats["unresolved_imports"] == len(unresolved), "CANDIDATE_STATISTICS_CENSUS")

    looked_up, available, seen, missing = {}, {}, set(), []

    def lookup(name):
        key = E.name_key(name)
        if key not in looked_up:
            check()
            need(len(looked_up) < 2*limits.max_bindings, "CANDIDATE_LOOKUP_BOUND")
            symbol = warranted_symbol(name)
            need(symbol is None or type(symbol) is str, "CANDIDATE_LOOKUP_TYPE")
            looked_up[key] = None if symbol is None else E._hex(symbol)
        return looked_up[key]

    for row in claimed:
        name, symbol = E._array(row, 2)
        key = E.name_key(name)
        E._hex(symbol)
        need(key not in available and prepared_bindings.get(key) == symbol and lookup(name) == symbol,
             "CANDIDATE_CLAIMED_IDENTITY")
        available[key] = symbol
    for name in unresolved:
        key = E.name_key(name)
        need(key not in seen and key not in available and key not in prepared_bindings,
             "CANDIDATE_DUPLICATE_OR_PREPARED_UNCLAIMED")
        seen.add(key)
        symbol = lookup(name)
        if symbol is None:
            missing.append(key)
        else:
            available[key] = symbol

    censuses, all_outputs, nodes, unit_bytes = [], set(), 0, 0
    for unit in units:
        check()
        census = E.inspect_unit(unit)
        nodes += census.total_nodes
        unit_bytes += len(E.canonical_json(unit))
        need(nodes <= limits.max_total_nodes and unit_bytes <= limits.max_bundle_bytes,
             "CANDIDATE_AGGREGATE_UNIT_BOUND")
        for row in unit[2]:
            key = E.name_key(row[0])
            need(key not in all_outputs and key not in available and key not in seen and
                 lookup(row[0]) is None, "CANDIDATE_EXISTING_OR_DUPLICATE_OUTPUT")
            all_outputs.add(key)
            need(len(all_outputs) <= limits.max_bindings, "CANDIDATE_OUTPUT_BOUND")
        censuses.append(census)
    need(unit_bytes == stats["unit_json_bytes"] and set(target_keys) <= all_outputs,
         "CANDIDATE_UNIT_BYTES_OR_TARGET")
    # Even a NEEDS result describes a well-shaped selected graph, not arbitrary
    # advertised missing names attached to a forward/cyclic new-unit request.
    earlier = set(available) | set(missing)
    for unit, census in zip(units, censuses):
        need(set(census.external_names) <= earlier, "CANDIDATE_UNBOUND_OR_FORWARD_REFERENCE")
        earlier.update(E.name_key(row[0]) for row in unit[2])
    check()
    if missing:
        return BoundCandidate("NEEDS_LOCAL_INTERPRETATIONS", context_root, (), tuple(sorted(missing)),
                              target_keys, len(looked_up), nodes)

    evidence, total_bytes = [], 0
    for unit, census in zip(units, censuses):
        check()
        imports = [[E.strict_json(key), available[key]] for key in census.external_names]
        envelope = E.canonical_json({"schema": PE.SCHEMA, "semantic_id": semantic_id,
                                    "imports": imports, "unit": unit})
        total_bytes += len(envelope)
        need(total_bytes <= limits.max_evidence_bytes, "CANDIDATE_EVIDENCE_BYTE_BOUND")
        parsed = PE.read_evidence(envelope)
        evidence.append(envelope)
        for row in unit[2]:
            available[E.name_key(row[0])] = S.export_id(semantic_id, parsed.unit_id, row[0])
    check()
    return BoundCandidate("READY", context_root, tuple(evidence), (), target_keys, len(looked_up), nodes)
