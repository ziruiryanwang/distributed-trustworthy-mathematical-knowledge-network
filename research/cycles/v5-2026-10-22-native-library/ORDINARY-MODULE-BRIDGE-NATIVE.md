# Native ordinary-module bridge: source checkpoint

2026-10-23, `project_hook_design`. Canonical guard PASS; source-only assignment.
No import, compilation, native execution, owner opening or Git operation ran.

Source: `software/v5/ordinary_module_bridge/OrdinaryModule.lean`

SHA256: `6a5037f84bbe9a09772481f92e847f203a38a8cdc55ff5ec12ae6b8a38eec3b9`.

## Actual user capability and narrow scope

A user who discovers an accepted commons-only theorem and definition should be
able to use them in an ordinary Lean project. This worker turns a bounded selected
full-proof closure into a normal proof-bearing module importing installed Init.
Approved ordinary packages remain preferable when they already supply the result.
No certificates, source elaboration, peer binary import, package manager, name
translation or basis promotion is introduced.

The selected future discriminator remains the existing accepted
`CommonsPeerExample.applyFour_eq` / `CommonsPackageExample.applyTwice` closure.
This source does not authorize its execution or establish arbitrary-project or
generated-group compatibility. Nonbasis output collisions with any private Init
declaration refuse even if a same-named library declaration looks compatible.

## Exact internal interface

Invocation:

`build SYSROOT BASIS_INVENTORY REQUEST OUTPUT_OLEAN REPORT`

All paths are absolute and bounded, with no dot components. The controller owns
the protected input/output directories, exact file authentication and a single
nonrenewing supervised allowance. There must be no concurrent path replacement.

Request has exactly these keys:

| Key | Value |
|---|---|
| `schema` | `DMKN_ORDINARY_MODULE_REQUEST_V1` |
| `semantic_id`, `foundation_id`, `context_root` | Controller-authenticated lowercase 64-hex labels |
| `module_name` | Existing encoded Name, one component `DMKNBridge_<64hex>` |
| `targets` | 1–32 distinct selected nonbasis encoded names |
| `unit_ids` | Distinct ordered controller-authenticated 64-hex unit labels |
| `units` | Same ordered raw declaration-unit arrays used by existing `DeclCodec`; complete theorem values retained |

The separate basis file is the exact pinned full 581-row inventory, not the
owner-authoring theorem-interface projection. Bounds: request 4 MiB, basis 1 MiB,
32 units, 4,096 added names and 131,072 aggregate descriptor/inventory nodes.
The unchanged checker additionally bounds scanned terms and each kernel call.
Output basename must exactly match the one-component module name plus `.olean`.

Success report has exactly: `schema`, `assurance`, `semantic_id`, `context_root`,
`foundation_id`, `module_name`, `targets`, `unit_ids`, `names`, `inventories`,
`units_checked`, `checking_passes`, `basis_rows`, `artifact_parts`.

Its schema is `DMKN_ORDINARY_MODULE_OUTPUT_V1`; assurance is
`LOCAL_CHECKED_MODULE_CONTROLLER_BOUND_IDENTITIES`. `checking_passes` is 2;
`units_checked` is the number of distinct input units, not twice that number.
`inventories` is the ordered concatenation checked equal to actual full output
records. Each artifact row is `{"path": absolutePath, "bytes": count}`.
Report bound is 8 MiB; aggregate five-artifact bound is 64 MiB.

The worker checks identity-string shape, **not cryptographic IDs**. The controller
must authenticate exact canonical evidence and all import bindings in one actual
eligible context, preserve the complete evidence/manifest, recompute IDs with the
selected semantics, check success/returned records, and pin all emitted bytes.
Neither custody possession, echoed labels nor a report alone is acceptance.

## Two existing checking passes, not a new visibility verifier

1. Import only installed Init privately, using a fixed runtime-only search path,
   no plugins and no extension initializers. Require modern imported modules.
2. Compare the actual full private fixed basis with `Export.compareSourceBasis`,
   including its established normalization; counts alone are not authentication.
3. Decode ordered units against **only** fixed basis names and earlier selected
   outputs. Extra Init names, including `sorryAx`, cannot become legal references.
4. Run unchanged `CheckedExtension.checkBatch` with real proofs. Compare actual
   full inventories, not only types or nominal success. This is the authoritative
   mathematical/identity gate, conditional on the protected controller premises.
