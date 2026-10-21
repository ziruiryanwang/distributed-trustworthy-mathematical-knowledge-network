"""Pure untrusted RC0 differential fixtures, not certificate production.

The original witness emitter is a native-test comparator only. Production RC0
does not reconstruct foundation/native rows. No filesystem or process access.
"""
from modules import codec as C
from modules.native_rows import NativeRows
from modules.receipt.witness import decode_journal

I_IMAGE = "9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e"
FIRST_NAME = [["s", "RC0"], ["s", "context_transport"]]
SECOND_NAME = [["s", "RC0"], ["s", "context_transport_then"]]
BC_NAME = [["s", "CommonsV5"], ["s", "binary_congr"]]


def var(scope, name):
    C.require(name in scope and len(set(scope)) == len(scope), "FIXTURE_SCOPE")
    return ["bvar", len(scope) - 1 - scope.index(name)]


def app(function, *arguments):
    for argument in arguments:
        function = ["app", function, argument]
    return function


def const(reference, *parameters):
    return ["const", reference, [["param", index] for index in parameters]]


def eq(scope, left, right):
    return app(const(["foundation", [["s", "Eq"]]], 3),
               var(scope, "D"), left, right)


def arrow(scope, arguments, result):
    if not arguments:
        return var(scope, result)
    temporary = "_arrow" + str(len(scope))
    return ["forall", "default", var(scope, arguments[0]),
            arrow(scope + [temporary], arguments[1:], result)]


def telescope(continuation=False):
    scope, entries = [], []

    def add(name, style, domain):
        C.require(name not in scope, "FIXTURE_BINDER_UNIQUE")
        entries.append((name, style, domain))
        scope.append(name)

    for parameter, name in enumerate(("A", "B", "C", "D")):
        add(name, "implicit", ["sort", ["param", parameter]])
    for name, arguments, result in (("f", ["B", "C"], "D"),
                                    ("g", ["A", "A"], "B"),
                                    ("h", ["A", "A"], "C")):
        add(name, "default", arrow(scope, arguments, result))
    for name in ("a", "aa", "b", "bb", "c", "cc"):
        add(name, "implicit", var(scope, "A"))
    for proof, left, right in (("ha", "a", "aa"), ("hb", "b", "bb"), ("hc", "c", "cc")):
        add(proof, "default", app(const(["foundation", [["s", "Eq"]]], 0),
            var(scope, "A"), var(scope, left), var(scope, right)))
    if continuation:
        add("d", "default", var(scope, "D"))
        _, middle = endpoints(scope)
        add("hd", "default", eq(scope, middle, var(scope, "d")))
    return scope, entries


def endpoints(scope):
    def v(name):
        return var(scope, name)
    return (app(v("f"), app(v("g"), v("a"), v("b")), app(v("h"), v("b"), v("c"))),
            app(v("f"), app(v("g"), v("aa"), v("bb")), app(v("h"), v("bb"), v("cc"))))


def close(tag, entries, body):
    for _, style, domain in reversed(entries):
        body = [tag, style, domain, body]
    return body


