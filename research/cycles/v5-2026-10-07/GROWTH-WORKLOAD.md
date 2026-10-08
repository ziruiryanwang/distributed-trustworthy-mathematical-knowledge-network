# V5 growth: warranted capabilities, not theorem counts

Root decision, 2026-10-07. This document selects a consequential workload and
comparison, not an assertion that v5 has passed. V4's payload result remains
unchanged. No global research agenda is imposed on participants.

## What grows

Fix a foundation/policy P, a local resource vector b and a finite evaluation
family Q. A capability is a typed method with explicit applicability premises,
an independently checkable correctness witness, and an operational way to use
it. Write Reach(K,b,q) when a specified agent with accessible library K can
produce a P-accepted solution to q within b. This is a relation on actual
methods/agents, not an oracle for optimal proof search or mathematical value.

The primary comparison is the attained set of q (and the corresponding
resource frontier), not the count of named theorems. Q and any weighting are
external evaluation choices, never acceptance rules. A parametric theorem can
increase reusable capability without changing the unrestricted deductive
closure of the foundation. That is the intended epistemic distinction:
derivable in principle does not imply available with a usable warrant at an
affordable cost. Nothing here consults human intention at the network boundary.

Exact-ID deduplication removes byte duplicates. Known certified transports can
identify equivalent representations for a particular comparison. Universal
semantic deduplication and a universal scalar ranking of mathematics are not
assumed computable. Usage observations are provisional signals for investment,
not proofs of novelty, truth or welfare.

## Selected method family: algebraic folds and fusion

Use a genuinely new, polymorphic finite expression inductive with leaf and
binary-node constructors. Its fold interprets leaves and nodes in an arbitrary
carrier. Publish the generic fusion theorem:

    h (fold leafA nodeA e) = fold leafB nodeB e

under the exact hypotheses h(leafA x)=leafB x and
h(nodeA x y)=nodeB (h x) (h y). Prove it once by structural induction.

Independently develop a mapped-expression law and a compositional transport
law; a downstream module combines them to remove a materialized mapped
intermediate while changing interpretation. Concrete uses include numeric
aggregation, leaf collection, and paired summaries. Each use must discharge
its premises. Merely renaming a theorem does not count as a new use.

This family is selected because it exercises new inductive declaration groups,
universe polymorphism, ordinary opaque theorem reuse, transparent definitions
needed by conversion, independently developed compatible branches, structural
discovery, and a useful algorithm transformation. It is not selected because a
deliberately weak proof tactic times out on it.

### Mathematical and operational arguments

Fusion follows by structural induction: apply the leaf hypothesis at a leaf;
at a binary node apply the node hypothesis followed by congruence of nodeB
using both induction hypotheses. Map/fold follows similarly. Composition of
transports follows by transitivity and application congruence. These arguments
can be kernel checked without benchmarking large trees.

In a specified strict evaluator, materializing map creates one new constructor
per input constructor before folding; the fused evaluator need not allocate
that intermediate. Both are linear traversals; this is not an exponential
speedup. Stack depth, leaf-value costs and retained input are counted. A good
local optimizer can already fuse: the optimized local baseline is allowed to
do exactly that, including use of an existing generic fusion theorem.

The method's algorithmic merit and the network's incremental merit are
different claims. The latter is primarily avoiding repeated independent
construction/certification of missing methods and amortizing distribution.

## Strong comparisons and an exact break-even theorem

Compare three routes with the same initial mathematics, representations,
verifier, caches, optimizer and application requests:

1. Independent optimized local development, caching each discovered generic
   method once per local library, not redoing it for every instance.
2. Ordinary decentralized distribution of named modules with locally checked
   proof packages, also cached once. This isolates sharing from succinctness.
3. The v5 certified-module/discovery route, including its actual service costs.

Existing baseline methods are free to reuse; do not withhold a method already
in the chosen initial library. A remote new method is not supplied for free to
the independent route. Do not infer a lower bound for the best possible agent
from one measured developer or tactic. State the selected algorithms explicitly.

For recipient i, let D_i be its cost of attaining the method locally under the
selected baseline (zero incremental discovery if already present); let R_i be
its search/acquire/authenticate/install/instantiate cost using the network.
Let F be all additional producer creation, generalization, certification,
publication and fixed service cost relative to the comparator. Let M include
replication, repair, retention, failed queries, failed proof attempts and
background service cost over a stated horizon. Count transfers/service CPU once
as physical resources, not twice as charges paid by two parties.

For explicitly stated nonnegative scalar resource prices w, network benefit
is exactly the condition

    sum_i w·(D_i - R_i) > w·(F + M).

This is accounting, not empirical evidence of positive demand. If each of N
distinct recipient libraries has avoided cost at least d, variable network
cost at most r+m, fixed cost at most f, and d>r+m, then any integer

    N > f / (d-r-m)

