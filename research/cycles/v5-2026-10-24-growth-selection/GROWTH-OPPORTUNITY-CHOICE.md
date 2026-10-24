# Growth opportunity: retain solver-discovered mathematical structure

2026-10-24. Bounded source/theory choice. No install, build, experiment, product
edit, migration, Git mutation or LP performance claim. All prior evidence stays.

## Decision first

Do not implement the advisory HTTP client merely because its contract is ready.
Existing tools already provide useful single-provider search; an unmet corpus or
consumer need is not yet identified. The higher-payoff opportunity is to let
**specialized producers return ordinary mathematical certificates which consumers
turn into locally checked results**, and preserve reusable structure discovered
in those certificates rather than only exact-instance answers.

Concretely, investigate the existing Lean LP certificate/proof-construction
packages as an optional ordinary-library route. Do not write a new LP checker,
solver, remote service or certificate format now. The strongest mathematical
growth case is a solver-discovered dual/basis yielding a *parametric theorem*,
not merely another cached optimum. The actionable simplification is to retire
the assumption that useful exchange must preserve the producer's original Lean
proof or solver implementation. A new locally checked proof of the selected
statement is sufficient; never mislabel it as validation of the original witness.

This is a specific instance and source-backed implementation opportunity for the
2026-10-22 reaudit's existing `check(x,w) -> R(x)` principle, not a new invention
of proof by reflection. EVALUATOR-METHOD-THEORY concerns fold uniqueness, while
PROOF-SEARCH-REUSE-CONSTRUCTION rejected the earlier SAT benchmark. Neither result
establishes or forbids this LP route. No rejected campaign is restarted.

## Three realistic workflow classes, not claimed actual adopters

| Workflow | Concrete capability | Existing alternative and adoption burden | Choice |
|---|---|---|---|
| Optimization research or formal analysis varies capacities/bounds while retaining the constraint matrix | Reuse a dual bound or a certified affine optimizer over an explicit parameter region | Ordinary solver sensitivity/basis reuse already does this computationally; formal package reuse can preserve its proof. Charge exact reconstruction, interface adoption, version support and region failures. | Highest architectural leverage: potentially reusable mathematics, not only cached output |
| Local proof agents/verification tools encounter rational linear subgoals | Obtain Farkas/dual multipliers from any suitable solver and construct a local proof | Existing `lp`/`maximize`, ordinary `linarith` and local solver use are strong alternatives. Remote use matters only when capability/cost/access differs; networking adds failure/latency/service cost. | Useful implementation substrate, not a new remote solver protocol |
| A consumer wants an arbitrary unfamiliar specialty-library theorem | Import a compatible ordinary package or selected inert evidence | Git/Lake/Loogle already help; notation, toolchain, licensing and assumptions remain. Another LP or search adapter does not fix these. | Keep existing route; no universal migration project |

These are supported problem classes, not evidence that a particular person will
adopt our software. No existing local user project was supplied. That prevents
an uptake claim, not a mathematical analysis of the opportunity.

## Exact primal/dual witness argument

For a simple representative profile, let `A` be an `m x n` rational matrix,
`b` an m-vector and `c` an n-vector. Maximize `c^T z` subject to `A z <= b`, with
free rational variables z. A supplied rational pair x,y is sufficient if

```text
A x <= b,       y >= 0,       A^T y = c,       c^T x = y^T b.
```

For every feasible z, stationarity and nonnegative multiplication give
`c^T z = y^T A z <= y^T b = c^T x`; x is feasible, hence globally optimal.
This proof does not depend on how x,y were discovered. It is also valid over an
ordered field containing those rationals, but **the inspected upstream Prop
interface quantifies over Rat arrays**. Do not silently report a real-optimization
theorem without an actual checked interpretation/extension.

Infeasibility similarly follows from `y >= 0`, `A^T y = 0`, `y^T b < 0`:
a feasible z would imply `0 = y^T A z <= y^T b < 0`. No solver trace, claimed
solver success or remote proof environment is a premise. Ranged rows, column
bounds, offsets and minimization require their actual sign conventions; the
upstream implementation uses lower/upper multiplier splits, not this simplified
wire shape. Never reinterpret one format by intuition.

## A more substantial accumulation unit: parametric certificates

### A discovered dual survives changes to the right-hand side

Fix A,c and a y satisfying `y >= 0` and `A^T y = c`. The same argument proves

```text
for all b,z,  A z <= b  implies  c^T z <= y^T b.
```

