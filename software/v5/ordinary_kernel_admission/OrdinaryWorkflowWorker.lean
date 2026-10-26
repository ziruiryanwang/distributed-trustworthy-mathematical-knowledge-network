import OrdinaryExport
import BasisSnapshot

/- Internal trusted-controller worker. The controller authenticates and reserves
   exact runtime/source/profile/parent/request bytes BEFORE invocation, supervises
   this process, and owns catalog promotion. Paths, JSON or reports are never
   warrants. No peer source execution, peer binary import or certificates. -/

open Lean

namespace OrdinaryLean.WorkflowWorker

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"ORDINARY_WORKER {message}"

def absolutePath (raw : String) : IO System.FilePath := do
  let path := System.FilePath.mk raw
  if !path.isAbsolute || path.toString.utf8ByteSize > 32768 then
    fail "ABSOLUTE_BOUNDED_PATH_REQUIRED"
  if path.components.contains "." || path.components.contains ".." then
    fail "DOT_PATH_COMPONENT"
  return path

/-- No token can request huge exponent/fraction/negative numeric parsing.
    This pass does not replace controller duplicate-key/canonical/schema checks. -/
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

/-- Internal bounded read of controller-authenticated input, not a peer gateway.
    Lexical/depth screening precedes the general JSON parser on every path. -/
def readSelectedJson (path : System.FilePath) (maximum : Nat) : IO Json := do
  if (← path.metadata).byteSize.toNat > maximum then fail "INPUT_BYTE_BOUND"
  let handle ← IO.FS.Handle.mk path .read
  let mut bytes : ByteArray := ⟨#[]⟩
  while true do
    let remaining := maximum + 1 - bytes.size
    let chunk ← handle.read (USize.ofNat (min 65536 remaining))
    if chunk.isEmpty then break
    bytes := bytes ++ chunk
    if bytes.size > maximum then fail "INPUT_BYTE_BOUND"
  if bytes.isEmpty then fail "INPUT_EMPTY"
  lexicalPreflight bytes
  let some text := String.fromUTF8? bytes | fail "INPUT_UTF8"
  if text.toUTF8 != bytes then fail "INPUT_UTF8_CANONICAL"
  match Json.parse text with
  | .ok value => return value
  | .error _ => fail "INPUT_JSON"

def requireFresh (path : System.FilePath) : IO Unit := do
  let present ← try
    discard path.symlinkMetadata
    pure true
  catch error =>
    match error with
    | .noFileOrDirectory .. => pure false
    | _ => throw error
  if present then fail "FRESH_OUTPUT_REQUIRED"

def writeFreshJson (path : System.FilePath) (value : Json) (maximum : Nat)
    : IO Unit := do
  let bytes := value.compress.toUTF8
  if bytes.size > maximum then fail "OUTPUT_BYTE_BOUND"
  let output ← IO.FS.Handle.mk path .writeNew
  output.write bytes
  output.flush

