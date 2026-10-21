# Sustained custody: two bounded generation slots

2026-10-21, core_growth. Source-only response to `PLACEMENT-LIFECYCLE-NEXT.md`.
No product edit, import, execution, deletion, network call or Git mutation.

Source basis: installed114 map `d3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0`,
with selected controller `ef1c9b59`, ledger `d955990c`, guarded Store `1c8543d4`,
network service `07c60c4f`, route journal `b5523f82` and final wire `1ec5c452`.
Location sources were resolved through the map's `portable/location/*` keys,
including the fresh-path body-location controller, not their legacy namesakes.
The old two-slot retention argument/review is reused from
SELECTIVE-PLACEMENT-CONTRACT and SELECTIVE-PLACEMENT-REVIEW. Legacy HOSTING.md's
sequential finite-session slots are not generation reclamation or transferable
evidence for this seam; its quiescence-versus-lock distinction remains relevant.

## Decision

Use **two independently bounded existing placement services**, not one shared
locator. Add a small owner-local generation manager, exact managed reclamation,
and one owner-only retained-cell advertisement operation. Preserve the core
placement transaction, mathematical receiver, HTTP schemas and index format.

This is a concrete refinement of SELECTIVE-PLACEMENT-CONTRACT's two-slot
retention section, not a new retention market. Its earlier shared V1 locator
was a possible topology, not necessary for its safety or discovery argument.
The existing source makes separate roles materially simpler:

| Actual boundary | Consequence |
|---|---|
| `PlacementService.open` and `PlacementAdvertisement.open` require an exact fresh V1 index-provider with `endpoints == [read_endpoint]`. | Give each occupied slot its own exact service/Workspace/locator. A shared locator would require changing two ownership invariants. |
| The core ledger already seals to `SEALED_SERVING`; new reservations/token issuance check that state, while exact duplicates remain observations. | Reuse `controller.seal(grant)`; do not invent row eviction or make a retired token writable. |
| Each service starts a fresh in-memory grant; core and route ledgers count bounded runs. | A restart consumes new explicit run authority but preserves old grant/placement charges. |
| Selected `portable/location/controller_services.py` requires fresh state/evidence paths for each process. | Do not reuse an old Node state directory. Budget all permitted run directories, not only the mathematical Workspace. |
| Current advertisement is triggered only by a new committed submit. Duplicate/status does not publish. | Restart currently loses active discovery routes. A narrowly scoped retained-cell operation is required; reopening alone is not sustained located custody. |

Two peers on this machine are two service roles, **not independent replicas**.
There is one physical failure domain. Reader endpoint/provider budgets still
apply; doubling roles does not improve global recall by itself.

## Fixed ownership and capacity

One manager has an owner-selected ordinary root, one exclusive OS owner lock,
one small capped SQLite registry, and exactly two slot rows. The root must be
disjoint from source, installation, research/evidence and unrelated user data.
Remote input never chooses a path, slot, service limit or reclamation action.

Each slot has fixed, distinct read/intake endpoints and a separately selected
DHT listen endpoint. Both roles use the same namespace/wire policy but distinct
managed work roots and location state. No cross-generation blob references are
introduced. Duplicate content in the two slots is charged twice.

The owner reserves both slots before exposing either:

    L_0 + L_1 <= L_owner
    B_registry + B_0 + B_1 + B_cleanup <= B_owner.

Here L_s bounds that slot's advertised cells. Each B_s includes:

- All six Workspace/module/packet/index/placement/route SQLite main files,
  their rollback journals and permitted transient files, and small lock/config
  files. Immutable index history counts; logical payload quotas are insufficient.
- Every permitted run's Node metadata database and its journal, identity and
  adoption files, private-channel config/source map, bounded supervisor output
  and terminal evidence. If the generation permits R runs, reserve R such run
  envelopes. There is no unbounded `runs/` directory outside the slot.
