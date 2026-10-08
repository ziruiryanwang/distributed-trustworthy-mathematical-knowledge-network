# TENURE1 resource and service audit

Date: 2026-09-20. Reviewer: `bounded_domains_resource`. Status: **complete initial and replacement whole-cut reviews; TEN-RES-001 CLOSED at the replacement cut below; no remaining blocking resource/service finding within scope**. Concept/specification and arithmetic only; no implementation, executable model, native extraction, Lean execution or benchmark.

## Exact cut and role

The reviewer independently verified [the held source](../lead-tenure-policy.md), then read all 182 lines: **33,508 bytes / SHA-256 `EC4162A1B9933D28BA3E0CCE0685525D978071F45FDDB50054908CAEBC98DA13`**. The [commissioning cycle](../../../cycles/2026-09-20-lead-tenure.md), live [WORK assignment](../../../registry/WORK.md), selected I profile and relevant preserved lifecycle/retry contracts were also inspected.

The single coordinated replacement was independently verified and read in its entirety, all 184 lines: **35,648 bytes / SHA-256 `79DA034872C011A8387AA8080BCEF79BF8992973898C6AE96C7CEB0DC7B381CE`**. The final verdict applies only to this replacement. The initial finding history below remains visible.

Root authored the source. This reviewer contributed resource/service preflight findings and now reviews that synthesis independently of authorship; this is not a fresh-blind third audit. Authority/interface coverage belongs to the separate [authority audit](lead-tenure-authority-audit.md). The reviewer owns only this audit; all predecessor sources and audits remain untouched.

Initial verdict: one shared calendar-premise defect blocks clearance of the general T-BOUND proof as written. The concrete 99-round calendar is arithmetically coherent. No other blocking resource/service defect was identified in the scoped conditional design. The source supplies certificate obligations and a hypothetical event trace, **not a fully numerical multi-owner resource fit or costed failed baseline**.

Final verdict: the replacement closes that defect, and its added uniformly periodic scaling exclusion is sound within its explicitly restricted recipe. No other blocking resource/service defect was found after complete reread. The evidence grade remains conditional concept reasoning, not numeric whole-owner qualification, policy selection or measured operability.

## TEN-RES-001: first post-due start and finite-tail coverage — CLOSED

The authority reviewer first flagged this shared issue; this reviewer independently checked it and supplied the following boundary countercase. Treat the two reviews as one underlying defect, not two unrelated findings.

In the initial source, T-BOUND assumes successful round-start gaps at most h and then infers that the first round starting at or after due time e starts by e+h. Adjacent-start gaps alone do not constrain activation-to-first-start or ensure enough rounds remain at the finite calendar end. “Enough rounds through e+Delta” does not precisely require the post-due window needed by the proof.

Take `M=r=1`, `h=w=1`, `a=0`, `tau=1`, so `e=1` and `Delta=2`. Let the sole successful round start at 2.5 and complete removal at 3.5 inside a maintenance horizon H=4. Its adjacent-start-gap premise is vacuous, and one round starts before `e+Delta=3`, yet the decision misses the claimed removal bound 3. All local resource and stable-clock premises can hold. A calendar with no post-due start exposes the terminal-edge problem even more directly.

Required repair: for each admitted due time e, explicitly reserve and require a first successful post-due start `s1 in [e,e+h]`, followed by `C=ceil(M/r)` successful consecutive covering rounds in total with successive starts at most h apart and every decision completed by its start+w. Alternatively supply explicit initial/terminal calendar coverage from which those facts follow. Admission must reserve that finite due-sweep window; missing/failed coverage withdraws the conditional bound. This does not require a new timer, resource grant or stronger native service promise.

Once supplied, the proof is straightforward: those C rounds inspect at least M consecutive fixed slots; a still-current incarnation cannot move its slot, and its visit either observes prior removal or removes it under the exact-incarnation guard. The last decision is at most `e+C*h+w`.

