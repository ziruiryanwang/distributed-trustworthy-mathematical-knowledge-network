/- Source body for the approved-project contribution wrapper.
   The wrapper supplies `public import Std.Data.HashMap.Lemmas`,
   `public import FiniteMapEffects.Contribution`, and `public section`.
   This file intentionally has no module/import preamble. -/

set_option autoImplicit false

namespace FiniteMapRefinement

open FiniteMapEffects

universe u v

/-- A finite one-hole binary context over an arbitrary payload type. -/
inductive Context (A : Type u) where
  | hole : Context A
  | seqLeft (inner : Context A) (right : A) : Context A
  | seqRight (left : A) (inner : Context A) : Context A
  | chooseLeft (inner : Context A) (right : A) : Context A
  | chooseRight (left : A) (inner : Context A) : Context A

set_option bootstrap.genMatcherCode false in
/-- Substitute a plan into the unique hole. -/
@[expose] noncomputable def fill {K : Type u} {V : Type v} : Context (Plan K V) → Plan K V → Plan K V
  | .hole, p => p
  | .seqLeft c r, p => .seq (fill c p) r
  | .seqRight l c, p => .seq l (fill c p)
  | .chooseLeft c r, p => .choose (fill c p) r
  | .chooseRight l c, p => .choose l (fill c p)

variable {K : Type u} {V : Type v}

/-- Every possible execution from this input returns a nonempty map. -/
@[expose] noncomputable def NonemptyResults [BEq K] [Hashable K]
    (p : Plan K V) (m : Std.HashMap K V) : Prop :=
  ∀ n, Exec p m n → n.isEmpty = false

/-- Replacing `p` by `q` preserves its nonemptiness guarantees. -/
@[expose] noncomputable def Refines [BEq K] [Hashable K] (p q : Plan K V) : Prop :=
  ∀ m, NonemptyResults p m → NonemptyResults q m

/-- The same guarantee is preserved in every finite one-hole context. -/
@[expose] noncomputable def ContextuallyRefines [BEq K] [Hashable K] (p q : Plan K V) : Prop :=
  ∀ c m, NonemptyResults (fill c p) m → NonemptyResults (fill c q) m

/-- Agreement on nonemptiness guarantees in all contexts and on all inputs. -/
@[expose] noncomputable def ContextuallyEquivalent [BEq K] [Hashable K]
    (p q : Plan K V) : Prop :=
  ContextuallyRefines p q ∧ ContextuallyRefines q p

private theorem bool_or_mono (a b c d : Bool)
    (hab : a = true → b = true) (hcd : c = true → d = true) :
    (a || c) = true → (b || d) = true := by
  cases a with
  | false =>
      cases c with
      | false => exact fun h => Bool.noConfusion h
      | true =>
          have hd : d = true := hcd rfl
          cases hd
          cases b <;> exact fun _ => rfl
  | true =>
      have hb : b = true := hab rfl
      cases hb
      cases d <;> exact fun _ => rfl

private theorem bool_and_mono (a b c d : Bool)
    (hab : a = true → b = true) (hcd : c = true → d = true) :
    (a && c) = true → (b && d) = true := by
  cases a with
  | false =>
      cases c <;> exact fun h => Bool.noConfusion h
  | true =>
      cases c with
      | false => exact fun h => Bool.noConfusion h
      | true =>
          have hb : b = true := hab rfl
          have hd : d = true := hcd rfl
          cases hb
          cases hd
          exact fun _ => rfl

private theorem bool_eq_of_mutual_implication (a b : Bool)
    (hab : a = true → b = true) (hba : b = true → a = true) : a = b := by
  cases a with
  | false =>
      cases b with
      | false => rfl
      | true => exact False.elim (Bool.noConfusion (hba rfl))
  | true => exact (hab rfl).symm

