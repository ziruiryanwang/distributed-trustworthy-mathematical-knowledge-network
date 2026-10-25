module
public import Init
public section

/- An asymmetric calculus of idempotent repairs. No novelty claim is made
   for idempotents themselves; the interface tracks preservation in run order. -/
namespace RepairTheory
universe u

structure Repair (α : Type u) where
  apply : α → α
  stable : ∀ x, apply (apply x) = apply x

variable {α : Type u}

@[expose] def Fixed (r : Repair α) (x : α) : Prop := r.apply x = x

/-- `Follows r s`: running `s` preserves every state already fixed by `r`. -/
@[expose] def Follows (r s : Repair α) : Prop :=
  ∀ x, Fixed r x → Fixed r (s.apply x)

theorem follows_iff (r s : Repair α) :
    Follows r s ↔ ∀ x, r.apply (s.apply (r.apply x)) = s.apply (r.apply x) := by
  constructor
  · intro h x
    exact h (r.apply x) (r.stable x)
  · intro h x hx
    change r.apply x = x at hx
    exact (congrArg (fun y => r.apply (s.apply y)) hx).symm.trans
      ((h x).trans (congrArg s.apply hx))

/-- Run `r` first, then `s`. The proof certifies the order. -/
@[expose] def merge (r s : Repair α) (h : Follows r s) : Repair α where
  apply x := s.apply (r.apply x)
  stable x := by
    have hr : r.apply (s.apply (r.apply x)) = s.apply (r.apply x) :=
      h (r.apply x) (r.stable x)
    exact (congrArg s.apply hr).trans (s.stable (r.apply x))

theorem merge_settles (r s : Repair α) (h : Follows r s) (x : α) :
    Fixed r ((merge r s h).apply x) ∧ Fixed s ((merge r s h).apply x) :=
  ⟨h (r.apply x) (r.stable x), s.stable (r.apply x)⟩

theorem merge_fixed_iff (r s : Repair α) (h : Follows r s) (x : α) :
    Fixed (merge r s h) x ↔ Fixed r x ∧ Fixed s x := by
  constructor
  · intro hx
    exact hx ▸ merge_settles r s h x
  · intro hx
    exact (congrArg s.apply hx.1).trans hx.2

/-- A completed prefix exposes its joint constraint, not its separate history. -/
theorem follows_merge_iff (r s t : Repair α) (h : Follows r s) :
    Follows (merge r s h) t ↔
      ∀ x, Fixed r x → Fixed s x → Fixed r (t.apply x) ∧ Fixed s (t.apply x) := by
  constructor
  · intro ht x hr hs
    exact (merge_fixed_iff r s h (t.apply x)).mp
      (ht x ((merge_fixed_iff r s h x).mpr ⟨hr, hs⟩))
  · intro ht x hx
    have hx' := (merge_fixed_iff r s h x).mp hx
    exact (merge_fixed_iff r s h (t.apply x)).mpr (ht x hx'.1 hx'.2)

/-- Lists run from left to right. -/
@[expose] def run : List (Repair α) → α → α
  | [], x => x
  | r :: rs, x => run rs (r.apply x)

@[expose] def Settled : List (Repair α) → α → Prop
  | [], _ => True
  | r :: rs, x => Fixed r x ∧ Settled rs x

/-- A sufficient discipline: each later repair preserves each earlier one. -/
@[expose] def Safe : List (Repair α) → Prop
  | [] => True
  | r :: rs => (∀ s, s ∈ rs → Follows r s) ∧ Safe rs

theorem run_preserves (r : Repair α) :
    ∀ rs : List (Repair α), (∀ s, s ∈ rs → Follows r s) →
      ∀ x, Fixed r x → Fixed r (run rs x) := by
  intro rs
  induction rs with
  | nil =>
      intro _ _ hx
      exact hx
  | cons s ss ih =>
      intro h x hx
      exact ih (fun t ht => h t (List.mem_cons_of_mem s ht))
        (s.apply x) (h s List.mem_cons_self x hx)

theorem run_of_settled :
    ∀ rs : List (Repair α), ∀ x, Settled rs x → run rs x = x := by
  intro rs
  induction rs with
  | nil => intro _ _; rfl
  | cons r rs ih =>
      intro x hx
      exact (congrArg (run rs) hx.1).trans (ih x hx.2)

theorem run_settles :
    ∀ rs : List (Repair α), Safe rs → ∀ x, Settled rs (run rs x) := by
  intro rs
  induction rs with
  | nil => intro _ _; trivial
  | cons r rs ih =>
      intro h x
      exact ⟨run_preserves r rs h.1 (r.apply x) (r.stable x), ih h.2 (r.apply x)⟩

theorem run_fixed_iff (rs : List (Repair α)) (h : Safe rs) (x : α) :
    run rs x = x ↔ Settled rs x :=
  ⟨fun hx => hx ▸ run_settles rs h x, run_of_settled rs x⟩

theorem run_stable (rs : List (Repair α)) (h : Safe rs) (x : α) :
    run rs (run rs x) = run rs x :=
  run_of_settled rs (run rs x) (run_settles rs h x)

@[expose] def schedule (rs : List (Repair α)) (h : Safe rs) : Repair α where
  apply := run rs
  stable := run_stable rs h

/- A noncanonical-choice model. The two accepted states are `some false` and
   `some true`; a repair chooses one only when presented with `none`. -/
@[expose] def choose (b : Bool) : Repair (Option Bool) where
  apply
    | none => some b
    | some c => some c
  stable x := by cases x <;> rfl

theorem choose_follows (a b : Bool) : Follows (choose a) (choose b) := by
  intro x hx
  cases x with
  | none => cases hx
  | some c => rfl

/-- Even mutual compatibility does not give order-independent outputs. -/
theorem choice_order_matters :
    run [choose false, choose true] none ≠
      run [choose true, choose false] none := by
  decide

/- Contextual preservation can be strictly weaker than pairwise preservation. -/
@[expose] def zeroLeft : Repair (Bool × Bool) where
  apply x := (false, x.2)
  stable _ := rfl

@[expose] def zeroRight : Repair (Bool × Bool) where
  apply x := (x.1, false)
  stable _ := rfl

@[expose] def copyRight : Repair (Bool × Bool) where
  apply x := (x.2, x.2)
  stable _ := rfl

theorem zeroRight_follows_zeroLeft : Follows zeroLeft zeroRight := by
  intro x hx
  exact congrArg (fun b => (b, false)) (congrArg Prod.fst hx)

theorem copyRight_follows_joint :
    Follows (merge zeroLeft zeroRight zeroRight_follows_zeroLeft) copyRight := by
  intro x hx
  change (false, false) = x at hx
  cases hx
  rfl

theorem copyRight_does_not_follow_zeroLeft : ¬ Follows zeroLeft copyRight := by
  intro h
  have bad := h (false, true) rfl
  have impossible : false = true := congrArg Prod.fst bad
  cases impossible

end RepairTheory
