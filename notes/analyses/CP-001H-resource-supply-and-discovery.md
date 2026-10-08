# CP-001H: supplied indexing, shared feature coverage, and the economics of unfamiliar reuse

Date: 2026-09-20. Status: selected concept amendment and analytic workload with [independent paper/accounting review](../audits/CP-001H-resource-cross-audit.md). No implementation, simulation, protocol execution, native run, or throughput measurement. Frozen F/G documents remain unchanged.

## Outcome

The v4 acceptance boundary is not by itself an efficient large-network operating plan. In particular, placing each 128-target FULL_FEATURE scope independently does not automatically scale to a million-target retained library: scopes repeat common keys, one provider/key row cannot belong to several groups, and many small scopes can destroy the intended lease-group amortization.

Select an **owner-local shared feature cover**, with one accounted publication owner per provider/token, and **size-tiered immutable scope consolidation**. These use the existing typed feature ads and holder-group operations; they add no global registry, server, research-task system, new mathematical authority, or new wire opcode. Individual G scopes that borrow coverage remain PARTIAL under G's original meaning. A new explicitly local aggregate predicate reports coverage across their actual owner rows.

The practical supplied role is a collection of bounded, independently operated **qualified index/custody slots**, supported by separate routing holders and many smaller investigator clients. A million-target library is explicitly partitioned among such supplied slots or admitted by a correspondingly larger provider. Downloading the framework is not a promise that every laptop stores or indexes every proof.

This repairs avoidable metadata/renewal amplification. It does not establish useful recall for a nondiscriminating token, cheap proof checking for every mathematical development, free global synchronization, or exponential growth without commensurate supply.

## Frozen contracts used

The analysis uses the complete relevant contracts in [F routing](CP-001F-dissemination-and-routing.md), [F exact coverage](CP-001F-exact-routing-coverage.md), [F economics](CP-001F-operability-and-index-economics.md), [G STRUCT2](CP-001G-structural-retrieval.md), and [G typed bindings](CP-001G-profile-and-consumer-bindings.md).

Important numerical constraints are actual constraints, not measured service rates:

- STRUCT2 emits at most 32 tokens per target. Its initial FULL_FEATURE scope has at most 128 targets and 4096 token memberships; larger local scope/index capacity must actually be supplied.
- A provider has one row per exact `(K,providerNodeID)` in a cell. A row has one group/ungrouped owner. Different groups cannot silently share its ownership.
- A chosen placement seeks four copies among at most 16 selected holders. Each cell admits at most 4096 provider ads. Deeper cells require separately maintained ancestor markers.
- One bounded group batch has at most 64 mutations and 64 KiB total control body; the byte ceiling can reduce the mutation count. A group can have at most 65536 members under the supplied fine-holder profile.
- Leases are at most 48 hours. The illustrative refresh policy is twice daily. Group renewal does not renew ancestor markers.
- The initial fine source has 4096 aggregate exact targets, 32768 total group records/reservations, 96 MiB publication metadata, and a daily envelope of 131072 operations, 1 GiB traffic and 3600 CPU-seconds. Those are not automatically suitable for a larger structural index.
- The routing holder's example aggregate is 65536 ads and 384 MiB routing storage, with its group/control/snapshot stock counted inside actual supply.
- A G interactive structural attempt has at most 16 cell lookups, 24 provider pages, four concurrent peers, 8 MiB discovery traffic, 32 initially inspected candidate types, two local CPU-seconds and ten wall-seconds. None is a guaranteed latency or recall result.

Existing schemas and foundation bindings remain exact. In particular, ProviderAd2 anchors a PublicIndexDescriptor3, whose structural hint binds the actual StructuralDescriptor1 and InstanceReplay3. A routing holder does not acquire the mathematical closure merely to store that record.

## Three roles, and the nonfree boundary between them

| Role | Supplies | Does not imply |
|---|---|---|
| Theorem custodian | Retained exact native objects/replays or an explicitly authorized archive scope, protection and repair capacity | That merely stored bytes are checked, well indexed or useful to a query |
| Qualified mathematical index provider | Checked, currently eligible public targets, their complete selected retained evidence, structural descriptors/postings and funded FIND service | That its index is globally complete, or that a remote client may trust its verdict |
| Routing holder | Typed signed provider metadata, group leases, bounded route lookup/list service and routing maintenance | Native adoption, proof custody, proof checking or mathematical relevance |

The roles can coexist on one machine, but their allocations add. Deduplicated shared storage is charged once only when it is really the same owner-controlled retained allocation; independent promises and service work still remain distinct obligations.

Under frozen G, a qualified index provider cannot discard its complete checked closure and retain only a descriptor while continuing to assert a currently native-eligible public root. A metadata-only third-party index could be a useful later protocol, but requires an explicit untrusted descriptor-to-custodian service contract. It is not smuggled into this amendment by renaming remote custody as local retention. The worked deployment therefore counts native evidence at its qualified index slots. Additional archival custodians may provide byte redundancy separately.

