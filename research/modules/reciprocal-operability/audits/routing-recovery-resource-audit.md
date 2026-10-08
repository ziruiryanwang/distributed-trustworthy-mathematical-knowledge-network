# Bounded routing recovery: independent resource/lifecycle audit

Date: 2026-09-20. Reviewer: `qualification_contract_review`. Scope: same-scale F/H supply, joint resource/calendar admission, lifecycle ownership, competing contributions, overflow and settlement. Concept/source-contract review only; no implementation, executable model, Lean execution, native replay, extraction or benchmark. Only this audit is owned by this reviewer.

Final disposition: **RREC-RES-001 and RREC-RES-002 are closed at the repaired held cut below.** The initial findings and arithmetic remain historical records of the initial source. Closure is source-contract/paper review, not empirical qualification, selected-baseline change or checkpoint integration approval.

## Initial held source and disposition

The complete [routing-recovery proposal](../routing-recovery-contract.md) was read and independently hash-confirmed at SHA-256 `653FD87EB766141D920B6BACF4BC62C7C2F106BF4A46C7B08D30FC222AB6FF30`.

Two medium-severity resource/lifecycle handoffs require repair at this cut. **RREC-RES-001** was first raised in the author's self-check and independently confirmed here; **RREC-RES-002** incorporates root's independently raised H side-scope classification issue and this review's calendar check. Neither is a demonstrated native-soundness defect. The aggregate paper arithmetic reproduces; that does not repair missing lifecycle or scheduling details.

Inherited contracts read: [F exact routing](../../../../notes/analyses/CP-001F-exact-routing-coverage.md) and [H supplied scale](../../../../notes/analyses/CP-001H-resource-supply-and-discovery.md), with relevant [base ROUTE1 occurrence, lookup, lease and maintenance rules](../../../../notes/analyses/CP-001F-dissemination-and-routing.md). The [earlier H resource audit](../../../../notes/audits/CP-001H-resource-cross-audit.md) was consulted to preserve its distinction between selected stock, actual maintenance work, amortized work and elapsed service.

## RREC-RES-001: serialized calls do not imply one live route executor

Severity: **medium; incorrect lifecycle/concurrency inference**.

The numerical calendar states that at most one actual route/group call is in flight, “hence at most one of the four aggregate route executors.” It also permits a sixteen-call maintenance lookup to advance through four 0.4-second gaps between managed-key jobs. That maintenance occurrence retains its candidate/tried sets, progress and deadline while paused. A managed-key lookup executes before the maintenance occurrence finishes. Serializing their individual remote calls does not serialize the two occurrences or eliminate the paused occurrence's resident state.

This is a repairable accounting error, not evidence that the four-executor envelope is inadequate. One main occurrence plus one maintenance occurrence would fit a limit of two, within the actual aggregate four. With four 0.1-second calls in each gap, sixteen maintenance calls can span four gaps separated by 20.4 seconds: approximately 61.2 seconds between first and last gap, plus the bounded call time, within the existing 120-second occurrence limit. Simultaneously due bucket and local-position lookups still need an explicit stagger/sequence; the per-lookup limit is not a new allowance of four additional executors.

Minimum repair: state the actual maximum number of live occurrences, count their full retained/transient state, and specify how recurring bucket/local-position starts and pauses satisfy their own deadlines under the one-at-a-time call schedule. Do not silently redefine an executor to mean only a momentarily in-flight RPC.

## RREC-RES-002: side-scope lifecycle and calendar handoff are incomplete

Severity: **medium; incomplete composition with existing H operating policy**.

The positive instance admits twenty new checked targets per day into one separate daily scope, retains eight such scopes plus the managed main scope, and charges the side scopes' new placements and twice-daily renewals. H also selects a size-tiered policy with explicit completed runs, pending inputs, one consolidation handoff and counted old/new/retired scopes. The proposal does not identify where those daily twenty-target scopes lie in that lifecycle or how required consolidation is scheduled or honestly deferred.

