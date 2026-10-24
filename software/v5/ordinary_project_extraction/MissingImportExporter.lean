import OrdinaryExport

/- Native local-library extraction only. The old installed-Std request remains
   separate from the explicit owner-approved local-project request. Exactly one
   private environment is imported; helpers are not a second environment.
   Parent lookups only cut serialization. Complete supplemental units still need
   independent receiver checking. Approved local artifacts are not peer input,
   hermetically pinned library contents, or a new mathematical trust mode. -/

open Lean

namespace OrdinaryLean.MissingImportExporter

def frameMaximum : Nat := 1048576
def protocolMaximum : Nat := 33554432
def lookupMaximum : Nat := 65536

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"ORDINARY_MISSING_IMPORT {message}"

def phase (message : String) : IO Unit := do
  let stderr ← IO.getStderr
  stderr.putStrLn s!"ORDINARY_MISSING_IMPORT_PHASE {message}"
  stderr.flush

def absolutePath (raw : String) : IO System.FilePath := do
  let path := System.FilePath.mk raw
  if !path.isAbsolute || path.toString.utf8ByteSize > 32768 then
    fail "ABSOLUTE_BOUNDED_PATH_REQUIRED"
  if path.components.contains "." || path.components.contains ".." then
    fail "DOT_PATH_COMPONENT"
  return path

/- Same filesystem-spelling rule as the reviewed OrdinaryModule04 boundary.
   Requests/reports retain their spelling. Never change a dot/space-ended path's
   referent by suppressing Win32 trimming. No new UNC/device-path support. -/
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

/-- Bound tokens/depth before Json.parse. The protected controller separately
    authenticates canonical request bytes and supplies exact canonical replies. -/
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

def parseBounded (bytes : ByteArray) : IO Json := do
  if bytes.isEmpty || bytes.size > frameMaximum then fail "JSON_BYTE_BOUND"
  lexicalPreflight bytes
  let some text := String.fromUTF8? bytes | fail "JSON_UTF8"
  if text.toUTF8 != bytes then fail "JSON_UTF8_CANONICAL"
  match Json.parse text with
  | .ok value => return value
  | .error _ => fail "JSON_PARSE"

def readRequest (path : System.FilePath) : IO Json := do
  let path := nativePath path
  if (← path.metadata).byteSize.toNat > frameMaximum then fail "REQUEST_BYTE_BOUND"
  let handle ← IO.FS.Handle.mk path .read
  let mut bytes : ByteArray := ⟨#[]⟩
  while true do
    let chunk ← handle.read (USize.ofNat (min 65536 (frameMaximum + 1 - bytes.size)))
    if chunk.isEmpty then break
    bytes := bytes ++ chunk
    if bytes.size > frameMaximum then fail "REQUEST_BYTE_BOUND"
  parseBounded bytes

def exactObject (value : Json) (keys : Array String) : IO Unit := do
  let object ← ExprCodec.jsonResult value.getObj?
  if object.size != keys.size then fail "JSON_EXACT_FIELDS"
  for key in keys do
    if (object.get? key).isNone then fail "JSON_MISSING_FIELD"

def field (value : Json) (key : String) : IO Json :=
  ExprCodec.jsonResult (value.getObjVal? key)

def identityOf (value : Json) : IO String := do
  let text ← ExprCodec.jsonResult value.getStr?
  if text.utf8ByteSize != 64 || !text.toList.all (fun c =>
      ('0' ≤ c && c ≤ '9') || ('a' ≤ c && c ≤ 'f')) then fail "IDENTITY_SHAPE"
  return text

def namesOf (value : Json) (maximum : Nat) : IO (Array Name) := do
  let raw ← ExprCodec.arrayOf value
  if raw.isEmpty || raw.size > maximum then fail "NAME_COUNT_BOUND"
  let mut result : Array Name := #[]
  let mut seen : Std.HashSet Name := {}
  for encoded in raw do
    let name ← ExprCodec.decodeName encoded
    CheckedExtension.requireName name
    if seen.contains name then fail "DUPLICATE_NAME"
    seen := seen.insert name
    result := result.push name
  return result

