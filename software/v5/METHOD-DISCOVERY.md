# Find reusable methods, not only an exact answer

This additive guide connects the existing query companions to existing
known-symbol discovery. It adds no command, matcher or mathematical acceptance
rule. The [current investigator handoff](ordinary_investigator_bundle/ADOPTION.md)
links the authoritative extracted guide for package/runtime selection and
operation checks. Its sealed source
archive is unchanged and does not include this later supplement.

## Choose the question you are asking the index

The query companions' `SPECS.json` contains one **exact declared-type key**.
Use it when looking for that whole type. A general method may instead have extra
parameters, unfamiliar hypotheses or a different conclusion. Its whole type
will not generally equal your goal's type, even when the method can help prove
the goal. An empty exact search does not exclude such a method.

For related methods, search for one or two deliberately chosen **known concepts**
in their declared types. You need not know a candidate's name, ID or full type.
The existing index exposes explicit constants/projections anywhere in the type,
including hypotheses, not just its conclusion. Finding a matching type still
does not establish applicability or truth.

This is a choice between existing queries, not an automatic fallback loop.
Ordinary approved Lean/library search remains a good first option. Do not fund a
network search merely because a query file exists.

## Select an actual known binding

Use the successful [fixed-basis or received-vocabulary query](ordinary_investigator_bundle/guides/QUESTIONS.md)
you already selected. Do not rerun it merely to choose a different feature.
Require its exit-zero terminal `RESULT.json` with `ok:true` and
`BASIS_QUERY_READY` or `ANCHOR_QUERY_READY`; the latter also requires
`owner_handles_closed:true`. Apply the original guide's complete output and
closure checks. A worker report or pending result is insufficient.

Read the actual `BINDINGS.json` after matching its byte length and SHA-256 to
`RESULT.json.files["BINDINGS.json"]`. Retain the result's approved
`profile_sha256`, `interpretation` and `namespace`. Both companions use this shape:

```text
BINDINGS.json = [
  [structuredName, portableSymbolID],
  ...
]
```

For a deliberately selected zero-based row `i`:

| Field | Use |
|---|---|
| `BINDINGS[i][0]` | Identify the known concept by its exact structured name. |
| `BINDINGS[i][1]` | Copy this complete value unchanged into `symbol_id` below. |

Structured names are arrays of components: a string component is
`[0,{"$bytes":[UTF-8 byte integers]}]`; a numeric component is `[1,unsignedInteger]`.
A dotted display name is only a reading aid, not a replacement identity. The
bindings enumerate references in this particular query's AST, **not** every
declaration in the basis, owner context or registered module chain. If the wanted
concept is absent, do not invent a row or borrow an unrelated result's ID. Select
an actual known binding from a supported public source first.

Choose concepts you expect a useful candidate to mention explicitly. A particular
relation, operation or structure is often more informative than ubiquitous
`Eq`, `And` or `List`. Do not select every reference automatically: specializing a
general theorem can introduce symbols absent from its original type. Additional
symbol requirements can therefore discard useful candidates.

## Replace the exact specs with a small symbol query

In your existing `find` preparation request, **replace the entire `specs` array**
with the following shape. The placeholder must be replaced with the actual
64-character lowercase value from the selected binding; it is not runnable input.

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

Optionally add a second `type-symbol` entry from another deliberately chosen
binding. This means **both symbols occur in the same declared type**, not either
symbol, a connection through proof bodies, or successful theorem application.
If you want only theorems, you may also add:

```json
{"tag":"declaration-kind","value":"theorem"}
```

Omit that restriction when definitions or other declaration kinds are relevant.
There may be at most eight feature specifications in one query. This recipe
uses only one/two symbols and an optional kind.

**Do not append these entries to the original `SPECS.json`.** All specifications
are conjoined; retaining its `declared-type-key` still demands the exact whole
type and defeats this broader search. Preserve original query outputs unchanged;
the replacement belongs in a separately selected request.

