# CP-001H: proof computation, canonical representatives, and reliable reconstruction

Date: 2026-09-20. Status: source-backed concept refinement and selected local reconstruction policy with [independent source/paper review](../audits/CP-001H-proof-computation-independent-audit.md). No implementation, Lean execution, build, native replay, source extraction, test, exploit or benchmark was performed. Frozen CP-001G and earlier artifacts are not edited.

## Outcome

The practical preservation boundary is stricter than "the replacement proves the same proposition." The pinned native kernel can unfold theorem bodies, but not genuine opaque declarations, while reducing a proof used by an accessibility recursor. Consequently two checked proofs of the same accessibility statement can expose different reduction behavior. Choosing another canonical semantic representative can make an unchanged source-shaped proof term fail native conversion, even when its semantic definition/group descriptors have not changed.

This note gives a concrete paper countercase and two usable repairs: select a computation-compatible representative and recheck the affected environment, or construct a new explicit checked equality/transport proof while retaining the original semantic definition and statement IDs. A finite set of source-occurrence preferences cannot always be satisfied by choosing one of the existing representatives; that limit is demonstrated separately.

Select **REDUCE1**, an owner-local, finitely budgeted export/reconstruction procedure that records those preferences and actual conversion obligations, tries bounded grounded representative plans, and permits explicit checked proof repair. Its output remains ordinary PI1 evidence. It is not a new axiom, native reduction rule, wire authority, mandatory remote execution service or global preferred-proof election.

## Frozen inputs and claim levels

Read the frozen [PI1 analysis](CP-001G-proof-instance-composition.md), SHA-256 `0E1D443FBF13727A0011BD101135BAADD79F48074137B90E5CC2FCAF63A34E3E`, and [CLIENT1 analysis](CP-001G-library-interoperability.md), SHA-256 `4CA3760D1943BA34F3E67BBB18872210CE3ABC1CF83B7513ADC63D522BD923CD`.

The pinned source for new observations is Lean commit `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`. Distinguish:

- a directly read source mechanism;
- a native-level paper family and a control-flow consequence of that mechanism;
- an actual executed frontend/build/kernel outcome, which is **not** reported here;
- a future qualified implementation result under specified budgets.

In particular, the countercase below is not a claim that a supplied `.lean` file was compiled or that a particular mathlib build failed. It specifies coherent native declarations and their typing/reduction obligations. Stock surface elaboration can have additional obstacles of its own.

The [complete-export/group-recovery analysis](CP-001H-complete-export-and-group-recovery.md) owns general source canonicalization and group-record extraction. This note owns proof-sensitive computation and the distinction between mathematical replacement, native conversion and frontend behavior.

## Three relations must not be conflated

Let `E_B` be the coherent native environment realized under a fixed F4 and representative map B. Write `Conv_K(E_B,Gamma,t,u,b)` for the qualified native conversion procedure with finite resource allocation b, whose operational result is success, conversion mismatch, or resource/incompleteness nondecision. This notation is a specification of the existing checked operation, not a new executable algorithm.

Distinguish it from a declarative typed equality relation closed under proof irrelevance, congruence and transitivity. A metatheoretic derivation relating proof-valued terms does not establish that the concrete native algorithm will reproduce every old conversion after the environment changes. In particular, it does not require the algorithm to invent an intermediate constructor-shaped proof that was not present in either compared expression.

Also distinguish both from `Meta.whnf`/frontend unification, with its own transparency, exact-name tests, metadata, heuristics and caches. A frontend can fail to expose a form that the native checker could check; changing frontend transparency does not authorize a new native reduction rule.

**Narrowed operational reading of G's proof-replacement lemma.** In an already coherent typed environment, proof irrelevance supports the stated mathematical replacement/congruence argument. It is not a universal theorem that a fixed transformed source body will be accepted by `Conv_K` under every grounded B, nor that source checks or caches transfer across B. Any reading as an unconditional operability claim is invalid: actual target checks, or an independently justified operational preservation result for the exact qualified fragment, remain necessary. G already states that the argument does not transfer acceptance without checking and does not guarantee complete source replay compatibility; this concrete countercase sharpens that existing qualification. Its rank proof continues to prove structural acyclicity, not the stronger algorithmic preservation property.

