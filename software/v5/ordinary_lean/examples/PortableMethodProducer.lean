module

public import Init
public meta import PortableOwnerConstructCommand
public meta import PortableConstructExportCommand

/- Source-only owner-authoring template. A protected controller must replace
   each complete quoted sentinel literal exactly once with a bounded,
   Lean-quoted selected value
   in a fresh source file before execution. These sentinel strings are not a
   selected context or a grant. This file itself is not a runnable selection.

   The method is elementary existing mathematics, not a novelty/growth claim.
   Its purpose is an ordinary source -> portable evidence -> fresh independent
   discovery/use/contribution discriminator. Never import the producer module
   into that fresh consumer or promote this authoring artifact to acceptance. -/

public section

#ordinary_construct_portable "__DMKN_REQUEST_DIRECTORY__" "__DMKN_SEMANTIC_ID__" "__DMKN_CONTEXT_ROOT__" "__DMKN_FOUNDATION_ID__"

namespace DMKN.PortableMethod

universe u

/-- A transformation preserves a predicate whenever that predicate holds. -/
def Stable {α : Sort u} (f : α → α) (P : α → Prop) : Prop :=
  ∀ x, P x → P (f x)

/-- Two predicate-preserving transformations compose without another
    preservation argument for the composite. No equality or choice is needed. -/
theorem stable_compose {α : Sort u} {f g : α → α} {P : α → Prop}
    (hf : Stable f P) (hg : Stable g P) :
    Stable (fun x => f (g x)) P :=
  fun x hx => hf (g x) (hg x hx)

end DMKN.PortableMethod

#ordinary_export_constructed_portable DMKN.PortableMethod.stable_compose "__DMKN_CANDIDATE_OUTPUT__"
