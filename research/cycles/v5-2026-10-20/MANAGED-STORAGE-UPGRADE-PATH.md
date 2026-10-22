# SDK updates: rehost selected knowledge, do not rewrite old state

2026-10-22. storage_launch_review. Source-only assessment; no implementation,
runtime, transfer/restart campaign, credential read, Git action or migration
authority. The existing SDK map and concrete APIs, not historical128/127
counts, are the basis of this assessment.

## Decision

**Existing APIs suffice for a safe side-by-side transfer of an explicitly
selected finite set of mathematical exports into a fresh manager. No database
migration or proof-generation protocol is needed for that operation.**

They do **not** establish that every retained object/obligation was transferred,
or authorize immediate retirement/deletion of the old manager. The single
missing boundary for that stronger claim is a **bounded, frozen source inventory
with an explicit destination-coverage result**. Do not confuse that inventory
problem with a missing transport, mathematical checker or global ledger.

Do not implement a migration framework now. Document the existing selective
rehosting procedure and keep old obligations intact. If a complete operator
cutover is selected, the first source task should be that finite inventory and
coverage boundary, not a second custody-transfer protocol.

## Exact basis

The129 SDK map is
`experiments/v5-local-checks/distribution-managed-storage-01-input.json`, SHA-256
`a629df82718f6a9d0560cacbfdc459739c15a56a1f2a46dd87929a1db51c22a4`.
Its fresh release document is
`product-local/v5-distribution-managed-storage-01/Mathematical Commons v5/V5-RELEASE.json`,
`811d4a86dd6523a44435ca89a4d7a5eb0367ccca727cdc45a9e095f8f22446e2`.
This identifies source; root's independent build/outcome adoption is separate.
Read the complete storage README, SHA
`c299cdfd1dde7e6df9cb2f493ed1a302f6e02aadccec700e749110ed5f0d2010`.

| Logical source, current SHA prefix | Concrete relevant boundary |
|---|---|
| `client/managed_owner.py`,6991ac58 | `_bindings` authenticates all129 SDK rows and reconstructs the storage writer digest; `_open` passes it to the manager. New code cannot assert an old digest to reopen an old manager. |
| `client/serve_placement.py`,c815331f | `open` attaches `CompositeProvider` to the current index, module custody and packet custody. Read serving and intake are separate. `issue_token`, `submit`, `status`, `advertise_retained` already exist. |
| `placement/codec.py`,6f32569d | `manifest` binds generation/namespace/wire profile, exact export and packet identities, optional selected bodies and retention. `request_id` additionally binds grant and generation. |
| `placement/controller.py`,ef1c9b59 | `_run` pulls missing opening, chosen packet and bodies; uses `EvidenceAcquisition(...,verifier=None)`; rereads exact custody, derives the formal index record and commits the placement receipt. It does not inherit an old acceptance report. |
| `placement/network.py`,1ec5c452 | `PlacementClient.submit/status` are the existing public transport; submitted-object identity is checked against `RECEIPT_COMMITTED` outcomes. |
| `placement/ledger.py`,59f87b93 | New requests are charged; duplicate matching requests are status-only. `request(id,...)` is exact-ID lookup, not a complete inventory API. |
| `placement/advertisement.py`,13b0ef1a | `advertise_retained(id)` validates the local retained receipt, exact objects, grant/manifest binding and horizon before dispatching a route. It cannot transfer an old receipt to a new generation. |
| `custody/module_store.py`,580515e4; `evidence_network/custody.py`,4264841e | Exact group/body retrieval and structurally checked packet offers/storage; no complete store-export iterator is exposed. |

These rows were resolved through the current map and the relevant actual
implementations were read. Existing audited transfer, restart and mathematical
reuse evidence is reused; no new combined outcome is claimed here.

## Assumptions, deliberately narrower than arbitrary software migration

Both releases are explicitly adopted and the old writer remains permitted to
serve its own state. Their mathematical foundation/policy, export namespace,
wire/evidence formats and relevant transport contracts are compatible. The
destination independently enforces them; equal storage layout alone is not
compatibility. A security update revoking the old writer is not permission to
run it to export: preserve that state and select a separate reviewed recovery
path if required.

The source remains reachable through an already authorized live service, a
legitimate remaining old run, or another custodian. Original run/session caps
and horizons must suffice. Exhausted caps do not authorize editing configuration
or bypassing the manager through a newly invented standalone opener. Source
disappearance cannot be repaired by hashes.

