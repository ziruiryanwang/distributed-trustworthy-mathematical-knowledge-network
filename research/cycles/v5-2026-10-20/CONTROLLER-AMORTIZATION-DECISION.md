# Controller amortization: narrow safe boundary, not a lifetime trust cache

2026-10-21. core_release; source-only independent decision. No execution,
profiling, implementation, new proof or repeated mirror operation.

## Decision

**GO in principle for phase-local amortization of standalone mixed-admission
installation validation. NO-GO for an unqualified operation-lifetime snapshot.**
The existing pin/trust/origin scopes already solve this inside import `_live`.
The concrete gap is that direct `MixedDeltaVerifier._check` calls do not enter
that scope. Reuse the existing boundary mechanism if selected; do not invent a
second authority cache or remove live checks to lower a timing number.

## Current implementation, not historical logical-path predecessors

Resolved through origin114 input SHA `2ea8322879b2e45afb2a2f5e8d99500bfcfdbe0982cdf14687b1e8bdd0950556`:

- `admission/pin_phase.py`: `origin_phase/admission/pin_phase.py`, `c00e1259...`.
- `admission/verifier.py`: `origin_phase/admission/verifier.py`, `32289cac...`.
- `admission/trust.py`: `validation_phase/admission/trust.py`, `c997d2a8...`.
- `mixed_claims/receiver.py`: `runtime_efficient/mixed_claims/receiver.py`, `aa591a18...`.
- `mixed_claims/imports_atomic.py`: `interface_views/imports_atomic.py`, `e38ac52a...`.
- `mixed_claims/authoring_atomic.py`: `interface_views/authoring_atomic.py`, `081d9d18...`.
- Aggregate issuer: `trust_withdrawal/aggregate_claims/aggregate_admission.py`.

All abbreviated source paths here are beneath `software/v5/`.

## Exact amplification

`receive` calls mixed `_check(deadline)` before staging, once per claim, twice
per native witness (before/after the subprocess), and twice during finalization
(receiver lines 241,252,281,295,303,309). Thus its direct check count is
`3 + c + 2d` for c claims and d witnesses, excluding nested issuer checks.
`describe` also calls `_check` (324). These are not enclosed by `PP.phase`.

Mixed `_check` (141–173) validates module origins/symbols, calls I `_check_install`
and A `_check_live`, then iterates mixed runtime pins. Each pin iteration calls
mixed `_active`, which fans out to both issuer `_active` methods. A inherits
I's `_active`; both reach `T.check_binding -> domain.check -> _current`.
Outside a validation scope, each `_current` invokes `_fresh_current`: repeated
directory/record/withdrawal-marker observations and complete adoption-byte reads.
I `_check_install` itself loops its pins with `_active` at each iteration.

By contrast, import `_live` (165–202) already wraps its entire synchronous graph
in `PP.phase(self._active)`. That graph also calls mixed `_check`, and hence gets
pin-byte, trust-read and absolute trust-origin reuse there. Authoring `_active`
calls `require_view -> _check_view -> _live`; repeated *separate* `_live` phases
still rescan the installation. Their phases must not simply be joined across a
frontend subprocess. Other module-origin loops still use direct `Path.resolve`.

Let q be validation phases, p pin visits per phase, U distinct pinned bytes,
A adoption-record bytes and D its path-observation work. Standalone checks have
an avoidable `Theta(q*p*(A+D))` trust-observation term, plus pin/origin work.
Scoped checking reduces that term to `O(q*(A+D)+q*p)` with constant-size live
guards; distinct pin-byte verification remains `O(q*U)`. This is an asymptotic
argument about this call graph, not measured attribution of all controller CPU.
Mirror03's 195.5625 summed controller CPU versus 202.328125 inclusive Job CPU
identifies where time lies, but does not identify the fraction this change saves.
Report construction, serialization, semantic processing and output census remain.

## One principled boundary

Treat one **standalone synchronous mixed `_check`** as a validation transaction:
observe exact owner installation/pins/trust on entry/first use, retain every
binding, module/symbol identity, expected-pin, profile, denial, deadline and CPU
check, then freshly validate touched files/trust/origins before successful exit.
No handle, accepted result or irreversible publication escapes before that exit.
Retain current mixed-owner revocation on every failure, including finalization.

If already inside import's compatible validation phase, borrow that boundary
rather than creating independent redundant nested sweeps. This needs an explicit
internal compatibility contract, not silently sharing arbitrary caller scopes.
The supplied per-call deadline must still be checked by every added callback.
Never span native/frontend execution, await, network operations or user callbacks;
never reuse packet/body/opening/receipt validation merely because files are pinned.

The threat model already trusts the controller, installed code and local OS/filesystem
during a serialized synchronous phase. Adversarial peers supply inert data, not
constructors, callbacks, pin maps or Python code. Equal repeated trusted observations
can then be coalesced; final persisted withdrawal plus uncached denial/binding checks
remain. Concurrent hostile path replacement/rollback or arbitrary same-process mutation
is not defended by this boundary, nor by the existing guards: they are not a sandbox.

A one-time lifetime snapshot would instead need genuinely immutable private runtime
configuration and a defined update/revocation protocol, plus fresh checks around each
external execution boundary. Public mutable objects and current file-change refusal
contracts prevent claiming it is a drop-in equivalent optimization. Defer that redesign.

## Minimal next evidence if root selects implementation

Use focused controls on the new standalone boundary: unchanged expected observations,
fewer real trust reads, exact original active checks, parameter/owner/pin conflicts,
withdrawal/final-sweep refusal and no cached state across external boundaries. Existing
import nesting must not duplicate sweeps or escape failure. No mirror replay is needed
to justify the source contract; any later integrated run needs its own new capability.
