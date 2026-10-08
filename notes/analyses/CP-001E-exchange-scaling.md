# CP-001E: exchanging large reusable mathematical closures efficiently

Date: 2026-09-19. Status: concept-stage performance audit and proposed amendments, not implementation. CP-001D and its files remain frozen. Numerical examples below are transparent calculations from stated assumptions, not measured benchmarks.

This note audits [NET1](../../spec/OPERATIONAL-CORPUS-V1-NETWORK.md) against the intended large, diverse mathematical commons. It proposes one bounded bulk-transfer mechanism and a compatible live accounting-generation amendment. It does not change native mathematical validity, mandate research goals, introduce a central registry, or make remote assessments authoritative.

Companion work: [native scaling](CP-001E-native-scaling.md) and [agent reuse and discovery](CP-001E-agent-reuse-and-discovery.md). The proposed versioned direct semantic-reference graph and persistent witness-map pages are distinct from this transport amendment. New page encodings and new protocol behaviors require an explicitly versioned profile; they cannot silently reinterpret existing IDs or frozen NET1 messages.

The historical Lean v4.22.0 target is not endorsed for deployment by this transport analysis. The separate [foundation security audit](CP-001E-foundation-security-audit.md) governs the current Lean v4.34.0 qualification target, source commit `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`; neither faster byte transfer nor authenticated inventory repairs an unsound native checker. A corrected qualified foundation and its exact cache/interpretation bindings are prerequisites to practical native-reuse claims. The source-scale observations below distinguish the historical dataset from the current qualification target; neither is a release approval or native measurement.

## Main finding

NET1's safety envelopes are useful, but its per-object exchange is not an adequate default bulk-import path. For many small missing objects, service issuance and round trips dominate payload bandwidth by orders of magnitude. Clean global drain can then interrupt useful imports and searches even when the byte volume is modest. A universal 65,536-object closure ceiling additionally excludes some possible large dependency bases by construction; its adequacy for a realistic library was never established.

The remedy is not unbounded messages or unlimited remote work. It is to separate five quantities that NET1 partially conflates:

- wire frame size;
- one paid transfer window's work and output;
- one receiver's finite import/check admission envelope;
- the exact complete mathematical dependency closure of the selected root;
- the total distributed corpus, which need not fit on one node.

A small wire window can transport pieces of a very large finite closure through many separately accounted steps. A receiver still must obtain, check, and protect the full required closure before advertising current native reuse. Neither streaming nor an index removes that evidence requirement.

## Baseline cost model

Let N be the number of missing exact objects, B their unique canonical payload bytes, r the network round-trip time, and p the maximum concurrent paid calls. For this calculation assume:

- every object fits in one NET1 256 KiB chunk;
- the receiver initially has neither its byte manifest nor its payload;
- each object uses one GET_MANIFEST and one GET_CHUNKS call;
- calls succeed without retries, no hash checks fail, and providers are willing;
- compute, storage, native checking, and queueing initially cost zero, so the result is an optimistic network/control bound;
- one offer exchange plus its call/result exchange takes approximately two round trips, excluding serialization time.

NET1 therefore requires C = 2N paid calls. Its default provider admits at most 32 new offers/second; each call also sends two inbound control frames, OFFER_REQUEST and CALL, against 64 frames/second. Ignoring finite initial bursts, both imply

\[
T_{\mathrm{issue}} \ge C/32 = N/16\text{ seconds}.
\]

With p = 4 concurrent requests, the latency bound is approximately

\[
T_{\mathrm{latency}} \ge 2rC/p = rN.
\]

NET1 also permits an initial 16 MiB transfer burst. The literal token-envelope lower bound is therefore

\[
T_{\mathrm{payload}} \ge \max(0,B-16\text{ MiB})/(8\text{ MiB/second}).
\]

For simple sustained-rate comparison, the tables below report B/(8 MiB/second) as a no-initial-burst fluid time, not as the literal minimum allowed for every finite transfer. For a long transfer the actual elapsed time is at least the maximum of the applicable token/latency lower bounds, and generally greater because of the omitted work. Independent stages can overlap; these lower bounds must not simply be added and called an exact prediction. The provider's offer burst of 64 and ingress burst of 128 can improve the issuance bound by at most about two seconds in this idealized calculation, not by a factor proportional to N. Data-dependent discovery can add further sequential latency.

| Synthetic missing closure | Paid calls | Payload time, no initial burst | Offer-limited time, approximately | Latency bound at 100 ms RTT |
|---|---:|---:|---:|---:|
| 4,096 objects of 8 KiB each: 32 MiB | 8,192 | 4 s | 256 s | 410 s |
| 16,384 objects of 2 KiB each: 32 MiB | 32,768 | 4 s | 1,024 s | 1,638 s |
| 65,536 objects of 2 KiB each: 128 MiB | 131,072 | 16 s | 4,096 s | 6,554 s |

The second row fits NET1's default object count and payload-size limits, yet its idealized issue-limited time alone exceeds the 900-second default transfer envelope. This is a concrete mismatch between independent default limits, not evidence that every actual closure reaches those limits simultaneously. At 50 ms RTT the second row's latency bound is about 819 seconds, so control issuance still dominates. Its payload goodput is at most approximately 32 KiB/second under the offer limit, despite an 8 MiB/second byte allowance.

