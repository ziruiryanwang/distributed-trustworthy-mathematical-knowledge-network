"""Pure bounded packet parsing and graph checks. These grant NO authority."""
from __future__ import annotations

from dataclasses import dataclass, fields as dataclass_fields, replace
import hashlib

from admission.bindings import journal
from modules import codec as C

SCHEMA = "DMKN_NATIVE_DELTA_PACKET_V1"
MIB = 1024**2


class DeltaError(ValueError):
    """A refusal/incompletion, never a theorem-false assertion."""
    def __init__(self, status, reason):
        super().__init__(reason)
        self.status = status


def need(ok, reason, status="INVALID_OR_UNBOUND"):
    if not ok:
        raise DeltaError(status, reason)


@dataclass(frozen=True)
class Envelope:
    packet_bytes: int = 16*MIB
    receipt_bytes: int = 8*MIB
    witness_bytes: int = 16*MIB
    frontiers: int = 8
    deltas: int = 16
    edges: int = 128
    openings: int = 4096
    bodies: int = 8192
    rows: int = 250000
    nodes: int = 500000
    depth: int = 128
    rank: int = 2**64-1

    def validate(self):
        ceilings = Envelope(32*MIB, 16*MIB, 32*MIB, 32, 128, 4096, 16384,
                             32768, 1000000, 2000000, 192, 2**64-1)
        for field in dataclass_fields(self):
            value = getattr(self, field.name)
            need(type(value) is int and 0 < value <= getattr(ceilings, field.name),
                 "OWNER_ENVELOPE:"+field.name)


def _census(value, limits):
    # Iterative after the byte-bounded JSON parse. Counts all submitted values,
    # including data later refused as duplicate, disconnected or inapplicable.
    stack, seen = [(value, 0)], 0
    while stack:
        item, depth = stack.pop(); seen += 1
        need(seen <= limits.nodes and depth <= limits.depth,
             "PACKET_STRUCTURE_ENVELOPE", "NEEDS_SEAL")
        if type(item) is dict:
            stack.extend((v, depth+1) for v in item.values())
        elif type(item) is list:
            stack.extend((v, depth+1) for v in item)
        else:
            need(item is None or type(item) in (str, bool, int), "JSON_VALUE_TYPE")
            if type(item) is int: need(0 <= item <= 2**64-1, "JSON_INTEGER")
    return seen


def journal_bytes(value):
    need(type(value) is list and len(value) == 184, "JOURNAL_BYTES")
    need(all(type(x) is int and 0 <= x <= 255 for x in value), "JOURNAL_BYTE")
    raw = bytes(value); journal(raw)
    return raw


