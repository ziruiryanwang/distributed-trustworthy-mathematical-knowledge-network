# CP-001C analysis: Conditions for reciprocal and meaningful mathematical growth

| Field | Value |
|---|---|
| Date | 2026-09-19 |
| Status | Concept analysis for integration and audit; no implementation or empirical claim |
| Scope | Conditions under which independent agents improve a shared mathematical resource and obtain measurable benefit from it |
| Inherited baseline | CP-001A autonomous research and its evaluation ladder; CP-001B distributed exact memory and frontier-relative status |
| Primary distinction | Growth in useful mathematical capability is different from growth in the number of stored statements |
| Requested direction | Open participation, reliable local reuse and contribution, recursive accumulation, and no mandatory central server or root goal |

## Reading conventions

`Requirement proposal` marks a proposed obligation for a future specification. `Conditional claim` marks a mathematical implication whose hypotheses are stated. `Hypothesis` marks an empirical question. `Counterexample` identifies why a stronger claim fails. None of the proposed growth measures creates a network-wide utility, credit system, or acceptance authority.

This analysis adds no requirement that agents agree on the same research agenda. Its finite evaluation suites are observer instruments. They are not root goals, shared coordination scopes, or a canonical ranking of mathematics.

## What can meaningfully grow

There are at least five different quantities:

| Quantity | Operational meaning | Why it is insufficient alone |
|---|---|---|
| Generated volume | Statements, attempted proofs, and bytes emitted | Duplicates and tautologies can inflate it arbitrarily |
| Admitted evidence | Exact objects whose evidence satisfies some receiver's contract | Correctness does not imply relevance or affordable reuse |
| Accessible usable knowledge | Evidence discoverable, retrievable, compatible, and admissible within a receiver's budget | Depends on receiver, context, policy, time, and task |
| Mathematical capability | Ability to complete externally specified tasks reliably within resources | Depends on task distribution, solver, and evaluation design |
| Productive infrastructure | Definitions, reusable abstractions, procedures, mappings, counterexamples, and tools that improve future capability | Value is often delayed and cannot be inferred from immediate popularity |

The intended virtuous cycle is:

> Available checked work reduces the cost or increases the success probability of later independent work; some of that later work becomes available checked input to further independent work.

Every arrow in that statement is contingent. Publishing more objects does not establish any of them.

### Receiver-relative capability

Let \(\mathcal D\) be a declared distribution of exact task contracts, \(B\) a resource vector, \(P\) an acceptance policy, \(\sigma\) a fixed research procedure, and \(K\) a sealed knowledge interface. Define

\[
\mathcal C_{\mathcal D,B,P,\sigma}(K)
=\Pr_{q\sim\mathcal D,\,\omega}
\left[\operatorname{SuccessfulCurrentReuse}_{P,B}
\bigl(\sigma(K,q;\omega),q\bigr)\right].
\]

Here the success predicate requires the procedure to produce a contract-valid, currently usable support tree for the exact task within the resource vector. The probability includes the declared task and solver randomness; faults belong to an explicitly declared fault model. Existing CP-001A endpoints remain normative for its testbed. This expression explains their interpretation rather than replacing them.

The useful effect of access to an additional corpus \(L\) is the intervention

\[
\Delta_{\mathcal D,B,P,\sigma}(L\mid K)
=\mathcal C_{\mathcal D,B,P,\sigma}(K\oplus L)
-\mathcal C_{\mathcal D,B,P,\sigma}(K),
\]

where \(K\oplus L\) means a specified accessible interface, including discovery behavior and its costs. It is not a cost-free set union or an assumption that every object in \(L\) is accepted. All import, checking, storage, and search expense is charged.

`Counterexample: negative growth in usable capability.` Adding a million valid but irrelevant statements can consume retrieval, checking, or attention budgets and displace useful premises. A fixed heuristic solver can then have \(\Delta<0\), even though the set of valid available objects has increased.

