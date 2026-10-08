# Next central integration: certified exchange and selective discovery

Source-based decision, `/root/contributor_plan`, 2026-09-29. **Proposal, not an
implemented protocol or runtime qualification.** No process, test, proof,
network service or product mutation was launched for this investigation.
Root's current collection proof, receiver intake and contributor qualification
remain prior gates. All used sources, failures and receipts remain unchanged.

## Decision in brief

Connect the certified contributor/receiver to an explicitly separate, indexed
peer lane. Its unit is the exact selected capsule plus its full collection
journal and receipt, not the native proof-closure package. A local agent must
be able to discover, acquire, independently verify, use and return a certified
result through public calls without root manually constructing a proof plan.

Do **not** label existing v2 remote enumeration a huge-network search design.
First add bounded exact-key remote lookup over persistent local postings and
content-addressed acquisition. Then compose this same request contract with
selective replicated key routing. The first integration can use configured
contacts; it qualifies only known-contact exchange. The large-network design
must additionally specify and test selective routing, shard maintenance and
availability. Neither step requires a globally ordered ledger, universal
latest head, central server, global task list or shared research objective.

The separation is important: proof certificates remove compulsory proof-history
replay, while an index/overlay removes compulsory corpus/peer enumeration.
Neither establishes useful discovery, cheap proving or useful growth by itself.

## What the inspected implementation actually provides

Frozen native baseline: `product-local/auxiliary-frontend-source-13`.
Certified contributor source: `product-local/certified-collection-contributor-source-04`.
Collection receiver/bundle source: `experiments/certified-collection-01/bundle`.
Their source existence is not evidence that all installed workflows passed.
Consult the current [research desk](../../NOW.md) for actual gates.

| Existing seam | Actual behavior | Consequence |
|---|---|---|
| Native `node.py:find`, `storage.py:page` | Local `(provider,symbol_key,sequence)` indexed range, bounded lookahead and cursor-bound snapshot; at most four reply rows | Reuse the operation-local indexing pattern, not a scan/rebuild helper |
| Native `symbol_index.py` | Keys encode exact external references in formal types; standalone helper `find` rebuilds its finite snapshot/postings | Its encoding is not the certified capsule format; standalone helper is not the integrated SQL lookup |
| Native `peer_node.py:find` | `peer_find` accepts only peer, snapshot, cursor; fetches the catalog root and one page, without a symbol predicate | Selecting one of many remote results can require enumerating that peer's advertised view |
| Native `peer_wire.py:load_view` | At service startup reads all selected pages and bundles | A larger limit alone would preserve a whole-view startup bottleneck |
| Native `peer_node.py:acquire/reuse` | Parses/rederives a native full package and compares exact closures; later separate native admission is required | This cannot be the certified lane's acquisition or acceptance implementation |
| Collection `cert_bundle.py` | Strict four-file BundleV2; exact selected member bound to a full DMKNJ003 journal; parsing/binding is not receipt verification | Preserve this framing/identity boundary; do not project a full receipt to a selected member |
| Contributor04 `prepare` / `advance` | Real immediate-parent receipt checks, body-free selected imports, ordinary local source, captured execution, bounded proof stages and final cold verification | Smallest producer seam exists in source; no public network/index/publish path is supplied by it |

The native limits are deliberately small: at most 8,192 local entries and 16
configured/added contacts; a remote view has at most 256 entries, 64 KiB root,
64 KiB/32-row pages, 8 MiB aggregate pages, 18 MiB per framed bundle and 64 MiB
aggregate bundle bytes. The service is finite and synchronous. These bounds
are safety envelopes, not evidence of huge-corpus or many-peer operation.

The current certified profile also has an explicit narrow envelope: one/two
outputs per parent collection, one child output, at most eight selected parent
interfaces, fixed support, Prop exports and no general new definition support.
Exact current interface identity includes declaration name, ordered universe
parameters and type. A renamed theorem can therefore have a new interface ID
without adding a new mathematical capability.

## Smallest coherent public loop

These are **proposed semantics/names**, not callable commands. Implement them
in a fresh explicitly selected successor/sidecar, preserving native v2 and used
certified sources. Prefer one documented facade over a second acceptance engine.

