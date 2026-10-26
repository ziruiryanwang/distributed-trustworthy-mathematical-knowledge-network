# Typed availability seam: source checkpoint

2026-10-26. Source implementation only under CONTRACT.md. No import, test,
network/native operation, live state access or Git action occurred. Independent
review and root's exact finite execution selection are still required.

## Exact delta

| Fresh payload | SHA-256 |
|---|---|
| http_provider.py | d9c342d1dcb5ee3e4b293e8dc0566397a321cc59a6f545e2f2afde452c760251 |
| ordinary_acquisition.py | 076130f7a34b505df33ee550501d1c4276bb46e408ff226df765225933a0658e |

Provider changes are confined to the bounded exception type and optional
`exchange(..., classify_unavailable=False)` classification. Endpoint/request
validation and local TLS-context/CA-file loading occur before the classified
network scope. Its own saved timeout manager must report expiry before a
TimeoutError becomes `TransportUnavailable("ATTEMPT_TIMEOUT")`. Bare timeouts
from elsewhere remain original exceptions. Explicit TLS errors are rethrown.

The remaining permitted reasons are CONNECTION_REFUSED, CONNECTION_RESET,
CONNECTION_ABORTED, BROKEN_PIPE and INCOMPLETE_READ, mapped from their narrow
Python exception classes. No OSError/BaseException/cancellation recovery was
added. Existing writer-close and at-most-one-second wait_closed behavior stays
unchanged; a typed exception exits only after that existing finally executes.
It asserts failed delivery, never global absence or quiescent remote state.

Acquisition adds keyword-only `attempt_timeout_ms=None, unavailable_errors=False`
to preview/locator/evidence and their common helper. Validate options before a
ticket is spent. Cap the existing remaining timeout without changing the ledger
deadline. The default calls exchange without new kwargs, retains old status
handling and keeps exact record/locator/evidence validation/retention unchanged.
Authoring-offer calls do not acquire an automatic fallback mode.

Only the exchange await catches TransportUnavailable. Framed HTTP404/503 become
HTTP_404/HTTP_503 before validation; HTTP400 and malformed protocol remain terminal.
Successful validation and local retention execute outside that narrow catch.
Thus a local TimeoutError, OSError or even accidentally raised transport sentinel
cannot be reclassified by the catch surrounding exchange.

The opt-in failure branch increments failed_attempts once, leaves `charged=None`,
and completes the unchanged failed-ticket settlement in finally. Only afterwards
does it recheck the original active budget and construct AcquisitionUnavailable
with bounded `reason`, `provider` and `route` fields. Settlement errors and an
expired/closed budget supersede the retryable result. Full failed response-cap
charges, requests, header/request bounds and observable completed-response counts
are retained. No ledger, refund, contact choice or retry loop is added here.

## Required changed-boundary controls

- Old signatures/default behavior; opt-in flag/timeout boolean and range refusal.
- Own network timeout and real premature EOF classify; bare timeout and TLS/CA
  setup failures do not. Refused/reset/aborted/broken-pipe remain narrow classes.
- HTTP404/503 opt-in only, with full failed-cap accounting; HTTP400 terminal.
- Invalid identity/parser/local-retain errors do not become availability.
- Settlement failure overrides pending availability; cancellation stays terminal.
- Original ledger exhaustion prevents another begun attempt; no byte refund.

These are transport/accounting claims, not mathematical acceptance. Root owns
receive's explicit source ordering and time allocation; no code here broadcasts,
selects another source, changes the parent or invokes a checker.
