/- UNCHECKED developmental proposal, 2026-10-28.
   This is a source body, following the corpus's contribution-body convention.
   Its only retained-theory dependency is FiniteMapRefinement.Context from
   software/v5/ordinary_finite_map_refinement/BodyParametric.lean.
   A later selected wrapper must import that approved compiled contribution.
   No compiler, import execution, or native check was performed in this phase.

   One extension: exact contextual guarantees for finite plans with destructive
   observation updates. Root supplied a seriality/realizability caution; see
   INVESTIGATION.md for the assistance and complete read log.
-/

set_option autoImplicit false

namespace ResetEffects

universe u v

/-- The least attainable Boolean observation as a function of the input.
    A compound plan with mode zero may also have true outcomes. -/
inductive Mode where
  | zero
  | keep
  | one

namespace Mode

def eval : Mode → Bool → Bool
  | .zero, _ => false
  | .keep, b => b
  | .one, _ => true

/-- Run the first summary, then the second. -/
def after (first second : Mode) : Mode :=
  match second with
  | .zero => .zero
  | .keep => first
  | .one => .one

/-- Both choice branches are possible; guarantees require both branches. -/
def meet : Mode → Mode → Mode
  | .zero, _ => .zero
  | .keep, .zero => .zero
  | .keep, .keep => .keep
  | .keep, .one => .keep
  | .one, b => b

def Refines (a b : Mode) : Prop :=
  ∀ x, eval a x = true → eval b x = true

theorem eval_after (a b : Mode) (x : Bool) :
    eval (after a b) x = eval b (eval a x) := by
  cases a <;> cases b <;> cases x <;> rfl

theorem eval_meet (a b : Mode) (x : Bool) :
    eval (meet a b) x = (eval a x && eval b x) := by
  cases a <;> cases b <;> cases x <;> rfl

/-- The lower of two Boolean observations is one of those observations. -/
theorem meet_attained (a b : Mode) (x : Bool) :
    eval (meet a b) x = eval a x ∨ eval (meet a b) x = eval b x := by
  cases a <;> cases b <;> cases x <;>
    first | exact Or.inl rfl | exact Or.inr rfl

theorem input_mono (a : Mode) {x y : Bool} (h : x = true → y = true) :
    eval a x = true → eval a y = true := by
  cases a with
  | zero => exact fun impossible => impossible
  | keep => exact h
  | one => exact fun _ => rfl

theorem refines_refl (a : Mode) : Refines a a :=
  fun _ h => h

theorem after_mono {a a' b b' : Mode}
    (ha : Refines a a') (hb : Refines b b') :
    Refines (after a b) (after a' b') := by
  intro x h
  rw [eval_after] at h ⊢
  exact hb _ (input_mono b (ha x) h)

private theorem and_parts {a b : Bool} (h : (a && b) = true) :
    a = true ∧ b = true := by
  cases a with
  | false => cases h
  | true => exact ⟨rfl, h⟩

theorem meet_mono {a a' b b' : Mode}
    (ha : Refines a a') (hb : Refines b b') :
    Refines (meet a b) (meet a' b') := by
  intro x h
  rw [eval_meet] at h ⊢
  have parts := and_parts h
  rw [ha x parts.1, hb x parts.2]
  rfl

theorem meet_left {a b : Mode} {x : Bool} (h : eval (meet a b) x = true) :
    eval a x = true := by
  rw [eval_meet] at h
  exact (and_parts h).1

theorem meet_right {a b : Mode} {x : Bool} (h : eval (meet a b) x = true) :
    eval b x = true := by
  rw [eval_meet] at h
  exact (and_parts h).2

end Mode

/-- Finite plans over independently specified total atomic updates. -/
inductive Plan (A : Type u) where
  | skip : Plan A
  | atom (action : A) : Plan A
  | seq (first second : Plan A) : Plan A
  | choose (left right : Plan A) : Plan A

variable {A : Type u} {S : Type v}