Most investigators need not be reachable routing servers or permanent index providers. Their finite local caches and selected imports still incur native acquisition/checking costs. Provider identities authenticate replacement authority; no calculation treats different keys as proven independent failure domains.

### Architecture limit: full-checking index providers are a substantive cost choice

Requiring every qualified mathematical index provider to retain/check the complete native closure is stronger than what is needed to protect a client from accepting a false **candidate**: an untrusted search broker could, in principle, return a useful pointer whose entire evidence the client then checks independently. The present coupling buys a simple honest producer/availability contract, but can duplicate expensive checking, common support and custody across many indexes. Its optimality is not established.

A future metadata-only broker should be evaluated as a distinct candidate service: an exact bounded descriptor, explicit named acquisition providers, no false claim of local PubliclyServed/native eligibility, limited untrusted ingestion, and independent client acceptance. Such a broker would also need an explicit protocol for scoped listing, false-lead control, update/withdrawal observations, routing advertisements and resource obligations. An attested remote checker or SNARK might reduce some repeated checking cost only under its exact adopted proof relation, implementation and cryptographic assumptions; it does not guarantee that proof bytes remain available, that metadata are relevant, or that the claimed input statement is the client's intended one. None of these future options is part of the current cost case or an undeclared reinterpretation of G's provider records.

## Distinguish four stocks

For provider p, let its exact currently selected public target set be T_p. Each target t has a completed deterministic selected feature set F(t), with cardinality at most 32, under one fixed foundation/extractor. Define

\[
P_p=\sum_{t\in T_p}|F(t)|,\qquad
U_p=\left|\bigcup_{t\in T_p}F(t)\right|.
\]

P_p is the target/token **posting** count. U_p is the provider/token **route-ad** count. Neither is the number of proof objects or the byte size of the full native closure. Several proof alternatives or replay contexts for one target require their actual distinct evidence/descriptor accounting; they do not automatically create new provider/token routes.

With r=4 chosen depth-zero copies, settled route membership stock is r times the sum of U_p over providers. It is not r times the global distinct-token count: different providers have different signed ads. It is also not r times the sum of P_p, because one provider's many matching targets share a route row.

The complete stock includes, separately:

1. Native unique retained objects and actual selected replay/representative contexts.
2. Per-target descriptors, optional local pattern material, postings and exact reverse incidence.
3. Provider/token advertisements, chosen/partial/transient replica rows and group map/receipt state.
4. Live and retired groups, snapshots, unresolved operations, marker paths, routing contacts, query cursors and actual protection/repair obligations.

Deduplication in one stock does not erase the others. A common token can save route rows while still having an enormous local posting list.

## Why independent tiny scopes fail as the general operating plan

### Ownership collision

Suppose targets a and b lie in two immutable 128-target G scopes, and both emit token k. Both scopes use the same provider identity. At the same cell/holder, their planned rows have the same `(K4(k),provider)` key. The second group's PUT fails with ROW_OWNER_CONFLICT. Replaying the first ad or copying its receipt cannot make the row a member of the second group. Its lease, membership root, eligibility summary and delayed reclamation fence have exactly one owner.

Thus “divide a million targets into 7813 scopes and declare every scope FULL_FEATURE” is not an established compositional construction. It needs an explicit sharing rule at the producer's coverage layer, rather than dual row ownership at the holder.

### Group multiplication

Even disjoint new tokens can be costly. For one scope with u owned tokens spread over M holders, selected group count is at most min(M,ru), and can be close to ru when ru is small relative to M. With many scopes, the bound is the sum of these quantities, not min(M,r times total U).

Under an explicitly idealized model where each independent key chooses r distinct uniform holders, the expected number of nonempty groups for that scope is

\[
\mathbb E G(u)=M\left(1-\left(1-\frac rM\right)^u\right).
\]

This is an occupancy calculation, not a measured DHT balance result. Actual hot keys, correlated placements, refusals, extra copies and empty/retiring groups must be counted. For ru much smaller than M, the expression is close to ru; a small group saves almost no renewal calls.

A provider with 2048 targets, eight target-specific tokens each, M=20000 and sixteen independent 128-target scopes has roughly sixteen times G(1024), about 59000 nonempty groups before small common-key adjustments. One consolidated owned set with approximately 16392 tokens has about 19250 groups in this same idealization. The original 32768-source-group default does not support the tiny-scope estimate. Larger libraries make the difference more severe.

## Selected repair: a provider-wide shared feature cover

### Exact local state

For each provider/foundation/extractor, maintain a receiver-owned finite ledger with:

