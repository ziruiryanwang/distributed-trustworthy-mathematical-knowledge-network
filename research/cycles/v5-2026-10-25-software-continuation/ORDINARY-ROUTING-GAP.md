# Ordinary investigator routing: source-only gap decision

2026-10-25. Owner: `ordinary_routing_gap`. Canonical root guard passed.
Only this checkpoint was written. No product import, test, compiler, network,
runtime, state mutation, publication or Git operation was performed. The root
selects any implementation. This does not duplicate the separately owned PAgE
research or assert useful-growth evidence.

## Decision

**There is a real, central integration gap:** the current ordinary investigator
cannot discover an unknown index endpoint from a formal query and a small set of
network bootstrap contacts. Its public `find` requires the operator to already
supply every candidate HTTP contact. The existing v5 rendezvous implementation
can supply this missing indirection without certificates and without a new DHT.

The strongest directly reusable route is a coherent optional **ordinary
located-find plus advertised-serve** successor, reusing the existing location
channel and fair search. It is not yet an implementation selection: its retained
runtime startup cost must be compared with a thin, owner-approved contact
federation before committing engineering. A mere JSON-contact generator would
lose descriptor expiry and move runtime/accounting composition into user scripts;
that is not an equivalent automatic located-find. Do not import the existing
high-level certified `CommonsClient` just to obtain routing.

This is a better concrete software target than another source archive variant
or repeated search microbenchmark. It connects two already implemented abilities
needed by a new participant: locating an index, then independently interpreting
ordinary candidates. It is not by itself a semantic recall, growth or worldwide
availability result.

There are two decisions to fix before implementation: the ordinary rendezvous
advertisement convention, and the optional location runtime boundary. Both are
specified below rather than deferred to an experiment. A review can settle them
without a mathematical proof campaign.

## Authoritative present path

This chat's adopted package is
`experiments/v5-local-checks/fair-investigator-assembly01/assembled/package`,
PROFILE `ea7a958db31ac070aa59be1c1e3c50d4b195cfd982c63658bd80de15ef3c6d01`.
Sources establishing the relevant behavior:

| Source | Actual boundary |
|---|---|
| `software/v5/ordinary_fair_search/peer_api.py:102` | `_contacts` accepts 1–64 owner-supplied endpoints; peers cannot select local CA paths |
| `software/v5/ordinary_fair_search/peer_api.py:162` | `find` requires exact `contacts`, `providers`, `specs`, `limits`, `offer`, `page` fields; every selected provider must already be in contacts |
| `software/v5/ordinary_fair_search/peer_api.py:195` | ordinary semantic namespace and query features are derived locally; one search allocation is prepaid |
| `software/v5/ordinary_fair_search/fair_search.py:37` | scheduler consumes one exact `SearchSession`, exact `Endpoint` objects and fair rounds; it has no location operation |
| `software/v5/ordinary_fair_search/peer_api.py:466` | `serve` opens the ordinary index/custody and listens for a finite lease; optional authoring offers are not location advertisements |
| `software/v5/ordinary_fair_search/profile.py:39` | selected support closure has discovery and HTTP modules but no `location` package or Node runtime |
| `software/v5/ordinary_bounded_operations/run.py:23` | public launcher permits the existing owner/peer/query actions, not a location action |
| `software/v5/ordinary_bounded_operations/source-map.json` | 84-input base source map contains no location runtime/source closure |

Thus the absence is not fixed by fair scheduling. Fair scheduling divides work
among supplied contacts; routing determines which relevant contacts to try.
The current independent provider/source-offer documentation is useful once a
provider is known, not a replacement for that missing selection step.

## Reusable implementation, not the historical README's source-only claim

The old `software/v5/location/README.md` describes an earlier stage and must not
be read as the current implementation inventory. Later portable location code
and the body-location successor actually contain a role-aware maintained DHT,
private Node channel, authenticated descriptor exchange and bounded workflow.