1. **`cert_offer(bundle)`**: inspect/bind an exact owned BundleV2 under an
   independently selected profile; register bounded immutable file pins and
   locally derived discovery keys. Advertise only an explicit owner-selected
   set, via incremental metadata insertion. Distinguish produced publication
   from exact-byte custody. An offer is not a receiver's acceptance decision.
2. **`cert_find(query, budget, scope)`**: query local indexed metadata or selected
   known peers. Return bounded untrusted descriptors, exact profile/interface/
   bundle identifiers, selected member, immutable query cut/cursor and explicit
   coverage/termination status. No proof/receipt blob is read merely to rank a
   row. No result may select an arbitrary filesystem path or bypass contact
   policy with a supplied endpoint.
3. **`cert_acquire(remote)`**: reserve bytes/work, fetch exactly the four files
   to a fresh quarantined location, validate lengths/hashes and strict BundleV2
   framing, then commit immutable custody atomically. Return a typed acquired
   handle, explicitly not a native context or verified theorem. Retries have
   exact request identity; interrupted input never becomes usable state.
4. **`cert_verify(acquired, adopted_policy)`**: perform the real local receipt
   check plus exact capsule/member/full-journal binding. Persist a typed local
   result keyed by all relevant profile and content pins, not a peer's success
   label. A wrong checker/foundation/image, unresolved premise or malformed
   receipt refuses. Acceptance remains under the experimental checker's stated
   Lean-correspondence/cryptographic assumptions, not native Lean admission.
5. **`cert_preparecontribute(source, root, selected_handles, budget)`**: resolve
   exact stored parent bundles into the installed public contributor's
   `prepare`, which still performs its specified real checks. Snapshot only
   immediate selected capsules/full receipts; do not hydrate ancestry. Local
   source is owner-authorized executable code, never arbitrary peer code.
6. **`cert_advance(operation, stage_budget)`**: delegate to that same operation's
   public bounded continuation. READY, failure and actual completion stay
   distinct. Only actual final receipt and cold verification yield an offered
   child bundle; do not publish intermediate proof checkpoints as certificates.
7. **Return**: another independent local node finds/acquires/verifies the exact
   child through the same path. A surviving custody holder can supply identical
   bytes after the original producer stops; it does not invent another theorem
   or borrow the producer's acceptance state.

Initially the facade may retain conservative repeated parent verification;
removing it is not necessary to integrate the loop and needs a separate safe
cache contract. Share identical journal/receipt blobs across selected siblings
in custody storage, but do not rewrite their exact manifests or claim receipt
normalization. Equality of journal bytes alone is insufficient authority to
replace differing receipt bytes in the currently selected contributor API.

## Exact metadata and query boundary

Use a new tagged discovery domain. Do not reinterpret native raw-reference hex
keys or current named interface IDs as interchangeable semantic identities.
An offer descriptor should bind:

```text
wire/profile version; foundation; relation/image/policy identifier;
exact bundle ID; selected interface ID; member index;
full journal/receipt/capsule lengths and hashes; finite derived feature keys;
holder/contact reference; local immutable advertisement cut
```

Locally adopted verifier code/parameters remain independent policy, not content
authorized by a remote descriptor. Holder/lease fields describe service and are
not mathematical authority. An index may advertise a replica it cannot currently
serve; the receiver reports this as unavailable, not an invalid theorem.

First keys: exact interface ID, exact bundle ID, and exact fixed-foundation
constant-occurrence keys derived from the capsule's canonical type. In the
present fixed profile, foundation plus the capsule's constant-name hash gives
an unambiguous reference to that adopted baseline, but a name hash alone does
not identify an arbitrary future definition. Future extensible profiles must
use authenticated semantic declaration identities; see
[next vocabulary](SCALE-NEXT-VOCABULARY.md).

Minimum query language: one exact key, an optional bounded conjunction of keys,
explicit compatible profile, row/byte/visited-posting/time budgets and snapshot
cursor. Single-key range lookup is the first implementation; conjunction picks
one bounded selective posting stream and tests the other keys on each candidate.
Statistics can choose a poor driving key, so work must stop at a **scanned-row**
budget, not merely an output-row limit. Report incomplete even if few rows pass.
No universal semantic theorem-search completeness is promised.