`Conditional claim: ideal optional-access monotonicity.` Suppose an extended interface preserves every old action and its cost, offers additional actions that a solver can ignore, and imposes no mandatory new overhead. The supremum of success probability over all admissible strategies cannot decrease, because every old strategy is still available. This claim does not imply monotonic performance of an implemented heuristic, an actual distributed network, or a solver forced to pay maintenance costs.

`Requirement proposal G-CAPABILITY.` Report capability by task family and budget regime, alongside invalid acceptance, semantic-fidelity failure, availability, and each resource component. Do not require one scalar ordering of all mathematical contributions.

### Why theorem count is not a usefulness measure

From one checked theorem \(P\), agents may generate \(P\land P\), \((P\land P)\land P\), renamed copies, or arbitrarily many harmless syntactic variants. A theorem schema may also express infinitely many instances compactly. Neither emitting every instance nor deleting all apparently redundant instances is universally optimal: a specialized lemma can reduce expensive elaboration or search for a frequent task.

Exact byte deduplication removes identical encodings. Structural normalization removes some equivalences. Neither decides all semantic equivalence, mathematical novelty, or future usefulness in expressive foundations. Relations such as equivalence, implication, instantiation, and conservative extension should be explicit checked objects where available; heuristic clustering remains advisory.

`Requirement proposal G-COUNT.` Theorem count, dependency-edge count, downloads, agent count, and reuse depth are diagnostics. They cannot independently establish meaningful growth.

## Reciprocal contribution without mandatory exchange

The desired reciprocity is a system property, not a requirement that every user upload something before reading. A reader can benefit without contributing; a researcher can contribute a rare foundational result without receiving a prompt reciprocal benefit; a relay can contribute storage rather than theorems. Requiring a balanced exchange for each identity would introduce a different incentive and access policy.

For an artifact \(a\), distinguish:

- a producer's local evidence and publication attempt;
- a receiver's discovery of \(a\) and admission of its exact closure;
- actual use in a subsequent task;
- a causal benefit of having access to \(a\);
- subsequent publication of new reusable evidence.

These events need not all occur. Local work can be sound without publication, and publication does not entitle its author to another node's budget.

`Requirement proposal G-RECIPROCITY.` The framework must permit an execution in which independently chosen work at cell A is reused by cell B, B's new checked work is reused by cell C, and C's later work is reused by A, with every coordination scope absent. Each receiver performs its own exact admission, every expensive action has local authority, and each support tree is finitely grounded.

This temporal cycle of useful exchange is compatible with the prohibition on circular proof support. A future theorem cannot retroactively justify an unsupported earlier premise. In a rigorous test, all accepted evidence trees must bottom out in admitted axioms, primitive judgments, or checked evidence permitted by their exact contracts.

`Requirement proposal G-INDEPENDENCE.` Changing a producer's original purpose, political attribution, or participation in a research program cannot invalidate an otherwise admissible receiver-local reuse. Exact logical assumptions, toolchain bindings, operational authorization, and semantic-fidelity obligations remain relevant.

## What must hold at each reuse boundary

An existing result creates benefit only when a sequence of conditions succeeds. For a declared task opportunity, let \(E_1,\ldots,E_m\) denote, in order:

- potentially helpful exact evidence exists;
- its closure remains recoverable within the relevant time and cost;
- the receiver discovers a suitable candidate;
- formal assumptions and representations can be matched or translated with checked obligations;
- the evidence satisfies the receiver's current contract;
- import and integration fit the receiver's resource envelope;
- the research procedure actually uses it productively.

When every conditioning prefix has positive probability, the probability chain rule gives

\[
\Pr\!\left[\bigcap_{j=1}^{m}E_j\right]
=\prod_{j=1}^{m}\Pr\!\left[E_j\mid E_1\cap\cdots\cap E_{j-1}\right].
\]

The first factor is \(\Pr[E_1]\). If a prefix has probability zero, the joint event has probability zero; undefined conditional factors are not multiplied. This is an identity using conditional probabilities, not an independence assumption. Estimating a single generic "reuse probability" conceals distinct bottlenecks. A network with excellent theorem production and poor retrieval can have negligible useful circulation; so can a highly searchable corpus with incompatible definitions or missing proof closures.