Relevant retained sources:

- `software/v5/portable_runtime/location/controller.py`: explicit immutable
  owner installation/source/workspace adoption, private child pipes, exact
  source/runtime hashes, deadline and cleanup. No root-specific source path.
- `software/v5/portable_runtime/location/controller_services.py`: exact
  `ServiceLocationProcess` and `ServiceLocatedWorkflow`, with reader and index
  provider roles; source/config/state scopes checked before child launch.
- `software/v5/portable_runtime/location/protocol.py`: namespace-and-feature
  rendezvous keys, owner egress, descriptor nonce/key/peer/endpoint binding.
- `software/v5/portable_runtime/location/workflow.py`: prepaid combined location
  and search budget; descriptor-derived contacts retain original expiries;
  one `SearchSession` is issued.
- `software/v5/portable_runtime/location/observed_route.py` and
  `available_descriptor.py`: actual same-channel diagnostics and the narrow
  settled TCP-connect-unavailable outcome. Malformed/authentication/IPC errors
  remain terminal; they are not reclassified as empty search.
- `software/v5/portable_runtime/location/maintained_roles.mjs`: libp2p/Kademlia,
  finite bootstrap addresses, bounded provider advertisements, DHT findProviders,
  role-specific descriptor serving, renewal and explicit incomplete outcomes.
- `software/v5/body_location/portable/location/`: later replacements for seven
  location payloads add exact body rendezvous alongside the unchanged index
  role. V1 index-only config is still supported. This is not absent functionality.

The precise portable source closure is documented in
`research/cycles/v5-2026-10-16/LOCATION-PORTABILITY-SEAM.md`; later role additions
are reviewed in
`research/cycles/v5-2026-10-20/EXACT-CUSTODY-ROUTING-REVIEW.md`.
The latter review distinguishes index and exact-body namespaces. Neither review
proves that the ordinary package currently includes those components.

Use a single coherent canonical-name `location` package in an isolated process.
The exact-class requirements in controller/workflow/observed-route/descriptor
helpers should stay intact. Do not combine separately imported lookalike classes
or monkeypatch frozen module globals.

## What a new participant must know—and need not know

| Item | Source of knowledge | Required before ordinary routed discovery? |
|---|---|---|
| Supported ordinary semantic/profile identity | Locally selected software and checker policy | Yes |
| Formal feature query | Local investigation | Yes |
| At least one reachable bootstrap peer address/PeerID, preferably alternatives | Owner-selected out-of-band contact or retained network contact | Yes; no protocol discovers a wholly disconnected network from nothing |
| Rendezvous key | Deterministically calculated from namespace, selected query-feature subset and stripe | No preknowledge of its value |
| Specialist index provider PeerID | DHT result | No |
| Specialist HTTPS endpoint | Authenticated advisory descriptor under owner egress | No |
| Snapshot ID, result/export ID, new definition name | Subsequent authenticated positive metadata search | No |
| Historical certified foundation/policy pair | Older certified module/body route | **No for ordinary index discovery** |

The actual current ordinary namespace is derived by
`software/v5/ordinary_formal_query/discovery/ordinary_export_adapter.py:32` from
the selected `semantic_id`, preview/evidence/formal-query feature profiles and
partition parameters. It is independent of provider, local context and the old
certificate implementation identity. `compile_query` at line 88 emits at most
eight feature hashes from formal specifications, without a theorem ID.

The location protocol treats this namespace as an exact 64-hex domain label;
its index route is

`H("DMKN-V5-INDEX-RENDEZVOUS-V1", namespace, formal-index-v1, features, stripe)`

with the exact canonical object encoding defined in the protocol. It does not
inspect certificates or derive a policy for the caller. Feeding the actual
ordinary adapter namespace into this unchanged role is therefore conceptually
well-typed. A forged hint cannot make a V3 ordinary record pass its existing
namespace/locator checks or create mathematical acceptance.

