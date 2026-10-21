# Selective placement: bounded custody with query-derived reachability

2026-10-21. core_release. **Source-only design; implementation not selected.**

Authoritative input: `experiments/v5-local-checks/distribution-terminal-i-01-input.json`,
SHA-256 `d3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0`
(114 logical SDK sources). Physical sources below are resolved through that map.
No product imports, tests, proofs, builds, network operations or Git mutations
were performed. The already solved exact-body-supplier gap is not reopened.

Revision after independent `SELECTIVE-PLACEMENT-REVIEW.md` SHA-256
`0997105bbc6721dc95757530a6c0d6487494ac4d773897e17c6e0411ac344b7f`:
the original unexecuted draft hash was
`59ecc15abf6a2e7197fd83927794f5872637387042a2d00c4d0ecde34be2d3be`.
This revision clarifies restart/status authority, the existing V1 two-endpoint
locator mode, the selected located-query source, offline exact-custody reuse,
future-only horizons, both index COMMIT guards and the bounded TLS token
envelope. It does not expand the design or select implementation/runtime.

## Decision and concrete value

**GO for review of a narrow, capability-gated pull-placement seam.** Do not
implement an adaptive shard directory, new proof protocol, universal custodian
market, or replacement authenticated index.

A publisher should be able to ask an independently owned custodian to retain a
selected export and its exact evidence, obtain a durable operational receipt,
and stop serving. A later reader, knowing a formal goal but neither the export
ID nor the publisher, should find the custodian through a deterministic formal
feature route. The custodian must not run the publisher's source or decide
whether its claimed mathematics is true. Existing receiver-side acceptance
remains mandatory.

The present local publication reports `remote_placement_confirmed=False`.
Existing transport can retrieve and custody exact groups/evidence; `Store.admit`
can index their derived metadata; maintained location can advertise routes.
What is missing is the operator-authorized composition of those capabilities
into an independently acknowledged placement, including finite retention and
query reachability. This contract supplies that composition.

The simpler alternative is an operator manually acquiring selected bytes,
calling structural indexing and configuring routes. It establishes feasibility
but does not let ordinary publishers obtain a checked placement outcome without
private state intervention. The proposed seam automates that exact workflow,
not arbitrary remote code or mathematical admission. Availability and reduced
manual coordination are its immediate payoff; net useful-growth benefit does
not follow merely from implementing it.

## Small supported query class

Use the already implemented **conclusion-fingerprint profile**, not a new
feature language. A deployment selects one exact profile with at most three
bounded syntactic paths. The namespace already binds this profile, foundation,
semantic policy and feature schema.

For export e, let f(e) be the single conclusion-fingerprint feature derived by
the existing `ModuleExportAdapter.describe` from its authenticated opening.
Its placement cell is

    cell(e) = route_key(namespace, [f(e)], stripe=0).

The publisher may propose f(e), but the custodian independently derives it.
Publisher-supplied feature lists are never authoritative. No ExportID prefix,
provider choice, packet hash, lease or human topic label determines this cell.

For a closed formal goal g, the existing `goal_queries` returns at most eight
singleton alternatives. Let K(g) contain their corresponding cells. These are
OR alternatives, not one conjunction. An optional additional conjunct filters
candidates inside a queried cell. The primary fingerprint remains in the actual
compiled query. The present located-query implementation already permits a
route predicate that is a subset of the actual query's features.

The supported recall argument is deliberately syntactic. Consider application
of a declaration after instantiating its outer telescope. At every selected
path, require either that the source encounters an instantiated parameter
(its token is STAR), or that the source and goal preserve the same observable
node/symbol/local-variable token. There must be no reduction, unfolding,
rewriting or implicit coercion that changes the observed structure. Under these
conditions the source fingerprint is among `goal_queries(g)`: each coordinate
is either the observed goal token or STAR, and the routine enumerates those
choices. Hence cell(e) belongs to K(g). Context goals use the existing explicitly
closed telescope wrapper and exact `context_binders`; that is not an inferred
unification context.

