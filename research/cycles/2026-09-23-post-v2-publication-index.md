# Post-v2 diagnosis: publication TYPE indexing

Date: 2026-09-23. Author: `post_handoff_continuity_gap`.
Disposition: **STATIC_DIAGNOSIS_AND_PROPOSED_CONTRACT_ONLY**.

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
The workspace guard passed. Source13 and the delivered v2 are frozen; no
product edit, product/native execution, new source selection or repeated audit
was performed for this note. This is the assigned bounded diagnosis, not an
implementation pass or mathematical acceptance claim.

## Central obstacle and smallest consequential intervention

The original source13 Count theorem passed the source/canonical/native/inverse
path, but publication refused its natural-literal TYPE node. The successful v2
continuation changed the statement's spelling to explicit constructors. That
was a valid source-level workaround, not a repair to the commons' ability to
publish the originally accepted exact statement.

The obstacle is in derived metadata, not the canonical mathematical language.
`py/source_codec.py:370` already validates and canonically rebuilds expression
tags 0 through 9. `py/symbol_index.py:72` separately rejects every projection
callback and then all tags outside 0 through 5. Its group-root closing callback
at line 182 also rejects every projection. `Checker.metadata` at
`py/checking.py:260` converts any such refusal into `CANDIDATE_TYPE_FRAGMENT`.

Proposed minimum: extend only the raw TYPE-symbol traversal and its reference
callback to cover the already represented expression constructors. Do not
normalize, unfold, beta/zeta-reduce, alter source capture, change the foundation,
weaken native checking, change CIDs, or invent equivalence classes. Keep all
resource ceilings. Update the public API's exact-symbol contract and relevant
asset binding in a separately selected successor, if root chooses to implement.

The simpler source rewrite remains usable for some expressions but cannot be
the general contract: it changes exact statement identity and asks every agent
to accommodate a metadata limitation after spending native submission work.

## Existing support, precisely separated

| Constructor | Canonical validation already present | Proposed index treatment |
|---|---|---|
| 0, bound variable | Closed-root/scope calculation | Leaf, no symbol |
| 1, sort | Universe DAG and parameter checks | Leaf, no symbol |
| 2, constant | External reference callback and universe vector | Record exact reference, as now |
| 3, application | Both backward child edges | Visit function then argument, as now |
| 4, lambda | Domain/body and binder scope | Visit domain then body, as now |
| 5, forall | Domain/body and binder scope | Visit domain then body, as now |
| 6, let | Type, value and body; binder closes body only | Visit **all three** in type/value/body order |
| 7, natural literal | Byte magnitude, no leading zero, size bound | Leaf, no invented constant key |
| 8, projection | Structure reference, field index, target child | Record exact structure reference, then visit target |
| 9, string literal | Strict UTF-8 bytes and size bound | Leaf, no invented constant key |

Canonical validation also rejects unknown tags, malformed arrays, booleans as
integers, forward/invalid edges, free bound variables, invalid levels, duplicate
or unreachable/noncanonical DAG nodes, and invalid reference encodings. Retain
`transform_dag` and the exact `checked == dag` requirement; extending extraction
must not become a substitute validator.

Important restriction: the native decoder and `AgentReplayCore.expandDag`
represent tag 9, but `AgentReplayCore.collectExtension` at line 141 explicitly
refuses new external string literals with
`INITIAL_EXTERNAL_STRING_LITERAL_UNSUPPORTED`. Handling tag 9 in the index does
**not** enable or qualify ordinary-source string-literal publication. That
source-capture boundary stays unchanged. Similarly, group-local projections
are refused by source compilation, canonical planning and native export; this
proposal does not add them.

The full bounded canonical TYPE grammar is wider than the actually qualified
source/publication envelope. Other unchanged restrictions include eligible root
kinds, explicit theorem telescopes, first-original-type group metadata,
canonical/package size, symbol/occurrence/depth limits and downstream offer/page
limits. Do not summarize the extension as “every Lean theorem can publish.”

## Proposed formal extraction contract

Let `D` be a canonical closed effective TYPE DAG under universe arity `u` and
one configured foundation `F`, accepted by the existing structural validator.
Let `T(D)` be its rooted expression occurrence tree: a shared child is visited
once per incoming occurrence, not merely once per unique DAG node. Define an
ordered sequence `R(D)` by preorder traversal:

- A constant contributes its exact encoded external reference.
- A projection contributes its exact encoded structure reference, then visits
  its target.
- Application, lambda and forall visit their existing ordered children.
- A let visits its type, value and body, including a value unused by the body.
- Variables, sorts and literals contribute no references.

`symbols(D)` is first-occurrence deduplication of `R(D)`. `symbol_keys(D)` uses
the existing canonical encoding; the row stores the existing sorted unique
keys. Retain exact group selectors, not merely their GroupID. Projection field
indices are not separate symbol keys: the existing query language asks whether
a reference occurs, not which field is projected.

