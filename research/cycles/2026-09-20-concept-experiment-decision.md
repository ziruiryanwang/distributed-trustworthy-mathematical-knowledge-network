# Decision: develop the concept through bounded experiments

Date: 2026-09-20. Root's strategy decision, informed by separately prompted read-only native and corpus/utility reviewers. No new code, experiment, deployment or network implementation is authorized or performed by this decision. Preserve the completed [local feasibility checkpoint](2026-09-20-executed-reciprocal-feasibility.md) and frozen specifications.

## Maturity judgment

The project has a coherent, substantially specified candidate architecture with one executed end-to-end local feasibility witness. It does **not** yet have a demonstrated operable system. We should develop concept and experiment together, organized around consequential questions rather than independent streams of additional mechanisms and additional examples.

Well-formedness has several distinct meanings. The basic mathematical objects, trust boundaries and reconstruction route are sufficiently determinate to implement and test. A complete engineering specification would additionally resolve the interfaces and failure outcomes of a supported product scope. Practical operability requires those interfaces to work at tolerable cost on relevant workloads and under stated resource/fault assumptions. Our finite success establishes neither the last two for the whole system nor universal soundness of its implementation.

Unperformed qualification is not automatically a missing concept. Conversely, an experiment that needs an unstated interpretation or authority rule exposes a specification problem even if a programmer can make the example run.

## Hold stable; do not declare everything final

Hold the following boundaries stable for the next investigation:

- Mathematical acceptance derives from exact formal evidence checked over an explicitly selected foundation, not authorship, popularity, a sender verdict or human intention.
- Contributions remain independently replayable; indexes and model weights help discovery/generation but do not replace proof evidence.
- Correctness, availability, discovery and usefulness remain separate claims.
- Local agents choose their own investigations; no shared mathematical task queue, mandatory root goal, central server or global ledger is required.
- Ranking, retention and usefulness estimates may be heuristic. Such estimates cannot override mathematical checking.

Do not freeze every encoding, adapter interface, retrieval policy or resource/default parameter as final. Preserve versioned contracts for reproducible experiments; revise a contract explicitly when evidence exposes a consequential defect or tradeoff. Published earlier evidence remains about its original cut.

## The next investigation: source-driven independent composition, then discovery

The next phase is **not a broad mathlib import project**. Select one small real source-library interface because it exercises an important presently untested boundary, such as a shared nominal structure with parameters or proof-bearing data. Exact declarations, required features and finite budgets must be fixed before execution. It need not exercise every unsupported feature simultaneously.

### Gate A: composition with known identifiers

Two separate producer environments start from the same exact admitted interface and independently author different contributions. Export actual ordinary Lean source records rather than hand-constructing the desired mathematical payloads. A fresh consumer receives the relevant IDs, acquires/checks both contributions, constructs a result whose checked representation uses both, exports its actual accepted representation, and obtains fresh independent replay.

Preserve the shared interface identity and each branch's meanings and dependencies. Do not build both branches in a single hidden producer environment and call that independent development. A different proof representative for a shared judgment is a useful **later separate variation**, not a condition silently conflated with the first source-export/composition case.

Known IDs are deliberately supplied at this gate: it isolates native/interface composition. Success supplies no discovery or efficiency claim. Library size alone is not the acceptance criterion.

### Gate B: discovery and costed reuse on the same corpus

Once the known-ID route works, use a fresh consumer without Gate A's useful IDs, proofs, plans, conversation history or other answer-bearing state. Its own local formal expressions must generate the queries. Include alternative relevant candidates and irrelevant valid contributions. Evaluate actual checked application and successor export, not merely a returned search hit or a listed dependency. Distinguish successful discoverable checked reuse from a measured benefit: the former can succeed while the latter fails.

Use three diagnostic conditions with matched local capabilities and explicit initial information:

1. No acquired contribution: the local-only reference condition.
2. Relevant contribution supplied by ID: an oracle-assisted known-access diagnostic, **not** a deployable search baseline, guaranteed performance bound or free-cost speedup claim.
3. Contribution obtainable only through the selected discovery interface: the operational candidate.

Keep initial toolchains, solver policy and finite budgets comparable; include unsuccessful attempts. Charge search, transfer, native checking, interface adaptation and local proving. Report producer preparation/publication and retained storage separately and include them in any claimed system-wide gain. Add a simple retrieval baseline if claiming that a sophisticated retrieval policy improves on it.

A small pilot can identify bottlenecks and show bounded benefits or failures. It cannot establish general usefulness, exponential growth or long-run statistical effects. Replication, held-out variations and credible supply assumptions are needed for stronger claims. Use frequency, measured saved work and learned rankings can guide local heuristics without becoming universal definitions of mathematical worth.

These cases are experimental instruments for us, not a compulsory task list in the future system. Human intention remains outside mathematical acceptance; local interests may influence the formal queries and work agents choose.

## How outcomes change the work

| Observation | Interpretation and next action |
|---|---|
| Known-ID composition fails because the specification leaves identity, evidence selection or dependencies ambiguous | Resolve that conceptual/interface ambiguity and amend the affected contract before expanding the experiment |
| A unique specified behavior exists, but the code violates it | Repair the implementation; do not treat the bug as architectural impossibility |
| Known-ID composition works but discovery fails | Investigate query representation, candidate coverage or retrieval policy using this same supported case |
| Supplied-ID reuse itself offers no benefit | Investigate workload relevance and acquisition/checking/adaptation costs before attributing the problem to discovery |
| Discovery and checked reuse work but do not help under the tested cost envelope | Do not claim a benefit; inspect acquisition/checking/adaptation overhead and the workload, then compare a targeted change |
| A bounded helpful reuse case succeeds | Preserve the mechanism/evidence and test variation; do not infer sustained growth from one case |
| The declared budget is exhausted | Record noncompletion and actual costs, identify the limiting stage, and choose an explicit resource/design tradeoff; do not silently enlarge the budget or reduce the mathematical claim |

Concept work runs alongside preparation of the experiment to specify contracts, assumptions and observable outcomes. It resumes substantively when a result changes an architectural decision. It should not require proof that every heuristic is optimal; it should require that heuristic claims be testable and that correctness cannot depend on their accuracy.

## Reviewer synthesis and scope

The native reviewer prioritized a costed unknown-result reuse investigation with an oracle-assisted control; the corpus reviewer prioritized separately authored shared-interface composition before discovery. Root resolves the difference with the two gates above on one corpus: known-ID composition is the diagnostic prerequisite, while discoverable beneficial reuse is the product question. This is a staged investigation, not one undifferentiated PASS condition.

The corpus reviewer then read this complete strategy note and found no blocking conceptual objection. Root incorporated three clarifications from that review: a fresh discovery consumer without prior answer-bearing state, separate discovery and benefit outcomes, and the supplied-ID/no-benefit diagnostic. This was a strategy review, not evidence that either new gate has executed.

Robust decentralized transport/custody, broad malicious-input qualification, large-corpus indexing and continuing-growth resource models remain necessary later work. Reopen them earlier if they actually block the selected local path. No current result justifies making blockchain consensus, SNARK delegation, political attribution or optional broker calendars the next implementation priority.

Immediate work within the concept phase is to select the exact shared-interface case and write its finite experimental contract. Executing or expanding the prototype beyond the previously authorized one-path experiment requires a separately bounded implementation authorization. This strategy decision itself makes no execution claim and does not mark the overall goal complete.
