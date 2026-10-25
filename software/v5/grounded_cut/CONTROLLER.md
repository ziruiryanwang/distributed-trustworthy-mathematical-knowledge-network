# Grounded local cuts: complete source path

Status: source candidate under independent review, not a built or adopted backend.
No new mathematical acceptance or measured speedup has occurred. Ordinary Lean
projects remain the concept/theory-authoring route; this optional lane checks one
new theorem over an already grounded vocabulary. It does not create cold trust,
authenticate peer theorem signatures, or replace the ordinary catalog.

## The four operations

An approved owner process first loads the existing ordinary package, then the
exact `cut_bootstrap.load` graph. `loaded.support` is the runtime passed to these
controller functions; `loaded.controller` supplies the functions themselves.

| Operation | Authority it may use | Result |
|---|---|---|
| `bootstrap` | A genuinely locked native-bootstrap catalog, its validated selected context, and exact retained V2 proof claims | A distinct local cut root whose summaries were derived from accepted exact units |
| `extend` | Earlier members of one committed cut root, live inherited support, and this call's actual clean kernel-check event | Exactly one new theorem and its new committed cut root |
| `resolve` | A durable exact proposed record plus the protected catalog's indexed root membership | COMMITTED or NOT_COMMITTED for that exact proposal; no mathematical re-execution |
| ordinary publication/receiving | Complete inert V2 claims in ordinary custody | Independently checked use by another consumer, never transfer of this local warrant |

All controller operations take an explicit one-shot `OperationBudget` and finite
map/storage `Allowance`. The budget starts before support/preparation work; the
controller claims it once. Caller-chosen caps cannot grow on failure or trigger
automatic retry. An external supervisor is still needed for hard controller
CPU/memory containment; Python budget checks alone are cooperative. Windows Job
resource supervision is not a hostile-code security sandbox.

`bootstrap` additionally takes an already-open native catalog, selected root,
ordinary custody store, fresh cut directory, fresh call directory, fresh selected
store/epoch identities and finite migration limits. `extend` takes the existing
cut directory, expected store/epoch, selected parent, one full new V2 claim,
ordinary custody and a fresh call directory. `resolve` takes the known earlier
call directory and the same expected store/epoch. Limits on reopen must match the
original marker. No network object can nominate a new authority or state location.

## Initial grounding is real paid work

The bootstrap holds the original native owner lock. Its selected context is
validated using the existing native catalog, including retained snapshot identity
and exact bindings. The source must have native-bootstrap origin and the same
implementation as the selected ordinary installation; legacy translation and
cross-support migration are outside this first lane.

For every nonbasis name, bootstrap obtains an exact custody locator and its full
V2 unit. The unit's semantic identity, full content ID, requested export, complete
generated inventory and every original import must agree with the accepted native
context. It derives the summary from those bytes, never from a caller's separate
statement. It stores a summary once per complete unit and a path-local map entry
`[exactExportID, exactSummaryDigest]` for each output name. Fixed basis names are
derived from the authenticated fixed seed and inventory, not a supplied dictionary.
All nonbasis names must be covered exactly, with no overlap or omitted group.

This association is particularly important for theorem summaries: once a proof
is erased, its original unit ID cannot be recomputed from the statement. A hash
of the short summary does not prove the connection. The protected derivation
event establishes it using the original accepted full unit.

Bootstrap is atomic. Until its root and counters commit, the destination remains
BOOTSTRAPPING and cannot be reopened as active. It performs no new proof checking;
its full-history validation, custody reads, projection, index writes and storage
are migration costs, not free setup or a substitute for initial checking.

## One extension and its inductive invariant

For each committed root, maintain this invariant:

> Each map entry names an exact summary derived either from the eligible initial
> native context or from an earlier successful cut event. A concrete entry retains
> exact checked declarations/computation rules; a theorem entry denotes a proposition
> derivable in the selected foundation with those concrete semantics.

An extension holds both the original source-support lock and the cut-catalog
lock. Source reopening checks fixed adoption/activation/withdrawal metadata by
primary key; it does not reopen the native catalog, restore its snapshots, scan
its operation records or enumerate its history.

