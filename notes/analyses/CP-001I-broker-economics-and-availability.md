# CP-001I analysis: broker economics and evidence availability

Date: 2026-09-20. Status: concept/arithmetic analysis of the proposed BROKER1 lane, not a selected protocol extension, resource measurement or benchmark. No implementation, native replay, artifact extraction or simulation has been performed. The frozen G/H contracts remain unchanged.

## Question, conclusion and comparison boundary

Separating candidate discovery from evidence custody can be useful when the desired replication or specialization of search is substantially greater than the evidence replication actually required and supplied. It does not make evidence, independent checking or cold support disappear. It can also be worse than the existing qualified native indexes, particularly when untrusted token-only results produce expensive false leads or when independent broker-route renewal dominates maintenance.

The companion [trust-boundary note](CP-001I-candidate-service-trust-boundary.md) owns the acceptance argument. The [BROKER1 proposal](CP-001I-untrusted-search-brokers.md) owns the actual mechanism. This note uses its minimal lane: a broker retains bounded canonical copies of STRUCT2 descriptors, token postings and bounded concrete acquisition leads; it does not qualify or retain their native closures, recompute the extractor, certify pattern matching, proxy evidence bytes or assert PUBLIC_SERVE. A lead names the exact descriptor-bound replay at an actual public-native source. Actual reads require fresh source negotiation and its existing public scope or independently issued holder-bound export authority. At most four leads per listed candidate are proposed. Different replay alternatives remain distinct candidates.

BROKER1's token query is not equivalent to a native provider's optional checked pattern-filtering query. Copied pattern digests are not the underlying pattern bodies. A fair evaluation therefore includes both a common token-only comparison and a comparison against the strongest applicable, actually funded native baseline. Improved ranking or future broker pattern storage is not assumed.

Three experiments answer different questions:

| Experiment | Resources held fixed | Valid possible conclusion |
|---|---|---|
| Qualified indexes alone | Existing native/index/custody supply | Baseline checked-reuse cost, coverage and availability |
| Existing custody and indexes plus brokers | Existing supply is preserved; extra broker supply is counted | Whether additional search service is worth its additional cost |
| Redistribution between native indexes and brokers | Stated evidence-recovery and useful-service requirements, with all changed supply disclosed | Whether some native duplication can be avoided without violating those requirements |

The second experiment cannot establish a saving merely by treating donated broker resources as free. The third cannot silently weaken an eight-source availability requirement to two sources. Retaining two sources is legitimate only if two-source supply is the declared policy and its actual failure/throughput limitations are acceptable. Previously promised custody cannot be withdrawn merely to improve this comparison.

## Four independently investigable economic modules

The following local module labels separate conclusions which need not be resolved together. They are analysis references, not protocol IDs. Each module can produce a useful conditional result even when another deployment regime is defeated.

| Module | Assumptions to expose | Relation to establish | Defeating case | Decision criterion |
|---|---|---|---|---|
| I-E1: native-replication savings | Actual closure unions; discretionary versus required copies; warm qualification costs; honest baseline metadata costs | Avoided native stock and future qualification minus changed metadata stock/ingestion | Baseline copies are all still required, or broker metadata exceeds the avoided native work | Report the actual coordinate-wise savings for the declared corpus; do not claim a system-level win yet |
| I-E2: custody/service substitution | Explicit recovery target, failure domains, warm/cold client demand, source capacities and peak native memory | Retained evidence sources still satisfy that recovery target and actual service load | Metadata survives but exact evidence is unavailable; consolidation overloads the remaining sources | Approve redistribution only for a stated target with supplied retention, bandwidth, native work and peak capacity; otherwise keep or add custody |
| I-E3: route/renewal amplification | Known-contact versus routed discovery; actual token unions, row copies, leases, selected native grouping | Broker-route stock and ungrouped renewal fit supply and the I-E1 margin | Full replicated token scopes generate unaffordable maintenance or silently borrow native grouping | Use known contacts/smaller explicit scope when sufficient; select large routed mode only after its actual maintenance budget fits |
| I-E4: stale-lead client cost | Same investigation pool; token-only versus native filtering; budgets; stale/false lead and cold-acquisition distributions | Extra candidate/source/client work and useful checked yield remain within the retained savings/service requirement | Cheap false metadata induces enough wasted native work to erase the gain or reduce useful throughput | Compare complete paid attempts and checked applications; accept only the measured/established workload-specific break-even |

I-E1 can be analyzed first as arithmetic over supplied closure/cost facts. I-E2 is an independent gate on any attempted custody reduction. I-E3 and I-E4 add different maintenance and demand-side differences; neither can be inferred from the other. The complete decision is their conjunction with the companion service/acceptance contracts, not a reason to postpone every small useful result until a universal architecture is proved. Pending numerical qualification in one module remains explicitly pending.

## The objects whose replication is being compared

Let a finite workload interval have:

- `N` selected exact mathematical targets, with explicit foundation and replay alternatives;
- `lambda` newly admitted distinct target/replay units per unit time before replication;
- `Q` admitted local discovery attempts per unit time, including unsuccessful attempts;
- `r_i` qualified native index copies per target in a simple homogeneous baseline;
- `r_e` qualified complete evidence-source copies per target in the proposed design;
- `r_m` broker metadata copies per target in that design.

