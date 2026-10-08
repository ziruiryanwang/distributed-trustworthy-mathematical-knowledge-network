import BootstrapSupport

open Lean BootstrapProbe

namespace SourceComposition

def objectField (j : Json) (key : String) : IO Json := do
  let o ← jsonResult j.getObj?
  let some x := o.get? key | fail s!"MISSING_PLAN_FIELD field={key}"
  return x

def commonRoots : Array Name :=
  #[``Subtype, ``Subtype.val, ``Subtype.property, ``Function.Injective, ``Subtype.ext]

def roleRoots (role : String) : IO (Name × Array Name) := do
  match role with
  | "interface" => return (`Init, commonRoots)
  | "A" => return (`ProducerA, commonRoots.push `SharedSubtypeA.val_injective)
  | "B" => return (`ProducerB, commonRoots ++ #[`SharedSubtypeB.map, `SharedSubtypeB.map_val])
  | "marked" => return (`MarkedSubtypeControl, commonRoots ++
      #[`ControlSubtype.MarkedSubtype, `ControlSubtype.map, `ControlSubtype.map_val])
  | "B2" => return (`ProducerB2, commonRoots ++ #[`SharedSubtypeB2.map, `SharedSubtypeB2.map_val])
  | _ => fail "CAPTURE_ROLE_EXPECTED_interface_A_B_marked_B2"

def seedNameSet (seed : Json) : IO (Std.HashSet Name) := do
  let a ← arrayOf seed (some 3)
  let mut out : Std.HashSet Name := {}
  for n in ← namesOf a[2]! do out := out.insert n
  return out

def collectExtension (src : Kernel.Environment) (seedNames : Std.HashSet Name)
    (selected : Array Name) : IO (Array UnitInfo) := do
  let members ← groupMembers src
  let mut todo := selected
  let mut pos := 0
  let mut seen : Std.HashSet Name := {}
  let mut units : Array UnitInfo := #[]
  let mut exports := 0
  while pos < todo.size do
    let n := todo[pos]!
    pos := pos + 1
    if seedNames.contains n then continue
    let key ← owner src n
    if seedNames.contains key then fail s!"UNCAPTURED_MEMBER_OF_SEED_GROUP name={n}"
    if seen.contains key then continue
    let unit ← makeUnit src members key
    match unit.decl with
    | .axiomDecl _ | .quotDecl => fail "EXTERNAL_AXIOM_OR_QUOTIENT_PROHIBITED"
    | _ => pure ()
    for member in unit.emitted do
      let c ← lookup src member
      if let .inductInfo i := c then
        if i.numNested != 0 then fail "INITIAL_EXTERNAL_NESTED_GROUP_UNSUPPORTED"
    if !unit.strLits.isEmpty then fail "INITIAL_EXTERNAL_STRING_LITERAL_UNSUPPORTED"
    seen := seen.insert key
    units := units.push unit
    exports := exports + unit.emitted.size
    if units.size > 256 || exports > 1024 then fail "EXTENSION_COUNT_LIMIT"
    todo := todo ++ unit.refs
  let sorted := units.toList.mergeSort (fun a b => bytesLT (nameBytes (unitName a)) (nameBytes (unitName b)))
  let mut remaining := sorted
  let mut done := seedNames
  let mut result : Array UnitInfo := #[]
  while !remaining.isEmpty do
    let some next := remaining.find? (fun u => u.edges.all (fun e => done.contains e.dep))
      | fail "EXTERNAL_SUPPORT_CYCLE_OR_MISSING_MEMBER"
    done := done.insert next.key
    for n in next.emitted do done := done.insert n
    result := result.push next
    remaining := remaining.filter (fun u => u.key != next.key)
  return result

def captureUnitsJson (src : Kernel.Environment) (units : Array UnitInfo) : IO Json := do
  let mut rows := #[]
  for unit in units do
    let mut inventory := #[]
    let mut inventoryUniverses := #[]
    let names := unit.emitted.toList.mergeSort (fun a b => bytesLT (nameBytes a) (nameBytes b))
    for n in names do
      let c ← lookup src n
      inventory := inventory.push (← inventoryRow c (if c.isDefinition then some 0 else none))
      inventoryUniverses := inventoryUniverses.push (← namesJson c.levelParams)
    let base ← lookup src unit.key
    rows := rows.push <| Json.mkObj [
      ("key", ← nameJson unit.key),
      ("descriptor", ← descriptorJson unit.decl),
      ("inventory", jarr inventory),
      ("universeNames", ← namesJson base.levelParams),
      ("inventoryUniverseNames", jarr inventoryUniverses)]
  return jarr rows

def capture (role : String) (seed : Json) : IO Unit := do
  let (moduleName, selected) ← roleRoots role
  Lean.initSearchPath (← Lean.findSysroot)
  let source ← Lean.importModules #[{ module := moduleName }] {} 0
    (plugins := #[]) (loadExts := false) (level := .private)
  let src := source.toKernelEnv
  if role == "A" && (src.find? `SharedSubtypeB.map).isSome then fail "A_SOURCE_SEES_B"
  if role == "B" && (src.find? `SharedSubtypeA.val_injective).isSome then fail "B_SOURCE_SEES_A"
  if role == "B2" && (src.find? `SharedSubtypeA.val_injective).isSome then fail "B2_SOURCE_SEES_A"
  if role == "B2" && (src.find? `SharedSubtypeB.map).isSome then fail "B2_SOURCE_SEES_B1"
  let seedNames ← seedNameSet seed
  let units ← collectExtension src seedNames selected
  if role == "A" then
    let own ← collectExtension src seedNames #[`SharedSubtypeA.val_injective]
    if own.any (fun u => u.key == ``Subtype.ext) then fail "A_SOURCE_USED_STANDARD_EXT"
  let output := Json.mkObj [("schema", jnat 1), ("roots", ← namesJson selected.toList),
    ("units", ← captureUnitsJson src units)]
  emit s!"SOURCE_CAPTURE role={role} module={moduleName} units={units.size} sourceImportAuthority=false"
  emit s!"SOURCE_CAPTURE_JSON {output.compress}"

