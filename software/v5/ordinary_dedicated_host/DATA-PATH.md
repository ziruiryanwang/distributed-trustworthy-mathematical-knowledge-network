# Dedicated ordinary custody/index hosting: existing data path

2026-10-28. Source-only finding; no code, imports, runtime, owner data or Git access.
**No mathematical or protocol redesign is needed.** The current SDK already
supports inert hosting without an OrdinaryAdmission owner. The missing public
boundary is fresh-store preparation and enforceable dedicated-store exclusion.
Paths below are relative to `software/v5/`.

## Selected existing code, not an older similarly named lane

`ordinary_advisory_query/source-map.json:60-82` and the prior
`ordinary_current_distribution/source-map.json:59-81` select:

- `ordinary_multi_source/peer_api.py`, `ordinary_multi_source/ordinary_acquisition.py`;
- `ordinary_sparse_access/discovery_store.py`;
- `ordinary_formal_query/discovery/ordinary_export_adapter.py`;
- `ordinary_binding_reuse/baseline_bundle.py`, exposed as `loaded.baseline_intake.B`.

The package loader returns `loaded.O`, `loaded.peer_api`, `loaded.baseline_intake`
and the verified installation (`ordinary_advisory_query/profile.py:258-265`).
Loading still hashes pinned installed/runtime support; it does not ground a
mathematical owner or run Lean. Preserve that installation and all portable IDs.

## Exact existing interchange and validators

The shared file bundle is canonical `DMKN_ORDINARY_BASELINE_BUNDLE_V1`:

```text
manifest.json = {schema, semantic_id, batches: [[
  {unit_id, raw_sha256, raw_bytes}, ...], ...]}
units/<unit_id>.json = exact canonical portable V2 evidence bytes
```

`baseline_bundle.read_manifest(raw, expected_sha256, limits=..., check_budget=...)`
validates canonical shape, semantic ID, duplicate IDs, batches and aggregate
unit/byte limits (`ordinary_binding_reuse/baseline_bundle.py:221-258`). Entry paths
are derived from validated IDs (`:96-111`), never arbitrary bundle paths.
`validate_batch(entries, raws, limits=..., check_budget=...)` binds every exact
length/hash/unit identity and structural census (`:261-287`); accumulate returned
censuses across all batches, including operation-wide nodes/names/edges/binding
limits. Existing `ordinary_intake_progress/baseline_intake.py:170-178` supplies
`_read_batch`, the bounded file-read-plus-validator seam. Do not invoke intake:
intake adds the mathematical owner and admission that this role does not need.

`ordinary_producer_package/baseline_production.py:271-324` writes this format;
its result/PRODUCTION metadata supplies `{name,export_id,unit_id}` target rows.
`ordinary_custody_return/custody_return.py:194,205-206,241-262` writes the same
format, with targets in pinned `obligations.json`. Its `selected-units` policy
does not acquire ancestor units; `closed-basis` does. Obligations/producer reports
are inert selection metadata, never acceptance or a replacement for byte checks.
The manifest itself contains no target list. The selected CONTRACT embeds the
explicit nonempty target list in the pinned prepare config, alongside the selected
bundle/manifest SHA-256; require
every target unit to be present and bind its original name/export ID to actual bytes.

## Reusable prepare operations

1. Capture/validate all request pins, bounded manifest and target shape. Use a fresh
   dedicated root, fresh custody and index children, all separated from input
   bundle, package/runtimes and any owner state. Reject symlinks/reparse/hardlink
   aliases with existing ordinary-path checks. Never accept arbitrary preexisting
   owner custody as a dedicated host by merely relabeling it.
2. `loaded.O.OrdinaryStore(custody_path, semantic_id, custody_limits, create=True)`;
   validate/read each batch, then `put_evidence(raw, before_commit=check)`. The
   unchanged put parses semantic syntax, records exact bytes and creates locators
   for **every output of each whole unit**, transactionally (`ordinary_multi_source/
   ordinary_acquisition.py:156-230`). No proof/dependency acceptance is asserted.
3. For each selected target, reuse `PP.preview_from_evidence(raw, name)`,
   `PP.resolve(preview, raw)` and `PP.read_preview(preview).export_id == export_id`;
   also require the parsed unit ID to equal the target's unit ID. These routines
   validate an actual selected header and its exact portable type bindings
   (`ordinary_lean/portable_preview.py:89-128,147-161`). Unresolved mathematical
   imports are allowed in this inert role; no basis closure must be downloaded.
