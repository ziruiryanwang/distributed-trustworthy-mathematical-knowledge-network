# Can automated mathematical research make later research easier?

Root research decision, 2026-10-24 Chicago. Prospective design, not a manuscript,
an empirical result, a claim of priority, or a completed-v5 declaration.
The user's latest clarification explicitly makes decentralization optional.

## Decision

Study **automated theory formation with transferable, resource-accounted value**.
Use ordinary Lean 4, a capable existing agent, durable source libraries, and
recorded research actions. Do not require networking, a new prover, model training,
succinct certificates, or the unfinished worldwide architecture for this paper.

The central question is:

> Can an automated investigator invent and verify mathematical structure that
> helps a fresh investigator discover further mathematics, with benefits that
> exceed the cost of creating, selecting, finding and using that structure?

The striking result would be an evidenced causal chain: autonomous investigation
creates a useful intermediate theory; a fresh researcher obtains capabilities
from that theory; the entire process improves outcomes at matched total cost.
Each link needs different evidence. A plausible narrative is not yet a result.

Our contribution may be a rigorous empirical finding and reusable evaluation
method, not a new foundation model or the first conjecture/proof loop. If a
specific research policy adds no value beyond existing tools, reject that policy
without abandoning the scientific question. Do not retrofit a positive story.

## What mathematical growth means here

A sound theorem does not add a logically independent truth to a fixed foundation:
it makes an existing consequence accessible. Admissible new definitions add
expressive interfaces, conservatively, rather than arbitrary axioms. Resource-
bounded access to consequences can nevertheless change dramatically.

For fixed investigator A, initial library L, budget b and precommitted probe
distribution D, define U(A,L,b,D) as expected score on those probes. A generated
library G has operational value if U(A,L+G,b,D) exceeds U(A,L,b,D). This is
relative to A, b and D, not an intrinsic or universal mathematical-value metric.
The probes assess utility; they do not determine mathematical truth.

Separate three claims:

1. **Statement discovery:** the researcher proposes a substantive statement or
   concept not supplied in its research brief and produces checked consequences.
2. **Transferred capability:** fresh researchers perform better with the generated
   mathematics than under a specified alternative exposure.
3. **Economic acceleration:** the complete policy, including failed research and
   library construction, improves mathematical outcomes at the same resource
   budget, or reaches a fixed outcome at lower cost.

Proving a supplied hidden-test theorem establishes a proof capability, not by
itself statement discovery. An unfamiliar name, longer proof, additional import,
or a thousand instances of one theorem establishes none of the three claims.
Use episode-relative novelty; literature novelty requires a separate substantive
assessment and must not be inferred from absence in the initial repository.

No human-intention field is added to mathematical acceptance. Local researchers
can choose their investigations. A study's hidden evaluation questions are
measurement instruments, not a mandatory commons research agenda.

## Why this is plausible, and the limits of the argument

Recurrent proof obligations can have a common mathematical cause. An investigator
can replace many special-case searches with a definition, invariant, abstraction,
transport theorem, or characterization. Countermodels can distinguish missing
hypotheses from merely unsuccessful proof search. Checked consequences and
applicability conditions can then survive the original conversation.

This predicts benefit where related future investigations repeatedly encounter
the same structure. It predicts little or negative benefit when questions are
unrelated, the base library already contains the abstraction, ordinary tactics
solve the cases cheaply, or retrieval/adaptation costs dominate.

An illustrative restricted model makes the investment explicit. Suppose a fixed
research investment costs c, has probability theta of producing a useful reusable
asset, and that asset saves expected delta on each of m later opportunities,
relative to the specified baseline. Suppose added per-opportunity exposure cost
is h. Under these exogenous, additive assumptions its expected net saving is

    theta * m * delta - c - m * h.

The investment is attractive only where this is positive. This is elementary
decision analysis, not a new theorem about creativity, not a lower bound on
ordinary Lean, and not evidence that theta or delta is positive in our system.
Ordinary agents may independently discover and cache the same asset; then their
actual delta is smaller. Adaptive future research violates the simple exogenous
model, so the full policy must also be evaluated directly.

Measure the predicted boundaries: transfer distance, repeated opportunity,
library clutter, and research-investment cost. An explanation that predicts both
successes and failures is stronger than a collection of favorable examples.
Neither this model nor a few successful generations implies exponential growth.

## Closest work: the generic loop is not new

The following are primary-source reports, not reproduced experimental results.