- One bounded provisioning record and any partial-failure residue. A failed or
  partly deleted generation still occupies its slot and budget.

This deliberately needs no within-generation log compactor: choose small R,
retain its bounded records until whole-generation retirement, then reclaim
them with the generation. Existing `max_runs <= 4096` is an absolute ceiling,
not a sensible default or free disk allocation. Run reservations are consumed
before creating any run directory; unsuccessful construction consumes one too.

Physical accounting needs an explicit supported-runtime envelope, not a claim
that `max_page_count` reserves disk. The selected Node quota store fixes 4096-byte
pages and DELETE journaling. The six Python databases have page caps and DELETE
journaling, but their page size must be checked. Their placement path uses no
mathematical operation directories. The manager's launch check must bind actual
page sizes/journal modes and cover rollback/SQLite temporary-file overhead plus
filesystem allocation rounding. A journal bound must be justified for the
pinned SQLite/VFS and SQL operations; a before/after directory census is not a
transient hard quota. If that bound is unavailable, require an actual owner
filesystem quota or refuse the claimed physical envelope. Do not silently
replace it by a logical-byte cap or launch a storage-filling measurement.

This is the only physical-accounting prerequisite not already supplied by the
existing page/file caps. It does not require more RAM or a different computer.
Ordinary disk exhaustion remains safe refusal even inside a correctly bounded
allocation; allocation is not a guarantee that another application leaves
space free. Cleanup/registry headroom must remain separately funded.

## Constant-size registry and generation identity

The immutable manager configuration binds an epoch E, exact managed root,
namespace/profile, slot endpoints/caps, and clock/reclamation policy. The
registry retains only:

- `allocated_sequence` and `retired_floor`;
- two fixed slot records with sequence, generation/config digest, A_j/T_j,
  phase, consumed run count, current run/closure state, and bounded retirement
  or reclamation progress;
- bounded current owner-run authority/accounting, not an append-only event log.

Allocate a sequence in a durable registry transaction **before** creating its
root. Derive the placement generation digest from E, sequence, exact slot and
immutable configuration using domain separation. The existing placement schema
can retain its 64-hex generation field; no new peer-visible integer is required.
Never reuse a sequence, including after partial provisioning failure. Refuse
integer exhaustion rather than wrapping. New roots use deterministic exact
paths such as `slot-0/g00000000000000000007`; no user string is concatenated.

Reopen requires an exact currently registered generation with sequence above
the floor and matching config/root marker. Absence is refusal, not permission
to recreate. Old remote capabilities cannot create manager records. High-water
allocation plus exact active membership handles failed/skipped generations
without one tombstone per abandoned sequence. Advance the floor only across a
prefix containing no still-live or unretired registered generation. Retain the
current slot's RETIRED record until physical reclamation finishes.

This prevents resurrection after ordinary crashes under durable local storage.
It does **not** resist an owner restoring an old registry backup or cloning the
same epoch. Such restoration needs a newly adopted epoch and separate treatment
of retained commitments; do not claim a local counter is anti-rollback hardware.

## Lifecycle and crash order

The public states remain OPEN, SEALED_SERVING and RETIRED. Bounded internal
PROVISIONING, SEALING, RETIRING and RECLAIMING states record interrupted work.

1. **Allocate:** require one physically free registered slot, adequate aggregate
   caps, a fresh explicit owner grant, A_j <= T_j, and nondecreasing T_j. Reserve
   the sequence and full generation/run envelopes durably. Then create only its
   exact managed root and existing stores. Construction failure remains charged
   PROVISIONING/INCOMPLETE; it cannot license another hidden generation.
2. **Start:** first recover registry/store consistency without exposing any
   listener. Reserve the next bounded run, construct a fresh existing locator
   in that run's directories, and open the exact existing Workspace/config.
   Original per-generation request/grant/index/run counts never reset. New
   service authority is finite; saved monotonic deadlines are not authority.
