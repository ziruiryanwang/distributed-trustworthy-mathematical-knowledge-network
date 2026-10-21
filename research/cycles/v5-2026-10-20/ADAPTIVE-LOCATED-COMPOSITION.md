# Adaptive queries and unknown-provider location: one remaining seam

2026-10-20 source-only decision. No implementation, imports, tests or runtime.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Basis: `sdk_sources` in `experiments/v5-local-checks/distribution-discovery-01-input.json`
(SHA-256 `e0e22f412a6d276f172603ad11ff5217ea321b5a038921af2bd7f1b4b028e20b`),
plus the four fresh `software/v5/iterative_queries/` successors. Historical
logical-path predecessors are not assumed to be the selected implementation.

## Already present: one unknown-provider query without a global scan

`conjunction_index/client/workspace_atomic.py:508` implements `CommonsClient.find`.
It compiles the formal query, validates an explicitly bounded plan of feature
subsets/stripes, uses an actual location child, requests authenticated service
descriptors, and opens a search over obtained advisory contacts. The agent need
not know result IDs, provider HTTP endpoints or snapshot IDs beforehand.
`search_offer` obtains a provider-selected snapshot; bounded formal pages follow.

The route is a rendezvous key, not a corpus scan:

- `portable_runtime/location/protocol.py:41` binds namespace, formal-feature
  conjunction and stripe into the exact route key.
- `portable_runtime/location/maintained_roles.mjs:236` calls DHT `findProviders`
  for that key, with event/provider caps and a 256-peer process-local result cap.
- `portable_runtime/location/available_descriptor.py:18` consumes the same
  workflow ticket and authenticated channel identity, with bounded descriptor
  bytes/age and an explicit unavailability outcome.
- `portable_runtime/location/workflow.py:146` validates descriptors against the
  original query/policy and retains absolute contact expiry; `:178` creates one
  `_LocatedSearchClient`, whose predial guard is at `:30`.

Bootstrap knowledge is still needed to join an otherwise unknown network:
`maintained_roles.mjs:50` accepts at most 16 bootstrap hints. This is not mandatory
preknowledge of every mathematics provider or a required central server.
No finite bootstrapping/routing plan guarantees connection to a hidden partition.

## The composition that is NOT currently exposed

The new direct envelope is intentionally incompatible with the located query
slot: `iterative_queries/client/direct_contacts.py:277` consumes `_query_used`,
and its `:181` invariant requires `_channel` and `_handoff` to remain None.
Conversely, existing `find` refuses an already used query slot and transfers
ownership of its channel/handoff to the client. Calling both is not composition.

The lower layer is also one-query-bound: `location/workflow.py:59` fixes the
feature tuple, `:86` routes only its subsets, and `:178` leaves LOCATING forever
after issuing one search. `delta/transport.py:169` requires a fresh unstarted
reader, prepays location+search once, snapshots that prepayment and query, and
`:225` issues only one search. Frontier/mixed handoffs alias this exact class
(`frontier_network/transport.py:20`, `mixed_network/transport.py:20`).

The Node service itself does NOT require recreation for every query:
`maintained_roles.mjs:196` admits successive bounded commands; `:236` accepts
different valid same-namespace route predicates. The Python channel already
serializes multiple commands under one original deadline (`controller.py:177`).
Thus a new DHT, daemon, proof relation or provider census is not the missing work.

An external trusted owner may discover endpoints separately and deliberately
approve them as direct contacts, funding both activities independently. That is
a valid different policy; it is not an existing automatic same-envelope adapter.
Blindly copying endpoints out of a located search into `next_query` would replace
descriptor expiry by a fresh contact lifetime and omit the location costs from
the query-envelope report. It must not be presented as preserved located scope.

## One recommended seam, and its cost boundary

If the next central requirement is adaptive unknown-provider searches in one live
mathematical operation, add **generation-scoped located contact acquisition under
one prospectively prepaid combined envelope and one retained location channel**.
Reuse the existing route/descriptor authentication and per-generation retirement.
Do not weaken direct-contact invariants or reset `WorkflowBudget`/handoff fields.

Before any acquisition, reserve the sum of generation routing attempts/events,
peer slots, descriptor requests/reply bytes, contact slots and search allocations.
Each new formal query draws a nonrefundable slice; exact descriptor-derived
contacts carry their existing absolute expiries into search and custody. All
work retains the original grant, channel/policy/namespace, issuers and deadlines.
Settled failed location consumes its slice; no contacts is not global absence.

Receiver acquisition charges remain in the same original ledger. Query events
are NOT DHT wire bytes: the retained service has separate transport limits and
reports (`maintained_roles.mjs:87`, `:332`); account for them without inventing an
O(log N) semantic-search guarantee. Fixed local caps remove mandatory corpus-
size scans by allowing explicit incompleteness, not by proving universal recall.

Recommendation: this is the sole concrete adapter gap identified here. Preserve
the direct-query result and scope; prefer this finite lifecycle composition over
another theorem demo or new routing architecture. Source review should decide
the minimum adapter before any new network experiment. No implementation is
commissioned by this note, and it does not claim a complete global v5.
