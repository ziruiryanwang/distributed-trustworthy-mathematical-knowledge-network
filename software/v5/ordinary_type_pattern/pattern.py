"""Whole-type variant keys for bounded ordinary Lean DAGs; never authority.

Port of the earlier module type-pattern relation. No owner, filesystem, network,
Lean import or proof body is accessed. Public raw inputs are parsed afresh. The
fixed inventory is caller supplied, hash-checked before parsing, and may be
prepared once by a trusted caller for repeated preview extraction.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from types import MappingProxyType

import ordinary_evidence as E
import ordinary_semantics as S
import formal_query as Q
import portable_preview as PP


PATTERN_TAG = "declared-type-pattern"
PROFILE = {
    "schema": "DMKN_ORDINARY_TYPE_PATTERN_PROFILE_V1",
    "expression_format": E.EXPR_FORMAT,
    "basis_inventory_sha256": S.INVENTORY,
    "anchors": "exact-fixed-basis-symbol-identities",
    "nonbasis": "ordered-preorder-first-occurrence-slots-shared-const-proj",
    "binder_labels": "ignored",
    "universe_labels": "ignored-ordered-arity-and-indices-preserved",
    "remaining_fields": "exact-no-reduction-no-substitution",
    "dag": "memoized-preorder-then-bottom-up-child-hashes",
}
DEFAULT_LIMITS = Q.DEFAULT_LIMITS
MAX_INVENTORY_BYTES = 1024 * 1024
INVENTORY_NAMES = 581
_CHILDREN = {3: (1, 2), 4: (3, 4), 5: (3, 4), 6: (2, 3, 4), 8: (3,)}


def _need(ok, code):
    if not ok:
        raise ValueError(code)


def _digest(domain, value):
    return hashlib.sha256(domain.encode("ascii") + b"\0" + E.canonical_json(value)).hexdigest()


PROFILE_ID = _digest("DMKN-ORDINARY-TYPE-PATTERN-PROFILE-V1", PROFILE)


@dataclass(frozen=True, slots=True, init=False)
class _Anchors:
    """Trusted same-process prepared data, never a serialized authority token."""
    semantic_id: str
    by_name: MappingProxyType
    by_symbol: MappingProxyType
    inventory_bytes: int


def prepare_inventory(inventory_raw):
    """Prepare only the exact current fixed inventory, before any input search.

    Hash validation precedes json.loads: no arbitrary peer inventory reaches its
    general parser. The fixed inventory's bytes can include native JSON formatting.
    The immutable returned object is reusable within this trusted interpreter;
    callers must not deserialize or synthesize such an object from peer data.
    """
    _need(type(inventory_raw) is bytes and
          0 < len(inventory_raw) <= MAX_INVENTORY_BYTES, "PATTERN_INVENTORY_BYTES")
    _need(hashlib.sha256(inventory_raw).hexdigest() == S.INVENTORY,
          "PATTERN_FIXED_INVENTORY")
    rows = json.loads(inventory_raw)
    _need(type(rows) is list and len(rows) == INVENTORY_NAMES,
          "PATTERN_INVENTORY_CENSUS")
    semantic, foundation = S.semantic_id(), S.foundation_id()
    by_name, by_symbol = {}, {}
    for row in rows:
        name = E._array(row, 5)[0]
        key = E.name_key(name)
        symbol = S.basis_symbol_id(semantic, foundation, name)
        _need(key not in by_name and symbol not in by_symbol,
              "PATTERN_INVENTORY_DUPLICATE")
        by_name[key] = symbol
        by_symbol[symbol] = key
    result = object.__new__(_Anchors)
    object.__setattr__(result, "semantic_id", semantic)
    object.__setattr__(result, "by_name", MappingProxyType(by_name))
    object.__setattr__(result, "by_symbol", MappingProxyType(by_symbol))
    object.__setattr__(result, "inventory_bytes", len(inventory_raw))
    return result


def _inventory(value):
    if type(value) is bytes:
        return prepare_inventory(value), len(value)
    _need(type(value) is _Anchors, "PATTERN_PREPARED_INVENTORY")
    _need(value.semantic_id == S.semantic_id(), "PATTERN_INVENTORY_SEMANTICS")
    return value, 0


def _derive(params, packet, symbols, anchors, limits, input_bytes, inventory_bytes):
    """Private traversal of freshly validated DAGs, not a public parser."""
    _, levels, nodes, root = packet
    counters = {
        "input_bytes": input_bytes,
        "inventory_bytes_hashed": inventory_bytes,
        "preorder_nodes": 0,
        "expression_edges": 0,
        "level_edges": 0,
        "universe_edges": 0,
        "symbol_occurrences": 0,
        "abstract_symbols": 0,
        "anchored_symbols": 0,
        "node_hashes": len(levels) + len(nodes),
        "max_pending_nodes": 1,
    }
    visited, slots, anchored = set(), {}, set()
    node_symbols = {}
    todo = [root]
    while todo:
        index = todo.pop()
        if index in visited:
            continue
        visited.add(index)
        counters["preorder_nodes"] += 1
        node = nodes[index]
        tag = node[0]
        if tag in (2, 8):
            identity = symbols[E.name_key(node[1], limits.codec)]
            if identity[0] == "basis":
                token = ["basis", identity[1]]
                anchored.add(identity[1])
            else:
                if identity not in slots:
                    slots[identity] = len(slots)
                token = ["slot", slots[identity]]
            node_symbols[index] = token
            counters["symbol_occurrences"] += 1
        offsets = _CHILDREN.get(tag, ())
        counters["expression_edges"] += len(offsets)
        # Reverse the push order so the declared child order is visited first.
        todo.extend(node[offset] for offset in reversed(offsets))
        counters["max_pending_nodes"] = max(counters["max_pending_nodes"], len(todo))
    _need(len(visited) == len(nodes), "PATTERN_UNREACHABLE_NODE")
    counters["abstract_symbols"] = len(slots)
    counters["anchored_symbols"] = len(anchored)

    level_keys = []
    for node in levels:
        if node[0] in (0, 4):
            normalized = node
        else:
            counters["level_edges"] += len(node) - 1
            normalized = [node[0], *[level_keys[index] for index in node[1:]]]
        level_keys.append(_digest("DMKN-ORDINARY-TYPE-PATTERN-LEVEL-V1", normalized))

    expression_keys = []
    for index, node in enumerate(nodes):
        tag = node[0]
        if tag in (0, 7, 9):
            normalized = node
        elif tag == 1:
            counters["universe_edges"] += 1
            normalized = [tag, level_keys[node[1]]]
        elif tag == 2:
            counters["universe_edges"] += len(node[2])
            normalized = [tag, node_symbols[index], [level_keys[level] for level in node[2]]]
        elif tag == 3:
            normalized = [tag, expression_keys[node[1]], expression_keys[node[2]]]
        elif tag in (4, 5):
            normalized = [tag, node[2], expression_keys[node[3]], expression_keys[node[4]]]
        elif tag == 6:
            normalized = [tag, expression_keys[node[2]], expression_keys[node[3]],
                          expression_keys[node[4]], node[5]]
        else:  # Validated projection: share the const/projection symbol table.
            normalized = [tag, node_symbols[index], node[2], expression_keys[node[3]]]
        expression_keys.append(_digest("DMKN-ORDINARY-TYPE-PATTERN-NODE-V1", normalized))

    key = _digest("DMKN-ORDINARY-TYPE-PATTERN-KEY-V1", {
        "semantic_id": anchors.semantic_id,
        "profile_id": PROFILE_ID,
        "universe_arity": len(params),
        "root": expression_keys[root],
    })
    # Structural extraction work only: parsing, hashing bytes, inventory setup
    # and physical CPU are not represented by this integer. Report bytes too.
    work = sum(counters[field] for field in (
        "preorder_nodes", "expression_edges", "level_edges", "universe_edges",
        "symbol_occurrences", "node_hashes"))
    return {"key": key, "spec": {"tag": PATTERN_TAG, "value": key},
            "profile_id": PROFILE_ID, "semantic_id": anchors.semantic_id,
            "counters": counters, "work": work, "mathematical_acceptance": False}


def preview_pattern(preview_raw, inventory, limits=DEFAULT_LIMITS):
    """Extract one complete variant key from an untrusted V2 type preview.

    Unknown symbols are compared by their exact claimed portable identities.
    A fixed-basis ID under a different name is refused, not reclassified. This
    is syntax/identity checking, not proof or correspondence validation.
    """
    Q._limits(limits)
    anchors, inventory_bytes = _inventory(inventory)
    preview = PP.read_preview(preview_raw, limits)
    doc = preview.document
    _need(doc["semantic_id"] == anchors.semantic_id, "PATTERN_SEMANTICS_NOT_SELECTED")
    symbols = {}
    for name, symbol in doc["type_bindings"]:
        key = E.name_key(name, limits.codec)
        if symbol in anchors.by_symbol:
            _need(anchors.by_symbol[symbol] == key, "PATTERN_BASIS_NAME_MISMATCH")
            symbols[key] = ("basis", symbol)
        else:
            symbols[key] = ("portable", symbol)
    return _derive(doc["header"][1], doc["header"][2], symbols, anchors,
                   limits, len(preview_raw), inventory_bytes)


def native_pattern(native_type_raw, inventory, limits=DEFAULT_LIMITS):
    """Prepare a variant query without owner lookup or invented global IDs.

    Exact selected-basis names are anchors; other local names are temporary
    distinct query variables. The AST is not a checked theorem. In particular,
    this does not certify that its original frontend uses the selected basis.
    """
    Q._limits(limits)
    anchors, inventory_bytes = _inventory(inventory)
    parsed = Q.read_native_type(native_type_raw, limits)
    symbols = {}
    for key in parsed["reference_keys"]:
        symbol = anchors.by_name.get(key)
        symbols[key] = (("basis", symbol) if symbol is not None else ("local", key))
    return _derive(parsed["universe_params"], parsed["type"], symbols, anchors,
                   limits, len(native_type_raw), inventory_bytes)
