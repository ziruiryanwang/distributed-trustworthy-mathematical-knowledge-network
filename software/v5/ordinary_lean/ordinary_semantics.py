"""Candidate V2 identity descriptors, never mathematical or local authority.

Pure canonical-byte/identity support for a later coherent V2 assembly. No V1
reader/catalog is changed, no migration occurs, and no snapshot is made safe.
An implementation descriptor CLAIMS conformance; local adoption must separately
justify it, pin actual support, supervise checking and retain warrant lineage.
"""
from __future__ import annotations

import hashlib

import ordinary_evidence as E

FOUNDATION_SCHEMA = "DMKN_ORDINARY_FOUNDATION_CONTRACT_V1"
SEMANTIC_SCHEMA = "DMKN_ORDINARY_SEMANTIC_CONTRACT_V1"
IMPLEMENTATION_SCHEMA = "DMKN_ORDINARY_IMPLEMENTATION_CLAIM_V1"
EVIDENCE_SCHEMA = "DMKN_LEAN_ORDINARY_EVIDENCE_V2"
FOUNDATION_DOMAIN = "DMKN-ORDINARY-FOUNDATION-CONTRACT-V1"
SEMANTIC_DOMAIN = "DMKN-ORDINARY-SEMANTIC-CONTRACT-V1"
IMPLEMENTATION_DOMAIN = "DMKN-ORDINARY-IMPLEMENTATION-CLAIM-V1"
EVIDENCE_DOMAIN = "DMKN-ORDINARY-EVIDENCE-V2"
EXPORT_DOMAIN = "DMKN-ORDINARY-EXPORT-V2"
BASIS_SYMBOL_DOMAIN = "DMKN-ORDINARY-BASIS-SYMBOL-V2"
LOCAL_ROOT_DOMAIN = "DMKN-ORDINARY-LOCAL-ROOT-V2"

SEED = "a0acdc706f5e42dca21950c14db2307a18955c63ff953019aaff413d0a976001"
INVENTORY = "c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0"
LEAN_REVISION = "293d5d0c0c3f3dded4688b3ccd6a33939ac5102b"
# Fixed interpretation references, NOT hashes recomputed from an installed build.
# Later edits to prose do not silently change these references or old identities.
EXPRESSION_CONTRACT = "ae067c69c5a7a22727b356ccbdc17eb74e02657029a0c00ffd228d7baa10cdf4"
DECLARATION_CONTRACT = "5c9554cd4ea29357942c22b6f73e88e6ca8704c9903cff35ef5ed2c0dcf533f1"
DESCRIPTOR_LIMITS = E.Limits(max_bytes=32768, max_json_depth=16)


class SemanticError(ValueError):
    """Identity/profile refusal, never a mathematical invalidity verdict."""


def need(ok, code):
    if not ok:
        raise SemanticError(code)


def _digest_raw(domain, raw):
    return hashlib.sha256(domain.encode("ascii") + b"\0" + raw).hexdigest()


def _digest(domain, value):
    return _digest_raw(domain, E.canonical_json(value))


def foundation_bytes():
    """Exact current foundation contract. This does not reconstruct the basis."""
    return E.canonical_json({
        "schema": FOUNDATION_SCHEMA,
        "lean_revision": LEAN_REVISION,
        "seed_sha256": SEED,
        "inventory_sha256": INVENTORY,
        "units": 456,
        "names": 581,
        "initialization": {
            "start": "empty-constant-map-and-quotInit-false",
            "ordering": "fixed-seed-descriptors-in-encoded-order",
            "quotient": "kernel-quotDecl-exactly-once-final-quotInit-true",
            "axioms": "only-safe-axiom-descriptors-in-exact-fixed-seed",
            "definitions": "fixed-inventory-normalized-heights-not-source-heights",
            "result": "complete-actual-name-census-and-normalized-inventory-equality",
        },
    })


