# CP-001E: goal-fitness audit of agent reuse and discovery

Date: 2026-09-19  
Status: Adversarial concept analysis and proposed optional client/index profile; not approved protocol, code, benchmark, or implementation qualification  
Scope: Local-agent usability and large-network discovery, with CP-001D frozen and unchanged

## Verdict

ORG1 is a credible bounded substrate for locating exact known content and checking selected evidence. It is not yet a demonstrated practical discovery system for a large, heterogeneous community of Lean agents. Safety after obtaining the right ReplayID does not establish that an agent can obtain that ID, understand the interface affordably, instantiate the result in its own environment, or gain more than it spends importing it.

Three properties must be distinguished:

1. **Sound reuse:** the actual checked application of exact evidence is correct relative to the stated foundation.
2. **Affordable access:** a selected agent can retrieve, reconstruct, and use that evidence within its local resources.
3. **Useful discovery:** the finite candidate window often includes evidence that helps that agent's independently chosen work.

CP-001D gives conditional contracts for the first and parts of the second. Its structural keys, contact policy, and observed-use heuristics are candidates for the third, not evidence that the third holds. A usable first release needs a concrete external client adapter and qualified retrieval recipe, not only more correctness disclaimers. The recommendation below keeps mathematical authority unchanged while making those missing mechanisms explicit.

There is no human-intention field, research assignment, unsolved-problem registry, mandatory root goal, or demand that an investigator explain why an expression interests it. Searching for existing material using a locally selected expression is ordinary retrieval. The network is not asked to prove that expression, solve its residual hypotheses, or maintain it as a public unanswered question.

## Audit basis and boundary

The frozen references are [ORG1](../../spec/OPERATIONAL-CORPUS-V1-ORGANIZATION.md), [native mathematics](../../spec/OPERATIONAL-CORPUS-V1-MATHEMATICS.md), [NET1](../../spec/OPERATIONAL-CORPUS-V1-NETWORK.md), and the [integrated interface](../../spec/OPERATIONAL-CORPUS-V1.md). This note does not amend them.

CP-001D already allows a client to install private aliases, notation, instance registrations, and simplifier hints after checked native reconstruction. That permission is important but is not a specified ergonomic adapter. No interoperable exporter/importer or representative library replay has yet been qualified. Any practical claim below is consequently a proposed qualification target, not an existing capability.

The external agent remains free to use tactics, search, language models, or handwritten proofs. A retrieval adapter can prepare candidates and tentative applications. Only the resulting exact native proof and selected replay closure establish an admitted mathematical result. A feature extractor, metadata bundle, learned ranker, or elaborator is not promoted into the mathematical acceptance relation.

## A local agent's actual path

The real path is longer than `query -> theorem`:

\[
\text{local expression/interface}
\longrightarrow\text{candidate discovery}
\longrightarrow\text{bounded statement inspection}
\longrightarrow\text{candidate instantiation}
\longrightarrow\text{closure acquisition and replay}
\longrightarrow\text{checked local application}.
\]

Failure at each boundary differs. No candidate may have been discovered; a candidate may use a different structure; arguments may remain uninstantiated; a necessary premise may be unavailable; the closure may exceed budget; or native checking may reject the actual term. A client should receive those distinctions and measured costs rather than one undifferentiated `not found` result.

The dominant cost need not be finding a statement. A ten-line lemma may have a large first-use dependency closure. A second use in the same compatible environment may be cheap. Conversely, an attractive statement can be discovered rapidly but depend on an incompatible copy of an algebra hierarchy. Ranking needs a local environment and a closure-cost estimate, not only a theorem's apparent size or popularity.

## Failure modes that materially threaten the goal

### Exact identity is necessary, but does not unify mathematical interfaces

Renaming a declaration or its binders alone does **not** create another ID when canonical payloads and references are unchanged. The native profile already avoids that elementary duplication. The problem is different formal encoding, not merely different spelling.

| Difference between two developments | Identity/applicability consequence | Safe response |
|---|---|---|
| Only source aliases or binder names differ | Canonical content can be identical | Reuse the same exact ID; keep aliases advisory |
| One definition inserts a beta-redex or uses a different checked helper | DefinitionID can differ although unfolding gives the same meaning | Keep both IDs; bounded conversion can help candidate matching, then native checking decides the actual application |
| Different native group descriptors representing isomorphic record/inductive interfaces | Different GroupIDs; generally not definitionally equal | Reuse the shared exact group, or import a checked explicit adapter/transport theorem |
| Same informal structure, different field order or superclass organization | Projections, parameter ordering, and instance interface can differ | Exact interface mapping and checked construction are required |
| Different fixed native profile/bootstrap | Profile-bound IDs and potentially different foundational rules | Do not merge environments by labels; use a compatible isolated environment or a separately qualified translation |

