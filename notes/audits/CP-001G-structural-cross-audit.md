# CP-001G independent integration audit: structural discovery

Date: 2026-09-20. Auditor: root, independently of the STRUCT2 author. Scope: specification review, finite paper arguments and cross-contract inspection. No implementation, simulation, Lean execution, exporter run or retrieval benchmark.

## Reviewed cuts and verdict

Read the [STRUCT2/FULL_FEATURE note](../analyses/CP-001G-structural-retrieval.md) in full at its first saved cut, then reread the changed deterministic extraction, emission, query lifting and negotiated-provider/group sections. The final reviewed cut is:

`28A766D3DC505DE72032121024535A75B7D7BDBB49E435E47B636532165A55AC`.

The [profile/consumer bindings](../analyses/CP-001G-profile-and-consumer-bindings.md) were authored by this auditor and are being independently reviewed by another collaborator; this note does not portray self-review of those bindings as independent verification. The author's Lean DiscrTree/LibrarySearch source observations are attributed to that source investigation; the root did not independently reproduce the entire upstream inspection.

Within this review, no unresolved contradiction remains in the selected structural extraction/query/coverage contracts. Concrete earlier defects and ambiguities were repaired below. This is not proof of acceptable recall or performance, and it does not qualify the native checker or actual extractor implementation.

## Finding S-LIFT: a compatible candidate can be unreachable

The original proposal used role-specific keys but did not completely specify how a local desired expression queries a different candidate view. Let the query be `Q(y)` and a stored theorem be `P(x) ↔ Q(x)`, with an informative exact head for Q. The query's terminal-head feature has role 0. The stored Q operand has an Iff-side role and relation-side token. Those bytes, and therefore ordinarily their hashes, differ.

Allowing a pattern matcher to inspect Iff sides is insufficient if the preceding posting lookup never reaches that row. This is a deterministic feature-generation countercase, not an assertion about malicious providers or weak models.

**Repair inspected:** the exact query-lifting table now supplies `[1,1,0,head(Q)]` and `[1,1,1,head(Q)]`, the same payloads the stored Iff sides emit. It compares the Q pattern to the selected side, not a fabricated whole Iff expression. Related Eq-side lifting supports rewriting either direction. Explicit reserved query slots prevent a token-rich ordinary goal from automatically consuming every direction slot. Different side roles are not accidentally conjoined into a predicate requiring one candidate view to be both sides.

For a reversed whole relation, the client also reverses the comparison pattern rather than only its head-pair token. A final native implication/symmetry/transport term is still needed. Finding a Q side of an Iff never proves Q without its actual other-side premise.

The repair establishes a concrete route in the untruncated example with live supplied postings and successful scan/import. It does not promise that every theorem survives finite extraction or that all general lemmas have informative rigid heads.

## Finding S-DETERMINISM: caching cannot change extractor output

The first draft fixed a total visit budget but left too much of its charge order implicit. If one implementation charges a shared node once while another charges every occurrence, a later informative constant may be inside one implementation's prefix and outside another's. Normalizing a large focus before or after raw operand inspection can produce a similar difference.

**Repair inspected:** the note now defines a virtual occurrence-level READ, charges repeated/cache-hit reads, fixes raw-before-normalized phase order, fixes expression child order, and makes substitution/shift visits and constructed occurrences explicit. A failed final normal-form search produces no completed companion. Hardware interruption is NOT_EXTRACTED, not an allegedly deterministic shorter token set.

The descriptor, token and pattern semantics consequently depend on the abstract input computation and fixed limits, not processor speed, hash-consing luck or scheduling. Runtime work remains separately charged. The logical bounds do not make canonical decoding of an enormous input free.

This is a specified reference computation, not an executed proof that a future implementation conforms to it. The profile's deliberately repeated spine reads may be inefficient; that is a measurable engineering choice rather than an undefined meaning.

## Typed patterns and native applicability

The pattern grammar retains exact semantic constant/group/projection selectors and internal bound-variable indexes. External parameters become wildcards. Wildcards do not preserve equalities between repeated source variables; literal buckets and erased universes deliberately admit false positives. CUT also matches arbitrary omitted syntax.

Therefore `Compatible` is a relation on bounded projections, not a type-correct substitution, native definitional equality or proof of applicability. The note preserves that boundary throughout its query results. A failed full proof import cannot be repaired by a positive token or pattern match.

