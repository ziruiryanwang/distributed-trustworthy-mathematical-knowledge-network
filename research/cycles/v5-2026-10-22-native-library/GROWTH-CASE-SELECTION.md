# Growth-case selection: two real workflows, no new campaign selected

2026-10-24. Source/theory assessment by `growth_case_selection` for root. The
canonical guard passed. Read AGENTS, GOAL, NOW, GROWTH-FIRST-ARCHITECTURE-DECISION,
PRACTICAL-NEXT-DECISION and GROWTH-COMPARATOR-CHALLENGE. Only small read-only
primary-source requests were made; no repository clone, dependency download,
compilation, product import, owner opening, experiment or Git mutation occurred.

## Selection

**Retain ordinary Lean/package interchange; select neither candidate for a new
growth experiment or architectural expansion.** Both workflows contain meaningful
mathematics beyond fold/involution demonstrations. Both already have timely Git
and package routes. Neither supplies evidence that our additional adoption layer
improves an actual independent consumer's outcome or total cost.

The first is a plausible later compatibility case. The second exposes a real
semantic gap, but its inspected adapter is explicitly unsound and therefore is
not a ready checked artifact. Creating new mathematics to fill that gap merely
to produce a successful showcase would invert the user's payoff priority.

| Workflow | Substantive contribution that could help a consumer | Present disposition |
|---|---|---|
| Sparse Gaussian covariance estimation to a tractable optimization formulation | A model-specific objective/feasible-set reduction, with an explicit map back to original solutions | Authentic existing parameterized reduction; ordinary package first; no demonstrated adoption friction |
| LLVM-to-RISC-V lowering through SSA rewrite correctness | A genuine refinement-preserving context theorem plus operation/representation bridges for poison, overflow and width conversions | Inspected equality adapter uses an unrestricted axiom; reject that adapter, defer new compiler-verification research |

These are local consumer workflows, not mandatory network tasks. No intention,
popularity or uptake criterion enters mathematical acceptance.

## 1. Covariance estimation: substantial existing bridge, package first

