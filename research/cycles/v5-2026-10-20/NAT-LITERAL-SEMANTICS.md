# Natural-number literals: a bounded lowering seam, not a new arithmetic oracle

2026-10-20, core_growth. Source/theory only; no compiler, runtime, image or code run.
**GO in principle for bounded raw-Nat lowering with unchanged fresh checking.**
NO-GO for passing raw literals through relocated rows, rewriting arbitrary OfNat
instances, or claiming all native Nat computation survives relocation. Actual
admission of the exact source remains unrun; this is an implementation decision.

## Exact current foundation and native source meaning

`receipt-prepare-01/prepared/foundation.json` has SHA-256
`736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c`.
Its 22 declarations are Eq/refl/rec, PUnit/unit/rec, PProd/mk/rec, Eq.trans,
Eq.casesOn, HEq/refl/rec, Eq.ndrec, rfl, Eq.symm, Prod/mk/rec/fst/snd.
There is NO Nat, Nat.zero, Nat.succ, Nat.add, OfNat or instOfNatNat foundation
declaration. Arithmetic must have explicit local/imported semantic closure.
The selected receipt policy and relation both disable Nat/String extensions.

Pinned Lean `Expr.lean:424` specifies raw `lit(natVal 2)` as definitionally equal
to `Nat.succ (Nat.succ Nat.zero)`; `Expr.lean:741-750` and `Init/Prelude.lean`
specify ordinary `2 : Nat` via `OfNat.ofNat Nat (nat_lit 2)
(instOfNatNat (nat_lit 2))`. The instance's field is its argument, not an oracle.
`Nat.add` has the logical clauses `add a zero=a` and
`add a (succ b)=succ(add a b)` despite its native arithmetic optimization.
The exact discriminator is `fun n : Nat => Nat.add n 2`, of type `Nat -> Nat`.
Its imported vocabulary includes the actual OfNat/instance and addition closure;
replacing all overloaded numeral applications by constructors is NOT licensed.

## Exact transformation and what its argument establishes

Define L on raw source expressions: L(lit(natVal k))=succ^k zero using the
original exact `Nat.zero` and `Nat.succ`; all other supported expression forms
are mapped homomorphically. Leave OfNat applications, their instance arguments,
constant identities, universes and declaration metadata unchanged. Apply L to
every exported declaration type, body and recursor-rule expression, not only roots.
Reject strings and all other unsupported syntax as before.
For each finite k the pinned native meaning gives L(lit k) definitionally equal
to lit k. Congruence gives L(e) definitionally equal to e before relocation.
This is a source-to-core elaboration argument, not a fresh native execution claim.

Let rho be the existing exact local/external relocation. The canonical artifact
denotes rho(L(e)), NOT rho(e) with a residual native literal. Native literals have
built-in Nat type; relocated Nat is an ordinary inductive, so raw-literal reuse
would be a type/primitive mismatch. Source native definitional equality alone
does not establish that every optimized native conversion survives rho.
Therefore unchanged fresh checking of the COMPLETE rho(L(declaration closure))
is mandatory. A failed relocated type/proof check must refuse, never add an
axiom, enable a primitive flag or borrow native success. This bounds acceptance
to actual valid extensions; it does not guarantee total native-library support.
For the discriminator, exact OfNat projection and recursive addition definitions
yield the intended ordinary two-successor argument without any Nat primitive.

## Minimum semantic implementation conditions

1. Lower only the exact native `natVal` row tag and a valid nonnegative decimal
   value. Require its complete same-source group with `Nat : Type`, no parameters,
   indices or universe binders, and `zero : Nat`, `succ : Nat -> Nat` constructors.
   Check exact structured names and constructor membership; never infer Nat from
   a similar spelling, an unknown module, or the current foundation. Preserve all
   collected recursors and let the unchanged checker validate their actual rules.
2. Reuse existing reference mapping for those exact constructors. Current
   AuthorLean.native02 already calls dumpNatDeps and captures the complete group.
   Python lowering is sufficient in principle; no frontend rebuild is inherently
   required. Retain the raw export and source hash; expose the normalized mapping.
3. Establish structural original-to-L correspondence with one specified transform
   and focused positive/negative controls. Existing Rust correspondence binds
   canonical openings to REBUILT normalized rows, not original frontend exports.
   Its pass alone proves neither raw-source correspondence nor source execution.
4. Keep canonical syntax, foundation, semantic policy and receipt relation/image
   unchanged: only supported app/const forms reach full local descriptor/body checking.

## Expansion must be refused before allocation
A single lowered k has 2k+1 expression-tree nodes. The canonical validator also
visits k+1 references, giving 3k+2 visits, and maximum depth d+k+1 at a literal
occurrence originally rooted at depth d. Thus require d+k+1 <= 192 and remaining
work sufficient BEFORE constructing it. For exact constructor-byte lengths Z,S,
the subtree's canonical JSON size is Z+k*(S+9). Charge this and surrounding bytes
against the existing 16 MiB limit; retain 250,000-node and declaration limits.
Count expanded occurrences, not unique DAG indices: OfNat can mention k twice.
Budget the entire type/body/rule closure with existing per-stage limit semantics.
Reject overlarge decimal values by bounded length/lexicographic comparison before
integer conversion or unary expansion. No permissive limit increase is required.
For k=2 each occurrence adds five expression nodes, not a whole-closure cost bound.
Small literals do not bound computation: `Nat.pow 2 30` may expand enormously.
This partial importer covers bounded numeral-bearing types/definitions/proofs
over captured ordinary models, subject to fresh checking; unsupported proofs refuse.
An acquired module's Nat is NOT the later author's built-in Nat. Automatic numeral
notation/instance interoperability with that relocated type is not supplied here.
Select the narrow seam, not an LRAT port or new proof campaign.
Literal compatibility establishes neither profitable growth nor final-v5 release.
