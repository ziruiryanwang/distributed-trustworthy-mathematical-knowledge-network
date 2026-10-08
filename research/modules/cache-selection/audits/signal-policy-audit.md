# CACHESEL1 independent signal and policy audit

Date: 2026-09-20. Reviewer: `commons_decentralization`, independently of the proposal author. Status: **CS-SIG-001 closed at the repaired exact cut below; no remaining blocking signal-policy finding within this scope**. No implementation, native execution, executable model, measurement or benchmark was performed. This audit owns only this new file and does not amend the proposal or frozen H/I/J contracts.

## Exact scope and evidence

Initially reviewed [proposal](../proposal.md) SHA-256 `2DCBFA1A979F6321199826CE8A6D55EEFDCF64A82A975EDAE152FFABD4EAE28C`, confirmed by a read-only file hash before complete reading. Then verified and reread the complete repaired source at SHA-256 `1B3530AD271F1CCD106445D6A7CE941D5BD516E03C2CB9C5876751A9EF9C99BE`. Earlier draft orientation and messages are not review coverage of another cut. The finding below preserves its original-cut diagnosis; the final section records the actual repair and rereview.

Inherited boundaries read:

- [ORG1 ingress, exploration, P4 and retention](../../../../spec/OPERATIONAL-CORPUS-V1-ORGANIZATION.md#ingress-duplicate-floods-and-valid-but-low-demand-output), especially lines 179–269: bounded receiver admission, exact-judgment proof families, finite warm terms and once-per-term renewal decisions.
- [C popularity/exploration and censoring](../../../../notes/analyses/CP-001C-growth-analysis.md#popularity-can-erase-future-value), plus [local utility](../../../../notes/analyses/CP-001C-reciprocity-analysis.md#local-utility-without-a-universal-utility-function): observed reuse is not causal benefit, absence of recorded use is censored, and finite exploration does not protect every future valuable object.
- [E custody](../../../../notes/analyses/CP-001E-custody-contract.md#selected-boundary): owner-release-required durable ownership is distinct from a discretionary warm-cache handle.
- [H preservation distinctions](../../../../notes/analyses/CP-001H-proof-computation-and-reconstruction.md#preservation-and-qualification-conditions): same-judgment evidence need not preserve a consumer's original conversion/application.

Review scope is signal identity, duplicate versus genuine repeated use, cross-judgment grouping/P4 composition, aging and term signals, exploration and finite heuristic claims. Exact physical union/transition accounting, GC, authority lifecycle and recovery composition have a separate reviewer; this note inspects those seams only where they affect the stated policy decision. It does not independently certify the entire inherited ledger, kernel or network.

## Initial finding CS-SIG-001: planning exhaustion leaves the proposed prefix undecided

Severity: blocking **policy-determinacy clarification** for this concept cut; not an exhibited mathematical-soundness failure or a claim that every possible resolution is unsafe.

The bounded-invocation section stops a round at its supplied work limits and distinguishes incomplete fit as `UNKNOWN_FIT`. Exact candidate choice says to make the four passes without committing while planning. The commitment section separately permits a committed prefix when later commits stop. What is not explicit is whether an already proposed, fully checked-fit prefix may enter commitment after the unfinished planning phase exhausts its work.

Minimal paper trace:

1. Two actionable families are present; any due renewal decisions are already reserved to this round under the stated once-only rule.
2. The exploration pass finds completely feasible A and records it as a proposed winner; no cache handle has been committed.
3. A later candidate-fit inspection exhausts the round's shared work limit before the remaining comparisons finish. B's fit is unknown, not disproved.
4. One reading discards the inert proposed A and produces no new term; another reading commits the already proposed A using separately reserved finalization/commit resources and reports a partial result. The source does not choose between these operationally different outcomes.

The distinction affects actual term selection, use of reserved resources, once-only renewal outcomes and interpretation of the returned status. A total score order among completely known feasible candidates does not settle it. `NO_FEASIBLE_CANDIDATE` must not silently turn an incomplete inspection into a complete absence-of-fit observation.

Required repair: specify the planning-to-commit boundary and the disposition of proposals, due-decision claims, consumed work and result status on interrupted/exhausted planning. One sufficient resolution is no new cache commits before completed planning, with proposals discarded/inert and due decisions finalized or fenced; interruptions after commit phase begins may preserve actually committed prefixes under the existing guards. Another explicit bounded policy is possible, but it must state its authority and resource conditions rather than infer them from a proposed winner.

Root coordinated this finding with the independent lifecycle findings for one author repair. No algorithm was coauthored or source text edited by this reviewer. Closure applies only to the repaired cut identified below.

## Signal and heuristic countercases at the initial cut

These are source-backed paper inspections, not executed tests. Their closure is scoped to the named cut and assumes the inherited local writer, exact checking and resource-enforcement contracts.

| Check | Minimal case and observed specification response | Review disposition |
|---|---|---|
| Duplicate delivery is not another use | Re-deliver a completed application or its callback after its original once-only commit. Its completion serial is unchanged; callbacks cannot append observations. Atomic credit/cursor advancement prevents applying an existing queued record twice. | No signal amplification permitted by the stated transitions. The ledger implementation remains unqualified. |
| Genuine repeated/self-generated use | Perform nine genuinely distinct cheap checked applications of one family across the three bins. Those applications can fill all bins and yield `4*3 + 2*3 + 3 = 21`. | This is allowed finite inflation, not detected unique demand. The source explicitly permits redundant premises and supplies a defeating usefulness case. No identity/novelty oracle is required. |
| No use credit from weaker events | Supply a remote use claim, repeated hint, download, import/check or failed application. | None satisfies successful owner-local checked application settlement. Observer work must be separately reserved; missing observer resources lose the signal rather than repeat the application. |
| One application, several witnesses | One application uses multiple proof/replay alternatives of the same exact judgment, or repeats that input syntactically. | At most one family credit per application, at most four distinct enrolled judgments total. P4 alternatives are not separate cross-judgment score entries. Canonical truncation can bias which inputs receive credit; no causal-importance claim is made. |
| Queue overflow and enrollment churn | Drop an unconsumed observation, evict its family row, then re-enroll the same JudgmentID before replaying an old observation. | Global consumed/dropped boundaries survive eviction, and the new row's lower boundary is the current completion serial. Old queued history cannot give the re-entered row fresh credits; lost signal stays lost. |
| Aging is not receipt-time refresh | Delay a completion observation, roll the service epoch, or lose the retention-clock origin. | Bins use completion time in one qualified generation. Older bins age out; clean rollover does not reset fences/deadlines. Clock loss discards old-generation signals and expires old warm validity; uncertain authority history requires reconciliation. |
| Ranking does not bypass renewal authority | Re-nominate a live family repeatedly, or retry a failed due-term decision. | Existing-row nomination preserves age/boundary/deadlines. Due decisions are reserved before planning, prior reservations exclude another try, and failed/stopped decisions remain consumed or fenced. CS-SIG-001 concerns the still-ambiguous uncommitted-prefix disposition, not a stated permission to retry for free. |
| Same judgment is not same operational use | A demand observation concerns R-old, while later P4 chooses R-new for the same judgment. | The source expressly denies preservation of the caller's realization, conversion, footprint or exact-replay hits from the score. Future application checking remains separate. A score can remain useful as a heuristic without proving the replacement useful. |
| Exploration and nominal reuse lanes | Several actionable families all have `u=0`; alternatively, the exploration lane is empty/infeasible. | Only the first slot is restricted to zero history. The three “reuse” passes consider all remaining actionable families, so they may also select zero-history families, receiving probation terms. The unused exploration slot is not a fourth reuse slot. This is not a three-positive-score quota. |
| Rare or delayed value | A potentially valuable abstraction is outside the 64-row window, loses its observation, is too large, or arrives under sustained nomination churn. | It can miss selection or disappear from discretionary warmth. Source claims only a conditional retained-window opportunity, not universal topic fairness, permanence or mathematical inferiority of discarded objects. |
| Custody is not a popularity cache | A low-scoring root shares evidence with durable custody, a seed, another cache owner or an active use/export. | Nonselection supplies no release authority for those other protections. This is consistent with E; detailed lawful physical transitions belong to the lifecycle audit. |

## Boundedness and value claims

The declared signal state is finite: 64 rows, three saturating bins per row, 64 queued observations, bounded exact family/evidence bindings, persistent cursors and checked nonwrapping counters. Optional history loss cannot erase the accounting/fencing state. Actual metadata and observer work remain charged under supplied allocations; naming those bounds does not demonstrate a memory fit or an implementation.

The ranking arithmetic is bounded by 21 because each bin is at most three. There are at most four proposed families per round, four rounds and 64 nominations per admitted interval, subject to smaller aggregate limits. These are bounds on opportunities, not a scheduler, throughput guarantee or free allowance after a policy hash/clock change. Physical feasibility and all transition costs remain independent obligations.

The A/B/C examples make the appropriate limited claims. Shared A/B residual payload is nine units, eleven including the stated two-unit foundation. C-first uses ten including the foundation, and adding A or B would require eighteen, exceeding eleven. Increasing C's recorded use to 21 can therefore defeat the prospective A/B opportunity despite preserving the resource limits. This establishes a counterexample to frequency as a usefulness oracle, not measured cache performance or actual future task yield.

Zero credits mean no retained credited observation, not zero demand. The source retains the C evaluation boundary: cohorts, exposure, availability, deletion/missingness and horizon matter. No positive net-benefit, independent-user, novelty, exact-replay-hit preservation, global fairness or durable-survival claim is established by selection.

## Repaired-cut rereview and disposition

The complete source at `1B3530AD271F1CCD106445D6A7CE941D5BD516E03C2CB9C5876751A9EF9C99BE` was reread, including the new one-shot nomination and timed-capacity passages. The following are paper transition checks, not executed tests.

| Recheck | Repaired contract and consequence |
|---|---|
| Earlier proposed A, unfinished later planning | Explicit phases are OBSERVE, CLAIM, PLAN, COMMIT and FINALIZE. Aggregate work/deadline exhaustion or interruption before completed planning gives `PLAN_INCOMPLETE`, discards every inert proposal and creates no new term. A's previously known fit cannot bypass this boundary. **CS-SIG-001 closed.** |
| Finalization and due-decision consumption | Finalization/outcome/fence/recovery capacity is reserved before round admission from the same parent account. Claimed first-term and renewal decisions end terminal/spent; uncertainty stays fenced. A hard failure cannot resume the incomplete round's commits. Neither a stopped plan nor a later round restores the old claim. |
| Candidate-local unknown versus exhausted round | An explicitly unavailable/incomplete inventory can be a completed `UNKNOWN_FIT` skip while work remains; global exhaustion instead stops the plan. A completed pass may have no confirmed feasible winner while containing such skips. Its candidate diagnostics do not prove those unknown inventories infeasible; `NO_FEASIBLE_CANDIDATE` is not a universal absence-of-fit certificate. |
| Partial committed prefix | Only PLAN_COMPLETE enters COMMIT. After entry, each term still needs its actual claim/version/native/time/resource checks. If later commits stop, earlier actually committed terms can remain; uncertain commits remain fenced. This is no longer confused with preserving a merely proposed prefix. |
| New first-term token versus use/metadata refresh | A successful explicit nomination arms one exact enrollment/nomination-generation/P4-version token. Same-request replay cannot duplicate it, a distinct request while armed cannot add another, and use signals/row presence/expiry/metadata refresh do not rearm it. A post-terminal explicit paid nomination preserves age, observation cutoff/history and cumulative spending. This creates no new credit or automatic retry channel. |
| P4 changes and group-level credit | New token/version checks add admission precision without changing the one-credit-per-event-family rule. The exact old-witness caveat remains explicit. The preexisting grouping, saturation and censoring limits are not replaced by stronger utility claims. |
| Retained-window exploration | CLAIM can consume a first-term opportunity even for a later nonwinner or failed prerequisite. Such a family needs a fresh explicit nomination to attempt another first term. The conditional exploration wording therefore cannot mean automatic repeated visits to every retained row; the source's one-shot eligibility and no-universal-fairness boundary remain controlling. |
| Timed renewal and finite headroom | The new example explicitly distinguishes fifteen existing terms plus one reserved future term from sixteen existing terms requiring an impermissible seventeenth. Refusal spends the old term's renewal decision; zero marginal payload does not create a slot or automatic later first-term authority. This supports the signal/term boundary; the separate lifecycle audit owns complete physical-fit validation. |

The repaired source adds conditional invariants, not measured benefits. Its original duplicate/self-use counterexample, 21-point bound, zero-history reuse-pass behavior, censored-observation interpretation and no-custody-release boundary remain intact on reread.

**Disposition:** no remaining blocking signal-policy contradiction identified at the repaired cut within this audit's stated scope. The initial finding is closed by an explicit operational policy choice, not by weakening a mathematical soundness rule. Separate lifecycle review and root's integration decision remain distinct. This result does not select CACHESEL1, qualify software execution or cover later source changes; a changed substantive signal/admission/phase contract requires a targeted new review.
