# Concrete computational capability: finite-semigroup powered evaluation

2026-10-06. Root-selected theory and source-only successor under
`experiments/finite-semigroup-01`. No native, guest, prover, network or test
execution is selected by this note. The unchanged F43 guest and compact execute
profile are sufficient in principle; root selects an actual bounded run only
after source review. Used predecessors remain frozen.

## Decision and exact useful endpoint

Implement a bounded untrusted proof-producing finite-semigroup evaluator.
Inputs are an owner-supplied associative d-by-d multiplication table,2<=d<=8,
a starting element a<d, and0<=r<=64. It computes the product of2^r copies of a
by r squaring steps and emits a proof of the **exact normalized value**, using
the genuinely acquired squaring law. The output is not another symbolic rewrite
law and does not leave associativity as an unproved hypothesis.

The utility supports any table in this finite envelope; it is not hardcoded
parity, a projection operation or opaque function composition. The fixed C3
table provides the smallest nontrivial discriminator:

| mul | 0 | 1 | 2 |
|---|---:|---:|---:|
| 0 | 0 | 1 | 2 |
| 1 | 1 | 2 | 0 |
| 2 | 2 | 0 | 1 |

At a=1,r=30 its value is1; at r=31 it is2. The table is cyclic addition modulo3
on its represented elements. This simple family has a better specialized parity
algorithm; the comparison is explicitly with the named naive repeated-product
implementation, never an optimal independent algorithm. Other accepted tables
use exactly the same utility and correctness construction.

## No new finite type or arithmetic library

Define q_d(n)=min(n,d-1) by a finite Nat.rec decision ladder. Use the total
operation on Nat

`op(x,y) = table[q_d(x)][q_d(y)]`.

Every result is one of0,...,d-1; q_d fixes those values. For arbitrary natural
x,y,z, let i=q_d(x),j=q_d(y),k=q_d(z). Then

`op(op(x,y),z) = table[table[i][j]][k]`,

`op(x,op(y,z)) = table[i][table[j][k]]`.

Consequently a finite associative table supplies an associative total Nat
operation. The represented subset is closed; the surrounding Nat semigroup
need not have a global identity. Unlike a modulo computation over huge inputs,
this clamp/table encoding needs only bounded decision depth. Inputs and all
computed intermediate values in the selected workload are canonical tags<d.

The formal operation is one safe closed transparent definition using only
Nat,Nat.zero,Nat.succ,Nat.rec,lambda/Pi/application constructors. The existing
compiler with zero imported definitions can assign its canonical DefinitionID.
It does not require Fin, new inductives, Nat.add/mod/pow, typeclasses, function
extensionality, tactics or a new image. The generator must independently rebuild
and canonically compare the expected table body with the supplied operation
capsule, so a compilation record alone cannot assert table correspondence.

## Finite associativity proof, not trusted table metadata

Check every d^3 integer table equation before proof construction as a useful
early refusal, but do not treat that host check as proof. Build a closed proof
term of `forall x y z:Nat, op(op x y)z = op x(op y z)`.

For a dependent property P(n), a d-way case eliminator has branches P(0),...,
P(d-2), and `forall t, P(succ^(d-1)t)`. It is a ladder of dependent Nat.rec
terms ignoring induction hypotheses. Apply that construction to x, then y,
then z. In each of the at most512leaves both sides reduce by the actual table
definition to the same Nat constructor numeral; emit Eq.refl at that numeral.
The tail branch represents every n>=d-1, not just the number d-1. No exhaustivity
assumption, unproved subtype law or host-generated axiom is used.

The final unchanged guest checks this complete finite proof and the operation
definition. A deliberately nonassociative table should fail the utility's early
table gate; a forged association term or wrong claimed value must still be
rejected by the actual guest, not accepted from an integer table status.

## Proof-producing evaluation without reducing the huge baseline

Let Q(x)=op(x,x),y_0=a,y_(j+1)=table[y_j][y_j]. The host performs exactly r
table reads. It emits proofs

`E_j : Iter Q j a = y_j`.

Base E_0 is Eq.refl a. Given E_j:

1. `congrArg Q E_j` proves `Q(Iter Q j a)=Q(y_j)`.
2. The actual bounded table computation gives `Q(y_j)=y_(j+1)` by Eq.refl
   and definitional equality.
3. Eq.trans composes them; the one-step Iter equation identifies the left side
   with `Iter Q (succ j) a`.

