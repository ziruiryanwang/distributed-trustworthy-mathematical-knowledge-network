import LocalSnapshot
import Lean.PrivateName

/- One changed-boundary control, not a production basis bootstrap.
   The 11 selected Init records form an explicitly conditional owner fixture.
   No protected catalog, peer artifact, full seed or Std closure is consumed.
   Root must pin the runtime and compiled successor modules before execution. -/

open Lean OrdinaryLean

namespace KernelAdmissionChecks

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"KERNEL_ADMISSION_CHECK_FAILED {message}"

def ensure (condition : Bool) (message : String) : IO Unit := do
  if !condition then fail message

def passed (label : String) : IO Unit :=
  IO.println s!"KERNEL_ADMISSION_CHECK_PASS {label}"

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

def publicName : Name := `KernelCollision.token
def privateA : Name := mkPrivateNameCore `KernelAdmissionAlpha publicName
def privateB : Name := mkPrivateNameCore `KernelAdmissionBeta publicName
def lawA : Name := `KernelAdmissionMath.alpha_is_false
def lawB : Name := `KernelAdmissionMath.beta_is_true
def lawPublic : Name := `KernelAdmissionMath.public_is_identity
def afterRestoreName : Name := `KernelAdmissionMath.after_restore
def frontendName : Name := `KernelAdmissionMath.frontend_identity
def groupName : Name := `KernelAdmissionMath.Singleton
def basisModule : Name := `KernelAdmissionStorage.Basis
def firstModule : Name := `KernelAdmissionStorage.First
def secondModule : Name := `KernelAdmissionStorage.Second

def boolType : Expr := .const ``Bool []
def boolFalse : Expr := .const ``Bool.false []
def boolTrue : Expr := .const ``Bool.true []
def equality (left right : Expr) : Expr :=
  mkApp3 (.const ``Eq [Level.succ .zero]) boolType left right
def reflexivity (value : Expr) : Expr :=
  mkApp2 (.const ``Eq.refl [Level.succ .zero]) boolType value

def constantDecl (name : Name) (value : Expr) : Declaration := .defnDecl {
  name, levelParams := [], type := boolType, value, hints := .abbrev, safety := .safe
}

def identityDecl (name : Name) : Declaration := .defnDecl {
  name, levelParams := [],
  type := .forallE `value boolType boolType .default,
  value := .lam `value boolType (.bvar 0) .default,
  hints := .abbrev, safety := .safe
}

def lawDecl (name : Name) (left right proof : Expr) : Declaration := .thmDecl {
  name, levelParams := [], type := equality left right, value := proof
}

def singletonDecl : Declaration := .inductDecl [] 0 [{
  name := groupName, type := .sort (.succ .zero),
  ctors := [{ name := .str groupName "mk", type := .const groupName [] }]
}] false

