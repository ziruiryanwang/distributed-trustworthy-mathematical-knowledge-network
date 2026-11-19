import BaselineArtifactCore04
import OwnerRebind

/- Protected original-reference materialization, not peer acceptance.
   The owner authenticates the live reference, exact snapshot/support and current
   warrants. This program checks only new units over that preserved interpretation.
   Native digest fields are binding labels; the worker/controller hash the bytes.
   No old proofs, saved reports or matching names establish authority here. -/

open Lean

namespace OrdinaryLean.ReferenceModule

def requestMaximum : Nat := 4194304
def planMaximum : Nat := 1048576
def reportMaximum : Nat := 8388608
def artifactMaximum : Nat := 67108864
def nodeMaximum : Nat := 131072
def codecLimits : DeclCodec.Limits := { maxUnitNodes := nodeMaximum }
def checkerLimits : CheckedExtension.Limits := {
  codec := codecLimits
  maxUnits := 32
  maxNewNames := 4096
  maxScanNodes := nodeMaximum }

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"ORDINARY_REFERENCE_MODULE {message}"

abbrev nativePath := BaselineArtifacts.nativePath
abbrev absolutePath := BaselineArtifacts.ordinaryDrivePath
abbrev field := BaselineArtifacts.field
abbrev exactObject := BaselineArtifacts.exactObject
abbrev moduleParts := BaselineArtifacts.moduleParts
abbrev identityOf := OwnerRebind.identityOf

def readJson (path : System.FilePath) (maximum : Nat) : IO Json := do
  let info ← (nativePath path).symlinkMetadata
  if info.type != .file || info.numLinks != 1 || info.byteSize.toNat > maximum then
    fail "ORDINARY_BOUNDED_INPUT_REQUIRED"
  let handle ← IO.FS.Handle.mk (nativePath path) .read
  let mut bytes : ByteArray := ⟨#[]⟩
  while true do
    let chunk ← handle.read (USize.ofNat (min 65536 (maximum + 1 - bytes.size)))
    if chunk.isEmpty then break
    bytes := bytes ++ chunk
    if bytes.size > maximum then fail "INPUT_BYTE_BOUND"
  if bytes.isEmpty then fail "INPUT_EMPTY"
  BaselineArtifacts.lexicalPreflight bytes
  let some text := String.fromUTF8? bytes | fail "INPUT_UTF8"
  if text.toUTF8 != bytes then fail "INPUT_UTF8_CANONICAL"
  ExprCodec.jsonResult (Json.parse text)

def pinnedJson (raw : Json) (maximum : Nat) : IO Json := do
  exactObject raw #["path", "bytes", "sha256"]
  let path ← absolutePath (← ExprCodec.jsonResult (← field raw "path").getStr?)
  let count ← ExprCodec.natOf (← field raw "bytes")
  discard <| identityOf (← field raw "sha256")
  if count == 0 || count > maximum ||
      (← (nativePath path).symlinkMetadata).byteSize.toNat != count then
    fail "PINNED_METADATA_BOUND"
  readJson path count

def encodedNames (names : Array Name) : IO Json :=
  return .arr (← names.mapM (fun name => ExprCodec.encodeName name))

def namesOf (raw : Json) (maximum : Nat) : IO (Array Name) := do
  let rows ← ExprCodec.arrayOf raw
  if rows.size > maximum then fail "NAME_BOUND"
  let mut names := #[]
  let mut seen : Std.HashSet Name := {}
  for row in rows do
    let name ← ExprCodec.decodeName row
    CheckedExtension.requireName name
    if seen.contains name then fail "DUPLICATE_NAME"
    seen := seen.insert name
    names := names.push name
  return names

def bridgeModule (raw : Json) : IO Name := do
  let name ← ExprCodec.decodeName raw
  match name with
  | .str .anonymous component =>
      if !component.startsWith "DMKNBridge_" then fail "MODULE_PREFIX"
      discard <| identityOf (.str (component.drop 11 |>.toString))
      return name
  | _ => fail "TOP_LEVEL_BRIDGE_REQUIRED"

def standardImport (name : Name) : Import :=
  { module := name, importAll := false, isExported := true, isMeta := false }

def rootImports (raw : Json) : IO (Array Import) := do
  let rows ← ExprCodec.arrayOf raw
  if rows.isEmpty || rows.size > 16 || raw.compress.utf8ByteSize > 65536 then
    fail "ROOT_BOUND"
  let mut names := #[]
  for row in rows do
    exactObject row #["module", "import_all", "is_exported", "is_meta"]
    if (← field row "import_all") != toJson (0 : Nat) ||
        (← field row "is_exported") != toJson (1 : Nat) ||
        (← field row "is_meta") != toJson (0 : Nat) then fail "ROOT_FLAGS"
    let name ← BaselineArtifacts.moduleOf (← field row "module")
    if names.contains name then fail "DUPLICATE_ROOT"
    names := names.push name
  return names.map standardImport