5. Independently import Init at `.exported`, obtaining genuine modern header and
   public/private maps through normal `importModules`. Run the same unchanged
   checker on the same units again. This is a separate compatibility gate: hidden
   private Init definitions cannot rescue it. No `import all` fallback is used.
6. Use `OwnerRebind.exposeAdded` for actual newly checked generated recursors;
   require all selected full inventories in both frontend views. Missing public
   records refuse. Set the main module with the normal API, then use `writeModule`.
7. Preserve `.olean`, `.olean.server`, `.olean.private`, `.ir.sig`, `.ir` together.
   Reread exact produced paths using `ImportArtifacts` at both private and exported
   levels. Check the module's modern header, exact Init import, complete name census
   and full actual selected inventories again. Only then write the success report.

This simplifies the earlier seam's custom `importModulesCore`/`finalizeImport`
proposal. No mixed-level constructor or manual module-bit change is now needed.
The first full-basis comparison is not replaced by the second public check.

All semantic and pre-write visibility checks occur before `writeModule`. I/O,
writer, reread or report failure may leave uncommitted artifacts; the controller
must retain/diagnose them without promoting or silently retrying them. Fresh-path
checks are not a security sandbox or atomic writer. Paths require owner protection.

## Cost, self-audit and limits

Two selected-proof checks are an explicit one-time cache-building cost. Ordinary
subsequent module imports do not rerun this worker. Selected evidence decoding,
two Init imports, basis comparison, writing and rereads also cost resources; no
constant-time or whole-cost win is claimed. No global library proof replay occurs.

Self-review traced the pinned Lean 4.34 `importModules`, `addDeclCore`,
`mkModuleData`, `writeModule` and `ImportArtifacts` source. The public writer uses
actual stage-two records, not copied claimed `ConstantInfo`; theorem bodies remain
present. Existing codec/checker rejects unsupported axioms/unsafe declarations and
checks generated inventory census. All raw request units remain bounded and exact.

This is **uncompiled source**, awaiting independent review and root's separate
integration/build selection. The writer's default IR files do not compile executable
implementations for added definitions. Intended support is theorem application and
kernel reduction, not `#eval`, `native_decide`, recovered notation, attributes,
instances, hidden aliases or arbitrary installed-package compatibility. No record
is loosened to force a pass. A real normal-project consumer is still required.

## Selected actual-discriminator harness, still source-only

Root subsequently assigned `software/v5/ordinary_module_bridge/native_check.py`.
The current exact source hash is reported with the final source-review handoff.
No test output, compilation or runtime was produced by the author. Before runtime,
independent review caught and the author corrected the original canonical-path
assumption: `BRIDGE` now resolves from this script's selected snapshot, requiring
the exact `OUTPUT/sources/software/v5/ordinary_module_bridge` layout. The actual
executed/imported bytes, not their mutable canonical counterparts, supply all pins.

The harness uses the existing support02 package/profile `e4c17343...` and its
exact bootstrap/loader, then verifies a separate selected four-source pin map
before loading the new collector/controller. A frozen `G.AuthoringProfile` is
augmented with those four pins; the package is not edited or rebuilt.

Command arguments are `--package`, `--profile-sha256`, `--bridge-pins`,
`--bridge-pins-sha256`, `--output`. The bridge-pins file is canonical JSON mapping
exactly `module_closure.py`, `module_export.py`, `module_worker.py` and
`OrdinaryModule.lean` to `{bytes, sha256}`. Root owns its creation and selection.

One original 150-wall/90-CPU-second allowance covers loader work, selected closure,
native export, the ordinary consumer and final checks. Each native grant is derived
from remaining allowance, uses 1536 MiB/four processes and the existing supervisor's
cleanup reserve. An enclosing 180-wall/110-CPU-second, 2048-MiB/eight-process Job
is required. No retry or budget renewal exists. Unknown child CPU reserves its
whole finite grant rather than becoming zero; outer aggregate cost remains the
authoritative full-tree measurement and must not be added again to child receipts.

The exact existing B catalog and custody open once with `create=False`, using
their existing adoption and limits. Target is the already accepted
`CommonsPeerExample.applyFour_eq`, unit `d52aed3d...`, export `0447787d...`, at
root `84dd6a9cf7ece45c4820ab3c28fc50ec072168c77e3cef9b890183bff5af9e13`.
No initialization, migration, state copy, new admission or publication is called.
Saved earlier reports select fixtures; the actual open context supplies warrants.

