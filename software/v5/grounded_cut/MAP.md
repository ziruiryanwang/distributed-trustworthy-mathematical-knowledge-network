# Grounded-cut exact-name map

Source-only implementation selected on 2026-10-24. No execution, migration,
protected-state opening or mathematical acceptance is established by this file.

## Purpose and reuse decision

`cut_map.py` is a small persistent storage primitive for the protected controller.
It makes a lookup, whole-root name-absence check or insertion independent of an
event-history traversal. It is not a mathematical checker, receipt verifier,
portable proof, root-eligibility decision or complete authenticated database.

The existing `discovery/authenticated_index.py` compressed map was inspected
before writing this specialization. Its leaves retain only hashed features and
feature roots; its commitment preserves an expanded 256-level sparse-map proof
format, maximal run encodings and discovery namespaces. Reusing that implementation
would still require a separate exact-key payload layer and storage adapter while
introducing unrelated schema/proof machinery. This specialization reuses the same
path-copying principle, but no discovery authority or frozen source is modified.

## API and ownership

```python
limits = Limits(max_key_bytes=16384, max_value_bytes=4096)
budget = Allowance(max_reads=600, max_writes=300,
                   max_read_bytes=16 * 1024 * 1024,
                   max_write_bytes=16 * 1024 * 1024)

# The protected controller explicitly begins/owns the transaction.
create_schema(conn, budget)             # once for a newly created database
root = EMPTY_ROOT
root = insert(conn, root, name_bytes, summary_reference_bytes, budget,
              limits=limits)
value_or_none = lookup(conn, root, name_bytes, budget, limits=limits)
# The controller atomically records the eligible event/root and commits.
```

The example budget is illustrative, not a prescribed controller allocation.
Every public operation requires `conn.in_transaction`; none calls BEGIN, COMMIT,
ROLLBACK, VACUUM, checkpoint, close, a connection context manager or migration.
The controller owns locking, schema creation, connection configuration, finite
SQL waiting, process supervision and failure cleanup. `create_schema` deliberately
refuses an existing table rather than silently adopting an unexamined schema.
The only table is `grounded_cut_nodes`, with a binary-collated text primary key,
blob payload and `WITHOUT ROWID`. All node reads use equality on that primary key.

The controller supplies **already validated canonical encoded-name bytes**, such
as the exact result of `ordinary_evidence.name_key` under its selected policy.
The map preserves these bytes exactly and applies SHA-256 to them; it does not
parse Lean names, accept dotted-name approximations or establish semantic-name
policy. Opaque nonempty values normally contain small exact summary references.
Large type/group objects belong in separately bounded controller-owned storage,
not one copied body per generated name. Defaults are 16 KiB keys and 4 KiB values;
each can be explicitly configured from one byte through 1 MiB. A changed bound
must be part of the controller's selected operation, never discovered from input.

## Exact representation

All integers are unsigned big-endian. Concatenation is unambiguous:

| Node | Canonical payload |
|---|---|
| Leaf | byte `01`, four-byte key length, exact key bytes, four-byte value length, exact value bytes |
| Branch | byte `02`, two-byte split depth, 32-byte masked prefix, 32-byte left node hash, 32-byte right node hash |

A node ID is lowercase hexadecimal
`SHA256(b"DMKN-GROUNDED-CUT-MAP-V1\0" + payload)`.
`EMPTY_ROOT` hashes the same domain followed by byte `00`; no empty node is stored.
Leaves retain the **entire original key**, not just its routing digest.
Branches have depth 0 through 255 and a common prefix consisting of exactly the
top `depth` routing bits (all remaining bits are zero). Both children are distinct
nonempty IDs. A branch's selected child must have a strictly deeper split, or be
a leaf, and match the parent's common prefix plus selected left/right bit.
There are no unary branches, compressed-run node chains or alternate encodings.

