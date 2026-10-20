"""Bounded data-only preview before expensive mathematical admission.

Staged records are descriptions, not evidence that receipts were verified.
The ordinary client must bind them to its actual same-client staged tokens.
This helper never creates an owner, import session, author context or warrant.
The unchanged live import must recheck everything after genuine admission.
"""
import json

from aggregate_claims import bindings as B
from mixed_claims.imports_atomic import (
    RelationBasis, _build_context, _context_limits, _decode_context_foundation)
from modules import codec as C

MAX_STAGED, MAX_BODIES = 128, 8192
MAX_PACKET_BYTES = 32*1024**2  # Same current public packet-custody ceiling.
MAX_INPUT_VALUES, MAX_INPUT_DEPTH = 2000000, C.DEFAULT_LIMITS.max_depth+32
NEED, READY = "NEED_STRUCTURAL_CONTEXT_DATA", "STRUCTURAL_CLOSURE_STAGED"


def _bounded_json(value, maximum):
    """Bound serialized work before whole-input encoding or semantic walking.

    Count exact canonical JSON bytes without constructing the complete output.
    Integers, strings, depth, pending work and visited values have finite caps.
    Repeated references count repeatedly, as their JSON representation does;
    cycles refuse at the depth/work cap. No arbitrary object hooks are called.
    """
    C.require(type(maximum) is int and maximum > 0, "STAGING_INPUT_BYTE_LIMIT")
    stack, count, size = [(value, 0)], 0, 0
    while stack:
        item, depth = stack.pop(); count += 1
        C.require(count <= MAX_INPUT_VALUES and depth <= MAX_INPUT_DEPTH,
                  "STAGING_INPUT_WORK_LIMIT")
        kind = type(item)
        if kind is dict:
            children = 2*len(item)
            size += 2+max(0, len(item)-1)+len(item)
            C.require(count+len(stack)+children <= MAX_INPUT_VALUES
                      and size+children <= maximum, "STAGING_INPUT_WORK_OR_BYTES")
            C.require(all(type(key) is str for key in item), "STAGING_INPUT_KEY")
            for key, part in item.items():
                stack.append((part, depth+1)); stack.append((key, depth+1))
        elif kind is list:
            size += 2+max(0, len(item)-1)
            C.require(count+len(stack)+len(item) <= MAX_INPUT_VALUES
                      and size+len(item) <= maximum, "STAGING_INPUT_WORK_OR_BYTES")
            stack.extend((part, depth+1) for part in item)
        elif kind is str:
            C.require(len(item) <= C.DEFAULT_LIMITS.max_string_bytes,
                      "STAGING_INPUT_STRING_LIMIT")
            try:
                encoded = json.dumps(item, ensure_ascii=False, allow_nan=False).encode("utf-8")
            except (ValueError, UnicodeError) as error:
                raise C.StructureError("STAGING_INPUT_STRING_ENCODING") from error
            size += len(encoded)
        elif kind is int:
            C.uint(item, 2**64-1); size += len(str(item))
        elif item is None:
            size += 4
        elif kind is bool:
            size += 4 if item else 5
        else:
            raise C.StructureError("STAGING_INPUT_JSON_TYPE")
        C.require(size <= maximum, "STAGING_INPUT_BYTE_LIMIT")
    return size, count


