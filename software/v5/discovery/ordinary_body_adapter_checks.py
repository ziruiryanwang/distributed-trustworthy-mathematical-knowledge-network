"""Finite metadata-only body/preview discovery controls; NOT runtime permission.

The initial local property is constructed before reading publisher evidence.
The two retained inputs are exact-hash selected by the caller. Decoys are
syntactic, unproved metadata. Two fresh real Stores and their SQLite files are
retained below --store-root. No Lean, catalog acceptance, sockets or subprocesses.
"""
from pathlib import Path
import argparse
from copy import deepcopy
from dataclasses import replace
import hashlib
import json
import sys
import time

sys.dont_write_bytecode = True
V5 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(V5))
sys.path.insert(0, str(V5 / "ordinary_lean"))
from discovery import formal_features as F
from discovery import authenticated_index as A
from discovery import discovery_query as Q
from discovery import ordinary_body_adapter as B
from discovery import ordinary_export_adapter as O
from discovery.discovery_store import Store, ordinary
import ordinary_evidence as E
import ordinary_semantics as S
import portable_evidence as PE
import portable_preview as PP


STORE_LIMITS = dict(max_objects=16, max_postings=4096, max_features=4096,
                    max_snapshots=32, max_logical_bytes=16777216, max_db_pages=8192)
PAGE_LIMITS = dict(examined=32, matches=8, bytes=65536, timeout_ms=1000,
                   node_reads=100000)
PATHS = [["body", "body", "arg", "arg"], ["body", "body", "arg"],
         ["body", "domain", "arg"]]
EXPECTED_TOKENS = [["local", 1], ["node", "app"], ["local", 0]]
PARAMS = [[[0, {"$bytes": [117]}]]]
MIB = 1024**2


def ensure(ok, code):
    if not ok:
        raise AssertionError(code)


def refuses(marker, action):
    try:
        action()
    except ValueError as exc:
        ensure(marker in str(exc), "WRONG_REFUSAL:" + str(exc))
    else:
        raise AssertionError("MISSING_REFUSAL:" + marker)


def report(label, **details):
    print("ORDINARY_BODY_CHECK " + label + " PASS " + json.dumps(
        details, sort_keys=True, separators=(",", ":")), flush=True)


def key(label):
    return hashlib.sha256(label.encode("ascii")).hexdigest()


def name(label):
    return [[0, {"$bytes": list(label.encode("ascii"))}]]


def v(label): return ("var", label)
def app(fn, arg): return ("app", fn, arg)
def pi(label, domain, body): return ("forall", label, domain, body)
def lam(label, domain, body): return ("lambda", label, domain, body)
def const(label): return ("const", label)
PROP, SORT_U = ("sort", 1), ("sort", 0)


def packet(tree):
    """Tiny independent test AST encoder; never reads publisher syntax/keys."""
    nodes, memo = [], {}

    def visit(expr, scope):
        tag = expr[0]
        if tag == "var":
            node = [0, scope.index(expr[1])]
        elif tag == "sort":
            node = [1, expr[1]]
        elif tag == "const":
            node = [2, name(expr[1]), []]
        elif tag == "app":
            node = [3, visit(expr[1], scope), visit(expr[2], scope)]
        else:
            ensure(tag in ("forall", "lambda"), "FIXTURE_AST_TAG")
            node = [5 if tag == "forall" else 4, name(expr[1]), 0,
                    visit(expr[2], scope), visit(expr[3], (expr[1], *scope))]
        encoded = E.canonical_json(node)
        if encoded not in memo:
            memo[encoded] = len(nodes)
            nodes.append(node)
        return memo[encoded]

    root = visit(tree, ())
    ensure(root == len(nodes)-1, "FIXTURE_ROOT")
    return [E.EXPR_FORMAT, [[4, 0], [0]], nodes, root]


