# Independent atomic-control source review

Disposition: **PASS_SOURCE_FOR_FINITE_SELECTION**, not an executed result.
Reviewer: `/root/memo_tests_review`, 2026-10-16. Root owns selection/runtime.

Scope: root-authored `mixed_claims/test_atomic.py`,
`client/atomic_control_owner.py` and the successor API seams those tests call.
This is test correctness/coverage review, not a duplicate security review of
the product. No test, project-code import, native call or Git operation ran;
no product/test file was edited.

## Reviewed identities

All source paths below are under `software/v5/`.

| Source | SHA-256 |
|---|---|
| `mixed_claims/test_atomic.py` | `d3109ad0518dad6b9b6f393200e972cbf8a2b01938fff437e2138cca49ba5928` |
| `client/atomic_control_owner.py` | `af7f1391ee38ec2026189356372c8c31b965bfa1953f5cf2b6734b661cca1244` |
| `mixed_claims/imports_atomic.py` | `8d5e77ea1a239c10bd745a2860080d4ea6c91e52f4da32c7f18562ca755c0ba8` |
| `mixed_claims/authoring_atomic.py` | `22c2e758ce487f77e22f465ed5191f64928a423af4ea63efefed7a8888b086fe` |
| `client/workspace_atomic.py` | `01eefed1804ec5f296aebfcc12441dd283cd77c9bac8f8d5b02e8a4becc5e8c1` |

## Findings and resolution

1. **Missing batch-byte charge, repaired before execution.** The initially read
   `materialize` omitted `_charge(batch_bytes)`. The malformed-second-record
   test correctly demanded the charged bytes; the submitted-budget test also
   exposed this omission. It was reported promptly, not worked around in tests.
   The reviewed successor now charges bounded built-in batch bytes before parsing.
2. **Legacy imports masked a cold product path, repaired and controlled.** The
   initial required-origin list included old `mixed_claims.imports` although the
   new product path did not import it. `OLD_A`, `OLD_I` and `test_imports` made it
   appear loaded in the original controls. The unused origin requirement is now
   removed. `atomic_control_owner.main` first imports `workspace_atomic`, then
   constructs/closes an atomic session with an explicitly synthetic owner while
   old `mixed_claims.imports` is absent. Only afterward does it import the old
   comparison helpers and load the thirteen tests. Its small fake-owner helper
   imports aggregate/admission/codec modules already in the product closure;
   it does not import the old mixed session. This checks the selected cold route,
   not an installed genuine-owner construction.

No unresolved test-source blocker was found in the reviewed identities.

## Why the controls test the intended seam

- Fixtures have well-formed canonical declarations, summary/journal bindings,
  aggregate headers and member openings. The theorem/definition bodies are
  deliberately not checked Lean mathematics. Fake exact-class owners, receipt
  bytes, source-pin maps and foundation decoding are plainly disclosed; no
  generated fixture is called a genuine warrant or proof.
- The semantic comparator checks the exact READY packet and selection binding,
  then byte-identical onward packets and deterministic parsed-wire censuses.
  It does **not** demand equality of operational `cost.warrant_census` call or
  submitted-byte counters, which intentionally differ after batching. Packet
  census is deterministic wire accounting, not elapsed time or session counters.
- NEED remains extendable; supplying the missing committed definition body
  reaches READY. READY blocks public and internal semantic writers. Invalid
  second records cannot publish their valid first records, and incurred work
  remains observable after the session is closed.
- `copy(view)` and `deepcopy(view)` currently create distinct empty-slotted
  `SealedSelection` objects; the session identity check must reject them. There
  is no current copy reducer that throws before the test's assertion block.
  Foreign tokens, dictionaries and unrelated objects are separately rejected.
  Returned data is mutated by the test to verify detachment from sealed state.
- Source preparation is run with `_group` made fatal, so the sealed route cannot
  quietly reopen per-group authority checks. Group counts one and sixteen must
  yield equal, positive mocked installation-scan counts for materialization
  and preparation. This measures logical call multiplicity, **not CPU speedup**.
- The client tests make obsolete incremental methods fatal, observe one batch
  charge, require the exact sealed view passed into source-operation creation,
  and verify operation closure. Decorator bypass via `__wrapped__` is explicit:
  these are narrow method-plumbing tests, not grant/Job/client-lifecycle tests.
- The suite loader selects only `AtomicImportControls`; importing old helper
  definitions does not run their older suites. Exactly thirteen non-skipped
  successful tests are required, in addition to the preceding cold-route check.

## Bounded coverage and next gate

The data-cap control sets the raw batch bound to one byte; it exercises ingress
refusal, not every cumulative retained-data or context-work-limit combination.
The suite also does not execute native source elaboration, genuine receipts,
filesystem pin mutation, full client decorators or a real reciprocal loop.
These limitations are compatible with its stated changed-boundary scope; they
must not be silently promoted into installed/runtime/security qualification.

Root may now select one finite native-free run after binding this complete
source closure and its actual launch plan. Independent actual-outcome review
remains required. The real continuation must still use preserved actual03 seed
material and obtain fresh live authority; this review authorizes no such launch,
new proof, seed reauthoring or broad repeated campaign.

## Changed-boundary supplement before freeze

2026-10-16. Root strengthened two existing controls without changing the test
count or product source. Independent source-only reread finds no new blocker;
the disposition remains **PASS_SOURCE_FOR_FINITE_SELECTION**, not a run result.
The revised `mixed_claims/test_atomic.py` is 17,244 bytes, SHA-256
`7da4a44f43ff7b5710155c61107a2880f4537dd66cb86a447eb2598c5f3da754`.
`atomic_control_owner.py` and `imports_atomic.py` still match the table above.

- `CustomLimits.__iter__` now records invocation, and the control explicitly
  asserts the record remains empty. This distinguishes rejecting a non-exact
  limits container from accidentally evaluating its user-supplied iterator.
- The data-cap subcase now commits a valid four-group NEED batch with one
  missing definition body. It next supplies only that committed body, explicitly
  asserts the new batch is smaller than the already retained data, and sets
  the data cap equal to those retained bytes. Ingress therefore fits, while
  the nonempty new body violates `data_bytes + len(raw) <= cap` in
  `materialize`'s body loop. Refusal closes/clears the session rather than
  publishing staged additions. The earlier one-byte-ingress-only limitation
  is superseded: this now targets genuine cumulative retained-data refusal.

This remains a synthetic changed-boundary test, not complete coverage of all
context limits, actual runtime cost, native mathematics or full client
lifecycle. Exactly thirteen tests plus the cold-route gate remain selected
in source; no runtime was launched by this reviewer.
