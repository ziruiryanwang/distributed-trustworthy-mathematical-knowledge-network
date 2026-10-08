theorem MultilineByLet (A : Type) (a : A) :
          Eq a a := by
  let witness : A := a
  exact Eq.refl witness