After a successful export, one separate normal `module` consumer imports only
Init and the generated module. It applies the exact acquired `applyFour_eq`
theorem and proves `applyTwice f x = f (f x)` by `rfl`. Its sanitized `LEAN_PATH`
contains only the pinned runtime and generated-module directory: no meta helpers,
scratch authoring imports or `import all`. It must finish cleanly with empty
diagnostics and actual modern consumer `.olean` parts. Added executable IR is
still not claimed. No independent mathematical discovery/growth claim follows.

Root additionally selected one genuine boundary negative in the **same** original
150/90 allowance, after the ordinary consumer: export newly accepted
`CommonsLibraryExample.add_zero` from branch
`b8363a72212a04c283cb9079fa3ea876aa172ad492e80cbc1fa9cc34da0c8928`.
Its complete closure includes nonbasis `Nat.add_zero`, already present in private
Init. Source analysis predicts exact `ORDINARY_EXTENSION OVERWRITE_OR_DUPLICATE`
from unchanged `checkBatch`, before the writer. The test requires child exit 1,
that one diagnostic line, empty stdout, complete clean tree closure and known CPU,
empty artifact directory, no native success report and no `MODULE.json`. A different
failure is not an expected negative pass. There is no forged proof, fallback,
retry, new admission or extra allowance. The failure record and charge are retained.