def cidBytes (j : Json) (expectedType expectedSchema : Nat) : IO (List UInt8) := do
  let a ← arrayOf j (some 4)
  if (← natOf a[0]!) != 1 || (← natOf a[1]!) != expectedType ||
      (← natOf a[2]!) != expectedSchema then fail "CID_KIND_SCHEMA"
  let digest ← bytesOf a[3]!
  if digest.size != 32 then fail "CID_DIGEST_LENGTH"
  return cborHead 4 4 ++ cborHead 0 1 ++ cborHead 0 expectedType ++
    cborHead 0 expectedSchema ++ cborHead 2 32 ++ digest.data.toList

def hexDigit (n : Nat) : Char := Char.ofNat (if n < 10 then 48+n else 87+n)
def hexBytes (bs : List UInt8) : String :=
  String.ofList (bs.flatMap (fun b => [hexDigit (b.toNat/16), hexDigit (b.toNat%16)]))

def idName (component : String) (id : Json) (tag schema : Nat) : IO Name := do
  let bytes ← cidBytes id tag schema
  return Name.str (Name.str (Name.str .anonymous "DTMKN") component) (hexBytes bytes)

def groupName (id : Json) (index : Nat) : IO Name := do
  checkU32 "groupTypeIndex" index
  return Name.str (← idName "i" id 0x18 2) s!"t{index}"

def ordinaryName (kind : Nat) (id : Json) : IO Name := do
  match kind with
  | 0 => idName "d" id 0x11 2
  | 1 => idName "w" id 0x23 1
  | 2 => idName "o" id 0x19 2
  | 4 => idName "j" id 0x13 2
  | _ => fail "ORDINARY_KIND"

abbrev Bindings := Std.HashMap Name Json

