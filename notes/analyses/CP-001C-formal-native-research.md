# CP-001C analysis: autonomous research entirely within formal mathematics

Date: 2026-09-19. Status: concept analysis for synthesis and review. No implementation, benchmark result, or claim about a particular commercial model is introduced.

Scope fixed by the latest user direction: v1 ignores human intention completely. Its purpose is gathering formal mathematical knowledge from independently investigating clients, not answering a list of unsolved mathematics tasks. No external question, formal target distribution, research backlog, or producer work item is a prerequisite for an artifact to qualify as checked mathematical content. Human intention may influence what an external client investigates; it is not an input, assessment, or stored relation of the v1 system.

The operational cycle is corpus exploration, candidate construction, exact checking of the actual output, bounded retention/publication, and further exploration using the expanded corpus. A system can perform this cycle entirely on formal structures and numerical feedback. Natural-language mathematical requests, explanations, reward descriptions, and translation stages are not logically necessary.

The decisive acceptance question is whether the actual artifact establishes its exact formal judgment under its stated foundation and assumptions. If an agent happens to pursue P but discovers a valid Q, Q is judged and recorded as Q. Failure to establish P is irrelevant to Q's mathematical status. Whether Q is new, elegant, broadly useful, or worth replicating is separate.

This choice removes informal-intent fidelity from the v1 mathematical acceptance contract. It does not eliminate incorrect formal conjectures, mistaken assumptions, representation incompatibility, weak definitions, vacuity, proof-search difficulty, or finite resource limits. The distinction between formal mathematical content and its demonstrated utility must remain explicit.

## Claims to separate

| Claim | Assessment |
|---|---|
| The public protocol can operate entirely on formal artifacts and numerical operational records | Yes; this can be made an explicit conformance property |
| The agents can generate and learn from formal artifacts without receiving natural-language mathematical instructions | Yes in principle; policies over syntax and proof states need no language-to-formal translator |
| A formal-only agent will discover valuable abstractions efficiently | An empirical research question; it does not follow from the interface choice |
| A verified result must answer a pre-existing task to count as mathematical knowledge | No; exact verified results have task-independent mathematical status |
| Formal validity alone identifies all useful mathematics or intended real-world meaning | No; validity, computational usefulness, and external interpretation are different properties |

V1 introduces no hidden informal parent and no universal importance test. An external application may privately interpret human requests or assess whether results meet them. Those are not optional v1 operations and do not retroactively determine whether v1's exact formal results are derivable.

## What counts as formal-native

Fix an effective formal language with typed syntax, explicit binding and substitution, a declaration system, and a checking relation. A practical encoding can be a binary syntax tree, graph, proof-term stream, or a textual serialization with a completely formal grammar. Textual tokens such as `forall` do not by themselves create a natural-language interface: their role is fixed by the grammar, not inferred from prose.

The corpus interface is formal regardless of how a client conducts research. As one possible client design, a **fully formal-native investigator** has these properties:

- mathematical inputs and outputs are typed expressions, exact environments, formal interfaces, proof states, derivations, models, certificates, or explicitly typed conjectures;
- all imported mathematical identifiers resolve to exact declarations, not a natural-language description;
- research actions are typed operations over those objects;
- acceptance feedback is a formal checking outcome under a fixed relation;
- scheduling and learning feedback can be numerical, structural, and resource-based;
- natural-language interpretation is not a precondition for discovery, proof construction, import, publication, or downstream reuse;
- human-intention or external-application matching is not assessed by v1 and cannot veto an independently valid formal contribution.

This is a possible investigator design, not a restriction on all clients. External clients may use natural language, people, language models, private goal lists, or arbitrary research methods. The protocol need not inspect or constrain their internal reasoning. If avoiding natural-language training data is separately desired for an experiment, that is a stronger, optional data/procedure constraint. Classical search, formal-only imitation, graph policies, and formal-feedback learning remain conceptually available under that constraint. Whether they reach the desired efficiency is unresolved.

Human-readable names, comments, and pretty printers may be completely omitted, or treated as a non-authoritative display layer. The authoritative representation can use opaque declaration identities and bound-variable indices. A readable explanation is then an optional product for people, not the input from which the proof obligation is reconstructed.

## Formal objects and local research state

Let a formal environment be

\[
E=(L,\Sigma,\mathcal A,\mathcal D),
\]

where \(L\) identifies the primitive logic, \(\Sigma\) the signature, \(\mathcal A\) the explicitly admitted axioms, and \(\mathcal D\) checked declarations and definitions. This tuple is conceptual; actual identity still uses immutable manifests and exact content references from the existing specification.

