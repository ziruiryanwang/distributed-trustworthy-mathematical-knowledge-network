# CP-001D operability audit and disposition

Date: 2026-09-19  
Scope: Concept, paper arguments, and interoperability boundaries; no software or executed conformance tests

## Review process

The root author integrated three separately authored specifications: native mathematics, independent peer service, and organization/growth. The authors then reviewed one another's work. The organization author independently reviewed networking and the root's paper arguments/cases; the network author independently reviewed the native Lean route and pinned upstream sources; the mathematics author independently reviewed integration, client reuse, long-term autonomy, and the interface inventory.

These are cross-reviews, not three independent implementations or three independent proofs of kernel soundness. Their scope and exact reviewed hashes are recorded separately:

- [Network and paper-case cross-audit](CP-001D-cross-audit-network.md).
- [Mathematics cross-audit](CP-001D-cross-audit-mathematics.md).
- [Integration and sustainability cross-audit](CP-001D-cross-audit-integration.md).

The root also read all three companion specifications and repaired their cross-component bindings. Review found substantive defects, not merely editorial improvements.

## Material findings and repairs

| Finding | Why it mattered | Selected repair |
|---|---|---|
| A six-seed no-new-inductive profile could substitute a toy for the intended commons | It could not directly support ordinary Lean algebra structures, quotient/classical developments, or realistic libraries | Separate core conformance profile; practical Lean-Native profile with checked groups/opaque bodies/projections and explicit standard assumptions |
| Blindly hashing every native name | Lean kernel behavior for literals/arithmetic/quotients includes reserved-name recognition | Exact locally admitted checked compatibility bootstrap; no publisher control over reserved names |
| Inductive identity circularity | A group cannot hash itself through its own global member references | Bound group-local indexes inside the descriptor; generated names after GroupID; regenerate recursors through checked kernel |
| Same-judgment alias self-support | A valid source theorem p2 := p1 can collapse both names to one JudgmentID | Export earlier witness directly or explicitly inline/substitute it; still reject cyclic selected replay |
| ProofID alone did not determine replay evidence | Auxiliary witnesses can change costs, assumptions, and availability | Separate exact ReplayID; bind assessment, retention, status, and export to it |
| Conditional opposition mistaken for invalid mathematics | Contradictory/uninhabited hypotheses soundly imply both a proposition and its negation | Scoped opposing relation; basis incident requires separately checked closed contradiction under compatible evidence |
| Definitions/groups forced into theorem-shaped status | Not every checked artifact has a proposition/ProofID | Tagged proof/definition/group/opaque roots and kind-correct optional status fields |
| Unfunded or misaccounted response delivery | A finalized computation meter cannot cover later network writes; socket success is not peer receipt | Separately preallocated one-shot reply execution and settlement; immutable computed outcome |
| Generic CAS reads could expose unrelated/private material | Knowing a hash is not disclosure authority | Exact public-closure/audience-export read scope, chunk membership check, full-closure publication approval |
| Delayed reply raced with withdrawal/currentness | Computed results may be sent after policy or epoch changes | Snapshot-labeled status; disclosure authority checked under NET1's reply-claim policy; no mutation of committed outcome |
| Eventual delivery falsely implied success under finite deadlines | Every reply can arrive just too late | Separate bounded nondecision termination from successful timely admitted attempt |
| Replay history could fill during indefinite service | Deleting active-epoch issuance keys permits replay amplification; refusing forever defeats operability | Clean stop/drain/retire rollover with durable epoch floor and preserved resource accounting |
| Routine service rollover could erase useful warm caches | Control-record pressure can force frequent rotation | Separate retention-clock generation; clean service rotation preserves funded original deadlines |
| GC grace period alone did not exclude new use | A new root can appear between mark and physical delete | DELETE_PENDING generation fence, protected use/export pins, recoverable deletion order |
| Four fixed neighbors did not provide a practical large-network search path | Diverse mathematics can be outside those neighbors' holdings | Bounded collection-aware peer directory, one-hop route hints, finite later directed/exploratory rounds |
| Native-negative/Module metadata had no peer read scope | Neither was a native replay root; generic read would weaken isolation | Transport negative proof ReplayID; derive relation locally; local/offline modules decompose into supported replay operations |
| Duplicate cache count exceeded its advertised byte footprint | Exact paired IDs plus overhead do not fit 64 bytes each | Smaller count plus simultaneous real-byte enforcement |
| Numerical workload exceeded default retained-root limits | A disk example alone did not authorize the extra records | Explicit alternative ORG-SAMPLE root/descriptor/edge allocations within hard caps |
| Pagination conventions disagreed | Last-examined and next-unprocessed cursors cannot silently share one schema | Fixed next-unprocessed exact-ID convention; output-cap/interrupted-test cases preserve that entry |
| Throughput and storage estimates omitted bottlenecks | Network concurrency alone ignores offer issuance; interpolated day counts are not discrete completion times | Explicit maximum of bottleneck bounds; corrected day interpretation and stated ignored caps |