- Completed public descriptor versions, exact target/token incidences and current native/public eligibility guards.
- Immutable G FeatureScopes, each retaining its exact target list and emitted-token union. Scope size remains bounded by the actually supplied profile; H explicitly supplies larger scopes where stated.
- For every settled covered token k, exactly one **publication owner scope** S(k), a selected currently eligible anchor target/replay in S(k) that emits k, and the exact existing group/cell/row references that realize its selected copies. A handoff instead records one intended next owner plus each row's actual old/new group/scope owner and exact transition state; intent never overwrites the observed old owner.
- Each selected target-scope's token obligations, expressed by references to these owners rather than extra copies of their rows.
- Current placed/pending/withdrawn/borrowed status, actual observation ages, in-flight handoffs, resource charges and coverage counters. No unsupported historical receipt is treated as live service.

An owner scope may own only a subset of its emitted union. Its ordinary G groups contain only those actual owned rows. That scope remains PARTIAL under G's own FULL_FEATURE accounting if its other tokens are not placed by it. Nothing changes the remote group mode, scopeID grammar or frozen completeness assertion.

Define the new local predicate `SharedFeatureCover(T_p,C)` at one owner observation cut C:

1. Every selected t has a completed currently eligible descriptor under the exact foundation/extractor and an exact current F(t).
2. For every k in F(t), the ledger references one publication owner S(k), and k really belongs to that scope's emitted union.
3. The owner's selected anchor is currently public/native-eligible under its exact replay and remains in that scope. Every recorded row/ad/root-hint binding uses that same token/foundation/extractor/anchor correctly.
4. The provider's actual FIND index contains t in k's posting at the stated index cut, irrespective of which scope owns k's route row.
5. The stated selected-copy and required marker observations exist with disclosed ages.

Every clause is required to assert the settled predicate. A failed or unresolved clause prevents that assertion and yields the appropriate PARTIAL, DEGRADED, TRANSFERRING or UNKNOWN local status with the unmet obligations identified.

This is a finite **local observed-coverage assertion**, not a global liveness certificate. It inherits F/G's actual route, overlap, current service and client budget assumptions. It is not serialized as a new mathematical object or inferred from one foreign aggregate digest.

The mathematical reason sharing is legitimate is simple: a K4 ad routes to the provider's matching public collection, not to a theorem-exclusive service. A subsequent conjunctive FIND filters the provider's real target postings. A provider whose existing route token now also indexes a new target can serve that target without creating a second identical route row. The exact old anchor can remain unchanged while another matching target becomes discoverable.

**Conditional preservation of the discovery path.** Fix t and a transmitted STRUCT2 predicate whose required tokens are a subset of F(t), with compatible permitted pattern view if a pattern is supplied. Assume the selected target/index entry remains eligible through the relevant provider snapshot, its borrowed owner rows and marker paths satisfy F's actual route-overlap premises, and the reader/provider fund enough routing and posting/pattern progress to reach that entry. Routing on any one required token reaches the same provider regardless of whether t owns that row. The provider's exact postings and predicate then include t, so complete scoped progress can return its candidate descriptor. This argument changes no mathematical acceptance condition and supplies no finite-budget recall guarantee: pattern-work exhaustion, a passed snapshot boundary, expired service or an insufficient reader budget can still prevent return. It establishes only that sharing a valid provider-level row does not itself delete the target's otherwise valid candidate path.

### Incremental contribution

For a newly checked selected target t:

1. Acquire/check/protect its actual incremental evidence and any missing shared closure under the native contract.
2. Extract F(t), insert its bounded descriptor/pattern/postings and exact reverse dependencies in one admitted index transaction.
3. For k already covered, add only the actual target/token incidence and owner obligation; do not rewrite a still-eligible route anchor merely because a newer theorem exists.
4. For each genuinely new provider/token k, allocate one publication owner and actual four-copy placement work. Pending placement remains visible.
5. Publish aggregate coverage only after its exact prerequisites are met. Local acceptance and posting insertion alone do not create remote placements.

If the new result's tokens are all already covered, routing membership work can be zero. Native proof work and local postings are not zero. If every new target introduces 32 fresh tokens, fine-route stock grows by up to 32 ads and 128 chosen copies per target per provider, before transients.

### Eligibility, anchor retention and withdrawal

An owner retains the anchor's actual needed evidence while using it for publication. This is a counted retention choice, not a right to prevent user withdrawal or to preserve an invalidated proof as usable. A stable qualified eligibility summary may accelerate renewal only when every relevant membership root, anchor, policy/incident dependency and public guard still matches.

If the anchor changes, prefer an eligible emitting target already in the same owner scope, and replace the signed ad/replay chain through the ordinary revision rules. If only another scope supplies an eligible anchor, transfer the key's publication ownership to that scope through funded old-row removal/new-group insertion. Same cell/provider rows cannot coexist under both owners. Move replica holders sequentially and disclose the gap at each holder; surviving other copies provide coverage only while they actually remain reachable/current. During a mixed old/new-scope placement, record TRANSFERRING/PARTIAL rather than the settled single-owner SharedFeatureCover predicate. The actual mixed rows may still provide useful discovery; partial bookkeeping is not a claim of global physical outage. Settle S(k) only after the required selected rows bind the new owner with the stated current observations. Old rows/groups/anchors/snapshots remain accounted through their actual withdrawal or expiry/reclamation. Neither historical snapshots nor four identities prove uninterrupted availability.

