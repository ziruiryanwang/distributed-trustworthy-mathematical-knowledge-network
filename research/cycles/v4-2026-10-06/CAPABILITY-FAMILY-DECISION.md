# Concrete capability family: associative repeated squaring

2026-10-06 UTC. `/root/growth_mechanism_v4`. **THEORY AND SOURCE ONLY.**
No Lean/native/guest/build/test/proof execution or product source change.
Root subsequently selected one ordinary endpoint source for independent review,
not a runtime campaign. Canonical root is the sole project root.

## Decision

Repeated squaring is suitable for the current profile. In fact it needs **only
the two already qualified F-closed Iter/Plus definitions**, with no new definition
capture, guest change, monoid typeclass, arithmetic library or user inductive.
Use the actually received first fragment `V4Growth.iterated_factor_map` to prove
a generic two-block semigroup algorithm equivalence. The new work proves the
associative power-combination lemma, rather than merely renaming that parent.

The intended software consequence is a portable checked law that permits local
agents to replace a specified exponentially long repeated-multiplication program
with a short squaring program. The operation-count comparison can be proved now;
a timing campaign cannot strengthen that exact count. Actual acceptance and
fragment exchange/reuse still require one bounded implementation-conformance
check. This is not an assertion that the present checker/evaluator is already
exponentially faster, or that every competing solver needs the baseline's work.

Source endpoint:
`experiments/capability-family-01/OwnerPower.lean`, 1913 bytes, SHA-256
`a0adf676faefed1d6e11be409fffa2acd2f77d3a3854116217fdb24e3408eb30`.
Its exact support/qualification contract is `ENDPOINT.md` in that directory.

## Grounding in the actual supported language

The fixed F43 registry and complete witness inventory were inspected. They
contain Nat/Nat.zero/Nat.succ/Nat.rec, Eq/Eq.refl/Eq.rec, Eq.trans and congrArg.
The exact inventory is
`research/cycles/v4-2026-10-02/CANONICAL-FOUNDATION-WITNESS-AVAILABILITY.md`.
No Nat.add, Nat.pow, OfNat, List, Bool, Semigroup/Monoid structure, function
extensionality theorem, tactics or unregistered algebraic library is assumed.

The existing definitions have these exact operational equations:

```text
I(f, 0, x)       = x
I(f, succ r, x)  = f(I(f, r, x))
P(0, n)         = n
P(succ r, n)    = succ(P(r, n))
```

`I` is the already captured polymorphic Iter definition, ID
`6104f4124046ad98d6702b4d5cf3e0152b0bd2383093f21fcf7b098d970def06`.
`P` is Plus, ID
`35ee27f0591a4973b368590b8ee6176ae338849b37fc5337f8991e80d4da1498`.
Each body independently refers only to F. These are not newly hypothesized
definitions. Plus recurses on its **first** argument; the proof orientation
below deliberately uses this equation and avoids unregistered arithmetic lemmas.

The incoming fragment's exact output interface is
`d7d3d3d481f2e48abd2367d5137443a9348b4cfc1f64c14e9ea4d68d5fecf5c7`.
Its existing F-closed semantic context already includes I and P. A received copy
is selected by exact manifest and interface; its advertised execution status is
not a proof. Final composed guest checking and genuine certified frontier
verification remain required.

## Formal statement

Let A be any Sort, `mul : A -> A -> A`, and assume only associativity:

\[
\forall x,y,z\in A,\quad (x\mathbin{\star}y)\mathbin{\star}z
=x\mathbin{\star}(y\mathbin{\star}z).
\]

Fix `a : A`. Define the following **local mathematical abbreviations**, not
additional exported definitions:

\[
R_a(x)=x\star a,\qquad Q(x)=x\star x,\qquad
D(k)=P(k,\operatorname{succ}k),
\]

\[
L_a(k)=I(R_a,k,a),\qquad M(r)=I(D,r,0).
\]

For all symbolic `m n : Nat`, prove the exact equality

\[
L_a\bigl(M(P(m,n))\bigr)
=I\bigl(Q,m,I(Q,n,a)\bigr). \tag{SQ}
\]

No identity element, commutativity, cancellation, nonzero assumption or finite
representation is needed for this semantic theorem. `a` supplies the first
factor, so an empty-product convention is unnecessary. For m=n=0 both sides
are a. The two-block form is not padding: it matches the actual parent law,
permits incremental squaring, and exposes exactly which already received
mathematics is being reused.

