# CP-001E: scaling native identities, exact evidence, and incremental reuse

Date: 2026-09-19. Status: selected concept amendment and independent scale analysis; no implementation, benchmark, bootstrap build, or executed native test. CP-001D is frozen and unchanged.

This note audits the representation in [the frozen mathematical contract](../../spec/OPERATIONAL-CORPUS-V1-MATHEMATICS.md). Its conditional safety boundary is retained. Its flat transitive manifests are not an adequate long-term scale choice. The amendment below is one selected design, not a menu and not a claim that a Merkle tree makes arbitrary mathematics cheap.

The frozen v4.22.0 kernel pin is a historical audit target, **not a deployment recommendation**. The parallel [foundation security audit](CP-001E-foundation-security-audit.md) examines subsequently fixed native-kernel issues relevant to raw universe/projection/inductive inputs. This note leaves FoundationID abstract over an explicitly selected and qualified native foundation; efficient replay or a cache hit cannot repair a vulnerable kernel. Source replacement/security qualification must be resolved before any practical release claim, and changes to an affected checker/foundation invalidate the appropriate certificates under the rules below.

## Selected changes

- A new SemanticContext representation commits to the **exact direct semantic references** of a statement. Exact transitive meanings remain recursively committed by the referenced immutable objects. Proof-only dependencies never enter this statement context merely because a proof uses them.
- A new Replay representation commits to its exact typed root and a **canonical persistent JudgmentID-to-ProofID map**. Reachable definitions, groups, and opaque declarations are derived from the native graph, not copied into every replay as a flat transitive list.
- Persistent map/set nodes are ordinary small content-addressed objects with canonical topology. Their shape depends on their entries, not publication order, producer identity, or insertion history.
- A receiver keeps its own immutable native-check certificates, exact dependency interfaces, and optional materialized closure summaries. Current permission, incidents, availability, and protected use are separate guards; a new unrelated contribution does not invalidate every previous native check.
- Foundation identity, representation schema, receiver resource policy, and transport windows are different versioning dimensions. Increasing an operational allowance is not a mathematical identity change or permission to change native rules.

These changes require an explicitly versioned reader/profile amendment. They do not reinterpret the frozen CP-001D records or rewrite its checkpoint.

## Cost model and what is being counted

Fix a cryptographic digest length λ, with λ = 256 in the selected current hash suite. Let L = λ + 40 be the bit length of the fixed key representation below. Let V and E be the numbers of distinct reachable native declaration units and direct dependency edges in one selected replay. A mutually/nested inductive group is one declaration unit. Let B be distinct canonical payload bytes that a receiver must read, and let K(u) be the actual native checking cost of unit u under its selected already checked predecessors.

We distinguish:

- logical manifest size, including repeated references;
- distinct retained CAS bytes after sharing;
- newly transferred bytes at a warm receiver;
- parsing/reference/manifest work;
- actual native kernel work;
- current-reliance and storage-protection work.

One must not count a constant-size root hash as if it supplied the data it commits to. Conversely, one must not charge all old payload bytes again merely because a new root can reach them. Complexity statements below are conditional on collision-resistant binding, qualified decoding/checking, and available receiver-owned caches where stated. They do not prove a bound on K(u), which can be very large even for a short term.

The asymptotics concern growing families or an explicitly enlarged versioned operational envelope. CP-001D already imposes finite declaration-depth/object/byte ceilings. A chain beyond those ceilings is not a CP-001D-admitted example. That ceiling does not repair the representation: it instead prevents indefinite growth along such a chain. The quadratic effect is observable well before the ceiling, and reappears whenever the ceiling is raised.

## Counterexample: short definitions, quadratic transitive manifests

Let d₀ be the checked definition `Nat.zero`, and, for i > 0, let dᵢ be a fresh content-addressed safe definition with type Nat and body the constant dᵢ₋₁. Each new definition has constant-sized native syntax and one direct nonseed dependency. All DefinitionIDs are distinct: their exact bodies reference different predecessor IDs, even though the values are definitionally equal.

For each i, publish the closed judgment

\[
J_i:\quad d_i=d_i
\]

with its reflexivity proof. Checking this equality does not need to normalize the entire d-chain: both sides are the same exact expression. Definitions themselves can be checked from their predecessor's already established type. This family therefore does not hide an inherent need to repeat all earlier arithmetic or proof search.

Under CP-001D, SemanticContext(Jᵢ) explicitly lists d₀ through dᵢ. Its ReplayManifest also explicitly lists all those definitions. These are distinct growing lists, so ordinary whole-object CAS deduplication does not share their repeated prefixes. With N nontrivial stages, each list contributes Θ(N²) total ID occurrences across the published family, although the native declaration graph has Θ(N) vertices and edges and Θ(N) small native terms.

