# Typed DAG decoder implementation checkpoint

2026-10-20, `core_growth`. Source-only implementation under root's
`TYPED-ROW-IMPLEMENTATION-SELECTION.md`, using the reviewed
`TYPED-ROW-FAST-SUBSET.md`. Canonical root is
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Written scope

| Fresh owned source | SHA-256 |
|---|---|
| `software/v5/typed_rows/rows.rs` | `46319730b74a7f61685413cbd35995c5f4fd0906e0a9faaf7acfcfe71a5c04b3` |
| `software/v5/typed_rows/decode.rs` | `4fd38c378b70523c318bec55524a4170efefe78700f2ce0f87692cb3d5b4a3a0` |

No predecessor, kernel, commitment, policy, input fixture or evidence file was
edited. No compiler, tests, native checker, proof, memory inspection or Git
mutation ran. Compilation and actual differential behavior remain unestablished.
`core_release` owns independent review; root owns integration and any execution.

`rows.rs` exports checker-side `Row::Legacy(Value) | Row::Dag(DagRow)`, fourteen
exact syntax variants and `DagBinderStyle`. Exact variant and field names were
agreed with `core_search`, whose fresh correspondence/native mapper consumes
them. These public syntax constructors grant no mathematical authority.
At the independent control author's request, `Row` and `DagRow` derive Clone
so tests can consume a copied syntax row in the native mapper while retaining
the original decoder observation. `HybridFrame` stays non-Clone and privately
constructed; production code does not clone these rows as part of decoding.

`decode.rs` exports `decode(bytes) -> DecodeOutcome` with only
`Typed(HybridFrame)` and `UnsupportedRepresentation`. Every recognizer error,
including malformed/ambiguous raw syntax, chooses the literal old frame path
before semantics. This deliberately avoids duplicating legacy final diagnostic
selection. Root's integration alone performs that one fallback; this decoder
never invokes a second semantic check.

## Data path and immutable counts

The decoder uses the existing pinned `serde_json::Deserializer` directly, with
`DeserializeSeed`/`Visitor` implementations for the frame, rows, typed payloads,
typed fields and generic subtrees. There is no initial full Value parse and no
generic reconstruction of supported DAG rows. A constant payload-field schema
stores a small temporary vector of typed fields, then constructs its DagRow.
Outer payload/index key order is arbitrary: a temporary DagRow receives its
checked-width outer index only after the complete row closes.

The adopted policy's first 413 rows remain generic. Suffix declaration rows
retain their full original singleton object and generic payload, including
ordinary `all` and inductive metadata. Non-row fields remain unextracted generic
Values. Parent shapes are intentionally not pre-extracted: root's aggregate
census still checks them sequentially after the original earlier charges.

`HybridFrame` owns private non-row fields, mixed rows, node count and maximum
depth. It provides only read-only accessors; no caller supplies counts or mutates
the counted syntax. `into_parts` consumes the token within the module crate at
the old relation extraction point. Root inserts an empty rows placeholder for
the unchanged non-row input extractor and separately passes the actual mixed
rows; that placeholder does not rebuild raw typed DAG rows.

Each actual scalar/container consumes one virtual old Value node at its actual
depth; keys consume none. Generic subtrees use the same rule. Thus the fourteen
row count formulas in the reviewed table are obtained by construction, without
hard-coded per-row totals or depth offsets. Counters are private and discarded
on every unsupported path. The original module node/depth caps and raw byte cap
are enforced; the same JSON parser's default recursion protection remains.

## Source-level acceptance argument

For a returned Typed frame:

1. The exact seven top keys are unique and present. `rows` is an array. Every
   supported suffix DAG row has exactly its matching index and constructor.
   Every typed payload has exactly its specified fields, including escaped-key
   duplicate detection by decoded String equality.
2. Numeric values use `deserialize_any` and accept only `visit_u64`, followed by
   checked `u16`, `u32` or actual-target `usize` conversion. Negative/i64 and
   floating visits refuse. No derived scalar deserializer introduces coercion.
3. String unescaping, Boolean contents, binder styles, pair arity and integer
   vector order match the reviewed schema. No name normalization, references,
   owner checks or theorem validity enter representation selection. `nondep`
   remains arbitrary Boolean; `const.us` has no new reached-only arity cap.
4. `StrictSeed` retains all generic scalar/container Values with the old unsigned
   numeric and duplicate-key domain. Foundation/declaration fields are not
   projected away. Exact scalar observations plus container induction give the
   original strict Value interpretation; counting the same induction gives the
   same successful node/depth totals.
5. Any unsupported representation/error discards its tentative state and gives
   root no typed token. The old pipeline then determines its success/refusal.
   The decoder does not catch correspondence, kernel, commitment or graph
   errors, so these cannot trigger fallback.

This establishes the intended syntax/refinement obligations at design/source
inspection level. The separate typed correspondence and native constructor
must still establish identical observations, traversal/resource checks and exact
journals/premises. Root's source integration must preserve aggregate update order
and one logical charge. No source claim here is a machine-checked code theorem.

## Cost and remaining narrow review

Supported DAG maps, persistent JSON key storage and Value-to-native conversion
are removed. Decoding still allocates transient decoded keys, typed field vectors,
strings/universe vectors, and the required canonical/native mathematical data.
Do not claim every key allocation disappears or count the predecessor's existing
singleton native flatten-buffer saving twice.

Unsupported input can pay a bounded typed prefix plus the old complete path.
All such work remains charged to the original physical operation; equal logical
acceptance is not identical completion under a fixed CPU/wall cap. This change
has no measured time/proof saving yet.

Next is the already assigned independent source review and root's finite
changed-boundary controls, if selected. Check constructor/count/raw spelling
boundaries, exact fallback, arbitrary field order and generic metadata retention;
then compare exact retained journals/premises through actual old/new entry points.
Do not expand this into typed declarations, a new wire, extra proof policy or a
production proof campaign without a separate root decision.
