"""Canonical witness emission and retained-export recovery; NEVER admission.

Frontend order respects Lean declaration dependencies. Relation order is the
unchanged Rust BTreeMap order of (owner module bytes, group index), then local
spec order. They are intentionally different. Only the final native relation
checks the emitted mathematical extension.
"""
from copy import deepcopy

from authoring.source import NATIVE_NAME_LIMITS
from modules import codec as C
from modules.native_rows import NativeRows
from modules.source_rows import decode_source
from .packet import Envelope, parse_packet


def emit_relation_rows(foundation_bytes, local, imports):
    C.require(type(foundation_bytes) is bytes and type(imports) is list,
              "DELTA_EMISSION_INPUT")
    keys = [(item["owner"], item["index"]) for item in imports]
    C.require(len(keys) == len(set(keys)), "DELTA_EMISSION_DUPLICATE_IMPORT")
    for owner, index in keys:
        C.digest_string(owner); C.uint(index, C.DEFAULT_LIMITS.max_groups)
    emitter = NativeRows(C.parse_json(foundation_bytes))
    for item in sorted(imports, key=lambda item: (item["owner"], item["index"])):
        emitter.group(local, item["owner"], item["group"], imported=True)
    for group in local.spec["groups"]:
        emitter.group(local, local.module, group, imported=False)
    return emitter.rows


def reprepare_retained_export(foundation_bytes, request_bytes, export_bytes, packet_bytes):
    """Recover untrusted producer bytes without another Lean/proving call.

This pure producer operation consumes NO saved acceptance flag or live handle.
It preserves all non-row witness fields and the complete predecessor packet.
Adoption still requires a fresh ordinary DeltaVerifier on its complete output.
"""
    request, exported = C.parse_json(request_bytes), C.parse_json(export_bytes)
    packet = C.parse_json(packet_bytes)
    parse_packet(packet_bytes, Envelope())
    C.require(request["schema"] == "DMKN_OWNER_LEAN_AUTHORING_REQUEST_V1"
              and exported["schema"] == "DMKN_OWNER_LEAN_AUTHORING_EXPORT_V1"
              and all(exported[k] == request[k] for k in ("source_sha256", "roots")),
              "DELTA_REPREPARE_EXPORT_BINDING")
    context = request["context"]
    C.require(context["selection_binding"] == exported["selection_binding"],
              "DELTA_REPREPARE_CONTEXT_BINDING")
    external = [{"source_name": C.relocated_name(item["owner"], d["name"]),
                 "module": item["owner"], "relative_name": d["name"]}
                for item in context["imports"] for d in item["group"]["declarations"]]
    local = decode_source(exported["rows"], exported["local_names"],
        context["foundation_view"]["names"], context["foundation"], context["policy"],
        external, NATIVE_NAME_LIMITS)
    target = packet["deltas"][-1]
    C.require(local.spec == target["local_spec"], "DELTA_REPREPARE_SAME_MATHEMATICS")
    C.validate_spec(local.spec)
    for body in target["bodies"]:
        C.require(local.supply_body(body["expression"], body["universes"]) == body["digest"],
                  "DELTA_REPREPARE_BODY_BINDING")
    expected = {}
    from admission.bindings import journal
    for parent in target["parents"]:
        owner = journal(bytes(parent["journal"]))["module"]
        for opening in parent["openings"]:
            key = owner, opening["index"]
            C.require(key not in expected, "DELTA_REPREPARE_DUPLICATE_OPENING")
            expected[key] = C.verify_group_opening(owner, opening)
    actual = {(item["owner"], item["index"]): item["group"] for item in context["imports"]}
    C.require(actual == expected and len(actual) == len(context["imports"]),
              "DELTA_REPREPARE_EXACT_SELECTED_GROUPS")
    result = deepcopy(packet)
    result["deltas"][-1]["rows"] = emit_relation_rows(foundation_bytes, local, context["imports"])
    raw = C.canonical(result)
    parse_packet(raw, Envelope())
    return raw
