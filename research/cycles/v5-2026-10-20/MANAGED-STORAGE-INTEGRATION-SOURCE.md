# Managed storage integration: root source review and binding

2026-10-21, root. Source implementation only; no installed129 candidate or
storage runtime has run. The installed observed127 remains current. Public02
audit9c779911 is adopted separately; commit4ceb17f preserves that result and
the reviewed arithmetic helper. No repeated proof/search or RAM investigation.

## Actual integrated changes

Fresh manager schema is `DMKN_V5_TWO_GENERATION_MANAGER_STORAGE_V1`.
Its immutable config adds `storage_profile` and `writer_profile_sha256`.
The installed owner reconstructs the latter using
`F.digest("DMKN-V5-MANAGED-STORAGE-WRITER-V1", value)`, where value is exactly:

```text
storage_profile: SP.PROFILE
base_manifest_sha256: the existing fixed runtime manifest identity
sdk_sources: complete SDK logical-name -> {bytes, sha256} map
```

No source paths, changing operation paths or whole distribution manifest are
included. Relocation preserves identity; any SDK modification refuses an old
manager. The separately adopted distribution and authenticated boot authorize
the code selection. The digest is not a proof of arbitrary code correctness.
No circular self-hash constant is required: the complete map is read from the
release, after authenticating it and every snapshotted selected source.

Owner6991ac58 passes the reconstructed digest explicitly to every admin,
supervisor and worker manager open. Supervisor sessions6e07010c retains it in
the live _Launch and uses it during both direct registry reopen paths. Composer
e12f3899 compares it to the manager, then checks generation marker and the
bounded metadata grammar before creating the new run directory or opening
stores. The fresh manager marker transitively binds each generation identity.

Root's storage_paths e1bcba27 checks paths, one-byte locks, individual DB/journal
maxima, registry enrollment and the closed generation grammar. It opens no
database and writes no files. Ordinary-path import is lazy to avoid a cycle
with discovery_store. Missing generation files remain missing, so partial
prefixes are not silently repaired; actual create/reopen calls decide required
presence. The registry precheck does not traverse reclaiming/partial slots.
Only the selected generation's bounded local run layout is scanned, never
global mathematics or proof payloads. Operations must remain empty.

## Independent author deltas read by root

Root read all six store deltas and source note2d657ed5: exactly19 added lines,
no changed SQL/checking/resource logic. Each actual connect is preceded by the
shared path check and followed, inside cleanup protection, by the connection
guard before prior PRAGMAs/DDL. Workspace lock validation precedes append open.
The fresh manager/session diff and note84466e2e are also read: registry bound
precedes mkdir; generation bound precedes sequence/PROVISIONING; stored records
repeat cap validation, and failures remain charged. All configured runs count.

Root read Node intent6c30e879 in full and the rolesd69d0b12 delta, plus source
notee816c257. The new run's metadata must be absent before DatabaseSync. Both
identity buffers are checked before either write; the actual adoption marker
is matched before store open. The fixed supported profile is configured before
the copied base schema/transaction. Original inherited quota operations and
intent logic remain. The Node lower-level old-store reopen path deliberately
refuses; ordinary managed entry already creates a fresh state per charged run.

Screen independently reviews root paths/owner/composer and the full integrated
writer boundary. This note is not a substitute for that review or execution.
Root's owner PINS now bind every changed writer/helper source, not the old ones.

## Map and assurance boundary

The prospective map has129 SDK entries:12 replacements,2 additions and115
unchanged rows from observed127. Python preparation entries become108. The
only additions are placement/storage_profile.py and placement/storage_paths.py;
Node logical filenames and all base runtime payloads remain unchanged. No test
harness or protocol fixture becomes an SDK module.

The gate covers all storage-bearing config caps and existing allocation role
checks, not a newly duplicated full semantic validator. Later non-storage
configuration refusal keeps its legitimate reservation. Preserve the distinction
between a bound on apparent default-data streams and physical disk allocation,
free space, OS/filesystem metadata, alternate streams or external report history.
All physical_envelope_adopted fields remain false. Exact runtime/source/VFS and
private no-other-writers/no-restores premises remain explicit.

Next select small actual SQLite/path and Node store controls only after their
source review. No network, key generation, proof generation, old-state migration
or broad lifecycle rerun is needed for these changed boundaries. Subsequent
directory build and public managed integration require distinct fresh selections.
