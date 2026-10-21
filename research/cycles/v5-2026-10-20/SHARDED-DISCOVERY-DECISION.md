# Discovery placement decision: do not confuse partitions with useful routing

2026-10-20, core_release. Source/theory only. Selected source map:
`experiments/v5-local-checks/distribution-projection-01-input.json` (113 SDK
entries). No import, runtime, network, test, build or Git operation was run.

## Decision

**Do not implement adaptive object-ID shards now.** They can bound a storage
unit but do not make an unselective query cheap. The current code already has
incremental authenticated indexing, finite provider quotas, selective feature
profiles, maintained index rendezvous and aggregate query budgets. Those are
not missing capabilities.

The next higher-payoff source contract is **exact-demand discovery of a new body
custodian while preserving the current semantic-reader operation**. The first
scope should be an already identified `NeedBody`, not a generic new role,
arbitrary module evidence or automatic global placement. It removes an actual
restriction: a needed committed body may survive at Q, yet the reader cannot
locate/adopt Q unless Q was already an authorized index contact. This decision
proposes that contract; it does not select its implementation or a launch.

Distributed selective-cell placement remains central subsequent work. Its
missing invariant and honest scalability condition are specified below so
that a later implementation cannot substitute all-shard fanout for search.

## What the selected source actually supplies

Logical paths here are resolved through the selected map; predecessor files at
the same logical module names are not assumed current.

| Selected physical source | Relevant fact |
|---|---|
| `software/v5/instantiation_discovery/discovery/discovery_store.py:216` | `Store.admit` derives one record and incrementally updates its feature postings/authenticated trees. It does not rebuild the corpus. |
| Same file, lines 17-20, 191-204 and 257-334 | Explicit object/posting/feature/snapshot/logical-byte/DB-page quotas; immutable cuts; bounded summaries and pages. Capacity refusal, not eviction/repair, is the current retention policy. |
| `software/v5/instantiation_discovery/discovery/authenticated_index.py:49`, `:234`, `:377` | Partition is exactly an 8-bit integer; a feature has exactly 256 authenticated partition descriptors. |
| `software/v5/discovery/discovery_query.py:82` | Each local partition chooses the least-populated queried feature as its anchor. Full interval work is proportional to the anchor postings examined, not merely the number of answers. |
| `software/v5/instantiation_discovery/discovery/module_export_adapter.py:111` | Existing owner-selected pair, type-pattern and conclusion-fingerprint profiles bind their namespace. `compile_query` already materializes a selected pair when applicable. |
| `software/v5/portable_runtime/location/protocol.py:45` | Rendezvous binds namespace, `formal-index-v1`, a feature conjunction and an independent stripe in 0..255. It returns advisory endpoints, not a placement/completeness certificate. |
| `software/v5/portable_runtime/location/maintained_roles.mjs:201`, `:237` | Maintained advertisement and bounded `findProviders` exist. Provider-write observations explicitly do not establish replicated placement. |
| `software/v5/base_projection/client/serve_advertised.py:281` | One selected index view is served with the workspace's custody; configured routes advertise that endpoint. There is no enforced route-to-row ownership map. |
| `software/v5/conjunction_index/client/workspace_atomic.py:738` | Publication stores/read-backs packet and selected semantics, then admits selected exports locally. Success explicitly says `remote_placement_confirmed=False`. |

The last source is an inherited publication boundary, not a claim that every
current facade method is defined there. Selected successor facades preserve
the distinction between local publication and remote custody.

Three quantities must stay distinct:

1. A **local partition** groups one provider's posting sequence by the first
   byte of ExportID. Its records and trees remain in that provider's database.
2. A **rendezvous stripe** changes an advisory DHT key. No source establishes
   that stripe p owns index partition p or a disjoint subset of mathematics.
3. A **placement unit** would specify which records an independently operated
   provider retains, under which cap and horizon, and how a query reaches it.
   That distributed admission/placement invariant is not implemented here.

Increasing partition bits would change authenticated contexts, descriptors and
query wire formats. It would not, by itself, implement item 3.

## Why a hot-key split is not a sufficient next change

