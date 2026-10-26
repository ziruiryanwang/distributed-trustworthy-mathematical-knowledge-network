# Real-library interoperability: evidence and next-decision boundary

2026-10-26. `current_acceptance_challenge`, source/data review for root.
Canonical workspace guard passed. No native program, build, owner state, test,
network, download or Git mutation was run. Paths below are relative to the sole
canonical project root. This file is a decision checkpoint, not runtime selection.

## Decision

**The existing APIs provide a coherent selective-library route, but retained
evidence does not yet establish end-to-end reuse of a nontrivial standard-library
method through that route. No newly demonstrated defect justifies converter
redesign or another unconditional library experiment.** Preserve ordinary
approved Lean packages as the primary working format. Do not export a library
merely to use mathematics already available in its approved local environment.

The distinction matters: absence of representative evidence is not evidence of
incompatibility; having a general API is not evidence that every library fits it.
The decision does not revisit the separately owned branch-composition question,
repeat the completed commons archive work, or assert final-v5 readiness.

## What is already established

| Evidence | Actual scope | What it does not establish |
|---|---|---|
| `ORDINARY-EXTRACTION-NATIVE-REVIEW.md`, actual completion02 | Public `contribute -> extract-std -> complete` acquired the full installed `Nat.add_zero` proof and checked the two-unit supplier/consumer closure | Nontrivial Std data structures or a broad standard library |
| `PRODUCER-PUBLIC-SELECTION-AUDIT.md`, saved public-export audit | Installed owner-free `produce-baseline` emitted the same six-unit inert bundle as the retained exporter; no owner registration or certificate | Its controlled Flag/flip fixture is not a genuine standard-library workload; production is not admission |
| `ORDINARY-MODULE-ANCHOR-SOURCE-REVIEW.md` | Controlled approved-project completion and incremental checked-module operations have actual evidence | Independently supplied real projects, arbitrary package semantics or general library compatibility |
| `experiments/lean-library-interop/RESULTS.md` | Historical `Fin.castLE_castLE` selected closure included private/generated support and a substantive successor | Success on the current v5 public producer/intake/module pipeline |

The three named review files above are under
`research/cycles/v5-2026-10-22-native-library/`. Completion02 is
`experiments/v5-local-checks/ordinary-library-public-completion-02`;
owner-free production is `ordinary-producer-public-export-01` below the same
experiments directory. The latter actually took 7.393 wall seconds and 4.859375
known CPU seconds, but only for its six-unit controlled fixture. Neither number
predicts a larger library's cost. Old source-only README wording is superseded
by these saved actual audits, not by a fresh invocation.

## Source argument: what the existing mechanism promises

Let B be the fixed 581-name basis, T selected exported declarations, and C(T;B)
their complete nonbasis declaration-unit closure, including whole inductive
groups and referenced proof bodies. The route is:

`approved compiled modules -> inert C(T;B) -> recipient checking -> selected use`.

`ordinary_baseline/BaselineExporter.lean` imports explicitly selected installed
or approved project modules privately, rejects incomplete/unsafe targets,
checks basis correspondence and exports complete selected closure. It calls
`Export.indexSource` over the whole loaded environment before selection.
Therefore bounded output does **not** imply producer time/memory proportional
only to C(T;B). No asymptotic improvement is claimed by this interface.

The producer's 8192-unit envelope is not the 32-unit completion envelope.
Existing `intake-baseline` can batch admission; peer receive separately permits
at most 1024 missing units. Cold checked-module realization still permits
32 units / 4 MiB, or an explicit compatible anchor plus a bounded new delta.
Whole declaration groups remain indivisible. An accepted larger bundle need
not fit cold realization; conversely the unequal limits do not prove that all
larger bundles are unusable. Fit is route- and recipient-relative.

Current `ordinary_exact_module/OrdinaryModule.lean` also removes a misleading
historical objection. `classifyUnits` can match an installed declaration exactly
instead of refusing every Init collision. Existing private theorem records must
match full inventories; the public theorem handle may be axiom-shaped only after
that complete private match. Non-theorems require exact concrete records, and
`matchNonTheorem` checks complete inductive membership/metadata and dependencies.
The added delta is kernel-checked again under public imports; private success
never waives public conversion failure. Thus older blanket collision/erasure
failures cannot be promoted into a universal current blocker.

These source properties establish a conditional route, not a universal Lean
compatibility theorem. Unsupported declarations, bound exhaustion, public/private
conversion, generated groups and exact-name conflicts can still refuse. Checked
modules preserve supported declarations, not arbitrary notation, simp/class
registrations, tactics or an ordinary package's executable behavior.

## At most one conditional discriminator; not selected now

If a real recipient needs **independently checked inert reuse without approving
the producer's executable package**, use the already installed declaration
`Std.HashMap.isEmpty_insert` from `Std.Data.HashMap.Lemmas` as one candidate.
It concerns actual map insertion under `EquivBEq`/`LawfulHashable` assumptions and
delegates to the dependent-map implementation. Its source imports real Std data
and private support; unlike `Nat.add_zero`, it crosses a nonbasis library-data
and transitive implementation boundary. No theorem fixture or new mathematical
claim is needed merely to select this existing declaration.

First ask only whether its **existing producer route** can emit the exact full
closure within one prospectively bounded allocation. Inspect closure counts,
groups, selected bytes and the first refusal before considering admission.
Do not assume its closure is small, infer it from source-line count, raise limits,
try neighboring lemmas until one passes, or build a new exporter on failure.
Root must separately select exact inputs, one finite envelope and fresh output.

Continue to an existing admission/use route only if the inspected bundle fits
that route and the selected recipient actually requires it. A public-API refusal
or excessive closure is already decision-changing evidence: choose approved
ordinary-package use where acceptable, or reconsider the precise missing inert
assurance requirement. No automatic module-realization, proof-generation or
growth experiment follows. This is one conditional case, not a campaign.

Why not launch it now? No independent real project or consumer requirement has
been supplied, and ordinary approved-library use already serves local work.
Testing this theorem solely to replace “unmeasured” with “passed” would not show
better discovery, concept formation, useful growth or lower total cost.

## Consequence for priorities

Keep the coverage gap explicit; do not label current interoperability universal.
Spend the next implementation budget on an observed user-path obstruction,
not a speculative conversion optimization. A genuine selected need for inert
Std transfer would make the single discriminator above relevant; until then,
the source-level route and its explicit bounds are sufficient for this decision.
The test would judge compatibility/cost only, never creative-growth superiority.