Eight separately retained daily scopes are not automatically eight lawful completed power-of-two runs. Conversely, the mere existence of H's bounded pending-input capacity does not prove that a scope has reached a completed consolidated state. Source attribution or a fresh scope hash cannot supply a second free row owner. Root raised this classification gap independently; the resource review confirms it against H's selected policy.

The calendar also puts the 54,128 other/reserve calls in one post-key block. The side-scope share includes recurring renewals, and same-day new publication depends on actual completed checks and committed index state. Merely assigning a daily total to that block does not show the recurring side-renewal schedule or the new-check → index → placement precedence while preserving the earlier inherited admission rules. The separately supplied 16,000 seconds of native/query work cannot be assumed to have produced public eligible targets before those checks occur.

Minimum repair:

- Give the eight-day side scopes an explicit lawful H pending/completed/merge classification. Count every required transition and retained parent/pending/uncertain scope; report any deferred consolidation as such, not a settled run invariant.
- Fit any newly required owner-transfer, renewal and cleanup work inside the already shared call, byte, CPU and stock allocations, or explicitly revise the supplied instance. An amortized merge estimate is not a daily burst allocation.
- Place the side scopes' actual periodic renewals in the conditional calendar and specify an admissible order for checking, public indexing and placement of the new contributions. The remaining daily slack suggests room for a repair, but room is not the missing schedule itself.

This finding does not require the main immutable scope to absorb every new theorem or forbid independent new mathematics. It requires the chosen positive contribution path to honor the same H contract whose budgets it uses.

## Arithmetic and simultaneous resource checks

All values below are stipulated fixture demands/supply, not measured Lean or network costs. The review recomputes their arithmetic without inferring operational success.

| Check | Result at the initial held cut |
|---|---|
| Scope refresh count | 2,049 keys/day × 8 days = 16,392 keys. At 80 calls per job, daily refresh reservation is 163,920 calls. |
| Total daily calls | 163,920 + 40,000 + 4,096 + 32,000 + 22,128 = **262,144**, exactly H's source call envelope. The classes cannot be added again as independent grants. |
| Maintenance share | (144 bucket + 24 local-position lookups) × 16 calls = 2,688; plus 1,408 other calls = **4,096**. It fits only under the stipulated sixteen-call actual completion premise, not the general sixty-four-call horizon. |
| New publication | 20 targets/day × 8 new tokens × (16 lookup + 4 OPEN + 4 PUT) = **3,840 calls/day**, conditional on those actual successful destinations and no extra work. |
| Side-scope final stock and renewal work | 8 × 20 × 8 × 4 = **5,120** new chosen rows, with at most that many new groups under the stated worst separation. Two renewals require 10,240 calls/day at final size. 32,000 − 3,840 − 10,240 = **17,920** remaining calls. RREC-RES-002 concerns lifecycle/timing, not this arithmetic. |
| Managed groups | (65,568 new generations + 20,000 original generations) × 4 KiB = **334.25 MiB**. The lifetime holder-union premise is additional to H's instantaneous holder population. |
| Managed row generations | (65,568 old + 65,568 new) × 2 KiB = **256.125 MiB**. DROP/CLOSE does not erase their charged generations immediately. |
| Other scope and aggregate metadata | 5,120 × (4 + 2) KiB = 30 MiB; adding 256 MiB remaining metadata gives **876.375 MiB**, below 1 GiB. Exact maps, snapshots and fences must actually be covered by the stipulated sizes. |
| Count ceilings | 90,688 group generations < 400,000; 136,256 row generations < 264,000. These are not substitutes for the byte limit or lifecycle qualification. |
| Traffic | 262,144 × 8 KiB = **2 GiB** control traffic; plus 4 GiB bulk and 1 GiB other = **7 GiB/day**, below 8 GiB. Connection/setup/failure traffic must truly be in those stipulated charges. |
| CPU | 262,144 × 0.025 + 2,049 + 2,400 + 16,000 = **27,002.6 CPU-seconds/day**, below 28,800, leaving 1,797.4. Repair work cannot silently exceed this same parent. |
| Native and resident stock | 2,208 × 256 KiB = 552 MiB incremental retained evidence; 2 GiB core + 552 MiB fits 8 GiB disk. The independently stipulated 1.75-GiB joint workspace fits 2 GiB; the disk calculation does not prove the RAM premise. |

