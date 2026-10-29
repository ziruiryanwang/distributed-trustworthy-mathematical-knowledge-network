# Independent challenge: exact dependency location and whole cost

2026-10-28, query_scaling. Read DECISION.md SHA-256
`89a7ad832875554545d782c8291b2f5040ad7d8dd5a307a621ae50a8b78da0dd`,
the earlier RESUMED-ROUTING-CHOICE and the specific current acquisition, custody,
contact-map and retained DHT seams cited below. Source/file review only: no code,
imports, database, runtime, network, benchmark or Git. This is a decision challenge,
not a second inventory or a claim that the proposed composition already exists.

## Recommendation

**Adopt the exact-export identity/trust contract; defer a general DHT gateway
implementation in this cycle.** Keep configured supplier sets and approved closed
bundles as the present supported operating path. Do not label them huge-network
location. DECISION correctly identifies a real additional availability capability,
but its default next-implementation recommendation is ahead of a selected operator
membership and registration model. A known-provider retrieval or a small map pass
would not resolve that choice. No new experiment is needed to establish this.

The gap is central when a useful result's missing support export is held only by
an unknown custodian outside the approved supplier set. It is not an obstruction
to correctness or to the existing bounded supplier workflow. Current receive
already tries 1–8 configured sources under one ledger/deadline, with explicit
unavailability handling. Requiring a full closure at a selected supplier is a real
operating compromise: it costs custody/transfer and constrains availability, but
it needs no new routing infrastructure. Use it honestly where that is acceptable.

The likely payoff of exact location is many independent readers reusing a slowly
changing distributed collection. Its payoff is weak for a small known group, rare
one-off exports, high endpoint churn or absent operators willing to maintain ads.
Removing reader-side Node installation is valuable, but shifting it to a gateway
does not eliminate its service, registration, renewal or failure cost.

## Identity and completeness of the actual workflow

`peer_api.receive:1012-1034` begins with **(SemanticID, ExportID)** plus the expected
name. Its validated locator reveals UnitID; exact evidence then establishes the
semantic/unit/export/name binding. UnitID-only routing cannot answer this first
question. Hashing does not reveal bundle membership or a provider. Keep the
ordinary-export routing domain distinct from formal features and certified-body
`{module_id,export_id,universes,body_hash}`. Reuse algorithms, not wrong identities.

Every supplied evidence unit already creates all output locators transactionally
in `ordinary_multi_source/ordinary_acquisition.py:172-216`, including unindexed
support units. Known custodians can answer with existing indexed `get_locator`.
A feature directory can find potentially relevant indexes; that is not an exact
custody guarantee. Do not index every proof-only export merely to make it locatable.

A complete new path must cover operator-approved registration from actual custody,
an independently deployable finite gateway service, learned-contact authorization,
and located receive under the original grant. A parser, bare endpoint response,
self-custody lookup or directory that secretly has every provider configured is
not evidence of open-network resolution. Partial/empty results remain incomplete;
neither a successful DHT event nor a signed descriptor proves continued custody.

## Publication and routing cost that the gateway must pay

Let X be advertised holder/export pairs, K one operator's retained key count,
m missing export demands, and p the bounded suppliers attempted per demand.

| Mechanism | Reader work and coverage | Operator cost/limit |
|---|---|---|
| Configured sources | At most O(mp); success needs a suitable chosen supplier | No global registration; explicit custody/availability premise. |
| Immutable exact-key HTTP map | Bounded direct lookups and returned candidates; only selected registrations | Existing map pattern parses/rebuilds O(K) metadata; 2,048 keys/2 MiB is a finite community limit. |
| Retained per-export DHT publication | Can avoid scanning all providers under routing/membership assumptions | New ordinary role, intents/replication/renewal and current repeated counting cost. |
| Grouped bundle/community hints | Amortizes endpoint/routing maintenance for known membership | Export-to-group mapping, overlap, membership updates and omitted groups remain charged. |

