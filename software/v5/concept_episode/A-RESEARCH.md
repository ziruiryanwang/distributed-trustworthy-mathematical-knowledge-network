# Investigator A: private concept-development record

2026-10-24. Source-only investigation; no Lean compilation or project execution.
Canonical guard passed using the documented process-local PowerShell bypass.
This record is not the recipient handoff.

## Disclosed inputs and boundary

Inputs are the task/contract and workspace governance, the Lean 4.34.0 `Init`
source tree, and my prior mathematical knowledge. The required governance reads
include historical project descriptions; I have not opened their linked
mathematical fixtures or used their mathematical statements. Initial combined
governance output was truncated; current GOAL/NOW directions and AGENTS were read
separately. No other investigator output or intended continuation is available.
Direct seed inspection so far: `Init/Data/Function.lean` and searched portions of
`Init/Data/List/Basic.lean` and `Init/Data/List/Lemmas.lean`.

## Candidate search and choice

1. Observation-compatible normalizers: an idempotent map together with an
   observation that it preserves. This risks only renaming a retraction plus a
   commuting diagram; the useful endpoint was not yet distinctive.
2. Commuting constraint repairs: composition is idempotent onto the common fixed
   points. This is familiar and imposes more symmetry than a sequential process
   requires.
3. **Chosen: asymmetric repair calculus.** A repair is an idempotent operation.
   A later repair may follow an earlier one if it preserves the earlier repair's
   fixed points. This supports one-pass composition without assuming commuting
   operations. The key object is the directional compatibility relation and its
   exact interaction with compound repairs, not the renamed idempotent alone.

The motivating mathematical question is how independently specified repairs can
be assembled so that completed constraints remain completed, and what a one-pass
guarantee actually determines. No target theorem was supplied by the coordinator.

## Derived direction and challenges

For idempotents r and s, preservation of r-fixed points by s is equivalent to
`r(s(r(x))) = s(r(x))`. Under exactly this condition, the composite s after r
is idempotent and its fixed points are precisely the intersection of the two
fixed-point sets. Thus a completed prefix can itself serve as the next repair
interface. Preservation of the prefix only requires preserving its intersection,
not each earlier constraint on states outside that intersection.

A second construction uses a finite list of repairs with later operations
preserving earlier fixed points. Induction should show a single run settles all
constraints, repeated runs do nothing, and already settled states are untouched.
This is a sufficient schedule discipline, not an iff characterization of all
successful schedules: a later repair may restore an intermediate violation.

Tempting false variant: mutual compatibility makes order irrelevant. Countermodel
idea: three states, two accepted states and one unresolved state. Two repairs fix
both accepted states but choose different accepted outputs for the unresolved
state. They preserve each other's fixed points, yet the first repair to run
determines the answer. Hence settledness is not a canonical-choice theorem.

A contextual-preservation model on Boolean pairs should also show why a compound
prefix interface can be weaker than pairwise preservation: zeroing both fields
leaves only `(false,false)`; copying the second field into both fields preserves
that conjunction but does not preserve the first-field-zero constraint globally.

## Content and novelty assessment

Idempotents/retractions, invariant preservation, and finite invariant arguments
are established mathematics. This is an independently selected, small synthesis
and interface design within this episode, with no claim of literature novelty.
Its potentially useful contribution is a compositional separation of directional
admissibility, exact joint fixed points, and absence of order-independent choice.
The research task is not satisfied by theorem counts alone; recipient usefulness
and source/transfer costs remain separate questions for actual evidence.

## Current status

`TheoryA.lean` and the standalone `A-HANDOFF.md` are now written. The formal
source covers exact ordered binary composition, a contextual composition
criterion, finite safe schedules, noncanonical choice, and strict contextual
preservation. Source proofs were checked by mathematical reasoning only. The
`follows_iff` reverse implication explicitly transports along `r(x)=x`; `merge`
uses preservation followed by s-idempotence; schedule proofs recurse on lists.
The finite countermodels reduce by constructor cases or decidable equality.

No Lean compiler, `lake`, runtime invocation, proof service, exchange frontend,
or native build has run. No source-level success should be read as kernel
acceptance. Modern-module exposed definitions are intentional for recipient
reduction; generated structure/recursor and list recursion support are known
transfer questions. The source is ready for the coordinator's selected feedback.
