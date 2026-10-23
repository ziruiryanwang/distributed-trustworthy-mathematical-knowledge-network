"""Proof-free portable V2 type advertisements; never mathematical authority.

Read/describe inspect only one bounded selected type DAG and its exact symbolic
bindings. Generation/resolution additionally parse the selected full unit once,
but never fetch or replay imported proof history. Index membership and preview
binding remain distinct from independent mathematical acceptance.

The existing ordinary_preview type-DAG validator and trusted limits are reused.
This module changes only the portable envelope/identity projection, not the Lean
grammar, V1 bytes, native checker, local catalog or any acceptance rule.
"""
from __future__ import annotations

import hashlib

import ordinary_evidence as E
import ordinary_preview as P
import portable_evidence as PE


SCHEMA = "DMKN_ORDINARY_LEAN_TYPE_PREVIEW_V2"
LOCATOR_SCHEMA = "DMKN_ORDINARY_LEAN_EXPORT_LOCATOR_V2"
PREVIEW_ASSURANCE = P.PREVIEW_ASSURANCE
BOUND_ASSURANCE = P.BOUND_ASSURANCE
Limits = P.Limits
DEFAULT_LIMITS = P.DEFAULT_LIMITS
Preview = P.Preview
PreviewError = P.PreviewError


def read_locator(value, limits=DEFAULT_LIMITS):
    """Validate an exact V2 locator claim; it proves neither existence nor truth.

    S binds F; implementation details/paths/provider addresses are not locators.
    Return a detached value so later caller mutation cannot alias validated names.
    Like every parsed object, the returned value itself grants no authority.
    """
    P._need(type(limits) is Limits, "PREVIEW_LIMIT_CONFIGURATION")
    P._need(type(value) is dict and set(value) == {
        "schema", "semantic_id", "unit_id", "export_name"}, "PORTABLE_LOCATOR_FIELDS")
    P._need(value["schema"] == LOCATOR_SCHEMA, "PORTABLE_LOCATOR_SCHEMA")
    semantic = E._hex(value["semantic_id"])
    unit = E._hex(value["unit_id"])
    name = E.name_key(value["export_name"], limits.codec)
    result = {"schema": LOCATOR_SCHEMA, "semantic_id": semantic,
              "unit_id": unit, "export_name": E.strict_json(name, limits.codec)}
    P._need(len(E.canonical_json(result)) <= limits.codec.max_bytes,
            "PORTABLE_LOCATOR_BYTE_BOUND")
    return result


def read_preview(raw, limits=DEFAULT_LIMITS):
    """Bounded V2 advertisement parsing, including unsupported semantic IDs.

    The portable ID commits to the claim. Recognizing supported S/F and proving
    the claim are separate controller operations; no network or kernel is used.
    """
    P._need(type(limits) is Limits, "PREVIEW_LIMIT_CONFIGURATION")
    doc = E.strict_json(raw, limits.codec)
    P._need(type(doc) is dict and set(doc) == {
        "schema", "semantic_id", "unit_id", "export_name", "header", "type_bindings"},
        "PORTABLE_PREVIEW_FIELDS")
    P._need(doc["schema"] == SCHEMA, "PORTABLE_PREVIEW_SCHEMA")
    E._hex(doc["semantic_id"])
    E._hex(doc["unit_id"])
    E.name_key(doc["export_name"], limits.codec)
    refs, nodes = P._type_census(doc["header"], limits)
    keys = []
    for row in E._array(doc["type_bindings"], maximum=limits.max_type_bindings):
        name, symbol = E._array(row, 2)
        keys.append(E.name_key(name, limits.codec))
        E._hex(symbol)
    P._need(tuple(keys) == refs, "PREVIEW_TYPE_BINDING_CENSUS_OR_ORDER")
    export = PE.export_id(doc["semantic_id"], doc["unit_id"], doc["export_name"], limits.codec)
    return Preview(raw, doc, export, refs, nodes)