For illustration, ignoring array headers and taking 38 bytes per relevant schema-1 DefinitionID, two copies of prefixes of lengths 1 through N cost

\[
2\cdot38\sum_{i=1}^{N}i=38N(N+1)\text{ bytes}.
\]

At N = 500 this is 9,519,000 bytes, solely for the two repeated ID lists; at N = 1,024 the expression is 39,884,800 bytes, before all other objects. The exact admitted maximum chain is smaller if wrapper/declaration-depth accounting consumes part of the configured limit. These arithmetic figures are representation examples, not measured workloads or promises that every listed N fits a particular admission policy.

This is a valid adversarial workload: the declarations need not supply useful new mathematics. Nevertheless, a representation suitable for untrusted honest-or-mistaken producers must not rely on every producer avoiding such cheap structural repetition.

## Ordinary family: incremental correctness of iterated constructions

The problem does not require gratuitous aliases. Fix checked addition by recursion on its second argument and a checked congruence lemma. Define

\[
k_0=0,\qquad k_{i+1}=\operatorname{succ}(k_i),
\qquad f_0(n)=n,\qquad f_{i+1}(n)=\operatorname{succ}(f_i(n)).
\]

At stage i prove

\[
P_i:\quad\forall n,\ f_i(n)=\operatorname{add}(n,k_i).
\]

P₀ is reflexivity. Pᵢ₊₁ follows from Pᵢ by congruence for successor and one unfolding of the new definitions/addition equation. Each stage has a constant number of direct references and a bounded local proof pattern. The exact statements are distinct, so this is not the same-JudgmentID theorem-alias cycle identified in CP-001D.

The selected proof graph is a lemma chain. Its CP-001D witness map at stage i has Θ(i) entries. Its semantic definitions and replay declaration lists also grow transitively. Publishing all intermediate reusable results gives Θ(N²) list entries although incremental native development has Θ(N) stages. The pattern models ordinary layered correctness developments: a new implementation step imports the previous correctness theorem instead of re-proving the whole history.

An additional simple semantic family is `T₀ := Nat`, `Tᵢ₊₁ := List Tᵢ`, with reflexivity theorems parameterized by Tᵢ. Short native definitions represent genuinely different nested types, but flat transitive meaning lists still copy every earlier layer. No claim is needed that arbitrarily deep nesting is itself useful.

## What cannot be optimized away

### Cold independent checking

A receiver with no locally justified predecessor certificates must establish the selected finite native closure. In general it must obtain and examine every previously unknown reachable declaration/proof body: an unexamined predecessor could contain the one invalid proof, forbidden axiom, or unresolved reference. A sender's root hash or previous acceptance flag supplies no such examination.

Thus cold work is at least proportional to distinct necessary input information, plus native checking cost. Content addressing and persistence avoid repetition; they do not make unknown dependencies valid. A separately specified succinct checking proof could change this trust/cost model, but none is assumed here.

### Incompressible witness choices

Take n distinct judgments, each with two eligible native proofs. A fixed root proof can mention all n judgments, while different replays choose any of the 2ⁿ witness vectors. Across m independently chosen vectors, representing the choices generally requires Ω(mn) bits beyond the fixed shared mathematics. A constant-size hash commits to a vector; it does not let a reader recover it without the vector's information somewhere.

Consequently, no selected representation promises O(1) new bytes for every new ReplayID. Persistent sharing is effective when choices/closures overlap structurally. Arbitrary changes to Θ(n) witness choices can legitimately require Θ(n) changed leaves and associated indexing work. Exact-ID deduplication is not semantic proof minimization.

### Real computation and large new terms

A small new root can require expensive native conversion or large auxiliary data; K(u) is not bounded by its count of direct references. A large theorem can have genuinely many direct premises. Kernel work, new information, and required dependency acquisition remain charged. This amendment removes repeated bookkeeping; it does not promise an optimal prover or a proof that useful discovery grows exponentially.

## Canonical persistent keyed nodes

The selected common data structure is a binary **Patricia trie** over fixed-length exact content keys. This means a compressed binary trie whose branches occur only at the first differing bit of the keys below them. It is not a history-shaped balanced tree.

For the current suite, encode a ContentID as a 37-byte lookup key:

`u8(algorithm) || u16be(type) || u16be(schema) || digest32`.

This key representation is injective over the selected ContentID domain and has L = 296 bits. Ordering is unsigned bytewise ordering of these key bytes. It is not an extra hash of the content ID. Node ContentIDs still use the common typed/domain-separated CAS commitment to canonical payload bytes.

Reserve proposed mathematical node kinds `0x0020` for direct-reference sets and `0x0021` for witness maps. These are CP-001E proposed allocations, not changes to the frozen registry. Both use schema 1 and the existing definite-array/uint/byte-string CBOR subset.

