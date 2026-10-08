# CP-001H independent audit: shared indexing and supplied scale

Date: 2026-09-20. Scope: independent paper-contract, arithmetic and accounting review of [H resource supply/discovery](../analyses/CP-001H-resource-supply-and-discovery.md). No implementation, protocol execution, simulation, Lean run or benchmark was performed. Simple displayed-workload arithmetic was independently recomputed. Frozen F/G artifacts are unchanged.

Initial reviewed analysis SHA-256: `F1A1967BB4B423B4D3F6256C415DA4527C0F1D097FC4378353AEE6B9F5474139`. Final reviewed analysis SHA-256: `175572369678586810838D0CD662AF026B86FA12D954E464187C2B5E3B9A06AB`. The author incorporated the corrections recorded below, and the revised portions were independently inspected.

## Verdict and actual contribution

Sharing an existing provider/token route among several local target scopes is a legitimate producer-local optimization: the route identifies the provider's matching public collection, not a theorem-exclusive fetch authority. Independent tiny scopes otherwise collide at the same `(cell,K,provider)` row and can multiply provider/holder groups. Size-tiered consolidation supplies a concrete amortized remedy, with no central registry or mathematical acceptance change.

The proposed million-target example is an explicitly conditional **supply case**, not a capacity proof, realistic feature-frequency measurement or native throughput result. Its principal arithmetic reproduces. After the handoff, scope/count, group-bound, amortization, workspace and predicate corrections below, no unresolved paper-review blocker remains at that stated evidence grade. Practical scale, native costs and retrieval usefulness remain unmeasured qualification obligations.

## Final dispositions

The final reviewed cut now separates intended ownership from every observed old/new row owner; mixed scopes are TRANSFERRING/PARTIAL, not settled cover, without pretending all live discovery has stopped. It explicitly supplies 64 total charged scope records, up to 13 completed size levels, 32 pending inputs and one handoff, with immutable scope maxima of 4096 targets and 131072 emitted tokens and all list/state bytes charged. Its separate 33000-owned-token cap cannot cover an arbitrary maximum-union scope without more supply.

It corrects the initial single-scope fixed-M maximum to 20000 groups/40000 daily renewals; labels 768 migrations as a history-amortized allowance rather than a daily upper bound; requires actual recurring-work admission; and separately requires resident native/source/index working sets to fit the supplied workspace. Finally, SharedFeatureCover now requires its observations unconditionally: a failed or unresolved clause prevents the settled predicate assertion and produces an explicit partial/degraded/transferring/unknown status. The detailed findings below preserve the audit rationale, not outstanding repair requests.

## Frozen contract alignment

Read the relevant FULL_FEATURE and ProviderAd2/FIND contracts in [G STRUCT2](../analyses/CP-001G-structural-retrieval.md), and group ownership, batches, renewal, recovery, caps and reclamation in [F exact routing](../analyses/CP-001F-exact-routing-coverage.md).

- A provider/token route is shared legitimately only **within the same provider identity, exact foundation/extractor and key**. One provider cannot borrow another provider's group ownership or receipt. The mathematical target's own exact public descriptor/posting/evidence eligibility is still required.
- The root-ad chain retains one actual eligible anchor carrying the token. A routing holder need not fetch its mathematical closure, and its signature check does not prove that closure.
- G's group mode FULL_FEATURE identifies the publication mode; it does not authorize H to relabel a scope whose own memberships are incomplete as individually fully placed. Borrowed coverage remains a distinct local aggregate claim.
- Every group member still needs an eligible supporting target inside **that exact immutable group scope**. An unrelated external theorem cannot rescue a stale anchor merely because it emits the same token.
- RENEW is bound to exact current membership/version/root and a current local eligibility summary; dirty summaries require paid revalidation. It does not renew ancestor markers or resurrect old rows.
- At one holder, an old row must be removed from its owner before another group can own that same row key. Separate DROP and PUT calls are not a cross-group transaction. The inherited expected-version, lost-response reconciliation and delayed-GC generation fences remain necessary.

These conditions preserve the trust boundary: shared indexing can change discoverability/accounting but cannot make an unchecked theorem accepted.

## Handoff needs two kinds of ownership state

The initial draft says every token k has one publication owner scope S(k), but also transfers its replicas sequentially. During transfer, different holders can truthfully retain that token under old and new scopes. This is not double ownership at one holder; it is a mixed cross-holder transition. A ledger that stores only S(k) cannot faithfully represent both facts.

