# Typed suffix rows: implementation review and minimal differential controls

2026-10-20, `core_release`. Source-only independent review of
`TYPED-ROW-IMPLEMENTATION-SELECTION.md`, exact table `8360a87e` and prior
design review `f76eac1f`, against the actual bounded parser/census/module relation,
input extraction and native row representation. No compiler, proof, test,
performance run, RAM work or Git mutation is selected by this note.

**Current disposition: implementation scope is appropriate; actual successor
code is not yet cleared.** This checkpoint names decision-changing checks and
the smallest proposed comparison, not another generic architecture audit.

## Concrete integration obligations

The old production chain is strict `parse_bounded(bytes)` -> private immutable
Value/count token -> aggregate `Census::charge` -> `check_validated` ->
`input::extract` -> foundation/correspondence -> native decode/apply -> exact J
and original-order parent journals. New dispatch must preserve those boundaries.

1. **Do not eagerly extract non-row semantics in the decoder.** Old aggregate
   charge changes maximum depth, then nodes, rows, bodies, parent edges and each
   parent's opening count, before `input::extract` checks image/rank/body fields.
   Valid JSON with a bad image/body scalar must retain this same charge-before-
   rejection behavior. Exact-object unsupported shapes may use the whole-frame
   old path; tentative typed counts must not leak into it.
2. **The census token is not caller-asserted truth.** Keep raw non-row Values,
   row storage and counts private and immutable until consumption. Expose only
   borrow/count methods needed by census. The agreed `into_parts` may move
   non-row Values into the old extractor with an empty row placeholder at the
   original point, provided every later row-bound/foundation/correspondence/native
   operation uses the actual mixed rows. The placeholder must never become
   the mathematical row inventory or reported census.
3. **Foundation equality must remain exact.** A borrowed mixed-prefix matcher
   may avoid cloning, but must reject a short prefix or any typed prefix row,
   compare all 413 unchanged Values through the original recursive equality,
   and retain ignored metadata. Copy the old comparison/data unchanged; only
   the mixed iterator adapter is new. Suffix length does not repair a prefix.
4. **Dispatch is structural once, not exception-based retry.** Unsupported raw
   shapes invoke the literal complete old entry point on original bytes before
   semantic checking. A typed path's correspondence/kernel/hash/parent/graph
   failure cannot invoke old checking. Aggregate dispatch is per module frame,
   not a restart of previously charged/checked frames or receipt obligations.
5. **Representation saving must survive consumers.** Direct DAG decoding must
   reach borrowed correspondence observations and parser-private fieldwise
   `OwnedExportRow` construction. Recreating generic raw row maps/arrays or
   universe `Vec<Value>` is not this intervention. Required canonical semantic
   type/body Values remain legitimate. Native application/finalization and
   cryptographic parent discharge stay unchanged.

## Proposed focused controls: not authorized to run

Use actual retained old entry points as oracles, not a second hand-written
checker. A single prospective native-free/host control binary can cover most
changed representation rules; any actual native module comparisons must be
separately selected after exact source/build review. No RISC0 proof is needed.

| Group | Actual comparison and falsifiable assertion |
|---|---|
| Direct fourteen-tag mapping | Decode exact canonical raw rows through the new typed visitor and compare parser-private native rows with old `decode_corresponded_owned_row`; `OwnedExportRow` already has exact `PartialEq`. Cover reversed outer/payload key order, empty/nonempty universes, all four binder styles, both let flags and target-width projection values. Do not rebuild generic rows in production merely to support this test oracle. |
| Strict raw boundary | Compare new selection/old strict parse for escaped-equivalent duplicate keys, negative/`-0`/fraction/exponent spellings, out-of-width integers, invalid strings/UTF-8, truncated/extra tokens and normal recursion limits. Ambiguous recognizer refusal must take old whole-frame fallback; malformed rejection needs old refusal. |
| Virtual census | For supported row envelopes, compare new private token counts with actual old `parse_bounded`, including nested rows, empty and nonempty universe arrays and generic declaration metadata. Assert exact nodes and maximum depth, not typed object count. Small counter seams may exercise near/over limits without allocating million-node fixtures. |
| Aggregate charge ordering | Start old/new actual census from equal seeded states at each nodes/rows/bodies/edges/openings boundary; compare successful state and partial state on failure. Include valid JSON with malformed image/body leaves, short/missing/extra records and one valid prior frame followed by unsupported/refused frame. No counter reset or doubled prefix charge. |
| Fallback versus semantic rejection | Positional top/parent/row shapes, aliases/extra fields and unsupported constructors must reach the unchanged old frame path once. Structurally typed bad foundation/commitment/parent metadata must stay on the typed semantic path and reject without fallback. A test-only dispatch trace may count branch selection; no caller-visible authority flag. |
| Retained end-to-end equivalence | Compare actual old/new module entry points on the two immutable retained ordinary suffix frames (942 and 596 rows after foundation) and the retained two-member aggregate input. Require identical success, exact encoded J, ordered parent journals/claims, aggregate header and census. Check that both frames actually select the typed branch; equality obtained by falling back everywhere is not success for this intervention. |

The retained fixture identities are in `TYPED-ROW-FAST-SUBSET.md`; reuse their
exact bytes and existing preparation, not a newly invented easier workload.
Timing, rows processed and file size are not acceptance equivalence or proof
speedup. Check both success directions; one-way soundness permits unwanted
rejection of old-valid mathematics.

Some old native bad-backreference paths call `std::process::exit`, so do not
assume `catch_unwind` can contain every negative native control. Direct equality
of private native records plus unchanged application is the cheap source-level
argument for those cases; any selected process-exit control needs a finite child
under the existing owner envelope. This does not justify a new supervision system.

