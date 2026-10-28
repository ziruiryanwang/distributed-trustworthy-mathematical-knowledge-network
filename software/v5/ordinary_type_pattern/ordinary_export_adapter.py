"""Exact ordinary discovery with explicitly selected whole-type pattern mode.

The default retains the existing exact namespace and record bytes. Only the
explicit pattern mode selects a new namespace; no old snapshot migration.
All inherited kind/symbol/head feature and exact locator checks remain.

Only the bounded selected type is read: no proof, ancestor, local snapshot or
provider is consulted. Pattern mode also requires the selected pure pattern
helper and caller-supplied fixed inventory bytes. Neither mode grants acceptance.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib

from . import formal_features as F
import formal_query as Q


PREVIEW_SCHEMA = "DMKN_ORDINARY_LEAN_TYPE_PREVIEW_V2"
EVIDENCE_SCHEMA = "DMKN_LEAN_ORDINARY_EVIDENCE_V2"
LOCATOR_SCHEMA = "DMKN_ORDINARY_LEAN_EXPORT_LOCATOR_V2"
OBJECT_KIND = "ordinary-lean-export-v2"
FEATURE_REVISION = "kind-symbol-memoized-spine-head-exact-type-v2"
PATTERN_FEATURE_REVISION = "kind-symbol-memoized-spine-head-exact-type-pattern-v1"
DISCOVERY_PROFILES = ("exact-v2", "type-pattern-v1")
FEATURE_DOMAIN = "DMKN-ORDINARY-LEAN-EXPORT-FEATURE-V1"
NAMESPACE_DOMAIN = "DMKN-ORDINARY-DISCOVERY-NAMESPACE-V1"
KINDS = {1: "definition", 2: "theorem", 3: "opaque", 4: "inductive",
         5: "constructor", 6: "recursor"}
TAGS = {0: "bvar", 1: "sort", 2: "const", 3: "app", 4: "lam",
        5: "forallE", 6: "letE", 7: "nat-literal", 8: "proj", 9: "string-literal"}


def _profile(value):
    F.need(type(value) is str and value in DISCOVERY_PROFILES, "ORDINARY_DISCOVERY_PROFILE")
    return value


def namespace_for(semantic_id, *, discovery_profile="exact-v2"):
    """Portable index namespace, independent of I, local context and provider."""
    mode = _profile(discovery_profile)
    descriptor = {
        "semantic_id": F.hexid(semantic_id), "preview_schema": PREVIEW_SCHEMA,
        "evidence_schema": EVIDENCE_SCHEMA,
        "unit_format": "DMKN_LEAN_ORDINARY_UNIT_V1",
        "expression_format": "DMKN_LEAN_ORIGINAL_EXPR_V1",
        "normalization": "original-type-dag-no-conversion",
        "feature_schema": F.ORDINARY_EXPORT_SCHEMA,
        "feature_revision": FEATURE_REVISION, "type_key_profile": Q.PROFILE_ID,
        "partition_bits": 8}
    if mode == "type-pattern-v1":
        import ordinary_type_pattern as T
        import ordinary_semantics as S
        F.need(semantic_id == S.semantic_id(), "ORDINARY_PATTERN_SEMANTICS_NOT_SELECTED")
        descriptor.update(feature_revision=PATTERN_FEATURE_REVISION,
                          pattern_profile=T.PROFILE_ID, max_features=F.MAX_FEATURES)
    return F.digest(NAMESPACE_DOMAIN, descriptor)


def _symbol(value):
    F.fields(value, ("kind", "symbol_id"))
    F.need(value["kind"] == "portable-symbol", "ORDINARY_SYMBOL_KIND")
    F.hexid(value["symbol_id"])


def _head(value):
    F.need(type(value) is dict and value.get("tag") in TAGS.values(), "ORDINARY_HEAD")
    if value["tag"] in ("const", "proj"):
        F.fields(value, ("tag", "symbol"))
        _symbol(value["symbol"])
    else:
        F.fields(value, ("tag",))


def validate_spec(spec, *, discovery_profile="exact-v2"):
    mode = _profile(discovery_profile)
    F.need(type(spec) is dict, "ORDINARY_FEATURE_SPEC")
    tag = spec.get("tag")
    if tag in ("object-kind", "declaration-kind"):
        F.fields(spec, ("tag", "value"))
        if tag == "object-kind":
            F.need(spec["value"] == OBJECT_KIND, "ORDINARY_OBJECT_KIND")
        else:
            F.need(spec["value"] in KINDS.values(), "ORDINARY_DECLARATION_KIND")
    elif tag == "declared-type-key" or tag == "declared-type-pattern" and mode == "type-pattern-v1":
        F.fields(spec, ("tag", "value"))
        F.hexid(spec["value"])
    elif tag == "type-symbol":
        F.fields(spec, ("tag", "symbol"))
        _symbol(spec["symbol"])
    elif tag in ("result-head", "binder-domain-head"):
        F.fields(spec, ("tag", "head"))
        _head(spec["head"])
    else:
        raise ValueError("ORDINARY_FEATURE_TAG")
    return spec


def feature_id(namespace, spec, *, discovery_profile="exact-v2"):
    mode = _profile(discovery_profile)
    if mode == "type-pattern-v1":
        import ordinary_semantics as S
        F.need(namespace == namespace_for(S.semantic_id(), discovery_profile=mode),
               "ORDINARY_DISCOVERY_PROFILE_NAMESPACE")
    return F.digest(FEATURE_DOMAIN, {
        "namespace": F.hexid(namespace),
        "feature_spec": validate_spec(spec, discovery_profile=mode)})


def compile_query(namespace, specs, *, discovery_profile="exact-v2"):
    """At most eight exact-feature conjuncts; no theorem identity is required."""
    F.need(type(specs) is list and 1 <= len(specs) <= 8, "ORDINARY_QUERY_CONJUNCTS")
    return sorted({feature_id(namespace, spec, discovery_profile=discovery_profile) for spec in specs})


def validate_record_locator(record):
    """New-record-only validation; generic metadata still adopts no semantics.

    Called by formal_features only for V3. Lazy imports preserve V1/V2 assemblies
    that do not ship ordinary syntax support. This function does not recurse into
    validate_record, extract a preview, or infer existence from a portable ID.
    """
    import portable_preview as P
    import ordinary_semantics as S

    F.need(record["kind"] == OBJECT_KIND, "ORDINARY_RECORD_KIND")
    locator = P.read_locator(record["locator"])
    if record["namespace"] != namespace_for(locator["semantic_id"]):
        # Old exact records take the unchanged path without loading the optional
        # pattern helper. Generic recognition never verifies claimed features;
        # selected adapter resolution still rederives the complete record.
        F.need(record["namespace"] == namespace_for(locator["semantic_id"],
                   discovery_profile="type-pattern-v1"), "ORDINARY_RECORD_NAMESPACE")
    expected = S.export_id(locator["semantic_id"], locator["unit_id"], locator["export_name"])
    F.need(record["object_id"] == expected, "ORDINARY_RECORD_EXPORT_BINDING")
    return locator


class OrdinaryExportAdapter:
    feature_schema = F.ORDINARY_EXPORT_SCHEMA

    def __init__(self, semantic_id, *, limits=None, discovery_profile="exact-v2", inventory=None):
        # This selected new-profile assembly requires the ordinary helper set.
        import portable_preview as P
        import ordinary_evidence as E
        import ordinary_semantics as S

        self.preview, self.evidence = P, E
        self.semantic_id = F.hexid(semantic_id)
        F.need(self.semantic_id == S.semantic_id(), "ORDINARY_SEMANTICS_NOT_SELECTED")
        self.limits = P.DEFAULT_LIMITS if limits is None else limits
        F.need(type(self.limits) is P.Limits, "ORDINARY_PREVIEW_LIMITS")
        Q._limits(self.limits)
        F.need(P.SCHEMA == PREVIEW_SCHEMA and P.LOCATOR_SCHEMA == LOCATOR_SCHEMA,
               "ORDINARY_PREVIEW_ASSEMBLY")
        self.discovery_profile = _profile(discovery_profile)
        self.namespace = namespace_for(self.semantic_id, discovery_profile=self.discovery_profile)
        self.pattern = self.pattern_inventory = None
        if self.discovery_profile == "type-pattern-v1":
            import ordinary_type_pattern as T
            self.pattern = T
            self.pattern_inventory = T.prepare_inventory(inventory)
        else:
            F.need(inventory is None, "ORDINARY_EXACT_INVENTORY_NOT_USED")

    def compile_query(self, specs):
        return compile_query(self.namespace, specs, discovery_profile=self.discovery_profile)

    def describe(self, raw, expected_id=None):
        P, E = self.preview, self.evidence
        preview = P.read_preview(raw, self.limits)
        doc = preview.document
        F.need(doc["semantic_id"] == self.semantic_id, "ORDINARY_PREVIEW_SEMANTICS")
        if expected_id is not None:
            F.need(preview.export_id == F.hexid(expected_id), "ORDINARY_EXPORT_ID_BINDING")
        specs, work = {}, 0

        def add(spec):
            nonlocal work
            key = feature_id(self.namespace, spec, discovery_profile=self.discovery_profile)
            F.need(key in specs or len(specs) < F.MAX_FEATURES,
                   "ORDINARY_FEATURE_PROFILE_EXHAUSTED")
            specs[key] = spec
            work += 1

        # The preview reader has established the exact reachable-type census.
        # These are only explicit const/projection names, not invented literal
        # dependencies or imported names that occur solely in a proof body.
        bound = {}
        add({"tag": "object-kind", "value": OBJECT_KIND})
        add({"tag": "declaration-kind", "value": KINDS[doc["header"][0]]})
        for name, identity in doc["type_bindings"]:
            symbol = {"kind": "portable-symbol", "symbol_id": identity}
            bound[E.name_key(name, self.limits.codec)] = symbol
            add({"tag": "type-symbol", "symbol": symbol})

        _, _, nodes, root = doc["header"][2]
        # All edges point backward. Compute each application's head ONCE;
        # shared application prefixes never expand into repeatedly traversed trees.
        spine = []
        for index, node in enumerate(nodes):
            spine.append(spine[node[1]] if node[0] == 3 else index)
            work += 1

        heads = {}

        def head(index):
            terminal = spine[index]
            if terminal in heads:
                return heads[terminal]
            node = nodes[terminal]
            result = {"tag": TAGS[node[0]]}
            if node[0] in (2, 8):
                result["symbol"] = bound[E.name_key(node[1], self.limits.codec)]
            heads[terminal] = result
            return result

        result = root
        while nodes[result][0] == 5:
            node = nodes[result]
            add({"tag": "binder-domain-head", "head": head(node[3])})
            result = node[4]
            work += 1
        add({"tag": "result-head", "head": head(result)})
        # Reuse the bounded type-only key helper. Its second preview parse is
        # intentional boundary validation, not proof/ancestor access. Work below
        # counts key-node visits, not whole-process parsing or physical CPU.
        exact_type = Q.preview_key(raw, self.limits)
        add({"tag": "declared-type-key", "value": exact_type["key"]})
        work += exact_type["key_node_visits"]
        pattern = None
        if self.discovery_profile == "type-pattern-v1":
            # Every old feature and this new required one must fit. Failure is
            # explicit; never drop a feature or fall back to the exact profile.
            F.need(len(specs) < F.MAX_FEATURES, "ORDINARY_PATTERN_FEATURE_PROFILE_EXHAUSTED")
            pattern = self.pattern.preview_pattern(raw, self.pattern_inventory, self.limits)
            key = feature_id(self.namespace, pattern["spec"], discovery_profile=self.discovery_profile)
            F.need(key not in specs, "ORDINARY_PATTERN_FEATURE_COLLISION")
            add(pattern["spec"])
            work += pattern["work"]
        locator = {"schema": LOCATOR_SCHEMA, "semantic_id": self.semantic_id,
                   "unit_id": doc["unit_id"], "export_name": deepcopy(doc["export_name"])}
        record = {"schema": F.ORDINARY_EXPORT_RECORD_SCHEMA, "namespace": self.namespace,
                  "kind": OBJECT_KIND, "object_id": preview.export_id,
                  "object_sha256": hashlib.sha256(raw).hexdigest(), "object_bytes": len(raw),
                  "features": sorted(specs), "locator": locator}
        F.validate_record(record, self.namespace)
        result = {"record": record, "specs": [specs[key] for key in sorted(specs)],
                "header": deepcopy(doc["header"]), "type_nodes": preview.type_nodes,
                "work": work, "mathematical_acceptance": False}
        if pattern is not None:
            result.update(pattern_profile=pattern["profile_id"],
                          pattern_work=pattern["work"], pattern_counters=pattern["counters"])
        return result

    def extract(self, raw, expected_id=None):
        return self.describe(raw, expected_id)["record"]

    def resolve(self, record, raw):
        """Bind candidate record to exact preview bytes, NOT to its full evidence.

        Index membership is another caller obligation; mathematical acceptance
        additionally requires exact evidence acquisition and independent checking.
        """
        F.validate_record(record, self.namespace)
        F.need(record["schema"] == F.ORDINARY_EXPORT_RECORD_SCHEMA,
               "ORDINARY_RECORD_REQUIRED")
        described = self.describe(raw, record["object_id"])
        F.need(described["record"] == record, "ORDINARY_PREVIEW_RECORD_BINDING")
        return {"export_id": record["object_id"], "locator": deepcopy(record["locator"]),
                "header": described["header"], "mathematical_acceptance": False,
                "assurance": "EXACT_PREVIEW_RECORD_BOUND_NOT_EVIDENCE_OR_MATHEMATICAL_ACCEPTANCE",
                "next_gate": "ACQUIRE_EXACT_PORTABLE_ORDINARY_EVIDENCE"}