For example, suppose `MonoidLike1 A` and `MonoidLike2 A` have genuinely distinct checked GroupIDs because their descriptors use different fields, field order, or helper references. A theorem taking the first does not automatically accept an instance of the second. Independently generating the exact same canonical group descriptor can instead deduplicate to one GroupID; different source authors or names alone do not force this incompatibility. A checked function from one distinct structure to the other may suffice for a particular theorem; equality of carrier types or an informal claim that both are monoids does not. If a theorem mentions the structures' operations, their preservation must also be checked. A generic assertion that the structures are "equivalent" is not an application recipe.

The cheapest successful path is often voluntary reuse of an exact shared interface bundle. This is not a central authority: anyone can retain a different bundle, and bundles cannot declare mathematics true. But unrestricted interface divergence has a real cost. With m incompatible encodings, independently supplying every directed pairwise adapter would require up to m(m-1) translations: 100 encodings give 9900 possible directed pairs. A checked shared hub interface can reduce the number of supplied conversions toward O(m) for supported translations, at the price of a consciously selected interface and possible expressiveness or performance loss. This arithmetic is not a theorem that arbitrary mathematical theories admit those translations.

### Raw structural keys are weak for ordinary mathematics

Many useful theorems conclude with equality, implication, membership, an order relation, or a common proposition constructor. The head is often a ubiquitous logical constant rather than the operation the agent wants. In practice, projections and class dictionaries complicate the application spine. `STRUCT1` must not be assumed to extract all practical group/constructor/projection selector information merely because it indexes ordinary constants.

The first-32-symbol policy can miss the only discriminating symbol after 32 unrelated symbols in telescope types or earlier subexpressions. The 4096-occurrence traversal can miss a useful suffix entirely. A query requiring such a symbol can return zero even though the complete checked statement contains it. Increasing the ranker's intelligence after this exclusion changes nothing: the candidate never reaches it.

Raw exact keys also separate a term from a definitionally equivalent wrapper around that term. Optional beta/let normalization does not solve arbitrary definition unfolding, representation translation, or equivalence by a nontrivial theorem. An index needs several bounded views, with explicit incompleteness, not a claim to canonicalize mathematical meaning.

### Prefix caps can produce permanent practical starvation

ORG1's deterministic ordered scan is valuable for reproducibility. However, repeated short searches can return the same prefix forever. A rare useful theorem beyond that prefix receives no opportunity merely because the client repeatedly asks. Round-robin merging across peers does not solve an inaccessible tail within every selected peer.

At the default 16384-root local ceiling, an all-match head bucket with 64 results per page requires 256 pages. At the hard 262144-root ceiling, it requires 4096 pages. These are profile-consistent examples, not an imaginary unbounded single node.

Assume a 50-ms round-trip time, no setup/CPU cost, and the two request/response stages required by one paid continuation. A dependent cursor chain then takes approximately 0.1 seconds per page: 25.6 seconds and 409.6 seconds respectively. Four independent peers can be queried concurrently, but four requests cannot advance the same opaque continuation chain before its predecessor returns. The hard-limit example cannot finish within the default 120-second snapshot lease under those assumptions. Increasing transfer efficiency does not alone fix that query-prefix problem.

For a single uniformly positioned eligible item in a 262144-entry bucket, a one-page 64-item prefix has expected inclusion probability 64/262144 = 1/4096, about 0.0244 percent. This uses a stated random-position model; the worst-case inclusion is zero. Repeating exactly the same prefix does not produce independent trials.

An exact JudgmentID lookup can bypass this case when the agent already knows the exact desired statement identity. The problem remains when looking for a more general theorem, a rewrite relation, a useful interface, or a result requiring instantiation. A benchmark that gives every agent the answer's exact ID does not qualify general discovery.

### Four-peer fanout is not the principal global bound

Four is a concurrency bound per round, not a lifetime limit of four providers. Later paid rounds can inspect other contacts. The more consequential bound is the admitted finite directory/session horizon and what that directory knows about collection coverage.

For illustration, suppose a million index providers exist, 100 cover an exact specialized interface, and the receiver's contacts are sampled uniformly without useful routing information. Four sampled providers hit at least one specialist with probability approximately 0.040 percent; 256 hit with probability approximately 2.53 percent. These are sampling-model calculations, not an adversarial guarantee. Accurate collection routing can improve them greatly; correlated contacts or misleading coverage can be much worse.

