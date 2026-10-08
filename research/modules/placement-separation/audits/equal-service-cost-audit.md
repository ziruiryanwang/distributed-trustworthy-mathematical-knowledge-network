# Independent audit of the equal-service routing comparison

Date: 2026-09-20. Reviewer: `placement_comparison_audit`. Status: **Repaired held-cut audit complete; ESC-AUD-001 and ESC-AUD-002 CLOSED after independent complete reread.** This reviewer did not author the comparison or change its source. Review covers paper reasoning and arithmetic, not execution, native feasibility or protocol selection. Original findings and attribution are preserved below.

## Exact reviewed cut and verdict

The current complete reviewed source is [equal-service-cost-comparison.md](../equal-service-cost-comparison.md), **48,606 bytes**, SHA-256 `467E52601C79B4E4B24253F8D9A6B94A2B06C13838893EA97391E617492EC6C5`. This complete replacement source was independently reread and its length/hash checked before closing the findings. The initial reviewed source was **47,405 bytes**, SHA-256 `FE5425945FD3FFAFA138A22810C746A1A273BC0933C544C2B15BD1DBAF9A23B4`; it also received a complete read and independent length/hash check. Its held dependencies include:

| Dependency | Bytes | SHA-256 |
|---|---:|---|
| [Stable-group candidate](../stable-group-contract.md) | 68458 | `EA9398969D640BDE89271E53274B4F0071D00436659F5BF8D03FC266AD250779` |
| [Placement architecture](../architectural-contract.md) | 33728 | `8FFD596DB086647971FB6E42AF5A2E2F38FE7D3FB1658C14DEC3D7686DA25C38` |

The principal result survives independent review: stable authority provides a conditional opportunity to reduce some route-owner transfer and group-renewal work, but the present comparison establishes neither uniform efficiency dominance nor an operable supplied deployment. The complete comparison makes the important adverse cases visible rather than suppressing them. The two findings below concern the rigor of two isolated negative/necessary-condition claims, not the dense/dispersed counts or the zero-remote-compaction proposition.

**Disposition:** ESC-AUD-001 and ESC-AUD-002 are closed against the current exact cut. No remaining blocker was found in the specified paper comparison. It may be used as a reviewed comparison and refinement decision aid. This does not select SG, allocate its binding, establish implementation costs, close native qualification, or demonstrate sustained useful growth.

## Review method and inherited boundaries

I first inspected the architecture and held SG contract and sent early challenges before receiving the held comparison. Those challenges included actual partition coarsening, existing H token sharing, already-available RETAIN compaction, O/adoption service gaps, coarse scan invalidation, batch byte limits, lifecycle caps and recipe-specific DROP counts. After author handoff I independently read the complete comparison and recomputed its cardinalities and arithmetic. Root separately called attention to the two precision points recorded below; I checked them independently and retain that attribution rather than presenting them as independent discoveries.

Relevant inherited contracts inspected for this review were:

- [F exact groups](../../../../notes/analyses/CP-001F-exact-routing-coverage.md): immutable old scope binding, one live owner per exact cell/provider row, current versus historical group observations, count/body batch limits, scope/holder/source caps, guarded eligibility summaries, CLOSE/expiry gates and delayed physical retirement.
- [F routing](../../../../notes/analyses/CP-001F-dissemination-and-routing.md): authenticated ungrouped PUT/renewal, exact cell/prefix incidence, adaptive deeper placement, provider row sharing and holder-local leases.
- [G structural publication](../../../../notes/analyses/CP-001G-structural-retrieval.md): at most 32 public tokens per descriptor, ProviderAd2/K4 binding, ungrouped capability path, immutable FULL_FEATURE support inside its owner scope, and unchanged native trust boundary.
- [H resource/discovery](../../../../notes/analyses/CP-001H-resource-supply-and-discovery.md): provider-wide unique key ownership with borrowing, only actual owned-key transfers, size-tiered owner consolidation, occupancy assumptions and enlarged aggregate count/byte limits.
- [O normalization](../../reciprocal-operability/batch-normalization-contract.md): actual parent-owned row moves, external borrowing, pre-mutation owner-version invalidation, one selected handoff, DROP-before-PUT and actual retained tails.
- [Q continuation](../../reciprocal-operability/continuation-admission-contract.md): actual residual state, disjoint unspent reservations, no forecast release credit, no small-holder premise and the distinction between final-stock reservation and actual renewal-pass order.