This comparison is already favorable to NET1: it ignores mathematical ReplayManifest traversal, profile objects, manifest-page reads, term parsing, storage durability, independent native checking, and record rollover. A mathematical contribution can consist of several typed objects; object rate is not theorem rate. An illustrative 4–8 newly required objects per contribution would lower 16 objects/second to roughly 2–4 contributions/second before checking, but that multiplicity is an explicit scenario assumption, not a measured property of Lean libraries.

If byte manifests are already known, C can fall toward N; if exact object payloads are already locally retained, their transfer cost is zero. These are important improvements, but do not make a cold or substantially new many-small-object import efficient. Warm reuse must be evaluated separately from cold bootstrap.

## Record retention and global-drain amplification

NET1 clean rollover triggers at 75% of a default 32,768-record control allocation, or earlier if byte/finalization reserves require it. Let q be the average retained record-equivalent units per completed paid call, including the implementation's issuance/replay/accounting representation. The paper specification does not fix q; multiple logical keys might share physical records. Therefore q must be a parameter, not an invented measured constant.

At 32 calls/second, an initially empty store reaches 24,576 record units after approximately

\[
T_{\mathrm{open}} = 24576/(32q)=768/q\text{ seconds}.
\]

| Assumed q | Approximate time to count trigger | Admission duty fraction if each drain costs 90 s | Admission duty fraction if each drain costs 1,200 s |
|---:|---:|---:|---:|
| 1 | 768 s | 89.5% | 39.0% |
| 2 | 384 s | 81.0% | 24.2% |
| 4 | 192 s | 68.1% | 13.8% |
| 8 | 96 s | 51.6% | 7.4% |

The fractions are T_open/(T_open + D) for the specified hypothetical drain D. They are not predicted utilization. Some drains can finish quickly; actual outstanding work and cleanup dominate. But the frozen protocol permits waiting for the residual 1,200-second import envelope before reopening, and exports/cursors also participate in global drain. Thus one long local job can obstruct otherwise short unrelated peer service.

Increasing the control-store size postpones this effect rather than resolving the coupling. Lower per-object call counts help substantially, but a healthy high-demand node can still fill any finite append-only control history. Long-lived work and short-lived remote invocation replay protection should not require one global stop-the-world retirement boundary.

The previous separation of warm-retention clock generation from service epoch was necessary and remains correct: compacting remote service records must not evict or refresh admitted warm mathematics. The same design principle should be applied carefully to running local work and finite data-snapshot leases.

## What the fixed closure caps actually exclude

NET1's 65,536-object, 8 GiB, and 1,024-dependency-depth ceilings are hard protocol limits, not merely defaults. The mathematical document repeats those limits. Consequently, a conforming node cannot presently reuse a root whose exact closure exceeds them by simply allocating more storage or sending additional messages. Having already cached most of the closure does not change its total logical cardinality or depth.

This distinction matters. Splitting a library into modules does not solve the problem when one later theorem's actual transitive closure exceeds the hard limit. Splitting wire transfer is useful, but it must not be mislabeled as a proof that the full mathematical closure was admitted. Replacing unavailable dependencies by remote positive attestations would change the trust model rather than solve transport.

The 64 MiB native-object cap and flat ReplayManifest/SemanticContext representations are additional constraints. Removing only NET1's count ceiling cannot make a manifest arbitrarily large or eliminate repeatedly copied transitive lists. The companion native-scaling proposal addresses these through a new versioned direct semantic-reference graph and persistent canonical witness-map pages. Those pages are ordinary exact mathematical objects for transport, and their completeness is established by receiver reconstruction, not by believing a publisher's page count.

Recommended distinction for the next profile:

| Bound | Its proper role |
|---|---|
| Frame, selector-list, fragment, and bundle bounds | Stable interoperability and bounded parsing/allocation per message/window |
| Native grammar, identity rules, primitive representation ranges | Explicit versioned representation/foundation semantics; legacy objects still obey their original frozen schemas |
| New-profile individual payload/node/depth admission ceilings | Finite local resource policy, separated from mathematical identity as specified by the native-scaling amendment |
| Aggregate closure bytes/objects/edges/depth/work | Finite receiver-local admission policy for a selected root and attempt; not a universal theorem-library size ceiling |
| Retained corpus/store capacity | Receiver-local aggregate allocation, independent of the total open network |

Every admitted closure still has concrete finite count, byte, edge, depth, CPU, memory, I/O, and time allowances. Counters use checked arithmetic. A larger root is admitted only if the receiver can actually reserve its complete obligations. A weak node can explicitly decline it without declaring the root unsupported throughout the entire commons. Arbitrarily large finite imports are not guaranteed on finite fixed hardware.

The root agent's read-only source-tree observations distinguish two datasets:

| Role | mathlib source revision | Mathlib `.lean` source blobs | Source bytes |
|---|---|---:|---:|
| Historical Lean/mathlib v4.22.0 reference, not deployable merely by this pin | `79e94a093aff4a60fb1b1f92d9681e407124c2ca` | 6,726 | 77,230,502 |
| Current Lean v4.34.0 qualification target | `5ed2965256430c3649e86755f9576b54eca72435` | 8,529 | 98,449,500 |

