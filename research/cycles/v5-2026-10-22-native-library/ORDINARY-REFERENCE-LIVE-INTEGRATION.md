# A2 live registration and ordinary delta: minimal integration seams

2026-10-24. Source/theory only, after the dual-view matcher review candidate
`5120d6bb7939e32b2c2cd45981dde015d9e041fd9d7a05e11cc453ce5fd3b30a`.
No implementation, native build/import, owner operation, snapshot copy or Git
mutation is selected here. The next experiment plan is separately owned in
`ORDINARY-BASELINE-NATIVE-WORKFLOW.md`; do not duplicate it.

## Immediate decision

Run one small actual artifact-boundary discriminator **before** implementing
the larger protected registration/controller successor. Its positive result
will establish conditional native correspondence, not mathematical admission
or registered authority. The source matcher still needs compilation and actual
modern-module testing; a parser-only suite cannot answer those questions.

After that discriminator, extend the existing owner-local realization workflow
with a tagged original-reference base. Do not pretend an original library is a
generated bridge with a fake declaration, and do not introduce a second generic
cache/registry protocol.

## Existing APIs and exact gaps

| Existing seam | Reusable behavior | Required successor change |
|---|---|---|
| `baseline_snapshot.prepare_snapshot(installation, ..., output_directory, spool_bytes, check_budget)` | Validates approved resolution, bounded copy/hash/readback, explicit original-module replay map | Call inside a reserved protected operation's fresh `snapshot` directory; keep those paths stable through matching and commit. Its prepared manifest remains inert. |
| `reference_request.prepare_request(owner, parent_root, bundle_directory, manifest_raw, manifest_sha256, targets=..., snapshot_id=..., support_id=..., check_budget=...)` | Validates actual context, every complete unit/output/import warrant, fixed seed and dependency order | Use unchanged inside the live controller while the same owner lock remains held. It cannot register a reference or authenticate snapshot labels itself. |
| `anchor_store.open_for_owner(owner, selected_support, check)` / `Store._owner_live` | Existing catalog lock, adoption/activation/store identity, immutable sidecar, no saved-report adoption | Fresh versioned successor with distinct `original-reference` and `generated-delta` record kinds, preserving old stores unchanged. Same owner lifetime and blocking discipline. |
| `Store.reserve` / `abandon` / `mark_blocked` | Record-before-native reservation; clean failure differs from unknown cleanup | Add an explicit reference reservation with its own bounded snapshot/request/report envelope. Do not reuse the generated 128-MiB operation envelope for a 512-MiB snapshot. |
| `Store._commit_generated` | Private live-event-only commit, copy/readback, fresh current-context validation, record-last non-overwriting commit, unknown-commit reporting | Add private `_commit_reference` for the live native match and zero new declarations. No public report-import/register API. |
| `Store.load(anchor_id, current_context, check)` / `plan` | Exact current warrants, support/artifact checks, immutable materialization plan | Add `load_reference` returning a protected `ReferenceView`; generated descendants bind exactly one reference ID plus the existing linear delta chain. |
| `module_closure.collect_closure(..., anchor_frontier, anchor_plan_sha256)` | Traversal stops at whole registered units; every frontier symbol is checked against current context; no old proofs fetched | Accept a separately bounded reference frontier plus ordinary delta frontier. Only matcher-derived public units enter it; private-only units never do. Preserve 32-unit/4-MiB new work limits. |
| `module_export.export_module(..., module_anchor="")` | Live support checks, finite supervision/accounting, exact partition/artifacts, three-phase module output and registration | Add optional `reference_base`; retain repeated all-covered zero-native reuse, returning the original reference when no new unit exists. Derive module key from reference ID as well as generated parent and targets. |
| `OrdinaryModule04.AnchorPlan.imports` / `readAnchorPlan` / `run` / `reread` | Restricted new-unit decoding, private/public delta checks, exact new inventories, fresh artifact rereads | Fresh native successor: original roots+complete explicit map below optional bridge chain; no runtime fallback in reference-backed mode; dual-view base interpretation and exact header checks. |
| `module_worker.selected_anchor` / input and artifact pins | Pins all parent artifacts across build/private/public phases | Parse the explicit reference plan and hash its complete original parts too; retain one nonrenewing allocation and clean-closure requirement. |

These existing source files are frozen predecessors, not authorized edit targets.
The successor selection should name exact fresh paths and changed files.

## Minimum authority/lifetime protocol

1. Open the real accepted owner and hold its existing catalog lock. Verify the
   selected implementation/runtime/support and context. Reserve one protected
   reference operation and its complete disk/process budget before copying.
2. Collect only the approved original module closure, then call the existing
   snapshot preparer directly into the reservation's final immutable location.
   This avoids copying hundreds of MiB again after matching and avoids moving
   absolute paths after they have been pinned. Validate the exact source report,
   prepared manifest and complete replay map. Prepared files are not authority.
3. Call `prepare_request` against the current context. Match exactly that request
   against exactly that snapshot in a supervised fresh process. No proof check,
   new accepted root, dummy theorem or certificate is needed at this stage.
4. Require clean actual completion; validate exact report fields, targets,
   private-unit census, public whole-unit rows, both projection fields and all
   counts. Match output IDs to the authenticated complete unit inventories, not
   just name strings. Verify unchanged support, inputs and snapshot bytes.
5. Revalidate current complete private output/import warrants under the still
   held owner. Record exact event/input/report pins and snapshot/support identity;
   commit the tagged reference record last using the existing unknown-commit
   discipline. A saved PASS never substitutes for the live event.
6. Every reuse revalidates that protected record, the exact snapshot and current
   context's complete requisite warrants. Different compatible contexts may use
   it only if the actual bindings agree. A stale context/root string alone does
   not suffice. Missing/changed support, artifacts or warrants refuses.

