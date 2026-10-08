# DTMKN Reliable Mathematical Research and Reuse Testbed v0

## 1. Deliverable

Build and evaluate a local-first, federation-ready mathematical research and reuse testbed, not a production global network. It must answer, in this order:

1. Can the selected agents and tools actually produce nontrivial contract-valid mathematical results within explicit resources?
2. Can exact validation and repair prevent seeded invalid or mismatched results from entering stable reuse?
3. Does typed local memory and cross-cell reuse improve useful yield or cost?
4. What marginal benefit or overhead comes from active coordination and decentralization?

No shared root goal or research program is required. Coordination activity is never itself a success metric.

## 2. Components

### 2.1 Cooperation schema and blackboard

- theories, contexts, judgments, goal templates, standalone work items, optional coordination scopes, and decompositions;
- bounded publication hints, interest subscriptions, receiver-owned service classes, and local budget grants;
- a separate harness-only `EvaluationSuite` store that is outside the cooperation blackboard, wire schemas, live-node APIs, and participant-visible traces;
- attempts, checkpoints, partial results, failure capsules, demand reservations, unique execution claims, receiver-authoritative meter records, exactly-once local finalization/settlement actions, and nonauthorizing outbox intents;
- evidence, relations, justifications, assessments, and challenges, with morphism objects reserved for expansion fixtures;
- sharded ready frontier, artifact/support graph, failure atlas, and conflict inbox;
- bounded receive/quarantine/admit lifecycle;
- receiver-issued demand tickets, nonspendable public offers that claim into holder-bound tickets, and durable-promotion rules;
- distinguish replicas of one logical cell from independently governed federation cells;
- set-union anti-entropy only among crash-fault replicas sharing one admission authority, transactional ledger, schema root, validation root, and policy epoch;
- candidate exchange plus receiver-local re-admission between independent cells, even when they advertise identical policy roots;
- deterministic policy-scoped materialized views.

A logical cell's replica group is one administrative admission and ledger trust boundary. Direct set-union reconciliation assumes those replicas are crash-fault-only and share the exact authoritative ledger roots. Every other authenticated federation member is an independent cell, even if it advertises identical schema, validation, and policy roots, and its facts are candidates requiring receiver-local admission. Byzantine compromise of a configured replica-group admission authority is outside v0; containing it requires receiver revalidation or Byzantine replication and is recorded as a residual assumption rather than hidden by the word “cohort.”

### 2.2 Scheduler

- hard capability filtering;
- calibrated capability/cost estimation;
- local value/information/cost scoring;
- fixed authenticated cell membership, rendezvous-hashed object/goal/interest routing keys, bounded top-\(k\) cell routing, and v0 fallback that explores every one of the 3–5 cells before declaring no route;
- a frozen local pull/planner/decomposition/portfolio engine shared by every inferential arm; optional cross-cell leases, heartbeats, and work stealing only in named active treatments;
- finite receiver-assigned service/capability classes and protected validation capacity as the P0 contract; WFQ versus deficit round robin, aging, and exploration as frozen per-run mechanism choices;
- parent/child resource envelopes;
- receiver-issued permission/role capabilities with holder proof of possession, attenuated nonreclaimable fanout, and exact running-execution binding for protected resource actions;
- atomic idempotent grant-to-ticket and child-ticket issuance, nonreclaimable descendant-issue allowances, `ACTIVE | TERMINAL` tombstones, `RESERVED -> RUNNING -> FINALIZED` reservation execution, authoritative/conservative accounting, and root/child terminal ledgers;
- ephemeral authenticated leases, cancellation, validator roles, and budget changes;
- backpressure, overload response, cancellation, and circuit breakers;
- bounded strategy portfolios and tail hedging.

### 2.3 Knowledge integration

- exact-key, structural, certified-relation, and candidate-semantic retrieval;
- dynamic AND/OR justification graph;
- signed positive/refuting dependency requirements for support and refutation composition;
- checked counterexamples and bridge relations;
- manually supplied in-environment relation support as an expansion fixture;
- assumption-based truth maintenance;
- alternative-support-aware dependency impact;
- reliance epochs, dirty roots, fail-closed cached queries, and bounded resumable invalidation;
- failure-subsumption checks;
- explicit formalization-fidelity justifications;
- abstraction and refactor proposals with validation obligations as a later/ablation feature.

### 2.4 Validation

- one Lean 4 adapter;
- exact environment and dependency binding sufficient for replay;
- sandbox and resource limits;
- `ACCEPT | REJECT | ERROR | UNKNOWN` results with reason codes: declared invalidity/malformedness is `REJECT`, missing closure or bounded nondecision is `UNKNOWN`, and unexpected checker/sandbox/runtime/TCB-integrity failure is `ERROR`;
- axiom/dependency report;
- counterexample and relation-certificate checking for the chosen workload;
- reserved validation capacity isolated from generation load.
- least-fixed-point grounded support with cycle rejection;
- native validation-basis metadata and optional succinct-argument field;
- separate parser, unpacker, build, checker, agent, and checkpoint sandboxes;
- local admission of support, refutation, transport, and defect evidence.
- strict active reuse that excludes exact inconsistent judgments;
- strict proof and refutation closure in which exact state `(1,1)` closes neither polarity;
- target-side replay for every v0 transport relation;

### 2.5 Network emulator and simulator

- configurable authenticated cells, agents, rendezvous lookup, scoped pub/sub, gossip, CAS locality, logical-cell replica anti-entropy, and independent-cell candidate exchange;
- zero-scope autonomous publication/discovery/reuse plus optional coordinated-program modes;
- heterogeneous capability, cost, caches, bandwidth, and interest;
- churn, crash/recovery, delayed messages, partitions, flash crowds, and overload;
- independent and common-mode error clusters;
- malicious unique-object, decomposition, challenge, lease, index, cache, and capability-fanout floods;
- valid-tautology/context spam, publication-hint/key/provider floods, coordination-scope and service-class minting attempts, concurrent ticket redemption and execution claiming, malicious public-offer claims, multi-use namespace tickets, reserve/cancel and zero-work child-object loops, capability replay/execution rebinding, meter underreporting, terminal-allocation resurrection, poisoned top-\(k\), endpoint renaming, and an authenticated malicious independent member cell;
- cyclic support, forged acceptance, proof/archive/graph bombs, blackholes, and prompt/checkpoint injection;
- high-fanout defects, missing proof closures, and wrong/vacuous formalizations;
- crashes at reserve/claim/meter/check/inert-staging/local-finalization/outbox/external-effect boundaries, bounded crash-safe running-claim expiry, child issuance/terminalization, partitioned issuer recovery, atomic reliance-state/dirty-seed/epoch publication, ordinary opposite-polarity admission, and reordered reliance overrides;
- heavy-tailed runtimes and power-law dependency graphs;
- trace replay for deterministic comparison.

## 3. Workloads

### 3.1 Real Lean integration workload

The minimum vertical slice uses 2–3 independently organized Lean namespaces with deliberate overlap and different local definitions, 30–50 externally preregistered task contracts, and roughly 100–200 internal work items. The mandatory profile has no `CoordinationScope` objects and no common work-graph root.

Task releases are staggered. Early producer tasks are assigned independently across cells. Later consumer tasks at different cells have exact or translatable dependencies on some earlier artifacts, while other superficially similar artifacts are hard negative matches. Each cell has its own task stream, interests, budgets, retention policy, and stopping decisions. Benchmark weights and reuse labels exist only in the sealed evaluation harness. The workload covers:

- exact duplicates;
- syntactic variants;
- valid implication/equivalence/specialization relations;
- hard false-equivalence negatives with subtle assumption differences;
- valid proofs of deliberately wrong, vacuous, or assumption-strengthened formalizations;
- alternative proofs and shared sublemmas;
- partial proofs and residual obligations;
- checked counterexamples;
- scoped failed tactic/premise searches;
- a dependency incident with an unaffected alternative proof.
- prior artifacts produced for a different local purpose but reusable under a later receiver contract;
- overlapping and nonoverlapping interest subscriptions, disappeared providers, and decoy hints.

