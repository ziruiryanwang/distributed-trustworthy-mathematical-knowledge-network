# Inert rehosting: current path and minimum missing interface

2026-10-26. Source/data-only decision; no product import, owner/database access,
native execution, test, network or Git mutation. Prior service-lifecycle and
same-owner concurrency conclusions are reused, not requalified here.

## Exact selection and answer

`P/` is `experiments/v5-local-checks/exact-module-assembly01/assembled/package/`.
Its observed PROFILE SHA-256 is
`bde63019d1a6ac2bccd8e0c245a405ad3ca551d0606c01a5193fee6897c60346`;
installation manifest is
`32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.
The nine source roles cited below were hash-checked against this actual PROFILE:
peer, peer_api, profile, run, baseline_bundle, discovery_store,
ordinary_export_adapter, ordinary_acquisition and http_provider. No old-source
variant or historical service note supplies the present selection.

Current handoff authority is `software/v5/ordinary_investigator_bundle/ADOPTION.md`:
169 payloads, archive SHA-256
`a757663ad564c382b55da98f5932efd26fe4c3d5e37e4561ef0127d31826fd28`.
Its relocated README and `guides/CONTINUE.md` offer checked-owner publication,
finite owner serving, and offline selected export/intake. **They do not ship an
owner-free bundle-to-discovery-and-service command.** Source APIs can express it;
that is not an existing turnkey operator route. Plain copying of an approved
bundle already solves offline byte preservation, but not this discovery service.

## What is already available

- `P/peer.py:174-226`: serve/publish require custody plus catalog/store arguments
  and open `OrdinaryAdmission`. Public serve cannot omit the mathematical owner.
- `P/peer_api.py:738-800`: publication first checks targets against the selected
  catalog context; only then derives previews, puts them and indexes them.
  Serving itself is inert; the CLI's owner opening is an operational coupling.
- `P/support/transport/ordinary_acquisition.py:68-217`: `OrdinaryStore` is inert
  SQLite custody. `put_evidence` checks syntax/IDs and derives locators for every
  actual unit output. `put_preview` stores exact structural metadata. Neither
  creates a mathematical warrant nor checks dependency closure/Lean typing.
- `P/support/discovery/discovery_store.py:221-274`: `Store.admit(preview)` derives
  exact metadata through its adapter and atomically indexes it; this unfortunate
  method name means index insertion, not mathematical admission. No acceptance
  callback or catalog is needed. Its status/results explicitly say false.
- `P/support/discovery/ordinary_export_adapter.py`: the selected exact-type
  adapter derives bounded formal features from previews. It checks semantic
  revision, exact export locator and syntax, not theorem truth or global coverage.
- `P/support/transport/http_provider.py:181-208,381-447`: Provider can expose those
  stores with existing wire routes, bounded requests/replies and finite lifecycle
  control supplied by a caller. It has no mathematical acceptance operation.
- Selected-export's `export.py`/`selected_export.py` already produce exact,
  bounded basis-closed bundles from protected custody without catalog/native use.
  `ordinary_custody_return` also writes existing bundles; its `closed-basis` and
  receiver-relative policies must not be conflated. Neither companion consumes
  a bundle to create an inert service. No new data format is needed for that edge.

## Compare the two candidate implementations

| Route | Reuse | Additional obligation / reason not already supported |
|---|---|---|
| Fresh OrdinaryStore + DiscoveryStore | Existing structural put, locator generation, preview adapter, index, exact-byte serving and Provider | Small operator companion must validate bounded bundle inputs, create two fresh stores, derive selected previews, record scope, close preparation, then run a finite lease under supervision. Existing copies/index costs remain. |
| Immutable baseline-bundle-backed reader + existing index | Avoids a second evidence copy; manifest already names exact unit bytes | Not a drop-in reader: Provider dispatch calls `ordinary_acquisition.serve`, which requires `type(store) is OrdinaryStore` at line 289. Subclassing/duck typing does not pass. New role/dispatch compatibility and locator/preview lookup, selected-file mutation detection, bounds and lifecycle handling need specification and review. |

Recommend the fresh-store companion first if this workflow is selected. It keeps
the actual protocol/provider and mathematical receiver unchanged. A new immutable
reader is justified only if avoiding the additional evidence copy materially
outweighs its larger changed boundary. No live DB copying, pretend admission
callback, catalog bypass or weakening of the existing exact-type guard is needed.
The resulting store is prepared once and treated exclusively during a finite
lease; immutable content identity alone does not enforce filesystem immutability.

## Loading and runtime prerequisites matter

Calling `P/profile.load` is not a lightweight source loader. Lines 156 onward
require isolated supported Windows Python, all selected payload/native helper
pins/census, and `NativeInstallation.open` with both runtime attachments. It
imports admission support and verifies native files even when no proof is run.
The public investigator build route also builds native support before producing
P. Thus documenting lower calls after `profile.load` would not make an install
for a storage-only operator independent of Lean/native artifacts.

An existing cheaper bootstrap pattern is selected-export `export.py:setup,
load_codecs`: `run.bind_support` pins launcher metadata, supervisor and Python
runtime support, then seven explicitly pinned pure codecs plus inventory are
loaded. This does not call `profile.load`, open an owner or validate Lean binaries.
It still requires approved executable Python sources and the named package
metadata/source files; it is not a generic safe import of an untrusted package.

A rehost companion can select this pattern but must pin its larger actual source
closure: preview/evidence/manifest codecs, formal_query, discovery/index helpers,
Provider and ordinary_acquisition. The latter imports clients, which imports
custody.module_store even when that other role is unused. Lazy route modules also
need explicit handling. Do not claim the seven-codec loader alone serves HTTP.
Sources can be supplied from the current distribution without executing a Lean
compiler, but an independently usable pure-data source selection/guide is missing.
Reuse the existing Job supervisor; do not add a new process-control framework.

## Minimum contract, not implementation permission

1. Explicitly approve one exact bundle manifest and the complete disclosure set,
   including whole groups, imported dependencies and sibling declarations. Select
   bounded advertised targets separately; indexing targets is not a custody ACL.
2. Read manifest/exact units through existing bounded codecs. `read_manifest`
   and `validate_batch` at `P/reference/baseline_bundle.py:221-286` establish
   syntax/identity/censuses, not dependency closure. Accumulate caps across all
   batches, outputs, previews and index insertions under one original allowance.
3. If claiming a closed-basis handoff, check exact name/ID import resolution and
   acyclic unit closure against the pinned basis inventory before READY. Otherwise
   explicitly report closure unasserted; a missing later dependency is unavailable
   data and receiver refusal, never accepted mathematics. Receiver-relative
   custody-return bundles must not be silently promoted into closed bundles.
4. Malformed data or exhausted preparation quota yields no service readiness;
   preserve partial fresh output without resuming/overwriting or claiming rollback.
   Structurally valid false mathematics may remain inert; no CHECKED label.
5. Serve only the explicitly prepared stores, without concurrent external writers.
   Retain selected per-read content checks, fixed lease/cleanup reserve, TLS policy,
   attempt/reply/storage budgets and clean-closure checks. Remote source/native
   files are not imported. Requests cannot mutate stores or trigger replication.
6. Report prepared bytes/index scope and all preparation/lease costs separately
   from mathematical checking. The receiving owner's existing independent check
   remains mandatory for mathematical use; mirrors do not extend its trust.

This is a missing public composition boundary, not a new mathematical protocol.
Source evidence supports one minimal companion decision; it does not establish
runtime compatibility or a speedup. No harness, service, automatic replication,
daemon, package rebuild or implementation has been selected by this note.
