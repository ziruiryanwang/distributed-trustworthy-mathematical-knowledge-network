"""Inert ordinary-Lean evidence identity and bounded syntax, NOT acceptance.

No module imports, proof checking, network, cache, or executable peer metadata.
The protected controller must match imports to its warranted bindings, run the
Lean decoder/checker, and compare actual generated output with the claimed census.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re


SCHEMA = "DMKN_LEAN_ORDINARY_EVIDENCE_V1"
UNIT_FORMAT = "DMKN_LEAN_ORDINARY_UNIT_V1"
EXPR_FORMAT = "DMKN_LEAN_ORIGINAL_EXPR_V1"
EVIDENCE_DOMAIN = "DMKN-ORDINARY-EVIDENCE-V1"
EXPORT_DOMAIN = "DMKN-ORDINARY-EXPORT-V1"
BASIS_SYMBOL_DOMAIN = "DMKN-ORDINARY-BASIS-SYMBOL-V1"
_HEX = re.compile(r"[0-9a-f]{64}\Z")
_U32, _U64 = (1 << 32) - 1, (1 << 64) - 1


class EvidenceError(ValueError):
    """A bounded syntax/identity refusal; not a mathematical invalidity verdict."""


def _need(condition, code):
    if not condition:
        raise EvidenceError(code)


@dataclass(frozen=True)
class Limits:
    """Trusted operation configuration; never loaded from an evidence envelope."""

    max_bytes: int = 8 * 1024 * 1024
    max_json_depth: int = 64
    max_integer_digits: int = 20
    max_name_parts: int = 4096
    max_name_bytes: int = 1024 * 1024
    max_literal_bytes: int = 1024 * 1024
    max_params: int = 1024
    max_levels: int = 65536
    max_exprs: int = 1048576
    max_dag_depth: int = 4096
    max_unit_nodes: int = 2097152
    max_inventory: int = 65536
    max_types: int = 4096
    max_constructors: int = 65536
    max_names: int = 65536
    max_imports: int = 65536

    def __post_init__(self):
        for value in vars(self).values():
            _need(type(value) is int and 1 <= value <= _U32, "LIMIT_CONFIGURATION")
        # Keep the recursive standard JSON parser below its normal stack limit.
        _need(self.max_json_depth <= 128, "JSON_DEPTH_CONFIGURATION")
        _need(self.max_integer_digits <= 20, "INTEGER_DIGITS_CONFIGURATION")


DEFAULT_LIMITS = Limits()


def canonical_json(value):
    """The existing discovery canonical encoding, independent of its schemas."""
    try:
        return json.dumps(value, sort_keys=True, ensure_ascii=False,
                          separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (TypeError, ValueError, UnicodeError, RecursionError) as exc:
        raise EvidenceError("JSON_ENCODING") from exc


def strict_json(raw, limits=DEFAULT_LIMITS):
    """Bound all raw numeric tokens/depth BEFORE calling the general JSON parser.

    This format needs only arrays, objects, strings and unsigned integers. It
    has no true/false/null or negative/fraction/exponent numeric syntax.
    """
    _need(isinstance(limits, Limits), "LIMIT_CONFIGURATION")
    _need(type(raw) is bytes and 0 < len(raw) <= limits.max_bytes, "JSON_BYTE_BOUND")
    stack, quoted, escaped, i = [], False, False, 0
    while i < len(raw):
        byte = raw[i]
        if quoted:
            _need(byte >= 32, "JSON_STRING_CONTROL")
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
            _need(len(stack) <= limits.max_json_depth, "JSON_DEPTH_BOUND")
        elif byte in (93, 125):
            _need(bool(stack) and stack.pop() == (91 if byte == 93 else 123),
                  "JSON_BRACKETS")
        elif 48 <= byte <= 57:
            start = i
            while i < len(raw) and 48 <= raw[i] <= 57:
                i += 1
                _need(i - start <= limits.max_integer_digits, "JSON_INTEGER_DIGITS")
            token = raw[start:i]
            _need(len(token) == 1 or token[0] != 48, "JSON_LEADING_ZERO")
            _need(len(token) < 20 or token <= b"18446744073709551615", "JSON_UINT64")
            continue
        elif byte not in (44, 58):
            # Includes whitespace (noncanonical), '-', '.', 'e', and nonfinite
            # or boolean tokens. None reaches json.loads' numeric conversion.
            raise EvidenceError("JSON_LEXICAL_TOKEN")
        i += 1
    _need(not quoted and not escaped and not stack, "JSON_UNTERMINATED")

    def pairs(items):
        result = {}
        for key, value in items:
            _need(key not in result, "JSON_DUPLICATE_KEY")
            result[key] = value
        return result

    def bad_number(_):
        raise EvidenceError("JSON_NONINTEGER")

    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                           parse_float=bad_number, parse_constant=bad_number)
    except EvidenceError:
        raise
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise EvidenceError("JSON_SYNTAX") from exc
    _need(canonical_json(value) == raw, "JSON_NONCANONICAL")
    return value


def _array(value, size=None, maximum=None):
    _need(type(value) is list, "ARRAY")
    _need(size is None or len(value) == size, "ARRAY_ARITY")
    _need(maximum is None or len(value) <= maximum, "ARRAY_BOUND")
    return value


def _uint(value, maximum=_U64):
    _need(type(value) is int and 0 <= value <= maximum, "INTEGER_BOUND")
    return value


def _hex(value):
    _need(type(value) is str and _HEX.fullmatch(value) is not None, "HASH_ENCODING")
    return value


def _bytes(value, maximum, *, utf8=False):
    _need(type(value) is dict and set(value) == {"$bytes"}, "BYTES_OBJECT")
    values = _array(value["$bytes"], maximum=maximum)
    result = bytes(_uint(x, 255) for x in values)
    if utf8:
        try:
            _need(result.decode("utf-8").encode("utf-8") == result, "UTF8_CANONICAL")
        except UnicodeError as exc:
            raise EvidenceError("UTF8_ENCODING") from exc
    return result


def name_key(value, limits=DEFAULT_LIMITS, *, semantic=True):
    """Exact original-name canonical bytes; not a dotted-name approximation."""
    components = _array(value, maximum=limits.max_name_parts)
    used, first = 0, None
    for index, component in enumerate(components):
        tag, item = _array(component, 2)
        tag = _uint(tag, 1)
        if tag == 0:
            payload = _bytes(item, limits.max_name_bytes - used, utf8=True)
            used += len(payload)
            if index == 0:
                first = payload.decode("utf-8")
        else:
            _uint(item, _U32)
    if semantic:
        _need(first is not None, "SEMANTIC_NAME_ROOT")
        _need(not first.startswith(("_kernel_fresh", "_ind_fresh", "_nested_fresh",
                                   "_uniq", "_nested")), "RESERVED_SEMANTIC_NAME")
        _need(first not in ("dontcare", "__expr_for_default_constructor__",
                            "__local_decl_for_default_constructor"), "RESERVED_SEMANTIC_NAME")
        if len(components) == 2 and first == "Lean" and components[1][0] == 0:
            second = bytes(components[1][1]["$bytes"]).decode("utf-8")
            _need(second not in ("reduceBool", "reduceNat"), "FORBIDDEN_EVALUATOR")
    return canonical_json(value)


def _names(value, maximum, limits, *, params=False, own=None):
    keys = [name_key(x, limits, semantic=not params)
            for x in _array(value, maximum=maximum)]
    _need(len(set(keys)) == len(keys), "DUPLICATE_NAME")
    if params:
        _need(all(x != b"[]" for x in keys), "ANONYMOUS_PARAMETER")
    if own is not None:
        _need(own in keys, "ALL_OMITS_SELF")
    return keys


def _hint(value):
    parts = _array(value)
    _need(bool(parts), "HINT_EMPTY")
    tag = _uint(parts[0], 2)
    _array(parts, 2 if tag == 2 else 1)
    if tag == 2:
        _uint(parts[1], _U32)


def _dag_references(packet, params, limits):
    """Syntactic DAG census; no expression construction, reduction or typing."""
    marker, levels, nodes, root = _array(packet, 4)
    _need(marker == EXPR_FORMAT, "EXPR_FORMAT")
    _array(levels, maximum=limits.max_levels)
    _array(nodes, maximum=limits.max_exprs)
    _need(bool(nodes), "EXPR_EMPTY")
    _uint(root, len(nodes) - 1)
    _need(root == len(nodes) - 1, "EXPR_ROOT")
    level_depths, depths, needs, refs = [], [], [], set()

    def back(value, prior):
        _uint(value)
        _need(value < len(prior), "BACKWARD_INDEX")
        return value

    for node in levels:
        _array(node)
        _need(bool(node), "LEVEL_EMPTY")
        tag = _uint(node[0], 4)
        _array(node, (1, 2, 3, 3, 2)[tag])
        if tag == 0:
            depth = 1
        elif tag == 4:
            _need(_uint(node[1]) < len(params), "LEVEL_PARAMETER")
            depth = 1
        else:
            indices = [back(x, level_depths) for x in node[1:]]
            depth = 1 + max(level_depths[x] for x in indices)
        _need(depth <= limits.max_dag_depth, "DAG_DEPTH_BOUND")
        level_depths.append(depth)
    for node in nodes:
        _array(node)
        _need(bool(node), "EXPR_NODE_EMPTY")
        tag = _uint(node[0], 9)
        _array(node, (2, 2, 3, 3, 5, 5, 6, 2, 4, 2)[tag])
        depth, need = 1, 0
        if tag == 0:
            need = _uint(node[1], _U32) + 1
        elif tag == 1:
            depth += level_depths[back(node[1], level_depths)]
        elif tag == 2:
            refs.add(name_key(node[1], limits))
            indices = [back(x, level_depths)
                       for x in _array(node[2], maximum=limits.max_params)]
            depth += max((level_depths[x] for x in indices), default=0)
        elif tag in (3, 4, 5, 6, 8):
            if tag in (4, 5, 6):
                name_key(node[1], limits, semantic=False)
            if tag in (4, 5):
                _uint(node[2], 3)
            if tag == 6:
                _uint(node[5], 1)
            if tag == 8:
                refs.add(name_key(node[1], limits))
                _uint(node[2], _U32)
            offsets = {3: (1, 2), 4: (3, 4), 5: (3, 4),
                       6: (2, 3, 4), 8: (3,)}[tag]
            indices = [back(node[x], depths) for x in offsets]
            depth += max(depths[x] for x in indices)
            requirements = [needs[x] for x in indices]
            if tag in (4, 5, 6):
                requirements[-1] = max(0, requirements[-1] - 1)
            need = max(requirements)
        else:
            literal = _bytes(node[1], limits.max_literal_bytes, utf8=(tag == 9))
            _need(tag != 7 or not literal or literal[0] != 0, "NAT_MAGNITUDE")
        _need(depth <= limits.max_dag_depth, "DAG_DEPTH_BOUND")
        depths.append(depth)
        needs.append(need)
    _need(needs[root] == 0, "EXPR_OPEN_ROOT")
    # All serialized nodes are included. Lean's subsequent decode/re-encode gate
    # refuses orphans, duplicate nodes and noncanonical traversal; they never
    # acquire authority from this syntactic census.
    return refs, len(levels) + len(nodes)


@dataclass(frozen=True)
class UnitCensus:
    """Exact serialized name keys; expected exports remain unproved claims."""

    expected_names: tuple[bytes, ...]
    external_names: tuple[bytes, ...]
    total_nodes: int


def inspect_unit(unit, limits=DEFAULT_LIMITS):
    marker, descriptor, inventory = _array(unit, 3)
    _need(marker == UNIT_FORMAT, "UNIT_FORMAT")
    _array(inventory, maximum=limits.max_inventory)
    _need(bool(inventory), "INVENTORY_EMPTY")
    names = [name_key(_array(row, 5)[0], limits) for row in inventory]
    _need(len(names) == len(set(names)), "INVENTORY_DUPLICATE_NAME")
    refs, total = set(), 0

    def dag(packet, params):
        nonlocal total
        found, count = _dag_references(packet, params, limits)
        refs.update(found)
        total += count
        _need(total <= limits.max_unit_nodes, "UNIT_NODE_BOUND")

    def params(value):
        return _names(value, limits.max_params, limits, params=True)

    def all_names(value, own=None, maximum=None):
        return _names(value, maximum or limits.max_names, limits, own=own)

    _array(descriptor)
    _need(bool(descriptor), "DESCRIPTOR_EMPTY")
    kind = _uint(descriptor[0], 3)
    if kind < 3:
        _array(descriptor, 7 if kind == 0 else 6)
        own = name_key(descriptor[1], limits)
        ps = params(descriptor[2])
        dag(descriptor[3], ps)
        dag(descriptor[4], ps)
        if kind == 0:
            _hint(descriptor[5])
        all_names(descriptor[-1], own)
        _need(names == [own], "ORDINARY_INVENTORY_CENSUS")
    else:
        _array(descriptor, 4)
        ps = params(descriptor[1])
        _uint(descriptor[2], _U32)
        types = _array(descriptor[3], maximum=limits.max_types)
        _need(bool(types), "INDUCTIVE_EMPTY")
        introduced, ctors = set(), 0
        for entry in types:
            own, type_dag, constructors = _array(entry, 3)
            declarations = [(own, type_dag)]
            for constructor in _array(constructors):
                declarations.append(tuple(_array(constructor, 2)))
                ctors += 1
                _need(ctors <= limits.max_constructors, "CONSTRUCTOR_BOUND")
            for name, type_dag in declarations:
                key = name_key(name, limits)
                _need(key not in introduced, "GROUP_DUPLICATE_NAME")
                introduced.add(key)
                dag(type_dag, ps)
        _need(introduced <= set(names), "GROUP_INVENTORY_MISSING_NAME")

    for row in inventory:
        own, row_kind, ps_raw, type_dag, details = _array(row, 5)
        own, row_kind, ps = name_key(own, limits), _uint(row_kind, 6), params(ps_raw)
        _need(row_kind >= 1, "INVENTORY_KIND")
        dag(type_dag, ps)
        _array(details, {1: 3, 2: 2, 3: 3, 4: 8, 5: 5, 6: 8}[row_kind])
        if row_kind <= 3:
            dag(details[0], ps)
            if row_kind == 1:
                _hint(details[1])
            elif row_kind == 3:
                _need(_uint(details[1], 1) == 0, "UNSAFE_INVENTORY")
            all_names(details[-1], own)
        elif row_kind == 4:
            for index in (0, 1, 4):
                _uint(details[index], _U32)
            all_names(details[2], own)
            all_names(details[3], maximum=limits.max_constructors)
            for index in (5, 7):
                _uint(details[index], 1)
            _need(_uint(details[6], 1) == 0, "UNSAFE_INVENTORY")
        elif row_kind == 5:
            name_key(details[0], limits)
            for index in (1, 2, 3):
                _uint(details[index], _U32)
            _need(_uint(details[4], 1) == 0, "UNSAFE_INVENTORY")
        else:
            _need(bool(all_names(details[0])), "RECURSOR_GROUP_EMPTY")
            for index in (1, 2, 3, 4):
                _uint(details[index], _U32)
            for rule in _array(details[5], maximum=limits.max_constructors):
                constructor, fields, rhs = _array(rule, 3)
                name_key(constructor, limits)
                _uint(fields, _U32)
                dag(rhs, ps)
            _uint(details[6], 1)
            _need(_uint(details[7], 1) == 0, "UNSAFE_INVENTORY")
    return UnitCensus(tuple(sorted(names)), tuple(sorted(refs - set(names))), total)


def _digest(domain, value):
    return hashlib.sha256(domain.encode("ascii") + b"\0" + canonical_json(value)).hexdigest()


def export_id(profile_id, unit_id, original_name, limits=DEFAULT_LIMITS):
    """Derive a claimed export identity; does not show that it exists or is valid."""
    name_key(original_name, limits)
    return _digest(EXPORT_DOMAIN, [_hex(profile_id), _hex(unit_id), original_name])


def basis_symbol_id(profile_id, basis_id, original_name, limits=DEFAULT_LIMITS):
    """Bind an exact basis identity; the caller still has to warrant that basis."""
    name_key(original_name, limits)
    return _digest(BASIS_SYMBOL_DOMAIN, [_hex(profile_id), _hex(basis_id), original_name])


@dataclass(frozen=True)
class Evidence:
    """Inert parsed data, never an acceptance token. `document` is not immutable."""

    raw: bytes
    document: dict
    unit_id: str
    census: UnitCensus


def read_evidence(raw, limits=DEFAULT_LIMITS):
    document = strict_json(raw, limits)
    _need(type(document) is dict and
          set(document) == {"schema", "profile_id", "imports", "unit"}, "EVIDENCE_FIELDS")
    _need(document["schema"] == SCHEMA, "EVIDENCE_SCHEMA")
    _hex(document["profile_id"])
    census = inspect_unit(document["unit"], limits)
    keys = []
    for row in _array(document["imports"], maximum=limits.max_imports):
        name, symbol = _array(row, 2)
        keys.append(name_key(name, limits))
        _hex(symbol)
    _need(keys == sorted(set(keys)), "IMPORT_ORDER_OR_DUPLICATE")
    _need(tuple(keys) == census.external_names, "IMPORT_REFERENCE_CENSUS")
    # Exact canonical raw bytes are already established; no mutable object is
    # reserialized between validation and this identity computation.
    unit_id = hashlib.sha256(EVIDENCE_DOMAIN.encode("ascii") + b"\0" + raw).hexdigest()
    return Evidence(raw, document, unit_id, census)
