# Transposed correlation filter: one query, at most two source postings

2026-10-26 America/Chicago. Source/theory checkpoint by
`pattern_retrieval_options`, coordinated with `correlation_integration`.
Canonical guard passed and AGENTS.md reread. No runtime, implementation, native
operation, external call, state opening, Git or shared-ledger edit.

## Decision

**The transpose is valid under the same raw-instance coverage assumptions.** It
puts a small finite expansion at indexing time rather than requiring an OR of
separately funded queries. It needs no new search-session protocol. Root's
two-path specialization is sufficient for the existing reflexivity discriminator
and is the proposed default; three paths remain an unselected generalization.

This filter deliberately drops the old constructor/constant/STAR vector. Its
sole information is a necessary equality constraint on selected positions.
It is weaker than the earlier combined-key proposal in some families, cheaper to
integrate, and not yet justified as a broad performance improvement.

## Exact two-path profile

Use this immutable, canonically sorted list of fn/arg-only paths:

```text
0: [arg, fn, arg]
1: [fn, arg, fn, arg]
```

In raw `Eq A (op x y) (op y x)`, these select the right operand's first
argument y and the left operand's first argument x. Profile ordering must be
bound into the feature schema/domain; it is not an informal display convention.

Validate the complete source type, then strip all leading foralls. Validate the
complete query wrapper `forall Gamma, g`, then strip exactly its explicit context
count. Paths never enter binder bodies, so all selected positions have the same
internal binder depth zero. Retain existing format, scope and resource bounds.

The source relation R_s has one nontrivial block `{0,1}` **only if both paths
end exactly at the same stripped term parameter**. Otherwise it is empty. A
parameter encountered before path end contributes no equality; an absent endpoint
contributes none. Do not equate all STARs or all absent endpoints.

Define two complete equivalence partitions of positions:

```text
SEPARATE = [[0], [1]]
EQUAL    = [[0, 1]]
```

They are fixed constants, not arbitrary supplied partitions. The source emits
the feature for every partition E whose equality relation includes R_s:

| Source R_s | Required emitted features |
|---|---|
| Empty | SEPARATE and EQUAL |
| `{0,1}` | EQUAL only |

The query emits exactly one feature. It is EQUAL iff both endpoints exist and
their complete subexpressions are syntactically equal under the fixed equality
profile below. Otherwise it is SEPARATE. Each missing endpoint is treated as
its own unrelated singleton, not a shared sentinel expression. Two missing
endpoints therefore yield SEPARATE, not EQUAL.

The new feature means **a possible exact query endpoint partition**, not an
exact source partition. The source's expansion is intentional under this new
meaning. This differs from the prior combined-key scheme, where adding an empty
relation alias destroyed discrimination. Reusing that scheme's feature domain
would be incorrect; a new explicit profile/domain is required.

## Coverage proof

Assume source `forall Delta, t` and query `forall Gamma, g` pass supported
bounds, use consistent rigid identities, and `g = sigma(t)` as raw syntax under
one simultaneous capture-avoiding substitution scoped in Gamma and consistent
universe instantiation. Display labels can be ignored as specified below.

If R_s is empty, the source is indexed under both possible query partitions;
the query's unique partition therefore finds its feature.

If R_s contains `{0,1}`, both source paths reach the same parameter a exactly
at their endpoints. The paths traverse only rigid application edges, which raw
substitution preserves, and enter no binder. Both query endpoints therefore
exist and equal the same sigma(a), with identical surrounding scope and universe
interpretation. The query emits EQUAL, which the source includes.

Thus the source's emitted feature family always contains the query's unique
feature. This is a **key-coverage** theorem, not evidence that sigma exists or
satisfies dependent parameter types, hypotheses or instance obligations.

Actual retrieval additionally requires correct profile extraction/indexing,
reachable selected providers and snapshots, sufficient budgets/pages, and no
provider omission. Returned membership proofs do not establish those conditions.
No automatic goal-derived symbol/head conjunct is part of the theorem: substitution
can introduce symbols or heads absent from the general source. Optional caller
conjuncts deliberately narrow coverage and require separate justification.

## Equality, missing paths and safe bounds

