# General Lean checking traces: decision and bounded next contract

2026-09-28 UTC, v3_index. Source analysis only: no build, prover call, installation,
runtime test or product change. Canonical workspace guard passed. This track is
disjoint from v3_efficiency's full native-kernel guest-closure investigation.
Root owns the separate pinned zkPi exporter/relation inspection.

## Decision

**A checking trace is a serious alternative to porting the entire Lean runtime,
but there is not yet a qualified Lean4.34 trace checker to put on our acceptance
path.** Its advantage would be to move conversion search, caches, elaboration
and proof construction outside the cryptographically certified program. A small
validator checks a supplied derivation instead of discovering that derivation.
This does not remove the dependent-type rules, environment invariant or conversion
side conditions. It moves those obligations into an explicit checker.

Do not implement another bounded equation calculus and label that progress on
general Lean checking. The next candidate must consume **actual ordinary Lean
Expr declarations**, not a new theorem recipe. The bounded contract below checks
new theorem bodies and safe ordinary definitions over a fixed already-qualified
environment. That is a reusable native-kernel subproblem, not all declaration
installation. New inductive-group generation is explicitly a subsequent gate;
using existing dependent inductives/recursors/projections is not excluded.

**Current selection status: NO-GO for changing product acceptance or promising
this as completed v3 scalability. Conditional GO for preparing the nonadmitting
general-judgment discriminator below, after the exact candidate rule map exists.**
There is no need to require every component's full machine-checked correctness
before engineering starts. The current blocker is missing executable coverage,
binding and a complete reviewed rule argument—not merely a desire for a perfect
formal proof. Keep the current native product and experimental EQ-DAG1 distinct.

## Source evidence that determines the scope

Pinned native kernel: Lean commit
`293d5d0c0c3f3dded4688b3ccd6a33939ac5102b` (selected4.34 lineage).
Read the actual `src/kernel/type_checker.cpp` and `environment.cpp`, not only
the Lean API declarations. These particular boundaries matter:

| Native behavior | Trace obligation |
|---|---|
| `infer_type` invokes `infer_type_core(..., true)`; `check` invokes false with declared universe parameters (type_checker:323–371) | A recorded inferred type or successful fast path alone is not a typing certificate. Every skipped well-formedness premise must already have a valid trace justification. |
| Constants instantiate an ordered universe list, check arity, scoped levels and safe/partial status (101–122) | Bind the entire constant record and substitution; forbid unbound level parameters, unsafe/partial premises and caller-selected replacement definitions. |
| Lambda/Pi/let check domains/values before extending local contexts; Pi uses `imax` (125–229) | Explicit well-formed binder contexts and capture-avoiding substitution, not an untyped expression rewrite. |
| Projection checks structure identity, index fitting unsigned32, one constructor, parameters/indices and Prop restrictions (237–291); reduction checks constructor belongs to that structure (420–453) | A projection index alone or an untyped constructor-field lookup is insufficient. Exact generated group records and dependent field instantiation are required. |
| Conversion uses beta/zeta, delta, recursor/quotient reduction, universe equality, proof irrelevance, function/structure eta, literals and unit-like structures (393–407,468–590,785–938,1159–1245) | Account for every used successful rule and side condition. No opaque `native_defeq_succeeded` leaf. |
| Theorem admission checks unique name/universe parameters, closed type/body, type formation, Prop and body/type conversion (environment:127–132,192–208) | A body-typing trace alone is not the whole declaration-admission relation. |

Native recursion/fuel/numeral bounds are also part of the selected resource
profile. They need not become mathematical axioms. Unsupported or oversized
traces must refuse cleanly, not wrap values or reinterpret failed computation.
Heuristic search order, negative failed branches and native pointer-cache layout
need not be replicated by a sound positive derivation validator.

