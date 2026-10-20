# Typed suffix DAG rows: exact fast subset and refinement contract

2026-10-20. Source/theory checkpoint by `core_growth`, selected by root and
submitted for independent review by `core_search`. **Proposal, not implemented or measured.**
All paths below are relative to the sole canonical project root,
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Decision and central payoff

Type only the suffix **name, level and expression DAG rows**. Retain the first
413 foundation rows, every declaration row, and all non-row semantic data in
their existing strict `serde_json::Value` representations. This narrows the
optimization scope in `TYPED-ROW-NEXT-DECISION.md`; its whole-frame dispatch and
bidirectional refinement requirements remain. In particular, the earlier idea
of typing ordinary/imported/inductive declaration fields is not selected.

The purpose is to remove generic map/key/tree construction and later generic
Value-to-native conversion for common DAG rows, **not** to weaken checking or
investigate RAM. The two retained ordinary-module suffixes contain 1,513 such
rows and only 25 declaration rows. Retaining the latter avoids a much larger
metadata-preservation rewrite while keeping both actual suffixes eligible:
each ordinary module contains an imported inductive group. Declining all
inductive-bearing frames would therefore miss both targets.

This counts removable representation work. It is not a time fraction, proof
speedup, successful-production bound, net-growth result, or v5 release claim.
Canonical semantic types/bodies, native DAG construction and kernel work remain.

## Exact retained opportunity, without a new experiment

Read-only census input:
`experiments/v5-local-checks/delta-reprepare-01/evidence/delta-packet.json`,
662,480 bytes, SHA-256
`54c7dac7f83a9a06c2b23b17a77be20364c1b90e4cd3b1db58b69c62fda2dcf1`.
Schema is `DMKN_NATIVE_DELTA_PACKET_V1`; both local group kinds are `ordinary`.

| Suffix tag | Delta 0 | Delta 1 | Representation |
|---|---:|---:|---|
| `str` | 22 | 25 | Typed DAG |
| `num` | 3 | 4 | Typed DAG |
| `succ` | 4 | 5 | Typed DAG |
| `param` | 3 | 4 | Typed DAG |
| `max` | 10 | 5 | Typed DAG |
| `bvar` | 7 | 1 | Typed DAG |
| `sort` | 7 | 8 | Typed DAG |
| `const` | 62 | 39 | Typed DAG |
| `app` | 560 | 280 | Typed DAG |
| `lam` | 142 | 102 | Typed DAG |
| `forallE` | 93 | 105 | Typed DAG |
| `proj` | 17 | 5 | Typed DAG |
| `def` | 9 | 9 | Unchanged Value |
| `thm` | 1 | 1 | Unchanged Value |
| `moduleImportTheorem` | 1 | 2 | Unchanged Value |
| `inductive` | 1 | 1 | Unchanged Value |
| **Suffix total** | **942** | **596** | **1,538** |
| **Typed subset** | **930** | **583** | **1,513** |
| **Generic declarations** | **12** | **13** | **25** |

Delta 0 has 1,355 total rows and one parent; delta 1 has 1,009 total rows and two
parents. Combined: 2,364 rows = 826 unchanged foundation + 1,513 typed DAG + 25
unchanged declarations. `imax` and `letE` have no occurrences here but belong to
the same small canonical DAG schema; including them avoids an artificial
producer-fragment split. This table is a structural opportunity census, not a
distributional claim about future mathematics.

Separate preserved aggregate native evidence:
`experiments/v5-local-checks/aggregate-claims-controls-02/evidence/actual-two-delta/stdout.txt`,
SHA-256 `01d7c9cc45a16f520980e80672f90c0a97a69e31e344f748910df5abb24ffd0b`.
It reports 2,364 rows, 29,858 old Value nodes, maximum depth 28, 22 bodies,
23 openings and three parent edges. Its adjacent `actual-two-delta.bin` is
215,540 bytes, SHA-256
`7e21d092206b08a9a71231045b8152df4179ee6575cdc5e3afc704ef03c0be58`.
This is conditional native execution evidence, not a successfully produced
recursive certificate or a measured typed-decoder result.

