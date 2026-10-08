# Exact-byte replica custody and re-serving

Bounded design proposal, 2026-09-21. Based on the complete
[v1 critical path](V1-CRITICAL-PATH.md), current acquisition/exposure/publication,
storage, wire, service and recovery paths. Only this note was authored for this
task; no import, execution, database query or product change was performed.
This is not qualification or permission to launch a new service.

## Decision: one explicit replica exposure, no new publication

Add one owner-local, ordinary-client operation:

```json
{"client":"local","request_id":"share-import-001","op":"replica_expose",
 "args":{"acquisition":"acquisition:ACTUAL_RETURNED_HANDLE"}}
```

It selects **one previously committed acquisition owned by that client**,
revalidates its original received package, and creates one ordinary immutable
peer view. The existing explicit finite `manage.py serve --client ... --view ...`
starts distribution. Acquisition itself still creates neither a view nor a
service. The operation does not publish a locally authored result, generate a
wrapper theorem, append a new P1 entry, admit a candidate or move a context head.

Keep existing `publish` and publication-only `expose` semantics unchanged.
Do not add a second custody registry, new table, global identity, cryptographic
signature, consensus protocol, network-wide index or custody reward mechanism.
The committed replica view is the local record of an explicit sharing choice;
the existing acquisition is the custody source. “Owner-local” uses the existing
trusted operator/configured-client boundary, not a new remote authorization API.

## The important distinction the current code exposes

There are two different exactness requirements:

1. **Mathematical-object exactness:** unchanged foundation, typed object IDs,
   canonical object payloads, root closure and descriptor/formal metadata.
2. **Transport exactness:** unchanged raw manifest, object ordering, framed
   bundle length and bundle SHA-256.

`peer_wire.receive_bundle` retains the original manifest/object bytes under the
request's `incoming` directory. But `Checker.offer` calls `import_package`, which
re-exports the package through `source_codec.export_package`. That export sorts
objects and rewrites manifest JSON. `PeerOperations.reuse` may then choose an
older equivalent local normalized package. The acquisition record's current
`package` field names this normalized/reused offer, not necessarily the exact
transport representation received from its source.

Consequently, merely removing `require_published` from `expose` is insufficient
for the stronger exact-bundle claim. Valid manifest whitespace/key ordering or
object-list ordering can differ while mathematical identities remain unchanged.
This proposal preserves the original inbound representation and checks both
notions of exactness explicitly. No normalized-byte equality is assumed.

## Minimal storage delta

Extend newly committed `acquisition` data by exactly one field:

```json
"received_package": {
  "path":"ABSOLUTE_OWNED_REQUEST_DIRECTORY/incoming",
  "manifest_sha256":"ORIGINAL_ADVERTISED_MANIFEST_SHA256"
}
```

Keep the existing `package` field for the normalized/reused candidate; do not
change its meaning. In preparation, retain `received["package"]` from the
already authenticated transport result. In the acquisition visibility
transaction, store that pin alongside the existing remote handle, peer,
endpoint, catalog digest, bundle digest, descriptor, sequence, snapshot and
request key. The remote record already retains the complete advertised entry,
including original bundle size/root/manifest digest/formal metadata. No second
copy of that entry or original `.bundle` file is needed in the ledger.

`incoming` already contains retained, individually flushed transfer files.
Its exact directory must equal `state/work/<acquisition.request>/incoming`, with
the actual request-key syntax and no reparse traversal. It must not be an
arbitrary path supplied to `replica_expose`. Original transfer files are part of
that existing acquisition's retained resource charge; no retroactive refund or
unfunded perpetual-storage promise follows.

Old acquisition records lacking this field are not silently upgraded or guessed
from directories: return `REPLICA_CUSTODY_UNAVAILABLE`. A new explicit acquisition
under the new installation can establish the needed custody record, even if its
candidate deduplicates with an existing P1 entry. Existing installed source/config
cuts remain immutable; no migration of historical receipts is implied.

## Preparation and commit contract

After ordinary exact-request replay and reservation, under the existing writer
exclusion, `replica_expose` performs these bounded steps:

1. Authenticate the acquisition record for the requesting client. Authenticate
   its remote record and historical snapshot membership; require P1 and the exact
   sequence/descriptor. Compare acquisition peer/endpoint/catalog/bundle fields
   to the remote record and its selected entry. A currently advanced P1 cut is
   harmless; rewriting an old selection to a new endpoint is not.
2. Bind its original request key to the committed `peer_acquire` request for
   this client and remote selection, and bind the stored terminal response to
   this acquisition handle. Use indexed lookup, not a history scan. Authenticate
   the current local offer at that P1 sequence. Compare the stored normalized
   package pin as data; sharing does not need to execute or trust a foreign
   receipt or re-open a vanished source endpoint.
3. Select `received_package` only from that authenticated record. Check path,
   raw manifest digest and original foundation. Read the complete package using
   the local structural/canonical validation path: full typed IDs, payloads,
   inventories, exact root closure and supported replay structure. Recompute
   descriptor, formal metadata and symbols and compare them to both the stored
   offer and advertised entry. This is not a native proof acceptance.
