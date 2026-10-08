import AgentReplayCore

open Lean BootstrapProbe SourceComposition

/-!
Finite owner-local client. AgentReplayCore is the byte-exact prefix of held
ReconcileComposition.lean through `end SourceComposition`; only its root main
wrapper is omitted in the staged module. The held source is never modified.

Contribution packages and replay plans are data. The source accepted below is
owner-authorized executable Lean input, NOT peer source and NOT sandboxed.
The caller binds canonical plans, process receipts, budgets and inverse export.
No success from this program alone authenticates a claimed ContentID.
-/

namespace AgentClient

def sourceByteLimit : Nat := 65536
def requestByteLimit : Nat := 1048576
def diagnosticByteLimit : Nat := 1048576
def outputByteLimit : Nat := 67108864

def clientOptions : Options :=
  ({} : Options).set `maxRecDepth (10000 : Nat)
    |>.set `maxHeartbeats (20000000 : Nat)

def presentationOptions : Options :=
  clientOptions.set `pp.all true
    |>.set `pp.explicit true
    |>.set `pp.fullNames true
    |>.set `pp.universes true
    |>.set `pp.notation false
    |>.set `pp.piBinderTypes true
    |>.set `pp.piBinderNames true
    |>.set `pp.maxSteps (2000000 : Nat)

def readBoundedText (path : String) (limit : Nat) : IO String := do
  let file := System.FilePath.mk path
  let fileInfo ← file.metadata
  if fileInfo.byteSize.toNat > limit then fail "AGENT_CLIENT_INPUT_BYTE_LIMIT"
  let text ← IO.FS.readFile file
  if text.utf8ByteSize > limit then fail "AGENT_CLIENT_INPUT_BYTE_LIMIT"
  return text

def emitJson (outputPrefix : String) (value : Json) : IO Unit := do
  let text := value.compress
  if text.utf8ByteSize > outputByteLimit then fail "AGENT_CLIENT_OUTPUT_BYTE_LIMIT"
  emit s!"{outputPrefix} {text}"

def declarationKind (info : ConstantInfo) : String :=
  match info with
  | .axiomInfo _ => "axiom"
  | .defnInfo _ => "definition"
  | .thmInfo _ => "theorem"
  | .opaqueInfo _ => "opaque"
  | .inductInfo _ => "inductive"
  | .ctorInfo _ => "constructor"
  | .recInfo _ => "recursor"
  | .quotInfo _ => "quotient"

def checkedName (state : Receiving) (ref : Json) : IO Name := do
  let name ← referenceName state.seedNames ref
  let some expected := state.bindings[name]?
    | fail "AGENT_CLIENT_UNCHECKED_REFERENCE"
  if expected != ref then fail "AGENT_CLIENT_REFERENCE_BINDING_MISMATCH"
  return name

def describe (plan inventory requests : Json) : IO Unit := do
  let refs ← arrayOf requests
  if refs.isEmpty || refs.size > 256 then fail "AGENT_CLIENT_REQUEST_COUNT_LIMIT"
  let state ← receive plan inventory
  let mut seen : Std.HashSet Name := {}
  let mut rows : Array Json := #[]
  let mut bytes := 0
  for ref in refs do
    -- A proof-root replay need not install a semantic alias. In particular,
    -- [7, PI] is accepted as itself; no nonexistent [2, J] is manufactured.
    let name ← checkedName state ref
    if seen.contains name then fail "AGENT_CLIENT_DUPLICATE_REQUEST"
    seen := seen.insert name
    let info ← lookup state.env.toKernelEnv name
    let formalType ← exportDag state.bindings #[] false info.levelParams info.type
    let mut display := Json.null
    let mut displayError := Json.null
    try
      let fmt ← Lean.PrettyPrinter.ppExprLegacy state.env {} {} presentationOptions info.type
      let text := fmt.pretty
      if text.utf8ByteSize > requestByteLimit then
        displayError := Json.str "PRESENTATION_BYTE_LIMIT"
      else
        display := Json.str text
    catch ex =>
      -- The exact formal DAG remains available if optional delaboration fails.
      displayError := Json.str s!"PRESENTATION_FAILED {ex}"
    let row := Json.mkObj [
      ("reference", ref), ("name", ← nameJson name),
      ("leanName", Json.str name.toString),
      ("kind", Json.str (declarationKind info)),
      ("u", jnat info.levelParams.length),
      ("universeNames", ← namesJson info.levelParams),
      ("type", formalType), ("typeText", display),
      ("typeTextError", displayError),
      ("typeTextAuthority", Json.str "PRESENTATION_ONLY_NOT_ROUNDTRIP_CERTIFIED")]
    bytes := bytes + row.compress.utf8ByteSize
    if bytes > outputByteLimit - requestByteLimit then
      fail "AGENT_CLIENT_DESCRIPTION_BYTE_LIMIT"
    rows := rows.push row
  emitJson "AGENT_CLIENT_DESCRIPTION_JSON" <| Json.mkObj [
    ("schema", jnat 1),
    ("status", Json.str "NATIVE_CHECKED_BINDINGS_REQUIRE_BOUND_CANONICAL_PLAN"),
    ("foundation", ← objectField plan "foundation"),
    ("replays", ← objectField plan "replays"),
    ("rows", jarr rows)]

