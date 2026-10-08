# V5 federated formal discovery: implementation contract

Scale owner,2026-10-07. Root adopted the source-backed design and selected the
four pure source files under software/v5/discovery. They are now authored with
primitive tests; no runtime or network campaign is authorized by this document.
Frozen v4 remains unchanged. All paths are below the canonical project root.

## Decision and first implementation boundary

Add a **separate metadata-only discovery store and new versioned protocol**.
Do not migrate the v4 custody database, overload its one-key `find`, change its
HMAC cursor semantics, or modify mathematical acceptance. First implement pure
formal features, authenticated immutable snapshots, conjunctive query planning
and a bounded SQLite serving store. Then connect these to a distinct network
service and existing exact-ID custody/acquisition/checking. Index providers need
not be custodians; neither role is a mathematical authority.

The decisive additional capability is unknown-ID discovery by several formal
features, with independently verifiable examined-page coverage and transferable
snapshot continuation. A public snapshot commitment does not prove truthful
feature extraction or complete coverage of the global mathematical corpus.

### Source evidence and compatibility

Installed baseline is
`product-local/v4-library-package-01/extracted/commons-v4`, manifest SHA256
`a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed`.

| Existing source | Relevant behavior and consequence |
|---|---|
| `library/library_codec.py`, SHA`9480ce938123c910ecbecddb55ba18d1e748505acc0202dd8fc7dcef56f46a36` | `inspect` verifies canonical bytes, policy, identifier, graph syntax, exact aliases/import use and bounded graph closure. It returns type key, plan and alias map. It does not establish mathematical inhabitation. This is the first adapter. |
| `library/library_store.py`, SHA`e691cb7f72945df87e3bd617f96728a90018683b43ae14fb3cc80e7fdc0f9d3a` | Stores full raw module custody. Only exact ID and one structural type key are indexed. HMAC cursor binds local store/cut/key/limits; clients cannot independently verify it or continue against another store. Keep this working custody path unchanged. |
| `definitions/definition_index.py`, SHA`bd3fad7c30b8922ce5869a3885b7d5c08900c6018424b6dffb7c9b7ee7e40b3f` | Already derives exact/alpha type and constant keys from selected canonical definitions. Reuse its architectural separation, not its different namespace/identity as if it were a named-module identity. |
| `overlay/library_overlay.mjs`, SHA`9665273e0f5309197cc4e72fd3f125b5061284e99403f47b5ee4f436a3614b48` | Existing request schema accepts one key and optional cursor, fixed8rows/32scan/16KiB/250ms. A new conjunctive authenticated reply does not fit that schema. Add a separate protocol/service rather than silently change it. |

No dependency graph must be lowered or mathematically rechecked to extract the
features below. Only the selected canonical object is inspected. Consequently
index construction does not fetch proof ancestry or every imported body.

## Four separate assertions

1. **Mathematical warrant:** the exact object is accepted by its applicable
   checker/certificate policy. Discovery never establishes this assertion.
2. **Feature truth:** a record's feature set equals the deterministic extractor
   on its exact object bytes under the adopted schema. The local honest builder
   computes this. A remote consumer can check it after acquiring those bytes.
3. **Committed-page coverage:** the page contains every ordinal in a specified
   interval of one committed posting sequence, with correct query filtering
   relative to the included feature records. This is publicly verifiable.
4. **Corpus coverage:** every qualifying object in a named corpus was included,
   with truthful features. Neither signatures nor membership prove this. It
   needs an independently justified index-build relation to that corpus.

Global completeness is not an available fifth assertion. Unknown participants,
partitions and publication policy prevent an unqualified global no-match claim.
Even a complete truthful index of a named finite corpus would be complete only
for this decidable feature predicate, not arbitrary mathematical equivalence.

## Canonical encodings and object adapters

All canonical JSON uses sorted keys, UTF-8, no insignificant whitespace, no
duplicate keys/floats/NaN, and exact field sets. Integers reject booleans. Hashes
are lowercase64hex SHA256. Domain strings below terminate with NUL; hash inputs
are domain bytes followed by canonical bytes, or explicitly specified fixed-size
binary fields. No generic concatenation of variable-width fields is permitted.

