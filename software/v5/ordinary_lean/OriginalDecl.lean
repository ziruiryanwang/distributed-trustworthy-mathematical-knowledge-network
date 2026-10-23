import OriginalExpr
import Lean.Declaration

/- Inert ordinary declaration units and exact mdata-erased actual inventories.
   This module never inserts ConstantInfo or declarations into an environment.
   Expected inventories are peer claims to compare AFTER checked generation. -/

open Lean
namespace OrdinaryLean.DeclCodec
open ExprCodec

def unitFormat : String := "DMKN_LEAN_ORDINARY_UNIT_V1"

structure Limits where
  expr : ExprCodec.Limits := {}
  maxTypes : Nat := 4096
  maxConstructors : Nat := 65536
  maxInventory : Nat := 65536
  maxAll : Nat := 65536
  maxUnitNodes : Nat := 2097152
  deriving Inhabited

structure DecodedUnit where
  decl : Declaration
  expected : Array Json

def boolJson (value : Bool) : Json := num (if value then 1 else 0)

def boundedNat (value : Nat) : IO Json := do
  if value > 4294967295 then fail "DECLARATION_UINT32"
  return num value

def nameOf (value : Json) (limits : Limits) : IO Name := do
  let name ← decodeName value limits.expr
  requireSemanticName name
  return name

def nameJson (name : Name) (limits : Limits) : IO Json := do
  requireSemanticName name
  encodeName name limits.expr

def namesOf (value : Json) (bound : Nat) (limits : Limits)
    (semantic := true) : IO (List Name) := do
  let raw ← arrayOf value
  if raw.size > bound then fail "DECLARATION_NAME_LIST_BOUND"
  let mut out : Array Name := #[]
  let mut seen : Std.HashSet Name := {}
  for entry in raw do
    let name ← decodeName entry limits.expr
    if semantic then requireSemanticName name
    if seen.contains name then fail "DECLARATION_DUPLICATE_NAME"
    seen := seen.insert name
    out := out.push name
  return out.toList

def namesJson (names : List Name) (bound : Nat) (limits : Limits)
    (semantic := true) : IO Json := do
  if names.length > bound then fail "DECLARATION_NAME_LIST_BOUND"
  let mut out := #[]
  let mut seen : Std.HashSet Name := {}
  for name in names do
    if semantic then requireSemanticName name
    if seen.contains name then fail "DECLARATION_DUPLICATE_NAME"
    seen := seen.insert name
    out := out.push (← encodeName name limits.expr)
  return arr out

def paramsOf (value : Json) (limits : Limits) : IO (List Name) := do
  let params ← namesOf value limits.expr.maxParams limits false
  validateParams params limits.expr
  return params

def paramsJson (params : List Name) (limits : Limits) : IO Json := do
  validateParams params limits.expr
  namesJson params limits.expr.maxParams limits false

def allOf (value : Json) (own : Name) (limits : Limits) : IO (List Name) := do
  let names ← namesOf value limits.maxAll limits
  if !names.contains own then fail "DECLARATION_ALL_OMITS_SELF"
  return names

def allJson (names : List Name) (own : Name) (limits : Limits) : IO Json := do
  if !names.contains own then fail "DECLARATION_ALL_OMITS_SELF"
  namesJson names limits.maxAll limits

def hintJson : ReducibilityHints → Json
  | .opaque => arr #[num 0]
  | .abbrev => arr #[num 1]
  | .regular height => arr #[num 2, num height.toNat]

def hintOf (value : Json) : IO ReducibilityHints := do
  let parts ← arrayOf value
  if parts.isEmpty then fail "EMPTY_HINT"
  match ← natOf parts[0]! with
  | 0 => do
      discard <| arrayOf value (some 1)
      pure .opaque
  | 1 => do
      discard <| arrayOf value (some 1)
      pure .abbrev
  | 2 => do
      discard <| arrayOf value (some 2)
      pure <| .regular (UInt32.ofNat (← u32Of parts[1]!))
  | _ => fail "HINT_TAG"