def property_tree(variant="preserve", *, source=False, suffix=""):
    """Local hf property: forall x, predicate x -> predicate (step x).

    All lexical variables are local. Remote names/IDs are not arguments. The
    query and publisher fixtures use different binder names and encodings.
    """
    a, f, p, q, x, h = [item+suffix for item in
                         ("carrier", "step", "predicate", "other", "witness", "premise")]
    av, fv, pv, qv, xv = map(v, (a, f, p, q, x))
    fx, px = app(fv, xv), app(pv, xv)
    left, right = px, app(pv, fx)
    if variant == "collision": right = app(qv, fx)
    elif variant == "reflexive": right = px
    elif variant == "composite": right = app(pv, app(fv, fx))
    elif variant == "stronger_premise": left = app(pv, fx)
    elif variant == "sort_conclusion": right = PROP
    body = pi(x, av, pi(h, left, right))
    if variant == "one_quantifier": body = pi(x, av, right)
    elif variant == "no_quantifier": body = PROP
    wrap = lam if source else pi
    if variant == "collision":
        body = wrap(q, pi("other_arg"+suffix, av, PROP), body)
    body = wrap(p, pi("predicate_arg"+suffix, av, PROP), body)
    body = wrap(f, pi("step_arg"+suffix, av, av), body)
    return wrap(a, SORT_U, body)


def definition(semantic, label, body, bindings=()):
    own, typ, value = name(label), packet(PROP), packet(body)
    hints, all_names = [2, 1], [own]
    descriptor = [0, own, PARAMS, typ, value, hints, all_names]
    row = [own, 1, PARAMS, typ, [value, hints, all_names]]
    return E.canonical_json({"schema": PE.SCHEMA, "semantic_id": semantic,
        "imports": sorted(deepcopy(list(bindings)), key=lambda row: E.name_key(row[0])),
        "unit": [E.UNIT_FORMAT, descriptor, [row]]})


def query(adapter, tree, *, context=3, bindings=()):
    return adapter.goal_queries(expression=packet(tree), universe_params=deepcopy(PARAMS),
                                bindings=deepcopy(list(bindings)), context_binders=context)


def reference_alternatives():
    """Independent expected order from the chosen local trace, not a record."""
    profile_id = F.digest("DMKN-ORDINARY-BODY-PROFILE-V1", {
        "schema": "DMKN_ORDINARY_DEFINITION_BODY_PROFILE_V1", "paths": PATHS})
    alternatives = []
    for mask in range(8):
        tokens = [["star"] if mask & (1 << i) else token
                  for i, token in enumerate(EXPECTED_TOKENS)]
        spec = {"tag": "definition-body-fingerprint", "profile_id": profile_id,
                "value": F.digest("DMKN-ORDINARY-BODY-FINGERPRINT-V1", {
                    "profile_id": profile_id, "tokens": tokens})}
        alternatives.append((mask.bit_count(), F.compact(spec), [spec]))
    return [item[2] for item in sorted(alternatives)]


def read_selected(path, expected_sha):
    selected = ordinary(Path(path), directory=False)
    F.hexid(expected_sha)
    ensure(selected.stat().st_size <= MIB, "INPUT_BYTE_CAP")
    with selected.open("rb") as stream:
        raw = stream.read(MIB+1)
    ensure(0 < len(raw) <= MIB and hashlib.sha256(raw).hexdigest() == expected_sha,
           "INPUT_EXACT_HASH")
    return raw


