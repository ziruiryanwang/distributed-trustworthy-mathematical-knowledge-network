import BaselineArtifactCore04

/- Conditional correspondence to an approved immutable original library.
   The controller authenticates the fixed inventory, snapshot/support, every
   complete accepted unit and identity label against current protected warrants.
   This native tool does not prove a unit, create a declaration or confer local
   registration authority. No saved report is a transferable certificate. -/

open Lean

namespace OrdinaryLean.ReferenceBase

def requestMaximum : Nat := 100663296
def unitsMaximumBytes : Nat := 67108864
def unitMaximumBytes : Nat := 8388608
def reportMaximum : Nat := 33554432
def unitMaximum : Nat := 8192
def nameMaximum : Nat := 262144
def edgeMaximum : Nat := 262144
def nodeMaximum : Nat := 20000000
def targetMaximum : Nat := 1024
def codecLimits : DeclCodec.Limits := {}

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"ORDINARY_REFERENCE_BASE {message}"

def identityOf (value : Json) : IO String := do
  let text ← ExprCodec.jsonResult value.getStr?
  if text.utf8ByteSize != 64 || !text.toList.all (fun c =>
      ('0' ≤ c && c ≤ '9') || ('a' ≤ c && c ≤ 'f')) then
    fail "IDENTITY_SHAPE"
  return text

def phase (message : String) : IO Unit := do
  let stderr ← IO.getStderr
  stderr.putStrLn s!"ORDINARY_REFERENCE_BASE_PHASE {message}"
  stderr.flush

def readJson (path : System.FilePath) (maximum : Nat) : IO Json := do
  let path := BaselineArtifacts.nativePath path
  let metadata ← path.symlinkMetadata
  if metadata.type != .file || metadata.numLinks != 1 then
    fail "ORDINARY_SINGLE_LINK_INPUT_REQUIRED"
  if metadata.byteSize.toNat > maximum then fail "INPUT_BYTE_BOUND"
  let handle ← IO.FS.Handle.mk path .read
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
  match Json.parse text with
  | .ok value => return value
  | .error _ => fail "INPUT_JSON"

structure Binding where
  name : Name
  exportId : String
  deriving Inhabited

def bindingOf (raw : Json) : IO Binding := do
  BaselineArtifacts.exactObject raw #["name", "export_id"]
  let name ← ExprCodec.decodeName (← BaselineArtifacts.field raw "name") codecLimits.expr
  CheckedExtension.requireName name
  return { name, exportId := ← identityOf (← BaselineArtifacts.field raw "export_id") }

def bindingJson (binding : Binding) : IO Json := do
  return Json.mkObj [("name", ← ExprCodec.encodeName binding.name codecLimits.expr),
    ("export_id", .str binding.exportId)]

structure MatchedUnit where
  unitId : String
  names : Array Name
  outputs : Array Binding
  expected : Array Json
  singletonAbstract : Bool
  deriving Inhabited

structure PrivateMatch where
  units : Array MatchedUnit := #[]
  owners : Std.HashMap Name Nat := {}
  symbols : Std.HashMap Name String := {}
  basis : Std.HashSet Name := {}
  encodedNodes : Nat := 0
  scanNodes : Nat := 0
  edges : Nat := 0
  nameCount : Nat := 0
  unitBytes : Nat := 0

/-- Full selected semantic references, not just statement references. The shared
    scan includes values (including theorem/opaque proofs), recursor rule RHS and
    constructor names. Add the remaining generated metadata and implicit literal
    roots. Definition/theorem/opaque `all` is documented nonkernel metadata; its
    bytes still participate in exact inventory equality. -/
def scanRecord (actual : ConstantInfo) (initial : BootstrapProbe.Scan)
    : IO BootstrapProbe.Scan := do
  let mut scan ← BootstrapProbe.scanInfo actual initial
  match actual with
  | .inductInfo d =>
      for name in d.all do scan := { scan with refs := scan.refs.insert name }
      for name in d.ctors do scan := { scan with refs := scan.refs.insert name }
  | .ctorInfo d => scan := { scan with refs := scan.refs.insert d.induct }
  | .recInfo d =>
      for name in d.all do scan := { scan with refs := scan.refs.insert name }
      for rule in d.rules do scan := { scan with refs := scan.refs.insert rule.ctor }
  | .quotInfo _ =>
      for name in BootstrapProbe.quotNames do scan := { scan with refs := scan.refs.insert name }
      scan := { scan with refs := scan.refs.insert ``Eq }
  | _ => pure ()
  if scan.natLit then scan := { scan with refs := scan.refs.insert ``Nat }
  if !scan.strLits.isEmpty then
    for name in BootstrapProbe.stringRoots do
      scan := { scan with refs := scan.refs.insert name }
  return scan