## Exact fourteen-tag representation

A selected DAG row is an object with exactly two keys: the indicated lowercase
index key and the indicated constructor key. Object key order is arbitrary;
duplicate keys are forbidden. Every field below is mandatory and payload object
field sets are exact. Index and reference values are retained without changing
their meaning. Continuity, earlier-reference, ownership and validity checks
remain semantic checks performed after the structural dispatch decision.
Duplicate detection compares decoded key strings, including escaped-equivalent
spellings, rather than raw key bytes.

| Tag | Outer index | Exact payload fields/type | Native variant |
|---|---|---|---|
| `str` | `in: u32` | `{pre: u32, str: String}` | `NameStr` |
| `num` | `in: u32` | `{pre: u32, i: u32}` | `NameNum` |
| `succ` | `il: u32` | `u32` | `LevelSucc` |
| `param` | `il: u32` | `u32` | `LevelParam` |
| `max` | `il: u32` | Exactly `[u32, u32]` | `LevelMax` |
| `imax` | `il: u32` | Exactly `[u32, u32]` | `LevelIMax` |
| `bvar` | `ie: u32` | **`u16`** | `ExprBVar` |
| `sort` | `ie: u32` | `u32` | `ExprSort` |
| `const` | `ie: u32` | `{name: u32, us: Vec<u32>}` | `ExprConst` |
| `app` | `ie: u32` | `{fn: u32, arg: u32}` | `ExprApp` |
| `lam` | `ie: u32` | `{name: u32, type: u32, body: u32, binderInfo: BinderStyle}` | `ExprLambda` |
| `forallE` | `ie: u32` | Same exact fields as `lam` | `ExprPi` |
| `letE` | `ie: u32` | `{name: u32, type: u32, value: u32, body: u32, nondep: bool}` | `ExprLet` |
| `proj` | `ie: u32` | `{typeName: u32, idx: usize, struct: u32}` | `ExprProj` |

`BinderStyle` is exactly one of `default`, `implicit`, `strictImplicit`,
`instImplicit`. `usize` is the **actual target width**, not an arbitrary `u64`;
native and guest targets may differ. All other integer widths above agree with
the existing private native row schema. A width failure may conservatively
select the old fallback; do not substitute a truncating conversion.

Parsing numeric fields must first preserve the existing strict
`deserialize_any` numeric domain and then perform checked width conversion.
The strict parser accepts `visit_u64`, rejects negative `visit_i64` and rejects
floating-point visits. Do not assume a newly derived `u32` parser has identical
behavior for `-0`, fractions or exponent forms. All string decoding uses the
same JSON unescaping/Unicode behavior, with no case folding or normalization.
The exact string contents survive; the old name checks still decide nonempty,
NUL, length and owner namespace requirements.

Do not turn reached-row semantic conditions into universal decoder limits:

- `const.us` is retained as an arbitrary bounded-by-frame `Vec<u32>`. The old
  correspondence checks arity at most 256 when it reaches the expression. An
  unused native-accepted row must not be newly refused by imposing that limit
  globally. A deliberate decoder subset limit must instead choose fallback.
- `letE.nondep` retains either Boolean. Reached correspondence requires `false`;
  the decoder does not use that condition to choose another semantic path.
- Structurally representable bad backreferences, unbound universes, wrong owner
  names and discontinuous indices enter the same later semantic checking rules.
  They are not repaired, normalized or retried after semantic rejection.

## What deliberately stays generic

The fixed prefix remains 413 strict Values, compared by the unchanged exact
`foundation_static::matches_rows`. All metadata and otherwise ignored prefix
fields participate in that comparison. This is not prefix elision or a
hash-only foundation substitute.

Every declaration row remains a strict Value and uses the unchanged declaration
correspondence and native decoder. In particular:

- Ordinary `def/thm/opaque` keep `all`, even though native ordinary variants do
  not retain it. Correspondence still checks the exact required group metadata.
- Imported theorem/definition/opaque records keep their original metadata and
  exact conditional premises. A typed row does not authorize an import.
- Inductive groups keep all type/constructor/recursor fields, including
  `isReflexive`, ordered parameters, counts, rules and `all`.