Sixteen advertised exact keys cannot summarize every interface of a diverse provider. The absence of a key is therefore not absence of coverage. Local response history favors previously queried collections and can repeatedly choose an irrelevant but healthy peer for a new subject. A node with a high-quality exact local index but no discoverable route contributes little to other agents' practical experience.

A global union of, for example, 40 million descriptors may be distributed across hundreds of bounded providers. No single frozen NET1 node is silently assumed to retain that entire union, and a bounded lookup session is not a complete federation-wide scan.

### Kernel declarations alone are an austere Lean interface

The mathematical representation erases implicit binder information and source binder names, gives generated names to nonseed declarations, and does not automatically install class/instance or simplifier registrations. Explicit term reuse remains possible. Familiar source expressions, instance synthesis, overloaded notation, and existing tactics need additional client metadata or an adapter that constructs explicit applications.

This is especially important for independent LLM-based agents trained on ordinary Lean source: an environment of generated names and explicit argument positions is not equivalent to the source-level library their model expects. Retraining the model is not a prerequisite to repairing that interface; a stable local naming/metadata view can bridge much of the ergonomic gap. Its factual binding still must be checked against exact native declarations.

Registering every remotely suggested instance or rewrite automatically is not an adequate repair. Even mathematically valid instances can create divergent instance search; true rewrite lemmas can create loops, expansion, or catastrophic simplifier cost. Native proof checking prevents false acceptance, not elaboration denial of service. Metadata activation therefore needs local selection and finite search limits.

### Usage is informative, manipulable, and not a necessity certificate

Let `p : P` and `q : Q` be checked proofs. The native term `(fun (_h : P) => q) p` has type Q and syntactically references p, although beta-reduction removes that dependency. Therefore even a receiver-extracted, fully checked downstream edge can be a padded use rather than a necessary contribution.

An adversary or mistaken generator can also produce many distinct trivial downstream judgments, each mentioning the same favored lemma. Exact-ID deduplication removes literal duplicates, not arbitrary equivalent padding. General detection of all semantically unnecessary premises would require substantially more reasoning than reading dependency edges and cannot serve as a free universal filter.

This does not make usage metrics worthless. It means a ranking must cap their influence, prefer observations of receiver-authorized local activity over imported self-advertisements, keep zero-use exploration, and expose the counter's scope. Neither distinct keys nor distinct proof IDs establish distinct independent demand. A low-use theorem is not invalid or necessarily unimportant.

## An optional external client profile: REUSE1

REUSE1 is a proposed client convention, not a new mandatory corpus goal/task system. It can initially operate over frozen NET1/ORG1, with the limitations identified below. The client owns its query context and may discard it after the bounded operation.

### Ephemeral request and outputs

A local request contains:

- an exact locally admitted native profile and environment view;
- a well-scoped local telescope and a selected formal expression or expression pattern;
- an optional operation hint such as `related statement`, `rewrite candidate`, `interface construction`, or `exact identity`;
- allowed foundation/footprint constraints and a resource envelope;
- owner-authorized network-disclosure settings.

The operation hint chooses a retrieval procedure, not a requested theorem-construction obligation. The network receives only the existing-content predicates or approved structural features needed by that procedure. It does not receive or retain a research task, and it does not solve resulting hypotheses. Sending even structural keys can reveal an investigator's subject; remote discovery is opt-in under local disclosure policy.

Outputs are exact candidate identities, scope/snapshot and truncation flags, a bounded formal statement view, optional tentative argument maps, unresolved formal obligations, estimated or measured import costs, and a precise result class:

- `EXACT_ID_FOUND`;
- `STRUCTURAL_CANDIDATE`;
- `TENTATIVE_MATCH_WITH_RESIDUALS`;
- `CHECKED_LOCAL_APPLICATION`;
- `INCOMPATIBLE_EXACT_INTERFACE`;
- `UNKNOWN_MATCH_BUDGET` or `UNKNOWN_DISCOVERY_BUDGET`.

These are client-layer results. Only `CHECKED_LOCAL_APPLICATION` includes a kernel-checked term under the actual local environment and exact admitted evidence. A timeout is not an incompatibility proof. A failed heuristic match is not a proof that the theorem cannot be used.

### Formal application boundary

Suppose a candidate theorem has checked type

\[
p : \Pi x_1:A_1.\cdots\Pi x_n:A_n(x_{<n}).B(x_1,\ldots,x_n).
\]

A matcher may propose a substitution sigma. To claim an application in local context Gamma, every actual argument must check against its dependent instantiated type and the resulting `p sigma` must check against the claimed result type, including any required definitional conversion. Unassigned metavariables, guessed class instances, unresolved law proofs, or unproved interface conversions remain residuals; they are not silently installed as assumptions of an unconditional result.

