# Exact installed declaration reuse: integration footprint

2026-10-26. Source/data-only followup; complete. Root owns selection, builds,
execution and Git. No implementation, product import, native probe, owner-state
opening or new experiment. The independent semantic relation is owned separately
in `EXACT-INSTALLED-RELATION.md`.

## Decision and exact predecessor

Conditional on the independent exact relation, the smallest coherent change is
**three runtime source payloads**, plus a new file-only assembly selection and
short compatibility documentation. Native classification alone is insufficient:
report validation, both fresh imports and saved anchor tags must agree. Do not
select implementation until root has resolved the actual target closure and the
independent relation; no equality of the installed records is claimed here.

The current selected package is
`experiments/v5-local-checks/transport-release-handoff01/suite/assembled/package`,
PROFILE SHA-256 `b047d4492da79e363fcd154144a6d9088a93100fde7aac3c385f3a296a41dad7`.
Its exact predecessor mappings are in
`software/v5/ordinary_bounded_operations/source-map.json`, `copies`/`sources`.
Direct source hashes and the installed PROFILE agree:

| Future replacement payload | Frozen source predecessor | SHA-256 |
|---|---|---|
| `module/OrdinaryModule.lean` | `software/v5/ordinary_module_anchor/OrdinaryModule04.lean` | `901e4fc06351f6ad658eba9b5ea23ab644648646c8567fc035b057aa1883cfe8` |
| `authoring/py/module_export.py` | `software/v5/ordinary_module_anchor/module_export.py` | `85f9a2b5695dd90dd888bd3868f51a41904cb0b2d0d14335abe0b65d5182b65c` |
| `authoring/py/anchor_store.py` | `software/v5/ordinary_module_anchor/anchor_store.py` | `a244eaf2764b6a51f4006447eebe3b69529a46bf376f999804a99f23661a929e` |

Create separately selected successors; never edit those used sources or the
installed package. All paths/line references below refer to these predecessors.

## Native changes: one complete integration, not one relaxed refusal

In `OrdinaryModule04.lean`:

1. `classifyUnits:260`: retain the existing exact singleton-theorem branch. Add
   only the independently justified all-present non-theorem branch. Partial
   groups, descriptor/inventory disagreement, unsafe/partial/axiom outputs and
   unequal private records still refuse. Reuse codec/OwnerRebind primitives;
   preserve bounded semantic-reference scans, atomic grouping and the exact
   basis/anchor/preceding-unit interpretation. Decoding a descriptor alone does
   not establish its equality to the claimed inventory or complete generated
   output group. The relation review governs these additional obligations.
   Its current `(env, units)` signature needs the basis/anchor prefix (or an
   equivalent authenticated reconstruction); update the `run` call and advance
   that prefix in original request order. Scanning against the final whole-batch
   name set would wrongly permit later/unbound dependencies. Check both selected
   kernel and frontend records; the current frontend-only inventory lookup is
   not a substitute for detecting a hidden kernel collision.
2. `checkMatchedPublic:228`: retain the theorem-specific public theorem/stub
   relation. For matched non-theorem rows require full safe concrete inventory
   equality in the exported view; an axiom-shaped opaque/definition handle is
   not an exact match. Existing `checkInventories:211` supplies the strict row
   comparison, subject to complete-group conditions from step 1. Keep both
   calls before writing and both private/public delta checker passes in `run`.
3. `reportPartition:297`: reconstruct the same matched/added partition from the
   protected original request for supported descriptor families. Preserve exact
   indices, ordering, inventory/name lists and counts. Do not accept a free
   standing report's claim that an arbitrary group was matched. `rereadPending`
   and `reread:585` must still establish private exact rows, exported exact rows
   for non-theorems, and the unchanged theorem relation in separate processes.
4. `readAnchorPlan:405`: admit one distinct, explicitly named exact non-theorem
   realization tag, with the supported kind/group constraints. Do not label it
   `installed-singleton-theorem`. Preserve disjoint added/matched names and the
   complete unit/name binding census. Existing `checkAnchorHeaders:517`,
   `checkAnchorRecords:543` and `checkWrittenHeader` need no broader acceptance:
   non-theorem public records must still be concrete with the same kind/ordered
   universes. Only **added** declarations belong in the new module's own header;
   matched declarations remain in its pinned imported environment.

Keep `NO_NEW_MODULE_DECLARATIONS` and the requirement that a new module have an
actual added delta. An all-installed query target is a separate workflow, not a
reason to expand this task. Keep 32-unit/4-MiB limits, source/import restrictions,
five artifact parts, both fresh rereads, protected bindings and failure behavior.

## Python, reports and anchors

`module_export.validate_partition:76` and
`anchor_store._commit_generated:502` each independently require the singleton
theorem descriptor today. Both must classify the proposed matched non-theorem
families from the unchanged canonical request, preserve descriptor/inventory
shape consistency and account for **complete units**, not individual rows.
The native relation remains the mathematical check; these Python checks bind
its reported partition and registered interpretation to that exact request.

`anchor_store._units:266` must recognize the new exact non-theorem tag: supported
singleton definition/opaque or generated inductive/constructor/recursor unit,
never an arbitrary mixed-kind list or theorem/axiom under this tag.
`_commit_generated` must derive the tag from the
validated unit family, never from an independent report label. Its record and
plan carry exact UnitIDs, ExportIDs, ordered universe parameters and inventory
hashes as before. `load:349` still checks every selected anchor binding against
the current owner context and hashes the complete protected artifact chain.

