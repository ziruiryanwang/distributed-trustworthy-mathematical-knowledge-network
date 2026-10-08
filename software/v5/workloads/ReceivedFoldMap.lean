-- Owner-authored source fixture for genuine receipt-to-source integration.
-- The native authoring environment must supply the selected certified interfaces.
-- This source and its frontend export are not independently trusted acceptance.
set_option autoImplicit false
noncomputable section
universe u v w
namespace OwnerV5
theorem fold_map_received {A : Type u} {B : Type v} {C : Type w}
    (f : A -> B) (leaf : B -> C) (node : C -> C -> C)
    (e : DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.Tree A) :
    DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.fold leaf node
      (DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.map f e) =
    DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.fold
      (fun x => leaf (f x)) node e := by
  induction e using DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.Tree.rec with
  | leaf x => rfl
  | node l r ihl ihr =>
    exact DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.binary_congr node ihl ihr
end OwnerV5