First supported object kind: `named-definition-v1`. Its exact ID is the existing
ModuleID, not the raw file SHA. Future certified-module/theorem adapters need
their own declared format/policy namespace and feature specification; the first
adapter is not a claim to index arbitrary Lean/mathlib objects.

The adapter API is:

```text
NamedModuleAdapter(adopted_library_codec, adopted_codec, adopted_registry)
adapter.extract(raw, expected_id=None) -> ObjectRecord
adapter.describe(raw, expected_id=None) -> record, specs, work, type_nodes,
                                          mathematical_acceptance=false
compile_query(discovery_namespace, feature_specs) -> sorted FeatureID set
```

`extract` calls the adopted `library_codec.inspect`, reconstructs its bounded
Graph, and uses its alias map and header type. It never executes source, tactics,
native code, imported definitions or a peer-provided extractor.

```json
{
  "schema":"DMKN_FORMAL_FEATURE_RECORD_V1",
  "namespace":"<discovery namespace digest>",
  "kind":"named-definition-v1",
  "object_id":"<ModuleID>",
  "object_sha256":"<raw bytes SHA256>",
  "object_bytes":2441,
  "features":["<sorted unique FeatureIDs>"]
}
```

`namespace = H('DMKN-DISCOVERY-NAMESPACE-V1', {object_format, formal_policy,
feature_schema:'DMKN_DECLARED_TYPE_FEATURES_V1', partition_bits:8})`.
Formal policy includes foundation/profile and lowering contract. An incompatible
extractor or future relation does not share this namespace accidentally.

`RecordID = H('DMKN-FORMAL-FEATURE-RECORD-V1', ObjectRecord)`.
`FeatureID = H('DMKN-FORMAL-FEATURE-V1', {namespace, feature_spec})`.
Record claims contain no mathematical acceptance flag, ownership entitlement,
human intention, usage reward or required retention promise.

## Exact first feature schema

Features are finite syntactic predicates, deliberately not semantic equality.
Display binder labels are ignored in the features below. The existing exact
structural type-key feature keeps its existing universe-name sensitivity.

| `feature_spec` | Exact extraction |
|---|---|
| `{"tag":"object-kind","value":"named-definition-v1"}` | Always emitted. |
| `{"tag":"declared-type-key","value":K}` | K is the existing inspector's complete `type:<digest>` value. |
| `{"tag":"type-symbol","symbol":S}` | One per distinct constant appearing in expressions reachable from the declared type root only. |
| `{"tag":"result-head","head":A}` | Peel leading syntactic `forallE` binders; flatten the remaining outer `app` spine; encode its head as below. No reduction/unfolding. |
| `{"tag":"binder-domain-head","head":A}` | For every leading `forallE`, flatten its domain's outer `app` spine and encode that head. This means presence, not a count or ordered telescope match. |
| `{"tag":"type-edge","parent":P,"slot":R,"child":C}` | Distinct expression-constructor/child-slot/constructor triples on the reachable declared-type DAG. Slots are from the adopted schema (`fn`,`arg`,`type`,`body`,`value`,`struct` as applicable). |
| `{"tag":"direct-import","module_id":I}` | One per exact distinct direct module import, including imports used only in the value. This is explicitly not a type-only feature. |

For a `const`, symbol S is either
`{"kind":"foundation-name","name_hash":H}` or
`{"kind":"module","module_id":I}` after the exact alias map. No contributor
display name substitutes for imported identity. A constant head A is
`{"tag":"const","symbol":S}`. Other heads are `{"tag":T}` for their actual
expression constructor. A `bvar` head does not encode an absolute variable name,
and presence of the same head does not establish matching binder dependencies.
Projection structure names are represented as foundation symbols when their
`proj` nodes occur. Universe level expressions are not treated as term symbols.