/-- Filesystem module grammar is deliberately narrower than formal Name. -/
def identifierStart (c : Char) : Bool :=
  ('A' ≤ c && c ≤ 'Z') || ('a' ≤ c && c ≤ 'z') || c == '_'

def moduleComponent (part : String) : Bool :=
  let letters := part.toList
  let valid := match letters with
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
    -- This lane deliberately supports ordinary Windows drive paths only.
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
    -- The protected controller additionally checks every ancestor for reparses.
    seen := seen.insert key
    paths := paths.push path
  return paths.toList

structure Capacity where
  units : Nat
  bytes : Nat
  encodedNodes : Nat

def capacityOf (value : Json) : IO Capacity := do
  exactObject value #["units", "bytes", "encoded_nodes"]
  let units ← ExprCodec.natOf (← field value "units")
  let bytes ← ExprCodec.natOf (← field value "bytes")
  let encodedNodes ← ExprCodec.natOf (← field value "encoded_nodes")
  if units == 0 || units > 32 || bytes == 0 || bytes > 4194304 ||
      encodedNodes == 0 || encodedNodes > 131072 then
    fail "PROJECT_CAPACITY_RANGE"
  return { units, bytes, encodedNodes }

def limitsFor (capacity : Option Capacity) : Export.Limits :=
  match capacity with
  | none => { maxUnits := 1024, maxScanNodes := 2097152 }
  | some cap =>
      let originalExpr : ExprCodec.Limits := {}
      { maxTargets := 32
        maxUnits := cap.units
        maxUnitBytes := cap.bytes
        maxOutputBytes := cap.bytes
        maxScanNodes := 2097152
        codec := {
          maxUnitNodes := cap.encodedNodes
          expr := {
            originalExpr with
            maxExprs := min originalExpr.maxExprs cap.encodedNodes
            maxLevels := min originalExpr.maxLevels cap.encodedNodes } } }

/-- Exact encoded DAG count, not the exporter's distinct traversal count.
    This deliberately follows export: shared helper bytes stay unchanged.
    Per-unit limits bound earlier encoding; a late aggregate refusal is possible. -/
def requireEncodedCapacity (units : Array Json) (limits : DeclCodec.Limits)
    (maximum : Nat) : IO Unit := do
  let mut total := 0
  for packet in units do
    let parts ← ExprCodec.arrayOf packet (some 3)
    total := total + (← DeclCodec.descriptorNodes parts[1]! limits)
    if total > maximum then fail "PROJECT_ENCODED_NODE_CAPACITY"
    for row in (← ExprCodec.arrayOf parts[2]!) do
      total := total + (← DeclCodec.inventoryNodes row limits)
      if total > maximum then fail "PROJECT_ENCODED_NODE_CAPACITY"

def requireFresh (path : System.FilePath) : IO Unit := do
  let present ← try
    discard (nativePath path).symlinkMetadata
    pure true
  catch error =>
    match error with
    | .noFileOrDirectory .. => pure false
    | _ => throw error
  if present then fail "FRESH_OUTPUT_REQUIRED"

def charge (used : IO.Ref Nat) (count : Nat) : IO Unit := do
  let before ← used.get
  if before + count > protocolMaximum then fail "AGGREGATE_PROTOCOL_BYTE_BOUND"
  used.set (before + count)

def sendFrame (stdout : IO.FS.Stream) (used : IO.Ref Nat) (packet : Json) : IO Unit := do
  let bytes := packet.compress.toUTF8
  if bytes.isEmpty || bytes.size > frameMaximum then fail "OUTBOUND_FRAME_BOUND"
  charge used (bytes.size + 1)
  stdout.write bytes
  stdout.write ("\n".toUTF8)
  stdout.flush

/-- One outstanding request, one bounded LF-terminated reply. Reading single
    bytes avoids an unbounded getLine allocation or a large blocking fread on
    a pipe. Parent supervision enforces the nonrenewing overall deadline. -/
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
  parseBounded bytes