The historical tag resolves to the first revision and its toolchain is `leanprover/lean4:v4.22.0`. The root agent reported the current revision's recursive GitHub tree as untruncated. The foundation audit owns the exact new compiler/source/security selection and its remaining qualification gates. Source files are not native objects, source bytes are not proof-term bytes, and a whole repository is not one theorem's transitive closure. These counts do not prove that NET1's closure caps are violated. They identify historical and current datasets for future exact exporter/closure measurements rather than justify reassuring guesses from a six-seed example. This note performed no native export, compilation, or replay measurement for either dataset.

## Selected bulk amendment: bounded object-range bundles

Call the proposed extension BUNDLE1. It amortizes service authorization across bounded groups of already identified object bytes. It does not grant a caller a search program, server filesystem access, arbitrary CAS enumeration, or an open-ended stream.

One BUNDLE1 service call contains:

`[readScope,requestItems,requestedPayloadLimit]`

where each request item is `[objectContentID,startOffset,spanCeiling]`.

The selected baseline is:

- at most 256 request items, in explicit canonical order, with no duplicate identical item;
- actual encoded request at most 16 KiB, including its fixed call fields;
- positive span ceilings, whose sum is at most 4 MiB;
- a committed canonical result body containing at most 4 MiB of selected payload plus at most 64 KiB of bounded item/status metadata;
- delivery frames carrying at most 256 KiB of result-body bytes, within the existing outer frame ceiling;
- at most four concurrently admitted outgoing bundle calls per receiver, sharing its existing aggregate transfer/record/memory allocation;
- provider computation, spool storage, pin lifetimes, and reply delivery admitted before its offer, with finite independently enforced budgets;
- no wire-level compression in this first amendment, so compressed-data expansion is not another acceptance boundary.

These are concrete baseline choices. They preserve small requests and bounded response buffers while allowing multiple small objects per paid call. The exact request byte bound is enforced even if a nominal count would fit; count and byte limits apply together. Data frames belong to an already claimed and metered bulk-delivery job, not a fresh anonymous-control request lane. Their frame parsing/connection memory still has aggregate bounds.

For mathematical bytes, readScope remains one explicit public ReplayID closure or one holder-bound live export scope, including the EXPORT_HEAD2 scope below. The provider authorizes every requested CID against that exact locally known scope, including any new mathematical trie pages. Same profile, same publisher, adjacent name, or appearance in a peer hint does not grant membership. Advisory cached child replay manifests are not silently included unless the selected mathematical closure actually includes them or another explicit permitted scope is selected.

The separately negotiated organization extension ADVISORY_READ1 adds scope `[2,manifestCID]` for one explicitly owner-disclosed, bounded bundle of typed inert advisory objects. Its negotiated HELLO_REPLY extension advertises at most four public manifest-root hints within the existing actual HELLO byte/control caps; it does not send their payloads or trigger automatic follow-up. The organization profile limits that manifest to 64 KiB, at most 1,024 explicitly listed typed objects, at most 1 MiB per advisory data object, at most 8 MiB aggregate including the manifest, and at most 4,096 advisory entries. The manifest itself is explicitly in scope, not recursively listed inside its own commitment. BUNDLE1 can transport only these exact authorized advisory members under the same metering, pinning, and disclosure-version rules. References inside an advisory object do not expand this scope into mathematical data, other advisory bundles, or arbitrary CAS records. Native theorem bytes need their own explicit public-root/export scope, and advisory bytes never become native proof or execution authority. Unsupported scope kinds are rejected rather than reinterpreted.

### Exact item result

For a known authorized object with canonical payload length L and request `(c,o,s)`, the success record is conceptually

`[requestOrdinal,OK_SLICE,c,L,o,payloadBytes]`.

It requires 0 <= o <= L and

`length(payloadBytes) = min(s,L-o)`.

The bytes are exactly that payload's interval beginning at o. A request with o > L returns a bounded invalid-range status. Unservable/private/absent items share the same nondisclosing `NOT_SERVABLE` treatment where required by the read-scope policy. Detected local corruption or lost availability has a bounded item status rather than substituted bytes.

The top-level service successfully returns one committed typed batch; individual items may report nonavailability. This is not a mathematical acceptance, an incomplete FIND page, or a claim that all requested objects exist. Request ordinal, CID, offset, length, and total length must be checked by the receiver. A shorter-than-ceiling slice can indicate the exact object end only under its declared total length; the receiver still recomputes the full object's ContentID before treating it as verified bytes.

If lengths are unknown, an initial window can request at most 16 KiB per object for 256 objects, fitting the 4 MiB payload reservation. Small objects finish immediately. Larger objects reveal their claimed length and supply an initial range; later separately paid windows request further explicit ranges. Thus the protocol does not require one preliminary byte-manifest RPC per small object. A misleading length cannot establish valid object identity or native acceptance, and all attempted bytes/work still count against the receiver's finite envelope.

### Sender execution and immutable commitment

The existing two-ticket separation is retained:

1. Before offering, the provider reserves a finite computation/spool allocation and a separate one-shot delivery allocation. It also reserves its worst-case terminal control records and bounded physical-generation read pins.
2. One claimed provider-local computation authorizes the exact scope and items, resolves currently available physical generations, pins the selected read ranges' containing generations while reading, and prepares the whole bounded canonical result in an inert spool. Scope-membership lookup, hashing, copying, storage reads, and spool writes are metered, not assumed free.
3. Its atomic completion records the exact call, result-body length and digest, disclosure scope/version, spool allocation, metered computation result, and a nonauthorizing reply intent. The computed result is now immutable.
4. The separately claimed delivery checks the still-authorized exact scope/version and audience, then sends only those committed body bytes. A withdrawal before delivery claim cancels the send; after claim it requests bounded cancellation, with no ability to recall bytes already handed to TLS.
5. Delivery meters actual bytes handed to the transport while running and settles once. Its end message does not prove peer receipt. A reply/body expiry or failed connection never reruns the computation under the old action key.

A concrete body commitment uses a versioned domain separator, the canonical call CID, and the exact canonical result body. START names its committed length and digest; DATA carries a strictly consecutive byte offset and a bounded body fragment; END closes that same committed sequence. The receiver rejects overlaps, unexpected offsets, excessive lengths, or an end/digest mismatch. The full body commitment detects transmission/protocol inconsistency; it does not make an untrusted provider's chosen object bytes mathematically authoritative.

Existing provider storage-generation and GC exclusion still apply. A physical object cannot be deleted under an active read pin. Once the immutable spool holds the selected bytes, the object read pin can end; the separate spool allocation lasts only through its finite delivery lifetime. Publishing a closure does not authorize exposing a private dependency, and a generic CID does not bypass the chosen read scope.

The byte-volume change does not authorize a 4 MiB theorem checker invocation on the sender. Serving already selected inert bytes is a network/storage job. Native checking, if needed for the provider's own prior corpus admission, remains a separate funded operation.

### Receiver execution, hashing, and crash/resume

The receiver first allocates its own finite transfer/staging/check envelope. The sender's offer never supplies receiver resource authority. Receiver work includes bounded parsing, object-range bookkeeping, bytes received, canonical payload hashes, staging writes, complete closure discovery, and later native checking.

Each object retains one exact expected ContentID, claimed total payload length, and bounded range-coverage state. Before allocating range state or enlarging staging, the receiver rejects lengths outside the applicable native/object/profile limit or its local admitted allocation. Offset, span, end-offset, count, and accumulated-byte arithmetic is checked for overflow and bounds; an adversarial uint64 value cannot wrap into a small allocation. Inconsistent total lengths or overlapping contradictory bytes fail that candidate assembly. The receiver may prefer sequential ranges for each object to minimize coverage metadata. Range bytes are inert partial evidence until the complete canonical payload has been reconstructed and its typed ContentID recomputed. A body digest or remote signature is not a substitute for that final object check.

Complete independently hash-verified objects may be durably retained in the receiver's staging allocation even if a later bundle item or END is missing. Their authority is their own verified content identity, not an assertion that the entire service completed. Incomplete ranges are also only inert staging and can be discarded or retained within a specifically bounded policy. Native promotion still requires the complete selected mathematical closure and the receiver's own checking/admission transaction.

After sender failure, the old paid action cannot be replayed for another free delivery. After receiver failure, recovery follows the conservative local accounting rules. A subsequent attempt requests only independently verified missing objects or explicit missing ranges under fresh funded authority; it does not extend a prior deadline or revive an old remote ticket. Reusing a complete object requires its current local integrity/availability condition. Reusing unverified partial bytes may save bandwidth, but they remain untrusted and can cause the final full-object check to fail.

An unfinished overall import does not retain staging forever. Continuing across an attempt boundary requires a new explicit local staging/use allocation before the old protection ends. A failed or abandoned root cannot install an infinite retention chain by repeatedly naming its partial bytes.

### Amplification and resource bound

For one admitted call with m <= 256 items and total span S <= 4 MiB:

- selected payload output is at most S;
- result metadata is at most the separately fixed 64 KiB;
- query/scope traversal, reads, hashes, spool writes, and delivery are bounded by the provider's complete finite vector, not by S alone;
- receiver bytes, parser memory, assembly state, and storage are independently bounded;
- no item causes recursive provider fetching, mathematical proof search, new retention pins after job termination, or further remote calls;
- mismatches, zero useful bytes, cancellation, and duplicate messages still consume the appropriate issue/record/accounting allowances.

Thus a caller can receive more bytes than its request size only within the deliberately granted bounded response envelope. Its arbitrary key count cannot create new aggregate bandwidth or control capacity. If the provider cannot reserve the requested envelope, it refuses or offers a separately specified smaller exact call, never silently increases the caller's authority.

## Conditional bundle efficiency

If object lengths fit the selected per-item spans and the closure's needed IDs can be batched, the many-small-object workload uses approximately ceil(N/256) bundle calls instead of 2N object calls. That is a factor of up to 512 fewer paid calls, not a factor of 512 faster native mathematics.

