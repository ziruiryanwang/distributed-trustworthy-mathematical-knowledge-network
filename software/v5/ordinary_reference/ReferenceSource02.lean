import ReferenceEnvironment

/- Ordinary source extraction over exact protected local artifacts. The source
   compiler and this exporter produce inert candidates, never mathematical
   warrants. No plugin/extension initialization occurs during extraction. The
   controller authenticates every plan/part and replies from the actual current
   owner intersected with the explicitly usable reference frontier. -/

open Lean

namespace OrdinaryLean.ReferenceSource

def frameMaximum : Nat := 1048576
def protocolMaximum : Nat := 33554432
def lookupMaximum : Nat := 65536

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"ORDINARY_REFERENCE_SOURCE {message}"

def limits : Export.Limits :=
  { maxTargets := 32
    maxUnits := 32
    maxUnitBytes := 4194304
    maxOutputBytes := 4194304
    maxScanNodes := 2097152
    codec := {
      maxUnitNodes := 131072
      expr := {
        maxExprs := 131072
        maxLevels := 131072 } } }

def parseFrame (bytes : ByteArray) : IO Json := do
  if bytes.isEmpty || bytes.size > frameMaximum then fail "FRAME_BYTE_BOUND"
  BaselineArtifacts.lexicalPreflight bytes
  let some text := String.fromUTF8? bytes | fail "FRAME_UTF8"
  if text.toUTF8 != bytes then fail "FRAME_UTF8_CANONICAL"
  ExprCodec.jsonResult (Json.parse text)

def charge (used : IO.Ref Nat) (count : Nat) : IO Unit := do
  let before ← used.get
  if before + count > protocolMaximum then fail "PROTOCOL_BYTE_BOUND"
  used.set (before + count)

def sendFrame (stdout : IO.FS.Stream) (used : IO.Ref Nat) (packet : Json) : IO Unit := do
  let bytes := packet.compress.toUTF8
  if bytes.isEmpty || bytes.size > frameMaximum then fail "OUTBOUND_FRAME_BOUND"
  charge used (bytes.size + 1)
  stdout.write bytes
  stdout.write ("\n".toUTF8)
  stdout.flush

def receiveFrame (stdin : IO.FS.Stream) (used : IO.Ref Nat) : IO Json := do
  let mut bytes : ByteArray := ⟨#[]⟩
  while true do
    let chunk ← stdin.read 1
    if chunk.isEmpty then fail "REPLY_EOF"
    if chunk.size != 1 then fail "REPLY_READ_CENSUS"
    charge used 1
    let byte := chunk[0]!
    if byte.toNat == 10 then break
    if byte.toNat == 13 then fail "REPLY_CR_FORBIDDEN"
    if bytes.size >= frameMaximum then fail "REPLY_FRAME_BOUND"
    bytes := bytes.push byte
  parseFrame bytes

def authorModule (raw : Json) : IO Name := do
  let name ← ExprCodec.decodeName raw
  match name with
  | .str .anonymous component =>
      if !component.startsWith "DMKNAuthor_" then fail "AUTHOR_MODULE_PREFIX"
      discard <| ReferenceEnvironment.identityOf (.str (component.drop 11 |>.toString))
      return name
  | _ => fail "TOP_LEVEL_AUTHOR_MODULE_REQUIRED"

