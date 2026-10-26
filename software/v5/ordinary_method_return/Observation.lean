universe u v

theorem CommonsMethodReturn.observation_invariant
    {A : Type u} {B : Type v}
    (o : RepairTheory.ClosureBridge.OrderData A)
    (rs ss : List (RepairTheory.Repair A))
    (hr : RepairTheory.ClosureBridge.AllClosure o rs)
    (hs : RepairTheory.ClosureBridge.AllClosure o ss)
    (sr : RepairTheory.Safe rs)
    (ssafe : RepairTheory.Safe ss)
    (same : (y : A) -> Iff (RepairTheory.Settled rs y) (RepairTheory.Settled ss y))
    (obs : A -> B) (x : A) :
    Eq (obs (RepairTheory.run rs x)) (obs (RepairTheory.run ss x)) :=
  congrArg obs
    (RepairTheory.ClosureBridge.same_constraints_same_run
      o rs ss hr hs sr ssafe same x)
