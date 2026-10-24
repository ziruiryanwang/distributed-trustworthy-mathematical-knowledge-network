# Ordinary module anchors: first implementable contract

2026-10-23, `query_native_boundary`. Source specification only; root separately
selects implementation and tests. This follows the adopted priority and independent
`ORDINARY-MODULE-ANCHOR-CHALLENGE.md`. Existing product bytes remain frozen.

## Scope and invariant

Support one explicitly selected, locally registered **modern five-part module**,
with a bounded one-parent chain. Preserve cold full-proof export when no anchor
is selected. No peer binaries, old-manifest adoption, legacy snapshot migration,
arbitrary branch merges, new theorem authority or admission-database schema change.

`Registered_P(A)` records an actual local event that established: the protected
artifact chain realizes an exact whole-unit portable map under policy P; private
proof records are warranted; ordinary public imports satisfy the checked export
relation. Immutable matching bytes and unchanged importer support preserve this
realization. Check only the missing delta privately and publicly, then register
the child after both fresh rereads. This inductive argument is conditional on the
existing kernel/codec/importer and trusted-local-owner premises. Hashes preserve
an established event; they do not create one from a caller's manifest.

## Owner API and physical state

Extend only `export-module` with optional `--module-anchor <64-hex AnchorID>`.
Omission means the unchanged cold route, now automatically registering successful
new exports. No register/import/migrate command and no automatic search for an
anchor. Return explicit `anchor_id`, `module_name`, `module_directory`, ordered
`import_directories`, and `new_catalog_acceptance: false`. These directories are
the protected local chain needed for normal Lean import, not a standalone child.

Use `<catalog>/module-anchors-v1/`, under the **existing held catalog owner lock**:

```text
STORE.json                      immutable owner/store/policy-format marker
operations/<fresh-op-id>/        reservation, owned copied artifacts and event data
records/<AnchorID>.json          final committed record, written last
BLOCKED                         uncertain live-child cleanup; blocks this sidecar
```

No second database or lock is necessary: every read/write requires the same live
eligible owner, and no network endpoint writes here. Reuse ordinary path/link
checks, bounded reads, canonical JSON, fresh writes/fsync and hashing helpers.
The existing catalog does not census these extra directories. Sidecar authority
is the same exclusive trusted-owner-storage assumption as owner acceptance, not
protection against an administrator rewriting both code and records.

First use may create a missing sidecar while holding the lock. Refuse a preexisting
malformed/unmarked directory; never import its contents. `STORE.json` binds schema
`DMKN_LOCAL_MODULE_ANCHOR_STORE_V1`, StoreID, catalog ADOPTION hash, activation
identity, semantic/foundation/implementation IDs and fixed limits. No absolute
external artifact path is retained as anchor authority. Generated export files
are copied once into the reserved operation directory, hash-compared and flushed;
the normal export output remains preserved, but the sidecar owns reusable bytes.

Private Python API in `anchor_store.py`:

```text
open_for_owner(owner, selected_support, check) -> Store
load(anchor_id, current_context, check) -> immutable AnchorView
reserve(parent_view_or_none, selected_request_pins, check) -> live Grant
_commit_generated(grant, validated_live_export, check) -> AnchorView
```

`_commit_generated` is called only by the export controller in the same operation
immediately after its actual clean worker, private/public rereads and final checks.
It requires the identical live Grant object held by Store, original unexpired
budget and owner lock. It has no saved-PASS-file recovery or public callback API.
The underscore is not a sandbox: trusted callers remain part of the stated TCB.

## Exact immutable record and support identity

Use canonical operational JSON with exact field validation, duplicate rejection,
bounded integers/strings and no floats; keep peer-evidence parsers unchanged.
Empty parent is `""`, not a new nullable mathematical encoding. Define AnchorID
as domain-separated SHA-256 of the final canonical record bytes (no self-ID).

Record schema `DMKN_LOCAL_MODULE_ANCHOR_V1` has exactly these fields:

| Field | Meaning |
|---|---|
| `schema`, `store_binding`, `support_id` | Schema; hash of STORE marker; exact checking/import support identity. |
| `operation_id`, `source_context_root` | Owned live generation operation and the genuinely warranted context. |
| `parent_anchor_id`, `module_name`, `direct_imports` | Empty parent + Init for the first anchor; otherwise exactly one registered parent module. |
| `targets` | Original materialization's exact name/ExportID/UnitID records, sorted by canonical name; at most 32. |
| `materialization_key` | Hash of policy/support, target identities and exact parent AnchorID/materialization; determines fresh bridge module name. |
| `artifact_parts` | Exactly five relative owned paths, sizes and SHA-256 hashes, in existing part order. |
| `units` | Only newly realized whole-unit records, described below; inherited units remain in parent records. |
| `added_names`, `matched_names` | Exact disjoint native report partitions; own module census is `added_names`. |
| `event_files` | Relative pins for request, inventory, anchor plan, native/phases reports and supervision, retained for audit. |

Each `units` row is `{unit_id, outputs, realization}`. Each output is
`{name, export_id, kind, level_params, inventory_sha256}` with the exact original
name, ordered universes and hash of its full original inventory row. `realization`
is `added` or `installed-singleton-theorem`. Derive this table once from the actual
validated full request/evidence and report, never from caller metadata. Include
matched installed theorems even though Init supplies their native records. Retain
whole output groups and exact ExportID derivation; no type-only theorem identity.
Original proof evidence remains in custody/event inputs, not copied into every
descendant record. Warm lookup does not decode old inventory rows or proofs.

Recompute `materialization_key` from domain `DMKN-ORDINARY-ANCHORED-MODULE-V1\0`
and canonical `{support_id, parent_anchor_id, targets}`; require module name
`DMKNBridge_` followed by that key. Parent AnchorID already commits to its exact
materialization/parts. No old request parsing is needed to validate this binding.

`support_id` hashes a fixed versioned descriptor: installation manifest and
implementation/semantic/foundation IDs, module policy, exact module controller,
collector, store, worker, owner facade/registration path and native source pins,
directly used Python helper pins,
and the transitive native helper parts actually used by this builder/importer.
The current native helper closure is OriginalExpr, OriginalDecl, CheckedExtension,
BootstrapSupport, OwnerRebind and OrdinaryExport, plus the pinned Lean runtime.
The implementer must enumerate the Python dependency set during source review.
Do not substitute the whole package PROFILE hash: query/docs-only changes need
not invalidate anchors. The existing **full profile verification remains before
and after each operation**; this narrower compatibility key is not permission to
skip support checks. Any changed selected support refuses warm reuse; automatic
compatibility migration is outside v1.

## Bounds and load procedure

Initial ceilings, reducible by configuration but never silently enlarged:

| Resource | Ceiling |
|---|---:|
| New proof units / evidence bytes / request bytes | Existing 32 / 4 MiB / 4 MiB |
| New nodes / names / edges / targets | Existing 131072 / 4096 / 32768 / 32 |
| Selected anchor chain | 32 modules, no branching/cycle |
| Registered unit/name union on that chain | 1024 units / 16384 names |
| Selected five-part artifact bytes | 256 MiB total; existing 64 MiB per module |
| Each record / combined selected records / native anchor plan | 2 MiB / 4 MiB / 4 MiB |
| Per-operation sidecar reservation / nonartifact retained metadata | 128 MiB / 32 MiB |
| Sidecar retained operations / total files' bytes | 256 operations / 1 GiB, including orphans |

The entire operation keeps its original shared time/CPU/I/O envelope. These are
first-profile operational bounds, not a claim of arbitrary local-context scale.
Before writes, bounded census reserves storage including failed/pending work; no
automatic deletion or eviction. Exhaustion is a capacity refusal. Cold export
still has its existing full-closure bounds; a single oversized unit is unresolved.