Let `S` be the explicitly selected finite export/packet/body set, with exact
commitments and resource bounds known from retained manifests or independently
checked descriptions. `S` is not implicitly all objects in the old manager.
Selected payloads must fit current interface ceilings and source offers. In
particular, placement currently requests only the first four packet offers for
a known module, and a manifest selects at most eight bodies. A hidden later
packet is not silently treated as transferred. These are existing finite
interfaces, not a universal bulk-export guarantee.

## Minimal operator procedure using existing APIs

1. Fix `S` and its exact source context. For a stable whole selected set, seal
   old intake through the old adopted lifecycle before declaring that set fixed;
   continue finite read serving only within its original authority. Preserve
   old manager/configuration, charges, keys and failed operations unchanged.
2. Adopt the new installation separately; initialize a fresh manager with its
   own correctly derived writer digest, storage reservations, epoch, endpoints,
   grants and finite lifetimes. Never copy an old SQLite file, marker or saved
   live-owner object into the fresh manager. The transfer is content rehosting,
   not operational-state migration.
3. Point a new destination intake grant at the old custodian's explicitly
   adopted read endpoint. For each selected item, construct a fresh canonical
   placement manifest: preserve exact mathematical export/packet/body identities
   and compatible namespace/wire binding; use the new generation and a newly
   funded permitted retention horizon. Use the existing private credential
   helper and `PlacementClient.submit/status`; do not reuse an old bearer token
   or its request ID as new authority.
4. Require the new request's durable `RECEIPT_COMMITTED` result with exact
   opening/packet/body commitments and index readback. A route facet is separate:
   `INDEXED_UNADVERTISED` is not worldwide discoverability. The new provider can
   advertise its own record, and a known-contact consumer can independently
   retrieve/verify it. Compare per-item destination evidence with `S`; a timed-out
   or incomplete item stays incomplete with both sides' charges retained.
5. Direct subsequent new work to the fresh installation. Keep old evidence and
   all outstanding old retention duties. A copy does not discharge an old
   contract or make the new host's receipt equivalent to the old receipt. Old
   retirement/reclamation remains a separate explicit operation under its old
   policy and timing conditions, not an automatic consequence of copying `S`.

No all-or-nothing transaction across hosts is assumed. A partially completed
transition leaves valid old objects and separately charged new partial custody;
it must not delete either side or relabel failures to simulate atomicity.

## Proof ancestry and cost

Custody transfer checks structural identities and stores exact selected bytes;
the controller deliberately supplies no mathematical verifier. It therefore
needs no new SNARK, certificate production or ancestor-proof replay. This is
**not mathematical acceptance**. A fresh user of the destination must still
apply its own current verifier/trust policy to the exact received evidence and
check any selected native delta or demanded transparent semantics.

For existing succinct certified packets this reuses their certificate boundary,
not old verification history. A native-only/mixed packet does not become succinct
merely because it is copied. Transfer cost is proportional to selected bytes,
bounded index work and per-item overhead, not independent of `|S|`; no whole
global corpus or all agents need be contacted.

## One consequential remaining issue: complete cutover coverage

For an operator claiming complete retention continuity, define a source set
`S_cut` at a specified sealed cut and require every required item to have a
matching new custody result and an adequate stated retention horizon. The
current managed status lists generations, not their complete retained content;
ledger lookup takes an already known request ID; packet offers take a known
module and truncate; feature search is not a complete local inventory oracle.
Consequently current APIs cannot justify `S = S_cut` from absence of further
search results. Saved operator submission manifests may already supply a
complete inventory in a controlled deployment, but that is an explicit
premise, not a software-established fact.

If full cutover is needed, the smallest missing owner boundary is a bounded,
resumable export manifest anchored to a sealed local generation/cut, carrying
exact retained obligations and content commitments plus explicit unsupported/
incomplete cases. Its coverage result must match new receipts without claiming
to move tokens, charges, live contexts or historical acceptance authority. Use
existing transfer APIs for items they support; report a truncated/unoffered item
instead of treating it as covered. No global index, consensus or generic
database migrator follows from this requirement. Stop here until root selects
whether complete cutover, rather than documented selective rehosting, is the
next consequential release obligation.
