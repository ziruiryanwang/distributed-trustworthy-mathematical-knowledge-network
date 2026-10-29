# Owned ordinary acquisition contract

2026-10-28. Implements only the two-helper source cut selected in `SELECTION.md`.
No runtime, import, socket operation, owner/database open, native work, benchmark
or Git operation was performed. Independent source review and root-owned assembly,
compatibility checks and finite runtime selection remain separate gates.

## Exact source cut

| Role | Preserved predecessor SHA-256 | Fresh successor SHA-256 |
|---|---|---|
| `ordinary_acquisition.py` from `../ordinary_multi_source/` | `076130f7a34b505df33ee550501d1c4276bb46e408ff226df765225933a0658e` | `677b6a6acd17de5ad60dbdd5700aac3014fc7a571876757b39382f8642f6d37e` |
| `fair_exchange.py` from `../ordinary_connect_ownership/` | `05cf2b5baef0130dbe3b43e594d6c800baf6b625c77125dd3356f59f78509575` | `a04c4577a4fd6b3f68a48a869397d5ee35ec5075f7e5c1c496f5bb31fb06fc9a` |

The copies were hash-verified against the predecessor before editing. Only the
ordinary helper's module description and `_fetch` change. The exchange helper
changes its module description and closed route allowlist; socket ownership,
framing, timers, cancellation and closure code remain byte-for-byte identical.
No used source or distribution was modified.

## One original deadline and ticket

`_fetch` records `attempt_started` immediately on entry, before request validation
or lazy module loading. After the unchanged request checks and `budget.begin`,
the ticket's existing `try/finally` computes and retains

`min(original_budget.deadline, attempt_started + cap_ms / 1000)`.

`cap_ms` is the caller's validated explicit attempt cap, or the existing 60,000 ms
per-exchange ceiling. The call still computes the original ledger's remaining
milliseconds and clips the relative timeout by an explicit attempt cap. It also
passes the absolute horizon to `fair_exchange.exchange`, so later request/TLS/
address setup cannot renew the attempt or original grant. A local delay can
shorten an attempt; it cannot grant new time.

`fair_exchange` is imported inside the begun-ticket `try`, preserving the
existing package loader's module order. A failed import is terminal and still
settles the begun ticket. Both default and explicit-unavailability calls use
this one owned exchange; there is no old-transport fallback branch.

The exchange already rechecks its original absolute horizon after local setup
and before socket allocation/connect. The async timer does not preempt TLS/CA
setup, request encoding or other synchronous work. Its existing up-to-one-second
close observation remains outside the attempt timer and needs the existing
outer cleanup allowance. Original ledger liveness is still checked before
validation, before/inside retention and before returning a retryable outcome.
No new ledger, timeout renewal, refund or hidden retry is added.

## Exact failure boundary

Owned exchange returns either a framed response dictionary or a `SettledRefusal`
value. The latter is not an exception. Only the following returned values become
`AcquisitionUnavailable`, and only with existing `unavailable_errors=True`:

| Owned settled reason | Existing ordinary reason |
|---|---|
| `ATTEMPT_TIMEOUT` | `ATTEMPT_TIMEOUT` |
| `CONNECTION_REFUSED` | `CONNECTION_REFUSED` |
| `CONNECTION_RESET` | `CONNECTION_RESET` |
| `BROKEN_PIPE` | `BROKEN_PIPE` |
| `PEER_EOF` | `INCOMPLETE_READ` |

An `HTTP_PROTOCOL` refusal is terminal even in explicit-unavailability mode.
Unknown reasons and every default-mode settled refusal raise terminal
`ValueError("ORDINARY_ACQUISITION_TRANSPORT_" + reason)`. Default behavior remains
no retry; the old raw exception class is not preserved for returned owned
refusals. Cancellation, TLS failures, uncertain close/handoff and unknown local
exceptions propagate without conversion. In particular, the owned transport does
not classify `ConnectionAbortedError` as a settled refusal, so it remains terminal.

Complete framed 404/503 responses retain their existing opt-in ordinary
unavailability handling. Default-mode 404/503, HTTP 400 and invalid/mismatched
payloads remain terminal. No transport outcome is global absence, mathematical
acceptance or independent authority to contact another provider.

Every begun attempt consumes one request. The unchanged `finally` settles a
failure at its full reply cap; success charges the validated raw length only
after all required liveness and retention checks. Only after settlement and an
additional original-budget liveness check can `AcquisitionUnavailable` escape.
Failed settlement, an expired grant and cancellation therefore cannot authorize
the next supplier. Existing HTTP completed/failed counters and conservative
request/header bounds retain their meanings; failed partial transport bytes are
not presented as a complete measured response.

## Supported routes and unchanged checks

The owned exchange's existing closed discovery allowlist gains exactly:

- `/v5/ordinary/preview`
- `/v5/ordinary/locator`
- `/v5/ordinary/evidence`
- `/v5/ordinary/authoring-offers`

There is no arbitrary-route escape hatch. Existing `H.ROUTES` caps, ordinary
request parsers and exact response validators remain unchanged. Preview record
binding, locator S/ExportID/expected-name checks, evidence UnitID/output census,
optional inert custody and all public result shapes remain unchanged. Authoring
offers use their unchanged request/reply schema and default no-retry `_fetch`;
they do not enter custody, follow repositories or authorize source execution.

Configured providers, source scheduling and mathematical admission are unchanged.
No learned endpoint, group hint, DHT route, metadata API or new configuration is
introduced. Root must assemble a fresh auxiliary source map/profile and verify
unchanged installation and anchor-support identity. The frozen standalone inert
host does not include fair exchange and must not be silently patched with this
successor.

## Review and selected validation boundary

Source inspection should verify the two exact diffs, lazy import, absolute
horizon, five-reason mapping, fatal protocol/default behavior, conservative
settlement and unchanged validators. The independent reviewer owns focused
controls. The changed-boundary cases are late local setup preventing a dial;
settled refusal followed by a permitted typed success under one budget; full
failure charging; no fallback after protocol/unsettled/unknown/cancelled outcomes;
and all four typed routes including default advisory authoring offers.

Reuse the existing owned-socket ownership controls unless review finds a new
socket boundary. This source edit does not justify another mathematical proof
campaign. A source review or passing control does not itself adopt a package or
select any further runtime.