def checkSnapshotView (env : Environment) (selection : BaselineArtifacts.Selection)
    (imports : Array Import) (privateView : Bool) : IO (Array Name) := do
  if env.header.imports != imports then fail "SNAPSHOT_ROOT_IMPORTS"
  let modules := env.header.modules
  let data := env.header.moduleData
  if modules.isEmpty || modules.size > BaselineArtifacts.moduleMaximum || modules.size != data.size then
    fail "SNAPSHOT_MODULE_CENSUS"
  if privateView && modules.size != selection.moduleNames.size then
    fail "PRIVATE_SNAPSHOT_CENSUS"
  let mut names : Array Name := #[]
  let mut seen : Std.HashSet Name := {}
  let mut edges := 0
  for i in [:modules.size] do
    let entry := modules[i]!
    BaselineArtifacts.requireModuleName entry.module
    if seen.contains entry.module || (selection.artifacts.find? entry.module).isNone then
      fail "UNBOUND_OR_DUPLICATE_IMPORTED_MODULE"
    if !data[i]!.isModule then fail "LEGACY_IMPORTED_MODULE"
    if privateView && (!entry.hasData || !entry.importAll) then
      fail "PRIVATE_MODULE_DATA_REQUIRED"
    edges := edges + data[i]!.imports.size
    if edges > BaselineArtifacts.importEdgeMaximum then fail "SNAPSHOT_IMPORT_EDGE_BOUND"
    -- Public active data may be a strict subset. Every named dependency must
    -- nevertheless be in the exact map; an absent inactive child is not loaded.
    for dependency in data[i]!.imports do
      if (selection.artifacts.find? dependency.module).isNone then
        fail "SNAPSHOT_DEPENDENCY_NOT_BOUND"
    seen := seen.insert entry.module
    names := names.push entry.module
  for root in imports do
    if !seen.contains root.module then fail "SNAPSHOT_ROOT_NOT_IMPORTED"
  return names

def checkArtifactSizes (selection : BaselineArtifacts.Selection) : IO Unit := do
  for name in selection.moduleNames do
    let some paths := selection.paths.find? name | fail "SNAPSHOT_PART_PATHS"
    let some counts := selection.byteCounts.find? name | fail "SNAPSHOT_PART_COUNTS"
    for i in [:paths.size] do
      let metadata ← (BaselineArtifacts.nativePath paths[i]!).symlinkMetadata
      if metadata.type != .file || metadata.byteSize.toNat != counts[i]! then
        fail "SNAPSHOT_PART_CHANGED"

