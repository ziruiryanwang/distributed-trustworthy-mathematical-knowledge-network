import OrdinaryExport

/- Owner-approved artifact closure discovery/replay only. This is neither a
   proof checker nor a baseline correspondence authority. The controller pins
   inputs, approves paths, snapshots exact bytes and bounds the whole process.
   Collect mode's size/census checks occur after the native import; they are not
   a pre-import allocation bound. Replay clears all name-search fallback. -/

open Lean

namespace OrdinaryLean.BaselineArtifacts

def requestMaximum : Nat := 1048576
def replayRequestMaximum : Nat := 16777216
def reportMaximum : Nat := 16777216
def moduleMaximum : Nat := 4096
def partMaximum : Nat := 20480
def partBytesMaximum : Nat := 67108864
def totalBytesMaximum : Nat := 536870912
def importEdgeMaximum : Nat := 65536

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"ORDINARY_BASELINE_ARTIFACTS {message}"

def phase (message : String) : IO Unit := do
  let stderr ← IO.getStderr
  stderr.putStrLn s!"ORDINARY_BASELINE_ARTIFACTS_PHASE {message}"
  stderr.flush

def absolutePath (raw : String) : IO System.FilePath := do
  let path := System.FilePath.mk raw
  if !path.isAbsolute || path.toString.utf8ByteSize > 32768 then
    fail "ABSOLUTE_BOUNDED_PATH_REQUIRED"
  if path.components.contains "." || path.components.contains ".." then
    fail "DOT_PATH_COMPONENT"
  return path

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

def ordinaryDrivePath (raw : String) : IO System.FilePath := do
  if raw.isEmpty || raw.utf8ByteSize > 32768 ||
      raw.toList.any (fun c => c.toNat < 32 || c == ';') then
    fail "PATH_SPELLING"
  let drivePath := match raw.toList with
    | letter :: ':' :: separator :: _ =>
        (('A' ≤ letter && letter ≤ 'Z') || ('a' ≤ letter && letter ≤ 'z')) &&
          (separator == '\\' || separator == '/')
    | _ => false
  if !System.Platform.isWindows || !drivePath then
    fail "ORDINARY_WINDOWS_DRIVE_REQUIRED"
  let components := (raw.replace "\\" "/").splitOn "/"
  if components.any (fun part => part == "." || part == "..") then
    fail "PATH_DOT_COMPONENT"
  if (components.filter (fun part => !part.isEmpty)).length > 128 then
    fail "PATH_COMPONENT_BOUND"
  absolutePath raw

/-- Strip only the extended spelling added for native local-drive lookup, not
    an arbitrary caller-supplied device namespace. Returned reports use ordinary
    paths so the controller's established ordinary-file validator can bind them. -/
def reportPath (path : System.FilePath) : IO System.FilePath := do
  let raw := path.toString
  let raw := if raw.startsWith "\\\\?\\" then
      String.ofList (raw.toList.drop 4) else raw
  ordinaryDrivePath raw

def pathKey (path : System.FilePath) : String :=
  path.normalize.toString.toLower.replace "\\" "/"

/-- Native lexical allocation guard. Duplicate keys, canonical raw input and
    exact request identity are independently enforced by the controller. -/
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

def readRequest (path : System.FilePath) : IO (Json × Nat) := do
  let path := nativePath path
  if (← path.metadata).byteSize.toNat > replayRequestMaximum then fail "REQUEST_BYTE_BOUND"
  let handle ← IO.FS.Handle.mk path .read
  let mut bytes : ByteArray := ⟨#[]⟩
  while true do
    let chunk ← handle.read (USize.ofNat (min 65536 (replayRequestMaximum + 1 - bytes.size)))
    if chunk.isEmpty then break
    bytes := bytes ++ chunk
    if bytes.size > replayRequestMaximum then fail "REQUEST_BYTE_BOUND"
  if bytes.isEmpty then fail "REQUEST_EMPTY"
  lexicalPreflight bytes
  let some text := String.fromUTF8? bytes | fail "REQUEST_UTF8"
  if text.toUTF8 != bytes then fail "REQUEST_UTF8_CANONICAL"
  match Json.parse text with
  | .ok value => return (value, bytes.size)
  | .error _ => fail "REQUEST_JSON"

def field (value : Json) (key : String) : IO Json :=
  ExprCodec.jsonResult (value.getObjVal? key)