This is a compatibility limitation, not an argument that invalid mathematics should be admitted or that an inconvenient native mismatch means the proposition is false.

## Pinned native and frontend mechanisms

### Native theorems really can unfold

`src/kernel/declaration.h:466–487` defines native `constant_info::has_value(false)` to include **theorems and definitions**, excluding opaque declarations unless explicitly allowed. Do not confuse it with the separately inspected Lean-level producer accessor whose default behavior can omit theorem/opaque bodies.

`src/kernel/type_checker.cpp:555–560` uses this native `has_value()` in `is_delta`, with exact universe-arity agreement. Its unfolding path at 565–600 instantiates the stored value at the supplied universe vector. The main `whnf` loop at 735–775 invokes that unfolding. Therefore PI1's checked theorem instances and theorem aliases can expose their bodies during native computation; a genuine opaque proof does not become unfoldable just because a theorem wraps it.

`environment.cpp:192–222` separately checks theorem and opaque bodies at declaration insertion. Having a complete checked opaque body is evidence of validity, not permission to delta-unfold that body during ordinary native conversion.

### Accessibility reduction needs an actual major-premise form

`src/Init/WF.lean:25–31` declares the accessibility predicate and its constructor:

\[
\operatorname{Acc}(r,x):\mathrm{Prop},\qquad
\operatorname{intro}(x,h):\operatorname{Acc}(r,x),
\quad h:\Pi y, r(y,x)\to\operatorname{Acc}(r,y).
\]

Its nondependent recursor wrapper `Acc.ndrec` at 33–36 permits a motive into an arbitrary `Sort`. The branch receives the constructor's accessibility field and the recursive results. Thus accessibility evidence can occur as a major premise of a computation returning Nat or a type; this is ordinary well-founded-recursion infrastructure, not unsafe extraction from an arbitrary proposition.

`src/kernel/inductive.h:77–120` identifies the actual recursor, obtains the major premise, normalizes it, looks up its constructor rule, and returns no reduction when no rule matches. `inductive.cpp:594–615` restricts the K-like shortcut to an inductive predicate with a single constructor and no post-parameter constructor arguments. Acc has such arguments and is not covered by that shortcut. `inductive.h:63–73` also refuses structure eta expansion when the major's type is a proposition. Neither mechanism supplies an arbitrary accessibility constructor when reduction is blocked by an opaque proof.

The kernel's proof-irrelevance check at `type_checker.cpp:932–938` compares **proofs**, requiring their inferred type to be a proposition. It does not directly identify a stuck Nat-valued recursor application with zero. The conversion procedure at 1171–1245 tries its specified reduction/application/eta cases; it does not search the library for another proof of an accessibility proposition to make a data term reduce.

### The frontend has an additional, different boundary

`Lean/Meta/WHNF.lean:207–209,232–239` recognizes the exact names `Acc.rec` and `WellFounded.rec`, and raises default transparency to `.all` while reducing their major premise. Content-renaming a recursor without a qualified local frontend interpretation can lose that special case.

However, **restoring those names or setting `.all` is not sufficient for theorem-backed major premises at this pin**. `Lean/Meta/GetUnfoldableConst.lean:78–93` returns none for theorem records independently of the transparency setting. The `.all` bump can help definition-backed proof helpers; it does not override the theorem-kind branch. Native C++ theorem unfolding and frontend theorem opacity are therefore separate source facts.

CLIENT1 qualification must distinguish ordinary frontend convenience from native acceptance. Exact names may be restored only with its existing exact semantic correspondence, and no theorem is silently reclassified as a definition to make frontend reduction convenient. Equation lemmas, explicit proof-carrying transports or a separately qualified owner-local native-check-assisted construction route can instead supply complete terms for independent receiving checks.

