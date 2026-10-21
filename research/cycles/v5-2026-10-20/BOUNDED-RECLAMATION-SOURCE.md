# Closed-generation capacity reuse: selected source

2026-10-21, core_release. Under
[the root's exact source selection](BOUNDED-GENERATIONS-RECLAMATION-SELECTION.md)
and [the adopted layout/crash design](BOUNDED-GENERATIONS-RECLAMATION-DESIGN.md)
(`9543abad206e63a14b707f1a3388aebd64c572c9befa47be10206a321a9ec3dd`).

**Implemented and source-inspected; independent review and execution pending.**
No product import, test, deletion, runtime, installation, migration or Git
mutation was performed. This source has no authority to delete existing
project/experiment/product/user data. Later deletion controls require root's
fresh disposable-fixture selection.

## Exact source and preserved base

| Relative canonical path | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/bounded_reclamation/placement/lifecycle.py` | 36902 | `d59615b664ca8dc934d07778046164313d226965cc3b2486e1e98d15bd57d9ef` |
| `software/v5/bounded_reclamation/placement/reclaim.py` | 12387 | `19713fc4baec821a5c77a0071182c63401b292cbe79a7ed7c04b7deba50e1894` |

Lifecycle derives from the final now-frozen `bounded_generations` base
`6852b5a20d4b188d328c5554f40e0bdfb2b20f84943ac689350459a5e8b2f90d`.
A read-only exact diff confirms changes only in these regions:

- Module docstring/import and a new manager schema.
- Stored reclaim-facet validation and RECLAIMING as a retired, occupied phase.
- Active lookup/floor treatment of that phase.
- Updated read-only plan description, two public reclamation methods and the
  status capability flag.

All startup, retirement, clock, exact actor close, run charging and lock-release
code remains unchanged. In particular, final `_started` phase/live-authority
guards, monitor wake without premature `_closing`, and partial release handling
are preserved. The exact existing composer remains reused unchanged:
`bounded_generations/client/serve_generations.py`,
`404365849dd0e41860ba8ccda01a5b064d028241a2d8b0063d76936fcd306687`.
These two fresh files are logical `placement/lifecycle.py` and
`placement/reclaim.py`; neither is installed into the consolidated candidate.

## New-root enrollment and owner interface

The manager schema is now `DMKN_V5_TWO_GENERATION_MANAGER_RECLAIM_V1`.
An original manager root/marker/config therefore fails exact schema/config
binding rather than silently acquiring cleanup authority. A newly created
manager still requires an ordinary fresh root separated from protected roots.
No automatic old-root upgrade or migration is provided.

```python
profile = {
    "layout": "DMKN_V5_CLOSED_GENERATION_LAYOUT_V1",
    "ownership": "PRIVATE_ENROLLED_NO_OTHER_WRITERS_OR_RESTORES_V1",
    "max_calls": 8,
    "max_entries_per_call": 128,
    "max_apparent_bytes": selected_finite_slot_byte_ceiling,
}
# Existing retirement first establishes original horizon and NONE/CLOSED.
manager.begin_reclamation(generation, profile)
outcome = manager.reclaim_step(
    generation, max_entries=128, deadline=fresh_finite_monotonic_deadline)
```

Profile fields are exact. Calls are 1..8192; entries per step are 1..36884;
apparent bytes are 1..the original slot's `reserved_bytes`. These are immutable
per-generation caps, not a budget that reopens after restart. `begin_reclamation`
performs no unlink. It requires already RETIRED, run NONE or genuine CLOSED,
no current handle, valid retirement lower bound, exact initial marker and a full
known-layout census. UNKNOWN closure remains held. No timestamp or close-looking
dictionary can bypass the existing retirement/closure protocol.

Each reclaim call also consumes the manager's finite owner-call authority and
must fit its current deadline and CPU allowance. A fresh step deadline cannot
exceed the manager deadline. Restart never adopts persisted execution deadlines.
Even pure final absence confirmation consumes a reclaim call; exhausting the
original cap conservatively holds the slot rather than granting extra attempts.
Operators should select an adequate finite cap, including interruption margin.

## Fixed deletion domain

`reclaim.layout(charged_runs)` is a source-defined sequence, not caller paths:
13 workspace files, 5 workspace directories, marker and root, plus 6 files and
3 directories per charged run. Exactly `20 + 9R` roles, at most 36,884 for
R <= 4096. It matches the adopted source-derived database/journal and locator
layout. `workspace/operations/` is allowed only empty. File contents remain
opaque except exact small manager/generation markers.

Census visits only the exact known directories with bounded `scandir`. The
first unknown/excess child refuses before descent. Only exact optional DELETE
journals are allowed; WAL/SHM, extra runs, arbitrary logs and backups are not.
Ordinary ancestry, regular-file/directory type, reparse/symlink refusal and
single-link regular files are checked. Unknown siblings in the selected slot
also refuse; no part of the other slot is traversed or modified.

The manager/slot/generation filesystem identities are nonzero `(st_dev,st_ino)`
pairs and remain bound to the cleanup intent. Unsupported or changed identities
hold. Initial per-file identities and lengths are **not** persisted. Consequently
the implementation does not claim to detect an arbitrary same-name substitution
of an allowed file by a hostile concurrent writer. It requires the explicitly
adopted private-tree/no-other-writers/restores premise. Rechecking paths is not
hostile same-user filesystem isolation.

## Durable protocol and failure argument

The slot facet contains exact layout/profile/root/marker/ancestor bindings,
original presence bitmap, cursor, current prepaid window, charged calls and
one bounded failure code. Its binding digest covers immutable fields, not the
mutable cursor/call accounting. Both the facet's actual encoded size against
`cleanup_reserved_bytes` and the entire record's 131072-byte bound are checked.
The maximum original-presence bitmap is 4611 bytes / 9222 hex characters.

1. After the full initial census, persist RECLAIMING and its original inventory
   before any filesystem mutation. The slot remains occupied and retired for
   floor/non-resurrection purposes.
2. At each admitted fresh call, durably charge one original cleanup call before
   census, retaining the old window. Thus a refused census also stays charged
   across manager restart. Census the exact finite layout and reconcile the previous
   prepaid window. Entries before the cursor must stay absent; entries beyond
   the window must retain original presence. Within the window, originally
   present entries may have lost only a prefix, followed by an undeleted suffix.
   Original absences cannot become new deletion authority.
3. Commit the new `[cursor,end)` window before effects. Missing
   original roles are skipped, not created. Known present files are unlinked by
   exact paths; directories are removed nonrecursively, child before parent.
   The marker is retained until it is the sole child; root is last.
4. Before each effect, recheck ordinary exact ancestry/root identity, current
   finite action authority, type and aliases. After each effect verify exact
   absence. After the window perform another full census and confirm the entire
   authorized prefix is absent before advancing its durable cursor.
5. FREE requires actual absence including no dangling link, unchanged ordinary
   manager/slot ancestry and no unexpected sibling. These are checked again
   inside the slot-clearing transaction. Only this one slot is cleared; sequence,
   horizon, retired floor and other slot are untouched.

An interruption after unlink and before cursor commit therefore retains the
prepaid window and slot charge. Restart can reconcile exactly that prefix,
including marker/root removal, without restoring anything. Unexpected holes,
new files or changed identities refuse. Commit uncertainty uses the existing
manager poison rule. Failure recording is best-effort under current authority;
the already committed call/window remains authoritative if recording itself
fails. A new allocation after FREE still uses a strictly greater sequence and
derived identity; old identifiers no longer match any active record.

## Cost and remaining boundary

With N fixed layout roles, each census is O(N) metadata work and O(N) temporary
bounded bookkeeping, with a finite constant cost for current manager checks and
small marker reads. Each step has a before/after census and at most its selected
window's exact effects. W calls therefore cost O(N*W); it is not amortized-linear
over arbitrarily tiny windows. A normally sized generation fitting one selected
window requires O(N) work. There are no database-content hash sweeps, Lean runs,
global-history scans, growing event logs or recursively enumerated unknown trees.

Apparent bytes/entry counts and SQLite page bounds remain logical observations,
not physical disk quotas, free-space guarantees or hostile-writer containment.
`physical_envelope_adopted` stays false, as does unknown-actor recovery support.

Independent review should now challenge actual deletion-domain, charged-window,
marker/root recovery and slot-isolation ordering. Focused controls must use only
fresh deliberately enrolled disposable fixtures. Legitimate zero-run NONE
retirement is the first positive path; synthetic nonzero layouts cannot certify
real service closure. Genuine service-close-to-reclaim composition remains a
distinct future boundary. No worldwide availability, net useful-growth or full
v5 completion claim follows from this source cut.