The 128-node occurrence-tree bound is applied before pattern DAG sharing, so large repeated term structure cannot evade it by presenting a small storage DAG. The explicit native/projection selectors are permitted syntax in a query, not authority for a provider to fetch an unknown declaration or install it.

The defined BINDER_DOMAIN mode may retrieve a target through one of its head tokens even though only the final domain has a stored full pattern. With a required pattern, that can become a deliberate recall loss; token-only retrieval and later native inspection remain separate options. The specification must not call that loss a semantic exclusion. The selected wording does not do so.

## Functions and constructors are part of reuse

Indexing only theorem conclusions would leave BRIDGE1 unable to find ordinary `f : B → A` constructions without already knowing their names/IDs. STRUCT2 now also selects safe definitions, checked opaque definitions and exact generated constructors, with input/output and domain-head tokens derived from actual checked types.

The constructor has a group-root replay, not an invented standalone declaration/replay. An opaque function needs its body checked and retained even though indexing looks at its type. An apparently suitable `Π b:B, A(b)` remains a dependent candidate, not automatically a nondependent graph edge. Final instantiation/checking preserves these distinctions.

This is enough to specify a useful map-discovery lane. It is not a universal interface-matching algorithm, and no shared English name identifies nominal groups.

## Finite feature coverage and its cost

At most 32 selected tokens per target and at most 128 initial targets give at most 4096 distinct union tokens before any beneficial cross-target deduplication. A provider/key ad can serve all its matching local targets, but each selected distinct key still needs actual publication storage, placements, leases and reader work. Four selected replicas can therefore require up to 16384 selected key-copy memberships for this initial scope, before transient/replacement/ancestor-marker state.

FULL_FEATURE explicitly covers the emitted token union of the selected finite target scope. It does not cover every useful fact about a target, every local root, or an arbitrarily large library. A failed target extraction makes that scope incomplete; silently dropping the target is not a complete original scope. The note inherits separately counted transient/empty/retiring group stock and funded placement/renewal limits, not only the optimistic settled-copy count.

One provider's separate advertisements for A and B do not prove that any one theorem has both features. The subsequent provider predicate performs that conjunction. Conversely, absence from a scanned scope does not prove global absence. These facts prevent a routing membership from becoming a semantic completeness certificate.

## Wire integration repair

During concurrent drafting, two meanings were briefly assigned to ProviderAd `0x8022/2`: a K4-only/direct-structural-anchor record and a code-4 all-key record using a public root descriptor. The independent profile auditor identified that exact same-schema disagreement. It has been removed.

The final STRUCT2 cut uses the integrated chain:

`ProviderAd2 → PublicIndexDescriptor3 → StructuralDescriptor1`.

The root and structural records bind the same InstanceReplay; K4 binds the exact foundation/extractor/token. The routing holder checks bounded codecs/signatures and local authority without fetching the anchor or adopting its foundation. Native acceptance remains at the receiver using complete evidence.

Mode-6 pages carry StructuralDescriptor records in their own ID order; exact-judgment pages carry PublicIndexDescriptor3. Their cursor/snapshot context binds that record universe. FULL_FEATURE groups require capabilities 5/6/7/8; frozen F3 FULL_EXACT groups require 5/6, and new F4 FULL_EXACT groups require 5/6/8. Exact/feature group mode is immutable. Neither batch operations nor old-row garbage collection can bypass the inherited owner/version/generation guards.

This audit confirms the repaired agreement at the reviewed bytes. It does not claim to have exhaustively verified every inherited NET2 transition.

## Assurance left for future execution

The mechanism is now sufficiently concrete to distinguish an implementation from a differently behaving extractor/query protocol. Its utility remains an empirical question under declared workloads and supplied resources. Appropriate qualification hides the useful theorem IDs from the query client, includes unfamiliar providers and diverse native types, counts failed discovery/import/application work, and compares actual checked reuse rather than successful RPC totals.

The expected benefit is better candidate access than an exact-ID-only or ubiquitous-Eq-head search. No theorem here establishes a universal recall rate, an optimal choice of 32 features, a complete global index, or exponential mathematical growth. Those claims remain deliberately outside the accepted design evidence.
