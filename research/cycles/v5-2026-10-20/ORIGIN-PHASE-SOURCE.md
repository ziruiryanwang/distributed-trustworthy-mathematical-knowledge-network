# Phase-local trust-module origin validation: source checkpoint

2026-10-21, core_growth. Implements [the root selection](ORIGIN-PHASE-SELECTION.md).
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
This is source implementation only: no product import, parsing/compilation,
test, native operation, installation, mirror retry or adoption was performed.
Root owns selectors, launches, integration and Git; core_release independently
reviews the boundary and adaptive_audit authors its focused controls.

## Exact source selection

The current 114-source map is
`experiments/v5-local-checks/distribution-validation-01-input.json`, SHA-256
`d11abac9a9c5a5ac7d7b22efbf26bb04fcad1e886f19a2195d42060dd44ab565`.
Only these two fresh successor files are changed; both predecessors remain
unchanged and their hashes were rechecked after writing the successors.

| Role | Canonical-root-relative path | SHA-256 |
|---|---|---|
| Pin predecessor | `software/v5/validation_phase/admission/pin_phase.py` | `76b54eb04fa2a66ec598b8c6d668e675d8bd483809f8fa66448fa7319b82a9ce` |
| Pin successor | `software/v5/origin_phase/admission/pin_phase.py` | `c00e1259488415b390b651eab307a91ee5db1966a57f4c236ac054c2445bac21` |
| Verifier predecessor | `software/v5/trust_withdrawal/admission/verifier.py` | `01fb93b5d0063110fe82978dcc8a593557b34eaa8b6497f596715ca65064e38c` |
| Verifier successor | `software/v5/origin_phase/admission/verifier.py` | `32289cac1c8db4f8a778f5347c4ba843f5e5510d2891b1b8184cc5e6edfc1d80` |

The selected trust implementation remains
`software/v5/validation_phase/admission/trust.py`, SHA-256
`c997d2a83ae5246dec9ff30eeca72e405ec0f66c0a307e53e0521eef66fae6d0`.
It is neither copied nor modified by this change.

The entire verifier diff is the following expression replacement inside
`ReceiptVerifier._active`:

```diff
-                and Path(T.__file__).resolve() == self._trust_origin,
+                and PP.check_origin(T.__file__, self._trust_origin),
```

The pin successor adds private `_OriginPhase` state, `_ORIGIN_PHASE`,
`check_origin` and `_origin_phase`; it wraps the existing trust/pin phase with
the origin scope. The existing `check_pin`, expected-pin validation, trust
scope, pin-sweep ordering and original active callbacks are unchanged.
Constructors and all other origin checks remain unchanged. There is no new
resolver injection parameter, checker, certificate scheme or public endpoint.

## Actual amplification in the selected sources

The relevant caller chain is present in the current map, not inferred from old
logical-path implementations:

1. `interface_views/imports_atomic.py:110` defines
   `MixedImportSession._active`. With all three normal owners, it calls the I
   owner, A owner and mixed owner once each (lines 120–127).
2. `runtime_efficient/mixed_claims/receiver.py:117` defines the mixed owner's
   `_active`, which calls its I and A owners again (lines 132–143).
3. `trust_withdrawal/aggregate_claims/aggregate_admission.py:103` defines the A
   owner's `_active`; its first operation calls `ReceiptVerifier._active`.
4. `trust_withdrawal/admission/verifier.py:134` resolves `admission.trust`'s
   filesystem origin on every successful `_active` invocation.

Consequently one ordinary all-owner import callback produces four such
resolutions: direct I, direct A, mixed-I and mixed-A. The same callback is
invoked before/after repeated pin checks and sweeps. Other owner loops can add
further calls. This is a source-established call-count amplification, not a
timing attribution for either failed mirror or a prediction of meeting its cap.

For the already used simple 17-pin-check shape with one distinct pin and one
trust domain, the preceding phase retains 40 active callbacks:
`1 + 2*17 + 1 + 2 + 1 + 1` (entry, checks, body exit, pin sweep, pin-tail,
trust-tail). The new origin sweep adds two callbacks for one distinct origin,
yielding 42, without removing the original 40. Actual controls must verify the
intended call sequence and real filesystem observations; this count is not an
executed result.

## Helper semantics and assurance boundary

