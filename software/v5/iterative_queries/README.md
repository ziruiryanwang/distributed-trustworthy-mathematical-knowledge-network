# Several queries, one finite mathematical operation

This optional direct-contact successor lets a local agent search for one result,
acquire and check it, then search for another without losing the first result's
live warrant. The mathematical checkers, proof forms and trust policy do not
change. This source successor is not installed merely by importing this folder;
the owner must select its exact sources in the ordinary distribution/runtime map.

## Why use it?

An agent may learn which second query to ask only after inspecting the first
result. Previously the direct-contact helper allowed one query per live client.
Starting a new operation remains valid, but discards that operation's live
warrants and verification cache. This option preserves those owners while
retiring each old search's candidate and supplier handles.

It does not choose research questions, retry failed requests, discover new
contacts, provide more computation, or promise useful results. Existing one-shot
`bind` and located `find` callers remain available and unchanged in purpose.

## Caller sequence

With a fresh validated `client`, an already authorized `policy`, and exact
owner-selected contact records, use the public direct-contact helper:

```python
from client.direct_contacts import reserve_queries, next_query

reserve_queries(client, {
    "generations": 2,
    "providers": 4, "snapshots": 8, "requests": 32,
    "pages": 16, "examined": 2048, "candidates": 64,
    "bytes": 4 * 1024**2, "wall_ms": 60000, "inflight": 1,
}, policy)

per_query = {
    "providers": 2, "snapshots": 4, "requests": 16,
    "pages": 8, "examined": 1024, "candidates": 32,
    "bytes": 2 * 1024**2, "wall_ms": 30000, "inflight": 1,
}
next_query(client, first_contacts, first_specs, per_query)
# Use the ordinary search, resolve, acquire/admit APIs. Retain real warrants.
# Finish required semantic acquisition and await every request before rotating.
next_query(client, second_contacts, second_specs, per_query)
# Collect the second result, then import the chosen warrants together ONCE.
# Close the client with the ordinary caller-owned cleanup when finished.
```

The two queries need not be chosen in advance: `second_specs` can depend on the
first result. Both must compile under the same configured index profile and
namespace. The original grant must have room for the entire search reservation
**plus** subsequent acquisition/admission; the example is not a suitable budget
for every workload. Contact lifetime is bounded separately and is never renewed
for old handles. There are at most eight generations in a plan.

## What remains bounded?

Reservation occurs before any search or acquisition request. Its request and
reply-byte allowances are prepaid once into the original acquisition ledger.
Each query consumes its whole selected allowance in every additive dimension:
providers, snapshot attempts, requests, pages, examined rows, candidates and
reply bytes. Unused allowances and failed construction attempts are not refunded.
Repeated providers, scans and candidates consume another generation's allowance.
Distinct provider labels do not establish independent operators.

The plan fixes one absolute search deadline, no later than the original grant.
Per-query wall limits can shorten it, never renew it. `inflight` is a concurrent
cap, not an additive allowance. Original CPU, admission, storage, staging and
input limits remain. The optional `iterative_queries` report separates compact
generation accounting from aggregate reservations and the shared acquisition
ledger; reserved bytes are not the same as actual wire bytes.

## What survives a query change?

Live checked warrants, their original owners, verified receipt/packet caches,
immutable custodied data, and the operation's cumulative counters survive.
Old candidates, unadmitted staging tokens, contacts, search clients and semantic
readers cannot be used as the next generation's authority, even when a provider
label is reused. Finish a staged acquisition before rotating, or retain its
bytes and use the ordinary local admission route later. Old helper `close()` and
inert reports remain usable without closing the current client.

A query change requires quiescence: no pending search reservation, acquisition
request or structural transfer. An unexpected retirement/construction failure
fail-stops the operation with its charges preserved; it does not restore a
possibly uncertain old generation. The caller still owns terminal cleanup.

Collecting A and B before one combined import is supported. A READY authoring
context remains sealed; this feature does not add B to it, reuse a consumed
authoring owner, or let a finished `SemanticReader` import a second context.
Use ordinary acquisition/admission calls when collecting several independently
searched components for that single import. `SemanticReader.finish()` still
performs its existing admission-and-import transition for its own selection.

No new proof production, global completeness, measured growth improvement, or
final-v5 readiness follows from this lifecycle change alone.
