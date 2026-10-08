/- Source-level workload for v5. No network or certificate authority is asserted.
   The generic lemmas are intended to become separately certified modules. -/
set_option autoImplicit false
set_option maxRecDepth 512
set_option maxHeartbeats 400000

universe u v w z
namespace CommonsV5

theorem binary_congr {A : Sort u} {B : Sort v} {C : Sort w}
    (f : A -> B -> C) {a a' : A} {b b' : B}
    (ha : a = a') (hb : b = b') : f a b = f a' b' := by
  cases ha
  cases hb
  rfl

inductive Tree (A : Type u) : Type u where
  | leaf : A -> Tree A
  | node : Tree A -> Tree A -> Tree A

def fold {A : Type u} {B : Type v}
    (leaf : A -> B) (node : B -> B -> B) : Tree A -> B
  | .leaf x => leaf x
  | .node l r => node (fold leaf node l) (fold leaf node r)

def map {A : Type u} {B : Type v} (f : A -> B) : Tree A -> Tree B
  | .leaf x => .leaf (f x)
  | .node l r => .node (map f l) (map f r)

theorem fusion {A : Type u} {B : Type v} {C : Type w}
    (leafB : A -> B) (nodeB : B -> B -> B)
    (leafC : A -> C) (nodeC : C -> C -> C) (h : B -> C)
    (hleaf : forall x, h (leafB x) = leafC x)
    (hnode : forall x y, h (nodeB x y) = nodeC (h x) (h y))
    (e : Tree A) : h (fold leafB nodeB e) = fold leafC nodeC e := by
  induction e with
  | leaf x => exact hleaf x
  | node l r ihl ihr =>
    exact (hnode (fold leafB nodeB l) (fold leafB nodeB r)).trans
      (binary_congr nodeC ihl ihr)

theorem fold_map {A : Type u} {B : Type v} {C : Type w}
    (f : A -> B) (leaf : B -> C) (node : C -> C -> C) (e : Tree A) :
    fold leaf node (map f e) = fold (fun x => leaf (f x)) node e := by
  induction e with
  | leaf x => rfl
  | node l r ihl ihr => exact binary_congr node ihl ihr

theorem fusion_map {A : Type u} {B : Type v} {C : Type w} {D : Type z}
    (f : A -> B) (leafC : B -> C) (nodeC : C -> C -> C)
    (leafD : B -> D) (nodeD : D -> D -> D) (h : C -> D)
    (hleaf : forall x, h (leafC x) = leafD x)
    (hnode : forall x y, h (nodeC x y) = nodeD (h x) (h y))
    (e : Tree A) :
    h (fold leafC nodeC (map f e)) = fold (fun x => leafD (f x)) nodeD e :=
  (fusion leafC nodeC leafD nodeD h hleaf hnode (map f e)).trans
    (fold_map f leafD nodeD e)

/- A substantive client: project a paired summary without computing the other
   interpretation. No laws on the two arbitrary node functions are needed. -/
theorem project_summary {A : Type u} {B : Type v} {C : Type w}
    (leafB : A -> B) (nodeB : B -> B -> B)
    (leafC : A -> C) (nodeC : C -> C -> C) (e : Tree A) :
    (fold (fun x => (leafB x, leafC x))
      (fun x y => (nodeB x.1 y.1, nodeC x.2 y.2)) e).1 = fold leafB nodeB e :=
  fusion (fun x => (leafB x, leafC x))
    (fun x y => (nodeB x.1 y.1, nodeC x.2 y.2))
    leafB nodeB Prod.fst (fun _ => rfl) (fun _ _ => rfl) e

end CommonsV5
