module

public import BootstrapSupport
public import OriginalDecl
public import CheckedExtension

/- Owner-side inert serialization, never mathematical acceptance. The exact
   source module/artifact map and fixed seed inventory are protected caller
   inputs. A peer cannot supply an Environment or basis JSON as a warrant. -/

public section
open Lean

namespace OrdinaryLean.Export

structure Limits where
  codec : DeclCodec.Limits := {}
  maxSourceRecords : Nat := 262144
  maxGroupRecords : Nat := 65536
  maxBasisNames : Nat := 4096
  maxTargets : Nat := 1024
  maxUnits : Nat := 8192
  maxEdges : Nat := 262144
  maxScanNodes : Nat := 20000000
  maxUnitBytes : Nat := 8388608
  maxOutputBytes : Nat := 67108864
  deriving Inhabited

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"ORDINARY_EXPORT {message}"

/-- Only grouping records need enumeration. All lookups use the original
    imported source environment. No full constant-list copy is required. -/
structure SourceRecords where
  environment : Kernel.Environment
  grouping : Array (Name × ConstantInfo)
  count : Nat

instance : BootstrapProbe.RecordSource SourceRecords where
  findRecord source name := source.environment.find? name
  records source := source.grouping

structure IndexedSource where
  source : SourceRecords
  members : BootstrapProbe.Members

/-- One bounded local-source census per immutable imported environment; reuse
    this index for multiple selected exports. Not a network-wide library scan. -/
def indexSource (environment : Kernel.Environment) (limits : Limits := {})
    : IO IndexedSource := do
  let mut count := 0
  let mut grouping := #[]
  for (name, info) in environment.constants do
    count := count + 1
    if count > limits.maxSourceRecords then fail "SOURCE_RECORD_BOUND"
    if name != info.name then fail "SOURCE_KEY_MISMATCH"
    match info with
    | .inductInfo _ | .ctorInfo _ | .recInfo _ =>
        if grouping.size >= limits.maxGroupRecords then fail "GROUP_RECORD_BOUND"
        grouping := grouping.push (name, info)
    | _ => pure ()
  let source : SourceRecords := { environment, grouping, count }
  let members ← BootstrapProbe.groupMembers source
  return { source, members }

/-- Source correspondence to an EXACT caller-pinned legacy seed inventory.
    Normalized correspondence is not original-binder metadata equality.
    The receiver must separately obtain the actual checked seed environment. -/
def compareSourceBasis (source : SourceRecords) (trustedInventory : Json)
    (limits : Limits := {}) : IO (Array Name) := do
  let rows ← ExprCodec.arrayOf trustedInventory
  if rows.isEmpty || rows.size > limits.maxBasisNames then fail "BASIS_COUNT"
  let mut names := #[]
  let mut seen : Std.HashSet Name := {}
  for raw in rows do
    let row ← ExprCodec.arrayOf raw (some 5)
    let name ← BootstrapProbe.nameOf row[0]!
    if seen.contains name then fail "BASIS_DUPLICATE_NAME"
    seen := seen.insert name
    let actual ← BootstrapProbe.lookup source name
    BootstrapProbe.screen actual
    let height ← if (← ExprCodec.natOf row[1]!) == 1 then do
      let details ← ExprCodec.arrayOf row[4]! (some 3)
      pure <| some (← ExprCodec.u32Of details[1]!)
    else pure none
    if (← BootstrapProbe.inventoryRow actual height) != raw then
      fail s!"BASIS_SOURCE_CORRESPONDENCE {name}"
    names := names.push name
  return names

def orderedNames (names : Array Name) : Array Name :=
  (names.toList.mergeSort (fun left right =>
    BootstrapProbe.bytesLT (BootstrapProbe.nameBytes left)
      (BootstrapProbe.nameBytes right))).toArray

structure Pending where
  keys : Array Name := #[]
  seen : Std.HashSet Name := {}

def schedule (source : SourceRecords) (basis : Std.HashSet Name)
    (pending : Pending) (name : Name) (limits : Limits) : IO Pending := do
  if basis.contains name then return pending
  CheckedExtension.requireName name
  let key ← BootstrapProbe.owner source name
  if basis.contains key then fail "BASIS_GROUP_STRADDLE"
  if pending.seen.contains key then return pending
  if pending.keys.size >= limits.maxUnits then fail "SELECTED_UNIT_BOUND"
  return { keys := pending.keys.push key, seen := pending.seen.insert key }

structure Exported where
  units : Array Json
  targets : Array Name
  basisNames : Array Name
  sourceRecords : Nat
  selectedUnits : Nat
  dependencyEdges : Nat
  scanNodes : Nat
  unitBytes : Nat
  /-- Selected boundary references, including required literal-stage support.
      This is a bundle lookup map, not the exact per-unit evidence imports. -/
  boundaryReferences : Array Name := #[]

/-- Shared closure scheduler. The boundary must already be established by the
    caller: fixed checked-basis correspondence, or authenticated owner rebinding.
    Names alone never constitute a warrant. A source with empty grouping avoids
    a census until a genuinely new inductive group requires its complete records.
    Existing proof bodies at the boundary are neither loaded nor serialized. -/
