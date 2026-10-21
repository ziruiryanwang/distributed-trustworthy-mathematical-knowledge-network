"""Per-declaration discovery from authenticated ModuleSpec group openings.

This checks structural binding, never a module certificate or mathematics.
ExportID is not a ModuleID. Use resolve's typed locator for later acquisition.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib

from . import formal_features as F
from .type_pattern import (PATTERN_PROFILE_SCHEMA, PATTERN_TAG, pattern_spec,
                           validate_type_pattern_profile, _derive as _derive_pattern)
from .conclusion_fingerprint import (
    FINGERPRINT_PROFILE_SCHEMA, FINGERPRINT_TAG, validate_fingerprint_profile,
    _derive_conclusion)

OBJECT_SCHEMA = "DMKN_MODULE_EXPORT_OBJECT_V1"
PAIR_PROFILE_SCHEMA = "DMKN_MODULE_EXPORT_PAIR_PROFILE_V1"
MAX_PAIR_PROFILE_BYTES = 8192
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
    if tag in ("object-kind", "declaration-kind", "declared-type-key", PATTERN_TAG):
        F.fields(spec, ("tag", "value"))
        if tag == "object-kind": F.need(spec["value"] == "module-export-v1", "EXPORT_KIND_FEATURE")
        elif tag == "declaration-kind": F.need(spec["value"] in KINDS, "EXPORT_DECLARATION_KIND")
        else: F.hexid(spec["value"])
    elif tag == FINGERPRINT_TAG:
        F.fields(spec, ("tag", "profile_id", "value"))
        F.hexid(spec["profile_id"]); F.hexid(spec["value"])
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


def _validate_pair(pair):
    F.need(type(pair) is list and len(pair) == 2, "EXPORT_PAIR_SHAPE")
    F.need(all(type(atom) is dict and atom.get("tag") not in (PATTERN_TAG, FINGERPRINT_TAG)
               for atom in pair),
           "EXPORT_PAIR_TYPE_PATTERN_UNSUPPORTED")
    keys = [F.compact(validate_spec(atom)) for atom in pair]
    F.need(keys[0] < keys[1], "EXPORT_PAIR_ATOM_ORDER")
    return pair


def validate_pair_profile(profile):
    """Accept canonical owner-selected atomic pairs, never nested features."""
    F.fields(profile, ("schema", "pairs"))
    F.need(profile["schema"] == PAIR_PROFILE_SCHEMA, "EXPORT_PAIR_PROFILE_SCHEMA")
    pairs = profile["pairs"]
    F.need(type(pairs) is list and 1 <= len(pairs) <= 8, "EXPORT_PAIR_PROFILE_COUNT")
    keys = [F.compact(_validate_pair(pair)) for pair in pairs]
    F.need(keys == sorted(set(keys)), "EXPORT_PAIR_PROFILE_ORDER")
    F.need(len(F.compact(profile)) <= MAX_PAIR_PROFILE_BYTES, "EXPORT_PAIR_PROFILE_BYTES")
    return deepcopy(profile)


def pair_feature_id(namespace, pair):
    """Derive one atomic-pair key; this alone does not adopt an index profile."""
    return F.digest("DMKN-MODULE-EXPORT-PAIR-FEATURE-V1", {
        "namespace": F.hexid(namespace), "atoms": _validate_pair(pair)})


class ModuleExportAdapter:
    feature_schema = F.EXPORT_SCHEMA

    def __init__(self, codec, foundation, policy, *, discovery_profile=None):
        self.codec = codec
        self.foundation, self.policy = F.hexid(foundation), F.hexid(policy)
        pattern = (type(discovery_profile) is dict
                   and discovery_profile.get("schema") == PATTERN_PROFILE_SCHEMA)
        fingerprint = (type(discovery_profile) is dict
                       and discovery_profile.get("schema") == FINGERPRINT_PROFILE_SCHEMA)
        selected = (None if discovery_profile is None else
                    validate_type_pattern_profile(discovery_profile) if pattern else
                    validate_fingerprint_profile(discovery_profile) if fingerprint else
                    validate_pair_profile(discovery_profile))
        self.feature_schema = (F.EXPORT_CONCLUSION_FINGERPRINT_SCHEMA if fingerprint else
                               F.EXPORT_TYPE_PATTERN_SCHEMA if pattern else
                               F.EXPORT_SCHEMA if selected is None else F.EXPORT_PAIR_SCHEMA)
        descriptor = {
            "object_format": OBJECT_SCHEMA, "module_schema": codec.SPEC_SCHEMA,
            "foundation": self.foundation, "semantic_policy": self.policy,
            "feature_schema": self.feature_schema, "partition_bits": 8}
        if selected is not None:
            descriptor["discovery_profile"] = selected
        self.namespace = F.digest("DMKN-DISCOVERY-NAMESPACE-V1", descriptor)
        self._profile_raw = None if selected is None else F.compact(selected)
        self._pattern_enabled = pattern
        self._fingerprint_enabled = fingerprint
        self._fingerprint_profile_id = (codec.hash_value("conclusion-fingerprint-profile-v1", selected)
                                        if fingerprint else None)
        self._pair_entries = () if selected is None or pattern or fingerprint else tuple(
            (frozenset(feature_id(self.namespace, atom) for atom in pair),
             pair_feature_id(self.namespace, pair), F.compact(pair))
            for pair in selected["pairs"])
        self._profile_binding = (self.namespace, self.feature_schema,
                                 self._profile_raw, self._pair_entries, self._pattern_enabled,
                                 self._fingerprint_enabled, self._fingerprint_profile_id)

    def _profile_active(self):
        F.need((self.namespace, self.feature_schema, self._profile_raw, self._pair_entries,
                self._pattern_enabled, self._fingerprint_enabled, self._fingerprint_profile_id)
               == self._profile_binding, "EXPORT_PAIR_PROFILE_CHANGED")

    def compile_query(self, specs):
        """First canonical eligible pair only; all other atomic predicates stay."""
        self._profile_active()
        keys = set(compile_query(self.namespace, specs))
        F.need(self._pattern_enabled or all(spec["tag"] != PATTERN_TAG for spec in specs),
               "EXPORT_TYPE_PATTERN_PROFILE_REQUIRED")
        for spec in specs:
            if spec["tag"] == FINGERPRINT_TAG:
                F.need(self._fingerprint_enabled, "EXPORT_FINGERPRINT_PROFILE_REQUIRED")
                F.need(spec["profile_id"] == self._fingerprint_profile_id,
                       "EXPORT_FINGERPRINT_PROFILE_MISMATCH")
        for atoms, pair_key, _ in self._pair_entries:
            if atoms <= keys:
                keys.difference_update(atoms)
                keys.add(pair_key)
                break
        return sorted(keys)

    def plan_query(self, specs):
        """Add bounded eligible pair anchors without removing legacy route keys.

        This is local profile derivation, not cost statistics or search coverage.
        Extra summaries consume the same existing allowance and may refuse.
        Default compile_query and every extracted record remain unchanged.
        """
        legacy = self.compile_query(specs)
        atomic = frozenset(compile_query(self.namespace, specs))
        eligible = [pair_key for atoms, pair_key, _ in self._pair_entries
                    if atoms <= atomic]
        keys, added, omitted = set(legacy), [], []
        for pair_key in eligible:
            if pair_key in keys:
                continue
            if len(keys) < 8:
                keys.add(pair_key); added.append(pair_key)
            else:
                omitted.append(pair_key)
        return {
            "schema": "DMKN_MODULE_EXPORT_PAIR_QUERY_PLAN_V1",
            "namespace": self.namespace,
            "status": ("WIRE_CAP" if omitted else
                       "ALL_ELIGIBLE" if added else "NO_EXTRA_PAIR"),
            "legacy_features": legacy, "features": sorted(keys),
            "eligible_pair_features": sorted(eligible),
            "added_pair_features": sorted(added),
            "omitted_pair_features": sorted(omitted),
            "global_complete": False, "mathematical_acceptance": False}

    def encode_opening(self, module_id, relative_name, opening):
        """Build canonical transport object; describe/extract still checks it."""
        return self.codec.canonical({"schema": OBJECT_SCHEMA, "module_id": module_id,
                                     "relative_name": relative_name, "opening": opening})

    def describe(self, raw, expected_id=None):
        self._profile_active()
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
        if self._pattern_enabled:
            spec, pattern_work = _derive_pattern(codec, module, declaration["universes"],
                                                 declaration["type"])
            work += pattern_work
            F.need(work <= 1000000, "EXPORT_FEATURE_WORK")
            add(spec)
        if self._fingerprint_enabled:
            spec, fingerprint_work = _derive_conclusion(
                codec, module, declaration["universes"], declaration["type"],
                F.strict(self._profile_raw, 1024))
            work += fingerprint_work
            F.need(work <= 1000000, "EXPORT_FEATURE_WORK")
            add(spec)
        # All atomics remain. The profile never enumerates their power set.
        atomic_keys = frozenset(specs)
        for atoms, pair_key, pair_raw in self._pair_entries:
            work += 3
            F.need(work <= 1000000, "EXPORT_FEATURE_WORK")
            if atoms <= atomic_keys:
                F.need(pair_key in specs or len(specs) < F.MAX_FEATURES,
                       "EXPORT_FEATURE_PROFILE_EXHAUSTED")
                specs[pair_key] = {"tag": "atomic-pair",
                                   "atoms": F.strict(pair_raw, MAX_PAIR_PROFILE_BYTES)}
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