## Source review queue

Await concrete `rows.rs`, `decode.rs`, correspondence/parser successors and
root relation/census/foundation dispatch. Review exact changed functions and
preserved old branches. First blocking concerns are eager extraction, mutable
counts, reconstructed raw DAG trees, target-width coercion, changed memo/work
order and semantic-failure fallback. Additional runtime work needs a demonstrated
remaining implementation uncertainty and root's fresh finite selection.

This representation opportunity is relevant to producer cost; it is not an
established speedup, affordable recursive certificate, net useful-growth result
or final-v5 release.

## Actual source review, subsequent 2026-10-20 checkpoint

**No blocking source defect found in the ten implementation files below.**
The earlier queue and proposed controls above remain historical planning, not
the current readiness label. This clears the implementation for root's bounded
compile/control decision; it is not compilation, execution, adoption or a
performance result. The controls authored by this reviewer require independent
review by another agent/root, not self-certification.

| File under `software/v5/typed_rows/` | Reviewed SHA-256 |
|---|---|
| `rows.rs` | `46319730b74a7f61685413cbd35995c5f4fd0906e0a9faaf7acfcfe71a5c04b3` |
| `decode.rs` | `4fd38c378b70523c318bec55524a4170efefe78700f2ce0f87692cb3d5b4a3a0` |
| `module_relation.rs` | `1000932993105188773b30d94571908a5607657c1ca865e79a7dae318460a699` |
| `module_lib.rs` | `1708b009eae0616f47524ecfaef732225516c72a47c784a261b214f20df685cd` |
| `foundation_static.rs` | `72abf9ac888e152363757920988831b5aaf82e3d545fef9b1fe9a0101a081763` |
| `census.rs` | `355ab4e2b1ae1b2b5f787f01db513d54cfeb107c2d93dc62ba6b50fdc27e0cba` |
| `aggregate_lib.rs` | `ce67e7ee6a8ae08382dd8e1b36d95798b42eda28f7cb68432451a0b15045ca40` |
| `aggregate_relation.rs` | `7608a1870f4bde2b02c71e06987f1ef0395bcd0abf805f06f8c56afaa2900f33` |
| `module_correspondence.rs` | `eeb4a45033588060216eadeda1753181d838e54d48778757790001d8dd574699` |
| `parser.rs` | `9bb168290d5ec2234c259c71e92f47cfec5c91d98ee0c4219f97210eac63f19d` |

The direct visitor increments one virtual node for every old Value node,
including frame/row/payload containers; keys are not nodes. Foundation rows
and all declaration metadata remain generic strict Values. DAG numeric fields
use `deserialize_any` with unsigned widths, not coercing numeric deserializers.
All keys are decoded before duplicate recognition. Same-deserializer recursion
and original-byte fallback preserve the old parser's final authority. Non-row
fields remain generic until the original extraction point. `HybridFrame` fields
and counts are private; syntax-only Row/DagRow Clone adds no authority/token
constructor and is used only by differential controls.

The relation's empty `rows` placeholder is consumed only by unchanged input
extraction. Every later row bound, exact foundation comparison, correspondence
and native decode uses the real mixed rows. Legacy input and its old conditional
relation remain literally linked. No semantic error is caught to retry legacy.
The exact old foundation comparison is retained and the new borrowed adapter
rejects every typed prefix row. Aggregate state mutation remains depth, nodes,
rows, bodies, parent edges, then ordered openings, including partial state on
refusal; unsupported syntax is discarded before any charge.

The correspondence diff replaces observations with borrowed typed/legacy views,
not semantic algorithms: same domain/index/backreference order, canonical names,
reached-only let/universe restrictions, traversal order, per-call memo context,
work/depth charges and failed-hit recursion remain. Declarations and result
assembly retain the old logic/types. The fourteen native constructors map
fieldwise to the private existing row schema, including `InstImplicit` to
`InstanceImplicit` and target-width projection index. Original native
application/finalization/kernel routines are untouched. No generic typed suffix
Value tree is reconstructed in production; canonical semantic Values still
required for commitments/correspondence are unchanged.

## Authored eight focused controls: not executed

`controls_root.rs` links the fresh production checker/module/aggregate crates
and includes exact new census plus old bounded census as an oracle. Eight
tests cover the six planned groups: all fourteen direct native maps; declaration
metadata/unreached semantics; strict raw/width fallback; recursion/decoded
duplicates; exact aggregate charge and partial-failure order; structural fallback
versus early typed semantic rejection; actual old/new retained module conclusions;
and exact saved aggregate output. The last two require the three paths below,
verify their hashes, and fail when absent; they never silently skip.

- `DMKN_TYPED_PACKET`: retained `delta-reprepare-01/evidence/delta-packet.json`.
- `DMKN_TYPED_AGGREGATE_INPUT`: retained
  `aggregate-claims-controls-02/evidence/actual-two-delta.bin`.
- `DMKN_TYPED_AGGREGATE_EXPECTED`: retained
  `aggregate-claims-controls-02/evidence/actual-two-delta/stdout.txt`.

No old aggregate rebuild is needed: the actual old/new module entry points are
compared for both deltas; the new aggregate is compared to exact saved header,
ordered claims, member journals, census, edges and wire length, supported by the
unchanged graph-source argument. Retained typed-row counts must be 930 and 583,
so blanket fallback cannot pass. Only known positive native fixtures execute;
no unsafe bad-backreference process-exit negatives are selected.

Initial controls identities: `controls.rs`
`4de1694aa8a90b83ffae9afa8f57fd7016e9a87509a6b4b6f9163d23301d2e02`,
`controls_root.rs`
`5c0232d74e052e55d159803d57c1246fab5c10c3141abddc24d649e8d297bb68`.