Only source inspection, formal paper arguments and ordinary arithmetic were used. No executable protocol model, extraction, Lean run, benchmark, native fixture or external write was performed. The author-owned source and registries remained read-only to this reviewer.

## Findings and resolution history

### ESC-AUD-001 — Larger upper envelopes do not by themselves refute actual total-cost dominance

**Location:** Dispersed holders, the sentence following the SG and scoped scan-budget comparison: “They defeat the argument ‘stable groups always make maintenance smaller’ …”.

**Status:** CLOSED against the 48,606-byte repaired cut. Initially OPEN against the 47,405-byte cut. Bounded claim-precision correction; the later exact call countercase is valid. The quoted location and argument below preserve the original finding.

The immediately preceding results compare declared sufficient scan envelopes, explicitly not realized CPU. From `actual_SG <= bound_SG`, `actual_old <= bound_old` and `bound_SG > bound_old`, the ordering of actual costs does not follow. For example, bounds 24 and 2 are compatible with actual costs 1 and 2, as well as with actual costs 24 and 2. Therefore larger upper envelopes alone cannot refute a claim about realized aggregate maintenance cost. The source correctly makes this distinction elsewhere; the quoted sentence is broader than that local evidence permits.

There are two sound ways to repair the sentence:

1. State that the envelopes defeat an inference of uniform maintenance savings from group counts, and identify this as conservative admission pressure rather than measured total-cost ordering.
2. State a narrower algorithm/metric counterexample with exact full-traversal work and the required primitive-cost assumptions. That would compare the stipulated algorithms' actual traversal class, not prove an ordering of every work axis or every correct implementation.

The first is the minimal repair. The source already contains an independent valid call-axis countercase later: fixed dispersed placements, no required future owner consolidation, no anchor/holder changes, already-supported RETAIN groups, equal renewal counts, zero RETAIN compaction transfer, and positive SG adoption work. Under those stated service assumptions SG has no call advantage over RETAIN. Referencing that countercase avoids importing any unselected optimization or invented measured scan cost.

This finding does **not** challenge `G*e`, `R*e`, the 24-fold comparison of the chosen envelopes, or the need to fund every actual SG scan attempt. It challenges only using those upper-envelope comparisons alone as a conclusion about actual total maintenance.

**Verified repair:** the dispersed paragraph now explicitly says that these are conservative scan-envelope comparisons, not realized CPU or total-maintenance ordering; a larger upper bound can coexist with smaller actual cost. It limits their consequence to admission pressure and blocking an unsupported inference of uniform savings from group counts, and separately points to the exact fixed-dispersed RETAIN call countercase. The complete reread confirms that the remaining equations, arithmetic, service distinctions and no-free-optimization boundary are unchanged in substance. This closes the finding without inventing primitive measurements.

### ESC-AUD-002 — The necessary renewal rate must name the holder-local time domain

**Location:** Finite capacity and recurring lower bounds, “leases of at most 48 hours require continuing successful extensions at asymptotic rate at least one per such interval per maintained group”.

**Status:** CLOSED against the 48,606-byte repaired cut. Initially OPEN against the 47,405-byte cut. Bounded time-domain correction; the holder-clock result is valid. The quoted location and argument below preserve the original finding.

F and SG deadlines are measured by the holder's continuous lease clock. They are not synchronized source or universal wall-clock deadlines. A necessary extension-frequency statement must therefore be expressed per 48 hours of that same holder clock, or explicitly derive its translation from appropriate clock-rate assumptions.

Counterexample to an unconditional wall-clock reading: let holder elapsed time equal one half of source elapsed time throughout an otherwise coherent interval. A 48-holder-hour lease can last 96 source hours. The necessary source-clock extension rate is then only one per 96 source hours, not one per 48. With no positive lower bound on holder-clock progress relative to the comparison clock, no fixed positive renewal-rate lower bound in that comparison clock follows.