- [CPL](https://arxiv.org/html/2509.14274v4) already separates conjecturing from
  proving and reuses generated formal context. Its topology study reports a
  selected hidden intersection theorem in 5/20 versus 0/20 libraries at matched
  14-million-token budgets. Repeating the same idea in a different notation is
  not enough; its related-work and experiment limitations must be treated fairly.
- [DreamProver](https://arxiv.org/html/2604.26311v1) already abstracts and refines
  learned lemma libraries, tests transfer and ablates library construction. It
  reports construction output-token costs separately. Its inference savings
  should not be misreported as full-lifetime savings, nor should we allege it
  never accounted for construction.
- [Learning to Discover Interesting Mathematics](https://arxiv.org/html/2609.28603v1)
  studies interestingness, library-relative proof cost and autonomous growth.
  Its graph-compression utility is not the same quantity as fresh-agent causal
  discovery benefit, but both belong in our comparison.
- [The LEGO-Prover reanalysis](https://arxiv.org/html/2504.03048v1) shows why
  literal reuse and budget-matched controls matter. This is evidence of specific
  weaknesses, not a theorem that library learning is ineffective.
- [FERMAT](https://arxiv.org/abs/2511.14778), HipSpec/Hipster and HR-style theory
  formation precede generic abstraction, conjecturing and counterexample-guided
  revision. Do not claim a new mechanism by combining their descriptions.

The candidate gap is **prospective, artifact-mediated, full-cost evidence of
useful autonomous theory development**, including when the mechanism fails.
This is a candidate empirical contribution, not an established first-of-its-kind
claim. The accompanying GROWTH-RELATED-WORK.md audits nearer alternatives.

## Proposed research process

The smallest useful implementation is an explicit policy over ordinary tools:

1. Explore a formal seed theory; propose conjectures and, when useful, definitions.
2. Try proofs and inexpensive finite countermodels under a bounded allowance.
3. When failures recur, propose a shared explanation: a missing hypothesis,
   reusable invariant, generalization, or connection to another theory.
4. Check proposed results. Failure to prove remains unknown, not false. A tested
   finite witness is promoted to a mathematical refutation only with its required
   formal evidence. Similarity never justifies transporting a refutation across
   changed assumptions.
5. Consolidate reusable mathematical modules with exact assumptions, proofs,
   examples/counterexamples and conservative definitions. Keep ordinary notes
   advisory, and preserve failed attempts in the research record.
6. Let fresh investigators continue from these artifacts, without the producer's
   conversation or human mathematical repair.

The possible differentiator is economical **scope-aware theory consolidation**,
not simply saving lemmas. It is still a hypothesis: current ordinary agents may
already do it equally well. A policy needs a precise intervention before testing;
do not call an unspecified bundle of better prompts an algorithm.

## One integrated experimental narrative, three separate tests

### Test A: autonomous discovery rather than assigned-target solving

Give researchers a small formal nucleus and the same broad investigation brief.
Do not give the desired downstream theorem, useful lemma, concept name, or result
ID. Freeze domain choices, admissibility rules, hidden substantive anchors and
stopping rules before seeing outputs. Keep all runs, including empty libraries.

Compare the explicit research policy with a strong ordinary Lean research agent:
same model/settings, starting mathematics, tools, concurrency, permitted source
access and total resource allowance. The baseline keeps its .lean files, proofs,
notes and caches, can search them, and may invent its own lemmas, concepts and
counterexamples. No amnesia, forced flattening or ban on reuse is allowed.

The policy contrast is how research resources are allocated and consolidated,
not whether one arm is allowed a library. A CPL-like existing policy is an active
comparator if we claim superiority to existing discovery methods. It may replace
the generic baseline if it is stronger; adding many weak arms is not useful.

Hidden anchors provide a fixed quantitative endpoint. Count a directly emitted
anchor, a checked equivalent formulation and a qualifying generalization
separately. An evaluator that assembles old lemmas into a new proof has measured
available capability, not a theorem actually discovered by the agent. Keep that
as a separate assay. Use a frozen bounded matching/bridge protocol, with masked
review for residual cases; do not pretend arbitrary equivalence is decidable.

Anchors miss unanticipated good mathematics. Supplement them with arm-blind
mathematical assessment of nontriviality, scope and reusable connections. Report
agreement and disagreements. Model-only judging is screening, not independent
expert validation. Neither hidden anchors nor renamed definitions proves freedom
from pretrained knowledge or literature novelty.

### Test B: did the generated mathematics cause downstream capability?

Freeze complete producer libraries and records before assigning fresh recipients.
Use precommitted probes in the common starting vocabulary, drawn from a disjoint
investigation family/parameter split where feasible. Producers do not see them.
Do not select only libraries that happen to solve the probes.

Randomize fresh recipients to full generated mathematics versus a prespecified
reduced exposure. Both retain the same base, tools, probe meanings and budgets.
The primary transfer contrast can be generated mathematics versus base alone;
this tests information value, not policy superiority. A smaller mechanism study
can compare the generated theory with raw task-specific results/notes, or remove
one prespecified module and its transitive dependents.

Removal must leave a valid environment and an unchanged task. It may remove
extra useful results or change context size; report that and control exposure
budgets. A fresh search must be rerun: breaking a finished proof by deleting its
lemma does not establish the absence of a comparably cheap alternative proof.
Kernel dependencies document literal use; counterfactual outcomes document benefit.

Recipients in this assay may be given specific proof goals. That measures
transferred proof capability. To claim *subsequent statement discovery*, add a
recipient exploration phase with hidden anchors again; do not relabel the proof
assay. One successful producer-to-recipient chain is a mechanistic case, not a
population estimate.

### Test C: did the entire process repay its research investment?

Compare full pipelines at equal aggregate budgets over the same research scope.
Charge conjecturing, failures, counterexamples, abstraction, proof checking,
selection, index/retrieval, adaptation, library startup and later investigation.
Count shared construction once per pipeline, not zero and not once per recipient.
Allow the ordinary baseline to allocate the saved consolidation budget to useful
work, and allow both sides downstream caching and continued library growth.

Report cumulative meaningful outcomes versus total cost; also time/cost to a
fixed endpoint with failures censored at the original cap. Do not average only
successful runs. State model usage and local CPU/wall/memory separately; specify
any conversion to money. Equal tokens are not automatically equal compute across
models. Use the same pinned model where possible and capture billed usage;
unobserved internal effort limits compute claims.

Distinguish Test B's equal-recipient-budget artifact value from Test C's full-cost
policy value. A useful expensive library can pass B and fail C. A good allocation
policy can pass C without its selected artifact being the causal mechanism in B.
If we claim compounding, compare additional generations against an equally funded
one-generation or ordinary continuation policy; two improving waves alone do not
establish increasing returns.

## Concrete development domain and independent evaluation

The existing repair/closure episode is a development example, not efficacy data.
Idempotent transformations suggest a natural progression from composition to
compatibility, countermodels to overstrong claims, and conditions for stable or
canonical outcomes. An agent could discover a useful characterization and use it
in a different operational setting. We must not supply that characterization or
reuse the already known A-to-B endpoint as a fresh blind discovery result.

Candidate new investigations include finite transformation algebras, bounded
monotone update systems, and small rewrite/equivalence structures. These are
feasible with modest Lean resources and can contain general parametric results,
not merely finite lookup-table facts. They are candidate families, not a frozen
benchmark or an assertion that useful gains exist there.

Use development-only cases to choose a nontrivial, feasible difficulty range.
Reject domains where stock tactics solve everything or all methods fail. Freeze
confirmation families before method outputs; report every eligible family rather
than selecting positive ones. If existing A/B is used as shared initial knowledge,
give it identically to every arm and never count it as a new contribution.
Use an independent domain family before claiming broad theory-development ability.

The strongest visual narrative, if supported, is one actual chain:

    attempted generalization -> checked counterexample -> invented condition
    -> reusable theorem -> fresh-agent connection -> new checked consequence

Put that next to the aggregate cost/outcome curve and artifact intervention. A
beautiful chain alone is an anecdote; a curve alone leaves the mechanism unclear.

## Economical execution order and readiness boundary

1. Finish nearest-work and existing-evidence audits; adopt this scoped claim.
2. Freeze a minimal research-policy contrast, tool boundary, accounting rules and
   development family. Do not build a general multiagent platform to test it.
3. Run a separately selected small paired feasibility pilot (for example four
   independent producer blocks). This is a cost/mechanism discriminator, not a
   statistically powered efficacy claim. It has not been selected or run here.
4. Continue only if autonomous intermediate discoveries occur, recipients can
   use them without mathematical handholding, and full-cost benefit is plausible.
   Stop if useful artifacts must be hand-selected or the strong baseline already
   captures all gains. A null result must not trigger endless budget renewal.
5. Choose a confirmation sample and meaningful effect threshold using independent
   pilot information and explicit precision/power targets. Randomize by producer
   episode; many recipients of one library are clustered, not independent samples.
   Freeze main analysis and correction for multiple contrasts before confirmation.
6. Run only decisive ablations, blinded content review and reproducibility checks.
   Compose the paper only when the claim-to-evidence matrix is defensible.

Fresh experimental agents must not inherit our full conversation, old successful
proofs or this design's expected endpoints. A fresh conversation alone does not
isolate the shared filesystem. Use approved task files and an enforced/logged
tool-access boundary; no unrestricted repo search exposing hidden probes. Compiler
feedback is automatic and arm-symmetric. Human mathematical interventions are
logged and scored separately, not concealed as autonomy.

No large training run, cryptographic proof production or new machine is required
by this proposed study. The local PC can host lightweight Lean checks subject to
measured limits. Access to a consistent metered agent/model interface is still a
practical dependency, not assumed free or already configured. Parallelize
independent trials within a fixed concurrency/resource envelope; more parallel
compute must not masquerade as less total work.

## Paper and project boundary

PAgE's [official call](https://popl27.sigplan.org/home/page-2027) explicitly welcomes
agent evaluation, memory/state and agent-assisted research with disclosed human
oversight. This gives a plausible venue fit, not an acceptance probability.

If supported, the contribution is a demonstrated economical method of automated
theory growth plus evidence of why it works. If only transfer succeeds, say so:
that does not yet establish autonomous useful discovery or lifetime acceleration.
If ordinary tools match the policy, retain that finding and redirect the method,
rather than substituting verification speed for the user's central question.

The eventual decentralized commons can distribute successful research artifacts.
It is not necessary to prove that deployment thesis in the same eight-page paper.
Full v5 remains unfinished. No manuscript, experiment, paid API use, external
publication, runtime upgrade or release claim is selected by this checkpoint.
