module
public import TheoryA
public section

/- Closure operators supply canonical choice to the asymmetric repair calculus.
   This is a bridge to established order theory, not a novelty claim. -/
namespace RepairTheory.ClosureBridge
universe u
variable {α : Type u}

structure OrderData (α : Type u) where
  le : α → α → Prop
  refl : ∀ x, le x x
  trans : ∀ {x y z}, le x y → le y z → le x z
  antisymm : ∀ {x y}, le x y → le y x → x = y

/-- An existing repair adds information and respects the information order. -/
structure IsClosure (o : OrderData α) (r : Repair α) : Prop where
  extensive : ∀ x, o.le x (r.apply x)
  monotone : ∀ {x y}, o.le x y → o.le (r.apply x) (r.apply y)

theorem below_fixed (o : OrderData α) (r : Repair α) (hr : IsClosure o r)
    {x y : α} (hxy : o.le x y) (hy : Fixed r y) : o.le (r.apply x) y := by
  change r.apply y = y at hy
  exact hy ▸ hr.monotone hxy

/-- Preservation in run order is exactly an inequality between the two orders. -/
theorem follows_iff_swap_le (o : OrderData α) (r s : Repair α)
    (hr : IsClosure o r) (hs : IsClosure o s) :
    Follows r s ↔ ∀ x, o.le (r.apply (s.apply x)) (s.apply (r.apply x)) := by
  constructor
  · intro h x
    have hle := hr.monotone (hs.monotone (hr.extensive x))
    exact (follows_iff r s).mp h x ▸ hle
  · intro h x hx
    apply o.antisymm
    · change r.apply x = x at hx
      exact (congrArg s.apply hx) ▸ h x
    · exact hr.extensive (s.apply x)

theorem mutual_follows_iff_commute (o : OrderData α) (r s : Repair α)
    (hr : IsClosure o r) (hs : IsClosure o s) :
    (Follows r s ∧ Follows s r) ↔
      ∀ x, r.apply (s.apply x) = s.apply (r.apply x) := by
  constructor
  · intro h x
    exact o.antisymm ((follows_iff_swap_le o r s hr hs).mp h.1 x)
      ((follows_iff_swap_le o s r hs hr).mp h.2 x)
  · intro h
    constructor
    · apply (follows_iff_swap_le o r s hr hs).mpr
      intro x
      rw [h x]
      exact o.refl _
    · apply (follows_iff_swap_le o s r hs hr).mpr
      intro x
      rw [h x]
      exact o.refl _

/-- Fixed-state inclusion reverses the pointwise order on closure operators. -/
theorem pointwise_le_iff_fixed_inclusion (o : OrderData α) (r s : Repair α)
    (hr : IsClosure o r) (hs : IsClosure o s) :
    (∀ x, o.le (r.apply x) (s.apply x)) ↔
      ∀ x, Fixed s x → Fixed r x := by
  constructor
  · intro h x hx
    apply o.antisymm
    · change s.apply x = x at hx
      exact Eq.mp (congrArg (fun y => o.le (r.apply x) y) hx) (h x)
    · exact hr.extensive x
  · intro h x
    exact below_fixed o r hr (hs.extensive x) (h (s.apply x) (s.stable x))

theorem same_fixed_same_output (o : OrderData α) (r s : Repair α)
    (hr : IsClosure o r) (hs : IsClosure o s)
    (h : ∀ x, Fixed r x ↔ Fixed s x) (x : α) : r.apply x = s.apply x :=
  o.antisymm
    ((pointwise_le_iff_fixed_inclusion o r s hr hs).mpr (fun y => (h y).mpr) x)
    ((pointwise_le_iff_fixed_inclusion o s r hs hr).mpr (fun y => (h y).mp) x)

@[expose] def AllClosure (o : OrderData α) (rs : List (Repair α)) : Prop :=
  ∀ r, r ∈ rs → IsClosure o r

theorem run_extensive (o : OrderData α) :
    ∀ rs : List (Repair α), AllClosure o rs → ∀ x, o.le x (run rs x) := by
  intro rs
  induction rs with
  | nil => intro _ x; exact o.refl x
  | cons r rs ih =>
      intro h x
      exact o.trans ((h r List.mem_cons_self).extensive x)
        (ih (fun s hs => h s (List.mem_cons_of_mem r hs)) (r.apply x))

