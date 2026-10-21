# Safe capacity reuse: exact closed-generation reclamation

2026-10-21, core_release. Source-level design only; no deletion, reclaimer
implementation, old-state migration, test execution or storage experiment.
This resolves the next API boundary after the current two-slot lifecycle.

## Decision and ownership premise

Add a small **layout-specific, nonrecursive reclaimer**. Reclaim only newly
enrolled manager-owned generations after durable retirement; preserve the two
slot charges until the exact generation directory is absent. Do not add a
general directory cleaner, glob, arbitrary path argument or retention market.

The deletion domain is a private ordinary directory created fresh under an
explicit owner allocation. The manager holds its existing exclusive lock;
source/installations, research/evidence and unrelated user data remain outside
that domain. All services/actors are closed before reclamation, and no unrelated
writer, backup restoration, hard-link importer or namespace renamer may mutate
the enrolled tree. These are explicit supported-owner conditions, not protection
against a hostile process with the same filesystem authority. Rechecking paths
alone does not solve that adversarial TOCTOU problem. A stronger threat model
would require a separately designed handle-relative/OS isolation boundary;
do not claim it here or delay this supported-owner route to investigate it.

No generation inherits ownership merely from its name. Existing exact manager
marker, registry membership, derived identity, generation marker and ordinary
ancestry must agree. A missing/foreign marker before reclaim intent is HOLD.
An absent root after a precommitted reclaim intent has a different, explicit
recovery meaning below. Partial provisioning with unknown ownership remains
charged; do not turn malformed marker bytes into deletion authority.

## Exact finite inventory, derived from the selected source

Basis: consolidated input
`8ba3707236c1a6e01ab7f87886814f801034b2fe9144ad9603585adcc73feb33`,
installed release `1fd0ae63faa84cc1f3ef82f17d2056657f8d6a3e5dea3686ace433987bd1e5be`.
Logical modules resolve through that map. Short hashes below identify exact
rows in it, not an alternate source selection.

| File role relative to generation root | Source binding |
|---|---|
| `generation.json` | Current lifecycle, `8a762cff...`; exact generated marker. |
| `workspace/owner.lock`, `workspace/workspace.sqlite`, empty `workspace/operations/` | `client/workspace_evidence.py`, `8531ee14...`. |
| `workspace/modules/modules.sqlite` | `custody/module_store.py`, `39e8eee8...`. |
| `workspace/packets/evidence-packets.sqlite` | `evidence_network/custody.py`, `c039af08...`; not the older delta-packet filename. |
| `workspace/index/discovery.sqlite` | `discovery/discovery_store.py`, `1c8543d4...`. |
| `workspace/placement.sqlite` | `placement/ledger.py`, `d955990c...`. |
| `workspace/placement-routes.sqlite` | `placement/advertisement.py`, `5aa23ee7...`. |
| `run-NNNN/location-state/identity.key`, `adopted.json`, `metadata.sqlite` | `portable/location/maintained_roles.mjs`, `128a5bd4...`; pinned base `quota_store.mjs` owns the SQLite file. |
| `run-NNNN/location-channel/config.json`, `source-map.json` | `portable/location/controller_services.py`, `eeb82d5d...`. |

Allow only the exact optional `-journal` companion of each of the six workspace
SQLite files and each Node `metadata.sqlite`. DELETE journaling does not license
WAL/SHM, backups, arbitrary temporary files or suffix wildcards. Such unexpected
files cause HOLD. No payload files are stored beside these databases by the
selected custody implementations. The controller keeps stderr in memory; this
layout does not invent permission to delete arbitrary saved logs.

Crucially, owner code can access the service's Workspace. Therefore
`workspace/operations/` **must be empty**, not merely assumed empty because the
placement path itself creates no mathematical operation. Any owner-created
operation, archive or unknown file remains preserved and blocks automatic
reclamation unless a later exact layout is separately reviewed.

For R durably charged runs, the fixed universe contains at most **20 + 9R**
entries: fourteen generation/workspace file roles, five workspace directories
and the generation root; per run, six file roles and three directories. Missing
optional/never-created roles are recorded as absent, not recreated. Only run
indices 1 through R are allowed; R <= 4096 gives at most 36,884 entries.
Enumerate each known directory once with bounded `scandir`, rejecting the first
unknown/excess entry. Do not descend through an unknown directory or reparse
point. Reject symbolic links/junctions, nonregular files, unsupported aliases
and multiple hard links. Use fixed exact names, not caller-controlled patterns.

Before deletion, collect only bounded ordinary-entry metadata: presence, type,
apparent length and supported filesystem identity. Check the owner-selected
finite apparent-byte ceiling and inventory-record bound. Hash the small
marker/layout/inventory commitment, **not all database contents**. This is an
owned-expired-data deletion boundary, not another mathematical verification.

## Registry extension and fresh authority

A fresh successor adds `RECLAIMING` to the closed phase set and one bounded
reclaim facet to its existing slot record:

- Exact layout version, generation/root/marker binding and supported root
  filesystem identity, such as nonzero stable `(st_dev, st_ino)` under the
  selected local runtime. Unsupported identity means HOLD, not PID substitution.
- Original presence bitmap, deterministic inventory length, cursor and one
  current prepaid deletion window; one bounded last-error code.
- Immutable per-generation reclaim-call cap, consumed calls and fixed maximum
  entries per call, selected before the first reclaim operation.

The 36,884-bit maximum presence bitmap is 4,611 bytes, or 9,222 hex characters.
Together with the already bounded generation configuration it fits the current
131,072-byte record ceiling; the successor must check the encoded total rather
than infer it from this estimate. No separate growing inventory/event table is
needed. Large maximum R is not a recommended allocation.

