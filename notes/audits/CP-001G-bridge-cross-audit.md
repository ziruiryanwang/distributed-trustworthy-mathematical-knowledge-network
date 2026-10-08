# CP-001G independent audit: checked interface bridges

Date: 2026-09-20. Auditor: `commons_reciprocity`, independently of the BRIDGE1 author. Scope: paper specification and read-only pinned-source inspection. No Lean execution, implementation, extraction, native replay, test, exploit or benchmark was performed. CP-001F remains frozen.

## Audited artifact and verdict

Reviewed [CP-001G interface bridges and applications](../analyses/CP-001G-interface-bridges-and-applications.md), SHA-256:

`6CBD6FFBF68C9FDEB5EDC93C4EA84A978B944E03A9F51A00FC5E11552C31DC04`.

Within this bounded audit, no contradiction was found in the stated conditional native-typing argument or the source-backed injective/surjective examples. BRIDGE1 distinguishes the actual resulting proposition from the requested proposition, recomputes actual support, binds local contexts, and explicitly declines completeness and optimality claims for bounded search. These are substantive safeguards, not evidence that an implementation has satisfied them.

One nonblocking specification clarification was recommended below: make extension by unresolved earlier arguments an explicit checked-context transition before a conditional map can become usable. It was subsequently repaired and checked as recorded in the closure section. The existing exact native-check and final conditional-result requirements already prevented interpreting such arguments as discharged premises.

This verdict does not cover broad practical library import, proof-instance realization, frontend metadata reconstruction, network retrieval, checker correctness, or measured efficiency. BRIDGE1 correctly depends on their separate contracts.

## Exact application and property transport

For a fixed qualified foundation and compatible checked context Gamma, assume:

\[
\Gamma\vdash b:B,\qquad
\Gamma\vdash f:B\to A,\qquad
\Gamma\vdash \ell:\Pi a:A, P(a).
\]

Function elimination establishes precisely `ell (f b) : P(f b)`. It does not establish an arbitrary desired `Q(b)`. BRIDGE1 requires either native conversion between these types or an independently checked transport term with the necessary instantiated arguments. That requirement is sufficient for the displayed application argument relative to the adopted native typing rules.

The note also correctly restricts a generic graph edge to a final nondependent subject argument after earlier instantiation. A term of type `Pi b : B, A(b)` cannot become a fixed endpoint-type edge merely because its printed codomain resembles A. Explicit dependent application remains admitted mathematics and must retain the resulting instantiated type.

Propositions as graph-vertex types do not remove premise obligations. Given only `f : P -> Q`, the usable term `f p : Q` still needs `p : P`. An unresolved proof of P can support a conditional theorem, not an unconditional Q.

## Checked-context transition for residual parameters

**Clarification C1.** The candidate-discovery paragraph allows earlier arguments to be instantiated or reported as residual, while `BridgeContext` binds the full exact telescope. State explicitly that a residual parameter introduced as a local variable creates an extended checked context, a fresh context identity, and correspondingly scoped candidates/results. It is not a checked inhabitant in the old context.

For example, a declaration `g : Pi h : H, B -> A` and a term `b : B` in Gamma do not give a usable `B -> A` edge in Gamma until some `h0 : H` has been supplied. They do give the conditional edge `g h : B -> A` in the well-formed extension `Gamma, h : H`, provided A and B are interpreted in that extension and all actual argument checks succeed. The produced result remains conditional on h, or is closed by explicit lambda abstraction to its actual Pi type. If later argument/result types depend on h, they must use that actual local variable in the same telescope.

BRIDGE1 already says that free-variable indexes are not identified across contexts, actual arguments must be checked, and unresolved premises cannot yield unconditional success. C1 clarifies how its candidate state machine satisfies those existing requirements. It is not a newly discovered permission to add axioms, nor a reason to forbid conditional results.

## Two counterexamples for missing transport hypotheses

### Multiplication preservation without injectivity is insufficient

Take B to be the two-element set `{0,1}` and define `x star_B y = 1 - x`. Then:

\[
(0\star_B 0)\star_B 0=0,
\qquad
0\star_B(0\star_B 0)=1.
\]

Thus B is not associative. Let A be a singleton with its unique binary operation, which is associative. The unique function `f : B -> A` preserves multiplication because all A values are equal. It is not injective. Therefore an associative target and multiplication-preserving map alone do not reflect associativity to B.

### Injectivity without multiplication preservation is insufficient

Keep the same nonassociative operation on B. Let A have the same two-element carrier but operation `x star_A y = x`, which is associative. The identity-on-carriers map `f : B -> A` is injective. It is not multiplication-preserving: at x=0, `f(0 star_B y)=1`, but `f(0) star_A f(y)=0`. Thus injectivity alone does not transfer the algebraic law either.

These are paper counterexamples to omitted mathematical hypotheses. They are not executed attacks on a verifier. They substantiate the distinction BRIDGE1 makes between a well-typed map, a property-preserving map, and the particular direction of property transfer.

## Independent pinned-source check

Read `Mathlib/Algebra/Group/InjSurj.lean` at commit `5ed2965256430c3649e86755f9576b54eca72435`, directly from the pinned raw source on 2026-09-20.

At lines 45–53, the surrounding context provides `[Mul M1]`; the construction requires `[Semigroup M2]`, `f : M1 -> M2`, `hf : Injective f`, and `mul : forall x y, f (x * y) = f x * f y`. Its result is `Semigroup M1`. The implementation of associativity explicitly uses injectivity and the repeated multiplication-preservation/target-associativity equalities. This supports BRIDGE1's injective transfer claim and its direction.