The scalar copy counts are only a homogeneous fixture. In general, use the actual target/source incidence relation, closure overlap, source resources and failure domains. Two replays of the same judgment may have different support, different closure bytes and different downstream utility. Merging their stock or qualifications because their terminal judgment is equal is not licensed by this accounting.

For target `t` at source `s`, let `C(s,t)` be the complete exact selected native evidence closure that the source must retain under its service contract, including required support. A source's canonical retained byte stock is

`B_native(s) = bytes(union over admitted t of C(s,t))`.

The union is over actual reusable content-addressed objects under that source's protected state, not over an imagined globally deduplicated disk. Fleet stock is the sum over independent physical retained allocations. If several logical slots share one physical allocation, count the actual allocation once but disclose its shared failure and service bottleneck. Reconstructed environments, caches, index structures, temporary exports, redundant local copies and allocator overhead are additional allocations.

For a homogeneous full-corpus fixture, write `B` for a shared retained native core and `delta` for an actual disjoint incremental byte bound per target. Then one full source needs at most `B + N delta` canonical native bytes. This formula is not valid when a supposed increment secretly contains uncounted external support, or when reuse is unavailable under the source's exact foundation/realization. Nor does canonical byte size bound resident kernel or collector memory.

Let `mu` be the actual per-target broker metadata allocation, including copied descriptor and leads, postings, local identifiers and the attributable retained snapshot/index state. Broker-route ads at remote holders, transport state, temporary versions and non-attributable fixed allocations are separately charged. `mu` is an accounting variable, not a new wire-record size. A broker can copy syntactically valid but false feature claims cheaply; that is metadata ingestion, not a native target qualification.

## Separate resource inequalities, not a single fictional cost

For design `D`, maintain a resource vector over the same workload and interval:

`Cost(D) = (CPU, network bytes, disk read/write work, retained byte-time, maintained record counts, native qualification events, …)`.

Peak memory, maximum concurrently protected native environments, socket/connection limits, admission deadlines and service latency distributions are constraints in addition to these cumulative coordinates. Adding seconds to bytes is meaningless. A local owner may introduce explicit prices or limits to compare a vector, but those choices must be stated; there is no universal proof that the smallest aggregate number is the best decentralized deployment.

Useful successful applications and subsequent useful contributions are outcomes, not free resource coordinates. If one design spends less only because it gives up on difficult investigations earlier, that does not establish equal-service efficiency. Compare a declared investigation pool and report checked successes, failures, timeouts, stale leads and later contributions together with their charged costs.

For any resource coordinate `k`, decompose the difference as

`Delta_k = Cost_k(broker design) - Cost_k(native baseline)`

`= - avoided_discretionary_native_k + metadata_and_route_difference_k + client_investigation_difference_k + source_service_difference_k + transition_difference_k`.

All terms are actual differences. The baseline already stores descriptors and postings and maintains routes; its metadata must not be charged only on the broker side. Conversely, a retained custody source that still runs its native index has not eliminated that metadata merely because another broker was added. Transition costs include new qualification, copying, partial service and retained old versions until actual release.

Under equal warm incremental qualification cost `c_native`, one deliberately simplified CPU break-even condition is

`(r_i - r_e) lambda c_native + avoided_new_core_qualification_CPU`

`> Delta_metadata_route_freshness_CPU + Q Delta_investigation_CPU + Delta_source_service_CPU + transition_CPU`.

Here `Delta_investigation_CPU` is the actual signed increase in per-attempt client work, including eventual checking and rejected candidates. The corresponding inequality must be checked independently for bandwidth, ongoing retained stock, disk service and required latency. A positive CPU result cannot compensate for violating a source's RAM ceiling or a retention obligation.

`c_native` is actual amortized incremental reconstruction/checking/protection cost under stated warm conditions, not one kernel instruction per theorem. Counting `r_i N` qualification events is not a count of distinct kernel declaration checks. Foundation qualification, duplicate declarations, replay environments, partial reuse and cache invalidations may change the cost per event substantially. Qualification performed in the past is sunk work; retiring a copy does not recover its old CPU time. Avoided future insertions or new replicas can save future work.

Similarly, native stock falls only when an extra copy is not created or when its real retention references can legitimately be released and its unshared bytes reclaimed. A logical role rename does not free shared pinned support. A required custodian which remains must retain its closure even if its public search function moves to a broker.

## Query and insertion work which must not be hidden

A complete discovery attempt may include:

1. Choosing an owner-admitted broker or qualified source and discovering/authenticating its contact.
2. Routing, bounded token pages, descriptor parsing and ranking, duplicate suppression and snapshot/cursor handling.
3. For each selected candidate, authenticating a concrete native source and establishing its current exact replay/read authority.
4. Partial candidate-type or support reads, unavailable-source attempts, compatibility checks and other bounded early rejection.
5. Acquisition of the complete selected closure, exact hash/closure checks, native reconstruction/checking and current-use protection.
6. Checking an actual useful local instantiation or transport and later building any derived contribution.

Costs already paid by a warm client may be reusable only while their exact local guards remain valid. The broker does not replace step 5 or 6. In particular, it cannot convert an unfamiliar foundation into an adopted one, supply a local assumption, or make a statement useful merely by returning it.