`check_origin(module_file, expected)` accepts an exact string and an absolute
`Path`. For ordinary unscoped calls it performs the previous fresh comparison,
`Path(module_file).resolve() == expected`. Invalid helper arguments raise
`ORIGIN_PHASE_INTERNAL_ARGUMENT`.

Inside one scope, successful observations are keyed by the exact raw file
string and expected `Path` pair. A cached pair is reusable only if the raw path
is absolute. A changed expected origin is not a hit; its actual comparison must
pass separately. Failed comparisons do not create observations. The actual
caller's module-object identity, `sys.modules` registration, string-type,
binding-object identity, domain binding, withdrawal/denial and deadline guards
still run on every call. There is no cached acceptance or authority handle.

The helper never invokes `active`: `active` invokes the helper, so doing so
would recurse. Instead the scope's own final sweep invokes `active` before and
after every fresh origin observation. The helper has no ambient/custom resolver
and uses actual `Path.resolve` both on first observation and during the sweep.

Relative paths deliberately remain uncached because their meaning depends on
the current working directory. Each relative use resolves afresh. Successful
relative observations are also retained for the final fresh sweep. This keeps
the earlier relative-input behavior and avoids silently introducing an
absolute-only verifier compatibility requirement. Relative origins receive no
claimed resolution-count improvement.

Successful scope completion has this order:

1. Enter the independent origin context, then the existing trust/pin contexts.
2. Run the original entry guard and trusted synchronous body unchanged.
3. Finish original pin-sweep, final pin guard and trust finalization unchanged.
4. Restore the preceding trust context; mark the origin state finalizing.
5. For each observed origin: run `active`, freshly resolve and compare the
   origin, then run `active` again. Any failure propagates; phase success cannot
   be returned after a failed final comparison or budget/authority guard.
6. Close and clear origin state in `finally`, restoring the enclosing context.

New origin pairs are refused once finalization begins, with
`ORIGIN_PHASE_NEW_ORIGIN_DURING_FINALIZATION`. Final mismatches raise
`ORIGIN_PHASE_FINAL_ORIGIN_CHANGED`. Closed copied contexts raise
`ORIGIN_PHASE_CLOSED`; they cannot revive discarded observations. Exceptions
skip successful-exit work and still close/clear state. Nested phases own
independent state and restore their enclosing contexts, not the inner cache.

This is deliberately a first/final filesystem-observation policy within the
existing trusted, owner-controlled, stable, synchronous validation scope.
It does not permit await, subprocess/network dispatch, untrusted callback or
authority escape inside that scope. It is not protection against a hostile
concurrent process that changes a path and rolls it back between observations.
The earlier owner/filesystem trust assumption is necessary; this optimization
does not create it or claim stronger hostile-filesystem security.

## Operation-count consequence and retained cost

For a successful ordinary phase with `q` origin-helper calls covering `k`
distinct absolute successful pairs, origin resolution is reduced from `q`
per-call filesystem resolutions to `2k`: one first and one final resolution
per pair. There are two additional active callbacks per pair. Calls outside
the phase, constructors, unrelated origin checks, relative paths, independent
nested scopes and failed comparisons remain separate costs. Memory is linear
in distinct observed pairs, not repeated calls or the global corpus.

The final origin callbacks intentionally lie outside the inner trust scope.
At an ordinary top-level exit they therefore perform fresh unscoped trust
reads. Nested exit instead restores the enclosing trust scope, with its
ordinary safeguards. Thus **do not claim two total trust reads for this new
composite phase**. For the simple one-owner/one-domain/one-origin shape, its
source count is four trust reads: first, trust-final, and the two origin-tail
guards. Mixed-owner callbacks have their actual multiplicity. Preserving this
small guarded tail avoids widening the trusted scope or changing `trust.py`.

The reduction is real at the operation-count level under the stated stable
scope assumptions. No wall-time fraction, whole-workflow speedup, cap-success,
new mathematical contribution, useful-growth advantage or release completion
is claimed before the separate reviewed controls and root integration.

## Review and next authority

Core_release reviews exact sources and boundary in
`MIRROR02-ORIGIN-BOUNDARY.md`; adaptive_audit owns
`software/v5/origin_phase/controls.py` and `ORIGIN-PHASE-CONTROL-PLAN.md`.
Root has the stable hashes above. The next useful evidence is one small,
finite, reviewed real-path/control run, not another broad campaign. The two
failed mirror operations and all previous passed controls remain frozen.