If no eligible anchor remains, stop renewing that key, mark its dependent obligations degraded, and fund withdrawal/expiry/reclamation. Targets removed from the selected current index cease being current obligations; remaining targets using the same token still need a valid owner. One last surviving unrelated token cannot justify renewing an obsolete group member.

Groups retain their frozen source rule: every grouped token must be supported inside that group's exact scope. The shared ledger does not permit an unrelated external anchor to satisfy that rule.

## Selected repair: counted size-tiered consolidation

The shared ledger prevents duplicate ownership but does not by itself eliminate tiny owner groups. Select a local size-tiered policy resembling immutable index-run consolidation:

- A newly admitted target can begin in a singleton scope, so it need not wait days to fill a 128-target batch. Several actually simultaneous admitted targets may start in a bounded batch.
- In the insertion-only baseline, maintain at most one completed owner run at each power-of-two target size. Merge two equal-sized runs into their exact target union. Complete target/token extraction results may be reused only under their unchanged validated identities/guards; constructing new lists/unions/hashes still costs work.
- The new immutable G scope contains the union's full actual target/token set. Transfer precisely the owned keys of the old runs; keys owned by other runs remain borrowed. Old groups remain counted until actual closure/reclamation.
- At most one consolidation handoff per supplied slot is active in this example. New work queues, current and replacement scopes, uncertain mutations, rows and snapshots share explicit aggregate ceilings. Exhaustion delays consolidation/publication or triggers a supplied new slot; it never invents another free queue.
- Native theorem objects and public target postings do not need rewriting merely because route-group ownership is reorganized. Conversely, native policy/representative changes are not justified by an index consolidation.

Every transfer uses existing G group OPEN/BATCH/CLOSE and exact row-ownership fences. At one holder it must drop the old owner before inserting the new owner. The implementation may preserve other actual replica placements during that funded transition; it cannot pretend to have a new make-before-break primitive at the same holder.

For insertion-only, fixed feature sets and no independent anchor/policy churn, a target participates in at most O(log N_p) equal-size merges. Assign a newly covered token to an actual first supporting target/run and move it only when that run merges. Its row migrations are then at most O(log N_p) over that growth history. This is an amortized accounting fact, not a per-contribution latency bound. A power-of-two boundary can trigger a large paid burst. Withdrawal, scope splitting, failed handoff and incident repair add separately measured work and are outside this simple amortized bound.

At a settled cut there are at most `floor(log2(N_p))+1` occupied size levels; temporary parent/new runs and pending singleton scopes need additional counted stock. A million-target provider can therefore avoid 7813 permanently tiny owners, but it must supply large immutable scope lists, their union/posting work, enlarged source metadata and actual holder groups. It cannot fit that deployment into the original four-scope/128-target interpretation by wordplay.

## Cost equations for warm operations

Let d be the bytes of newly required native objects after qualified warm reuse, c_native their actual checking/composition cost, f=|F(t)|, nu the newly introduced provider tokens, L(k) actual holder-discovery calls for a new token, g_new newly opened holder groups, b actual bounded mutation batches, and h actual marker/repair work. Then a warm contribution's work includes

\[
W_{contrib}=W_{native}(d,c_{native})+W_{extract}+W_{postings}(f)
+W_{route}\left(\sum_{k\ new}L(k),\;r\nu,\;g_{new},\;b,\;h\right).
\]

The plus signs combine additive dimensions of a resource vector, not peak memory. Concurrent working sets and admission deadlines require separate inequalities. Complete cold shared support is not included in d unless it is actually already present, qualified and protected; otherwise it must be added.

For unchanged depth-zero placement, one renewal pass needs one operation per actual active owner/holder group, not per target or posting. With refresh period tau and G_p active groups,

\[
R_{renew}=\sum_pG_p/\tau.
\]

Eligibility revalidation, transport/authentication, group retention byte-time, directory refresh and replica repair remain additional work. If exact eligibility summaries become dirty, a large scan cannot be hidden inside an alleged constant-cost renewal. Deeper markers need their own renewals; shared holder-side marker storage does not make every provider's refresh request free.

For one token ownership move across r already known holders, the basic row work is r old deletions and r new insertions, plus necessary group opens/closes, bounded batch transactions and actual replay/reconciliation. It does not require a new DHT lookup if the exact holders remain useful, but later routing convergence/placement repair remains separately supplied. A 64-row batch amortizes calls only when those rows share the same destination/group and its byte limit; hashing 64 unrelated keys does not guarantee one batch.

A query pays for actual route discovery or cached leads, provider pages, candidate-type reads/instantiation and final selected native acquisition/application. A 24-page ceiling says nothing about how many useful candidates exist, which 32 types are inspected, or whether their closure fits.