def preview(staged, openings, bodies, foundation_bytes, foundation_sha256, *, limits=None,
            definition_mode="eager"):
    """Return structural missing-data demands, never a usable author context.

    Exactly one chosen whole-J record per module is required. All module items
    come from that explicit staged-evidence set, including members whose needed
    declarations have not yet been fetched. Group presence cannot invent it.
    Per-call bounds do not replace the caller's cumulative controller budget.
    """
    C.require(limits is None or type(limits) is dict and len(limits) == 5,
              "STAGING_LIMIT_FIELDS")
    C.require(type(definition_mode) is str and definition_mode in ("eager", "interface-only"),
              "STAGING_DEFINITION_MODE")
    if limits is not None: _bounded_json(limits, 2048)
    caps = _context_limits(limits)
    C.require(type(staged) is list and 0 < len(staged) <= MAX_STAGED,
              "STAGING_EVIDENCE_LIST")
    C.require(type(openings) is list and 0 < len(openings) <= caps["groups"],
              "STAGING_OPENING_LIST")
    C.require(type(bodies) is list and len(bodies) <= MAX_BODIES, "STAGING_BODY_LIST")
    C.require(type(foundation_bytes) is bytes and 0 < len(foundation_bytes) < caps["data_bytes"],
              "STAGING_FOUNDATION_BOUND")
    C.digest_string(foundation_sha256)
    payload = {"staged": staged, "openings": openings, "bodies": bodies}
    if definition_mode != "eager": payload["definition_mode"] = definition_mode
    measured, values = _bounded_json(payload, caps["data_bytes"]-len(foundation_bytes))
    codec_limits = C.Limits(max_bytes=caps["data_bytes"],
                            max_nodes=min(C.DEFAULT_LIMITS.max_nodes, caps["expression_visits"]))
    raw = C.canonical(payload, codec_limits)
    C.require(len(raw) == measured, "STAGING_INPUT_CENSUS_BINDING")
    # Snapshot bounded ordinary data before any repeated semantic scans.
    data = C.parse_json(raw, codec_limits)
    basis, members, items = RelationBasis(), {}, {}
    for row in data["staged"]:
        C.fields(row, {"module", "journal", "summary", "packet_sha256", "packet_bytes"})
        module = C.digest_string(row["module"])
        C.require(module not in members, "STAGING_DUPLICATE_MODULE_VARIANT")
        C.require(type(row["journal"]) is list and len(row["journal"]) == 184,
                  "STAGING_EXACT_JOURNAL")
        exact = bytes(C.uint(part, 255) for part in row["journal"])
        parsed = B.member_journal(exact)
        C.validate_summary(row["summary"])
        C.require(parsed["module"] == module and parsed["summary"] == row["summary"]
                  and parsed["foundation"] == basis.foundation and parsed["policy"] == basis.policy,
                  "STAGING_JOURNAL_SUMMARY_BASIS")
        C.digest_string(row["packet_sha256"])
        C.require(0 < C.uint(row["packet_bytes"], MAX_PACKET_BYTES), "STAGING_PACKET_BYTES")
        members[module] = row
        items[module] = {"module": module, "openings": [], "bodies": []}

    seen_groups, addresses, allowed, declaration_count = set(), set(), set(), 0
    for row in data["openings"]:
        C.fields(row, {"module", "opening"}); module = C.digest_string(row["module"])
        C.require(module in members, "STAGING_OPENING_WITHOUT_EVIDENCE")
        opening = row["opening"]
        C.fields(opening, {"schema", "summary", "index", "group", "siblings"})
        C.fields(opening["group"], {"kind", "declarations"})
        declarations = opening["group"]["declarations"]
        C.require(type(declarations) is list and 0 < len(declarations)
                  and declaration_count+len(declarations) <= caps["declarations"],
                  "STAGING_DECLARATION_LIMIT")
        declaration_count += len(declarations)
        group = C.verify_group_opening(module, opening, codec_limits)
        C.require(opening["summary"] == members[module]["summary"], "STAGING_GROUP_SUMMARY")
        key = module, opening["index"]
        C.require(key not in seen_groups, "STAGING_DUPLICATE_GROUP"); seen_groups.add(key)
        for declaration in group["declarations"]:
            address = module, C.name_key(declaration["name"])
            C.require(address not in addresses, "STAGING_DUPLICATE_DECLARATION"); addresses.add(address)
            kind, arity = declaration["kind"], declaration["universes"]
            # Match the actual live materializer's permissible commitments.
            # The walker only demands definition/recursor computation bodies.
            if kind in ("definition", "opaque"):
                allowed.add((module, arity, declaration["value_hash"]))
            elif kind == "recursor":
                allowed.update((module, arity, rule["value_hash"]) for rule in declaration["meta"]["rules"])
        items[module]["openings"].append(opening)

    seen_bodies = set()
    for row in data["bodies"]:
        C.fields(row, {"module", "universes", "expression"}); module = C.digest_string(row["module"])
        C.require(module in members, "STAGING_BODY_WITHOUT_EVIDENCE")
        arity = C.uint(row["universes"], C.DEFAULT_LIMITS.max_universes)
        digest = C.body_id(row["expression"], arity, codec_limits)
        key = module, arity, digest
        C.require(key in allowed, "STAGING_BODY_NOT_COMMITTED")
        C.require(key not in seen_bodies, "STAGING_DUPLICATE_BODY"); seen_bodies.add(key)
        items[module]["bodies"].append({"universes": arity, "digest": digest, "expression": row["expression"]})

    foundation, work = _decode_context_foundation(foundation_bytes, foundation_sha256, basis)
    binding = C.hash_value("structural-semantic-staging-v1", data, codec_limits)
    result = _build_context([items[module] for module in sorted(items)], binding,
        foundation_bytes, foundation_sha256, foundation, work, basis, {}, caps,
        definition_mode=definition_mode)
    C.require(result["status"] in ("NEED_AUTHORING_CONTEXT_DATA", "UNTRUSTED_AUTHORING_CONTEXT_READY"),
              "STAGING_WALKER_STATUS")
    demands = []
    for demand in result.get("demands", []):
        kind = demand["kind"]
        C.require(kind in ("NeedVerifiedMixedMember", "NeedDeclaration", "NeedBody"),
                  "STAGING_WALKER_DEMAND")
        fields = {"kind", "module", "name"}
        if kind == "NeedBody": fields |= {"universes", "body_hash"}
        C.fields(demand, fields)
        demands.append({**demand, "kind": "NeedModuleEvidence" if kind == "NeedVerifiedMixedMember" else kind})
    ready = result["status"] == "UNTRUSTED_AUTHORING_CONTEXT_READY"
    C.require((ready and not demands) or (not ready and 0 < len(demands) <= caps["demands"]),
              "STAGING_WALKER_READINESS")
    cost = result["cost"]
    # Explicit whitelist: no packet, live selection binding or warrant census.
    result = {"status": READY if ready else NEED, "demands": demands,
        "cost": {"preview_calls": 1, "staged_modules": len(members),
            "supplied_groups": len(seen_groups), "supplied_bodies": len(seen_bodies),
            "input_json_values": values, "serialized_input_bytes": len(raw)+len(foundation_bytes),
            "groups": cost["groups"], "declarations": cost["declarations"],
            "counted_expression_visits": cost["counted_expression_visits"],
            "context_selected_input_bytes": cost["selected_input_bytes"],
            "projected_frontend_packet_bytes": cost.get("frontend_packet_bytes", 0),
            "frontend_theorem_ancestor_proof_bytes": 0,
            "fixed_foundation_proof_bodies_included": True,
            "expression_counter_is_not_total_cpu_work": True,
            "cumulative_operation_budget_required": True},
        "mathematical_acceptance": False}
    if definition_mode != "eager": result["definition_mode"] = definition_mode
    return result