**Replacement disposition:** admission now reserves/checks the first start in `[e,e+h]` and C successive covering rounds; T-BOUND independently requires their actual successful service rather than inferring execution from a reservation. The initial countercase's 2.5 start is outside `[1,2]` and is excluded. The final proof derives `s_C <= e+C*h` and removal by `s_C+w` from fixed-slot traversal. It also handles earlier actual removal and committed partial-round advances: the cursor cannot advance past a still-current due incarnation without its guarded removal, and an interrupted decision never advances it. Finite-tail coverage, clock/authority continuity and actual work remain explicit premises. This closes TEN-RES-001; it is the same repaired issue recorded by the authority reviewer, not an additional independent defect.

## Independent arithmetic on the finite trace

| Quantity | Recomputed result and scope |
|---|---|
| Maximum possible lead-slot count from I | `4*65,536=262,144`; this is not a byte or service fit |
| Coverage rounds and lag | `ceil(8/4)=2`; `2*4+2=10` |
| Planned scan calendar | Starts 4 through 396 by 4: 99 jobs; `99*4=396` planned slot inspections; final completion by 398 |
| Adopted cohort | Due 100. Initial cursor 4 makes odd rounds inspect slots 4–7 and even rounds slots 0–3. Round 25 at 100 inspects empties; round 26 at 104 removes the four due leads by 106, within bound 110 |
| X installation | Commit at 110 selects least free slot 0; due `110+100=210`. Round 54 at 216 inspects that slot and completes by 218, within bound 220 |
| Cutoff admission margin | Even installation at A=120 has `120+100+10=230 <= H=400` under the supplied service calendar |
| Reader elapsed path after result | `114+40+200+10=364`, leaving 36 seconds before deadline 400 |
| Visible counted starts | 99 scans plus two X submission attempts plus two reader queries gives 103; adoption and all other separately admitted work remain additional |

The five actual lead removals, two last-lead unlistings and one X insertion follow from the stated unchanged one-row trace. Their transaction costs, retained versions and finalization are not obtained from these counts. Scan jobs contain their own internal inspection/removal work; separately counted mutation execution identities must be disjoint, as the source requires. No internal transaction is silently counted as both a new job and free work.

The source reserves all 99 rounds and 396 inspections even if authorized complete drain permits earlier stopping. It does not claim those savings. The interval after A closes installations is long enough for the trace's admitted due windows; H remains a service boundary, not a history-deletion time.

## Added uniform-periodic exclusion

The replacement explicitly restricts this argument to one applicable accounting interval `[0,86400)`, uniform successful spacing h throughout, first start in `[0,h]`, and no early drain or aborted coverage. For `M=262144,r=32`, independently recomputing gives `C=8192`. Certifying `Delta=C*h+w <= 3600` requires `h <= 3600/8192 = 0.439453125` even after optimistically relaxing w to zero.

Under those exact periodic premises, the half-open interval has at least `ceil(86400/h)-1 >= 196607` starts. First start h and exclusion of the right endpoint give the conservative boundary count when `86400/h=196608`; first start zero or counting the endpoint cannot reduce it. Positive w tightens the spacing constraint. Thus scan jobs alone exceed the candidate's shared 20000-per-interval execution allowance before queries, submissions, adoption and other work.

This is a genuine count exclusion for the declared full-interval certificate recipe under TENURE1's expressly chosen scan-job charging. It is not a measured CPU/byte limit, an unavoidable actual deletion latency, a rejection of targeted finite due-window schedules, or an impossibility result for other TENURE1 configurations, representations, local policies or decentralized network scale. A stricter optional local count convention is not relabeled a universal wire restriction.

## Resource and lifecycle conditions that remain premises

