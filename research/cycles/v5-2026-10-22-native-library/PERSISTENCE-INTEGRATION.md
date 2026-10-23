# Concrete persistence integration for the ordinary Lean candidate

2026-10-22. Narrow source-only continuation by `lean_persistence_boundary`.
Read `software/v5/ordinary_lean/INTEGRATION.md`, `CheckedExtension.lean`, the
declaration format, the retained Lean4.34 module APIs, fixed seed receiver and
existing local lock/SQLite/trust primitives. No code or runtime selected here.

## Implement this seam, not a generic cache framework

Add one Lean worker wrapper and one small trusted Python library owner. The
worker performs checked admission and writes a local `.olean` chunk from its
**actual `CheckedBatch.added`**. The owner commits that chunk's exact bytes in a
protected local catalog. A later fresh process restores only the catalog's
selected chunk closure and checks another contribution. No generic snapshot
codec, daemon, replacement database, receipt, old exact-J identity or new proving
backend is required.

The prior source note's incremental-writer obligation is now concretely met by
the new `CheckedExtension.checkBatch` result:

```lean
structure CheckedBatch where
  environment : Lean.Environment
  added : Array Lean.ConstantInfo
  unitsChecked : Nat

def checkBatch (parent : Lean.Environment)
    (units : Array OrdinaryLean.DeclCodec.DecodedUnit)
    (limits : OrdinaryLean.CheckedExtension.Limits := {})
    : IO CheckedBatch
```

`added` is populated only by reading actual kernel records after the batch's
generated-inventory and bounded stage2 census checks. It includes generated
constructors/recursors/nested auxiliaries in the advertised, verified order.
It does not include old stage2 declarations from an earlier successful batch.

`CheckedBatch` itself currently has a public Lean constructor. It is therefore
internal plumbing, not an unforgeable capability. The new public worker path
must call `checkBatch` and the private writer in the same trusted function; it
must not accept a user-supplied `CheckedBatch`, `Environment`, `ConstantInfo` or
serialized `verified=true` report as authorization.

## Exact Lean signatures and data construction

The following proposed wrapper signatures use the existing Lean4.34 API types.
Names are prospective; this document does not claim they compile or exist yet.

```lean
namespace OrdinaryLean.LocalSnapshot

structure SavedChunk where
  moduleName : Lean.Name
  imports : Array Lean.Name
  names : Array Lean.Name
  unitsChecked : Nat
  -- The trusted controller hashes the resulting file after clean worker exit.

private def writeCheckedBatch
    (parentModule moduleName : Lean.Name)
    (path : System.FilePath)
    (checked : OrdinaryLean.CheckedExtension.CheckedBatch)
    : IO SavedChunk

def checkAndWriteChunk
    (parent : Lean.Environment)
    (parentModule moduleName : Lean.Name)
    (units : Array OrdinaryLean.DeclCodec.DecodedUnit)
    (path : System.FilePath)
    (limits : OrdinaryLean.CheckedExtension.Limits := {})
    : IO SavedChunk

def restoreLocal
    (rootModule : Lean.Name)
    (artifacts : Lean.NameMap Lean.ImportArtifacts)
    : IO Lean.Environment

end OrdinaryLean.LocalSnapshot
```

The process entry point is not a peer RPC exposing these raw arguments. A
trusted local controller supplies the protected import plan and new output path;
the worker obtains `parent` only from `restoreLocal` or the exact fixed-basis
initializer. The peer supplies only bounded inert mathematical declarations.
The ordinary API owns fresh process/operation grants and prohibits arbitrary
runtime module/plugin configuration.

Inside `checkAndWriteChunk`, decode the supplied inert units using the actual
parent names, call `checkBatch`, then pass that exact return to the private
writer. If callers already decoded units, maintain the same source ownership:
no higher-level public method accepts an independently constructed checked result.

The private writer uses this existing public Lean data structure:

```lean
let imports : Array Lean.Import := #[{
  module := parentModule
  importAll := false
  isExported := true
  isMeta := false
}]
let data : Lean.ModuleData := {
  isModule := false
  imports := imports
  constNames := checked.added.map (fun c => c.name)
  constants := checked.added
  extraConstNames := #[]
  entries := #[]
}
Lean.saveModuleData path moduleName data
```

