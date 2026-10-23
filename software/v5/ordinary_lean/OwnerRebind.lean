module

public import BootstrapSupport
public import CheckedExtension
public import Lean.Namespace

/- Conditional owner-authoring correspondence, NOT a mathematical acceptance
   authority. The controller authenticates the accepted context, every symbol
   binding and every prepared byte before this API is called. Matching an owner
   axiom-shaped authoring handle never supplies a warrant or creates an axiom.
   Final successor admission must independently check against the actual
   warranted receiver context. No peer source, importModules or binary loading. -/

public section
open Lean

namespace OrdinaryLean.OwnerRebind

def groupFormat : String := "DMKN_OWNER_GROUP_V1"

/-- Trusted construction policy, never selected by peer request JSON. Abstract
    handles retain the pinned kernel's primitive reductions, not delta bodies. -/
inductive DefinitionView where
  | exact
  | existingAbstract
  deriving BEq, Inhabited

inductive MatchKind where
  | theoremInterface
  | abstractDefinition
  | exact
  deriving BEq, Inhabited

structure Limits where
  checker : CheckedExtension.Limits := {}
  maxBasisRows : Nat := 4096
  maxGroups : Nat := 8192
  maxRows : Nat := 65536
  maxTargets : Nat := 1024
  maxCheckedUnits : Nat := 1024
  maxAddedNames : Nat := 65536
  maxScanNodes : Nat := 20000000
  maxEncodedNodes : Nat := 20000000
  maxGroupBytes : Nat := 8388608
  maxPayloadBytes : Nat := 67108864
  deriving Inhabited

/-- All identities are exact controller-authenticated labels, not self-proving
    claims. `basisRows` entries are [basisSymbolId, legacyInventoryRow]. A basis
    theorem row has kind 2 and empty details, retaining its warranted type/arity.
    `targets` entries are [originalName, acceptedSymbolId]. `readGroup` returns
    immutable, preflighted JSON from a controller-chosen numbered file. It must
    not execute peer code or treat peer paths as authorized. -/
structure Prepared where
  profileId : String
  contextId : String
  basisId : String
  basisRows : Array Json
  targets : Array Json
  groupCount : Nat
  readGroup : Nat → IO Json

structure BoundName where
  name : Name
  symbolId : String
  deriving Inhabited

/-- `mode = 0` is a warranted theorem interface [params, originalTypeDAG].
    `mode = 1` carries the full accepted non-theorem inventory row. Concrete
    owner records always match it exactly; only explicit existingAbstract policy
    permits an already existing axiom-shaped definition/opaque handle. -/
structure Row where
  binding : BoundName
  mode : Nat
  payload : Json
  encodedNodes : Nat
  deriving Inhabited

structure Rebound where
  environment : Environment
  bindings : Array BoundName
  targetNames : Array Name
  interfaceMatched : Nat
  abstractDefinitions : Nat
  exactMatched : Nat
  checkedUnits : Nat
  addedNames : Array Name
  scanNodes : Nat
  encodedNodes : Nat
  payloadBytes : Nat

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"ORDINARY_OWNER_REBIND {message}"

def identityOf (value : Json) : IO String := do
  let text ← ExprCodec.jsonResult value.getStr?
  if text.utf8ByteSize != 64 || !text.toList.all (fun c =>
      ('0' ≤ c && c ≤ '9') || ('a' ≤ c && c ≤ 'f')) then
    fail "IDENTITY_SHAPE"
  return text

def nameOf (value : Json) (limits : Limits) : IO Name := do
  let name ← ExprCodec.decodeName value limits.checker.codec.expr
  CheckedExtension.requireName name
  return name

def boundOf (value : Json) (limits : Limits) : IO BoundName := do
  let fields ← ExprCodec.arrayOf value (some 2)
  return { name := ← nameOf fields[0]! limits, symbolId := ← identityOf fields[1]! }

