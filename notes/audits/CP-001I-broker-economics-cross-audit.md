# CP-001I independent cross-audit: broker economics and evidence availability

Date: 2026-09-20. Reviewer: `commons_independent_audit`, independent of the economics author. Scope: conditional paper accounting, authority-compatible availability models and the four bounded economic modules I-E1 through I-E4. No implementation, protocol execution, native replay, artifact extraction, simulation or benchmark. Simple arithmetic was independently recomputed. H and earlier frozen contracts are unchanged.

## Reviewed cut and disposition

Reviewed the [economics and availability analysis](../analyses/CP-001I-broker-economics-and-availability.md), including its complete repaired argument, at SHA-256:

`F5E82A4A52A4FD8223D831782920FB71003FFF53094753745A30EE1BDA732A9F`.

Checked its composition with [BROKER1](../analyses/CP-001I-untrusted-search-brokers.md), SHA-256 `2A404FAE9F79FE7ED40D1430CAF8AB0B0738CE35F53F340A4BA490C2ECB83C1F`, and the relevant [H resource fixture](../analyses/CP-001H-resource-supply-and-discovery.md). The separate [broker/client audit](CP-001I-broker-client-cross-audit.md) owns the service and receiver-boundary review. Authorship of BROKER1 does not make this an independent audit of BROKER1; this note independently audits the different economics author's claims.

**Disposition:** no remaining blocking arithmetic or conceptual-accounting contradiction was found in the inspected economics cut. It supports a conditional, modest, known-contact role-separation case and explicit defeating cases. It does **not** establish measured superiority, realized native memory/throughput, automatic availability preservation, large broker-routing feasibility or exponential useful growth. Selection of a small service can remain separate from selection of an economic deployment policy.

## Findings and repairs

### EC1: byte absence and native-checking absence are different

The initial analysis used a set of objects not already present **and qualified/protected** when discussing network acquisition. That conflates two obligations. If all required exact bytes are local and hash-correct but their native qualification has expired or never occurred, replay/reconstruction may be necessary while external transfer is zero. Charging those bytes as a mandatory network miss would be an invalid lower bound.

The repaired cut separates `MissingBytes(a,R)` from `NeedsNativeCheck(a,R,context,policy)`. It also allows local integrity checking to establish that existing bytes need no retransmission. Disk, integrity and native work remain charged. Thus a network lower bound now refers to actual externally missing exact bytes under the fixed transfer coding, not to absent acceptance certificates. EC1 is closed at the reviewed cut.

### EC2: a large extrapolation cannot supply the initial broker envelope

The million-target example originally supplied the main favorable regime, but the broker proposal's illustrative current-record cap is 65,536, not a million; an eight-GiB metadata replica also exceeds its four-GiB total stock envelope. A hypothetical larger profile is useful as an extrapolation, not as evidence that the modest profile fits.

The repaired note supplies a one-day known-contact fixture starting at 4000 targets and ending at at most 4096. It separately accounts for current/snapshot versions, postings, fixed state, resident execution memory, recurring CPU and traffic. It labels the large case an extrapolation and does not quietly increase protocol/deployment capacity. EC2 is closed at this paper-accounting grade. Actual implementation fit and native peak memory remain qualification gates.

### EC3: more than four evidence sources need an actual path

A single BrokerCandidate contains at most four leads. An idealized eight-source availability union cannot be instantiated by putting eight sources into that row. The repaired analysis explicitly requires several permitted lead sets or independently known native contacts, with all attempts inside the client's aggregate budget. The static reliability example is conditional on that actual reachability, not a free union over every source in the network. EC3 is closed.

## I-E1: discretionary native-replication savings

**Inputs.** Exact selected replay/target incidences, actual per-source native closure unions, explicit recovery/service requirements, actual metadata allocations and future qualification work. Counts of identical terminal judgments do not license merging different replay contexts or physical failure domains.