`saveModuleData : FilePath -> Name -> ModuleData -> IO Unit` is already defined
at retained `Lean/Environment.lean:1792`. The module wrapper's name does not
rename the contained mathematical constants. All original binder names, universe
parameters, hints, native literals, proof values, inductive metadata and rules
in `checked.added` survive. There is no metadata regeneration from expected
peer records, no weakening of theorems to axioms, and no export of elaborator
extensions. Do not replace this with `writeModule checked.environment`: stage2
means since import, not since the previous successful commit.

Pre-write conditions: nonanonymous distinct module names; output fresh inside
the controller's reserved staging directory; checked quotient state true; added
names nonempty/distinct; exact selected parent binding. The latter is a controller
precondition, not something an arbitrary `Environment` object proves. The first
implementation has one parent root. Compatible multi-parent merging is not
needed for two independent consumers to extend the same parent; their branches
can coexist. A future merger must resolve name/definition conflicts explicitly.

### Restoration is a local operation, not mathematical admission

For every local chunk in the selected parent closure, build an `ImportArtifacts`
entry using the existing constructor:

```lean
Lean.ImportArtifacts.ofArrays #[#[exactProtectedOleanPath], #[]]
```

The outer array's second item is the empty IR list. The selected artifacts are
single legacy/non-`module` snapshots, so no `.olean.server`/`.olean.private`
parts are needed. This internal choice does not restrict the user's ordinary
source project's module syntax.

Then invoke the actual existing API:

```lean
Lean.importModules #[{ module := rootModule }] {} 0
  (plugins := #[]) (leakEnv := false) (loadExts := false)
  (level := .private) (arts := artifacts)
```

The controller must first establish all of these conditions:

- Every selected module comes from a committed local catalog record, with the
  same native profile and basis and currently eligible assurance supports.
- The explicit map covers the entire recorded import closure, including the
  basis; module names are unique and each maps to the exact approved local file.
- All selected file lengths/digests match before unsafe binary deserialization.
  They remain immutable through use under the trusted local-storage model.
- The bound writer emitted exactly the recorded imports, empty extension entries
  and empty IR metadata. Thus the complete catalog closure equals the actual
  embedded import closure. No unverified file is opened merely to inspect it.

Set the worker search path empty for this restore path as defense in depth.
The upstream loader otherwise falls back to `findOLean` when an explicit map
entry is missing. Do not use the ordinary project's search path or allow an
import-plan caller to insert peer paths. A missing map entry is a refusal, not
permission to resolve an import online.

After restore, require `quotInit=true` and the recorded root census at the
selected boundary. A full re-comparison/re-check of every old proof is neither
necessary nor intended: authenticated local bytes preserve the original writer's
checked state. Runtime/serializer correctness remains in the declared TCB.
For initial qualification, compare the restored newly written chunk records to
the pre-save actual records; this is a focused round-trip boundary check.

## Basis: one distinct authorized chunk, never arbitrary Init import

The root basis writer is a separate internal function, not the extension API:

```lean
def createBasisChunk
    (fixedSeed fixedInventory : Lean.Json)
    (moduleName : Lean.Name)
    (freshPath : System.FilePath)
    : IO SavedChunk
```

The controller supplies only exact profile-pinned files:

- seed SHA-256 `a0acdc706f5e42dca21950c14db2307a18955c63ff953019aaff413d0a976001`;
- inventory SHA-256 `c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0`.

Call existing `BootstrapProbe.receiveSeed (payload inventory : Json)
: IO Lean.Environment` in `software/native/BootstrapSupport.lean:960` under a
pinned source/runtime selection. It starts empty, checked-inserts fixed
descriptors, generates Quot in the kernel, compares output rows and checks the
exact name census. Its historic logging calls itself an experiment; integration
must make the newly adopted production profile explicit rather than treating
an old success log as authority.

After success, read the finite actual kernel constants, order them by the
profile's fixed export-name order, and save a `ModuleData` with empty imports,
all those actual constants, and no entries/IR. Do not use `DeclCodec.inventoryRow`
to project this basis: its extension format intentionally forbids axiom and
quotient records. The basis's own fixed inventory format and source pin establish
its identity. The new ordinary extension format remains metadata-preserving.

