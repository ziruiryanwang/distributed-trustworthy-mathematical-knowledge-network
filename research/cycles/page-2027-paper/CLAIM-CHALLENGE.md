# Paper claim challenge: what the evidence can support

2026-10-24, independent source/theory audit by `page_claim_challenge`.
This is research, not manuscript prose, a runtime selection, or a v5 release.
No experiment, database access, Git mutation, deletion or external submission
was performed. The canonical workspace guard passed.

## Final controlling recommendation: automate research, then test transfer

Root reports the latest user removes decentralization as a paper requirement.
The target is a convincing, technologically achievable automated research process
and a decisive experiment, not a networking paper. This section supersedes both
earlier rankings and the peer/central experimental plan retained below.

The best current thesis is:

> An explicit conjecture–countermodel–repair–proof–consolidation process can
> autonomously create reusable mathematical knowledge, and that knowledge can
> improve later independent investigations enough to repay its production cost.

This is a **research hypothesis**. Existing self-improving provers, theorem
discovery and library-learning work preclude claiming that the loop, generated
lemmas, or persistent memory are themselves unprecedented. The possible paper
contribution is a careful, causal, full-cost demonstration of **transferable
mathematical work produced by autonomous research**, especially conceptual repair
and useful statements rather than merely solving supplied proof obligations.
If the closest work already establishes this with a stronger comparator, redirect
or identify a narrower actual advance. A protocol diagram alone cannot do so.

### The narrowest convincing study

Use two experiments with different estimands, not a large factor grid:

1. **Discovery-policy comparison.** Starting from the same definition-only seed,
   compare a strong ordinary Lean coding/research agent against the explicit
   research loop at equal total production budget. Both may invent definitions,
   propose conjectures, seek counterexamples, revise hypotheses, use approved
   tactics, retain `.lean` source/notes, and use the same retrieval. The difference
   is the operational research policy, not privileged access to a memory or tools.
   Measure directly emitted checked statements, conceptual repairs, full cost
   and usefulness of the resulting frozen artifact. Keep every failed attempt.
2. **Fresh-recipient transfer assay.** Freeze each output library, then randomize
   independent fresh recipient agents to the common base alone or base plus that
   library, on prospectively hidden downstream tasks. Give identical retrieval,
   tools, task statements, cache rules and resource caps. Count actual checked
   outcomes and all retrieval/failed-search/adaptation/checking costs. This asks
   whether produced knowledge is useful to someone who did not discover it.

Within one frozen library, transfer randomization isolates the information value
of that artifact. Comparing the entire production policies isolates which process
creates useful artifacts economically. These are **not interchangeable**: an
expensive library can help recipients but lose on total cost, while a policy can
produce many statements with no downstream benefit. Analyze libraries/seed
episodes as clusters; multiple probes on one library are not independent research
replications. The artifact assay is not another proof of statement discovery.

All producers get a broad research objective, not the hidden anchor statements
or desired intermediate lemma names. Ordinary baseline researchers should be
competently prompted; a weak generic "try something" baseline against a detailed
treatment prompt would mostly test instruction quality. Let the baseline deploy
its best ordinary planning within the same constraints. If it naturally executes
the proposed loop already, the mechanism difference is small and should be
reported rather than suppressed by forbidding good baseline behavior.

### Distinguish statement discovery from proof discovery at scoring time

Define the discovery endpoints before running researchers:

- **Direct emitted anchors:** a researcher explicitly states and proves one of
  the hidden substantive anchor claims, in the original seed vocabulary, up to
  a prospectively fixed harmless normalization. This is statement discovery
  relative to disclosed inputs, not world-first mathematics.
- **Emitted genuine generalizations:** a researcher explicitly states and proves
  a stronger useful result encompassing an anchor. Keep these separately and
  require a predeclared bounded specialization test or blinded expert judgment.
  An evaluator must not run unconstrained theorem search to manufacture an
  unexpressed anchor from arbitrary base facts and award the agent discovery.
- **Unanticipated discoveries/repairs:** blinded content reviewers inspect the
  emitted definitions, models, countermodels, hypothesis changes and bridges
  against a frozen rubric for nonvacuity, nonredundancy and coherent extension.
  These are separate qualitative/ordinal outcomes, not automatically comparable
  theorem counts. Hidden anchors necessarily favor the benchmark author's known
  directions and can miss genuinely useful surprises; report this limitation.
- **Held-out proof assay:** a fresh recipient receives a target statement and
  produces its proof. This is proof discovery/usefulness, not autonomous discovery
  of that target statement. Do not combine its successes into the first count.

A proof's mere syntactic mention of a generated lemma is not a causal usefulness
test: unused `have` bindings and redundant premises can manufacture dependence.
Neither deduction from the whole logical closure nor wrapper count is a discovery
metric. The fresh-recipient randomized comparison answers the causal question
more directly than post hoc dependency counting.

### Prevent the treatment from defining its own exam

Freeze a definition-only seed and downstream probe sampler **before** production.
Use original-base-language anchors/probes; treatment-created vocabulary may be
used in solutions but must not be required to understand the task. Otherwise a
new definition can make a favored statement tautological or make the baseline's
task impossible to express. The seed, task meaning and permitted tools must remain
identical between arms. Do not pick held-out consequences after reading outputs.

Use several small theory seeds with different mathematical structures rather
than many renamed schedules. The previously observed repair/closure episode is
exploratory development data, not a confirmatory seed. One realistic pinned public
Lean source/benchmark family, where feasible, adds relevance; fresh source-defined
families add some protection against exact benchmark memorization. Neither route
eliminates pretraining knowledge. A generic tactic preflight should identify
ceiling/floor cases; exclusions and pilot changes must be recorded prospectively.