Traversal is an iterative visited-expression walk; binder context is not needed
for these explicitly syntactic presence predicates. Expression child iteration
must use the adopted tag schema, including `letE` type/value/body. Each visited
node and child edge is charged. Never normalize, unfold an import, invoke
definitional equality, or enumerate all root-to-node paths during extraction.

Limits: preserve canonical object4MiB/62285rows and inspector work/depth limits;
add at most128 distinct emitted features and16KiB record bytes. Overflow returns
`FEATURE_PROFILE_EXHAUSTED`; do not silently truncate and then advertise complete
extraction. Local admission records unsupported objects as excluded, not indexed.
These numeric caps are a proposed first profile, not measured optimal settings.

The API permits a caller to construct FeatureSpecs from symbols and formal
shapes it already understands without knowing a target ModuleID. A conjunction
is sorted unique1..8FeatureIDs in one namespace. No disjunction, negation,
semantic unification or learned ranking is required for the first code slice.
Those can remain client-side candidate selection or separately versioned APIs.

## Immutable index structure and hot-key partitions

For each object, `partition = first byte of object_id`, an integer0..255. Thus
the256 disjoint intervals partition the whole256-bit ID space exactly. A hot
feature's entries are spread over these fixed ranges, not placed in one capped
posting list. These are index partitions; no particular peer owns a range.

Per(namespace,FeatureID,partition), maintain an append-only vector of ObjectRecords
having that feature. One object contributes at most one vector entry per feature.
Positions are zero-based insertion ordinals; do NOT assume ID-sorted leaves or
derive range nonmembership from unaudited sortedness claims. This avoids a
subtle false guarantee from an allegedly sorted Merkle tree.

Commit each vector by a length-bound padded binary Merkle tree:

```text
context = H(domain-context, {namespace,feature_id,partition})
leaf(i,R) = H(domain-leaf, context || u64be(i) || RecordID(R))
pad = H(domain-pad, context)
node(left,right) = H(domain-node, left || right)
vector_root = H(domain-vector, context || u64be(n) || tree_root)
```

Domains are respectively `DMKN-DISCOVERY-CONTEXT-V1`, `...LEAF-V1`, `...PAD-V1`,
`...NODE-V1`, `...VECTOR-V1`, each NUL terminated. Each digest is32bytes, n/i
are unsigned64 big-endian. For n=0 the tree root is the context-derived `pad`;
for n=1 the tree root is its sole leaf. For n>1 pad to the next power of two
with `pad`; derive padding-subtree hashes by height. The vector commitment
binds n; a membership path alone must not be used to authenticate its supplied
length. Its depth is `(max(1,n)-1).bit_length()`. Initial profile limits
n<=1048576 per vector; the configured store cap separately bounds features.

For one feature, commit the256 fixed-order partition descriptors
`{partition,count,tree_root}` in a256-leaf binary Merkle vector with separate
domains. The nonempty partition leaf is
`H('DMKN-DISCOVERY-PARTITION-LEAF-V1', context || vector_root)`, where vector_root
is recomputed from that descriptor. An empty descriptor must have count0 and
tree_root exactly equal to its context-derived PAD. After that validation its
leaf is the shared `H('DMKN-DISCOVERY-PARTITION-EMPTY-V1', empty bytes)`.
This empty-leaf optimization avoids256 unique stored empty leaves per feature;
an arbitrary claimed empty tree root is not permitted. Internal nodes use
`DMKN-DISCOVERY-PARTITION-NODE-V1` followed by left/right32byte digests.
A feature summary carries all256descriptors (bounded metadata), allowing the
consumer to recompute its root, sum counts, and identify zero/nonzero ranges
without trusting an unauthenticated occupancy bitmap. The root is `feature_root`.

An outer256-bit sparse Merkle map associates FeatureID with `feature_root`.
Key bits determine paths, most-significant first, not claimed sortedness.
The nonempty leaf uses `DMKN-DISCOVERY-MAP-LEAF-V1` followed by raw32FeatureID
and raw32feature_root. An absent leaf uses `DMKN-DISCOVERY-MAP-EMPTY-LEAF-V1`
followed by raw32namespace. Internal nodes use `DMKN-DISCOVERY-MAP-NODE-V1`
followed by unsigned16big-endian depth (root0 through255), left32 and right32.
Empty subtree hashes recurse from depth256. All domains terminate with NUL.
A proof has exactly256siblings root-to-leaf; vector/partition siblings are
leaf-to-root. Compression is a later wire optimization, not a prerequisite.

