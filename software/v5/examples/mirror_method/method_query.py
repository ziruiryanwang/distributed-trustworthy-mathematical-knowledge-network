"""Local formal contract queries; no candidate IDs, packet reads or authority.

The caller supplies its already known Tree module and adopted codec. The two
fixed alternatives accommodate declaration universe-parameter order, not answer
feedback. Each alternative must consume the caller's original query allowance.
"""
from copy import deepcopy


def _name(*parts):
    return [["s", part] for part in parts]


def _var(name):
    return ["var", name]


def _apply(function, *arguments):
    for argument in arguments:
        function = ["app", function, argument]
    return function


def _pi(name, domain, body, flag="default"):
    return ["pi", name, flag, domain, body]


def _lower(expression, context=()):
    tag = expression[0]
    if tag == "var":
        if expression[1] not in context:
            raise ValueError("METHOD_QUERY_FREE_VARIABLE")
        return ["bvar", context.index(expression[1])]
    if tag == "pi":
        _, name, flag, domain, body = expression
        return ["forall", flag, _lower(domain, context),
                _lower(body, (name, *context))]
    if tag == "app":
        return [tag, _lower(expression[1], context), _lower(expression[2], context)]
    if tag in ("sort", "const"):
        return deepcopy(expression)
    raise ValueError("METHOD_QUERY_EXPRESSION")


def _contract(base_module, u_index, v_index):
    u, v = ["param", u_index], ["param", v_index]
    a, b = _var("A"), _var("B")
    def tree_constant(suffix):
        return ["const", ["external", base_module,
                          _name("CommonsV5", "Tree", *suffix)], [u]]
    tree = _apply(tree_constant(()), a)
    def leaf(x):
        return _apply(tree_constant(("leaf",)), a, x)
    def node(left, right):
        return _apply(tree_constant(("node",)), a, left, right)
    def eq(left, right):
        return _apply(["const", ["foundation", _name("Eq")], [["succ", v]]],
                      b, left, right)
    l, n, h, k = (_var(key) for key in ("L", "N", "h", "k"))
    x, left, right, t = (_var(key) for key in ("x", "left", "right", "t"))
    def leaf_equation(function):
        return _pi("x", a, eq(_apply(function, leaf(x)), _apply(l, x)))
    def node_equation(function):
        return _pi("left", tree, _pi("right", tree,
            eq(_apply(function, node(left, right)),
               _apply(n, _apply(function, left), _apply(function, right)))))
    binders = [
        ("A", ["sort", ["succ", u]], "implicit"),
        ("B", ["sort", ["succ", v]], "implicit"),
        ("L", _pi("_Larg", a, b), "default"),
        ("N", _pi("_Narg1", b, _pi("_Narg2", b, b)), "default"),
        ("h", _pi("_harg", tree, b), "default"),
        ("k", _pi("_karg", tree, b), "default"),
        ("h_leaf", leaf_equation(h), "default"),
        ("h_node", node_equation(h), "default"),
        ("k_leaf", leaf_equation(k), "default"),
        ("k_node", node_equation(k), "default"),
        ("t", tree, "default"),
    ]
    expression = eq(_apply(h, t), _apply(k, t))
    for name, domain, flag in reversed(binders):
        expression = _pi(name, domain, expression, flag)
    return _lower(expression)


def method_queries(codec, base_module):
    """Two bounded, answer-independent exact-contract alternatives.

    These keys express the local agent's chosen formal contract. They neither
    certify that a provider contains a match nor admit returned mathematics.
    The caller must not treat an exhausted first query as permission to renew
    an envelope; any second alternative is reserved prospectively.
    """
    codec.digest_string(base_module)
    result = []
    for u_index, v_index in ((0, 1), (1, 0)):
        expression = _contract(base_module, u_index, v_index)
        codec.validate_expr(expression, 2)
        # The constructor emits foundation/external refs only. Independence
        # from the arbitrary owner is checked, not inferred from a type hash.
        relocated = codec.relocate_expr(expression, "00" * 32, 2)
        if relocated != codec.relocate_expr(expression, "ff" * 32, 2):
            raise ValueError("METHOD_QUERY_ANSWER_LOCAL_REFERENCE")
        key = codec.hash_value("discovery-declared-type",
                               {"universes": 2, "type": relocated})
        result.append({"universes": 2, "type": expression,
            "universe_order": {"u": u_index, "v": v_index},
            "specs": [{"tag": "declaration-kind", "value": "theorem"},
                      {"tag": "declared-type-key", "value": key}],
            "mathematical_acceptance": False, "global_complete": False})
    return result
