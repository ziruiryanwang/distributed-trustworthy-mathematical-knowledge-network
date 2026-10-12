"""Bounded inert mixed-frontier packets. No cryptography or mathematical authority.

Witness parsing and conditional-output binding reuse the frozen delta helpers.
New wire tags distinguish I receipts from A receipts plus exact member openings.
"""
from dataclasses import asdict, dataclass, replace
import hashlib

from admission.bindings import journal
from aggregate_claims import bindings as B
from delta import packet as D
from delta_claims.claims import expected_journal
from modules import codec as C

SCHEMA = "DMKN_MIXED_DELTA_PACKET_V1"
MIB = D.MIB
need, DeltaError = D.need, D.DeltaError


@dataclass(frozen=True)
class Envelope:
    packet_bytes: int = 32*MIB
    receipt_bytes: int = 8*MIB
    witness_bytes: int = 16*MIB
    claims: int = 8
    frontiers: int = 32
    deltas: int = 16
    edges: int = 128
    openings: int = 4096
    bodies: int = 8192
    rows: int = 250000
    nodes: int = 500000
    depth: int = 128
    rank: int = 2**64-1

    def validate(self):
        need(type(self) is Envelope,"MIXED_EXACT_ENVELOPE")
        for name,cap in asdict(Envelope()).items():
            value = getattr(self,name)
            need(type(value) is int and 0 < value <= cap,"MIXED_ENVELOPE:"+name)

    def delta_limits(self):
        values = asdict(self); del values["claims"]
        return D.Envelope(**values)


def _bytes(value,size):
    need(type(value) is list and len(value) == size
         and all(type(x) is int and 0 <= x <= 255 for x in value),"MIXED_EXACT_BYTES")
    return bytes(value)


def frontier_evidence(claim,frontier):
    """Compact identity of a complete terminal representation, not authority.

    Receipt hash/length avoid copying the same large receipt once per member.
    Actual transferable receipt bytes remain in the packet's claim table.
    """
    tag,statement,receipt = claim
    unused,exact,index,siblings = frontier
    return C.canonical({"tag":tag,"statement":list(statement),
        "receipt_sha256":hashlib.sha256(receipt).hexdigest(),"receipt_bytes":len(receipt),
        "journal":list(exact),"member_index":index,"siblings":[list(s) for s in siblings]})


