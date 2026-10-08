# CP-001C analysis: an open mathematical commons without a required central server

Status: concept proposal for the next checkpoint; no implementation or deployment claim.

Date: 2026-09-19.

Scope: decentralization, open participation, bootstrap, availability, exit, upgrades, and the conditions under which independent mathematical agents can exchange reliable work. This analysis supplements CP-001A and CP-001B. It does not edit their frozen specifications or import the five-cell experiment's membership assumptions into the ultimate public system.

## Intended object

The downloadable software should let a participant independently operate a mathematical workspace and participate in a larger, extensible commons. Its core operations are local construction, exact evidence checking, discovery, import, reuse, publication, retention, and export. No network-wide research goal, accepted publisher list, elected theorem authority, compulsory token, or central account is needed for those operations.

The phrase "the whole body of mathematics" is an aspiration to broad coverage and interoperability. At any actual time, the system contains only the objects that participants have generated, imported, and retained. It cannot promise all true propositions, all private discoveries, all future mathematics, complete semantic equivalence search, or simultaneous possession of every object by every node. It can represent a virtual union of exact objects and disclose the coverage of particular collections.

Let \(O_i(t)\) be the exact immutable objects held by participant \(i\). For analysis, define

\[
\mathcal O(t)=\bigcup_{i\in\mathcal N(t)}O_i(t).
\]

Here \(\mathcal N(t)\) is an observer's mathematical model of participating nodes. It is not a registry that nodes must enumerate or agree on. An object can belong to this union while being unreachable by a particular receiver. Distinguish possession, public advertisement, discoverability, current retrieval, and policy-relative usable evidence.

The software is therefore a portable interface to independently operated exact collections and checked evidence graphs. The commons is the interoperable activity of these nodes, rather than one mandatory database image or one universally accepted materialized view.

## What must be decentralized

Decentralization is a set of properties of operations and dependencies, not a property established by the word "peer-to-peer."

| Property | Required meaning | Explicit limitation |
|---|---|---|
| Local autonomy | A participant can create questions, run available tools, check evidence, and use its retained closure while disconnected. | Online-only tools or missing remote dependencies are unavailable during disconnection. |
| Permissionless operation | Running a compatible node and choosing a local identity require no global enrollment authority. | A particular provider may decline to serve or store data. |
| Open contribution | A participant can construct and self-host a validly encoded contribution and advertise it through willing peers. | It cannot compel another participant to validate, index, retain, or prioritize it. |
| Independent acceptance | A receiver's evidence contract and local checker determine formal acceptance. | Acceptance is relative to foundations, exact context, policy, and trusted computation. |
| Replaceable discovery | A receiver may use several discovery routes, export indexes, change index providers, or build its own. | No route guarantees global semantic completeness. |
| Replaceable storage | Exact payloads and dependency closures can be moved among willing providers without rewriting their mathematical contents. | No protocol creates storage after every holder has left. |
| Exit and fork | A participant can retain and export its data, use its preferred compatible software, and continue without permission from previous peers. | Continued interoperability requires shared encodings or explicit checked translations. |
| No mandatory operator | No named organization or service must remain online for all core operations or all cross-node exchange. | Connectivity still requires some functioning network and reachable peers. |
| Local policy sovereignty | Independent receivers may select different foundations, resource budgets, retention policies, and priorities. | The result is plural, scoped evidence views, not mandatory universal agreement. |

A network running on many machines but requiring one login service, one boot server, one index, one model API, one theorem approval key, or one package host does not satisfy the corresponding property.

Software licensing, public encoding specifications, portable archives, and independently implementable interfaces are part of the practical openness requirement. A protocol can be technically distributed but impossible to operate independently if its only checker, schema, or executable is unavailable under usable redistribution terms.

## System model and trust boundary

Use a time-varying directed communication graph \(G(t)\). Nodes know a bounded, changing set of contacts; nobody is required to know \(\mathcal N(t)\). Nodes may join, leave, crash, recover, equivocate, withhold objects, advertise false providers, or generate valid but unwanted mathematics. Agents, models, index services, and remote validators are untrusted input sources.

Separate four assumptions.

