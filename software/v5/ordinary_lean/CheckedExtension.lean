import OriginalDecl
import Lean.Environment

/- Internal checked-extension plumbing, NOT a public acceptance authority.
   The caller must supply an independently warranted, exact-profile environment.
   A peer cannot establish that precondition by passing an environment or a file.
   No source elaboration, peer binary import, proof production or persistence. -/

open Lean

namespace OrdinaryLean.CheckedExtension

structure Limits where
  codec : DeclCodec.Limits := {}
  maxUnits : Nat := 1024
  maxNewNames : Nat := 65536
  maxStageTwo : Nat := 131072
  maxScanNodes : Nat := 2097152
  maxHeartbeats : USize := 20000000
  maxRecDepth : USize := 4096
  deriving Inhabited

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"ORDINARY_EXTENSION {message}"

def requireName (name : Name) : IO Unit := do
  ExprCodec.requireSemanticName name
  if name == ``sorryAx then fail "SORRY_REFERENCE"

/-- The visited equality may erase binder labels: this traversal only collects
    semantic references. Exact record equality is handled by DeclCodec. -/
def references (expr : Expr) (maximum : Nat) : IO (Std.HashSet Name × Nat) := do
  if expr.hasLooseBVars || expr.hasFVar || expr.hasMVar then fail "OPEN_TERM"
  let mut todo := #[expr]
  let mut seen : Std.HashSet Expr := {}
  let mut refs : Std.HashSet Name := {}
  while !todo.isEmpty do
    let current := todo.back!
    todo := todo.pop
    if seen.contains current then continue
    if seen.size >= maximum then fail "SCAN_BOUND"
    seen := seen.insert current
    match current with
    | .const name _ =>
        requireName name
        refs := refs.insert name
    | .proj name _ value =>
        requireName name
        refs := refs.insert name
        todo := todo.push value
    | .app fn arg => todo := (todo.push fn).push arg
    | .lam _ type body _ | .forallE _ type body _ =>
        todo := (todo.push type).push body
    | .letE _ type value body _ => todo := ((todo.push type).push value).push body
    | .mdata _ body => todo := todo.push body
    | _ => pure ()
  return (refs, seen.size)

def allowedDeclaration (decl : Declaration) : IO (Std.HashSet Name) := do
  let mut selfTypes : Std.HashSet Name := {}
  match decl with
  | .defnDecl d =>
      if d.safety != .safe then fail "UNSAFE_OR_PARTIAL"
  | .thmDecl _ => pure ()
  | .opaqueDecl d => if d.isUnsafe then fail "UNSAFE_OPAQUE"
  | .inductDecl _ _ types unsafeFlag =>
      if unsafeFlag || types.isEmpty then fail "UNSAFE_OR_EMPTY_GROUP"
      for type in types do
        if selfTypes.contains type.name then fail "DUPLICATE_GROUP_TYPE"
        selfTypes := selfTypes.insert type.name
  | _ => fail "AXIOM_QUOT_OR_UNSUPPORTED_DECLARATION"
  let mut names : Std.HashSet Name := {}
  for name in decl.getNames do
    requireName name
    if names.contains name then fail "DUPLICATE_DECLARATION_NAME"
    names := names.insert name
  return selfTypes

/-- Result remains conditional on the caller's parent/profile warrant. Only
    actual kernel output is returned; no caller-supplied ConstantInfo is installed. -/
structure CheckedBatch where
  environment : Environment
  added : Array ConstantInfo
  unitsChecked : Nat
  deriving Nonempty

def stageTwoNames (env : Kernel.Environment) (maximum : Nat) : IO (Std.HashSet Name) := do
  if env.constants.stage₁ then fail "STAGE_TWO_PARENT_REQUIRED"
  let mut names : Std.HashSet Name := {}
  for (name, _) in env.constants.map₂ do
    if names.size >= maximum then fail "STAGE_TWO_BOUND"
    names := names.insert name
  return names

/-- One atomic bounded batch over an already warranted ordinary environment.
    No successful prefix escapes on failure. The immutable parent stays unchanged.
    Native literal semantics and permitted foundation axioms are parent-profile
    obligations; quotInit alone is NOT evidence of that profile. -/
def checkBatch (parent : Environment) (units : Array DeclCodec.DecodedUnit)
    (limits : Limits := {}) : IO CheckedBatch := do
  if units.isEmpty || units.size > limits.maxUnits then fail "UNIT_BOUND"
  if limits.maxHeartbeats == 0 || limits.maxRecDepth == 0 then fail "FINITE_KERNEL_LIMITS"
  if !parent.toKernelEnv.quotInit then fail "INITIALIZED_PROFILE_REQUIRED"
  let before ← stageTwoNames parent.toKernelEnv limits.maxStageTwo
  let mut current := parent
  let mut promised : Std.HashSet Name := {}
  let mut ordered : Array Name := #[]
  let mut scans := 0
  for unit in units do
    let selfTypes ← allowedDeclaration unit.decl
    let names ← DeclCodec.expectedNames unit.expected limits.codec
    if names.isEmpty || promised.size + names.size > limits.maxNewNames then
      fail "NEW_NAME_BOUND"
    let mut thisNames : Std.HashSet Name := {}
    for name in names do
      requireName name
      if (current.toKernelEnv.find? name).isSome || promised.contains name then
        fail "OVERWRITE_OR_DUPLICATE"
      thisNames := thisNames.insert name
    for name in unit.decl.getNames do
      if !thisNames.contains name then fail "INCOMPLETE_DECLARED_INVENTORY"
    let scanResult ← unit.decl.foldExprM (fun count expr => do
      let (refs, visited) ← references expr (limits.maxScanNodes - count)
      for name in refs do
        if !selfTypes.contains name && (current.toKernelEnv.find? name).isNone then
          fail s!"UNGROUNDED_REFERENCE {name}"
      return count + visited) scans
    scans := scanResult
    -- This call deliberately bypasses Lean.addDecl's elaborator options,
    -- asynchronous checking and fallback-axiom recovery. Do not make doCheck configurable.
    let candidate ← match current.addDeclCore limits.maxHeartbeats limits.maxRecDepth
        unit.decl none (doCheck := true) with
      | .ok checked => pure checked
      | .error _ => fail "KERNEL_REJECTED_OR_RESOURCE_LIMIT"
    for i in [:names.size] do
      let name := names[i]!
      let some actual := candidate.toKernelEnv.find? name | fail "MISSING_GENERATED_NAME"
      if actual.isUnsafe || actual.isPartial || actual.isAxiom then fail "UNSAFE_GENERATED_RECORD"
      if (← DeclCodec.inventoryRow actual limits.codec) != unit.expected[i]! then
        fail "GENERATED_RECORD_MISMATCH"
      promised := promised.insert name
      ordered := ordered.push name
    current := candidate
  -- Scan only bounded in-process stage two, once per batch, not imported ancestors
  -- or one whole-environment pass for every declaration. Persistent chunks should
  -- restore accepted ancestors into stage one before another large batch.
  let after ← stageTwoNames current.toKernelEnv limits.maxStageTwo
  if after.size != before.size + promised.size then fail "UNEXPECTED_GENERATED_CENSUS"
  for name in after do
    if !before.contains name && !promised.contains name then fail "UNADVERTISED_GENERATED_NAME"
  let mut added := #[]
  for name in ordered do
    let some actual := current.toKernelEnv.find? name | fail "INTERNAL_ADDED_RECORD"
    added := added.push actual
  return { environment := current, added, unitsChecked := units.size }

end OrdinaryLean.CheckedExtension
