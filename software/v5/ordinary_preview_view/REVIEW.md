# Preview display: independent design challenge

2026-10-28. Reviewer: query_scaling. Source/theory only. No renderer, validator,
test, theorem, native tool, service or owner database was executed/opened, and no
Git operation was performed. The saved preview JSON and existing codec sources
were read as data. A separate read-only subreview checked name/universe identity.

**PASS for the reconciled source/theory design and hand-derived specimen.**
The complete-only capped traversal is the recommended minimal design. No design
blocker remains after the two wording corrections recorded below. This review
does not qualify renderer implementation or runtime behavior.

Exact reviewed design hashes:

- `CONTRACT.md`: `e559814aea0c79f60510f87a5c65ef0ab7555107555ca480d5db3432de771fcf`.
- `SPECIMEN.md`: `0c04fe688aaf2ce8b815e51dadb57de086686d06aa8e6b1c248bd9353359e5c4`.

## Recommended small boundary

Render the whole advertised type with fresh binder-occurrence tokens and exact
binding/universe legends. If any display limit or unsupported display case is
encountered, discard the partial type and report `TYPE_DISPLAY_INCOMPLETE`, the
exact input identity and original root-node reference. A root reference in this
diagnostic is a reference to saved syntax, not a new mathematical constant.

This avoids a second system of parameterized aliases or scoped abbreviations.
It is preferable to publishing a readable prefix that could hide an important
premise. Completeness must cover the header metadata and the legends needed to
resolve tokens as well as the expression text. A truncated legend cannot leave
an otherwise complete-looking theorem with unresolved names.

The renderer must call the existing `portable_preview.read_preview` on bounded
raw bytes. Its result is advisory; a saved report's success/binding words confer
no new authority. Reuse `ordinary_evidence.name_key` for all exact-name lookup.
The renderer may interpret already validated tags for display, but must not
become an alternative input validator or acceptance path.

## Scope and capture requirements

`ordinary_evidence.py:216-290` validates a backward DAG and a closed root through
its context-depth requirement calculation. That does not give a node a unique
lexical environment: one `bvar 0` node can be shared under different binders.

- Render a bound variable with the token at `environment[-1-index]` for that
  occurrence. Never resolve it by the stored binder-name spelling.
- A lambda/forall domain uses the incoming environment; only its body extends
  the environment. In `forall A, forall x:A, ...`, introducing `x` before its
  domain would mistakenly capture the reference to `A`.
- A let's type and value use the incoming environment; only its body extends it.
  Preserve its `nondep` bit. That bit is not permission to drop the syntactic
  binder or rewrite indices.
- Allocate a fresh display token for every expanded binder occurrence, including
  repeated occurrences of the same binder node. Original binder names remain
  escaped annotations, not variable identities. Constant tokens and universe
  tokens must be syntactically distinguishable from these local tokens.
- Do not cache a rendered expression solely by source node ID. The same open
  node under `x` and `y` would otherwise be printed as the wrong variable. Do not
  lift it into a global alias. Closed-node optimization is unnecessary here.

The existing tag meanings are source-backed in `OriginalExpr.lean:149-161,250-298,
395-434`: default/implicit/strict-implicit/instance-implicit binder information,
lambda versus forall, let's nondependency bit, explicit application, native
literals and projections. Preserve them without inferred notation, reduction,
implicit-argument insertion, binder merging or omitted hypotheses.

## Exact names, references and universes

`ordinary_evidence.name_key` (`:170-203`) preserves typed name segments and their
exact UTF-8 bytes. Examples that a dotted label must not conflate include one
string segment `"A.B"` versus two string segments `"A"`, `"B"`; a string `"1"`
versus numeric segment `1`; canonically distinct Unicode normalization forms;
empty segments; and names containing controls or bidi characters. Escape these
visibly and never normalize, strip or resolve by the pretty label. Binder names
can also be anonymous or outside the semantic-name restrictions.

Every constant and projection structure-name reference must resolve by exact
`name_key` into the validated `type_bindings` row. Keep the row index and full
symbol ID in the legend. Distinct names may have the same symbol ID, so reversing
the map by ID is also incorrect. `portable_preview.py:67-75` already requires
the exact sorted name-key census; the renderer should use that authority.

Keep the complete original ordered universe-parameter list, including unused
parameters. Preserve all constant instance arguments in order and distinguish
level zero, successor, max and imax, including ordered children. Parameter
indices refer to this header's parameter list. `Sort(level)` avoids an accidental
Type/Sort off-by-one. Sources: `ordinary_evidence.py:232-261`,
`ordinary_preview.py:87-95,131-133`, and `OriginalExpr.lean:202-220,333-355`.

Native natural literals are canonical big-endian magnitude bytes, with empty
bytes meaning zero (`OriginalExpr.lean:167-174,415-427`). A bounded explicit hex
spelling avoids constructing a huge decimal integer/string. String literals
need exact, visible escaping rather than interpreted control characters.

## Bounded work before output

