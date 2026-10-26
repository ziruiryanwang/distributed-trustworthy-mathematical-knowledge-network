/- Source body for the existing approved-project contribution wrapper.
   The wrapper supplies `public import Std.Data.HashMap.Lemmas` and
   `public section`. This file intentionally has no module/import preamble. -/

set_option autoImplicit false

namespace FiniteMapEffects

universe u v

/-- Finite write-only plans. Both branches of `choose` are possible. -/
inductive Plan (K : Type u) (V : Type v) where
  | skip : Plan K V
  | put (key : K) (value : V) : Plan K V
  | seq (first second : Plan K V) : Plan K V
  | choose (left right : Plan K V) : Plan K V

/-- The plan writes on every path, independently of its initial map. -/
@[expose] def mustWrite {K : Type u} {V : Type v} : Plan K V → Bool
  | .skip => false
  | .put _ _ => true
  | .seq p q => mustWrite p || mustWrite q
  | .choose p q => mustWrite p && mustWrite q

/-- Relational execution; there is no erase, failure, loop or guard correlation. -/
inductive Exec {K : Type u} {V : Type v} [BEq K] [Hashable K] :
    Plan K V → Std.HashMap K V → Std.HashMap K V → Prop where
  | skip (m : Std.HashMap K V) : Exec .skip m m
  | put (m : Std.HashMap K V) (key : K) (value : V) :
      Exec (.put key value) m (m.insert key value)
  | seq {p q : Plan K V} {m n r : Std.HashMap K V} :
      Exec p m n → Exec q n r → Exec (.seq p q) m r
  | chooseLeft {p q : Plan K V} {m n : Std.HashMap K V} :
      Exec p m n → Exec (.choose p q) m n
  | chooseRight {p q : Plan K V} {m n : Std.HashMap K V} :
      Exec q m n → Exec (.choose p q) m n

private theorem or_true_cases {a b : Bool} (h : (a || b) = true) :
    a = true ∨ b = true := by
  cases a with
  | false => exact Or.inr h
  | true => exact Or.inl rfl

private theorem or_false_parts {a b : Bool} (h : (a || b) = false) :
    a = false ∧ b = false := by
  cases a with
  | false => exact ⟨rfl, h⟩
  | true => cases h

private theorem and_true_parts {a b : Bool} (h : (a && b) = true) :
    a = true ∧ b = true := by
  cases a with
  | false => cases h
  | true => exact ⟨rfl, h⟩

private theorem and_false_cases {a b : Bool} (h : (a && b) = false) :
    a = false ∨ b = false := by
  cases a with
  | false => exact Or.inl rfl
  | true => exact Or.inr h

variable {K : Type u} {V : Type v} [BEq K] [Hashable K]

/-- A zero summary has an actual path that leaves the exact map unchanged. -/
theorem zero_effect_witness (p : Plan K V) (m : Std.HashMap K V) :
    mustWrite p = false → Exec p m m := by
  induction p with
  | skip =>
      intro _
      exact Exec.skip m
  | put key value =>
      intro h
      cases h
  | seq p q ihp ihq =>
      intro h
      have parts := or_false_parts h
      exact Exec.seq (ihp parts.1) (ihq parts.2)
  | choose p q ihp ihq =>
      intro h
      cases and_false_cases h with
      | inl hp => exact Exec.chooseLeft (ihp hp)
      | inr hq => exact Exec.chooseRight (ihq hq)

variable [EquivBEq K] [LawfulHashable K]

/-- Every execution preserves an initially nonempty map. -/
theorem preserves_nonempty {p : Plan K V} {m n : Std.HashMap K V}
    (execution : Exec p m n) : m.isEmpty = false → n.isEmpty = false := by
  induction execution with
  | skip m =>
      intro h
      exact h
  | put m key value =>
      intro _
      exact Std.HashMap.isEmpty_insert
  | seq first second ihFirst ihSecond =>
      intro h
      exact ihSecond (ihFirst h)
  | chooseLeft branch ih =>
      exact ih
  | chooseRight branch ih =>
      exact ih

/-- A guaranteed write establishes nonemptiness from any initial map. -/
theorem forces_nonempty {p : Plan K V} {m n : Std.HashMap K V}
    (execution : Exec p m n) : mustWrite p = true → n.isEmpty = false := by
  induction execution with
  | skip m =>
      intro h
      cases h
  | put m key value =>
      intro _
      exact Std.HashMap.isEmpty_insert
  | seq first second ihFirst ihSecond =>
      intro h
      cases or_true_cases h with
      | inl hp => exact preserves_nonempty second (ihFirst hp)
      | inr hq => exact ihSecond hq
  | chooseLeft branch ih =>
      intro h
      exact ih (and_true_parts h).1
  | chooseRight branch ih =>
      intro h
      exact ih (and_true_parts h).2

/-- Exact weakest precondition for every result of a finite plan to be nonempty. -/
theorem nonempty_iff (p : Plan K V) (m : Std.HashMap K V) :
    (∀ n, Exec p m n → n.isEmpty = false) ↔
      (m.isEmpty = false ∨ mustWrite p = true) := by
  constructor
  · intro allNonempty
    cases effect : mustWrite p with
    | false => exact Or.inl (allNonempty m (zero_effect_witness p m effect))
    | true => exact Or.inr rfl
  · intro sufficient n execution
    cases sufficient with
    | inl initial => exact preserves_nonempty execution initial
    | inr writes => exact forces_nonempty execution writes

/-- An optional first write followed by two writing alternatives forces a write. -/
theorem optional_then_writing_choice {m n : Std.HashMap K V}
    (k₀ k₁ k₂ : K) (v₀ v₁ v₂ : V)
    (execution : Exec
      (.seq (.choose (.put k₀ v₀) .skip)
        (.choose (.put k₁ v₁) (.put k₂ v₂))) m n) :
    n.isEmpty = false :=
  forces_nonempty execution rfl

/-- For an empty input the skip alternative gives a concrete empty outcome. -/
theorem optional_write_empty_outcome (m : Std.HashMap K V) (key : K) (value : V)
    (emptyInput : m.isEmpty = true) :
    ∃ n, Exec (.choose (.put key value) .skip) m n ∧ n.isEmpty = true :=
  ⟨m, Exec.chooseRight (Exec.skip m), emptyInput⟩

end FiniteMapEffects