Proposed owner API:

```python
manager.begin_reclamation(generation, profile)  # closed retirement + full census
manager.reclaim_step(generation, *, max_entries, deadline)  # fresh finite authority
manager.status()  # same two slots, explicit occupied/reclaiming/free distinction
```

`profile` is one exact source-defined layout and a bounded owner allocation,
not a dictionary of arbitrary paths or a caller-authored closure report. Every
call uses the current manager's finite authority and an original-or-shorter
deadline; persisted deadlines are never live execution permission. Reserve one
call and its bounded target window durably before filesystem mutation. Failures
and uncertain attempts stay charged. Exhaustion holds the slot; no silent reset.

## State order and crash argument

1. **Retire first.** Existing `commit_retired` must already have established the
   original retention horizon through its adopted lower-bound clock and exact
   current-run closure, or no run ever existed. UNKNOWN closure still refuses.
   A saved PID, free endpoint or reacquired manager lock is not evidence. A
   retirement valid at time t stays valid later; reclaim needs fresh action
   authority, not a fabricated new clock assertion from its old timestamp.
2. **Commit intent before unlink.** Validate enrollment, marker and full finite
   inventory; durably write `RECLAIMING`, original presence bits, root identity,
   cursor and immutable cleanup cap. `RECLAIMING` remains retired for floor/
   non-resurrection purposes and occupied for capacity purposes. No unlink is
   permitted if this commit is absent or uncertain.
3. **Delete exact entries in fixed order.** Ordinary files first, then empty
   directories bottom-up; retain `generation.json` until every other child is
   gone; remove the generation root last. Invoke exact `unlink`/`rmdir` only,
   never recursive delete. Recheck ordinary ancestry, identity and inventory
   before each bounded window. A nonempty directory, unknown/reappearing file,
   link, lock, permission failure or missing identity causes HOLD.
4. **Persist a window before its effects.** A call reserves [cursor,end) before
   deleting any entry. On ordinary completion verify each selected absence and
   advance the cursor. On crash, earlier completed entries must remain absent;
   entries beyond the prepaid window must match original presence; the current
   window may contain the already-deleted prefix followed by its undeleted
   suffix. This covers an unlink that succeeded before its cursor commit without
   licensing arbitrary missing/reappearing future entries. An inconsistent view
   holds rather than guessing the previous effect.
5. **Marker/root recovery is explicit.** Missing marker is allowed only when its
   position lies in the previously prepaid deletion prefix/window. Before that
   it is corruption/unknown ownership. If the root is absent after a window
   authorized its last removal, there are no contents to traverse or recreate.
   A present root must still have the original supported identity. No empty
   replacement directory is silently adopted.
6. **Free only after exact absence.** Under the still-held owner lock, verify
   `lexists(exact_generation_root) == false` (including no dangling link),
   recheck ordinary slot/manager ancestry and absence of unexpected sibling
   generations, then durably clear this one slot record. Never clear another
   generation, lower the allocated sequence, reset history counters or infer
   FREE merely from `RETIRED`/`RECLAIMING`. Commit uncertainty poisons the current
   session. Restart observes either the same reclaiming record or committed FREE.

Before intent, a crash deletes nothing. During deletion, the retired identity,
slot charge, original presence and charged window survive. After root removal
but before FREE, restart finishes the same absence-confirmation transaction.
After FREE, a new generation uses a strictly larger sequence and fresh marker;
old IDs fail exact active membership even without one tombstone per generation.
The other slot's independent endpoint/store remains untouched throughout.

## Bound and limits

This gives a bound on **managed logical records, known file roles and retained
history**: two generation allocations plus a constant-size registry/cleanup
facet, not one permanent log per retired generation. Temporary errors occupy a
slot; they never authorize a third generation or an unbounded retry transcript.
Keep only a bounded last cleanup summary in the product; optional external audit
archives require separate allocation and cannot be called reclaimed space.

The earlier `PLACEMENT-LIFECYCLE-SPACE-BOUND.md` separately states the conditional
SQLite/VFS data-stream envelope. Entry/size observations and a page cap are not
a hard disk quota, a free-space reservation, an NTFS metadata theorem or evidence
against other writers/COW snapshots. Physical deletion effects can be uncertain
after interruption, which the state machine handles conservatively. No disk
saturation test or RAM investigation is required to implement this protocol.

## Smallest next implementation and controls

After root selection, add one `placement/reclaim.py` implementing the fixed
inventory and bounded executor; add only the reclaim facet/state/floor/FREE
transition to a fresh lifecycle successor. Reuse the current service and close
mechanism. No new network protocol, installation build, proof campaign or whole
database hash sweep is necessary.

Use newly enrolled tiny fixture roots only. Decision-changing controls are:

- Exact expired closed generation reclaims and a higher sequence reuses its slot;
  the other occupied slot and old-ID refusal remain intact.
- Early/uncertain clock and LIVE/UNKNOWN closure cannot begin deletion.
- Foreign/missing marker, root-identity change, unknown file, nonempty operations,
  link and extra run directory preserve all targets and charges.
- Crash/refusal before intent, after one unlink before cursor commit, after
  marker removal, after root removal and before FREE; resume only the prepaid
  prefix and never recreate a missing generation.
- Mid-window permission/timeout/commit uncertainty and cleanup-cap exhaustion
  leave the slot occupied; no automatic refund or third root.
- Count/bitmap/byte ceilings refuse before mutation; normal cleanup hashes only
  small metadata and does not open database payloads for a new proof check.

The deletion tests themselves require a later explicit fixture-only selection.
This document selects no deletion and does not claim the current source already
recycles slots or achieves sustained useful growth.
