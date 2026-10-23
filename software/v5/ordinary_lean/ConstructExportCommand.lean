module

public meta import Lean.Elab.Command
public meta import OwnerConstructCommand
public meta import SuccessorExportCommand
public meta import SuccessorExport

/- Inert candidate export after explicit scratch construction. Reuse the prior
   bounded fresh-output path, not its exact owner-correspondence contract.
   No environment mutation or mathematical acceptance occurs in this command. -/

public meta section
open Lean
open Lean.Elab.Command

namespace OrdinaryLean.ConstructExportCommand

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"ORDINARY_CONSTRUCT_EXPORT {message}"

def phase (message : String) : IO Unit := do
  let stdout ← IO.getStdout
  stdout.putStrLn s!"ORDINARY_CONSTRUCT_EXPORT_PHASE {message}"
  stdout.flush

/-- The protected controller authenticates the finite prepared interpretation
    labels; the command retrieves them only from this module's construction.
    Imported scratch state is not inherited. The target is a new full theorem,
    not an accepted label or an axiom-shaped construction signature. -/
def run (owner : Environment) (target : Name) (rawOutput : String) : IO Unit := do
  phase "ENTERED_EXISTING_OWNER_ENVIRONMENT mode=receiver-interpreted-candidate"
  if owner.asyncPrefix?.isSome then fail "TOP_LEVEL_OWNER_REQUIRED"
  let some context := OwnerConstruct.getConstructContext? owner |
    fail "NO_LOCAL_CONSTRUCTION_CONTEXT"
  if context.mainModule != owner.mainModule then fail "DIFFERENT_OWNER_MODULE"
  CheckedExtension.requireName target
  if owner.isImportedConst target then fail "CURRENT_MODULE_TARGET_REQUIRED"
  if context.interpretationLabels.any (fun binding => binding.name == target) then
    fail "TARGET_ALREADY_IN_BOUNDARY"
  match owner.toKernelEnv.find? target with
  | some (.thmInfo _) => pure ()
  | _ => fail "NEW_THEOREM_RECORD_REQUIRED"
  let path ← SuccessorExportCommand.outputPath rawOutput
  SuccessorExportCommand.requireFresh path
  let candidate ← SuccessorExport.selectedDeferred owner context.interpretationLabels
    context.introducedNames #[target]
  let exported := candidate.exported
  if exported.selectedUnits == 0 then fail "NEW_UNITS_REQUIRED"
  phase s!"SELECTED_SUCCESSOR_COMPLETED units={exported.selectedUnits} boundaryImports={exported.boundaryImports.size} unresolvedImports={candidate.unresolvedImports.size} sourceRecordsEnumerated={exported.sourceRecords} edges={exported.dependencyEdges} scanNodes={exported.scanNodes} unitBytes={exported.unitBytes}"
  let bytes ← SuccessorExport.candidateBundleBytes context.profileId context.contextId context.basisId candidate
  let stream ← IO.FS.Handle.mk path .writeNew
  stream.write bytes
  stream.flush
  phase s!"OUTPUT_WRITTEN bytes={bytes.size} assurance=INERT_OWNER_EXPORT_NOT_MATHEMATICAL_ACCEPTANCE"

end OrdinaryLean.ConstructExportCommand

/-- Serialize a new complete theorem for independent receiver checking. The
    local authoring environment and scratch signatures are never promoted. -/
elab "#ordinary_export_constructed " target:ident output:str : command => do
  let owner ← getEnv
  liftIO <| OrdinaryLean.ConstructExportCommand.run owner target.getId output.getString