For a rewrite candidate, matching one side of a checked equality to a selected subexpression is only a proposal. Rewriting under dependent contexts can require an explicit transport/congruence proof. The client constructs and checks that proof. It does not replace a subtree merely because printed terms or embeddings resemble each other.

Candidate matching is bounded and incomplete. In the simple case of a theorem `P -> Q`, deciding whether it supplies Q can already require producing P. REUSE1 does not hide general proof search inside an allegedly cheap applicability predicate. It can return the residual P to the external investigator without creating an in-system unsolved-problem record.

### Inert advisory library views

An optional `LibraryView` is a bounded client-side data bundle keyed by exact native profile and declaration IDs. It can contain:

| Data | Use | Required boundary |
|---|---|---|
| Human-friendly aliases and source-qualified labels | Display and model/source compatibility | Never replace exact target IDs or silently shadow another binding |
| Original binder/argument hints | Construct readable source wrappers and explicit applications | Actual dependent argument types come from the checked declaration |
| Structure/class labels and field selectors | Navigate a known exact interface | Class labels alone do not identify two distinct GroupIDs |
| Candidate instance IDs with class/parameter hints | Seed bounded local instance search | Check the actual instance type; activation is local and cannot execute scripts |
| Candidate rewrite IDs and orientations | Seed a locally chosen simplifier set | Checked equations, cycle/expansion precautions, finite simplifier budget |
| Exact module/collection identifiers and public provider hints | Route to compatible material | Advisory availability/coverage only |

One initial client policy permits at most 4096 view entries and 8 MiB per admitted view, with a separate aggregate view-cache cap and bounded alias strings. Count and byte limits apply together. These are proposed local defaults, not new frozen wire limits. Unicode/display sanitization, conflicting aliases, and stale profile references need explicit handling. Unknown or conflicting aliases display their exact ID suffix rather than silently selecting one declaration.

Views are inert data: no macros, plugins, executable code, filesystem fetch directives, or automatic tactic execution. A local standing policy may enable a selected bundle's bounded declarative conveniences; it need not ask a person about every theorem. Offline/software-packaged views remain usable. The selected decentralized distribution path is the optional `ADVISORY_READ1` capability below, not an implicit enlargement of frozen native read scopes.

For a minimal safe client, retain explicit generated declarations as the kernel-facing namespace and put friendly names in wrappers or a display/name-resolution map. Do not mutate the identity or type of an imported constant to simulate source compatibility. If implicitness hints cannot be restored faithfully, use explicit argument construction and report the ergonomic limitation.

### Selected distribution path: ADVISORY_READ1

`ADVISORY_READ1` is a negotiated new-profile capability for explicitly public inert bundles. A new-profile HELLO reply may contain at most four optional public advisory-manifest root hints, still within its existing overall message/control limits. A client may also learn an exact root through an offline bundle or a previous authorized application. A hint does not authorize automatic fetching, activation, or executable installation.

An advisory manifest is an immutable, typed data object containing a canonical sorted duplicate-free list of `[advisoryKind, dataContentID, encodedLength]` entries. The supported data kinds are exactly the defined `LibraryView` and `CollectionGuide` records/pages. The manifest does not contain its own hash. The selected bounds are:

- manifest payload at most 64 KiB and at most 1024 listed typed data IDs;
- at most 1 MiB per listed data object;
- at most 8 MiB for the manifest plus all listed payloads;
- at most 4096 total advisory entries across the bundle;
- a separate receiver-local aggregate cache/activation allowance.

All count, encoded-byte, parsing-depth, and resource limits apply together. A view larger than one object is explicitly divided into bounded listed pages. Unknown critical kinds or schema versions are unsupported, not interpreted as arbitrary blobs. Human-readable text is bounded inert UTF-8 data; it is not an instruction channel for the node or agent. Public source labels can be wrong or malicious, so clients retain the exact-ID binding and sanitize display/name resolution.

The provider activates a bundle only through its owner's explicit disclosure authority covering the exact manifest and every listed payload. Proposed BUNDLE1 reads use `readScope = [2, advisoryManifestCID]`. That scope permits the manifest itself and exactly its listed, type-checked advisory data IDs. It does not recursively follow references found in their contents. In particular:

- an alias naming a JudgmentID does not authorize reading that theorem's bytes;
- a guide naming another bundle, contact, profile, or collection does not authorize fetching or installing it;
- native proof acquisition still needs its independent public-native-root or live export scope;
- no grant, checker-private record, meter, native declaration, executable, or arbitrary CAS object becomes readable merely because a bundle cites its ID;
- a signature, alias, route, or bundle membership supplies no native validation authority.