Prior Lean4Lean assessment is reused, not restarted. At inspected commit
`8223d223ed98661882e95d9d6a7126df7097cd76`, its toolchain is4.33.0-rc2, it expressly
shares implementation lineage, and it documents level/projection/primitive and
inductive differences. The earlier foundation audit records unfinished
inductive/weakening proofs and explicit runtime correspondence assumptions.
This inspection additionally found `Verify/TypeChecker/InferType.lean:388–391`
ends `inferProj.WF` with `sorry`. That is a missing proof at an exact relevant
boundary, not evidence that its executable is unsound.

Its `Theory/Typing/Basic.lean:18–56` is a useful typed-equality skeleton:
application, lambda/Pi, conversion, beta, eta and typed proof irrelevance are
explicit. However, `extra` accepts entries of `env.defeqs`; the environment
invariant must justify those entries. Putting attacker-selected equations into
an authenticated map does not establish that invariant. Do not claim this
metatheory file is already an independently verified4.34 executable validator.

Root's newly inspected zkPi commit
`ff136f79ca5843cafed61bc1222a5dd85d7a8646` contains actual dependent typing/evaluation
trace rules and term/context/lift tables. This is relevant candidate code, not
the old claim that only an equational recipe is available. Its exporter,
semantics, compatibility and recursive composition remain root's separate
investigation; no drop-in suitability follows here.

## Exact relation a trace would certify

