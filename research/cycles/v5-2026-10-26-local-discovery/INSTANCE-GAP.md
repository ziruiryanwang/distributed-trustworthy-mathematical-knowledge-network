# Specialized goals: a real gap, but not a reason to port another fingerprint

2026-10-26. Source-only bounded investigation by `instance_discovery_gap`.
The canonical workspace guard passed. No product import, test, Lean execution,
network request, state operation, Git mutation or paper/shared-ledger edit was
performed. Current handoff is `software/v5/ordinary_release_bundle/ADOPTION.md`.
Local and unpublished remains the user's selected scope. Full v5 is unfinished.

## Decision

**Do not yet add a provider index or automatic generalization adapter.** There is
a precise specialization/selectivity gap in the current ordinary evidence index.
However, the cheapest existing remedy for the concrete discriminator below is a
generalized exact-type query, using the already implemented public interface.
Ordinary local search and approved Loogle providers are additional real
alternatives. Porting the older conclusion fingerprint does not solve the most
informative discriminator: its independent wildcard observations erase the
variable-sharing relation that distinguishes useful commutativity from reflexivity.

This is not a claim that general remote applicability has been solved. It retires
one tempting but presently unjustified next implementation, and specifies the
missing evidence needed to choose between an optional local adapter and a richer
provider access path. No large corpus or native campaign is needed for that choice.

## What the current sources actually support

- `ordinary_formal_query/formal_query.py:109-160` computes the whole declared-type
  structural key. Its fixed profile explicitly preserves all remaining structure
  without substitution or reduction. `query_spec` produces one exact-key query.
- `ordinary_formal_query/discovery/ordinary_export_adapter.py:60-92,132-219`
  supports declaration kind, exact type symbols, result head, binder-domain heads
  and the exact type key. `compile_query` allows at most eight feature conjuncts.
  A symbol in the goal but absent from a general theorem is not a sound mandatory
  condition for finding that theorem.
- `ordinary_query_context/query.py` and the selected `OwnerQueryCommand02.lean`
  already turn an independently supplied ordinary formal type into the bounded
  original-expression DAG and resolve known portable identities. They do not
  require a theorem proof, target theorem name or ExportID. An investigator can
  supply a generalized statement through this interface today.
- The actual current package's `support/discovery/candidate_query.py` retains
  both atomic traversal and opt-in sparse V2 pair access. Pair access reduces
  work for selective intersections of existing features. It cannot separate
  candidates that contain exactly the same requested atomic features.
- `software/runtime/lean-4.34.0-windows/src/lean/Lean/Meta/Tactic/LibrarySearch.lean`
  supplies `libSearchFindDecls` at line 187 and ordinary application search. This
  searches imported declarations. It deliberately drops very broad wildcard
  patterns (`droppedKeys`, lines 164-168), which is a useful existing warning
  about the proposed fallback rather than a missing invention.
- The previously read primary-source audit
  `../v5-2026-10-24-growth-selection/PREEXPORT-TOOLS.md` records Loogle's maintained
  formal matching and configurable LeanSearchClient/lean-lsp-mcp clients. A
  suitable existing provider can be used as advisory discovery before acquisition.
  Its current JSON is not a cryptographically bound corpus answer and its output
  limit does not bound backend work. Those limits do not make the tool absent.

The ordinary definition-body observer is a different existing lane:
`software/v5/discovery/ordinary_body_adapter.py:145-271` strips leading lambdas
and samples a definition body. It is not a theorem-conclusion index. The earlier
`instantiation_discovery/discovery/conclusion_fingerprint.py` does index theorem
conclusions, but belongs to a different representation/profile. Neither source
may silently be relabeled as the current ordinary provider implementation.

## Concrete finite-budget obstruction

Assume shared, exact already known symbols `A : Type` and `op : A -> A -> A`.
The locally approved project also knows `f g : A -> A`. A local goal is

```text
op (f a) (g b) = op (g b) (f a).
```

The investigator need not know the name or portable identity of an external
checked theorem with declared type

```text
T : forall x y : A, op x y = op y x.
```

Consider true but unhelpful-for-this-raw-instance declarations

```text
D_j : forall z_1 ... z_j x y : A, op x y = op x y.
```

Every `D_j` is provable by reflexivity; the unused binders make their whole types
distinct. Choose a small number within the existing expression/telescope bounds,
not an unbounded declaration. `T` is stipulated to have an available valid proof
in the remote library; this source argument does not claim that such a specific
portable corpus has already been exported or measured. A natural operation with
a nontrivial commutativity proof would be needed for a reuse-cost experiment.

All these declaration types have the same non-exact ordinary feature set:
theorem kind; symbols `A`, `op`, `Eq`; binder-domain head `A`; result head `Eq`.
Multiple equal binder heads are deduplicated. Their arbitrary feature pairs
therefore coincide too. The query type closed over the local context contains
`f` and `g` and is not the whole type of `T`. Exact-query failure is not repaired
by asking for `f` and `g`: doing that excludes the desired general theorem.

For a selected honest index snapshot with `B` such non-target entries before
`T` in the visited candidate order and only `B` available candidate examinations,
the existing broad search cannot inspect `T`. This is a permitted conditional
index state, not a claim that a particular hash partition or saved test currently
has that order. Pair access has no selectivity advantage on this family because
the pair intersection is the whole candidate set. Increasing peer count or
repeating the same query cannot establish relevance under the original allowance.

This differs from the completed pair/hot-key audit: that audit had a rare
intersection of broad atomic lists. Here the intersection itself is broad and
all present non-exact features are observationally identical. An index over the
same information cannot recover a distinction that was discarded.

