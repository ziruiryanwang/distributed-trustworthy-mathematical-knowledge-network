# Owner-local selective placement: exact source proposal

2026-10-21, core_growth. Proposal for root selection **before product edits**.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
No runtime, tests, imports, Git changes, HTTP/TLS handler, route dispatch or
reclamation is proposed in this source slice.

Basis: corrected SELECTIVE-PLACEMENT-CONTRACT SHA-256
`fbbb47b449d551a9a1a675b9814b310197fc4ef499aa43be192a2ebbeccb0823`,
independent review `0997105b`, and current 114-source input `d3519be1`.
The corrected contract's restart, V1 two-slot, exact selected query source,
offline-custody, future retention, both COMMIT guards and bounded token-envelope
clarifications were read. The broad contract is not all implemented here.

## Owned product paths if root selects

All paths below are fresh under `software/v5/selective_placement/`:

| Physical file | Logical installation path | Responsibility |
|---|---|---|
| `placement/__init__.py` | `v5/placement/__init__.py` | Minimal package marker; no implicit construction. |
| `placement/codec.py` | `v5/placement/codec.py` | Closed bounded request/config/grant schemas, canonical IDs and derived-cell binding. |
| `placement/ledger.py` | `v5/placement/ledger.py` | Durable per-generation reservations, grant hashes, request phases/status, restart epochs and finite recovery accounting. |
| `placement/controller.py` | `v5/placement/controller.py` | Exact live service grant, serialized owner-local submit/status/reconcile and composition of existing structural APIs. |
| `discovery/discovery_store.py` | `v5/discovery/discovery_store.py` | Successor of selected `instantiation_discovery/discovery/discovery_store.py`; only optional pre-COMMIT owner guard. |

The Store basis is 19,728 bytes, SHA-256
`32df0e1d5be03b9bb0ac3c57f3df367857e608e4678c8ede262593ea9f65b884`.
`admit(raw, expected_id=None, *, before_commit=None)` calls the guard immediately
before COMMIT in duplicate and fresh branches. Existing default behavior,
bounded internal work, rollback and storage/proof bytes stay unchanged. No
monkeypatching or subclass substitution of exact Workspace roles is needed.

Author checkpoint after implementation: SELECTIVE-PLACEMENT-SOURCE.md. Root
owns selectors/source maps, integration and later launches. Independent author
review/controls remain separately assigned. Used predecessors stay unchanged.

## Deliberately bounded usable endpoint

One controller owns **one existing exact, owner-locked fingerprint Workspace**
and one newly created placement ledger under its ordinary root. Workspace
creation/reopen remains the existing `Workspace.open` operation; placement
does not create mathematical clients or issuer/verifier/preparation objects.
Its exact immutable configuration binds service identity, generation identity,
namespace/wire profile, admission close, retirement horizon, ledger/grant/row/cell
limits and aggregate resource ceilings. This slice can seal and reopen that
generation; it neither adds an unlimited sequence of stores nor removes data.

The successful result is `INDEXED_UNADVERTISED`: authenticated structural
custody, exact index admission and durable route **intent**, not DHT discovery,
remote acknowledgement, future uptime or mathematical acceptance. A callable
owner-local interface provides the real transaction that later remote handlers
will invoke. No second manual/index-only shortcut is implemented.

First local public operations:

- Open the ledger under the supplied exact Workspace and immutable config.
- Start a fresh finite locally issued service grant, bound to that ledger,
  Workspace identity, controller CPU/deadline and original resource allowance.
- Issue a bounded source-contact placement token; persist its hash and policy,
  not its secret. Caller receives the secret once for later submit/status use.
- `submit(token, canonical_manifest)` reserves and performs one serial bounded
  transaction, or returns an existing exact request's durable status.
- `status(token, request_id)` reads only, with no retry or authority renewal.
- An explicit owner-only `reconcile(request_id)` attempts bounded local readback
  completion once; it never dials, restarts a pull or renews the original lease.
- Seal and close without deleting any generation data.

These are local Python APIs only. Tokens are future intake capabilities, not
identity claims or mathematical authority. No caller-supplied object is accepted
as a live service grant; the original controller registers its exact objects.

## Closed manifest and commitment domains

Keep canonical input at most 16 KiB. It identifies one generation, namespace,
wire profile, module, relative declaration name, ExportID, proposed fingerprint,
one exact **encoded export-opening object** size/hash, one exact packet
size/hash, requested retention end and a small bounded list of committed body
hashes with response byte ceilings. The export-opening commitment is over
`adapter.encode_opening(module, name, opening)`, not an ambiguously named wire
group response. A separate bounded declaration response ceiling is explicit.

The immutable token policy, not the manifest, selects its source endpoint and
local egress policy. No remote CA, path, executable, trust setting, arbitrary URL,
recursive body list or budget update is permitted. Derive the actual primary
fingerprint and compiled feature ID from the locally authenticated opening;
require proposed namespace/cell to match. Cell route is the existing
`route_key(namespace, [feature_id], 0)`.

