"""Fifteen pure V2 boundary discriminators; root selects execution separately.

Synthetic inert syntax only: no Lean checking, catalog, filesystem writes,
network, certificates, supported alternate platform claim or V1 migration.
Reuse the small semantic_identity_checks fixtures without running that suite.
"""
from pathlib import Path
import copy
from dataclasses import replace
import hashlib
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ordinary_evidence as E
import ordinary_preview as P
import ordinary_semantics as S
import portable_evidence as PE
import portable_preview as PP
import semantic_identity_checks as Fixtures


def ensure(ok, code):
    if not ok:
        raise AssertionError(code)


def refuses(error_type, marker, action):
    try:
        action()
    except error_type as exc:
        ensure(marker in str(exc), "WRONG_REFUSAL:" + str(exc))
    else:
        raise AssertionError("MISSING_REFUSAL:" + marker)


def report(label):
    print("PORTABLE_IDENTITY_CHECK " + label + " PASS", flush=True)


def theorem_fixture(semantic):
    """Tiny claimed theorem with a proof-only external name; no warrant implied."""
    own = Fixtures.name("SyntheticIdentityDeclaration")
    truth = Fixtures.name("True")
    proof = Fixtures.name("SyntheticProofDependency")
    # A shared two-node True -> True type; the body is an unproved imported claim.
    type_dag = [E.EXPR_FORMAT, [], [[2, truth, []], [5, [], 0, 0, 0]], 1]
    proof_dag = [E.EXPR_FORMAT, [], [[2, proof, []]], 0]
    unit = [E.UNIT_FORMAT, [1, own, [], type_dag, proof_dag, [own]],
            [[own, 2, [], type_dag, [proof_dag, [own]]]]]
    imports = [[truth, "a" * 64], [proof, "b" * 64]]
    imports.sort(key=lambda row: E.name_key(row[0]))
    return E.canonical_json({"schema": PE.SCHEMA, "semantic_id": semantic,
                             "imports": imports, "unit": unit})


