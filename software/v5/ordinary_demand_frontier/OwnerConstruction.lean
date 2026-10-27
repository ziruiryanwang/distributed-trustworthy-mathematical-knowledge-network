module

public import OwnerRebind

/- Best-effort local candidate construction, NOT receiver acceptance or semantic
   correspondence. The controller authenticates Prepared against an accepted
   receiver context. Existing owner records stop demand traversal. Only missing
   accepted theorem TYPES become safe scratch assumptions; these assumptions
   never become receiver evidence. Complete new proofs are checked separately
   in the actual accepted receiver context. No peer code or binary is loaded. -/

public section
open Lean

namespace OrdinaryLean.OwnerConstruction

structure Constructed where
  environment : Environment
  interpretationLabels : Array OwnerRebind.BoundName
  targetNames : Array Name
  introducedNames : Array Name
  introducedSignatures : Array Name
  checkedUnits : Nat
  scanNodes : Nat
  encodedNodes : Nat
  payloadBytes : Nat

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"ORDINARY_OWNER_CONSTRUCTION {message}"

private structure Group where
  rows : Array OwnerRebind.Row
  unit? : Option Json
  deriving Inhabited

private structure Index where
  labels : Array OwnerRebind.BoundName
  names : Std.HashSet Name
  basis : Std.HashSet Name
  frontier : Std.HashSet Name
  groups : Array Group
  groupOf : Std.HashMap Name Nat
  targets : Array Name
  encodedNodes : Nat
  payloadBytes : Nat

/-- Bounded initial adapter: index the authenticated prepared packet once, not
    the owner environment or the global library. Unneeded proof DAGs are only
    shape/count-preflighted; they are not decoded, traversed or checked. -/