This is a reusable bound for an entire explicitly stated family, independent of
the original b. It is not an optimality claim for every b. A new consumer can use
the bound where useful without reconstructing the original optimization search.
The discovery may expose a mathematical linear inequality useful in later proofs.
An ordinary generic duality theorem already supplies the logic; the new useful
information is the actually discovered, checked multiplier y and its application.

### A discovered active basis yields an explicit optimizer on a region

Choose n distinct rows I of A; write B for that square row submatrix. Supply a
rational matrix M and nonnegative y such that

```text
B M = identity,       A^T y = c,       y_i = 0 when i is outside I.
R = { b : A M b_I <= b }.
```

For any `b in R`, define `x(b) = M b_I`. Region membership proves feasibility;
`B M = identity` gives `B x(b) = b_I`. Therefore

```text
c^T x(b) = y^T A x(b) = y_I^T B x(b) = y_I^T b_I = y^T b.
```

The primal/dual theorem makes x(b) optimal for every b in R. This is a finite
certificate for a parametric mathematical fact, not a list of unrelated endpoint
proofs. It can be recorded as an ordinary named Lean theorem plus its constants.
The derivation does not claim that upstream currently emits this parametric
theorem automatically. It would be a separate ordinary lemma/application, not
a new trusted rule or an unproved extrapolation from examples.

R can be narrow, lower-dimensional or uninteresting for later work. Infinitely
many rescalings do not imply infinitely many new insights. Preserve a useful
original instance and test each consumer's actual region premise; outside R,
retain the dual upper bound or use another route. Do not automatically generate
every basis, classify regions globally, or count every instantiation as novelty.
The mathematical generalization is justified; its demand remains empirical.

## Actual maintained source, pinned rather than inferred from README

Primary source was read in memory only; no repository was cloned or installed.

- `leanprover/lp`: `e87b229a42a0373e6750f5af17ec409787c42832`.
- Its pinned `lp-verify`: `1131b0a11c683d4833cd735c83157a32952ad3aa`.
- Its pinned `lp-tactic`: `86634295a1fa2b45110a680215e208b16f40cd33`.
- Both verifier/tactic pin `lp-core`:
  `8b6d241bc84e54357aa6628f1b18ff795d53de7e`.

The actual `lean-toolchain` is **4.33.1**; the README badge still says 4.31.0-rc1.
Our retained project runtime is 4.34.0. Source availability is not compatibility
evidence, and this note does not select a toolchain change or a port.

The verifier's lakefile depends on LPCore only: no SoPlex C++ or tactic dependency.
`LPVerify/Bool.lean` supplies `checkOptimal`, `checkInfeasible`, `checkUnbounded`
using sparse products and rational checks. `Sound.lean` supplies the corresponding
soundness theorems. `Driver.lean` only constructs positive `Verified` cases from
those theorem conclusions after actual successful checks; failures return
`unchecked`. The optional bit budget concerns certificate coordinates only.

**The driver indexes its result by the actual supplied normalized Problem and
objective sense.** It does not prove correspondence with an arbitrary raw input,
informal optimization problem, changed index ordering or external solver's model.
Bind the local formal target to that exact problem, or supply a separately checked
normalization/reification relation. Do not trust a solver's echoed problem.

### Kernel theorem versus native checked program

A `#eval` result reporting `Verified.optimal` is not a retained kernel-checked
theorem object for later imports. Runtime evaluation erases proofs and relies on
the execution implementation; storing its printed status does not establish a
new commons warrant. A local theorem needs the actual proof of the check equation
and soundness application, or another actual proof term accepted by the kernel.
No `native_decide`/new axiom substitution is authorized.

The separate `LPTactic/LP/RatCertificate.lean` supplies
`RatCtx.assembleLeProof` and `assembleInfeasibleProof`: explicit weighted-sum proof
assembly from multipliers and the consumer's actual hypothesis expressions.
`LPTactic/Q.lean` supplies an integer/natural rational payload and checked bridges
for kernel-facing arithmetic. This is concrete existing proof-construction code
to reuse, not a reason to write another arithmetic checker. Its presence does not
prove that every imported certificate fits its interface or our resource bounds.
The producer's optimization implementation may remain completely outside the
consumer's environment. Optional native solver FFI has a separate memory/ABI trust
boundary; it is not required just to use the pure checker package.

## Costs: input-local, not constant-time