def matchPrivate (env : Environment) (rawUnits : Array Json) (basisNames : Array Name)
    : IO PrivateMatch := do
  if rawUnits.isEmpty || rawUnits.size > unitMaximum then fail "PRIVATE_UNIT_BOUND"
  let mut state : PrivateMatch := {}
  let mut allowed : Std.HashSet Name := {}
  for name in basisNames do
    state := { state with basis := state.basis.insert name }
    allowed := allowed.insert name
  let mut unitIds : Std.HashSet String := {}
  let mut exportIds : Std.HashSet String := {}
  -- Exact serialized raw-unit array bytes, including brackets and commas.
  let mut rawBytes := 2
  let view := env.setExporting false
  for entry in rawUnits do
    BaselineArtifacts.exactObject entry #["unit_id", "unit", "outputs"]
    let unitId ← identityOf (← BaselineArtifacts.field entry "unit_id")
    if unitIds.contains unitId then fail "DUPLICATE_UNIT_ID"
    let raw ← BaselineArtifacts.field entry "unit"
    let size := raw.compress.utf8ByteSize
    if size == 0 || size > unitMaximumBytes then fail "PRIVATE_UNIT_BYTE_BOUND"
    rawBytes := rawBytes + size + (if state.units.isEmpty then 0 else 1)
    if rawBytes > unitsMaximumBytes then fail "PRIVATE_UNIT_ARRAY_BYTE_BOUND"
    let fields ← ExprCodec.arrayOf raw (some 3)
    let mut nodes ← DeclCodec.descriptorNodes fields[1]! codecLimits
    for row in (← ExprCodec.arrayOf fields[2]!) do
      nodes := nodes + (← DeclCodec.inventoryNodes row codecLimits)
    let encodedNodes := state.encodedNodes + nodes
    if encodedNodes > nodeMaximum then fail "ENCODED_NODE_BOUND"
    let unit ← DeclCodec.decodeUnit allowed raw codecLimits
    discard <| CheckedExtension.allowedDeclaration unit.decl
    let names ← DeclCodec.expectedNames unit.expected codecLimits
    if state.nameCount + names.size > nameMaximum then fail "PRIVATE_NAME_BOUND"
    let labels ← ExprCodec.arrayOf (← BaselineArtifacts.field entry "outputs") (some names.size)
    let mut outputs : Array Binding := #[]
    let mut groupAllowed := allowed
    for name in names do groupAllowed := groupAllowed.insert name
    let mut singletonAbstract := false
    match unit.decl with
    | .defnDecl d =>
        if (← DeclCodec.inventoryRow (.defnInfo d) codecLimits) != unit.expected[0]! then
          fail "DESCRIPTOR_INVENTORY_MISMATCH"
        singletonAbstract := names == #[d.name] && d.all == [d.name]
    | .thmDecl d =>
        if (← DeclCodec.inventoryRow (.thmInfo d) codecLimits) != unit.expected[0]! then
          fail "DESCRIPTOR_INVENTORY_MISMATCH"
        singletonAbstract := names == #[d.name] && d.all == [d.name]
    | .opaqueDecl d =>
        if (← DeclCodec.inventoryRow (.opaqueInfo d) codecLimits) != unit.expected[0]! then
          fail "DESCRIPTOR_INVENTORY_MISMATCH"
        singletonAbstract := names == #[d.name] && d.all == [d.name]
    | .inductDecl .. => pure () -- Complete generated census is a real warrant premise.
    | _ => fail "UNSUPPORTED_PRIVATE_DESCRIPTOR"
    let mut scan : BootstrapProbe.Scan := { nodes := state.scanNodes }
    for i in [:names.size] do
      let binding ← bindingOf labels[i]!
      if binding.name != names[i]! || exportIds.contains binding.exportId then
        fail "OUTPUT_IDENTITY_LABELS"
      let some actual := view.find? binding.name (skipRealize := true) |
        fail s!"MISSING_PRIVATE_RECORD name={binding.name}"
      let some checked := env.toKernelEnv.find? binding.name |
        fail s!"MISSING_PRIVATE_KERNEL_RECORD name={binding.name}"
      if actual.name != binding.name || actual.isAxiom || actual.isUnsafe || actual.isPartial then
        fail "INCOMPLETE_OR_UNSAFE_PRIVATE_RECORD"
      if (← DeclCodec.inventoryRow actual codecLimits) != unit.expected[i]! then
        fail s!"PRIVATE_INVENTORY_MISMATCH name={binding.name}"
      if checked.name != binding.name || checked.isAxiom || checked.isUnsafe || checked.isPartial ||
          (← DeclCodec.inventoryRow checked codecLimits) != unit.expected[i]! then
        fail s!"PRIVATE_KERNEL_INVENTORY_MISMATCH name={binding.name}"
      scan ← scanRecord actual scan
      outputs := outputs.push binding
      exportIds := exportIds.insert binding.exportId
    let edges := state.edges + scan.refs.size
    if scan.nodes > nodeMaximum || edges > edgeMaximum then fail "PRIVATE_SCAN_BOUND"
    for name in scan.refs do
      CheckedExtension.requireName name
      if !groupAllowed.contains name then fail s!"UNCLOSED_PRIVATE_REFERENCE name={name}"
    let index := state.units.size
    let mut owners := state.owners
    let mut symbols := state.symbols
    for binding in outputs do
      owners := owners.insert binding.name index
      symbols := symbols.insert binding.name binding.exportId
    state := { state with
      units := state.units.push { unitId, names, outputs, expected := unit.expected, singletonAbstract },
      owners, symbols, encodedNodes, scanNodes := scan.nodes, edges,
      nameCount := state.nameCount + names.size, unitBytes := rawBytes }
    unitIds := unitIds.insert unitId
    allowed := groupAllowed
  return state