/-- Shape/count preflight only; expression decoding and checking are separate. -/
def dagNodes (value : Json) (limits : Limits) : IO Nat := do
  let packet ← arrayOf value (some 4)
  if (← jsonResult packet[0]!.getStr?) != ExprCodec.format then fail "DECLARATION_EXPR_FORMAT"
  let levels ← arrayOf packet[1]!
  let exprs ← arrayOf packet[2]!
  if levels.size > limits.expr.maxLevels || exprs.isEmpty || exprs.size > limits.expr.maxExprs then
    fail "DECLARATION_DAG_BOUND"
  discard <| indexOf packet[3]! exprs.size
  return levels.size + exprs.size

def chargeNodes (used added : Nat) (limits : Limits) : IO Nat := do
  let total := used + added
  if total > limits.maxUnitNodes then fail "UNIT_NODE_BOUND"
  return total

/-- Exact ordinary output projection; all metadata except Expr.mdata is retained. -/
def inventoryRow (info : ConstantInfo) (limits : Limits := {}) : IO Json := do
  if info.isUnsafe || info.isPartial then fail "UNSAFE_INVENTORY"
  let name ← nameJson info.name limits
  let params ← paramsJson info.levelParams limits
  let type ← ExprCodec.encode info.levelParams info.type limits.expr
  let (kind, details) ← match info with
    | .defnInfo d => do
        if d.safety != .safe then fail "UNSAFE_DEFINITION"
        pure (1, arr #[← ExprCodec.encode d.levelParams d.value limits.expr,
          hintJson d.hints, ← allJson d.all d.name limits])
    | .thmInfo d => pure (2, arr #[← ExprCodec.encode d.levelParams d.value limits.expr,
          ← allJson d.all d.name limits])
    | .opaqueInfo d => pure (3, arr #[← ExprCodec.encode d.levelParams d.value limits.expr,
          boolJson d.isUnsafe, ← allJson d.all d.name limits])
    | .inductInfo d => pure (4, arr #[← boundedNat d.numParams, ← boundedNat d.numIndices,
          ← allJson d.all d.name limits, ← namesJson d.ctors limits.maxConstructors limits,
          ← boundedNat d.numNested, boolJson d.isRec, boolJson d.isUnsafe, boolJson d.isReflexive])
    | .ctorInfo d => pure (5, arr #[← nameJson d.induct limits, ← boundedNat d.cidx,
          ← boundedNat d.numParams, ← boundedNat d.numFields, boolJson d.isUnsafe])
    | .recInfo d => do
        if d.rules.length > limits.maxConstructors then fail "RECURSOR_RULE_BOUND"
        let mut rules := #[]
        for rule in d.rules do
          rules := rules.push (arr #[← nameJson rule.ctor limits, ← boundedNat rule.nfields,
            ← ExprCodec.encode d.levelParams rule.rhs limits.expr])
        pure (6, arr #[← namesJson d.all limits.maxAll limits,
          ← boundedNat d.numParams, ← boundedNat d.numIndices,
          ← boundedNat d.numMotives, ← boundedNat d.numMinors,
          arr rules, boolJson d.k, boolJson d.isUnsafe])
    | .axiomInfo _ | .quotInfo _ => fail "AXIOM_OR_QUOT_IN_EXTENSION"
  return arr #[name, num kind, params, type, details]

def expectedNames (expected : Array Json) (limits : Limits := {}) : IO (Array Name) := do
  if expected.isEmpty || expected.size > limits.maxInventory then fail "INVENTORY_COUNT"
  let mut names := #[]
  let mut seen : Std.HashSet Name := {}
  for row in expected do
    let fields ← arrayOf row (some 5)
    let name ← nameOf fields[0]! limits
    if seen.contains name then fail "INVENTORY_DUPLICATE_NAME"
    seen := seen.insert name
    names := names.push name
  return names

