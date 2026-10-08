# CP-001F: end-to-end operability and the cost of useful discovery

Date: 2026-09-20. Status: concept analysis awaiting independent review; no implementation or measurements. This note does not change frozen CP-001E.

## The claim we actually need

The commons succeeds when an independently investigating agent can obtain affordable trustworthy existing mathematics, use it in an independently checked construction, and contribute evidence that another initially unfamiliar agent can actually discover and reuse. Independent investigation is external to the protocol. The protocol neither assigns research goals nor judges human intentions.

Terminating bounded requests, storing many valid propositions, and producing correct local rejection messages are necessary infrastructure but insufficient evidence of that reciprocal outcome. Each can occur in a network that never supports an unfamiliar successful reuse.

The selected CP-001F mechanisms address different links in that chain:

| Link | Required evidence | Insufficient substitute |
|---|---|---|
| Produce | Complete body-bearing native candidate and exact selected closure | Successful public Lean import or source signature |
| Publish | Actual public index entry and admitted dissemination state | Local proof check alone |
| Find a provider | Scoped route observations leading to a willing endpoint | Physical connectivity or a signed offline address |
| Find a candidate | A returned exact statement/interface matching the actual formal query | A provider having some mathematics in the same foundation |
| Reuse | Complete locally protected checked evidence and a checked application | Similar name, embedding, foreign acceptance, or matching type text |
| Combine branches | Consistent selected evidence or an explicitly transformed and checked join | Independently valid input replays alone |
| Preserve | Surviving complete evidence under actual custody allocations | An unbounded aspiration or a past retention receipt |

No line in this table requires a natural-language/formal-language interface. Agents may generate, inspect, query and combine formal objects directly. A private investigator may have preferences or intentions, but they supply no corpus acceptance condition.

## A rigorous limitation of provider catalogs

Consider P honest publicly serving providers under one exact foundation. Each has one candidate relevant to a different exact existing-statement query. Suppose their publicly routed metadata expose only the foundation key and the same common structural features, with no information correlating a particular query to its owner. Provider identities differ, but the assignment of the queried candidate to these identities is unknown. Assume there is one owner for the chosen candidate and no already useful local cache.

For a deterministic lookup strategy that has probed fewer than P providers, place the candidate at an unqueried provider. Every observed negative response remains consistent with that placement. Therefore there is a compliant worst case requiring P provider probes. If the unique owner is uniformly distributed over the P identities, q distinct probes find it with probability q/P. Adaptive selection does not improve this fraction when all earlier observations are merely negative and the metadata have no ownership information.

This is an information limitation of the stated catalog, not a lower bound on all distributed indexes. A routed exact-judgment or informative structural posting breaks the indistinguishability premise. A learned model with useful correlated metadata might also improve practical selection, without becoming mathematical authority. A logarithmic route to the coarse foundation catalog does not by itself make the following provider search logarithmic.

Consequently, the ROUTE1 design must not claim efficient targeted discovery merely from bounded provider advertisements and a fallback key. Its finite fine-key coverage, actual selection policy, publication backlog and query cost must be visible. The highest-count local-key policy can systematically omit rare but useful keys; it cannot be the only practical coverage mechanism.

### What a fine-grained index costs

An exact posting for each distinct advertised provider/key pair occupies metadata, replica storage, placement/renewal traffic and reader work. Provider aggregation avoids one record per proof when many proofs share a useful key, but it cannot encode an arbitrary independent collection of exact ownership facts in a constant number of uninformative records.

Let A be the number of maintained provider/key advertisements, r their chosen live replica count, m their mean stored metadata bytes including local indexes, and tau their intended refresh interval. A simple steady-state allocation must account for approximately rAm stored bytes. In the **individual-record lease model**, independently renewing every admitted row requires approximately rA/tau successful renewal operations per unit time, before routing, failed calls, markers, snapshots, signatures or churn repair. Grouped leases/batches can amortize those operations; rA/tau is not a universal network-call lower bound. These are workload quantities, not proof of balanced load; a hot key can overload its holders while aggregate spare space remains elsewhere.