## Exact reused APIs from the selected map

- `terminal_i/client/workspace_evidence.py`: exact `Workspace` and its original
  exclusive lock, immutable config, adapter, modules, packets and index.
- `pair_planning/discovery/module_export_adapter.py`: `encode_opening`,
  `describe`, `resolve` and `compile_query`; source-derived fingerprint specs.
- `terminal_i/evidence_network/transport.py`: `EvidenceAcquisition` with no
  verifier; direct `declaration`, bounded `offers`, exact `packet`, and selected
  `body`. Use one fresh bounded acquisition budget subordinate to the current
  service grant, and original owner-approved endpoint contacts only.
- `terminal_i/evidence_network/custody.py`: selected typed `PacketStore` profile,
  `inspect`, `get`, `put`; no packet or receipt protocol changes.
- `custody/module_store.py`: `get_group`/`get_body` and commitment validators;
  existing before-COMMIT custody callbacks remain active.
- `transport/receipt_client.py`: original `AcquisitionBudget`; its positive
  verification ceiling fields do not authorize verification, and the controller
  never calls `verification`.
- The new selected Store successor's `admit(..., before_commit=active)` plus
  exact record/snapshot readback; no new authenticated-index representation.
- Existing location protocol's pure `route_key`; no channel or node is started.

For local packet reuse, distinguish genuine absence from corruption with a
bounded exact-key existence read before `PacketStore.get`, whose legacy error
otherwise combines size mismatch and absence. Never treat arbitrary readback
exceptions as permission to fetch a replacement. A positive local readback
does not need a new remote offer; an actual remote packet fetch still does.

## Durable state and accounting invariants

1. Bind immutable ledger config and generation; use finite SQLite page/row caps,
   explicit schema and ordinary managed paths. The supplied Workspace lock is
   required for every operation; no separate unlocked writer is introduced.
2. Persistent service epoch is independent of a fresh runtime grant ID. A new
   run never inherits a saved monotonic deadline. Tokens issued in an old run
   or past write expiry are status-only while retained; no old-token new-write
   readoption in this slice.
3. Request ID commits canonical manifest, grant ID and generation. Reserve its
   request/byte/structural/index/cell/ledger envelope transactionally **before**
   pull or storage. Original reservations survive failure; exact duplicates
   return their old phase/outcome without creating rows, executing or renewing.
4. Prepay a finite recovery allowance in the original request reservation.
   Persist consumption before owner-only reconciliation, allowing at most one
   local-only recovery pass. Missing bytes yield an explicit incomplete result;
   no second network attempt is hidden inside reconciliation. A crash in this
   pass may leave uncertain retained state and an exhausted recovery slot.
5. One busy slot, no automatic queue/retry. Service attempts, controller CPU,
   monotonic deadline, input/parse work and egress checks remain finite. The
   acquisition reserves worst-case requests/reply bytes; reports distinguish
   reserved ceilings, known actual work and conservatively charged unknown
   tails. Persistent token and generation counters never reset on restart.
6. Exact preexisting custody is read/validated and can avoid network requests
   and duplicate payload storage. Reserve index/history/ledger overhead as
   well as payload. Finite physical Store/packet/module quotas remain decisive;
   no per-export packet-copy requirement or cap enlargement is introduced.
7. Persist phase transitions RESERVED -> PULLING -> CUSTODIED -> INDEXED ->
   RECEIPT_COMMITTED, with `route=INTENT_ONLY`. Separate SQLite commits can leave
   partial state; no distributed rollback is claimed. Complete outcome binds
   independently derived record, snapshot, cell, exact evidence commitments,
   retention/service windows and original reservation/observation accounting.
8. Current owner guards run before every durable commit, including Store's
   duplicate branch, and before/after bounded synchronous work. Wall timeout is
   not CPU preemption. Root's eventual external containment remains necessary.
9. Every saved result sets mathematical_acceptance=false, global_complete=false,
   cross_database_atomic=false and all_future_bodies_covered=false. An existing
   index root or structural packet is never a local mathematical warrant.

## Explicit exclusions and next integration boundary

No HTTP/TLS implementation, broad auth framework, DHT publication, two-slot
runner, physical reclamation, token vending, mutable trust policy, verification,
proving or new cryptographic receipt is selected here. Fixed storage exhaustion
refuses. The full contract's bounded rollover/reclamation and network discovery
remain later integration obligations, not alleged capabilities of this slice.

After independent source review, the smallest prospective controls exercise
reserve-before-effect, exact duplicates, short-circuit custody, wrong commitments,
expired/restarted token status, cross-store interruption/reconciliation and both
index COMMIT callbacks. Root must separately select any control execution.
No new mathematics, proof campaign or full old circulation is needed.
