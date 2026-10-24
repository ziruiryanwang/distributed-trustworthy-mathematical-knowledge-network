# Native-first workflow: selection and compatibility

2026-10-24. Source-only investigation by `package_continuation`; independent
fixture/collision cross-check by `demand_producer`. No native process, owner
operation, package build, database opening or Git mutation. Root owns adoption.

## Decision and one next action

**Use ordinary approved Lean projects first; keep inert interchange optional;
leave the broken original-reference branch parked.** Existing module export and
project-return operations do not need that branch. The sequence
`produce-baseline -> intake-baseline -> export-module -> ordinary project ->
contribute / extract-project / complete` is source-connected but **conditional**,
not a general library round trip. Intake supports more than the current normal-
module materializer can realize.

**Highest-payoff next action:** source-only clean-recipe integration of unchanged
producer/baseline-intake dependencies atop existing preview distribution support,
omitting parked reference commands. Today's producer assembly depends on a
retained historical reference assembly and exposes failed commands: it is not a
clean deployable distribution. No new semantics, migration, certificate or search
engine is needed to resolve that blocker. Review the finite source/dependency map
before separately selecting a build. **No code, package or runtime is commissioned
by this note.**

This follows the adopted GROWTH-NEXT-LEVERAGE decision. Useful conditional
interchange does not require unique superiority over Git or another external-
consumer study before implementation. Conversely, another passing fixture does
not establish broad usefulness or justify every mechanism. Full-cost/capacity
limitations remain explicit.

## Command and dependency map

Owner commands also require adopted package/runtimes, existing catalog/custody/
store identity and a finite allocation. Parents are explicit; no silent rebase.

| Operation | Exact inputs/output | Support and compatibility |
|---|---|---|
| `produce-baseline` | Approved project-selection JSON/hash, explicit local approval, structured targets -> exact manifest/units; `PRODUCED_INERT_BASELINE_NOT_ACCEPTED` | Existing production controller, project-selection parser, bundle parser, worker, `BaselineExporter.exe`. No owner, reference or certificate. |
| `intake-baseline` | Exact manifest hash, bundle directory, receiving parent -> checked finite prefix/final local root | Baseline intake/bundle parser, ordinary admission/custody. No original-library registration. |
| `export-module` | Warranted `{name, export_id, unit_id}` targets and parent; optional exact local anchor -> checked module parts/manifest/anchor | Existing module controller/collector/store, `OrdinaryModule04`, worker. Imports Init or registered generated chain, not arbitrary original projects. |
| Ordinary Lean import/use | Approved generated module and compatible toolchain -> ordinary source using its declarations | Normal Lean; no owner operation. Do not also import the original library's duplicate definitions. |
| `contribute --project-authoring ...` | Exact approved config/hash, new source/output names, parent, acquired-target rows or `[]` -> checked result or retained candidate needing interpretations | Existing ordinary authoring/export/admission. Project code/plugins are locally approved executable support, not sandboxed peer content. |
| `extract-project` | Same parent, retained contribution, REQUEST/candidate hashes, separate approved extraction config/hash -> pinned candidate/supplement/bindings/targets, not acceptance | Existing extraction controller and role-pinned `MissingImportExporter.exe`; no build/download/reference registration. |
| `complete` | Same parent and exact candidate/supplement/prepared-binding pins, target names -> checked extension/publication bytes | Existing completion/admission; no automatic announcement/replication. |
| Existing peer offer/discover/preview/receive | Exact contribution/custody data -> advisory discovery and separate receiver checking | Existing transport/discovery; no reference branch. |

Authoring schema `DMKN_ORDINARY_TRUSTED_PROJECT_AUTHORING_V1` has exactly `schema`,
`module_name`, `project_cwd`, `project_search_paths`, `imports`: 1-16 paths and
1-64 `{module,meta}` imports. Exact generated `DMKNBridge_<64hex>` imports work.
Production/extraction instead uses `DMKN_ORDINARY_TRUSTED_PROJECT_EXTRACTION_V1`
with exactly `schema`, `project_search_paths`, structured `modules`; at most
16 roots/modules. Config pins select these choices, not all transitive artifacts.
The approved-project extraction README documents the exact return CLI.

## Source-proven conditions, not a new runtime pass

| Boundary | Principal ceilings |
|---|---|
| Produced baseline | 8,192 units, <=64 batches, 64 MiB evidence, 20,000,000 nodes, 1,024 targets, 8 MiB/unit |
| Baseline intake | Iterates batches: <=1,024 units/64 MiB/2,097,152 nodes per admission batch, plus catalog/custody/spool/aggregate-resource checks |
| Cold module or new anchored delta | 32 targets/32 new units, 4 MiB/unit and aggregate evidence/request, 131,072 nodes, 4,096 names, 32,768 edges |
| Local anchor chain | <=32 records, 1,024 total units, 16,384 names, 256 MiB artifacts; further record/plan/store bounds |
| Project return completion | Combined candidate/supplement <=32 units/4 MiB/131,072 nodes; extraction gets remaining capacity |

Thus 1,024 is not a whole-invocation baseline-intake cap. Single peer receive has
its own missing-closure cap. Production/intake success implies neither normal-
module realization nor return eligibility.

