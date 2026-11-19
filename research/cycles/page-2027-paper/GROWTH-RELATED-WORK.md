# Growth, reuse, and theory-development literature audit

Research checkpoint, 2026-10-24 America/Chicago. Owner: `page_growth_literature`.
This is a paper-viability audit, not a manuscript and not an acceptance forecast.
Primary texts were browsed; no software was installed, external repository
cloned, experiment run, or historical project evidence changed.

## Decision in brief

The broad proposed story is already occupied: verified growing libraries,
LLM-generated auxiliary lemmas, lifelong Lean retrieval, conjecture/proof loops,
interestingness-guided library growth, shared negative research memory, and
minimal general-purpose Lean agents all have direct predecessors. A paper cannot
derive substantial novelty from assembling these descriptions or showing that
one agent successfully imports another's theorem.

The current selected scientific objective is **accelerated mathematical
discovery**, not a verification-cost paper or a requirement to prove that
decentralization itself creates the gain. This supersedes the audit's earlier
fallback ranking. The most promising gap is a rigorous causal study: let agents
explore concepts without seeing later evaluation targets, freeze what they
create, and test whether fresh recipients gain meaningful checked capability
at lower whole-system cost. Ordinary durable Lean libraries and plain notes
must remain strong controls. Counterexample-guided scope/concept repair is a
candidate intervention, not an established new algorithm or a selected design.

This is a potentially valuable empirical contribution even if the loop stages
are familiar. It needs an attributable result, not a claim that nobody previously
combined definitions, proofs, refutations and reuse. No source inspected here
settles the proposed exact experiment; that bounded observation is not proof
that no competing paper exists.

High acceptance probability cannot be justified from a bibliography or an
attractive premise. What this audit supplies is a rejection-risk map and an
evidence gate strong enough to avoid drafting the wrong paper.

## Primary-source claim matrix

Publication status is stated only as established by the linked primary venue,
paper, or author repository. ArXiv dates are version dates, not acceptance dates.
Paper-reported findings below are not independently reproduced findings.