def exportMethod (sysroot methodDir inventoryPath outputPath : System.FilePath)
    : IO Unit := do
  requireFresh outputPath
  let inventory ← readSelectedJson inventoryPath 1048576
  -- Do not call initSearchPath: it prepends inherited LEAN_PATH. Runtime first
  -- prevents a selected owner directory from shadowing standard module names.
  searchPathRef.set [sysroot / "lib" / "lean", methodDir]
  let owner ← importModules #[{ module := `examples.ReadFootprint }]
    {} 0 (plugins := #[]) (loadExts := false) (level := .private)
  let indexed ← Export.indexSource owner.toKernelEnv
  let exported ← Export.selected indexed inventory #[`DMKN.ReadFootprint.readsOnly_insertMany]
  let targets ← exported.targets.mapM (fun name => ExprCodec.encodeName name)
  let basis ← exported.basisNames.mapM (fun name => ExprCodec.encodeName name)
  let stats := Json.mkObj [
    ("source_records", toJson exported.sourceRecords),
    ("selected_units", toJson exported.selectedUnits),
    ("dependency_edges", toJson exported.dependencyEdges),
    ("scan_nodes", toJson exported.scanNodes),
    ("unit_json_bytes", toJson exported.unitBytes)]
  let result := Json.mkObj [
    ("schema", Json.str "DMKN_ORDINARY_EXPORT_BUNDLE_V1"),
    ("assurance", Json.str "INERT_OWNER_EXPORT_NOT_MATHEMATICAL_ACCEPTANCE"),
    ("targets", Json.arr targets), ("basis_names", Json.arr basis),
    ("units", Json.arr exported.units), ("stats", stats)]
  writeFreshJson outputPath result 67108864

def moduleForRoot (root : String) : IO Name := do
  let bytes := root.toUTF8
  if bytes.size != 64 || !bytes.data.all (fun byte =>
      (byte.toNat >= 48 && byte.toNat <= 57) ||
      (byte.toNat >= 97 && byte.toNat <= 102)) then fail "ROOT_HEX"
  return .str (.str .anonymous "DMKNLocal") ("r" ++ root)

def exactObject (value : Json) (keys : Array String) : IO Unit := do
  let object ← ExprCodec.jsonResult value.getObj?
  if object.size != keys.size then fail "JSON_EXACT_FIELDS"
  for key in keys do
    if (object.get? key).isNone then fail "JSON_MISSING_FIELD"

def field (value : Json) (key : String) : IO Json := do
  let object ← ExprCodec.jsonResult value.getObj?
  let some found := object.get? key | fail "JSON_MISSING_FIELD"
  return found

def moduleName (value : Json) : IO Name := do
  let name ← ExprCodec.decodeName value
  ExprCodec.requireSemanticName name
  return name

def decodePlan (value : Json) : IO LocalSnapshot.LocalImportPlan := do
  exactObject value #["basis_module", "root_module", "modules"]
  let basisModule ← moduleName (← field value "basis_module")
  let rootModule ← moduleName (← field value "root_module")
  let entries ← ExprCodec.arrayOf (← field value "modules")
  if entries.isEmpty || entries.size > 4096 then fail "PLAN_MODULE_BOUND"
  let mut modules := #[]
  for entry in entries do
    exactObject entry #["module_name", "path", "parent_module", "artifact_bytes", "names_count"]
    let name ← moduleName (← field entry "module_name")
    let path ← absolutePath (← ExprCodec.jsonResult (← field entry "path").getStr?)
    let parent ← ExprCodec.decodeName (← field entry "parent_module")
    let parentModule ← if parent.isAnonymous then pure none else do
      ExprCodec.requireSemanticName parent
      pure (some parent)
    let artifactBytes ← ExprCodec.natOf (← field entry "artifact_bytes")
    let namesCount ← ExprCodec.natOf (← field entry "names_count")
    modules := modules.push ({
      moduleName := name
      path := path
      parentModule := parentModule
      artifactBytes := artifactBytes
      namesCount := namesCount
    } : LocalSnapshot.LocalModule)
  return { basisModule, rootModule, modules }

def writeReport (path : System.FilePath) (kind : String) (moduleId : Name)
    (parent : Option Name) (names : Array Name) (units bytes : Nat) : IO Unit := do
  let reportedNames ← names.mapM (fun name => ExprCodec.encodeName name)
  let parentName ← ExprCodec.encodeName (parent.getD .anonymous)
  writeFreshJson path (Json.mkObj [
    ("schema", Json.str "DMKN_ORDINARY_WORKER_OUTPUT_V1"),
    ("kind", Json.str kind), ("module_name", ← ExprCodec.encodeName moduleId),
    ("parent_module", parentName), ("names", Json.arr reportedNames),
    ("units_checked", toJson units), ("artifact_bytes", toJson bytes)]) 16777216

def initializeBasis (seedPath inventoryPath : System.FilePath) (root : String)
    (outputPath reportPath : System.FilePath) : IO Unit := do
  if outputPath == reportPath then fail "OUTPUT_REPORT_ALIAS"
  requireFresh outputPath
  requireFresh reportPath
  let moduleId ← moduleForRoot root
  let seed ← readSelectedJson seedPath 1048576
  let inventory ← readSelectedJson inventoryPath 1048576
  let written ← BasisSnapshot.checkAndWriteBasis seed inventory moduleId outputPath
  writeReport reportPath "basis" written.chunk.moduleName none written.chunk.names
    BasisSnapshot.fixedUnitCount written.chunk.artifactBytes

def extend (planPath unitsPath : System.FilePath) (root : String)
    (outputPath reportPath : System.FilePath) : IO Unit := do
  if outputPath == reportPath then fail "OUTPUT_REPORT_ALIAS"
  requireFresh outputPath
  requireFresh reportPath
  let moduleId ← moduleForRoot root
  let plan ← decodePlan (← readSelectedJson planPath 16777216)
  let rawUnits ← ExprCodec.arrayOf (← readSelectedJson unitsPath 67108864)
  -- Preserve the reviewed checker default. Do not inflate it to exporter bounds.
  if rawUnits.isEmpty || rawUnits.size > 1024 then fail "BATCH_UNIT_BOUND"
  let parent ← LocalSnapshot.restoreLocal plan
  let mut allowed : Std.HashSet Name := {}
  for (name, _) in parent.toKernelEnv.constants do
    if allowed.size >= 1048576 then fail "PARENT_NAME_BOUND"
    allowed := allowed.insert name
  let mut units := #[]
  let mut claimedNames := 0
  for raw in rawUnits do
    let unit ← DeclCodec.decodeUnit allowed raw
    -- Earlier expected names aid syntax decoding only. Actual checkBatch must
    -- generate and compare those records before any later unit is checked.
    let expectedNames ← DeclCodec.expectedNames unit.expected
    claimedNames := claimedNames + expectedNames.size
    if claimedNames > 65536 || allowed.size + expectedNames.size > 1048576 then
      fail "BATCH_NAME_BOUND"
    for name in expectedNames do
      allowed := allowed.insert name
    units := units.push unit
  let written ← LocalSnapshot.checkAndWriteKernelChunk
    parent.toKernelEnv plan.rootModule moduleId units outputPath
  writeReport reportPath "extension" written.chunk.moduleName
    (some written.chunk.parentModule) written.chunk.names written.chunk.unitsChecked
    written.chunk.artifactBytes

end OrdinaryLean.WorkflowWorker

def main (args : List String) : IO UInt32 := do
  try
    match args with
    | ["export", sysroot, methodDir, inventoryPath, outputPath] =>
        OrdinaryLean.WorkflowWorker.exportMethod
          (← OrdinaryLean.WorkflowWorker.absolutePath sysroot)
          (← OrdinaryLean.WorkflowWorker.absolutePath methodDir)
          (← OrdinaryLean.WorkflowWorker.absolutePath inventoryPath)
          (← OrdinaryLean.WorkflowWorker.absolutePath outputPath)
        return 0
    | ["basis", seedPath, inventoryPath, root, outputPath, reportPath] =>
        OrdinaryLean.WorkflowWorker.initializeBasis
          (← OrdinaryLean.WorkflowWorker.absolutePath seedPath)
          (← OrdinaryLean.WorkflowWorker.absolutePath inventoryPath)
          root
          (← OrdinaryLean.WorkflowWorker.absolutePath outputPath)
          (← OrdinaryLean.WorkflowWorker.absolutePath reportPath)
        return 0
    | ["extend", planPath, unitsPath, root, outputPath, reportPath] =>
        OrdinaryLean.WorkflowWorker.extend
          (← OrdinaryLean.WorkflowWorker.absolutePath planPath)
          (← OrdinaryLean.WorkflowWorker.absolutePath unitsPath)
          root
          (← OrdinaryLean.WorkflowWorker.absolutePath outputPath)
          (← OrdinaryLean.WorkflowWorker.absolutePath reportPath)
        return 0
    | _ =>
        OrdinaryLean.WorkflowWorker.fail
          "USAGE export sysroot methodDir inventory output | basis seed inventory rootHex output report | extend plan units rootHex output report"
  catch error =>
    let stderr ← IO.getStderr
    stderr.putStrLn error.toString
    stderr.flush
    return 1