For illustration only, one million providers each maintaining sixteen keys gives sixteen million provider/key pairs. Four copies of a 1 KiB mean record already require about 65.536 GB of aggregate metadata. In the individual-record lease model, refreshing every twelve hours requires about 1481 successful replica renewals per second across the network, before discovering holders or publishing marker paths. This is not inherently infeasible for that population, but neither is it zero because the operation is called a hint. The selected ROUTE1 maximum record size is larger than this illustrative mean; no measured average is asserted.

Rotating a small live key subset can improve exploration but does not establish continuous coverage. If publication and reading windows repeatedly fail to overlap, a desired provider may never be seen even while both sides cycle forever. A fairness argument must name adequate overlapping live placement and reader service, or a persistent fine-key coverage policy; it cannot infer overlap from two independent round-robin schedules.

## A finite capacity model for the whole loop

For each local service class j, let a completed or failed occurrence consume an actual nonnegative vector w_j of CPU, peak/concurrent memory, bytes transferred, durable/staging byte-time, storage I/O and control-state creation. Peak memory and instantaneous concurrency require their own simultaneous bounds; they are not added as if they were CPU time. The authority mechanism admits occurrences only within supplied capacity vectors and hard instantaneous limits.

For an additive bottleneck resource, an illustrative work backlog satisfies

\[
Q_{t+1}=\max(0,Q_t+A_t-C_t),
\]

where A_t is admitted work entering the class during the interval and C_t is actual completed service capacity. If cumulative arrivals exceed cumulative available service by an unbounded amount, then the backlog grows without bound unless work is declined, coalesced or discarded. A finite node must do one of those things; a retry label cannot create capacity.

In a stationary idealization, average demand no greater than average usable capacity is a necessary long-run balance condition for serving all admitted work without growing backlog. Strict slack is a useful design margin under further workload assumptions, not universally necessary: deterministic equal arrivals and service can remain stable. Neither average inequality alone is a universal liveness theorem. Burst sizes, correlated failures, expensive outliers, deadlines, queue policies and contention can still cause indefinite starvation. Conversely, the real protocol's finite queues may remain bounded by dropping useful work, while delivering poor mathematical utility. Bounded memory alone is not proof of healthy accumulation.

The relevant classes include full-evidence producer collection, new native checking, cold acquisition, warm extension, fine-key publication, routing maintenance, candidate search, checked application, custody repair, and selected foundation migration. Their grants come from one owner's supplied node budget. Giving every subsystem its own apparently modest default without summing them would oversubscribe the machine.

### Selected admission and progress policy

Keep the existing exact authority/conservation mechanism. Add the following product-level interpretation to all profiles in this amendment:

1. Every standing policy states its finite aggregate capacity and partition among serving, local active work, maintenance and exploration. A displayed default is not an additional grant outside that partition.
2. Coalesce repeated publication/update nominations by exact key/root when their chosen semantics allow it. Do not coalesce mathematical evidence by an unproved equivalence or forget a separately owed exact custody target.
3. Record declined, delayed, expired and completed work separately. A completed false lead still consumes discovery budget; a successful RPC is not a successful theorem reuse.
4. Maintain persistent bounded progress for each actually admitted long sweep. Restarting a stale immutable snapshot requires a new paid read with an explicit next lower boundary when legal, not automatically beginning the whole collection again.
5. Exhaustion produces visible degraded coverage or nondecision. It never permits unchecked proof dependencies, revival of expired work rights, or hidden destruction of a custody promise.
6. Supply fair finite service shares to the selected exploration/maintenance classes. This is fairness among locally admitted scopes, not a right for every remote key or a promise to explore every mathematical subject.

The exact ROUTE1 key-selection/continuation policy belongs to the [routing contract](CP-001F-dissemination-and-routing.md). The above conditions expose whether that contract's actual operating scope supports useful discovery. They do not silently expand its table or grant limits.

## Branch interoperability is a separate usability denominator

Two agents can each export individually checked results yet fail to combine them under one selected witness map. The [composition analysis](CP-001F-proof-identity-composition.md) selects proof-valued opaque capsules for an exact eligible slice, not universal cheap merging. Missing full source bodies, proof-dependent statement types and nominal group differences are distinct compatibility cases.

