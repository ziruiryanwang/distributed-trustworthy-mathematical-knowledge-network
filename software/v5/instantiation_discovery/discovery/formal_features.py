"""Bounded formal discovery metadata. No proof or source-execution authority.

The named-module adapter receives already adopted codec/registry objects. Future
module formats implement their own adapter and namespace; do not reuse this
adapter as an assertion that another representation has v4 semantics.
"""
from __future__ import annotations

import hashlib
import json
import re

HEX = re.compile(r"[0-9a-f]{64}\Z")
SCHEMA = "DMKN_DECLARED_TYPE_FEATURES_V1"
EXPORT_SCHEMA = "DMKN_MODULE_EXPORT_FEATURES_V1"
EXPORT_PAIR_SCHEMA = "DMKN_MODULE_EXPORT_PAIR_FEATURES_V1"
EXPORT_TYPE_PATTERN_SCHEMA = "DMKN_MODULE_EXPORT_TYPE_PATTERN_FEATURES_V1"
EXPORT_CONCLUSION_FINGERPRINT_SCHEMA = "DMKN_MODULE_EXPORT_CONCLUSION_FINGERPRINT_FEATURES_V1"
RECORD_SCHEMA = "DMKN_FORMAL_FEATURE_RECORD_V1"
EXPORT_RECORD_SCHEMA = "DMKN_FORMAL_FEATURE_RECORD_V2"
MAX_FEATURES, MAX_RECORD = 128, 16384
TAGS = frozenset(("sort", "bvar", "const", "app", "forallE", "lam", "letE", "proj"))
CHILDREN = {"app": ("fn", "arg"), "forallE": ("type", "body"),
            "lam": ("type", "body"), "letE": ("type", "value", "body"),
            "proj": ("struct",), "sort": (), "bvar": (), "const": ()}


def need(ok, code):
    if not ok:
        raise ValueError(code)


def uint(value, low, high, code="INTEGER_BOUND"):
    need(type(value) is int and low <= value <= high, code)
    return value


def hexid(value):
    need(type(value) is str and HEX.fullmatch(value), "HASH_ENCODING")
    return value


def fields(value, expected):
    need(type(value) is dict and set(value) == set(expected), "EXACT_FIELDS")


def compact(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def strict(raw, maximum):
    need(type(raw) is bytes and 0 < len(raw) <= maximum, "JSON_BYTE_LIMIT")
    depth, quoted, escaped = 0, False, False
    for byte in raw:
        if quoted:
            if escaped: escaped = False
            elif byte == 92: escaped = True
            elif byte == 34: quoted = False
        elif byte == 34: quoted = True
        elif byte in (91, 123):
            depth += 1
            need(depth <= 32, "JSON_DEPTH_LIMIT")
        elif byte in (93, 125):
            depth -= 1
            need(depth >= 0, "JSON_DEPTH_LIMIT")
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "JSON_DUPLICATE_KEY")
            result[key] = value
        return result
    def bad(_): raise ValueError("JSON_NONINTEGER")
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                       parse_float=bad, parse_constant=bad)
    need(compact(value) == raw, "NONCANONICAL_JSON")
    return value


def digest(domain, value):
    return hashlib.sha256(domain.encode("ascii") + b"\0" + compact(value)).hexdigest()


def _symbol(value):
    need(type(value) is dict, "SYMBOL")
    if value.get("kind") == "foundation-name":
        fields(value, ("kind", "name_hash")); hexid(value["name_hash"])
    else:
        fields(value, ("kind", "module_id"))
        need(value["kind"] == "module", "SYMBOL_KIND"); hexid(value["module_id"])


def _head(value):
    need(type(value) is dict and value.get("tag") in TAGS, "HEAD")
    if value["tag"] == "const":
        fields(value, ("tag", "symbol")); _symbol(value["symbol"])
    else:
        fields(value, ("tag",))


