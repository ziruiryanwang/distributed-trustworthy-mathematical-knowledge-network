# Selective placement source review

2026-10-21, adaptive_audit. **GO for separately selected focused controls of
this owner-local placement boundary; no remaining concrete source blocker.** No
product edits, imports, execution, tests, network work or Git mutations.

Scope is SELECTIVE-PLACEMENT-SELECTION, corrected contract `fbbb47b4`, and
implementation proposal `93b86755`. This is not another architecture review.
Canonical source mapping is terminal-I114 `d3519be1`; selected transport,
custody, Workspace, adapter and Store API seams were read directly.

## Stable Store seam

Successor `software/v5/selective_placement/discovery/discovery_store.py`,
SHA-256 `1c8543d4903754174b80d107ee923116ddb402d41a3b5af3f1d255abdfc6a328`,
was compared by complete line diff with selected basis `32df0e1d`.

Only three seams change: optional keyword-only `before_commit=None`, callback
immediately before duplicate COMMIT, and callback immediately before fresh
COMMIT. Both remain inside the original rollback region, after the Store's
internal deadline guard. Callback refusal rolls back any transaction and clears
the operation-local node cache through the unchanged exception path. Omitting
the callback preserves the original behavior and storage/proof schema.

No concrete blocker found in this seam. The callback remains trusted owner
code; it adds a commit-time owner check, not preemption of synchronous work or
a hostile-code sandbox. The eventual controller must supply its exact current
service guard on both ordinary and reconciliation admission paths.

## Stable placement source

Read all four placement sources and their selected dependency interfaces; then
read the final cleanup correction and updated author checkpoint `74a72776`.
Recomputed the following full hashes after that correction. All paths below
are under `software/v5/selective_placement/placement/`.

| File | Bytes | SHA-256 |
|---|---:|---|
| `__init__.py` | 78 | `8fe08470d7fd15e96d1305f0e49a8b359cb53ce0c542bf7473b68d869159112e` |
| `codec.py` | 6363 | `6f32569d4807f96130350b85233161603f6860f082c75f81a8bfacf4f0a58999` |
| `ledger.py` | 12537 | `d955990c347ed466617c752893dded8b8494dd266a050b045352c77c48f21a91` |
| `controller.py` | 18192 | `ef1c9b59072127379e955bafeea001a22d6e3d10c9c46dca1304f85ab09e2b49` |

## Implementation argument

- **Authority:** exact locked Workspace and captured store/adapter roles, one
  ledger/controller registration, exact issued service-object identity and its
  original deadline/CPU/call bindings. Fresh runtime identity is separate from
  persistent epoch/generation; durable run count is finite. A prior-runtime
  token can observe its existing request, not authorize a new write. Only the
  token hash is persisted. The fixed source is locally selected through the
  existing OwnerEgressPolicy, not supplied by the manifest.
- **Durability and accounting:** grant/generation counters, request identity
  and potential cell authorization commit before pulls. Reservations persist
  on failure and are not refunded by retries. Exact request duplicates return
  saved status without repeating work; distinct requests for the same content
  receive separate reservations and exact local readback. Ledger row/page caps
  and immutable store capacities remain decisive.
- **Custody and binding:** explicit exact-key existence/size probes distinguish
  true absence from malformed or inconsistent retained data. Corruption is not
  caught as a fetchable cache miss. Remote packet retrieval requires a bounded
  real offer; existing valid custody needs none. The export opening hash,
  namespace and independently extracted fingerprint/cell are checked; packet
  target equals opening summary. At most eight explicit bodies are acquired,
  without recursive pulls. Index record and snapshot are read back exactly.
- **Live guards:** the private acquisition override composes controller checks
  with inherited checks; `_Contact.validate` rechecks owner/egress before each
  dial. The exact existing AcquisitionBudget is retained. Both index COMMIT
  branches, nested custody commits and ledger commits retain live owner guards.
  Ordinary write/admission/retention bounds are checked dynamically at commit,
  not only sampled when the operation started.
- **Recovery:** one original prepaid recovery slot is durably consumed before
  reads. Recovery constructs no acquisition object/contact and cannot fetch or
  reserve again. Initial and recovery passes each get half the original
  structural-input allowance and at most one of the two funded index calls.
  Root explicitly resolved the horizon interpretation: a fresh finite local
  owner may finish this prepaid local recovery after write/admission expiry,
  but never past original retention end. This neither revives an old token nor
  extends a lease. Missing data or exhausted recovery remains incomplete.
- **Cleanup correction:** `PlacementCleanupError` is now raised from any
  acquisition-close failure after invalidating the service and clearing the
  transient busy/current state. It overrides a pending success return, keeps
  request identity, whether a receipt was committed, and any original body
  exception; the close exception is its explicit cause. A durable receipt or
  custody is not rolled back or silently reclassified. Later fresh-owner status
  may inspect that history, but the failed operation cannot report clean return.

## Bounds and honest endpoint

Reviewed the source-derived new-index-logical-byte bound against the selected
authenticated index and Store: at most128 features,260 conservative compressed
map nodes,9 partition nodes,22 vector nodes per feature,4096 bytes per node,
plus16384 record and4096 snapshot bytes. This supports the selected bound
`128*(260+9+22)*4096+16384+4096`, capped by the immutable index logical ceiling.
A committed initial admission followed by recovery uses the duplicate record
path; a rolled-back admission creates no committed second history chain.

These are cumulative funded authorizations, NOT physical disk reservations or
promises of fit. Actual store/page caps can still refuse. Structural-byte
counters describe controller entry-point input, not all parser traversals;
CPU guards are separate and synchronous operations are not hard-preempted by
asyncio. Eventual external containment remains necessary for hard ceilings.

The successful result is accurately `INDEXED_UNADVERTISED`, route `INTENT_ONLY`,
with structural-custody assurance and no mathematical authority. Multi-store
transactions are not globally atomic; a crash can leave useful custody or index
state before the ledger result. Saved observations do not prove future service.
There is no HTTP/TLS placement handler, DHT dispatch, independent network
placement, rollover, reclamation or sustained finite-disk operation here.

This review authorizes no execution itself and establishes no actual runtime
pass, full-cost growth result or completed v5. The source-only outcome justifies
root selecting the focused changed-boundary controls; no old mathematics or
circulation campaign needs repeating.
