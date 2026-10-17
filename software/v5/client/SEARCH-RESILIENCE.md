# Continue discovery after a settled provider failure

The explicit `client.workspace_resilient.Workspace` entry uses the existing
evidence-workspace configuration and storage schema. Its ordinary operation
constructor creates the new `CommonsClient`. Include both
`client/workspace_resilient.py` and `transport/search_resilience.py` in the
actual mathematical owners' pinned source closure before construction.
There is no migration, new grant, trusted provider or replacement search session.

After the existing `find(...)` returns authorized contacts, select an attempt:

```python
answer = await client.search_offer(contact, max_bytes=65536,
    max_expanded_bytes=1048576, max_age_ms=60000, attempt_timeout_ms=5000)
if answer["status"] == "REFUSED_PROVIDER_ATTEMPT":
    # The caller may choose another returned contact using this SAME client.
    # Original requests/providers/snapshots/bytes/time limits still apply.
    pass
```

`search_page` has the same extra `attempt_timeout_ms` keyword, for either
positive candidate search or verified interval coverage. Successful results
retain the predecessor formats and unchanged authentication. A failed attempt
does not mean the query has no answer, and never establishes global coverage.

## What may return a settled refusal

The outcome identifies one provider, ticket, operation and finite reason, with
`mathematical_acceptance=false` and `global_complete=false`. It carries no
candidate, theorem warrant, continuation cursor or verified scan coverage.

An expired contact is not dialed. Connection refusal uses the pinned asyncio
failed-connect cleanup behavior. A received EOF, supported non-200 response,
malformed bounded HTTP frame, reset/broken pipe, or per-attempt read timeout
can be recoverable only when the acquired stream subsequently closes cleanly.
The full original ticket reservation is charged exactly once; unknown bytes
or provider work do not earn a refund. The caller decides whether another
attempt is worthwhile. There is no automatic retry, referral dialing or renewal.

## What is still fatal

Invalid metadata or authentication inside `SearchSession.accept`, exhausted
budgets/deadlines, changed pins/policy/endpoint/owner, unexpected local errors,
TLS validation/configuration failure, cancellation and uncertain cleanup escape
to the original fail-stop client. In particular, connect/handshake timeout or
reset before a writer is obtained is not treated as clean recovery. A one-second
bounded close attempt cannot extend the original client/session authority:
post-call checks still enforce the original deadline.

The extra timeout is at most60,000ms and is clipped to the ticket/session time.
It is a transport attempt bound, not a new operation allowance or a hard
end-to-end wall-time guarantee; local cleanup and enclosing supervision remain.

## Scope

This is a narrow pre-accept fault-containment improvement, not complete Byzantine
search tolerance or a proof of useful growth. Mathematical admission, imports,
authoring, publication, acquisition and recovery after arbitrary authentication
failure are unchanged. A failed remote read preserves prior live authority only
after complete settlement and unchanged-owner checks. Actual release evidence
and current test status are recorded in the2026-10-17 research cycle; this API
document alone is not qualification of genuine mathematical or public operation.