The SG repair contract's upper relative-rate premise is useful for conservative expiration lower bounds. By itself, an upper bound on holder speed is not a positive lower bound on holder progress and does not repair this renewal-frequency lower-bound conversion. State the necessary rate in each continuous holder-local lease clock. If a common source/calendar rate is desired, supply the appropriate lower or two-sided relative-progress assumption and account for recovery discontinuity.

This necessary condition is specific to the inherited finite-lease model and its maximum lease duration, not an impossibility theorem for all decentralized indexes. A different durable-service or maximum-lease contract would need its own explicit authority, resources and protocol analysis; none is imported into this comparison.

This does not undermine the finite named two-pass arithmetic: that arithmetic counts explicitly stipulated successful renewal occurrences, not an inferred universal real-time minimum.

**Verified repair and added expression:** the source now names the issuing holder's own continuous lease clock and states the finite necessary bound `N >= H/48 - 1` for a single continuously ACTIVE group over H elapsed holder-hours. It explicitly excludes source/universal wall-clock conversion without a positive holder-progress lower bound, says the upper relative-rate premise alone is insufficient, and confines the result to the inherited finite-lease model.

The new finite expression is valid. At the start of the measured continuous interval, the existing lease has at most 48 holder-hours remaining. At any successful extending renewal commit t while ACTIVE, the old deadline is later than t and the new deadline is at most `t+48`. Consequently the positive increase of the deadline is at most 48 holder-hours. With N such extensions, total covered elapsed holder time is at most `48+48N`; continuous ACTIVE service for H therefore implies `H <= 48(N+1)`, equivalently the displayed necessary bound. Nonextending renewal calls do not add coverage and cannot invalidate this argument. The bound is loose at finite endpoints and is not a sufficient schedule or an extra grant. No clock discontinuity, replacement group generation or different durable-service contract is silently included.

## Verified incidence and coarsening argument

The source correctly fixes exact selected rows `(key, cell, holder)` rather than just theorem or token-incidence counts. The cell component matters: partial shallow and deeper placements can coexist, even for one key at one holder. Those extras are not silently bounded by the desired four chosen copies.

For the settled single-owner domain, let `I_h` be the set of old key-owner classes represented at holder h. If a map `alpha` sends each complete old key-owner class to one admitted stable authority, then

`G_old = sum_h |I_h|`,

`G_SG = sum_h |alpha(I_h)| <= sum_h |I_h|`.

The proof is the cardinality inequality for the image of each finite set. It requires actual coarsening on unchanged incidence and actual per-holder admission. Strictness requires two represented old classes to map to the same authority at some holder. With all selected rows on distinct holders, the image map has no such collision and equality holds. Capacity-driven splitting or changed holders invalidates this particular proof; the comparison explicitly says so.

The lower bound `sum_h ceil(R_h/c_h)` is a necessary count bound for positive effective per-group capacity `c_h`, not a construction theorem. A holder unable to admit even one required row must refuse that case; it is not a zero-denominator optimization. Foundation/authority separation, canonical bytes and actual aggregate holder stock can force additional groups or nonadmission. Empty ACTIVE groups, uncertain allocations and unreclaimed generations remain outside these selected-nonempty equalities and inside real stock admission.

H's existing borrowing is preserved. Two targets emitting the same provider/key do not need two route rows. O moves only keys owned by its selected input parents; keys borrowed from external owners remain physically untouched. Conversely, external borrowers of a moved key lose their settled old-version coverage before the physical transition. Neither retained owner scope IDs nor stable authority IDs justify stale borrower caches.

## Independent arithmetic

The complete finite stress case uses 480 targets, 24 old scopes of 20 targets, 32 distinct fresh keys per target and four chosen depth-zero rows per key. This is a conditional metadata incidence, not a demonstrated mathematical corpus.