## A consistent million-target paper workload

This is a deliberately stated analytic capacity case, not a generated corpus or measured performance claim. Future qualification must either produce real native fixtures with these incidences/costs or report that the case's premises fail. In particular, the feature-incidence assumptions are not asserted for mathlib.

### Population and target incidence

| Quantity | Selected workload value |
|---|---:|
| Distinct selected mathematical targets | 1,048,576 |
| Investigator clients | 100,000 |
| Qualified index/custody slots | 1,024 |
| Target copies at qualified slots | 2 per target |
| Targets per slot at the initial cut | 2,048 |
| Routing holders | 20,000 |
| Tokens emitted per target | 16: eight shared common tokens plus eight target-specific tokens |
| Chosen depth-zero route copies | 4 per provider/token |
| Unknown-lemma query attempts | 20 per client per day: 2,000,000 total |
| Newly selected distinct targets | 10,000/day, replicated into two supplied index slots |

The two index copies are an explicit availability placement choice, not a proof that their owners fail independently. The case's complete native closures share a 2-GiB qualified retained core at each serving slot; each target adds at most 256 KiB of unique evidence relative to that core/its prior admitted support. This is a fixture bound, not a claim that arbitrary mathematical targets fit it.

Let `c_core,p` be the actual cost to acquire/qualify/reconstruct that slot's shared core, and `c_j,p` the incremental native checking/composition cost of its j-th target in the selected compatible environment. Initial native work at slot p is at least the work it actually performs for `c_core,p + sum(j=1..2048)c_j,p`, plus parsing, protected staging, any cold dependency misses, current-guard establishment and failures. Compatible sharing must be demonstrated by the exact PI1 cache/support contract; different representative contexts or source-exporter normalization may invalidate the assumed incremental path. There is no numeric native-throughput claim in this equation.

For example, with 28800 CPU-seconds/day as the slot's **entire** supply, completing all 2048 cold target checks in one day would require their mean to be at most 14.0625 CPU-seconds even if the core and every other job cost zero. A nonzero core and serving/maintenance allocation make the necessary threshold smaller. At an actual 60 CPU-seconds per target, those checks alone need more than four such funded days; at one hour per target, 256 days before other work. These are sensitivity calculations, not observed native costs. Initial mathematical checking, sustained incremental checking and source-exporter feasibility can each invalidate the deployment even if every metadata number below fits.

Initial selected stock follows exactly:

- 2,097,152 target copies and 33,554,432 target/token postings.
- 16,392 distinct provider tokens per slot: `8 + 8*2048`.
- 16,785,408 provider/token ads across the 1024 slots.
- 67,141,632 chosen route rows at four copies, before partial/retiring replacements.
- At an assumed 1-KiB stored ad record alone, 64.03125 GiB aggregate chosen-ad bytes. Signatures, group-map nodes, indexes, snapshots and retirement stock are additional. The actual ad ceiling is 4 KiB, which would give 256.125 GiB for that component alone.
- Average chosen rows per routing holder are 3357.0816. This average is not a per-holder admission proof. Each common key has 1024 provider ads at its cells, below the 4096 cell ceiling in this particular workload.
- Native serving-slot stock is at most 2 TiB of replicated common cores plus 512 GiB of target increments in this fixture, before metadata, temporary replays and additional custody copies. Global mathematical deduplication does not make those independently retained core copies occupy no disks.

With one consolidated 2048-target scope per slot and the ideal uniform placement assumption, the occupancy formula gives about 19250 active holder groups per slot, or roughly 19.7 million across the network. Two renewals per day are about 39.4 million group-renewal calls, about 456 calls/second across all holders before other traffic. For this **single-scope, M=20000** settled initial case, the actual count bound is `min(20000,65568)=20000` groups, hence at most 40000 unchanged renewal calls/day per slot. The looser 65568-row/group bound is useful for general multi-run or larger-holder-population safety accounting, not an achievable distinct-holder group count for this single-scope fixture. Multiple scopes can use different groups at the same holder. Actual empty/partial/retiring groups need further stock and possibly further active renewal work; the ideal estimate cannot replace accounting.

### Supplied capacity, not extra invisible defaults

An example funded slot raises the G source envelope and supplies the following **aggregate**, rather than stacking separate default grants:

| Slot allocation | Explicit example cap |
|---|---:|
| Selected target capacity | 4096, with any larger future slot separately admitted |
| Maximum immutable scope target count / emitted-token union | 4096 / 131072, explicitly replacing the initial G 128/4096 local envelope |
| All charged immutable scope records | 64 total across completed, merging-parent/new, pending, retired and uncertain states; at most 13 completed size levels and 32 pending input scopes; at most one consolidation handoff |
| Active owned-token capacity | 33000 |
| Chosen plus transient membership stock | 264000 |
| All charged group records/reservations | 400000, including closing/uncertain/empty states |
| Publication/index/control metadata and retained snapshots | 1 GiB total, with earlier count caps still conditional on actual byte fit |
| Native retained evidence | 8 GiB for this fixture; no general-library fit asserted |
| Concurrent native/query/consolidation workspace | 2 GiB total |
| Source publication/maintenance/serving traffic | 8 GiB/day total, including connection setup and ordinary native responses |
| Source route/group maintenance and publication calls | 262144/day |
| Total CPU supply to all slot work | 28800 CPU-seconds/day, with explicit shares for checking, queries and maintenance |
| Concurrent route executors / pending mutation batches | 4 / 32 |

These caps do not guarantee that every simultaneously maximal dimension fits. For example, 400000 group records at several kilobytes each cannot fit the 1-GiB metadata cap; actual byte admission must stop earlier. A shared physical host offering several slots must add their obligations or explicitly deduplicate actual owned allocations and declare the resulting shared bottleneck. The table is not an assertion that every ordinary investigator donates this capacity.

The 64 charged-scope cap explicitly replaces the old initial four-scope limit for this H local policy. It is one aggregate ceiling, not 64 records in each lifecycle state. Exact target lists, token unions, owner ledgers, old/new commitments and pinned diagnostics count against the same 1-GiB metadata budget; deduplicating actual immutable bytes does not erase live record/retention obligations. Retired parent scopes remain counted until their references and required old groups/snapshots are released. A 4096-target STRUCT2 scope can have 131072 emitted tokens in general; the example's union is only 32776. The separate 33000 owned-token cap means the slot cannot claim full shared coverage for the general maximum-union case without new supply or an explicitly smaller selected target scope.

The current scope's scheduled renewals, queries, new checks, exact extraction, consolidation and repair must fit the actual CPU/I/O/network shares together. Count ceilings do not imply maintenance capacity: the broad 33000-token cap alone yields a loose bound of 132000 membership groups and hence 264000 twice-daily renewals, above the 262144-call grant. Tighter fixed-topology/run-size bounds may rule out attaining that loose bound in a particular settled fixture; the count cap itself is nevertheless not a maintenance proof. Before admitting/claiming maintained coverage, reserve the actual scheduled active-group renewal share plus other required work, or narrow/degrade the scope. Closed/expired groups consume stock but are not renewed. In particular, dividing the CPU cap by an assumed cheap RPC cost is not evidence that native checking also fits. A service-class stability analysis needs the observed cost distribution and burst envelope of each of those classes, not merely their mean record sizes.

Canonical retained bytes do not bound resident native environment memory. The fixture's 2-GiB core and 256-KiB incremental evidence can reconstruct substantially larger declaration/type caches, distinct representative-map environments and protected staging. A full-private source collector may require still more memory before canonical export. The table's 2-GiB concurrent workspace is realizable only if actual peak qualified native/collector/index/query/consolidation working sets and their allowed concurrency fit it, or those stages are explicitly scheduled elsewhere with supplied capacity and transfer costs. An 8-GiB disk fit does not establish this RAM condition. Failure requires new supply, a smaller fixture/slice or a visible unsupported result, not an assumed resident-byte equality.

Routing holders retain their independently supplied row/byte/group limits and need actual service/CPU/connection allocations. Average stock fits the example counts, but overloaded nearest-holder sets can refuse while other holders remain empty. There is no right to use all distant spare capacity through an unchanged nearest-16 route.

### Warm query traffic

For this particular useful-query subset, assume an informative routed token exists and points to a willing provider within the funded horizon. A declared mean plan uses two token-cell lookups, each four route-contact RPCs and two holder pages, then four provider FIND pages. This is 12 routing RPCs plus four provider pages per attempt; it is not the worst G ceiling. It assumes the looked-up retaining holders overlap the queried ones. Failure of that premise is reported, not charged as a successful lookup.

If route-contact replies average 2 KiB, holder pages 8 KiB and FIND pages 32 KiB, application payload is 176 KiB per attempt, about 335.7 GiB/day at two million attempts. Connection framing/authentication and failed retries are additional. Each slot sees an average of 7812.5 FIND pages/day only under balanced provider demand. At one checked successful application per five attempts and at most 256 KiB of missing warm evidence per success, another approximately 97.66 GiB/day is supplied by native acquisition. Neither the 20% yield nor the byte averages is a measured result; both are qualification premises to test.

Initial cold clients are not free. If all 100000 clients need the fixture's full 2-GiB core, initial core traffic alone is about 195.31 TiB. Even dedicating every index slot's full 8-GiB/day traffic grant to that transfer gives a best aggregate lower bound of about 24.4 days, before ordinary query traffic, replication, setup or skew. A successful warm experiment cannot conceal this onboarding cost. A smaller actually sufficient local slice, peer caching with explicit service supply, or greater admitted bandwidth can change the cost; the word decentralized cannot.