- Foundation axioms/quotient primitives and any other declaration forms receive
  no new authority. The old checks continue to permit or refuse them.

The generic declaration component is part of a single selected fast frame. It
is **not** a per-row semantic fallback. A decoder may retain recognized
declaration outer objects/subtrees generically while directly decoding DAG
payloads. It must establish the complete outer shape before committing a row;
an unexpected index/tag/extra outer field causes whole-frame fallback. Do not
materialize a generic DAG payload merely because its constructor precedes its
index in the byte stream: a temporary typed payload plus a later matched index
handles arbitrary key order.

`local_spec`, parent journals/openings, body expressions and other non-row data
remain in their old representation and pass the same extraction/validation.
The fast frame may require exact object-form top module/parent records; old
positional record forms use fallback. Unsupported DAG positional/alias/extra
field forms also use fallback. `natVal`, `strVal` and `mdata` select fallback;
the original config/application refuses them, including unused occurrences.

## Virtual old census: same logical accounting

Typed storage changes physical allocations, not what the logical resource
contract counts. Count the Value tree the old strict parser would have built.
Object keys are not Value nodes. With the row root at relative depth zero:

| Tags | Virtual nodes | Maximum relative depth |
|---|---:|---:|
| `str`, `num` | 5 | 2 |
| `succ`, `param`, `bvar`, `sort` | 3 | 1 |
| `max`, `imax` | 5 | 2 |
| `const`, with k universe entries | 5 + k | 2 if k = 0; otherwise 3 |
| `app` | 5 | 2 |
| `lam`, `forallE` | 7 | 2 |
| `letE` | 8 | 2 |
| `proj` | 6 | 2 |

For example, `const` contributes outer object + index + payload object + name +
universe array + its k scalar children. The enclosing row-array/module nodes
are separate. Integrate counts at the actual token traversal depth; do not
hard-code a depth offset of two merely because ordinary module rows have it.
Generic subtrees use the same strict parser and node/depth rules. Checked
arithmetic preserves overflow rejection. Duplicate keys, UTF-8, EOF, scalar
rules and the default Serde parser recursion limit remain in force as well;
the virtual depth formula alone is not a substitute for parser recursion safety.

Preserve the raw module-frame limit of 16 MiB, module Value node limit 1,000,000
and depth 256, and the aggregate limits: 500,000 nodes, depth 128, 250,000 rows,
8,192 bodies, 4,096 openings and the existing graph edge bound. Existing parser
recursion limits can be stricter for a particular encoding than these explicit
logical limits. Do not disable them silently to reach the explicit ceiling.

## One deterministic structural choice per immutable frame

Let `P(b)` be the old strict parse of bytes b and `C(P(b))` its exact census.
Let `O` be the complete old conditional relation, not native row decoding alone.
The new structural decoder `D` returns exactly one outcome:

1. `Typed(t,c)`: all candidate DAG rows have the finite representation above;
   every generic component has the old strict representation; syntax and
   virtual old census have been established.
2. `UnsupportedRepresentation`: discard tentative typed data/counters and run
   the **unchanged old complete frame path once** on the original immutable
   bytes. It is safe to fallback even if the old path will eventually reject.
3. `Malformed`: refuse only when a source argument establishes that the old
   pipeline also rejects those raw/logical conditions. Ambiguous cases may use
   outcome 2 rather than duplicating the old acceptance analysis.

The choice occurs before correspondence, native application, kernel checking,
commitments, parent binding or aggregate graph processing. Their failures never
cause fallback. No sender assertion selects a weaker trust path.

Tentative census is private. Successful typed parsing commits exactly one
frame contribution; unsupported representation discards its tentative counts
and lets the old path supply exactly one contribution. Aggregate overflow
never resets the global counter or retries a different path. Prefix processing,
allocation and discarded data have no authority side effects. All physical
work remains charged to the original operation/deadline; no new grant, Job or
automatic attempt is created.
Counts belong to a private immutable parse token, not caller-supplied counters
or a tree mutable after counting. Preserve the existing census update order when
partial counters are visible in a failure report; mathematical equivalence
alone does not justify silently changing that operational observation.