Suppose N records share a queried feature f, with at most B matching records per
provider. Hash partitioning requires at least ceil(N/B) storage units. If a
query specifies only f, its answer may be in any of them. Searching all shards
therefore has Omega(N/B) provider fanout and Omega(N) record-output work when
all N matches are requested. For a rare additional predicate evaluated only
after fetching/scanning f, an adversarial placement can force that same scan
before finding its sole match. More replicas spread load; they do not remove
this logical search work. ExportID prefixes do not promise balance against
chosen inputs or correlated contributions.

Even requesting one useful answer does not solve the general case: relevance
may distinguish a single unknown member, and an irrelevant bounded prefix can
hide it. A bounded response is a safety property, not a recall theorem.

Current hard caps already bound the work the caller authorizes. Their valid
failure result is incomplete coverage or exhausted budget. A new shard layout
that only reaches the same result with more metadata is not advancement.

## The missing invariant for later scalable selective discovery

For a stated query class Q, define a deterministic, independently derivable
planner K(q) returning at most a routing predicates. Reuse the existing feature
specifications/profiles; do not invent an answer-dependent namespace. Each
predicate denotes a selective **cell**, not a hash bucket chosen after learning
the desired answer. Require the following operating assumptions/invariants:

- **Bounded ownership:** every participating provider admits at most L cells
  and a configured total record/posting/byte budget B. Overflow refuses or
  transfers future admissions under explicit owner policy; caps do not grow
  silently. Retained immutable-cut history counts against those budgets.
- **Admitted placement:** an owner deposits a record in a cell only after
  computing the cell predicate from its exact export, obtaining a bounded
  custodian acknowledgement and recording the chosen finite retention horizon.
  A published DHT hint is not that acknowledgement. There is no global cell
  owner or mandatory universally complete index.
- **Query-directed coverage:** for the declared participating snapshot family,
  every promised candidate for q is assigned to one of K(q)'s cells. The number
  of relevant cells cannot secretly be a function of total corpus size.
- **Selective local work:** the sum S(q) of the chosen cells' shortest relevant
  anchors is within the work envelope, or the interface explicitly returns
  `REFINE_OR_INCOMPLETE`. If an existing pair/type-pattern/fingerprint expresses
  the discriminant, use it before proposing a new posting representation.
- **Bounded routing/replicas:** at most r chosen providers per cell are tried,
  with all attempted hints, stale contacts, responses and acquisitions charged
  to one original envelope. Additional providers do not replenish it.

Under successful routing/availability and those assumptions, selected work has
the form

    O(a r R(P) + a r H + S(q) log B + returned_bytes),

where P is participating routing-peer count, R(P) is the actual exact-key
routing cost under stated network assumptions, and H is the bounded local
summary/verification cost for the retained 256-partition format. If a, r, B
and S(q) are fixed operating bounds, unrelated corpus growth does not add a
scan term. A logarithmic expected R(P) would require the usual reachability,
routing-table and honest-enough maintenance assumptions; it is not a guarantee
of this untested deployment. DHT event limits are not a bound on every wire byte.

Storage scales by adding funded bounded providers, not by requiring each one
to retain all mathematics. This is a conditional feasible design, not a proof
that arbitrary queries satisfy selectivity or that enough providers volunteer.
High traffic on a genuinely selective cell also requires sufficient replica
service capacity; small data volume alone does not bound query arrival rates.

The current missing boundary is **bounded remote cell admission plus a
query-derived placement/coverage contract**, not incremental indexing or a
missing feature hash. An adaptive directory whose internal nodes require the
client to traverse every child fails the query-directed condition. If no known
query feature distinguishes an overflowing cell, return partial coverage or
ask the local agent to refine. Do not advertise global completeness.

The smallest later placement implementation could use finite owner-selected
cell views built by existing `Store.admit` and existing profiles, with explicit
per-cell custodians/acknowledgements and route bindings. It need not change the
authenticated 256-way layout first. However, no supported target/query/cell
assignment presently makes that new distributed lifecycle more urgent than
the known-body acquisition restriction below. Do not implement it speculatively.

## Immediate concrete seam: find a custodian for an exact demanded body

### Counterexample within the present architecture

A reader has already selected module evidence and a declaration opening. Its
semantic preview requests a body at (module, relative name, universe arity,
body hash). Its original provider P is unavailable or does not serve that body.
An independently retained Q serves the exact committed body but is not among
the current query's adopted contacts. The mathematics and bytes exist; the
current public operation cannot use them without foreknowledge of Q.

