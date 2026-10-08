import Lean

/- Isolated support copy from the predecessor Bootstrap.lean cut
0AC74094017D17F4F0252215B456170B2406C73E33936A5F1DCEC7C557F2E2E5.
Only the local seed receiver return/wrapper path is adapted here.
Predecessor files and preserved experiments remain unchanged. -/

/-
Bounded BOOT1 source-record feasibility probe, not a canonical codec or FoundationID.
Producer import is isolated from receiver reconstruction. The receiver is genuinely empty
and receives only Declaration values through Kernel.Environment.addDeclCore.
Root controls invocation, wall time, memory, log capture and runtime-byte binding.
-/

open Lean

namespace BootstrapProbe

def roots : Array Name := #[
  ``True, ``False, ``Eq, ``Nat, ``Bool, ``List, ``Iff, ``Nonempty,
  ``propext, ``Classical.choice, ``Quot.sound,
  ``Quot, ``Quot.mk, ``Quot.lift, ``Quot.ind,
  ``Nat.zero, ``Nat.succ, ``Bool.false, ``Bool.true,
  ``Nat.add, ``Nat.sub, ``Nat.mul, ``Nat.pow, ``Nat.gcd, ``Nat.div, ``Nat.mod,
  ``Nat.beq, ``Nat.ble, ``Nat.land, ``Nat.lor, ``Nat.xor, ``Nat.shiftLeft,
  ``Nat.shiftRight, ``String, ``String.ofByteArray, ``String.ofList,
  ``Char, ``Char.ofNat, ``List.nil, ``List.cons,
  ``outParam, ``semiOutParam, ``optParam, ``autoParam, ``eagerReduce]

def stringRoots : Array Name :=
  #[``String, ``String.ofList, ``Char, ``Char.ofNat, ``List.nil, ``List.cons]

def allowedAxioms : Array Name := #[``propext, ``Classical.choice, ``Quot.sound]
def quotNames : Array Name := #[``Quot, ``Quot.mk, ``Quot.lift, ``Quot.ind]

def fail {α : Type} (s : String) : IO α := throw <| IO.userError s

def emit (s : String) : IO Unit := do
  let out ← IO.getStdout
  out.putStrLn s
  out.flush

class RecordSource (σ : Type) where
  findRecord : σ → Name → Option ConstantInfo
  records : σ → Array (Name × ConstantInfo)

instance : RecordSource Kernel.Environment where
  findRecord := Kernel.Environment.find?
  records src := src.constants.toList.toArray

structure InventoryData where
  entries : Std.HashMap Name ConstantInfo := {}

instance : RecordSource InventoryData where
  findRecord src n := src.entries[n]?
  records src := src.entries.toArray

def lookup {σ : Type} [RecordSource σ] (src : σ) (n : Name) : IO ConstantInfo :=
  match RecordSource.findRecord src n with
  | some c => pure c
  | none => fail s!"MISSING_SOURCE_RECORD name={n}"

def rootComponent : Name → Name
  | .anonymous => .anonymous
  | n@(.str .anonymous _) => n
  | n@(.num .anonymous _) => n
  | .str p _ | .num p _ => rootComponent p

def forbidden (n : Name) : Bool :=
  n == ``Lean.reduceBool || n == ``Lean.reduceNat ||
  match rootComponent n with
  | .anonymous => true
  | .num _ _ => true
  | .str _ s =>
      ["_kernel_fresh", "_ind_fresh", "_nested_fresh", "_uniq", "_nested"].any (fun p : String => s.startsWith p) ||
      ["dontcare", "__expr_for_default_constructor__", "__local_decl_for_default_constructor"].contains s

def screen (c : ConstantInfo) : IO Unit := do
  if forbidden c.name then fail s!"FORBIDDEN_NAME name={c.name}"
  if c.isUnsafe || c.isPartial then fail s!"UNSAFE_OR_PARTIAL name={c.name}"
  if c.isAxiom && !allowedAxioms.contains c.name then
    fail s!"NONPERMITTED_AXIOM_OR_INCOMPLETE_RECORD name={c.name} importLevel=private"

structure Scan where
  refs : Std.HashSet Name := {}
  natLit : Bool := false
  strLits : Array String := #[]
  nodes : Nat := 0
  deriving Inhabited

/- A local structural visited set avoids expanding shared proof DAGs repeatedly.
   It is not a canonical encoding or a certificate cache. -/
def scanExpr (e : Expr) (initial : Scan := {}) : IO Scan := do
  if e.hasLooseBVars || e.hasFVar || e.hasMVar then
    fail "OPEN_OR_METAVARIABLE_SOURCE_EXPRESSION"
  let mut todo := #[e]
  let mut seen : Std.HashSet Expr := {}
  let mut out := initial
  while !todo.isEmpty do
    let t := todo.back!
    todo := todo.pop
    if seen.contains t then continue
    seen := seen.insert t
    out := { out with nodes := out.nodes + 1 }
    if out.nodes > 20000000 then fail "EXPRESSION_SCAN_NODE_LIMIT limit=20000000"
    match t with
    | .const n _ =>
        if forbidden n then fail s!"FORBIDDEN_REFERENCE name={n}"
        out := { out with refs := out.refs.insert n }
    | .proj n _ v =>
        if forbidden n then fail s!"FORBIDDEN_PROJECTION name={n}"
        out := { out with refs := out.refs.insert n }
        todo := todo.push v
    | .app f a => todo := (todo.push f).push a
    | .lam _ t b _ | .forallE _ t b _ => todo := (todo.push t).push b
    | .letE _ t v b _ => todo := ((todo.push t).push v).push b
    | .mdata _ b => todo := todo.push b
    | .lit (.natVal _) => out := { out with natLit := true }
    | .lit (.strVal s) =>
        if !out.strLits.contains s then out := { out with strLits := out.strLits.push s }
    | _ => pure ()
  return out

def scanInfo (c : ConstantInfo) (s : Scan) : IO Scan := do
  let mut s ← scanExpr c.type s
  if let some v := c.value? (allowOpaque := true) then s ← scanExpr v s
  if let .recInfo r := c then
    for rule in r.rules do
      s ← scanExpr rule.rhs s
      s := { s with refs := s.refs.insert rule.ctor }
  return s

def owner {σ : Type} [RecordSource σ] (src : σ) (n : Name) : IO Name := do
  match ← lookup src n with
  | .inductInfo i =>
      match i.all with
      | first :: _ => return first
      | [] => fail s!"EMPTY_GROUP_LIST name={n}"
  | .ctorInfo c =>
      match ← lookup src c.induct with
      | .inductInfo i =>
          match i.all with
          | first :: _ => return first
          | [] => fail s!"EMPTY_GROUP_LIST name={c.induct}"
      | _ => fail s!"BAD_CONSTRUCTOR_OWNER name={n}"
  | .recInfo r =>
      match r.all with
      | first :: _ =>
          match ← lookup src first with
          | .inductInfo i =>
              if i.all != r.all then fail s!"RECURSOR_GROUP_LIST_MISMATCH name={n}"
              return first
          | _ => fail s!"BAD_RECURSOR_OWNER name={n}"
      | [] => fail s!"EMPTY_RECURSOR_GROUP name={n}"
  | .quotInfo _ => return ``Quot
  | _ => return n