def referenceName (seedNames : Array Name) (r : Json) : IO Name := do
  let a ← arrayOf r
  if a.isEmpty then fail "EMPTY_REFERENCE"
  match ← natOf a[0]! with
  | 0 =>
      discard <| arrayOf r (some 2)
      return seedNames[(← nodeIndex a[1]! seedNames.size)]!
  | 1 => discard <| arrayOf r (some 2); idName "d" a[1]! 0x11 2
  | 2 => discard <| arrayOf r (some 2); idName "j" a[1]! 0x13 2
  | 4 => discard <| arrayOf r (some 2); idName "o" a[1]! 0x19 2
  | 7 => discard <| arrayOf r (some 2); idName "w" a[1]! 0x23 1
  | 3 =>
      discard <| arrayOf r (some 3)
      let sel ← arrayOf a[2]!
      if sel.isEmpty then fail "EMPTY_GROUP_SELECTOR"
      match ← natOf sel[0]! with
      | 0 =>
          discard <| arrayOf a[2]! (some 2)
          groupName a[1]! (← u32Of sel[1]!)
      | 1 =>
          discard <| arrayOf a[2]! (some 3)
          return Name.str (← groupName a[1]! (← u32Of sel[1]!)) s!"c{← u32Of sel[2]!}"
      | 2 =>
          discard <| arrayOf a[2]! (some 2)
          return Name.str (← groupName a[1]! (← u32Of sel[1]!)) "rec"
      | _ => fail "INITIAL_NESTED_OR_UNKNOWN_SELECTOR"
  | _ => fail "UNSUPPORTED_EXTERNAL_REFERENCE"

def resolveReference (seedNames : Array Name) (bindings : Bindings)
    (localTypes : Array Name) (witness : Bool) (r : Json) : IO Name := do
  let a ← arrayOf r
  if a.isEmpty then fail "EMPTY_REFERENCE"
  let tag ← natOf a[0]!
  if tag == 5 then
    discard <| arrayOf r (some 2)
    if witness then fail "LOCAL_GROUP_REFERENCE_IN_WITNESS"
    return localTypes[(← nodeIndex a[1]! localTypes.size)]!
  if tag == 7 && !witness then fail "PROOF_INSTANCE_IN_SEMANTIC_TERM"
  if tag == 2 && witness then fail "SEMANTIC_THEOREM_IN_WITNESS_TERM"
  let n ← referenceName seedNames r
  let some expected := bindings[n]? | fail s!"UNCHECKED_REFERENCE name={n}"
  if expected != r then fail "REFERENCE_NAME_BINDING"
  return n

def expandDag (seedNames : Array Name) (bindings : Bindings) (localTypes : Array Name)
    (witness : Bool) (j : Json) : IO Json := do
  let a ← arrayOf j (some 3)
  let nodes ← arrayOf a[1]!
  if nodes.isEmpty || nodes.size > 65536 || (← arrayOf a[0]!).size > 4096 then fail "ORDINARY_DAG_LIMIT"
  let mut out := #[]
  for node in nodes do
    let p ← arrayOf node
    if p.isEmpty then fail "EMPTY_EXPRESSION_NODE"
    let tag ← natOf p[0]!
    let mapped ← match tag with
      | 0 | 1 | 3 | 6 | 7 | 9 => pure node
      | 2 => do
          discard <| arrayOf node (some 3)
          let n ← resolveReference seedNames bindings localTypes witness p[1]!
          pure <| jarr #[jnat 2, jarr #[jnat 6, ← nameJson n], p[2]!]
      | 4 | 5 => do
          discard <| arrayOf node (some 3)
          pure <| jarr #[jnat tag, jnat 0, p[1]!, p[2]!]
      | 8 => do
          discard <| arrayOf node (some 4)
          let ref ← arrayOf p[1]!
          if ref.isEmpty then fail "EMPTY_PROJECTION_REFERENCE"
          let rt ← natOf ref[0]!
          if rt != 0 && rt != 3 then fail "PROJECTION_REFERENCE_KIND"
          if rt == 3 then
            discard <| arrayOf p[1]! (some 3)
            let sel ← arrayOf ref[2]! (some 2)
            if (← natOf sel[0]!) != 0 then fail "PROJECTION_REQUIRES_TYPE_SELECTOR"
          let n ← resolveReference seedNames bindings #[] false p[1]!
          pure <| jarr #[jnat 8, jarr #[jnat 6, ← nameJson n], p[2]!, p[3]!]
      | _ => fail "ORDINARY_EXPR_TAG"
    out := out.push mapped
  return jarr #[a[0]!, jarr out, a[2]!]