def parse_packet(raw, limits):
    """Returns bounded inert data; no flags or claimed receipt successes exist."""
    limits.validate()
    need(type(raw) is bytes and 0 < len(raw) <= limits.packet_bytes,
         "PACKET_BYTE_ENVELOPE", "NEEDS_SEAL")
    value = C.parse_json(raw, replace(C.DEFAULT_LIMITS, max_bytes=limits.packet_bytes))
    nodes = _census(value, limits)
    C.fields(value, {"schema", "frontiers", "deltas"})
    need(value["schema"] == SCHEMA, "PACKET_SCHEMA")
    frontiers, deltas = value["frontiers"], value["deltas"]
    need(type(frontiers) is list and len(frontiers) <= limits.frontiers
         and type(deltas) is list and 0 < len(deltas) <= limits.deltas,
         "PACKET_NODE_ENVELOPE", "NEEDS_SEAL")
    received, witnesses = [], []
    receipt_bytes = witness_bytes = edges = openings = bodies = rows = 0
    for item in frontiers:
        C.fields(item, {"receipt_hex", "summary"})
        encoded = item["receipt_hex"]
        need(type(encoded) is str and 0 < len(encoded) <= 2*limits.receipt_bytes
             and len(encoded) % 2 == 0
             and all(c in "0123456789abcdef" for c in encoded), "RECEIPT_HEX")
        receipt_bytes += len(encoded)//2
        need(receipt_bytes <= limits.receipt_bytes, "RECEIPT_ENVELOPE", "NEEDS_SEAL")
        C.validate_summary(item["summary"])
        received.append((bytes.fromhex(encoded), C.canonical(item["summary"])))
    for item in deltas:
        # This transport uses the named record form. Native relation semantics
        # remain unchanged; its alternate positional encoding is not required.
        C.fields(item, {"schema", "image", "rank", "local_spec", "rows", "parents", "bodies"})
        need(item["schema"] == "DMKN_CERTIFIED_MODULES_V2", "RELATION_SCHEMA")
        C.uint(item["rank"], limits.rank)
        need(all(type(item[k]) is list for k in ("image", "rows", "parents", "bodies")),
             "RELATION_ARRAYS")
        edges += len(item["parents"]); bodies += len(item["bodies"]); rows += len(item["rows"])
        parents = []
        for parent in item["parents"]:
            C.fields(parent, {"journal", "openings"})
            need(type(parent["openings"]) is list, "PARENT_OPENINGS")
            openings += len(parent["openings"])
            parents.append(journal_bytes(parent["journal"]))
        need(edges <= limits.edges and openings <= limits.openings
             and bodies <= limits.bodies and rows <= limits.rows,
             "COMPLETE_UNCERTIFIED_CLOSURE_ENVELOPE", "NEEDS_SEAL")
        encoded = C.canonical(item)
        witness_bytes += len(encoded)
        need(witness_bytes <= limits.witness_bytes, "WITNESS_ENVELOPE", "NEEDS_SEAL")
        summary = C.summarize(item["local_spec"])
        witnesses.append((encoded, tuple(parents), summary, item["rank"]))
    return received, witnesses, {"packet_bytes":len(raw), "receipt_bytes":receipt_bytes,
        "witness_bytes":witness_bytes, "frontiers":len(received), "deltas":len(witnesses),
        "edges":edges, "openings":openings, "bodies":bodies, "rows":rows, "nodes":nodes}


def bind_native(raw, witness, parents, summary, rank, image, foundation, policy):
    """Same-call structural binding only. A fabricated report can pass this."""
    value = C.parse_json(raw, replace(C.DEFAULT_LIMITS, max_bytes=4*MIB))
    C.fields(value, {"schema", "status", "input_sha256", "input_bytes", "journal",
                     "parents", "mathematical_admission"})
    need(value["schema"] == "DMKN_NATIVE_DELTA_CONCLUSION_V1"
         and value["status"] == "CHECKED_CONDITIONAL_RELATION_NOT_ADMISSION"
         and value["mathematical_admission"] is False, "NATIVE_CONDITIONAL_STATUS")
    need(type(value["input_bytes"]) is int and value["input_bytes"] == len(witness)
         and value["input_sha256"] == hashlib.sha256(witness).hexdigest(), "NATIVE_EXACT_INPUT")
    need(type(value["parents"]) is list, "NATIVE_PARENT_ARRAY")
    actual_parents = tuple(journal_bytes(item) for item in value["parents"])
    need(actual_parents == parents, "NATIVE_EXACT_PARENTS")
    raw_journal = journal_bytes(value["journal"]); decoded = journal(raw_journal)
    need(raw_journal[12:44].hex() == image and decoded["foundation"] == foundation
         and decoded["policy"] == policy and decoded["summary"] == summary
         and decoded["rank"] == rank, "NATIVE_OWN_ADOPTED_CONCLUSION")
    return raw_journal, actual_parents


def require_closure(target, graph):
    """Graph keys/edges must come from actual verified/checked journals."""
    seen, pending = set(), [target]
    while pending:
        node = pending.pop()
        if node in seen: continue
        need(node in graph, "MISSING_CERTIFIED_FRONTIER_OR_DELTA", "MISSING_MATERIAL")
        seen.add(node); pending.extend(graph[node])
    need(seen == set(graph), "UNUSED_PACKET_MATERIAL")
