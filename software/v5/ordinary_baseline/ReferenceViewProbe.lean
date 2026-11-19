import BaselineArtifactCore04

/- One retained-snapshot exported-view census. This diagnostic does not compare
   types or bodies, check proofs, register a reference, or confer any authority. -/

open Lean

namespace OrdinaryLean.ReferenceViewProbe

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"ORDINARY_REFERENCE_VIEW_PROBE {message}"

def readJson (path : System.FilePath) (maximum : Nat) : IO Json := do
  let metadata ← (BaselineArtifacts.nativePath path).symlinkMetadata
  if metadata.type != .file || metadata.numLinks != 1 ||
      metadata.byteSize.toNat > maximum then fail "INPUT_FILE_OR_BOUND"
  let (value, size) ← BaselineArtifacts.readRequest path
  if size > maximum then fail "INPUT_BYTE_BOUND"
  return value

def kind (info : ConstantInfo) : String :=
  match info with
  | .axiomInfo _ => "axiom"
  | .defnInfo _ => "definition"
  | .thmInfo _ => "theorem"
  | .opaqueInfo _ => "opaque"
  | .inductInfo _ => "inductive"
  | .ctorInfo _ => "constructor"
  | .recInfo _ => "recursor"
  | .quotInfo _ => "quotient"

def group (info : ConstantInfo) : Option (List Name) :=
  match info with
  | .defnInfo d => some d.all
  | .thmInfo d => some d.all
  | .opaqueInfo d => some d.all
  | .inductInfo d => some d.all
  | .recInfo d => some d.all
  | _ => none

def facts (info : Option ConstantInfo) : Json :=
  match info with
  | none => Json.mkObj [("present", toJson (0 : Nat))]
  | some info => Json.mkObj [
      ("present", toJson (1 : Nat)), ("kind", .str (kind info)),
      ("unsafe", BaselineArtifacts.bit info.isUnsafe),
      ("partial", BaselineArtifacts.bit info.isPartial),
      ("group_count", (group info).map (fun names => toJson names.length) |>.getD (.str "not_applicable")),
      ("singleton_group", (group info).map (fun names =>
        BaselineArtifacts.bit (names == [info.name])) |>.getD (.str "not_applicable"))]

def checkSnapshotView (env : Environment) (selection : BaselineArtifacts.Selection)
    (imports : Array Import) : IO (Array Name) := do
  if env.header.imports != imports || !env.header.isModule then fail "SNAPSHOT_ROOT_IMPORTS"
  let modules := env.header.modules
  let data := env.header.moduleData
  if modules.isEmpty || modules.size > BaselineArtifacts.moduleMaximum ||
      modules.size != data.size then fail "SNAPSHOT_MODULE_CENSUS"
  let mut seen : Std.HashSet Name := {}
  let mut edges := 0
  for i in [:modules.size] do
    let entry := modules[i]!
    BaselineArtifacts.requireModuleName entry.module
    if seen.contains entry.module || (selection.artifacts.find? entry.module).isNone then
      fail "UNBOUND_OR_DUPLICATE_IMPORTED_MODULE"
    if !data[i]!.isModule then fail "LEGACY_IMPORTED_MODULE"
    edges := edges + data[i]!.imports.size
    if edges > BaselineArtifacts.importEdgeMaximum then fail "SNAPSHOT_IMPORT_EDGE_BOUND"
    for dependency in data[i]!.imports do
      if (selection.artifacts.find? dependency.module).isNone then
        fail "SNAPSHOT_DEPENDENCY_NOT_BOUND"
    seen := seen.insert entry.module
  for root in imports do
    if !seen.contains root.module then fail "SNAPSHOT_ROOT_NOT_IMPORTED"
  return modules.map (fun entry => entry.module)

def checkArtifactSizes (selection : BaselineArtifacts.Selection) : IO Unit := do
  for name in selection.moduleNames do
    let some paths := selection.paths.find? name | fail "SNAPSHOT_PART_PATHS"
    let some counts := selection.byteCounts.find? name | fail "SNAPSHOT_PART_COUNTS"
    for i in [:paths.size] do
      let metadata ← (BaselineArtifacts.nativePath paths[i]!).symlinkMetadata
      if metadata.type != .file || metadata.byteSize.toNat != counts[i]! then
        fail "SNAPSHOT_PART_CHANGED"

def expectedRow (row : Json) (origin : String) : IO (Name × Json) := do
  let fields ← ExprCodec.arrayOf row (some 5)
  let name ← ExprCodec.decodeName fields[0]!
  CheckedExtension.requireName name
  let expectedKind ← ExprCodec.natOf fields[1]!
  return (name, Json.mkObj [("name", ← ExprCodec.encodeName name),
    ("origin", .str origin), ("expected_kind", toJson expectedKind)])

