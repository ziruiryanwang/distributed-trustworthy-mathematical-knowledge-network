# Growth by reusable evidence interfaces

2026-10-24. Root synthesis, independently reviewed as recorded below. This changes
the candidate architecture, not the mathematical acceptance policy. No new product
code, solver service, installation, migration or experiment is selected here.
Final deployable v5 remains active and unfinished.

## Decision and its practical meaning

Keep the ordinary Lean library commons. Add a **candidate consumer-native evidence
route**: for suitable families, a supplier sends an inert mathematical witness,
and the receiver constructs a proof using a small, already warranted local
verification method. The supplier need not export its solver, tactic environment,
research history, or a cryptographic proof of its computation.

This is not another name for the expensive succinct-certificate campaign. A dual
vector, an algebraic identity, or a finite combinatorial witness can justify a
result directly. We should use such mathematical structure where it exists before
paying to prove every step of an arbitrary computation. Ordinary proof-producing
tools already do this; integration should reuse them rather than invent a solver.

The preceding pre-export investigation is closed. Existing Loogle clients are
adequate starting points; a new plural-provider HTTP client is deferred. Improving
transport before knowing what useful knowledge should cross it has lower current
payoff than deciding the evidence and reuse boundary.

## Philosophical commitment, without a universal importance score

Under a fixed foundation, another derivable theorem need not enlarge ideal
deductive closure. The relevant change is what finite agents can warrant, find,
understand through formal interfaces, and use within their resource opportunities.
The previous PHILOSOPHY-OF-GROWTH already establishes this distinction.

In particular, a finite object can describe a useful infinite family. A parametric
method or a proved solution region can give a consumer a procedure for answering
many later questions. Counting its instances as separate insights is misleading;
discarding it as merely an eliminable definition is equally misleading.

Validity is independent of intention. Usefulness and investment are local and
context-dependent. The protocol need not decide whether a theorem is important,
new to humanity, or relevant to a human. Agents may pursue new questions precisely
because earlier knowledge makes them affordable. Hence a fixed benchmark can
measure one productivity claim, but cannot exhaust all capability growth.

This does not justify a new global novelty metric, task list or popularity ledger.
Existing local usage and cost observations can guide selection without authorizing
proofs or becoming a promise of inevitable scientific progress.

## The exact assurance boundary

Let K be a receiver's warranted environment containing a specific verifier V
and a proved theorem:

    sound : forall x w, V(x,w) = true -> R(x).

Here x can encode a matrix or a formal statement; R(x) may itself quantify over
infinitely many mathematical objects. The remote party supplies only w. The
receiver must establish a real checked proof of V(x,w)=true and apply sound.

The accepted judgment then depends on K, x and w, not on how w was discovered.
This is the elementary soundness construction in GROWTH-CONSTRUCTIVE-MODEL,
not a new cryptographic theorem. A binary returning true, a solver status, or a
printed `Verified` value is not a substitute for the checked judgment. Parsing,
normalization and problem-to-local-statement correspondence are part of the
boundary. A proof of a normalized problem does not automatically prove a different
raw problem. Approved native execution must not tamper with K or the validator.

The cost excludes mandatory replay of the producer's *search history*. It still
includes adopting V/sound, parsing and binding x/w, exact evaluation or explicit
proof reconstruction, checking, storage and failures. Generic cold theorem imports
still face their ancestry problem. This specialized route does not waive that
unresolved v5 requirement or reinterpret a trusted base as a fresh proof.

There is a useful distinction within this limitation: a consumer can be **cold
with respect to every previously generated domain answer** while already having
the fixed checker/soundness library. It can validate a new domain witness without
any earlier answer's proof history. The one-time library adoption remains paid
and explicit; it is independent of how many answers the network later generates.
This is stronger than requiring each consumer to cache every previous answer,
but narrower than cheaply adopting arbitrary newly invented verification methods.

## A constructive reusable-knowledge example: regions, not just answers

Consider an exact linear optimization family over rationals (or an ordered field
with an explicitly checked embedding). Fix A with m rows and n columns and c with
n entries. The problem at parameter b is to maximize c^T z subject to A z <= b;
variables are unrestricted. Lower bounds can be represented as additional rows.
Do not conflate this convention with a solver's minimization/bound convention.

