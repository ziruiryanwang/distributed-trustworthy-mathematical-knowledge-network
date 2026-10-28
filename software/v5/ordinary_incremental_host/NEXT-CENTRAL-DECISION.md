# New contribution bytes to an incremental inert host

Source-only recommendation, 2026-10-28. Owner: `operable_scale_decision`.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
This checkpoint neither selects implementation/runtime nor relies on the separate
public-host workflow's output. Existing source, evidence and packages stay frozen.

## Decision

Select one small **offline publication-to-bundle projection** if root selects the
next implementation. An independent contributor already receives the exact new
portable units from public `owner contribute` or `owner complete`. Copy those
selected public bytes into the existing `units/<UnitID>.json` layout and produce
the existing baseline manifest using the existing pure bundle APIs. Transfer that
bundle and selected target rows; the host runs unchanged `host append`, then its
usual finite `host serve` session. No native export, owner reopening, private
SQLite access, new portable format or host protocol is needed for this handoff.

This is an operability gap, not a missing mathematical production capability.
The source already supplies all necessary data and codecs; an expert caller can
compose them today. The missing piece is a bounded public file-only entrypoint
that joins the two existing layouts reliably. Prefer that tiny companion over a
new cold-export frontier, a registry/global index, or another native campaign.
If root chooses no implementation, document the same composition explicitly;
do not describe a full baseline reexport as a prerequisite for fresh output.

The highest expected marginal payoff is that every successful ordinary concept
or consequence can leave its author's owner state immediately, without paying
for a second export/check of older work. This does **not** remove upstream context
reconstruction, guarantee useful mathematics, or make unavailable dependencies
available. Those are separate costs and capabilities.

## What the selected source already returns

The source roles are those in [source-map.json](source-map.json), not a guessed
newest file under `software/`.

1. [ordinary_contribution.py](../ordinary_demand_frontier/ordinary_contribution.py)
   binds the candidate at lines 583-588, preflights/admit its raw units, and requires
   new `CHECKED` admission with the matching unit count at lines 609-610. Lines
   612-649 write public `evidence/<UnitID>.json` and `previews/<ExportID>.json` and
   return target rows plus each unit's absolute file path, exact byte count and
   SHA-256. Status is `CHECKED_CONTRIBUTION_WITH_DURABLE_PUBLICATION_BYTES`.
2. [completion_api.py](../ordinary_library_package/completion_api.py), lines
   93-168, does the same for retained candidate plus supplement after independent
   admission. Status is `CHECKED_COMPLETION_WITH_DURABLE_PUBLICATION_BYTES`.
   Completion does not repeat the original source execution. Its
   [library_completion](../ordinary_library_package/library_completion.py)
   combines supplemental units first, original consumer units last, while target
   names remain the original consumer targets. The publication projection must
   retain the supplemental units as well. The result adds exact candidate and
   supplement hashes; contribution instead has acquired targets and authoring
   supervision/request-cost metadata. Neither difference changes bundle syntax.
3. [portable_candidate.py](../ordinary_lean/portable_candidate.py), lines 201-244,
   rejects outputs whose names already exist in the selected parent, preserves
   complete declaration groups, and constructs exact import bindings for each
   new unit. Old dependencies become immutable name/ExportID references; they
   need not appear as copied earlier units in this publication result. Additional
   new helper/generated units needed by the candidate can be present, so a return
   is not necessarily one unit per requested target.
4. [owner.py](../ordinary_dedicated_host/owner.py), lines 605-667, wraps the result
   with operation/profile/state information and closure outcome. Helper
   `RESULT.json` and wrapper success are distinct. A helper's durable publication
   status must not be promoted into clean wrapper closure or peer acceptance.

Both authoring paths cap this returned evidence at 32 units and 4 MiB, with
bounded bindings/nodes. These are local caps, not a claim that arbitrary new
theories fit one operation. Definitions and their consequences use the same
portable units; this route does not require inventing wrapper theorems.

