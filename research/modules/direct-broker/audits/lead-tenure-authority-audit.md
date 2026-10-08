# TENURE1 authority, interface and state audit

Date: 2026-09-20. Reviewer: `bounded_domains_author`. Read-only source review; this audit is the reviewer's sole writable path. The reviewer contributed the preceding read-only preflight and reviewed the root-authored synthesis; this is an independent review of root's candidate, not a blind originating analysis. No source edits, implementation, executable model, Lean execution or benchmark occurred.

## Initial reviewed cut and finding history

Read the entire [TENURE1 candidate](../lead-tenure-policy.md), including its scope, all operation/lifecycle cases, the formal bound, resource obligations and positive/defeating traces:

- 33,508 bytes; 182 lines.
- SHA-256 `EC4162A1B9933D28BA3E0CCE0685525D978071F45FDDB50054908CAEBC98DA13`.
- Status at this cut: root-authored, NOT SELECTED.

Independently verified the entire source's byte count, line count and hash before review. Also verified the inherited [I interface](../../../../notes/analyses/CP-001I-direct-broker-bindings.md) hash `2CE9222631ED95AE0CE7B31C875AA4CD72EA5D0440B7BC1A8E34FB84D7F2EFB2`, matching the candidate's stated dependency. That interface was read completely during preflight. Relevant BROKER1 owner/disclosure clauses and the NET1/NET2 clock, admission-seal and recovery distinctions were cross-checked separately.

**Initial disposition: one blocking proof-premise precision issue, TEN-AUTH-001, was open on this cut.** No additional concrete authority, no-op, CAS, snapshot or incarnation defect was found. The root author and resource reviewer were notified promptly; the resource reviewer independently identified the same calendar boundary issue. The historical diagnosis below applies to this initial cut. The complete replacement-source review and closure are recorded at the end; the policy remains unselected.

## TEN-AUTH-001 — successful-calendar boundary coverage is underspecified

Location: candidate T-BOUND at lines 109–117, coupled to episode/calendar admission and local status.

The proof takes the first successful round starting at or after a due time e and states that it starts by e+h. Bounded gaps **between** successful starts do not establish that statement for the first start of a finite calendar, and do not supply a next start near its end. The phrase "includes enough rounds through e+Delta" does not define the missing initial/terminal coverage. Treating it as an assumption that the required removals already finish by the claimed bound would make the argument circular rather than state the operational service premise.

A minimal diagnostic schedule has M=r=1, h=w=1 and e=1, hence Delta=2 and claimed removal by 3. Let the finite calendar contain one successful scan starting at 2.5, with its guarded decision completing at 3.5. Pairwise successful-start gaps are vacuously bounded; its one slot is inspected and decided within w; one required round starts before e+Delta=3. Nevertheless the first post-due start is later than e+h=2, and the claimed completion bound does not follow. If "through" was meant to exclude this schedule, its exact temporal meaning must be stated rather than inferred.

Recommended repair, agreed in coordination with root: for each admitted still-current due time e, specify actual finite calendar coverage with a first successful start s1 in [e,e+h] and C=ceil(M/r) successive successful rounds beginning there, with adjacent starts at most h apart and each round's guarded slot decisions completed within w of its own start. Admission must reserve/check these finite windows, including the initial and terminal boundaries; missing or failed required coverage withdraws the bound. A case where the target is removed earlier already satisfies the residence conclusion and need not force pointless further scanning after complete drain.

This is a scheduling/service assumption, not an assumption of the removal result. Given it, the independent derivation is sC <= e+C*h, followed by completion <= e+C*h+w. Stable-slot traversal and the guarded due-removal rule supply the removal implication. The finite example's particular calendar does satisfy the needed boundary service; the issue is the general theorem's missing explicit premise, not the supplied example's arithmetic.

No source edit was made by this reviewer. The initial closure requirement was a complete repaired-source read with its new exact hash and rechecking of the surrounding admission, drain and status language, not merely agreement with this proposed wording. That requirement is discharged by the final record below.

## State and authority composition checked