private def makeIndex (prepared : OwnerRebind.Prepared) (limits : OwnerRebind.Limits)
    (frontierLabels : Array Json)
    : IO Index := do
  for id in [prepared.profileId, prepared.contextId, prepared.basisId] do
    discard <| OwnerRebind.identityOf (Json.str id)
  if prepared.basisRows.isEmpty || prepared.basisRows.size > limits.maxBasisRows ||
      prepared.groupCount > limits.maxGroups || prepared.targets.isEmpty ||
      prepared.targets.size > limits.maxTargets then fail "PREPARED_COUNT_BOUND"
  let header := Json.arr #[Json.str prepared.profileId, Json.str prepared.contextId,
    Json.str prepared.basisId, Json.arr prepared.basisRows, Json.arr prepared.targets,
    toJson prepared.groupCount]
  let mut bytes ← OwnerRebind.chargeBytes 0 header limits.maxPayloadBytes
  -- The portable wrapper separately charges the complete raw header, including
  -- its root. Keep the old internal count identical when no labels are supplied.
  if !frontierLabels.isEmpty then
    bytes ← OwnerRebind.chargeBytes bytes (Json.arr frontierLabels) limits.maxPayloadBytes
  let mut nodes := 0
  let mut labels : Array OwnerRebind.BoundName := #[]
  let mut names : Std.HashSet Name := {}
  let mut basis : Std.HashSet Name := {}
  let mut frontier : Std.HashSet Name := {}
  let mut symbols : Std.HashMap Name String := {}
  let mut groups : Array Group := #[]
  let mut groupOf : Std.HashMap Name Nat := {}
  for raw in prepared.basisRows do
    let entry ← ExprCodec.arrayOf raw (some 2)
    let symbolId ← OwnerRebind.identityOf entry[0]!
    let row ← ExprCodec.arrayOf entry[1]! (some 5)
    let name ← BootstrapProbe.nameOf row[0]!
    CheckedExtension.requireName name
    if names.contains name then fail "DUPLICATE_BASIS_NAME"
    if labels.size >= limits.maxRows then fail "AGGREGATE_ROW_BOUND"
    nodes ← OwnerRebind.addEncoded nodes (← OwnerRebind.basisNodes entry[1]! limits) limits
    names := names.insert name
    basis := basis.insert name
    symbols := symbols.insert name symbolId
    labels := labels.push { name, symbolId }
  let mut previousFrontierKey : Option String := none
  for raw in frontierLabels do
    if labels.size >= limits.maxRows then fail "AGGREGATE_ROW_BOUND"
    let binding ← OwnerRebind.boundOf raw limits
    -- Structured names encode entirely as ASCII arrays, integers and $bytes.
    -- This canonical JSON ordering therefore equals the controller's byte order.
    let key := (← ExprCodec.encodeName binding.name limits.checker.codec.expr).compress
    if let some previous := previousFrontierKey then
      if compare previous key != .lt then fail "FRONTIER_LABEL_ORDER"
    previousFrontierKey := some key
    if names.contains binding.name then fail "DUPLICATE_OR_REBOUND_FRONTIER_NAME"
    names := names.insert binding.name
    frontier := frontier.insert binding.name
    symbols := symbols.insert binding.name binding.symbolId
    labels := labels.push binding
  for index in [:prepared.groupCount] do
    let packet ← prepared.readGroup index
    let groupBytes := packet.compress.utf8ByteSize
    if groupBytes > limits.maxGroupBytes || bytes + groupBytes > limits.maxPayloadBytes then
      fail "AGGREGATE_PAYLOAD_BYTE_BOUND"
    bytes := bytes + groupBytes
    let fields ← ExprCodec.arrayOf packet (some 3)
    if (← ExprCodec.jsonResult fields[0]!.getStr?) != OwnerRebind.groupFormat then
      fail "GROUP_FORMAT"
    let rawRows ← ExprCodec.arrayOf fields[1]!
    if rawRows.isEmpty || labels.size + rawRows.size > limits.maxRows then
      fail "AGGREGATE_ROW_BOUND"
    let optionalUnit ← ExprCodec.arrayOf fields[2]!
    if optionalUnit.size > 1 then fail "OPTIONAL_UNIT_SHAPE"
    let mut rows : Array OwnerRebind.Row := #[]
    let mut groupNames : Array Name := #[]
    for rawRow in rawRows do
      let row ← OwnerRebind.rowOf rawRow limits
      let name := row.binding.name
      if names.contains name then fail "DUPLICATE_OR_REBOUND_NAME"
      nodes ← OwnerRebind.addEncoded nodes row.encodedNodes limits
      names := names.insert name
      symbols := symbols.insert name row.binding.symbolId
      labels := labels.push row.binding
      groupOf := groupOf.insert name index
      rows := rows.push row
      groupNames := groupNames.push name
    if rows.any (fun row => row.mode == 0) && rows.size != 1 then
      fail "NONATOMIC_THEOREM_GROUP"
    let mut unit? : Option Json := none
    if optionalUnit.size == 1 then
      let unitFields ← ExprCodec.arrayOf optionalUnit[0]! (some 3)
      if (← ExprCodec.jsonResult unitFields[0]!.getStr?) != DeclCodec.unitFormat then
        fail "UNIT_FORMAT"
      let expected ← ExprCodec.arrayOf unitFields[2]!
      if (← DeclCodec.expectedNames expected limits.checker.codec) != groupNames then
        fail "GROUP_UNIT_CENSUS_MISMATCH"
      nodes ← OwnerRebind.addEncoded nodes
        (← DeclCodec.descriptorNodes unitFields[1]! limits.checker.codec) limits
      for raw in expected do
        nodes ← OwnerRebind.addEncoded nodes
          (← DeclCodec.inventoryNodes raw limits.checker.codec) limits
      unit? := some optionalUnit[0]!
    groups := groups.push { rows, unit? }
  let mut targets : Array Name := #[]
  let mut targetSet : Std.HashSet Name := {}
  for raw in prepared.targets do
    let target ← OwnerRebind.boundOf raw limits
    if targetSet.contains target.name then fail "DUPLICATE_TARGET"
    let some id := symbols[target.name]? | fail "UNBOUND_TARGET"
    if id != target.symbolId then fail "TARGET_SYMBOL_MISMATCH"
    targetSet := targetSet.insert target.name
    targets := targets.push target.name
  return {
    labels := labels
    names := names
    basis := basis
    frontier := frontier
    groups := groups
    groupOf := groupOf
    targets := targets
    encodedNodes := nodes
    payloadBytes := bytes }

private structure Work where
  environment : Environment
  active : Std.HashSet Nat := {}
  introduced : Array Name := #[]
  signatures : Array Name := #[]
  checkedUnits : Nat := 0
  scans : Nat := 0

