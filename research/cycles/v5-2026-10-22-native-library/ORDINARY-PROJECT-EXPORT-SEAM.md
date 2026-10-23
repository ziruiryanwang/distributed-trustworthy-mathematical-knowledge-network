# Concrete reverse seam: checked portable units to a normal Lean module

2026-10-23, `project_hook_design`. Source/theory only; guard PASS. No code,
build, import, experiment, owner opening, state change or Git operation. This
refines ORDINARY-PROVED-LIBRARY-EXPORT-DECISION without reopening its broad audit.

## Selected smallest candidate

**A local, cached, Init-only proof-bearing module builder**, not a snapshot
renamer or arbitrary project adapter. Given locally warranted target ExportIDs,
collect their complete selected portable-unit closure down to the fixed basis,
recheck that closure over the approved installed Init, and use Lean's module
writer. Keep original names; refuse collisions. Make the selected closure's
records publicly available initially; do not reconstruct lost notation or aliases.

Use inert full evidence rather than loading the receiver's complete snapshot
chain. This avoids native ancestor-module loading and re-export census. Current
`catalog.context` still checks/materializes bounded local lineage metadata and
artifact pins; selected proof closure can itself be large. Neither cost vanishes.

The existing authoring shortcut is unsuitable: `OwnerConstruction.demand`
inserts an `axiomDecl` for a theorem interface. This builder must instead decode
the original theorem value and use unchanged `CheckedExtension.checkBatch`.

## Exact reuse points and required new glue

All project source paths below are under `software/v5/ordinary_lean/`; Lean API
paths are under `software/runtime/lean-4.34.0-windows/src/lean/Lean/`.

| Step | Existing concrete mechanism | New glue / constraint |
|---|---|---|
| Select warranted inputs | `portable_catalog.py:PortableCatalog.context`; `ordinary_contribution.py:contribute_source`'s `evidence` callback pattern; `transport/ordinary_acquisition.py:OrdinaryStore.get_locator/get_evidence` | Capture the actual eligible owner context once. Fetch bounded exact units, not prepared theorem-interface groups. |
| Bind identities/closure | `portable_evidence.py:read_evidence`; `ordinary_semantics.py:export_id/basis_symbol_id`; admission `_plan`'s direct-import/collision/topological checks | Reuse these checks against an explicit foundation boundary. Calling normal preflight against the full receiver context would mark every accepted unit reused and supply no rebuilding order. |
| Construct an Init module environment | `Environment.lean:Lean.withImporting`, `importModulesCore`, `finalizeImport`, `Environment.setMainModule` | Fresh environment from installed Init, never copy or change the old snapshot header. See exact visibility choice below. |
| Check fixed boundary | `OrdinaryExport.lean:Export.compareSourceBasis`; `BootstrapSupport.lean:BootstrapProbe.inventoryRow/screen` | Direct lookup of all 581 pinned basis records. Use `Export.SourceRecords` with empty grouping, not `Export.indexSource`'s whole-environment census. |
| Rebuild exact declarations | `OriginalDecl.lean:DeclCodec.decodeUnit/expectedNames`; `CheckedExtension.lean:checkBatch` | Decoder allows only fixed-basis names and exact ordered selected-unit outputs, not every imported Init name. |
| Expose/write | `OwnerRebind.lean:exposeAdded`; `Environment.lean:mkModuleData/writeModule` | Expose actual generated recursors/prefixes; write a fresh normal module, with the writer's real file parts. |

The custody module's full path is `software/v5/transport/ordinary_acquisition.py`.
This is one small controller collector plus one native builder, reusing current
canonical codecs/checker and the existing one-operation supervision, not a new
checking language, certificate, service, scheduler or project package manager.

## Identity preservation is stronger than a successful Lean recheck

For every fetched unit U, reparse exact canonical bytes and bind S, all direct
imports and the complete unit to its UnitID. For every selected exported name n,
require the selected receiver context to warrant `ExportID(S,U,n)`; verify every
reached import against that same context. Custody possession/locator hashes alone
are not acceptance. Follow each nonbasis import to its exact unit, memoize units,
include every group member, reject cycles/conflicts and enforce aggregate caps.

In the target environment, require the pinned semantic/foundation descriptors,
same supported Lean/literal interpretation, and actual fixed-basis correspondence.
`Export.compareSourceBasis` compares the pinned foundation inventory (including
theorem values and allowed axioms/quotient primitives) against installed private
records; its existing regular-height normalization is part of that comparison,
not original-binder/implementation-byte identity. Do not replace it with names,
type equality, `quotInit`, or `OwnerRebind.matchBasisRow`'s authoring theorem view.