This is a supported candidate-filter class, not full Lean elaboration,
unification, equivalence or a theorem-applicability decision. Candidates still
need structural resolution, real proof acceptance, and discharge of their
remaining premises. Unsupported or unselective queries can use other existing
local/provider methods; this placement mode must not silently claim their
coverage. Pair-profile compilation is a separate namespace and is not mixed
into this first mode.

## What a custodian owns

Each custodian is an independent operator, not the unique owner of a cell.
Multiple custodians may hold different subsets or replicas of the same cell.
No consensus, globally elected cell leader, or complete cell-membership list is
required. An operator configures:

- One exact namespace/wire profile, finite store quotas, and at most L live
  advertised cells over all of its active generations.
- At most G=2 simultaneous storage generations, with separate ordinary
  workspace roots and fixed HTTP endpoint slots. Both count against its total
  disk and service budgets; G is not increased to bypass exhaustion.
- Fixed generation admission-close and retirement times, plus finite service
  deadlines. A generation has no promise of perpetual storage.
- Finite capability grants for publishers, aggregate intake/pull/index/route
  budgets, and a separate allowance for existing read service and cleanup.
- Owner-selected egress rules and accepted source endpoints. Remote requests
  cannot choose CA files, executables, trust adoptions, directories or budgets.

Reuse `Workspace.open` for its immutable configuration and exclusive owner
lock, `ModuleStore`, typed `PacketStore`, the existing adapter and `Store`.
Do not construct mathematical issuer/receiver/preparation objects for placement.
The structural acquisition class already refuses a verifier argument.

The local operation-grant pattern is reusable, but an existing `CommonsClient`
mathematical grant must not be forged or its JSON deserialized into authority.
Introduce one exact, locally issued **placement service grant** with the
workspace/endpoint/deadline bindings and finite counters needed here. It is
not a mathematical warrant. Remote bearer tokens are references to portions of
that owner-granted intake budget, never arbitrary persisted owner objects.

## Bootstrap without a global directory

Separate two bootstraps that serve different purposes:

1. Ordinary DHT bootstrap peers connect a reader to the overlay. They do not
   select, own or certify mathematics. Owners may configure several independent
   peers and change them through the existing local policy.
2. A publisher has a bounded set of **placement contacts plus grants** issued
   by willing custodian operators. These can be configured directly, exchanged
   between collaborators, or retained from earlier successful placements. They
   need not contain the new cell already. A valid grant may allow creation of
   new cells up to its cell cap. Thus a new mathematical fingerprint does not
   require finding an already populated index or creating a central directory.

A publisher may try an existing-cell custodian returned by bounded rendezvous
only if it already has a valid grant for that endpoint, or obtains a separate
owner-approved grant. Discovery of an endpoint is not write permission. If no
willing contact is available, the result is `NO_AUTHORIZED_CUSTODIAN`; local
publication remains usable and no remote-placement claim is made.

This is a realistic explicitly seeded federation, not permission from one
central institution: anyone may run a custodian and issue its own grants, and
no particular operator is essential. Readers do not need publishing grants or
knowledge of the publisher/custodian. Automatic public grant vending/funding is
not secretly provided by the DHT. It is optional later operator policy, not a
prerequisite for this bounded feature. A claim of effortless permissionless
storage for arbitrary strangers would be false for this initial contract.

## Intake: small requests, existing bounded pulls

Use a new closed placement route, not a general write switch on current read
routes. An intake manifest is at most the existing 16 KiB request ceiling and
names one export, one exact evidence packet, and optionally a small explicit
list of selected committed bodies. It contains the exact namespace/profile,
module/name/ExportID, proposed primary fingerprint, group-opening size/hash,
packet size/hash, selected body addresses/ceilings, and requested retention end.
The source endpoint comes from the grant; it is not followed from a downloaded
object or an arbitrary URL in the manifest. Content identifiers are validated
before any disk/network effect. Bodies outside the selected opening are not
recursively chased by intake.