def rowOf (value : Json) (limits : Limits) : IO Row := do
  let fields ← ExprCodec.arrayOf value (some 4)
  let name ← nameOf fields[0]! limits
  let mode ← ExprCodec.natOf fields[1]!
  if mode > 1 then fail "MATCH_MODE"
  let symbolId ← identityOf fields[2]!
  let encodedNodes ← if mode == 0 then do
    let payload ← ExprCodec.arrayOf fields[3]! (some 2)
    discard <| DeclCodec.paramsOf payload[0]! limits.checker.codec
    DeclCodec.dagNodes payload[1]! limits.checker.codec
  else do
    let payload ← ExprCodec.arrayOf fields[3]! (some 5)
    if (← nameOf payload[0]! limits) != name then fail "ROW_NAME_MISMATCH"
    if (← ExprCodec.natOf payload[1]!) == 2 then fail "THEOREM_REQUIRES_INTERFACE_MODE"
    DeclCodec.inventoryNodes fields[3]! limits.checker.codec
  return { binding := { name, symbolId }, mode, payload := fields[3]!, encodedNodes }

def legacyDagNodes (raw : Json) (limits : Limits) : IO Nat := do
  let packet ← ExprCodec.arrayOf raw (some 3)
  let levels ← ExprCodec.arrayOf packet[0]!
  let exprs ← ExprCodec.arrayOf packet[1]!
  if levels.size > limits.checker.codec.expr.maxLevels || exprs.isEmpty ||
      exprs.size > limits.checker.codec.expr.maxExprs then fail "BASIS_DAG_BOUND"
  discard <| ExprCodec.indexOf packet[2]! exprs.size
  return levels.size + exprs.size

def basisNodes (raw : Json) (limits : Limits) : IO Nat := do
  let row ← ExprCodec.arrayOf raw (some 5)
  let mut nodes ← legacyDagNodes row[3]! limits
  let kind ← ExprCodec.natOf row[1]!
  let details ← ExprCodec.arrayOf row[4]!
  if kind == 1 || kind == 3 then
    discard <| ExprCodec.arrayOf row[4]! (some 3)
    nodes := nodes + (← legacyDagNodes details[0]! limits)
  else if kind == 6 then
    discard <| ExprCodec.arrayOf row[4]! (some 8)
    let rules ← ExprCodec.arrayOf details[5]!
    if rules.size > limits.checker.codec.maxConstructors then fail "BASIS_RULE_BOUND"
    for rawRule in rules do
      let rule ← ExprCodec.arrayOf rawRule (some 3)
      nodes := nodes + (← legacyDagNodes rule[2]! limits)
  else if kind == 2 then
    discard <| ExprCodec.arrayOf row[4]! (some 0)
  if nodes > limits.maxEncodedNodes then fail "AGGREGATE_ENCODED_NODE_BOUND"
  return nodes

def addEncoded (used added : Nat) (limits : Limits) : IO Nat := do
  if used + added > limits.maxEncodedNodes then fail "AGGREGATE_ENCODED_NODE_BOUND"
  return used + added

def requireSafe (actual : ConstantInfo) (name : Name) : IO Unit := do
  if actual.name != name then fail "RECORD_KEY_MISMATCH"
  if actual.isUnsafe || actual.isPartial then fail "UNSAFE_OWNER_RECORD"

def theoremPayload (actual : ConstantInfo) (limits : Limits) : IO Json := do
  match actual with
  | .thmInfo _ | .axiomInfo _ => pure ()
  | _ => fail "THEOREM_AUTHORING_HANDLE_REQUIRED"
  return Json.arr #[← DeclCodec.paramsJson actual.levelParams limits.checker.codec,
    ← ExprCodec.encode actual.levelParams actual.type limits.checker.codec.expr]

/-- Existing axiom-shaped construction handle only; this does not classify it
    as a theorem or infer any accepted identity from its type. -/
def abstractPayload (actual : ConstantInfo) (limits : Limits) : IO Json := do
  if !actual.isAxiom then fail "EXISTING_ABSTRACT_HANDLE_REQUIRED"
  return Json.arr #[← DeclCodec.paramsJson actual.levelParams limits.checker.codec,
    ← ExprCodec.encode actual.levelParams actual.type limits.checker.codec.expr]

