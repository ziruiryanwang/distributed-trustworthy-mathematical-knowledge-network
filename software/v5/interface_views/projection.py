"""Untrusted Lean-request projection; never an authenticated module opening.

Only the frontend sees these surrogate descriptors. The caller must retain the
original sealed context for final relation emission and exact parent warrants.
This helper provides neither mathematical admission nor a semantic equivalence
claim. A missing transparent value can still be demanded by the final checker.
"""

from modules import codec as C
from authoring.context import SCHEMA as CONTEXT_SCHEMA


def project_frontend_context(original_context):
    """Return a bounded fresh READY context and an inert projection census.

    Ordinary missing definition values may be hidden only in the explicitly
    selected interface-only mode. Present values, types, identities, universes,
    commitments and inductive/recursor declarations are not changed. The copy
    is proposal data, not suitable for validating an authenticated opening.
    """
    C.require(type(original_context) is dict
              and original_context.get("status") == "UNTRUSTED_AUTHORING_CONTEXT_READY"
              and original_context.get("mathematical_acceptance") is False,
              "MIXED_FRONTEND_PROJECTION_READY")
    # Serialization bounds the helper's data and makes an independent plain-data
    # copy. There is no source evaluation, filesystem access or live callback.
    projected = C.parse_json(C.canonical(original_context))
    packet = projected.get("packet")
    C.require(type(packet) is dict and packet.get("schema") == CONTEXT_SCHEMA
              and packet.get("mathematical_acceptance") is False,
              "MIXED_FRONTEND_PROJECTION_PACKET")
    mode = packet.get("definition_mode", "eager")
    C.require(type(mode) is str and mode in ("eager", "interface-only"),
              "MIXED_AUTHORING_DEFINITION_MODE")
    C.require(packet.get("selection_binding") == projected.get("selection_binding"),
              "MIXED_FRONTEND_PROJECTION_BINDING")
    count = 0
    if mode == "interface-only":
        imports = packet.get("imports")
        C.require(type(imports) is list and len(imports) <= 256,
                  "MIXED_FRONTEND_PROJECTION_IMPORTS")
        for item in imports:
            C.fields(item, {"owner", "index", "group", "bodies"})
            group = item["group"]
            C.validate_group(group)
            C.require(type(item["bodies"]) is list, "MIXED_FRONTEND_PROJECTION_BODIES")
            present = set()
            for value in item["bodies"]:
                C.fields(value, {"universes", "digest", "expression"})
                present.add((C.uint(value["universes"], C.DEFAULT_LIMITS.max_universes),
                             C.digest_string(value["digest"])))
            if group["kind"] != "ordinary":
                continue
            descriptor = group["declarations"][0]
            if (descriptor["kind"] == "definition"
                    and (descriptor["universes"], descriptor["value_hash"]) not in present):
                # Existing Lean frontend handles imported opaque declarations as
                # rigid axioms. This is only a candidate-construction view: the
                # original definition/hash/hints remain in the sealed context.
                descriptor["kind"] = "opaque"
                descriptor["meta"] = {"safety": "safe"}
                count += 1
    return projected, {
        "schema": "mixed-frontend-interface-projection-v1",
        "definition_mode": mode,
        "projected_definitions": count,
        "mathematical_acceptance": False,
        "final_witness_uses_original_descriptors": True,
    }