1. Select an actually committed root, not a caller-supplied map root. Resolve
   only demanded exact names and full group memberships through its persistent
   trie. Check new-name absence against the whole selected root, not just the
   reconstructed scratch subset.
2. Recursively include all concrete semantics and only the types of selected
   old theorems. The first implementation refuses concrete-to-nonbasis-theorem
   dependencies and cycles. It checks concrete groups together before signatures.
3. Bind the exact packet and a fresh request identity. Preflight includes the
   fixed seed/inventory and JSON framing, plus reserved call-spool/report/log
   space. Retain and read back the full new V2 claim in ordinary inert custody.
4. Run the fixed approved worker under the original resource allowance. The
   kernel primitive checks signature types as propositions, exact complete
   concrete inventories and one genuine new theorem. No peer command, source,
   snapshot or arbitrary prebuilt environment is accepted. A report alone grants
   nothing: this invocation must actually complete with a cleanly closed child
   tree and exact matching request/output inventories.
5. Recheck live support, unchanged parent/frontier and whole-root freshness.
   Derive the new summary from the same complete new input, path-copy insert
   its single output, retain a schema-distinct event/frontier, persist the exact
   commit intent, then atomically commit the new root and storage counters.

The interpretation argument substitutes already warranted theorem proofs for
scratch assumptions while retaining exact concrete computation rules. It is a
one-way soundness argument, not equivalence with every native checking success:
proof-dependent reductions unavailable in the scratch environment may refuse.
The new committed theorem can supply an interface to the next event after a
normal close/reopen, without retaining or trusting a scratch axiom environment.

Initial grounding establishes the invariant. Exact earlier membership plus
positive kernel checking and the interpretation argument preserve it. Atomic
commit prevents an unchecked or partial prefix from being reused. This argument
still relies on the reviewed checker/codec/Lean correspondence, approved runtime,
cryptographic identity assumptions and protected local storage; source review
does not discharge all those assumptions or constitute a formal kernel proof.

## Failure, lost replies and support withdrawal

Every proposed root is durably recorded in the known call directory as
`COMMIT-INTENT.json` before COMMIT. The file includes the exact root record and
derived candidate identity. If a process dies after COMMIT but before return,
`resolve` queries that exact root by primary key and checks exact record bytes.
It neither scans ancestors nor repeats the worker or commit.

An absent exact row in an otherwise eligible, cleanly opened active catalog gives
NOT_COMMITTED. A hot journal, incomplete bootstrap, missing intent, changed
identity or withdrawn source refuses resolution; it is not silently translated
to NOT_COMMITTED. Live COMMIT exceptions also carry the catalog's explicit
COMMITTED/NOT_COMMITTED/UNKNOWN disposition. No disposition schedules a retry.
This is bounded lost-reply resolution, not general damaged-disk recovery. File
flush/SQLite durability still depend on the stated filesystem/hardware premises.

Uncertain worker cleanup creates a sticky local WITHDRAWN marker and cannot
promote a theorem. Any original source withdrawal/quarantine conservatively
disables inherited cuts. A renamed epoch or copied signature cannot rehabilitate
them. Source relocation and general support migration remain unsupported.

Missing ordinary proof custody prevents publication/reacquisition but does not
by itself erase an already sound local theorem. Conversely, a surviving proof
claim does not restore withdrawn local checking support.

## Cost and concept development

Per-extension work includes fixed support validation/basis reconstruction, the
actual new proof, selected concrete semantics, old theorem types, finite indexed
reads/writes, custody, commit and failures. It has no mandatory full ancestor-proof
or whole-root enumeration step. SQLite physical B-tree work, database capacity,
map-node retention and call-spool capacity remain real costs; logical point-read
counts are not constant-time physical I/O guarantees.

There is no measured speedup yet. Compare against the existing native path,
which restores snapshots but does not re-kernel-check every old theorem. Credit
batching, small eligible native roots, caches and simpler metadata optimizations.
Frequent changes of definitions or proof-bearing structures may require ordinary
native re-entry; that additional cost belongs in the comparison. Cuts must not
turn open-ended theory development into a theorem-only terminal branch.

Before runtime selection: complete independent source review, focused bounded
controls, selected support compilation and a specific recursive-use evidence
plan are separate gates. Passing any one is not completion of v5 or evidence of
automatic creative growth.
