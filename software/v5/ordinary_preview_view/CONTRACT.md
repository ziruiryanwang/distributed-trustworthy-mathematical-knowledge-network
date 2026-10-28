# Offline formal preview: complete display or explicit incompleteness

2026-10-28. Source/theory contract for root reconciliation, not an implementation
or runtime selection. The result is an advisory display of a claim. No new
mathematical acceptance relation, notation inference, natural-language summary,
owner access, native execution, network access or proof replay is introduced.
Root owns the selected-package loader, report wrapper and CLI. This contract
covers the pure view of one current portable type preview.

## Input and existing validation

Root's companion selects the package/PROFILE and one report/path hash explicitly.
It checks the selected source bytes before loading the small inert codec surface.
It reads no paths named inside the report. The original report is retained.
Root canonically encodes `result.preview`. The pure renderer takes those raw
preview bytes plus explicit selected inert codec modules and display limits. It
calls `portable_preview.read_preview` once internally to establish bounded syntax
and its exact reference census; use `ordinary_evidence.name_key` for all name
identity comparisons. The modules are supplied by root's pinned loader, not
selected or dynamically loaded from a report field by the renderer.
The wrapper also compares reconstructed preview byte length/hash and export/record
identity with the selected report fields. This is internal consistency, not new
network evidence or acceptance. A malformed/inconsistent input is refused rather
than rendered as a validated preview. Saved success words are ordinary input data.

The renderer derives freshly validated detached data from those bytes, not a
mutable object whose historical construction is treated as a permanent validation
token. It returns a detached bounded structured view: completion status, complete
type text and legends only on success, identities, limits/counters and any
limitation. Its serializer/display implementation is independent of the report
wrapper/controller. It neither implements a different expression validator nor
asks Lean to load symbols.
The original expression format's metadata erasure means source notation and all
frontend presentation state cannot be recovered. Display the encoded formal type.

## Complete-view notation

The view contains the declaration kind/name, all original ordered universe
parameters, the complete type, exact constant-binding table and binder-occurrence
legend. It identifies the original root and the source node of each displayed
binder. It preserves every universe argument, including an empty argument list
under the explicitly stated empty-list convention. Source names are labels;
display tokens identify references.

- `name#cN` denotes exactly row N of `type_bindings`, with that row's exact
  structured name and SymbolID. Resolve a constant or projection structure by
  `name_key` bytes to row index. Never resolve by printed spelling, normalize a
  name, or reverse-map only by SymbolID: distinct names can share a SymbolID.
  A basis SymbolID need not be an ordinary ExportID or have an inspectable export.
- `hint#bN` denotes one binder occurrence, not an expression node. N is allocated
  in deterministic preorder on encountering a binder, before traversing its
  type. The legend retains that occurrence's source expression node, exact
  original label and binder-information code. Fresh tokens avoid capture even
  when original labels repeat or collide with constants/parameters. Anonymous
  and hygienic labels remain exact in the legend; hints grant no semantics.
- `hint#uN` denotes universe parameter N in the original ordered parameter list.
  Keep unused parameters too. Retain their exact names in the parameter legend.
  Levels are `zero`, `succ(level)`, `max(left,right)`, `imax(left,right)` and
  parameter references. No reordering, simplification or max/imax identification.
- Sorts are `Sort(level)`, never a guessed `Type` spelling. Applications use
  explicit parentheses and left-associated argument lists. Constants with a
  nonempty universe list use `name#cN.{level,...}`; absence of this suffix means
  exactly the empty list. No implicit argument of an application is omitted.
- Universal/lambda binders retain codes 0/default, 1/implicit, 2/strictImplicit
  and 3/instImplicit. The displayed binder delimiters are respectively `(x:T)`,
  `{x:T}`, `{{x:T}}` and `[x:T]`, with this explicit legend; they are display
  syntax, not a claim of compilable Lean source.
- A let explicitly displays its type, value, body and `nondep=0` or `nondep=1`.
  The flag is retained data, not authority for changing scope. A projection
  displays exact structure binding, numeric field index and value expression.
- Nat literals use a bounded exact hexadecimal magnitude form; empty magnitude
  means zero. String literals retain exact UTF-8 via ASCII-escaped string text.
  No potentially huge decimal conversion is needed.

Readable dotted names are hints only. Every exact name in a legend uses typed
components: `str("...") / num(n)`; anonymous is `[]`. Escape strings losslessly
with ASCII escapes, including controls/bidi characters and non-ASCII code points;
do not normalize Unicode. Consequently `str("A.B")` differs from
`str("A") / str("B")`, and `str("1")` differs from `num(1)`. Printable hints
are restricted to ordinary ASCII identifier components; other names use a neutral
hint. Emit a plain text view, not executable text or active markup.