structure Binding where
  name : Name
  kind : Nat
  params : Json
  projection : String
  kernelProjection : String
  deriving Inhabited

structure Generated where
  deltaId : String
  moduleName : Name
  imports : Array Import
  addedNames : Array Name
  deriving Inhabited

structure Plan where
  referenceId : String
  parentId : String
  supportId : String
  roots : Array Import
  original : BaselineArtifacts.Selection
  privateModules : Array Name
  publicModules : Array Name
  basis : Array Binding := #[]
  usableBasis : Array Name := #[]
  publicBindings : Array Binding := #[]
  publicUnitCount : Nat := 0
  generated : Array Generated := #[]
  generatedBindings : Array Binding := #[]
  artifacts : NameMap ImportArtifacts := {}

def Plan.imports (plan : Plan) : Array Import :=
  if plan.generated.isEmpty then plan.roots else
    #[standardImport plan.generated.back!.moduleName]

def Plan.externalNames (plan : Plan) : Array Name :=
  plan.usableBasis ++ plan.publicBindings.map (·.name) ++ plan.generatedBindings.map (·.name)

def projectionOf (raw : Json) (kind : Nat) (allowAbsent : Bool) : IO String := do
  let value ← ExprCodec.jsonResult raw.getStr?
  if value == "full" || (allowAbsent && value == "absent") ||
      (kind == 1 && value == "abstract_singleton_definition") ||
      (kind == 2 && value == "erased_singleton_theorem") ||
      (kind == 3 && value == "abstract_singleton_opaque") then return value
  fail "PROJECTION_KIND"

def readBinding (row : Json) (basis : Bool) : IO Binding := do
  if basis then exactObject row #["name", "kind", "level_params", "projection", "kernel_projection"]
  else
    exactObject row #["name", "export_id", "kind", "level_params", "projection", "kernel_projection"]
    discard <| identityOf (← field row "export_id")
  let name ← ExprCodec.decodeName (← field row "name")
  CheckedExtension.requireName name
  let kind ← ExprCodec.natOf (← field row "kind")
  if kind > 7 || (!basis && (kind == 0 || kind == 7)) then fail "ORIGINAL_KIND"
  let params ← field row "level_params"
  discard <| DeclCodec.paramsOf params codecLimits
  return {
    name := name, kind := kind, params := params,
    projection := ← projectionOf (← field row "projection") kind basis,
    kernelProjection := ← projectionOf (← field row "kernel_projection") kind basis }

/- Compact registered metadata is sufficient ONLY under the controller's
   immutable-artifact/import-preservation premise. It is not a new signature
   proof, nor a way to accept a saved V2 report from another party. -/