This is not the already-solved split-supplier case. That case assumes Q is
already authorized. Actual current boundaries are:

- `iterative_queries/client/semantic_reader.py:58` pins the search/acquisition
  generation; `:153` validates pending typed semantic demands.
- `instantiation_discovery/client/workspace_evidence.py:368` permits a supplier
  only if it is in both acquisition endpoints and the original search endpoints.
- `located_queries/client/located_queries.py:66` binds immutable endpoint and
  expiry maps. Its `retire` at line 241 closes the acquisition generation and
  clears candidate/staging state.
- `portable_runtime/location/protocol.py:14` fixes the role to formal indexes.
  The present protocol has no committed-body rendezvous role.

Consequently, neither mutating a contact dictionary nor starting another
semantic query is an honest implementation: the former violates live bindings;
the latter retires the very context being completed. The new capability must
be explicit and preserve the existing reader's original grant and origin.

### Smallest proposed contract

1. Select only an already pending `NeedBody` whose exact declaration commitment
   was acquired/validated. Derive a domain-separated **committed-body route**
   from the semantic format/foundation/policy and exact module/name/arity/hash.
   It is not an arbitrary formal feature or a new interpretation of stripe.
   It must not depend on an optional discovery-profile namespace: identical
   semantic objects remain locatable across different specialist indexes.
2. A custodian advertises only a finite owner-selected set after a current
   ordinary-store exact-body read-back. No full-corpus inventory scan, semantic
   proof execution or unbounded automatic advertisement is required. This
   observation establishes current readable custody, not future availability.
3. Route and request bounded advisory descriptors using retained authenticated
   transport, owner egress rules and finite TTLs. The role/key must bind the
   requested semantic address. A descriptor never makes its sender a
   mathematical authority or certifies replication independence.
4. Issue an opaque **demand-local supplier capability**, bound to that demand,
   current grant, active reader, policy and expiration. Keep it separate from
   the immutable search contact map. It authorizes only the existing body GET
   path for this demand, not new search, code execution or unrelated endpoints.
   Location and fetch consume pre-reserved slices of the existing outer budget;
   no new process allowance or query generation is obtained implicitly.
5. Use the existing exact body validator/custody/admission path. Preserve the
   original candidate supplier and all mathematical identities. Ordinary
   pre-validation unavailability can settle an attempt; malformed/commitment
   failures follow the current failure rules. Do not let a new contact turn
   post-custody uncertainty into a recoverable network miss.

This needs deliberate successors of Python/MJS location role/key validation,
the advertised-service finite selection, and a demand-bound contact issuer /
acquisition adapter. Existing `OwnerEgressPolicy`, authenticated peer handling,
settled body transport, exact commitments and final proof acceptance are reused.
It is not a one-line loosening of `_selected_supplier` or `_Binding`.

Defer `NeedModuleEvidence`: a ModuleID can have several offered evidence-packet
variants, so locating that semantic claim is not locating one already selected
packet hash. Likewise generic receipt discovery and autonomous replication are
separate contracts. Beginning with exact bodies avoids silently choosing a
proof variant or another trust domain.

### Conditional payoff and stop condition

For d actual demanded bodies and at most r attempted custodians per body,
additional selected routing work is O(d r R(P)) plus the selected payloads and
ordinary validation. It does not inspect unrelated theorem records or every
provider. Honest completion requires a live advertised copy reachable within
the finite envelope. Failure means not acquired from the tried custodians,
never global absence. Existing custody quotas bound each provider's stored
body bytes; per-body advertisements need their own existing-style quota.

The decisive small future check is: P's selected declaration is already staged;
Q is absent from the original search contacts; Q is found from the exact pending
body address; one validated fetch completes that same reader; a wrong body and
expired/mismatched capability refuse without resetting budgets. Retained
mathematics suffices. No proof production or planet-scale benchmark is needed
to distinguish this capability from the predecessor.

Stop this investigation at a reviewed exact-demand contract. Root must select
implementation and a bounded changed-boundary check separately. This seam does
not prove net growth, automatic retention, broad semantic-query recall or v5
completion. It advances a necessary independent-custody path while avoiding an
unjustified distributed-sharding mechanism.