def matchRow (actual : ConstantInfo) (row : Row) (limits : Limits)
    (definitionView : DefinitionView := .exact) : IO MatchKind := do
  requireSafe actual row.binding.name
  if row.mode == 0 then
    if (← theoremPayload actual limits) != row.payload then
      fail s!"THEOREM_INTERFACE_MISMATCH {row.binding.name}"
    return .theoremInterface
  if definitionView == .existingAbstract && actual.isAxiom then
    let accepted ← ExprCodec.arrayOf row.payload (some 5)
    let kind ← ExprCodec.natOf accepted[1]!
    if kind != 1 && kind != 3 then
      fail s!"NEEDS_DEPENDENCY_SEMANTICS {row.binding.name}"
    if (← abstractPayload actual limits) != Json.arr #[accepted[2]!, accepted[3]!] then
      fail s!"ABSTRACT_INTERFACE_MISMATCH {row.binding.name}"
    return .abstractDefinition
  if actual.isAxiom || actual.isTheorem then
    fail s!"NEEDS_DEPENDENCY_SEMANTICS {row.binding.name}"
  if (← DeclCodec.inventoryRow actual limits.checker.codec) != row.payload then
    fail s!"EXACT_SEMANTICS_MISMATCH {row.binding.name}"
  return .exact

/-- Never calls inventoryRow on theorem handles: imported public theorem stubs
    need neither their original proof values nor a reclassification as axioms.
    Explicit abstract policy also permits existing definition/opaque stubs,
    without changing their warranted accepted meaning or primitive rules. -/
def matchBasisRow (actual : ConstantInfo) (raw : Json)
    (definitionView : DefinitionView := .exact) : IO MatchKind := do
  let row ← ExprCodec.arrayOf raw (some 5)
  let name ← BootstrapProbe.nameOf row[0]!
  CheckedExtension.requireName name
  requireSafe actual name
  let kind ← ExprCodec.natOf row[1]!
  if kind == 2 then
    match actual with
    | .thmInfo _ | .axiomInfo _ => pure ()
    | _ => fail "BASIS_THEOREM_HANDLE_REQUIRED"
    discard <| ExprCodec.arrayOf row[4]! (some 0)
    if actual.levelParams.length != (← ExprCodec.natOf row[2]!) ||
        (← BootstrapProbe.dagJson actual.levelParams actual.type) != row[3]! then
      fail s!"BASIS_THEOREM_INTERFACE_MISMATCH {name}"
    return .theoremInterface
  if kind > 7 then fail "BASIS_KIND"
  if definitionView == .existingAbstract && actual.isAxiom && (kind == 1 || kind == 3) then
    if actual.levelParams.length != (← ExprCodec.natOf row[2]!) ||
        (← BootstrapProbe.dagJson actual.levelParams actual.type) != row[3]! then
      fail s!"BASIS_ABSTRACT_INTERFACE_MISMATCH {name}"
    return .abstractDefinition
  BootstrapProbe.screen actual
  if kind == 0 && !BootstrapProbe.allowedAxioms.contains name then
    fail "NONPERMITTED_FOUNDATION_AXIOM"
  if kind == 7 && !BootstrapProbe.quotNames.contains name then
    fail "NONPERMITTED_QUOTIENT_PRIMITIVE"
  let height ← if kind == 1 then do
    let details ← ExprCodec.arrayOf row[4]! (some 3)
    pure <| some (← ExprCodec.u32Of details[1]!)
  else pure none
  if (← BootstrapProbe.inventoryRow actual height) != raw then
    fail s!"BASIS_SEMANTICS_MISMATCH {name}"
  return .exact

def requireBound (allowed : Std.HashSet Name) (name : Name) : IO Unit := do
  CheckedExtension.requireName name
  if !allowed.contains name then fail s!"UNBOUND_SEMANTIC_DEPENDENCY {name}"