/-- Validate claims' shape/bounds, without constructing or trusting ConstantInfo. -/
def inventoryNodes (row : Json) (limits : Limits) : IO Nat := do
  let fields ← arrayOf row (some 5)
  let own ← nameOf fields[0]! limits
  discard <| paramsOf fields[2]! limits
  let mut used ← dagNodes fields[3]! limits
  let details ← arrayOf fields[4]!
  match ← natOf fields[1]! with
  | 1 =>
      discard <| arrayOf fields[4]! (some 3)
      used ← chargeNodes used (← dagNodes details[0]! limits) limits
      discard <| hintOf details[1]!
      discard <| allOf details[2]! own limits
  | 2 =>
      discard <| arrayOf fields[4]! (some 2)
      used ← chargeNodes used (← dagNodes details[0]! limits) limits
      discard <| allOf details[1]! own limits
  | 3 =>
      discard <| arrayOf fields[4]! (some 3)
      used ← chargeNodes used (← dagNodes details[0]! limits) limits
      if ← boolOf details[1]! then fail "UNSAFE_INVENTORY"
      discard <| allOf details[2]! own limits
  | 4 =>
      discard <| arrayOf fields[4]! (some 8)
      discard <| u32Of details[0]!
      discard <| u32Of details[1]!
      discard <| allOf details[2]! own limits
      discard <| namesOf details[3]! limits.maxConstructors limits
      discard <| u32Of details[4]!
      discard <| boolOf details[5]!
      if ← boolOf details[6]! then fail "UNSAFE_INVENTORY"
      discard <| boolOf details[7]!
  | 5 =>
      discard <| arrayOf fields[4]! (some 5)
      discard <| nameOf details[0]! limits
      for i in [1, 2, 3] do discard <| u32Of details[i]!
      if ← boolOf details[4]! then fail "UNSAFE_INVENTORY"
  | 6 =>
      discard <| arrayOf fields[4]! (some 8)
      let group ← namesOf details[0]! limits.maxAll limits
      if group.isEmpty then fail "EMPTY_RECURSOR_GROUP"
      for i in [1, 2, 3, 4] do discard <| u32Of details[i]!
      let rules ← arrayOf details[5]!
      if rules.size > limits.maxConstructors then fail "RECURSOR_RULE_BOUND"
      for rawRule in rules do
        let rule ← arrayOf rawRule (some 3)
        discard <| nameOf rule[0]! limits
        discard <| u32Of rule[1]!
        used ← chargeNodes used (← dagNodes rule[2]! limits) limits
      discard <| boolOf details[6]!
      if ← boolOf details[7]! then fail "UNSAFE_INVENTORY"
  | _ => fail "EXTENSION_INVENTORY_KIND"
  return used

def encodeDescriptor (decl : Declaration) (limits : Limits := {}) : IO Json := do
  match decl with
  | .defnDecl d =>
      if d.safety != .safe then fail "UNSAFE_DEFINITION"
      return arr #[num 0, ← nameJson d.name limits, ← paramsJson d.levelParams limits,
        ← ExprCodec.encode d.levelParams d.type limits.expr,
        ← ExprCodec.encode d.levelParams d.value limits.expr,
        hintJson d.hints, ← allJson d.all d.name limits]
  | .thmDecl d =>
      return arr #[num 1, ← nameJson d.name limits, ← paramsJson d.levelParams limits,
        ← ExprCodec.encode d.levelParams d.type limits.expr,
        ← ExprCodec.encode d.levelParams d.value limits.expr, ← allJson d.all d.name limits]
  | .opaqueDecl d =>
      if d.isUnsafe then fail "UNSAFE_OPAQUE"
      return arr #[num 2, ← nameJson d.name limits, ← paramsJson d.levelParams limits,
        ← ExprCodec.encode d.levelParams d.type limits.expr,
        ← ExprCodec.encode d.levelParams d.value limits.expr, ← allJson d.all d.name limits]
  | .inductDecl params numParams types unsafeFlag =>
      if unsafeFlag || types.isEmpty || types.length > limits.maxTypes then fail "INDUCTIVE_GROUP_BOUND"
      let mut rows := #[]
      let mut count := 0
      let mut seen : Std.HashSet Name := {}
      for type in types do
        if seen.contains type.name then fail "GROUP_DUPLICATE_NAME"
        seen := seen.insert type.name
        let mut ctors := #[]
        for ctor in type.ctors do
          count := count + 1
          if count > limits.maxConstructors then fail "CONSTRUCTOR_COUNT"
          if seen.contains ctor.name then fail "GROUP_DUPLICATE_NAME"
          seen := seen.insert ctor.name
          ctors := ctors.push (arr #[← nameJson ctor.name limits,
            ← ExprCodec.encode params ctor.type limits.expr])
        rows := rows.push (arr #[← nameJson type.name limits,
          ← ExprCodec.encode params type.type limits.expr, arr ctors])
      return arr #[num 3, ← paramsJson params limits, ← boundedNat numParams, arr rows]
  | _ => fail "AXIOM_QUOT_OR_MUTUAL_UNSAFE_EXTENSION"