Before any federation run, the `Isolated capable agent` profile, using the same research engine and Lean adapter as every later arm, must complete a local no-network capability suite containing known-solvable tasks, known-invalid candidates, partial results, and semantic-fidelity traps. For capability task \(q\), freeze nonnegative weight \(c_q\), release time \(t_q\), and deadline \(d_q\). Normalize the endpoint as

\[
G_{\mathrm{cap}}=
\frac{\sum_{q\in Q_{\mathrm{cap}}}c_q\,
\mathbf 1[\exists t\in[t_q,d_q]:
\operatorname{Stable}_{P_{\mathrm{cap}}}(
\operatorname{RelianceQueryOf}(q);A_{\mathrm{cap}}(t),O_{\mathrm{cap}}(t))]}
{\sum_{q\in Q_{\mathrm{cap}}}c_q}.
\]

Require \(\sum_{q\in Q_{\mathrm{cap}}}c_q>0\). The preregistered minimum \(y_{\min}\), exact isolated profile, weights, deadlines, and resampling unit are chosen from a disjoint pilot and frozen before confirmatory runs. Failure of the one-sided 95% lower confidence bound for \(G_{\mathrm{cap}}\) to exceed \(y_{\min}\) blocks every mathematical-efficacy claim, regardless of network behavior. Invalid and fidelity-trap cases remain separate hard reliability gates and do not acquire positive capability weight.

Use a mixture of hand-constructed ground truth, existing Lean examples, generated candidates, and seeded errors. Record exactly which relations and supports are mechanically known.

Expansion-only fixtures, excluded from every minimum-slice exit gate and primary success criterion, add an interface theory with manually supplied certified in-environment relations and a repeated pattern for abstraction/refactor experiments. General morphism discovery and abstraction promotion are not v0 dependencies.

### 3.2 Real-agent deployment

Run a bounded heterogeneous population—8–16 actual/scripted workers for the minimum slice and 8–64 only after the local gates pass—using a mixture of:

- proof/search agents;
- decomposition/planning agents;
- retrieval agents;
- counterexample and critic agents;
- Lean checker workers;
- integration/repair agents;
- deterministic scripted agents for controlled cases.

The exact count depends on compute. The scientific result comes from controlled equal-budget comparisons, not a theatrical agent count. Agents receive no hidden evaluation-suite weights or cross-cell reuse labels.

### 3.3 Large-scale simulation

Simulate \(10^3,10^4,\) and \(10^5\) logical agents. Treat \(10^6\) as a stretch complexity run, not evidence about a real million-agent WAN. Logical agents use calibrated trace-derived distributions rather than one expensive model call each. Scale task events only after checking the simulator on held-out real-agent traces and publishing sensitivity ranges.

No operation may require an all-agent broadcast or per-agent state proportional to the full network.

## 4. Baselines

1. **Isolated capable agent:** the same research agent and exact local validator, but no persistent typed memory and no shared results.
2. **Local typed workspace:** persistent exact objects, support, action cache, and failures inside each cell, but no cross-cell exchange.
3. **Raw shared store:** agents share documents/embeddings but no typed work items, receiver re-admission, support graph, or failure semantics.
4. **Federated passive reuse:** publication hints, subscriptions, receiver-funded fetch, local replay, retention, and cross-cell reuse; no remote task assignment, remote/shared decomposition, cross-cell leases, work stealing, or coordination scopes.
5. **Federated passive reuse—prior-artifact blind:** paired with profile 4. Before outcomes, the harness assigns a preregistered artifact–consumer treatment set or interference-safe workload cluster. Producer work, local validation, retention, publication attempts, and their costs still occur in both arms; the blind arm filters the designated artifacts and hints only from the selected consumer discovery/read interface and exposes no treatment label. This estimates the total effect of consumer access, including downstream traffic and checking changes. A narrower content-only effect requires a separately preregistered shadow-traffic treatment.
6. **Federated active coordination:** exactly the same local planner, retriever, decomposition logic, bounded local strategy portfolio, validator, memory, and resource ceilings as profile 4. It enables only cross-cell work-item routing, exchange/adoption of remote decompositions, remote capability offers, cross-cell leases, work stealing, and remote portfolio orchestration. The primary active profile still has zero coordination scopes.
7. **Optional coordinated programs:** profile 6 plus explicit `CoordinationScope` objects. Any shared-budget escrow is carved from the same componentwise arm-wide ceiling as profile 6; it reallocates rather than supplements resources. A run with additional program resources is a separately labeled program-plus-budget bundle and is not an estimate of the program overlay alone.
8. **Central typed service:** the same typed memory, demand admission, validation, caches, support semantics, worker mix, and optional active mechanisms, but one scheduler/store.
9. **Central FIFO:** one queue with homogeneous workers.
10. **Oracle capability matcher:** exact global state on small traces only, reported as an upper bound rather than a deployable baseline.
11. **Naive global broadcast:** every task or hint advertised everywhere, for scale contrast only.

This factorial structure separates base research capability, exact validation, local memory, cross-cell passive reuse, active coordination, optional programs, and federation. Every inferential pair uses the same worker set, local research engine, checker, fixed initial corpus, task releases, random tapes, fault trace, and componentwise arm-wide ceilings; only the named treatment switches differ. Local decomposition and local portfolios therefore remain enabled in passive and active arms. A coordination mechanism is useful only through its marginal outcome after all messages, planning, retries, validation, and storage are charged. The federated design need not beat the central typed service under benign small-scale conditions; it must quantify federation overhead and resilience.

Ablations are divided before analysis.

**Nonconforming safety-negative controls** deliberately remove a P0 property: no exact action cache; no demand tickets/reservations; no backpressure; no receiver-owned fair-share/service-floor queues; or no truth maintenance. Each must fail its targeted conformance gate in the seeded trace and exists only to measure failure severity or mechanism cost. It cannot qualify for a release, safety, reliability, or liveness claim and is never presented as a deployable alternative.

**Deployable performance ablations** preserve every P0 contract while removing one optional or evaluative mechanism:

- no publication hints/subscriptions;
- no scheduler DAG-awareness heuristic, while exact support semantics remain;
- no failure capsules;
- no soft leases;
- no exploration bonus;
- no locality score;
- no active coordination (passive reuse only);
- no progressive routing exploration, with its weaker declared routing horizon;
- fixed-\(k\) checking instead of risk-aware allocation;
- homogeneous rather than diversity-requested replication, only where the reliance contract requires no diversity;
- no theory mappings (expansion-only ablation).

## 5. Quantitative objective

Separate participant-visible execution, sealed future inputs, and observer-only metadata:

\[
E=(A_0,\{\Lambda_{i\ell}\},\{\Sigma_i(t)\},F,B,\mathrm{RNG}),
\]

where \(A_0\) is the initial public corpus, \(\Lambda_{i\ell}\) are heterogeneous ordinary local task streams, \(\Sigma_i(t)\) are overlapping subscriptions, \(F\) is the fault trace, \(B\) contains resource ceilings, and `RNG` fixes paired random tapes. Sealed held-out query contents, their future release times, and their participant-visible budgets form a committed future-input object

\[
S_{\mathrm{probe}}=(Q_{\mathrm{probe}},t_{\mathrm{release}},B_{\mathrm{probe}}).
\]

The harness withholds \(S_{\mathrm{probe}}\) until its frozen release transition; after release, each query and visible budget becomes an ordinary participant input and therefore part of the visible execution. Changing probe contents or their visible budgets changes the experiment and is not a metadata-only intervention. Let

\[
M=(Q_{\mathrm{obs}},w,\ell_{\mathrm{probe}},v,
\operatorname{Contrasts},\operatorname{Analysis})
\]

contain only observer-side membership, weights, labels/groupings, contrasts, and analysis. Receiver-local scheduling priorities belong in \(E\), not \(M\). The required measurement-noninterference property is

