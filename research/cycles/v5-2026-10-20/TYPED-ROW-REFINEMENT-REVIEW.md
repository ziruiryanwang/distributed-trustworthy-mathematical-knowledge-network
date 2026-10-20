# Independent review: hybrid typed syntax rows

2026-10-20. Reviewer: core_search. Root scope:
[TYPED-ROW-SELECTION](TYPED-ROW-SELECTION.md). Source-only review, no checker
edit, build, input replay, test, proof operation or performance claim.

## Decision at this checkpoint

**The narrowed design is feasible in principle without reconstructing generic
suffix DAG rows and without changing mathematical checking rules.** Keep all
declaration rows and the exact fixed foundation prefix as their old Values;
type only the 14 canonical name/level/expression tags. Retain one whole-frame
legacy fallback for every unsupported raw representation before semantics.

This is not a drop-in change to `serde_json::from_value`. Three current interfaces
require explicit successor seams: `Input.rows: Vec<Value>`, correspondence's
`Inventory` holding `&Value` rows, and the native parser's private row enum.
Those seams are tractable. Merely adding a decoder while leaving those interfaces
unchanged would reconstruct the removed Values and defeat the intervention.

The author's final finite table has now been reviewed as recorded below. This
checkpoint records independent source analysis; it does not adopt unwritten
implementation or authorize it. Source bindings are the 13 exact inputs already recorded in
TYPED-ROW-NEXT-DECISION, including the memo correspondence, not the older
unmemoized file.

## Why retaining generic declarations matters

The source proposal initially included typed declarations and inductive metadata.
That expanded scope is unnecessary. Native `Defn/Thm/Opaque` drop `all`, while
correspondence observes it. Inductive `isReflexive` and other metadata also have
different native/correspondence roles. Keeping their full Values preserves these
observations through the unchanged declaration-matching routines. The old
native conversion remains for those few rows.

Root/growth's retained input census identifies 1,513 DAG rows among 1,538 suffix
rows, with 25 declarations and 826 fixed-foundation rows across two frames.
This review uses that as their recorded data count, not a measured work fraction.
Typing declarations would enlarge assurance work for little additional row
coverage. Keeping them generic also prevents imported inductive rows from
unnecessarily forcing every ordinary theorem frame onto the fallback route.

## The non-reconstruction path exists

The proposed implementation must preserve the following data path:

1. An owned immutable byte frame enters a strict context-aware decoder. Before
   semantics, it yields either a private hybrid syntax/count token or a decision
   to run the original complete frame path once.
2. Hybrid input retains normal non-row Values and a single original-order row
   collection with generic foundation/declaration rows and typed DAG rows.
   Its token contains private verified virtual counts, not caller-owned counters.
3. Correspondence indexes borrowed typed-or-legacy row views. Names still become
   the same canonical `Value::Array`s; levels and expressions retain typed or
   generic references. Declaration/group Values remain borrowed unchanged.
4. Existing name/reference construction, canonical expression construction,
   syntax memo walk, group matching, body obligations and role derivation consume
   those views. Canonical semantic outputs are still Values: producing required
   canonical types/bodies is not reconstructing raw suffix rows.
5. After correspondence, each typed DAG row maps directly to the corresponding
   private `ExportJsonVal` and matching `BackRef` **inside parser.rs**. Generic
   rows call unchanged `decode_corresponded_owned_row`. Preserve original row
   order; feed the resulting owned native rows to unchanged `parse_owned_rows`,
   `apply_row` and finalization.
6. Existing conditional module checking, commitments, exact J, parent-journal
   sequence, aggregate graph and actual guest receipt verification remain.

The native mapping must be a narrowly typed constructor, not a stringly typed
escape hatch around the old row schema. Its existence follows from the selected
14 variants' fields in `ExportJsonVal`; there is no inaccessible kernel state to
reproduce. It requires no public mutable handle or authority bit. The field
mapping must be checked in the later source review, rather than justified by the
name `OwnedExportRow` alone.

## Local refinement argument

