import Lean.Expr
import Lean.Data.Json.FromToJson.Basic
import Std.Data.HashSet.Basic

/- Metadata-preserving inert expression codec for the ordinary Lean lane.
   Reuses bounded DAG patterns from the project's frozen BootstrapSupport and
   full-field serializer patterns from AuthorLean. No imported peer environment,
   kernel insertion, proof acceptance, filesystem access, or source execution.
   The caller binds the ordered universe parameters and a grounded name set. -/

open Lean

namespace OrdinaryLean.ExprCodec

def format : String := "DMKN_LEAN_ORIGINAL_EXPR_V1"
def normalization : String := "erase-mdata-only-v1"

/-- Trusted caller configuration, never a peer-granted resource allowance. -/
structure Limits where
  maxLevels : Nat := 65536
  maxExprs : Nat := 1048576
  maxDepth : Nat := 4096
  maxParams : Nat := 1024
  maxNameParts : Nat := 4096
  maxNameBytes : Nat := 1048576
  maxLiteralBytes : Nat := 1048576
  maxTotalLiteralBytes : Nat := 67108864
  deriving Inhabited

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"ORDINARY_EXPR {message}"

def jsonResult {α : Type} (result : Except String α) : IO α :=
  match result with
  | .ok value => pure value
  | .error message => fail s!"JSON {message}"

def arr (xs : Array Json) : Json := .arr xs
def num (n : Nat) : Json := toJson n

def arrayOf (value : Json) (arity : Option Nat := none) : IO (Array Json) := do
  let xs ← jsonResult value.getArr?
  if let some count := arity then
    if xs.size != count then fail "ARITY"
  return xs

def natOf (value : Json) : IO Nat := do
  let n ← jsonResult value.getNat?
  if n > 18446744073709551615 then fail "UINT64"
  return n

def u32Of (value : Json) : IO Nat := do
  let n ← natOf value
  if n > 4294967295 then fail "UINT32"
  return n

def indexOf (value : Json) (bound : Nat) : IO Nat := do
  let i ← natOf value
  if i >= bound then fail "BACKWARD_INDEX"
  return i

def boolOf (value : Json) : IO Bool := do
  match ← natOf value with
  | 0 => pure false
  | 1 => pure true
  | _ => fail "BOOL_CODE"

def bytesJson (bytes : ByteArray) : Json :=
  Json.mkObj [("$bytes", arr (bytes.data.map (fun b => num b.toNat)))]

def bytesOf (value : Json) (maximum : Nat) : IO ByteArray := do
  let object ← jsonResult value.getObj?
  if object.size != 1 then fail "BYTES_OBJECT"
  let some raw := object.get? "$bytes" | fail "BYTES_KEY"
  let values ← arrayOf raw
  if values.size > maximum then fail "BYTES_BOUND"
  let mut result : ByteArray := ⟨#[]⟩
  for value in values do
    let n ← natOf value
    if n > 255 then fail "BYTE_RANGE"
    result := result.push (UInt8.ofNat n)
  return result

def rootComponent : Name → Name
  | .anonymous => .anonymous
  | n@(.str .anonymous _) => n
  | n@(.num .anonymous _) => n
  | .str parent _ | .num parent _ => rootComponent parent

/-- A role restriction for semantic names, not for inert binder labels. -/
def forbiddenSemanticName (name : Name) : Bool :=
  name == ``Lean.reduceBool || name == ``Lean.reduceNat ||
  match rootComponent name with
  | .anonymous | .num _ _ => true
  | .str _ component =>
      ["_kernel_fresh", "_ind_fresh", "_nested_fresh", "_uniq", "_nested"].any
        (fun reserved : String => component.startsWith reserved) ||
      ["dontcare", "__expr_for_default_constructor__",
       "__local_decl_for_default_constructor"].contains component

def requireSemanticName (name : Name) : IO Unit := do
  if forbiddenSemanticName name then fail "FORBIDDEN_SEMANTIC_NAME"