def validate_spec(spec):
    need(type(spec) is dict, "FEATURE_SPEC")
    tag = spec.get("tag")
    if tag in ("object-kind", "declared-type-key"):
        fields(spec, ("tag", "value"))
        if tag == "object-kind":
            need(spec["value"] == "named-definition-v1", "OBJECT_KIND_FEATURE")
        else:
            need(type(spec["value"]) is str and spec["value"].startswith("type:"), "TYPE_KEY")
            hexid(spec["value"][5:])
    elif tag == "type-symbol":
        fields(spec, ("tag", "symbol")); _symbol(spec["symbol"])
    elif tag in ("result-head", "binder-domain-head"):
        fields(spec, ("tag", "head")); _head(spec["head"])
    elif tag == "type-edge":
        fields(spec, ("tag", "parent", "slot", "child"))
        need(spec["parent"] in TAGS and spec["child"] in TAGS
             and spec["slot"] in CHILDREN[spec["parent"]], "TYPE_EDGE")
    elif tag == "direct-import":
        fields(spec, ("tag", "module_id")); hexid(spec["module_id"])
    else:
        raise ValueError("FEATURE_TAG")
    return spec


def feature_id(namespace, spec):
    return digest("DMKN-FORMAL-FEATURE-V1", {"namespace": hexid(namespace),
                                           "feature_spec": validate_spec(spec)})


def compile_query(namespace, specs):
    need(type(specs) is list and 1 <= len(specs) <= 8, "QUERY_CONJUNCTS")
    result = sorted({feature_id(namespace, spec) for spec in specs})
    need(1 <= len(result) <= 8, "QUERY_CONJUNCTS")
    return result


def validate_features(features, maximum=MAX_FEATURES):
    need(type(features) is list and 1 <= len(features) <= maximum, "FEATURE_COUNT")
    for value in features: hexid(value)
    need(features == sorted(set(features)), "FEATURE_ORDER")
    return features


def validate_record(record, namespace=None):
    need(type(record) is dict, "RECORD_SHAPE")
    schema = record.get("schema")
    need(schema in (RECORD_SCHEMA, EXPORT_RECORD_SCHEMA), "RECORD_SCHEMA")
    base = ("schema", "namespace", "kind", "object_id", "object_sha256", "object_bytes", "features")
    fields(record, (*base, "locator") if schema == EXPORT_RECORD_SCHEMA else base)
    hexid(record["namespace"])
    need(namespace is None or record["namespace"] == namespace, "RECORD_NAMESPACE")
    need(type(record["kind"]) is str and re.fullmatch(r"[a-z0-9-]{1,64}", record["kind"]), "RECORD_KIND")
    hexid(record["object_id"]); hexid(record["object_sha256"])
    uint(record["object_bytes"], 1, 64 * 1024**2, "RECORD_OBJECT_BYTES")
    if schema == EXPORT_RECORD_SCHEMA:
        need(record["kind"] == "module-export-v1", "EXPORT_RECORD_KIND")
        locator = record["locator"]
        fields(locator, ("schema", "module_id", "group_index", "relative_name", "descriptor_id"))
        need(locator["schema"] == "DMKN_MODULE_EXPORT_LOCATOR_V1", "EXPORT_LOCATOR_SCHEMA")
        hexid(locator["module_id"]); hexid(locator["descriptor_id"])
        uint(locator["group_index"], 0, 4095, "EXPORT_GROUP_INDEX")
        name = locator["relative_name"]
        need(type(name) is list and 1 <= len(name) <= 64, "EXPORT_NAME_PARTS")
        for part in name:
            need(type(part) is list and len(part) == 2, "EXPORT_NAME_COMPONENT")
            if part[0] == "s":
                need(type(part[1]) is str and 0 < len(part[1].encode("utf-8")) <= 1024
                     and "\0" not in part[1], "EXPORT_NAME_STRING")
            else:
                need(part[0] == "n", "EXPORT_NAME_TAG"); uint(part[1], 0, 2**32-1, "EXPORT_NAME_NUMBER")
    validate_features(record["features"])
    need(len(compact(record)) <= MAX_RECORD, "RECORD_BYTES")
    return record