abbrev Members := Std.HashMap Name (Array Name)

def groupMembers {σ : Type} [RecordSource σ] (src : σ) : IO Members := do
  let mut out : Members := {}
  for (n, c) in RecordSource.records src do
    match c with
    | .inductInfo _ | .ctorInfo _ | .recInfo _ =>
        let key ← owner src n
        out := out.insert key ((out[key]?.getD #[]).push n)
    | _ => pure ()
  return out

structure Edge where
  dep : Name
  reason : String
  deriving Inhabited

structure UnitInfo where
  key : Name
  decl : Declaration
  emitted : Array Name
  refs : Array Name
  edges : Array Edge := #[]
  natLit : Bool
  strLits : Array String
  scanNodes : Nat
  deriving Inhabited

def makeUnit {σ : Type} [RecordSource σ] (src : σ) (members : Members) (key : Name) : IO UnitInfo := do
  let c ← lookup src key
  screen c
  let mut emitted := #[key]
  let decl ← match c with
    | .axiomInfo a => pure <| Declaration.axiomDecl a
    | .defnInfo d => pure <| Declaration.defnDecl d
    | .thmInfo t => pure <| Declaration.thmDecl t
    | .opaqueInfo o => pure <| Declaration.opaqueDecl o
    | .quotInfo _ =>
        emitted := quotNames
        pure Declaration.quotDecl
    | .inductInfo first => do
        emitted := members[key]?.getD #[]
        let mut types : List InductiveType := []
        for n in first.all do
          let .inductInfo i ← lookup src n | fail s!"BAD_GROUP_MEMBER name={n}"
          if i.all != first.all || i.levelParams != first.levelParams ||
              i.numParams != first.numParams || i.isUnsafe then
            fail s!"INCONSISTENT_GROUP_INPUT name={n}"
          let mut ctors : List Constructor := []
          for idx in [:i.ctors.length] do
            let cn := i.ctors[idx]!
            let .ctorInfo v ← lookup src cn | fail s!"BAD_CONSTRUCTOR_RECORD name={cn}"
            if v.induct != n || v.cidx != idx || v.numParams != i.numParams ||
                v.levelParams != i.levelParams || v.isUnsafe then
              fail s!"CONSTRUCTOR_METADATA_MISMATCH name={cn}"
            ctors := ctors ++ [{ name := cn, type := v.type }]
          types := types ++ [{ name := n, type := i.type, ctors }]
        pure <| Declaration.inductDecl first.levelParams first.numParams types false
    | _ => fail s!"UNSUPPORTED_ATOMIC_OWNER name={key}"
  let input ← decl.foldExprM (fun s e => scanExpr e s) ({} : Scan)
  let mut support := input
  for n in emitted do
    let ec ← lookup src n
    screen ec
    support ← scanInfo ec support
  let mut refs := support.refs.toArray
  if key == ``Quot then refs := refs.push ``Eq
  if input.natLit then refs := refs.push ``Nat
  if !input.strLits.isEmpty then refs := refs ++ stringRoots
  let mut edges : Array Edge := #[]
  for r in refs do
    let dep ← owner src r
    -- Only native group/quotient internal references are inside an atomic unit.
    if dep == key && (match decl with | .inductDecl .. | .quotDecl => true | _ => false) then
      continue
    edges := edges.push { dep, reason := s!"reference:{r}" }
  return { key, decl, emitted, refs, edges, natLit := input.natLit, strLits := input.strLits, scanNodes := support.nodes }

def collect {σ : Type} [RecordSource σ] (src : σ) (members : Members) : IO (Array UnitInfo) := do
  let mut todo := roots
  let mut pos := 0
  let mut seen : Std.HashSet Name := {}
  let mut out : Array UnitInfo := #[]
  while pos < todo.size do
    let name := todo[pos]!
    pos := pos + 1
    let key ← owner src name
    if seen.contains key then continue
    if out.size ≥ 50000 then fail "UNIT_LIMIT limit=50000"
    let u ← makeUnit src members key
    seen := seen.insert key
    out := out.push u
    todo := todo ++ u.refs
    if out.size % 100 == 0 then emit s!"COLLECT_PROGRESS units={out.size} pending={todo.size-pos}"
  return out

def cborHead (major n : Nat) : List UInt8 :=
  let byte := fun x : Nat => UInt8.ofNat x
  if n < 24 then [byte (major * 32 + n)]
  else if n < 256 then [byte (major * 32 + 24), byte n]
  else if n < 65536 then [byte (major * 32 + 25), byte (n / 256), byte n]
  else if n < 4294967296 then
    byte (major * 32 + 26) :: [24,16,8,0].map (fun k => byte (n / 2^k))
  else byte (major * 32 + 27) :: [56,48,40,32,24,16,8,0].map (fun k => byte (n / 2^k))

def nameComponents : Name → List (List UInt8)
  | .anonymous => []
  | .str p s => nameComponents p ++ [[0x82, 0] ++ cborHead 2 s.utf8ByteSize ++ s.toUTF8.data.toList]
  | .num p k => nameComponents p ++ [[0x82, 1] ++ cborHead 0 k]

def nameBytes (n : Name) : List UInt8 :=
  let cs := nameComponents n
  cborHead 4 cs.length ++ cs.flatten

def bytesLT : List UInt8 → List UInt8 → Bool
  | [], [] => false
  | [], _::_ => true
  | _::_, [] => false
  | a::as, b::bs => if a == b then bytesLT as bs else a < b

def unitName (u : UnitInfo) : Name :=
  u.emitted.foldl (fun best n => if bytesLT (nameBytes n) (nameBytes best) then n else best) u.key

def orderAndReport {σ : Type} [RecordSource σ] (src : σ) (units : Array UnitInfo) : IO (Option (Array UnitInfo)) := do
  let mut map : Std.HashMap Name UnitInfo := {}
  for u in units do map := map.insert u.key u
  -- L is full logical support, including generated support and implicit literal roots.
  let mut ltodo : Array Name := #[]
  for n in stringRoots do ltodo := ltodo.push (← owner src n)
  let mut lseen : Std.HashSet Name := {}
  let mut cursor := 0
  while cursor < ltodo.size do
    let k := ltodo[cursor]!
    cursor := cursor + 1
    if lseen.contains k then continue
    lseen := lseen.insert k
    let some u := map[k]? | fail s!"UNCLOSED_STRING_SUPPORT name={k}"
    for e in u.edges do ltodo := ltodo.push e.dep
  let mut staged := units
  for idx in [:staged.size] do
    let mut u := staged[idx]!
    if u.natLit then u := { u with edges := u.edges.push { dep := ``Nat, reason := "nat-literal-stage" } }
    if !u.strLits.isEmpty then
      emit s!"STRING_LITERAL_DESCRIPTOR name={u.key} inStringSupport={lseen.contains u.key} values={reprStr u.strLits}"
      for k in lseen do
        u := { u with edges := u.edges.push { dep := k, reason := "string-complete-support-stage" } }
    if u.refs.contains ``Nat.beq || u.refs.contains ``Nat.ble || u.key == ``Nat.beq || u.key == ``Nat.ble then
      u := { u with edges := u.edges.push { dep := ``Bool, reason := "builtin-bool-stage" } }
    staged := staged.set! idx u
  let sorted := staged.toList.mergeSort (fun a b => bytesLT (nameBytes (unitName a)) (nameBytes (unitName b)))
  let mut done : Std.HashSet Name := {}
  let mut ordered : Array UnitInfo := #[]
  let mut remaining := sorted
  while !remaining.isEmpty do
    let next := remaining.find? (fun u => u.edges.all (fun e => done.contains e.dep))
    let some u := next | break
    done := done.insert u.key
    ordered := ordered.push u
    remaining := remaining.filter (fun v => v.key != u.key)
  emit s!"STAGING_SUMMARY units={units.size} stringSupportUnits={lseen.size} ordered={ordered.size} residual={remaining.length}"
  if remaining.isEmpty then
    for i in [:ordered.size] do
      emit s!"ORDER index={i} unit={ordered[i]!.key} emitted={ordered[i]!.emitted.size}"
    return some ordered
  let mut residualMap : Std.HashMap Name UnitInfo := {}
  for u in remaining do residualMap := residualMap.insert u.key u
  let mut k := remaining.head!.key
  let mut visited : Std.HashMap Name Nat := {}
  let mut steps : Array (Name × Edge) := #[]
  while !visited.contains k do
    visited := visited.insert k steps.size
    let some u := residualMap[k]? | fail s!"RESIDUAL_MISSING_UNIT name={k}"
    let some e := u.edges.find? (fun e => !done.contains e.dep) | fail s!"RESIDUAL_WITHOUT_BLOCKER name={k}"
    steps := steps.push (k, e)
    k := e.dep
  let cycleStart := visited[k]?.getD 0
  for i in [:steps.size] do
    let (sourceName, edge) := steps[i]!
    emit s!"BLOCKER_PATH index={i} cycle={decide (i >= cycleStart)} from={sourceName} to={edge.dep} reason={edge.reason}"
  emit s!"STAGE_OBSTRUCTION cycleEntry={k} cycleStart={cycleStart} receiverReplay=NOT_RUN"
  return none

def sameRules : List RecursorRule → List RecursorRule → Bool
  | [], [] => true
  | a::as, b::bs => a.ctor == b.ctor && a.nfields == b.nfields &&
      Expr.equal a.rhs b.rhs && sameRules as bs
  | _, _ => false

def sameConstant (a b : ConstantInfo) : Bool :=
  a.name == b.name && a.levelParams == b.levelParams && Expr.equal a.type b.type &&
  match a, b with
  | .axiomInfo a, .axiomInfo b => a.isUnsafe == b.isUnsafe
  | .defnInfo a, .defnInfo b => Expr.equal a.value b.value && a.safety == b.safety && a.all == b.all
  | .thmInfo a, .thmInfo b => Expr.equal a.value b.value && a.all == b.all
  | .opaqueInfo a, .opaqueInfo b => Expr.equal a.value b.value && a.isUnsafe == b.isUnsafe && a.all == b.all
  | .ctorInfo a, .ctorInfo b => a.induct == b.induct && a.cidx == b.cidx &&
      a.numParams == b.numParams && a.numFields == b.numFields && a.isUnsafe == b.isUnsafe
  | .recInfo a, .recInfo b => a.all == b.all && a.numParams == b.numParams &&
      a.numIndices == b.numIndices && a.numMotives == b.numMotives &&
      a.numMinors == b.numMinors && sameRules a.rules b.rules && a.k == b.k && a.isUnsafe == b.isUnsafe
  | .inductInfo a, .inductInfo b =>
      a.numParams == b.numParams && a.numIndices == b.numIndices && a.all == b.all &&
      a.ctors == b.ctors && a.numNested == b.numNested && a.isRec == b.isRec &&
      a.isUnsafe == b.isUnsafe && a.isReflexive == b.isReflexive
  | .quotInfo a, .quotInfo b =>
      match a.kind, b.kind with
      | .type, .type | .ctor, .ctor | .lift, .lift | .ind, .ind => true
      | _, _ => false
  | _, _ => false

def withHeight (env : Kernel.Environment) (decl : Declaration) : IO Declaration := do
  let .defnDecl d := decl | return decl
  let s ← scanExpr d.value
  let mut maxH := 0
  for n in s.refs do
    let some c := env.find? n | fail s!"HEIGHT_UNBOUND_REFERENCE name={n}"
    if let .defnInfo v := c then
      if let .regular h := v.hints then maxH := max maxH h.toNat
  let h := maxH + 1
  if h > 4294967295 then fail s!"HEIGHT_OVERFLOW name={d.name} height={h}"
  return .defnDecl { d with hints := .regular (UInt32.ofNat h) }

def negativeControl : IO Unit := do
  let e ← Lean.mkEmptyEnvironment 0
  let env := e.toKernelEnv
  if env.quotInit || !env.constants.toList.isEmpty then fail "NEGATIVE_CONTROL_ENV_NOT_EMPTY"
  -- Closed, constant-free ill-typed witness for the proposition forall P : Prop, P.
  let ty := Expr.forallE `P (.sort .zero) (.bvar 0) .default
  let bad := Expr.lam `P (.sort .zero) (.bvar 0) .default
  let decl := Declaration.thmDecl { name := `BootProbeIllTyped, levelParams := [], type := ty, value := bad }
  match env.addDeclCore 100000 1000 decl none with
  | .ok _ => fail "NEGATIVE_CONTROL_WRONGLY_ACCEPTED"
  | .error (.declTypeMismatch ..) => emit "NEGATIVE_CONTROL_REJECTED kind=declTypeMismatch basisSuccess=false"
  | .error (.exprTypeMismatch ..) => emit "NEGATIVE_CONTROL_REJECTED kind=exprTypeMismatch basisSuccess=false"
  | .error ex =>
      let msg ← (ex.toMessageData {}).toString
      fail s!"NEGATIVE_CONTROL_INCONCLUSIVE detail={msg}"

def reconstruct (src : Kernel.Environment) (ordered : Array UnitInfo) : IO Kernel.Environment := do
  let empty ← Lean.mkEmptyEnvironment 0
  let mut env := empty.toKernelEnv
  if env.quotInit || !(env.constants.toList.isEmpty) then fail "RECEIVER_NOT_EMPTY"
  let mut expected : Std.HashSet Name := {}
  for i in [:ordered.size] do
    let u := ordered[i]!
    for n in u.emitted do
      if (env.find? n).isSome then fail s!"RECEIVER_OVERWRITE name={n}"
    if u.key == ``Quot && env.quotInit then fail "REPEATED_QUOT_INITIALIZATION"
    let decl ← withHeight env u.decl
    emit s!"CHECK_BEGIN index={i} name={u.key}"
    match env.addDeclCore 20000000 10000 decl none with
    | .error ex =>
        let msg ← (ex.toMessageData {}).toString
        fail s!"NATIVE_RECONSTRUCTION_FAILED index={i} name={u.key} detail={msg}"
    | .ok next => env := next
    for n in u.emitted do
      let a ← lookup src n
      let b ← lookup env n
      if !sameConstant a b then fail s!"SOURCE_INVENTORY_MISMATCH name={n}"
      expected := expected.insert n
    let actualSize := env.constants.fold (fun count _ _ => count + 1) 0
    if actualSize != expected.size then
      fail s!"GENERATED_INVENTORY_SIZE_MISMATCH after={u.key} actual={actualSize} expected={expected.size}"
    emit s!"CHECK_OK index={i} name={u.key} cumulativeExports={expected.size}"
  if !env.quotInit then fail "MISSING_QUOT_INITIALIZATION"
  emit s!"FULL_CHECKED_SOURCE_RECORD_RECONSTRUCTION_OK exports={expected.size} canonicalCodec=NOT_IMPLEMENTED FoundationID=UNASSIGNED"
  return env

/- JSON is only a lossless local projection of the selected array/uint/bytes grammar.
   The strict CBOR bridge and its locally adopted identity binding are separate. -/
def jnat (n : Nat) : Json := toJson n
def jarr (xs : Array Json) : Json := .arr xs
def jbytes (xs : ByteArray) : Json :=
  Json.mkObj [("$bytes", .arr (xs.data.map (fun b => jnat b.toNat)))]

def checkU32 (label : String) (n : Nat) : IO Unit := do
  if n > 4294967295 then fail s!"NATIVE_U32_RANGE field={label} value={n}"

def nameJson (n : Name) : IO Json := do
  if forbidden n then fail s!"FORBIDDEN_WIRE_NAME name={n}"
  let rec components : Name → IO (Array Json)
    | .anonymous => pure #[]
    | .str p s => do
        let a ← components p
        return a.push (jarr #[jnat 0, jbytes s.toUTF8])
    | .num p k => do
        checkU32 "nameNumeral" k
        let a ← components p
        return a.push (jarr #[jnat 1, jnat k])
  return jarr (← components n)

def binderCode : BinderInfo → Nat
  | .default => 0
  | .implicit => 1
  | .strictImplicit => 2
  | .instImplicit => 3

def magnitude (n : Nat) : IO ByteArray := do
  let mut n := n
  let mut bytes : Array UInt8 := #[]
  while n > 0 do
    if bytes.size ≥ 1048576 then fail "NAT_MAGNITUDE_LIMIT"
    bytes := bytes.push (UInt8.ofNat (n % 256))
    n := n / 256
  return ⟨bytes.reverse⟩

structure Encoder where
  levels : Array Json := #[]
  exprs : Array Json := #[]
  levelDepths : Array Nat := #[]
  exprDepths : Array Nat := #[]
  levelNodes : Std.HashMap Json Nat := {}
  exprNodes : Std.HashMap Json Nat := {}
  levelMemo : Std.HashMap Level Nat := {}
  exprMemo : Std.HashMap UInt64 (Array (Expr × Nat)) := {}
  deriving Inhabited

abbrev EncodeM := StateT Encoder IO

def internLevel (node : Json) (depth : Nat) : EncodeM Nat := do
  let s ← get
  if let some i := s.levelNodes[node]? then return i
  if depth > 4096 || s.levels.size ≥ 65536 then
    fail "LEVEL_DAG_BOUND"
  let i := s.levels.size
  set { s with levels := s.levels.push node, levelDepths := s.levelDepths.push depth, levelNodes := s.levelNodes.insert node i }
  return i

partial def encodeLevel (params : List Name) (u : Level) (fuel : Nat := 4096) : EncodeM Nat := do
  let s ← get
  if let some i := s.levelMemo[u]? then return i
  if fuel == 0 then fail "LEVEL_SOURCE_DEPTH_LIMIT"
  let (node, depth) ← match u with
    | .zero => pure (jarr #[jnat 0], 1)
    | .succ a => do
        let i ← encodeLevel params a (fuel-1)
        pure (jarr #[jnat 1, jnat i], (← get).levelDepths[i]! + 1)
    | .max a b | .imax a b => do
        let i ← encodeLevel params a (fuel-1)
        let j ← encodeLevel params b (fuel-1)
        let tag := match u with | .max .. => 2 | _ => 3
        let st ← get
        pure (jarr #[jnat tag, jnat i, jnat j], max st.levelDepths[i]! st.levelDepths[j]! + 1)
    | .param p => do
        let i := params.idxOf p
        if i ≥ params.length then fail s!"UNDECLARED_UNIVERSE name={p}"
        pure (jarr #[jnat 4, jnat i], 1)
    | .mvar _ => fail "UNIVERSE_METAVARIABLE"
  let i ← internLevel node depth
  modify fun st => { st with levelMemo := st.levelMemo.insert u i }
  return i

def internExpr (node : Json) (depth : Nat) : EncodeM Nat := do
  let s ← get
  if let some i := s.exprNodes[node]? then return i
  if depth > 4096 || s.exprs.size ≥ 1048576 then fail "EXPR_DAG_BOUND"
  let i := s.exprs.size
  set { s with exprs := s.exprs.push node, exprDepths := s.exprDepths.push depth, exprNodes := s.exprNodes.insert node i }
  return i

partial def encodeExpr (params : List Name) (e : Expr) (fuel : Nat := 8192) : EncodeM Nat := do
  if fuel == 0 then fail "EXPR_SOURCE_DEPTH_LIMIT"
  let st ← get
  if let some (_, i) := (st.exprMemo[hash e]?.getD #[]).find? (fun p => Expr.equal p.1 e) then
    return i
  if let .mdata _ b := e then return ← encodeExpr params b (fuel-1)
  let (node, depth) ← match e with
    | .bvar k => do
        checkU32 "bvar" k
        pure (jarr #[jnat 0, jnat k], 1)
    | .sort u => do
        let i ← encodeLevel params u
        pure (jarr #[jnat 1, jnat i], (← get).levelDepths[i]! + 1)
    | .const n ls => do
        let mut us := #[]
        let mut dep := 0
        for l in ls do
          let i ← encodeLevel params l
          us := us.push (jnat i)
          dep := max dep (← get).levelDepths[i]!
        pure (jarr #[jnat 2, jarr #[jnat 6, ← nameJson n], jarr us], dep + 1)
    | .app f a => do
        let i ← encodeExpr params f (fuel-1)
        let j ← encodeExpr params a (fuel-1)
        let s ← get
        pure (jarr #[jnat 3, jnat i, jnat j], max s.exprDepths[i]! s.exprDepths[j]! + 1)
    | .lam _ t b bi | .forallE _ t b bi => do
        let i ← encodeExpr params t (fuel-1)
        let j ← encodeExpr params b (fuel-1)
        let s ← get
        let tag := match e with | .lam .. => 4 | _ => 5
        pure (jarr #[jnat tag, jnat (binderCode bi), jnat i, jnat j], max s.exprDepths[i]! s.exprDepths[j]! + 1)
    | .letE _ t v b _ => do
        let i ← encodeExpr params t (fuel-1)
        let j ← encodeExpr params v (fuel-1)
        let k ← encodeExpr params b (fuel-1)
        let s ← get
        pure (jarr #[jnat 6, jnat i, jnat j, jnat k], max (max s.exprDepths[i]! s.exprDepths[j]!) s.exprDepths[k]! + 1)
    | .lit (.natVal n) => pure (jarr #[jnat 7, jbytes (← magnitude n)], 1)
    | .lit (.strVal s) => do
        if s.utf8ByteSize > 1048576 then fail "STRING_LITERAL_LIMIT"
        pure (jarr #[jnat 9, jbytes s.toUTF8], 1)
    | .proj n k b => do
        checkU32 "projectionIndex" k
        let i ← encodeExpr params b (fuel-1)
        pure (jarr #[jnat 8, jarr #[jnat 6, ← nameJson n], jnat k, jnat i], (← get).exprDepths[i]! + 1)
    | _ => fail "UNSUPPORTED_EXPRESSION_EXPORT"
  let i ← internExpr node depth
  modify fun s => { s with exprMemo := s.exprMemo.insert (hash e) ((s.exprMemo[hash e]?.getD #[]).push (e, i)) }
  return i

def dagJson (params : List Name) (e : Expr) : IO Json := do
  if params.length > 1024 || params.eraseDups.length != params.length then fail "UNIVERSE_ARITY_OR_DUPLICATE"
  if e.hasLooseBVars || e.hasFVar || e.hasMVar then fail "OPEN_EXPORT_ROOT"
  let (root, s) ← (encodeExpr params e).run {}
  if root + 1 != s.exprs.size then fail "INTERNAL_NONFINAL_ROOT"
  return jarr #[jarr s.levels, jarr s.exprs, jnat root]

def descriptorJson (d : Declaration) : IO Json := do
  match d with
  | .axiomDecl a =>
      return jarr #[jnat 5, ← nameJson a.name, jnat a.levelParams.length, ← dagJson a.levelParams a.type]
  | .defnDecl d =>
      return jarr #[jnat 0, ← nameJson d.name, jnat d.levelParams.length, ← dagJson d.levelParams d.type, ← dagJson d.levelParams d.value]
  | .thmDecl d =>
      return jarr #[jnat 1, ← nameJson d.name, jnat d.levelParams.length, ← dagJson d.levelParams d.type, ← dagJson d.levelParams d.value]
  | .opaqueDecl d =>
      return jarr #[jnat 2, ← nameJson d.name, jnat d.levelParams.length, ← dagJson d.levelParams d.type, ← dagJson d.levelParams d.value]
  | .quotDecl => return jarr #[jnat 4]
  | .inductDecl us np types unsafeFlag =>
      if unsafeFlag || types.isEmpty || types.length > 4096 then fail "GROUP_EXPORT_SHAPE"
      checkU32 "inductiveNumParams" np
      let mut ts := #[]
      let mut count := 0
      for t in types do
        let mut cs := #[]
        for c in t.ctors do
          count := count + 1
          if count > 65536 then fail "GROUP_CONSTRUCTOR_LIMIT"
          cs := cs.push (jarr #[← nameJson c.name, ← dagJson us c.type])
        ts := ts.push (jarr #[← nameJson t.name, ← dagJson us t.type, jarr cs])
      return jarr #[jnat 3, jnat us.length, jnat np, jarr ts]
  | _ => fail "UNSUPPORTED_SEED_DESCRIPTOR"

def sourceCommit : ByteArray := ⟨#[0x29,0x3d,0x5d,0x0c,0x0c,0x3f,0x3d,0xde,0xd4,0x68,0x8b,0x3c,0xcd,0x6a,0x33,0x93,0x9a,0xc5,0x10,0x2b]⟩

def namesJson (names : List Name) : IO Json := do
  return jarr (← names.toArray.mapM nameJson)

def boolJson (b : Bool) : Json := jnat (if b then 1 else 0)

/- A separately bound diagnostic inventory, not an extra SeedProfile field.
   Definition/theorem/opaque `all` is normalized to its single declaration, as
   the seed descriptor has no mutual-block metadata and checked safe blocks are lowered. -/
def inventoryRow (c : ConstantInfo) (heightOverride : Option Nat := none) : IO Json := do
  let name ← nameJson c.name
  let ty ← dagJson c.levelParams c.type
  let (kind, data) ← match c with
    | .axiomInfo a => pure (0, jarr #[boolJson a.isUnsafe])
    | .defnInfo d => do
        let h ← match heightOverride with
          | some h => pure h
          | none => match d.hints with
            | .regular h => pure h.toNat
            | _ => fail s!"INVENTORY_NONREGULAR_DEFINITION name={d.name}"
        checkU32 "regularHeight" h
        pure (1, jarr #[← dagJson d.levelParams d.value, jnat h, jarr #[name]])
    | .thmInfo d => pure (2, jarr #[← dagJson d.levelParams d.value, jarr #[name]])
    | .opaqueInfo d => pure (3, jarr #[← dagJson d.levelParams d.value, boolJson d.isUnsafe, jarr #[name]])
    | .inductInfo i => do
        for n in [i.numParams, i.numIndices, i.numNested] do checkU32 "generatedInductiveCount" n
        pure (4, jarr #[jnat i.numParams, jnat i.numIndices, ← namesJson i.all, ← namesJson i.ctors, jnat i.numNested, boolJson i.isRec, boolJson i.isUnsafe, boolJson i.isReflexive])
    | .ctorInfo v => do
        for n in [v.cidx, v.numParams, v.numFields] do checkU32 "generatedConstructorCount" n
        pure (5, jarr #[← nameJson v.induct, jnat v.cidx, jnat v.numParams, jnat v.numFields, boolJson v.isUnsafe])
    | .recInfo r => do
        for n in [r.numParams, r.numIndices, r.numMotives, r.numMinors] do checkU32 "generatedRecursorCount" n
        let mut rs := #[]
        for rule in r.rules do
          checkU32 "generatedRuleFields" rule.nfields
          rs := rs.push (jarr #[← nameJson rule.ctor, jnat rule.nfields, ← dagJson r.levelParams rule.rhs])
        pure (6, jarr #[← namesJson r.all, jnat r.numParams, jnat r.numIndices, jnat r.numMotives, jnat r.numMinors, jarr rs, boolJson r.k, boolJson r.isUnsafe])
    | .quotInfo q =>
        pure (7, jarr #[jnat (match q.kind with | .type => 0 | .ctor => 1 | .lift => 2 | .ind => 3)])
  return jarr #[name, jnat kind, jnat c.levelParams.length, ty, data]

def exportHeights (src : Kernel.Environment) (ordered : Array UnitInfo) : IO (Std.HashMap Name Nat) := do
  let mut hs : Std.HashMap Name Nat := {}
  for u in ordered do
    if let .defnDecl d := u.decl then
      let s ← scanExpr d.value
      let mut h := 0
      for n in s.refs do
        if let .defnInfo _ := ← lookup src n then
          let some dep := hs[n]? | fail s!"EXPORT_HEIGHT_MISSING name={n}"
          h := max h dep
      checkU32 "exportHeight" (h+1)
      hs := hs.insert d.name (h+1)
  return hs

def emitSeed (src : Kernel.Environment) (ordered : Array UnitInfo) : IO Unit := do
  let mut ds := #[]
  let mut ns : Array Name := #[]
  for u in ordered do
    ds := ds.push (← descriptorJson u.decl)
    ns := ns ++ u.emitted
  let names := ns.toList.mergeSort (fun a b => bytesLT (nameBytes a) (nameBytes b))
  if names.eraseDups.length != names.length then fail "DUPLICATE_EXPORT_NAMES"
  let mut nameRows := #[]
  for n in names do nameRows := nameRows.push (← nameJson n)
  let payload := jarr #[jbytes sourceCommit, jarr ds, jarr nameRows]
  emit s!"SEED_JSON {payload.compress}"
  let heights ← exportHeights src ordered
  let mut inventory := #[]
  for n in names do
    inventory := inventory.push (← inventoryRow (← lookup src n) heights[n]?)
  emit s!"SEED_INVENTORY_JSON {(jarr inventory).compress}"

def jsonResult {α : Type} (r : Except String α) : IO α :=
  match r with | .ok x => pure x | .error s => fail s!"JSON_PROJECTION {s}"

def arrayOf (j : Json) (size : Option Nat := none) : IO (Array Json) := do
  let a ← jsonResult j.getArr?
  if let some n := size then
    if a.size != n then fail s!"SCHEMA_ARITY expected={n} actual={a.size}"
  if a.size > 1048576 then fail "JSON_ARRAY_LIMIT"
  return a

def natOf (j : Json) : IO Nat := do
  let n ← jsonResult j.getNat?
  if n > 18446744073709551615 then fail "WIRE_UINT64_RANGE"
  return n

def u32Of (j : Json) : IO Nat := do
  let n ← natOf j
  checkU32 "decodedInteger" n
  return n

def boolOf (j : Json) : IO Bool := do
  match ← natOf j with
  | 0 => return false
  | 1 => return true
  | _ => fail "BOOL_CODE_RANGE"

def bytesOf (j : Json) : IO ByteArray := do
  let obj ← jsonResult j.getObj?
  if obj.size != 1 then fail "BYTES_PROJECTION_ARITY"
  let some data := obj.get? "$bytes" | fail "BYTES_PROJECTION_KEY"
  let a ← arrayOf data
  let mut out : ByteArray := ⟨#[]⟩
  for x in a do
    let n ← natOf x
    if n > 255 then fail "BYTE_RANGE"
    out := out.push (UInt8.ofNat n)
  return out

def nameOf (j : Json) : IO Name := do
  let a ← arrayOf j
  if a.isEmpty || a.size > 4096 then fail "NAME_PATH_BOUND"
  let mut out := Name.anonymous
  for entry in a do
    let p ← arrayOf entry (some 2)
    match ← natOf p[0]! with
    | 0 =>
        let b ← bytesOf p[1]!
        let some s := String.fromUTF8? b | fail "INVALID_NAME_UTF8"
        if s.toUTF8 != b then fail "NONCANONICAL_NAME_UTF8"
        out := .str out s
    | 1 => out := .num out (← u32Of p[1]!)
    | _ => fail "NAME_COMPONENT_TAG"
  if forbidden out then fail s!"FORBIDDEN_DECODED_NAME name={out}"
  if (← nameJson out) != j then fail "NAME_ROUNDTRIP_MISMATCH"
  return out

def namesOf (j : Json) : IO (List Name) := do
  return (← (← arrayOf j).mapM nameOf).toList

def indexedParams (arity : Nat) : IO (List Name) := do
  if arity > 1024 then fail "UNIVERSE_ARITY_BOUND"
  return (List.range arity).map (fun i => Name.mkSimple s!"u{i}")

def nodeIndex (j : Json) (bound : Nat) : IO Nat := do
  let n ← u32Of j
  if n ≥ bound then fail s!"DAG_INDEX_RANGE index={n} bound={bound}"
  return n

def binderOf (j : Json) : IO BinderInfo := do
  match ← natOf j with
  | 0 => return .default
  | 1 => return .implicit
  | 2 => return .strictImplicit
  | 3 => return .instImplicit
  | _ => fail "BINDER_INFO_RANGE"

def localRefOf (allowed : Std.HashSet Name) (j : Json) : IO Name := do
  let a ← arrayOf j (some 2)
  if (← natOf a[0]!) != 6 then fail "NONSEED_REFERENCE_IN_BOOTSTRAP"
  let n ← nameOf a[1]!
  if !allowed.contains n then fail s!"UNEXPORTED_SEED_REFERENCE name={n}"
  return n

def decodeDag (params : List Name) (allowed : Std.HashSet Name) (j : Json) : IO Expr := do
  let a ← arrayOf j (some 3)
  let rawLs ← arrayOf a[0]!
  let rawEs ← arrayOf a[1]!
  if rawLs.size > 65536 || rawEs.isEmpty then fail "DAG_NODE_BOUND"
  let mut ls : Array Level := #[]
  for node in rawLs do
    let p ← arrayOf node
    if p.isEmpty then fail "EMPTY_LEVEL_NODE"
    let tag ← natOf p[0]!
    let u ← match tag with
      | 0 => do
          discard <| arrayOf node (some 1)
          pure Level.zero
      | 1 => do
          discard <| arrayOf node (some 2)
          pure <| Level.succ ls[← nodeIndex p[1]! ls.size]!
      | 2 | 3 => do
          discard <| arrayOf node (some 3)
          let x := ls[← nodeIndex p[1]! ls.size]!
          let y := ls[← nodeIndex p[2]! ls.size]!
          pure <| if tag == 2 then Level.max x y else Level.imax x y
      | 4 => do
          discard <| arrayOf node (some 2)
          let k ← nodeIndex p[1]! params.length
          pure <| Level.param params[k]!
      | _ => fail "LEVEL_TAG"
    ls := ls.push u
  let mut es : Array Expr := #[]
  let mut needs : Array Nat := #[]
  for node in rawEs do
    let p ← arrayOf node
    if p.isEmpty then fail "EMPTY_EXPR_NODE"
    let tag ← natOf p[0]!
    let (e, req) ← match tag with
      | 0 => do
          discard <| arrayOf node (some 2)
          let k ← u32Of p[1]!
          pure (Expr.bvar k, k+1)
      | 1 => do
          discard <| arrayOf node (some 2)
          pure (Expr.sort ls[← nodeIndex p[1]! ls.size]!, 0)
      | 2 => do
          discard <| arrayOf node (some 3)
          let n ← localRefOf allowed p[1]!
          let inst ← arrayOf p[2]!
          if inst.size > 1024 then fail "LEVEL_INSTANCE_BOUND"
          let mut us := []
          for k in inst do us := us ++ [ls[← nodeIndex k ls.size]!]
          pure (Expr.const n us, 0)
      | 3 => do
          discard <| arrayOf node (some 3)
          let i ← nodeIndex p[1]! es.size
          let k ← nodeIndex p[2]! es.size
          pure (Expr.app es[i]! es[k]!, max needs[i]! needs[k]!)
      | 4 | 5 => do
          discard <| arrayOf node (some 4)
          let bi ← binderOf p[1]!
          let i ← nodeIndex p[2]! es.size
          let k ← nodeIndex p[3]! es.size
          let e := if tag == 4 then Expr.lam `x es[i]! es[k]! bi else Expr.forallE `x es[i]! es[k]! bi
          pure (e, max needs[i]! (needs[k]! - 1))
      | 6 => do
          discard <| arrayOf node (some 4)
          let i ← nodeIndex p[1]! es.size
          let k ← nodeIndex p[2]! es.size
          let l ← nodeIndex p[3]! es.size
          pure (Expr.letE `x es[i]! es[k]! es[l]! false, max (max needs[i]! needs[k]!) (needs[l]! - 1))
      | 7 => do
          discard <| arrayOf node (some 2)
          let b ← bytesOf p[1]!
          if b.size > 1048576 || (!b.isEmpty && b[0]! == 0) then fail "NAT_MAGNITUDE_CANONICALITY"
          let n := b.data.foldl (fun n x => n*256+x.toNat) 0
          pure (Expr.lit (.natVal n), 0)
      | 8 => do
          discard <| arrayOf node (some 4)
          let n ← localRefOf allowed p[1]!
          let field ← u32Of p[2]!
          let i ← nodeIndex p[3]! es.size
          pure (Expr.proj n field es[i]!, needs[i]!)
      | 9 => do
          discard <| arrayOf node (some 2)
          let b ← bytesOf p[1]!
          if b.size > 1048576 then fail "STRING_LITERAL_BOUND"
          let some s := String.fromUTF8? b | fail "STRING_LITERAL_UTF8"
          if s.toUTF8 != b then fail "STRING_LITERAL_NONCANONICAL_UTF8"
          pure (Expr.lit (.strVal s), 0)
      | _ => fail "EXPR_TAG"
    es := es.push e
    needs := needs.push req
  let root ← nodeIndex a[2]! es.size
  if root+1 != es.size || needs[root]! != 0 then fail "DAG_ROOT_OR_SCOPE"
  let e := es[root]!
  -- Re-encoding validates exact sharing, left-to-right postorder, reachability,
  -- level parameter order, and selected structural limits without tree expansion.
  if (← dagJson params e) != j then fail "DAG_NONCANONICAL_ROUNDTRIP"
  return e

def decodeDescriptor (allowed : Std.HashSet Name) (j : Json) : IO Declaration := do
  let a ← arrayOf j
  if a.isEmpty then fail "EMPTY_DESCRIPTOR"
  let tag ← natOf a[0]!
  if tag == 4 then
    discard <| arrayOf j (some 1)
    return .quotDecl
  if tag == 3 then
    discard <| arrayOf j (some 4)
    let ps ← indexedParams (← u32Of a[1]!)
    let np ← u32Of a[2]!
    let ts ← arrayOf a[3]!
    if ts.isEmpty || ts.size > 4096 then fail "INDUCTIVE_GROUP_SIZE"
    let mut types := []
    let mut count := 0
    for row in ts do
      let t ← arrayOf row (some 3)
      let n ← nameOf t[0]!
      if !allowed.contains n then fail "GROUP_TYPE_NOT_EXPORTED"
      let ty ← decodeDag ps allowed t[1]!
      let mut ctors := []
      for cr in ← arrayOf t[2]! do
        count := count+1
        if count > 65536 then fail "CONSTRUCTOR_COUNT_LIMIT"
        let c ← arrayOf cr (some 2)
        let cn ← nameOf c[0]!
        if !allowed.contains cn then fail "CONSTRUCTOR_NOT_EXPORTED"
        ctors := ctors ++ [{ name := cn, type := ← decodeDag ps allowed c[1]! }]
      types := types ++ [{ name := n, type := ty, ctors }]
    return .inductDecl ps np types false
  if tag > 5 then fail "DESCRIPTOR_TAG"
  discard <| arrayOf j (some (if tag == 5 then 4 else 5))
  let n ← nameOf a[1]!
  if !allowed.contains n then fail "DECLARATION_NOT_EXPORTED"
  let ps ← indexedParams (← u32Of a[2]!)
  let ty ← decodeDag ps allowed a[3]!
  if tag == 5 then
    if !allowedAxioms.contains n then fail s!"UNADOPTED_AXIOM_NAME name={n}"
    return .axiomDecl { name := n, levelParams := ps, type := ty, isUnsafe := false }
  let v ← decodeDag ps allowed a[4]!
  match tag with
  | 0 => return .defnDecl { name := n, levelParams := ps, type := ty, value := v, hints := .regular 0, safety := .safe }
  | 1 => return .thmDecl { name := n, levelParams := ps, type := ty, value := v }
  | 2 => return .opaqueDecl { name := n, levelParams := ps, type := ty, value := v, isUnsafe := false }
  | _ => fail "DESCRIPTOR_KIND"

def inventoryInfo (allowed : Std.HashSet Name) (row : Json) : IO ConstantInfo := do
  let a ← arrayOf row (some 5)
  let n ← nameOf a[0]!
  if !allowed.contains n then fail "INVENTORY_NAME_NOT_EXPORTED"
  let kind ← natOf a[1]!
  let ps ← indexedParams (← u32Of a[2]!)
  let ty ← decodeDag ps allowed a[3]!
  let base : ConstantVal := { name := n, levelParams := ps, type := ty }
  let d ← arrayOf a[4]!
  match kind with
  | 0 =>
      discard <| arrayOf a[4]! (some 1)
      return .axiomInfo { toConstantVal := base, isUnsafe := ← boolOf d[0]! }
  | 1 =>
      discard <| arrayOf a[4]! (some 3)
      let all ← namesOf d[2]!
      if all != [n] then fail "NONCANONICAL_DEFINITION_ALL"
      return .defnInfo { toConstantVal := base, value := ← decodeDag ps allowed d[0]!, hints := .regular (UInt32.ofNat (← u32Of d[1]!)), safety := .safe, all }
  | 2 =>
      discard <| arrayOf a[4]! (some 2)
      let all ← namesOf d[1]!
      if all != [n] then fail "NONCANONICAL_THEOREM_ALL"
      return .thmInfo { toConstantVal := base, value := ← decodeDag ps allowed d[0]!, all }
  | 3 =>
      discard <| arrayOf a[4]! (some 3)
      let all ← namesOf d[2]!
      if all != [n] then fail "NONCANONICAL_OPAQUE_ALL"
      return .opaqueInfo { toConstantVal := base, value := ← decodeDag ps allowed d[0]!, isUnsafe := ← boolOf d[1]!, all }
  | 4 =>
      discard <| arrayOf a[4]! (some 8)
      return .inductInfo { toConstantVal := base, numParams := ← u32Of d[0]!, numIndices := ← u32Of d[1]!, all := ← namesOf d[2]!, ctors := ← namesOf d[3]!, numNested := ← u32Of d[4]!, isRec := ← boolOf d[5]!, isUnsafe := ← boolOf d[6]!, isReflexive := ← boolOf d[7]! }
  | 5 =>
      discard <| arrayOf a[4]! (some 5)
      return .ctorInfo { toConstantVal := base, induct := ← nameOf d[0]!, cidx := ← u32Of d[1]!, numParams := ← u32Of d[2]!, numFields := ← u32Of d[3]!, isUnsafe := ← boolOf d[4]! }
  | 6 =>
      discard <| arrayOf a[4]! (some 8)
      let mut rules := []
      for rr in ← arrayOf d[5]! do
        let r ← arrayOf rr (some 3)
        rules := rules ++ [{ ctor := ← nameOf r[0]!, nfields := ← u32Of r[1]!, rhs := ← decodeDag ps allowed r[2]! }]
      return .recInfo { toConstantVal := base, all := ← namesOf d[0]!, numParams := ← u32Of d[1]!, numIndices := ← u32Of d[2]!, numMotives := ← u32Of d[3]!, numMinors := ← u32Of d[4]!, rules, k := ← boolOf d[6]!, isUnsafe := ← boolOf d[7]! }
  | 7 =>
      discard <| arrayOf a[4]! (some 1)
      let kind ← match ← natOf d[0]! with
        | 0 => pure QuotKind.type
        | 1 => pure QuotKind.ctor
        | 2 => pure QuotKind.lift
        | 3 => pure QuotKind.ind
        | _ => fail "QUOTIENT_KIND"
      return .quotInfo { toConstantVal := base, kind }
  | _ => fail "INVENTORY_KIND"

def readProjection (path : String) : IO Json := do
  let metadata ← (System.FilePath.mk path).metadata
  if metadata.byteSize > 134217728 then fail "PROJECTION_FILE_LIMIT"
  jsonResult <| Json.parse (← IO.FS.readFile path)

def receiveSeed (payload inventory : Json) : IO Lean.Environment := do
  emit "DATA_ONLY_SEED_BEGIN producerImport=false authority=experiment-owner-selected-candidate-bound-by-trusted-CBOR-bridge inventoryAuthority=false productionAdoption=false"
  let seed ← arrayOf payload (some 3)
  if (← bytesOf seed[0]!) != sourceCommit then fail "UNSUPPORTED_SOURCE_PIN"
  let rawNames ← arrayOf seed[2]!
  let mut allowed : Std.HashSet Name := {}
  let mut names : Array Name := #[]
  for row in rawNames do
    let n ← nameOf row
    if allowed.contains n then fail "DUPLICATE_EXPORT_NAME"
    if !names.isEmpty && !bytesLT (nameBytes names.back!) (nameBytes n) then fail "EXPORT_NAME_ORDER"
    allowed := allowed.insert n
    names := names.push n
  for n in roots do
    if !allowed.contains n then fail s!"MISSING_REQUIRED_BOOT_ROOT name={n}"
  let invRows ← arrayOf inventory
  if invRows.size != names.size then fail "INVENTORY_EXPORT_COUNT"
  let mut expected : InventoryData := {}
  let mut rowMap : Std.HashMap Name Json := {}
  for i in [:invRows.size] do
    let c ← inventoryInfo allowed invRows[i]!
    if c.name != names[i]! then fail "INVENTORY_SORT_ORDER"
    screen c
    if (← inventoryRow c) != invRows[i]! then fail "INVENTORY_CANONICAL_ROUNDTRIP"
    expected := { entries := expected.entries.insert c.name c }
    rowMap := rowMap.insert c.name invRows[i]!
  let members ← groupMembers expected
  let units ← collect expected members
  let some ordered ← orderAndReport expected units | fail "DECODED_SEED_STAGE_OBSTRUCTION"
  let rawDecls ← arrayOf seed[1]!
  if rawDecls.size != ordered.size || rawDecls.size > 16384 then fail "SEED_DESCRIPTOR_COUNT"
  let mut declared : Std.HashSet Name := {}
  let mut decoded : Array Declaration := #[]
  for i in [:ordered.size] do
    let u := ordered[i]!
    if (← descriptorJson u.decl) != rawDecls[i]! then fail s!"SEED_DESCRIPTOR_INVENTORY_OR_ORDER_MISMATCH unit={u.key}"
    for n in u.emitted do
      if declared.contains n then fail "MULTIPLE_GENERATORS_FOR_EXPORT"
      declared := declared.insert n
    decoded := decoded.push (← decodeDescriptor allowed rawDecls[i]!)
  if declared.size != allowed.size then fail "SEED_NONROOT_EXTRA_INVENTORY"
  let empty ← Lean.mkEmptyEnvironment 0
  let mut fullEnv := empty
  let mut env := fullEnv.toKernelEnv
  if env.quotInit || !env.constants.toList.isEmpty then fail "DATA_RECEIVER_NOT_EMPTY"
  let mut done : Std.HashSet Name := {}
  for i in [:ordered.size] do
    let u := ordered[i]!
    for e in u.edges do
      if !done.contains e.dep then fail "DECODED_STAGE_PREREQUISITE"
    for n in u.emitted do
      if (env.find? n).isSome then fail s!"DECODED_OVERWRITE name={n}"
    if u.key == ``Quot && env.quotInit then fail "DECODED_REPEATED_QUOT"
    let d ← withHeight env decoded[i]!
    emit s!"DATA_CHECK_BEGIN index={i} name={u.key}"
    match fullEnv.addDeclCore 20000000 10000 d none (doCheck := true) with
    | .error ex =>
        let msg ← (ex.toMessageData {}).toString
        fail s!"DATA_NATIVE_REJECTED name={u.key} detail={msg}"
    | .ok checked =>
        fullEnv := checked
        env := checked.toKernelEnv
    for n in u.emitted do
      let actual ← inventoryRow (← lookup env n)
      let some expectedRow := rowMap[n]? | fail "INTERNAL_EXPECTED_ROW_MISSING"
      if actual != expectedRow then fail s!"DATA_GENERATED_INVENTORY_MISMATCH name={n}"
    done := done.insert u.key
  if !env.quotInit then fail "DATA_QUOT_NOT_INITIALIZED"
  let actualNames := env.constants.toList.map Prod.fst
  if actualNames.length != names.size || !(actualNames.all allowed.contains) then fail "DATA_UNEXPECTED_GENERATED_NAME"
  let mut actualRows := #[]
  for n in names do actualRows := actualRows.push (← inventoryRow (← lookup env n))
  emit s!"RECEIVED_INVENTORY_JSON {(jarr actualRows).compress}"
  emit s!"DATA_ONLY_SEED_CHECKED units={ordered.size} exports={names.size} producerImport=false canonicalCommitmentVerification=trusted-local-CBOR-bridge"
  return fullEnv

end BootstrapProbe