def retained_and_scope(adapter, alternatives, raw, method_raw):
    described = adapter.describe(raw)
    record = described["record"]
    ensure(B.profile()["paths"] == PATHS and PATHS == sorted(PATHS, key=F.compact),
           "FIXED_CANONICAL_PATH_PROFILE")
    ensure(described["observations"] == EXPECTED_TOKENS and
           described["source_lambdas"] == 3 and described["path_visits"] == 13 and
           described["work"] == described["total_unit_nodes"]+16 and
           described["mathematical_acceptance"] is False, "RETAINED_TRACE_OR_WORK")
    compiled = [adapter.compile_query(specs) for specs in alternatives]
    ensure(len(alternatives) == len({F.compact(x) for x in alternatives}) == 8 and
           record["features"] == compiled[0] and alternatives == reference_alternatives(),
           "INDEPENDENT_LOCAL_PREMISE_RECALL_AND_SPECIFICITY_ORDER")
    ensure(alternatives == query(adapter, property_tree(suffix="_renamed")),
           "BINDER_RENAMING_CHANGED_QUERY")
    for context in (0, 5):
        wrong = query(adapter, property_tree(), context=context)
        ensure(record["features"] not in [adapter.compile_query(x) for x in wrong],
               "CONTEXT_INTERNAL_BINDER_CONFUSION")
    refuses("ORDINARY_BODY_QUERY_CONTEXT_TELESCOPE",
            lambda: query(adapter, property_tree(), context=6))
    composite = query(adapter, property_tree("composite"))
    ensure(record["features"] not in [adapter.compile_query(x) for x in composite],
           "RAW_REDUCED_COMPOSITE_GOAL_OVERCLAIM")
    wildcard = definition(adapter.semantic_id, "Wildcard", lam("T", PROP, v("T")))
    star = adapter.describe(wildcard)
    local_star = query(adapter, pi("T", PROP, v("T")), context=1)
    ensure(star["observations"] == [["star"]]*3 and star["path_visits"] == 3 and
           len(local_star) == 8 and adapter.compile_query(local_star[-1]) == star["record"]["features"],
           "SOURCE_STAR_PRECEDES_MISSING_CHILD_QUERY_CONTEXT_BEFORE_ENDPOINT_IS_ABSENT")
    # Context at a final coordinate is mandatory STAR; context before an
    # unfinished path gives ABSENT and only optionally STAR. Keep them distinct.
    applied = app(v("Q"), v("t"))
    inner = pi("x", PROP, pi("h", applied, applied))
    context_property = pi("Q", pi("z", PROP, PROP), pi("t", PROP, inner))
    context_queries = query(adapter, context_property, context=2)
    ensure(len(context_queries) == 2 and
           adapter.compile_query(context_queries[-1]) == star["record"]["features"],
           "FINAL_CONTEXT_COORDINATES_NOT_FORCED_TO_STAR")
    refuses("ORDINARY_BODY_SINGLE_DEFINITION", lambda: adapter.extract(method_raw))
    report("retained_trace_local_scope_and_raw_instance_limit",
           alternatives=len(alternatives), total_unit_nodes=described["total_unit_nodes"],
           path_visits=described["path_visits"], work=described["work"])
    return record


