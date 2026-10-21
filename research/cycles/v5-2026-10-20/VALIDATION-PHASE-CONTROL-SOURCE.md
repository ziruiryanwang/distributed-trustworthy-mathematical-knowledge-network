# Validation-phase focused controls: source checkpoint

2026-10-20, adaptive_audit. **Source complete; not executed.** Root owns eventual
selection/launch, core_growth owns the two product successors, and core_release
owns independent combined source/selector review. No product, old test, used
record, Git state, installation or runtime operation was modified by this work.

Exact control source:
`software/v5/validation_phase/controls.py`, 25992 bytes, SHA-256
`775a68abca3c5ac3c094a1ee921c1b2bc367a5a55a753e34783b0c3a76da4b0a`.

Final prospective plan:
`VALIDATION-PHASE-CONTROL-PLAN.md`, SHA-256
`6a8bfd4bc468de65835aa9e0b23bf9283f776a1a6677c08a839438149f7943bd`.
This corrects the earlier ownership wording and makes the selected trust-scope
entry ordering explicit: the unchanged active callback is inside the trust scope,
so both the simple and active-checks-trust compositions require two full reads
per touched domain per successful phase, including entry and finalization.

## Bound sources and execution boundary

The control stages the current 114 logical SDK entries from exact map
`995525c5cbf2746718cbf583a3e3e401bc56c2f88d1cef8664ffeb1b644454be`, replacing only:

- `v5/admission/pin_phase.py` with
  `76b54eb04fa2a66ec598b8c6d668e675d8bd483809f8fa66448fa7319b82a9ce`;
- `v5/admission/trust.py` with
  `c997d2a83ae5246dec9ff30eeca72e405ec0f66c0a307e53e0521eef66fae6d0`.

The other 112 modules keep exact selected sizes/hashes. Each logical copy is
verified before any product import, and selected trust/phase/codec origins are
checked after import. No historical test fixture is imported. Product imports
and tests run under a class-preserving socket-construction guard, subprocess
guard and `os.system` guard; forbidden attempts fail the result. No asyncio,
native owner, mathematical executable, proof verifier or network service is
required. These guards and fixtures are not a hostile-code security sandbox.

Every counted trust read wraps and delegates to the real `_read`. Fresh inert
policy records are created with actual `TrustDomain.create`, filesystem reads,
bindings, markers and withdrawal. Generation/path/adoption mutations affect
only the explicitly fresh per-test fixtures, and old bytes are retained where
record identity is deliberately replaced. No real previously adopted domain is
used as a mutable fixture.

The active callback is an explicitly deterministic guard, not a real issuer
constructor: it preserves a fixed original deadline, optionally calls actual
`check_binding`, and records callback order. The final-read cost control advances
that synthetic clock only after the original real `_read` returns. Source checks
and the unchanged installed-map entries establish that original import active/
deadline call sites were not edited; no execution-time owner-cost claim follows.

## Fourteen selected methods

1. Seventeen outside checks versus two successful-phase reads; two real registered
   bindings, returned-identity copy independence, and actual trust calls from every
   original active callback while 17 pin checks become two real pin reads.
2. Independent domains with the same support and separate objects opened on the
   same persisted path: three objects require six real reads.
3. Wrong types, wrong-domain and unregistered bindings refuse after cached success;
   the original valid binding is not spuriously denied by those unchanged errors.
4. Separate phases and ordinary calls remain fresh; a between-phase persisted
   marker is detected and denial cannot be cleared by another phase.
5. Independent nested phases, body failures, restoration of outer scope and fresh
   ordinary calls. A copied context from a completed phase refuses
   `TRUST_PHASE_CLOSED` rather than reviving cached observations.
6. Nested observed tampering latches denial and defeats an outer cached result,
   even after fixture bytes are restored.
7. Actual adoption-byte change and actual same-byte record replacement both fail
   the final read and latch; the original file is retained during replacement.
8. Each in-memory generation field is independently mutated: path, raw adoption,
   directory key, record key and identity. Cached checks must reject and latch
   without another persisted read.
9. Real persisted withdrawal after first touch, including a marker created by
   the final pin checker. An event trace proves the final trust read occurs after
   that pin sweep and rejects the marker.
10. Real local `withdraw` immediately latches denial and writes the exact adoption
    marker; no cache suppresses revocation or reports success afterward.
11. A real missing first-read record fails, is never cached successfully, and its
    restored bytes do not revive the denied object.
12. The original deterministic guard fails on a cached hit, at ordinary pin exit,
    and after the final trust read consumes the synthetic deadline; no renewal.
13. A previously unseen domain first touched by a final active callback refuses
    explicitly, performs zero late-domain disk reads and cannot escape finalization.
14. Original expected-pin/checker conflicts, changed final pin, uncached failed
    comparisons and outside-scope freshness remain. AST inspection verifies the
    existing `PP.phase(self._active)` integration and synchronous `_live_phase`
    with original owner/snapshot calls and no await/yield.

The suite explicitly selects those fourteen names, rejects skipped/failed/errored
or forbidden-call runs, checks both ContextVars are restored after each method,
and emits actual read counts, traces and the complete logical-source map. No test
result is claimed yet. All `native_calls`, `network_calls`, `proof_calls` and
mathematical-acceptance indicators are deliberately non-authority boundaries.

## Decision value and next gate

The controls can establish deterministic elimination of redundant persisted
reads while preserving the selected denial/freshness/deadline contract. They
cannot establish a measured whole-operation speedup, fixed seconds saved, mirror
authoring success, worldwide readiness or useful mathematical growth.

After independent combined source/selector GO, root may select one finite
native-free operation. Its exact snapshots, all fourteen methods, full logs,
actual fixture counts, clean closure and complete known CPU require an independent
terminal audit. No automatic installation, budget increase or Mirror01 retry
follows from this source checkpoint.