def scanExpr (expr : Expr) (allowed : Std.HashSet Name) (used : Nat)
    (limits : Limits) : IO Nat := do
  if used > limits.maxScanNodes then fail "AGGREGATE_SCAN_BOUND"
  let (refs, count) ← CheckedExtension.references expr (limits.maxScanNodes - used)
  for name in refs do requireBound allowed name
  return used + count

/-- Theorem handles and explicit abstract definition handles scan their actual
    types, not a fictitious body. Concrete definitions/opaques retain body scans;
    generated records retain computation and group references. Exact accepted
    meaning and primitive interpretation remain controller/profile premises. -/
def scanSemantics (actual : ConstantInfo) (matchKind : MatchKind)
    (allowed : Std.HashSet Name) (used : Nat) (limits : Limits) : IO Nat := do
  let mut count ← scanExpr actual.type allowed used limits
  if matchKind != .exact then return count
  match actual with
  | .defnInfo value => count ← scanExpr value.value allowed count limits
  | .opaqueInfo value => count ← scanExpr value.value allowed count limits
  | .inductInfo value =>
      for name in value.all do requireBound allowed name
      for name in value.ctors do requireBound allowed name
  | .ctorInfo value => requireBound allowed value.induct
  | .recInfo value =>
      for name in value.all do requireBound allowed name
      for rule in value.rules do
        requireBound allowed rule.ctor
        count ← scanExpr rule.rhs allowed count limits
  | .thmInfo _ => fail "THEOREM_PROOF_SCAN_FORBIDDEN"
  | .axiomInfo _ | .quotInfo _ => pure ()
  return count

def isNamespaceName : Name → Bool
  | .str .anonymous _ => true
  | .str parent _ => isNamespaceName parent
  | _ => false

def registerPrefixesAux (env : Environment) : Name → Environment
  | .str parent _ =>
      if isNamespaceName parent then
        registerPrefixesAux (env.registerNamespace parent) parent
      else env
  | _ => env

/-- Same small namespace rule as Lean.AddDecl, without importing elaborator or
    compiler implementation modules. No notation, instance or plugin loader. -/
def registerPrefixes (env : Environment) (name : Name) : Environment :=
  let userName := privateToUserName name
  match userName with
  | .str _ last =>
      if last.front == '_' then env else registerPrefixesAux env userName
  | _ => env

/-- Only actual newly checked recursors may be exposed in the frontend map.
    Existing hidden/private records are never copied or promoted here. -/
def exposeAdded (env : Environment) (added : Array ConstantInfo) : IO Environment := do
  let mut candidate := env
  for actual in added do
    if (candidate.find? actual.name (skipRealize := true)).isNone then
      match actual with
      | .recInfo _ =>
          let result ← candidate.addConstAsync actual.name .recursor
          result.commitConst result.asyncEnv (info? := actual)
          result.commitCheckEnv result.asyncEnv
          candidate := result.mainEnv
      | _ => fail s!"NEW_FRONTEND_RECORD_ABSENT {actual.name}"
    candidate := registerPrefixes candidate actual.name
  return candidate

def chargeBytes (used : Nat) (value : Json) (maximum : Nat) : IO Nat := do
  let size := value.compress.utf8ByteSize
  if used + size > maximum then fail "PAYLOAD_BYTE_BOUND"
  return used + size

/-- Check the prepared group's local shape without a whole-environment census.
    Completeness of the supplied generated inventory is inherited only from
    the controller's exact accepted unit, never from these names themselves. -/
