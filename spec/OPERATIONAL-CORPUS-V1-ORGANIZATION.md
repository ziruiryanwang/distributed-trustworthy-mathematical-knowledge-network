# Operational corpus v1: organization, retrieval, and bounded accumulation

Date: 2026-09-19  
Status: Reviewed candidate paper specification; not implementation-qualified  
Profile: ORG1, composed with the native mathematical and peer-service profiles  
Implementation: None. Record descriptions, algorithms, arithmetic examples, and fixtures below are specifications, not executable code or measured results.

## Scope and concrete decisions

The [formal knowledge contract](FORMAL-KNOWLEDGE-CONTRACT-v0.md) governs this document. Independent people and agents investigate outside the corpus. ORG1 organizes existing formal objects, supplies bounded retrieval, and decides how a receiver spends its own resources. It introduces no human-intention fields, mathematical work items, goal keys, unanswered-question catalogue, or research scheduler.

ORG1 chooses a deliberately small operational baseline:

1. Each node maintains exact local object and judgment indexes, plus bounded structural indexes extracted from locally checked formal syntax.
2. Network search is a finite local scan or direct requests to at most four receiver-selected peers. A receiver does not recursively forward a search.
3. Exact judgments are grouped independently of their proofs. Different proof witnesses and different axiom footprints remain distinguishable.
4. Structural signatures and optional learned proposals generate candidates only. Native checking decides formal applicability.
5. A fixed receiver-owned exploration allocation allows some unfamiliar content to be checked; new publisher identities do not create new allocations.
6. Automatic proof-family retention is bounded. Original-byte promises, active dependencies, and explicit funded retention roots override automatic eviction proposals.
7. The baseline performs exact chunk sharing. A proof-replacing compression is a separately checked mathematical contribution, not an automatic storage rewrite.
8. Accumulation is measured through several scoped operational quantities. No global importance score or decidable semantic-novelty oracle governs formal recognition.

The named constants are initial engineering choices for a runnable-on-paper profile. They are not universal mathematical limits or proven performance optima. A deployment can advertise a different versioned resource profile, but cannot silently enlarge a received request's budget or reinterpret a result.

## Composition with the other layers

The native mathematical profile supplies:

- `JudgmentID`: the exact closed contextual judgment, including its logic/seed, ordered universe parameters, definitions, and statement dependencies;
- `ProofID`: the exact pair of a JudgmentID and native proof term, distinct from the judgment;
- `ReplayID`: the complete selected auxiliary-proof witness map and reachable native definition closure; it is a separate identity from ProofID;
- `DefinitionID` and `ModuleID`: exact declaration and export identities;
- a `ValidationKey` binding the chosen proof/dependency witness, checker, environment, options, and applicable native policy;
- receiver-extracted dependency and axiom/trust-feature footprints;
- current strict mathematical reliance, including defect handling and available closure.

ORG1 does not reconstruct any of those identities from a theorem name, an embedding, or a publisher's declaration of its dependencies. Native syntax in the practical `Lean-Native/v1` mathematical profile is a pinned, safely replayed Lean declaration/expression DAG; source text, peer-produced executable modules, and arbitrary build scripts are not index extraction inputs. The smaller `Lean-Expr-6/v1` subprofile remains a conformance fixture, not the practical corpus's universal expressive ceiling.

The unit of assessment, cost comparison, and retained proof selection below is an evidence candidate \(r=(\operatorname{ProofID},\operatorname{ReplayID})\). The same proof term can have different selected auxiliary proof witnesses, costs, and trust footprints. Bare ProofID equality therefore does not deduplicate replay assessments or justify substituting one closure for another. A retained proof root in this document means its exact ReplayID closure. Practical `Lean-Native/v1` permits only its exactly pinned standard foundation axioms (`propext`, `Classical.choice`, and `Quot.sound`) and native quotient rules; the actual transitive footprint remains explicit, and a receiver may require a stricter subset. The conformance subprofile's examples can have an empty axiom footprint. Arbitrary peer-created axioms, admitted gaps, or executable native-evaluation shortcuts are not silently enabled.

Nonproof replay roots are native definitions, inductive groups, or checked opaque declarations according to the mathematical profile's tagged root union. They have exact native root IDs and ReplayIDs, but no invented JudgmentID or ProofID. Proof-family selection applies only to proof roots. General object/declaration lookup, authorized transfer, dependency extraction, and root-union resource accounting apply to all supported root kinds.

The peer-service profile supplies bounded `HINT`, `FIND`, `PAGE`, manifest/chunk transfer, current-status requests, and cancellation. Its default page is 64 descriptors, its maximum is 256, and the encoded page including its envelope is at most 1 MiB. A descriptor is at most 4096 bytes. ORG1 stops a page early when the byte limit would be exceeded.

Wire record type codes `0x8100` through `0x81FF` are reserved for organization records. Record names below are paper field labels; canonical wire values use the common fixed-array, unsigned-integer, byte-string encoding. No textual field name, formal-language name, or participant-supplied label creates an authority or service class. SHA-256 typed content identities and the 256 KiB transfer-chunk profile come from the common object/transport specification.

Operational grants, reservations, single execution claims, authoritative metering, atomic finalization, and expiry remain mandatory for protected work. They describe work such as checking a proof or reading a posting list, not an obligation to discover mathematics. Query keys identify service requests; they are not legacy `GoalKey` objects.

## Local state and the meaning of an index

Let a receiver's snapshot be

\[
S=(\mathcal V,\mathcal R,\mathcal G,\mathcal I,e,\rho).
\]

Here \(\mathcal V\) contains finite retained validation assessments; \(\mathcal R\) the authorized retained roots and their terms; \(\mathcal G\) the exact local dependency graph needed for active-root safety; \(\mathcal I\) the index materializations; \(e\) the reliance epoch; and \(\rho\) the local resource/retention policy version. Historical assessment, current allowed reliance, current byte availability, and a promise to retain bytes are separate fields.

An index entry means that an exact record appears in a named local index snapshot under a declared extraction schema. It does not mean that the receiver has seen all public mathematics, that a remote provider still has the bytes, or that the indexed assessment is currently acceptable for use.

Each snapshot also binds its exact collection. Remote `FIND` is restricted to the receiver-authorized `PUBLIC_SERVE` collection: only roots explicitly selected for public service and their authorized public projections can appear. A local authenticated application may have a separate index of local-only retained material. Remote queries cannot select that collection or infer its contents through counts, failure reasons, cursor positions, or postings. Native checking or local retention alone does not authorize publication.

This is operational sharing authority, not a human-intention assessment. The public root is an exact ReplayID. A subsequent remote byte read must use the network profile's public-root or audience-bound export read scope and pass exact closure membership; knowing a content hash does not authorize reading arbitrary local CAS content.