- **Local safety assumptions:** the receiver's canonical parsing and hashing, evidence checker, exact context binding, policy evaluator, protected storage, accounting, and isolation satisfy their specifications. The selected cryptographic assumptions hold for the current security profile. The mathematics remains relative to its declared logic and assumptions.
- **Communication assumptions:** particular messages or requested objects eventually cross a relevant honest, willing path. Partial synchrony, bounded delay, or resistance to traffic saturation must be declared separately when finite deadlines are claimed.
- **Availability assumptions:** a complete closure or enough valid coded fragments remains retained and reachable for the relevant interval; required providers have capacity to serve it.
- **Progress assumptions:** the receiver independently selects the relevant work, allocates finite sufficient resources, and services it fairly; the bounded checker computation terminates. Relevance and usefulness are not guaranteed by the transport protocol.

An honest receiver can preserve formal acceptance safety even if every remote contact is malicious: it rejects or fails to complete candidates without valid evidence. It cannot preserve useful remote discovery or retrieval in that execution. Byzantine safety and useful progress have different quantifiers.

Operational cryptographic identities authenticate messages, authority epochs, feed continuity, budgets, and key possession. They do not demonstrate that two keys belong to distinct people, independent operators, independent failure domains, or independent models. Producer attribution remains outside native theorem validity, except where an explicitly chosen evidence contract requires a particular scoped review or authority.

## Precise candidate requirements

These are requirements to specify and eventually verify, rather than claims that the current documents already establish them.

### Local autonomy requirement

Fix a retained dependency closure \(C\), a local task \(q\), and the exact local tool and policy state. Disconnect all network interfaces. Operations whose declared dependencies lie entirely in \(C\) must still execute according to their local specification and resource limits.

This is a trace refinement condition: projection of an online execution onto wholly local transitions must be reproducible by a valid offline execution when local inputs, tool behavior, random choices, and resources are fixed. It does not require identical scheduling or successful solution of an arbitrary mathematical question.

An exported package must identify which dependencies are locally present, which require retrieval, and which are optional accelerators. A hidden license check or mandatory remote model call on the acceptance path would violate this requirement.

### Producer independence requirement

For a native proof contract that does not explicitly require a scoped attestation, fix an exact proof package, closure, checker, policy, and admitted processing budget. Replacing transport source \(a\) by source \(b\) must not change the native checking result:

\[
\operatorname{NativeCheck}_i(C,q\mid\operatorname{source}=a)
=
\operatorname{NativeCheck}_i(C,q\mid\operatorname{source}=b).
\]

Sources may affect routing, admission, rate limits, or whether retrieval succeeds. This equation isolates checking after exact bytes have been obtained and admitted. It does not claim that all publishers receive equal resources.

### No mandatory online authority requirement

For every named service operator \(a\), remove that operator's services and keys from the available online dependency graph. Core local operations remain possible from retained materials. Cross-node exchange remains possible whenever at least one compatible willing route and the required retained data survive outside \(a\).

The qualification is essential. If \(a\) happens to hold the last copy of an object, removing it makes that object unavailable regardless of protocol. The requirement forbids designing \(a\) as an unavoidable authority; it does not assert redundant storage where none was paid for.

For collections that claim tolerance of any \(f\) failed independent operators, the retention and communication assumptions must ensure reconstructibility and a usable route after each such failure set. A count of \(f+1\) public keys is insufficient evidence of independent operation.

### Bounded receiver authority requirement

Unsolicited remote identities, objects, namespaces, feeds, or subscriptions cannot mint positive service shares or durable local records. Over any interval, total admitted work is bounded by receiver-issued resources and aggregate ingress/control allowances. All rejected or expired traffic is handled with bounded memory and amortized processing under an explicit ingress envelope.

This is not a guarantee of usable bandwidth against an adversary able to saturate every physical link or exhaust the operating system before protocol admission. Network and host isolation assumptions must accompany any availability claim. Nor is an individual finite quota a global bound if an attacker can create arbitrarily many independently provisioned quota classes.

A compatible participant may always use its own resources to operate. It cannot derive a claim on another participant's resources merely from producing a true statement. This preserves open participation without making every receiver an unlimited public computing service.

### Conditional useful delivery requirement

Fix a receiver \(i\), exact contribution \(c\), and a finite required closure \(C(c)\). Suppose:

- an honest publication route persistently advertises \(c\) under a key matched by an independently selected receiver subscription or lookup;
- relevant request and response messages are eventually delivered through willing peers;
- the required closure remains reconstructible and responsive long enough to transfer;
- descriptor, transfer, and validation work are finite under the chosen representation;
- the receiver authorizes that work, reserves sufficient resources, and services this admitted item fairly despite other traffic;
- the declared checker terminates on that item.

