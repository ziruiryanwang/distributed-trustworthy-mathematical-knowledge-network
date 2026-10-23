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