def summary (effect : A → Mode) : Plan A → Mode
  | .skip => .keep
  | .atom a => effect a
  | .seq p q => Mode.after (summary effect p) (summary effect q)
  | .choose p q => Mode.meet (summary effect p) (summary effect q)

/-- No failure, guard, loop, or correlated branch restriction is present. -/
inductive Exec (step : A → S → S) : Plan A → S → S → Prop where
  | skip (s : S) : Exec step .skip s s
  | atom (a : A) (s : S) : Exec step (.atom a) s (step a s)
  | seq {p q : Plan A} {s m t : S} :
      Exec step p s m → Exec step q m t → Exec step (.seq p q) s t
  | chooseLeft {p q : Plan A} {s t : S} :
      Exec step p s t → Exec step (.choose p q) s t
  | chooseRight {p q : Plan A} {s t : S} :
      Exec step q s t → Exec step (.choose p q) s t

def Guarantee (observe : S → Bool) (step : A → S → S)
    (p : Plan A) (s : S) : Prop :=
  ∀ t, Exec step p s t → observe t = true

section Semantics

variable (observe : S → Bool) (step : A → S → S) (effect : A → Mode)
variable (atomic_law : ∀ a s,
  observe (step a s) = Mode.eval (effect a) (observe s))

include atomic_law

/-- Every actual result lies above the summarized observation. -/
theorem execution_lower_bound {p : Plan A} {s t : S}
    (execution : Exec step p s t) :
    Mode.eval (summary effect p) (observe s) = true → observe t = true := by
  induction execution with
  | skip s => exact fun h => h
  | atom a s =>
      intro h
      exact (atomic_law a s).trans h
  | seq first second ihFirst ihSecond =>
      intro h
      simp only [summary, Mode.eval_after] at h
      exact ihSecond (Mode.input_mono _ ihFirst h)
  | chooseLeft branch ih =>
      intro h
      exact ih (Mode.meet_left h)
  | chooseRight branch ih =>
      intro h
      exact ih (Mode.meet_right h)

/-- Seriality and exactness together: the summarized observation is attained.
    In the sequence case the suffix starts from an actual prefix outcome. -/
theorem minimum_outcome (p : Plan A) :
    ∀ s, ∃ t, Exec step p s t ∧
      observe t = Mode.eval (summary effect p) (observe s) := by
  induction p with
  | skip =>
      intro s
      exact ⟨s, Exec.skip s, rfl⟩
  | atom a =>
      intro s
      exact ⟨step a s, Exec.atom a s, atomic_law a s⟩
  | seq p q ihp ihq =>
      intro s
      obtain ⟨m, hp, hm⟩ := ihp s
      obtain ⟨t, hq, ht⟩ := ihq m
      refine ⟨t, Exec.seq hp hq, ?_⟩
      simp only [summary, Mode.eval_after]
      rw [← hm]
      exact ht
  | choose p q ihp ihq =>
      intro s
      cases Mode.meet_attained (summary effect p) (summary effect q) (observe s) with
      | inl h =>
          obtain ⟨t, hp, ht⟩ := ihp s
          exact ⟨t, Exec.chooseLeft hp, ht.trans h.symm⟩
      | inr h =>
          obtain ⟨t, hq, ht⟩ := ihq s
          exact ⟨t, Exec.chooseRight hq, ht.trans h.symm⟩

theorem guarantee_iff (p : Plan A) (s : S) :
    Guarantee observe step p s ↔
      Mode.eval (summary effect p) (observe s) = true := by
  constructor
  · intro allTrue
    obtain ⟨t, ht, heq⟩ := minimum_outcome observe step effect atomic_law p s
    exact heq.symm.trans (allTrue t ht)
  · intro h t ht
    exact execution_lower_bound observe step effect atomic_law ht h

end Semantics

