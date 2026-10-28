# Ordinary exact-object replies within remaining service capacity

Source contract, 2026-10-28, under `SELECTION.md`. This successor changes only
the HTTP transport admission of ordinary evidence and locator requests.
No imports, tests, service calls, owner-state access or runtime qualification
were performed by the author. Root owns controls, integration and any later
finite runtime selection.

Baseline: `../ordinary_multi_source/http_provider.py`, SHA-256
`d9c342d1dcb5ee3e4b293e8dc0566397a321cc59a6f545e2f2afde452c760251`.
The fresh `http_provider.py` was copied with this exact hash before editing.
The sole source change is an eight-line branch after ordinary request validation
inside `Provider._serve`; the predecessor and all used evidence stay unchanged.

## Behavior

An independent client supplies the maximum bytes it accepts for a locator or
evidence unit. The provider has a separate finite aggregate service allowance.
Previously it required that the client's whole maximum fit that remaining
allowance before looking up the object. Thus a tiny unit could be refused
whenever an otherwise valid client maximum exceeded the service remainder.

The successor validates the original request with the unchanged
`ordinary_acquisition.request_limit`, then computes:

`remaining = max_reply_bytes - reply_bytes - reserved_reply_bytes`.

If `remaining < 1`, it refuses before dispatch using the existing
`PROVIDER_REPLY_QUOTA` failure. Otherwise, for ordinary locator/evidence only,
the private JSON-parsed request's `max_bytes` becomes
`min(original_max_bytes, remaining)`. That is also the reservation passed to
the unchanged aggregate admission check and reserved before dispatch.

The unchanged store performs an indexed length lookup before materializing
the selected BLOB. If the complete object exceeds the effective maximum or
is unavailable, it fails normally. If it fits, existing hash/identity checks
and the response-length check apply to the complete object. Actual body bytes
are charged before writing, and the effective reservation is released in the
existing `finally` block. Neither partial evidence nor a truncated locator is
ever returned as success.

Only the parsed transport-local dictionary changes. The caller's input is wire
bytes; no external caller dictionary is modified. Direct `dispatch` behavior
is unchanged. Original malformed, zero, negative, Boolean or above-protocol
maxima still fail validation before narrowing; narrowing cannot legalize them.
The new valid cap is positive and no larger than the already validated original.

## Aggregate accounting argument

Assume the existing supported model: protected provider counters and serialized
event-loop mutation, with no external mutation of the store/counters. Write:

- `B`: the fixed service body-byte allowance;
- `C`: cumulative body bytes already charged, including interrupted writes;
- `U`: sum of active reservations whose responses have not yet been charged;
- `D`: sum of active reservations whose responses have been charged but whose
  write/cleanup has not yet released the reservation;
- `Q = U + D`: the implementation's `reserved_reply_bytes`.

The actual accounting invariant is `C + U <= B`, hence `C <= B`. In contrast,
`C + Q <= B` is **not** a continuous invariant: retained charged reservations
in `D` deliberately double-count capacity during writes.

Initially all counts are zero. Admission requires `C + Q + r <= B` for the
new positive reservation `r`. For the two changed routes, choosing
`r = min(original_cap, B - C - Q)` preserves that check. Since `D >= 0`, adding
`r` to `U` preserves `C + U <= B`. Computing the remainder, narrowing the
request, checking aggregate capacity and adding the reservation contain no
`await`, so another connection cannot spend the same available capacity in
between under the event-loop model.

Before charging, dispatch and response validation are synchronous, with no
suspension. A successful response has length `b <= r`. At charge time,
`C` increases by `b`, the conceptual uncharged reservation `r` moves from `U`
to `D`, and therefore `C + U` changes by `b - r <= 0`. The implementation keeps
the reservation in `Q` until its unchanged `finally` block. Subsequent writes
can suspend, fail or be cancelled without undoing `C`.

A failure before charge removes `r` from `U` on release and cannot increase
`C + U`. Release after charge removes `r` from `D` and leaves `C + U` unchanged.
This proves bounded cumulative charged output and excludes concurrent
overcommit of outstanding uncharged responses. Other routes keep their existing
reservation and validation paths and satisfy the same transition argument.
Negative conservative remainder while charged writes are still live causes a
refusal; the successor does not reinterpret that as available capacity.

Header accounting remains separate. This is a body-byte proof, not a new total
wire-byte or process-resource claim. Connection/request counts, operation times,
the service deadline, cleanup ownership and outer containment remain unchanged.

## Preserved boundaries and focused review

Preview remains exact-size and identity-bound; its `object_bytes` is never
narrowed. Discovery offers/pages/summaries, authoring offers, contact directories
and module routes are unaffected. Request/response schemas and the ordinary
store/client files are unchanged. No retry, grant renewal, failed-client-attempt
refund, new error body, capacity advertisement or new mathematical acceptance
rule is introduced. An unavailable/oversized response is still only a failed
attempt, not evidence of global absence.

The change removes the false refusal when a complete object fits the provider's
positive conservative remainder but the client's maximum does not. It cannot
make an object fit an insufficient remainder, guarantee a two-request inspection
will finish, or resolve conservative concurrent refusal while writes are live.
Client reservations still use the original client caps and retain their existing
failure accounting.

Root's later controls should distinguish a successful small full object under a
large cap, a genuinely oversized object, zero/negative conservative remainder,
missing objects, active uncharged/charged reservations, interrupted writes and
unchanged nonselected routes. These are changed transport boundaries; they do
not require any new native theorem, grounding, proof or broad service campaign.