| Node | Reference-set payload | Witness-map payload |
|---|---|---|
| Empty root | `[2]` | `[2]` |
| Leaf | `[0,keyBytes]` | `[0,keyBytes,ProofID]` |
| Branch | `[1,splitBit,prefixBytes,leftNodeID,rightNodeID]` | Same fields, with witness-node child IDs |

For a branch, splitBit is the first differing bit among its descendant keys, counted from zero at the most significant bit. Its prefix has exactly splitBit bits, packed in the minimum number of bytes; unused low bits are zero. All keys in both children share this prefix. The left child's keys have zero at splitBit, the right child's keys have one there. Both children are nonempty; unary branches and duplicate keys are forbidden. Child branches split strictly later. A leaf key has its fixed exact length and permitted content kind. A witness key must decode to JudgmentID and its value must decode to ProofID; subsequent native checking verifies that the proof actually names that judgment.

Every node is bounded to 256 canonical bytes in this suite. The selected fields fit that envelope; future larger ID suites require an explicit node-schema decision rather than silent truncation. A node may be transported alone or within a bounded network bundle. A transport bundle is not part of the node's identity.

The verifier validates child types, prefixes, ordering, actual subtree boundaries, and node hashes. Locally cached subtree summaries may include exact minimum/maximum key and leaf count, but an unverified publisher count is not an authority or a completeness argument. Missing children are nondecision, not empty branches.

### Canonicality and persistence claims

**Unique representation.** A finite nonempty map has either one key, hence its unique leaf, or at least two keys. The first bit where its keys differ is uniquely determined, as are its zero/one partitions. Induction over partition size gives one branch tree and one root commitment, conditional on content binding. The empty map has its distinguished root. Consequently identical maps built by different agents or insertion orders have identical roots.

**Bounded path copy.** A lookup, insertion, deletion, or value replacement follows at most L branch positions. Updating k entries can use at most O(kL) newly created nodes; unchanged subtrees retain their exact IDs. The worst-case bound is O(L), not an unproved expected O(log n) claim about publisher-chosen keys. For n leaves a fully materialized nonempty Patricia trie has n leaves and n−1 branches.

Local and transported page-count work is separate from native dependency depth. An L-deep trie over one lookup key is not an L-step theorem chain. Conflating them would reintroduce an accidental semantic scale cap.

## Native-width interpretation is a schema rule, not a resource heuristic

Separating operational limits from FoundationID does not permit machine-integer truncation. A wire uint64 must never silently become a different native unsigned integer, array offset, projection selector, or binder index. The parallel foundation audit identified native-width conversion hazards as well as corrected historical kernel bugs. The selected Native2 adapter contract therefore includes the following fixed representation/ABI rules.

| Input or derived value | Required exact conversion and semantic check |
|---|---|
| ContentID algorithm/type/schema and node tags | Check each declared fixed range before construction; no modulo narrowing into u8/u16/tag enums |
| Native projection field index | Require 0 ≤ index ≤ 2³²−1 before constructing Expr.proj, and check the exact field bound against the qualified reconstructed one-constructor structure interface; a huge index cannot wrap to field zero |
| de Bruijn/native binder indexes, native inductive parameter counts, and other fields consumed as C++ unsigned | Require u32 representability and the actual scope/arity constraints; generated counts receive the same checks, not only directly supplied fields |
| Native expression/universe arrays and native declaration/member lists | Length must fit the actual container index/length API and every narrower native consumer used by the qualified adapter; the selected unsigned-count interface caps such counts at 2³²−1 independently of lower local memory limits |
| DAG node indexes, universe parameter indexes, group/type/constructor/recursor selectors | Check against the actual referenced collection/arity and its qualified native index type before conversion; value-preserving round-trip is required |
| Byte lengths, offsets, allocation sizes, and calculated products/sums | Use checked wide arithmetic; establish offset+length ≤ actual enclosing length without overflow and verify allocation/stream/container range before conversion; separately enforce local byte/memory authority |
| Natural-number literal mathematical value | Decode losslessly to native arbitrary-precision Nat; do not apply the u32 index restriction to ordinary mathematical values and do not silently convert those values to machine indexes |

Each call across the adapter/native boundary must identify the callee's exact integer type and establish both representability and the relevant semantic bound. The u32 limit is the selected conservative ceiling for the native unsigned interfaces, not an assumption that all host size_t values are u32. The checker-image/adapter qualification records the actual ABI widths and supported runtime. An unsupported host ABI or an unaccounted narrowing path prevents activation; it is not permission to run the same input under host-dependent meanings. Fixed machine-width requirements belong to the interpretation/encoding contract even when a receiver raises resource allowances below them.

