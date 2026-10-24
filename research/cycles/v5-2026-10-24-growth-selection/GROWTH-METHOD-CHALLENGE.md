# Challenge: reusable mathematical methods, without an LP detour

2026-10-24. Independent bounded theory review by `growth_method_challenge`.
Read canonical AGENTS/GOAL/current NOW and the complete GROWTH-DESIGN-REVISION.
No code, dependency survey, download, build, experiment, state or Git mutation.

## Verdict

**The two-parameter LP proposition and its nondegenerate example are correct.**
They justify a real reusable mathematical interface, not demonstrated productivity
or a reason to build an LP-specific commons. The general architecture consequence
is worthwhile but largely confirms the native-first decision: exchange usable
ordinary methods with their definitions and exact applicability theorems, rather
than treating every new instance as an unrelated answer/certificate.

Finish the selected file-backend source review. Do not automatically fund its
compatibility/build work. That callback offers exact-response ingestion; it is
not needed merely to express or publish the proved parametric method, and it
does not itself realize parametric reuse.

## Mathematical checks

Write B for the selected row indices and A_B for the square row matrix. Under
`A_B M = I` and `M A_B = I`, for any proposed (b,c) put

    x = M b_B,       u = M^T c.

If `A x <= b` and `u >= 0`, then `A_B^T u = c`. Every feasible z obeys

    c^T z = u^T A_B z <= u^T b_B
          = u^T A_B x = c^T x.

The inequality uses componentwise order and nonnegative u. The penultimate
equality uses A_B M = I; stationarity uses M A_B = I. Feasibility of x is a
separate premise. No full-rank assumption on all of A, primal boundedness theorem,
strict positivity, uniqueness or solver correctness is missing. The constructed
feasible optimizer itself establishes attainment on this region. Its outside
region has no promised outcome.

The displayed inverse M for `A_B=[[1,1],[2,1]]` gives I in both product orders.
Its primal residual conditions and objective cone are exactly

    b_3-b_1+b_2 >= 0,       b_4-b_2+2*b_1 >= 0,
    c_1-c_2 >= 0,           2*c_2-c_1 >= 0.

At `b=(3,4,0,0), c=(3,2)` their margins are 1, 2, 1, 1.
Every coordinate perturbation of magnitude less than 1/4 preserves strictness:
the four possible margin decreases are bounded respectively by 3/4, 1, 1/2,
3/4. Thus this is a genuinely full-dimensional neighborhood in the six parameters
(or its rational points), not only one ray or finitely many repeated answers.
The solution is `(1,2)` at the center and can change with b.

This is ordinary parametric linear-programming structure. The small example is
easy for conventional methods and must not be used to imply solver speedup.

The dense arithmetic counts are right for `m >= n >= 1`. For dimensions including
zero, use `O(n^2 + mn + m + n + 1)` per application: testing feasibility with no
variables can still inspect m bounds. Each inverse-product check takes O(n^3)
field operations for positive n. These remain arithmetic-operation counts, not
bit complexity or bounds for Lean elaboration, conversion or kernel checking.
The coordinate/denominator lengths and exact retained theorem identity matter.

## Why the method shape is not itself a growth criterion

The type

    forall x, Domain x -> Correct x (run x)

is expressive, but expressiveness is not useful growth. Set `Domain x := False`
to obtain vacuous applicability, or set the domain equal to the desired result
and use the hypothesis. Even a very large nonempty region can be irrelevant to
later local investigations. Neither theorem shape nor region volume certifies
value. Do not make this shape a compulsory special object or a protocol-level
importance test.

What is substantively stronger than an answer cache is an available supported
application procedure: after adopting the method, the consumer can obtain actual
new outcomes from actual new parameters, with its residual obligations checked
and its full acquisition/application costs accounted for. The LP theorem gives
a constructive procedure and explicit applicability predicate. It does not
establish that such parameters will occur, that basis lookup is cheap, or that
ordinary warm-start/cached solvers cannot do the same work more cheaply.

Composition in the root note is valid in the stated jointly compatible checked
environment. It transports correctness only. A bridge may be as hard as the
original problem; computing intermediate values may dominate costs; the composed
conjunction may not be the consumer's required conclusion. Those are real costs
and additional theorem obligations, not failures of the composition proof.

## Highest-payoff software consequence

Make **method acquisition and application**, not answer replay, the supported
growth-bearing contract of the ordinary-library path. This is an API/workflow
selection, not a new mathematical acceptance rule. A supported path should let
an independently chosen consumer:

1. Acquire a named method and its actual required definitions/data under a
   compatible foundation/version policy.
2. Establish the concrete domain premises and obtain the exact local conclusion.
3. Retain the method for another input without requiring the original producer.
4. Return a genuine proved adaptation, stronger domain lemma or mathematical
   consequence through the ordinary contribution path when it has one.

Existing ordinary Lean modules and selected-target export may already provide
all four. If so, the right implementation is to expose and document that path,
not create a new method schema, LP region service or generic solver RPC. Source
selection must identify a particular missing boundary before new code is funded.
This note did not audit those APIs and does not declare that integration complete.

**Concrete falsifier:** a changing-input use of the retained method still requires
the supplier's live solver, replay of its exact original answer, hidden state edits,
or fresh integration of its entire executable environment. Then the alleged
method interface is actually an answer/service dependency, and that specific
boundary must be repaired or its capability claim withdrawn. A second, economic
falsifier is that supported premise discharge/adoption costs erase the expected
benefit against the same ordinary reusable library; then keep the sound method
as optional mathematics, not as the product's growth justification.

Do not choose LP simply because its proof is available. Its role is currently a
well-founded domain illustration. The next actual supported application should
be chosen by compatibility, real reuse structure and marginal implementation
cost; no external recruit or expensive growth experiment is required to make
that source-level choice.

## Whole-commons boundary

For selected fixed data and warranted methods, correctness and application need
not inspect unrelated worldwide results. This is a locality property, not a
guarantee that semantic search finds the right method cheaply. Exponentially many
bases, overlapping applicability regions, incompatible representations, unavailable
custody and skewed demand can defeat discovery or economics. Keep finite optional
discovery and locally selected retention; do not enumerate the global family.

The adopted checker/method foundation still costs something. Neither this LP
construction nor exact-response replay resolves arbitrary cold ancestry-free
verification. General cold acceptance, sustainable decentralized service and
public deployment remain separate full-v5 obligations. This review passes the
theoretical method direction, not those release gates, actual uptake or inevitable
exponential mathematical progress.