Copy the binding value, not a UnitID, AnchorID, type key, feature hash or arbitrary
candidate theorem ID. A received concept's portable symbol may equal that exact
concept's ExportID; a fixed-basis symbol uses a different derivation. Neither
case permits guessing an ID from its name.

The current inert kit supports type symbols, object/declaration kinds and exact
declared-type keys. The direct public API additionally accepts result-head and
binder-domain-head specifications, but the kit does not: do not put those forms
into this recipe or weaken the selector to accept them. No head query is needed
for the known-symbol route.

## Use the existing bounded discovery and checking route

Keep the explicit contacts/providers, approval policy, finite limits, offer and
page settings from the [network request guide](ordinary_network_kit/START-HERE.md).
Use `ordinary_investigator_bundle/prepare_selected.py` and the same approved final
package/profile, overriding that older guide's historical package/selector paths.
Preparation produces inert inputs only; launch through the existing bounded
`run.py` route with fresh diagnostics/output and require its full closure checks.

`atomic-v1` is sufficient and remains the default. Optional `sparse-v2` can use a
provider's already configured pair access path for a two-symbol conjunction;
without a suitable pair it traverses atomically within the same V2 allowance.
It adds no semantic meaning or recall guarantee, and an unsupported V2 provider
does not authorize an automatic V1 retry. Do not create/reindex a provider merely
to use this recipe.

For `directory-find`, use the same replacement `specs`. Its explicitly selected
`routes` must be nonempty subsets of those **new** specs and must have matching
directory registrations. Do not retain a route containing the old exact-type
key. Directories suggest contacts; they do not promise coverage or renew egress
authority. Follow the existing combined directory/search budget.

The original companion `RESULT.features` describes its **exact-type** query.
It is not the feature list for this new symbol query and must not be copied into
a provider pair configuration. That configuration requires separately compiled
atomic feature IDs for the new symbol specs in the selected namespace; the
existing find report exposes its compiled features. Pair setup is a separate
provider decision, not part of this reader recipe.

Inspect the actual find report's matches, errors, truncation and charged budgets.
Choose a candidate only from a returned record; do not prefill a desired remote
theorem ID. Follow the existing explicit preview, optional definition inspection,
and receive/intake steps. For prepared preview/receive, use the actual same-profile
find report and selected `match_index`, not a reconstructed report or guessed
endpoint. Independently approve retrieval contacts and dependency policy.

Read every hypothesis in the preview. A useful method may expose assumptions you
did not know to ask for; determine whether you can prove them in your actual
context or need a different method. Acquire/check the exact mathematics before
using it as warranted input, then perform ordinary Lean application, premise
discharge and final proof checking through the supported contribution route.
Search membership, preview binding and a matching symbol do not perform these
steps. Return useful checked consequences using the
[existing continuation guide](ordinary_investigator_bundle/guides/CONTINUE.md).

## Scope and stopping rule

This route exposes a neighborhood of explicitly shared vocabulary. It can miss
methods whose relevance requires instantiation, unfolding, a representation
bridge, a body-only relationship or an unfamiliar concept. Broad popular symbols,
unavailable providers and finite candidate prefixes can also hide useful work.
Sparse access changes local index work, not these semantic limits. The query is
not general unification or a search for all mathematically equivalent statements.

Do not infer absence from no hit, exhaustively broaden queries, or automatically
repeat failed searches. Each further operation needs an explicit choice within
the investigator's remaining aggregate budget; fresh per-command limits do not
refund prior work. Include failed discovery, inspection, cold adoption, local
application, publication and custody costs when judging usefulness.

Stop when an applicable method is selected, the finite exploration allocation is
spent, or ordinary local work is the better route. This recipe enables an
existing capability; it establishes no speedup, novelty, complete recall or
large-network coverage. Everything remains local/unpublished and the license
remains undecided.
