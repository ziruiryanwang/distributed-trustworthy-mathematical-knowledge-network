# Managed storage owner, paths and composer source review

2026-10-21. Independent reviewer: support_screen. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Disposition

**PASS_SOURCE_BOUNDARIES_AND_OWNER_PIN_CLOSURE.** No concrete defect
was found in the reviewed owner digest propagation, fixed-path metadata gates,
composer ordering, or their targeted manager/supervisor/Node integration.
This is source reasoning, not import, runtime, build, installed adoption or
physical-storage qualification.

Root completed the initially pending owner PINS rebinding before this review
was sealed. All16 explicit pins match their selected source files. Replacing
only the final PINS block in memory with the prior block reproduces the exact
previously reviewed owner hash `ef1544aa2ca90bc613c31b868cda228978ac44b33e53d37df44ba9be1af3b67a`;
there is no additional executable-code delta in that final update. The final
owner hash is in the table below. The known pending closure was not a newly
discovered defect, and is now closed at the source level.

Root still owns selection/authentication of the exact129-entry SDK map and
130-entry owner snapshot and any finite changed-boundary launch. Root reports
12 replacements,115 unchanged predecessor SDK rows and two new helpers, with
108 Python prep entries; the not-yet-sealed selector is not audited here.
No launch, test, build or installed adoption is authorized by this note.

## Exact source identity

Paths in this table are relative to `software/v5/managed_storage/`.

| Source | Bytes | SHA-256 |
|---|---:|---|
| `placement/storage_paths.py` | 7490 | `e1bcba2730e432b4dfc428d9c56ebb2e5b7bc0f4d8a9bfa0751b8818557eb9da` |
| `client/managed_owner.py` | 33789 | `6991ac58310b0c3a6456f033bff7bccbb02dd1299c67716d805762e0dea69a0f` |
| `client/serve_generations.py` | 9369 | `e12f3899f28cab8a95a9b497a6a7f5148cdc537912bed3d357310e2c0d220a83` |
| `placement/lifecycle.py` | 39828 | `0fa3dcc4285aa4afc87dfda5741e5c68334f8c0398138c3f218351e705a1f427` |
| `placement/sessions.py` | 20462 | `6e07010c47b0e95abbb80125e838b759e2a4206bdc3cafa735e31c7015d1a63b` |
| `portable/location/intent.mjs` | 8680 | `6c30e8793f737f0512e3e7e9d785d1311cafa35116784f4f8b3dda5c1a75fa29` |
| `portable/location/maintained_roles.mjs` | 29824 | `d69d0b123e52f5cfbf4c2eef2e2d2dfecf9b9b11c9ddfabc4c5e37499e1a12e0` |
| `placement/storage_profile.py` | 9331 | `3b535a337c1731ead3b9930c7cbe1f7c340a17152bd8b57e32981552ec061c90` |

The first three files are the primary assignment. The next four received a
targeted integration challenge in this same review. The final helper's settled
conditional arithmetic/pre-schema contract was reused, not independently
requalified. Root supplied the stable manager/Node pins and they matched the
read-only source hashes.

Authoritative predecessor navigation is
`experiments/v5-local-checks/distribution-managed-observed-01-input.json`,
SHA-256 `e0f0dc5d63dee0d088b8edd9e61d9a1d1bebbe31d3dde76b53887d1c901f7201`.
The owner was compared with the observed-owner source31626B/
`1c022737e4d51a25d873e6fd255cd87ee8427f21d7455f78b29d4b2e4d133503`;
composer with8896B/
`404365849dd0e41860ba8ccda01a5b064d028241a2d8b0063d76936fcd306687`.
Lifecycle/sessions predecessors are `bec62143`/`b4cfab61`; Node intent/roles
predecessors are `220bff26`/`128a5bd4`, resolved through the same map. Read-only
line comparisons and direct source inspection identify the intended storage
additions; prior acceptance, closure and mathematical logic is not replaced.

## Owner binding and propagation

`_bindings` retains the ordinary boot/context/plan checks, fixed launch origin,
adopted release hash and fixed base-runtime manifest. It requires129 logical
SDK names, the exact `sdk/` mapping, and exact equality of the non-owner plan
rows with the complete selected release map. The sole owner snapshot is the
selected `v5/client/managed_owner.py` row, for130 total source entries.

The unchanged launch `read_plan` validates canonical logical names, case-fold
uniqueness, exact `{bytes,sha256}` row shape, per-file/aggregate bounds, and the
portable closure. `_bindings` then verifies every relocated source's bytes
and digest. Thus the selected map used below is not a set of unchecked names
or only the16 explicit PINS. Missing/malformed release rows refuse;
there is no fallback map.

