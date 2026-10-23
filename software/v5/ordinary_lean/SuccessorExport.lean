module

public import OrdinaryExport
public import OwnerRebind

/- Inert successor serialization over a controller-authenticated correspondence.
   This does not authenticate a boundary or grant any mathematical authority.
   The receiver independently resolves every exact imported symbol identity and
   checks the complete new declaration units in its actual accepted context. -/

public section
open Lean

namespace OrdinaryLean.SuccessorExport

structure Limits where
  closure : Export.Limits := {}
  maxBoundaryNames : Nat := 65536
  maxBoundaryLookups : Nat := 262144
  maxBundleBytes : Nat := 67108864
  deriving Inhabited

structure Exported where
  units : Array Json
  targets : Array Name
  boundaryImports : Array OwnerRebind.BoundName
  sourceRecords : Nat
  selectedUnits : Nat
  dependencyEdges : Nat
  scanNodes : Nat
  unitBytes : Nat

structure CandidateExported where
  exported : Exported
  /-- Reached imported owner names without a supplied accepted-ID claim. These
      require exact protected receiver resolution before any native checking. -/
  unresolvedImports : Array Name

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"ORDINARY_SUCCESSOR_EXPORT {message}"

/-- The caller must provide the exact successful rebind correspondence for this
    owner environment and its later ordinary declarations. The array is NOT an
    unforgeable token. In particular, accepting caller-created axiom/name rows
    here would not make them warranted; final receiver admission is mandatory.

    Direct point lookups suffice for ordinary missing declarations. A new
    inductive group triggers the old bounded kernel census once, solely to obtain
    its complete actual generated records. The default accepted group boundary
    is complete because OwnerRebind matched it against the accepted atomic unit.
    A partially supplied boundary is refused if reached. -/
