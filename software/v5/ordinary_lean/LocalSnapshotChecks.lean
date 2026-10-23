import LocalSnapshot

/- Focused owner-authored persistence controls, NOT production basis acceptance.
   A small exact subset of owner-selected Init supplies a CONDITIONAL fixture.
   No peer source/binary is consumed, no protected catalog/grant is implemented,
   and no cryptographic proof or ancestor-proof replay is performed on restore.
   The outer selected runner must pin source/runtime and bound the child tree. -/

open Lean OrdinaryLean

namespace LocalSnapshotChecks

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"SNAPSHOT_CHECK_FAILED {message}"

def ensure (condition : Bool) (message : String) : IO Unit := do
  if !condition then fail message

def passed (label : String) : IO Unit :=
  IO.println s!"SNAPSHOT_CHECK_PASS {label}"

def expectReject (label marker : String) (action : IO Unit) : IO Unit := do
  let caught ← try
    action
    pure none
  catch error => pure (some error.toString)
  match caught with
  | none => fail s!"{label}: unexpectedly succeeded"
  | some message =>
      ensure (message.contains marker) s!"{label}: wrong rejection: {message}"
      passed label

def basisModule : Name := `SnapshotControlStorage.Basis
def firstModule : Name := `SnapshotControlStorage.First
def secondModule : Name := `SnapshotControlStorage.Second
def firstName : Name := `SnapshotControlMath.identity
def secondName : Name := `SnapshotControlMath.reuseIdentity
def thirdName : Name := `SnapshotControlMath.afterRestore

def identityDecl : Declaration :=
  .thmDecl {
    name := firstName
    levelParams := []
    type := .forallE `proposition (.sort .zero)
      (.forallE `witness (.bvar 0) (.bvar 1) .default) .implicit
    value := .lam `proposition (.sort .zero)
      (.lam `witness (.bvar 0) (.bvar 0) .default) .implicit
  }

def reuseDecl : Declaration :=
  .thmDecl {
    name := secondName
    levelParams := []
    type := .const ``True []
    value := mkApp2 (.const firstName []) (.const ``True []) (.const ``True.intro [])
  }

def afterRestoreDecl : Declaration :=
  .thmDecl {
    name := thirdName
    levelParams := []
    type := .const ``True []
    value := .const secondName []
  }

/-- Expected inventory is a claim. Actual checkAndWriteChunk/checkBatch still
    checks the declaration and compares the kernel-generated record. -/
def theoremUnit (declaration : Declaration) : IO DeclCodec.DecodedUnit := do
  let .thmDecl value := declaration | fail "fixture theorem kind"
  return {
    decl := declaration
    expected := #[← DeclCodec.inventoryRow (.thmInfo value)]
  }

def lookup (environment : Environment) (name : Name) : IO ConstantInfo := do
  let some actual := environment.toKernelEnv.find? name | fail s!"missing {name}"
  return actual

def requireRow (environment : Environment) (name : Name)
    (unit : DeclCodec.DecodedUnit) : IO Unit := do
  let some expected := unit.expected[0]? | fail "missing fixture inventory"
  let actual ← lookup environment name
  ensure ((← DeclCodec.inventoryRow actual) == expected) s!"restored record differs: {name}"

def snapshotLimits : LocalSnapshot.Limits := {
  maxModules := 4
  maxNames := 64
  maxArtifactBytes := 1048576
  maxTotalBytes := 4194304
  maxPathBytes := 32768
}

/-- Test-local fixture construction ONLY. The production fixed-basis initializer
    must independently check its exact pinned seed instead of doing this. -/
def writeConditionalFixture (sysroot path : System.FilePath)
    : IO LocalSnapshot.LocalModule := do
  Lean.searchPathRef.set [sysroot / "lib" / "lean"]
  let fixture ← Lean.importModules #[{ module := `Init }] {} 0
    (plugins := #[]) (loadExts := false) (level := .private)
  ensure fixture.toKernelEnv.quotInit "owner fixture quotient state"
  let names : Array Name := #[``Eq, ``Eq.refl, ``Eq.rec,
    ``Quot, ``Quot.mk, ``Quot.lift, ``Quot.ind,
    ``True, ``True.intro, ``True.rec]
  let mut constants : Array ConstantInfo := #[]
  for name in names do constants := constants.push (← lookup fixture name)
  ensure (!(← path.pathExists)) "fixture path must be fresh"
  let data : ModuleData := {
    isModule := false
    imports := #[]
    constNames := names
    constants := constants
    extraConstNames := #[]
    entries := #[]
  }
  Lean.saveModuleData path basisModule data
  let metadata ← path.symlinkMetadata
  return {
    moduleName := basisModule
    path := path
    parentModule := none
    artifactBytes := metadata.byteSize.toNat
    namesCount := names.size
  }

def chunkEntry (chunk : LocalSnapshot.SavedChunk) : LocalSnapshot.LocalModule := {
  moduleName := chunk.moduleName
  path := chunk.path
  parentModule := some chunk.parentModule
  artifactBytes := chunk.artifactBytes
  namesCount := chunk.names.size
}