def emitDiagnostics (messages : MessageLog) : IO Unit := do
  let all := messages.reportedPlusUnreported
  let mut bytes := 0
  let mut count := 0
  let mut total := 0
  let mut truncated := false
  for msg in all do
    total := total + 1
    if truncated then continue
    if count >= 4096 then
      truncated := true
      continue
    let row ← msg.toJson
    let text := row.compress
    if bytes + text.utf8ByteSize > diagnosticByteLimit then
      truncated := true
      continue
    emit s!"AGENT_CLIENT_DIAGNOSTIC_JSON {text}"
    bytes := bytes + text.utf8ByteSize
    count := count + 1
  emitJson "AGENT_CLIENT_DIAGNOSTICS_JSON" <| Json.mkObj [
    ("total", jnat total), ("emitted", jnat count), ("bytes", jnat bytes),
    ("truncated", toJson truncated), ("hasErrors", toJson messages.hasErrors)]

def requestedRoot (text : String) : IO Name := do
  if text.isEmpty || text.utf8ByteSize > 4096 then fail "AGENT_CLIENT_ROOT_NAME_LIMIT"
  let name := text.toName
  -- This initial CLI accepts ordinary canonical dotted source names. Quoted
  -- components are not parsed by String.toName and must not be misinterpreted.
  if name.isAnonymous || name.toString != text then
    fail "AGENT_CLIENT_ROOT_EXPECTED_CANONICAL_DOTTED_NAME"
  return name

/-- Local elaboration needs imported syntax, macros and tactics. Kernel-only
reconstruction deliberately has none of that module extension state. The
imported environment is an authoring tool; only the subsequent canonical
capture and fresh data-only replay can grant mathematical acceptance. -/
def sameSourceBinding (expected actual : ConstantInfo) : IO Bool := do
  screen expected
  screen actual
  -- Reconstruction renames universes and binders and removes expression
  -- metadata. Compare the existing canonical inventory representation, not
  -- source-level spellings. Definition heights are recomputed by the receiver.
  return (← inventoryRow expected (some 0)) == (← inventoryRow actual (some 0))

def sourceEnvironment (checked : Lean.Environment) : IO Lean.Environment := do
  emit "AGENT_CLIENT_FRONTEND_BEGIN module=Init importedAuthority=false"
  Lean.initSearchPath (← Lean.findSysroot)
  -- The pinned runtime and its native code are already loaded in this
  -- single-threaded owner process (-j 1); use Lean's frontend initializer API.
  unsafe Lean.enableInitializersExecution
  -- Ordinary Lean files implicitly import Init. Importing the entire Lean
  -- implementation again duplicates a large metaprogramming environment in
  -- this already-loaded checker process and exceeds the 4 GiB stage profile.
  let mut frontend ← Lean.importModules #[{ module := `Init }] clientOptions 0
    (loadExts := true)
  let kernel := checked.toKernelEnv
  let imported := frontend.toKernelEnv
  if imported.quotInit != kernel.quotInit then fail "AGENT_CLIENT_FRONTEND_FOUNDATION_MISMATCH"
  let mut shared : Std.HashSet Name := {}
  let mut missing : Array Name := #[]
  for (name, expected) in kernel.constants.toList do
    if let some actual := imported.find? name then
      if !(← sameSourceBinding expected actual) then
        fail s!"AGENT_CLIENT_FRONTEND_BINDING_MISMATCH name={name}"
      shared := shared.insert name
    else
      missing := missing.push name
  -- Install complete dependency-ordered groups, including checked peer work.
  -- No imported declaration may stand in for a different checked binding.
  let units ← collectExtension kernel shared missing
  for unit in units do
    frontend ← checkedAdd frontend unit.decl
  let assembled := frontend.toKernelEnv
  for (name, expected) in kernel.constants.toList do
    let some actual := assembled.find? name
      | fail s!"AGENT_CLIENT_FRONTEND_BINDING_ABSENT name={name}"
    if !(← sameSourceBinding expected actual) then
      fail s!"AGENT_CLIENT_FRONTEND_BINDING_MISMATCH name={name}"
  emit s!"AGENT_CLIENT_FRONTEND_READY module=Init checkedBindings={kernel.constants.toList.length} canonicalReplayRequired=true"
  return frontend