def read_foundation(raw):
    """Recognize the exact selected descriptor, not a foundation warrant."""
    doc = E.strict_json(raw, DESCRIPTOR_LIMITS)
    need(raw == foundation_bytes(), "FOUNDATION_CONTRACT_NOT_SELECTED")
    return doc


def foundation_id(raw=None):
    raw = foundation_bytes() if raw is None else raw
    read_foundation(raw)
    return _digest_raw(FOUNDATION_DOMAIN, raw)


def semantic_bytes():
    """Exact current portable interpretation; no implementation/artifact pins."""
    return E.canonical_json({
        "schema": SEMANTIC_SCHEMA,
        "foundation_id": foundation_id(),
        "lean_revision": LEAN_REVISION,
        "expression": {"format": E.EXPR_FORMAT, "contract_sha256": EXPRESSION_CONTRACT,
                       "projection": "erase-mdata-only-v1"},
        "declaration": {"format": E.UNIT_FORMAT, "contract_sha256": DECLARATION_CONTRACT,
                        "inventory": "exact-actual-generated-records-and-name-census"},
        "canonical_bytes": {
            "encoding": "UTF-8",
            "objects": "recursively-key-sorted",
            "separators": [",", ":"],
            "whitespace": "none-including-no-final-newline",
            "strings": "json-ensure_ascii-false",
            "numbers": "unsigned-decimal-integers-through-uint64-no-leading-zero",
            "excluded_tokens": ["boolean", "null", "negative", "fraction", "exponent", "nonfinite"],
        },
        "extension_policy": {
            "declarations": ["safe-definition", "theorem", "safe-opaque", "safe-inductive-group"],
            "forbidden_declarations": ["new-axiom", "quot-init", "unsafe", "partial"],
            "semantic_names": {
                "root": "nonanonymous-string-component-not-numeric-root",
                "forbidden_root_prefixes": ["_kernel_fresh", "_ind_fresh", "_nested_fresh", "_uniq", "_nested"],
                "forbidden_root_names": ["dontcare", "__expr_for_default_constructor__",
                                         "__local_decl_for_default_constructor"],
                "forbidden_exact_string_component_paths": [["sorryAx"], ["Lean", "reduceBool"],
                                                          ["Lean", "reduceNat"]],
                "scope": "declaration-and-semantic-reference-names-not-inert-binder-labels",
            },
            "parameters": "exact-original-ordered-universe-names",
            "dependencies": "exact-name-and-symbol-bindings-for-complete-direct-reference-census",
            "insertion": "kernel-checked-extension-of-warranted-parent-with-no-overwrite",
            "output": "actual-generated-inventory-equals-claim-and-no-unadvertised-name",
        },
    })


def read_semantic(raw):
    """Recognize selected interpretation bytes, not implementation conformance."""
    doc = E.strict_json(raw, DESCRIPTOR_LIMITS)
    need(raw == semantic_bytes(), "SEMANTIC_CONTRACT_NOT_SELECTED")
    return doc


def semantic_id(raw=None):
    raw = semantic_bytes() if raw is None else raw
    read_semantic(raw)
    return _digest_raw(SEMANTIC_DOMAIN, raw)