**Checked claim.** Replacing discretionary native-search copies with broker copies may avoid their native stock and future qualification. The analysis sums actual per-source unions, retains the original producer's work, does not recover sunk CPU, and permits byte release only where existing retention obligations allow it. It treats costs coordinate-wise and includes baseline metadata rather than charging search metadata only to the new design.

For the small fixture at exactly attained bounds, one full source holds `2 GiB + 4096 * 256 KiB = 3 GiB`. Eight versus two such native copies differ by 18 GiB. This is a canonical native-stock difference, **not** net fleet storage after all metadata, workspaces and fixed allocations. The note explicitly keeps those other terms in the comparison.

The larger fixture similarly gives 258 GiB per source, 2064 GiB across eight and 516 GiB across two, for 1548 GiB avoided at the same attained bounds. Subtracting unrelated upper bounds would not prove such a lower saving; the text correctly conditions the number on attained identical increments and otherwise requires actual closure differences.

**Countercase.** If eight physical evidence copies are still required, moving their public search frontends does not remove those copies. If native evidence is tiny and metadata expensive, the role split can lose. Both appear explicitly.

**Exit at current grade.** Coherent conditional stock/future-work separation is established. Real native qualification cost, closure sharing and an actual release policy remain deployment facts to supply; no release or benchmark is authorized by this audit.

## I-E2: custody, source service and the modest supplied fixture

The two-source design preserves only a separately declared two-copy minimum. It does not preserve the eight-source baseline's possible locality, throughput or independent-failure availability. Source signing keys are not independent failure domains, and live brokers are not proof custodians.

Independent scalar checks of the new small fixture give:

| Quantity | Recomputed result |
|---|---:|
| Retained row-version ceiling | 8192 |
| Postings at 16 tokens per version | 131,072 |
| Version allocations at 8 KiB each | 64 MiB |
| Versions plus stated fixed/control stock | At most 128 MiB, conditionally on actual fit |
| Resident allocation partition | 128 + 64 + 64 = 256 MiB |
| Worst stated broker daily CPU | 3096 <= 3600 CPU-seconds |
| Worst stated native-source daily CPU | 25,096 <= 28,800 CPU-seconds |
| Broker traffic expression | 10.766357421875 GiB < 16 GiB/day |
| Native-source traffic expression | 10.7890625 GiB < 16 GiB/day |
| Avoided future qualification events at 96 insertions | 576 |

This is a nonempty **conditional arithmetic resource region**, not a measured admission certificate. The broker allocations count pinned versions and execution/transport stock; canonical payload size alone does not prove resident fit. The source's three-GiB canonical stock does not prove the native reconstruction/collector fits memory. The traffic supply is expressly 16 GiB/day per source, not an unacknowledged use of H's eight-GiB/day allowance.

The entire pool contains at most 10,000 one-page/one-replay attempts during the interval, with aggregate source-stage limits; the per-node maxima tolerate all those attempts selecting one node in cumulative accounting. Their completion latency still needs a burst/queue condition. The attempt caps may produce nondecision, not successful mathematics. Costs of extra attempts, repeated lead updates, rejected inputs, source setup and retries must stay within the stated ingestion/remaining-work/traffic allocations or require new admission; the fixture does not furnish an unlimited arrival entitlement.

At the final 4096 targets, the referenced native target-count envelope has no continued-growth headroom. The note correctly limits the fixture to this day and requires more supplied capacity for subsequent growth. All clients are warm for the core in this experiment; cold onboarding is explicitly separate.

The H-like consolidation countercase is also numerically coherent. Moving 2-GiB shared cores from 1024 to 64 physical source slots avoids 1920 GiB of that component, but raises the mean native stock to ten GiB per remaining source at attained increments, beyond H's eight-GiB stock. Retaining only 64 times eight GiB/day of traffic gives a 390.625-day ideal lower bound for 100,000 two-GiB cold transfers, versus 24.4140625 days at the original 1024-slot supply. Those are cut-capacity lower bounds, not predicted completion times.

