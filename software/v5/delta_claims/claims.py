"""Inert exact-J binding helpers. Fabricated inputs can pass; no authority here."""
import hashlib

from admission.bindings import journal
from modules import codec as C
from delta.packet import need, parse_packet


def expected_journal(summary, rank, image):
    """Construct a requested statement, NOT prove it or choose its rank."""
    C.validate_summary(summary); C.uint(rank, 2**64-1); C.digest_string(image)
    raw = (b"DMKNM002" + (2).to_bytes(4, "little") + bytes.fromhex(image)
        + bytes.fromhex(summary["foundation"]) + bytes.fromhex(summary["policy"])
        + bytes.fromhex(C.summary_id(summary)) + bytes.fromhex(summary["group_root"])
        + summary["group_count"].to_bytes(4, "little") + rank.to_bytes(8, "little"))
    need(journal(raw)["summary"] == summary, "EXACT_WARRANT_ENCODING")
    return raw


def bind_members(raw, members, *, envelope, image, profile, packet_digest):
    """Bind packet representations to copied facts from a SAME live verifier.

    This helper cannot establish that its members came from such a verifier;
    the exact-class session must enforce that boundary before and after calling.
    """
    received, witnesses, unused = parse_packet(raw, envelope)
    need(hashlib.sha256(raw).hexdigest() == packet_digest, "CLAIM_PACKET_HASH")
    need(type(members) is list and len(members) == len(received)+len(witnesses),
         "CLAIM_PACKET_MEMBER_COUNT")
    actual = {}
    for item in members:
        C.fields(item, {"module","summary","journal","profile_id","packet_sha256",
                        "proof_form","evidence_sha256"})
        parsed = journal(item["journal"])
        need(item["journal"] not in actual and parsed["module"] == item["module"]
             and parsed["summary"] == item["summary"] and item["profile_id"] == profile
             and item["packet_sha256"] == packet_digest, "CLAIM_ACTUAL_MEMBER_BINDING")
        actual[item["journal"]] = item
    pending = {}

    def register(exact, summary, form, payload, parents):
        need(exact in actual and exact not in pending, "CLAIM_ACTUAL_EXACT_J_REQUIRED")
        item = actual[exact]
        need(item["summary"] == summary and item["proof_form"] == form
             and item["evidence_sha256"] == hashlib.sha256(payload).hexdigest(),
             "CLAIM_EXACT_REPRESENTATION_BINDING")
        pending[exact] = (exact, form, payload, tuple(parents), packet_digest)

    for receipt, summary_bytes in received:
        summary = C.parse_json(summary_bytes); digest = hashlib.sha256(receipt).hexdigest()
        candidates = [exact for exact,item in actual.items()
            if item["proof_form"] == "receipt-frontier" and item["evidence_sha256"] == digest
            and item["summary"] == summary]
        need(len(candidates) == 1, "CLAIM_RECEIPT_EXACT_J_UNAMBIGUOUS")
        register(candidates[0],summary,"receipt-frontier",receipt,())
    for witness,parents,summary,rank in witnesses:
        register(expected_journal(summary,rank,image),summary,"native-delta",witness,parents)
    need(set(pending) == set(actual), "CLAIM_COMPLETE_ACTUAL_INVENTORY")
    need(all(set(node[3]) <= set(pending) for node in pending.values()), "CLAIM_COMPLETE_EXACT_ANCESTRY")
    return pending