def descriptorNodes (value : Json) (limits : Limits) : IO Nat := do
  let parts ← arrayOf value
  if parts.isEmpty then fail "EMPTY_DESCRIPTOR"
  let tag ← natOf parts[0]!
  if tag == 3 then
    discard <| arrayOf value (some 4)
    discard <| paramsOf parts[1]! limits
    discard <| u32Of parts[2]!
    let types ← arrayOf parts[3]!
    if types.isEmpty || types.size > limits.maxTypes then fail "INDUCTIVE_GROUP_BOUND"
    let mut count := 0
    let mut used := 0
    for rawType in types do
      let type ← arrayOf rawType (some 3)
      discard <| nameOf type[0]! limits
      used ← chargeNodes used (← dagNodes type[1]! limits) limits
      let ctors ← arrayOf type[2]!
      count := count + ctors.size
      if count > limits.maxConstructors then fail "CONSTRUCTOR_COUNT"
      for rawCtor in ctors do
        let ctor ← arrayOf rawCtor (some 2)
        discard <| nameOf ctor[0]! limits
        used ← chargeNodes used (← dagNodes ctor[1]! limits) limits
    return used
  if tag > 2 then fail "EXTENSION_DESCRIPTOR_KIND"
  discard <| arrayOf value (some (if tag == 0 then 7 else 6))
  let own ← nameOf parts[1]! limits
  discard <| paramsOf parts[2]! limits
  let used ← chargeNodes (← dagNodes parts[3]! limits) (← dagNodes parts[4]! limits) limits
  if tag == 0 then
    discard <| hintOf parts[5]!
    discard <| allOf parts[6]! own limits
  else
    discard <| allOf parts[5]! own limits
  return used

