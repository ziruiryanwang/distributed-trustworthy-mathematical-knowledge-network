# Source feasibility of the selected owner-operated location layer

2026-10-28. Answers [OPERATOR-MODEL.md](OPERATOR-MODEL.md); source reading only.
No implementation, imports, database opens, execution, network or Git action.
The common receive cut is independently specified in
[RECEIVER-SEAM.md](RECEIVER-SEAM.md), SHA-256
`801c193e75f31abaf4c1426317d11ba77c0c7f01d5c1cf0d5a0371ad5efe90ef`.
Root has separately selected the immediate fixed-provider transport repair in
`ordinary_owned_acquisition/SELECTION.md`. The location additions below remain
feasibility candidates, not part of that two-helper implementation.

## Result

The selected voluntary, own-custody model is implementable with the retained
DHT. It needs no remote registration service, new DHT, mathematical schema or
native-owner change. The repeated advertisement-count scan has a safe small fix:
one bounded startup census plus a conservative process-local charged-key set,
using the existing serialized commands and atomic intent operations. A new
durable counter schema is unnecessary for this model.

This is still a complete operator/HTTP/reader integration, not a wrapper-only
change. The main costs that survive the count fix are runtime verification,
bounded metadata recovery, per-key provider publication/renewal, periodic
provider scans and finite gateway service. Current public launch rejects reused
state, IPC allows only62 commands, and existing descriptors carry no lifetime.
Those seams must be selected together. Nothing requires reopening old proof
campaigns to decide them.

Correction to DECISION: the192MiB check in
`portable_runtime/location/controller.py:112` bounds **authenticated runtime
payload bytes**, not process memory. The controller checks5,896 selected
Node/overlay payloads before and after service. RAM requires a separate outer
process grant. These runtime files and their pinned manifest can be projected
without the full certified application or Lean payloads; the verifier selects
only `overlay/` and `runtime/node/`.

## Smallest complete logical source cut

All paths below are existing origins under `software/v5/`; any implementation
must use fresh successors, leaving these used sources unchanged. New helper
names describe boundaries, not files already present.

| Boundary / source origin | Required successor or unchanged reuse |
|---|---|
| New bounded advertisement-delta helper; reuse `ordinary_contribution_bundle/project.py:279-325` and `ordinary_multi_source/ordinary_acquisition.py:172-185` | Parse only supplied new bundle units; derive every output locator/export, apply explicit owner selection and finite row/byte caps. No target-only projection or old-proof scan. |
| Own-custody eligibility; reuse `OrdinaryAcquisition.locator` and host `get_locator` | Before first advertisement, check proposed keys against the operator's explicitly approved current custodian endpoint, including expected name/UnitID. Charge these reads to the operator. Existing host service stays a separate finite role; no host database surgery or arbitrary remote registration. |
| `body_location/portable/location/protocol.py` and `protocol.mjs` | Add one distinct ordinary semantic/export domain, route key, closed descriptor request/reply and finite lifetime binding. Do not map ordinary hashes into certified-body fields. Reuse endpoint and authenticated-peer validation. |
| `body_location/portable/location/intent.mjs` | Reuse atomic intent/published insertion and revocation unchanged if `validateIntentSpec` accepts the new closed ordinary role. No new datastore or intent schema is needed for the conservative count. |
| `body_location/portable/location/maintained_roles.mjs` | Ordinary publish/withdraw/locate/descriptor entrypoints, config/domain/role validation, lifetime-bearing descriptor, and startup charged-key census replacing per-publish counting. Query-only gateway operators cannot publish; custodian operators advertise one approved endpoint. |
| `body_location/portable/location/ipc_wire.mjs`, `node_entry_services.mjs` | Add only the closed ordinary commands; explicit create versus reopen mode; consistent finite frame/command caps. Preserve source pinning, private pipe, no foreign absolute clock, service timer and shutdown. |
| `portable_runtime/location/controller.py`, body-location `controller_services.py` | Ordinary-specific controller/profile: optional existing state, fresh evidence and fresh owner grant, consistent IPC caps and finalization reserve. Remove unused located-formal-search imports from this narrow role instead of loading its full search workflow. |
| New operator/gateway orchestration; adapt lifecycle ordering from `body_location/client/serve_advertised.py`, not its certified workspace | Own finite Node process, approved delta publication, read-only HTTP service, one bounded private-channel queue and shared operator budget. No certified workspace/module reader or mathematical owner object. |
| New pure exact-lookup envelope/backend class; successor of `ordinary_registration_refresh/http_provider.py` | Add one concrete async lookup route inside the current request/response reservation and timeout path. `Provider.dispatch` is synchronous today; inserting a DHT call there unchanged is not viable. No peer-supplied callback or write/registration route. |
| Receive/client/owned transport successors | Exactly the common cut in RECEIVER-SEAM: private per-demand candidates, upfront location prepayment, unchanged exact validators/admission, absolute expiry through every dial, narrow settled-refusal mapping. |
| Operator and investigator source maps/launchers | Pin the changed logical roles and their complete import closure; reuse existing Python supervision and the selected Node/overlay projection. Node remains optional for readers. Public configuration/docs must expose independent reader/operator/host grants. |

