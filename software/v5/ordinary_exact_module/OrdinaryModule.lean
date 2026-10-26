import OrdinaryExport
import OwnerRebind

/- Internal local bridge, not a peer entry point or a new acceptance authority.
   The controller authenticates the runtime, full fixed-basis inventory, actual
   owner context, canonical evidence, every import identity and exact request
   bytes before invoking this bounded worker. Identity strings below are echoed
   labels, never cryptographic verification. Imports are installed Init or one
   locally registered modern anchor and its exact bounded five-part chain.
   The output directory and inputs are protected against concurrent replacement.
   Fresh artifacts are uncommitted until controller validation/adoption.
   Existing theorem interfaces are interpreted ONLY by exact full warranted
   singleton proofs. Installed non-theorems require complete selected units,
   exact concrete private/public records and closed selected dependencies.
   This is not a new axiom/evidence-acceptance rule. -/

open Lean

namespace OrdinaryLean.ModuleBridge

def requestMaximum : Nat := 4194304
def inventoryMaximum : Nat := 1048576
def reportMaximum : Nat := 8388608
def artifactMaximum : Nat := 67108864
def nodeMaximum : Nat := 131072
def anchorPlanMaximum : Nat := 4194304
def anchorArtifactMaximum : Nat := 268435456
def anchorNameMaximum : Nat := 16384

def codecLimits : DeclCodec.Limits := { maxUnitNodes := nodeMaximum }

def checkerLimits : CheckedExtension.Limits := {
  codec := codecLimits
  maxUnits := 32
  maxNewNames := 4096
  maxScanNodes := nodeMaximum
}

def matchLimits : OwnerRebind.Limits := {
  checker := checkerLimits
  maxScanNodes := nodeMaximum
}

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"ORDINARY_MODULE {message}"

def absolutePath (raw : String) : IO System.FilePath := do
  let path := System.FilePath.mk raw
  if !path.isAbsolute || path.toString.utf8ByteSize > 32768 then
    fail "ABSOLUTE_BOUNDED_PATH_REQUIRED"
  if path.components.contains "." || path.components.contains ".." then
    fail "DOT_PATH_COMPONENT"
  return path

/- Only the native filesystem spelling changes. Stable request/plan/report paths
   retain their original bytes. This handles ordinary absolute drive paths on
   Windows, not UNC/device namespaces; all caller validation remains upstream.
   Extended spelling suppresses Win32 trimming of dot/space-ended components:
   preserve the old spelling for those paths, rather than change their referent. -/
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

/- Same bounded-token preflight as the existing ordinary worker. Exact canonical
   and duplicate-key validation remains a protected controller prerequisite. -/
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

def readSelectedJson (path : System.FilePath) (maximum : Nat) : IO Json := do
  let metadata ← (nativePath path).symlinkMetadata
  if metadata.type != .file || metadata.numLinks != 1 then
    fail "ORDINARY_SINGLE_LINK_INPUT_REQUIRED"
  if metadata.byteSize.toNat > maximum then fail "INPUT_BYTE_BOUND"
  let handle ← IO.FS.Handle.mk (nativePath path) .read
  let mut bytes : ByteArray := ⟨#[]⟩
  while true do
    let chunk ← handle.read (USize.ofNat (min 65536 (maximum + 1 - bytes.size)))
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
    discard (nativePath path).symlinkMetadata
    pure true
  catch error =>
    match error with
    | .noFileOrDirectory .. => pure false
    | _ => throw error
  if present then fail "FRESH_OUTPUT_REQUIRED"
  let some directory := path.parent | fail "OUTPUT_PARENT_REQUIRED"
  if (← (nativePath directory).symlinkMetadata).type != .dir then
    fail "ORDINARY_OUTPUT_DIRECTORY_REQUIRED"

def exactObject (value : Json) (keys : Array String) : IO Unit := do
  let object ← ExprCodec.jsonResult value.getObj?
  if object.size != keys.size then fail "JSON_EXACT_FIELDS"
  for key in keys do
    if (object.get? key).isNone then fail "JSON_MISSING_FIELD"

def field (value : Json) (key : String) : IO Json :=
  ExprCodec.jsonResult (value.getObjVal? key)

def targetNames (value : Json) : IO (Array Name) := do
  let raw ← ExprCodec.arrayOf value
  if raw.isEmpty || raw.size > 32 then fail "TARGET_COUNT_BOUND"
  let mut names : Array Name := #[]
  let mut seen : Std.HashSet Name := {}
  for encoded in raw do
    let name ← ExprCodec.decodeName encoded
    CheckedExtension.requireName name
    if seen.contains name then fail "DUPLICATE_TARGET"
    seen := seen.insert name
    names := names.push name
  return names

def bridgeModule (value : Json) : IO Name := do
  let name ← ExprCodec.decodeName value
  match name with
  | .str .anonymous component =>
      if !component.startsWith "DMKNBridge_" then fail "MODULE_PREFIX"
      let suffix := component.drop 11 |>.toString
      discard <| OwnerRebind.identityOf (.str suffix)
      return name
  | _ => fail "TOP_LEVEL_BRIDGE_MODULE_REQUIRED"

def initImports : Array Import :=
  #[{ module := `Init, importAll := false, isExported := true, isMeta := false }]

def requireModern (env : Environment) : IO Unit := do
  for data in env.header.moduleData do
    if !data.isModule then fail "LEGACY_IMPORTED_MODULE"

def decodeUnits (rawUnits : Array Json) (basisNames anchorNames : Array Name)
    : IO (Array DeclCodec.DecodedUnit × Array Name × Array Json) := do
  let mut allowed : Std.HashSet Name := {}
  for name in basisNames do allowed := allowed.insert name
  let mut anchored : Std.HashSet Name := {}
  for name in anchorNames do
    if allowed.contains name then fail "ANCHOR_BASIS_NAME_OVERLAP"
    anchored := anchored.insert name
    allowed := allowed.insert name
  let mut units := #[]
  let mut names := #[]
  let mut inventories := #[]
  let mut nodes := 0
  for raw in rawUnits do
    let fields ← ExprCodec.arrayOf raw (some 3)
    nodes := nodes + (← DeclCodec.descriptorNodes fields[1]! codecLimits)
    for row in (← ExprCodec.arrayOf fields[2]!) do
      nodes := nodes + (← DeclCodec.inventoryNodes row codecLimits)
      if nodes > nodeMaximum then fail "BATCH_ENCODED_NODE_BOUND"
    if nodes > nodeMaximum then fail "BATCH_ENCODED_NODE_BOUND"
    -- Only basis, registered anchor outputs and preceding new outputs are legal.
    -- Importing an environment does NOT authorize all its ambient declarations.
    let unit ← DeclCodec.decodeUnit allowed raw codecLimits
    let unitNames ← DeclCodec.expectedNames unit.expected codecLimits
    if names.size + unitNames.size > checkerLimits.maxNewNames then
      fail "BATCH_NAME_BOUND"
    for name in unitNames do
      if anchored.contains name then fail "ANCHORED_OUTPUT_COLLISION"
      allowed := allowed.insert name
      names := names.push name
    inventories := inventories ++ unit.expected
    units := units.push unit
  return (units, names, inventories)

