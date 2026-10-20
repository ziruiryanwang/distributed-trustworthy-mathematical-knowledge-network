# Acquisition failure: source-level decision

## Selected direction: recover a clean body-supplier unavailability

**Principle:** a failed read that has not reached custody or mathematical
admission adds no authority and need not revoke already verified facts. Keep
the original live client, warrants, grant, deadline and budget; let the caller
explicitly select another already authorized supplier. This establishes neither
global absence nor a guarantee of eventual availability.

Source inspection supports a bounded body-only seam:

- `AcquisitionBudget.begin/settle` already consumes an attempt and settles its
  byte reservation. `_SharedAcquisition._get` settles in `finally`; its lower
  `AcquisitionClient._get` releases `inflight` and `reserved_bytes` in `finally`.
  Unknown/zero measured outcomes conservatively consume the selected byte cap.
  Preserve those charges, facade/helper calls and the original deadline.
- `AcquisitionClient.body` validates commitments before optional custody;
  `DeltaAcquisition.body` performs the actual store write only after the awaited
  structural body read returns. A narrow unavailability outcome can terminate
  before either write. Never catch a custody/readback failure as recoverable.
- Current `_async_action` treats every exception as fatal; mixed `_fail` clears
  warrants/caches and closes the budget/issuers. `SemanticReader._call` also
  becomes FAILED. The successor must return a typed pre-commit refusal through
  these boundaries, not broadly swallow exceptions or weaken their fail-stop
  handling. Check live state and census on the ordinary successful-return path.
- Before returning refusal, require clean local transport closure, no pending
  acquisition ticket, zero lower in-flight/reserved bytes and unchanged owner/
  grant identities. Consume exactly one failed attempt; no fresh acquisition
  owner, retry, replacement grant or refunded allowance.

Eligible transport outcomes are locally identified connection refusal, clean
response EOF, or a completely framed bounded unavailable status, after positively
known cleanup. EOF means **UNAVAILABLE**, never proof that an object does not
exist. Malformed successful replies, commitment mismatch, cancellation, policy/
pin/expiry/grant failures, uncertain cleanup and post-custody failures retain
fail-stop behavior. Use an exact locally produced outcome at the transport seam,
not classification of an arbitrary exception string at the public facade.

The current provider closes on missing-store errors rather than sending 404.
Both current HTTP exchange functions swallow `wait_closed` errors, so their
return/exception alone does not attest clean cleanup. The fresh seam must expose
that outcome explicitly. Restricting this increment to bodies avoids the
separate packet framing issue: `delta.exchange` demands exact packet length
before status handling, which rejects an ordinary short error response.

Root selects a fresh supplier-resilient facade/helper and
`transport/acquisition_resilience.py`, retaining the real structural owner and
unchanged validator/custody functions. No new mathematical owner/evidence class,
provider protocol, packet recovery or search re-audit is needed. This checkpoint
is source reasoning only; no runtime, test, import, build or Git mutation ran.
