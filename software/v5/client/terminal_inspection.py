"""Bounded inspection of actual terminal-route author outputs, not admission.

Exact local interfaces/journals and real exported proof references are compared.
Unused imported groups, old witness rows and theorem proof bytes are NOT fixed.
The independent receiving A/mixed verifier remains the mathematical authority.
"""
from collections import Counter
import hashlib
from pathlib import Path

from aggregate_claims import bindings as B
from authoring.source import EXPORT_SCHEMA, REQUEST_SCHEMA, NATIVE_NAME_LIMITS
from delta_claims.claims import expected_journal
from delta.reprepare import emit_relation_rows
from mixed_claims.packet import parse_packet
from modules import codec as C
from modules.model import Address
from modules.source_rows import decode_source

MIB = 1024**2


def _need(value, reason):
    if not value:
        raise ValueError(reason)


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _read(path, grant, maximum):
    """Only ordinary bounded actual outputs below this same original grant."""
    grant.remaining_seconds()
    path, base = Path(path), Path(grant.directory)
    _need(path.is_absolute() and base.is_absolute() and path.resolve() == path
          and base.resolve() == base and path.is_relative_to(base),
          "TERMINAL_INSPECTION_OUTPUT_SCOPE")
    _need(path.is_file() and all(not p.is_symlink() and not p.is_junction()
                                for p in (path, *path.parents)),
          "TERMINAL_INSPECTION_ORDINARY_FILE")
    size = path.stat().st_size
    _need(0 < size <= maximum, "TERMINAL_INSPECTION_FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    _need(len(raw) == size == path.stat().st_size, "TERMINAL_INSPECTION_FILE_CHANGED")
    grant.remaining_seconds()
    return raw


def _read_pin(row, grant, maximum):
    C.fields(row, {"path", "bytes", "sha256"})
    C.digest_string(row["sha256"])
    _need(type(row["bytes"]) is int and 0 < row["bytes"] <= maximum,
          "TERMINAL_INSPECTION_PIN_SIZE")
    raw = _read(row["path"], grant, maximum)
    _need(len(raw) == row["bytes"] and _sha(raw) == row["sha256"],
          "TERMINAL_INSPECTION_PIN_CHANGED")
    return raw


def inspect_author(prepared, source, roots, grant, *, envelope, aggregate_image,
                   expected_header, expected_target_journal, expected_frontier_journals,
                   required_proof_module, required_proof_name, foundation_bytes):
    """Bind one real source/export/new-delta return; mint no proof or live handle.

    This selected gate has one root, one A claim, two A-member frontiers and one
    newly authored delta. A body reference is an audited syntactic dependency,
    not by itself a theorem of useful growth or an independent validity check.
    """
    grant.remaining_seconds()
    _need(type(source) is str and 0 < len(source.encode("utf-8")) <= 65536
          and type(roots) is list and len(roots) == 1, "TERMINAL_INSPECTION_SOURCE_ROOT")
    C.validate_name(roots[0]); C.validate_name(required_proof_name)
    C.digest_string(required_proof_module)
    _need(type(expected_frontier_journals) in (list, tuple)
          and len(expected_frontier_journals) == 2
          and all(type(j) is bytes for j in expected_frontier_journals)
          and len(set(expected_frontier_journals)) == 2,
          "TERMINAL_INSPECTION_TWO_EXACT_FRONTIERS")
    for exact in (*expected_frontier_journals, expected_target_journal):
        B.member_journal(exact)
    header = B.decode_header(expected_header, adopted_image=aggregate_image)
    _need(header["member_count"] == 2 and header["maximum_member_rank"] == 1
          and header["seal_height"] == 1
          and expected_target_journal not in expected_frontier_journals,
          "TERMINAL_INSPECTION_SELECTED_FRONTIER")
    _need(prepared["status"] == "UNTRUSTED_MIXED_DELTA_PACKET_PREPARED"
          and prepared["mathematical_acceptance"] is False, "TERMINAL_INSPECTION_AUTHOR_STATUS")
    child = prepared["child"]
    source_sha = _sha(source.encode("utf-8"))
    _need(child["status"] == "UNTRUSTED_MIXED_DELTA_PACKET"
          and child["mathematical_acceptance"] is False and child["roots"] == roots
          and child["source_sha256"] == source_sha, "TERMINAL_INSPECTION_SOURCE_BINDING")
    request_raw = _read(Path(prepared["evidence"])/"source-request.json", grant, 16*MIB)
    export_raw = _read_pin(prepared["export"], grant, 16*MIB)
    raw = _read_pin(prepared["packet"], grant, envelope.packet_bytes)
    request, exported = C.parse_json(request_raw), C.parse_json(export_raw)
    _need(request["schema"] == REQUEST_SCHEMA and exported["schema"] == EXPORT_SCHEMA
          and request["source"] == source and request["roots"] == exported["roots"] == roots
          and request["source_sha256"] == exported["source_sha256"] == source_sha
          and request["mathematical_acceptance"] is False
          and exported["mathematical_acceptance"] is False
          and exported["status"] == "OWNER_FRONTEND_EXPORT_REQUIRES_INDEPENDENT_RELATION"
          and exported["selection_binding"] == child["parent_selection_binding"],
          "TERMINAL_INSPECTION_EXPORT_BINDING")
    _need(raw == child["packet"] and _sha(raw) == child["packet_sha256"],
          "TERMINAL_INSPECTION_PACKET_OUTPUT")
    claims, frontiers, witnesses, census = parse_packet(raw, envelope, aggregate_image=aggregate_image)
    _need(len(claims) == 1 and claims[0][0] == 1 and claims[0][1] == expected_header
          and len(frontiers) == 2 and len(witnesses) == 1
          and {row[1] for row in frontiers} == set(expected_frontier_journals),
          "TERMINAL_INSPECTION_ONE_NEW_DELTA_SHAPE")
    witness_raw, parents, summary, rank = witnesses[0]
    _need(set(parents) == set(expected_frontier_journals) and rank == 2
          and expected_journal(summary, rank, B.RELATION_IMAGE) == expected_target_journal,
          "TERMINAL_INSPECTION_EXACT_TARGET_JOURNAL")
    witness = C.parse_json(witness_raw)
    context = request["context"]
    _need(context["foundation"] == B.FOUNDATION and context["policy"] == B.POLICY
          and context["selection_binding"] == exported["selection_binding"],
          "TERMINAL_INSPECTION_CONTEXT_PROFILE")
    _need(type(foundation_bytes) is bytes and 0 < len(foundation_bytes) <= 16*MIB
          and _sha(foundation_bytes) == context["foundation_sha256"]
          and C.hash_value("owner-workload-foundation-candidate", C.parse_json(foundation_bytes)) == B.FOUNDATION,
          "TERMINAL_INSPECTION_FOUNDATION_BINDING")
    external = [{"source_name": C.relocated_name(item["owner"], declaration["name"]),
                 "module": item["owner"], "relative_name": declaration["name"]}
                for item in context["imports"] for declaration in item["group"]["declarations"]]
    env = decode_source(exported["rows"], exported["local_names"], context["foundation_view"]["names"],
                        B.FOUNDATION, B.POLICY, external, NATIVE_NAME_LIMITS)
    _need(env.module == child["local_module"] == C.summary_id(summary)
          and env.spec == witness["local_spec"] and C.summarize(env.spec) == summary,
          "TERMINAL_INSPECTION_LOCAL_INTERFACE")
    # Tie the inspected exported proof to the actual witness consumed by C.
    # A matching interface/J alone deliberately says nothing about proof bytes.
    # Re-emit only this new proof and its demanded semantics, not parent proofs.
    actual_groups = {(item["owner"], item["index"]): item["group"] for item in context["imports"]}
    expected_groups = {}
    for parent in witness["parents"]:
        owner = B.member_journal(bytes(parent["journal"]))["module"]
        for opening in parent["openings"]:
            key = owner, opening["index"]
            _need(key not in expected_groups, "TERMINAL_INSPECTION_DUPLICATE_PARENT_GROUP")
            expected_groups[key] = C.verify_group_opening(owner, opening)
    _need(actual_groups == expected_groups and len(actual_groups) == len(context["imports"]),
          "TERMINAL_INSPECTION_EXACT_IMPORT_GROUPS")
    for body in witness["bodies"]:
        _need(env.supply_body(body["expression"], body["universes"]) == body["digest"],
              "TERMINAL_INSPECTION_SEMANTIC_BODY")
    _need(emit_relation_rows(foundation_bytes, env, context["imports"]) == witness["rows"],
          "TERMINAL_INSPECTION_EXPORT_TO_WITNESS_ROWS")
    declarations = {C.name_key(d["name"]): d for group in env.spec["groups"] for d in group["declarations"]}
    root_key = C.name_key(roots[0])
    _need(root_key in declarations and declarations[root_key]["kind"] == "theorem",
          "TERMINAL_INSPECTION_EXPORTED_THEOREM")
    required = ("external", required_proof_module, C.name_key(required_proof_name))
    visits = 0

    def references(expression):
        nonlocal visits
        stack, found = [expression], Counter()
        children = {"sort": (), "bvar": (), "const": (), "app": (1, 2),
                    "lam": (2, 3), "forall": (2, 3), "let": (1, 2, 3), "proj": (3,)}
        while stack:
            node = stack.pop(); visits += 1
            _need(visits <= 500000, "TERMINAL_INSPECTION_NODE_BOUND")
            if visits % 1024 == 0:
                grant.remaining_seconds()
            if node[0] in ("const", "proj"):
                ref = node[1]
                key = ((ref[0], ref[1], C.name_key(ref[2])) if ref[0] == "external"
                       else (ref[0], "", C.name_key(ref[1])))
                found[key] += 1
            stack.extend(node[index] for index in children[node[0]])
        return found

    pending, seen, proof_references = [root_key], set(), Counter()
    while pending:
        key = pending.pop()
        if key in seen:
            continue
        _need(key in declarations and len(seen) < 4096, "TERMINAL_INSPECTION_LOCAL_CLOSURE")
        seen.add(key); declaration = declarations[key]
        if declaration["kind"] not in ("theorem", "definition", "opaque"):
            continue
        digest = (env.local_proofs[Address.of(env.module, declaration["name"])]
                  if declaration["kind"] == "theorem" else declaration["value_hash"])
        refs = references(C.parse_json(env.bodies[declaration["universes"], digest]))
        proof_references.update(refs)
        pending.extend(ref[2] for ref in refs if ref[0] == "local")
    _need(proof_references[required] > 0, "TERMINAL_INSPECTION_REQUIRED_PROOF_EDGE")
    grant.remaining_seconds()
    return {"module": env.module, "roots": roots, "target_journal_sha256": _sha(expected_target_journal),
        "local_spec_sha256": _sha(C.canonical(env.spec)), "local_groups": len(env.spec["groups"]),
        "root_universes": declarations[root_key]["universes"],
        "source_sha256": source_sha, "request_sha256": _sha(request_raw), "export_sha256": _sha(export_raw),
        "packet_sha256": _sha(raw), "packet_bytes": len(raw), "export_rows": len(exported["rows"]),
        "native_witness_rows": len(witness["rows"]), "packet_census": census,
        "required_proof_edge": {"module": required_proof_module, "name": required_proof_name},
        "required_reference_occurrences": proof_references[required],
        "proof_closure_declarations": len(seen), "inspected_nodes": visits,
        "exported_proof_reemission_matches_witness": True,
        "historical_witness_equality_required": False, "mathematical_acceptance": False,
        "authority": "ACTUAL_EXPORT_DEPENDENCY_INSPECTION_NOT_MATHEMATICAL_ADMISSION"}
