# Beyond fixed vocabulary: the next semantic boundary

Root investigation, revised 2026-09-29 after
[independent challenge](../../../experiments/certified-collection-01/VOCABULARY-CHALLENGE.md).
**Design proposal, not implemented or qualified.** The challenge preserves the
original draft's exact identity; this revision addresses its six findings,
without treating the revised argument as a verified implementation.
The live collection certificate/receiver work remains first. This note narrows
one unresolved issue in SCALE-DESIGN rather than selecting a new runtime or
claiming that the current fixed-support profile covers a growing vocabulary.

## The unresolved problem

Eliminating ancestral theorem proofs is necessary, but not sufficient, for a
large mathematical commons. New work introduces definitions. A theorem about
a constant cannot be interpreted from its printable name and type alone:
`c : Nat` with value zero and `c : Nat` with value one are different meanings.
Conversely, requiring every consumer to unfold every definition would recreate
a history-sized download through a different dependency edge.

The design should distinguish two uses of a certified definition:

1. **Sealed reasoning:** use its exact type and certified laws, without unfolding.
2. **Selected computation:** fetch its authenticated body/rules when the local
   computation explicitly requires them and the adopted profile permits them.

The current implementation supports neither arbitrary new-definition route.
Its safe body-free imports are Prop premises over fixed support. Merely deleting
that Prop check would be unsound as an implementation change.

## A candidate sufficient invariant: common realization

Fix a foundation F and a conservative-extension discipline. Let S be a finite
signature of named typed declarations. A realization r assigns an actual
F-relative definition to each non-foundational sealed data constant, preserving
universes, types, shared references and the adopted conversion rules. The
assignment is mathematical witness material, not compulsory receiver input.

A module certificate should establish an F-derivable typed substitution by
those exact definitions and derivations of its exported laws after substitution:
`F |- r(p) : r(P)`. It must not merely assert existence of a model in which
the laws happen to hold: independent P and not-P could separately satisfy
that weaker condition and still be invalid to combine. This is relative
derivability, not a proof of F's consistency or of intended-model truth.
Its public semantic identities commit to the actual definition/group
descriptors and referenced semantic identities.

For two certified modules, independent existence of realizations does **not**
justify combining them. They must agree on every shared semantic constant.
Otherwise one module can prove `c = 0` and another `c = 1` under incompatible
realizations of the same apparent `c`. A common display name is no evidence of
agreement; separately satisfiable signatures need not have a common model.

Content-bound identity alone is not sufficient. The proposed next profile
requires all of the following, relative to explicit commitment binding and
recursive-certificate assurance assumptions:

1. One foundation and interpretation/reduction profile for the combined proof.
2. Canonical descriptors binding kind, universes, type, body and every external
   semantic reference. Hash equality implies descriptor agreement only under
   the commitment assumption, not unconditional mathematical injectivity.
3. Discharged validity evidence for each non-foundational reference; an
   identifier or locally added axiom is not such evidence.
4. Strict dependency-rank descent across the entire finite reachable closure,
   including external type/body edges, not only a module's internal order.
5. Each definition checked as a safe total nonrecursive extension of its
   already certified predecessor context, with no direct or indirect self use.
6. A certificate-bound projection from the hidden descriptor to the exact
   public sealed signature: identity, kind, ordered universes/constraints,
   canonical type and external bindings. A body hash alone cannot authenticate
   an independently supplied signature. In particular `c : Nat` must never
   be imported as `c : Empty` under a valid but disconnected certificate.

For a finite union of selected closures, descent gives a topological order.
Under the rules above, induction constructs a common typed realization by
conservative extension; equal identities have the same descriptor and external
bindings. This is a logical argument under the stated hypotheses, not a demand
that receivers actually download or expand that closure. The recursive
certificate must establish the hypotheses without ancestral body retrieval.

Global display-name uniqueness, authorship, blockchain order and a worldwide
context root are unnecessary. Locally chosen aliases must resolve to exact
identities before checking and export. Distinct semantic constants with the
same display name may coexist under different local aliases.

Under that invariant, a new ordinary proof checked against sealed constants
and certified Prop laws can be interpreted in the common realization. Its
certificate must discharge the imported laws and certify the new checking
step. The receiver relies on that relation plus its cryptographic assurance;
stock Lean accepting an axiom-shaped entry alone establishes none of this.