The content-addressed snapshot descriptor is:

```json
{
  "schema":"DMKN_FORMAL_INDEX_SNAPSHOT_V1",
  "namespace":"<digest>",
  "feature_schema":"DMKN_DECLARED_TYPE_FEATURES_V1",
  "partition_bits":8,
  "feature_map_root":"<digest>",
  "local_cut":42,
  "previous_snapshot":"<digest or null>",
  "coverage_claim":"PROVIDER_SELECTED_FEATURE_RECORDS_NOT_GLOBAL_CORPUS"
}
```

SnapshotID hashes this exact descriptor with `DMKN-FORMAL-INDEX-SNAPSHOT-V1`.
`previous_snapshot` is a history hint, not consensus or proof that two roots
extend one another. Clients do not replay that history to query the selected root.
An operational envelope may sign the SnapshotID with an owner Ed25519 key:
`{snapshot, snapshot_id, key_kind:'ed25519', public_key:<32bytehex>, signature:<64bytehex>}`.
Sign `DMKN-INDEX-SNAPSHOT-SIGNATURE-V1\0 || raw32byteSnapshotID`. Transport code
uses the adopted key implementation; pure snapshot code takes signature
verification as a separate boundary. A pinned SnapshotID is sufficient for
content authentication; a signature adds issuer binding, not content truth.

Snapshots are immutable. A serving replica can answer against the same root
without possessing the publisher's secret or sharing a cursor MAC. The selected
snapshot bytes, metadata/vector nodes and records must actually be retained for
service. A snapshot hash does not ensure its continuing availability.

## Storage and incremental build algorithm

First implementation is a fresh SQLite schema, not v4 DB migration:

```sql
objects(object_id PRIMARY KEY, record_id UNIQUE, record BLOB, admitted_seq)
postings(feature_id, partition, ordinal, object_id,
         PRIMARY KEY(feature_id,partition,ordinal),
         UNIQUE(feature_id,partition,object_id))
cas_nodes(hash PRIMARY KEY, encoded BLOB)
feature_heads(feature_id PRIMARY KEY, feature_root)
meta(id PRIMARY KEY, cfg, seq, maproot, latest,
     objects, postings, features, snapshots, logical)
snapshots(snapshot_id PRIMARY KEY, descriptor BLOB)
```

Store imported object bytes only long enough to run the pinned inspector and
extractor. Retain their content identity and derived record, not mandatory full
object custody. A separate custody node may retain/serve the object. An index
provider can also voluntarily be a custodian, but roles are not conflated.

One admission transaction: verify/extract before mutation; check object-ID
deduplication/conflict; reserve quotas; insert the record; append one posting
for each feature; copy-on-write affected vector paths; update the corresponding
eight-level partition-tree paths and256-level feature-map paths; commit all
heads/records/counters atomically. Duplicate identical admission is a no-op.
An ID with conflicting bytes/record refuses. Do not commit half the features.
Emit a new immutable snapshot only for an actually committed cut.

The persistent CAS shares untouched nodes between snapshots. Old nodes and
snapshot retention consume real disk. The first code slice may refuse new
snapshots on quota rather than implement unsafe deletion. A release-level
retention/GC policy must preserve all nodes reachable from retained snapshot
roots and active query leases; it is a separate explicit implementation step.
Root-count limits never excuse an unmetered CAS-node or database growth path.

No full index rebuild on every admission. If f is emitted feature count, L the
largest touched vector and B selected object bytes, work is
`O(inspect(B) + f*(log L + 8 + 256))` hash/path operations plus corresponding
indexed DB writes. Input Graph traversal is charged separately by node/edge
counts; B alone is not a bound on arbitrary mathematical evaluation because no
such evaluation is performed. SQLite transaction and storage costs remain real.
Bulk construction is the sum of these costs; an optional sorted bulk builder
must produce the same specified commitment, not a different unchecked layout.

