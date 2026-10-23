# Pure legacy-to-portable identity translation: independent review

2026-10-23. `admission_event_audit`. Source-only assignment following the
successful seven-unit reciprocal admission. No test, compiler, native worker,
catalog operation or Git command is run by this review.

**No blocking finding for the pure helper and its focused controls.** This is
not approval of a completed migration/importer, portable native snapshots,
cross-platform checker conformance or public release.

## Exact read cut

Paths are under `software/v5/ordinary_lean`.

| File | SHA-256 |
|---|---|
| `legacy_identity_translation.py` | `59c8f3549e775e5922902b0e6d9b2fcedfd2d3c10ab0f052b191c6906c09eb3f` |
| `legacy_translation_checks.py` | `5c5f1ed95653ebcd9d651a2f2e1beff8e164b86b436ea87edd0e7400be6bd9fa` |
| Referenced `portable_evidence.py` | `f8ea819bdd9344d696cef2725888828125b2ef5d1b60d2c31a0412657a62cbd8` |
| Referenced `ordinary_semantics.py` | `ee601536f53640a2695e51d37d3e87e6746604ed6433cb3ace9349ae1aedf915` |

All four files were read completely. Existing ordinary evidence/name/unit/DAG
validation was inspected at the invoked seams; baseline tests were not repeated.

## What the helper actually guarantees

`translate_unit` parses exact canonical V1 evidence under bounded existing
grammar and requires its profile to equal the caller's chosen legacy profile.
For each complete direct reference, the V1 ID must equal the supplied legacy
prefix, and a valid paired portable ID must exist in the portable prefix. It
replaces only those import IDs and the envelope schema/profile labeling, using
the selected semantic descriptor S. The complete raw declaration unit and its
syntactic census are compared for equality after V2 reparse.

Both V1 and V2 output IDs derive from their respective exact evidence domains
and original names. Outputs cannot overwrite either prefix. The function does
not mutate its arguments or install provisional outputs. The returned outputs
are canonical bytes, not mutable name/ID rows; hashes bind the original evidence
and unchanged unit. They are inert translation claims, not admission tokens.

`basis_pairs` validates profile/basis ID shape and exactly 581 unique valid
names. It derives paired IDs using the selected S/foundation descriptor. Its
documentation correctly makes **no** claim that cardinality proves membership
in the real fixed foundation. A caller must supply that authenticated inventory.

## Conditional semantic argument for the later importer

Suppose a separately justified importer establishes that the old and portable
prefixes denote the same checked declarations under the same formal semantics.
For a complete accepted V1 unit U whose reference IDs match the old prefix,
the helper preserves U and replaces each external ID with its paired meaning.
Thus U's interpretation is unchanged, conditional on that prefix relation and
the old checker's correspondence to S. The output pairing extends that relation
inductively in dependency order.

The helper does **not** establish the induction's premises. In particular:

- A supplied map or hash does not prove acceptance or meaning equality.
- A valid semantic descriptor does not prove checker conformance.
- A 581-name list does not prove the actual fixed foundation was constructed.
- Translation does not authenticate the old local store, accepted lineage,
  retained evidence order, artifact identity or real checking events.
- Returned V2 IDs do not authorize loading any native artifact or committing a
  new catalog. The future importer must establish its whole eligible lineage
  and atomically activate only its complete validated local materialization.

These obligations match the code's explicit authority separation. No hidden
mathematical trust follows from the pure translation's success.

## Focused control-source review

The controls use synthetic maps and syntax, not warranted mathematics. The fake
basis deliberately contains Nat plus 580 invented distinct names, illustrating
why count/shape success is not foundation acceptance. Unit fixtures use valid
JSON arrays, root-last single-node DAGs and matching descriptor/inventory
bodies. The literal change from zero to one changes both copies of the body.
Expected refusal markers reach the intended translation gates, rather than an
earlier malformed-fixture branch.

Coverage includes exact basis ID formulas, count/duplicate refusal, raw-unit
and unit-ID consistency, successful prefix nonmutation, an ordered two-unit
dependency, missing/wrong prefix imports, output overwrite, wrong profile and
changed-content nonaliasing. The source itself has no map mutations on refusal;
the explicit nonmutation assertion in these controls is on the successful first
translation. No control invokes catalog/native/migration code. Root may select
one bounded pure execution; this source review makes no runtime claim.