def decodeDescriptor (allowed : Std.HashSet Name) (value : Json) (limits : Limits)
    : IO Declaration := do
  let parts ← arrayOf value
  if parts.isEmpty then fail "EMPTY_DESCRIPTOR"
  let tag ← natOf parts[0]!
  if tag == 3 then
    discard <| arrayOf value (some 4)
    let params ← paramsOf parts[1]! limits
    let numParams ← u32Of parts[2]!
    let rawTypes ← arrayOf parts[3]!
    if rawTypes.isEmpty || rawTypes.size > limits.maxTypes then fail "INDUCTIVE_GROUP_BOUND"
    let mut typeNames := #[]
    let mut groupAllowed := allowed
    let mut introduced : Std.HashSet Name := {}
    let mut constructorCount := 0
    for rawType in rawTypes do
      let fields ← arrayOf rawType (some 3)
      let name ← nameOf fields[0]! limits
      if allowed.contains name || introduced.contains name then fail "GROUP_NAME_OVERWRITE"
      introduced := introduced.insert name
      groupAllowed := groupAllowed.insert name
      typeNames := typeNames.push name
      let rawCtors ← arrayOf fields[2]!
      constructorCount := constructorCount + rawCtors.size
      if constructorCount > limits.maxConstructors then fail "CONSTRUCTOR_COUNT"
      for rawCtor in rawCtors do
        let ctor ← arrayOf rawCtor (some 2)
        let ctorName ← nameOf ctor[0]! limits
        if allowed.contains ctorName || introduced.contains ctorName then fail "GROUP_NAME_OVERWRITE"
        introduced := introduced.insert ctorName
    let mut types : Array InductiveType := #[]
    for i in [:rawTypes.size] do
      let fields ← arrayOf rawTypes[i]! (some 3)
      let type ← ExprCodec.decode params groupAllowed fields[1]! limits.expr
      let mut ctors : Array Constructor := #[]
      for rawCtor in ← arrayOf fields[2]! do
        let ctor ← arrayOf rawCtor (some 2)
        ctors := ctors.push {
          name := ← nameOf ctor[0]! limits
          type := ← ExprCodec.decode params groupAllowed ctor[1]! limits.expr }
      types := types.push { name := typeNames[i]!, type, ctors := ctors.toList }
    return .inductDecl params numParams types.toList false
  if tag > 2 then fail "EXTENSION_DESCRIPTOR_KIND"
  discard <| arrayOf value (some (if tag == 0 then 7 else 6))
  let name ← nameOf parts[1]! limits
  if allowed.contains name then fail "ORDINARY_NAME_OVERWRITE"
  let params ← paramsOf parts[2]! limits
  let type ← ExprCodec.decode params allowed parts[3]! limits.expr
  let body ← ExprCodec.decode params allowed parts[4]! limits.expr
  if tag == 0 then
    return .defnDecl {
      name, levelParams := params, type, value := body
      hints := ← hintOf parts[5]!, safety := .safe, all := ← allOf parts[6]! name limits }
  else if tag == 1 then
    return .thmDecl {
      name, levelParams := params, type, value := body
      all := ← allOf parts[5]! name limits }
  else
    return .opaqueDecl {
      name, levelParams := params, type, value := body
      isUnsafe := false, all := ← allOf parts[5]! name limits }

def decodeUnit (allowed : Std.HashSet Name) (packet : Json) (limits : Limits := {})
    : IO DecodedUnit := do
  let parts ← arrayOf packet (some 3)
  if (← jsonResult parts[0]!.getStr?) != unitFormat then fail "UNIT_FORMAT"
  let expected ← arrayOf parts[2]!
  let names ← expectedNames expected limits
  for name in names do
    if allowed.contains name then fail "INVENTORY_NAME_OVERWRITE"
  let mut nodes ← descriptorNodes parts[1]! limits
  for row in expected do nodes ← chargeNodes nodes (← inventoryNodes row limits) limits
  let decl ← decodeDescriptor allowed parts[1]! limits
  if (← encodeDescriptor decl limits) != parts[1]! then fail "NONCANONICAL_DESCRIPTOR"
  match decl with
  | .defnDecl _ | .thmDecl _ | .opaqueDecl _ =>
      if names.size != 1 || names[0]! != decl.getTopLevelNames.head! then fail "ORDINARY_INVENTORY_CENSUS"
  | .inductDecl _ _ types _ =>
      for type in types do
        if !names.contains type.name then fail "GROUP_INVENTORY_MISSING_TYPE"
        for ctor in type.ctors do
          if !names.contains ctor.name then fail "GROUP_INVENTORY_MISSING_CONSTRUCTOR"
  | _ => fail "EXTENSION_DESCRIPTOR_KIND"
  return { decl, expected }

def encodeUnit (decl : Declaration) (inventory : Array ConstantInfo) (limits : Limits := {})
    : IO Json := do
  if inventory.isEmpty || inventory.size > limits.maxInventory then fail "INVENTORY_COUNT"
  let descriptor ← encodeDescriptor decl limits
  let mut expected := #[]
  for info in inventory do expected := expected.push (← inventoryRow info limits)
  discard <| expectedNames expected limits
  let mut nodes ← descriptorNodes descriptor limits
  for row in expected do nodes ← chargeNodes nodes (← inventoryNodes row limits) limits
  return arr #[Json.str unitFormat, descriptor, arr expected]

end OrdinaryLean.DeclCodec