Appending delta exports does not require full-proof re-export: parse new supplied
units and reuse their output-locator derivation. Only actual committed custody
should authorize an advertisement. On uncertain append reporting, bounded exact
lookups of the proposed new keys suffice; no corpus scan is logically required.
Failure to advertise a committed prefix loses discoverability, not correctness.

However, current immutable-map replacement still costs O(K) per refresh. Replacing
it on every constant-size append gives quadratic cumulative metadata work. Batching
can amortize that work at the price of delayed discovery; it does not turn a full
map rebuild into an incremental update. A maintained exact registry would be a new
stateful capability, not the existing ContactMap with a larger cap.

Independently corroborated in `body_location/portable/location/maintained_roles.mjs:
226-234`: `_publishRoute` enumerates all published keys before each publish, even
repeat keys. n new adverts can cause Theta(n²) local key visits. Its 4,096-key cap,
32-item reprovide queue and concurrency two are real finite limits. Repairing the
counter requires durable quota/recovery reasoning; merely removing its check is
not a scale fix. Do not run a benchmark to reconfirm this source-level obstruction.

Even after that repair, X intent records, routing/replication and periodic renewals
remain. Grouping can reduce renewal multiplicity, but arbitrary ExportID lookup
still needs discoverable membership. Current manifests expose UnitID/raw pins and
target lists omit support exports. Optional handoff membership can help already
known coherent bundles without changing mathematics; it is not presently supplied
for arbitrary imports. A bounded gateway could serve a declared community or shard,
provided its registration/partition convention is explicit. Sharding does not
automatically locate the right shard, assign responsibility or solve churn.

DHT benefit assumes reachable participating operators, bootstrap membership,
usable routing tables, registered keys, maintained replicas and a live holder.
Conditional logarithmic routing intuition is not adversarial completeness. The
retained transport does meter service attempts/bytes; those counters do not price
away persistent metadata, CPU, storage, endpoint liveness or operator administration.

## Reader authority cannot be discarded at the gateway boundary

Learned endpoints remain hints. Preserve numeric-address/port/TLS egress policy,
owner-controlled CA trust, immutable endpoint/policy binding and request-start
monotonic expiry, clipped by the original operation and upstream hint authority.
Apply that authority before both locator and evidence dials, including after TLS
setup. DECISION correctly identifies the current relative-timeout acquisition seam;
returning dictionaries into unchanged configured receive would not preserve it.

Missing frontiers arise after ordinary fetch tickets. Existing `charge_external`
requires sequence zero: pre-reserve the complete bounded lookup slice before I/O,
or explicitly compose lookup into the same begin/settle ledger. Never reset it.
Known and learned suppliers share one per-demand attempt cap and original total
request/byte/time envelope; failures consume authority. Deduplicate exact endpoints,
retain cleanup reserve, refuse recursive referrals, and treat uncertain closure
as terminal. A gateway's own DHT/maintenance grant is additional operator cost.

## When implementation becomes the next high-payoff step

Select one coverage contract and one backend, with a concrete membership handoff:
who registers which exact keys/groups, how fresh appends/withdrawals reach the
operator, what is retained/rebuilt/renewed, and who pays those bounds. For a small
declared federation, HTTP metadata or configured sources may suffice. For arbitrary
open distributed keys, retained DHT routing is the stronger reusable candidate,
but ordinary-role integration and publication cost must be selected together.
Do not implement a new registry and DHT gateway in parallel as speculative options.

Only then is the named unknown-holder workflow worth one bounded integration:
a missing support export outside original sources, actual registration/location,
exact locator/evidence and existing ordinary use, including expiry/unavailable
failure and full cleanup. Price publisher, renewal, gateway and reader together.
Until that selection, preserve DECISION as the architecture direction and use the
current cheaper path. The huge-network location obligation remains explicitly open.
