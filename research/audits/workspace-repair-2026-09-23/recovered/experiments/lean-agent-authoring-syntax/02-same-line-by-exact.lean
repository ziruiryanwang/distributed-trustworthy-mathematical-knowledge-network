theorem SameLineByExact (A : Type) (a : A) :
          Eq a a := by exact Eq.refl a