def exactObject (value : Json) (keys : Array String) : IO Unit := do
  let object ← ExprCodec.jsonResult value.getObj?
  if object.size != keys.size then fail "JSON_EXACT_FIELDS"
  for key in keys do
    if (object.get? key).isNone then fail "JSON_MISSING_FIELD"

def identifierStart (c : Char) : Bool :=
  ('A' ≤ c && c ≤ 'Z') || ('a' ≤ c && c ≤ 'z') || c == '_'

def moduleComponent (part : String) : Bool :=
  let valid := match part.toList with
    | [] => false
    | first :: rest => identifierStart first && rest.all (fun c =>
        identifierStart c || ('0' ≤ c && c ≤ '9'))
  let lower := part.toLower
  let reserved := ["con", "prn", "aux", "nul"].contains lower ||
    (List.range 9).any (fun i => lower == "com" ++ toString (i + 1) ||
      lower == "lpt" ++ toString (i + 1))
  valid && part.utf8ByteSize ≤ 96 && !reserved

def requireModuleName (name : Name) : IO Unit := do
  CheckedExtension.requireName name
  let mut cursor := name
  let mut parts := 0
  while cursor != .anonymous do
    match cursor with
    | .str parent component =>
        parts := parts + 1
        if parts > 16 || !moduleComponent component then fail "MODULE_IDENTIFIER"
        cursor := parent
    | _ => fail "MODULE_IDENTIFIER"
  if parts == 0 then fail "MODULE_IDENTIFIER"

def moduleOf (raw : Json) : IO Name := do
  if raw.compress.utf8ByteSize > 4096 then fail "MODULE_NAME_BYTES"
  let name ← ExprCodec.decodeName raw
  requireModuleName name
  return name

def rootModules (value : Json) : IO (Array Import) := do
  if value.compress.utf8ByteSize > 65536 then fail "ROOT_MODULE_BYTES"
  let raw ← ExprCodec.arrayOf value
  if raw.isEmpty || raw.size > 16 then fail "ROOT_MODULE_COUNT"
  let mut imports : Array Import := #[]
  let mut seen : Std.HashSet Name := {}
  for encoded in raw do
    let name ← moduleOf encoded
    if seen.contains name then fail "DUPLICATE_ROOT_MODULE"
    seen := seen.insert name
    imports := imports.push { module := name }
  return imports

def projectPaths (value : Json) : IO (List System.FilePath) := do
  let raw ← ExprCodec.arrayOf value
  if raw.isEmpty || raw.size > 16 then fail "PROJECT_ROOT_COUNT"
  let mut paths : Array System.FilePath := #[]
  let mut seen : Std.HashSet String := {}
  for encoded in raw do
    let path ← ordinaryDrivePath (← ExprCodec.jsonResult encoded.getStr?)
    let key := pathKey path
    if seen.contains key then fail "PROJECT_ROOT_DUPLICATE"
    if (← (nativePath path).symlinkMetadata).type != .dir then
      fail "PROJECT_ROOT_DIRECTORY_REQUIRED"
    -- Full ancestor/reparse validation remains an upstream controller check.
    seen := seen.insert key
    paths := paths.push path
  return paths.toList

def moduleParts (base : System.FilePath) : Array System.FilePath :=
  #[base, OLeanLevel.server.adjustFileName base,
    OLeanLevel.private.adjustFileName base,
    base.withExtension "ir.sig", base.withExtension "ir"]

def asArtifacts (parts : Array System.FilePath) : ImportArtifacts :=
  .ofArrays #[#[nativePath parts[0]!, nativePath parts[1]!, nativePath parts[2]!],
    #[nativePath parts[3]!, nativePath parts[4]!]]

def matrixJson (parts : Array Json) : Json :=
  .arr #[.arr #[parts[0]!, parts[1]!, parts[2]!], .arr #[parts[3]!, parts[4]!]]

structure Selection where
  paths : NameMap (Array System.FilePath) := {}
  artifacts : NameMap ImportArtifacts := {}
  moduleNames : Array Name := #[]
  byteCounts : NameMap (Array Nat) := {}
  pathKeys : Std.HashSet String := {}
  totalBytes : Nat := 0

