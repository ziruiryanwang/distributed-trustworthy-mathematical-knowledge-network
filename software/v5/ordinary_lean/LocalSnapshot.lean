import CheckedExtension
import Lean.Environment

/- INTERNAL local persistence plumbing, not peer admission or a protected store.
   The trusted controller supplies the exact-profile warranted parent and a
   complete catalog-authenticated import plan. It checks artifact digests before
   this unsafe native deserialization, keeps files immutable during use, owns
   fresh operation grants/output reservation, and commits only after clean exit.
   No peer .olean, source frontend environment or saved PASS is authority.
   The fixed-basis initializer/catalog/withdrawal owner are separate integration.
   This file deliberately contains no import-Init shortcut or generic basis hook. -/

open Lean

namespace OrdinaryLean.LocalSnapshot

structure Limits where
  maxModules : Nat := 4096
  maxNames : Nat := 1048576
  maxArtifactBytes : Nat := 1073741824
  maxTotalBytes : Nat := 4294967296
  maxPathBytes : Nat := 32768
  deriving Inhabited

/-- Catalog-owned metadata, not a peer assertion of checking or file integrity.
    The first record is the fixed checked basis; each later record has exactly
    its preceding record as parent. The current implementation restores a chain. -/
structure LocalModule where
  moduleName : Name
  path : System.FilePath
  parentModule : Option Name
  artifactBytes : Nat
  namesCount : Nat
  deriving Inhabited

structure LocalImportPlan where
  basisModule : Name
  rootModule : Name
  modules : Array LocalModule
  deriving Inhabited

/-- A fresh local file description, never a durable acceptance record or grant. -/
structure SavedChunk where
  moduleName : Name
  parentModule : Name
  path : System.FilePath
  names : Array Name
  unitsChecked : Nat
  artifactBytes : Nat
  deriving Inhabited

/-- Internal same-process continuation state. The environment is the actual
    checked result, not reconstructed from the file description. Neither field
    is a serialized grant or permission to skip protected catalog promotion. -/
structure WrittenExtension where
  chunk : SavedChunk
  environment : Environment
  deriving Nonempty

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"ORDINARY_SNAPSHOT {message}"

private def requireModule (name : Name) : IO Unit := do
  if name.isAnonymous then fail "ANONYMOUS_MODULE"
  ExprCodec.requireSemanticName name

private def requirePath (path : System.FilePath) (limits : Limits) : IO Unit := do
  if !path.isAbsolute || path.toString.utf8ByteSize > limits.maxPathBytes then
    fail "ABSOLUTE_BOUNDED_PATH_REQUIRED"
  if path.components.contains ".." || path.components.contains "." then
    fail "DOT_PATH_COMPONENT"
  -- The controller additionally verifies fully qualified canonical paths,
  -- ancestor redirections, root ownership and no concurrent replacement.

private def requireFresh (path : System.FilePath) (limits : Limits) : IO Unit := do
  requirePath path limits
  let present ← try
    discard path.symlinkMetadata
    pure true
  catch error =>
    match error with
    | .noFileOrDirectory .. => pure false
    | _ => throw error
  if present then fail "FRESH_OUTPUT_REQUIRED"
  let some directory := path.parent | fail "OUTPUT_PARENT_REQUIRED"
  let metadata ← directory.symlinkMetadata
  if metadata.type != .dir then fail "ORDINARY_OUTPUT_DIRECTORY_REQUIRED"

private def ordinarySize (path : System.FilePath) (limits : Limits) : IO Nat := do
  requirePath path limits
  let metadata ← path.symlinkMetadata
  if metadata.type != .file || metadata.numLinks != 1 then
    fail "ORDINARY_SINGLE_LINK_FILE_REQUIRED"
  let count := metadata.byteSize.toNat
  if count == 0 || count > limits.maxArtifactBytes then fail "ARTIFACT_BYTE_BOUND"
  return count

private def oneImport (parentModule : Name) : Import := {
  module := parentModule
  importAll := false
  isExported := true
  isMeta := false
}

/-- Only the actual result returned inside checkAndWriteChunk reaches this
    private writer. It does not dump stage2 and does not install peer records. -/
private def writeCheckedBatch
    (parentModule moduleName : Name)
    (path : System.FilePath)
    (checked : CheckedExtension.CheckedBatch)
    (limits : Limits) : IO SavedChunk := do
  requireModule parentModule
  requireModule moduleName
  if parentModule == moduleName then fail "SELF_IMPORT"
  if !checked.environment.toKernelEnv.quotInit then fail "INITIALIZED_PROFILE_REQUIRED"
  if checked.added.isEmpty || checked.added.size > limits.maxNames then
    fail "ADDED_NAME_BOUND"
  let mut seen : Std.HashSet Name := {}
  for actual in checked.added do
    CheckedExtension.requireName actual.name
    if seen.contains actual.name then fail "DUPLICATE_ADDED_NAME"
    if actual.isAxiom || actual.isUnsafe || actual.isPartial then
      fail "UNSAFE_OR_AXIOM_ADDED_RECORD"
    seen := seen.insert actual.name
  requireFresh path limits
  let data : ModuleData := {
    isModule := false
    imports := #[oneImport parentModule]
    constNames := checked.added.map (fun actual => actual.name)
    constants := checked.added
    extraConstNames := #[]
    entries := #[]
  }
  saveModuleData path moduleName data
  let artifactBytes ← ordinarySize path limits
  return {
    moduleName := moduleName
    parentModule := parentModule
    path := path
    names := data.constNames
    unitsChecked := checked.unitsChecked
    artifactBytes := artifactBytes
  }