private def collectExpr (expr : Expr) (used : Nat) (limits : OwnerRebind.Limits)
    : IO (Std.HashSet Name × Nat) := do
  if used > limits.maxScanNodes then fail "AGGREGATE_SCAN_BOUND"
  let (refs, count) ← CheckedExtension.references expr (limits.maxScanNodes - used)
  return (refs, used + count)

private def collectDecl (decl : Declaration) (used : Nat) (limits : OwnerRebind.Limits)
    : IO (Std.HashSet Name × Nat) :=
  decl.foldExprM (fun (state : Std.HashSet Name × Nat) expr => do
    let (more, count) ← collectExpr expr state.2 limits
    let mut refs := state.1
    for name in more do refs := refs.insert name
    return (refs, count)) ({}, used)

private def requireCapacity (work : Work) (names : Nat) (limits : OwnerRebind.Limits)
    : IO Unit := do
  if work.checkedUnits + work.signatures.size >= limits.maxCheckedUnits ||
      work.introduced.size + names > limits.maxAddedNames then
    fail "AGGREGATE_ADDITION_BOUND"

/-- Recursion is guarded by finite depth, finite indexed groups and active-group
    cycle detection. No existing owner body is inspected. The environment remains
    local; even a successful dependency prefix cannot escape a later failure. -/
private partial def demand (index : Index) (limits : OwnerRebind.Limits)
    (work : Work) (name : Name) (depth : Nat) : IO Work := do
  CheckedExtension.requireName name
  if index.frontier.contains name then
    let some actual := work.environment.toKernelEnv.find? name
      | fail s!"MISSING_DEMANDED_FRONTIER_KERNEL {name}"
    OwnerRebind.requireSafe actual name
    let some visible := work.environment.find? name (skipRealize := true)
      | fail s!"MISSING_DEMANDED_FRONTIER_FRONTEND {name}"
    OwnerRebind.requireSafe visible name
    -- A cut is only an optimistic authoring boundary. Never expose a hidden
    -- record, reconstruct ancestors, or infer agreement with receiver semantics.
    return work
  if let some actual := work.environment.toKernelEnv.find? name then
    OwnerRebind.requireSafe actual name
    return work
  if depth >= limits.maxRows || depth >= limits.checker.maxRecDepth.toNat then
    fail "DEMAND_DEPTH_BOUND"
  if index.basis.contains name then fail s!"MISSING_DEMANDED_FIXED_BASIS {name}"
  let some groupIndex := index.groupOf[name]? | fail s!"MISSING_CONSTRUCTION_DATA {name}"
  if work.active.contains groupIndex then fail s!"CONSTRUCTION_DEPENDENCY_CYCLE {name}"
  let group := index.groups[groupIndex]!
  -- This branch is reached only for a missing name. A partial existing group
  -- cannot be overwritten or silently spliced into the accepted group.
  for row in group.rows do
    if (work.environment.toKernelEnv.find? row.binding.name).isSome then
      fail "PARTIAL_EXISTING_GROUP"
  let mut current := { work with active := work.active.insert groupIndex }
  if group.rows.size == 1 && group.rows[0]!.mode == 0 then
    let row := group.rows[0]!
    let payload ← ExprCodec.arrayOf row.payload (some 2)
    let params ← DeclCodec.paramsOf payload[0]! limits.checker.codec
    let allowed := index.names.erase row.binding.name
    let type ← ExprCodec.decode params allowed payload[1]! limits.checker.codec.expr
    if (← ExprCodec.encode params type limits.checker.codec.expr) != payload[1]! then
      fail "NONCANONICAL_SIGNATURE_TYPE"
    let (refs, scans) ← collectExpr type current.scans limits
    current := { current with scans }
    for dependency in refs do
      current ← demand index limits current dependency (depth + 1)
    requireCapacity current 1 limits
    -- Checking a declaration of assumption establishes well-formedness ONLY.
    -- The exact accepted theorem ID supplies receiver interpretation at export.
    let decl := Declaration.axiomDecl {
      name := row.binding.name, levelParams := params, type, isUnsafe := false }
    let candidate ← match current.environment.addDeclCore limits.checker.maxHeartbeats
        limits.checker.maxRecDepth decl none (doCheck := true) with
      | .ok env => pure env
      | .error _ => fail "SIGNATURE_KERNEL_REJECTED_OR_RESOURCE_LIMIT"
    let some actual := candidate.toKernelEnv.find? row.binding.name
      | fail "SIGNATURE_RECORD_ABSENT"
    OwnerRebind.requireSafe actual row.binding.name
    if !actual.isAxiom || (← OwnerRebind.theoremPayload actual limits) != row.payload then
      fail "SIGNATURE_INTERFACE_MISMATCH"
    let candidate ← OwnerRebind.exposeAdded candidate #[actual]
    return { current with
      environment := candidate
      active := current.active.erase groupIndex
      introduced := current.introduced.push row.binding.name
      signatures := current.signatures.push row.binding.name }
  let some rawUnit := group.unit? | fail "MISSING_CHECKED_CONSTRUCTION_UNIT"
  let mut allowed := index.names
  for row in group.rows do allowed := allowed.erase row.binding.name
  let unit ← DeclCodec.decodeUnit allowed rawUnit limits.checker.codec
  let selfTypes ← CheckedExtension.allowedDeclaration unit.decl
  -- Accepted theorem proofs are never replayed by this helper. Their groups
  -- must use the explicitly classified signature path above.
  match unit.decl with
  | .thmDecl _ => fail "THEOREM_REQUIRES_SIGNATURE_GROUP"
  | _ => pure ()
  let beforeScan := current.scans
  let (refs, scans) ← collectDecl unit.decl current.scans limits
  let checkScans := scans - beforeScan
  current := { current with scans }
  for dependency in refs do
    if !selfTypes.contains dependency then
      current ← demand index limits current dependency (depth + 1)
  requireCapacity current group.rows.size limits
  if checkScans > limits.checker.maxScanNodes ||
      current.scans + checkScans > limits.maxScanNodes then
    fail "AGGREGATE_CHECK_SCAN_BOUND"
  let checked ← CheckedExtension.checkBatch current.environment #[unit] limits.checker
  let candidate ← OwnerRebind.exposeAdded checked.environment checked.added
  for row in group.rows do
    let some actual := candidate.toKernelEnv.find? row.binding.name
      | fail "CHECKED_RECORD_ABSENT"
    if row.mode != 1 ||
        (← DeclCodec.inventoryRow actual limits.checker.codec) != row.payload then
      fail "CHECKED_CONSTRUCTION_ROW_MISMATCH"
  let mut introduced := current.introduced
  for actual in checked.added do introduced := introduced.push actual.name
  return { current with
    environment := candidate
    active := current.active.erase groupIndex
    introduced := introduced
    checkedUnits := current.checkedUnits + checked.unitsChecked
    scans := current.scans + checkScans }

