"""Bounded untrusted v2 preparation. No mathematical or receipt authority.

Graph identities and targets are exact 184-byte journals. Never substitute
another rank, union alternative derivations, or discard a submitted new target
in favor of a certified frontier merely because the semantic ModuleID matches.
"""
from aggregate_claims import bindings as B
from modules import codec as C

MAGIC, VERSION = b"DMKNAI02", 2
MAX_BYTES = 16 * 1024**2
MAX_ASSUMPTIONS, MAX_FRONTIERS, MAX_DELTAS = 8, 32, 16


def _u32(value):
    return C.uint(value, 2**32-1).to_bytes(4, "little")


def encode(*, adopted_image, claims, frontiers, witnesses, targets):
    """Encode DMKNAI02; caller supplies genuine matching receipts separately.

    claims: [(0, legacy_J) | (1, v2_aggregate_header)]
    frontiers: [(claim_index, legacy_J, member_index, [sibling_hash_bytes])]
    witnesses: [ordinary relation input bytes], topological order
    targets: [exact 184-byte J], unique and required to be newly checked

    The relation independently checks every witness and graph constraint. This
    encoder does not predict its conclusions. Ambiguous duplicate exact claims
    are refused conservatively instead of selecting a derivation implicitly.
    """
    B._adopted_image(adopted_image)
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
        size += len(raw); parts.append(raw)

    seen_claims = set()
    for claim in claims:
        C.require(type(claim) is tuple and len(claim) == 2, "AGGREGATE_INPUT_CLAIM_TUPLE")
        tag, raw = claim
        C.uint(tag, 1)
        if tag == 0: B.member_journal(raw)
        else: B.decode_header(raw, adopted_image=adopted_image)
        C.require((tag, raw) not in seen_claims, "AGGREGATE_INPUT_DUPLICATE_CLAIM")
        seen_claims.add((tag, raw)); append(bytes([tag])); append(raw)
    used, warrants = set(), set()
    for frontier in frontiers:
        C.require(type(frontier) is tuple and len(frontier) == 4, "AGGREGATE_INPUT_FRONTIER_TUPLE")
        claim_index, raw, member_index, siblings = frontier
        C.require(len(claims) > 0, "AGGREGATE_INPUT_FRONTIER_NO_CLAIM")
        C.uint(claim_index, len(claims)-1); C.uint(member_index, B.MAX_MEMBERS-1)
        B.member_journal(raw)
        C.require(type(siblings) is list and len(siblings) <= B.MAX_SIBLINGS
                  and all(type(part) is bytes and len(part) == 32 for part in siblings),
                  "AGGREGATE_INPUT_SIBLINGS")
        tag, claim_raw = claims[claim_index]
        if tag == 0:
            C.require(raw == claim_raw and member_index == 0 and not siblings,
                      "AGGREGATE_INPUT_LEGACY_FRONTIER")
        else:
            B.bind_member(claim_raw, raw, member_index, siblings, adopted_image=adopted_image)
        C.require(raw not in warrants, "AGGREGATE_INPUT_DUPLICATE_WARRANT")
        warrants.add(raw); used.add(claim_index)
        append(_u32(claim_index)); append(raw); append(_u32(member_index)); append(_u32(len(siblings)))
        for sibling in siblings: append(sibling)
    C.require(used == set(range(len(claims))), "AGGREGATE_INPUT_UNUSED_CLAIM")
    seen_targets = set()
    for target in targets:
        B.member_journal(target)
        C.require(target not in seen_targets, "AGGREGATE_INPUT_DUPLICATE_TARGET")
        C.require(target not in warrants, "AGGREGATE_INPUT_TARGET_MUST_BE_NEW")
        seen_targets.add(target); append(target)
    for witness in witnesses:
        C.require(type(witness) is bytes and 0 < len(witness) <= MAX_BYTES-size-4,
                  "AGGREGATE_INPUT_WITNESS_BOUND")
        append(_u32(len(witness))); append(witness)
    return b"".join(parts)


def from_legacy_packet(raw, frontier_journals, *, adopted_image, targets):
    """Prepare a packet without merging any alternative proof-edge sets.

    Receipt-to-journal equality is checked later by the real host. This helper
    matches inert summary metadata only. No duplicate elimination is implicit.
    """
    from delta.packet import Envelope, parse_packet
    received, witnesses, census = parse_packet(raw, Envelope())
    C.require(type(frontier_journals) is list and len(frontier_journals) == len(received),
              "AGGREGATE_INPUT_FRONTIER_JOURNAL_COUNT")
    claims, frontiers, pending = [], [], []
    for index, ((receipt, summary), raw_journal) in enumerate(zip(received, frontier_journals)):
        value = B.member_journal(raw_journal)
        C.require(C.canonical(value["summary"]) == summary, "AGGREGATE_INPUT_FRONTIER_SUMMARY")
        claims.append((0, raw_journal)); frontiers.append((index, raw_journal, 0, []))
        pending.append((receipt, raw_journal))
    wire = encode(adopted_image=adopted_image, claims=claims, frontiers=frontiers,
                  witnesses=[item[0] for item in witnesses], targets=targets)
    return wire, pending, census
