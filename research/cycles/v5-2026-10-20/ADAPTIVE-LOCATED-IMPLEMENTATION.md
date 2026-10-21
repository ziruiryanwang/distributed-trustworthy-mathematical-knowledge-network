# Adaptive located-query implementation checkpoint

2026-10-20. Source implementation only; no imports, tests, process launch,
network activity, proof production, installation or acceptance performed here.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Exact source and public seam

New source: `software/v5/located_queries/client/located_queries.py` (384 lines).
SHA-256: `419df8428528203858eff69da43c7e3ed7e5634d06007dc5e30ca2f33df82c4e`.
Logical installed module: `client/located_queries.py`. Root owns later exact
selection and adoption. The current installed release stays unchanged.

```python
reserve_located_queries(client, channel, envelope, policy)
await next_located_query(client, specs, location_limits, search_limits,
                         routes=routes, descriptor_bytes=4096,
                         descriptor_age_ms=60000)
```

The selection is `ADAPTIVE-LOCATED-SELECTION.md`, following design
`27cec9e66687eb67302361b4011a581feee75b813ff6397b006a75b3dd3334be`.
Use the authoritative 110-source mapping in
`experiments/v5-local-checks/distribution-discovery-01-input.json` plus the four
already adopted iterative-query successors. Portable location sources come
from `software/v5/portable_runtime/location/`, not older logical-path copies.
No existing direct-query, controller, workflow, checker or DHT source changed.

## Concrete behavior

The helper implements the validated client's existing optional envelope
protocol, rather than modifying its one-shot `find` or fabricating a handoff.
Reservation adopts the owner-selected pin for this helper; mathematical runtime
owners pin the selected v5 Python map, while portable location adoption remains
the channel launcher's responsibility. One fresh reader child transfers to
`client._channel` and starts at most once. Namespace, policy, original grant,
budget, adoption, role pins, configuration and output paths remain bound.

The envelope contains exactly `search` and `location`. Search has the existing
SearchSession fields and `generations` in 1..8; location has the existing
WorkflowBudget fields. Prepayment charges exactly:

`requests = L.route_operations + L.descriptor_requests + S.requests`

`reply_bytes = L.reply_bytes` (already includes `S.bytes`).

Generation allocation validates and consumes complete prospective vectors
before retirement, construction or I/O. No refund or renewal follows empty or
failed work. Additive search dimensions are providers, snapshots, requests,
pages, examined, candidates and bytes. Additive location dimensions are route
operations, routing events, routing peer slots, descriptor requests, contacts
and reply bytes. Wall limits and inflight are caps, not additive currencies.
The original child keeps its own cumulative command/IPC/transport limits.

Each query uses an actual ServiceLocatedWorkflow on that same child and the
existing observed-route and available-descriptor helpers. Their genuine ticket,
route-key, nonce, authenticated-peer, endpoint-policy, parser, settlement and
expiry checks remain in the path. The helper takes the actual `begin_search()`
result. Custody contacts retain each original absolute descriptor expiry; no
handoff-generated lifetime extension occurs.

Prior search, workflow, acquisition, candidate and staging scopes retire only
when quiescent. Genuine warrants, exact verified caches and persistent custody
are not cleared by rotation. Binding guards invalidate stale contact/helper
capabilities. The existing one-combined-import boundary is unchanged.

## Deadline and failure arguments

Root and independent review identified and corrected one important boundary:
generic identity checks must not require a still-open location connection.
A shorter search deadline or normally ended service cannot revoke local work
under the original mathematical grant. New located queries separately require
an unexpired envelope and live original channel. Search/custody transport keeps
its own actual endpoint expiry. An actual failed client action remains fail-stop.

A settled no-contact generation terminalizes its workflow immediately as
`RETIRED_NO_CONTACTS`, snapshots its scalar costs and permits another funded
query. The result is `NO_CONTACTS_IN_SELECTED_ROUTE_PLAN`, never global absence.
Malformed, expired or cancelled operations are not translated to this result.

Validation, allocation, retirement, construction and awaits are inside one
failure boundary. Partial workflow/search state is tombstoned before diagnostics;
allocated rows and charges remain. Original channel cleanup is awaited even if
diagnostic capture fails, then the existing decorator closes mathematical owners
and budget. `FAILED` survives later close. The caller still needs its ordinary
`finally: await client.close()`, including failures in decorator postchecks.

Reports use `DMKN_LOCATED_QUERY_ENVELOPE_V1` under `iterative_queries`:
fixed caps, monotone allocated vectors, at most eight scalar generation outcomes,
route termination/census summaries, last nonempty bounded route error,
descriptor-unavailability count, and one cumulative channel report. They do not
copy peer/route maps, full coverage or repeated acquisition ledgers. Route events
are explicitly not DHT wire bytes, and reports confer no mathematical authority.

## Review and next boundary

Author source inspection found the five-group control fixture compatible: its
ServiceLocatedWorkflow recorder patches `__init__`, not the exact class, and its
channel constructor preserves the real identity/path fields. Its transport and
issuer replacements are explicitly inert. Independent implementation review and
README are owned by core_growth; controls and their outcome audit by core_release.

Only root may select the one finite native-free composition run after source
clearance. No repeated passing direct-query campaign, native proof graph or
large distribution rebuild is implied by this checkpoint. Full v5 remains open.