partial def normalizeExpr (e : Expr) : Expr :=
  match e with
  | .app f a => .app (normalizeExpr f) (normalizeExpr a)
  | .lam _ t b _ => .lam .anonymous (normalizeExpr t) (normalizeExpr b) .default
  | .forallE _ t b _ => .forallE .anonymous (normalizeExpr t) (normalizeExpr b) .default
  | .letE _ t v b _ => .letE .anonymous (normalizeExpr t) (normalizeExpr v) (normalizeExpr b) false
  | .mdata _ b => normalizeExpr b
  | .proj n i b => .proj n i (normalizeExpr b)
  | _ => e

def normalizedInfo (c : ConstantInfo) : ConstantInfo :=
  match c with
  | .axiomInfo d => .axiomInfo { d with type := normalizeExpr d.type }
  | .defnInfo d => .defnInfo { d with type := normalizeExpr d.type, value := normalizeExpr d.value }
  | .thmInfo d => .thmInfo { d with type := normalizeExpr d.type, value := normalizeExpr d.value }
  | .opaqueInfo d => .opaqueInfo { d with type := normalizeExpr d.type, value := normalizeExpr d.value }
  | .inductInfo d => .inductInfo { d with type := normalizeExpr d.type }
  | .ctorInfo d => .ctorInfo { d with type := normalizeExpr d.type }
  | .recInfo d => .recInfo { d with
      type := normalizeExpr d.type
      rules := d.rules.map (fun r => { r with rhs := normalizeExpr r.rhs }) }
  | .quotInfo d => .quotInfo { d with type := normalizeExpr d.type }

def exportDag (bindings : Bindings) (localTypes : Array Name) (witness : Bool)
    (params : List Name) (e : Expr) : IO Json := do
  let a ← arrayOf (← dagJson params (normalizeExpr e)) (some 3)
  let mut out := #[]
  for node in ← arrayOf a[1]! do
    let p ← arrayOf node
    let tag ← natOf p[0]!
    let mapped ← match tag with
      | 2 | 8 => do
          let raw ← arrayOf p[1]! (some 2)
          if (← natOf raw[0]!) != 6 then fail "ACTUAL_NAME_REFERENCE_EXPECTED"
          let n ← nameOf raw[1]!
          let ref ← match localTypes.toList.idxOf? n with
            | some i =>
                if tag == 8 then fail "GROUP_LOCAL_PROJECTION_UNSUPPORTED"
                pure <| jarr #[jnat 5, jnat i]
            | none => do
                let some r := bindings[n]? | fail s!"ACTUAL_REFERENCE_UNBOUND name={n}"
                pure r
          let rr ← arrayOf ref
          let rt ← natOf rr[0]!
          if rt == 7 && !witness then fail "ACTUAL_INSTANCE_IN_SEMANTIC_TERM"
          if rt == 2 && witness then fail "ACTUAL_SEMANTIC_THEOREM_IN_WITNESS"
          if tag == 2 then pure <| jarr #[jnat 2, ref, p[2]!]
          else pure <| jarr #[jnat 8, ref, p[2]!, p[3]!]
      | 4 | 5 => pure <| jarr #[jnat tag, p[2]!, p[3]!]
      | _ => pure node
    out := out.push mapped
  return jarr #[a[0]!, jarr out, a[2]!]

structure Receiving where
  env : Lean.Environment
  seedNames : Array Name
  bindings : Bindings
  actual : Array Json := #[]

def checkedAdd (env : Lean.Environment) (d : Declaration) : IO Lean.Environment := do
  let d ← withHeight env.toKernelEnv d
  match env.addDeclCore 20000000 10000 d none (doCheck := true) with
  | .ok next => return next
  | .error ex =>
      fail s!"EXTENSION_NATIVE_REJECTED detail={← (ex.toMessageData {}).toString}"