The required consumer metatheorem is:

```text
CompatibleTypedRealization_F(r, S)
and F |- r(l_i) : r(L_i) for every imported law
and Check_sealed(F, S, L, q, Q)
imply F |- r(q) : r(Q).
```

Here sealed constants are rigid: the consumer receives no new conversion rule
from a descriptor hash. Dependent types, universe instantiation, references,
and every permitted conversion belong to this substitution obligation. This
is a proposed soundness argument, with canonical semantics, substitution,
conservative extension and actual recursive security still to establish.
It is not a proof of the existing implementation.

## Start with acyclic definitions, not arbitrary inductive extensions

The smallest consequential extension would allow one total, nonrecursive
definition whose type and body use the already supported foundation and exact
certified earlier declarations. Its identity commits to kind, ordered universes,
type, body, external identities and the supported reduction policy. Creation
checks the type/body and all referenced certified declarations; recipients can
choose a sealed signature plus laws without obtaining the body.

Do not include arbitrary axioms, unsafe declarations, partial definitions,
native evaluation or user-installed reduction rules. Keep mutual inductives,
positivity, generated recursors and nested auxiliaries outside this first
extension. A later group encoding would need scoped internal slots to avoid
self-hashing name cycles; hashing ordinary recursive names is not a solution.

Sealing deliberately removes definitional reduction through the remote
constant. Certified equality laws can support explicit rewriting instead.
This may reject an unchanged Lean source that relied on unfolding. It is a
different supported authoring profile, not a promise of universal source
compatibility or an instruction to fetch all proof history on failure.

## A concrete future discriminator

Use a new, certified composition definition and its application law. A producer
checks the actual defining body and proves the law. A consumer receives only:

- the exact sealed definition signature and semantic identity;
- the application law's interface and final validity evidence;
- the local fixed support and its own new proof.

The consumer proves a new composition property using the law, not by unfolding
or copying the producer's body. A separate, explicitly requested computation
may fetch the definition body, verify its exact identity and evaluate it.
These are two distinct operations with distinct input sets and costs.

Required refusal cases include substituted bodies under an unchanged identity,
an altered public signature, ambiguous aliases or interchange of different
semantic identities, unbound/uncertified external references, non-descending
dependency ranks, mismatched universe order, an unproved law, unsupported
recursion and a conversion demand for an unavailable/forbidden body. Distinct
identities sharing a display name should also pass a coexistence test under
separate aliases. A refusal does not imply mathematical falsity.

Include a dependent-conversion case: a term checked using transparent `n := 0`
may require an explicit certified equality/transport when used with sealed n
in a type such as `Fin (n + 1)`. The consumer may not grant that conversion from
a commitment alone or silently fetch proof ancestry to make it work.

The semantic gate is common realization and genuine successor certification,
not merely successful Lean elaboration with two new axioms. The engineering
gate is absence of producer bodies and proof histories from sealed-consumer
inputs, followed by a real certificate accepted at another cold receiver.
No such experiment is selected by this note; reuse the qualified infrastructure
when this boundary becomes the next central priority.

## Scale and benefit limits

For selected signatures of size I, all transitively demanded computation data D, certificate
evidence C and required lookup/authentication data L, desired receiving bytes
remain O(I + D + C + L), with no compulsory ancestral-proof-size term. Type
expressions and semantic references can themselves be large. Their cost must
remain visible; compressing them to a hash does not make them locally usable.
Demanding computational bodies must be explicit, bounded and separately charged.
D is not merely the top-level body: its evaluation may demand a large body/rule
closure or produce a large result. No uniform cheap-evaluation guarantee follows.

Certified rewrite interfaces may reduce bandwidth while increasing proof-search
or rewriting work. Their practical value therefore requires a matched complete
workflow comparison; neither the realization argument nor a shorter payload
proves positive amortized benefit. A growing network also still needs selective
discovery and custody, independently of this mathematical acceptance rule.

## Priority decision

Finish the current actual collection proof, selective intake and usable
contribution boundary first. Then choose between this vocabulary extension and
the measured producer-cost bottleneck using actual outcomes. Do not add a
global ledger, political identity machinery or an untested larger formal
language to make the existing small example look like a complete large system.