`ReferenceView` needs: local reference ID, support/snapshot IDs, original root
imports, complete exact artifact map, private warrant-binding metadata, derived
public whole-unit frontier, per-view projection classes, and retained event pins.
It does **not** need to repeat all old proof bodies in every later delta plan.
Retain complete evidence in the ordinary evidence store and the one-time match
event. Store original public metadata and the artifact map as bounded immutable
objects; small delta plans reference their exact protected IDs/pins rather than
serializing the whole native request again.

Existing generated-anchor format is incompatible as-is: it requires nonempty
`added_names`, exactly five newly generated artifacts, a single `DMKNBridge_*`
module, and direct parent `Init` or another bridge. Its caps are 32 modules,
1,024 total units, 16,384 names, 4-MiB plan, 2-MiB record and 256-MiB artifacts.
Reference profile ceilings must be separate and coherent with matcher/snapshot
ceilings; blindly widening these generated-delta caps is not integration.
Store-wide reservation/census must include failed partial operations and old
versions; no deletion or migration is implicit.

## Native delta and ordinary frontend obligations

For the first generated delta, direct imports are the registered original roots;
later deltas import the preceding generated bridge whose exact base is fixed.
The plan's artifact map is original snapshot plus generated chain, with no
conflicting module key and no fallback. New proof decoding allows only the seed,
derived public frontier and preceding new outputs. Unrelated imported names are
not warranted just because Lean can resolve them.

The new matcher review establishes why `setExporting true` alone is insufficient:
it does not change `toKernelEnv`. The successor must preserve the authenticated
interpretation of both actual checker and frontend views, including their
separately recorded full/erased theorem projections. Importing the original
roots through a generated wrapper must preserve effective original import
flags/records; prove that selected no-collision wrapper case from the importer
or re-establish exact correspondence if it changes. Kind/universe-only checks
are not independent semantic evidence. Fresh private/public rereads must cover
the actual kernel map as well as public lookup, not silently inherit the old
two-view assumption.

Ordinary authoring should consume a controller-generated Lean `ModuleSetup`
through supported `lean --setup=<file>` (`Lean/Shell.lean:171,431,540`), with
complete `importArts`, exact direct imports and explicit empty plugins/dynlibs
unless separately owner-approved. `Lean/Elab/Frontend.lean:294-306` uses that
map while loading original frontend extensions. Preserve notation/simp/instance
metadata by importing the exact original artifacts; do not reconstruct it.
The setup JSON uses Lean's actual `ToJson` format, not the matcher's custom name
codec. An uncontrolled later `LEAN_PATH` import is outside the reference warrant.
Normal approved authoring is not mathematical acceptance: extract each genuine
new result and use unchanged strict admission before returning it to the commons.

## One small discriminator; two stages, no duplicated campaign

Proposed modern library `DMKNBaselineFixture`, `public import Init`, with:

- `inductive Flag | low | high`;
- exposed transparent `flip x := Flag.rec (motive := fun _ => Flag) Flag.high Flag.low x`;
- private `hidden_low : flip Flag.low = Flag.high := rfl`;
- public `[simp]` theorem `flip_low` proved by that hidden helper;
- scoped notation `lowF` for `Flag.low`.

Select `flip` and `flip_low` for the producer. Actual exporter output, not guessed
unit counts, determines the complete generated group and private proof helper.
The first boundary harness compiles this library once, collects/exports/binds,
snapshots/replays, then performs conditional correspondence with explicitly
non-authoritative test context/support labels if no owner is opened. Check actual
reported full/erased records and whether the private helper is truly omitted
from the reusable closure. Do not count an assumed erased shape as success.

Before launch, a cheap finite artifact metadata bound is still needed: `Init`
is the known existing basis-compatible root, but its transitive modern five-part
byte total has not been established by this note. A source-confined Init-tree
metadata upper bound can resolve whether the 512-MiB snapshot ceiling suffices;
it is not a substitute for the actual collector's dependency census. No large
Mathlib closure or previous 2,852-unit admission is rerun.

Only after that first boundary succeeds, the integrated owner test actually
admits the small baseline, registers it, and checks a new independent delta:
`flip (flip lowF) = lowF` by `rfl`. A normal source consumer also proves
`flip lowF = Flag.high` with the preserved scoped notation and `simp` registration.
Extract/admit its new theorem, then reuse above the same reference without
rechecking its ancestral proofs. This is one coherent ordinary-use gate, not a
new claim of net growth or public deployment. The workflow-plan owner chooses
the exact cheap negative controls and one finite aggregate allocation.

Root subsequently supplied the finite metadata-only upper bound without a
native import: 649 Init modules, 3,245 parts, 389,437,304 bytes total and
13,007,656 bytes maximum part; no outside-Init source imports observed. This
resolves the preliminary 512-MiB envelope question for the small fixture's
existing Init dependency. The actual native collector must still establish its
real loaded closure. Do not repeat the metadata census. The fixture only needs
normal `lean -o <output.olean> <source.lean>`: the modern `writeModule` default
emits three olean parts plus `.ir.sig`/`.ir`; no C/object/link step is required.

## Source evidence

Inspected actual APIs in `anchor_store.py`, `module_closure.py`, `module_export.py`,
`module_worker.py`, `OrdinaryModule04.lean`, `reference_request.py` and
`baseline_snapshot.py`; selected runtime `Setup.lean`, `Shell.lean`,
`Elab/Frontend.lean`, `Elab/MutualDef.lean` and `Init.lean`. This note proposes
integration seams and a discriminator, not a changed package or live registration.

## Actionable successor selection proposal (2026-10-24 continuation)

Root requested the smallest source set before authorizing edits. This section
supersedes the earlier fixture's explicit-recursor suggestion: preserved workflow01
failed at code generation; fresh fixture02 uses ordinary executable matching.
Its source repair and separate runtime are not duplicated here.

The semantic auditor owns `ORDINARY-REFERENCE-DELTA-CONTRACT.md`. Coordinated
interface: exact ordered original imports with `importAll=false`,
`isExported=true`, `isMeta=false`; complete original artifact map; separately
tagged generated chain; complete public whole-unit frontier; both frontend and
kernel projection labels. First delta imports original roots, later deltas only
the preceding generated module, with those same flags. Reference-mode lookup
uses `searchPath=[]`. The auditor supplies the importer-preservation argument;
this section only maps it to concrete code.