## Query protocol and verifiable filtering

First pure operations:

```text
store.summary(snapshot_id, feature_ids[1..8], max_bytes=1048576)
  -> snapshot descriptor, feature-map proofs,256descriptors per feature
store.page(request)
  -> authenticated examined records, matches, next position, termination
verify_summary(expected_snapshot_id, namespace, features, response)
  -> verified summaries
verify_page(verified summaries, request, response) -> verified examined interval
```

For a given selected partition, choose the conjunct with minimum authenticated
count; tie-break by FeatureID byte order. If any conjunct is authenticated absent
or has count0 in that partition, the conjunction has no match there **relative
to the committed truthful index premise below**. Otherwise inspect the chosen
anchor vector in ordinal order. For every examined record, test set inclusion
`query_features <= record.features`.

The reply must include **all examined anchor records**, even nonmatches, and
each record's vector membership proof. Returned matches are a subset selected
by the client-recomputed predicate, not opaque provider filtering. Require
consecutive ordinals `[start,next)`, exact namespace/partition/anchor and record
shape; each record contains anchor and hashes to its RecordID. A skipped ordinal,
modified nonmatch, false match or changed root refuses. Each record's object ID
must be in the selected hash range. Distinct-object and immutable-record
consistency are checked for observed records; an unobserved global uniqueness
invariant still belongs to correct index construction, not membership alone.

Stop before consuming a matching record that would exceed output limits. Return
it at the same ordinal on the next page; never advance past an unreturned match.
Byte/work/time exhaustion similarly advances only through records included in
the authenticated reply. If even one record/proof cannot fit, return explicit
`PAGE_TOO_SMALL` with unchanged position. A zero-row page can be incomplete.
Budget exhaustion during preparation may return an explicit error before a
page exists. Exhaustion while examining records returns the previous verified
interval, possibly empty. On deadline expiry, produce no unauthenticated progress.
Server charged counters are bounded self-reported work, not cryptographic
measurements; client/outer supervision accounts actual received/elapsed costs.
The client preserves
its last verified cursor and charged resources, not a claimed server offset.

```json
{
  "schema":"DMKN_FORMAL_QUERY_CURSOR_V1",
  "snapshot_id":"<digest>",
  "query_id":"<canonical conjunction digest>",
  "partition":7,
  "anchor":"<FeatureID>",
  "next":32
}
```

The cursor is public data, not authority. Server and client validate it against
the selected snapshot and summaries. It needs no secret and may continue at a
different server serving the same root. A caller can deliberately start at32,
but cannot claim coverage of0..31 without retaining corresponding evidence.
The client aggregates verified intervals; only their union establishes coverage.
Changing conjuncts/snapshot/partition/anchor is not continuation of the old query.

Reply fields: schema,namespace,snapshot_id,query_id,partition,anchor,start,next,
anchor_count,examined[],match_ordinals[],next_cursor,termination,charged,
coverage=`COMMITTED_ANCHOR_INTERVAL_ONLY`, mathematical_acceptance=false.
`complete_partition` is true only when coverage assembled by the client includes
all ordinals0..anchor_count (or an authenticated zero-conjunct case), under the
truthful/cross-consistent index premise below. A single last page does not prove
the client saw earlier pages. Whole-snapshot conjunction coverage requires all
256partitions accounted for. Different providers' snapshots remain distinct
coverage domains; merging candidates does not merge them into a global snapshot.

### Exact guarantee and its premise

Unconditionally under collision resistance and valid proofs, the receiver gets
every committed record in the reported anchor interval and correctly filters
those records. This is the directly machine-checkable guarantee.