This is one actual first-time library initialization when root selects it, not
another broad seed-qualification campaign or a basis replay on every test/session.
Only after its protected chunk is committed may subsequent sessions restore it.
The current conditional `AdmissionChecks` fixture importing owner-selected Init
does not supply this durable basis warrant and cannot be promoted into it.

The nonempty import restore sets `quotInit=true` internally. This matches the
already checked basis state and is why this profile cannot accept prelude-free
or partially initialized basis chunks. The original names and fixed builtin
meanings must remain immutable; normal owner `Init` compatibility is handled
by the separate owner bridge, not by importing both environments together.

## Fresh native profile and minimal catalog

Define a new `DMKN_ORDINARY_NATIVE_PROFILE_V1`; do not insert placeholder relation
images into the existing zk-specific `TrustDomain` schema. Fields:

| Field | Binding |
|---|---|
| `checker_support` | Exact selected Lean runtime/kernel and trusted adapter role manifest ID; stable across operation grants. |
| `basis_seed`, `basis_inventory` | Exact fixed bytes above. |
| `basis_receiver_support` | Exact selected bootstrap constructor implementation. |
| `expression_format`, `declaration_format` | `DMKN_LEAN_ORIGINAL_EXPR_V1`, `DMKN_LEAN_ORDINARY_UNIT_V1`, with erase-mdata-only extension normalization. |
| `axiom_policy` | No new extension axiom/Quot primitive/unsafe/sorry; the exact permitted basis is already pinned, not merely three names. |
| `snapshot_format` | Pinned Lean4.34 single ModuleData chunk, preserved proof values, empty entries/IR, exact local import map. |
| `support_lineage` | Initially only the adopted native/basis stack. No cross-profile certified assumptions in this first seam. |

`profile_id = H(domain, canonical_profile)` uses the project's existing bounded
canonical JSON/hash pattern. Toolchain version labels are advisory; exact selected
runtime roles identify what executes. Local absolute paths and per-operation
resource limits are not mathematical identity. Finite resource failures remain
distinct from mathematical falsehood.

Avoid a cycle between module name and artifact hash:

```text
basis_root = H("ordinary-basis-root-v1", profile_id, seed_hash, inventory_hash)
extension_root = H("ordinary-extension-root-v1", profile_id, parent_root,
                   exact_ordered_batch_bytes_hash)
snapshot_module = Name.str (Name.str Name.anonymous "DMKNLocal") ("r" + root)
```

The exact serialized batch already binds expected full output records; successful
admission is required before publishing this root. Artifact length/hash are
recorded afterwards, separately from mathematical identity. A refused batch's
computed root has no accepted record and no authority.

One bounded SQLite catalog is sufficient. Suggested tables:

```text
meta(id=1, profile_bytes, profile_id, owner_store_id)
roots(root PRIMARY KEY, kind, parent NULLABLE, module_name, artifact_path,
      artifact_bytes, artifact_sha256, names_count, request_hash,
      support_set_bytes, committed_generation)
operations(id PRIMARY KEY, grant_bytes, state, root NULLABLE, outcome_bytes)
```

Each root row is inserted only after successful local checking and artifact
finalization. A separate `accepted` boolean writable by arbitrary callers is
not useful. Presence in the protected roots table under this schema is the
record of legitimate local promotion. `parent` is a foreign key; the first seam
needs no generalized DAG schema, distributed ledger or global transaction.
`support_set_bytes` is a canonical finite set; initially it is the one ordinary
stack. Do not implement cross-profile imports now merely to populate it.

The root catalog is private authority state. Existing packet/module custody
stores remain untrusted bytes and may share physical transport primitives, but
cannot write this table. Existing discovery reports/operations are not warrants.
No public restore accepts a report path and marks it accepted.

## Reuse actual Python primitives without inheriting whole frameworks

- `continuing_context/client/workspace_atomic.py:163-334` provides the supported
  Windows byte-lock owner, fresh grants, SQLite DELETE/FULL transaction and
  interrupted-operation pattern. Copy/extract the small required pieces into
  the fresh ordinary owner; do not construct its old zk receipt owners just to
  obtain a lock or grant.