Index snapshots are immutable for the lifetime of their bounded pins. Current reliance is evaluated separately against a current local epoch. A historical snapshot must never be presented as current by overwriting its epoch label. Index replacement and compaction publish a new snapshot only after its complete local transaction succeeds.

The mandatory exact tables cover every locally retained indexed mathematical root. An object can remain in temporary staging without entering these tables. If a node cannot afford a root's mandatory exact metadata and dependency bookkeeping, it declines durable root admission; it does not retain a supposedly manageable root while silently omitting the references needed for safe collection or correction.

### Index records and their authority

| Record | Type code | Contents and bounds | Authority |
|---|---:|---|---|
| `IndexDescriptor` | `0x8101` | Judgment/definition identity, ProofID and ReplayID where applicable, validation-assessment reference, footprint/closure references, extractor version, bounded structural keys, extraction flags; at most 4096 bytes | A remote descriptor is a hint; a local trusted descriptor is derived from locally admitted native material |
| `FindPredicate` | `0x8102` | Mode code, exact identifiers or at most eight structural predicates, exact extractor version, local scope, page/scan ceilings | Selects existing candidate records; allocates no resources |
| `IndexSnapshot` | `0x8103` | Receiver/service epoch, index schema, source admitted-state root, materialization root, local sequence, coverage declaration | Binds a specific local materialization, not mathematical truth or global completeness |
| `ProofFamilySelection` | `0x8104` | JudgmentID, considered ProofID/ReplayID pairs, assessment/cost snapshot, selected automatic roots, reasons, policy version | Receiver-local cache/retention decision only |
| `OrganizationCounters` | `0x8105` | Bounded interval counters and denominators, policy/snapshot references, saturation flags | Operational observation, never evidence of theorem validity or causal usefulness |
| `PreservationAssessment` | `0x8106` | Exact finite preservation scope, old/new roots, reconstruction relation, checker basis, cost scope, local outcome | May establish the declared preservation relation after ordinary native checking; creates no deletion authority |
| `PublicIndexDescriptor` | `0x8111` | Exact public native identifiers, ReplayID, bounded derived formal keys, extractor flags, and public service observations; at most 4096 bytes | Self-contained candidate projection for PAGE; contains no private assessment/ValidationKey/control-ledger references |

Large footprints and complete dependency lists are referenced by immutable roots rather than embedded in a descriptor. Resolving those references costs a separately admitted operation. A publisher's claimed extractor output, cost, or footprint cannot populate a trusted local index without receiver-side extraction/checking.

The full `IndexDescriptor` and its assessment references are local records. Network `PAGE` exposes `PublicIndexDescriptor` only. A remote receiver reconstructs formal dependency and axiom footprints from the authorized native replay closure; PAGE does not turn local validation ledgers or operational records into generally fetchable objects. Public descriptors are hints carried by the page, not a new arbitrary-CAS-read permission.

Metadata is not free. Descriptors, posting entries, cursor pins, assessment records, retention references, reverse edges, compaction workspace, and recoverable transaction records are all charged. A descriptor may be evicted while its underlying object survives; the advertised index scope must then cease claiming that descriptor is present.

## Exact and structural key schemas

### Exact materializations

The following tables have complete semantics over their named local admitted snapshot:

| Table | Key | Value |
|---|---|---|
| Object lookup | Typed content ID | Local byte/manifest location and explicitly separate availability state |
| Judgment lookup | Exact `JudgmentID` | Retained proof-descriptor IDs and their assessment references |
| Definition/module lookup | Exact native ID | Retained declaration/export descriptors |
| Direct dependents | Exact referenced ID | Retained root/proof IDs whose receiver-extracted immediate dependency edges name it |
| Certified relations | Endpoint native ID plus relation-kind code | Retained native relation-proof IDs naming that exact endpoint |

The dependents table is not a transitive-reachability oracle. A transitive walk requires additional bounded work. The full dependency graph needed for live-root and incident safety is not replaced by the sampled structural keys below. If a required exact graph exceeds the node's admitted edge/storage envelope, root admission is declined or deferred.

Judgment lookup groups only identical native judgments. A weaker context, different definition body, changed universe order, or different statement is another judgment unless the native profile identifies it exactly. A theorem name is never this key. A proof that uses different admitted axioms can be another witness of the same judgment when the native statement context is unchanged and its distinct transitive proof footprint is disclosed.

### Structural extraction version `STRUCT1`

Extraction is a bounded deterministic pass over already resolved native syntax. It does not unfold arbitrary definitions or search for proofs.

For each statement descriptor:

1. Traverse the canonical expression representation in pre-order, preserving application argument order, de Bruijn binder indices, universe-parameter positions, and exact constant references. Visit at most 4096 expression occurrences and descend at most 64 constructors.
2. Record the first 32 distinct referenced constant IDs encountered. Record whether traversal and symbol extraction were complete. If either bound is reached, retain the selected keys and set `SYMBOLS_TRUNCATED`; do not fabricate keys for unvisited subterms.
3. Extract a conclusion head by stripping at most 64 leading dependent function binders and following at most 64 application-function edges. The key is the resulting exact constant ID or a nonconstant constructor tag, together with the extraction version. Exhaustion gives `HEAD_UNKNOWN`.
4. Form a bounded raw shape from at most 256 constructor occurrences to depth eight. Retain constant IDs and binder indices; replace literal values with their native literal-kind and encoded-length bucket. Truncated subtrees become an explicit cut marker. The shape is a candidate key, not a statement identity.
5. Optionally generate `BETA128` shape in a separately budgeted extraction substep: perform at most 128 capture-avoiding beta/let reductions, create at most 4096 expression occurrences, and then use the same shape procedure. No delta unfolding, rewrite-library search, or arbitrary evaluator execution is permitted. An exhausted budget produces `NORMALIZATION_PARTIAL` and cannot erase the raw shape.

The baseline enables raw keys and disables `BETA128` unless the receiver's advertised `STRUCT1` profile explicitly allocates its cost. Keys of different extraction profiles occupy different namespaces. A partial shape can be matched as a partial candidate feature; it must not masquerade as a complete normal form.

Exact native equality and any reduction relied on mathematically remain the native verifier's responsibility. Bugs in structural extraction may damage recall or consume the admitted index budget, but may not establish an equality or alter the exact statement.

A symbols query therefore means “contains these keys in the declared extracted key set,” not “the full theorem contains exactly these symbols.” Its negative result is not a complete mathematical exclusion. The difference is especially important for a large statement whose relevant constant occurs after the extraction limit.

## Retrieval protocol with fixed modes

ORG1 exposes five `FIND` modes. Byte acquisition itself uses the object/manifest/chunk operations rather than a second search language.

