set_option autoImplicit false
namespace OwnerV5
def addTwo := fun n : Nat => Nat.add n 2
theorem addTwo_spec : forall n : Nat, addTwo n = Nat.succ (Nat.succ n) := fun n => rfl
end OwnerV5
