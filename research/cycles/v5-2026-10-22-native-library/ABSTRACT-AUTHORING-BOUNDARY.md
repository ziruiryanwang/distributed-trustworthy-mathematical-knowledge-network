# A possible stronger authoring abstraction, not a new acceptance mode

2026-10-23. Root source/theory note prompted by the actual hidden `Nat.gcd`
definition refusal. No implementation or runtime is selected by this note.

## Separate two questions

1. What meaning has the independent receiver accepted?
2. How much of that meaning must a local authoring environment expose to build
   a new proof that the receiver can check?

These need not have identical answers. A public Lean import may deliberately
hide an implementation body. Requiring it for an unrelated definition is simply
overbroad; the immediate selected fix is dependency-closed basis projection.
Even a *relevant* hidden body may be unnecessary when the consumer uses only
its specified laws and never reduces that definition.

## Conditional interpretation argument

Let K be the actual accepted receiver environment. Let A be an authoring
environment for a selected finite interface. Give each selected constant an
exact identity-preserving interpretation into K. Require:

- Every declared interface type is preserved under that interpretation,
  including universe parameters and dependency identities.
- Every reduction/computation rule available in A is valid in K. Keep actual
  constructor/recursor rules and kernel-primitive semantics within this condition.
- A retained concrete definition has its exact accepted semantics. In contrast,
  an abstract handle has a type but **no additional reduction rule**.
- An abstract handle is interpreted by an already warranted declaration of
  that exact type in K, not an arbitrary claimed inhabitant or a name match.

Then the usual derivation-interpretation induction gives:

    if A derives t : T, K derives interpret(t) : interpret(T),

subject to the precise Lean calculus/primitive rules and the premises above.
The constant case uses the accepted declaration in K. The conversion case uses
preservation of A's available reductions. Erasing a definition body does not
introduce a new conversion. It loses some proof-construction power, rather than
automatically creating an unsound inference.

Thus, in principle, the existing warranted-theorem-handle idea could extend to
an **already existing axiom-shaped public handle for an accepted definition**.
This would be an abstract authoring view of a concrete warranted object, not a
new permitted foundation axiom. It would not justify replacing a conflicting
concrete definition based merely on equal types. Missing reductions would still
require acquiring actual semantics, or a different proof using accepted laws.

## Scope and decision

This is a conditional mathematical argument, not a mechanized Lean refinement
proof. Native primitive reduction, opaque values, dependent projections and
generated groups require explicit treatment before implementing a broader mode.
The final actual receiver check remains mandatory even with a justified
construction abstraction: local elaboration is never the acceptance authority.

Do not silently weaken the current exact-definition rule. First execute the
already selected semantic basis projection, which changes no matching rule.
If a *needed* public definition is hidden, assess this abstraction against a
small exact-semantics acquisition instead of reflexively importing the whole
private library or restarting a certificate campaign. A justified authoring
abstraction could reduce repeated interface work and improve ordinary usability;
it is worth investigating only at that concrete integration boundary.