- **Actual owner budgets:** initial adoption enumerates the complete current cut, and every failed preparation, query, mutation, scan and recovery attempt consumes its actual grant. `Q+U+J+other` must fit the actual remaining execution allowance; the I maximum 20,000 does not prove residual capacity. CPU, I/O, traffic, resident stock and timing need separate certificates. The trace does not provide numeric values for those whole-owner certificates.
- **Bounded scanning:** the fixed slot array prevents insertion from moving an old target behind a dynamic cursor. Empty slots, non-due entries, revalidation and failed work are charged. Only actual completed inspections/guarded decisions advance the cursor. At most one tenure scan job is admitted, so M records are not M queued executions; I's pending-work and shared-concurrency ceilings still apply.
- **Synchronized adoption:** assigning a0 to all adopted leads can make M entries due together. Admission must reserve the entire accepted cohort's row/posting/version transitions and service. Mean rate N/tau or an r-per-job ceiling cannot establish a burst deadline. Failure to provide that work yields a charged nondecision, not fictional removal.
- **Current versus historical stock:** removal frees a current slot/map entry, not every physical allocation associated with it. Old snapshot roots, prepared replacements, stale job references, immutable outcomes, current/new versions and reconciliation coexist until actual release. Reuse of a slot therefore requires additional whole-node fit. Neither END nor nominal snapshot expiry proves every retained result has disappeared.
- **Standing authority and finite service:** the finite caller calendar is separately authorized; each occurrence consumes a finite job. Seals and competing work count in the promised service timing. No new episode name, restart, endpoint update or no-op renews tenure or funding. Aftercare may outlive H and remains allocated; optional work cannot consume it.
- **Clock/revocation:** unqualified clock or ledger continuity stops positive active-policy/progress claims. Recovery either establishes original deadlines or uses separately authorized/funded retirement, without inferring downtime. Revocation can withdraw removal authority despite prior resource reservation. Hidden/suspended rows are not deleted or free, and repeated incidents can defeat progress.

These conditions are concrete admission and proof obligations, not independently measured supplies. No additional measurement is demanded as a repair to this concept-only source.

## Useful service, failures and comparative limits

T-OPPORTUNITY correctly needs more than vacancy: X must actually win a subsequent funded admission, a reader must obtain an adequate fresh view early enough, and independently paid source/receiver work must meet the remaining deadline. The old snapshot at 98 does not learn X by continuation. Historical pages elsewhere can nevertheless retain a usable contact, so the no-X conclusion is restricted to the stipulated graph.

X's first failed submission and already paid public preparation do not disappear when its second attempt succeeds. Source custody, publication, uploads, scopes and aftercare have their own owners and guards. Readers separately pay failed trials, refresh, acquisition, native checking/application and settlement. Broker removal at 218 does not revoke an independently established native scope or delete accepted mathematics. The source explicitly declines to pay these native obligations by mere directory arithmetic.

Unchanged row selection rejects the same two X attempts and lacks an X edge for the stipulated reader. That is a causal reachability comparison, **not a completely charged unsuccessful execution or net-efficiency theorem**. Healthy sole-source disappearance, absent resubmission, competitive recapture, expired/retained historical views and clock/authority incidents remain admitted defeats. The inclusive-cut information limitation permits heuristic tradeoffs; it does not establish optimal tenure or universal availability impossibility.

## Handoff and evidence grade

TEN-RES-001 was the only requested repair and is closed after independent hash verification and complete reading of the coordinated replacement identified above. The whole replacement, including unchanged lifecycle/trace passages and the added count exclusion, was reviewed rather than only the changed paragraphs. No new resource/service finding arose. The source remains UNSELECTED; this audit does not certify the separate authority review by assertion.

Clearance establishes only the scoped conditional local current-incarnation argument and stipulated discovery opportunity. It cannot select TENURE1, prove source-admission fairness, make native costs real, establish useful growth or authorize deployment. All six native and eight reciprocal execution gates remain **NOT RUN**. Final handoff ends this reviewer's write authority unless a new exact assignment is given.
