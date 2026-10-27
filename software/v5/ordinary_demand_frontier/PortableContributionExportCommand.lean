module

public meta import PortableConstructExportCommand

/- Owner-approved source export only. The selected array may contain new bare
   definitions and theorems. Complete dependency groups still come from the
   unchanged exporter; no scratch signature is promoted into mathematics. -/

public meta section
open Lean
open Lean.Elab.Command

namespace OrdinaryLean.PortableContributionExportCommand

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"PORTABLE_CONTRIBUTION_EXPORT {message}"

def run (owner : Environment) (rawTargets rawOutput : String) : IO Unit := do
  if owner.asyncPrefix?.isSome then fail "TOP_LEVEL_OWNER_REQUIRED"
  let some context := PortableOwnerConstruct.getConstructContext? owner |
    fail "NO_LOCAL_CONSTRUCTION_CONTEXT"
  if context.mainModule != owner.mainModule then fail "DIFFERENT_OWNER_MODULE"
  let targetsPath ← OwnerUse.absolutePath rawTargets
  let (packet, _) ← OwnerUse.readJsonBounded targetsPath 65536
  let rows ← ExprCodec.arrayOf packet
  if rows.isEmpty || rows.size > 32 then fail "TARGET_COUNT_BOUND"
  let mut targets : Array Name := #[]
  for row in rows do
    let name ← ExprCodec.decodeName row
    CheckedExtension.requireName name
    if targets.contains name then fail "DUPLICATE_TARGET"
    if owner.isImportedConst name then fail "CURRENT_MODULE_TARGET_REQUIRED"
    if context.interpretationLabels.any (fun binding => binding.name == name) then
      fail "TARGET_ALREADY_IN_BOUNDARY"
    let some actual := owner.toKernelEnv.find? name | fail "TARGET_NOT_FOUND"
    OwnerRebind.requireSafe actual name
    match actual with
    | .thmInfo _ | .defnInfo _ => pure ()
    | _ => fail "NEW_DEFINITION_OR_THEOREM_REQUIRED"
    targets := targets.push name
  let path ← SuccessorExportCommand.outputPath rawOutput
  SuccessorExportCommand.requireFresh path
  let candidate ← SuccessorExport.selectedDeferred owner context.interpretationLabels
    context.introducedNames targets
  if candidate.exported.selectedUnits == 0 then fail "NEW_UNITS_REQUIRED"
  let bytes ← PortableConstructExportCommand.candidateBundleBytes context.semanticId
    context.contextRoot context.foundationId candidate
  let stream ← IO.FS.Handle.mk path .writeNew
  stream.write bytes
  stream.flush

end OrdinaryLean.PortableContributionExportCommand

elab "#ordinary_export_contribution " targets:str output:str : command => do
  let owner ← getEnv
  liftIO <| OrdinaryLean.PortableContributionExportCommand.run owner
    targets.getString output.getString