The twenty-target side scopes' correct lifecycle and any repair-induced scheduling costs remain subject to RREC-RES-002. The stated sizes are peak **physical** accounting assumptions, not upper bounds derived from identifiers alone. Actual remote holder group/map/row/snapshot work requires its own supplied stock and service; no source ledger can confer that capacity.

## Timing, authority and tail boundaries inspected

The source correctly distinguishes a fresh-start bound from completed lookup, observed placement and checked use. Its recovery proposition has explicit successful lookup/placement and reader-overlap premises. CLOSEST_SEEN is not a globally-nearest-set certificate. A pre-stabilization occurrence does not count as the promised fresh post-stabilization start. Clock/reference-time precision is separately cross-reviewed; this resource review does not invent globally synchronized monotonic clocks.

The eight-day illustration does more than divide work by a daily budget: it supplies strong 0.1-second actual control-operation service and a twenty-second successful managed-job bound. Without those and the admitted competing-service calendar, arithmetic gives no wall-clock recovery theorem. At the stated calendar, the first 2,000 slots end at second 43,000 and the remaining 49 end at 46,399.6. Adding 5,412.8 seconds for the other/reserve calls and 18,400 for native/local work gives 70,212.4 seconds, leaving 16,187.6 seconds of nominal daily slack. That aggregate room is compatible with finding a corrected calendar; it does not by itself close the two findings.

The comparison 1,049,088 lookup calls divided by 222,144 residual calls/day is correctly labelled a sustained-rate/average calculation. Arbitrarily phased grants, missing service and other work preclude treating that quotient as a universal elapsed lower or upper bound. Future cycle authority/resources must actually be supplied, and continuing contribution growth requires new admission.

The proposal retains exact group ownership/version/root checks, does not CLOSE a nonempty group solely because one key moved, counts uncertain possibly committed work, preserves generation-fenced cleanup and charges old/new overlap. Its four successful new holders and sixteen group calls per key are a favorable explicit premise, not a guarantee that sixteen attempted destinations all need only one call or that refusals are free. Paid failures can exhaust the reserve and defeat the timing claim.

The numerical fixture is depth zero. It therefore spends no markers in that case; the general path still requires actual ancestor lookup, admission, refresh and repair. Renewing a leaf group cannot discharge them. The result is not a same-budget deep-shard or arbitrary-churn guarantee.

Tail settlement within two hours and old snapshot lifetimes of at most one hour are explicit additional **actual service/lifecycle premises** for repetition. They are not derived from a row count, lease expiry or available daily CPU. Required unreconciled state must carry forward and can block the next cycle. No released ownership or deadline alone proves physical reclamation. A corrected calendar must retain this distinction rather than claiming that its spare average allowance guarantees those premises.

Historical ROUTE_LIST data remain historical snapshot observations. This audit does not require a valid historical page to assert live-at-delivery leases; a future useful discovery path is a separate premise, not an extra truth property attached to every old page.

## Initial handoff

At this held initial cut, **RREC-RES-001 and RREC-RES-002 remain open**. Root and author have received the consolidated finding set; a repaired exact source must be reread before closure. No selected-baseline change, implementation authority, empirical feasibility result or checkpoint-integration approval follows from this audit.

## Repaired held cut and independent full reread

The complete repaired proposal was read and independently hash-confirmed at SHA-256 `65B395B47DE0CD86EB802C30409276E5202416ADB334378B52EB126846D8F605`. This reviewer did not edit the proposal. The following dispositions apply to that exact cut, not retroactively to its initial version.

### RREC-RES-001: closed