Let `L_D` be the number of attempted candidate-source leads per investigation under design `D`. Exact expected lead work is `E[sum over attempted leads of their actual work]`; writing `E[L_D] c_lead` additionally assumes an appropriate common per-lead expectation. Stale expensive leads may be correlated with both later source failures and checking cost, so multiplying unrelated unconditional averages can be misleading.

BROKER1 can save server-side feature derivation and native evidence retention while increasing `L_D`. The first token-only lane can increase both cheap type probes and expensive failed acquisitions relative to a qualified source's pattern filter. Fresh source authorization is required even for an old broker listing. A maximum of four leads per row is not a maximum of four leads for an investigation: multiple rows, pages and replays share one owner-admitted aggregate budget. Retries and new broker hops cannot replenish that budget.

On insertion, count the producer's original local proof generation/checking and canonical export separately from replicated native qualification, broker metadata ingestion, postings, route placement and source disclosure. Removing six discretionary native index copies cannot erase the original producer's work. A broker's cheap admission also does not establish that any evidence source ever accepted the new publication obligation. Reciprocal accumulation requires actual supplied custody and later checked reuse, not merely a rising metadata-row count.

## Small known-contact fixture inside the illustrative broker stock envelope

This module-level fixture supplies a modest test case before extrapolating to full-corpus broker routing. It remains paper accounting, not an assertion that actual artifacts or a native implementation attain the declared bounds.

Use eight owner-chosen known broker contacts and two independently chosen complete native sources. Compare against eight known-contact qualified native indexes. No token-route publication is required on either side of this comparison. Begin a one-day interval with 4000 targets and admit at most 96 new targets, ending with at most 4096. Assume a 2-GiB shared core and at most 256-KiB disjoint additional native evidence per target, as in the larger fixture below. All clients in this particular experiment are warm for the complete core; cold onboarding is a separate charged experiment, not silently included in the warm success claim.

Each broker admits at most 4096 current identities, at most 8192 current/snapshot-pinned row versions, and 16 tokens per version in this fixture. Thus it needs at most 131072 retained posting entries, below BROKER1's illustrative 4194304-entry ceiling. If actual attributable metadata is at most 8 KiB per retained version, versions consume at most 64 MiB. Reserve at most another 64 MiB for retained fixed/control metadata and observe actual total allocation. This is below the illustrative 4-GiB stock limit; none of the eight snapshots, retired rows or lead updates receives uncounted storage. Admission stops if any bound is exceeded.

A sufficient *conditional* resident-memory allocation per broker is at most 128 MiB for its actual resident index/version/fixed state, at most `4 * 16 MiB = 64 MiB` for its four concurrent executions, and at most 64 MiB for all remaining queues, transport, result spools and control state. Their sum is BROKER1's 256-MiB illustrative limit. The actual native-free implementation must fit these allocations; canonical record size alone does not prove that it does.

At exactly attained evidence bounds, eight full native copies require 24 GiB and two require 6 GiB, avoiding 18 GiB of discretionary canonical native stock. Actual saved bytes use the actual closure unions. Each native source's at-most-3-GiB canonical stock fits H's illustrative 8-GiB native-retention allowance, but its native/collector peak memory still needs independent qualification. The 4096-target endpoint has no further headroom under that H target-count allowance; continuing growth requires additional supplied capacity or a different explicitly admitted scope, not indefinitely repeating this one-day fixture.

For a transparent recurring service envelope, let the entire investigation pool make at most 10000 attempts in an 86400-second interval, each using at most one new-snapshot broker page and one exact replay investigation. All source leads and native reads in that investigation share one aggregate admitted budget. Give each broker 3600 CPU-seconds, 16 GiB traffic and at most 20000 new paid broker executions per interval, and each native source 28800 CPU-seconds and 16 GiB traffic. The native traffic allowance is explicitly larger than H's illustrative 8-GiB/day slot allowance. These are actual proposed allocations to count, not new universal defaults or measured capacity. The cumulative CPU/traffic caps below permit all 10000 attempts to choose one node only under the additional temporal admission premises that follow; daily totals alone do not establish service or snapshot turnover.

### Snapshot stock and temporal supply

Use the separately proposed [direct-binding retirement contract](CP-001I-direct-broker-bindings.md): the hard maximum snapshot lifetime remains 600 issuer-local seconds, but an issuer may select a shorter lifetime and reports the actual expiry in its token. A committed END retires eligibility for new snapshot claims without destroying an independently retained immutable reply spool. MORE/PARTIAL, an abandoned continuation and a lost first reply can leave a snapshot charged until expiry. No new close opcode or client-acknowledged release is assumed here.

The following is one sufficient **paper workload**, not a qualified queue/scheduler implementation or an average-arrival argument. Measure time at the broker. Initially no snapshot slots from earlier work remain charged, and no unrelated user consumes these slots during the trace. Let the slot reservations for the 10000 new requests begin at `t_i = i * 8.64 seconds`, for `i = 0,...,9999`. If the pool divides among brokers, each broker receives a subsequence with spacing at least 8.64 seconds. Require:

