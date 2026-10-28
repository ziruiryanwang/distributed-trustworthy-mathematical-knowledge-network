# First native frontier fixture: failed before frontier cases

2026-10-28 independent saved-data audit. **FAIL for the planned three-case
fixture; clean terminal closure is verified.** No rerun, product import,
owner/catalog/database open, native execution or Git mutation occurred in this
review. All failed source, partial output and accepted setup evidence remain.

Run: `experiments/v5-local-checks/demand-frontier-native01`.

| Evidence | SHA-256 |
|---|---|
| selection.json | `b21425f7c2d9242a44d7c6307351c97b037eca9dea07e15f53044d46168fe18a` |
| RESULT.json | `f7d6e1af9802501837b4b73e84ff374019207e3c4596c9dead40b824ba41975d` |
| workflow/OUTCOME.json | `a3737d9678a924a0be3212cf5057b86e1d6a4de1e151ec6dc56ff419a4fe5ecf` |
| setup-p/FAILURE.json | `cc5e4115db86ae135675869e912c4c40c78e3f16d4aa91351fd3873a48a29dfe` |

All four selected source hashes match both actual snapshots and retained current
source. All 164 selected external input/runtime hashes still match. The source
is the reviewed `2cd81f0d...` workflow, including both pre-launch `@[expose]`
corrections. The inspected package and receiver identities are unchanged.

The saved events establish a successful 456-unit/581-name basis at
`0d57737d263d880fe3e9827b991ed0bd02fd6459dc883c2856d22e2a8f0220ab`,
then a successful one-unit F contribution at
`ee9fbadfbb73199964a37ceeade5db64d39f71114aca4bf7cb673a5af0849da4`.
F's retained exact evidence defines `Base.c : Nat := Nat.zero`; its evidence and
preview lengths/hashes match the contribution result. Both native worker reports
and clean zero-exit supervision reports agree. Their retained artifacts are
669,968 and 1,000 bytes. These are saved acceptance events, not a fresh query of
the currently eligible protected database state.

SETUP_P then attempted plain `def Above.d : Nat := Nat.succ Base.c`. Its request
is the original seven-field **DMKN_OWNER_REQUEST_V2**, with no frontier fields.
It fetched the exact one Base.c unit. The native log reaches
`CONSTRUCTED_READY_FOR_AUTHORING_INSTALL` with `checkedUnits=1`, followed by:

```text
failed to compile definition, compiler IR check failed at `Above.d._closed_0`.
Error: unknown join point 'block_0'
```

Lean also reports LCNF ExplicitBoxing and missing-map/option panics. The authoring
process exits one and is cleanly reaped. This establishes failure during executable
code generation after successful scratch construction; it does not identify a
kernel proof rejection or establish the complete compiler bug's cause.

The contributor refuses with `CONTRIBUTION_AUTHORING_NOT_CLEAN` in AUTHORING,
with `accepted: null`. A 1,779-byte `setup-p/candidate.json` was emitted before
the failed process ended (SHA-256
`a93e5340702f819e8b5288c571c73c5234b233b72628878a84b9961a83cf5ba6`).
It is **inert failed-authoring output, not an accepted result**. The driver stops
before binding or admitting P. Exactly two admission-call and two operation
directories exist, belonging to basis and F. There is no P native admission.

OUTCOME has phase SETUP_P, one completed setup result, zero cases and no owner/
custody close errors. Positive, false-parent, missing-name and alternate-frontend
directories are absent. Thus no V3 frontier case ran, no ancestor-fetch claim was
tested, and the proposed false-under-parent/missing-name controls remain open.
This failure must not be labeled a passing negative control.

The outer report is COMMAND_FAILED with exit one, child reaped, Job closed,
zero active or terminated processes, no cleanup errors and no termination request.
Measured wall time is 17.4836364 seconds; Job CPU is 16.515625 seconds plus
0.59375 separately reported wrapper CPU, totaling 17.109375 known CPU seconds.
Peak Job private commitment is 925,257,728 bytes. Outer stdout/stderr are
0/2,625 bytes; the outer stderr is the propagated Python failure traceback.
No OS resource termination is recorded. Inner observations are contained costs,
not additional charges. The selected run is terminal, not a live experiment.

The next decision should address ordinary authoring without executable metadata
for reconstructed mathematics. A source-level noncomputable mode or approved
local module route may be suitable, but neither is qualified by this failure.
Any correction needs a fresh root selection; no retry, budget increase, old-state
reuse or backend rewrite is selected by this audit. Full v5 remains unfinished.
