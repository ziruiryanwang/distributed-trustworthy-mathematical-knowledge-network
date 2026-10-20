# Persistent runtime withdrawal: implementation selection

Root adopts DESIGN `3132ddc7` and SOURCE `b37a7675`: close the concrete local
trust-update gap without another proof campaign. The whole v5 goal stays open.
The immutable installed interface candidate and all previously used bytes stay.

## Selected source work

Fresh overlays under `software/v5/trust_withdrawal/` only:

- core_growth: `admission/trust.py`, `admission/verifier.py` (successor of the
  actual runtime_efficient owner), and `aggregate_claims/aggregate_admission.py`.
- core_search: `client/runtime.py`, ordinary adoption/example integration and
  concise API instructions. Its only shipped SDK factory caller requires a
  small `client/remote_reader.py` successor forwarding explicit existing-domain
  configuration. Historical unused examples are not copied. Agree helper calls
  directly with core_growth.
- core_release: independent source review and `controls.py`, covering only
  the changed persisted/live withdrawal boundaries; no runtime yet.
- root: exact source selection/launch adapter and subsequent result adoption.

Mandatory `trust_binding` on both issuers; RuntimeProfile retains the original
domain/binding and checks at construction and each operation. No None/default
allow. Stable support identity covers actual selected source/runtime roles and
mathematical policy. Ordinary startup opens existing state. Explicit owner-only
provisioning is a separate action and must not be a hidden factory side effect.
Expose a source-validated support-description route if required for provisioning;
describing configuration alone must not mint acceptance authority.

Use one immutable adoption plus create-only WITHDRAWN tombstone, bounded reads,
fail closed on missing/corrupt/redirected state, sticky refusal, no reinstatement.
The trusted owner/OS and owner-serialized final-check ordering are assumptions;
do not claim antirollback or instantaneous recall of already returned data.
Preserve pin/origin gates, finite accounting and cleanup. Existing downstream
liveness propagation is reused, not copied into unrelated overlays.

## Evidence and scope limit

First resolve source review; then one finite native-free targeted suite. At most
one genuine receipt integration may follow if needed for the changed boundary.
No new proofs, compiler builds, network campaign, RAM work or old-run restart.
Do not include full distribution copying/readback in this source decision.
Checkpoints: TRUST-WITHDRAWAL-IMPLEMENTATION, -REVIEW and -OUTCOME in this cycle.

Root may prepare `software/v5/trust_withdrawal/actual.py` and a small selector
for one genuine BASE receipt integration through the public client launcher.
It will explicitly provision then reopen a fresh domain; accept one genuine
receipt, apply withdrawal, refuse cached/live/new-operation use and close.
This is preparation only; actual execution awaits source/controls review.