1. Every reservation either creates its snapshot within two seconds or, if creation cannot complete, relinquishes its uncreated slot within two seconds. A queue, unredeemed offer or failed preparation cannot reserve a slot indefinitely while being omitted from occupancy.
2. Each created snapshot in this workload has issuer-selected lifetime **at most 60 seconds** from creation. No continuation, lost response, fresh client key or interval boundary extends it.
3. Any already claimed scan requiring the snapshot releases its snapshot references within at most two seconds after the original expiry. This conservative allowance covers a claim just before expiry; the one-page fixture grants no additional continuation calls merely by including this allowance.
4. Final slot reclamation finishes within two more seconds after eligibility has ended and the last permitted snapshot reference is released. Reclamation work, including failed/abandoned requests, fits the funded cleanup allocation below. Reply spools that survive independently remain charged in their own byte/control allocations; if a spool or stalled delivery retains a snapshot reference longer, this temporal premise has failed.

Thus each charged interval, from reservation through creation/orphan retention/last scan/reclamation, has length at most `W = 2 + 60 + 2 + 2 = 66 seconds`. All reserved-but-uncreated, live, orphaned and retired-but-unreclaimed slots count. Write `r_i` for actual release time, with `r_i <= t_i + W`, and use the half-open charged interval `[t_i,r_i)`. At every time t:

`S(t) = sum_i 1[t_i <= t < r_i] <= count{i : t - 66 < t_i <= t} <= ceil(66 / 8.64) = 8`.

This is the exact finite-spacing occupancy argument needed for the eight-slot cap. It does **not** depend on any page reaching END, a reply reaching its client, or any native investigation completing successfully. Early END retirement can reduce occupancy, but no such reduction is used in the bound. Work and retained allocations extending beyond the accounting interval remain charged; a new interval does not recreate a free slot or replenish the old execution's grant.

The assumptions deliberately exclude arbitrary bursts, preexisting residue and other slot users. If those exist, admit a reduced trace or supply their counted share; do not treat 10000/day as a service guarantee under them. The two-second creation/reference-release/reclamation conditions and required scheduling/admission opportunity still need actual qualification. A locally selected shorter lifetime supplies no theorem that every meaningful multi-page query can finish inside it; this fixture makes only one-page attempts, including unsuccessful attempts.

**Defeating long-lifetime case.** If every incomplete/orphan snapshot instead remains charged for the full 600 seconds, even zero creation/reclamation overhead gives sustained turnover at most `8 * 86400 / 600 = 1152` new snapshots/day. That cannot support 10000 new queries/day. At the 8.64-second spacing, full 600-second residence can require `ceil(600 / 8.64) = 70` simultaneous slots before overhead. More CPU or unused byte stock does not solve that stock-time conflict; actual shorter residence, fewer admitted new queries or separately supplied capacity is required. This countercase is why the 60-second workload premise is explicit rather than inferred from the hard maximum.

### Paid-execution and recurring resource counts

For each broker, count all new paid executions by operation, whether they succeed, fail, conflict, return PARTIAL or are interrupted after admission:

`N_exec = N_find,new + N_find,continuation + N_submit + N_withdraw <= 20000`.

These are disjoint operation counts. A failed submission is already in `N_submit`, not a free retry and not an extra double-counted failure category. Fresh retries increment the appropriate count; exact-action replay retains its existing no-reexecution semantics but its actual control/response work is still charged. Pre-admission refusals do not allocate a paid execution yet still spend their own funded control resources.

In this trace, `N_find,new <= 10000` and `N_find,continuation = 0`; failed new-query calls are included, not appended to a 10000-success denominator. To give both complete native sources a selected self lead for each of the at most 96 new candidates, reserve up to `2 * 96 = 192` submission executions per broker. Allow at most 400 further mutation executions in total, shared by replacements, withdrawals, failed/conflicting paid submissions and their freshly funded mutation retries. Thus `N_exec <= 10000 + 0 + 192 + 400 = 10592 < 20000`. Requests outside these counts are not promised by this experiment even though the protocol execution ceiling leaves headroom.

Each of the at most 192 publication submissions is budgeted at one CPU-second. Reserve another 500 CPU-seconds jointly for the at most 400 additional one-second mutations and at most 100 CPU-seconds of all remaining cleanup/control work, including snapshot reclamation. These are accounting/temporal premises to qualify, not measured per-operation costs. If extra queries or continuations are desired, their CPU, execution count, traffic and changed snapshot residence must all be re-admitted; the unused execution count alone supplies none of those resources.

The following are sufficient recurring accounting conditions, to be qualified on actual work:

| Supplied component | Explicit one-day inequality |
|---|---|
| Each broker CPU | `10000 * 0.25 + 192 * 1 + 500 = 3192 <= 3600` CPU-seconds; all publication, additional paid mutations, reclamation and other control work obey the preceding allocations |
| Each broker traffic | `10000 * 1 MiB + 192 * 8 KiB + 1 GiB < 16 GiB`; the final allowance covers all additional mutation/request/reply, authentication, failure, retry and control traffic actually incurred, including spooling/delivery overhead where transmitted |
| Each native source CPU | `10000 * 2 + 96 * 1 + 5000 = 25096 <= 28800` CPU-seconds; two seconds is the admitted total source-side work per replay investigation, one second the assumed warm incremental qualification cost, and 5000 seconds all other source work |
| Each native source traffic | `10000 * 1 MiB + 96 * 256 KiB + 1 GiB < 16 GiB`; each investigation has at most 1 MiB aggregate native payload across all of its lead attempts, and the remaining allowance covers other actual traffic |