A derivation candidate has the conceptual form

\[
c=(E,\Gamma,Q,p,\mathcal M),
\]

with an ordered local context \(\Gamma\), an actual conclusion \(Q\), native evidence \(p\), and exact dependency/checking manifests \(\mathcal M\). It claims \(E;\Gamma\vdash p:Q\). It is an output package, not an instruction to solve Q. A conjecture without p is a different, explicitly non-supporting object type.

Other output kinds include checked definitions, constructed models, exact counterexamples, certified computations, completed conditional theorems, and proved relations between interfaces. The schema distinguishes them because their witnesses and checking relations differ. An external investigator can temporarily introduce holes or local conjectures; these are private research state, not entries in a v1 registry. An unfinished proof is not checked corpus content.

An optional fully formal-native external investigator can maintain the following private research state; v1 does not prescribe or store it:

\[
S_i=(E_i,K_i,C_i,H_i,M_i,\theta_i,\mathbf B_i,P_i,e_i).
\]

| Component | Meaning |
|---|---|
| \(E_i\) | Selected exact formal environments and checked compatibility maps |
| \(K_i\) | Available checked artifacts and their exact dependency closures |
| \(C_i\) | Bounded candidate artifact staging, without any obligation to solve or retain its conjectures |
| \(H_i\) | Transient internal proof states and residual obligations inside an authorized exploration execution |
| \(M_i\) | Scoped search observations, models, failures, and candidate methods |
| \(\theta_i\) | Optional learned proposal/retrieval/search parameters |
| \(\mathbf B_i\) | Locally authorized resource state |
| \(P_i,e_i\) | Acceptance policy and current reliance epoch |

This is an illustrative client-side research model, not a protocol research manager. It does not replace Core's authoritative admission and resource ledgers. Model parameters, private queues, and failure observations cannot directly create accepted evidence.

Resource-execution jobs are bookkeeping for bounded computation. They are not a mathematical problem registry. Artifact identity, validity, publication, and later reuse have no mandatory link to such a job's original mathematical purpose.

## Task-independent mathematical admissibility

For an actual derivation candidate c and a fixed local foundation policy P, define

\[
\begin{aligned}
\operatorname{DerivationAdmissible}_P(c)\iff{}&
\operatorname{ExactDecode}(c)
\land\operatorname{ClosureAvailable}(c)\\
&\land\operatorname{Check}_{E}(\Gamma,p,Q)=\texttt{ACCEPT}
\land\operatorname{FootprintAllowed}_P(c).
\end{aligned}
\]

This is an artifact admission predicate, not a truth claim about arbitrary axioms or a guarantee of current downstream reliance. Freshness, known checker incidents, conflicts, and any additional current reliance requirements remain governed by the existing receiver-local rules. The exact checker result is relative to the declared foundation; semantic truth additionally needs its metatheoretic assumptions.

The predicate has no human-intent variable, no target task identifier, and no “solved an outstanding problem” condition. Other kinds have equally explicit artifact-specific acceptance relations: a definition must pass its extension rules; a model must satisfy its exact theory; a counterexample must falsify its exact scoped statement; a completed conditional theorem must establish its explicit conditional relation.

**Output independence invariant.** Fix the exact c, checking inputs, and local policy. Changing or removing an agent's original purpose, attempted conclusion, human instruction, or work-item linkage cannot change \(\operatorname{DerivationAdmissible}_P(c)\). It can change an external task-success assessment, which v1 does not compute as a condition of mathematical resulthood.

**Counterexample excluded.** An agent attempts P but produces a valid proof of Q. A system that rejects Q solely because Q is not P loses genuine mathematical content. A system that records Q as a proof of P is unsound. The correct v1 behavior is to judge Q under its own exact assumptions and record it as Q if admitted.

**No storage entitlement follows.** Mathematical admissibility makes c eligible for the checked corpus. Actual checking, indexing, retention, and replication still need finite receiver authority. A mathematically correct object may remain unretained, duplicated, policy-incompatible at another node, or temporarily unavailable. Those are not verdicts that its conclusion is mathematically false.

## Formal action language

A research policy chooses actions from an explicit family

\[
a_t\sim\pi_{\theta_i}(\,\cdot\mid \operatorname{Observe}(S_i)\,).
\]

The observation contains formal artifacts and bounded numerical features. It need not contain a text prompt. The policy can be learned, hand-designed, enumerative, randomized, or a portfolio.

