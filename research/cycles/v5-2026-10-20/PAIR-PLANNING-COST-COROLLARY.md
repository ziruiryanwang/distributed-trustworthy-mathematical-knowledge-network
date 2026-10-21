# Pair planner: what total-query improvement follows from source?

2026-10-20, core_release. Bounded source/theory follow-up only; no benchmark,
import, candidate evaluation or runtime. Current114 map995525c5 and the reviewed
pair-planning successors are the basis. Decision: a concrete **whole-query wire
cost separation** follows for the fixed-compiler ordinary-coverage comparison;
**NO-GO for full-cost superiority against an optimally informed old-API agent**.

## Precise supported comparison

Use the same correctly built finite materialized-pair snapshot, records, caches,
provider, routes, protocol and original allocations. Request atoms A,B,C; the
profile first pairs AB and later AC. Legacy exact compilation yields {AB,C};
the new planner yields {AB,C,AC}. Require full ordinary authenticated coverage
of that query's committed index, not merely the first useful positive candidate.
Both use compact offers and the same maximal legal ordinary page sizes.

In each256 partition put N records AB-not-C and N records C-not-A; put one ABC
record in one partition. Conditional on this finite inventory, legacy must
examine256N+1 anchor rows; planned examines1. `Store.page` sends every examined
record and ordinal-vector proof, including nonmatches. `verify_page` requires a
consecutive interval with `next=start+len(examined)`; skipping a rejected row
cannot establish that ordinary interval. This is a protocol requirement, not a
deliberately slow linear implementation. Existing operation-local node caching
is allowed on both sides and cannot erase those transmitted records.

For N=256:131073 stored records,65537 legacy examined rows, one planned row.
The32-row page maximum forces at least2049 legacy pages versus one planned page.
Even counting only the64 ASCII characters of each mandatory object_id, legacy
page responses exceed4MiB. This lower bound ignores its summaries, sibling
hashes, other record fields, requests and HTTP headers, so favors the baseline.

For the planned complete query, select128KiB maximum offer and128KiB maximum
page response. Two requests have at most16KiB bodies each; each exchange has
at most8KiB request and8KiB response headers. Hence the **entire application-
protocol exchange is at most320KiB**, including the enlarged summary, request
metadata and headers. This excludes TLS/TCP/IP/DHT overhead equally; the route
is fixed. The complete planned result therefore has >12.8x less wire payload
than even that conservative legacy lower bound, **if both complete**.

These are byte/count bounds, not invented seconds or hardware constants. For
ordinary pages, each old row additionally requires one record SELECT/parse/hash
and `ceil(log2(anchor_count))+1` authenticated vector-node visits; at N=256 this
is at least589833 logical CAS reads across old pages. Cache hits do not avoid
the existing logical-read charge. The planned summary still pays for3 feature
map proofs and3*256 partition descriptors; its one-row page has a height0
anchor proof. No proportional old-ancestor-proof cost enters either query.

## Finite conditions and why this is not the stronger economic claim

Summary work is real: `Store.summary` permits30000 logical reads,2million
index-hash calls and5seconds; compact decoding expands present features to256
descriptors and256 siblings. Source preflight repeats summary/page validation
before acceptance. The offer can refuse on wire/expanded bytes or these caps;
additional keys receive no refund, fallback or grant renewal. The wire bound
above is on successful completion, not a guarantee against refusal/timeouts.

With small records (for example <=2048bytes),32-row pages fit the stated128KiB
bound even with the9-level exceptional partition. The65537 examined rows and
2049pages fit the protocol maxima131072/4096, with2050 requests below8192;
original caller budgets, storage quotas, byte limits and deadlines must also
permit them. This is a conditional inventory/capacity argument, not evidence
that the completed32-to-1 control built this larger corpus.

An informed legacy owner can instead query **A,C only**, obtain the already
materialized AC anchor, and locally filter authenticated records for B. Complete
AC coverage also covers the ABC subset. That uses the same existing protocol,
one summary and one rare posting; no new planner is required when the owner
already knows the selective pair. Candidate-only pages likewise avoid sending
all rejected records but offer a weaker coverage claim. Thus the mandatory
large cost above belongs to unchanged exact compilation, not every old-API
strategy. The planner removes a default planning blind spot; it does not beat
an oracle-informed query decomposition or establish universally optimal search.

Nor do byte/logical-read counts prove wall-time, energy or fully weighted CPU
dominance: hashing, JSON, SQLite, source checks, routing and provider work have
different costs. No scalar exchange rate is supplied by source. Do not promote
this corollary to net growth, whole-network benefit or a full-cost margin.
No further experiment or implementation follows from this bounded finding.

Sources: selected `instantiation_discovery/discovery/{discovery_store,
authenticated_index,formal_features}.py`; `discovery/{summary_wire,
discovery_query,search_session,candidate_query}.py`; `transport/{http_provider,
search_validation}.py`; pair-planning adapter. Hash identities are in995525c5
and PAIR-PLANNING-SOURCE.md; all inspected bytes remain unchanged.
