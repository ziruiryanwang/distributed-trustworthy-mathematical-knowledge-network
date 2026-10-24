module

public import Init

/- Small owner-approved original-library fixture. Compilation alone is not
   commons admission. The selected native workflow must discover its actual
   complete unit closure and private/public representations. -/

public section

namespace DMKNBaselineFixture

inductive Flag where
  | low
  | high

/-- Expose actual computation through the complete generated Flag group. -/
@[expose] def flip (x : Flag) : Flag :=
  Flag.rec (motive := fun _ => Flag) Flag.high Flag.low x

private theorem hidden_low : flip Flag.low = Flag.high := rfl

/-- Its private proof requires hidden_low; its statement does not. -/
@[simp] theorem flip_low : flip Flag.low = Flag.high := hidden_low

scoped notation "lowF" => Flag.low

end DMKNBaselineFixture