Then the receiver eventually obtains \(C(c)\) and records a local checking outcome. If the package satisfies its evidence and query contract, the receiver can integrate the checked result. This is an eventual outcome theorem under explicit assumptions. It does not promise finite latency without stronger bounds, solution of a research task, global retention, or the usefulness of every publication.

Proof outline: fair advertisement/lookup processing yields a candidate; eventual request/response delivery and finite reconstructible closure yield exact bytes; local fair service and checker termination yield a verdict; the atomic local integration transition records the outcome. Each arrow requires its own resource and fault assumptions. "The DHT will find it" is not a proof of the first arrow in a Byzantine open network.

## Bootstrap and discovery impossibilities

### A node cannot discover an unreachable universe

Consider a fresh node with no peer addresses, no accessible directory, no local discovery channel, no out-of-band exchange, and no responding public endpoint. Its local execution is indistinguishable between a world containing a large unreachable commons and a world containing no other participant. It cannot guarantee joining the former from local computation alone.

The requirement must therefore be **replaceable bootstrap**, not bootstrap without initial information. The distribution can carry several optional contact bundles; users can import a contact from a friend, institution, local broadcast, printed identifier, removable drive, alternate public directory, or previously exported peer cache. None is a theorem authority. Bootstrap contacts may be completely untrusted for content correctness.

This suffices for content safety but not anti-eclipse liveness. A malicious contact can reveal only malicious contacts, withhold all useful results, or claim that no useful results exist. A newly installed node must report its limited observed coverage, rather than treating successfully connecting to many keys as evidence of a representative network view.

### Sybil-resistant fairness needs an additional assumption

If identities cost nothing and a receiver grants each new identity an independent positive entitlement, an adversary can create arbitrarily many identities and consume an arbitrarily large aggregate entitlement. Cryptographic signatures do not repair this argument; they prove possession of keys, not scarcity of actors.

Consequently, the minimum public profile should allocate a bounded aggregate onboarding/exploration budget. Resource grants, fair queues, and durable state limits belong to the receiver. Optional invitation paths, proof-of-resource mechanisms, established relationships, deposits, or rate limits can improve service under particular threats, but each introduces costs or trust assumptions. They must not become tests of mathematical correctness.

An aggregate onboarding budget can prevent receiver exhaustion while still allowing adversaries to monopolize all of that budget. It gives resource safety, not universal newcomer fairness. Stronger newcomer-liveness claims require a mechanism and an adversary bound; they remain an open design obligation.

### Reachability is necessary for censorship resistance

If every communication route from a receiver is controlled by omitting peers, no protocol can guarantee it discovers withheld data. Multiple providers, diverse routes, direct invitations, portable archives, and independently operated indexes reduce exposure. Without an honest-route assumption, they do not prove resistance to complete eclipse.

A mathematical proof can remain valid despite censorship, yet be practically useless to a node that never sees it. The architecture must evaluate both acceptance safety and the ability to find useful work.

### No complete membership view in a fully open asynchronous network

A receiver observing a finite execution cannot distinguish "no other participant exists" from "another participant joined and all its messages are delayed." It cannot certify a complete live roster without imposing a membership boundary and additional completion assumptions.

Therefore no ordinary theorem lookup, local acceptance, or publication should require a complete current membership list. Exact global counts and global completeness claims must be scoped to an explicitly named collection, overlay, or observation procedure.

## Recommended public topology

The candidate architecture is a federation of independently operated object stores, feeds, and replaceable index overlays.

**Object stores.** Each provider offers exact content identifiers and optional availability/retention statements. The receiver fetches from one or more selected providers, verifies content identity, materializes the required closure, and runs its own admission/checking procedure. Payloads need not pass through indexes.

**Publisher feeds.** A publisher may maintain an authenticated sequence of bounded descriptors and corrections. A feed establishes what that publisher committed to in a particular sequence and authority epoch. It is neither a global publication ledger nor a proof that the publisher revealed everything it knew. Feeds can be mirrored, queried by explicit sequence, and exported with their retained content.

A publisher can sign incompatible continuations. A receiver detects an observed sequence gap or inconsistency; equivocation hidden in disjoint views becomes detectable only when the views meet or an appropriate witness mechanism exposes them. A feed signature alone therefore cannot establish one globally unique latest feed head. Coverage claims bind the exact observed branch and checkpoint, and unresolved inconsistency affects coverage without directly deciding mathematical validity.

