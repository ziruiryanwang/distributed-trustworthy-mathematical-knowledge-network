# Offline selective export from an ordinary local custody

2026-10-26. Source-only feasibility review. No code import/execution, native run,
network, state access, Git mutation or implementation was performed. `P/` below
means the default package
`experiments/v5-local-checks/transport-release-handoff01/suite/assembled/package/`
selected by `software/v5/ordinary_release_bundle/ADOPTION.md`.

**Revised recommendation after root's challenge:** the accepted-target variant
below answers the original assignment, but its local-acceptance precondition is
unnecessary for inert export. Prefer the read-only, no-owner variant in the final
section. Existing-route findings are unchanged; do not implement both variants.

## Answer and decision

**No shipped public command currently exports arbitrary already accepted exact
targets from a no-project owner into a standalone inert dependency-closed bundle
without native work or serving that custody.** The necessary low-level building
blocks already exist. The gap is a bounded operator operation, not a missing
mathematical representation, new trust system or new network protocol.

A small `owner export-bundle` operation is justified for this workflow: a local
investigator has acquired and extended knowledge, wants to transfer selected work
offline or populate a smaller disclosure-approved serving state, and should not
need to reconstruct a compiled producer project or expose unrelated custody.
This materially supports provider-independent continuation and selective
mobility. It is not evidence of mathematical novelty or a general growth speedup.
Do not add a daemon, replication service, ACL, new bundle format or new native
checker for this seam.

## Existing routes checked first

| Existing route | Why it does not generally meet this request |
|---|---|
| Retained baseline bundle, then `intake-baseline` | Already sufficient if the exact desired complete closure is retained as a bundle. Reuse it directly. General mixed custody and later contribution branches need not have such a retained bundle. Reusing a larger bundle also discloses/imports its extra content. |
| `produce-baseline` | Requires an approved compiled project and native exporter, not just accepted no-project custody; `P/owner.py:285` and `P/authoring/py/baseline_production.py:150`. |
| `export-module` | Collects evidence but then invokes native module generation at `P/authoring/py/module_export.py:259`; emits local compiled artifacts and a module report, not a baseline bundle. Warm anchor export can omit the anchor's ancestry. These artifacts are not peer warrants. |
| Existing contribution outputs | `P/authoring/py/ordinary_contribution.py:563` saves the newly bound units and selected previews. It does not export the complete acquired/import ancestry from the owner. It may be sufficient for a fixed-basis-only contribution, not arbitrary later reuse. |
| `receive` output | `P/peer_api.py:622` retains bytes in custody; its final report at `:700` contains identities/accounting, not a complete standalone evidence bundle. The owner keeps bytes, but the report is not an exporter. |
| `publish` / preview / inspect | Publish creates index records and previews, not an inert closure. Preview/inspect are bounded network reads and not whole-proof export. |
| Serve privately, then receive into another owner | Requires service exposure and temporary coexistence of source and receiver. Loopback is not a confidentiality boundary against other local users. It is an existing option only when disclosure scope is acceptable, not an answer to this request. |
| Owner status / catalog migration | Status reports bounded root/count metadata, not raw selected evidence. The catalog's private legacy activation seam is not a general export and copies compiled-state provenance, not a new portable warrant. |
| Existing Python APIs | `OrdinaryStore.get_locator/get_evidence` plus `baseline_bundle.split_units/make_manifest` provide nearly all primitives. Combining them correctly is a new small adapter; telling every operator to write one is not a shipped workflow. No direct SQLite editing is necessary or appropriate. |

The closed command lists are `P/owner.py:41`, `P/peer.py:42`, and `P/run.py:25`.
There is no hidden inert export CLI in those lists. A retained cold module request
or old contribution files can sometimes be converted manually, but that requires
reconstructing exact bindings/closure and is not a general supported route.

## Minimal data-only operation

Inputs: approved existing package/runtimes; exact owner/custody/store selection;
an explicit existing local context root; exact target rows
`{name, export_id, unit_id}`; original finite wall/CPU/memory/output and structural
limits; an absent output directory disjoint from implementation/state/inputs.

