"""Bounded ordinary formal-contract queries, never evidence or acceptance.

All public inputs are bounded raw bytes. The caller supplies already known
portable symbol bindings; this module never derives them from names, fetches
dependencies, imports a Lean environment or mutates an owner/index. Type-only
syntax validation reuses the existing ordinary preview census and codec.
"""
from __future__ import annotations

import hashlib

import ordinary_evidence as E
import ordinary_preview as P
import ordinary_semantics as S
import portable_preview as PP


NATIVE_SCHEMA = "DMKN_ORDINARY_LEAN_QUERY_TYPE_AST_V1"
QUERY_SCHEMA = "DMKN_ORDINARY_FORMAL_TYPE_QUERY_V1"
PROFILE = {
    "schema": "DMKN_ORDINARY_EXACT_TYPE_KEY_PROFILE_V1",
    "expression_format": E.EXPR_FORMAT,
    "binder_labels": "ignored",
    "universe_labels": "ignored-ordered-arity-and-indices-preserved",
    "constant_identity": "exact-portable-symbol-and-level-instance",
    "remaining_fields": "exact-no-reduction-no-substitution",
    "dag": "bottom-up-child-hashes-independent-of-numbering-and-sharing",
}


def _digest(domain, value):
    return hashlib.sha256(domain.encode("ascii") + b"\0" + E.canonical_json(value)).hexdigest()


PROFILE_ID = _digest("DMKN-ORDINARY-EXACT-TYPE-PROFILE-V1", PROFILE)
DEFAULT_LIMITS = P.DEFAULT_LIMITS


def _need(ok, code):
    if not ok:
        raise ValueError(code)


def _limits(limits):
    _need(type(limits) is P.Limits, "FORMAL_QUERY_LIMITS")
    # Caller-selected stricter limits are allowed, not a peer-granted increase.
    _need(limits.max_type_nodes <= DEFAULT_LIMITS.max_type_nodes and
          limits.max_type_bindings <= DEFAULT_LIMITS.max_type_bindings and
          all(getattr(limits.codec, field) <= maximum
              for field, maximum in vars(DEFAULT_LIMITS.codec).items()),
          "FORMAL_QUERY_LIMITS_NOT_STRICTER")
    return limits


def _census(params, packet, limits):
    # Kind 2 is only the existing syntax validator's header slot. No theorem,
    # declaration, preview, UnitID or accepted record is created by this call.
    return P._type_census([2, params, packet], limits)


def read_native_type(raw, limits=DEFAULT_LIMITS):
    """Read owner-produced AST bytes; successful parsing is not type authority."""
    _limits(limits)
    schema, params, packet = E._array(E.strict_json(raw, limits.codec), 3)
    _need(schema == NATIVE_SCHEMA, "FORMAL_QUERY_NATIVE_SCHEMA")
    refs, nodes = _census(params, packet, limits)
    return {"universe_params": params, "type": packet,
            "reference_keys": refs, "type_nodes": nodes}


def reference_names(native_raw, limits=DEFAULT_LIMITS):
    """List exactly the names whose already known identities the caller needs."""
    parsed = read_native_type(native_raw, limits)
    return [E.strict_json(key, limits.codec) for key in parsed["reference_keys"]]


def _bindings(rows, refs, limits):
    keys, bound = [], {}
    for row in E._array(rows, maximum=limits.max_type_bindings):
        name, symbol = E._array(row, 2)
        key = E.name_key(name, limits.codec)
        keys.append(key)
        bound[key] = E._hex(symbol)
    _need(tuple(keys) == refs, "FORMAL_QUERY_BINDING_CENSUS_OR_ORDER")
    return bound


def bind_native_type(native_raw, bindings_raw, *, semantic_id, limits=DEFAULT_LIMITS):
    """Combine query syntax with exact caller-known search bindings.

    Bindings are a canonical JSON list of [originalName, portableSymbolID] rows,
    in the reference_names order. Even a well-formed false association is only
    a search input, not a warrant. Unknown identities must not be guessed.
    """
    parsed = read_native_type(native_raw, limits)
    _need(E._hex(semantic_id) == S.semantic_id(), "FORMAL_QUERY_SEMANTICS_NOT_SELECTED")
    rows = E.strict_json(bindings_raw, limits.codec)
    _bindings(rows, parsed["reference_keys"], limits)
    raw = E.canonical_json({"schema": QUERY_SCHEMA, "semantic_id": semantic_id,
        "key_profile": PROFILE_ID, "universe_params": parsed["universe_params"],
        "type": parsed["type"], "type_bindings": rows})
    read_query(raw, limits)
    return raw