The provider reserves and meters advisory serving through the same finite call/delivery mechanism. Disclosure scope/version is rechecked at delivery claim, just as for mathematical public data; withdrawal cannot recall already transmitted bytes. The receiver first checks exact hashes, lengths, schema, and aggregate allocation. That permits bounded inert storage and visibly untrusted display/routing hints; it does not require importing every mathematical target mentioned in an eight-MiB guide.

Semantic activation is **per entry**, only after that entry's exact required target interface is checked locally under the applicable current-use policy and its claimed declaration binding is verified. Unfetched entries remain tentative hints, not installed native meanings, active instances, or rewrite rules. Activating one entry does not activate the entire bundle or grant reads for its other references. Actual proof use retains the ordinary complete selected closure, footprint, and native checking requirements. Successful bundle transfer is not proof that a label is accurate, that a suggested instance is appropriate, or that a provider remains available.

This path is specified jointly with the [CP-001E exchange proposal](CP-001E-exchange-scaling.md). It is not supported by frozen NET1 and cannot be sent to a legacy peer without capability negotiation. If unsupported, the client can still use packaged/offline views and exact native reconstruction. A new source may publish its inert naming/interface bundle alongside its ordinary independently checked native roots without obtaining central permission. Original source names are optional conveniences, not required mathematical identities or political attribution records.

## Frozen-compatible bounded retrieval recipe

The following is usable as a paper baseline without pretending ORG1 has undeclared query features.

1. Inspect the locally chosen expression and its type in the existing checked environment. Preserve exact universe and variable scope. Extract candidate anchors separately from its conclusion, operations/relations, type constructors, and relevant explicit interface instances.
2. Search exact known IDs and compatible local caches first. If an exact JudgmentID is available, try its direct lookup before a broad head scan.
3. Build at most six existing ORG1 predicates from those anchors: discriminating one-/two-symbol conjunctions; a head plus a nonubiquitous symbol; an exact certified-relation endpoint when known; and one deliberately relaxed query. Frequency estimates from the local collection can choose anchors, but remote frequencies remain uncertain.
4. Allocate at most 24 paid FIND pages across selected peers and continuations in the initial interactive attempt, at most four peers concurrently, and an explicit total byte/time budget. A continuation consumes one of those pages. Coverage-aware contacts and one exploration contact follow NET1's bounded policy; new contacts require a new admitted session when outside its pinned horizon.
5. Merge in lane/peer round-robin order before final scoring. Deduplicate exact descriptor IDs and evidence pairs. Present one judgment initially with up to four available evidence alternatives; this display grouping does not equate the alternatives' costs, footprints, or acceptance states.
6. Inspect bounded native statement syntax for the best candidates, using locally available data first. Remote syntax remains a candidate until its bindings and necessary environment are checked. If complete statement data or definitions needed for conversion do not fit this phase, return an unresolved candidate rather than guessing.
7. Perform bounded telescope alignment, pattern matching, and local definitional-conversion trials. Do not solve arbitrary premises or run remotely supplied tactics. Re-rank using the observed residuals, exact interface compatibility, and local import-cost information.
8. Select a small number of candidates for separately admitted closure acquisition/native replay. Construct and check the desired local application, then export any resulting new work through ordinary native admission. Failed imports or applications do not silently change the candidate identity.

An illustrative interactive envelope is 10 seconds wall time, 2 local CPU-seconds, 64 MiB temporary memory, 24 FIND pages, and 8 MiB total discovery traffic. Keep at most 1536 descriptors, subject also to the byte limit; inspect at most 32 candidate statements, with remote statement probing additionally limited to 64 paid object-read calls and 512 KiB of newly fetched syntax. All discovery traffic shares the same aggregate 8-MiB ceiling. When a single required statement exceeds the small inspection allowance, explicitly offer a separately funded deep inspection.

These limits are an honest bounded attempt, not a promise to return an applicable theorem in ten seconds. Descriptor bodies, local data structures, incomplete fetches, and all calls count. The full proof/replay phase has its own declared import envelope and latency; it is not hidden inside that ten-second interface. A cached statement can be inexpensive to rank while its missing proof closure remains expensive to admit.

### Ranking after matching

Rank only within the finite obtained candidate set. An initial deterministic ordering is:

1. actual known exact-interface compatibility, ahead of unresolved interface conversion;
2. stronger completed local matching evidence, with fully checked application ahead of tentative matching and shape-only candidates;
3. fewer unresolved dependent argument/premise obligations, while reporting their structure rather than treating a count as difficulty;
4. lower measured/estimated marginal acquisition and replay cost in this exact local cache/environment, with unknown costs explicitly unknown;
5. bounded local retrieval/use recency; then a stable exact-ID tie-break.

