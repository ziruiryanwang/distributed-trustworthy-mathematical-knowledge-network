# CP-001H independent audit: proof-sensitive computation

Date: 2026-09-20. Scope: independent source/control-flow and paper-argument review of [REDUCE1](../analyses/CP-001H-proof-computation-and-reconstruction.md). No Lean execution, build, native replay, artifact extraction, implementation or benchmark was performed. Frozen G and earlier artifacts are unchanged.

Initial reviewed draft SHA-256: `43AF8F1B6E754F843900E928D354B31617338960D94799426CBFB32E3496361C`. The author incorporated both editorial precisions below. Final reviewed analysis SHA-256: `9FB85BA950C3B9E0F1217ABAA0CB4554F3A3AE6C301C73A9BD388591B9F5DF77`. No unresolved paper-review blocker remains at the stated bounded evidence grade.

## Verdict

The source-backed countercase and the explicit congruence repair are coherent at the claimed **native-level paper** evidence grade. They expose a real operational distinction that a proof-irrelevance slogan alone does not settle. No executed failure or broad-library incompatibility has been established. No new axiom or change to PI1 is required for the displayed repair.

The bounded source review found no additional K-like, structure-eta, unit-like, arithmetic or application-congruence rule that would make the displayed blocked Nat-valued computation convert directly to literal zero in a fresh checking context. The claim should remain tied to that exact family, source pin, declaration kinds and cold context.

## Independently checked source facts

All locations below are Lean `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`.

| Obligation | Independent observation |
|---|---|
| Theorem versus opaque unfolding | `kernel/declaration.h:466–487` includes theorems and definitions in native `has_value(false)` but not opaque declarations. `type_checker.cpp:555–600` uses that predicate and exact universe arity for delta unfolding. |
| Complete opaque evidence is still checked | `environment.cpp:211–222` checks the actual opaque type/value before insertion. Body retention does not make its constant delta-reducible. |
| Acc eliminates into data | `Init/WF.lean:25–36` gives the actual Acc constructor and `Acc.ndrec` with arbitrary-Sort motive and recursive-result branch arguments. Constant Nat motive/zero branch is a supported paper instantiation. |
| Blocked major does not obtain a constructor automatically | `inductive.h:77–120` normalizes the recursor major and needs a matching constructor rule. `inductive.cpp:594–615` rejects Acc as a K target because constructor arguments remain after parameters. `inductive.h:63–73` refuses proposition structure eta. |
| Native proof irrelevance has the required scope | `type_checker.cpp:932–938` requires the inferred type of the compared terms to be a proposition. It applies to p and q of type P, not directly to `Z(p)` and `0` of type Nat. |
| Remaining converter paths do not repair the missing intermediate | Read `type_checker.cpp:835–858,874–927,999–1105,1145–1245`. A stuck Acc recursor versus a Nat literal is not a pair of applications with a common head; it is not a lambda/structure/string comparison; Nat is not unit-like. Offset/native/Nat reducers do not synthesize an accessibility witness. |
| Cached successes need a scope qualifier | `type_checker.cpp:835–838` accepts a previously cached successful comparison. The displayed cold route therefore must not inherit a success cache from another realization or a separate repair. |
| Frontend `.all` is not native theorem unfolding | `Lean/Meta/WHNF.lean:207–209,232–239` has the exact-name Acc/WellFounded recursor transparency special case, while `Meta/GetUnfoldableConst.lean:78–93` independently excludes theorem records. Restoring a name or selecting `.all` does not remove that exclusion. |
| Equation-based and data-fuel alternatives actually exist | `Init/WF.lean:98–104,135–141` supplies the generic checked fixpoint equations; 484–517 supplies the Nat-measure/data-fuel construction and its equation theorem. These are source mechanisms, not evidence that exporting those closures has been executed. |

## Countercase derivation and limits

Take the displayed constructor **expression** c of `P := Acc R star` with empty relation R on Unit. This expression is not an additional theorem whose reference itself gets replaced through the same semantic judgment. The source's opaque o has body c; blocked is a theorem with body o; fast is a theorem with body c.

