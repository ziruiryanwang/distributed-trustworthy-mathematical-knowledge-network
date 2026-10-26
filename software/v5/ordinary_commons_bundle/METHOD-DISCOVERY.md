# Find reusable methods, not only an exact answer

This guide connects existing query companions to existing known-symbol search.
It adds no matcher, command, retry loop or mathematical acceptance rule. The
[current root README](../../README.md) controls source approval and the selected
package/PROFILE/selector. This guide is included in that source distribution;
no external supplement or project-specific adoption report is required.

## Choose what to ask the index

Query companions' `SPECS.json` contains an **exact declared-type key**. Use it
when you want that whole type. A reusable method may have additional parameters,
unfamiliar assumptions or a different conclusion; its whole type need not equal
your goal even if it helps solve it. An empty exact search does not exclude it.

Instead, deliberately choose one or two **known concepts** likely to occur in a
useful method's declared type. You need not know the candidate name, ID or whole
type. Existing type-symbol indexing includes explicit constants/projections in
hypotheses as well as conclusions. Matching a symbol proves neither relevance,
applicability nor mathematical truth. Approved ordinary Lean/library search is
often a good first route; a query file alone is no reason to fund network search.

## Use actual known vocabulary

Use a successful [fixed-basis or received-vocabulary query](ordinary_investigator_bundle/guides/QUESTIONS.md)
already selected for the actual package/PROFILE. Do not rerun it merely to choose
a different feature. Require exit zero and terminal `RESULT.json` with `ok:true`
and `BASIS_QUERY_READY` or `ANCHOR_QUERY_READY`; the latter also requires
`owner_handles_closed:true`. Keep the original complete output/closure checks.
A worker report or pending result is not sufficient.

Match `BINDINGS.json`'s byte length/SHA-256 against `RESULT.json.files["BINDINGS.json"]`
before reading it. Retain the selected `profile_sha256`, `interpretation` and
`namespace`. Both companions produce:

```text
BINDINGS.json = [[structuredName, portableSymbolID], ...]
```

For a deliberately chosen row `i`, `BINDINGS[i][0]` identifies the known concept;
copy the complete `BINDINGS[i][1]` unchanged into `symbol_id`. Structured names
contain components: strings are `[0,{"$bytes":[UTF-8 byte integers]}]`, numbers
are `[1,unsignedInteger]`. Dotted display spelling does not replace identity.

These bindings enumerate references in this particular question's AST, not all
declarations in the basis, owner or registered module chain. If your intended
concept is absent, select an actual known binding from a supported public source
first; never invent a row or borrow an unrelated result's ID.

A particular relation, operation or structure usually filters better than `Eq`,
`And` or `List`. Do not select every reference automatically. Instantiating a
general method can introduce symbols absent from its original declared type;
requiring those symbols would discard the useful general method.

## Replace the whole exact-type query

In the existing `find` preparation request, **replace the entire `specs` array**
with this shape using the actual 64-character lowercase binding value:

```json
[
  {
    "tag":"type-symbol",
    "symbol":{
      "kind":"portable-symbol",
      "symbol_id":"COPY_THE_SELECTED_BINDINGS_ROW_SECOND_VALUE"
    }
  }
]
```

Optionally add a second type-symbol specification from another selected binding.
This asks that **both occur in the same declared type**, not either symbol,
proof-body relatedness, connected theorems or successful application. If only
theorems are relevant, optionally add:

```json
{"tag":"declaration-kind","value":"theorem"}
```

Omit this restriction when definitions or other declarations could help. At most
eight feature specifications are allowed; this recipe uses one/two symbols and
optionally a kind. Do not append them to the original `SPECS.json`: all features
are conjoined, so retaining `declared-type-key` still requires exact whole-type
equality. Preserve original outputs; edit only a separately selected request.

A binding is not an arbitrary UnitID, AnchorID, feature hash or theorem ID. A
received concept's portable symbol can equal its exact ExportID; fixed-basis
symbols have another derivation. Neither permits deriving a guessed ID from
a human-readable name. The kit supports type-symbol, object/declaration-kind
and exact declared-type queries. Head features accepted by the direct API are
not accepted by this kit; do not add those forms or relax its selector.

## Discover and check within one allocation

Keep the explicit contacts/providers, approval policy and finite limits from the
[network request guide](ordinary_network_kit/START-HERE.md). For the current
multi-source package, use
`software/v5/ordinary_multi_source_package/prepare_selected.py`, as shown by the
root README, with the actual selected final package and PROFILE. An intentionally
retained exact-module-only package uses its matching investigator selector.
Never mix interfaces or rewrite reports to change their PROFILE.

Preparation produces inert inputs only. Launch through the existing bounded
`run.py` route with fresh diagnostics/output and all complete closure checks.
`atomic-v1` is sufficient and remains the default. Optional `sparse-v2` can use
an already configured pair path for two symbols; absent a suitable pair, it
traverses atomically within the same V2 allowance. Sparse access changes index
work, not meaning or recall. An unsupported V2 provider does not authorize a V1
retry, and this recipe does not require creating/reindexing a provider.

For `directory-find`, replace `specs` the same way. Its explicit `routes` must be
nonempty subsets of the **new** specifications with corresponding directory
registrations. Do not retain a route containing the old exact-type key. Directory
contacts are hints, not coverage or renewed egress authority. Keep the combined
directory/search budget.

The original companion `RESULT.features` describes its original exact-type query,
not the replacement symbol query. Do not reuse it as pair-configuration features.
The existing find report exposes the newly compiled atomic feature IDs for the
selected namespace; optional provider pair setup is a separate provider decision.

Inspect actual matches, errors, truncation and charged budgets. Choose from a
returned record, not a prefilled desired theorem ID. Follow explicit preview,
optional definition inspection and receive/intake. Prepared preview/receive use
the actual same-PROFILE find report and `match_index`, not a reconstructed report.
Separately approve retrieval contacts and dependency policy. Multiple suppliers
cannot repair an unavailable required preview or make local checking unnecessary.

Read every hypothesis. Decide whether your actual local context can discharge
it or another candidate is needed. Acquire and independently check the exact
mathematics before treating it as warranted input. Then use ordinary Lean
application, premise discharge and final checking through the supported
contribution route. Search membership and preview binding do not perform those
steps. Return checked consequences through
[the continuation guide](ordinary_investigator_bundle/guides/CONTINUE.md), with
the root README's current package/selector overrides.

## Limits and stopping rule

This route explores explicitly shared vocabulary. It can miss a method whose
usefulness requires instantiation, unfolding, a representation bridge, a body-only
relationship or an unfamiliar concept. Popular symbols, unavailable providers
and finite result prefixes also hide useful work. This is not general unification
or complete search over mathematical equivalence.

An empty result is not proof of absence. Do not broaden exhaustively or repeat
failures automatically. Each additional search/inspection needs a deliberate
choice within the remaining aggregate exploration budget; fresh command ceilings
do not refund earlier costs. Count failed discovery, inspection, cold acceptance,
local application, publication and custody when judging a reuse strategy.

Stop when a useful method is selected, the finite allocation is spent, or ordinary
local work has better expected payoff. These existing tools enable investigation;
this guide establishes no speedup, novelty or large-network recall guarantee.
Local agents remain free to introduce new concepts and theories, independent of
any global task list or interpretation of human intent.
