# CP-001D: autonomous long-term accumulation without a central service

Date: 2026-09-19  
Status: Operational concept and design limits; no daemon, automation, or implementation has been created

The intended product is a downloadable decentralized framework through which local investigators can indefinitely contribute to and reuse an evolving body of formal mathematics. “Indefinitely” is an architectural objective: no required central lifetime, finite research campaign, compulsory global goal, or fixed list of questions ends the system. It is not an unconditional guarantee that physical storage, electricity, operators, or cryptography survive forever.

This note complements the [integrated specification](../../spec/OPERATIONAL-CORPUS-V1.md). It concerns sustained operation, not political attribution.

## What constitutes the body of knowledge

At time \(t\), distinguish:

- \(K_{\mathrm{derived}}\): artifacts actually constructed with admissible evidence, including ones whose bytes may later be lost;
- \(K_i(t)\): exact roots currently available and admissible at node \(i\);
- \(K_{\mathrm{recoverable}}(t)\): roots whose complete exact evidence and compatible checking materials can be obtained from the actual surviving willing providers under stated resource conditions;
- \(V_i(t)\): the node's bounded view of candidate locations, selected collections, and status observations.

A theorem's formal derivability does not cease when a disk fails. The system's recoverable stock can nevertheless decrease. Conversely, an index entry or learned model memory can increase \(V_i\) without increasing the exact recoverable stock.

The software represents mathematics as an interoperable open object space and independently checked local views. It cannot package every future theorem into its installer or keep every participant synchronously informed of an unbounded global state. A full replica of a specified finite collection is meaningful; “full replica of everything that exists anywhere now” is not a locally decidable role under arbitrary partitions.

This distinction must appear in product language, not only in security footnotes. A node must report the collection, observation time/epoch, available closure, and retention terms it actually knows.

## Locally autonomous cycles

The base service can run without a central coordinator once its operator has chosen local policies. Its maintenance cycle has five separately funded lanes:

| Lane | Inputs | Allowed local effect | Prohibited shortcut |
|---|---|---|---|
| Ingest | Local contributions and bounded selected hints | Fetch, check, and optionally retain exact closures | Automatically accept another node's verification flag |
| Serve/discover | Existing public collection, bounded peer directory | Answer paid queries; rotate contacts; publish selected hints | Unlimited recursive search or global completeness claim |
| Preserve | Local pins, integrity observations, optional replica targets | Scan, repair, request independent replicas | Treat another key's signed promise as durable storage |
| Recover | Locally admitted incidents and crash records | Fail closed, recheck, finalize, restore current usability | Continue relying on stale success during background repair |
| Improve | Local access/reuse/cost telemetry and candidate policies | Rebalance bounded cache/index/exploration allocations | Let popularity decide mathematical validity |

These are service lanes, not in-system mathematical objectives. A local researcher or agent decides what to investigate and submits the resulting artifacts when it wishes. The corpus does not need to know why.

The selected NET1 and ORG1 envelopes give the baseline bounded queues, rotating discovery, snapshot/offer deadlines, retention transitions, and protected maintenance shares. Concrete periodic schedules are local policy choices within those allowances. They cannot create authority just because a timer fired.

## Maintenance that does not accumulate an infinite to-do list

A retention/integrity cycle traverses the currently retained root/chunk inventory with a bounded cursor. It does not allocate one perpetual job for every object ever advertised. Each pass has a declared scope, budget, and completion observation. A growing collection may take multiple intervals to scan; report that age rather than imply continuous whole-corpus verification.

A repair cycle keeps a bounded set of root priorities and progress cursors. A provider's disappearance is an availability observation, not evidence that its mathematics was false. A complete local replica remains usable; a partial local closure is explicitly unavailable until repaired.

Discovery periodically revisits a bounded contact directory, with some rotation outside previously successful sources. Collection-key claims are hints; actual query results and delivery history guide local routing. New route suggestions can seed later funded sessions, not extend an active lookup forever.

Counters and detailed histories have bounded retention. Exact currently needed objects, witnesses, obligations, and recovery state must remain; optional historical events can be summarized and discarded. This is a local operational ledger, not a requirement to store a global history of every theorem.

## Resource renewal without remote resource creation

A system that runs indefinitely must replenish budgets through an explicit local policy. Finite grants alone describe only one finite interval.

The local owner can configure finite CPU/network allowances per monotonic operating interval, admission rates, live storage limits, and a storage replacement policy. A scheduler may automatically issue the next local interval's grants only under that preauthorized policy. A peer's requests, keys, proof count, claimed importance, or model-generated instructions cannot raise these ceilings.

Renewing a cumulative CPU/network allowance is justified by the next interval's supplied capacity. It does not erase existing disk occupancy, live pins, outstanding reservations, or prior promises. Disk capacity renews only through an authorized release or actual added storage. Likewise, a startup or service-epoch rollover does not create a fresh burst independently of the persisted budget policy.

If timing or accounting state is uncertain after a crash, conservatively withhold replenishment until a safe local condition holds. A permanently offline machine can operate within supplied local resources but cannot receive current external incident knowledge.

Monotonic epoch/counter limits have explicit exhaustion behavior: never wrap. Stop issuing the affected authority and require an explicit migration/new identity or a separately versioned larger representation. Indefinite architecture means renewable and migratable operation, not pretending finite machine integers are infinite.

## Preservation under realistic failure models

One full local closure makes a theorem independent of its original publisher. Several independently checked full replicas can improve resilience. They do not prove permanent survival.