**Index overlays.** Several independent services or cooperative groups can index overlapping portions of the commons. Each advertises its schema, collection scope, version, checkpoints, supported predicates, coverage, and service limits. A receiver may consult multiple overlays and merge candidate lists. Exact keys and structural keys are primary; semantic ranking remains advisory.

**Local indexes.** A node can always derive exact indexes over its own admitted snapshot. These are the foundation for offline usefulness, reindexing after an upstream service disappears, and independent review of advertised collection coverage.

**Gossip and subscriptions.** Participants disseminate small descriptors, capability/compatibility hints, and relevant incident notices under quotas. Most nodes follow selected interests and active dependencies. They are not required to receive every feed or remember every participant.

**Direct exchange.** A receiver knowing an exact content identifier and a willing provider must be able to fetch without first obtaining approval from an index overlay. A receiver with a portable archive must be able to check and import without any live network connection.

An optional overlay may use a DHT, consistent hashing, rendezvous hashing, authenticated membership, or replicated index authorities internally. Its assumptions remain properties of that overlay. There is no single global shard owner table, required DHT operator set, or network membership epoch.

In particular, CP-001B's authenticated shard configuration \(\mu\) becomes \(\mu_{o,v}\), the named configuration of overlay \(o\) at version \(v\), when applied to this public design. A receiver's frontier is a bounded collection of scoped feed or overlay observations. It is not proof that every possible publisher has been covered.

Re-sharding within an overlay can require authenticated handoff and continuity proofs. Moving to a different independently operated overlay does not establish that the new service inherited all old coverage. The receiver must treat its frontier as different or verify a precisely specified transfer.

## Why not require one public DHT

A DHT is one mechanism for locating data; it is not the definition of decentralization. A conventional logarithmic lookup analysis assumes a suitable routing population and distribution, available routing state, and bounded churn. It does not establish the same bound under adversarial identity grinding, eclipsed routing tables, targeted withholding, or malicious key-placement concentration.

Three candidate designs deserve separate analysis:

| Alternative | Benefit | Main limitation |
|---|---|---|
| One open public DHT | Common discovery path and broad potential reach | Sybil/eclipse resistance, bootstrapping, hot keys, and resource admission become critical common dependencies. |
| Multiple optional DHT/index overlays plus direct exchange | Operators and users can replace discovery infrastructure; subsets can specialize | More duplicate descriptors and queries; no automatic global recall or consistent shard map. |
| Relationship-based feed exchange and archive federation | Simple trust boundaries, strong offline portability, useful with existing communities | Slower cross-community discovery; possible isolated knowledge clusters. |

The second is the preferred conceptual direction, with the third as a valid minimal public operation mode. A common discovery convention improves interoperability; mandatory dependence on one discovery authority reduces it. A comparison should measure useful retrieval yield, suppression under attack, transfer/check cost, and operational concentration rather than choosing a topology by terminology.

## Retention, indexes, and the last-copy problem

Object publication, mathematical checking, index inclusion, and durable preservation are distinct state transitions. Each needs an owner of the consumed storage and work. Exact bytes do not remain available merely because a hash, signature, append-only record, or proof of prior possession survives.

For a full-replication retention contract tolerating loss of any \(f\) independent failure domains, at least \(f+1\) domains must hold the required closure at the relevant time. For an \((n,k)\) coded object, retrieval needs at least \(k\) valid usable fragments with the decoding metadata and accessible environment. Domain-level failures may remove several fragments, so \(n-k\) is a fragment-loss tolerance, not automatically an operator-loss tolerance.

For independent per-replica unavailability probability \(p\), \(r\) full replicas have simultaneous unavailability probability \(p^r\). Shared credentials, cloud regions, software defects, funding, or operators violate independence. A service must not use the equation without declaring and supporting its failure model.

Suggested contracts specify retained closure, term, reconstruction condition, independent-domain evidence, audit method, grace interval, repair resource allocation, and permitted degradation. Audits detect some historical or current failures; they do not compel future service. Proofs of retrievability or possession may inform an availability assessment under their extraction assumptions, but do not by themselves guarantee timely delivery to every receiver.

Useful mathematical objects often depend on shared foundations. Retaining a theorem while losing its exact definitions, axioms, environment, or certificate interpreter is insufficient for exact replay. Retention therefore follows dependency closures, with reference accounting and preservation of shared hot dependencies.

Indexes also need capacity, replication, and continuity. Keeping proof payloads while losing every useful descriptor makes discovery expensive. Keeping descriptors while losing payloads leaves an unavailable catalogue. Reliability measurements must report both cases.