def binding_and_bounds(adapter, raw, record):
    original = PE.read_evidence(raw)
    # Each mismatch remains separately syntactically valid, so equality cannot
    # be delegated to a later native roundtrip or hidden behind a parse failure.
    for field in ("params", "type", "body", "hints", "all_names", "kind"):
        doc = deepcopy(original.document)
        row = doc["unit"][2][0]
        if field == "params": row[2] = [name("different_universe")]
        elif field == "type": row[3] = packet(PROP)
        elif field == "body": row[4][0] = packet(PROP)
        elif field == "hints": row[4][1] = [2, 2]
        elif field == "all_names": row[4][2].append(name("InventedGroupMember"))
        else:
            row[1] = 2
            row[4] = [row[4][0], row[4][2]]
        altered = E.canonical_json(doc)
        PE.read_evidence(altered)
        marker = "ORDINARY_BODY_SINGLE_DEFINITION" if field == "kind" else "ORDINARY_BODY_DESCRIPTOR_INVENTORY"
        refuses(marker, lambda altered=altered: adapter.extract(altered))
    doc = deepcopy(original.document)
    doc["unit"][2][0][0] = name("WrongInventoryName")
    refuses("ORDINARY_INVENTORY_CENSUS", lambda: adapter.extract(E.canonical_json(doc)))
    doc = deepcopy(original.document)
    doc["unit"][2].append(deepcopy(doc["unit"][2][0]))
    refuses("ARRAY_BOUND", lambda: adapter.extract(E.canonical_json(doc)))
    doc = deepcopy(original.document)
    doc["unit"][1][6].append(name("UnexpectedGroupMember"))
    doc["unit"][2][0][4][2] = deepcopy(doc["unit"][1][6])
    refuses("ORDINARY_BODY_DESCRIPTOR_INVENTORY", lambda: adapter.extract(E.canonical_json(doc)))
    doc = deepcopy(original.document)
    desc, row = doc["unit"][1], doc["unit"][2][0]
    doc["unit"][1] = [2, *desc[1:5], desc[6]]
    row[1], row[4] = 3, [row[4][0], 0, row[4][2]]
    refuses("ORDINARY_BODY_SINGLE_DEFINITION", lambda: adapter.extract(E.canonical_json(doc)))
    refuses("JSON_LEXICAL_TOKEN", lambda: adapter.extract(raw+b" "))
    refuses("ORDINARY_BODY_EXPORT_BINDING", lambda: adapter.extract(raw, expected_id=key("wrong")))
    for field in ("object_sha256", "object_bytes", "features"):
        bad = deepcopy(record)
        bad[field] = record[field]+1 if field == "object_bytes" else (
            [key("wrong-feature")] if field == "features" else key("wrong-bytes"))
        refuses("ORDINARY_BODY_EVIDENCE_RECORD_BINDING", lambda bad=bad: adapter.resolve(bad, raw))
    for field in ("unit_id", "export_name", "semantic_id"):
        bad = deepcopy(record)
        bad["locator"][field] = name("wrong-name") if field == "export_name" else key("wrong-locator")
        marker = "ORDINARY_BODY_RECORD_NAMESPACE" if field == "semantic_id" else "ORDINARY_BODY_RECORD_EXPORT"
        refuses(marker, lambda bad=bad: adapter.resolve(bad, raw))
    wrong = deepcopy(original.document)
    wrong["semantic_id"] = key("unsupported")
    refuses("ORDINARY_BODY_EVIDENCE_SEMANTICS", lambda: adapter.extract(E.canonical_json(wrong)))
    refuses("ORDINARY_BODY_SEMANTICS_NOT_SELECTED", lambda: B.OrdinaryBodyAdapter(key("unsupported")))
    for limits, marker in (
        (replace(adapter.limits, max_bytes=len(raw)-1), "JSON_BYTE_BOUND"),
        (replace(adapter.limits, max_unit_nodes=original.census.total_nodes-1), "UNIT_NODE_BOUND"),
        (replace(adapter.limits, max_exprs=1), "ARRAY_BOUND"),
        (replace(adapter.limits, max_dag_depth=1), "DAG_DEPTH_BOUND")):
        small = B.OrdinaryBodyAdapter(adapter.semantic_id, limits=limits)
        refuses(marker, lambda small=small: small.extract(raw))
    ensure(adapter.limits.max_bytes == MIB and adapter.limits.max_inventory == 1,
           "EXPLICIT_TIGHT_DEFAULTS")
    refuses("ORDINARY_BODY_LIMITS_NOT_STRICTER", lambda: B.OrdinaryBodyAdapter(
        adapter.semantic_id, limits=replace(adapter.limits, max_bytes=MIB+1)))
    for context in (-1, True, adapter.limits.max_dag_depth+1):
        marker = "INTEGER_BOUND" if type(context) is int and context > 0 else "ORDINARY_BODY_QUERY_PREFLIGHT_"
        refuses(marker, lambda context=context: query(adapter, property_tree(), context=context))
    shallow = B.OrdinaryBodyAdapter(adapter.semantic_id,
                                   limits=replace(adapter.limits, max_bytes=128))
    refuses("ORDINARY_BODY_QUERY_PREFLIGHT_", lambda: query(shallow, property_tree()))
    cycle = []
    cycle.append(cycle)
    refuses("ORDINARY_BODY_QUERY_PREFLIGHT_WORK", lambda: adapter.goal_queries(
        expression=cycle, universe_params=[], bindings=[]))
    shared_python = []
    for _ in range(16):
        shared_python = [shared_python, shared_python]
    tighter = B.OrdinaryBodyAdapter(adapter.semantic_id,
                                   limits=replace(adapter.limits, max_bytes=512))
    refuses("ORDINARY_BODY_QUERY_PREFLIGHT_", lambda: tighter.goal_queries(
        expression=shared_python, universe_params=[], bindings=[]))
    preview = PP.preview_from_evidence(raw, record["locator"]["export_name"])
    refuses("PORTABLE_EVIDENCE_FIELDS", lambda: adapter.extract(preview))
    other = O.OrdinaryExportAdapter(adapter.semantic_id)
    refuses("PORTABLE_PREVIEW_FIELDS", lambda: other.extract(raw))
    ensure(other.namespace != adapter.namespace and record["object_sha256"] == hashlib.sha256(raw).hexdigest()
           and record["object_bytes"] == len(raw), "FULL_EVIDENCE_NOT_PREVIEW_NAMESPACE")
    old_record = other.extract(preview)
    encoded = json.dumps(old_record, sort_keys=True, ensure_ascii=False,
                         separators=(",", ":"), allow_nan=False).encode("utf-8")
    ensure(old_record["schema"] == "DMKN_FORMAL_FEATURE_RECORD_V3" and
           F.record_id(old_record) == hashlib.sha256(b"DMKN-FORMAL-FEATURE-RECORD-V3\0"+encoded).hexdigest()
           and other.resolve(old_record, preview)["mathematical_acceptance"] is False,
           "V3_RECORD_DOMAIN_OR_RESOLUTION_CHANGED")
    bad = deepcopy(record)
    bad["schema"] = "DMKN_FORMAL_FEATURE_RECORD_V3"
    refuses("ORDINARY_RECORD_KIND", lambda: F.validate_record(bad))
    bad = deepcopy(record)
    bad["namespace"] = other.namespace
    refuses("ORDINARY_BODY_RECORD_NAMESPACE", lambda: F.validate_record(bad))
    refuses("RECORD_NAMESPACE", lambda: other.resolve(record, raw))
    report("descriptor_inventory_full_bytes_kinds_and_bounds")