All repairs are concept-level rules, not evidence that an eventual implementation obeys them. A bibliography or API name does not establish execution correctness.

## Scope protected during revision

No mandatory human-intention field, originating question, shared root goal, unsolved-mathematics task list, or central research scheduler was introduced. Formal statements are judged by their actual encoded evidence and assumptions. Local agents choose their investigations externally.

Usefulness remains heuristic where appropriate. Exact local access and checked downstream dependency occurrences can guide cache/index policy. Neither usage counts nor an LLM ranking decides mathematical validity. Valid but unretained content is not declared false.

No global theorem ledger, universal peer roster, mandatory DHT, central server, or token is needed for the selected contribution/reuse path. Local authentication protects operational authority. Political attribution does not enter the native checking relation.

## What has and has not been established

The notes now select a coherent candidate route rather than a menu of unspecified architectures: exact native artifacts, independent replay, locally funded service, scoped retrieval, closure retention, and repeated external investigation. Paper cases cover a substantive three-generation mathematical chain, ordinary exchange, malformed input, hidden assumptions, contradictory hypotheses, overload, pagination, crash cuts, delayed delivery, and preservation.

Conditional paper arguments establish consequences of explicit premises: native composition, no authority gained by copying, cumulative resource conservation, coherent epoch observations, closure-preserving collection, and honest pinned pagination. These are not mechanically verified proofs, source-code audits of an implementation, or measurements.

No review can certify the absence of every unknown loophole. The active project goal is therefore not declared achieved merely because these notes are lengthy or no additional finding appeared in one review round.

## Explicit qualification gates

| Gate | Required evidence before the corresponding release claim |
|---|---|
| Practical native foundation | Actual canonical bootstrap bytes and reserved-name inventory; exact checked generated members; no unexpected axiom/unsafe dependency |
| Faithful client interchange | Round trips for dependent telescopes/universes, theorem aliases, opaque bodies, structures, mutual/nested groups, strings/arithmetic, and quotient/classical examples |
| Representative library utility | A pinned realistic mathlib slice with complete bodies and independently replayed closures, not merely a tiny core example |
| Exact wire interoperability | Final enum/field fixtures for all public records and independently checked canonical encoder/decoder vectors |
| Crash/resource implementation | Executable transitions and fault-injection around claims, settlement, promotion, delivery, epoch rotation, retention, and deletion |
| Practical capacity | Measured full cost of small-object transfer, indexing, checking, metadata, repair, and rollover under honest load and floods |
| Large-network discovery | Scoped recall/latency/cost under heterogeneous holdings, contact churn, partitions, and hostile hints; no global completeness claim |
| Software assurance | Qualified checker builds, isolation, runtime, crypto libraries, storage durability, and adoption/migration procedures |

These gates are not excuses to silently narrow the product or trust foreign compiled artifacts. They state exactly where concept reasoning stops and empirical/executable assurance must begin. Implementation remains prohibited until the user explicitly requests it.

## Checkpoint integrity

The accompanying [manifest](../checkpoints/CP-001D-SHA256-MANIFEST.md) identifies final document bytes and excludes itself. Earlier frozen checkpoints are preserved; the new top-level operability index does not rewrite their historical index.

Preservation was checked against the existing 18-file CP-001/CP-001A manifest and 11-file CP-001C manifest: all recorded sizes and SHA-256 hashes matched. The CP-001B checkpoint and its audit also matched their recorded hashes. No earlier frozen file was edited.

The new Markdown set was checked for UTF-8 replacement/control characters, balanced display/inline mathematical delimiters, and local link targets. The manifest is then checked against its final listed files. These are document checks only, not executed protocol or Lean conformance.

Document hash, UTF-8, link, and delimiter checks establish only document integrity. They cannot establish the correctness of mathematical evidence, an eventual implementation, or the rate of useful knowledge growth.