Compare endpoint syntax using hash-consed structural DAG keys, not node identity,
display text or head tokens. The equality profile ignores binder display names
and universe-parameter labels but retains ordered universe positions, exact
level syntax, portable constants, bvar indices, binder annotations, let flags,
literal values and projection metadata. Within one query its context is fixed.
No DAG-to-tree expansion, proof-body inspection, ancestor fetching or conversion
is necessary. Same terms with different DAG sharing must compare equal.

Endpoint subterms may contain internal lambdas/foralls/lets; those are part of
the compared syntax. The selected paths do not cross them, so inserted terms
do not receive different enclosing shifts. This is why no capture counterexample
arises. Extending to body edges requires a new argument.

A missing query endpoint cannot correspond to a direct source parameter endpoint
under the coverage premise: all preceding rigid application edges remain. Treating
missing endpoints as distinct singletons is consequently safe. A repeated source
parameter encountered *before* the path ends supplies no such premise and must
not constrain the relation.

Strict collision-resolving structural interning establishes actual syntax equality;
digest-only comparison needs its stated collision assumption. A digest collision
can merge unequal query terms and weaken rejection, not remove raw-instance
coverage. Truncated or incomplete equality computation must refuse or return an
explicit incomplete outcome, never silently claim inequality: false inequality
could omit a source requiring EQUAL.

## Discriminator and important weakness

For query `op (f a) (g b) = op (g b) (f a)`, the endpoints are `g b` and `f a`.
If syntactically unequal, its query key is SEPARATE. A commutativity conclusion
has distinct endpoint parameters y and x, so emits both keys and survives.
A reflexivity conclusion has x at both positions, emits EQUAL only, and is
excluded. Leading unused parameters or proof premises do not alter this argument
provided the chosen conclusions/endpoint bindings remain as stated. This does
not certify that any hidden premises are dischargeable.

Conversely **every source without this repeated-parameter constraint gets both
keys**. Distinct rigid constants, absent paths, unrelated structure, no parameters
or different parameter positions all count as unconstrained here. An EQUAL query
matches every indexed source on the correlation feature alone. For SEPARATE the
filter can remove only this particular repeated-parameter family. General
relevance still relies on optional selective context and actual application.

## Costs and feature capacity

Source extraction adds at most the telescope length plus nine path-position
visits (path lengths three and four, including endpoints), after full validated
type parsing. It groups two parameter indices and emits one or two postings.
It never reads a proof or dependency history.

Query equality can touch a substantial part of the supplied type DAG. A bottom-up
pass retains O(N) node/level keys and charges all bounded fields/bytes; actual
hash-table/string/comparison costs and peak memory remain implementation costs.
The public query is one existing conjunctive find, so no OR session, query rotation
or union-acquisition lifecycle is introduced. Provider/partition fanout and all
existing shared budgets remain unchanged, not eliminated.

With the current 128-feature cap, reserve capacity for **all required** new keys:
two for unconstrained sources, one for constrained sources. If the complete
feature set exceeds the cap, refuse the record for this profile; never omit a
required key. This is an explicit coverage limit. New namespace/reindexing and
coexisting old-profile postings cost real storage and maintenance; counting only
two new hashes understates deployment cost.

For the unselected three-path generalization, emit every partition E coarser than
R_s: at most Bell(3)=5 keys; empty R_s emits five, a pair emits two, a triple one.
The query selects one exact partition with each absent endpoint a distinct
singleton. The proof is the same relation inclusion `R_s subset E_g`. This is
not authorization to add the third path or five-feature overhead by default.

## Payoff and stopping rule

The transpose trades up to two source postings for one query and loses token
selectivity. It is cheaper than introducing a new OR protocol, but can still be
worse than existing search. The supplied example is solved by the already
supported generalized exact query; approved Lean/Loogle remain allowed comparators.

Let J include incremental construction/reindexing, M maintenance/holding, and
F(q) the complete new query/application cost. Let O(q) be the actually available
optimized alternative including exact generalization and ordinary library tools.
An amortized benefit requires `sum_q (O(q)-F(q)) > J+M`. Candidate-count reduction
alone supplies none of these whole-cost constants. A synthetic family proves
discrimination, not real useful growth or a decentralization-specific advantage.

The source contract may proceed only by root selection with a concrete useful
portable workflow. If that workflow needs an EQUAL query, lacks this repeated
parameter distractor class, or existing exact queries already solve it cheaply,
this filter's marginal payoff can be negligible. No new general matcher, tree,
cryptographic proof or large-scale campaign follows from this theoretical result.