Let s be stored sparse entries, m,n the dimensions and L a bound on input/certificate
integer numerator/denominator lengths. The inspected Bool algorithm performs
`O(s+m+n)` rational operations and coordinate checks for an instance. Dense input
gives `s=mn`. Accumulated sums can increase bit lengths: exact arithmetic is not
unit cost. Conservative rational cross-products/sums have polynomial bit cost in
the explicit encoded input size; a fixed coordinate-size cap alone is not a
total time or memory limit. Parsing huge dimensions, the problem's own rationals,
duplicate entries, logs, normalization, proof construction and kernel conversion
must also be bounded. This arithmetic-operation bound is **not** a proved linear
bound for Lean's complete theorem-checking path.

For the basis theorem, naive validation of `BM=I` costs `O(n^3)` field operations;
forming AM costs `O(m n^2)` dense operations. These are one-time investments only
when exact retained results really serve later uses. Subsequent b still incurs
matrix-vector and region checking, acquisition, compatibility and proof costs.
Large rational inverses can defeat the intended saving. No claim of superiority
over modern exact/warm-start LP algorithms follows from the simple formulas.

The architectural removal is concrete: the recipient need not install/run the
original solver or replay its optimization trajectory. The solver may be much
more expensive than verification for an actual workload; this note proves no
lower bound on all solvers. Existing ordinary witness exchange gets identical
credit. Charge original solving, failed cases, rational reconstruction, checker
adoption, transport, curation, operator support and version maintenance. A service
does not remove producer cost; it can concentrate optional specialist capability.

## Existing API seam and smallest next decision

Current `ordinary_native_package/owner.py` offers ordinary `contribute` and
owner-free `produce-baseline`; the producer exports already compiled selected
Lean declarations. Thus a *locally reconstructed finished theorem* can use the
existing selected-output path, subject to exact version/fragment compatibility.
It does not require another mathematical acceptance mode, global index or original
solver-proof identity. Existing ordinary Git/files can carry data and packages.

What is **not implemented or qualified** is a supported inert LP certificate
reader tied to an exact local formal problem and a resulting kernel-proof API.
The existing peer routes carry ordinary proof-evidence units, not arbitrary LP
data. Do not fake those IDs. Upstream already separates solver/backend/checker;
first inspect/reuse that boundary before inventing a new RPC or data standard.
The preferred first artifact is a retained file usable offline, not a mandatory
live service or a port of the entire solver stack. A source-only integration
decision should settle whether an existing backend/proof-assembly entry can accept
selected fixed evidence without invoking a solver, and which exact proof it returns.

Retain the exact problem, certificate and checker/profile relation through
replaceable ordinary storage. A remote service disappearing must not erase
previously acquired evidence. Retain parametric lemmas/basis certificates when
they are useful ordinary mathematics; merely keeping an API endpoint is not
knowledge accumulation. Acquired exact instances are warranted computational
knowledge, not automatically novel mathematical abstractions.

**Recommended next change:** adopt this optional consumer-native certificate
branch and select only its source-level file-to-proof integration seam. Do not
install 4.33.1, port upstream, manufacture a small LP benchmark or add transport
until that seam is cheaper than ordinary use and preserves the target/proof
boundary. If upstream already exposes it adequately, use it as a dependency and
write no competing mechanism. This recommendation moves the architecture by
changing where specialized work lives; it does not claim another final v5 pass.

## Root closure of the optional dependency follow-up

The exact API names above were corrected against the independent author/reviewer
inspection. The four pinned packages are recorded in the unused backend's
DEPENDENCIES.json. A complete recursive source/build footprint was not established;
do not infer it from those four names or from importing only the Contract module.
Root closed the optional footprint assignment without further lookups because
dependency compatibility is not yet the selected growth bottleneck.

The adapter's completed source review is preserved in GROWTH-CLAIMS-CHALLENGE.
No installation, port, build, test or runtime support follows. Exact-response
replay is narrower than parametric method reuse. Root's subsequent design and
fresh GROWTH-METHOD-CHALLENGE select the ordinary method/application/return
boundary as the next justification, not another backend campaign. Existing
ordinary APIs may already supply it; identify an actual obstruction before code.

## Sources and scope

- Prior notes: GROWTH-DECISION, BRIDGE-INVESTMENT, native-library/
  GROWTH-FIRST-ARCHITECTURE-DECISION, GROWTH-COMPARATOR-CHALLENGE,
  DEMAND-DRIVEN-GROWTH, GROWTH-NEXT-PAYOFF and GROWTH-DEFAULT-ARCHITECTURE-AUDIT.
- Prior witness principle: architecture-reaudit/ARCHITECTURE-REAUDIT,
  especially “The most promising non-cryptographic improvement”.
