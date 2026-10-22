# Managed storage distribution: independent actual build audit

2026-10-22, storage_outcome_audit. **PASS_SELECTED_129_DIRECTORY_BUILD.**
Root reported session58636 terminal before this saved-output audit. The canonical
guard passed. No build/import/verifier rerun, full payload sweep, credential read,
state edit or Git mutation occurred. This is file-only installation evidence,
not actual managed-service integration or full-v5 acceptance.

Installation: `product-local/v5-distribution-managed-storage-01/Mathematical Commons v5`.
Evidence directory: `experiments/v5-local-checks/distribution-managed-storage-build-01`.
Selected input: `experiments/v5-local-checks/distribution-managed-storage-01-input.json`,
SHA-256 `a629df82718f6a9d0560cacbfdc459739c15a56a1f2a46dd87929a1db51c22a4`.

## Exact evidence and map

| Evidence | Bytes | SHA-256 |
|---|---:|---|
| Installed V5-RELEASE.json |2370856|`811d4a86dd6523a44435ca89a4d7a5eb0367ccca727cdc45a9e095f8f22446e2`|
| Original/saved selection |8538|`4df4b09b82c00e4ad70351eeb385b6d6a900fdaf70565b41c716400ee0246f54`|
| RESULT.json |2258|`ec09169be434f34f95efcc56184b4dbb2d00e694c046b80988b294f07d939fb2`|
| command/command.json |907|`928b2e9a4bf089ab40bf36251ce68f0785beb927a4e0b88abac46ab2f37ecdc8`|
| command/stdout.txt |356|`100588badfd41644f0b4a3f4cf7d45b0d28a838260c658e5a58a4df8a3516fdb`|
| command/stderr.txt |0|`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`|

These hashes and the predecessor inpute0f0dc5d/release7381fa03 were checked.
Exact comparison establishes129 SDK entries:115 complete predecessor input rows
(original path, length and digest) unchanged,12 replaced, two added, none removed.
All non-SDK input fields and field names are unchanged. Every installed SDK
manifest mapping is exactly `sdk/<logical>` with the selected length/digest.
All108 preparation source rows equal the complete selected v5 Python subset,
with no duplicate, missing or additional row.

The14 selected originals and their installed copies were independently hashed:

| Logical path (v5/ unless portable/) | Previous bytes | New bytes | Selected SHA prefix |
|---|---:|---:|---|
| client/managed_owner.py |31626|33789|6991ac58|
| client/serve_generations.py |8896|9369|e12f3899|
| client/workspace_evidence.py |51539|51821|d94e3825|
| custody/module_store.py |10535|10754|580515e4|
| evidence_network/custody.py |8166|8385|4264841e|
| discovery/discovery_store.py |19886|20113|7f3c884b|
| placement/ledger.py |12537|12758|59f87b93|
| placement/advertisement.py |23256|23475|13b0ef1a|
| placement/lifecycle.py |38399|39828|0fa3dcc4|
| placement/sessions.py |20233|20462|6e07010c|
| portable/location/intent.mjs |2899|8680|6c30e879|
| portable/location/maintained_roles.mjs |29168|29824|d69d0b12|
| placement/storage_profile.py |added|9331|3b535a33|
| placement/storage_paths.py |added|7490|e1bcba27|

Full hashes are retained in the exact input and manifest, and match the reviewed
selector's14 pins. The test-only protocol alias is not selected; its product row
remains the original unchanged source. No control script enters the product.

Manifest-only comparison finds9860 unchanged payload rows, exactly the12 changed
SDK payloads and two additions above, with no removed payload. Total9874 payload
files /842723052 bytes matches the sole saved builder result, an increase of
28939 bytes. Base roles, assets, Lean support, other manifest fields and all
non-source preparation fields are unchanged. The new manifest binds the exact
input and unchanged base manifesta93714ec.

## Reused verification and closure

Runner44a7bf1b and buildereb1348f6 originals/snapshots match selection; the snapshot
contains exactly two files. The installed builder also matches. The29 runtime
rows are the28 identical predecessor rows plus the new input, replacing only the
old input row. The inspected runner verifies these pins before/after execution;
no extra runtime-tree sweep was conducted here.

The unchanged builder's actual path copies with input/target hashes, saves the
manifest, then runs `verify_release(..., full=True)` before returning success.
That verification checks manifest, exact on-disk census, every payload length/
hash and the base-role projection. Reuse its saved terminal
`DIRECTORY_CREATED_AND_EXACTLY_VERIFIED` plus the adopted predecessor build
audit029bf860; do not repeat the842MB sweep. Stdout's installation, manifest,
counts and mathematical_acceptance=false match the independently compared map.

Selection, command and result agree on canonical cwd, isolated `-I -S -B`, exact
snapshot builder/input/hash/output and120CPU/600wall/128MiB/two active processes,
with1MiB per log. Status is `COMMAND_EXITED_ZERO_AND_CLOSED`, exit0, direct child
reaped, final active0, Job closed, no cleanup errors, no requested termination
and terminated_processes0. Cumulative total_processes is2. Stderr is empty.

Job CPU31.484375 seconds (15.515625 user +15.96875 kernel), wrapper0.9375:
**32.421875 known CPU seconds**. Nested supervision0.65625 is already inside
wrapper CPU and is not added again. Outer wall222.1359027000144 seconds;
command-through-cleanup222.0739254001528; peak Job private commit56541184 bytes.
Logs356/0 bytes and all observations remain within the selected envelope.

Root may adopt this exact129/108 candidate with the separate actual controls
audit9e3a0ff3 before a separately selected installed operation. This result does
not prove manager/worker runtime wiring, storage-envelope premises, networking,
mathematical acceptance, independent hosting or final-v5 readiness. Old
installations and all used sources, inputs, selections and outputs stay frozen.
