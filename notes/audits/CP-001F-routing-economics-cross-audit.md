# CP-001F: independent routing and discovery-economics cross-audit

Date: 2026-09-20  
Status: Completed bounded base-routing/economics paper audit; reported findings repaired at the recorded final revisions  
Method: Complete note reads, counterexecutions and arithmetic/reasoning checks. No implementation, network simulation, benchmark or native proof execution.

## Scope

This reviewer independently read the complete [ROUTE1 base contract](../analyses/CP-001F-dissemination-and-routing.md) and [operability/economics analysis](../analyses/CP-001F-operability-and-index-economics.md). These notes are authored by other agents. The reviewer did not implement routing or reproduce the cited external Kademlia/IPNI source investigation. The separate fine-key coverage extension is not silently covered by this base audit before its actual bytes are read.

| Input revision | SHA-256 |
|---|---|
| ROUTE1 initial full read | `a74f4c07cdabc64c877f19ac4cd646e2273b3fc3db6ec9f6325cd3f74fe75c1a` |
| ROUTE1 stop-condition repair re-read | `599846b6e99457ec06dc9efe7e255057ee60a0d283af6ac87190140cb13005a1` |
| ROUTE1 final shard/horizon clarification re-read | `6648cfb19c677b045dc14f5899aace791b5547a0f0dc6d5335956e10c75539a3` |
| ROUTE1 concrete wire-grammar delta re-read | `b6c9a72d652dec4321324b08c0a72d18d06c94442aa074883f17ea7c1d2a91b8` |
| ROUTE1 final provider-contact clarification re-read | `57ea2ff2473cc2afd3fd68c2b7ea1fe84046de765d97bc6706441ee2a4b83f05` |
| Economics initial full read | `ad4c5673e99c4bceef0d1acd259cf24a508d85783ce4896d72eb9a5c30f366aa` |
| Economics repaired load/renewal clauses re-read | `03a7db93fdff03989c877f75459ee063c26c4f3a960a4ed626f013a7027b6725` |

Hashes identify inspected revisions, not approval of future files at the same pathname. Frozen CP-001E was not edited.

## Concrete findings

### R-STOP: the initial lookup completion test could stop after one response

Severity: material operability defect. Disposition: repaired and independently re-read.

The initial rule stopped when every one of the nearest sixteen **responsive** candidates seen had answered and no closer untried candidate remained. Responsiveness already implies having answered. With known reachable contacts at distances 1,…,16, suppose contact 1 answers and returns no closer node. The responsive set is `{1}`; the stated test can already hold, despite fifteen known live untried contacts. A publisher can consequently receive only one holder and fail the four-copy target in an otherwise adequate local topology.

The repaired rule explicitly separates cases:

- With fewer than sixteen successful contacts, continue eligible untried candidates until candidate exhaustion or budget/deadline.
- With at least sixteen, set the cutoff to the sixteenth successful `(distance,NodeID)` tuple; no eligible closer untried candidate may remain, and closer in-flight work must settle.
- Additional in-flight work is cancelled/settled under its original allocations before fixing the result. Budget/deadline exhaustion is PARTIAL, not a completed sixteen-holder frontier; actual exhaustion can return an explicitly smaller set.

This resolves the counterexecution without pretending CLOSEST_SEEN is global nearest-neighbor completeness. Remaining unknown nodes can still be closer.

### E-LOAD: strictly less average load is not universally necessary

Severity: mathematical wording error, not an admission-authority defect. Disposition: repaired and independently re-read in the final economics revision.

The note calls average demand **below** average capacity a necessary load margin. In the displayed deterministic queue, `A_t=C_t=1` and `Q_0=0` yield `Q_t=0` forever. Strict inequality is therefore not universally necessary for bounded backlog. Equality can be stable in special deterministic or otherwise structured models.

The correct broadly necessary conservation condition is that persistent completed/admitted demand cannot exceed available service in the relevant cumulative/long-run sense without backlog or declined/discarded/coalesced work. Strict slack is a useful robust design target and enters many stochastic stability theorems under additional hypotheses; it is not by itself a universal necessary-and-sufficient condition.

The note's stronger practical point remains correct: even favorable average load does not establish deadlines or fair service under arbitrary bursts, policy choices and contention.