## Scope rule: traverse occurrences, not node aliases

Maintain an ordered environment Gamma of binder-occurrence tokens, oldest first.
At a bound-variable node with index k, print Gamma[len(Gamma)-1-k]; lack of that
entry refuses the complete view. A variable is never looked up by original name.

For lambda/forall, allocate the fresh binder token, render its domain under Gamma,
then render its body under Gamma extended by that token. For let, render type and
value under Gamma and body under the extended environment, regardless of nondep.
Sibling traversals restore the prior environment. Use explicit traversal frames,
not recursion limited by the host language's call stack.

The same DAG node can be reached under distinct binders. Do not memoize a rendered
open expression by node ID or assign it a global textual alias. Each occurrence
is traversed with its actual environment; each binder occurrence gets a fresh
token even when its underlying node was shared. The first version has no scoped
abbreviations, global expression definitions, or reified substitution calculus.

## Finite work and all-or-nothing output

Before expansion, choose finite ceilings for expression occurrences, universe
occurrences, fresh binder tokens, outstanding traversal frames, name/literal
escape work and total emitted UTF-8 bytes. Root's outer input/read limits remain
in force. Suggested first fixed display ceilings are 16,384 expression occurrences,
8,192 universe occurrences, 4,096 binder tokens, 16,384 frames and 65,536 output
bytes; these are choices, not required capacity or measured costs. Escaping and
tables share the output ceiling and explicit charged input-character/byte work.
The source implementation must record the exact selected constants.

Check the relevant counter before every expression/level occurrence expansion,
binder/frame allocation, escape step and append, including legends and parameter
lists. Do not pre-expand trees, compute an exponential expanded-size integer,
recursively concatenate subtree strings, or build an unbounded table/literal and
check its length afterward. A bounded fragment list/byte buffer may be joined once.
Finite input validation is separate from display work; it is not a speed claim.

If any cap is reached, or a valid input has an unsupported display case, discard
the entire partially generated declaration and its partial legends. Return
`TYPE_DISPLAY_INCOMPLETE`, the reason/limits/counters, the exact preview digest,
semantic/unit/export IDs and original root node index. Root's report wrapper adds
the original report digest/provenance; the pure renderer has no report input.
No partial type
or partial symbol table may look like a complete declaration. The root reference
only identifies where the raw type is stored; it is not a global term alias.
The user can inspect the retained raw input or approved ordinary source. There is
no automatic second pass, renewal or larger allowance.

Only a successful whole display returns `TYPE_DISPLAY_COMPLETE` and its view.
This says all displayed syntax and required legends fit, never that the claim is
true, dependencies available, source notation restored, or a proof checked.

## Why the two critical properties hold in principle

**Scope fidelity.** Induct on an occurrence traversal with environment Gamma.
Constants/projections are resolved by exact name keys; levels use the original
parameter order. A bvar selects exactly its de Bruijn distance in Gamma. Domain
and let-value traversals keep Gamma; body traversals extend it by one fresh token.
These are exactly the codec's binding rules. Application and other constructors
retain order and fields. Therefore complete output preserves reference structure
up to the explicit fresh binder labels, whose original labels remain recorded.
This is a display invariant, not kernel checking or a certified pretty-printer.

**Bounded sharing expansion.** Every visited expression and universe occurrence
is charged before adding its descendants; every frame and output step is capped.
Shared DAGs may describe exponentially larger trees, but traversal stops after
the fixed number of permitted occurrences and discards the partial view. Work is
bounded by parsed input processing plus the chosen visit/escape/output ceilings,
and workspace by parsed input plus frame/binder/output ceilings. The argument
does not assert linear time in DAG size for a successful full expansion.

Before implementation, review the complete retained [specimen](SPECIMEN.md) and
these rules. Later focused pure controls should distinguish capture across shared
nodes, all binder codes and let scopes, name/identity collisions, unused universes,
max versus imax, large shared levels, literals and every cap/fallback boundary.
No new theorem, native proof, service or owner operation is warranted.

Source anchors: `ordinary_lean/EXPRESSION-FORMAT.md`,
`ordinary_lean/OriginalExpr.lean::decode`,
`ordinary_lean/ordinary_evidence.py::name_key,_dag_references`,
`ordinary_lean/ordinary_preview.py::_type_census`,
`ordinary_lean/portable_preview.py::read_preview`.