The protocol can carry a mathematically large natural value. That does not imply every pinned kernel arithmetic routine handles every such value robustly. For example, merely filtering a large literal at the surface does not bound a shift count that an otherwise short term computes during native reduction. A known dangerous native operation requires a separately qualified containment/fix or an explicit supported-operation restriction, not a claim that a small wire object is computationally safe.

Native checking remains isolated, with finite memory/CPU supervision. An execution failure, unsupported internal bound, or supervisor stop supplies no mathematical acceptance and no proof that the submitted proposition is false. The mathematical outcome is nondecision such as UNKNOWN(NATIVE_EXECUTION_FAILED/UNSUPPORTED_NATIVE_RANGE); an unexpected runtime crash also records its diagnostic ERROR/incident under the local operational contract. A completed range violation of the selected external schema can reject schema conformance, but not refute the theorem. No success flag is synthesized from a partial native run.

## SemanticContext2: direct meanings, exact transitive binding

The proposed schema-2 payload is

`[FoundationID,directSemanticRefSetRoot]`.

The exact root set is recomputed from constant references **syntactically present in the judgment's telescope types and conclusion**, after the existing canonical term rules. A definition reference contributes that DefinitionID, a theorem-constant reference contributes that JudgmentID, a group member contributes its GroupID, and an opaque constant contributes its OpaqueID. Member selectors and universe instantiations remain in the exact terms; dropping them from this set does not remove them from judgment identity. Seed references are bound by the foundation and do not become public independent declarations.

Crucially, this direct set does not include references encountered only inside the selected proof or its auxiliary lemmas. Those affect replay evidence and footprint, not the statement's direct semantic context. A publisher cannot add a convenient arbitrary context object: the receiver compares the canonical set obtained from the exact statement terms against the submitted root.

Transitive interpretation follows the exact referenced objects:

- definitions contribute their checked exact types and bodies;
- judgments contribute their exact statement contexts/conclusions, not a proof choice;
- groups contribute their exact descriptors and derived native member interface;
- opaque declarations contribute their exact types/bodies according to the adopted conservative footprint rule.

The meaning graph is still checked for forbidden cycles and missing data. Group-local inductive recursion remains the existing explicit native rule, not a cross-object hash recursion. An isolated judgment remains an inert descriptor, not an accepted theorem.

**Binding argument.** Fix the direct root refs and all qualified decoding/native rules. Every next reachable object is named by an exact content identifier in a previously committed object. Induct along the finite acyclic meaning graph. Changing any referenced type, body, group, or context changes some reached object bytes/ID and therefore changes a predecessor reference, absent a content-binding failure. Listing every descendant again in the outer context supplies no additional binding. Direct-set equality eliminates extra or omitted direct roots; exact graph traversal determines the least transitive meaning closure.

This changes the canonical context representation and hence the IDs of contexts/judgments newly represented that way. It is not a claim that old and new context payloads hash identically. It remains source-neutral: private goals, source aliases, authors, import history, and chosen theorem witnesses do not choose the direct set or its trie shape.

## Replay2: exact witness map, derived declaration closure

The proposed schema-2 payload is

`[FoundationID,typedRoot,witnessMapRoot]`.

The typed root retains tags 0 ProofID, 1 DefinitionID, 2 GroupID, and 3 OpaqueID. The map W selects exactly one proof for each needed JudgmentID. For a proof root p with judgment j, W(j) must equal p. A construction/group root has no invented judgment. There is no extra flat declaration list.

Define `Reach(root,W)` by the following finite traversal, not by a publisher's claimed node count:

1. Decode the exact root declaration/proof, statement terms, and native expressions.
2. Follow every actual nonseed definition/group/opaque reference to its exact declaration. Traverse all relevant types/bodies/constructors and qualified generated native interfaces under the existing footprint rules.
3. On a theorem reference j, follow its exact statement and the unique selected proof W(j). Check that this proof names j, and traverse its proof term and statement. The proof root also counts as a selected judgment/witness.
4. Detect selected support cycles before any ungrounded native insertion. Process each reached unit once for this traversal; repeated references are not repeated declarations.

Let `NeededJudgments(root,W)` be the exact set found by that traversal. Acceptance requires

\[
\operatorname{dom}(W)=\operatorname{NeededJudgments}(root,W),
\]

with every selected proof/declaration independently justified under the stated local checking rules. Missing W entries, invalid proof-to-judgment associations, and selected cycles reject the claimed replay when the relevant data are available. Missing trie/object data yield nondecision. An extra map entry is not an innocent undeclared import: it violates exactness and is rejected.

A concrete equality check builds the canonical expected map while traversing selected native references and compares its root with witnessMapRoot. This checks both missing and extra entries without relying on a leaf count or a probabilistic filter. The traversal derives the declaration closure; there is no independently supplied declaration list whose omission could erase a required body.

