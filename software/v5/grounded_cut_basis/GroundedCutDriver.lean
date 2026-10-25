import GroundedCut

/- Fixed local driver for the conditional primitive. Only the protected
   controller can bind its input identities and promote its clean process event.
   No owner state, peer code, arbitrary native snapshot, retry or mathematical
   warrant. The one genuine committed basis artifact is authenticated by that
   controller before this process starts; module/path/size alone are not trust. -/

open Lean

namespace OrdinaryLean.GroundedCutDriver

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"GROUNDED_CUT_BASIS_DRIVER {message}"

def pathOf (raw : String) : IO System.FilePath := do
  let path := System.FilePath.mk raw
  if !path.isAbsolute || raw.utf8ByteSize > 32768 ||
      path.components.contains "." || path.components.contains ".." then
    fail "ABSOLUTE_BOUNDED_PATH_REQUIRED"
  return path

/-- Same finite lexical guard as the existing ordinary worker; no general
    JSON numeric token reaches parsing before this bounded scan. -/
def lexical (bytes : ByteArray) : IO Unit := do
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
        value := value * 10 + bytes[i]!.toNat - 48
        if value > 18446744073709551615 then fail "JSON_UINT64"
        i := i + 1
      if i - start > 1 && bytes[start]!.toNat == 48 then fail "JSON_LEADING_ZERO"
      continue
    else if ![9, 10, 13, 32, 44, 58].contains byte then fail "JSON_LEXICAL_TOKEN"
    i := i + 1
  if quoted || escaped || !stack.isEmpty then fail "JSON_UNTERMINATED"

def readJson (path : System.FilePath) (maximum : Nat) : IO Json := do
  if (← path.metadata).byteSize.toNat > maximum then fail "INPUT_BYTE_BOUND"
  let handle ← IO.FS.Handle.mk path .read
  let mut bytes : ByteArray := ⟨#[]⟩
  while true do
    let chunk ← handle.read (USize.ofNat (min 65536 (maximum + 1 - bytes.size)))
    if chunk.isEmpty then break
    bytes := bytes ++ chunk
    if bytes.size > maximum then fail "INPUT_BYTE_BOUND"
  if bytes.isEmpty then fail "INPUT_EMPTY"
  lexical bytes
  let some text := String.fromUTF8? bytes | fail "INPUT_UTF8"
  if text.toUTF8 != bytes then fail "INPUT_UTF8_CANONICAL"
  match Json.parse text with
  | .ok value => return value
  | .error _ => fail "INPUT_JSON"

/-- Only the exact protected basis descriptor's projection is accepted.
    No module list, root selector, parent or caller-supplied name census exists.
    This shape does NOT authenticate the artifact; that is a caller precondition. -/
def basisSnapshotOf (value : Json) : IO GroundedCut.FixedBasisSnapshot := do
  let obj ← ExprCodec.jsonResult value.getObj?
  let keys := #["module_name", "path", "artifact_bytes"]
  if obj.size != keys.size then fail "BASIS_EXACT_FIELDS"
  for key in keys do
    if (obj.get? key).isNone then fail "BASIS_MISSING_FIELD"
  let get (key : String) : IO Json := do
    let some found := obj.get? key | fail "BASIS_MISSING_FIELD"
    return found
  let moduleName ← ExprCodec.decodeName (← get "module_name")
  ExprCodec.requireSemanticName moduleName
  if moduleName.isAnonymous then fail "BASIS_MODULE_REQUIRED"
  let path ← pathOf (← ExprCodec.jsonResult (← get "path").getStr?)
  let artifactBytes ← ExprCodec.natOf (← get "artifact_bytes")
  if artifactBytes == 0 || artifactBytes > 1073741824 then fail "BASIS_ARTIFACT_BYTE_BOUND"
  return { moduleName, path, artifactBytes }

def run (args : List String) : IO Unit := do
  let [seedArg, inventoryArg, requestArg, reportArg] := args
    | fail "FIXED_ARGUMENTS"
  let seedPath ← pathOf seedArg
  let inventoryPath ← pathOf inventoryArg
  let requestPath ← pathOf requestArg
  let reportPath ← pathOf reportArg
  if [seedPath, inventoryPath, requestPath].contains reportPath then fail "OUTPUT_INPUT_ALIAS"
  let present ← try
    discard reportPath.symlinkMetadata
    pure true
  catch error =>
    match error with
    | .noFileOrDirectory .. => pure false
    | _ => throw error
  if present then fail "FRESH_REPORT_REQUIRED"
  let request ← readJson requestPath 67108864
  let obj ← ExprCodec.jsonResult request.getObj?
  let keys := #["schema", "request_id", "basis_snapshot", "concrete_units",
    "signature_rows", "new_unit"]
  if obj.size != keys.size then fail "EXACT_FIELDS"
  for key in keys do
    if (obj.get? key).isNone then fail "MISSING_FIELD"
  let get (key : String) : IO Json := do
    let some value := obj.get? key | fail "MISSING_FIELD"
    return value
  if (← ExprCodec.jsonResult (← get "schema").getStr?) != "DMKN_GROUNDED_CUT_BASIS_REQUEST_V1" then
    fail "SCHEMA"
  let requestId ← OwnerRebind.identityOf (← get "request_id")
  let snapshot ← basisSnapshotOf (← get "basis_snapshot")
  if snapshot.path == reportPath then fail "OUTPUT_BASIS_ALIAS"
  let concrete ← ExprCodec.arrayOf (← get "concrete_units")
  let signatures ← ExprCodec.arrayOf (← get "signature_rows")
  let newUnit ← get "new_unit"
  let seed ← readJson seedPath 1048576
  let inventory ← readJson inventoryPath 1048576
  let result ← GroundedCut.check snapshot seed inventory concrete signatures newUnit
  let labels ← result.signatureLabels.mapM fun label => do
    return Json.arr #[← ExprCodec.encodeName label.name, Json.str label.symbolId]
  let report := Json.mkObj [
    ("schema", Json.str "DMKN_GROUNDED_CUT_BASIS_CONDITIONAL_OUTPUT_V1"),
    ("assurance", Json.str "CONDITIONAL_KERNEL_JUDGMENT_NOT_LOCAL_WARRANT"),
    ("request_id", Json.str requestId),
    ("theorem_name", ← ExprCodec.encodeName result.theoremName),
    ("theorem_inventory", result.theoremInventory),
    ("signature_labels", Json.arr labels),
    ("counts", Json.mkObj [
      ("concrete_units", toJson result.concreteUnits),
      ("concrete_names", toJson result.concreteNames),
      ("signatures", toJson result.signatures),
      ("scratch_names", toJson result.scratchNames),
      ("input_bytes", toJson result.inputBytes),
      ("basis_artifact_bytes", toJson result.basisArtifactBytes),
      ("encoded_nodes", toJson result.encodedNodes),
      ("scan_nodes", toJson result.scanNodes),
      ("kernel_calls", toJson result.kernelCalls)])]
  let raw := report.compress.toUTF8
  if raw.size > 16777216 then fail "REPORT_BYTE_BOUND"
  let output ← IO.FS.Handle.mk reportPath .writeNew
  output.write raw
  output.flush

end OrdinaryLean.GroundedCutDriver

def main (args : List String) : IO UInt32 := do
  OrdinaryLean.GroundedCutDriver.run args
  return 0
