# Validation-phase successor: combined independent source review

2026-10-20, `core_release`. **GO for one root-selected focused control run.**
No product import, test, native/proof execution, build, selector execution or Git
mutation was performed by this review. This is not an outcome audit, mirror
success, end-to-end speedup or final-v5 acceptance. Root owns adoption and launch.

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
The canonical guard passed. Basis is current114 map
`995525c5cbf2746718cbf583a3e3e401bc56c2f88d1cef8664ffeb1b644454be`.
The selection is `VALIDATION-PHASE-SELECTION.md`; diagnosis is
`MIRROR-CPU-CAUSE.md`. This review challenges the repair rather than duplicating
the diagnosis or requesting another timing/RAM campaign.

## Exact reviewed bytes

Paths below are relative to the canonical root.

| Path | SHA-256 |
|---|---|
| `software/v5/validation_phase/admission/trust.py` | `c997d2a83ae5246dec9ff30eeca72e405ec0f66c0a307e53e0521eef66fae6d0` |
| `software/v5/validation_phase/admission/pin_phase.py` | `76b54eb04fa2a66ec598b8c6d668e675d8bd483809f8fa66448fa7319b82a9ce` |
| `software/v5/validation_phase/controls.py` | `775a68abca3c5ac3c094a1ee921c1b2bc367a5a55a753e34783b0c3a76da4b0a` |
| `research/cycles/v5-2026-10-20/Select-ValidationPhase01.ps1` | `9a5a039829d85041fafb413fb1d284b826eec42da790f876b2e03a21b2665141` |
| `research/cycles/v5-2026-10-20/Select-ValidationDistribution01.ps1` | `94702a0a71cdbfb90525b6e19f550070da6a927c283cd5c0c3f2e9ea03204b0d` |
| `research/cycles/v5-2026-10-20/Select-MirrorMethod02.ps1` | `489beb998553a4c40d35437f0c4c7e1b2634fd6632c6ca2ccacce9083e3e634f` |

All six files were read completely, including final control pins, copied-context
refusal and mirror-copy rehashing. The five-entry
`VALIDATION-DISTRIBUTION-SOURCES.json` agrees with the two reviewed successors
and the already independently adopted three-source pair-planning change.

## Why the two-file implementation is acceptable

Let a successful selected phase touch exact domain objects `D` with fixed
generations `G(D)`. The code establishes a full first persisted check for each
`D`, checks its same generation and sticky-denial flag on every subsequent
`_current`, and completes a fresh full persisted check of every touched `D`
after the final installation-pin sweep. It then invokes the original active
callback after each fresh trust read, before the trust scope closes. No cached
observation is returned as a mathematical warrant.

This is sufficient under the existing owner-stable, synchronous validation
contract: repeated intermediate reads establish no additional persistent fact.
It is intentionally **not** equivalent sampling under arbitrary concurrent
filesystem mutation. A transient marker created and removed between observations
can be missed; distinct domain reads are not an atomic global snapshot. The
successor docstring states the changed granularity and trusted local premise.

The implementation meets the consequential safeguards:

- `_read` is unchanged: ordinary ancestors, marker-before/after, bounded regular
  single-link file, open/file identity and directory stability remain checked.
  `_fresh_current` retains the original complete comparison and sticky exception
  handling. It cannot consult the phase cache.
- The cache is keyed by the exact `TrustDomain` object. Its generation snapshots
  path, raw adoption bytes, directory key, record key and identity values.
  Every cache hit checks exact type, denial and generation. Equal paths/support
  hashes do not merge distinct domain objects.
- `check_binding` and registered-binding membership remain uncached. Issuer
  identity, owner profile/origin, resource and deadline checks are unchanged.
  `withdraw` still sets denial before persistence; a cached hit cannot revive it.
- The finalizer checks generation before and after its uncached fresh read.
  Finalization-only new domains refuse explicitly. The callback following each
  final read checks the original cost/deadline guard while trust reuse remains
  active, so it does not recursively repeat disk reads.
- Successful, body-failure and finalization-failure exits clear records, mark the
  state closed and reset the context. Nested phases have independent state.
  A copied context cannot reuse a closed trust scope. Outside any scope, every
  `_current` remains a fresh full persisted check.
- `PP.check_pin` and all original phase callbacks/final pin checks are preserved.
  The new trust scope starts before the original entry callback, so its trust
  checks participate in the first read; it ends after the pin sweep.

I also reread the selected `interface_views/imports_atomic.py` `_live`,
`_live_phase`, `_active` and `_snapshot` paths and their relevant issuer guards.
The existing phase performs synchronous owner/origin/pin/source validation, not
native dispatch, network operations, user callbacks, publication or warrant
minting. Its fixed active callback does not call pin checks; resetting the pin
context before final trust callbacks does not move a pin check into an outer
scope. The two-file change does not widen this caller boundary. Future expansion
of that call graph needs a new review; the helper is not an arbitrary-action cache.

For successful phases without provisioning inside them, the persisted `_current`
read contribution changes from `sum(q_j)` to `2 * sum(d_j)`, where `d_j` counts
exact touched domains independently per scope, including nested scopes. Original
liveness callback counts are not reduced. This is an operation-count argument,
not proof that the entire mirror workload fits 120 controller-CPU seconds.

## Focused controls and selectors

The 14 selected control methods use real fresh inert local-policy records and
delegate counted reads to the real `_read`. They check 17 ordinary reads versus
two scoped reads; issuer-like active-callback composition and real pin first/final
checks; same-path distinct-domain separation; binding guards; repeated/nested
scope freshness; body exceptions and closed captured context; adoption bytes,
file identity and in-memory generation changes; sticky observed withdrawal;
withdrawal created by the final pin sweep; actual local `withdraw`; failed first
read; cached/final deadline failures; a synthetic clock crossing only after the
real final trust read; new-final-domain refusal; and pin conflict/freshness rules.
The unchanged import seam is additionally inspected structurally. These are
changed-boundary controls, not a claim of actual receipt/Lean execution.

Source staging uses the fixed current114 map with exactly the two replacements,
hash-checks/copies its logical source tree and validates loaded origins. Product
imports and tests are under subprocess/system/socket guards. The report requires
all 14 methods, no skips/failures/errors/forbidden calls, with saved observations;
the real filesystem fixtures remain preserved. The original selected mathematical
owners and failed mirror01 state are not fixtures.

`Select-ValidationPhase01.ps1` stages 192 fixed predecessor snapshots plus exactly
three fresh files, validates current114 closure/runtime pins, refuses old output,
and proposes only 45 CPU seconds / 90 wall seconds / 384 MiB / two processes.
It does not execute the controls. No blocker found for this focused envelope.

The other selectors are **source-ready future preparations, not launch approval**:

- Distribution preparation requires exact future validation-outcome bytes and
  adopted pair-outcome bytes, retains the current114 map/assets/builder, replaces
  exactly five sources, and uses fresh input/output under a fixed build envelope.
  Checking an outcome hash verifies identity, not PASS: root must separately read
  and adopt the successful outcome before selecting the build.
- Mirror02 preparation checks the future repaired114 release/map/payloads and
  builder, copies and rehashes exact original owner/template bytes, and changes
  only fresh paths/domain IDs/request name. Mathematical inputs and all original
  limits remain unchanged. It does not renew the failed01 allocation or execute
  the returned launch command. Root must separately adopt the build outcome and
  justify one changed-boundary integration before launching it.

No implementation repair or extra campaign is requested by this review. Preserve
all predecessor files and evidence. The next consequential evidence is the single
focused native-free run, followed by its independent actual-outcome audit.