Recommended persistent tables are typed bundle/custody records, immutable
advertisement versions, `(scope,profile,key,sequence)` postings and exact local
acceptance records. Publication adds only its own finite postings. An immutable
query cut plus next sequence bounds pagination across concurrent insertion;
withdrawals/expiry need versioned visibility or an explicit stale-cursor refusal,
not silent changes to a previously pinned cut. Resource reclamation may expire
old cuts; no promise to retain every historical query snapshot forever.

For `n_s` locally selected shard entries, an ordinary B-tree lookup should visit
index paths and at most `s` scanned candidates plus `r` returned records, rather
than decode all `n_s` entries. Per-record primary-key lookups may each cost an
additional `O(log n_s)`; do not claim `O(log n_s+r)` without a covering-layout/
query-plan justification. Hard byte/work limits and instrumented actual reads
matter more than an informal asymptotic label. Server startup authenticates its
small configuration/index root, not every stored receipt/blob; a selected fetch
rechecks the selected exact file pins. Database rebuild/audit is a separate,
explicit maintenance operation, never hidden in every query or service start.

## Large-network routing: selective, conditional and not implemented

Use independently operated replicated **key rendezvous shards** as the next
architectural candidate, not a mandatory blockchain. A structured overlay
locates responsible index shards for `H(profile,feature_key,shard_prefix)`;
their bounded postings name exact candidates/holders. Mathematical blobs remain
with producers, caches and voluntary custodians. A participant may be a client,
holder, index/router or several of these; nobody must store all results/peers.

This must be an explicit successor to v2's 16 owner contacts. An implementation
can start with a finite owner-authorized overlay membership/configuration and
later add bounded admission/churn. It must not claim permissionless global
routing while actually needing manually configured edges to every holder.
Operational endpoint identity is needed for transport and quota accounting;
political attribution/reputation is not needed for mathematical soundness.

Assumptions for a useful routing/liveness statement:

- The query enters a connected supported overlay and enough chosen replicas
  are honest, reachable and retain the selected shard/holder advertisements.
- Routing tables stabilize sufficiently relative to churn; message delivery
  and remote work fit the declared timeout/budget. No synchrony assumption is
  silently used to promise a globally current view.
- The chosen key/partition scheme is actually advertised by relevant suppliers,
  and at least one reachable holder retains the exact requested bytes.
- Membership, endpoint authentication and resource policy bound cheap flooding;
  arbitrary Sybil/eclipse resistance is not obtained from theorem receipts.

Under standard well-maintained balanced structured-overlay assumptions,
exact-key lookup can have logarithmic expected routing hops in peer count.
That is a conditional algorithmic target, not a proven bound for this product
or arbitrary adversarial/asynchronous networks. Each request instead has hard
finite budgets: at most `h` hops, `f` parallel/replica branches, `b` bytes, `s`
postings examined, `r` candidates and a deadline. Deduplicate visited query/node
pairs and decrement the forwarded budget; cycles cannot restart it. The caller
never falls back to contacting all peers when the budget runs out.

The result distinguishes `complete_for_selected_shard_cut`, `budget_exhausted`,
`unavailable`, `unsupported` and `routing_incomplete`. An empty partial result
does not mean no theorem exists. Even authenticated absence from every selected
shard proves nothing about unadvertised/offline knowledge or another partition.
Local result checking does not require believing a route's recall claim.

### Common keys, hotspots and skew

A key such as equality can have a huge posting list even with perfect routing.
Hashing only that key moves the hotspot; it does not solve it. Split overloaded
posting lists by a stable prefix of candidate ID and replicate hot read shards.
A small versioned directory identifies the active prefix partition; when this
directory itself grows, route prefixes through bounded tree pages. Advertise
new entries incrementally, recording per-entry/per-key maintenance cost.