## Complete proof argument

First prove by induction on l, uniformly in k:

\[
L_a(P(l,\operatorname{succ}k))=L_a(k)\star L_a(l). \tag{JOIN}
\]

Base l=0: the left is `L_a(succ k)`, hence `L_a(k) star a`.
The right is the same because `L_a(0)=a`.

Inductive step from l to succ l: unfolding only the known successor equations,

\[
\begin{aligned}
L_a(P(\operatorname{succ}l,\operatorname{succ}k))
&=L_a(P(l,\operatorname{succ}k))\star a\\
&=(L_a(k)\star L_a(l))\star a\\
&=L_a(k)\star(L_a(l)\star a)\\
&=L_a(k)\star L_a(\operatorname{succ}l).
\end{aligned}
\]

The second equality is congruence on the induction hypothesis; the third is
the supplied associativity law. No assumption that arbitrary factors commute
appears. The orientation `P(l,succ k)` is essential to the short source proof.
Setting l=k in JOIN gives `L_a(D(k)) = Q(L_a(k))`.

Now instantiate the actual incoming factor-map theorem as follows:

| Parent parameter | Instantiation |
|---|---|
| alpha, beta, gamma | Nat, A, A |
| f, g, t | D, Q, Q |
| h, k | L_a, identity on A |
| hf | JOIN(k,k), proving `L_a(D(k)) = Q(L_a(k))` |
| kg | Reflexivity, since identity commutes with Q |
| m, n, x | The same symbolic m,n and Nat.zero |

Its conclusion is SQ after beta reduction and `L_a(0)=a`. The authored source
contains exactly one local Nat.rec induction and one actual application of the
received factor-map theorem. The induction introduces no exported auxiliary
theorem, unproved axiom, new semantic definition or dependency cycle.

This is a checked-law design, not proof-source concealment or an agent-efficiency
trial. The source author knows the parent statement and deliberately uses it.
No independent-discovery or unassisted proof-search advantage is claimed.

## Exact algorithm and cost comparison

Specify the two compared algorithms, including evaluation strategy.

`LEFT-POWER(m,n,a)` computes r=m+n and c=M(r), starts y=a, then performs
`y := mul(y,a)` exactly c times. Its result is SQ's left side. This is the named
left-associated baseline, not a lower bound on all methods for the problem.

`SQUARE-BLOCKS(m,n,a)` starts y=a, performs `y := mul(y,y)` n times, then the
same update m times. Each already computed y is passed twice by value/reference;
it is **not recomputed recursively** for the two operands. Its result is SQ's
right side. Streaming the two blocks avoids constructing the large c.

Let r=m+n as ordinary mathematical arithmetic. Plus's defining induction gives
P(m,n)=m+n. Then

\[
M(0)=0,\qquad M(r+1)=2M(r)+1,
\]

so induction yields `M(r)=2^r-1`. Counting calls to the supplied multiplication
operation, rather than guessing CPU from expression size:

\[
\operatorname{Mult}_{\rm LEFT}(m,n)=2^{m+n}-1,
\qquad
\operatorname{Mult}_{\rm SQUARE}(m,n)=m+n. \tag{COUNT}
\]

At r=0 both counts are zero; at r=1 they coincide; for r>=2 the saving is
`2^r-1-r > 0`, with ratio `(2^r-1)/r`. Computing the baseline's explicit counter
adds work and never subtracts its specified multiplication calls. COUNT is exact
for these algorithms even if A's elements have variable size; it is not yet a
statement about bit operations, memory, CPU, serialization or proof-checking.

If an adopted local implementation represents each A value in fixed bounded
storage, multiplication has uniformly bounded positive cost, assignments are
bounded-cost, and Nat iteration has the declared ordinary per-step cost, then
the named implementations take respectively Theta(2^r) and Theta(r) work. One
way to satisfy the data-size assumption is a **fixed** finite semigroup with a
fixed-size representation, such as fixed-dimension matrices over a fixed finite
field; implementing/certifying that concrete instance is not part of this source
task. If dimension/modulus grows, charge its actual multiplication and storage
costs. For exact unbounded integer powers, output size alone may grow
exponentially; claiming Theta(r) bit complexity would be false.