The authoring path reads `owner.catalog.context(parent_root)` before preparing
and interpreting the candidate; completion also reads that context at line 87.
The binder's point-lookups do not establish that building the lookup map was
independent of owner lineage size. Do not call the entire creative/admission loop
delta-only merely because its returned publication bytes are bounded.

## Exact existing join and the missing convenience

[baseline_bundle.py](../ordinary_binding_reuse/baseline_bundle.py) already provides
`split_units` (line 313) and `make_manifest` (line 335). They accept selected exact
portable evidence, preserve complete units, check structural/identity/batch bounds
and produce `DMKN_ORDINARY_BASELINE_BUNDLE_V1`. They do not require a dependency
closure. `validate_batch` explicitly does not check dependencies against a local
mathematical environment. `Entry.relative_path` derives `units/<UnitID>.json`.

The return helper writes those same bytes below `evidence/`, with their pins in
its public result. The missing join is consequently **layout plus manifest**, not
exporting mathematics. A pinned source-result reference and an explicit local
relocated evidence directory suffice; never follow the producer's old absolute
paths on another machine. Derive filenames from validated IDs, read only the
listed units under that chosen directory, and compare their bytes and hashes.

[custodian.append](custodian.py), lines 363-474, accepts the existing manifest,
bundle directory and 1-64 exact target rows. It calls the existing intake batch
reader, stores exact evidence, regenerates/resolves previews from it, and indexes
the requested targets. It neither needs the saved preview files nor uses a
contribution report as mathematical authority. All supplied unit bytes and their
export locators are shareable, including unindexed declarations; the existing
`share_all_bundle` and partial-publication disclosures must remain explicit.

The current kit's selected [operator preparer](../ordinary_reply_capacity/operator/prepare.py)
can extract contribution target rows to prepare owner `publish`, but it does not
consume `result.units`, copy publication evidence, or emit a baseline manifest.
Its `accepted_report`/`chosen_targets` cases do not include `complete`. Its
`intake-baseline` branch consumes an already-existing bundle. The selected adapter
in `kit/operator/prepare_selected.py` only chooses the compatible interface; it
does not add the missing projection. This is not already a shipped preparer mode.

## Alternatives and their actual costs

| Route | What it provides | Cost and reason for this decision |
|---|---|---|
| Contribution/completion public result plus existing bundle APIs | New complete units, exact pins and target identities; direct inert host input after layout projection | Reads/writes the selected new return only, plus fixed support. Best route for freshly created work. No owner or native work after production. |
| Existing owner `publish` and `serve` | Direct incremental publication by the mathematical owner | Already useful when the author also operates the service. `peer_api.publish` reconstructs selected owner context and reads selected custody evidence; `serve` retains owner/custody and service obligations. Does not hand an independent inert host a file bundle. |
| Existing `custody_return.write_bundle(..., policy="selected-units")` | Exactly selected whole units, manifest and explicit unresolved-import obligations; no ancestry traversal | Already solves sparse export **from custody** without native work. Its public `return_bundle.py` opens approved local OrdinaryStore, uses fixed inventory/support, and requires serialized owner-approved custody access. Reuse when return files are absent; do not reopen custody just to recover bytes already emitted publicly. |
| The same return helper with `closed-basis` | Full exact import closure through the fixed basis | Useful for a deliberately self-contained delivery. Pays reads, dependency traversal, copied bytes, storage and later checks of the selected closure, which can grow with history. Not required for inert hosting. |
| Existing `selected_export` / `export_selected` | Cold closure bundle from selected custody roots | Uses a bounded read-only SQLite snapshot and traverses every non-basis import. No native checker, but still closure acquisition and copying; requires access to the supported custody representation. It is not a pure projection of the public result files. |
| `owner export-module` | A checked local compiled module/registered anchor for later authoring | Cold export collects/checks complete proof closure; warm export cuts at an exact locally registered module anchor. It reads owner context and may run native work/register artifacts. Its compiled-module output is not the portable bundle accepted by host append and is not authority at an independent receiver. Preserve it for local authoring reuse. |
| `owner produce-baseline` | Native project extraction followed by a fixed-basis portable bundle | Appropriate when importing selected math from an ordinary source library without portable return bytes. Its selected closure may include earlier dependencies; production/spool/native validation costs recur. It does not necessarily export the whole project, but it is unnecessary after successful contribution/completion. |
| Public peer `inspect` | Two bounded reads returning one exact complete inert unit and locator | Valuable if evidence is available only at a peer. It traverses no dependencies and opens no owner/custody. It requires a live known provider, paid network attempts, and another projection to a local file bundle. Do not publish an author service merely to download the public bytes the author already holds. |
| No change | Experts compose existing codecs and public files | Architecturally sufficient. Saves a small implementation but leaves ordinary users to construct a manifest and remap files correctly. Prefer the small companion if this concrete handoff is the next deployment task. |
| New cold-export frontier | A new way for the native exporter to omit previously retained closure | Could matter for repeated arbitrary source-library exports without public portable returns. It addresses a different workload and expands the native interpretation/identity boundary. Do not select it to solve this already-supplied-byte handoff. |