### Make the new reference lane all-new

Do not carry `OrdinaryModule04.classifyUnits`'s installed-singleton matching branch
into the initial reference-backed lane. The protected reference frontier already
cuts known original units. Require every selected delta output to be absent in
both actual private kernel and frontend maps and require `units_matched=0`.
Reject a collision instead of reconstructing another old-proof matching rule.
Keep the existing generated-only route and its evidence unchanged.

This permits a simpler pending/output schema: exact new units and names,
reference/parent/plan bindings, two checker passes and five output artifacts.
Keep both fresh reread phases. Add actual `toKernelEnv.find?` inventory checks
for new records in build and reread, alongside existing frontend checks.
Only old reference records use the compact projection/kind/universe checks plus
the separate immutable-import preservation premises. Do not substitute those
cheap checks for full new-declaration inventory equality.

### Exact minimal changed source set

Proposed fresh directory `software/v5/ordinary_reference/`, not an edit to any
used source or installed package:

| Fresh file | Concrete predecessor/reuse | Required change |
|---|---|---|
| `ReferenceModule.lean` | `ordinary_module_anchor/OrdinaryModule04.lean`; import the already compiled `BaselineArtifactCore04` library for original five-part replay parsing | Reference-required base provider, original+generated explicit map, no fallback, all-new delta check, dual kernel/frontend new inventories, existing write/private-reread/exported-reread lifecycle. No new proof checker. |
| `reference_module_worker.py` | `ordinary_module_anchor/module_worker.py` | Bind one reference metadata/replay map and generated plan; hash exact original and generated parts across the same three phases; require new schema/reference IDs and `units_matched=0`; preserve one enclosing allowance. |
| `reference_closure.py` | `ordinary_module_anchor/module_closure.py` | Separate original-reference and generated frontiers, with independent metadata ceilings; unchanged new-work32-unit/4-MiB/131,072-node limits, same context warrants and complete-unit ordering. Carry reference ID into request/key. |
| `reference_module.py` | `ordinary_module_anchor/module_export.py` | Root-owned controller over the actual reference store: current-warrant load, zero-native all-covered path, exact support/key selection, supervision, final report validation and record-last delta commit. No new catalog acceptance for materializing already accepted units. |

The root's separately owned store/controller work must expose one concrete
`ReferenceView` and exact plan constructor to these files. It needs separate
original snapshot and generated artifact ceilings: original replay alone retains
the512-MiB profile, while existing generated chain remains separately bounded.
Do not concatenate both into `BaselineArtifactCore04.replaySelection` and silently
either exceed its cap or enlarge the original profile. Parse originals and
generated parts separately, reject duplicate module/path keys, then merge their
bounded maps for import.

Native original metadata is bounded separately from the4-MiB new-unit request.
The reference may contain many more units than the existing1,024-unit generated
frontier. Explicitly choose finite original frontier/name/byte caps coherent with
the registered public projection; a reference larger than this local supported
envelope may refuse. No claim that arbitrary admitted references fit local RAM.

The four files above are the first implementation selection to request. A fresh
package profile/owner allowlist and build adapter are unavoidable final wiring,
but should follow the agreed exact call contracts rather than preemptively copy
the entire package or mutate the current installed profile. Root owns these
integration and source-selection decisions.

### Ordinary authoring without reconstruction

The current `ordinary_contribution.assemble_source` always imports
`PortableOwnerConstructCommand` and runs `#ordinary_construct_portable`. Merely
adding a project directory does not remove that reconstruction. Its current
project worker also uses ordered `LEAN_PATH`, not an exact artifact map. Neither
is an adequate implementation of reference-backed normal authoring unchanged.

Prefer two small additional successors, selected after the reference delta
contract is settled:

- `reference_authoring.py`: prepare a normal source module and exact Lean
  `--setup` JSON from a currently protected reference/delta view; supervise
  compile once, retain and pin five parts, and hand output to extraction.
  Source imports only the original roots or selected generated module. Do not
  insert construction commands or new helper meta imports into its environment.
- `ReferenceExtract.lean`: a narrow original-artifact-map variant of
  `ordinary_project_extraction/MissingImportExporter.lean`. Reuse its existing
  bounded parent-lookup protocol and `Export.selectedFromBoundary` scheduler,
  but import the exact preserved base plus newly compiled source module with an
  explicit map and no fallback. Restrict selected targets to that source module's
  genuine output inventory. Emit the existing inert missing-import bundle;
  reuse real binding and strict `owner.preflight`/`owner.admit` afterward.

An external extractor is preferable to an in-source export command here: it
does not add `Lean`/exporter/OwnerRebind meta modules and their entire dependency
graph to the authored mathematical library, and no source construction context
is fabricated. Existing extractor targets may legitimately be imported records;
its source already checks targets against the real current parent and cuts only
at current protected symbol identities. The new source-root membership check
distinguishes genuinely authored outputs from unrelated imported declarations.
The extractor is inert, never the mathematical acceptance authority.

Lean setup encoding is now source-verified, not guessed:

- `ModuleSetup` fields serialize as `name`, `package`, `isModule`, `imports`,
  `importArts`, `dynlibs`, `plugins`, `options`; deriving removes trailing `?`
  (`Lean/Elab/Deriving/FromToJson.lean:31`).
- Names are ordinary dotted JSON strings; `NameMap` is an object with those
  string keys (`Lean/Data/Json/FromToJson/Basic.lean:173-208`), unlike our formal
  structured-name codec. Restrict module components to the existing approved
  unambiguous ASCII identifier grammar before converting.
- `imports` contains exact `module`, `importAll`, `isExported`, `isMeta` fields
  with actual JSON booleans; `importArts` values are the existing two nested
  path arrays. Use `isModule=true`, `package=null`, empty `dynlibs`/`plugins`
  and explicit options. The controller may set exact imports in setup, which
  `Lean/Elab/Frontend.lean:294-306` chooses over the parsed header.