Choose n indexed rows B. Let A_B be their matrix, b_B their right-hand side, and
suppose a finite certificate contains M and u satisfying

    A_B M = I,      u >= 0,      A_B^T u = c.

Define the proposed optimizer and its explicitly described applicability region:

    x(b) = M b_B,      Omega = { b : A x(b) <= b }.

**Parametric certificate theorem.** For every b in Omega, x(b) is feasible and
maximizes c^T z over all feasible z.

**Proof.** Membership in Omega gives feasibility. For any feasible z, selecting
rows gives A_B z <= b_B. Since u >= 0,

    c^T z = u^T A_B z <= u^T b_B
          = u^T A_B M b_B = c^T x(b).

Every equality or inequality uses a displayed checked premise. No assertion about
how the solver found B, M or u occurs. This is ordinary linear-programming duality
and basis reasoning, not newly discovered optimization mathematics. It works for
singular A overall; the selected certificate must satisfy its exact conditions.
Outside Omega no optimality conclusion follows. Omega may be irrelevant to future
work, and a library of regions may have expensive overlap and discovery costs.

The transferable object is now more than one solved numerical instance: it is a
proved affine solution procedure on an explicit parameter region. A later agent
can use it while changing b, or prove that a whole parameter set lies in Omega.
That latter containment is new mathematical work, not a free extrapolation.
The old basis/region can be retained by other holders after the solver disappears.

The finite algebraic checks for a proposed certificate and a selected b are
constructive. The following dense operation counts assume 1 <= n <= m.
A dense implementation checks A_B M=I once using O(n^3) arithmetic
operations, checks the dual relation in O(n^2), then uses O(n^2+mn) operations
per b for x(b), feasibility and objective data. These are operation counts for
specified algorithms, not constant-time arithmetic or measured Lean costs.
Rational numerator/denominator lengths and exact normalization must be charged;
there is no bound on kernel time from the number of matrix entries alone.

This gives a nonvacuous *capability* construction without inventing a difficult
benchmark. It does not prove a speedup over a good LP solver: ordinary sensitivity
analysis, warm starts, basis caching, and the same shared certificate are all
permitted in the comparator. It justifies a reusable mathematical interface and
identifies the cost questions an implementation actually needs to answer.

## Place in the whole architecture

| Responsibility | Candidate design and boundary |
|---|---|
| Local research | Ordinary approved Lean packages, independent objectives and existing automation. Requests to a selected solver are optional; no network agenda. |
| Mathematical acceptance | Existing exact receiver policy. General proof bundles, already warranted local reuse, and supported domain witnesses are separate evidence routes, never provider votes. |
| Discovery | Existing formal/library indexes give advisory candidates. Domain/interface keys can narrow a chosen family; neither they nor an LP region solve global semantic search. |
| Acquisition and custody | Immutable selected packages/proofs or instance/witness bytes through replaceable holders. Retention is selective; no node needs all global knowledge. |
| Reuse and contribution | Use the resulting actual Lean theorem locally; offer useful general methods, reduction lemmas, regions or supported outputs through ordinary publication. |
| Economic policy | Compare local solving, ordinary package reuse, witness acquisition and optional expensive certification. Charge all participants and failed branches. |

Do not invent a generic witness RPC service, registry, region-search engine or new
acceptance format at this stage. The mathematical tuple is a design boundary,
not an adopted wire schema. Existing storage/transport can carry inert bytes;
existing exact theorem records must retain their existing identity meaning.

A remote solver alone is not a knowledge commons. Persisting a response can make
that answer independently reusable, but does not preserve the unavailable solver's
ability to answer new questions. Retaining general methods/verified checkers and
reusable regions addresses a different, larger capability. Neither replaces
ordinary theorem-library sharing for mathematics outside these families.

For a fixed supported evidence interface, checking a selected input/witness need
not depend on the number of unrelated results or solvers worldwide. That is a
useful locality guarantee. It is not a cheap global-discovery theorem: finding a
relevant region among many overlapping regions, or recognizing an equivalent
problem written differently, may itself be hard. Exact family/instance keys can
help only when their semantics are actually shared. Keep bounded incomplete
discovery and explicit checked reductions; do not introduce a global region
catalogue on the strength of the algebraic theorem.

