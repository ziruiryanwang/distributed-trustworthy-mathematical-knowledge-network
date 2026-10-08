"""Canonical module specifications and openings, without mathematical admission.

All successful functions establish structural/hash properties only. The new
native/guest relation and actual certificate verification are separate gates.
No frozen v4 protocol or implementation is imported by this module.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any

SPEC_SCHEMA = "DMKN_MODULE_SPEC_V1"
SUMMARY_SCHEMA = "DMKN_MODULE_SUMMARY_V1"
OPENING_SCHEMA = "DMKN_MODULE_GROUP_OPENING_V1"
HEX = re.compile(r"[0-9a-f]{64}\Z")
KINDS = {"definition", "theorem", "opaque", "inductive", "constructor", "recursor"}
BINDERS = {"default", "implicit", "strictImplicit", "instImplicit"}


class StructureError(ValueError):
    """Invalid or unsupported canonical structure, never a mathematical result."""


@dataclass(frozen=True)
class Limits:
    max_bytes: int = 16 * 1024 * 1024
    max_groups: int = 4096
    max_declarations: int = 16384
    max_nodes: int = 250000
    max_depth: int = 192
    max_name_parts: int = 64
    max_string_bytes: int = 1024
    max_universes: int = 256


DEFAULT_LIMITS = Limits()


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise StructureError(reason)


def fields(value: Any, names: set[str]) -> dict:
    require(type(value) is dict and set(value) == names, "EXACT_RECORD_FIELDS")
    return value


def uint(value: Any, maximum: int = 2**32 - 1) -> int:
    require(type(value) is int and 0 <= value <= maximum, "BOUNDED_UNSIGNED_INTEGER")
    return value


def digest_string(value: Any) -> str:
    require(type(value) is str and HEX.fullmatch(value) is not None, "LOWERCASE_DIGEST")
    return value


def canonical(value: Any, limits: Limits = DEFAULT_LIMITS) -> bytes:
    try:
        result = json.dumps(value, ensure_ascii=False, sort_keys=True,
                            separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (TypeError, ValueError, RecursionError, UnicodeError) as exc:
        raise StructureError("CANONICAL_ENCODING") from exc
    require(len(result) <= limits.max_bytes, "CANONICAL_BYTE_LIMIT")
    return result


def parse_json(data: bytes, limits: Limits = DEFAULT_LIMITS) -> Any:
    require(type(data) is bytes and 0 < len(data) <= limits.max_bytes, "INPUT_BYTE_LIMIT")

    def distinct(pairs: list[tuple[str, Any]]) -> dict:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, "DUPLICATE_JSON_KEY")
            result[key] = value
        return result

    def bad_number(_value: str) -> Any:
        raise StructureError("NONINTEGER_JSON_NUMBER")

    try:
        result = json.loads(data.decode("utf-8"), object_pairs_hook=distinct,
                            parse_float=bad_number, parse_constant=bad_number)
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise StructureError("JSON_DECODE") from exc
    canonical(result, limits)
    return result


def hash_value(domain: str, value: Any, limits: Limits = DEFAULT_LIMITS) -> str:
    tag = domain.encode("ascii")
    content = canonical(value, limits)
    framed = b"DMKN-V5-MODULE\0" + len(tag).to_bytes(4, "big") + tag
    return hashlib.sha256(framed + len(content).to_bytes(8, "big") + content).hexdigest()


class _Budget:
    def __init__(self, limits: Limits):
        self.limits = limits
        self.nodes = 0

    def visit(self, depth: int) -> None:
        self.nodes += 1
        require(depth <= self.limits.max_depth and self.nodes <= self.limits.max_nodes,
                "STRUCTURE_WORK_LIMIT")


def validate_name(value: Any, limits: Limits = DEFAULT_LIMITS) -> None:
    require(type(value) is list and 0 < len(value) <= limits.max_name_parts, "NAME_PARTS")
    for part in value:
        require(type(part) is list and len(part) == 2, "NAME_COMPONENT")
        if part[0] == "s":
            require(type(part[1]) is str and 0 < len(part[1].encode("utf-8"))
                    <= limits.max_string_bytes, "NAME_STRING")
            require("\x00" not in part[1], "NAME_NUL")
        elif part[0] == "n":
            uint(part[1])
        else:
            raise StructureError("NAME_TAG")


def name_key(value: Any, limits: Limits = DEFAULT_LIMITS) -> bytes:
    validate_name(value, limits)
    return canonical(value, limits)


def _ref(value: Any, budget: _Budget, depth: int) -> None:
    budget.visit(depth)
    require(type(value) is list and value, "REFERENCE")
    if value[0] in ("foundation", "local"):
        require(len(value) == 2, "REFERENCE_ARITY")
        validate_name(value[1], budget.limits)
    elif value[0] == "external":
        require(len(value) == 3, "REFERENCE_ARITY")
        digest_string(value[1])
        validate_name(value[2], budget.limits)
    else:
        raise StructureError("REFERENCE_TAG")


def _level(value: Any, arity: int, budget: _Budget, depth: int) -> None:
    budget.visit(depth)
    require(type(value) is list and value, "LEVEL")
    tag = value[0]
    if tag == "zero":
        require(len(value) == 1, "LEVEL_ARITY")
    elif tag == "param":
        require(len(value) == 2, "LEVEL_ARITY")
        require(uint(value[1], budget.limits.max_universes) < arity, "LEVEL_BINDER_SCOPE")
    elif tag == "succ":
        require(len(value) == 2, "LEVEL_ARITY")
        _level(value[1], arity, budget, depth + 1)
    elif tag in ("max", "imax"):
        require(len(value) == 3, "LEVEL_ARITY")
        _level(value[1], arity, budget, depth + 1)
        _level(value[2], arity, budget, depth + 1)
    else:
        raise StructureError("LEVEL_TAG")


def _expr(value: Any, universes: int, binders: int, budget: _Budget, depth: int) -> None:
    budget.visit(depth)
    require(type(value) is list and value, "EXPRESSION")
    tag = value[0]
    if tag == "bvar":
        require(len(value) == 2 and uint(value[1]) < binders, "BOUND_VARIABLE_SCOPE")
    elif tag == "sort":
        require(len(value) == 2, "EXPRESSION_ARITY")
        _level(value[1], universes, budget, depth + 1)
    elif tag == "const":
        require(len(value) == 3 and type(value[2]) is list
                and len(value[2]) <= budget.limits.max_universes, "CONSTANT_LEVELS")
        _ref(value[1], budget, depth + 1)
        for level in value[2]:
            _level(level, universes, budget, depth + 1)
    elif tag == "app":
        require(len(value) == 3, "EXPRESSION_ARITY")
        for part in value[1:]:
            _expr(part, universes, binders, budget, depth + 1)
    elif tag in ("lam", "forall"):
        require(len(value) == 4 and type(value[1]) is str and value[1] in BINDERS, "BINDER_SHAPE")
        _expr(value[2], universes, binders, budget, depth + 1)
        _expr(value[3], universes, binders + 1, budget, depth + 1)
    elif tag == "let":
        require(len(value) == 4, "EXPRESSION_ARITY")
        _expr(value[1], universes, binders, budget, depth + 1)
        _expr(value[2], universes, binders, budget, depth + 1)
        _expr(value[3], universes, binders + 1, budget, depth + 1)
    elif tag == "proj":
        require(len(value) == 4, "EXPRESSION_ARITY")
        _ref(value[1], budget, depth + 1)
        uint(value[2])
        _expr(value[3], universes, binders, budget, depth + 1)
    else:
        raise StructureError("EXPRESSION_TAG")


def validate_expr(value: Any, universes: int, limits: Limits = DEFAULT_LIMITS) -> None:
    uint(universes, limits.max_universes)
    canonical(value, limits)
    _expr(value, universes, 0, _Budget(limits), 0)


def body_id(value: Any, universes: int, limits: Limits = DEFAULT_LIMITS) -> str:
    validate_expr(value, universes, limits)
    return hash_value("body", {"universes": universes, "expr": value}, limits)


def _names(values: Any, limits: Limits) -> list[bytes]:
    require(type(values) is list and len(values) <= limits.max_declarations, "NAME_LIST")
    keys = [name_key(value, limits) for value in values]
    require(len(keys) == len(set(keys)), "DUPLICATE_NAME_LIST")
    return keys


def _declaration(d: Any, budget: _Budget) -> None:
    fields(d, {"name", "kind", "universes", "type", "value_hash", "meta"})
    validate_name(d["name"], budget.limits)
    require(type(d["kind"]) is str and d["kind"] in KINDS, "DECLARATION_KIND")
    uint(d["universes"], budget.limits.max_universes)
    _expr(d["type"], d["universes"], 0, budget, 0)
    kind, meta = d["kind"], d["meta"]
    if kind in ("definition", "opaque"):
        digest_string(d["value_hash"])
    else:
        require(d["value_hash"] is None, "UNEXPECTED_VALUE_COMMITMENT")
    if kind == "definition":
        fields(meta, {"hint", "safety"})
        require(meta["safety"] == "safe", "UNSAFE_DEFINITION")
        hint = meta["hint"]
        if hint not in ("abbrev", "opaque"):
            fields(hint, {"regular"})
            uint(hint["regular"], 65535)
    elif kind == "opaque":
        fields(meta, {"safety"})
        require(meta["safety"] == "safe", "UNSAFE_OPAQUE")
    elif kind == "theorem":
        fields(meta, set())
    elif kind == "inductive":
        fields(meta, {"all", "constructors", "num_params", "num_indices", "num_nested",
                      "is_recursive", "is_reflexive"})
        _names(meta["all"], budget.limits)
        _names(meta["constructors"], budget.limits)
        for field in ("num_params", "num_indices", "num_nested"):
            uint(meta[field], 65535)
        require(type(meta["is_recursive"]) is bool and type(meta["is_reflexive"]) is bool,
                "INDUCTIVE_FLAGS")
    elif kind == "constructor":
        fields(meta, {"inductive", "constructor_index", "num_params", "num_fields"})
        validate_name(meta["inductive"], budget.limits)
        for field in ("constructor_index", "num_params", "num_fields"):
            uint(meta[field], 65535)
    elif kind == "recursor":
        fields(meta, {"all", "num_params", "num_indices", "num_motives", "num_minors",
                      "is_k", "rules"})
        _names(meta["all"], budget.limits)
        for field in ("num_params", "num_indices", "num_motives", "num_minors"):
            uint(meta[field], 65535)
        require(type(meta["is_k"]) is bool and type(meta["rules"]) is list
                and len(meta["rules"]) <= budget.limits.max_declarations, "RECURSOR_RULES")
        for rule in meta["rules"]:
            fields(rule, {"constructor", "num_fields", "value_hash"})
            validate_name(rule["constructor"], budget.limits)
            uint(rule["num_fields"], 65535)
            digest_string(rule["value_hash"])


def _group(group: Any, budget: _Budget) -> None:
    fields(group, {"kind", "declarations"})
    ds = group["declarations"]
    require(type(ds) is list and 0 < len(ds) <= budget.limits.max_declarations,
            "GROUP_DECLARATION_COUNT")
    keys = set()
    for declaration in ds:
        _declaration(declaration, budget)
        key = name_key(declaration["name"], budget.limits)
        require(key not in keys, "DUPLICATE_GROUP_DECLARATION")
        keys.add(key)
    if group["kind"] == "ordinary":
        require(len(ds) == 1 and ds[0]["kind"] in ("definition", "theorem", "opaque"),
                "ORDINARY_GROUP_SHAPE")
        return
    require(group["kind"] == "inductive"
            and all(d["kind"] in ("inductive", "constructor", "recursor") for d in ds),
            "INDUCTIVE_GROUP_SHAPE")
    inds = {name_key(d["name"]): d for d in ds if d["kind"] == "inductive"}
    ctors = {name_key(d["name"]): d for d in ds if d["kind"] == "constructor"}
    recs = [d for d in ds if d["kind"] == "recursor"]
    require(bool(inds) and bool(recs), "INCOMPLETE_INDUCTIVE_GROUP")
    declared_ctors: set[bytes] = set()
    for key, ind in inds.items():
        require(set(_names(ind["meta"]["all"], budget.limits)) == set(inds), "MUTUAL_GROUP_MEMBERS")
        for index, ctor_name in enumerate(ind["meta"]["constructors"]):
            ctor_key = name_key(ctor_name)
            require(ctor_key in ctors and ctor_key not in declared_ctors, "CONSTRUCTOR_CENSUS")
            ctor = ctors[ctor_key]
            require(name_key(ctor["meta"]["inductive"]) == key
                    and ctor["meta"]["constructor_index"] == index, "CONSTRUCTOR_OWNERSHIP")
            declared_ctors.add(ctor_key)
    require(declared_ctors == set(ctors), "EXTRA_CONSTRUCTOR")
    for rec in recs:
        owners = set(_names(rec["meta"]["all"], budget.limits))
        require(bool(owners) and owners <= set(inds), "RECURSOR_OWNERS")
        rule_names = [name_key(rule["constructor"]) for rule in rec["meta"]["rules"]]
        require(len(rule_names) == len(set(rule_names)) and set(rule_names) <= set(ctors),
                "RECURSOR_RULE_CENSUS")
    # Positivity, exact derived recursor names/types/rules and nested elaboration
    # are mathematical checker obligations, never inferred from this census.


def validate_group(group: Any, limits: Limits = DEFAULT_LIMITS) -> None:
    canonical(group, limits)
    _group(group, _Budget(limits))


def validate_spec(spec: Any, limits: Limits = DEFAULT_LIMITS) -> None:
    canonical(spec, limits)
    fields(spec, {"schema", "foundation", "policy", "groups"})
    require(spec["schema"] == SPEC_SCHEMA, "SPEC_SCHEMA")
    digest_string(spec["foundation"])
    digest_string(spec["policy"])
    groups = spec["groups"]
    require(type(groups) is list and 0 < len(groups) <= limits.max_groups, "MODULE_GROUP_COUNT")
    budget, seen = _Budget(limits), set()
    for group in groups:
        _group(group, budget)
        for declaration in group["declarations"]:
            key = name_key(declaration["name"], limits)
            require(key not in seen, "DUPLICATE_MODULE_DECLARATION")
            seen.add(key)
    require(len(seen) <= limits.max_declarations, "MODULE_DECLARATION_COUNT")


def _leaf(index: int, group: dict, limits: Limits) -> str:
    return hash_value("group-leaf", {"index": index, "group": group}, limits)


def _parent(left: str, right: str, limits: Limits) -> str:
    return hash_value("group-node", [left, right], limits)


def _levels(groups: list, limits: Limits) -> list[list[str]]:
    levels = [[_leaf(i, group, limits) for i, group in enumerate(groups)]]
    while len(levels[-1]) > 1:
        previous = levels[-1]
        levels.append([_parent(previous[i], previous[min(i + 1, len(previous) - 1)], limits)
                       for i in range(0, len(previous), 2)])
    return levels


def summarize(spec: Any, limits: Limits = DEFAULT_LIMITS) -> dict:
    validate_spec(spec, limits)
    return {"schema": SUMMARY_SCHEMA, "foundation": spec["foundation"], "policy": spec["policy"],
            "group_count": len(spec["groups"]), "group_root": _levels(spec["groups"], limits)[-1][0]}


def validate_summary(summary: Any, limits: Limits = DEFAULT_LIMITS) -> None:
    fields(summary, {"schema", "foundation", "policy", "group_count", "group_root"})
    require(summary["schema"] == SUMMARY_SCHEMA, "SUMMARY_SCHEMA")
    for key in ("foundation", "policy", "group_root"):
        digest_string(summary[key])
    require(0 < uint(summary["group_count"], limits.max_groups), "SUMMARY_GROUP_COUNT")


def summary_id(summary: Any, limits: Limits = DEFAULT_LIMITS) -> str:
    validate_summary(summary, limits)
    return hash_value("module-spec", summary, limits)


def module_id(spec: Any, limits: Limits = DEFAULT_LIMITS) -> str:
    return summary_id(summarize(spec, limits), limits)


def export_id(module: str, relative_name: Any, limits: Limits = DEFAULT_LIMITS) -> str:
    digest_string(module)
    validate_name(relative_name, limits)
    return hash_value("export-address", {"module": module, "name": relative_name}, limits)


def group_opening(spec: Any, index: int, limits: Limits = DEFAULT_LIMITS) -> dict:
    summary = summarize(spec, limits)
    require(uint(index, limits.max_groups) < summary["group_count"], "GROUP_INDEX")
    levels, cursor, siblings = _levels(spec["groups"], limits), index, []
    for level in levels[:-1]:
        siblings.append(level[min(cursor ^ 1, len(level) - 1)])
        cursor //= 2
    result = {"schema": OPENING_SCHEMA, "summary": summary, "index": index,
              "group": spec["groups"][index], "siblings": siblings}
    return parse_json(canonical(result, limits), limits)


def verify_group_opening(expected_module: str, opening: Any,
                         limits: Limits = DEFAULT_LIMITS) -> dict:
    """Verify commitment binding only; expected_module itself is NOT authority."""
    digest_string(expected_module)
    canonical(opening, limits)
    fields(opening, {"schema", "summary", "index", "group", "siblings"})
    require(opening["schema"] == OPENING_SCHEMA, "OPENING_SCHEMA")
    summary = opening["summary"]
    require(summary_id(summary, limits) == expected_module, "MODULE_BINDING")
    validate_group(opening["group"], limits)
    cursor, width = uint(opening["index"], limits.max_groups), summary["group_count"]
    require(cursor < width and type(opening["siblings"]) is list, "OPENING_INDEX")
    current = _leaf(cursor, opening["group"], limits)
    position = 0
    while width > 1:
        require(position < len(opening["siblings"]), "MISSING_MERKLE_SIBLING")
        sibling = digest_string(opening["siblings"][position])
        if cursor ^ 1 >= width:
            require(sibling == current, "ODD_MERKLE_PADDING")
        current = _parent(sibling, current, limits) if cursor & 1 else _parent(current, sibling, limits)
        cursor //= 2
        width = (width + 1) // 2
        position += 1
    require(position == len(opening["siblings"]) and current == summary["group_root"],
            "MERKLE_ROOT_OR_TRAILING_SIBLING")
    return parse_json(canonical(opening["group"], limits), limits)


def relocated_name(module: str, relative: Any, limits: Limits = DEFAULT_LIMITS) -> list:
    digest_string(module)
    validate_name(relative, limits)
    return [["s", "DMKN"], ["s", "Mod"], ["s", module]] + parse_json(canonical(relative, limits), limits)


def relocate_expr(expr: Any, owner: str, universes: int,
                  limits: Limits = DEFAULT_LIMITS) -> Any:
    """Return explicit absolute-name AST; not a Lean term or proof of relocation."""
    digest_string(owner)
    validate_expr(expr, universes, limits)

    def ref(value: list) -> list:
        if value[0] == "foundation":
            return ["absolute", value[1]]
        if value[0] == "local":
            return ["absolute", relocated_name(owner, value[1], limits)]
        return ["absolute", relocated_name(value[1], value[2], limits)]

    def walk(value: list) -> list:
        tag = value[0]
        if tag == "const":
            return [tag, ref(value[1]), value[2]]
        if tag == "proj":
            return [tag, ref(value[1]), value[2], walk(value[3])]
        if tag == "app":
            return [tag, walk(value[1]), walk(value[2])]
        if tag in ("lam", "forall"):
            return [tag, value[1], walk(value[2]), walk(value[3])]
        if tag == "let":
            return [tag, walk(value[1]), walk(value[2]), walk(value[3])]
        return value

    return parse_json(canonical(walk(expr), limits), limits)