def groupScope (environment : Kernel.Environment) (rows : Array Row)
    (bound allNames : Std.HashSet Name) (hasGeneratedUnit : Bool) : IO (Std.HashSet Name) := do
  let mut ownerName : Option Name := none
  let mut generated := false
  for row in rows do
    let some actual := environment.find? row.binding.name | fail "GROUP_RECORD_ABSENT"
    match actual with
    | .inductInfo _ | .ctorInfo _ | .recInfo _ =>
        if row.mode != 1 || !hasGeneratedUnit then fail "GENERATED_GROUP_DATA_REQUIRED"
        generated := true
        let key ← BootstrapProbe.owner environment row.binding.name
        match ownerName with
        | none => ownerName := some key
        | some old => if old != key then fail "MIXED_GENERATED_GROUP"
    | _ =>
        if rows.size != 1 then fail "NONATOMIC_ORDINARY_GROUP"
  if generated then
    let some key := ownerName | fail "MISSING_GENERATED_GROUP_OWNER"
    if bound.contains key || !allNames.contains key then fail "PARTIAL_EXISTING_GROUP"
    return allNames
  return bound

/-- Atomic caller-visible construction. The supplied owner is retained; all
    candidate environments remain local until the whole request succeeds.
    This function does not call setEnv/modifyEnv, import a module, publish a
    result, save an olean or grant mathematical authority to its output. -/
