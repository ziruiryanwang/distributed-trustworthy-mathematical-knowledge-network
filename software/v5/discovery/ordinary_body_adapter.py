"""Bounded ordinary definition-body discovery, never mathematical authority.

One exact singleton definition gives one path fingerprint. A closed local
property gives at most eight independently funded query alternatives. No
normalization, imported-body fetch, module load, checker or network is used.
The observer follows the retained conclusion_fingerprint algorithm, with source
lambda peeling and the ordinary V2 DAG/symbol representation.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json

from . import formal_features as F


PROFILE_SCHEMA = "DMKN_ORDINARY_DEFINITION_BODY_PROFILE_V1"
FINGERPRINT_TAG = "definition-body-fingerprint"
OBJECT_KIND = "ordinary-lean-definition-body-v1"
EVIDENCE_SCHEMA = "DMKN_LEAN_ORDINARY_EVIDENCE_V2"
LOCATOR_SCHEMA = "DMKN_ORDINARY_LEAN_EXPORT_LOCATOR_V2"
FEATURE_REVISION = "raw-single-definition-lambda-paths-v1"
PATHS = (("body", "body", "arg", "arg"), ("body", "body", "arg"),
         ("body", "domain", "arg"))
_PROFILE = {"schema": PROFILE_SCHEMA, "paths": [list(path) for path in PATHS]}
PROFILE_ID = F.digest("DMKN-ORDINARY-BODY-PROFILE-V1", _PROFILE)
_TAGS = {0: "bvar", 1: "sort", 2: "const", 3: "app", 4: "lam",
         5: "forall", 6: "let", 7: "nat-literal", 8: "proj", 9: "string-literal"}
_SLOTS = {0: {}, 1: {}, 2: {}, 3: {"fn": 1, "arg": 2},
          4: {"domain": 3, "body": 4}, 5: {"domain": 3, "body": 4},
          6: {"type": 2, "value": 3, "body": 4}, 7: {},
          8: {"struct": 3}, 9: {}}


def profile():
    """Return the fixed profile, detached from module constants."""
    return deepcopy(_PROFILE)


def namespace_for(semantic_id):
    return F.digest("DMKN-ORDINARY-BODY-DISCOVERY-NAMESPACE-V1", {
        "semantic_id": F.hexid(semantic_id), "profile_id": PROFILE_ID,
        "feature_schema": F.ORDINARY_BODY_SCHEMA,
        "record_schema": F.ORDINARY_BODY_RECORD_SCHEMA,
        "evidence_schema": EVIDENCE_SCHEMA,
        "expression_format": "DMKN_LEAN_ORIGINAL_EXPR_V1",
        "feature_revision": FEATURE_REVISION, "partition_bits": 8})


def validate_spec(spec):
    F.fields(spec, ("tag", "profile_id", "value"))
    F.need(spec["tag"] == FINGERPRINT_TAG and spec["profile_id"] == PROFILE_ID,
           "ORDINARY_BODY_FEATURE_PROFILE")
    F.hexid(spec["value"])
    return spec


def feature_id(namespace, spec):
    return F.digest("DMKN-ORDINARY-BODY-FEATURE-V1", {
        "namespace": F.hexid(namespace), "feature_spec": validate_spec(spec)})


def validate_record_locator(record):
    import portable_preview as P
    import ordinary_semantics as S

    F.need(record["kind"] == OBJECT_KIND, "ORDINARY_BODY_RECORD_KIND")
    locator = P.read_locator(record["locator"])
    F.need(record["namespace"] == namespace_for(locator["semantic_id"]),
           "ORDINARY_BODY_RECORD_NAMESPACE")
    expected = S.export_id(locator["semantic_id"], locator["unit_id"], locator["export_name"])
    F.need(record["object_id"] == expected, "ORDINARY_BODY_RECORD_EXPORT")
    return locator


def _spec(vector):
    return {"tag": FINGERPRINT_TAG, "profile_id": PROFILE_ID,
            "value": F.digest("DMKN-ORDINARY-BODY-FINGERPRINT-V1",
                              {"profile_id": PROFILE_ID, "tokens": vector})}


def _query_preflight(value, limits):
    """Bound all local Python input before recursive encoding/codec calls.

    Reuses type_pattern's occurrence-counting principle, without expanding a
    DAG into a tree. Sharing counts each supplied occurrence; cycles hit depth.
    The only dictionaries in the ordinary expression grammar are $bytes values.
    """
    stack, count, size = [(iter((value,)), 0)], 0, 0
    while stack:
        children, depth = stack[-1]
        try:
            item = next(children)
        except StopIteration:
            stack.pop()
            continue
        count += 1
        F.need(count <= limits.max_bytes and depth <= limits.max_json_depth,
               "ORDINARY_BODY_QUERY_PREFLIGHT_WORK")
        if type(item) is list:
            F.need(len(item) <= limits.max_bytes, "ORDINARY_BODY_QUERY_PREFLIGHT_LIST")
            size += 2 + max(0, len(item)-1)
            stack.append((iter(item), depth+1))
        elif type(item) is dict:
            F.need(len(item) == 1 and "$bytes" in item, "ORDINARY_BODY_QUERY_PREFLIGHT_OBJECT")
            size += 3  # braces and colon; key/value are charged below.
            stack.append((iter(("$bytes", item["$bytes"])), depth+1))
        elif type(item) is str:
            F.need(len(item) <= limits.max_bytes, "ORDINARY_BODY_QUERY_PREFLIGHT_STRING")
            try:
                size += len(json.dumps(item, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
            except (UnicodeError, ValueError) as exc:
                raise ValueError("ORDINARY_BODY_QUERY_PREFLIGHT_ENCODING") from exc
        elif type(item) is int:
            F.need(0 <= item < 2**64, "ORDINARY_BODY_QUERY_PREFLIGHT_INTEGER")
            size += len(str(item))
        else:
            raise ValueError("ORDINARY_BODY_QUERY_PREFLIGHT_VALUE")
        F.need(size <= limits.max_bytes, "ORDINARY_BODY_QUERY_PREFLIGHT_BYTES")
    return count


class OrdinaryBodyAdapter:
    feature_schema = F.ORDINARY_BODY_SCHEMA

    def __init__(self, semantic_id, *, limits=None):
        import portable_evidence as PE
        import ordinary_evidence as E
        import ordinary_semantics as S

        self.portable, self.evidence = PE, E
        self.semantic_id = F.hexid(semantic_id)
        F.need(self.semantic_id == S.semantic_id(), "ORDINARY_BODY_SEMANTICS_NOT_SELECTED")
        defaults = E.Limits(max_bytes=1024*1024, max_json_depth=64,
            max_name_parts=128, max_name_bytes=16384, max_literal_bytes=65536,
            max_params=128, max_levels=8192, max_exprs=32768,
            max_dag_depth=256, max_unit_nodes=131072, max_inventory=1,
            max_types=1, max_constructors=1, max_names=128, max_imports=8192)
        self.limits = defaults if limits is None else limits
        F.need(type(self.limits) is E.Limits, "ORDINARY_BODY_LIMITS")
        F.need(all(getattr(self.limits, key) <= value for key, value in vars(defaults).items()),
               "ORDINARY_BODY_LIMITS_NOT_STRICTER")
        F.need(PE.SCHEMA == EVIDENCE_SCHEMA, "ORDINARY_BODY_ASSEMBLY")
        self.namespace = namespace_for(self.semantic_id)

    def compile_query(self, specs):
        F.need(type(specs) is list and len(specs) == 1, "ORDINARY_BODY_SINGLE_FINGERPRINT_QUERY")
        return [feature_id(self.namespace, specs[0])]

    def _observe(self, packet, root, path, bindings, *, parameters=0, context=0):
        nodes, current, q, work = packet[2], root, 0, 0
        for position in range(len(path)+1):
            work += 1
            node, variable = nodes[current], None
            tag = node[0]
            if tag == 0:
                index = node[1]
                if index < q:
                    variable = ["local", index]
                elif index < q+parameters:
                    return ["star"], work
                elif index < q+context:
                    variable = ["context", index-q]
                else:
                    raise ValueError("ORDINARY_BODY_VARIABLE_SCOPE")
            if position == len(path):
                if variable is not None:
                    return variable, work
                if tag == 2:
                    key = self.evidence.name_key(node[1], self.limits)
                    F.need(key in bindings, "ORDINARY_BODY_UNBOUND_CONSTANT")
                    return ["const", {"kind": "portable-symbol", "symbol_id": bindings[key]}], work
                return ["node", _TAGS[tag]], work
            edge = path[position]
            child = _SLOTS[tag].get(edge)
            if child is None:
                return ["absent"], work
            if edge == "body" and tag in (4, 5, 6):
                q += 1
            current = node[child]
        raise AssertionError("UNREACHABLE_BODY_POSITION")

    def describe(self, raw, expected_id=None):
        PE, E = self.portable, self.evidence
        exact = PE.read_evidence(raw, self.limits)
        doc = exact.document
        F.need(doc["semantic_id"] == self.semantic_id, "ORDINARY_BODY_EVIDENCE_SEMANTICS")
        _, descriptor, inventory = doc["unit"]
        F.need(descriptor[0] == 0 and len(inventory) == 1 and inventory[0][1] == 1,
               "ORDINARY_BODY_SINGLE_DEFINITION")
        row = inventory[0]
        F.need(descriptor[1] == row[0] and descriptor[2] == row[2] and
               descriptor[3] == row[3] and descriptor[4] == row[4][0] and
               descriptor[5] == row[4][1] and descriptor[6] == row[4][2] and
               descriptor[6] == [descriptor[1]], "ORDINARY_BODY_DESCRIPTOR_INVENTORY")
        export = PE.export_id(self.semantic_id, exact.unit_id, row[0], self.limits)
        if expected_id is not None:
            F.need(export == F.hexid(expected_id), "ORDINARY_BODY_EXPORT_BINDING")
        bindings = {E.name_key(name, self.limits): symbol for name, symbol in doc["imports"]}
        bindings[E.name_key(row[0], self.limits)] = export
        packet, k = descriptor[4], 0
        root, nodes = packet[3], packet[2]
        while nodes[root][0] == 4:
            k += 1
            F.need(k <= self.limits.max_dag_depth, "ORDINARY_BODY_LAMBDA_BOUND")
            root = nodes[root][4]
        vector, observed = [], 0
        for path in PATHS:
            token, work = self._observe(packet, root, path, bindings, parameters=k)
            vector.append(token)
            observed += work
        spec = _spec(vector)
        locator = {"schema": LOCATOR_SCHEMA, "semantic_id": self.semantic_id,
                   "unit_id": exact.unit_id, "export_name": deepcopy(row[0])}
        record = {"schema": F.ORDINARY_BODY_RECORD_SCHEMA, "namespace": self.namespace,
                  "kind": OBJECT_KIND, "object_id": export,
                  "object_sha256": hashlib.sha256(raw).hexdigest(), "object_bytes": len(raw),
                  "features": [feature_id(self.namespace, spec)], "locator": locator}
        F.validate_record(record, self.namespace)
        return {"record": record, "specs": [spec], "observations": vector,
                "source_lambdas": k, "body_nodes": len(packet[1])+len(packet[2]),
                "path_visits": observed, "total_unit_nodes": exact.census.total_nodes,
                "work": exact.census.total_nodes+k+observed,
                "mathematical_acceptance": False}

    def extract(self, raw, expected_id=None):
        return self.describe(raw, expected_id)["record"]

    def resolve(self, record, raw):
        F.validate_record(record, self.namespace)
        F.need(record["schema"] == F.ORDINARY_BODY_RECORD_SCHEMA, "ORDINARY_BODY_RECORD_REQUIRED")
        described = self.describe(raw, record["object_id"])
        F.need(described["record"] == record, "ORDINARY_BODY_EVIDENCE_RECORD_BINDING")
        return {"export_id": record["object_id"], "locator": deepcopy(record["locator"]),
                "mathematical_acceptance": False,
                "assurance": "EXACT_DEFINITION_EVIDENCE_FEATURES_NOT_MATHEMATICAL_ACCEPTANCE",
                "next_gate": "MATCH_WARRANTED_IMPORTS_AND_CHECK_ORDINARY_EXTENSION"}

    def goal_queries(self, *, expression, universe_params, bindings, context_binders=0):
        """Return most-specific alternatives first, not automatic broadcasts.

        Input is formal local Pi-Gamma.property, with no remote target ID.
        The caller must select and fund each actual query; all-STAR may be huge.
        """
        E = self.evidence
        _query_preflight([expression, universe_params, bindings, context_binders], self.limits)
        params = E._names(universe_params, self.limits.max_params, self.limits, params=True)
        refs, _ = E._dag_references(expression, params, self.limits)
        keys, bound = [], {}
        for row in E._array(bindings, maximum=self.limits.max_imports):
            name, symbol = E._array(row, 2)
            key = E.name_key(name, self.limits)
            keys.append(key)
            bound[key] = E._hex(symbol)
        F.need(keys == sorted(refs), "ORDINARY_BODY_QUERY_BINDING_CENSUS")
        E._uint(context_binders, self.limits.max_dag_depth)
        nodes, root = expression[2], expression[3]
        for _ in range(context_binders):
            F.need(nodes[root][0] == 5, "ORDINARY_BODY_QUERY_CONTEXT_TELESCOPE")
            root = nodes[root][4]
        vector = [self._observe(expression, root, path, bound, context=context_binders)[0]
                  for path in PATHS]
        varying = [i for i, token in enumerate(vector) if token[0] != "context"]
        base = [["star"] if token[0] == "context" else token for token in vector]
        alternatives = {}
        for mask in range(1 << len(varying)):
            choice = list(base)
            for bit, index in enumerate(varying):
                if mask & (1 << bit):
                    choice[index] = ["star"]
            spec = _spec(choice)
            alternatives[F.compact(spec)] = (sum(token[0] == "star" for token in choice), [spec])
        keys = sorted(alternatives, key=lambda key: (alternatives[key][0], key))
        return [alternatives[key][1] for key in keys]
