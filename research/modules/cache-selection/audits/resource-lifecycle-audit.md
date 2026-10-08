# CACHESEL1 resource and lifecycle audit

Date: 2026-09-20. Independent reviewer: `qualification_contract_review`. Scope: owner-local discretionary warm-cache selection, exact resource accounting and lifecycle handoffs. No implementation, native execution, extraction, executable model or benchmark. The separate qualification-readiness audit and all frozen H/I/J files remain unchanged.

Status: **two resource/lifecycle findings closed at the repaired held cut below; no remaining blocking contradiction found in this scope**. This record does not select CACHESEL1 or certify an implementation. Signal/usefulness review remains the separate reviewer's scope.

## Reviewed input and authority

Initial held [proposal](../proposal.md) SHA-256: `2DCBFA1A979F6321199826CE8A6D55EEFDCF64A82A975EDAE152FFABD4EAE28C`. The reviewer read the complete file and independently confirmed that hash. The module card was not a held selection authority for this review.

Repaired held proposal SHA-256: `1B3530AD271F1CCD106445D6A7CE941D5BD516E03C2CB9C5876751A9EF9C99BE`. The reviewer independently confirmed this hash and reread the complete repaired file, including the shared planning-phase repair from the signal review. The findings below retain the initial countercases rather than rewriting their history as though the guards were always present.

Inherited contracts inspected: [ORG1 root unions, P4 and finite cache terms](../../../../spec/OPERATIONAL-CORPUS-V1-ORGANIZATION.md), [NET1 warm clocks and generation-aware GC](../../../../spec/OPERATIONAL-CORPUS-V1-NETWORK.md), [V2 current-use and NET2 epoch separation](../../../../spec/OPERATIONAL-CORPUS-V2.md), [E custody ownership/release](../../../../notes/analyses/CP-001E-custody-contract.md), and [H shared coverage/anchor retention](../../../../notes/analyses/CP-001H-resource-supply-and-discovery.md). These supply the rules; this audit does not reopen them or require a proof of optimal cache selection.

## Findings sent before final review

| Finding | Minimal countercase and consequence | Required repair | Status |
|---|---|---|---|
| **CS-LIFE-001 — expired row versus fresh first-term authority** | A term T expires and settles; its family row remains enrolled. A later separately paid round sees no current term and can mistake the row for an uncommitted first-term candidate. The proposal requires fresh explicit nomination after expiry but does not identify the retained state/guard that distinguishes these cases. A paid round is not itself that fresh nomination. | Bind explicit first-term nomination eligibility to durable local state and require it at planning/commit; consume it on a successful or uncertain admission as specified. Retain enough terminal/fence state to prevent an expired row, old request or replay from silently rearming it. Use existing local request/recovery authority, not a new callback or network operation. | Closed at repaired cut `1B3530AD…`; inspected exact token, claim, terminal/fence and commit guards below. |
| **CS-LIFE-002 — renewal headroom and nonvacuity** | Sixteen active family terms occupy all sixteen active/reserved allocation slots. A future renewal is counted separately before the old expiry, so it cannot fit; old terms remain charged while settling. Final interval fit alone supplies no overlap slot. The original numerical examples exercise first admission, not successful renewal. | State the full-sixteen refusal and give a finite successful renewal trace with actual slot, metadata, payload, transition and settlement headroom. Keep the ceiling if sufficient; disclose the condition rather than claim unconditional renewal or presume a larger limit. | Closed at repaired cut `1B3530AD…`; explicit successful and defeating traces checked below. This was scope/operability-evidence precision, not a demonstrated safety contradiction. |

Root coordinated these with the independent signal review into one repaired author cut. Closure is based on rereading that cut, not on the request for a repair or the author's report alone.

## Initial-cut checks not requiring a new mechanism

- Exact marginal cache union is recomputed after each proposed winner and again at commit; zero marginal payload still carries root/handle/metadata costs. The shared-set arithmetic is correct: foundation 2 plus A/B residual union 9 gives 11, while all three candidates occupy 19 payload units. The declared separate control unit and staging supply remain premises, not measurements.
- Cache-term fit and actual physical transition fit are distinct. All mandatory owners, old live terms, staged/reserved/retiring generations and future reservations stay charged as applicable. The old-eight/new-six/limit-ten countercase correctly defers rather than deleting the incumbent to make replacement fit.
- Durable custody, seed ownership, active use/export pins, snapshots and publication anchors are not release candidates. Expiry removes only the selected term handle through the inherited paid transition; shared bytes can remain wholly protected elsewhere. No receipt or selection score establishes preservation or public native eligibility.
- Generation-aware GC is preserved: a claimed deletion generation cannot be used as zero-cost dedup merely because its bytes still exist. Unclaimed cancellation or a separately staged checked generation needs the inherited authority, and overlap remains charged until actual reclamation.
- Due renewal decisions are claimed before planning, including decisions that produce no committed winner; interruption leaves them fenced. This is conservative and can decline renewal even for useful families. It is not a guarantee of an attempt for every row at every later round, nor permission to omit those failures from evaluation.
- Every first-term commit recomputes its actual interval and both fits against earlier commits and existing/future obligations. A stale plan or late renewal stops rather than replanning for free. Cost/fit inspection exhaustion is explicit nondecision.
- Clean admission-epoch sealing preserves the original warm deadline and does not refill interval spending. Retention-clock continuity loss invalidates old warm authority conservatively while preserving durable accounting/protection obligations. Required fences cannot be evicted as optional history.
- Signals create neither jobs nor grants. Every invocation, expiry transition, settlement, acquisition, native recheck, GC step or other maintenance operation still needs its own applicable admitted local work. The selector itself does not fetch, publish or invoke a foreign tool.

