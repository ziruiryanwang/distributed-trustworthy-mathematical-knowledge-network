# Independent decision: bounded natural-literal lowering

2026-10-20, core_release. Source/theory review only; no execution, imports,
builds, proofs or Git actions. Read SEMANTICS `5a4d9a19`, SOURCE-SEAM `f01196de`,
selected `modules/source_rows.py` `60c7255d`, codec and selected source finish path.
**GO for one bounded SourceRows successor plus focused controls.** No frontend,
canonical schema, mathematical checker, receipt image, policy or foundation change.
This is a partial source importer, not unrestricted arithmetic interoperability.

## Why this is the smallest defensible seam

The selected native02 frontend already exports `natVal` and dumps Nat dependencies.
The current Python decoder is the actual missing boundary. The exact adopted
foundation has no Nat. Lower raw native literals homomorphically to the captured
original `Nat.zero`/`Nat.succ` group, then retain existing relocation and fresh
checking. Do not rewrite OfNat instances, primitive arithmetic calls or policies.
Original literal definitional equality justifies L in the original environment;
it does not establish preservation of every native conversion after relocation.
Only full unchanged checking of rho(L(closure)) admits the resulting module.

## Required guards; these are implementation conditions, not new mechanisms

1. Accept only the exact singleton `natVal` expression tag with canonical decimal
   text. Bound decimal length/value before integer conversion or unary allocation.
   Reject strings, signs, leading zeros and all other unsupported literal forms.
2. Require exact structured local names Nat, Nat.zero, Nat.succ, not name suffixes,
   foundation promotion, external aliases or another module's nominally similar Nat.
   Check one inductive type, no universe/parameter/index/nested parameters, exact
   Nat : Type0 and ordered zero : Nat / succ : Nat -> Nat constructor shapes.
   Require constructor indices/owners, 0/1 fields and original safe group metadata.
3. Preserve the COMPLETE group, including its original Nat.rec declaration and
   both constructor rules. Check expected recursor name/owner/census and metadata;
   retain the existing derived-recursor mathematical check for exact type/RHS rules.
   A nonempty recursor list or constructor census alone is insufficient. Never
   synthesize or trim a recursor to make closure pass. Hostile replacement group,
   missing recursor/rule and malformed derived rules need explicit controls.
4. Run these semantic preconditions when actually lowering a literal, not eagerly
   in SourceRows.__init__: source finish first constructs a census-only reader with
   empty local/foundation sets. Preserve this existing nonconverting use.
5. Every type, body and recursor RHS must use the same lowering branch. Retain the
   raw export and source binding. The later Rust rebuilt-row correspondence checks
   normalized rows, not original frontend rows; do not describe it as the latter.

## Allocation accounting must be prospective

At expression depth d, succ^k zero has 2k+1 expression nodes, k+1 references,
3k+2 canonical visits and deepest canonical reference depth d+k+1. SourceRows
already calls _visit(d) before tag dispatch: reserve remaining cost exactly once
before allocation, including a conservative reference charge where appropriate.
Its existing const path does not itself charge reference visits. Distinguish this
source-work counter from unchanged later codec validator scopes; neither proves
the other's complete aggregate bound automatically.

Count each EXPANDED OCCURRENCE, not each raw DAG index. Repeated references to one
literal can otherwise multiply allocations. Enforce closure-wide work and an
explicit conservative output-byte budget including enclosing structure/metadata,
not just each numeral. For exact compact zero/succ byte lengths Z,S, the numeral
subtree size is Z+k*(S+9). codec.canonical serializes before its byte-limit check;
it is not by itself an allocation preflight. Preserve existing limits and final
group/spec/body validation. No post-hoc oversized allocation or limit increase.

## Minimal decisive controls and native follow-through

One finite native-free contract run should cover exact 0/1/2 structure, repeated
DAG occurrence charging, leading/negative/huge decimal refusals before expansion,
depth/node/byte boundaries, exact local Nat identity and complete group refusals,
census-only compatibility and unchanged unsupported syntax. Exercise actual decode,
not a separately reimplemented lowering oracle; use a small exact expected tree.

Only after source review and these contracts, select one separately bounded actual
native smoke for `fun n : Nat => Nat.add n 2`, keeping its source/export/normalized
rows and unchanged full check. Do not expand it into a proof or performance campaign.
A semantic/checker refusal is a real result, not permission to enable Nat primitives.
Small literal bounds do not bound recursive conversion (e.g. exponentiation);
existing finite checker containment stays mandatory.

## Scope of the decision

Acquired relocated Nat is not a later author's builtin Nat; automatic numeral
instances or bridges are not supplied. A successful small native smoke would
establish a concrete interoperability improvement only, not growth, all-Lean
coverage, cryptographic readiness or completed v5. The next action is the one
small successor, not another broad theory or source survey.