An owner-issued random bearer token references a stored, hashed-token grant.
The grant binds its service epoch, source endpoint, namespace/profile, expiry,
retention ceiling, permitted placement count/new cells and total resource caps.
It may authorize a finite stream of contributions without a human approving
every theorem. Store only the token hash in durable state; redact tokens from
reports and logs. TLS is mandatory outside the explicit loopback test mode.
A token is storage permission, not identity, attribution or mathematical trust.

The persistent service epoch identifies an operator/configuration/credential
domain; it is distinct from each fresh local runtime service grant and its
monotonic deadline. After restart or write expiry, old tokens are **status-only**
while their generation's bounded ledger remains retained. They can retrieve an
existing exact outcome but cannot authorize any new submission, pull, commit,
route dispatch or retention renewal. The first slice has no old-token new-write
readoption API. Restart always requires fresh explicit local service authority.

This is HTTP TLS, not an inference from libp2p Noise encryption. The retained
data-plane exchange uses `ssl.create_default_context`, certificate/hostname
validation and TLS >= 1.2; endpoint/CA options are locally adopted. The new
placement client must preserve those checks, including a matching IP SAN when
the selected endpoint is a numeric address. Never transmit a bearer token over
arbitrary plaintext HTTP, accept a downloaded CA, or disable verification to
make a deployment work. The current read-only service does not automatically
authorize exposing this new intake route. No independently deployed public-TLS
test is claimed here. If a deployment has no usable owner-adopted authenticated
TLS endpoint, its safe first mode is **owner-local pull initiation** of the same
manifest/commit workflow; remote capability submission stays disabled. A
rendezvous descriptor alone does not satisfy this prerequisite.
The token belongs in the closed bounded request envelope on that new route;
do not assume the current HTTP header allowlist supports Authorization or
weaken unrelated read-route framing to add it.

Two small request operations suffice:

- `submit`: authenticate the token; reserve the exact manifest under the grant;
  return the existing result for an identical request, or perform the bounded
  pull/commit sequence. A busy intake slot returns `BUSY`, not an unbounded
  in-memory queue. A request/operation timeout can leave an uncertain result.
- `status`: authenticate the same grant and exact request ID; return its
  bounded durable outcome without executing a retry or renewing a lease.

For identical existing requests, `submit` is also observation-only, even when
the saved phase is incomplete. After write expiry/restart this observation may
still succeed, but fresh work is refused. Explicit owner reconciliation, not a
duplicate remote request, is the only way to finish an interrupted placement.

The request ID hashes the exact canonical manifest, grant identifier and
generation identity. Altering a manifest under a claimed ID refuses. Retrying
an identical request never adds a ledger row, performs acquisition/commit work,
replenishes allowance or extends its original retention end. A genuinely
new attempt needs remaining owner-granted budget and is explicitly distinguishable.
Unauthenticated/malformed requests receive no durable intake row; their network
processing still consumes finite ingress limits. This does not solve public
denial of service or guarantee fair access under Sybil flooding.

The sequence is:

1. Validate grant/policy/horizon and reserve finite incoming/outgoing bytes,
   requests, structural work, disk headroom, ledger rows, possible new cell and
   advertisement work **before** pulling. Persist the reservation.
2. First check bounded existing exact custody where available; otherwise pull
   the named declaration through existing structural acquisition. Verify its
   exact size/hash/ExportID, recompute the fingerprint and compare the cell.
   Any pull uses only the fixed source contact and original deadline.
3. An exact local packet commitment/readback can satisfy custody without a
   remote offer, including during explicit reconciliation after the source
   disappears. A saved phase alone cannot do so; corruption is refusal, not a
   cache miss. If a remote packet acquisition is needed, use the existing
   evidence-offer check followed by exact acquisition. The packet must actually
   appear in that bounded source offer. Absence yields `PACKET_NOT_OFFERED`, not
   an invented offer or unlimited variant scan. Bound `max_offers` explicitly.