4. Build a **one-entry** view from the original received package and recomputed
   metadata. `make_bundle` deterministically emits the same framing from the
   original manifest and object bytes. Require the newly built entry to equal
   the original advertised entry field-for-field, including bundle length and
   digest. Refuse any difference, even if normalized mathematical identities
   happen to match. Preserve exact bytes; do not repair or re-export them.
5. Flush and authenticate the completed view's catalog, completion marker and
   bundle. Retain it in this request's fresh `work/<key>/peer-view` directory.
   No catalog or service becomes authorized from a partially written directory.
6. In the short ordinary visibility transaction, recheck the selected immutable
   ledger bindings, create only the view record, and terminalize the request
   with the exact reply. Preserve all candidate/provider/snapshot/publication,
   head, artifact, mathematical evidence and stage state. Ordinary reservation,
   attempt marker and terminal bookkeeping remain real consumed work.

The view's existing top-level record shape remains `kind:peer_view`, directory,
foundation, catalog pin, completion pin, selected list and
`mathematicalAcceptance:false`. Its single selected row is:

```json
{"provider":"P1","sequence":1,"descriptor_id":"ACTUAL_TYPED_ID",
 "basis":"replica-custody","acquisition":"ACTUAL_ACQUISITION_HANDLE"}
```

The descriptor above stands for its actual typed JSON structure, not a string
encoding substituted by the API. Existing publication-backed selected rows
remain distinct and retain their `publication` field. Do not manufacture that
field or a `publication` record for an acquisition.

Return the ordinary non-acceptance peer response with view handle, catalog
digest, `entries:1`, `historical_view:true`, `candidate_only:true`,
`untrusted:true`, `mathematicalAcceptance:false`, `native_stages:0`, plus
`basis:"replica-custody"`. No `accepted:true`, origin author or new theorem ID
is emitted. Exact request replay returns the original response bytes without
new work, even if view files later disappear; replay describes history, not
live availability. A later actual serving attempt reauthenticates its bytes.

## Serving and receiving: no borrowed acceptance

The service worker recognizes the exact replica-selected-row shape and binds
it to the selected catalog entry and authenticated acquisition record. This is
local authority to serve an immutable view, not a claim of authorship. Its
runtime path continues to use only the committed view, its catalog/completion
pins and bundled bytes. It does not import the mathematical checker or run Lean.
Source/evidence/config files, other acquired packages and unselected bundles
remain outside the HTTP namespace. Explicit serve grants retain their present
finite request/byte/time accounting and process-tree supervision.

At service startup `load_view` authenticates all selected bundle bytes; each
bundle request reads and hashes the bytes actually returned before sending.
Missing/changed bytes close or refuse that transfer. A served in-memory copy
remains the authenticated copy even if its backing file subsequently changes.
The frozen view is self-contained: loss of the separate normalized analysis copy
or the original source's files does not invalidate an intact committed view.
Loss of the original received copy prevents *new* replica-view construction,
but does not retroactively change an old immutable view's identity.

C still follows unchanged `peer_find` → `peer_acquire` → `admit` and, for fresh
downstream work, `submit`. C verifies transport framing and bundle/object IDs,
derives local metadata and receives only a candidate before admission. B's
view/acquisition records and A's proof-execution receipts are not imported as
C's mathematical acceptance. C's own selected Lean checking path must accept
the package relative to its foundation/current context. C may refuse even when
B served exact authentic bytes: unsupported foundations, invalid proofs,
incompatible inventories, missing dependencies and resource limits are distinct
possibilities. Hash authentication is not a proof of a theorem.

For package x, keep these implications deliberately absent:

```text
Have_B(x)  does not imply Offer_B(x)
Offer_B(x) does not imply Accept_B(x) or Accept_C(x)
Accept_C(x) historically does not imply Have_C(x) now
```

Conditionally on trusted local implementation, stable selected files and hash
security, successful replica preparation establishes equality of original and
re-served bundle bytes and preserved mathematical IDs. It does not establish
the content's truth, usefulness, authorship or perpetual availability.

## Concrete implementation boundary and resources

| Existing location | Selected small change |
| --- | --- |
| `peer_node.acquire/commit` | Carry/store the original `received_package` pin; leave existing normalized offer and candidate behavior intact |
| `node.PEER_OPS`, request parser, grant selection | Add `replica_expose`; forbid native allocation and charge the existing 80-MiB exposure grant |
| `peer_node.prepare/commit` | One-acquisition validation and exact inbound-bundle view construction; commit only the view/terminal reply |
| `peer_wire.build_view` | Clarify that caller provides explicit publication-or-custody authority; framing need not change |
| `manage.invoke` | Include the new operation in the existing native-free 120-second/120-CPU-second/1024-MiB profile |
| `service_worker` | Validate replica selected-row/catalog/acquisition binding; preserve checker-free serving and exact view pins |
| `recovery_worker` | Extend the explicit native-free allowlist only with corresponding interruption controls; do not assume the existing qualification automatically transfers |