By contrast, the later **body** rendezvous namespace commits to the old module
foundation/policy domain and a declaration/body reference. It must not be reused
as if an ordinary unit ID had those semantics. Integrating ordinary proof-unit
custody location is a separate future requirement, not needed to discover index
providers in this selected bridge.

## Required rendezvous convention

Matching feature hashes are necessary but not sufficient. A consumer locating
route `(namespace, R, stripe)` finds a provider only if that provider advertised
the same key and routing retained a usable hint. Existing code deliberately lets
owners select routes. It does not infer all routes from every theorem, and it
does not promise that a provider advertises every subset of its indexed features.

For an ordinary first integration, use a documented, bounded **specialist
registration convention**: the provider selects a small list of formal feature
predicates it serves, and the client selects a finite plan of those feature
subsets from its query. Both compile those specifications with the same actual
ordinary adapter. Default stripe zero is a convention, not a partitioning theorem.
Keep existing explicit contact mode as a useful fallback chosen by the owner.

This convention removes endpoint preknowledge but does not remove vocabulary or
route-coverage assumptions. A client asking only for novel symbol X cannot find
a provider registered solely under unrelated feature Y. A broad theorem-kind
key can supply a discovery starting point but may be a hot key; it must not be
advertised as universally efficient semantic search. Likewise the existing
pair-planning helper improves index posting selection; it does not automatically
create matching rendezvous advertisements and does not change ordinary syntax.

For route plan A and provider advertisement set B, the immediate conditional
reachability obligation is `A ∩ B ≠ ∅`, plus connectedness, a live hint, and an
allowed reachable descriptor/HTTP endpoint. The protocol can enforce bounded
work and truthful incomplete outcomes even when this obligation fails. It cannot
promise useful recall from the route-key hash alone. No experiment is needed to
establish this limitation.

## Smallest coherent actual integration

Prefer one optional ordinary rendezvous adapter with two public compositions,
not a replacement mathematical client:

1. **Located find.** Derive the current ordinary namespace and formal features;
   allocate one original outer grant; start one adopted reader channel; execute
   the finite route/descriptor plan using the existing typed helpers; hand its
   one existing `SearchSession` and exact contacts to `FairSearch`; retain the
   original descriptor expiries and owner egress check before each HTTP request;
   close the channel within the original operation's reserved teardown.
2. **Advertised serve.** Start the actual ordinary HTTP index/custody provider;
   advertise only the returned live endpoint and locally compiled route keys
   through the same finite owned service; stop/withdraw renewal when serving
   ends. Preserve the explicit distinction between hint dispatch and remotely
   confirmed placement. The predecessor `serve_advertised` is a lifecycle model,
   not a drop-in ordinary implementation because it opens certified workspace
   modules, packet stores and optional body routes.

The current public `peer_api.find` must not be called after location as if it
were a fresh grant: that creates another session and drops the private contact
expiry contract. Reuse its result/report validation and scheduler boundary in a
fresh successor. Similarly, wrapping `FairSearch` around raw endpoints without
predial expiry/egress checks would regress the existing located-client boundary.
Its callback currently has no provider parameter; either a narrow explicit
predial guard or an equivalent stricter common expiry must be selected and
documented. Do not silently renew per-contact lifetimes.

The old `located_queries`/`pair_planning` client layer is not the correct reuse
unit: it imports `EvidenceAcquisition`, requires an exact `CommonsClient`,
checks certificate-owner source pins, and installs module/packet acquisition.
That machinery is unnecessary for advisory ordinary routing. Reuse only the
independent channel/protocol/workflow and the existing ordinary acceptance path.

### Runtime cost and genuinely light reader caveat