1. Use the existing serialized owner-open path and protected context validation.
   Require every selected target's exact name/export binding in that context,
   and the existing semantic/foundation policy. No newest-root inference.
2. Traverse the union of complete declared-import closures from the selected
   target units. Read exact locators and bytes through `OrdinaryStore` methods,
   verify locator name/semantic/export identities, reparse the evidence, and
   verify actual target/group outputs. Deduplicate units; retain their bytes
   unchanged. Require all group outputs and all imports to agree with that
   selected local context. Stop only at the exact pinned fixed basis.
3. Order/check the collected units using existing `A._plan` against a **basis-only
   structural planning context**, not the full owner context. Require READY,
   no missing premises, no reused units and exact closure census. The restricted
   planner prevents all already accepted units from being elided as warm reuse;
   it is structural planning, not fabricated mathematical acceptance.
4. Call existing `baseline_bundle.split_units`, then `make_manifest` on that
   order. Both are public pure functions (`P/reference/baseline_bundle.py:313`
   and `:335`). Do **not** rebind through `bind_writer`: preserve original raw
   evidence, UnitIDs and ExportIDs. No new serialization semantics are needed.
5. Write only derived `units/<validated-id>.json` files, a finite exact-target
   export report/census, and the existing baseline `manifest.json`, with fresh
   writes, readback/hash checks and bounded output census. Preserve partial
   failures. Manifest presence alone is not a successful terminal operation.
6. The ordinary receiver uses existing explicit `owner intake-baseline` with
   exact bundle/manifest pins. Source-local acceptance does not transfer; cold
   recipient checking remains mandatory. Do not fabricate a producer report to
   pass the kit's narrower producer-report convenience path.

Reuse the full closure pattern in `P/authoring/py/module_closure.py:187` and the
locator callback in `P/authoring/py/module_export.py:197`. Do not invoke the module
collector wholesale: its module name/anchor plan/request construction and
32-unit/4-MiB materialization bounds are unrelated to inert bundle export. In
particular, do not use the no-project authoring **signature** frontier here:
cold recipients need the complete imported proof evidence, not scratch axioms.

## Explicit limits and guarantees

The least change uses existing preflight bounds, not larger bespoke limits:
at most 1,024 units / 64 MiB total / 2,097,152 nodes / 65,536 output names /
1,048,576 import edges, or smaller caller-selected values. Individual units must
also satisfy the selected custody and baseline bounds. Refuse beyond the selected
envelope. Existing baseline batching may partition the resulting closed sequence;
it does not justify silently raising the planner's aggregate bound.

The closure is minimal under **declared import edges and indivisible units**,
not a decision procedure for mathematically minimal assumptions. Group siblings,
definitions and proof-only dependencies may be unavoidable disclosures. Export
is an explicit copy into an operator-controlled staging directory; it does not
authorize network publication. Inspect its full census/content before serving.

Cost is selected-evidence I/O, parse/hash, dependency ordering and file writes,
plus existing local protected-context validation. `portable_catalog.context`
(`software/v5/ordinary_lean/portable_catalog.py:530`) checks the local lineage and
snapshot bytes; therefore do not claim cost depends only on exported units or
that a huge local catalog is free. No global library scan or native Lean check
is inherent to the export helper, but receiver cold checking remains.

The existing owner-open path can mark interrupted reservations; do not call this
operation a bitwise read-only open of all state. The helper adds no mathematical
acceptance, custody writes, new catalog roots, project/native import, source
compilation or service. It uses the existing protected-state/serialization
assumptions and must not accept arbitrary paths from evidence.

## Benefit and implementation bar

Against an already retained exact closed bundle, benefit is zero: use that bundle.
Against arbitrary mixed no-project custody, the alternatives are a custom API
script, broader disclosure/copy, reauthoring/recompilation, or live service plus
network reacquisition. A supported bounded exporter removes those obligations
using existing inert mathematics, then enables existing independent intake.
This is enough practical value to select a small implementation now, provided
root keeps scope to the operation above rather than a new replication system.