## What justifies shipping, and what does not

The product need not defeat the best imaginable Git+Lean stack: that stack may
include this very tool. It must provide a maintained, usable reciprocal workflow
at acceptable cost and assurance. Three evidence levels remain separate:

- A theoretical construction can establish valid composition, a useful supported
  procedure, and an explicit conditional cost region. It need not recruit a user.
- Integration evidence must establish that the actual supported program supplies
  those exact statements, data bindings, refusal behavior and independent reuse.
- Broad uptake, prevalence of savings and sustained research acceleration require
  observations. They cannot be inferred from the first two levels.

Outsourcing one solve generally relocates cost instead of reducing aggregate work.
Payoff can come from avoiding repeated integration of a complex solver, sharing
already produced evidence, or reusing a parametric result. All such claims retain
checker adoption, provider effort, searching, negative cases and maintenance.
No universal exponential-growth claim, solver lower bound, or zero-cost checker
is needed or established. The independent challenge supplies falsifiers.

## Source evidence and next decision

The opportunity investigation identifies existing Lean LP verifier/proof-building
packages, not a missing mathematical invention. Root independently inspected the
pinned LPVerify README, full Driver and the Sound theorem interfaces. The driver
binds its proof to the validated/normalized Problem; its `#eval` display is not
itself our retained kernel proof. The package/toolchain compatibility and exact
export to the current receiver have not been tested. Do not install or port it
merely to make a demonstration, nor equate a solver success with admission.

Before another runtime, the highest-value discriminator is a source-level answer:
can an existing producer-independent proof constructor accept inert multipliers
and yield an ordinary checked theorem under the supported local base, without
solver execution or new trust axioms? If yes, select only that missing data/proof
boundary. If the maintained tool already exposes it adequately, use it. If no,
compare the cost of the narrow adapter with deferring this optional route.

The new candidate does not erase earlier usable software. It removes the proposed
universal obligation to transport a producer's method history for every useful
answer. No new package or final-v5 completion is claimed by a mathematical model.

## Review and current allocation

Root read/adopts the complete independent GROWTH-CLAIMS-CHALLENGE verdict:
the parametric proof needs no missing left-inverse assumption, its cost statements
are appropriately scoped, and the release evidence levels preserve the full
reciprocal/assurance obligations. This is source/theory approval, not a passing
implementation. The zero parameter lies in the displayed Omega, establishing
nonemptiness but not any practical demand or substantial region coverage.

The opportunity author's finite follow-up resolves the decisive seam. Root read
its full appended analysis and independently inspected the pinned Registry entry
and complete RatCertificate module. An existing public static-backend callback
can return evidence instead of solving; the tactic retains local parsing and
explicit proof construction. A direct multiplier assembler also exists but uses
internal row/parser APIs. Neither requires a native solver. Existing JSON Contract
code supplies a decoder, whereas its Backend is subprocess-based, not a bounded
retained-file input command.

**Next implementation choice, in principle:** a small approved offline-file
backend using the existing public callback/decoder, not a new arithmetic checker.
Before implementation, bind the exact source dependencies/toolchain and finite
input/call/resource contract. Preserve the actual local request, select the
backend explicitly, refuse unsupported additional requests, and prohibit solver
fallback. Produce the ordinary finished theorem through the existing tactic and
require actual kernel/axiom-policy checking; do not preserve only a native status.
Immutable file evidence permits replay without an online generating service.

The old 4.33.1 dependency pin versus installed 4.34.0 is unresolved integration
work, not permission to switch global toolchains or reinterpret accepted state.
No new LP checker, remote service, package port, toolchain installation or test
campaign is selected by this source conclusion. A separate narrow implementation
contract is the next action, not another literature or transport survey. The
parametric-region theorem is the justification for preserving reusable structure;
the file backend does not automatically discover or generalize such regions.

### Later bounded source selection

Root now selects only the small source implementation governed by
`software/v5/ordinary_witness_backend/CONTRACT.md`: an explicitly registered,
bounded, immutable-file callback reusing the existing request/response codec and
proof-producing tactic. growth_constructive_model owns the new source/README and
dependency manifest; preexport_tools independently reviews the contract/source.
No solver/checker fork, dependency installation, build, runtime, performance
experiment or existing-state change is selected. Stop on an API or safety mismatch
instead of expanding into a new framework. This selection supersedes the earlier
source-investigation-only allocation, not any mathematical or release gate.