Permit **only** that verified fixed basis as an existing boundary in the first
endpoint. Every other reached external name must be rebuilt from its complete
exact selected unit, even if ordinary Init happens to contain that name; such a
collision refuses initially. Reject all selected output collisions, including
partial generated groups. Never broaden the boundary merely to make a proof pass.
In particular imported `sorryAx` or other unselected Init constants are not legal
decoder references; existing `CheckedExtension.requireName` also rejects sorry.

Then `checkBatch` kernel-checks each real declaration with `doCheck := true`,
compares every actual generated full inventory row, and refuses extra/missing
records. The original unit descriptor round trip, exact import IDs and actual
inventory comparison preserve the original ExportIDs; a proof valid under
differently interpreted same-named constants would not meet these premises.
No new axioms, theorem stubs, name rewriting or arbitrary equivalence claims.

## Precise module/visibility construction

Use a fresh import array containing the approved standard `Init`, exported and
non-meta. Within `Lean.withImporting`, run `importModulesCore` with
`globalLevel := .private, isExported := true`, then public `finalizeImport` with
`level := .private, isModule := true, loadExts := false, leakEnv := false` and
trust level 0. Set the fresh intended module name with `setMainModule`.
This uses the source API's separate loading-level/module parameters:
private Init records are available for boundary comparison and conversion, while
a genuine module header and public/private base maps are constructed together.
It is **not** changing `isModule` on an already-written legacy snapshot.

Because private-level import skips the new-system legacy-import prohibition,
the bridge must explicitly require every imported Init closure `ModuleData` in
the finalized header to be `isModule = true`. Import paths are fixed to the approved local runtime, with
no peer binary modules or plugins. Full imported-Std artifact authentication is
still the existing owner-trusted-installation premise, not a hermetic manifest.

`addDeclCore` adds declared records to both frontend visibility maps; generated
recursors may need the existing `exposeAdded` repair. Inspect both views for every
selected target. Initial policy retains full theorem/definition values in the
exported view as well as the private kernel data. No custom proof erasure needed.
`mkModuleData` writes stage-two additions, not imported Init's stage-one basis.
`writeModule` emits `.olean`, `.olean.server`, `.olean.private` together; its
default IR path also emits `.ir.sig`/`.ir`. Keep/pin all produced parts together.
Do not invent `ModuleData`, omit required parts, or merely rename `chunk.olean`.

The minimal builder does not compile executable IR for newly added definitions.
Proof use and kernel reduction are the target; `#eval`, `native_decide`, custom
attributes/instances, notation and source-level private aliases are not promised.
Full-closure public records are deliberate; an abstract/minimal interface is later
work only if actual users need it. A normal project with conflicting names refuses.

**Separate visibility obligation:** private-Init rechecking alone does not show
that a plain importing consumer can resolve every public record or perform the
needed conversions. The builder must check the selected public records' referenced
basis names against Init's public view, including dependencies reached through
required transparent definitions, and refuse an unavailable public boundary. The
normal consumer check below is decisive for the selected fixture; success is not
a theorem of arbitrary-library public compatibility. Do not silently switch the
consumer to `import all`, duplicate hidden Init constants, or promote hidden basis
records merely to pass. A separately documented `import all` export profile is a
possible later alternative, not the normal-import claim selected here.

## Cheapest alternative and cost boundary

If an approved ordinary Lean package already supplies the result, use its pinned
normal import. Rebuilding the same trusted package through the commons adds cost
and is not the default. The bridge matters when discovered results exist only as
commons evidence and the user wants editor/tactic/proof reuse in a normal project.

Pay once for owner-context validation + selected evidence acquisition + Init load
+ fixed-boundary comparison + selected proof checking + module writing. Cache by
selected portable identities/closure, supported runtime/writer and export policy;
unrelated context growth need not invalidate the mathematical cache. Record the
original warranted context in its local manifest, not as a global ledger.
Against repeated context reconstruction, a benefit requires
`R * (C_reconstruct - C_cached_import) > C_build`; against already available
trusted package import there is no asserted advantage. Counts/actual cost remain
needed before claiming a practical win. No whole-library proof recheck is required,
but all selected nonboundary proof dependencies are paid once by this first bridge.

## One narrow discriminator, only after separate selection

Reuse existing accepted `CommonsPeerExample.applyFour_eq` and its
`CommonsPackageExample.applyTwice` / `applyTwice_eq` dependency closure. The retained
B-contribution reports unit `d52aed3d1d0f94b8ee2236a7ee84435c983c9523dca0f100f4369c183c3d4e51`
and accepted local root `84dd6a9cf7ece45c4820ab3c28fc50ec072168c77e3cef9b890183bff5af9e13`;
these saved labels are fixtures, not fresh owner authority. Root must select actual
eligible retained custody/context, not trust the report or scratch producer olean.