def badProof : Declaration :=
  lawDecl `KernelAdmissionMath.bad boolFalse boolTrue (reflexivity boolFalse)

def missingReference : Declaration :=
  lawDecl `KernelAdmissionMath.missing (.const `KernelAdmissionUnknown.token [])
    boolFalse (reflexivity boolFalse)

def fixtureNames : Array Name := #[``Eq, ``Eq.refl, ``Eq.rec,
  ``Quot, ``Quot.mk, ``Quot.lift, ``Quot.ind,
  ``Bool, ``Bool.false, ``Bool.true, ``Bool.rec]

def checkingLimits : CheckedExtension.Limits := {
  maxUnits := 4, maxNewNames := 16, maxStageTwo := 32,
  maxScanNodes := 10000, maxHeartbeats := 1000000, maxRecDepth := 1000
}

def snapshotLimits : LocalSnapshot.Limits := {
  maxModules := 4, maxNames := 64, maxArtifactBytes := 1048576,
  maxTotalBytes := 4194304, maxPathBytes := 32768
}

def lookup (environment : Kernel.Environment) (name : Name) : IO ConstantInfo := do
  let some info := environment.find? name | fail s!"missing exact name {name}"
  return info

def requireRows (environment : Kernel.Environment) (units : Array DeclCodec.DecodedUnit)
    : IO Unit := do
  for unit in units do
    let names ← DeclCodec.expectedNames unit.expected
    for index in [:names.size] do
      ensure ((← DeclCodec.inventoryRow (← lookup environment names[index]!)) == unit.expected[index]!)
        s!"exact generated row changed {names[index]!}"

/-- Owner fixture producer only; tested admission still rechecks the resulting claims. -/
def producerUnit (environment : Kernel.Environment) (allowed : Std.HashSet Name)
    (declaration : Declaration)
    : IO (Kernel.Environment × DeclCodec.DecodedUnit × Std.HashSet Name) := do
  let next ← match environment.addDeclCore 1000000 1000 declaration none with
    | .ok next => pure next
    | .error _ => fail "fixture producer kernel rejected"
  -- The fixture's singleton is nonnested; getNames contains its generated group.
  let mut inventory := #[]
  for name in declaration.getNames do inventory := inventory.push (← lookup next name)
  let packet ← DeclCodec.encodeUnit declaration inventory
  let decoded ← DeclCodec.decodeUnit allowed packet
  let mut permitted := allowed
  for name in ← DeclCodec.expectedNames decoded.expected do permitted := permitted.insert name
  return (next, decoded, permitted)

def claim (declaration : Declaration) : IO DeclCodec.DecodedUnit := do
  let info ← match declaration with
    | .defnDecl value => pure (.defnInfo value)
    | .thmDecl value => pure (.thmInfo value)
    | _ => fail "ordinary claim kind"
  return { decl := declaration, expected := #[← DeclCodec.inventoryRow info] }

def tamperConstructor (unit : DeclCodec.DecodedUnit) : IO DeclCodec.DecodedUnit := do
  let mut expected := unit.expected
  let mut changed := false
  for index in [:expected.size] do
    let fields ← ExprCodec.arrayOf expected[index]! (some 5)
    if !changed && (← ExprCodec.natOf fields[1]!) == 5 then
      let details ← ExprCodec.arrayOf fields[4]! (some 5)
      let count ← ExprCodec.natOf details[3]!
      expected := expected.set! index (ExprCodec.arr (fields.set! 4
        (ExprCodec.arr (details.set! 3 (ExprCodec.num (count + 1))))))
      changed := true
  ensure changed "constructor row was not changed"
  return { unit with expected }

def writeFixture (sysroot path : System.FilePath) : IO LocalSnapshot.LocalModule := do
  Lean.searchPathRef.set [sysroot / "lib" / "lean"]
  let imported ← Lean.importModules #[{ module := `Init }] {} 0
    (plugins := #[]) (loadExts := false) (level := .private)
  ensure imported.toKernelEnv.quotInit "conditional fixture quotient state"
  let mut constants := #[]
  for name in fixtureNames do constants := constants.push (← lookup imported.toKernelEnv name)
  ensure (!(← path.pathExists)) "fixture output not fresh"
  Lean.saveModuleData path basisModule {
    isModule := false, imports := #[], constNames := fixtureNames,
    constants, extraConstNames := #[], entries := #[]
  }
  let metadata ← path.symlinkMetadata
  return { moduleName := basisModule, path, parentModule := none,
           artifactBytes := metadata.byteSize.toNat, namesCount := fixtureNames.size }

def chunkEntry (chunk : LocalSnapshot.SavedChunk) : LocalSnapshot.LocalModule := {
  moduleName := chunk.moduleName, path := chunk.path, parentModule := some chunk.parentModule,
  artifactBytes := chunk.artifactBytes, namesCount := chunk.names.size
}

def run (sysroot output : System.FilePath) : IO Unit := do
  ensure (output.isAbsolute && !(← output.pathExists)) "fresh absolute output required"
  IO.FS.createDirAll output
  IO.println "KERNEL_ADMISSION_FIXTURE owner-selected-Init-subset records=11 conditional=true protectedWarrant=false"
  ensure (privateA != privateB && privateA != publicName && privateB != publicName &&
    isPrivateName privateA && isPrivateName privateB && !isPrivateName publicName &&
    privateToUserName privateA == publicName && privateToUserName privateB == publicName)
    "fixture does not have genuine private/private/public projection collisions"
  passed "genuine-name-projection-collision-fixture"
  let basis ← writeFixture sysroot (output / "basis.olean")
  let parent ← LocalSnapshot.restoreLocal {
    basisModule, rootModule := basisModule, modules := #[basis]
  } snapshotLimits
  ensure ((← CheckedExtension.stageTwoNames parent.toKernelEnv 32).size == 0)
    "conditional parent not restored into stage one"
  let mut allowed : Std.HashSet Name := {}
  for name in fixtureNames do allowed := allowed.insert name
  let mut producer := parent.toKernelEnv
  let mut firstUnits : Array DeclCodec.DecodedUnit := #[]
  for declaration in #[constantDecl privateA boolFalse, constantDecl privateB boolTrue,
                        identityDecl publicName] do
    let (next, unit, permitted) ← producerUnit producer allowed declaration
    producer := next
    allowed := permitted
    firstUnits := firstUnits.push unit
  let mut secondUnits : Array DeclCodec.DecodedUnit := #[]
  for declaration in #[
      lawDecl lawA (.const privateA []) boolFalse (reflexivity boolFalse),
      lawDecl lawB (.const privateB []) boolTrue (reflexivity boolTrue),
      lawDecl lawPublic (.app (.const publicName []) boolTrue) boolTrue (reflexivity boolTrue)] do
    let (next, unit, permitted) ← producerUnit producer allowed declaration
    producer := next
    allowed := permitted
    secondUnits := secondUnits.push unit
  let (_, consumer, _) ← producerUnit producer allowed
    (lawDecl afterRestoreName (.const privateB []) boolTrue (.const lawB []))

  let first ← LocalSnapshot.checkAndWriteKernelChunk parent.toKernelEnv basisModule firstModule
    firstUnits (output / "first.olean") checkingLimits snapshotLimits
  ensure (first.chunk.names == #[privateA, privateB, publicName] && first.chunk.unitsChecked == 3)
    "exact three-definition native delta"
  requireRows first.environment firstUnits
  passed "exact-private-private-and-public-names-checked"
  -- No Environment.ofKernelEnv, restore or frontend update between these calls.
  let second ← LocalSnapshot.checkAndWriteKernelChunk first.environment firstModule secondModule
    secondUnits (output / "second.olean") checkingLimits snapshotLimits
  ensure (second.chunk.names == #[lawA, lawB, lawPublic] && second.chunk.unitsChecked == 3)
    "second snapshot dumped prior stage-two constants"
  requireRows second.environment (firstUnits ++ secondUnits)
  ensure ((← CheckedExtension.stageTwoNames second.environment 32).size == 6)
    "same-process exact stage-two census"
  passed "later-exact-references-and-delta-only-snapshot"

  let restored ← LocalSnapshot.restoreLocal {
    basisModule, rootModule := secondModule,
    modules := #[basis, chunkEntry first.chunk, chunkEntry second.chunk]
  } snapshotLimits
  requireRows restored.toKernelEnv (firstUnits ++ secondUnits)
  ensure ((← CheckedExtension.stageTwoNames restored.toKernelEnv 32).size == 0)
    "restored ancestors not in stage one"
  let some storedFirst := restored.header.moduleData[1]? | fail "first stored module missing"
  let some storedSecond := restored.header.moduleData[2]? | fail "second stored module missing"
  ensure (storedFirst.constNames == #[privateA, privateB, publicName] &&
    storedSecond.constNames == #[lawA, lawB, lawPublic]) "stored exact full-name census"
  let continuation ← CheckedExtension.checkKernelBatch restored.toKernelEnv #[consumer] checkingLimits
  ensure (continuation.unitsChecked == 1 && continuation.added.size == 1)
    "restore continuation rechecked ancestors"
  requireRows continuation.environment #[consumer]
  passed "restore-full-names-and-check-only-new-consumer"

  let some firstUnit := firstUnits[0]? | fail "first unit missing"
  expectReject "true-exact-duplicate-in-batch" "OVERWRITE_OR_DUPLICATE" do
    discard <| CheckedExtension.checkKernelBatch parent.toKernelEnv #[firstUnit, firstUnit] checkingLimits
  expectReject "true-exact-parent-overwrite" "OVERWRITE_OR_DUPLICATE" do
    discard <| CheckedExtension.checkKernelBatch first.environment #[firstUnit] checkingLimits

  match parent.toKernelEnv.addDeclCore 1000000 1000 badProof none with
  | .error (.declTypeMismatch ..) | .error (.exprTypeMismatch ..) =>
      passed "bad-proof-is-genuine-kernel-type-mismatch"
  | .error _ => fail "bad proof reached unrelated kernel failure"
  | .ok _ => fail "false-equals-true proof accepted"
  let bad ← claim badProof
  let badPath := output / "bad-refused.olean"
  expectReject "invalid-proof-refuses-before-snapshot" "KERNEL_REJECTED_OR_RESOURCE_LIMIT" do
    discard <| LocalSnapshot.checkAndWriteKernelChunk parent.toKernelEnv basisModule
      `KernelAdmissionStorage.Bad #[bad] badPath checkingLimits snapshotLimits
  ensure (!(← badPath.pathExists)) "invalid proof wrote snapshot"

  let alternate ← claim (constantDecl privateA boolTrue)
  expectReject "ordinary-expected-row-mismatch" "GENERATED_RECORD_MISMATCH" do
    discard <| CheckedExtension.checkKernelBatch parent.toKernelEnv
      #[{ firstUnit with expected := alternate.expected }] checkingLimits
  let missing ← claim missingReference
  expectReject "unbound-reference-refused" "UNGROUNDED_REFERENCE" do
    discard <| CheckedExtension.checkKernelBatch parent.toKernelEnv #[missing] checkingLimits

  let mut baseAllowed : Std.HashSet Name := {}
  for name in fixtureNames do baseAllowed := baseAllowed.insert name
  let (_, groupUnit, _) ← producerUnit parent.toKernelEnv baseAllowed singletonDecl
  let groupChecked ← CheckedExtension.checkKernelBatch parent.toKernelEnv #[groupUnit] checkingLimits
  requireRows groupChecked.environment #[groupUnit]
  ensure (groupChecked.added.size == groupUnit.expected.size && groupChecked.unitsChecked == 1)
    "complete generated group census"
  passed "complete-generated-group-checked"
  let tampered ← tamperConstructor groupUnit
  expectReject "generated-constructor-row-mismatch" "GENERATED_RECORD_MISMATCH" do
    discard <| CheckedExtension.checkKernelBatch parent.toKernelEnv #[tampered] checkingLimits
  expectReject "aggregate-stage-two-bound-retained" "STAGE_TWO_BOUND" do
    discard <| CheckedExtension.checkKernelBatch parent.toKernelEnv firstUnits
      { checkingLimits with maxStageTwo := 2 }
  let empty ← Lean.mkEmptyEnvironment 0
  expectReject "uninitialized-kernel-parent-refused" "INITIALIZED_PROFILE_REQUIRED" do
    discard <| CheckedExtension.checkKernelBatch empty.toKernelEnv #[firstUnit] checkingLimits
  ensure ((← CheckedExtension.stageTwoNames parent.toKernelEnv 32).size == 0)
    "failed calls changed immutable parent census"
  for name in [privateA, privateB, publicName, lawA, lawB, lawPublic, afterRestoreName, groupName] do
    ensure (parent.toKernelEnv.find? name).isNone "failed calls leaked a new parent declaration"
  passed "failed-batches-preserve-immutable-parent"

  let (_, frontendUnit, _) ← producerUnit parent.toKernelEnv baseAllowed (identityDecl frontendName)
  let frontend ← LocalSnapshot.checkAndWriteChunk parent basisModule `KernelAdmissionStorage.Frontend
    #[frontendUnit] (output / "frontend.olean") checkingLimits snapshotLimits
  ensure (frontend.chunk.unitsChecked == 1 && frontend.chunk.names == #[frontendName])
    "old frontend API result changed"
  requireRows frontend.environment.toKernelEnv #[frontendUnit]
  passed "unchanged-environment-backed-snapshot-api"
  IO.println "KERNEL_ADMISSION_CHECKS_COMPLETE fixtureRecords=11 chainCheckedUnits=7 generatedGroupUnits=1 frontendUnits=1 conditionalFixtureOnly=true protectedCatalog=false basisAdoption=false"

end KernelAdmissionChecks

def main (args : List String) : IO UInt32 := do
  match args with
  | [sysroot, output] =>
      KernelAdmissionChecks.run (System.FilePath.mk sysroot) (System.FilePath.mk output)
      return 0
  | _ => throw <| IO.userError "USAGE KernelAdmissionChecks PINNED_SYSROOT FRESH_OUTPUT_DIRECTORY"