4. Store and read back the group and packet with their existing validators;
   require packet target summary = authenticated opening summary. Retain only
   the explicitly selected bodies, using existing commitment validators. An
   unsupported proof form or bad commitment is refusal; a structurally valid
   but false proof can be retained and is still untrusted.
5. Encode the export opening and call incremental `Store.admit`. Read back the
   admitted record/snapshot identity. No proofs are executed and no acceptance
   token is created. Persist the exact bounded placement outcome.
6. Record/dispatch the cell's existing stripe-0 route intent. Distinguish actual
   retained/indexed success, local advertisement intent, and the existing
   `HINT_DISPATCHED_UNACKNOWLEDGED` outcome. DHT publication is not a replicated
   custody acknowledgement or a proof that any reader can currently find it.

Reuse the direct, structural `EvidenceAcquisition` path, not a fake search
candidate or fabricated live contact. Its offer/packet/declaration/body methods
already bind exact bytes and custody. The new owner must still enforce endpoint
policy before every dial and reserve all requests in its original envelope.
The existing `AcquisitionBudget` has positive verification-limit fields; those
fields do not authorize verification in this service. Do not instantiate a
verifier or count a nonzero configured ceiling as work performed.

### Deduplication and accounting

One packet may warrant many exports. Packet identity/storage is already
content-addressed; repeated exact packet/group custody is idempotent. Charge
network bytes only when actually fetched (unknown tails conservatively), and
disk by actual new packet/group/body bytes plus new metadata/index/ledger costs.
On a duplicate, first perform the bounded exact existing-custody readback and
skip the network pull when it matches the complete requested commitment. Do
not require a novel full packet copy per export or subtract its cost from the
first placement. Structural readback/parse and every request remain charged.

For a set of placements in one generation, packet storage is the sum over
distinct retained packet hashes, not the sum of packet sizes over exports.
Separate generations can hold two copies during rollover; charge both. Avoid
a cross-generation shared-blob reference-counting subsystem in the first seam.
Capacity reservations must cover worst-case index nodes/history as well as
payload bytes. A safe over-reservation is preferable to an unbounded expansion;
actual accepted-operation reports should distinguish reserved from actual cost.

## Receipt and crash semantics

The receipt binds custodian endpoint/service epoch, request and generation ID,
namespace/profile/cell, exact export/record/snapshot, retained packet and selected
group/body commitments, retention end, current service end, all charged/reserved
dimensions, phase and route outcome. It always states:

    mathematical_acceptance = false
    global_complete = false
    cross_database_atomic = false
    all_future_bodies_covered = false

It is an authenticated endpoint's operational acknowledgement, not a detached
cryptographic storage proof, quorum certificate, guarantee of future uptime or
transferable mathematical warrant. Independently fetching an authenticated page
can verify inclusion in its committed index; neither that proof nor a read-back
establishes future availability. Do not add a new cryptographic receipt system.

Keep three evidence levels distinct in the client result:

| Level | What the client actually knows |
|---|---|
| `PEER_ACKNOWLEDGED` | The authenticated endpoint made the exact bounded custody/index/retention claims. The client checks all expected manifest/profile/cell bindings against its own independently derived record; this does not validate the peer's claimed readbacks. |
| `CURRENT_READBACK_AND_INDEX_VERIFIED` | The client additionally fetched and checked the selected retained commitments and a valid existing authenticated index inclusion at the named cut, charging those extra bytes and work. An ACK containing a root hash alone is insufficient. |
| Future retention | An operator promise under its fault, funding, clock and service assumptions; never upgraded to observed durability through a future horizon by either of the preceding levels. |

The second level can reuse existing authenticated summary/page proofs when a
selected interval contains the expected record; a direct bounded inclusion
helper, if added, must use the same posting/snapshot commitments rather than
an unauthenticated database lookup. It is optional additional evidence, not a
reason to re-download every large packet for each metadata export. Neither
level proves complete feature extraction over the provider's claimed corpus,
global coverage, independent replicas, or mathematical truth.