/-- Internal trusted-controller entry point. The parent must be the warranted
    environment named by parentModule under the selected initialized profile.
    This function does not authenticate that relationship or create a grant.
    A failed batch writes no snapshot. A write failure may leave uncommitted
    local bytes; only the protected controller may promote a clean result. -/
def checkAndWriteChunk
    (parent : Environment)
    (parentModule moduleName : Name)
    (units : Array DeclCodec.DecodedUnit)
    (path : System.FilePath)
    (checkingLimits : CheckedExtension.Limits := {})
    (snapshotLimits : Limits := {}) : IO WrittenExtension := do
  requireModule parentModule
  requireModule moduleName
  if parentModule == moduleName then fail "SELF_IMPORT"
  requireFresh path snapshotLimits
  let checked ← CheckedExtension.checkBatch parent units checkingLimits
  let chunk ← writeCheckedBatch parentModule moduleName path checked snapshotLimits
  return {
    chunk := chunk
    environment := checked.environment
  }

/-- Validate the complete protected one-parent closure before native import.
    Hash/lineage validation belongs to the trusted owner, not to this metadata
    check. A missing parent or an extra unrelated module is refused here. -/
private def importArtifacts (plan : LocalImportPlan) (limits : Limits)
    : IO (NameMap ImportArtifacts) := do
  requireModule plan.basisModule
  requireModule plan.rootModule
  if plan.modules.isEmpty || plan.modules.size > limits.maxModules then
    fail "IMPORT_MODULE_BOUND"
  let mut artifacts : NameMap ImportArtifacts := {}
  let mut names : Std.HashSet Name := {}
  let mut paths : Std.HashSet String := {}
  let mut expectedParent : Option Name := none
  let mut totalBytes := 0
  let mut totalNames := 0
  for entry in plan.modules do
    requireModule entry.moduleName
    if names.contains entry.moduleName || paths.contains entry.path.toString then
      fail "DUPLICATE_MODULE_OR_PATH"
    if entry.parentModule != expectedParent then fail "INCOMPLETE_OR_UNORDERED_IMPORT_CHAIN"
    if expectedParent.isNone && entry.moduleName != plan.basisModule then
      fail "BASIS_MODULE_MISMATCH"
    if entry.namesCount == 0 || entry.namesCount > limits.maxNames then
      fail "IMPORT_NAME_BOUND"
    let count ← ordinarySize entry.path limits
    if count != entry.artifactBytes then fail "IMPORT_ARTIFACT_SIZE_MISMATCH"
    totalBytes := totalBytes + count
    totalNames := totalNames + entry.namesCount
    if totalBytes > limits.maxTotalBytes || totalNames > limits.maxNames then
      fail "IMPORT_TOTAL_BOUND"
    artifacts := artifacts.insert entry.moduleName
      (ImportArtifacts.ofArrays #[#[entry.path], #[]])
    names := names.insert entry.moduleName
    paths := paths.insert entry.path.toString
    expectedParent := some entry.moduleName
  if expectedParent != some plan.rootModule then fail "ROOT_MODULE_MISMATCH"
  return artifacts

/-- Check stored import/header bindings after authenticated native load. This
    scans finite module metadata, not ancestor proof terms or kernel derivations. -/
private def checkRestored (plan : LocalImportPlan) (environment : Environment)
    : IO Unit := do
  if !environment.toKernelEnv.quotInit then fail "RESTORED_QUOTIENT_STATE"
  let actualNames := environment.allImportedModuleNames
  let actualData := environment.header.moduleData
  if actualNames.size != plan.modules.size || actualData.size != plan.modules.size then
    fail "RESTORED_MODULE_CENSUS"
  for index in [:plan.modules.size] do
    let entry := plan.modules[index]!
    let data := actualData[index]!
    if actualNames[index]! != entry.moduleName then fail "RESTORED_MODULE_IDENTITY"
    if data.isModule || !data.entries.isEmpty || !data.extraConstNames.isEmpty then
      fail "RESTORED_UNSUPPORTED_METADATA"
    if data.constNames.size != entry.namesCount || data.constants.size != entry.namesCount then
      fail "RESTORED_CONSTANT_CENSUS"
    let expectedImports := match entry.parentModule with
      | none => #[]
      | some parentModule => #[oneImport parentModule]
    if data.imports != expectedImports then fail "RESTORED_IMPORT_BINDING"

/-- Restore only previously checked, protected local artifacts. The controller
    authenticates all bytes and the embedded-import/catalog correspondence
    before calling. This is never an untrusted .olean verification function.
    No concurrent changes to Lean's global searchPathRef are permitted. -/
def restoreLocal (plan : LocalImportPlan) (limits : Limits := {}) : IO Environment := do
  let artifacts ← importArtifacts plan limits
  let previousPath ← Lean.searchPathRef.get
  Lean.searchPathRef.set []
  try
    let restored ← Lean.importModules #[{ module := plan.rootModule }] {} 0
      (plugins := #[]) (leakEnv := false) (loadExts := false)
      (level := .private) (arts := artifacts)
    checkRestored plan restored
    return restored
  finally
    Lean.searchPathRef.set previousPath

end OrdinaryLean.LocalSnapshot
