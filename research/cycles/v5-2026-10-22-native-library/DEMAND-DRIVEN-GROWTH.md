# Demand-driven materialization: make exact interchange a selected investment

2026-10-24. `growth_payoff`; source/theory only. No runtime, product change, Git
operation or experiment. Read together with CANDIDATE-OFFER-CONTRACT and the
demand-driven source addendum to CANDIDATE-OFFER-CHALLENGE. This note adds the
overlap-aware decision argument, not another proof calculus or growth benchmark.

## Decision and practical meaning

**Do not require exact proof-data export as the price of making ordinary work
discoverable.** A producer can first offer its ordinary source/package reference
and untrusted hints. Materialize an exact supported bundle only when a consumer
selects a concrete potential use, or when anticipated demand justifies a batch.
Reuse a retained exact bundle when possible. Keep the current exact evidence,
preview and receiver-admission lane unchanged.

This does not establish that lazy export always wins. It is a candidate policy
for uncertain demand, with no optimality or default-win guarantee without demand
and cost assumptions. A popular shared core, high service latency, disappearing
producers, or useful normal package imports can favor another route.
The existing exporter facade remains useful: it can serve either selected demand
or an operator-chosen eager batch. No remote export daemon is needed initially.

The important architectural choice is **when conversion becomes necessary**, not
whether a mathematical producer has joined a new network. A source repository can
remain the initial contribution. Conversion can be performed by its author, an
explicitly approving third party, or a locally approving consumer; these actors
have different execution permissions and must not be conflated.

## Three statuses, with no premature proof identity

| Stage | What exists | What it can establish |
|---|---|---|
| Unmaterialized hint | Ordinary source/package locator, optional claimed name/type/features | A candidate to inspect or request; neither exact proof identity nor validity |
| Exact candidate | Actual supported evidence, derived IDs, bound preview and locators | Identity of available bytes and their syntactic claims; not receiver acceptance |
| Locally accepted mathematics | Current receiver checking/admission and retained local state | Its ordinary mathematical warrant under the selected policy |

Existing V2 previews are in the **second** row. They are derived from an actual
evidence unit and bind exact identities and type references. They cannot be filled
with guessed IDs or used as placeholders for unexported source. A proposed hint
must stay outside that exact lane; ordinary repository documentation/source search
already suffices for a first workflow. A new typed hint format/extractor is not
necessary merely to express the distinction.

A hint can be stale, malformed, false, notation-dependent or insufficiently precise.
Materialization can refuse, reveal a different actual statement, or yield nothing.
The consumer must inspect/select the resulting exact candidate anew. A backlink
to the hint records a discovery path, not equivalence to its alleged statement.
Hint counts must not be reported as admitted mathematical knowledge.

The source-seam review establishes two relevant limitations. First, extracting a
typed hint may still require importing the Lean environment: "type-only" does not
mean free. Second, the current project-selection hash binds paths/module names,
not all transitive artifact bytes. It is not an immutable revision commitment.
Use independently pinned source/toolchain/artifact premises where reproducibility
is promised; otherwise explicitly reselect current approved inputs and identify
only the resulting actual evidence. Never silently promise one revision and
materialize a changed one.

## An overlap-aware cost model

Fix one immutable supported library/toolchain epoch and a finite evaluation
horizon. Let `T` be its potentially offered targets. For `S ⊆ T`, let `D(S)` be the
union of whole declaration units needed for those targets outside the fixed seed.
Thus `D(S) = union_{t in S} D({t})`; a common dependency is not charged once per
theorem. Indivisible recursive groups are units, not freely splittable nodes.

Compare with the strong eager route: **one union export**, not a separate export
per offered theorem, when that union fits its operational bounds. Both histories
must finish the same selected useful consumer endpoints; keeping unused objects
is not itself an endpoint. If the union does not fit, compare a feasible batched
eager route, not an artificially failing baseline. Let `U = D(T)`. Adopt a stated
scalar resource measure (or
apply the equations to each resource separately) and the following bounded model:

- `I`: one private-environment import and source census for this epoch.
- `w_u`: processing/encoding/binding cost of unit `u` in one export, including its
  own outgoing dependency references. It includes relevant temporary-memory/I/O
  work only when those resources have explicit weights. Shared units are processed
  once within a batch, not magically once across separate exporter calls.
- `H`: net incremental hint preparation/indexing and demand-selection overhead
  relative to eager advertisement. Include differing exact-preview/target-index
  work here too; do not assume eager advertisements cost nothing. It can be signed.
- `F`: extra failed attempts, screening and unsupported/stale-candidate work.
- `R`: net additional service/retention cost of lazy versus eager operation,
  including retaining the source/toolchain needed for future materialization.
  `R` may be negative, but omitting a positive component is invalid.

The additive model is an analyzable approximation, not an asserted runtime law.
The current native exporter really imports/indexes its source environment and
exports selected full closure; it has no persistent cross-call unit cache. A
prospective guarantee can instead use upper bounds for lazy work and lower bounds
for eager work, with an explicit residual for nonadditive behavior. Working-set
and deadline constraints must hold independently of a favorable scalar total.

For actual selected demand processed in nonempty batches `S_1,...,S_K`, define
`r_u = number of batches j with u in D(S_j)`. Repeated requests already answered
from an exact cached bundle need not create a new batch; any lookup/serving cost
still belongs in the totals. In this model,

    Eager = I + sum_{u in U} w_u + common consumer costs
    Lazy  = H + F + R + K*I + sum_{u in U} r_u*w_u + common consumer costs.

Here `R` is relative, so the expression for Lazy is normalized by subtracting the
same eager service/retention base from both histories. Consequently, lazy delivery
is cheaper for the **same successful consumer endpoints** precisely when

    (1-K)*I + sum_{u in U} (1-r_u)*w_u > H + F + R.              (1)

This is not a sum of per-theorem closure savings. An undemanded unit has `r_u=0`
and contributes a saving; a once-exported unit contributes zero; a shared core
re-exported many times contributes a loss. The latter can dominate everything.
Each receiver still pays its own missing-proof checking. No producer-level union
argument permits charging independent receiver checks only once globally.

**Proof of (1):** partition the charged exporter work by call and unit, exchange
the two finite sums, and subtract the totals. Nothing about proof-search hardness,
semantic novelty or the probability of mathematical discovery is assumed.

### A nonempty sufficient region, not a measured estimate

Suppose one epoch has import cost 10, common-core processing cost 90 and 1,000
target-specific disjoint tails costing 1 each. Eager union export costs 1,100.
Ten demanded targets in two batches cost `2*(10+90)+10 = 210`; if incremental
`H+F+R <= 20`, their total is at most 230. Both routes can deliver the same ten
selected targets while lazy delivery saves at least 870 units of the stipulated
resource. **These are illustrative model values, not observations from our code.**
The common core has been charged twice in lazy delivery, correctly.

For a single demand-coalescing window, let `q = Pr(S is nonempty)` and
`p_u = Pr(u belongs to D(S))`. Linearity of expectation gives expected saving

    (1-q)*I + sum_u (1-p_u)*w_u - E[H+F+R].                    (2)

In particular, the avoided unique-closure work is exactly

    sum_{u in U} w_u * Pr(u is not required by selected demand).

No independence between targets is required. If individual demand events happen
to be independent, `p_u = 1 - product_{t requiring u}(1-Pr(t demanded))`.
That optional special case explains why a popular common core may have `p_u`
near one even when each individual target is rarely requested. A model that
multiplies every theorem's full closure by its demand probability is incorrect.

One coalescing window is available only when consumer deadlines permit waiting.
For repeated windows, replace `q` by `E[K]` and `p_u` by `E[r_u]` in (2).
These coefficients can exceed one and turn anticipated savings negative.

