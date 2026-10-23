import Lean.Elab.Command
import OrdinaryExport

/- Trusted owner-project command, NOT a peer source endpoint or receiver.
   Reuses the current elaborator environment; no second importModules call.
   The outer controller pins runtime/import artifacts/fixed inventory and owns
   finite process supervision. The output remains inert producer claims. -/

open Lean
open Lean.Elab.Command

namespace OrdinaryLean.OwnerExport

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"ORDINARY_OWNER_EXPORT {message}"

def phase (message : String) : IO Unit := do
  let stdout ← IO.getStdout
  stdout.putStrLn s!"ORDINARY_OWNER_EXPORT_PHASE {message}"
  stdout.flush

def absolutePath (raw : String) : IO System.FilePath := do
  let path := System.FilePath.mk raw
  if !path.isAbsolute || path.toString.utf8ByteSize > 32768 then
    fail "ABSOLUTE_BOUNDED_PATH_REQUIRED"
  if path.components.contains "." || path.components.contains ".." then
    fail "DOT_PATH_COMPONENT"
  return path

/-- Small raw lexical bound before Json.parse; trusted controller still owns
    exact fixed-file authentication, duplicate-key and canonical checks. -/
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

def readInventory (path : System.FilePath) : IO Json := do
  let maximum := 1048576
  if (← path.metadata).byteSize.toNat > maximum then fail "INVENTORY_BYTE_BOUND"
  let handle ← IO.FS.Handle.mk path .read
  let mut bytes : ByteArray := ⟨#[]⟩
  while true do
    let chunk ← handle.read (USize.ofNat (min 65536 (maximum + 1 - bytes.size)))
    if chunk.isEmpty then break
    bytes := bytes ++ chunk
    if bytes.size > maximum then fail "INVENTORY_BYTE_BOUND"
  if bytes.isEmpty then fail "INVENTORY_EMPTY"
  lexicalPreflight bytes
  let some text := String.fromUTF8? bytes | fail "INVENTORY_UTF8"
  if text.toUTF8 != bytes then fail "INVENTORY_UTF8_CANONICAL"
  match Json.parse text with
  | .ok value => return value
  | .error _ => fail "INVENTORY_JSON"

def requireFresh (path : System.FilePath) : IO Unit := do
  let present ← try
    discard path.symlinkMetadata
    pure true
  catch error =>
    match error with
    | .noFileOrDirectory .. => pure false
    | _ => throw error
  if present then fail "FRESH_OUTPUT_REQUIRED"

def run (owner : Environment) (target : Name) (inventoryRaw outputRaw : String)
    : IO Unit := do
  phase "ENTERED_EXISTING_OWNER_ENVIRONMENT"
  let inventoryPath ← absolutePath inventoryRaw
  let outputPath ← absolutePath outputRaw
  requireFresh outputPath
  CheckedExtension.requireName target
  let kernel := owner.toKernelEnv
  match kernel.find? target with
  | some (.thmInfo _) => pure ()
  | some (.axiomInfo _) => fail "TARGET_PUBLIC_AXIOM_VIEW_NOT_PROOF"
  | _ => fail "TARGET_THEOREM_RECORD_REQUIRED"
  let inventory ← readInventory inventoryPath
  let indexed ← Export.indexSource kernel
  phase s!"SOURCE_INDEX_COMPLETED records={indexed.source.count} grouping={indexed.source.grouping.size}"
  let exported ← Export.selected indexed inventory #[target]
  phase s!"SELECTED_EXPORT_COMPLETED units={exported.selectedUnits} edges={exported.dependencyEdges} scanNodes={exported.scanNodes} unitBytes={exported.unitBytes}"
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
  let bytes := result.compress.toUTF8
  if bytes.size > 67108864 then fail "BUNDLE_BYTE_BOUND"
  let output ← IO.FS.Handle.mk outputPath .writeNew
  output.write bytes
  output.flush
  phase s!"OUTPUT_WRITTEN bytes={bytes.size}"

end OrdinaryLean.OwnerExport

/-- Owner-only export of an exact native theorem name from the current project.
    The inventory/output strings are controller-selected absolute local paths. -/
elab "#ordinary_export " target:ident inventory:str output:str : command => do
  let owner ← getEnv
  liftIO <| OrdinaryLean.OwnerExport.run owner target.getId
    inventory.getString output.getString