suffices. The proof is addition of the per-library bounds. If d<=r+m, this
model gives no positive-benefit guarantee. If a baseline shares an identical
producer cost, subtract it from both sides; never count it only against the
baseline. Without prices, report vector/Pareto comparisons rather than adding
CPU seconds, bytes and storage duration as if they shared units.

Bounds may be analytic, measured or forecast, but their provenance must remain
visible. A sensitivity region supported by bounds is a legitimate result;
invented demand or hypothetical timings are not measurements. Large-scale
replication is not required to prove this inequality, but service feasibility
and the constants still need implementation evidence.

## Falsifiable integration endpoint

A fresh client knows a formal pattern and policy, not the target content ID.
It queries replaceable indexes, gets candidate IDs plus explicit coverage,
acquires only selected certified interfaces and demanded semantics, checks a
new transport/application, and contributes the extension. A later fresh client
finds and uses that extension after the original producer/index is unavailable,
using retained replicas and an alternative index through public APIs.

Required observations include proof-ancestry bytes fetched (must be zero for
certified opaque theorem import), demanded semantic bytes, certificate work,
query/posting work and transfer bytes, cache state, provider work, local new
proof checking, and the support/retention horizon. Include failed searches and
a false applicability premise, an altered body, an incompatible merge and a
budget-exhausted query. Each outcome has a distinct explicit status.

The first Lean source below software/v5/workloads is a source-level derivation
and fixture seed. Compiling it alone will not qualify certified import, network
growth, discovery or public release. Split/export it through the new module
protocol once that relation exists; do not retrofit trusted imports as axioms.

## D08 continuation: selective certification and two different scales

The actual tiny workload has warm native module checks of roughly hundredths
of a second. It does not establish that a cryptographic receipt is faster than
an ordinary checked package. More recipients cannot fix a negative per-recipient
margin. The purpose of this workload at present is exercising substantive
method reuse and semantic boundaries, not demonstrating cryptographic speedup.

Two size variables must not be conflated: network corpus size G and the selected
dependency proof DAG size H. Discovery must avoid mandatory work in G; certified
imports must avoid mandatory proof replay in H. Neither eliminates the cost of
selected interfaces, conversion-required definitions, or returned query answers.
A small H in a large G needs economical search, not necessarily certification.
A large H with a tiny selected interface is the strongest case for certification.

### A sufficient receipt-benefit region, with the baseline explicit

Fix a module, an exact cache state and an ordinary DAG-sharing verifier that
checks its uncached proof package once per independent recipient installation.
Let C_i be its cost, V_i the receipt route cost (including exact statement,
interface and demanded semantics), F the additional certification cost and M_N
the additional service/retention/repair cost for N installations over horizon T.
Costs common to both routes cancel. A recipient already possessing an accepted
exact module is not another paid validation event. Let scalar prices w be fixed
in advance, or keep each resource as a separate coordinate.

If w·(C_i-V_i) >= delta > 0 and w·M_N <= m_0 + N m with m < delta, then

    N > (w·F + m_0) / (delta-m)

is sufficient for receipts to have lower total cost. This follows by summing
the N margins and subtracting the fixed and variable costs. Demand N and the
strictly positive margin are hypotheses, not conclusions of the protocol.

For a selected full-proof verifier that actually consumes L bytes of uncached
proof material over a bottleneck with sustainable throughput at most B bytes/s,
its transfer time is at least L/B. If the receipt route has a justified upper
bound v including all selected semantic transfers, L/B > v establishes a
positive transfer-time margin. This is a conditional property of that route and
resource model, NOT a lower bound against every possible compressed proof,
alternative derivation, preinstalled library or faster checker. Compare the
best supported ordinary representation, including shared subterms and caches.
CPU, peak memory and latency interference require separate bounds.

### Software consequence: mathematical identity is not proof packaging

Retain one immutable mathematical ModuleID across independently checked proof
witnesses and certificate encodings. Acceptance records additionally bind the
actual policy, checker/verification profile and receipt claim; an old cached
acceptance cannot silently survive a revoked verifier profile. A publisher may
offer an ordinary proof package, a genuine receipt, or both. A consumer chooses
a locally budgeted route. Ordinary checking must discharge its imports too;
declining certification is never permission to assume an unverified interface.
If that route exceeds its explicit ancestry budget, return an explicit demand
or resource refusal, not a trusted-import fallback. The required bounded-ancestry
certified route remains a release obligation, not replaced by ordinary checking.

Receipt production should be a selective investment. Quotes must name the exact
module, input/cache state, proof route, resource caps and service horizon. Usage
counts may inform the decision but cannot certify future demand, mathematical
truth, or independent users. No global usage ledger or compulsory research task
is required. For now this is an adopted architectural consequence, not an
implemented quote service or a positive empirical return claim.

### What the index repair can establish