## Availability and latency are conditions, not free consequences

The same-endpoint comparison above requires that each demanded exact bundle can
actually be produced and acquired before its consumer deadline. A sufficient
deterministic service regime is:

1. At least one willing materializer retains accessible exact approved inputs,
   compatible toolchain and enough working memory until the selected deadline.
2. For each admitted batch, its bounded work fits finite reserved service capacity.
   Its coalescing wait + queued work + production + delivery + consumer checks
   fits the deadline. No finite-capacity producer accepts an unbounded request queue.
3. Produced evidence and required dependencies remain obtainable through the
   consumer's use interval, directly or from explicitly retained replicas.

This is a conditional scheduling/retention premise, not a new availability proof.
An asynchronous producer may legitimately decline. If demand is speculative or
has no deadline, refusal is cheap; if a consumer needs immediate use, eager exact
materialization/custody can be the correct investment.

For probabilistic analysis, separate input survival, materializer service, bundle
delivery and receiver compatibility/checking failure. If their conditional failure
bounds are `epsilon_1,...,epsilon_4`, a union bound gives success at least
`1-sum epsilon_i` without an independence assumption. Lazy delivery has an extra
production-availability dependency that an already hosted exact bundle need not
have. It is not fair to compare lower lazy cost while ignoring its missed endpoints.

Eager proof-data custody can survive deletion of the original source/toolchain.
Lazy hints cannot. Replicating immutable source plus the necessary toolchain can
reduce that risk, but its bytes, legality, execution approval and maintenance cost
belong in `R`. Another peer identity does not imply independent failure behavior.

## Counterexamples and bounded downside

There is no universal lazy advantage:

- If nearly every target is soon requested and deadlines prevent batching,
  `K` imports and repeated shared-core exports can be far worse than one eager
  union. Exact custody deduplication after export does not refund native work.
- If hints require almost the same import/scan as proof production, `H` can erase
  the hoped-for saving before the first request.
- If the producer disappears before the first demand, a hint may never become
  usable although an eagerly replicated bundle would have survived.
- If the selected closure exceeds the current exporter/receiver ceilings, waiting
  for demand does not make it fit. One large cold dependency core remains large.
- If normal locally approved Lean package reuse already solves the consumer's
  problem cheaply, converting it to this representation may add only overhead.
- False hints or many unique adversarial requests can consume unbounded work
  unless materializers and consumers enforce their own aggregate budgets.

A simple enforceable downside policy is **optional bounded exploration**. A local
participant retains its ordinary baseline route and allocates at most `B` extra
resource units over a fixed horizon to hint preparation/selection, failed requests
and selected materialization. Every attempted batch reserves a conservative bound
before launch; unknown accounting retains that reservation. Deduct cached serving,
retries and failed outputs too. Requests do not reset `B`. Stop or decline before
the next bound exceeds the remaining allowance.

If the baseline's resources/state are not impaired and it still performs exactly
the same work, the combined resource cost is at most `baseline cost + B`.
This follows by summing the reservations, not by assuming successful reuse.
It is an optional participant policy, not a global network research budget.
It does **not** bound completion-time slowdown or memory interference unless
capacity/scheduling is separately isolated. Nor does it recover costs already
paid by other participants; they need their own budget or explicit reimbursement.

Batching, exact-target cache reuse and declining expensive requests improve this
policy without needing an automatic export service. A demand-triggered full eager
conversion may later be sensible, but its next cost must be justified; "cumulative
past work is large" is not sufficient reason to spend more on a failing route.

## What this can justify about growth and ordinary Git sharing

If (1) holds, service assumptions hold and both routes deliver the same accepted
consumer endpoints, the software has a justified resource-saving region. With a
fixed budget, that saving can fund an additional **specified feasible** checked
use only if its full marginal cost fits. It does not imply that agents will choose
useful work, that every extra hint becomes knowledge, or that novelty grows
exponentially. The supplied capability argument is constructive and conditional.

