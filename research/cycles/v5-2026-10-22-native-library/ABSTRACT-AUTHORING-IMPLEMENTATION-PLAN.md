# Minimal abstract authoring handles

2026-10-23. Source-only design by `preview_boundary_review`, following root's
`ABSTRACT-AUTHORING-BOUNDARY.md`. No implementation, runtime or Git action is
selected here. Consumer02's dependency-closed projection retains 316 basis
rows and omits 265, but required `Nat.xor` is an existing public axiom-shaped
handle. Dropping that required row is not a solution.

## Proposed rule

Permit an **already existing safe `.axiomInfo`** to serve as an abstract
construction handle for an independently warranted definition or non-theorem
opaque, provided its name, universe interface and type match the exact accepted
row. Ordinary rows compare the exact ordered universe-parameter encoding and
original type DAG; legacy fixed-basis rows use the existing normalized universe
arity/type-DAG convention. Exact semantic symbol IDs remain authenticated by
the controller and unchanged in the boundary map.

Only accepted kinds 1 (definition) and 3 (non-theorem opaque) qualify for this
new rule. Existing theorem handles retain their separate rule. No axiom is
inserted, no record is overwritten, and no axiom-shaped result is published as
a newly checked definition. Generated kinds 4/5/6, quotient primitives and fixed
foundation axioms retain their existing exact requirements. A concrete owner
definition or opaque with a differing body still refuses even if its type is
identical. A wrong universe/type, unsafe/partial handle, absent warrant or
unbound dependency still refuses. Public visibility alone is not a warrant.

## What can legitimately be claimed

Let K be the actual warranted receiver, and let A be the **selected** authoring
interface, not the owner's whole arbitrary environment. Interpret each bound
constant by its exact accepted counterpart in K. Every handle type must be
preserved, every concrete rule used in A must be valid in K, and every primitive
rule must have the same meaning under the pinned kernel/profile. Under those
premises, induction on the selected derivation transports A's proof into K:
the constant case uses the accepted inhabitant; conversion uses rule
preservation. Removing ordinary delta-reduction rules is conservative for this
direction. An arbitrary local axiom cannot satisfy the interpretation merely
by sharing a name with something in the network.

This is a conditional design argument, not a proved correspondence for every
Lean owner environment. The owner can contain unrelated assumptions, elaborate
unexportable proofs or run untrusted tactics. Consequently source compilation
and missing-unit checks over A remain construction evidence only. Actual
receiver checking against K is mandatory and determines mathematical acceptance.
No failure or unsupported conversion is relabeled as a theorem.

**Primitive qualification is essential.** `Nat.xor` can still reduce by name
even when its owner record is axiom-shaped. The rule is not “abstract handles
never reduce.” Pinned C++ `type_checker::reduce_nat` gives the same standard
operation in A and K, and K's exact fixed basis establishes the matching
standard definition. The selected owner/receiver runtime and primitive profile
must stay pinned. The prior restrictions on `Lean.reduceBool`, `Lean.reduceNat`
and other forbidden evaluator names stay intact. Generated recursors, dependent
projections and literal support do not become abstract by this rule.

## Minimal implementation delta

1. In `OwnerRebind`, introduce a three-way result such as `MatchKind` with
   `theoremInterface`, `abstractDefinition`, `exact`. `matchRow` and
   `matchBasisRow` return it instead of Unit/Bool. Do not change the request
   format or change mode1 into an unqualified type-only policy.
2. For an actual safe `.axiomInfo` and accepted kind1/3 only, compare the exact
   type/universe interface against that accepted row, before the existing
   `BootstrapProbe.screen`/non-theorem exact-record branch. Other cases retain
   current behavior. Keep theorem-specific classification checks rather than
   broadening `theoremPayload` to make everything look like a theorem.
3. Scan the actual type for either handle kind. Concrete records retain body,
   group and rule scans. The request still contains the accepted complete
   non-theorem rows and dependency closure; their existing byte/node bounds and
   controller authentication remain. Missing declarations still use unchanged
   `CheckedExtension.checkBatch` and never its fallback-axiom path.
4. Retain each selected name's matching class (or just the abstract-name set)
   through final target checks. An abstract target's frontend view must remain
   a safe axiom-shaped handle of the same interface. Do not silently accept a
   conflicting concrete frontend record or misclassify it as a theorem. Fixed
   basis targets can reuse their accepted row matcher as before.
5. Add `abstractDefinitions` to `Rebound`; `interfaceMatched` continues to mean
   theorem interfaces only and `exactMatched` remains concrete matches. The
   three counts partition matched names. Add a distinct diagnostic field in
   `OwnerUseCommand`; no acceptance wording or persistent authority follows.
6. `BoundContext` and successor transport need no new trust mode: retain the
   same `(name, exact accepted symbol ID)` map. `SuccessorExport` stops only at
   these bound IDs. Receiver assembly resolves all IDs in its actual accepted
   context and independently checks complete new declaration units unchanged.

Use an explicit trusted policy parameter, not a peer-requested JSON flag:
`DefinitionView := exact | existingAbstract`. Append it to `rebindPrepared`
after the existing optional limits argument, defaulting to `.exact`; preserve
all old three-argument callers. `OwnerUse.run` similarly accepts the policy
with exact default. Keep `#ordinary_use` exact and expose a separately named
`#ordinary_use_abstract` wrapper that selects `.existingAbstract` in pinned
owner source. Both commands retain the sole final environment installation.
This makes the construction compromise explicit without changing any request
byte or silently loosening exact-correspondence callers. No use of the word
`abstract` creates a new acceptance mode.

## Costs, alternatives and decision-changing checks

This avoids demanding private bodies from ordinary public module artifacts or
importing a second private environment. It adds a small match classification and
interface comparison, not a new proof system, axiom scheme or replay campaign.
The prepared requests, projected header identity and all 387 group bytes can
be reused. Header projection and concrete matching are not weakened further.

Acquiring exact missing semantics remains preferable when actual reduction is
needed and a supported import can expose it. Here the name already exists as
a public stub: checked insertion cannot overwrite it, and broad private imports
have already incurred excessive cost. Renaming/reinterpreting a whole affected
library would be a larger change. The proposed construction abstraction is the
smaller principled route, with independent receiver checking as the authority.

Before actual adoption, independently challenge: wrong type/universe; a same-type
but different concrete body; an axiom-shaped generated record; absent exact
accepted identity; successful type-only ordinary use; native `Nat.xor` behavior
under the fixed primitive profile; and independently checked final successor.
Select the smallest source arguments/controls that resolve each uncertainty;
do not repeat the completed projection or full basis-admission campaigns.
