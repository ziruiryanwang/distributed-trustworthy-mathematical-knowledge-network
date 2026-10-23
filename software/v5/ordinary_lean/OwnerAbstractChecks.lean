module

public meta import OwnerRebind
public meta import Lean.Elab.Command

/- Synthetic construction-matcher controls only. No environment lookup or
   insertion, no imported record treated as a warrant, no receiver operation.
   Exact hypothetical rows and handles are built as inert ConstantInfo values.
   Root selects one compilation; run_cmd performs only these small IO checks. -/

public meta section
open Lean
open Lean.Elab.Command
open OrdinaryLean

namespace OrdinaryLean.OwnerAbstractChecks
open OwnerRebind

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"OWNER_ABSTRACT_MATCHER_FAILED {message}"

def passed (label : String) : IO Unit := do
  let output ← IO.getStdout
  output.putStrLn s!"OWNER_ABSTRACT_MATCHER_PASS {label}"
  output.flush

def accepts (label : String) (expected : MatchKind) (action : IO MatchKind) : IO Unit := do
  if (← action) != expected then fail s!"{label}: wrong match class"
  passed label

def refuses (label marker : String) (action : IO MatchKind) : IO Unit := do
  let observed ← try
    discard action
    pure none
  catch error => pure (some error.toString)
  match observed with
  | none => fail s!"{label}: unexpectedly matched"
  | some message =>
      if (message.splitOn marker).length <= 1 then
        fail s!"{label}: wrong refusal: {message}"
      passed label