Prefer lower-cost permitted proof alternatives only after respecting the caller's actual footprint constraints. A remote performance claim is not a receiver measurement. A theorem with one hard premise is not necessarily preferable to one with three trivial premises; the ranking is a starting heuristic, not a proof of usefulness.

Reserve, for example, 8 of 32 inspection opportunities for diversity/exploration lanes and no more than two per exact JudgmentID in the initial inspection batch. Avoid filling all inspection slots with alternate proofs of the same statement. This is receiver-owned candidate diversity, not per-publisher fairness. A candidate can enter a later separately budgeted inspection batch even if the first batch was full.

Cap any popularity contribution; one proposed local rule counts at most one successful local application per exact candidate judgment per local session, uses a finite observation window, and saturates the score after eight such observations. Imported claims and repeated announcements contribute zero to that score. Sessions are local allocation scopes, not claims about distinct people; an authorized local workload can still pad them. Explicit exact-ID access, alternative lanes, and exploration remain available at score zero.

## Where a client-only recipe is insufficient

A better client cannot recover features the server did not index or candidates an unchanged prefix never exposes. Two optional capabilities are therefore proposed for a later explicitly versioned index service. They do not exist implicitly in frozen ORG1.

### STRUCT2: several bounded, typed views

Keep exact identity tables and the old extractor namespace. Add a candidate-only extractor that records, under separately bounded construction/storage work:

- conclusion-head and application-spine features distinct from telescope features;
- exact practical group/type/constructor/recursor/field selectors and opaque references, not only ordinary constant IDs;
- equality/iff/order-shaped relation features with operand/type-head features, where those forms are syntactically recognized;
- bounded term-pattern features in which local variables can be wildcards while exact constants, binder positions, and universe constraints remain available;
- optional bounded beta/let and selected safe-definition unfolding views, with explicit transparency/fuel limits, provenance to the raw syntax, and partial flags;
- bounded features of antecedents, so a theorem discoverable from an available premise need not share the desired conclusion head.

One starting policy records at most 64 fixed-size feature tokens per descriptor, split into 24 conclusion/relation, 16 interface/type, 16 telescope/antecedent, and 8 residual-sampling tokens. Token hashes are retrieval features only; collisions can add wrong candidates but cannot prove identity or equality. Both full extraction memory/CPU and encoded descriptor size are independently capped, preserving a 4-KiB public projection through bounded token selection. No complete dependency list is squeezed into these tokens.

Choose features from the bounded inspected syntax, not an unbounded expansion of a shared DAG. Reserving conclusion/interface lanes mitigates first-32-prefix bias but does not guarantee complete feature coverage. If the expression is too large or unfolding exhausts its allowance, expose truncation and keep raw keys. Learned formal-syntax embeddings may add another candidate lane under the same authority and cost constraints; they cannot replace exact access or final checking.

### Selected nonprefix operation: FIND_WINDOW

The initial extension is one operation, `FIND_WINDOW`, not a windows-or-sampling menu. Its conceptual request is `[predicate, snapshotSelector, startPosition, pageCeilings]`. The snapshot selector chooses the provider's current authorized public snapshot or an exact still-live previously returned snapshot token. `startPosition` is either `BEGIN` or a caller-chosen exact lexicographic boundary in the ordered public-descriptor-ID namespace. A boundary need not name an existing record. The server seeks the inclusive lower bound in the fixed base posting list selected by that predicate/snapshot/planner.

The remote order uses public descriptor IDs, not private assessment-bearing descriptor IDs. This is a new-profile public index ordering requirement. The operation does not reveal private index entries, counts, or key positions. The same bounded scan, result count, response bytes, CPU, memory, and holder/disclosure checks apply as to the corresponding ordinary page; a seek and its index traversal are charged work.

The reply binds the exact public snapshot, predicate digest, extractor, planner/base-list identity, original lower boundary, and:

1. the lower boundary for this page;
2. the next unprocessed exact public descriptor position, or explicit `END`;
3. the half-open processed interval between those boundaries within the selected source list;
4. returned candidate descriptors and all truncation/budget outcomes;
5. a holder-bound authenticated continuation when unprocessed entries remain.

Only fully handled entries lie in the processed interval. A matching entry that cannot fit the output, or whose test is interrupted, remains the next unprocessed position. Continuations cannot change the predicate, planner, snapshot, or original window start; beginning elsewhere requires a new funded request. A snapshot's original finite lifetime is not extended by starting another window or issuing a continuation.

There is **no implicit wrap** from the upper end to the beginning. `END` means that this named suffix/window scan reached the upper end of its fixed source list, not that entries below the requested start were searched. A caller wishing to inspect the earlier range starts a separate bounded request at `BEGIN`. Even a complete honest suffix says nothing about other snapshots/providers or mathematical relevance outside the predicate. A remote coverage claim remains server-declared.