3. **Seal:** record SEALING intent and perform the existing synchronous
   `controller.seal(grant)` only while intake/controller/advertisement are idle.
   Otherwise return BUSY under the current owner deadline; do not queue forever.
   A same-event-loop idle-check plus synchronous seal does not yield to another
   intake. Then record SEALED_SERVING. On a crash, either ledger seal or manager
   seal intent forces completion of sealing before re-exposure; never unseal.
   The read service and active routes can continue. New reservations fail;
   exact prior requests are still observations while their ledger is retained.
4. **Retire:** only after a conservative time lower bound reaches T_j. Record
   RETIRING first, preventing any new run/token/grant or re-advertisement. Close
   the exact service and drain both listeners; stop/reap its locator and finish
   every task/store close. A failed drain is not permission to close SQLite
   under a live actor or delete anything. Retain an explicit failed state.
5. **Commit retirement:** after quiescence and the horizon check, durably write
   RETIRED and the allowable floor before any unlink. A crash before this commit
   means no reclaim. A crash after it means never reopen that generation.
6. **Reclaim:** delete only the exact manager-owned retired root under a distinct
   finite reclamation authority, using ordinary-path/marker/allowlist checks.
   An interrupted deletion stays RECLAIMING and charged; resume only the same
   targets. Mark the slot FREE only after verifying their absence. A new
   generation receives a higher sequence and fresh identity.

Missing closure evidence after a controller crash is **not** evidence of an
empty process tree. Recovery needs the owning supervisor's exact run-bound
positive closure/Job-empty evidence, or a fresh bounded supervisor recovery
that establishes termination of that same run. PID absence, a released owner
lock, or a free TCP port alone is insufficient. Without this, hold the slot;
do not guess quiescence. The existing service close report and caller-required
whole-process containment are the base, not a replacement for this check.

Reclamation is a new product retention policy for newly enrolled managed roots.
It gives no authority to delete any current project experiment, package or user
directory. No archive is implicit. An optional archive needs its own bounded
quota and cannot be counted as reclaimed space.

## Conservative time and old identities

Retirement uses T_j = existing `retention_not_after_ms`, not a scan of individual
receipts. Every accepted requested horizon u satisfies u <= T_j. Therefore

    certified_lower_bound_UTC >= T_j  =>  all generation promises have elapsed.

The owner must explicitly adopt a clock-error/drift model. One sufficient model
is a valid anchor [L_0,U_0] at monotonic time m_0 with bounded rate error rho;
before the anchor's validity ends, a lower bound is
`L_0 + (m-m_0)*(1-rho)`. After restart/downtime obtain new valid clock authority
or conservatively wait. Merely taking the maximum of observed wall-clock values
does not make a forward jump safe. Uncertain clocks forbid retirement, not reads.
The current core's admission/request timestamps retain their existing wall-clock
semantics; this seam does not falsely strengthen them to strict global-UTC or
HTTP-timeout precommit guarantees.

Each occupied slot serves only its exact existing Store. Reusing its endpoint
after retirement does not rebind an old snapshot ID: old-cut requests either
find exactly identical committed content or receive not-retained/refusal. A
content-addressed identical snapshot may naturally recur; inventing a new
meaning for its identifier is forbidden. Old placement generation IDs refuse
before reservation; old hashed tokens are not copied into the replacement.

## The one required service addition: restore existing cell routes

Add an **owner-only** method, for example:

    await service.advertise_retained(request_id, until=original_run_deadline)

It is absent from the current HTTP protocol. Its caller holds fresh local
service authority for the currently registered nonretired generation. It:

1. Loads one bounded original manifest and RECEIPT_COMMITTED outcome; binds the
   exact generation/domain, derived cell, export and stored index record.
2. Requires current service/read availability and a still-supported original
   retention horizon. It does not create, extend or rewrite a placement receipt.