## Positive case: a proof field need not obstruct data projection

Fix n : Nat and proofs p,q of the same predicate H(n). Let a_p and a_q be native values of the **same** subtype/record, each with data field n and proof field p or q. Projecting the data field from either constructor application returns n without evaluating the proof field.

This follows from the actual constructor-layout projection rule: `type_checker.cpp:420–438` checks the projected constructor's inductive identity and selects the exact field offset. It does not normalize every proof field before projecting the data. The existing Finset/quotient examples therefore do not automatically become unsupported merely because their definitions contain proof terms.

The qualification conditions remain exact group/constructor/field selectors, well-typed complete values and actual support. A computation that instead invokes a recursor on the proof field has a different obligation. A matching result type or propositional projection equality cannot replace the qualified computational projection correspondence fixed in CLIENT1.

## Countercase: an acyclic earliest representative can obstruct a source conversion

This is a paper native-declaration family, not executed Lean code. Use a fixed exact Unit and Acc interface. Let star be Unit's inhabitant, let `R(y,x) := False`, and put `P := Acc R star`.

The constructor term

\[
c=\operatorname{Acc.intro}\;\star\;
  (\lambda y\,h.\operatorname{False.elim}(h))
\]

has type P. Here c is notation in this analysis for the displayed **constructor expression**, not a separately declared earlier theorem of P that would create another representative candidate. Define a Nat-valued recursor `Z : P -> Nat` using `Acc.ndrec` with constant Nat motive and branch `m x children ih := 0`. Its constructor rule gives `Z(c)` reducing to zero.

Now consider this exact declaration-kind/order distinction:

| Declaration | Native kind | Type and complete value |
|---|---|---|
| o | checked safe opaque | `o : P`, body c |
| blocked | checked theorem | `blocked : P`, body o |
| fast | checked theorem | `fast : P`, body c |
| d | safe definition | `d : Nat`, body `Z(fast)` |
| result | checked theorem candidate | `result : d = 0`, body `Eq.refl 0` |

In the source native environment, d unfolds to `Z(fast)`, fast unfolds to c, and the recursor reduces to zero. Thus the displayed fixed proof body's source typing obligation has the indicated native reduction route. The declarations are finite and acyclic. This is not a claim about which surface tactic would produce that body under the pinned frontend.

Both blocked and fast have the same semantic judgment j, with the same empty telescope and universe vector. PI1 keeps their proof implementations separate. The semantic descriptor of d contains `Z(J(j))`, not a source-specific ProofInstanceID. The earliest-source choice chooses `B(j)=blocked`.

In that target realization the reduction path is instead

\[
d\;\longrightarrow\;Z(J(j))\;\longrightarrow\;
Z(w(\mathrm{blocked}))\;\longrightarrow\;Z(o).
\]

The complete body c of o is retained and checked, but o is opaque. Acc is not K-like, and proposition structure eta does not manufacture its constructor. The recursor is therefore stuck at o. Comparing this Nat-valued expression with zero does not invoke proof irrelevance on the data result, and the inspected conversion path supplies no missing intermediate accessibility proof. Use a fresh native checker state for the displayed obligation, with no inherited successful-conversion cache for these expressions and no stale cache from another B. Under those exact native rules, the original `Eq.refl 0` body's conversion obligation is predicted to fail if evaluation reaches that mismatch rather than a resource limit.

**What this establishes:** structural source acyclicity and exact same-proposition representatives do not entail that the chosen earliest-B realization accepts every unchanged source-shaped proof body. The target definition d itself can still check at Nat. The failure is the original result proof's required conversion.

**What this does not establish:** an executed failure, a failure in an inspected actual mathlib build, changed Acc generated rules, a new nominal group, mathematical falsity of `d=0`, or impossibility of a useful PI1 representation. The same group interface is enough for the obstruction; group-shape mismatch is a separate qualification question.

## Two concrete repairs preserving d's semantic identity

### Select the computationally useful representative

