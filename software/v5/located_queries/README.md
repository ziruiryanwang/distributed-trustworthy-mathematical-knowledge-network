# Adaptive discovery without preknowing provider endpoints

This optional helper lets one finite live mathematical operation locate providers
for query A, acquire checked mathematics, and then locate providers for a different
query B. The original warrants survive. It reuses one existing location child,
authenticated service descriptors, formal indexes and mathematical checkers.
It is a source successor, not an automatic update to an existing installation;
the owner must select its exact sources and runtime through the ordinary process.

The local agent decides each query and route plan. There is no mandatory research
agenda, global ledger, automatic retry, provider census or central math server.
Joining a network still requires some bootstrap knowledge; a finite route plan
cannot discover disconnected participants or prove that a theorem does not exist.

## What the owner supplies

Use a fresh validated `CommonsClient`, its original finite grant, an exact fresh
reader `ServiceLocationProcess`, and the owner's `OwnerEgressPolicy`. The child
must use the matching namespace/egress policy, original grant deadline and
authorized disjoint output locations. Its existing deployment configuration,
source pins and transport bounds remain mandatory. Do not reuse an old child,
reset its counters or issue out-of-band commands after transferring it.

The helper takes ownership of that same child through the client; ordinary final
`await client.close()` performs teardown. The caller must still use its usual
`try/finally` cleanup. No source example here bypasses actual trust adoption or
process containment, and no new issuer is created by a search result.

## API and an example allocation

```python
from client.located_queries import reserve_located_queries, next_located_query

search_slice = {
    "providers": 2, "snapshots": 2, "requests": 4, "pages": 2,
    "examined": 64, "candidates": 16, "bytes": 256 * 1024,
    "wall_ms": 30000, "inflight": 1,
}
location_slice = {
    "route_operations": 1, "routing_events": 16, "routing_peer_slots": 4,
    "descriptor_requests": 1, "contacts": 2,
    "reply_bytes": search_slice["bytes"] + 4096, "wall_ms": 30000,
}
search_totals = {**search_slice, **{key: 2 * search_slice[key] for key in (
    "providers", "snapshots", "requests", "pages", "examined", "candidates", "bytes")},
    "wall_ms": 60000, "generations": 2}
location_totals = {**location_slice, **{key: 2 * location_slice[key] for key in (
    "route_operations", "routing_events", "routing_peer_slots", "descriptor_requests",
    "contacts", "reply_bytes")}, "wall_ms": 60000}

reserve_located_queries(client, channel,
    {"search": search_totals, "location": location_totals}, policy)

features = client.workspace.adapter.compile_query(first_specs)
result = await next_located_query(client, first_specs, location_slice, search_slice,
    routes=[{"features": features, "stripe": 0, "event_cap": 16,
             "peer_cap": 4, "descriptors": 1}])
# If contacts are ready: use ordinary search_offer/search_page/resolve/acquire.
# Finish desired semantic acquisition and keep actual admitted warrants.
# Form second_specs from what was learned, compile its route features, and call
# next_located_query again within the SAME envelope; then import both selections.
```

This is an API fragment inside an already adopted owner operation. The sample
chooses only one route/stripe and at most one peer descriptor per query: it can
miss useful work. Budgets must be chosen for the actual workload. The original
grant must cover this entire search/location prepayment PLUS later mathematical
acquisition, admission, authoring and storage. At most eight generations are
allowed, and the plan never guarantees that every nominal generation fits.

## Accounting that does not restart

Location `reply_bytes` already includes search `bytes`. Initial prepayment is:

- Requests: location route attempts + descriptor requests + search requests.
- Reply capacity: location `reply_bytes`, not location plus search again.

Each generation consumes its full prospective location/search slices before
retirement, construction or I/O. Unused slots, failures and empty results are
not refunded. Repeated providers/contact slots count again. The plan fixes one
absolute deadline; shorter per-query deadlines do not extend it. Original CPU,
source/input, staging, admission and storage limits also remain in force.

The fixed envelope deadline or normal end of the location service bars new
located work; it does not by itself revoke already checked mathematics before
the original mathematical grant expires. An individual query's shorter deadline
ends that query's search, not the remaining funded generations. Identity and
configuration must still match. An actual failed operation remains fail-stop;
this is not recovery from failure.

Route-event counters are not DHT packet counts or wire bytes. The same child
retains its separate transport bounds and IPC counters. Reports distinguish
reserved allowances, actual/charged activity, incomplete route outcomes and
the single cumulative channel ledger. Multiple labels do not prove independent
operators, and bounded work does not imply complete semantic search.

## Lifetime, empty outcomes and failures

Descriptor-derived contacts keep their ORIGINAL absolute expiries through
search and custody. Handoff does not grant a new contact lifetime. Query changes
retire old workflow/search/contact/candidate/staging/helper capabilities, even
when provider labels recur. Actual checked warrants and immutable custody remain.

`NO_CONTACTS_IN_SELECTED_ROUTE_PLAN` means that the funded, settled selected
attempts supplied no usable contact; it is not global absence. Typed descriptor
unavailability may permit another caller-chosen generation within remaining
funds. Invalid metadata, authentication/IPC failure, cancellation and exhausted
deadlines do not become a successful empty result or automatic retry.

Rotation requires every prior request to be settled and awaited. An unexpected
construction/retirement failure preserves charges and fail-stops the operation;
there is no restoration of an uncertain old scope. Final cleanup must still run,
including when diagnostic reporting failed.

Collect A and B BEFORE one combined import. READY authoring contexts remain
sealed, and `SemanticReader.finish()` still performs its existing single import
transition. This helper does not extend a finished context or manufacture
mathematical authority from route, index or popularity information.
