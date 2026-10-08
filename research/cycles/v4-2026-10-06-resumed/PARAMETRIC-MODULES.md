# Parametric modules: what can actually be factored

2026-10-06, independent source/theory reviewer. Canonical root only. This is a
design argument, not an executed compiler or a newly qualified language feature.
Root owns selection and adoption; the mechanism author's separate
PARAMETRIC-COMPILER-DESIGN.md owns its implementation decision. Existing passed
sources and campaigns remain frozen. The full v4 goal is not accepted.

## Decision in one paragraph

Prefer mathematics stated over explicit typed operations and laws when it is
genuinely independent of their implementations. A checked universally quantified
theorem then serves many independently chosen instances; its certified proof
need not be downloaded by consumers. This uses the existing Pi/lambda/application
language and unchanged certificate relation. It is not a generic procedure that
turns every specialized proof into a theorem about arbitrary implementations.
Nor does it make the current concrete-definition representation modular: when
a consumer requests definitional computation on a concrete implementation, its
required body still has to be supplied and checked in the selected profile.

## The obstruction that an automatic abstraction must respect

Let the adopted environment be F and let D be the transparent declaration
`D : Type := Nat`. In F,D, the term `0` has type D by delta conversion. Replacing
D by an unconstrained variable A produces `0 : A`, which is generally ill-typed.
Similarly, a proof using `f x = x` by reducing an identity implementation does
not become a proof of that statement for an arbitrary function f.

Consequently the tempting metatheorem

`F,D |- e : T  implies  F |- fun (d : type(D)) => e[D:=d] : forall d, T[D:=d]`

is false without an additional abstraction-stability premise. Syntactic closure,
an acyclic definition graph, or a valid original certificate does not supply that
premise. Keeping an equality `d = implementation` can repair certain statements,
but imports that implementation into the interface and can erase the hoped-for
size saving. Extra laws and transports are mathematical content to prove, not
metadata that a compiler can assert on its own authority.

## A sound, useful conditional construction

Work in dependent type theory under exactly the adopted F. Use a well-formed
finite telescope

`Delta = (x1 : A1), (x2 : A2[x1]), ..., (xk : Ak[x1,...,x(k-1)])`.

Suppose actual checking establishes `F;Delta |- e : T` with all universes and
local variables explicit. This is the essential premise. Iterated lambda and
Pi introduction gives

`F |- M := lambda x1 ... xk, e : Pi x1 ... xk, T`.

For a well-typed dependent substitution sigma satisfying, in order,
`F;Gamma |- ai : Ai[a1/x1,...,a(i-1)/x(i-1)]`, repeated application gives

`F;Gamma |- M a1 ... ak : T[sigma]`.

This is ordinary introduction/elimination plus substitution. It adds no axiom
and depends on no author's identity or intention. A proof module is the same
construction with e a proof and T a proposition. Laws may be earlier binders,
e.g. `(op : A -> A -> A)` followed by `(assoc : forall x y z, ...)`.
Their instances must themselves be checked, or supplied as authenticated
theorem premises; mere names or popularity are never sufficient.

There are two honest authoring interfaces:

- Author an explicitly parametric module and check it as such. This is the
  simplest route and avoids guessing which implementation facts were used.
- Propose a lift of a specialized source as an untrusted candidate, then check
  the full lifted term under abstract parameters. Rejection is an ordinary
  outcome. A successful original specialized check is not lifted authority.

If the implementation promises guaranteed abstraction rather than proposal,
its input contract must establish the abstract-context typing premise (for
example by restricting the source to already-parametric terms). We currently
have no proof of a general automatic lifting implementation.

## Exact syntax obligations for a proposed lifting compiler

Use stable declaration identities, not suggestive names, to select what is
being abstracted. Compute the finite dependency closure of the selected parameter
types, and order it as a telescope. The input may refer to earlier binders only.
A cycle, unknown constant, unsupported declaration kind or exceeded bound must
refuse rather than silently replace a dependency by an axiom.

For a fixed telescope of k parameters, number xi by i in 1..k. In a body nested
under d original local binders, the occurrence of xi is de Bruijn index
`d + k - i`. Old locally bound indices less than d stay unchanged. If translating
an open term, old external indices at least d must be shifted by k; alternatively
require a closed original root and prove this branch unreachable. In the type
Ai, only the preceding i-1 parameters exist, so xj becomes `d + i - 1 - j`.
Binder type/value and binder body do not have the same depth: the depth increases
only in the body of lambda/Pi/let. A let value is checked at the outer depth.

Memoization keys must include every context dimension affecting translation:
source graph/node, effective parameter telescope or its stable identity,
specialized universe substitution, and relevant local binder depth. Reusing the
old definition compiler's context-free expression memo is unsound for a new
bvar-changing transform without a separate argument that its mapping is invariant.
Hash-consing occurs after the fully translated expression has been computed.

Names in declaration-name positions cannot generally be replaced by expressions.
In particular a projection's typeName is not a variable slot. The existing
definition compiler correctly rejects nonfoundation projection substitution;
a lifting compiler must preserve that refusal or implement and check an actual
elimination translation. It must not reinterpret a name hash as a term.

### Universes are not implicit higher-rank term parameters

A Lean declaration may be universe-polymorphic, but a local term variable is
not an arbitrary universe-polymorphic declaration. A parameter x:T[u] represents
one level instance; it cannot be silently reused as a parameter at T[v] when
u and v differ. A finite candidate can introduce a separate parameter for each
selected `(declaration identity, simultaneous level substitution)` pair. Its
type dependencies are likewise specialized. Distinct instances may coincide
after a checked substitution; this does not justify merging them beforehand.

