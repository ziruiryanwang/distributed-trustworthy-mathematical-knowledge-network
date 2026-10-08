# Operational mathematical commons v2: integrated scale and assurance amendment

Draft begun: 2026-09-19; integration review: 2026-09-20. Status: selected concept/specification, not implemented or deployment-qualified.

## Product and scope

The product is downloadable node software through which independent local investigators obtain, use, contribute, discover, and preserve exact formal mathematics. It is initially Lean 4 based. It has no necessary central server, compulsory global ledger, human-intention model, root research objective, or public unsolved-mathematics task list. Maintenance jobs concern existing bytes, evidence, indexes and service obligations, not what mathematics agents must investigate.

The software represents access to a growing distributed mathematical object space. It cannot contain all future knowledge in its installer or give every finite node instantaneous knowledge of all remote state. A node owns a bounded collection and explicit observation scopes. Its locally usable selected evidence is complete; its knowledge of the whole network is necessarily partial.

Correctness is a hard acceptance boundary under an explicit qualified foundation. Discovery, useful-growth selection, proof preference, and retention nomination can use imperfect heuristics and learned models. Their mistakes must waste bounded resources or miss useful mathematics, not turn false evidence into accepted mathematics.

## Normative documents and precedence

This is an explicit amendment, not a silent edit of CP-001D. For v2, the table names the selected contract. The frozen v1 specifications supply unchanged definitions only where no v2 override applies. An unresolved conflict is a specification defect; an implementation must not choose an interpretation opportunistically.

| Area | Selected contract |
|---|---|
| Foundation and known security corrections | [Foundation-security audit](../notes/analyses/CP-001E-foundation-security-audit.md) |
| Exact mathematical identity, direct meaning, witness maps, native certificates, current guards | [Native scaling amendment](../notes/analyses/CP-001E-native-scaling.md) plus the schema decisions below |
| Bounded bulk serving, persistent export inventories, generation sealing | [Exchange amendment](../notes/analyses/CP-001E-exchange-scaling.md) plus the NET2 bindings below |
| Formal client reuse, bounded views, nonprefix discovery, useful-growth evaluation | [Agent reuse and discovery](../notes/analyses/CP-001E-agent-reuse-and-discovery.md) plus the advisory grammar below |
| Local durable custody and maintenance | [Custody contract](../notes/analyses/CP-001E-custody-contract.md) |
| Preservation limits and assumptions | [Unbounded-time analysis](../notes/analyses/CP-001E-preservation-over-unbounded-time.md) |
| Unchanged local authority, one-shot claims, conservative recovery, physical deletion fencing, contextual opposition | Frozen [integration](OPERATIONAL-CORPUS-V1.md), [mathematics](OPERATIONAL-CORPUS-V1-MATHEMATICS.md), [network](OPERATIONAL-CORPUS-V1-NETWORK.md), and [organization](OPERATIONAL-CORPUS-V1-ORGANIZATION.md), subject to these overrides |

The analyses are part of this concept contract; calling them analyses does not make their chosen mechanisms optional. Their illustrative workload/rate models remain explicitly conditional rather than normative performance promises.

## Layer boundaries

| Layer | Responsibility | Must not supply |
|---|---|---|
| Formal evidence | Exact declarations, selected proof closure, qualified native checks and explicit assumptions | Claims of universal usefulness or physical availability |
| Local reliable service | Resource admission, exact storage, current guards, recovery, bounded disclosure and peer exchange | A remote truth verdict or global authoritative current state |
| Discovery and reuse | Existing-content indexes, formal matching, local checked application, inert interface views | Missing premises, semantic equality from names, executable peer instructions |
| Accumulation and custody | Finite selection, deduplication, affordable alternatives, durable allocations and repair | Guaranteed exponential discovery or unconditional eternity |

Authentication is cross-cutting operational machinery: it binds a peer to an offer, audience, or observation. It is not a vote on truth or a requirement for political attribution. An honest producer can err; an authenticated malicious producer cannot bypass checking.

## Foundation activation

Initial candidate:

- Lean `v4.34.0`, source `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`.
- Matching mathlib `v4.34.0`, source `5ed2965256430c3649e86755f9576b54eca72435`.
- Practical safe native declaration support, including mutual/nested groups, projections, checked opaque bodies, literal support and explicit standard axiom allowance.
- No peer source builds, imported `.olean` authority, plugin execution, new arbitrary axioms, unsafe/partial declarations, or compiler-assisted acceptance shortcuts.