Verified repair: the note now states average demand no greater than average usable service as its long-run balance condition, explicitly permits the deterministic equality example, and describes strict slack as a useful margin under further workload assumptions rather than a universal necessity.

### E-RENEW: renewal-operation count depends on the lease representation

Severity: cost-model scoping refinement. Disposition: repaired and independently re-read in the final economics revision.

The formulas `r A m` for simple replicated stored metadata and `r A / tau` for successful per-record renewals are correct for the declared uncompressed per-advertisement lease model. They are not a universal lower bound on network RPC count for every implementation.

Batching several independent row renewals into one RPC changes RPC count while retaining its per-row checks/payload costs. A genuine shared lease group can instead renew one group deadline for multiple already admitted memberships; then even independent per-row deadline updates are not required at each refresh. The grouped record inventory, admission changes, indexes, group-to-row references, expiry/reclamation semantics and finite payload/meter costs still exist.

The forthcoming exact-key lane may use such groups. Its claim must be charged to that actual selected representation rather than simultaneously asserting the old per-row renewal formula as a representation-independent lower bound. Arbitrary initial ownership facts still require real information/storage; fewer refresh messages do not imply free indexing.

Verified repair: the note explicitly restricts rA/tau and its numerical renewal example to the individual-record lease model; it says grouped leases/batches can amortize operations and that the expression is not a universal network-call lower bound. The actual fine-key group design remains outside this base audit until separately inspected.

### R-AVERAGE: a mean shard occupancy does not force overflow

Severity: minor probabilistic wording refinement. Disposition: repaired and independently re-read in the final base-routing revision.

For a million providers across 256 equally likely first-byte shards, the average is 3906.25. It is possible that every shard stays at or below capacity 4096. Therefore "some branches will split" is not an unconditional consequence of the mean/uniform-placement assumption. Some branches **can** require deeper placement; random imbalance or holder admission can cause that, and the mean alone does not bound the maximum. The selected 32-byte depth and explicit nonplacement behavior remain appropriate.

Verified repair: the note now uses "can require another byte" and explicitly says the average cannot certify maximum load. It also adds an explicit route-horizon-stall case, distinguishing retained DFS/page progress from restarting an insufficient sixty-four-call nearest-holder search.

## Checked countermodels and positive properties

### Connected honest networks can fail the old discovery loop

The three-community/ring counterexecution is valid under the stated original rules. With at least twenty-five higher-ranked local contacts and only sixteen exclusions, every request leaves at least nine local contacts ahead of the outward bridge. An eight-contact response can therefore omit that bridge forever. Fairness over an agent's fixed directory does not imply traversal of all graph paths. Honest complete local FIND replies do not import unknown remote results or recursively forward queries.

The example distinguishes mathematical availability from discovery without assuming malicious censorship. Native exact checking and bundle transfer cannot locate a provider that never enters the reader's candidate scope.

### Coarse provider catalogs have the stated indistinguishability lower bound

Under a uniform unique owner and no ownership-correlated metadata, q distinct probes have success probability q/P. For deterministic worst-case search, every unqueried owner remains consistent with the observed negative answers, so P probes can be necessary. Adaptivity does not beat the uniform fraction when each previous observation is only absence and the prior owners are otherwise symmetric.

This result does not extend to an informative exact posting, correlated useful metadata, replication at several owners or a different prior without changing the premises. It also does not prove every structural heuristic ineffective. It correctly blocks the claim that a logarithmic route to a coarse foundation catalog makes exact theorem discovery logarithmic.

The base note now explicitly calls its sixteen-intent policy a coarse lane and identifies a separately specified fine-key extension. That is the right boundary, but the new lane still needs independent review and eventual workload qualification; its name alone does not discharge the lower bound.

### Base state and traffic limits are genuinely separate dimensions

The base selects finite routing buckets, cell/row/marker counts, aggregate metadata, candidate/tried sets, bounded operations, deadlines and daily authority. Count and byte limits apply together. Four 4096-byte row payloads or sixty-four such rows are not guaranteed to fit a nominal reply once envelopes, keys and child bits are counted; the explicit encoded-byte bound must stop earlier where necessary.