def addParts (selection : Selection) (name : Name) (parts : Array System.FilePath)
    : IO Selection := do
  requireModuleName name
  if (selection.paths.find? name).isSome then fail "DUPLICATE_ARTIFACT_MODULE"
  if selection.moduleNames.size >= moduleMaximum ||
      (selection.moduleNames.size + 1) * 5 > partMaximum then fail "ARTIFACT_CENSUS_BOUND"
  if parts.size != 5 || parts[0]!.extension != some "olean" ||
      parts != moduleParts parts[0]! then fail "MODERN_FIVE_PART_LAYOUT_REQUIRED"
  let mut seen := selection.pathKeys
  let mut total := selection.totalBytes
  let mut counts : Array Nat := #[]
  for path in parts do
    let key := pathKey path
    if seen.contains key then fail "ARTIFACT_PATH_ALIAS"
    let metadata ← (nativePath path).symlinkMetadata
    if metadata.type != .file then fail "ORDINARY_ARTIFACT_FILE_REQUIRED"
    let size := metadata.byteSize.toNat
    if size == 0 || size > partBytesMaximum then fail "ARTIFACT_PART_BYTE_BOUND"
    total := total + size
    if total > totalBytesMaximum then fail "ARTIFACT_TOTAL_BYTE_BOUND"
    seen := seen.insert key
    counts := counts.push size
  return { paths := selection.paths.insert name parts,
    artifacts := selection.artifacts.insert name (asArtifacts parts),
    moduleNames := selection.moduleNames.push name,
    byteCounts := selection.byteCounts.insert name counts,
    pathKeys := seen, totalBytes := total }

def replaySelection (raw : Json) : IO Selection := do
  let entries ← ExprCodec.arrayOf raw
  if entries.isEmpty || entries.size > moduleMaximum then fail "ARTIFACT_MODULE_BOUND"
  let mut selection : Selection := {}
  for entry in entries do
    exactObject entry #["module", "parts"]
    let name ← moduleOf (← field entry "module")
    let matrix ← ExprCodec.arrayOf (← field entry "parts") (some 2)
    let oleans ← ExprCodec.arrayOf matrix[0]! (some 3)
    let irs ← ExprCodec.arrayOf matrix[1]! (some 2)
    let mut parts : Array System.FilePath := #[]
    for value in oleans ++ irs do
      parts := parts.push (← ordinaryDrivePath (← ExprCodec.jsonResult value.getStr?))
    selection ← addParts selection name parts
  return selection

def bit (value : Bool) : Json := toJson (if value then (1 : Nat) else 0)

def importJson (entry : Import) : IO Json := do
  requireModuleName entry.module
  return Json.mkObj [
    ("module", ← ExprCodec.encodeName entry.module),
    ("import_all", bit entry.importAll), ("is_exported", bit entry.isExported),
    ("is_meta", bit entry.isMeta)]

def effectiveJson (entry : EffectiveImport) : Json :=
  Json.mkObj [
    ("import_all", bit entry.importAll), ("is_exported", bit entry.isExported),
    ("is_meta", bit entry.isMeta), ("has_data", bit entry.hasData),
    ("ir_phases", .str (match entry.irPhases with
      | .runtime => "runtime" | .comptime => "comptime" | .all => "all"))]

def requireFresh (path : System.FilePath) : IO Unit := do
  let present ← try
    discard (nativePath path).symlinkMetadata
    pure true
  catch error =>
    match error with
    | .noFileOrDirectory .. => pure false
    | _ => throw error
  if present then fail "FRESH_OUTPUT_REQUIRED"