This table is the implementation boundary. Unchanged runtime transport, framing,
quota-store primitive, Noise/Kademlia provider stack, ordinary evidence codecs,
custody transactions and mathematical checking should be reused. In particular,
`role_composition.mjs` supplies service-abort to pending raw connects and
`services_composition.mjs` supplies required Ping; bypassing those wrappers would
discard already established lifecycle behavior.

## Delta preparation and own-custody publication

The original bundle plus its pinned manifest suffices to derive all proposed
output keys: read/validate each new unit once, enumerate `unit[2]`, build the
unchanged locator and calculate its ordinary ExportID. The existing helper's
target list does not include every support output. A new small sidecar can retain
these proposals independently of append reporting; it is not evidence of commit.

The cheapest separate-role composition leaves the current host code unchanged.
After append and host readiness, the operator verifies selected proposals through
the existing exact locator route at its owner-approved own-custody endpoint.
`get_locator` checks retained evidence metadata; compare its exact UnitID/name
against the parsed bundle. This costs at most one bounded locator read per
proposed export, with no earlier corpus proof read. Successful earlier append
reports may inform selection but do not replace this readback after uncertain
commit/reporting. An alternative combined host action can perform the same
indexed read under the existing host lock; it is a source change, not necessary
to make the separate-role composition complete.

Only operator-approved keys are published. The input may include every new output
and then deliberately select a capped subset; report omitted coverage. Failed
publication leaves valid custody undiscoverable. The host may stop before the
operator's advertised horizon: serving and advertising have separate grants, and
a candidate is always advisory. A combined wrapper can align their horizons,
but cannot promise continued remote availability.

There is no remote registration/write API. The operator's approval names its own
custodian endpoint and selected keys; a gateway request can ask about an exact
key but cannot insert it into the operator's publication set or renew service.

## Durable storage APIs and the cheaper count invariant

The retained `overlay/quota_store.mjs` supplies `DatabaseSync`, `_transaction`,
`_put`, `_delete`, `has`, `get`, `query`/`queryKeys` and finite batches. Transactions
use `BEGIN IMMEDIATE`, synchronous operations and `COMMIT`; global entry/byte
totals are updated with rows. Open uses DELETE/FULL journaling, an exclusive
SQLite owner, fixed page/entry/byte limits, a full bounded row/counter census and
provider-group quota checks. There is no per-prefix count or TTL API.

`intent.mjs:42-57` already inserts the intent and `/application/published/<key>`
in one transaction. Revocation deletes intent, self-provider record and published
row in one transaction. Its `_put` guard forbids a self-provider write without
the matching intent. These are sufficient durable primitives.

Let `P` be the committed published-key set and `S` the in-process charged set.
Maintain **`P` subset-of `S`, with `|S| <= K`**, where K is the unchanged adopted
advertised-key cap:

1. After opening the locked metadata store and before starting libp2p, scan the
   published prefix once, with the original startup deadline and K bound. Load
   `S = P`; refuse malformed keys or excess cardinality. Reconcile only from the
   committed store, not an earlier success report. This census costs O(K) row
   visits, with indexed datastore lookup overhead, and is charged at every open.
2. Under existing `_command` serialization, reserve a previously uncharged key
   in S before calling `enableIntent`. A duplicate key already in S uses no new
   slot. The atomic insertion either adds that reserved key to P, changes nothing,
   or has uncertain reporting; all three preserve the subset invariant.
3. Keep the reservation after failed/ambiguous publication, including network
   failure after successful intent commit. Do not infer rollback from an error.
   This can reduce usable capacity but cannot exceed the owner quota.
4. Remove a key from S only after `revokeIntent` has returned confirmed success.
   If deletion/commit reporting is uncertain, retain the charge. A subsequent
   publish must reserve the key again if a confirmed withdrawal released it.
5. Crash ends this process's authority. A separately authorized next finite
   session performs the same startup census and recovers exact committed P,
   discarding phantom in-memory charges without altering durable rows.

