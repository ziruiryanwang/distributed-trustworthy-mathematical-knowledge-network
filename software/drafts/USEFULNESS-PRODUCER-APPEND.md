# Candidate: right-fold preservation of append

Source: `UsefulnessProducerAppend.lean`. Submission root: `Reduction_append`.
Status: independently authored source candidate; not executed, qualified,
accepted, submitted, or published by this author. Root's fresh bounded run is
required before any such claim.

For arbitrary `A : Type u`, binary `op`, and `e`, assume
`Eq (op (op a b) c) (op a (op b c))` and `Eq (op e a) a` for all elements.
With `F` equal to the exact admitted vocabulary definition applied to
`A`, `op`, and `e`, the sole theorem proves
`Eq (F (List.append xs ys)) (op (F xs) (F ys))` for all lists `xs`, `ys`.
A right-unit assumption is unnecessary.

The proof is `List.rec` on `xs`, keeping `ys` fixed. For the empty list,
the target reduces to `Eq (F ys) (op e (F ys))`, the symmetry of the
left-unit hypothesis. For a cons, congruence under `fun t => op a t`
transports the induction hypothesis; symmetry of associativity then changes
`op a (op (F zs) (F ys))` into `op (op a (F zs)) (F ys)`.
The fold and append constructor equations are used by definitional reduction.

## Dependencies and source profile

The only external mathematical definition is
`DTMKN.d.«84011102582061903d4b0e3bb04e9ac15e179d35e6e4ae0b358285c91d29c5426b6c590f318a»`,
with universe arity 1, read from the vocabulary submission's public description.
Its independently supplied source is a right fold, using `List.rec` with base
`e` and step `fun a _ acc => op a acc`.

Explicit foundation constants used by this source are `List`, `List.append`,
`List.rec`, `Eq`, `Eq.symm`, `Eq.trans`, and `congrArg`; all were found by name
in the installed seed inventory. The source has no imports, tactics, infix
equality, new definitions, axioms, `sorry`, unsafe terms, or new inductives.
The `let F` is local to the proof and abbreviates the exact receiving name.

Unverified source-profile points are acceptance of the ordinary `theorem`
declaration and local `let` syntax in this reconstructed environment, the
elaborator's inference of implicit/universe arguments to the seeded constants,
and reduction through the admitted fold and seeded `List.append` during
elaboration and canonical replay. The mathematical proof relies only on the
stated hypotheses and constructor equations. No product or Lean process was
run, and no benchmark consumer or historical theorem was inspected.

## Exact source identity

The source is 1,067 bytes, measured read-only after authoring.
SHA-256: `457a31d4ff4125c1697a43b666b5b07b898059233577cfc6919887df5a5bf1cc`.
This digest identifies the candidate file, not a checked canonical object.