The custody-return helper is in
[custody_return.py](../ordinary_custody_return/custody_return.py), lines 65-260;
its two policies are explicit, and `selected-units` still reports receiver imports.
The [return command](../ordinary_custody_return/return_bundle.py), lines 133-151,
refuses unrecovered sidecars and opens/closes OrdinaryStore through its API.
The [selected exporter](../ordinary_selected_export/selected_export.py) uses
`ReadCustody` and schedules each non-basis import; it has no selected-units policy.
Neither return/export helper appears as a current package role in this source map
or as a shipped file in `SELECTED-FILES.json`; their existence must not be described
as a new current-kit command. Their mechanisms and retained checkpoints are useful
reuse evidence, not authorization to edit or execute frozen predecessors.

[peer_api.inspect](../ordinary_registration_refresh/peer_api.py), line 1330 onward,
returns parsed evidence plus exact raw-byte pins, not a baseline directory. When
reconstructing bytes from that report, equality to the raw pin must be established;
arbitrary JSON reserialization must not be silently assumed byte-identical.

## Whole-pipeline cost and availability

Let `D` be returned new units, `B` their bytes, `T` indexed target count, `I` their
import edges, `H` the existing host collection, and `C` a cold dependency closure.
The recommended additional handoff work is a bounded read/parse/hash/copy of
`D,B,I`, manifest/target metadata, transfer of `B` plus metadata, and the existing
host's selected-byte validation/custody/index work. It avoids revisiting or
transferring `C` solely to publish fresh output. It does not remove:

- Production: source exploration and failed approaches, bounded source/native
  authoring, request materialization, owner-context construction, admission and
  the already-written publication files. These costs belong in the denominator.
- Local handoff: report/support authentication, at least one extra file copy and
  its readback, a retained transfer directory, and operator selection. A local
  projection can use a caller-selected file arrangement, but ordinary copies are
  the simple relocatable default; do not claim zero-copy savings.
- Hosting: fixed package verification/startup, indexed metadata/tree operations
  whose depth/capacity depend on `H`, derived previews, locators, stored evidence,
  cumulative quota consumption, service traffic and retention. No full-corpus
  proof/history walk is required by append. This is not a claim of constant cost
  per addition regardless of index size or deployment.
- Service continuity: append and serve use the same exclusive host lock. The
  operator waits for the finite service to close, appends, then starts another
  session. Stable descriptor bytes do not promise concurrent online ingestion,
  unchanged discovery snapshots, or zero downtime.
- Receiving/use: an independent receiver still acquires/checks the chosen units
  and every missing exact dependency under its policy/budget. A warm receiver
  may already warrant old imports; a cold receiver can need `C`. This projection
  saves publication duplication, not the cost of first learning mathematics.
