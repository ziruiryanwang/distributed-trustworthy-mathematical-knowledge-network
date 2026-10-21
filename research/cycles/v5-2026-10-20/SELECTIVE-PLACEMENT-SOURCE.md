# Owner-local placement source checkpoint

2026-10-21, core_growth. Source only under SELECTIVE-PLACEMENT-SELECTION;
corrected contract `fbbb47b4`, proposal `93b86755`, review `0997105b`.
No imports, compilation, tests, service processes, network calls, mathematical
verification, proving, installation or Git operations were performed.

## Exact files and ownership

Under `software/v5/selective_placement/placement/`:

| File | Bytes | SHA-256 |
|---|---:|---|
| `__init__.py` | 78 | `8fe08470d7fd15e96d1305f0e49a8b359cb53ce0c542bf7473b68d869159112e` |
| `codec.py` | 6363 | `6f32569d4807f96130350b85233161603f6860f082c75f81a8bfacf4f0a58999` |
| `ledger.py` | 12537 | `d955990c347ed466617c752893dded8b8494dd266a050b045352c77c48f21a91` |
| `controller.py` | 18192 | `ef1c9b59072127379e955bafeea001a22d6e3d10c9c46dca1304f85ab09e2b49` |

Root separately owns `selective_placement/discovery/discovery_store.py`,
SHA-256 `1c8543d4903754174b80d107ee923116ddb402d41a3b5af3f1d255abdfc6a328`.
Its backward-compatible `admit(..., before_commit=None)` is required. No
Workspace fork, transport mutation or monkeypatch is introduced. All other
dependencies resolve through the current 114-source map `d3519be1`.
Independent source review belongs to adaptive_audit; root alone adopts/executes.

## Callable boundary

```text
PlacementLedger.open(exact_workspace, config, create=False)
PlacementController(ledger, owner_egress_config)
controller.start_service(wall_seconds=600, controller_cpu_seconds=120, calls=128)
controller.issue_token(service, source, write_until_ms=..., retention_until_ms=..., limits=...)
await controller.submit(service, token, canonical_manifest_bytes)
controller.status(service, token, request_id)
await controller.reconcile(service, request_id)
controller.seal(service)
controller.close()
```

One exact fingerprint Workspace must already be open through its existing
owner-lock/configuration API. Its module/packet/index stores are used directly;
no mathematical client, verifier, receipt issuer or preparation owner is made.
Only one live placement ledger may register on that Workspace, and one
controller may register on the ledger. Captured roles and lock are checked by
identity. Closing placement does not delete or close the external Workspace.

The endpoint is **INDEXED_UNADVERTISED** with route **INTENT_ONLY**. This is a
real owner-local reserve/pull/custody/index/record transaction, not a remote
placement ACK or DHT discovery demonstration. It is the core to be reused by a
later closed remote handler, not a competing manual-only publication design.

## Inputs, tokens and exact bindings

Codec schemas are closed and bounded. Config fixes service epoch, generation,
namespace, wire profile, absolute admission/retention bounds, finite ledger
pages/grants/requests/cells/runs and aggregate resource authorization. Requests
are canonical bytes capped at 16 KiB. Their export-object hash is explicitly
over `adapter.encode_opening(module, name, opening)`, not the HTTP group response.
Declaration wire ceiling and exact packet bytes/hash are separate fields.
Up to eight selected body hashes/ceilings are allowed; no recursive retrieval.

Tokens are random 256-bit secrets; only their SHA-256 is stored or used as a
grant identifier. Token issuance is local under an exact live service object.
The fixed source endpoint is obtained through the adopted OwnerEgressPolicy,
not from a request. This first source uses its existing system-CA/public-IP
or explicitly allowed loopback-test behavior, without adding a CA discovery
mechanism. No token appears in persisted manifests, results or diagnostics.

The proposed fingerprint/cell is checked structurally before reservation; after
acquisition, the actual fingerprint is independently extracted from the committed
opening and must match exactly. The actual compiled fingerprint ID yields the
stripe-zero route. The exact packet's structural target must match the opening
summary. False but structurally valid evidence remains untrusted and may consume
its authorized storage; only existing later mathematical receivers decide use.

## Authority and restart

Persistent service epoch is not live execution authority. `start_service`
creates one exact controller-issued object and random runtime identifier, under
original monotonic deadline, process-CPU limit and call count. A finite durable
run count prevents silent unlimited generations of that authority. Neither
deserialized JSON nor a copied grant object can start work.

Token writes require the issuing runtime to be current and their original
absolute write/admission/retention bounds to hold. Tokens from earlier runs, or
past write expiry, can only obtain a retained request's status. New token writes
require explicit fresh local issuance; there is no old-token re-adoption path.

An exact duplicate **request** returns its existing ledger outcome, without
custody readback, network work, new row, renewed lease or replenished reservation.
A distinct request for identical **content** is different: it receives its own
bounded reservation and may reuse existing committed bytes after genuine local
readback. This content deduplication does not require a fabricated fresh offer.

## Ordering and failure