These inequalities and the slot-residence premises together describe a sufficient bounded paper service case; neither alone proves useful operation. They do not prove any particular query succeeds. Work requiring a larger source stage is declined/deferred or separately admitted and then charged to a different experiment. Broken timing/source bounds, expensive malformed inputs, initialization, incident-driven requalification, peak native RAM and bursts cannot be hidden inside averages. Snapshot versions, orphan state, immutable reply spools, pending reservations, failures and cleanup remain inside the actual stock, memory and work limits. All actual native replicas, client checks, producer exports and allocated but idle headroom stay visible in the fair comparison.

The insertion saving is six discretionary qualifications per new target, hence at most `6 * 96 = 576` qualification events in this interval. Under the assumed one-second incremental cost, a workload with all 96 insertions has a 576-CPU-second gross saving. A positive CPU comparison additionally requires the actual sum of changed metadata/maintenance, source service and client investigation work to be less than 576 CPU-seconds; for example a proven combined increase of at most 300 leaves at least 276 CPU-seconds. The coarse service envelopes above do **not** prove that narrower cost premise. Stock separation is already a useful conditional I-E1 result, whereas the I-E4 useful-yield and end-to-end CPU comparison remain independent qualification questions.

This fixture's scope is an explicitly supplied known-contact panel. It establishes neither unfamiliar-broker discovery nor network-wide routing. The optional BROKER_ROUTE lane remains a separate unresolved proposal and is not needed to investigate this minimal service first.

## Larger extrapolation: more search copies than custody copies

Consider the following declared paper fixture, not an extracted corpus or an initial-profile capacity claim:

| Parameter | Assumption |
|---|---:|
| Selected targets | 1,048,576 |
| Shared complete native core per full source | 2 GiB |
| Disjoint additional native bytes per target | At most 256 KiB |
| Independently chosen complete search replicas desired | 8 |
| Required complete qualified evidence copies | 2 |
| New targets/day | 10,000 |
| Broker metadata allocation per target | Illustrative 8 KiB, to be qualified against actual retained allocations |

For the favorable known-contact variant, investigators are explicitly supplied an owner-chosen finite panel of these eight broker contacts, and comparable native baseline contacts. Neither design needs token-route publication for this experiment. The panel is not a mandatory global roster, privileged server or claim that an unfamiliar investigator can discover every broker. BROKER1 explicitly permits this direct-contact mode. Its initial illustrative envelope has 65,536 current candidates and 4 GiB total metadata: a million-target broker with the stated 8-GiB metadata allocation needs a separately supplied larger profile. No such operational qualification is claimed here.

Eight full qualified indexes would retain at most `8 (2 + 256) = 2064 GiB` canonical native stock in this fixture. Two full qualified sources retain at most `2 (2 + 256) = 516 GiB`. If the per-target bounds are attained identically, the avoided stock is `1548 GiB`, about `1.512 TiB`; for smaller actual closures, use their actual difference. This is not a guaranteed lower bound on savings from upper bounds alone.

Eight full brokers at the illustrative metadata allocation add `64 GiB` of broker-local metadata before separately charged routing, staging and fixed overhead. The native baseline also needs search metadata for its eight indexes. If comparable allocations are equal, that common component cancels. Differences in canonical copied leads, live snapshots, checked pattern bodies, custodian indexes and native eligibility state must be retained in the comparison rather than asserted equal.

For a new corpus, this layout uses `2N` instead of `8N` target-placement qualification events, with actual costs as above. For steady insertion it avoids `(8 - 2) 10000 = 60000` discretionary native target-placement qualifications/day. It does not reduce final clients' required native checking or the two retained sources' qualification obligations.

This is a genuine favorable *replication separation* when all the following conditions hold:

- Eight-way search coverage is useful to the declared investigations, while two complete native sources meet the independently stated evidence-recovery requirement.
- Broker metadata is much smaller/cheaper than complete native qualification and retention for this corpus.
- Sources supply the increased acquisition load and required warm/cold locality; the source reduction is not concealed as a bandwidth gain.
- Extra false-lead, recontact, route, freshness and client-native work stays below the coordinate-wise savings and every required peak/service constraint is met.
- The selected broker profiles actually admit the full metadata/posting/snapshot/maintenance load, or explicitly partition it with all extra stock and coverage effects counted.

For CPU sensitivity only, if the real incremental qualification cost were one CPU-second, the saved insertion term would be 60000 CPU-seconds/day. At two million investigations/day, each additional `0.03` client CPU-seconds/attempt would consume that entire term before any extra maintenance or source work. The example shows how little repeated per-query waste is needed to erase a large insertion saving; neither the one-second cost nor the query overhead is a measured value.

The eight original native sources also supplied eight places to obtain evidence. Two retained sources do not preserve eight-source failure tolerance or serving capacity. The favorable comparison preserves a declared two-copy minimum, not an unstated equivalence of these different services. Owners needing eight independent evidence recovery domains should keep eight evidence copies and expect no saving from deleting six of them.

