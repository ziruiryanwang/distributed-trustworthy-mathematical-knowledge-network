module

public meta import OwnerRebind
public meta import Lean.Elab.Command

/- Trusted owner-project authoring command, NOT a mathematical acceptance
   endpoint. The controller authenticates the exact accepted context and every
   prepared file, pins this helper/runtime, and keeps those files immutable.
   Identity strings here are conditional labels, not self-proving warrants.
   Final successor admission independently checks the resulting inert proof. -/

public meta section
open Lean
open Lean.Elab.Command

namespace OrdinaryLean.OwnerUse

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"ORDINARY_OWNER_USE {message}"

def phase (message : String) : IO Unit := do
  let stdout ← IO.getStdout
  stdout.putStrLn s!"ORDINARY_OWNER_USE_PHASE {message}"
  stdout.flush

def absolutePath (raw : String) : IO System.FilePath := do
  let path := System.FilePath.mk raw
  if !path.isAbsolute || path.toString.utf8ByteSize > 32768 then
    fail "ABSOLUTE_BOUNDED_PATH_REQUIRED"
  if path.components.contains "." || path.components.contains ".." then
    fail "DOT_PATH_COMPONENT"
  return path

/-- Source-module-local correspondence for successor construction. This is not
    persisted in oleans, inherited on import, or accepted as receiver authority.
    The binding map includes the fixed basis and selected semantic closure. -/
structure BoundContext where
  mainModule : Name
  profileId : String
  contextId : String
  basisId : String
  bindings : Array OwnerRebind.BoundName
  deriving Inhabited

private initialize boundContextExt : EnvExtension (Option BoundContext) ←
  registerEnvExtension (pure none) (asyncMode := .local)

/-- Read authoring correspondence only in its original source module. The
    public getter is plumbing; arbitrary owner code is not a trust boundary. -/
def getBoundContext? (env : Environment) : Option BoundContext :=
  match boundContextExt.getState env with
  | some context => if context.mainModule == env.mainModule then some context else none
  | none => none

/-- Raw size is bounded before this preflight, and this preflight precedes
    Json.parse. Duplicate-key rejection, canonical bytes, file alias policy,
    complete file census and exact authentication remain controller duties. -/
def lexicalPreflight (bytes : ByteArray) : IO Unit := do
  let mut stack : Array UInt8 := #[]
  let mut quoted := false
  let mut escaped := false
  let mut i := 0
  while i < bytes.size do
    let byte := bytes[i]!.toNat
    if quoted then
      if byte < 32 then fail "JSON_STRING_CONTROL"
      if escaped then escaped := false
      else if byte == 92 then escaped := true
      else if byte == 34 then quoted := false
      i := i + 1
      continue
    if byte == 34 then quoted := true
    else if byte == 91 || byte == 123 then
      if stack.size >= 64 then fail "JSON_DEPTH_BOUND"
      stack := stack.push bytes[i]!
    else if byte == 93 || byte == 125 then
      if stack.isEmpty || stack.back!.toNat != (if byte == 93 then 91 else 123) then
        fail "JSON_BRACKETS"
      stack := stack.pop
    else if byte >= 48 && byte <= 57 then
      let start := i
      let mut value := 0
      while i < bytes.size && bytes[i]!.toNat >= 48 && bytes[i]!.toNat <= 57 do
        if i - start >= 20 then fail "JSON_INTEGER_DIGITS"
        value := value * 10 + (bytes[i]!.toNat - 48)
        if value > 18446744073709551615 then fail "JSON_UINT64"
        i := i + 1
      if i - start > 1 && bytes[start]!.toNat == 48 then fail "JSON_LEADING_ZERO"
      continue
    else if ![9, 10, 13, 32, 44, 58].contains byte then
      fail "JSON_LEXICAL_TOKEN"
    i := i + 1
  if quoted || escaped || !stack.isEmpty then fail "JSON_UNTERMINATED"