def run (inventoryPath artifactMapPath requestPath reportPath : System.FilePath) : IO Unit := do
  BaselineArtifacts.requireFresh reportPath
  let inventory ← ExprCodec.arrayOf (← readJson inventoryPath 1048576)
  if inventory.size != 581 then fail "EXPECTED_BASIS_COUNT"
  let artifactMap ← readJson artifactMapPath BaselineArtifacts.replayRequestMaximum
  BaselineArtifacts.exactObject artifactMap #["schema", "mode", "modules", "artifacts"]
  if (← ExprCodec.jsonResult (← BaselineArtifacts.field artifactMap "schema").getStr?) !=
      "DMKN_ORDINARY_BASELINE_ARTIFACT_REQUEST_V1" ||
      (← ExprCodec.jsonResult (← BaselineArtifacts.field artifactMap "mode").getStr?) != "replay" then
    fail "EXPLICIT_SNAPSHOT_REPLAY_REQUIRED"
  let imports ← BaselineArtifacts.rootModules (← BaselineArtifacts.field artifactMap "modules")
  let selection ← BaselineArtifacts.replaySelection (← BaselineArtifacts.field artifactMap "artifacts")
  let request ← readJson requestPath 1048576
  BaselineArtifacts.exactObject request #["schema", "semantic_id", "foundation_id", "context_root",
    "snapshot_id", "support_id", "units", "targets"]
  if (← ExprCodec.jsonResult (← BaselineArtifacts.field request "schema").getStr?) !=
      "DMKN_ORDINARY_REFERENCE_BASE_REQUEST_V1" then fail "REQUEST_SCHEMA"
  let units ← ExprCodec.arrayOf (← BaselineArtifacts.field request "units")
  if units.size != 6 then fail "EXPECTED_SELECTED_UNIT_COUNT"
  let mut expected : Array (Name × Json) := #[]
  for row in inventory do expected := expected.push (← expectedRow row "basis")
  for entry in units do
    BaselineArtifacts.exactObject entry #["unit_id", "unit", "outputs"]
    let raw ← ExprCodec.arrayOf (← BaselineArtifacts.field entry "unit") (some 3)
    let rows ← ExprCodec.arrayOf raw[2]!
    if rows.isEmpty || rows.size > 4 then fail "EXPECTED_SELECTED_GROUP_COUNT"
    for row in rows do expected := expected.push (← expectedRow row "selected")
  if expected.size != 590 then fail "EXPECTED_NAME_COUNT"
  let mut seen : Std.HashSet Name := {}
  for (name, _) in expected do
    if seen.contains name then fail "DUPLICATE_EXPECTED_NAME"
    seen := seen.insert name
  searchPathRef.set []
  BaselineArtifacts.phase "VIEW_PROBE_BEFORE_ONE_EXPORTED_IMPORT"
  let env ← importModules imports {} 0
    (plugins := #[]) (leakEnv := false) (loadExts := false) (level := .exported)
    (arts := selection.artifacts)
  let moduleNames ← checkSnapshotView env selection imports
  let frontend := env.setExporting true
  let kernel := env.toKernelEnv
  let mut rows : Array Json := #[]
  let mut frontendMissing := 0
  let mut kernelMissing := 0
  let mut frontendAxioms := 0
  let mut kernelAxioms := 0
  for (name, label) in expected do
    let f := frontend.find? name (skipRealize := true)
    let k := kernel.find? name
    frontendMissing := frontendMissing + (if f.isNone then 1 else 0)
    kernelMissing := kernelMissing + (if k.isNone then 1 else 0)
    frontendAxioms := frontendAxioms + (if f.any (fun i => kind i == "axiom") then 1 else 0)
    kernelAxioms := kernelAxioms + (if k.any (fun i => kind i == "axiom") then 1 else 0)
    rows := rows.push (Json.mkObj [("expected", label), ("frontend", facts f), ("kernel", facts k)])
  checkArtifactSizes selection
  let report := Json.mkObj [
    ("schema", .str "DMKN_ORDINARY_REFERENCE_VIEW_PROBE_V1"),
    ("assurance", .str "DIAGNOSTIC_ONLY_NO_CORRESPONDENCE_OR_ACCEPTANCE"),
    ("basis_count", toJson inventory.size), ("selected_count", toJson (expected.size - inventory.size)),
    ("exported_module_count", toJson moduleNames.size),
    ("exported_module_names", .arr (← moduleNames.mapM (fun name => ExprCodec.encodeName name))),
    ("import_count", toJson (1 : Nat)),
    ("frontend_missing", toJson frontendMissing), ("kernel_missing", toJson kernelMissing),
    ("frontend_axioms", toJson frontendAxioms), ("kernel_axioms", toJson kernelAxioms), ("rows", .arr rows)]
  let bytes := report.compress.toUTF8
  if bytes.size > 1048576 then fail "REPORT_BYTE_BOUND"
  let output ← IO.FS.Handle.mk (BaselineArtifacts.nativePath reportPath) .writeNew
  output.write bytes
  output.flush
  BaselineArtifacts.phase s!"VIEW_PROBE_WRITTEN names={rows.size} bytes={bytes.size}"

end OrdinaryLean.ReferenceViewProbe

def main (args : List String) : IO UInt32 := do
  try
    match args with
    | [inventory, artifactMap, request, report] =>
        OrdinaryLean.ReferenceViewProbe.run
          (← OrdinaryLean.BaselineArtifacts.absolutePath inventory)
          (← OrdinaryLean.BaselineArtifacts.absolutePath artifactMap)
          (← OrdinaryLean.BaselineArtifacts.absolutePath request)
          (← OrdinaryLean.BaselineArtifacts.absolutePath report)
        return 0
    | _ => OrdinaryLean.ReferenceViewProbe.fail "USAGE inventory replay-map request report"
  catch error =>
    let stderr ← IO.getStderr
    stderr.putStrLn (String.ofList (error.toString.toList.take 2048))
    stderr.flush
    return 1