The factors also interact with workload and scale. Adding agents can improve coverage while simultaneously increasing candidate noise and queue delay. Results measured at five cells cannot be extrapolated by keeping all factors constant at a million agents.

`Requirement proposal G-BOUNDARY.` Record bounded, receiver-local failure categories for missing closure, incompatible context, excessive import cost, negative retrieval, failed checking, semantic mismatch, and unsuccessful application. Absence of a result in an incomplete search is never a mathematical nonexistence claim.

### Break-even is receiver- and horizon-dependent

Let \(\mathbf c_{\mathrm{base},j}\) be the cost of receiver opportunity \(j\) without access to a candidate shared resource, and \(\mathbf c_{\mathrm{reuse},j}\) its cost with access, including discovery, failed candidates, fetch, local checking, and integration. Let \(\mathbf c_{\mathrm{publish}}\) and \(\mathbf c_{\mathrm{maint}}(H)\) include the incremental publication and maintenance cost through a declared horizon \(H\). Then an arm-level resource effect is

\[
\Delta\mathbf C(H)
=\mathbf c_{\mathrm{publish}}
+\mathbf c_{\mathrm{maint}}(H)
+\sum_{j\le n(H)}
\left(\mathbf c_{\mathrm{reuse},j}-\mathbf c_{\mathrm{base},j}\right).
\]

Do not count the same shared construction, check, storage, or repair repeatedly. Nor may a study omit producer work simply because it preceded the consumer task. A paired experiment must declare which costs are common, which are incremental, and where prehistory is charged.

The resource-Pareto claim requires the preregistered reliability and yield noninferiority gates and the specified componentwise resource rule. Summing CPU, bytes, review time, and tokens with a hidden price vector is not a substitute. An explicitly declared local economic model may choose a price vector for a local decision; it is not the network's definition of mathematical worth.

## Compounding and exponential growth: conditional models

### A bounded endpoint cannot grow exponentially forever

For fixed \(\mathcal D,B,P,\sigma\),

\[
0\le\mathcal C_{\mathcal D,B,P,\sigma}(K)\le1.
\]

Therefore no strictly positive constant exponential growth rate can hold indefinitely for that endpoint. A fixed finite test suite also has a bounded weighted task yield. A claim of exponential capability growth must name a different unbounded quantity or a finite time interval, and must explain why its measurement remains comparable over time.

Options include cost reduction on fixed tasks, expansion along preregistered difficulty families, growth in distinct externally demanded completed tasks, or improvement in the frontier of task difficulty versus resource use. None is a universal scalar for mathematics. Changing the task mix after seeing successes would make the trend uninterpretable.

### A branching model states assumptions rather than proving the vision

Suppose a controlled idealized model classifies productive contributions into a finite set of types. Let \(Z_n\) be the vector of newly useful contributions in generation \(n\), where generations are an observer's analytic grouping and have no protocol authority. Let \(M_{ab}\) be the expected number of type-a successor contributions generated per type-b contribution.

Under stationary offspring distributions and the model's branching assumptions,

\[
\mathbb E[Z_{n+1}]=M\,\mathbb E[Z_n].
\]

If the initial population reaches a component with a supercritical growth mode, the relevant expectations can grow exponentially when that component has spectral radius greater than one. The matrix must already account for discovery, availability, compatibility, successful production, admissibility, retention, and the definition of useful successor work. It is not the raw number of theorem references.

The assumptions are strong:

- successor work is not counted repeatedly when several predecessors jointly enable it;
- useful opportunities and sufficient complementary resources remain available;
- duplication, competition, and overlapping descendants do not invalidate the branching approximation;
- error, disappearance, and correction losses are represented;
- calendar time per generation is bounded for a claim about growth per unit time;
- the offspring distribution does not deteriorate as easy tasks are exhausted or attention becomes congested.