def run (sysroot requestPath report : System.FilePath) : IO Unit := do
  requireFresh report
  let (request, requestBytes) ← readRequest requestPath
  if (← ExprCodec.jsonResult (← field request "schema").getStr?) !=
      "DMKN_ORDINARY_BASELINE_ARTIFACT_REQUEST_V1" then fail "REQUEST_SCHEMA"
  let mode ← ExprCodec.jsonResult (← field request "mode").getStr?
  let replay := mode == "replay"
  if !replay && mode != "collect" then fail "REQUEST_MODE"
  if !replay && requestBytes > requestMaximum then fail "COLLECT_REQUEST_BYTE_BOUND"
  if replay then exactObject request #["schema", "mode", "modules", "artifacts"]
  else exactObject request #["schema", "mode", "modules", "project_search_paths"]
  let imports ← rootModules (← field request "modules")
  let mut selection : Selection := {}
  if replay then
    selection ← replaySelection (← field request "artifacts")
    for entry in imports do
      if (selection.artifacts.find? entry.module).isNone then fail "ROOT_ARTIFACT_MISSING"
    -- importModules falls back to findOLean for missing map keys. Empty search
    -- makes such a key fail, including any omitted runtime dependency.
    searchPathRef.set []
  else
    let roots ← projectPaths (← field request "project_search_paths")
    searchPathRef.set (((sysroot / "lib" / "lean") :: roots).map nativePath)
  phase s!"BEFORE_PRIVATE_IMPORT mode={mode}"
  let env ← importModules imports {} 0
    (plugins := #[]) (leakEnv := false) (loadExts := false) (level := .private)
    (arts := selection.artifacts)
  phase "PRIVATE_IMPORT_COMPLETED"
  if env.header.imports != imports then fail "ROOT_IMPORT_MISMATCH"
  let modules := env.header.modules
  let data := env.header.moduleData
  if modules.isEmpty || modules.size > moduleMaximum || modules.size != data.size then
    fail "IMPORTED_MODULE_CENSUS"
  let mut names : Std.HashSet Name := {}
  for entry in modules do
    requireModuleName entry.module
    if names.contains entry.module then fail "DUPLICATE_IMPORTED_MODULE"
    names := names.insert entry.module
  for root in imports do
    if !names.contains root.module then fail "MISSING_IMPORTED_ROOT"
  if replay && selection.moduleNames.size != modules.size then
    fail "UNUSED_OR_MISSING_BOUND_MODULE"
  let mut rows : Array Json := #[]
  let mut edgeCount := 0
  let mut metadataBytes := 0
  for i in [:modules.size] do
    let entry := modules[i]!
    let own := data[i]!
    if !own.isModule then fail "LEGACY_MODULE_LAYOUT_UNSUPPORTED"
    if !entry.hasData || !entry.importAll then fail "FULL_PRIVATE_MODULE_DATA_REQUIRED"
    edgeCount := edgeCount + own.imports.size
    if edgeCount > importEdgeMaximum then fail "DIRECT_IMPORT_EDGE_BOUND"
    for dependency in own.imports do
      if !names.contains dependency.module then fail "UNRESOLVED_TRANSITIVE_IMPORT"
    if !replay then
      -- Same explicit search path as import. These are candidate locators,
      -- not proof of stable bytes: the controller snapshots and fresh-replays.
      let base ← reportPath (← findOLean entry.module)
      selection ← addParts selection entry.module (moduleParts base)
    let some paths := selection.paths.find? entry.module | fail "BOUND_MODULE_MISSING"
    let some counts := selection.byteCounts.find? entry.module | fail "BOUND_PART_COUNTS_MISSING"
    -- Detect size/type changes after replay import. Same-size changes still
    -- require the controller's exact hashes and protected snapshot discipline.
    for j in [:paths.size] do
      let metadata ← (nativePath paths[j]!).symlinkMetadata
      if metadata.type != .file || metadata.byteSize.toNat != counts[j]! then
        fail "ARTIFACT_CHANGED_DURING_COLLECTION"
    let direct ← own.imports.mapM importJson
    let row := Json.mkObj [
      ("module", ← ExprCodec.encodeName entry.module), ("is_module", toJson (1 : Nat)),
      ("imports", .arr direct), ("effective", effectiveJson entry),
      ("parts", matrixJson (paths.map (fun p => Json.str p.toString))),
      ("part_bytes", matrixJson (counts.map toJson))]
    metadataBytes := metadataBytes + row.compress.utf8ByteSize
    if metadataBytes > reportMaximum then fail "REPORT_BYTE_BOUND"
    rows := rows.push row
  let result := Json.mkObj [
    ("schema", .str "DMKN_ORDINARY_BASELINE_ARTIFACT_REPORT_V1"),
    ("assurance", .str "INERT_ARTIFACT_CLOSURE_NOT_MATHEMATICAL_ACCEPTANCE"),
    ("mode", .str mode), ("roots", .arr (← imports.mapM importJson)),
    ("modules", .arr rows), ("module_count", toJson modules.size),
    ("part_count", toJson (modules.size * 5)),
    ("direct_import_edges", toJson edgeCount), ("artifact_bytes", toJson selection.totalBytes)]
  let bytes := result.compress.toUTF8
  if bytes.size > reportMaximum then fail "REPORT_BYTE_BOUND"
  let output ← IO.FS.Handle.mk (nativePath report) .writeNew
  output.write bytes
  output.flush
  phase s!"REPORT_WRITTEN modules={modules.size} parts={modules.size * 5} bytes={selection.totalBytes}"

end OrdinaryLean.BaselineArtifacts
