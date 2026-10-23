"""Pure proposed identity discriminators; root must select execution separately.

Synthetic inert declarations/support commitments, not checked mathematics,
supported alternate platforms, native snapshots or a V1 migration.
"""
from pathlib import Path
import copy
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ordinary_evidence as E
import ordinary_semantics as S


def ensure(ok, code):
    if not ok:
        raise AssertionError(code)


def refuses(kind, marker, action):
    try:
        action()
    except kind as exc:
        ensure(marker in str(exc), "WRONG_REFUSAL:" + str(exc))
    else:
        raise AssertionError("MISSING_REFUSAL:" + marker)


def name(text):
    return [[0, {"$bytes": list(text.encode("utf-8"))}]]


def evidence(semantic):
    own, nat = name("SyntheticIdentityDeclaration"), name("Nat")
    type_dag = [E.EXPR_FORMAT, [], [[2, nat, []]], 0]
    value_dag = [E.EXPR_FORMAT, [], [[7, {"$bytes": []}]], 0]
    unit = [E.UNIT_FORMAT,
            [0, own, [], type_dag, value_dag, [2, 1], [own]],
            [[own, 1, [], type_dag, [value_dag, [2, 1], [own]]]]]
    return E.canonical_json({"schema": S.EVIDENCE_SCHEMA, "semantic_id": semantic,
        "imports": [[nat, S.basis_symbol_id(semantic, S.foundation_id(), nat)]], "unit": unit})


def implementation():
    return {"schema": S.IMPLEMENTATION_SCHEMA, "semantic_id": S.semantic_id(),
        "platform": {"os": "windows", "architecture": "x86_64", "word_bits": 64, "byte_order": "little"},
        "kernel_support": "1" * 64, "adapter_support": "2" * 64,
        "basis_receiver_support": "3" * 64, "controller_support": "4" * 64,
        "snapshot_support": "5" * 64,
        "snapshot_format": "LEAN_4_34_MODULEDATA_NO_EXTENSIONS_NO_IR",
        "support_scope": "EXPLICIT_NAMED_SUPPORT_NOT_HERMETIC_TOOLCHAIN"}


def main():
    s, f = S.semantic_id(), S.foundation_id()
    ensure(S.semantic_id(S.semantic_bytes()) == s and S.foundation_id(S.foundation_bytes()) == f,
           "EXACT_DESCRIPTOR_DETERMINISM")
    changed = S.read_foundation(S.foundation_bytes())
    changed["seed_sha256"] = "0" * 64
    refuses(S.SemanticError, "FOUNDATION_CONTRACT_NOT_SELECTED",
            lambda: S.foundation_id(E.canonical_json(changed)))
    semantic_doc = S.read_semantic(S.semantic_bytes())
    semantic_doc["controller_support"] = "0" * 64
    refuses(S.SemanticError, "SEMANTIC_CONTRACT_NOT_SELECTED",
            lambda: S.semantic_id(E.canonical_json(semantic_doc)))
    refuses(E.EvidenceError, "JSON_LEXICAL_TOKEN", lambda: S.read_semantic(S.semantic_bytes() + b"\n"))
    print("SEMANTIC_IDENTITY_CHECK exact_selected_descriptors PASS", flush=True)

    raw = evidence(s)
    unit = S.portable_unit_id(raw)
    export = S.export_id(s, unit, name("SyntheticIdentityDeclaration"))
    first = implementation()
    second = copy.deepcopy(first)
    second["platform"]["os"] = "linux"
    second["kernel_support"] = "6" * 64
    second["controller_support"] = "7" * 64
    first_raw, second_raw = E.canonical_json(first), E.canonical_json(second)
    ensure(S.implementation_id(first_raw) != S.implementation_id(second_raw), "DISTINCT_IMPLEMENTATIONS")
    root_a = S.local_root_id(first_raw, "a" * 64, "basis", "", "b" * 64)
    root_b = S.local_root_id(second_raw, "a" * 64, "basis", "", "b" * 64)
    ensure(root_a != root_b and S.portable_unit_id(raw) == unit and
           S.export_id(s, S.portable_unit_id(raw), name("SyntheticIdentityDeclaration")) == export,
           "PORTABLE_ID_INDEPENDENT_OF_LOCAL_SUPPORT")
    ensure(root_a != S.local_root_id(first_raw, "c" * 64, "basis", "", "b" * 64), "STORE_LINEAGE_SEPARATE")
    print("SEMANTIC_IDENTITY_CHECK implementation_separation PASS", flush=True)

    # Unknown S is syntactically hashable, never a selected/adopted semantics.
    other = "0" * 64 if s != "0" * 64 else "1" * 64
    other_raw = evidence(other)
    other_unit = S.portable_unit_id(other_raw)
    ensure(other_unit != unit and S.export_id(other, other_unit, name("SyntheticIdentityDeclaration")) != export,
           "SEMANTIC_CLAIM_CHANGES_PORTABLE_ID")
    ensure(S.basis_symbol_id(s, f, name("Nat")) != S.basis_symbol_id(other, f, name("Nat")),
           "SEMANTIC_CLAIM_CHANGES_BASIS_SYMBOL")
    second["semantic_id"] = other
    refuses(S.SemanticError, "IMPLEMENTATION_SEMANTIC_NOT_SELECTED",
            lambda: S.implementation_id(E.canonical_json(second)))
    print("SEMANTIC_IDENTITY_CHECK changed_semantics_not_adopted PASS", flush=True)

    legacy = E.strict_json(raw)
    legacy["schema"] = E.SCHEMA
    legacy["profile_id"] = legacy.pop("semantic_id")
    refuses(S.SemanticError, "SEMANTIC_EVIDENCE_FIELDS",
            lambda: S.portable_unit_id(E.canonical_json(legacy)))
    ensure(E.read_evidence(E.canonical_json(legacy)).unit_id != unit, "V1_V2_DOMAIN_SEPARATION")
    bad = E.strict_json(raw)
    bad["imports"].append(copy.deepcopy(bad["imports"][0]))
    refuses(S.SemanticError, "SEMANTIC_IMPORT_CENSUS_OR_ORDER",
            lambda: S.portable_unit_id(E.canonical_json(bad)))
    refuses(S.SemanticError, "LOCAL_BASIS_PARENT",
            lambda: S.local_root_id(first_raw, "a" * 64, "basis", root_a, "b" * 64))
    refuses(E.EvidenceError, "HASH_ENCODING",
            lambda: S.local_root_id(first_raw, "a" * 64, "extension", "", "b" * 64))
    print("SEMANTIC_IDENTITY_CHECK no_legacy_or_parent_relabel PASS", flush=True)
    print("SEMANTIC_IDENTITY_ALL_PASS checks=4 mathematical_acceptance=false", flush=True)


if __name__ == "__main__":
    main()