def readPlan (path inventoryPath : System.FilePath) (request : Json) : IO Plan := do
  let raw ← readJson path planMaximum
  exactObject raw #["schema", "reference_id", "snapshot_id", "support_id", "semantic_id",
    "foundation_id", "implementation_id", "registration_context_root", "parent_delta_id",
    "original_roots", "reference_report", "replay_request", "generated_plan"]
  if (← field raw "schema") != .str "DMKN_ORDINARY_REFERENCE_MODULE_PLAN_V1" then
    fail "PLAN_SCHEMA"
  let referenceId ← identityOf (← field raw "reference_id")
  let supportId ← identityOf (← field raw "support_id")
  let parentId ← ExprCodec.jsonResult (← field raw "parent_delta_id").getStr?
  if !parentId.isEmpty then discard <| identityOf (.str parentId)
  discard <| identityOf (← field raw "implementation_id")
  discard <| identityOf (← field request "reference_plan_sha256")
  for key in #["reference_id", "parent_delta_id", "semantic_id", "foundation_id"] do
    if (← field request key) != (← field raw key) then fail "REQUEST_PLAN_BINDING"
  let roots ← rootImports (← field raw "original_roots")
  let replay ← pinnedJson (← field raw "replay_request") 16777216
  exactObject replay #["schema", "mode", "modules", "artifacts"]
  if (← field replay "schema") != .str "DMKN_ORDINARY_BASELINE_ARTIFACT_REQUEST_V1" ||
      (← field replay "mode") != .str "replay" ||
      (← field replay "modules") != (← encodedNames (roots.map (·.module))) then
    fail "ORIGINAL_REPLAY_BINDING"
  let original ← BaselineArtifacts.replaySelection (← field replay "artifacts")
  for entry in roots do
    if (original.artifacts.find? entry.module).isNone then fail "ORIGINAL_ROOT_MISSING"
  let report ← pinnedJson (← field raw "reference_report") 33554432
  exactObject report #["schema", "assurance", "semantic_id", "foundation_id", "context_root",
    "snapshot_id", "support_id", "targets", "private_unit_ids", "public_units", "public_basis",
    "usable_basis_names", "basis_scan_nodes", "basis_edges", "basis_pruning_rounds",
    "private_module_names", "public_module_names", "private_unit_count", "private_name_count",
    "public_unit_count", "public_name_count", "unit_array_bytes", "encoded_nodes",
    "private_scan_nodes", "public_scan_nodes", "private_edges", "public_edges", "checked_units", "added_names"]
  if (← field report "schema") != .str "DMKN_ORDINARY_REFERENCE_BASE_REPORT_V2" ||
      (← field report "assurance") != .str "CORRESPONDENCE_REQUIRES_CURRENT_PROTECTED_WARRANTS" ||
      (← field report "context_root") != (← field raw "registration_context_root") ||
      (← field report "checked_units") != toJson (0 : Nat) ||
      (← field report "added_names") != .arr #[] then fail "REGISTERED_REPORT_BINDING"
  for key in #["semantic_id", "foundation_id", "snapshot_id", "support_id"] do
    discard <| identityOf (← field raw key)
    if (← field report key) != (← field raw key) then fail "REGISTERED_REPORT_IDENTITY"
  discard <| identityOf (← field raw "registration_context_root")
  let privateModules ← namesOf (← field report "private_module_names") 4096
  let publicModules ← namesOf (← field report "public_module_names") 4096
  if privateModules.size != original.moduleNames.size || publicModules.isEmpty then
    fail "ORIGINAL_MODULE_CENSUS"
  for name in privateModules do
    if (original.artifacts.find? name).isNone then fail "ORIGINAL_PRIVATE_MODULE"
  for name in publicModules do
    if !privateModules.contains name then fail "ORIGINAL_PUBLIC_MODULE"
  for entry in roots do
    if !publicModules.contains entry.module then fail "ORIGINAL_PUBLIC_ROOT"
  let mut plan : Plan := {
    referenceId := referenceId, parentId := parentId, supportId := supportId,
    roots := roots, original := original, privateModules := privateModules,
    publicModules := publicModules, artifacts := original.artifacts }
  let inventory ← ExprCodec.arrayOf (← readJson inventoryPath 1048576) (some 581)
  let basisRows ← ExprCodec.arrayOf (← field report "public_basis") (some 581)
  let mut allNames : Std.HashSet Name := {}
  for i in [:basisRows.size] do
    let binding ← readBinding basisRows[i]! true
    let old ← ExprCodec.arrayOf inventory[i]! (some 5)
    if old[0]! != (← ExprCodec.encodeName binding.name) ||
        old[1]! != toJson binding.kind ||
        old[2]! != toJson (← ExprCodec.arrayOf binding.params).size ||
        allNames.contains binding.name then fail "FIXED_BASIS_METADATA"
    allNames := allNames.insert binding.name
    plan := { plan with basis := plan.basis.push binding }
  let usable ← namesOf (← field report "usable_basis_names") 581
  let selected : Std.HashSet Name := usable.foldl (fun set name => set.insert name) {}
  let ordered := plan.basis.filter (fun row => selected.contains row.name)
  if ordered.map (·.name) != usable then fail "USABLE_BASIS_ORDER"
  for row in ordered do
    if row.projection == "absent" || row.kernelProjection == "absent" then
      fail "USABLE_BASIS_ABSENT"
  plan := { plan with usableBasis := usable }
  let publicUnits ← ExprCodec.arrayOf (← field report "public_units")
  if publicUnits.isEmpty || publicUnits.size > 8192 then fail "REFERENCE_UNIT_BOUND"
  let mut unitIds : Std.HashSet String := {}
  for unit in publicUnits do
    exactObject unit #["unit_id", "outputs"]
    let id ← identityOf (← field unit "unit_id")
    if unitIds.contains id then fail "REFERENCE_DUPLICATE_UNIT"
    unitIds := unitIds.insert id
    let outputs ← ExprCodec.arrayOf (← field unit "outputs")
    if outputs.isEmpty || outputs.size > 262144 then fail "REFERENCE_OUTPUT_BOUND"
    for output in outputs do
      let binding ← readBinding output false
      if allNames.contains binding.name then fail "REFERENCE_NAME_COLLISION"
      allNames := allNames.insert binding.name
      plan := { plan with publicBindings := plan.publicBindings.push binding }
      if plan.publicBindings.size > 262144 then fail "REFERENCE_NAME_BOUND"
  if (← field report "public_unit_count") != toJson publicUnits.size ||
      (← field report "public_name_count") != toJson plan.publicBindings.size then
    fail "REFERENCE_PUBLIC_CENSUS"
  plan := { plan with publicUnitCount := publicUnits.size }
  let generated ← pinnedJson (← field raw "generated_plan") 4194304
  exactObject generated #["schema", "reference_id", "support_id", "delta_id", "modules", "bindings"]
  if (← field generated "schema") != .str "DMKN_ORDINARY_REFERENCE_GENERATED_PLAN_V1" ||
      (← field generated "reference_id") != .str referenceId ||
      (← field generated "support_id") != .str supportId ||
      (← field generated "delta_id") != .str parentId then fail "GENERATED_PLAN_BINDING"
  let modules ← ExprCodec.arrayOf (← field generated "modules")
  let bindings ← ExprCodec.arrayOf (← field generated "bindings")
  if modules.size > 32 || bindings.size > 1024 ||
      (parentId.isEmpty != modules.isEmpty) || (parentId.isEmpty != bindings.isEmpty) then
    fail "GENERATED_CHAIN_BOUND"
  let mut paths := original.pathKeys
  let mut deltaIds : Std.HashSet String := {}
  let mut added : Std.HashSet Name := {}
  let mut generatedBytes := 0
  for row in modules do
    exactObject row #["delta_id", "module_name", "direct_imports", "added_names", "artifact_parts"]
    let deltaId ← identityOf (← field row "delta_id")
    let moduleName ← bridgeModule (← field row "module_name")
    if deltaIds.contains deltaId || (plan.artifacts.find? moduleName).isSome then
      fail "GENERATED_MODULE_COLLISION"
    deltaIds := deltaIds.insert deltaId
    let imports := plan.imports
    if (← field row "direct_imports") != (← encodedNames (imports.map (·.module))) then
      fail "GENERATED_IMPORT_BINDING"
    let names ← namesOf (← field row "added_names") 4096
    if names.isEmpty then fail "GENERATED_EMPTY_MODULE"
    for name in names do
      if allNames.contains name || added.contains name then fail "GENERATED_NAME_COLLISION"
      added := added.insert name
      if added.size > 16384 then fail "GENERATED_NAME_BOUND"
    let partRows ← ExprCodec.arrayOf (← field row "artifact_parts") (some 5)
    let mut partPaths := #[]
    let mut moduleBytes := 0
    for part in partRows do
      exactObject part #["path", "bytes", "sha256"]
      let path ← absolutePath (← ExprCodec.jsonResult (← field part "path").getStr?)
      let key := BaselineArtifacts.pathKey path
      if paths.contains key then fail "GENERATED_PART_ALIAS"
      paths := paths.insert key
      discard <| identityOf (← field part "sha256")
      let count ← ExprCodec.natOf (← field part "bytes")
      moduleBytes := moduleBytes + count
      generatedBytes := generatedBytes + count
      if count == 0 || moduleBytes > artifactMaximum || generatedBytes > 268435456 then
        fail "GENERATED_ARTIFACT_BOUND"
      let info ← (nativePath path).symlinkMetadata
      if info.type != .file || info.numLinks != 1 || info.byteSize.toNat != count then
        fail "GENERATED_ARTIFACT_METADATA"
      partPaths := partPaths.push path
    if partPaths[0]!.fileName != some (moduleName.toString ++ ".olean") ||
        partPaths != moduleParts partPaths[0]! then fail "GENERATED_ARTIFACT_NAMES"
    plan := { plan with
      generated := plan.generated.push {
        deltaId := deltaId, moduleName := moduleName, imports := imports, addedNames := names },
      artifacts := plan.artifacts.insert moduleName (BaselineArtifacts.asArtifacts partPaths) }
  if !plan.generated.isEmpty && plan.generated.back!.deltaId != parentId then
    fail "GENERATED_PARENT_ID"
  let mut realized : Std.HashSet Name := {}
  for unit in bindings do
    exactObject unit #["unit_id", "outputs", "realization"]
    let id ← identityOf (← field unit "unit_id")
    if unitIds.contains id || (← field unit "realization") != .str "added" then
      fail "GENERATED_UNIT_ID_OR_REALIZATION"
    unitIds := unitIds.insert id
    let outputs ← ExprCodec.arrayOf (← field unit "outputs")
    if outputs.isEmpty || outputs.size > 4096 then fail "GENERATED_OUTPUT_BOUND"
    for output in outputs do
      exactObject output #["name", "export_id", "kind", "level_params", "inventory_sha256"]
      let name ← ExprCodec.decodeName (← field output "name")
      if !added.contains name || realized.contains name then fail "GENERATED_BINDING_CENSUS"
      realized := realized.insert name
      discard <| identityOf (← field output "export_id")
      discard <| identityOf (← field output "inventory_sha256")
      let kind ← ExprCodec.natOf (← field output "kind")
      if kind < 1 || kind > 6 then fail "GENERATED_KIND"
      let params ← field output "level_params"
      discard <| DeclCodec.paramsOf params codecLimits
      plan := { plan with generatedBindings := plan.generatedBindings.push {
        name := name, kind := kind, params := params,
        projection := "full", kernelProjection := "full" } }
  if realized.size != added.size then fail "GENERATED_ADDED_CENSUS"
  return plan

