# Independent review of typed correspondence and native consumption

2026-10-20, reviewer `core_growth`, consumer author `core_search`. This scope
covers only the fresh correspondence and native parser successors, against their
actual frozen predecessors and the agreed row schema. Root census/dispatch and
my decoder are independently reviewed by `core_release`, not self-adopted here.
No compiler, native run, tests, proof operation or memory inspection occurred.

## Disposition

**No blocking defect found in this source comparison.** On the finite decoded
subset and current 32-/64-bit targets, the changed observations preserve the
ordered correspondence work and exact native record fields. This is source
clearance for the scoped consumer implementation, not compilation, empirical
equivalence, successful proof production or v5 acceptance.

| Source | SHA-256 |
|---|---|
| Fresh `software/v5/typed_rows/module_correspondence.rs` | `eeb4a45033588060216eadeda1753181d838e54d48778757790001d8dd574699` |
| Fresh `software/v5/typed_rows/parser.rs` | `9bb168290d5ec2234c259c71e92f47cfec5c91d98ee0c4219f97210eac63f19d` |
| Row schema `software/v5/typed_rows/rows.rs` | `46319730b74a7f61685413cbd35995c5f4fd0906e0a9faaf7acfcfe71a5c04b3` |
| Old `software/v5/modules/native/proof_memo/module_correspondence.rs` | `7877ee22c7e1d4350858e67c8cebbedf057dee1820cd9f61940e37cf51f6508e` |
| Old `software/v5/modules/native/checker/src/parser.rs` | `7a183a1c9e6ff3ee2c32ee6542ed85d3de0835b00e235f80f6982c3e7038d218` |

## Concrete source findings

Read-only `git diff --no-index` identified every source change. Independent
exact text comparisons additionally found these three regions byte-for-text
equal under the same UTF-8 read:

- Native source from `pub fn decode_owned_row` through EOF: unchanged. This
  includes both old row decoders, native row schema, ordered application and
  finalization. The only executable parser insertion is the new typed mapper.
- Correspondence from `fn body_match` through the public-entry documentation:
  unchanged. Ordinary `all`, imported roles, body obligations and complete
  inductive/constructor/recursor metadata matching are retained.
- The public correspondence function body after its changed signature:
  unchanged. Group and descriptor order, matching indices, duplicate checks,
  result assembly and pending structural obligations retain their old code.

The new file reexports the actual legacy input/output types and old entry point,
rather than creating lookalike result types or redefining the fallback. Its
legacy module still owns the prior controls. The typed entry is separately named.

### Inventory and borrowed observations

`Inventory` retains generic declaration references and canonical name Values.
Only level/expression row references change to `DagRef::Legacy | Typed`.
Foundation rows cannot enter the typed branch: the first row must be Legacy and
each later typed row asserts its position is at or after the foundation prefix.
The foundation equality itself remains a separate relation obligation.

For typed names, predecessor/index ordering and parent bounds are checked in the
same sequence before constructing the canonical name and running `name_parts`.
The string/number component is the same scalar that old JSON interpolation
produced; these necessary canonical names are not raw row reconstruction.
Typed levels/expressions perform the same ordered-index checks before insertion.

I checked every `PayloadRef` arm against the fourteen variants. Scalar, pair,
universe-list and named-field access supplies the old value without allocating
generic row objects or universe arrays. `DagRef::split` returns the same tag;
the inventory's variant dispatch prevents a typed expression being stored in a
level slot. `PayloadRef::fields` verifies the same fixed schema for typed data,
whose actual field set was already established by the strict decoder.

The casts from `u32` to `usize` are exact on the selected native 64-bit and guest
32-bit targets. `proj.field` already is target `usize`, and bvars retain u16.
This review does not establish portability to a hypothetical narrower pointer
target; that would require checked conversions or an explicit build exclusion.

### Traversal, reached-only checks and memo accounting

Both canonical reconstruction and syntax-only memo validation preserve these
actual orders, not merely their sets of children:

| Constructor | Preserved ordered work |
|---|---|
| `max` / `imax` | Read both references; check both bounds; left child then right |
| `const` | Exact payload fields, universe arity; ordered universe traversals; then name/owner reference |
| `app` | Function child then argument child |
| `lam` / `forallE` | Binder-name bound, binder style; type child then body child |
| `letE` | Binder-name bound and `nondep=false`; type, value, then body |
| `proj` | Type-name/owner reference, projection index, then structure child |

The reached-only universe arity and `nondep=false` checks are still inside the
same reached expression branches. Unused typed rows are not newly traversed by
correspondence, while unchanged native application still consumes every row.
Canonical binder strings are reconstructed with identical content; no binder
style or variable interpretation is normalized.

`visit`, `SyntaxSummary`, memo lifetime/key sets, cache-hit budget/depth check,
summary inclusion and insertion are unchanged. Replacing scalar access with a
borrowed view introduces no new visit. The old ordered descent remains when a
memo hit would exceed the logical work/depth budget. Thus equality of view
observations gives equality of ordered logical visits and first semantic/resource
failures on the selected well-typed raw shapes. Allocation timing and physical
CPU completion are not claimed equal.

### Native mapper

The new mapper exhaustively matches all fourteen DagRow variants and constructs
the corresponding existing private native variant plus its exact BackRef.
Checked the easy-to-confuse mappings explicitly:

- `NameStr.text` becomes `Cow::Owned(str)`; no borrowed input lifetime or leak.
- `ExprApp.fun` maps to native `fun` (wire `fn`), in the original field order.
- `ExprConst.levels` maps to native `levels` (wire `us`), preserving order.
- Lambda/Pi `name/ty/body` map to `binder_name/binder_type/body`.
- `DagBinderStyle::InstImplicit` maps to native `BinderStyle::InstanceImplicit`,
  whose unchanged Serde spelling is `instImplicit`.
- Projection `type_name/field/structure` map to native `type_name/idx/structure`,
  retaining target `usize` exactly.
- `ExprLet.nondep` is copied, not forced to false in native decoding.

No declaration variant is newly constructed. No kernel or apply/finalize code
changes. Syntax constructors are not certificates; relation/foundation/group
binding and actual conditional checking remain required after mapping.

## Remaining validation, without scope growth

The already assigned finite differential controls should catch actual compiler
or wiring mistakes and compare old/new successful outputs, constructor mappings,
reached/unused semantics and the retained ordinary suffixes. A full machine-
checked source refinement proof is not supplied by this review. It also does
not price production proofs, establish positive full-cost growth, or authorize
any runtime on its own. No extra consumer mechanism is recommended.