The no-background-writer premise is supported by the actual call graph. In the
selected role, only `_publishRoute` calls `enableIntent`; only `_withdrawRoute`
calls `revokeIntent`. Descriptor serving reads published keys. Retained
`providers.js` and `reprovider.js` write/delete `/dmknv5/provider/...`; DHT value
storage uses `/dmknv5/record/...`, not application publication rows. Peer-store
and transport activity cannot create published intent through the closed IPC.
Provider expiry therefore does not change P. If future code deletes published
rows in the background, retaining their charges is safe; any future background
creation must first use this reservation path. Trusted local source/state and
exclusive ownership remain premises, not hostile-owner isolation.

An exact durable counter is also feasible: add a fixed versioned KV counter and
update it through `super._put` in the same existing enable/revoke transaction,
changing it only on absent-to-present/present-to-absent transitions. Count its
own storage; compare it with a bounded startup census and refuse mismatch. This
adds schema/bootstrap/migration and additional writes without improving safety
or avoiding the quota store's existing startup census. Prefer S for this model.
Never substitute `totals.entries` for the advertised count: those totals include
unrelated provider/peer records.

## Expiry, withdrawal and restart are distinct

The actual retained provider implementation stores a varint `Date.now()` timestamp.
`Providers.loadProviders` excludes invalid/future or age-at-least-TTL records,
even before physical deletion. `Reprovider.processRecords` scans the provider
prefix, deletes expired non-self entries and queues near-expiry or expired self
records. Self-provider records deliberately survive offline periods. Published
intent has no automatic TTL; it stays quota-charged until withdrawal. That fits
an owner-selected retained scope whose maintenance runs only during explicit
finite sessions. Do not claim expiry itself recovers advertisement slots.

The existing service timer/abort stops maintenance. Remote hints may survive
their provider TTL after stop or withdrawal. New finite sessions authorize new
maintenance; they are not a retry with the prior expired grant. No durable
monotonic deadline is invented across processes. Wall-clock anomalies can reduce
provider recall; reader and service authority still use local monotonic time.

`MaintainedLocator.start({create:false})` already reads the retained identity and
requires an exact adopted config hash, then opens the quota store. However, the
Python controller and Node entry currently require fresh state and the entry
always calls `start({create:true})`. Both must expose an owner-only explicit reopen
path while keeping fresh evidence, profile checks and finite outer containment.
The exact config includes addresses, bootstraps and limits: reopening it does
not authorize endpoint/profile migration. Changed profiles need a separately
selected transition or fresh state; stale old peer hints still expire normally.

A failed first provide can leave intent without a self-provider row: the
`enableIntent` commit precedes DHT `provide`, which then inserts its self record.
The background reprovider scans provider rows, not intents, so it does not
necessarily repair this case. Keep it charged and report it as pending/possibly
undiscoverable; the startup scan can check the corresponding self record with
one indexed lookup per key. Any later publication attempt is an explicitly
selected bounded delta in a new grant, not an automatic unbounded replay.

## Finite gateway and lifetime translation

The gateway serializes access to its one existing private Node channel; public
HTTP connections have a finite queue or receive a settled busy/unavailable
answer. It reserves HTTP request/reply capacity before DHT work and clips each
lookup/descriptor operation to both its HTTP-operation deadline and its own
remaining service/IPC/transport grant. Client maxima can narrow these limits;
they cannot increase them. Cancellation or an uncertain private-pipe result is
terminal for that channel, using the existing controller teardown.

A lookup consumes one DHT locate command plus at most q descriptor commands,
with bounded event, provider, descriptor-byte and elapsed-time limits. Gateway
policy checks remote descriptors; the reader independently checks returned HTTP
endpoints. The gateway must not recursively follow HTTP referrals. No global
provider roster is materialized or enumerated.

Current descriptors contain no remaining lifetime. The new ordinary descriptor
must express a bounded remaining advertisement/contact duration, clipped at the
provider's original service/advertisement horizon. It is separate from DHT
provider TTL, whose remaining value is not exposed by `findProviders`.
For gateway descriptor request start g0 and returned remaining duration r,
derive `eg <= min(g0+r, gateway policy cutoff, original operation cutoff)`.
At HTTP response construction, disclose at most `max(0, eg-now_gateway)`;
the reader anchors that duration to its original HTTP request start, then clips
its own grant and policy. This conservatively consumes transit/setup time
without comparing remote absolute clocks. A cached duration must be recomputed
from the original eg, never restarted. Omit expired hints. Dishonest upstream
duration claims remain advisory and locally capped; this is not a proof of
availability or honest clocks. RECEIVER-SEAM then preserves the resulting
private horizon through locator and evidence setup and dial.