def fixtureName : Name := `OwnerAbstractFixture.item
def natType : Expr := .const ``Nat []

def stub (type : Expr := natType) (params : List Name := []) (unsafeFlag := false)
    : ConstantInfo :=
  .axiomInfo { name := fixtureName, levelParams := params, type := type, isUnsafe := unsafeFlag }

def definition (value : Nat := 7) : ConstantInfo :=
  .defnInfo {
    name := fixtureName
    levelParams := []
    type := natType
    value := .lit (.natVal value)
    hints := .regular 1
    safety := .safe
  }

def opaqueValue (value : Nat := 7) : ConstantInfo :=
  .opaqueInfo {
    name := fixtureName
    levelParams := []
    type := natType
    value := .lit (.natVal value)
    isUnsafe := false
  }

def generated : ConstantInfo :=
  .inductInfo {
    name := fixtureName
    levelParams := []
    type := .sort (.succ .zero)
    numParams := 0
    numIndices := 0
    all := [fixtureName]
    ctors := []
    numNested := 0
    isRec := false
    isUnsafe := false
    isReflexive := false
  }

def theoremValue : ConstantInfo :=
  .thmInfo {
    name := fixtureName
    levelParams := []
    type := .const ``True []
    value := .const ``True.intro []
  }

def syntheticId : String :=
  "0000000000000000000000000000000000000000000000000000000000000000"

def ordinaryRow (accepted : ConstantInfo) : IO Row := do
  let payload ← DeclCodec.inventoryRow accepted
  rowOf (Json.arr #[← ExprCodec.encodeName accepted.name, toJson (1 : Nat),
    Json.str syntheticId, payload]) {}

def ordinaryTheoremRow : IO Row := do
  rowOf (Json.arr #[← ExprCodec.encodeName fixtureName, toJson (0 : Nat),
    Json.str syntheticId, ← theoremPayload theoremValue {}]) {}

def basisTheoremRow : IO Json := do
  let full ← ExprCodec.arrayOf (← BootstrapProbe.inventoryRow theoremValue) (some 5)
  return Json.arr #[full[0]!, full[1]!, full[2]!, full[3]!, Json.arr #[]]

def run : IO Unit := do
  let definitionRow ← ordinaryRow definition
  let opaqueRow ← ordinaryRow opaqueValue
  let generatedRow ← ordinaryRow generated
  let theoremRow ← ordinaryTheoremRow
  refuses "ordinary-exact-default-refuses-stub" "NEEDS_DEPENDENCY_SEMANTICS"
    (matchRow stub definitionRow {})
  accepts "ordinary-explicit-definition-handle" .abstractDefinition
    (matchRow stub definitionRow {} .existingAbstract)
  accepts "ordinary-explicit-opaque-handle" .abstractDefinition
    (matchRow stub opaqueRow {} .existingAbstract)
  refuses "ordinary-wrong-type" "ABSTRACT_INTERFACE_MISMATCH"
    (matchRow (stub (.const ``Bool [])) definitionRow {} .existingAbstract)
  refuses "ordinary-wrong-universe-arity" "ABSTRACT_INTERFACE_MISMATCH"
    (matchRow (stub natType [`unexpectedUniverse]) definitionRow {} .existingAbstract)
  refuses "ordinary-different-concrete-body" "EXACT_SEMANTICS_MISMATCH"
    (matchRow (definition 8) definitionRow {} .existingAbstract)
  refuses "ordinary-different-concrete-opaque-body" "EXACT_SEMANTICS_MISMATCH"
    (matchRow (opaqueValue 8) opaqueRow {} .existingAbstract)
  refuses "ordinary-generated-stub" "NEEDS_DEPENDENCY_SEMANTICS"
    (matchRow (stub generated.type) generatedRow {} .existingAbstract)
  refuses "ordinary-unsafe-stub" "UNSAFE_OWNER_RECORD"
    (matchRow (stub natType [] true) definitionRow {} .existingAbstract)
  accepts "ordinary-theorem-class-stays-separate" .theoremInterface
    (matchRow (stub theoremValue.type) theoremRow {} .existingAbstract)
  accepts "ordinary-concrete-class-stays-exact" .exact
    (matchRow definition definitionRow {} .existingAbstract)
  -- Equal encoded universe slots do not erase ordinary parameter-name identity.
  let polymorphic : ConstantInfo := .defnInfo {
    name := fixtureName
    levelParams := [`originalUniverse]
    type := .sort (.succ (.param `originalUniverse))
    value := .sort (.param `originalUniverse)
    hints := .regular 1
    safety := .safe
  }
  let polymorphicRow ← ordinaryRow polymorphic
  refuses "ordinary-wrong-universe-parameter-name" "ABSTRACT_INTERFACE_MISMATCH"
    (matchRow (stub (.sort (.succ (.param `renamedUniverse))) [`renamedUniverse])
      polymorphicRow {} .existingAbstract)

  let basisDefinition ← BootstrapProbe.inventoryRow definition
  let basisOpaque ← BootstrapProbe.inventoryRow opaqueValue
  let basisGenerated ← BootstrapProbe.inventoryRow generated
  let basisTheorem ← basisTheoremRow
  refuses "basis-exact-default-refuses-stub" "NONPERMITTED_AXIOM_OR_INCOMPLETE_RECORD"
    (matchBasisRow stub basisDefinition)
  accepts "basis-explicit-definition-handle" .abstractDefinition
    (matchBasisRow stub basisDefinition .existingAbstract)
  accepts "basis-explicit-opaque-handle" .abstractDefinition
    (matchBasisRow stub basisOpaque .existingAbstract)
  refuses "basis-wrong-type" "BASIS_ABSTRACT_INTERFACE_MISMATCH"
    (matchBasisRow (stub (.const ``Bool [])) basisDefinition .existingAbstract)
  refuses "basis-wrong-universe-arity" "BASIS_ABSTRACT_INTERFACE_MISMATCH"
    (matchBasisRow (stub natType [`unexpectedUniverse]) basisDefinition .existingAbstract)
  refuses "basis-different-concrete-body" "BASIS_SEMANTICS_MISMATCH"
    (matchBasisRow (definition 8) basisDefinition .existingAbstract)
  refuses "basis-generated-stub" "NONPERMITTED_AXIOM_OR_INCOMPLETE_RECORD"
    (matchBasisRow (stub generated.type) basisGenerated .existingAbstract)
  refuses "basis-unsafe-stub" "UNSAFE_OWNER_RECORD"
    (matchBasisRow (stub natType [] true) basisDefinition .existingAbstract)
  accepts "basis-theorem-class-stays-separate" .theoremInterface
    (matchBasisRow (stub theoremValue.type) basisTheorem .existingAbstract)
  accepts "basis-concrete-class-stays-exact" .exact
    (matchBasisRow definition basisDefinition .existingAbstract)
  let output ← IO.getStdout
  output.putStrLn "OWNER_ABSTRACT_MATCHER_CHECKS_PASS checks=22 synthetic_matchers_only=true receiver_acceptance=false"
  output.flush

end OrdinaryLean.OwnerAbstractChecks

run_cmd liftIO OrdinaryLean.OwnerAbstractChecks.run