The client can rotate chosen start keys across separately admitted exploration windows, while retaining bounded interval/duplicate summaries. This is a heuristic against repeated-prefix starvation, not uniform record sampling or guaranteed recall. Uniformly chosen hash-space boundaries can overrepresent records after large gaps. Caller-chosen starts may also systematically miss a relevant cluster. Directed exact/interface queries remain the primary lanes; rotating windows provide another opportunity within explicit resource limits.

A future **distinct** rank-sampling profile could specify a distribution over stored records and pay for the necessary order-statistic/sampling structure. It is not part of initial FIND_WINDOW. Even ideal uniform sampling would not solve low-density relevance: 64 independent samples with one eligible record among 262144 have inclusion probability approximately 0.0244 percent. Better features and collection scopes remain essential.

Frozen clients cannot manufacture a cursor for a different starting position, request recursive forwarding, or assume a server honors FIND_WINDOW. Capability negotiation and new seek/boundary/privacy conformance cases are required before use.

## Collection routes and compatibility guides

The client should prefer contacts advertising exact relevant interface bundles, not merely a generic native profile that almost every provider supports. Locally chosen `CollectionGuide` data can map a finite set of exact interfaces/modules and verified translation endpoints to public candidate providers. Guides remain optional, replicated, bounded, and replaceable; they are neither a compulsory taxonomy nor a global membership authority.

A guide is distributed as the exact typed CollectionGuide data in an explicitly disclosed ADVISORY_READ1 bundle, or imported through its offline equivalent. Its input observations can come from a previous successful exact fetch, public contact bundles, or bounded separately authorized route responses. A reference in a guide is advisory, not a transitive read capability. The receiver independently authorizes and verifies any actual mathematical acquisition and updates service observations from its own calls. Guide expiry or disagreement affects routing confidence, not theorem truth.

Some contact capacity should serve receiver-chosen distinct interface collections and unfamiliar routes instead of a single global popularity ordering. The concrete allocation is a local heuristic; it cannot guarantee coverage of unbounded subjects in a 256-contact directory. Correlated guides, stale specialist contacts, profile forks, and incomplete advertised keys belong in the qualification corpus. The separate CP-001E network analysis owns transport batching and any capability-generation changes; neither removes this discovery requirement.

## Quantified qualification cases

All rows below are proposed future experiments or mathematical countercases, not results already measured.

| Case | Construction | What must be recorded |
|---|---|---|
| Prefix overload within profile | 16384 and 262144 retained judgments share a head/shape bucket; eligible items placed in early, middle, and late positions | Known-eligible inclusion by page/time budget; repeated-prefix starvation; window/feature ablations |
| Missing discriminating symbol | Insert 32 earlier distinct symbols before the relevant reference; separately place it beyond occurrence 4096 | STRUCT1 miss/truncation, STRUCT2 conclusion-lane gain, exact-ID fallback |
| Wrapper mismatch | Define f and a beta/delta-equivalent wrapper g with different IDs, then state parallel lemmas | Raw versus bounded-normalized candidate inclusion; conversion CPU; no identity merging |
| Isomorphic structures | Two checked monoid records with different field order/group IDs | Failure of direct instantiation; successful exact checked adapter when supplied; added closure costs |
| Class metadata absent | Import exact native declarations for a representative class hierarchy with explicit-only binders | Explicit-application success versus ordinary source elaboration; recovered metadata work and bounded instance search |
| Dangerous but valid metadata | True rewrite rules forming a cycle; overlapping/cyclic instance-search hints | Finite elaboration timeout, no auto-executed peer code, no change to native acceptance |
| Contextual mismatch | Candidate has a stronger premise, reordered dependent telescope, or incompatible universe | Correct residuals/unknowns; no missing premise silently discharged |
| Sparse providers | Million-provider synthetic contact model with 100 specialist indexes and controlled correlation | Directory coverage versus queried-peer coverage; collection-guide benefit; no global-completeness claim |
| Duplicate interfaces at scale | Ten and 100 independent encodings, with zero, hub, or selected pairwise checked adapters | Cross-interface application success and full adapter/import cost, not name-match count |
| Padding attack | Checked unused-argument references and many trivial distinct downstream judgments inflate one lemma's edges | Score saturation, effect on rare zero-use candidates, native validity unchanged |
| Expensive closure | A short theorem adds 256 MiB of unique dependencies; a longer alternative adds 64 KiB | Cache-conditional ranking; complete replay cost; no shortest-term assumption |
| Drift and loss | Valid profile upgrade, stale alias view, removed provider, local cache loss, delayed correction | Exact profile isolation, explicit nondecision, recovery cost and actual retained alternatives |