The native export result is recorded before consumer assertions, so later failure
does not erase partial success. Nine explicit previous branch reports/inputs and
snapshot artifacts (including the newly accepted branch's `87e6a8c3.../chunk.olean`)
are hashed before/after, and generated module hashes are checked
after the consumer. Database/lock byte identity is not asserted: ordinary owner
opening may touch operational SQLite state. The code invokes no mathematical
state-mutating method. Sources, existing state and all failed outputs remain retained.

## Native01 failure and minimal source successor (2026-10-23)

Root's first actual run failed during source elaboration, before the builder's
checking, writing, ordinary consumer or collision negative. The retained diagnostics
are `experiments/v5-local-checks/ordinary-module-native-01/export/supervision/stdout.txt`;
stderr is empty. This is a failed discriminator, not a bridge acceptance result.

The actual errors identify three source-layout/token problems: `matches` is a
reserved token; the multiline inline Import record is not parsed at its selected
indentation; and the fallback `fail` application separates its argument at an
invalid indentation. The subsequent placeholder errors follow the failed Import
record parse and are not evidence of a mathematical checker failure.

Root selected a fresh source-only successor, leaving the used source unchanged:

- Original `OrdinaryModule.lean` SHA256:
  `6a5037f84bbe9a09772481f92e847f203a38a8cdc55ff5ec12ae6b8a38eec3b9`.
- Successor `OrdinaryModule02.lean` SHA256:
  `adf0302a4c44379a96690d481b6d3792fad3daa043fd038462a99c6b48a4462f`.

The complete text delta consists only of renaming the local counter to
`matchCount` at its three occurrences, joining the existing Import record onto
one line and joining the existing fallback `fail` application onto one line.
The declarations, checking passes, reference restrictions, import fields, writer,
reread validation, limits and fail-closed policy are unchanged. A read-only
`git diff --no-index` confirms this exact delta; no Git index or history changed.

The controller and worker already receive an explicit native source path and
need no edits. Root owns the fresh harness/selector filename-only successors,
independent review, prospective source selection and any new bounded execution.
No compilation, native run, owner open, project import or retry was performed by
the source author. The corrected source remains unelaborated until that separate
selection; syntax correction alone does not establish success.

## Native02 failure and selected process-lifetime phase contract (2026-10-23)

Native02 wrote all five module parts but failed before its success report while
reading installed `Init/Data/String/Lemmas/Splits.olean.server`; that file exists.
Root reports peak job memory 1,610,625,024 bytes, essentially the 1536-MiB cap,
with clean exit 1. This does not by itself prove the underlying read-failure
cause. Source analysis identifies an avoidable lifetime accumulation: the private
and public construction imports remain in one process when both validation imports
are attempted. Lean's `Environment.freeRegions` is explicitly unsafe unless no
references into the imported regions remain. Manual freeing is not selected.

Root selected source-only `OrdinaryModule03.lean` and `module_worker03.py`:

1. **Construction process:** keep the exact private fixed-basis comparison and
   full-proof check, exact exported-Init second check, writer and part inspection.
   Write only `DMKN_ORDINARY_MODULE_PENDING_V1`, with assurance
   `LOCAL_CHECKED_MODULE_PENDING_REREADS`, to a fresh derived pending path.
   Exit before either validation import. Its success is not overall acceptance.
2. **Private reread process:** load only the generated module through the exact
   five-part artifact map, once, at the private level. Do not import Init separately.
   Perform the unchanged modern-header, import, complete-name-census and full
   inventory validation against the exact pending construction record.
3. **Exported reread process:** repeat that same validation in a fresh process at
   the exported level, still without an extra Init import or weakened visibility.
4. **Worker commit gate:** each phase runs sequentially inside the same existing
   supervised worker/Job, original total wall/CPU allowance and memory ceiling.
   Stop on the first nonzero exit; never retry or renew a grant. Record phase exits
   separately. Hash exact source/request/inventory before phases and require
   stability throughout. After construction, hash pending bytes and all five
   parts; require those exact bytes before and after each reread. The existing
   controller retains complete runtime/helper/profile pre/post verification and
   protected-file premises. Only after all three successful exits and all stable
   hashes may the worker write a fresh final report with the unchanged V1 output
   schema. The controller's independent report/artifact checks and final
   `MODULE.json`-last adoption gate remain unchanged.

Process exit supplies a clear memory ownership boundary. The cost is two extra
Lean startups within the same original total grant, not a claim of cheaper CPU
or guaranteed feasibility. Pending/report/phase paths are distinct and fresh;
failure leaves preserved uncommitted artifacts, never a promoted success. This
contract is root-approved source work only. Used01/02 and their evidence stay frozen.

### Implemented source03, not executed

`OrdinaryModule03.lean` is SHA256
`9002e54d73fc884ebce50b8c782757801a0d0abd6cc6c0fee6ed83a455f8536f`;
`module_worker03.py` is SHA256
`35b24343be54ce26ea36c0bfad4c4e81ea869e35fcd24a7892dfd3ad4f4585a6`.
The native delta retains the original construction body through writing and
inspection, replaces its two in-process rereads with the pending record, and
adds only a request-bound fresh-process reread command. Each reread reconstructs
the expected name/inventory list from the exact request, compares it with the
pending record and calls the unchanged original header/inventory validator.

The worker's existing eight arguments remain unchanged. For a final report
`native-report.json`, it uses `native-report.json.pending` and a separate
`native-report.json.phases.jsonl` trace. The trace records phase start and actual
exit without declaring mathematical acceptance. The pending bytes are retained
after finalization. The final report changes only the pending schema/assurance
back to the existing output schema/assurance; no controller schema change is
required. The worker uses no new support import, supervisor, allowance or owner.

Author self-review compared the exact native02/03 source delta and traced first
failure exits, fresh-path checks, bounded single-link file hashing, request and
pending bindings, before/after artifact stability and manifest-last behavior.
This is source inspection, not a test or elaboration result. Independent review
and root's exact integration/execution selection remain separate prerequisites.

### Focused source-only phase controls

After independent source03 clearance, root assigned `phase_controls.py`, SHA256
`bfef6412a5095aa15352b9e2c4b5830aaed0b2c793f71c178ab9ee602243613a`.
Its CLI accepts `--worker`, `--worker-sha256` and an existing selected `--output`
directory. It creates fresh retained `phase-fixtures/` plus a final `RESULTS.json`;
the source is pinned before Python import. Its one internal allowance is 35 wall
and 20 CPU seconds, with separate root-selected external supervision required.

The fourteen planned cases cover full three-phase finalization, early stop after
each of the three nonzero exits, same-size mutation of each of source/inventory/
request/pending and the five artifact parts, and refusal of an existing final
report before any phase starts. It checks exact phase command arguments, selected
environment, order, exit trace, retained pending bytes and absence of final success
after every failure. The phase simulator replaces `subprocess.call`; subprocess
creation, shell launching, sockets and SQLite are explicitly forbidden. Invented
inert reports are labelled mocked evidence, never mathematical acceptance.

This adds targeted validation of the changed commit gate only. No Lean invocation,
owner/database opening, networking, compilation, test execution or Git mutation
was performed by the author. Runtime and outcome adoption remain root-owned.