- A closed exact map and import vector are essential. Merely setting
  `LEAN_PATH` empty does not itself disable Lean's implicit runtime fallback.
  For approved authoring, pin the complete known import graph and inspect the
  resulting module's actual imports; native receiver/extractor routes clear
  `searchPathRef` and refuse missing explicit map entries.

Approved local source elaboration may execute ordinary tactics and extensions;
it remains owner-authorized execution, not a sandbox for hostile downloaded
source. No remote artifact becomes trusted just because authoring succeeds.

### Implementation order and decisive completion condition

1. Adopt or diagnose the one actual original-library correspondence result.
2. Root implements protected reference registration; agree `ReferenceView` and
   exact plan bytes with native/worker owners, using the auditor's contract.
3. Select the four reference-delta successors above; retain generated-only old
   behavior separately. Review actual map/projection boundaries before a small
   integration run.
4. Select the ordinary setup/extractor adapters, then perform one real
   admit-reference → normal-source authoring → new-unit extraction/admission →
   reference-backed delta materialization → subsequent reuse sequence.

Do not spend a separate benchmark on any of these. The decisive product result
is a current owner using the original library's scoped notation and simp
metadata, producing and strictly accepting a real new theorem, then using the
result through a protected reference-backed module without ancestral proof
serialization. That demonstrates operable integration, not global net-growth
superiority or a completed public v5 release.

This proposal creates no software files and launches no operation. It awaits
root's exact source scope; the only edit is this existing integration checkpoint.

## Actual workflow02 boundary: abstract interfaces, not forged axioms

Workflow02 compiled the ordinary executable-match fixture, collected its actual
artifacts, exported and bound six units/nine names, and prepared the exact
650-module/3,250-part/389,559,024-byte snapshot. The matcher completed private
correspondence and then refused with
`PUBLIC_COMPUTATIONAL_OR_NONSINGLETON_ERASURE`. This is a clean failure, not a
registered reference. The negative command and inert controls were not reached.
Preserve every used source, artifact and failure. Do not repeat compilation,
collection, export or snapshot copying to investigate this boundary.

The current error does **not** identify the failing declaration or view.
`matchBasisViews` runs before `matchPublic` and checks all 581 fixed-basis names;
therefore the error cannot honestly be attributed to the fixture's `flip`,
`casesOn`, matcher, or private theorem. A future selected matcher successor must
include declaration name, original kind and actual view in its failures and
mark the transition from basis comparison to selected public closure.

### A candidate principled relaxation

Pinned `Lean/AddDecl.lean:109-126` intentionally exports safe definition and
opaque declarations as axiom-shaped public records when their bodies are not
exposed. `Lean/Environment.lean:1109` checks that the exported `ConstantVal`
(name, ordered universes, type) equals the private one. The `subsumesInfo`
singleton-theorem condition elsewhere in that file concerns duplicate-record
merging, not a general theorem that definition abstraction is unsound.

Let `G` be the independently checked full private environment. Consider a public
view `A` whose corresponding records have exactly the same signatures. Retained
definitions and all inductive/constructor/recursor/quotient rules are exact
records from `G`; selected safe singleton definition/theorem/opaque bodies may
instead be absent in `A`. An axiom-shaped record in this relation is not a newly
assumed mathematical axiom: its interpretation is the already checked constant
with the same identity in `G`.

Under the pinned kernel typing/reduction rules, the intended argument is
identity interpretation of typing derivations: a constant-use rule refers to
the same checked signature in `G`; each retained computation rule also holds in
`G`; removing a body contributes no extra delta-reduction. The narrow proposed
supported projection is thus **abstract singleton**, not full computational
equivalence. It must be justified separately for actual frontend and kernel
maps. Independently checked complete private units, safety, exact signatures,
closed actual public dependencies and original artifact identity remain required.
Do not accept arbitrary axiom-shaped records, unsafe/partial definitions,
unwarranted types, or abstract inductive/constructor/recursor/quotient records.

An important nuance: after abstraction, an old retained body might no longer
typecheck from scratch because a conversion it used is hidden. The assurance
claim is interpretation into checked `G`, not that the public subset is a fresh
standalone declaration sequence whose every old body has been rechecked. The
auditor must validate this distinction before any implementation is selected.

### Availability of computation is a separate capability

An abstract interface permits using its constant and exact type. It does not
promise that clients can unfold the body, run `rfl` through it, or execute
compiled code. A normal client may use an exported theorem describing the
function instead. If a particular delta needs hidden conversion, the public
checker pass must refuse even if its private pass succeeds. No controller may
silently promote the body, change an import to `import all`, or label this loss
of computation as full semantic equality. Source-authoring documentation and
registered projection labels must expose the distinction.

### Fixed basis is also a public-availability question

The fixed private basis contains internal proof helpers, including
`Nat.pow_pos._f` and `_private.Init.*` records. The current blanket public-basis
loop demands every one even when unused by the selected library outputs. Pinned
Lean source permits private proof helpers to be omitted entirely from the public
frontend map. This is a source-derived possible next refusal, not a named
diagnosis of workflow02.

Do not solve it by ignoring missing rows while still authorizing all 581 names
as interchangeable public interfaces. Either maintain an explicitly strict
supported profile, or define a separately closed and matched public-basis
frontier and enforce it in downstream deltas. Root and semantic auditor must
select that policy; no missing-record relaxation is implemented here.

### Reuse the retained snapshot, with no second trust registry

Root's fresh `snapshot_reopen.py` is the designated source-only reopening seam:
`read_snapshot` returns an inert validated `SnapshotView`, reusing prepared
artifact bytes rather than re-reading original source paths or copying the
library again. It does not confer mathematical acceptance or registration.
Use it in the later protected reference integration proposal after review.
Original references and generated deltas remain tagged realizations in one
versioned sidecar; this proposal does not introduce another authority store.

