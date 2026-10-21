"""Pure preparation of the one selected same-target RC/general execution pair.

No filesystem, process, receipt verification or mathematical acceptance occurs.
The enclosing owner must bind fixture_sha256 to the independently adopted native
controls fixture, and each image to its actual assembled guest. Caller-supplied
hash equality alone does not discharge either adoption obligation.
"""
import hashlib

from aggregate_claims import bindings as B
from aggregate_claims.input import encode
from modules import codec as C
from restricted_composition import fixtures as F

FIXTURE_LIMIT = 4 * 1024**2
FRAME_LIMIT = 256 * 1024
FRAME_NODES = 32768
FRAME_DEPTH = 64
GENERAL_IMAGE = "9d5072a67f5ab2c4f9468df03c2424d71c457021c4b442d7739c5a3d51ba2865"
BASE_JOURNAL_SHA = "22fe722c57894cb192a6700954fb045a708431a1470e274440c7d60a5767b682"
BASE_RECEIPT_SHA = "850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47"
GENERAL_PREFIX = b"DMKNAI02\x02\x00\x00\x00"
RC_PREFIX = b"DMKNRC01\x01\x00\x00\x00"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def _frame_bounds(value):
    # Iterative traversal matches the RC Value boundary without implementing
    # inference. Charge each occurrence, not Python object identity.
    stack, nodes = [(value, 0)], 0
    while stack:
        current, depth = stack.pop()
        nodes += 1
        C.require(nodes <= FRAME_NODES and depth <= FRAME_DEPTH, "RC_PREP_FRAME_TREE_BOUND")
        if type(current) in (dict, list):
            C.require(len(current) <= FRAME_NODES, "RC_PREP_CONTAINER_BOUND")
            children = list(current.values()) if type(current) is dict else current
            if type(current) is dict:
                C.require(all(type(key) is str and len(key.encode("utf-8")) <= FRAME_LIMIT
                              for key in current), "RC_PREP_KEY_BOUND")
            stack.extend((child, depth + 1) for child in children)
        elif type(current) is str:
            C.require(len(current.encode("utf-8")) <= FRAME_LIMIT, "RC_PREP_STRING_BOUND")
        elif type(current) is int:
            C.uint(current, 2**64 - 1)
        else:
            C.require(current is None or type(current) is bool, "RC_PREP_JSON_VALUE")
    raw = C.canonical(value, C.Limits(max_bytes=FRAME_LIMIT))
    return raw, nodes


def _header(image, members):
    raw = (B.MAGIC + B.VERSION.to_bytes(4, "little") + bytes.fromhex(image)
           + bytes.fromhex(B.RELATION_IMAGE) + bytes.fromhex(B.FOUNDATION)
           + bytes.fromhex(B.POLICY) + B.commitment(members)
           + len(members).to_bytes(4, "little")
           + max(B.member_journal(member)["rank"] for member in members).to_bytes(8, "little")
           + (1).to_bytes(8, "little"))
    decoded = B.decode_header(raw, adopted_image=image)
    C.require(decoded["member_count"] == 2 and decoded["maximum_member_rank"] == 1
              and decoded["seal_height"] == 1, "RC_PREP_EXACT_FIRST_HEADER")
    return raw