Select `B(j)=fast`, construct the corresponding clean/coherent target environment, and independently recheck all affected types, bodies and generated interfaces. The actual alias then unfolds to c and restores this example's direct conversion. The semantic d descriptor and its DefinitionID are unchanged **within the same F4**. The replay ID, selected support and validation context change.

An old certificate from the blocked or source environment is not copied. A source-occurrence preference for fast is an operational search input, not a proof that all target checks will succeed.

### Keep B and construct an explicit equality proof

It is also possible to retain `B(j)=blocked`. Let `p := w(blocked)` and `q := w(fast)`. Both are independently checked at P. A proof of `p=q` can be constructed by checking `Eq.refl p` at that type: this comparison is between **proofs of P**, so it uses the actual native proof-irrelevance rule directly.

Ordinary congruence then supplies

\[
e:p=q,\qquad
\operatorname{congrArg}(Z,e):Z(p)=Z(q).
\]

The right side reduces through the retained fast instance to zero; the left corresponds to d through the actual chosen alias. Independently checking this new term supplies `d=0` without asking the converter to invent the intermediate q. The witness term contains exact ProofInstance references to p and q; it does not insert a JudgmentID constant into WitnessTermDAG or a ProofInstanceID into d's semantic body.

This is a **new proof instance of the same target statement**, with its actual extra support. It is not a claim that the old proof body was preserved or that q's assumptions are free. If policy forbids q's footprint, the repair is unavailable under that policy. The opaque o remains opaque, and its complete actual body remains required evidence.

This concrete repair is stronger than saying "try again": it identifies the missing intermediate proof and constructs the exact proposition-level evidence that removes dependence on the failed implicit conversion. A general exporter may not be able to find such a repair for every source body within budget.

## A single B need not satisfy all existing source preferences

Reuse P, c, o and Z. Let `hL : P and P` have constructor fields `(c,o)`, and `hR : P and P` have fields `(o,c)`, both checked theorems. The pinned `And` declaration at `Init/Prelude.lean:595–603` has precisely those two proof fields.

The source definitions `dL := Z(hL.left)` and `dR := Z(hR.right)` both have a constructor-reduction route to zero. Their corresponding fixed reflexivity proof bodies therefore have that source-native route. hL and hR have the same exact semantic judgment k.

After semantic normalization, both definitions use the one alias `J(k)`. In the finite candidate pool containing only hL and hR:

- choosing hL makes the right computation reach o;
- choosing hR makes the left computation reach o.

Therefore neither existing representative preserves both displayed source conversions. Exact source-occurrence preferences conflict even though the mathematics and source graph are coherent. This is a finite-pool obstruction, not a theorem that no usable representative exists.

A newly checked witness with fields `(c,c)` is one constructive additional candidate. Alternatively, each result can be given an explicit checked equality proof as above, with its actual source evidence. Neither option is authorized by merely choosing a preferred source name or suppressing an inconvenient dependency.

## Existing library mechanisms supply robust equation paths

The pinned `Init/WF.lean:98–104` defines `WellFounded.fixF` over an explicit accessibility proof and proves the generic equation `fixF_eq` by induction. At 135–141, `WellFounded.fix` uses `apply hwf x`, and `fix_eq` states its unfolding equation for arbitrary supplied well-founded evidence.

For a constant-zero step F, instantiating the checked `fixF_eq` or `fix_eq` gives an equality whose right side beta-reduces to zero without requiring the arbitrary accessibility/well-founded proof on the left to expose a constructor. This is a useful actual-library **paper application path** for an opaque-backed proof: use a checked equation theorem, not a claimed new definitional reduction. Its complete actual theorem/definition support must still be exported and checked.

The same file at 484–499 explicitly supplies `WellFounded.Nat.fix`, specialized to Nat-valued measures, with a data-fuel recursor; the source documentation says it reduces when the measure evaluates to a ground value. At 513–517 it has its own equation theorem. This supplies another practical design choice for new computations, but replacing an existing definition with Nat.fix changes its descriptor unless a separately checked transformation/bridge is provided. It is not a silent canonicalization rule.