Dependency-closed library removal is useful only as a **diagnostic** ablation.
Removing a generated definition can delete many unrelated downstream entries,
change expression meaning or shrink retrieval burden. Preserve the complete
common base, exact target meaning and tool interfaces; report what actually
disappeared. Do not label a missing-dependency failure as loss of mathematical
insight. Statement-only, proof-syntax-only and recipe-only alternatives may help
explain a positive primary result but are not mandatory initial arms.

An oracle library is a **ceiling/sensitivity control**, not a fair policy rival.
An evaluator-selected small relevant lemma set can show that the targets are
transferable in principle. Its selection knows the hidden target and must not be
counted as autonomous knowledge production or a zero-cost achievable strategy.
If generated libraries help no one but oracle access helps, the producer/selection
policy is the likely bottleneck; if even oracle access does not help, the task or
recipient interface may be unsuitable. A strong dynamic-retrieval baseline uses
the same corpus, index and query budget whenever information access is matched.

### What can be justified mathematically, without pretending to prove novelty

Let policy g produce a checked library L on seed s at observed aggregate cost
C_g(s). Let a fixed recipient procedure on probe q and budget b have success
indicator Y(s,q,L,b). The artifact-value estimand is

    tau(L,b) = E_q,recipient[Y(s,q,L,b) - Y(s,q,empty,b)],

where `empty` means no newly produced artifact, **not** removal of the common
base. Randomization after L is frozen can estimate this without assuming that
the creator's chosen artifacts were unbiased. Generalizing to a production
policy averages over independently selected seeds and complete production runs;
it cannot treat the best observed library as representative of g.

For n future uses, a full-cost capability comparison must allocate C_g(s) to
those uses. A plot over total budget includes creation plus recipient costs,
not just n post-creation runs. If a scalar cost measure is justified, an observed
per-use saving d > 0 and incremental production/infrastructure cost A imply an
observed-model break-even condition n*d > A. This is an arithmetic extrapolation
under a stable workload/use-cost model, not a theorem that future demand exists
or savings persist. For multiple resources keep componentwise costs or disclose
weights. A measured positive tau with no plausible amortization is useful
information but not evidence of economically accelerating total research.

The formal validity argument is the ordinary conservative-library/checked-proof
argument: accepted new definitions and proved results do not grant false premises
under the fixed foundation. Definitional extension does not enlarge old-language
deductive truth, but known proof witnesses and representations can alter bounded
search success. This explains why resource-bounded transfer is a meaningful
scientific question; it does not solve it. Existing notes' conditional savings
inequalities cannot replace the proposed causal measurements.

### Multi-generation claim: valuable if real, optional until the first signal

A striking later stage lets fresh researchers consume the first generated library
and autonomously extend it before a second hidden assay. But comparing two stages
against a one-stage researcher with half the total compute proves nothing about
compounding. Match the total production allowance and give the one-stage/ordinary
baseline durable memory, retrieval, its own definitions and the full allowance.
Use holdouts whose construction does not depend on treatment-created names.
Second-generation artifacts must be new checked consequences/concepts rather
than repeated first-generation outputs.

One initial generation plus a fresh-recipient assay is the cheapest decisive
pilot. Add a second generation only if the pilot indicates a robust useful
transfer mechanism and affordable telemetry. Two successful generations can
demonstrate iterative capability, not exponential or indefinitely sustained
research growth. Do not spend the first budget on a large agent population or
distributed deployment merely to make the narrative look bigger.

### Pre-composition gate and concrete kill criteria

Before runtime, verify that model usage and the claimed resource caps are actually
observable/enforceable; the subagent interface may not expose enough token or
compute accounting. If only calls/time are measured, name that resource honestly.
Do not manufacture a full-compute claim from compiler timing. External model API
use has its separate credential/authorization rules; no campaign is selected here.

The theoretical/design story is ready only when the closest prior-work difference,
fixed seeds/holdouts, competent baseline, observable cost, artifact checks and
outcome distinctions are explicit. The empirical acceleration claim is ready only
after independent held-out evidence. No prose should say it already holds.

Kill or redirect when ordinary automation saturates the tasks; both policies
produce essentially the same behavior; positive-library selection was tuned to
the test set; generated lemmas are merely target answers in disguise; shared
artifacts hurt fresh recipients after retrieval costs; only one handpicked theory
shows a benefit; or creation cost cannot plausibly amortize. Record pilot failures
and bound redesigns; repeated unreported prompt tuning is researcher overfitting.

Recommended paper narrative if successful: **autonomous research produces an
auditable mathematical artifact; a fresh independent agent uses it on unseen
demands; the full-cost causal comparison shows when this transfer accelerates
discovery and when it does not.** The novelty must be checked against existing
automatic theory exploration, dynamic theorem libraries and self-improving agents.
Networking, a new cryptographic mechanism and a claim of global novel mathematics
are unnecessary. No acceptance probability can honestly be inferred in advance.

## Superseded update: decentralized discovery acceleration

Root reports a new explicit user steering instruction: the main paper must
demonstrate that decentralized sharing accelerates theorem discovery in some
meaningful way; checker-cost improvement cannot replace that headline. This
**supersedes the ranking in the historical audit below**. Retain the cut analysis
as supporting architecture/assurance, not the proposed primary contribution.