Even in a valid branching model, supercritical expected growth does not guarantee that each run survives. Mathematical results often require several complementary predecessors, violating the simplest branching assumption. A finite observed range with a good exponential fit does not establish any of these conditions indefinitely.

`Hypothesis H-COMPOUND.` Certain task families may exhibit a sustained finite interval in which prior shared results increase the rate of future useful results after full costs and correction losses. Establishing this is an experiment, not a protocol safety theorem.

### Capacity limits the observed rate

For a particular resource \(d\), let \(C_d(t)\) be available service per unit time and let \(c_{\min,d}>0\) be a lower bound on consumption of that resource for each separately counted completion event. Resource charges must be additive across those events: shared precomputation is charged once, not once per descendant. Let \(W_d(0)\ge0\) be a finite upper bound on pre-interval work credited to events completing after time zero. Then any execution satisfying this accounting convention obeys

\[
N(T)-N(0)
\le
\frac{W_d(0)+\int_0^T C_d(t)\,dt}{c_{\min,d}}.
\]

With bounded constant service and finite carry-in \(W_d(0)\), this bounds event count by an affine function of time. The carry-in is zero if there is no initial work in progress, or if only events whose full charged cost lies in the observation interval are counted. Omitting it would be incorrect when jobs do almost all their work before time zero and finish just afterward. This is an accounting bound for the specified event unit. It does not assert that one theorem schema cannot encode infinitely many cases, that mathematical insight has a fixed bit size, or that every family of proof tasks has a uniform checking cost.

A heuristic stock-flow model makes the bottleneck visible:

\[
\frac{dU}{dt}
=\min\{a(t)U(t),\,V(t),\,I(t),\,A(t)\}-\delta(t)U(t),
\]

where \(U\) is a stipulated measure of currently productive resources, \(aU\) is potential useful production, and \(V,I,A\) are validation, integration, and attention capacities converted to the same model-specific units. The loss term represents unavailability, obsolescence for the workload, and disqualification; it does not say that valid mathematics becomes false with age.

This differential equation is an explanatory model, not a measured law. An approximately constant positive net proportional rate is possible only while the capacity ceilings do not bind and the coefficients remain suitable. Saturation, linear accumulation, stagnation, or decline are all possible. Increasing the number of independent agents is an external resource expansion and must not be mislabeled as intrinsic algorithmic compounding.

### Information and recomputation

CP-001B's exact-recovery lower bound applies to the number of distinguishable retained corpus states. If the system promises exact recovery of one of \(2^U\) possible states from a retained representation alone, an injective representation needs at least \(U\) bits in the worst case, up to its encoding conventions.

It does not follow that every new theorem carries new independent information. For a fixed recursively enumerable proof system, one can enumerate all finite candidate proofs and their checked conclusions from a compact description, subject to that system's effective checking assumptions. The difficulty is obtaining particular useful results, bounded search, affordable proof reconstruction, choosing the intended corpus, and locating the right artifact in time.

Thus an efficient knowledge commons stores computational achievements as well as statements: proof witnesses, interfaces, executable certificates, selected abstractions, and indexes can save enormous search even when their conclusions are logically implied by a compact axiom set. A tiny enumerator is not an efficient replacement unless it meets the specified exact-recovery, latency, and resource contract.

No format or network can guarantee eventual proofs of arbitrary mathematical statements in a fixed effective foundation. Undecidability, incompleteness where applicable, and limited resources constrain the claim independently of decentralization.

## Protecting useful growth without closing exploration

### Correctness does not create a resource entitlement

A publisher can generate indefinitely many valid objects. Acceptance of one statement's evidence is separate from admission to expensive indexing, replication, repair, or permanent retention. Existing CP-001A and CP-001B demand, execution, and aggregate retention bounds are therefore necessary even in a mostly honest network: enthusiastic agents can overload the system accidentally.

`Requirement proposal G-ADMISSION.` Every receiving authority controls aggregate work and state, including valid objects, their hints, dependencies, descriptors, control records, and future maintenance. New identities, topics, or theorem variants cannot increase that authority's finite resource ceiling.

