"""Pure translation boundary checks; synthetic claims, not checked mathematics."""
from pathlib import Path
import copy
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ordinary_evidence as E
import ordinary_semantics as S
import portable_evidence as P
import legacy_identity_translation as T


def name(text):
    return [[0, {"$bytes": list(text.encode())}]]


def ensure(ok, message):
    if not ok:
        raise AssertionError(message)


def refuse(marker, call):
    try:
        call()
    except ValueError as error:
        ensure(marker in str(error), "WRONG_REFUSAL:" + str(error))
    else:
        raise AssertionError("MISSING_REFUSAL:" + marker)


def claim(label, profile, bindings, previous=None):
    own, nat = name(label), name("Nat")
    typ = [E.EXPR_FORMAT, [], [[2, nat, []]], 0]
    value = [E.EXPR_FORMAT, [], [[7, {"$bytes": []}]] if previous is None else [[2, previous, []]], 0]
    unit = [E.UNIT_FORMAT, [0, own, [], typ, value, [2, 1], [own]],
            [[own, 1, [], typ, [value, [2, 1], [own]]]]]
    census = E.inspect_unit(unit)
    imports = [[E.strict_json(key), bindings[key]] for key in census.external_names]
    return E.canonical_json({"schema": E.SCHEMA, "profile_id": profile, "imports": imports, "unit": unit})


def main():
    profile, basis = "a" * 64, "b" * 64
    names = [name("Nat")] + [name("Basis" + str(i)) for i in range(580)]
    old, new = T.basis_pairs(profile, basis, names)
    nat = E.name_key(name("Nat"))
    ensure(old[nat] == E.basis_symbol_id(profile, basis, name("Nat")) and
           new[nat] == S.basis_symbol_id(S.semantic_id(), S.foundation_id(), name("Nat")), "EXACT_BASIS_PAIRS")
    refuse("BASIS_COUNT", lambda: T.basis_pairs(profile, basis, names[:-1]))
    refuse("BASIS_DUPLICATE", lambda: T.basis_pairs(profile, basis, names[:-1] + [names[0]]))
    raw = claim("First", profile, old)
    saved_old, saved_new = dict(old), dict(new)
    translated = T.translate_unit(raw, profile, old, new)
    ensure(old == saved_old and new == saved_new, "TRANSLATOR_MUTATED_PREFIX")
    original = E.read_evidence(raw)
    portable = P.read_evidence(translated.raw)
    ensure(E.canonical_json(original.document["unit"]) == E.canonical_json(portable.document["unit"])
           and original.unit_id == translated.legacy_unit_id and portable.unit_id == translated.portable_unit_id,
           "UNIT_BYTES_OR_IDENTITIES_CHANGED")
    for rows, mapping in ((translated.legacy_outputs_raw, old), (translated.portable_outputs_raw, new)):
        for nm, symbol in E.strict_json(rows):
            mapping[E.name_key(nm)] = symbol
    child_raw = claim("Second", profile, old, name("First"))
    refuse("UNMAPPED_OR_CHANGED_IMPORT", lambda: T.translate_unit(child_raw, profile, saved_old, saved_new))
    child = T.translate_unit(child_raw, profile, old, new)
    child_doc = P.read_evidence(child.raw).document
    ensure(dict((E.name_key(n), s) for n, s in child_doc["imports"])[E.name_key(name("First"))]
           == new[E.name_key(name("First"))], "DEPENDENCY_ORDER_TRANSLATION")
    wrong = dict(old); wrong[nat] = "c" * 64
    refuse("UNMAPPED_OR_CHANGED_IMPORT", lambda: T.translate_unit(raw, profile, wrong, saved_new))
    refuse("UNMAPPED_OR_CHANGED_IMPORT", lambda: T.translate_unit(raw, profile, saved_old, {}))
    refuse("OUTPUT_OVERWRITE", lambda: T.translate_unit(raw, profile, old, new))
    refuse("TRANSLATION_PROFILE", lambda: T.translate_unit(raw, "d" * 64, saved_old, saved_new))
    # Complete raw-unit changes produce distinct V2 identity, never an alias.
    changed = copy.deepcopy(original.document)
    changed["unit"][1][4][2][0][1]["$bytes"] = [1]
    changed["unit"][2][0][4][0][2][0][1]["$bytes"] = [1]
    changed_translation = T.translate_unit(E.canonical_json(changed), profile, saved_old, saved_new)
    ensure(changed_translation.portable_unit_id != translated.portable_unit_id and
           changed_translation.unchanged_unit_sha256 != translated.unchanged_unit_sha256,
           "CHANGED_DECLARATION_ALIASED")
    print("LEGACY_TRANSLATION_ALL_PASS basis exact_bytes ordered_imports no_mutation refusal_boundaries changed_content", flush=True)


if __name__ == "__main__":
    main()