## Resource and cost discriminators

Let delta be newly selected exports, K retained advertised keys, M all retained
metadata entries, T service duration, I maintenance interval, G admitted gateway
lookups, q descriptor attempts per lookup, and C total private commands.

| Work | Bound/cost that must be exposed |
|---|---|
| Delta preparation and eligibility | New supplied bytes/output rows plus at most delta exact locator reads; no earlier proof corpus. |
| First/duplicate publication | O(1) charged-set work and indexed transactional writes per key, then bounded provide work; duplicates still pay requested network publication. |
| Withdrawal | Indexed atomic deletion and confirmed charge release; remote revocation remains eventual. |
| Open/recovery | Full retained-runtime verification and bounded quota-store census O(M), plus O(K) publication census/optional pending-row checks. Repeated tiny restarts can dominate. |
| Periodic maintenance | At most the finite number of scheduled passes during T, each visiting up to M provider metadata rows, plus queued bounded network work. Queue32/concurrency2 are limits, not guaranteed coverage throughput. |
| HTTP gateway | G bounded lookup responses; at most G(1+q) locate/descriptor commands, plus publication/withdrawal/health/stop commands, all inside C and total pipe bytes. |
| Reader | Common prepayment and `md + 2mp` request upper bound, p<=8, exact validation, original deadline and cleanup; no Node installation. |

The current pipe has16KiB frames,1MiB each direction and64 frames; its effective
command maximum is62, including lifecycle work. `limits.commands <= 8192` does
not override that smaller pipe limit. A useful operator profile must either
declare this small service capacity honestly or select consistent larger finite
caps in Python controller, wire validator and Node entry. Bounded publication
batches can amortize IPC but must still charge every key, provide operation and
reply; they cannot evade key/transport/work caps. No arbitrary remote batch is
accepted. Do not claim a4,096-key limit means4,096 publications fit one current
service call.

Even after the count fix, if every append restarts the operator, cumulative
startup census/verification can dominate; only within-session publication has
lost the cumulative scan. Deliberate finite batching and useful service duration
are part of the cost decision. Provider/self/application rows also share the
metadata quota: each advertised key needs two intent/publication rows and normally
a self-provider row before remote-provider and peer metadata. K alone is not a
capacity guarantee. Global network renewal remains proportional to advertised
holder/export pairs and replication, subject to partial coverage.

## Decision for root

For the selected workflow requiring a previously unknown independent custodian,
this source cut is feasible and preserves the desired coverage opportunity.
The concrete operator model removes the earlier unspecified-registration issue,
and the conservative count avoids a new persistent schema. Prefer this retained
backend if arbitrary exact-key reachability is the required next capability.
Grouped membership remains cheaper when a discovered bundle already carries the
needed supplier/group graph; it cannot by itself locate an independent holder
outside that graph. [GROUPING-ALTERNATIVE.md](GROUPING-ALTERNATIVE.md), SHA-256
`2143c62cde963346e4b68df0409925904f88bbe9830704238d97955782444c51`,
specifies the missing GroupRef/sidecar/membership work and stable-anchor premise;
do not implement both backends speculatively.

The choice can change if realistic selected key counts/TTL imply renewal work
that exceeds the finite grant, if tiny service sessions make runtime/open costs
dominate, or if the intended imports already have adequate grouped provenance.
No count benchmark is needed to establish these source facts. A subsequent
implementation selection must fix K/M, delta and G/q/C, service/cleanup horizons,
one create/reopen policy, and the exact changed source map before any execution.
The later qualification should exercise the complete unknown support-holder
path, duplicate/ambiguous publication and reopen count, expiry/withdrawal, finite
gateway exhaustion and cleanup; it need not generate new mathematics.

## Retained primitive bindings inspected

The following source files were read, not imported or executed, under
`product-local/v5-distribution-body-custody-01/Mathematical Commons v5/base/overlay/`:

| Source | SHA-256 |
|---|---|
| `quota_store.mjs` | `7c6cbeea0c685ec81f8d263cf84c6b8b9dd2c1f09e9f2f0f063196abc929eca4` |
| `node_modules/@libp2p/kad-dht/dist/src/providers.js` | `62df9d6539043cddbd61b69bab05c080c8e4098f25c2d8344610b914defb1ebb` |
| `node_modules/@libp2p/kad-dht/dist/src/reprovider.js` | `fc7a92f68778dad60d37ce6769d58ad04adbd279f42769e1339dd53a70ab4e28` |
