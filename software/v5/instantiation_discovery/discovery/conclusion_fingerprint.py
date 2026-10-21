"""Small substitution-stable conclusion filters, never a proof or unifier.

One source fingerprint and at most eight separately funded goal queries. Exact
symbol addresses remain significant; no reduction or semantic equivalence is
performed. Local contexts require an explicitly closed telescope wrapper.
"""
from __future__ import annotations

import json

from .type_pattern import _preflight

FINGERPRINT_PROFILE_SCHEMA = "DMKN_MODULE_EXPORT_CONCLUSION_FINGERPRINT_PROFILE_V1"
FINGERPRINT_TAG = "conclusion-fingerprint"
EDGES = frozenset(("fn", "arg", "domain", "body", "type", "value", "struct"))
SLOTS = {
    "app": {"fn": 1, "arg": 2},
    "forall": {"domain": 2, "body": 3},
    "lam": {"domain": 2, "body": 3},
    "let": {"type": 1, "value": 2, "body": 3},
    "proj": {"struct": 3}, "const": {}, "sort": {}, "bvar": {},
}


def _need(ok, code):
    if not ok:
        raise ValueError(code)


def _compact(value):
    # Only bounded profiles, tiny tokens/specs or hashes reach this helper.
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def validate_fingerprint_profile(profile):
    """Refuse noncanonical paths before any whole-value encoding or copying."""
    _need(type(profile) is dict and len(profile) == 2
          and "schema" in profile and "paths" in profile,
          "EXPORT_FINGERPRINT_PROFILE_FIELDS")
    _need(type(profile["schema"]) is str and profile["schema"] == FINGERPRINT_PROFILE_SCHEMA,
          "EXPORT_FINGERPRINT_PROFILE_SCHEMA")
    paths = profile["paths"]
    _need(type(paths) is list and 1 <= len(paths) <= 3,
          "EXPORT_FINGERPRINT_PROFILE_COUNT")
    for path in paths:
        _need(type(path) is list and len(path) <= 12, "EXPORT_FINGERPRINT_PATH_LENGTH")
        for edge in path:
            _need(type(edge) is str and len(edge) <= 6 and edge in EDGES,
                  "EXPORT_FINGERPRINT_PATH_EDGE")
    keys = [_compact(path) for path in paths]
    _need(keys == sorted(set(keys)), "EXPORT_FINGERPRINT_PATH_ORDER")
    return {"schema": FINGERPRINT_PROFILE_SCHEMA, "paths": [list(path) for path in paths]}


def _validated(codec, owner_module_id, universes, expression):
    _need(type(owner_module_id) is str and len(owner_module_id) == 64,
          "EXPORT_FINGERPRINT_OWNER")
    codec.digest_string(owner_module_id)
    codec.uint(universes, codec.DEFAULT_LIMITS.max_universes)
    work = _preflight(expression)
    # Public validate_expr has no local context argument and serializes before
    # walking. Preflight must therefore precede it, including for wrappers.
    codec.validate_expr(expression, universes)
    return work


def _symbol(codec, owner_module_id, ref):
    if ref[0] == "foundation":
        return {"kind": "foundation-name", "name_hash": codec.hash_value("foundation-symbol", ref[1])}
    module, name = (owner_module_id, ref[1]) if ref[0] == "local" else (ref[1], ref[2])
    return {"kind": "export", "export_id": codec.export_id(module, name)}


def _observe(codec, owner_module_id, expression, path, *, parameters=0, context=0):
    """Return a token and visited-position count; input is already validated."""
    current, q, work = expression, 0, 0
    for position in range(len(path)+1):
        work += 1
        tag = current[0]
        variable = None
        if tag == "bvar":
            index = current[1]
            if index < q:
                variable = ["local", index]
            elif index < q+parameters:
                # A parameter can acquire children after substitution. STAR
                # must win before missing-child handling at every position.
                return ["star"], work
            elif index < q+context:
                variable = ["context", index-q]
            else:
                raise ValueError("EXPORT_FINGERPRINT_VARIABLE_SCOPE")
        if position == len(path):
            if variable is not None:
                return variable, work
            if tag == "const":
                return ["const", _symbol(codec, owner_module_id, current[1])], work
            return ["node", tag], work
        edge = path[position]
        child = SLOTS[tag].get(edge)
        if child is None:
            return ["absent"], work
        if edge == "body" and tag in ("forall", "lam", "let"):
            q += 1
        current = current[child]
    raise AssertionError("UNREACHABLE_FINGERPRINT_POSITION")


def _spec(codec, profile_id, vector):
    return {"tag": FINGERPRINT_TAG, "profile_id": profile_id,
            "value": codec.hash_value("conclusion-fingerprint-v1",
                                      {"profile_id": profile_id, "tokens": vector})}


def _derive_conclusion(codec, owner_module_id, universes, declaration_type, profile):
    selected = validate_fingerprint_profile(profile)
    work = _validated(codec, owner_module_id, universes, declaration_type)
    conclusion, k = declaration_type, 0
    while conclusion[0] == "forall":
        k += 1
        work += 1
        conclusion = conclusion[3]
    vector = []
    for path in selected["paths"]:
        token, visited = _observe(codec, owner_module_id, conclusion, path, parameters=k)
        vector.append(token)
        work += visited
    pid = codec.hash_value("conclusion-fingerprint-profile-v1", selected)
    return _spec(codec, pid, vector), work


def conclusion_spec(codec, owner_module_id, universes, declaration_type, profile):
    """One source feature; structural syntax validation is not mathematics."""
    return _derive_conclusion(codec, owner_module_id, universes, declaration_type, profile)[0]


def goal_queries(codec, owner_module_id, universes, closed_goal, profile, *, context_binders=0):
    """Return singleton query alternatives, not an AND over all alternatives.

    For context_binders=n, closed_goal must encode the complete closed Pi Gamma.g
    wrapper. Strip exactly n validated leading foralls; the remaining quantifiers
    belong to the goal. The caller funds and orders actual adaptive queries.
    """
    codec.uint(context_binders, codec.DEFAULT_LIMITS.max_depth)
    selected = validate_fingerprint_profile(profile)
    _validated(codec, owner_module_id, universes, closed_goal)
    goal = closed_goal
    for _ in range(context_binders):
        _need(goal[0] == "forall", "EXPORT_FINGERPRINT_CONTEXT_TELESCOPE")
        goal = goal[3]
    vector = [_observe(codec, owner_module_id, goal, path, context=context_binders)[0]
              for path in selected["paths"]]
    # No source vector contains CONTEXT: its outer parameters always yield
    # STAR. Retaining a final CONTEXT coordinate would query an impossible key.
    varying = [i for i, token in enumerate(vector) if token[0] != "context"]
    base = [["star"] if token[0] == "context" else token for token in vector]
    pid = codec.hash_value("conclusion-fingerprint-profile-v1", selected)
    queries = {}
    for mask in range(1 << len(varying)):
        choice = list(base)
        for bit, index in enumerate(varying):
            if mask & (1 << bit):
                choice[index] = ["star"]
        spec = _spec(codec, pid, choice)
        queries[_compact(spec)] = [spec]
    return [queries[key] for key in sorted(queries)]
