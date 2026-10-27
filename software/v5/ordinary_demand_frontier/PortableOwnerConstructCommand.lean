module

public meta import OwnerConstruction
public meta import OwnerUseCommand
public meta import Lean.Elab.Command

/- Explicit portable scratch construction, NOT receiver acceptance. V3 optionally
   supplies controller-authenticated installed-name cuts; V2 and the raw group/unit
   grammar remain unchanged. The controller authenticates selected S/F, the
   protected local context and V3 ancestor bindings. Scratch theorem signatures
   remain assumptions. Installed-name cuts assert no semantic correspondence. -/

public meta section
open Lean
open Lean.Elab.Command

namespace OrdinaryLean.PortableOwnerConstruct

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"PORTABLE_OWNER_CONSTRUCT {message}"

def phase (message : String) : IO Unit := do
  let stdout ← IO.getStdout
  stdout.putStrLn s!"PORTABLE_OWNER_CONSTRUCT_PHASE {message}"
  stdout.flush

structure ConstructContext where
  mainModule : Name
  semanticId : String
  contextRoot : String
  foundationId : String
  interpretationLabels : Array OwnerRebind.BoundName
  introducedNames : Array Name
  deriving Inhabited

private initialize constructContextExt : EnvExtension (Option ConstructContext) ←
  registerEnvExtension (pure none) (asyncMode := .local)

def getConstructContext? (env : Environment) : Option ConstructContext :=
  match constructContextExt.getState env with
  | some context => if context.mainModule == env.mainModule then some context else none
  | none => none

/-- All fallible work precedes installation. Canonical bytes/duplicate keys,
    exact file maps and actual S/F/warrant eligibility remain controller checks. -/
def run (owner : Environment) (directoryRaw expectedSemantic expectedContext expectedFoundation : String)
    : IO Environment := do
  if owner.asyncPrefix?.isSome then fail "TOP_LEVEL_OWNER_REQUIRED"
  if (constructContextExt.getState owner).isSome then fail "SECOND_CONSTRUCTION_NOT_SUPPORTED"
  for id in [expectedSemantic, expectedContext, expectedFoundation] do
    discard <| OwnerRebind.identityOf (Json.str id)
  let directory ← OwnerUse.absolutePath directoryRaw
  phase "ENTERED_EXISTING_OWNER_ENVIRONMENT mode=portable-receiver-interpreted-candidate"
  let (header, headerBytes) ← OwnerUse.readJsonBounded (directory / "header.json") 1048576
  let fields ← ExprCodec.jsonResult header.getObj?
  if fields.size != 7 && fields.size != 9 then fail "HEADER_FIELD_CENSUS"
  let schema ← ExprCodec.jsonResult (← OwnerUse.headerField header "schema").getStr?
  let isV3 := schema == "DMKN_OWNER_REQUEST_V3"
  if !isV3 && schema != "DMKN_OWNER_REQUEST_V2" then fail "HEADER_SCHEMA"
  if fields.size != (if isV3 then 9 else 7) then fail "HEADER_FIELD_CENSUS"
  let limits : OwnerRebind.Limits := if isV3 then {
    maxGroups := 32
    maxRows := 4096
    maxTargets := 32
    maxGroupBytes := 1048576
    maxPayloadBytes := 4194304
  } else {}
  let frontierLabels ← if isV3 then do
    -- Root shape is checked here; the protected owner controller authenticates
    -- the root, ancestor plan prefix and exact per-name receiver bindings.
    discard <| OwnerRebind.identityOf (← OwnerUse.headerField header "frontier_root")
    ExprCodec.arrayOf (← OwnerUse.headerField header "frontier_labels")
  else pure #[]
  let semanticId ← OwnerRebind.identityOf (← OwnerUse.headerField header "semantic_id")
  let contextRoot ← OwnerRebind.identityOf (← OwnerUse.headerField header "context_root")
  let foundationId ← OwnerRebind.identityOf (← OwnerUse.headerField header "foundation_id")
  if semanticId != expectedSemantic || contextRoot != expectedContext || foundationId != expectedFoundation then
    fail "HEADER_EXPECTED_IDENTITY_MISMATCH"
  let basisRows ← ExprCodec.arrayOf (← OwnerUse.headerField header "basis_rows")
  let targets ← ExprCodec.arrayOf (← OwnerUse.headerField header "targets")
  let groupCount ← ExprCodec.natOf (← OwnerUse.headerField header "group_count")
  if basisRows.isEmpty || basisRows.size > limits.maxBasisRows ||
      targets.isEmpty || targets.size > limits.maxTargets || groupCount > limits.maxGroups ||
      (isV3 && basisRows.size + frontierLabels.size > limits.maxRows) ||
      headerBytes > limits.maxPayloadBytes then fail "HEADER_COUNT_BOUND"
  let nextGroup ← IO.mkRef 0
  let rawBytes ← IO.mkRef headerBytes
  let readGroup : Nat → IO Json := fun index => do
    if index != (← nextGroup.get) || index >= groupCount then fail "GROUP_READ_SEQUENCE"
    let used ← rawBytes.get
    if used >= limits.maxPayloadBytes then fail "AGGREGATE_RAW_BYTE_BOUND"
    let maximum := min limits.maxGroupBytes (limits.maxPayloadBytes - used)
    let (packet, count) ← OwnerUse.readJsonBounded
      (directory / OwnerUse.groupFilename index) maximum
    rawBytes.set (used + count)
    nextGroup.set (index + 1)
    if (index + 1) % 64 == 0 || index + 1 == groupCount then
      phase s!"GROUPS_READ count={index + 1} rawBytes={used + count}"
    return packet
  -- These legacy internal field NAMES are bookkeeping only: S, local root, F.
  -- No V1 profile identity or old local basis-root formula is interpreted here.
  let prepared : OwnerRebind.Prepared := {
    profileId := semanticId
    contextId := contextRoot
    basisId := foundationId
    basisRows := basisRows
    targets := targets
    groupCount := groupCount
    readGroup := readGroup
  }
  phase s!"HEADER_MATCHED groups={groupCount} basisRows={basisRows.size} targets={targets.size}"
  let constructed ← OwnerConstruction.constructPrepared owner prepared limits frontierLabels
  if (← nextGroup.get) != groupCount then fail "GROUP_READ_CENSUS"
  let context : ConstructContext := {
    mainModule := owner.mainModule
    semanticId := semanticId
    contextRoot := contextRoot
    foundationId := foundationId
    interpretationLabels := constructed.interpretationLabels
    introducedNames := constructed.introducedNames
  }
  let candidate := constructContextExt.setState constructed.environment (some context)
  let used ← rawBytes.get
  phase s!"CONSTRUCTED_READY_FOR_AUTHORING_INSTALL labels={constructed.interpretationLabels.size} introducedNames={constructed.introducedNames.size} introducedSignatures={constructed.introducedSignatures} checkedUnits={constructed.checkedUnits} scanNodes={constructed.scanNodes} encodedNodes={constructed.encodedNodes} payloadBytes={constructed.payloadBytes} rawBytes={used}"
  return candidate

end OrdinaryLean.PortableOwnerConstruct

elab "#ordinary_construct_portable " directory:str semantic:str context:str foundation:str : command => do
  let owner ← getEnv
  let candidate ← liftIO <| OrdinaryLean.PortableOwnerConstruct.run owner directory.getString
    semantic.getString context.getString foundation.getString
  modifyEnv (fun _ => candidate)