Resource limits must bound discovery's cheap path as well as proof checking. A proof bomb can be valid and still be too expensive for a receiver's contract. A timed-out proof attempt means insufficient established evidence, not a false theorem.

### Popularity can erase future value

`Counterexample: delayed foundational benefit.` A new representation has immediate import cost and no users. After several bridge lemmas it makes an entire difficult family simple. A policy that retains only artifacts with current reuse discards the representation before its benefits can appear.

`Counterexample: popularity feedback.` A ranker shows only popular results; those results receive more use; measured use justifies showing them again. A technically superior independent representation may never receive one evaluated opportunity.

`Requirement proposal G-EXPLORATION.` A receiver that claims continuing exploration must allocate a declared bounded service share to candidates selected independently of the dominant learned ranker. The policy may use a bounded eligible pool, randomized selection, age, topic coverage, or rotating curator sets. Selection still requires ordinary authorization and checking. No exploration policy grants global storage or usefulness guarantees.

If an eligible object has conditional selection probability at least \(p>0\) on each of \(n\) opportunities while it remains available and eligible, then

\[
\Pr[\text{never selected in those }n\text{ opportunities}]
\le(1-p)^n.
\]

This follows from the conditional failure bound and does not need independence. The difficult assumption is the uniform positive \(p\). In an unbounded growing pool, equal shares need not supply it; candidate expiry or unaffordability also breaks the premise. Thus the result is a scoped exploration guarantee, not eventual attention for every public submission.

Alternatives worth comparing are a bounded age-stratified reservoir, topic-specific exploration budgets, investigator-funded retention, an archival service with explicit terms, and user-maintained specialist collections. Each shifts costs and selection bias; none is a universal solution.

### Retention and abandonment introduce censoring

Observed reuse is conditional on survival, discoverability, and exposure. An artifact deleted after one week has fewer opportunities for reuse than one retained for a year. Treating "no recorded reuse" as "no future value" confuses censoring with evidence of irrelevance.

`Requirement proposal G-CENSORING.` Evaluations of retention policies report candidate cohorts, exposure, admission decisions, deletion times, missingness, availability, and the observation horizon. Future-use conclusions must remain conditional on these factors. If a correction or closure disappears, its absence is not evidence that it never mattered.

Demand histories and utility estimates should remain local advisory data. They are easily manipulated and do not change mathematical validity. Retaining descriptors while dropping a proof may preserve a lead, but it must not preserve an unsupported claim of strict reusability.

Under finite capacity no policy can preserve every object that an adversarial future query might require. The specification must choose an explicit retention service objective and allow unavailable results; CP-001B already states this impossibility.

## Compounding also amplifies defects

The same graph that spreads a powerful abstraction spreads a bad formalization, mismatched assumption, compromised checker, or poisoned toolchain. Ordinary untrusted agent errors should be caught by exact checking, but shared defects inside the declared trusted boundary can affect many accepted results at once.

Let \(W(x)\) be a declared observer's total weight of future reliance opportunities that transitively depend on a component \(x\), counted without double-counting repeated paths within the same opportunity. High \(W(x)\) gives that component high leverage for both productivity and failure. It is a risk diagnostic, not evidence that \(x\) is wrong or a reason to reject a sound theorem.

If multiple reviewers share a common failure with probability \(q\), and otherwise have independent false-acceptance probability \(p\), the illustrative probability that all \(m\) accept erroneously is

\[
q+(1-q)p^m.
\]

This formula depends on that mixture model. It shows why multiplying the number of agents does not eliminate a common-mode floor. In a real system, independence must not be inferred from different names, model instances, endpoints, or keys. A mathematical proof is not accepted by majority voting.

`Requirement proposal G-AMPLIFICATION.` Highly reused foundations and transformations need explicit assumptions, pinned checkers and environments, replayable closures, bounded correction propagation, and clear local freshness state. Independent implementation or kernel audits may reduce particular common-mode risks; they do not prove absence of all defects.