/-- Match one observed view to its exact already checked private record. A safe
    singleton body may be abstract, but no computational rule or axiom is added.
    This is interpretation into that original environment, not arbitrary merging
    of declarations with equal signatures or a promise of preserved reduction. -/
def matchPublicRow (actual : ConstantInfo) (expected : Json) (name : Name)
    (singletonAbstract : Bool) (view : String) : IO String := do
  if actual.name != name || actual.isUnsafe || actual.isPartial then
    fail s!"UNSAFE_OR_MISKEYED_PUBLIC_RECORD name={name} view={view}"
  match actual with
  | .axiomInfo d =>
      let fields ← ExprCodec.arrayOf expected (some 5)
      let expectedKind ← ExprCodec.natOf fields[1]!
      if !singletonAbstract || ![1, 2, 3].contains expectedKind then
        fail s!"PUBLIC_ABSTRACTION_UNSUPPORTED name={name} view={view} kind={expectedKind}"
      if fields[0]! != (← ExprCodec.encodeName name codecLimits.expr) ||
          (← DeclCodec.paramsJson d.levelParams codecLimits) != fields[2]! ||
          (← ExprCodec.encode d.levelParams d.type codecLimits.expr) != fields[3]! then
        fail s!"PUBLIC_ABSTRACT_SIGNATURE_MISMATCH name={name} view={view}"
      return if expectedKind == 1 then "abstract_singleton_definition"
        else if expectedKind == 2 then "erased_singleton_theorem"
        else "abstract_singleton_opaque"
  | _ =>
      if (← DeclCodec.inventoryRow actual codecLimits) != expected then
        fail s!"PUBLIC_INVENTORY_MISMATCH name={name} view={view}"
      return "full"

/-- Original signature, retaining ordered universe and binder metadata. -/
def originalSignature (info : ConstantInfo) : IO Json := do
  return .arr #[← ExprCodec.encodeName info.name codecLimits.expr,
    ← DeclCodec.paramsJson info.levelParams codecLimits,
    ← ExprCodec.encode info.levelParams info.type codecLimits.expr]

def quotKindCode : QuotKind → Nat
  | .type => 0
  | .ctor => 1
  | .lift => 2
  | .ind => 3

/-- Private basis equality is unchanged. Present public basis records use the
    original full record or approved singleton abstraction. Fixed primitives
    retain their existing exact policy; none may become an abstract group. -/
def matchBasisRecord (original actual : ConstantInfo) (allowAbstraction : Bool)
    (view : String) : IO String := do
  let name := original.name
  if actual.name != name || actual.isUnsafe || actual.isPartial then
    fail s!"BASIS_VIEW_NAME_OR_SAFETY name={name} view={view}"
  match original with
  | .axiomInfo _ =>
      if !BootstrapProbe.allowedAxioms.contains name then
        fail s!"BASIS_AXIOM_POLICY name={name} view={view}"
      let .axiomInfo _ := actual | fail s!"BASIS_AXIOM_KIND name={name} view={view}"
      if (← originalSignature actual) != (← originalSignature original) then
        fail s!"BASIS_AXIOM_SIGNATURE name={name} view={view}"
      return "full"
  | .quotInfo privateQuot =>
      if !BootstrapProbe.quotNames.contains name then
        fail s!"BASIS_QUOT_POLICY name={name} view={view}"
      let .quotInfo publicQuot := actual | fail s!"BASIS_QUOT_KIND name={name} view={view}"
      if quotKindCode publicQuot.kind != quotKindCode privateQuot.kind ||
          (← originalSignature actual) != (← originalSignature original) then
        fail s!"BASIS_QUOT_SIGNATURE_OR_KIND name={name} view={view}"
      return "full"
  | _ =>
      let singleton := allowAbstraction && (match original with
        | .defnInfo d => d.all == [d.name]
        | .thmInfo d => d.all == [d.name]
        | .opaqueInfo d => d.all == [d.name]
        | _ => false)
      matchPublicRow actual (← DeclCodec.inventoryRow original codecLimits) name singleton view