### Warm contribution and consolidation load

Twenty thousand replicated target insertions/day average 19.53125 per slot. Under the stated incidence, each adds eight new provider tokens, hence 32 chosen route rows, while its eight common tokens need only local postings. Across the network that is 160000 new provider/token ads and 640000 chosen rows/day, before merges and repairs.

With a four-RPC mean warm holder lookup per new token, initial token discovery contributes 640000 route RPCs/day network-wide. Each singleton's rows may initially have different holders, so group OPEN and mutation work can approach another two calls per newly needed holder group, not one cheap batch per theorem.

For a slot growth epoch bounded by 4096 targets, at most twelve equal-size upward moves charge any inserted token in the simple size-tiered accounting. With one DROP and one PUT per moved copy, a deliberately conservative amortized row-mutation allowance is `2*4*8*12 = 768` mutations per inserted target copy, plus its initial 32 insertions. At twenty thousand inserted copies/day, provisioning that allowance corresponds to 15.36 million migration mutations plus 640000 initial insertions/day across the network. The 768 bound is over the complete admitted insertion-only growth history; it is **not** a hard maximum on any calendar day's work. Actual funded scheduling and finite pending state must absorb/decline its boundary bursts. Actual calls depend on destination/group batching and opens/closes; a batch cannot be assumed full. Boundary bursts can spend a substantial part of an individual slot's daily allowance before later low-work days amortize them.

At a 1-KiB mutation-record scale, these migration payloads can exceed the newly added proof bytes. Fine indexing is not necessarily a negligible fraction of contribution cost. Useful measurements must include record framing, signatures, connection setup, eligibility guards, exact Patricia-map updates, staging and paid failures.

The group-renewal example alone illustrates the connection issue: approximately 39.4 million daily renewals at 1 KiB of request/reply payload are tens of GiB/day; adding a hypothetical 12-KiB fresh authenticated-connection cost to each would add roughly 451 GiB/day. That 12-KiB number is a declared sensitivity assumption, not an observed handshake size. Persistent connections or admitted session reuse can amortize it, but keeping tens of thousands of idle sessions per provider has its own memory, descriptor and recovery cost. The four-executor limit does not create free persistent connections.

The slot's initial cold population is a different workload. Even under four lookup RPCs per token, each slot spends 65568 lookup calls before group OPENs, insertion batches and any native checking. The full 64-call lookup envelope instead gives more than one million lookup calls per slot, exceeding its 262144-call daily grant. Same-day cold publication is therefore not promised by these bounds.

## Heterogeneity, hot keys and failure regimes

### Storage balance does not establish query-service balance

If a fraction z of two million daily queries starts at the same hot cell, its nearest-holder set receives z times that arrival stream even when global average load is low. At z=0.25 and two holder pages per lookup, the cell attracts one million holder-page requests/day, about 11.57/second before route-contact work. Whether four or sixteen relevant holders can serve that work depends on actual costs, admitted quotas, burst patterns and willingness. A severe burst or more active agents can overload it while most holders are idle.

Clients may reuse bounded cached signed leads and previously successful provider contacts, within their actual directory/cache allocations. Those are historical candidates: current native/public checks still apply, and no cached negative result proves global absence. Locally staggered funded refresh can reduce synchronized work. Cache hit rate is an empirical workload property, not a correctness assumption that makes all hot-key traffic vanish.

For provider populations exceeding the depth-zero cell limit, inherited byte-prefix sharding and separately supplied marker paths remain necessary. Our 1024-provider example avoids that particular cell overflow; it does not establish that a million agents can all advertise every common token cheaply. A shared marker is one stored hint, but one million independent refreshers can still generate one million paid requests unless an explicit funded shared-refresh policy exists. This amendment claims no new marker-refresh delegation or lifetime authority.

### Broad tokens can remain information-poor

Suppose every one of P providers advertises the same query token and only two contain the useful lemma. If metadata reveal no correlation with those two identities, q distinct provider probes have probability at most `2q/P` of finding either under uniform hidden placement, capped at one; an adversarial placement can require nearly all providers. With P=1024 and q=4, the elementary bound is about 0.78%. A good DHT route to the common token does not fix that loss.

Likewise, a huge provider may return many matching rows while the useful declaration remains outside the 32 candidate types the client initially inspects. A query conjunction can shrink a posting, but an index provider owning token A somewhere and B elsewhere does not prove cooccurrence. STRUCT2's actual feature recall, query-role lifting, context compatibility and candidate ranking must be measured separately from route reachability.

The worked incidence's eight target-specific tokens deliberately supplies discriminating information. If real mathematics does not expose such useful informative features for the chosen query pool, this optimistic discovery workload is not realized. Larger budgets, better bounded extractors, domain-local indexes or local learned ranking are hypotheses to test; a complete global ledger alone does not solve this relevance bottleneck.

### Maintenance and growth can outrun supply