Root also independently found that Lean 4.35.0 (released October 12) already offers
`lake check --from-export`, a comparator, Linux sandboxing and external/paranoid
checking; OpenTheory already has explicit assumption/discharge theory packages
and standalone checking/remote-tactic patterns. The project runtime remains 4.34.
Do not upgrade it during this source-only investigation. Generic independent inert
proof checking or the logical cut rule cannot carry the novelty claim. The exact
upstream coverage/cost comparison still needs root's retained primary-source audit.

The new recommended headline is conditional on actual results:

> Under a fixed aggregate research budget, independently discovered and checked
> intermediate mathematics exchanged through replaceable peers increases held-out
> downstream proof discovery relative to optimized noncommunicating researchers,
> while preserving the benefit of an equally informed centralized sharing system.

This is a **hypothesis, not an existing result**. Its value would come from a
credible causal experiment plus reliable mathematical artifacts, not from the
elementary observation that a supplied lemma can shorten a proof. It must say
*proof discovery* if consumers receive the target theorem. A stronger claim about
*statement/concept discovery* needs separately evaluated generated conjectures;
do not rename theorem proving after results arrive. Independent producer discovery
of reusable intermediate statements is nevertheless part of this proposed loop.

### A single bounded ecosystem, not an isolated lucky consumer

Use an ecosystem episode as the unit of experimentation:

1. **Common initial state.** Fix a Lean foundation, definition-only seed theory,
   approved automation/search, environment/tool versions, resource vector and
   endpoint-selection protocol. Seed material must not already contain the
   intended intermediate lemmas. All researchers can inspect the same initial
   material; private exploratory choices may differ. Existing standard tactics
   and directly applicable library lemmas stay available in every arm.
2. **Independent discovery prefix.** Several researchers explore that theory
   under the same broad instruction to develop useful reusable consequences,
   without receiving downstream test statements or names of desired lemmas.
   Each keeps its own ordinary source, private cache and notes. Record all work,
   including failures. Freeze their output artifacts and checking outcomes.
3. **Held-out continuation schedule.** Only after the prefix is frozen reveal a
   prospectively committed downstream sample. The sample cannot be selected or
   edited to match what the producers happened to discover. Targets must be
   absent as exact proved producer outputs and require genuinely new composition,
   instantiation, hypotheses or bridges; changes of bound-variable spelling do
   not count. Record accidentally direct-answer targets under a separate category.
4. **Branch the same recorded prefix into matched arms.** Restart researchers
   with the same private artifacts and approved tools in each arm. Every arm is
   charged the full attributable discovery prefix, even if we execute and reuse
   the common prefix only once for experimental efficiency. This avoids giving
   one arm a free research labor force. Only cross-agent knowledge access differs.
5. **Complete actual checking and return.** Only fully checked, semantically
   matched outputs count. Consumers must search using their actual target/context,
   not hidden answer IDs. Make new outputs available through the actual ordinary
   publication path. This establishes a usable contribution loop, but one round
   does not establish sustained or exponential growth.

This matched-prefix design identifies the effect of **reuse after a common
discovery history**. It does not estimate the effect of sharing on the producers'
earlier exploration policies. That is a legitimate, narrower intervention and a
much cheaper initial experiment than pretending to evaluate lifelong collective
intelligence. Later multi-round adaptive studies are separate investments.

The evaluation's finite task set is not a product-wide research agenda. The
protocol still permits independent local goals; a controlled experiment needs
fixed outcomes to make an acceleration claim falsifiable.

### Arms that distinguish the causal questions

| Arm | Available reusable knowledge | What it identifies |
|---|---|---|
| I: optimized independent researchers | Each researcher's own prefix artifacts, ordinary libraries/tools/caches and any universally public seed knowledge | Noncommunication baseline without disabling local ingenuity |
| P: decentralized peer sharing | I plus peer discovery, exact checked mathematical artifacts and normal reciprocal publication | Aggregate value of cross-agent information exchange through this software |
| C: centralized equal-information sharing | Exactly P's available artifacts, matching indexing/ranking, publication timing and checking policy, served by a central index/custodian | Whether decentralization preserves sharing's benefit; not a deliberately crippled server |

The primary contrast is P-I. The C arm is essential to prevent assigning the
general value of sharing to topology. A positive P-I and parity with C would
support useful **decentralized realization** of the benefit, not superiority of
decentralization in an ordinary no-failure setting. If P loses substantially to
C, report that cost and revise the architecture or paper claim.

Mechanism ablations should be conditional on a credible primary result, not a
combinatorial experiment before there is signal. The best single ablation is
P with peer theorem statements/previews but no their proofs versus full checked
artifacts, while keeping private tools/budgets identical. This separates proposal
information from ready proof reuse, but it answers an additional question and
must charge failed proof attempts. A positive/negative-memory ablation matters
only if countermodels actually account for the observed benefit. Do not run both
automatically. Giving hints-only access a broken importer would confound it.

Provider failure is another separate axis. Demonstrating that selected shared
work survives loss of its origin is useful decentralization evidence; it does
not establish better normal discovery. The C comparator can have ordinary
replication and backups. Compare matched resilience budgets, not a replicated
peer network against an intentionally unreplicated single disk.

### A feasible, meaningful mathematical task family

Do not use the retained repair/closure episode as confirmatory data: authors
already know it, the targets informed the architecture, and its single observed
continuation lacks a counterfactual. It can serve as a clearly labeled feasibility
example only. It has not established an effect size.

