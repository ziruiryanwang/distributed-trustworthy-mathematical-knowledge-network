"""Bounded semantic authoring context from one actual live import session.

Returned packets and demands are untrusted data, never admission or handles.
This module does not launch Lean, dial a peer or fetch theorem proof ancestry.
"""
from copy import deepcopy
import hashlib

from modules import codec as C
from modules.model import Address
from modules.source_rows import SourceRows
from .imports import ImportSession

SCHEMA = "DMKN_UNTRUSTED_AUTHORING_CONTEXT_V1"
DEFAULT_LIMITS = dict(groups=256, declarations=4096, expression_visits=500000,
                      data_bytes=16*1024**2, demands=256)


def selection(session):
    C.require(type(session) is ImportSession, "AUTHORING_EXACT_SESSION")
    items = session.selected_data()
    public = [{"module": item["module"], "summary": item["summary"],
               "journal_sha256": hashlib.sha256(item["journal"]).hexdigest(),
               "receipt_sha256": hashlib.sha256(item["receipt"]).hexdigest(),
               "openings": item["openings"], "bodies": item["bodies"]} for item in items]
    return items, C.hash_value("authoring-session-selection", public)


def require_live_selection(session, binding):
    C.digest_string(binding)
    unused, actual = selection(session)
    C.require(actual == binding, "AUTHORING_SELECTION_CHANGED")


def _records(row):
    tag, value = next(iter(row.items()))
    return ([d for field in ("types", "ctors", "recs") for d in value[field]]
            if tag == "inductive" else [value])


def _foundation(raw, pin, session):
    C.require(type(raw) is bytes and 0 < len(raw) <= DEFAULT_LIMITS["data_bytes"], "AUTHORING_FOUNDATION_BYTES")
    C.digest_string(pin)
    C.require(hashlib.sha256(raw).hexdigest() == pin, "AUTHORING_FOUNDATION_PIN")
    rows = C.parse_json(raw)
    C.require(C.canonical(rows) == raw, "AUTHORING_FOUNDATION_CANONICAL")
    # The current adopted relation uses this exact foundation identity scheme.
    C.require(C.hash_value("owner-workload-foundation-candidate", rows) == session._verifier._foundation,
              "AUTHORING_ADOPTED_FOUNDATION")
    reader = SourceRows(rows, [], [])
    names = [reader.name(d["name"]) for row in reader.declarations for d in _records(row)]
    decoder = SourceRows(rows, names, [])
    env = decoder.module(session._verifier._foundation, session._verifier._policy)
    values = []
    for group in env.spec["groups"]:
        for d in group["declarations"]:
            if d["kind"] not in ("definition", "theorem", "opaque"): continue
            key = (env.local_proofs[Address.of(env.module, d["name"])] if d["kind"] == "theorem"
                   else d["value_hash"])
            values.append({"name": d["name"], "expression": C.parse_json(env.bodies[d["universes"], key])})
    bodies = [{"universes": arity, "digest": digest, "expression": C.parse_json(body)}
              for (arity, digest), body in sorted(env.bodies.items())]
    return {"groups": env.spec["groups"], "bodies": bodies, "values": values, "names": names}, decoder.work


