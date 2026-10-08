/- Adapted from leanprover/lean4export, commit
ddeb0869b0b5679b0104e16291ffd929fbaa6a48, Export.lean (Apache-2.0).
See LEAN4EXPORT-LICENSE for the unchanged upstream license.
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

structure State where
  visitedNames : HashMap Name Nat := HashMap.emptyWithCapacity 1024 |>.insert .anonymous 0
  visitedLevels : HashMap Level Nat := HashMap.emptyWithCapacity 256 |>.insert .zero 0
  visitedExprs : HashMap Expr Nat := HashMap.emptyWithCapacity 16384
  visitedConstants : NameHashSet := {}
  bytesWritten : Nat := 0
  declarationRows : Array Json := #[]
  noMDataExprs : HashMap Expr Expr := HashMap.emptyWithCapacity 16384
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
  modify fun st => { st with bytesWritten := st.bytesWritten + count }

def wire16 (n : Nat) : M Unit := do
  if n >= 65536 then throw <| IO.userError "WIRE_U16_RANGE"

def M.run (env : Environment) (output : IO.FS.Handle) (act : M α) : IO (α × State) :=
  StateT.run (s := {}) <| ReaderT.run (r := { env, output }) act

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
  if let some x := (← get).noMDataExprs[e]? then
    return x
  let e' ← match e with
  | .mdata _ e' => removeMData e'
  | .fvar .. | .mvar .. => throw <| IO.userError "FREE_OR_META_EXPRESSION"
  | .bvar .. | .sort .. | .const .. | .lit _ => pure e
  | .app f a =>
    pure <| e.updateApp! (← removeMData f) (← removeMData a)
  | .lam _ d b _ =>
    pure <| e.updateLambdaE! (← removeMData d) (← removeMData b)
  | .letE _ d v b _ =>
    -- Normalize `nonDep` to `false` to avoid duplicate expression indices.
    -- Lean's `BEq` for `Expr` considers the `nonDep` flag, but external type checkers
    -- (e.g., nanoda_lib) treat expressions as identical regardless of this optimization hint.
    -- Without normalization, the same expression can get different indices, causing parse errors.
    -- See: https://github.com/ammkrn/lean4export/commit/eb023e5
    pure <| e.updateLet! (← removeMData d) (← removeMData v) (← removeMData b) false
  | .forallE _ d b _ =>
    pure <| e.updateForallE! (← removeMData d) (← removeMData b)
  | .proj _ _ e2 =>
    pure <| e.updateProj! (← removeMData e2)
  modify (fun st => { st with noMDataExprs := st.noMDataExprs.insert e e' })
  pure e'

mutual

partial def dumpExprAux (e : Expr) : M Nat := do
  getIdx e "ie" (·.visitedExprs) ({ · with visitedExprs := · }) do
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
  match declar with
  | .axiomInfo val => do
    dumpDeps val.type
    dumpObj [
      ("axiom", Json.mkObj [
        ("name", ← dumpName val.name),
        ("levelParams", ← dumpUparams val.levelParams),
        ("type", ← dumpExpr val.type),
        ("isUnsafe", val.isUnsafe)
      ])
    ]
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
  | .quotInfo val =>
    dumpDeps val.type
    dumpObj [
      ("quot", .mkObj [
        ("name", ← dumpName val.name),
        ("levelParams", ← dumpUparams val.levelParams),
        ("type", ← dumpExpr val.type),
        ("kind", val.kind.toJson)
      ])
    ]
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
      dumpDeps val.type
      if let .some names := (← get).recursorMap.get? indName
      then recursorNames := recursorNames.union names
      else assert! ctorVals.size == 0

    /- We dump the constructor dependencies (which will not include the inductives in this block since we've
    added the names to `visitedConstants`) before actually outputting anything in this inductive block to
    ensure e.g. the `LT` in `Fin.mk` is dumped before this inductive block appears in the export file. -/
    for ctorVal in ctorVals do
      modify fun st => { st with visitedConstants:= st.visitedConstants.insert ctorVal.name }
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
    ("name", "v5/selected-owner-module-export"),
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
def main (args : List String) : IO UInt32 := do
  let [sourcePath, outputPath] := args
    | throw <| IO.userError "EXPECTED_SOURCE_AND_FRESH_OUTPUT"
  let out : System.FilePath := outputPath
  if (← out.pathExists) then throw <| IO.userError "FRESH_OUTPUT_REQUIRED"
  let source ← IO.FS.readFile sourcePath
  if source.utf8ByteSize > 65536 then throw <| IO.userError "SOURCE_BYTE_LIMIT"
  IO.FS.createDirAll out
  Lean.initSearchPath (← Lean.findSysroot)
  let options := ({} : Options) |>.set `maxRecDepth (1024 : Nat) |>.set `maxHeartbeats (1000000 : Nat)
  -- This process runs only pinned owner-selected source, never peer input.
  unsafe Lean.enableInitializersExecution
  let frontend ← Lean.importModules #[{ module := `Init }] options 0 (loadExts := true)
  let (env, messages) ← Lean.Elab.process source frontend options (some sourcePath)
  if messages.hasErrors then
    let mut count := 0
    for msg in messages.reportedPlusUnreported do
      if count < 16 then IO.println (← msg.toJson).compress
      count := count + 1
    throw <| IO.userError "OWNER_SOURCE_REJECTED"
  let roots := [`CommonsV5.fusion_map, `CommonsV5.project_summary]
  for root in roots do
    let some (.thmInfo _) := env.find? root
      | throw <| IO.userError "EXACT_THEOREM_ROOT_REQUIRED"
  let (_, st) ← IO.FS.withFile (out / "module.ndjson") .writeNew fun handle => do
    let result ← M.run env handle do
      initState env
      dumpMetadata
      for root in roots do dumpConstant root
    handle.flush
    return result
  let names := st.visitedNames.toList.map fun (n, i) =>
    Json.arr #[toJson i, Json.str n.toString]
  let axioms := st.visitedConstants.toList.filter fun n =>
    match env.find? n with
    | some (.axiomInfo _) => true
    | _ => false
  let record := Json.mkObj [
    ("schema", Json.str "DMKN_V5_OWNER_SOURCE_EXPORT_V1"),
    ("source_bytes", toJson source.utf8ByteSize),
    ("roots", toJson (roots.map Name.toString)),
    ("names", toJson names),
    ("declaration_rows", toJson st.declarationRows),
    ("axioms", toJson (axioms.map Name.toString)),
    ("bytes_written", toJson st.bytesWritten),
    ("mathematical_admission", Json.bool false),
    ("status", Json.str "OWNER_FRONTEND_EXPORT_REQUIRES_INDEPENDENT_RELATION")]
  IO.FS.withFile (out / "EXPORT.json") .writeNew fun handle => do
    handle.putStrLn record.compress
    handle.flush
  return 0