| Code | Mode | Request meaning | Result |
|---:|---|---|---|
| 1 | `EXACT_JUDGMENT` | An existing exact JudgmentID | Locally indexed proof descriptors for that judgment |
| 2 | `MENTIONS_ALL` | One to eight exact symbol keys in one extraction profile | Descriptors whose extracted sets contain all requested keys |
| 3 | `HEAD_SHAPE` | A head or shape key, plus at most seven other extracted-key predicates | Structurally matching descriptors; no applicability conclusion |
| 4 | `DEPENDENTS_DIRECT` | An exact object/declaration/proof/replay ID | Immediate reverse-edge matches in the stated local graph snapshot |
| 5 | `RELATIONS` | Exact endpoint ID and one relation-kind code | Candidate native relation proofs involving that endpoint |

There is no free-form question, natural-language search field, theorem-synthesis request, global novelty request, or persistent subscription to an unsolved statement. Local collection filters are finite mathematical predicates over object kinds, exact foundations, module roots, or these formal keys. They express which existing material a node is prepared to collect; the system does not infer an investigator's motivation.

### A page algorithm

For an admitted request, the server pins one already committed local snapshot and evaluates a canonical predicate digest. A conjunction starts from its shortest available posting list; ties are broken by canonical key bytes. Entries are traversed in ascending exact descriptor ID order and checked against the other predicates. Exact-judgment, relation, and reverse-edge modes use their corresponding ordered table.

The default per-page envelope is:

- 8192 inspected posting entries;
- 0.25 CPU-seconds and two wall-seconds, each enforced independently;
- 16 MiB temporary query memory;
- 64 returned descriptors, at most 256 by explicit admitted request;
- at most 1 MiB encoded response including envelope and cursor.

The first exhausted bound stops the scan. A record is not skipped merely because a time limit arrived between testing it and committing the page position. The snapshot/query cursor records a position from which an unfinished record is reconsidered; deduplication by descriptor ID makes harmless repeat delivery acceptable. A cursor must not advance beyond unexamined records.

Concretely, `scanPosition` is `[0]` for the initial position, `[1,nextDescriptorID]` for the least source-list descriptor not yet completely processed, or `[2]` for the completed scan. Resumption at `[1,id]` uses the inclusive lower bound of `id` in the exact pinned source list. If a match cannot fit the current page, that match remains the next unprocessed descriptor. If a time limit interrupts testing or output commitment, the same descriptor remains unprocessed. Only a completed nonmatch or committed result permits advancing to the next source descriptor. The cursor also binds the chosen source key and planner version through the query/snapshot/planner context; it never reconstructs the source from a newer shortest-posting calculation. An implementation may resend a committed boundary descriptor after recovery, but cannot omit it.

Successful page bodies use `END_OF_LOCAL_MATCH_SCAN`, `MORE_RESULTS`, or `PARTIAL_SCAN_BUDGET`; unsupported profiles and stale cursors are separate service errors. An empty `PARTIAL_SCAN_BUDGET` page is not an empty completed scan. Reaching the output cap with unscanned entries returns `MORE_RESULTS`.

The opaque authenticated cursor binds service epoch, requester authority, snapshot, predicate digest, page position, and monotonic deadline. Its default lifetime is 120 seconds. A new boot/service epoch, missing snapshot pin, changed query, different requester, or expired deadline yields `STALE_CURSOR`; the server must not continue it against a different snapshot. A bounded snapshot pin is resource-accounted. A client that needs more time restarts against a newly named snapshot and deduplicates results.

### Completeness and current-status labels

An honest implementation's `END_OF_LOCAL_MATCH_SCAN` means it finished the predicate scan over that particular snapshot and extracted-key schema. A remote answer carries `SERVER_DECLARED_LOCAL_SNAPSHOT` coverage. A signature, Merkle root, or cursor does not prove that a malicious server built a complete index, included all admissible objects, or returned every matching record.

A client may establish a stronger finite scoped statement only by obtaining and independently checking the specified enumeration/coverage evidence under a separately admitted contract. ORG1's baseline does not promise that facility.

Even a genuinely complete local exact lookup establishes no world-wide nonexistence result. An indexed historical validation record is also not a current `ACCEPT`: actual reliance fetches the selected evidence and checks its current local contract/epoch. A remote status is a scoped remote assertion until the receiver completes its own acceptance path.

### Candidate routing

The receiver queries its local index first. If its caller has authorized network discovery, it sends the same bounded predicate to at most four selected peer services per admitted lookup round. Those services answer from their own indexes and do not forward the request. Each remote page consumes a separate bounded operation; a page cursor never grants unlimited continuation. A caller's lookup session has explicit aggregate call, byte, and time ceilings, rather than an unbounded promise to find a result.

The receiver maintains NET1's bounded `PeerDirectory`: at most 256 contacts and 256 KiB including local statistics. Each contact can advertise at most 16 exact profile/structural collection keys and bounded endpoints. These declarations describe candidate coverage only. They do not attest to complete indexing, mathematical reliability, or continued availability. Contact entries arise from explicit bootstrap bundles, local contact decisions, bounded public provider advertisements, or a separately paid `GET_ROUTES` reply of at most eight publicly shareable contacts. A reply does not recursively cause its recipients to query those contacts. Admission/replacement stays within the same directory envelope; identities do not create extra slots.

For a four-peer round, take up to three compatible contacts ranked by the NET1 collection-key/local-service scoring rule, then one compatible contact selected by persistent round-robin rotation and not already selected. Exact keys come from the requested formal predicate or locally known statement context; opaque exact IDs without such context fall back to compatible-contact observations and rotation. Locally observed successful matching replies can improve future ordering, while timeout/empty-partial outcomes cannot establish mathematical absence. A false coverage claim can waste only admitted discovery work. Mathematical admission never uses the routing score.

Later admitted rounds select previously untried compatible contacts, preserving the three-directed/one-exploratory pattern where possible. A lookup session pins its finite candidate contact set and tried-ID set at admission; later route suggestions can seed a new separately admitted session, not enlarge the active session indefinitely. The default horizon is at most the retained directory's 256 contacts, and a smaller caller budget usually ends it earlier. Each session's tried set, route replies, and peer statistics are charged to bounded discovery memory. Thus the protocol can progressively reach more than four known providers without recursive flooding or a claim of worldwide completeness.

Merge responses by exact descriptor ID and ProofID/ReplayID pair, retaining conflicting provider records as separate hints. Different replay witnesses must not disappear merely because they share a ProofID. Merge each selected peer's returned list in fixed round-robin order, deduplicating exact pairs; the merged cap is explicit. Overflow is not absence, and clients can request remaining named pages within new budgets. This avoids assigning all visible positions solely to one peer's ranking but does not promise to expose every returned object when the cap is smaller than their union.

This offers redundant paths, not a permissionless eclipse-resistance theorem. An adversary controlling the contact set can suppress all discovery. Four public keys are not four independent failure domains. No completeness or fair-access claim extends to unseen, unselected, disconnected, or unwilling peers.

