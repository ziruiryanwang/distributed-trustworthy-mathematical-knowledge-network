# Fixed-foundation partial evaluation: source decision

2026-10-21; core_growth. Source/theory only; no build, import, test or proof.

## Decision

**Do not prioritize a new guest or kernel rewrite for this optimization.**
The foundation's mathematical checking is already skipped under its exact
adopted premise. There is no repeated 413-row foundation proof-checking term
to eliminate. Native reconstruction still repeats, but the safe small change
replaces row construction with state copying, not with free initialization.
Its actual net saving is unknown. Retain the contract below as a deferred
candidate, not a scalability solution or production-speedup claim.

## What already happens

The selected aggregate calls the bounded module relation separately per delta.
Each call compares every supplied foundation value with compiled static data,
performs correspondence, decodes rows and constructs a fresh native export.
The conditional checker then skips foundation and authenticated import names;
only local declarations enter `check_declar`. Foundation declarations remain
available for typing and reduction of those locals, which cannot be discarded.

`foundation_static` already avoids building an expected JSON foundation.
Typed rows retain the exact legacy prefix and still construct its native DAG.
Proof memoization is per owner/parameters/top-level syntax call, not a reusable
mathematical environment. Retained build recipes reuse compiled libraries,
not runtime checker state. None of those is a missing optimization to redo.

## Small safe refinement contract, if later selected

Let F be the exact fixed prefix, C the exact checker configuration, and
P_C(S,X) the parser state after applying rows X to state S. Define the seed
B = P_C(initial(C), F), **inside the executing relation using the old parser**.
For every suffix X, require:

`finish(P_C(exact_clone(B), X)) == finish(P_C(initial(C), F ++ X))`.

Equality means ordered DAG entries, declaration records and indices, notation,
mutual-block metadata, skipped declarations, configuration and refusal behavior;
hash-table allocation addresses need not agree. Keep each module's full syntax
census, exact F comparison, correspondence, parent bindings/ranks, local checking
and genuine guest assumption verification unchanged. No prefix inferred from
a sender label, cache hit, digest alone or previous successful dynamic import.

A parser-state clone is locally plausible without changing inference rules:
`Ptr` stores a DAG tag and integer index, not an arena address. The seed owns
six DAG collections plus ordered declarations, notation and block metadata;
strings must be owned or immutable with valid lifetime. Shared `Arc` parameter
arrays are immutable. Preserve collection order and all indices/hash-consing
semantics. Do not copy typechecker temporaries or syntax memo entries.

Build B once per aggregate; give every delta a fresh clone of B. Never seed
the next delta from the previous delta's completed export. That would retain
unrelated dynamic imports/locals and can change collisions, visibility and
demands. Existing checking borrows its export immutably and makes temporary
DAGs/caches per declaration. Keep that isolation and ordinary finalization.

This is a new internal parser entry point, not an existing API. Source review
and changed-boundary equivalence/refusal controls would still be required.
The selected guest image changes; old receipts/capsules cannot be relabeled.

## Exact cost boundary and why it is deferred

For d deltas, let D_F be prefix native decoding, P_F parser application and
K_F a complete seed clone. These are not measured values. The proposed change
replaces `d(D_F + P_F)` with `(D_F + P_F) + d K_F`, up to fixed setup work.
It leaves JSON frame parsing, exact equality, correspondence, finalization,
conditional-role scanning and every local kernel inference/reduction intact.
K_F is still linear in stored foundation state; there is no all-cost O(1)
foundation initialization. A one-delta invocation has no reuse advantage.
No evidence identifies this residual fixed-prefix term as a dominant cost.

Hand-generated native tables could avoid row interpretation but introduce an
additional parser-to-table refinement obligation and still require compatible
runtime maps. A raw native memory image is not a portable certificate. A truly
zero-copy prefix/overlay would alter DAG lookup/hash-consing and declaration
index/cutoff invariants across the checker: **NO-GO as a small optimization**.

Prefer the already reviewed typed decoder if a consequential producer decision
later warrants one matched guest evaluation. Mirror03's completed ordinary
loop changes ordering, not this unmeasured cost argument. No new campaign or
numerical speedup follows from this note; no frozen source was modified.

## Essential source anchors

- `software/v5/bounded_parse/module_relation.rs:45,115-118`: exact prefix and native construction.
- `software/v5/bounded_parse/aggregate_relation.rs:188`: independent per-delta relation call.
- `software/v5/modules/native/checker/src/module.rs:111,160-176`: conditional skips and local checks.
- `software/v5/modules/native/checker/src/parser.rs:40,484-550,650`: parser state/application/finalization.
- `software/v5/modules/native/checker/src/util.rs:42,203,251,269,683`: indexed ownership and fresh checking contexts.
- `software/v5/modules/native/checker/src/env.rs:239-320`: declaration cutoff and dynamic demand semantics.
- `software/v5/modules/native/proof_memo/module_correspondence.rs:117,138`: memo scope and full inventory.
- `software/v5/typed_rows/module_relation.rs:50,120-124`; `typed_rows/foundation_static.rs:43`.
- `TYPED-PRODUCER-NEXT-DECISION.md`; `COLD-CERTIFICATION-ROUTES.md`; `software/v5/proof_memo_guest/recipes.py`.
