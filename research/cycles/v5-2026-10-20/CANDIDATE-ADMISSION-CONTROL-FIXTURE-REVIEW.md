# Candidate-admission controls: fixture cross-review

2026-10-22. Reviewer: storage_outcome_audit. Source-only review; no imports,
compilation, controls, verifier, proof or installation run was performed.

Disposition: **no remaining fixture blocker found for the six selected controls**.
This is a review of the harness against its stated contracts, not an executed
pass or independent review of the lower implementation authored by this reviewer.
Product review and actual-outcome adoption remain separate.

## Exact reviewed boundary

- `software/v5/candidate_admission/controls.py`: 32,700 bytes,
  SHA-256 `61e49ac2130e6f5e5368ec6465e06306dbb6128997638274a5d96d7e4502cb71`.
- Selected facade: `candidate_admission/client/workspace_evidence.py`,
  SHA-256 `e81407b9296d14a3f3f2f1a1c8554efa2747829fa6a2639fc29215c7ed29cb44`.
- Lower helper/I/A implementations are the three exact source pins recorded in
  `CANDIDATE-ADMISSION-OWNERS.md`; the harness stages them rather than importing
  an arbitrary installed predecessor.
- Base map129 is `distribution-exact-packet-01-input.json` / `328c21bb...`.
  Its 129 physical sources plus six overlays and runner/control are 137 selected
  snapshots; six logical replacements/additions produce 130 logical modules.
  The helper is the sole new logical key. Frozen offer custody is an overlay,
  not another selected edit.

## Findings fixed before execution

1. After the product reviewer required post-census final liveness guards, the
   facade fixture supplied grant timing fields but omitted `_origin_owners`.
   The real final guard would raise `AttributeError` on the normal trial path.
   Root added an explicitly doubled four-slot owner tuple and issuer deadlines
   bounded by the original grant. Both sync and async controls now also expire
   an original issuer after census, in addition to authority, grant deadline
   and controller-CPU cases: eight final-boundary denials in total.
2. `_staged` identity alone could not detect an in-place mutation because the
   comparison fixture aliased the same dict. Root added a separate dict snapshot
   and equality checks after refusal and the I/A positive/cache paths. Values in
   this fixture are immutable tuples/bytes, so the shallow snapshot is sufficient.

Both corrections were read in the final pinned harness. No product change or
new test campaign was made by this review.

## Contract checks

The clean report fixture has exactly the helper's 19 fields, a seven-field final
Job observation, exact call binding, strictly typed exit1 and closure flags,
matching final/last observations, consistent CPU sum, empty stdout and bounded
stderr. Missing/extra/error fields, resource/type/closure failures are selected
refusals. Cumulative process count5 is correctly permitted when final active0;
it is not confused with the simultaneous-process cap.

Output checks use the operation root containing `command/stdout.txt` and
`command/stderr.txt`, not the command directory. The real pinned supervisor's
ordinary-path/read/save helpers are used. Byte/entry limits, log-size mismatch
and active-guard propagation are exercised without changing the inspected files.

The I/A fixtures execute real `try_receive`, `_receive`, helper and revocation
method bodies on explicitly constructed owners. Their selected limits satisfy
the real validators; header and journal construction use the real codec/bindings.
Clean refusal preserves existing registries and consumes `[1,3,1]` attempt,
receipt-byte and CPU reservations. A also retains its explicit output reservation.
Exit2, stdout, CPU overrun, changed input, changed trust, late refusal evidence I/O
and A header mutation take fatal paths. Strict APIs retain their predecessor
distinction: strict A revokes; strict I raises and leaves enclosing-client closure
unchanged. Neither gains a clean `None` result.

The facade controls use real terminal-I encoding/inspection, exact-journal checks,
A membership binding, trial dispatch, positive cache logic and public decorators.
NOT_ADMITTED issues no warrant/cache entry; later positive reuse avoids another
issuer call/reservation. A commitment corruption precedes issuer invocation.
The new final wrapper fixtures contain its required fields and use mutations
during census, not artificial elapsed waiting, to reach the final checks.

## Required scope disclosure

The supervisor's worker execution and lower-owner constructor/trust checks are
doubles. The fake supervisor creates real logs but does not launch a child.
Facade issuers, warrants, stores, acquisition and failure recording are doubles;
positive handles are inert, not cryptographic acceptance. Mixed unsupported-form
dispatch uses an explicit inspection double, not a valid mixed packet. Public
async controls test argument/decorator dispatch, not HTTP or custody transfer.
Lower fatal registry clearing is real method behavior; facade `_fail` is only
recorded by a double, not a real workspace shutdown.

Consequently these controls can establish selected structural/control behavior
only when actually run and audited. They cannot establish genuine receipt
acceptance, real supervisor cleanup/trust withdrawal, network operation, useful
growth, hostile-code isolation, or final-v5 readiness. The harness reports those
limitations and zero actual cryptographic/native/proof work explicitly.
