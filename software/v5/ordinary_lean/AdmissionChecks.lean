import CheckedExtension

/- Root-run targeted checks, not a benchmark or network trust bootstrap.
   Init is explicitly an OWNER-SELECTED CONDITIONAL TEST FIXTURE. Its imported
   records are NOT newly warranted by importing them. No456-unit seed replay.
   The runtime harness must pin the supplied sysroot and this source closure. -/

open Lean OrdinaryLean
namespace AdmissionChecks

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"ADMISSION_CHECK_FAILED {message}"

def ensure (condition : Bool) (message : String) : IO Unit := do
  if !condition then fail message

def passed (label : String) : IO Unit :=
  IO.println s!"ADMISSION_CHECK_PASS {label}"

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

def natType : Expr := .const ``Nat []
def identityName : Name := `OrdinaryAdmissionTest.identity
def polyName : Name := `OrdinaryAdmissionTest.polyIdentity
def hintedName : Name := `OrdinaryAdmissionTest.opaqueHintIdentity
def opaqueName : Name := `OrdinaryAdmissionTest.opaqueSeven
def theoremName : Name := `OrdinaryAdmissionTest.identity_eq
def groupName : Name := `OrdinaryAdmissionTest.Choice
def badName : Name := `OrdinaryAdmissionTest.badProof
def missingName : Name := `OrdinaryAdmissionTest.missingDefinition

def identityDecl (name : Name) (hint : ReducibilityHints) : Declaration :=
  .defnDecl {
    name := name
    levelParams := []
    type := .forallE `input natType natType .default,
    value := .lam `input natType (.bvar 0) .default,
    hints := hint
    safety := .safe
  }

def polyDecl : Declaration :=
  let u := `originalUniverse
  .defnDecl {
    name := polyName
    levelParams := [u]
    type := .forallE `carrier (.sort (.param u))
      (.forallE `element (.bvar 0) (.bvar 1) .default) .implicit,
    value := .lam `carrier (.sort (.param u))
      (.lam `element (.bvar 0) (.bvar 0) .default) .implicit,
    hints := .regular 17
    safety := .safe
    all := [polyName, `OrdinaryAdmissionTest.metadataCompanion]
  }

def lawDecl : Declaration :=
  let value := Expr.bvar 0
  let lhs := Expr.app (.const identityName []) value
  let equality := mkApp3 (.const ``Eq [Level.succ .zero]) natType lhs value
  let proof := mkApp2 (.const ``Eq.refl [Level.succ .zero]) natType value
  .thmDecl {
    name := theoremName
    levelParams := []
    type := .forallE `value natType equality .default,
    value := .lam `value natType proof .default
  }

def opaqueDecl : Declaration :=
  .opaqueDecl {
    name := opaqueName
    levelParams := []
    type := natType
    value := .lit (.natVal 7)
    isUnsafe := false
  }

