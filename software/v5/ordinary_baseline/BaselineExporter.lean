import OrdinaryExport

/- Explicit owner-approved baseline production, not mathematical acceptance.
   The controller authenticates the selected executable/runtime, exact fixed
   inventory, canonical request and approved local project paths, and supervises
   the complete operation. This producer has no catalog, callback, source build
   or executable peer input. Project approval does not pin its transitive
   artifacts or establish a warm semantic reference base. -/

open Lean

namespace OrdinaryLean.BaselineExporter

def jsonMaximum : Nat := 1048576
def bundleMaximum : Nat := 67108864

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"ORDINARY_BASELINE_EXPORT {message}"

def phase (message : String) : IO Unit := do
  let stderr ← IO.getStderr
  stderr.putStrLn s!"ORDINARY_BASELINE_EXPORT_PHASE {message}"
  stderr.flush

def absolutePath (raw : String) : IO System.FilePath := do
  let path := System.FilePath.mk raw
  if !path.isAbsolute || path.toString.utf8ByteSize > 32768 then
    fail "ABSOLUTE_BOUNDED_PATH_REQUIRED"
  if path.components.contains "." || path.components.contains ".." then
    fail "DOT_PATH_COMPONENT"
  return path

/- Preserve the reviewed approved-project filesystem spelling rule. This changes
   native spelling only, not request identity or the referent of a dot/space-ended
   Win32 component. No UNC/device-path project input is supported. -/
def nativePath (path : System.FilePath) : System.FilePath :=
  if !System.Platform.isWindows then path else
    let normalizedPath := path.normalize
    if normalizedPath.components.any (fun component =>
        component.endsWith "." || component.endsWith " ") then path else
    let normalized := normalizedPath.toString
    match normalized.toList with
    | driveLetter :: ':' :: '\\' :: _ =>
        if ('A' ≤ driveLetter && driveLetter ≤ 'Z') then
          System.FilePath.mk ("\\\\?\\" ++ normalized)
        else path
    | _ => path

/-- Allocation bounds before Json.parse. The controller separately authenticates
    fixed inventory bytes and canonical duplicate-free request bytes. -/
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

def readJson (path : System.FilePath) : IO Json := do
  let path := nativePath path
  if (← path.metadata).byteSize.toNat > jsonMaximum then fail "JSON_BYTE_BOUND"
  let handle ← IO.FS.Handle.mk path .read
  let mut bytes : ByteArray := ⟨#[]⟩
  while true do
    let chunk ← handle.read (USize.ofNat (min 65536 (jsonMaximum + 1 - bytes.size)))
    if chunk.isEmpty then break
    bytes := bytes ++ chunk
    if bytes.size > jsonMaximum then fail "JSON_BYTE_BOUND"
  if bytes.isEmpty then fail "JSON_EMPTY"
  lexicalPreflight bytes
  let some text := String.fromUTF8? bytes | fail "JSON_UTF8"
  if text.toUTF8 != bytes then fail "JSON_UTF8_CANONICAL"
  match Json.parse text with
  | .ok value => return value
  | .error _ => fail "JSON_PARSE"

def exactObject (value : Json) (keys : Array String) : IO Unit := do
  let object ← ExprCodec.jsonResult value.getObj?
  if object.size != keys.size then fail "JSON_EXACT_FIELDS"
  for key in keys do
    if (object.get? key).isNone then fail "JSON_MISSING_FIELD"

def field (value : Json) (key : String) : IO Json :=
  ExprCodec.jsonResult (value.getObjVal? key)

def namesOf (value : Json) (maximum : Nat) : IO (Array Name) := do
  let raw ← ExprCodec.arrayOf value
  if raw.isEmpty || raw.size > maximum then fail "NAME_COUNT_BOUND"
  let mut names : Array Name := #[]
  let mut seen : Std.HashSet Name := {}
  for encoded in raw do
    let name ← ExprCodec.decodeName encoded
    CheckedExtension.requireName name
    if seen.contains name then fail "DUPLICATE_NAME"
    seen := seen.insert name
    names := names.push name
  return names