/-- Any run stays below every jointly fixed upper bound of its input. -/
theorem run_below_settled (o : OrderData α) :
    ∀ rs : List (Repair α), AllClosure o rs →
      ∀ x y, o.le x y → Settled rs y → o.le (run rs x) y := by
  intro rs
  induction rs with
  | nil => intro _ _ _ hxy _; exact hxy
  | cons r rs ih =>
      intro h x y hxy hy
      exact ih (fun s hs => h s (List.mem_cons_of_mem r hs)) (r.apply x) y
        (below_fixed o r (h r List.mem_cons_self) hxy hy.1) hy.2

/-- A safe run computes the least jointly fixed state above its input. -/
theorem run_is_least (o : OrderData α) (rs : List (Repair α))
    (hc : AllClosure o rs) (hs : Safe rs) (x : α) :
    o.le x (run rs x) ∧ Settled rs (run rs x) ∧
      ∀ y, o.le x y → Settled rs y → o.le (run rs x) y :=
  ⟨run_extensive o rs hc x, run_settles rs hs x,
    fun y hxy hy => run_below_settled o rs hc x y hxy hy⟩

/-- Equivalent joint constraints give equal results, even for different lists. -/
theorem same_constraints_same_run (o : OrderData α) (rs ss : List (Repair α))
    (hr : AllClosure o rs) (hs : AllClosure o ss) (sr : Safe rs) (ssafe : Safe ss)
    (same : ∀ y, Settled rs y ↔ Settled ss y) (x : α) : run rs x = run ss x :=
  o.antisymm
    (run_below_settled o rs hr x (run ss x) (run_extensive o ss hs x)
      ((same _).mpr (run_settles ss ssafe x)))
    (run_below_settled o ss hs x (run rs x) (run_extensive o rs hr x)
      ((same _).mp (run_settles rs sr x)))

/- Two Boolean facts ordered by inclusion: installing a fact can enable a rule. -/
@[expose] def pairOrder : OrderData (Bool × Bool) where
  le x y := x.1 ≤ y.1 ∧ x.2 ≤ y.2
  refl x := ⟨Bool.le_refl x.1, Bool.le_refl x.2⟩
  trans := by
    intro x y z hxy hyz
    exact ⟨Bool.le_trans hxy.1 hyz.1, Bool.le_trans hxy.2 hyz.2⟩
  antisymm := by
    intro x y hxy hyx
    exact Prod.ext (Bool.le_antisymm hxy.1 hyx.1) (Bool.le_antisymm hxy.2 hyx.2)

@[expose] def installLeft : Repair (Bool × Bool) where
  apply x := (true, x.2)
  stable _ := rfl

@[expose] def propagateRight : Repair (Bool × Bool) where
  apply x := (x.1, x.1 || x.2)
  stable x := by
    cases x with
    | mk a b => cases a <;> cases b <;> rfl

theorem installLeft_closure : IsClosure pairOrder installLeft where
  extensive x := ⟨Bool.le_true x.1, Bool.le_refl x.2⟩
  monotone := by
    intro x y h
    exact ⟨Bool.le_refl true, h.2⟩

theorem propagateRight_closure : IsClosure pairOrder propagateRight where
  extensive x := by
    have hor : ∀ a b : Bool, b ≤ (a || b) := by decide
    exact ⟨Bool.le_refl x.1, hor x.1 x.2⟩
  monotone := by
    intro x y h
    have hor : ∀ a b c d : Bool, a ≤ c → b ≤ d → (a || b) ≤ (c || d) := by decide
    exact ⟨h.1, hor _ _ _ _ h.1 h.2⟩

theorem propagation_follows_installation : Follows installLeft propagateRight := by
  intro x hx
  exact congrArg (fun b => (b, x.1 || x.2)) (congrArg Prod.fst hx)

theorem installation_does_not_follow_propagation : ¬ Follows propagateRight installLeft := by
  intro h
  have impossible : true = false := congrArg Prod.snd (h (false, false) rfl)
  cases impossible

/-- One-way preservation does not make two closure operators commute. -/
theorem directed_closures_need_order :
    propagateRight.apply (installLeft.apply (false, false)) ≠
      installLeft.apply (propagateRight.apply (false, false)) := by decide

/-- A's distinct choices cannot both be closures for any one partial order. -/
theorem choices_have_no_common_closure_order (o : OrderData (Option Bool)) :
    ¬ (IsClosure o (choose false) ∧ IsClosure o (choose true)) := by
  intro h
  have heq := (mutual_follows_iff_commute o (choose false) (choose true) h.1 h.2).mp
    ⟨choose_follows false true, choose_follows true false⟩ none
  have impossible : true = false := Option.some.inj heq
  cases impossible

end RepairTheory.ClosureBridge
