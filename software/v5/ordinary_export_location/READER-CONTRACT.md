# Ordinary ExportID receive integration

2026-10-28. Source-only implementation under `SELECTION.md`; no execution,
syntax compilation, imports, network calls, owner/database opens or tests were
performed by this author. Runtime qualification and adoption remain root-owned.

## Public entry and exact configuration

The unchanged pinned `ordinary_registration_refresh/peer.py` reads the complete
configuration object and passes it unchanged to `api.receive`. The fresh
`peer_api.py` accepts optional `export_location` only with
`dependency_policy: "bounded-closure"` and all three existing explicit fields
`acquisition_sources`, `attempt_timeout_ms`, `finalization_reserve_ms`.
Without that optional object, the existing receive path is retained.

Example optional object (the contact label must already exist in `contacts`):

```json
{
  "gateways": ["ordinary-gateway"],
  "egress": {
    "schema": "DMKN_V5_OWNER_EGRESS_V1",
    "mode": "public-ipv4",
    "public_ports": [443],
    "test_endpoints": []
  },
  "limits": {
    "requests": 8,
    "reply_bytes": 65536,
    "demands": 8,
    "descriptors": 64,
    "unique_origins": 16,
    "max_providers": 8,
    "max_descriptors": 8,
    "max_bytes": 8192,
    "max_age_ms": 60000,
    "attempt_timeout_ms": 5000
  }
}
```

These are illustrative owner-selected caps, not added grants. Receive's existing
`limits.requests` and `limits.reply_bytes` describe the original aggregate grant
including this prepaid slice. The demands cap cannot exceed receive's missing
frontier cap. Exact numeric ranges are `O.EXPORT_LOCATION_LIMITS`; the whole
object has exactly `gateways`, `egress`, `limits`. There are one to eight distinct
configured gateway labels. Loopback qualification uses the existing explicit
`loopback-test` egress policy, never a remotely supplied trust policy.

## Original accounting and exact-demand authority

After configuration and wrong-parent checks, and before preview/evidence I/O,
`ExportLocationClient` calls unchanged `OrdinaryBudget.charge_external` once.
The original request/reply slice is fully prepaid, with no refunds or top-ups.
An existing ledger with `sequence > 0` refuses before I/O. Lookup request,
descriptor, reply-byte, demand and distinct-origin subcounters enforce that
slice; descriptor ceilings are conservatively consumed on every lookup attempt.
Metadata subcounters explain the prepaid charge and are not added a second time.

For each missing `(SemanticID, ExportID)`, the reader privately binds the expected
name, tries distinct configured suppliers first, then at most the remaining
slots from one bounded location result. One visited set permits eight exact
endpoint identities total, with at most a locator and evidence call per identity
(sixteen ordinary calls). Eight configured identities leave no learned slot.
Endpoint identity includes numeric host, port, TLS, server name and CA-file trust
binding; configured CA pins remain rechecked by the existing live-budget checks.
The independent learned-endpoint policy uses owner system CA trust, as reported
by the unchanged egress policy. Same endpoint under a different trust binding
is a different exact identity. The original request/byte/deadline limits may
stop before any of these ceilings.

Learned reads reuse the same `OrdinaryAcquisition`, HTTP counters, custody and
ledger. A private frozen authority selects the endpoint without adding mutable
entries to its configured table. It binds the exact demand/name, policy bytes,
endpoint bytes and original expiry; the evidence authority additionally binds
the exact locator-derived UnitID. The same expiry is checked before request
admission, through transport setup/dial, and before validation/retention. A failed
begun call is fully settled before any availability exception can escape. An
expired authority after a begun attempt is terminal. Already retained units
still require the exact output-name census check. Preflight and native admission
are unchanged and synchronous.

Only the existing narrow settled transport unavailability and HTTP 404/503 permit
another ordinary supplier. Malformed bytes, binding errors, TLS/authentication
errors, uncertain cleanup and budget expiry remain terminal. Empty bounded
location results, prepaid-slice exhaustion and eight-candidate exhaustion never
claim global absence. Reports retain aggregate counters without an unbounded
per-attempt history.

## Gateway and lifetimes

`gateway.py` loads separately as `transport.ordinary_location_gateway` after the
concrete controller. `Gateway(controller, policy=..., limits=..., deadline=...)`
validates before startup and permits an unstarted channel. Every lookup checks
the running controller, immutable owner configuration and policy. The operator
starts Node, then binds HTTP; root owns lifecycle and teardown. One fail-fast
busy owner spans locate, every descriptor and response construction because the
backend peer cache belongs to that lookup. No waiter queue is created.

The HTTP lookup cutoff bounds lookup, descriptor and response work. A returned
hint is separately clipped by the original gateway/controller service cutoffs,
policy max-age and the descriptor duration anchored at descriptor-command start.
It may remain useful after the lookup's execution cutoff. Reader duration is
anchored at the earlier HTTP-request start and clipped by its original receive
acquisition deadline. Duplicate hints within that exact demand narrow to the
earliest expiry, including across gateway attempts; a different missing demand
may obtain a fresh hint under the same aggregate grant. Neither path renews an
existing authority or service grant.

The exact authenticated negative descriptor `NOT_ADVERTISED` represents stale
DHT metadata after local revoke and produces no candidate. Malformed negatives,
wrong peer/key/nonce and uncertain channel teardown remain terminal. See
`WIRE-CONTRACT.md` for closed schemas. Gateway reply construction encodes a bounded
prefix that fits the full selected reply cap, with explicit truncation.

Malformed or wrong-semantics incoming HTTP requests fail before gateway work.
A terminal backend failure halts HTTP admission and sends a bounded terminal
HTTP 400 when the original response deadline still permits framing. The gateway
report records terminal failure; root treats it as operation failure.

## Loader cut and source review scope

The reader keeps its existing closed SUPPORT set. Its four source successors
are `ordinary_acquisition.py`, `fair_exchange.py`, `http_provider.py`, and
`peer_api.py`. The existing module names hold the client/wire logic and async
route; the new operator-only gateway/controller are not imported by ordinary
reader startup. No `owner.py`, `profile.py`, native or module-anchor projection
is edited here. The provider only lazily imports the separately loaded gateway
when that concrete operator role is explicitly supplied.

Source inspection covered the changed call path, exact wire binding, accounting,
bounded state, lifetime propagation, loader order and public CLI pass-through.
Independent source review and root-selected focused runtime controls are still
required; this document asserts no runtime or mathematical result.