A promising *candidate family*, pending overlap/difficulty inspection, is
**finite-state transformation and invariant theory over ordinary Lean-defined
structures**, spanning more than one seed vocabulary: commuting/idempotent
transformations and schedules; transition-system invariants and simulations;
and list/fold or relation-composition laws. Producers see definitions and broad
research directions, discover intermediate algebraic facts, bridges and
countermodels themselves, and downstream investigators face independently
sampled consequences involving composition or changed hypotheses. The family
has executable small models for finding false statements and universal Lean
theorems for accepted results. It does not require a huge mathlib installation
or new proof-generating backend on this PC.

This is a **proposal, not an assumption of publishable difficulty**. It must pass
two cheap preflight objections before use: (a) ordinary `simp`/`aesop`/`omega` or
a directly available generic lemma does not already solve nearly everything;
(b) the family has enough independent transferable structure that results are
not renamed copies of one repair example. A novel name for associativity is not
new mathematics. Sampling only examples where our handcrafted bridge wins would
invalidate the transfer claim. The predefined generator/sampler and all exclusions
must be retained, along with their rationale.

For stronger practical significance, seed at least one family from a public
existing Lean project or benchmark with a pinned pre-extension version. Producers
must not see later commits/solutions; consumers get held-out relevant work after
the freeze. Leakage from the model's training remains possible and must be
reported. Source-defined fresh families reduce exact benchmark memorization but
do not remove prior mathematical knowledge or guarantee general relevance.
The minimal main result should not depend solely on manually invented problems.

An open-ended statement-discovery extension would give consumers broad questions
rather than target theorems, then independently judge newly proposed conjectures,
countermodels and repaired assumptions. Exact checks establish truth; a frozen
blinded rubric establishes nonredundant contribution to the local theory. This
is scientifically harder to score and costlier than the fixed-target experiment.
Include it only if it can be evaluated credibly; otherwise state honestly that
the primary quantitative outcome is downstream proof discovery, with qualitative
concept formation as a separate case study.

### Estimand and proof obligations for a fair aggregate benefit claim

Let s be a preselected ecosystem seed, including initial theory, producer choices
or randomization, target schedule and allowed tools. Let Y_s(a,B) be the count of
distinct correctly checked target endpoints completed by arm a before its full
aggregate resource cap B; all prefix production, failed search, checking,
curation/indexing, acquisition and service charged to that arm are included.
Use an explicit resource vector unless a weighted scalar has a justified meaning.
The target estimand is

    Delta_peer(B) = E_s[Y_s(P,B) - Y_s(I,B)].

The topology cost/benefit contrast is

    Delta_topology(B) = E_s[Y_s(P,B) - Y_s(C,B)].

These definitions are not proofs that either difference is positive. Randomize
arm execution order and use independent consumer randomness under a predefined
paired scheme. Analyze **ecosystem-level** differences: targets inside one shared
episode interfere through their artifacts, so treating every theorem as an
independent data point manufactures sample size. Report individual episode
outcomes, uncertainty and resource curves, not only a pooled successful target
percentage. A noninferiority comparison to C requires a prospectively meaningful
margin, not a margin chosen after seeing P's deficit.

**Elementary but useful accounting lemma.** For matched prefixes with charged
cost A, let each arm's observed total discovery/continuation history be its exact
sequence of accepted endpoints and charged events. If P finishes k endpoints at
aggregate cost c_P and I finishes fewer than k by cost c_P under the same cap and
accepted-target policy, then P's retained trace has strictly better realized
capability at that boundary. A whole-trace comparison includes failures and
shared production once; it cannot be established by subtracting just successful
proof-check times. Extending this to an expected or reproducible benefit requires
the multi-episode causal design above. This lemma is accounting, not paper novelty.

The meaningful scientific information is that independently discovered artifacts
regularly make c_P smaller or Y(P,B) larger **after A and all transfer costs are
paid**, across unseen downstream demands. The theorem "sharing wins whenever its
savings exceed its costs" supplies none of that information and should not be
offered as the central theoretical result.

### Resource observability is a prerequisite, not an afterthought

Before any model experiment, root must verify usable per-run telemetry and actual
budget enforcement. Tool counts, source lines, elapsed conversation time and
compiler CPU are not substitutes for model reasoning/input/output usage. If the
current subagent interface does not expose accountable model usage, a tool-call-
bounded study may still be possible, but it cannot claim equal total compute or
tokens. Do not hide this by using arbitrary invented token estimates. An external
API campaign requires its own credential/authorization process and budget; this
note does not authorize it.

Reasonable measurable axes are provider-reported model token/cost totals, local
tool CPU, wall latency, peak memory and bytes/storage. Source approval/review
cost, if included, needs actual work measurements or an explicit unmeasured
limitation, not invented hours. Holding all caps equal does not mean all realized
costs are equal; plot outcomes against their actual charged cost. Save partial
attempts and refusals rather than retaining only successful artifacts.

### Confounds, kills and redirects

- **Free producer effect:** P receives a labor force that is absent or uncharged
  in I. Kill the comparison; fix aggregate budgets and private producer access.
- **Answer cache effect:** target theorem was already returned during production.
  Separate exact replay results; require held-out composition/changed premises
  for the main transfer claim, without hiding easy original solves in I.
- **Retrospective relevance:** downstream targets are chosen after producer
  output inspection. Kill confirmatory status; preserve as an exploratory pilot.
- **Knowledge versus topology:** P beats I but C already achieves the same gain.
  This supports the sharing mechanism, not a superior decentralized discovery
  algorithm. The decentralization contribution must be accurate resilience/
  replaceability plus measured overhead, not a rebranded causal effect.
