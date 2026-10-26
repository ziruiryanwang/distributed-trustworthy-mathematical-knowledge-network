# Independent exact-name control source review

Disposition: **PASS_LEAN_CONTROL_SOURCE; FINAL LAUNCH SELECTION PENDING**.

Reviewed `KernelAdmissionChecks.lean`, 15,763 bytes, SHA-256
`b8bb7074012ae09e586911e0a0f7e5031173270b4539267f2d4d11b7990743c5`,
and the initial TEST-PLAN, 9,251 bytes, SHA-256
`eb3c40b6164f682732463f2ae94ad8014523e2ce0e6aad8be444a69d8501324a`.
The reviewer read the complete fixture/plan and relevant codec inventory and
Lean declaration-group definitions. No compiler, fixture, native, owner/state,
recovery or Git operation ran during this review.

No Lean source blocker found. The parent is openly conditional on eleven selected
trusted Init records; it is not presented as a new protected basis or independent
validation of Init. Quotient initialization and a stage-one restore are checked.
The explicit false/true distinction and public function type give a consequential
collision case: different full private names, with opposite Bool values, and a
public name with the same user-facing projection. Actual Lean name helpers and
preconditions establish that these are genuine projection collisions.

The first three-unit kernel snapshot and second three-unit snapshot use only
kernel continuation. Each theorem depends on the intended full-name definition.
The second artifact's exact three-name delta is checked despite six stage-two
records. A full chain restore checks both stored name arrays and all actual
inventory rows, then checks a new theorem whose proof uses the restored theorem.
No ancestral proof units are submitted to that new check; this does not claim
that import/acquisition itself is constant-cost.

The refusals distinguish exact duplication from projection collision. The bad
proof first must cause an actual kernel type mismatch, then the production
snapshot route must reject it without writing an artifact. Other controls cover
wrong ordinary row, ungrounded reference, genuine singleton generated group,
tampered constructor field count, stage-two quota, initialized-parent requirement,
and unchanged immutable parent after failures. `Declaration.getNames` includes
this nonnested group's type, recursor and constructor, so its expected inventory
is complete. The tampered row changes the actual `numFields` slot. The unchanged
frontend snapshot API is exercised on a noncolliding declaration.

Expected-row production uses the same kernel/codec; this is appropriate for a
changed-boundary compatibility control, not an independent kernel implementation
or a proof of global soundness. Exact stored rows and the explicit negative
prevent the output label alone from being the test oracle. The sixteen labels
and completion counts agree with the source; counts are successful paths, not
total checking work.

## Launcher decision before execution

The initial plan's inline launcher omits `CREATE_NO_WINDOW` and scrubs only three
environment keys. Prefer the already used build-style cleanup of inherited
Lean/Python/PATH values and hidden subprocess launch. Its proposed two-process
cap is also not established by the build evidence: build01 recorded twelve inner
process creations for five compiler calls. That does not prove the peak process
shape, but warrants allowing a small finite helper-process margin rather than
spending a run on an avoidable harness refusal. This concerns prospective test
limits only, never an increase to product admission limits. Author and root were
notified before any control selection.

A separately reviewed exact selection must bind the actual adopted build objects,
fixture/runtime bytes and fresh output; its complete outer closure, empty stderr,
all sixteen markers, exact completion and artifact census remain actual audit
obligations. This source review authorizes no large Std retry, new identity,
owner migration, package adoption or v5 completion claim.