def record_id(record):
    validate_record(record)
    domain = "DMKN-FORMAL-FEATURE-RECORD-V2" if record["schema"] == EXPORT_RECORD_SCHEMA else "DMKN-FORMAL-FEATURE-RECORD-V1"
    return digest(domain, record)


class NamedModuleAdapter:
    def __init__(self, library, codec, registry):
        self.library, self.codec, self.registry = library, codec, registry
        self.namespace = digest("DMKN-DISCOVERY-NAMESPACE-V1", {
            "object_format": "named-definition-v1",
            "formal_policy": {"policy": library.policy(registry, codec), "lowering": library.LOWERING},
            "feature_schema": SCHEMA, "partition_bits": 8})

    def describe(self, raw, expected_id=None):
        info = self.library.inspect(raw, self.registry, self.codec, expected_id=expected_id)
        graph = self.codec.Graph()
        for row in info["plan"]["graph"]: graph.push(row)
        header, aliases = info["plan"]["header"], info["aliases"]
        specs = {}
        def add(spec):
            key = feature_id(self.namespace, spec)
            need(key in specs or len(specs) < MAX_FEATURES, "FEATURE_PROFILE_EXHAUSTED")
            specs[key] = spec
        def symbol(index):
            name = graph.hashes["name"][index]
            return ({"kind": "module", "module_id": aliases[name]} if name in aliases else
                    {"kind": "foundation-name", "name_hash": name})
        work = 0
        def head(index):
            nonlocal work
            while True:
                work += 1; need(work <= 1000000, "FEATURE_WORK_BOUND")
                tag, node = graph.nodes["expr"][index]
                if tag != "app": break
                index = node["fn"]
            return {"tag": tag, **({"symbol": symbol(node["name"])} if tag == "const" else {})}
        add({"tag": "object-kind", "value": "named-definition-v1"})
        add({"tag": "declared-type-key", "value": info["type_key"]})
        todo, seen = [header["type"]], set()
        while todo:
            index = todo.pop()
            if index in seen: continue
            seen.add(index); work += 1
            need(len(seen) <= 62285 and work <= 1000000, "FEATURE_WORK_BOUND")
            tag, node = graph.nodes["expr"][index]
            need(tag in TAGS, "FEATURE_EXPRESSION_PROFILE")
            if tag == "const": add({"tag": "type-symbol", "symbol": symbol(node["name"])})
            if tag == "proj": add({"tag": "type-symbol", "symbol": symbol(node["typeName"])})
            for slot in CHILDREN[tag]:
                child = node[slot]; child_tag = graph.nodes["expr"][child][0]
                add({"tag": "type-edge", "parent": tag, "slot": slot, "child": child_tag})
                todo.append(child); work += 1
        result = header["type"]
        while graph.nodes["expr"][result][0] == "forallE":
            node = graph.nodes["expr"][result][1]
            add({"tag": "binder-domain-head", "head": head(node["type"])})
            result = node["body"]; work += 1
            need(work <= 1000000, "FEATURE_WORK_BOUND")
        add({"tag": "result-head", "head": head(result)})
        for module in info["import_ids"]: add({"tag": "direct-import", "module_id": module})
        record = {"schema": RECORD_SCHEMA, "namespace": self.namespace, "kind": "named-definition-v1",
                  "object_id": info["module_id"], "object_sha256": hashlib.sha256(raw).hexdigest(),
                  "object_bytes": len(raw), "features": sorted(specs)}
        validate_record(record, self.namespace)
        return {"record": record, "specs": [specs[key] for key in sorted(specs)],
                "work": work, "type_nodes": len(seen), "mathematical_acceptance": False}

    def extract(self, raw, expected_id=None):
        return self.describe(raw, expected_id)["record"]