The requested repair is to distinguish the **desired settled owner** from each exact row's effective current owner and handoff phase. Record holder/cell/group/generation, actual owner scope, exact anchor/ad/version observation, pending call and missing/uncertain states. Do not overwrite old observed ownership locally before its actual remote mutation is reconciled.

Settled `SharedFeatureCover` must not count old and new owner rows as if every selected replica already belonged to one desired scope. A separately disclosed transition/degraded observation can describe surviving mixed rows and their real scopes. This avoids two opposite errors:

- falsely claiming completed four-copy same-owner placement during a gap or unresolved mutation;
- falsely claiming that all discovery has stopped merely because some still-current rows belong to the retiring scope.

Each surviving row must satisfy its actual scope's anchor and guard rules. Partial observation is not continuous availability. Sequential moves can preserve a useful path when enough actual rows remain reachable, but asynchronous expiry, failed mutation, restart and holder refusal may still remove that path.

An anchor cannot be retained as eligible against an incident/withdrawal. If a same-scope replacement exists, replace the signed anchor under ordinary revision rules; otherwise fund an owner transfer or disclose degraded coverage. Physical native-evidence retention remains counted even when convenient stable anchors increase its duration.

## Consolidation bound: correct under its stated baseline

For insertion-only distinct targets with fixed extracted features, pair equal-size runs and associate every newly covered token with its actual first supporting target/run. Each successful move doubles that run's target count. Through a history ending at N targets, that token moves at most `floor(log2 N)` times. Borrowing from another owner does not itself add a migration, and duplicate incidences do not create duplicate owned rows.

Hence `O(log N)` migrations per token is a valid amortized count for that baseline. It does not establish a bound on:

- failed/retried or uncertain mutations;
- scope splitting, withdrawal, anchor replacement or policy incidents;
- temporary records/rows/snapshots still awaiting reclamation;
- per-target proof checking or new representative environments;
- time to finish a power-of-two merge under leases and finite service shares.

The 4096-target history allows at most twelve equal-size upward moves. With eight new provider tokens per inserted target and four copies, one DROP plus one PUT per move gives `2*4*8*12 = 768` amortized row mutations per target copy, plus 32 initial row insertions. Multiplying by 20000 inserted copies yields **15,360,000 amortized migration mutations**, not an unconditional per-day burst upper bound. Actual days can spend credits/work associated with earlier insertions; scheduling and reserve capacity must meet the real deadlines.

The immutable parent scope's target/token union still must be constructed and hashed, even if unchanged target features are cached. Largest-scope lists, concurrent old/new groups, pending singleton runs and retired scopes all need supplied count and byte limits. Routing consolidation does not change native objects or justify stale native certificates.

## Scope and recurring-capacity corrections requested

F's original source profile allows four active scopes. G's initial feature scope allows 128 targets and 4096 emitted tokens. A binary-tier history can need up to thirteen occupied target-size levels near a 4096-target envelope, plus the active handoff, pending work and retained retired state. H must explicitly supply the larger **scope count**, **per-scope target/union size** and **charged pending/retired scope stock**, not only a larger target or provider/holder group count.

In the workload, a full 4096-target scope has `8+8*4096 = 32776` tokens. Its raw token bytes alone are `32776*32 = 1048832` bytes, before target references, array framing or repeated live/retired lists. This exceeds the old token-count envelope but is compatible with an explicitly raised and actually admitted local profile. No remotely unbounded scope fetch is needed: holders receive its fixed scope commitment, not authority to read arbitrary source material.

The 33000-owned-token and 400000-charged-group caps are independent maxima, not a promise to maintain all such groups under the supplied daily work cap. The loose worst sparse-placement count `33000*4*2 = 264000` twice-daily renewals already exceeds 262144 daily maintenance/publication calls, before useful insertion, repair or lookup. For the selected fixed-M size-tiered workload, tighter bounds may be much smaller, but admission must use actual admitted active groups and reserved service shares. A count cap never supplies recurring operations by itself.

Likewise 400000 group records can exceed 1 GiB depending on their real stored representation, maps and snapshots; the draft correctly makes byte admission dominant. Closed records need not be renewed but remain charged until safe reclamation. Current group count, charged lifecycle stock and scheduled renewal load are distinct variables.

## Recomputed million-target arithmetic