No new storage table, mathematical codec, content-address calculation, wire
schema, endpoint or proof mechanism is required. The one-entry limit is deliberate:
it keeps the cut and authority selection small without adding a batching policy.
Current bundle limits remain 18 MiB framed, 16 MiB payload, 1 MiB manifest,
8192 objects; catalog is at most 65536 bytes. Existing 80-MiB exposure reserve
is a conservative grant, not an assertion that the new view occupies 80 MiB.
No stage grant is permitted. Actual CPU, retained bytes and failures are measured.

## Interruption and availability boundary

Before the visibility transaction, partial view files are retained charged
staging, not a serveable view. After successful commit but lost caller output,
exact replay recovers the old view handle without rebuilding. A pending request
may be terminalized as interrupted only through authenticated original-attempt
quiescence, writer exclusion, intact/openable ledger and zero native-stage
evidence. No directory scan or completion marker alone can promote an orphan.
Unknown commit/cleanup state stays unknown; no automatic new-ID retry follows.

The present nonempty-sidecar refusal and process-interruption-only durability
limits still apply. This cut does not solve a kill inside a SQLite transaction,
power loss, damaged media, missing original execution evidence or general
native recovery. Normal serve remains a finite explicit session, not an
indefinite hosting service or background replication daemon. Future durable
hosting authorization is a separate critical-path task.

At least one reachable holder with intact bytes and supplied resources is an
availability premise. Three copies on one physical machine do not establish
independent-host fault tolerance. A preparatory loopback experiment can establish
the custody transition; a multi-host claim requires real separate environments
and a separately reviewed transport/contact profile. There is no necessary
central endpoint in this mechanism, nor a promise of global instantaneous state.

## Positive discriminator: A offline, B serves, C checks and uses

Use one already authenticated genuinely source-produced/published package x at
A; no new theorem need be generated merely to test custody. Fresh B and C use
the same supported foundation. Keep all original mathematical artifacts and
historical source cuts unchanged.

1. Bootstrap B. Through A's finite service, B discovers/acquires x. Require one
   actual acquisition, exact original transfer pins, unchanged B head and no
   publication or view created by acquisition. Do not natively admit x at B.
2. Stop A's service and authenticate its complete worker-tree quiescence. A is
   unavailable before B constructs the replica view; no refresh from A is
   permitted. Configure C with B only, not A.
3. B explicitly calls `replica_expose` for that acquisition and starts a finite
   service for the returned view. Compare A's preserved original bundle and
   B's actual served bundle byte-for-byte, not just descriptor strings.
4. Bootstrap C; discover/acquire x from B. Require unchanged foundation, typed
   IDs, root, canonical object bytes, raw manifest and bundle digest/size. The
   different supplier/locator creates no new mathematical identity. At this
   point C has a candidate and unchanged bootstrap head, not acceptance.
5. Stop B's finite service after its actual transfers. C freshly admits x and
   submits a small source result with a substantive reachable use of x through
   its returned formal name. Audit C's actual native plans/outputs/dependencies;
   no borrowed A/B acceptance or alias-only pseudo-reuse is sufficient.

With A's already-qualified artifact reused, the mathematical minimum is four
new stages: B bootstrap, C bootstrap, C admission, C submission. Their current
pipeline has eight children (1+1+1+5); support builds are counted separately.
B's four ordinary requests reserve 160 MiB, C's five reserve 96 MiB; four
128-MiB stage grants give 768 MiB aggregate grant charges under today's profile.
Serving sessions, actual physical bytes and CPU are separate observations.
These are prospective arithmetic, not a launch allocation or measured result.

## Critical negative discriminator and smaller controls

In a separate fresh custody fixture, after genuine acquisition and before
replica exposure, change exactly one retained inbound manifest/object byte or
remove one required inbound object. Preserve the original received pin and
candidate/ledger records. The subsequent `replica_expose` must refuse before
committing a view, without publication, candidate append, head movement or
native stage. Retain the fault and failed-request charge; do not repair it to
force the positive path. Never mutate the preserved positive fixture.

Also test the subtler substitution boundary with native-free valid framing:
a mathematically identical normalized manifest is **not** accepted in place of
the original inbound manifest when their transport digests differ. Conversely,
a legitimately received noncanonical-JSON presentation with valid canonical
objects must be re-served byte-identically if it passes the supported structural
checks. The normalized candidate may remain the same. These controls distinguish
the newly found representation issue from ordinary malformed-input rejection.

Compact native-free controls additionally cover another client's acquisition,
unknown/missing custody field, changed request/remote/entry binding, out-of-domain
paths, truncated files, foundation mismatch, resource exhaustion and replay.
Existing `expose` on an acquired-but-unpublished candidate must still refuse;
only the explicit replica operation grants its own view. A tampered committed
bundle must not produce a successful transfer, and C must never gain acceptance
from a peer metadata flag. No new feature may bypass the receiver's native path.

The exit condition is a reviewed implementation and actual bounded positive/
negative evidence for this custody boundary. This note alone establishes none
of those execution outcomes and does not close the usable-v1 goal.
