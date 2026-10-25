# Short route for the independent concept episode

2026-10-24, `theory_exchange_route`. Source inspection only; no project code
executed, owner/store opened, compilation, download or Git action. This is an
operational choice, not another growth argument or a prediction of success.

## Decision

Use ordinary approved-source A/B handoff as the baseline. The root's selected
direct Lean invocation under `tools/Run-V5-Check.py` needs no new compiler harness:
`-DElab.async=false -R <snapshot-source-root> -o <fresh-output>/TheoryA.olean
<snapshot-source-root>/TheoryA.lean`. It preserves the normal structure/notation
metadata. An ordinary approved package is sufficient for collaborative concept
development; it is not an inert-peer or hostile-source assurance boundary.

The shortest additional independent mathematical check is **produce + fresh
recipient init + intake**. Do not run original-reference registration: A has an
Init-only base and no existing P-project identity to reconcile. A generated checked
module is an additional, narrower experiment only if testing no-producer-code
recipient use is worth its actual closure and frontend costs.

## Existing command map

Use the current built package
`experiments/v5-local-checks/native-src01/distribution/package`, its actual PROFILE
SHA `fc45893cef624978f0ab5212d0e1e172ff7c71f821124daa8751727bf7123ef6`, and its exact
supported Python/Lean runtimes. The source map selects
`ordinary_native_package/owner.py`, `ordinary_producer_package/baseline_production.py`,
`ordinary_project_extraction/library_extraction.py`,
`ordinary_project_return/ordinary_contribution.py`, and
`ordinary_module_anchor/module_export.py` / `OrdinaryModule04.lean`.

Every owner command takes explicit profile/runtime/wall/CPU/memory options.
Every stateful command additionally takes catalog, custody, store ID and custody
limits. Root must select fresh outputs and any finite runtime separately.

| Step | Actual public inputs/result |
|---|---|
| A export | `owner.py produce-baseline --project-production <config> --project-production-sha256 <hash> --approve-local-project --output-names <names> --output <fresh> --spool-mib 144`. No catalog/custody/parent flags are allowed. |
| Producer config | Exact canonical JSON fields: `schema: DMKN_ORDINARY_TRUSTED_PROJECT_EXTRACTION_V1`, `project_search_paths: [<approved compiled A directory>]`, `modules: [<structured TheoryA name>]`. Config hashes bind paths/modules, not all transitive artifact bytes. |
| Names | `--output-names` is a nonempty array of structured names, not strings: a dotted name becomes one `[0,{"$bytes":[UTF-8 byte integers]}]` component per segment. Select actual public theory declarations after A exists; do not preselect a result for A. |
| Independent recipient | `init` creates a genuinely fresh recipient and returns its basis root. `intake-baseline --parent-root <that actual root> --bundle-directory <A output> --bundle-manifest <output/manifest.json> --bundle-manifest-sha256 <actual hash>` checks the selected inert closure. Producer status `PRODUCED_INERT_BASELINE_NOT_ACCEPTED` alone warrants nothing. |
| Optional no-producer-code use | `export-module --parent-root <actual accepted root> --module-targets <exact name/export_id/unit_id rows> --output <fresh>`. Omit module-anchor for first export. B imports the returned `DMKNBridge_<hex>` from the locally generated module directory using the supported runtime. |
| B checked return | `contribute --parent-root <A accepted root> --source <B source BODY> --acquired-targets <actual A target rows> --output-names <B names> --output <fresh> --project-authoring <config> --project-authoring-sha256 <hash>`. The source body excludes module/import headers; the command supplies them. |