## Full-corpus broker routing is not free

The minimal proposal uses a distinct broker key/ad/service role and ordinary bounded **ungrouped** placement/renewal. It does not reinterpret native K4/ProviderAd2 eligibility and does not inherit H's native FULL_FEATURE group renewal or SharedFeatureCover contract. A later grouped broker profile would need a separately specified and audited mechanism. No such improvement is included here.

For the preceding million-target fixture, suppose each target contributes eight common tokens and eight target-specific tokens, and every one of the eight brokers indexes the whole corpus. The token union per broker is

`U = 8 + 8N = 8,388,616`.

With four selected holder copies per advertised broker/token pair:

- `8U = 67,108,928` broker/token ads;
- `4 * 8U = 268,435,712` chosen route rows;
- at an assumed 1 KiB stored ad allocation alone, `256.000244140625 GiB` aggregate chosen-row bytes;
- with twice-daily ungrouped row renewal, `536,871,424` row-renewal operations/day, approximately `6213.79` per second fleet-wide;
- at a separate assumed 1 KiB total request/reply payload per unchanged renewal, `512.00048828125 GiB/day` before authentication, connection setup, retries, markers or repair.

Both 1-KiB assumptions are sensitivities, not BROKER1 size guarantees or measured transport costs. Each distinct row renewal remains an admitted operation even if an implementation amortizes some transport setup. Retired/uncertain records, higher-depth markers, revisions, snapshot stock and holder refusals add work. Native eligibility checks may be absent from broker renewal, but the row count is not.

The same number of frontends and token coverage need not entail the same renewal count under the native baseline's already selected grouping mechanism. A fair comparison must compute each design's actual selected scopes/groups and holder occupancy; it cannot charge native renewal once per row merely to make BROKER1 look equivalent. Conversely, a hypothetical million-target native scope also exceeds H's initial capacity and must not be granted free.

This routing stress case differs from H's sharded two-copy fixture, which has `16,785,408` provider/token ads and `67,141,632` four-copy route rows. Eight full-corpus brokers do not directly improve that two-copy deployment: they buy a different number and distribution of searchable copies, repeat provider/token coverage and introduce their own maintenance.

Direct service at an explicitly selected admitted contact, as permitted by the companion contract, can avoid token-route publication for that broker. Such a deployment must state how investigators actually obtain those contacts and measure the resulting coverage, skew and failure modes. It cannot claim routed global discoverability for unadvertised tokens. Nor can a single mandatory contact list or seed silently become the system's required central server.

Thus the positive stock example is not by itself a positive whole-system result. If full token routing is required, its ungrouped maintenance must fit real supply and the complete break-even inequality. An infeasible initial broker profile yields partial/smaller scope or a separately qualified larger profile, not a fictional full index.

## H-like redistribution: core locality versus concentrated source load

H's selected paper workload already has exactly two qualified target placements. Replacing its search indexes with brokers while retaining those same sources does not remove either required evidence copy. In that case the advertised native-retention/qualification saving from reducing eight search copies to two does not apply.

A different, explicit redistribution can reduce duplicated shared support by concentrating the same two target copies in fewer sources. Keeping H's `1,048,576` targets and `2N` total qualified placements but reducing serving slots from `1024` to `64` changes the common-core component from `1024 * 2 GiB` to `64 * 2 GiB`. This saves `1920 GiB` only if each source genuinely needs one full 2-GiB core and the old independent copies can actually be avoided/released. Total target increments remain up to `512 GiB`, and target-placement qualifications remain `2N`.

The mean targets per source rise from `2048` to `32768`. With exactly attained 256-KiB increments, each source's canonical native stock rises from `2.5 GiB` to `10 GiB` before metadata/workspaces. The latter already exceeds H's illustrative 8-GiB native-retention slot ceiling and target-count ceiling. It needs a genuinely larger source profile and independently qualified peak native memory, not just a new sharding label.

Each retained source also bears sixteen times the former mean target-serving load under equal demand. If the 8-GiB/day traffic allowance per source stays unchanged, aggregate serving supply falls sixteenfold from `8 TiB/day` to `0.5 TiB/day`. Delivering a 2-GiB core to each of 100000 cold clients then has the following ideal lower bounds:

`100000 * 2 GiB / (1024 * 8 GiB/day) = 24.4140625 days`,

`100000 * 2 GiB / (64 * 8 GiB/day) = 390.625 days`.

To preserve the former aggregate `8 TiB/day` using 64 sources, each needs `128 GiB/day`, before ordinary traffic/skew and with enough native/checking/connection capacity to serve it. Independently supplied caching or extra byte-serving peers can alter this budget only with an explicit compatible serving contract and actual resource supply; metadata brokers do not provide that service in the first lane.

The consolidation may be a good choice for capable archives and a bad one for many ordinary hosts. It trades duplicated core stock for concentrated service, larger peak working sets and potentially correlated loss. It is not a proof that decentralization requires one layout or the other.

## Warm and cold acquisition are different workloads