/-- Boolean summary implication composes through every context. -/
theorem fill_summary_mono (c : Context (Plan K V)) (p q : Plan K V)
    (h : mustWrite p = true → mustWrite q = true) :
    mustWrite (fill c p) = true → mustWrite (fill c q) = true := by
  induction c with
  | hole => exact h
  | seqLeft c r ih =>
      exact bool_or_mono (mustWrite (fill c p)) (mustWrite (fill c q))
        (mustWrite r) (mustWrite r) ih (fun hr => hr)
  | seqRight l c ih =>
      exact bool_or_mono (mustWrite l) (mustWrite l)
        (mustWrite (fill c p)) (mustWrite (fill c q)) (fun hl => hl) ih
  | chooseLeft c r ih =>
      exact bool_and_mono (mustWrite (fill c p)) (mustWrite (fill c q))
        (mustWrite r) (mustWrite r) ih (fun hr => hr)
  | chooseRight l c ih =>
      exact bool_and_mono (mustWrite l) (mustWrite l)
        (mustWrite (fill c p)) (mustWrite (fill c q)) (fun hl => hl) ih

section Semantics

variable [BEq K] [Hashable K] [EquivBEq K] [LawfulHashable K]

/-- Summary implication preserves nonemptiness on every starting map. -/
theorem refines_of_summary (p q : Plan K V)
    (h : mustWrite p = true → mustWrite q = true) : Refines p q := by
  intro m hp
  apply (nonempty_iff q m).mpr
  have hp' := (nonempty_iff p m).mp hp
  cases hp' with
  | inl hm => exact Or.inl hm
  | inr hw => exact Or.inr (h hw)

/-- Soundness needs no designated empty input. -/
theorem contextual_refines_of_summary (p q : Plan K V)
    (h : mustWrite p = true → mustWrite q = true) :
    ContextuallyRefines p q := by
  intro c m hp
  exact refines_of_summary (fill c p) (fill c q) (fill_summary_mono c p q h) m hp

/-- Complete summary criterion, with an explicit empty-map witness. -/
theorem contextual_refines_iff (p q : Plan K V)
    (e : Std.HashMap K V) (he : e.isEmpty = true) :
    ContextuallyRefines p q ↔ (mustWrite p = true → mustWrite q = true) := by
  constructor
  · intro h hp
    have hn : NonemptyResults p e := (nonempty_iff p e).mpr (Or.inr hp)
    have hq : NonemptyResults q e := h .hole e hn
    have hq' := (nonempty_iff q e).mp hq
    cases hq' with
    | inl hem => exact False.elim (Bool.noConfusion (he.symm.trans hem))
    | inr hw => exact hw
  · exact contextual_refines_of_summary p q

/-- The failing true/false summary pair has an actual empty-result witness
    at the hole context, as well as a proof that contextual refinement fails. -/
theorem nonrefinement_witness (p q : Plan K V)
    (e : Std.HashMap K V) (he : e.isEmpty = true)
    (hp : mustWrite p = true) (hq : mustWrite q = false) :
    NonemptyResults p e ∧ Exec q e e ∧ e.isEmpty = true ∧
      ¬ ContextuallyRefines p q := by
  have hn : NonemptyResults p e := (nonempty_iff p e).mpr (Or.inr hp)
  have hrun : Exec q e e := zero_effect_witness q e hq
  refine ⟨hn, hrun, he, ?_⟩
  intro hctx
  have hem : e.isEmpty = false := hctx .hole e hn e hrun
  exact Bool.noConfusion (he.symm.trans hem)

/-- Equal summaries characterize exact equivalence for this observation. -/
theorem contextual_equivalence_iff (p q : Plan K V)
    (e : Std.HashMap K V) (he : e.isEmpty = true) :
    ContextuallyEquivalent p q ↔ mustWrite p = mustWrite q := by
  constructor
  · intro h
    exact bool_eq_of_mutual_implication (mustWrite p) (mustWrite q)
      ((contextual_refines_iff p q e he).mp h.1)
      ((contextual_refines_iff q p e he).mp h.2)
  · intro h
    constructor
    · exact contextual_refines_of_summary p q (fun hp => h.symm.trans hp)
    · exact contextual_refines_of_summary q p (fun hq => h.trans hq)

end Semantics

end FiniteMapRefinement
