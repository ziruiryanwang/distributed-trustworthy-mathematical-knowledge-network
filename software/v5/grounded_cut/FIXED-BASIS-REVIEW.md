# Independent fixed-basis reuse challenge

2026-10-24. SOURCE/THEORY ONLY; no code, experiment, state-database open or Git
mutation. Scope is the smallest useful successor, not a repeated whole-system
audit. Reviewed `FIXED-BASIS-PAYOFF.md`, including its final clarification delta:
`a7a46409ed7263d4ceb19d22e3e16b3e3aa2c04b0a1131e2162d1cc0be01ad98`.

## Decision

**GO in principle for an exact protected fixed-basis capability; defer metadata
check amortization. NO-GO for a public accelerator or speedup claim today.**
Native/batched admission and ordinary Lean authoring remain the default.
The two observed cut workers are not a matched comparison with the native batch.
No subtraction of basis timing from cut timing establishes measured savings.
Nevertheless, source establishes 456 repeated seed kernel additions per cut;
removing those through an existing restoration primitive is a focused investment.

## Soundness conditions for the smallest successor

Read anchors: complete `BasisSnapshot.lean` and `LocalSnapshot.lean`;
`OrdinaryWorkflowWorker.initializeBasis/extend`; `ordinary_admission.initialize`
and `_execute`; `portable_catalog._artifact/_validate_record/_context_rows/`
`_commit_checked`; `BootstrapSupport.inventoryRow`; current grounded cut
`check/census`, source-anchor capture/check and controller promotion boundaries.

`BasisSnapshot.checkAndWriteBasis` serializes actual records from `receiveSeed`,
not asserted inventory records. The committed native basis row binds the clean
live operation to its exact artifact. `LocalSnapshot.restoreLocal` supports the
one-module, zero-parent case; its exact-artifact map, empty search path and
disabled plugin/extensions avoid arbitrary discovery through module names.
It is still trusted native deserialization, not proof verification of peer bytes.

The successor must enforce all of the following:

1. During the already-paid locked native derivation, select the committed
   **basis** operation/root, not merely the selected extension's first filename.
   Authenticate its native origin, zero parent, basis request and exact support.
   Derive artifact length/hash from that validated record. Context plan rows
   alone omit the artifact digest and are insufficient to manufacture provenance.
2. Commit a protected descriptor binding source store, basis root/module,
   foundation, seed/inventory, implementation/support, ordinary path and bytes.
   The current source anchor lacks this artifact binding. A supplied hash,
   matching descriptor or saved success report cannot substitute for derivation.
3. Construct a singleton import plan internally: basis=root, parent absent,
   exactly 581 names. No caller-supplied module list, arbitrary snapshot path,
   extension root, peer `.olean` or full ancestral import route is accepted.
4. Authenticate exact artifact bytes before deserialization under the held
   source lock and immutable-file premise. Hash once at this event boundary,
   not inside every trie/budget callback. Preserve exact runtime/loader support,
   resource bounds, no concurrent replacement and clean child supervision.
5. Validate restored module/quotient state and the fixed names/inventory before
   using the environment; keep the existing full final census, concrete-record
   checking, grounded signatures, freshness, new-theorem check and atomic commit.
6. Use a distinct support identity and fresh bound cut state. Existing state,
   events and used bytes must not be reinterpreted under the new loading rule.
   Reopening/withdrawal remains tied to the original source support.

Conditional argument: genuine checked origin + immutable exact artifact + the
adopted serializer/deserializer correspondence recover the same fixed basis;
the previous cut induction then applies unchanged. `inventoryRow` includes
proof bodies and computational metadata but normalizes def/theorem/opaque
`all` to `[name]`. It is equality in that inventory representation, **not** an
injective encoding of every raw kernel-record field. Origin/correspondence cannot
be replaced by census equality. Census also cannot make unsafe deserialization
of previously unauthenticated bytes safe after the fact.

The receiver still reads fixed basis proof bodies. What disappears is repeated
kernel reconstruction of that fixed basis, not every proof read. No cost term
proportional to growing application ancestry is introduced by this singleton.

## Why not bundle metadata amortization now?

Repeated anchor identity/SQLite reads are source-visible, but parent timing was
intrusively profiled. Their ordinary cost is not yet established. Removing them
changes a separate observable validation/withdrawal cadence. Keep existing checks
in this first successor to isolate the high-confidence fixed kernel cost.

Later amortization is sound in principle only under lock-honoring serialized
mutation, immutable support, no rollback and explicit withdrawal semantics.
Cheap original-budget checks and sticky observed denial must remain at inner
checkpoints; full eligibility checks remain at open, launch, clean completion,
precommit and reopen/resolve. Cheap monotone withdrawal-marker sampling may stay
even if identity/SQLite checks are amortized. A marker written out of band after
the last check can race COMMIT; neither current nor proposed sampling proves
instantaneous revocation. Future use must revalidate. Do not weaken this policy
implicitly by treating an initial observation as permanently current.

## Payoff gate

The note's break-even inequality is conditional, not evidence that its bracket
is positive. Compare the successor against the existing matched cut route and
an equally optimized native/batched workflow; count initial capture, fixed hash/
load/census, selected semantics, controller/support, custody and failed work.
One small unprofiled changed-boundary discriminator can test uncertain constants
after source review; no broad benchmark or new creative episode is needed.
If the resulting useful region over ordinary reuse remains implausible, shelve
cuts. This improvement supports efficient continuation, not concept invention
or final-v5 completion by itself.