A warm client's actual missing closure may be a small unique target increment. A cold client may require most of a large support library, a newly adopted exact foundation and an expensive native environment reconstruction. A heterogeneous client may be warm for another incompatible realization but still cold for this replay. A byte hit without valid native qualification/current-use guards is not necessarily a checking hit.

For client `a`, separate two obligations:

- `MissingBytes(a,R)` consists only of required exact encoded object/range bytes that no admissible retained local byte path can supply after permitted local integrity checks. Bytes which are already present and hash-correct do not enter this set merely because native qualification or protection is absent.
- `NeedsNativeCheck(a,R,context,policy)` consists of the actual reconstruction/checking/assumption/protection/current-guard obligations not discharged by reusable local qualified state. These obligations can refer to completely present local bytes. They are not a network-missing-object set.

For the fixed native transfer coding, acquisition must supply the actual externally missing bytes and its required framing; any lower bound on network transfer uses `MissingBytes`, not the size of `NeedsNativeCheck`. If local bytes are present but their integrity has not yet been checked, checking that integrity locally may remove any need to transfer them. Disk reads, hash verification and native replay still cost resources. Native work depends on the actual reusable qualification and realization, not solely on missing byte size. Invalid, aborted and expired stages add real costs even when they never become protected results.

A broker cannot reduce either obligation merely by listing the replay more often. It can help discover a genuinely smaller suitable replay, a better-located permitted source or a useful already-cached target, but that is an explicit workload-dependent selection benefit to measure. An alternative proof may need a different support closure; relevance and locality cannot be inferred just from equality of terminal statements.

For any set of cold clients whose required evidence must cross a given supplied cut, transfer completion time is at least required cut-crossing bytes divided by actual available cut capacity, before retries or other traffic. This is a simple resource lower bound, not a prediction of a decentralized protocol's completion time. A warm-only evaluation that omits onboarding does not establish long-run usability for new participants.

## Evidence availability: more catalogs do not manufacture more proofs

Fix one investigator, its budget and current policy, one exact useful replay and a finite observation interval. Define:

- `D`: discovery returns that candidate within the admitted search budget;
- `E`: after discovery, the investigator can actually acquire the complete exact required evidence through allowed concrete native source scopes within the remaining admitted acquisition budget;
- `K`: native compatibility, complete checking, actual assumption accounting, protection and current-use guards succeed;
- `U`: the resulting checked artifact has a useful checked local application for the investigation.

Define success for this broker-mediated attempt as `S = D and E and K and U`. Then the exact chain rule is

`P(S) = P(D) P(E | D) P(K | D,E) P(U | D,E,K)`

whenever the conditioning events have nonzero probability; equivalently use the ordinary joint event with zero-probability cases assigned zero contribution. This is not an independence assumption. The probabilities refer to a declared workload/failure model or empirical distribution, not objectively known constants for all mathematics.

More broker copies may improve `D`, while concentrated evidence custody may reduce `E` and extra false leads may exhaust the budget before either. An inapplicable but perfectly valid theorem has `K` without `U`. An authenticated fresh endpoint can fail `E` for an exact replay. The trust-boundary note's `EvidenceReadObserved` establishes only the exact successful CIDs/ranges and observation interval, not the rest of the closure or future service.

For an explicitly idealized independent static model, if `b` broker replicas each independently supply a correct discoverable entry with probability `p_b`, and `e` complete sources independently supply the entire usable evidence within budget with probability `p_e`, then

`A_discovery = 1 - (1 - p_b)^b`,

`A_evidence = 1 - (1 - p_e)^e`.

Even in that idealization, success is at most the smaller of these availabilities and additionally requires checking/application. Their product requires independence between discovery and evidence events as well. Per-source `p_e` includes the complete usable closure and service budget, not mere process uptime. The model assumes the sources are actually named/reachable within the client's permitted leads; a large fleet of unlisted sources does not enter this union for free.

For example, under the artificial per-source `p_e = 0.95` model, two complete sources give `0.9975` evidence availability, while eight give `1 - 0.05^8`. The eight-source case requires an actual permitted discovery/lead path reaching all eight within budget, such as several broker snapshots with different selected lead sets or independently known native contacts. It cannot be obtained from one four-lead row. Reducing eight sources to two does not preserve the latter value even if there are millions of broker replicas. These figures illustrate the model only and are not a measured reliability statement.

Real failures can be strongly correlated: shared administrators, power/network domains, one lost core, the same native checker defect, a common policy suspension, a single foundation incompatibility or a partition cut. Distinct contact keys do not establish independence. Replicating metadata across independent operators while keeping one irreplaceable evidence custodian leaves that custodian as a single point of evidence failure. Keeping several full closures all dependent on one irreplaceable shared external byte source is not several complete independently retained closures.

With several sources whose available chunks can actually be combined under existing exact CID/range/scope rules, evidence acquisition can succeed without any one source serving every requested byte during the interval. Account for the actual union, compatible authority and transfer budget. The minimal lane's qualified-source retention contract is not weakened by that client-side transfer optimization. A sum of partial observations is not complete custody until every required object is actually covered.

Availability is therefore an explicit supplied recovery property, not a mathematical vote. Identity can help distinguish contacts and enforce bounded local admission, but no political attribution system is required for the receiver's native acceptance boundary. When an availability model needs independent domains, it needs evidence/assumptions about those domains, not simply a count of keys.