The source now counts up to **two live route occurrences/executors**, one managed-key job and one paused maintenance lookup. Both retain the actual bounded F lookup state in the stipulated metadata/workspace. Actual route/group calls remain serialized, with at most one pending mutation batch. The paused occurrence is no longer silently erased from concurrency or state accounting; two fits the shared four-executor envelope.

Each sixteen-call maintenance lookup uses four 0.4-second gaps under the actual 0.1-second-per-call premise. Its stated maximum completion time, including waiting to the next gap, is 82 seconds, below F's 120-second occurrence deadline. Hourly own-position opportunities are offset by two minutes from the hour's bucket opportunity, and one maintenance lookup completes before the next begins. Other local/native work yields at due opportunities outside the fixed key slots. These timing assumptions select a feasible paper schedule; no empirical latency or automatically granted callback follows.

Managed-key jobs finish inside their reserved slots before the next key begins. Renewal windows and key blocks are disjoint. A maintenance lookup only discovers/probes contacts; it does not concurrently mutate the managed groups. Consequently the favorable calendar need not manufacture stale expected-member roots by preempting a pending key batch with renewal. Other admitted mutations still require their inherited current-root/version checks and paid reconciliation; the calendar does not waive them.

### RREC-RES-002: closed

The eight daily twenty-target scopes are now explicitly **pending input/consolidation scopes**, not completed equal-size tiers. The fixture has one completed 2,048-target run, at most eight pending inputs and no active consolidation handoff. Actual constructed feature scopes and their row owners can expose these admitted contributions while consolidation is deferred. Pending status preserves every renewal, coverage, storage and cleanup obligation. A later settled tier layout or continued cadence requires separately funded H merge/handoff/retirement, or refusal of further inputs.

This is a legitimate finite deferral within the supplied pending capacity, not a proof of perpetual contribution/consolidation throughput. The fixture still includes twenty new targets per day and does not remove their native acquisition/checking, publication or renewal work to obtain the desired refresh bound. Common-token ownership remains with its actual existing owner; a pending scope does not acquire a duplicate row or count borrowed coverage as its own independent placement.

Both 3,000-second renewal windows now include side groups. A pass has at most 20,000 managed plus 5,120 side-group renewals: **25,120 calls**, using at most 2,512 elapsed seconds, with side calls charged to the original 32,000-call class. At fixed window starts twelve hours apart, the worst inter-commit separation under that full window bound is below thirteen hours. The explicit initial fourteen-hour genuine headroom and newly granted 48-hour leases are therefore compatible with this supplied schedule. A duration receipt alone does not establish those foreign-clock/headroom premises.

New publication now follows its actual prerequisites. After managed-key slots, the first 1,000 seconds of the existing 16,000-second native allocation complete twenty targets' acquisition/checking/protection/export/index preparation at a stipulated fifty elapsed seconds each. Only then do their separately counted route/group placements occur. This is not another native allowance or an inference that any arbitrary twenty Lean targets fit fifty seconds each. New groups initially obtain their own actual 48-hour grants and join subsequent renewal passes.

### Recomputed repaired calendar and unchanged joint ceilings

| Repaired calendar component | Result |
|---|---|
| First renewal window | Seconds 0 through 3,000; at most 25,120 calls. |
| First key block | 1,950 × 20.4 = 39,780 seconds; starting at 3,000, ends at **42,780**. |
| Second renewal window | Seconds 43,200 through 46,200; same maximum renewal count, separately charged. |
| Remaining key block | 99 × 20.4 = 2,019.6 seconds; ends at **48,219.6**. There are still exactly 2,049 keys/day. |
| New-target prerequisites | First 1,000 seconds of the existing native work allocation, before placement. |
| Remaining nonrenewal other/reserve calls | 32,000 − 10,240 + 22,128 = **43,888**, taking at most **4,388.8 seconds**; includes the 3,840 new placement calls. |
| Other local/native work | Remaining 15,000 seconds of native/query work plus 2,400 seconds local maintenance. |
| Sum before remaining maintenance pauses | 48,219.6 + 1,000 + 4,388.8 + 15,000 + 2,400 = **71,008.4 seconds**, leaving **15,391.6 seconds** in the day. |