def allowedNames (bindings : Bindings) (extras : Array Name := #[]) : Std.HashSet Name := Id.run do
  let mut out : Std.HashSet Name := {}
  for (n, _) in bindings.toArray do out := out.insert n
  for n in extras do out := out.insert n
  return out

def receiveOrdinary (state : Receiving) (row : Json) : IO Receiving := do
  let kind ← natOf (← objectField row "kind")
  let id ← objectField row "id"
  let u ← u32Of (← objectField row "u")
  if u > 64 then fail "ORDINARY_UNIVERSE_ARITY_LIMIT"
  let params ← indexedParams u
  let n ← ordinaryName kind id
  if (state.env.toKernelEnv.find? n).isSome || state.bindings.contains n then fail "ORDINARY_OVERWRITE"
  let witness := kind == 1 || kind == 4
  let allowed := allowedNames state.bindings
  let ty ← decodeDag params allowed (← expandDag state.seedNames state.bindings #[] false (← objectField row "type"))
  let value ← decodeDag params allowed (← expandDag state.seedNames state.bindings #[] witness (← objectField row "value"))
  let decl ← match kind with
    | 0 => pure <| Declaration.defnDecl { name := n, levelParams := params, type := ty, value, hints := .regular 0, safety := .safe }
    | 1 | 4 => pure <| Declaration.thmDecl { name := n, levelParams := params, type := ty, value }
    | 2 => pure <| Declaration.opaqueDecl { name := n, levelParams := params, type := ty, value, isUnsafe := false }
    | _ => fail "ORDINARY_KIND"
  let before := state.env.toKernelEnv.constants.toList.length
  emit s!"SOURCE_NATIVE_CHECK_BEGIN name={n} kind={kind} universes={u}"
  let env ← checkedAdd state.env decl
  if env.toKernelEnv.constants.toList.length != before+1 then fail "ORDINARY_GENERATED_COUNT"
  let c ← lookup env.toKernelEnv n
  if c.levelParams != params then fail "ORDINARY_UNIVERSE_ORDER_CHANGED"
  let some body := c.value? (allowOpaque := true) | fail "ACTUAL_BODY_MISSING"
  let actual := Json.mkObj [("kind", jnat kind), ("id", id), ("u", jnat u),
    ("type", ← exportDag state.bindings #[] false c.levelParams c.type),
    ("value", ← exportDag state.bindings #[] witness c.levelParams body)]
  let rt := if kind == 0 then 1 else if kind == 1 then 7 else if kind == 2 then 4 else 2
  let bindings := state.bindings.insert n (jarr #[jnat rt, id])
  emit s!"SOURCE_NATIVE_CHECK_OK name={n}"
  return { state with env, bindings, actual := state.actual.push actual }

def receiveGroup (state : Receiving) (row : Json) : IO Receiving := do
  let id ← objectField row "id"
  discard <| cidBytes id 0x18 2
  let u ← u32Of (← objectField row "u")
  if u > 64 then fail "GROUP_UNIVERSE_ARITY_LIMIT"
  let params ← indexedParams u
  let numParams ← u32Of (← objectField row "numParams")
  let types ← arrayOf (← objectField row "types")
  if types.isEmpty || types.size > 16 then fail "GROUP_TYPE_COUNT_LIMIT"
  let mut typeNames : Array Name := #[]
  for i in [:types.size] do typeNames := typeNames.push (← groupName id i)
  let allowed := allowedNames state.bindings typeNames
  let mut nativeTypes : List InductiveType := []
  for i in [:types.size] do
    let pair ← arrayOf types[i]! (some 2)
    let ty ← decodeDag params allowed (← expandDag state.seedNames state.bindings typeNames false pair[0]!)
    let constructors ← arrayOf pair[1]!
    if constructors.size > 32 then fail "GROUP_CONSTRUCTOR_COUNT_LIMIT"
    let mut ctors : List Constructor := []
    for k in [:constructors.size] do
      let cn := Name.str typeNames[i]! s!"c{k}"
      if (state.env.toKernelEnv.find? cn).isSome then fail "GROUP_CONSTRUCTOR_OVERWRITE"
      let cty ← decodeDag params allowed (← expandDag state.seedNames state.bindings typeNames false constructors[k]!)
      ctors := ctors ++ [{ name := cn, type := cty }]
    if (state.env.toKernelEnv.find? typeNames[i]!).isSome then fail "GROUP_TYPE_OVERWRITE"
    nativeTypes := nativeTypes ++ [{ name := typeNames[i]!, type := ty, ctors }]
  let before := state.env.toKernelEnv
  emit s!"SOURCE_GROUP_CHECK_BEGIN types={types.size} universes={u}"
  let env ← checkedAdd state.env (.inductDecl params numParams nativeTypes false)
  let added := env.toKernelEnv.constants.toList.filter (fun (n, _) => (before.find? n).isNone)
  let mut bindings := state.bindings
  for (n, c) in added do
    let sel ← match c with
      | .inductInfo info => do
          if info.numNested != 0 || info.levelParams != params then fail "UNEXPECTED_GROUP_SHAPE_OR_UNIVERSES"
          let some i := typeNames.toList.idxOf? n | fail "UNEXPECTED_GROUP_TYPE"
          pure <| jarr #[jnat 0, jnat i]
      | .ctorInfo info => do
          let some i := typeNames.toList.idxOf? info.induct | fail "UNEXPECTED_CONSTRUCTOR_OWNER"
          if n != Name.str typeNames[i]! s!"c{info.cidx}" then fail "UNEXPECTED_CONSTRUCTOR_NAME"
          pure <| jarr #[jnat 1, jnat i, jnat info.cidx]
      | .recInfo _ => do
          let some i := typeNames.toList.findIdx? (fun tn => Name.str tn "rec" == n)
            | fail "UNSUPPORTED_NESTED_OR_EXTRA_RECURSOR"
          pure <| jarr #[jnat 2, jnat i]
      | _ => fail "UNEXPLAINED_GROUP_GENERATION"
    if bindings.contains n then fail "GROUP_BINDING_OVERWRITE"
    bindings := bindings.insert n (jarr #[jnat 3, id, sel])
  let expected ← arrayOf (← objectField row "inventory")
  if expected.size != added.length then fail "GROUP_INVENTORY_COUNT"
  let mut seen : Std.HashSet Name := {}
  let mut actualInventory := #[]
  for wanted in expected do
    let wr ← arrayOf wanted (some 5)
    let n ← nameOf wr[0]!
    if seen.contains n || (before.find? n).isSome then fail "GROUP_INVENTORY_DUPLICATE_OR_PREEXISTING"
    if !(added.any (fun a => a.1 == n)) then fail "GROUP_INVENTORY_UNGENERATED_NAME"
    let actual ← inventoryRow (normalizedInfo (← lookup env.toKernelEnv n))
    if actual != wanted then fail s!"GROUP_GENERATED_CORRESPONDENCE_MISMATCH name={n}"
    actualInventory := actualInventory.push actual
    seen := seen.insert n
  let mut actualTypes := #[]
  for tn in typeNames do
    let .inductInfo info ← lookup env.toKernelEnv tn | fail "ACTUAL_GROUP_KIND"
    let mut constructors := #[]
    for cn in info.ctors do
      let ci ← lookup env.toKernelEnv cn
      constructors := constructors.push (← exportDag bindings typeNames false ci.levelParams ci.type)
    actualTypes := actualTypes.push (jarr #[← exportDag bindings typeNames false info.levelParams info.type, jarr constructors])
  let actual := Json.mkObj [("kind", jnat 3), ("id", id), ("u", jnat u),
    ("numParams", jnat numParams), ("types", jarr actualTypes), ("inventory", jarr actualInventory)]
  emit s!"SOURCE_GROUP_CHECK_OK generated={added.length} sourceCorrespondence=true"
  return { state with env, bindings, actual := state.actual.push actual }

def receive (plan inventory : Json) : IO Receiving := do
  emit "SOURCE_RECEIVER_BOUNDARY peerInputAPI=false trustedLocalCanonicalBridge=true sourceImport=false"
  let seed ← objectField plan "seed"
  discard <| cidBytes (← objectField plan "foundation") 0x1 2
  let replays ← arrayOf (← objectField plan "replays")
  if replays.isEmpty || replays.size > 256 then fail "SOURCE_REPLAY_ROOT_LIMIT"
  for replay in replays do discard <| cidBytes replay 0x15 3
  let env ← receiveSeed seed inventory
  let sa ← arrayOf seed (some 3)
  let seedNames := (← namesOf sa[2]!).toArray
  let mut bindings : Bindings := {}
  for i in [:seedNames.size] do bindings := bindings.insert seedNames[i]! (jarr #[jnat 0, jnat i])
  let mut state : Receiving := { env, seedNames, bindings }
  let batch ← arrayOf (← objectField plan "batch")
  if batch.size > 256 then fail "SOURCE_BATCH_LIMIT"
  for row in batch do
    let kind ← natOf (← objectField row "kind")
    state ← if kind == 3 then receiveGroup state row else receiveOrdinary state row
    if state.env.toKernelEnv.constants.toList.length > seedNames.size+1024 then fail "SOURCE_EXPORT_COUNT_LIMIT"
  let actual := Json.mkObj [("foundation", ← objectField plan "foundation"),
    ("replays", jarr replays), ("batch", jarr state.actual)]
  emit s!"ACTUAL_BATCH_JSON {actual.compress}"
  return state

def consume (plan inventory : Json) (templatePath : String) : IO Unit := do
  let state ← receive plan inventory
  let presentation ← objectField plan "presentation"
  let fields : Array (String × String) := #[
    ("subtype", "__SUBTYPE__"), ("val", "__VAL__"), ("injective", "__INJECTIVE__"),
    ("a", "__A__"), ("map", "__MAP__"), ("law", "__LAW__")]
  let mut text ← IO.FS.readFile (System.FilePath.mk templatePath)
  if text.utf8ByteSize > 65536 then fail "CONSUMER_SOURCE_LIMIT"
  let mut used : Array Name := #[]
  for (field, token) in fields do
    let ref ← objectField presentation field
    let n ← referenceName state.seedNames ref
    let some expected := state.bindings[n]? | fail "PRESENTATION_UNCHECKED_REFERENCE"
    if expected != ref then fail "PRESENTATION_BINDING_MISMATCH"
    if !text.contains token then fail s!"MISSING_TEMPLATE_TOKEN field={field}"
    text := text.replace token n.toString
    used := used.push n
  emit s!"CONSUMER_SOURCE_JSON {(Json.str text).compress}"
  let options := ({} : Options).set `maxRecDepth (10000 : Nat)
    |>.set `maxHeartbeats (20000000 : Nat)
  let before := state.env.toKernelEnv
  let (full, messages) ← Lean.Elab.process text state.env options (some templatePath)
  if messages.hasErrors then
    for msg in messages.toList do emit s!"CONSUMER_FRONTEND_MESSAGE {← msg.toString}"
    fail "CONSUMER_SOURCE_ELABORATION_REJECTED"
  let actual := full.toKernelEnv
  let n := `SharedSubtypeConsumer.exists_injective_lift
  let c ← lookup actual n
  screen c
  if !c.isTheorem || c.levelParams.length != 2 then fail "CONSUMER_KIND_OR_UNIVERSE_SPECIALIZATION"
  let some body := c.value? (allowOpaque := true) | fail "CONSUMER_COMPLETED_BODY_MISSING"
  let refs ← scanExpr body
  for i in [3,4,5] do
    if !refs.refs.contains used[i]! then fail "CONSUMER_DID_NOT_USE_SELECTED_CONTRIBUTION"
    emit s!"CONSUMER_ACTUAL_DEPENDENCY name={used[i]!}"
  let known := allowedNames state.bindings
  let units ← collectExtension actual known #[n]
  let added := actual.constants.toList.filter (fun (name, _) => (before.find? name).isNone)
  let exported := units.foldl (fun total u => total+u.emitted.size) 0
  if added.length != exported then fail "CONSUMER_UNCAPTURED_FRONTEND_DECLARATIONS"
  let output := Json.mkObj [("schema", jnat 1), ("roots", ← namesJson [n]),
    ("units", ← captureUnitsJson actual units)]
  emit s!"CONSUMER_CHECKED sourceImport=false newDeclarations={added.length} universes={c.levelParams.length}"
  emit s!"SOURCE_CAPTURE_JSON {output.compress}"

def consumeR1 (plan inventory : Json) (templatePath : String) : IO Unit := do
  let state ← receive plan inventory
  let presentation ← objectField plan "presentation"
  let fields : Array (String × String) := #[
    ("subtype", "__SUBTYPE__"), ("val", "__VAL__"),
    ("map", "__MAP__"), ("other", "__OTHER__")]
  let mut text ← IO.FS.readFile (System.FilePath.mk templatePath)
  if text.utf8ByteSize > 65536 then fail "R1_CONSUMER_SOURCE_LIMIT"
  let mut used : Array Name := #[]
  for (field, token) in fields do
    let ref ← objectField presentation field
    let ra ← arrayOf ref
    if ra.isEmpty then fail "R1_PRESENTATION_EMPTY_REFERENCE"
    let expectedTag := if field == "subtype" then 3 else if field == "other" then 7 else 1
    if (← natOf ra[0]!) != expectedTag then fail s!"R1_PRESENTATION_REFERENCE_KIND field={field}"
    let n ← referenceName state.seedNames ref
    let some expected := state.bindings[n]? | fail "R1_PRESENTATION_UNCHECKED_REFERENCE"
    if expected != ref then fail "R1_PRESENTATION_BINDING_MISMATCH"
    if !text.contains token then fail s!"R1_MISSING_TEMPLATE_TOKEN field={field}"
    text := text.replace token n.toString
    used := used.push n
  emit s!"CONSUMER_SOURCE_JSON {(Json.str text).compress}"
  let options := ({} : Options).set `maxRecDepth (10000 : Nat)
    |>.set `maxHeartbeats (20000000 : Nat)
  let before := state.env.toKernelEnv
  let (full, messages) ← Lean.Elab.process text state.env options (some templatePath)
  if messages.hasErrors then
    for msg in messages.toList do emit s!"R1_CONSUMER_FRONTEND_MESSAGE {← msg.toString}"
    fail "R1_CONSUMER_SOURCE_ELABORATION_REJECTED"
  let actual := full.toKernelEnv
  let n := `ReconciledSubtypeConsumer.map_property
  let c ← lookup actual n
  screen c
  if !c.isTheorem || c.levelParams.length != 2 then fail "R1_CONSUMER_KIND_OR_UNIVERSE_SPECIALIZATION"
  let some body := c.value? (allowOpaque := true) | fail "R1_CONSUMER_COMPLETED_BODY_MISSING"
  let typeRefs ← scanExpr c.type
  let bodyRefs ← scanExpr body
  if !typeRefs.refs.contains used[2]! then fail "R1_CONSUMER_TYPE_DOES_NOT_USE_SHARED_MAP"
  if !bodyRefs.refs.contains used[3]! then fail "R1_CONSUMER_BODY_DOES_NOT_USE_OTHER_INSTANCE"
  emit s!"R1_CONSUMER_ACTUAL_TYPE_DEPENDENCY name={used[2]!}"
  emit s!"R1_CONSUMER_ACTUAL_BODY_DEPENDENCY name={used[3]!}"
  let known := allowedNames state.bindings
  let units ← collectExtension actual known #[n]
  let added := actual.constants.toList.filter (fun (name, _) => (before.find? name).isNone)
  let exported := units.foldl (fun total u => total+u.emitted.size) 0
  if added.length != exported then fail "R1_CONSUMER_UNCAPTURED_FRONTEND_DECLARATIONS"
  let output := Json.mkObj [("schema", jnat 1), ("roots", ← namesJson [n]),
    ("units", ← captureUnitsJson actual units)]
  emit s!"R1_CONSUMER_CHECKED sourceImport=false newDeclarations={added.length} universes={c.levelParams.length}"
  emit s!"SOURCE_CAPTURE_JSON {output.compress}"

def run (args : List String) : IO UInt32 := do
  match args with
  | ["--capture", role, "--seed", path] =>
      capture role (← readProjection path)
      return 0
  | ["--receive", path, "--inventory", inventoryPath] =>
      discard <| receive (← readProjection path) (← readProjection inventoryPath)
      return 0
  | ["--consume", path, "--inventory", inventoryPath, "--template", templatePath] =>
      consume (← readProjection path) (← readProjection inventoryPath) templatePath
      return 0
  | ["--consume-r1", path, "--inventory", inventoryPath, "--template", templatePath] =>
      consumeR1 (← readProjection path) (← readProjection inventoryPath) templatePath
      return 0
  | _ => fail "USAGE --capture ROLE --seed PATH | --receive PLAN --inventory INVENTORY | --consume PLAN --inventory INVENTORY --template TEMPLATE | --consume-r1 PLAN --inventory INVENTORY --template TEMPLATE"

end SourceComposition
