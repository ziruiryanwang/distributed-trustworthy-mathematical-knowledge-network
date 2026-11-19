/- Shared protected-reference environment parser. Mechanical derivative of the
   reviewed ReferenceModule prefix through checkBaseHeaders; no output, checker
   invocation or main entry. Frozen ReferenceModule remains unchanged. -/

import BaselineArtifactCore04
import OwnerRebind

/- Protected original-reference materialization, not peer acceptance.
   The owner authenticates the live reference, exact snapshot/support and current
   warrants. This program checks only new units over that preserved interpretation.
   Native digest fields are binding labels; the worker/controller hash the bytes.
   No old proofs, saved reports or matching names establish authority here. -/

open Lean

namespace OrdinaryLean.ReferenceEnvironment

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

end OrdinaryLean.ReferenceEnvironment