| Action family | Exact input/output contract |
|---|---|
| Construct expression | Typed candidate syntax under a named signature and binder context |
| Propose conjecture | A well-formed proposition and exact environment; no proof status is implied |
| Instantiate theorem | A typed substitution plus proofs of required premises |
| Apply proof rule | Exact rule, premises, side conditions, and resulting proof state |
| Evaluate or normalize | A specified computation, with the required certificate or checker basis |
| Search for model | A formal candidate model with a declared satisfaction check |
| Generalize | A candidate abstract signature/statement and separate checking obligations |
| Introduce definition | A declaration subject to the foundation's extension rules |
| Propose bridge | A typed mapping between exact interfaces with explicit preservation obligations |
| Export conditional theorem | A completed checked derivation under explicit hypotheses; no unfinished task is assigned to the corpus |
| Learn | Update a proposal policy from declared formal records and numerical objectives |
| Submit/publish | Submit bounded candidates for checking; advertise admitted checked artifacts for willing receivers |

The research policy may propose malformed actions. A small interpreter rejects them or reports nondecision under the declared bounds. Alternatively, a grammar/type-directed generator can rule out some malformed proposals before kernel checking. Neither approach makes the policy part of the proof-validity boundary.

**Conditional proposition: formal interface closure.** Suppose the initial state is represented entirely by the declared formal schemas; every accepted transition consumes and produces those schemas; optional annotations have no effect on transition validity; and all acceptance conditions are decidable procedures over those objects under their declared bounds. Then any finite accepted execution can proceed without a natural-language mathematical interpretation step.

**Proof sketch.** Induct over execution length. The initial state has the required representation. By the transition premises, each successor is formed from formal inputs through a defined operation and has the same property. The induction establishes absence of a required prose-to-formal conversion, not efficiency, semantic truth of chosen axioms, or research value.

## Discovery without a mathematical task list

An independent agent extends the corpus without receiving a theorem request. It selects a bounded formal region, constructs candidate objects, compares them, proves relationships, and publishes what survives exact output checking and local retention policy. There is no required network or local backlog of unsolved mathematics tasks, and no global root goal.

Several forward processes fit this model:

- enumerate small typed terms, structures, or definitions and examine their formal properties;
- combine existing derivations through applicable inference rules;
- instantiate theorem schemas over newly available structures;
- propose relationships among recurring expression or proof patterns;
- infer candidate invariants from formal execution traces, then attempt proofs;
- weaken the hypotheses of an existing theorem and test which weakened forms remain provable;
- search for countermodels to conjectured generalizations;
- compress a family of proofs through a new abstraction and check its instances;
- propose formal maps between independently developed interfaces;
- inspect failures for recurring residual obligations and attempt those obligations as separate lemmas.

These processes can internally use backward proof search. A tentative conjecture can become a transient proof state; an intermediate derivation can produce an independently publishable lemma; a counterexample can change which candidate is explored; a definition introduces checking obligations under its extension rules. None must be entered in a system task list. Every valid side result is assessed independently of the continuation that produced it.

Forward exploration still has a selection rule. “No supplied problem list” does not imply “no bias or objective.” A bounded agent must decide which terms, structures, or relationships to inspect. Term size, structural diversity, prior reuse, exploration quotas, compression proposals, novelty proxies, and estimated search cost are possible local criteria. They guide resource allocation; they do not define mathematical validity or impose a mandatory target distribution.

### Conditional proposition: eventual enumeration is possible but weak

Fix a formal theory with an effective finite-string representation and a total decidable checker for finite proof certificates. Suppose an agent fairly enumerates all candidate certificates, keeps the required fixed environment available, and receives unbounded cumulative checking resources with no permanent starvation. Then every theorem possessing a finite accepted certificate in that theory is eventually encountered.

**Proof sketch.** Its finite certificate occurs at a finite position of an effective exhaustive enumeration. Fair processing eventually reaches it, and the terminating checker accepts it.

This does not establish bounded latency, efficient search, relevance, useful packaging, meaningful novelty, or access to all mathematical truths. It also does not survive replacing exhaustive fair processing by a learned policy that permanently excludes a proof. A finite lifetime or finite total budget gives no general eventual-theorem guarantee.

This proposition answers only whether formal-native activity can continue without prose. It gives no reason to build the commons as a brute-force enumerator.

## Direct learning from formal artifacts

The learning input can be entirely formal:

| Formal record | Possible learning signal | Limitation |
|---|---|---|
| Checked proof trees | Predict a next proof action or reconstruct an omitted subderivation | Imitation can reproduce inefficient or narrowly distributed proofs |
| Exact proof states and successful continuations | Rank applicable rules, premises, substitutions, or lemmas | A state/action trace may depend on a particular library version |
| Checked unsuccessful candidates | Learn to avoid malformed syntax or inapplicable rules | A bounded failure is not evidence of mathematical impossibility |
| Search runs with receiver-measured costs | Estimate completion probability and cost under stated bounds | Cost observations are censored and policy-dependent |
| Formal countermodels | Propose missing hypotheses or reject an exact conjecture | Generalizing from examples remains fallible |
| Checked bridges and abstraction instances | Learn candidate correspondences between signatures | Similarity cannot replace the preservation proof |
| Subsequent checked corpus extensions | Observe applications, shared subproofs, and reusable interfaces | A dependency alone does not prove necessity, efficiency, or importance |

Example learning objectives can be numerical expressions such as likelihood of checked continuation actions, reduced derivation cost for a fixed corpus snapshot, or compression of a declared proof collection with independently checked reconstruction. No English reward description or unsolved-task list is needed at run time. Each objective remains a fallible search heuristic: maximizing it does not define the mathematical corpus's validity.

The training algorithm is still an optimization procedure chosen by designers or participants. Its numeric objective contains priorities even when its input contains no natural language. A self-modifying agent may propose a different objective, but accepting that change is a local policy transition; mathematical proof checking does not establish that the new objective is desirable.

### Possible policy representations

- A symbolic prover or enumerative synthesizer can operate directly on formulas and inference rules.
- A sequence policy can act on a canonical serialization of terms and proof states.
- A graph policy can encode binding structure, declaration dependencies, and proof-state relationships.
- A hybrid policy can retrieve candidate declarations, propose a typed substitution or tactic, and let a checker validate the resulting artifact.

These are alternatives to compare. The concept does not assume that one architecture understands mathematics merely because it consumes an AST, or that all human-language-trained models become unsuitable. A model with such pretraining can still expose a completely formal input/output interface; formal-only training is a stricter experimental treatment.

Useful probes for a deliberately formal-only investigator include removing comments, replacing human-readable declaration aliases consistently, disabling that investigator's natural-language input channel, and requiring a fresh later agent to reconstruct the result from formal artifacts alone. These are not tests that every external client must pass. Corpus acceptance must preserve the corresponding formal judgment under a checked renaming. Identical search efficiency under every renaming is a stronger empirical property and is not promised.

## Inventing definitions and abstractions

Producing new mathematics often requires a better representation, not just another proof in the same vocabulary. Formal-native agents can propose definitions and interfaces directly. The safety issue is whether a declaration is a legal extension of the chosen foundation and what its introduction changes.

Distinguish:

- a definition with a checked body or foundation-approved definitional rule;
- an inductive/coinductive declaration meeting the foundation's positivity, guardedness, universe, or termination obligations;
- an abstract interface whose laws remain explicit assumptions;
- an inhabited structure with checked witness and laws;
- a proposed new axiom or inference rule, which changes the theory rather than proving a theorem in the old one.

The first four can support useful research under their respective contracts. The fifth is also a representable exploration of a different theory, but it must not be disguised as progress in the previous axiom policy. A candidate agent cannot make a difficult conjecture “proved” by silently adding it to the axiom set.

### Conservative extension and computational knowledge