structure PublicBasis where
  rows : Array Json := #[]
  usable : Std.HashSet Name := {}
  usableNames : Array Name := #[]
  scanNodes : Nat := 0
  edges : Nat := 0
  pruningRounds : Nat := 0

/-- Validate every present record, then compute the greatest common semantic-
    dependency-closed subset. Absence never creates a declaration. Full records
    contribute bodies/rules, abstract ones only their actual signature. -/
def matchBasisViews (privateEnv publicEnv : Environment) (basisNames : Array Name)
    (inventoryRows : Array Json) (privateMatch : PrivateMatch) : IO PublicBasis := do
  let privateView := privateEnv.setExporting false
  let publicView := publicEnv.setExporting true
  let mut result : PublicBasis := {}
  let mut dependencies : Std.HashMap Name (Std.HashSet Name) := {}
  let mut totalNodes := privateMatch.scanNodes
  let mut totalEdges := privateMatch.edges
  for i in [:basisNames.size] do
    let name := basisNames[i]!
    let some original := privateEnv.toKernelEnv.find? name |
      fail s!"MISSING_PRIVATE_KERNEL_BASIS_RECORD name={name} view=private_kernel_basis"
    let some privateRecord := privateView.find? name (skipRealize := true) |
      fail s!"MISSING_PRIVATE_FRONTEND_BASIS_RECORD name={name} view=private_frontend_basis"
    discard <| matchBasisRecord original privateRecord false "private_frontend_basis"
    let publicRecord := publicView.find? name (skipRealize := true)
    let checkedRecord := publicEnv.toKernelEnv.find? name
    let mut projection := "absent"
    let mut kernelProjection := "absent"
    let mut scan : BootstrapProbe.Scan := { nodes := totalNodes }
    if let some actual := publicRecord then
      projection ← matchBasisRecord original actual true "public_frontend_basis"
      scan ← scanRecord actual scan
    if let some actual := checkedRecord then
      kernelProjection ← matchBasisRecord original actual true "public_kernel_basis"
      scan ← scanRecord actual scan
    totalNodes := scan.nodes
    totalEdges := totalEdges + scan.refs.size
    if totalNodes > nodeMaximum || totalEdges > edgeMaximum then fail "BASIS_SCAN_BOUND"
    for dependency in scan.refs do
      CheckedExtension.requireName dependency
      if !privateMatch.basis.contains dependency then
        fail s!"BASIS_REFERENCE_OUTSIDE_FIXED_BASIS name={name} dependency={dependency}"
    dependencies := dependencies.insert name scan.refs
    let fields ← ExprCodec.arrayOf inventoryRows[i]! (some 5)
    if fields[0]! != (← ExprCodec.encodeName name codecLimits.expr) then
      fail s!"BASIS_REPORT_ORDER name={name}"
    let row := Json.mkObj [("name", fields[0]!), ("kind", fields[1]!),
      ("level_params", ← DeclCodec.paramsJson original.levelParams codecLimits), ("projection", .str projection),
      ("kernel_projection", .str kernelProjection)]
    result := { result with
      rows := result.rows.push row,
      usable := if publicRecord.isSome && checkedRecord.isSome then
        result.usable.insert name else result.usable }
  -- Monotone deletion. Each counted round removes at least one of 581 names;
  -- the final unchanged pass is not counted. Cyclic supported groups survive.
  let mut changed := true
  while changed do
    changed := false
    for name in basisNames do
      if !result.usable.contains name then continue
      let some refs := dependencies[name]? | fail s!"BASIS_DEPENDENCY_CENSUS name={name}"
      for dependency in refs do
        if !result.usable.contains dependency then
          result := { result with usable := result.usable.erase name }
          changed := true
          break
    if changed then
      result := { result with pruningRounds := result.pruningRounds + 1 }
      if result.pruningRounds > basisNames.size then fail "BASIS_PRUNING_BOUND"
  let usableNames := basisNames.filter (fun name => result.usable.contains name)
  return { result with
    usableNames, scanNodes := totalNodes - privateMatch.scanNodes,
    edges := totalEdges - privateMatch.edges }

