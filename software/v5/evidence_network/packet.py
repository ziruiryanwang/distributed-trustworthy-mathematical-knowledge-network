"""Two exact inert evidence forms; no verifier, opaque handle or new mathematics."""
from modules import codec as C
from aggregate_claims import bindings as B
from mixed_claims import packet as P
from delta_claims.claims import expected_journal

MIB = 1024**2
SCHEMA = "DMKN_CERTIFIED_TERMINAL_MEMBER_V1"
MAX_RECEIPT = 8*MIB


def validate_limits(envelope, terminal_receipt_bytes):
    C.require(type(envelope) is P.Envelope, "EVIDENCE_EXACT_MIXED_ENVELOPE")
    envelope.validate()
    C.require(0 < C.uint(terminal_receipt_bytes, MAX_RECEIPT), "TERMINAL_RECEIPT_LIMIT")


def _decode(raw, envelope, aggregate_image, terminal_receipt_bytes):
    validate_limits(envelope, terminal_receipt_bytes); B._adopted_image(aggregate_image)
    limits = C.Limits(max_bytes=envelope.packet_bytes)
    value = C.parse_json(raw, limits)
    C.require(C.canonical(value, limits) == raw, "EVIDENCE_CANONICAL_BYTES")
    C.require(type(value) is dict, "EVIDENCE_OBJECT")
    return value


def _bytes(value, size):
    C.require(type(value) is list and len(value) == size
              and all(type(part) is int and 0 <= part <= 255 for part in value),
              "TERMINAL_EXACT_BYTE_ARRAY")
    return bytes(value)


def _terminal(value, envelope, aggregate_image, terminal_receipt_bytes):
    C.fields(value, {"schema", "header", "journal", "member_index", "siblings", "receipt_hex"})
    C.require(value["schema"] == SCHEMA, "TERMINAL_SCHEMA")
    header = _bytes(value["header"], B.HEADER_BYTES)
    exact = _bytes(value["journal"], 184)
    index = C.uint(value["member_index"], B.MAX_MEMBERS-1)
    C.require(type(value["siblings"]) is list and len(value["siblings"]) <= B.MAX_SIBLINGS,
              "TERMINAL_SIBLING_COUNT")
    siblings = tuple(_bytes(part, 32) for part in value["siblings"])
    member = B.bind_member(header, exact, index, list(siblings), adopted_image=aggregate_image)
    C.require(member["rank"] <= envelope.rank, "TERMINAL_MEMBER_RANK_BOUND")
    encoded = value["receipt_hex"]
    C.require(type(encoded) is str and 0 < len(encoded) <= 2*terminal_receipt_bytes
              and len(encoded)%2 == 0 and all(part in "0123456789abcdef" for part in encoded),
              "TERMINAL_RECEIPT_HEX")
    receipt = bytes.fromhex(encoded)
    return receipt, header, exact, index, siblings, member


def parse_terminal(raw, envelope, *, aggregate_image, terminal_receipt_bytes=MAX_RECEIPT):
    """Return exact bytes and copied structural facts, never mathematical authority.

    The fixed raw-byte cap bounds JSON decoding. C.parse_json does not itself
    enforce a node/depth census; exact fixed fields bound subsequent traversal.
    """
    value = _decode(raw, envelope, aggregate_image, terminal_receipt_bytes)
    return _terminal(value, envelope, aggregate_image, terminal_receipt_bytes)


def inspect_evidence(raw, envelope, *, aggregate_image, terminal_receipt_bytes=MAX_RECEIPT):
    """Return (kind, summary, exact J, JSON-safe structural census)."""
    value = _decode(raw, envelope, aggregate_image, terminal_receipt_bytes)
    if value.get("schema") == P.SCHEMA:
        # Retain the original mixed grammar/census; no zero-delta relaxation.
        unused_claims, unused_frontiers, witnesses, census = P.parse_packet(
            raw, envelope, aggregate_image=aggregate_image)
        unused_raw, unused_parents, summary, rank = witnesses[-1]
        exact = expected_journal(summary, rank, B.RELATION_IMAGE)
        return "mixed", summary, exact, {**census, "evidence_kind": "mixed", "packet_bytes": len(raw)}
    C.require(value.get("schema") == SCHEMA, "EVIDENCE_UNSUPPORTED_SCHEMA")
    receipt, unused_header, exact, unused_index, siblings, member = _terminal(
        value, envelope, aggregate_image, terminal_receipt_bytes)
    census = {"evidence_kind": "terminal", "packet_bytes": len(raw), "receipt_bytes": len(receipt),
              "claims": 1, "deltas": 0, "frontiers": 1, "selected_members": 1,
              "membership_siblings": len(siblings)}
    return "terminal", member["summary"], exact, census


def pack_terminal(header, journal, index, siblings, receipt, *, aggregate_image, envelope,
                  terminal_receipt_bytes=MAX_RECEIPT):
    """Encode owner-supplied exact bytes; successful encoding is not verification."""
    validate_limits(envelope, terminal_receipt_bytes)
    C.require(type(header) is bytes and len(header) == B.HEADER_BYTES
              and type(journal) is bytes and len(journal) == 184
              and type(receipt) is bytes and 0 < len(receipt) <= terminal_receipt_bytes
              and type(siblings) in (list, tuple) and len(siblings) <= B.MAX_SIBLINGS
              and all(type(part) is bytes and len(part) == 32 for part in siblings),
              "TERMINAL_IMMUTABLE_INPUT")
    C.uint(index, B.MAX_MEMBERS-1)
    raw = C.canonical({"schema": SCHEMA, "header": list(header), "journal": list(journal),
        "member_index": index, "siblings": [list(part) for part in siblings], "receipt_hex": receipt.hex()},
        C.Limits(max_bytes=envelope.packet_bytes))
    parse_terminal(raw, envelope, aggregate_image=aggregate_image, terminal_receipt_bytes=terminal_receipt_bytes)
    return raw
