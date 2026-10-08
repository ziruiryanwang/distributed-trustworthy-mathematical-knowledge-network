universe u
theorem Reduction_append (A : Type u) (op : A -> A -> A) (e : A)
    (assoc : (a b c : A) -> Eq (op (op a b) c) (op a (op b c)))
    (left_unit : (a : A) -> Eq (op e a) a)
    (xs ys : List A) :
    Eq
      (DTMKN.d.«84011102582061903d4b0e3bb04e9ac15e179d35e6e4ae0b358285c91d29c5426b6c590f318a»
        A op e (List.append xs ys))
      (op
        (DTMKN.d.«84011102582061903d4b0e3bb04e9ac15e179d35e6e4ae0b358285c91d29c5426b6c590f318a»
          A op e xs)
        (DTMKN.d.«84011102582061903d4b0e3bb04e9ac15e179d35e6e4ae0b358285c91d29c5426b6c590f318a»
          A op e ys)) :=
  let F : List A -> A :=
    DTMKN.d.«84011102582061903d4b0e3bb04e9ac15e179d35e6e4ae0b358285c91d29c5426b6c590f318a»
      A op e
  List.rec
    (motive := fun (zs : List A) =>
      Eq (F (List.append zs ys)) (op (F zs) (F ys)))
    (Eq.symm (left_unit (F ys)))
    (fun (a : A) (zs : List A)
        (ih : Eq (F (List.append zs ys)) (op (F zs) (F ys))) =>
      Eq.trans
        (congrArg (fun (t : A) => op a t) ih)
        (Eq.symm (assoc a (F zs) (F ys))))
    xs
