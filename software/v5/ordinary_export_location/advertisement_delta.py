"""Derive inert publication proposals from one selected new baseline bundle.

Pure bytes only: no filesystem, network, owner, database or native execution.
Every unit output is eligible, including support-only declarations. The caller
must read bounded units using manifest-derived paths and must separately check
its approved custodian's exact locator before publishing a selected proposal.
"""
from __future__ import annotations

import hashlib

import baseline_bundle as B
import ordinary_evidence as E
import ordinary_semantics as S
import portable_evidence as PE

MIB = 1024**2
SCHEMA = "DMKN_ORDINARY_EXPORT_ADVERTISEMENT_DELTA_V1"
MAX_UNITS, MAX_BYTES, MAX_SELECTED = 256, 8*MIB, 4096
MAX_SCANNED_OUTPUTS, MAX_PROPOSAL_BYTES = 65536, 2*MIB
LIMITS = B.Limits(max_units=MAX_UNITS, max_bytes=MAX_BYTES,
                 max_names=MAX_SCANNED_OUTPUTS, max_batch_units=MAX_UNITS,
                 max_batch_bytes=MAX_BYTES)


def need(ok, code):
    if not ok:
        raise ValueError("ADVERTISEMENT_DELTA_"+code)


def check(callback):
    if callback is not None:
        callback()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def manifest(raw, expected_sha256, *, check_budget=None):
    """Authenticate the finite input census before the caller reads unit files."""
    need(check_budget is None or callable(check_budget), "BUDGET_CALLBACK")
    check(check_budget)
    result = B.read_manifest(raw, expected_sha256, limits=LIMITS,
                             check_budget=check_budget)
    need(result.semantic_id == S.semantic_id(), "SEMANTICS")
    check(check_budget)
    return result


def prepare(manifest_raw, manifest_sha256, unit_raws, *, selected_export_ids=None,
            check_budget=None):
    """Validate a selected bundle and return exact all-output/subset proposals.

    unit_raws must be in the manifest's flattened batch order. Explicit selected
    IDs are a finite operator subset, not source targets or mathematical quality
    judgments. None means every output, subject to the fixed publication ceiling.
    An over-cap all-output proposal refuses; it is never silently truncated.
    """
    held = manifest(manifest_raw, manifest_sha256, check_budget=check_budget)
    need(type(unit_raws) in (list, tuple) and len(unit_raws) == held.unit_count,
         "EXACT_UNIT_COUNT")
    entries = tuple(entry for batch in held.batches for entry in batch)
    need(len(entries) == len(unit_raws) and
         all(type(raw) is bytes and 0 < len(raw) <= MAX_BYTES for raw in unit_raws)
         and sum(len(raw) for raw in unit_raws) == held.evidence_bytes <= MAX_BYTES,
         "EXACT_UNIT_BYTES")
    selected = None
    if selected_export_ids is not None:
        need(type(selected_export_ids) in (list, tuple) and
             1 <= len(selected_export_ids) <= MAX_SELECTED, "SELECTED_COUNT")
        for identity in selected_export_ids:
            E._hex(identity)
        need(len(set(selected_export_ids)) == len(selected_export_ids), "DUPLICATE_SELECTION")
        selected = frozenset(selected_export_ids)

    proposed, seen, unit_pins = [], set(), []
    output_count, proposal_bytes, nodes, edges = 0, 2, 0, 0
    for entry, raw in zip(entries, unit_raws):
        check(check_budget)
        need(len(raw) == entry.raw_bytes and digest(raw) == entry.raw_sha256,
             "UNIT_RAW_PIN")
        parsed = PE.read_evidence(raw)
        check(check_budget)
        need(parsed.unit_id == entry.unit_id and
             parsed.document["semantic_id"] == held.semantic_id, "UNIT_IDENTITY")
        nodes += parsed.census.total_nodes
        edges += len(parsed.document["imports"])
        need(nodes <= LIMITS.max_nodes and edges <= LIMITS.max_edges, "PARSED_AGGREGATE")
        unit_pins.append(dict(unit_id=entry.unit_id, raw_sha256=entry.raw_sha256,
                              raw_bytes=entry.raw_bytes))
        for declaration in parsed.document["unit"][2]:
            check(check_budget)
            output_count += 1
            need(output_count <= MAX_SCANNED_OUTPUTS, "OUTPUT_CENSUS_CAP")
            name = declaration[0]
            identity = S.export_id(held.semantic_id, entry.unit_id, name)
            if selected is not None and identity not in selected:
                continue
            need(identity not in seen and len(proposed) < MAX_SELECTED, "PROPOSAL_COUNT_OR_COLLISION")
            row = dict(semantic_id=held.semantic_id, export_id=identity,
                       unit_id=entry.unit_id, name=name)
            encoded = E.canonical_json(row)
            proposal_bytes += len(encoded)+int(bool(proposed))
            need(proposal_bytes <= MAX_PROPOSAL_BYTES, "PROPOSAL_BYTE_CAP")
            seen.add(identity)
            proposed.append(row)
    need(selected is None or seen == selected, "SELECTED_EXPORT_NOT_IN_BUNDLE")
    check(check_budget)
    document = dict(schema=SCHEMA, semantic_id=held.semantic_id,
        manifest_sha256=held.sha256, unit_pins=unit_pins,
        proposals=proposed, selected_output_count=len(proposed),
        total_output_count=output_count, omitted_output_count=output_count-len(proposed),
        selection="ALL_OUTPUTS" if selected is None else "EXPLICIT_EXPORT_SUBSET",
        custody_checked=False, published=False, mathematical_acceptance=False,
        assurance="INERT_BUNDLE_IDENTITIES_NOT_CUSTODY_OR_AVAILABILITY")
    result = E.canonical_json(document)
    need(len(result) <= MAX_PROPOSAL_BYTES, "DOCUMENT_BYTE_CAP")
    check(check_budget)
    return result
