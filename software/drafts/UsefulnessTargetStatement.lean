universe u
noncomputable def ChunkedReductionStatement (A : Type u) (op : A -> A -> A)
    (e : A) : Prop :=
  ((a b c : A) -> Eq (op (op a b) c) (op a (op b c))) ->
  ((a : A) -> Eq (op e a) a) ->
  ((a : A) -> Eq (op a e) a) ->
  (chunks : List (List A)) ->
  Eq
    (DTMKN.d.«84011102582061903d4b0e3bb04e9ac15e179d35e6e4ae0b358285c91d29c5426b6c590f318a»
      A op e (List.flatten chunks))
    (DTMKN.d.«84011102582061903d4b0e3bb04e9ac15e179d35e6e4ae0b358285c91d29c5426b6c590f318a»
      A op e
      (List.map
        (DTMKN.d.«84011102582061903d4b0e3bb04e9ac15e179d35e6e4ae0b358285c91d29c5426b6c590f318a»
          A op e) chunks))
