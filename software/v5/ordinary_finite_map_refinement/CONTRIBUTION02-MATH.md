# Accepted contextual-refinement endpoint: saved mathematical audit

2026-10-28. **PASS_SAVED_MATHEMATICAL_ENDPOINT.** Scope: actual saved declarations,
types, definitions, proof dependencies and native-input correspondence from
`experiments/v5-local-checks/finite-map-refinement-contribution02`.
No product import, Lean execution, fresh proof replay, owner/database access or
Git mutation occurred. This agent authored the source correction; this is a
saved-data audit, not a separate independent prover or formal exporter proof.
The independent operational audit is separate.

Accepted root:
`d06c73e7dbd80203deee01e565f508fa239f9b819e58b44588033718dd80e559`.
Its actual parent remains
`ad4aa90b014ff326ded6f4750dd4f6ac7e3b56d15027114b91788923d0238079`.
Admission reports CHECKED for 21 units. These contain 27 names and 11 selected
public definition/theorem targets. The result is a substantive extension of the
received plan theory with new contexts and contextual refinement laws.

## Byte and identity correspondence

All 21 canonical evidence files match RESULT's length/SHA pins (379,701 bytes
combined). Recomputed evidence-domain IDs match all 21 unit IDs; recomputed
export-domain IDs match all 11 selected targets. Actual native units.json
contains exactly those 21 units, in admission's retention order. The worker's
27 names equal their combined inventories. Target names and acquired triples
equal their snapshots in order; all 68 internal refinement import bindings
match recomputed export identities. Every expression packet was scanned:
no sorryAx, admit, Lean.ofReduceBool or Lean.trustCompiler occurs.

These are correspondence checks. Mathematical authority remains the unchanged
adopted native receiver; this diagnostic decoder is not a second checker.

## The actual new datatype and definitions

Context's actual descriptor has one universe parameter u, one type parameter
`A : Type u`, no indices and exactly the intended five constructors. Its group
contains Context, Context.rec and all five constructors. The recursor has one
parameter, one motive and five minor premises; constructor field counts are
0, 2, 2, 2, 2. All recorded safety flags are safe.

Decoded constructor types are:

```text
hole        : Context A
seqLeft     : Context A -> A -> Context A
seqRight    : A -> Context A -> Context A
chooseLeft  : Context A -> A -> Context A
chooseRight : A -> Context A -> Context A
```

Actual fill is polymorphic in K/V and has type
`Context (Plan K V) -> Plan K V -> Plan K V`. Its body applies Context.brecOn to
fill._f. The actual fill._f branches return the hole's plan, sequence the
recursive result on the correct left/right side, or choose with the recursive
result on the correct left/right side. The named matcher and structural recursion
helpers are present as checked definition units. This is a generic context
datatype specialized to the received Plan, not an axiom naming the desired fill.

The other four definition bodies were decoded and inspected:

| Definition | Actual meaning |
|---|---|
| NonemptyResults p m | Every n satisfying Exec p m n has n.isEmpty = false. |
| Refines p q | For every m, NonemptyResults p m implies NonemptyResults q m. |
| ContextuallyRefines p q | For every c and m, the same implication holds for fill c p and fill c q. |
| ContextuallyEquivalent p q | ContextuallyRefines p q and ContextuallyRefines q p. |

These definitions have exactly the expected BEq/Hashable instance arguments.
The direction of refinement is preserved; no equality of final maps or execution
traces is asserted. Context and fill introduce no map-instance requirement.

## Actual theorem meanings and reuse

All six public theorem types retain universe parameters u/v and explicit Plan
arguments p/q. fill_summary_mono has no map-instance arguments. The five semantic
theorems have precisely BEq, Hashable, EquivBEq and LawfulHashable instances.
Completeness/equivalence and the counterexample theorem retain the explicit map
e and hypothesis `e.isEmpty = true`; no empty-map existence premise is hidden.

| Theorem | Actual endpoint |
|---|---|
| fill_summary_mono | Summary implication from p to q is preserved by every c. |
| refines_of_summary | Summary implication implies Refines p q. |
| contextual_refines_of_summary | Summary implication implies ContextuallyRefines p q. |
| contextual_refines_iff | Given an empty e, contextual refinement iff summary implication. |
| nonrefinement_witness | Given empty e, mustWrite p = true and mustWrite q = false, returns NonemptyResults p e, Exec q e e, e.isEmpty = true, and not ContextuallyRefines p q. |
| contextual_equivalence_iff | Given empty e, contextual equivalence iff mustWrite p = mustWrite q. |

Actual proof dependencies match the source argument: Context.rec and private
OR/AND lemmas establish monotonicity; nonempty_iff transports the guarantee;
the hole establishes completeness; mutual Boolean implication gives equivalence.
The inspected nonrefinement_witness term binds hn using nonempty_iff and hrun
by applying zero_effect_witness to **q, e, hq**. It returns that concrete
execution, preserves he and derives the contradictory Boolean equality using
that same witness, rather than a marker of failed search/checking.

The decisive exact upstream import bindings are:

| Imported theorem | Export ID | Actual direct users |
|---|---|---|
| FiniteMapEffects.nonempty_iff | `3fe2401bbd04ea80d7d7ab4851005865e43b9669099f78f5e0892dfeeaad4175` | refines_of_summary, contextual_refines_iff, nonrefinement_witness |
| FiniteMapEffects.zero_effect_witness | `3d68aec796ef21713c99e7c839663a4c49f3aa06a45ab3f17982dc812113877c` | nonrefinement_witness |

These are the exact acquired/discovered identities, not same-named replacements.
The other contextual laws reuse the newly checked intermediary laws, so their
transitive dependence on the imported theory is genuine even where the direct
import list contains only the new intermediary names.

## Exact accepted unit map

The complete 21-unit/name/export map remains in the pinned RESULT; it is not
duplicated here. All units match the actual native list and its reported
retention order. The composition is one seven-name inductive group, 11
definitions (five public endpoints plus six helpers), and nine theorems
(six public endpoints plus three private Boolean lemmas).

## Audit input pins and claim limit

| Saved input | Bytes | SHA-256 |
|---|---:|---|
| contribution/RESULT.json | 42,128 | `37ea97b2c006b216782e7a53142ed741a53a26a86a3b89ded9252dae1279b9b0` |
| native call units.json | 335,508 | `846da3506e6b6ed21489dcf24a634bac0bb66cb7328915518c4f524282323eac` |
| native call worker-report.json | 6,035 | `a9ae9f3e96b84ccbc87fd041ee49dfda2059c9119b8fc8bc30373f72f3914bde` |
| selected BodyParametric.lean snapshot | 6,902 | `55988cf3fde26bc08173cbc352c1266ea836897ac56d70ec45c8e9e900d71b9d` |

Native call directory is the original Std catalog's
`admission-calls/95746899a32b13c1f7667db9c68a61a276a523754cbddc44376c520ea1d407d6`.
Per-unit byte/SHA pins and all eleven export IDs remain in the pinned RESULT.

This closes the intended local mathematical endpoint: a received theory supports
a new general concept and checked consequences through the standard public
launcher, using the selected frontier. It does not establish independent
recipient use, historical novelty, automated concept selection, causal discovery
speedup, general compiled-library interoperability or final deployable v5.