The physical package can contain cached or out-of-band irrelevant bytes, but they do not enter the replay's mathematical environment, authorized disclosure scope, or retention obligations merely by arriving together. The native closure consists of the root, exact map/set nodes, and exactly reached mathematical payloads under the schema rules. A provider's unrelated cache is not the artifact's closure.

### Network implications

Trie nodes are ordinary typed immutable objects. A receiver can request the next hash-verified frontier under one admitted root-bound transfer, rather than demanding a giant upfront list. Every expansion is derived from an already bounded/verified payload; its bytes, discovered object count, queues, and subsequent requests remain within locally authorized staging bounds. A declared root does not authorize unlimited graph exploration.

For public serving, the provider has already validated the exact replay and authorizes only its selected closure or its finite audience export. For unvalidated incoming material, staged frontier exploration is a receiver-owned finite activity, not inherited mathematical authority. In either case, map pages, native terms, and byte-storage chunks keep different IDs/roles.

Auxiliary child-replay hints, local cache certificates, negative-relation annotations, and local/offline Module wrappers do not automatically become members of the root's public read scope. No generic CAS-read capability is introduced. The companion network amendment owns bundle/window mechanics; this note specifies the exact commitment they must preserve.

## Cold verification without quadratic preprocessing

A cold verifier need not first materialize the transitive witness set for every interior declaration. It can verify one requested root by a bounded depth-first traversal with a visited set, an active-stack cycle check, and native topological insertion. Exact direct-ref extraction is memoized by the actual object/decoder key. Every reached theorem inserts its selected pair into one expected-map builder. Every judgment's direct semantic set is checked from that judgment's own terms.

Ignoring native kernel internals, one root can thereby be checked using O(B + (V+E)L) parsing/reference/map work, plus the cost of validating its received trie nodes and

\[
\sum_{u\in\operatorname{Reach}(root,W)}K(u).
\]

Dictionary implementations, term sharing, and storage faults affect constants and actual resource cost; the expression is a paper operation bound, not a benchmark. An implementation that additionally materializes all interior transitive summaries must account for that work separately. Such summaries are optional local optimizations, not a mandatory quadratic precondition for accepting one root.

## Warm incremental native certificates

The native acceptance cache is receiver-owned evidence, not a copied remote verdict. For a selected unit/root v and its exact selected reachable witness map Wᵥ, use a key of the form

\[
\operatorname{CheckKey}(v)=
(\operatorname{typedRoot}(v),\operatorname{Root}(W_v),
\operatorname{FoundationID},\operatorname{CheckerImageID},
\operatorname{DecoderAdapterID},\operatorname{InterpretationViewID},
\operatorname{SemanticOptionsID}).
\]

The associated immutable certificate records exact direct dependencies, the resulting checked native interface, the actual syntactic axiom/rule footprint, checked generated group members where applicable, and the local native environment/selection commitment needed for safe reuse. InterpretationViewID binds the exact locally qualified legacy/same-foundation reader view, including the versioned mapping used; a different interpretation table cannot inherit a certificate merely because the executable adapter is unchanged. CheckerImageID/DecoderAdapterID qualification also fixes the supported native ABI and the exact range-conversion rules above. An ACCEPT certificate is retained only under local integrity/recovery controls. The selected baseline requires compatible uniform checker/adapter semantics throughout reused certificates; heterogeneous checker compositions need a later explicit contract.

Resource budgets are recorded as operational evidence of the completed attempt, not needlessly included as semantic input to every successful check. A later larger budget cannot turn UNKNOWN into a reusable ACCEPT certificate by changing a key. Native rejection, policy rejection, missing data, and resource nondecision remain different outcomes. A changed decoder, native interpretation, checker image, or relevant semantic option requires the corresponding new key/qualification.

### Exact warm assembly rule

For each direct native dependency of a new unit v, obtain a local child certificate for the exact selected declaration or selected proof, with map Wc. For theorem reference j the chosen child proof must be W(j). Existing child certificates can be proposed by hints, but neither the hints nor their provenance are authoritative.

Compute the compatible union

\[
W_v=\bigcup_c W_c\ \cup\
\begin{cases}
\{j\mapsto p\}, & v\text{ is proof }p\text{ of }j,\\
\varnothing, & \text{otherwise}.
\end{cases}
\]

Equal-key unequal-value conflicts reject that assembly. Compare the canonical union root with the candidate's exact witness-map root. Then check the new native declaration against a receiver-created compatible checked environment. A producer can instead supply a different consistent witness selection or expand an earlier theorem alias as in CP-001D; it cannot ignore a union conflict.

The compatibility requirement includes overlapping theorem assignments in the native environment. Reusing an environment with j installed from an incompatible selected witness is not silently justified by the fact that its printed theorem type looks the same. The selected baseline forks/uses a compatible persistent native environment or reconstructs one under the exact local certificates. On the ordinary extension chain, the preceding environment can be reused and the new declaration inserted once. General branch joins can cost more; no constant-cost arbitrary environment merge is assumed.