def kindOf : ConstantInfo → Nat
  | .axiomInfo _ => 0 | .defnInfo _ => 1 | .thmInfo _ => 2 | .opaqueInfo _ => 3
  | .inductInfo _ => 4 | .ctorInfo _ => 5 | .recInfo _ => 6 | .quotInfo _ => 7

def checkRecord (actual : Option ConstantInfo) (row : Binding) (projection : String)
    (basis : Bool) : IO Unit := do
  if projection == "absent" then
    if actual.isSome then fail s!"REGISTERED_ABSENCE_CHANGED name={row.name}"
    return
  let some info := actual | fail s!"REGISTERED_RECORD_MISSING name={row.name}"
  if info.name != row.name || info.isUnsafe || info.isPartial ||
      (← DeclCodec.paramsJson info.levelParams codecLimits) != row.params then
    fail s!"REGISTERED_RECORD_METADATA name={row.name}"
  let expected := if projection == "full" then row.kind else 0
  if kindOf info != expected then fail s!"REGISTERED_PROJECTION_CHANGED name={row.name}"
  if row.kind == 0 && (!basis || !BootstrapProbe.allowedAxioms.contains row.name) then
    fail "REGISTERED_AXIOM_POLICY"
  if row.kind == 7 && (!basis || !BootstrapProbe.quotNames.contains row.name) then
    fail "REGISTERED_QUOTIENT_POLICY"

