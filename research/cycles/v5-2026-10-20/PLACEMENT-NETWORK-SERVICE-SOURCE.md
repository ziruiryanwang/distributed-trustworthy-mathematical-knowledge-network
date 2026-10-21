# Placement network service and durable route source

2026-10-21, core_growth. Source-only implementation under
`PLACEMENT-NETWORK-SELECTION.md`, following seam `e1514d57`.
No product imports, execution, tests, builds, networking or Git mutations.
Existing used controller/ledger/codec/Store/read-provider/Node bytes are unchanged.

## Exact source boundary

| New source under `software/v5/placement_network/` | Bytes | SHA-256 |
|---|---:|---|
| `placement/advertisement.py` | 14569 | `b5523f82f6d5eba4ba9e72639888f1c9da014f298aa9c1081c76aa3f920f35a6` |
| `client/serve_placement.py` | 19750 | `07c60c4f33401d41694228d0f6bde35d9148e769947b75211e9ed4098ec68674` |

`placement/network.py` belongs to core_release and is a separate coordinated
source/review. Root owns the later logical source map and execution selection;
these files have not been imported or installed. The exact selected local
controller is cleanup-fixed `ef1c9b59`; the core source control audit is separate.

## Public owner API

```text
PlacementService.open(
    workspace_path, workspace_config, placement_config, egress,
    exact_fresh_ServiceLocationProcess,
    read_endpoint=..., intake_endpoint=..., limits=..., outer_deadline=...,
    create=False, placement_create=False, journal_create=False,
    read_tls_context=None, intake_tls_context=None)
await service.start()
service.issue_token(source, write_until_ms=..., retention_until_ms=..., limits=...)
await service.close()
```

An async context manager is also available. This is a compact trusted-owner SDK
service, not a new command-line daemon or remote grant API. Root's ordinary owner
entry can call it directly. It supports early close after useful work; no need
to wait out the configured lifetime.

The source opens **one** exact fingerprint Workspace, existing placement ledger
and controller. It borrows the unchanged real `CompositeProvider` for reads
and owns one caller-constructed, fresh exact V1 `ServiceLocationProcess` for its
existing protocol/pinned runtime. The new placement listener is separate.
There is no projected index view, second Workspace opening, generic RPC, new
Node implementation, proof issuer or verifier.

`limits` is closed and contains:

```text
lifetime_seconds, controller_cpu_seconds, controller_calls,
health_interval_ms, journal_pages,
read = {max_connections,max_requests,max_reply_bytes,operation_ms},
intake = {max_connections,max_requests,incoming_bytes,outgoing_bytes,operation_ms}
```

Both endpoints are fixed, nonzero and distinct host/port pairs. The locator
config is V1 index-provider with `endpoints=[read_endpoint]` and exact namespace
and owner egress policy. Remote clients never choose the listener, TLS context,
runtime, mutable directory, source endpoint grant or budgets. TLS contexts are
trusted owner-created server contexts with TLS >= 1.2; no key/token bytes are
written by this module. Only `issue_token` returns a secret, privately to the
trusted caller. The service never persists that return in reports/config.

## Wire integration agreed with core_release

`PlacementProvider(service, limits=...)` calls the exact service's `_active`,
async `submit(token,manifest_bytes,until=...)` and synchronous
`status(token,request_id,until=...)`. Both return exactly `{placement,route}`;
the wire layer performs its own binding validation and bounded projection.
`service.bindings` exposes the four nonsecret fixed identity fields and
`service.deadline` the original finite monotonic cutoff. `_active` permits the
listener's construction/startup, but public submit/status require started state.

The controller's original receipt remains `INDEXED_UNADVERTISED`. The separate
wire route facet has precisely:

```text
status, cell, features, stripe, run_id, request_id,
observed_at_ms, add_provider_write, error_code
```

Only absent route observations use null run/request/time. Cell/feature/stripe
remain derived from the retained manifest. A prior same-cell result retains its
original run/request/time, not a fabricated per-request fresh dispatch.

Reviewer-found diagnostic boundaries are handled explicitly: noncommitted core
outcome details become only `{status:INCOMPLETE,code:PLACEMENT_INCOMPLETE}` before
return; arbitrary saved `reason`/exception strings are not emitted. Local route
journal observations may retain bounded exact Node diagnostics, but its public
facet includes only validated status/addresses/count/time and closed error codes.
The wire module separately sanitizes success observations and never copies raw
acquisition reports merely because the core receipt was successful.

The agreed intake request cap is at most 4,096, matching the wire module.
Its shutdown uses the service's original outer deadline, not a new allowance;
`stop` clears its server handle only after confirmed listener closure.