`Requirement proposal G-CORRECTION.` After a locally admitted relevant defect or exact opposing evidence, stale affected reliance fails closed at the local epoch transition before a potentially enormous descendant walk finishes. Clean alternative support remains eligible. During a partition, a cell must not claim awareness of unseen remote corrections. These are inherited safety conditions, not optional growth optimizations.

Semantic fidelity remains distinct from derivability. A completely valid proof of a weak or vacuous formal statement is not evidence that the intended research problem was solved. Semantic review, exact contracts, assumption visibility, and adversarial formalization examples remain necessary even when a kernel is sound.

SNARKs or recursive verification may eventually reduce the cost of proving that a specified checking computation accepted. They do not decide usefulness, repair a wrong encoded checker, supply a missing proof closure, or demonstrate faithful formalization. Their use must pass CP-001A's versioned adoption gates rather than silently expanding strict P0 acceptance.

## How to test compounding causally

### Preserve the existing ladder

The primary order remains:

1. An isolated local research procedure demonstrates useful checked work within declared resources.
2. Typed local memory is compared with the isolated procedure.
3. Passive cross-cell typed reuse is compared with local memory and the paired prior-artifact-blind profile.
4. Typed reuse is compared separately with raw shared storage.
5. Active coordination is compared with passive reuse.
6. Optional shared programs and central-service comparisons remain separate interventions.

No amount of exchange, apparent recursion, or network throughput can substitute for failure at the isolated capability gate. No coordination effect is inferred from comparison with an intentionally weaker local solver.

CP-001B's frozen/periodic/online-learning matrix is nested inside this ladder. A changed model is an explicit treatment. It is not an uncontrolled improvement added only to the network arm.

### Prospective benefit rather than retrospective credit

The useful question is whether a receiver with access to prior work performs better on later independent tasks. Whether a successful proof cites a popular artifact is a different question. A solver might cite an unnecessary lemma; conversely, a counterexample can prevent a wasted search without appearing in the final proof.

Existing CP-001A consumer-interface blinding estimates the effect of access, including downstream traffic and checking changes. Producer work and publication attempts continue and are charged in both arms. A content-only effect requires the separately defined shadow-traffic treatment.

`Requirement proposal G-CAUSAL.` Do not infer causal contribution, exclusive necessity, or additive credit from final dependency trees. Complementarity means two individually unhelpful artifacts can jointly unlock a result; redundancy means several artifacts can substitute for each other. Marginal effects depend on the available background corpus and order of intervention.

The study should use fresh later tasks committed before outcomes and withheld until autonomous knowledge snapshots and interfaces are sealed. Neither hidden weights nor treatment labels become live protocol inputs. Solver/model checkpoints, libraries, cutoffs, read interfaces, and training exposure remain fixed except for the named treatment.

### Extension for repeated useful circulation

After the original gates pass, compare preregistered temporal sharing policies while keeping solver, initial corpus, ordinary local work, faults, and arm-wide resource ceilings identical:

| Arm | Cross-cell access during the production phase | Question |
|---|---|---|
| Static sharing | Only an agreed prehistory snapshot is accessible across cells | What can one initial shared corpus achieve? |
| Continuing sharing | Later producer outputs become eligible through normal passive discovery and re-admission | Does ongoing circulation improve future work? |
| Continuing sharing with selected consumer access blinded | Production continues; designated cross-cell access is filtered by the external harness | Is the gain caused by access rather than a correlated change in producers? |

All outputs still undergo ordinary local validation. The dynamic-versus-static contrast measures the bundle of continuing availability, timing, discovery, and induced work changes. It does not identify a universal reproduction number or the individual value of every result.

An additional explicitly scoped experiment may admit successive cohorts of independently generated work and measure whether later cohorts benefit from earlier ones. Cohorts are experimental schedules, not required network rounds. Operational origin events may be needed to define treatment eligibility; this does not create political attribution or permanent author authority.

