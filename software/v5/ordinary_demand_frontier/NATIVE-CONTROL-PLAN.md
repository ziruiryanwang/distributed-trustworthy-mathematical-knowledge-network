# Tiny real demand-frontier workflow: source checkpoint

Status: design/implementation preparation only. No runtime, build, package load,
owner/database access or state mutation has occurred. Root owns later exact
selection, review and execution. Actual package root and PROFILE hash will be
explicit required inputs; no future identity is guessed.

The proposed driver loads the selected ordinary package through its existing
public bootstrap/profile API, creates one fresh owner and custody store under a
fresh output, and initializes the existing foundation once. Two ordinary source
contributions establish F (`Base.c : Nat := Nat.zero`) and P extending F
(`Above.d : Nat := Nat.succ Base.c`). Each new declaration is genuinely checked;
the driver neither fabricates an accepted root nor adopts synthetic warrants.

Use the actual returned Above.d name/export/unit triple. All three controls
select the original P and frontier F. One serial owner lifecycle and existing
bounded native supervisors avoid extra public CLI/bootstrap overhead. Every
authoring attempt is a fresh native process. Existing evidence reads are traced
with a pass-through guard; frontier evidence is forbidden during the three cases,
while needed Above.d reads and actual parent snapshot checks remain allowed.

The positive approved frontend supplies zero-valued Base.c and no Above.d. The
negative approved frontend supplies successor-zero-valued Base.c and no Above.d.
The missing-name frontend imports Init only. The positive theorem is
`Above.d = Nat.succ Nat.zero`; the semantic negative is
`Above.d = Nat.succ (Nat.succ Nat.zero)`. Both proof bodies are `rfl`.
The semantic negative passes actual authoring and candidate binding, then must
fail native admission against P. Any earlier refusal is inconclusive. The missing
case must fail construction once, with no candidate/native admission/fallback.

Root approved the direct public API path and reuse of F's actual ordinary
authoring output (`setup-f/lean-build/OrdinaryProducer` and its five artifact
parts) as the positive frontend. The generated case module has a distinct name.
Its imports resolve using the existing helper/runtime/project order. Exactly
one additional tiny frontend build supplies the negative definition; the missing
case imports Init only. Positive/negative constructor logs must each show one
construction invocation and one checked construction unit, demonstrating that
Above.d was reconstructed rather than already installed. No fallback frontend
build is available if reuse fails.

Pre-launch source correction: both definitions of Base.c now explicitly use
`@[expose]`. The pinned Lean 4.34 source
`src/lean/Lean/Elab/MutualDef.lean` (the `wouldBeExposed`/`hasExpose` branch near
line 1346) exposes ordinary definitions by default only in an expose section;
`public section` alone does not do so. `Lean/AddDecl.lean` near line 224 describes
the separate public body projection. The imported Base.c body must therefore be
explicitly exposed for these `rfl` controls. This changes only the two unused
fixture source strings; Above.d is reconstructed from its complete checked group
and already exposed by the existing construction helper. No test or compile was
needed to identify this deterministic setup issue.

Record exact inputs, acquired/frontier bindings, generated request/header and
source, all supervision reports, candidate outputs, actual acceptance/refusal
phase, evidence-read trace, accepted-root inventory before/after refusals and
unchanged package identities. Every failure retains prior accepted roots and all
partial outputs. Whole-run and per-case budgets are fixed prospectively; no
retry, renewal, networking, certificate, full Std replay or old-state access.

The source driver is `native_workflow.py`. Required arguments are `--package`,
`--profile-sha256` and `--output`; output must be the fresh `workflow` sibling of
the runner's source snapshot. Snapshot the driver and the same pinned file-only
utility used by the build. The package remains a separately selected input.

Its prospective whole allowance is 360 wall / 220 aggregate-accounted CPU
seconds. Initialization has 120/70; each setup contribution and positive/negative
case has 90/45; alternate compilation and missing-name case each have 60/25.
Every allocation is clipped to the original parent remainder. Native memory
is 1536 MiB; each existing native Job has at most four processes and the default
1 MiB streams. Propose one enclosing 420-wall/260-CPU/2048-MiB/eight-process Job
with 4 MiB streams. These are limits, not predicted costs. Root selects the actual
outer operation. Success would comprise five admission invocations (basis, F, P,
positive and false-parent), five authoring invocations and one alternate build.

The false-parent check inspects the exact unit delivered to the actual native
admission call: its type must be `Above.d = succ (succ zero)` and its proof must
have reflexivity as its head. The genuinely checked F/P definitions establish
that Above.d evaluates to succ zero. A clean nonzero native event and the existing
kernel-rejection marker are required. The existing marker combines type rejection
and internal kernel resource failure; this test does not strengthen that diagnostic.
It establishes that this explicitly false statement reached the kernel and was
refused without OS-level resource termination. Earlier failures remain inconclusive.

Source review and actual root launch selection are still required. No control,
native compilation or owner operation has run during this source preparation.
