# Why an optional interface view can remove unnecessary work safely

Root argument, 2026-10-20. Source-supported design, not completed runtime evidence.
This concerns proposal construction, not a replacement mathematical checker.

## Acceptance stays unchanged

Let E be the environment specified by authenticated module declarations. Let
V(E,p) be the adopted final native checking relation for proposed extension p.
The existing acceptance rule also discharges every exact certified/native parent
premise and enforces its foundation, policy, rank and resource conditions.

A frontend F receives a view of E and proposes p. It is not mathematical
authority. Replacing F's input by an explicitly partial view can affect which
proposals it produces, but cannot change the accepted set if all of the following
conditions are preserved:

1. Final witness construction uses original authenticated declarations, not
   substituted frontend descriptors.
2. Missing imported definition values remain `Definition + Missing(hash)` with
   their original reduction hints. They never become final axioms or opaque
   declarations.
3. Final correspondence checks bind every imported name/type/kind/commitment
   to those authenticated declarations. Newly declared axioms remain forbidden.
4. V and actual premise discharge still run before any warrant/publication.

Under these conditions a new accepted result still satisfies the same V(E,p)
and premise obligations. This implication does not require trusting F, proving
it complete, or asserting equivalence between opaque and transparent constants.
It inherits, rather than discharges, the existing checker and cryptographic
assurance assumptions.

The new proposal view treats only an absent ordinary imported definition body
as unavailable for frontend computation. Its name, universe arity and type are
preserved. The original descriptor is retained separately. Existing Lean
frontend support for untrusted opaque/theorem interfaces can supply the rigid
placeholder, provided projection never feeds final native witness construction.

## A concrete avoidable dependency family

Consider independently certified definitions d_0, ..., d_n, all of fixed
foundation type T, where d_(i+1)'s body refers to d_i. Their types do not refer
to prior d_j. A client wants to reason abstractly about d_n, for example use
reflexivity or a generic theorem instantiated at d_n without unfolding it.

The current eager context algorithm visits every imported definition body.
Starting with d_n, it therefore demands n+1 bodies and their body-reference
declarations/warrants. For the proposed interface view, the required semantic
input is the d_n descriptor plus its fixed type support; the uninspected bodies
do not introduce new demands. Certificate availability for d_n is an explicit
assumption, not a free producer cost.

For this family, eager semantic acquisition grows at least linearly in n;
interface-only semantic acquisition is independent of n, excluding address bit
length, the exact certificate, selected interface and ordinary resource costs.
This is a family-specific upper/lower comparison, not a lower bound on all
mathematical algorithms or a claim that every Lean proof avoids unfolding.

The retained native checker has a concrete compatible path: `tc.rs::def_eq`
calls `def_eq_quick_check` before reduction, and syntactically identical terms
return true there. `ValueSlot::Missing` still raises a body demand when its value
is actually required. A targeted implementation check should exercise both
body-independent success and refusal when a missing body is needed.

## Limits and honest growth interpretation

Hidden reducible type aliases or definitions needed during elaboration can
prevent frontend construction. Inductives and recursors remain fully supported
by the existing eager path, not generalized to missing computation rules.
The first slice has no automatic fetch/retry: final missing-body failure remains
charged and yields no accepted result. Local users can choose the unchanged
eager mode when computation is needed.

Compared with an equally optimized ordinary library, this optional view is not
an intrinsic cryptographic advantage: that library can also expose abstract
interfaces. The defensible improvement is removal of our current mandatory
body-acquisition cost, enabling bounded reuse on this family. A positive whole-
network growth margin still includes certificate production, index/custody
service, failures and actual demand. No new receipt or exponential discovery
claim follows from this change.

## Source anchors

- `runtime_efficient/mixed_claims/imports_atomic.py::_build_context`: eager
  definition and recursor body traversal.
- `authoring/native02/AuthorLean.lean::installGroup`, `checkInfo`: existing
  rigid imported theorem/opaque frontend interfaces and eager definitions.
- `mixed_claims/authoring_atomic.py::MixedSourceOperation.finish` and
  `delta/reprepare.py::emit_relation_rows`: original-descriptor native emission.
- `modules/native_rows.py::NativeRows.group`: exact `moduleImportDef` emission
  when an imported definition's body is absent.
- `modules/native/checker/src/{parser.rs,env.rs,tc.rs}`: definition kind/hints,
  explicit missing-value demand, and equality-before-reduction.

These are semantic source anchors. Current installation selection remains the
explicit SDK map in NOW; a successor must pin its actual dependency graph.