Module export needs exact locally warranted available complete evidence. Its
fixed seed is not all Init. For names already installed, `classifyUnits` matches
only complete exact singleton theorems; installed definitions/groups refuse
`INSTALLED_NON_THEOREM_OR_GROUP_COLLISION`. Both private and exported-view checking
must pass: proof erasure can lose needed conversion (e.g. some `Acc.rec` uses).
Both fresh artifact rereads must pass. Cold requests with no new declarations
refuse; already imported results should normally be used directly.

**Existing anchor batching is conditionally sufficient:** take a dependency-
ordered partition of a finite unit DAG, with each new part within all export
bounds, earlier dependencies exactly registered as whole units in the preceding
anchor, and every step satisfying both semantic views. Induction on the exact
frontier cut shows successive exports check only new parts. No new semantics
are needed. There is no selected automatic partitioner; oversized indivisible
groups, total-chain overflow, installed conflicts or public conversion failures
are not repaired. One parent chain is not arbitrary merging of independent DAGs.

**Six-unit fixture:** independent source inspection found only custom Flag group,
Flag.casesOn, flip.match_1, flip, private hidden_low and flip_low names. Six units/
nine names/31,083 bytes/322 nodes/27 edges fit cold numerical bounds; no inherent
installed-Init non-theorem collision was found. This does not qualify an unrun
combined workflow. No repeat of the fixture is justified by this map.

**Metadata matters:** generated modules carry supported checked kernel
declarations, not original notation, tactics, simp/typeclass registrations or
source layout. The builder does not replay original frontend registrations
(`loadExts := false`). A manually usable theorem can lose its ergonomic API.
This favors direct approved-library reuse where available. Local artifact
approval remains necessary; resource limits are not hostile-artifact isolation.

## Concrete consolidation blocker and anchor stability

Packages below are under `experiments/v5-local-checks/`:

| Package | PROFILE SHA-256 | Scope |
|---|---|---|
| `ordinary-preview-assembly-01/package` | `ab04e72440bcd09381a81d4b721d1103fa2e62bc260fa6c0434e6c568419016f` | Stable pre-reference authoring/extraction/completion, module anchors, query/discovery/preview; no produce/intake-baseline commands. |
| `ordinary-producer-assembly-01/package` | `3e7caee37ebd969212246cdee6bc56f4d5458c417186537de982f4f09b2cd723` | Current producer plus intake and inherited reference branch. |

Both bind installation
`32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.
Profile-map comparison: 104 files unchanged, owner/profile replaced, 34 profiled
files added. This is identity information, not whole-path execution.

Producer `assemble.py` requires `ordinary-reference-assembly-03/package`.
Its facade/profile unconditionally require/import reference support even for
ordinary operations. But baseline production/intake require only bundle parsing,
ordinary core/custody and extraction support, not registration, snapshot recovery
or reference authoring. A clean-source successor can reuse the existing preview
recipe and those unchanged baseline components. The module checker already has
genuine separate private/exported checks; it does not share the failed reference
header guard. No repair of that branch is a prerequisite.

Lowest-change selection: retain logical `reference/baseline_bundle.py` and
`reference/baseline_intake.py` paths to preserve tested controller bytes (the
directory name grants no authority), plus preview roles and producer controller/
worker/executable. Omit the separate reference profile/helper directory and
`register-reference`, `export-reference-delta`, `contribute-reference` CLI paths.
Do not rename the binder purely cosmetically or alter the native exporter.

**Clean packaging alone does not preserve old anchors.** The narrower anchor
`support_descriptor` still pins exact owner.py/profile.py bytes. Query-only
changes can preserve support; facade/loader changes deliberately cannot. STORE
binds owner/installation rather than one support ID, but anchor load requires
record/current support equality. Compatible accepted core state can remain usable
without old anchors becoming valid under new support. Previously generated files
may remain usable in ordinary Lean under their approved original runtime; this
is not protected warm-anchor reuse.

Do not drop pins or invent migration. For the proposed clean facade, record one
explicit support-version boundary and preserve the old package/anchors. Keep
the new ordinary owner/loader stable thereafter; unrelated optional producer
changes should not force changes there. No new manifest/dispatch framework is
selected.

## Evidence and source pointers

Retained `ordinary-module-public-native-01` establishes selected normal Lean use;
`ordinary-project-extraction-public-01` establishes extraction and same-parent
completion (21.4497549 wall/10.3125 known inclusive CPU seconds); the independent
producer audit establishes inert production. These are separate operations, not
one executed pipeline or measured growth benefit.

Sources: `software/v5/ordinary_module_anchor/` controller/closure/store and
`OrdinaryModule04.lean`; current producer package owner/profile, ordinary
contribution, baseline bundle/intake; producer controller/assembler; preview
distribution recipe; approved-project extraction README. Evidence/arguments:
this cycle's `RETAINED-WORKFLOW-AUDIT.md`, `ORDINARY-PROJECT-EXPORT-SEAM.md`,
`ORDINARY-MODULE-ANCHOR-SOURCE-REVIEW.md`, `PRODUCER-PUBLIC-SELECTION-AUDIT.md`,
`GROWTH-NEXT-LEVERAGE.md`. Mutable navigation is
`software/v5/ordinary_distribution/CURRENT.md`.
