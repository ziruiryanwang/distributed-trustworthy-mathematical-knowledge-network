# Contact-only issuance cutoff

2026-10-28, query_scaling. Selected by SELECTION.md; source work only. No module
imports, tests, runtime, owner/database/network access or Git were performed.

The fresh `http_provider.py` is copied from
`ordinary_reply_capacity/http_provider.py`, SHA256
`929fbf453bb23d353f89384db3dbb8cd4e11e6fd5383a09a36d93fc92631b93b`.
It keeps the same imports and existing loader/package dependencies. The selected
source map is `ordinary_name_directory/source-map.json`; the deferred pattern
integration is not a dependency.

## API and checks

`Provider(..., contact_directory=None, contact_deadline=None, ...)` adds one
optional keyword. A non-None deadline requires the exact ContactMap role and a
finite exact Python int or float, excluding bool, NaN and infinity. It is an
absolute value on this process's monotonic clock, not UTC, a relative TTL or
provider-supplied time. An already elapsed finite value is allowed at construction
but refuses contact use with `CONTACT_DIRECTORY_EXPIRED`.

The peer composition computes the deadline from fresh local request-start
horizons. Its internal `directory_serve` clips the requested lease to that value
and passes the clipped service deadline to Provider. Public static configuration
cannot provide or renew this argument. Callers without the keyword retain the
existing behavior, including the old static-directory lease behavior.

With a non-None cutoff, direct contact `dispatch` composes the caller's optional
budget callback with `_check_contact_deadline`. It checks before invoking
ContactMap reply construction, supplies the composed callback for that bounded
construction and checks again before returning its bytes. A direct caller
therefore cannot bypass freshness merely by omitting a callback. Noncontact
dispatch branches never consult the cutoff.

In the HTTP handler, the existing operation-deadline callback additionally
checks the cutoff for the contact route. The final response decision uses that
callback. The handler supplies it to both header and body `_write` calls only
when serving contacts with a non-None cutoff. `_write(writer, raw,
check_budget=None)` checks an optional callback immediately before each chunk's
`writer.write` and after every awaited `drain`, including the final drain.
Thus a header drain crossing the cutoff cannot lead to a newly enqueued body;
a body drain crossing it cannot lead to another chunk. The helper remains a
no-callback write loop for all existing transport calls and other routes.

The full declared response/header charges occur before the first write, as
before. A later cutoff failure does not refund them. Existing finally blocks
release the outstanding reservation; the handler records failure and existing
connection ownership/close logic performs cleanup. No listener lifecycle,
retry, admission limit, parser, route schema or learned-endpoint authority
changes here. The outer finite service timer still owns shutdown.

## Exact guarantee and limits

Every new contact-response enqueue with the cutoff enabled has a successful
combined operation/cutoff check immediately before it. This is a check-guarded
application boundary under the existing trusted monotonic-clock and execution
assumptions, not a hard real-time guarantee about preemption between check and
write. Bytes already queued can arrive after expiry; a post-drain failure can
occur after a complete response has already been queued. It does not revoke
that response or refund its charge. Readers keep their existing bounded
request-start hint horizon. There is no global revocation, endpoint-liveness
claim or proof of current provider configuration.

## Narrow independent controls requested

The changed seams need direct-dispatch expiry and composed-callback controls,
expiry during construction, and an inert writer/clock crossing the cutoff during
header/body drains. Verify no later enqueue, conservative charge/reservation
settlement, and the None/noncontact compatibility paths. Reuse existing
transport/parser evidence; no repeated broad suite or real network is needed to
establish these callback boundaries. Root owns any later runtime selection.

Source SHA256:
`3ce581f4057b6694c6d99a697847984fe7431a695989018f3e179217712859a2`.