structure PublicMatch where
  visible : Std.HashSet Nat := {}
  projections : Std.HashMap Name String := {}
  kernelProjections : Std.HashMap Name String := {}
  scanNodes : Nat := 0
  edges : Nat := 0
  nameCount : Nat := 0

def matchPublic (env : Environment) (privateMatch : PrivateMatch) (publicBasis : PublicBasis)
    (targets : Array Binding)
    : IO PublicMatch := do
  let view := env.setExporting true
  let mut todo : Array Nat := #[]
  let mut queued : Std.HashSet Nat := {}
  for target in targets do
    let some owner := privateMatch.owners[target.name]? | fail "TARGET_NOT_IN_PRIVATE_UNITS"
    if privateMatch.symbols[target.name]? != some target.exportId then
      fail "TARGET_IDENTITY_MISMATCH"
    if !queued.contains owner then
      queued := queued.insert owner
      todo := todo.push owner
  let mut result : PublicMatch := {}
  let initialScanNodes := privateMatch.scanNodes + publicBasis.scanNodes
  let initialEdges := privateMatch.edges + publicBasis.edges
  let mut totalScanNodes := initialScanNodes
  let mut totalEdges := initialEdges
  let mut cursor := 0
  while cursor < todo.size do
    let index := todo[cursor]!
    cursor := cursor + 1
    let unit := privateMatch.units[index]!
    let mut scan : BootstrapProbe.Scan := { nodes := totalScanNodes }
    for i in [:unit.names.size] do
      let name := unit.names[i]!
      let some actual := view.find? name (skipRealize := true) |
        fail s!"MISSING_PUBLIC_RECORD name={name} view=public_frontend_unit"
      let some checked := env.toKernelEnv.find? name |
        fail s!"MISSING_PUBLIC_KERNEL_RECORD name={name} view=public_kernel_unit"
      let projection ← matchPublicRow actual unit.expected[i]! name unit.singletonAbstract "public_frontend_unit"
      let kernelProjection ← matchPublicRow checked unit.expected[i]! name unit.singletonAbstract "public_kernel_unit"
      -- setExporting changes find?, not toKernelEnv. Match both real maps and
      -- take the union of semantic references. A full view requires its whole
      -- semantic support; an abstract view contributes only its type.
      scan ← scanRecord actual scan
      scan ← scanRecord checked scan
      result := { result with
        projections := result.projections.insert name projection,
        kernelProjections := result.kernelProjections.insert name kernelProjection }
    totalScanNodes := scan.nodes
    totalEdges := totalEdges + scan.refs.size
    if totalScanNodes > nodeMaximum || totalEdges > edgeMaximum then fail "PUBLIC_SCAN_BOUND"
    for name in scan.refs do
      CheckedExtension.requireName name
      if privateMatch.basis.contains name then
        if !publicBasis.usable.contains name then
          fail s!"PUBLIC_BASIS_NOT_USABLE name={name}"
        continue
      let some dependency := privateMatch.owners[name]? |
        fail s!"PUBLIC_REFERENCE_OUTSIDE_PRIVATE_WARRANT name={name}"
      if !queued.contains dependency then
        if queued.size >= unitMaximum then fail "PUBLIC_UNIT_BOUND"
        queued := queued.insert dependency
        todo := todo.push dependency
    result := { result with
      visible := result.visible.insert index,
      nameCount := result.nameCount + unit.names.size }
  return { result with
    scanNodes := totalScanNodes - initialScanNodes,
    edges := totalEdges - initialEdges }

def publicRows (privateMatch : PrivateMatch) (publicMatch : PublicMatch) : IO (Array Json) := do
  let mut rows : Array Json := #[]
  let mut bytes := 0
  for i in [:privateMatch.units.size] do
    if !publicMatch.visible.contains i then continue
    let unit := privateMatch.units[i]!
    let mut outputs : Array Json := #[]
    for j in [:unit.outputs.size] do
      let binding := unit.outputs[j]!
      let expected ← ExprCodec.arrayOf unit.expected[j]! (some 5)
      let some projection := publicMatch.projections[binding.name]? |
        fail "PUBLIC_PROJECTION_CENSUS"
      let some kernelProjection := publicMatch.kernelProjections[binding.name]? |
        fail "PUBLIC_KERNEL_PROJECTION_CENSUS"
      outputs := outputs.push (Json.mkObj [
        ("name", ← ExprCodec.encodeName binding.name codecLimits.expr),
        ("export_id", .str binding.exportId), ("kind", expected[1]!),
        ("level_params", expected[2]!), ("projection", .str projection),
        ("kernel_projection", .str kernelProjection)])
    let row := Json.mkObj [("unit_id", .str unit.unitId), ("outputs", .arr outputs)]
    bytes := bytes + row.compress.utf8ByteSize
    if bytes > reportMaximum then fail "REPORT_BYTE_BOUND"
    rows := rows.push row
  return rows

