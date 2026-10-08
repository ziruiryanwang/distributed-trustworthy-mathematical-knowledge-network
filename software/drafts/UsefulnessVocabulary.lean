universe u
noncomputable def Reduction (A : Type u) (op : A -> A -> A)
    (e : A) (xs : List A) : A :=
  List.rec (motive := fun (_ : List A) => A) e
    (fun (a : A) (_ : List A) (acc : A) => op a acc) xs