`load` follows only the explicit ID's parent chain, verifies record-address hashes,
schema/store/support/eligibility, exact headers/part names and every artifact pin,
and merges only its small unit maps. Every registered output in the entire chain
must agree with the selected current owner context, not just requested targets.
Reject name collisions, repeated unit ownership, partial group maps, altered
universes/kinds, incompatible policy, missing parts or withdrawal. Do not scan
unrelated cached records or treat available files as evidence of registration.
Existing profile/context reconstruction costs and selected-artifact hashing remain.

## Closure and native request delta

Pure seam: add frozen `AnchorFrontier(anchor_id: str, units: tuple)` where each
unit is `(unit_id, outputs)` and each output is `(canonical_name_key_bytes,
export_id)`. Empty frontier is `AnchorFrontier("", ())`. Add keyword parameters
`anchor_frontier` and `anchor_plan_sha256` to `collect_closure`; the latter is a
caller-bound hash, not proof authority. The collector opens no files/registry.
Check every frontier name/ID, ExportID derivation, whole-group uniqueness and
current warrant before traversal; bound the frontier by the table above. Require
nonempty ID iff nonempty frontier. Explicit target UnitIDs must match anchored
units, not merely their ExportIDs. The caller authenticates completeness/origin.

Extend immutable Closure with `anchor_id` and sorted actually reached
`cut_unit_ids`; retain all old counters/bindings/evidence fields. `request` is
`None` only for all-anchored reuse, with empty ordered units/evidence and zero
fetches; otherwise it is the complete V2 request. Its reuse status is explicit
and mathematical_acceptance remains false. This data shape allows independent
pure-collector work without implementing storage or a native importer.

The fresh collector accepts that immutable `AnchorFrontier`. Its cutoff is the
fixed basis plus complete anchored units. `schedule(name, ExportID)` cuts only
when the exact registered unit and all its outputs match the warranted map;
otherwise retain existing full-evidence fetch, verification and all-import walk.
Reject partial overlap/conflicting names. Planner input is basis + anchored
bindings, not the entire owner context; require every unanchored unit to be new,
all its dependencies resolved, and deterministic topological order. Preserve the
existing `ordinary_admission._plan` and portable codecs; do not invent a planner.

If targets are all anchored, return `REUSED_LOCAL_MODULE_ANCHOR` after load and
exact target validation: same AnchorID/module/chain, zero native calls, no new
registration, no fabricated empty module. A fresh output may contain only a reuse
summary. Its requested targets are separate from the anchor's immutable original
targets/materialization; never rewrite the old manifest. If units remain, the
32/4 MiB caps count **only the unanchored delta**.

Use request schema `DMKN_ORDINARY_MODULE_REQUEST_V2`: existing request fields plus
`anchor_id` and `anchor_plan_sha256`. Keep delta request ≤4 MiB. Separate protected
`anchor-plan.json`, schema `DMKN_LOCAL_MODULE_ANCHOR_PLAN_V1`, contains exactly
`schema, anchor_id, support_id, modules, bindings`; empty anchor has empty arrays.
Modules are oldest-first `{anchor_id, module_name, direct_imports, added_names,
artifact_parts}`; worker paths are explicit absolute ordinary paths derived from
owned records. Bindings are the registered unit/output maps. Controller derives
and pins this plan; native echoed IDs are not cryptographic authority. The worker
binds plan/parent parts before/after phases under the same single Job allowance.

Native successor behavior:

1. Import only pinned Init (cold), or the exact registered parent using an explicit
   full-chain five-part `ImportArtifacts` map and runtime-only fallback (warm).
   Retain modern-module checks; legacy `LocalSnapshot` is never an anchor.
2. Decoder allow-set is fixed basis + registered output names + earlier new names,
   not all imported constants. Validate imported headers/own name census against
   the plan. Prior live realization plus exact bytes/support supplies old meaning;
   do not call full `checkInventories` over old proofs again.
3. Preserve current residual installed-singleton matching using its complete new
   selected evidence. All other additions use unchanged checked insertion. A
   different identity under an anchored name is a conflict, not an installed match.