| Quantity | Recalculation | Result |
|---|---|---:|
| Distinct owned keys | `480*32` | 15360 |
| Selected rows | `15360*4` | 61440 |
| Keys / rows per old scope | `20*32`; `640*4` | 640 / 2560 |
| Dense old groups | `24*256` | 6144 |
| Dense final NORMALIZE groups | `4*256`, with additional final-block balance | 1024 |
| Dense SG groups / rows per group | `256`; `24*10` | 256 / 240 |
| Dense two-pass RETAIN / NORMALIZE / SG calls | `2*6144`; `2*1024`; `2*256` | 12288 / 2048 / 512 |
| Dense two-pass savings versus RETAIN / NORMALIZE | `12288-512`; `2048-512` | 11776 / 1536 |
| Dispersed groups under all owner partitions | one holder per selected row | 61440 |
| Dispersed two-pass calls | `2*61440` | 122880 |

The dense per-scope construction `holder=4*(j mod 64)+c`, `0<=j<640`, `0<=c<4`, gives exactly ten rows per holder and four distinct holders per key. It establishes combinatorial incidence only. It does not establish F's nearest-holder hash realizability, real holder willingness or a Lean family. Final normalized sizes `256+128+64+32=480` do not alone establish all-holder occupancy; the source explicitly adds the needed final-block balance premise.

| Scan term | Dense SG | Dense old scoped fallback | Dispersed SG | Dispersed old scoped fallback |
|---|---:|---:|---:|---:|
| Entry-traversal envelope | `256*480=122880` | `6144*20=122880` | `61440*480=29491200` | `61440*20=1228800` |
| Anchor-search comparison envelope | `61440*480=29491200` | `61440*20=1228800` | `61440*480=29491200` | `61440*20=1228800` |

The selected-row token-comparison envelope is `32*61440=1966080`. At a common inventory size e, `sum_g m_g=R` gives `sum_g m_g*e=R*e`; reducing G does not reduce this second envelope by itself. The claimed quadratic worst-case budget under both R and e proportional to growing N is algebraically correct. It is explicitly not a universal lower bound or measured CPU result.

## Adoption skeletons and batching

The prescribed DROP-before-PUT transfer has two successful row mutations per moved actual row. This is recipe-specific, not a universal lower bound for every possible F lifecycle strategy. F's CLOSE gate and subsequent fenced replacement could support a different separately admitted plan with a different service trace; the comparison correctly refuses to substitute it silently.

In the dense regime every old group has ten rows. At least one DROP batch per old group gives 6144 count-only DROP batches. Each destination SG group has 240 rows, so its 64-count ceiling gives at least four PUT batches and `256*4=1024` in total. Adding the explicit fresh-OPEN/empty-CLOSE policy gives

`6144 + 1024 + 256 + 6144 = 13568`.

This is an optimistic count-only skeleton lower bound, not an executable packed schedule. Bytes, candidate header size, root/version changes, per-key uniqueness, settlement, control authority and service constraints can require more. No cross-holder or cross-owner batching is assumed.

With singleton mutation calls that individually fit, the same clean dense skeleton is

`2*61440 + 256 + 6144 = 129280`.

With all selected rows at distinct holders, each source/destination group is a singleton and the explicit strategy uses

`61440*(DROP + PUT + OPEN + CLOSE) = 245760`

skeleton calls. These calculations agree with the source. None is a full deployment or interval budget: ordinary lease events, source support work, action settlement/delivery, failures, histories, connection costs, custody and aftercare remain separately charged. Transferring only a selected subset cannot authorize closing a parent containing unrelated residual rows.

The batch inequality `ceil(n/64)<=B<=n` is properly restricted to fitting singleton requests, a plan permitting singleton progress, and no extra retries. The left side is not a promised packing. The right side is a simple admissible mutation-request envelope, not an upper bound on all complete service actions. O's actual row-at-a-time path is not retrospectively replaced by ideal full batches.

## Renewal and support schedules

The comparison correctly counts successful renewal events at their actual cuts. A final population multiplied by two is valid for an unchanged two-pass fixture or a labeled conservative reservation, not an arrival-interleaved actual trace. Empty/partial groups receive additional renewal events only when their real obligations require them; closed/expired records remain stock without automatic renewal.

