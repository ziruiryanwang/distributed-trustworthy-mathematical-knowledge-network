# Local agent policy versus the mathematical commons API

Date: 2026-09-20. Architectural clarification prompted by the user's question: can API documentation and agent skills replace our proposed tightly integrated search/proof controller? This is a design checkpoint, not a new conformance result or an executed agent experiment.

## Decision and reason

Yes, for the agent's policy. The commons must support independent investigation, not implement or prescribe it. When to search, which definition to try, how to instantiate it, and how to prove remaining obligations belong to the local agent. Documentation, examples and optional skills are an appropriate initial way to teach that workflow. No particular model, prompt, tactic engine or public task queue is required.

Our proposed deterministic `SolveByElim` controller is optional experimental scaffolding. Its acquisition barriers, search restarts and witness-selection strategy must not become prerequisites for the core product. Preserve its proposal, but defer implementation until an actual interface experiment demonstrates a need. Close integration with Lean's checking and environment management is important; close integration with one research strategy is not.

This does not establish that any prompted agent will succeed efficiently. It separates safety guarantees from empirical agent capability rather than substituting prompts for either.

## Three responsibilities

| Component | Must provide | Does not decide |
|---|---|---|
| Commons/node interface | Discoverable candidates; exact artifact/dependency retrieval; independently checkable publication; explicit limits and failure semantics | Which mathematics an agent should investigate; which proof strategy is best |
| Local Lean client/SDK | Checked admission into a bound environment; usable declarations and dependency mappings; ordinary Lean diagnostics; isolated, bounded execution | Whether a retrieved object is interesting or which unsolved local obligation to pursue |
| Independent agent | Queries, candidate choices, local constructions, proof attempts, optional contribution/retention choices | Whether its unsupported assertion becomes trusted mathematical evidence |

These are responsibility boundaries, not a requirement for three separate executables or services. Query projection, import helpers, display adapters and optional tactics can ship together as a reference client without being required network policy.

## Enforced boundary, not prompt advice

Let `E` be a locally accepted environment under pinned foundation `F` and assumption policy `A`. For any agent policy `pi`, successful admission must satisfy the conditional safety obligation:

`Admit(E, package) = E'  =>  E' is a checked compatible extension of E under (F, A).`

Similarly, accepting a claimed theorem `T` requires a closed proof checked against its bound dependency closure and permitted assumptions. Neither the agent's confidence, its compliance with a skill nor a provider's description is a premise of mathematical acceptance. These are specification obligations relative to checker/bridge/host correctness, not new unconditional soundness proofs.

A returned definition is not just a text snippet. After checking, the client must expose its exact reference, type, universe parameters, usable local Lean binding and relevant transparency/body information where available, with dependencies resolved. The agent then uses ordinary Lean to apply it and obtain obligations. Failed elaboration or proof search is an agent outcome, not a verdict that the acquired mathematics is false.

Failed or interrupted admission must not leave a partially trusted environment. Candidate metadata remains untrusted before checking. Remote mathematical artifacts do not authorize running arbitrary build scripts, plugins or tactics. Resource, decoding and execution protections must be enforced even when an agent ignores instructions.

## What the initial documented API must make possible

The following are capability requirements, not frozen endpoint names or new wire schemas:

- Search using a well-scoped formal request, with bounded responses, explicit truncation and version/environment context. Search results are candidates; an empty page or timeout is not proof of nonexistence.
- Inspect untrusted candidate metadata as data, then fetch exact artifacts and the dependencies needed for checking.
- Check and admit a compatible closure, returning a usable Lean environment/declaration mapping or a structured refusal without partial admission.
- Run local Lean elaboration/checking with actionable diagnostics. An adapter from a local goal to a formal query is convenient, but queries may also be formulated independently of a current goal.
- Export a complete checkable contribution and offer it to peers. Local validity, publication, peer acceptance, discovery and durable custody are separate statuses; publication does not imply global adoption or permanent retention.

Documentation should explain errors, budgets and these distinctions, not merely list successful calls. Natural-language instructions to an external agent do not introduce human intention into mathematical acceptance or require a natural-language/formal-mathematics interface inside the commons.

## Smaller decisive experiment

Replace the custom-controller critical path with an agent-in-the-loop interface experiment. Keep the original full existential Gate B target and mathematical corpus; do not shrink it to theorem lookup. Supply a genuinely isolated consumer with the formal target, initial checked environment, provider contacts and API documentation, without known useful contribution IDs or previous solutions. An instruction to ignore leaked answers is not input isolation.

Let the consumer choose its own queries and proof actions. Record exposures, requests, replies, checked acquisitions, failures and total resource cost. Check the final proof and inspect whether acquired material is genuinely used. Publish its exported artifact; have a fresh consumer independently check and actually reuse it in a subsequent result. If the first consumer proves the target directly, report completion without discovery-origin reuse; do not force a decorative dependency.

This experiment would establish a particular API-mediated reuse/contribution/further-reuse path. It would not prove utility, search optimality, robustness to arbitrary clients or exponential growth. A competent local-only comparison is needed for an efficiency claim, but not for the narrower existence-of-an-operable-path claim. No networking claim follows from local provider snapshots. Fixed compatibility, failure and malformed-input conformance tests remain necessary alongside agent trials.

Agent/model cost and latency require explicit experimental accounting; the earlier deterministic-controller timing envelope must not silently be claimed for a different workflow. The replacement experiment needs a finite reviewed plan before execution. No external API use, deployment or unbounded trial is authorized by this checkpoint itself.

## Immediate disposition and preserved evidence

- Preserve completed Gate A and R1 evidence unchanged.
- Existing preparation A1 finished its 16 commands with zero nonzero exits. Its receipt says `STAGE_COMMANDS_COMPLETED_NOT_MATH_ACCEPTANCE`; corpus identity/replay audit is still pending. This does not qualify discovery.
- Keep authored metadata helper/tests provisional and unexecuted. Final reference-lane overflow and universe-erasure flag semantics remain unresolved. Do not expand the extractor merely to support the shelved controller.
- Next prioritize the usable agent/API boundary and the smallest missing capability for an honest end-to-end trial. Reuse existing import/export and Lean capabilities; no general prover is commissioned.

## Sources and review scope

- [Full Gate B target](2026-09-20-subtype-composition-contract.md).
- [Preparation contract](2026-09-20-formal-discovery-preparation-contract.md): retained historical experimental cut; its native controller is not core policy.
- [Native-controller proposal](2026-09-20-discovery-controller-native-proposal.md): optional and unimplemented.
- [Preparation ledger](../../experiments/lean-formal-discovery/IMPLEMENTATION-LOG.md).

The native/source author independently confirmed this policy/API separation and proposed the smaller agent-in-the-loop test. A separate evidence reviewer agreed, emphasizing contextual handles, complete checked artifacts, actual dependency-path inspection and fresh reuse. Guided fixtures must be labelled; isolated inputs, disclosed agent/model configuration, matched baselines, complete costs and eventually repeated held-out trials are needed for broader utility claims. These architectural reviews do not certify an implementation, an API specification or agent performance.