No new report fields are necessary: `matched_unit_indices`, `units_matched`,
matched/added names and inventories already represent a whole-unit partition.
The existing pending/output report schema and assurance strings are generic.
With those field sets unchanged, **`module_worker.py` can remain byte-identical**:
it binds inputs, parents, pending report and all artifacts across build/private/
exported phases and promotes success only after both rereads. Its anchor parser
does not assign mathematical meaning to the realization string; native parsing
and the protected store do. If root instead changes report schemas/fields, the
worker becomes a fourth payload and all three report validators must change
together; that is avoidable for this slice.

Likewise `module_closure.py` can stay unchanged. It collects complete exact
evidence and uses a registered frontier of exact units/names; it neither guesses
installed declarations nor interprets the realization tag. There is no change to
owner CLI/launcher, query interfaces, receiver, semantic/foundation descriptors,
portable identities or evidence format. `OwnerConstruction` is not in this path.

Use a newly explicit policy string instead of the old
`...EXACT_THEOREM_MATCH_PUBLIC_MODULE_V1` in `module_export.py:22`.
`support_descriptor:27` already includes native/controller/store/collector/
worker sources, owner/profile, installation and six five-part native helpers.
Consequently changed source bytes and policy produce a new support ID and new
module materialization key. **Old anchors fail `ANCHOR_RECORD_SUPPORT` when
explicitly loaded under the successor.** No migration or trust transfer follows.
Closed old operations remain stored and charged; the sidecar census does not
reinterpret their records. A new cold export can use the same compatible owner
while preserving old artifacts, subject to existing capacity/cleanup limits.
Keeping the existing support-bound record/plan field schemas with an explicit
new realization enum is sufficient; old readers reject the unsupported enum or
support identity. Do not claim cross-support anchor compatibility.

## Assembly and build boundary

Prefer a fresh terminal **file-only overlay of the selected final package**:
verify the entire predecessor map, replace exactly the three payloads, generate
a new PROFILE and receipt, and preserve every other byte. Historical
`ordinary_module_anchor_package/assemble04.py` demonstrates a source-only overlay,
but is hard-pinned to an older package and one replacement: it is a pattern,
not an executable instruction for this successor. Root must select the fresh
overlay's exact source/input pins and output location before any execution.

This avoids rebuilding unchanged helpers. The existing worker invokes selected
Lean `--run` on `module/OrdinaryModule.lean` for each phase; that source is copied
directly by the distribution builder. Reusing already built `OwnerRebind`,
`OriginalDecl` and checking helpers does not require changing their sources or
artifacts. Any later Lean elaboration/typecheck/export is still a **new runtime
selection**, not part of this source decision or a file-only assembly claim.

The old reproducible recipes remain frozen: bounded-operations build pins its
source-map SHA, transport assembly independently pins that map and checks the
baseline projection, and the release/workflow bundles pin those recipes. Do not
replace a base source-map under those pins or insert changed files into an old
archive. A later distributable successor can ship the new three sources and
terminal overlay recipe against the unchanged documented build/overlay chain.
Updating a source bundle/repack is a separate release selection; it is not needed
to decide or implement the narrow source boundary.

## Retained target and smallest decision-changing evidence

Use the exact target and ten-unit closure already identified in
`RECEIVED-VOCABULARY-QUERY.md`, under
`experiments/v5-local-checks/concept-theory-b-export-01/bundle`.
This followup read all ten inert units and checked their lengths/SHA-256 against
the retained manifest: **62,079 bytes; five definition descriptors (tag 0), five
generated descriptors (tag 3); rows kind 1/4/5/6 = 5/5/6/5**. There are no theorem
or opaque rows. The candidate installed subset is `Membership` (three rows),
`List.Mem` (four), `Membership.mem` and `List.instMembership`: four units/nine
rows. The remaining six RepairTheory units have twelve rows.

These counts predict a meaningful mixed matched/added path if the exact relation
holds. They do **not** prove installed private/exported record equality, complete
public body visibility, descriptor reconstruction compatibility or successful
native execution. Different bodies, reducibility data, universe order, generated
rules/group metadata or public stubs can still cause a correct refusal. Root
must reason through those actual rows before deciding that this target warrants
implementation; no exact-ID substitution, normalization or renaming is assumed.

The smallest later evidence, if separately selected, is:

- Review the three changed paths against the independent relation, including
  descriptor-to-row binding, complete-group semantics and public visibility.
- Focused inert partition/anchor checks for mixed theorem/non-theorem/addition
  accounting, unsupported/partial groups, changed rows/indices/tags and changed
  support. Reuse the existing worker/closure/transport evidence where unchanged.
- One bounded actual realization of this retained concept through the selected
  public export, requiring both native rereads and exact controller registration;
  use only fresh state/outputs selected by root. No new theorem or producer
  project is needed. A failure is a result, not permission for a fallback.
- One subsequent selected-context anchor reuse/extension boundary only if needed
  to exercise the newly persisted non-theorem tag; reuse retained exact evidence
  for the delta. Include a bounded mismatch/partial-group refusal at the changed
  native boundary, chosen from the relation review. Do not repeat the earlier
  transport, growth, certificate or basis-query campaigns.

This evidence would qualify an exact module-realization slice, not a new
proof-free query launcher, scientific growth benefit or completed v5 release.
No implementation, assembly, build, control or native operation is selected here.