def authorParts (raw : Json) (name : Name) (plan : ReferenceEnvironment.Plan)
    (forbidden : Array System.FilePath) : IO (Array System.FilePath) := do
  let rows ← ExprCodec.arrayOf raw (some 5)
  let mut paths := #[]
  let mut keys := plan.original.pathKeys
  for item in plan.generated do
    let some arts := plan.artifacts.find? item.moduleName | fail "GENERATED_MAP_MISSING"
    for group in arts.toArrays do
      for path in group do
        keys := keys.insert (BaselineArtifacts.pathKey (← BaselineArtifacts.reportPath path))
  for path in forbidden do keys := keys.insert (BaselineArtifacts.pathKey path)
  let mut total := 0
  for row in rows do
    ReferenceEnvironment.exactObject row #["path", "bytes", "sha256"]
    let path ← ReferenceEnvironment.absolutePath (← ExprCodec.jsonResult (← ReferenceEnvironment.field row "path").getStr?)
    let key := BaselineArtifacts.pathKey path
    if keys.contains key then fail "AUTHOR_ARTIFACT_ALIAS"
    keys := keys.insert key
    discard <| ReferenceEnvironment.identityOf (← ReferenceEnvironment.field row "sha256")
    let count ← ExprCodec.natOf (← ReferenceEnvironment.field row "bytes")
    total := total + count
    if count == 0 || total > 67108864 then fail "AUTHOR_ARTIFACT_BOUND"
    let info ← (ReferenceEnvironment.nativePath path).symlinkMetadata
    if info.type != .file || info.numLinks != 1 || info.byteSize.toNat != count then
      fail "AUTHOR_ARTIFACT_METADATA"
    paths := paths.push path
  if paths[0]!.fileName != some (name.toString ++ ".olean") ||
      paths != ReferenceEnvironment.moduleParts paths[0]! then fail "AUTHOR_ARTIFACT_NAMES"
  return paths

def ownNames (env : Environment) (moduleName : Name) (imports : Array Import)
    : IO (Std.HashSet Name) := do
  let modules := env.allImportedModuleNames
  let data := env.header.moduleData
  if modules.size != data.size then fail "HEADER_CENSUS"
  let mut count := 0
  let mut names : Std.HashSet Name := {}
  for i in [:modules.size] do
    if modules[i]! != moduleName then continue
    count := count + 1
    let own := data[i]!
    if !own.isModule || own.imports != imports || own.constNames.isEmpty ||
        own.constNames.size > 65536 || own.constants.size != own.constNames.size then
      fail "AUTHOR_MODULE_HEADER"
    for name in own.constNames do
      if names.contains name then fail "AUTHOR_DUPLICATE_NAME"
      names := names.insert name
  if count != 1 then fail "AUTHOR_MODULE_IDENTITY"
  return names

def checkSelectedUnits (units : Array Json) (owned : Std.HashSet Name) : IO Unit := do
  let mut nodes := 0
  let mut names : Std.HashSet Name := {}
  for unit in units do
    let parts ← ExprCodec.arrayOf unit (some 3)
    nodes := nodes + (← DeclCodec.descriptorNodes parts[1]! limits.codec)
    if nodes > 131072 then fail "ENCODED_NODE_BOUND"
    for row in (← ExprCodec.arrayOf parts[2]!) do
      nodes := nodes + (← DeclCodec.inventoryNodes row limits.codec)
      if nodes > 131072 then fail "ENCODED_NODE_BOUND"
      let fields ← ExprCodec.arrayOf row (some 5)
      let name ← ExprCodec.decodeName fields[0]!
      if !owned.contains name || names.contains name then fail "NONAUTHOR_OR_DUPLICATE_EXPORT"
      names := names.insert name
      if names.size > 4096 then fail "EXPORTED_NAME_BOUND"