Implementation of reference-backed delta/store adapters remains on hold until
the actual correspondence policy is settled. This is the highest-payoff semantic
decision: a genuine ordinary library must remain usable without falsely calling
every intentionally hidden definition a new trusted axiom, and without promising
computation the ordinary public interface does not supply.

## Minimal native-delta selection after matcher05, not a redesign

The exported-view probe and source-reviewed matcher05 resolve the blocking
representation principle. Matcher05 uses V2 per-view projections and the
greatest common dependency-closed `usable_basis_names`; it still awaits its
exact live continuation and protected registration. Do not implement a delta
against a fabricated accepted reference merely because source review passes.

The next native selection remains one fresh
`software/v5/ordinary_reference/ReferenceModule.lean`, derived from existing
`ordinary_module_anchor/OrdinaryModule04.lean`, importing retained
`BaselineArtifactCore04` as well as existing `OrdinaryExport`/`OwnerRebind`.
No new checker, certificate lane, generated artifact format or separate trust
registry is needed. Root's controller/store and existing worker architecture
remain the authority and resource boundary.

### Exact predecessor seams

| Existing seam | Minimal reference-backed change |
|---|---|
| `AnchorPlan`, `readAnchorPlan`, `AnchorPlan.imports` | Required original-reference provider plus separately bounded all-added generated chain. First generated module imports exact original roots; later ones import only their preceding generated module. |
| `decodeUnits` | External names are only V2 usable basis, registered public nonbasis units and generated ancestors. Do not pass all581 private names as allowed basis. Preserve32-unit/4-MiB/131,072-node new-work limits. |
| `classifyUnits` and matched partitions | Remove matching from this new route. Reject any output already present in original/generated private kernel or frontend; all units new, `units_matched=0`, matched arrays empty. Existing Init mode unchanged. |
| `checkAnchorHeaders`, `checkAnchorRecords` | Exact original module census/order and projection/absence metadata, separate from generated headers. Inspect actual kernel and frontend independently; preserve abstract and absent states without promotion. |
| `checkInventories` | New records require exact inventory in actual kernel and applicable frontend. Compact metadata remains only an old-import integrity check. |
| `run`, `reread`, `rereadPending` | Disjoint original/generated maps, empty search fallback, unchanged two checker passes, five-part writing and fresh private/exported rereads. Bind reference identity and exact plan digest across all phases. |

Original artifacts do not go through the generated-chain ceiling. Reuse the
snapshot's original-map bound (16-MiB map,512-MiB parts) and retain separate
generated limits (32 modules,256-MiB parts,16,384 names). Reject module and
normalized path collisions before merging. Runtime dependencies are already
explicit original-map entries, not a fallback path.

Do not force the V2 reference report plus artifact map into the old4-MiB
new-work request. Root can bind separately read exact files in one protected
plan: request remains new work; reference metadata retains its established
32-MiB report ceiling; snapshot map retains16-MiB. A small plan envelope binds
their paths/digests and separate generated chain. The worker rechecks files and
parts across phases. This reuses existing finite envelopes instead of silently
enlarging generated limits or introducing unbounded original-library fields.

### Provider data required before coding its parser

Root's one versioned realization sidecar supplies:

- Registered reference identity, snapshot/support identities and exact original
  root vector/map.
- Original private/public module order from the actual correspondence event.
- All581 V2 basis projection rows and ordered usable subset, distinguishing
  unavailable helpers from allowed external declarations.
- Whole public nonbasis units with identities, names, kinds, ordered universes
  and both projection labels.
- Generated modules/bindings from this same reference, all added and collision
  free; no inherited installed-singleton matching entries.
- Original registration context separately from current owner context. Later
  owner extension reauthenticates current warrants; it must not require the owner
  to remain forever at the historical registration context root.

These are existing-contract inputs with V2 capabilities explicit. Root must fix
their field/file spelling before native parser implementation, avoiding a second
incompatible registry or serialization designed by the native author.

### One useful integration discriminator

Keep the existing ordinary source workflow: an approved reference exposes
`flip` computationally and `flip_low` abstractly as a proven theorem; normal
Lean source uses original scoped notation/attributes and derives a genuinely
new theorem. External extraction emits a candidate cut at the current reference
frontier. Real owner admission checks it; materialization checks/writes only the
new delta; a second source module uses the delta through its generated wrapper.

Changed-boundary refusals are outside-usable-basis references, original-name
collision, changed imports/artifacts, and a delta requiring computation hidden
by public abstraction. They belong in the same finite workflow, not repeated
producer/checker/network campaigns. Full-cost growth, worldwide discovery and
public deployment remain distinct unfinished release gates.

## Selected source implementation: reference-backed native delta and worker

Root selected only fresh `ordinary_reference/ReferenceModule.lean` and
`ordinary_reference/reference_module_worker.py`, following concrete API
`46a837d2...` and its independent protocol review. The source drafts now exist;
no compiler, AST check, import, test, experiment, owner, package or Git operation
has been run by this author. Source review and root selection still precede use.

The native helper imports existing `BaselineArtifactCore04` and `OwnerRebind`,
reusing the actual unchanged bounded checker. It does not import the predecessor
executable module with its conflicting root `main`. It reads the separate
1-MiB plan, 32-MiB V2 metadata, 16-MiB original replay map and 4-MiB generated
plan. Private fixed-basis metadata comes from the pinned 581-row inventory;
old declaration bodies are not decoded or rechecked. Exact artifact hashes,
current warrants and the live registration remain controller prerequisites.

Native CLI is uniform across `build`, `reread-private`, `reread-exported`:
`phase sysroot inventory request reference_plan output_olean pending_report`.
The worker keeps the predecessor's nine arguments:
`lean source helpers sysroot inventory request reference_plan output report`.
`helpers` is the existing platform-path-separated exact support directory list.
Reference imports themselves always clear native fallback and use the complete
disjoint map; the tool's own import-support path is not a mathematical fallback.