Required guarantees, conditional on successful bounded extraction:

1. **Raw-reference completeness:** every explicit external reference occurring
   in the TYPE syntax appears in the result, including references found only
   in a let value/type/body or a projection's structure slot/target.
2. **Raw-reference soundness:** every returned key occurs in one of those
   explicit reference slots. No implicit runtime declaration, proof/body
   dependency, unfolded definition, human name or semantic equivalent is added.
3. **Identity preservation:** input DAG, mathematical payloads and typed IDs are
   unchanged. Group first-type closing performs only its existing local-type
   reference substitution; accepting additional constructors changes neither
   that substitution nor the derivative type-CID formula.
4. **Legacy equality:** for every previously successful input, the **entire**
   extraction and formal metadata output remains equal, including symbol order,
   sorted keys, occurrence count, maximum depth, distinct count,
   `normalization: NONE` and `native_acceptance: false`.
5. **Fail-closed boundedness:** exceeding any bound returns no successful partial
   symbol list. Existing inclusive limits remain 4,096 occurrences, root-relative
   expression depth 64 and 32 distinct symbols. Keep the same work-counting rule
   for shared subexpressions and the same old-domain failure behavior.

Proof obligation for (1)-(2): induction over the finite rooted occurrence tree.
The additional cases are: let is the ordered union of all three child walks;
projection adds exactly its own structure slot before the target walk; literal
adds the empty sequence. Canonical backward edges make the tree finite; bounded
traversal is a partial implementation that returns success only after every
occurrence has been processed. Deduplication preserves the underlying set.
This is a proposed argument, not a machine-checked theorem or executed result.

This is **not dependency-closure completeness**. A numeral denotes a Lean
primitive but contains no explicit `Nat` reference slot. Native support already
accounts for literal staging dependencies (`BootstrapSupport.makeUnit` injects
`Nat` and string roots). The index must neither erase those package dependencies
nor pretend that raw TYPE-symbol search enumerates them. Keeping a literal as a
leaf therefore does not hide explicit syntax; adding synthetic `Nat`/`String`
keys would change this index's meaning. Likewise, not reducing a let is important:
zeta-reduction could erase the only syntactic occurrence of a dependency.

### Projection validation and group closing

The current `_ref` validates general external reference framing, not projection
eligibility. It must not be used unchanged as the whole projection callback.
For a projection, require:

`ref.tag == 0` **or** `ref.tag == 3 and ref.selector.kind == 0`.

Then retain all existing `_ref` checks. Reject definition, theorem, opaque,
constructor, main-recursion, auxiliary-recursion, source-name, witness and local
references in projection structure position. Native/canonical package checking
still owns actual membership, structure suitability and field correctness; the
symbol helper cannot infer those facts merely from a seed index or GroupID.

The group-root closing callback must apply that same external projection
restriction. It may continue mapping nonprojection `[5,i]` to the exact
`[3,GroupID,[0,i]]` after range checking, but must continue refusing projection
`[5,i]`. A group may contain a projection of an already external group; this is
different from allowing its own group-local type as a projection structure.

## Actual downstream path and consequences

`source_codec.read_package` checks the exact root closure and calls `make_plan`.
This validates canonical references/closure, but does not itself grant native
mathematical acceptance. `Checker.offer` can derive metadata for an inert
acquisition before the independent native `admit` stage. The extraction helper's
documentation should not imply that every caller has already performed native
acceptance; it is a structural metadata function with `native_acceptance: false`.

The relevant consumers are:

| Consumer | Uses of extraction | Consequence for a safe extension |
|---|---|---|
| `Checker.publication` | Rechecks artifact evidence, derives metadata, binds final actual description | Original valid TYPE may become publishable; proof policy unchanged |
| `Checker.offer` / peer acquire | Re-derives complete metadata from received package | Incoming metadata is not trusted merely because peer advertised it |
| `Checker.admit` | Re-derives and compares descriptor, metadata and keys before native stage | Keep exact comparison; no “ignore trace” bypass |
| `peer_node.revalidate` / exact reuse | Compares full stored metadata and keys | Do not rewrite an old entry under the same descriptor |
| `ControlStore.append` | Stores sorted keys in `(provider,symbol_key,sequence)` postings | No schema change needed for unchanged key representation |
| Public local `find` / `preview` | Reads stored metadata/postings, one optional exact key | New keys become locally searchable; this is not proof acceptance |
| `peer_wire.validate_entry` / peer catalogs | Checks formal-field framing, not TYPE grammar | New syntax can be advertised to an old peer before later safe refusal |

The standalone `symbol_index.find` implements local `MENTIONS_ALL` over its own
bounded snapshot helper. The product's persistent public local `find` instead
uses `storage.py` and one optional exact `symbol_key`; remote `peer_find` is
bounded catalog enumeration without a symbol predicate. Do not promise a new
remote or multi-key search feature merely by extending the extractor.