Fix foundation F, checker/encoding profile P and a compatible selected environment
E. Let U be the **ordered universe-parameter context** and Δ a well-formed local
context of types and optional let values. A witness is a finite acyclic DAG with
typed nodes, for example:

    Ty(F,P,E,U,Δ,e,T)
    Conv(F,P,E,U,Δ,e,e',T)
    LevelEq(U,l,l')
    Lookup(E,symbol,exact-record)

These are specification shapes, not existing software. Node keys bind all the
displayed context, exact expression references and the applicable reduction/
opacity policy. Reusing a cached equality across two binder contexts, universe
instances, definition versions or opacity modes is forbidden. Contexts and
expressions may be shared by hashes only after canonical decoding and exact
reference checks; cycles and forward references without a justified DAG order
must refuse. Metadata erased by the existing canonical normalization has an
explicit semantics-preserving projection, not an undocumented change of term.

Each conversion witness must be **typed**. For example, proof irrelevance requires
checked `p : Prop`, `h : p` and `h' : p`; it cannot say “both nodes are proofs”
from a peer flag. Dependent application must verify the argument's type against
the Pi domain and instantiate the exact codomain without capture. Pi formation
uses the correct impredicative `imax`, not an ordinary maximum. A beta/zeta
substitution trace checks every required lift/index operation. Structural
equality/hash equality does not supply missing typing or context well-formedness.

The desired mathematical implication is

    WF_F(E) ∧ WF(E,U,Δ) ∧ TraceCheck(P,E,U,Δ,e,T,τ)=accept
      ⇒ E;U;Δ ⊢_F e : T.

For a declaration, add name uniqueness, exact declaration category, universe
scope, safe closed type/body and the theorem's Prop condition. The final checked
root is the exact requested declaration, not some well-typed node in the DAG.

There are three separate correspondence obligations:

1. Canonical bytes → actual native Expr/Level/constant interpretation. Include
   names, exact indices, literal expansion and generated recursor/projection
   metadata; reject metavariables and dangling local references.
2. Accepted trace rules → legitimate typing/conversion in the selected Lean
   foundation. A reviewed rule-by-rule simulation is the initial engineering
   requirement; a formal inductive proof is the stronger intended artifact.
3. Validator implementation/cryptographic program → that rule specification.
   A native host check is an independent comparator, not a trusted witness bit
   that permits skipping either1 or2 inside the certified program.

One-way soundness matters first. A sound trace profile can refuse native proofs
whose conversion strategy it cannot reproduce. It must report the lost coverage
and cannot call that refusal complete Lean support. Agreement on a few positive
examples is neither soundness proof nor broad completeness evidence.

## Certified environment and no hidden ancestry replay

An external constant lookup has three allowed origins: exact adopted base F,
an already valid certified interface, or an earlier checked declaration in this
new finite extension. Bind category, ordered universes, type, semantic references,
safety and computation policy. Definitions additionally bind exact bodies;
inductives bind their checked atomic groups, constructors, recursors and rules.
A bare Merkle membership proof is only byte authentication, not derivability.

Sealed theorem parents contribute exact typed opaque premises. Their certificates
must establish compatible validity and type support under F/P, and their shared
definition identities must agree. The child checking relation recursively
verifies/discharges those certificates with well-founded ranks or a separately
justified recursion rule. Environment realization then justifies substituting
parent derivations. A trace of `F + h:T ⊢ p:U` alone never establishes `F ⊢ U`.

The support walk ends at an authenticated sealed theorem interface; it must not
flatten that theorem's proof trace, recursively recheck its historical environment,
or require all ancestor certificates as an outer attachment. The new proof can
still require a large **current** type/definition computation. Authenticate and
charge that selected support rather than call it free. Missing definition bodies
or unsupported proof-dependent conversion must refuse/need-data; never silently
hydrate the entire ancestral proof history or substitute an unproved rule.

## Bounded next implementation contract: GENERAL-JUDGMENT-0

This is a proposed **nonadmitting discriminator**, not authorization to run it.
Use one separately selected source successor and one existing general-Expr
candidate after root's rule/export gap map; do not start a third checker merely
because the other two have unresolved gaps.

**Input/output.** Input is an exact retained native declaration packet and its
selected compatible environment, in the project's existing canonical representation.
Output is either an explicit unsupported/refused reason, or a typed trace plus
a deterministic revalidation report bound to the original packet/profile.
No node database write, product `accepted` flag or cryptographic certificate is
produced by this first contract. The untrusted producer may use native checking
or heuristics to find a trace; the validator may not call an unchecked native
oracle or accept a supplied success receipt.

**Small consequential boundary.** Check an arbitrary safe theorem/ordinary
definition body over an already qualified environment. Support actual Sort,
Const, bound variables, application, lambda, Pi, let, projection and retained
literal/metadata interpretation, with general universe parameters—not fixed
term depth, symbol counts, theorem names or CONGR2/TRANS plans. Existing group
records must support their real eliminations. New mutual/nested inductive
admission remains an explicit missing declaration-extension obligation; it is
not approximated by user-supplied recursor axioms.

**Reuse existing evidence inputs.** Do not repeat old source discovery/proving.
Select retained ordinary polymorphic/dependent proof packets and their exact
types/bodies: the Fin three-cast successor is a useful required case because it
already involves dependent Fin indices, proof-bearing definitions and genuine
library use. Add retained function/structure/recursor/let/literal cases needed
to exercise the claimed rule families; select their exact identities before
execution, without rewriting theorems to avoid unsupported constructors. The
choice is an evaluation instrument, never a network task list.

**Changed-boundary refusals.** Fixed mutations must cover a free/loose variable,
wrong universe order/arity, incorrect argument domain, capture-invalid
substitution, mismatched dependent result, wrong structure name/oversized
projection index, fabricated proof-irrelevance type, unauthorized delta body,
unjustified recursor rule, changed parent/context identity and a cyclic/replayed
trace node. Native reference outcome and trace outcome are recorded separately;
a parser crash or resource failure is not counted as semantic refusal.

**Pass/stop.** Every claimed-success root must match the unchanged native
declaration and have no oracle/opaque success node. Record all rule families
used and their actual correspondence arguments. If a required existing-library
case needs an unmodeled rule, report **INCOMPLETE_GENERAL_JUDGMENT**, preserve
the evidence and stop; do not replace it with a small equation example. A pass
only qualifies this deterministic typed-trace boundary. Sealed-parent recursive
certification, new group admission, production security and product deployment
remain distinct gates.

**Cost/accounting.** Measure producer time, complete trace construction/bytes,
validator time/peak memory, selected definition-support reads and refused work.
No speedup is presumed: normalization and trace generation can dwarf proof size
and can grow exponentially. A future succinct wrapper reduces receiver work
only if its *actual proved relation* runs this validator and completes parent
discharge; a plain trace is generally linear in the supplied checking evidence.
The producer must also operate using immediate certified interfaces, not a
hidden full-history reconstruction. This contract alone establishes no useful
knowledge-growth advantage.

## Subsequent candidate selection advice: prefer existing general code

Root's [general-checker decision](GENERAL-CHECKER-DECISION.md) identifies
`ammkrn/nanoda_lib` at `3a2407216ee84a75f9e1aead6803d0578be06ae7`, a recent
Rust checker with a substantially smaller apparent runtime closure. Root owns
its exact parser/API/feature inspection and efficiency owns guest feasibility;
this note does not duplicate or assert the outcomes of those inspections.

**Prefer one bounded native differential qualification of that existing general
checker and a SEALED_PROP extension adapter over implementing a new partial
typechecker.** A matching general parser/checker would exercise actual ordinary
proofs sooner and expose the real import/definition boundary. A new custom trace
checker should remain contingency, not a simultaneous third implementation.
The positive trace architecture above still specifies useful later acceleration
and explains which semantics a guest/checker cannot silently omit.

Historical nanoda reports justify targeted controls, not automatic rejection of
the new pin: the prior source audit attributes a bogus-proof acceptance to nanoda
in PR14807. Check the **current** genuine-sort requirement in proposition
recognition and its use in structure/recursor reduction; also normalized Prop
universes, the PR14806 classification/cache invariant, projection identity/u32
width and nested-group generated-output checks. Version recency or a broad
feature list cannot resolve those questions. A native disagreement is a held
case requiring classification, never a majority vote.

The smallest consequential positive endpoint remains: a retained actual
polymorphic dependent theorem checks under exact selected bindings, then a new
ordinary Lean successor uses certified sealed theorem interfaces without old
proof bodies. The adapter must explicitly bind allowed base/derived-axiom origins,
types/universes, shared definition identities and the final output; it cannot
authorize whatever axioms the imported JSON happens to contain. Different checker
acceptance is engineering evidence, not yet a recursive proof of correct execution
or a completed cryptographic discharge of those premises. This recommendation
changes no product acceptance and requires no full formalization of every checker
implementation detail as a precondition to a bounded diagnostic build.

## Evidence links

- [Pinned native typing/conversion implementation](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/type_checker.cpp).
- [Pinned native declaration checks](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/environment.cpp).
- [Prior Lean4Lean foundation cross-audit](../../../notes/audits/CP-001E-foundation-cross-audit.md).
- [Pinned typed equality rules](https://github.com/digama0/lean4lean/blob/8223d223ed98661882e95d9d6a7126df7097cd76/Lean4Lean/Theory/Typing/Basic.lean).
- [Pinned projection verification gap](https://github.com/digama0/lean4lean/blob/8223d223ed98661882e95d9d6a7126df7097cd76/Lean4Lean/Verify/TypeChecker/InferType.lean#L388).
- [Pinned deliberate divergences](https://github.com/digama0/lean4lean/blob/8223d223ed98661882e95d9d6a7126df7097cd76/divergences.md).
- [Retained real-library proof packet evidence](../../../experiments/lean-library-interop/RESULTS.md).
- [Selected environment/interface design](SCALE-DESIGN.md) and [native interface obligations](SCALE-LEAN-INTERFACES.md).

Targeted independent challenge from v3_growth required exact context/mode binding,
no hidden ancestor-WF traversal and full trace-generation cost; all are explicit
above. This note does not replace that agent's PCD/security assessment.