Use explicit phases such as `RESERVED`, `PULLING`, `CUSTODIED`, `INDEXED`,
`RECEIPT_COMMITTED`, with a separate route facet. `INDEXED_UNADVERTISED` is useful
partial success but not completed located placement. The publisher preserves
its source until the outcome it requires is observed; it must not treat a lost
HTTP response as a negative result or automatically retry with fresh funding.

Existing stores use separate SQLite transactions. A crash may leave retained
bytes, or an indexed row, before the receipt ledger is updated. That partial
state is preserved and its conservative reservation stays charged. No global
rollback is invented. A bounded owner-authorized reconciliation reads the exact
stored commitments and finishes idempotently, or reports incomplete/uncertain.
It uses fresh local execution authority but preserves the original placement's
reservations, remaining allowance and retention end; it cannot restart a retired
write grant, replenish funding or manufacture an ACK from a DHT hint.
Malformed proof bytes can consume granted structural custody but cannot obtain
mathematical authority. Such storage pollution is bounded by capability and
operator quotas, not solved by a new universal usefulness oracle.

## Retention and sustainable bounded generations

**A finite ACK is not sustainable storage by itself.** The existing immutable
index has no deletion/GC; its historical nodes and cuts count toward quotas.
Therefore the operational contract needs bounded whole-generation retirement,
not an assumption that expired individual rows disappear.

For generation j, owner configuration fixes admission close A_j and retirement
not-before T_j, with A_j <= T_j. An accepted retention end u must satisfy
now < A_j and now < u <= T_j, within the token's permitted horizon; a past or
too-long requested end returns `HORIZON_NOT_SUPPORTED`.
The operator may retain data longer but cannot promise more by extending a
duplicate request. Existing store caps are never enlarged by incoming demand.
Generation sequences increase and configured retirement times are
nondecreasing, so the durable retired floor can advance without hiding an
older still-live generation.

A generation moves through:

    OPEN -> SEALED_SERVING -> RETIRED

`SEALED_SERVING` refuses new placements but keeps all its retained cuts,
packets/groups/bodies and routes available under its current service grant.
Sealing can happen at A_j or capacity exhaustion. It does not withdraw earlier
ACKs. A second pre-budgeted generation can open for new arrivals while the
first continues serving. If both slots are occupied, refuse new storage rather
than adding a third store, expiring promises early or silently evicting records.

Each live generation has a distinct fixed endpoint slot serving its own real
Store and custody. Select the existing **V1 index-only maintained locator**,
which permits up to four endpoints; use at most two. Body-enabled V2 explicitly
requires one endpoint and is not the two-slot mode. Direct group/body HTTP
custody still works, and independently selected V2 body-location roles remain
separate. This placement mode makes no new body-route-advertisement claim.
The V1 locator advertises the union of cells still held in these slots.
Readers account for endpoints/snapshot roots, not merely PeerIDs: two slots are
two independently charged search contacts. An empty/not-relevant slot can
return a genuine empty/local response; it is not evidence about the other slot.
The existing index namespace and proofs need not change.

After T_j, stop new requests to that slot and drain/settle live handlers before
closing its stores. Stop renewing a cell route only if no still-serving slot
holds that cell. Stale remote hints remain possible and are ordinary bounded
misses. Old immutable snapshot IDs are never rebound to new content. An owner
may then reuse the endpoint slot with a **fresh** generation/root; late old-cut
queries return not-retained, never a fabricated current-cut answer.

Physical reclamation is necessary for sustained finite-disk operation. It is an
explicit operator retention policy over exact managed generation paths, after
all promises and live handlers end, with bounded recovery/tombstone state.
Default preservation is acceptable during development but then the service must
refuse when disk is full; archival without an archive quota is not reclamation.
This document authorizes no deletion of current project/evidence or user data.
Automatic retirement cannot target arbitrary paths from peer manifests.

