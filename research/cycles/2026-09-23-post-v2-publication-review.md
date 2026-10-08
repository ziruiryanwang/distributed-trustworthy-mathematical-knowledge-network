# Post-v2 review: extend raw type indexing, not mathematical authority

Independent scope/correctness review, 2026-09-23 Chicago.
Reviewer: `post_handoff_math_gap`. Canonical workspace guard passed. Product
inspection was read-only; no product import, native execution, SQLite operation,
new runtime test or product edit. Source13 and the delivered v2 remain frozen.
This is a proposed contract for root selection, not implementation qualification.

## Decision and centrality

**Recommend a fresh, narrowly selected successor that removes the avoidable
raw-type indexing restriction for existing canonical expression forms.** The
original Count case supplies an actual central obstacle: native source capture,
canonicalization, fresh checking and inverse replay passed, but publication
refused the statement's natural literal. Requiring an agent to restate the same
mathematics with constructor syntax changes the exact statement/CID and adds
unnecessary work before it can contribute. Improving this seam directly serves
reliable reciprocal knowledge accumulation; it is not an attribution, research
scheduling or optional global-coordination mechanism.

The modest extension is traversal of existing tags 6–9, with their existing
validation and finite ceilings. It is not permission to support arbitrary Lean
syntax, arbitrary foundation changes, all source/library capture, larger quotas,
semantic search, normalization, or an unbounded mathematical knowledge graph.
The known successful constructor-spelled Count path stays a frozen v2 result;
the original literal-bearing failure must not be relabeled.

## Observed boundary

Source paths below are relative to frozen
`product-local/auxiliary-frontend-source-13/`.

| Boundary | Actual source behavior |
|---|---|
| `py/source_codec.py:370`, `transform_dag` | Validates canonical DAG shape/sharing/order, scoping, references through a callback, and expression tags 0–9; let/literal/projection support already exists. |
| `native/AgentReplayCore.lean:279`, `expandDag` | Already translates the same expression forms; projections require a seed reference or group original-type selector. |
| `native/BootstrapSupport.lean:821` | Decodes let, natural literal, projection and UTF-8 string literal into existing Lean expression constructors; actual native checking remains separate. |
| `py/symbol_index.py:71`, `extract_type_symbols` | Validates through `transform_dag`, but refuses projections in its resolver and then refuses every tag outside 0–5. |
| `py/symbol_index.py:180`, group `close_type_ref` | Independently refuses projections while closing first-original-type group metadata. Fixing only the general extractor leaves this second restriction. |
| `py/checking.py:260`, `metadata` | Requires successful extraction; failure becomes `CANDIDATE_TYPE_FRAGMENT`. |
| `py/checking.py:505`, `offer`; `:513`, `admit` | Offers derive metadata without new native acceptance; admission compares exact metadata before fresh receiving checks. |
| `py/peer_node.py:242`, acquisition; `:257`, revalidation | Received/stored full metadata is recomputed and compared exactly, including trace and symbol ordering. |
| `py/peer_wire.py:230`, `validate_entry` | Frames/binds advertised metadata but does not establish its full expression semantics or mathematical truth. |

Important qualification: a syntactically valid canonical candidate is not yet
mathematics accepted by a receiving node. The extractor is neither a type
checker nor a proof checker. It can produce candidate metadata before native
admission. Its syntactic/ref-shape guarantees must hold on hostile candidates,
but structure-kind, type correctness and proof validity still belong to the
unchanged package/native acceptance path.

There is a separate string-source restriction:
`native/AgentReplayCore.lean:141` rejects nonempty `unit.strLits` with
`INITIAL_EXTERNAL_STRING_LITERAL_UNSUPPORTED`. Canonical/native decoder support
for tag 9 does **not** establish ordinary-source string contribution support.
Do not remove that restriction or claim its resolution in this work. Static
index support for tag 9 is useful grammar completeness, not a new source claim.

## Required extractor semantics

Let `E13` be the current partial extractor and `E+` its proposed extension.
For a fixed foundation, universe arity and seed count, require:

1. If `E13(T)` succeeds, `E+(T)` returns the identical result: same type DAG,
   first-occurrence symbols, sorted keys, occurrence count, maximum depth,
   distinct count, normalization marker and acceptance marker.
2. `E+(T)` succeeds only after the same canonical DAG validation, reference
   restrictions, closedness checks and resource bounds. Unknown tags, forward
   edges, duplicate/unreachable nodes, nonminimal natural magnitudes, invalid
   UTF-8, open roots and forbidden references are not tolerated or repaired.
3. The emitted set is exactly the canonical encodings of explicit external
   references encountered in this raw effective type, with no symbol inferred
   from evaluation, dependency closure, declaration bodies or literal values.
4. Traversal is complete within the selected ceilings. A bound/support/invalid
   failure returns no partial successful symbol set or postings.

The new cases should have precisely this meaning:

| Node | Symbols at the node | Traversed expression children, in order |
|---|---|---|
| `[6,type,value,body]` | None at the let constructor itself | Type, value, body |
| `[7,naturalMagnitudeBytes]` | None | None |
| `[8,structureRef,fieldIndex,target]` | Exact `structureRef` | Target |
| `[9,utf8Bytes]` | None | None |

