"""Bounded, untrusted aggregate input preparation; never receipt authority.

The Rust relation independently checks every mathematical frame and graph edge.
The guest must separately verify every pending I/A claim. This encoder does not
decode receipts, run mathematics, predict guest feasibility, or mint handles.
"""
from aggregate import bindings as B
from delta.packet import Envelope, parse_packet
from modules import codec as C

MAGIC, VERSION = b"DMKNAI01", 1
MAX_BYTES = 16 * 1024**2
MAX_ASSUMPTIONS, MAX_FRONTIERS, MAX_DELTAS = 8, 32, 16


def _u32(value):
    return C.uint(value, 2**32-1).to_bytes(4, "little")


def encode(*, adopted_image, claims, frontiers, witnesses, targets):
    """Encode exact inert tuples into DMKNAI01 bytes.

    claims: [(0, legacy_journal_bytes) | (1, aggregate_header_bytes)]
    frontiers: [(claim_index, legacy_journal_bytes, member_index, [hash_bytes])]
    witnesses: [exact ordinary relation input bytes], in topological order
    targets: [raw 32-byte ModuleID], unique new targets

    Neither topological validity nor proof correctness is asserted by encoding.
    The caller must supply actual matching receipts separately to the host.
    """
    C.digest_string(adopted_image)
    C.require(adopted_image not in ("00"*32, B.RELATION_IMAGE), "AGGREGATE_INPUT_IMAGE")
    for value, maximum, minimum in ((claims, MAX_ASSUMPTIONS, 0),
                                    (frontiers, MAX_FRONTIERS, 0),
                                    (witnesses, MAX_DELTAS, 1),
                                    (targets, MAX_DELTAS, 1)):
        C.require(type(value) is list and minimum <= len(value) <= maximum,
                  "AGGREGATE_INPUT_COUNTS")
    C.require(len(targets) <= len(witnesses) and len(frontiers)+len(witnesses) <= B.MAX_MEMBERS,
              "AGGREGATE_INPUT_MEMBER_TARGET_COUNTS")
    parts = [MAGIC, _u32(VERSION), bytes.fromhex(adopted_image)]
    parts.extend(_u32(len(value)) for value in (claims, frontiers, witnesses, targets))
    size = sum(len(part) for part in parts)

    def append(raw):
        nonlocal size
        C.require(type(raw) is bytes and len(raw) <= MAX_BYTES-size,
                  "AGGREGATE_INPUT_WIRE_BOUND")
        size += len(raw)
        parts.append(raw)

    seen_claims = set()
    for claim in claims:
        C.require(type(claim) is tuple and len(claim) == 2, "AGGREGATE_INPUT_CLAIM_TUPLE")
        tag, raw = claim
        C.uint(tag, 1)
        if tag == 0:
            B.member_journal(raw)
        else:
            B.decode_header(raw, adopted_image=adopted_image)
        C.require((tag, raw) not in seen_claims, "AGGREGATE_INPUT_DUPLICATE_CLAIM")
        seen_claims.add((tag, raw))
        append(bytes([tag])); append(raw)
    used, modules = set(), set()
    for frontier in frontiers:
        C.require(type(frontier) is tuple and len(frontier) == 4, "AGGREGATE_INPUT_FRONTIER_TUPLE")
        claim_index, raw, member_index, siblings = frontier
        C.require(len(claims) > 0, "AGGREGATE_INPUT_FRONTIER_NO_CLAIM")
        C.uint(claim_index, len(claims)-1); C.uint(member_index, B.MAX_MEMBERS-1)
        value = B.member_journal(raw)
        C.require(type(siblings) is list and len(siblings) <= B.MAX_SIBLINGS
                  and all(type(part) is bytes and len(part) == 32 for part in siblings),
                  "AGGREGATE_INPUT_SIBLINGS")
        tag, claim_raw = claims[claim_index]
        if tag == 0:
            C.require(raw == claim_raw and member_index == 0 and not siblings,
                      "AGGREGATE_INPUT_LEGACY_FRONTIER")
        else:
            B.bind_member(claim_raw, raw, member_index, siblings, adopted_image=adopted_image)
        C.require(value["module"] not in modules, "AGGREGATE_INPUT_DUPLICATE_MODULE")
        modules.add(value["module"]); used.add(claim_index)
        append(_u32(claim_index)); append(raw); append(_u32(member_index)); append(_u32(len(siblings)))
        for sibling in siblings: append(sibling)
    C.require(used == set(range(len(claims))), "AGGREGATE_INPUT_UNUSED_CLAIM")
    seen_targets = set()
    for target in targets:
        C.require(type(target) is bytes and len(target) == 32 and target not in seen_targets,
                  "AGGREGATE_INPUT_TARGET")
        seen_targets.add(target); append(target)
    for witness in witnesses:
        C.require(type(witness) is bytes and 0 < len(witness) <= MAX_BYTES-size-4,
                  "AGGREGATE_INPUT_WITNESS_BOUND")
        append(_u32(len(witness))); append(witness)
    return b"".join(parts)


def from_legacy_packet(raw, frontier_journals, *, adopted_image, targets):
    """Return untrusted wire and exact pending receipt pairs from a delta packet.

    Frontier journals must be supplied in packet order. Their summaries are
    matched, but the receipt-to-journal claim is NOT verified here. The real host
    must verify each (receipt, journal) pair before using it as an SDK assumption.
    Canonical named witness encoding is the same as the existing delta receiver;
    original packet bytes and their lineage remain separately preserved.
    """
    received, witnesses, census = parse_packet(raw, Envelope())
    C.require(type(frontier_journals) is list and len(frontier_journals) == len(received),
              "AGGREGATE_INPUT_FRONTIER_JOURNAL_COUNT")
    claims, frontiers, pending = [], [], []
    for index, ((receipt, summary), journal) in enumerate(zip(received, frontier_journals)):
        value = B.member_journal(journal)
        C.require(C.canonical(value["summary"]) == summary, "AGGREGATE_INPUT_FRONTIER_SUMMARY")
        claims.append((0, journal)); frontiers.append((index, journal, 0, []))
        pending.append((receipt, journal))
    wire = encode(adopted_image=adopted_image, claims=claims, frontiers=frontiers,
                  witnesses=[item[0] for item in witnesses], targets=targets)
    return wire, pending, census
