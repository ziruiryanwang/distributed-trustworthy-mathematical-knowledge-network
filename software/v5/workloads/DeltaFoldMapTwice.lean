-- Owner-chosen downstream use of the actually retained mapped-fold theorem.
-- Authoring success alone is not mathematical admission.
set_option autoImplicit false
noncomputable section
universe u v w x
namespace OwnerV5
theorem fold_map_twice_received {A : Type u} {B : Type v} {C : Type w} {D : Type x}
    (first : A -> B) (second : B -> C) (leaf : C -> D) (node : D -> D -> D)
    (e : DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.Tree A) :
    DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.fold leaf node
      (DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.map second
        (DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.map first e)) =
    DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.fold
      (fun a => leaf (second (first a))) node e :=
  Eq.trans
    (DMKN.Mod.«4adbc049e4d1e29ec045d64c7dba9e27bdd506dfa6c7fb707f022be40439e742».OwnerV5.fold_map_received
      second leaf node
      (DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5.map first e))
    (DMKN.Mod.«4adbc049e4d1e29ec045d64c7dba9e27bdd506dfa6c7fb707f022be40439e742».OwnerV5.fold_map_received
      first (fun b => leaf (second b)) node e)
end OwnerV5
