module

public meta import OriginalExpr
public meta import Lean.Elab.Command
public meta import Lean.Elab.Term
public meta import Lean.Meta.Check
public meta import Lean.Util.Sorry

/- Owner-local type query, not a peer source endpoint or theorem producer.
   Uses the existing project elaborator and expression serializer only.
   No source inventory, proof export, dependency walk or environment insertion.
   Owner macros/imports are executable trusted support, not sandboxed input.
   A selected outer runner must bound total elaboration CPU/memory/wall time. -/

public meta section
open Lean Lean.Elab Lean.Elab.Command

namespace OrdinaryLean.OwnerQuery

def fail {α : Type} (message : String) : IO α :=
  throw <| IO.userError s!"ORDINARY_TYPE_QUERY {message}"

def limits : ExprCodec.Limits := {
  maxLevels := 8192
  maxExprs := 65536
  maxDepth := 4096
  maxParams := 256
  maxNameParts := 256
  maxNameBytes := 65536
  maxLiteralBytes := 65536
  maxTotalLiteralBytes := 1048576
}

def writeType (params : List Name) (type : Expr) (outputRaw : String) : IO Unit := do
  let output := System.FilePath.mk outputRaw
  if !output.isAbsolute || output.toString.utf8ByteSize > 32768 ||
      output.components.contains "." || output.components.contains ".." then
    fail "ABSOLUTE_BOUNDED_FRESH_PATH_REQUIRED"
  let present ← try
    discard output.symlinkMetadata
    pure true
  catch error =>
    match error with
    | .noFileOrDirectory .. => pure false
    | _ => throw error
  if present then fail "FRESH_OUTPUT_REQUIRED"
  if type.hasSorry then fail "SORRY_QUERY_REFUSED"
  let packet ← ExprCodec.encode params type limits
  let names ← params.toArray.mapM (fun name => ExprCodec.encodeName name limits)
  -- Arrays plus codec values use the existing canonical inert JSON vocabulary.
  -- There is deliberately no theorem name, unit, proof, status or locator here.
  let raw := (Json.arr #[Json.str "DMKN_ORDINARY_LEAN_QUERY_TYPE_AST_V1",
                         Json.arr names, packet]).compress.toUTF8
  if raw.isEmpty || raw.size > 1048576 then fail "QUERY_BYTE_BOUND"
  let handle ← IO.FS.Handle.mk output .writeNew
  handle.write raw
  handle.flush

end OrdinaryLean.OwnerQuery

/-- Type-only query in a trusted local project. Universe order is explicit;
    section variables are closed only when needed by this formal contract. -/
syntax (name := ordinaryTypeQuery) "#ordinary_type_query "
  "[" ident,* "]" str " : " term : command

elab_rules : command
  | `(#ordinary_type_query [$params:ident,*] $output:str : $requested:term) => do
    withoutModifyingEnv <| runTermElabM fun variables => do
      let type ← Term.elabType requested
      Term.synthesizeSyntheticMVarsNoPostponing
      let type ← instantiateMVars type
      let closed ← Meta.mkForallFVars variables type (usedOnly := true)
      let closed ← instantiateMVars closed
      Meta.check closed
      let names := params.getElems.toList.map (fun name => name.getId)
      liftIO <| OrdinaryLean.OwnerQuery.writeType names closed output.getString