- **Same checker, different help:** one arm gets richer task explanations, known
  lemma IDs, manual bridges or author intervention. Charge and disclose it; the
  main controlled comparison cannot silently depend on such help.
- **Triviality or total hardness:** optimized I solves nearly everything already,
  or every arm fails. Do not manufacture significance by selecting only surviving
  favorable examples; revise the family prospectively after recording pilot
  failure and reset confirmatory targets. Bound the number of pilot revisions.
- **Harmful retrieval:** irrelevant valid lemmas increase token/search cost or
  suppress good conjectures. These are real negative outcomes, not invalid trials.
  Fix retrieval only if the anticipated gain exceeds its development/evaluation
  cost; the paper may reveal a practical operating boundary instead.
- **Narrow one-family victory:** a positive repair-style result does not justify
  broad mathematical discovery. A second independently selected vocabulary or
  realistic held-out source family is the minimum direction for transfer validity,
  not a guarantee that two examples suffice statistically.
- **No net effect after production:** strong consumer savings do not amortize the
  creator/curator/service bill at plausible reuse counts. Report the observed
  break-even demand region and compare with ordinary Git/Lake sharing. If that
  region is implausible, stop claiming useful network growth and redirect.

The efficient order is: resolve venue/prior-work/telemetry; freeze a credible task
family and comparators; run one explicitly exploratory mechanism discriminator;
decide whether the effect and budget justify a separate held-out confirmatory
study; only then compose the paper. No number of repeated source audits replaces
the missing causal evidence. A grounded-cut speed test does not answer this new
main research question and should not consume the growth-paper budget.

## Decision

The following section is the **superseded pre-steering audit**. Its candidate
ranking is historical; its correctness, prior-work and comparator cautions remain
relevant. The controlling main-paper direction is the discovery study above.

The current project does **not** yet justify an assertion of a high acceptance
probability. Neither a long engineering history nor a collection of successful
checks establishes a publishable contribution. The viable objective is a narrow,
falsifiable contribution whose strongest objection has been answered before
writing. The venue's actual call and prior publications must be verified by root;
this audit does not independently establish the deadline or submission rules.

Rank the following two candidates, not the entire v5 architecture:

1. **Grounded, history-local verified memory for independently restarted agents.**
   A concrete negative result identifies an accumulation tax even without repeated
   proof checking; an exact local-warrant cut removes omitted theorem ancestry
   from selected continuation, while preserving a stated mathematical acceptance
   relation. This has the strongest implementation/theory correspondence already
   available. It is an enabling result for growth, not proof of faster discovery.
2. **Semantically scoped negative knowledge for conceptual continuation.** Checked
   countermodels and nonimplications can guide later investigators away from
   invalid generalizations without becoming a global research agenda. This is
   closer to the user's creative-growth interest, but the present episode only
   establishes possibility. Broad negative-memory novelty is already threatened
   by direct prior work; causal downstream benefit and exact semantic scope are
   the possible distinctions, not the mere existence of a failure bank.

Do not combine both into a claim of an end-to-end worldwide accelerating commons.
They need different comparators, assumptions and outcomes. Candidate 1 is the
first paper-selection target unless prior work shows it to be only routine glue;
candidate 2 should replace it only if a genuine prior-work gap and affordable
decisive study survive. A negative finding may redirect the project, as authorized.

## Four different achievements

| Achievement | Meaning | What it does not imply |
|---|---|---|
| Correctness | The exact accepted statement follows under the selected foundation/policy | Relevance, novelty, useful uptake, cheapness, computer security |
| Capability | A disclosed recipient can obtain and use a warranted result under its actual constraints | That the baseline could not do so or that the path is faster |
| Comparative growth | A specified investigator/workload completes more distinct useful downstream work for the same full resource allowance | Universal scientific value or inevitable exponential growth |
| Novel contribution | A specific mechanism, result, empirical finding or evaluation advance beyond the closest published approaches | A new mathematical fact or priority based on the date of our code |

The retained `Repair`/closure theory is nonvacuous episode-relative development,
not established new-to-literature mathematics. Its 67 newly checked units include
ordinary library dependencies; 22 changed artifact IDs after a source realization
are not 22 new concepts. These must not become growth labels in the paper.

## Candidate 1: negative result and a sound repair

### Research question and intervention

Can a long-lived verified agent reuse locally warranted mathematical interfaces
after process restart without mandatory traversal of all its old theorem proofs
or unrelated accepted history? The relevant intervention is **the warrant and
continuation contract**, not a new solver, better prompt, global blockchain or
succinct proof production. Exact local checking was paid earlier; the subsequent
consumer uses a protected summary of that actual event.

The user workflow is independently arriving contributions that must become
durably usable before an unknown later contribution arrives. One giant final
batch is not semantically equivalent to this latency requirement. Nevertheless,
ordinary batching is a necessary comparator whenever all proofs are already
available together. An approved long-lived Lean session is also a comparator
where the threat/restart/retention policy permits one. The paper cannot invent an
extra process-restart requirement merely to make its method win.

### Proposition C1-A: a restoration tax, not a proof-search lower bound

**Proved in the following explicit model.** Suppose a continuation algorithm,
before operation i, traverses every record in its selected accumulated context.
The initial context has m records; each earlier operation added at least d > 0
records that remain in that context. The sequence has n successful operations.
Then it performs at least

    n*m + d*n*(n-1)/2