No protocol can retain every arbitrary new object forever with bounded total storage. No retention rule can guarantee preserving every object that some adversarial future task might require. The defensible objective is durable coverage of declared collections and demonstrated downstream usefulness under a workload model.

## Exit, fork, and rejoin

**Graceful exit:** stop accepting new commitments; export a complete manifest of the participant's selected collections; publish bounded expiring provider updates; offer transfer to willing recipients; finish or explicitly degrade existing retention obligations. The network cannot assume every exit will be graceful.

**Unannounced failure:** peers expire provider records, record uncertainty, attempt alternate providers, and initiate already budgeted repair when warranted. The absence of a departing node's signed approval must not prevent surviving nodes from serving exact objects they already hold.

**Fork:** a participant can adopt different resource policies, foundations, indexes, or software while preserving exact old content identifiers and provenance of environments. Different foundations produce different context-bound judgments. A fork does not need to erase objects or rewrite a universal ledger.

**Rejoin:** exchange bounded inventories and candidate descriptors; resolve exact bytes by content identifiers; independently re-admit imported evidence; verify compatibility and policy choices. Matching remote claims are not automatically adopted as local status. Old authority epochs, expired capabilities, and remote budgets do not become valid local authority through rejoining.

Forking is compatible with a common mathematical commons when object identities, foundation profiles, and proof interfaces remain interpretable. Where they diverge, explicit translation or checked bridges are required. Social agreement on one canonical branch is not needed for native proof checking.

Portability requires an export to contain exact objects, manifests, selected policy/environment commitments, and enough indexing metadata to rebuild the collection. A dump that contains only proprietary database keys or links to the original host is not a portable archive.

## Long-lived upgrades

A long-lived mathematical commons needs more than versioned networking. Schema, hash function, signature scheme, proof language, checker, library, and foundation versions can all change.

- Exact versions and domain separators belong in object and protocol interpretation. Unknown versions yield an explicit unsupported outcome, not reinterpretation under the nearest available checker.
- Network negotiation does not authorize execution of downloaded code, a policy update, or a checker substitution. The local operator admits software and verifier changes through a separate authority path.
- New descriptors can refer to old exact objects; a migration that changes bytes creates a new identifier plus a declared relation to the old representation. Semantic equivalence requires checking the relevant relation rather than copying an old accepted flag.
- A checker security incident affects reliance on results that depend on the compromised checker profile. It does not mathematically refute all of their statements. Rechecking with an independently acceptable implementation may restore particular results.
- Deprecating a hash or signature scheme requires an explicit migration threat model. Dual commitments and archived verified mappings established before a break may help. Once the original binding is ambiguous or compromised, hashing the ambiguous reference again cannot retrospectively identify the intended object.
- Exact old environment bytes should remain archivable. Running old executable environments can itself be unsafe; sandboxing or a new checker for their declarative certificates is a separate obligation.
- Upgrade manifests and release signatures identify a distributor's claim. No distributor key is a mathematical truth authority or a compulsory remote kill switch.
- Compatibility can be preserved by overlap periods, multiple schema readers, explicit adapters, and archived conformance fixtures. An update has to specify what remains interoperable and what requires revalidation.

A particular optional overlay may agree on a new protocol or membership version using local consensus. That agreement governs only its own service state. It cannot force every independent receiver to adopt a new foundation or accept a theorem.

## Hidden dependencies that would undermine the vision

| Dependency | Failure mode | Required escape path |
|---|---|---|
| One bootstrap domain | Fresh nodes cannot find peers when it disappears or censors | Manual contacts, cached peers, alternate contact bundles, offline imports |
| One package registry or binary host | New installations and replays cease | Redistributable source/binaries, mirrors, content-pinned releases, archived toolchains |
| One commercial model API | Autonomous generation disappears when access or prices change | Model-agnostic interfaces, local or alternate generation, manual theorem contribution |
| One hosted semantic index | Relevant earlier work becomes invisible | Exact/local indexes, multiple discovery overlays, structural search, portable catalogue manifests |
| One identity or login provider | Participants can be globally excluded | Locally generated operational keys and peer-chosen authentication |
| One cloud storage account | Many apparent replicas fail together | Independent failure domains, portable object format, funded transfer and repair |
| One release or revocation key | Compromise can pressure everyone into the same bad update | Local upgrade choice, pinned profiles, multiple maintainers/implementations, explicit review |
| One foundation or library maintainership | Old proofs cannot be replayed or changed definitions silently shift meaning | Immutable versioned closures, independent mirrors, explicit migration evidence |
| One public token or payment chain | Access depends on external consensus or affordability | Core local operation and voluntary exchange without mandatory chain access |