def read_query(raw, limits=DEFAULT_LIMITS):
    """Reparse complete raw query at each boundary; returned dicts are inert."""
    _limits(limits)
    doc = E.strict_json(raw, limits.codec)
    _need(type(doc) is dict and set(doc) == {
        "schema", "semantic_id", "key_profile", "universe_params", "type", "type_bindings"},
        "FORMAL_QUERY_FIELDS")
    _need(doc["schema"] == QUERY_SCHEMA and doc["key_profile"] == PROFILE_ID,
          "FORMAL_QUERY_SCHEMA_OR_PROFILE")
    _need(E._hex(doc["semantic_id"]) == S.semantic_id(), "FORMAL_QUERY_SEMANTICS_NOT_SELECTED")
    refs, nodes = _census(doc["universe_params"], doc["type"], limits)
    _bindings(doc["type_bindings"], refs, limits)
    return doc, nodes


def _structural_key(semantic_id, params, packet, bindings, limits):
    """Private bottom-up keying of freshly validated syntax, not a validator."""
    bound = {E.name_key(name, limits.codec): symbol for name, symbol in bindings}
    _, levels, expressions, root = packet
    level_keys = []
    for node in levels:
        tag = node[0]
        if tag in (0, 4):
            normalized = node  # zero or exact ordered universe-parameter index
        else:
            normalized = [tag, *[level_keys[index] for index in node[1:]]]
        level_keys.append(_digest("DMKN-ORDINARY-EXACT-TYPE-LEVEL-V1", normalized))
    expression_keys = []
    for node in expressions:
        tag = node[0]
        if tag in (0, 7, 9):
            normalized = node
        elif tag == 1:
            normalized = [tag, level_keys[node[1]]]
        elif tag == 2:
            normalized = [tag, bound[E.name_key(node[1], limits.codec)],
                          [level_keys[index] for index in node[2]]]
        elif tag == 3:
            normalized = [tag, expression_keys[node[1]], expression_keys[node[2]]]
        elif tag in (4, 5):
            normalized = [tag, node[2], expression_keys[node[3]], expression_keys[node[4]]]
        elif tag == 6:
            normalized = [tag, expression_keys[node[2]], expression_keys[node[3]],
                          expression_keys[node[4]], node[5]]
        else:  # validated projection: retain exact structure identity and field
            normalized = [tag, bound[E.name_key(node[1], limits.codec)], node[2],
                          expression_keys[node[3]]]
        expression_keys.append(_digest("DMKN-ORDINARY-EXACT-TYPE-NODE-V1", normalized))
    return {"key": _digest("DMKN-ORDINARY-EXACT-TYPE-KEY-V1", {
                "semantic_id": semantic_id, "profile_id": PROFILE_ID,
                "universe_arity": len(params), "root": expression_keys[root]}),
            # This counts this key pass, not parsing/elaboration or physical CPU.
            "key_node_visits": len(levels) + len(expressions)}


def type_key(query_raw, limits=DEFAULT_LIMITS):
    doc, _ = read_query(query_raw, limits)
    return _structural_key(doc["semantic_id"], doc["universe_params"], doc["type"],
                           doc["type_bindings"], limits)["key"]


def query_spec(query_raw, limits=DEFAULT_LIMITS):
    """One exact feature spec; caller funds/selects ordinary find separately."""
    return {"tag": "declared-type-key", "value": type_key(query_raw, limits)}


def preview_key(preview_raw, limits=DEFAULT_LIMITS):
    """Same key from exact V2 advertised type; still no evidence acceptance."""
    _limits(limits)
    preview = PP.read_preview(preview_raw, limits)
    doc = preview.document
    _need(doc["semantic_id"] == S.semantic_id(), "FORMAL_QUERY_SEMANTICS_NOT_SELECTED")
    return _structural_key(doc["semantic_id"], doc["header"][1], doc["header"][2],
                           doc["type_bindings"], limits)