def selectedFromBoundary (indexed : IndexedSource) (basisNames : Array Name)
    (targets : Array Name) (limits : Limits := {}) : IO Exported := do
  if targets.isEmpty || targets.size > limits.maxTargets then fail "TARGET_BOUND"
  let mut active := indexed
  let mut basis : Std.HashSet Name := {}
  for name in basisNames do basis := basis.insert name
  let mut boundaryRefs : Std.HashSet Name := {}
  let mut pending : Pending := {}
  for name in targets do
    if basis.contains name then boundaryRefs := boundaryRefs.insert name
    pending ← schedule active.source basis pending name limits
  let mut cursor := 0
  let mut units : Std.HashMap Name BootstrapProbe.UnitInfo := {}
  let mut dependencies : Std.HashMap Name (Array Name) := {}
  let mut edgeCount := 0
  let mut scanNodes := 0
  while cursor < pending.keys.size do
    let key := pending.keys[cursor]!
    cursor := cursor + 1
    if let some (.axiomInfo _) := active.source.environment.find? key then
      let originalName ← ExprCodec.encodeName key limits.codec.expr
      fail s!"MISSING_WARRANT_OR_FULL_DECLARATION original_name={originalName.compress} name={key}"
    if !active.members.contains key then
      if let some (.inductInfo _) := active.source.environment.find? key then
        -- Generated recursors, including nested groups, require the actual
        -- complete kernel census. Ordinary definitions/theorems never pay it.
        active ← indexSource active.source.environment limits
    let unit ← BootstrapProbe.makeUnit active.source active.members key
    discard <| CheckedExtension.allowedDeclaration unit.decl
    if unit.emitted.isEmpty || unit.emitted.size > limits.codec.maxInventory then
      fail "UNIT_INVENTORY_BOUND"
    let mut emitted : Std.HashSet Name := {}
    for name in unit.emitted do
      if basis.contains name then fail "BASIS_GROUP_STRADDLE"
      if emitted.contains name then fail "DUPLICATE_GROUP_OUTPUT"
      emitted := emitted.insert name
    scanNodes := scanNodes + unit.scanNodes
    if scanNodes > limits.maxScanNodes then fail "SELECTED_SCAN_BOUND"
    for name in unit.refs do
      if basis.contains name then
        boundaryRefs := boundaryRefs.insert name
      else if basis.contains (← BootstrapProbe.owner active.source name) then
        -- A group owner without its referenced generated member is not a
        -- complete stopping boundary. Never silently treat it as an import.
        fail "BOUNDARY_GROUP_STRADDLE"
    let mut deps : Std.HashSet Name := {}
    for edge in unit.edges do
      if !basis.contains edge.dep then deps := deps.insert edge.dep
    let ordered := orderedNames deps.toArray
    edgeCount := edgeCount + ordered.size
    if edgeCount > limits.maxEdges then fail "SELECTED_EDGE_BOUND"
    for dep in ordered do
      pending ← schedule active.source basis pending dep limits
    dependencies := dependencies.insert key ordered
    units := units.insert key unit
  -- Kahn scheduling is linear in selected units/edges after deterministic
  -- per-unit dependency ordering. Do not repeatedly scan the whole remainder.
  let mut remaining : Std.HashMap Name Nat := {}
  let mut dependents : Std.HashMap Name (Array Name) := {}
  let mut ready := #[]
  for key in pending.keys do
    let some deps := dependencies[key]? | fail "INTERNAL_DEPENDENCIES"
    remaining := remaining.insert key deps.size
    if deps.isEmpty then ready := ready.push key
    for dep in deps do
      if !units.contains dep then fail "UNCLOSED_SELECTED_DEPENDENCY"
      dependents := dependents.insert dep ((dependents[dep]?.getD #[]).push key)
  let mut ordered := #[]
  cursor := 0
  while cursor < ready.size do
    let key := ready[cursor]!
    cursor := cursor + 1
    ordered := ordered.push key
    for child in dependents[key]?.getD #[] do
      let some count := remaining[child]? | fail "INTERNAL_REMAINING"
      if count == 0 then fail "INTERNAL_EDGE_ACCOUNTING"
      let next := count - 1
      remaining := remaining.insert child next
      if next == 0 then ready := ready.push child
  if ordered.size != pending.keys.size then fail "CYCLIC_SELECTED_CLOSURE"
  let mut encoded := #[]
  let mut totalBytes := 0
  for key in ordered do
    let some unit := units[key]? | fail "INTERNAL_UNIT"
    let mut inventory := #[]
    for name in orderedNames unit.emitted do
      inventory := inventory.push (← BootstrapProbe.lookup active.source name)
    let packet ← DeclCodec.encodeUnit unit.decl inventory limits.codec
    let size := packet.compress.utf8ByteSize
    if size > limits.maxUnitBytes then fail "UNIT_BYTE_BOUND"
    totalBytes := totalBytes + size
    if totalBytes > limits.maxOutputBytes then fail "OUTPUT_BYTE_BOUND"
    encoded := encoded.push packet
  return {
    units := encoded
    targets := targets
    basisNames := basisNames
    sourceRecords := active.source.count
    selectedUnits := ordered.size
    dependencyEdges := edgeCount
    scanNodes := scanNodes
    unitBytes := totalBytes
    boundaryReferences := orderedNames boundaryRefs.toArray
  }

/-- Original fixed-basis entry point. The same exact source-basis comparison
    precedes the shared scheduler; historical producer artifacts are unchanged.
    The result remains inert claims, not a receiver acceptance event. -/
def selected (indexed : IndexedSource) (trustedInventory : Json)
    (targets : Array Name) (limits : Limits := {}) : IO Exported := do
  if targets.isEmpty || targets.size > limits.maxTargets then fail "TARGET_BOUND"
  let basisNames ← compareSourceBasis indexed.source trustedInventory limits
  selectedFromBoundary indexed basisNames targets limits

end OrdinaryLean.Export
