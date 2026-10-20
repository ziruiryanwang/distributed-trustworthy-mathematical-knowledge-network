-- Owner-authored reusable method over an already certified Tree interface.
-- The four evaluator equations are genuine premises, not supplied for free.
-- The source is untrusted until fresh native checking accepts its output.
set_option autoImplicit false
noncomputable section
universe u v
namespace OwnerV5
theorem evaluator_unique {A : Type u} {B : Type v}
    (L : A -> B) (N : B -> B -> B)
    (h k : DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.Tree A -> B)
    (h_leaf : forall x, h (DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.Tree.leaf x) = L x)
    (h_node : forall l r, h (DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.Tree.node l r) = N (h l) (h r))
    (k_leaf : forall x, k (DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.Tree.leaf x) = L x)
    (k_node : forall l r, k (DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.Tree.node l r) = N (k l) (k r))
    (t : DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.Tree A) :
    h t = k t := by
  induction t using DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.Tree.rec with
  | leaf x => exact Eq.trans (h_leaf x) (Eq.symm (k_leaf x))
  | node l r ihl ihr =>
    exact Eq.trans (h_node l r)
      (Eq.trans (DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.binary_congr N ihl ihr)
        (Eq.symm (k_node l r)))
end OwnerV5
