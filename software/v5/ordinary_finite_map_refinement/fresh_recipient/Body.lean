/- Body for a fresh recipient's approved Std-only project. The public contribution
   request reconstructs the acquired theory above this recipient's own Std root. -/

set_option autoImplicit false

namespace FiniteMapRecipient

open FiniteMapEffects FiniteMapRefinement

universe u v

/-- Sequence distributes over choice for contextual nonemptiness observations.
    This claims neither equal output maps nor equal execution traces. -/
theorem seq_choose_contextually_equivalent
    {K : Type u} {V : Type v}
    [BEq K] [Hashable K] [EquivBEq K] [LawfulHashable K]
    (p q r : Plan K V) (e : Std.HashMap K V) (he : e.isEmpty = true) :
    ContextuallyEquivalent (.seq p (.choose q r))
      (.choose (.seq p q) (.seq p r)) := by
  apply (contextual_equivalence_iff
    (.seq p (.choose q r)) (.choose (.seq p q) (.seq p r)) e he).mpr
  change (mustWrite p || (mustWrite q && mustWrite r)) =
    ((mustWrite p || mustWrite q) && (mustWrite p || mustWrite r))
  cases hp : mustWrite p <;> cases hq : mustWrite q <;>
    cases hr : mustWrite r <;> rfl

end FiniteMapRecipient