## Growth-first follow-through: a reusable domain, not an exact-answer cache

The small offline callback is a possible ingestion boundary, not the growth
mechanism. Its finite exact request map deliberately refuses a changed request.
Finishing that source does not select a build, a solver service, or further
backend engineering. The more consequential question is which retained object
lets a future agent do genuinely different work without repeating discovery.

For the LP example, the previous fixed-objective construction can be strengthened
to allow both bounds and objective to change. This is established parametric LP
reasoning, not a claim of new optimization theory. It exposes an implementation
distinction that the single-instance adapter does not address.

### A two-parameter reusable mathematical interface

Fix a rational m-by-n matrix A and n selected rows B. Let A_B denote that
square submatrix. Retain M and checked identities

    A_B M = I,       M A_B = I.

Over a field either inverse identity implies the other for square matrices, but
including both keeps the displayed construction explicit and avoids hiding an
unimplemented linear-algebra lemma. The earlier fixed-c proof did not need this
additional identity and remains correct as stated.

Define the primal and dual applicability regions

    P_B = {b : A M b_B <= b},
    D_B = {c : M^T c >= 0}.

**Reusable-basis proposition.** For every (b,c) in P_B times D_B, the procedure
`x = M b_B` returns an optimizer of `max c^T z` subject to `Az <= b`.

**Proof.** Put u = M^T c. Then u is nonnegative and
`A_B^T u = (M A_B)^T c = c`. For every feasible z,

    c^T z = u^T A_B z <= u^T b_B
          = u^T A_B M b_B = c^T M b_B.

The last vector is feasible by membership in P_B. Thus the existing fixed-c
argument applies uniformly to every pair in the displayed product region.
Outside the region this procedure makes no optimality promise. No finite set
of example executions substitutes for either inverse identity or the region
premises.

The region need not be a singleton or a set of aliases. For example, take

    A = [[1,1], [2,1], [-1,0], [0,-1]],
    B = [row 1, row 2],    M = [[-1,1], [2,-1]].

Both inverse products are I. The proposed solution is
`(b_2-b_1, 2*b_1-b_2)`, and the remaining primal conditions are
`b_1-b_2 <= b_3` and `b_2-2*b_1 <= b_4`.
The objective cone is `c_2 <= c_1 <= 2*c_2`. At
`b=(3,4,0,0)` and `c=(3,2)` all these nontrivial inequalities are strict.
Consequently a neighborhood of that point lies in the region (or its rational
points when working over Q); both optimizer and objective can vary. This verifies
nondegenerate applicability, not an advantage over an ordinary solver: the
small example is easily solved directly and must not become a speed benchmark.

### What is actually accumulated, and what can be composed

The useful retained object is a **proved partial solution procedure with an
explicit domain**, not an unqualified answer service. A general form is

    method : forall x, Domain x -> Correct x (run x).

Domain membership must be warranted at each application, either computationally
or by a local proof; it is not merely an advisory rank or a supplier assertion.
A local agent may establish a larger family of domain memberships, transport
the method to another representation, improve its implementation with a proved
refinement, or derive a new mathematical consequence. Those are possible
substantive returned contributions. Producing them is new work, not automatic
growth credited to every download.

For composition, if one warranted procedure provides R(x,f(x)) on D(x), a second
provides S(y,g(y)) on E(y), and a checked bridge proves `D(x) -> E(f(x))`, then
on D(x) the composed procedure provides
`R(x,f(x)) and S(f(x),g(f(x)))`. Proof is two applications and conjunction
introduction, with all functions and interpretations in one compatible checked
environment. It establishes composition, not a useful final property without
the corresponding checked consequence, nor a free bridge or cost improvement.
This instantiates the already adopted method/bridge argument; no new global
task graph, semantic novelty oracle or special method language is required.

In the concrete LP case, a receiver can warrant the inverse identities and
generic method once, then check the selected region premises and specialize the
theorem. For 1 <= n <= m, straightforward dense numeric work is O(n^3) for each inverse-product
check and O(n^2+mn) per application. Final Lean construction/checking, rational
bit growth, matrix acquisition and initial theorem adoption remain separate paid
costs. A backend that reconstructs a new full proof for each exact JSON response
does not automatically realize this amortization.