Keep three conclusions separate: **correctness** comes only from unchanged
receiver checking; **resource improvement** follows only inside the stated
cost/service regime; **induced mathematical innovation** is unproved. This model
contains no lower bound on all possible local proof searches and does not deny
the local comparator its existing libraries, tactics, caches or ingenuity.

An equally capable Git/package sharing system can publish the same hints, batch
the same exporter, retain the same bundles and use the same receiver. Therefore
this analysis gives **no intrinsic advantage over that system**. The useful
deliverable may be the shared safe-interchange adapter itself, usable on Git,
ordinary files and optional peers. Compare actual integration, trust and resource
constraints, not a fictitious eager Git baseline that exports every theorem or
cannot publish a branch promptly.

Where the simpler ordinary route can use a locally approved package directly,
make that route available; do not force conversion merely to populate a commons.
Where automatic admission must avoid executing a new publisher's source/native
code, exact inert evidence is useful, but current process limits are not a proven
hostile-input sandbox. Equal-assurance comparators may use the same data adapter
or appropriate isolation. The theorem checker remains the authority, not the hint.

## Minimal workflow and architectural consequences

1. Publish ordinary work by the producer's chosen repository/file mechanism and
   expose optional untrusted discovery hints. No producer mathematical owner,
   proof-data conversion or new network membership is compulsory.
2. A local agent investigates its own work and selects a possible result. First
   consider its existing approved package route or an already materialized exact
   bundle. There is no global list of mathematical tasks or protocol input about
   human intention.
3. If exact interchange is genuinely needed, an explicitly willing operator
   selects approved local compiled inputs and a bounded group of targets. Run the
   existing owner-free exporter once within its finite limits. This request is
   for artifact conversion, not a command to the network to invent mathematics.
4. Validate the actual bundle, derive its real exact preview and expose/transfer
   those inert bytes. The consumer independently selects/checks/adopts them under
   the existing rule. Do not automatically download and execute remote packages,
   Lake hooks, tactics or initializers merely because a hint was found.
5. Retain useful exact output for later demand, advertise its concrete availability
   where desired, and charge retention. A later receiver may use a replaceable
   custodian even if the original materializer is gone, while still checking its
   own missing mathematics.

Recommended boundary now: finish the public **file exporter** integration and
document that it is invoked on selected demand or an explicit useful batch.
Keep pre-materialization hints in ordinary search/documentation rather than
building another protocol. Provider candidate ingestion stays optional. Do not
add a request broker, persistent producer cache, hint compiler, value score or
automatic full-library conversion without a concrete remaining obstruction.

Demand staging reduces speculative producer work; it does not solve cold
whole-closure verification, arbitrary Lean compatibility, semantic search or
worldwide availability. In particular, it does not satisfy the ancestry-free
verification ambition by relabeling a hint as a proof. Retained receiver caches,
approved library integration and optional specialized certification remain separate
choices with their own assurance/cost boundaries. None should become compulsory
solely to rescue an unfavorable conversion case.

**Decision-changing next evidence:** no new mathematics experiment is needed for
this policy. First expose the existing selected-target exporter and use its
retained evidence. A real request history can later estimate demand overlap,
materializer availability and missing-closure costs; a synthetic local theorem
campaign cannot establish their prevalence. Reject the policy for a workload when
the stated cost/availability premises fail, without weakening mathematical checks.

## Source-only adoption checkpoint

Root reviewed the cost argument and counterexamples. Recommendation: adopt the
**choice** to contribute ordinary work without compulsory proof-data conversion;
expose the existing bounded selected-target producer as the minimal optional tool.
Use on-demand, batched or eager conversion according to the actual cost/service
case, not uncertainty alone. The separately selected `produce-baseline` facade
fits this recommendation. No hint index/protocol, remote export daemon, new cache,
proof calculus, experiment or growth-success claim is selected by this note.