It also correctly refuses to infer two source scans from two renewal passes. Under unchanged coherent guards a complete summary may be reused or paid-rebound; dirty, discarded and restarted attempts count separately. SG's coarse fence can invalidate many summaries even when a newly added target contributes only already-owned tokens. Coalescing several additions before a scan is lawful only under the same admitted temporary coverage degradation and publication deadlines; it is not a free reduction in scan frequency.

The old scoped fallback is identified as a separately stipulated algorithm, not an implemented measured baseline. It still must include actual posting paths, complete native assessment dependencies and current guards even if its selected anchor-search inventory is smaller. Shared dependencies can invalidate several scopes. The comparison does not incorrectly impose SG's provider-wide scan on all competitors, and does not import a free dictionary, common-C scan or resident cache into SG.

The repair-service discussion preserves the held SG contract's relevant constraints: one unresolved effectful lane, actual old-action settlement, exhaustive known-supported/removal classification, separately admitted UNKNOWN branches, two paid scan attempts in the simple episode, original-dispatch timing basis and prefix deadlines. It does not upgrade survivor row continuity into uninterrupted source coverage or checked reader reuse.

## Caps, stock and service fairness

At the named selected starting state the target/key/row/group counts fit the enlarged H/B cardinality limits, not necessarily bytes, actual source control state or recurring service. The dispersed count does exceed F's smaller default 32768-group source cap. The source explicitly distinguishes those regimes and forbids inheriting old bytes-per-record as an SG measurement.

At a dense holder, 240 selected rows and 24 old groups or one SG group do not exceed the cited isolated holder count limits. This is not aggregate holder admission: other providers, empty/retired groups, row histories, markers, snapshots and actual byte/service limits still matter. Keeping immutable owner scopes after physical compaction continues to consume real scope capacity. Stable namespace names do not create uncapped authority or inventory capacity.

All-prefix admission keeps incumbent duties, native/custody service and optional migration together. Work reservations are disjoint residuals excluding spent work. A measured release barrier can recut physical stock, but cannot reset expenditure or subtract the same release twice. No source declaration of remote CLOSE/expiry becomes observed physical foreign GC.

Adoption and O migration necessarily expose the same-holder DROP/PUT gap under the chosen recipe. If the common service offer prohibits any such gap, that policy is infeasible. Other actual copies can meet a separately stated weaker redundancy or reachability offer only under their own current guards, leases, marker paths and reader overlap. The comparison properly reports both actual row absence and current assertion degradation rather than equating them.

The break-even expression is valid for its explicitly stationary counts and complete extra adoption term. The skeleton is not a substitute for complete adoption cost. Against RETAIN, pure-layout compaction avoidance is zero; against NORMALIZE it is only actual avoided transfer work, not a logarithmic allowance misreported as expenditure. Axis-wise savings do not imply feasibility in other resource axes, and a weighted utility cannot override a hard cap.

## Evidence limits and next handoff

This review supports using the repaired comparison to decide where further concept work is worthwhile. It does not provide missing cost functions, a real nearest-holder incidence, an incident workload, a sufficient service calendar, an accepted native cohort or useful checked reuse. No positive tiny fixture can fill those gaps by repetition of the same assumptions.

A separately specified shared preparation or anchor lookup mechanism could improve the analyzed SG fallback, but it is not part of this source or audit. Any such later source must preserve exact guards, byte/visit accounting, retention and complete-input arguments and receive its own independent review.

The initial audit was handed to root with ESC-AUD-001 and ESC-AUD-002 OPEN, at **20,641 bytes**, SHA-256 `B2B9CC0B50619E2C4740DCDE372C4AC55940FCC0550A748DA890C987B01FED63`. Root coordinated the author repair and supplied a new held cut after the author ceased edits. I independently checked the replacement source hash and reread that complete 48,606-byte cut, including the affected composition and the new finite holder-clock inequality. Both findings are now CLOSED with no additional blocker found at this audit's paper-comparison scope. This closure is based on the read replacement source, not merely an author message that it was fixed.

Final handoff preserves all earlier evidence limits: no SG selection, no new wire allocation, no shared-catalog optimization, no executed qualification and no sustained useful-growth claim. The source and registries remain read-only to this reviewer; editing authority over this audit ceases at final handoff unless root explicitly reopens it.