**Exactness and grounding argument.** Child certificates already establish complete acyclic selected closures. Native parsing identifies all and only direct dependencies of v. Compatible map union therefore contains every transitive selected judgment needed by those dependencies and no unrelated entry. The root singleton accounts for a proof root. Equality with the candidate map rules out both extra and missing choices. A cycle involving v is rejected by the active-stack/grounding check. More generally, compatible unions of complete child closures cannot hide a new internal cycle: following an edge in a child closure must remain in that complete closure with the same selected witnesses. No theorem type is installed as an axiom.

Persistent trie union can reuse identical subtree IDs and skip disjoint key ranges. Its actual cost is the number of distinct node-pair interactions it must inspect plus new result nodes; it is not universally O(number of newly named root declarations). A conflicting or radically different witness selection may force substantial work. Identical compatible child maps and chain-prefix updates are the intended efficient cases.

### Chain bound

For the iterative correctness family, suppose each previous selected root/certificate/environment remains locally available, the new stage has O(1) direct dependencies, and its witness choices extend the previous map by O(1) entries. Then each new replay creates O(L) map nodes and a constant-sized root. Each direct semantic context has O(1) refs. Across N stages, repeated manifest material is O(NL) small nodes rather than Θ(N²) flat ID entries; only the newly introduced native units need fresh native checking.

The total warm cost is consequently

\[
O(NL)+\sum_{i=1}^{N}K(\text{new units at }i)
\]

for these representation/checking components, plus actual transfer, storage, and local guard costs. This is conditional amortization for the specified family, not a universal graph theorem. Independent cold replicas still each pay their own first validation cost. A node that evicts its prior certificates or bytes may legitimately pay again.

## Current reliance without global-epoch cache collapse

A successful native certificate and a currently authorized protected use are not the same fact. Changing a local index score, admitting unrelated exact content, or adding a new valid descendant does not change the immutable inputs of a previous native check. Such events must not force its kernel work to repeat.

CP-001D's global final-epoch-equality rule can also cause needless retries even if native caches survive. In an idealized countermodel, irrelevant commits arrive as a Poisson process of rate a, evaluation takes fixed time T, and fresh attempts inspect independent intervals. A whole-epoch equality check succeeds with probability exp(−aT), so the mean attempt count is exp(aT). At a = 100/s and T = 0.05s, it is about 148.4 attempts, although the selected mathematical basis never changed. This is an illustrative liveness/cost countermodel, not a measured arrival model or a universal performance law.

The selected amendment keeps a local global epoch as an **observation label**, but uses **relevant guards** for current-use commitment:

1. Capture an immutable state view and identify the exact root/replay certificate, locally adopted checker/profile/interpretation-view/policy guards, and exact closure-protection handle/generation.
2. Establish that no active applicable incident blocks this selected support. An exact derived support-ID set may be materialized locally as a persistent trie. It includes **every binding-relevant object in the exact native closure**: the Replay/root objects, selected ProofIDs, judgments, definitions/groups/opaque bodies, native term objects, direct-reference set pages, witness-map pages, and foundation/profile/bootstrap/rule objects. It is not merely a list of theorem or declaration IDs; a relevant collision/decoder incident on a trie page must not be falsely cleared. Checker/profile-wide incidents and locally trusted adapter/certificate-store integrity have their own guards. The local summary does not include itself in its own mathematical content set; uncertainty in the summary's integrity prevents use of that summary. Approximate membership structures may reject candidates conservatively but must not supply a false-negative clearance.
3. Before committing the positive observation/use pin, the authoritative writer checks the relevant policy/checker generations, current protection generation and expiry, and incident coverage from the captured view through this commit.
4. If the incident journal is complete over that interval, newly added exact incident keys may be checked for disjointness from the exact support summary. Unrelated additions need not force a retry. If coverage is missing, the service must re-establish clearance from a complete current incident view within budget or return UNKNOWN; absence of a remembered event is not clearance.
5. A broad or unresolved incident whose affected scope cannot safely be narrowed trips a global conservative breaker before background work. It invalidates the relevant positive guards immediately. An expensive descendants traversal is not required before refusing stale use.

If these checks pass, the returned observation is linearized at the final writer boundary and labeled by that boundary's actual epoch. It is not falsely described as current merely because an older snapshot was once good. Byte-expiry and real loss are checked even if no policy epoch changed. An unrelated epoch increment is no longer a rejection condition by itself. Lost-response and later-reader freshness qualifications from CP-001D remain.