| Synthetic missing closure | Bundle calls | Offer-limited time, approximately | Latency bound at 100 ms RTT and four calls | Payload time, no initial burst |
|---|---:|---:|---:|---:|
| 16,384 objects of 2 KiB: 32 MiB | 64 | 2 s | 3.2 s | 4 s |
| 65,536 objects of 2 KiB: 128 MiB | 256 | 8 s | 12.8 s | 16 s |
| 1,048,576 objects of 2 KiB: 2 GiB | 4,096 | 128 s | 204.8 s | 256 s |

The third row is a proposed-profile scaling scenario, not a valid NET1 import and not a claim that its native checking fits current hardware or budgets. Payload fluid times omit metadata, source/sink storage, hashing, scheduler contention, dependency discovery, and native checking. The initial transfer burst changes the literal payload token bounds to 2, 14, and 254 seconds respectively; control bursts also change small-call token bounds. Neither removes actual link/CPU/storage work. The table demonstrates removal of the forced per-object RPC tax; it is not a throughput benchmark.

If dependencies are discovered along a chain of depth d with no usable prior inventory, at least d causally dependent discovery stages may remain. Bundling does not collapse a sequential mathematical dependency chain into one round trip. A provider's exact snapshot-bound inventory and the companion paged native witness/reference graphs can expose breadth efficiently, but the receiver still verifies actual native reachability and rejects missing/extraneous witness claims.

Very large objects likewise need several range windows. Their transfer approaches a byte-volume-bound path rather than one service per tiny object. Repeatedly requesting single-byte slices remains bounded paid behavior; a provider can decline such inefficient traffic under local service policy without changing mathematical validity.

## Selected portable-inventory amendment: EXPORT_HEAD2

NET1's export root can list only 16 pages of 4,096 objects each. Therefore bundles and relaxed receiver closure ceilings alone do not make a closure of more than 65,536 objects exportable or portable as a conforming archive. The native witness trie also is not an inventory of every reachable definition, term, group, profile, and other mathematical object. This is a separate interface that must change.

The selected next-profile amendment replaces the bounded flat page-ID list with a bounded-page authenticated inventory tree. Call the operation EXPORT_HEAD2. Its head commits to:

`[version,issuer,exportLeaseID,holder,rootReplayID,inventoryRootCID,objectCount,totalPayloadBytes,requiredProfileIDs,createdTick,expiresTick]`.

The operation accepts only an explicitly public root or, for an owner-authorized local archive, the owner's explicitly authorized local collection. Remote requests do not confer permission to export private dependencies. The exact root here is one typed-root ReplayID with its complete native closure; optional collection packaging would require a separately specified finite root set rather than pretending a module name is this root.

The provider offers EXPORT_HEAD2 only for an already committed exact inventory, or explicitly declines until a separately locally authorized and bounded inventory-build job completes. It cannot hide an unbounded full-library graph walk inside a cheap HEAD request. Inventory construction, integrity checks, persistent page storage, and the subsequent finite export pin have independent admitted costs. Shared immutable inventory pages can be deduplicated, but current root membership, authorization, and pinning remain checked local state.

### Canonical persistent inventory, not position-packed pages

The first draft grouped sorted entries into consecutive full 2,048-entry leaves. The native agent's independent audit found that one insertion near the front shifts entries throughout the suffix, changing Theta(N) leaf bytes and parent hashes. Canonical ordering alone does not imply persistence. Repeated growing exports could therefore recreate quadratic metadata copying. That packing is withdrawn from this selected amendment.

EXPORT_HEAD2 instead uses a canonical binary Patricia map from exact native ContentID to canonical payload length. Its operational node type is proposed `0x8020`, schema 1, distinct from the mathematical direct-reference/witness node types. The new export-head record uses proposed operational type `0x8021`, schema 1. These are new-profile registry allocations, not reinterpretations of frozen NET1 types.

For the current identifier suite, a key is the injective fixed 37-byte representation

`u8(algorithm) || u16be(type) || u16be(schema) || digest32`.

Let L = 296 bits. Keys compare in unsigned bytewise order of those exact bytes, not source-name order, a digest prefix, or an extra hash of the CID. The node payloads are:

| Kind | Canonical payload | Bound and meaning |
|---|---|---|
| Empty | `[2]` | Defined for map operations; a valid native-root export itself is nonempty |
| Leaf | `[0,keyBytes,payloadLength]` | Exactly one full CID key and checked uint64 length |
| Branch | `[1,splitBit,prefixBytes,leftCID,rightCID]` | Exactly two nonempty children of this operational node type |

Each encoded node is at most 256 bytes in this suite. `splitBit` is the first differing bit among its descendant keys, numbered from zero at the most significant bit. `prefixBytes` encodes exactly the preceding splitBit bits in the minimum byte count, with unused low bits zero. Every descendant shares that prefix. The left/right descendants respectively have bit zero/one at the split; child branches split strictly later. Unary branches, duplicate keys, wrong child types, noncanonical prefixes, and missing-child-as-empty interpretations are forbidden. Each actual object length is subsequently checked against its canonical payload and the applicable local/representation bounds.

The receiver checks node hashes, exact shapes, key kinds, child partitions, and actual descendant boundary conditions. Verified local subtree summaries may record minimum/maximum keys, leaf count, and total native payload bytes. Unverified sender summaries or head counts cannot certify completeness; local summaries are derived under the exact node root and qualified decoder and use checked arithmetic. A first unknown tree requires traversal within the admitted envelope. Locally retained verified subtrees may reuse their exact summaries.

