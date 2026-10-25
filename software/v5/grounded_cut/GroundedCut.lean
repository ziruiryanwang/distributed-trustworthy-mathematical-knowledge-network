import OwnerRebind

/- CONDITIONAL local kernel primitive, not mathematical acceptance authority.
   The protected caller binds the EXACT selected seed/inventory, earlier local
   warrants, concrete records, logical-root freshness and all runtime/source bytes.
   A new event requires independent protected promotion after clean supervision.
   This primitive accepts no owner Environment, imports no runtime modules, writes
   no files and returns no scratch Environment or native snapshot. -/

open Lean

namespace OrdinaryLean.GroundedCut

structure Limits where
  maxConcreteUnits : Nat := 1024
  maxSignatures : Nat := 1024
  maxScratchNames : Nat := 65536
  maxEncodedNodes : Nat := 20000000
  maxScanNodes : Nat := 20000000
  maxPacketBytes : Nat := 67108864
  maxItemBytes : Nat := 8388608
  maxKernelCalls : Nat := 4096
  maxHeartbeats : USize := 20000000
  maxRecDepth : USize := 4096
  deriving Inhabited

/-- Evidence about this call conditional on the caller's grounding/identity
    premises. These fields are not a warrant, grant, restored context or PASS
    token. In particular signature labels do not prove their own eligibility. -/
structure Conditional where
  theoremName : Name
  theoremInventory : Json
  signatureLabels : Array OwnerRebind.BoundName
  concreteUnits : Nat
  concreteNames : Nat
  signatures : Nat
  scratchNames : Nat
  inputBytes : Nat
  encodedNodes : Nat
  scanNodes : Nat
  kernelCalls : Nat

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"GROUNDED_CUT {message}"