- Curation/discovery: useful concepts must still be selected, described, found
  and extended. Neither a returned unit count nor lower transfer cost measures
  useful capability growth relative to an optimized local library.

Retaining all units of one bounded return is the simplest default: it preserves
new helper definitions and consequences together without walking old ancestry.
Selecting only target-containing units is technically possible for an inert host
but can omit other new units needed by those targets; do not make that the default
silently. This default still does not guarantee every older import is served.

If old imports already live at this host, or remain supplied elsewhere, consumers
can fetch them through existing exact locator/evidence routes. If they exist only
in the author's disappearing custody, hosting the new units does not solve that
availability problem. Select existing custody-return/closure export and funded
retention when such independent cold use is a concrete requirement. Do not make
all contributors reexport the past on every addition as a universal rule.

## Minimal next scope and stop condition

If selected, add one fresh standalone offline companion, patterned on
[view_preview.py](../ordinary_preview_view/view_preview.py), with these boundaries:

1. Explicitly select the public contribution or completion report,
   its hash, a local public evidence directory and fresh output. Parse the actual
   wrapper or helper schema explicitly. Treat report status as provenance data,
   never mathematical authority. Match the recognized helper status with the
   wrapper operation when present, but retain outer `ok`/cleanup fields only as
   provenance. An `ok: false` wrapper may still hold a complete durable result
   after cleanup failure. A helper result alone cannot claim wrapper closure;
   record that distinction without opening owner state or demanding closure
   evidence. Reconstructing missing partial-output lists is outside this route.
2. Read all listed `units` once from derived local filenames under tight return
   caps; validate size/hash/semantic/UnitID and exact selected target membership.
   Preserve complete unit groups and original raw bytes. Reject duplicate IDs,
   target mismatch, missing/changed evidence and inappropriate output overlap.
3. Reuse the existing portable-evidence and baseline-bundle codecs. Write only
   `units/`, the existing manifest, selected target/config metadata and a bounded
   preparation record with pins. Preserve emitted order. There is no need for a
   new obligations schema, generalized import resolver or native compilation.
4. Emit the unchanged public `host append` configuration with current explicit
   disclosure/limits. The operator separately supplies the host root/descriptor
   pin when invoking the existing launcher; the projector need not inspect a host.
   No reads or writes of any owner, custody or index state occur in the projection.
   Host and receiver independently recheck their respective existing boundaries.

Recommended minimal command inputs are `--package`, `--profile-sha256`, `--report`,
`--report-sha256`, `--evidence-directory`, `--output`, and two required affirmative
flags `--share-all-bundle` / `--allow-partial-publication`. A single fresh output
directory contains `units/<UnitID>.json`, `manifest.json`, `append.json` and a
bounded preparation receipt. All return targets are included in append.json;
there is no target-filter mode initially. Require the caller's two flags before
writing the corresponding true disclosure values.

The exact `append.json` fields are `schema` (value
`DMKN_INCREMENTAL_HOST_APPEND_V1`), `bundle_directory`, `manifest` with `path` and
`sha256`, `targets`, `share_all_bundle`, `allow_partial_publication`, and optionally
existing lowered `bundle_limits`. Paths in this configuration are local to the
projection machine. After moving the bundle, the host operator rebinds just its
explicit local directory/manifest paths and hashes the resulting config, or runs
the offline projection after transferring the public evidence files. The bundle
manifest itself contains no machine paths and needs no rewrite.

Use the selected profile hash as the operator's approval reference and inspect
its profile metadata, but authenticate/execute **only** the following fixed inert
source roles. Do not call `profile.load`, import owner/admission code, verify native
artifacts, or attach Lean. A report's historical profile may differ: disclose it,
then require portable semantic/evidence compatibility under these selected codecs;
do not turn historical operational profiles into portable mathematical identity.

