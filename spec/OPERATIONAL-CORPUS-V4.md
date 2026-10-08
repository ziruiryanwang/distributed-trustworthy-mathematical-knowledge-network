# Operational mathematical commons v4: composable evidence and practical reuse

Date: 2026-09-20. Status: selected integrated concept/specification, independently reviewed at the bounded scopes recorded in the [CP-001G disposition](../notes/audits/CP-001G-AUDIT-DISPOSITION.md). The [checkpoint](../notes/checkpoints/CP-001G-composable-evidence-and-practical-reuse.md) and its manifest bind this cut. This is not deployment qualification. No implementation, build, native replay or benchmark has been performed.

## Product and priority

Independent investigators download the commons, find and acquire existing formal mathematics, check and use it locally, and contribute further reusable mathematics. The initial language is Lean 4. There is no mandatory central server, global theorem ledger, human-intention assessment, research scheduler or unsolved-mathematics task registry.

The priority is trustworthy and effective reciprocal use. Exact evidence establishes mathematical acceptance. Local heuristics and learned tools can improve retrieval, construction, presentation and allocation without proving that they are optimal. Popularity, source labels and signatures do not establish truth. A rarely used theorem remains mathematics; repeated padded uses do not prove that it is valuable.

This amendment addresses three concrete usability obstacles left by the frozen [v3 design](OPERATIONAL-CORPUS-V3.md): proof choices that obstruct otherwise coherent branch composition, unknown-identifier retrieval, and loss of ordinary Lean authoring facilities. A fourth mechanism makes mathematical interface transport an actual bounded local operation.

## Selected mechanisms and precedence

| Mechanism | Detailed contract | Boundary |
|---|---|---|
| PI1: proof-instance evidence | [Composition analysis](../notes/analyses/CP-001G-proof-instance-composition.md) | Multiple exact implementations may prove one judgment; complete grounded evidence still checks independently |
| STRUCT2 and FULL_FEATURE | [Structural retrieval](../notes/analyses/CP-001G-structural-retrieval.md) | Bounded formal features lead to candidates, not proofs of applicability or complete search |
| CLIENT1 | [Library/client interoperability](../notes/analyses/CP-001G-library-interoperability.md) | Owner-local presentation and elaboration produce complete native candidates; peer code is not installed |
| BRIDGE1 | [Checked interface applications](../notes/analyses/CP-001G-interface-bridges-and-applications.md) | Explicit checked maps and property transport, not nominal equality by assertion |
| Profile/consumer bindings | [Exact typed consumers](../notes/analyses/CP-001G-profile-and-consumer-bindings.md) | New proof kinds receive explicit codec, root, hint, index and custody bindings |

This integration overrides only its expressly named v3/v2 contracts. Frozen earlier checkpoints remain unchanged. The exact profile/consumer note controls operational codec bindings where a mechanism note summarizes them; the mathematical composition and structural notes control their respective exact algorithms. In an unresolved contradiction, the proposed mechanism is not qualified; an implementer cannot choose whichever interpretation is convenient. The disposition records the found contradictions and their repairs.

## Foundation and representation version boundary

Select NativeRules code **4** for PI1 plus the unchanged HEIGHT1 rule and native semantic constructors. This produces a new NativeRulesID and FoundationID. The kernel qualification candidate remains Lean `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b` with matching mathlib `5ed2965256430c3649e86755f9576b54eca72435`.

Code 3 continues to mean the frozen v3 reconstruction and witness selection. Neither its artifacts nor its certificates are relabeled. The changed evidence-reference and native-name contract is explicit even though PI1 adds no axiom and no new kernel inference principle. Actual bootstrap, reserved-name inventory, adapter and image qualification remain unperformed; no resulting digest is fabricated.

Claims of unchanged semantic declaration/JudgmentID identity are restricted to one exact code-4 foundation with unchanged semantic descriptors. Re-expressing code-3 content under code 4 changes foundation-bound identities. It is staged re-expression and independent checking under MIGRATE1, not automatic proof of source/target equivalence. There is no compulsory global upgrade or silently preferred latest foundation.

## Integrated registry and typed service boundaries

NativeRules retains type/schema `0x0003/1` and payload `[nativeFamilyTag,ruleSchemaCode,featureCodes,allowedAxiomNamePaths]`. The selected value is family 0, rule code 4, unchanged feature codes `[0,1,2,3,4,5]`, and the exact previously selected native axiom inventory/types. Code 4 binds the new PI1 reconstruction with HEIGHT1; it does not admit a new peer axiom or executable shortcut. Native semantic schema-2 descriptors keep their grammar but now bind their actual code-4 foundation.

