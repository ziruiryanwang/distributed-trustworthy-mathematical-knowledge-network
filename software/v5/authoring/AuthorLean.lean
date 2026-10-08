/- Adapted from leanprover/lean4export, commit
ddeb0869b0b5679b0104e16291ffd929fbaa6a48, Export.lean (Apache-2.0).
See ../workloads/LEAN4EXPORT-LICENSE for the unchanged upstream license.
Serializer prefix retained from the frozen project Export03.lean, with a new
Lean-only import, exporter name and owner-source workload entrypoint below.
Exclusive bounded file output, explicit wire ranges and safe-only refusal
remain. This is an untrusted serialization boundary, not module admission.
Upstream serializer toolchain was4.29.0-rc1; compatibility with selected4.34
is a gate, not inferred from NDJSON3.1 format compatibility. -/
import Lean.Elab.Frontend
import Std.Data.HashMap.Basic

open Lean
open Std (HashMap)

def Lean.BinderInfo.toJson : BinderInfo → Json
  | .default => "default"
  | .implicit => "implicit"
  | .strictImplicit => "strictImplicit"
  | .instImplicit => "instImplicit"

def Lean.ReducibilityHints.toJson : ReducibilityHints → Json
  | .opaque => "opaque"
  | .abbrev => "abbrev"
  | .regular n => .mkObj [("regular", n.toNat)]

def Lean.QuotKind.toJson : QuotKind → Json
  | type => "type"
  | ctor => "ctor"
  | lift => "lift"
  | ind => "ind"

def Lean.DefinitionSafety.toJson : DefinitionSafety → Json
  | «unsafe» => "unsafe"
  | safe => "safe"
  | «partial» => "partial"

def Lean.KVMap.toJson (kvs: Lean.KVMap) : Json :=
  .mkObj <| kvs.entries.map (fun (k, v) => (k.toString, reprStr v))

structure Context where
  env : Environment
  output : IO.FS.Handle
  boundaries : NameHashSet

structure State where
  visitedNames : HashMap Name Nat := HashMap.emptyWithCapacity 1024 |>.insert .anonymous 0
  visitedLevels : HashMap Level Nat := HashMap.emptyWithCapacity 256 |>.insert .zero 0
  visitedExprs : HashMap ExprStructEq Nat := HashMap.emptyWithCapacity 16384
  visitedConstants : NameHashSet := {}
  bytesWritten : Nat := 0
  allRows : Array Json := #[]
  declarationRows : Array Json := #[]
  noMDataExprs : HashMap ExprStructEq Expr := HashMap.emptyWithCapacity 16384
  exportMData : Bool := false
  exportUnsafe : Bool := false
  /-- Maps the name of an inductive type to a list of names of corresponding recursors.
  This is used to facilitate exporting of related inductives, constructors, and recursors as a unit. -/
  recursorMap : NameMap NameSet := {}

abbrev M := ReaderT Context <| StateT State IO

def writeLine (value : Json) : M Unit := do
  let line := value.compress ++ "\n"
  let count := line.toUTF8.size
  if count > 8 * 1024 * 1024 || (← get).bytesWritten + count > 64 * 1024 * 1024 then
    throw <| IO.userError "EXPORT_BYTE_LIMIT"
  (← read).output.putStr line
  modify fun st => { st with bytesWritten := st.bytesWritten + count, allRows := st.allRows.push value }

def wire16 (n : Nat) : M Unit := do
  if n >= 65536 then throw <| IO.userError "WIRE_U16_RANGE"

def M.run (env : Environment) (output : IO.FS.Handle) (boundaries : NameHashSet) (act : M α) : IO (α × State) :=
  StateT.run (s := {}) <| ReaderT.run (r := { env, output, boundaries }) act

/--
Initialize the exporter state from an environment and cli options.
The `recursorMap` maps each inductive declaration's name to the list
of relevant recursors, which is used to ensure that for any inductive
declaration, the inductives, constructors, and recursors are exported
together in that order.
-/
def initState (env : Environment) (cliOptions : List String := []) : M Unit := do
  let mut recursorMap : NameMap NameSet := {}
  for (_, constInfo) in env.constants do
    if let .recInfo recVal := constInfo then
      for indName in recVal.all do
        recursorMap := recursorMap.alter indName <|
          fun
          | none => some <| NameSet.empty.insert recVal.name
          | some recNames => some <| recNames.insert recVal.name
  modify fun st => { st with
    exportMData  := cliOptions.any  (· == "--export-mdata")
    exportUnsafe := cliOptions.any (· == "--export-unsafe")
    recursorMap
  }

/--
For a given primitive (name, level, expr) to be exported:
IFF it's been seen before, return its index within the export file
IFF it has not been seen before, add it to the cache, print it into the export, and return its cache index.
-/
@[inline]
def getIdx [Hashable α] [BEq α] (x : α) (namespaced: String) (getM : State → HashMap α Nat) (setM : State → HashMap α Nat → State) (rec : M Json) : M Nat := do
  let m ← getM <$> get
  if let some idx := m[x]? then
    return idx
  let s ← rec
  let m ← getM <$> get
  let idx := m.size
  if idx >= 1000000 then throw <| IO.userError "EXPORT_NODE_LIMIT"
  writeLine (s.setObjVal! namespaced idx)
  modify fun st => setM st ((getM st).insert x idx)
  return idx

def dumpName (n : Name) : M Nat := getIdx n "in" (·.visitedNames) ({ · with visitedNames := · }) do
  match n with
  | .anonymous => unreachable!
  | .str n s =>
    return .mkObj [
      ("str", .mkObj [
        ("pre", ← dumpName n),
        ("str", s)
      ])
    ]
  | .num n i =>
    if i >= 4294967296 then throw <| IO.userError "NAME_U32_RANGE"
    return .mkObj [
      ("num", .mkObj [
        ("pre", ← dumpName n),
        ("i", i)
      ])
    ]