def selectedAbove (owner : Environment) (boundary : Array OwnerRebind.BoundName)
    (targets : Array Name) (limits : Limits := {}) : IO Exported := do
  if owner.asyncPrefix?.isSome then fail "TOP_LEVEL_OWNER_REQUIRED"
  if boundary.isEmpty || boundary.size > limits.maxBoundaryNames then
    fail "BOUNDARY_COUNT"
  if targets.isEmpty || targets.size > limits.closure.maxTargets then
    fail "TARGET_COUNT"
  let kernel := owner.toKernelEnv
  let mut names : Array Name := #[]
  let mut symbols : Std.HashMap Name String := {}
  for binding in boundary do
    CheckedExtension.requireName binding.name
    discard <| OwnerRebind.identityOf (Json.str binding.symbolId)
    if symbols.contains binding.name then fail "DUPLICATE_BOUNDARY_NAME"
    let some actual := kernel.find? binding.name | fail "BOUNDARY_NAME_ABSENT"
    OwnerRebind.requireSafe actual binding.name
    symbols := symbols.insert binding.name binding.symbolId
    names := names.push binding.name
  let mut targetSet : Std.HashSet Name := {}
  for name in targets do
    CheckedExtension.requireName name
    if targetSet.contains name then fail "DUPLICATE_TARGET"
    targetSet := targetSet.insert name
  -- No full source census for ordinary successor proofs/definitions. A lazy
  -- census is performed by the shared scheduler only for new inductive groups.
  let indexed : Export.IndexedSource := {
    source := { environment := kernel, grouping := #[], count := 0 }
    members := {} }
  let exported ← Export.selectedFromBoundary indexed names targets limits.closure
  let mut imports : Array OwnerRebind.BoundName := #[]
  for name in exported.boundaryReferences do
    let some symbolId := symbols[name]? | fail "UNBOUND_STOPPING_REFERENCE"
    imports := imports.push { name, symbolId }
  return {
    units := exported.units
    targets := exported.targets
    boundaryImports := imports
    sourceRecords := exported.sourceRecords
    selectedUnits := exported.selectedUnits
    dependencyEdges := exported.dependencyEdges
    scanNodes := exported.scanNodes
    unitBytes := exported.unitBytes }

/-- Candidate construction entry point, deliberately distinct from the exact
    correspondence API above. Labels designate the intended RECEIVER meaning;
    they need not match local bodies/types and unused labels need not be present.
    Only reached labels are checked locally. A current-module name can stop at
    a label only if this construction introduced it; another local declaration
    with the same name must not silently replace a new unit with an old import.

    The caller authenticates the finite label map and construction bookkeeping.
    Neither is an unforgeable token. Final checking of every complete new unit
    with exact accepted receiver imports remains the sole admission authority. -/
def selectedInterpreted (owner : Environment)
    (interpretationLabels : Array OwnerRebind.BoundName) (introducedNames : Array Name)
    (targets : Array Name) (limits : Limits := {}) : IO Exported := do
  if owner.asyncPrefix?.isSome then fail "TOP_LEVEL_OWNER_REQUIRED"
  if interpretationLabels.isEmpty || interpretationLabels.size > limits.maxBoundaryNames ||
      introducedNames.size > limits.maxBoundaryNames then fail "BOUNDARY_COUNT"
  if targets.isEmpty || targets.size > limits.closure.maxTargets then fail "TARGET_COUNT"
  let kernel := owner.toKernelEnv
  let mut names : Array Name := #[]
  let mut symbols : Std.HashMap Name String := {}
  for binding in interpretationLabels do
    CheckedExtension.requireName binding.name
    discard <| OwnerRebind.identityOf (Json.str binding.symbolId)
    if symbols.contains binding.name then fail "DUPLICATE_BOUNDARY_NAME"
    symbols := symbols.insert binding.name binding.symbolId
    names := names.push binding.name
  let mut introduced : Std.HashSet Name := {}
  for name in introducedNames do
    CheckedExtension.requireName name
    if introduced.contains name then fail "DUPLICATE_INTRODUCED_NAME"
    if !symbols.contains name then fail "INTRODUCED_NAME_WITHOUT_INTERPRETATION"
    introduced := introduced.insert name
  let mut targetSet : Std.HashSet Name := {}
  for name in targets do
    CheckedExtension.requireName name
    if symbols.contains name then fail "TARGET_ALREADY_IN_BOUNDARY"
    if targetSet.contains name then fail "DUPLICATE_TARGET"
    targetSet := targetSet.insert name
  let indexed : Export.IndexedSource := {
    source := { environment := kernel, grouping := #[], count := 0 }
    members := {} }
  let exported ← Export.selectedFromBoundary indexed names targets limits.closure
  let mut imports : Array OwnerRebind.BoundName := #[]
  for name in exported.boundaryReferences do
    let some symbolId := symbols[name]? | fail "UNBOUND_STOPPING_REFERENCE"
    let some actual := kernel.find? name | fail "REACHED_BOUNDARY_NAME_ABSENT"
    OwnerRebind.requireSafe actual name
    if !owner.isImportedConst name && !introduced.contains name then
      fail s!"NEW_LOCAL_BOUNDARY_COLLISION name={name}"
    imports := imports.push { name, symbolId }
  return {
    units := exported.units
    targets := exported.targets
    boundaryImports := imports
    sourceRecords := exported.sourceRecords
    selectedUnits := exported.selectedUnits
    dependencyEdges := exported.dependencyEdges
    scanNodes := exported.scanNodes
    unitBytes := exported.unitBytes }

/-- Best-effort candidate export. In addition to prepared interpretation labels,
    safe constants imported by the local owner stop traversal dynamically. Their
    original names are emitted as unresolved requests, NOT invented symbol IDs.
    The receiver must resolve the entire missing map in its actual accepted
    parent before constructing checking envelopes or launching native work.

    Existing local new declarations do not stop merely because they have names:
    they are exported in full, or refused on a prepared-label collision. -/
def selectedDeferred (owner : Environment)
    (interpretationLabels : Array OwnerRebind.BoundName) (introducedNames : Array Name)
    (targets : Array Name) (limits : Limits := {}) : IO CandidateExported := do
  if owner.asyncPrefix?.isSome then fail "TOP_LEVEL_OWNER_REQUIRED"
  if interpretationLabels.isEmpty || interpretationLabels.size > limits.maxBoundaryNames ||
      introducedNames.size > limits.maxBoundaryNames then fail "BOUNDARY_COUNT"
  if targets.isEmpty || targets.size > limits.closure.maxTargets then fail "TARGET_COUNT"
  let kernel := owner.toKernelEnv
  let mut names : Array Name := #[]
  let mut symbols : Std.HashMap Name String := {}
  for binding in interpretationLabels do
    CheckedExtension.requireName binding.name
    discard <| OwnerRebind.identityOf (Json.str binding.symbolId)
    if symbols.contains binding.name then fail "DUPLICATE_BOUNDARY_NAME"
    symbols := symbols.insert binding.name binding.symbolId
    names := names.push binding.name
  let mut introduced : Std.HashSet Name := {}
  for name in introducedNames do
    CheckedExtension.requireName name
    if introduced.contains name then fail "DUPLICATE_INTRODUCED_NAME"
    if !symbols.contains name then fail "INTRODUCED_NAME_WITHOUT_INTERPRETATION"
    introduced := introduced.insert name
  let mut targetSet : Std.HashSet Name := {}
  for name in targets do
    CheckedExtension.requireName name
    if symbols.contains name then fail "TARGET_ALREADY_IN_BOUNDARY"
    if owner.isImportedConst name then fail "CURRENT_MODULE_TARGET_REQUIRED"
    if targetSet.contains name then fail "DUPLICATE_TARGET"
    targetSet := targetSet.insert name
  let indexed : Export.IndexedSource := {
    source := { environment := kernel, grouping := #[], count := 0 }
    members := {} }
  let policy : Export.DynamicBoundary := {
    stop := fun name => do
      if !owner.isImportedConst name then return false
      let some actual := kernel.find? name | fail "IMPORTED_RECORD_ABSENT"
      OwnerRebind.requireSafe actual name
      return true
    maxLookups := limits.maxBoundaryLookups
    maxNames := limits.maxBoundaryNames
  }
  let selected ← Export.selectedFromBoundary indexed names targets limits.closure (some policy)
  let mut imports : Array OwnerRebind.BoundName := #[]
  let mut unresolved : Array Name := #[]
  for name in selected.boundaryReferences do
    let some actual := kernel.find? name | fail "REACHED_BOUNDARY_NAME_ABSENT"
    OwnerRebind.requireSafe actual name
    if !owner.isImportedConst name && !introduced.contains name then
      fail s!"NEW_LOCAL_BOUNDARY_COLLISION name={name}"
    if let some symbolId := symbols[name]? then
      imports := imports.push { name, symbolId }
    else
      if !owner.isImportedConst name then fail "UNRESOLVED_LOCAL_NAME"
      unresolved := unresolved.push name
  let exported : Exported := {
    units := selected.units
    targets := selected.targets
    boundaryImports := imports
    sourceRecords := selected.sourceRecords
    selectedUnits := selected.selectedUnits
    dependencyEdges := selected.dependencyEdges
    scanNodes := selected.scanNodes
    unitBytes := selected.unitBytes }
  return { exported := exported, unresolvedImports := unresolved }

/-- A distinct schema is mandatory because unresolved names are not imported
    warrants. Complete receiver resolution precedes all native work; the same
    complete new-unit checking and event-bound commit remain necessary. -/
def candidateBundleBytes (profileId contextId basisId : String) (candidate : CandidateExported)
    (limits : Limits := {}) : IO ByteArray := do
  for identity in [profileId, contextId, basisId] do
    discard <| OwnerRebind.identityOf (Json.str identity)
  let exported := candidate.exported
  if exported.boundaryImports.size + candidate.unresolvedImports.size > limits.maxBoundaryNames then
    fail "BOUNDARY_COUNT"
  let targets ← exported.targets.mapM (fun name => ExprCodec.encodeName name)
  let imports ← exported.boundaryImports.mapM (fun binding => do
    pure <| Json.arr #[← ExprCodec.encodeName binding.name, Json.str binding.symbolId])
  let unresolved ← candidate.unresolvedImports.mapM (fun name => ExprCodec.encodeName name)
  let statistics := Json.mkObj [
    ("source_records_enumerated", toJson exported.sourceRecords),
    ("selected_units", toJson exported.selectedUnits),
    ("dependency_edges", toJson exported.dependencyEdges),
    ("scan_nodes", toJson exported.scanNodes),
    ("unit_json_bytes", toJson exported.unitBytes),
    ("boundary_imports", toJson exported.boundaryImports.size),
    ("unresolved_imports", toJson candidate.unresolvedImports.size)]
  let packet := Json.mkObj [
    ("schema", Json.str "DMKN_ORDINARY_CANDIDATE_BUNDLE_V1"),
    ("assurance", Json.str "INERT_OWNER_EXPORT_NOT_MATHEMATICAL_ACCEPTANCE"),
    ("profile_id", Json.str profileId),
    ("context_id", Json.str contextId),
    ("basis_id", Json.str basisId),
    ("targets", Json.arr targets),
    ("boundary_imports", Json.arr imports),
    ("unresolved_imports", Json.arr unresolved),
    ("units", Json.arr exported.units),
    ("stats", statistics)]
  let bytes := packet.compress.toUTF8
  if bytes.size > limits.maxBundleBytes then fail "BUNDLE_BYTE_BOUND"
  return bytes

/-- Encode an inert bundle. `boundary_imports` is a selected lookup map, including
    literal-stage support if needed. The controller must derive each envelope's
    exact imports from ordinary_evidence.inspect_unit, resolve them in this map
    or earlier new units, and obtain actual receiver checking. Profile/context
    labels are caller-authenticated, not self-proving statements. -/
def bundleBytes (profileId contextId basisId : String) (exported : Exported)
    (limits : Limits := {}) : IO ByteArray := do
  for identity in [profileId, contextId, basisId] do
    discard <| OwnerRebind.identityOf (Json.str identity)
  let targets ← exported.targets.mapM (fun name => ExprCodec.encodeName name)
  let imports ← exported.boundaryImports.mapM (fun binding => do
    pure <| Json.arr #[← ExprCodec.encodeName binding.name, Json.str binding.symbolId])
  let statistics := Json.mkObj [
    ("source_records_enumerated", toJson exported.sourceRecords),
    ("selected_units", toJson exported.selectedUnits),
    ("dependency_edges", toJson exported.dependencyEdges),
    ("scan_nodes", toJson exported.scanNodes),
    ("unit_json_bytes", toJson exported.unitBytes),
    ("boundary_imports", toJson exported.boundaryImports.size)]
  let packet := Json.mkObj [
    ("schema", Json.str "DMKN_ORDINARY_SUCCESSOR_BUNDLE_V1"),
    ("assurance", Json.str "INERT_OWNER_EXPORT_NOT_MATHEMATICAL_ACCEPTANCE"),
    ("profile_id", Json.str profileId),
    ("context_id", Json.str contextId),
    ("basis_id", Json.str basisId),
    ("targets", Json.arr targets),
    ("boundary_imports", Json.arr imports),
    ("units", Json.arr exported.units),
    ("stats", statistics)]
  let bytes := packet.compress.toUTF8
  if bytes.size > limits.maxBundleBytes then fail "BUNDLE_BYTE_BOUND"
  return bytes

end OrdinaryLean.SuccessorExport