def frame(parent, opening, *, continuation=False):
    parsed = decode_journal(parent)
    C.require(parent[12:44].hex() == I_IMAGE, "FIXTURE_FIXED_I_IMAGE")
    group = C.verify_group_opening(parsed["module"], opening)
    C.require(opening["summary"] == parsed["summary"] and group["kind"] == "ordinary"
              and len(group["declarations"]) == 1, "FIXTURE_PARENT_GROUP")
    declaration = group["declarations"][0]
    expected_name = FIRST_NAME if continuation else BC_NAME
    C.require(declaration["kind"] == "theorem" and declaration["name"] == expected_name
              and declaration["universes"] == (4 if continuation else 3), "FIXTURE_PREMISE")
    scope, entries = telescope(continuation)
    left, middle = endpoints(scope)
    reference = ["external", parsed["module"], expected_name]

    def v(name):
        return var(scope, name)

    if not continuation:
        pg = app(const(reference, 0, 0, 1), v("A"), v("A"), v("B"), v("g"),
                 v("a"), v("aa"), v("b"), v("bb"), v("ha"), v("hb"))
        ph = app(const(reference, 0, 0, 2), v("A"), v("A"), v("C"), v("h"),
                 v("b"), v("bb"), v("c"), v("cc"), v("hb"), v("hc"))
        proof = app(const(reference, 1, 2, 3), v("B"), v("C"), v("D"), v("f"),
                    app(v("g"), v("a"), v("b")), app(v("g"), v("aa"), v("bb")),
                    app(v("h"), v("b"), v("c")), app(v("h"), v("bb"), v("cc")), pg, ph)
        proposition = eq(scope, left, middle)
    else:
        first_application = app(const(reference, 0, 1, 2, 3),
                                *(v(name) for name, _, _ in entries[:16]))
        proof = app(const(["foundation", [["s", "Eq"], ["s", "trans"]]], 3),
                    v("D"), left, middle, v("d"), first_application, v("hd"))
        proposition = eq(scope, left, v("d"))
    spec = {"schema": C.SPEC_SCHEMA, "foundation": parsed["foundation"], "policy": parsed["policy"],
            "groups": [{"kind": "ordinary", "declarations": [{
                "name": SECOND_NAME if continuation else FIRST_NAME, "kind": "theorem",
                "universes": 4, "type": close("forall", entries, proposition),
                "value_hash": None, "meta": {}}]}]}
    return {"schema": "DMKN_RESTRICTED_COMPOSITION_V1", "image": parsed["image"],
            "rank": parsed["rank"] + 1, "local_spec": spec,
            "parents": [{"journal": list(parent), "openings": [opening]}],
            "proofs": [close("lam", entries, proof)]}


def predicted_journal(value):
    """Untrusted byte prediction; neither verifies a proof nor makes a receipt."""
    summary = C.summarize(value["local_spec"])
    raw = b"DMKNM002" + (2).to_bytes(4, "little")
    raw += b"".join(C.uint(word).to_bytes(4, "little") for word in value["image"])
    for digest in (summary["foundation"], summary["policy"], C.summary_id(summary), summary["group_root"]):
        raw += bytes.fromhex(digest)
    raw += summary["group_count"].to_bytes(4, "little") + C.uint(value["rank"], 2**64-1).to_bytes(8, "little")
    C.require(len(raw) == 184, "FIXTURE_JOURNAL_SIZE")
    decode_journal(raw)
    return raw


def original_witness(value, foundation_rows):
    """Test-only constructive W, using the existing untrusted native-row codec."""
    emitter = NativeRows(foundation_rows)
    imported = {}
    for parent in value["parents"]:
        parsed = decode_journal(bytes(parent["journal"]))
        for opening in parent["openings"]:
            key = parsed["module"], opening["index"]
            C.require(key not in imported, "FIXTURE_DUPLICATE_GROUP")
            imported[key] = C.verify_group_opening(parsed["module"], opening)
    for (owner, _), group in sorted(imported.items()):
        C.require(group["kind"] == "ordinary" and len(group["declarations"]) == 1,
                  "FIXTURE_ORDINARY_IMPORT")
        declaration = group["declarations"][0]
        C.require(declaration["kind"] == "theorem", "FIXTURE_THEOREM_IMPORT")
        emitter._append({"moduleImportTheorem": emitter.header(owner, declaration)})
    owner = C.module_id(value["local_spec"])
    groups = value["local_spec"]["groups"]
    C.require(len(groups) == len(value["proofs"]), "FIXTURE_PROOF_COUNT")
    for group, proof in zip(groups, value["proofs"]):
        declaration = group["declarations"][0]
        header = emitter.header(owner, declaration)
        header["value"] = emitter.expression(owner, proof)
        header["all"] = [header["name"]]
        emitter._append({"thm": header})
    return {"schema": "DMKN_CERTIFIED_MODULES_V2", "image": value["image"],
            "rank": value["rank"], "local_spec": value["local_spec"], "rows": emitter.rows,
            "parents": value["parents"], "bodies": []}


def make_fixtures(parent_journal, binary_congr_opening, foundation_rows):
    first = frame(parent_journal, binary_congr_opening)
    second = frame(predicted_journal(first), C.group_opening(first["local_spec"], 0), continuation=True)
    return {"first": first, "second": second,
            "first_witness": original_witness(first, foundation_rows),
            "second_witness": original_witness(second, foundation_rows)}