Let `R` project each typed DAG row to its exact old JSON Value; R is a
specification function and need not execute in production. Generic rows project
to themselves. Let `D` recognize the finite supported raw subset; let `O` be the
complete existing frame relation, including raw and logical bounds; let `N` be
the proposed typed frame path.

For `D(b)=Typed(t,c)`, require strict parsing `P(b)=R(t)` and virtual census
`C(P(b))=c`. On that subset the following source facts permit a constructive
simulation:

- Every typed scalar has the original native width and value; string and binder
  variants are preserved without normalization. All index/domain fields remain.
- Name inventory reconstructs the same canonical name arrays in the same order.
  Indexed level/expression views return exactly the payload observations that
  `Inventory::level/expression/validate_*_memo` previously obtained from Values.
- Reference bounds, owner interpretation, universe order, field-dependent checks
  and traversal order are unchanged. Reached `nondep=true` fails at its original
  correspondence check; unused `nondep=true` retains its native meaning.
- By induction on the old ordered recursive traversal, canonical outputs,
  successful syntax summaries and logical work/depth are the same. Memo keys
  remain scoped to the same owner/parameter invocation. An insufficient memo
  budget descends by the original path; do not replace its first-failure behavior.
- Direct native construction yields the exact same 14 private enum variants and
  backreferences as the old decoder on the recognized subset. Generic rows use
  the literal old decoder. Induction over ordered `apply_row` calls gives equal
  native DAG/declarations, duplicate rejection and finalization outcomes.
- Therefore unchanged conditional checks and commitments produce identical J
  and parent-premise sequence when either selected path succeeds.

This argument requires both `N(t)` success implies `O(P(b))` success **and the
converse on all typed-selected inputs**. The former alone permits silently
rejecting old-valid syntax. Nothing here establishes source-level verification
for code that does not yet exist.

If `D(b)=Unsupported`, invoke O on the original complete frame, not reconstructed
bytes. If `D(b)=Malformed`, its reason must already imply old raw/logical
rejection. A simpler conservative implementation may route any uncertain
syntactic case to `Unsupported`; it need not predict semantic failures. By cases,
these conditions preserve the complete old mathematical/logical success domain.
Equal frame outputs plus unchanged aggregate graph rules preserve aggregate
results; they do not replace cryptographic proof soundness.

## Parser and accounting traps to block before implementation

| Trap | Required treatment |
|---|---|
| Generic row construction used merely to decide the fast path | Decode directly with a structural visitor/seed. No initial full-Value parse followed by conversion |
| Arbitrary JSON object key order | Decode a temporary typed payload and index independently; require exact recognized field set before producing the row. Do not require index first |
| Duplicate or escaped-equivalent keys | Compare decoded key strings, including generic subtrees. Never accept both `name` and its escaped spelling |
| Numeric convenience coercions | Retain old strict unsigned/integer-only visitor behavior; floats, exponents, negative syntax and `-0` must not slip through a permissive typed numeric conversion |
| Lost parser nesting behavior | Preserve pinned Serde safe default recursion bound as well as virtual node/depth limits; neither substitutes for the other |
| Wrong field width | Indices are `u32`, `bvar` is `u16`, projection index is actual-target `usize`; width mismatch can conservatively fall back, never truncate |
| Universal semantic checks in the recognizer | Do not pre-reject an unused typed `nondep=true` or apply reached-only bounds to every row. Structural choice precedes proof/reference checking |
| Normal `max/imax` arrays treated as exotic | These exact two-element arrays belong in the fast path; only unsupported shapes fall back |
| Legacy native forms ignored | All rows still reach native application. Positional/extra-field/alias forms outside the recognized subset use full-frame O |
| Lost declaration fields or foundation exactness | Parse generic rows strictly, preserve every value, use exact 413-row foundation equality; no hash-only substitute |
| Double accounting on fallback | Tentative counts stay private and are discarded; old full-frame path makes the one committed logical charge |
| Fall back after semantic failure | Forbidden. No second kernel/correspondence/commitment/graph attempt, no budget renewal |
| Whole-aggregate fallback after earlier frames | Use the existing complete module-witness boundary. Do not replay prior checked modules or their receipt/graph work |