Retain a bounded generation tombstone/config summary. Old capabilities name the
retired generation and cannot cause recreation, renewed leases or new writes.
Persist the retired decision/floor before reclaiming the managed root, so a
crash cannot delete data and then recreate that generation from an old token.
Per-request history can retire with the generation because old requests fail by
generation before lookup. Tombstone retention itself needs a fixed bound: use
a locally persisted monotonically advancing generation sequence and reject
sequences below the retained floor, not an ever-growing request archive.

Retention promises and service availability are separate. ACKs carry both the
storage retention end and current `service_not_after`; the current owner runner
has finite service grants. Restarts require a fresh explicit owner service grant,
reopening the exact immutable configuration, read-back/reconciliation of live
generation state and re-advertisement within new finite budgets. No persisted
monotonic deadline is treated as live authority. Local wall-clock uncertainty
must fail conservatively: do not delete possibly unexpired generations. An
owner clock-error assumption is needed for absolute retirement times; no
blockchain clock is proposed. Uptime across a crash or unfunded service gap is
not promised by retaining bytes.

For generation byte budget B and admission window W, sustained operation needs
the accepted unique-byte/metadata arrival rate and history overhead to fit B
per generation, plus service/repair capacity and a schedule that retires a slot
before another is needed. Long leases or bursts can make that impossible; the
correct result is capacity refusal. Adding independently funded custodians can
add capacity, but their existence and fault independence are assumptions, not
consequences of issuing many PeerIDs.

## Query reachability and conditional guarantee

For each accepted record, the receipt records the independently derived cell
and each live generation holding it. Queries derive K(g) without the record's
ID or placement receipt and try at most r owner-budgeted contacts per cell.
No scan of intake contacts, global peer list, all hash stripes or all object-ID
shards is needed. Stripe stays zero in this first contract.

The precise positive statement is:

> If export e satisfies the supported fingerprint condition for g, an honest
> custodian holding e remains within its retention/service window, its cell
> advertisement is returned and its endpoint is selected inside the reader's
> finite routing budget, and the reader completes the required authenticated
> intervals at a cut containing e, then the reader discovers e. Actual use
> additionally requires its selected evidence and demanded semantics to be
> available and accepted by the existing local verifier.

The proof is composition of deterministic cell coverage, acknowledged local
admission, actual selected endpoint reachability, and existing complete-interval
verification. It does not infer endpoint selection from DHT publication. With
many custodians under one cell, a capped lookup can omit one holding a desired
record. Report that coverage limit; no global cell/corpus completeness follows.

A cell can still be hot or semantically unselective. An operator cap B bounds
its local data, not total records held under that fingerprint worldwide. Query
limits must return `REFINE_OR_INCOMPLETE` when relevant anchor work cannot be
completed. Do not fan out across all providers and call it logarithmic search.
Richer owner-selected fingerprint paths/profile variants can improve selective
work, but migrating/admitting into another profile is a separate funded action,
not an invisible query rewrite. A generic theorem with STAR coordinates may
remain intrinsically broad.

With a <= 8 alternatives, at most r endpoint contacts per alternative, fixed
provider quotas, S examined postings and returned payload D, selected work is
bounded by routing plus O(a*r*H + S*log(B) + D), where H is the current bounded
summary/authentication overhead. Conditional expected logarithmic overlay
routing requires suitable connectivity/honest-enough maintenance. Neither a
constant cell count nor a finite response proves semantic recall at world scale.
There is no mandatory term for scanning unrelated global mathematics or replaying
ancestral proofs in this new placement path. Evidence production/acceptance and
any needed semantic imports retain their separate costs and assumptions.

## Exact implementation seams and non-goals