def run (sysroot requestPath outputPath : System.FilePath) : IO Unit := do
  if outputPath == requestPath then fail "REQUEST_OUTPUT_ALIAS"
  requireFresh outputPath
  let request ← readRequest requestPath
  let schema ← ExprCodec.jsonResult (← field request "schema").getStr?
  let project := schema == "DMKN_ORDINARY_PROJECT_MISSING_IMPORT_REQUEST_V1"
  if project then
    exactObject request #["schema", "profile_id", "context_id", "basis_id",
      "modules", "targets", "project_search_paths", "project_selection_sha256", "capacity"]
  else if schema == "DMKN_ORDINARY_MISSING_IMPORT_REQUEST_V1" then
    exactObject request #["schema", "profile_id", "context_id", "basis_id", "modules", "targets"]
  else fail "REQUEST_SCHEMA"
  let profileId ← identityOf (← field request "profile_id")
  let contextId ← identityOf (← field request "context_id")
  let basisId ← identityOf (← field request "basis_id")
  let moduleValue ← field request "modules"
  let moduleNames ← if project then projectModulesOf moduleValue else namesOf moduleValue 16
  let targets ← namesOf (← field request "targets") (if project then 32 else 1024)
  let capacity ← if project then do
    -- Hash shape is checked here; exact local selection authentication is the
    -- controller's responsibility, not an implication of echoing this label.
    discard (identityOf (← field request "project_selection_sha256"))
    pure (some (← capacityOf (← field request "capacity")))
  else pure none
  let roots ← if project then projectPathsOf (← field request "project_search_paths")
    else pure []
  let limits := limitsFor capacity
  let mut imports : Array Import := #[]
  for name in moduleNames do
    if !project && !(Name.isPrefixOf `Std name) then fail "INSTALLED_STD_MODULE_REQUIRED"
    imports := imports.push { module := name }
  -- Runtime-first, then the exact ordered approved roots. No inherited path,
  -- supplementary source directory, helper environment, meta import or plugins.
  let paths := (sysroot / "lib" / "lean") :: roots
  searchPathRef.set (paths.map nativePath)
  phase (if project then "BEFORE_APPROVED_PROJECT_IMPORT" else "BEFORE_TRUSTED_INSTALLED_IMPORT")
  let owner ← importModules imports {} 0
    (plugins := #[]) (loadExts := false) (level := .private)
  phase (if project then "APPROVED_PROJECT_IMPORT_COMPLETED" else "TRUSTED_INSTALLED_IMPORT_COMPLETED")
  let kernel := owner.toKernelEnv
  for name in targets do
    let some actual := kernel.find? name | fail s!"TARGET_NOT_IN_SELECTED_LIBRARY name={name}"
    if actual.isAxiom then fail s!"TARGET_MISSING_COMPLETE_DECLARATION name={name}"
    if actual.name != name || actual.isUnsafe || actual.isPartial then
      fail "UNSAFE_TARGET_RECORD"
  let stdin ← IO.getStdin
  let stdout ← IO.getStdout
  let protocolBytes ← IO.mkRef 0
  let sequence ← IO.mkRef 0
  let answers ← IO.mkRef ({} : Std.HashMap Name (Option String))
  let resolve : Name → IO (Option String) := fun name => do
    let cache ← answers.get
    if let some found := cache[name]? then return found
    CheckedExtension.requireName name
    let seq ← sequence.get
    if seq >= lookupMaximum then fail "LOOKUP_COUNT_BOUND"
    let encoded ← ExprCodec.encodeName name
    sendFrame stdout protocolBytes (Json.mkObj [
      ("schema", Json.str "DMKN_ORDINARY_PARENT_LOOKUP_V1"),
      ("seq", toJson seq), ("name", encoded)])
    let response ← receiveFrame stdin protocolBytes
    let status ← ExprCodec.jsonResult (← field response "status").getStr?
    if status == "FOUND" then
      exactObject response #["schema", "seq", "name", "status", "symbol_id"]
    else if status == "ABSENT" then
      exactObject response #["schema", "seq", "name", "status"]
    else fail "REPLY_STATUS"
    if (← ExprCodec.jsonResult (← field response "schema").getStr?) !=
        "DMKN_ORDINARY_PARENT_REPLY_V1" ||
        (← ExprCodec.natOf (← field response "seq")) != seq ||
        (← field response "name") != encoded then fail "REPLY_BINDING"
    let symbol ← if status == "FOUND" then do
      pure (some (← identityOf (← field response "symbol_id")))
    else pure none
    answers.set (cache.insert name symbol)
    sequence.set (seq + 1)
    return symbol
  -- The controller must select the real missing set, not request accepted work.
  for name in targets do
    if (← resolve name).isSome then fail s!"TARGET_ALREADY_ACCEPTED name={name}"
  let indexed : Export.IndexedSource := {
    source := { environment := kernel, grouping := #[], count := 0 }
    members := {} }
  let policy : Export.DynamicBoundary := {
    stop := fun name => do return (← resolve name).isSome
    maxLookups := lookupMaximum
    maxNames := 65536
  }
  let exported ← Export.selectedFromBoundary indexed #[] targets limits (some policy)
  if exported.units.isEmpty then fail "COMPLETE_MISSING_UNITS_REQUIRED"
  if let some cap := capacity then
    requireEncodedCapacity exported.units limits.codec cap.encodedNodes
  let known ← answers.get
  let mut boundary : Array Json := #[]
  for name in exported.boundaryReferences do
    let some (some symbol) := known[name]? | fail "REACHED_BOUNDARY_WITHOUT_REPLY"
    boundary := boundary.push (Json.arr #[← ExprCodec.encodeName name, Json.str symbol])
  let lookupCount ← sequence.get
  let encodedTargets ← targets.mapM (fun name => ExprCodec.encodeName name)
  let statistics := Json.mkObj [
    ("source_records_enumerated", toJson exported.sourceRecords),
    ("selected_units", toJson exported.selectedUnits),
    ("dependency_edges", toJson exported.dependencyEdges),
    ("scan_nodes", toJson exported.scanNodes),
    ("unit_json_bytes", toJson exported.unitBytes),
    ("boundary_imports", toJson boundary.size),
    ("lookup_count", toJson lookupCount)]
  let result := Json.mkObj [
    ("schema", Json.str "DMKN_ORDINARY_MISSING_IMPORT_BUNDLE_V1"),
    ("assurance", Json.str "INERT_OWNER_EXPORT_NOT_MATHEMATICAL_ACCEPTANCE"),
    ("profile_id", Json.str profileId), ("context_id", Json.str contextId),
    ("basis_id", Json.str basisId), ("targets", Json.arr encodedTargets),
    ("boundary_imports", Json.arr boundary), ("units", Json.arr exported.units),
    ("stats", statistics)]
  let bytes := result.compress.toUTF8
  let maximumBytes := match capacity with
    | none => 67108864
    | some cap => cap.bytes
  -- Includes the entire wrapper, boundary and statistics, not just unit bytes.
  if bytes.isEmpty || bytes.size > maximumBytes then fail "BUNDLE_BYTE_BOUND"
  let output ← IO.FS.Handle.mk (nativePath outputPath) .writeNew
  output.write bytes
  output.flush
  phase s!"MISSING_CLOSURE_EXPORTED units={exported.selectedUnits} boundary={boundary.size} lookups={lookupCount} bytes={bytes.size}"
  sendFrame stdout protocolBytes (Json.mkObj [
    ("schema", Json.str "DMKN_ORDINARY_MISSING_IMPORT_DONE_V1"),
    ("lookups", toJson lookupCount), ("units", toJson exported.selectedUnits),
    ("output_bytes", toJson bytes.size)])
  -- DONE is not a success token. The controller now closes stdin and waits for
  -- clean exit. An extra unsolicited response causes refusal, not acceptance.
  if !(← stdin.read 1).isEmpty then fail "TRAILING_REPLY_BYTES"

end OrdinaryLean.MissingImportExporter

def main (args : List String) : IO UInt32 := do
  try
    match args with
    | [sysroot, requestPath, outputPath] =>
        OrdinaryLean.MissingImportExporter.run
          (← OrdinaryLean.MissingImportExporter.absolutePath sysroot)
          (← OrdinaryLean.MissingImportExporter.absolutePath requestPath)
          (← OrdinaryLean.MissingImportExporter.absolutePath outputPath)
        return 0
    | _ => OrdinaryLean.MissingImportExporter.fail "USAGE sysroot request output"
  catch error =>
    let stderr ← IO.getStderr
    stderr.putStrLn (String.ofList (error.toString.toList.take 2048))
    stderr.flush
    return 1
