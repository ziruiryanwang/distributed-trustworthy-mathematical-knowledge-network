"""Pure exact-target selection for aggregate sealing; never proof or admission.

The retained mixed parser owns packet grammar. The retained aggregate encoder
owns wire grammar. This helper only selects a backward-closed subgraph and
computes an expected header that the actual native/guest checker must confirm.
No I/O, receipt verification, source execution, funding or fallback occurs here.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib

from aggregate_claims import bindings as B
from aggregate_claims.input import encode
from delta.packet import require_closure
from delta_claims.claims import expected_journal
from mixed_claims import packet as P
from modules import codec as C


@dataclass(frozen=True, slots=True)
class ParentClaim:
    tag: int
    statement: bytes
    receipt: bytes


@dataclass(frozen=True, slots=True)
class SelectedWitness:
    input_index: int
    journal: bytes
    bytes: int
    sha256: str


@dataclass(frozen=True, slots=True)
class SealCensus:
    input_packet_bytes: int
    input_witness_bytes: int
    wire_bytes: int
    receipt_bytes: int
    maximum_parent_receipt_bytes: int
    claims: int
    frontiers: int
    deltas: int
    members: int
    edges: int


@dataclass(frozen=True, slots=True)
class PreparedSeal:
    adopted_image: str
    input_sha256: str
    input_bytes: int
    target_journal: bytes
    wire: bytes
    expected_header: bytes
    parents: tuple[ParentClaim, ...]
    members: tuple[bytes, ...]
    target_index: int
    target_siblings: tuple[bytes, ...]
    selected_claim_indices: tuple[int, ...]
    selected_frontier_indices: tuple[int, ...]
    selected_delta_indices: tuple[int, ...]
    witnesses: tuple[SelectedWitness, ...]
    census: SealCensus
    status: str = "UNTRUSTED_MIXED_SEAL_PREPARATION"
    mathematical_admission: bool = False


def prepare_mixed_seal(raw: bytes, target_journal: bytes, *, adopted_image: str,
                       envelope: P.Envelope) -> PreparedSeal:
    """Select one existing native exact J, preserving its entire needed closure.

    The caller supplies the adopted A image and unchanged finite mixed envelope.
    Existing certified frontiers are terminal premises, not targets to reprove.
    Parent receipts in the return remain unverified candidates, in wire order.
    Witness bytes are the existing parser's canonical named-record encoding,
    not arbitrary whitespace substrings of the original packet JSON.
    """
    C.require(type(raw) is bytes, "MIXED_SEAL_IMMUTABLE_PACKET_BYTES")
    C.require(type(target_journal) is bytes and len(target_journal) == 184,
              "MIXED_SEAL_EXACT_TARGET_BYTES")
    C.require(type(envelope) is P.Envelope, "MIXED_SEAL_EXACT_ENVELOPE")
    B._adopted_image(adopted_image)
    B.member_journal(target_journal)
    claims, frontiers, witnesses, input_census = P.parse_packet(
        raw, envelope, aggregate_image=adopted_image)

    # The parser already rejects duplicate exact Js, forward/missing parents,
    # wrong ranks/profiles, unused input material and invalid A membership paths.
    graph = {exact: () for unused, exact, unused_index, unused_path in frontiers}
    native_keys = []
    facts = {exact: B.member_journal(exact) for exact in graph}
    for unused, parents, summary, rank in witnesses:
        exact = expected_journal(summary, rank, B.RELATION_IMAGE)
        C.require(exact not in graph, "MIXED_SEAL_DUPLICATE_EXACT_NODE")
        facts[exact] = B.member_journal(exact)
        graph[exact] = parents
        native_keys.append(exact)
    C.require(target_journal in native_keys, "MIXED_SEAL_TARGET_MUST_BE_NATIVE_DELTA")
    C.require(len(graph) <= B.MAX_MEMBERS, "MIXED_SEAL_MEMBER_LIMIT")

    selected, pending = set(), [target_journal]
    while pending:
        exact = pending.pop()
        if exact in selected:
            continue
        C.require(exact in graph, "MIXED_SEAL_MISSING_EXACT_PARENT")
        selected.add(exact)
        C.require(len(selected) <= B.MAX_MEMBERS, "MIXED_SEAL_FINITE_CLOSURE")
        pending.extend(graph[exact])
    selected_graph = {exact: graph[exact] for exact in selected}
    require_closure(target_journal, selected_graph)

    delta_indices = tuple(i for i, exact in enumerate(native_keys) if exact in selected)
    frontier_indices = tuple(i for i, row in enumerate(frontiers) if row[1] in selected)
    claim_indices = tuple(sorted({frontiers[i][0] for i in frontier_indices}))
    remap = {old: new for new, old in enumerate(claim_indices)}
    parents = tuple(ParentClaim(*claims[i]) for i in claim_indices)
    selected_frontiers = [
        (remap[frontiers[i][0]], frontiers[i][1], frontiers[i][2], list(frontiers[i][3]))
        for i in frontier_indices]
    wire = encode(adopted_image=adopted_image,
                  claims=[(parent.tag, parent.statement) for parent in parents],
                  frontiers=selected_frontiers,
                  witnesses=[witnesses[i][0] for i in delta_indices],
                  targets=[target_journal])

    # Rust relation::Graph uses a BTreeMap keyed by the full exact journal.
    members = tuple(sorted(selected))
    maximum_rank = max(facts[exact]["rank"] for exact in members)
    parent_height = max((B.decode_header(parent.statement, adopted_image=adopted_image)["seal_height"]
                         for parent in parents if parent.tag == 1), default=0)
    C.require(parent_height < 2**64-1, "MIXED_SEAL_HEIGHT_OVERFLOW")
    height = parent_height+1
    expected = (B.MAGIC + B.VERSION.to_bytes(4, "little") + bytes.fromhex(adopted_image)
                + bytes.fromhex(B.RELATION_IMAGE) + bytes.fromhex(B.FOUNDATION)
                + bytes.fromhex(B.POLICY) + B.commitment(list(members))
                + len(members).to_bytes(4, "little") + maximum_rank.to_bytes(8, "little")
                + height.to_bytes(8, "little"))
    header = B.decode_header(expected, adopted_image=adopted_image)
    C.require(header["member_count"] == len(members)
              and header["maximum_member_rank"] == maximum_rank
              and header["seal_height"] == height, "MIXED_SEAL_EXPECTED_HEADER")
    index = members.index(target_journal)
    siblings = tuple(B.opening(list(members), index))
    B.bind_member(expected, target_journal, index, list(siblings), adopted_image=adopted_image)

    selections = tuple(SelectedWitness(i, native_keys[i], len(witnesses[i][0]),
                                       hashlib.sha256(witnesses[i][0]).hexdigest())
                       for i in delta_indices)
    census = SealCensus(
        input_packet_bytes=len(raw), input_witness_bytes=input_census["witness_bytes"],
        wire_bytes=len(wire), receipt_bytes=sum(len(parent.receipt) for parent in parents),
        maximum_parent_receipt_bytes=max((len(parent.receipt) for parent in parents), default=0),
        claims=len(parents), frontiers=len(frontier_indices), deltas=len(delta_indices),
        members=len(members), edges=sum(len(graph[exact]) for exact in selected))
    return PreparedSeal(
        adopted_image=adopted_image, input_sha256=hashlib.sha256(raw).hexdigest(),
        input_bytes=len(raw), target_journal=target_journal, wire=wire,
        expected_header=expected, parents=parents, members=members, target_index=index,
        target_siblings=siblings, selected_claim_indices=claim_indices,
        selected_frontier_indices=frontier_indices, selected_delta_indices=delta_indices,
        witnesses=selections, census=census)
