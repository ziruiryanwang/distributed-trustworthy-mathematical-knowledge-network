"""Pure same-call data binding. Success here NEVER grants mathematical authority.

The owner must independently adopt/run the native executable and require clean
supervised closure. Saved or fabricated JSON can pass structural checks.
"""
import hashlib

from aggregate_claims import bindings as B
from aggregate_claims import input as AI
from modules import codec as C

OUTPUT_BYTES = 128 * 1024
OUTPUT_FIELDS = {"schema", "status", "mathematical_admission", "input_sha256",
                 "input_bytes", "wire_bytes", "header", "assumptions", "members",
                 "edges", "census"}
CENSUS_LIMITS = {"rows": 250000, "bodies": 8192, "openings": 4096,
                 "nodes": 500000, "maximum_depth": 128, "parent_edges": 128}


def _bytes(value, length):
    C.require(type(value) is list and len(value) == length, "NATIVE_CLOSURE_BYTE_ARRAY")
    for part in value:
        C.uint(part, 255)
    return bytes(value)


def _wire(wire, targets, adopted_image):
    """Check zero-premise framing only, not mathematical witness contents."""
    B._adopted_image(adopted_image)
    C.require(type(wire) is bytes and 60 <= len(wire) <= AI.MAX_BYTES,
              "NATIVE_CLOSURE_WIRE_BYTES")
    C.require(wire[:8] == AI.MAGIC and int.from_bytes(wire[8:12], "little") == AI.VERSION
              and wire[12:44].hex() == adopted_image, "NATIVE_CLOSURE_WIRE_PROFILE")
    counts = tuple(int.from_bytes(wire[i:i+4], "little") for i in range(44, 60, 4))
    claims, frontiers, witnesses, target_count = counts
    C.require(claims == 0 and frontiers == 0, "NATIVE_CLOSURE_ZERO_INPUT_PREMISES")
    C.require(1 <= witnesses <= AI.MAX_DELTAS and 1 <= target_count <= witnesses,
              "NATIVE_CLOSURE_WIRE_COUNTS")
    C.require(type(targets) is list and len(targets) == target_count,
              "NATIVE_CLOSURE_TARGET_LIST")
    for target in targets:
        B.member_journal(target)
    C.require(len(set(targets)) == len(targets), "NATIVE_CLOSURE_DUPLICATE_TARGET")
    position = 60
    for target in targets:
        C.require(wire[position:position+184] == target, "NATIVE_CLOSURE_EXACT_INPUT_TARGET")
        position += 184
    for _ in range(witnesses):
        C.require(position+4 <= len(wire), "NATIVE_CLOSURE_FRAME_PREFIX")
        size = int.from_bytes(wire[position:position+4], "little")
        position += 4
        C.require(0 < size <= len(wire)-position, "NATIVE_CLOSURE_FRAME_BOUND")
        position += size
    C.require(position == len(wire), "NATIVE_CLOSURE_COMPLETE_WIRE")
    return witnesses


def bind_output(raw, wire, targets, *, adopted_image):
    """Return inert exact J data; a header image does not adopt the executable."""
    count = _wire(wire, targets, adopted_image)
    value = C.parse_json(raw, C.Limits(max_bytes=OUTPUT_BYTES))
    C.fields(value, OUTPUT_FIELDS)
    C.require(value["schema"] == "DMKN_NATIVE_AGGREGATE_CONCLUSION_V1"
              and value["status"] == "CHECKED_CONDITIONAL_AGGREGATE_NOT_ADMISSION"
              and value["mathematical_admission"] is False, "NATIVE_CLOSURE_OUTPUT_STATUS")
    C.require(type(value["assumptions"]) is list and not value["assumptions"],
              "NATIVE_CLOSURE_ZERO_OUTPUT_PREMISES")
    digest = hashlib.sha256(wire).hexdigest()
    C.digest_string(value["input_sha256"])
    C.uint(value["input_bytes"], AI.MAX_BYTES); C.uint(value["wire_bytes"], AI.MAX_BYTES)
    C.require(value["input_sha256"] == digest and value["input_bytes"] == len(wire)
              and value["wire_bytes"] == len(wire), "NATIVE_CLOSURE_EXACT_INPUT")
    header = _bytes(value["header"], B.HEADER_BYTES)
    decoded = B.decode_header(header, adopted_image=adopted_image)
    C.require(decoded["member_count"] == count and decoded["seal_height"] == 1,
              "NATIVE_CLOSURE_HEADER_COUNTS")
    C.require(type(value["members"]) is list and len(value["members"]) == count,
              "NATIVE_CLOSURE_MEMBER_LIST")
    members, ranks = [], []
    for index, item in enumerate(value["members"]):
        C.fields(item, {"index", "journal", "siblings"})
        C.uint(item["index"], count-1)
        C.require(item["index"] == index, "NATIVE_CLOSURE_MEMBER_INDEX")
        member = _bytes(item["journal"], 184)
        C.require(type(item["siblings"]) is list and len(item["siblings"]) <= B.MAX_SIBLINGS,
                  "NATIVE_CLOSURE_OPENING_BOUND")
        siblings = [_bytes(part, 32) for part in item["siblings"]]
        bound = B.bind_member(header, member, index, siblings, adopted_image=adopted_image)
        members.append(member); ranks.append(bound["rank"])
    # commitment independently requires strict exact-J order and uniqueness.
    C.require(B.commitment(members).hex() == decoded["members_root"]
              and max(ranks) == decoded["maximum_member_rank"] and max(ranks) < count,
              "NATIVE_CLOSURE_COMPLETE_MEMBER_BINDING")
    C.require(all(target in members for target in targets), "NATIVE_CLOSURE_TARGET_MEMBERSHIP")
    C.uint(value["edges"], min(128, count*(count-1)//2))
    C.fields(value["census"], set(CENSUS_LIMITS))
    for key, maximum in CENSUS_LIMITS.items():
        C.uint(value["census"][key], maximum)
    C.require(value["census"]["parent_edges"] == value["edges"], "NATIVE_CLOSURE_EDGE_CENSUS")
    return {"header": header, "members": tuple(members), "input_sha256": digest,
            "input_bytes": len(wire), "census": dict(value["census"]), "edges": value["edges"]}