## Freshness is a separate service cost and observation grade

A live broker snapshot and renewed broker ad establish only that its metadata service remains available under its own scope. They do not renew a native source's PUBLIC_SERVE eligibility, source evidence pins or an export lease. The source's present willingness, retention and applicable native state must be obtained through its own contract.

If an operator voluntarily checks every copied entry's one selected source individually once per interval `tau`, the attempted status-probe rate is `r_m N / tau` before retries and extra leads. With `N = 1,048,576` and `r_m = 8`, this is `8,388,608` probes per complete sweep. Checking all four leads multiplies that example's count by up to four. Overlap between entries, common endpoints or source batching may reduce work only where an actual specified query and observation semantics supports it; an endpoint ping does not establish that every replay at that endpoint is still retained.

BROKER1 does not promise a complete periodic availability audit of its listed evidence. On-demand source contact can shift freshness cost to investigators. This may be desirable for rarely accessed entries, but frequent repeated queries and negative-cache expiry can make the shift expensive. A recorded successful read remains scoped to its actual CIDs/ranges and past interval; calling it a "fresh proof availability certificate" would overstate its evidence.

Negative caching must similarly distinguish exact malformed data from unavailable sources, temporary budget exhaustion and local incompatibility. Its byte/time/query budget and loss of useful retry opportunities are real tradeoffs. A false positive candidate can be safe but costly; treating all false leads as harmless because mathematical acceptance remains guarded confuses safety with usability.

## Defeating workloads and what each one disproves

| Workload | Why the broker separation may lose |
|---|---|
| Baseline already has exactly the required two evidence copies | Native retention and replicated qualification cannot be removed; new brokers are additional discovery supply |
| Broad common tokens; native pattern filtering is effective | Token-only brokers shift many irrelevant leads, type reads and rejected native acquisitions to clients |
| Tiny cheap evidence; large descriptor/lead/posting state | Metadata, snapshots and route fanout can cost more than the native duplication avoided |
| Large cold shared support with many newcomers | Custodian-to-client transfer and local native reconstruction dominate; metadata replication does not reduce them |
| Many brokers, two underprovisioned sources | A larger query frontier overloads the same source CPU, bandwidth, connection and export budgets |
| Many stale, syntactically plausible or dishonest claims | Safe rejection still spends finite client/source resources; listing growth can reduce useful yield |
| Aggressive full freshness sweeps | Probe load approaches metadata-copy count times corpus size, without proof of complete future availability |
| Distinct foundations/realizations with poor cache locality | Canonical overlap may not provide usable native qualification or a small local application closure |
| Full replicated broker indexes and canonical prefix paging | More peers may return the same candidates; replication does not by itself provide diverse recall |
| Ungrouped token routes at large scale | Renewal and holder stock can dominate, while native grouped maintenance has an existing advantage |
| A shared evidence outage or checker suspension | Independent broker uptime cannot restore unavailable or currently unusable evidence |
| Stopped or reduced hard investigations | Lower resource use merely reflects less useful work, not an equal-service efficiency improvement |

These are not arguments for banning brokers. They delimit the claims that can be made from a smaller metadata object or a preserved acceptance predicate. A useful architecture can retain direct qualified indexes for some corpora/workloads and use candidate-only brokers for others.

## Required qualification evidence before selecting this lane

For a declared diverse finite pool of local investigations, without a mandatory public goal registry, collect or establish the following before making an operational superiority claim:

- Exact target/replay/foundation scope and actual native closure unions, including common support and replay alternatives.
- All retained native/index/broker allocations, route rows/groups/markers, snapshots and retirement stock, with independent physical failure domains disclosed.
- Warm, cold and incompatible-foundation cases; actual incremental native work and peak reconstructed/collector environments, not disk-byte proxies.
- The complete query funnel: attempts, returned duplicates, lead attempts, scoped source-read observations, complete acquisitions, rejected checks, useful checked applications and later useful contributions.
- Actual token-only versus native pattern-filtering cost/recall under the same declared corpus and supplied budgets.
- Source serving and onboarding capacity after any redistribution; burst/queue/deadline behavior and aggregate client limits.
- Publication, insertion, routing, renewal, freshness, failure suppression, repair and migration costs, including unsuccessful work.
- Correlated source loss, one shared-core loss, stale metadata, custody withdrawal, provider refusal, source-scope mismatch and malformed claims.
- A clearly stated recovery/service requirement that the new design still satisfies, plus honest differences where it deliberately provides a weaker or stronger service.

Useful aggregate measurements include total resources per checked useful application and per subsequently checked useful contribution, but they require nonzero denominators and should not conceal the investigation distribution or latency tail. Failed, expensive and abandoned attempts stay charged. Corpus-size growth and broker-listing growth are not substitutes for these outcomes.

Concept decision: BROKER1 is a plausible optional search-role separation, especially for replicated/specialized discovery over expensive native evidence with adequate independent custody. It is not a general proof of lower cost, global awareness, durability, complete search or exponential mathematical growth. Selection requires its service contract and the favorable workload inequalities to hold together. Until then, the qualified native index/custody path remains the operative baseline.