def checkBaseRecords (env : Environment) (plan : Plan) (publicView : Bool) : IO Unit := do
  let frontend := env.setExporting publicView
  for row in plan.basis do
    checkRecord (frontend.find? row.name (skipRealize := true)) row
      (if publicView then row.projection else "full") true
    checkRecord (env.toKernelEnv.find? row.name) row
      (if publicView then row.kernelProjection else "full") true
  for row in plan.publicBindings do
    checkRecord (frontend.find? row.name (skipRealize := true)) row
      (if publicView then row.projection else "full") false
    checkRecord (env.toKernelEnv.find? row.name) row
      (if publicView then row.kernelProjection else "full") false
  for row in plan.generatedBindings do
    checkRecord (frontend.find? row.name (skipRealize := true)) row "full" false
    checkRecord (env.toKernelEnv.find? row.name) row "full" false

def checkModuleHeader (env : Environment) (moduleName : Name) (names : Array Name)
    (imports : Array Import) : IO Unit := do
  let modules := env.allImportedModuleNames
  let data := env.header.moduleData
  if modules.size != data.size then fail "HEADER_CENSUS"
  let mut count := 0
  let expected : Std.HashSet Name := names.foldl (fun set name => set.insert name) {}
  for i in [:modules.size] do
    if modules[i]! != moduleName then continue
    count := count + 1
    let own := data[i]!
    if !own.isModule || own.imports != imports || own.constNames.size != names.size ||
        own.constants.size != names.size then fail "GENERATED_HEADER"
    let mut seen : Std.HashSet Name := {}
    for name in own.constNames do
      if !expected.contains name || seen.contains name then fail "GENERATED_HEADER_NAMES"
      seen := seen.insert name
  if count != 1 then fail "GENERATED_HEADER_IDENTITY"

def checkBaseHeaders (env : Environment) (plan : Plan) (publicView : Bool)
    (own : Option Name := none) : IO Unit := do
  if !env.header.isModule then fail "MODERN_ENVIRONMENT_REQUIRED"
  for data in env.header.moduleData do
    if !data.isModule then fail "LEGACY_IMPORTED_MODULE"
  let originals := if publicView then plan.publicModules else plan.privateModules
  let suffix := match own with | none => #[] | some name => #[name]
  let expected := originals ++ plan.generated.map (·.moduleName) ++ suffix
  if env.allImportedModuleNames != expected then fail "EXACT_IMPORTED_MODULE_ORDER"
  for item in plan.generated do
    checkModuleHeader env item.moduleName item.addedNames item.imports