context-record visits, even if no old proof is kernel-checked again.

**Proof.** Before operation i (numbering from 1), the context has at least
m + d*(i-1) records. Sum that lower bound for i=1,...,n. It is independent of
whether a visited record contains a proof or a cached checking result.

This source-level negative result applies to the disclosed predecessor's actual
metadata loops. It is **not** a lower bound on Lean, Git, all verified libraries,
all file-system I/O, or all implementations of persistent agent memory. Delta
storage avoids duplicated stored bodies but does not refute a repeated-traversal
bound. Conversely, a resident environment or a maintained exact-key index may
avoid that traversal; these must receive credit.

For a batch size b dividing n, with one traversal per completed batch and the
same monotone context, the analogous visit count is

    (n/b)*m + d*b*(n/b)*(n/b-1)/2.

Thus batching itself changes the coefficient/order when b scales with n. A claim
of an asymptotic improvement that hides b is misleading. Selected smaller roots
can also change the premises but pay their real construction/re-admission costs.

### Proposition C1-B: one-way, recursively composable interface-cut safety

**Conditional system theorem, not a new foundational cut-elimination result.**
Let K_0 be an exact warranted environment under policy P and support epoch e.
Each successful event i has:

1. An eligible committed parent root, and exact protected summaries whose claims
   were established by earlier committed events or K_0, never by peer assertions.
2. A scratch context H_i containing the supported exact foundation, complete
   demanded computational declarations/groups, and only selected old theorem
   assumptions with their exact names, universes and types.
3. A realization J_i from H_i into the mathematical environment represented by
   the selected parent. It preserves every typing/conversion rule used by this
   supported profile, gives concrete declarations their exact old semantics,
   and realizes each scratch theorem assumption by its earlier warranted proof.
4. A genuine kernel check H_i |- t_i : Q_i, with Q_i : Prop, exhaustive allowed
   assumption census, and exact identity/fresh-name binding to the request.
5. An atomic durable event that makes the new summary eligible only after that
   exact check has completed under the still-eligible parent/support binding.
   Failed/uncertain checks and uncommitted summaries cannot be used as premises.

Then every committed output has a derivation under P in an environment extending
its selected warranted parent. Reopening a process does not change this result
if the protected root/support association is preserved. A branch cannot borrow
an uncommitted or unrelated branch's theorem merely because its name matches.

**Proof.** Induct over committed event order. K_0 is warranted by premise. Every
scratch theorem assumption at event i is realized by an already warranted proof
from the eligible parent; concrete rules and foundation retain their meanings.
Typing preservation under J_i yields J_i(t_i) : J_i(Q_i). Exact binding identifies
this with the stored output claim; atomic promotion makes it available only after
the inductive step. An event with no completed promotion contributes no premise.
Restrict the induction to the selected parent ancestry when branches coexist.

The hidden hard premise is **implementation-to-realization correspondence**,
not the displayed induction. It includes universe substitution, primitive
operations/literals, dependent conversion, exact generated declaration groups,
concrete bodies, namespace collision handling, foundation/axiom policy and the
controller's binding to the event. A checksum or a `.olean` load does not prove
this premise. This can be a carefully scoped paper theorem backed by a precise
rule argument; it must not be labeled a machine-checked proof of the whole system.

**Completeness counterexample/limit.** Replacing theorem bodies by assumptions
does not generally preserve every original native conversion success. The retained
accessibility-recursion example shows the danger: eliminating a constructor-backed
proof of `Acc R x` into Nat can reduce when the body is available and fail to reduce
when it is opaque. The old source finding concerns a historical Lean pin; it is
not executed evidence for the current 4.34 runtime. The sound contract needs only
the positive implication above and must refuse unsupported cases. It must not
claim equivalence to native full-context checking or derive computational opacity
from proof irrelevance. Any current-runtime completeness claim needs new evidence.

### Proposition C1-C: a useful locality statement

**Proved for the described abstract operation, conditional on complete path
correspondence.** Let a call request k exact old name bindings and introduce r
fresh names. Suppose its persistent compressed binary trie uses h-bit routing
keys, strictly increasing split depths, exact full keys at leaves, bounded payloads,
and only path-local lookups/path-copy insertions. Then one lookup reads at most
h+1 trie nodes; one insertion has O(h) logical node reads/writes. Thus indexed
summary/freshness work is O((k+r)*h), independent of the number of unrelated
accepted events, apart from the underlying storage engine's access cost.

**Proof.** Every descent strictly increases a depth in {0,...,h-1}; at most h
branches and one leaf are visited. Insertion adds at most a new branch and leaf
and copies the visited ancestor path. Sum over requested bindings and insertions.
Retained roots share untouched subtrees; this is not a whole-map copy.

For the actual selected map h=256, its conservative source bounds are 257 node
visits per lookup, and 515 logical reads/258 attempted writes per insertion.
Repeated controller lookups multiply these bounds by their actual constant count.
Hash collisions explicitly refuse; they do not create name equality. These are
logical operation bounds, not constant SQLite page I/O, CPU, fsync or latency.

With B the fixed restored basis, S_i the selected full semantic records/types,
T_i the new proof/type, and A the one-time genuine summary construction, the
architecture-level bound has the form

    A + sum_i [index_i + read/authenticate(B) + read/check(S_i,T_i)
               + commit_i + custody_i + failure_i].

