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

/-- Expose ordinary executable computation; preserve generated matcher support. -/
@[expose] def flip (x : Flag) : Flag :=
  match x with
  | .low => .high
  | .high => .low

private theorem hidden_low : flip Flag.low = Flag.high := rfl

/-- Its private proof requires hidden_low; its statement does not. -/
@[simp] theorem flip_low : flip Flag.low = Flag.high := hidden_low

scoped notation "lowF" => Flag.low

end DMKNBaselineFixture
