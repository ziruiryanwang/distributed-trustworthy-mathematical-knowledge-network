module

public meta import OwnerConstruction
public meta import OwnerUseCommand
public meta import Lean.Elab.Command

/- Explicit scratch construction, NOT mathematical acceptance or semantic
   correspondence with the receiver. The controller authenticates the prepared
   request and exact receiver identities. Introduced theorem signatures are
   local assumptions only; every new successor proof is checked independently
   against the actual receiver context. No peer executable source is loaded. -/

public meta section
open Lean
open Lean.Elab.Command

namespace OrdinaryLean.OwnerConstruct

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"ORDINARY_OWNER_CONSTRUCT {message}"

def phase (message : String) : IO Unit := do
  let stdout ← IO.getStdout
  stdout.putStrLn s!"ORDINARY_OWNER_CONSTRUCT_PHASE {message}"
  stdout.flush

/-- Same-module, nonpersistent construction bookkeeping. The finite labels
    describe receiver interpretation, not equality to the owner's definitions.
    Neither these labels nor the scratch environment confer receiver authority. -/
structure ConstructContext where
  mainModule : Name
  profileId : String
  contextId : String
  basisId : String
  interpretationLabels : Array OwnerRebind.BoundName
  introducedNames : Array Name
  deriving Inhabited

private initialize constructContextExt : EnvExtension (Option ConstructContext) ←
  registerEnvExtension (pure none) (asyncMode := .local)

def getConstructContext? (env : Environment) : Option ConstructContext :=
  match constructContextExt.getState env with
  | some context => if context.mainModule == env.mainModule then some context else none
  | none => none

/-- All fallible request reads, construction and diagnostics precede the single
    final command-state installation below. Canonical bytes, duplicate keys,
    aliases and the exact complete file map remain controller checks. -/
def run (owner : Environment) (directoryRaw expectedProfile expectedContext expectedBasis : String)
    : IO Environment := do
  if owner.asyncPrefix?.isSome then fail "TOP_LEVEL_OWNER_REQUIRED"
  if (constructContextExt.getState owner).isSome then fail "SECOND_CONSTRUCTION_NOT_SUPPORTED"
  for id in [expectedProfile, expectedContext, expectedBasis] do
    discard <| OwnerRebind.identityOf (Json.str id)
  let directory ← OwnerUse.absolutePath directoryRaw
  phase "ENTERED_EXISTING_OWNER_ENVIRONMENT mode=receiver-interpreted-candidate"
  let limits : OwnerRebind.Limits := {}
  let (header, headerBytes) ← OwnerUse.readJsonBounded (directory / "header.json") 1048576
  let fields ← ExprCodec.jsonResult header.getObj?
  if fields.size != 7 then fail "HEADER_FIELD_CENSUS"
  if (← ExprCodec.jsonResult (← OwnerUse.headerField header "schema").getStr?) !=
      "DMKN_OWNER_REQUEST_V1" then fail "HEADER_SCHEMA"
  let profileId ← OwnerRebind.identityOf (← OwnerUse.headerField header "profile_id")
  let contextId ← OwnerRebind.identityOf (← OwnerUse.headerField header "context_id")
  let basisId ← OwnerRebind.identityOf (← OwnerUse.headerField header "basis_id")
  if profileId != expectedProfile || contextId != expectedContext || basisId != expectedBasis then
    fail "HEADER_EXPECTED_IDENTITY_MISMATCH"
  let basisRows ← ExprCodec.arrayOf (← OwnerUse.headerField header "basis_rows")
  let targets ← ExprCodec.arrayOf (← OwnerUse.headerField header "targets")
  let groupCount ← ExprCodec.natOf (← OwnerUse.headerField header "group_count")
  if basisRows.isEmpty || basisRows.size > limits.maxBasisRows ||
      targets.isEmpty || targets.size > limits.maxTargets || groupCount > limits.maxGroups ||
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
  let prepared : OwnerRebind.Prepared := {
    profileId := profileId
    contextId := contextId
    basisId := basisId
    basisRows := basisRows
    targets := targets
    groupCount := groupCount
    readGroup := readGroup
  }
  phase s!"HEADER_MATCHED groups={groupCount} basisRows={basisRows.size} targets={targets.size}"
  let constructed ← OwnerConstruction.constructPrepared owner prepared limits
  if (← nextGroup.get) != groupCount then fail "GROUP_READ_CENSUS"
  let context : ConstructContext := {
    mainModule := owner.mainModule
    profileId := profileId
    contextId := contextId
    basisId := basisId
    interpretationLabels := constructed.interpretationLabels
    introducedNames := constructed.introducedNames
  }
  let candidate := constructContextExt.setState constructed.environment (some context)
  let used ← rawBytes.get
  phase s!"CONSTRUCTED_READY_FOR_AUTHORING_INSTALL labels={constructed.interpretationLabels.size} introducedNames={constructed.introducedNames.size} introducedSignatures={constructed.introducedSignatures} checkedUnits={constructed.checkedUnits} scanNodes={constructed.scanNodes} encodedNodes={constructed.encodedNodes} payloadBytes={constructed.payloadBytes} rawBytes={used}"
  return candidate

end OrdinaryLean.OwnerConstruct

/-- Construct scratch handles for selected accepted methods. Compilation of the
    resulting owner module is not a warrant; use the independent receiver. -/
elab "#ordinary_construct " directory:str profile:str context:str basis:str : command => do
  let owner ← getEnv
  let candidate ← liftIO <| OrdinaryLean.OwnerConstruct.run owner directory.getString
    profile.getString context.getString basis.getString
  modifyEnv (fun _ => candidate)
