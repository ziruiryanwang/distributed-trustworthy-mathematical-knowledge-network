namespace CommonsExample.Transformations

universe u

/-- A caller-chosen definition; no fixture name is required by the API. -/
def composeFour {α : Sort u} (f g h k : α → α) (x : α) : α :=
  f (g (h (k x)))

/-- Explicit method arguments avoid result-guided higher-order inference across
    the caller's newly defined composition. Both acquired methods are reused. -/
theorem preservesFour {α : Sort u} {f g h k : α → α} {P : α → Prop}
    (hf : DMKN.PortableMethod.Stable f P)
    (hg : DMKN.PortableMethod.Stable g P)
    (hh : DMKN.PortableMethod.Stable h P)
    (hk : DMKN.PortableMethod.Stable k P) :
    DMKN.PortableMethod.Stable (composeFour f g h k) P :=
  @DMKN.PortableMethod.stable_compose α f (fun x => g (h (k x))) P hf
    (@DMKN.PortableMethod.stable_threefold α g h k P hg hh hk)

end CommonsExample.Transformations