### Whole-cost and very-large-network consequences

The software should carry this object as an ordinary named theorem plus required
definitions/data. The current native-package and selected-target paths are the
first candidates; do not invent a region wire protocol or LP-specific acceptance
rule. A receiver chooses what to retain. The generating solver can disappear
without invalidating retained proved procedures and their data.

Do not enumerate all bases: there can be exponentially many. Select only locally
encountered or explicitly requested useful objects; offer them optionally through
replaceable providers. Formal family/shape hints can narrow discovery but do not
prove applicability. Bounded incomplete discovery may miss a suitable method;
region membership and the final local theorem remain the acceptance boundary.
Neither local region checks nor correctness requires scanning the worldwide
result set. Discovery success, custody and capacity still require their stated
separate assumptions. This does not solve arbitrary cold theorem ancestry.

Charge the extra generalization, inverse/data production, warrant/adoption,
publication, maintenance, failed discovery and failed applicability work. An
ordinary library/solver may reuse the same basis, warm start and cache; it gets
equal credit. The supported gain is conditional: reusing the retained procedure
must cost less than the best allowed available alternative for the relevant
history. No new lower bound for optimal LP solving follows. The absolute benefit
is an explicit sound reusable capability; comparative savings and prevalence
must not be inferred merely from a large parameter region.

**Next selection rule:** close the source adapter review, then resolve the
ordinary-package representation of this method/domain/application/return seam
before spending on dependency compatibility. If existing APIs already supply it,
use them. If they do not, identify that exact missing seam. Do not expand the
offline backend just because it is the next available engineering task. A real
parametric use, not another exact-response replay, must justify any later LP
integration investment. This section is theoretical design; it does not claim
that the current software emits the region theorem.

### Adopted independent challenge and actual decision

Root read/adopts GROWTH-METHOD-CHALLENGE.md in full. It independently validates
the two-parameter proof and gives an explicit open neighborhood for the example.
Its arithmetic-count correction is incorporated above: those counts require
positive dimensions. More importantly, a method type can have a vacuous or
unaffordable domain. Neither its syntax nor its region volume is a usefulness
criterion. The LP construction remains an illustration, not the whole commons.

The reviewed offline source is retained, with no compilation or deployment
selected. The optional dependency-footprint follow-up is closed with its remaining
unknown stated, not expanded into an installation survey. Current ordinary API
inspection confirms selected multiple named outputs and an independent intake
route; the already adopted native-first README explicitly includes reusable
adaptations. Thus this analysis does not justify a new interchange schema or
another multi-target export test. Full method compatibility, premise discharge
and actual returned mathematics remain particular application obligations.

The next high-payoff work must select a supported changing-input application and
map it to the retained public paths and evidence. Reuse those paths wherever
they already suffice; code only a surviving named obstruction. Do not select LP
automatically, add a new parser, or reopen passing package/proof campaigns to
make this theoretical argument look experimental. The unchanged full-v5 goal
stays active; general cold ancestry, useful large-scale discovery, sustained
service and public deployment are not declared solved here.

## References and deduplication

- [GROWTH-CONSTRUCTIVE-MODEL](GROWTH-CONSTRUCTIVE-MODEL.md): local soundness and
  holder substitution, adaptive investigations, and durable evidence limits.
- GROWTH-OPPORTUNITY-CHOICE and GROWTH-CLAIMS-CHALLENGE: independently owned
  concrete source/cost case and adversarial evidence contract in this directory.
- Earlier PHILOSOPHY-OF-GROWTH, GROWTH-MECHANISM, GROWTH-FIRST-ARCHITECTURE-DECISION
  and GROWTH-COMPARATOR-CHALLENGE remain the basis for capability semantics,
  economic accounting and fair comparison. Their results are not new here.
- [Alkassar, Boehme, Mehlhorn and Rizkallah, A Framework for the Verification of
  Certifying Computations](https://arxiv.org/html/1301.7462v1), introduction and
  section 2 inspected. Established precedent for separating witness correctness,
  concrete representations and the mathematical conclusion. This source supports
  the design pattern, not our implementation or LP cost estimates.