Build one fresh module with public targets retaining a real definition and theorem
proof. In one ordinary new-system consumer, import it alongside standard Init,
apply the exact theorem and reduce the definition. A private reread must recover
the actual theorem value and compare all selected inventories. Recompute original
portable IDs using their bound imports. Include a changed-boundary/collision refusal
before writing; add no new mathematical benchmark or certificate campaign.
Start with existing public batch caps (32 units/4 MiB/131,072 nodes); if the selected
closure does not fit, report that discriminator limit instead of silently enlarging
it. Generated-group support remains the unchanged codec/checker obligation, not
evidence from this simple workload. No implementation or execution is selected here.

Citation correction to the earlier preparation02 note: the actual basis comparison
function in OwnerRebind is named `matchBasisRow`, not `checkBasisRow`.

## Public export workflow proposal (2026-10-23)

Source/theory only, `retained_preparation`. This specifies the smallest public
integration of the existing bridge; it does not claim the native discriminator
or a public export command has passed. Failed native01 stays failed. Root selects
the repaired native source and any subsequent package/runtime separately.

### User action and acceptance boundary

An agent has already admitted an exact result into its local owner and wants to
use it in an ordinary pinned Lean project. First prefer an approved ordinary
package if it already supplies that result. Otherwise select this one command:

```text
<python> -I -S -B <package>/owner.py export-module
  --profile-sha256 <selected-package-hash>
  --python-runtime <absolute-root> --lean-runtime <absolute-root>
  --catalog <existing-catalog> --custody <existing-custody>
  --store-id <existing-id> --custody-limits <existing-limits.json>
  --wall-seconds <original> --cpu-seconds <original> --memory-mib <original>
  --parent-root <explicit-warranted-context>
  --module-targets <exact-target-records.json> --output <fresh-export-directory>
```

This is one command shown across lines, not literal shell continuation syntax.
Use `--module-targets`: the same bounded nonempty JSON list schema as the existing
acquired-target records, `{name, export_id, unit_id}`, not a search string. Obtain them
from public contribution/receive results, not a private database edit or root
harness. IDs select mathematics; the chosen context must actually warrant them.
No latest-parent inference, implicit admission, network fetch or automatic retry.

### Exact implementation seams and minimum package delta

Use a fresh successor of `ordinary_library_support/owner.py`, not its frozen
bytes. In `arguments`/`run`, add `export-module`, require parent/output/module-targets,
and forbid acquired-targets/source/output-names/project-authoring/completion/
extraction inputs for it. Read targets once under the existing 64 KiB inert JSON bound.
Keep existing profile bootstrap, state/path separation, owner lock and `finally`
closure. Call `module_export.export_module` after opening the existing owner,
passing `loaded.profile`, fixed installed worker/native paths, and the unchanged
`Allowance.deadline`, `operation`, `account`, `check` callbacks. No new allowance.

A fresh `ordinary_library_support/profile.py` successor adds the two importable
helpers `module_closure` and `module_export` to its exact `AUTHOR` allowlist,
returns the latter in `load`'s namespace, and pins the worker/native source as
support files. Its `AuthoringProfile.file_pins` already carries the complete map.
The package, never target evidence, chooses source/worker/helpers. No user-made
profile augmentation or source path argument. Require the shared core identities.

