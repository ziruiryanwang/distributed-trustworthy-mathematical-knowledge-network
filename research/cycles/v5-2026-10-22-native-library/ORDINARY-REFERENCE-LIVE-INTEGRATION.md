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