The journal/delta shortcut is finite and receiver-funded. A slow reader that outlives retained change coverage falls back or gets UNKNOWN. The writer must not perform an unbounded incident scan under its commit lock: expensive clearance work occurs against immutable roots, and the final bounded revalidation covers intervening relevant changes. Under sustained genuinely relevant changes, retry/nondecision is legitimate; this amendment does not promise wait-free positive status.

### Incident cost and cached support summaries

For a root with an already materialized exact support trie and k new exact incident keys, a direct disjointness check costs O(kL), independent of total closure size. Equality of unchanged trie roots and memoized verified subtree intersections can provide further sharing. A cache can also retain a clearance certificate keyed by exact support and active-incident roots. Large incident sets or very different closures can still require substantial bounded work.

The support summary is **local derived cache state**, not an additional public transitive manifest required in every theorem identity. It is built from fully checked direct dependencies and memoized child summaries where useful, with the current root's exact representation-node frontier included and obsolete/unreachable child-replay wrappers excluded. Retaining every such summary for every possible root is not mandated; a node can limit them to active/likely reused roots. In the extension-chain workload they share persistently. Updating a second persistent inventory/support map for O(L) changed native map nodes can cost O(L²) path-copy work, in addition to the O(L) native witness-map update; this does not become a free constant-size inventory operation. For difficult DAGs a node may use bounded traversal or decline to materialize the summary; it must report the resulting cost/nondecision rather than assume an O(1) oracle.

A known checker-image incident can invalidate all certificates made by that image. Revalidation with a new image may genuinely require rechecking the affected retained graph. This is necessary changed trust, not removable manifest overhead. By contrast, losing and refetching identical hash-verified bytes need not by itself rerun a still-trusted historical native check; it changes availability and protection guards.

## Protecting warm closure bytes without repinning every leaf

A successful current use still requires the selected complete local native closure. This amendment does not replace that requirement with a remote promise. It avoids repeatedly enumerating a protected unchanged closure just to add another use pin.

The selected local storage design can represent protected roots over the exact typed CAS dependency DAG. Root ownership and parent-edge reference counts are locally authorized state. Adding a root that reaches an already protected shared subtree increments its owned reference; it does not recursively add another independent count at every descendant. New nodes register their exact child edges when entering protected state; propagation through descendants is needed only on unprotected-to-protected transitions. Releasing the last owner propagates in the reverse direction under the existing generation/deletion fence.

For persistent chain extensions, the new root/map/term nodes are O(L) plus the genuinely new native objects; old shared subtrees are already protected. A new finite use pin over an already protected exact root can retain that root handle without traversing all old leaves. The authorization, deadline, generation, actual availability, and incident guards must still pass. A root whose protection ended cannot revive an old positive handle merely by presenting its hash.

This is a local DAG-ownership accounting argument, not a requirement that peers keep a global ledger. Cold acquisition of a previously unprotected closure still has to establish every new object's availability and protection. Last-owner deletion can touch a large subgraph and must be separately budgeted. Unexpected physical loss bypasses logical reference counts and must publish an availability fault/conservative breaker before positive reliance resumes. Exact current-use bytes and export pins remain subject to the qualified storage/recovery implementation.

## Versioning, operational limits, and interoperability

### Four different identities

| Dimension | Selected commitment | Effect of change |
|---|---|---|
| FoundationID | Exact pinned native semantics, admitted axiom/rule basis, bootstrap inventory and reserved-name interpretation | New foundation; no silent theorem reinterpretation |
| Object type/schema | Canonical representation and exact node/reference interpretation | New IDs for bytes actually represented differently |
| Receiver resource policy | Object/closure/session budgets, memory/depth/CPU allowances, retention and cache quotas | New local operational decision; no rewrite of unchanged mathematical bytes |
| Transport profile/window | Batching, finite offers, chunk/window sizes, transfer deadlines | New transport behavior/authorization, not a new theorem or definition |

CP-001D's LogicProfile includes syntaxLimits; changing those immutable fields changes all profile-bound IDs. That is a real fragmentation cost. CP-001E therefore selects a foundation commitment without operational size/depth limits. Its proposed schema-2 payload is `[nativeFamilyTag,kernelSourceCommit,SeedProfileID,nativeRulesProfileID,reservedNameInterpretationID]`, with nativeFamilyTag 0 for the selected Lean foundation and the latter interpretation/rule records locally fixed and content-addressed. They describe the exact native constructors, rules, allowed foundation assumptions, and naming interpretation, not one receiver's budget. Canonical integer widths, node forms, and parsing rules remain fixed by object schemas; they cannot be changed by raising a budget. Permitting a previously unsupported axiom, reduction rule, executable primitive, or new native interpretation is not a resource increase.

Representation-valid but over-budget objects return a scoped resource/admission nondecision under the new policy, not a claim of mathematical invalidity. Structurally invalid encodings remain invalid. Increasing maxExprNodes or a closure/window allowance within the fixed representation's ranges does not reassign existing TermID/DefinitionID/JudgmentID. No source document claims that arbitrary huge inputs must be processed without local authorization.