def dumpLevel (l : Level) : M Nat := getIdx l "il" (·.visitedLevels) ({ · with visitedLevels := · }) do
  match l with
  | .zero => unreachable!
  | .mvar _ => throw <| IO.userError "LEVEL_METAVARIABLE"
  | .succ l => return .mkObj [("succ", ← dumpLevel l)]
  | .max l1 l2 => return .mkObj [("max", Json.arr #[← dumpLevel l1, ← dumpLevel l2])]
  | .imax l1 l2 => return .mkObj [("imax", Json.arr #[← dumpLevel l1, ← dumpLevel l2])]
  | .param n => return .mkObj [("param", ← dumpName n)]

def dumpUparams (uparams : List Name) : M Json := do
  let nameIdxs ← uparams.mapM dumpName
  let _ ← (uparams.map (Level.param)).mapM dumpLevel
  pure nameIdxs.toJson

def dumpNames (uparams : List Name) : M Json := do
  let nameIdxs ← uparams.mapM dumpName
  return nameIdxs.toJson

def removeMData (e : Expr) : M Expr := do
  if let some x := (← get).noMDataExprs[ExprStructEq.mk e]? then
    return x
  let e' ← match e with
  | .mdata _ e' => removeMData e'
  | .fvar .. | .mvar .. => throw <| IO.userError "FREE_OR_META_EXPRESSION"
  | .bvar .. | .sort .. | .const .. | .lit _ => pure e
  | .app f a =>
    pure <| e.updateApp! (← removeMData f) (← removeMData a)
  | .lam _ d b bi =>
    pure <| .lam .anonymous (← removeMData d) (← removeMData b) bi
  | .letE _ d v b _ =>
    -- Normalize `nonDep` to `false` to avoid duplicate expression indices.
    -- Lean's `BEq` for `Expr` considers the `nonDep` flag, but external type checkers
    -- (e.g., nanoda_lib) treat expressions as identical regardless of this optimization hint.
    -- Without normalization, the same expression can get different indices, causing parse errors.
    -- See: https://github.com/ammkrn/lean4export/commit/eb023e5
    pure <| .letE .anonymous (← removeMData d) (← removeMData v) (← removeMData b) false
  | .forallE _ d b bi =>
    pure <| .forallE .anonymous (← removeMData d) (← removeMData b) bi
  | .proj _ _ e2 =>
    pure <| e.updateProj! (← removeMData e2)
  modify (fun st => { st with noMDataExprs := st.noMDataExprs.insert (ExprStructEq.mk e) e' })
  pure e'

mutual

partial def dumpExprAux (e : Expr) : M Nat := do
  getIdx (ExprStructEq.mk e) "ie" (·.visitedExprs) ({ · with visitedExprs := · }) do
    match e with
    | .fvar .. | .mvar .. => throw <| IO.userError "FREE_OR_META_EXPRESSION"
    | .mdata a e' =>
      return .mkObj [
        ("mdata", .mkObj [
            ("data", a.toJson),
            ("expr", ← dumpExprAux e')
        ])
      ]
    | .bvar i =>
      if i >= 65535 then throw <| IO.userError "BVAR_U16_DEPTH_RANGE"
      return .mkObj [("bvar", i)]
    | .lit (.natVal i) => dumpNatDeps; return .mkObj [("natVal", s!"{i}")]
    | .lit (.strVal s) => dumpStrDeps; return .mkObj [("strVal", s)]
    | .sort l => return .mkObj [("sort", ← dumpLevel l)]
    | .const n us => return .mkObj [
      ("const", .mkObj [
        ("name", ← dumpName n),
        ("us", (← us.mapM dumpLevel).toJson)
      ])
    ]
    | .app f a => return .mkObj [
      ("app", .mkObj [
        ("fn", ← dumpExprAux f),
        ("arg", ← dumpExprAux a)
      ])
    ]
    | .lam n d b bi => return .mkObj [
      ("lam", .mkObj [
        ("name", ← dumpName n),
        ("type", ← dumpExprAux d),
        ("body", ← dumpExprAux b),
        ("binderInfo", bi.toJson)
      ])
    ]
    | .forallE n d b bi => return .mkObj [
      ("forallE", .mkObj [
        ("name", ← dumpName n),
        ("type", ← dumpExprAux d),
        ("body", ← dumpExprAux b),
        ("binderInfo", bi.toJson)
      ])
    ]
    | .letE n d v b nondep => return .mkObj [
      ("letE", .mkObj [
        ("name", ← dumpName n),
        ("type", ← dumpExprAux d),
        ("value", ← dumpExprAux v),
        ("body", ← dumpExprAux b),
        ("nondep", nondep)
      ])
    ]
    | .proj s i e =>
      if i >= 4294967296 then throw <| IO.userError "PROJECTION_U32_RANGE"
      return .mkObj [
      ("proj", .mkObj [
        ("typeName", ← dumpName s),
        ("idx", i),
        ("struct", ← dumpExprAux e)
      ])
    ]
where
  dumpNatDeps : M Unit := do
    let nat := ``Nat
    if ((← read).env.find? nat).isNone then throw <| IO.userError "NAT_LITERAL_SUPPORT_MISSING"
    if !(← get).visitedConstants.contains nat then dumpConstant nat
  dumpStrDeps : M Unit := do
    let charOfNat := ``Char.ofNat
    if ((← read).env.find? charOfNat).isNone then throw <| IO.userError "STRING_LITERAL_SUPPORT_MISSING"
    if !(← get).visitedConstants.contains charOfNat then dumpConstant charOfNat
    let stringOfList := ``String.ofList
    if ((← read).env.find? stringOfList).isNone then throw <| IO.userError "STRING_LITERAL_SUPPORT_MISSING"
    if !(← get).visitedConstants.contains stringOfList then dumpConstant stringOfList

partial def dumpExpr (e : Expr) : M Nat := do
    let aux (e : Expr) : M Expr := do
      modify (fun st => { st with noMDataExprs := HashMap.emptyWithCapacity })
      removeMData e
    dumpExprAux <| ← if (← get).exportMData then pure e else aux e

partial def dumpConstant (c : Name) : M Unit := do
  let some declar := (← read).env.find? c
    | throw <| IO.userError s!"MISSING_NATIVE_CONSTANT {c}"
  if declar.isUnsafe || declar.isPartial then
    throw <| IO.userError s!"UNSAFE_OR_PARTIAL_NATIVE_CONSTANT {c}"
  if (← get).visitedConstants.contains c then return
  if (← get).visitedConstants.size >= 4096 then
    throw <| IO.userError "EXPORT_DECLARATION_LIMIT"
  modify fun st => { st with visitedConstants := st.visitedConstants.insert c }
  if (← read).boundaries.contains c then return
  match declar with
  | .axiomInfo _ => throw <| IO.userError s!"NEW_AXIOM_REFUSED {c}"
  | .defnInfo val => do
    dumpDeps val.type
    dumpDeps val.value
    dumpObj [
      ("def", Json.mkObj [
        ("name", ← dumpName val.name),
        ("levelParams", ← dumpUparams val.levelParams),
        ("type", ← dumpExpr val.type),
        ("value", ← dumpExpr val.value),
        ("hints", val.hints.toJson),
        ("safety", val.safety.toJson),
        ("all", ← dumpNames val.all)
      ])
    ]
  | .opaqueInfo val => do
    dumpDeps val.type
    dumpDeps val.value
    dumpObj [
      ("opaque", Json.mkObj [
        ("name", ← dumpName val.name),
        ("levelParams", ← dumpUparams val.levelParams),
        ("type", ← dumpExpr val.type),
        ("value", ← dumpExpr val.value),
        ("all", ← dumpNames val.all),
        ("isUnsafe", val.isUnsafe)
      ])
    ]
  | .thmInfo val => do
    dumpDeps val.type
    dumpDeps val.value
    dumpObj [
      ("thm", Json.mkObj [
        ("name", ← dumpName val.name),
        ("levelParams", ← dumpUparams val.levelParams),
        ("type", ← dumpExpr val.type),
        ("value", ← dumpExpr val.value),
        ("all", ← dumpNames val.all)
      ])
    ]
  | .quotInfo _ => throw <| IO.userError s!"NEW_QUOTIENT_REFUSED {c}"
  | .inductInfo baseIndVal => do
    let mut indVals := #[]
    let mut ctorVals := #[]
    let mut recursorNames := NameSet.empty
    for indName in baseIndVal.all do
      let val := ((← read).env.find? indName |>.get!).inductiveVal!
      assert! ((!val.isUnsafe) || (← get).exportUnsafe)
      indVals := indVals.push val
      for ctor in val.ctors do
        match ((← read).env.find? ctor |>.get!) with
        | .ctorInfo ctorVal =>
          assert! ((!ctorVal.isUnsafe) || (← get).exportUnsafe)
          ctorVals := ctorVals.push ctorVal
        | _ => panic! "Expected a `ConstantInfo.ctorInfo`."
      modify fun st => { st with visitedConstants:= st.visitedConstants.insert indName }
      if (← get).visitedConstants.size > 4096 then throw <| IO.userError "EXPORT_DECLARATION_LIMIT"
      dumpDeps val.type
      if let .some names := (← get).recursorMap.get? indName
      then recursorNames := recursorNames.union names
      else assert! ctorVals.size == 0

    /- We dump the constructor dependencies (which will not include the inductives in this block since we've
    added the names to `visitedConstants`) before actually outputting anything in this inductive block to
    ensure e.g. the `LT` in `Fin.mk` is dumped before this inductive block appears in the export file. -/
    for ctorVal in ctorVals do
      modify fun st => { st with visitedConstants:= st.visitedConstants.insert ctorVal.name }
      if (← get).visitedConstants.size > 4096 then throw <| IO.userError "EXPORT_DECLARATION_LIMIT"
      dumpDeps ctorVal.type

    let mut recursorVals := #[]
    for recursorName in recursorNames do
      match ((← read).env.find? recursorName |>.get!) with
      | .recInfo recVal =>
        assert! ((!recVal.isUnsafe) || (← get).exportUnsafe)
        recursorVals := recursorVals.push recVal
      | _ => panic! "expected a `constantinfo.recinfo`."
    for recursorVal in recursorVals do
      modify fun st => { st with visitedConstants:= st.visitedConstants.insert recursorVal.name }
      if (← get).visitedConstants.size > 4096 then throw <| IO.userError "EXPORT_DECLARATION_LIMIT"
      dumpDeps recursorVal.type

    /- We only dump these after we've already dumped the `recursorVal` type and added the name
    to `visitedConstants` so that `dumpDeps` does not retry dumping the appearance of `Foo.rec` -/
    for recursorVal in recursorVals do
      for rule in recursorVal.rules do
        dumpDeps rule.rhs

    let inductiveValsJson ← indVals.mapM <| fun indVal => do
      for n in [indVal.numParams, indVal.numIndices, indVal.numNested] do wire16 n
      pure <| Json.mkObj [
          ("name", ← dumpName indVal.name),
          ("levelParams", ← dumpUparams indVal.levelParams),
          ("type", ← dumpExpr indVal.type),
          ("numParams", indVal.numParams),
          ("numIndices", indVal.numIndices),
          ("all", ← dumpNames indVal.all),
          ("ctors", ← dumpNames indVal.ctors),
          ("numNested", indVal.numNested),
          ("isRec", indVal.isRec),
          ("isReflexive", indVal.isReflexive),
          ("isUnsafe", indVal.isUnsafe),
      ]
    let ctorValsJson ← ctorVals.mapM <| fun ctorVal => do
      for n in [ctorVal.cidx, ctorVal.numParams, ctorVal.numFields] do wire16 n
      pure <| Json.mkObj [
          ("name", ← dumpName ctorVal.name),
          ("levelParams", ← dumpUparams ctorVal.levelParams),
          ("type", ← dumpExpr ctorVal.type),
          ("induct", ← dumpName ctorVal.induct),
          ("cidx", ctorVal.cidx),
          ("numParams", ctorVal.numParams),
          ("numFields", ctorVal.numFields),
          ("isUnsafe", ctorVal.isUnsafe)
      ]
    let recursorValsJson ← recursorVals.mapM <| fun recursorVal => do
      for n in [recursorVal.numParams, recursorVal.numIndices, recursorVal.numMotives, recursorVal.numMinors] do wire16 n
      pure <| Json.mkObj [
          ("name", ← dumpName recursorVal.name),
          ("levelParams", ← dumpUparams recursorVal.levelParams),
          ("type", ← dumpExpr recursorVal.type),
          ("all", ← dumpNames recursorVal.all),
          ("numParams", recursorVal.numParams),
          ("numIndices", recursorVal.numIndices),
          ("numMotives", recursorVal.numMotives),
          ("numMinors", recursorVal.numMinors),
          ("rules", (← recursorVal.rules.mapM dumpRecRule).toJson),
          ("k", recursorVal.k),
          ("isUnsafe", recursorVal.isUnsafe),
      ]
    dumpObj [
      ("inductive", Json.mkObj [
        ("types", inductiveValsJson.toJson),
        ("ctors", ctorValsJson.toJson),
        ("recs", recursorValsJson.toJson),
      ])
    ]
  | .ctorInfo val => dumpConstant val.induct
  | .recInfo val =>
    for indName in val.all do
      dumpConstant indName
where
  dumpDeps e := do
    for c in e.getUsedConstants do
      dumpConstant c
  /- Return these for inclusion inline with the exported `recInfo`. -/
  dumpRecRule (rule : RecursorRule) : M Json := do
    wire16 rule.nfields
    return Json.mkObj [
      ("ctor", ← dumpName rule.ctor),
      ("nfields", rule.nfields),
      ("rhs", ← dumpExpr rule.rhs),
    ]
  dumpObj (fields : List (String × Json)) : M Unit := do
    let row := Json.mkObj fields
    writeLine row
    modify fun st => { st with declarationRows := st.declarationRows.push row }

end

def exportMetadata : Json :=
  let leanMeta := Json.mkObj [
    ("version", versionString),
    ("githash", githash)
  ]
  let exporterMeta := Json.mkObj [
    ("name", "v5/certified-context-owner-source-export"),
    ("version", "3.1.0")
  ]
  let formatMeta := Json.mkObj [
    ("version", "3.1.0")
  ]

  Json.mkObj [
    ("meta", Json.mkObj [
      ("exporter", exporterMeta),
      ("lean", leanMeta),
      ("format", formatMeta)
    ])
  ]

def dumpMetadata : M Unit := do
  writeLine exportMetadata

/- V5 owner-source export adapter. The serialized terms must be rechecked by
   the independent relation; this source execution is not a security sandbox. -/

namespace SourceFrontend

def fail {α : Type} (s : String) : IO α := throw <| IO.userError s

def checked {α : Type} (r : Except String α) : IO α :=
  match r with
  | .ok value => pure value
  | .error detail => fail s!"AUTHOR_JSON {detail}"

def field (j : Json) (key : String) : IO Json := checked (j.getObjVal? key)
def array (j : Json) : IO (Array Json) := checked j.getArr?
def string (j : Json) : IO String := checked j.getStr?
def natural (j : Json) : IO Nat := checked j.getNat?
def boolean (j : Json) : IO Bool := checked j.getBool?
def require (ok : Bool) (message : String) : IO Unit := unless ok do fail message

def structuredName (j : Json) : IO Name := do
  let parts ← array j
  require (!parts.isEmpty && parts.size ≤ 67) "AUTHOR_NAME_PARTS"
  let mut name := Name.anonymous
  for part in parts do
    let pair ← array part
    require (pair.size == 2) "AUTHOR_NAME_COMPONENT"
    match ← string pair[0]! with
    | "s" =>
      let s ← string pair[1]!
      require (!s.isEmpty && s.utf8ByteSize ≤ 4096 && !s.contains '\x00') "AUTHOR_NAME_STRING"
      name := .str name s
    | "n" =>
      let n ← natural pair[1]!
      require (n < 4294967296) "AUTHOR_NAME_NUMBER"
      name := .num name n
    | _ => fail "AUTHOR_NAME_TAG"
  return name

def structured : Name → Array Json
  | .anonymous => #[]
  | .str p s => (structured p).push (.arr #[toJson "s", toJson s])
  | .num p n => (structured p).push (.arr #[toJson "n", toJson n])

def absoluteName (owner : Option String) (j : Json) : IO Name := do
  let n ← structuredName j
  return match owner with
    | none => n
    | some id => (Name.str `DMKN.Mod id).append n

def parameters (n : Nat) : IO (List Name) := do
  require (n ≤ 64) "AUTHOR_UNIVERSE_LIMIT"
  return (List.range n).map (Name.num `DMKNAuthorUniverse)

partial def decodeLevel (ps : List Name) (j : Json) : IO Level := do
  let a ← array j
  require (!a.isEmpty) "AUTHOR_LEVEL_SHAPE"
  match ← string a[0]! with
  | "zero" => require (a.size == 1) "AUTHOR_LEVEL_ARITY"; return .zero
  | "param" =>
    require (a.size == 2) "AUTHOR_LEVEL_ARITY"
    let i ← natural a[1]!
    let some name := ps[i]? | fail "AUTHOR_UNIVERSE_SCOPE"
    return .param name
  | "succ" =>
    require (a.size == 2) "AUTHOR_LEVEL_ARITY"
    return .succ (← decodeLevel ps a[1]!)
  | "max" =>
    require (a.size == 3) "AUTHOR_LEVEL_ARITY"
    return .max (← decodeLevel ps a[1]!) (← decodeLevel ps a[2]!)
  | "imax" =>
    require (a.size == 3) "AUTHOR_LEVEL_ARITY"
    return .imax (← decodeLevel ps a[1]!) (← decodeLevel ps a[2]!)
  | _ => fail "AUTHOR_LEVEL_TAG"

def reference (owner : Option String) (allowed : NameHashSet) (j : Json) : IO Name := do
  let a ← array j
  require (!a.isEmpty) "AUTHOR_REFERENCE_SHAPE"
  let name ← match ← string a[0]! with
    | "local" => require (a.size == 2) "AUTHOR_REFERENCE_ARITY"; absoluteName owner a[1]!
    | "foundation" => require (a.size == 2) "AUTHOR_REFERENCE_ARITY"; structuredName a[1]!
    | "external" =>
      require (a.size == 3) "AUTHOR_REFERENCE_ARITY"
      absoluteName (some (← string a[1]!)) a[2]!
    | _ => fail "AUTHOR_REFERENCE_TAG"
  require (allowed.contains name) s!"AUTHOR_UNDECLARED_REFERENCE {name}"
  return name

def binder (j : Json) : IO BinderInfo := do
  match ← string j with
  | "default" => return .default
  | "implicit" => return .implicit
  | "strictImplicit" => return .strictImplicit
  | "instImplicit" => return .instImplicit
  | _ => fail "AUTHOR_BINDER_INFO"

partial def decodeExpr (owner : Option String) (allowed : NameHashSet)
    (ps : List Name) (j : Json) (depth : Nat := 0) : IO Expr := do
  let a ← array j
  require (!a.isEmpty) "AUTHOR_EXPRESSION_SHAPE"
  match ← string a[0]! with
  | "bvar" =>
    require (a.size == 2) "AUTHOR_EXPRESSION_ARITY"
    let i ← natural a[1]!
    require (i < depth) "AUTHOR_BOUND_VARIABLE_SCOPE"
    return .bvar i
  | "sort" =>
    require (a.size == 2) "AUTHOR_EXPRESSION_ARITY"
    return .sort (← decodeLevel ps a[1]!)
  | "const" =>
    require (a.size == 3) "AUTHOR_EXPRESSION_ARITY"
    let levels ← array a[2]!
    require (levels.size ≤ 64) "AUTHOR_CONSTANT_LEVELS"
    return .const (← reference owner allowed a[1]!) (← levels.toList.mapM (decodeLevel ps))
  | "app" =>
    require (a.size == 3) "AUTHOR_EXPRESSION_ARITY"
    return .app (← decodeExpr owner allowed ps a[1]! depth) (← decodeExpr owner allowed ps a[2]! depth)
  | "lam" =>
    require (a.size == 4) "AUTHOR_EXPRESSION_ARITY"
    return .lam .anonymous (← decodeExpr owner allowed ps a[2]! depth)
      (← decodeExpr owner allowed ps a[3]! (depth+1)) (← binder a[1]!)
  | "forall" =>
    require (a.size == 4) "AUTHOR_EXPRESSION_ARITY"
    return .forallE .anonymous (← decodeExpr owner allowed ps a[2]! depth)
      (← decodeExpr owner allowed ps a[3]! (depth+1)) (← binder a[1]!)
  | "let" =>
    require (a.size == 4) "AUTHOR_EXPRESSION_ARITY"
    return .letE .anonymous (← decodeExpr owner allowed ps a[1]! depth)
      (← decodeExpr owner allowed ps a[2]! depth) (← decodeExpr owner allowed ps a[3]! (depth+1)) false
  | "proj" =>
    require (a.size == 4) "AUTHOR_EXPRESSION_ARITY"
    let i ← natural a[2]!
    require (i < 4294967296) "AUTHOR_PROJECTION_RANGE"
    return .proj (← reference owner allowed a[1]!) i (← decodeExpr owner allowed ps a[3]! depth)
  | _ => fail "AUTHOR_EXPRESSION_TAG"

partial def normalLevel (ps : List Name) : Level → IO Level
  | .zero => pure .zero
  | .succ l => do return .succ (← normalLevel ps l)
  | .max l r => do return .max (← normalLevel ps l) (← normalLevel ps r)
  | .imax l r => do return .imax (← normalLevel ps l) (← normalLevel ps r)
  | .param n => do
    let some i := ps.idxOf? n | fail "AUTHOR_ACTUAL_UNBOUND_UNIVERSE"
    return .param (.num `DMKNAuthorUniverse i)
  | .mvar _ => fail "AUTHOR_ACTUAL_LEVEL_METAVARIABLE"

partial def normalExpr (ps : List Name) : Expr → IO Expr
  | .mdata _ e => normalExpr ps e
  | .bvar n => pure (.bvar n)
  | .sort l => do return .sort (← normalLevel ps l)
  | .const n ls => do return .const n (← ls.mapM (normalLevel ps))
  | .app f x => do return .app (← normalExpr ps f) (← normalExpr ps x)
  | .lam _ t b bi => do return .lam .anonymous (← normalExpr ps t) (← normalExpr ps b) bi
  | .forallE _ t b bi => do return .forallE .anonymous (← normalExpr ps t) (← normalExpr ps b) bi
  | .letE _ t v b _ => do return .letE .anonymous (← normalExpr ps t) (← normalExpr ps v) (← normalExpr ps b) false
  | .proj n i e => do return .proj n i (← normalExpr ps e)
  | _ => fail "AUTHOR_UNSUPPORTED_ACTUAL_EXPRESSION"

def sameExpression (actual : Expr) (ps : List Name) (expected : Expr) : IO Bool := do
  -- Expr's ordinary BEq deliberately ignores binderInfo. Structural equality
  -- after this narrow normalization is essential for exact interface matching.
  return Expr.equal (← normalExpr ps actual) expected

def names (owner : Option String) (j : Json) : IO (List Name) := do
  (← array j).toList.mapM (absoluteName owner)

def hint (j : Json) : IO ReducibilityHints := do
  match j.getStr? with
  | .ok "abbrev" => return .abbrev
  | .ok "opaque" => return .opaque
  | _ =>
    let n ← natural (← field j "regular")
    require (n < 65536) "AUTHOR_HINT_RANGE"
    return .regular n.toUInt32

def body (owner : Option String) (allowed : NameHashSet) (ps : List Name)
    (bodies : Array Json) (digest : Json) : IO Expr := do
  let wanted ← string digest
  let mut found : Option Json := none
  for item in bodies do
    if (← string (← field item "digest")) == wanted &&
        (← natural (← field item "universes")) == ps.length then
      require found.isNone "AUTHOR_DUPLICATE_BODY"
      found := some (← field item "expression")
  let some value := found | fail "AUTHOR_MISSING_BODY"
  decodeExpr owner allowed ps value

def foundationValue (allowed : NameHashSet) (ps : List Name) (values : Array Json)
    (name : Name) : IO Expr := do
  let mut found : Option Json := none
  for item in values do
    if (← structuredName (← field item "name")) == name then
      require found.isNone "AUTHOR_DUPLICATE_FOUNDATION_VALUE"
      found := some (← field item "expression")
  let some value := found | fail "AUTHOR_MISSING_FOUNDATION_VALUE"
  decodeExpr none allowed ps value

def sameRules : List RecursorRule → List RecursorRule → Bool
  | [], [] => true
  | a::as, b::bs => a.ctor == b.ctor && a.nfields == b.nfields &&
      Expr.equal a.rhs b.rhs && sameRules as bs
  | _, _ => false

def sameConstant (a b : ConstantInfo) : Bool :=
  a.name == b.name && a.levelParams == b.levelParams && Expr.equal a.type b.type &&
  match a, b with
  | .axiomInfo a, .axiomInfo b => a.isUnsafe == b.isUnsafe
  | .defnInfo a, .defnInfo b => Expr.equal a.value b.value && a.safety == b.safety &&
      a.all == b.all && a.hints.toJson == b.hints.toJson
  | .thmInfo a, .thmInfo b => Expr.equal a.value b.value && a.all == b.all
  | .opaqueInfo a, .opaqueInfo b => Expr.equal a.value b.value && a.isUnsafe == b.isUnsafe && a.all == b.all
  | .ctorInfo a, .ctorInfo b => a.induct == b.induct && a.cidx == b.cidx &&
      a.numParams == b.numParams && a.numFields == b.numFields && a.isUnsafe == b.isUnsafe
  | .recInfo a, .recInfo b => a.all == b.all && a.numParams == b.numParams &&
      a.numIndices == b.numIndices && a.numMotives == b.numMotives &&
      a.numMinors == b.numMinors && sameRules a.rules b.rules && a.k == b.k && a.isUnsafe == b.isUnsafe
  | .inductInfo a, .inductInfo b => a.numParams == b.numParams && a.numIndices == b.numIndices &&
      a.all == b.all && a.ctors == b.ctors && a.numNested == b.numNested && a.isRec == b.isRec &&
      a.isUnsafe == b.isUnsafe && a.isReflexive == b.isReflexive
  | .quotInfo a, .quotInfo b => a.kind.toJson == b.kind.toJson
  | _, _ => false

/-- Exact semantic descriptor comparison, including complete generated recursor rules.
    `assumptions` applies only to authenticated theorem/opaque authoring interfaces. -/
def checkInfo (owner : Option String) (allowed : NameHashSet) (bodies values : Array Json)
    (assumptions : Bool) (d : Json) (actual : ConstantInfo) : IO Unit := do
  let name ← absoluteName owner (← field d "name")
  let ps ← parameters (← natural (← field d "universes"))
  require (actual.name == name && actual.levelParams.length == ps.length &&
    !actual.isUnsafe && !actual.isPartial) s!"AUTHOR_DECLARATION_HEADER {name}"
  let expectedType ← decodeExpr owner allowed ps (← field d "type")
  require (← sameExpression actual.type actual.levelParams expectedType) s!"AUTHOR_DECLARATION_TYPE {name}"
  let meta ← field d "meta"
  match (← string (← field d "kind")), actual with
  | "theorem", .axiomInfo _ | "opaque", .axiomInfo _ =>
    require assumptions "AUTHOR_FOUNDATION_ASSUMPTION_REFUSED"
  | "theorem", .thmInfo a =>
    require (!assumptions) "AUTHOR_IMPORTED_PROOF_NOT_REQUIRED"
    require (← sameExpression a.value a.levelParams (← foundationValue allowed ps values name)) "AUTHOR_FOUNDATION_THEOREM_VALUE"
  | "opaque", .opaqueInfo a =>
    require (!assumptions) "AUTHOR_IMPORTED_OPAQUE_BODY_NOT_REQUIRED"
    require (← sameExpression a.value a.levelParams (← foundationValue allowed ps values name)) "AUTHOR_FOUNDATION_OPAQUE_VALUE"
  | "definition", .defnInfo a =>
    require (a.hints.toJson == (← hint (← field meta "hint")).toJson) "AUTHOR_DEFINITION_HINT"
    require ((← string (← field meta "safety")) == "safe") "AUTHOR_DEFINITION_SAFETY"
    let value ← body owner allowed ps bodies (← field d "value_hash")
    require (← sameExpression a.value a.levelParams value) "AUTHOR_DEFINITION_VALUE"
  | "inductive", .inductInfo a =>
    require (a.all == (← names owner (← field meta "all")) &&
      a.ctors == (← names owner (← field meta "constructors")) &&
      a.numParams == (← natural (← field meta "num_params")) &&
      a.numIndices == (← natural (← field meta "num_indices")) &&
      a.numNested == (← natural (← field meta "num_nested")) &&
      a.isRec == (← boolean (← field meta "is_recursive")) &&
      a.isReflexive == (← boolean (← field meta "is_reflexive"))) "AUTHOR_INDUCTIVE_METADATA"
  | "constructor", .ctorInfo a =>
    require (a.induct == (← absoluteName owner (← field meta "inductive")) &&
      a.cidx == (← natural (← field meta "constructor_index")) &&
      a.numParams == (← natural (← field meta "num_params")) &&
      a.numFields == (← natural (← field meta "num_fields"))) "AUTHOR_CONSTRUCTOR_METADATA"
  | "recursor", .recInfo a =>
    require (a.all == (← names owner (← field meta "all")) &&
      a.numParams == (← natural (← field meta "num_params")) &&
      a.numIndices == (← natural (← field meta "num_indices")) &&
      a.numMotives == (← natural (← field meta "num_motives")) &&
      a.numMinors == (← natural (← field meta "num_minors")) &&
      a.k == (← boolean (← field meta "is_k"))) "AUTHOR_RECURSOR_METADATA"
    let rules ← array (← field meta "rules")
    require (a.rules.length == rules.size) "AUTHOR_RECURSOR_RULE_CENSUS"
    for (rule, wanted) in a.rules.zip rules.toList do
      require (rule.ctor == (← absoluteName owner (← field wanted "constructor")) &&
        rule.nfields == (← natural (← field wanted "num_fields"))) "AUTHOR_RECURSOR_RULE_HEADER"
      let rhs ← body owner allowed ps bodies (← field wanted "value_hash")
      require (← sameExpression rule.rhs a.levelParams rhs) "AUTHOR_RECURSOR_RULE_RHS"
  | _, _ => fail s!"AUTHOR_DECLARATION_KIND {name}"

def addChecked (env : Environment) (decl : Declaration) : IO Environment := do
  match env.addDeclCore 20000000 2048 decl none (doCheck := true) with
  | .ok next => return next
  | .error error => fail s!"AUTHOR_CHECKED_RECONSTRUCTION {← (error.toMessageData {}).toString}"

def installGroup (env : Environment) (allowed : NameHashSet) (item : Json) :
    IO (Environment × NameHashSet) := do
  let owner := some (← string (← field item "owner"))
  let group ← field item "group"
  let ds ← array (← field group "declarations")
  let bodies ← array (← field item "bodies")
  require (!ds.isEmpty && ds.size ≤ 4096) "AUTHOR_GROUP_SIZE"
  let before := env.toKernelEnv
  let mut wanted : NameHashSet := {}
  let mut scoped := allowed
  for d in ds do
    let n ← absoluteName owner (← field d "name")
    require (!(before.find? n).isSome && !wanted.contains n) "AUTHOR_GROUP_OVERWRITE_OR_DUPLICATE"
    wanted := wanted.insert n
    scoped := scoped.insert n
  let groupKind ← string (← field group "kind")
  let first := ds[0]!
  let next ← if groupKind == "ordinary" then do
      require (ds.size == 1) "AUTHOR_ORDINARY_GROUP_SIZE"
      let name ← absoluteName owner (← field first "name")
      let ps ← parameters (← natural (← field first "universes"))
      let type ← decodeExpr owner allowed ps (← field first "type")
      match ← string (← field first "kind") with
      | "theorem" | "opaque" =>
        addChecked env (.axiomDecl { name, levelParams := ps, type, isUnsafe := false })
      | "definition" =>
        let value ← body owner allowed ps bodies (← field first "value_hash")
        let hints ← hint (← field (← field first "meta") "hint")
        addChecked env (.defnDecl { name, levelParams := ps, type, value, hints, safety := .safe })
      | _ => fail "AUTHOR_ORDINARY_KIND"
    else do
      require (groupKind == "inductive") "AUTHOR_GROUP_KIND"
      let mut head : Option Json := none
      for d in ds do
        if (← string (← field d "kind")) == "inductive" && head.isNone then head := some d
      let some firstInd := head | fail "AUTHOR_NO_INDUCTIVE"
      let meta ← field firstInd "meta"
      let ordered ← names owner (← field meta "all")
      let arity ← natural (← field firstInd "universes")
      let ps ← parameters arity
      let nparams ← natural (← field meta "num_params")
      let mut types : List InductiveType := []
      for tn in ordered do
        let mut selected : Option Json := none
        for d in ds do
          if (← absoluteName owner (← field d "name")) == tn then selected := some d
        let some d := selected | fail "AUTHOR_MISSING_INDUCTIVE"
        let dm ← field d "meta"
        require ((← string (← field d "kind")) == "inductive" &&
          (← natural (← field d "universes")) == arity &&
          (← names owner (← field dm "all")) == ordered &&
          (← natural (← field dm "num_params")) == nparams) "AUTHOR_INDUCTIVE_GROUP_PARAMETERS"
        let mut ctors : List Constructor := []
        for cn in (← names owner (← field dm "constructors")) do
          let mut selectedCtor : Option Json := none
          for c in ds do
            if (← absoluteName owner (← field c "name")) == cn then selectedCtor := some c
          let some c := selectedCtor | fail "AUTHOR_MISSING_CONSTRUCTOR"
          require ((← string (← field c "kind")) == "constructor" &&
            (← natural (← field c "universes")) == arity) "AUTHOR_CONSTRUCTOR_PARAMETERS"
          ctors := ctors ++ [{ name := cn, type := ← decodeExpr owner scoped ps (← field c "type") }]
        types := types ++ [{ name := tn, type := ← decodeExpr owner scoped ps (← field d "type"), ctors }]
      addChecked env (.inductDecl ps nparams types false)
  let added := next.toKernelEnv.constants.toList.filter (fun (n, _) => (before.find? n).isNone)
  require (added.length == wanted.size) "AUTHOR_GENERATED_CENSUS_SIZE"
  for (n, _) in added do require (wanted.contains n) s!"AUTHOR_EXTRA_GENERATED_CONSTANT {n}"
  for d in ds do
    let n ← absoluteName owner (← field d "name")
    let some actual := next.toKernelEnv.find? n | fail s!"AUTHOR_MISSING_GENERATED_CONSTANT {n}"
    checkInfo owner scoped bodies #[] true d actual
    -- addDeclCore's getNames can omit nested auxiliary recursors. Require actual
    -- frontend visibility too; never repair it with caller-supplied ConstantInfo.
    let some visible := next.find? n | fail s!"AUTHOR_FRONTEND_CONSTANT_NOT_VISIBLE {n}"
    require (sameConstant actual visible) s!"AUTHOR_FRONTEND_CONSTANT_MISMATCH {n}"
  return (next, scoped)

def readBounded (path : System.FilePath) (limit : Nat) : IO String := do
  let metadata ← path.metadata
  require (metadata.byteSize ≤ limit.toUInt64) "AUTHOR_INPUT_BYTE_LIMIT"
  let text ← IO.FS.readFile path
  require (text.utf8ByteSize ≤ limit) "AUTHOR_INPUT_BYTE_LIMIT"
  return text

def run (requestPath outputPath : String) : IO Unit := do
  let out : System.FilePath := outputPath
  require (!(← out.pathExists)) "AUTHOR_FRESH_OUTPUT_REQUIRED"
  let request ← checked <| Json.parse (← readBounded requestPath (16 * 1024 * 1024))
  require ((← string (← field request "schema")) == "DMKN_OWNER_LEAN_AUTHORING_REQUEST_V1" &&
    !(← boolean (← field request "mathematical_acceptance"))) "AUTHOR_REQUEST_SCHEMA"
  let context ← field request "context"
  require ((← string (← field context "schema")) == "DMKN_UNTRUSTED_AUTHORING_CONTEXT_V1" &&
    !(← boolean (← field context "mathematical_acceptance"))) "AUTHOR_CONTEXT_SCHEMA"
  let source ← string (← field request "source")
  require (0 < source.utf8ByteSize && source.utf8ByteSize ≤ 65536) "AUTHOR_SOURCE_BYTE_LIMIT"
  let rootsJson ← array (← field request "roots")
  require (!rootsJson.isEmpty && rootsJson.size ≤ 64) "AUTHOR_ROOT_COUNT"
  let roots ← rootsJson.mapM structuredName
  let options := ({} : Options) |>.set `maxRecDepth (2048 : Nat) |>.set `maxHeartbeats (1000000 : Nat)
  Lean.initSearchPath (← Lean.findSysroot)
  -- Only the owner's explicitly selected source may execute in this supervised
  -- process. This is NOT a sandbox for peer-submitted source or metaprograms.
  unsafe Lean.enableInitializersExecution
  let mut frontend ← Lean.importModules #[{ module := `Init }] options 0 (loadExts := true)
  let foundation ← field context "foundation_view"
  let foundationNames ← array (← field foundation "names")
  let foundationBodies ← array (← field foundation "bodies")
  let foundationValues ← array (← field foundation "values")
  let mut boundaries : NameHashSet := {}
  for name in foundationNames do
    let n ← structuredName name
    require (!boundaries.contains n) "AUTHOR_DUPLICATE_FOUNDATION_NAME"
    boundaries := boundaries.insert n
  let mut foundationCensus : NameHashSet := {}
  for group in (← array (← field foundation "groups")) do
    for d in (← array (← field group "declarations")) do
      let n ← structuredName (← field d "name")
      require (boundaries.contains n && !foundationCensus.contains n) "AUTHOR_FOUNDATION_CENSUS"
      foundationCensus := foundationCensus.insert n
      let some actual := frontend.find? n | fail s!"AUTHOR_FOUNDATION_NOT_IN_RUNTIME {n}"
      checkInfo none boundaries foundationBodies foundationValues false d actual
  require (foundationCensus.size == boundaries.size) "AUTHOR_FOUNDATION_CENSUS_SIZE"
  let imports ← array (← field context "imports")
  require (imports.size ≤ 256) "AUTHOR_IMPORT_GROUP_LIMIT"
  for item in imports do
    let (next, scoped) ← installGroup frontend boundaries item
    frontend := next
    boundaries := scoped
    require (boundaries.size ≤ 8192) "AUTHOR_CONTEXT_DECLARATION_LIMIT"
  let before := frontend.toKernelEnv
  for root in roots do require (!(before.find? root).isSome) "AUTHOR_ROOT_ALREADY_EXISTS"
  let (env, messages) ← Lean.Elab.process source frontend options (some requestPath)
  if messages.hasErrors then
    let mut count := 0
    for msg in messages.reportedPlusUnreported do
      if count < 16 then IO.println (← msg.toJson).compress
      count := count + 1
    fail "AUTHOR_OWNER_SOURCE_REJECTED"
  let actual := env.toKernelEnv
  require (actual.quotInit == before.quotInit) "AUTHOR_QUOTIENT_STATE_CHANGED"
  for (n, old) in before.constants.toList do
    let some current := actual.find? n | fail "AUTHOR_OLD_CONSTANT_REMOVED"
    require (sameConstant old current) s!"AUTHOR_OLD_CONSTANT_CHANGED {n}"
    -- Pinned Init can already contain kernel-only nested auxiliaries. Preserve
    -- every old visible binding, without requiring originally hidden names to
    -- become visible. Any newly exposed old kernel name must still agree.
    match frontend.find? n, env.find? n with
    | some previous, some visible =>
      require (sameConstant previous visible) s!"AUTHOR_OLD_FRONTEND_CONSTANT_CHANGED {n}"
    | none, some visible =>
      require (sameConstant old visible) s!"AUTHOR_OLD_FRONTEND_CONSTANT_CHANGED {n}"
    | none, none => pure ()
    | some _, none => fail s!"AUTHOR_OLD_FRONTEND_CONSTANT_REMOVED {n}"
  let added := actual.constants.toList.filter (fun (n, _) => (before.find? n).isNone)
  require (added.length ≤ 4096) "AUTHOR_NEW_DECLARATION_LIMIT"
  for root in roots do
    let some info := env.find? root | fail "AUTHOR_ROOT_ABSENT"
    require (!info.isUnsafe && !info.isPartial) "AUTHOR_ROOT_UNSAFE"
    match info with
    | .thmInfo _ | .defnInfo _ | .opaqueInfo _ | .inductInfo _ => pure ()
    | _ => fail "AUTHOR_ROOT_KIND"
  IO.FS.createDirAll out
  let (_, st) ← IO.FS.withFile (out / "module.ndjson") .writeNew fun handle => do
    let result ← M.run env handle boundaries do
      initState env
      dumpMetadata
      for root in roots do dumpConstant root
    handle.flush
    return result
  let localNames := st.visitedConstants.toList.filter (fun n => !boundaries.contains n)
  let record := Json.mkObj [
    ("schema", toJson "DMKN_OWNER_LEAN_AUTHORING_EXPORT_V1"),
    ("source_sha256", ← field request "source_sha256"),
    ("selection_binding", ← field context "selection_binding"),
    ("roots", .arr rootsJson), ("rows", .arr st.allRows),
    ("local_names", toJson (localNames.map (fun n => Json.arr (structured n)))),
    ("mathematical_acceptance", Json.bool false),
    ("status", toJson "OWNER_FRONTEND_EXPORT_REQUIRES_INDEPENDENT_RELATION")]
  let text := record.compress
  require (text.utf8ByteSize + 1 ≤ 16 * 1024 * 1024) "AUTHOR_RETURN_BYTE_LIMIT"
  IO.FS.withFile (out / "EXPORT.json") .writeNew fun handle => do
    handle.putStrLn text
    handle.flush

end SourceFrontend

def main (args : List String) : IO UInt32 := do
  try
    let [requestPath, outputPath] := args
      | throw <| IO.userError "EXPECTED_REQUEST_AND_FRESH_OUTPUT_DIRECTORY"
    SourceFrontend.run requestPath outputPath
    return 0
  catch error =>
    IO.eprintln s!"OWNER_AUTHORING_FAILED {error}"
    return 1