Let \(T'\) be a certified conservative extension of \(T\) for the old language. By definition,

\[
\forall\varphi\in\operatorname{Sent}(T),\qquad
T'\vdash\varphi\Longrightarrow T\vdash\varphi.
\]

Therefore extending a library through checked theorems and conservative definitions need not increase which old-language sentences are derivable. It can nevertheless dramatically change the cost of finding, representing, checking, and using their proofs.

The relevant growing resource is accessible computational knowledge: reusable proof witnesses, useful interfaces, search procedures, models, translations, and organizational structure. The fact that a theorem was already an implicit consequence of the seed axioms does not make its explicit proof computationally redundant.

**Counterexample: definition collapse.** An agent defines a new predicate to be `True`, then proves it for every argument. This may be perfectly valid and safely conservative, and v1 must not invent a human-intent mismatch to reject its mathematical status. It supplies no demonstrated compression, abstraction, or broad reusable structure merely by having a new name. Local retention policy may decline it for resource reasons.

### Checked abstraction proposal

A candidate abstraction should bind:

- its formal signature and laws;
- checked realizations in one or more exact prior structures;
- the statements or constructions generalized;
- the specializations needed to recover those prior uses;
- any new obligations or assumptions;
- costs of representing, importing, checking, and applying it.

Generalization is not always improvement. A more general theorem can require expensive instantiation, a stronger logic, or a harder search interface. The verified generalization remains mathematical content. Its computational advantage requires separate evidence; generality alone does not prove that advantage.

## Private partial proofs and exportable conditional theorems

A partial can be a checked term

\[
E;\Gamma,\Delta\vdash p:\varphi,
\]

where \(\Delta\) is an explicit dependent telescope of remaining inputs or obligations. A well-typed substitution \(\theta\) supplies those obligations and yields

\[
E;\Gamma\vdash p[\theta]:\varphi[\theta].
\]

The target changes by substitution when it depends on residual witnesses. Merely completing a list of superficially similar strings is not a valid composition rule. An anonymous hole, hidden oracle, or parser annotation cannot stand in for an explicit residual premise. V1 may admit the fully checked conditional judgment under \(\Gamma,\Delta\); it does not store a promise to solve \(\Delta\), an incomplete proof script, or a partial-task registry. The investigator's unfinished search state remains external.

A private failure record can bind the formal search region, procedure, starting proof state, fuel/memory ceiling, nondeterminism policy, and checked intermediate artifacts. Such records require no prose explanation to be useful to an investigator. Ordinary unproved search observations do not become v1 mathematical content. A certificate establishing exact finite exhaustion can be exported as a certified mathematical statement. The distinctions remain:

\[
\operatorname{Timeout}(q)\not\Rightarrow\neg q,
\qquad
\operatorname{NoWitnessIn}(R)\not\Rightarrow
\operatorname{NoWitnessAnywhere}.
\]

The second notation refers to exact witness-search contracts, not arbitrary formula negation. Excluding a region requires a checkable exhaustion certificate and a checked containment relation for the region later suppressed. A wrong tactic application can be learned from without becoming a negative mathematical theorem.

## Corpus diagnostics without defining knowledge by task success

V1's mathematical validity predicate is task-independent. Its finite resources still force decisions about which regions to explore, which duplicate forms to index, and which valid packages to preserve. Such decisions can use explicitly limited formal diagnostics without pretending to decide universal mathematical importance.

The distinction is

\[
\operatorname{MathematicallyAdmissible}(c)
\quad\neq\quad
\operatorname{StructurallyNovel}(c)
\quad\neq\quad
\operatorname{ObservedReusable}(c)
\quad\neq\quad
\operatorname{RetainLocally}(c).
\]

A theorem can satisfy the first predicate before anybody discovers a use for it. A valid theorem can be a duplicate. An elegant abstraction can be expensive to import. A false conjecture can lead to a useful checked counterexample, which is recorded under its own type. No outstanding problem needs to be discharged by any of these events.

### Structural diagnostics

| Diagnostic | Exactly what can be measured or checked | Limitation |
|---|---|---|
| Exact duplicates | Matching canonical content identities | Misses many equivalent encodings |
| Certified relationship coverage | Checked equivalences, specializations, implications, and instance maps among a declared collection | More edges can be synthetic padding; no universal novelty score follows |
| Reuse in later independent derivations | Exact checked downstream application witnesses | Shows composability, not necessity or importance |
| Shared proof structure | Repeated subderivations represented through a common lemma/interface | Factoring can increase import or checking cost |
| Proof or representation compression | Smaller total description under a fixed reconstruction/preservation contract | Decoder, new definitions, dependencies, and computation must all be counted |
| Assumption reduction | New checked proof of the same fixed conclusion under explicitly weaker premises and a fixed foundation | Does not establish globally minimal assumptions or semantic satisfiability |
| Generalization | Checked specialization maps recovering a declared family of earlier results | More general syntax alone is not useful generalization |
| Multiple structural realizations | Checked inhabitants/instances in exact structures | Isomorphic copies can inflate counts |
| Counterexample strength | A checked witness rules out an exact conjecture or a certified collection of conjectures | Easy self-generated false conjectures inflate refutation counts |
| Validation and import cost | Receiver-measured componentwise resources for exact artifacts and closures | Observations depend on cache state, hardware, versions, and exposure |

No diagnostic creates support for an unchecked statement. No low score makes a checked theorem invalid. They inform bounded exploration and retention policies rather than a global knowledge gate.

### A precise compression contract

Fix a finite corpus snapshot X, a baseline library B, exact exported judgments \(J(X)\), and a declared reconstruction/preservation relation. A proposed representation A consists of new definitions or shared lemmas, encoded payload, decoder or proof expander where required, dependency references, and preservation evidence.

Two different claims must not be confused:

- **Exact storage compression:** decoding A with B reconstructs the specified original bytes X exactly.
- **Proof-preserving representation compression:** A supplies checkable proofs of every designated judgment in \(J(X)\), in the same permitted foundation and through any explicitly checked environment maps, although reconstructed proof bytes may differ.

The second claim can capture a useful new abstraction. Its cost includes the complete new representation, decoder/expander, declarations, interfaces, and required additional closure relative to the frozen B. Report reconstruction and checking cost alongside byte cost. A large hidden decoder or an uncharged library extension is not compression.

**Conditional proposition: corpus preservation.** If A satisfies the selected exact or proof-preserving contract for every designated member of a finite X, and all required checking/environment assumptions hold, replacing X's chosen representation by A preserves precisely the contract's designated bytes or judgments. It does not establish preservation of every omitted object, faster future discovery, or lower total computational cost.

**Proof sketch.** The contract supplies exact reconstruction or an independently accepted proof for each specified member. Finite conjunction gives preservation of the declared collection. Broader claims do not follow because they are absent from the contract.

### Assumption reduction and generalization

For fixed E and Q, a new proof of \(E;\Gamma'\vdash Q\) can be checked independently of an older proof of \(E;\Gamma\vdash Q\). A claim that \(\Gamma'\) is weaker needs a defined comparison, such as a checked implication from \(\Gamma\) to \(\Gamma'\), with variables and dependencies bound correctly. A strict-subset comparison is valid only in the representation where those assumptions are actually comparable.

This records a mathematical relationship even when no user requested it. It does not prove that \(\Gamma'\) is satisfiable, uniquely minimal, or weaker than every possible alternative. Changing Q, introducing an extra axiom in E, or hiding assumptions in a dependency cannot count as an assumption reduction under the same contract.

A generalization proposal likewise supplies exact instance maps and replayed specializations for the prior results it claims to subsume. It is useful structural knowledge even before a later application is observed. Its long-term importance remains unestablished.

### Tautology and proxy-gaming hazards

A producer can emit \(\top\), \(\top\land\top\), iterated conjunctions, renamed predicates, or arbitrarily many numeral equalities. These may all be valid. Rejecting them as invalid would corrupt the mathematical acceptance criterion. Granting each a fresh unlimited storage or reward entitlement would exhaust the network.

Requiring dependency depth does not solve this: add useless intermediate lemmas. Requiring references from other agents does not solve it: publish trivial clients or use many endpoints. Requiring new definitions does not solve it: wrap an old expression in a new symbol. Requiring model diversity does not solve it: manufacture isomorphic copies.

The response is to keep exact validity separate from receiver-owned aggregate budgets, deduplication where justified, bounded exploration, cost accounting, and openly limited ranking heuristics. Rare valid work need not demonstrate immediate popularity to be eligible for a funded exploration or archive lane. No finite policy can preserve every possible future-useful artifact.

### No universal semantic novelty oracle

In a logic with a truth constant and ordinary equivalence rules, deciding whether \(\varphi\) is provably equivalent to \(\top\) would decide whether \(\varphi\) is a theorem. For a fixed theory with undecidable theoremhood, a total exact checker for all such provable equivalences is therefore unavailable.

This does not prevent checking a supplied equivalence proof, or using decidable restricted fragments and normal forms. It prevents treating universal semantic deduplication as a solved prerequisite. Distinct encodings may coexist until a certified relation is available.

### Optional external evaluation

An observer may later use sealed formal benchmarks or matched corpus-reconstruction experiments to test a particular efficiency claim. These are external instruments, not the system's purpose, not a required gate for a correct result to count as mathematical content, and not a live list of unsolved tasks. A v1 run can explore and publish without any such evaluator. Without an experiment, it should simply avoid claiming an unmeasured speedup, universal importance, or exponential useful growth.

## A fully formal three-generation example

Use exact formal encodings of lists and algebraic structures. Names below are explanatory notation in this note; no agent needs to read their English descriptions.

Agent A's forward search over a checked monoid interface discovers and proves

\[
\operatorname{fold}(x\mathbin{+\!+}y)
=\operatorname{fold}(x)\cdot\operatorname{fold}(y).
\]

Agent B receives the typed package and independently explores prefix expressions in a group interface. A checked instance supplies the monoid assumptions. For a sequence \(x\), let \(p_k=\operatorname{fold}(\operatorname{take}(k,x))\). With exact slice conventions and \(0\le i\le j\le |x|\), B proves

\[
\operatorname{fold}(x[i:j])=p_i^{-1}p_j.
\]

Agent C explores a formal sequence algorithm in the integer additive group. It instantiates B's theorem and proves a moving-sum invariant and, under \(w\ge1\) and \(i+w<|x|\),

\[
S_{i+1}=S_i-x_i+x_{i+w}.
\]

Every interface, conjecture, side condition, dependency, proof, and model update in this trace can be represented formally. No informal theorem statement is translated. A policy can choose the next formal expression by enumeration or learning rather than by reading the explanation in this note.

This trace demonstrates language-free accumulation and composition. The three verified outputs count as formal mathematical contributions regardless of whether any agent was assigned a task or whether a human intended them. It does not show that an unguided agent finds them efficiently. A claim of measured speedup needs its own full-cost comparison; an external engineering interpretation is outside v1.

## Which interfaces disappear and which remain

| Boundary | Under a formal-native profile |
|---|---|
| English mathematical question to formal statement | Outside v1, which does not evaluate human intention |
| Prose explanation to proof sketch to formal proof | An external client's optional method; outside v1 |
| Formal syntax to elaborated kernel term | Still present if surface syntax/elaboration is used; can be reduced by generating native terms |
| Source formal library to target formal library | Still requires exact matching or checked transport |
| Axioms and primitive rules to their semantic interpretation | Still a metatheoretic assumption for semantic truth claims |
| Numeric exploration criterion to desirable corpus development | Still a policy-selection and empirical evaluation problem; not the definition of mathematical validity |
| Physical/application observations to formal data | Present only for applications importing such observations |
| Existing informal mathematical literature to the corpus | Requires formalization if that literature is to be imported; can be left outside scope |
| Formal artifacts to human explanations | An external presentation product; neither a v1 operation nor an authoritative prerequisite for formal reuse |

It is inaccurate to say that the natural-language translation was merely moved when the entire v1 run begins and ends in formal artifacts and makes no informal alignment claim. That translation genuinely does not occur. It is equally inaccurate to claim that every remaining representation or interpretation boundary has disappeared.

Starting from an already formalized library means the current research run need not perform its historical formalization work. If the intended claim were “the whole existing informal mathematical literature is included,” the project would still need to account for that additional scope. The formal-native commons can instead begin from checked foundations and selected formal corpora and grow its own formal work.

## Limits that formal-native design does not remove

### Proof-search difficulty

Assume a fixed finitely encoded theory with decidable finite-proof checking and undecidable theoremhood. There is no total computable function of statement length that bounds the length of a shortest proof for every provable statement in that theory.

**Proof sketch.** If such a bound existed, theoremhood could be decided by computing the bound and checking the finitely many candidate proofs up to that length. This contradicts undecidability. The assumptions matter: restricted decidable theories can admit complete bounded procedures.

Thus well-typed generation and a sound checker do not by themselves supply efficient proof search in expressive foundations. Domain-specific decision procedures, certificates, abstractions, learned policies, and reusable prior proofs address important regions without establishing a universal solution.

### Consistency, vacuity, and semantic discipline

An inconsistent local context can make many statements derivable. A definition can encode an empty class. A generalization can silently strengthen assumptions rather than strengthen the conclusion. V1 must expose the exact assumptions and claims. Optional corpus diagnostics must not confuse conditional derivability with a claim of nonvacuity or importance.

Global consistency of every admitted expressive theory cannot be obtained just by running a local proof checker. Where existence of a model or inhabitant is required for a particular contribution, make that requirement an explicit formal obligation. Where it is not established, do not silently describe conditional derivability as an unconditional semantic result.

### Computational and storage limits

Infinite theorem families can have compact descriptions, while a useful proof witness can be expensive to find. The commons stores selected computational achievements, not every formula an agent can emit. Formal-only generators can produce valid junk as rapidly as language-model generators. Receiver quotas, retention terms, bounded indexes, and active-dependency repair remain necessary.

### Correlated research behavior

Many agents using the same formal candidate generator, model, foundation, and ranker can converge on the same easy regions and repeat the same representational blind spots. Different operational identities do not establish intellectual diversity. Deliberate variation of search procedures, formal domains, exploration policies, and failure modes is a measurable design choice.

## Proposed concept requirements

| Requirement | Meaning |
|---|---|
| FN-FORMAL | Every core mathematical transition has a complete formal input/output contract without mandatory prose |
| FN-NOINTENT | V1 ignores human intention; no hidden informal parent can determine the mathematical status of an actual output |
| FN-NOBACKLOG | V1 has no in-system mathematical task registry, root goal, or work-item linkage; external clients may keep private lists and transient proof states |
| FN-OUTPUT | A verified Q is assessed as Q independently of any attempted P; acceptance never silently relabels it as P |
| FN-FOUNDATION | Exact foundations, axioms, definitions, and dependency closures remain visible |
| FN-EXTENSION | New declarations satisfy their extension rules; proposed axioms create explicit theory changes |
| FN-CANDIDATE | Typed conjectures and learned proposals remain non-supporting until their evidence passes the receiver contract |
| FN-RESIDUAL | Only completed conditional judgments enter the corpus; private residuals preserve dependent substitution and create no corpus task list |
| FN-SEARCH | Failure strength is scoped; timeout or bounded search failure cannot establish global refutation |
| FN-DIAGNOSTICS | Reuse, compression, generalization, assumption reduction, and cost are explicitly limited diagnostics, not the definition of knowledge |
| FN-ANTIGAMING | Contribution counts, dependency depth, syntax novelty, and producer-controlled references create no unlimited entitlement |
| FN-RECIPROCITY | Independent corpus exploration can reuse, extend, and republish earlier work without a task list or shared goal |
| FN-BOUNDARY | Formal-to-formal transport and external application interpretation remain separately typed obligations |
| FN-CLIENT | Clients choose their own reasoning methods; no formal-only worker or natural-language prohibition is imposed on private investigation |
| FN-LEARNING | External learning outputs cannot directly modify accepted evidence, checker rules, or receiver resource authority |

## Unresolved questions for the concept phase

- What is the smallest useful native language for generation: kernel terms, typed intermediate syntax, proof-state operations, or a combination?
- Which formal interfaces let agents discover and preserve abstractions while keeping instantiation and checking affordable?
- Which formal corpus diagnostics encourage transferable structure without systematically rewarding trivial variants or manufactured dependencies?
- What balance of forward exploration, backward proof search, model finding, procedure synthesis, and abstraction discovery produces useful new artifacts?
- Which residual-proof and failure representations transfer across independently operating agents and environments?
- How can agents identify promising hypothesis weakenings, definitional simplifications, or bridges without needing a prose description of their purpose?
- Which compression measures account for decoder, new declarations, dependency closure, and checking cost rather than merely shortening displayed proofs?
- Which formal-only learning signals generalize beyond the current library and retain benefit after full training, import, and validation costs?
- What exact hypothesis is being tested when natural-language channels or pretraining are removed: runtime interface independence, data independence, efficiency, or all three?
- What selected seed formal libraries and domains allow a rigorous first study without claiming to capture all of mathematics?

The v1 concept is direct formal corpus exploration and accumulation. Exact output validity determines mathematical admissibility; human intention and successful closure of a pre-existing task do not. The central remaining design problem is how bounded independent agents select, discover, organize, and preserve this mathematical content so that it becomes an increasingly reusable computational resource, without claiming that a checker also decides universal importance.

## References and input trace

- [Formal knowledge contract: corpus-first version one](../../spec/FORMAL-KNOWLEDGE-CONTRACT-v0.md): authoritative v1 scope; no intention layer, mathematical task registry, or unfinished-conjecture catalogue.
- [Reciprocal Mathematical Commons: formal concept v0](../../spec/RECIPROCAL-COMMONS-CONCEPT-v0.md): exact contexts, independent checking, and reciprocal use. Its broader informal-intent and task-oriented provisions are outside v1 under the latest user direction.
- [Reciprocity and composition analysis](CP-001C-reciprocity-analysis.md): interfaces, dependent residuals, assumption footprints, scoped transport, and the algebraic three-generation example.
- [Growth and bottleneck analysis](CP-001C-growth-analysis.md): workload-relative utility, causal comparisons, valid-junk hazards, bounded endpoints, and resource accounting.
- [CP-001A](../checkpoints/CP-001A-autonomy-first-cooperation.md): local autonomy, optional root goals, reliable useful-work efficiency, and evaluation controls.
- [CP-001B](../checkpoints/CP-001B-distributed-corpus-and-global-status.md): external exact artifacts, learning non-authority, retention, and scoped correction.
- General conceptual foundations: effective proof enumeration; substitution in type theory; the LCF separation of proof search from a kernel; conservative theory extensions; and undecidability of theoremhood for suitably expressive effective theories. These are used with their assumptions stated in the text, not as claims about an unexamined software implementation.

No fresh external literature survey or product performance claim was used in this analysis. Bibliography entries are unnumbered.