Request identity binds manifest hash/length, grant and generation. All request,
byte/work, index, ledger and potential new-cell authorizations are transactionally
reserved before acquisition. The reservation persists on failure. Ledger
phases are RESERVED, PULLING, CUSTODIED, INDEXED and RECEIPT_COMMITTED, with
explicit incomplete/recovery phases. Separate store transactions are not rolled
back globally; a crash can leave real retained bytes or index state before the
receipt ledger catches up.

The exact original controller guard is composed into a private
`_OwnedAcquisition._active`, preserving the existing declaration/packet/body
before-COMMIT hooks. `_Contact.validate` applies the owner guard and adopted
egress policy at every inner structural dial. The exact original AcquisitionBudget
still enforces requests/replies and deadline; no subclass/forged budget or
verification allocation is used. Every ledger COMMIT and both index COMMIT
branches use an owner guard. The request-specific guard checks original write,
admission and retention bounds dynamically, not merely sampled `now_ms`.

Exact-key existence/size reads distinguish genuine local absence from corrupt
group, packet or body state before bounded normal validators read it. A size
conflict, missing related group, invalid commitment or malformed retained value
refuses; it is never converted into a network cache miss. Remote packet fetches
still require a real bounded offer from the selected fixed source.

Reconciliation is explicit owner work and local-only: no acquisition object,
endpoint or network operation is constructed. Its single prepaid recovery slot
is durably consumed before reading. Missing data produces incomplete status;
there is no hidden retry. Even if a recovery crashes, its slot stays consumed.
Initial and recovery passes each receive half the original structural-input
allowance; neither can reset the total. Each can invoke index admission at most
once, matching the two reserved calls. Original retention bounds still apply,
but explicit recovery may finish retained partial work after write/admission
expiry. No lease or token is revived.

When authority expires, even failure reporting may no longer COMMIT; the older
durable phase and reservation then remain the honest uncertain outcome. The
caller can later inspect it under a fresh explicit service grant. A successful
receipt/result never claims cross-database atomicity or future availability.

The narrow cleanup correction propagates an acquisition-close failure as
`PlacementCleanupError`, even if the body had already committed its receipt and
was about to return success. It invalidates the service and clears transient
controller state. The exception exposes `request_id`, `receipt_committed` and
`original_error`, with the close failure as its explicit cause; a preceding body
failure is therefore retained as well. The error explicitly states
`DURABLE_STATE_NOT_ROLLED_BACK`: custody, index state and any saved receipt remain
historical facts. A later explicit service may inspect that state, but the failed
call cannot silently return `INDEXED_UNADVERTISED`. This is source correction,
not an executed cleanup qualification.

## Resource semantics and source-derived index bound

The resource vector is **cumulative nonrefundable funded authorization**, not a
filesystem reservation or a guarantee that a placement will fit. Immutable
module/packet/index logical quotas and SQLite page caps govern actual capacity;
the new ledger also has its own page/row caps. Capacity failure is permitted and
retains its charge. No quota is enlarged, and no packet is copied anew merely
because another export points to it. Results separately expose before/after
store counts and known-new logical bytes; funding ceilings are not observations.

Instead of always reserving an arbitrarily large complete index, the source
uses the lesser of that index's logical ceiling and this per-export bound:

```text
128 * (260 + 9 + 22) * 4096 + 16384 + 4096
```

Reason under the selected authenticated-index source:

- At most 128 extracted features are admitted.
- Each compressed map update visits at most 256 bit positions. It writes at
  most one node per traversed ancestor plus a leaf and bounded split/suffix
  nodes; 260 is a conservative allowance.
- Each partition update writes one leaf and eight fixed-depth ancestors.
- The vector maximum is 1,048,576, hence height at most 20. Appending writes
  at most a leaf, 20 ancestors and one height-growth node: 22.
- `Store.put_node` bounds each encoded node by 4096 bytes. The record is at
  most 16 KiB; the selected bounded snapshot descriptor fits the extra 4096.

This bounds new charged index logical bytes, including immutable history, not
database page overhead. Module/packet/body allowances and bounded receipt/ledger
overheads are additional. A committed initial index admission followed by
recovery of the same record takes the duplicate path; it does not create a
second new record/history chain. A rolled-back initial index write consumes
work but not committed logical capacity. Smaller future charging is optional,
not required to complete this finite transaction.

`structural_bytes` counts input bytes submitted by this controller to bounded
read/validation entry points, not every internal parser traversal or CPU step.
Actual CPU is separately guarded; synchronous work is not preempted by asyncio.
The eventual external process supervisor remains required for a hard ceiling.

## Integration limits

No HTTP/TLS handler, DHT command, two-slot runner, retirement floor manager,
physical reclamation or network deployment is implemented here. This controller
can seal/reopen one finite generation and must refuse when full. It cannot be
advertised as sustained finite-disk rollover. Nor do its exact local index
readbacks prove global/provider-subset discovery, cryptographic storage,
independent custody, net growth benefit or completed v5.

Next gate: independent source review, then separately selected focused controls
for this changed boundary. No old circulation or certificate production needs
repeating to qualify the source composition.