def checkInventories (env : Environment) (names : Array Name)
    (inventories : Array Json) (publicView : Bool) : IO Unit := do
  if names.size != inventories.size then fail "INVENTORY_CENSUS"
  let view := env.setExporting publicView
  for i in [:names.size] do
    let name := names[i]!
    let some visible := view.find? name (skipRealize := true) |
      fail s!"MISSING_VISIBLE_RECORD name={name}"
    let some kernel := view.toKernelEnv.find? name |
      fail s!"MISSING_KERNEL_RECORD name={name}"
    for actual in #[kernel, visible] do
      if actual.name != name then fail "VISIBLE_RECORD_KEY_MISMATCH"
      if actual.isAxiom || actual.isUnsafe || actual.isPartial then
        fail s!"INCOMPLETE_OR_UNSAFE_VISIBLE_RECORD name={name}"
      if (← DeclCodec.inventoryRow actual codecLimits) != inventories[i]! then
        fail s!"VISIBLE_INVENTORY_MISMATCH name={name}"

/- Only the theorem branch permits an existing public axiom-shaped handle,
   after its full private proof and warranted closure have matched. Every other
   selected record must remain concrete and exact in both lookup maps. -/
def checkMatchedPublic (env : Environment) (names : Array Name)
    (inventories : Array Json) : IO Unit := do
  if names.size != inventories.size then fail "MATCHED_INVENTORY_CENSUS"
  let view := env.setExporting true
  for i in [:names.size] do
    let name := names[i]!
    let expected ← ExprCodec.arrayOf inventories[i]! (some 5)
    if expected[0]! != (← ExprCodec.encodeName name) then fail "MATCHED_NAME_REQUIRED"
    let kind ← ExprCodec.natOf expected[1]!
    if kind != 2 then
      if kind < 1 || kind > 6 then fail "MATCHED_NON_THEOREM_KIND"
      checkInventories view #[name] #[inventories[i]!] true
      continue
    let some visible := view.find? name (skipRealize := true) |
      fail s!"MISSING_PUBLIC_MATCH name={name}"
    let some kernel := view.toKernelEnv.find? name |
      fail s!"MISSING_KERNEL_PUBLIC_MATCH name={name}"
    for actual in #[kernel, visible] do
      if actual.name != name || actual.isUnsafe || actual.isPartial then
        fail "UNSAFE_OR_MISKEYED_PUBLIC_MATCH"
      match actual with
      | .thmInfo _ =>
          if (← DeclCodec.inventoryRow actual codecLimits) != inventories[i]! then
            fail s!"PUBLIC_THEOREM_PROOF_MISMATCH name={name}"
      | .axiomInfo d =>
          if d.isUnsafe ||
              (← DeclCodec.paramsJson d.levelParams codecLimits) != expected[2]! ||
              (← ExprCodec.encode d.levelParams d.type codecLimits.expr) != expected[3]! then
            fail s!"PUBLIC_THEOREM_SIGNATURE_MISMATCH name={name}"
      | _ => fail s!"PUBLIC_THEOREM_HANDLE_REQUIRED name={name}"

def selectedKernelRecord (env : Environment) (selected : Std.HashSet Name)
    (name : Name) : IO ConstantInfo := do
  if !selected.contains name then fail s!"NONSELECTED_GROUP_RECORD name={name}"
  let some actual := env.toKernelEnv.find? name | fail s!"MISSING_GROUP_RECORD name={name}"
  return actual

/- The protected accepted unit supplies complete generated membership. This
   reconstruction uses only its bounded selected names, never an ambient census.
   Exact rows were checked in BOTH maps before this function is called. -/