- `validation_phase/admission/trust.py` provides exact local adoption identity
  and a sticky `WITHDRAWN` marker. The ordinary owner needs a small native-profile
  equivalent; it must not claim the old schema already supports native profiles.
- `managed_storage/placement/storage_paths.py` has ordinary-file, no-alias,
  bounded pre-open database/journal checks. `storage_profile.configure_connection`
  demonstrates explicit journal/page-size/synchronous validation. These helpers
  have lineage preconditions: importing a helper does not authenticate an
  arbitrary existing SQLite file. Prefer direct reuse of the small checks or a
  tightly reviewed dependency, not all managed two-slot placement infrastructure.
- Existing `hashlib`, canonical JSON and `sqlite3` suffice. No external service,
  key management, administrator attestation or new storage runtime is needed.

For a fresh store, pin an ordinary adoption record plus one owner lock. On open,
validate that exact native profile before opening a writable known catalog;
enforce its finite database/artifact quota and allowed journal sidecars. Do not
mutate old workspace schemas or migrate frozen states implicitly.

## Exact transaction, grants and withdrawal

One extension operation follows:

1. New finite grant and fresh stage directory; reserve full potential output.
2. Read committed parent metadata/support status. Validate each newly loaded
   selected artifact once, not every `_active` call or unrelated install file.
3. Invoke the pinned local worker with exact restore plan/batch/output binding.
   It restores, checked-inserts and writes only actual added constants.
4. Require clean worker completion; verify the expected fresh output census,
   module/parent bindings, size limits and exact artifact bytes. Flush the file
   through the trusted controller; save under a unique protected immutable path.
5. Recheck eligibility/withdrawal; in one `BEGIN IMMEDIATE` transaction insert
   the root row and its operation outcome. Commit before returning durable root.
6. Close live process/grant handles. A later operation always obtains a new grant.

Crashes before step5 leave only unaccepted staging artifacts. A committed root
with missing/corrupt bytes refuses restore before Lean deserialization. The
absence of authority is not repaired by loading a matching peer filename.
An acknowledgment lost after commit is resolved by exact root lookup, not
automatic replay. Operation costs/failures remain charged; partial admission
is never promoted. No cleanup/GC campaign is required to prove this first seam.

The profile withdrawal marker blocks new restore/admission before output
promotion. It does not erase saved data or recall already returned conclusions.
The native catalog depends on its exact profile; no cryptographic source support
may be silently discarded by persisting a Lean axiom. When a later bridge is
implemented, its support union and descendant invalidation become additional
schema/application obligations. Same-owner/OS whole-store rollback and hostile
concurrent mutation are excluded, matching the existing local trust model.

Hashing happens once for newly loaded selected artifacts per process. Within a
single owner process, immutable checked environments may serve multiple fresh
operation grants. The current `maxStageTwo` bounds new in-process state; when
approaching it, explicitly restore a committed parent so earlier constants move
to stage1. That reset reloads local data, not mathematical proof checking. It
must not silently raise caps or force an ancestor replay on every new theorem.

## Highest-payoff finite integration endpoint

After the direct admission checks pass, root should select these concrete source
pieces, followed by one targeted cross-process workflow:

1. Initialize and commit the exact basis once under the fresh native profile.
2. Admit the actual dependency extension and reusable Std-backed method as inert
   data; produce chunk A from `CheckedBatch.added`, not the author environment.
3. Close. Restore A in a new process with no ordinary project search path and
   no source/proof replay, then check and commit downstream chunk B.
4. Restore B and verify its exact declaration records/usable theorem. Include
   two consecutive same-process commits to discriminate correct delta census
   from stage2 duplication; this should not require a second broad workload.
5. Exercise only new trust boundaries: missing map entry, foreign/corrupt native
   artifact, uncommitted file, wrong profile/basis, withdrawn adoption and expired
   grant. Reuse existing unchanged codec/admission evidence.

Discovery and ordinary-project checked rebinding must then connect to this same
profile/catalog endpoint; isolated round-trip success is not final v5 or useful
growth evidence. This contract is intended to make that integration small and
operable, not to defer it behind another architecture study.