## Refinement argument and its exact remaining obligations

Define `R(t)` mathematically by replacing each typed DAG variant with its table
object and leaving every generic component unchanged. `R` is a specification
projection, **not** an implementation instruction to rebuild row Values.

### Decoder and census

For a selected shape, unique exact field sets and the same scalar decoding give
the same old Value at each field. The name/string, scalar, pair, record and
universe-vector cases cover all fourteen variants. Induction over the enclosing
arrays/objects gives `P(b) = R(t)`. The table counts each scalar/container once;
induction over those same containers gives `C(P(b)) = c`. Object key order does
not change Value equality or census. A source implementation must show that its
duplicate/extra-field handling and recursion checks implement these premises.

### Correspondence

Use borrowed row views that expose the same scalar and list values from either
generic foundation rows or typed suffix rows. Keep generic declaration groups
as `Vec<&Value>`; keep their matching rules unchanged.

- For names, the same predecessor and string/number component produce the same
  canonical name Value, followed by the same name validation. Induct on native
  name index order; the empty name seed is unchanged.
- For levels, expose the same `param/succ/max/imax` tag and references. Keep
  earlier-reference tests, universe-parameter lookup, traversal order and
  canonical output unchanged. Induct on the successful old traversal, not on an
  unchecked assumption that every syntactic reference is already valid.
- For expressions, expose the same eight tag payloads. Preserve the same child
  order, name/owner lookup, binder style, universe arity and `nondep` checks.
  Construct the same canonical output Values where required by commitments.
- Preserve memo lifetime, `SyntaxSummary` visits/height, cache-hit budget test
  and original-walk fallback within correspondence. The latter is the existing
  memo accounting mechanism, not permission to retry another frame checker.
  Since the view supplies identical observations, induction over the existing
  walk gives identical successful results and logical resource charges.

In particular a convenient `Vec<Value>` rebuilt for every universe list would
erase part of the benefit. A borrowed accessor such as
`IndexListRef::Json(&[Value]) | Typed(&[u32])` can expose a common iterator
without constructing generic row maps/arrays. Canonical semantic output Values
are still necessary and are not the forbidden generic row reconstruction.

### Native row construction and checking

Inside the native parser module, consume each typed variant directly into the
same private `ExportJsonObject`/`ExportJsonVal` fields and exact BackRef. The
table gives a fieldwise constructor equality to old successful Serde decoding:
rename `fn` to native `fun`, `us` to `levels`, binder fields to their existing
native names, and `struct` to `structure`; copy values without coercion.
Name strings become the same owned `Cow` contents. Generic rows continue through
the original `decode_corresponded_owned_row` path.

The private `OwnedExportRow` constructor must remain controlled by the parser
module; do not expose a caller assertion of verified rows. It denotes decoded
syntax, not mathematical validity. Ordered `parse_owned_rows`, `apply_row`,
finalization and all kernel checks stay unchanged. Equal ordered native records
therefore give equal construction/checking outcomes, conditional on completion.

### Composition theorem required for adoption

For every typed-selected b, require **both directions**:

`N(t)` succeeds iff `O(P(b))` succeeds, and exact returned journal J, ordered
pending-premise list and retained logical resource checks are identical.

The preceding component simulations are sufficient in principle: same fixed
foundation, canonical correspondence output, native records, local checked
declarations, body/group commitments and parent conditions give the same module
output. Then unchanged aggregate rank/edge/closure rules give the same aggregate
header and pending claims. Actual final guest `env::verify` calls discharge
those exact recursive receipt obligations unchanged. No source argument replaces
cryptographic verification or proves the kernel itself sound.

The whole-frame hybrid inherits old mathematical/logical acceptance: selected
inputs use bidirectional simulation; unsupported inputs literally use O;
malformed inputs have an old-refusal argument. One-way fast-implies-old would
establish only soundness, not unchanged old-valid compatibility. This is a
complete design-level proof decomposition, **not** a formal proof about
unwritten Rust or a passed implementation audit.

## Physical cost and adversarial limits

