# CP-001D: an operable Lean-based mathematical commons

Date: 2026-09-19  
Status: Detailed candidate design with adversarial paper review; not implementation-qualified  
Stage: Concept/specification only

## Outcome

This checkpoint selects a concrete architecture for the democratization of mathematics: a downloadable Lean 4 based node that independent investigators can use to obtain exact checked mathematics and contribute new independently checked artifacts. The network has no required central theorem server, global research goal, human-intention assessment, or unsolved-problem registry.

The concept's central unit is not “a result somebody said was verified.” It is an exact formal artifact plus a selected complete replay closure that another node can acquire, check, retain, and use without the producer.

Read the [integrated contract](../../spec/OPERATIONAL-CORPUS-V1.md), then its three companions:

- [Native mathematics](../../spec/OPERATIONAL-CORPUS-V1-MATHEMATICS.md).
- [Peer service and preservation](../../spec/OPERATIONAL-CORPUS-V1-NETWORK.md).
- [Organization and accumulation](../../spec/OPERATIONAL-CORPUS-V1-ORGANIZATION.md).

## Four layers with different standards of evidence

| Layer | Selected mechanism | Appropriate standard |
|---|---|---|
| Correct mathematics | Inert Lean native expressions/declarations, exact foundation, receiver-side checked replay | Formal derivability under exact assumptions and a qualified checking boundary |
| Independent availability/service | Content addressing, full selected closures, direct authenticated peers, local resource authority, exports, repair | Explicit state transitions, fault models, conservation and conditional progress |
| Discovery and reuse | Exact indexes plus bounded structural keys, scoped pages, directed/rotating peer search | Honest coverage labels, checked applicability, measured cost/recall |
| Efficient growth | Bounded proof alternatives, access/reuse-guided retention, exploration, explicit resource tradeoffs | Defensible empirically evaluated heuristics, not a universal utility theorem |

Authentication and isolation cross the layers wherever somebody can spend resources or disclose content. Attribution is not a condition of native mathematical validity.

## The chosen Lean route is practical, not only a toy fragment

Lean-Native/v1 targets safe definitions, theorems, opaque declarations with checked bodies, structures/projections, mutually and nested inductive groups, quotient machinery, and exactly specified standard axioms. The kernel source is pinned to official Lean v4.22.0; it is not described as the newest available release.

Peer source, tactics, plugins, compiled .olean files, and downloaded checker binaries do not execute on the receiver's acceptance path. A producer-side exporter can use an ordinary Lean environment but is untrusted. A receiver independently reconstructs native data and checks it. Native reserved names require an exact checked bootstrap.

A separate small constructive profile provides conformance examples. Its success would not establish the practical profile's compatibility. Actual bootstrap bytes and representative library replay remain release gates.

## Identity, acceptance, and availability

JudgmentID preserves the exact context and statement. ProofID distinguishes witnesses. ReplayID selects the complete dependency/witness closure. These cannot be collapsed into a theorem's printed name or one generic hash.

Native checking, locally allowed assumptions, current incident state, actual bytes, and retention are separate dimensions. A historical check remains historical when its proof becomes unavailable. A remote status is a scoped observation, not local acceptance.

Opposite proofs under contradictory hypotheses can both be sound conditional mathematics. The checkpoint repairs the earlier overbroad interpretation that any such pair constitutes a defect. A closed contradiction under a compatible admitted basis is a different, stronger event.

## No global ledger is required

Nodes retain their chosen complete closures and bounded indexes. They maintain local spend/recovery ledgers, not a universal record of every theorem. Direct peers, contact bundles, finite route hints, and offline archives suffice for the base protocol.

Every provider and receiver authorizes its own finite work. Computation and network delivery have separate metered executions. Service epochs can rotate without reviving old tickets or discarding live funded warm caches. Exact storage-generation fences prevent garbage collection from racing with a new protected use.

Blockchain-style consensus may later coordinate a genuinely shared scarce resource. SNARKs may later accelerate a precisely bound verification computation. Neither substitutes for available reusable formal content or decides mathematical usefulness.

## A real reciprocal mathematical path

The [paper cases](../analyses/CP-001D-operational-paper-cases.md) develop monoid fold/append laws, reuse them for folds over blocks and homomorphisms, and derive ordered hierarchical aggregation at a third independent node after the first leaves.

The derivation preserves hypotheses and block order, exercises structures and induction, and includes exact transfer/admission/retention steps. It is a hand-checked paper chain, not a claimed executed Lean proof.

The [conditional arguments](../analyses/CP-001D-conditional-safety-arguments.md) justify the specified native composition, resource accounting, status epochs, protected retention, and pagination under explicit premises. They also exhibit counterexamples to overstrong progress and growth claims.

## Autonomous indefinite accumulation

The [sustainability analysis](../analyses/CP-001D-autonomy-and-sustainability.md) specifies recurring local ingest, discovery, preservation, recovery, and policy-improvement cycles. Standing local policies can authorize successive finite jobs without assigning mathematical investigations.

The system has no mandatory central lifetime. It still requires continued physical capacity, surviving copies, and maintained checking software. A network of finite machines cannot retain every future incompressible artifact forever at fixed resources. The useful engineering objective is sustained recoverable growth and affordable reuse, not an unsupported promise of universal exponential accumulation.

## Audited checkpoint, not claimed completion of the ultimate goal

The [audit](../audits/CP-001D-OPERABILITY-AUDIT.md) records material repairs and independent cross-reviews. The [interface inventory](../analyses/CP-001D-interface-inventory.md) reconciles root kinds, record ownership, public read scopes, operations, and time boundaries.

The design is substantially more actionable than the prior concept: it chooses concrete data paths, procedures, limits, failure outcomes, and qualification gates. It is not yet qualified software. No implementation, native builds, executable tests, or performance benchmarks were started.

The long-term project goal remains active. Neither “all uncertainty removed” nor “forever guaranteed” is asserted. The [goal record](CP-001D-GOAL.md) preserves the user's intent; the [checkpoint manifest](CP-001D-SHA256-MANIFEST.md) identifies the reviewed document snapshot.
