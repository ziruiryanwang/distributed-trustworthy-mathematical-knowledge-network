# Explicit aggregate producer resource profile: source implementation

Status: **SOURCE READY FOR INDEPENDENT DELTA REVIEW; NOT EXECUTED**.
Authority: root's `PRODUCER-RESOURCE-PROFILE.md`, read completely before edits.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Owner: `memo_tests_review`; independent delta reviewer: `v5_growth_decision`.
Independent focused-controls author: `memo_independent_review`.

## Exact fresh sources

| New file | Bytes | SHA256 |
|---|---:|---|
| `software/v5/aggregate_resources/producer.py` |44,720|`1d191bdc2079760ce89a57a08924254f01487d24726e10b386c7eca1ef9eec09`|
| `software/v5/aggregate_resources/__init__.py` |152|`0ca27c691b5afe5ad93086251afb3259491f2ebcaf6e2a9b7ff7b209d4489bb2`|

The predecessor `aggregate_production/producer.py` remains44,253 bytes and
SHA256 `796eb24619370a30192db6d0f63b914516919e7cae90aee32a1750736331b86b`.
Its package marker remains byte-identical to the new marker. Both old and new
files use LF; no line-ending normalization occurred. Source creation and edits
used `apply_patch` only. No old source or used evidence was edited.

## Complete delta

A data-only exact full-text comparison reconstructed the new44,720-byte source
from the retained44,253-byte predecessor by **four unique replacement hunks**
and found exact equality. No source was imported, compiled or executed.

1. Profile docstring names explicit `stage_memory_ceiling_mib`.
2. Constructor exact-field set adds that mandatory field and requires
   `DMKN_V5_AGGREGATE_PRODUCER_PROFILE_V2`. Before constructing the retained
   support loader, `uint(profile["stage_memory_ceiling_mib"], 8192, 1)` rejects
   missing/extra fields, zero, negative, excessive, float and boolean values
   through the existing exact-type/field helpers. V1 is not auto-converted.
3. Immediately after obtaining the adopted supervisor, require that
   `self._A.CEILINGS["memory_mib"]` is an exact built-in integer and is at least
   the selected profile ceiling. Missing or malformed supervisor capability
   fails closed. A profile cannot confer capability the adopted helper lacks.
4. In the existing per-kind request-limit loop, only the `memory_mib` maximum
   uses that explicit profile field. Every other maximum still comes from the
   unchanged retained `P.COMMON`; stage CPU/wall and all other checks are intact.

The source-selection contract makes the profile an owner decision. A configured
ceiling is an upper bound, **not** a default request, memory reservation,
availability assertion or proof that a particular stage fits.

## Preserved invariants

- The whole canonical profile already supplies `self._raw` and `profile_id`;
  the new field is therefore included without a side identity scheme.
- Live `_check` compares the full current profile with `self._raw` exactly.
- Same-allowance history still requires exact profile identity, session,
  budget, carried costs and complete supplied predecessor sequence. This is
  the existing owner-scoped accounting contract, not a global allowance registry.
- The two new actual source paths are checked through the unchanged
  `Path(__file__).resolve().parent / SOURCE_NAMES` rule; no path alias is used.
- `production.producer.COMMON` and every legacy module remain unchanged.
- Graph/order, stage argv, retained capsule/image, cryptographic/native checks,
  receipt/checkpoint formats, request/attempt versions, CPU/wall/process/output/
  input limits, first-failure stopping and closure accounting are unchanged.
- No fixture-specific hash, universal memory estimator, SDK correction,
  geometry change, implicit fallback or automatic retry was added.

## Qualification boundary and next action

This establishes only a minimal auditable source successor. Independent review
must compare the actual bytes to the retained predecessor; focused controls
cover just explicit profile and request memory policy, profile mutation/identity
and incompatible history. Do not repeat the ten unchanged aggregate controls.
The controls' construction/adoption substitutes must be disclosed; a synthetic
control cannot establish genuine build adoption or a mathematically valid receipt.

No imports, tests, build, native execution, proof, process polling or Git changes
were performed by this author. Root retains exact-selection, execution and
adoption authority. Real production remains unfunded pending an actually
provisioned finite resource decision; no v5 acceptance claim follows.