def checkInventories (env : Environment) (names : Array Name) (rows : Array Json)
    (publicView : Bool) : IO Unit := do
  if names.size != rows.size then fail "NEW_INVENTORY_CENSUS"
  let frontend := env.setExporting publicView
  for i in [:names.size] do
    for actual in #[frontend.find? names[i]! (skipRealize := true), env.toKernelEnv.find? names[i]!] do
      let some info := actual | fail "NEW_RECORD_MISSING"
      if info.name != names[i]! || info.isAxiom || info.isUnsafe || info.isPartial ||
          (← DeclCodec.inventoryRow info codecLimits) != rows[i]! then
        fail s!"NEW_INVENTORY_MISMATCH name={names[i]!}"

def decodeUnits (rawUnits : Array Json) (plan : Plan) (privateEnv : Environment)
    : IO (Array DeclCodec.DecodedUnit × Array Name × Array Json) := do
  let mut allowed : Std.HashSet Name := {}
  for name in plan.externalNames do
    if allowed.contains name then fail "EXTERNAL_NAME_OVERLAP"
    allowed := allowed.insert name
  let mut units := #[]
  let mut names := #[]
  let mut rows := #[]
  let mut nodes := 0
  let frontend := privateEnv.setExporting false
  for raw in rawUnits do
    let fields ← ExprCodec.arrayOf raw (some 3)
    nodes := nodes + (← DeclCodec.descriptorNodes fields[1]! codecLimits)
    if nodes > nodeMaximum then fail "NEW_NODE_BOUND"
    for row in (← ExprCodec.arrayOf fields[2]!) do
      nodes := nodes + (← DeclCodec.inventoryNodes row codecLimits)
      if nodes > nodeMaximum then fail "NEW_NODE_BOUND"
    let unit ← DeclCodec.decodeUnit allowed raw codecLimits
    discard <| CheckedExtension.allowedDeclaration unit.decl
    let added ← DeclCodec.expectedNames unit.expected codecLimits
    if names.size + added.size > checkerLimits.maxNewNames then fail "NEW_NAME_BOUND"
    for name in added do
      if allowed.contains name || (frontend.find? name (skipRealize := true)).isSome ||
          (privateEnv.toKernelEnv.find? name).isSome then fail s!"ALL_NEW_NAME_COLLISION name={name}"
      allowed := allowed.insert name
      names := names.push name
    units := units.push unit
    rows := rows ++ unit.expected
  return (units, names, rows)

def requestOf (path : System.FilePath) : IO Json := do
  let raw ← readJson path requestMaximum
  exactObject raw #["schema", "semantic_id", "context_root", "foundation_id", "module_name",
    "targets", "unit_ids", "units", "reference_id", "parent_delta_id", "reference_plan_sha256"]
  if (← field raw "schema") != .str "DMKN_ORDINARY_REFERENCE_MODULE_REQUEST_V1" then
    fail "REQUEST_SCHEMA"
  for key in #["semantic_id", "context_root", "foundation_id", "reference_id", "reference_plan_sha256"] do
    discard <| identityOf (← field raw key)
  let units ← ExprCodec.arrayOf (← field raw "units")
  let ids ← ExprCodec.arrayOf (← field raw "unit_ids")
  if units.isEmpty || units.size > 32 || units.size != ids.size then fail "NEW_UNIT_BOUND"
  let mut seen : Std.HashSet String := {}
  for value in ids do
    let id ← identityOf value
    if seen.contains id then fail "NEW_DUPLICATE_UNIT_ID"
    seen := seen.insert id
  let targets ← namesOf (← field raw "targets") 32
  if targets.isEmpty then fail "TARGET_EMPTY"
  return raw

def inspectParts (paths : Array System.FilePath) : IO (Array Json) := do
  let mut total := 0
  let mut rows := #[]
  for path in paths do
    let info ← (nativePath path).symlinkMetadata
    if info.type != .file || info.numLinks != 1 || info.byteSize == 0 then fail "OUTPUT_PART_FILE"
    total := total + info.byteSize.toNat
    if total > artifactMaximum then fail "OUTPUT_ARTIFACT_BOUND"
    rows := rows.push (Json.mkObj [("path", .str path.toString), ("bytes", toJson info.byteSize.toNat)])
  return rows