**Inspected source.** CvxLean commit
`c62c2f292c6420f31a12e738ebebdfed50f6f840`. Its
[covariance example](https://github.com/verified-optimization/CvxLean/blob/c62c2f292c6420f31a12e738ebebdfed50f6f840/CvxLean/Examples/CovarianceEstimation.lean)
defines `covEstimation n N α y`: maximize a product of Gaussian densities over
positive-definite covariance matrices, subject to an inverse-matrix sparsity
constraint. The parameterized `red/covEstimationConvex` development transforms
the objective using logarithms, moves products into sums, uses the sample
covariance quadratic-form identity, and changes variables by matrix inversion.
This is a substantive application bundle, not a new generic inverse law.

The explicit mathematical interface is already available in
[Reduction.lean](https://github.com/verified-optimization/CvxLean/blob/c62c2f292c6420f31a12e738ebebdfed50f6f840/CvxLean/Lib/Reduction.lean):
`Reduction p q` contains `psi : E → D` and
`psi_optimality : ∀ x, q.optimal x → p.optimal (psi x)`.
`Reduction.trans` composes these witnesses and `Reduction.toBwd` maps
`Solution q` to `Solution p`. The
[solution definition](https://github.com/verified-optimization/CvxLean/blob/c62c2f292c6420f31a12e738ebebdfed50f6f840/CvxLean/Lib/Minimization.lean)
requires both a point and an optimality proof.

**Potential independent use.** A statistical-model consumer could use this
reduction after proving its own likelihood, feasible set and coordinate choice
correspond to this formulation. The new-to-consumer object would be that concrete
model correspondence, or the existing parameterized reduction if not already
known. It would not be `Reduction.trans`, a new filename, or one theorem per
dataset. Different data parameters do not establish many independent insights.
The inspected repository demonstrates the producer-side method; this assessment
does not establish that such an independent consumer currently needs our route.

**Strong baseline and remaining friction.** A good Lean consumer gets mathlib's
matrix/analysis results and CvxLean's exact reduction through its public Git
commit, searchable source and locally approved package. The same facts must be
available through both sharing routes at the same time. Reusing the reduction
could avoid rebuilding its model-specific derivation relative to isolated work;
no source inspection bounds the strongest independent proof strategy. There is
currently no measured or otherwise evidenced additional advantage over the
ordinary package route.

The plausible narrower product service would let an owner with the compatible
base accept one missing reduction as inert checked mathematics, avoiding review
or execution of a new producer's automation. That is conditional on real owner
policy, existing common context and extraction/admission cost. Ordinary sharing
can also carry extracted evidence or use approved checking tools. Do not assume
the baseline must install an entire foreign toolchain per theorem.

**Metadata and compatibility.** Source uses `reduction*`, `conv_opt`, local
transformation attributes, `simp`, `solve`, and generated backward maps.
[Equivalence.lean](https://github.com/verified-optimization/CvxLean/blob/c62c2f292c6420f31a12e738ebebdfed50f6f840/CvxLean/Lib/Equivalence.lean)
imports `CvxLean.Meta.Attributes`; its registrations support automation. An
already checked reduction can in principle be applied explicitly through its
fields, but importing its mathematical declarations alone does not recreate
those commands or transformation databases. The current commons preserves
original owner-approved metadata through exact original artifacts; new portable
deltas do not convey arbitrary new registrations. Source-level possibility is
not an established supported extraction or admission of this example.

Its pinned
[toolchain](https://github.com/verified-optimization/CvxLean/blob/c62c2f292c6420f31a12e738ebebdfed50f6f840/lean-toolchain)
is `leanprover/lean4:v4.8.0-rc1`, different from the project's retained v4.34.0
foundation reference. Rechecking or porting compatible mathematics is real work;
matching printed names does not remove it. The example's approximate solver
status/value and floating-point backward map are not a `Solution q` proof.
Do not claim certified numerical optimality from the verified reduction alone.

**Falsifiers and smallest useful check.** Reject a bespoke extension if the
consumer already imports CvxLean cheaply, the local model correspondence is
trivial, executable automation supplies nearly all value, version adaptation
dominates, or no relevant consumer need exists. Before any runtime, use one
independently specified consumer endpoint and its existing pinned imports to
inspect whether this exact reduction is applicable and whether its explicit
interface suffices. Compare the missing obligations and approval steps with
ordinary package/source use. If ordinary import wins, use it. Without that
endpoint, a newly invented covariance fixture would establish mechanics only.

## 2. LLVM/RISC-V: real semantic obstacle, rejected current adapter

**Inspected source.** Lean-MLIR commit
`b8c4a771319a044854a4bbb49b8821381ef86ff8`. Its
[core rewrite file](https://github.com/opencompl/lean-mlir/blob/b8c4a771319a044854a4bbb49b8821381ef86ff8/LeanMLIR/LeanMLIR/Transforms/Rewrite/Rewrite.lean#L135)
requires `PeepholeRewrite.correct : lhs.denote = rhs.denote` and supplies
`denote_rewritePeepholeAt` and repeated-rewrite correctness. The file contains
axiom-output guards listing `propext`, `Classical.choice` and `Quot.sound` for
those core theorems. This is existing reusable mathematics; no new general
equality-substitution theorem is needed from us. The guards were read, not run.

The separately inspected
[LLVM/RISC-V wrapper](https://github.com/opencompl/lean-mlir/blob/b8c4a771319a044854a4bbb49b8821381ef86ff8/SSA/Projects/LLVMRiscV/PeepholeRefine.lean)
uses a different contract: `LLVMPeepholeRewriteRefine.correct` proves
`PoisonOr.IsRefinedBy` pointwise. It explicitly documents the mismatch with the
equality rewriter and declares:

```lean
axiom refinement_correctness {p : Prop} : p
```

`LLVMToRiscvPeepholeRewriteRefine.toPeepholeUNSOUND` then supplies that axiom as
the equality witness. The
[multiplication lowering file](https://github.com/opencompl/lean-mlir/blob/b8c4a771319a044854a4bbb49b8821381ef86ff8/SSA/Projects/LLVMRiscV/Pipeline/mul.lean)
defines width/overflow variants and uses this adapter in `mul_match`.

**Disposition and scope.** This exact adapter is inadmissible under the project's
fixed permitted-axiom policy: the unrestricted axiom can instantiate `False`.
It is an actual new axiom, not an abstract public view backed by a checked private
declaration. Extracting an application must preserve complete support; hiding
this dependency behind a familiar theorem name cannot make it eligible. This
finding concerns this wrapper and dependent use, not the validity of the whole
Lean-MLIR library. The core equality theorem and the wrapper make different
claims. No axiom audit of every individual lowering lemma was performed here.

**Potential valuable bridge.** A producer could prove a refinement-preserving
rewrite/context theorem for the actual semantic relation, with congruence or
monotonicity obligations for the contexts and operations. Independent compiler
developers could then compose width/overflow/representation lemmas into checked
lowerings. Refinement alone cannot imply unrestricted equality: replacing a
poison result by a defined one is the motivating countercase. A sound route
must retain a refinement conclusion, or impose and prove adequate definedness
restrictions before using equality. A general unchecked renaming cannot fix it.

This is feasible as a mathematical research direction, not a source-established
small repair. Context semantics, casts, poison, effects and operation hypotheses
have to be specified and proved compatible; an existing alternative development
may already supply some of this. This bounded scan does not establish absence
of such work elsewhere. Creating that theory solely for our demonstration has
no justified payoff compared with using an already sound ordinary library.

**Strong baseline, metadata and falsifiers.** Lean-MLIR already provides Git,
cached package installation and reusable rewrite proofs. Its
[README](https://github.com/opencompl/lean-mlir/blob/b8c4a771319a044854a4bbb49b8821381ef86ff8/README.md)
documents distinct project maturity and advises polishing cross-project code
into core or cloning it. This is evidence of integration policy, not evidence
that users want another network. The source uses dialect quotation, custom
simplification registrations, `simp_lowering` and `bv_decide`; checked result
terms do not transfer the executable authoring environment. Its
[toolchain](https://github.com/opencompl/lean-mlir/blob/b8c4a771319a044854a4bbb49b8821381ef86ff8/lean-toolchain)
is `nightly-2025-12-01`, also not the retained project foundation pin.
If stock bitvector automation cheaply solves the selected endpoint, copying its
proof is not a demonstrated productivity gain. If a sound existing package
already supplies the relevant refinement interface, use it. If it does not,
transport engineering cannot supply the missing theorem.

**Smallest decision-changing check.** The source inspection already rejects
this adapter without compilation. Reconsider only on evidence of an existing
sound bridge under the same semantic relation and an independently needed
consumer endpoint. Then inspect its actual statement, complete support and
package compatibility before selecting any execution. No compiler-framework
extension, imported axiom exception, or new proof campaign follows from this note.

## What is missing and what should happen next

The missing evidence is a consumer with an independently useful endpoint, an
actual compatible reusable artifact, and a remaining adoption obstruction after
allowing timely searchable Git, approved packages, warm caches and the same
checking tools. This can come from existing project use or documented adoption
work; it need not be a global experiment. Neither inspected case supplies all
three. No outside party was contacted and no demand is inferred from repository
stars, examples, theorem count or scientific importance.

Use these cases to keep the architecture honest: ordinary package compatibility
and explicit checked applications have higher demonstrated relevance than a new
protocol, automatic bridge synthesis or identity migration. Preserve the current
integration evidence separately. Its diagnostic-file defect and repair are not
growth observations. If no concrete residual adoption problem is identified,
do not select another comparative campaign to manufacture one.

Primary-source contents were read at the exact commits linked above. No build,
full dependency closure, numerical solver claim, exported artifact size or
commons support for either external project was established. The unchanged
L/O/C and full-cost requirements in GROWTH-FIRST-ARCHITECTURE-DECISION apply;
this note introduces no new break-even formula or proof-search hardness premise.