**Exit at current grade.** The small known-contact fixture fits its stated arithmetic caps conditionally and identifies actual qualification gates. No availability equivalence, real implementation fit or custody deletion follows. The larger consolidation is explicitly a different service/capacity choice, not a free optimization.

## I-E3: route and renewal amplification

Known broker contacts are a valid bounded comparison only when how investigators obtain them is supplied. They establish no unfamiliar-broker reachability. Both sides of the small fixture use known contacts, so omitting token-route costs there is a controlled experiment, not a benefit credited only to brokers.

For the separate million-target routed stress case, independently recomputed:

`U = 8 + 8 * 1,048,576 = 8,388,616` tokens per broker.

Eight brokers and four selected holder copies produce `268,435,712` route rows. Twice-daily ungrouped renewal produces `536,871,424` operations/day, approximately `6213.79` per second. At the expressly hypothetical one-KiB request-plus-reply cost, the traffic is `512.00048828125 GiB/day`, before the omitted-but-explicitly-additional markers, setup, failures and repair. Chosen-row storage alone at one KiB is `256.000244140625 GiB`.

The H comparator values, `16,785,408` provider/token ads and `67,141,632` four-copy rows, match H's different two-placement, 1024-slot incidence. They are not presented as equal-coverage experimental designs. The analysis also preserves the native baseline's selected grouped-renewal advantage and refuses to assign that advantage to the proposed ungrouped broker lane.

**Countercase and exit.** Full replicated broker routing can erase a native-storage benefit. A known-contact service can be investigated without resolving that lane; it must not advertise routed-global coverage. The current economics supports keeping broker routing an unselected separate module, rather than letting an unfinished route protocol block or implicitly augment the smaller service.

## I-E4: candidate quality, freshness and receiver cost

Token-only broker predicates do not inherit native pattern filtering. A common token-only comparison and a comparison to the strongest actually supplied native baseline are both needed. False/stale candidates, failed type probes, abandoned acquisitions and actual local applications remain in the accounting; stopping hard investigations sooner is not equal-service efficiency.

The analysis correctly uses `E[sum of actual attempted lead work]` before any common-cost simplification. It does not multiply unrelated unconditional averages in the presence of correlated stale leads. Its success factorization `P(D) P(E|D) P(K|D,E) P(U|D,E,K)` is the chain rule, with zero-conditioning cases handled as joint-event zero, not an independence assertion. The independent source-reliability formula is explicitly a separate artificial model with actual permitted source paths.

Periodic status checking, if selected, costs work proportional to the entries/leads actually checked. Endpoint uptime is not exact-replay retention. A partial exact read observes those ranges during that interval, not all remaining closure bytes or future service. Correct negative-cache meanings are necessary but not sufficient to establish a quantitative fair-retry policy or useful query yield.

At all 96 new targets in the small fixture and the assumed one-second future native qualification cost, the gross avoided CPU term is 576 seconds. The stated service envelopes **do not prove** that additional broker/source/client work is below 576. The text explicitly leaves that net difference and useful yield to independent measurement/establishment. The larger sensitivity, 60,000 seconds divided by two million attempts = 0.03 seconds per attempt, is also correct and illustrates how query waste can dominate insertion savings.

**Exit at current grade.** The break-even questions are well formed and failure costs remain charged. No empirical superiority is established or needed merely to define the safe optional service. A stronger efficiency claim needs the declared workload, actual native/metadata cost distributions, complete denominators and source/service constraints.

## Final bounded conclusion

EC1 through EC3 are closed in the reviewed cut. I-E1 through I-E4 compose without an identified accounting contradiction at the stated conditional paper grade. A small known-contact broker service is a coherent next concept-selection target; a universal broker replacement, reduced mandatory custody, native acceptance shortcut or wide broker DHT is not justified by these results.

The remaining choices are local and separable: finish the minimal metadata/search/lead interface registry, supply a sustained deployment envelope, qualify native and resident costs, and evaluate checked useful applications on a declared investigation pool. No implementation has begun, no final wire IDs are allocated, and no frozen contract is amended by this audit.