The count argument uses call-by-value/shared intermediate values. Replacing y
by an unevaluated duplicated expression can reintroduce an exponential tree.
Kernel definitional reduction, a compiler and a local agent's evaluator are
different algorithms; the present guest is not assumed to implement this cost
model merely because it checks the equality theorem. The generic proof is
symbolic in m,n and need not evaluate the reference power for concrete large
inputs, but actual checker behavior remains a separate implementation question.

## Why this is capability growth, and what is not proved

The resource-bounded interpretation treats a verified algorithm plus its law as
reusable capability. A fixed axiomatic theory already entails SQ; storing a
proof does not enlarge its deductive closure. It can make a justified method
available within resources to independent later agents who did not reconstruct
that law. That is the relevant epistemic/operational growth, not extra truth
created by a transport protocol or the number of theorem wrappers.

In the multiplication-only model, suppose a future agent has b available
multiplication calls after adoption overhead. For the one-parameter subfamily
n=0, `LEFT-POWER` fits r only up to floor(log2(b+1)), while `SQUARE-BLOCKS` fits r
up to b. The largest nominal product length in this powers-of-two subfamily is
respectively `2^floor(log2(b+1))` (at most b+1) versus `2^b`.
This is an exponential expansion in the **reachable specified exponent**. It
does not mean exponentially many independent facts, distinct outputs, theorem
objects, or agents. In a finite semigroup many outputs repeat and periodicity
can enable an even better algorithm. A projection operation can make the
problem trivial. Neither case invalidates COUNT's named-algorithm comparison;
both invalidate universal optimality or novelty conclusions.

Let K be the total one-time producing, checking, transporting and acquiring cost
of this reusable law, and H_i all incremental adoption/search/checking overhead
for a use i. In a comparable cost model, cumulative advantage over the named
baseline requires

\[
\sum_i\bigl(C_{\rm LEFT}(r_i)-C_{\rm SQUARE}(r_i)\bigr)
>K+\sum_i H_i.
\]

This conditional statement includes failures, parent acquisition and semantic
data costs. It does not invent values for K or H_i. The present source/cost
derivation proves neither demand frequency nor network-wide net benefit.
Agents choose independently whether the law is useful; popularity can inform
local retention but cannot make an unproved associativity premise acceptable.

## Assumption and implementation checks that matter

- Associativity is necessary. On Nat, `mul(x,y)=succ x` is not associative;
  at a=0 and m=n=1, squaring gives 2 but three baseline calls give 3. The theorem
  therefore genuinely depends on a proved premise rather than mere syntax.
- A higher-order law hypothesis is part of the mathematical statement, not an
  extra trusted axiom. A concrete downstream application must discharge it or
  retain it visibly as a hypothesis. The transfer system must not silently
  present the conditional theorem as unconditional computation.
- Only two existing DefinitionIDs are needed. Use the actual incoming capsule's
  semantic closure; do not capture aliases/new versions or silently admit
  new global constants. A law-bearing typeclass would add avoidable machinery.
- The new root is a genuinely different generic algebraic law, not a wrapper
  around F. Its local JOIN proof converts an algebraic law into the iteration
  simulation premise; the final application uses F's quantitative composition.
- A direct proof without F also exists: prove JOIN, then induct on the counter
  iteration and on the split. Thus this is not a minimal-proof lower bound or
  a claim that the commons is logically indispensable.
- No new full certificate campaign is needed to check this source-family seam.
  The bounded fragment composer can inline the acquired F proof and retain its
  genuine certified frontier, followed by the actual unchanged guest check.

## Smallest root-selected next consequence

After independent source/theory review, root may select one finite ordinary
source preparation using **C's acquired exact first fragment**, output mode
fragment, and existing semantic data. The gate is actual native export plus
real final composed-guest acceptance of SQ under the unchanged foundation,
with no new axioms/definitions, exact output interface and retained costs.
It must not substitute the producer's original directory for C's received input.

Then one fresh recipient can acquire that new result and check or use it if
needed for the release loop. Reuse existing exact evidence rather than paying
for duplicate OwnerNext or unrelated exponent timing runs. The operation-count
proof above is already the relevant theoretical justification; an implementation
test validates the theorem/transport boundary, not COUNT by sampling inputs.

No global utility oracle, compulsory task list, human-intention test, new guest,
general agent planner or consensus ledger follows. The theoretical comparison
and the actual qualified artifact must be reported separately until both exist.