def _read_exact_evidence(evidence, expected_unit=None):
    # Public instances and their mutable documents are not validation tokens.
    raw = evidence.raw if type(evidence) is PE.Evidence else evidence
    P._need(type(raw) is bytes and 0 < len(raw) <= PE.DEFAULT_LIMITS.max_bytes,
            "PREVIEW_EVIDENCE_BYTES")
    exact = PE.read_evidence(raw)
    if expected_unit is not None:
        P._need(exact.unit_id == expected_unit, "PREVIEW_EVIDENCE_ID_MISMATCH")
    return exact


def _from_checked_syntax(evidence, export_name, limits):
    """Projection from freshly parsed syntax, NOT checked mathematics."""
    key = E.name_key(export_name, limits.codec)
    doc = evidence.document
    selected = None
    for row in doc["unit"][2]:
        if E.name_key(row[0]) == key:
            selected = row
            break
    P._need(selected is not None, "PREVIEW_EXPORT_NOT_IN_UNIT")
    header = [selected[1], selected[2], selected[3]]
    refs, _ = P._type_census(header, limits)
    own_names = set(evidence.census.expected_names)
    imported = {E.name_key(name): symbol for name, symbol in doc["imports"]}
    bindings = []
    for reference in refs:
        name = E.strict_json(reference, limits.codec)
        if reference in own_names:
            symbol = PE.export_id(doc["semantic_id"], evidence.unit_id, name, limits.codec)
        else:
            P._need(reference in imported, "PREVIEW_UNBOUND_TYPE_REFERENCE")
            symbol = imported[reference]
        bindings.append([name, symbol])
    raw = E.canonical_json({"schema": SCHEMA, "semantic_id": doc["semantic_id"],
        "unit_id": evidence.unit_id, "export_name": selected[0],
        "header": header, "type_bindings": bindings})
    # Enforce the same bounded external read contract on generated previews.
    read_preview(raw, limits)
    return raw


def preview_from_evidence(evidence, export_name, limits=DEFAULT_LIMITS):
    """Return one proof-free preview; parse selected evidence once, not ancestry.

    Evidence can be bounded raw V2 bytes or this module's inert Evidence wrapper.
    Only the selected header and type bindings are published. Publication does not
    warrant them, and a preview-size refusal is not mathematical invalidity.
    """
    P._need(type(limits) is Limits, "PREVIEW_LIMIT_CONFIGURATION")
    return _from_checked_syntax(_read_exact_evidence(evidence), export_name, limits)


def _description(preview, assurance, next_gate):
    doc = preview.document
    return {"assurance": assurance, "mathematical_acceptance": False,
        "next_gate": next_gate, "object_id": preview.export_id,
        "object_sha256": hashlib.sha256(preview.raw).hexdigest(),
        "object_bytes": len(preview.raw), "type_nodes": preview.type_nodes,
        "locator": {"schema": LOCATOR_SCHEMA, "semantic_id": doc["semantic_id"],
                    "unit_id": doc["unit_id"], "export_name": doc["export_name"]}}


def describe(raw, limits=DEFAULT_LIMITS):
    """Describe exact advertised bytes, not index membership or accepted math."""
    return _description(read_preview(raw, limits), PREVIEW_ASSURANCE,
                        "ACQUIRE_EXACT_PORTABLE_ORDINARY_EVIDENCE")


def resolve(raw, evidence, limits=DEFAULT_LIMITS):
    """Bind selected advertised metadata to exact inert V2 evidence.

    Even a successful result does not adopt S, warrant F/imports, check a proof,
    load a native artifact or promote a catalog entry. The protected controller
    still performs all those applicable gates independently.
    """
    preview = read_preview(raw, limits)
    exact = _read_exact_evidence(evidence, preview.document["unit_id"])
    P._need(exact.document["semantic_id"] == preview.document["semantic_id"],
            "PREVIEW_EVIDENCE_SEMANTIC_MISMATCH")
    expected = _from_checked_syntax(exact, preview.document["export_name"], limits)
    P._need(expected == raw, "PREVIEW_EVIDENCE_HEADER_OR_BINDINGS_MISMATCH")
    return _description(preview, BOUND_ASSURANCE,
                        "SELECT_SEMANTICS_MATCH_WARRANTED_DEPENDENCIES_AND_CHECK_EXTENSION")