Renewal-window slack is 488 seconds per window at maximal call occupancy. The 2,049 inter-key maintenance gaps provide 819.6 seconds in total. The declared 409.6 seconds/day of maintenance can be distributed through its due opportunities and separately counted pauses; its calls were already included in 4,096, not added again. Total daily calls remain 262,144, traffic at most 7 GiB, CPU 27,002.6 seconds and metadata 876.375 MiB. The actual stipulated simultaneous workspace, resident host/runtime supply and remote-holder capacities remain independent requirements.

No bound is obtained merely by dividing daily funding by cost. The repaired numerical witness stipulates one mathematical elapsed-time scale, unit-rate continuous monotonic clocks with arbitrary offsets, actual local scheduling, operation response bounds, granted leases and successful placement service. This imposes no synchronized-clock protocol or permission to compare foreign expiry timestamps. The timing statement is conditional on those actual premises, including future cycle supply when the chosen fresh-start bound crosses the cycle boundary.

The repaired proposal also distinguishes holder eligibility at actual ROUTE_LIST snapshot/read cuts from historical page delivery after ordinary lease expiry. This audit retains that distinction; it does not strengthen historical observations into a current lease or native-reuse certificate. Detailed clock and discovery composition remains the separate review's scope.

### Settlement and failure limits remain explicit

Retired/uncertain state continues to consume its exact charged stock. Repetition still requires actual funded generation-fenced cleanup and the stated tail settlement/snapshot premises. The calendar's residual 15,391.6 seconds is **not** proof that remote reclamation or arbitrary uncertain outcomes resolve within two hours. Failed settlement carries the tails into actual readmission or stops the next cycle; the one-cycle stock bound cannot be reused against unreclaimed history.

Larger holder unions, deep marker paths, actual costs above the stipulated operation/native/RAM limits, dirty eligibility work, unsuccessful admissions or response delays can defeat the numerical witness. The policy reports degraded/partial service without releasing unrelated custody, forgetting work or creating new grants. Its eight-day refresh-start schedule is not global convergence, an availability SLA, a worldwide discovery result or evidence of sustained knowledge growth.

## Final review boundary

Final held proposal SHA-256: `72ED31CCDC22975784C94AC3F15D6244E83E76444ECE70E214B3FAFBD1C58292`, 24,955 bytes. This is the final root-authorized narrow ownership clarification following the completely reread intermediate cut above.

The final scope-stability paragraph was read and hash-confirmed. It distinguishes the admitted provider/publication-scope owner from mutable holder/group/row placement references. Guarded movement of those physical references for the same admitted obligation is the intended recovery transition, not self-invalidation. Changed scope membership/owner, required cell path, disclosure or native eligibility still requires the actual new admission and guards. Intending a new destination does not establish observed placement, and old/new ownership/accounting obligations remain intact.

For a precise delta check, this reviewer substituted only the previously read paragraph in memory and recomputed the whole proposal digest. It exactly recovered `65B395B47DE0CD86EB802C30409276E5202416ADB334378B52EB126846D8F605`. Thus all other bytes, including resource tables, side-scope lifecycle and calendar, are unchanged from the fully reviewed intermediate source. No source file was edited in that check. The clarification was raised by root and confirmed in the separate composition review; this audit records its resource/lifecycle compatibility, not independent origination of that finding.

Both named resource/lifecycle findings remain **closed at this final held cut**. No additional resource/lifecycle countercase was identified in this bounded selected fixture. All positive conclusions remain conditional paper consistency under its explicit finite scope, successful service, capacity, clock, eligibility and settlement premises.

This review does not approve checkpoint integration, select the optional policy, alter frozen F/H contracts or authorize implementation. Only this audit file was edited; original findings and their attribution are preserved.
