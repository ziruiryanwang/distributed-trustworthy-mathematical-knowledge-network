# Managed Node pre-schema storage: source handoff

2026-10-21, core_release. **Source authored; independent review pending.**
Root selected only two successors after design0fc3dfa2. No Node/Python import,
runtime/probe/test/build, database or private-key access, Git change or old-source
edit occurred.

## Exact files

| New source below software/v5/managed_storage/portable/location | Bytes | SHA-256 |
|---|---:|---|
| intent.mjs |8680|6c30e8793f737f0512e3e7e9d785d1311cafa35116784f4f8b3dda5c1a75fa29|
| maintained_roles.mjs |29824|d69d0b123e52f5cfbf4c2eef2e2d2dfecf9b9b11c9ddfabc4c5e37499e1a12e0|

The exact predecessors are selected body_location intent220bff26 and
maintained_roles128a5bd4. Base open is taken from the selected installed
base/overlay/quota_store.mjs,9487 bytes,
SHA7c6cbeea0c685ec81f8d263cf84c6b8b9dd2c1f09e9f2f0f063196abc929eca4,
under retained base manifesta93714ec. They all remain unchanged.

## Delta and source identity checks

Intent adds built-in imports, two local guards, a copied base initialization
method named _openFreshProfile, and changes only the original open wrapper's
first call from super.open to that method. The wrapper's orphan-intent scan and
close-on-error remain byte-identical. The existing constructor, provider prefix,
intent authorization methods and inherited base methods are unchanged.

Read-only string inverse checks establish:

- Removing the new imports/guards/private open method and restoring that one
  call recovers the exact predecessor intent bytes, including EOF.
- Removing freshMetadata and configureFreshDatabase calls, restoring the original
  pre-open stat block, method name and indentation recovers the exact base open
  method bytes. Thus base SQL, configuration binding, counters, census,
  transaction and error cleanup are not an approximate reimplementation.
- Reversing the one identity/adoption block change recovers exact predecessor
  maintained_roles bytes.

These are source equality checks, not JavaScript parsing or executed tests.

## Before writable connection and before schema

freshMetadata requires the fixed metadata.sqlite basename and canonical absolute
path. It checks ordinary directory ancestors with lstat/realpath. A bounded
directory iterator allows exactly identity.key and adopted.json; each must be a
regular non-symlink single-link file with realpath identity and0<size<=1024.
The first unknown/extra entry refuses, so directory enumeration stores at most
two names and does not scan mathematical payloads.

It then explicitly requires absence of metadata.sqlite and its -journal/-wal/
-shm paths. There is no deletion, repair or recovery path. These checks precede
new DatabaseSync. Existing same-profile databases/journals also refuse.

configureFreshDatabase runs on that actual new connection before the copied
base's first BEGIN EXCLUSIVE or CREATE. It requires zero initial pages,
the selected build's TEMP_STORE=1 and a256..65536 integer cap, then sets/reads:

- page_size4096 and auto_vacuumNONE;
- DELETE main journal and FULL synchronous mode;
- MEMORY temporary storage, positive cache spilling and exact max_page_count.

The original base configuration then repeats its unchanged page/DELETE/FULL/
page-cap setup and preserves busy_timeout250/locking_modeEXCLUSIVE before DDL.
Those repetitions do not undo MEMORY temp or auto_vacuumNONE. No VACUUM,
ATTACH, MEMORY main journal, global monkey patch, VFS replacement or
throwaway-connection configuration is used.

On configuration/SQL/census failure the copied base rollback attempt, connection
close and rethrow are unchanged; this.db is assigned only after COMMIT.
There is no super.open call. The original post-open orphan-intent check and
close-on-error still follow. Future operations inherit the same atomic quota,
key/value, batch, indexed iteration and close implementations.

## Identity and lineage ordering

The maintained_roles fresh path serializes both identityRaw and adoptionRaw
before either write, requires each to be a nonempty Uint8Array of at most1024
bytes, then preserves identity wx/mode0600 and adoption wx writes.
If either serialization/bound fails, neither file is written. A later write
failure keeps its charged partial run; no cleanup or allowance refund is added.

The actual bounded adoption file is now read and matched to the unchanged
DMKN_V5_LOCATION_STATE_V1 schema and exact this.configHash on both fresh and
non-fresh branches, before store construction/open. Non-fresh key decoding
still follows marker validation. No private key is emitted in diagnostics.

This authenticates the expected local marker under trusted-owner source/runtime
and exclusive-writer premises, not merely a caller's profile boolean. The store's
path/census guard is separate from marker content validation at this selected
caller. It is not an atomic defense against another same-user process replacing
files between checks and SQLite open; that adversary remains outside the settled
managed-storage profile.

## Scope and compatibility

Both files retain their existing logical map names. V1/V2 role schemas, the14
source filenames, base manifest/runtime, imports selected from the overlay and
all routing/transport/checker behavior stay unchanged. No new package dependency,
persistent marker, log, directory or file extends the settled storage grammar.

The existing public entry services always creates a fresh state directory after
a newly charged run. It therefore uses this guarded path without Node database
migration. A direct lower-level create:false call with an existing metadata DB
now refuses. No claim is made that such old-state reopening remains supported;
frozen installations are unchanged. Hot journals remain preserved and charged.

The unchanged quota constructor still normalizes missing/null limits for other
non-managed callers. Its normalized page/value/entry/provider caps remain
bounded. The new managed-manager profile independently requires all five explicit
fields before allocation. Receiving a guarded fresh connection alone is not
whole-root adoption or proof that a reservation covers all stores/runs.

No adoption flag is changed. Runtime/default-VFS correspondence, fresh manager
identity, all-R arithmetic, Python continuing-store lineage and each writer's
bounds remain parts of root's coherent integration. These Node files alone
do not establish the complete managed envelope or a deployable release.

Independent review should focus on exact base preservation, absence/census
before DatabaseSync, profile before DDL and both buffers before either write.
Any later root-selected controls should target only these changed boundaries;
no broad network/proof/lifecycle rerun is needed merely for this source handoff.