def validateOutput (plan : Plan) (request : Json) (output : System.FilePath) : IO Name := do
  let name ← bridgeModule (← field request "module_name")
  if (plan.artifacts.find? name).isSome || output.fileName != some (name.toString ++ ".olean") then
    fail "OUTPUT_MODULE_COLLISION_OR_BASENAME"
  for path in moduleParts output do
    if plan.original.pathKeys.contains (BaselineArtifacts.pathKey path) then fail "OUTPUT_ORIGINAL_ALIAS"
  return name

def importBase (plan : Plan) (level : OLeanLevel) : IO Environment := do
  searchPathRef.set []
  let env ← importModules plan.imports {} 0
    (plugins := #[]) (leakEnv := false) (loadExts := false) (level := level) (arts := plan.artifacts)
  if env.header.imports != plan.imports then fail "BASE_ROOT_IMPORTS"
  checkBaseHeaders env plan (level != .private)
  checkBaseRecords env plan (level != .private)
  return env

def run (inventoryPath requestPath planPath outputPath pendingPath : System.FilePath) : IO Unit := do
  for path in (moduleParts outputPath).push pendingPath do BaselineArtifacts.requireFresh path
  let request ← requestOf requestPath
  let plan ← readPlan planPath inventoryPath request
  let moduleName ← validateOutput plan request outputPath
  let privateEnv ← importBase plan .private
  let (units, names, inventories) ← decodeUnits (← ExprCodec.arrayOf (← field request "units")) plan privateEnv
  for target in (← namesOf (← field request "targets") 32) do
    if !names.contains target && !plan.externalNames.contains target then fail "TARGET_NOT_REALIZED"
  let checked ← CheckedExtension.checkBatch privateEnv units checkerLimits
  let privateChecked ← OwnerRebind.exposeAdded checked.environment checked.added
  checkInventories privateChecked names inventories false
  let publicEnv ← importBase plan .exported
  let publicChecked ← CheckedExtension.checkBatch publicEnv units checkerLimits
  let exposed ← OwnerRebind.exposeAdded publicChecked.environment publicChecked.added
  let writer := exposed.setMainModule moduleName
  checkInventories writer names inventories false
  checkInventories writer names inventories true
  if writer.imports != plan.imports then fail "OUTPUT_IMPORTS_CHANGED"
  for path in (moduleParts outputPath).push pendingPath do BaselineArtifacts.requireFresh path
  writeModule writer (nativePath outputPath)
  let mut rows : List (String × Json) := []
  for key in #["semantic_id", "context_root", "foundation_id", "module_name", "targets", "unit_ids",
      "reference_id", "parent_delta_id", "reference_plan_sha256"] do
    rows := rows ++ [(key, ← field request key)]
  rows := rows ++ [
    ("schema", .str "DMKN_ORDINARY_REFERENCE_MODULE_PENDING_V1"),
    ("assurance", .str "LOCAL_CHECKED_REFERENCE_MODULE_PENDING_REREADS"),
    ("direct_imports", ← encodedNames (plan.imports.map (·.module))),
    ("names", ← encodedNames names), ("inventories", .arr inventories),
    ("added_names", ← encodedNames names), ("added_inventories", .arr inventories),
    ("matched_unit_indices", .arr #[]), ("matched_names", .arr #[]), ("matched_inventories", .arr #[]),
    ("units_checked", toJson units.size), ("units_matched", toJson (0 : Nat)),
    ("checking_passes", toJson (2 : Nat)), ("basis_rows", toJson plan.basis.size),
    ("usable_basis_rows", toJson plan.usableBasis.size),
    ("reference_public_units", toJson plan.publicUnitCount),
    ("reference_public_names", toJson plan.publicBindings.size),
    ("generated_names", toJson plan.generatedBindings.size),
    ("artifact_parts", .arr (← inspectParts (moduleParts outputPath)))]
  let bytes := (Json.mkObj rows).compress.toUTF8
  if bytes.size > reportMaximum then fail "PENDING_BYTE_BOUND"
  let handle ← IO.FS.Handle.mk (nativePath pendingPath) .writeNew
  handle.write bytes
  handle.flush

def reread (inventoryPath requestPath planPath outputPath pendingPath : System.FilePath)
    (level : OLeanLevel) : IO Unit := do
  let request ← requestOf requestPath
  let plan ← readPlan planPath inventoryPath request
  let moduleName ← validateOutput plan request outputPath
  let pending ← readJson pendingPath reportMaximum
  exactObject pending #["schema", "assurance", "semantic_id", "context_root", "foundation_id",
    "module_name", "targets", "unit_ids", "reference_id", "parent_delta_id", "reference_plan_sha256",
    "direct_imports", "names", "inventories", "added_names", "added_inventories", "matched_unit_indices",
    "matched_names", "matched_inventories", "units_checked", "units_matched", "checking_passes",
    "basis_rows", "usable_basis_rows", "reference_public_units", "reference_public_names",
    "generated_names", "artifact_parts"]
  if (← field pending "schema") != .str "DMKN_ORDINARY_REFERENCE_MODULE_PENDING_V1" ||
      (← field pending "assurance") != .str "LOCAL_CHECKED_REFERENCE_MODULE_PENDING_REREADS" then
    fail "PENDING_SCHEMA"
  for key in #["semantic_id", "context_root", "foundation_id", "module_name", "targets", "unit_ids",
      "reference_id", "parent_delta_id", "reference_plan_sha256"] do
    if (← field pending key) != (← field request key) then fail "PENDING_REQUEST_BINDING"
  let units ← ExprCodec.arrayOf (← field request "units")
  let mut inventories := #[]
  for unit in units do
    let fields ← ExprCodec.arrayOf unit (some 3)
    inventories := inventories ++ (← ExprCodec.arrayOf fields[2]!)
    if inventories.size > checkerLimits.maxNewNames then fail "NEW_NAME_BOUND"
  let names ← DeclCodec.expectedNames inventories codecLimits
  for key in #["names", "added_names"] do
    if (← field pending key) != (← encodedNames names) then fail "PENDING_NAMES"
  for key in #["inventories", "added_inventories"] do
    if (← field pending key) != .arr inventories then fail "PENDING_INVENTORIES"
  for key in #["matched_unit_indices", "matched_names", "matched_inventories"] do
    if (← field pending key) != .arr #[] then fail "ALL_NEW_REQUIRED"
  if (← field pending "units_checked") != toJson units.size ||
      (← field pending "units_matched") != toJson (0 : Nat) ||
      (← field pending "checking_passes") != toJson (2 : Nat) ||
      (← field pending "basis_rows") != toJson (581 : Nat) ||
      (← field pending "usable_basis_rows") != toJson plan.usableBasis.size ||
      (← field pending "reference_public_units") != toJson plan.publicUnitCount ||
      (← field pending "reference_public_names") != toJson plan.publicBindings.size ||
      (← field pending "generated_names") != toJson plan.generatedBindings.size ||
      (← field pending "direct_imports") != (← encodedNames (plan.imports.map (·.module))) then
    fail "PENDING_PLAN_CENSUS"
  let parts ← inspectParts (moduleParts outputPath)
  if (← field pending "artifact_parts") != .arr parts then fail "PENDING_ARTIFACTS"
  let artifacts := plan.artifacts.insert moduleName (BaselineArtifacts.asArtifacts (moduleParts outputPath))
  searchPathRef.set []
  let restored ← importModules #[standardImport moduleName] {} 0
    (plugins := #[]) (leakEnv := false) (loadExts := false) (level := level) (arts := artifacts)
  checkBaseHeaders restored plan (level != .private) (some moduleName)
  checkBaseRecords restored plan (level != .private)
  checkModuleHeader restored moduleName names plan.imports
  checkInventories restored names inventories (level != .private)
  if (← inspectParts (moduleParts outputPath)) != parts then fail "REREAD_OUTPUT_CHANGED"

end OrdinaryLean.ReferenceModule

def main (args : List String) : IO UInt32 := do
  try
    match args with
    | [phase, sysroot, inventory, request, plan, output, pending] =>
        discard <| OrdinaryLean.ReferenceModule.absolutePath sysroot
        let inventory ← OrdinaryLean.ReferenceModule.absolutePath inventory
        let request ← OrdinaryLean.ReferenceModule.absolutePath request
        let plan ← OrdinaryLean.ReferenceModule.absolutePath plan
        let output ← OrdinaryLean.ReferenceModule.absolutePath output
        let pending ← OrdinaryLean.ReferenceModule.absolutePath pending
        match phase with
        | "build" => OrdinaryLean.ReferenceModule.run inventory request plan output pending
        | "reread-private" => OrdinaryLean.ReferenceModule.reread inventory request plan output pending .private
        | "reread-exported" => OrdinaryLean.ReferenceModule.reread inventory request plan output pending .exported
        | _ => OrdinaryLean.ReferenceModule.fail "PHASE"
        return 0
    | _ => OrdinaryLean.ReferenceModule.fail "USAGE phase sysroot inventory request plan output pending"
  catch error =>
    (← IO.getStderr).putStrLn (toString error)
    return 1
