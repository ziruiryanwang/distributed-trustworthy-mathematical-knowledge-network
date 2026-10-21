"""Bounded whole-type variant keys; never mathematics or symbol transport.

Only nonfoundation symbol addresses are forgotten. This is not definitional
equality, generalization, metavariable matching, or a semantic equivalence test.
"""
from __future__ import annotations

import json

PATTERN_PROFILE_SCHEMA = "DMKN_MODULE_EXPORT_TYPE_PATTERN_PROFILE_V1"
PATTERN_TAG = "declared-type-pattern"
MAX_VALUES = 1_000_000
MAX_DEPTH = 256
MAX_LIST = 256
MAX_BYTES = 16 * 1024**2 - 256
MAX_STRING_CHARS = 1024
MAX_INTEGER = 2**32 - 1


def _need(ok, code):
    if not ok:
        raise ValueError(code)


def validate_type_pattern_profile(profile):
    _need(type(profile) is dict and set(profile) == {"schema"},
          "EXPORT_TYPE_PATTERN_PROFILE_FIELDS")
    _need(profile["schema"] == PATTERN_PROFILE_SCHEMA,
          "EXPORT_TYPE_PATTERN_PROFILE_SCHEMA")
    return {"schema": PATTERN_PROFILE_SCHEMA}


def _preflight(value):
    """Count JSON occurrences before any whole-tree serialization/copy.

    Iterator frames keep stack storage bounded by depth. A shared subtree is
    charged again at every occurrence; a cycle reaches the depth bound.
    """
    stack = [(iter((value,)), 0)]
    count = size = 0
    while stack:
        children, depth = stack[-1]
        try:
            item = next(children)
        except StopIteration:
            stack.pop()
            continue
        count += 1
        _need(count <= MAX_VALUES and depth <= MAX_DEPTH,
              "EXPORT_TYPE_PATTERN_PREFLIGHT_WORK")
        if type(item) is list:
            _need(len(item) <= MAX_LIST, "EXPORT_TYPE_PATTERN_PREFLIGHT_LIST")
            size += 2 + max(0, len(item) - 1)
            stack.append((iter(item), depth + 1))
        elif type(item) is str:
            # Bound the small scalar BEFORE JSON escaping or UTF-8 allocation.
            _need(len(item) <= MAX_STRING_CHARS,
                  "EXPORT_TYPE_PATTERN_PREFLIGHT_STRING")
            try:
                size += len(json.dumps(item, ensure_ascii=False,
                    separators=(",", ":"), allow_nan=False).encode("utf-8"))
            except (UnicodeError, ValueError) as exc:
                raise ValueError("EXPORT_TYPE_PATTERN_PREFLIGHT_ENCODING") from exc
        elif type(item) is int:
            _need(0 <= item <= MAX_INTEGER, "EXPORT_TYPE_PATTERN_PREFLIGHT_INTEGER")
            size += len(str(item))
        else:
            raise ValueError("EXPORT_TYPE_PATTERN_PREFLIGHT_VALUE")
        _need(size <= MAX_BYTES, "EXPORT_TYPE_PATTERN_PREFLIGHT_BYTES")
    return count


def _derive(codec, owner_module_id, universes, type_expr):
    # No arbitrary large owner, arity conversion, or entire-tree encoding first.
    _need(type(owner_module_id) is str and len(owner_module_id) == 64,
          "EXPORT_TYPE_PATTERN_OWNER")
    codec.digest_string(owner_module_id)
    codec.uint(universes, codec.DEFAULT_LIMITS.max_universes)
    count = _preflight(type_expr)
    codec.validate_expr(type_expr, universes)
    symbols = {}

    def reference(ref):
        if ref[0] == "foundation":
            return ["foundation", ref[1]]
        owner, name = ((owner_module_id, ref[1]) if ref[0] == "local"
                       else (ref[1], ref[2]))
        key = owner, codec.name_key(name)
        if key not in symbols:
            symbols[key] = len(symbols)
        return ["slot", symbols[key]]

    def walk(expr):
        tag = expr[0]
        if tag == "const":
            return [tag, reference(expr[1]), expr[2]]
        if tag == "proj":
            ref = reference(expr[1])
            return [tag, ref, expr[2], walk(expr[3])]
        if tag == "app":
            return [tag, walk(expr[1]), walk(expr[2])]
        if tag in ("forall", "lam"):
            return [tag, expr[1], walk(expr[2]), walk(expr[3])]
        if tag == "let":
            return [tag, walk(expr[1]), walk(expr[2]), walk(expr[3])]
        return expr  # Validated sort/level and bvar syntax stays exact.

    normalized = {"universes": universes, "type": walk(type_expr)}
    key = codec.hash_value("declared-type-pattern-v1", normalized)
    return {"tag": PATTERN_TAG, "value": key}, count


def pattern_spec(codec, owner_module_id, universes, type_expr):
    """Build a query from local syntax without knowing any remote symbol IDs."""
    return _derive(codec, owner_module_id, universes, type_expr)[0]
