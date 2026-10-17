"""Pure selected H2 input construction; no layout, file write or admission.

The generic owner accepts ordinary selected packets. This helper reconstructs
only the retained BASE+FIRST selection and proves byte equality to its selected
wire/header/ordered I receipt before a caller may request a fresh layout.
"""
from aggregate_claims.prepare_mixed import prepare_mixed_seal
from mixed_claims.packet import Envelope, SCHEMA
from modules import codec as C
from production import producer as P

IMAGE = "99b9f1cf14f922f13790b4949999dd71f3da9143465a0033299cd3a3a960ec60"
REFERENCES = (
    (113849, "898660ddeea92cefccbf793e35b1ee49ef4867c9daec24b5344f37a1ed375500"),
    (192, "49dd845edaec83f5b0cba5af38653f768e51ed95a4bb6ea7824c10bdd1c3169e"),
    (223594, "850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47"))
TARGET_SHA = "07734789fd165d5c29667a2925c09b882d346db97a511c75644f2cb4b8ccd0da"
WITNESS_SHA = "88b71b8282afc99297bf6564d22616fce6211eed9a9e18afa1cb42a41d1206e1"


def prepare_h2(wire: bytes, header: bytes, receipt: bytes, *, envelope: Envelope):
    """Return (ordinary packet bytes, PreparedSeal), without trusting either.

    Fixed offsets apply only after exact retained byte-length/hash checks. The
    generic parser/selector/encoder must reconstruct every selected input byte.
    Native parent verification and successful guest execution remain mandatory.
    """
    for raw, (size, expected) in zip((wire, header, receipt), REFERENCES):
        P.require(type(raw) is bytes and len(raw) == size and P.hash_bytes(raw) == expected,
                  "GEOMETRY17_H2_SELECTED_REFERENCE")
    base, target, first = wire[61:245], wire[441:625], wire[629:]
    P.require(P.hash_bytes(target) == TARGET_SHA and P.hash_bytes(first) == WITNESS_SHA,
              "GEOMETRY17_H2_EXACT_TARGET_AND_WITNESS")
    packet = C.canonical({"schema": SCHEMA,
        "claims": [{"tag": 0, "statement": list(base), "receipt_hex": receipt.hex()}],
        "frontiers": [{"claim_index": 0, "journal": list(base), "member_index": 0, "siblings": []}],
        "deltas": [C.parse_json(first)]})
    prepared = prepare_mixed_seal(packet, target, adopted_image=IMAGE, envelope=envelope)
    P.require(prepared.wire == wire and prepared.expected_header == header
              and len(prepared.parents) == 1 and prepared.parents[0].tag == 0
              and prepared.parents[0].statement == base and prepared.parents[0].receipt == receipt
              and prepared.target_journal == target and prepared.mathematical_admission is False,
              "GEOMETRY17_H2_GENERIC_PREPARATION_EXACT_BYTES")
    return packet, prepared
