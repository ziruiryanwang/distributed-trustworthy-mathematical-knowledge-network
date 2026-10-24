module

public meta import OwnerQueryCommand

public meta section
open Lean Lean.Elab Lean.Elab.Command

/- Test instrumentation only. Compare current-file declaration names around the
   actual product command; do not enumerate imported proofs or their ancestry. -/
elab "#assert_type_query " "[" params:ident,* "]" output:str " : " requested:term : command => do
  let names := fun (env : Environment) =>
    env.constants.foldStage2 (fun (xs : Array Name) name _ => xs.push name) #[]
  let before := names (← getEnv)
  elabCommand (← `(#ordinary_type_query [$params:ident,*] $output:str : $requested:term))
  unless names (← getEnv) == before do
    throwError "QUERY_TEST_DECLARATIONS_CHANGED"

set_option autoImplicit false
universe u v
section
variable {A : Type u} (B : A → Type v)
variable (f g : (a : A) → B a) (unused : Nat)

-- An independently chosen formal contract, with no name or proof supplied.
-- It is not asserted true: arbitrary f and g need not be pointwise equal.
#assert_type_query [u, v] "__QUERY_OUTPUT__" : ∀ a, f a = g a
end
