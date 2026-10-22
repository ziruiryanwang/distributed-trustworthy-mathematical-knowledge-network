# Managed Node storage: smallest coherent pre-schema integration design

2026-10-21, core_release. **Design only; not implemented or adopted.** Root
selected this note after the storage helper review. No Node/Python execution,
database/probe/build, private key read, runtime sweep, Git change or modification
of installed sources occurred. Reuse contract246bafdf and runtimee36470bb; there
is no new pager theory or saturation experiment.

The preceding author-note wording is corrected at
MANAGED-STORAGE-GATE-SOURCE.md,7860 bytes,
SHA-256 `36766bb26d3b4e2837cff72e32d1d79d3dff7ef46f12e397c9628f9b2cb53f91`.
Helper3b535a33 is unchanged and independently reviewed4e7f38cf.

## Decision: fresh Node database, not a new state-recovery protocol

Use **two fresh source successors at existing logical names**:

- `software/v5/managed_storage/portable/location/intent.mjs`, replacing logical
  `portable/location/intent.mjs`.
- `software/v5/managed_storage/portable/location/maintained_roles.mjs`,
  replacing logical `portable/location/maintained_roles.mjs`.

The first overrides only database open/configuration, preserving the inherited
quota-store behavior. The second bounds the identity writes and performs the
fixed state preflight. No extra source-map filename, new role schema, changed
DHT protocol, Node rebuild, package change or base-overlay rewrite is needed.

Apply the guarded fresh-database open unconditionally in this successor intent
store. Only the future separately bound managed-manager profile may claim the
whole-root envelope. Other callers receive the safer fresh Node database but
**no** automatic manager/slot/physical-envelope adoption.

This is smaller than a managed-only role-schema branch, which would propagate
through controller, service, advertisement and manager validation merely to
select a different open method. The actual public entry already enforces the
fresh-state precondition that makes the unconditional guard suitable.

## Exact dependency and launch chain

Basis is selected127 input33bd99d7. The combined observed release changes only
owner and placement service; this Node chain is the same. These are inspected
source identities, not guessed older namesakes:

```text
GenerationServices._start (40436584)
  -> AdoptedLocationRuntime + ServiceLocationProcess (eeb82d5d)
  -> node_entry_services.mjs (7efae4a2)
  -> services_composition.mjs (94341e6e)
       loadRuntime -> runtime.mjs (8beb9f5d)
         -> base/overlay/quota_store.mjs (7c6cbeea)
       createLocator -> role_composition.mjs (5502bd2e)
         -> MaintainedLocator in maintained_roles.mjs (128a5bd4)
           -> intentStoreClass in intent.mjs (220bff26)
             -> subclass of runtime.quota.QuotaDatastore
```

The base quota store is9487 bytes, exact SHA-256
`7c6cbeea0c685ec81f8d263cf84c6b8b9dd2c1f09e9f2f0f063196abc929eca4`,
directly corroborated against the selected installation and its base manifest.
It imports node:sqlite DatabaseSync; datastore-core BaseDatastore (index exports
base.js); interface-datastore Key (index imports key.js); and interface-store
NotFoundError (index reexports errors.js). Their entire transitive overlay
closure remains covered by the retained base manifest, not only those exports.

Base manifest SHA is
`a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed`.
Its Node executable row is92279112 bytes,
`b3094d0b49f9ad602262a9921551737bb97637c05dd357a06ae98188d7290aa3`.
The already settled runtime is Node24.16.0/SQLite3.53.0. Version/source-id strings
alone are not adoption; the existing source/runtime binding remains substantive:

- Parent AdoptedLocationRuntime.verify checks the exact manifest and its5896
  overlay/Node files before launch and again after close, plus selected sources.
- ServiceLocationProcess verifies the five role pins before/after, preserves
  private-pipe ownership, exact limits and original deadlines.
- Entry services requires exact process.execPath, empty execArgv, canonical
  source/install/workspace paths and config/source-map hashes. Its existing
  resolver hook confines file imports to the14 selected source names and
  manifest overlay. Adding node:sqlite to the fresh intent source needs no new
  file import; built-ins are already admitted.
- Runtime loader supplies the fixed quota module from that exact overlay.
  This is not a caller-selected arbitrary database class at the public boundary.

The two new files fit existing names: SOURCE_NAMES9 plus ROLE_NAMES5 and
distribution LOCATION_SOURCES14 are unchanged. Fresh distribution source-map
pins and manifest change through the usual root build; used old files do not.

## Why fresh-only is a genuine simplification

The selected composer first durably charges a new run and checks the generation
marker, then requires a fresh run path and assigns fresh run/location-state and
run/location-channel. The Python controller checks state freshness in its
constructor and again before spawning. Entry services independently calls
freshWorkspacePath for state and always calls locator.start({create:true}).

Therefore normal manager continuation preserves the six Python custody stores
but **never reopens a prior Node run database**. A failed Node start consumes
its original charged run; the next authorized run uses another charged path.
We should exploit this existing rule rather than design Node hot-journal
recovery that the product does not use.

Unconditional fresh-only intent open will refuse an existing metadata.sqlite
or journal, including one produced by this new source. A lower-level direct
MaintainedLocator.start({create:false}) with an existing metadata database is
therefore not supported by the new open path. The current public entry does
not expose that operation. Frozen installations retain their old behavior.
If a genuine later requirement needs Node reopen, it requires a separately
reviewed authenticated lineage/recovery design; no fallback to super.open.