Request schema is `DMKN_ORDINARY_REFERENCE_MODULE_REQUEST_V1`, with exactly
`schema,semantic_id,context_root,foundation_id,module_name,targets,unit_ids,units,
reference_id,parent_delta_id,reference_plan_sha256`. Pending/output schemas are
`DMKN_ORDINARY_REFERENCE_MODULE_PENDING_V1` and
`DMKN_ORDINARY_REFERENCE_MODULE_OUTPUT_V1`. Their assurance strings are
`LOCAL_CHECKED_REFERENCE_MODULE_PENDING_REREADS` and
`LOCAL_CHECKED_REFERENCE_MODULE_CONTROLLER_BOUND_IDENTITIES` respectively.
Both bind all request identities, new inventories, exact direct imports and
five output parts. Reference public names are not redundantly echoed: counters
`usable_basis_rows,reference_public_units,reference_public_names,generated_names`
are integers; detailed imported metadata is bound by the exact plan digest.

The new route is all-added: decoder authorization uses only usable basis,
registered public whole units and generated ancestors. Private frontend/kernel
name collisions refuse; no installed-theorem matching shortcut exists. Both
actual checker passes and both fresh rereads compare new frontend/kernel
inventories. Original projection/absence metadata, module order and fixed import
flags are checked without promoting abstract or absent original declarations.
Generated chain limits remain independent of original snapshot limits.

The worker preserves one enclosing allocation and no retries. It pins all three
plan files plus original/generated parts across phase boundaries. Original replay
rows carry paths, not hashes: the controller's exact protected-snapshot validation
is necessary, while worker initial hashes establish only within-operation
immutability. Between adjacent phases one full input/parent check serves as both
the preceding phase's postcheck and the following phase's precheck, avoiding
consecutive duplicate scans of the same large snapshot. Final checks precede the
fresh final report; pending files remain retained on failure.

Source-only handoff identities for independent review:

- `ReferenceModule.lean`:
  `6660c657e10b7f34bcb2ecc1c32361c34075ff137197be9d87bb54780e03303e`.
- `reference_module_worker.py`:
  `fdaf97a8bfa90f257645f8a6a016cfac765de2346e4523a3c96f7eb8995884ff`.

Self-review is source reading, not independent clearance or a syntax pass.
It removed a needless basis-list search per public name; compact record checks
are linear in the selected basis/public/generated frontier sizes. No original
proof ancestry is encoded into the new request or its pending/final report.

## Minimal source-qualification builder, not a second native campaign

Root selected source-only `build_reference_module.py` and
`select_reference_module_build.py` in the same fresh directory. Read-only
inventory found no retained `OwnerRebind.o` or `.c`; the actual delta worker uses
`lean --run`, so root chose **one `.olean` compiler command**, not unnecessary
helper code generation and executable linking. There is no library compilation,
artifact collection, snapshot copying or invocation of candidate `main`.

The adapter retains six exact legacy oleans from successful baseline build04:
the five shared codec/checker/export helpers and `BaselineArtifactCore04`.
`OwnerRebind` is a modern module, so its complete five-part set is reused from
the successful current source-build package. This is seven modules / eleven
files, not seven incomplete files. Its current source is exactly `63ffaac1...`;
the package profile, source map, build result, selection and clean enclosing
result bind the retained parts. Native/compiler compatibility of that combined
support is the purpose of the single future qualification, not an assumed pass.

Proposed fresh operation is `ordinary-reference-module-build-01`: one command,
one `ReferenceModule.olean` output, five source snapshots, existing23 named
runtime pins and the two exact provenance sets. The unchanged proposed outer
allowance is120wall/60aggregateCPU/1536MiB/four processes; the adapter has one
105wall/50controllerCPU deadline and104MiB cooperative inner spool. Final input,
snapshot, support, output and metadata pins precede its compilation-only receipt.
It does not prove mathematical correspondence or authorize a later owner action.

Source-only builder SHA-256:
`535bbaa8253037e3884aaf1c8d37f8410e4aa49b75370a0690688a65959494d6`.
Source-only selector SHA-256:
`cd1e52fa4eac80d47bda4ab92165f8e74d93b67940425c8f3d57edae63a7c4de`.
The selector requires explicit reviewed `--build-sha256` and
`--reference-sha256`. No selector/import/AST check/compiler/build/runtime or Git
operation was performed. Independent review and root's exact finite launch are
still required; previous successful stages and all used files remain unchanged.

## Root controller and closure integration draft

The fresh `reference_closure.py` separates three sets: all original names that
are reserved against collision, the closed usable basis, and complete public
original/generated units that may cut dependencies. Every selected original and
generated binding must remain warranted in the current protected owner context.
Only new units are fetched, decoded and planned. A hidden original declaration
cannot be reintroduced as a newly fetched declaration with the same name.
Original library metadata has its own8192-unit/262144-name bounds; the32-unit,
4-MiB,131072-node limits apply only to new work. This is pure preparation, not
admission or independent authentication of a caller-supplied frontier.

The fresh `reference_module.py` obtains its original operation budget before
loading/preparation, authenticates the common support profile and protected
reference/optional delta chain, and reuses already covered targets without a
new native operation. Otherwise it reserves one final destination, writes the
separate plans once, collects the new closure and calls the three-phase native
worker under one Job. It binds complete new inventories, explicit imports,
reference/frontier counters and actual five-part output bytes before the store's
private record-last commit. Unknown cleanup and unknown commit retain their
distinct recovery dispositions; no automatic retry is selected.

The original snapshot is not an ordinary module-search root: its hash-addressed
parts are consumed through the exact replay map. Returned generated module
directories do not silently substitute for that original map. A protected
normal-source authoring adapter must preserve this distinction and the original
notation/attribute extensions. Source drafts alone do not establish that full
workflow. Store/controller integration review and a finite actual-owner test
remain pending; no test-only correspondence context is adopted as acceptance.

## Normal-source authoring seam (source inspection, not implementation)

The minimal usable next seam is one setup-aware ordinary compiler worker plus
one external exporter over the protected original reference and optional
generated chain. Do not reconstruct the original library in source, import
construction/export commands into mathematics, copy its snapshot, or rebuild it.

