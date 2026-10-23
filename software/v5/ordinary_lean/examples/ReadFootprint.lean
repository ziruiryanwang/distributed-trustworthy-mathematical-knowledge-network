import Std.Data.ExtHashMap.Lemmas

/-!
Owner-authored ordinary Lean input for the selected library-reuse workflow.

This file is not peer code for automatic execution by a receiver. The intended
exchange is its elaborated inert declarations, independently checked against
exact warranted dependencies. Successful source compilation alone would not
establish network admission. No claim of mathematical novelty is made.

The standard library already supplies `insertMany` and its single-key no-touch
law. This contribution exposes a general observation-footprint interface above
that existing law; it does not reimplement the standard update operation.
-/

set_option autoImplicit false

namespace DMKN.ReadFootprint

universe u v w

variable {α : Type u} {β : Type v} {γ : Type w}
variable [BEq α] [Hashable α] [EquivBEq α] [LawfulHashable α]

/-- An observation depends only on optional lookups at keys satisfying `R`. -/
def ReadsOnly (R : α → Prop) (F : Std.ExtHashMap α β → γ) : Prop :=
  ∀ m n, (∀ k, R k → m[k]? = n[k]?) → F m = F n

/-- No write compares equal to any key in the selected read footprint. -/
def Avoids (R : α → Prop) (writes : List (α × β)) : Prop :=
  ∀ k, R k → (writes.map Prod.fst).contains k = false

/-- Updating outside an established read footprint preserves the observation. -/
theorem readsOnly_insertMany
    (R : α → Prop) (F : Std.ExtHashMap α β → γ)
    (m : Std.ExtHashMap α β) (writes : List (α × β))
    (reads : ReadsOnly R F) (avoids : Avoids R writes) :
    F (m.insertMany writes) = F m := by
  apply reads (m.insertMany writes) m
  intro k hk
  exact Std.ExtHashMap.getElem?_insertMany_list_of_contains_eq_false
    (m := m) (l := writes) (k := k) (avoids k hk)

end DMKN.ReadFootprint