No equation theorem permits omitting proof arguments, marking an opaque declaration transparent, executing a remote tactic or accepting unsafe native computation. The result is still a complete ordinary term checked under the chosen native policy.

## REDUCE1: selected bounded reconstruction contract

### Owner-local records

Retain the complete source-to-semantic and source-to-instance maps required by the exporter. For computation-sensitive reconstruction, additionally retain finite local records of:

- the source declaration/occurrence path and its actual selected source proof instance;
- the target semantic judgment, exact local telescope and universe substitution;
- the containing semantic type/value/group member and ordinary dependency path;
- the relevant declaration kinds and available alternative proof instances;
- any actual failed target conversion pair and diagnostic location, bound to the target environment/checker/adapter and budget;
- the proposed response: representative choice, explicit term repair, or a precise unsupported/nondecision outcome.

These records are local correspondence/diagnostic data. They do not become mandatory public provenance, network theorem authority or a permanent preferred-witness registry. A producer claim that an occurrence is harmless cannot remove it from actual support.

A conservative source scan can flag theorem occurrences in semantic types/values/groups and recursor-major dependencies as candidates for scrutiny. Such syntactic flags are **not** a complete relevance oracle: reductions may expose dependencies transitively. Actual complete checking remains decisive, and missing diagnostic information is reported rather than used to infer preservation.

### Finite planning and checking policy

The owner supplies aggregate acquisition, parsing, graph, native-check, memory and elapsed-time budgets. One example envelope permits at most 16 distinct complete representative plans, at most four retained alternatives per demanded judgment, and at most 256 diagnostic/repair attempts with 16 MiB of local diagnostic bookkeeping. These adjustable caps are not measured practical library defaults, and complete native environments/support require separately funded finite capacity within the same aggregate owner allocation. Per-plan quotas never create free retries.

The selected sequence is:

1. Preserve actual complete source alternatives before import coalescing where needed. Normalize semantic descriptors and witness expressions using their distinct PI1 grammars. Preserve exact declaration kinds, universe vectors and scopes.
2. Construct a grounded initial B and its exact root-reachable closure. Earliest-source choice remains a valid structural starting plan, not a promise of computational success.
3. Reconstruct/check the selected native environment. Only complete success can produce an accepted replay. Record actual failed obligations without declaring their propositions false.
4. For a representative-sensitive conversion failure, first nominate the actual source witness used at the failing semantic occurrence, if complete and policy-admissible. Then nominate other retained candidates according to source occurrence relevance, compatible support and honestly scoped cost. Ground every proposed plan again; a source preference never permits a support cycle.
5. Rebuild/fork coherently and recheck the affected closure. The baseline can conservatively recheck the whole selected closure. Any smaller recheck set must include reverse-reachable dependencies through **types, values and generated group support**, with exact receiver-owned compatibility records. Never overwrite an installed alias in place or carry old conversion caches across a changed B.
6. If existing B choices fail or conflict, admit a bounded explicit-proof repair. Prefer directly applicable checked equation lemmas or an explicit proof-irrelevance/congruence intermediate as demonstrated above. The candidate constructor is untrusted; every new term and full support is checked. No automatic remote program installation is part of this step.
7. If repair succeeds at the original exact statement, emit a new ProofInstance and its actual replay while preserving unchanged semantic descriptors. If repair changes a statement, type or definition, expose the new identity and any actual checked correspondence. Added hypotheses produce a conditional theorem, not success at the original unconditional claim.
8. If the allocation is exhausted or no qualified repair is found, retain whatever independently usable prior branches the owner still protects and return the exact failed/incomplete export scope. Do not advertise a complete library view or a successful interoperable source replay.

This procedure supplies a concrete local usability mechanism without promising a universal conversion-repair algorithm. No fixed finite cap can guarantee that an existing compatible representative or short proof will be found.

## Preservation and qualification conditions

The exporter/client must report separate predicates, rather than one ambiguous "round trip succeeded":