| Quantity | Independently recomputed value |
|---|---:|
| Target copies | 2097152 |
| Target/token postings | 33554432 |
| Provider tokens per initial 2048-target slot | 16392 |
| Provider/token ads across 1024 slots | 16785408 |
| Four-copy chosen route rows | 67141632 |
| Ad-only stock at 1 KiB / 4 KiB | 64.03125 GiB / 256.125 GiB |
| Mean chosen rows over 20000 holders | 3357.0816 |
| Ideal expected groups for one 16392-token scope | 19246.4769 |
| Ideal two-pass network renewals | 39416784.7 per day, or 456.2128 per second |
| Sixteen separate 1024-token scope group expectations | 59266.0567 total, before common-token adjustments |
| Selected warm query payload | 176 KiB/attempt; 335.6934 GiB/day |
| Warm success-evidence traffic under the 20%/256-KiB premise | 97.65625 GiB/day |
| 100000 clients each receiving a 2-GiB core | 195.3125 TiB |
| Best aggregate core-delivery time at 1024 times 8 GiB/day | 24.4141 days, with no other traffic |
| 2048 native checks/day under 28800 CPU-seconds, ignoring all other work | At most 14.0625 CPU-seconds mean per check |
| Initial 2048 checks at 60 seconds / 3600 seconds each | 4.2667 / 256 funded days before all other work |

The occupancy expectation uses independent uniform r-distinct holder choices for each token. It is not guaranteed DHT load balance. Common-token placements correlate across providers, and a cell or its closest-holder set can overload independently of global mean storage.

One numerical wording correction is required: with **one consolidated scope and M=20000 holders**, selected active groups satisfy `G <= min(20000,65568) = 20000`, hence at most 40000 twice-daily renewals for that settled scope. The draft's 65568 row-based group ceiling is a valid loose generic bound, but its hypothetical distinct-group case is not attainable with one scope and this fixed holder count. Multiple scopes/transients have separate larger accounting. Do not mix that generic allowance with the initial case's achievable maximum.

## Native closure and memory costs remain decisive

The example correctly includes full checked retained evidence at each qualified index slot. At the initial cut, 1024 copies of the 2-GiB core occupy 2 TiB, and the stated per-target increments occupy at most 512 GiB across target copies. A mathematical global deduplication ratio does not remove independently retained physical copies.

Those byte premises do **not** bound resident native checking state. Reconstructed expression objects, full environments, alternate B contexts, producer full-private source collection, local postings and query/merge staging can exceed their canonical stored byte counts. Qualification must separately establish that admitted concurrent native/index/source work fits the 2-GiB workspace cap, or supply a larger/explicitly different memory arrangement. An 8-GiB retained-data limit cannot be substituted for that peak-memory condition.

The mean/check sensitivity is honest but insufficient for stability: core qualification, tails, retries, queries, incidents and consolidation share the actual CPU/network service. Neither free native checking nor zero-cost connection setup may be inferred from successful metadata arithmetic. The draft's cold-onboarding lower bound usefully prevents warm-only figures from hiding the initial access burden.

## Discovery, trust and scope of the resulting claim

Given a currently eligible target posting, an emitted required token, a correctly owned/anchored provider route, actual route overlap and sufficient scoped posting progress, sharing that route leaves the target's candidate path intact. This is the right conditional preservation claim. It says nothing about the extractor finding informative tokens for all mathematics, bounded-query recall, candidate rankings or native proof cost.

For a token shared by P otherwise indistinguishable providers with two useful providers, the union bound `Pr[hit] <= min(1,2q/P)` after q distinct probes is valid under uniformly hidden useful placement. A faster route to the common key does not add missing relevance information. An adversarial ordering can hide useful providers beyond the reader's finite scope. Pattern/index progress must not label exhausted work as a negative answer.

A metadata-only broker could safely offer **untrusted candidates** in principle, provided the client independently checks their exact evidence. Its availability, advertisement, false-lead, custody and service contract differs from the present qualified local provider contract. Deferring that extension is coherent; counting its potential efficiency as if already supplied would not be. SNARKs cannot silently discharge byte availability or relevance obligations.

The proper conclusion is therefore a better specified, finitely supplied decentralized reuse loop, with exact partial-coverage and failure reporting. It is not a proof that all nodes possess all mathematics, that all replicas are independent, or that meaningful knowledge grows exponentially without growing resource supply.