## Before any writable SQLite open

The proposed ordering is explicit:

1. Preserve parent source/runtime adoption, generation binding, charged run
   and fresh paths. In the managed-manager integration, strict five-field Node
   metadata is already validated by the helper before allocation. Other callers
   may retain existing missing/null defaults in the unchanged quota constructor;
   its normalized finite limits still determine this connection's guard.
2. In the fresh maintained_roles path, require ordinary canonical state ancestors
   and absent state, then create only the charged state directory. Generate the
   Ed25519 key and serialize **both** private-key bytes and canonical adoption
   bytes into local buffers. Require each to be a byte buffer with
   `0 < byteLength <= 1024` before either writeFile. Only then write identity.key
   with wx/mode0600 and adopted.json with wx. Keep the existing state schema and
   config_sha256; no new caller-adoption boolean is needed.
3. Before constructing the datastore connection, check the state directory's
   fixed entries: only the two bounded regular identity/adoption files may
   exist. Use a bounded directory iterator; reject the first unknown/extra entry,
   symlink/reparse alias or incompatible kind. Check realpath/canonical ancestors
   and file bounds; where supported require ordinary single-link files.
   Revalidate the adoption record against the exact local config hash.
4. Inside the override, immediately before new DatabaseSync, require canonical
   metadata.sqlite beneath that checked state directory and absence of
   metadata.sqlite itself, its journal, WAL and SHM. Unknown files are refusal,
   never deleted. A bounded fixed-name census must not scan mathematical content.
5. Only then construct DatabaseSync and configure the connection before BEGIN,
   CREATE, INSERT, index creation or any other schema write.

These checks establish fresh lineage under the stated trusted-owner/exclusive-
writer premise, not an atomic sandbox against a same-user filesystem attacker.
DatabaseSync does not offer an O_EXCL database-open guarantee; ordinary local
concurrent replacement remains outside this profile. Existing parent ownership
and fresh paths do not magically prove a hostile-filesystem theorem.

A previous run's hot journal is never opened by this route. It stays charged
and available for the existing fail-closed reclamation decision. This does not
remove the separate same-profile hot-journal prerequisites for the manager and
six continuing Python databases; their guards must authenticate before writable
open, not after recovery has already happened.

## Guarded open while preserving base schema and counters

Do not call super.open and then apply PRAGMAs: the inspected base open has already
created tables and committed. In the fresh intent successor, retain the existing
constructor and inherited methods, but override open with a small reviewed copy
of the base initialization/census block and insert the guard before its first
BEGIN EXCLUSIVE.

The guard must establish/read back page_size4096, auto_vacuumNONE,
journal_modeDELETE, synchronousFULL, effective MEMORY temp under the adopted
TEMP_STORE=1 build, exact max_page_count=this.limits.pages and normal cache
spilling. Preserve busy_timeout250 and locking_modeEXCLUSIVE. No VACUUM, ATTACH,
backup, MEMORY main journal or VFS replacement. Configure all of this on the
actual connection, not on an earlier throwaway connection.

Preserve exactly:

- config(id,schema,limits), kv(k,v,sz,provider_group), provider_groups index and
  totals(id,entries,bytes), including existing primary/check constraints.
- DMKN_QUOTA_STORE_V1 and JSON.stringify(this.limits), whose constructor ordering
  and fixed /dmknv5/provider prefix remain unchanged.
- Empty-store adoption condition, config equality, totals-vs-SQL census,
  per-row _value/size/provider-group checks, entry/byte/provider-group caps.
- COMMIT before assigning this.db; failure rollback attempt then close/rethrow.
- Existing intent-store orphan-self-hint scan after successful base-equivalent
  initialization, and its close-on-error behavior.
- Inherited _key/_value/_put/_delete/_transaction, batch bounds, indexed keyset
  iteration, report/close and intent authorization/atomicity methods.

Freshness makes many reopening branches unreachable, but retaining the exact
base validation block reduces semantic drift and preserves its checked invariant.
This is a local subclass override, not a mutation of QuotaDatastore.prototype,
DatabaseSync, module globals or the fixed runtime import table.

## Integration and compatibility boundary

The Node-only delta is two source files. Root's separately selected coherent
managed integration still needs fresh manager/profile identity, pre-write
registry/generation gates, seven Python connection guards, one-byte locks and
continuing-store file/lineage checks. The package must select these together
before claiming the full managed data-stream bound. Source/helper success alone
does not flip physical_envelope_adopted or certify the runtime/VFS premise.

No old database or manager is automatically migrated. Ordinary readers retain
V1/V2 role configuration, routing and transport semantics, while their fresh
Node connection gains pre-schema safeguards without a whole-root claim.
Failed starts keep all original charges and partial files. Existing cleanup
state/counters and original service/process limits are not reset.

## Minimal next evidence, only after source selection

Review exact base-to-override delta and two-buffer ordering first. Then, if root
selects controls, use tiny changed-boundary cases: wrong/extra pre-open files
refuse before DatabaseSync; bad pragma readback refuses before first DDL;
oversized identity/adoption buffers refuse before either write; successful
guard preserves base schema/census order. These do not need a real network,
full lifecycle, new proof campaign or disk-filling experiment. Actual startup
can be integrated with the next already-needed managed operation, not a
duplicated broad service campaign.