**Canonicality.** A singleton map has one uniquely determined leaf. Otherwise the first bit at which its keys differ and the two resulting nonempty partitions are uniquely determined. Recursion gives one shape and root for an exact CID-to-length map, independent of insertion order or publisher. Distinct maps remain distinct commitments under the content-binding assumption.

**Conditional incremental update.** Given an already verified retained old map and an independently established exact delta of k changed membership/length entries, path copying produces at most O(kL) new inventory nodes and reuses unchanged subtree IDs. Ancestor summaries can be updated from already verified child summaries along those paths. For a fixed ContentID, a conflicting length is an integrity mismatch rather than a legitimate semantic rewrite. This bound concerns representation maintenance after obtaining the correct delta; it does not establish the delta or prove native closure completeness for free.

A wholly new snapshot, unknown selected witness graph, cold receiver, unavailable child summaries, or newly discovered large dependency change can require a complete native graph walk and Theta(N) inventory validation/construction. A producer may exploit its own checked closure/dependency caches to derive an exact small delta, but a peer's asserted delta is not authority. The inventory must still match the selected root's actual complete native closure. Joining arbitrary unrelated closures has no claimed O(k) shortcut.

For N nonempty inventory entries, a fully materialized binary Patricia tree has N leaves and N-1 branches. An inventory of 1,048,576 native objects thus has 2,097,151 logical inventory nodes, not the earlier 517 position-packed pages. The 256-byte node ceiling gives a coarse bound below 512 MiB on their payload bytes, excluding CAS indexes and physical storage overhead; actual encoded lengths are smaller but unmeasured here. Logical CAS nodes need not each be a filesystem file. Physical packing, lookup cost, and bundle overhead are explicit qualification issues, not free benefits of content addressing.

The tradeoff is intentional: bounded canonical path-copy updates replace suffix-wide rewriting at the cost of more small logical nodes and potentially greater cold metadata overhead. BUNDLE1 amortizes their transport but does not erase that overhead. A cold exact export with N native objects has up to 3N-1 native-plus-inventory logical objects before any already available/shared objects are excluded. The earlier transfer tables count the stated N objects only; an actual exported closure must count its additional inventory nodes and bytes too. If each new native stage changes O(L) native map nodes, updating its operational inventory can require O(L squared) additional inventory nodes; the native O(L) update bound is not automatically the bound for every downstream index.

There is no fixed 16-page or 65,536-object total ceiling. Each local export/import still selects finite aggregate inventory-node, native-object, byte, traversal-depth, CPU, memory, and I/O budgets. Trie lookup depth is at most L and is distinct from mathematical dependency depth. Reaching a budget yields bounded noncompletion, never a certified truncated inventory. A larger future identifier suite requires an explicit node-schema/key decision rather than silent truncation.

The leaf set contains the complete mathematical closure, including its selected Replay root and all required native trie pages. It does not include the operational inventory nodes themselves, avoiding a self-commitment cycle. The export scope separately authorizes exactly the operational inventory nodes reachable from inventoryRootCID plus the native objects named by its validated leaves. It does not authorize arbitrary operational/CAS objects, all same-profile objects, or foreign suggested child replay manifests. The content-addressed head and root page are explicitly part of this finite export scope; the head does not insert its own hash into the inventory. NET2 returns the head payload and its CID in the authenticated exact response; it does not define a separate head-signature wrapper. Offline possession of that head does not establish a currently live remote lease or mathematical acceptance.

### Fetch, completeness, and archive

The head returns the immutable inventory root CID and its bounded root page. The receiver can request its exact child pages, then selected native object ranges, through paid BUNDLE1 calls under that same holder-bound export lease. A parent-page commitment authenticates which child CID was named; a hash-verified page still must pass all native/operational syntax bounds before its references become candidate fetches. No remote page can enlarge the receiver's already admitted aggregate envelope.

The head's declared object count and total payload bytes enable bounded tentative planning; verified subtree summaries and exact key-prefix paths support membership/coverage checks. Claimed counts are not trusted evidence that the producer included every mathematical dependency. On complete import, the receiver rebuilds the actual native closure from the selected ReplayID and witness/reference objects, checks its canonical CID-to-length map against the exact inventory root, and rejects missing or extraneous native objects under this export profile. Missing source bytes or budget exhaustion produce noncompletion, not a falsely complete archive. Where complete exact locally checked closure caches are reused, their snapshot/incident/integrity conditions remain independently required.

The export lease pins the exact inventory pages and named native physical generations until its finite deadline or permitted termination. Creating that pin requires local retention capacity; enumerating IDs alone does not make the bytes present. Disclosure-version withdrawal prevents a not-yet-started response from exposing revoked contents, independently of whether an export pin still protects physical bytes. A live lease does not mint bandwidth: each page/range request is separately funded at provider and receiver.

An offline archive is a finite record stream containing the head, every reachable inventory page, and every named exact native canonical payload. Individual archive records have declared checked lengths and are processed under the same object/page and aggregate local bounds; the archive file is not forced into one wire frame or one memory allocation. The actual mathematical checker distribution remains separately selected/admitted: a named profile or bundled executable is not permission to run peer code.

