"""Pure V1-to-portable identifier translation, NEVER import/admission authority.

The future owner-local importer must separately authenticate the complete
accepted lineage, retained ordered evidence, fixed foundation and checker-to-S
correspondence. This helper neither loads native artifacts nor opens catalogs.
It preserves complete raw declaration units and resolves every import through
both supplied prefixes. Returned claims remain inert until that importer meets
all its actual-local-lineage and atomic-activation obligations.
"""
from dataclasses import dataclass
import hashlib

import ordinary_evidence as E
import ordinary_semantics as S
import portable_evidence as P


@dataclass(frozen=True)
class Translation:
    raw: bytes
    legacy_unit_id: str
    portable_unit_id: str
    legacy_evidence_sha256: str
    unchanged_unit_sha256: str
    # Canonical bytes, not caller-mutable decoded rows. No map is modified.
    legacy_outputs_raw: bytes
    portable_outputs_raw: bytes
    nodes: int


def translate_unit(raw, profile_id, legacy_bindings, portable_bindings, *, limits=E.DEFAULT_LIMITS):
    """Translate one unit relative to exact name→ID prefixes, in dependency order.

    Equality of each old ID and existence of its paired portable ID are checked.
    This does not prove that the caller's maps pair equal mathematical meanings.
    That inductive premise comes from the selected eligible lineage importer.
    No partial mapping escapes or input-map mutation occurs on any refusal.
    """
    profile_id = E._hex(profile_id)
    E._need(type(legacy_bindings) is dict and type(portable_bindings) is dict,
            "TRANSLATION_PREFIX_MAPS")
    old = E.read_evidence(raw, limits)
    E._need(old.document["profile_id"] == profile_id, "TRANSLATION_PROFILE")
    imports = []
    for name, identity in old.document["imports"]:
        key = E.name_key(name, limits)
        E._need(legacy_bindings.get(key) == identity and key in portable_bindings,
                "TRANSLATION_UNMAPPED_OR_CHANGED_IMPORT")
        imports.append([name, E._hex(portable_bindings[key])])
    semantic = S.semantic_id()
    unit_raw = E.canonical_json(old.document["unit"])
    new_raw = E.canonical_json({"schema": P.SCHEMA, "semantic_id": semantic,
                               "imports": imports, "unit": old.document["unit"]})
    new = P.read_evidence(new_raw, limits)
    E._need(E.canonical_json(new.document["unit"]) == unit_raw and new.census == old.census,
            "TRANSLATION_RAW_UNIT_CHANGED")
    old_outputs, new_outputs = [], []
    for row in old.document["unit"][2]:
        name = row[0]
        key = E.name_key(name, limits)
        E._need(key not in legacy_bindings and key not in portable_bindings,
                "TRANSLATION_OUTPUT_OVERWRITE")
        old_outputs.append([name, E.export_id(profile_id, old.unit_id, name, limits)])
        new_outputs.append([name, P.export_id(semantic, new.unit_id, name, limits)])
    return Translation(new_raw, old.unit_id, new.unit_id, hashlib.sha256(raw).hexdigest(),
        hashlib.sha256(unit_raw).hexdigest(), E.canonical_json(old_outputs),
        E.canonical_json(new_outputs), old.census.total_nodes)


def basis_pairs(profile_id, legacy_basis_id, fixed_names):
    """Derive paired basis claims from a caller-authenticated exact inventory.

    The required census is checked; the names' actual membership and foundation
    construction are NOT established by their count. No basis check is skipped
    merely because this pure function returns successfully.
    """
    E._hex(profile_id); E._hex(legacy_basis_id)
    E._need(type(fixed_names) in (tuple, list) and len(fixed_names) == 581,
            "TRANSLATION_FIXED_BASIS_COUNT")
    ordered = sorted((E.name_key(name), name) for name in fixed_names)
    E._need(len({key for key, _ in ordered}) == 581, "TRANSLATION_FIXED_BASIS_DUPLICATE")
    semantic, foundation = S.semantic_id(), S.foundation_id()
    old, new = {}, {}
    for key, name in ordered:
        old[key] = E.basis_symbol_id(profile_id, legacy_basis_id, name)
        new[key] = P.basis_symbol_id(semantic, foundation, name)
    return old, new