def run (inventoryPath artifactMapPath requestPath reportPath : System.FilePath) : IO Unit := do
  BaselineArtifacts.requireFresh reportPath
  let inventory ← readJson inventoryPath BaselineArtifacts.requestMaximum
  let inventoryRows ← ExprCodec.arrayOf inventory
  if inventoryRows.size != 581 then fail "FIXED_BASIS_COUNT"
  let artifactMap ← readJson artifactMapPath BaselineArtifacts.replayRequestMaximum
  BaselineArtifacts.exactObject artifactMap #["schema", "mode", "modules", "artifacts"]
  if (← ExprCodec.jsonResult (← BaselineArtifacts.field artifactMap "schema").getStr?) !=
      "DMKN_ORDINARY_BASELINE_ARTIFACT_REQUEST_V1" ||
      (← ExprCodec.jsonResult (← BaselineArtifacts.field artifactMap "mode").getStr?) != "replay" then
    fail "EXPLICIT_SNAPSHOT_REPLAY_REQUIRED"
  let imports ← BaselineArtifacts.rootModules (← BaselineArtifacts.field artifactMap "modules")
  let selection ← BaselineArtifacts.replaySelection (← BaselineArtifacts.field artifactMap "artifacts")
  let request ← readJson requestPath requestMaximum
  BaselineArtifacts.exactObject request #["schema", "semantic_id", "foundation_id", "context_root",
    "snapshot_id", "support_id", "units", "targets"]
  if (← ExprCodec.jsonResult (← BaselineArtifacts.field request "schema").getStr?) !=
      "DMKN_ORDINARY_REFERENCE_BASE_REQUEST_V1" then fail "REQUEST_SCHEMA"
  let semanticId ← identityOf (← BaselineArtifacts.field request "semantic_id")
  let foundationId ← identityOf (← BaselineArtifacts.field request "foundation_id")
  let contextRoot ← identityOf (← BaselineArtifacts.field request "context_root")
  let snapshotId ← identityOf (← BaselineArtifacts.field request "snapshot_id")
  let supportId ← identityOf (← BaselineArtifacts.field request "support_id")
  let rawUnits ← ExprCodec.arrayOf (← BaselineArtifacts.field request "units")
  if rawUnits.isEmpty || rawUnits.size > unitMaximum then fail "PRIVATE_UNIT_BOUND"
  let rawTargets ← ExprCodec.arrayOf (← BaselineArtifacts.field request "targets")
  if rawTargets.isEmpty || rawTargets.size > targetMaximum then fail "TARGET_BOUND"
  let mut targets : Array Binding := #[]
  let mut targetNames : Std.HashSet Name := {}
  for raw in rawTargets do
    let binding ← bindingOf raw
    if targetNames.contains binding.name then fail "DUPLICATE_TARGET_NAME"
    targetNames := targetNames.insert binding.name
    targets := targets.push binding
  -- The entire snapshot, including runtime dependencies, is explicit. Missing
  -- keys cannot resolve through an ambient/current-directory/runtime path.
  searchPathRef.set []
  phase "BEFORE_PRIVATE_SNAPSHOT_IMPORT"
  let privateEnv ← importModules imports {} 0
    (plugins := #[]) (leakEnv := false) (loadExts := false) (level := .private)
    (arts := selection.artifacts)
  let privateModules ← checkSnapshotView privateEnv selection imports true
  let source : Export.SourceRecords := {
    environment := privateEnv.toKernelEnv, grouping := #[], count := 0 }
  let basisNames ← Export.compareSourceBasis source inventory
  let privateMatch ← matchPrivate privateEnv rawUnits basisNames
  phase s!"PRIVATE_CORRESPONDENCE_COMPLETE units={privateMatch.units.size} names={privateMatch.nameCount}"
  checkArtifactSizes selection
  phase "BEFORE_PUBLIC_SNAPSHOT_IMPORT"
  let publicEnv ← importModules imports {} 0
    (plugins := #[]) (leakEnv := false) (loadExts := false) (level := .exported)
    (arts := selection.artifacts)
  let publicModules ← checkSnapshotView publicEnv selection imports false
  if !publicEnv.header.isModule then fail "MODERN_PUBLIC_ENVIRONMENT_REQUIRED"
  -- The actual exported-import kernel map is not selected by setExporting.
  -- Bind every present public basis record to its checked original, recording
  -- absences and the greatest closed common subset instead of postulating them.
  let publicBasis ← matchBasisViews privateEnv publicEnv basisNames inventoryRows privateMatch
  phase s!"PUBLIC_BASIS_COMPLETE usable={publicBasis.usableNames.size} rounds={publicBasis.pruningRounds}"
  let publicMatch ← matchPublic publicEnv privateMatch publicBasis targets
  checkArtifactSizes selection
  let publicUnits ← publicRows privateMatch publicMatch
  let result := Json.mkObj [
    ("schema", .str "DMKN_ORDINARY_REFERENCE_BASE_REPORT_V2"),
    ("assurance", .str "CORRESPONDENCE_REQUIRES_CURRENT_PROTECTED_WARRANTS"),
    ("semantic_id", .str semanticId), ("foundation_id", .str foundationId),
    ("context_root", .str contextRoot), ("snapshot_id", .str snapshotId),
    ("support_id", .str supportId), ("targets", .arr (← targets.mapM bindingJson)),
    ("private_unit_ids", .arr (privateMatch.units.map (fun unit => Json.str unit.unitId))),
    ("public_units", .arr publicUnits),
    ("public_basis", .arr publicBasis.rows),
    ("usable_basis_names", .arr (← publicBasis.usableNames.mapM (fun name => ExprCodec.encodeName name))),
    ("basis_scan_nodes", toJson publicBasis.scanNodes),
    ("basis_edges", toJson publicBasis.edges), ("basis_pruning_rounds", toJson publicBasis.pruningRounds),
    ("private_module_names", .arr (← privateModules.mapM (fun name => ExprCodec.encodeName name))),
    ("public_module_names", .arr (← publicModules.mapM (fun name => ExprCodec.encodeName name))),
    ("private_unit_count", toJson privateMatch.units.size),
    ("private_name_count", toJson privateMatch.nameCount),
    ("public_unit_count", toJson publicMatch.visible.size),
    ("public_name_count", toJson publicMatch.nameCount),
    ("unit_array_bytes", toJson privateMatch.unitBytes),
    ("encoded_nodes", toJson privateMatch.encodedNodes),
    ("private_scan_nodes", toJson privateMatch.scanNodes),
    ("public_scan_nodes", toJson publicMatch.scanNodes),
    ("private_edges", toJson privateMatch.edges), ("public_edges", toJson publicMatch.edges),
    ("checked_units", toJson (0 : Nat)), ("added_names", .arr #[])]
  let bytes := result.compress.toUTF8
  if bytes.size > reportMaximum then fail "REPORT_BYTE_BOUND"
  let output ← IO.FS.Handle.mk (BaselineArtifacts.nativePath reportPath) .writeNew
  output.write bytes
  output.flush
  phase s!"CORRESPONDENCE_REPORT_WRITTEN publicUnits={publicMatch.visible.size} bytes={bytes.size}"

end OrdinaryLean.ReferenceBase

def main (args : List String) : IO UInt32 := do
  try
    match args with
    | [inventory, artifactMap, request, report] =>
        OrdinaryLean.ReferenceBase.run
          (← OrdinaryLean.BaselineArtifacts.absolutePath inventory)
          (← OrdinaryLean.BaselineArtifacts.absolutePath artifactMap)
          (← OrdinaryLean.BaselineArtifacts.absolutePath request)
          (← OrdinaryLean.BaselineArtifacts.absolutePath report)
        return 0
    | _ => OrdinaryLean.ReferenceBase.fail "USAGE inventory replay-map request report"
  catch error =>
    let stderr ← IO.getStderr
    stderr.putStrLn (String.ofList (error.toString.toList.take 2048))
    stderr.flush
    return 1