Routing contacts are not a silent expansion of the fixed mathematical PeerDirectory. Returned provider contacts only nominate independently paid ordinary FIND/import work. A signed routing ad is not proof of its formal key, complete theorem availability, service independence, or native truth. The server does not recursively follow child markers or fetch proof anchors during one caller-funded operation.

The provider itself must authenticate placements/renewals/withdrawals. A relayed signed row can be returned as a historical candidate, not used by a third party to refresh its storage lease. Receiver-local monotonic leases and conservative uncertain-clock recovery avoid fictitious global-time authority. New paid calls are distinct from retained data leases.

### Snapshot pages are not current availability certificates

The row tag `PRESENT_AT_NAMED_SNAPSHOT_CUT_ONLY` and equivalent child-marker semantics correctly handle expiry between snapshot and delivery. A beginning-current-snapshot operation sees then-live data at its writer boundary; later reuse needs separately observed native service. No signature or cursor converts a historical row into a live remote storage guarantee.

Provider lower boundaries and child work retained across expired immutable snapshots can prevent repeated prefix scanning. They do not combine different cuts into one completed historical snapshot. Newly inserted rows before the frontier require another sweep. Missing cursors or budget interruptions cannot be converted into END.

### The conditional reachability proof is valid but deliberately strong in its premises

Assume the exact ad and every marker on its finite prefix chain remain represented in the same reached holder sets; assume the reader actually queries retaining holders and fairly completes the necessary pages. Induction on the at-most-thirty-two marker edges then reaches the leaf and returns the provider ad. No intermediate mathematical import is needed.

The assumption that publisher and reader reach the same adequate holder sets is not established by mere physical connectivity or CLOSEST_SEEN. The finite table and sixty-four-call route horizon can miss unseen nodes. Page/DFS frontier persistence also does not automatically retain an unfinished long ROUTE_NEAR candidate frontier across occurrences. A stable adversarially populated route topology can keep yielding PARTIAL unless adequate contact/bucket progress is actually supplied. The theorem excludes that case through its explicit within-budget routing premise; deployments must measure it separately rather than counting each terminated occurrence as eventual discovery.

In particular, expected Kademlia-style prefix progress under a well-maintained honest random population is an engineering hypothesis distinct from a universal guarantee over every connected graph. Sybil grinding, eclipsed bootstraps, unwilling near holders, insufficient budgets and growth faster than polling remain live failure modes even when native mathematical acceptance is protected.

### Arithmetic and accounting checks

The example of one million providers × sixteen keys × four replicas × 1024 bytes gives 65,536,000,000 bytes, i.e. 65.536 decimal GB. Dividing 64,000,000 per-record refreshes by 43,200 seconds gives approximately 1481.48 per second under that stated lease model. These are global aggregate quantities, not a per-node throughput measurement or balanced-placement proof.

The base depth-zero example uses `16 × 2 × (64+16) = 2560` worst-envelope lookup/placement calls per day for sixteen keys refreshed twice, before deeper marker paths. `32768/86400` is approximately 0.3793 operations per second as a daily average, not a guarantee of low burst latency. A 256-bucket refresh cycle at one bucket per ten minutes is 2560 minutes, about 42.67 hours, before interruptions. These calculations check out.

The Lindley-style queue recurrence expresses the conservation issue correctly once the strict-average wording is repaired. Capacity vectors must not add peak memory or instantaneous concurrency as if they were fungible CPU-time units; the economics note explicitly keeps those simultaneous constraints separate. Shared total-node capacity remains the controlling budget.

## Required additional adversarial qualifications

- Known contacts at distances 1 through 16, with no new closer response: the repaired algorithm must fill or explicitly exhaust its holder set rather than stopping after one success.
- Late in-flight closer reply moves the sixteenth-distance cutoff: final set and accounting must include the settled response or explicit permitted cancellation outcome.
- Marker and ad placements succeed but on inconsistent reached holder sets: return degraded/partial reachability, not a successful common-rendezvous certificate.
- Reader snapshot expires repeatedly: retain an exact next lower boundary without claiming a single immutable completed cut or restarting every occurrence at BEGIN.
- A 64-call route horizon repeatedly exhausts along a stable contact path: distinguish route-frontier stagnation from page-sweep progress.
- Candidate output/handoff queues fill: any dropped/unprobed candidates must be counted as discovery limits, not successful candidate use; further ordinary FIND work remains separately authorized.
- A rare exact key is absent from the sixteen coarse advertisements: reproduce q/P behavior instead of reporting catalog routing time as theorem discovery time.
- Simultaneous withdrawal, old in-flight PUT and lease expiry: disclose stale-lead behavior without claiming already disclosed ads were remotely erased.
- Per-row renewal, batched row renewal and true group renewal: account each mechanism's actual group/row metadata, operations, admission changes and expiry costs separately.
- Equal deterministic arrival/service load: the economic model must not call an exactly stable queue impossible merely because it has no strict slack.