The prior v4.22.0 pin is historical and withdrawn from deployment candidacy due known later soundness repairs. The new candidate needs a newly derived bootstrap; in particular its string basis uses `String.ofList`. Source inspection establishes inclusion of identified fixes, not complete soundness or executed qualification.

Locally qualified configuration determines which exact foundation, decoder, checker image, ABI and semantic options are active. Remote data cannot install them. The local state machine is CANDIDATE → QUALIFIED → ACTIVE, with ACTIVE → SUSPENDED/RETIRED on locally admitted incidents or owner policy. No elapsed timer or remote signature automatically restores ACTIVE. Corrected-foundation migration rechecks evidence under new identities; no old acceptance cache is inherited across foundation source changes.

## Native2 representation and registry

Common typed content addressing, canonical definite-array/uint/byte-string CBOR, canonical term DAG order, scoped binders, and generated native names are retained. Byte strings carry opaque data only where their type says so. Native integer conversions must be lossless under the explicit ABI constraints; resource increases cannot permit truncation.

The initial Native2 reader uses the following registry. All listed new allocations are specific to this amendment and do not change frozen schema-1 interpretation.

| Type/schema | Name and payload |
|---|---|
| `0x0001/2` | Foundation: `[nativeFamilyTag,kernelSourceCommit,SeedProfileID,NativeRulesID,ReservedNamesID]`; family 0 is Lean; commit is 20 bytes |
| `0x0002/1` | SeedProfile uses its existing descriptor grammar with the new source pin and newly frozen complete seed/export inventory |
| `0x0003/1` | NativeRules: `[nativeFamilyTag,ruleSchemaCode,featureCodes,allowedAxiomNamePaths]`; family 0, rule code 2 binds this Native2 reconstruction contract; features `[0,1,2,3,4,5]`; exact axiom paths are `propext`, `Classical.choice`, `Quot.sound` |
| `0x0004/1` | ReservedNames: `[SeedProfileID,sortedEntries]`; each entry `[namePath,exportIndexOption]` maps a reserved exact name to one seed export or marks it forbidden with `[]`; a present option is `[index]` |
| `0x0010/2` | NativeTermDAG: unchanged term/level grammar, replacing LogicProfileID with FoundationID |
| `0x0011/2`, `0x0018/2`, `0x0019/2` | Definition, InductiveGroup, OpaqueDefinition: unchanged safe descriptor shapes, with FoundationID and Native2 references |
| `0x0012/2` | SemanticContext: `[FoundationID,directSemanticRefSetRoot]` |
| `0x0013/2` | Judgment: `[SemanticContextID,universeArity,contextTypeTermIDs,conclusionTermID]` |
| `0x0014/2` | Proof: `[JudgmentID,proofTermID]` |
| `0x0015/2` | Replay: `[FoundationID,typedRoot,witnessMapRoot]` |
| `0x0016/2`, `0x0017/2` | Module and same-context opposing-evidence records retain existing shapes with Native2 IDs/FoundationID where applicable; neither is a mathematical authority shortcut |
| `0x0020/1` | Canonical direct-reference Patricia set nodes |
| `0x0021/1` | Canonical JudgmentID-to-ProofID Patricia map nodes |

Foundation.kernelSourceCommit must equal SeedProfile.sourceCommit; ReservedNames.SeedProfileID must equal Foundation.SeedProfileID; NativeRules.nativeFamilyTag must equal Foundation.nativeFamilyTag. Feature codes and axiom paths are canonically sorted and duplicate-free. The exact permitted axiom declarations/types in the seed must agree with the rule record; familiar names alone do not satisfy that check. Reserved-name entries sort by canonical name-path bytes, are duplicate-free, and their present indexes must name that exact seed export. The kernel's internal fresh-name prefixes remain inaccessible through contributed references. The descriptor inventory and reserved-name table are local qualification artifacts: a publisher cannot supply a different table to expand the foundation. The actual digest values cannot be claimed before those bytes are derived/frozen. This is an explicit release input, not an implementation invitation to improvise seed meanings.