B's project-authoring config has exactly `schema:
DMKN_ORDINARY_TRUSTED_PROJECT_AUTHORING_V1`, `module_name`, `project_cwd`,
`project_search_paths`, and `imports: [{"module": <actual checked bridge>,
"meta": false}]`. It uses the existing project author worker; no special concept
worker is needed. Alternatively, already compiled B outputs can use the same
produce/intake path; this avoids rebuilding B solely to use `contribute`.
Missing nonbasis interpretations may require the existing retained
`extract-project` + `complete` route; do not launch that automatically.

## Cheap source/data gates before funding module export

- Baseline production supports up to 8,192 units and partitions into batches.
  Module export is much narrower: 32 targets/closure units, 4 MiB, 131,072 encoded
  nodes and 4,096 names. Actual bundle inspection can reject an oversized selected
  closure without another native run. There is no promise that intake implies fit.
- New safe definitions and inductive groups are supported. Existing ambient Init
  **non-theorem** or group collisions still fail
  `INSTALLED_NON_THEOREM_OR_GROUP_COLLISION`; only exact singleton-theorem matching
  is implemented for an installed collision. Do not silently change A's theory to
  avoid a real interoperability failure and then claim general support.
- Generated kernel structures/constructors/projections do not restore structure
  elaborator metadata, instances, notation or simp registrations. Explicit
  constructor/projection constants may suffice for B, but are not a guarantee of
  pleasant theory development. If elaborate reconstruction is required, retain
  native approved-package use and report a real inert-import usability gap.
- A/B source and native-artifact approval is separate from mathematical intake.
  B importing the original approved A module does not demonstrate reliance only
  on inert checked data, even if A's separately exported bundle was also admitted.
  No source-only map establishes runtime success, creativity or acceleration.

The finite next choice is therefore: inspect/compile A, let independent B choose
an extension through the normal handoff, and add only the independent-data steps
that answer a live assurance/usable-interface question. No new API or framework
is required by the concept/theory shape itself.

## Root-selected A export inputs, not an export execution

Root reported A's successful first compile and selected exactly two inert input
files. The unchanged `TheoryA.lean` SHA is
`d2391e4a1a69d1ce57274ed011cd16734457e8239d2831a8e6eddd3349cbd9d9`.
`A-EXPORT-PROJECT.json` selects only module `TheoryA` from the existing directory
`experiments/v5-local-checks/concept-theory-a-01`; no recompilation or original
reference inputs. Its 250 bytes hash to
`cc76c41ce5d4ea7117ccbf1bfaaebe60e3be83291021ff4954e41aba78cfee4e`.

`A-EXPORT-NAMES.json` is 1,698 bytes with SHA
`80b32f91b75e16680ee1e2d23e7b853f990c48f943a44ed4aa43414cabb8adb8`.
It selects these twelve actual public `RepairTheory` declarations:
`follows_iff`, `merge_fixed_iff`, `follows_merge_iff`, `run_preserves`,
`run_settles`, `run_fixed_iff`, `run_stable`, `schedule`, `choose_follows`,
`choice_order_matters`, `copyRight_follows_joint`,
`copyRight_does_not_follow_zeroLeft`. Their required definitions/proofs are left
to the exporter's real dependency closure; no predicted closure count is asserted.
The selection covers composition, schedules and both countermodel distinctions,
without supplying A or B an additional mathematical target.

Both files were authored with apply_patch as compact canonical JSON. A permitted
formatting-only operation removed exactly their fresh terminal LF; final lengths,
terminators, parsing and decoded target spellings were checked. No existing input
or used source was changed. Root retains launch authority. No selector, harness,
runtime, owner operation or B contact occurred in this preparation.

## Independent export selection review

2026-10-24, `thin_delta_audit`. **GO for the one root-selected public production
operation**, not for intake, a generated module, novelty or growth claims.
The canonical guard passed. This is source/input inspection only: no selector
or project code execution, package import, compiler run, protected-store access,
Git mutation, B contact or reading of B's draft.

Exact declarative selection:
`experiments/v5-local-checks/concept-theory-a-export-01.selection.json`, SHA-256
`2b5887d68dc9df6e3e9d0bd4cb6d61e02405d4b9d5ab7382d7f35fff900872dd`.
It selects the existing native-src01 `owner.py produce-baseline` with the
previously reviewed PROFILE above, existing pinned runtimes, explicit local
project approval, and only the fresh `{output}/bundle` destination. No owner,
custody, catalog, parent, registration or thin-delta argument is present.

The project/names files have the exact hashes and sizes recorded above. Both
are compact JSON with no terminal newline; the project has exactly the supported
schema, one ordinary absolute artifact-search directory and structured `TheoryA`
module name. All twelve distinct target spellings decode correctly and occur in
the actual public `RepairTheory` source. `schedule` is intentionally a safe
definition, not mislabeled as a theorem; the exporter supports such targets and
must discover its actual dependency closure. The target list supplies no B task.

The four source snapshots are the existing runner, project config, names config
and A source. Their actual file hashes match selection. A's source hash also
matches the retained successful `concept-theory-a-01` compile snapshot. That
saved compile result is clean zero/closed under selection `75f5b73d...`; it is
approved-source compilation, not independent inert-bundle acceptance.

All five retained compiled artifacts independently match the selection:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `TheoryA.olean` | 95,824 | `adf357fc56674de3a766a583f401d4daa0e935a60439943f375d9ef8926e3a10` |
| `TheoryA.olean.server` | 7,840 | `eb1d5bdd8dcff55fb743412ac9296fa1c1a4a26f097d2d3c8139dbf9b085a998` |
| `TheoryA.olean.private` | 58,056 | `e3382acd89f5df5765bb5264ade3e70264b9479326e4c732886b0285a859ca77` |
| `TheoryA.ir.sig` | 176 | `e9af2a83203ae52db06f3ab7cc1372b2b5f9db05df6d1e86a7b3381b389ec695` |
| `TheoryA.ir` | 11,376 | `00fd1b4ca1597e3ce9db16e5a15305228efcfffa191a36883240d6a6bd2c6ea0` |

The runtime map has 154 pins. Comparison with the successful thin-export02
selection finds 149 identical package/runtime pins plus these five A artifacts;
only nonexecuted README/PRODUCER documentation pins are omitted from the reused
package map. No executed package/runtime pin changed. This comparison reuses the
prior package review rather than redundantly rehashing its complete tree. It is
not a hermetic pin of every installed Lean-library artifact.

The runner's direct-command binding holds: its pinned Python is argv[0], and
both configuration inputs are actual `{snapshot}` arguments backed by selected
source bytes. The A source is preserved as evidence but not compiled again by
this command. Runtime pins will be checked before and after execution by the
existing runner. The output directory was absent at inspection.

Caps are unchanged: inner 120 wall / 90 CPU seconds, 1,536 MiB memory and
144 MiB spool; outer 150 wall / 120 CPU seconds, 1,792 MiB memory, six processes,
4 MiB stdout and 1 MiB stderr. The native exporter must freshly privately import
the retained declarations and extract full selected proofs/definitions; no old
success report becomes mathematical authority. Inspect the actual closure and
cost before selecting any independent intake or optional module-export boundary.
No further test or new framework is authorized by this GO.

## Independent actual export audit

2026-10-24, `thin_delta_audit`. **PASS for saved production output and clean
closure; no independent mathematical acceptance or recipient use follows.**
This audit reads only the completed `concept-theory-a-export-01` evidence,
its 66 exported units and the relevant installed source. No project code was
executed/imported, no owner/store API was called, no state was changed, and no
B draft or private work was consulted. The prior thin-delta campaign remains
closed. No receiver operation is selected here.

The retained outer `RESULT.json` binds the reviewed selection above and reports
`COMMAND_EXITED_ZERO_AND_CLOSED`, exit zero, child reaped, Job closed, no cleanup
error, no termination request, zero final active processes and six total Job
processes. The actual public stdout has `ok: true` and
`PRODUCED_INERT_BASELINE_NOT_ACCEPTED`, with `mathematical_acceptance: false`
and `NOT_ESTABLISHED_RECEIVER_RELATIVE` acquisition fit. The inner Job also
closed cleanly; its retained phase log reaches approved project import,
selected export and `OUTPUT_WRITTEN`. `PRODUCTION.json` is explicitly the
pre-manifest observation, not a substitute for that terminal public result.

One bounded independent byte pass verified every manifest entry against the
actual unit file's length, raw SHA-256 and domain-separated unit ID:
`SHA256(ASCII("DMKN-ORDINARY-EVIDENCE-V2") || NUL || raw_bytes)`.
All 66 match. The four production-pinned files and the manifest also match
their saved sizes and hashes. No package recensus or native rerun was needed.

| Saved artifact | Bytes | SHA-256 |
|---|---:|---|
| `bundle/manifest.json` | 11,771 | `324c8a04fe7a31cd0ee3a3cba0421014f5a5136593c26bcefa65ee2e0ad36e07` |
| `bundle/inventory.json` | 823,690 | `c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0` |
| `bundle/project-selection.json` | 250 | `cc76c41ce5d4ea7117ccbf1bfaaebe60e3be83291021ff4954e41aba78cfee4e` |
| `bundle/request.json` | 1,956 | `06a853a77ba804aaccd613943c997097da5649a1f70aa4a81a83de5362d0ef59` |
| `bundle/writer.json` | 412,005 | `0833338e361445d3dc81e489eef551ae0dd02c063ad8cc2277ffc38f26eaac8e` |

The actual selected closure is one batch: **66 units / 430,438 unit bytes /
78 names**, with the public census reporting 480 edges and 10,181 nodes.
Its descriptors comprise 30 definitions, 31 theorems and five inductive groups;
the inventories contain 30 definition rows, 31 theorem rows, five inductive
rows, seven constructor rows and five recursor rows. A direct saved-directory
count agrees with the terminal spool: 77 files / 1,689,251 bytes. All twelve
selected public targets appear in the result; `schedule` remains a definition.

The five groups are `RepairTheory.Repair`, `Option`, `Prod`, `List.Mem` and
`Membership`. Ordinary nonbasis Init definitions actually present include
`Prod.fst`, `Prod.snd`, `Membership.mem`, `List.instMembership`,
`instDecidableNot`, `Option.casesOn`, `Option.ctorIdx`,
`Option.instDecidableEq`, its `match_1` and `match_3` helpers, and
`Option.noConfusionType` / `Option.noConfusion`. Consequently, a theorem-only
interpretation of this export would omit real dependencies.

Observed outer elapsed time is **6.471061300020665 seconds**. The whole child
Job charged 4.015625 CPU seconds and the separate outer wrapper charged
0.703125, for a nonduplicated observed sum of **4.71875 CPU seconds**. Peak
outer Job private commit was 502,263,808 bytes; outer stdout/stderr were
6,717/0 bytes. The inner native charge of 1.46875 CPU seconds is already
included in the whole child Job charge and must not be added again. These
costs cover production, not intake, module generation, recipient use or growth.

### A concrete cold-module obstruction, without an experiment

The complete selected closure cannot pass unchanged through installed module
export: `authoring/py/module_closure.py` fixes `max_units` and its ceiling at
32 (lines 31, 40, 229), and `module/OrdinaryModule.lean` independently fixes
`maxUnits := 32` and checks it (lines 32, 627–628). Sixty-six exceeds 32.
This is a source-established incompatibility, not an observed module-run failure.

There is also a separate obstruction below that cap. Following only the saved
66 units' actual import-name edges gives these exact nonbasis closures:

| Actual selected target | Nonbasis closure units | Direct imported group |
|---|---:|---|
| `RepairTheory.choose_follows` | 11 | `Option`, also `Option.none` and `Option.some` |
| `RepairTheory.copyRight_does_not_follow_zeroLeft` | 12 | `Prod`, also `Prod.mk` and `Prod.fst` |

The `Option` group is unit
`704e497fbea5151050ea97d921cd5884beec99b6436155331112f9e48b2a9402`
(4,214 bytes); the `Prod` group is
`8c76b854922d5082fb0c0933c6f8dd31e430fcf7d2a870580af9d25ab9ffa718`
(3,202 bytes). These are direct dependency witnesses, not guessed transitive
requirements. The original A source corroborates them: `choose` operates on
`Option Bool`, and `zeroLeft` / `copyRight` operate on `Bool × Bool`.

Cold `OrdinaryModule.lean` imports `Init` (lines 170–171, 378, 639).
The pinned runtime's `Init/Prelude.lean` declares `Prod` at line 554 and
`Option` at line 2927. Its `classifyUnits` (lines 260–289) checks already
installed names and permits reconciliation only for an exact complete singleton
theorem; present non-theorem/group declarations fail
`INSTALLED_NON_THEOREM_OR_GROUP_COLLISION`. Therefore, even assuming a future
successful intake and sufficient remaining limits, these small genuine selected
closures do not fit the unchanged cold module relation. Raising 32 alone or
splitting the full output does not remove this dependency conflict.

This conclusion does **not** say every A subset collides, that Lean rejects A's
mathematics, or that a broader exact-Init reconciliation relation is impossible.
It says the currently implemented cold inert-to-module route cannot presently
serve these ordinary A examples unchanged. Do not change A's mathematics merely
to obtain a passing fixture, claim native approved-package use is inert-data-only
use, or fund an unchanged module run whose failure is already implied by source.
Preserve the ordinary approved-source A/B baseline while root weighs whether
this real interoperability gap warrants a targeted architecture change. Export
success itself establishes neither creative-growth advantage nor release readiness.

## Architecture decision after the real concept obstruction

2026-10-24, source-only follow-up by `theory_exchange_route`. Read
`research/cycles/v5-2026-10-22-native-library/GROWTH-REUSE-FIDELITY.md` and the
actual current matcher, codec, checker and anchor paths. No runtime, state access,
product edit or new experiment. The preceding outcome audit is retained unchanged.

**Recommendation: retain ordinary approved-package handoff as the concept-development
default; the minimum worthwhile optional importer improvement is exact semantic
reconciliation of supported installed units, not generic frontend reconstruction.**
This is feasible and sound in principle under the existing checker/runtime
premises. A source-level successor can be justified by the real Option/Prod
obstruction; it must not be represented as completing the 66-unit theory route,
restoring a foreign class hierarchy, or replacing the successful native baseline.
Do not fund an unchanged module run or a broad package-compatibility campaign.

### Why exact reconciliation does not need a new proof technology

Let K warrant the selected complete unit closure, B be its fixed approved basis,
and I be the actual locally approved imported environment. For each whole unit
already present in I, require its complete observed constant records to equal
those warranted in K. For each absent unit, retain real kernel checking. References
must remain closed in B plus these exact matched units and earlier new units.
Induction along the unit DAG then transports the relevant interpretation: this
is record-preserving reuse, not a decision procedure for mathematical equivalence.
Types alone, a matching name, compiler success or a peer-provided digest do not
establish the premise. Partial group collisions must refuse.

The existing record encoding is already suitable for this restricted equality:
`OriginalDecl.inventoryRow` includes ordered universe parameters and types,
definition bodies and kernel reducibility hints, opaque/theorem bodies, inductive
parameters/indices/group/constructors, constructor field metadata, and recursor
motives/minors/computation rules. Only nonsemantic Expr.mdata is omitted.
`ReferenceBase05.matchPrivate` already compares both frontend and kernel records,
rejects unsafe/partial/axiom records, and scans semantic dependencies including
recursor rules and implicit literal roots. Reuse that argument, not its expensive
snapshot-registration workflow. Complete generated-group census must come from
actual prior admission, never solely a peer's expected-inventory list.

For the **first narrow matcher**, require full equality in both private and public
views for newly supported definitions, opaque declarations and inductive groups.
Keep the existing separately justified singleton-theorem erasure case. Do not
copy ReferenceBase05's abstract-definition allowance as an accidental weakening:
a public type-only handle cannot provide a transparent body or recursor rule.
Keep both new-declaration checking passes and both fresh artifact rereads. The
fixed allowed-axiom/quotient/builtin policy is unchanged; no extension axiom is added.

### Small source delta, but not a one-line whitelist change

The coupled changes are in the current module native relation (`classifyUnits`,
matched-public validation, report partition and anchor-plan handling),
`module_export.validate_partition`, and `anchor_store` commit/reopen validation.
All currently encode `installed-singleton-theorem`; simply deleting that guard
would leave inconsistent or insufficient downstream checks. Use a fresh explicit
support policy/realization tag for full semantic matches and preserve old support
records; do not migrate or reinterpret earlier anchors.

There is an important lifetime obligation. `checkAnchorRecords` presently checks
kind and ordered universes, while anchor records already retain an
`inventory_sha256` that the native plan parser does not compare to the current
body. Generated module parts are pinned, but the installation manifest does not
pin every transitive Init artifact. For new computational matches, either bind
the entire relevant immutable artifact closure, **or, more locally, recompute the
actual full matched inventories on every restored use and compare them with the
protected locally established commitments**, in private and public views. The
latter reuses existing stored information and avoids full-runtime hashing.
Its authority is the original actual warrant plus protected local commitment,
not the hash by itself. Preserve exact dependency closure/basis checks as well.
This costs work proportional to the selected matched semantic records, not all
worldwide mathematics, and does not require re-proving the recorded theorems.

### Decision boundary

This removes a real, common built-in interpretation obstruction without making
the optional inert lane the architecture's center again. Full A still exceeds
the unchanged 32-unit module cap; matching support alone does not resolve that.
Any later partition/anchor or budget-policy decision must use the actual useful
closure and its costs, not discard inconvenient mathematics or just raise a cap.
Public-body availability and practical use of the new `Repair` structure remain
separate questions. The immediate supported theory route is still native A/B
handoff with optional independent endpoint intake. Select this narrow importer
successor only for an actual no-producer-code reuse boundary; do not delay that
working theory route for generic metadata recovery or another registration system.
