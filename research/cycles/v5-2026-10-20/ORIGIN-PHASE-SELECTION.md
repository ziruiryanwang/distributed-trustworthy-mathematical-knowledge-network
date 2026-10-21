# Remove repeated trust-module path resolution, not authority checks

2026-10-21, root. Source implementation/control-authoring selection only.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Current114 source map is distribution-validation-01-input.json, SHA d11abac9.
Mirror02 audited failure451fc8e5 is preserved; no cap increase/retry selected.

## Decision and scope

ReceiptVerifier._active resolves the same trust-module filesystem path on every
call. Aggregate inherits that call; mixed/import owners multiply it further,
including the callbacks before/after every pin in existing PP.phase. This is a
source-established amplification, not measured attribution of the120CPU failure.
Trust-record and file-pin deduplication already exist; do not implement them again.

Select two fresh successors below `software/v5/origin_phase/admission/`:
`pin_phase.py` from validation_phase, and `verifier.py` from trust_withdrawal.
Only phase-local origin-resolution reuse and the verifier trust-origin _active
call site change. Constructors and other origin checks can remain unchanged.
Do not broaden the existing synchronous validation scope, alter limits, remove
active callbacks, or cache acceptance, handles, clocks, bindings or denial.

## Required semantics

The helper checks the exact current module-file string against the expected
absolute origin; caller retains original module-object, registration and binding
checks. It must not call the phase active callback itself, because that callback
calls the helper. First use performs actual Path.resolve; a cached successful
observation only replaces the filesystem resolution, not expected-origin equality.
Unscoped calls always perform the original resolution. Prefer the smallest API
with positive-only caching, exact arguments and no ambient configurable resolver.

Origin state surrounds the existing trust and pin scopes, including entry guards
and all their finalization callbacks. Every successful exit freshly resolves all
observed paths after trust/pin finalization, with original active guards bounding
the additional work. New origins during finalization refuse. Nested scopes are
independent; exceptions discard state; copied exited contexts cannot revive it.
Finalization failure cannot return success. No await, worker, network or user
callback is introduced within this trusted synchronous phase.

This uses the existing owner-controlled stable filesystem/process assumption.
It changes filesystem observation granularity deliberately; it is not protection
against hostile concurrent path rollback. No reduction in mathematical checking.

## Owners and evidence

core_growth implements the two fresh sources and ORIGIN-PHASE-SOURCE.md.
core_release independently challenges the boundary and reviews final source in
MIRROR02-ORIGIN-BOUNDARY.md. adaptive_audit owns fresh
`software/v5/origin_phase/controls.py` and ORIGIN-PHASE-CONTROL-PLAN.md.
Root owns exact selectors, integration, NOW/WORK and Git. All old used files stay
immutable. Source changes may await review fixes before any execution.

Controls should count real path resolutions, exercise the actual verifier active
method with inert/non-authoritative issuer shells and real local trust records,
and prove original guard counts are retained. Cover changed __file__, expected
origin, module registration, trust binding/withdrawal, independent phases,
body/finalization failures, final origin change and budget crossing, closed copied
context, and ordinary freshness. No native/crypto/network operation or repeat of
the previous successful full suite. Select one small finite run only after review.

Terminal-I contract38a5f73c/reviewc82d15c6 are retained for later integration; that
lane must not displace the current unusable contribution path.
