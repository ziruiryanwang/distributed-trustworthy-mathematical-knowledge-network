# Typed DAG correspondence and native mapping: fresh source checkpoint

2026-10-20. Owner: core_search. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
Selected by [TYPED-ROW-IMPLEMENTATION-SELECTION](TYPED-ROW-IMPLEMENTATION-SELECTION.md).
**Source implemented; not compiled, executed, proved or adopted.** No predecessor
bytes, installation, Git index or runtime state were changed.

## Exact delivered source

| Fresh path | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/typed_rows/module_correspondence.rs` | 41,530 | `eeb4a45033588060216eadeda1753181d838e54d48778757790001d8dd574699` |
| `software/v5/typed_rows/parser.rs` | 47,604 | `9bb168290d5ec2234c259c71e92f47cfec5c91d98ee0c4219f97210eac63f19d` |

Preserved predecessors remain respectively
`software/v5/modules/native/proof_memo/module_correspondence.rs`
(`7877ee22c7e1d4350858e67c8cebbedf057dee1820cd9f61940e37cf51f6508e`)
and `software/v5/modules/native/checker/src/parser.rs`
(`7a183a1c9e6ff3ee2c32ee6542ed85d3de0835b00e235f80f6982c3e7038d218`).
Fresh source uses LF; neither frozen file was normalized.

## Agreed integration interface

Root binds the exact frozen memo predecessor as
`nanoda_lib::module_correspondence_legacy`, and this successor as
`nanoda_lib::module_correspondence`. The successor reexports:

```rust
pub use crate::module_correspondence_legacy::{
    BodyOpening, GroupBinding, MatchedGroup, StructuralCorrespondence,
    check_rows_correspondence_conditional,
};
```

Thus old module-relation fallback uses the actual old function, not this new
walk pretending to be unchanged. Its shared input/output types are identical
Rust types, avoiding separate incompatible declarations.

The new entry is:

```rust
pub fn check_typed_rows_correspondence_conditional(
    rows: &[crate::typed_rows::Row],
    foundation_rows: usize,
    bindings: &[GroupBinding],
    openings: &[BodyOpening],
) -> StructuralCorrespondence;
```

`crate::typed_rows` is core_growth's `rows.rs`, using the agreed mixed
`Row::Legacy(Value) | Row::Dag(DagRow)` and fourteen variants. A typed foundation
row is rejected; decoder/root must retain and exactly authenticate the 413
foundation Values. Suffix declaration Values remain unchanged.

Native parser successor adds:

```rust
pub fn decode_typed_dag_row(row: crate::typed_rows::DagRow) -> OwnedExportRow;
```

This is a syntax constructor, not a mathematical-success token. After
correspondence, root dispatches generic rows to existing
`decode_corresponded_owned_row`, typed rows to this fieldwise mapper, then all
owned rows in original order to the unchanged `parse_owned_rows` and conditional
module check. No caller-provided receipt/authority flag is added.

## What changed, and what did not

The parser adds only the fourteen-variant consuming match, four binder-style
mapping and a documentation correction. Strings become owned Cow strings;
`fn/us/struct` map to native `fun/levels/structure`; projection `usize`, bvar
`u16`, indices `u32` and every other field retain their exact values. BackRef
domain is derived from the variant. All old decoders, `apply_row`, parser
configuration, finalization and kernel code remain unchanged.

Correspondence keeps its old semantic structure but borrows a `DagRef`,
`PayloadRef` or `IndexListRef` instead of demanding a generic row. Their legacy
branches read old Values; typed branches expose the same scalar/list observations.
Universe lists and max/imax pairs do not become temporary `Vec<Value>`s.
Name rows still produce the same canonical name arrays, and expansion still
produces required canonical type/body Values. These semantic outputs are not
raw-row reconstruction.

Inventory inserts typed name/level/expression rows under the same continuity,
backreference and name rules. Generic rows retain the old inventory path and
all declaration metadata. Generic declaration matching, foundation namespace
rules, group ordering and body obligations are unchanged. Typed expressions
retain reached-only arity and `nondep=false` checks: merely parsing an unused
`nondep=true` row does not introduce a new universal rejection.

The four traversal routines change only row/payload observations and scalar/list
accessors. Their child evaluation order remains: const universes before owner
reference; app function before argument; lambda/pi type before body; let type,
value, body; projection owner/index before structure. Memo lifetime, summaries,
visit charging, depth checks, sufficient-hit shortcut and insufficient-hit
original recursion remain.

## Source-only checks performed

Ordinary file/hash reads and exact textual comparisons establish that these
sections match the memo predecessor byte-for-byte after line-ending comparison:

- Generic declaration matching (`body_match` through `match_declaration`).
- Canonical name, field and tagged-value helpers.
- Syntax summary/memo structure.
- Generic declaration-record extraction, visit charging and reference lookup.
- Memo hit-budget logic and top-level fresh-memo entry methods.
- Group matching/result construction after inventory creation.

The parser diff is only the new constructor and its related documentation.
The fourteen fields and four binder mappings were manually checked against
the exact predecessor native enum and the agreed `rows.rs`. The new borrowed
views were manually compared against all original payload accesses. These are
source checks, not Rust type checking or evidence of runtime agreement.

The old correspondence's internal control module remains attached to the
separate old module. The new successor does not incorrectly include that same
fixture file against a changed private Inventory signature. Root/reviewer owns
the separately selected differential controls and source assembly.

## Acceptance and next boundary

This implements the row observation/native constructor parts of the design
argument. The decoder's strict raw/virtual census, root's exact foundation,
module commitments and one-census aggregate dispatch remain separate owned
components. No semantic failure may fall back; root must select the old/typed
frame before invoking either correspondence path. These files do not decide
fallback, fund a retry, certify a module, or omit recursive receipt obligations.

core_release has the exact files/hashes for independent source review. Relevant
future controls compare all fourteen mapped native variants, supported typed
and actual old correspondence outputs, reached/unused boundary behavior, memo
work/first failures and retained exact J/premises. No build/control/proof run is
selected by this checkpoint. Removed generic allocation/conversion work is not
yet a measured proof saving, affordable frontier supply or completion of v5.
