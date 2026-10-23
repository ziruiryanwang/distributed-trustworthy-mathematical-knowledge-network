import examples.ReadFootprint

/-!
Owner-authored downstream mathematical fixture. The `examples` import prefix
expects `software/v5/ordinary_lean` as a selected Lean module search root.

This source uses the producer's footprint interface and theorem explicitly.
It is not an independent-agent discovery experiment: the fixture author knows
the producer module. A later actual unknown-ID workflow must obtain that module
through the public search/acquisition path without fixture-ID injection.

As with the producer, source compilation is not independent mathematical
admission. Exported inert declarations must cross the ordinary checker boundary.
-/

set_option autoImplicit false

namespace DMKN.ReadFootprint.Consumer

universe u v

variable {α : Type u} {β : Type v}
variable [BEq α] [Hashable α] [EquivBEq α] [LawfulHashable α]

/-- Read a finite ordered snapshot; repeated keys and their order are retained. -/
def snapshot (ks : List α) (m : Std.ExtHashMap α β) : List (Option β) :=
  ks.map (fun k => m[k]?)

/-- Execute a finite sequence of existing standard-library insertion batches. -/
def applyBatches (m : Std.ExtHashMap α β)
    (batches : List (List (α × β))) : Std.ExtHashMap α β :=
  batches.foldl (fun state writes => state.insertMany writes) m

/-- A finite snapshot has exactly the footprint needed by the acquired method. -/
theorem snapshot_readsOnly (ks : List α) :
    ReadsOnly (fun k => k ∈ ks) (snapshot (β := β) ks) := by
  intro m n agree
  exact List.map_congr_left (fun k hk => agree k hk)

/-- Any number of batches avoiding the read keys preserves the whole snapshot. -/
theorem snapshot_applyBatches (ks : List α) (batches : List (List (α × β))) :
    ∀ (m : Std.ExtHashMap α β)
      (avoids : ∀ writes ∈ batches, ∀ k ∈ ks,
        (writes.map Prod.fst).contains k = false),
      snapshot ks (applyBatches m batches) = snapshot ks m := by
  induction batches with
  | nil =>
      intro m _
      rfl
  | cons writes rest ih =>
      intro m avoids
      have headAvoids : Avoids (fun k => k ∈ ks) writes := by
        intro k hk
        exact avoids writes List.mem_cons_self k hk
      have restAvoids : ∀ more ∈ rest, ∀ k ∈ ks,
          (more.map Prod.fst).contains k = false := by
        intro more hmore k hk
        exact avoids more (List.mem_cons_of_mem writes hmore) k hk
      calc
        snapshot ks (applyBatches m (writes :: rest)) =
            snapshot ks (applyBatches (m.insertMany writes) rest) := rfl
        _ = snapshot ks (m.insertMany writes) := ih (m.insertMany writes) restAvoids
        _ = snapshot ks m :=
          readsOnly_insertMany
            (R := fun k => k ∈ ks) (F := snapshot ks)
            (m := m) (writes := writes)
            (reads := snapshot_readsOnly ks) (avoids := headAvoids)

/-- An arbitrary snapshot predicate remains valid across footprint-safe batches. -/
theorem snapshot_predicate_applyBatches
    (ks : List α) (Q : List (Option β) → Prop)
    (m : Std.ExtHashMap α β) (batches : List (List (α × β)))
    (avoids : ∀ writes ∈ batches, ∀ k ∈ ks,
      (writes.map Prod.fst).contains k = false) :
    Q (snapshot ks (applyBatches m batches)) ↔ Q (snapshot ks m) := by
  rw [snapshot_applyBatches ks batches m avoids]

end DMKN.ReadFootprint.Consumer
