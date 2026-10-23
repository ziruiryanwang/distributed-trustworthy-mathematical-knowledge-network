module

public import Init
public meta import PortableOwnerConstructCommand
public meta import PortableConstructExportCommand

/- Owner-approved scratch source. The controller supplies B's already checked
   method through a bounded portable request; no producer module is imported.
   Each full quoted sentinel is replaced exactly once before local execution.
   The constructed theorem signature is an authoring assumption only. The
   exported successor still requires independent native admission into B. -/

public section

#ordinary_construct_portable "__DMKN_REQUEST_DIRECTORY__" "__DMKN_SEMANTIC_ID__" "__DMKN_CONTEXT_ROOT__" "__DMKN_FOUNDATION_ID__"

namespace DMKN.PortableMethod

universe u

/-- Reuse the acquired composition method twice to preserve a predicate through
    three transformations. No new preservation proof is unfolded here. -/
theorem stable_threefold {α : Sort u} {f g h : α → α} {P : α → Prop}
    (hf : Stable f P) (hg : Stable g P) (hh : Stable h P) :
    Stable (fun x => f (g (h x))) P :=
  stable_compose hf (stable_compose hg hh)

end DMKN.PortableMethod

#ordinary_export_constructed_portable DMKN.PortableMethod.stable_threefold "__DMKN_CANDIDATE_OUTPUT__"
