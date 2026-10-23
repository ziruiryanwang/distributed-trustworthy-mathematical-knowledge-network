import BootstrapSupport
import LocalSnapshot

/- INTERNAL fixed-basis initialization and snapshot writing.
   The trusted controller must authenticate the exact immutable input files
   BEFORE JSON parsing and invocation:
     seed: 724174 bytes,
       a0acdc706f5e42dca21950c14db2307a18955c63ff953019aaff413d0a976001
     inventory: 823690 bytes,
       c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0
   Arbitrary peer JSON with the same counts or source label is NOT authorized.
   Profile adoption, runtime/source pinning, fresh grants, output reservation,
   durability, withdrawal and protected catalog promotion are controller duties.
   This wrapper calls the real empty-environment checked seed receiver. It never
   imports Init, copies a peer ConstantInfo, or treats a saved PASS as evidence. -/

open Lean

namespace OrdinaryLean.BasisSnapshot

def fixedNameCount : Nat := 581
def fixedUnitCount : Nat := 456

/-- Local file description only; no parent, operation grant or public warrant. -/
structure SavedBasis where
  moduleName : Name
  path : System.FilePath
  names : Array Name
  artifactBytes : Nat
  deriving Inhabited

/-- Only the actual checked seed environment is returned for local continuation. -/
structure WrittenBasis where
  chunk : SavedBasis
  environment : Environment
  deriving Nonempty

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"ORDINARY_BASIS_SNAPSHOT {message}"

/- These small guards intentionally duplicate the already reviewed snapshot
   pattern instead of modifying the successful LocalSnapshot source solely to
   expose private utilities. Canonical protected paths/no concurrent replacement
   and fixed input authentication remain explicit controller preconditions. -/
private def requirePath (path : System.FilePath) (limits : LocalSnapshot.Limits)
    : IO Unit := do
  if !path.isAbsolute || path.toString.utf8ByteSize > limits.maxPathBytes then
    fail "ABSOLUTE_BOUNDED_PATH_REQUIRED"
  if path.components.contains ".." || path.components.contains "." then
    fail "DOT_PATH_COMPONENT"

private def requireFresh (path : System.FilePath) (limits : LocalSnapshot.Limits)
    : IO Unit := do
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
  if (← directory.symlinkMetadata).type != .dir then
    fail "ORDINARY_OUTPUT_DIRECTORY_REQUIRED"

private def ordinarySize (path : System.FilePath) (limits : LocalSnapshot.Limits)
    : IO Nat := do
  requirePath path limits
  let metadata ← path.symlinkMetadata
  if metadata.type != .file || metadata.numLinks != 1 then
    fail "ORDINARY_SINGLE_LINK_FILE_REQUIRED"
  let count := metadata.byteSize.toNat
  if count == 0 || count > limits.maxArtifactBytes then fail "ARTIFACT_BYTE_BOUND"
  return count

/-- Accept only controller-authenticated fixed inputs. Counts and quotInit are
    consistency checks, not authentication of arbitrary JSON or a foundation.
    The seed receiver rechecks the fixed declarations from an empty environment
    and compares generated records before this wrapper can write any artifact. -/
def checkAndWriteBasis
    (seed inventory : Json)
    (moduleName : Name)
    (freshPath : System.FilePath)
    (limits : LocalSnapshot.Limits := {}) : IO WrittenBasis := do
  if moduleName.isAnonymous then fail "ANONYMOUS_MODULE"
  ExprCodec.requireSemanticName moduleName
  if fixedNameCount > limits.maxNames then fail "BASIS_NAME_BOUND"
  requireFresh freshPath limits
  let seedFields ← BootstrapProbe.arrayOf seed (some 3)
  let descriptors ← BootstrapProbe.arrayOf seedFields[1]!
  let rawNames ← BootstrapProbe.arrayOf seedFields[2]!
  let inventoryRows ← BootstrapProbe.arrayOf inventory
  if descriptors.size != fixedUnitCount || rawNames.size != fixedNameCount ||
      inventoryRows.size != fixedNameCount then
    fail "FIXED_INPUT_CENSUS"

  let environment ← BootstrapProbe.receiveSeed seed inventory
  let kernel := environment.toKernelEnv
  if !kernel.quotInit then fail "CHECKED_QUOTIENT_REQUIRED"
  if kernel.constants.toList.length != fixedNameCount then fail "ACTUAL_BASIS_CENSUS"
  let mut names : Array Name := #[]
  let mut constants : Array ConstantInfo := #[]
  let mut seen : Std.HashSet Name := {}
  -- receiveSeed already verifies this ordering equals the fixed inventory's
  -- ordering. Read records only from the returned kernel, never the inventory.
  for rawName in rawNames do
    let name ← BootstrapProbe.nameOf rawName
    if seen.contains name then fail "DUPLICATE_BASIS_NAME"
    let some actual := kernel.find? name | fail "MISSING_CHECKED_BASIS_NAME"
    names := names.push name
    constants := constants.push actual
    seen := seen.insert name
  requireFresh freshPath limits
  let data : ModuleData := {
    isModule := false
    imports := #[]
    constNames := names
    constants := constants
    extraConstNames := #[]
    entries := #[]
  }
  Lean.saveModuleData freshPath moduleName data
  let artifactBytes ← ordinarySize freshPath limits
  let chunk : SavedBasis := {
    moduleName := moduleName
    path := freshPath
    names := names
    artifactBytes := artifactBytes
  }
  return {
    chunk := chunk
    environment := environment
  }

end OrdinaryLean.BasisSnapshot
