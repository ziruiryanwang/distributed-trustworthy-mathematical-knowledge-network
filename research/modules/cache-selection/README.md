# Module: bounded cross-judgment cache selection

Date: 2026-09-20. Scope: concept investigation and exact-cut review of an optional local policy. Integration owner: root. Current assignments, source cuts and review/selection status are in [WORK](../../registry/WORK.md). No implementation, model execution, native replay or measurement is authorized.

## Concrete missing choice

[ORG1](../../../spec/OPERATIONAL-CORPUS-V1-ORGANIZATION.md#deterministic-automatic-selection-p4) already specifies P4 selection among evidence for the same exact judgment. Its [retention section](../../../spec/OPERATIONAL-CORPUS-V1-ORGANIZATION.md#retention-and-index-maintenance-policy) also specifies finite probation/cache terms and permits checked-use observations to nominate content. The remaining choice investigated here is narrower:

> Given several different checked judgments and finite discretionary cache capacity, how does one owner turn bounded local observations into an actual promotion or renewal decision?

This is an optional engineering-policy question, not a native-soundness defect or a demand for a universal measure of mathematical worth. Different owners may prefer different policies. A concrete baseline lets us inspect behavior, resource use and failure modes without forcing agreement across the network.

The authoritative network/native specification remains [V6/I](../../../spec/OPERATIONAL-CORPUS-V6.md), with [J/VIEWS1](../../../notes/checkpoints/CP-001J-unfamiliar-interface-entry.md) optional. Neither is edited by this investigation. [K](../../../notes/checkpoints/CP-001K-local-cache-feedback.md) now selects CACHESEL1 after both scoped source reviews and [integration review](audits/selection-audit.md). Its [five-file manifest](../../../notes/checkpoints/CP-001K-SHA256-MANIFEST.md) freezes exact sources/audits/checkpoint; this card remains mutable navigation. The newest source file alone has no selection authority.

## Scope and boundaries

Read the [source policy](proposal.md), [signal/policy audit](audits/signal-policy-audit.md) and [resource/lifecycle audit](audits/resource-lifecycle-audit.md). Each has its separately assigned author/reviewer in WORK. Root coordinated one repair cut for the planning-abort, nomination-fence and renewal-headroom findings; both reviewers reread that complete cut before K integration. Historical author roles confer no right to edit now-frozen files. Review closure is not implementation approval.

| Input or decision | Permitted role | Boundary to preserve |
|---|---|---|
| Receiver-observed checked applications | Bounded local signal for later cache decisions | Repeated delivered observations are not new uses; genuinely repeated cheap uses still do not prove independent demand or causal value |
| Different proofs/replays of one judgment | P4 evidence alternatives | Extra alternatives do not manufacture additional cross-judgment demand weight |
| Shared native closure and metadata | Exact resource input at the actual state cut | Marginal payload is set-dependent; zero new payload does not mean zero index, control or maintenance cost |
| Ranking/exploration result | Advisory candidate set for owner-authorized warm terms | No automatic native acceptance, publication, durable release, extra resources or mathematical research assignment |
| Existing custody, active use/export and route anchors | Protected obligations accounted in the base and transition | Falling score or nonselection cannot erase another holder's protection or pretend a lost public anchor remains qualified |
| Warm terms and recovery | Inherited finite retention authority | Usage does not reset a deadline; clean admission sealing differs from actual retention-clock loss; uncertainty cannot replenish spend |

[E custody](../../../notes/analyses/CP-001E-custody-contract.md) remains owner-release-required durable protection. [H coverage](../../../notes/analyses/CP-001H-resource-supply-and-discovery.md) remains conditional on actual selected/retained anchors and paid service. CACHESEL1 cannot silently turn either into an evictable popularity cache.

## Decisive countercases

- Two different judgments each need eight payload units and share seven; their joint nine-unit cost differs from summing sixteen. A third disjoint eight-unit result can compete with them. Frequency alone does not decide which set is genuinely better.
- Deliver one checked-use observation twice, then create many distinct cheap applications. Idempotent observation handling and bounded signal inflation are different requirements; neither identifies independent investigators.
- A replacement of an eight-unit root by a disjoint six-unit root fits a ten-unit final capacity but not a fourteen-unit coexistence peak. Deferral is a legitimate outcome.
- A discarded cache handle shares bytes with durable custody, an active export or an H routing anchor. Only that handle's lawful release is permitted. A physical generation already claimed for deletion is not free usable deduplication.
- A low-observation abstraction helps only after later bridge work. A bounded exploration lane can make room for some such candidates but cannot guarantee every object's survival or future usefulness.

The last limitation is already explained in [C's popularity and censoring analysis](../../../notes/analyses/CP-001C-growth-analysis.md#popularity-can-erase-future-value). Its finite-capacity impossibility is not repaired by changing the score's name. A selector may be practically useful without being optimal, fair to all mathematics or robust to arbitrarily funded signal manipulation.

## Exit and evidence grade

Concept-stage exit requires an exact finite policy with admitted inputs, bounded observation state/work, determinate ordering and ties, explicit promotion/renewal/deferral outcomes, lawful transition accounting, one favorable and one defeating paper trace, and separate exact-cut signal/lifecycle audits. Formal arguments should establish the stated boundedness and authority separation; usefulness remains a falsifiable heuristic hypothesis.

The [readiness evidence contract](../qualification-readiness/README.md) governs stronger later claims. A paper example cannot demonstrate measured hit-rate, reduced checking cost, useful long-term retention or overall operability. The source policy must not depend on those claims already being true.

## Prior-work orientation

Frequency-informed cache admission is established systems work, not a project novelty claim. Gil Einziger, Roy Friedman and Ben Manes, [TinyLFU: A Highly Efficient Cache Admission Policy](https://arxiv.org/abs/1512.00727), describe recent-access estimates used to choose whether to admit an item, separately from choosing an eviction candidate. Their reported trace/simulation results do not establish effectiveness for mathematical evidence with shared dependency closures, multiple realizations and non-evictable protection obligations.

Evidence boundary: root inspected the primary arXiv abstract, citation metadata and submission history read-only on 2026-09-20 (HTTP 200; original submission 2015-12-02, latest history entry v2 dated 2015-12-03). The full paper, algorithms and experimental artifacts were not inspected or reproduced. This is orientation for future policy comparisons, not selection of TinyLFU, a sketch-based counter implementation, or its measured performance as a premise of CACHESEL1. CACHESEL1 has its own exact-cut paper reviews; actual effectiveness still needs later measurements.