3. Reserves the same one-opportunity-per-cell/current-run journal row before
   issuing the existing `publish` command, inside that run's prepaid L-cell
   allowance. Failed/uncertain dispatch remains charged and is not retried in
   that run. Existing route observations are not mistaken for live Node intent.
4. Returns only a current route facet: it is not a new custody acknowledgement,
   mathematical warrant or proof of successful remote discovery.

It must **not** call the existing `_publish` with an old publisher policy: that
guard correctly requires the publisher's original write/admission windows and
would prohibit sealed-generation restoration. Give restoration an explicit
separate owner-service guard, while preserving all original submit guards.
No duplicate/status request triggers restoration, and no old token can call it.

At start the manager selects at most L committed representatives through bounded
ledger rows/cells, not a scan of global mathematics or all proof ancestry. It
can choose representatives still within their original horizons. A cell with
only partial placements is not silently promoted to successful custody. The
route itself remains advisory; clients perform existing exact readback and
mathematical acceptance. If stronger new custody acknowledgements were wanted,
fresh funded readback would be a separate action, not this restoration API.

Stopping slot 0's locator stops its own renewals only; slot 1's independent role
retains its intent for any shared cell. No cross-slot reference count or union
withdrawal algorithm is needed. Stale hints remain bounded misses. Two matching
slots consume two real contacts in the reader's aggregate budget.

## Concrete source/API cut and minimum checks

If selected, place fresh successor sources in `software/v5/placement_lifecycle/`:

| Source/API | Responsibility |
|---|---|
| `placement/lifecycle.py`: `ManagedGenerations.open`, `allocate`, `reserve_run`, `seal`, `begin_retire`, `commit_retired`, `status` | Owner lock, fixed two-row registry, identity/floor, aggregate quotas, durable phase order and clock/closure guards. |
| `client/serve_generations.py`: finite `start_slot` / `close_slot` | Compose at most two exact existing placement services with disjoint endpoints/paths; expose no central network directory or new remote authority. |
| Fresh `placement/advertisement.py` and `client/serve_placement.py` successors | Only the owner-only retained-cell route operation and its finite accounting; preserve ordinary submit/status behavior. |
| `placement/reclaim.py`: `plan_retired` / `reclaim_retired` | Exact retired path manifest, finite deletion budget, conservative restart, no links/aliases/unknown files and no recursive broad-root operation. |

No core controller/ledger/codec, verification, fingerprint or immutable-index
format change is required by this composition. Operator wrappers may reuse
public `controller.seal(grant)` without modifying its implementation. Only the
current-source successors can be edited after root selection; used files freeze.

Use one tiny fixture and changed-boundary controls, not another proof campaign:

1. Fill/seal first slot; second admits while first still serves exact retained
   data. Both occupied refuses a third root and preserves all reservations.
2. A restart uses fresh run directories/authority, charges another bounded run,
   and restores a committed cell; old token new-write and duplicate republish
   remain refused/no-effect. Run-cap exhaustion neither resets nor creates files.
3. Retire with a deliberately uncertain/too-early clock or live actor: no delete.
   Inject crash boundaries before/after durable retirement and during deletion:
   no reopen, no free slot until absence, no lost charge or third root.
4. Reuse the endpoint with a fresh generation; stale tokens/cuts cannot bind new
   content. Same-cell other-slot service remains intact when the old role stops.
5. Reject foreign root, marker mismatch, links/reparse points, unexpected files,
   missing quiescence and absent journal/temp budget. An undeletable file leaves
   a charged quarantined slot, never a fabricated reclamation success.

The guarantee is conditional sustained operation: if each generation's bounded
accepted load fits its allocation, owner service/clock/cleanup authority remains
available, and an expired slot is reclaimed before another is needed, then
successive fresh generations can continue within the fixed two-slot disk bound.
Otherwise the system refuses admission. This is neither perpetual retention nor
unconditional uptime, independently replicated custody, or net useful-growth
evidence. It closes a specific reason a working custodian would otherwise stop
accepting contributions permanently as its immutable history fills.
