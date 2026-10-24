# Ordinary formal-contract query source

This development source seam lets a trusted local Lean project ask for a
known formal type without supplying a theorem name, proof or target ExportID.
It is a candidate-search interface, not a prover, acceptance rule, universal
goal matcher or measured useful-growth improvement.

## Local type extraction

Use `OwnerQueryCommand02.lean` as the source for logical module
`OwnerQueryCommand`. The unsuffixed source and first failed compile are preserved
history, not the selected implementation. The current distribution recipe stages
the successor under that logical name.

In a root-selected helper assembly containing the existing `OriginalExpr`
serializer and new `OwnerQueryCommand`:

```lean
import OwnerQueryCommand
universe u
variable {A : Type u} (f : A -> A)
#ordinary_type_query [u] "ABSOLUTE_FRESH_OUTPUT.json" :
  forall x, f (f x) = f x
```

Replace the output with an actual owner-selected absolute fresh path. The
command elaborates the type, closes used section variables with their binder
annotations/order and writes a query-only AST. Explicit universe order must
match the desired contract. Unresolved metas/universes, `sorry`, open expressions
and format limits refuse. No theorem or scratch axiom is added. Owner source,
macros and imports are ordinary executable local code: resource bounds are not
a hostile-source sandbox. Accept output only from the owner's selected clean
execution; a partial file is not a successful extraction.

The type-key pass never reads proof/dependency history. Elaboration can still
perform expensive type conversion and execute local macros; it needs separate
finite process CPU, memory and wall-time limits. No constant or polynomial
elaboration-time claim follows from bounded serialized output.

## Query preparation and existing search

With `formal_query.py` and its existing ordinary helper dependencies selected
on the Python import path:

```python
import formal_query as Q

needed_names = Q.reference_names(native_type_bytes)
# Supply exact, already known portable identities for precisely these names.
# known_binding_bytes is canonical JSON [[originalName, SymbolID], ...],
# in needed_names order; it is data, not a callback or theorem warrant.
query_bytes = Q.bind_native_type(native_type_bytes, known_binding_bytes,
                                semantic_id=selected_semantic_id)
specs = [Q.query_spec(query_bytes)]
```

Submit `specs` to the existing ordinary `find` API in a separately assembled
new-profile package. This helper adds no network operation or autonomous search
strategy. Existing budgets, selected providers, incomplete outcomes and exact
candidate/evidence checks still apply. Type key equality is not acceptance.

Bindings come from already known exact basis/acquired-symbol correspondence.
An ordinary local declaration name is not enough to infer a content-derived
SymbolID. Unknown names or missing/duplicate/extra binding rows refuse; do not
fetch a proof ancestry merely to construct a query. An incorrect caller-supplied
mapping may spoil search but cannot authorize any returned mathematics.

## Exact profile and source assembly

The fresh `discovery/ordinary_export_adapter.py` successor adds one required
`declared-type-key` while preserving the original candidate/locator/evidence
boundaries. Root must select it alongside `formal_query.py`, unchanged discovery
helpers and ordinary codecs in one coherent new assembly. It has a different
feature revision and namespace; old snapshots are not migrated or reinterpreted.
New indexing/storage/maintenance costs must be charged. This source tree is not
an installed or qualified package and does not change a used source file.

The key ignores binder labels and universe labels, preserving ordered universe
positions/arity, exact SymbolIDs and level instances, binder annotations, let
flags, literals, projections and expression structure. It is independent of
node numbering/sharing. There is no reduction, arbitrary equivalence, theorem
instantiation, proof unfolding or new fingerprint engine. Reordered hypotheses,
specializations and definitionally equal formulations may miss. Popular exact
type buckets may remain large. No result establishes global absence.

`#check` already elaborates/displays types; Loogle-style services may already
solve a user's lookup. This seam only exports portable machine-readable queries
to our existing indexes. Ordinary package sharing gets the identical facility.
Use the cheaper appropriate route, rather than claiming a custom-index advantage.

## Adoption boundary

The 42 pure query/preview controls pass independent review. The selected command
and a proof-free dependent-function query compiled successfully; the enclosing
native02 test then failed because its harness used an inappropriate JSON reader
for the fixed foundation inventory. A separate pure saved-output postcheck
passed, without repeating either compile or weakening strict query parsing.
The original failure remains recorded. See the
[independent evidence review](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-FORMAL-QUERY-REVIEW.md).

These results qualify the query extraction/key boundary, not useful discovery,
growth, arbitrary Lean projects or final v5. Coherent public package integration
has its own review and single actual-use check. Do not copy a returned theorem's
type into a supposedly independent query.