def choiceDecl : Declaration :=
  .inductDecl [] 0 [{
    name := groupName
    type := .sort (.succ .zero)
    ctors := [
      { name := .str groupName "left", type := .const groupName [] },
      { name := .str groupName "right", type := .forallE `payload natType (.const groupName []) .default }
    ]
  }] false

def badDecl : Declaration :=
  .thmDecl {
    name := badName
    levelParams := []
    type := .const ``False []
    value := .const ``True.intro []
  }

def missingDecl : Declaration :=
  .defnDecl {
    name := missingName
    levelParams := []
    type := natType
    value := .const `OrdinaryAdmissionTest.unprovided []
    hints := .regular 1
    safety := .safe
  }

def fixtureAllowed : Std.HashSet Name := Id.run do
  let mut names : Std.HashSet Name := {}
  for name in [``Nat, ``Eq, ``Eq.refl, ``False, ``True, ``True.intro] do
    names := names.insert name
  return names

def lookup (env : Environment) (name : Name) : IO ConstantInfo := do
  let some info := env.toKernelEnv.find? name | fail s!"fixture output missing {name}"
  return info

/-- Owner construction tool for expected records; not the tested admission path. -/
def producerUnit (env : Environment) (decl : Declaration)
    : IO (Environment × Json × DeclCodec.DecodedUnit) := do
  let next ← match env.addDeclCore 1000000 1000 decl none (doCheck := true) with
    | .ok next => pure next
    | .error _ => fail "owner fixture kernel construction rejected"
  -- This fixture has no nested inductives; all generated names are in getNames.
  let mut inventory := #[]
  for name in decl.getNames do inventory := inventory.push (← lookup next name)
  let packet ← DeclCodec.encodeUnit decl inventory
  let fields ← ExprCodec.arrayOf packet (some 3)
  let expected ← ExprCodec.arrayOf fields[2]!
  return (next, packet, { decl, expected })

def ordinaryClaim (decl : Declaration) : IO DeclCodec.DecodedUnit := do
  let info ← match decl with
    | .defnDecl d => pure (.defnInfo d)
    | .thmDecl d => pure (.thmInfo d)
    | .opaqueDecl d => pure (.opaqueInfo d)
    | _ => fail "test ordinary claim kind"
  return { decl, expected := #[← DeclCodec.inventoryRow info] }

def checkDirectTypeMismatch (parent : Environment) : IO Unit := do
  match parent.addDeclCore 1000000 1000 badDecl none (doCheck := true) with
  | .error (.declTypeMismatch ..) => passed "invalid-proof-is-actual-type-mismatch"
  | .error (.exprTypeMismatch ..) => passed "invalid-proof-is-actual-type-mismatch"
  | .error _ => fail "invalid proof hit unrelated kernel/resource failure"
  | .ok _ => fail "invalid proof unexpectedly kernel-checked"

def checkMetadata (env : Environment) : IO Unit := do
  let .defnInfo identity ← lookup env identityName | fail "identity kind"
  ensure (identity.hints == .abbrev) "abbrev hint changed"
  let .forallE binder _ _ bi := identity.type | fail "identity binder shape"
  ensure (binder == `input && bi == .default) "named argument metadata changed"
  let .defnInfo poly ← lookup env polyName | fail "poly kind"
  ensure (poly.levelParams == [`originalUniverse]) "original universe names changed"
  ensure (poly.hints == .regular 17) "regular height changed"
  ensure (poly.all == [polyName, `OrdinaryAdmissionTest.metadataCompanion]) "all metadata changed"
  let .forallE carrier _ body bi := poly.type | fail "poly carrier shape"
  ensure (carrier == `carrier && bi == .implicit) "implicit carrier metadata changed"
  let .forallE element _ _ elementInfo := body | fail "poly element shape"
  ensure (element == `element && elementInfo == .default) "element binder changed"
  let .defnInfo hinted ← lookup env hintedName | fail "opaque-hint kind"
  ensure (hinted.hints == .opaque) "opaque definition hint changed"
  let .opaqueInfo opaqueInfo ← lookup env opaqueName | fail "opaque declaration kind"
  ensure (Expr.equal opaqueInfo.value (.lit (.natVal 7))) "native numeral changed"
  let .thmInfo law ← lookup env theoremName | fail "law kind"
  let .forallE value _ _ _ := law.type | fail "law binder shape"
  ensure (value == `value) "theorem named argument changed"
  let .inductInfo group ← lookup env groupName | fail "group kind"
  ensure (group.ctors == [.str groupName "left", .str groupName "right"])
    "group constructor order changed"
  passed "actual-kernel-metadata-fidelity"

def tamperConstructor (unit : DeclCodec.DecodedUnit) : IO DeclCodec.DecodedUnit := do
  let mut expected := unit.expected
  let mut changed := false
  for i in [:expected.size] do
    let fields ← ExprCodec.arrayOf expected[i]! (some 5)
    if !changed && (← ExprCodec.natOf fields[1]!) == 5 then
      let details ← ExprCodec.arrayOf fields[4]! (some 5)
      let count ← ExprCodec.natOf details[3]!
      let details := details.set! 3 (ExprCodec.num (count + 1))
      expected := expected.set! i (ExprCodec.arr (fields.set! 4 (ExprCodec.arr details)))
      changed := true
  ensure changed "no constructor row tampered"
  return { unit with expected }

def run (sysroot : System.FilePath) : IO Unit := do
  -- Explicit search root only: do not inherit LEAN_PATH or LEAN_SYSROOT.
  Lean.searchPathRef.set [sysroot / "lib" / "lean"]
  IO.println "ADMISSION_FIXTURE owner-selected-Init conditional=true networkParentWarrant=false"
  let parent ← Lean.importModules #[{ module := `Init }] {} 0
    (plugins := #[]) (loadExts := false) (level := .private)
  ensure parent.toKernelEnv.quotInit "fixture quotient state"
  let before ← CheckedExtension.stageTwoNames parent.toKernelEnv 1000
  for name in [identityName, polyName, hintedName, opaqueName, theoremName, groupName, badName, missingName] do
    ensure (parent.toKernelEnv.find? name).isNone "fixture names pre-exist"

  let mut producer := parent
  let mut allowed := fixtureAllowed
  let mut decoded : Array DeclCodec.DecodedUnit := #[]
  let declarations := #[identityDecl identityName .abbrev, polyDecl,
    identityDecl hintedName .opaque, opaqueDecl, lawDecl, choiceDecl]
  for decl in declarations do
    let (next, packet, _) ← producerUnit producer decl
    let unit ← DeclCodec.decodeUnit allowed packet
    for name in ← DeclCodec.expectedNames unit.expected do allowed := allowed.insert name
    decoded := decoded.push unit
    producer := next
  let checked ← CheckedExtension.checkBatch parent decoded
  let some firstUnit := decoded[0]? | fail "missing first fixture unit"
  let some groupUnit := decoded[5]? | fail "missing group fixture unit"
  ensure (checked.unitsChecked == declarations.size) "positive batch unit count"
  checkMetadata checked.environment
  passed "decode-and-check-actual-six-unit-batch"

  let bad ← ordinaryClaim badDecl
  checkDirectTypeMismatch parent
  expectReject "invalid-proof-admission" "KERNEL_REJECTED_OR_RESOURCE_LIMIT" do
    discard <| CheckedExtension.checkBatch parent #[bad]

  let axiomDeclValue : Declaration := .axiomDecl {
    name := `OrdinaryAdmissionTest.newAxiom
    levelParams := []
    type := .const ``False []
    isUnsafe := false
  }
  expectReject "axiom-encoding" "AXIOM_QUOT_OR_MUTUAL_UNSAFE_EXTENSION" do
    discard <| DeclCodec.encodeDescriptor axiomDeclValue
  expectReject "axiom-admission" "AXIOM_QUOT_OR_UNSUPPORTED_DECLARATION" do
    discard <| CheckedExtension.checkBatch parent #[{ decl := axiomDeclValue, expected := #[] }]

  let .defnDecl identity := identityDecl identityName .abbrev | fail "fixture definition shape"
  let unsafeDecl := Declaration.defnDecl {
    identity with
    name := `OrdinaryAdmissionTest.unsafeId
    safety := .unsafe
    all := [`OrdinaryAdmissionTest.unsafeId]
  }
  expectReject "unsafe-encoding" "UNSAFE_DEFINITION" do
    discard <| DeclCodec.encodeDescriptor unsafeDecl
  expectReject "unsafe-admission" "UNSAFE_OR_PARTIAL" do
    discard <| CheckedExtension.checkBatch parent #[{ decl := unsafeDecl, expected := #[] }]

  expectReject "overwrite-admission" "OVERWRITE_OR_DUPLICATE" do
    discard <| CheckedExtension.checkBatch checked.environment #[firstUnit]
  let firstPacket ← DeclCodec.encodeUnit firstUnit.decl #[← lookup producer identityName]
  expectReject "overwrite-decoder" "INVENTORY_NAME_OVERWRITE" do
    discard <| DeclCodec.decodeUnit allowed firstPacket

  let missing ← ordinaryClaim missingDecl
  let missingPacket ← DeclCodec.encodeUnit missingDecl #[
    match missingDecl with | .defnDecl d => .defnInfo d | _ => unreachable!]
  expectReject "missing-reference-decoder" "UNBOUND_REFERENCE" do
    discard <| DeclCodec.decodeUnit fixtureAllowed missingPacket
  expectReject "missing-reference-admission" "UNGROUNDED_REFERENCE" do
    discard <| CheckedExtension.checkBatch parent #[missing]

  let tampered ← tamperConstructor groupUnit
  expectReject "generated-constructor-inventory" "GENERATED_RECORD_MISMATCH" do
    discard <| CheckedExtension.checkBatch parent #[tampered]

  expectReject "failed-batch-no-success-prefix" "KERNEL_REJECTED_OR_RESOURCE_LIMIT" do
    discard <| CheckedExtension.checkBatch parent #[firstUnit, bad]
  let after ← CheckedExtension.stageTwoNames parent.toKernelEnv 1000
  ensure (before.size == after.size) "failed batch changed parent stage-two census"
  for name in [identityName, polyName, hintedName, opaqueName, theoremName, groupName, badName, missingName] do
    ensure (parent.toKernelEnv.find? name).isNone "failed batch leaked into immutable parent"
  passed "immutable-parent-preserved"
  IO.println "ADMISSION_CHECKS_COMPLETE conditionalFixtureOnly=true publicDeployment=false"

end AdmissionChecks

def main (args : List String) : IO UInt32 := do
  match args with
  | [sysroot] =>
      AdmissionChecks.run (System.FilePath.mk sysroot)
      return 0
  | _ => throw <| IO.userError "USAGE AdmissionChecks PINNED_LEAN_SYSROOT"