def identifierStart (c : Char) : Bool :=
  ('A' ≤ c && c ≤ 'Z') || ('a' ≤ c && c ≤ 'z') || c == '_'

def moduleComponent (part : String) : Bool :=
  let valid := match part.toList with
    | [] => false
    | first :: rest =>
        identifierStart first && rest.all (fun c =>
          identifierStart c || ('0' ≤ c && c ≤ '9'))
  let lower := part.toLower
  let reserved := ["con", "prn", "aux", "nul"].contains lower ||
    (List.range 9).any (fun i => lower == "com" ++ toString (i + 1) ||
      lower == "lpt" ++ toString (i + 1))
  valid && part.utf8ByteSize ≤ 96 && !reserved

def projectModulesOf (value : Json) : IO (Array Name) := do
  if value.compress.utf8ByteSize > 65536 then fail "PROJECT_MODULE_BYTES"
  let names ← namesOf value 16
  for encoded in (← ExprCodec.arrayOf value) do
    if encoded.compress.utf8ByteSize > 4096 then fail "PROJECT_MODULE_NAME_BYTES"
  for name in names do
    let mut cursor := name
    let mut parts := 0
    while cursor != .anonymous do
      match cursor with
      | .str parent component =>
          parts := parts + 1
          if parts > 16 || !moduleComponent component then
            fail "PROJECT_MODULE_IDENTIFIER"
          cursor := parent
      | _ => fail "PROJECT_MODULE_IDENTIFIER"
    if parts == 0 then fail "PROJECT_MODULE_IDENTIFIER"
  return names

def projectPathsOf (value : Json) : IO (List System.FilePath) := do
  let rawPaths ← ExprCodec.arrayOf value
  if rawPaths.isEmpty || rawPaths.size > 16 then fail "PROJECT_ROOT_COUNT"
  let mut paths : Array System.FilePath := #[]
  let mut seen : Std.HashSet String := {}
  for encoded in rawPaths do
    let raw ← ExprCodec.jsonResult encoded.getStr?
    if raw.isEmpty || raw.utf8ByteSize > 32768 ||
        raw.toList.any (fun c => c.toNat < 32 || c == ';') then
      fail "PROJECT_ROOT_SPELLING"
    let drivePath := match raw.toList with
      | letter :: ':' :: separator :: _ =>
          (('A' ≤ letter && letter ≤ 'Z') || ('a' ≤ letter && letter ≤ 'z')) &&
            (separator == '\\' || separator == '/')
      | _ => false
    if !System.Platform.isWindows || !drivePath then
      fail "PROJECT_ROOT_ORDINARY_WINDOWS_DRIVE_REQUIRED"
    let components := (raw.replace "\\" "/").splitOn "/"
    if components.any (fun part => part == "." || part == "..") then
      fail "PROJECT_ROOT_DOT_COMPONENT"
    let nonempty := components.filter (fun part => !part.isEmpty)
    if nonempty.length > 128 then fail "PROJECT_ROOT_COMPONENT_BOUND"
    let key := String.intercalate "/" (nonempty.map String.toLower)
    if seen.contains key then fail "PROJECT_ROOT_DUPLICATE"
    let path ← absolutePath raw
    if (← (nativePath path).symlinkMetadata).type != .dir then
      fail "PROJECT_ROOT_DIRECTORY_REQUIRED"
    -- The selected controller must also reject reparses in every ancestor.
    seen := seen.insert key
    paths := paths.push path
  return paths.toList

def requireFresh (path : System.FilePath) : IO Unit := do
  let present ← try
    discard (nativePath path).symlinkMetadata
    pure true
  catch error =>
    match error with
    | .noFileOrDirectory .. => pure false
    | _ => throw error
  if present then fail "FRESH_OUTPUT_REQUIRED"

/-- Reject a seed target before loading the selected project. Exact seed byte
    identity remains the controller/binder's job, not a conclusion of this shape
    check. The existing exporter performs actual source-basis correspondence. -/