Every visited node is bounded before materializing its payload, hash-checked,
decoded with exact lengths/tags, and checked against its incoming edge. Child
hashes have fixed 32-byte encodings; a visited child must match its committed ID.
Unvisited subtrees are not recursively scanned. Consequently a supplied arbitrary
hash is not a validated or eligible root. Integrity of a whole reachable tree
follows inductively from an eligible empty root and successful controller-owned
insertions, under SHA-256 collision resistance and the protected-storage model.

## Algorithms and invariants

Lookup descends only while the requested routing prefix agrees. A mismatching
compressed prefix or leaf hash proves absence **inside that supplied well-formed
root**, not global absence. A matching leaf hash with a different full key refuses
`CUT_MAP_KEY_HASH_COLLISION`; a routing collision never overwrites a name.

Insertion follows the same path. At the first differing bit it adds one leaf and
one branch above the old subtree, then copies only the visited ancestors. It does
not enumerate events, roots, names, other subtrees or all database rows. Identical
key/value insertion returns the same root without node writes; different values
for the same key refuse `CUT_MAP_KEY_ALREADY_BOUND`. Existing hash-addressed rows
are compared byte-for-byte before reuse. A node-hash collision or collision with
the reserved empty root refuses. There is no update/delete API.

Inductively, for any eligible root `R`, successful insertion of previously absent
`k -> v` yields `R'` with that new binding and all prior bindings unchanged. `R`
and its nodes remain readable. In a reachable tree with `n > 0` distinct routing
keys, there are exactly `n` leaves and `n - 1` binary branches. Retained historical
roots share unchanged subtrees; total historical storage still grows with the
number and depth of insertions and needs explicit retention accounting.

## Bounds and costs

Depth strictly increases, so lookup visits at most 256 branches plus one leaf.
Insertion has the same traversal bound and stores at most 258 nodes (a deliberately
conservative bound). Each store first makes one exact existing-node read. Therefore
one insertion makes at most 515 logical node reads and 258 attempted node writes;
duplicate rows may reduce writes. These are absolute 256-bit bounds, not a claim
that arbitrary semantic search is logarithmic or that all SQLite work is constant.
Under suitably dispersed hash keys typical path depth is logarithmic; no such
distribution assumption is needed for the finite refusal bounds.

`Allowance` has finite read, write, payload-read-byte and payload-write-byte caps.
Every issued node SELECT is charged, including misses; every INSERT attempt is
charged before execution. Schema creation charges one write and zero payload
bytes. Existing rows charge their returned payload bytes. Reads use SQL type/length
checks and a CASE expression so an oversized blob is not returned to Python.
The row header can distinguish node-size refusal from exhausted byte allowance.
Hashes and decode work are bounded by the finite node/read limits. Counters are
operation objects: they are not reset after a failed recursive insert. Conservative
charging can count reserved payload bytes when the write-count cap then refuses;
it never undercounts issued statements. They do not measure SQLite page I/O,
cache effects, lock wait, CPU, fsync or transaction/retention cost.

The enclosing controller must retain its existing time/process/resource bounds.
A storage error or allowance refusal can leave an uncommitted node prefix in the
caller's transaction; the controller must roll back the whole failed event (or
its own pre-established event savepoint), never adopt a partially built root.
Only a clean controller event committed atomically with its new root makes that
root eligible. A later fresh transaction may reuse a committed root by indexed
access without reading its ancestor events. That authority invariant, support
epoch and exact summary grounding are obligations of the controller, not this map.

## Focused review obligations before any execution

The independent review should cover old-root persistence; close/reopen lookup;
prefix mismatch absence; exact duplicate/refused replacement; insertion before,
at and below existing splits; malformed/hash-mismatched/missing nodes; invalid
child prefixes or depth; key/value/node caps; missing transaction; logical I/O
allowance exhaustion; and caller rollback after partial insertion. Collision
handling can be source-reviewed or tested using a narrowly controlled digest
substitution, without claiming an actual SHA-256 collision. End-to-end acceptance
requires the separate complete controller/worker authority review. No map-only
test establishes a grounded theorem, a safe migration or full-cost speedup.