| Work and verified status | What it already establishes or investigates | Consequence for our claim |
|---|---|---|
| [LEGO-Prover](https://proceedings.iclr.cc/paper_files/paper/2024/file/85dca46374dc0f27b4bb5f265b3d17f0-Paper-Conference.pdf), ICLR 2024; [author code](https://github.com/wiio12/LEGO-Prover) | Growing verified Isabelle lemma library, retrieval, modular proofs, lemma evolution; miniF2F evaluation. | Neither generated-lemma accumulation nor retrieval-assisted improvement is new. |
| [LLM Library Learning Fails](https://arxiv.org/html/2504.03048v1), April 3, 2025 preprint; [author code](https://github.com/ikb-a/llm_lib_learning_fails) | Behavioral and compute-accounted reanalysis of LEGO-Prover. | Actual repeated reuse and cost-matched benefit are necessary evidence, not optional embellishments. |
| [LeanAgent](https://proceedings.iclr.cc/paper_files/paper/2025/hash/b67c77f8db8b991d73d6f2e16f491840-Abstract-Conference.html), ICLR 2025; [paper v8](https://arxiv.org/html/2410.06209v8), March 6, 2025; [author code](https://github.com/lean-dojo/LeanAgent) | Curriculum, dynamic database, progressive retriever training across Lean repositories; reports 155 completed proofs in 23 repositories. | Evolving Lean knowledge and cross-repository learning are established topics; avoid claiming to introduce them. |
| [Prover Agent](https://arxiv.org/html/2506.19923v4), October 23, 2025 preprint version | Coordinates informal reasoning, formal proving and Lean feedback; auxiliary lemmas include useful special cases rather than only explicit subgoals. | Generating helpful intermediate mathematical structure is not by itself a contribution. |
| [Conjecturing-Proving Loop](https://aclanthology.org/2026.naloma-1.5/), NALOMA 2026; [full paper](https://arxiv.org/html/2509.14274); [author code](https://github.com/auto-res/ConjecturingProvingLoop) | Iterative Lean conjectures/proofs; previous results and proofs condition later generation; theoretical sampling argument and matched-token experiments. | A parameter-free growing Lean library plus an experiment is already insufficient differentiation. |
| [DreamProver](https://arxiv.org/html/2604.26311), April 29, 2026 preprint | Wake-sleep abstraction and compact library refinement; separate training/test problems; reuse counts and library ablations. | Learned abstraction with later proof benefit is already a close competitor, not an unoccupied contribution. |
| [Learning to Discover Interesting Mathematics](https://arxiv.org/html/2609.28603), September 23, 2026 preprint | A proof-difficulty/description-length metric, downstream library-compression correlation, trained conjecturer, iterative promoted-theorem graphs. | Do not claim the first useful-interest metric, autonomous theorem promotion, or self-expanding Lean discovery loop. |
| [Learning Interestingness in Automated Mathematical Theory Formation](https://arxiv.org/html/2511.14778), 2025 preprint | FERMAT represents definitions/conjectures/theorems; EvoAbstract learns interestingness functions. | Target-free concept formation and learned search heuristics are occupied; function abstraction here concerns the heuristic program. |
| [Learning to Disprove](https://arxiv.org/html/2603.19514v2), October 14, 2026 preprint version | Trains formal counterexample generation using hypothesis mutation and multiple verified rewards. | Lean-checked negative knowledge itself is not a new contribution. |
| [Self-Supervised Theorem Discovery in a Formal Axiomatic System](https://arxiv.org/html/2606.28747), June 27, 2026 preprint | Starts from Hilbert-system axioms; extracts general/hard-to-reprove formulas and adds them as search actions. | Target-free discovery, lemma selection, and downstream reuse need a sharper distinguishing feature. |
| [Minimo](https://papers.nips.cc/paper_files/paper/2024/hash/4b8001fc75f0532827472ea5a16af9ca-Abstract-Conference.html), NeurIPS 2024; [full text](https://arxiv.org/html/2407.00695) | Joint conjecturing/proving from axioms in three formal domains, with difficulty and hindsight-learning signals. | Mathematical acceptance independent of human-provided problems is not new. |
| [DreamCoder](https://people.csail.mit.edu/asolar/papers/EllisWNSMHCST21.pdf), PLDI 2021 | Joint library-abstraction and neural-search learning across eight program-synthesis domains. | Concept creation, compositional abstraction and improved future solving have a substantial PL predecessor. |
| [Voyager](https://arxiv.org/html/2305.16291), October 19, 2023 preprint version; [ICLR paper](https://openreview.net/pdf?id=P8E4Br72j3) | Persistent executable skill library, open-ended curriculum and transfer to new Minecraft tasks/worlds. | The generic agent-library feedback loop is not distinctive; formal semantics and attributable benefit must matter. |
| [HipSpec](https://smallbone.se/papers/hipspec-cade.pdf), CADE 2013; [venue record](https://research.chalmers.se/en/publication/175485) | Theory exploration, counterexample testing and induction synthesize equational background lemmas. | New-theory support cannot be equated with inventing lemma discovery. |
| [QuickSpec](https://smallbone.se/papers/quickspec2.pdf), JFP 2017 per [institution record](https://research.chalmers.se/en/publication/246148) | Efficient testing-based equational theory exploration from a supplied signature. | Filtering redundancy and exploring useful laws are longstanding concerns; tests alone are not proofs. |
| [IsaCoSy](https://www.research.ed.ac.uk/en/publications/conjecture-synthesis-for-inductive-theories/), peer-reviewed journal article per institutional record; 2010 manuscript | Bottom-up inductive conjecture synthesis. | Historical prior art, not a newly discovered strategy. Full PDF was inaccessible in this audit; no detailed numerical comparison asserted. |
| [Hipster](https://arxiv.org/abs/1405.3426), May 14, 2014 preprint; [institution venue record](https://research.chalmers.se/en/publication/216678) | Isabelle theory exploration both without a particular goal and to discover missing lemmas during proof. | Optional local goals plus exploratory mode are well precedented. |
| [The TM System for Repairing Non-Theorems](https://research.monash.edu/en/publications/the-tm-system-for-repairing-non-theorems/), peer-reviewed 2005 paper | HR invents concepts separating supporting examples from countermodels; modified statements are proved with Otter. | Counterexample-guided conceptual repair is longstanding prior art, not a new philosophical invention. |
| [Computational Model of Lakatos-style Reasoning](https://era.ed.ac.uk/items/d76bcf70-a95d-4872-b999-3170d2f07316), 2007 thesis | Multiagent theory formation with distinct examples, communicated conjectures and counterexample-driven definition/proof revision. | Even the multiagent Lakatos framing needs a sharper contribution than its headline. |
| [Negative Knowledge as Failure-aware Shared Memory for AutoResearch](https://arxiv.org/html/2606.21024), June 19, 2026; ICML AI4Research workshop per [author repository](https://github.com/hch-wang/Negative_Knowledge) | Bounded typed shared failure records, separate curation, downstream adoption/rejection, retry and cross-task PDE evaluation. | Shared negative memory and reduced repeated dead ends are already explicit contributions elsewhere. |
| [Multi-agent Autoformalization of Tensor Network Theory](https://arxiv.org/html/2607.07857), July 8, 2026 preprint | Research-level Lean library development; blueprint, persistent counterexample/strategy memory, specialized agents and full-project API-cost accounting. | A multi-agent Lean case study with notes and new library content is not enough by itself. |
| [Numina-Lean-Agent](https://proceedings.mlr.press/v306/liu26gp.html), ICML 2026 | General coding agent plus Lean/MCP tools, theorem search and research-level formalization. | Do not artificially handicap the ordinary agent baseline. |
| [mini-Lean-agent](https://arxiv.org/html/2610.17331), October 12, 2026 preprint | Shell-only Lean agent; fixed-model/budget comparisons and a separate trusted final evaluator. | This is an especially relevant baseline design for evaluating added machinery. |
| [Let the Library Speak](https://arxiv.org/html/2610.09401), October 7, 2026 preprint | Applicability-aware method contracts, ranking analysis, and fixed-compilation-budget downstream proof evaluation. | Reusable proof methods and applicability-driven retrieval already have a direct recent competitor. |

## The strongest novelty and evaluation objections

### DreamProver closes the generic abstraction-and-transfer claim

Its inequality ablations report 104 solved problems for the full method,
76 without iterative optimization, 53 without clustering, 55 without a library,
and 61 for its retrieval variant. The text interprets excess low-level lemmas as
harmful, rather than presuming that a larger library always helps. Appendix B
reports training output tokens separately: construction is not silently absent.
The headline 48% saving is an inference-output-token comparison, not a complete
lifecycle cost estimate. The appendix's token-unit labels and the main figure
use differing scales; do not import their absolute cost figures without checking.
[Sections 4.2–4.4 and Appendices A–B](https://arxiv.org/html/2604.26311).

Our inference: there is no defensible broad novelty claim in clustering lemmas,
abstracting them, pruning the library or testing later proof success. A sharper
study would isolate target-blind concept creation and its incremental causal
benefit against equally capable ordinary persistent-memory exploration. We have
not audited its implementation or established benchmark-contamination claims.

### Concept invention and counterexample repair are not blank spaces

FERMAT's reported evaluation reconstructs human-selected mathematical entities,
with random, hand-written interestingness and evolutionary-policy baselines.
Its discussion explicitly reports redundant/vacuous entities and bottlenecks
where a large graph obstructs further use of a discovered concept. Appendix A.5
reports substantial CPU parallelism. This motivates, but does not establish,
our different question: does the discovered theory actually accelerate a fresh
recipient's investigation? [Sections 5–5.2 and A.5](https://arxiv.org/html/2511.14778).

The October version of Learning to Disprove evaluates counterexample search,
autoformalization errors and invalid proof steps. It distinguishes proving an
existential counterexample from verifying that a particular proposed witness is
used; it also records limitations of the auxiliary feedback. We must enforce
the exact witness and hypothesis scope if we reuse countermodels. These findings
do not establish its absence of every conceivable transfer experiment; the
inspected evaluations address the listed tasks.
[Sections 2–4, 6 and Appendix E](https://arxiv.org/html/2603.19514v2).

TM and HRL establish that conceptual revision guided by refutation, including
social/multiagent versions, predates LLMs. Their institutional primary records
were read; complete implementations and historical experiment details were not
audited. A contemporary Lean system may still contribute strong experimental
evidence and an executable reliable artifact. It cannot claim that adopting
Lakatos, generating definitions, or remembering checked failures is itself new.

### Reusable-looking artifacts do not demonstrate reuse

The 2025 LEGO-Prover audit finds no direct reused learned lemmas in its inspected
successful proofs and evidence against its operational soft-reuse hypothesis.
Its fixed-cost comparisons remove the apparent advantage over simpler prompting;
some expensive-model conditions use small subsets and the o3-mini matched-cost
comparison is incomplete. These are scoped empirical results, not a theorem that
all library learning fails. See sections 3–5 and limitations of the
[primary audit](https://arxiv.org/html/2504.03048v1).

Fair reading is important: the **final** LEGO-Prover paper itself already has an
approximate token-balanced appendix control. It reports 131M prover and 117M
evolver tokens, a no-library result of 53.2% at 189 attempts, and 55.3% with the
library at 100 attempts. Its main validation ablation is 55.3% versus 50.4%.
The earlier arXiv version differs; cite the final source rather than mixing
versions. Our critique cannot be “they never considered compute.” It must concern
stronger causal attribution and an appropriate deployment comparison.
[Final paper, Table 2 and Appendix Figure 5](https://proceedings.iclr.cc/paper_files/paper/2024/file/85dca46374dc0f27b4bb5f265b3d17f0-Paper-Conference.pdf).

Our own inference: a kernel dependency edge is stronger evidence of literal
mathematical use than a name occurrence, but still not evidence of *benefit*.
An agent can reference a cumbersome lemma unnecessarily. Removing a dependency
from a finished proof will make that proof fail even if an equally cheap
alternative proof exists. Dependency audits and counterfactual agent runs answer
different questions and must both be present for a causal reuse claim.

### Growth experiments already extend beyond miniF2F

CPL's evaluation starts with three anonymized general-topology definitions. It
runs each method 20 times to a 14-million-token budget and reports the chosen
intersection theorem in 5/20 CPL libraries versus 0/20 simple-loop libraries.
It also evaluates previous context. Its theory models resampling allocated to
fixed statements, explicitly ignoring context effects. Its `exact?` novelty
filter is an operational screen, not a decision procedure for mathematical
novelty. See sections 3–5 of [CPL](https://arxiv.org/html/2509.14274).

Our inference: merely replacing CPL's topology with our closure-style example
would be a weak paper. The new claim would need independent transfer,
semantic-scope safety, resource-accounted amortization, or a demonstrated failure
and repair that its single-library loop does not address. Anonymizing definitions
does not guarantee the model has never seen the underlying mathematics.

### Interestingness is not established by counts or compression alone

The September 2026 interestingness paper defines utility through expanded proof
length and direct citation counts. It reports Spearman correlation 0.756 after
excluding zero-user declarations. Its discovery loop generates 400 candidates per
round and promotes ten; comparisons include random, longest-proof and retain-all
promotion. Novelty/quality judgments partly use an LLM. Read sections 3.1–3.4 and
Appendix D of [the primary paper](https://arxiv.org/html/2609.28603).

Our inference: its utility and interestingness measures share a proof-length
factor; their correlation does not establish independent causal savings for
later agents. Nor does replacing shared lemmas by fully expanded proofs model
the strongest optimized local baseline. This does not invalidate the metric as
a heuristic. It means our potential contribution should measure the gap between
surrogate promise and *realized, full-cost, independent downstream use*, rather
than propose another unsupported scalar “mathematical value.”

### Negative knowledge is a crowded alternative, not an automatic rescue

The June 2026 shared-negative-memory paper explicitly compares fresh retry,
self-debug and curated failure records, and includes cross-task scientific
transfer. Appendix B distinguishes memory size from end-to-end tokens: reported
medians are about 56k for self-debug, 53k for depth-one negative retry, and 101k for
deep negative retry. Curation is charged and amortization is discussed. Its
records classify observations and suggested actions; this is not Lean-checked
universal refutation. [Primary text and appendix](https://arxiv.org/html/2606.21024).

TNLean independently records false statements/counterexamples and promotes
persistent lessons for later sessions; it reports a whole-library API-cost
estimate rather than treating all orchestration as free. See memory sections
C.2–C.3 and cost Appendix F of [the primary report](https://arxiv.org/html/2607.07857).

Our potential distinction is **checked portability of the negative claim's
exact logical scope**, not merely remembering failures. Even that needs a
nontrivial demonstrated consequence: prevent an invalid reuse of negative advice
while transferring a valid exclusion to a different concept investigation.
Without such a consequence, it is just a counterexample theorem plus storage.

### A minimal ordinary agent is a strong baseline

The October 2026 mini-Lean-agent preprint directly compares generic shell access
with specialized Lean machinery, fixes models and budgets, and validates final
artifacts in a separate pinned environment using Comparator. It records model
charges, rejects statement drift and extra axioms, and acknowledges a small
benchmark. Its numerical performance should not be transplanted to our machine
or model. [Primary methods, results, and reproducibility appendix](https://arxiv.org/html/2610.17331).

The method-contract paper also measures downstream proof success, not only
retrieval coverage, but explicitly says its intervention bundles selection and
contract content. Its ten-compilation budget is not a universal full-cost metric.
[Let the Library Speak, section 5.4](https://arxiv.org/html/2610.09401).

Our inference: compare the proposed contribution against an ordinary coding
agent with the same base model, library, shell tools, documentation and budget.
Do not select a crippled one-shot agent or count only successful Lean invocations.

## Distinguish six meanings of growth

These definitions are our analytical framing, not a claim of new mathematics.

1. **Corpus growth:** more declarations or bytes. Easy to measure and easy to
   inflate; not a primary success metric.
2. **Deductive growth:** more derivable old-language sentences. Adding proved
   lemmas to a fixed theory does not change its unbounded deductive closure.
   Conservative definitions add convenient vocabulary, not new old-language
   mathematical consequences. This is why theorem count is conceptually weak.
3. **Representational growth:** shorter descriptions, abstractions, new
   interfaces and transport maps. Valuable, but may simply move work into a
   definition or opaque artifact.
4. **Operational capability growth:** a specified agent can obtain more checked
   results, or the same results more cheaply, within a specified resource budget.
5. **Transfer growth:** one investigation's output improves another independent
   investigation rather than only its own continuation.
6. **Creative growth:** agents introduce or revise concepts and develop a
   connected body of consequences whose utility is evidenced outside the
   discovery episode. This need not imply historical priority or grand
   mathematical importance.

The paper should pick one primary meaning, probably operational transfer, with
creative growth as a demonstrated application. Human intention is not reintroduced
into mathematical acceptance by choosing an evaluation workload: experiments
must name the capability they measure even when the product has no global agenda.

## Candidate contribution directions and kill conditions

| Direction | Nontrivial question | Evidence required before drafting | Kill or redirect condition |
|---|---|---|---|
| Causal cross-agent theory transfer | Does the proposed sharing mechanism add net benefit over ordinary checked library exchange? | Fresh consumers; multiple later uses; honest whole-cost ledger; library-content and interface ablations; native/Git/Lake control. | Benefit disappears against ordinary import, or depends on giving the intervention extra mathematical answers. |
| Checked negative-knowledge transfer | Can a countermodel safely eliminate false generalizations and guide productive concept repair across independent sessions? | Exact scope witnesses; wrong-scope rejection; fresh sibling/descendant investigations; raw-note and theorem-library controls; curation cost. | Same gain comes from a plain note containing the checked theorem, or no genuine concept revision occurs. |
| Semantically safe low-cost checked-memory restoration | Can retained local trust cut repeated validation cost without creating unsafe cross-environment reuse? | Precise trust relation; adversarial mismatch controls; cold/warm separation; strong native/batched control; realistic end-to-end savings. | It only wins against the project's own unnecessarily expensive predecessor. |
| Evaluation/methodology contribution | Can apparent growth claims be separated into extra compute, repeated proof use, representation and real transfer? | Reproducible harness; several systems/mechanisms or a compelling concrete failure/repair; correct causal design. | Merely lists desirable metrics or repeats the 2025 LEGO audit on one hand-selected example. |

The restoration-cost row is retained as historical triage, not a current paper
selection. Do not switch to it without root/user reconsideration of the current
discovery objective. Do not commit to a full autonomous-mathematician training
campaign on this PC. A narrow, well-controlled discovery/transfer finding has
higher expected payoff. Existing local theories are *pilot instruments*, not
already sufficient evidence of generality or automated concept invention.

## A defensible evaluation design, if root selects the growth route

### Experimental unit and information boundary

The unit is an independent later investigation, not an individual lemma or a
tool call. Define a producer episode and a later consumer episode. The producer
must not be given the consumer's target answer. Freeze what the producer leaves
behind before exposing later tasks. Fresh consumers get only the selected
library/metadata and their own instructions, not the producer transcript or an
orchestrator's hidden hints. Existing replay scripts are useful functional
controls but cannot substitute for this independence.

Build a small held-out panel of investigations with at least two mathematical
families, several distinct consumer tasks, and both useful and irrelevant
contributions. Randomization/order should be specified before seeing outcomes.
Two tasks hard-coded to require one existing theorem demonstrate a possible use,
not estimated general benefit. Conversely, unconstrained “do interesting math”
prompts make outcomes incomparable and invite post-selection; independent
assessable task families are scientifically necessary.

### Minimal arms

- **Local-only:** same initial mathematics, ordinary agent, local search and
  self-produced lemmas; no later remote discovery.
- **Ordinary exchange:** producer artifacts available as normal pinned Lean
  source/library plus ordinary file search or notes. This is the crucial control
  against merely showing that sharing useful mathematics helps.
- **Proposed exchange:** identical available mathematics, but the proposed
  discovery/validation/negative-knowledge interface.

If the scientific claim is about creation of the reusable contribution rather
than its transfer mechanism, add an otherwise identical producer without the
proposed selection/abstraction method. Do not automatically double a campaign:
choose the contrast that answers the actual claim. An oracle useful-artifact arm
can upper-bound headroom; it cannot be the baseline or reported as deployable.

### Outcomes and causal checks

Primary outcome: completed independently checked capability at fixed whole-agent
resource budget, or resource to a fixed capability with failures censored and
charged. Secondary outcomes: exact cross-episode proof dependencies, eliminated
invalid proposals, useful concept revisions, query failures, import overhead,
proof-check cost, token categories, peak memory and elapsed time.

Measure the *effect of access* with paired or randomized fresh-run interventions.
Dependency knockouts of final proofs are supporting mechanism checks, not the
primary estimate. For negative knowledge, report false exclusions as a safety
failure separately from unproductive search. A valid strengthening of a refuted
claim must remain eligible unless the counterexample still satisfies its new
hypotheses.

Do not pool multiple dependent descendants as independent samples. Cluster by
producer/library episode; report per-task outcomes and intervals, not only one
aggregate percentage. Token and CPU costs are different resources: publish raw
counts and explicit weights if combining them. Price-weighted gains may reverse
when cached-input/output ratios or model prices change.

### Whole-cost boundary

For a fixed measured capability and declared cost unit, compute

\[
G(m)=\sum_{i=1}^{m}\bigl(C_{\mathrm{ordinary},i}
-C_{\mathrm{proposed},i}\bigr)-F-M(m),
\]

where `F` includes any *incremental* creation, curation, publication and setup
cost required by the proposed route, and `M(m)` includes retention, index/service,
failed queries and other incremental maintenance. Use incremental costs only
when both arms truly share the same expense; otherwise report total costs.
Do not charge an artifact twice, but do not give its invention to the experiment
for free. A fitted break-even reuse count is a conditional engineering result,
not an acceptance-rate argument or a theorem of inevitable useful growth.

The equation alone is accounting, not a novel theorem. A paper needs observed or
justifiably bounded terms, a plausible reuse regime, and an implementation that
actually realizes the promised information/trust boundary.

## Checked negative knowledge: exact scope of a possible formal result

If this route is selected, the strongest elementary soundness statement is:
given a checked witness `w` and proofs of `H(w)` and `not C(w)`, the candidate
`forall x, H(x) -> C(x)` is refuted. A revised candidate with hypothesis `H'`
may be pruned by the same witness only after checking `H'(w)` and the relevant
conclusion/interpretation. Exact symbols, universes, environment and definition
identities must be bound. Failed proof search is never a refutation.

This reasoning is standard and should not be marketed as deep new theory.
Counterexample-guided synthesis and invariant learning are older predecessors:
[Solar-Lezama's CEGIS account](https://people.csail.mit.edu/asolar/SynthesisCourse2020/Lecture10.htm)
and [ICE, CAV 2014 institutional record](https://experts.illinois.edu/en/publications/ice-a-robust-framework-for-learning-invariants/).
The question for our software is whether independently shared checked witnesses
remain safe and useful across *changing concept vocabularies*, without an
all-knowing curator. A new transport/checking design plus a demonstrated reduction
in repeated unproductive investigation might be a contribution. A JSON schema
and the elementary implication alone would not be.

## What the literature does not justify

- It does not justify a numerical probability of PAgE acceptance.
- It does not show our implementation produces net growth.
- It does not establish that the newest preprints' claimed results reproduce.
- It does not make a growing graph, a successful import, or a shorter proof a
  sufficient scientific result.
- It does not require cryptographic certification as the default; the important
  comparison is real user/agent cost under explicit trust assumptions.
- It does not prove decentralization improves discovery. Decentralization may be
  an availability/independence requirement while the experimentally attributable
  benefit comes from reusable content. Keep these explanations separate.

## Reading coverage and unresolved checks

Read primary methods/results relevant to the central distinctions in the final
LEGO paper and its critical audit; LeanAgent; CPL; the 2026 interestingness paper;
the 2026 Hilbert discovery paper; Minimo; Prover Agent; DreamCoder; Voyager;
HipSpec/QuickSpec; negative shared memory; TNLean; mini-Lean-agent; and method
contracts. Opened author repositories for LeanAgent, the LEGO audit and negative
memory to confirm artifacts/status, without cloning or executing them. Numina's
primary proceedings record was read, not its complete implementation. IsaCoSy's
full manuscript returned access denied. ICE's author PDF timed out; the official
institutional abstract establishes prior art but not a detailed comparator.

The bounded follow-up read DreamProver's method, experimental questions, main
ablations, limitations and cost appendix; FERMAT's methods, evaluation metrics,
discussion and compute appendix; and Learning to Disprove's task, rewards,
evaluation/limitations and witness caveat. TM/HRL are primary institutional
records only. Related platform reports Prove2Me, Agent Hunt and EinsteinArena
were inspected for comparison boundaries: case-study achievements are not
interchangeable with a fixed-agent, matched-total-cost sharing intervention.
These observations are not negative claims about uninspected implementations.

An additional relevant primary lead is [TheSy: Theory Exploration Powered by
Deductive Synthesis](https://arxiv.org/abs/2009.04826), CAV 2021 according to its
[publisher record](https://link.springer.com/chapter/10.1007/978-3-030-81688-9_6).
Its abstract describes deductive bottom-up lemma-library generation; HTML was
unavailable. Read the PDF if root chooses a new theory-exploration algorithm.

No source found in this targeted audit establishes the exact proposed combined
semantic-scope transfer protocol. **That is not proof of absence.** Before a
first/new claim, follow citations of the selected closest predecessor and inspect
the relevant current software interfaces. Do not spend time exhaustively auditing
every adjacent paradigm before selecting a single falsifiable contribution.

## Recommendation to the central agent

Keep the discovery objective and stop broadening this literature branch. The
closest-work gap worth testing is **causal, full-cost usefulness of target-blind
automated theory development for fresh recipients**, not generic library growth.
The decisive comparisons are:

- CPL establishes an iterative discovery setting; our added question is transfer
  beyond a continuing producer's own context.
- DreamProver is the closest reusable-abstraction baseline; our study must not
  rename its positive-library mechanism as a new result.
- The two interestingness approaches supply useful search surrogates; our
  outcome is actual independently checked downstream capability, not surrogate
  agreement or mere reconstruction of a supplied curriculum.
- Negative memory, formal counterexamples and Lakatos-style repair are all
  predecessors. A checked scope-repair intervention is optional and must earn
  its place against plain retained notes and ordinary theorem source.

Before manuscript composition, require a modest preregistered feasibility gate:
automated producer exploration introduces a nontrivial definition/abstraction or
repaired theory; its artifacts are frozen before withheld targets are revealed;
fresh recipients show reproducible benefit against an ordinary durable-library
agent under a complete cost ledger. Choose task families prospectively and keep
unsuccessful episodes. If it fails, change the intervention or workload for a
documented reason, then use a fresh holdout—not a retrospective success story.

An apparent gain over no sharing but no gain over ordinary durable libraries
supports a *content-sharing* result, not a novel transfer-interface claim. An
apparent gain only before producer/curation cost supports an amortization
hypothesis, not demonstrated net growth. A successful imported proof alone is
not discovery acceleration. These distinctions should decide the next action,
not a need to preserve every past component in the paper.

This recommendation leaves the whole deployable-v5 goal intact. The paper is a
bounded scientific contribution within it, not a substitute completion claim.