The first Native2 acceptance policy **disables mixed legacy mathematical closures**. All contributed declaration, judgment, proof, context, replay and native-term references use the registry above and the same FoundationID. Seed/rule/interpretation and trie objects use their explicitly listed schemas. A schema-1/v4.22 object remains archival input and is re-exported/rechecked if migrated. The native note's qualified same-foundation reader view is a possible later extension, not enabled by this first deployment. Local caches, physical blobs and independent profiles may coexist without granting cross-profile native references.

Modules remain optional bounded packages of exact exports; they are not a mandatory ever-growing global manifest. Very large collections are local custody inventories or separately specified collection packaging, not a way to smuggle an unbounded Module array through a small control request.

### Meaning, evidence and exactness

Direct semantic references are recomputed from the judgment's telescope/conclusion syntax. Recursively addressed declarations bind transitive meanings. Proof-only dependencies remain outside statement identity but inside selected evidence and its footprint.

A Replay selects one exact witness per needed judgment. Traverse actual terms, declaration types/bodies, constructors and generated native interfaces; reject cycles in external selected support. The expected witness map reconstructed from this traversal must equal the submitted canonical map, including the proof root's own pair. Missing data give nondecision; missing/extra choices proven by complete available data reject that artifact. Hash membership or publisher counts do not prove closure completeness.

Patricia keys are the fixed injective 37-byte encoding of the current ContentID suite; L=296 bits. Branches split at the first differing bit and have two nonempty correctly partitioned children. Nodes have at most 256 canonical bytes. Equal maps therefore have equal roots irrespective of insertion history, conditional on content binding. Updating k entries needs at most O(kL) new nodes given a verified old map and exact delta. This is a representation bound, not a bound on arbitrary proof computation.

### Local checking certificates and current use

Cold checking establishes one exact complete closure. Warm checking can reuse receiver-owned certificates bound to typed root, selected witness-map root, foundation, image, adapter, interpretation, ABI and semantic options. New declarations check in a compatible actual native environment; a theorem previously inserted with witness A is not mislabeled as selected witness B.

The minimum current-use predicate is

\[
\operatorname{Reusable}(r,t)=
\operatorname{QualifiedCheck}(r)\land
\operatorname{CompleteProtectedLocalClosure}(r,t)\land
\operatorname{CurrentPolicyAllows}(r,t)\land
\operatorname{NoApplicableBlockingIncident}(r,t).
\]

Each conjunct refers to exact local evidence. A peer's status observation cannot satisfy the first two conjuncts. Availability and disclosure differ: retained private bytes can be usable locally but not publicly readable.

The authoritative local writer linearizes positive current observations/use pins only after revalidating relevant checker/policy, incident, protection-generation and deadline guards. A global epoch remains an observation label; unrelated new mathematics is not itself a reason to repeat an old proof check. Complete bounded incident-delta coverage can justify disjointness; lost coverage forces current-state revalidation or nondecision. Broad unresolved incidents use a breaker before descendant traversal. Binding-relevant map/context/replay objects belong to the exact incident support, not just leaf theorem IDs.

Unexpected storage faults invalidate availability guards. DAG ownership can retain an already protected shared subtree without revisiting every descendant, but cannot detect every silent hardware fault by logic alone. Integrity checks, physical storage assumptions and conservative recovery remain explicit.

## NET2 exchange and service generation

NET2 uses the same authenticated direct-peer and single-local-writer authority model. Its outer envelope has `version=2`; message roles and authentication bindings remain unchanged unless specified below. A NET1-only peer cannot be sent NET2 operations as if they were valid NET1 requests. Failed version negotiation gives explicit incompatibility; no silent downgrade trusts old mathematical evidence.

The legacy envelope `serviceEpoch` position means **admissionEpoch** in NET2. Local recovery fencing and warm-retention time-origin generation are separate state. OFFER/CALL may create new remote work only in the current unsealed admission epoch. Already claimed local work and exact preallocated reply continuations can survive a durable seal with unchanged allocations/deadlines. Old requests cannot recreate forgotten authority. Snapshot/export leases survive only as enumerated finite data scopes usable by new paid calls; they do not preserve old CALL rights.

Schema 2 of ServiceCall (`0x8004`) uses `[operation,arguments]`. Existing operation codes keep their meanings except old EXPORT_HEAD code 5 is unsupported in the first NET2 profile. New codes are:

| Code | Operation | Arguments |
|---:|---|---|
| 8 | BUNDLE1 | `[readScope,requestItems,requestedPayloadLimit]` |
| 9 | EXPORT_HEAD2 | `[rootReplayID]` |
| 10 | FIND_WINDOW | `[predicate,snapshotSelector,startPosition,pageCeilings]` |

Reused NET1 call/offer/result, public observation, export/retention/status and contact record types use schema 2 where they bind NET2 profiles, calls, epochs or observations. Their field layouts otherwise remain those of NET1; the changed schema prevents misinterpreting their authority. This bump applies only to reused types, not the expressly allocated new types. Exact raw chunks and byte manifests keep schema 1 because their unchanged byte meaning supplies no invocation authority. New export types are `0x8020/1` inventory node and `0x8021/1` export head.

The NET2 HELLO shape remains the existing one. HELLO_REPLY appends `[capabilityCodes,publicAdvisoryManifestIDs]`, with capability codes 1=BUNDLE1, 2=EXPORT_HEAD2, 3=FIND_WINDOW, 4=ADVISORY_READ1. Codes are sorted, unique, at most 16; hints are at most four; actual HELLO/control byte ceilings still apply. An absent capability cannot be inferred from a root hint. Each nativeProfileID field in NET2 names the exact FoundationID plus the advertised Native2 schema capability through the negotiated profile; that field does not claim an already qualified remote theorem.

### Bounded data transfer

BUNDLE1 accepts at most 256 canonically ordered explicit CID/range items, at most 16 KiB encoded request, and positive spans whose sum is at most requestedPayloadLimit, with `0 < requestedPayloadLimit <= 4 MiB`. Its immutable result has at most that requested payload allowance plus 64 KiB metadata. Provider computation/spooling and delivery have separately preallocated one-shot tickets. All ranges require exact public-root, live holder-bound export, or expressly disclosed advisory scope membership. No generic CAS read is introduced.

Read scopes are `[0,ReplayID]` for its currently authorized public native closure, `[1,exportLeaseID]` for one live holder-bound export, and `[2,advisoryManifestID]` for the bounded explicit advisory set below. Root read scope includes its binding native trie pages. Export scope also includes its reachable operational inventory pages; those pages do not recursively list themselves as mathematical content.

Large result delivery uses the original paid reply job, not new per-frame remote work. New outer message kinds are 10=BODY_START, 11=BODY_DATA, 12=BODY_END. Their bodies are `[offerID,actionID,resultCode,resultMetadata,bodyDigest,totalBodyBytes]`, `[offerID,actionID,offset,fragmentBytes]`, and `[offerID,actionID,bodyDigest,totalBodyBytes]`. Fragments are at most 256 KiB and consecutive; the full body commitment is SHA-256 of the ASCII domain `DTMKN-NET2-BODY`, canonical call ContentID bytes, u64be body length, and canonical result-body bytes in that order. This digest supplies integrity, not mathematical authority. BODY_START requires resultCode=0 (OK) for a completed typed bundle. Its resultMetadata must name that exact call and body length; outcomeDigest equals SHA-256 of ASCII `DTMKN-NET2-OUTCOME`, canonical call ContentID bytes, u16be(0), and bodyDigest in that order. Per-item codes distinguish OK_SLICE=0, NOT_SERVABLE=1, INVALID_RANGE=2, UNKNOWN_LOCAL_AVAILABILITY=3. The result body is one array containing exactly one row per requested item in request-ordinal order. A result row begins `[requestOrdinal,itemCode]`; OK_SLICE appends `[CID,totalLength,offset,payloadBytes]`, other codes append no private object metadata. Failed top-level operations use ordinary bounded RESULT with no body stream. Whole bundle success is not whole-mathematics acceptance.

The receiver checks all ranges, integer arithmetic and aggregate quotas before allocating, and verifies each completed object's own typed ContentID. Partial data remain inert staging. Independently verified objects can survive an interrupted body within explicit staging authority; reuse of them does not claim the service ended successfully. Retry/resume requires fresh independently admitted work and never resets cumulative budgets.

For BUNDLE1, publicAssessmentDigestOption is `[0]`, the inherited NET resultMetadata absent-option encoding (not the separate `[]` convention of newly defined advisory records); no private or public theorem verdict is silently attached to a byte-serving result. The resultMetadata encodedBodyBytes, BODY_START totalBodyBytes and BODY_END totalBodyBytes must agree, and START/END bodyDigest must match the computed full-body digest. Each ordinal is exactly its zero-based request index, once. An old-origin BODY stream may finish after a clean admission seal only under its exact retained already-claimed reply continuation; this does not allow an old CALL to create work.

