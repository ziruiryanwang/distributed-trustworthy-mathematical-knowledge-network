# Incremental ordinary modules: pure frontier and protected sidecar

2026-10-23, `anchor_state_impl`. Source implementation only. No product import,
test, Lean invocation, owner/database open or experiment has been performed.
Root selects execution separately. Predecessor sources and evidence are unchanged.

## Implemented boundary

`software/v5/ordinary_module_anchor/module_closure.py` is the selected successor
of the old bridge collector. Its immutable `AnchorFrontier` authenticates nothing
itself: the protected controller/registry must supply complete registered units.
It validates every frontier output against the selected warranted context before
traversal, checks exact ExportID and target UnitID relationships, rejects all
basis/anchor/new-group collisions and passes only basis plus frontier to the
unchanged planner. Delta limits remain 32 units / 4 MiB; the frontier itself is
bounded to 1024 units / 16384 names / 4 MiB compact name/ID material. All-anchored
targets produce `request=None`, no fetches, and no mathematical acceptance.

`anchor_store.py` adds a sidecar under the existing held catalog owner lock.
No generic register/import/recover/migrate entrypoint exists. The trusted selected
controller alone calls `_commit_generated` with the identical unexpired live
grant after the actual native event and both fresh rereads. The sidecar derives
whole-unit output metadata from the pinned complete new request, binds the exact
native partition, copies five local artifact parts and seven event files once,
rechecks the current context and parents, and publishes the final record last.

Warm loading verifies compact records, exact current warrants, artifact hashes,
chain imports and representation identities. It does not reopen or decode old
proof request/event files. Event-file pins remain retained audit evidence, not
authority that can reconstruct a missing registration. Imported artifact hashes
preserve the already checked headers; native warm use also validates those actual
headers through its explicit complete artifact map.

## Exact controller seam

```text
open_for_owner(owner, selected_support: bytes, check) -> Store
Store.support_id: str
Store.plan(parent: AnchorView | None = None) -> canonical bytes
Store.load(anchor_id, current_context, check) -> AnchorView
Store.reserve(parent, selected_request_pins, check, *, deadline) -> live _Grant
Store._commit_generated(grant, validated_live_export, check) -> AnchorView
Store.abandon(grant, reason)       # no child started, or actual cleanup known
Store.mark_blocked(grant, reason, check=None)  # uncertain cleanup
```

`AnchorView` is frozen and contains `anchor_id`, textual `module_name`,
`materialization_key`, `module_directory`, oldest-first `import_directories`,
`frontier`, `plan_raw`, oldest-first immutable `records`, `artifact_bytes`,
`store_binding`, and `support_id`. It contains no mutable parsed record tables.

`selected_support` has exact fields `schema`, `installation_manifest_sha256`,
`semantic_id`, `foundation_id`, `implementation_id`, `policy`, `sources`, and
`native_helpers`. The schema is `DMKN_LOCAL_MODULE_ANCHOR_SUPPORT_V1`. `sources`
maps explicitly enumerated trusted roles to `{bytes, sha256}`; `native_helpers`
is a sorted list of `[logical_name, bytes, sha256]`. The manifest already binds
the selected core/runtime. Root's controller selects and verifies the exact
dependency set; the narrower support key never skips full profile verification.

The reservation selection has exact fields:

```text
source_context_root, targets, materialization_key,
request: {bytes, sha256}, inventory: {bytes, sha256}, anchor_plan: {bytes, sha256}
```

The live export has exact fields `request` (original immutable bytes), `report`
(actual validated in-memory native report), `artifact_parts` (five ordered
`{path, bytes, sha256}` rows), and `event_files` (same pin shape under fixed names).
Fixed events are `request.json`, `inventory.json`, `anchor-plan.json`,
`native-report.json`, `native-report.json.pending`,
`native-report.json.phases.jsonl`, and `SUPERVISION.json`.

The plan matches the native author's agreed schema. Module/direct-import names
are structured Lean names, not strings; bindings carry complete unit/output rows.
Absolute artifact paths appear only in the transient plan. Registered artifact
and event paths have exact sidecar-relative forms.

## Deliberate contract refinement: durable cleanup knowledge

The reviewer identified a crash gap if `BLOCKED` were the only indication of
uncertain cleanup: writing that marker could itself fail. Root accepted this
minimal refinement before implementation:

- `RESERVATION.json` is flushed before a worker may start.
- `CLOSED.json` is written only when the live controller knows no child started
  or all child cleanup is complete, including clean native failure.
- An existing reserved operation without a valid CLOSED marker independently
  refuses a new store open. Thus a crash or failed BLOCKED write is fail-closed.
- `_commit_generated` records known cleanup before committing the final record.
  Clean failure abandons the grant but preserves all bytes as charged orphans.
- Cleanup metadata may be recorded after budget expiry, under the still-held
  owner lock, with a bounded 256-character reason. It performs no native work
  and never renews the mathematical operation allowance.

No automatic cleanup recovery or receipt reconstruction is supplied. A genuinely
missing/incomplete reservation may conservatively block later work; resolving
that exceptional operator state is explicit future work, not silent reuse.

## Commit outcomes and bounds

The commit point is a same-volume Windows non-overwriting rename into
`records/<AnchorID>.json`. Atomic publication is not a promise of unqualified
power-loss durability. Files are flushed; later loads verify retained state.