Lean 4.34's actual `Lean/Setup.lean` `ModuleSetup` is accepted by `--setup=FILE`.
Its JSON has `name,package,isModule,imports,importArts,dynlibs,plugins,options`.
Use the fresh ordinary author module name, `package:null`, `isModule:true`,
empty dynamic-library/plugin arrays, and controller-selected options. Each
import row is `{module,importAll:false,isExported:true,isMeta:false}`. The first
authoring operation imports the exact protected original roots; an operation
over a generated chain imports only its last module. `importArts` is a JSON
object keyed by ordinary dotted module name, with values
`[[olean,olean.server,olean.private],[ir.sig,ir]]` in the runtime's actual
artifact-role order (`irSig` followed by `ir`). Paths are the existing protected
paths, not new aliases. The map includes the entire original closure and every
generated ancestor, disjoint by module name and ordinary file identity.

`Lean/Elab/Frontend.lean:294-306` forwards setup imports and the artifact map,
overriding parsed header imports. `Lean/Elab/Import.lean:140-162` loads a modern
module's exported view with `loadExts := true`. This is the needed preservation
of original notation, simp attributes, instances and other extension metadata.
An empty `LEAN_PATH` alone does not disable Lean's implicit runtime fallback;
the complete protected map plus a later exact imported-module/header check is
necessary. Ordinary source and imported elaborator metadata are owner-approved
executable inputs, not hostile-source-sandboxed data.

The new compiler worker can mirror `ordinary_project_package/author_worker.py`
but take the exact setup path, compile once with `-DElab.async=false`, and emit
only the fresh five-part author module. The controller writes a generated
header (`module`, `prelude`, exact public imports, `public section`) and the
owner's bounded source body. Do not call the existing `assemble_source`:
`ordinary_project_return/ordinary_contribution.py` injects reconstruction and
export commands which this reference lane intentionally does not need.

Proposed external-export request schema is
`DMKN_ORDINARY_REFERENCE_SOURCE_REQUEST_V1`, with exact fields
`schema,semantic_id,foundation_id,context_root,reference_id,parent_delta_id,
reference_plan_sha256,module_name,targets,artifact_parts`.
`module_name` and `targets` use existing structured names; artifact parts are
the exact five fresh `{path,bytes,sha256}` pins. The actual author request can
be passed to `ReferenceModule.readPlan`: it already reads the shared identity
fields without pretending this is a materialization request. The extractor
can reuse its reviewed original/generated map parsing, `checkBaseHeaders` and
`checkBaseRecords`. Import the newly authored module once in a fresh private
environment with `searchPathRef=[]`, explicit combined artifacts, no plugins
and `loadExts=false`. Its exact direct-import flags must equal `plan.imports`;
all imported module names/order must equal the protected chain plus this module.
Every selected target must belong to this module's own `constNames`, be a full
safe declaration, and be absent from the current protected owner context.

Use the existing `Export.selectedFromBoundary` and
`ordinary_library_support/supervised_library_exchange.py:exchange`, including
its bounded parent-lookup/DONE protocol, original allowance and cleanup/CPU
accounting. The controller may answer FOUND only from the intersection of actual
current warrants and the closed usable basis, registered public whole-unit
frontier, and protected generated frontier. Every non-boundary declaration
extracted must belong to the newly authored module. An imported name outside
that frontier refuses explicitly; it must not trigger hidden original proof
re-export, arbitrary owner-name substitution, or silent private-library growth.
Complete new declaration groups remain indivisible.

Emit the existing `DMKN_ORDINARY_CANDIDATE_BUNDLE_V2` directly, with empty
`unresolved_imports`, instead of inventing a retained incomplete candidate or
using `library_completion.complete_candidate` outside its genuine missing-set
precondition. Bind the returned boundary against the reached IPC answers and
current warrants; supply exactly those authenticated boundary IDs as the
existing `portable_candidate.bind_candidate` preparation map. Its existing
strict graph/collision/canonical-evidence checks produce only a READY plan.
Reuse `publication_targets`, `owner.preflight`, `owner.admit`, and ordinary
publication-byte custody. Neither compiler success, extractor success nor a
saved setup/report confers a warrant. Root owns the public facade/profile and
the original enclosing operation budget across compile/extract/admit.

Important metadata boundary: original-library extensions survive ordinary
imports. A generated mathematical delta reconstructed only from proof units
does **not** thereby preserve newly authored notation, simp attributes, custom
tactics or arbitrary persistent extensions. For the immediate seam, preserve
the author's original module as an owner-local authoring artifact and describe
generated deltas as mathematical declarations only. Transferring executable
extension metadata would require a separately explicit trust/retention policy;
do not advertise arbitrary authoring-metadata preservation from portable proof
units. The source mechanism must not silently turn this open policy into a
peer-binary trust lane.

Cost consequence: one new-source compile, one selected new-closure export and
the existing actual new-unit admission. No original snapshot copy or rebuild,
no ancestral proof serialization, no certificate production, and no full
portable-owner reconstruction. Ordinary original artifact loading and local
immutability validation still have real cost; this is not a constant-time or
whole-v5 qualification. No author adapter or exporter was implemented, compiled
or executed by this inspection. Root selection is required before source work.

## Root-selected normal-source implementation draft

Root subsequently selected the source-only worker/exporter plus the smallest
no-main shared parser derivative. The new files are:

- `reference_author_worker.py`: six positional paths,
  `lean source_root source_file setup_json output_olean report_json`.
  One ordinary compile, exact setup with `Elab.async:false`, fresh top-level
  `DMKNAuthor_<64hex>` source/module/output, bounded source/setup reads and
  pre/post byte pins, five output parts with64MiB aggregate maximum. Original
  library authentication remains the protected controller's responsibility;
  this worker does not add a redundant full-library hashing pass.
- `ReferenceEnvironment.lean`: mechanical reviewed `ReferenceModule` prefix
  through `checkBaseHeaders`, namespace renamed, no checker invocation, output
  or global `main`. The frozen predecessor stays unchanged. Lean's supported
  `--run` invokes global `main`, so importing the old module and redefining main
  was rejected; no `#eval` execution workaround is used.