4. `custody.put_preview(preview, before_commit=check)` followed by
   `DS.Store(index_path, OrdinaryExportAdapter(semantic_id), index_limits,
   create=True, access_pairs=...)` / `index.admit(preview, expected_id=export_id)`.
   Prefer the existing `loaded.peer_api._index(loaded, None, custody, config, check)`
   constructor for its exact config/separation checks (`peer_api.py:813-824`).
   `Store.admit` binds preview bytes, locator/object ID, features and current index
   namespace; each target commits separately (`discovery_store.py:221-274`).
   **Do not call `peer_api.publish`**: its distinct claim is checked local outputs
   and it correctly requires `owner.catalog.context` (`peer_api.py:827-866`).
5. Retain partial state on any refusal; do not publish it as ready or silently
   resume it. After complete exact readback, final input-pin checks and successful
   index/custody closes, publish one fresh final preparation marker by the existing
   pending-file/final-rename pattern. Bind package/profile, semantic/index namespace,
   manifest and target hashes, dedicated relative store paths, exact store limits
   and access-pair config. Record inert assurance and explicit whole-store sharing.
   A saved marker is operational readiness under protected storage, not mathematics.

## Exclusion, serving and readiness are the actual new boundary

`peer_api.serve(loaded, custody, config, allowance, ready=callback)` already uses
`_state(loaded, None, custody)` and `_index(loaded, None, custody, ...)`
(`ordinary_multi_source/peer_api.py:893-964`). It needs no catalog/root/store ID.
Its docstring explicitly permits API-only inert rehosting with caller serialization.
The shipped `ordinary_sparse_access/peer.py:223-226` obtains an OrdinaryAdmission
lock because it handles owner stores; bypass that CLI by exposing this existing SDK
role with its own dedicated lifecycle, not by pretending its lock is unnecessary.

Hold a real protected Windows OS lock for the dedicated root throughout prepare,
and throughout each later serve from before custody/index opening through all
provider/index/custody closure. Reuse the one-byte ordinary-file `msvcrt.LK_NBLCK`
pattern (`ordinary_lean/portable_catalog.py:180-188`), not an owner catalog.
Both store classes assume serialized callers; `exclusive:true` is an assertion,
not exclusion. Fresh dedicated children plus the same lock for every supported
host operation prevent accidental mixing with a mathematical owner's stores.
External hostile writers remain outside the existing protected-owner/OS model.

Serve rechecks the selected preparation marker/pins/config and opens custody with
`create=False`; its index config must also use `create=False`. It requires
`share_all_custody:true`, `exclusive:true`, finite 1..3600-second lease, 10..60-second
cleanup reserve, provider caps and one original outer Job allowance. Loopback may
use no TLS; non-loopback needs pinned TLS files (`peer_api.py:910-955`).
Preparation's marker means configured stores. A **separate per-invocation** ready
record comes only from the existing callback after `provider.start`; it is tied
to that invocation/lease and cannot make an old ready file evidence of a listener.
API cleanup stops provider, drains tasks and closes index; caller must close
custody and release the dedicated lock even on PeerFailure (`:976-1008`).

Exact database files are `<custody>/ordinary.sqlite` (`ordinary_acquisition.py:96`)
and `<index>/discovery.sqlite` (`discovery_store.py:70`). Serving uses custody getters
and index snapshot/summary/page/candidate reads; `snapshot(:210-218)` reads an
existing descriptor, not `_seal`. No content admission/refresh occurs. Both stores
still use read-write SQLite handles and configuration PRAGMAs, with possible
recovery/configuration file effects. Describe an immutable hosted generation,
not filesystem-read-only operation. Current public auxiliary entrypoints can
reject dedicated-root-descendant mutable state/output paths using the permanent
host marker; old executables and arbitrary same-user SDK calls remain outside
that cooperative exclusion guarantee.

Whole-store disclosure is material: all selected unit bytes and all generated
export locators are addressable even if only some targets are indexed. There is
no per-object ACL. Approve that whole dedicated bundle, not just its target names.
An incomplete dependency bundle may still be hosted honestly; availability of
missing imports and receiver mathematical admission remain separate. A fresh
prepare/seal/serve wrapper is sufficient; no new network/storage schema, global
registry, grounding, certificate or proof replay is required. The blocking issue
for exposing the role today is lifecycle enforcement, not a theoretical data-path gap.
