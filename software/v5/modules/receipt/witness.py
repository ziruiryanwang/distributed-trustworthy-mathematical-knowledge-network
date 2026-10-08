"""Untrusted producer adapter for the new real relation input.

No receipt verification or mathematical admission occurs here. Parent journals
must later be supplied with real proof witnesses to the prover, and final
receiving must use the pinned cryptographic verifier. This adapter is also
usable for explicitly synthetic native diagnostic fixtures.
"""
from __future__ import annotations

from .. import codec as C, native_rows as N
from ..model import ConditionalEnvironment


def decode_journal(raw: bytes) -> dict:
    C.require(type(raw) is bytes and len(raw) == 184 and raw[:8] == b"DMKNM002"
              and int.from_bytes(raw[8:12], "little") == 2, "MODULE_JOURNAL_LAYOUT")
    value = {"image": [int.from_bytes(raw[i:i+4], "little") for i in range(12,44,4)],
             "foundation":raw[44:76].hex(), "policy":raw[76:108].hex(), "module":raw[108:140].hex(),
             "group_root":raw[140:172].hex(), "group_count":int.from_bytes(raw[172:176],"little"),
             "rank":int.from_bytes(raw[176:184],"little")}
    value["summary"] = {"schema":C.SUMMARY_SCHEMA, **{key:value[key] for key in
                         ("foundation","policy","group_count","group_root")}}
    C.require(C.summary_id(value["summary"]) == value["module"], "MODULE_JOURNAL_IDENTITY")
    return value


def make_input(environment: ConditionalEnvironment, foundation_rows: list[dict],
               image: list[int], parents: list[dict]) -> dict:
    """parents entries have journal (bytes) and exact selected group openings.

    The environment must already use the NEW semantic policy. This helper does
    not rewrite identifiers or reinterpret an old noncertified-policy module.
    """
    C.require(type(image) is list and len(image) == 8, "IMAGE_WORDS")
    for word in image: C.uint(word)
    C.require(C.module_id(environment.spec) == environment.module, "LOCAL_SPEC_IMMUTABILITY")
    seen, groups, encoded_parents, ranks = set(), {}, [], []
    for parent in parents:
        C.fields(parent, {"journal","openings"})
        parsed = decode_journal(parent["journal"])
        module = parsed["module"]
        C.require(module != environment.module and module not in seen
                  and parsed["image"] == image and parsed["foundation"] == environment.spec["foundation"]
                  and parsed["policy"] == environment.spec["policy"], "PARENT_COMPATIBILITY")
        C.require(type(parent["openings"]) is list and parent["openings"], "PARENT_NONEMPTY_OPENINGS")
        seen.add(module); ranks.append(parsed["rank"])
        for opening in parent["openings"]:
            group = C.verify_group_opening(module, opening)
            C.require(opening["summary"] == parsed["summary"], "PARENT_OPENING_SUMMARY")
            key = module, opening["index"]
            C.require(key not in groups, "DUPLICATE_PARENT_GROUP")
            groups[key] = C.canonical(group)
        encoded_parents.append({"journal":list(parent["journal"]), "openings":parent["openings"]})
    expected = {key:value for key,value in environment.groups.items() if key[0] != environment.module}
    C.require(groups == expected, "EXACT_PARENT_ENVIRONMENT_GROUPS")
    rank = max(ranks) + 1 if ranks else 0
    C.uint(rank, 2**64-1)
    emitted = N.emit_conditional(environment, foundation_rows)
    required = set()
    for encoded in environment.groups.values():
        for descriptor in C.parse_json(encoded)["declarations"]:
            arity, kind = descriptor["universes"], descriptor["kind"]
            if kind in ("definition","opaque"):
                key = arity, descriptor["value_hash"]
                if key in environment.bodies: required.add(key)
            elif kind == "recursor":
                required.update((arity,rule["value_hash"]) for rule in descriptor["meta"]["rules"])
    bodies = [{"universes":arity,"digest":digest,"expression":C.parse_json(environment.bodies[arity,digest])}
              for arity,digest in sorted(required)]
    # Local theorem proof stays inside native rows. It is NOT a committed
    # definition/rule opening and cannot be passed as an unused body entry.
    result = {"schema":"DMKN_CERTIFIED_MODULES_V2", "image":image, "rank":rank,
              "local_spec":environment.spec, "rows":emitted["rows"],
              "parents":encoded_parents, "bodies":bodies}
    return C.parse_json(C.canonical(result))
