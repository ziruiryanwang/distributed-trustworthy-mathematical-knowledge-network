namespace CommonsExample.Transformations

universe u

/-- A caller-chosen definition; no fixture name is required by the API. -/
def composeFour {α : Sort u} (f g h k : α → α) (x : α) : α :=
  f (g (h (k x)))

/-- Both previously acquired methods are used. This elementary statement
    tests the contribution interface, not novelty or net growth. -/
theorem preservesFour {α : Sort u} {f g h k : α → α} {P : α → Prop}
    (hf : DMKN.PortableMethod.Stable f P)
    (hg : DMKN.PortableMethod.Stable g P)
    (hh : DMKN.PortableMethod.Stable h P)
    (hk : DMKN.PortableMethod.Stable k P) :
    DMKN.PortableMethod.Stable (composeFour f g h k) P :=
  DMKN.PortableMethod.stable_compose hf
    (DMKN.PortableMethod.stable_threefold hg hh hk)

end CommonsExample.Transformations