The codec permits DAG depth 4,096, beyond ordinary safe Python recursion depth.
Use an explicit traversal/event stack and scoped push/pop operations. Budget
expression occurrences, universe occurrences and binder/frame work before
expansion; a bound on distinct input nodes alone cannot prevent exponential
unfolding. Universes can share sub-DAGs exponentially too.

Charge output bytes before appending escaped names/literals, source-node
references or legend entries. Stream bounded fragments rather than repeatedly
concatenating whole subtree strings. Do not compute an unbounded fully expanded
size before applying the display budget, allocate a string and check afterward,
or repeatedly copy an entire binder environment at each node. The fallback
diagnostic itself must fit a small explicit bound.

These are display budgets in addition to the existing bounded parse/census.
They need not claim mathematical or canonical equality of a rendered string.
Output must remain explicitly non-compilable advisory notation, with input
digest and semantic/unit/export identities available independently of names.

## Independent saved-DAG reading

The saved `dedicated-host-preview01/RESULT.json` has SHA-256
`77065fe33292368d3d4a177c4b836cf0bcf98128b0984a6178168734226c5113`.
Its embedded preview reports 4,798 canonical bytes and digest
`f3fd920019c877c33483c8b82bfa1692e300aad7307008cb70edd97d7c32a435`.
Static inspection finds 75 expression nodes, six universe nodes, root 74,
two universe parameters and eleven exact type bindings.

Manual source decoding yields twelve outer binders: implicit `A` and `S`, then
`observe`, `step`, `effect`, `atomic_law`, `s0`, `s1`, `h0`, `h1`, `p`, `q`.
Their required structure is:

- `A : Sort(succ u)` and `S : Sort(succ v)`;
- `observe : S -> Bool`, `step : A -> S -> S`, `effect : A -> ResetEffects.Mode`;
- `atomic_law`: for every `a:A` and `s:S`, equality at `Bool` between
  `observe(step a s)` and `Mode.eval(effect a)(observe s)`;
- `s0,s1:S`, with `h0` asserting `observe s0 = false` and `h1` asserting
  `observe s1 = true`;
- `p,q : ResetEffects.Plan.{u} A`.

The body is `Iff` between `ContextuallyRefines.{u,v} A S observe step p q` and
`Mode.Refines (summary.{u} A effect p) (summary.{u} A effect q)`. Each equality
constant has universe instance `succ zero`. This paragraph is a reviewer
description, not the proposed exact rendering syntax or a checked theorem.
The final specimen must retain all these binders/premises with exact row/node
references. Omitting the observation witnesses or atomic law would materially
misrepresent the advertised claim.

## Written specimen and reconciliation

Read the author's complete CONTRACT and SPECIMEN. The type text matches the
independent DAG reading above. Its fresh binder tokens `b0` through `b17` occur
in the specified preorder: twelve outer binders and six binders inside their
domains. Their source-node indices, original hygienic labels, binder codes,
universe parameters and all eleven binding-index/name/ID rows agree with the
saved preview. `Eq` has exactly `succ(zero)`; `Plan`/`summary` use `u`, while
`ContextuallyRefines` uses the ordered pair `u,v`. No assumption or application
argument was omitted. All three reported assurance flags remain false.

The specimen is materially easier to inspect than byte-encoded names and raw
DAG indices: it places the two observation witnesses and atomic law beside the
complete conclusion, and exposes the existing inspection binding indices.
That is sufficient practical justification for a small offline renderer. It
is not a measured usefulness result, permission for a body browser or a reason
to rerun mathematics.

Two narrow issues were returned to the author. Type-binding rows must be called
SymbolIDs, since imported basis bindings need not be ordinary ExportIDs or
inspectable exports; the selected declaration's own ExportID is separate. Also,
the pure raw-preview renderer can derive a preview digest but cannot know a
saved report's digest; root's wrapper must compose that report provenance.
Neither requires a new schema authority or a broader renderer.
Both corrections are present in the pinned final design: binding rows use
SymbolID, and the wrapper adds report provenance to preview-derived output.

## Implementation review

**PASS source review of the selected renderer and saved-report wrapper.** Exact
reviewed SHA-256 pins are `render.py`
`3b525d8e42709249196062733290486516b40c7cc1c320e9f3d005718a874352`
and `view_preview.py`
`ccffc03f2138f0e1cca6b64a2df032b5f094592847d01ed8cf30a516fef6b9e5`.
The complete read found no remaining blocker: one existing preview parse,
occurrence-specific binder tokens, persistent scopes, exact name-key bindings,
iterative expression/universe expansion and precharged work/output caps implement
the reconciled contract. Display-cap handling discards the entire type and all
legends. The wrapper pins its five inert codecs and renderer, bounds and checks
the selected saved report, ignores embedded paths, preserves both original and
selected profile provenance and refuses existing output.

The six focused source-authored control groups are in `controls.py`, SHA-256
`d279fadb895dedff841b5a5401eeec57f8f485b2e0919222bfe3c007e9825fd3`;
root independently read this control source and reported no blocker. Their scope
and inputs are recorded in CONTROL-PLAN.md. This checkpoint reports source review
only: neither reviewer execution nor a mathematical, native or network PASS is
claimed. Runtime selection and saved-outcome adoption remain root's separate gates.