Import can resume using verified immutable page/object IDs and explicitly funded local staging. An expired lease is not silently renewed. A fresh independently admitted lease for the same exact inventory can serve remaining bytes; a new inventory root is a different snapshot and cannot be spliced into an allegedly complete old archive. Receiver-native recomputation, final object hashes, and retained complete closure remain mandatory in either case.

Thus this amendment covers both recursive public-root fetching and genuinely portable whole-closure archives without retaining NET1's hidden export cardinality ceiling. It does not promise free export of arbitrary-sized archives, indefinite leases, or that any fixed node stores the entire mathematical commons.

## Selected accounting amendment: seal invocation generations without draining all work

Bundling reduces tombstone growth but does not remove the need for bounded compaction. This amendment separates remote-invocation admission generations from local execution/recovery fencing. It is proposed for a new protocol profile, not asserted to be the behavior of NET1.

Use two independent concepts:

- `admissionEpoch`: the namespace in which remote offers and CALL redemptions may create new protected work;
- `recoveryGeneration`: the actual local writer/boot fence under which already claimed executions, authoritative meters, and finite data leases are valid.

Warm retention retains its separate monotonic time-origin generation already specified. All counters are checked, never wrapped. These names distinguish authority roles; they do not create separate independent spend budgets.

### Seal transition

At the record threshold, the single authority writer can perform one atomic transition:

1. Advance the durable remote-admission floor and advertise a new admission epoch. After this point no OFFER_REQUEST or CALL in a sealed epoch can create an offer, reservation, or remote execution claim. Reject it before allocating new durable request state.
2. Cancel/terminalize all sealed-epoch unused offers and unclaimed remote operation reservations, retaining consumed issue/redemption allowances and any necessary terminal accounting. A caller must obtain a new offer to try again.
3. Preserve only explicitly enumerated already claimed execution records and their preallocated fixed local continuations. For example, a running bundle computation can finish and its previously allocated issuer-only reply ticket can be claimed once for that exact immutable reply. A computation already FINALIZED with its exact committed reply still RESERVED/unclaimed is also explicitly preserved as that fixed one-shot reply continuation, even though its parent is no longer running; it is not mistaken for an unused remote-operation offer. The remote caller cannot change either continuation or supply another computation through it.
4. Preserve live finite snapshot/export data leases and their original holders, scope versions, immutable cuts, pins, and monotonic deadlines. These leases authorize which data an independently paid new call may read; they do not themselves authorize execution or bandwidth.
5. Retain global cumulative spend, reserved allocations, rate-token state, current storage roots, recovery fencing, and all outstanding terminalization capacity. Do not release and remint the surviving allocations.
6. Compact sealed-epoch issuance/replay records that are not required by those live records. The durable rejection floor prevents forgotten old request keys from becoming fresh authority. A completed old action may subsequently return REPLAY_EXPIRED, never reexecute.

New-epoch admissions can start as soon as this atomic transition and required conservative reservations permit. They need not wait for an unrelated old local import to finish. Finite currently running work can still consume all resources and cause ordinary admission refusal; the improvement removes an artificial global epoch drain, not real resource contention.

### What must remain in the live continuation set

Each preserved execution/continuation record binds its original exact action, grant/allocation, audience if any, request digest, execution phase, one-shot claim state, authoritative meter, recovery generation, deadline, and permitted next local effect. It has no remote delegation or new-work fanout. A later result transaction can settle that record or activate only its already allocated fixed reply continuation. It cannot create new old-epoch external service authority.

The live set has independent count/byte limits and is charged against the same aggregate control store; one old epoch cannot leave unlimited survivors. New admissions reserve their eventual terminal records before acceptance. If the surviving records, compaction workspace, and new-work records cannot all fit, the node refuses new work. This is the correct bounded failure mode, rather than pretending compaction always succeeds under arbitrary load.

Ordinary standing local maintenance and a claimed local import are not remote invocation rights. Their existing finite authority can survive an admission-generation seal under the same recovery generation, without new grant issuance. Creating new local work still requires the current local admission rules and new allocations. On a real writer change or reboot, old running executions receive the existing conservative nonpromoting recovery treatment; clean sealing is not an exemption from crash fencing.

### Snapshot and export continuity

A cursor must bind its immutable snapshot lease, exact query/planner, holder, and expiry. Its authentication material is retained with that bounded live snapshot lease, rather than requiring an otherwise useless entire admission epoch's replay history. A new paid FIND continuation can validate this still-live old-origin snapshot without treating an old CALL as valid. An expired or missing snapshot still gives STALE_CURSOR, and no seal extends the 120-second default lifetime.

An export scope similarly names one live local export lease, holder, exact root/closure and authorized disclosure version. A new-epoch paid bundle can use it until its original expiry or revocation. Any issuance-time admission epoch recorded by its original response remains historical metadata; availability and authority come from the current local live-lease record, not from reactivating that epoch. Lease IDs are never reused within the authority history, and removing a lease makes its unknown old ID unservable. Randomness alone is not a budget or a replacement for checked exhaustion rules.