def constants_and_shared_dag(adapter):
    bindings = [[name(label), key("symbol:"+label)] for label in ("Predicate", "Argument")]
    bindings.sort(key=lambda row: E.name_key(row[0]))
    expr = app(const("Predicate"), const("Argument"))
    body = pi("x", SORT_U, pi("h", expr, expr))
    raw = definition(adapter.semantic_id, "ConstantPaths", body, bindings)
    record = adapter.extract(raw)
    alternatives = query(adapter, body, context=0, bindings=bindings)
    ensure(record["features"] in [adapter.compile_query(x) for x in alternatives], "EXACT_CONSTANT_RECALL")
    changed = deepcopy(bindings)
    next(row for row in changed if row[0] == name("Argument"))[1] = key("different-argument")
    ensure(record["features"] not in [adapter.compile_query(x) for x in
           query(adapter, body, context=0, bindings=changed)], "PORTABLE_CONSTANT_ID_IGNORED")
    for bad in (bindings[:-1], [*bindings, [name("Unused"), key("unused")]], list(reversed(bindings))):
        refuses("ORDINARY_BODY_QUERY_BINDING_CENSUS",
                lambda bad=bad: query(adapter, body, context=0, bindings=bad))
    doc = PE.read_evidence(raw).document
    doc["imports"].pop()
    refuses("PORTABLE_IMPORT_CENSUS_OR_ORDER", lambda: adapter.extract(E.canonical_json(doc)))
    # The ordinary DAG can represent an exponentially expanded application tree
    # in a few nodes. Construct this packet directly; do not expand that tree.
    dag = [E.EXPR_FORMAT, [[0]], [[1, 0]], 0]
    for _ in range(80):
        prior = len(dag[2])-1
        dag[2].append([3, prior, prior])
    dag[3] = len(dag[2])-1
    doc = PE.read_evidence(definition(adapter.semantic_id, "SharedDAG", PROP)).document
    doc["unit"][1][4] = dag
    doc["unit"][2][0][4][0] = deepcopy(dag)
    shared = adapter.describe(E.canonical_json(doc))
    ensure(shared["body_nodes"] == 82 and shared["path_visits"] == 3 and
           shared["work"] == shared["total_unit_nodes"]+3, "DAG_OCCURRENCE_EXPANSION")
    report("exact_constants_import_census_and_shared_dag", body_nodes=shared["body_nodes"],
           total_unit_nodes=shared["total_unit_nodes"], work=shared["work"])