| Type/schema or code | Selected meaning |
|---|---|
| `0x0022/1` | WitnessTermDAG, with explicit proof-instance references and no direct canonical JudgmentID reference alternative |
| `0x0023/1` | ProofInstance `[JudgmentID,WitnessTermID]` |
| `0x0024/1` | Exact canonical JudgmentID-to-ProofInstanceID representative map |
| `0x0015/3` | InstanceReplay `[FoundationID,typedRoot,representativeMapRoot]`; root tags 1/2/3/4, no legacy tag 0 |
| `0x0016/3`, `0x0017/3` | InstanceModule and same-context opposing evidence, with exact PI-root/replay bindings |
| `0x8123/1`, `0x8124/1` | STRUCT2 extractor and public structural descriptor |
| `0x8102/3` mode 6 | Exact bounded STRUCT2 predicate for FIND_WINDOW |
| `0x8111/3`, `0x800A/3` | Public PI1 root descriptor and historical status observation |
| `0x8022/2` | Signed code-4 provider advertisement, including explicitly negotiated K4 feature keys |
| `0x8120/2`, `0x8121/2`, `0x8122/2` | Inert code-4 advisory manifest/library/collection pages with InstanceReplay hints |
| Capability 7 | STRUCT2/1; fixed extractor/query/descriptor semantics |
| Capability 8 | PI1 and the exact code-4 mathematical/service-consumer domains |
| Operation 20 | ROUTE_FEATURE_GROUP_OPEN; immutable FULL_FEATURE group mode and exact extractor |

The detailed composition, structural and profile-binding notes give the exact payloads, limits and dependencies for these allocations. NET2 remains outer version 2; ServiceCall remains `0x8004/2`. Existing generic typed-CID transfer and inventory records retain their bytes/authority while explicitly admitting only the new exact selected closure kinds under capability 8. Strict legacy ProofID fields are not made untyped.

Capability 8 and the exact FoundationID are both required for code-4 native service. The selected STRUCT2 query path additionally requires capabilities 3 and 7; its routing path requires 5, and grouped FULL_FEATURE publication requires 6. Reciprocal existing HELLO exchanges establish the two-sided advertisements without changing HELLO's request shape. Codec support is separate from willingness to serve or local adoption of a foundation.

Public exact-judgment results use `0x8111/3`; mode-6 structural results use `0x8124/1`. Snapshot/cursor commitments bind that actual record ordering, not a hypothetical shared descriptor universe. A schema-2 ProviderAd binds its schema-3 public root anchor and InstanceReplay; for K4 that root's exact structural hint must contain the token. It is still an untrusted provider lead, not independent evidence of truth or global coverage.

Operation 16 creates only FULL_EXACT/K1 groups. Operation 20 creates only FULL_FEATURE/K4 groups. Operations 17–19 act on the exact retained group mode/foundation/extractor and inherited owner/root/version/lifecycle guards. Neither a batch nor an old garbage-collection sweep can reinterpret or seize another group's rows. Changes to record eligibility are capability/profile-bound; frozen code-3 records retain their meanings.

## Mathematics: semantic references and proof implementations

Semantic statement terms, definitions, opaque declarations and group descriptors continue to use canonical judgment references. Proof-instance references occur only inside their expressly permitted evidence term format; they cannot enter semantic identity through an unnoticed extension of NativeTermDAG. A receiver materializes each exact nominal group once in its coherent selected environment.

The selected evidence view separates a finite proof-instance DAG from a canonical-judgment realization map. The map supplies an actual checked proof for each canonical judgment reference reached through the selected semantic/evidence closure. A root proof need not be that map's representative for its own judgment. Every alias is backed by a previously checked proof; an unproved theorem type is never inserted as an axiom.

For example, an earlier proof `a : True`, a proof `c : a = a`, and a later proof `b : True` using c are an ordinary acyclic source development. The evidence view may retain a as the canonical representative while contributing b as another implementation. Forcing b to replace a everywhere can create an artificial selected-support cycle; PI1 removes that requirement, not cycle checking.

Proof irrelevance can justify checked native conversions between proofs of convertible propositions. It cannot identify arbitrary data values, equate independently declared nominal types, or justify reusing a footprint/checking certificate from a different representative realization. Changed realization choices require compatible reconstruction and checking with the actual complete assumptions/support.

## Discovery is an operating service, not a relevance oracle

STRUCT2 derives finite deterministic features from formal terms: exact semantic heads/selectors, relation operands, argument edges and function input/output information. It includes definitions, opaque declarations and constructors useful as maps, not only theorem conclusions. The canonical extractor bounds syntax inspection and its beta/zeta-only supplemental view; it never executes a peer tactic or assumes source binder/class metadata was retained.

The selected feature budget is at most 32 tokens per target. Truncation and excluded views are reported. A provider can advertise FULL_FEATURE only for an explicit finite selected scope and its actual emitted token memberships. It does not claim to index every useful property of those targets, every local theorem or all mathematics.