Changed-boundary controls should cover exact bytes and independent branches,
fixed-basis stops, missing/changed warrants, wrong locators, group siblings,
cycles/conflicting names, exhausted closure/output budgets and preserved partial
outputs. Existing schema/parser/transport/native campaigns need not be repeated.
The only decisive integration question is whether the unchanged intake accepts
the exact generated bundle into a fresh small context. That is a later separately
selected finite check, not authorized or executed by this feasibility note.

## Revised, smaller boundary: inert export does not need owner acceptance

Root correctly challenged the premise: the receiver independently checks the
result, so an exporter need not restore or attest any source owner's mathematical
context. It may move exact selected stored evidence, including evidence which
has never been accepted or was refused. This is no weaker than receiving inert
data over the existing peer interface. Therefore prefer **one standalone bounded
custody-export operation**, not an owner-context acceptance feature.

Keep exact target rows, semantic policy, fixed-basis import identities, complete
declared-import traversal, structural conflict/cycle checks, preserved raw bytes,
baseline manifest and recipient intake. Remove source catalog, local context root,
owner/native snapshot validation, accepted-status claims and source execution.
The report must say source acceptance was not checked and the output is inert.
It must not impersonate `PRODUCED_INERT_BASELINE_NOT_ACCEPTED` from a compiled
project or a successful owner admission. Structural closedness is enough for
export; an invalid mathematical proof may legitimately export and later fail
independent intake.

### Read-only source integration

The present `OrdinaryStore(..., create=False)` is not a strict read-only opener.
`P/support/transport/ordinary_acquisition.py:98` opens SQLite read/write and sets
`journal_mode=DELETE` and `max_page_count`; its existing journal handling permits
ordinary recovery. Reusing that constructor while claiming no source writes is
incorrect. It also acquires no custody-specific process lock.

Smallest principled reuse: add a narrowly scoped read-only opener on a fresh
successor of `OrdinaryStore` (or a small public reader with exactly its existing
getters), with these conditions:

- Retain absolute canonical/non-reparse path, single-link database, finite file
  size, selected semantic ID and exact custody-limit configuration checks.
  Operator approves the local store; it is not an arbitrary remotely supplied
  SQLite database.
- Open `database.as_uri() + '?mode=ro'` using `uri=True`; enable `query_only=ON`,
  `trusted_schema=OFF`, bounded in-memory cache and `mmap_size=0`. Do not set
  persistent journal/max-page-count values or create directories/metadata.
- Refuse existing `-journal`, `-wal` or `-shm` rather than performing hidden
  recovery. A source requiring repair must use its separately authorized normal
  recovery path, not be repaired as an export side effect.
- Start one bounded read transaction and establish its snapshot by reading the
  exact configuration/meta row before traversal. Keep the same connection until
  export selection/readback completes. SQLite read locking supplies a coherent
  snapshot against cooperative writers; a busy/locked source refuses within the
  original deadline, without retry/renewal. The finite read transaction can delay
  writers, which is an explicit operational cost, not a mutation of mathematics.
- Do **not** set `immutable=1` merely to bypass locks: that would assume away
  writes by other ordinary commands. Protected paths/no same-account hostile
  replacement remain a premise, as for the existing system. An operator-selected
  stable custody plus the SQLite snapshot does not require loading a mathematical
  owner merely to borrow its catalog lock.
- Reuse exact `get_locator` / `get_evidence` identity checks and parameterized
  lookups; parse each selected unit and all its imports under aggregate limits.
  Native checked snapshots and proof ancestry outside the selected closure are
  not inputs. Close/rollback the read transaction on all outcomes.

The repository already uses `mode=ro`, `query_only` and sidecar-refusal at
`software/v5/grounded_cut_basis/source_anchor.py:217`; that source is precedent,
not a dependency to import or a reason to restore its certificate machinery.
Its owner lock protects a different authority-bearing operation. Here there is
no source mathematical authority to transfer.

This revised boundary avoids the full local-lineage hashing identified above.
Expected work is finite indexed reads plus parsing/hashing the selected closure,
structural ordering and exact output writes; SQLite lookup cost and selected
store-file configuration checks remain. It does not establish constant cost,
unlimited export size, cheap recipient cold checking or secure handling of a
hostile replacement SQLite file. Scope and implementation controls should target
this one smaller variant; the earlier accepted-state variant is not recommended.
