# Minimum same-lifetime adaptive located-query composition

2026-10-20. Proposed source contract, not implementation or launch authority.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Basis/line trace: `ADAPTIVE-LOCATED-COMPOSITION.md` (SHA-256 `3b3cc152...7433b`).
Reuse selected 110-source map plus the four iterative-query successors. Keep
all used sources and evidence unchanged. No new DHT, checker, grant or daemon.

## Exact proposed source/API boundary

One new helper: `software/v5/located_queries/client/located_queries.py`, installed
as logical `client/located_queries.py`. Separate `README.md` and `controls.py`
live under `software/v5/located_queries/`. No existing core source is edited.
The helper uses the tested exact validated CommonsClient and its optional
same-object envelope `check(client)`, `report()`, `terminal(status)` protocol.
It must not call direct `bind/next_query`, reset `find`, or impersonate a handoff.

Proposed public calls, using existing serialized action decorators:

```python
reserve_located_queries(client, channel, envelope, policy)  # no I/O
await next_located_query(client, specs, location_limits, search_limits,
                         routes=routes, descriptor_bytes=4096,
                         descriptor_age_ms=60000)
```

`envelope` has exactly `search` and `location`. `search` has existing
SearchSession limit fields plus `generations` in 1..8. `location` has existing
WorkflowBudget limit fields. Keep their existing ranges; no peer-chosen limits.
One absolute deadline is fixed at reservation as min(original grant deadline,
now + search.wall_ms, now + location.wall_ms). Each generation may be shorter.
Inflight is a fixed cap, not an additive work allowance.

## Original authority and child ownership

Reservation requires a fresh query slot, no search/acquisition/handoff/channel,
the exact validated client and exact unstarted ServiceLocationProcess, reader
role, original grant deadline, unchanged adopted workspace/output containment,
and namespace/egress equal to adapter.namespace/policy._config. Preserve the
fresh-child checks of DeltaLocatedHandoff, including no pending start/close task,
no process, no command/frame/byte history, no failure or closed state.

Capture the original channel, adoption identity, config, role pins, policy and
namespace; do not freeze its legitimately increasing sequence/traffic counters.
Register the new helper's source origin and owner-selected pin before
use. Any reused private helper module also needs its origin/pin registered; a
new file's hash alone does not adopt transitive code. Prefer self-contained small
located state over inheriting direct-envelope assumptions about channel=None.

Prepay once, set `_query_used=True`, bind `_query_envelope` and its original
identity, and transfer channel to `client._channel`. Leave `_handoff=None`.
The original inherited async `client.close()` then owns child teardown. Start
this SAME child at most once, inside the first funded next-query call. Retain
all real issuers, original AcquisitionBudget, grant, warrants/caches and imports.
Normal envelope checks validate identities/configuration without creating owners.

## Nonrefundable accounting, without double-counting search bytes

Let S be the search envelope and L the location envelope. Existing L.reply_bytes
already INCLUDES S.bytes; require L.reply_bytes >= S.bytes + 1024, as in the
existing WorkflowBudget. Reserve once through unchanged `charge_external`:

`requests = L.route_operations + L.descriptor_requests + S.requests`
`reply_bytes = L.reply_bytes` -- NOT `L.reply_bytes + S.bytes`.

For generation i, atomically debit full prospective vectors l_i and s_i, after
validating all dimensions but before retirement, construction or any I/O. Require
sum(l_i) <= L for route_operations/routing_events/routing_peer_slots,
descriptor_requests/contacts/reply_bytes, and sum(s_i) <= S for all seven search
dimensions. Each l_i.reply_bytes includes its s_i.bytes. Repeated peers/contact
slots and failed/empty generations consume allocations again, with no refund.
Validate each explicit route plan exactly as current find does; summed route
events, peer slots and descriptor counts must fit its generation allocation.

Actual acquisition still charges original B after the combined prepayment.
Logical route attempts are NOT DHT packets; event caps are NOT wire-byte bounds.
Retain the single Node service's original command/transport/metadata/deadline
limits and Python IPC sequence/frame/byte limits. Never restart it to evade a cap.
Costs and incompleteness remain explicit; no global scan or universal recall claim.

## One generation lifecycle

Before replacement require no active client call other than this serialized
action, shared acquisition ticket, search pending/reserved work, structural
inflight/reserved bytes, pending workflow ticket or concurrent channel command.
Validate next inputs, debit both vectors, and create a bounded generation row.
Retire old search/acquisition with the existing narrow retirement method; clear
candidate/staging lookup maps, not cumulative counters or authentic warrants.
Mark the old WorkflowBudget terminal too, including a no-search generation.

Construct one actual ServiceLocatedWorkflow for the new query on the SAME child;
record it as the current generation BEFORE awaiting start/route/descriptor work.
Clamp its workflow and search deadlines to the fixed envelope deadline once,
before issuing tickets. It has a new local query scope, not new aggregate funds.
Use existing `observed_route.route` and `available_descriptor.descriptor` helpers,
not raw equivalents: retain their diagnostics, typed unavailability, authentication,
conservative settlement and fail-close behavior. No provider enumeration/crawl.

If settled selected routes/descriptors yield no usable contact, mark the workflow
terminal and row `NO_CONTACTS_IN_SELECTED_ROUTE_PLAN`; leave search/acquisition
None and the envelope reusable within remaining limits. Descriptor-unavailable
counts are charged. Determine usability from the actual retained endpoint map
and its original absolute expiries, not an accumulated set of labels. A race or
overall-budget expiry still fails closed. Do NOT translate malformed data, authentication failure,
budget expiry or cancellation into this normal no-contact result.

For contacts, use the actual workflow's `begin_search()` return, not a duplicate
SearchSession. Its endpoint map and ORIGINAL per-endpoint absolute expiries are
the exact input to EvidenceAcquisition with generation-bound ExpiringContacts.
Never set descriptor-derived expiry to now + descriptor_age_ms at handoff.
The guard checks original budget/policy plus exact current channel, workflow,
search/acquisition and envelope identity. Old labels cannot authorize new endpoints.
Set acquisition._search to that search and acquisition._handoff=None; do not
fabricate DeltaLocatedHandoff. Inherited semantic-reader identity guards apply.

## Faults, cancellation and final report

At most one generation is live. A failed next-query construction/retirement keeps
both vectors and the row; no restoration, retry or second reservation occurs.
Mark status and tombstone every partial workflow/search BEFORE diagnostics,
even if no search/acquisition was created. Preserve FAILED through later close.
Unexpected faults or cancellation await the same channel's existing close path
and inherit client fail-stop/owner cleanup; original final client.close remains
required and child close is idempotent. No detached task may outlive rotation.
Existing helper finally blocks settle tickets; if settlement is uncertain,
record it and terminate instead of declaring a new query safe. Never let a
diagnostic exception skip original cleanup or erase consumed allocations.

Report through existing `iterative_queries` field with a distinct located schema:
S/L caps and allocated vectors, at most eight compact generation outcomes,
original fixed deadline, scalar search/location counters, and one channel report.
Do not copy peer/route maps, coverage or repeated cumulative acquisition ledgers.
Keep logical attempts, descriptor bytes, HTTP bytes, DHT transport and IPC costs
distinct. One combined import remains the capability; no sealed-context renewal.

Stop for root selection after independent source challenge. The later smallest
test boundary is new located composition/parsing/lifecycle, not repeated proof
production or re-running all already-qualified direct-query controls.