Minimal new payloads: `authoring/py/module_closure.py`,
`authoring/py/module_export.py`, `module_worker.py`, and
`module/OrdinaryModule.lean` (the explicitly selected successor's exact bytes).
Reuse the existing checked helper artifacts and supervisor; no native rebuild
merely to package this script. Replace owner/loader, update the public README and
regenerate the exact profile/file map. Installed core S/F/I, database/custody
schemas, peer protocol and existing admission rules need no change for this seam.

### What the user receives and how an ordinary project consumes it

Keep the controller's `MODULE.json` format and five-part manifest unchanged.
The public success result additionally reports absolute `module_directory` and
`manifest_path`, the exact supported Lean executable/pin from the selected
installation, and the generated `module_name`; these are convenience metadata,
not a new warrant. Return success only after the exporter and owner closure pass.
`CHECKED_PROOF_COMPLETE_LOCAL_MODULE` means locally checked export, with
`new_catalog_acceptance=False`; it is not cryptographic certification.

For a matching normal project, add only `<export>/modules` to its local module
search path after the approved runtime's `lib/lean`. Do not expose authoring
helpers, receiver snapshots or arbitrary peer directories. Alternatively copy
all five manifest-verified same-stem parts together into a dedicated local module
directory; do not overwrite the toolchain or another module. Retain the manifest.
The project must use the same pinned Lean runtime, not merely a matching version
string. The export command cannot inspect an unspecified downstream project;
therefore it must not claim to enforce that project's toolchain compatibility.

The documented direct consumer launch is the reported Lean executable with
`-DElab.async=false -R <project-root> -o <fresh-Consumer.olean> <Consumer.lean>`,
using process-local `LEAN_PATH=<approved-runtime>/lib/lean;<export>/modules`
on Windows. Add only explicitly owner-trusted project paths when necessary.
No Lake build, global environment change or package-manager integration is needed.
The supported normal module header is:

```lean
module
public import Init
public import DMKNBridge_<returned-hex-key>
public section
-- Use the returned exact declaration names in ordinary definitions/theorems.
```

Replace the placeholder with the literal returned identifier. Existing fixture
`native_check02.consumer_source` demonstrates theorem application and `rfl`
definition reduction; it is not a public tool dependency. No `import all`, theorem
stub or private owner state is needed by that consumer. This profile does not
promise arbitrary Mathlib interoperability, notation/attributes/typeclass
registration, executable IR, `#eval` or `native_decide`. Ordinary proof checking
and kernel reduction are its actual initial scope.

### Failure handling and decision-changing evidence

Preserve structured phase/error/cost detail for unwarranted IDs, absent/damaged
custody evidence, closure/aggregate bounds, name collisions, unavailable public
semantics, native limits, changed pins and incomplete output/closure. Keep old
accepted state and diagnostics; do not infer rollback from owner-open maintenance.
No success marker on incomplete builder validation. If a valid local manifest was
written before a later owner-close failure, outer `ok=False` must preserve that
partial outcome, not claim nothing was created or automatically retry it.
Remote copies of module binaries are never new acceptance authority.

First finish/audit the selected native discriminator. Then one public-command
integration should exercise this exact installed loader/entrypoint and a normal
consumer, without initialization or a broad replay of prior controls. Record real
cost and failure behavior. The original full-proof build remains a paid one-time
step; repeated ordinary import may avoid rebuilding it. No automatic cache lookup,
new project manager or global-scale efficiency claim is implied by this proposal.

### Thin public implementation candidate (2026-10-23)

Root selected the source successor `software/v5/ordinary_module_package`.
`retained_preparation` authored only its new owner.py and README.md; root owns
loader/assembly. Owner SHA256:
`c28ba23d5fafc9dfefd39e1db1f96759dd584e9c8ca0dab010bceb9e56b316de`.
README SHA256:
`2117aa74dfcbc218930be764641969cf3d6aba02541856da9ad7a9e2b5c69e32`.
The source delta is operation/argument validation, bounded exact target parsing,
fixed-path controller delegation, public location/runtime fields and preservation
of completed export detail if later reporting fails. Existing owner closure also
retains successful result detail when close fails. No admission branch, allowance,
core/checker/evidence reader or existing-operation behavior is changed.
Read-only source diff confirms the intended delta; no Python/Lean execution,
owner opening, package build or Git index mutation was performed by this author.
Independent review and the separately selected native/public integration gates
remain necessary; writing this candidate is not evidence that either gate passes.

### Focused public controls, source candidate (2026-10-23)

`ordinary_module_package/public_controls.py` SHA256
`43cdfe88c0175d79759ecd634be651d17091880eea8690c558cd2b3b23bbf8a8`
loads the selected package once and defines seven groups: real CLI argument
parsing/exclusivity, malformed/empty/identity-bound target refusals before owner
opening, exact mocked forwarding and original-budget derivation, retained measured
versus unknown mock charges on export failure, successful-export/owner-close
failure, successful-export/reporting failure, and inert-fixture preservation.
Synthetic targets and mock owner/custody/exporter supply no mathematical warrant.
Guards reject real database, process, network, owner, custody, admission and native
export activity. All work shares one original 50 wall / 30 CPU second allowance;
mock charges are explicitly not measurements. Package/profile/runtime/output are
explicit arguments; the root-owned selector supplies any actual package and run.
No controls were executed by this author. This source is pending independent
review and separate runtime selection, not passing public-interface evidence.

## Return seam: normal module to a new checked contribution (2026-10-23)

Source/theory only, `retained_preparation`; no code/runtime/owner operation.
**The existing trusted-project backend is the right mechanism, but direct bridge
imports currently fail a deterministic module-name bound. Fix that narrow input
compatibility before selecting a run; no new export/admission protocol is needed.**

### Evidence and exact blocker

The saved native03 `normal-consumer/Consumer.lean` normally imports
`DMKNBridge_450bf7c15f3af7aa703934147ce9cd2fa1fbb5a50ec2dca7f7e41bbf1714f458`,
applies `CommonsPeerExample.applyFour_eq` and reduces `applyTwice` by `rfl`.
Its sibling `export/MODULE.json` records three full-proof units, the exact target
and parent `84dd6a9cf7ece45c4820ab3c28fc50ec072168c77e3cef9b890183bff5af9e13`.
These are saved local outputs, not a new project-return qualification.

`ordinary_project_package/ordinary_contribution.py:_project_module` permits at
most 64 characters per component. Every generated bridge module has a single
75-character component (11-character prefix plus 64 hex digits). Therefore its
current `TrustedProjectAuthoring.from_document` refuses a direct import before
owner opening, regardless of the validity of the generated mathematics.

Recommended minimum successor: allow the exact ASCII single-component pattern
`DMKNBridge_[0-9a-f]{64}` as an **import-only** alternative to existing component
bounds. Keep the ordinary <=64 rule for all other components and generated output
module names; retain the <=256 total length, <=16 components, reserved-name,
path, import-count and duplicate checks. An internal validator option passed only
from the `imports` loop can express this; no user-selectable trust mode is needed.
This recognizes a supported generated filename, not the authority of its contents.
Do not shorten its hash, rename the binary, weaken formal declaration identities,
or broaden the mathematical basis. Root owns any actual successor selection.

### Minimum explicit configuration and operation

For a fresh user-chosen declaration module, the existing configuration suffices
after that correction (angle-bracket placeholders require replacement):

```json
{
  "schema": "DMKN_ORDINARY_TRUSTED_PROJECT_AUTHORING_V1",
  "module_name": "CommonsReturn.Contribution",
  "project_cwd": "<existing-owner-approved-project-directory>",
  "project_search_paths": ["<verified-export-directory>/modules"],
  "imports": [{"module": "DMKNBridge_<exact-returned-key>", "meta": false}]
}
```

Use public `owner.py contribute` with the exact parent, acquired target records
from the local module result, new source-body/output-names files, fresh output,
and `--project-authoring` plus its SHA-256. The source body contains new declarations,
not a second `module`/import header: `assemble_source` emits that header and imports
the bridge before `#ordinary_construct_portable`. No manual inert-evidence file
or database change is needed. Configuration/paths remain owner-trusted inputs.

The worker already orders pinned helpers, pinned runtime, then approved module
directories; it writes only fresh generated output, not the original project.
Use the same selected runtime and all five local bridge parts. Configuration
hashing currently authenticates the configuration bytes, not every project module:
immutable owner-controlled support and the saved module-manifest checks remain
premises. No claim of hostile-project isolation or hermetic project authentication.

### Why identity and proof authority can be preserved

`contribute_source` verifies selected target IDs against the actual parent, reads
their exact custody evidence and prepares interpretation labels through `R.prepare`.
`OwnerConstruction.demand` leaves safe already-imported records present; it need
not insert a theorem stub for a target genuinely supplied by the full-proof bridge.
It does not prove arbitrary project/receiver equivalence by comparing names.

`PortableContributionExportCommand.run` exports only fresh current-module targets.
`SuccessorExport.selectedDeferred` stops at imported names, emitting existing exact
interpretation labels or unresolved names, never inventing accepted IDs.
`B.bind_candidate` resolves those against the protected parent; `preflight` and
`owner.admit` then independently check the complete NEW proof in that exact context.
Thus local module loading is not acceptance authority and no scratch theorem
assumption is promoted into a result. Changed meanings can fail final checking;
the admitted statement has receiver semantics, not a blanket project-equivalence
claim. Existing imported proofs remain the parent IDs, not newly re-identified units.

### One consequential next check, not a second framework

After source review of the narrow name correction, one existing-owner public
contribution should import the actual bridge and admit a fresh proof that uses its
theorem/definition. Require exact acquired-ID reuse, real new-proof acceptance,
and construction diagnostics showing no introduced signatures for supplied names.
An imported `Consumer` theorem cannot simply be selected as a new output:
`CURRENT_MODULE_TARGET_REQUIRED` is intentional. A short compiled import shim
could bypass the 64-character issue, but makes routine users build extra glue;
prefer correcting direct supported-import compatibility. No shim/build is selected.

Normal-project usefulness justifies this return path, not a claim of net growth.
Creating a full bridge solely for one `contribute` call may cost MORE than the
existing scratch-authoring path. Once normal project use already needs the bridge,
reuse its paid artifact; return still pays preparation, module loading, new-proof
export and receiver checking. This does not remove cold selected-closure cost,
guarantee full-library compatibility or prove a whole-workflow speedup.

### Independent public native-harness source review (2026-10-23)

Reviewed root-authored `ordinary_module_package/public_native_check.py`, initial
SHA256 `eb699e03de310a392f64ce6ca5d3d1189a44b430523e4681539f497cc137a73e`,
and its pinned utility `ordinary_module_bridge/native_check03.py`, SHA256
`20f6c613eb8fdd051b1f7df923e528e2c01874eb2e2c6277e3aca73d8475ccfd`.
This is a separate public-entrypoint review, not a repeat of native03 outcome,
phase-control or package-loader review.

The workflow correctly selects the existing B catalog/custody/store and explicit
accepted parent/target; the only CLI operation is `export-module`, never `init`.
The parent imports package support but opens no owner itself. The normal consumer
and its generated Lean source are reused from the exact selected utility rather
than copied. Its search path remains runtime plus generated module directory.

One original 150-wall/90-CPU allowance covers support loading, the public CLI
tree and normal consumer. The CLI's requested grant is strictly smaller than
its enclosing derived supervised grant; its native budget is derived again from
that CLI allowance. Actual whole-child-Job CPU is charged once to the original
allowance; unknown CPU reserves the full selected grant. The later consumer
receives only what remains. No retry, deadline reset or grant renewal appears.

The returned context/targets, success status, module/manifest paths and exact
runtime identity are checked. Removing only three documented convenience fields
must produce exactly the stored manifest. All manifest artifact hashes are checked
after ordinary consumption, and the package/targets and nine prior artifacts are
checked for preservation. This does not assert immutable SQLite operational bytes.

Two pre-execution corrections were requested; initial source disposition is HOLD:

- The public stdout and `MODULE.json` are ordinary diagnostic/manifest JSON with
  booleans and timing floats. `A._writer_json` deliberately rejects those tokens,
  so both current parsing calls would fail on a real successful export. Use a
  bounded normal JSON reader here; do not weaken mathematical-evidence parsing.
- Enforce the literal reviewed utility hash and bounded ordinary-file read before
  executing the utility. Initially the literal-hash check occurred after execution,
  and the size check followed an unbounded `read_bytes` call.

These findings were sent directly to root before any selected run. No runtime,
native action, owner/database opening, test execution or Git mutation was performed
by this reviewer. A corrected-source delta and selector review remain pending.

#### Corrected harness and selector source disposition

Root corrected both findings before use. Reread harness SHA256
`aa24b93100a4cdea20a9f79d06333ec6281e3d510584ee27f587c3244c07d860`
checks the literal utility hash, selected snapshot location, ordinary single-link
file/path and bounded read before executing its exact bytes. A separate operational
JSON reader now handles stdout and manifest booleans/finite floats while rejecting
duplicate keys and nonfinite constants/numbers. Mathematical parsers are unchanged.
The earlier HOLD is resolved at source level; no further blocking harness defect
was found within this selected existing-owner/public-consumer workflow.

Reviewed all three branches of root-authored `select_checks.py`, SHA256
`3988ba94e3c36adbb1de4d4ec3f8a043f3c25b9e38ecf06aceec5c8618f3ecbc`:

- `phase` snapshots the exact controls and worker, passes that worker's hash,
  pins five named Python runtime files and selects 45 wall / 25 CPU seconds,
  512 MiB / two processes. It selects no package, Lean, owner or real native work.
- `controls` pins the chosen package profile, all profile payloads and installation
  runtime/support entries, snapshots its public-control runner and supplies exact
  runtime roots. Its envelope is 60 wall / 35 CPU seconds, 512 MiB / two processes.
- `native` uses the same package/runtime binding, snapshots and pins the exact
  `20f6c613...` utility, and prospectively pins the five old report/config artifacts
  plus four old chunk files. It selects only the reviewed public-export/normal-
  consumer runner under 180 wall / 110 CPU seconds, 2048 MiB / eight processes.

Every branch includes the existing outer runner and selector in its source map,
uses fresh local output/selection names and writes only a selection. The existing
outer runner verifies selected sources/runtime before launching, executes snapshot
bytes and checks source snapshots/runtime/selection again afterwards. The pinned
builder is used only for its ordinary-file, hash and fresh-write helpers. No branch
builds, runs or opens an owner during selection. The named runtime pins remain an
explicit trusted-runtime profile, not a hermetic-runtime proof.

**Disposition: source clearance for these exact harness/selector bytes.** Actual
package adoption, phase/public-control outcomes, native execution and resulting
evidence remain separate root-owned selections. This reviewer did not execute
the selector, controls, native consumer or any project import, and did not mutate
Git or owner state. The separate reviewer retains native03/package/control audit
ownership; this review does not duplicate or replace those outcomes.

### Independent actual public-native01 outcome audit (2026-10-23)

**Disposition: PASS for the selected installed public export plus ordinary Lean
consumer workflow.** This audit reads saved files and hashes; it invokes no project
code, Lean, owner, database, test or Git mutation. It does not rerun native03 or the
separately owned mock controls.

Evidence directory:
`experiments/v5-local-checks/ordinary-module-public-native-01`.
Original and saved selection both hash to
`196c297f0aac48eeb7b6ee8af3ab71d010c394b582a15ae0ed09ff7de295493d`.
All four selected source snapshots match their exact selection hashes, including
reviewed harness `aa24b931...`, utility `20f6c613...`, selector `3988ba94...` and
the unchanged outer runner. All 145 selected package/runtime/retained-file pins
match current saved bytes. This is an explicit named-support profile, not a
hermetic-runtime or remote authenticity claim.

The executed public command is exactly `owner.py export-module`, against the
existing B catalog/custody/store and accepted parent `84dd6a9c...`. It uses package
profile `f01398e394a7bfda05f641469077cb74927aafd1cb1a3d42383d4b1d271e9435`
and installation manifest
`32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.
Its actual stdout equals the saved public result. Removing only the three documented
location/runtime convenience fields produces exactly `export/MODULE.json`. The
supported runtime paths, Lean executable size/hash and implementation identity
match the selected installation and actual command. The source uses existing-owner
opening (`create=False`) and the export operation, not initialization or admission.

The local request contains the exact three complete selected units: `applyTwice`,
`applyTwice_eq` and `CommonsPeerExample.applyFour_eq`. Request/inventory input hashes
match the controller selection. The phase trace records build, private reread and
exported reread, each started and exited zero, in that order. Pending and final
reports differ only in the intended schema/assurance transition. Their identity
fields, three names and full inventories exactly match the request; the final
record retains two checking passes and 581 fixed-basis rows. Its hash is
`035de7d52abe5a71ba41b7a48ba0b1382f0e9037dae50cdb7cb4ba26bb968b48`,
matching the manifest. All five generated module parts match exact manifest hashes
and sizes, with a total of 7,992 bytes and no extra module-directory file.

The generated module is
`DMKNBridge_450bf7c15f3af7aa703934147ce9cd2fa1fbb5a50ec2dca7f7e41bbf1714f458`.
The separate normal consumer imports only Init and that module, applies the exact
`CommonsPeerExample.applyFour_eq` theorem and proves the acquired `applyTwice`
reduction by `rfl`. Its source matches its recorded hash; all five generated
consumer artifacts match their saved sizes/hashes. The actual selected utility
supplies the sanitized runtime-plus-generated-module search path. No authoring
helper path, copied theorem proof, `import all` or private owner-state access is
part of this consumer.

All enclosing/CLI/export/consumer processes exited zero and closed cleanly, with
zero active or terminated processes and no cleanup errors. The six expected-empty
diagnostic logs are empty. The original 150-wall/90-CPU allowance was not renewed:
public command grant 121/87 encloses CLI request 118/86 and its derived native grant
88/83; the later consumer receives a remaining 109/75 grant, not a fresh allowance.
Authoritative whole-run cost is **14.8253905 wall seconds** and **14.015625 known
inclusive CPU seconds** = 13.3125 outer-Job CPU + 0.703125 wrapper CPU. Native export
10.171875, public command 11.40625 and consumer 0.65625 CPU seconds are nested
diagnostics; they must not be added again to that whole-run total.

All nine saved before/after prior-file pins are identical and still match those
files. No owner reset, state copy or new mathematical admission appears in the
selected command/source. Ordinary owner opening may maintain operational SQLite
state; this audit does not claim byte-identical database files or inspect them.

This closes the actual public-command-to-normal-Lean-use boundary for the chosen
Init-only full-proof closure on this Windows runtime. It establishes neither
arbitrary library interoperability, executable IR/notation reconstruction, a
comparative amortized-cost win, global scalability, useful mathematical growth nor
final-v5 completion. Existing native01/02 failures remain preserved; no repetition
or larger-RAM experiment is selected by this passing outcome.

### Selected source-only ordinary-project return discriminator

Root next selected one new harness under `software/v5/ordinary_project_return/`.
It reuses the already paid public-native01 module; it does not export or build that
module again. The single new mathematical target is `CommonsReturnExample.mapFour`:
for types `a : Type u`, `b : Type v`, endomorphisms `f`, `g`, and a map `h`, a
pointwise equation `h (f y) = g (h y)` entails

\[
h(\operatorname{applyTwice}(f,\operatorname{applyTwice}(f,x)))
=\operatorname{applyTwice}(g,\operatorname{applyTwice}(g,h(x))).
\]

The explicit proof uses the acquired `applyFour_eq` once at each type, four
instances of the pointwise premise, and `congrArg`, `Eq.trans`, `Eq.symm`. Source
inspection confirms all three equality combinators are in the fixed basis.
This is a generic theorem-transport interoperability workload, not new mathematics
or experimental evidence of useful/exponential growth.

The project configuration imports the exact 75-character bridge module from the
public-native01 `export/modules` directory before `#ordinary_construct_portable`.
Its new source-module identifier remains ordinary `CommonsReturnExample`. Existing
`OwnerConstruction.demand` finds the acquired theorem already present and safe,
so it introduces no names, theorem signatures or checked scratch units. It does
not thereby grant a receiver warrant: exact acquired IDs still pass candidate
binding, preflight and native admission against parent `84dd6a9c...`. The expected
actual log must confirm zero introduced names/signatures/checked units.

The only found deterministic blocker is the selected import-name validator's
64-character component limit; the separately assigned helper correction permits
only the exact top-level `DMKNBridge_` plus 64 lowercase hexadecimal digits.
No output-name, basis, identity, checking or path rule is relaxed by this harness.

Proposed interface: `--package`, `--profile-sha256`, `--utility`,
`--utility-sha256`, `--output`, reusing the exact `20f6c613...` utility snapshot.
The existing module manifest is pinned to `d447b491...`, its native report to
`035de7d5...`, and all five artifact parts to the manifest. Those seven files plus
the existing nine old artifacts are preserved before/after. One public `contribute`
command receives exact source/acquired-target/output-name/project-config inputs.
It must return one genuinely checked fresh theorem with the exact acquired theorem
ID in its proof dependencies, durable evidence/preview bytes and unchanged prior
module/state artifacts. There is no owner initialization, direct private-state
editing, networking, certificate production or module rebuild.

One original 150-wall/90-CPU allowance and derived 1536-MiB native grants are
proposed inside the unchanged 180-wall/110-CPU, 2048-MiB/eight-process outer Job.
Root owns the helper overlay, final source selection and any later execution.
Theory/source feasibility is not an executed return-path result.

### Return harness source ready for independent review

The narrowly selected harness is now written at
`software/v5/ordinary_project_return/public_native_check.py`, SHA256
`479dbf4e9f30c82d86afbf88e551a7c9a1796fff91c2c2b683dff95328c97a0b`.
It has not been executed or imported. Independent theorem/harness source review
is assigned to `retained_preparation`; root owns exact selection and execution.

The implementation uses only one public `contribute` command against existing B.
It verifies the previously paid module's exact manifest/report/five parts and
preserves those seven files plus the existing nine retained files. The selected
package/profile and installation remain separately pinned. The public response
and any accepted outcome are retained before later assertions; a failed harness
assertion must never be interpreted as rollback of an admission already made.

Postconditions bind saved request, generated source, new target, result/admission,
portable evidence and preview bytes. Both the candidate boundary and final evidence
must contain exact acquired `applyFour_eq` and `applyTwice` identities. The original
proof DAG must contain the acquired theorem at both independently quantified
universe instantiations. The actual authoring log must report no introduced names,
no scratch signatures and no checked scratch units; no three-unit preparation
closure count is imposed. The ordinary project directory must remain empty because
all generated authoring source belongs under the fresh contribution output.

Source inspection matches the installed helper's request/result schema and
`candidateBundleBytes` fields. The existing evidence schema places a singleton
theorem's original proof expression at `unit[1][4]`, with DAG nodes at `[2]`.
Operational JSON parsing intentionally permits booleans and finite floats,
whereas candidate/evidence parsing uses the existing strict mathematical parser.
This is an interoperability check only; no novelty, growth, broad-library or
final-release claim follows from either source review or a later bounded pass.

Independent review found one reporting-only defect before use: owner close failure
can change `ok` to false while preserving an accepted result under `result`.
The harness now extracts nested admission whenever that result exists, falling
back to top-level `accepted`; the entire response was already preserved. Revised
source SHA256 is
`5c9d1d3bc7cf66e3aaa5ca46845a78508127e81aa3b1a28e98de95ff59159290`.
`retained_preparation` independently cleared this revised source, including the
two independent universe instantiations and actual schema/marker bindings; its
separate disposition is in `ORDINARY-PROJECT-RETURN.md`. Root owns any execution.
