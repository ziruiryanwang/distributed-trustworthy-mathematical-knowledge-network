# Genuine terminal adapter: prospective source closure

## Current staging integration (supersedes the counts below)

2026-10-17 root read-only closure check after independent source review
TERMINAL-STAGING-REVIEW4ec3db28. Apply the predecessor removals/additions below,
then additionally include `v5/client/workspace_staged.py` and
`v5/transport/semantic_staging.py`. The result is100distinct entries:
78v5,21portable and one owner. All92retained predecessor entries still match
their original length/hash; no competing location namespace was introduced.

Current sources: assets19,634B/d16429325e109492b5d28173219e0328842080aa9f65ca30b8e078c24ca8efd3;
strategy35,673B/a29a0a73c162afdcafe8c99dc6f46634c5e67941a76b5f202d5379402d032157;
staged facade12,836B/bdd539d5f3fbc48d18215e25811178c5991e8475068156353e3cce7c1a97cf1a;
helper10,598B/1b58f247a4f03c393fe6e52fb22037d56449b183bbb63b2767ab1b344c523be2.
Inspector remains unchanged at8b779763. The78v5files total959,128bytes;
A issuer97pins/24,744,888bytes; native issuer79pins/2,672,280bytes.
The unchanged runtime counts/lengths below supply those sums. This check read
source metadata/hashes only, not imported/executed code or a launch selection.

The full100-entry launch map must still bind final actual sources, real receipt,
ports and finite resources. No receipt exists and no dummy is selected. Read
TERMINAL-STAGING-INTEGRATION for current stage-before-admit ordering and exact
packet-size preflight; the older source list/counts below are retained history.

## Earlier non-staging closure record

2026-10-17. Source-only analysis under TERMINAL-ADAPTER-SELECTION. This is an
explicit allowlist for a future root-selected genuine-receipt launch, not an
executable plan or execution clearance. No imports, tests, builds, proof work,
runtime-tree hashing or Git mutations were performed for this checkpoint.

## Construction and owner identity

Use the frozen `experiments/v5-local-checks/evidence-client-controls-01-plan.json`
(SHA-256 `ae2722995cd86b1bbfe11ee113f18fc93a4e0d70289a88e8d9f7ea6bc69b88f1`)
as the source-list predecessor, not as runtime authorization. Remove:

- `owner/evidence_control_owner.py`
- `v5/client/test_workspace_evidence.py`
- `v5/client/test_workspace_mixed.py`

Add the six entries below, preserving all other predecessor source entries:

- `owner/terminal_strategy.py`
- `v5/client/actual_assets_atomic.py`
- `v5/client/terminal_assets.py`
- `v5/client/terminal_inspection.py`
- `v5/client/workspace_resilient.py`
- `v5/transport/search_resilience.py`

The result is **98 distinct entries: 76 v5 files, 21 portable/location files,
and one owner entry**. Source roots remain `software/v5`,
`software/v5/portable_runtime`, and `software/v5/client`, respectively.
`owner_entry` is `terminal_strategy.py`. Do not also add it as
`v5/client/terminal_strategy.py`: the outer owner loader already pins it.
The portable map must exactly equal `launch.PORTABLE`; do not create a second
`v5/location` or `v5/portable_runtime` import namespace.

The strategy author confirms no further imports planned. Its provisional source
is 31,701 bytes, SHA-256
`5596241ead27a57a043606415f84d0abf098bf64c2a46c0a7a16d519a0923569`.
Assets' latest source is 19,562 bytes, SHA-256
`ac81eb61db88112619aea7ed90dc3645a98e1def368c75045622747a2768a445`;
this includes the inert selected-receipt `receipt_identity` field. These are
observations, not replacement for root's eventual final source pins. The genuine
A receipt does not yet exist and no dummy receipt can satisfy this gate.

## Issuer-pin bounds and actual dependencies

The retained authoring profile is
`experiments/v5-local-checks/delta-author-01-profile.json`: 21,137 bytes,
SHA-256 `f03b591c6e9e40346028c35b663d4d2c5daaf9a58ec6eb890810f96c6c984a4b`.
Its producer Python executable, Python DLL and runtime pins have **18 distinct
rows**, totaling **17,155,360 bytes**. Rebase their installed locations exactly
as the assets loader requires; do not substitute a different interpreter.

At the inspected source revision the 76 v5 files total 935,622 bytes. Thus:

| Issuer selection | Entries | Observed pinned bytes |
|---|---:|---:|
| Aggregate receipt issuer: v5 + Python18 + actual A host | 95 | 24,721,382 |
| Native mixed issuer: v5 + native checker | 77 | 2,648,774 |

Both satisfy the 128-entry/512MiB limits by a substantial margin. Source bytes
may change during unexecuted review; recompute exact final pins before launch.
Preparation's source list has 76 entries; its retained Lean runtime selection
has six rows totaling 212,510,976 bytes. No whole Lean-tree hash is necessary.

The 18 Python runtime paths, relative to installed `receiver/runtime/python/`,
are:

```text
python.exe
python314.dll
python3.dll
vcruntime140.dll
vcruntime140_1.dll
DLLs/_asyncio.pyd
DLLs/_ctypes.pyd
DLLs/_hashlib.pyd
DLLs/_overlapped.pyd
DLLs/_queue.pyd
DLLs/_socket.pyd
DLLs/_sqlite3.pyd
DLLs/_ssl.pyd
DLLs/libcrypto-3.dll
DLLs/libffi-8.dll
DLLs/libssl-3.dll
DLLs/select.pyd
DLLs/sqlite3.dll
```

The installed release manifest is
`product-local/v4-library-commons-02/commons-v4/RELEASE-MANIFEST.json`, SHA-256
`a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed`.
`client/boot.py` verifies the installed Python runtime and selected import
origins. The 18 issuer pins are not a claim of complete hermetic OS/DLL closure.

Important non-obvious edges:

- `authoring/worker.py` is a standalone, stdlib-only worker launched using
  pinned Python by atomic preparation. It invokes the pinned native frontend;
  it does not import project modules.
- `MixedOwnerPreparation` requires retained `mixed_claims/authoring.py` and
  `mixed_claims/imports.py` among source pins even though the atomic classes are
  selected. Both remain in this list.
- The function-local `delta/reprepare.py` import of
  `admission.bindings.journal` is covered.
- Production/admission dynamically load installed `operator/commons.py`,
  `receiver/helpers/domains.py`, and `receiver/helpers/run_stage.py`. These are
  pinned installed helpers, not extra v5 snapshot sources.
- Existing frontend/image binaries are asset pins. Lean build sources are not
  runtime imports. Ordinary author source/roots are immutable input pins.
- The retained module/I host is a preparation-constructor/supervision dependency,
  not authorization to verify I at either consumer. The selected real gate has
  two A checks, one author call and one native SECOND check, with no FIRST proof
  replay or consumer I checks.

## Complete source allowlist

```text
owner/terminal_strategy.py
portable/location/__init__.py
portable/location/available_descriptor.py
portable/location/composition.mjs
portable/location/controller.py
portable/location/controller_services.py
portable/location/framing.mjs
portable/location/intent.mjs
portable/location/ipc_wire.mjs
portable/location/maintained.mjs
portable/location/maintained_roles.mjs
portable/location/node_entry.mjs
portable/location/node_entry_roles.mjs
portable/location/node_entry_services.mjs
portable/location/observed_route.py
portable/location/protocol.mjs
portable/location/protocol.py
portable/location/role_composition.mjs
portable/location/runtime.mjs
portable/location/services_composition.mjs
portable/location/transport.mjs
portable/location/workflow.py
v5/admission/__init__.py
v5/admission/bindings.py
v5/admission/verifier.py
v5/aggregate_claims/__init__.py
v5/aggregate_claims/admission_binding.py
v5/aggregate_claims/aggregate_admission.py
v5/aggregate_claims/bindings.py
v5/authoring/__init__.py
v5/authoring/context.py
v5/authoring/imports.py
v5/authoring/source.py
v5/authoring/worker.py
v5/client/__init__.py
v5/client/actual_assets_atomic.py
v5/client/boot.py
v5/client/launch.py
v5/client/terminal_assets.py
v5/client/terminal_inspection.py
v5/client/workspace.py
v5/client/workspace_atomic.py
v5/client/workspace_evidence.py
v5/client/workspace_mixed.py
v5/client/workspace_resilient.py
v5/custody/module_store.py
v5/custody/receipt_store.py
v5/delta/__init__.py
v5/delta/custody.py
v5/delta/packet.py
v5/delta/receiver.py
v5/delta/reprepare.py
v5/delta/transport.py
v5/delta_claims/__init__.py
v5/delta_claims/claims.py
v5/delta_claims/receiver.py
v5/discovery/authenticated_index.py
v5/discovery/candidate_query.py
v5/discovery/discovery_query.py
v5/discovery/discovery_store.py
v5/discovery/formal_features.py
v5/discovery/module_export_adapter.py
v5/discovery/search_session.py
v5/discovery/summary_wire.py
v5/evidence_network/__init__.py
v5/evidence_network/custody.py
v5/evidence_network/packet.py
v5/evidence_network/transport.py
v5/frontier_network/__init__.py
v5/frontier_network/custody.py
v5/frontier_network/transport.py
v5/mixed_claims/__init__.py
v5/mixed_claims/authoring.py
v5/mixed_claims/authoring_atomic.py
v5/mixed_claims/imports.py
v5/mixed_claims/imports_atomic.py
v5/mixed_claims/packet.py
v5/mixed_claims/receiver.py
v5/mixed_network/__init__.py
v5/mixed_network/custody.py
v5/mixed_network/transport.py
v5/modules/__init__.py
v5/modules/codec.py
v5/modules/model.py
v5/modules/native_rows.py
v5/modules/receipt/__init__.py
v5/modules/receipt/witness.py
v5/modules/source_rows.py
v5/preparation/__init__.py
v5/preparation/owner.py
v5/production/__init__.py
v5/production/producer.py
v5/transport/clients.py
v5/transport/http_provider.py
v5/transport/http_provider_receipts.py
v5/transport/located_receipts.py
v5/transport/receipt_client.py
v5/transport/search_resilience.py
```

## Decision boundary

Root must separately select finalized source hashes, real receipt identity,
unused ports, finite allocations and the exact future launch. This checkpoint
closes the source-map/count question, not real A production, mathematical
admission, positive useful-growth cost, independent hosting or final v5 readiness.