def checkSource (plan inventory : Json) (sourcePath rootText : String) : IO Unit := do
  let root ← requestedRoot rootText
  let text ← readBoundedText sourcePath sourceByteLimit
  let state ← receive plan inventory
  let frontend ← sourceEnvironment state.env
  let before := frontend.toKernelEnv
  if (before.find? root).isSome then fail "AGENT_CLIENT_ROOT_ALREADY_EXISTS"
  emit "AGENT_CLIENT_SOURCE_BOUNDARY ownerAuthorizedExecutable=true peerSource=false sandbox=false"
  emitJson "AGENT_CLIENT_SOURCE_JSON" <| Json.mkObj [
    ("path", Json.str sourcePath), ("root", ← nameJson root),
    ("source", Json.str text), ("bytes", jnat text.utf8ByteSize)]
  let (full, messages) ← Lean.Elab.process text frontend clientOptions (some sourcePath)
  emitDiagnostics messages
  if messages.hasErrors then fail "AGENT_CLIENT_SOURCE_ELABORATION_REJECTED"
  let actual := full.toKernelEnv
  if actual.quotInit != before.quotInit then fail "AGENT_CLIENT_FOUNDATION_CHANGED"
  for (name, old) in before.constants.toList do
    let some current := actual.find? name | fail "AGENT_CLIENT_IMPORTED_DECLARATION_REMOVED"
    if !sameConstant old current then fail "AGENT_CLIENT_IMPORTED_DECLARATION_CHANGED"
  let some info := actual.find? root | fail "AGENT_CLIENT_REQUESTED_ROOT_ABSENT"
  screen info
  if info.levelParams.length > 64 then fail "AGENT_CLIENT_ROOT_UNIVERSE_LIMIT"
  match info with
  | .thmInfo _ | .defnInfo _ | .opaqueInfo _ | .inductInfo _ => pure ()
  | _ => fail "AGENT_CLIENT_UNSUPPORTED_ROOT_KIND"
  -- All dependencies outside the checked bindings must be exported as proof
  -- data too, including any used from the local Lean library. collectExtension
  -- rejects new axioms/unsafe declarations; the caller then performs fresh
  -- canonical replay against the selected foundation, without these imports.
  let units ← collectExtension actual (allowedNames state.bindings) #[root]
  let exported := units.foldl (fun total unit => total + unit.emitted.size) 0
  if units.size > 256 || exported > 1024 then fail "AGENT_CLIENT_CAPTURE_COUNT_LIMIT"
  let added := actual.constants.toList.filter (fun (name, _) => (before.find? name).isNone)
  if added.length > 1024 then fail "AGENT_CLIENT_NEW_DECLARATION_COUNT_LIMIT"
  let capturedNames := units.foldl (fun names unit =>
    unit.emitted.foldl (fun names name => names.insert name) names)
    ({} : Std.HashSet Name)
  let omitted := added.filter (fun (name, _) => !capturedNames.contains name)
  emitJson "AGENT_CLIENT_CAPTURE_SUMMARY_JSON" <| Json.mkObj [
    ("status", Json.str "SOURCE_CAPTURED_NOT_CANONICAL_OR_REPLAY_ACCEPTANCE"),
    ("root", ← nameJson root), ("kind", Json.str (declarationKind info)),
    ("u", jnat info.levelParams.length), ("units", jnat units.size),
    ("exports", jnat exported), ("newDeclarations", jnat added.length),
    ("omittedUnreachedDeclarations", jnat omitted.length)]
  emitJson "SOURCE_CAPTURE_JSON" <| Json.mkObj [
    ("schema", jnat 1), ("roots", ← namesJson [root]),
    ("units", ← captureUnitsJson actual units)]

def run (args : List String) : IO UInt32 := do
  match args with
  | ["--describe", planPath, "--inventory", inventoryPath, "--requests", requestsPath] =>
      let requests ← jsonResult <| Json.parse (← readBoundedText requestsPath requestByteLimit)
      describe (← readProjection planPath) (← readProjection inventoryPath) requests
      return 0
  | ["--check-source", planPath, "--inventory", inventoryPath,
      "--source", sourcePath, "--root", rootText] =>
      checkSource (← readProjection planPath) (← readProjection inventoryPath) sourcePath rootText
      return 0
  | _ => fail "USAGE --describe PLAN --inventory INVENTORY --requests JSON_REF_ARRAY | --check-source PLAN --inventory INVENTORY --source SOURCE --root NAME"

end AgentClient

def main (args : List String) : IO UInt32 := do
  try AgentClient.run args
  catch ex =>
    BootstrapProbe.emit s!"AGENT_CLIENT_FAILED detail={ex}"
    return 1
