"""Fixed congruence contracts; no module ID, candidate, fixture or file read.

The frozen owner-only formal_terms helper supplies named-binder lowering. Its
exact source is selected and pinned alongside this optional local-agent policy.
This is exact-contract discovery, not broad semantic search or proof authority.
"""
from formal_terms import _apply, _lower, _pi, _var


def contract(arity):
    if arity not in (2, 3):
        raise ValueError("TERMINAL_I_FIXED_CONGRUENCE_ARITY")
    types = ["A", "B", "C", "D"][:arity+1]
    arguments = ["a", "b", "c"][:arity]
    binders = [(name, ["sort", ["param", index]], "implicit")
               for index, name in enumerate(types)]
    function_type = _var(types[-1])
    for index, name in reversed(list(enumerate(types[:-1]))):
        function_type = _pi("_argument"+str(index), _var(name), function_type)
    binders.append(("f", function_type, "default"))
    for name, type_name in zip(arguments, types):
        binders.extend(((name, _var(type_name), "implicit"),
                        (name+"_next", _var(type_name), "implicit")))
    def equality(index, left, right):
        return _apply(["const", ["foundation", [["s", "Eq"]]], [["param", index]]],
                      _var(types[index]), left, right)
    for index, name in enumerate(arguments):
        binders.append(("h"+name, equality(index, _var(name), _var(name+"_next")), "default"))
    expression = equality(arity, _apply(_var("f"), *(_var(name) for name in arguments)),
                          _apply(_var("f"), *(_var(name+"_next") for name in arguments)))
    for name, domain, flag in reversed(binders):
        expression = _pi(name, domain, expression, flag)
    return _lower(expression)


def query(codec, arity):
    expression = contract(arity)
    codec.validate_expr(expression, arity+1)
    relocated = codec.relocate_expr(expression, "00"*32, arity+1)
    if relocated != codec.relocate_expr(expression, "ff"*32, arity+1):
        raise ValueError("TERMINAL_I_QUERY_LOCAL_REFERENCE")
    key = codec.hash_value("discovery-declared-type",
                           {"universes": arity+1, "type": relocated})
    return {"universes": arity+1, "type": expression,
            "specs": [{"tag": "declaration-kind", "value": "theorem"},
                      {"tag": "declared-type-key", "value": key}],
            "mathematical_acceptance": False, "global_complete": False}