/-- Controller-authenticated labels select a receiver interpretation, not a
    guarantee that local records share its semantics. The caller must keep
    scratch state distinct from accepted state and export complete new proofs
    through an independently checking receiver. No command state is mutated. -/
def constructPrepared (owner : Environment) (prepared : OwnerRebind.Prepared)
    (limits : OwnerRebind.Limits := {}) (frontierLabels : Array Json := #[])
    : IO Constructed := do
  if owner.asyncPrefix?.isSome then fail "TOP_LEVEL_OWNER_REQUIRED"
  if !owner.toKernelEnv.quotInit then fail "OWNER_QUOTIENT_PROFILE_REQUIRED"
  if limits.checker.maxHeartbeats == 0 || limits.checker.maxRecDepth == 0 then
    fail "FINITE_KERNEL_LIMITS"
  let index ← makeIndex prepared limits frontierLabels
  let mut work : Work := { environment := owner }
  for target in index.targets do
    work ← demand index limits work target 0
  for target in index.targets do
    let some visible := work.environment.find? target (skipRealize := true)
      | fail s!"TARGET_FRONTEND_ABSENT {target}"
    OwnerRebind.requireSafe visible target
  if !work.active.isEmpty then fail "UNFINISHED_CONSTRUCTION_GROUP"
  return {
    environment := work.environment
    interpretationLabels := index.labels
    targetNames := index.targets
    introducedNames := work.introduced
    introducedSignatures := work.signatures
    checkedUnits := work.checkedUnits
    scanNodes := work.scans
    encodedNodes := index.encodedNodes
    payloadBytes := index.payloadBytes }

end OrdinaryLean.OwnerConstruction