These are source-level composition checks, not runtime tests. The initial cut did not receive final documentary closure; the following repairs supply that closure at the new exact bytes.

## Repair verification

### CS-LIFE-001: no implicit first-term rearming

An explicit admitted nomination now arms `(rowEnrollmentSerial, nominationGeneration, exactP4BundleVersion)` with recorded `ARMED`, `CLAIMED(roundID)`, `TERMINAL(outcome)` or `FENCED_UNKNOWN` state. This is not inferred from root availability or the absence of a cache handle. A distinct request while ARMED does not produce another token or silently change its bundle. Requests during live terms cannot prearm post-expiry first-term admission or reset renewal.

The atomic CLAIM phase binds every included token and due renewal decision before eligibility/selection. Failed prerequisites, nonwinners and interrupted attempts do not restore ARMED. COMMIT requires the exact row/enrollment/nomination-or-renewal claim, P4 binding, clock/current guards and both actual fits. Uncertain commits retain their original identity and reservations while reconciliation resolves them; another round cannot create a second term from that token.

After the old term expires, absence of its handle leaves the prior token terminal, not ARMED. Fresh explicit paid nomination can advance its checked generation only after the relevant live/reserved/unsettled term and claim obligations settle. Nomination replay returns its previous result. Row deletion cannot erase required replay/consumption fences, and an unresolved nomination or decision prevents row replacement. Thus the minimal stale-row trace cannot reach a new first-term commit under the repaired guard. This conclusion remains conditional on the inherited durable writer/ledger assumptions, not on mere in-memory state labels.

### CS-LIFE-002: timed headroom is explicit

For the successful invented trace, the payload arithmetic is `2 + 3 + 14 = 19`. Fifteen current term allocations plus one future reservation give exactly sixteen; control stock is at most `2 + 0.2 = 2.2 <= 3`. T's unchanged bundle adds no new payload, but it still consumes a separate term slot and control allocation. Its renewal commits thirty minutes before the old expiry and starts at that fixed expiry, not at the earlier decision time.

The stated seven other admissions on each of days 5 and 6 are compatible with the four-round/64-nomination daily ceilings: three rounds of at most three positive-use winners suffice (`3 + 3 + 1`). Nomination batches must be supplied as needed; arming all seven before the first round would spend the nonwinners' tokens and would require fresh paid nominations for later attempts. Either permitted schedule must count those attempts. The paper fixture supplies finite grants and positive histories rather than claiming a measured acquisition/checking/selector latency.

At the displayed cohort boundaries, the active payload unions are nineteen, then twelve after seven other terms end, then five after the remaining seven end. This does not authorize an immediate physical-stock refund. The source explicitly permits unreclaimed payload to remain within the original nineteen-unit physical ceiling, and the expired T handle keeps its slot/control charges until its actual paid settlement. The future interval is already committed; its beginning does not create a callback, new grant or deadline extension.

For the defeating trace, the added family makes `2 + 3 + 15 = 20` payload units and sixteen existing term allocations. Supplied payload/control capacity can make that old state valid but cannot change the separate slot ceiling. Renewal would create allocation seventeen and must fail despite zero added payload. Its once-only decision is consumed, the incumbent remains protected until the original deadline, and no later periodic round can implicitly rearm it. This is an explicit finite-stock limitation, not evidence that sixteen occupants can all renew continuously or that a larger slot limit is required by mathematical safety.

### Planning repair and commit-time seam

The repaired source reserves bounded finalization/outcome/fence/recovery capacity before round admission. It distinguishes a completed candidate-local unknown-fit/capacity skip from exhaustion or interruption before the prescribed planning passes finish. `PLAN_INCOMPLETE` discards all proposals, commits no terms and spends the already claimed decisions. Only completed planning may enter COMMIT; recovery does not resume an unfinished term-commit program.

This is compatible with the lifecycle repairs. Completed planning still does not reserve permission to ignore a later stale version, changed physical state, elapsed warm deadline or future reservation. Each actual first-term commit recomputes its shifted interval from its real commit time against earlier commits and all existing/future terms. Failure can leave a visible partial commit of already valid terms, not a hidden automatic replan. No completion, usefulness or fairness guarantee follows from conservative claim consumption.

## Final scoped disposition

The resource/lifecycle proposal is coherent at repaired hash `1B3530AD271F1CCD106445D6A7CE941D5BD516E03C2CB9C5876751A9EF9C99BE`; CS-LIFE-001 and CS-LIFE-002 are closed there. Initial and repaired findings concern this owner-local optional policy, not a revision of V6, native truth, durable custody or H routing authority. The separate signal reviewer owns signal-quality/selection-order closure.

Actual physical sizes, full-closure inspection costs, generation-aware store operations, crash recovery, sustained renewal success and useful cache effects remain unqualified. The tiny numeric cases are conditional arithmetic, not Lean measurements. Selection cannot establish globally meaningful novelty or causal utility, and refusal/expiration cannot establish mathematical falsity. Any later source edit needs an affected-cut review; this audit does not automatically transfer to changed nomination, term, resource or recovery semantics.