def run (sysroot output : System.FilePath) : IO Unit := do
  ensure (output.isAbsolute && !(← output.pathExists)) "fresh absolute control output required"
  IO.FS.createDirAll output
  IO.println "SNAPSHOT_FIXTURE owner-selected-Init-subset conditional=true catalogAuthority=false"
  let basis ← writeConditionalFixture sysroot (output / "basis.olean")
  let basisPlan : LocalSnapshot.LocalImportPlan := {
    basisModule := basisModule
    rootModule := basisModule
    modules := #[basis]
  }
  let parent ← LocalSnapshot.restoreLocal basisPlan snapshotLimits
  let firstUnit ← theoremUnit identityDecl
  let secondUnit ← theoremUnit reuseDecl
  let thirdUnit ← theoremUnit afterRestoreDecl
  let first ← LocalSnapshot.checkAndWriteChunk parent basisModule firstModule
    #[firstUnit] (output / "first.olean") {} snapshotLimits
  ensure (first.chunk.names == #[firstName] && first.chunk.unitsChecked == 1)
    "first exact delta"
  -- Crucial regression: no import/restore occurs between these two calls.
  -- The second writer receives an environment whose stage2 already contains A.
  let second ← LocalSnapshot.checkAndWriteChunk first.environment firstModule secondModule
    #[secondUnit] (output / "second.olean") {} snapshotLimits
  ensure (second.chunk.names == #[secondName] && second.chunk.unitsChecked == 1)
    "second writer dumped old stage2 constants"
  let stageTwo ← CheckedExtension.stageTwoNames second.environment.toKernelEnv 64
  ensure (stageTwo.size == 2 && stageTwo.contains firstName && stageTwo.contains secondName)
    "same-process checked environments not retained"
  passed "two-chained-deltas-without-intermediate-restore"

  let firstEntry := chunkEntry first.chunk
  let secondEntry := chunkEntry second.chunk
  let plan : LocalSnapshot.LocalImportPlan := {
    basisModule := basisModule
    rootModule := secondModule
    modules := #[basis, firstEntry, secondEntry]
  }
  let restored ← LocalSnapshot.restoreLocal plan snapshotLimits
  requireRow restored firstName firstUnit
  requireRow restored secondName secondUnit
  let some storedFirst := restored.header.moduleData[1]? | fail "first chunk absent"
  let some storedSecond := restored.header.moduleData[2]? | fail "second chunk absent"
  ensure (storedFirst.constNames == #[firstName] && storedSecond.constNames == #[secondName])
    "stored chunk census is not exact added delta"
  let restoredStageTwo ← CheckedExtension.stageTwoNames restored.toKernelEnv 64
  ensure (restoredStageTwo.size == 0) "restored ancestors did not enter stage1"
  passed "exact-map-restore-without-ancestor-checking"

  -- Check only one new consumer declaration. A and B are never re-submitted
  -- to checkBatch after restore, and no old inert proof packet is read.
  let continuation ← CheckedExtension.checkBatch restored #[thirdUnit]
  ensure (continuation.unitsChecked == 1 && continuation.added.size == 1)
    "unexpected postrestore admission count"
  requireRow continuation.environment thirdName thirdUnit
  passed "restored-theorem-supports-new-consumer-proof"

  let incomplete : LocalSnapshot.LocalImportPlan := { plan with
    modules := #[basis, secondEntry]
  }
  expectReject "incomplete-import-plan" "INCOMPLETE_OR_UNORDERED_IMPORT_CHAIN" do
    discard <| LocalSnapshot.restoreLocal incomplete snapshotLimits

  let wrongParent : LocalSnapshot.LocalModule := { secondEntry with
    parentModule := some basisModule
  }
  let wrongPlan : LocalSnapshot.LocalImportPlan := { plan with
    modules := #[basis, firstEntry, wrongParent]
  }
  expectReject "wrong-parent-plan" "INCOMPLETE_OR_UNORDERED_IMPORT_CHAIN" do
    discard <| LocalSnapshot.restoreLocal wrongPlan snapshotLimits

  let preserved ← IO.FS.readBinFile first.chunk.path
  expectReject "existing-output-refused" "FRESH_OUTPUT_REQUIRED" do
    discard <| LocalSnapshot.checkAndWriteChunk restored secondModule
      `SnapshotControlStorage.Unused #[thirdUnit] first.chunk.path {} snapshotLimits
  ensure ((← IO.FS.readBinFile first.chunk.path) == preserved) "existing artifact changed"

  let empty ← Lean.mkEmptyEnvironment 0
  let refusedPath := output / "uninitialized-refused.olean"
  expectReject "uninitialized-parent-refused" "INITIALIZED_PROFILE_REQUIRED" do
    discard <| LocalSnapshot.checkAndWriteChunk empty basisModule
      `SnapshotControlStorage.Uninitialized #[firstUnit] refusedPath {} snapshotLimits
  ensure (!(← refusedPath.pathExists)) "uninitialized parent wrote a snapshot"
  IO.println "SNAPSHOT_CHECKS_COMPLETE conditionalFixtureOnly=true protectedCatalog=false basisAdoption=false publicDeployment=false"

end LocalSnapshotChecks

def main (args : List String) : IO UInt32 := do
  match args with
  | [sysroot, output] =>
      LocalSnapshotChecks.run (System.FilePath.mk sysroot) (System.FilePath.mk output)
      return 0
  | _ => throw <| IO.userError "USAGE LocalSnapshotChecks PINNED_SYSROOT FRESH_OUTPUT_DIRECTORY"