## Version and compatibility decision

No mathematical schema, FoundationID, descriptor schema, key encoding, SQLite
schema, configuration grammar or peer framing change is intrinsically required
for a **strictly additive support-domain extension with legacy output equality**.
The descriptor CID does not include an extractor version; preserving old
metadata exactly is therefore a release requirement, not cosmetic compatibility.

Expected cross-version behavior, requiring focused verification before claims:

- New software derives byte-identical metadata for an old-supported package.
  Old and new peers can exchange that common subset subject to ordinary limits.
- Old software may list a newly supported candidate because wire framing does
  not validate TYPE syntax. Its `peer_acquire`/`offer` subsequently refuses the
  unsupported type before the P1 append or native head change. No new-grammar
  result may be presented as having been mathematically accepted by an old peer.
- A future peer that computes different symbols/order/trace for the **same**
  descriptor will safely conflict under exact metadata comparison. Avoid that
  incompatibility now; if semantics ever change on the shared successful domain,
  use a deliberately specified metadata/profile version instead of weakening
  comparisons or silently reindexing historical entries.

The chosen new source and asset hashes necessarily change. Existing configured
nodes pin those files and persist their configuration identity; unchanged grammar
does **not** authorize patching a live installation or migrating its state.
Use a fresh selected source/install/allocation unless a separate migration is
designed. This note selects neither a new source cut nor a migration.

## Small falsifiable follow-up, if selected

One focused native-free contract suite should cover:

- Exact predecessor equality on old successful TYPEs, including full trace and
  metadata, theorem/definition/group roots and complete group selectors.
- Natural and UTF-8 literal leaves, malformed natural encodings/UTF-8, and the
  explicit distinction between index grammar and the unchanged source string
  refusal.
- A let whose three branches each contain a distinguishable reference, including
  an unused value; shared nodes exercise occurrence counting rather than a
  unique-node shortcut.
- A projection with a key present only in its structure slot plus a different
  target-only key; valid seed/group-type references and each forbidden reference
  category; external projection in a group first TYPE versus refused local one.
- Existing inclusive occurrence/depth/symbol ceilings, unknown tags and canonical
  structure refusals. No partial successful keys on refusal.
- Real metadata consumers: exact advertised/stored metadata equality; tampering
  with a projection-only key or let-only key refuses; local postings expose the
  expected keys; old-domain cross-version metadata remains identical.

Then one bounded ordinary-source mathematical publication/acquisition/admission
case must reproduce the **original literal-bearing statement**, not its v2
constructor rewrite, with unchanged original statement encoding/CID. If let or
projection public support is claimed, include an actual TYPE containing those
constructors and verify that capture retains them rather than elaborating them
away. Native grammar probes and synthetic index DAGs alone do not establish
that source-to-publication path. Root can choose a minimal combined witness
instead of repeating old peer/custody/recovery campaigns.

Large literal payloads can satisfy canonical validation but exceed the existing
1 MiB formal metadata, 32 KiB stored offer, 16 KiB local reply or 64 KiB peer-page
allowance. Keep those refusals; never omit TYPE syntax or keys to fit. The new
index support does not solve metadata scaling. Canonical validation also still
precedes the smaller 4,096-occurrence index bound and may visit up to 65,536 DAG
nodes; do not claim a new whole-workflow performance bound from the extraction
ceiling alone.

Stop condition for this decision: the narrow implementation preserves old
outputs, indexes all explicit references in the newly admitted syntax, and lets
the retained original mathematical statement complete its public reuse path
under unchanged acceptance and resource rules. Broader retrieval quality,
scalability, library coverage and useful growth remain separate central work.

## Source anchors

- Frozen source13 `py/symbol_index.py`: `extract_type_symbols` (72), group
  closing callback (182), descriptor/row creation (205 onward).
- `py/source_codec.py`: `transform_dag` (370), source `resolve` (666), planner
  `reference` (812), exact package `read_package` (1044).
- `native/AgentReplayCore.lean`: initial string refusal (141), `expandDag`
  (278 onward), projection kind rules (298 onward), group-local export refusal
  (351).
- `py/checking.py`: metadata (260), offer (505), admission comparison (514),
  publication (604 onward).
- `py/peer_node.py`: acquire and metadata equality (225 onward), revalidation
  (257), exact same-descriptor reuse (273).
- `py/storage.py`: key framing (51), postings schema (176 onward), append (732),
  indexed page (752); `py/node.py`: public local find (296 onward).
- `py/peer_wire.py`: exact formal-field set (28), entry framing (215).
- Frozen public `API.md`: exact local type-symbol discovery (64 onward).

All paths in this source-anchor list are relative to
`product-local/auxiliary-frontend-source-13`, not the historical `software/` tree.