| Existing selected source | Reuse or smallest required successor |
|---|---|
| `instantiation_discovery/discovery/conclusion_fingerprint.py` | Reuse source fingerprint and bounded goal alternatives unchanged. |
| `pair_planning/discovery/module_export_adapter.py` | Reuse namespace, extraction and resolution; add only a pure cell-plan helper if a public API is needed. |
| `instantiation_discovery/discovery/discovery_store.py` | Reuse storage/proof format. An owner-bounded admit/read-back seam must invoke the intake owner guard immediately before both duplicate and fresh COMMIT paths, retaining rollback on refusal; its internal 30-second budget alone is not the new owner's deadline. No repartitioning or per-record GC. |
| `terminal_i/evidence_network/{custody,transport}.py` | Reuse exact typed custody and structural pull; no verifier. Add a bounded existing-custody lookup only where needed to avoid redundant exact fetches. |
| `custody/module_store.py` | Reuse group/body commitment checking, idempotent storage and readback. No recursive remote object traversal. |
| `terminal_i/client/workspace_evidence.py` | Open owner-locked profile workspaces; preserve ordinary local publication semantics. Placement does not mutate its mathematical-operation API into a remote authority. |
| `body_location/client/serve_advertised.py` and `base_projection/client/serve_workspace.py` | A dedicated placement-service successor owns the small intake handler, generation slots and finite dynamic route intents. The current read-only projected view is not writable custody. |
| `body_location/portable/location/maintained_roles.mjs` | Reuse publish/withdraw/maintenance and fixed endpoint descriptors. Serialize new publication commands with health/stop; reserve maximum dynamic cells/commands before startup. No new DHT role or global directory. |
| `pair_planning/client/located_queries.py` (selected logical `v5/client/located_queries.py`) | Reuse subset routes and aggregate query generations. At most eight separately funded fingerprint alternatives, never resetting the query budget between them. |

Current `serve_advertised` reserves commands from a fixed route list; it cannot
silently accommodate dynamic cells. Its successor must reserve startup,
permitted new-cell advertisements, health, withdrawal and cleanup commands,
using one serialized channel. Current Store operations are synchronous; an
async timeout alone cannot preempt their CPU work. Preserve bounded parsing,
index work and hard owner containment, add an actual pre-commit owner-deadline
check, and allow explicit incomplete service if health cannot run on time.
Do not promise a stronger real-time bound from an asyncio wrapper.

This first seam does not require new crypto proving, remote source execution,
mathematical trust in a custodian, all-lemma replay, full-corpus replication,
global task lists, ranking-policy changes or forced attribution. Index-only
placement is not the default: the exact selected evidence is retained too.
Still, retaining that packet and one selected opening is not a promise that
every future imported declaration/body is present. Existing independently
located body custody remains applicable; broader closure availability is
explicit, not assumed from a placement receipt.

## Small decisive implementation evidence, if root selects it

Use retained mathematics/evidence, not a new certificate campaign. A finite
three-role check can distinguish the feature: A already holds a publication;
B begins with no such cell and an explicit finite grant; A submits once; B
pulls, deduplicates, indexes and acknowledges; A stops serving; fresh C knows
only a goal/profile and overlay bootstrap and retrieves the export/evidence
from B through the derived cell. Verify the existing certificate only if that
changed integration boundary requires it; do not regenerate it.

Focused controls should cover bad/expired grant, disallowed source endpoint,
wrong cell/profile/packet, exact duplicate, duplicate after reply loss, one
interrupted cross-store boundary, generation restart/retirement, old request
replay, long-horizon refusal, full capacity and bounded query incompleteness.
These can share one small retained fixture; they are not reasons to rerun prior
discovery/body/mirror/proof campaigns. A source review must first establish
that no remote data reaches an executable/trust configuration and that every
cost is charged to the existing owner, including rejected pulls and history.

Stop conditions for this proposal: do not implement if unknown-ID discovery
requires a hidden manifest of all custodians, if intake requires a mathematical
issuer, if expiry cannot reclaim bounded generations without dropping promises,
or if packet-per-export duplication is unavoidable. Reuse the existing manual
owner workflow until those issues are resolved. A pass of this seam is progress
in independent selective accumulation, not a completed v5 or a proof of net
useful growth.