/-- Name grammar permits anonymous binders. Semantic callers apply their role check. -/
def encodeName (name : Name) (limits : Limits := {}) : IO Json := do
  let mut current := name
  let mut reversed : Array Json := #[]
  let mut byteCount := 0
  while !current.isAnonymous do
    if reversed.size >= limits.maxNameParts then fail "NAME_PART_BOUND"
    match current with
    | .anonymous => pure ()
    | .str parent component =>
        byteCount := byteCount + component.utf8ByteSize
        if byteCount > limits.maxNameBytes then fail "NAME_BYTE_BOUND"
        reversed := reversed.push (arr #[num 0, bytesJson component.toUTF8])
        current := parent
    | .num parent n =>
        if n > 4294967295 then fail "NAME_UINT32"
        reversed := reversed.push (arr #[num 1, num n])
        current := parent
  return arr reversed.reverse

def decodeName (value : Json) (limits : Limits := {}) : IO Name := do
  let components ← arrayOf value
  if components.size > limits.maxNameParts then fail "NAME_PART_BOUND"
  let mut name := Name.anonymous
  let mut byteCount := 0
  for component in components do
    let pair ← arrayOf component (some 2)
    match ← natOf pair[0]! with
    | 0 =>
        let bytes ← bytesOf pair[1]! (limits.maxNameBytes - byteCount)
        byteCount := byteCount + bytes.size
        let some text := String.fromUTF8? bytes | fail "NAME_UTF8"
        if text.toUTF8 != bytes then fail "NAME_UTF8_CANONICAL"
        name := .str name text
    | 1 => name := .num name (← u32Of pair[1]!)
    | _ => fail "NAME_TAG"
  return name

def validateParams (params : List Name) (limits : Limits := {}) : IO Unit := do
  if params.length > limits.maxParams then fail "PARAMETER_BOUND"
  let mut seen : Std.HashSet Name := {}
  for parameter in params do
    if parameter.isAnonymous || seen.contains parameter then fail "PARAMETER_NAME"
    discard <| encodeName parameter limits
    seen := seen.insert parameter

def binderCode : BinderInfo → Nat
  | .default => 0
  | .implicit => 1
  | .strictImplicit => 2
  | .instImplicit => 3

def binderOf (value : Json) : IO BinderInfo := do
  match ← natOf value with
  | 0 => pure .default
  | 1 => pure .implicit
  | 2 => pure .strictImplicit
  | 3 => pure .instImplicit
  | _ => fail "BINDER_CODE"

def checkedDepth (limits : Limits) (depth : Nat) : IO Nat := do
  if depth > limits.maxDepth then fail "DEPTH_BOUND"
  return depth

def magnitude (value : Nat) (maximum : Nat) : IO ByteArray := do
  let mut remaining := value
  let mut bytes : Array UInt8 := #[]
  while remaining > 0 do
    if bytes.size >= maximum then fail "NAT_BYTE_BOUND"
    bytes := bytes.push (UInt8.ofNat (remaining % 256))
    remaining := remaining / 256
  return ⟨bytes.reverse⟩

structure Encoder where
  levels : Array Json := #[]
  exprs : Array Json := #[]
  levelDepths : Array Nat := #[]
  exprDepths : Array Nat := #[]
  levelNodes : Std.HashMap Json Nat := {}
  exprNodes : Std.HashMap Json Nat := {}
  levelMemo : Std.HashMap Level Nat := {}
  /-- ExprStructEq uses Expr.equal, including binder names and annotations. -/
  exprMemo : Std.HashMap ExprStructEq Nat := {}
  literalBytes : Nat := 0
  deriving Inhabited

abbrev EncodeM := StateT Encoder IO

def internLevel (limits : Limits) (node : Json) (depth : Nat) : EncodeM Nat := do
  let state ← get
  if let some i := state.levelNodes[node]? then return i
  discard <| checkedDepth limits depth
  if state.levels.size >= limits.maxLevels then fail "LEVEL_NODE_BOUND"
  let i := state.levels.size
  set { state with
    levels := state.levels.push node
    levelDepths := state.levelDepths.push depth
    levelNodes := state.levelNodes.insert node i }
  return i

partial def encodeLevel (limits : Limits) (params : List Name)
    (level : Level) (fuel : Nat) : EncodeM Nat := do
  if let some i := (← get).levelMemo[level]? then return i
  if fuel == 0 then fail "LEVEL_SOURCE_DEPTH"
  let (node, depth) ← match level with
    | .zero => pure (arr #[num 0], 1)
    | .succ child => do
        let i ← encodeLevel limits params child (fuel - 1)
        pure (arr #[num 1, num i], (← get).levelDepths[i]! + 1)
    | .max left right | .imax left right => do
        let i ← encodeLevel limits params left (fuel - 1)
        let k ← encodeLevel limits params right (fuel - 1)
        let tag := match level with | .max .. => 2 | _ => 3
        let state ← get
        pure (arr #[num tag, num i, num k], max state.levelDepths[i]! state.levelDepths[k]! + 1)
    | .param parameter => do
        let i := params.idxOf parameter
        if i >= params.length then fail "UNDECLARED_LEVEL_PARAMETER"
        pure (arr #[num 4, num i], 1)
    | .mvar _ => fail "LEVEL_METAVARIABLE"
  let i ← internLevel limits node depth
  modify fun state => { state with levelMemo := state.levelMemo.insert level i }
  return i

def internExpr (limits : Limits) (node : Json) (depth : Nat)
    (literalBytes : Nat := 0) : EncodeM Nat := do
  let state ← get
  if let some i := state.exprNodes[node]? then return i
  discard <| checkedDepth limits depth
  if state.exprs.size >= limits.maxExprs then fail "EXPRESSION_NODE_BOUND"
  if state.literalBytes + literalBytes > limits.maxTotalLiteralBytes then
    fail "TOTAL_LITERAL_BYTES"
  let i := state.exprs.size
  set { state with
    exprs := state.exprs.push node
    exprDepths := state.exprDepths.push depth
    exprNodes := state.exprNodes.insert node i
    literalBytes := state.literalBytes + literalBytes }
  return i

partial def encodeExpr (limits : Limits) (params : List Name)
    (expr : Expr) (fuel : Nat) : EncodeM Nat := do
  if let some i := (← get).exprMemo[ExprStructEq.mk expr]? then return i
  if fuel == 0 then fail "EXPRESSION_SOURCE_DEPTH"
  if let .mdata _ body := expr then
    let i ← encodeExpr limits params body (fuel - 1)
    modify fun state => { state with exprMemo := state.exprMemo.insert (ExprStructEq.mk expr) i }
    return i
  let (node, depth, literalBytes) ← match expr with
    | .bvar i => do
        if i > 4294967295 then fail "BVAR_UINT32"
        pure (arr #[num 0, num i], 1, 0)
    | .sort level => do
        let i ← encodeLevel limits params level limits.maxDepth
        pure (arr #[num 1, num i], (← get).levelDepths[i]! + 1, 0)
    | .const name levels => do
        requireSemanticName name
        if levels.length > limits.maxParams then fail "LEVEL_INSTANCE_BOUND"
        let mut indices : Array Json := #[]
        let mut depth := 0
        for level in levels do
          let i ← encodeLevel limits params level limits.maxDepth
          indices := indices.push (num i)
          depth := max depth (← get).levelDepths[i]!
        pure (arr #[num 2, ← encodeName name limits, arr indices], depth + 1, 0)
    | .app fn arg => do
        let i ← encodeExpr limits params fn (fuel - 1)
        let k ← encodeExpr limits params arg (fuel - 1)
        let state ← get
        pure (arr #[num 3, num i, num k], max state.exprDepths[i]! state.exprDepths[k]! + 1, 0)
    | .lam name type body bi | .forallE name type body bi => do
        let i ← encodeExpr limits params type (fuel - 1)
        let k ← encodeExpr limits params body (fuel - 1)
        let state ← get
        let tag := match expr with | .lam .. => 4 | _ => 5
        pure (arr #[num tag, ← encodeName name limits, num (binderCode bi), num i, num k],
          max state.exprDepths[i]! state.exprDepths[k]! + 1, 0)
    | .letE name type value body nondep => do
        let i ← encodeExpr limits params type (fuel - 1)
        let k ← encodeExpr limits params value (fuel - 1)
        let l ← encodeExpr limits params body (fuel - 1)
        let state ← get
        pure (arr #[num 6, ← encodeName name limits, num i, num k, num l,
          num (if nondep then 1 else 0)],
          max (max state.exprDepths[i]! state.exprDepths[k]!) state.exprDepths[l]! + 1, 0)
    | .lit (.natVal value) => do
        let bytes ← magnitude value limits.maxLiteralBytes
        pure (arr #[num 7, bytesJson bytes], 1, bytes.size)
    | .proj name field value => do
        requireSemanticName name
        if field > 4294967295 then fail "PROJECTION_UINT32"
        let i ← encodeExpr limits params value (fuel - 1)
        pure (arr #[num 8, ← encodeName name limits, num field, num i],
          (← get).exprDepths[i]! + 1, 0)
    | .lit (.strVal value) => do
        if value.utf8ByteSize > limits.maxLiteralBytes then fail "STRING_BYTE_BOUND"
        pure (arr #[num 9, bytesJson value.toUTF8], 1, value.utf8ByteSize)
    | _ => fail "FREE_OR_META_EXPRESSION"
  let i ← internExpr limits node depth literalBytes
  modify fun state => { state with exprMemo := state.exprMemo.insert (ExprStructEq.mk expr) i }
  return i

/-- Encode a closed expression, preserving its ordinary API metadata except mdata. -/
def encode (params : List Name) (expr : Expr) (limits : Limits := {}) : IO Json := do
  validateParams params limits
  if expr.hasLooseBVars || expr.hasFVar || expr.hasMVar then fail "OPEN_EXPRESSION"
  let (root, state) ← (encodeExpr limits params expr limits.maxDepth).run {}
  if root + 1 != state.exprs.size then fail "INTERNAL_ROOT"
  return arr #[Json.str format, arr state.levels, arr state.exprs, num root]

def referenceOf (allowed : Std.HashSet Name) (value : Json) (limits : Limits) : IO Name := do
  let name ← decodeName value limits
  requireSemanticName name
  if !allowed.contains name then fail "UNBOUND_REFERENCE"
  return name

/-- Decode inert data only. This establishes syntax, not any mathematical judgment. -/
def decode (params : List Name) (allowed : Std.HashSet Name) (value : Json)
    (limits : Limits := {}) : IO Expr := do
  validateParams params limits
  let packet ← arrayOf value (some 4)
  if (← jsonResult packet[0]!.getStr?) != format then fail "FORMAT"
  let rawLevels ← arrayOf packet[1]!
  let rawExprs ← arrayOf packet[2]!
  if rawLevels.size > limits.maxLevels then fail "LEVEL_NODE_BOUND"
  if rawExprs.isEmpty || rawExprs.size > limits.maxExprs then fail "EXPRESSION_NODE_BOUND"
  let mut levels : Array Level := #[]
  let mut levelDepths : Array Nat := #[]
  for raw in rawLevels do
    let node ← arrayOf raw
    if node.isEmpty then fail "EMPTY_LEVEL_NODE"
    let (level, depth) ← match ← natOf node[0]! with
      | 0 => do
          discard <| arrayOf raw (some 1)
          let depth ← checkedDepth limits 1
          pure (Level.zero, depth)
      | 1 => do
          discard <| arrayOf raw (some 2)
          let i ← indexOf node[1]! levels.size
          let depth ← checkedDepth limits (levelDepths[i]! + 1)
          pure (Level.succ levels[i]!, depth)
      | 2 | 3 => do
          discard <| arrayOf raw (some 3)
          let i ← indexOf node[1]! levels.size
          let k ← indexOf node[2]! levels.size
          let depth ← checkedDepth limits (max levelDepths[i]! levelDepths[k]! + 1)
          pure ((if (← natOf node[0]!) == 2 then Level.max else Level.imax) levels[i]! levels[k]!, depth)
      | 4 => do
          discard <| arrayOf raw (some 2)
          let i ← indexOf node[1]! params.length
          let depth ← checkedDepth limits 1
          pure (Level.param params[i]!, depth)
      | _ => fail "LEVEL_TAG"
    levels := levels.push level
    levelDepths := levelDepths.push depth
  let mut exprs : Array Expr := #[]
  let mut depths : Array Nat := #[]
  let mut needs : Array Nat := #[]
  let mut literalBytes := 0
  for raw in rawExprs do
    let node ← arrayOf raw
    if node.isEmpty then fail "EMPTY_EXPRESSION_NODE"
    let tag ← natOf node[0]!
    let (expr, depth, need) ← match tag with
      | 0 => do
          discard <| arrayOf raw (some 2)
          let i ← u32Of node[1]!
          let depth ← checkedDepth limits 1
          pure (Expr.bvar i, depth, i + 1)
      | 1 => do
          discard <| arrayOf raw (some 2)
          let i ← indexOf node[1]! levels.size
          let depth ← checkedDepth limits (levelDepths[i]! + 1)
          pure (Expr.sort levels[i]!, depth, 0)
      | 2 => do
          discard <| arrayOf raw (some 3)
          let name ← referenceOf allowed node[1]! limits
          let rawInstances ← arrayOf node[2]!
          if rawInstances.size > limits.maxParams then fail "LEVEL_INSTANCE_BOUND"
          let mut instances : Array Level := #[]
          let mut instanceDepth := 0
          for rawIndex in rawInstances do
            let i ← indexOf rawIndex levels.size
            instances := instances.push levels[i]!
            instanceDepth := max instanceDepth levelDepths[i]!
          let depth ← checkedDepth limits (instanceDepth + 1)
          pure (Expr.const name instances.toList, depth, 0)
      | 3 => do
          discard <| arrayOf raw (some 3)
          let i ← indexOf node[1]! exprs.size
          let k ← indexOf node[2]! exprs.size
          let depth ← checkedDepth limits (max depths[i]! depths[k]! + 1)
          pure (Expr.app exprs[i]! exprs[k]!, depth, max needs[i]! needs[k]!)
      | 4 | 5 => do
          discard <| arrayOf raw (some 5)
          let name ← decodeName node[1]! limits
          let bi ← binderOf node[2]!
          let i ← indexOf node[3]! exprs.size
          let k ← indexOf node[4]! exprs.size
          let depth ← checkedDepth limits (max depths[i]! depths[k]! + 1)
          let expr := if tag == 4 then Expr.lam name exprs[i]! exprs[k]! bi
            else Expr.forallE name exprs[i]! exprs[k]! bi
          pure (expr, depth, max needs[i]! (needs[k]! - 1))
      | 6 => do
          discard <| arrayOf raw (some 6)
          let name ← decodeName node[1]! limits
          let i ← indexOf node[2]! exprs.size
          let k ← indexOf node[3]! exprs.size
          let l ← indexOf node[4]! exprs.size
          let nondep ← boolOf node[5]!
          let depth ← checkedDepth limits (max (max depths[i]! depths[k]!) depths[l]! + 1)
          pure (Expr.letE name exprs[i]! exprs[k]! exprs[l]! nondep,
            depth, max (max needs[i]! needs[k]!) (needs[l]! - 1))
      | 7 | 9 => do
          discard <| arrayOf raw (some 2)
          let bytes ← bytesOf node[1]! (min limits.maxLiteralBytes (limits.maxTotalLiteralBytes - literalBytes))
          literalBytes := literalBytes + bytes.size
          let depth ← checkedDepth limits 1
          if tag == 7 then
            if !bytes.isEmpty && bytes[0]! == 0 then fail "NAT_MAGNITUDE_CANONICAL"
            let n := bytes.data.foldl (fun n byte => n * 256 + byte.toNat) 0
            pure (Expr.lit (.natVal n), depth, 0)
          else
            let some text := String.fromUTF8? bytes | fail "STRING_UTF8"
            if text.toUTF8 != bytes then fail "STRING_UTF8_CANONICAL"
            pure (Expr.lit (.strVal text), depth, 0)
      | 8 => do
          discard <| arrayOf raw (some 4)
          let name ← referenceOf allowed node[1]! limits
          let field ← u32Of node[2]!
          let i ← indexOf node[3]! exprs.size
          let depth ← checkedDepth limits (depths[i]! + 1)
          pure (Expr.proj name field exprs[i]!, depth, needs[i]!)
      | _ => fail "EXPRESSION_TAG"
    exprs := exprs.push expr
    depths := depths.push depth
    needs := needs.push need
  let root ← indexOf packet[3]! exprs.size
  if root + 1 != exprs.size || needs[root]! != 0 then fail "ROOT_OR_SCOPE"
  let result := exprs[root]!
  -- Re-encoding preserves sharing and validates unique nodes, reachability and
  -- left-to-right postorder without expanding the represented expression tree.
  if (← encode params result limits) != value then fail "NONCANONICAL_DAG"
  return result

end OrdinaryLean.ExprCodec