| Predicate | Required evidence |
|---|---|
| Exact semantic correspondence | The selected normalized type/value/group descriptor matches under the explicitly permitted reference/annotation transformation, with exact universe order, telescope split and native kinds. |
| Target replay validity | Complete native checking under the actual F4, B, checker/adapter and support; not the source's acceptance bit. |
| Original-body preservation | The specifically transformed source body checks at the exact target type. A newly repaired proof does not satisfy this predicate merely because it proves the same statement. |
| Selected conversion preservation | The declared finite conversion obligations succeed under their bound target context and allocation; no extrapolation to every future application. |
| Generated-interface correspondence | The qualified reconstructed group descriptor/member/rule inventory agrees under the selected exact comparison, or returns an explicit mismatch. |
| Frontend usability | The declared local name/metadata/transparency operations work within the independently qualified client scope; native acceptance alone is insufficient. |
| Current reusable evidence | The actual selected closure remains available, protected and policy/incident-admissible. |

The complete-export analysis owns how original declaration inputs or completed group records supply the generated-interface comparison. A mismatch means that the stated source-correspondence route failed; it does not by itself prove that the separately reconstructed target mathematics is invalid. This note has exhibited a native conversion obstruction with an unchanged Acc interface, not a distinct generated-shape counterexample.

Exact universe/telescope details are computationally relevant. The pinned native constant checker at `type_checker.cpp:101–122` requires exact universe arity and declared parameters; `is_delta` also checks arity before unfolding. Do not drop an unused parameter, reorder a universe vector, shift a dependent local variable or close a witness twice and then call the changed result "the same proof." Group constructor/recursor order and exact selectors are equally binding; a renamed recursor still needs its actual regenerated rule inventory.

## Required future conformance cases

- A proof-bearing constructor's data projection succeeds without evaluating its proof field.
- A theorem-backed Acc constructor reduces natively; a genuine opaque-backed major blocks the displayed direct data reduction despite complete checked evidence.
- The earliest-source blocked/fast family produces the specified conversion diagnostic, and choosing fast restores the direct source-body route under a newly checked context.
- The explicit congruence repair proves the original exact target with B still blocked, distinct new proof-instance identity and complete additional support.
- The two-field preference conflict does not claim that either existing B preserves both original bodies; a new checked representative or explicit repairs are recorded honestly.
- Generic checked `fixF_eq`/`fix_eq` supplies the constant-step result without relying on constructor exposure of the actual well-founded proof.
- Frontend `.all` and restored recursor names are not incorrectly treated as theorem-unfolding authority at the pinned source.
- Changed B invalidates dependent conversion caches/certificates even when semantic IDs stay fixed; finite recheck costs are charged.
- Missing original proof bodies, changed universe arity, generated-interface mismatch and resource nondecision remain separate from a proposition's falsity.

All are future qualification obligations. Their inclusion is not a report of execution.

## Sources

- [Frozen PI1](CP-001G-proof-instance-composition.md) and [frozen CLIENT1](CP-001G-library-interoperability.md), hashes above.
- [Pinned native theorem/opaque value classification](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/declaration.h#L466).
- [Pinned native delta/universe substitution](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/type_checker.cpp#L555), [WHNF](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/type_checker.cpp#L735), and [conversion](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/type_checker.cpp#L1171).
- [Pinned checked theorem/opaque insertion](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/environment.cpp#L192).
- [Pinned native recursor reduction and proposition-eta restriction](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/inductive.h#L63) and [K-target condition](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/inductive.cpp#L594).
- [Pinned Acc and well-founded equations](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Init/WF.lean#L25), [fixF_eq](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Init/WF.lean#L98), and [Nat-measure fixpoint](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Init/WF.lean#L484).
- [Pinned frontend exact-name recursion handling](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Meta/WHNF.lean#L207) and [frontend theorem exclusion](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Meta/GetUnfoldableConst.lean#L78).
- [Pinned And proof fields](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Init/Prelude.lean#L595).
- [Pinned source comment on theorem coalescing/accessibility computation](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Environment.lean#L2249).