There is **no required term for omitted old theorem-proof bodies or unrelated
event enumeration** if all implementation paths obey the contract. There remain
fixed-basis proof bytes, large theorem types, concrete definitions and their
embedded proofs, expensive dependent conversion, source-support checks and real
storage-engine costs. Calling this constant-time proof verification is false.
The actual source anchor checks one protected identity row, not a context scan;
the current fixed-basis successor hashes that fixed artifact once per event.

### What is potentially new, and what is not

Cut/substitution reasoning, proof-carrying code, incremental checking, Merkle
structures and persistent maps are established. Merely assembling them is not
automatically a research contribution. A viable contribution is the precise
**usable and persistent boundary** between an agent's untrusted proposed work,
its expensive locally grounded mathematical memory, and later independent
processes, plus a concrete exposure of where standard apparent caching fails.
Actual selected Lean semantics, refusal conditions, crash/branch/revocation
behavior and retained proof interchange may make that integration nontrivial.

Novelty therefore depends on the closest existing Lean proof importers, context
pruners, independent checkers, persistent theorem-prover sessions, proof capsules
and agent-library systems. Root's prior-work investigation must settle whether
an existing tool already supplies this exact practical contract more simply.

### Smallest decisive evidence before choosing this paper

- Reuse the retained recursive two-event implementation evidence and 42-group
  corrected controls; distinguish them from the unused performance comparison.
  They show a path, not a speedup or broad supported-workload distribution.
- Fully map the formal realization and locality premises to the current selected
  source, including no accidentally history-sized recovery/census path. The
  historical theorem-opacity countercase must not stand in for current semantics.
- Complete the already-written matched comparison only if root selects it for
  this paper question. It compares old/restored cuts, native sequential, and native
  batch. Its single two-target engineering point does not establish a scaling
  curve, statistical significance or real-world prevalence.
- For a paper locality claim, add one *different* decisive check if needed:
  demonstrate selected continuation remains valid when unrelated prior proof
  custody is unavailable, while altered selected summaries/branches fail. Use
  disposable fresh copies/fixtures only; never remove preserved historical data.
  Whether existing controls already cover this must be checked before any run.
- A scientifically strong practical claim also needs at least one representative
  supported theory beyond the construction-motivating repair example, selected
  before inspecting outcome. Report refusals and preparation cost. If this is
  infeasible before submission, narrow to an implementation/theory workshop
  contribution; do not label the original two-theorem example general growth.

**Falsifiers:** exact realization fails; a call silently traverses growing omitted
history; the useful semantic closure is usually almost the whole environment;
ordinary approved Lean/Lake or batching meets the same constraints at lower cost;
initial migration never amortizes in plausible histories; failures/refusals make
the restricted route less useful than its savings; or closest work already offers
the same boundary. Any of these can defeat the paper thesis without making the
software worthless. Do not respond by weakening the comparator secretly.

## Candidate 2: checked negative transfer and concept revision

### Claim and direct prior-work obstruction

The distinctive hypothesis would be that **exactly scoped, checked mathematical
nonimplications** transfer useful constraints on later concept design, rather
than merely storing unsuccessful attempts or giving a solver more positive lemmas.
The existing A/B episode supplies a coherent motivating instance: mutual repair
preservation does not imply commutation; B introduces common closure-order
assumptions and proves both a bridge and a stronger impossibility statement.

Parallel literature review reports a direct relevant primary source, to be fully
verified/adopted by root before citation: Wang, *Negative Knowledge as Failure-aware
Shared Memory for AutoResearch*, arXiv:2606.21024 (June 2026), and TNLean,
arXiv:2607.07857. The former already concerns typed bounded shared failure banks,
fresh researchers and cross-task transfer; the latter reportedly retains
counterexamples/strategies. Therefore "agents benefit from sharing failures" or
"negative knowledge is reusable" is not a defensible novelty claim.

### Proposition C2: exact refutations can transfer, but arbitrary wording cannot

Let q be an exact proposition in warranted environment K, with r : Not q. A later
candidate p may be ruled out if the later warranted environment contains both
the compatible interpretation of r and a checked transport f : p -> q. Then

    fun hp => r (f hp) : Not p.

**Proof.** Function application and implication elimination. If the environment
is consistent, excluding this exact p cannot exclude a provable p. No type/name
similarity, textual paraphrase or failed proof search supplies f.

The engineering opportunity is the explicit scope/transport obligation: a stored
negative result must not reject a strengthened hypothesis, a changed definition,
an alternate carrier or a different axiom policy by fuzzy match alone. Heuristics
may suggest a candidate mapping; kernel checking must validate the actual bridge.
This rule is elementary and already expressible in Lean. It becomes a contribution
only if it solves a demonstrated failure in existing practical agent memory and
improves worthwhile downstream behavior economically.

**Counterexample to naive transfer.** A model satisfying A and not B refutes
`forall x, A x -> B x`, but does not refute `forall x, A x /\ C x -> B x` when the
model fails C. The A/B episode itself illustrates this: a counterexample without
closure-order structure is compatible with B's corrected theorem. A system that
simply remembers "preservation does not imply commutation" could suppress exactly
the useful strengthening it should help discover.

### Why current evidence is insufficient

B's research record says the shared model stopped it pursuing the unrestricted
false generalization. That is honest qualitative process evidence. There is no
paired counterfactual, randomization, conserved reasoning budget, multiple domain
episodes or blinded assessment. B also received positive theory and a handoff;
the negative result's marginal effect is confounded. The later symbol query is an
API test over known content, not blind discovery by a fresh researcher. Neither
can be reinterpreted as an observed speedup.