For every additive resource class, admitted cumulative work must be compatible with actual supplied service, including consolidation and repair. Finite queues can remain safe by declining work while useful coverage deteriorates. Report that deterioration; do not equate bounded refusal with successful reciprocal accumulation.

Specific falsifiable failures include:

- **Unfunded large provider:** a million-target library activates only 128 targets or 4096 tokens, while the UI claims its whole retained collection is structurally covered.
- **Naive partitioning:** common-key rows collide across scopes, or the system charges/reports one physical row as independently renewed by several groups.
- **Too many small groups:** renewal/group stock exceeds supply before metadata bytes or proof storage fills.
- **Growth-boundary burst:** a scope merge cannot complete before old leases expire; report partial handoff rather than claiming amortization supplies immediate work.
- **Dirty eligibility storm:** one incident invalidates shared anchor/support summaries, forcing scans/rechecks that displace renewal and query service.
- **Sparse diverse foundations:** providers split across many exact F/E namespaces, so duplicated core and routing maintenance dominate and apparent global token counts give little reusable overlap.
- **Proof-dominated workload:** source normalization, native composition/reconstruction or full closure checking costs overwhelm the slot's CPU/memory even when metadata fits.
- **Cold-client surge:** common-core delivery exceeds serving bandwidth; warm-only performance conceals initial access failure.
- **Hot/broad token:** nearest-holder service or candidate selectivity fails despite ample total storage.
- **Churn:** actual useful holder sets change faster than route refresh, so retained old groups consume renewal without supplying a current reader path.
- **Source monopoly:** a key has only one available proof custodian; replicated ads do not replicate proof bytes or remove that dependency.

## Explicit million-target supply and continued growth

The initial 1048576-target workload has exactly 2097152 qualified target placements across 1024 slots. An owner can maintain the target-to-slot assignment as local collection/custody configuration, exchange exact public artifact IDs, and obtain independent willing placements. There is no global authority that forces this assignment, no mathematical acceptance vote and no shared research goal. Missing placements remain missing rather than automatically promised by an algorithmic hash.

A physical provider retaining the whole million-target library has choices:

1. Supply its own larger qualified index/native/metadata and traffic profile, with explicit large-scope consolidation and measured posting service.
2. Supply several separately accounted local slots, each with a bounded selected target set, without pretending extra virtual identities create extra hardware.
3. Arrange actual independently operated index/custody slots for selected shards; each qualifies/retains its selected targets and advertises its own keys.
4. Retain more than it indexes and report the exact uncovered fraction/identities. This is honest partial coverage, not a fully supplied index.

Shards can follow actual mathematical interface locality to improve warm reuse and reduce duplicate core costs; proof truth does not depend on that heuristic. Random splitting may provide balance while destroying useful locality. The assignment's closure overlap, keyword/token skew and cross-shard dependency costs must therefore be part of the declared workload.

At a constant 10000 new distinct targets/day, keeping two qualified placements and 2048 targets per steady slot would require approximately 9.77 additional such slot-equivalents/day, or corresponding increases in existing capacity. Existing 4096-target ceilings provide finite headroom, not permanent growth capacity. A real expansion uses funded import/checking, postings, route ownership and partial-coverage transitions; its costs are not removed by drawing a new shard boundary.

More generally, if meaningfully retained target count grows as `N(t)=N0 exp(g t)` while nonzero evidence/index costs per target remain bounded below, supplying and preserving all of it eventually requires resource stock growing at least proportionally in the relevant dimensions, unless a genuinely demonstrated compression/deduplication reduction changes those per-target costs. Search effort need not grow linearly per query if useful indexes remain discriminating; total maintained evidence and arbitrary independent ownership facts cannot be constant-size by proclamation.

## Qualification criteria

Future implementation qualification should report, for a declared diverse native query pool with useful candidate IDs hidden from the client:

- Native cold/warm incremental bytes, actual replay/representative compatibility, CPU/memory and checked application success.
- P_p, U_p, active/retiring/uncertain groups, actually paid rows/markers and exact local target coverage, with borrowed versus individually FULL_FEATURE scopes distinguished.
- Contribution-to-posting, posting-to-placed-cover and unfamiliar-query-to-checked-application latency, including missed deadlines and all denominator failures.
- Route service distribution, hot cells, index query skew, generic bucket size and candidate recall before/after the 32-type selection.
- Stable and dirty-summary renewal costs, connection setup/session state, consolidation amplification, ownership-transfer gaps and recovery expense.
- Initial client/provider onboarding separately from steady warm operation.
- Outcomes under low-capacity/mobile clients, concentrated high-capacity providers, sparse foundation communities, churn, rate bursts and actual service refusal.

Passing the stated resource inequalities is necessary engineering evidence, not a formal guarantee of mathematical usefulness. Failing them is a concrete reason to change supplied roles, scopes, extractors or operating budgets before claiming that the decentralized reciprocal loop works at that scale.
