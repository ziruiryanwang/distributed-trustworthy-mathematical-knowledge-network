module

public meta import Lean.Elab.Command
public meta import OwnerUseCommand
public meta import SuccessorExport

/- Trusted local-owner command. No peer source, plugin import, second owner
   environment, or mathematical acceptance. Its local boundary comes only from
   the successful OwnerUse command in the same source module. -/

public meta section
open Lean
open Lean.Elab.Command

namespace OrdinaryLean.SuccessorExportCommand

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"ORDINARY_SUCCESSOR_COMMAND {message}"

def phase (message : String) : IO Unit := do
  let stdout ← IO.getStdout
  stdout.putStrLn s!"ORDINARY_SUCCESSOR_EXPORT_PHASE {message}"
  stdout.flush

def outputPath (raw : String) : IO System.FilePath := do
  let path := System.FilePath.mk raw
  if !path.isAbsolute || path.toString.utf8ByteSize > 32768 then
    fail "ABSOLUTE_BOUNDED_OUTPUT_REQUIRED"
  if path.components.contains "." || path.components.contains ".." then
    fail "DOT_OUTPUT_COMPONENT"
  return path

def requireFresh (path : System.FilePath) : IO Unit := do
  let present ← try
    discard path.symlinkMetadata
    pure true
  catch error =>
    match error with
    | .noFileOrDirectory .. => pure false
    | _ => throw error
  if present then fail "FRESH_OUTPUT_REQUIRED"

/-- The controller pins source, command/helper artifacts, prepared request and
    output path. The same local bound context cannot be inherited as a warrant
    through imports. Target is an exact fully qualified, current-module theorem.
    Successful serialization still yields only untrusted inert claims. -/
def run (owner : Environment) (target : Name) (rawOutput : String) : IO Unit := do
  phase "ENTERED_EXISTING_OWNER_ENVIRONMENT"
  if owner.asyncPrefix?.isSome then fail "TOP_LEVEL_OWNER_REQUIRED"
  let some bound := OwnerUse.getBoundContext? owner | fail "NO_LOCAL_BOUND_CONTEXT"
  if bound.mainModule != owner.mainModule then fail "DIFFERENT_OWNER_MODULE"
  CheckedExtension.requireName target
  if owner.isImportedConst target then fail "CURRENT_MODULE_TARGET_REQUIRED"
  if bound.bindings.any (fun binding => binding.name == target) then
    fail "TARGET_ALREADY_IN_BOUNDARY"
  match owner.toKernelEnv.find? target with
  | some (.thmInfo _) => pure ()
  | _ => fail "NEW_THEOREM_RECORD_REQUIRED"
  let path ← outputPath rawOutput
  requireFresh path
  let exported ← SuccessorExport.selectedAbove owner bound.bindings #[target]
  if exported.selectedUnits == 0 then fail "NEW_UNITS_REQUIRED"
  phase s!"SELECTED_SUCCESSOR_COMPLETED units={exported.selectedUnits} boundaryImports={exported.boundaryImports.size} sourceRecordsEnumerated={exported.sourceRecords} edges={exported.dependencyEdges} scanNodes={exported.scanNodes} unitBytes={exported.unitBytes}"
  let bytes ← SuccessorExport.bundleBytes bound.profileId bound.contextId bound.basisId exported
  let stream ← IO.FS.Handle.mk path .writeNew
  stream.write bytes
  stream.flush
  phase s!"OUTPUT_WRITTEN bytes={bytes.size}"

end OrdinaryLean.SuccessorExportCommand

/-- Export a newly authored exact theorem above this module's successful
    #ordinary_use boundary. The path is controller-selected and fresh. -/
elab "#ordinary_export_above " target:ident output:str : command => do
  let owner ← getEnv
  liftIO <| OrdinaryLean.SuccessorExportCommand.run owner target.getId output.getString
