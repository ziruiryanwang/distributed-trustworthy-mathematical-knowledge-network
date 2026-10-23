"""Pure portable completion planning; no execution, state mutation or authority.

The retained consumer is validated FIRST against its original prepared map and
the real protected parent. A separately supplied complete-proof supplement may
fill exactly its genuinely missing names. Both lanes then pass the existing
portable binder as one bounded graph against that SAME parent, never a pretend
accepted context augmented with provisional supplemental outputs.

The V1 missing-import wrapper is only an inert field layout here: profile_id
must already equal the requested portable semantic ID, basis_id the portable
foundation ID, and context_id the exact parent. Genuine legacy IDs are NOT
translated or adopted. Caller selects compatible pure support and a stable
protected lookup; only later owner.preflight/admit can accept the returned units.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib

import portable_candidate as B

E = B.E
SUPPLEMENT_SCHEMA = "DMKN_ORDINARY_MISSING_IMPORT_BUNDLE_V1"


def need(condition, code):
    if not condition:
        raise ValueError(code)


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class CompletionPlan:
    status: str
    semantic_id: str
    foundation_id: str
    context_root: str
    raw_units: tuple[bytes, ...]
    consumer_targets: tuple[bytes, ...]
    supplemental_targets: tuple[bytes, ...]
    candidate_sha256: str
    supplement_sha256: str
    composite_sha256: str
    consumer_unit_sha256s: tuple[str, ...]
    supplemental_unit_sha256s: tuple[str, ...]
    consumer_units: int
    supplemental_units: int
    total_nodes: int
    selected_names: int
    input_bytes: int
    composite_bytes: int
    evidence_bytes: int
    parent_lookups: int

    @property
    def mathematical_acceptance(self):
        return False


def complete_candidate(candidate_raw, supplement_raw, *, semantic_id, foundation_id,
                       context_root, expected_targets, prepared_bindings,
                       warranted_symbol, limits=B.Limits(), check_budget=None):
    """Return one READY inert batch, supplement first, unchanged consumer last.

    `warranted_symbol` is a stable point lookup in the REAL protected parent.
    No whole-parent enumeration, remote acquisition, native call or file I/O.
    `check_budget` shares the caller's original allowance and may raise; errors
    propagate. Counts describe selected bytes/nodes/names, not measured CPU or
    unique traversal work: original validation and composite validation repeat
    bounded parsing/scanning. READY is never mathematical acceptance.
    """
    need(type(limits) is B.Limits and callable(warranted_symbol) and
         (check_budget is None or callable(check_budget)), "COMPLETION_CONFIGURATION")

    def check():
        if check_budget is not None:
            check_budget()

    check()
    need(type(candidate_raw) is bytes and type(supplement_raw) is bytes and
         0 < len(candidate_raw) and 0 < len(supplement_raw) and
         len(candidate_raw)+len(supplement_raw) <= limits.max_bundle_bytes,
         "COMPLETION_COMBINED_INPUT_BYTES")
    looked_up = {}

    def lookup(name):
        check()
        key = E.name_key(name)
        if key not in looked_up:
            need(len(looked_up) < 2*limits.max_bindings, "COMPLETION_LOOKUP_BOUND")
            value = warranted_symbol(name)
            need(value is None or type(value) is str, "COMPLETION_LOOKUP_TYPE")
            looked_up[key] = None if value is None else E._hex(value)
        return looked_up[key]

    original = B.bind_candidate(candidate_raw, semantic_id=semantic_id,
        foundation_id=foundation_id, context_root=context_root,
        expected_targets=expected_targets, prepared_bindings=prepared_bindings,
        warranted_symbol=lookup, limits=limits, check_budget=check)
    need(original.status == "NEEDS_LOCAL_INTERPRETATIONS" and original.missing_names,
         "COMPLETION_NOT_NEEDED")
    missing = set(original.missing_names)
    candidate = B._writer_json(candidate_raw, limits.max_bundle_bytes)
    supplement = B._writer_json(supplement_raw, limits.max_bundle_bytes)
    need(type(supplement) is dict and set(supplement) == {
        "schema", "assurance", "profile_id", "context_id", "basis_id", "targets",
        "boundary_imports", "units", "stats"}, "COMPLETION_SUPPLEMENT_FIELDS")
    need(supplement["schema"] == SUPPLEMENT_SCHEMA and
         supplement["assurance"] == B.ASSURANCE and
         supplement["profile_id"] == semantic_id and supplement["basis_id"] == foundation_id and
         supplement["context_id"] == context_root, "COMPLETION_PORTABLE_LABEL_BINDING")
    targets = E._array(supplement["targets"], maximum=limits.max_targets)
    target_keys = tuple(E.name_key(name) for name in targets)
    need(len(target_keys) == len(set(target_keys)) and set(target_keys) == missing,
         "COMPLETION_EXACT_MISSING_TARGETS")
    supplementary = E._array(supplement["units"], maximum=limits.max_units)
    consumer = candidate["units"]  # The original binder validated this exact raw input.
    need(supplementary and len(supplementary)+len(consumer) <= limits.max_units,
         "COMPLETION_COMBINED_UNIT_BOUND")
    boundary = E._array(supplement["boundary_imports"], maximum=limits.max_bindings)
    need(len(boundary)+len(candidate["boundary_imports"])+
         len(candidate["unresolved_imports"]) <= limits.max_bindings,
         "COMPLETION_COMBINED_BOUNDARY_BOUND")
    stats = supplement["stats"]
    need(type(stats) is dict and set(stats) == {"source_records_enumerated", "selected_units",
        "dependency_edges", "scan_nodes", "unit_json_bytes", "boundary_imports", "lookup_count"},
        "COMPLETION_SUPPLEMENT_STATISTICS_FIELDS")
    for value in stats.values():
        E._uint(value)
    need(stats["selected_units"] == len(supplementary) and
         stats["boundary_imports"] == len(boundary) and stats["lookup_count"] <= 65536,
         "COMPLETION_SUPPLEMENT_STATISTICS_CENSUS")

    # Preserve every original claimed ID; new boundary labels come only from K.
    claims = {E.name_key(name): (name, identity) for name, identity in candidate["boundary_imports"]}
    supplemental_boundary = set()
    for row in boundary:
        check()
        name, identity = E._array(row, 2)
        key = E.name_key(name)
        E._hex(identity)
        need(key not in supplemental_boundary and lookup(name) == identity,
             "COMPLETION_SUPPLEMENT_PARENT_IDENTITY")
        supplemental_boundary.add(key)
        need(key not in claims or claims[key][1] == identity, "COMPLETION_CLAIM_CONFLICT")
        if key not in claims:
            claims[key] = (name, identity)

    consumer_outputs = {E.name_key(row[0]) for unit in consumer for row in unit[2]}
    supplemental_outputs, supplemental_hashes = set(), []
    supplemental_available = set(supplemental_boundary)
    nodes, supplemental_bytes = original.total_nodes, 0
    for unit in supplementary:
        check()
        census = E.inspect_unit(unit)
        need(set(census.external_names) <= supplemental_available,
             "COMPLETION_UNBOUND_OR_FORWARD_SUPPLEMENT_REFERENCE")
        nodes += census.total_nodes
        raw = E.canonical_json(unit)
        supplemental_bytes += len(raw)
        need(nodes <= limits.max_total_nodes and supplemental_bytes <= limits.max_bundle_bytes,
             "COMPLETION_COMBINED_CONTENT_BOUND")
        supplemental_hashes.append(_sha(raw))
        for row in unit[2]:
            key = E.name_key(row[0])
            need(key not in supplemental_outputs and key not in consumer_outputs and
                 lookup(row[0]) is None, "COMPLETION_EXISTING_OR_DUPLICATE_OUTPUT")
            supplemental_outputs.add(key)
            supplemental_available.add(key)
            need(len(supplemental_outputs)+len(consumer_outputs) <= limits.max_bindings,
                 "COMPLETION_COMBINED_OUTPUT_BOUND")
    need(missing <= supplemental_outputs, "COMPLETION_MISSING_TARGET_NOT_PRODUCED")
    need(supplemental_bytes == stats["unit_json_bytes"], "COMPLETION_SUPPLEMENT_UNIT_BYTES")

    # Only the internal composite wrapper changes. Original raw units and claims
    # are retained. Missing names now designate earlier NEW units, not K entries.
    unresolved = [name for name in candidate["unresolved_imports"]
                  if E.name_key(name) not in missing and E.name_key(name) not in claims]
    selected_names = (consumer_outputs | supplemental_outputs | set(claims) |
                      {E.name_key(name) for name in unresolved})
    need(len(selected_names) <= limits.max_bindings, "COMPLETION_COMBINED_NAME_BOUND")
    combined_units = [*supplementary, *consumer]
    combined_claims = [[name, identity] for name, identity in claims.values()]
    composite = {"schema": B.SCHEMA, "assurance": B.ASSURANCE,
        "semantic_id": semantic_id, "foundation_id": foundation_id,
        "context_root": context_root, "targets": candidate["targets"],
        "boundary_imports": combined_claims, "unresolved_imports": unresolved,
        "units": combined_units,
        # This synthetic wrapper performs no source-environment enumeration or
        # exporter work. Only structural counters below assert exact quantities.
        "stats": {"source_records_enumerated": 0, "dependency_edges": 0, "scan_nodes": 0,
            "selected_units": len(combined_units), "boundary_imports": len(combined_claims),
            "unresolved_imports": len(unresolved),
            "unit_json_bytes": supplemental_bytes+candidate["stats"]["unit_json_bytes"]}}
    check()
    composite_raw = E.canonical_json(composite)
    need(len(composite_raw) <= limits.max_bundle_bytes, "COMPLETION_COMPOSITE_BYTES")
    # This controller-derived preparation map consists only of original claims
    # checked against original P/K, plus supplemental claims independently read
    # from K. It contains NO supplemental outputs or fabricated acceptance.
    combined_prepared = {key: identity for key, (_, identity) in claims.items()}
    combined = B.bind_candidate(composite_raw, semantic_id=semantic_id,
        foundation_id=foundation_id, context_root=context_root,
        expected_targets=expected_targets, prepared_bindings=combined_prepared,
        warranted_symbol=lookup, limits=limits, check_budget=check)
    need(combined.status == "READY" and combined.total_nodes == nodes and
         len(combined.raw_units) == len(combined_units), "COMPLETION_COMPOSITE_NOT_READY")
    consumer_hashes = tuple(_sha(E.canonical_json(unit)) for unit in consumer)
    check()
    plan = CompletionPlan("READY", semantic_id, foundation_id, context_root,
        combined.raw_units, combined.targets, tuple(sorted(target_keys)),
        _sha(candidate_raw), _sha(supplement_raw), _sha(composite_raw),
        consumer_hashes, tuple(supplemental_hashes), len(consumer), len(supplementary),
        nodes, len(selected_names), len(candidate_raw)+len(supplement_raw), len(composite_raw),
        sum(map(len, combined.raw_units)), len(looked_up))
    check()
    return plan