Logical acceptance equality is conditional on completing the selected
computation. Equal OS CPU/wall caps do not imply identical operational success:
fallback can pay a typed prefix plus the old full path and time out where the
old path alone fits. Conversely the optimized path might finish where old code
does not. Neither advantage nor penalty has been measured.

Bound the fallback structure to one finite typed prefix plus one original
complete frame execution under the existing overall caps. Adversaries can force
this slower representation lane. There is no global guaranteed speedup and no
free retry allowance. Counts should describe removed work precisely: supported
suffix DAG maps/keys and generic-to-native conversion disappear; direct typed
decoding, temporary structural fields, views, strict census, generic foundation/
declarations and native/canonical semantic work remain.

## Concrete source/interface scope if root selects implementation

No predecessor below is editable under this note. A fresh successor needs:

1. A private direct typed frame decoder/input module with the fourteen variants,
   strict scalar/container helpers, private tentative census and explicit
   `Typed/UnsupportedRepresentation/Malformed` outcomes. It must not first build
   a full generic frame and then convert it to typed rows.
2. A parser-module typed DAG input/view and fieldwise consuming conversion to
   private native `OwnedExportRow`, alongside the unchanged legacy decoder.
   `parse_owned_rows`, application/finalization and the kernel remain unchanged.
3. A fresh typed-view correspondence entry point, retaining the old entry point
   for the literal fallback. Its scalar/list views cover generic foundation and
   typed suffix rows; declaration matching and semantic output constructions
   retain their behavior. Sharing unchanged pure helpers is possible, but a
   refactored fallback must not be called literally unchanged without review.
4. A bounded module-relation dispatch seam and aggregate census commit seam.
   These borrow the same immutable frame and preserve existing aggregate graph
   behavior. Fixed foundation, commitments, policy and guest recursive receipt
   rule do not change.

The correspondence predecessor is about 33 KiB and the parser about 45 KiB.
This is a bounded representation change, not a trivial few-line optimization;
root should reject it if the actual source requires semantic/kernel redesign.
Do not grow it into a new binary wire, foundation cache, typed declarations,
direct-I transport, second proof policy or broad benchmark framework.

The smallest future differential control set would cover all fourteen variants
and arbitrary field order; `u16/u32/usize` boundaries and numeric spelling;
empty/nonempty universes; reached/unused `nondep` and arity; declaration metadata
preservation; prefix equality; exact virtual census near limits; deterministic
whole-frame unsupported fallback; no fallback on semantic rejection; and exact
J/premises on the two existing retained suffixes. Controls should use the actual
old entry point as comparator. They are **not selected to run by this note**;
no build, proof-production campaign or RAM probe is authorized here.

## Source bindings

The complete inspected binding table is retained in
`TYPED-ROW-NEXT-DECISION.md#exact-inspected-source-bindings`. Key sources for
this narrower table are:

| Source | SHA-256 |
|---|---|
| `software/v5/modules/native/checker/src/parser.rs` | `7a183a1c9e6ff3ee2c32ee6542ed85d3de0835b00e235f80f6982c3e7038d218` |
| `software/v5/modules/native/proof_memo/module_correspondence.rs` | `7877ee22c7e1d4350858e67c8cebbedf057dee1820cd9f61940e37cf51f6508e` |
| `software/v5/bounded_parse/canonical.rs` | `f8356d9300f5436b3b6fb7a76b7d2d19e0b3dcedae0bfd00e1e10abea54de9c1` |
| `software/v5/bounded_parse/census.rs` | `48cad55b54d3cd233d760871308ccfdc54bb50711adb89651f7d2861caa5a1d5` |
| `software/v5/bounded_parse/module_relation.rs` | `0f78c1663673f291c7b612cc3bdef423124cc6cc47fd649b71e5bc13d4cd808a` |
| `software/v5/modules/receipt/src/input.rs` | `4b5da4aefeef4ca7dc2ce3d2bd10cd0f270a3d5682f2ea16d8ea2e37c63bfa46` |

Only ordinary read-only source/data inspection and this Markdown checkpoint
were performed. Successful affordable frontier production, full-cost positive
benefit and the genuine final v5 objective remain open.
