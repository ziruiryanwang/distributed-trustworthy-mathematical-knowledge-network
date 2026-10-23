"""Portable ordinary-Lean V2 syntax/identity, never mathematical acceptance.

The semantic descriptor S commits to the foundation F and the interpretation of
unchanged ordinary unit syntax. Local implementation, store, native snapshot and
checking-event identities are deliberately absent from portable evidence. Their
protected warrant relation remains a separate local-catalog obligation.

This reader recognizes bounded claims even for an unsupported S. A successful
parse is NOT recognition/adoption of that interpretation. Controllers must select
the exact semantic descriptor, resolve warranted imports and check the actual unit.
All Lean/name/DAG grammar is reused from ordinary_evidence; V1 is unchanged.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib

import ordinary_evidence as E
import ordinary_semantics as S


SCHEMA = S.EVIDENCE_SCHEMA
EVIDENCE_DOMAIN = S.EVIDENCE_DOMAIN
Limits = E.Limits
DEFAULT_LIMITS = E.DEFAULT_LIMITS
EvidenceError = E.EvidenceError
# These are the selected portable identity definitions, not new hash formulas.
export_id = S.export_id
basis_symbol_id = S.basis_symbol_id


@dataclass(frozen=True)
class Evidence:
    """Inert claim. The document is mutable; reparse raw at changed boundaries."""

    raw: bytes
    document: dict
    unit_id: str
    census: E.UnitCensus

    @property
    def mathematical_acceptance(self):
        return False


def read_evidence(raw, limits=DEFAULT_LIMITS):
    """One strict parse and unit census; no checking, I/O or profile adoption.

    Exact canonical bytes bind S, every direct import and the complete raw unit.
    Import order/census is the same contract as ordinary_semantics.portable_unit_id.
    An identity can therefore exist before (or without) mathematical acceptance.
    """
    E._need(type(limits) is E.Limits, "PORTABLE_EVIDENCE_LIMITS")
    document = E.strict_json(raw, limits)
    E._need(type(document) is dict and set(document) == {
        "schema", "semantic_id", "imports", "unit"}, "PORTABLE_EVIDENCE_FIELDS")
    E._need(document["schema"] == SCHEMA, "PORTABLE_EVIDENCE_SCHEMA")
    E._hex(document["semantic_id"])
    census = E.inspect_unit(document["unit"], limits)
    keys = []
    for row in E._array(document["imports"], maximum=limits.max_imports):
        name, symbol = E._array(row, 2)
        keys.append(E.name_key(name, limits))
        E._hex(symbol)
    E._need(tuple(keys) == census.external_names,
            "PORTABLE_IMPORT_CENSUS_OR_ORDER")
    # census.external_names is sorted and duplicate-free; equality establishes
    # exact ordered imports, including references occurring only inside proofs.
    unit_id = hashlib.sha256(EVIDENCE_DOMAIN.encode("ascii") + b"\0" + raw).hexdigest()
    return Evidence(raw, document, unit_id, census)


def portable_unit_id(raw, limits=DEFAULT_LIMITS):
    """Validated V2 content identity, equal to ordinary_semantics' definition."""
    return read_evidence(raw, limits).unit_id