def nonbasisTargets (inventory : Json) (targets : Array Name) : IO Unit := do
  let rows ← ExprCodec.arrayOf inventory
  if rows.size != 581 then fail "FIXED_BASIS_NAME_COUNT"
  let mut basis : Std.HashSet Name := {}
  for raw in rows do
    let row ← ExprCodec.arrayOf raw (some 5)
    let name ← BootstrapProbe.nameOf row[0]!
    if basis.contains name then fail "BASIS_DUPLICATE_NAME"
    basis := basis.insert name
  for target in targets do
    if basis.contains target then fail "NONBASIS_TARGET_REQUIRED"

def run (sysroot inventoryPath requestPath outputPath : System.FilePath) : IO Unit := do
  requireFresh outputPath
  let inventory ← readJson inventoryPath
  let request ← readJson requestPath
  exactObject request #["schema", "project_search_paths", "modules", "targets"]
  if (← ExprCodec.jsonResult (← field request "schema").getStr?) !=
      "DMKN_ORDINARY_BASELINE_EXPORT_REQUEST_V1" then fail "REQUEST_SCHEMA"
  let modules ← projectModulesOf (← field request "modules")
  let targets ← namesOf (← field request "targets") 1024
  nonbasisTargets inventory targets
  let roots ← projectPathsOf (← field request "project_search_paths")
  let imports := modules.map (fun name => ({ module := name } : Import))
  -- One original private environment. No inherited LEAN_PATH, helper/source
  -- directories, dynamic parent lookup, plugins or environment extensions.
  let paths := (sysroot / "lib" / "lean") :: roots
  searchPathRef.set (paths.map nativePath)
  phase "BEFORE_APPROVED_PROJECT_IMPORT"
  let owner ← importModules imports {} 0
    (plugins := #[]) (loadExts := false) (level := .private)
  phase "APPROVED_PROJECT_IMPORT_COMPLETED"
  let kernel := owner.toKernelEnv
  for name in targets do
    let some actual := kernel.find? name | fail s!"TARGET_NOT_IN_SELECTED_LIBRARY name={name}"
    if actual.isAxiom then fail s!"TARGET_MISSING_COMPLETE_DECLARATION name={name}"
    if actual.name != name || actual.isUnsafe || actual.isPartial then
      fail "UNSAFE_OR_MISKEYED_TARGET"
  -- Preserve the existing finite source census and complete-unit scheduler.
  -- This concrete route indexes eagerly; it is not a streaming export claim.
  let indexed ← Export.indexSource kernel
  phase s!"SOURCE_INDEX_COMPLETED records={indexed.source.count} grouping={indexed.source.grouping.size}"
  let exported ← Export.selected indexed inventory targets
  phase s!"SELECTED_EXPORT_COMPLETED units={exported.selectedUnits} edges={exported.dependencyEdges} scanNodes={exported.scanNodes} unitBytes={exported.unitBytes}"
  let encodedTargets ← exported.targets.mapM (fun name => ExprCodec.encodeName name)
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
    ("targets", Json.arr encodedTargets), ("basis_names", Json.arr basis),
    ("units", Json.arr exported.units), ("stats", stats)]
  let bytes := result.compress.toUTF8
  if bytes.size > bundleMaximum then fail "BUNDLE_BYTE_BOUND"
  let output ← IO.FS.Handle.mk (nativePath outputPath) .writeNew
  output.write bytes
  output.flush
  phase s!"OUTPUT_WRITTEN bytes={bytes.size}"

end OrdinaryLean.BaselineExporter

def main (args : List String) : IO UInt32 := do
  try
    match args with
    | [sysroot, inventoryPath, requestPath, outputPath] =>
        OrdinaryLean.BaselineExporter.run
          (← OrdinaryLean.BaselineExporter.absolutePath sysroot)
          (← OrdinaryLean.BaselineExporter.absolutePath inventoryPath)
          (← OrdinaryLean.BaselineExporter.absolutePath requestPath)
          (← OrdinaryLean.BaselineExporter.absolutePath outputPath)
        return 0
    | _ =>
        OrdinaryLean.BaselineExporter.fail "USAGE sysroot inventory request output"
  catch error =>
    let stderr ← IO.getStderr
    stderr.putStrLn (String.ofList (error.toString.toList.take 2048))
    stderr.flush
    return 1
