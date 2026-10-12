"""Inert aggregate header/member binding; NO receipt verification or authority.

Keep the 192-byte aggregate statement distinct from the legacy 184-byte module
statement. The actual future receiver must verify a genuine resolved A receipt
and bind its exact journal before calling these helpers. Fabricated commitments
can satisfy every check below; they do not establish mathematical validity.
"""
import hashlib

from admission.bindings import journal
from modules import codec as C

MAGIC, VERSION, HEADER_BYTES = b"DMKNA001", 1, 192
MAX_MEMBERS, MAX_SIBLINGS = 48, 6
RELATION_IMAGE = "9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e"
FOUNDATION = "d931d114155cf3cf0dc0b868aa88c6d38b8ada8ecafe267a5934934075782481"
POLICY = "5edfd0ee15b141b7304e26c1a39cd11f7f7e721713cf099813ae4f4442fad377"
LEAF_DOMAIN = b"DMKN-V5-AGGREGATE\0LEAF\0"
NODE_DOMAIN = b"DMKN-V5-AGGREGATE\0NODE\0"
ROOT_DOMAIN = b"DMKN-V5-AGGREGATE\0ROOT\0"


def _u32(value):
    return C.uint(value, 2**32-1).to_bytes(4, "little")


def _sha(raw):
    return hashlib.sha256(raw).digest()


def _adopted_image(image):
    C.digest_string(image)
    C.require(image not in ("00"*32, RELATION_IMAGE), "AGGREGATE_DISTINCT_ADOPTED_IMAGE")


def member_journal(raw):
    value = journal(raw)
    C.require(raw[12:44].hex() == RELATION_IMAGE and value["foundation"] == FOUNDATION
              and value["policy"] == POLICY and 1 <= value["group_count"] <= 4096,
              "AGGREGATE_MEMBER_RELATION_PROFILE")
    return value


def decode_header(raw, *, adopted_image):
    _adopted_image(adopted_image)
    C.require(type(raw) is bytes and len(raw) == HEADER_BYTES and raw[:8] == MAGIC
              and raw[8:12] == _u32(VERSION), "AGGREGATE_EXACT_HEADER_LAYOUT")
    value = {"aggregate_image": raw[12:44].hex(), "relation_image": raw[44:76].hex(),
             "foundation": raw[76:108].hex(), "policy": raw[108:140].hex(),
             "members_root": raw[140:172].hex(), "member_count": int.from_bytes(raw[172:176], "little"),
             "maximum_member_rank": int.from_bytes(raw[176:184], "little"),
             "seal_height": int.from_bytes(raw[184:192], "little")}
    C.require(value["aggregate_image"] == adopted_image and value["relation_image"] == RELATION_IMAGE
              and value["foundation"] == FOUNDATION and value["policy"] == POLICY,
              "AGGREGATE_ADOPTED_PROFILE")
    C.require(1 <= value["member_count"] <= MAX_MEMBERS and value["seal_height"] > 0,
              "AGGREGATE_HEADER_COUNT_OR_HEIGHT")
    return value


def _leaf(count, index, raw):
    return _sha(LEAF_DOMAIN+_u32(count)+_u32(index)+raw)


def _node(count, level, left, right):
    return _sha(NODE_DOMAIN+_u32(count)+_u32(level)+left+right)


def _root(count, top):
    return _sha(ROOT_DOMAIN+_u32(count)+top)


def _leaves(members):
    C.require(type(members) is list and 1 <= len(members) <= MAX_MEMBERS,
              "AGGREGATE_MEMBERS_BOUND")
    previous, hashes = None, []
    for index, raw in enumerate(members):
        value = member_journal(raw)
        C.require(previous is None or previous < value["module"], "AGGREGATE_STRICT_MEMBER_ORDER")
        previous = value["module"]
        hashes.append(_leaf(len(members), index, raw))
    return hashes


def commitment(members):
    """Structural digest of sorted unique journals, NOT a certificate."""
    hashes = _leaves(members); count, level = len(hashes), 0
    while len(hashes) > 1:
        hashes = [_node(count, level, hashes[i], hashes[min(i+1, len(hashes)-1)])
                  for i in range(0, len(hashes), 2)]
        level += 1
    return _root(count, hashes[0])


def opening(members, index):
    hashes = _leaves(members); count = len(hashes)
    C.uint(index, count-1)
    position, level, siblings = index, 0, []
    while len(hashes) > 1:
        siblings.append(hashes[min(position ^ 1, len(hashes)-1)])
        hashes = [_node(count, level, hashes[i], hashes[min(i+1, len(hashes)-1)])
                  for i in range(0, len(hashes), 2)]
        position //= 2; level += 1
    return siblings


def bind_member(header_raw, member_raw, index, siblings, *, adopted_image):
    """Bind a selected journal to a header; receipt verification is separate."""
    header = decode_header(header_raw, adopted_image=adopted_image)
    member = member_journal(member_raw)
    count = header["member_count"]; C.uint(index, count-1)
    C.require(member["rank"] <= header["maximum_member_rank"], "AGGREGATE_MEMBER_RANK_BOUND")
    C.require(type(siblings) is list and len(siblings) <= MAX_SIBLINGS
              and all(type(item) is bytes and len(item) == 32 for item in siblings),
              "AGGREGATE_PATH_BOUND")
    depth, width = 0, count
    while width > 1: depth += 1; width = (width+1)//2
    C.require(len(siblings) == depth, "AGGREGATE_EXACT_PATH_LENGTH")
    digest, position, width = _leaf(count, index, member_raw), index, count
    for level, sibling in enumerate(siblings):
        if position % 2 == 0:
            if position+1 == width:
                C.require(sibling == digest, "AGGREGATE_ODD_PADDING_BINDING")
            digest = _node(count, level, digest, sibling)
        else:
            digest = _node(count, level, sibling, digest)
        position //= 2; width = (width+1)//2
    C.require(_root(count, digest).hex() == header["members_root"], "AGGREGATE_MEMBER_ROOT_BINDING")
    return member