- [Pinned LP package and dependency map](https://github.com/leanprover/lp/tree/e87b229a42a0373e6750f5af17ec409787c42832).
- [Verifier Driver](https://github.com/leanprover/lp-verify/blob/1131b0a11c683d4833cd735c83157a32952ad3aa/LPVerify/Driver.lean),
  [Bool](https://github.com/leanprover/lp-verify/blob/1131b0a11c683d4833cd735c83157a32952ad3aa/LPVerify/Bool.lean),
  [Sound](https://github.com/leanprover/lp-verify/blob/1131b0a11c683d4833cd735c83157a32952ad3aa/LPVerify/Sound.lean),
  [Prop](https://github.com/leanprover/lp-verify/blob/1131b0a11c683d4833cd735c83157a32952ad3aa/LPVerify/Prop.lean),
  [Budget](https://github.com/leanprover/lp-verify/blob/1131b0a11c683d4833cd735c83157a32952ad3aa/LPVerify/Budget.lean).
- [Rat proof assembly](https://github.com/leanprover/lp-tactic/blob/86634295a1fa2b45110a680215e208b16f40cd33/LPTactic/LP/RatCertificate.lean),
  [kernel-facing rational payload](https://github.com/leanprover/lp-tactic/blob/86634295a1fa2b45110a680215e208b16f40cd33/LPTactic/Q.lean).

No upstream benchmarks or README performance claims were adopted. This source
screen is not an independent audit of the complete upstream dependency closure,
does not solve arbitrary cold theorem ancestry, and does not prove actual uptake.

## Finite follow-up: the exact certificate-to-kernel-proof seam

Root requested this source-only continuation. **The proof assembly already exists;
the narrow missing convenience is bounded retained-file ingestion/dispatch.**
No new checker, arithmetic proof engine or LP wire protocol is needed.

### Direct existing entry, with no solver call

At the pinned lp-tactic revision, `RatCertificate.lean` is a `public meta section`.
The accessible name is `LP.Tactic.LP.Internal.RatCtx.assembleLeProof`, with inputs

```text
RatCtx, rows : Array Row, strict : Bool, objLin : LinExpr,
mults : Array Rat, vars : Array FVarId, lhs rhs : Expr,
atoms : AtomTable := {}                 -> MetaM Expr.
```

Locally approved Lean metaprogramming can call it after `mkRatCtx`. Despite its
`Internal` namespace, it is not private in these sources; that is an accessible
implementation API, **not a promise of upstream API stability**.
It neither invokes a backend nor runs a solver. The provided multipliers are
ordinary rational data. `Row` is not wire data: it includes `MetaM Expr` thunks
for actual local hypothesis terms/proofs and must be constructed locally.
`Parse.lean` exposes `parseAtomic?`, `collectHypProof`/`collectHyps` and `ParseState`
for that job. Producer-supplied Lean Exprs or executable row thunks are unnecessary.

For rows `e_i <= 0`, it forms their weighted sum s, recomputes the numerical
residual, and constructs a proof of `rhs - lhs + s = c`. With nonnegative
multipliers and `c >= 0`, `Types.direct_le_close` returns `lhs <= rhs`.
With `strict=true` it returns `lhs < rhs`, requiring either positive c or a
strict contributing row and nonnegative c. `assembleInfeasibleProof` separately
constructs a contradiction and eliminates False into the explicit goalType.
It does **not** return an unconditional optimization theorem about a JSON problem.
The conclusion concerns those actual local expressions/hypotheses. Equality
requires two directions plus antisymmetry, as the existing atomic frontend does.

The result is a proposed `Expr`, not an acceptance event. A caller must bind it
to the actual selected goal, complete all metavariables and obtain genuine final
kernel checking under its admitted environment/axiom policy. Numeric residual
checks aid early refusal but do not replace that proof check. A misparsed or
incorrect coefficient proposal cannot establish a false endpoint if the final
term/target is actually checked under those premises.

### Arithmetic checks are proof-producing, not native-decide attestations

`CarrierCertificate.buildWeightedSumDecide` obtains sign proofs with
`Lean.Meta.mkDecideProof`; `proveCertificateIdentity` normalizes the actual
expression and returns a chain of arithmetic lemma applications.
`Certificate.mkEqReflProof` constructs `Eq.refl` for the integer cross-product
side of `ratlit_add`/`ratlit_mul`/`ratlit_neg`; the opposite side must be convertible
when the resulting proof is checked. A numeric native result alone cannot supply
that equality. Pinned Lean 4.33.1 resolves to commit
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`; its `Lean/Meta/AppBuilder.lean`
`mkDecideProof` constructs `of_decide_eq_true` applied to a reflexivity term with
expected type `decide p = true`. This is not `native_decide` or a new axiom.

Proof construction can be substantial: `Certificate.lean` itself discusses
quadratically many operator/literal proof sites, and the final kernel still
checks generated terms and integer computation. The earlier `O(s+m+n)` count
belongs only to the Boolean verifier, not this complete proof-construction path.
No performance ratio or large-instance feasibility is established here.

### Prefer the existing backend interface over reparsing the entire tactic

`LP.registerStaticBackend` (in the Registry module) accepts an approved callback

```text
{m n : Nat} -> Options -> Problem m n ->
  IO (Except SolveError (Solution m n)).
```

Nothing requires that callback to solve a problem. It can return selected inert
evidence read from a retained artifact. The normal frontend then preserves its
local parse, uses the supplied dual and constructs its proof. Pin the backend
explicitly (`lp.backend` or the per-call backend selection); do not use default
fallback which probes other installed backends. Strict-goal fallback/equality
can request additional solves: a file callback must have a finite explicitly
selected request map or refuse, never silently launch another solver/service.

There is also an existing reusable JSON decoder. At
`lp-backend-soplex-json` commit `ce953f3b926815ebda5d65f88f1a06e9578abdc8`,
`LP.Backend.SoplexJSON.decodeResponse m n text` returns
`Except String (Decoded m n)`, with `.solution` and `.wireError` branches;
the former contains a dimension-checked `Solution`.
`LP.Backend.SoplexJSON.encodeRequest opts p` serializes the actual request. Its lakefile
pins exactly the same LPCore/LPTactic revisions above. Importing only `Contract`
does not require using the executable-dispatch `Backend` module.

The inspected maintained `Backend.solveExactWith` spawns a binary with JSON stdio
and calls `IO.Process.output`; it is **not a solver-free retained-file command**
and does not enforce our aggregate output/time/memory bounds. The decoder itself
calls `Json.parse` on an already complete String; dimension checks are not raw
input-size limits. The inspected source therefore supplies parsing/proof APIs,
but not the whole bounded file-to-local-proof operation.

The smallest missing adapter, if later selected, is one owner-approved local
file-backed callback: bounded immutable bytes, exact selected request/problem
association, bounded dimensions/rational strings/results and call count, existing
decoder, explicit backend, then existing actual proof construction/checking.
Its input never chooses paths, executable names, imports or solver fallbacks.
A direct multiplier entry is smaller for a deliberately narrow local hypothesis
profile, but would depend more tightly on internal Row/parser details. Both must
check multiplier count against the local row count; direct helpers use array `!`
accesses and are not a hardened untrusted-input boundary by themselves.

This is source feasibility on **4.33.1**, not a supported installed operation on
our **4.34.0**. The version difference does not refute the architecture or public
source seam; it does prohibit claiming compatible binaries, tested source reuse
or plug-and-play product integration. Root must separately choose pinning,
compatibility work or deferral. No port/build was performed. The bolder parametric
basis theorem also remains a separate mathematical application, not something
this callback automatically generalizes or proves.

Additional exact sources: [Registry](https://github.com/leanprover/lp-tactic/blob/86634295a1fa2b45110a680215e208b16f40cd33/LPTactic/Registry.lean),
[atomic frontend](https://github.com/leanprover/lp-tactic/blob/86634295a1fa2b45110a680215e208b16f40cd33/LPTactic/LP/Atomic.lean),
[certificate helpers](https://github.com/leanprover/lp-tactic/blob/86634295a1fa2b45110a680215e208b16f40cd33/LPTactic/LP/Certificate.lean),
[shared proof builder](https://github.com/leanprover/lp-tactic/blob/86634295a1fa2b45110a680215e208b16f40cd33/LPTactic/LP/CarrierCertificate.lean),
[JSON contract](https://github.com/leanprover/lp-backend-soplex-json/blob/ce953f3b926815ebda5d65f88f1a06e9578abdc8/LPBackendSoplexJSON/Contract.lean),
[subprocess backend](https://github.com/leanprover/lp-backend-soplex-json/blob/ce953f3b926815ebda5d65f88f1a06e9578abdc8/LPBackendSoplexJSON/Backend.lean),
[Lean proof builder](https://github.com/leanprover/lean4/blob/819816b2e0a3bf405af45ae5c7af2491d8f5bee6/src/Lean/Meta/AppBuilder.lean).