These escape paths are requirements to demonstrate in a future artifact. Stating that alternatives are theoretically possible does not show that a user can actually use them.

## Relationship to the existing five-cell plan

The five authenticated independent cells in CP-001A/CP-001B are a controlled experiment. They are useful for testing exact checking, accounting, passive reuse, storage, scoped indexes, and partition behavior. Their known roster makes certain routing and coverage statements possible.

They do not establish permissionless entry, public routing security, healthy bootstrapping, independence of operators, Sybil-resistant service, or public-network liveness. Simulating many logical agents under five known operators does not establish those properties either.

The next concept checkpoint should therefore state two profiles explicitly:

- **Experimental profile:** known cells and declared fault/load schedules; bounded scopes allow precise measurements and model checking.
- **Open commons profile:** no global roster; local operator sovereignty; replaceable bootstrap and discovery; scoped overlay assumptions; identity-independent native checking; conditional discovery, availability, and anti-censorship claims.

The profiles should share exact evidence formats and acceptance semantics. The open profile cannot inherit a fixed-roster proof by merely replacing five with a very large number.

## Issues that remain unresolved before implementation

| Obligation | Why it matters | Acceptable concept evidence |
|---|---|---|
| Open ingress under Sybil traffic | Aggregate quotas bound cost but can still exclude newcomers | Explicit adversary budget, admission policy, and liveness claim or stated non-claim |
| Public route diversity | A large neighbor count may still represent one attacker | An honest-contact assumption and a concrete way to obtain/recover diverse routes |
| Overlay coverage semantics | Different indexes expose incomparable incomplete worlds | Typed scope/frontier model and rules for comparing or merging observations |
| Finite-state feed continuity | Unbounded feeds, tombstones, and replay records consume storage | Bounded snapshots/compaction plus exact continuity and replay semantics |
| Retention sustainability | Everyone may prefer to consume popular work while rare work disappears | Explicit voluntary service commitments, costs, policy alternatives, and workload assumptions |
| Exit and replacement | A vanished authority must not strand otherwise recoverable bytes | Archive and handoff specification independent of the old operator's online approval |
| Cryptographic migration | Old hashes and signatures may age before mathematics does | Versioned trust model, pre-break migration procedures, and post-break limitations |
| Cross-foundation interchange | A common wire protocol cannot make incompatible assumptions identical | Exact foundation identifiers and checked translation obligations |
| Offline install and recovery | P2P running nodes can conceal central supply-chain dependencies | Portable distribution and reconstruction requirements from archived materials |
| Useful contribution selection | Open publication alone can accumulate valid junk | Demand/reuse policies with measurable downstream outcomes and protected exploration |

Proof and counterexample work should focus first on the boundaries where one layer could accidentally confer authority on another: feed identity versus truth; index inclusion versus availability; publication versus resource entitlement; software updates versus theorem acceptance; and same-overlay convergence versus universal agreement.

The system can offer unconditional local protocol invariants only relative to its local trusted computing and resource model. Broad properties such as useful discovery, durable preservation, bounded delay, and expanding coverage are conditional service claims. Making their assumptions explicit is part of the design, not an optional qualification added after implementation.

## References and input trace

- [Project README](../../README.md), consulted for the current priority ordering, autonomous loop, and five-cell experimental boundary.
- [CP-001A: autonomous research and optional coordination](../checkpoints/CP-001A-autonomy-first-cooperation.md), especially autonomous admissibility, query-relative acceptance, receiver-owned fairness, resource authority, independent-purpose reuse, retention, and conditional liveness.
- [CP-001B: distributed corpus and scoped status](../checkpoints/CP-001B-distributed-corpus-and-global-status.md), especially impossibility boundaries, authenticated scoped frontiers, retention, sharded indexing, and the fixed-roster threat assumption.
- [Technology reuse map](../../research/COOPERATION-TECHNOLOGY-REUSE.md), consulted for the separation of native proof checking, cryptographic arguments, candidate discovery, and optional public DHTs.

This note introduces conceptual requirements and proof sketches. It does not claim externally checked performance guarantees for a particular DHT, storage network, proof-of-retrievability scheme, or blockchain. Those choices require exact specifications and threat models before adoption.