Virtual census is not typed-object count. For a row-root at relative depth zero,
the independently derived local counts are:

| Tags | Value nodes | Maximum relative depth |
|---|---:|---:|
| `str`, `num` | 5 | 2 |
| `succ`, `param`, `bvar`, `sort` | 3 | 1 |
| `max`, `imax` | 5 | 2 |
| `const` with k universes | 5 + k | 2 if k=0; otherwise 3 |
| `app` | 5 | 2 |
| `lam`, `forallE` | 7 | 2 |
| `letE` | 8 | 2 |
| `proj` | 6 | 2 |

Object keys are not Value nodes. Add the actual surrounding depth and all other
fields, generic rows and subtrees. Preserve the original raw 16 MiB, strict
1,000,000-node and structural depth-256 preconditions, together with aggregate
500,000 nodes/depth128/250,000 rows/8,192 bodies/4,096 openings/128 edges and
the stricter Serde recursion behavior. Commit aggregate counts in the existing
order if failure reports expose partial census. A token whose tree can be
mutated after counting or whose counts can be supplied by a caller is invalid.

## Work and scope judgment

This removes generic suffix row maps/key storage and Value-to-native conversion
for the recognized DAG rows. It does not remove required canonical semantic
construction, fixed foundation work, generic declaration checking, native DAG
construction or the proof system's work. The current singleton-row native decode
already avoids two outer flatten buffers: that existing saving cannot be counted
again as a new benefit.

Fallback pays at most one partial structural attempt plus one complete old frame
execution. Both use the same original physical CPU/wall allowance. Logical
domain equivalence is not equal wall-clock completion: the added prefix can
make an unsupported input run out of resources earlier. This must remain an
explicit resource failure, never a claim that the old mathematical domain was
invalid or that failed work was free.

Minimum implementation seams, if root later selects them: a private hybrid
frame/strict decoder, mixed row/input transport, typed/legacy correspondence
views, parser-internal native constructor, and one aggregate census/dispatch
adapter. Existing legacy entrypoints can remain literally unchanged. No typed
kernel, binary format, new trust policy, hash-only foundation or new proof lane
is justified. A runtime build or benchmark is not selected by this review.

## Final finite-table review

Reviewed `TYPED-ROW-FAST-SUBSET.md`, 21,887 bytes, SHA-256
`8360a87e913ca5d271e643e6c460c08315d18fe0460b16dae5e3dbb695fff572`.
The exact fourteen field/type/shape rows agree with the inspected native enum;
the four binder styles agree with `expr.rs`. The virtual-node/depth table agrees
with the independent derivation above. The proposal explicitly retains generic
declarations and fixed prefix, `const.us` reached-only arity, both `nondep`
Booleans, target-width projection, strict numeric syntax, escaped-equivalent
duplicate keys, one private immutable census and whole-frame structural fallback.
The concrete borrowed-list view avoids reconstructing a `Vec<Value>` merely to
read typed universes. Its native constructor belongs inside parser.rs as needed.

**No remaining design-level blocker found for root to select this one narrow
source implementation.** Recommend it over a full typed declaration rewrite or
a second direct-I implementation lane. It targets producer representation work
and the inspected interfaces can carry it end-to-end. This conclusion does not
predict a proof speedup or certify future Rust code.

The next review must enforce the stated equal-success/logical-domain obligations
on the actual successor. In particular, source inspection should verify that
the supported path never reconstructs raw DAG Values and that the fallback still
calls the actual old entrypoint. Existing memo constructor/shared-DAG/work-limit/
first-error controls can inform the smallest differential controls; do not rerun
an unchanged broad suite merely because a new source file exists. The author's
proposed retained-frame J/premise comparison is a relevant changed-boundary
control, not permission for proving or replaying completed proof campaigns.

The saved retained row census was not re-extracted by this reviewer; duplicating
that author's read-only count would add little. This review independently checks
the source mapping, virtual counts, interface feasibility and acceptance argument.
Root owns selection, source ownership and any later bounded execution.