For an honest builder, each object record R is inserted exactly once in each
posting vector corresponding to its features and exactly one partition. Thus
for conjunct setQ and partitionp, choose any anchor a in Q. If Q is a subset of
R.features, then a is in R.features, so R occurs in the anchor vector forp.
Exhausting that vector and locally filtering therefore finds exactly all
qualifying indexed records in p. Disjoint exhaustive partition coverage extends
this result to the chosen snapshot. Choosing a minimum-count anchor changes
work, not the result. This is the query/partition completeness proof.

**The honest/cross-consistent build premise is not proved by Merkle membership.**
A malicious indexer can omit an object, lie about features, or maintain
inconsistent postings. Its signed roots do not eliminate these behaviors.
An authenticated zero count can therefore mean only an empty committed posting,
not absence of matching mathematics. The wire result must distinguish
`VERIFIED_COMMITTED_INTERVAL` from
`COMPLETE_FOR_CORRECTLY_BUILT_SELECTED_SNAPSHOT` and never assert the latter
without an explicit caller-adopted build assurance policy. After acquisition,
recompute features of each selected candidate before invoking existing proof
acceptance; this catches false positive features, not all omitted true positives.

First implementation requires honest-builder invariants, independent pure
construction tests and this honest labeling. Optional full snapshot audit can
recompute all source records/postings for a finite adopted source set; remote
proof of correct construction is a later separately justified relation. Do not
turn an attractive future SNARK into an implemented trust claim.

## Prospective bounds and query planning

Initial per-page ceilings:8conjuncts,32examined records,8matches,1MiB encoded
reply,16KiB request,1000ms server work. Summary replies have their own explicit
1MiB encoded-byte ceiling, including all256descriptors and256SMT siblings per
requested feature; this is not waived because summaries contain metadata.
The extraction input remains4MiB. Records are
at most16KiB; proof paths are at most20vector hashes plus separate summary
proofs. Enforce actual encoded byte limits before reply publication. External
CPU/memory/process supervision remains mandatory; a cooperative timestamp
check is not hard kernel isolation.

Initial per-workflow client ceilings are explicit owner inputs: providers,
snapshots,partitions,pages,candidates,received bytes,requests,wall/CPU budgets.
No automatic all-pages/all-providers loop. Candidate defaults may be small, but
the protocol must report each exhausted budget and unvisited partition. Usage
statistics may reorder independent candidates without altering coverage claims.

Summary work is O(d*(256+256)) hash/descriptor operations for d<=8; it is not an
M-object census. Page work is O(C*(log L+d+f_record)) for C examined leaves with
set construction/filtering charged, plus output bytes and indexed reads.
Matching Q results has unavoidable Omega(Q)output. A popular feature with no
selective conjunct can require all of its postings for complete selected-corpus
search; bounded refusal/incompleteness is an honest outcome, not cheap complete
semantic search. Provider counts/hints may guide planner choices but never
justify a completeness claim about providers not queried.

Fixed256ranges address a consequential hot-key storage and serving seam; they
do not create infinite capacity. Multiple serving replicas can host the same
snapshot/range. If a provider's selected catalog outgrows the profile, it admits
less, publishes multiple explicitly scoped snapshots, or adopts a new profile
with more partition bits. Repartitioning has explicit rebuild/placement costs;
no silent data loss or hidden migration of frozen snapshot IDs is allowed.
Uniform load is not an adversarial guarantee: an attacker can grind a chosen
8-bit hash prefix in about256 trials. Per-partition/store quotas and explicit
hot-range refusal remain required. The proposed4096-feature finite-test store cap
includes distinct per-type keys; it bounds one selected store, not the total
global vocabulary, and reaching it requires explicit refusal or another scoped
store rather than silently claiming universal indexing.

## Network and custody separation

New discovery protocol ID/schema must not masquerade as the v4 library `find`.
Operations are bounded summary/page/snapshot fetches only. Index servers do not
receive authority to offer objects into a client's custody or execute source.
Use the existing transport's framing, peer-policy and abort/containment discipline
through an explicitly selected successor adapter with its own larger byte caps.