## Ingress, duplicate floods, and valid but low-demand output

### Fixed receiver-owned admission classes

The default admitted service queue has at most 256 jobs, partitioned into 96 explicit fetch/replay jobs, 64 maintenance/correction jobs, 32 exploration jobs, and 64 index/discovery jobs. These are local operational jobs, not mathematical investigations. Unused slots may be borrowed only through a receiver-authorized bounded transition; they do not become sender entitlements.

Hints occupy at most 4096 entries and 16 MiB, each expiring after ten minutes unless a receiver-funded selection has already replaced it with an admitted operation. When that buffer is full, the baseline drops new hints until expiration or receiver selection frees space; it creates no per-dropped-identity state. The admitted duplicate cache has its own ceilings of 32768 exact identity entries and 8 MiB including data-structure overhead; reaching either stops further allocation until eviction by local insertion order. Proof entries store the complete typed ProofID/ReplayID pair, not a collision-prone truncated identity. The count permits an average 256-byte entry, but both limits remain enforced: an actual larger representation reaches the byte limit sooner. Its exhaustion does not allocate a new cache for each publisher, topic, or identity.

For identical known ProofID/ReplayID-pair or exact descriptor announcements:

1. If the local current record and closure already satisfy the requested native contract, no new proof check is needed merely because another publisher sent it. Any acknowledgment is still bounded and metered.
2. If the cached assessment is stale, a new publisher's signature does not refresh it. Rechecking requires ordinary admitted resources.
3. If the identity is only remembered as a past hint, the cache suppresses repeated candidate insertion; it does not create formal acceptance.

If a newly fetched descriptor's exact identity or native-derived keys disagree with its advertised binding, report a descriptor-binding failure. A different valid mathematical object found in the bytes cannot silently satisfy the requested descriptor. Recognizing that object requires a separate correctly bound admission decision.

### Exploration is bounded attention, not unique-person fairness

One tenth of the reference daily CPU allocation below is reserved for exploration. The receiver maintains at most 16 configured formal collection partitions, plus one aggregate residual partition. A publisher cannot create a partition by inventing a new identity, namespace, statement, or topic.

Within the admitted exploration hint buffer, select partitions in deterministic cyclic order and then their oldest unattempted candidate, breaking receipt-order ties by exact content ID. A candidate that has already consumed its allowed attempt is removed from that buffer; retries require new receiver authority. Empty partitions are skipped. A partition with no inspected candidates gains no credit that can later create an unbounded burst.

The residual partition is visited at least once per full cycle while it has eligible hints, so unfamiliar formal material need not match a preexisting subject filter. Its global size and service limits remain fixed. This is a baseline policy, not a guarantee that every good contribution will be sampled. FIFO arrival, formal-domain partitioning, or hash sampling can all be manipulated by a sufficiently large adversarial stream. The guarantee is bounded work and conditional service for already admitted eligible jobs; it is not fairness among arbitrary public keys or all generated mathematics.

Queue admission, outstanding reservations, and the aggregate resource vector are checked before a job exists. At overload, return a bounded `DECLINED_RESOURCE` response when an authorized response budget exists, otherwise drop the frame under the ingress profile. Do not create a durable rejected-ID record, future-work promise, or task backlog for each discarded item. A node cannot control every byte sent toward its physical network interface; its in-process memory, admitted processing, responses, and durable state are what this protocol bounds.

A correct theorem may be declined for checking or storage. The response must not label it false or mathematically inferior. The sender can keep it on its own resources or offer it to other willing nodes.

## Proof families and bounded alternative retention

### Grouping and measured data

A proof family is indexed by one exact `JudgmentID`. Each member retains its ProofID/ReplayID pair, exact dependency closure, receiver-extracted trust footprint, permitted checker profile, historical assessment, current-use state, and receiver-measured costs. Same-ProofID/different-ReplayID entries are different family members.

The default candidate window contains at most 16 locally checked evidence-candidate descriptors per judgment for automatic selection. A newly checked candidate can occupy one separately reserved temporary seventeenth slot while selection is recomputed; this prevents a full window from permanently excluding later improvements. Keep the selected automatic representatives, then fill remaining window positions from the cost-Pareto candidates ordered by most recent local completed assessment and exact pair, then other candidates in that order. Release the extra temporary slot atomically with the new window. Explicit retained/pinned roots remain in exact indexes outside this automatic window when necessary; their retention obligations do not disappear. A candidate excluded from the window is still a valid formal result if its native check passed, but receives no additional automatic storage entitlement.

Measure native replay costs under a named checker/hardware/options profile with declared cold or warm cache conditions. Unknown cost is not zero. A remote claimed cost is not a measurement. The baseline records CPU time, peak memory, complete encoded closure bytes, and the exact dependency/footprint roots. Subsequent observations can replace a performance estimate through a new immutable local record; they do not replace the native evidence.

For a retained-root set \(S\), actual local storage is based on the union

\[
B_i(S)=\left|\bigcup_{p\in S}\operatorname{Closure}(p)\right|_i
  +B_i^{\mathrm{metadata}}(S),
\]

where shared chunks are counted once physically, while every additional root/reference/assessment record is charged. Marginal storage for adding \(p\) is \(B_i(S\cup\{p\})-B_i(S)\), computed against exact existing local chunks within a bounded transaction. Summing a advertised standalone size per proof is neither a correct union calculation nor deletion authority.

### A limited Pareto comparison

Compare costs only for the same exact judgment and a declared compatible native validation profile. Say that \(p\) cost-dominates \(q\) in snapshot \(S\) when:

- its extracted admitted trust-feature set is a subset of q's;
- its measured replay CPU, peak memory, and full closure bytes are each no larger;
- at least one compared feature is strictly better.

The comparison does not establish independence of proof failures, preservation of byte contracts, or dominance in every future cache state. Differing validation bases or unmeasured axes are incomparable. A dominated proof can still be worth retaining as a different evidence path or because its exact bytes are promised.

### Deterministic automatic selection `P4`

The baseline automatically retains at most four proof roots per judgment, subject to the aggregate byte/record ceiling. It considers the 16-member local window plus at most one newly admitted temporary candidate, and first removes currently unusable proofs from the automatic-usable candidate set; their historical assessments need not be falsified or silently overwritten.

Select without duplicating a winner:

1. A trust-footprint representative: smallest number of admitted unsafe features, then smallest axiom-footprint cardinality, then measured cold replay CPU, then exact ProofID/ReplayID pair. This tie-breaking is a local heuristic among otherwise permitted footprints, not a theorem that all axioms have equal risk. In the no-axiom conformance fixture the first two axes tie; the practical profile can distinguish permitted standard axiom footprints.
2. From the cost-Pareto set, the least measured cold replay CPU, then peak memory, then exact pair.
3. From remaining usable members, the least actual marginal union-storage increase given the roots already selected, then replay CPU, then exact pair. A proof dominated on standalone full-closure costs may win this slot because it shares existing bytes; the standalone Pareto screen does not discard it from consideration here.
4. The oldest locally checked currently usable different witness in the window, preferring a different exact dependency fingerprint from the selected roots; tie by exact pair. It may be cost-dominated. This preserves one incumbent alternative when possible; it does not prove failure-domain independence.

If a slot's set is empty, fill it from remaining usable candidates by replay CPU and exact pair. Unmeasured performance ranks after measured performance; an otherwise permitted proof can remain as the only representative. Apply the current aggregate storage/metadata budget when adding each root; report skipped alternatives and any insufficient-capacity outcome explicitly.

Explicit original-byte contracts, seed roots, and in-flight dependency pins are handled outside `P4` and cannot be evicted to meet its cap. A node must decline new promises if it lacks their resources. Replacing an automatic root requires first obtaining, validating, and pinning the replacement closure; only then may the old unpromised root be released under the normal grace/recovery protocol. If temporary double storage cannot be afforded, retain the old root and defer the replacement.

No selected alternative creates current support automatically. The receiver's exact current evidence tree still determines reliance. An index may advertise four historical proofs and have no currently acceptable one after a local checker incident.

## Retention and index maintenance policy

For automatic collection, ORG1 uses these local selection categories. The peer-service layer's exact grant/lease records implement their finite authority; a category name does not create a second unaccounted retention mechanism.

| Category | Default selection behavior | Expiry and authority |
|---|---|---|
| Seed or explicit retained root | Locally chosen native basis or explicitly funded exact content | Its actual retention contract governs; no automatic eviction while a live obligation exists |
| Probation | A bounded sample of newly checked eligible content, with no usefulness prerequisite | At most one day from admitted activation; renewal needs another local decision |
| Reusable cache | Selected exact content whose measured local retrieval/reuse or policy merits a larger allocation | At most seven days; at most one automatic renewal decision per term |
| Optional archive | Exact content chosen for longer preservation | Only an explicit funded archive contract; no default perpetual promise |

Probation and reusable-cache terms map to NET1 warm checked caches. Their original monotonic expiry is bound to the receiver's `retentionClockGeneration`, which survives a clean same-process service-capability rollover but not a real reboot, writer takeover, or uncertain clock origin. Clean control-record compaction cannot extend a warm deadline or require every still-funded warm root to be discarded. The one- and seven-day terms are ORG1's explicit local term settings; the numerical nominal stocks below assume an uninterrupted retention-clock generation and no early authorized eviction. Seed, cross-reboot retention, and optional archives use explicit NET1 pinned roots with receiver-authorized release; their actual contracts govern whether and when release is permitted. These are alternative term settings in one retention mechanism, not additional storage authority. Recovery never converts uncertain or outstanding pinned allocations into free space without the normal root/reference accounting.

A witnessed import, query count, or new dependency edge may nominate a probationary root for a seven-day cache term. It does not directly renew that root. At each term boundary the receiver selects within its current aggregate byte/object ceilings, including repair and metadata reservations. Replaying a request or creating many principals cannot bypass this decision. Request counts are susceptible to gaming; they remain policy inputs, not mathematical importance or unique-demand measurements.

The baseline performs index compaction when obsolete index segments reach 25 percent of index allocation, subject to an admitted compaction job and reserved temporary space. If compaction space is unavailable, stop fresh index promotions before overrunning the cap. Existing exact lookup remains available within its admitted service envelope; no background compaction is allowed to use an unbounded hidden reserve.

Assessment and operation histories have finite retention. A later compacted interval can preserve bounded aggregate counters and authenticated terminal summaries without preserving every historical event. A summary must never claim that an omitted proof or original assessment remains independently replayable. Deleting optional history does not revive old service tickets or permit replayed execution.

## Compression and representation improvement

### Baseline choice

ORG1 initially enables only exact-byte chunk deduplication and separately measured lossless byte compression with exact reconstruction. It does not run an autonomous semantic equivalence quotient. Formal definitions, relations, or shorter proofs supplied by clients are ordinary candidate mathematical objects subject to native checking.

The expression-DAG/native module profile already shares exact subexpressions and immutable declarations where their identities permit. A proposed codec is not permitted to reinterpret a ContentID: requesting that ID must reconstruct its exact original canonical bytes. Decoder software, version, memory, worst-case expansion bounds, and its own retained dependencies are part of the codec's service profile.

### Proof-preserving transformations

