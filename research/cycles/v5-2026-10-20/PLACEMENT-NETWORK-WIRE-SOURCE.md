# Placement network wire: source checkpoint

2026-10-21, core_release. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

Implemented only the new wire module selected by
`PLACEMENT-NETWORK-SELECTION.md`. No import, syntax execution, test, network
launch, build, proof production, installation copy or Git mutation occurred.
This is source ready for independent review, not runtime or release acceptance.

| File | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/placement_network/placement/network.py` | 31301 | `1ec5c452ec129ae033f0577ebac6223e2cf3192d4724a3d31fe2e5c27a06cd4b` |

The wire composes with the unchanged current HTTP framing helpers, owner egress
policy, placement codec and ledger; it opens no databases and creates no new
mathematical checker. Its exact handler is the new `PlacementService` owned by
core_growth. That service owns the controller, route journal and locator.

## Callable interface

```python
provider = PlacementProvider(service, limits={
    "max_connections": ..., "max_requests": ...,
    "incoming_bytes": ..., "outgoing_bytes": ..., "operation_ms": ...,
})
endpoint = await provider.start(host="127.0.0.1", port=0, tls_context=None)
await provider.stop(until=original_cleanup_cutoff)
provider.report()  # status() is an alias

client = PlacementClient(
    egress, contact, expected, token,
    deadline=original_absolute_monotonic_deadline,
    requests=..., incoming_bytes=..., outgoing_bytes=..., operation_ms=60000,
)
result = await client.submit(canonical_manifest_bytes)
observation = await client.status(request_id)
client.close()
client.report()
```

`expected` is exactly `service_epoch`, `generation`, `namespace`,
`wire_profile_id`, all fixed hexadecimal identities. `contact` is an explicit
owner-selected endpoint validated by `OwnerEgressPolicy`. It is not a descriptor
chosen by the locator. The service supplies immutable original bindings, its
intake deadline and its separately reserved original outer cleanup deadline.
Mapping-proxy service bindings are copied into a closed dict for wire use.

`submit` and `status` return:

```text
{
  response: {
    schema: DMKN_PLACEMENT_RESPONSE_V1,
    status: OBSERVED,
    bindings: expected,
    request_id: exact_request_id,
    placement: sanitized_core_public_row,
    route: closed_route_observation,
    mathematical_acceptance: false
  },
  acknowledgement: PEER_ACKNOWLEDGED | LOOPBACK_RESPONSE_OBSERVED,
  transport_assurance: SYSTEM_CA_TLS_OWNER_SELECTED_PEER |
                       EXPLICIT_PLAINTEXT_LOOPBACK_TEST,
  mathematical_acceptance: false
}
```

The TLS acknowledgement reports only that this authenticated endpoint returned
the validated observation. It is not a cryptographic custody proof, mathematical
acceptance, DHT acknowledgement or perpetual retention promise. Status is a new
bounded transport operation but never initiates placement recovery or dispatch.

## Closed wire contract and bounds

Two POST routes, one request per connection, canonical UTF-8 JSON bodies,
explicit Content-Length, `application/json`, connection close:

| Route | Exact envelope fields | Body ceiling |
|---|---|---:|
| `/v5/placement/submit` | `schema`, `token`, nested-object `manifest` | 17408 bytes |
| `/v5/placement/status` | `schema`, `token`, `request_id` | 1024 bytes |

Schemas are `DMKN_PLACEMENT_SUBMIT_V1` and `DMKN_PLACEMENT_STATUS_V1`.
Tokens are exactly 64 lower-case hexadecimal characters. The inner canonical
manifest stays at most 16384 bytes. No escaped-string/base64 expansion or
increased core manifest allowance is introduced. Header ceiling is 8192 bytes;
full response ceiling is 81920 bytes; route-facet ceiling is 4096 bytes.

Each accepted application connection nonrefundably reserves 25600 incoming
bytes and 90112 outgoing bytes before creating its handler task. The client
uses the corresponding reverse-direction reservations before connecting.
Malformed, busy and closed-error connections consume the same allowances.
There are at most 4096 accepted requests and at most eight concurrent handlers,
with one active intake action. No unbounded action queue or automatic retry is
created. A finite owner may select much smaller caps. Exhaustion closes the
listener; overflow handler admission closes the connection rather than queuing.

Observed byte counters are lower-bound observations when a frame is malformed
or cut short; nonrefundable fixed reservations cover the authorized unknown
tail. These are application read/write authorizations, **not a bound on arbitrary
TCP ingress, kernel buffers, TLS handshake work or Internet denial of service**.
TLS occurs before the asyncio application accept callback. Finite handshake and
shutdown timeouts exist, but external process/OS exposure controls are still
required. Backlog is not advertised as a hard handshake-concurrency guarantee.

## Projection and binding checks

The existing local ledger receipt remains immutable and keeps its original
`INDEXED_UNADVERTISED` status. Its nested route remains `INTENT_ONLY`. The new
route facet is separate, always with exactly:

```text
status, cell, features, stripe, run_id, request_id,
observed_at_ms, add_provider_write, error_code
```

It permits only `NOT_ATTEMPTED`, `DISPATCH_ATTEMPTED`,
`HINT_DISPATCHED_UNACKNOWLEDGED`, `INCOMPLETE`, `DISPATCH_UNCERTAIN`.
The cell and one feature are always present; stripe is integer zero. Only an
unattempted route has null run/request/time and zero dispatch writes. A positive
hint requires positive writes and no error. All other errors are closed codes.
Historical same-cell observations retain their original request, run and time.

Incomplete core outcomes are null or reduced to:

```json
{"status":"INCOMPLETE","code":"PLACEMENT_INCOMPLETE"}
```

Raw saved controller `reason`, exception names/messages, Node `error`, and
`census.last_query_error` cannot pass the wire projection. Success receipts are
closed-field validated, including record/snapshot identities, object byte/hash
bindings, sorted unique bodies and route-key derivation from its feature and
namespace. The route feature must be included in the committed record.
The successful `observed` projection keeps only `structural_input_bytes` and
`new_store_logical_bytes`; nested acquisition/census diagnostics remain local.
Received projected receipts have their own exact smaller observation schema;
no fabricated validation placeholders are used.

The client independently derives submit request identity from the canonical
manifest, token digest and expected generation. It validates the complete reply,
expected service bindings and requested export/packet/hash/size/retention/cell,
plus exact requested body-hash sequence and each body's declared byte ceiling.
A status request verifies its requested identity but has no manifest to compare.
Mathematical reception remains the independently checked read-side workflow.

## Errors, uncertainty and teardown

Public server errors are only `INVALID_REQUEST`, `BUSY`,
`REFUSED_OR_INCOMPLETE`, or `SERVICE_UNAVAILABLE` within the closed error schema.
There are no request/body logs, arbitrary headers, token-returning status fields,
exception strings or remote token-vending route. Client exceptions have closed
codes and a conservative `uncertain` flag. A submit transport/response failure
may follow a committed placement; callers must observe the same request rather
than infer rollback. No new nonce, grant or automatic retry is generated.

The owner-selected public client uses system CA/hostname verification and
TLS >= 1.2; no downloaded CA or verification bypass is supported. Explicit
allowed plaintext loopback produces only the loopback observation label.

Provider start closes its accepting listener after a partial-start exception,
retaining its handle for owner cleanup. Stop closes intake, cancels/drains
tracked handlers and closes all retained writers under a cutoff no later than
the original pinned outer deadline. Successful stop sets `server=None` and
requires no remaining tasks/writers or cleanup errors. Reports expose active
connections/intake, retained closing connections, requests/reservations,
completed actions and cleanup/error counters. The service must not close its
databases underneath a remaining actor when stop is uncertain.

Client cleanup failure refuses successful return and closes further client use.
Its busy flag clears even if cleanup itself is cancelled. The per-operation
deadline never refreshes its original client deadline. Framing allows the
multiword HTTP reason phrases used by closed 400/503 responses.

Independent source review caught and corrected two client failure-boundary
defects before execution. Any caught in-flight submit error, including the
final expiry/binding check after receiving a committed reply, is now recreated
with its closed code and `uncertain=True`; a definite pre-reservation rejection
remains definite. No external exception is mutated or reused. The immediate
`writer.close()` call is inside the cleanup exception guard as well as
`wait_closed()`: either ordinary cleanup failure reports `CLEANUP_UNCERTAIN`,
closes further client use, clears busy and does not expose its raw diagnostic.
These are source corrections, not passed controls; the independent control
author adds memory-stream regressions for both exact boundaries.

The final accounting review also identified cancellation first occurring in
writer cleanup: it bypassed the earlier send-side cancellation handler. A local
at-most-once helper now records submit uncertainty at either cancellation site
and at ordinary final failure. Cleanup-only cancellation is counted, while
send-plus-cleanup cancellation cannot double count. Cancellation still
propagates and cleanup cancellation closes client use and clears busy. Two
additional subcases within the existing client control cover these boundaries;
no extra campaign or changed outer allowance follows.

## Next narrow evidence boundary

Independent reviewer owns source objections; root owns exact source selection,
small changed-boundary controls and any actual network integration. Relevant
new controls are closed projection/secret hygiene, exact bounds, uncertain
submit followed by observation-only replay/status, one-intake/finite traffic,
and failure cleanup. Do not repeat the passed twelve local-placement controls,
native integration, old proof campaigns or an entire distribution copy.

The consequential integrated path remains one real placement, exact replay,
publisher withdrawal and an independent goal-only reader acquiring retained
knowledge. This source checkpoint does not establish that outcome, public TLS,
independent hosting, full-cost growth, unlimited service rollover or final v5.