| Seam | Checked result at this cut |
|---|---|
| Managed-state invariant | Row/map/slot/reservations share one writer; all selected collection leads are managed, with no aliasing parallel writer. Absent leads have no current slot |
| Endpoint churn and fencing | Endpoints can change without changing incarnation/a/e. Due cleanup removes the current variant by incarnation, not an obsolete LeadDigest. A stale reference cannot remove a replacement; a subsequently prepared decision concerning that replacement must pass its own current due test |
| Source versus owner authority | Self mutation remains self-only. Due retirement is separately funded owner selection, not a fifth submitter's eviction power. Owner insertions use the same installation constraints |
| No-op and replay | ALREADY_LISTED cannot renew, enroll or perform cleanup, including while due. Exact replay returns the historical outcome only. Neither acknowledgment promises current listing at delivery |
| Wire ABA | Delayed distinct same-value op22 and expected-absent op21 retain I's allowed behavior. T-FENCE applies only to local cleanup; it does not revise wire CAS or promise lasting source exclusion |
| Adoption and continuation | Complete-cut preparation is serialized or abandoned on change. ADOPT age is activation-relative; repeated adoption cannot reset tracked tenure. Failed continuity invokes recovery, not now+tau |
| Cursor and concurrency | Fixed slots do not move behind the frontier. Empty/future/stale cases count; only completed guarded decisions advance the durable cursor. Interrupted work remains charged. One scan job avoids M queued timers |
| Cutoff and drain | No fresh installs after A; endpoint updates cannot use protected removal reserves. Empty state before A does not abandon future scan coverage. H does not delete aftercare obligations |
| Clock and restart | Clean admission sealing preserves qualified deadlines and spending, with pauses counted. Uncertain continuity fences work and suspends disclosure; funded authorized retirement replaces rebasing. Hidden rows are not free/deleted |
| Revocation | Selection revocation fences unclaimed/prepared removals and degrades the residence promise. Reserved resources do not override authority. Disclosure revocation remains a separate I event |
| Historical retention | Last-lead removal atomically retires current row/postings, not every version/outcome. Authorized historical snapshots remain historical; T-BOUND excludes their visibility, native custody and later incarnations |

These results are conditional on the inherited writer, storage, current authority and admission premises. Compatible continuation cannot bypass current correspondence/clock/authority checks; the specified alternative is suspension and reconciliation, not an implicit re-enrollment.

## Trace check and evidence limits

Independently checked the supplied calendar: M=8, r=4, c0=4, h=4, w=2 gives C=2 and Delta=10. Starts 4,8,...,396 give 99 planned rounds/396 reserved inspections. The 100-round visits slots 4..7; the 104-round visits incumbent slots 0..3 and can finish by106. X at110 occupies slot0 with due210; the 216-round can remove it by218, within220. These are stipulated scheduling calculations, not measured primitive or native performance.

The positive path separately assumes X's fresh successful admission, a new reader view and funded native acquisition/check/use. Its unchanged-row comparison is confined to the declared contact graph. Healthy sole-source loss, no re-entry, competitive recapture, historical pages, synchronized bursts and clock/authority failures remain real countercases. Vacancy is neither queued admission nor fairness.

T-SAFE, T-AGE and the locally scoped T-FENCE have adequate conditional paper arguments at the initial cut. T-OPPORTUNITY is a sufficient composition path, not an autonomous scheduling theorem. T-BOUND required the repair reviewed below. All six native/eight reciprocal execution gates remain NOT RUN; the optional policy remains UNSELECTED. No default-rate optimality, net benefit, sustained reciprocal growth or implementation correctness is certified. Changed wire outcomes, authority, adoption/incarnation, cursor/calendar, clock, disclosure or shared retention/accounting reopens affected review.

## Complete replacement-source review and final disposition

Independently verified and read the **entire** replacement: 35,648 bytes, 184 lines, SHA-256 `79DA034872C011A8387AA8080BCEF79BF8992973898C6AE96C7CEB0DC7B381CE`. This was not a changed-paragraph-only review. The operation table, adoption, cursor, authority/clock recovery, aftercare, countertraces and evidence limitations were reconsidered together with the repaired calendar proof and added scaling warning.

**TEN-AUTH-001: CLOSED at the replacement cut.** Episode admission now explicitly checks/reserves the initial post-due start and the finite C-round coverage window. T-BOUND separately requires those rounds actually succeed; a reservation is not runtime evidence. With s1 in [e,e+h] and adjacent starts at most h apart, sC <= e+C*h and final guarded decision <= e+C*h+w. The fixed-slot scan then supplies the removal result. Completed advances in an intervening partial round cannot pass a still-current due installation without its guarded removal; interrupted decisions do not advance. Earlier actual removal already satisfying the conclusion or authorized complete drain need not fabricate later scan executions. The original counter-schedule fails the repaired first-start premise. Admission, cutoff/drain and degraded-status treatment remain consistent with this conditional claim.

Independently checked the new, explicitly **uniform-periodic full-accounting-interval** exclusion: M/r=262144/32=8192; even with relaxed w=0, Delta<=3600 requires h<=3600/8192=0.439453125. Over [0,86400), a first start at h gives the conservative minimum ceil(86400/h)-1>=196607 starts, already exceeding the shared 20000 count before other work. Positive w cannot weaken this exclusion. The source correctly excludes conclusions about arbitrary targeted due-window calendars, actual deletion-delay lower bounds, other policies or decentralized network scale. The small hypothetical trace remains unchanged and does not justify this maximum-table periodic default.

**Final scoped disposition: no remaining blocking authority/interface/state/proof-composition finding at the exact replacement cut.** This clears the reviewed conditional paper policy in this audit's scope; it does not select the policy, set a default, certify implementation or supply any native/reciprocal execution evidence. Reviewer role remains preflight-informed. Only this assigned audit path was edited. Audit edits stop at final handoff pending a new bounded assignment.