def matchNonTheorem (env : Environment) (unit : DeclCodec.DecodedUnit)
    (names : Array Name) (bound : Std.HashSet Name) (scans : Nat) : IO Nat := do
  let mut selected : Std.HashSet Name := {}
  for name in names do
    if bound.contains name then fail "MATCHED_GROUP_PREFIX_OVERLAP"
    selected := selected.insert name
  let mut allowed := bound
  match unit.decl with
  | .defnDecl d =>
      if names != #[d.name] || d.all != [d.name] then
        fail "INSTALLED_MATCH_REQUIRES_SINGLETON_DEFINITION"
      if (← DeclCodec.inventoryRow (.defnInfo d) codecLimits) != unit.expected[0]! then
        fail "MATCHED_DESCRIPTOR_INVENTORY_MISMATCH"
  | .opaqueDecl d =>
      if names != #[d.name] || d.all != [d.name] then
        fail "INSTALLED_MATCH_REQUIRES_SINGLETON_OPAQUE"
      if (← DeclCodec.inventoryRow (.opaqueInfo d) codecLimits) != unit.expected[0]! then
        fail "MATCHED_DESCRIPTOR_INVENTORY_MISMATCH"
  | .inductDecl _ _ types _ =>
      let typeNames := types.map (fun value => value.name)
      if typeNames.isEmpty then fail "EMPTY_MATCHED_GROUP"
      let .inductInfo first ← selectedKernelRecord env selected typeNames.head! |
        fail "MATCHED_GROUP_OWNER_KIND"
      if first.all != typeNames then fail "MATCHED_GROUP_TYPE_ORDER"
      let mut actualTypes : Array InductiveType := #[]
      for name in typeNames do
        let .inductInfo actual ← selectedKernelRecord env selected name |
          fail "MATCHED_GROUP_TYPE_KIND"
        if actual.all != typeNames || actual.levelParams != first.levelParams ||
            actual.numParams != first.numParams || actual.isUnsafe then
          fail "MATCHED_GROUP_TYPE_METADATA"
        let mut ctors : Array Constructor := #[]
        for index in [:actual.ctors.length] do
          let ctorName := actual.ctors[index]!
          let .ctorInfo ctor ← selectedKernelRecord env selected ctorName |
            fail "MATCHED_GROUP_CONSTRUCTOR_KIND"
          if ctor.induct != name || ctor.cidx != index ||
              ctor.numParams != actual.numParams || ctor.levelParams != actual.levelParams ||
              ctor.isUnsafe then fail "MATCHED_GROUP_CONSTRUCTOR_METADATA"
          ctors := ctors.push { name := ctorName, type := ctor.type }
        actualTypes := actualTypes.push { name, type := actual.type, ctors := ctors.toList }
      let reconstructed := Declaration.inductDecl first.levelParams first.numParams
        actualTypes.toList false
      if (← DeclCodec.encodeDescriptor reconstructed codecLimits) !=
          (← DeclCodec.encodeDescriptor unit.decl codecLimits) then
        fail "MATCHED_GROUP_DESCRIPTOR_MISMATCH"
      for name in names do
        let actual ← selectedKernelRecord env selected name
        match actual with
        | .inductInfo d =>
            if !typeNames.contains name || d.all != typeNames then
              fail "MIXED_MATCHED_INDUCTIVE_GROUP"
        | .ctorInfo d =>
            if !typeNames.contains d.induct then fail "MIXED_MATCHED_CONSTRUCTOR_GROUP"
            let .inductInfo parent ← selectedKernelRecord env selected d.induct |
              fail "MATCHED_CONSTRUCTOR_OWNER_KIND"
            if d.cidx >= parent.ctors.length || parent.ctors[d.cidx]! != name then
              fail "MATCHED_CONSTRUCTOR_OWNER_INDEX"
        | .recInfo d =>
            if d.all != typeNames then fail "MIXED_MATCHED_RECURSOR_GROUP"
            for rule in d.rules do
              let .ctorInfo ctor ← selectedKernelRecord env selected rule.ctor |
                fail "MATCHED_RECURSOR_RULE_CONSTRUCTOR"
              if !typeNames.contains ctor.induct || rule.nfields != ctor.numFields then
                fail "MATCHED_RECURSOR_RULE_METADATA"
        | _ => fail "MATCHED_GENERATED_RECORD_REQUIRED"
      for name in names do allowed := allowed.insert name
  | _ => fail "INSTALLED_NON_THEOREM_KIND"
  let mut used := scans
  for name in names do
    let actual ← selectedKernelRecord env selected name
    used ← OwnerRebind.scanSemantics actual .exact allowed used matchLimits
  return used

structure MatchPlan where
  addedUnits : Array DeclCodec.DecodedUnit := #[]
  matchedIndices : Array Nat := #[]
  addedNames : Array Name := #[]
  addedInventories : Array Json := #[]
  matchedNames : Array Name := #[]
  matchedInventories : Array Json := #[]

def classifyUnits (env : Environment) (units : Array DeclCodec.DecodedUnit)
    (basisNames anchorNames : Array Name)
    : IO MatchPlan := do
  let mut plan : MatchPlan := {}
  let view := env.setExporting false
  let mut index := 0
  let mut scans := 0
  let mut bound : Std.HashSet Name := {}
  for name in basisNames ++ anchorNames do bound := bound.insert name
  for unit in units do
    discard <| CheckedExtension.allowedDeclaration unit.decl
    let names ← DeclCodec.expectedNames unit.expected codecLimits
    let mut present := 0
    for name in names do
      let kernelPresent := (view.toKernelEnv.find? name).isSome
      let visiblePresent := (view.find? name (skipRealize := true)).isSome
      if kernelPresent != visiblePresent then fail "HIDDEN_INSTALLED_COLLISION"
      if kernelPresent then present := present + 1
    if present != 0 && present != names.size then fail "PARTIAL_INSTALLED_GROUP"
    if present != 0 then
      checkInventories view names unit.expected false
      -- One row alone does not rule out a mutual theorem block. Require the
      -- original descriptor's complete singleton metadata as well.
      match unit.decl with
      | .thmDecl d =>
          if names != #[d.name] || d.all != [d.name] then
            fail "INSTALLED_MATCH_REQUIRES_SINGLETON_THEOREM"
          if (← DeclCodec.inventoryRow (.thmInfo d) codecLimits) != unit.expected[0]! then
            fail "MATCHED_DESCRIPTOR_INVENTORY_MISMATCH"
      | _ => scans ← matchNonTheorem view unit names bound scans
      plan := { plan with
        matchedIndices := plan.matchedIndices.push index
        matchedNames := plan.matchedNames ++ names
        matchedInventories := plan.matchedInventories ++ unit.expected }
    else
      plan := { plan with
        addedUnits := plan.addedUnits.push unit
        addedNames := plan.addedNames ++ names
        addedInventories := plan.addedInventories ++ unit.expected }
    for name in names do bound := bound.insert name
    index := index + 1
  if plan.addedUnits.isEmpty then fail "NO_NEW_MODULE_DECLARATIONS"
  return plan

/- Request-derived family check for the pending partition. The protected build
   phase already decoded the descriptor and established complete group/actual
   correspondence; rereads do not reinterpret free-standing name lists. -/
def checkMatchedDescriptor (raw : Json) (rows : Array Json) (names : Array Name)
    : IO Unit := do
  discard <| DeclCodec.descriptorNodes raw codecLimits
  let descriptor ← ExprCodec.arrayOf raw
  let tag ← ExprCodec.natOf descriptor[0]!
  if tag == 3 then
    let mut hasType := false
    for row in rows do
      let fields ← ExprCodec.arrayOf row (some 5)
      let kind ← ExprCodec.natOf fields[1]!
      if kind < 4 || kind > 6 then fail "MATCHED_GENERATED_INVENTORY_KIND"
      if kind == 4 then hasType := true
    if !hasType then fail "MATCHED_GENERATED_TYPE_REQUIRED"
    return
  if tag > 2 || names.size != 1 then fail "MATCHED_SINGLETON_DESCRIPTOR_REQUIRED"
  let own ← ExprCodec.encodeName names[0]!
  let allNames := descriptor[if tag == 0 then 6 else 5]!
  if descriptor[1]! != own || allNames != .arr #[own] then
    fail "MATCHED_SINGLETON_DESCRIPTOR_REQUIRED"
  let details := if tag == 0 then
      Json.arr #[descriptor[4]!, descriptor[5]!, allNames]
    else if tag == 1 then Json.arr #[descriptor[4]!, allNames]
    else Json.arr #[descriptor[4]!, toJson (0 : Nat), allNames]
  if rows[0]! != .arr #[own, toJson (tag + 1), descriptor[2]!, descriptor[3]!, details] then
    fail "MATCHED_DESCRIPTOR_INVENTORY_MISMATCH"