The utility retains proof DAG sharing and never beta-normalizes or numerically
evaluates the giant reference iteration. Explicit endpoint annotations and
the recursive proof chain let the checker compare matching symbolic terms,
using at most one Iter unfolding at each link. No claim that the whole current
checker has a proven linear runtime follows; its actual reduction/memoization
behavior is a changed-boundary risk to inspect and test once.

Instantiate the genuinely acquired generic squaring law at Nat,op,the actual
association proof,a,m=0,n=r. If the returned compiled T2 law is available, use
that exact law and its compiled D2 body; otherwise root must explicitly select
the already acquired original law. Compose its right side with E_r via Eq.trans.
The exact final target is

`Iter (fun x => op x a)`
`  (Iter (fun k => Plus k (Nat.succ k)) (Plus 0 r) 0) a = y_r`.

Its right side is a literal normalized canonical tag. The left side denotes
2^r factors but has O(r)unary-input syntax; no enormous numeral is materialized.
The proof must actually contain the acquired-law application. Compiling a result
or trusting the host's y_r is insufficient. The untrusted evaluator can be wrong;
actual acceptance still requires a correct exact equation.

T2 uses Plus,Iter,D2. Adding op gives at most4definitions in the complete
selected context. The output type itself needs Plus,Iter,op; D2 is proof-only.
The original-law fallback uses only3. Definition IDs, contexts and acquired
fragment bytes must remain exact; no extra opaque data constant is introduced.

## Cost and size model before execution

The named direct evaluator performs2^r-1 table multiplications. The utility
performs r squarings, plus at most d^3 associativity-table comparisons and
constructs an explicit proof chain of r links. At d=3,r=30 this is30table
multiplications rather than1,073,741,823. The definition/proof construction and
all receiving/service costs remain additional work, not zero.

Operation syntax is O(d^2)decision nodes with bounded numerals. A conservative
nonshared association proof bound is O(d^4)small constructor/decision work from
d^3leaves with depthO(d); normal DAG sharing reduces repeated fragments but is
not needed for the finite bound. Unary j repeated in the annotated evaluation
chain permits an O(r^2)nonshared construction bound; sharing can reduce it.
The generator will hard-cap nodes, serialization, traversal and wall/CPU, and
report actual counts rather than infer4MiB compatibility from big-O. d=8,r=64
are input maxima, not a guarantee every case fits the guest envelope.

For fixed d<=8, the symbolic construction/checking candidate has no2^r-sized
data term. Whether guest conversion accidentally unfolds the reference side
must be challenged before claiming efficient final checking. The sole proposed
actual C3 gate should preserve the symbolic left expression and supply full
guest rows/segments, resources, exact target and returned value.

For an all-in overhead bound K(r) at the selected r, baseline per-operation lower cost l>0 and
complete squaring-step upper cost u, the proven sufficient full-cost condition
is `l(2^r-1)>K(r)+ur`, with all other resource caps also met. Here an actual
software endpoint will provide y_r with a checked equation, not merely an
unimplemented evaluator premise. K(r) still includes generator/compiler/checker,
initial production if not common, acquisition, setup, agent planning, service,
custody and failures. See [operating region](NET-BENEFIT-OPERATING-REGION.md)
for explicit sensitivity; do not fabricate unknown cost constants.

## Selected source scope and next discriminants

Author fresh pure utility, narrow pinned CLI and focused native-free contracts
under `experiments/finite-semigroup-01`. Stage1 emits exact table operation plan;
the frozen compiler emits its actual capsule; stage2 compares that exact body,
then emits the expected normalized proposition and explicit application proof.
No process/network/checker invocation belongs in the utility. Root's existing
compact public apply/check/offer path remains the execution and trust boundary.

Tests should cover table validation, d/r/seed caps, all finite association cases,
nonassociative early refusal, exact known C3 values, a different associative
table, tail case coverage, graph closure/binder discipline, proof-chain counts,
wrong-value candidate construction for genuine guest refusal, and exact
operation-body binding. The final mathematical gate is not replaced by any
mocked proof test. Proposed actual values30/31 are decisions for root; do not
run either merely because they appear in this source-only document.

This utility directly closes the missing warranted-method-to-normalized-value
bridge in a bounded nontrivial family. It does not solve arbitrary algorithms,
broader foundation/library coverage, best-known baseline selection or universal
net growth. Its relevance is a reusable software route that can turn acquired
mathematical knowledge into independently checkable concrete computations,
with a theoretically justified cost transformation and explicit limits.