Universe parameters of the final module must include every free level parameter
needed by the resulting type and value, with collision-free renaming. Substitute
level expressions simultaneously, not repeatedly into one another. Respect all
constraints of the actual capsule codec and checker; lifting cannot broaden the
fixed foundation or make unsupported inductive packages admissible. Bound the
number of distinct specializations, dependency nodes, telescope depth, output
bytes and traversal work. Finite DAG input does not imply a small specialization
closure when many different universe instantiations occur.

## What this could save, and what it cannot

Let P be the DAG bytes of a genuinely implementation-independent module and
its type; let Ii be the explicit type/law/interface bytes needed for instance i;
let Bi be the concrete implementation bodies demanded by that use. Distinguish
three routes rather than comparing against an artificially duplicated baseline.

1. Independent monolithic storage can cost roughly sum_i(P_i + Ii + Bi), with
   separately checked proof construction. The P_i need not be literally identical.
2. Content-addressed storage of identical subgraphs already shares identical
   bytes. The current inlining compiler also hash-conses its output DAG. A new
   factoring feature cannot claim savings already supplied by this route.
3. A certified parametric theorem can cost one shared module/certificate plus
   sum_i(Ii + arguments_i + bounded application_i), provided consumers ask only
   for the abstract theorem's instances and all needed interfaces fit the profile.
   Bi can disappear from the proof-ancestry cost, but NOT from computations or
   explicit output interfaces that themselves demand these bodies.

In particular, a reusable theorem about any associative operation can be shared
across independently defined operations using checked associativity witnesses.
The theorem's own proof is replaced by its exact certified interface. Checking
the operation's actual definition/law and doing an instance-specific evaluation
remain costs. If each new consumer already has the same verified local theorem,
the network has no new mathematical checking advantage merely by serving it again.

For a monomorphic chain `D(i+1) := fun x => Di (Di x)`, the current compiler's
hash-consing can already give O(n) distinct expression nodes for Dn. Therefore
exponential textual expansion is not a valid description of that implementation.
Separately stored fully flattened historical capsules can nevertheless total
O(n^2) bytes; transport, inter-object sharing and constant-size module interfaces
are different problems. Do not claim a new source-DAG wrapper solves them.

Let V_i be each consumer's actual certificate verification, S sealing/certification,
A authoring/adoption, R service/discovery/acquisition, C_i residual instance
checking, and L_i the strong
same-algorithm local alternative. A workload has positive net resource benefit
only under a declared weighting/resource envelope when

`A + S + R + sum_i(V_i + C_i) < sum_i(L_i)`.

Independent consumers do not share a sender's verification authority. Legitimate
exact local/invocation reuse may reduce a particular V_i, but global once-only
verification is not assumed. Charge argument/interface bytes and all demanded
conversion in C_i. This is an
operating-region inequality, not a measured universal speedup. No general upper
bound linear in transmitted DAG bytes is available for dependent conversion.
Beta/delta reduction can expose expensive computation; resource limits can
refuse a valid term. Native execution changes a constant factor/implementation
path, not the logical cost of an arbitrarily expensive conversion.

## How the proof and semantic boundaries interact

A certified theorem may cut off its proof ancestry because the receipt
authenticates the adopted checking relation and exact interface. A proof module's
type must still be available, well-formed and matched to its actual arguments.
Current F-closed transparent definitions are semantic bodies, not opaque theorem
assumptions. Their bodies cannot be erased just because an earlier actor checked
them: future delta conversion might need them. A genuinely abstract interface
works because the theorem is proved without that delta knowledge, not because
the system pretends a transparent definition became opaque.

Unsealed returned application fragments retain their bounded proof suffix above
certified frontiers. Further uses can accumulate that suffix until a size/cycle
limit refuses. Parametric authoring and native checking do not eliminate the need
for owner-funded certified cuts. The existing full sealer is the operational
candidate for those cuts; see FULL-SEALER-PATH.md. No automatic seal funding or
subsidy follows from the mathematical factoring theorem.

## Consequence for search and growth

The abstract module creates reusable capability rather than merely another
syntactic theorem. However, more generic types also produce broader wildcard
search streams. Indexing only the outer Eq/forall head is insufficient at huge
scale; typed operation/law structure can supply selective necessary-condition
features, while incomplete budgeted search remains explicit. One cannot claim
constant discovery cost just because the module is small.

This proposal is independent of human intention: all accepted statements and
instances are judged under F. A local agent decides which module to construct or
instantiate. A usage heuristic may estimate expected downstream amortization,
but cannot establish the typing premise, certify the laws, or prove net growth.

## Selection recommendation

Do not change the guest/image solely to rediscover Pi/lambda/application, and do
not ship an alleged general abstraction theorem with the false delta premise.
First make the existing parameterized authoring/application route explicit to
agents. Implement a bounded proposal compiler only if it removes an observed
authoring obstacle that is not already solved by explicit plans. Its decisive
controls would include the D:=Nat counterexample, dependent binder shifts,
multiple universe instances, projection-name refusal and unchanged final checking.
A new compiler would be ergonomics plus checked proposals, not a new authority.
Broad kernel-visible dependent named definitions and foundation extension remain
separate central semantic work, not closed by this note.