FIND_WINDOW candidate filtering and routing are separately metered. A failed bounded match is not a proof of nonapplicability. An unobserved posting is not evidence of global absence. Complete native evidence acquisition and checked argument instantiation remain required after a useful-looking descriptor is found.

## Authoring and genuinely different interfaces

CLIENT1 distinguishes an exact admitted mathematical environment from an owner-local Lean presentation environment. Its correspondence map binds actual canonical declarations and selected evidence. A qualified finite frontend-name inventory handles actual name-sensitive frontend operations such as parameter markers, numerals and coercions. Checked inert metadata can reconstruct selected structures, classes, instances and simp entries; arbitrary remote plugins/macros/simprocs are not accepted.

This is substantively needed: `Finset.range` contains proof data; `Fin.castLE_castLE` mentions another theorem in its statement; the List-setoid/Multiset/Finset chain reaches proofs through nominal interfaces. The source note distinguishes actual read-source facts, paper representation consequences and unexecuted qualification. No complete mathlib compatibility is inferred from these examples.

BRIDGE1 handles genuinely different mathematical interfaces. From `b : B`, `f : B → A` and `ell : Π a:A, P(a)`, it constructs and checks `ell (f b) : P(f b)`. Claiming a different result `Q(b)` additionally needs native conversion or an actual checked transport `Π x:B, P(f x) → Q(x)`. Neither a familiar name nor a structural feature match supplies that transport.

Search states include actual values, context and evidence, not endpoint types alone. The initial automatic map graph is restricted to functions nondependent in the final subject after earlier parameters are supplied; arbitrary dependent functions remain explicitly applicable. Finite search can miss a useful map. Such incompleteness is allowed in the heuristic, never in the claim that a returned result has been checked.

## One reciprocal-use trace

The following is an operational paper trace, not an executed test or a shared research plan:

1. Investigator A independently chooses some mathematics, obtains complete producer evidence, exports a PI1 root, and establishes its own native check and protected local closure. It may stop there without publishing.
2. With separately authorized public disclosure/index/retention resources, A publishes the exact root and selected STRUCT2 descriptors. It funds its finite feature-key placements and renewals; local acceptance alone does not produce remote discovery.
3. Investigator B independently encounters a formal expression in its own work. Under its disclosure policy it searches selected local/remote feature lanes and reaches A through live routing observations. No desired conclusion is stored as a network task.
4. B treats descriptors as hints, acquires the exact chosen replay closure, checks its finite evidence graph and actual axioms under its own adopted foundation, and obtains current protected local use. A's signature cannot replace this step.
5. B selects a compatible realization and either explicitly applies the imported mathematics or uses its owner-local CLIENT1 view. If its interface differs, BRIDGE1 constructs actual maps and transport terms. Residual premises remain explicit until supplied or honestly abstracted into a conditional theorem.
6. B exports a newly checked result with the real proof instances and semantic dependencies used. It may contribute an alternative proof, a cheaper checked map, a reusable definition or a new statement. Only the last of these necessarily changes the statement stock, and none alone proves novel insight.
7. An independently chosen investigator C can repeat this loop without joining A's or B's research agenda. Availability, retrieval and supplied capacity remain explicit premises, not consequences of the theorem-checking rule.

Correctness composes conditionally on the qualified native basis and complete checks. Useful progress additionally requires actual discoverable evidence, affordable applications and sustainable supplied resources. The design does not infer exponential useful growth from a rising number of hashes.

## Resource and assurance boundary

The earlier NET2 bounded transfer, receiver-owned checking certificates, relevant current-use guards, exact disclosure, owned custody and source/target migration rules remain in force. New evidence and descriptor kinds must be explicitly included in their exact codecs, closure walks and typed identity keys before they are serviced; there is no generic permission to insert new types into old record slots.

All layers share one owner's real resource supply. Proof-instance parsing/checking, representative selection, structural extraction/posting, presentation reconstruction and bridge search each consume finite allocations. Complete cold closures and rebuilt environments can be much larger than the newly displayed theorem. Default surface-target counts do not bound transitive native work by magic.

Future execution must distinguish direct application, compatible branch joining, changed-realization rechecking, successful feature retrieval, checked interface transport, unsupported frontend facilities and resource nondecision. Qualification must include ordinary proof-dependent Lean developments and unfamiliar providers; answer IDs supplied in advance or toy closed proofs alone would not test the selected mechanisms.

This specification cannot establish absence of every unknown implementation bug, perpetual survival without continuing storage supply, universally complete retrieval or guaranteed exponential mathematical productivity. These are not claims that can be repaired by declaring a checkpoint complete. The project goal remains active while concrete design gaps are investigated.