4. Perform both private and actual public delta checks; preserve transparent bodies,
   group/recursor computation and theorem-handle rules. Private success does not
   waive a public failure caused by proof erasure or hidden computation.
5. Write only newly added declarations with exactly the selected direct import.
   Both fresh rereads use the same exact parent plan and validate child headers,
   new inventory/report partitions and target resolution (anchor or new output).
   A nonempty residual containing only exact installed matches may return an
   explicit no-new-module refusal in v1; do not manufacture an empty child.

## Call flow, commit and faults

Owner locks/open existing context → verify profile → open sidecar/load optional
anchor → collect delta or return reuse → reserve live operation → existing
three-phase native event → controller validates exact report/bytes/support →
copy/flush bounded owned artifacts/event files → recheck parents/context → commit
record last → return owned import directories. Source-return extraction and
admission remain unchanged; dependencies outside the anchored map still need
their evidence. Normal project consumers must retain/import the returned chain.

Write the final canonical record to a fresh staging file and fsync it, then rename
without overwrite on the same volume to `records/<AnchorID>.json` while locked.
That namespace publication is the local commit point; re-read and verify it.
Before publication, all failures leave charged ineligible orphans. After publication,
later reporting failure does not revoke a valid receipt. Commit ambiguity causes
`COMMIT_UNKNOWN`, no retry; a later explicit exact-ID lookup may establish whether
the already-written complete record exists and all its files validate. It never
reconstructs missing authority from saved success reports. Missing data after a
crash fails closed. Do not promise power-loss durability beyond flushed files,
same-volume filesystem semantics and subsequent validation.

Uncertain worker cleanup marks this sidecar BLOCKED and denies further anchor
work until explicitly resolved; do not mint a receipt or invalidate unrelated
accepted mathematics. Ordinary missing/corrupt/withdrawn support refuses warm
use without a silent cold fallback. Parent files are retained while referenced;
automatic garbage collection and state migration are not part of this change.

## Candidate successor ownership and smallest checks

All proposed new files are under `software/v5/ordinary_module_anchor/`:

- **Pure/state author:** new `anchor_store.py`; successor `module_closure.py`
  from ordinary_module_bridge. Implements records/grants/load/frontier only.
- **Native author:** successor `OrdinaryModule.lean` and `module_worker.py` from
  ordinary_module_matching; only anchor import/plan/delta/readback changes.
- **Root:** successor `module_export.py` from ordinary_module_matching, controller
  call flow and integration. In fresh `ordinary_module_anchor_package/`, own
  `owner.py`, `profile.py`, `build.py`, `source-map.json`, `assemble.py`, `README.md`;
  derive from current selected recipe/package, explaining every changed payload.
- **Independent reviewer:** read actual deltas and this contract before any run;
  no author changes another owner's files or any used source/installation.

Reuse unchanged core admission/database, codecs, native checked insertion,
supervisor, discovery and query. No first-phase compile/helper changes are expected.
First inspect the selected helper dependency list, exact commit API and header
preservation argument. Stop before implementation if authority requires a copied
manifest, old proof re-encoding or a new unreviewed importer assumption.

After source clearance, propose one bounded pure-control group for whole-unit
cut/caps, missing/conflicting context, old/uncommitted/external-manifest rejection,
chain/census/policy limits, commit uncertainty and all-anchored reuse. Test-only
inert grants/files establish storage contracts, never mathematical acceptance.
Then one narrow native integration may generate/register A, export a genuinely
dependent B using A, and use B by ordinary import; choose already warranted
saved mathematics to avoid another admission campaign. Assert A's proof evidence
was not fetched/decoded, B's request contains only delta and both views passed.
Reopen and request anchored targets with zero native calls. Include one selected
parent-binding/public-view refusal justified by the source review. Do not rerun
old query/discovery tests or run a synthetic 33-unit native stress campaign.

This establishes an incremental ordinary-module boundary, not net growth or
constant-time import. Remaining O(selected context/anchor metadata), artifact I/O,
resident memory and lifetime storage must stay in full-workflow accounting.