### Export inventories and archives

EXPORT_HEAD2 serves an already built exact inventory or declines pending independently admitted local construction. The inventory is a canonical persistent CID-to-payload-length Patricia map, not consecutive packed pages that shift after each insertion. Exact native closure membership is independently reconciled by the receiver. The export head binds exact root, issuer/holder, lease, inventory root/count/bytes, required profiles and finite timestamps; its maximum encoded size is 4 KiB, at most 16 profile IDs, and aggregate counts are checked uint64. The current first native profile needs one foundation. More heterogeneous archives require separate scopes or a later profile.

The head's leading version value is 2. Its successful ordinary RESULT body is `[headCID,headPayloadBytes,inventoryRootNodePayloadBytes]`; headCID has type/schema `0x8021/1`. The receiver recomputes that CID, checks the exact head fields against its call/holder, and recomputes the embedded root node's CID against the head's inventoryRootCID (`0x8020/1`). The head/root-node byte bounds and normal RESULT bounds all apply. Returning these bytes supplies a bounded starting point, not evidence that the whole inventory is already checked. Failure returns the ordinary bounded RESULT code with no purported export. No giant inline inventory list is permitted.

Logical inventory nodes add real cost: an N-entry map has 2N−1 nodes; native-plus-inventory transfer can contain 3N−1 objects before sharing. No arithmetic example that counts N payload objects silently includes those extra nodes. Cold archive work can be linear in the complete closure; warm small-delta inventories share unchanged nodes. An offline archive is a finite length-delimited record stream, not a single enormous frame. Importing bundled checker bytes never grants execution permission.

NET2 retains small frame/request/fragment bounds and finite local resource admission. It removes NET1's aggregate mathematical-closure hard ceiling; **it does not remove local finite budgets**. Term/object/declaration depth, trie depth, total closure objects/bytes, snapshot allocation and active transfer windows are separately accounted. The default limits can remain modest. Larger admitted profiles require actual local capacity, not new theorem identities. No receiver is required to fit an arbitrarily large closure.

## Advisory2: an exact inert client grammar

To close the gap between a safe mathematical corpus and usable local Lean tools, the downloadable deliverable includes an optional explicit-application client plus bounded declarative views. These are not a human-intention interface. Human-readable aliases are optional labels; removing them leaves native mathematical reuse intact.

Use organizational types `0x8120/1` for AdvisoryManifest, `0x8121/1` for LibraryViewPage, and `0x8122/1` for CollectionGuidePage. An AdvisoryManifest is a canonically sorted duplicate-free array of `[kind,dataCID,payloadLength]`; kind 0 means LibraryViewPage, 1 means CollectionGuidePage and must agree with CID type. Native records, unknown kinds and nested advisory manifests are not allowed as members.

Manifest limits: 64 KiB, 1024 members. Every member: at most 1 MiB. Manifest plus all members: at most 8 MiB and 4096 entries. The receiver also imposes aggregate cache/activation/work bounds. Duplicated member IDs reject the manifest. The manifest is explicitly in read scope without listing itself.

A LibraryViewPage payload is `[FoundationID,entries]`. A `targetRef` uses the mathematical constant-reference grammar for an external seed, definition, judgment, group member or opaque declaration; group-local/bootstrap-only references are forbidden. An optional replay hint is `[]` or `[ReplayID]` and grants no read authority. Entries are:

| Tag | Payload | Local activation check |
|---:|---|---|
| 0 | `[0,labelBytes,targetRef,replayHint]` | Exact locally checked target; label is display/alias only |
| 1 | `[1,targetRef,binderInfoCodes]` | At most 256 codes in 0..3, no more than the available syntactic consecutive outer Pi binders of the reconstructed checked constant type (including a Judgment's abstracted telescope), starting at position zero; an excessive list cannot activate, and a shorter list leaves later binders explicit/default. The codes only guide an explicit application builder |
| 2 | `[2,GroupID,typeIndex,classHint,fieldLabels]` | Exact checked one-constructor non-indexed native structure type; classHint 0/1 is search metadata, not an axiom; each `[fieldIndex,labelBytes]` uses the native projection field numbering after uniform parameters |
| 3 | `[3,classGroupID,classTypeIndex,instanceRef,replayHint]` | Locally check actual instance type against the exact advertised class head; no automatic assertion that it solves an arbitrary query |
| 4 | `[4,JudgmentID,replayHint,orientation]` | The checked conclusion after its telescope/outer Pi binders has the exact admitted seed Eq head after bounded local conversion; orientation 0 means left-to-right, 1 right-to-left. Each actual dependent rewrite still requires a checked application/transport |

Each label is at most 256 UTF-8 bytes, with no ASCII controls or bidirectional formatting controls. No label is interpreted as a path, command, URL to execute, source code or instruction. Presentation clients must escape markup and use an exact-ID fallback on ambiguity; different labels cannot rebind one native constant. Each page has at most 1024 entries; field-label lists at most 256. Entries sort by canonical entry bytes with exact duplicates forbidden; different conflicting hints remain separate, never silently resolved by publication order.

Every resolved mathematical target, interface and replay hint must use the page's exact FoundationID; seed references are interpreted only through that foundation's qualified export inventory. A mismatched target keeps the entry inactive and reports the mismatch, not a cross-foundation translation. Field-label lists are strictly increasing by fieldIndex with no duplicate field index; every index is checked against the actual generated constructor field count and native projection rules. Labeling a field does not certify projection admissibility at every universe/context instantiation; every constructed projection is checked where used. Multi-constructor or indexed groups are not representable as this tag-2 structure convenience. Non-Eq statements and failed/budget-limited normalization do not activate tag-4 rewrites. They remain ordinary possibly useful mathematics outside this particular convenience.

A CollectionGuidePage is `[FoundationID,entries]`; each entry is `[interfaceRefs,publicContacts,replayHints]`, with at most 16 exact external interface refs, eight contacts, and 16 ReplayID hints. The contact shape is exactly `[nodeID,endpoints,nativeProfileIDs,indexKeys]` from the bounded GET_ROUTES record, not the simpler offline `[nodeKey,endpoints]` form; inherited endpoint/profile/key count, encoding, disclosure and connection-admission rules apply. Each list is sorted/duplicate-free by canonical bytes; at most 1024 entries/page. These are existing-content routing hints, not tasks, universal subject ontologies, proof evidence or custody promises. Contact validation cannot cause recursive route following. The whole bundle's 4096-entry limit includes both page kinds.

Receipt permits only hash/schema-checked inert storage and visibly tentative display. Semantic activation is **per entry**, after its required exact targets are locally checked and allowed; it does not require importing every target in a guide or activate neighboring entries. A replay hint does not choose a witness until independently accepted. View references do not expand read scope. Competing instance/rewrite hints receive local finite search/rewriting budgets; cycles, misleading hints and expansion bombs cannot alter kernel acceptance. Text is never fed to an agent as trusted system instructions.

Provider disclosure activation validates the complete manifest and all listed members, including actual lengths and the aggregate entry count. The receiver can reject excessive declared byte totals immediately but cannot infer aggregate entry counts from lengths. Partial pages are tentative inert data. Before this received bundle is marked conforming or any entry is semantically activated through it, every listed payload must match its declared length/hash/type, all page schemas must pass, and the sum of actual entries must be at most 4096 within the aggregate byte/allocation ceilings. This is bounded advisory-data validation, not import of the referenced native proofs. A failed/abandoned bundle keeps no semantic activation or free persistent retention; already checked data may remain only under independent local cache authority.

## Finding and applying existing mathematics

Use exact IDs and checked shared interfaces first. The client issues a bounded portfolio of existing-content predicates; it may use embeddings/LLMs to propose candidates but not to authorize native equality or discharge missing premises. REUSE1 takes an exact local formal context/expression and emits candidates, proposed argument maps, residuals and cost estimates. These are ephemeral local interactions, not a public research registry.

FIND_WINDOW adds an inclusive lower-bound seek in a fixed provider-public descriptor ordering, bound to exact predicate, snapshot, extractor and planner. `snapshotSelector` is `[0]` current authorized view or `[1,liveSnapshotToken]`; a new `startPosition` is `[0]` BEGIN or `[1,publicDescriptorID]`, and the boundary need not exist as a record. Resume uses `startPosition=[2,continuationToken]` together with the corresponding `[1,liveSnapshotToken]`, not a forged new boundary. The provider-authenticated continuation binds the exact snapshot/holder/predicate/extractor/planner, original lower boundary, next unprocessed position and original expiry. All must agree with retained snapshot state and this request; page ceilings can be lowered but cannot exceed its admitted profile/lease constraints. Inconsistent tokens or a current-view selector on resume yield STALE_CURSOR/REQUEST_MISMATCH rather than a new scan. Replies state their half-open processed interval and `END` or next position, and return the next authenticated token when eligible. A matching record cannot be skipped because the output was full. There is no implicit wrap or completeness claim below the requested boundary. Lifetime remains finite across generation seals.

Exact/unambiguous queries and ordinary STRUCT1 remain baselines, interpreted under the explicit Native2 profile and current organization schema. STRUCT2 and learned lanes are optional research/client extensions with candidate-only semantics; this checkpoint does not instantiate an interoperable STRUCT2 ExtractorID from a merely suggested feature budget. Any public deployment of a new extractor must first fix its exact versioned extraction/token/normalization/truncation contract, then negotiate its distinct ID; it cannot reuse another extractor's keys or advertise interoperability from a label alone. The selected exploratory feature budgets and evaluation cases are in the reuse note. A heuristic extractor can be valuable without a universal optimality proof; actual end-to-end coverage/cost must be measured. Structural hash collisions can change candidates, not mathematics.

For candidate type `p : Π x₁:A₁, …, Π xₙ:Aₙ, B`, the client can claim CHECKED_LOCAL_APPLICATION only after each dependent argument and the resulting application/transport pass the selected native checking path. Missing premises remain residuals. Differently encoded structures need exact checked adapters, not common English names or vector similarity. Independent agents producing identical canonical descriptors deduplicate; independence alone does not force a new GroupID.

Initial interactive envelopes in the reuse note bound pages, peers, descriptors, statement probes, bytes, CPU and wall time. Deep import is separately admitted. A finite failed search means unknown/missed-under-this-scope, not that no useful theorem exists.

## Accumulation, local selection and durable custody

No accepted theorem is mathematically invalid merely because it is trivial, duplicated semantically, unused, expensive or unfashionable. Exact byte/statement deduplication is deterministic; semantic equivalence is itself an evidence-bearing relation and generally cannot supply a universal canonical representative.

Nodes choose what to index, cache and preserve. Usage observations, checked downstream references, proof cost, alternative assumptions, structural coverage and learned recommendations are permitted finite selection signals. They are not authority to override a proof failure. Usage is not causal necessity: a valid proof can be padded with an unused argument. The baseline caps those signals and reserves exploration rather than counting raw citation chains as guaranteed growth.

Custody1 is **local-only**, owner-funded durable retention with bounded maintenance/repair and explicit release rules. It publishes no new wire-level permanent-storage certificate. Existing RetentionAck/export/provider observations retain their weaker scoped meanings. Signed statements do not prove independent failure domains or perpetual service. Maintenance budget expiry marks maintenance degraded; it does not silently cancel an owner-authorized durable pin.

Preservation targets distinguish exact selected replay evidence from judgment recovery via a separately checked replacement witness. A new-foundation encoding is not automatically the same exact JudgmentID. Planned handoff remains a bounded attempt followed by whatever explicit local release condition was authorized; the base protocol cannot prove a successor will never delete its copy. The custody contract supplies the detailed states, records and transitions.

Accumulation is assessed over scoped retained knowledge and demonstrated reuse, not just submissions or historical checks. Report unique protected closure bytes, available checked judgments, actual checked applications, missing/invalid/unknown outcomes, cold/warm costs, alternatives and repair burden. A finite evaluation pool is not all mathematics. No quantity implies exponential useful growth without an empirically justified generation/supply model.

## End-to-end paper executions

### Cold connected acquisition

1. A installs a locally selected qualified foundation/image and obtains at least one willing contact. If either is missing, A can still inspect inert bytes but cannot claim native reusable results.
2. A independently funds bounded discovery, receives public descriptors/views, and selects an exact ReplayID. No received descriptor, score, alias or provider signature is an acceptance certificate.
3. A funds staging plus complete-closure acquisition/checking. B serves explicit bundles under a public root or finite exact export scope. A validates inventory/native trie nodes as data and follows only qualified bounded references.
4. A independently reconciles exact selected witnesses/declarations, reconstructs/checks native groups and definitions in topological order, records actual assumptions, and rejects unsupported/cyclic/malformed evidence. Resource failure is nondecision.
5. A protects the complete local closure and commits current guards. Only now is it locally reusable. A can activate the relevant per-entry client conveniences and check a local application.
6. Public serving, warm cache and durable custody are separate locally admitted choices. Successful import alone does not impose a permanent replication obligation.

For the explicit 16,384 small-object/32-MiB workload, BUNDLE1 reduces 32,768 per-object manifest/chunk service calls to 64 bundles **if those needed object IDs are known and the lengths fit**. This counts the stated payload objects, not additional export inventory nodes. A deep undiscovered chain can still impose causal rounds. No executed throughput result is asserted.

### Warm reciprocal contribution chain

A has a compatible checked environment and protected closure Cᵢ. Its private investigator constructs a new definition/theorem referring to selected earlier declarations. Export produces exact new objects, a direct statement context and a persistent witness-map extension. Local and receiving warm nodes reuse unchanged receiver-owned certificates and compatible native environments, check the actual new declaration, and protect shared bytes through DAG ownership. A second agent can then repeat the process.

For an ordinary constant-direct-dependency extension family, genuinely new native information and witness-map nodes are bounded per stage by the corresponding syntax plus O(L); optional inventory/support updates may add O(L²), not an unacknowledged zero. N stages avoid the old forced Θ(N²) flat transitive lists. A different witness for many shared judgments, a large new term or expensive kernel conversion can still require large work. This is an efficiency argument for the chosen family, not a law of exponential mathematical productivity.

### Parallel independent branches

A and B derive different results using overlapping mathematics. No global order or consensus is required for their content identities. C unions compatible exact support only; conflicting selected witnesses require a consistent new selection or separately checked reconstruction/environment branch. A received proof of Γ ⊢ ¬φ does not invalidate an accepted Γ ⊢ φ without analyzing the compatible composed assumptions; an inconsistent Γ is different from a closed foundation inconsistency. Actual checked closed False under an adopted basis triggers its incident policy.

### Seal during a long import

B's control store reaches its compaction threshold while a separately funded import and a completed-but-undelivered bundle exist. The durable seal advances the admission floor, cancels unused old offers, retains exact claimed work plus fixed reply continuation and live data leases, and preserves spend counters. A new-epoch call can use an old-origin live export lease; replaying the old call cannot execute again. A real crash instead changes recovery fencing and invokes conservative finalization. Clean sealing is not crash recovery.

### Partial loss and a checker incident

A custodian loses a physical object: availability becomes degraded before reliance resumes; repair fetches exact bytes under fresh funded authority. An unchanged trusted historical check can become usable after exact bytes/protection return. If instead its checker is suspended, refetching identical bytes cannot restore trust. It needs a qualified repaired foundation/image and appropriate independent rechecking. Custody may preserve historical bytes while mathematical-current-use remains suspended.

## Deliverable and qualification boundary

The eventual downloadable software comprises a local node/store/admission authority, pinned Native2 decoder/checker adapter, an untrusted producer-side exporter, exact client import/application support, bounded public indexes/views, peer/offline transfer, and optional local custody. It must be useful without identity-based attribution, blockchain consensus, remote-execution SNARKs, a central model, or online training. Agents may privately train on corpus material; model weights are not a substitute for recoverable selected evidence.

The concept deliverable is this integrated contract with the attached mechanism notes, adversarial paper traces, source evidence and audit dispositions. The next release qualification must exercise the actual adapter/bootstrap, realistic library slices, exact native/transport conformance, concurrent/crash/storage faults, discovery/application utility and custody load. Nothing in this checkpoint authorizes implementation or claims those executions happened.

Practical acceptance criteria are high but not impossible: coherent chosen mechanisms; no known unresolved contradiction in the intended contract; explicit environmental assumptions and nondecision behavior; completed representative end-to-end operations at acceptable declared cost; and demonstrated bounded failure behavior. No proof of heuristic optimality, all-future-resource supply, universal discoverability, or absence of every unknown implementation bug is promised. Known defects must be repaired, not hidden inside these qualifications.
