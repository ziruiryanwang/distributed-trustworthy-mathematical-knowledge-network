# Settled peer-packet preflight

Source-only successor selected by
`research/cycles/v5-2026-10-20/CANDIDATE-PREFLIGHT-SELECTION.md`.
No execution, installation, proof, migration or release qualification follows
from this directory. Preserve candidate_admission and exact_packet predecessors.

## Purpose and public behavior

Only the existing asynchronous `try_acquire_terminal` and
`try_acquire_terminal_exact` APIs gain this outcome:

```text
CANDIDATE_REJECTED_UNDER_SELECTED_POLICY
```

It means one bounded, successfully closed transfer supplied bytes that failed
the requested packet identity or selected structural/profile/target rules.
It does not mean false mathematics, cryptographic invalidity, peer misconduct,
global absence or a verified alternative schema. It carries no warrant.

The result contains `reason`, `module`, copied requested `selection`
(`packet_sha256`, `packet_bytes`), `received_sha256`, `received_bytes`,
`mathematical_acceptance: false`, and authority label
`LOCAL_CANDIDATE_PREFLIGHT_NOT_MATHEMATICAL_ACCEPTANCE`.
Reasons are `PACKET_IDENTITY_MISMATCH`,
`PACKET_STRUCTURE_OR_SELECTED_POLICY`, and `SELECTED_TARGET_MISMATCH`.
The requested identity is not mislabeled as the received identity.

The other terminal outcomes retain their meanings:

- `ADMITTED`: the ordinary live local warrant is included.
- `NOT_ADMITTED`: the actual original verifier passed its complete clean
  nonacceptance gate; this is not structural preflight rejection.
- `UNSUPPORTED_TRIAL_FORM`: a structurally valid mixed packet is outside this
  terminal-trial API; no mixed verifier is invoked.

Strict `acquire`/`acquire_exact`, all local admission and the positive packet
cache remain strict. An old stored packet failing local validation is not
reclassified as new malformed peer input. Public argument/token/offer errors
and an explicit expected-journal mismatch remain fatal.

## Sequence and costs

The new transport method captures the original acquisition, structural owner,
budget, selected contact, deadlines and packet profile/limits. It copies the
requested digest/size before any await. The offered API still requires exact
offer membership; the exact API still accepts an independently known identity.

One packet request uses one original acquisition ticket. The packet-specific
exchange preserves HTTP/TLS/framing/EOF rules and returns only after successful
`close`/bounded `wait_closed` within the original operation deadline. Unknown
network/closure outcomes conservatively settle the full reply reservation.
No retry, refund, replacement owner, new contact, budget or deadline is created.

The facade charges received raw bytes **before** pure hashing/parsing. A valid
path does not incur a duplicate raw-input charge merely because preflight moved
earlier. Existing receipt/member/input charges remain. Preflight rejection
creates no verifier reservation, custody write, stage, import, cache or warrant.

Successful preflight is not custody or admission. The valid branch still uses
ordinary packet `put`, exact readback, custody readiness and the existing
mathematical admission gate. Those operations are outside the recoverable
parser catch. Any disagreement or storage error is fatal, even if its exception
class happens to match a parser error.

Original owner/contact/configuration checks run after transfer and after
preflight or later admission. The existing trial finalization performs active,
census, active, then nonblocking original deadline/controller-CPU checks.
The two asynchronous terminal methods additionally require zero pending
network ticket, structural inflight requests and structural byte reservations
before returning. Existing work survives by nonmutation, not rollback.
The supplier contact must be live through the completed attempt/triage/admission
checks, not throughout the subsequent purely local final census. Contact expiry
then does not revoke acquired immutable bytes; original client/issuer deadlines,
CPU limits and quiescence are still enforced at return.

## Narrow error classification

`preflight_packet(raw, entry, summary, *, envelope, aggregate_image,
terminal_receipt_bytes, terminal_i)` is a pure internal helper. Trusted arguments
and adopted configuration are validated outside its catch. It invokes the
selected real `inspect_evidence` parser, not a second grammar.

Only exact reviewed `StructureError` and `DeltaError` failures from that call
are candidates for structural rejection. The latter includes intentionally
declared finite mixed grammar bounds. The helper follows at most sixteen typed
exception-chain nodes; supported decode causes are exact `JSONDecodeError`,
`UnicodeDecodeError`, `UnicodeEncodeError`, or `ValueError`. Resource exceptions,
unexpected types/subclasses, cycles, divergent cause/context chains and longer
chains stay fatal. This matters because the existing codec wraps interpreter
`RecursionError` in `StructureError`; that must not be hidden by a broad catch.

No catch surrounds store operations, source/profile/owner checks, byte charging,
grant exhaustion, controller limits, cancellation or final liveness. Actual
`MemoryError` and direct/chained `RecursionError` do not return rejection.
Malformed HTTP, timeouts, unavailable peers and ambiguous socket closure remain
fatal rather than becoming a general availability-recovery feature.

## Internal contracts and preserved scope

- `_exchange_packet_settled(endpoint, entry, *, timeout_ms, deadline)` returns
  the original HTTP response fields only after its strict closure gate.
- `EvidenceAcquisition._trial_packet_bytes(provider, module, entry, *, offered)`
  returns `(raw, bound)` without parser/store/admission mutation. `bound` is
  internal in-memory evidence of original identity, not a portable capability.
- `_packet_trial_unchanged(bound)` checks the existing contact/budget binding,
  packet configuration and network quiescence.
- `preflight_packet` returns internal `CANDIDATE_PREFLIGHT_PASSED` plus structural
  facts, or the public policy-relative rejection above. Passed preflight does
  not bypass any later ordinary gate.

The body-transfer binding checks are reused through local imports to avoid a
construction-time import cycle. The facade adopts only already-selected source
pins. No logical SDK module is added: three existing logical sources change,
so the current 130-source selection and 128 I/A runtime-pin cap need not grow.
`managed_owner.py` changes only its embedded facade source pin.

The old delta/provider/search transports still have their inherited cleanup
limitations. This successor establishes strict client closure only for its new
packet-trial transfer. It is not a hostile-code sandbox or a claim of universal
network recovery. Independent source review, focused controls and any selected
actual integration remain separate root-owned gates.