The finite-budget argument proves neither a lower bound against an optimal
mathematical reasoner nor that the goal is hard. It also does not prove that all
existing public alternatives miss: the following alternative decisively matters.

## The simpler existing solution must get credit

An investigator can abstract the repeated compounds `f a` and `g b`, ask the
existing exact interface for

```text
forall x y : A, op x y = op y x,
```

and find `T` in its exact-type bucket if the selected provider covers it and the
bucket fits the budget. No new provider format or code is needed. This query is
derivable from the local goal alone, before inspecting `T`. Actual receipt of a
candidate still requires exact acquisition, checking and normal Lean application;
query generalization supplies no mathematical authority.

For an already imported theorem, `apply?`, `exact?`, explicit source search or a
known theorem name may be cheaper still. A compatible approved Loogle provider
may supply the missing external candidate using its existing pattern machinery.
If the underlying example is ordinary addition, built-in commutativity is an
especially strong baseline; it would be misleading to claim software-enabled
growth from this example merely because one artificial query route misses it.

Thus this is a valid counterexample to the *ordinary atomic/pair/exact-instance
retrieval path*, not to the entire permitted investigator workflow. Converting
that path limitation into a claim of system-wide incapability would be incorrect.

## Why the obvious fingerprint port does not solve it

The older conclusion-fingerprint theorem is useful and should be reused when
applicable. After stripping the telescope it replaces every outer parameter
encountered at or above a sampled path by `STAR`. For the two conclusions

```text
op x y = op y x       versus       op x y = op x y
```

every fixed child path yields the same token: unchanged constructors/constants
until a parameter is reached, and then `STAR` in either expression. Taking more
independent paths does not restore whether the same parameter occurred twice.
The same observation applies to the ordinary body observer's parameter logic.

Hence the prior raw-substitution recall result remains valid, but its fingerprint
cannot reject these reflexive nonmatches. A naive port would add extraction,
posting and query costs without changing this discriminator's candidate count.
The old concrete example `f(f x)=x` versus `f(f x)=f x` tests a different, simpler
constructor distinction and must not be reused to claim this gap is closed.

General pattern matching with consistent substitutions can distinguish these
types: reflexivity cannot instantiate to two syntactically distinct sides.
That fact does not select a new distributed unifier. Existing local/native and
Loogle matching remain the first alternatives, and consistency checking alone
does not supply discharged premises or dependent-type correctness.

## The desired guarantee and the smallest discriminating next evidence

A useful optional matcher would promise only conditional candidate recall:
for a stated supported syntax, a well-scoped substitution from a theorem's
conclusion to a local goal must not be excluded by its prefilter. Actual return
additionally assumes coverage, reachable providers and sufficient budgets.
It should preserve repeated-variable constraints where doing so is justified,
and report that premises/typeclass/conversion obligations remain unchecked.
Neither applicability nor global completeness follows from a matching key.

The query DAG, exact symbol bindings and source type-preview DAG already exist.
The missing choice is not how to serialize them, but which independently chosen
generalizations/matches deserve finite work. Arbitrary binder/premise orders,
dependent abstractions, definitional reduction and hypotheses not visible in the
conclusion make exhaustive generalization impossible as a cheap default.

The smallest decision-changing next artifact is therefore **a source-level
trace for one real supported goal, fixed before seeing the target theorem**, with:

1. The existing local/native and advisory-search alternatives explicitly allowed.
2. A finite list of locally generated generalized exact queries and their order.
3. The target's actual type, showing why this list does or does not include it.
4. A specified comparison budget covering failed queries, bytes, candidate
   inspection and any provider maintenance, not only returned-hit count.

If a few ordinary generalizations solve it, an optional agent recipe is enough;
automatic helper implementation would need repeated scripting/usage evidence.
If the necessary binder/premise pattern cannot reasonably be supplied locally
but a maintained provider matcher already finds it, reuse that matcher under
the existing advisory boundary. Only if a named portable-only corpus/workflow
has no adequate existing alternative, and a proposed index separates its actual
candidate family under a justified full cost budget, should root select a
provider-side successor. Do not require external publication to produce that
evidence; a local saved real goal/corpus may suffice.

No new code or experiment is recommended from the present evidence alone.
In particular, neither another successful old fingerprint fixture nor more
packaging tests would resolve the missing investigator-level decision.

## Prior work reused, not counted as a new result

- `../v5-2026-10-20/INSTANTIATION-DISCOVERY-SEAM.md`: raw capture-avoiding
  substitution key compatibility, independent STAR observations, and fingerprint
  indexing/Lean discrimination-tree precedents.
- `../v5-2026-10-22-native-library/ORDINARY-APPLICABILITY-DESIGN.md`: ordinary
  body-DAG implementation, explicit context wrappers and limits.
- `../v5-2026-10-22-native-library/GROWTH-NEXT-LEVERAGE.md`: existing native
  application machinery, ordinary-library comparator and supported adoption path.
- `../v5-2026-10-24-growth-selection/PREEXPORT-TOOLS.md` and
  `PREEXPORT-SELECTION.md`: actual upstream tooling and prior no-new-client
  payoff decision. No external source was rerequested for this investigation.
- Current sparse candidate source and ordinary formal-query source, read above.

The new contribution is the variable-sharing counterexample and its consequence:
**the evident profile port does not remove this obstruction, while an existing
generalized exact query does.** That is a reason to avoid implementing by inertia,
not a certificate that final v5 discovery or useful growth is complete.