Index-provider advertisements route by FeatureID/schema namespace and exact
SnapshotID. They are hints, not exhaustive service membership or custody leases.
The first network bridge can use configured independent peers and maintained
exact snapshot providers; feature-based DHT hints must preserve the declared
provider/query caps and incomplete status. No indispensable index owner is
required. A replica serving a pinned snapshot need not be its signer.

Query output identifies a canonical object, not an authoritative source host.
For named-definition-v1, hand the selected ModuleID to existing exact-ID provider
lookup/acquire-closure. Any compatible custodian can supply matching bytes.
Then recompute selected feature truth and perform existing local/certified
mathematical checking. An indexer disappearing does not invalidate acquired
mathematics; losing every snapshot server can still make that search unavailable.

Maintained advertisement, snapshot retention and object replication are separately
funded service obligations. Aggregate posting storage is at least r*f*M; update
service must exceed admitted indexed work plus renewal/repair work under the
stated load model. Queue stability alone does not supply worst-case latency.
Use the frozen SCALING-CONTRACT's reachability/coverage/load conditions, not an
unsupported Internet-scale theorem inferred from a local bound.

## Isolated implementation ownership proposal

Root adopted the pure implementation direction under D01. The one evolving
development source directory is `software/v5/discovery/`; immutable selected
source/evidence snapshots belong in later root-selected experiment directories.
Do not fork another complete source tree for each revision.

| Proposed file | Responsibility |
|---|---|
| `formal_features.py` | Pure canonical-object adapter and FeatureSpec/query compiler; no I/O/native/network authority. |
| `authenticated_index.py` | Domain-separated sparse map, fixed partition tree, length-bound ordinal vector proofs and snapshot identities. |
| `discovery_store.py` | New bounded SQLite schema, atomic admission, persistent nodes/snapshot retention and indexed serving. |
| `discovery_query.py` | Pure planner/client coverage accumulator and exact-ID handoff records, no automatic unbounded loop. |
| `test_authenticated_index.py` | Author-supplied primitive widths0..5, retained-root and mutation controls; not independent assurance. |
| `../tests/test_discovery_contract.py` | Root-owned independent synthetic-store/coverage and actual frozen-object adapter contracts. |

Suggested ownership: scale authors the four source components; assurance owns
independent invariant/source review and adversarial case requirements; a separate
test author may own tests when capacity is available. Root owns transport/public
integration, actual selections and any package successor. Do not ask a subagent
to rewrite the accepted v4 inspector or to rerun its unchanged pure contracts.

First code/test gate is finite and native-free: actual frozen canonical named
objects, independently checked expected feature sets, at least two conjuncts
with selective/nonselective order, data beyond page1 and several partitions,
membership corruption/omission/filter tampering, cursor portability, concurrent
new admissions with old snapshot retained, duplicate/conflict atomicity, quota
failure and explicit incomplete coverage. Exact observed feature-index counts
and hash/DB-work counters must distinguish query work from index-build work.
Use syntactic records for volume controls only with that label; do not call
synthetic rows mathematically valid knowledge or growth.

The decisive later vertical slice is two replaceable index providers and a
distinct surviving custodian; fresh consumer discovers an unknown-ID reusable
construction by formal conjunction, acquires/checks/uses it and returns a
substantive successor. Stop a publisher/index service and continue at another
server using the same snapshot where applicable. This adds a new discovery
boundary; it is not another rerun of v4's nine exact-type candidates.

## Readiness and unresolved implementation decisions

Root has selected authoring of the four pure files, but no runtime. Mandatory dependencies:
adopt exact v4 canonical inspector/codec/registry as read-only inputs; preserve
mathematical namespace separation; independently review Merkle encodings before
implementation use; choose concrete store quotas in the finite test selection.
No fresh cryptographic guest/proving campaign is required for this slice.

The main deliberate limitation is unaudited remote build truth: authenticated
pages expose committed search behavior, not honest source coverage. The first
implementation must make that limitation machine-visible. Broader semantic
features, full remote index-build proofs, adaptive repartitioning, GC, public
NAT/relay deployment and full-cost usefulness comparison remain separately
selected release work, not invisible assumptions or completion claims.

### Root-facing Python interface checkpoint