def parse_packet(raw,limits,*,aggregate_image=None):
    """Return immutable claims/frontiers/witnesses and a charged wire census.

    Complete graph-shape/cap/unused checks happen before any expensive verifier.
    A fabricated mathematically invalid packet may still pass this pure parser.
    """
    limits.validate()
    need(type(raw) is bytes and 0 < len(raw) <= limits.packet_bytes,
         "MIXED_PACKET_BYTES","RESOURCE_INCOMPLETE")
    parse_limits = replace(C.DEFAULT_LIMITS,max_bytes=limits.packet_bytes,
                           max_nodes=limits.nodes,max_depth=limits.depth)
    value = C.parse_json(raw,parse_limits)
    nodes = D._census(value,limits)
    C.fields(value,{"schema","claims","frontiers","deltas"})
    need(value["schema"] == SCHEMA,"MIXED_PACKET_SCHEMA")
    need(type(value["claims"]) is list and len(value["claims"]) <= limits.claims
         and type(value["frontiers"]) is list and len(value["frontiers"]) <= limits.frontiers
         and type(value["deltas"]) is list and 1 <= len(value["deltas"]) <= limits.deltas
         and len(value["frontiers"])+len(value["deltas"]) <= B.MAX_MEMBERS,
         "MIXED_COUNTS","RESOURCE_INCOMPLETE")
    claims,frontiers,seen_claims,used,graph = [],[],set(),set(),{}
    receipt_bytes = 0
    for item in value["claims"]:
        C.fields(item,{"tag","statement","receipt_hex"}); tag = C.uint(item["tag"],1)
        statement = _bytes(item["statement"],184 if tag == 0 else B.HEADER_BYTES)
        if tag == 0: B.member_journal(statement)
        else:
            need(aggregate_image is not None,"MIXED_AGGREGATE_OWNER_REQUIRED","UNSUPPORTED_PROOF_FORM")
            B.decode_header(statement,adopted_image=aggregate_image)
        need((tag,statement) not in seen_claims,"MIXED_DUPLICATE_EXACT_CLAIM")
        seen_claims.add((tag,statement))
        encoded = item["receipt_hex"]
        need(type(encoded) is str and 0 < len(encoded) <= 2*limits.receipt_bytes
             and len(encoded)%2 == 0 and all(c in "0123456789abcdef" for c in encoded),
             "MIXED_RECEIPT_HEX")
        receipt_bytes += len(encoded)//2
        need(receipt_bytes <= limits.receipt_bytes,"MIXED_RECEIPT_BYTES","RESOURCE_INCOMPLETE")
        claims.append((tag,statement,bytes.fromhex(encoded)))
    for item in value["frontiers"]:
        C.fields(item,{"claim_index","journal","member_index","siblings"})
        need(len(claims) > 0,"MIXED_FRONTIER_WITHOUT_CLAIM")
        claim_index = C.uint(item["claim_index"],len(claims)-1)
        index = C.uint(item["member_index"],B.MAX_MEMBERS-1)
        exact = _bytes(item["journal"],184); decoded = B.member_journal(exact)
        need(decoded["rank"] <= limits.rank,"MIXED_FRONTIER_RANK")
        need(type(item["siblings"]) is list and len(item["siblings"]) <= B.MAX_SIBLINGS,
             "MIXED_MEMBER_PATH_BOUND")
        siblings = tuple(_bytes(part,32) for part in item["siblings"])
        tag,statement,unused = claims[claim_index]
        if tag == 0:
            need(exact == statement and index == 0 and not siblings,"MIXED_EXACT_I_FRONTIER")
        else: B.bind_member(statement,exact,index,list(siblings),adopted_image=aggregate_image)
        need(exact not in graph,"MIXED_DUPLICATE_EXACT_FRONTIER")
        graph[exact] = (); used.add(claim_index)
        frontiers.append((claim_index,exact,index,siblings))
    need(used == set(range(len(claims))),"MIXED_UNUSED_CLAIM")
    # Reuse the retained named-witness decoder, not a second relation parser.
    # Temporary canonicalization is bounded by the controller/whole wire limit.
    delta_raw = C.canonical({"schema":D.SCHEMA,"frontiers":[],"deltas":value["deltas"]},parse_limits)
    unused,witnesses,census = D.parse_packet(delta_raw,limits.delta_limits())
    target = None
    image_words = [int.from_bytes(bytes.fromhex(B.RELATION_IMAGE)[i:i+4],"little") for i in range(0,32,4)]
    for item,(witness,parents,summary,rank) in zip(value["deltas"],witnesses):
        need(item["image"] == image_words and all(type(word) is int for word in item["image"]),
             "MIXED_NATIVE_RELATION_IMAGE")
        need(all(parent in graph for parent in parents),"MIXED_MISSING_OR_FORWARD_PARENT","MISSING_MATERIAL")
        need(len(set(parents)) == len(parents),"MIXED_DUPLICATE_PARENT")
        need(rank == (1+max(journal(parent)["rank"] for parent in parents) if parents else 0),
             "MIXED_EXACT_RANK")
        target = expected_journal(summary,rank,B.RELATION_IMAGE); B.member_journal(target)
        need(target not in graph,"MIXED_DUPLICATE_EXACT_DELTA")
        graph[target] = parents
    D.require_closure(target,graph)
    census.update({"packet_bytes":len(raw),"receipt_bytes":receipt_bytes,
        "claims":len(claims),"frontiers":len(frontiers),"warrants":len(graph),"nodes":nodes})
    return tuple(claims),tuple(frontiers),tuple(witnesses),census