def run (inventoryPath requestPath planPath outputPath : System.FilePath) : IO Unit := do
  if [inventoryPath, requestPath, planPath].contains outputPath then fail "OUTPUT_INPUT_ALIAS"
  BaselineArtifacts.requireFresh outputPath
  let request ← ReferenceEnvironment.readJson requestPath frameMaximum
  ReferenceEnvironment.exactObject request #["schema", "semantic_id", "foundation_id", "context_root",
    "reference_id", "parent_delta_id", "reference_plan_sha256", "module_name", "targets", "artifact_parts"]
  if (← ReferenceEnvironment.field request "schema") != .str "DMKN_ORDINARY_REFERENCE_SOURCE_REQUEST_V1" then
    fail "REQUEST_SCHEMA"
  let semanticId ← ReferenceEnvironment.identityOf (← ReferenceEnvironment.field request "semantic_id")
  let foundationId ← ReferenceEnvironment.identityOf (← ReferenceEnvironment.field request "foundation_id")
  let contextRoot ← ReferenceEnvironment.identityOf (← ReferenceEnvironment.field request "context_root")
  let moduleName ← authorModule (← ReferenceEnvironment.field request "module_name")
  let targets ← ReferenceEnvironment.namesOf (← ReferenceEnvironment.field request "targets") 32
  if targets.isEmpty then fail "TARGETS_REQUIRED"
  let plan ← ReferenceEnvironment.readPlan planPath inventoryPath request
  if (plan.artifacts.find? moduleName).isSome then fail "AUTHOR_MODULE_COLLISION"
  let parts ← authorParts (← ReferenceEnvironment.field request "artifact_parts") moduleName plan
    #[inventoryPath, requestPath, planPath, outputPath]
  let artifacts := plan.artifacts.insert moduleName (BaselineArtifacts.asArtifacts parts)
  searchPathRef.set []
  let owner ← importModules #[ReferenceEnvironment.standardImport moduleName] {} 0
    (plugins := #[]) (loadExts := false) (level := .private) (arts := artifacts)
  ReferenceEnvironment.checkBaseHeaders owner plan false (some moduleName)
  ReferenceEnvironment.checkBaseRecords owner plan false
  let owned ← ownNames owner moduleName plan.imports
  let allowed : Std.HashSet Name := plan.externalNames.foldl (fun set name => set.insert name) {}
  for name in owned do
    if allowed.contains name then fail "AUTHOR_BOUNDARY_NAME_COLLISION"
  let kernel := owner.toKernelEnv
  let publicEnv := owner.setExporting true
  for name in targets do
    if !owned.contains name || (publicEnv.find? name (skipRealize := true)).isNone then
      fail "TARGET_NOT_AUTHOR_PUBLIC_DECLARATION"
    let some actual := kernel.find? name | fail "TARGET_NOT_IN_AUTHOR_MODULE"
    if actual.isAxiom || actual.name != name || actual.isUnsafe || actual.isPartial then
      fail "TARGET_NOT_COMPLETE_SAFE_DECLARATION"
  let stdin ← IO.getStdin
  let stdout ← IO.getStdout
  let used ← IO.mkRef 0
  let sequence ← IO.mkRef 0
  let answers ← IO.mkRef ({} : Std.HashMap Name (Option String))
  let resolve : Name → IO (Option String) := fun name => do
    let cache ← answers.get
    if let some found := cache[name]? then return found
    let boundary := allowed.contains name
    if !boundary && !owned.contains name then fail s!"DEPENDENCY_OUTSIDE_APPROVED_FRONTIER name={name}"
    CheckedExtension.requireName name
    let seq ← sequence.get
    if seq >= lookupMaximum then fail "LOOKUP_COUNT_BOUND"
    let encoded ← ExprCodec.encodeName name
    sendFrame stdout used (Json.mkObj [
      ("schema", .str "DMKN_ORDINARY_PARENT_LOOKUP_V1"),
      ("seq", toJson seq), ("name", encoded)])
    let response ← receiveFrame stdin used
    let status ← ExprCodec.jsonResult (← ReferenceEnvironment.field response "status").getStr?
    if status == "FOUND" then
      ReferenceEnvironment.exactObject response #["schema", "seq", "name", "status", "symbol_id"]
    else if status == "ABSENT" then
      ReferenceEnvironment.exactObject response #["schema", "seq", "name", "status"]
    else fail "REPLY_STATUS"
    if (← ReferenceEnvironment.field response "schema") != .str "DMKN_ORDINARY_PARENT_REPLY_V1" ||
        (← ExprCodec.natOf (← ReferenceEnvironment.field response "seq")) != seq ||
        (← ReferenceEnvironment.field response "name") != encoded then fail "REPLY_BINDING"
    let symbol ← if status == "FOUND" then do
      pure (some (← ReferenceEnvironment.identityOf (← ReferenceEnvironment.field response "symbol_id")))
    else pure none
    if boundary != symbol.isSome then fail "BOUNDARY_CURRENT_WARRANT_OR_NEW_NAME_CONFLICT"
    answers.set (cache.insert name symbol)
    sequence.set (seq + 1)
    return symbol
  for name in targets do
    if (← resolve name).isSome then fail "AUTHOR_TARGET_ALREADY_WARRANTED"
  let indexed : Export.IndexedSource := {
    source := { environment := kernel, grouping := #[], count := 0 }
    members := {} }
  let policy : Export.DynamicBoundary := {
    stop := fun name => do return (← resolve name).isSome
    maxLookups := lookupMaximum, maxNames := 65536 }
  let exported ← Export.selectedFromBoundary indexed #[] targets limits (some policy)
  if exported.units.isEmpty then fail "AUTHOR_UNITS_REQUIRED"
  checkSelectedUnits exported.units owned
  let known ← answers.get
  let mut boundary : Array Json := #[]
  for name in exported.boundaryReferences do
    let some (some symbol) := known[name]? | fail "BOUNDARY_WITHOUT_REPLY"
    boundary := boundary.push (.arr #[← ExprCodec.encodeName name, .str symbol])
  let result := Json.mkObj [
    ("schema", .str "DMKN_ORDINARY_CANDIDATE_BUNDLE_V2"),
    ("assurance", .str "INERT_OWNER_EXPORT_NOT_MATHEMATICAL_ACCEPTANCE"),
    ("semantic_id", .str semanticId), ("foundation_id", .str foundationId),
    ("context_root", .str contextRoot), ("targets", ← ReferenceEnvironment.encodedNames targets),
    ("boundary_imports", .arr boundary), ("unresolved_imports", .arr #[]),
    ("units", .arr exported.units),
    ("stats", Json.mkObj [
      ("source_records_enumerated", toJson exported.sourceRecords),
      ("selected_units", toJson exported.selectedUnits),
      ("dependency_edges", toJson exported.dependencyEdges),
      ("scan_nodes", toJson exported.scanNodes),
      ("unit_json_bytes", toJson exported.unitBytes),
      ("boundary_imports", toJson boundary.size), ("unresolved_imports", toJson (0 : Nat))])]
  let bytes := result.compress.toUTF8
  if bytes.isEmpty || bytes.size > 4194304 then fail "CANDIDATE_BYTE_BOUND"
  -- Native metadata checks supplement, never replace, controller byte pins.
  discard <| authorParts (← ReferenceEnvironment.field request "artifact_parts") moduleName plan
    #[inventoryPath, requestPath, planPath, outputPath]
  BaselineArtifacts.requireFresh outputPath
  let output ← IO.FS.Handle.mk (ReferenceEnvironment.nativePath outputPath) .writeNew
  output.write bytes
  output.flush
  sendFrame stdout used (Json.mkObj [
    ("schema", .str "DMKN_ORDINARY_MISSING_IMPORT_DONE_V1"),
    ("lookups", toJson (← sequence.get)), ("units", toJson exported.selectedUnits),
    ("output_bytes", toJson bytes.size)])
  if !(← stdin.read 1).isEmpty then fail "TRAILING_REPLY_BYTES"

end OrdinaryLean.ReferenceSource

def main (args : List String) : IO UInt32 := do
  try
    match args with
    | [sysroot, inventory, request, plan, output] =>
        discard <| OrdinaryLean.ReferenceEnvironment.absolutePath sysroot
        OrdinaryLean.ReferenceSource.run
          (← OrdinaryLean.ReferenceEnvironment.absolutePath inventory)
          (← OrdinaryLean.ReferenceEnvironment.absolutePath request)
          (← OrdinaryLean.ReferenceEnvironment.absolutePath plan)
          (← OrdinaryLean.ReferenceEnvironment.absolutePath output)
        return 0
    | _ => OrdinaryLean.ReferenceSource.fail "USAGE sysroot inventory request reference_plan output_candidate"
  catch error =>
    (← IO.getStderr).putStrLn (toString error)
    return 1