def readJsonBounded (path : System.FilePath) (maximum : Nat) : IO (Json × Nat) := do
  if maximum == 0 || (← path.metadata).byteSize.toNat > maximum then
    fail "REQUEST_FILE_BYTE_BOUND"
  let handle ← IO.FS.Handle.mk path .read
  let mut bytes : ByteArray := ⟨#[]⟩
  while true do
    let chunk ← handle.read (USize.ofNat (min 65536 (maximum + 1 - bytes.size)))
    if chunk.isEmpty then break
    bytes := bytes ++ chunk
    if bytes.size > maximum then fail "REQUEST_FILE_BYTE_BOUND"
  if bytes.isEmpty then fail "REQUEST_FILE_EMPTY"
  lexicalPreflight bytes
  let some text := String.fromUTF8? bytes | fail "REQUEST_FILE_UTF8"
  if text.toUTF8 != bytes then fail "REQUEST_FILE_UTF8_CANONICAL"
  match Json.parse text with
  | .ok value => return (value, bytes.size)
  | .error _ => fail "REQUEST_FILE_JSON"

def headerField (header : Json) (key : String) : IO Json :=
  ExprCodec.jsonResult (header.getObjVal? key)

/-- Numbered filenames are chosen here, never read from peer JSON. -/
def groupFilename (index : Nat) : String :=
  let digits := toString index
  let padding := String.ofList (List.replicate (5 - digits.length) '0')
  s!"group-{padding}{digits}.json"

/-- Construct a complete candidate without mutating command state. Only the
    final elaborator below installs it, after all potentially failing IO. -/
def run (owner : Environment) (directoryRaw expectedProfile expectedContext expectedBasis : String)
    : IO Environment := do
  if owner.asyncPrefix?.isSome then fail "TOP_LEVEL_OWNER_REQUIRED"
  if (boundContextExt.getState owner).isSome then fail "SECOND_USE_NOT_SUPPORTED"
  for id in [expectedProfile, expectedContext, expectedBasis] do
    discard <| OwnerRebind.identityOf (Json.str id)
  let directory ← absolutePath directoryRaw
  phase "ENTERED_EXISTING_OWNER_ENVIRONMENT"
  let limits : OwnerRebind.Limits := {}
  let (header, headerBytes) ← readJsonBounded (directory / "header.json") 1048576
  let fields ← ExprCodec.jsonResult header.getObj?
  if fields.size != 7 then fail "HEADER_FIELD_CENSUS"
  if (← ExprCodec.jsonResult (← headerField header "schema").getStr?) !=
      "DMKN_OWNER_REQUEST_V1" then fail "HEADER_SCHEMA"
  let profileId ← OwnerRebind.identityOf (← headerField header "profile_id")
  let contextId ← OwnerRebind.identityOf (← headerField header "context_id")
  let basisId ← OwnerRebind.identityOf (← headerField header "basis_id")
  if profileId != expectedProfile || contextId != expectedContext || basisId != expectedBasis then
    fail "HEADER_EXPECTED_IDENTITY_MISMATCH"
  let basisRows ← ExprCodec.arrayOf (← headerField header "basis_rows")
  let targets ← ExprCodec.arrayOf (← headerField header "targets")
  let groupCount ← ExprCodec.natOf (← headerField header "group_count")
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
    let (packet, count) ← readJsonBounded (directory / groupFilename index) maximum
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
  let rebound ← OwnerRebind.rebindPrepared owner prepared limits
  if (← nextGroup.get) != groupCount then fail "GROUP_READ_CENSUS"
  let context : BoundContext := {
    mainModule := owner.mainModule
    profileId := profileId
    contextId := contextId
    basisId := basisId
    bindings := rebound.bindings
  }
  let candidate := boundContextExt.setState rebound.environment (some context)
  let used ← rawBytes.get
  phase s!"REBOUND_READY_FOR_AUTHORING_INSTALL interfaces={rebound.interfaceMatched} exact={rebound.exactMatched} checkedUnits={rebound.checkedUnits} addedNames={rebound.addedNames.size} rawBytes={used}"
  return candidate

end OrdinaryLean.OwnerUse

/-- Owner-selected prepared directory and expected identities. This command
    offers conditional authoring support, not peer or mathematical authority. -/
elab "#ordinary_use " directory:str profile:str context:str basis:str : command => do
  let owner ← getEnv
  let candidate ← liftIO <| OrdinaryLean.OwnerUse.run owner directory.getString
    profile.getString context.getString basis.getString
  modifyEnv (fun _ => candidate)