def read_implementation(raw):
    """Bounded exact support commitments; their existence/truth is NOT checked.

    Each support digest must be resolved/pinned by the eventual local adopter.
    A syntactically valid platform is not a claim that this project supports it.
    Only the current Lean 4.34 no-extension/no-IR snapshot format is recognized;
    this function does not implement a serializer-format upgrade or migration.
    """
    doc = E.strict_json(raw, DESCRIPTOR_LIMITS)
    need(type(doc) is dict and set(doc) == {
        "schema", "semantic_id", "platform", "kernel_support", "adapter_support",
        "basis_receiver_support", "controller_support", "snapshot_support",
        "snapshot_format", "support_scope"}, "IMPLEMENTATION_FIELDS")
    need(doc["schema"] == IMPLEMENTATION_SCHEMA, "IMPLEMENTATION_SCHEMA")
    need(E._hex(doc["semantic_id"]) == semantic_id(), "IMPLEMENTATION_SEMANTIC_NOT_SELECTED")
    for key in ("kernel_support", "adapter_support", "basis_receiver_support",
                "controller_support", "snapshot_support"):
        E._hex(doc[key])
    platform = doc["platform"]
    need(type(platform) is dict and set(platform) == {"os", "architecture", "word_bits", "byte_order"},
         "IMPLEMENTATION_PLATFORM_FIELDS")
    need(platform["os"] in ("windows", "linux", "darwin") and
         platform["architecture"] in ("x86_64", "aarch64") and
         type(platform["word_bits"]) is int and platform["word_bits"] == 64 and
         platform["byte_order"] == "little", "IMPLEMENTATION_PLATFORM")
    need(doc["snapshot_format"] == "LEAN_4_34_MODULEDATA_NO_EXTENSIONS_NO_IR",
         "IMPLEMENTATION_SNAPSHOT_FORMAT")
    need(doc["support_scope"] == "EXPLICIT_NAMED_SUPPORT_NOT_HERMETIC_TOOLCHAIN",
         "IMPLEMENTATION_SUPPORT_SCOPE")
    return doc


def implementation_id(raw):
    read_implementation(raw)
    return _digest_raw(IMPLEMENTATION_DOMAIN, raw)


def portable_unit_id(raw, limits=E.DEFAULT_LIMITS):
    """Identity of a bounded V2 CLAIM, even when its semantic ID is unsupported.

    Reuses the unchanged ordinary unit/name/reference validators. An eventual
    admission controller must match semantic_id to its selected contract and
    warranted dependency meanings before checking. This is not a V1 migration.
    """
    need(type(limits) is E.Limits, "SEMANTIC_EVIDENCE_LIMITS")
    doc = E.strict_json(raw, limits)
    need(type(doc) is dict and set(doc) == {"schema", "semantic_id", "imports", "unit"},
         "SEMANTIC_EVIDENCE_FIELDS")
    need(doc["schema"] == EVIDENCE_SCHEMA, "SEMANTIC_EVIDENCE_SCHEMA")
    E._hex(doc["semantic_id"])
    census = E.inspect_unit(doc["unit"], limits)
    keys = []
    for row in E._array(doc["imports"], maximum=limits.max_imports):
        name, symbol = E._array(row, 2)
        keys.append(E.name_key(name, limits))
        E._hex(symbol)
    need(tuple(keys) == census.external_names, "SEMANTIC_IMPORT_CENSUS_OR_ORDER")
    return _digest_raw(EVIDENCE_DOMAIN, raw)


def export_id(semantic, unit, original_name, limits=E.DEFAULT_LIMITS):
    """Claimed portable export ID; does not prove the unit exports this name."""
    E.name_key(original_name, limits)
    return _digest(EXPORT_DOMAIN, [E._hex(semantic), E._hex(unit), original_name])


def basis_symbol_id(semantic, foundation, original_name, limits=E.DEFAULT_LIMITS):
    """Claimed basis-symbol identity, not a local snapshot or basis warrant."""
    E.name_key(original_name, limits)
    return _digest(BASIS_SYMBOL_DOMAIN, [E._hex(semantic), E._hex(foundation), original_name])


def local_root_id(implementation_raw, store_id, kind, parent, request_hash):
    """Planned owner-local materialization identity, NOT a committed root.

    The protected record must separately bind actual artifact bytes, parent
    warrants and the clean checking event. No artifact may be loaded on this ID.
    """
    implementation = read_implementation(implementation_raw)
    need(kind in ("basis", "extension"), "LOCAL_ROOT_KIND")
    if kind == "basis":
        need(parent == "", "LOCAL_BASIS_PARENT")
    else:
        E._hex(parent)
    return _digest(LOCAL_ROOT_DOMAIN, [implementation["semantic_id"],
        _digest_raw(IMPLEMENTATION_DOMAIN, implementation_raw), E._hex(store_id),
        kind, parent, E._hex(request_hash)])