/- Reconstruct the exact report partition from the original request, not from
   free-standing reported name lists. Fresh-process rereads need no second Init
   load or descriptor decoding: build already decoded and checked the protected
   request; the worker binds its bytes and this pending record across phases. -/
def reportPartition (rawUnits : Array Json) (pending : Json)
    : IO (Array Name × Array Json × Array Name × Array Json) := do
  let matchedRaw ← ExprCodec.arrayOf (← field pending "matched_unit_indices")
  if matchedRaw.size >= rawUnits.size then fail "MATCHED_UNIT_CENSUS"
  let mut matched : Array Nat := #[]
  for raw in matchedRaw do
    let index ← ExprCodec.indexOf raw rawUnits.size
    if !matched.isEmpty && index <= matched.back! then fail "MATCHED_UNIT_ORDER"
    matched := matched.push index
  let mut addedNames := #[]
  let mut addedInventories := #[]
  let mut matchedNames := #[]
  let mut matchedInventories := #[]
  for i in [:rawUnits.size] do
    let fields ← ExprCodec.arrayOf rawUnits[i]! (some 3)
    let rows ← ExprCodec.arrayOf fields[2]!
    let names ← DeclCodec.expectedNames rows codecLimits
    if matched.contains i then
      checkMatchedDescriptor fields[1]! rows names
      matchedNames := matchedNames ++ names
      matchedInventories := matchedInventories ++ rows
    else
      addedNames := addedNames ++ names
      addedInventories := addedInventories ++ rows
  if (← field pending "units_checked") != toJson (rawUnits.size - matched.size) ||
      (← field pending "units_matched") != toJson matched.size ||
      (← field pending "matched_names") != .arr (← matchedNames.mapM (fun name => ExprCodec.encodeName name)) ||
      (← field pending "matched_inventories") != .arr matchedInventories ||
      (← field pending "added_names") != .arr (← addedNames.mapM (fun name => ExprCodec.encodeName name)) ||
      (← field pending "added_inventories") != .arr addedInventories then
    fail "PENDING_PARTITION_BINDING"
  return (addedNames, addedInventories, matchedNames, matchedInventories)

def moduleParts (output : System.FilePath) : Array System.FilePath :=
  #[output, OLeanLevel.server.adjustFileName output,
    OLeanLevel.private.adjustFileName output,
    output.withExtension "ir.sig", output.withExtension "ir"]

def inspectParts (paths : Array System.FilePath) : IO (Array Json) := do
  let mut bytes := 0
  let mut rows := #[]
  for path in paths do
    let metadata ← (nativePath path).symlinkMetadata
    if metadata.type != .file || metadata.numLinks != 1 then
      fail "ORDINARY_SINGLE_LINK_OUTPUT_REQUIRED"
    let count := metadata.byteSize.toNat
    if count == 0 then fail "EMPTY_ARTIFACT"
    bytes := bytes + count
    if bytes > artifactMaximum then fail "AGGREGATE_ARTIFACT_BYTE_BOUND"
    rows := rows.push (Json.mkObj [
      ("path", .str path.toString), ("bytes", toJson count)])
  return rows

structure AnchorBinding where
  name : Name
  kind : Nat
  params : Json

structure AnchorModule where
  anchorId : String
  moduleName : Name
  imports : Array Import
  addedNames : Array Name
  parts : Array System.FilePath
  deriving Inhabited

structure AnchorPlan where
  anchorId : String
  supportId : String
  modules : Array AnchorModule := #[]
  bindings : Array AnchorBinding := #[]
  artifacts : NameMap ImportArtifacts := {}

def AnchorPlan.names (plan : AnchorPlan) : Array Name :=
  plan.bindings.map (fun row => row.name)

def AnchorPlan.imports (plan : AnchorPlan) : Array Import :=
  if plan.modules.isEmpty then initImports else
    #[{ module := plan.modules.back!.moduleName,
        importAll := false, isExported := true, isMeta := false }]

def encodedNames (names : Array Name) : IO Json := do
  return .arr (← names.mapM (fun name => ExprCodec.encodeName name))

def encodedImports (imports : Array Import) : IO Json :=
  encodedNames (imports.map (fun entry => entry.module))

def planNames (raw : Json) (maximum : Nat) : IO (Array Name) := do
  let rows ← ExprCodec.arrayOf raw
  if rows.size > maximum then fail "ANCHOR_NAME_BOUND"
  let mut names := #[]
  let mut seen : Std.HashSet Name := {}
  for row in rows do
    let name ← ExprCodec.decodeName row
    CheckedExtension.requireName name
    if seen.contains name then fail "ANCHOR_DUPLICATE_NAME"
    seen := seen.insert name
    names := names.push name
  return names

/- The protected controller authenticates this complete plan from its local
   registry. The worker hashes every parent part and the exact plan between
   phases. This parser checks shape/header/name correspondence, NOT authority
   from an untrusted hash list, and never decodes previous proof inventories. -/
