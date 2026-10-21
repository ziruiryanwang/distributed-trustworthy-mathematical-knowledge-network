# Fixed-layout reclamation: independent source review

2026-10-21, `support_guest`.

Disposition: **PASS_SELECTED_SOURCE_NOT_DELETION_EXECUTION**. The exact fixed
layout, prepaid-window recovery and slot-freeing order meet the selected
supported-owner boundary. No remaining source blocker was found. Controls,
genuine service-close integration and any actual fixture-only deletion still
require their separately reviewed exact selections; this note invokes none.

## Pins and preserved base

- Fresh `software/v5/bounded_reclamation/placement/lifecycle.py`, 36902 B:
  `d59615b664ca8dc934d07778046164313d226965cc3b2486e1e98d15bd57d9ef`.
- Fresh adjacent `reclaim.py`, 12387 B:
  `19713fc4baec821a5c77a0071182c63401b292cbe79a7ed7c04b7deba50e1894`.
- Author `BOUNDED-RECLAMATION-SOURCE.md`:
  `22371d6603283a78a0c1a9dc1b9a3d4d0bb94235c8a79ea6181f7c4069a0befb`.
- Adopted design `BOUNDED-GENERATIONS-RECLAMATION-DESIGN.md`:
  `9543abad206e63a14b707f1a3388aebd64c572c9befa47be10206a321a9ec3dd`.
- Frozen lifecycle base:
  `6852b5a20d4b188d328c5554f40e0bdfb2b20f84943ac689350459a5e8b2f90d`.
- Reused unchanged composer:
  `404365849dd0e41860ba8ccda01a5b064d028241a2d8b0063d76936fcd306687`.

The complete selection/design/checkpoint, helper and lifecycle delta were read.
An independent ordered diff confirms only selected reclamation additions:
docstring/import/schema, stored facet/phase validation, retired lookup/floor
treatment, read-only planning/status and the two new public methods. AST-level
method comparison confirms the only changed existing methods are `_records`,
`_find`, `commit_retired`, `plan_reclamation` and `status`; the only additions are
`begin_reclamation` and `reclaim_step`. Startup, clock, retirement intent, exact
actor close and release code are unchanged, including all three prior fixes.
Both fresh files parse successfully. No product import or test was performed.

## Ownership and exact deletion domain

The new manager schema prevents old roots from silently acquiring cleanup
authority. Fresh-root creation, exact manager/generation markers, current
registry membership and derived identity remain prerequisites. Beginning
cleanup requires durable RETIRED, NONE or genuine CLOSED, no current handle
and a recorded retirement lower bound at least the original horizon. UNKNOWN
is never accepted as closure; imported reports or free locks/ports are not a
substitute. `begin_reclamation` itself performs no deletion.

The fixed source-generated layout has exactly `20 + 9R` roles for durably charged
runs R, at most 36884. It enumerates six exact workspace SQLite files and their
optional DELETE journals, the owner lock, five workspace directories, marker
and generation root; each charged run adds six exact locator/channel files and
three directories. WAL/SHM, arbitrary logs/backups, unknown run directories and
extra sibling generations are not admitted. `workspace/operations` is empty
by inspection: it has no allowed child names.

Census rejects unknown/excess children before descending. Known entries must
have their specified regular-file/directory kind; symlinks, junction/reparse
entries and regular files with multiple hard links refuse. No suffix glob or
arbitrary caller path reaches the executor. Only small exact markers are read;
database contents are not hashed or mathematically rechecked. The current
regular-file apparent-byte sum is bounded by the immutable profile ceiling.

Manager, slot and generation `(st_dev, st_ino)` identities are nonzero and bound
to the intent. The selected slot must contain only its registered generation
or, after permitted final removal, be empty. The other slot is not traversed or
modified by cleanup. Each effect rechecks exact ordinary ancestry, root identity,
kind, aliases and current finite authority, then verifies target absence.
Files are unlinked explicitly; directories use nonrecursive `rmdir`. The
generation marker must be the sole remaining child when removed; root is last.

This safety argument expressly requires the adopted private enrolled tree with
no other writers, restorers or namespace renamers. Per-file original identities
and lengths are not persisted, so arbitrary hostile same-name substitution is
not claimed detectable. Ordinary-path rechecks are not same-user OS isolation.
Unsupported identity or unexpected data holds and preserves the slot; it does
not broaden the deletion domain.

## Durable order and recovery

The initial full census is committed as RECLAIMING with immutable profile,
presence bitmap, manager/slot/root identity, marker binding and bounded facet.
This remains both retired for non-resurrection/floor purposes and occupied for
capacity purposes. The actual encoded facet and full-record size are checked,
not inferred from the maximum bitmap estimate.

Every valid admitted reclaim step durably consumes one original profile call
before census. This is the author's final accounting correction: the earlier
draft charged only after census, permitting repeated failed censuses across
manager sessions without consuming that per-generation allowance. The final
source retains the previous prepaid window during this first charge. A census
or reconciliation refusal now stays charged; there is no reset on restart.

Reconciliation requires every entry before cursor absent, every entry beyond
the prepaid window at its original presence, and only an already-deleted prefix
of originally present entries inside the window. Original absences cannot
become new deletion targets. It computes the surviving suffix before a second
transaction commits the next exact window. No unlink/rmdir precedes that window
commit. Failure/commit uncertainty leaves charged intent or poisons the session;
best-effort failure recording never restores files or asserts FREE.

An interrupted unlink can therefore be recovered without repeating an absent
effect. Marker absence is accepted only after its prepaid position; root
absence is accepted only when reconciliation permits the final removal. An
empty replacement root fails its original identity. If the root disappeared
before its authorized turn, future-presence checks refuse. If the whole final
window already completed but cursor/FREE did not commit, a fresh charged step
may reconcile an empty remaining window and confirm the same root absence.
That confirmation still consumes an original cleanup call; exhaustion holds.

After a completed window, a second census verifies its entire authorized prefix
absent before cursor advancement. FREE requires exact `lexists(root)==false`,
ordinary unchanged manager/slot ancestry and no unexpected sibling, checked
again inside the slot-clearing transaction. Only the selected slot row is
cleared. Sequence, horizon, retired floor and the other slot are unchanged;
later allocation uses a strictly higher sequence and old identity fails exact
membership. No tombstone/event history grows per reclaimed generation.

## Resource and qualification limits

The algorithm honestly performs O(N) census before and after each step, plus its
bounded window effects. W steps cost O(NW), not amortized O(N) for tiny windows.
A small one-window generation is O(N). Temporary bookkeeping and durable bitmap
are bounded; there is no recursive unknown-tree walk, payload-wide hash sweep,
proof run or global-history scan. Finite call/CPU/deadline authority bounds
attempts; failures can permanently occupy a slot when that allowance is spent.

Logical byte/entry/page bounds are not a physical disk quota, reserved free
space or NTFS metadata/COW theorem. `physical_envelope_adopted=false` and unknown
actor recovery remains unsupported. The earlier actual twelve controls do not
exercise this fresh source. New controls must use only newly enrolled disposable
fixtures and must label injected crash/link/clock/commit faults. A synthetic
nonzero layout cannot create a positive actor-closure warrant. Genuine service
close-to-reclaim integration is a separate review/execution boundary.

All review work was read-only source/hash/AST analysis. No deletion, service,
network, native/verifier/proof, test execution, installation change, migration
or Git mutation occurred. Root owns later exact fixture authorization and
adoption; this source pass is not sustained-use or full-v5 qualification.