`formal_features.NamedModuleAdapter(library,codec,registry)` exposes namespace
and `extract(raw,expected_id=None)`. `feature_id(namespace,spec)` and
`compile_query(namespace,specs)` construct formal queries independently of target
IDs. `discovery_store.Store(root,adapter,limits,create=False)` exposes
`admit`, `snapshot`, `summary`, `page`, `close`. `discovery_query` exposes
`verify_summary`, `plan_partitions`, `verify_page` and a client-owned `Coverage`
interval accumulator. Adapters for later certified modules must have their own
format/policy/schema namespace and satisfy the same metadata interface; no v4
language bound defines the future module relation. Root owns integration tests.

### Authored source/checkpoint, before execution

All four source files and the primitive test file are authored. Root's separate
black-box `software/v5/tests/test_discovery_contract.py` was read completely;
its API calls match the implementation by source inspection. Neither this
statement nor the test sources claim a passing run. Root selects source pins,
finite launches and outcome adoption. Independent assurance owns source review.

Store limits are exact keys: max_objects (1..1000000), max_postings
(1..128000000), max_features (1..1048576), max_snapshots (1..1000001),
max_logical_bytes (1024..2**40), max_db_pages (256..268435456). An initial empty
snapshot consumes one snapshot slot and its descriptor bytes. Creation and
reopen bind namespace and all limits. Canonical record/CAS-node/snapshot bytes
are charged logically; SQLite max_page_count separately bounds physical table
and index overhead. The first version refuses quota exhaustion and retains all
snapshots; no GC/retention lease implementation is implied.

Admission's fixed cooperative limits are30seconds and500000CAS reads/writes
each. Summary's are5seconds and30000CAS reads plus max_bytes<=1MiB. Page
limits have exact keys examined (1..32), matches (1..8), bytes (1024..1048576),
timeout_ms (1..1000), node_reads (1..100000). Response counters disclose CAS
reads and examined rows, not every SQLite or CPU operation. Transport and
runtime containment must still supply hard wall/memory/received-byte bounds.
The ordinary-path guard uses Python3.13+'s os.path.isreserved on Windows.

Coverage keeps a private copy of the locally verified summary, validates every
page before merging intervals, and refuses conflicting observed object/ordinal
bindings. Report fields deliberately distinguish
complete_committed_anchor_domain from conditional_complete_if_correctly_built;
build_assurance is NOT_PROVIDED, global_complete is false and
mathematical_acceptance is false. A provider-created dictionary is not a locally
verified summary. The public network adapter must invoke verify_summary itself.

### Certified-module cross-lane mapping (next adapter, not implemented)

Mechanism's software/v5/modules/codec.py exposes a module summary with foundation,
policy, group_count and group_root. ModuleID identifies that whole summary.
Groups are ordinary singleton declarations or atomic inductive packages; each
descriptor binds structured relative Lean name, kind, universes, declared type,
value hash and computation metadata. The selected group opening contains the
summary, group index, group and Merkle siblings. Checking its binding is not
mathematical acceptance; the resolved module receipt remains necessary.

A module can export several unrelated declarations. Therefore index one record
per exported declaration, not the union of every export's features: union would
make a conjunction appear matched even when no single declaration satisfies it.
Use mechanism's exact `codec.export_id(module, relative_name)` helper for the
ExportID; it hashes domain export-address over `{module:ModuleID,name:Name}`
under framing DMKN-V5-MODULE followed by NUL. Do not invent a competing ID or
silently treat ExportID as a custody ModuleID. The acquisition locator is
`(ModuleID,groupIndex,relativeName)`; declared-type feature extraction must bind
the opened descriptor, optionally by codec.hash_value's declaration-descriptor
domain, without requiring all module bodies or all exports.

This requires an explicit new record/adapter version including that locator
and descriptor binding. The current V1 named-definition record remains unchanged
for its own tests. Root must select the new adapter after the actual module
format/checker boundary stabilizes; otherwise present source cannot be claimed
to discover the new certified module exports merely because both use hex IDs.