This amendment does not fix a FIND scan that needs longer than its actual snapshot lease or repeatedly returns the same prefix. Those are independent retrieval/planning questions addressed by the organization analysis. Nor does it promise every session survives a real crash, disclosure withdrawal, or lack of allocated resources.

### Crash ordering and the conservation argument

The seal/floor update, cancellation decisions, and identification of survivors must be durably atomic under the local store model. Completed old records must not be physically forgotten before the durable floor prevents their replay. A crash before that commit leaves the old state to normal recovery; a crash afterward retains the rejection floor and conservatively finalizes old-running work under the new recovery fence. Background log compaction is separately metered and reserves its temporary physical bytes.

The intended safety invariant is:

`new remote claim => current unsealed admission epoch and an unspent admitted offer`;

`old-origin protected effect => exact retained live continuation and its unchanged finite allocation`.

Together with one-shot claims and cumulative accounting, sealing cannot amplify a grant. No restored old request is allowed to manufacture the live-continuation record that would be required to execute it. Data leases remain nonexecution capabilities. This is a paper refinement argument requiring later state-machine and crash-ordering qualification, not a completed formal proof.

## Routing horizon at large network size

NET1 has at most 256 locally stored contacts and selects at most four peers per lookup round. Four is a concurrency/fanout limit, not a theorem that only four peers can ever be consulted. A session that eventually tries every contact in its initially pinned directory can have up to 64 four-peer rounds, each still independently funded. The fixed 256-contact snapshot is the actual maximum search horizon of that session.

GET_ROUTES returns at most eight shareable contact hints and accepts at most 16 excluded IDs. It is one-hop discovery, not recursive FIND. New hints seed a separately funded session rather than enlarge an active session. Consequently:

- repeated queries can return the same eight hints; a 16-ID exclusion field cannot express an arbitrary 256-contact tried set;
- replacing directory entries can broaden future exploration, but no global coverage or eventual honest route follows from the current ranking rule;
- a newly encountered relevant specialist must first enter a future local directory/session; the active lookup cannot claim it inspected that specialist;
- no universal roster or central bootstrap is required, but an eclipse or disconnected contact graph still limits discovery.

These are substantive discoverability constraints, not mathematical unsoundness. Exact checking protects an imported proof even when discovery is hostile; it does not make a useful missing theorem appear. At very large scale, bounded collection guides, profile/domain advertisements, alternative contact sources, and locally selected specialty indexes can improve routing without changing proof acceptance. Their query utility and coverage require scoped evaluation. This note does not silently replace the directory with an unbounded DHT or universal index.

## Acceptance criteria for the next concept checkpoint

Before moving from this concept to software, the integrated specification should show all of the following on paper:

- a many-small-object import uses bounded bundles rather than one manifest/call pair per object;
- frame/window limits do not become an unacknowledged universal mathematical-closure size limit;
- the native paged witness/reference representation and public read scope agree on exactly which page/object IDs can be fetched;
- complete local dependency availability, independent checking, scope revocation, generation pins, and exact object hashes remain unchanged obligations;
- a service-generation seal cannot resurrect old claims and does not force unrelated current work to stop merely to delete old tombstones;
- response framing, provider spool, receiver staging, partial-object state, compaction bytes, and recovery finalization all have explicit finite allocations;
- no timer, retry, missing dependency, cursor, export lease, or advisory page creates another unfunded operation;
- cold bootstrap, warm incremental reuse, realistic closure distributions, and adversarial failed transfers are evaluated separately;
- a representative pinned library export measures exact object counts, unique bytes, dependency edges/depth, cache reuse, and native check costs; source-file counts alone are insufficient.

The central desired improvement is reciprocal local reuse at a cost close to the actual new bytes, new verification work, and bounded discovery—not a fixed global promise of exponential mathematical growth. This amendment removes identifiable protocol overhead while keeping success conditional on actual retained evidence, compatible native profiles, willing service, and funded resources.

## References and evidence status

- [Frozen NET1](../../spec/OPERATIONAL-CORPUS-V1-NETWORK.md), reviewed SHA-256 `46529C8040D8D58F9CB6C27FB4DBC148C525AFC0B0FCCA49788A71FD2136871B`.
- [Frozen mathematical profile](../../spec/OPERATIONAL-CORPUS-V1-MATHEMATICS.md), for existing flat manifests, native object limits, complete closure, and exact checking requirements.
- [Proposed native scaling amendment](CP-001E-native-scaling.md), for versioned persistent witness maps and direct semantic-reference commitments.
- [Official mathlib4 v4.22.0 tag reference](https://api.github.com/repos/leanprover-community/mathlib4/git/ref/tags/v4.22.0).
- [Historical mathlib4 source tree](https://api.github.com/repos/leanprover-community/mathlib4/git/trees/79e94a093aff4a60fb1b1f92d9681e407124c2ca?recursive=1).
- [Current qualification mathlib4 source tree](https://api.github.com/repos/leanprover-community/mathlib4/git/trees/5ed2965256430c3649e86755f9576b54eca72435?recursive=1). Both sets of source-count figures above were supplied by the root agent's source-only inspection; this note does not claim a compiled exporter/native-closure measurement.

No coding, executable model, conformance test, native proof replay, or performance measurement was performed for this note.