`AnchorCommitUnknown` exposes `anchor_id` and a structured `report` with status
`COMMIT_UNKNOWN`. Publication/readback ambiguity must not be retried. A later
explicit exact-ID lookup can determine whether the complete record exists.
`AnchorCommittedError` instead records `COMMITTED_LOCAL_ANCHOR_REPORTING_FAILED`
if publication/readback succeeded but final view construction/reporting fails.
Neither `abandon` nor a late error revokes or overwrites a published record.

The fixed first-profile bounds include chain length, units/names, artifact bytes,
record/plan bytes, retained operation count and total store bytes. Bounded census
counts actual retained files and orphan bytes without hashing unrelated content;
reserve requires room for the whole 128-MiB operation envelope. A selected chain
still has metadata, artifact-integrity, import-loading and memory costs. This
source does not claim unlimited context scale, cheap cold verification, a net
growth advantage or final-v5 readiness.

## Review/next evidence

Collector `f053e9726bdba24724e7e44baa03ffa0006f80b068440086a36023068512aa8c`
received focused source review without a blocker. Registry source is handed to
`module_anchor_audit` for the exact changed boundary before any run. Root owns
the separate controller, native integration and bounded-control selection.

### Source review correction and minimal storage-control plan

The reviewer found that checking the aggregate event metadata bound only after
copying could leave a clean failed operation above its own reopening ceiling.
Registry successor `a244eaf2764b6a51f4006447eebe3b69529a46bf376f999804a99f23661a929e`
checks all artifact/event pins and reserves actual reservation bytes, 4096 bytes
for cleanup and the full 2-MiB record bound before any copy/directory creation.
The same 32-MiB metadata ceiling therefore holds even after partial failure.
The corrected source received focused clearance; it has not executed here.

Root separately assigned `storage_controls.py`, source only. It uses the existing
pinned package-loader/control helpers and real retained portable evidence. Exact-
class owners/catalogs are deliberately built with `__new__`, inert eligibility
and context methods, and an ordinary file handle without acquiring an owner lock.
Tiny artifacts are visibly NOT Lean modules. There is no database, native or
network call and no mathematical authority claim. This isolates storage behavior
without repeating admission, query or compilation campaigns.

Its eight groups cover:

- Complete-file/cleanup-before-commit ordering; warm lookup without proof-event
  reads/decoding; one child-chain materialization.
- Missing/manifest-only/uncommitted records and foreign live grants; clean abort
  reopening versus pending-reservation refusal.
- Missing or conflicting current warrants, whole-unit metadata collisions,
  incorrect export identities and artifact corruption.
- Record-address corruption, changed support and absent foreign-owner records.
- Missing artifact parts, retained orphan-byte charging and finite capacity.
- Oversized event metadata refused before writes, followed by clean reopening.
- An injected post-rename error: COMMIT_UNKNOWN survives abandonment and later
  exact-ID lookup validates the already-published record without reconstruction.
- Pending cleanup with and without BLOCKED, plus incomplete STORE refusal.

CLI: `--package --profile-sha256 --python-runtime --lean-runtime --output
--collector-sha256 --store-sha256`. Root should snapshot the controls, unchanged
collector and reviewed registry; pin the same existing helper, package/runtime
and retained evidence as the already selected frontier-controls path. No large
allocation is required; inflated metadata pins exercise refusal before copying.
The control plan is not a runtime selection or a substitute for the later actual
native A-to-B test and the controller's live-event authority review.

## Fresh source-build recipe, source only

Root subsequently assigned only `ordinary_module_anchor_package/build.py` and
`source-map.json`. The intended six-replacement/one-addition map was reported
before editing. The new recipe is derived mechanically from the preserved
`ordinary_distribution/build03.py` and `source-map03.json`, not a new compiler
or installation builder. The previously tested collector, registry and storage
controls remain unchanged.

Six logical payloads change: `authoring/py/module_closure.py`,
`authoring/py/module_export.py`, `module_worker.py`, `module/OrdinaryModule.lean`,
`owner.py`, and `profile.py`. The sole addition is
`authoring/py/anchor_store.py`. All 47 base inputs, receiver/authoring/extractor/
query lane rows, native runtime pins, helper companions and installation contents
remain unchanged. No new compilation lane is introduced: OrdinaryModule is still
shipped as selected source for the existing bounded worker.

The map therefore has 71 selected source inputs, 54 direct copies (19 installed,
35 auxiliary), 134 payloads excluding PROFILE and 106 auxiliary payloads. The
builder changes only its recipe prefix/file names, map hash, these fixed census
constants and explanatory heading. Its original three finite child Jobs and
original allowance accounting remain the same. This provides a reproducible
future source recipe; it is not authorization to rerun the existing build.

At handoff, a read-only exact comparison found no mismatch among the 71 selected
source pins. Recipe SHA-256:

- `build.py`: `8cf0ae6cf877b297315dc7b6861b39826faad7b8fa05656a5b2ad1834938ebf8`
- `source-map.json`: `9392b9e91f7bd8e8fd2022a524a716083525e07519a9ab163db22fd5289265da`

Root's controller/native source remains subject to its pending finite integration.
Any future pre-execution source repair requires explicitly updating this unused
map/recipe pin before adoption. No builder, assembler or compilation was run by
this author, and no Git state was changed.