def readAnchorPlan (path : System.FilePath) (request : Json) : IO AnchorPlan := do
  let raw ← readSelectedJson path anchorPlanMaximum
  exactObject raw #["schema", "anchor_id", "support_id", "modules", "bindings"]
  if (← field raw "schema") != .str "DMKN_LOCAL_MODULE_ANCHOR_PLAN_V1" then
    fail "ANCHOR_PLAN_SCHEMA"
  let anchorId ← ExprCodec.jsonResult (← field raw "anchor_id").getStr?
  if !anchorId.isEmpty then discard <| OwnerRebind.identityOf (.str anchorId)
  if (← field request "anchor_id") != .str anchorId then fail "ANCHOR_REQUEST_BINDING"
  discard <| OwnerRebind.identityOf (← field request "anchor_plan_sha256")
  let supportId ← OwnerRebind.identityOf (← field raw "support_id")
  let moduleRows ← ExprCodec.arrayOf (← field raw "modules")
  let unitRows ← ExprCodec.arrayOf (← field raw "bindings")
  if moduleRows.size > 32 || unitRows.size > 1024 ||
      (anchorId.isEmpty != moduleRows.isEmpty) ||
      (anchorId.isEmpty != unitRows.isEmpty) then fail "ANCHOR_CHAIN_BOUND"
  let mut plan : AnchorPlan := { anchorId := anchorId, supportId := supportId }
  let mut moduleNames : Std.HashSet Name := {}
  let mut anchorIds : Std.HashSet String := {}
  let mut partPaths : Std.HashSet String := {}
  let mut declaredAdded : Std.HashSet Name := {}
  let mut declaredCount := 0
  let mut totalBytes := 0
  for row in moduleRows do
    exactObject row #["anchor_id", "module_name", "direct_imports", "added_names", "artifact_parts"]
    let id ← OwnerRebind.identityOf (← field row "anchor_id")
    let moduleName ← bridgeModule (← field row "module_name")
    if anchorIds.contains id || moduleNames.contains moduleName then
      fail "ANCHOR_REPEATED_MODULE"
    anchorIds := anchorIds.insert id
    moduleNames := moduleNames.insert moduleName
    let imports := plan.imports
    if (← field row "direct_imports") != (← encodedImports imports) then
      fail "ANCHOR_PARENT_IMPORT_BINDING"
    let addedNames ← planNames (← field row "added_names") checkerLimits.maxNewNames
    if addedNames.isEmpty then fail "ANCHOR_EMPTY_GENERATED_MODULE"
    for name in addedNames do
      if declaredAdded.contains name then fail "ANCHOR_REDECLARED_OUTPUT"
      declaredAdded := declaredAdded.insert name
      declaredCount := declaredCount + 1
      if declaredCount > anchorNameMaximum then fail "ANCHOR_NAME_BOUND"
    let partRows ← ExprCodec.arrayOf (← field row "artifact_parts") (some 5)
    let mut paths := #[]
    let mut moduleBytes := 0
    for part in partRows do
      exactObject part #["path", "bytes", "sha256"]
      let path ← absolutePath (← ExprCodec.jsonResult (← field part "path").getStr?)
      if partPaths.contains path.toString then fail "ANCHOR_PART_ALIAS"
      partPaths := partPaths.insert path.toString
      let bytes ← ExprCodec.natOf (← field part "bytes")
      discard <| OwnerRebind.identityOf (← field part "sha256")
      if bytes == 0 then fail "ANCHOR_EMPTY_PART"
      moduleBytes := moduleBytes + bytes
      totalBytes := totalBytes + bytes
      if moduleBytes > artifactMaximum || totalBytes > anchorArtifactMaximum then
        fail "ANCHOR_ARTIFACT_BOUND"
      let metadata ← (nativePath path).symlinkMetadata
      if metadata.type != .file || metadata.numLinks != 1 ||
          metadata.byteSize.toNat != bytes then fail "ANCHOR_PART_METADATA"
      paths := paths.push path
    if paths[0]!.fileName != some (moduleName.toString ++ ".olean") ||
        paths != moduleParts paths[0]! then fail "ANCHOR_PART_NAMES"
    let nativePaths := paths.map nativePath
    plan := { plan with
      modules := plan.modules.push {
        anchorId := id
        moduleName := moduleName
        imports := imports
        addedNames := addedNames
        parts := paths }
      artifacts := plan.artifacts.insert moduleName
        (ImportArtifacts.ofArrays #[#[nativePaths[0]!, nativePaths[1]!, nativePaths[2]!], #[nativePaths[3]!, nativePaths[4]!]]) }
  if !plan.modules.isEmpty && plan.modules.back!.anchorId != anchorId then
    fail "ANCHOR_ROOT_ID_BINDING"
  let mut units : Std.HashSet String := {}
  let mut names : Std.HashSet Name := {}
  let mut realizedAdded := 0
  for unit in unitRows do
    exactObject unit #["unit_id", "outputs", "realization"]
    let id ← OwnerRebind.identityOf (← field unit "unit_id")
    if units.contains id then fail "ANCHOR_DUPLICATE_UNIT"
    units := units.insert id
    let realization ← ExprCodec.jsonResult (← field unit "realization").getStr?
    if realization != "added" && realization != "installed-singleton-theorem" &&
        realization != "installed-exact-nontheorem" then
      fail "ANCHOR_REALIZATION"
    let outputs ← ExprCodec.arrayOf (← field unit "outputs")
    if outputs.isEmpty || outputs.size > checkerLimits.maxNewNames ||
        (realization == "installed-singleton-theorem" && outputs.size != 1) then
      fail "ANCHOR_UNIT_OUTPUT_BOUND"
    let mut outputKinds : Array Nat := #[]
    for output in outputs do
      exactObject output #["name", "export_id", "kind", "level_params", "inventory_sha256"]
      let name ← ExprCodec.decodeName (← field output "name")
      CheckedExtension.requireName name
      if names.contains name then fail "ANCHOR_DUPLICATE_OUTPUT"
      names := names.insert name
      let kind ← ExprCodec.natOf (← field output "kind")
      if kind < 1 || kind > 6 ||
          (realization == "installed-singleton-theorem" && kind != 2) ||
          (realization == "installed-exact-nontheorem" && kind == 2) then
        fail "ANCHOR_OUTPUT_KIND"
      outputKinds := outputKinds.push kind
      let params ← field output "level_params"
      discard <| DeclCodec.paramsOf params codecLimits
      discard <| OwnerRebind.identityOf (← field output "export_id")
      discard <| OwnerRebind.identityOf (← field output "inventory_sha256")
      if realization == "added" then
        if !declaredAdded.contains name then fail "ANCHOR_ADDED_MAP_MISMATCH"
        realizedAdded := realizedAdded + 1
      else if declaredAdded.contains name then
        fail "ANCHOR_MATCHED_MAP_OVERLAP"
      plan := { plan with bindings := plan.bindings.push { name := name, kind := kind, params := params } }
      if plan.bindings.size > anchorNameMaximum then fail "ANCHOR_NAME_BOUND"
    if realization == "installed-exact-nontheorem" then
      let ordinary := outputKinds.size == 1 && (outputKinds[0]! == 1 || outputKinds[0]! == 3)
      let generated := outputKinds.contains 4 && outputKinds.all (fun kind => kind >= 4 && kind <= 6)
      if !ordinary && !generated then fail "ANCHOR_EXACT_NON_THEOREM_FAMILY"
  if realizedAdded != declaredCount then fail "ANCHOR_ADDED_MAP_CENSUS"
  return plan

def checkAnchorHeaders (env : Environment) (plan : AnchorPlan) : IO Unit := do
  let modules := env.allImportedModuleNames
  let data := env.header.moduleData
  if modules.size != data.size then fail "ANCHOR_RESTORED_HEADER_CENSUS"
  for selected in plan.modules do
    let mut moduleMatches := 0
    let mut expected : Std.HashSet Name := {}
    for name in selected.addedNames do expected := expected.insert name
    for i in [:modules.size] do
      if modules[i]! == selected.moduleName then
        moduleMatches := moduleMatches + 1
        let own := data[i]!
        if !own.isModule || own.imports != selected.imports ||
            own.constNames.size != selected.addedNames.size ||
            own.constants.size != selected.addedNames.size then
          fail "ANCHOR_RESTORED_HEADER"
        let mut seen : Std.HashSet Name := {}
        for name in own.constNames do
          if !expected.contains name || seen.contains name then
            fail "ANCHOR_RESTORED_OUTPUTS"
          seen := seen.insert name
    if moduleMatches != 1 then fail "ANCHOR_RESTORED_MODULE_IDENTITY"

/- No old type/body re-encoding: the registered live event supplied their full
   correspondence, and the protected exact artifact/import chain preserves it.
   These checks retain safe record kind, name and ordered-universe boundaries. -/
def checkAnchorRecords (env : Environment) (plan : AnchorPlan) (publicView : Bool)
    : IO Unit := do
  let view := env.setExporting publicView
  for row in plan.bindings do
    let some visible := view.find? row.name (skipRealize := true) |
      fail s!"ANCHOR_MISSING_RECORD name={row.name}"
    let some kernel := view.toKernelEnv.find? row.name |
      fail s!"ANCHOR_MISSING_KERNEL_RECORD name={row.name}"
    for actual in #[kernel, visible] do
      if actual.name != row.name || actual.isUnsafe || actual.isPartial then
        fail "ANCHOR_UNSAFE_OR_MISKEYED_RECORD"
      let kind ← match actual with
        | .defnInfo _ => pure 1
        | .thmInfo _ => pure 2
        | .opaqueInfo _ => pure 3
        | .inductInfo _ => pure 4
        | .ctorInfo _ => pure 5
        | .recInfo _ => pure 6
        | .axiomInfo _ =>
            if publicView && row.kind == 2 then pure 2 else fail "ANCHOR_UNWARRANTED_AXIOM_VIEW"
        | .quotInfo _ => fail "ANCHOR_QUOTIENT_OUTPUT"
      if kind != row.kind || (← DeclCodec.paramsJson actual.levelParams codecLimits) != row.params then
        fail "ANCHOR_RECORD_KIND_OR_UNIVERSES"

def checkWrittenHeader (env : Environment) (moduleName : Name)
    (names : Array Name) (imports : Array Import) : IO Unit := do
  let modules := env.allImportedModuleNames
  let data := env.header.moduleData
  if modules.size != data.size then fail "RESTORED_HEADER_CENSUS"
  let mut matchCount := 0
  let mut expected : Std.HashSet Name := {}
  for name in names do expected := expected.insert name
  for i in [:modules.size] do
    if modules[i]! == moduleName then
      matchCount := matchCount + 1
      let own := data[i]!
      if !own.isModule || own.imports != imports then fail "RESTORED_MODULE_HEADER"
      if own.constNames.size != names.size || own.constants.size != names.size then
        fail "RESTORED_OUTPUT_CENSUS"
      let mut seen : Std.HashSet Name := {}
      for name in own.constNames do
        if !expected.contains name || seen.contains name then fail "RESTORED_OUTPUT_NAMES"
        seen := seen.insert name
  if matchCount != 1 then fail "RESTORED_MODULE_IDENTITY"

def reread (output : System.FilePath) (moduleName : Name)
    (addedNames : Array Name) (addedInventories : Array Json)
    (matchedNames : Array Name) (matchedInventories : Array Json)
    (anchor : AnchorPlan) (level : OLeanLevel) : IO Unit := do
  let parts := (moduleParts output).map nativePath
  let artifacts := anchor.artifacts.insert moduleName
    (ImportArtifacts.ofArrays #[#[parts[0]!, parts[1]!, parts[2]!], #[parts[3]!, parts[4]!]])
  let restored ← importModules #[{ module := moduleName, importAll := false, isExported := true, isMeta := false }] {} 0
    (plugins := #[]) (leakEnv := false) (loadExts := false) (level := level) (arts := artifacts)
  requireModern restored
  checkAnchorHeaders restored anchor
  checkAnchorRecords restored anchor (level != .private)
  checkWrittenHeader restored moduleName addedNames anchor.imports
  checkInventories restored addedNames addedInventories (level != .private)
  if level == .private then
    checkInventories restored matchedNames matchedInventories false
  else
    checkMatchedPublic restored matchedNames matchedInventories

def run (sysroot inventoryPath requestPath anchorPlanPath outputPath reportPath : System.FilePath)
    : IO Unit := do
  let parts := moduleParts outputPath
  if parts.contains reportPath then fail "OUTPUT_REPORT_ALIAS"
  for path in parts do requireFresh path
  requireFresh reportPath
  let request ← readSelectedJson requestPath requestMaximum
  exactObject request #["schema", "semantic_id", "context_root", "foundation_id",
    "module_name", "targets", "unit_ids", "units", "anchor_id", "anchor_plan_sha256"]
  if (← ExprCodec.jsonResult (← field request "schema").getStr?) !=
      "DMKN_ORDINARY_MODULE_REQUEST_V2" then fail "REQUEST_SCHEMA"
  let anchor ← readAnchorPlan anchorPlanPath request
  let semanticId ← OwnerRebind.identityOf (← field request "semantic_id")
  let contextRoot ← OwnerRebind.identityOf (← field request "context_root")
  let foundationId ← OwnerRebind.identityOf (← field request "foundation_id")
  let moduleName ← bridgeModule (← field request "module_name")
  if anchor.modules.any (fun entry => entry.moduleName == moduleName) then
    fail "OUTPUT_ANCHOR_MODULE_COLLISION"
  if outputPath.fileName != some (moduleName.toString ++ ".olean") then
    fail "MODULE_OUTPUT_BASENAME"
  let targets ← targetNames (← field request "targets")
  let rawUnits ← ExprCodec.arrayOf (← field request "units")
  let unitIds ← ExprCodec.arrayOf (← field request "unit_ids")
  if rawUnits.isEmpty || rawUnits.size > checkerLimits.maxUnits ||
      rawUnits.size != unitIds.size then fail "UNIT_COUNT_BOUND"
  let mut seenIds : Std.HashSet String := {}
  for value in unitIds do
    let id ← OwnerRebind.identityOf value
    if seenIds.contains id then fail "DUPLICATE_UNIT_ID"
    seenIds := seenIds.insert id
  let inventory ← readSelectedJson inventoryPath inventoryMaximum
  if (← ExprCodec.arrayOf inventory).size != 581 then fail "FIXED_BASIS_CENSUS"
  -- Runtime-only fallback; locally registered parents use exact artifact maps.
  -- Neither inherited project LEAN_PATH nor peer binary input is permitted.
  searchPathRef.set [nativePath (sysroot / "lib" / "lean")]
  let privateInit ← importModules anchor.imports {} 0
    (plugins := #[]) (leakEnv := false) (loadExts := false) (level := .private)
    (arts := anchor.artifacts)
  requireModern privateInit
  checkAnchorHeaders privateInit anchor
  checkAnchorRecords privateInit anchor false
  let source : Export.SourceRecords := {
    environment := privateInit.toKernelEnv, grouping := #[], count := 0 }
  let basisNames ← Export.compareSourceBasis source inventory
  let (units, names, inventories) ← decodeUnits rawUnits basisNames anchor.names
  for target in targets do
    if !names.contains target && !anchor.names.contains target then fail "TARGET_NOT_IN_SELECTED_UNITS"
  -- Full private identities match genuinely warranted complete selected units.
  -- The scan prefix advances in request order; ambient names are never granted.
  -- Everything absent still passes unchanged kernel checking.
  let plan ← classifyUnits privateInit units basisNames anchor.names
  let exact ← CheckedExtension.checkBatch privateInit plan.addedUnits checkerLimits
  let exactEnv ← OwnerRebind.exposeAdded exact.environment exact.added
  checkInventories exactEnv names inventories false
  -- A SECOND unchanged checker pass checks only the delta. Public parent
  -- imports, no import-all, ensure hidden definitions cannot make this
  -- pass merely because the preceding private import happened to contain them.
  let publicInit ← importModules anchor.imports {} 0
    (plugins := #[]) (leakEnv := false) (loadExts := false) (level := .exported)
    (arts := anchor.artifacts)
  requireModern publicInit
  checkAnchorHeaders publicInit anchor
  checkAnchorRecords publicInit anchor true
  if !publicInit.header.isModule then fail "MODERN_OUTPUT_ENVIRONMENT_REQUIRED"
  checkMatchedPublic publicInit plan.matchedNames plan.matchedInventories
  -- This actual compatibility check may fail when theorem-body erasure loses
  -- conversion (for example Acc.rec). Private success never waives this gate.
  let publicChecked ← CheckedExtension.checkBatch publicInit plan.addedUnits checkerLimits
  let publicEnv ← OwnerRebind.exposeAdded publicChecked.environment publicChecked.added
  let writerEnv := publicEnv.setMainModule moduleName
  checkInventories writerEnv plan.addedNames plan.addedInventories false
  checkInventories writerEnv plan.addedNames plan.addedInventories true
  checkMatchedPublic writerEnv plan.matchedNames plan.matchedInventories
  if writerEnv.imports != anchor.imports then fail "OUTPUT_IMPORTS_CHANGED"
  -- All semantic and visibility refusals above precede writing. Writer/I/O or
  -- reread failure can leave partial uncommitted files; never adopt on failure.
  for path in parts do requireFresh path
  requireFresh reportPath
  writeModule writerEnv (nativePath outputPath)
  let artifactRows ← inspectParts parts
  -- Validation imports run in separate processes after this process exits.
  -- The worker must never promote this pending record before BOTH rereads.
  let encodedNewNames ← names.mapM (fun name => ExprCodec.encodeName name)
  let report := Json.mkObj [
    ("schema", .str "DMKN_ORDINARY_MODULE_PENDING_V3"),
    ("assurance", .str "LOCAL_CHECKED_ANCHORED_MODULE_PENDING_REREADS"),
    ("semantic_id", .str semanticId), ("context_root", .str contextRoot),
    ("foundation_id", .str foundationId),
    ("module_name", ← ExprCodec.encodeName moduleName),
    ("anchor_id", .str anchor.anchorId),
    ("anchor_plan_sha256", ← field request "anchor_plan_sha256"),
    ("direct_imports", ← encodedImports anchor.imports),
    ("anchor_names", ← encodedNames anchor.names),
    ("targets", ← field request "targets"), ("unit_ids", .arr unitIds),
    ("names", .arr encodedNewNames), ("inventories", .arr inventories),
    ("matched_unit_indices", toJson plan.matchedIndices),
    ("matched_names", .arr (← plan.matchedNames.mapM (fun name => ExprCodec.encodeName name))),
    ("matched_inventories", .arr plan.matchedInventories),
    ("added_names", .arr (← plan.addedNames.mapM (fun name => ExprCodec.encodeName name))),
    ("added_inventories", .arr plan.addedInventories),
    ("units_checked", toJson plan.addedUnits.size),
    ("units_matched", toJson plan.matchedIndices.size),
    ("checking_passes", toJson (2 : Nat)),
    ("basis_rows", toJson basisNames.size), ("artifact_parts", .arr artifactRows)]
  let bytes := report.compress.toUTF8
  if bytes.size > reportMaximum then fail "REPORT_BYTE_BOUND"
  let handle ← IO.FS.Handle.mk (nativePath reportPath) .writeNew
  handle.write bytes
  handle.flush

/- Fresh-process validation. No separate Init import: the generated module's
   exact imports are loaded once by reread. The protected worker binds this
   request/pending record and all five artifact bytes across all three phases. -/
def rereadPending (sysroot requestPath anchorPlanPath outputPath pendingPath : System.FilePath)
    (level : OLeanLevel) : IO Unit := do
  let request ← readSelectedJson requestPath requestMaximum
  exactObject request #["schema", "semantic_id", "context_root", "foundation_id",
    "module_name", "targets", "unit_ids", "units", "anchor_id", "anchor_plan_sha256"]
  if (← field request "schema") != .str "DMKN_ORDINARY_MODULE_REQUEST_V2" then
    fail "REQUEST_SCHEMA"
  let anchor ← readAnchorPlan anchorPlanPath request
  let pending ← readSelectedJson pendingPath reportMaximum
  exactObject pending #["schema", "assurance", "semantic_id", "context_root",
    "foundation_id", "module_name", "targets", "unit_ids", "names", "inventories",
    "matched_unit_indices", "matched_names", "matched_inventories", "added_names",
    "added_inventories", "units_checked", "units_matched", "checking_passes",
    "basis_rows", "artifact_parts", "anchor_id", "anchor_plan_sha256", "direct_imports", "anchor_names"]
  if (← field pending "schema") != .str "DMKN_ORDINARY_MODULE_PENDING_V3" ||
      (← field pending "assurance") != .str "LOCAL_CHECKED_ANCHORED_MODULE_PENDING_REREADS" then
    fail "PENDING_REPORT_REQUIRED"
  for key in #["semantic_id", "context_root", "foundation_id", "module_name",
      "targets", "unit_ids", "anchor_id", "anchor_plan_sha256"] do
    if (← field pending key) != (← field request key) then fail "PENDING_REQUEST_BINDING"
  let moduleName ← bridgeModule (← field request "module_name")
  if anchor.modules.any (fun entry => entry.moduleName == moduleName) then
    fail "OUTPUT_ANCHOR_MODULE_COLLISION"
  if (← field pending "direct_imports") != (← encodedImports anchor.imports) ||
      (← field pending "anchor_names") != (← encodedNames anchor.names) then
    fail "PENDING_ANCHOR_PLAN_BINDING"
  if outputPath.fileName != some (moduleName.toString ++ ".olean") then
    fail "MODULE_OUTPUT_BASENAME"
  let targets ← targetNames (← field request "targets")
  let rawUnits ← ExprCodec.arrayOf (← field request "units")
  let unitIds ← ExprCodec.arrayOf (← field request "unit_ids")
  if rawUnits.isEmpty || rawUnits.size > checkerLimits.maxUnits ||
      rawUnits.size != unitIds.size then fail "UNIT_COUNT_BOUND"
  let mut inventories : Array Json := #[]
  for raw in rawUnits do
    let fields ← ExprCodec.arrayOf raw (some 3)
    inventories := inventories ++ (← ExprCodec.arrayOf fields[2]!)
    if inventories.size > checkerLimits.maxNewNames then fail "BATCH_NAME_BOUND"
  let names ← DeclCodec.expectedNames inventories codecLimits
  let encodedNames ← names.mapM (fun name => ExprCodec.encodeName name)
  if (← field pending "names") != .arr encodedNames ||
      (← field pending "inventories") != .arr inventories ||
      (← field pending "checking_passes") != toJson (2 : Nat) ||
      (← field pending "basis_rows") != toJson (581 : Nat) then
    fail "PENDING_CHECKED_INVENTORY_BINDING"
  for target in targets do
    if !names.contains target && !anchor.names.contains target then fail "TARGET_NOT_IN_SELECTED_UNITS"
  let (addedNames, addedInventories, matchedNames, matchedInventories) ←
    reportPartition rawUnits pending
  let artifactRows ← inspectParts (moduleParts outputPath)
  if (← field pending "artifact_parts") != .arr artifactRows then
    fail "PENDING_ARTIFACT_BINDING"
  searchPathRef.set [nativePath (sysroot / "lib" / "lean")]
  reread outputPath moduleName addedNames addedInventories matchedNames matchedInventories anchor level
  if (← inspectParts (moduleParts outputPath)) != artifactRows then
    fail "REREAD_ARTIFACT_SIZE_CHANGED"

end OrdinaryLean.ModuleBridge

def main (args : List String) : IO UInt32 := do
  try
    match args with
    | ["build", sysroot, inventoryPath, requestPath, anchorPlanPath, outputPath, reportPath] =>
        OrdinaryLean.ModuleBridge.run
          (← OrdinaryLean.ModuleBridge.absolutePath sysroot)
          (← OrdinaryLean.ModuleBridge.absolutePath inventoryPath)
          (← OrdinaryLean.ModuleBridge.absolutePath requestPath)
          (← OrdinaryLean.ModuleBridge.absolutePath anchorPlanPath)
          (← OrdinaryLean.ModuleBridge.absolutePath outputPath)
          (← OrdinaryLean.ModuleBridge.absolutePath reportPath)
        return 0
    | ["reread-private", sysroot, requestPath, anchorPlanPath, outputPath, pendingPath] =>
        OrdinaryLean.ModuleBridge.rereadPending
          (← OrdinaryLean.ModuleBridge.absolutePath sysroot)
          (← OrdinaryLean.ModuleBridge.absolutePath requestPath)
          (← OrdinaryLean.ModuleBridge.absolutePath anchorPlanPath)
          (← OrdinaryLean.ModuleBridge.absolutePath outputPath)
          (← OrdinaryLean.ModuleBridge.absolutePath pendingPath)
          .private
        return 0
    | ["reread-exported", sysroot, requestPath, anchorPlanPath, outputPath, pendingPath] =>
        OrdinaryLean.ModuleBridge.rereadPending
          (← OrdinaryLean.ModuleBridge.absolutePath sysroot)
          (← OrdinaryLean.ModuleBridge.absolutePath requestPath)
          (← OrdinaryLean.ModuleBridge.absolutePath anchorPlanPath)
          (← OrdinaryLean.ModuleBridge.absolutePath outputPath)
          (← OrdinaryLean.ModuleBridge.absolutePath pendingPath)
          .exported
        return 0
    | _ => OrdinaryLean.ModuleBridge.fail "USAGE build sysroot basisInventory request anchorPlan outputOlean pending | reread-private/reread-exported sysroot request anchorPlan outputOlean pending"
  catch error =>
    let stderr ← IO.getStderr
    stderr.putStrLn error.toString
    stderr.flush
    return 1