If three copies fail independently with probability \(q\) during a stated interval, simultaneous loss has probability \(q^3\). This calculation is invalid when copies share an operator, disk array, cloud account, region, checker defect, or a coordinated attacker. Distinct node keys establish none of these independence premises. The baseline records distinct endpoints and observations without advertising a fictional independence guarantee.

Effective long-term preservation combines actual checking/fetch observations, independently supplied storage, offline exports where desired, and repair before all copies disappear. An unfunded request cannot compel strangers to maintain a copy. When every recoverable copy is lost, an old hash cannot reconstruct it.

For exact-byte archives, preserving a logically equivalent theorem is not the same as preserving the original evidence. For judgment-preserving migration, a complete checked finite coverage map may establish a different preservation claim. Keep these promises separate.

## Profile and checker evolution

Lean 4 is the selected foundation for the first operational profile. Kernel release, fixed bootstrap, encoded syntax, and allowed foundation assumptions are immutable profile commitments.

Evolution has separate cases:

1. **New checker build for unchanged profile.** Locally qualify its behavior, supply chain, and conformance; produce new assessment keys. A shared profile label does not prove two executables behave identically.
2. **New Lean/profile semantics.** Create a new profile ID and independently qualified checking route. Re-elaborate/export or translate selected material and recheck it. Old and new objects coexist; nothing is relabeled in place.
3. **New foundation or hybrid checker.** Specify exact admissible judgments, interpretations, and bridge evidence. A theorem in one theory is not imported into another merely because their pretty-printed formulas resemble each other.
4. **Hash or encoding migration.** Preserve exact old bytes plus newly calculated identifiers and explicit mapping records under a qualified migration. After an actual collision, an ambiguous old ID alone cannot identify which payload was meant.

No mandatory global upgrade vote or central signing key decides mathematical truth. Local adoption necessarily risks fragmentation: disconnected communities can retain different valid profiles and indexes. Exact declared interoperability is preferable to silently interpreting one profile as another.

The software distribution and security-update ecosystem still needs practical governance and supply-chain verification. Removing a central theorem server does not remove all software trust. Local policies may authorize update checking and staged qualification, but proof traffic never installs a checker binary. When an update lacks local adoption authority, the node remains on its old profile or suspends affected service; it does not override the owner because an automated agent said the upgrade was urgent.

## Client interoperability and agent autonomy

An external Lean client obtains exact native replay packages and uses a local adapter to reconstruct checked declarations with deterministic names. Local notation, aliases, structure-registration and instance-search metadata, tactics, search models, and user interfaces are optional client conveniences. Those registrations and search hints are not mathematical identity or corpus acceptance. Actual structure/inductive declarations and instance values are exact checked mathematical content; they are not excluded merely because an elaborator can use them.

A client can preserve those conveniences in its own versioned environment and export the actual elaborated result back into inert native objects. If it uses a different foundation, unavailable proof bodies, or unsupported primitives, export must explain the boundary rather than assume compatibility.

A trained model is an optional generator or retrieval aid. It can learn useful patterns from admitted mathematics, but parameters do not replace exact proof storage and checking. An autonomous agent can be wrong, forget facts, or fabricate references without causing corpus acceptance, provided the receiver boundary holds.

The reciprocal loop is therefore:

1. a client acquires and independently checks exact previous results;
2. it investigates privately using any tools it chooses;
3. it offers resulting artifacts, with no task-completion certificate;
4. willing nodes check, organize, preserve, and serve selected results;
5. other independent clients repeat the loop.

This loop can remain active without shared root goals or synchronous coordination. Its usefulness depends on actual access, representations, search cost, and supplied resources.

## Where blockchain, SNARKs, and distributed indexing belong

A global blockchain is not needed to decide whether an immutable Lean derivation checks. Independent checking and exact content addressing already permit concurrent contributions and idempotent replication without a universal theorem order.

A ledger can become useful for scarce shared commitments: paid storage contracts, transferable resource credits, or ordering operations of one replicated service authority. Those are additional systems with consensus, economic, and availability assumptions. They should not become prerequisites for contributing valid mathematics to the base commons.

Merkle-style content commitments help address and compare exact finite inventories. They do not prove that an index is complete, that bytes are still stored, or that a queried theorem does not exist elsewhere. DHTs or larger directory overlays can improve routing in later profiles, with eclipse/churn/spam/resource costs. NET1 uses bounded direct directories and independently selected rounds so it can operate before adopting a global overlay.

A succinct proof of a specified native checking computation could reduce repeated expensive verification. To be meaningful, it must bind the exact checker/profile, formal statement, assumptions, selected dependency witnesses, and computation/output relation. If footprint extraction occurs outside the proven computation, a succinct proof of kernel acceptance alone does not authenticate that footprint.

SNARKs add proof-system, implementation, circuit/VM, and possibly setup assumptions. They do not prove long-term availability or mathematical usefulness, and an opaque certificate without reusable native content would undermine the central contribution/reuse loop. They remain an optional later checking acceleration with explicitly available native fallback, not an unexplained foundation of v1.

## What a practically operable concept can responsibly claim

The concept can select one complete contribution/reuse path, explicit state transitions and failure outcomes, bounded authority, ordinary/adversarial cases, and qualification criteria. It cannot honestly certify production performance, the absence of every unknown flaw, or eternal survival before implementation and deployment.

The outstanding qualification is substantive: the native codec/exporter, reserved-name bootstrap, realistic library closures, storage/recovery implementation, large-network retrieval workload, and cost calibration must be demonstrated when implementation is authorized. Keeping these gates visible is not permission to substitute a toy demonstration or a successful-status assertion for them.
