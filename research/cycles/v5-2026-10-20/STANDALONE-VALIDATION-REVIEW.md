# Independent review: scoped standalone mixed validation

2026-10-21, adaptive_audit. **GO for source-only focused controls; no runtime,
installation, speedup, mathematical acceptance or release adoption claimed.**

The review follows STANDALONE-VALIDATION-SELECTION and decision
`091f0385761e75f6d567bbc6ef729fd09c3cf0b0e5e02237f0d0fdf531853a73`.
The relevant source baseline is the terminal-I 114-source map
`d3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0`.
No old suite was imported or run. Read-only whole-file diffs delimit the two
controller changes; the phase implementation and actual selected trust and
receipt-verifier guard implementations were inspected directly.

## Exact reviewed successor bytes

Paths below are relative to `software/v5/standalone_validation/`.

| Source | Bytes | SHA-256 |
|---|---:|---|
| admission/pin_phase.py | 8677 | ac7ed2285f2c15630a482817828cf4784ca807c6ec700b4a17bfe3e561eee881 |
| mixed_claims/receiver.py | 24731 | 835d59809045c3e49f9d7e5483108f4034c591a3a82224e4155f4f7d0f6dcced |
| mixed_claims/imports_atomic.py | 44771 | 8a8313376d736f25a45b6089f491373bc7e0206aa77b539dbff077fc4eb92595 |

The predecessors respectively have SHA-256 `c00e1259488415b390b651eab307a91ee5db1966a57f4c236ac054c2445bac21`,
`aa591a1829deff82576ba30af484ab560ee04900200fd79ac93c19a9c2c7bf7f` and
`e38ac52a888f354e8e878984397a5c93c82ac38284b9e6fc89051063537aa459`.
All remain unchanged. No selected mathematical relation, receipt interpretation,
native invocation, source packet, resource ceiling or trust manifest changed.

## Standalone call graph and preservation argument

`MixedDeltaVerifier._check(deadline)` now enters
`borrow_or_phase(lambda: self._active(deadline), owner=self)` and calls
`_check_phase(deadline)`. The latter is exactly the predecessor `_check` body,
including its original check order and revoke-on-exception block. In particular
loaded-origin, imported-symbol, original-owner, native-source-pin and saved-owner
selection checks remain. Additional wrapper exceptions also revoke the mixed
owner, covering failures in final pin, trust and origin checks after the old body
has returned.

Outside an explicitly matching enclosing phase, `borrow_or_phase` enters an
independent `phase`. Thus this path now has the established first/final
pin/trust/origin validation transaction rather than repeated persisted trust
reads at every pin guard. Every new standalone active callback closes over the
exact supplied deadline; it does not substitute the broader owner lifetime.
Near-deadline refusal timing is deliberately allowed to become stricter because
new finalization work is now charged and guarded. This is preservation of static
checks and finite authority, not bit-for-bit scheduling equivalence.

## Enclosed import call graph

`MixedImportSession._live` snapshots only `self._origins[2]`, registering that
exact identity in an immutable tuple. Its original `_live_phase` body is
unchanged. That body checks current-vs-original owner identity before invoking
the mixed owner. The mixed owner's new wrapper finds its explicit registration
and uses a temporary view over the outer pin records. The view composes both
the enclosing guard and the mixed call's own guard. It neither drops the
original `_check_phase` guards nor creates a second trust/origin transaction.

The outer import owns the sole final pin/trust/origin sweep. A
`phase_body_complete` flag is set only after the unchanged body succeeds. If
subsequent finalization fails, `_live` revokes its captured original mixed owner
and closes the import. It does not close independent I/A owners or a substituted
current mixed owner. If the import body itself fails, existing cleanup remains:
the import closes, and a mixed `_check` failure revokes that mixed owner itself.
This avoids broadening unrelated body-only failure revocation.

No usable public result is emitted from this phase before its enclosing context
manager exits. `_live_phase` is synchronous validation, not native execution,
network access or result promotion. Calls from public import operations receive
the return only after finalization succeeds. This conclusion relies on the
existing trusted serialized controller model, not on sandboxing Python callers.

## Lifetime and conflict invariants

1. A root `_PinPhase` and each `_PinView` have separate open flags. A pin visit
   requires both. Root state remains open through trust and origin finalization,
   then closes and clears records in `finally`, even if entry/body/exit fails.
2. Each borrowing view closes in its own `finally`. A copied context containing
   that view therefore refuses after the borrow ends, even while its outer root
   remains live. A copied root context refuses after root completion.
3. The default `phase(active)` still creates independent nested scopes. A
   nonmatching or absent owner registration also creates an independent phase;
   an already closed inherited view refuses instead of silently reviving it.
4. Registration matches with `is`, not equality. The tuple is snapshotted by
   reference as an immutable tuple of original object identities. No registration
   is inferred from an arbitrary caller's current context.
5. Shared records preserve exact original checker identity and `(bytes, sha256)`
   comparison. Checker/expected-value conflicts still refuse. Failed comparisons
   are not recorded. This remains a validation observation cache, never a proof
   result or operation-lifetime authority cache.
6. Independent nested scopes restore outer ContextVars on every exit. Trust and
   origin scopes retain their existing fresh final checks and denial semantics.

The stronger copied-context closure rules are material: the predecessor pin
context held only `(active, records)` and relied on callbacks for expiry. The
successor explicitly refuses even if such a callback were otherwise permissive.

## Conditional safety and useful cost consequence

Assume owner-controlled stable local code/filesystem during a non-yielding phase,
original binding/denial/profile checks, and no authority escape before its final
sweep. Under those existing premises, replacing repeated successful observations
by first/final samples does not grant a new mathematical warrant. Distinct source
bytes still require pin checking, and final source/trust failures still preclude
success. This is not hostile concurrent mutation/rollback protection.

For `q` standalone checks and `p` pin visits per check, repeated guard-level trust
observation work can move from a multiplicative `q*p` term to per-phase work;
distinct byte hashing remains. The source does **not** establish what fraction
of the observed controller CPU comes from this term or an end-to-end speedup.
Already-enclosed imports must retain one final sweep, which is why explicit
borrowing is required rather than an unconditional new nested phase.

## Required focused controls before any integration

Exercise actual mixed `_check` and import `_live` using exact-class inert owner
shells, real trust records, real pin reads and unchanged guard implementations.
Check the supplied deadline, original binding/profile/CPU checks, registered vs
wrong-owner/default-independent scopes, pin/checker conflicts, successful final
read counts, failed final pin/trust/origin cleanup, copied-context expiry, and
outer-state restoration. No actual receipt handle, verifier process or native
proof acceptance may be manufactured or inferred from those controls.

There is no source blocker in the exact reviewed three-file change. Later
execution, outcome review and integration remain root decisions under fresh
exact selections. Used predecessor evidence and its failures remain immutable.
