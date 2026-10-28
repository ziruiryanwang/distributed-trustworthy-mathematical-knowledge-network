# Independent source review: advisory symbol projection

2026-10-28. **PASS for the selected source boundary and finite controls; no runtime
or deployment conclusion.** The reviewer read source/data only, ran the canonical
workspace guard, and authored the separately identified control source. No real
catalog was opened, product imported, test run, native process started or Git
state changed.

## Reviewed selection

| File | SHA-256 |
|---|---|
| advisory_context.py | `58e20183a71a58877a34e8c8ebd9fb384afe188bfced43d4e1b9c9eb1b66a47c` |
| CONTRACT.md | `5680322333d02c25d29398e65b38e8721bd0afba51c67e28db3e0e6dd5fe0d1a` |
| query.py | `8a5cbfeb6800ab53b84f34875872e8276797db60a762e297d5b9804f1c0be0d0` |
| API.md | `ed9528e30b8688da4e71010e0b0f3f5d540cbac41be7e437b4d8af599a43b2ec` |
| profile.py | `40b348cfaef96aebf9bda2ed6e09723153bc918fabee79948016d8daad71670c` |
| assemble.py | `9347d01177f2d234ef96fdd6832ce489d64502e13a9f720bfd41c2f925ee0b0a` |
| build.py | `889b56db11f588f2b0eb00b51d9308d57eb0ba1740e9292bc815970308dbb96e` |
| source-map.json | `8e706bd6437b10afa8d5293dfbd0614f9e435f1ab54121129f64bf40a426cbfe` |
| operator/prepare.py | `a61438a26a22695f5a87d4ffec41b233526141714578ef30288106df1c29e513` |
| operator/prepare_selected.py | `f38fc95746701daa37558fbdc78a89dec846b9495ae6bc126def00f81f77c159` |
| operator/compatibility.json | `7922cbab1222ac41381cb008fc9245cdf1740d5160c9cac366bc083ebce3be14` |

## Assurance argument

The intended assertion is a projection of **owner-recorded** name bindings, not
that retained compiled modules are currently usable. Snapshot hashing does not
derive the binding map from the snapshot; the protected actual-check commit and
immutable/no-rollback local records already supply that relationship. Omitting
snapshot bytes therefore removes a current availability/integrity assertion,
while retaining the existing conditional recorded-name meaning. The report
explicitly says `snapshot_integrity: NOT_CHECKED`,
`context_readiness: NOT_ASSERTED`, and `mathematical_acceptance: false`.

The helper's local subclass changes only generated snapshot access. Its scoped
tuple is restricted to exact native/imported `chunk.olean` paths, bounded size,
hex hash and `maximum is None`. The original `_validate_record` runs first and
reaches `_artifact` only after native root/operation checks or imported record,
source-record and path checks. Scope is cleared even on failure. No skipped
artifact is added to the original verified-artifact cache.

Outside that scope `_artifact` is unchanged: import audit bytes are still hashed.
Correspondence and original source-record bytes remain bounded, hashed reads.
Full selected ancestry, basis, no-shadow, module-parent chain, SQL-to-record
binding, committed operation, limits and semantic/foundation/implementation
checks remain in the original catalog. The helper does not stop at the first
matching name or bypass later conflicting metadata.

The inherited opener constructs `cls.__new__(cls)` and may invoke
`self.context(activation["selected_root"])` before returning for legacy imports.
Dynamic dispatch applies the same scoped artifact override during this eager
hydration; no constructor-initialized token is assumed. Its metadata/audit checks,
exclusive lock, withdrawal/activation checks and reservation recovery remain.
This is deliberately not database-read-only. The final `_active` check and
successful close precede return. If close or opening is uncertain, no successful
projection is returned.

The subclass remains local to `project`; no class, catalog, module plan, snapshot
path or grant escapes. Create/importing and reservation/commit/import methods
refuse. No global class or admission method is monkey-patched in production.
This is an API/call-path boundary under trusted in-process code, not a Python
object-capability sandbox against hostile introspection.

## Caller and operator boundary

Only symbol mode selects the helper. Exact-type/manual paths retain their prior
operations; exact-type context identity is still checked before name projection.
The new helper is captured and hash/size checked from the required profile role,
executed under a unique name, and included in final profile verification.
Its result has a strict field set, exact selected identities, only requested
keys, validated symbol IDs, consistent missing names and confirmed closure.
Any missing name yields no specs or output directory. Custody is explicitly
forbidden/omitted for the advisory symbol route; ordinary proof use is unchanged.

The caller rechecks inputs/profile and budget, closes before output, and retains
the predecessor's fresh final-marker/uncertain-rename behavior. The operator
success validator requires the exact advisory statuses, closed owner/unopened
custody and names-only input pin. It cannot silently consume the predecessor's
different custody contract. Its other actions remain unchanged.

## Package integration and cost

The profile delta only adds required `advisory_context.py`. The file-only assembler
starts from the explicitly pinned current build receipt, checks every source/base
byte and permits exactly five changed files plus that added helper: 149 unchanged
files and 155 total. It does not import a product or touch owner state.

The source map's 88 source pins were independently rehashed: all match. Relative
to the symbol map, only query/profile/LAUNCHER redirect and the added helper alter
source selection. Native lanes, outputs, runtime pins, tool selection and suffixes
are unchanged. The builder changes only prefix/map pin and consequent counts.
No installed core or implementation identity changes. A full native rebuild is
not needed to check this auxiliary delta.

This removes generated snapshot-byte reads, including eager legacy hydration,
from advisory projection. Whole local metadata/lineage/name processing and
package/runtime verification remain. No constant-time cold lookup, measured
speedup, search completeness or mathematical growth advantage follows from this
review. Root may select the finite controls and one actual advisory query; prior
native, mathematical, service and find campaigns need not be repeated.

## Control-source independence

The reviewer authored `control_tests.py`, so this note does not independently
qualify that test source. Its four groups use real catalog record validators
with synthetic metadata, fresh tiny audit/source files and inert opening/SQL/
activation doubles. A separate source check by the helper author or root is
required before selection. `CONTROL-PLAN.md` records the intended finite scope.
