# Native exact installed-unit successor

2026-10-26. Source ready for independent review; **not compiled or executed**.
Only this checkpoint and `OrdinaryModule.lean` are owned here. Root owns review
adoption, native selections, assembly and Git. Canonical guard passed. No owner
state, native process, tests, product import, network or frozen source was used.

Fresh source predecessor:
`software/v5/ordinary_module_anchor/OrdinaryModule04.lean`, SHA-256
`901e4fc06351f6ad658eba9b5ea23ab644648646c8567fc035b057aa1883cfe8`.
Its hash remains unchanged. The new file was copied and edited only with
`apply_patch`; the selected installed package is untouched.

Current review cut `OrdinaryModule.lean` SHA-256:
`54f36991e4707b487a21f237e0854f6bd4127c2c2da805440c6119abf7cfd3d5`.

## Implemented relation

- `checkInventories` checks every selected row in both the kernel and frontend
  lookup maps, including name/key, safety and full exact inventory. This applies
  to the old full private checks, the new concrete public branch, added records
  and both fresh rereads. It never promotes hidden installed records.
- `classifyUnits` counts presence in both maps and rejects hidden or partially
  present units. It starts the semantic bound set from basis and authenticated
  anchor names, and advances it only after each original request unit. Existing
  singleton-theorem descriptor/proof matching stays separate.
- `matchNonTheorem` admits only safe singleton definition/opaque descriptors
  with `all=[name]`, or a complete supported inductive unit. Singleton descriptor
  rows must equal the expected inventory. Inductive descriptors are reconstructed
  from bounded selected actual types/constructors and compared canonically.
  All selected generated rows must share the descriptor's ordered type list;
  constructor ownership/indices and recursor rule constructors/field counts are
  checked. Exact inventory equality also covers all recursor RHSs and flags.
- Group lookup refuses names outside the selected unit. There is no ambient
  environment census. The protected accepted complete-unit premise remains
  explicit: parser inclusion or `all` metadata alone is not completeness proof.
- `OwnerRebind.scanSemantics` checks each matched non-theorem's actual type,
  body, recursor RHS and group references against the preceding bound set, plus
  current names only for a whole inductive unit. Its accumulated budget is the
  existing `nodeMaximum`; no resource limit is increased. Native literal and
  primitive semantics retain their existing pinned-profile premises.
- `checkMatchedPublic` requires concrete full equality for non-theorems. Only
  the unchanged singleton-theorem relation permits an existing public theorem
  stub after its full private proof match. Kernel and frontend maps are both
  checked; any actual public asymmetry that fails the relation remains a refusal.

`reportPartition` keeps the same fields, ordering and request binding. Its new
request-derived family check recognizes exact singleton descriptor rows or a
generated-only inventory with an inductive row. Full generated descriptor/actual
coherence is established during build; the unchanged protected worker binds the
exact request and pending partition across fresh rereads, which repeat exact
actual inventories. No free-standing report name list grants a realization.

The native anchor-plan parser recognizes `installed-exact-nontheorem` only for
singleton kind 1/3 or a kind 4/5/6 group containing kind 4. It does not invent a
mandatory constructor/recursor count. Added and matched outputs remain disjoint;
only added outputs belong to the module's own header. Existing registered-anchor
checks now inspect safe kind/name/universe headers in both lookup maps; they
still rely on the original complete relation and protected exact artifact chain,
not re-encoding old bodies. The Python owner supplies the new policy
`ORDINARY_EXACT_INSTALLED_PUBLIC_MODULE_V2`; the predecessor native protocol has
no separate policy field, and none was invented.

## Preserved boundary and remaining evidence

Both new-declaration `CheckedExtension.checkBatch` passes remain, followed by all
writer checks and separate private/exported rereads. The actual-added-delta
requirement, request/report schemas, 32-unit/4-MiB request limits, five artifact
parts, profile/foundation identities, output/header census, import restrictions,
fresh-output requirements and failure/adoption behavior remain unchanged.

Static source inspection checked the implementation against the accepted exact
relation, integration footprint and independent challenge. No Lean elaboration,
syntax probe, build or tests were run by this author. The separate reviewer is
examining this source cut; root's bounded typecheck and actual mixed realization
are later decisions. None of the source changes establishes actual installed
private/public equality for the retained AllClosure units, successful module
export, a proof-free query API, scientific growth benefit, or final v5.

## Source-only negative-test boundary review

Read root's `test_native_refusals.py` and `typecheck.py`; neither was executed or
edited. The two mutations target their intended new branches for the selected
successful cold ten-unit AllClosure request, subject to the unchanged runtime
and earlier baseline checks. No fixture change is required by this source trace.

`Membership.mem` is retained unit
`96863a2f1f2cd686538c2b39ff9cd8dcb6a4c76b81216a719a952874796151fc`.
Its descriptor and inventory both have hint `[1]`. The fixture changes only the
descriptor to `[0]`: both are valid canonical hint encodings, node/dependency/name
checks remain valid, and the untouched inventory still matches the positive
baseline. The descriptor-derived row then fails
`MATCHED_DESCRIPTOR_INVENTORY_MISMATCH` in `matchNonTheorem`.

`List.Mem` is retained unit
`e8d02c6c1c6e72fa4c1e8e6a9390b71eb2836653cb32b7bc9838dfa3e25f4b98`.
Its four rows are `List.Mem`, `List.Mem.rec`, `List.Mem.head`, `List.Mem.tail`.
Renaming only the recursor inventory name preserves the required descriptor
type/constructor census, unique bounded name grammar and kind-6 row shape.
Read-only inspection of all ten retained descriptors found **no** constant or
projection reference to `List.Mem.rec`; therefore processing the whole request
before classification does not introduce an earlier `UNBOUND_REFERENCE` for
this closure. With the chosen artificial name absent from both selected lookup
maps, presence is three of four and `PARTIAL_INSTALLED_GROUP` precedes inventory
comparison. Actual absence and baseline exact matches remain native-run facts,
not claims proved by the spelling of a source name.

The worker intentionally treats these mutated requests as unwarranted negative
fixtures: its entry checks bind files/anchor plan, not portable unit semantics.
The unchanged unit IDs are not new evidence or an admission attempt. Root's
selection must bind the already successful exact request/runtime; the test
script alone checks only cold anchor plus ten units, and is not a general
arbitrary-request proof of branch reachability. Its required exact refusal and
absence of pending/final success reports prevent an earlier different failure
from being counted as the intended pass.

`typecheck.py` invokes Lean on the pinned source without `--run`, so it does not
call the module worker's `main`. It is a bounded elaboration selection under the
outer Job and dependency/runtime pins, not an installed-module semantic test.
The independent reviewer owns the broader script/envelope review.
