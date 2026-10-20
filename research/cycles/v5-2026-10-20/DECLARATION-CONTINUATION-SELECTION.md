# Complete acquisition under ordinary provider disappearance

Root selection, 2026-10-20. Full v5 remains active.

## Central capability and demonstrated obstacle

An agent must be able to obtain the declarations needed to use a discovered
result when one authorized supplier disappears. Current body acquisition has
an explicit settled, unsuccessful-attempt outcome; exact-name declaration
resolution still propagates transport failure through the client and semantic
reader failure transitions. The agent then loses its live context and cannot
choose another already authorized supplier within the same operation.

This is an actual incomplete acquisition protocol, not a new routing strategy.
The existing `prepare_mixed_seal` and production lifecycle already implement the
previously proposed frontier compiler; that duplicate task is cancelled.
Successful affordable frontier certification/renewal remains a distinct central
obligation. Do not imply this transport fix resolves it.

## Small intervention and invariants

Add optional one-attempt exact-declaration retrieval, reusing the body-attempt
transport classification, settlement, original contact and budget machinery.
Old fail-stop APIs retain their behavior. The caller explicitly chooses
whether to try another existing supplier; no retry loop or new owner is created.

Only positively settled, pre-validation availability failures are recoverable.
Malformed successful replies, invalid openings, wrong module/name, expired or
changed contacts, exhausted budgets, cancellation, unknown cleanup, failed
custody/readback and failed final source/liveness checks remain fatal.
Successful structural acquisition still supplies no mathematical authority.

On recoverable failure, retain the exact origin candidate, existing selected
members/groups/bodies, pending semantic demands and revision. Charge the
original grant/request/reply/step allowances. Do not install a candidate,
commit an opening or reset a deadline on refusal. On success validate the exact
requested module/name and its commitment before ordinary custody and exposure.

## Ownership

- `core_search`: implementation in fresh
  `software/v5/transport/declaration_resilience.py` and fresh logical overlays
  `software/v5/client/supplier_complete/{workspace_evidence,semantic_reader}.py`.
  Reuse existing body machinery. Do not edit used predecessors. Checkpoint
  `DECLARATION-CONTINUATION-IMPLEMENTATION.md`.
- `core_release`: focused independent controls in fresh
  `software/v5/client/supplier_complete/test_declaration.py`, after coordinating
  the API. No duplication of unchanged body tests; checkpoint
  `DECLARATION-CONTINUATION-CONTROLS.md`.
- `core_growth`: independent source/protocol review in
  `DECLARATION-CONTINUATION-REVIEW.md`. Check existing code and scope, especially
  whether shared helpers actually preserve the declaration protocol/accounting.
- Root: inspect integration and source map; select bounded tests, adopt results,
  maintain Git and decide the next central production/assurance step.

Canonical root and explicit workdir are mandatory. No native/guest/proof,
installation build, RAM investigation or old campaign rerun is selected.
Controls should be deterministic and small; a tiny genuine loopback exchange
is useful only for this changed failure boundary, with mathematical issuers
explicitly inert. Runtime selection follows source review. Stop after this
declaration boundary is complete; do not automatically enumerate additional
transport variants or create another framework.