- `ReferenceSource.lean`: five positional arguments after `--run SOURCE`,
  `sysroot inventory request reference_plan output_candidate`. It emits the
  existing Candidate V2 and uses the unchanged missing-import exchange DONE
  frame; DONE's output bytes describe this candidate, not a supplement. No
  imported declaration outside the approved frontier may be extracted as new.

Worker report schema is `DMKN_ORDINARY_REFERENCE_AUTHOR_OUTPUT_V1`, assurance
`OWNER_APPROVED_SOURCE_OUTPUT_NOT_MATHEMATICAL_ACCEPTANCE`, with exactly
`schema,assurance,module_name,source_root,source,setup,artifact_parts`.
Module name is a dotted string; source/setup and each of five artifact parts are
`{path,bytes,sha256}` pins. Controller can bind the complete report without
treating compiler success as acceptance. Native generated-artifact alias checks
use the existing `reportPath` normalization before ordinary path-key comparison.

Current source-only pins, before independent review or execution:

- Worker: `8633631b597c66bcfcc380279ee95876a47b2b4b2903a5c87ae31116c7af2402`.
- Shared environment: `a5aee6d1ca7e1b8ce295fd725da0a2dd90f1dddc69e081e860325d7f170b6587`.
- External exporter: `810d6245d6989b6dec6ce28962cd118f24252b2fe42e214ae58fcd3c34962751`.

Root also selected source preparation of `build_reference_source.py` and
`select_reference_source_build.py`. Proposed operation is
`ordinary-reference-source-build-01`: exactly two compile commands, Environment
then Source, writing the two `.olean` files under `build/objects`. Reuse the
qualified module-build01's exact eleven support files **in place**, without
another support copy or helper rebuild. Search path is fresh objects followed
by that exact support directory. The new shared Environment `.olean` is intended
for the package; the Source `.olean` is compilation evidence, not a native run.

Predecessor receipt pins are BUILD `dd51cef6...`, result `d7075a3b...`, selection
`18dc8fb7...`. Eight source snapshots and23 named runtime pins are selected.
Proposed outer allowance is150wall/90aggregateCPU/1536MiB/four processes;
inner135wall/75controllerCPU and64MiB cooperative fresh spool. The source-build
receipt schema is `DMKN_ORDINARY_REFERENCE_SOURCE_BUILD_V1`, status
`COMPILED_CANDIDATES_NOT_INSTALLED_OR_EXECUTED`, with exact two generated output
pins, eleven retained helper pins, inputs, sources, metadata and both commands.
Selector requires reviewed build/environment/source/worker hashes explicitly.

Builder SHA-256: `7287ddd595c8ef54fad3e659923b26934283b80be6f00ad4a4b585c4927e0951`.
Selector SHA-256: `672e93f19ae0369c04b058f3f9e07d9167abba8753a5e196c4907df3159c8cbd`.
No selector, parser/AST check, import, compiler, author, extractor, owner mutation,
experiment or Git action has been executed by this agent. Root owns review
adoption, exact runtime selection, controller/facade and release integration.

Independent `reference_soundness_audit` subsequently source-cleared those exact
five final pins for root's bounded two-command compilation selection. It confirmed
the shared prefix equivalence and latest artifact-path normalization. This is
source clearance only, not compilation, runtime extraction or owner acceptance.

## Preserved source-build01 failure and minimal one-command correction

Root's actual source-build01 failed at the new Source's nested limits-record
layout (`line23:38`, expected closing brace). Environment compiled successfully
in8.3846 seconds; Source returned1 after1.3912 seconds. The outer event closed
cleanly in12.3216wall/9.9375knownCPU. This is not a successful whole build; no
native main or owner operation ran. Both frozen sources and all failure evidence
remain unchanged. The existing2,378,696-byte `ReferenceEnvironment.olean`,
SHA-256 `a082feb7bfcf3b28199c4438baafc11e3e00b4ad37af07e3507473e1e452c698`,
is explicitly selected as a retained partial output, not silently rebuilt.

Root selected source-only `ReferenceSource02.lean`. Its sole source difference
is multiline record layout; all limits and mathematical/extraction semantics
stay identical. SHA-256:
`79a13b525b20f96b82b1ecaf4da5561248998968b073d82db8b855ca88133ef2`.

The narrow `build_reference_source_continuation.py` reuses the pinned original
builder's input inspection, validates the exact failed01/clean-closure result,
the two actual commands (Environment0, Source1), retained selected/staged source
bytes, and explicitly pinned Environment output. It compiles only Source02 with
the existing Environment directory and eleven helper parts on its search path.
No support copy, helper compilation, native main or acceptance is involved.

Proposed operation `ordinary-reference-source-continuation-01` has one output,
`build/objects/ReferenceSource02.olean`, eleven source snapshots and twelve
retained support pins. Proposed outer90wall/60aggregateCPU/1536MiB/four processes;
inner75wall/45controllerCPU/32MiB cooperative fresh spool. Receipt schema is
`DMKN_ORDINARY_REFERENCE_SOURCE_CONTINUATION_V1`, status
`COMPILED_SOURCE_CANDIDATE_REUSING_PARTIAL_ENVIRONMENT_NOT_EXECUTED`.
The separate failed01 evidence is bound under `partial_provenance`, never changed
to a success. `generated_outputs` contains only the new Source02; `reused_support`
adds the separately pinned Environment to the unchanged eleven helper rows.

Builder SHA-256: `9063669bb434b39a141e755203f5b5e794de34d63682423827432de2bcd2a13b`.
Selector SHA-256: `8c1988195fc32628f6287b262a6e98796d2c0774e6d19081b1c84b4a66dea038`.
Selector requires reviewed `--build-sha256` and `--source-sha256`.
This agent made no execution; independent changed-boundary review and root's
separate launch remain required. Practical-next-decision research resumes
without turning this small parser repair into another experiment campaign.