/-- Reuse the existing polymorphic context type, with the extended plan type. -/
def fill : FiniteMapRefinement.Context (Plan A) → Plan A → Plan A
  | .hole, p => p
  | .seqLeft c r, p => .seq (fill c p) r
  | .seqRight l c, p => .seq l (fill c p)
  | .chooseLeft c r, p => .choose (fill c p) r
  | .chooseRight l c, p => .choose l (fill c p)

theorem summary_fill_mono (effect : A → Mode)
    (c : FiniteMapRefinement.Context (Plan A)) (p q : Plan A)
    (h : Mode.Refines (summary effect p) (summary effect q)) :
    Mode.Refines (summary effect (fill c p)) (summary effect (fill c q)) := by
  induction c with
  | hole => exact h
  | seqLeft c r ih => exact Mode.after_mono ih (Mode.refines_refl _)
  | seqRight l c ih => exact Mode.after_mono (Mode.refines_refl _) ih
  | chooseLeft c r ih => exact Mode.meet_mono ih (Mode.refines_refl _)
  | chooseRight l c ih => exact Mode.meet_mono (Mode.refines_refl _) ih

def ContextuallyRefines (observe : S → Bool) (step : A → S → S)
    (p q : Plan A) : Prop :=
  ∀ c s, Guarantee observe step (fill c p) s → Guarantee observe step (fill c q) s

/-- Soundness does not require both Boolean observations to be inhabited. -/
theorem contextual_of_summary (observe : S → Bool) (step : A → S → S)
    (effect : A → Mode)
    (atomic_law : ∀ a s, observe (step a s) = Mode.eval (effect a) (observe s))
    (p q : Plan A) (h : Mode.Refines (summary effect p) (summary effect q)) :
    ContextuallyRefines observe step p q := by
  intro c s hp
  apply (guarantee_iff observe step effect atomic_law (fill c q) s).mpr
  apply summary_fill_mono effect c p q h (observe s)
  exact (guarantee_iff observe step effect atomic_law (fill c p) s).mp hp

/-- Exact contextual criterion. The two observation witnesses are essential
    to this uniform statement over all three abstract modes. -/
theorem contextual_iff (observe : S → Bool) (step : A → S → S)
    (effect : A → Mode)
    (atomic_law : ∀ a s, observe (step a s) = Mode.eval (effect a) (observe s))
    (s0 s1 : S) (h0 : observe s0 = false) (h1 : observe s1 = true)
    (p q : Plan A) :
    ContextuallyRefines observe step p q ↔
      Mode.Refines (summary effect p) (summary effect q) := by
  constructor
  · intro h b hb
    cases b with
    | false =>
        have hp : Guarantee observe step p s0 :=
          (guarantee_iff observe step effect atomic_law p s0).mpr
            (by simpa only [h0] using hb)
        have hq := (guarantee_iff observe step effect atomic_law q s0).mp
          (h .hole s0 hp)
        simpa only [h0] using hq
    | true =>
        have hp : Guarantee observe step p s1 :=
          (guarantee_iff observe step effect atomic_law p s1).mpr
            (by simpa only [h1] using hb)
        have hq := (guarantee_iff observe step effect atomic_law q s1).mp
          (h .hole s1 hp)
        simpa only [h1] using hq
  · exact contextual_of_summary observe step effect atomic_law p q

/-- A two-state instance exposes the new distinction between skip and reset. -/
def boolStep (action : Mode) (state : Bool) : Bool := Mode.eval action state

theorem skip_not_refined_by_reset :
    ¬ ContextuallyRefines (fun b : Bool => b) boolStep .skip (.atom .zero) := by
  intro h
  have hs : Guarantee (fun b : Bool => b) boolStep .skip true := by
    intro t ht
    cases ht
    rfl
  have impossible : false = true :=
    h .hole true hs false (Exec.atom Mode.zero true)
  cases impossible

/-- A write occurrence alone no longer guarantees a true final observation. -/
theorem write_then_reset_false :
    Exec boolStep (.seq (.atom .one) (.atom .zero)) false false :=
  Exec.seq (Exec.atom Mode.one false) (Exec.atom Mode.zero true)

end ResetEffects