Declare interference blocks before execution. Shared descendants, training, caches, queues, and budgets can contaminate nominally separate task treatments. Randomization at a consumer-artifact edge alone does not remove network interference. Retain CP-001A's complete-replicate resampling rule for fixed-suite claims and its independent-workload-instance rule for population claims. Do not resample individual correlated tasks as if independent.

### What evidence would support a compounding claim

At a minimum, report:

- autonomous online and sealed future-task yield with the original reliability gates;
- fixed-budget capability by mathematical family and difficulty stratum;
- the marginal effect of continuing access compared with the frozen-corpus control;
- total and componentwise amortized costs over a declared horizon;
- reuse latency, failed import costs, and availability-adjusted exposure;
- beneficial partial, counterexample, or failure reuse even when absent from final proof trees;
- repeated cross-cell circulation under absent coordination scopes;
- correction loss and recovery after a high-impact seeded defect;
- minority-topic performance and bounded exploration opportunities;
- sensitivity to publication growth, task novelty, dependency fanout, hot foundations, and valid-junk load.

For an exponential-growth claim, additionally preregister the quantity, time interval, resource trajectory, generation-to-time mapping, comparison models, and decision rule. Compare exponential, linear, saturating, and changing-task-mix explanations. If per-unit-time resources also grow exponentially, report that fact and separate it from growth in useful yield per comparable resource budget.

A positive effect on one interval supports only that interval and declared population. A null or negative result is informative: it can locate a retrieval, interoperability, retention, integration, or local-capability bottleneck without falsifying every part of the architectural vision.

## Open choices requiring further specification

| Choice | Defensible alternatives | Unresolved condition |
|---|---|---|
| Primary contribution granularity | Native proof objects, reusable modules, certified procedures, or several typed forms | Cross-form usefulness without forcing one artificial count |
| Exploration | Random eligible reservoir, age/topic quotas, specialist curation | Adequate rare-topic exposure under fixed budgets |
| Retention | Local demand, term-funded archives, foundational collections, exact recomputation | Delayed value versus ongoing cost and disappearance |
| Representation diversity | One initial prover/environment; later certified interfaces | Import savings versus fragmentation and conversion cost |
| Trust diversification | Pinned small kernels, independent replay implementations, targeted foundational audits | Which common-mode assumptions are actually reduced |
| Learning | Frozen agents first; periodic or online proposal adaptation as separate experiments | Net capability improvement after training and regression costs |
| Growth endpoint | Fixed-task cost frontier, future-task yield, growing preregistered difficulty families | Comparable meaning across time and domains |

The critical next conceptual deliverable is a contract for useful circulation: an exact contribution can be discovered, checked, retained, and used by an independent receiver under explicit costs and failure assumptions, and the next resulting contribution can take the same path. The specification must guarantee the safety of this path and expose its failure states. Whether repeated traversal produces accelerating useful mathematics remains a measured hypothesis.

## Source trace

- [CP-001A: Autonomous research, trustworthy reuse, and optional coordination](../checkpoints/CP-001A-autonomy-first-cooperation.md): receiver-local usefulness; rootless operation; demand and resource invariants; prior-artifact blinding; the full evaluation ladder; strict validation-basis gates.
- [CP-001B: Distributed exact memory, indexed discovery, and frontier-relative status](../checkpoints/CP-001B-distributed-corpus-and-global-status.md): exact-recovery lower bounds; corpus/index/training distinction; retention and availability; growth accounting; common-mode and learned-ranker containment; nested learning experiments.
- [Reliable Mathematical Research and Reuse Testbed v0](../../research/COOPERATION-TESTBED.md): isolated capability gate; autonomous and sealed held-out endpoints; causal access controls; complete-replicate inference; fixed-budget claims; fault and overload regimes.

External literature has not been independently checked for this analysis. The probability identities and elementary counting bounds above are derived in the text. The branching model and continuous stock-flow equation are explicitly conditional analytic models; they are not claimed to describe the realized network.