### Selected migration boundary

The frozen CP-001D schema-1 records retain their exact identities and original interpretation. Schema-2 direct contexts and replay roots are new objects. An existing statement re-encoded into a direct context normally has a new ContextID/JudgmentID; the two can coexist with an explicit representation mapping and independent checking. There is no mutable alias called latest.

To avoid reissuing unchanged native terms/definitions solely for operational evolution, the new reader may reuse legacy objects by exact ID under a **locally qualified same-foundation view**. Such a view is permitted only when it mechanically matches the exact pinned native kernel semantics, bootstrap/seed export inventory, reserved-name interpretation, and admitted axioms/rules. It does not compare pretty-printed types or accept a publisher's equivalence claim. The old object is first interpreted/validated under its own frozen schema and original limits; the view then identifies its unchanged mathematical foundation with the new separated FoundationID. New schema-2 objects may explicitly reference that exact legacy declaration ID under this qualified view. Native generated names continue to bind actual content IDs, so two different definitions are not renamed into one constant.

This is a representation-reader compatibility rule for the same pinned foundation, not cross-foundation theorem transport. If any native meaning, kernel source commitment, admitted native rule, or seed mapping differs, the view is unavailable; use separate re-export/replay under a genuinely new profile with explicit evidence where needed. In particular, a security-corrected kernel commit cannot inherit an affected old ACCEPT through this same-foundation shortcut merely because axiom names and type signatures agree. A legacy object that violates its original schema is not rehabilitated by a larger new resource policy. New larger objects use the new schema/admission semantics. If the same-foundation view has not been qualified, a deployment must keep the readers separate and perform explicit re-export rather than silently accept mixed closure.

Once the separation is adopted, future changes merely to batching, resource budgets, or locally selected cache limits do not force reserialization of unchanged mathematics. This removes repeated cap-induced identity churn; it does not pretend the one-time change from a flat context record to a direct-context record preserves its hash.

## Selected bounds and remaining qualification

The new representation fixes key/node grammar and the 256-byte trie-node envelope. It does **not** retain CP-001D's network-hard 65,536-object/8-GiB limit as a universal upper bound on all mathematical closures. Each admitted attempt still has finite total discovered-object/byte/work allowances, plus bounded active transfer windows and staging. A larger retained collection or later admitted incremental operation does not mean an infinite single request. Whether a receiver can service a particular large closure is an explicit local capacity question.

The distinct counts are: native declaration depth; native term DAG depth; trie lookup depth; mathematical closure cardinality; distinct retained CAS objects; and one transfer window's objects/bytes. Raising one does not silently raise the others. Continuation must preserve the same immutable root and checked progress state; restarting a grant cannot forget charged work or create an infinite free fetch.

The following obligations remain concrete and unresolved by paper reasoning alone:

- qualify the canonical trie codec, fixed key encoding, duplicate/prefix validation, and structural-sharing bounds;
- audit every native integer conversion and generated count against the fixed range/ABI contract, including projection indexes and computed native arithmetic failures;
- qualify direct semantic-reference extraction separately from proof/replay reference extraction, especially native group-generated members;
- establish native cache/environment reuse correspondence for the pinned Lean implementation, including incompatible alternative witness maps and safe environment branching;
- qualify same-foundation legacy-reader views and source-neutral generated-name behavior without a hidden reinterpretation path;
- qualify current incident/support guards, journal-coverage failure, broad breakers, expiry, and final linearization under concurrency/crash;
- qualify DAG ownership/reference-count transitions, generation fencing, corruption detection, and funded last-owner collection;
- select measured cache/support-summary quotas and fairness policies for difficult graph shapes; no universal best setting is claimed;
- integrate the proposed new type/schema allocations and root-bound page/bundle authorization with the network amendment before freezing CP-001E.

These are not unchosen architectural alternatives: the direct-context/persistent-witness design is selected. They are the conditions required to claim its intended implementation and performance properties. Native proof soundness, preservation over unbounded physical time, and empirical usefulness retain their separate assumptions.

## Review conclusion

Flat transitive context and replay lists can turn a linear stream of short incremental mathematics into quadratic aggregate metadata. Native whole-closure replay and whole-global-epoch invalidation can independently recreate quadratic or retry-amplified work if their local caches/guards are underspecified.

The selected amendment removes redundant transitive meaning/declaration lists, shares exact witness selections persistently, checks native increments against receiver-owned predecessor certificates, and separates current relevant guards from unrelated global activity. It gives explicit improvements for growing extension chains while retaining cold-checking and changing-witness lower bounds. It is a scale-conscious mathematical exchange concept, not evidence of a implemented fast verifier or guaranteed exponential useful knowledge growth.
