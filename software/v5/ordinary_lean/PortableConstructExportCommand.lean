module

public meta import Lean.Elab.Command
public meta import PortableOwnerConstructCommand
public meta import SuccessorExportCommand
public meta import SuccessorExport

/- Portable wrapper for unchanged selectedDeferred/raw unit serialization.
   The new V2 labels are explicit S/F/local-context roots. Complete new units
   remain inert candidates requiring protected receiver resolution/checking. -/

public meta section
open Lean
open Lean.Elab.Command

namespace OrdinaryLean.PortableConstructExportCommand

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"PORTABLE_CONSTRUCT_EXPORT {message}"

def phase (message : String) : IO Unit := do
  let stdout ← IO.getStdout
  stdout.putStrLn s!"PORTABLE_CONSTRUCT_EXPORT_PHASE {message}"
  stdout.flush

/-- Same complete candidate payload and resource checks as V1; distinct schema
    and explicit portable labels. Unresolved names are not accepted imports. -/
def candidateBundleBytes (semanticId contextRoot foundationId : String)
    (candidate : SuccessorExport.CandidateExported) (limits : SuccessorExport.Limits := {})
    : IO ByteArray := do
  for identity in [semanticId, contextRoot, foundationId] do
    discard <| OwnerRebind.identityOf (Json.str identity)
  let exported := candidate.exported
  if exported.boundaryImports.size + candidate.unresolvedImports.size > limits.maxBoundaryNames then
    fail "BOUNDARY_COUNT"
  let targets ← exported.targets.mapM (fun name => ExprCodec.encodeName name)
  let imports ← exported.boundaryImports.mapM (fun binding => do
    pure <| Json.arr #[← ExprCodec.encodeName binding.name, Json.str binding.symbolId])
  let unresolved ← candidate.unresolvedImports.mapM (fun name => ExprCodec.encodeName name)
  let statistics := Json.mkObj [
    ("source_records_enumerated", toJson exported.sourceRecords),
    ("selected_units", toJson exported.selectedUnits),
    ("dependency_edges", toJson exported.dependencyEdges),
    ("scan_nodes", toJson exported.scanNodes),
    ("unit_json_bytes", toJson exported.unitBytes),
    ("boundary_imports", toJson exported.boundaryImports.size),
    ("unresolved_imports", toJson candidate.unresolvedImports.size)]
  let packet := Json.mkObj [
    ("schema", Json.str "DMKN_ORDINARY_CANDIDATE_BUNDLE_V2"),
    ("assurance", Json.str "INERT_OWNER_EXPORT_NOT_MATHEMATICAL_ACCEPTANCE"),
    ("semantic_id", Json.str semanticId),
    ("context_root", Json.str contextRoot),
    ("foundation_id", Json.str foundationId),
    ("targets", Json.arr targets),
    ("boundary_imports", Json.arr imports),
    ("unresolved_imports", Json.arr unresolved),
    ("units", Json.arr exported.units),
    ("stats", statistics)]
  let bytes := packet.compress.toUTF8
  if bytes.size > limits.maxBundleBytes then fail "BUNDLE_BYTE_BOUND"
  return bytes

def run (owner : Environment) (target : Name) (rawOutput : String) : IO Unit := do
  phase "ENTERED_EXISTING_OWNER_ENVIRONMENT mode=portable-receiver-interpreted-candidate"
  if owner.asyncPrefix?.isSome then fail "TOP_LEVEL_OWNER_REQUIRED"
  let some context := PortableOwnerConstruct.getConstructContext? owner |
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
  let bytes ← candidateBundleBytes context.semanticId context.contextRoot context.foundationId candidate
  let stream ← IO.FS.Handle.mk path .writeNew
  stream.write bytes
  stream.flush
  phase s!"OUTPUT_WRITTEN bytes={bytes.size} assurance=INERT_OWNER_EXPORT_NOT_MATHEMATICAL_ACCEPTANCE"

end OrdinaryLean.PortableConstructExportCommand

elab "#ordinary_export_constructed_portable " target:ident output:str : command => do
  let owner ← getEnv
  liftIO <| OrdinaryLean.PortableConstructExportCommand.run owner target.getId output.getString