A generic query must **not** fan out to every prefix. It chooses bounded shards
or refines with a more discriminating conjunction/structural feature and reports
incomplete coverage. Popular-key top-k summaries/reservoir samples can cheaply
offer candidates, but their rank and coverage are heuristic. Results should
include a diversity/exploration allowance so stale popularity is not the only
access path. Remote shard splits, replica changes and failures require bounded
version redirects; no unbounded retry/redirect chain is allowed.

Fairness/quota/backpressure prevent one expensive feature from monopolizing a
node. Index replication, refresh and repair use bounded owner-funded maintenance
budgets and appear in the cost ledger; they are not free background work.
Network-wide metadata necessarily scales with retained advertisements and their
chosen replication factor. The requirement is **no compulsory global per-node
copy or per-query scan**, not zero aggregate indexing/storage cost.

### Availability and changes

Receipts establish the selected relation, not custody. Use finite expiring holder
advertisements and more than one independently selected holder where possible;
missing data triggers a bounded alternative lookup. Expiry is local service
metadata, not revocation of a theorem. Exact immutable descriptors can remain
valid while unavailable. Interface/certificate availability is distinct from
optional proof archives needed for audit or future checker migration.

Partitions allow independent valid contributions and partial local indices.
On reconnection, merge content-addressed offers and bounded index updates, not
one total order of all proofs. Different foundations/profiles coexist in typed
namespaces; a supported-profile query does not silently translate results.
The resulting software gives access to a distributed body of knowledge, not
every participant instantaneous awareness of that body's complete status.

## Deduplication and usefulness without changing truth

Maintain three distinct identities:

1. Exact bundle identity for transport/custody, including certificate bytes.
2. Exact certified interface identity for mathematical reliance under its
   profile. Current names remain part of this identity.
3. Optional **discovery-only statement fingerprint** for grouping alternatives.

An initial conservative fingerprint can omit only the exported declaration name
from the already decoded interface while retaining foundation, ordered universe
parameters, exact canonical type and referenced meanings. This catches some
renamed copies, not all alpha-equivalent universe encodings. A later explicitly
versioned alpha-normalized fingerprint must normalize bound term/universe names
consistently, preserve universe constraints and external semantic references,
and avoid unbounded reduction. It is a separate index feature, not permission
to edit a certified capsule or replace a selected receipt/interface.

Keep alternative exact results retrievable even when displayed as one group.
Syntactic grouping is not a decision procedure for mathematical equivalence;
different statements may expose the same useful capability, and syntactically
different formulations may be valuable. Heuristic embedding/LLM ranks, local
usage frequency, witnessed downstream reuse, byte cost and successful-find
history may guide a bounded candidate set. None may authorize acceptance or
make popularity the only retention path. Usage can be inflated, is task-biased
and is not proof of causal benefit; selected-profile verification is unchanged.

## Changes and tests that decide the next implementation

| Fresh seam | Required change | Decisive changed-boundary test |
|---|---|---|
| Wire/storage | New explicit certified family, four exact payload routes/framing, inert custody and typed records | Native/certified format confusion, forged member/profile/pins, extra/missing file and interrupted transfer refuse without accepted state |
| Local/remote index | Capsule-derived typed keys; persistent postings; predicate/cut/budget-bound request and cursor | Unrelated-corpus expansion does not read unrelated capsules/receipts; sparse/overfull/common-key queries stop at scanned-row/byte limits |
| Service | Index-backed bounded lookup and exact on-demand blobs, no whole-store `load_view` | Startup/query works with unrelated blob inaccessible; selected corrupt/missing blob refuses or reports unavailable |
| Public facade | Acquired/verified/contributor/completed handles remain distinct; real installed workflow delegation | READY or fake completion cannot publish a certified child; parent verified before native use; only final exact receipt accepted downstream |
| Custody/return | Exact byte preservation and bounded independent holder selection | Original producer off; second holder supplies exact child; fresh receiver independently verifies; no imported local acceptance |
| Later router | Typed selective key routing, finite budgets, prefix/replica maintenance | Route loop, churn, stale shard map, hotspot, unsupported profile and partition cannot force all-peer fanout or false global completeness |