The source definition d reduces through fast to the actual constructor expression. The recursor's constructor rule exposes the constant-zero branch, so `Eq.refl 0` has the displayed source-native conversion route at `d = 0`. These are exact declaration-kind and reduction premises, not a surface elaboration claim.

Under the blocked target B, d reaches `Z(o)`. The opaque body is present and checked but unavailable to ordinary delta reduction. Acc's major does not gain a constructor through the K/eta rules. Its result has type Nat. The compared other term is literal zero. In a fresh context the inspected converter has neither an application pair on which to compare proof arguments nor a rule to invent fast as an intermediate. This justifies the predicted native conversion obstruction, subject to the pinned mechanisms and resource completion.

This does **not** refute declarative proof irrelevance or congruence. Declaratively one can relate the major proofs and compose the resulting equations. Operationally the concrete conversion algorithm need not invent that composition when checking this fixed proof body. Nor does the example show a changed inductive interface, a false theorem, a failed real mathlib build, or impossibility of another proof of the same statement.

The cold checker condition is natural for the baseline receiving route: checked theorem/opaque/definition insertion uses fresh type-checker instances in `environment.cpp:180–220`. Independently reusing a prior success cache after changing B would already violate PI1's coherent-environment/cache contract.

## Explicit repair is well scoped

Let p and q be exact checked proof-instance constants for blocked and fast. Check `Eq.refl p` at `p = q`; the converter directly compares proofs of the same P and its proof-irrelevance branch applies. Fully instantiate ordinary congruence with Z, p, q and that equality proof. This places q explicitly in the proof term's supplied arguments; it is not an omitted witness that the converter must discover.

The resulting proof has type `Z(p) = Z(q)`. Its left side matches the actual blocked alias used in d; its right reduces through q to zero. Thus the repaired witness targets the same semantic `d = 0` judgment and keeps d's DefinitionID within one F4. Its ProofInstanceID, actual support and possibly footprint change. No step turns an opaque constant into a definition or puts a ProofInstanceID into the semantic descriptor of d.

The repair needs complete checked support for both instances and the actual congruence operation. A local policy excluding q's assumptions may disallow this repair even though it is mathematically valid. B can stay blocked because the witness references q directly; its target statement does not force B to choose q.

## Finite-pool conflict is correctly limited

The two actual proof fields of And are confirmed by `Init/Prelude.lean:595–603`. For theorem bodies `(c,o)` and `(o,c)`, source left/right selections expose c respectively. A shared semantic And judgment allows only one selected alias at a time, so the candidate pool containing only those two instances cannot preserve both displayed original reflexivity conversions.

This is a conflict among **existing finite choices**, not proof that no global witness exists. The constructor witness `(c,c)` supplies a coherent additional candidate, and separate explicit equality repairs are another route. The paper example does not require an impossible semantic split or a new nominal inductive type.

## Requested editorial precisions

1. State that c is the displayed constructor expression, not another theorem reference, and that the predicted mismatch uses a fresh native conversion state with no inherited successful comparison cache. This makes the countercase's quantification explicit.
2. Phrase the G limitation as excluding **a reading** of the proof-replacement lemma as an unconditional algorithmic operability theorem. Frozen G already says that neither argument transfers acceptance without checking and does not promise complete source replay compatibility. H provides a concrete obstruction and repair; it need not inaccurately attribute a blanket promise to G.

Neither item changes the exhibited mathematical construction. They strengthen evidence precision and prevent accidental overclaim.

## Integration consequence

Keep separate predicates for exact semantic correspondence, complete candidate export, target replay validity, preservation of a particular original body, selected conversion success, generated-interface correspondence and frontend usability. REDUCE1's bounded alternate-B/equation/explicit-repair procedure is an appropriate concept mechanism so long as every successful output is independently checked and every changed support/certificate is rebound. No finite planning cap implies complete library compatibility or guaranteed repair discovery.

BOOT1's name-local fixed seed evidence is outside ordinary B choice; its exact theorem/opaque bodies and kinds remain bound into SeedProfile. EXTRACT1 must retain the source kinds and alternatives needed to diagnose the displayed issue. The combined design therefore preserves a trustworthy acceptance boundary without falsely promising that canonical statement identities preserve every operational reduction trace.