class Ledger:
    """One local-test envelope, not a substitute for OrdinaryBudget transport."""
    def __init__(self):
        self.deadline = time.monotonic()+120
        self.requests, self.reply_bytes, self.buckets = 0, 0, {}

    def check(self):
        ensure(time.monotonic() < self.deadline, "ORIGINAL_CHECK_DEADLINE")

    def call(self, bucket, action):
        self.check()
        ensure(self.requests < 64, "AGGREGATE_REQUEST_CAP")
        self.requests += 1
        counts = self.buckets.setdefault(bucket, {"requests": 0, "reply_bytes": 0, "examined": 0})
        counts["requests"] += 1
        result = action()
        raw = result if type(result) is bytes else F.compact(result)
        self.reply_bytes += len(raw)
        counts["reply_bytes"] += len(raw)
        ensure(self.reply_bytes <= 8*MIB, "AGGREGATE_REPLY_CAP")
        self.check()
        return result


def search(store, features, ledger, bucket):
    sid = store.status()["latest"]
    response = ledger.call(bucket, lambda: store.summary(sid, features))
    summary = Q.verify_summary(sid, store.namespace, features, response)
    found = []
    for plan in Q.plan_partitions(summary):
        if plan["committed_empty"]:
            continue
        request = {"schema": "DMKN_FORMAL_QUERY_REQUEST_V1", "namespace": store.namespace,
                   "snapshot_id": sid, "features": features, "partition": plan["partition"],
                   "anchor": plan["anchor"], "start": 0, "limits": dict(PAGE_LIMITS)}
        response = ledger.call(bucket, lambda: store.page(request))
        verified = Q.verify_page(summary, request, response)
        ensure(verified["termination"] == "anchor_exhausted" and
               verified["mathematical_acceptance"] is False, "QUERY_BOUNDED_EXHAUSTION")
        ledger.buckets[bucket]["examined"] += len(response["examined"])
        found.extend(verified["matches"])
    return found


def type_preview(semantic, label, symbol, *, kind=2):
    # Unproved publisher metadata; never feeds the consumer's initial property.
    own = name(label)
    symbol_name = name("ReferencedVocabulary")
    # forall h : (forall x : C, C), C. C occurs in reachable domain/result
    # syntax. All theorem decoys satisfy the ACTUAL predecessor broad filter:
    # theorem AND binder-domain-head(forallE), not merely all-theorems.
    nodes = [[2, symbol_name, []], [5, name("x"), 0, 0, 0],
             [5, name("h"), 0, 1, 0]]
    return E.canonical_json({"schema": PP.SCHEMA, "semantic_id": semantic,
        "unit_id": key("synthetic-unit:"+label), "export_name": own,
        "header": [kind, [], [E.EXPR_FORMAT, [], nodes, 2]],
        "type_bindings": [[symbol_name, symbol]]})