The 256-MiB/64-KiB closure contrast represents a factor of 4096 in incremental payload before metadata. At a sustained 8 MiB/second with no initial burst, idealized payload times are 32 seconds versus about 0.0078125 seconds. NET1-DEFAULT also permits a 16-MiB token-bucket burst: its strict rate-envelope lower bound is instead `max(0, B-16 MiB)/(8 MiB/second)`, giving 30 seconds versus zero from that constraint alone. Physical bandwidth, per-object operations, native checking, and synchronization add their own limits. A warm cache can reverse the marginal comparison. No universal statement-only ranker captures that without environment information.

For index/storage scaling, evaluate bounded local providers up to their declared caps and a federation of increasing numbers of such providers. Do not claim a test at 100 million single-node retained roots conforms to the frozen 262144-root hard limit. If a later archival/index-only profile changes that restriction, qualify it separately rather than borrowing an impossible test configuration.

## Evaluation without an intention or task registry

Build a finite offline evaluation set from existing checked derivations and explicit application witnesses. Each sample consists of a local environment/expression view and one or more already known eligible declaration/application pairs. That fixture is a retrieval test input, not a live public unsolved-mathematics object.

An eligibility witness includes exact profile/interface bindings, the actual argument substitution or rewrite proof, and checked residual-premise witnesses when a completed application is claimed. Without them, label the sample as structural matching only. Timeout or failure to find a witness does not make a candidate a certified negative.

Report at least:

- known-eligible Recall@K within the finite declared gold pool, plus probability of at least one known eligible result within the resource envelope;
- counts of exact hits, tentative matches, completed checked applications, missing premises, incompatible interfaces, and resource nondecisions;
- cold and warm total CPU, wall time, transferred bytes, full/marginal retained bytes, native replay cost, metadata construction, and repair/update cost;
- separate discovery loss, matching loss, acquisition failure, and final-application failure;
- stratified results for exact shared interfaces, harmless wrappers, separate structure encodings, rare subjects, deep statements, and newly introduced profiles;
- exposure of zero-use content and degradation under padding/advertisement floods;
- local expression-query privacy and remote public-scope compliance.

Split evaluations by development/interface cluster and profile version, not only by random theorem rows. Otherwise a query may reveal nearly the same statement or exact supporting interface already present in the ranker's training/cache. Measure library-view installation and model/ranker preparation costs rather than treating them as free. Positive relevance labels may be incomplete: measured recall is against the declared witness pool, not against every useful theorem in mathematics.

Compare exact-only lookup; frozen STRUCT1; client query planning/matching; STRUCT2; the selected FIND_WINDOW operation; and a learned candidate lane under the same end-to-end envelopes. Qualify any later rank-sampling profile separately. A ranker that improves ordering only after candidates are artificially supplied has not solved discovery. A method that returns more useful-looking names but seldom completes checked applications has not qualified reciprocal reuse.

No arbitrary universal utility threshold is proposed here. Before a release claim, operators should predeclare representative workloads, acceptable latency/cost tradeoffs, and minimum known-eligible retrieval/application coverage per important stratum. They should report intervals and regressions. Heuristics may be useful without optimality proofs; they still need evidence that they improve the experience they purport to support.

## Recommended concept decisions before implementation

1. Treat the optional external agent adapter, inert LibraryView/CollectionGuide format, and explicitly bounded ADVISORY_READ1 distribution path as first-class deliverables, not unspecified conveniences left to every agent to reinvent.
2. Preserve exact shared-interface bundles and verified adapter relations as the economical interoperability path; do not promise automatic semantic merging.
3. Keep a frozen-compatible bounded query planner as a baseline, but explicitly qualify its recall and prefix limitations.
4. Develop a separately versioned structural index with practical selector features and the selected FIND_WINDOW nonprefix operation; do not silently extend ORG1 wire semantics or claim it is uniform record sampling.
5. Make contextual matching and verified final application visible in the interface, including residual hypotheses and exact closure costs.
6. Cap popularity and dependency-occurrence signals, preserve bounded exploration/direct access, and test syntactically valid padding rather than assuming dishonest use is detectable by a proof checker.
7. Require representative end-to-end import-and-application evidence before calling the framework practically usable by diverse Lean agents.

The central objective is not a universal ranking oracle. It is a reliable reciprocal path in which an independently investigating agent can often find an affordable exact interface, use checked evidence through a transparent local adapter, and contribute a new independently replayable result. ORG1's safety boundaries are valuable, but achieving that objective requires the missing discovery and client-workflow layer to work in practice.