For a declared sample of independent branch pairs, report at least:

- pairs whose exact interfaces already agree and whose witness maps union;
- pairs handled by the selected bounded capsule/rechecking route;
- pairs requiring a different explicit checked transformation or semantic bridge;
- pairs refused because complete evidence is unavailable;
- pairs that exceed their actual time/memory/closure envelope.

These are receiver-local outcomes over a declared finite sample. They are not a network-wide ranking of agents or a mathematical judgment that an unsupported proposition is false. Counting only the pairs already compatible would hide the very interoperability barrier this project needs to solve.

An algorithmic improvement is valuable without a universal guarantee. For example, preserving polymorphic proof sharing on an eligible slice avoids a concrete literal-export blowup. Its coverage in practical Lean developments must still be established, rather than calling the restricted slice the whole of mathematics.

## Workload specification before future implementation

No measurements are claimed now. The concept nevertheless needs a fixed kind of evidence that could later refute the design's practical adequacy. A qualification workload records exact source/target foundations, selected input snapshots, node roles and supplied capacities, network topology/churn assumptions, query scopes, and completion deadlines.

It includes the following complementary cases, not only small arithmetic demonstrations:

| Case | What it must reveal |
|---|---|
| Ordinary structured Lean library slice | Full private-body availability; structures, instances, dependent types, classical/quotient mathematics, literal bootstrap and exact native rename compatibility |
| Warm independent contributions | Incremental native and metadata costs, with unchanged shared evidence actually reused |
| Independently developed overlapping branches | Witness conflicts, capsule eligibility, proof-dependent interfaces, retained exact footprints and join costs |
| Clustered honest network | Useful contribution discovery across initially unfamiliar communities |
| Rare precise query among many providers | Fine-key coverage, provider probes and the failure of an uninformative coarse fallback |
| Rapidly growing corpus | Publication/scan lag, newer-versus-older candidate coverage, queue depletion and explicit degradation |
| Withdrawals, crashes and storage losses | Stale advertisements remain nonauthorizing; acquisition/custody failures cannot become native reliance |
| Changed or suspended foundation | Selected migration work, temporary storage, target checking and honest distinction between re-expression and established correspondence |

For each chosen query/application, record provider discovery, candidate retrieval and native application success separately. Record complete selected-evidence bytes, incremental bytes, cold/warm checking cost, control traffic, elapsed contribution-to-reuse time and reason-coded failures. Queries are test inputs about existing artifacts; they do not become a live registry of unsolved mathematics tasks.

The workload can include utility heuristics or agent-chosen applications. Their imperfections do not weaken the acceptance boundary. A useful practical result is high successful reuse and affordable contribution under meaningful diverse workloads, not a formal proof that a theorem's popularity equals its intrinsic mathematical value.

## Meaningful growth without fabricated novelty

Keep three distinct accounting views:

1. **Evidence stock:** exact independently checked usable statements, definitions, groups, proof alternatives and their recoverable closures.
2. **Operational reach and reuse:** which existing evidence can actually be located and used within stated scopes and cost envelopes, including successful unfamiliar-agent applications.
3. **Estimated useful accumulation:** local cost savings, reused interfaces, complementary coverage and other explicitly heuristic observations.

New proof capsules, changed foundation encodings, alternate wrappers and reserialized archives can increase evidence bytes or new IDs without representing a new mathematical insight. They may still improve affordability, preservation or interoperability. Count their operational role honestly instead of defining every new ContentID as mathematical growth.

Likewise, a new checked theorem may have zero observed reuse so far without being invalid or intrinsically worthless. Corpus correctness does not depend on contemporary audience size. No universal equivalence/novelty oracle is required for this separation.

## Current disposition

The full-evidence collector, bounded branch transformation, routed provider layer and local foundation migration are concrete advances over CP-001E. They are not an executed operability demonstration. In particular, selective fine-key indexing and practical branch-compatibility coverage remain central adequacy questions, not optional political features.

A checkpoint may freeze the exact selected design, counterexamples and remaining evidence obligations. It must not mark the ultimate goal achieved merely because every bounded call has an error response or every Markdown file has a hash. The goal remains a useful, trustworthy reciprocal mathematical system.