Current portable runtime adoption is path-portable, **not arbitrary-runtime
portable**. It pins a specific retained release manifest, a 5,896-file
Node/overlay subtree and a 192-MiB upper bound. That subtree is absent from the
3.05-MiB ordinary source handoff. A bridge must provide an explicit optional
runtime artifact/source recipe rather than secretly requiring the giant history
checkout. It need not ship or run old certificate/native mathematics. A narrower
dependency manifest may be useful, but first reuse the known runtime closure;
do not launch a new cryptographic or native campaign to justify routing.

Also, current `maintained_roles.mjs:50–60` requires a listen entry and public
announce for **both** roles; line 167 sets `clientMode: false` for both. Therefore
the existing reader is not yet a well-specified outbound-only laptop/NAT light
client. This matters to the requested ordinary user workflow, not just a threat
checklist. A selected reader-only successor should use the retained library's
client mode, permit no public announce/inbound service, and retain all outbound
egress/transport bounds. Providers can keep their reachable server role.
Inspect the retained library's actual client-mode behavior before selecting the
precise change; do not claim NAT/relay support merely from a loopback pass.

## Decision-changing verification, if root selects implementation

Do not repeat native theorem checking or the old DHT campaign. A small changed
boundary suite can cover ordinary namespace/route agreement; no old-policy
namespace substitution; one prepaid grant/session; predial expiry; no-contact
incompleteness; original typed unavailability; and owned child/provider closure.

The one real integration scenario should be a new reader given only a query,
small bootstrap set and owned budgets. Its ordinary provider HTTP endpoint,
snapshot and export ID must be learned, not fixture-injected into the search
client. Provider registration must be through the proposed public serving
composition. Check exactly one ordinary candidate and complete closure; this is
routing integration evidence, not another mathematical-growth measurement.

If reader client-mode is changed, source review of the retained Kademlia mode
and one relevant outbound-only behavior should resolve that new boundary.
Do not automatically add network-size simulations, throughput benchmarks,
certificate experiments, renewed allocations or independent-host claims.

## What remains outside this bridge

Explicitly unresolved: robust discoverability of unfamiliar vocabulary;
advertisement coverage and hot-key load at huge scale; sustained independent
availability; ordinary exact-unit custody routing; cross-platform deployment;
external security/operational evidence; licensing; and a justified full-cost
growth advantage against optimized local libraries. This routing bridge improves
a necessary end-to-end user behavior, but none of those requirements disappears.

The root should choose this work only as that high-payoff integration—not as a
reason to abandon the growth study or relabel the current software final v5.

## Pause checkpoint and decisive future choice

The user requested pausing after tasks at hand while this source task was being
completed. This checkpoint closes the assignment. No implementation, test,
network run or further delegation is selected; there is no process to leave live.

The retained DHT runtime costs are material relative to the ordinary package.
At resumption, compare these two concrete composition strategies before coding:

- **Thin existing-location bridge:** derive ordinary route keys, use the known
  transport/runtime, and preserve private descriptor lifetime plus fair search.
  This removes provider-endpoint preknowledge and uses an existing maintained
  rendezvous protocol, but introduces a Node dependency/5,896-file pin census,
  service lifecycle and the light-reader-mode repair described above.
- **Owner-approved contact federation:** let a small replaceable set of
  explicitly selected index/directory contacts provide bounded specialist
  contact suggestions under owner egress and expiry rules; retain fair ordinary
  search and ordinary checking. This might have lower deployment cost and avoid
  a new mandatory Node service for readers. It does not automatically establish
  decentralized route coverage or independence, and is not implemented merely
  because existing `contacts` accepts multiple entries.

Do not invent a new DHT to resolve this choice. The source-level questions that
decide payoff are: which already implemented service can supply bounded contact
suggestions without pulling in the certified client; what knowledge a fresh user
must supply in each route; whether the existing runtime can be an optional
operator service instead of a reader obligation; and how original finite grants,
advisory lifetimes and a replaceable bootstrap set are preserved. Neither route
should be selected just because its smallest loopback demonstration is easy.