The old prefix-cost proposition is mathematically valid only under unchanged
independently replayable remaining trials. A creative agent deliberately changes
its hypothesis space after a countermodel; that violates the coupling premise.
The theorem cannot justify the very adaptive creative effect the paper wants.
The total-benefit inequality is a budget identity once all differences are put
inside the overhead term. It does not provide the missing baseline lower bound.

### Minimal new study if this candidate survives literature review

Use independently selected downstream formal investigations; the test set must
not be chosen after seeing which examples our countermodels help. Separate
proposal/selection records from test material. Same models, initial mathematics,
positive results, tools, budget, retrieval affordances and stopping rules in all
arms. A useful minimal contrast is positive library alone versus the same library
plus typed negative records; a third heuristic-negative arm isolates checking/
scope discipline if that is the claimed improvement. Give every arm the existing
ordinary Lean/Git retrieval capability, not a deliberately blind local agent.

Measure checked nonduplicate downstream capability, conceptual repair/refinement,
scope errors, abandonment of false conjectures, useful recovered hypotheses and
complete cost, including producing/curating/retrieving countermodels. Reporting
only successful proofs omits successful refutations; reporting only rejected
conjectures rewards trivial branch inflation. A blinded domain-informed content
rubric is needed for open-ended conceptual output, with exact formal checks as
the validity component, not an automatic novelty score.

The smallest design size cannot be chosen honestly before effect/variance and
cost information. One independent seed episode is a feasibility discriminator,
not a high-confidence estimate. Avoid promising acceptance on the basis of a
handful of favorable demonstrations. No API spending or new experiment is
authorized by this audit. If no measurable distinction survives the existing
negative-memory literature, redirect to Candidate 1 or abandon this paper angle.

## Comparator discipline and reviewer rejection tests

1. **Simulator circularity.** If ordinary Git/Lake plus the same importer/index/
   adapter can simulate the path at essentially the same cost, there is no unique
   decentralized mathematical power. The contribution may be the importer or
   adapter. Do not require a public-good implementation to defeat a baseline that
   is given the entire implementation for free, but identify exactly what is new.
2. **Information fairness.** Isolation versus sharing is a legitimate intervention
   if the question is information transfer; it is not evidence that this protocol
   beats another sharing system. Receiving extra useful facts is not by itself
   a new algorithmic contribution. Compare equal available remote information
   for protocol efficiency and unequal negative-record access only when that is
   the prospectively specified causal intervention.
3. **No invented lower bounds.** Missing a named lemma from a local library does
   not imply a large discovery cost: a standard tactic or alternative proof may
   already solve the task. Avoid contrived endpoint families that merely unpack
   one parametric theorem into many aliases.
4. **Full and appropriate costs.** Charge preparation, checking, failed retrieval,
   retries, migration and retained service once where actually shared, not zero
   or once per recipient arbitrarily. Do not add nested worker CPU twice. Separate
   already-grounded continuation from cold end-to-end use and fixed from recurring
   costs. Experiments on warm caches cannot establish cold reception cost.
5. **Agent relevance.** A small persistent proof database alone might be a theorem-
   proving systems paper rather than an agentic-engineering contribution. Explain
   an actual autonomous propose/validate/reuse/continue loop and its failure mode;
   do not sprinkle "agent" onto every database operation. Conversely, prompt-
   engineering anecdotes without a controlled mechanism are unlikely to justify
   a programming-languages-oriented systems contribution.
6. **Scope and maturity.** PAgE workshop selection, if confirmed, is not main-track
   POPL acceptance. A workshop can value a sharp early result, but that does not
   justify a qualified-v5 replacement, global-deployment claims, or predictions
   of high acceptance probability. The full v5 goal remains independent and open.

## Selection gate before manuscript prose

Proceed only after root has a one-sentence claim, its closest competing work,
the exact implemented or formal difference, a source-bound acceptance/cost
argument, and evidence that answers the strongest specific reviewer objection.
For Candidate 1 the central objection is "ordinary Lean/library persistence already
does this"; for Candidate 2 it is "known counterexample-guided learning with an
uncontrolled anecdote." If those objections remain unanswered, more prose is
not progress. Gather only evidence that can change this decision.

Do not require or claim a numerical acceptance chance. A defensible readiness
judgment is that the scope fits the verified call, the novelty survives direct
comparison, the principal claims are evidenced, and limitations are explicit.
An independent adversarial mock review is useful at that point, not repeated
reviews of the same unaltered claim while the decisive evidence remains missing.

## Inspected local inputs

- `AGENTS.md`, `GOAL.md`, top of `research/NOW.md`, `CURRENT-DESIGN.md`.
- Growth-selection `CONCEPT-CAPABILITY-THEOREM`, `GROWTH-RELEASE-THESIS`,
  `GROWTH-LIFETIME-DECISION`, `GROWTH-VALUE-CHALLENGE`,
  `GROUNDED-CUT-CONTRACT`, and the relevant source/opacity/cost sections of
  `LIFETIME-VIEW-FEASIBILITY`; selected constructive-model sections.
- Native-library `GROWTH-COMPARATOR-CHALLENGE` and its recipe follow-up.
- Concept episode `CONTRACT`, `CONTENT-AUDIT`, and `B-RESEARCH`.
- Grounded-cut `CONTRACT`, `cut_map.py`, `MAP`; current basis successor
  `source_anchor.py`, controller admission path, and `PAYOFF-PLAN`.

External-paper particulars above are explicitly cross-agent findings awaiting
root's source adoption, not independently verified citations by this auditor.