The writer identity is reconstructed with domain
`DMKN-V5-MANAGED-STORAGE-WRITER-V1` over `SP.PROFILE`, the fixed
`L.MANIFEST_SHA`, and the complete logical-name to `{bytes,sha256}` SDK map.
No relocated disk paths enter this digest. It deliberately changes with any
selected SDK change. The requested manager configuration must match this
derived identity; reading a user configuration hash alone does not adopt it.

The derived value is an explicit argument through `main`, `_admin`,
`_supervise`, `_worker` and `_open`. `_open` supplies it as
`writer_profile_sha256` to `ManagedGenerations.open`. The worker independently
reconstructs the same binding from its own authenticated snapshot and exact
parent-plan derivation. Its composer runtime receives that same value.
The additional report field is observational, not an authority.

The supervisor `_Launch` copies `manager._writer_profile`, separately from
the copied configuration; `_open_launch` supplies it to every supervisor
registry reopen. Existing exact-launch/session checks remain. Thus neither
parent bind nor final quiescence recovery silently reopens using only the
persistent configuration's assertion.

Code identity is not proof that arbitrary adopted code obeys the profile.
The authenticated selected implementation, supported runtime/default VFS,
private ordinary paths and absence of concurrent writers/restores remain
explicit premises. Direct calls to manager/composer APIs by arbitrary Python
code do not become an independent security boundary.

## Metadata gates and import dependency

`storage_paths` imports the pure feature/profile helpers at module scope.
Its access to `discovery_store.ordinary` is lazy inside `_ordinary`, avoiding
an eager cycle when `discovery_store` imports SP/SF before defining
`ordinary`. No storage gate executes at import time. This is a source-level
dependency argument; imports were not executed.

The underlying `ordinary` checks canonical paths, ancestor/target links and
Windows reparse attributes. `_file` further requires a regular file with
exactly one link, then an exact integer length inside the allowed range.
Unknown directories are rejected before traversal. None of these checks
defeats a hostile concurrent rename, handle substitution, restore or writer;
that adversary is outside the adopted private-path premise.

`preopen_lock` distinguishes absent fresh locks from exactly-one-byte enrolled
locks. `preopen_database` rejects fresh sidecars; on reopen it bounds both
main and optional rollback journal before a writable connection is possible.
WAL/SHM are rejected, including dangling lexical entries. Zero-length main or
journal files may represent interrupted managed writes and are not treated
as proof of a valid database; the connection/schema checks still decide that.
These routines themselves perform no database open, recovery, repair or write.

The registry gate permits only manager marker, lock, registry database,
optional rollback journal and exactly the two slot directories. All except
the journal must exist. Bounded set membership stops on an unknown or
duplicate entry. It checks exact marker size/content, lock, ordinary slot
directories and main/journal bounds. It does not recursively inspect slot
contents: those do not participate in registry recovery, and generation
configuration/identity comes from the authenticated registry lineage.

The generation scan has an explicit grammar for six persistent databases,
their optional journals, generation marker, workspace lock, empty operations,
and only the already charged run numbers. Each run permits one Node database
and journal, two state files capped1024B each and two channel files capped
16384B each. For r charged runs the grammar contains14+6r files and6+3r
directories including the generation root. Traversal observes at most
19+9r descendant entries. The reported20+9r possible entries includes that
root, matching the shared arithmetic convention.

The scan charges/checks the guard on directory/entry work and during run-list
construction, and rejects unknown names before descending. Every allowed
file has the exact selected bound; main files use4096*pages and journals
reuse `SP.database_envelope`. It intentionally does not require every allowed
file or directory to exist. Missing objects remain missing; actual creation
or reopen prerequisites decide what is required. No unknown path is adopted
because a census is incomplete.

## Ordering, partial states and reclamation

The changed manager schema requires `storage_profile` and writer digest.
`open` validates the independent digest and calls the complete registry/owner
reservation calculation before root mkdir, lock allocation or connection.
On reopen, exact registry marker/layout/main/journal validation is before
append-mode lock access and before `sqlite3.connect` can perform recovery.
The connection guard is the first configuration operation after connect,
before old pragmas, DDL, schema reads that can trigger later effects, or
transactions. Failure closes held resources through the inherited cleanup.
Old schema/marker roots are not migrated.

Generation allocation calls the full configured envelope before entering the
sequence/PROVISIONING reservation transaction. `_records` repeats the storage
calculation on retained rows. The calculation charges every permitted run,
not just occupied files or the currently active run. All five Node metadata
limits must be explicit, bounded, nonnull integers at this boundary.