\[
\pi_{\mathrm{protocol}}(\operatorname{Run}(E,S_{\mathrm{probe}},M))
=
\pi_{\mathrm{protocol}}(\operatorname{Run}(E,S_{\mathrm{probe}},M'))
\]

whenever participant-visible inputs, the sealed future-input object, faults, and random tapes are equal. Changing only \(M\) may change analysis output, never protocol messages or state.

All confirmatory usefulness objects live in a harness-only `EvaluationSuite`; the suite is not serialized to live nodes, not a protocol root, not a scheduler input, and not a global utility. In this document, `Stable(q;K)` abbreviates the Core predicate `Stable_P(RelianceQueryOf(q);A(K),O(K))`; `RelianceQueryOf` is the identity when \(q\) is already a query. Let

\[
\mathcal E_{\mathrm{online}}
=\{(i,q,w_q,B_q,t_q,d_q)\}
\]

be the preregistered set of receiver-local task contracts \(q\), observer weights, task budgets, release times, and deadlines, with \(t_q\leq d_q\leq T\). Each query enters through the ordinary local-work API with `coordinationScopeRef` absent; the live system receives \(q,B_q,t_q,d_q\), but not \(w_q\), reuse labels, or hidden dependency annotations. Local task priority is a separate participant-visible field. For system profile \(s\), define the autonomous online endpoint:

\[
A_s(T)=
\sum_{(i,q,w_q,B_q,t_q,d_q)\in\mathcal E_{\mathrm{online}}}
w_q\,
\mathbf 1[
\exists t\in[t_q,d_q]:
\operatorname{Stable}_{i,s}(q;K_{i,s}(t))].
\]

The protocol enforces each task's descendant ceiling \(B_q\) through its ticket lineage, and any ceiling violation is a hard gate rather than a post-hoc outcome adjustment. Costs shared across tasks are never inserted into the success indicator or charged repeatedly: descendant work is charged to its task lineage, autonomous prehistory and publication are charged once to their producing phase, and shared federation/checking/storage infrastructure is charged once to the arm-level actual resource vector \(\mathbf C_s\) under the common arm ceiling. Freeze any finer allocation rule before outcomes. Only the first contract-valid closure of a benchmark task counts. Internal lemmas, decompositions, attempts, messages, and theorem counts have no intrinsic evaluation value. They matter only through an externally scored task, held-out reuse, reliability, or a separately reported cost component.

Let \(\mathcal E_{\mathrm{reuse}}\) be the sealed held-out task set, with frozen weights \(v_h\), receiver assignments \(i(h)\), and per-task resource vectors \(B_h\). For each system \(s\), seal every receiver's autonomous-run knowledge snapshot and read-only interface \(K_{i,s}^{\mathrm{train}}\) before revealing held-out task contents. Run the same evaluator agents, code, seeds, fault schedule, and budgets for every profile; only the sealed knowledge interface varies. Define

\[
H_s=
\sum_{h\in\mathcal E_{\mathrm{reuse}}}
v_h\,\mathbf 1[
  \operatorname{Stable}^{\mathrm{reuse}}_{i(h),s}(
    h;K_{i(h),s}^{\mathrm{train}},B_h)].
\]

`Stable_reuse` means that the common evaluator produces an exact contract-valid finite support tree within \(B_h\), charging retrieval, validation, compute, storage, communication, and review normally. Evaluation-produced artifacts do not enter another task or profile during the confirmatory run.

To isolate learning from other cells, rerun the held-out evaluator with a snapshot selected by the preregistered rule that retains only artifacts available to the receiver without inter-cell import, including their exact retained closures. Define the secondary paired cross-cell reuse effect

\[
X_s=H_s^{\mathrm{all\ admitted}}-H_s^{\mathrm{local\ only}}.
\]

The selection uses operational cell events solely as an experimental treatment, not as authorship or credit. The main causal contrast for passive cross-cell reuse is nevertheless the full system comparison `federated passive reuse` versus `local typed workspace`, because snapshot filtering can alter dependency availability.

For diagnostic evidence-tree reuse, let \(T_q\) be the accepted closing tree:

\[
R_s(q)=
\mathbf 1[
\exists a\in\operatorname{nodes}(T_q):
t_{\mathrm{publish}}(a)<t_q
\land a\notin A_0].
\]

Cross-cell tree reuse additionally requires the test harness's operational `originCell(a)` to differ from the receiving cell. This diagnostic misses heuristic, counterexample, retrieval, and failure-capsule reuse that guides a new proof without appearing in the final tree. The paired prior-artifact-blind profile is therefore the causal reuse treatment; tree counts alone are not.

Compare systems under the same multidimensional arm-wide ceilings for model tokens, CPU, accelerator time, checker time, memory, retained bytes, network bytes, wall time, and human/operator review time. Let \(\mathbf C_s\) be actual consumption, reported separately in every dimension. For active coordination, publish the **net arm resource delta**

\[
\mathbf D_C=
\mathbf C_{\mathrm{active}}-\mathbf C_{\mathrm{passive}}
\]

componentwise and report Pareto dominance; do not call this entire delta direct overhead or hide it in a favorable scalar. Also instrument a direct coordination-overhead vector \(\mathbf O_C^{\mathrm{direct}}\) containing at least coordination message bytes, remote-planning compute, lease/heartbeat processing, work-stealing traffic, coordination-only retained state, and duplicated checking attributable to remote coordination. Equal ceilings may turn overhead into displaced mathematical work even when \(\mathbf D_C=0\), so report both yield and the direct categories. A secondary scheduler-analysis lens for horizon \(T\) is:

\[
J_T=\mathbb E\left[
\sum_{r:\tau_r\le T}\delta^{\tau_r}
\left(V_r+\beta U_r+\gamma I_r\right)
-\sum_r\pi^\top C_r
-\lambda L_r
-E_r
\right],
\]

where:

- \(V_r\): direct receiver-local usefulness;
- \(U_r\): downstream obligations unlocked or future work saved;
- \(I_r\): information from counterexamples, narrowed search, or useful failure;
- \(C_r\): compute, memory, storage, bandwidth, checker, and review resource vector;
- \(L_r\): latency;
- \(E_r\): expected loss from erroneous automatic reuse.

The terms \(V_r\), \(U_r\), and \(I_r\) are receiver-side estimates and may guide scheduling; they do not define either external endpoint. This objective is an analysis lens, not a global currency or permanent scalar. Publish its components and Pareto frontiers and do not double-count internal work.

Active coordination is evaluated only by its paired marginal effect relative to passive typed reuse:

\[
\Delta_{\mathrm{coord}}
=\left(A_{\mathrm{active}}-A_{\mathrm{passive}},
H_{\mathrm{active}}-H_{\mathrm{passive}},
\mathbf C_{\mathrm{active}}-\mathbf C_{\mathrm{passive}}\right).
\]

A positive claim requires its preregistered confidence rule; a null or negative result is reported as such and narrows or rejects the mechanism. Coordination-message counts, assigned tasks, or created decompositions are not outcomes.

For endpoint \(Z\in\{A,H\}\), report the full estimand ladder:

\[
\begin{aligned}
\Delta_L^Z&=Z_{\mathrm{LocalTyped}}-Z_{\mathrm{Isolated}},\\
\Delta_R^Z&=Z_{\mathrm{TypedReuse}}-Z_{\mathrm{LocalTyped}},\\
\Delta_{\mathrm{prior}}^Z&=Z_{\mathrm{TypedReuse}}-Z_{\mathrm{TypedReuseBlind}},\\
\Delta_T^Z&=Z_{\mathrm{TypedReuse}}-Z_{\mathrm{RawReuse}},\\
\Delta_C^Z&=Z_{\mathrm{FullCoordination}}-Z_{\mathrm{TypedReuse}},\\
\Delta_P^Z&=Z_{\mathrm{OptionalProgram}}-Z_{\mathrm{FullCoordination}}.
\end{aligned}
\]

The primary reuse family is \(\Delta_R^A,\Delta_R^H,\Delta_{\mathrm{prior}}^A,\Delta_{\mathrm{prior}}^H\). Local-memory, typed-infrastructure, coordination, and optional-program families are separately labeled secondary claims with their own preregistered two-endpoint multiplicity control; they are not silently pooled.

### 5.1 v0 preregistration defaults

The following are the v0 defaults for every confirmatory run. They may be changed only by a new numbered checkpoint committed before inspecting confirmatory outcomes; calibration and pilot traces used to justify a change are then excluded from the confirmatory sample.

**Topology and routing.** The primary federation has exactly five independently governed logical cells; a three-cell configuration is a smoke test. Home-placement fanout is \(r=2\) for domain-separated object, goal, environment, and receiver-approved interest routing keys. The homes are two independent hint/candidate rendezvous sites rather than one shared admission replica group or authority. The autonomous primary profile gives each cell a nontransferable issuer-local evaluation budget grant; no cross-cell shared budget exists. In the program-overlay contrast, local grants plus all nonoverlapping prepartitioned shared escrow equal the `FullCoordination` arm-wide ceiling componentwise; escrow reallocates that ceiling and does not add to it. Any larger program ceiling defines a separately labeled program-plus-budget intervention. One logical cell additionally has two crash-fault replicas for ledger-reconciliation tests. Each issuer ledger has exactly one write-authoritative replica per authorization epoch; other replicas reject writes, and failover requires fencing the old writer and advancing the epoch before the new writer accepts work. The initial candidate set is \(k=2\), and every failed routing epoch contacts at least one previously untried cell. A v0 work item therefore contacts every one of the five cells within at most five routing epochs before `NO_MATCHING_CELL` may be reported. Poisoning the initial top-\(k\) cannot defeat this exhaustive v0 fallback. Scale simulations with more than five cells use an exploration horizon of eight distinct nonhome cells; their routing-liveness claim is explicitly conditional on a matching cell lying in the home, initial, or eight-cell exploration set, and they report empirical miss probability rather than claiming universal discovery.

**Capacity and admitted load.** For every resource/capability class \(k\), calibrate service capacity \(\mu_k\) before the run and let \(L_k\) be the maximum admitted nonpreemptible job demand. The confirmatory horizon is \(H=10{,}000\) scheduler ticks after a \(2{,}000\)-tick warm-up in simulation and 60 wall-clock minutes after a 10-minute warm-up in a real-agent trial. For the formulas below, divide each measured real-agent horizon into \(10{,}000\) equal accounting ticks. Require

\[
L_k\leq 0.01\mu_k H
\]

and the admitted arrival envelope

\[
A_k(t,t+\Delta)\leq 5L_k+0.75\mu_k\Delta
\]

for every measured interval. Larger jobs must checkpoint and obtain another debit. Sweep malicious admitted work at \(0\), \(0.10\mu_k\), and \(0.25\mu_k\); it is included in, not added above, the \(0.75\mu_k\) total envelope. Separate overload runs use post-admission rates \(0.90\mu_k\), \(1.00\mu_k\), and \(1.25\mu_k\) and do not qualify for the within-envelope liveness claim; any higher offered load is explicitly recorded as shed and is not silently called admitted. After a stable baseline, each overload pulse lasts exactly \(D_{\mathrm{pulse}}=200\) ticks and has cumulative excess above service

\[
E_k=\int_{\mathrm{pulse}}(a_k(t)-\mu_k)_+\,dt
\leq 50\mu_k\text{-ticks}.
\]

The admitted rate then returns immediately to at most \(0.75\mu_k\).

**Fair service and backlog.** Admit at most ten positive-share receiver-owned service-class/capability-class queues per resource class. Every admitted, continuously backlogged queue receives a reservation \(s_q\geq0.05\mu_k\); the mandatory-validation queue receives \(s_{\mathrm{validate}}\geq0.25\mu_{\mathrm{validate}}\). A sender-created goal, namespace, topic, identity, or coordination scope creates no service class. Admission must reject or defer a new receiver service class if reservations would exceed capacity. For every continuously backlogged queue and every \(500\)-tick measurement window, require

\[
S_q(t,t+500)\geq 500s_q-L_k.
\]

Under the preregistered fixed-suite or workload-population resampling rule below, the upper endpoint of the 95% confidence interval for the steady-state backlog slope of every reserved queue must be nonpositive. For each profile and queue, the seed statistic is that complete seed replicate's fitted steady-state slope; it is not a paired-arm difference. The overload-recovery endpoint is deliberately **aggregate per resource class**, not per queue: after the frozen pulse ends and aggregate admitted work returns to \(0.75\mu_k\), total class-\(k\) backlog must return to at most its pre-pulse value plus \(5L_k\) within \(1{,}000\) ticks. The service-floor premise alone would not imply that every continuously backlogged queue receives aggregate spare capacity. The aggregate bound is feasible under the frozen pulse envelope: the nominal drain bound for excess plus one maximum nonpreemptible-job lag is

\[
T_{\mathrm{drain},k}
\leq
\left\lceil\frac{E_k+L_k}{0.25\mu_k}\right\rceil
\leq 600\text{ ticks},
\]

leaving 400 ticks for scheduler/accounting granularity. These service gates apply only when compatible workers remain reachable and the declared job-size and arrival envelopes hold; offered, admitted, served, and shed work are reported separately.

**Frozen external evaluation and statistical rule.** Before tuning, commit the CIDs of the online task contracts, receiver assignments, release times and deadlines, weights, workload instances, all profile definitions and feature flags, resource ceilings, snapshot-selection rule, analysis script, sealed future-input object \(S_{\mathrm{probe}}\), held-out weights, per-task budgets, prior-artifact-blind assignment and filtering point, interference-block construction, inference scope, noninferiority margins, direct-overhead categories, \(y_{\min}\), and common evaluator. These fields form an external `EvaluationSuite`; weights, reuse labels, treatment labels, and hidden task contents are absent from live protocol APIs. Keep held-out task contents inaccessible to workers and scheduler tuning and reveal them only after every profile's autonomous knowledge snapshots and read interfaces are sealed.

A **complete seed replicate** contains the complete online trajectories, sealed terminal knowledge snapshots, and held-out evaluations for every profile required by the estimand, under one frozen workload instance and one common random seed. Run at least 30 complete seed replicates per workload instance, coupling agent outcomes, task releases, network faults, evaluator seeds, and budgets across relevant profiles. A connected workload remains intact inside every replicate. For a two-arm estimand, compute its paired within-seed difference from the two profiles in that replicate. For a one-profile gate such as \(G_{\mathrm{cap}}\) or a queue's backlog slope, compute that profile's statistic from its complete trajectory; no nonexistent comparison arm is introduced.

There are exactly two confirmatory resampling rules:

1. **Fixed-suite stochastic estimand.** Conditional on a fixed workload instance, resample whole complete seed replicates across its seeds. The replicate statistic is the paired within-seed contrast for a two-arm estimand and the named one-profile statistic for a single-profile gate. If the fixed suite contains several named instances, resample replicates within each instance and aggregate with the preregistered instance weights. Never resample tasks, task families, artifacts, messages, or subgraphs.
2. **Workload-population estimand.** Use independently generated workload instances as outer clusters. First average the relevant replicate statistic—paired contrast or one-profile statistic—over seeds within each instance, then resample whole instance-level aggregates. A preregistered hierarchical sensitivity analysis may additionally resample whole complete seed replicates inside a selected outer instance, but individual tasks are never resampled. Require at least 30 independent instances for a bootstrap population-generalization claim; otherwise report only fixed-suite inference.

A dependency/communication-connected component may replace a whole workload instance only if the preregistered construction proves that no artifact, hint, queue, budget, fault, participant, treatment, or measurement spillover crosses components. A connected workload is one interference block; repeated seeds are stochastic repeats of that whole block, not independent workload-population draws. Every confidence interval below uses the applicable rule above, chosen before treatment. The isolated-agent capability gate uses the fixed-suite one-profile rule and passes only if the one-sided 95% complete-seed-replicate bootstrap lower confidence bound for \(G_{\mathrm{cap}}\) exceeds \(y_{\min}\).

There are four co-primary paired reuse contrasts: federated passive reuse versus local typed workspace and versus its paired prior-artifact-blind treatment, on both \(A_s(T)\) and \(H_s\). The cross-cell prior-knowledge **yield-superiority** claim passes only if the lower endpoint of a two-sided 98.75% estimand-appropriate paired-bootstrap confidence interval is strictly greater than zero for all four contrasts; 98.75% is the Bonferroni adjustment for four comparisons at familywise level 5%. Use only the resampling rule and interference unit above. Any invalid automatic online or held-out closure, fidelity-contract bypass, evaluation-label leakage into live decisions, or resource-ceiling violation fails the overall v0 reliability/usefulness claim regardless of yield. The raw shared-store contrast estimates the marginal value of typed discovery/admission and is a separately labeled secondary family. Resource savings or resilience improvements are distinct claims using preregistered noninferiority margins and endpoints; the primary rule does not silently establish every meaning of “benefit.”

Active coordination is a separate marginal analysis against passive reuse. Report claim types separately:

1. **yield superiority:** both \(A_{\mathrm{active}}-A_{\mathrm{passive}}\) and \(H_{\mathrm{active}}-H_{\mathrm{passive}}\) have strictly positive lower endpoints in two-sided 97.5% estimand-appropriate paired-bootstrap intervals, controlling the two endpoints at familywise 5%;
2. **resource Pareto improvement:** the preregistered yield endpoints and reliability are noninferior within frozen margins, no resource component is worse beyond its frozen margin, and at least one resource component has a strictly favorable adjusted interval;
3. **reliability or resilience improvement:** a separately preregistered reliability/resilience endpoint improves while yield and resources satisfy their frozen noninferiority margins.

If none passes, report no demonstrated coordination benefit. Always publish both yield intervals, \(\mathbf D_C\), and \(\mathbf O_C^{\mathrm{direct}}\). Central typed results quantify decentralization cost and resilience but are not a primary superiority test.

Any confirmatory local-memory, typed-infrastructure, or optional-program yield family likewise uses a separately preregistered two-endpoint 97.5% estimand-appropriate paired-bootstrap rule. Resource-Pareto and reliability/resilience claims use their separately frozen endpoint families and multiplicity correction. Otherwise label the analysis exploratory and make no familywise positive claim. Never select a family, margin, or direction after inspecting outcomes.

## 6. Primary metrics

### Knowledge yield

- autonomous online endpoint \(A_s(T)\) per compute-hour, wall-clock hour, and identical resource vector;
- held-out weighted reuse \(H_s\) under identical frozen evaluator/resource vectors, plus separately reported per-resource cost reduction;
- cross-cell paired effect \(X_s\) and federated-passive versus local-workspace contrast;
- active-coordination marginal effects on \(A_s\), \(H_s\), reliability, latency, and each resource;
- net arm resource delta \(\mathbf D_C\) and direct coordination-overhead vector \(\mathbf O_C^{\mathrm{direct}}\), with every frozen category reported;
- downstream obligations unlocked;
- reuse yield: fraction of closures whose accepted tree uses a previously admitted artifact, reported as telemetry rather than intrinsic value;
- held-out transfer gain from abstractions (expansion-only, not part of the primary criterion);
- high-fanout obligations discharged per validated lemma.

### Efficiency

- exact duplicate attempt ratio;
- intentional diverse-replication ratio;
- compute saved through action cache and failure-capsule reuse;
- routing regret relative to an omniscient small-trace scheduler;
- cache hit value, not only hit count;
- communication bytes and control messages per accepted artifact;
- per-agent control-state growth as network size increases;
- idle, queueing, and transfer time;
- validation backlog and generation throttling.
- demand-ticket issue/use/reject counts and valid-junk promotion rate;
- reserved/running/finalized redemption counts and authoritative/conservative charge vectors by `ACCEPT | REJECT | ERROR | UNKNOWN | CANCELLED_UNCLAIMED`;
- grant-to-ticket/child-ticket allocations, nonreclaimable ticket/grant/capability fanout use, live/terminal tombstones, reservation claims, meter records/alarms, duplicate actions, child terminal accounting, crash recovery, and atomic promotion-only retention/index/graph/replication accounting;

### Error behavior

- invalid automatic closure rate;
- false-equivalence and unsafe-merge rate;
- counterexample detection latency;
- challenge-to-correction latency;
- dependency-impact precision/recall;
- percentage of conclusions preserved through alternative support;
- common-mode errors that incorrectly satisfy a diversity policy;
- semantic mismatch caught by critics versus missed.
- valid but wrong/vacuous formalizations that incorrectly close an intent parent;
- stale-accept responses immediately after high-fanout defects and ordinary exact opposite-polarity admission;
- signed-support false-closure rate by required dependency polarity and validation basis;
- materialized-view divergence across delivery permutations of quarantine, release, and supersession facts;

Define the seeded false-acceptance rate

\[
\widehat{\mathrm{FAR}}=
\frac{\#\{\text{seeded invalid or mismatched cases obtaining stable closure}\}}
{\#\{\text{seeded invalid or mismatched cases}\}}.
\]

Release requires zero observed false stable acceptances, zero fidelity-contract bypasses, and zero resource-conservation violations. Zero observations are not a proof of zero population error. For \(n\) genuinely independent zero-failure trials, report the one-sided 95% exact upper bound \(1-0.05^{1/n}\); for clustered trials, use the preregistered cluster/block unit and do not apply the independent-trial formula naively.

### Resilience and fairness

- completion and useful-yield degradation under churn/partitions;
- convergence time after healing;
- accidental duplicate work during partitions;
- queue stability and overload recovery;
- per-resource/per-capability-class backlog slope and reserved-share delivery;
- starvation rate across domains, languages, and rare capabilities;
- task aging distribution;
- hot-key and foundational-environment availability.

## 7. Initial engineering gates

These are finite regression/model targets, not proofs of a zero population error rate. Numerical defaults are frozen by section 5.1 and may change only through a new pre-run checkpoint.

1. Zero seeded invalid Lean proofs are automatically accepted.
2. Zero seeded false-equivalence pairs cause automatic merge or obligation closure.
3. Exact deduplication has 100% precision on the controlled corpus.
4. Failed attempts suppress only mechanically subsumed searches.
5. A checked counterexample refutes exactly its scoped judgment.
6. A dependency incident preserves every conclusion with an unaffected accepted support path.
7. Crash-fault replicas of one logical cell converge to equal materialized views given equal admitted ledger facts, available closures, schemas, terminating checker outcomes, policies, and reliance overrides.
8. After a tested replica-group partition, admitted ledger facts merge without rollback; every independent cell's facts are re-admitted even when policy roots match; duplicate compute is measured separately.
9. The `Isolated capable agent` profile's exact normalized endpoint \(G_{\mathrm{cap}}\) has a one-sided 95% complete-seed-replicate bootstrap lower confidence bound above preregistered \(y_{\min}\); if it does not, no mathematical-efficacy or network-gain claim is made.
10. Federated passive reuse satisfies the section 5.1 paired primary rule: all four Bonferroni-adjusted confidence-interval lower endpoints for autonomous online and sealed held-out-reuse gain against local typed-workspace and paired prior-artifact-blind profiles are strictly positive under identical multidimensional budgets; the raw-store contrast is reported separately.
11. Active coordination is compared with passive reuse on both yield endpoints, reliability/resilience endpoints, every resource component, \(\mathbf D_C\), and \(\mathbf O_C^{\mathrm{direct}}\). Any positive statement is labeled specifically as yield superiority, resource Pareto improvement under noninferiority, or reliability/resilience improvement under noninferiority; a null, negative, or dominated result is retained as a mechanism-level falsification.
12. Compare the central typed service and federated profiles to isolate decentralization overhead/resilience; the oracle matcher is only a small-trace upper bound.
13. Under the section 5.1 arrival, job-size, and 200-tick/50\(\mu_k\)-tick excess-pulse envelopes, every reserved queue meets its \(500\)-tick service curve, every one-profile backlog-slope confidence interval has nonpositive upper endpoint, and aggregate per-resource-class post-overload backlog recovers within \(1{,}000\) ticks; offered/admitted/served/shed work is separated and overload sheds generation before mandatory checks.
14. From \(10^3\) to \(10^5\) simulated agents, and in a \(10^6\) stretch run, no operation becomes an \(O(N)\) broadcast and per-worker coordination state remains tied to local working sets; larger-cell routing reports its eight-cell-horizon miss probability and makes no universal discovery claim.
15. Seeded common-mode replicas do not satisfy a declared diversity requirement.
16. With the initial top-\(k\) poisoned and the only matching v0 worker at the last untried cell, the task reaches that cell within five routing epochs and receives an attempt under the declared queue envelope.
17. Forged remote `ACCEPT`, policy, grade, cancellation, priority, and challenge objects do not change stable state.
18. Circular support graphs of up to the tested maximum size support nothing without an accepted leaf.
19. Concurrent, duplicated, reordered, crash-recovered, and partitioned capability actions cannot widen scope or exceed the issuer-local nonreclaimable fanout or finite control-record allowance; capabilities expose no mathematical-work vector, rejected fresh IDs create no durable per-ID state, and every protected resource action binds the exact unique running reservation, execution action ID, authenticated principal, and receiver-controlled meter.
20. An anonymous challenge flood stays within attention/recomputation budgets and does not disable valid support.
21. A blackholing worker cannot suppress retry beyond the maximum lease interval.
22. Untrusted candidate/negative traffic cannot evict the protected validated working set or enter anti-entropy without admission.
23. Parser, proof, archive, decompression, graph, build, and checkpoint bombs terminate within declared limits.
24. Transport without checked target-side evidence cannot close an obligation.
25. At malicious admitted loads \(0\), \(0.10\mu_k\), and \(0.25\mu_k\) included within the total \(0.75\mu_k\) envelope, honest fair-share work and mandatory checking satisfy the reserved service curves.
26. An authenticated malicious independent member cell, including one advertising identical policy roots, cannot import acceptance, consume a receiver's demand budget, or alter stable reliance without receiver-local admission and authority.
27. A flood of at least \(10^5\) distinct valid tautologies consumes no more protected validation, storage, graph, or replication resource than its demand/exploration tickets authorize.
28. A high-fanout defect causes immediate fail-closed reuse at distant descendants while each invalidation transition processes only bounded work.
29. A correct proof of a deliberately wrong, vacuous, or assumption-strengthened formalization cannot close its semantic-intent parent.
30. Provider corruption fails CID checking; provider eclipse yields bounded fallback or explicit `UNKNOWN`/unavailability.
31. Hidden network/package access and mutable lookup during validation always fail closed.
32. Poisoned semantic indexes affect only bounded discovery/routing, never equivalence, support, admission, or merge.
33. Endpoint renaming cannot exceed aggregate onboarding exposure or satisfy mandatory diversity.
34. An authorized quarantine changes stable reliance only through an immutable admitted override; replicas of the same logical cell then converge.
35. A semantic reviewer can affect only the exact fidelity contract named by its receiver-issued role; forged, out-of-scope, expired, and post-revocation review actions have no effect.
36. An optional coordination organizer or external budget authority cannot mint a receiver's demand ticket, exceed its exact authorized scope, weaken another work item's contract, cancel unrelated autonomous work, or continue mutating control state after its service/authorization epoch is revoked.
37. The evaluation-suite tasks, receiver assignments, release times/deadlines, weights, per-task budgets, sealed future-input object, blind-treatment assignment, interference blocks, inference scope, noninferiority margins, direct-overhead categories, \(y_{\min}\), snapshot-selection rule, profile feature flags, analysis, and common evaluator commitments predate tuning; held-out contents remain unavailable until every profile's autonomous snapshots/read interfaces are sealed; and the published analysis reproduces all adjusted intervals and resource vectors.
38. With a ticket having `maxRedemptions=1`, 32 simultaneous valid reservation requests for distinct candidate roots create exactly one outstanding-or-settled redemption; replay of the winning `(ticketID, redemptionActionID, requestDigest)` is idempotent, while reuse of that action ID with another digest is rejected.
39. A public demand offer is never directly spendable. When an authorized worker and a malicious authenticated first claimant race, only the claim selected by receiver policy creates a holder-bound ticket; every losing claimant has no redemption authority or debit, and an accepted malicious claim can consume only its explicitly allocated offer/onboarding budget.
40. A namespace ticket with `maxRedemptions=8` subjected to 32 concurrent distinct candidates never has more than eight outstanding-plus-settled redemptions, and the componentwise sum of spending, outstanding reservations, and reserved children never exceeds its ceiling.
41. `REJECT`, `ERROR`, and `UNKNOWN` finalize and charge receiver-authoritative parsing, fetch, validation, and inert-staging work while releasing only soundly known unused balance; a measurement gap incurs its frozen conservative upper bound, potentially the full reservation. These outcomes create no durable promotion and spend zero promotion-only retained-byte, protected-index, support-graph, outbox, or replication allocation.
42. Crashes immediately after reserve, claim, meter debit, checking, inert staging, and before or during the local finalization transaction recover to exactly one `RESERVED`, `RUNNING`, or immutably `FINALIZED` state: no reservation becomes silently reusable or multiply executing, no protected work is free, and no finalization is charged twice. Outbox dispatch and every actual external effect remain outside that transaction and require separately funded execution.
43. Ticket/grant expiry is judged solely by the issuing receiver's crash-safe ordered `ReceiverTime(writerTimeEpoch, monotonicTick)` and requires no cross-cell clock synchronization. Every writer activation durably advances the time epoch before accepting work; prior-epoch deadlines are expired and prior-epoch running claims recovery-finalize before new protected work. An unclaimed pre-expiry reservation may only cancel/expire with its redemption slot consumed; a running pre-expiry claim may finalize under its receiver-bounded execution expiry, after which recovery charges authoritative use plus conservative gaps and forbids promotion.
44. Child-ticket issuance reserves the child's full resource ceiling and redemption allowance and nonreclaimably consumes \(1+\) its descendant fanout before publication; its normative attenuation checks reject cross-grant, later-expiry, widened principal/audience, scope, class, artifact-kind, predicate, contract, and fanout attempts. Replay, cancellation, child crash, and parent/child concurrency preserve every parent resource, redemption, and count bound, and reclamation occurs only through an explicit durable terminal transition that does not restore issue authority.
45. During an issuer-replica partition only the ledger side retaining write authority accepts new ticket, reservation, execution-claim, or child allocations. After recovery, the fenced authoritative ledger's grant/ticket outstanding, finalized, settled, descendant-reserved, and nonreclaimable issue/fanout amounts remain within every ancestor ceiling; control state is not set-union merged, and an isolated replica fails closed rather than creating a second spend history. In the program-overlay comparison, local grants plus prepartitioned shared escrow equal the `FullCoordination` arm-wide ceiling componentwise; any added resources are labeled a bundled program-plus-budget intervention.
46. A mechanically accepted direct counterexample in the exact context yields raw state `(0,1)` and closes the exact `REFUTE` obligation but not its `PROVE` obligation.
47. A mixed-polarity refutation composition declaring a supported premise and a refuted child activates only when each signed dependency polarity is present; replacing either dependency with the opposite polarity does not derive the refutation.
48. Exact raw state `(1,1)` closes neither `PROVE` nor `REFUTE` under the strict profile and cannot support a downstream dependency of either polarity.
49. A path using a forbidden axiom, checker profile, or weaker validation basis cannot enter a stricter contract, even when the same conclusion is admissible under a permissive policy. Current strict P0 accepts exactly `LOCAL_REPLAY` and receiver-checked `DOMAIN_CERTIFICATE`; `SUCCINCT_ARGUMENT` is rejected until a later versioned policy passes its adoption gates.
50. If one support tree is defeated, inconsistent, or inadmissible under the current basis while a separate clean tree satisfies the exact contract, the clean alternative still closes the obligation.
51. All delivery orders and duplicate deliveries of concurrent quarantine, release, and supersession override facts with the same immutable inputs and policy epochs yield the same stable view; genuinely incomparable facts yield an explicit unresolved state rather than arrival-order choice.
52. Missing-closure, declared timeout/fuel/memory, malformed-certificate, checker-crash, sandbox-failure, corrupt-runtime, and TCB-alarm fixtures map respectively to the frozen `UNKNOWN`/`REJECT`/`ERROR` taxonomy, consume receiver-authoritative reserved work plus frozen conservative bounds for measurement gaps, and enter no signed support set or negative suppression cache.
53. The complete independent-purpose reuse trace passes with every `coordinationScopeRef` absent: local production and validation at one cell, bounded hint publication, overlapping subscription at another cell, receiver-funded fetch, receiver-local replay, and exact downstream reuse.
54. A flood of at least \(10^5\) unique publication hints from rotating endpoints stays inside aggregate hint/key/provider quotas, causes no closure fetch, validation, protected indexing, child creation, or payload replication, and causes no hint forwarding outside bounded matching subscription/home-shard quotas.
55. Creating arbitrarily many identities, goals, topics, namespaces, or coordination scopes does not increase the finite receiver service-class count or any reserved queue share.
56. Changing only evaluation-suite weights, reuse labels, or hidden annotations changes no live admission, validation, promotion, scheduling input, or stable-support decision.
57. A coordination organizer's attempt to revoke an artifact that remains contract-valid for an unrelated receiver has no effect on that receiver's stable evidence; only receiver-local evidence, closure/policy state, an admitted defect, or a reliance override can change reliance through the epoch-linearized rules.
58. A disappearing or withholding publisher yields explicit unavailability or `UNKNOWN` unless the receiver has funded and obtained the exact retained closure; a CID or hint alone never supports reuse.
59. Routing-key grinding and hot-key concentration remain within per-home quotas and trigger bounded alternate routing; homes never obtain admission authority from key placement.
60. Two or more sibling tickets whose requested ceilings each equal one parent grant cannot all be issued against that same balance: the atomic issuance ledger preserves the grant vector, redemption allowance, and nonreclaimable issue/fanout bounds. Closing a child ticket transfers its actual spend and consumed redemptions to its parent before releasing unused work allocation, while its count authority remains consumed, so repeated zero-work child creation cannot create unbounded objects or recycle spent capacity.
61. After a root ticket, child ticket, or grant is terminalized before cryptographic expiry, every fresh issuance or reservation action fails, including after released capacity is allocated to a sibling; an identical recorded action still returns its prior result.
62. A full-ceiling ticket plus any capability never yields more than the ticket ceiling: the capability has no spendable resource state, and attempts to omit, reuse, or rebind the exact running reservation/execution/principal/meter fail.
63. Two concurrent finalization requests for one running execution that differ in outcome, promotion choice, meter digest, or spend commit exactly one immutable settlement. There is no state in which released promotion allocation can be consumed elsewhere and later charged by a post-settlement promotion.
64. A locally verified succinct argument with unavailable native closure is labeled `OPAQUE_RELIANCE` and fails every strict P0/public reusable-knowledge query even when succinct verification accepts.
65. From one reservation of vector 10, 32 concurrent distinct execution claims yield exactly one `RUNNING` claim. Every losing claim exposes zero protected service; wrong execution IDs/principals fail; all parallel subactions under the winner remain within the one cumulative hard envelope of 10.
66. After actual protected use, a claimant report of zero or a forged meter digest cannot reduce the authoritative charge. A crashed, missing, rolled-back, or integrity-alarmed meter charges the frozen conservative bound for each gap; no capacity is released from claimant testimony.
67. A fresh claim's issuer-derived expiry is no later than both reservation expiry and `claimedAt + MaxExecutionDuration` in one writer-time epoch. A maximally long hung claim is recovery-finalized by that bound as `UNKNOWN`, with receiver-authoritative plus conservative-gap charges, and never returns to `RESERVED`.
68. With `maxRedemptions=1`, a reserve/cancel loop can create exactly one `CANCELLED_UNCLAIMED` settlement: cancellation releases the resource vector but consumes the redemption slot, and every later fresh reservation fails.
69. Zero-work create/terminalize loops cannot exceed a root grant's nonreclaimable ticket-issue/grant-fanout allowance or a ticket's descendant fanout allowance, including across nested child grants/tickets and crash replay.
70. Cache `PROVE x=ACCEPT`, then admit an exact locally checked `REFUTES x` justification; the immediately following old-cache query returns non-`ACCEPT` even before reverse traversal. The symmetric refute-then-proof trace also passes, and an independent clean alternative accepts only after exact current-epoch tree checking.
71. The frozen 200-tick overload pulse respects \(E_k\leq50\mu_k\)-ticks, reports offered/admitted/served/shed work separately, and meets both the derived drain bound and the 1,000-tick **aggregate per-resource-class** recovery gate for every profile; no per-queue recovery claim is inferred from aggregate slack.
72. A root-ticket action carrying a nonabsent `parentTicketID` and a root-grant action carrying a nonabsent `parentBudgetGrantID` are rejected before allocation. Conversely, child transitions require the exact parent ID; no object can enter root allocation and child terminal accounting, or vice versa.
73. A parent grant of ceiling 10 issues a child grant of ceiling 10; descendant tickets spend all 10 and terminalize into the child. Terminalizing the child subtracts its full reserved allocation while adding spend 10 and consumed redemptions to the parent, so no sibling can spend a recycled 10. Nested nonzero-spend and crash-replay variants preserve every ancestor inequality.
74. After claiming near tick 800 with expiry 900, crash/restart resets the platform monotonic counter but durably advances `writerTimeEpoch`. The old claim recovery-finalizes before new protected work, and repeated restarts cannot extend it or any old ticket/grant deadline.
75. At every crash/interleaving point between preparation of a support-changing fact, dirty seeds, and reliance-epoch publication, a query either observes the entire old tuple, the entire new tuple, or a fail-closed in-progress epoch. It never observes a current new epoch without the fact and later accepts an old tree after the fact appears under that unchanged epoch.
76. A capability with action-record allowance \(a\), including \(a=0\), subjected to at least \(10^5\) distinct fresh authenticated non-metered control actions creates at most \(a\) accepted replay records across its entire preallocated child subtree. Concurrent final requests cannot both spend the last unit; rejected IDs create no unbounded per-ID durable state; expiry, terminalization, replay, and epoch compaction never restore allowance.
77. Crash injection before and after inert staged-CAS writes, the local admission/settlement/retained-reference transaction, outbox-intent creation, and attempted external effects yields one of: an unreferenced garbage-collectable staged object, one paid durable local retention/admission plus pending intent, or a separately funded completed effect. Any actual external effect attempted before a committed `PROMOTE` intent is rejected. No external/filesystem effect outside the authority transaction is claimed atomic with the ledger, no outbox intent grants execution authority, and no post-finalization effect spends the old reservation.

## 8. Fault matrix

Vary:

- benign result-error rate: 0%, 1%, 5%, 10%, 20%;
- correlated-error clusters: shared model/method/retrieval/checker/context;
- capability concentration and rare skills;
- runtime tails: lognormal and Pareto;
- agent churn and crash rate;
- message loss/delay/duplication/reordering;
- partitions among replicas of one logical cell, partitions among independent cells, and isolated cells;
- stale capability advertisements;
- embedding drift and cross-domain misrouting;
- hot tasks and flash crowds;
- generated-work arrival from 50% to above 100% of service capacity;
- dependency fanout and artifact demand skew.
- malicious admitted loads \(0\), \(0.10\mu_k\), and \(0.25\mu_k\) by resource class plus unlimited unauthenticated endpoint labels;
- valid-tautology/context arrival far above demand-ticket capacity;
- publication-hint, discovery-key, provider-record, optional-scope, and service-class-minting floods from rotating endpoints;
- concurrent single-redemption and multi-use namespace-ticket races, reserve/cancel loops, same-reservation execution-claim races, and malicious first claims on public offers;
- `REJECT | ERROR | UNKNOWN` per-component receiver-authoritative/conservative charging, meter underreporting and gaps, bounded crash-safe running-claim expiry, conflicting promotion decisions, and crashes at reserve/claim/meter/check/inert-staging/local-finalization/outbox/external-effect boundaries;
- duplicate/concurrent capability authorization and fanout, missing/rebound execution claims, zero-work child-object amplification, child widening/reclamation, post-terminal fresh actions, issuer crash recovery, and partitioned issuer writes;
- forged assessments, mutually supporting cycles, unvalidated challenges, false exhaustive failures, and out-of-scope or revoked budget-authority/reviewer/coordination actions;
- an authenticated malicious independent cell advertising identical policy roots, plus an explicitly nonpassing assumption-violation run showing that Byzantine compromise of a replica-group admission authority is outside v0;
- provider/index eclipse attempts, cache pollution, and decomposition amplification;
- hostile archives, terms, build recipes, checkpoints, and natural-language prompt injection.
- incorrect/vacuous formalizations with valid proofs and spoofed failure-domain diversity.
- missing proof closures, active dirty roots, and power-law reverse-dependency fanout.
- evaluation-suite weight/reuse-label leakage and coordination-scope deletion or revocation attempts;
- direct and composed refutation, cached proof/refutation followed by exact opposite evidence, mixed signed dependency polarities, exact inconsistency, forbidden validation bases, and clean alternative support trees;
- every permutation and duplicate delivery of concurrent quarantine, release, and supersession overrides.

Report confidence intervals under the preregistered fixed-suite or workload-population rule from section 5.1. Do not present one cherry-picked scale run or composite score.

## 9. Suggested implementation sequence

### Milestone A: local mathematical efficacy and validation

- one cell, standalone goal templates/work items, attempts, typed partials/counterexamples, and a pinned Lean adapter;
- semantic-intent parents with separate fidelity contracts;
- signed support/refutation/strict-active-reuse fixed points and one-process deterministic materialized view;
- the minimal local grant → ticket → reservation → unique execution claim/meter → check → local finalization/outbox path for every paid validation, including idempotent issue/reserve/claim/finalize actions, zero-spend unclaimed cancellation with slot consumption, per-component receiver-authoritative/conservative charging, immutable optional promotion, and separately funded execution of every external effect;
- no federation, remote task assignment, shared program, or coordination scope.

**Exit:** the `Isolated capable agent` profile's one-sided 95% complete-seed-replicate bootstrap lower bound for \(G_{\mathrm{cap}}\) exceeds \(y_{\min}\); exact acceptance, circular-support rejection, direct and mixed-polarity refutation, opposite-evidence cache invalidation, exact-inconsistency nonclosure, validation-basis isolation, clean-alternative preservation, and formalization-mismatch tests pass.

### Milestone B: local reusable knowledge and resource safety

- exact/structural retrieval, action cache, typed failure capsules, dependency repair, and retained closures;
- local demand offers, namespace tickets, permission-only proof-of-possession capabilities, unique running-execution binding, authoritative meters, nonreclaimable descendant-issue allowances, normative child-ticket attenuation/allocation, irreversible grant/ticket terminal reclamation, concurrent redemption/claiming, and bounded onboarding;
- exact in-environment relations with target-side replay, delivery-order-invariant overrides, and lazy bounded dependency impact.

**Exit:** local memory reuse is measured; sibling and attenuated child-ticket issuance, zero-work object-loop bounds, concurrent redemption/execution claim, authoritative/conservative atomic outcome/promotion charging, reserve/cancel and crash boundaries, bounded expiry recovery, post-terminal fresh-action rejection, child terminal parent charging, permission/resource separation, and issuer recovery conserve every ancestor budget; no unsafe merge occurs; stale opposite-evidence caches fail closed and alternative support survives incidents.

### Milestone C: autonomous cross-cell reuse

- exactly five authenticated independent cells, domain-separated object/goal/interest homes, bounded `PublicationHint` objects, overlapping subscriptions, CAS locality, and receiver-local import;
- optional crash-fault replicas for one logical cell;
- staggered independent tasks with every `coordinationScopeRef` absent.

**Exit:** the zero-scope trace, malicious-member re-admission, hint-flood noninterference, disappeared-provider, hard-nonmatch, replica-partition, and exhaustive five-cell routing gates pass.

### Milestone D: optional active coordination and scale

- remote work routing, remote decomposition exchange/adoption, remote capability offers, cross-cell pull/leases/checkpoints/stealing, and remote portfolio orchestration as separable features; the local solver and P0 admission/backpressure contract remain unchanged;
- optional coordinated-program profile whose shared escrow reallocates the same arm-wide ceiling, plus a separately labeled program-plus-budget stress arm if desired;
- event-driven simulator calibrated to held-out real traces.

**Exit:** active coordination is compared with passive reuse under identical local solvers, task/fault/random tapes, and componentwise arm-wide ceilings; all overhead is charged and reported; safety and fair-service gates still pass. Yield, resource-Pareto, and reliability/resilience claims are classified separately, and a null, negative, or dominated coordination result is accepted as a mechanism-level result.

### Milestone E: comparative evaluation

- baselines and ablations;
- real-agent autonomous streams, prior-artifact-blinded treatments, optional coordinated-program runs, and large simulations;
- reproducibility bundle, raw traces, confidence intervals, and audit.

**Exit:** the narrow experimental claim is supported or explicitly rejected.

## 10. Published artifact

Deliver:

- Markdown protocol and fault-model specification;
- reference local research/validation core plus separable knowledge, federation, and coordination layers with transactional admission and budget ledgers;
- Lean validation adapter;
- real workload and ground-truth relation set;
- agent adapters and deterministic replay agents;
- event-driven simulator with held-out trace calibration;
- baseline and ablation implementations;
- harness-only evaluation-suite metadata and a protocol-projection noninterference test;
- raw traces, analysis notebooks/scripts, and reproducible environment;
- published \(\mathbf D_C\), \(\mathbf O_C^{\mathrm{direct}}\), arm resource vectors, frozen noninferiority margins, and claim classification;
- Lean or equivalent lemmas for grounded signed-support/refutation properties plus a TLA+/PlusCal, Apalache, or equivalent model of grant/root/child issuance, nonreclaimable count authority, reserve/claim/meter/cancel/atomic-finalize spending, terminal tombstones, permission capabilities, epoch-linearized reliance changes, leases, defects, and partitions;
- independent audit and disposition ledger;
- technical paper reporting both gains and overhead.

## 11. Success claim

The project should claim only what the evaluation establishes. Use a decomposed statement:

> Under the measured tasks, budgets, and fault distributions, the isolated local research/validation core [did/did not] exceed its preregistered capability floor and contained all seeded invalid or mismatched stable acceptances. Typed cross-cell reuse [did/did not] establish preregistered yield superiority. Active coordination [did/did not] establish [yield superiority / a resource Pareto improvement under noninferiority / a reliability or resilience improvement under noninferiority]; its net resource delta and direct overhead were [reported values].

It should not claim universal research acceleration, global optimality, complete semantic alignment, or eventual solution of arbitrary mathematics.

The minimum v0 intentionally defers permissionless membership, a public DHT, global ANN discovery, general cross-prover morphisms, learned scheduling, general certified-exhaustion semantics, SNARKs, blockchain, political attribution, and incentive systems. These are reconsidered only after the vertical slice establishes a measured need.
