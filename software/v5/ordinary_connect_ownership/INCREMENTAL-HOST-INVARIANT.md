# Incremental inert hosting without a batch transaction layer

2026-10-28 root design correction. Read NEXT-CENTRAL-DECISION and challenged its
exact-generation premise before implementation. No runtime or database access.
The public workflow needs a custodian to retain and expose growing selected work;
it does not inherently need atomic publication of every multi-object batch.

## State and authorization

Let E be the stored inert evidence and generated export locators, P the stored
previews, and I the committed index records with immutable historical snapshots.
All are candidate mathematics. Each recipient retains independent acceptance.
The host has one permanent OS lock and fixed cumulative storage limits.

A new V2 descriptor binds implementation/profile, mathematical interpretation,
index namespace, fixed limits and an explicit policy permitting partial
publication of approved inputs. Its identity is stable across content updates;
it does not purport to identify the current collection. A service reports the
actual selected index snapshot and actual current counters separately.

Before any insertion, an append invocation must bind the selected bounded
manifest, selected targets and explicit approval to disclose all supplied units,
their export locators, and generated previews, including an interrupted prefix.
Every inserted raw unit must match that manifest. No remote automatic writes or
implicit acquisition follow from this authorization.

## Safety invariant

For every record in I, E contains its exact referenced evidence unit and export
locator, and P contains its exact preview; preview resolution and index adapter
validation establish their bindings. Each member of E/P was independently
validated as inert syntax and authorized for disclosure. These claims do not
assert that any theorem is true or that all its dependencies are available.

Initialize empty stores, close them successfully, and only then install the
descriptor. This establishes the invariant. Each append holds the same lock
used by serving and performs, for each selected item:

1. Atomically commit validated evidence together with its generated locators.
2. Resolve the selected preview against that evidence, then atomically commit it.
3. Atomically admit the preview's validated index record and snapshot.

Existing identical bytes may be reused; conflicts refuse. Data is monotone: no
supported operation deletes evidence needed by a retained record. Steps 1 and 2
can leave approved unindexed data. Step 3 adds a record only after its support
has committed. Thus every committed prefix preserves the invariant. There is
no separate all-or-nothing batch obligation to reconcile across databases.

After process interruption, SQLite rolls back incomplete individual transactions
when the stores reopen. Under the existing atomic/durable commit and protected
filesystem premises, the remaining prefix still satisfies the invariant. The
next finite service can use the current committed snapshot. An interrupted
append's overall completion remains unknown; successful later service cannot
turn it into a successful batch report. A deliberate repeated append is a new
funded operation and pays for its supplied bytes again, even if duplicates.

Arbitrary power-loss durability, hostile local database changes and unsupported
concurrent writers do not follow from this argument. Existing resource/physical
storage obligations remain. Uncertain live process cleanup must be settled by
the existing process supervisor before another invocation, not by removing locks.

## Why this is smaller than generation recovery

Exact content seals are useful for an immutable generation, but were an imposed
constraint when applied to an incremental advisory host. Keeping them would
require pending intent, bounded recovery and new seal publication merely to
recover the same safe prefix. V2 instead makes that prefix an expressly supported
state. No intent database, replay operation, counter reconstruction, full-history
walk, rollback or cross-database atomicity mechanism is required.

V1 static hosting remains a distinct preserved contract. V2 needs a fresh host;
old PROFILE-bound roots are never silently reinterpreted. Keeping the current
prepare/serve interface for newly prepared static V1 generations and adding
explicit init/append for V2 allows a small additive public surface.

## Cost and honest scope

Per append, charge every supplied byte, including duplicates, selected preview
work, index paths, SQLite I/O and fixed open/close/support costs. There is no
mandatory previous-corpus scan/copy or lifetime 64-target list. Keep at most
64 targets per append; cumulative capacity is governed by existing store limits.
Finite nodes still eventually fill and need operator retention/sharding choices.

This does not prove that producer export already supplies minimal deltas. The
ordinary producer can export a selected non-seed closure, with environment-loading
cost and repeated dependency bytes. A supported bounded manifest projection over
already obtained evidence, or existing producer selection, is a separate
decision if end-to-end use requires it. Do not claim O(new bytes) for the whole
pipeline when a producer actually resends the prior closure.

The useful benefit is a maintained independent custodian that does not need a
mathematical owner, full generation copies or one service endpoint per small
batch. Existing owner publication remains preferable when the contributor
already maintains a checked owner; static shards remain appropriate for stable
collections. This capability supports growth infrastructure, not a theorem
count or a claimed causal acceleration of mathematical discovery.