def main():
    semantic = S.semantic_id()
    own = Fixtures.name("SyntheticIdentityDeclaration")
    raw = Fixtures.evidence(semantic)
    evidence = PE.read_evidence(raw)
    unit = evidence.unit_id
    export = PE.export_id(semantic, unit, own)
    ensure(unit == S.portable_unit_id(raw) == PE.portable_unit_id(raw) and
           not evidence.mathematical_acceptance, "EXACT_V2_ID_DEFINITION")
    report("identity_definition_and_nonacceptance")

    first = Fixtures.implementation()
    second = copy.deepcopy(first)
    second["platform"]["os"] = "linux"
    second["kernel_support"] = "6" * 64
    first_raw, second_raw = E.canonical_json(first), E.canonical_json(second)
    ensure(S.implementation_id(first_raw) != S.implementation_id(second_raw) and
           S.local_root_id(first_raw, "1" * 64, "basis", "", "2" * 64) !=
           S.local_root_id(second_raw, "3" * 64, "basis", "", "2" * 64) and
           PE.read_evidence(Fixtures.evidence(first["semantic_id"])).unit_id ==
           PE.read_evidence(Fixtures.evidence(second["semantic_id"])).unit_id == unit,
           "IMPLEMENTATION_STORE_INDEPENDENCE")
    located = copy.deepcopy(evidence.document)
    located["location"] = "not-a-mathematical-field"
    refuses(E.EvidenceError, "PORTABLE_EVIDENCE_FIELDS",
            lambda: PE.read_evidence(E.canonical_json(located)))
    report("implementation_store_location_separation")

    changed = copy.deepcopy(evidence.document)
    one = [E.EXPR_FORMAT, [], [[7, {"$bytes": [1]}]], 0]
    changed["unit"][1][4] = one
    changed["unit"][2][0][4][0] = one
    changed_unit = PE.read_evidence(E.canonical_json(changed)).unit_id
    ensure(changed_unit != unit and PE.export_id(semantic, changed_unit, own) != export,
           "UNIT_CONTENT_NOT_BOUND")
    report("exact_unit_discrimination")

    changed = copy.deepcopy(evidence.document)
    changed["imports"][0][1] = "d" * 64
    ensure(PE.read_evidence(E.canonical_json(changed)).unit_id != unit,
           "EXACT_IMPORT_ID_NOT_BOUND")
    report("exact_import_discrimination")

    other = "0" * 64 if semantic != "0" * 64 else "1" * 64
    unsupported = copy.deepcopy(evidence.document)
    unsupported["semantic_id"] = other
    unsupported_raw = E.canonical_json(unsupported)
    unsupported_evidence = PE.read_evidence(unsupported_raw)
    unsupported_preview = PP.preview_from_evidence(unsupported_raw, own)
    ensure(unsupported_evidence.unit_id != unit and
           not PP.describe(unsupported_preview)["mathematical_acceptance"] and
           not PP.resolve(unsupported_preview, unsupported_raw)["mathematical_acceptance"],
           "UNKNOWN_SEMANTICS_MUST_REMAIN_METADATA")
    second["semantic_id"] = other
    refuses(S.SemanticError, "IMPLEMENTATION_SEMANTIC_NOT_SELECTED",
            lambda: S.implementation_id(E.canonical_json(second)))
    report("semantic_discrimination_without_adoption")

    method_raw = theorem_fixture(semantic)
    method = PE.read_evidence(method_raw)
    for mutation in ("missing", "extra", "duplicate", "reordered"):
        bad = copy.deepcopy(method.document)
        if mutation == "missing":
            bad["imports"].pop()
        elif mutation == "extra":
            bad["imports"].append([Fixtures.name("Unreferenced"), "c" * 64])
            bad["imports"].sort(key=lambda row: E.name_key(row[0]))
        elif mutation == "duplicate":
            bad["imports"].append(copy.deepcopy(bad["imports"][0]))
        else:
            bad["imports"].reverse()
        refuses(E.EvidenceError, "PORTABLE_IMPORT_CENSUS_OR_ORDER",
                lambda bad=bad: PE.read_evidence(E.canonical_json(bad)))
    report("complete_ordered_direct_import_census")

    preview_raw = PP.preview_from_evidence(method_raw, own)
    preview = PP.read_preview(preview_raw)
    description = PP.describe(preview_raw)
    bound = PP.resolve(preview_raw, method_raw)
    ensure(preview.document["type_bindings"] == [[Fixtures.name("True"), "a" * 64]] and
           E.canonical_json(Fixtures.name("SyntheticProofDependency")) not in preview_raw and
           preview.type_nodes == 2 and not preview.mathematical_acceptance and
           not description["mathematical_acceptance"] and
           not bound["mathematical_acceptance"] and
           bound["assurance"] == PP.BOUND_ASSURANCE,
           "EXACT_TYPE_ONLY_PREVIEW")
    report("type_only_projection_and_exact_binding")

    bad = copy.deepcopy(method.document)
    bad["imports"][0][1] = "e" * 64
    refuses(P.PreviewError, "PREVIEW_EVIDENCE_ID_MISMATCH",
            lambda: PP.resolve(preview_raw, E.canonical_json(bad)))
    report("different_evidence_refused")

    bad = copy.deepcopy(preview.document)
    bad["export_name"] = Fixtures.name("NotExported")
    refuses(P.PreviewError, "PREVIEW_EXPORT_NOT_IN_UNIT",
            lambda: PP.resolve(E.canonical_json(bad), method_raw))
    bad = copy.deepcopy(preview.document)
    bad["export_id"] = preview.export_id
    refuses(P.PreviewError, "PORTABLE_PREVIEW_FIELDS",
            lambda: PP.read_preview(E.canonical_json(bad)))
    report("forged_export_and_extra_preview_fields")

    locator = copy.deepcopy(description["locator"])
    detached = PP.read_locator(locator)
    locator["export_name"][0][1]["$bytes"][0] = 88
    ensure(detached == description["locator"], "LOCATOR_NAME_ALIAS")
    for key, value in (("provider", "untrusted-location"), ("profile_id", semantic)):
        bad = copy.deepcopy(detached)
        bad[key] = value
        refuses(P.PreviewError, "PORTABLE_LOCATOR_FIELDS", lambda bad=bad: PP.read_locator(bad))
    bad = copy.deepcopy(detached)
    bad["unit_id"] = "not-a-hash"
    refuses(E.EvidenceError, "HASH_ENCODING", lambda: PP.read_locator(bad))
    report("strict_detached_portable_locator")

    bad = copy.deepcopy(preview.document)
    bad["header"][0] = 1
    refuses(P.PreviewError, "PREVIEW_EVIDENCE_HEADER_OR_BINDINGS_MISMATCH",
            lambda: PP.resolve(E.canonical_json(bad), method_raw))
    bad = copy.deepcopy(preview.document)
    # Well-formed metadata for True, but not this theorem's True -> True header.
    bad["header"][2] = [E.EXPR_FORMAT, [], [[2, Fixtures.name("True"), []]], 0]
    refuses(P.PreviewError, "PREVIEW_EVIDENCE_HEADER_OR_BINDINGS_MISMATCH",
            lambda: PP.resolve(E.canonical_json(bad), method_raw))
    report("forged_kind_and_type_refused")

    bad = copy.deepcopy(preview.document)
    bad["type_bindings"][0][1] = "f" * 64
    refuses(P.PreviewError, "PREVIEW_EVIDENCE_HEADER_OR_BINDINGS_MISMATCH",
            lambda: PP.resolve(E.canonical_json(bad), method_raw))
    bad["type_bindings"] = []
    refuses(P.PreviewError, "PREVIEW_TYPE_BINDING_CENSUS_OR_ORDER",
            lambda: PP.read_preview(E.canonical_json(bad)))
    report("forged_and_missing_type_bindings")

    refuses(P.PreviewError, "PREVIEW_TYPE_NODE_BOUND",
            lambda: PP.read_preview(preview_raw, replace(PP.DEFAULT_LIMITS, max_type_nodes=1)))
    bad = copy.deepcopy(preview.document)
    # Keep the shared codec's root-last/backward-edge contract valid. Node0 is
    # unreachable; shifted nodes1/2 still encode the same True -> True root.
    bad["header"][2] = [E.EXPR_FORMAT, [], [
        [7, {"$bytes": []}], [2, Fixtures.name("True"), []], [5, [], 0, 1, 1]], 2]
    refuses(P.PreviewError, "PREVIEW_ORPHAN_TYPE_NODE",
            lambda: PP.read_preview(E.canonical_json(bad)))
    report("selected_type_bound_and_orphan_refusal")

    legacy = copy.deepcopy(evidence.document)
    legacy["schema"] = "DMKN_LEAN_ORDINARY_EVIDENCE_V1"
    legacy["profile_id"] = legacy.pop("semantic_id")
    legacy_raw = E.canonical_json(legacy)
    fixed_domain_id = hashlib.sha256(b"DMKN-ORDINARY-EVIDENCE-V1\0" + legacy_raw).hexdigest()
    ensure(E.read_evidence(legacy_raw).unit_id == fixed_domain_id ==
           E.read_evidence(legacy_raw).unit_id and fixed_domain_id != unit,
           "V1_DETERMINISTIC_DOMAIN_CHANGED")
    refuses(E.EvidenceError, "EVIDENCE_FIELDS", lambda: E.read_evidence(raw))
    refuses(E.EvidenceError, "PORTABLE_EVIDENCE_FIELDS", lambda: PE.read_evidence(legacy_raw))
    legacy_preview = P.preview_from_evidence(legacy_raw, own)
    refuses(P.PreviewError, "PREVIEW_FIELDS", lambda: P.read_preview(preview_raw))
    refuses(P.PreviewError, "PORTABLE_PREVIEW_FIELDS", lambda: PP.read_preview(legacy_preview))
    report("v1_v2_separation_and_fixed_v1_digest")

    forged_wrapper = PE.Evidence(method_raw, {"semantic_id": "f" * 64}, "f" * 64,
                                 E.UnitCensus((), (), 0))
    ensure(PP.preview_from_evidence(forged_wrapper, own) == preview_raw and
           PP.resolve(preview_raw, forged_wrapper) == bound, "MUTABLE_WRAPPER_BYPASS")
    report("wrapper_fields_are_not_authority")
    print("PORTABLE_IDENTITY_ALL_PASS checks=15 mathematical_acceptance=false", flush=True)


if __name__ == "__main__":
    main()