The retained 18-export store has 67 feature keys and 362 postings; its 92,672
physical map-node records contain 16,641,140 encoded bytes. Physical database
size is 28,975,104 bytes. A fresh compressed representation preserving all exact
snapshot commitments can establish a service/storage improvement against this
same workload without a different mathematical corpus or weaker correctness.
It cannot by itself establish increased mathematical capability, cheaper proof
verification, or whole-network net growth. The 44.1875 CPU seconds previously
recorded include two index builds and operations; they are not a one-index
timing baseline. The two-feature summary's large wire encoding remains a
separate cost until an authenticated sparse encoding is implemented and tested.

## D10: composition without accumulating mandatory proof-replay cost

The central growth advantage of certified modules is not a larger theorem
counter. It is a possible separation between the depth of useful mathematical
reuse and the validation work imposed on the next participant. The following
conditional statement is a design obligation for the implemented route.

Fix one adopted checking/certificate profile. Let a new module use d selected
certified owner modules; let I be the total selected interface/opening bytes,
S the total semantics actually demanded by conversion/checking, and L its own
proof/checking work. These variables include all transitively demanded owners
and their interfaces/semantics, not just the declared immediate parents. Let
H be the total length of ancestral theorem-proof witnesses, which excludes
these selected types and computational bodies. Let V bound one verifier
invocation under the profile, including a refusal, and let n_v be the actual
number of such invocations (including failures and repeated checks). Thus d
need not equal n_v. Let A bound the entire selected acquisition workflow,
including its failed requests. Assume successful bounded acquisition; do not replace a missing body
with an axiom, an opaque object or an unchecked local assertion.

If the implementation (i) verifies each selected owner's resolved certificate,
(ii) authenticates every installed declaration/body against that owner's
commitment, (iii) checks every new local declaration, and (iv) never fetches
imported opaque theorem proofs, then receiving/using this contribution has
the structural bound

    T <= n_v V + T_open(I) + T_check(L, I, S) + A,

with no *mandatory* summand proportional to H. Proving the new certificate has
a separate cost P(L,I,S,d); it must not be hidden in the receiver bound.
Here opening and checking costs include all demand/restart passes, not only
the final successful pass. Reducing n_v to d requires an operation-local exact
receipt/profile acceptance cache and separate accounting for rejected receipts;
it is not implied merely by the presence of d distinct owners.
This is an operation-count decomposition, not a timing estimate or a claim
that T_check is linear. Type conversion and checking can be expensive even
without proof ancestry. In particular, S or d may themselves grow with a
problem's semantic dependencies, so the statement is not constant-time use of
arbitrary mathematics.

Justification: partition the actual work into certificate verification,
authenticated interface reads, demanded semantic reads, local checking and
acquisition. Each parent theorem proof has only one possible entry point—the
import route—which (iv) excludes. Rank-decreasing grounded module composition
and the adopted recursive-certificate soundness assumption justify imported
validity; hashing alone does not. Extending a chain or branching DAG with
additional *proof witnesses* while holding the selected interfaces/semantics
fixed introduces no operation in these classes. This concerns the selected
algorithm and representation, not an information-theoretic lower bound against
all possible competing proofs. Native conditional diagnostics do not discharge
(i); the forthcoming real guest/receiver must do so.

Consequently a sequence of N useful extensions need not impose the quadratic
sum of ancestor-proof replays on N fresh recipients. Under uniform bounded
d, n_v, I, S, L and A (including all restart work), receiver/use work is bounded by N times the displayed bound,
plus actual index/custody maintenance. If those bounds fail, charge their actual
growth. This contrasts only with a specified cold full-proof-checking route
that actually reads/checks each missing ancestor. It does not claim improvement
over an already accepted optimized local cache or pretend such a cache is cold.

### What would make this reciprocal *useful* growth

Two independent observations are required: a later contribution actually uses
an earlier reusable method, and the resulting method expands a specified
resource-bounded capability frontier or reduces costs at an existing frontier.
Dependency edges alone establish neither. The fold-map composition and paired
summary examples supply different warranted transformations; their algorithmic
cost improvements can be analyzed on symbolic input size without running huge
trees. The equally optimized comparator is allowed those transformations once
it has obtained them. The network's incremental advantage must still satisfy
the full-cost inequalities above.

This yields concrete instrumentation, not a universal usefulness score:
record exact method/interface identities, independently checkable applicability
obligations, the successful transformation/result, route/cache state and complete
costs. Usage frequencies may choose which expensive certificates or replicas to
fund. They do not decide mathematics, independent demand, future usefulness or
novelty. No human-intention field or compulsory task list enters the protocol.

### Current discriminator and next decision

Actual public compact-summary comparison now removes 96.64733% of the selected
summary's reply bytes (89,988 -> 3,017) with identical authenticated contents.
This improves one measured term of A. It does not establish a net growth result.
Next, provider offers remove pre-supplied snapshot IDs while sharing aggregate
workflow budgets. The exact new guest execution screen determines whether the
first module's P is operationally affordable before selecting real proving.
Do not infer a positive certification margin from metadata compression or from
the very cheap native checks of this small workload.