## Durable route journal and duplicate discipline

`PlacementAdvertisement` binds the exact controller/grant/provider/location and
original Workspace. One registered live journal is allowed on that Workspace.
Its fixed `placement-routes.sqlite` stores immutable config, bounded run
allocations and at most `generation.max_cells` route rows per permitted run;
the existing generation `max_runs` bounds lifetime history. SQLite page caps
remain real capacity limits; storage failure is refusal, not quota expansion.

At open, before any listener/process starts, one durable nonrefundable run
allocation reserves H health calls, L publications, L possible withdrawals and
one stop. Require `H+2*L+1 <= min(Node.commands,60)`, with
`L=generation.max_cells` and `L <= Node.advertised_keys`. This slice uses stop,
not per-cell withdrawal; the latter capacity is conservatively reserved.
Node transport, metadata, descriptor and background-maintenance budgets remain
the unchanged independent bounds. Unused route funding is not reset/refunded.

The coordinator authenticates and performs a primary-key request existence
check before calling the authoritative unchanged controller. It never treats
an arbitrary database error as absence. Exact request duplicates return saved
placement and route observations without journal mutations, route dispatch,
new acquisition or durable reservations. Ephemeral finite API-call accounting
still applies. New requests are serialized by the wire slot and a second
coordinator busy guard; there is no unbounded queue.

Only a clean successful controller return for a genuinely new request can
dispatch a cell. The authoritative derived receipt route is compared exactly
with the freshly compiled manifest fingerprint. The original token's write,
admission, retention and service bounds are checked before dispatch/commit.
A durable `DISPATCH_ATTEMPTED` charge precedes the actual existing `publish`
command. One opportunity exists per cell/run, even if dispatch is uncertain.

Positive state requires matching key, actual positive ADD_PROVIDER-write count,
no returned error and `HINT_DISPATCHED_UNACKNOWLEDGED`. A missing saved return
becomes `DISPATCH_UNCERTAIN`; it does not prove nothing was sent. A real returned
`INCOMPLETE` preserves that local intent may exist. No automatic retry follows
a lost response, failed journal commit or new contribution in the same cell.
Status can report a prior run's observation; it does not re-advertise an old
token. The first service API does not implement restart re-advertisement.

## Lifetime and cleanup

Active time is bounded by requested lifetime, the existing locator deadline and
the caller's original outer deadline after explicit read/intake drain, Node
stop/close and final margins. The existing controller receives an integer
wall interval rounded down, never an extension. Each request supplies an earlier
bounded deadline; the wrapper checks it and propagates cancellation without
changing the controller's exact grant. Synchronous Store work is still not
preemptible by asyncio; external whole-process containment remains required.

The HTTP request's `until` is not a replacement for the core service grant:
the wrapper checks it before/after the unchanged controller and surrounds the
await with an asyncio timeout, while the controller's custody/index precommit
guards retain their original service/token authority. Synchronous work can
therefore cross the earlier request cutoff and commit before the wrapper's
postcheck rejects. This is an uncertain HTTP outcome, not evidence of no write;
the caller observes the same request ID rather than assuming a safe retry with
a new ID. No strict no-commit-after-request-timeout property is claimed.

The tracked background monitor issues bounded existing status calls and starts
the same tracked close task at expiry or health failure. Explicit `close()`
can stop early. Teardown cancels/settles startup and health tasks, drains intake,
invalidates its write grant, stops/closes the locator, stops the read listener,
then closes journal/controller/Workspace only if no live intake/read actor
remains. A failed drain does not license closing SQLite under a running actor.
Such failure remains explicit and the caller's outer supervisor is the final
containment boundary. Close errors are never erased by later cleanup success.

Final report retains sanitized intake/read counters and existing Node lifecycle
report, alongside route funding/health counters. It contains no token or raw
exception text. TLS handshakes happen before asyncio's app callback; application
connection counts are **not** claimed to cap concurrent handshakes. Host/OS and
outer-supervisor exposure limits remain necessary for public deployment.

## Scope of this checkpoint

This is stable source for independent review, not an executed result. There
has been no new cryptographic certificate, mathematical admission, public TLS
qualification, independent-host pilot, completed renewal/GC, full-cost profit
or final-v5 claim. Root's next intended integration reuses retained evidence
and only two real Node roles: reader/bootstrap R and custodian B; source A needs
only ordinary read HTTP. After one submit and observation-only duplicate,
withdraw A and let R start goal-only discovery/acquisition. Runtime remains
separately selected after source and changed-boundary reviews.
