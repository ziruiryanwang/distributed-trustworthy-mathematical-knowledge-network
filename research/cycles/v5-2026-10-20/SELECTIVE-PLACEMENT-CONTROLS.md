# Focused owner-local placement controls

2026-10-21, core_release. Source-only harness under root's assignment following
`SELECTIVE-PLACEMENT-SELECTION.md`. No product import, test, proof, native process,
network, build, or Git mutation has been performed by this agent.

Harness: `software/v5/selective_placement/controls.py`, 32002 bytes, SHA-256
`819bdf189e208e9974bcf7354d80f470113353a423994887fbd24d405c43e299`.

The harness is stable for independent source review. Root owns its fresh selector,
fixed outer allocation and any later launch. Proposed outer ceiling is 60 CPU
seconds / 120 wall seconds / 384 MiB / two processes. No work has been executed
to establish either elapsed cost or a passing result.

## Source closure and small fixtures

Stage the current 114-source map `d3519be1` with its exact 2805479-byte map bound.
Replace the three qualified phase/import/incremental-receiver sources with
`ac7ed228...`, `8a831337...`, `54365699...`; replace the discovery Store with
`1c8543d4...`; add placement marker `8fe08470...`, codec `6f32569d...`, ledger
`d955990c...`, controller **`ef1c9b59...`**. The final selected logical tree has
118 files. Only the map plus the normal pinned Python runtime are external inputs;
no retained proof, distribution recopy or historical test module is needed.

Each fixture genuinely opens the selected conclusion-fingerprint Workspace,
its owner lock, module/packet/index SQLite stores, and PlacementLedger through
their real APIs. PlacementController/service/token issuance are real. A tiny
one-declaration structural module has a genuine group commitment, export address,
conclusion fingerprint and index record. Optional body fixtures carry a genuine
descriptor/body hash binding. Its terminal-I envelope contains **inert fabricated
receipt bytes**: no issuer is constructed or called, and no mathematics is
asserted. Structural custody and indexing of untrusted evidence are precisely
the product boundary under test.

For pull controls, separate real source ModuleStore/PacketStore instances feed
the real CompositeProvider dispatcher. Only the two transport `exchange`
functions are replaced by explicit in-process delivery. Requests, exact returned
bytes, real acquisition budgets, canonical parsing, offers, custody commits,
readbacks and index writes remain in the product path. The simulated exchange
validates the original endpoint and a separate SQLite connection observes the
committed reservation/PULLING phase before every delivered request. It returns
synthetic HTTP accounting; those counters are not physical wire measurements.

No provider starts a listener. The harness blocks subprocess creation, shell
launches and mathematical `receive`; each async test also blocks actual sockets,
connections and servers **after its event loop has created its local self-pipe**.
This permits normal asyncio setup/teardown without permitting product network
access. No complete old test suite runs or supplies fixture authority.

## Twelve changed-boundary methods

| Method | Required observations |
|---|---|
| Reserved pull/custody/index | Reservation visible from an independent connection before all four simulated group/offer/packet/body requests; actual custody and index; INDEXED_UNADVERTISED / INTENT_ONLY / stripe zero; no verification allocation consumed; no raw bearer token in ledger bytes. |
| Exact request duplicate, expiry/restart | Completed request is observation-only with custody readback/index explicitly forbidden; same outcome under write-expired and fresh-runtime owners; old token cannot start a distinct request; no renewed charge. |
| Distinct request, identical content | New token yields a distinct request/reservation; actual local readback occurs; no fetch or duplicate store/index growth; new-cell charge stays one. |
| Corrupt group/packet/body | Deliberately corrupted retained SQLite value refuses, remains charged/incomplete, never becomes a missing-object fetch, and never enters the index. |
| Exact bindings | Wrong namespace/profile/generation/cell refuses before funding; a well-shaped but false derived fingerprint refuses after reservation; locally held packet for another module cannot satisfy this target. |
| Both Store commit hooks | Raising real `before_commit` during fresh admission rolls back all index state; raising it on duplicate admission also runs inside the transaction and preserves the prior exact index. |
| Partial commit and recovery | Injected receipt-finalization failure leaves real committed index/custody and an incomplete ledger outcome; exactly prepaid local reconciliation succeeds after write/admission expiry but before retention, with no acquisition object or extra funding. |
| Failed recovery exhaustion | Interrupted pull retains a group but not its packet; local-only recovery consumes the durable slot before failing; subsequently filling local custody cannot authorize a second recovery or reset resource charges. |
| Nested custody commit guards | Test-only horizon crossing at the actual group/packet/body COMMIT callback exercises the original composed owner guard; transaction rolls back, no index entry appears, and the reservation remains charged. |
| Cleanup failure propagation | Injected acquisition-close failure overrides both a pending success return and an earlier pull error; exact request/historical receipt state and original failure context remain available; the affected service is closed. |
| Original limits | Zero storage allowance refuses before effects; exhausted call cap, original CPU/wall limits, finite durable runtime count and expired retention refuse without replenishment. |
| Seal and exact owner registration | Simultaneous second ledger/controller refuses; sealed generation serves duplicate status but cannot start a fresh request or increase funding. |

Fault injections alter only fixture data, simulated absolute clock observations,
specific before-COMMIT/finalization callbacks and close behavior. They are not
production fallback paths, performance measurements, forced valid handles or
checker substitutions. Real request manifests remain canonical, exact grants
remain controller-issued, and real storage/rollback behavior is retained.

## Outcomes and scope

The final `placement-controls-result.json` records the exact selected source
map, twelve named methods, success/error counts, simulated exchange counts,
unexpected loop errors and any forbidden-call attempts. A pass requires all
twelve methods, no skips, no forbidden effects and no loop errors. Every created
controller, store and Workspace is closed at teardown; SQLite state is retained
as bounded evidence rather than deleted.

This gate tests owner-local durable placement semantics. It does not qualify
HTTP/TLS authentication, network delivery, DHT advertisement, retention repair,
rollover/physical reclamation, mathematical validity, independently hosted
operation, full-cost growth or complete v5. No fabricated receipt or report may
be reused later as acceptance authority. Product source review, harness review,
launch selection and actual outcome audit remain distinct.
