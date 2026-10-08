"""Per-declaration discovery from authenticated ModuleSpec group openings.

This checks structural binding, never a module certificate or mathematics.
ExportID is not a ModuleID. Use resolve's typed locator for later acquisition.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib

from . import formal_features as F

OBJECT_SCHEMA = "DMKN_MODULE_EXPORT_OBJECT_V1"
TAGS = frozenset(("sort", "bvar", "const", "app", "forall", "lam", "let", "proj"))
SLOTS = {"app": (("fn", 1), ("arg", 2)), "forall": (("domain", 2), ("body", 3)),
         "lam": (("domain", 2), ("body", 3)),
         "let": (("type", 1), ("value", 2), ("body", 3)),
         "proj": (("struct", 3),), "const": (), "sort": (), "bvar": ()}
KINDS = frozenset(("definition", "theorem", "opaque", "inductive", "constructor", "recursor"))


def _symbol(value):
    F.need(type(value) is dict, "EXPORT_SYMBOL")
    if value.get("kind") == "foundation-name":
        F.fields(value, ("kind", "name_hash")); F.hexid(value["name_hash"])
    else:
        F.fields(value, ("kind", "export_id"))
        F.need(value["kind"] == "export", "EXPORT_SYMBOL_KIND"); F.hexid(value["export_id"])


def _head(value):
    F.need(type(value) is dict and value.get("tag") in TAGS, "EXPORT_HEAD")
    if value["tag"] == "const":
        F.fields(value, ("tag", "symbol")); _symbol(value["symbol"])
    else: F.fields(value, ("tag",))


def validate_spec(spec):
    F.need(type(spec) is dict, "EXPORT_FEATURE_SPEC")
    tag = spec.get("tag")
    if tag in ("object-kind", "declaration-kind", "declared-type-key"):
        F.fields(spec, ("tag", "value"))
        if tag == "object-kind": F.need(spec["value"] == "module-export-v1", "EXPORT_KIND_FEATURE")
        elif tag == "declaration-kind": F.need(spec["value"] in KINDS, "EXPORT_DECLARATION_KIND")
        else: F.hexid(spec["value"])
    elif tag == "type-symbol":
        F.fields(spec, ("tag", "symbol")); _symbol(spec["symbol"])
    elif tag in ("result-head", "binder-domain-head"):
        F.fields(spec, ("tag", "head")); _head(spec["head"])
    elif tag == "type-edge":
        F.fields(spec, ("tag", "parent", "slot", "child"))
        F.need(spec["parent"] in TAGS and spec["child"] in TAGS
               and spec["slot"] in {name for name, _ in SLOTS[spec["parent"]]}, "EXPORT_TYPE_EDGE")
    elif tag == "type-import":
        F.fields(spec, ("tag", "module_id")); F.hexid(spec["module_id"])
    else: raise ValueError("EXPORT_FEATURE_TAG")
    return spec


def feature_id(namespace, spec):
    return F.digest("DMKN-MODULE-EXPORT-FEATURE-V1", {
        "namespace": F.hexid(namespace), "feature_spec": validate_spec(spec)})


def compile_query(namespace, specs):
    F.need(type(specs) is list and 1 <= len(specs) <= 8, "EXPORT_QUERY_CONJUNCTS")
    return sorted({feature_id(namespace, spec) for spec in specs})


class ModuleExportAdapter:
    feature_schema = F.EXPORT_SCHEMA

    def __init__(self, codec, foundation, policy):
        self.codec = codec
        self.foundation, self.policy = F.hexid(foundation), F.hexid(policy)
        self.namespace = F.digest("DMKN-DISCOVERY-NAMESPACE-V1", {
            "object_format": OBJECT_SCHEMA, "module_schema": codec.SPEC_SCHEMA,
            "foundation": self.foundation, "semantic_policy": self.policy,
            "feature_schema": self.feature_schema, "partition_bits": 8})

    def encode_opening(self, module_id, relative_name, opening):
        """Build canonical transport object; describe/extract still checks it."""
        return self.codec.canonical({"schema": OBJECT_SCHEMA, "module_id": module_id,
                                     "relative_name": relative_name, "opening": opening})

    def describe(self, raw, expected_id=None):
        codec = self.codec
        value = codec.parse_json(raw)
        F.need(codec.canonical(value) == raw, "EXPORT_CANONICAL_BYTES")
        F.fields(value, ("schema", "module_id", "relative_name", "opening"))
        F.need(value["schema"] == OBJECT_SCHEMA, "EXPORT_OBJECT_SCHEMA")
        module = F.hexid(value["module_id"])
        group = codec.verify_group_opening(module, value["opening"])
        summary = value["opening"]["summary"]
        F.need(summary["foundation"] == self.foundation and summary["policy"] == self.policy,
               "EXPORT_NAMESPACE_POLICY")
        name_key = codec.name_key(value["relative_name"])
        selected = [d for d in group["declarations"] if codec.name_key(d["name"]) == name_key]
        F.need(len(selected) == 1, "EXPORT_DECLARATION_SELECTION")
        declaration = selected[0]
        identifier = codec.export_id(module, declaration["name"])
        if expected_id is not None: F.need(identifier == F.hexid(expected_id), "EXPORT_ID_BINDING")
        specs, work = {}, 0

        def add(spec):
            key = feature_id(self.namespace, spec)
            F.need(key in specs or len(specs) < F.MAX_FEATURES, "EXPORT_FEATURE_PROFILE_EXHAUSTED")
            specs[key] = spec

        def symbol(ref):
            if ref[0] == "foundation":
                return {"kind": "foundation-name", "name_hash": codec.hash_value("foundation-symbol", ref[1])}
            owner, name = (module, ref[1]) if ref[0] == "local" else (ref[1], ref[2])
            return {"kind": "export", "export_id": codec.export_id(owner, name)}

        def head(expr):
            nonlocal work
            while expr[0] == "app":
                work += 1; F.need(work <= 1000000, "EXPORT_FEATURE_WORK")
                expr = expr[1]
            return {"tag": expr[0], **({"symbol": symbol(expr[1])} if expr[0] == "const" else {})}

        add({"tag": "object-kind", "value": "module-export-v1"})
        add({"tag": "declaration-kind", "value": declaration["kind"]})
        relocated = codec.relocate_expr(declaration["type"], module, declaration["universes"])
        type_key = codec.hash_value("discovery-declared-type", {"universes": declaration["universes"], "type": relocated})
        add({"tag": "declared-type-key", "value": type_key})
        todo, nodes = [declaration["type"]], 0
        while todo:
            expr = todo.pop(); tag = expr[0]
            nodes += 1; work += 1
            F.need(work <= 1000000 and nodes <= codec.DEFAULT_LIMITS.max_nodes, "EXPORT_FEATURE_WORK")
            if tag in ("const", "proj"):
                ref = expr[1]
                add({"tag": "type-symbol", "symbol": symbol(ref)})
                if ref[0] == "external": add({"tag": "type-import", "module_id": ref[1]})
            for slot, index in SLOTS[tag]:
                child = expr[index]
                add({"tag": "type-edge", "parent": tag, "slot": slot, "child": child[0]})
                todo.append(child); work += 1
        result = declaration["type"]
        while result[0] == "forall":
            add({"tag": "binder-domain-head", "head": head(result[2])})
            result = result[3]; work += 1
            F.need(work <= 1000000, "EXPORT_FEATURE_WORK")
        add({"tag": "result-head", "head": head(result)})
        locator = {"schema": "DMKN_MODULE_EXPORT_LOCATOR_V1", "module_id": module,
                   "group_index": value["opening"]["index"], "relative_name": deepcopy(declaration["name"]),
                   "descriptor_id": codec.hash_value("declaration-descriptor", declaration)}
        record = {"schema": F.EXPORT_RECORD_SCHEMA, "namespace": self.namespace, "kind": "module-export-v1",
                  "object_id": identifier, "object_sha256": hashlib.sha256(raw).hexdigest(),
                  "object_bytes": len(raw), "features": sorted(specs), "locator": locator}
        F.validate_record(record, self.namespace)
        return {"record": record, "specs": [specs[k] for k in sorted(specs)], "type_nodes": nodes,
                "work": work, "descriptor": deepcopy(declaration), "mathematical_acceptance": False}

    def extract(self, raw, expected_id=None):
        return self.describe(raw, expected_id)["record"]

    def resolve(self, record, raw):
        """Authenticate exact candidate/locator; does not accept its mathematics."""
        F.validate_record(record, self.namespace)
        F.need(record["schema"] == F.EXPORT_RECORD_SCHEMA, "EXPORT_RECORD_REQUIRED")
        described = self.describe(raw, record["object_id"])
        F.need(described["record"] == record, "EXPORT_RECORD_BINDING")
        return {"export_id": record["object_id"], "locator": deepcopy(record["locator"]),
                "descriptor": described["descriptor"], "assurance": "AUTHENTICATED_EXPORT_DESCRIPTOR",
                "mathematical_acceptance": False,
                "next_gate": "VERIFY_APPLICABLE_MODULE_CERTIFICATE_BEFORE_MATHEMATICAL_USE"}