def integration(root, adapter, alternatives, raw, method_raw, ledger):
    ordinary(root, fresh=True).mkdir()
    methods = O.OrdinaryExportAdapter(adapter.semantic_id)
    body_store = Store(root/"body-index", adapter, STORE_LIMITS, create=True)
    method_store = None
    try:
        method_store = Store(root/"method-index", methods, STORE_LIMITS, create=True)
        bodies, previews, records = {}, {}, []
        corpus = [raw]
        variants = ("collision", "reflexive", "composite", "stronger_premise",
                    "sort_conclusion", "one_quantifier", "no_quantifier")
        corpus += [definition(adapter.semantic_id, "Fixture_"+variant,
                   property_tree(variant, source=True, suffix="_publisher")) for variant in variants]
        corpus.append(definition(adapter.semantic_id, "WildcardAlias", lam("T", PROP, v("T"))))
        for item in corpus:
            ledger.check()
            admitted = body_store.admit(item)
            ensure(admitted["new"] and admitted["mathematical_acceptance"] is False,
                   "BODY_METADATA_ADMISSION")
            record = admitted["record"]
            records.append(record)
            bodies[record["object_id"]] = item
        actual_method = PE.read_evidence(method_raw)
        method_name = actual_method.document["unit"][2][0][0]
        method_preview = PP.preview_from_evidence(method_raw, method_name)
        actual_preview_record = methods.extract(method_preview)
        method_corpus = [method_preview]
        method_corpus += [type_preview(adapter.semantic_id, "UnrelatedTheorem"+str(i), key("unrelated"+str(i)))
                          for i in range(7)]
        method_corpus.append(type_preview(adapter.semantic_id, "DefinitionWithVocabulary",
                                          records[0]["object_id"], kind=1))
        for item in method_corpus:
            ledger.check()
            admitted = method_store.admit(item)
            ensure(admitted["new"] and admitted["mathematical_acceptance"] is False,
                   "METHOD_METADATA_ADMISSION")
            previews[admitted["record"]["object_id"]] = item
        old_snapshot = method_store.snapshot()
        encoded = json.dumps(old_snapshot, sort_keys=True, ensure_ascii=False,
                             separators=(",", ":"), allow_nan=False).encode("utf-8")
        ensure(old_snapshot["feature_schema"] == "DMKN_ORDINARY_LEAN_EXPORT_FEATURES_V1" and
               A.snapshot_id(old_snapshot) == hashlib.sha256(b"DMKN-FORMAL-INDEX-SNAPSHOT-V1\0"+encoded).hexdigest(),
               "EXISTING_PREVIEW_SNAPSHOT_DOMAIN_CHANGED")
        before = body_store.snapshot()
        ensure(not body_store.admit(raw)["new"] and body_store.snapshot() == before,
               "BODY_IDEMPOTENCE_CHANGED_SNAPSHOT")
        # Choose only the most-specific query, as fixed before publisher reads.
        # STAR alternatives were checked separately and are not broadcast. In
        # particular, the all-STAR alias is not an excuse for a free hot-key scan.
        # No expected ID selects the partition or anchor in this consumer path.
        candidates = {}
        for specs in alternatives[:1]:
            for record in search(body_store, adapter.compile_query(specs), ledger, "stage1"):
                candidates[record["object_id"]] = record
        ensure(set(candidates) == {records[0]["object_id"], records[1]["object_id"]},
               "DIVERSE_DECOYS_OR_INTENTIONAL_COLLISION")
        all_methods, empty_method_searches, candidate_ids = {}, 0, []
        for record in candidates.values():
            acquired = ledger.call("definition_evidence", lambda: bodies[record["object_id"]])
            resolved = adapter.resolve(record, acquired)
            ensure(resolved["mathematical_acceptance"] is False and
                   resolved["assurance"] == "EXACT_DEFINITION_EVIDENCE_FEATURES_NOT_MATHEMATICAL_ACCEPTANCE",
                   "BODY_RESOLUTION_AUTHORITY")
            # The only exact symbol entering stage two is learned here, from
            # actual stage-one membership plus fetched full-evidence binding.
            learned = resolved["export_id"]
            candidate_ids.append(learned)
            features = O.compile_query(methods.namespace, [
                {"tag": "declaration-kind", "value": "theorem"},
                {"tag": "type-symbol", "symbol": {"kind": "portable-symbol", "symbol_id": learned}}])
            matches = search(method_store, features, ledger, "stage2")
            empty_method_searches += not matches
            for candidate in matches:
                fetched = ledger.call("method_preview", lambda: previews[candidate["object_id"]])
                resolution = methods.resolve(candidate, fetched)
                ensure(resolution["mathematical_acceptance"] is False, "METHOD_RESOLUTION_AUTHORITY")
                all_methods[candidate["object_id"]] = candidate
        ensure(list(all_methods.values()) == [actual_preview_record] and empty_method_searches == 1,
               "TWO_STAGE_UNKNOWN_ID_METHOD_OR_FALSE_CANDIDATE")
        # Bind the already retained theorem bytes as an inert final cross-check;
        # this is not replay, new admission, or an inferred mathematical warrant.
        acquired_method = ledger.call("method_evidence", lambda: method_raw)
        PP.resolve(method_preview, acquired_method)
        broad = search(method_store, O.compile_query(methods.namespace, [
            {"tag": "declaration-kind", "value": "theorem"},
            {"tag": "binder-domain-head", "head": {"tag": "forallE"}}]), ledger, "broad_comparator")
        ensure(len(broad) == 8, "BROAD_COMPARATOR_CENSUS")
        staged_examined = ledger.buckets["stage1"]["examined"]+ledger.buckets["stage2"]["examined"]
        ensure(staged_examined < ledger.buckets["broad_comparator"]["examined"],
               "SELECTED_POSTING_WORK_DISCRIMINATOR")
        report("real_two_stage_store_query_with_false_candidate", definition_corpus=len(corpus),
               method_corpus=len(method_corpus), stage1_candidates=len(candidates),
               alternatives_generated=len(alternatives), alternatives_attempted=1,
               alternatives_not_selected=len(alternatives)-1,
               empty_stage2_searches=empty_method_searches, method_candidates=len(all_methods),
               stage1_ids=candidate_ids, counts=ledger.buckets,
               body_store=body_store.status(), method_store=method_store.status(),
               claim="FINITE_POSTING_FILTER_NOT_TOTAL_COST_SPEEDUP_OR_APPLICABILITY")
    finally:
        if method_store is not None:
            method_store.close()
        body_store.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store-root", required=True)
    parser.add_argument("--definition-evidence", required=True)
    parser.add_argument("--definition-sha256", required=True)
    parser.add_argument("--method-evidence", required=True)
    parser.add_argument("--method-sha256", required=True)
    args = parser.parse_args()
    ledger = Ledger()
    adapter = B.OrdinaryBodyAdapter(S.semantic_id())
    # This event order is intentional: no producer file is opened, parsed or
    # fingerprinted until the entire local query list is fixed and reported.
    alternatives = query(adapter, property_tree())
    frozen_queries = F.compact(alternatives)
    print("LOCAL_QUERY_BEFORE_PUBLISHER_READ " + frozen_queries.decode("utf-8"), flush=True)
    raw = read_selected(args.definition_evidence, args.definition_sha256)
    method_raw = read_selected(args.method_evidence, args.method_sha256)
    record = retained_and_scope(adapter, alternatives, raw, method_raw)
    binding_and_bounds(adapter, raw, record)
    constants_and_shared_dag(adapter)
    ensure(F.compact(alternatives) == frozen_queries, "LOCAL_QUERY_MUTATED_AFTER_PUBLISHER_READ")
    integration(Path(args.store_root), adapter, alternatives, raw, method_raw, ledger)
    ledger.check()
    print("ORDINARY_BODY_ALL_PASS " + json.dumps({"groups": 4,
        "requests": ledger.requests, "reply_bytes": ledger.reply_bytes,
        "request_cap": 64, "reply_cap": 8*MIB, "original_deadline_seconds": 120,
        "mathematical_acceptance": False}, sort_keys=True, separators=(",", ":")), flush=True)


if __name__ == "__main__":
    main()