For an exact finite exported-judgment set \(\mathcal J\), define a proposed replacement by old/new root sets \(K,K'\), an exact reconstructing procedure or explicit new proofs, and per-judgment resource envelopes \(b_j\). The receiver must verify

\[
\forall j\in\mathcal J,\quad
\operatorname{RecoverCheck}(K',j;b_j)=\texttt{ACCEPT},
\]

where that operation binds the actual reconstructed proof, exact context, allowed foundation, chosen native checker, dependency closure, and measured or certified reconstruction bounds. The complete finite coverage enumeration must be checked; sampling some judgments does not certify all of \(\mathcal J\). These are previously established exported judgments, not an unsolved-problem list.

The initial admissible transformation is especially concrete: the producer supplies each replacement native proof explicitly, the receiver replays each one, and exact-byte manifests enumerate all retained outputs. A general decoder or proof generator is a later profile with separately justified termination/resource behavior; calling it a compressor is not a proof of either.

Even successful proof preservation creates new proof identities. It does not satisfy an outstanding obligation to retain old proof bytes, old modules, or an alternative axiom footprint. Check old retention promises, current live references, native context compatibility, and external export commitments before any release. The safe paper transition is replacement admission, new-root pin, validation of the complete coverage relation, permitted old-root release, then ordinary garbage collection after the grace interval.

Charge discovery/selection of the transformation, construction of new definitions and proofs, validation, index rebuilding, duplicate temporary storage, decoder/bridge maintenance, later reconstruction/checking, repair, and any retained old promises. A smaller proof display or a lower isolated byte count does not establish net improvement.

Two proved closed propositions \(P,Q\) can always be related by constant witnesses for \(P\leftrightarrow Q\). Such a relation is legitimate mathematics, but it is not a lossless common representation of their interfaces or evidence. It cannot make their statement IDs equal, erase their hypotheses, or authorize deleting either endpoint.

## Reference resource envelope and a numerical workload

### Declared example, not benchmark evidence

`ORG-SAMPLE` is a small-node accounting example composed with two native-checker slots and at most four paid network executors. It is an alternative combined local resource policy, replacing rather than adding to `NET1-DEFAULT`'s disk ceilings and service-pool proportions; NET1 hard wire limits still apply. It raises the local HINT rate ceiling from 16 to 24 per second, within NET1's aggregate control ceiling, while imposing the tighter daily metadata-byte cap below. A deployment must measure its actual checker/hardware costs before claiming the throughputs below. CPU-seconds, byte amounts, memory, wall-time, and record counts are separate dimensions; unused storage is not permission to exceed a CPU reservation.

It also explicitly raises the local retained-root ceiling from NET1-DEFAULT's 16384 to 131072, below NET1's hard 262144 limit. Its metadata allocations admit at most 262144 index descriptors, 524288 bounded native assessment records, and 4194304 exact dependency/reverse-edge records, each also subject to the byte allocations below. These are paper-example local caps, not extra control-ticket allowances. The seed uses at most 4096 retained roots, each within the native/NET per-closure limits; 100000 later proof roots plus a conservative nominal bound of 4800 probation/cache roots therefore fit the 131072-root cap. The example assumes their exact dependency metadata fits the separate edge and byte caps. If it does not, admission fails before the numerical workload is declared feasible. Operational offers, replay keys, and control records retain their NET1 caps and require safe epoch retirement/compaction for sustained operation. Actual reboot/writer/time-origin changes still expire warm roots and must enter empirical reuse-cost estimates; clean service rollover preserves their original funded deadlines.

The example's daily CPU envelope is 86400 CPU-seconds, partitioned as follows:

| Service class | CPU-seconds/day | Share |
|---|---:|---:|
| Explicit fetch/replay and selected ordinary checking | 51840 | 60% |
| Maintenance, defect rechecking, integrity work, repair accounting | 21600 | 25% |
| Exploratory new-content checking | 8640 | 10% |
| Index extraction, discovery, bounded hint processing, metadata work | 4320 | 5% |

An admitted native-check execution reserves its declared bound, default 60 CPU-seconds and 300 wall-seconds under the peer profile. Authoritative finalization releases only demonstrably unused allocation. The mean-cost example below is not a guarantee that every request costs two seconds: at 60 seconds each, the ordinary-plus-exploration CPU quotas admit only 1008 checks/day. Bounded reservation is what protects the node when easy-looking inputs are expensive.

Scheduling uses a fixed weighted cycle over these service classes and their finite eligible queues, with bounded executions. Service floors apply only to jobs already admitted under the declared envelope. Idle class allocation may be reassigned only through an explicit receiver policy transaction; the baseline does not rely on this reassignment to meet the example. Byte and memory constraints can still prevent an otherwise CPU-affordable job.

The illustrative disk allocation is 256 GiB:

| Allocation | GiB | Includes |
|---|---:|---|
| Exact corpus storage | 192 | Seed, current root unions, probation, cache, and explicit archives |
| Indexes | 12 | Descriptors, posting lists, exact tables |
| Assessment/dependency records | 8 | Native assessment and reverse-edge metadata, bounded histories; 128 MiB within this allocation is reserved for operational ticket/control records under their separate NET1 cap, not an additional allocation or an eight-GiB control allowance |
| Fetch/replay staging | 16 | Uncommitted chunks and at most admitted in-flight closures |
| Compaction/replacement workspace | 16 | Temporary double representation and index rewrites |
| Recovery reserve | 12 | Recovery and controlled emergency bookkeeping |

Actual root-union accounting avoids double-counting shared corpus chunks. Index/control/transaction entries remain separate costs. No automatic admission spends the recovery reserve merely because another category is full.

The daily network envelope is 16 GiB in aggregate received and sent application bytes: six for closure acquisition, six for serving, three for repair/export, and one for hint/query/control traffic. Frames and descriptors are charged by actual encoded bytes. With 4096-byte hints, a one-GiB metadata envelope permits far fewer hints than the small-average-hint example below. Source advertisements cannot choose which byte class to charge.

### One feasible mean-cost day

Assume a local 16-GiB pinned seed and 100000 retained proof packages averaging 256 KiB of additional unique bytes each. Assume the following measured means and bounded traffic, solely for this numerical trace:

- 1728000 incoming hints/day, averaging 512 encoded bytes: 0.824 GiB;
- 12000 ordinary and 3000 exploratory proof checks, averaging two CPU-seconds each and 256 KiB of newly fetched closure;
- 80 percent native acceptance; that is 12000 verified results, not 12000 mandatory storage commitments;
- 2000 admitted index queries, costing at most 0.25 CPU-seconds each; mean returned pages of 64 descriptors averaging 512 bytes;
- 10000 served 256-KiB packages;
- 2000 probationary results selected for at most one day and 400 selected cache results for at most seven days within one uninterrupted retention-clock generation, with 8 KiB of descriptor/index/control overhead per retained root in this trace;
- 1000 maintenance replays/day at two CPU-seconds each, a budgeted two-GiB integrity scan, and at most one GiB of repair/export traffic.

The arithmetic is:

| Quantity | Accounted use | Envelope comparison |
|---|---:|---|
| Ordinary checking | 24000 CPU-seconds | Below 51840 |
| Exploratory checking | 6000 CPU-seconds | Below 8640 |
| Maintenance replay | 2000 CPU-seconds, plus separately metered scan/repair/control work | Below 21600 only if those additional charges fit |
| Index queries | At most 500 CPU-seconds | Leaves 3820 for extraction, hints, and metadata |
| Fresh closure acquisition | 3.662 GiB | Below six GiB |
| Serving | 2.441 GiB | Below six GiB |
| Hint bytes | 0.824 GiB | Leaves about 0.176 GiB of the metadata byte allocation |
| Query answer bytes at stated mean | About 0.061 GiB before envelopes | Must share that remaining metadata allocation |
| Original additional corpus bytes | 24.414 GiB | Plus the 16-GiB seed and actual metadata |
| One-day probation nominal stock ceiling | 0.488 GiB | Before deduplication and metadata; no earlier retention-clock reset assumed |
| Seven-day cache nominal stock ceiling | 0.684 GiB | No automatic unbounded renewal; no earlier retention-clock reset assumed |
| New retained-root metadata | 18.75 MiB/day | Terms/history policies bound its retained stock |

For the example to be feasible, the measured aggregate hint/extraction/control CPU must be at most the remaining 3820 CPU-seconds, and all envelopes and other metadata bytes must fit their reserves. Those are explicit conditions to measure; no unmeasured parsing speed is assumed. Mean package bytes likewise are not the transfer limit: default per-operation closure bounds and staging reservations still apply.

The node checks fewer than one percent of incoming hints in this trace. Most receive no expensive service. It recognizes 12000 correct results in completed checking assessments but retains only a selected subset under stated terms. It must report those different numbers rather than describe every accepted check as a permanent addition to the network.

### Exponentially increasing candidate load

Suppose distinct potentially retainable candidates arrive at

\[
\lambda_d=1000\,2^{d/7}\quad\text{per day},
\]

with a constant two-second mean check cost and 256 KiB mean new unique payload. Ordinary and exploration CPU together supply at most

\[
\mu_{\mathrm{check}}=(51840+8640)/2=30240
\]

checks/day at that mean. Offered candidate load exceeds this optimistic mean envelope at about day 34.43. The actual safe admitted count can be lower because of expensive tails, index/transfer limits, missing closures, and maintenance incidents. The finite queues reject/defer excess work; they do not preserve an exponentially growing backlog.

If every candidate were nevertheless retained forever, ignoring checking, retained-root-count, and metadata bottlenecks, additional bytes after \(T\) complete days would be

\[
S(T)=\frac{1000}{4096}
\frac{2^{T/7}-1}{2^{1/7}-1}\quad\text{GiB}.
\]

With 150 GiB spare corpus space, the geometric interpolation reaches the limit at \(T\approx42.15\); the first integer full-day stock exceeding it is \(T=43\). This is before adding metadata, replication, or repairs. The two calculations expose different limits; they are not a prediction of actual admission under the bounded policy, whose root-count or other constraints can bind earlier.

Increasing arrivals require some combination of more supplied capacity, less costly representation/checking, limited selection, and expiry. At fixed byte-growth allowance \(g\), average new payload \(b\), and offered rate \(\lambda\), a retained fraction must satisfy \(p\lambda b\le g\) over the stated interval. Over an indefinitely fixed storage stock, even a constant positive growth allowance cannot continue forever without release or additional capacity.

For a stationary admitted workload, every bottleneck needs a sustainable service condition such as \(\lambda_a\mathbb E[c_r]<\mu_r\) for resource \(r\), plus an explicit burst envelope and finite-job assumptions. Mean inequalities alone are not a worst-case latency guarantee. Receiver reservations enforce safety even when the service conditions fail.

### A correlated checker incident

If a local incident affects 100000 proof assessments, the node first blocks affected current reliance through the admitted incident and epoch mechanism. It does not enqueue 100000 separately funded repair jobs at once. It retains a bounded incident scope and progress cursor, admitting rechecks as resources permit.

At the unrealistic best case of all 21600 maintenance CPU-seconds going to two-second rechecks, full replay still takes at least 9.26 days. Ordinary maintenance, bandwidth, and hard cases lengthen that time. Immediate local safety is compatible with slow recovery; the response is `UNKNOWN` or the appropriate nonreliance state while no clean current path exists. A reassuring global “all fixed” flag is not available.

## Accumulation records and evidence for policy changes

### Counters with honest denominators

Within a named local interval and policy/snapshot scope, retain aggregate counters for:

- encoded hints observed within the metered boundary, duplicate hints, dropped hints, and selected candidates;
- native accepted, rejected, unsupported, error, and resource-nondecision assessments;
- newly encountered exact JudgmentIDs, ProofIDs, and ProofID/ReplayID pairs, with the bounded historical comparison window named;
- roots currently retained, exact union bytes, metadata bytes, and expired/removed roots;
- currently reusable proof paths, blocked paths, unavailable closures, and pending bounded maintenance work;
- local/remote query latency, completed and partial scans, pages, examined postings, and returned candidate IDs;
- receiver-checked downstream dependency occurrences of an imported result;
- all charged CPU, wall-time, bandwidth, temporary/durable storage, repair, and index/control costs.

Counters use saturating or epoch-rotated checked arithmetic; saturation is explicit, never silent wraparound. Aggregate history can be retained longer than detailed records under a bounded policy. “Newly encountered” means new within the recorded local history/window, not first published in the world. “Another endpoint” does not mean another independent researcher. A downstream dependency occurrence does not prove necessity or a causal speedup.

The mathematical corpus contains the actual formal artifacts and native relations. Operational counters are service/diagnostic records; human intentions, research prompts, or task-completion labels are not collected to produce them.

### Fixed-resource comparison profiles

Freeze the same finite native corpus/snapshot sequence, checker, receiver resources, contact/failure trace, and exact stored-object query sample. Compare:

| Profile | Difference being investigated |
|---|---|
| `O0` | Exact ID and JudgmentID lookup only; no structural index |
| `O1` | `STRUCT1` raw structural indexes and the fixed five query modes |
| `O2` | `O1` plus explicitly budgeted `BETA128` candidate keys |
| `O3` | `O1` plus one learned formal-syntax ranker; candidate count and native verification unchanged |
| `P1` | One automatic proof representative, with the same explicit pins |
| `P4` | The four-root policy above, charged for all additional validation, bytes, indexes, and maintenance |
| `C0/C1` | Exact-byte-only storage versus one specified checked replacement transform over the same exported scope |

The finite query sample is generated from already existing stored content; it is a service-evaluation input, not a registry of unsolved mathematics. Structural candidate recall is measured against a completely enumerated finite declared key relation or labeled admissible application pool. It must not be relabeled as completeness over mathematical relevance generally.

The initial replacement gates are concrete but provisional:

1. Zero observed native-acceptance bypasses, identity substitutions, unsupported absence claims, or resource-envelope violations in the prescribed paper/adversarial fixtures. An implementation must later exercise corresponding conformance checks; zero observations do not prove zero risk.
2. Exact lookup and promised coverage preservation remain unchanged under the same scope. Any lost endpoint or original-byte obligation disqualifies a claim of lossless replacement.
3. On frozen completed replicas of the finite service trace, a proposed structural/ranking change must reduce the median measured total lookup-plus-fetch-plus-native-validation CPU per successfully retrieved eligible object by at least 10 percent, with no more than a two-percentage-point loss in scoped Recall@64, no increase above 10 percent in p99 response latency, and no resource-axis increase above its separately approved cap. Construction, training if any, rollout, and repair costs are amortized over a declared 30-day horizon.
4. A proof/representation policy must report the full resource vector and preserved scopes. Its operator may adopt a declared tradeoff, but it must not call a byte win a componentwise win when checking, reconstruction, availability, or maintenance worsens.

These thresholds are a practical proposed replacement gate, not proof obligations for heuristic optimality or prerequisites to operating the baseline. Before making a confirmatory performance claim, fix replication units, distributions, interval estimates, multiplicity handling, and acceptance margins alongside them. Exploratory engineering can change a heuristic using clearly labeled evidence; a changed margin must not be presented as though an earlier run satisfied the old decision rule.

No such performance gate decides whether an individual correct artifact is mathematics. It chooses an implementation/policy for organizing material within a finite receiver budget.

## Runnable-on-paper fixtures

The fixtures use exact opaque IDs and small native relations. The expected effects are semantic outcomes, not claims that software has executed them.

| Fixture | Input and initial state | Required result |
|---|---|---|
| Exact replay storm | A currently checked available pair `(ProofID A, ReplayID R)`; 1000 identical hints | At most one hint entry; no new native check solely for repeated announcements; metered bounded ingress/egress; no new storage entitlement |
| Same term, changed witness | ProofID A unchanged, but ReplayID R' selects different auxiliary proof witnesses | Distinct validation/cost candidate; no reuse of R's footprint, closure, or assessment merely from ProofID equality |
| Stale duplicate | Same A, but its selected checker is blocked at the current epoch | Duplicate identity cannot refresh it; current reliance remains nonaccepting until an admitted clean check/path exists |
| Misbound descriptor | Hint names JudgmentID X and ProofID P; fetched P natively establishes Y | Reject the X/P descriptor binding; do not report X established. A separate valid Y contribution requires correctly bound admission |
| Truncated symbols | Relevant constant occurs after the 4096-occurrence extraction limit | Descriptor says `SYMBOLS_TRUNCATED`; symbols search may miss it; exact JudgmentID lookup still works if indexed; no nonexistence conclusion |
| Empty partial page | Shortest posting list has 20000 entries; first matching result is entry 19000 | First 8192-entry page can be empty `PARTIAL_SCAN_BUDGET`; second can also be empty; third may return the match and finish. No cursor skips unexamined entries |
| Stale continuation | Cursor for snapshot S crosses expiry/reboot or is presented for predicate Q' | `STALE_CURSOR`; never continue silently in snapshot S' or under Q' |
| Remote omission | Remote peer says `END_OF_LOCAL_MATCH_SCAN` while withholding a known candidate | Coverage remains server-declared; no world-wide or cryptographically established absence. Another selected peer may still supply the object |
| Valid-junk flood | One million different valid tautology candidates offered inside one hour | Hint/job/byte/CPU caps hold; excess receives bounded decline/drop, not a permanent backlog; unserved candidates are not labeled false |
| Proved equivalence | Closed proofs p:P and q:Q plus constant witnesses for P iff Q | Add a checked relation if admitted; preserve distinct endpoint IDs, interfaces, and byte promises |
| Smaller display, larger closure | New proof display is 2 MiB, but introduces a 9-MiB decoder/dependency closure replacing 10 MiB old data | At least 11 MiB before metadata, validation, and old promises; no claimed byte saving based on display alone |
| Old-byte promise | A new proof of the same judgment checks, while old ProofID has an active exact-byte retention term | Both can be retained if funded; new proof does not discharge old byte promise; no deletion solely because the judgment still has support |
| Contradictory hypotheses | Native proof of 0=1 under explicit P and not-P | Record only the exact conditional judgment if policy permits; never strip hypotheses or call it unqualified arithmetic truth |
| Checker incident | An admitted defect affects all automatic proofs for a judgment | Historical check records remain historical; current reliance fails closed; alternative unaffected proof may restore use only after current checking |
| Metadata exhaustion | Proof bytes fit, but required dependency/assessment/index references exceed admitted record limits | Decline/defer durable promotion; no uncharged metadata and no falsely complete local exact index |
| Private retained theorem | A locally checked retained ReplayID is outside PUBLIC_SERVE and any caller-authorized export | Remote FIND omits it without a private-corpus count; knowing its exact ID gives no generic CAS read; local validation is not publication authority |

### Worked proof-family fixture

Assume five currently eligible ProofID/ReplayID candidates of one exact judgment, all measured under the no-axiom conformance subprofile. All have zero unsafe flags, empty axiom footprints, and measured peak memory equal. Their simplified costs are:

| Proof | Axiom footprint | Full closure bytes | Replay CPU | Other fixture state |
|---|---|---:|---:|---|
| A | empty | 8 KiB | 100 ms | Oldest different proof/dependency witness |
| B | empty | 12 KiB | 150 ms | Ten KiB already shared with pinned roots |
| C | empty | 6 KiB | 80 ms | No bytes shared in this fixture |
| D | empty | 40 KiB | 40 ms | Fastest replay |
| E | empty | 100 KiB | 400 ms | Another independently encoded witness |

C cost-dominates A, B, and E on full-closure/replay axes; C and D are incomparable. `P4` selects D for slot one because the trust axes tie and D replays fastest, then C for slot two. Slot three considers all remaining usable candidates and selects B because its marginal extra storage is two KiB, compared with A's eight and E's 100 KiB in this fixture. Slot four selects A as the oldest different remaining witness. E remains valid mathematics but is not selected. This deliberately shows why the marginal-storage slot cannot be restricted to a Pareto screen based on standalone full-closure bytes. The bounded greedy policy still makes no global optimality claim.

If A has an explicit live retention promise, it remains retained regardless of automatic selection. If D becomes locally blocked, it cannot continue as the current representative; selection recomputes from currently eligible paths. If the apparent ten-KiB sharing for B cannot be established from exact chunk/reference state, the node may not use the two-KiB marginal estimate. The conformance subprofile rejects a witness introducing an axiom. Practical `Lean-Native/v1` can accept a witness using its pinned standard axioms, subject to the receiver's explicit footprint policy; such a witness keeps its nonempty footprint and competes under P4 only with other currently permitted candidates. A new arbitrary choice-like axiom remains unsupported in both profiles.

## Remaining paper decisions before implementation

The choices above make organization operations determinate enough to walk through without code. The following refinements remain explicit work, not hidden successful assumptions:

- exact canonical field ordering and enum values for every record and query response, reconciled with the native and peer profiles;
- worst-case parser/extractor costs and native expression/edge admission bounds;
- a crash trace for index publication, cursor pin release, retained-root replacement, and compaction;
- a proof that page cursors never omit an unexamined entry in an honest pinned scan;
- measured calibration of the 16-member/4-root proof policy and the reference resource envelope;
- optional alternate exploration policies with explicit measured miss rates, without asserting Sybil fairness;
- the finite preservation checker and resource-accounted transition for the first proof-replacing transform;
- conformance and empirical decision procedures that remain outside the mathematical validity predicate.

The central invariant is unchanged: organization can affect which exact results are found, served, and retained; it cannot manufacture formal evidence, silently change a judgment, or make human intention part of mathematical recognition.

## Local references

- [Formal knowledge contract](FORMAL-KNOWLEDGE-CONTRACT-v0.md).
- [Layered problem decomposition](../notes/analyses/CP-001C-layered-problem-decomposition.md).
- [Frozen Cooperation Core](COOPERATION-CORE-v0.md), for grant/reservation/atomic-finalization and current-reliance semantics; research-task features are not v1 requirements.
- [Distributed memory checkpoint](../notes/checkpoints/CP-001B-distributed-corpus-and-global-status.md), for exact memory, receiver admission, scoped observation, and bounded retention.

No new literature survey, performance benchmark, implementation, or mechanized proof is claimed.