private def fixedNames : Nat := 581
private def fixedUnits : Nat := 456
private def guardName : Name := `DMKNGroundedCutPropGuard

private def validateLimits (limits : Limits) : IO Unit := do
  if limits.maxConcreteUnits > 1024 || limits.maxSignatures > 1024 ||
      limits.maxScratchNames < fixedNames + 1 || limits.maxScratchNames > 65536 ||
      limits.maxEncodedNodes == 0 || limits.maxEncodedNodes > 20000000 ||
      limits.maxScanNodes == 0 || limits.maxScanNodes > 20000000 ||
      limits.maxPacketBytes == 0 || limits.maxPacketBytes > 67108864 ||
      limits.maxItemBytes == 0 || limits.maxItemBytes > 8388608 ||
      limits.maxKernelCalls < fixedUnits + 2 || limits.maxKernelCalls > 4096 ||
      limits.maxHeartbeats == 0 || limits.maxHeartbeats > 20000000 ||
      limits.maxRecDepth == 0 || limits.maxRecDepth > 4096 then
    fail "FINITE_LIMITS"

private def checkerLimits (limits : Limits) : CheckedExtension.Limits := {
  maxUnits := max 1 limits.maxConcreteUnits
  maxNewNames := limits.maxScratchNames
  maxStageTwo := limits.maxScratchNames
  maxScanNodes := limits.maxScanNodes
  maxHeartbeats := limits.maxHeartbeats
  maxRecDepth := limits.maxRecDepth
}

private def rebindLimits (limits : Limits) : OwnerRebind.Limits := {
  checker := checkerLimits limits
  maxRows := limits.maxScratchNames
  maxScanNodes := limits.maxScanNodes
  maxEncodedNodes := limits.maxEncodedNodes
  maxGroupBytes := limits.maxItemBytes
  maxPayloadBytes := limits.maxPacketBytes
}

private def chargeBytes (used : Nat) (value : Json) (limits : Limits) : IO Nat := do
  let count := value.compress.utf8ByteSize
  if count > limits.maxItemBytes || used + count > limits.maxPacketBytes then
    fail "PACKET_BYTE_BOUND"
  return used + count

private def chargeNodes (used added : Nat) (limits : Limits) : IO Nat := do
  if used + added > limits.maxEncodedNodes then fail "PACKET_NODE_BOUND"
  return used + added

private def unitNodes (raw : Json) (limits : Limits) : IO Nat := do
  let fields ← ExprCodec.arrayOf raw (some 3)
  if (← ExprCodec.jsonResult fields[0]!.getStr?) != DeclCodec.unitFormat then
    fail "UNIT_FORMAT"
  let expected ← ExprCodec.arrayOf fields[2]!
  let codec := (checkerLimits limits).codec
  discard <| DeclCodec.expectedNames expected codec
  let mut nodes ← DeclCodec.descriptorNodes fields[1]! codec
  for row in expected do
    nodes ← chargeNodes nodes (← DeclCodec.inventoryNodes row codec) limits
  return nodes

private def scanDeclaration (decl : Declaration) (used : Nat) (limits : Limits)
    : IO Nat :=
  decl.foldExprM (fun count expr => do
    if count > limits.maxScanNodes then fail "PACKET_SCAN_BOUND"
    let (_, visited) ← CheckedExtension.references expr (limits.maxScanNodes - count)
    return count + visited) used

private def chargeRepeatedScan (used beforeScan : Nat) (limits : Limits) : IO Nat := do
  -- checkBatch scans the same declared expressions again; this is not a fresh
  -- packet allowance for the native helper's second traversal.
  let repeated := used - beforeScan
  if used + repeated > limits.maxScanNodes then fail "PACKET_SCAN_BOUND"
  return used + repeated

private def requireMember (allowed : Std.HashSet Name) (name : Name) : IO Unit := do
  CheckedExtension.requireName name
  if !allowed.contains name then fail s!"MISSING_SEMANTIC_REFERENCE {name}"

/-- A throwaway kernel definition proves that P itself has type Prop. Its
    returned environment is deliberately discarded, even after success. This
    is not an axiom, frontend `isProp` heuristic, or retained guard declaration. -/
private def requireProp (environment : Environment) (params : List Name)
    (type : Expr) (limits : Limits) : IO Unit := do
  if (environment.toKernelEnv.find? guardName).isSome then fail "PROP_GUARD_NAME_COLLISION"
  let guard : Declaration := .defnDecl {
    name := guardName, levelParams := params, type := .sort .zero, value := type,
    hints := .opaque, safety := .safe, all := [guardName] }
  match environment.addDeclCore limits.maxHeartbeats limits.maxRecDepth guard none (doCheck := true) with
  | .ok _ => pure ()
  | .error _ => fail "PROP_KERNEL_REJECTED_OR_RESOURCE_LIMIT"

/-- Exhaustive and bounded: all actual names and inventories, including every
    axiom, must fall into exactly one caller-built category. No scratch state
    supplied by an authoring frontend is ever used to construct these maps. -/
private def census (environment : Environment)
    (basis exact signatures : Std.HashMap Name Json) (limits : Limits) : IO Nat := do
  let expectedCount := basis.size + exact.size + signatures.size
  if expectedCount > limits.maxScratchNames then fail "SCRATCH_NAME_BOUND"
  if !environment.toKernelEnv.quotInit then fail "FIXED_QUOTIENT_REQUIRED"
  let mut seen : Std.HashSet Name := {}
  for (name, actual) in environment.toKernelEnv.constants do
    if seen.size >= limits.maxScratchNames || seen.contains name then fail "ACTUAL_CENSUS_BOUND"
    if actual.name != name || actual.isUnsafe || actual.isPartial then fail "UNSAFE_ACTUAL_RECORD"
    seen := seen.insert name
    if let some row := basis[name]? then
      if exact.contains name || signatures.contains name then fail "CATEGORY_OVERLAP"
      if (← BootstrapProbe.inventoryRow actual) != row then fail "BASIS_INVENTORY_CHANGED"
      if actual.isAxiom && !BootstrapProbe.allowedAxioms.contains name then fail "UNPERMITTED_BASIS_AXIOM"
    else if let some row := exact[name]? then
      if signatures.contains name || actual.isAxiom then fail "EXACT_RECORD_IS_ASSUMPTION"
      if (← DeclCodec.inventoryRow actual (checkerLimits limits).codec) != row then
        fail "EXACT_INVENTORY_CHANGED"
    else if let some payload := signatures[name]? then
      if !actual.isAxiom || (← OwnerRebind.theoremPayload actual (rebindLimits limits)) != payload then
        fail "SIGNATURE_INVENTORY_CHANGED"
    else
      fail s!"UNEXPECTED_ACTUAL_RECORD {name}"
  if seen.size != expectedCount then fail "ACTUAL_CENSUS_MISMATCH"
  return seen.size

/-- One new theorem checked under precisely classified scratch assumptions.
    Caller MUST authenticate fixed seed/inventory bytes before parsing, ground
    every concrete unit/signature in one eligible earlier logical root, prove
    global new-name absence, and protect the later actual-event commit. This
    function itself only checks the conditional small-environment judgment. -/
def check (seed inventory : Json) (concreteUnits signatureRows : Array Json)
    (newUnit : Json) (limits : Limits := {}) : IO Conditional := do
  validateLimits limits
  if concreteUnits.size > limits.maxConcreteUnits || signatureRows.size > limits.maxSignatures then
    fail "PACKET_ITEM_COUNT"
  let calls := fixedUnits + concreteUnits.size + 2 * signatureRows.size + 2
  if calls > limits.maxKernelCalls then fail "KERNEL_CALL_BOUND"
  let mut bytes ← chargeBytes 0 seed limits
  bytes ← chargeBytes bytes inventory limits
  let mut nodes := 0
  for raw in concreteUnits do
    bytes ← chargeBytes bytes raw limits
    nodes ← chargeNodes nodes (← unitNodes raw limits) limits
  for raw in signatureRows do
    bytes ← chargeBytes bytes raw limits
    let row ← OwnerRebind.rowOf raw (rebindLimits limits)
    if row.mode != 0 then fail "THEOREM_SIGNATURE_MODE_REQUIRED"
    nodes ← chargeNodes nodes row.encodedNodes limits
  bytes ← chargeBytes bytes newUnit limits
  nodes ← chargeNodes nodes (← unitNodes newUnit limits) limits

  let seedFields ← BootstrapProbe.arrayOf seed (some 3)
  let descriptors ← BootstrapProbe.arrayOf seedFields[1]!
  let rawNames ← BootstrapProbe.arrayOf seedFields[2]!
  let inventoryRows ← BootstrapProbe.arrayOf inventory
  if descriptors.size != fixedUnits || rawNames.size != fixedNames || inventoryRows.size != fixedNames then
    fail "FIXED_INPUT_CENSUS"
  let mut environment ← BootstrapProbe.receiveSeed seed inventory
  let mut basis : Std.HashMap Name Json := {}
  let mut allowed : Std.HashSet Name := {}
  for i in [:rawNames.size] do
    let name ← BootstrapProbe.nameOf rawNames[i]!
    let fields ← BootstrapProbe.arrayOf inventoryRows[i]! (some 5)
    if (← BootstrapProbe.nameOf fields[0]!) != name || allowed.contains name then
      fail "FIXED_BASIS_BINDING"
    basis := basis.insert name inventoryRows[i]!
    allowed := allowed.insert name
  if basis.size != fixedNames then fail "FIXED_BASIS_NAMES"

  let mut exact : Std.HashMap Name Json := {}
  let mut decoded : Array DeclCodec.DecodedUnit := #[]
  let mut scans := 0
  for raw in concreteUnits do
    let unit ← DeclCodec.decodeUnit allowed raw (checkerLimits limits).codec
    match unit.decl with
    | .defnDecl _ | .opaqueDecl _ | .inductDecl _ _ _ _ => pure ()
    | _ => fail "NONCONCRETE_DECLARATION"
    discard <| CheckedExtension.allowedDeclaration unit.decl
    let names ← DeclCodec.expectedNames unit.expected (checkerLimits limits).codec
    if allowed.size + names.size + signatureRows.size + 1 > limits.maxScratchNames then
      fail "SCRATCH_NAME_BOUND"
    for i in [:names.size] do
      let name := names[i]!
      if allowed.contains name || name == guardName then fail "CONCRETE_NAME_OVERWRITE_OR_RESERVED"
      allowed := allowed.insert name
      exact := exact.insert name unit.expected[i]!
    let beforeScan := scans
    scans ← scanDeclaration unit.decl scans limits
    scans ← chargeRepeatedScan scans beforeScan limits
    decoded := decoded.push unit
  if !decoded.isEmpty then
    let checked ← CheckedExtension.checkBatch environment decoded (checkerLimits limits)
    if checked.unitsChecked != concreteUnits.size || checked.added.size != exact.size then
      fail "CONCRETE_CHECKED_CENSUS"
    environment := checked.environment
    -- Audit generated computational semantics too, including implicit metadata
    -- references not covered by declaration-expression syntax alone.
    for actual in checked.added do
      if actual.isTheorem || actual.isAxiom then fail "CONCRETE_THEOREM_OR_AXIOM"
      scans ← OwnerRebind.scanSemantics actual .exact allowed scans (rebindLimits limits)
      match actual with
      | .defnInfo value => for name in value.all do requireMember allowed name
      | .opaqueInfo value => for name in value.all do requireMember allowed name
      | _ => pure ()
  let concreteNames := exact.size

  let mut signatures : Std.HashMap Name Json := {}
  let mut labels : Array OwnerRebind.BoundName := #[]
  for raw in signatureRows do
    let row ← OwnerRebind.rowOf raw (rebindLimits limits)
    if row.mode != 0 || allowed.contains row.binding.name || row.binding.name == guardName then
      fail "SIGNATURE_MODE_OVERWRITE_OR_RESERVED"
    if allowed.size + 2 > limits.maxScratchNames then fail "SCRATCH_NAME_BOUND"
    let payload ← ExprCodec.arrayOf row.payload (some 2)
    let params ← DeclCodec.paramsOf payload[0]! (checkerLimits limits).codec
    let type ← ExprCodec.decode params allowed payload[1]! (checkerLimits limits).codec.expr
    if (← DeclCodec.paramsJson params (checkerLimits limits).codec) != payload[0]! ||
        (← ExprCodec.encode params type (checkerLimits limits).codec.expr) != payload[1]! then
      fail "NONCANONICAL_SIGNATURE"
    if scans > limits.maxScanNodes then fail "PACKET_SCAN_BOUND"
    let (refs, visited) ← CheckedExtension.references type (limits.maxScanNodes - scans)
    scans := scans + visited
    for name in refs do requireMember allowed name
    requireProp environment params type limits
    let assumption : Declaration := .axiomDecl {
      name := row.binding.name, levelParams := params, type, isUnsafe := false }
    environment ← match environment.addDeclCore limits.maxHeartbeats limits.maxRecDepth
        assumption none (doCheck := true) with
      | .ok candidate => pure candidate
      | .error _ => fail "SIGNATURE_KERNEL_REJECTED_OR_RESOURCE_LIMIT"
    let some actual := environment.toKernelEnv.find? row.binding.name | fail "SIGNATURE_ABSENT"
    if !actual.isAxiom || actual.isUnsafe || actual.isPartial ||
        (← OwnerRebind.theoremPayload actual (rebindLimits limits)) != row.payload then
      fail "SIGNATURE_ACTUAL_MISMATCH"
    allowed := allowed.insert row.binding.name
    signatures := signatures.insert row.binding.name row.payload
    labels := labels.push row.binding

  let beforeCount ← census environment basis exact signatures limits
  if beforeCount != allowed.size then fail "PRECHECK_ALLOWLIST_MISMATCH"
  let target ← DeclCodec.decodeUnit allowed newUnit (checkerLimits limits).codec
  let newTheorem ← match target.decl with
    | .thmDecl value => pure value
    | _ => fail "ONE_NEW_THEOREM_REQUIRED"
  let names ← DeclCodec.expectedNames target.expected (checkerLimits limits).codec
  if names.size != 1 || names[0]! != newTheorem.name || allowed.contains newTheorem.name ||
      newTheorem.name == guardName ||
      beforeCount + 1 > limits.maxScratchNames then fail "NEW_THEOREM_CENSUS_OR_OVERWRITE"
  requireProp environment newTheorem.levelParams newTheorem.type limits
  let beforeScan := scans
  scans ← scanDeclaration target.decl scans limits
  scans ← chargeRepeatedScan scans beforeScan limits
  let checked ← CheckedExtension.checkBatch environment #[target] (checkerLimits limits)
  if checked.unitsChecked != 1 || checked.added.size != 1 then fail "NEW_CHECKED_CENSUS"
  let actual := checked.added[0]!
  if !actual.isTheorem || actual.name != newTheorem.name || actual.isAxiom ||
      actual.isUnsafe || actual.isPartial then fail "NEW_ACTUAL_THEOREM_REQUIRED"
  let actualInventory ← DeclCodec.inventoryRow actual (checkerLimits limits).codec
  if actualInventory != target.expected[0]! then fail "NEW_ACTUAL_INVENTORY"
  exact := exact.insert newTheorem.name actualInventory
  let afterCount ← census checked.environment basis exact signatures limits
  if afterCount != beforeCount + 1 then fail "POSTCHECK_CENSUS_MISMATCH"
  return {
    theoremName := newTheorem.name, theoremInventory := actualInventory,
    signatureLabels := labels, concreteUnits := concreteUnits.size,
    concreteNames, signatures := labels.size, scratchNames := afterCount,
    inputBytes := bytes, encodedNodes := nodes, scanNodes := scans, kernelCalls := calls }

end OrdinaryLean.GroundedCut