At lines 309–318, the surrounding context instead provides `[Mul M2]`; the construction requires `[Semigroup M1]`, `f : M1 -> M2`, `hf : Surjective f`, and the same-direction preservation equation. Its result is `Semigroup M2`. The body uses surjectivity on the three arguments and the source associativity law. This supports BRIDGE1's opposite-direction surjective transfer claim.

Both are `protected abbrev` declarations producing ordinary algebraic structures. This source fact does not by itself prove that their complete elaborated terms, generated members, local metadata or dependency closures are supported by the proposed exporter. BRIDGE1 states that limitation explicitly.

## Search identity, pruning and cost

The sample depth/branch limits permit a full rooted tree with

\[
1+16+16^2+16^3=4369
\]

vertices, including the initial state. Consequently a 256-retained-state envelope cannot represent the full such tree simultaneously. The note does not equate its retained-state cap with exhaustive enumeration. Its independent finite work/time/candidate allocation is essential: a bound on live retained states alone would not bound total expansions in a search that repeatedly evicts and inserts states.

The four-alternative cap per exact type/context bucket is not a sound quotient of mathematical values. For a simple example, take five checked maps `f_i : Unit -> Nat` with `f_i () = i`, for i in `{0,1,2,3,4}`, and a selected lemma `ell : Pi n : Nat, n = n`. Applying ell to the five resulting states yields proofs whose actual types are respectively `i = i`. For desired result type `4 = 4`, retaining only the first four map results can discard the immediate route whose resulting type matches the request by conversion. The four other actual equality types do not become `4 = 4` merely because all input values inhabit Nat.

This example does not assert that the target theorem is otherwise hard or unprovable; an investigator can of course supply another proof. It establishes the relevant algorithmic point: endpoint-type bucketing can remove a successful selected application path, so the finite procedure cannot infer nonexistence of an application from its failure. BRIDGE1 explicitly acknowledges that limitation.

Term/context/support-sensitive state identity is appropriate. Different paths can change data values, assumptions, available evidence and warm/cold costs. No endpoint-name-only cache may substitute for those distinctions. BRIDGE1 also correctly allows a locally expensive one-edge path and a cheaper two-edge path, without claiming that its heuristic always chooses the optimal one.

## Evidence footprint and lifecycle

The typing argument requires one compatible actual checked environment. A syntactic map graph over independently valid but incompatible branches is insufficient. BRIDGE1 explicitly defers exact compatibility to the selected evidence backend and does not authorize arbitrary union of witness maps.

Its requirement to compute the final selected term/closure footprint includes the maps and transport proof, not merely the original theorem. In the proposed proof-instance setting, actual representatives reached through types, definitions and groups remain part of that backend's obligations. A stable semantic identifier does not certify unchanged representative support; the backend must expose the actual compatibility and cache keys used by BRIDGE1.

The note separates historical/native checking, current usable closure and guards, public contribution, and durable custody. Thus an old cached path may remain inert discovery data after its selected evidence becomes unavailable or inadmissible; it cannot remain a current checked edge just because its endpoint type is unchanged. Cancelling a search also does not release another owner's live evidence obligation.

These safeguards keep local exploration separate from network duties. Neither successful application nor publishing an adapter silently promises a standing global conversion service.

## Distinction from presentation reconstruction

BRIDGE1 maps genuinely different mathematical types or interfaces, with checked property transport where necessary. CLIENT1 instead reconstructs owner-local frontend names and metadata with exact correspondence to already selected semantic declarations. A source name, inferred class alias, or restored notation is not a BRIDGE1 map and does not identify distinct GroupIDs. Conversely, a valid mathematical adapter does not automatically reconstruct the frontend's hard-coded names or extension metadata.

Maintaining that distinction is necessary for the nominal-record example: checked constructor/projection applications can transport the needed operations and laws without declaring the independently reconstructed records identical. Native projection conversion may suffice for a particular lemma; otherwise the specific preservation/transport proof is still required.

## Remaining qualification boundary

The audit supports BRIDGE1 as a bounded local construction specification, conditional on its exact native/evidence backend. It does not establish:

- that every pair of useful representations admits an affordable bridge;
- that finite search finds a bridge when one exists;
- that a map into a shared hub transports every desired property;
- that all practical mathlib constructions survive the selected producer/import pipeline;
- that current chosen numerical budgets provide acceptable real-world performance;
- that a checked result is novel, important, or exponentially productive.

No such guarantee should be added by summarizing the successful paper composition argument. The useful delivered condition is narrower: every reported successful application is independently checked at its stated actual type and, when claimed, at its separately checked requested type, under its actual current context/support.

## Clarification closure

Reread the amended residual-parameter passage on 2026-09-20 in BRIDGE1 hash:

`E073B76A8DFAB8F4E4C6DA70738137346BA3C6754244369420E6B1CC4F8B69B4`.

It now explicitly requires extension of the checked telescope in dependent order, a new context identity, and use of the conditional map only in that extended context. Returning to Gamma requires explicit abstraction or actual checked arguments. The text also excludes unresolved metavariables and residual-list metadata as native assumption declarations. C1 is closed for this inspected revision. No additional finding was identified in this focused reread.

## Sources

- [Audited BRIDGE1 note](../analyses/CP-001G-interface-bridges-and-applications.md), hash-bound above.
- [Pinned injective transfer source](https://github.com/leanprover-community/mathlib4/blob/5ed2965256430c3649e86755f9576b54eca72435/Mathlib/Algebra/Group/InjSurj.lean#L45).
- [Pinned surjective transfer source](https://github.com/leanprover-community/mathlib4/blob/5ed2965256430c3649e86755f9576b54eca72435/Mathlib/Algebra/Group/InjSurj.lean#L309).
- [CLIENT1 library/presentation analysis](../analyses/CP-001G-library-interoperability.md), for the separate exact-correspondence boundary.