The composer checks manager ownership and writer identity at construction
and use. `start_slot` durably reserves/increments the run before `_start`.
`_start` checks the exact generation marker, then performs the metadata scan,
and only then creates the fresh run directory or opens the workspace stores.
A scan refusal therefore leaves a charged run and takes the inherited
failure/cleanup path; it does not allocate a replacement run or claim CLOSED.
The unchanged strict service report consumer remains the closure authority.

PROVISIONING is not a create/reopen ambiguity: `reserve_run` still requires
zero prior runs and no existing workspace. A partially created workspace
does not qualify for provisioning recreation. Failures after the durable
charge preserve occupied sequence/slot/run state. Incomplete manager creation
without its required marker/layout refuses ordinary reopen; no repair or
unrecorded adoption is introduced.

The new generation preopen scan is used only on service startup, not as a
universal all-files-present requirement on registry status or reclamation.
An enrolled RECLAIMING generation may therefore have missing files or its
marker/root already removed by a prepaid window. Existing `R.validate`,
census, reconciliation and exact absence-before-free logic remain responsible
for that operation. It does not reopen the deleted generation's SQLite files.
The new registry gate checks only the surviving manager/slot boundary, so it
does not prevent resuming a legitimate partial reclamation. Unknown closure,
retention gates and charged failed windows are not weakened.

## Targeted Node integration

The selected `node_entry_services.mjs` calls `locator.start({create:true})`.
The Python service controller already requires fresh state/channel paths in
the charged run, and bounds both serialized channel buffers by
`FRAME_BYTES=16384` before creating/writing the channel directory.

`maintained_roles` now constructs both identity/adoption buffers and checks
both are nonempty byte arrays of at most1024B before either write. Exclusive
creation is retained. It authenticates the resulting adoption marker before
constructing/opening the datastore. Failed partial writes remain in the
charged run; the managed public path does not reuse them on another run.

`intent` first checks the absolute canonical metadata filename and ordinary
ancestors, then a bounded exact two-file state directory: `identity.key` and
`adopted.json`, each ordinary, one-link, nonempty and at most1024B. It refuses
any existing metadata main, rollback journal, WAL or SHM before
`new DatabaseSync`. There is no Node hot-journal reopen lane to authenticate.
The distinct direct API possibility of a state marker/key with no database
does not add managed run reuse: the selected entry still requires fresh state.

The fresh Node connection requires page_count0 and TEMP_STORE=1, configures
P4096/auto_vacuumNONE/DELETE/FULL/tempMEMORY/cache_spillON and the exact page
cap, and checks readbacks before the copied quota schema transaction.
Inspection against the fixed runtime `base/overlay/quota_store.mjs` confirms
the retained quota schema, counts, key/value/provider checks and transaction
shape. `_put`, intent revocation and the inherited quota methods remain the
selected mechanisms; no new network or mathematical acceptance path is added.
Failed connection setup closes the local connection before it is published
as `this.db`.

The quota constructor's inherited null/default behavior still exists for
direct nonmanaged callers. It cannot lower the managed admission bar:
SP rejects missing/null metadata fields before generation allocation, and
the composer supplies the retained exact configuration. This review does
not award a whole-root envelope to direct standalone Python or Node users.

## Independence, evidence and remaining limits

The six Python store successors were authored by this reviewer under a prior
disjoint assignment, recorded in `MANAGED-STORAGE-PYTHON-STORES-SOURCE.md`
(`2d657ed589a5ddcd0032118307ee7477336b72e38e304b9b6f74f3923fe3025e`).
They are not self-awarded an independent review here; root owns their review.
Their documented preopen/configuration interface was used only to trace the
composer boundary. The settled storage helper/theory reviews are likewise
not relabeled as fresh executed evidence.

Canonical guard passed on resumption. This task used source reads, metadata
hashes, read-only source comparisons and this assigned Markdown checkpoint
only. No product edits, imports, AST execution, tests, probes, builds, SQLite
access, credential reads, process launches for product work, deletion or Git
operations occurred. All used predecessors and sealed reviews are preserved.

Remaining integration work is root's exact fresh map/adoption/finite
changed-boundary selection. Unsupported runtimes may
refuse compile-option or pragma readbacks; no runtime compatibility result
was manufactured here. Apparent managed stream bounds are conditional on
the selected source/runtime/VFS/private-writer premises. Physical allocation,
free disk, external output directories, inherited installations, hostile local
writers, migration and full-v5 release qualification remain outside this pass.
