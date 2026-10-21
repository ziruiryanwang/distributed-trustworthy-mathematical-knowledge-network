-- Trusted-owner example source; not yet compiled or admitted.
-- The exact retained evaluator method must first be independently admitted.
-- Publication roots: OwnerV5.mirror and OwnerV5.mirror_involution.
set_option autoImplicit false
noncomputable section
universe u
namespace OwnerV5

def mirror {A : Type u}
    (t : DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.Tree A) :
    DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.Tree A :=
  DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.Tree.rec
    (motive := fun _ : DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.Tree A =>
      DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.Tree A)
    (fun a => DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.Tree.leaf a)
    (fun _ _ ml mr => DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.Tree.node mr ml)
    t

theorem mirror_involution {A : Type u}
    (t : DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.Tree A) :
    mirror (mirror t) = t :=
  DMKN.Mod.«bbf0845d2622374699a93a9d8ccc6e565dd1c985e72441ec0eeae41bb03fc0c5».OwnerV5.evaluator_unique
    (fun a : A => DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.Tree.leaf a)
    (fun l r : DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.Tree A =>
      DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.Tree.node l r)
    (fun t : DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.Tree A => mirror (mirror t))
    (fun t : DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.Tree A => t)
    (fun _ => rfl)
    (fun _ _ => rfl)
    (fun _ => rfl)
    (fun _ _ => rfl)
    t

end OwnerV5