def prepare_context(session, foundation_bytes, foundation_sha256, *, limits=None):
    """Return complete context or typed missing-data demands; no automatic I/O.

    Include every opened group in this bounded session because the frozen
    make_request also includes them. Do not claim a smaller frontend context
    silently prunes parent receipts/openings from the later child request.
    """
    caps = dict(DEFAULT_LIMITS if limits is None else limits)
    C.fields(caps, set(DEFAULT_LIMITS))
    for key, maximum in DEFAULT_LIMITS.items():
        C.require(0 < C.uint(caps[key], maximum), "AUTHORING_CONTEXT_LIMIT:"+key)
    C.require(type(foundation_bytes) is bytes and len(foundation_bytes) <= caps["data_bytes"],
              "AUTHORING_FOUNDATION_INPUT_LIMIT")
    items, binding = selection(session)
    foundation, work = _foundation(foundation_bytes, foundation_sha256, session)
    C.require(work <= caps["expression_visits"], "AUTHORING_FOUNDATION_WORK")
    foundation_names = {C.name_key(name) for name in foundation["names"]}
    groups, addresses, bodies, modules = {}, {}, {}, set()
    demands = {}
    stored_bytes = len(foundation_bytes)
    declaration_count = 0
    for item in items:
        owner = item["module"]; modules.add(owner)
        C.require(item["openings"], "AUTHORING_EMPTY_SELECTED_MODULE")
        for opening in item["openings"]:
            group = C.verify_group_opening(owner, opening)
            key = owner, opening["index"]
            C.require(key not in groups, "AUTHORING_DUPLICATE_GROUP")
            addition = len(C.canonical(opening))
            C.require(len(groups)+1 <= caps["groups"]
                      and declaration_count+len(group["declarations"]) <= caps["declarations"]
                      and stored_bytes+addition <= caps["data_bytes"], "AUTHORING_CONTEXT_CENSUS")
            groups[key] = deepcopy(group)
            stored_bytes += addition
            for d in group["declarations"]:
                address = owner, C.name_key(d["name"])
                C.require(address not in addresses, "AUTHORING_DUPLICATE_DECLARATION")
                addresses[address] = key
                declaration_count += 1
        for body in item["bodies"]:
            key = owner, body["universes"], body["digest"]
            C.require(C.body_id(body["expression"], body["universes"]) == body["digest"], "AUTHORING_BODY_BINDING")
            C.require(key not in bodies, "AUTHORING_DUPLICATE_BODY")
            addition = len(C.canonical(body))
            C.require(stored_bytes+addition <= caps["data_bytes"], "AUTHORING_CONTEXT_CENSUS")
            bodies[key] = deepcopy(body["expression"])
            stored_bytes += addition
    C.require(len(groups) <= caps["groups"] and declaration_count <= caps["declarations"]
              and stored_bytes <= caps["data_bytes"], "AUTHORING_CONTEXT_CENSUS")
    edges = {key: set() for key in groups}
    selected_bodies = {key: {} for key in groups}

    def demand(value):
        key = C.canonical(value)
        C.require(key in demands or len(demands) < caps["demands"], "AUTHORING_DEMAND_LIMIT")
        demands[key] = value

    def reference(key, ref):
        if ref[0] == "foundation":
            C.require(C.name_key(ref[1]) in foundation_names, "AUTHORING_UNKNOWN_FOUNDATION_NAME")
            return
        owner, name = (key[0], ref[1]) if ref[0] == "local" else (ref[1], ref[2])
        address = owner, C.name_key(name)
        if owner not in modules:
            demand({"kind": "NeedVerifiedModule", "module": owner, "name": deepcopy(name)})
        elif address not in addresses:
            demand({"kind": "NeedDeclaration", "module": owner, "name": deepcopy(name)})
        else:
            target = addresses[address]
            C.require(target != key or groups[key]["kind"] == "inductive", "AUTHORING_ORDINARY_SELF_REFERENCE")
            if target != key: edges[key].add(target)

    def expression(key, value):
        nonlocal work
        pending = [value]
        while pending:
            expr = pending.pop(); work += 1
            C.require(work <= caps["expression_visits"], "AUTHORING_EXPRESSION_WORK")
            tag = expr[0]
            if tag in ("const", "proj"): reference(key, expr[1])
            children = {"sort": (), "bvar": (), "const": (), "app": (1, 2),
                        "lam": (2, 3), "forall": (2, 3), "let": (1, 2, 3), "proj": (3,)}[tag]
            pending.extend(expr[i] for i in children)

    for key, group in groups.items():
        for d in group["declarations"]:
            expression(key, d["type"])
            hashes = ([d["value_hash"]] if d["kind"] == "definition" else
                      [rule["value_hash"] for rule in d["meta"]["rules"]] if d["kind"] == "recursor" else [])
            for digest in hashes:
                address = key[0], d["universes"], digest
                if address not in bodies:
                    demand({"kind": "NeedBody", "module": key[0], "name": deepcopy(d["name"]),
                            "universes": d["universes"], "body_hash": digest})
                elif address not in selected_bodies[key]:
                    selected_bodies[key][address] = bodies[address]
                    expression(key, bodies[address])
    report = {"groups": len(groups), "declarations": declaration_count,
              "counted_expression_visits": work, "selected_input_bytes": stored_bytes,
              "all_session_openings_included": True, "theorem_ancestor_proof_bytes": 0,
              "fixed_foundation_proof_bodies_included": True,
              "expression_counter_is_not_total_cpu_work": True,
              "whole_operation_supervision_required": True}
    if demands:
        require_live_selection(session, binding)
        return {"status": "NEED_AUTHORING_CONTEXT_DATA", "demands": [demands[k] for k in sorted(demands)],
                "selection_binding": binding, "cost": report, "mathematical_acceptance": False}
    remaining, ordered, done = set(groups), [], set()
    while remaining:
        ready = [key for key in sorted(remaining) if edges[key] <= done]
        C.require(ready, "AUTHORING_INTERGROUP_CYCLE")
        for key in ready:
            ordered.append({"owner": key[0], "index": key[1], "group": groups[key],
                "bodies": [{"universes": address[1], "digest": address[2], "expression": body}
                           for address, body in sorted(selected_bodies[key].items())]})
        remaining.difference_update(ready); done.update(ready)
    packet = {"schema": SCHEMA, "foundation": session._verifier._foundation,
              "policy": session._verifier._policy, "foundation_sha256": foundation_sha256,
              "foundation_view": foundation, "imports": ordered,
              "selection_binding": binding, "mathematical_acceptance": False}
    raw = C.canonical(packet)
    C.require(len(raw) <= caps["data_bytes"], "AUTHORING_CONTEXT_OUTPUT_BYTES")
    report["frontend_packet_bytes"] = len(raw)
    require_live_selection(session, binding)
    return {"status": "UNTRUSTED_AUTHORING_CONTEXT_READY", "packet": C.parse_json(raw),
            "selection_binding": binding, "cost": report, "mathematical_acceptance": False}
