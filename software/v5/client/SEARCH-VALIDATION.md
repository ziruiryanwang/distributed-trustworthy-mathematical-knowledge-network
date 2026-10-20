# Continue discovery after an invalid index reply

Use `Workspace` from `client.workspace_validated` for the staged evidence
client with pre-commit metadata validation. The persisted workspace schema,
mathematical verifiers, grant limits, custody and staging API are unchanged.
Select the new files in the launch plan and in the actual owners' source pins:

```text
client/workspace_validated.py
transport/search_validation.py
```

All predecessor pins are still required. There is no implicit migration of an
old installed source profile or fallback to a different verifier.

`search_offer` and `search_page` keep their existing signatures. The caller
chooses the next already authorized provider. The client does not retry, renew
the grant, extend its deadline, crawl peers, or change the formal query.

An invalid reply detected during bounded pure metadata validation returns:

```json
{
  "schema": "DMKN_SEARCH_VALIDATION_REFUSAL_V1",
  "status": "REFUSED_PROVIDER_ATTEMPT",
  "provider": "selected-provider",
  "ticket": 1,
  "operation": "offer",
  "reason": "INVALID_METADATA",
  "validation_error": "bounded diagnostic",
  "settlement": "ABANDONED_CONSERVATIVELY_CHARGED",
  "mathematical_acceptance": false,
  "global_complete": false
}
```

The full original ticket reservation is charged once. No summary, candidate,
interval coverage or mathematical warrant is created by the rejected reply.
Existing live warrants and the proof context survive this classified outcome.
It is not evidence that the requested mathematics does not exist.

The gate handles expected canonical-JSON and metadata-validation errors from
the existing pure parsers and authenticators. Unexpected failures, local owner
or accounting faults, deadline exhaustion, cancellation, uncertain socket
closure, and any actual acceptance/commit error still fail the operation.
This is not a blanket catch for every malicious input or local failure.

On a successful preflight, the unchanged session `accept` validates the same
bytes again and performs the ordinary commit. Thus successful metadata
validation currently does extra work; no native proof or ancestral proof is
replayed. Preflight examines the bounded reply and its touched snapshot/page,
not a copy of the full session or global corpus. This tradeoff keeps the old
stateful acceptance boundary intact.

The result is conditional fault isolation: if a later authorized provider is
honest/reachable and enough of the original allowance and deadline remains,
the caller can continue after a classified bad reply. It is not universal
discovery completeness, mathematical admission, or a full v5 release claim.