Tags 0–5 keep their current semantics and order. A let's initializer and
annotation are part of the raw type syntax even when reduction would discard
them. This is deliberately different from the strict term-only computational
dependency walk used in the reciprocal proof audit. Mixing those two notions
would quietly change what an exact-symbol query means.

A natural literal contributes no invented `Nat`/constructor key, and a string
literal no invented `String`/runtime key. Bootstrap/source closure separately
adds literal-support dependencies (`BootstrapSupport.makeUnit:225–226`). The
index is therefore **not** a complete semantic dependency list. It cannot
search for the value 1 or a substring merely because it supports literal nodes.

Projection needs extra validation beyond generic `_ref`: that helper also
accepts declaration/theorem/opaque and constructor/recursor references, which
are not allowed as a projection's structure reference. Permit only `[0,i]`
within seed range, or `[3,GroupID,[0,typeIndex]]` with the ordinary typed-ID and
selector grammar. Do not erase group selectors or reinterpret a constructor
or recursor selector as its owner type. Actual membership/structure correctness
remains checked by package planning/native reconstruction. A valid seed index
alone is not proof that its binding is a structure.

For a group root, preserve the current first-original-type rule. Close ordinary
group-local constant references as before, and allow only appropriately shaped
external projections. **Keep group-local projections refused**: the source
compiler and native export already reject them. Closing such a reference to an
external one merely to bypass this policy would be an unauthorized grammar
expansion, not an index repair. The derived closed type ID remains metadata,
not a new stored dependency or additional replay root.

## Exactness, limits and compatibility

Preserve the existing 4096 expression-occurrence, depth-64 and 32-distinct-key
ceilings, including inclusive boundary behavior. Count each visited expression
occurrence, not merely unique DAG nodes; otherwise sharing changes cost and
trace semantics. A projection reference is metadata on its one expression node,
not an extra expression child/depth. A literal is one leaf occurrence, not one
occurrence per payload byte. Existing literal-byte, canonical package, JSON,
metadata, entry and transport caps still apply. In particular, supporting a
1-MiB canonical literal does not promise it fits a public offer or page.

Do not use a global visited-node optimization that changes occurrence counts or
first-occurrence ordering. Do not normalize, beta/zeta reduce, unfold definitions
or rewrite literals into constructor syntax. No mathematical object, replay,
proof-instance, declaration, type or descriptor CID may change for unchanged
bytes. The index's new domain is additive; the canonical encoding and its
meaning remain fixed.

Full `formal_metadata`, including `trace`, is an interoperability commitment
even though the descriptor CID does not independently name an extractor
version. Thus key-set equality alone is insufficient. If old-domain output
bytes remain identical, no mathematical schema, foundation, wire/catalog or
database version change is needed merely to accept previously refused syntax.
Adding an extractor-version field or changing trace formatting would instead
break exact peer comparisons and require a different compatibility design.

Expected mixed-version behavior under that strict-extension contract:

| Producer metadata domain | New receiver | Frozen source13 receiver |
|---|---|---|
| Previously supported type | Same derived metadata; normal existing gates | Existing behavior |
| Newly supported type containing tags 6–9 | New metadata gate may pass, then unchanged native admission | Catalog framing may be browsed; acquisition/offer metadata derivation safely refuses unsupported syntax, before mathematical acceptance |

This does not guarantee every new type passes all other gates. An old peer
cannot be claimed fully interoperable with new offers merely because catalog
and bundle versions match. Do not add a fallback that trusts sender metadata,
drops unsupported references, silently filters new syntax, or marks acquisition
as accepted. No automatic old-installation/database mutation, index backfill,
configuration rewrite, retry refund or allowance renewal is selected.

## Bounded evidence necessary to select and qualify the fix

The separate test-design agent owns exact test construction. These are the
minimum distinguishing obligations, not a mandate to repeat old campaigns:

- Legacy successful fixtures retain exact complete extraction/formal metadata,
  including traces; existing malformed-reference and type-only/no-body rules
  remain. Retain this evidence with the successor source map.
- Focused inert DAG cases distinguish each new child position, literal leaves,
  exact projection references, separate group-type closure and forbidden local
  or non-type projection references. Check malformed payloads and finite-limit
  boundaries without executing a guessed mathematical source.
- The retained original Count capture/type is the actual positive discriminator
  for natural literals. A new qualified run must submit/publish the **original
  literal-bearing source** and return the same exact theorem/package for fresh
  receiver admission; a second constructor-spelling workaround does not qualify
  the fix. New operation/state allocation and all old charges remain explicit.
- Exercise changed metadata integrity on selected invalid advertised/stored
  symbols or trace, and establish old/new compatibility on the legacy domain.
  Do not infer ordinary-source string support from a synthetic tag-9 index test.

A fresh source selection, minimal file-map delta, focused tests and one relevant
native public round trip are sufficient to decide this repair. No new ranking,
global ledger, agent-goal orchestration, proof-normalization or broad performance
campaign is needed. Measured costs must remain scoped; successful publication
does not itself prove useful or exponential knowledge growth.

## Coordination and disposition

The continuity diagnosis independently identified both projection refusal sites
and the source-string restriction. The test-design agent was explicitly asked
to preserve old trace bytes and distinguish raw syntax from semantic closure.
The above constraints agree with their current findings. No product successor
is selected by this reviewer, and no publication/native behavior has yet changed.