| Module | Package role | Selected source SHA-256 |
|---|---|---|
| ordinary_evidence | installation/py/ordinary_evidence.py | `fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6` |
| ordinary_semantics | installation/py/ordinary_semantics.py | `ee601536f53640a2695e51d37d3e87e6746604ed6433cb3ace9349ae1aedf915` |
| portable_evidence | installation/py/portable_evidence.py | `f8ea819bdd9344d696cef2725888828125b2ef5d1b60d2c31a0412657a62cbd8` |
| portable_candidate | authoring/py/portable_candidate.py | `29ae111a362472b09b2b1ff16b567b352be793d76c2cd1b5421e0aee29219331` |
| baseline_bundle | reference/baseline_bundle.py | `e4b52c2f2e823cc98aa37c8cc7adb0cf79952def9c19b54d7072116a39fa19b6` |

The first four source roles come from `ordinary_lean`; the last comes from
`ordinary_binding_reuse`. `portable_candidate` is required by baseline_bundle's
existing import graph, even though the projection does not call candidate binding.
Capture and hash source before execution using the existing isolated temporary
module pattern. Report contents choose no code, limits or filesystem destinations.
Profile-hash equality plus these five pins is not authentication of the entire
package or runtime: the receipt must say so and set mathematical acceptance false.

Keep the operation at the existing return envelope: at most 32 whole units,
4 MiB total evidence and 32 targets, with bounded report/manifest/output metadata,
names/nodes/edges and a single cooperative allowance. Reuse `B.split_units`,
`B.make_manifest`, `B.read_manifest` and `B.validate_batch` at their appropriate
boundaries rather than implementing new portable formulas. Their repeated
bounded parsing is a real cost, not a reason to claim each unit is scanned once.
Copy exact raw units, read back/pin written files, and write a final preparation
receipt only after output validation. Failure may still leave partial files;
neither a manifest nor the receipt is mathematical acceptance.

The changed-boundary evidence need only show byte-exact relocation of one existing
returned definition/consequence set, manifest/target compatibility with unchanged
host input, and refusal of altered/missing units or mismatched target/report
selection. Use retained public return artifacts; do not create a new mathematical
example, replay native admission, or rerun the already-qualified host lifecycle
merely to supply projector inputs. Root decides the smallest finite validation
that remains necessary after source review; no allocation is selected here.

Stop once the independent author-to-inert-host handoff is concrete and usable.
Then reassess the remaining creative workflow/whole-cost bottleneck. Do not widen
this into a generic export framework, automatic dependency replication, owner
database adapter, host recovery protocol, native frontier or global registry.

## Failed-attempt costs remain real

Source/native authoring and completion attempts retain all observed or
conservatively reserved charges. Contribution/completion may admit successfully
and then fail while writing publication bytes or closing/logging; preserve their
accepted state and diagnostics. Do not infer rollback or rerun source blindly.
Existing retained completion is useful only when its inputs and acceptance
conditions actually apply.

Projection failures cost selected reads/parsing/hashing/writes and retain partial
fresh output; they do not justify another native authoring/export operation.
Missing public files may warrant a separately selected existing custody-return
operation rather than reconstructing mathematics. A second operation gets a new
explicit bounded output/allocation; it does not erase the first failure.

Append failures can leave permitted durable evidence/preview/index prefixes,
including commits beyond the reported prefix. They are not atomic rollback.
Keep the descriptor and failed operation reports; subsequent service reports the
actual current state under lock. A new explicitly selected append can use the
existing content-addressed/idempotent primitives, but must not assert that an
earlier whole batch completed. No intent journal or recover command is proposed.

Peer acquisition failures retain begun request/byte reservations and closure
uncertainty under the existing transport ledger. Unavailable providers and failed
searches therefore remain charged when comparing this route with local-library
work. Lower repeated export cost is the supported expected gain; a numerical
end-to-end speedup or useful-growth claim needs evidence not supplied here.