def prepare_pair(fixture_raw, *, fixture_sha256, parent_receipt, general_image, restricted_image):
    """Return byte-valued general/restricted arms and a JSON-safe derivation.

    Input is the saved four-field native-controls fixture, not a new theorem
    generator. Both hosts must independently reproduce the expected H, verify
    the same genuine base-I receipt, and execute their actual guest. All returned
    commitments and membership paths are inert predictions until those gates.
    """
    C.digest_string(fixture_sha256)
    C.require(type(fixture_raw) is bytes and 0 < len(fixture_raw) <= FIXTURE_LIMIT
              and digest(fixture_raw) == fixture_sha256, "RC_PREP_ADOPTED_FIXTURE_BYTES")
    C.require(type(parent_receipt) is bytes and 0 < len(parent_receipt) <= 1024**2
              and digest(parent_receipt) == BASE_RECEIPT_SHA, "RC_PREP_EXACT_BASE_RECEIPT")
    B._adopted_image(general_image)
    B._adopted_image(restricted_image)
    C.require(general_image == GENERAL_IMAGE and restricted_image != general_image,
              "RC_PREP_DISTINCT_ACTUAL_IMAGES")
    fixture = C.parse_json(fixture_raw, C.Limits(max_bytes=FIXTURE_LIMIT))
    C.fields(fixture, {"first", "second", "first_witness", "second_witness"})
    first, original = fixture["first"], fixture["first_witness"]
    C.fields(first, {"schema", "image", "rank", "local_spec", "parents", "proofs"})
    C.require(first["schema"] == "DMKN_RESTRICTED_COMPOSITION_V1"
              and type(first["parents"]) is list and len(first["parents"]) == 1,
              "RC_PREP_EXACT_FIRST_FRAME")
    parent = C.fields(first["parents"][0], {"journal", "openings"})
    C.require(type(parent["journal"]) is list and len(parent["journal"]) == 184,
              "RC_PREP_PARENT_EXTENT")
    parent_raw = bytes(C.uint(word, 255) for word in parent["journal"])
    base = B.member_journal(parent_raw)
    C.require(digest(parent_raw) == BASE_JOURNAL_SHA and base["rank"] == 0,
              "RC_PREP_EXACT_BASE_JOURNAL")
    C.require(type(parent["openings"]) is list and len(parent["openings"]) == 1,
              "RC_PREP_ONE_BINARY_CONGR_OPENING")
    C.require(first == F.frame(parent_raw, parent["openings"][0]),
              "RC_PREP_UNCHANGED_CONTEXT_TRANSPORT_PROOF")
    rc_raw, rc_nodes = _frame_bounds(first)
    C.fields(original, {"schema", "image", "rank", "local_spec", "rows", "parents", "bodies"})
    C.require(original["schema"] == "DMKN_CERTIFIED_MODULES_V2" and original["bodies"] == []
              and type(original["rows"]) is list and 413 < len(original["rows"]) <= 32768
              and all(original[key] == first[key] for key in ("image", "rank", "local_spec", "parents")),
              "RC_PREP_MATCHED_ORIGINAL_WITNESS")
    # The adopted native differential checked these exact W rows against RC.
    # Do not re-emit, optimize or reconstruct W differently for either arm.
    general_raw = C.canonical(original, C.Limits(max_bytes=1024**2))
    target = F.predicted_journal(first)
    C.require(target != parent_raw and B.member_journal(target)["rank"] == 1,
              "RC_PREP_NEW_EXACT_TARGET")
    members = sorted([parent_raw, target])
    common = {"claims": [(0, parent_raw)], "frontiers": [(0, parent_raw, 0, [])], "targets": [target]}
    general_wire = encode(adopted_image=general_image, witnesses=[general_raw], **common)
    before = encode(adopted_image=restricted_image, witnesses=[rc_raw], **common)
    C.require(general_wire[:12] == before[:12] == GENERAL_PREFIX
              and len(before) >= 629 and before[629:] == rc_raw
              and general_wire[629:] == general_raw, "RC_PREP_EXACT_ENVELOPE_LAYOUT")
    restricted_wire = RC_PREFIX + before[12:]
    # Exactly one claim, one frontier, one delta, one target. No old-A receipt
    # is relabeled; the only boundary is the unchanged genuine fixed-I receipt.
    C.require(general_wire[44:625] == restricted_wire[44:625]
              and all(int.from_bytes(before[i:i+4], "little") == 1 for i in (44, 48, 52, 56))
              and int.from_bytes(before[625:629], "little") == len(rc_raw)
              and int.from_bytes(general_wire[625:629], "little") == len(general_raw),
              "RC_PREP_IDENTICAL_GRAPH_DIFFERENT_WITNESS")
    general_header, restricted_header = (_header(image, members)
                                        for image in (general_image, restricted_image))
    C.require(general_header[:12] == restricted_header[:12]
              and general_header[44:] == restricted_header[44:], "RC_PREP_ONLY_H_IMAGE_DIFFERS")
    member_rows = []
    for index, member in enumerate(members):
        siblings = B.opening(members, index)
        for image, header in ((general_image, general_header), (restricted_image, restricted_header)):
            B.bind_member(header, member, index, siblings, adopted_image=image)
        member_rows.append({"index": index, "journal": list(member),
                            "siblings": [list(part) for part in siblings]})
    derivation = {"schema": "DMKN_RC_SAME_TARGET_PREPARATION_V1",
        "authority": "UNTRUSTED_PREPARATION_NOT_RECEIPT_OR_ADMISSION",
        "fixture_sha256": fixture_sha256, "fixture_bytes": len(fixture_raw),
        "required_adoption": "Exact fixture digest from adopted native differential; both actual guest images",
        "parent_receipt_sha256": BASE_RECEIPT_SHA, "parent_receipt_bytes": len(parent_receipt),
        "parent_journal": list(parent_raw), "target_journal": list(target), "members": member_rows,
        "restricted_frame": {"sha256": digest(rc_raw), "bytes": len(rc_raw), "json_nodes": rc_nodes},
        "original_witness": {"sha256": digest(general_raw), "bytes": len(general_raw)},
        "arms": {name: {"image": image, "wire_bytes": len(wire), "wire_sha256": digest(wire),
                         "header": list(header), "header_sha256": digest(header)}
                 for name, image, wire, header in (
                     ("general", general_image, general_wire, general_header),
                     ("restricted", restricted_image, restricted_wire, restricted_header))},
        "host_calls": 0, "guest_calls": 0, "proof_calls": 0, "mathematical_admission": False}
    return {"general": {"wire": general_wire, "header": general_header},
            "restricted": {"wire": restricted_wire, "header": restricted_header},
            "parent": parent_raw, "target": target, "derivation": derivation}
