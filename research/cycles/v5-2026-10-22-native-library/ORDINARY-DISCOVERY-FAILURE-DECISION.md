# Known-provider-failure continuation: bounded decision

2026-10-23, `ordinary_api_flow`; source/theory only, canonical guard PASS.
No code edit, import, runtime, network, test, large scan or Git action.

## Decision and smallest change

Recommend a fresh **peer_api.find-only successor** that skips a provider after
an explicitly recognized failure and continues the already selected list.
Make this the default, not a new config switch: find already promises incomplete
positive metadata, and an unavailable optional contact should not suppress other
funded contacts. Keep the config schema, provider order and all budgets unchanged.
Retain the old frozen package; root must separately select successor/package pins.
Do not introduce retries, referrals, parallel fan-out, provider scoring or new TLS.

## Existing lower-level behavior is usable, conditionally

`transport/clients.py:31` catches exchange failure, calls session.abandon, then
reraises. Non-200 responses also abandon. `search_session.py:149,244,305` removes
the pending ticket, preserves request/page/provider/snapshot-attempt charges,
and charges full reserved bytes/rows on abandonment. Invalid received replies
charge their actual raw length plus conservative reserved rows; candidate scan
allowances are always fully charged. No refund, fresh session or replay is needed.
Earlier verified summaries/dedup state remain; rejected pages commit no matches.
Ordinary transport/parse rejection does not close the session. Exceptions:
deadline exhaustion makes it terminal; oversized raw bytes reaching accept mark
TRANSPORT_BYTE_VIOLATION (a trusted transport-contract failure, not recoverable).

`peer_api.py:171` prepays the whole search suballocation once into OrdinaryBudget.
Keep that exact charge, even on failure; SearchSession enforces its internal
remaining caps. Do not demand unused outer request/byte balance after prepayment:
a standalone search legitimately prepays its entire grant. The shared ledger's
deadline/closed state still governs, and subsequent receive gets no replenishment.

## Exact conservative recovery boundary

Catch only around `await client.offer(...)` or `await client.candidates(...)`,
not around setup, config compilation, local pin checks or result processing.
Initially recognize these exact exception classes (not broad base classes):
ConnectionRefusedError, ConnectionResetError, ConnectionAbortedError,
BrokenPipeError, TimeoutError, asyncio.IncompleteReadError,
asyncio.LimitOverrunError, ssl.SSLCertVerificationError,
json.JSONDecodeError and UnicodeDecodeError. The last two arise from returned
HTTP/JSON bytes here; request keys/features are already validated ASCII data.
Additionally recognize **type(error) is ValueError** with exactly these codes:

```text
REMOTE_HTTP_ERROR_CONSERVATIVELY_CHARGED
HTTP_HEADER_BYTES HTTP_HEADER_LINES HTTP_HEADER_SHAPE HTTP_HEADER_NAME
HTTP_HEADER_DUPLICATE_OR_CONTROL HTTP_UNSUPPORTED_HEADER HTTP_CONTENT_LENGTH
HTTP_MESSAGE_PROFILE HTTP_STATUS HTTP_RESPONSE_BOUND HTTP_TRAILING_RESPONSE
JSON_BYTE_LIMIT JSON_DEPTH_LIMIT JSON_DUPLICATE_KEY JSON_NONINTEGER NONCANONICAL_JSON
SESSION_OFFER_QUERY_BINDING SESSION_OFFER_ASSURANCE SESSION_OFFER_STATUS
SESSION_OFFER_NO_SUMMARY SESSION_OFFER_SUMMARY SESSION_OFFER_EXPIRED
CANDIDATE_PAGE_SCHEMA CANDIDATE_ASSURANCE CANDIDATE_CURSOR_BINDING
```

No prefix matching and no blanket ValueError/OSError/Exception catch. Generic
EXACT_FIELDS/HASH_ENCODING and other ambiguous validation errors remain fatal;
this first seam does **not** claim continuation after every malformed reply.
Unknown OSError/SSLError can mean local CA/config/resource faults; do not guess.
This conservative false-negative boundary is smaller than adding typed errors
through every shared validator. Broader coverage needs a separate concrete need.

Before skipping, recheck allowance, ledger.active(), CA pins and session._live(),
and require no pending session ticket. Any failure of these checks stops globally.
Never recover SESSION_BUDGET:*, session/query/ticket corruption, byte-contract
violation, cancellation/SystemExit/KeyboardInterrupt, or unexpected program errors.
The next ordinary reservation, not a synthetic new grant, decides if another
provider fits. Preserve existing global budget/deadline/failure reporting.
Timeout is recoverable only if those original clocks remain live: current request
timeouts may consume the entire remainder, so no slow-peer fairness is claimed.

## Public report and one decisive cheap control

On recovery retain all prior offers/matches exactly, abandon the remainder of
that provider (including other partitions), and append one bounded diagnostic
`{provider, phase, error}` using existing sanitized error rendering. At most 64
entries; no retry or discarded charge. Keep INCOMPLETE_SEARCH and all completeness,
coverage and mathematical-acceptance flags false; distinguish finished contacts
with failures from budget/deadline termination. Empty matches never prove absence.
Do not reinterpret existing HTTP completed/failed counters as provider outcomes.

Select one native-free fake-exchange control using real SearchClient/SearchSession:
P0 yields a verified page then malformed JSON; P1 raises ConnectionRefusedError;
P2 yields a verified result. Require both earlier/later matches, ordered failures,
zero pending reservations, exact failed-page/abandon charges, one unchanged ledger
prepayment and unchanged original deadlines. A table row with request cap exhausted
before P2 must make no P2 exchange and retain only prior matches; cancellation and
an unexpected ValueError row must stop rather than continue. No sockets/native
checker or new theorem fixture; use existing inert discovery reply material.
Stop after that changed-boundary control and outcome audit; no broad search,
mathematics, scalability or useful-growth campaign follows from this decision.