Qualify the actual certified public contributor first. Then one same-host
multi-process reciprocal TLS integration should reuse that qualified parent and
produce the **one genuinely new downstream child needed by the API test**.
Do not repeat old proof campaigns just to make transport fixtures. Inert large
metadata/noise fixtures can test access locality and routing failures cheaply,
but must be labeled synthetic and cannot become mathematical growth evidence.
Independent-host operation remains a distinct, later qualification.

Keep immediate and later gates separate: known-contact public exchange is not
overlay qualification; a router simulation is not a real deployed giant network;
a conditional asymptotic argument is not measured whole-workflow speedup.

## How this can justify useful growth

Reuse [GROWTH-DESIGN](GROWTH-DESIGN.md)'s resource-sensitive criterion, but do not
run the old native-only paused workload as if it tested the new certified lane.
Predeclare fresh matched downstream endpoints expressible in the selected
certified profile. Independent consumers receive the same task/interface/model
budgets; treatment can discover the contributed results, baseline has the same
foundation and permitted local library without those results. Prevent accidental
seed leakage through a common package and disclose procedural independence.

Primary observations: actual independently completed, locally verified reusable
endpoints per declared resource allowance, plus capped effort to completion and
failure counts. Charge seed production/certification once, search/index/routing
maintenance, transfer, cold verification, authoring, new proof production and
return acceptance; retain CPU, elapsed time, tokens, bytes and memory separately.
Report both cold and amortized use, failures and the reuse count at which any
measured one-time certification investment breaks even. If it never does within
the tested regime, say so.

New bundle IDs, named duplicates, dependency edges and trace-row savings are not
new useful outcomes. A positive small comparison supports only those tasks and
that operating regime. Sustained/exponential growth needs broader longitudinal
evidence and a resource-supply model; it does not follow from a recursive proof,
a growing index, the hypergraph description or a completed reciprocal example.

## Architectural contract versus outstanding evidence

For a chosen operation, let `H` be ancestral witness bytes, `N` the unrelated
corpus, `P` peer count, `I` selected exact interface/allowed semantic-data bytes,
`C` selected receipt bytes, `Q` actually traversed query metadata, and `W_new`
the new local proof/checking/proving work. The proposed receiving path reads
`O(I+C+Q)` bytes and does local parse/hash/receipt verification; contribution
adds `W_new` and immediate-parent certificate composition. Neither operation
may have a compulsory linear `H`, `N` or `P` term. `Q` is finite and explicitly
budgeted, not asserted constant or globally complete. Large selected statements,
large fan-in, demanded computation and actual new proving still cost real work.

This is a design contract, conditional on the checker/import/certificate
assumptions and actual implementations satisfying their access boundaries.
Current evidence must separately establish real receipt verification, actual
public contributor completion, exact-byte peer integration, indexed access,
selective routing, supported semantics and useful-growth benefit. This note
closes none of those runtime gates. The immediate decision is to integrate the
existing certified boundary with indexed exchange; general definitions and
elaborate global ranking remain later work unless a selected endpoint makes
them the next concrete blocker.

## Source references inspected

- `product-local/auxiliary-frontend-source-13/API.md`, `PEER.md`.
- Same source `py/node.py:295`, `py/storage.py:29`, `py/storage.py:177`,
  `py/storage.py:731`, `py/storage.py:750`: integrated selective local lookup.
- Same source `py/peer_node.py:182`, `py/peer_node.py:226`,
  `py/peer_node.py:273`, `py/peer_node.py:487`: remote enumeration, full-package
  acquisition/reuse and separate inert commit semantics.
- Same source `py/peer_wire.py:474`, `py/peer_service.py:476`: whole-view startup
  authentication and exact catalog/page fetch.
- Contributor04 `cert_capsule.py:221`, `cert_bundle.py:73`,
  `cert_bundle.py:145`, `cert_workflow.py:333`, `CONTRIBUTOR-API.md`:
  exact named interfaces, selected-member/full-journal binding, real grouped
  parent verification and current public producer boundary.
- [Scale dataflow](SCALE-DATAFLOW.md), [scale design](SCALE-DESIGN.md),
  [growth criterion](GROWTH-DESIGN.md) and
  [minimal definition decision](../../../experiments/certified-collection-01/NEXT-DEFINITION-IMPLEMENTATION-DECISION.md).