## Current conclusion

The base selected layer supplies an actual bounded provider-rendezvous path, not just a contact list and an aspiration to disseminate. R-STOP was a concrete missing progress condition and is repaired. The conditional prefix-chain proof and arithmetic are sound under their stated premises. E-LOAD, E-RENEW and R-AVERAGE are repaired at the independently re-read revisions. No further concept blocker was found in this bounded base-routing/economics review; the separately forthcoming fine-key mechanism is not approved by proxy.

No reviewed mechanism establishes useful discovery under arbitrary growth or scarce service, and no routing result weakens native checking. The project still needs end-to-end evidence of unfamiliar-provider discovery, candidate return and successful checked application under actual supplied budgets. This is a concept audit, not such an execution.

## Final bounded wire-delta disposition

After the initial audit completion, the reviewer re-read the actual base note's new wire-grammar clauses and their surrounding lease, snapshot, lookup and authority rules at `b6c9a72d652dec4321324b08c0a72d18d06c94442aa074883f17ea7c1d2a91b8`, then the final publicContact clarification at `57ea2ff2473cc2afd3fd68c2b7ea1fe84046de765d97bc6706441ee2a4b83f05`. The inherited NET result-code table and resultMetadata/localOutcomeID format were also checked directly.

The added definitions are coherent within this reviewed base boundary:

- `RouteContact` is the separate three-field `[nodeID,endpoints,capabilityCodes]` record, with two endpoint, sixteen capability, sorted/unique and 1024-byte bounds. Capability 5 advertises syntax support, not supplied storage. Mutual negotiation uses reciprocal existing HELLO exchanges, not an invented HELLO request field.
- ProviderAd.publicContact is now explicitly the different GET_ROUTES four-field record. Its NodeID equals the provider; its two public endpoints and at-most-sixteen native-profile/index-key lists are bounded; K's exact FoundationID must be included. The entire signed advertisement still obeys its 4096-byte cap. Maximum list counts do not override that aggregate byte ceiling.
- ROUTE_NEAR echoes its exact 32-byte target and returns at most the requested 1..16 contacts in the specified distance/NodeID order. The 32-KiB total bound remains sufficient for the stated per-contact maximum, subject to actual envelope limits.
- The five positive page ceilings bind row count, encoded bytes, inspected rows, CPU milliseconds and wall milliseconds. Lower requested/offered limits apply; inability to fit the fixed reply fields gives a bounded decline instead of an oversized reply or skipped row. Positive lease requests are bounded by 172800000 milliseconds, exactly 48 hours; the existing receiver-local lease semantics remain unchanged.
- DROP returns a fixed body and numeric removed/already-absent status; mismatch is an error. Redundant key and provider fields are checked against the cell and authenticated peer, not treated as independent authority.
- The new route failure subreasons map to the existing NET top-level codes 2, 3, 4, 5, 8, 15 and 16 with their inherited meanings. Existing cursor/offer/replay/execution failures are not repurposed. The base absent group-observation option is `[0]`; authorization and content of any present fine-group observation belong to that separately reviewed extension.
- Operational result metadata fixes `publicAssessmentDigestOption=[0]`. The local observation/outcome identifier is 16 bytes and binds the committed operational result; possessing it grants no mathematical acceptance, storage read, renewal or spending authority.

No new contradiction or authority enlargement was found in these bounded deltas. The repaired sixteen-success lookup cutoff, historical-only row interpretation, explicit coarse-catalog limitation, finite work/capacity and uncertain-recovery behavior remain intact. Fine-key group transitions and the V3 integration are covered by another reviewer, not implicitly certified here. No execution or implementation was performed. This audit's final reviewed base hash is the `57ea2ff…` revision recorded above.