def rebindPrepared (owner : Environment) (prepared : Prepared) (limits : Limits := {})
    (definitionView : DefinitionView := .exact)
    : IO Rebound := do
  if owner.asyncPrefix?.isSome then fail "TOP_LEVEL_OWNER_REQUIRED"
  if !owner.toKernelEnv.quotInit then fail "OWNER_QUOTIENT_PROFILE_REQUIRED"
  for id in [prepared.profileId, prepared.contextId, prepared.basisId] do
    discard <| identityOf (Json.str id)
  if prepared.basisRows.isEmpty || prepared.basisRows.size > limits.maxBasisRows ||
      prepared.groupCount > limits.maxGroups || prepared.targets.isEmpty ||
      prepared.targets.size > limits.maxTargets then fail "PREPARED_COUNT_BOUND"
  let header := Json.arr #[Json.str prepared.profileId, Json.str prepared.contextId,
    Json.str prepared.basisId, Json.arr prepared.basisRows, Json.arr prepared.targets,
    toJson prepared.groupCount]
  let mut bytes ← chargeBytes 0 header limits.maxPayloadBytes
  let mut candidate := owner
  let mut bound : Std.HashSet Name := {}
  let mut symbols : Std.HashMap Name String := {}
  let mut basisByName : Std.HashMap Name Json := {}
  let mut matchKinds : Std.HashMap Name MatchKind := {}
  let mut bindings : Array BoundName := #[]
  let mut interfaces := 0
  let mut abstractDefinitions := 0
  let mut exact := 0
  let mut rowsCount := 0
  let mut scans := 0
  let mut encodedNodes := 0
  let mut checkedUnits := 0
  let mut addedNames : Array Name := #[]
  -- The fixed foundation is a closed selected block, not a whole-owner census.
  for raw in prepared.basisRows do
    let entry ← ExprCodec.arrayOf raw (some 2)
    let symbolId ← identityOf entry[0]!
    let row ← ExprCodec.arrayOf entry[1]! (some 5)
    let name ← BootstrapProbe.nameOf row[0]!
    CheckedExtension.requireName name
    if bound.contains name then fail "DUPLICATE_BASIS_NAME"
    bound := bound.insert name
    symbols := symbols.insert name symbolId
    basisByName := basisByName.insert name entry[1]!
    bindings := bindings.push { name, symbolId }
    encodedNodes ← addEncoded encodedNodes (← basisNodes entry[1]! limits) limits
  rowsCount := bindings.size
  if rowsCount > limits.maxRows then fail "AGGREGATE_ROW_BOUND"
  for raw in prepared.basisRows do
    let entry ← ExprCodec.arrayOf raw (some 2)
    let row ← ExprCodec.arrayOf entry[1]! (some 5)
    let name ← BootstrapProbe.nameOf row[0]!
    let some actual := candidate.toKernelEnv.find? name | fail s!"MISSING_FIXED_BASIS {name}"
    let matchKind ← matchBasisRow actual entry[1]! definitionView
    scans ← scanSemantics actual matchKind bound scans limits
    matchKinds := matchKinds.insert name matchKind
    match matchKind with
    | .theoremInterface => interfaces := interfaces + 1
    | .abstractDefinition => abstractDefinitions := abstractDefinitions + 1
    | .exact => exact := exact + 1
  for index in [:prepared.groupCount] do
    let packet ← prepared.readGroup index
    let groupSize := packet.compress.utf8ByteSize
    if groupSize > limits.maxGroupBytes || bytes + groupSize > limits.maxPayloadBytes then
      fail "AGGREGATE_PAYLOAD_BYTE_BOUND"
    bytes := bytes + groupSize
    let fields ← ExprCodec.arrayOf packet (some 3)
    if (← ExprCodec.jsonResult fields[0]!.getStr?) != groupFormat then fail "GROUP_FORMAT"
    let rawRows ← ExprCodec.arrayOf fields[1]!
    if rawRows.isEmpty || rowsCount + rawRows.size > limits.maxRows then
      fail "AGGREGATE_ROW_BOUND"
    let optionalUnit ← ExprCodec.arrayOf fields[2]!
    if optionalUnit.size > 1 then fail "OPTIONAL_UNIT_SHAPE"
    let mut rows : Array Row := #[]
    let mut groupNames : Array Name := #[]
    let mut allowed := bound
    let mut present := 0
    for rawRow in rawRows do
      let row ← rowOf rawRow limits
      let name := row.binding.name
      if allowed.contains name then fail "DUPLICATE_OR_REBOUND_NAME"
      allowed := allowed.insert name
      groupNames := groupNames.push name
      rows := rows.push row
      encodedNodes ← addEncoded encodedNodes row.encodedNodes limits
      if (candidate.toKernelEnv.find? name).isSome then present := present + 1
    if present != 0 && present != rows.size then fail "PARTIAL_EXISTING_GROUP"
    let mut hasGeneratedUnit := false
    -- Even an optional unit ignored for an existing theorem must obey aggregate
    -- byte/node bounds. Do not decode its proof or demand proof dependencies.
    if optionalUnit.size == 1 then
      let unitFields ← ExprCodec.arrayOf optionalUnit[0]! (some 3)
      if (← ExprCodec.jsonResult unitFields[0]!.getStr?) != DeclCodec.unitFormat then
        fail "UNIT_FORMAT"
      let expected ← ExprCodec.arrayOf unitFields[2]!
      if (← DeclCodec.expectedNames expected limits.checker.codec) != groupNames then
        fail "GROUP_UNIT_CENSUS_MISMATCH"
      encodedNodes ← addEncoded encodedNodes
        (← DeclCodec.descriptorNodes unitFields[1]! limits.checker.codec) limits
      for raw in expected do
        encodedNodes ← addEncoded encodedNodes
          (← DeclCodec.inventoryNodes raw limits.checker.codec) limits
      let descriptor ← ExprCodec.arrayOf unitFields[1]!
      if descriptor.isEmpty then fail "EMPTY_DESCRIPTOR"
      hasGeneratedUnit := (← ExprCodec.natOf descriptor[0]!) == 3
    if present == 0 then
      if optionalUnit.size != 1 then fail "MISSING_CHECKED_CONSTRUCTION_DATA"
      if checkedUnits >= limits.maxCheckedUnits ||
          addedNames.size + rows.size > limits.maxAddedNames then fail "AGGREGATE_ADDITION_BOUND"
      let unit ← DeclCodec.decodeUnit bound optionalUnit[0]! limits.checker.codec
      if (← DeclCodec.expectedNames unit.expected limits.checker.codec) != groupNames then
        fail "GROUP_UNIT_CENSUS_MISMATCH"
      let selfTypes ← CheckedExtension.allowedDeclaration unit.decl
      let mut declarationAllowed := bound
      for name in selfTypes do declarationAllowed := declarationAllowed.insert name
      let beforeScan := scans
      scans ← unit.decl.foldExprM (fun count expr =>
        scanExpr expr declarationAllowed count limits) scans
      -- The unchanged checker performs the same declaration scan. Account for
      -- both traversals globally instead of renewing its budget per group.
      let checkScan := scans - beforeScan
      if checkScan > limits.checker.maxScanNodes ||
          scans + checkScan > limits.maxScanNodes then fail "AGGREGATE_CHECK_SCAN_BOUND"
      let checked ← CheckedExtension.checkBatch candidate #[unit] limits.checker
      scans := scans + checkScan
      candidate ← exposeAdded checked.environment checked.added
      checkedUnits := checkedUnits + checked.unitsChecked
      for actual in checked.added do addedNames := addedNames.push actual.name
    let semanticsAllowed ← groupScope candidate.toKernelEnv rows bound allowed hasGeneratedUnit
    for row in rows do
      let some actual := candidate.toKernelEnv.find? row.binding.name
        | fail "MISSING_MATCHED_RECORD"
      let matchKind ← matchRow actual row limits definitionView
      scans ← scanSemantics actual matchKind semanticsAllowed scans limits
      matchKinds := matchKinds.insert row.binding.name matchKind
      match matchKind with
      | .theoremInterface => interfaces := interfaces + 1
      | .abstractDefinition => abstractDefinitions := abstractDefinitions + 1
      | .exact => exact := exact + 1
      symbols := symbols.insert row.binding.name row.binding.symbolId
      bindings := bindings.push row.binding
    bound := allowed
    rowsCount := rowsCount + rows.size
  let mut targets : Array Name := #[]
  let mut targetSet : Std.HashSet Name := {}
  for raw in prepared.targets do
    let target ← boundOf raw limits
    if targetSet.contains target.name then fail "DUPLICATE_TARGET"
    let some symbolId := symbols[target.name]? | fail "UNBOUND_TARGET"
    if symbolId != target.symbolId then fail "TARGET_SYMBOL_MISMATCH"
    let some actual := candidate.toKernelEnv.find? target.name | fail "TARGET_KERNEL_ABSENT"
    let some visible := candidate.find? target.name (skipRealize := true)
      | fail "TARGET_FRONTEND_ABSENT"
    requireSafe visible target.name
    let some matchKind := matchKinds[target.name]? | fail "TARGET_MATCH_CLASS_ABSENT"
    -- Targets may be basis names. Reuse their already verified matching mode,
    -- rather than assuming every target is a theorem or comparing proof values.
    if let some basisRow := basisByName[target.name]? then
      if (← matchBasisRow visible basisRow definitionView) != matchKind then
        fail "TARGET_FRONTEND_MATCH_CLASS_MISMATCH"
    else
      match matchKind with
      | .theoremInterface =>
          if (← theoremPayload visible limits) != (← theoremPayload actual limits) then
            fail "TARGET_FRONTEND_INTERFACE_MISMATCH"
      | .abstractDefinition =>
          if (← abstractPayload visible limits) != (← abstractPayload actual limits) then
            fail "TARGET_FRONTEND_ABSTRACT_INTERFACE_MISMATCH"
      | .exact =>
          if (← DeclCodec.inventoryRow visible limits.checker.codec) !=
              (← DeclCodec.inventoryRow actual limits.checker.codec) then
            fail "TARGET_FRONTEND_SEMANTICS_MISMATCH"
    targetSet := targetSet.insert target.name
    targets := targets.push target.name
  if interfaces + abstractDefinitions + exact != bindings.size ||
      matchKinds.size != bindings.size then fail "MATCH_CLASS_CENSUS"
  return {
    environment := candidate
    bindings := bindings
    targetNames := targets
    interfaceMatched := interfaces
    abstractDefinitions := abstractDefinitions
    exactMatched := exact
    checkedUnits := checkedUnits
    addedNames := addedNames
    scanNodes := scans
    encodedNodes := encodedNodes
    payloadBytes := bytes
  }

end OrdinaryLean.OwnerRebind
