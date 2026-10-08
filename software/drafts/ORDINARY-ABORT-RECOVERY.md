# Conservative recovery of interrupted ordinary work

Prospective design checkpoint, 2026-09-21. Not implemented or qualified.
This narrows the continuing-operation problem after capacity renewal. It is
based on the current `node.Dispatcher.execute`, control-store transactions,
public process-tree supervisor and authenticated peer-recovery path. It does
not change any frozen source cut or authorize another execution allocation.

## Prefer aborting unpublished work over reconstructing acceptance

An interrupted submission need not be reconstructed into a successful result
to make the node usable again. If its original process tree is demonstrably
quiescent and its database state is intact, a still-pending request can instead
receive a durable interrupted refusal. All files and consumed work remain.
The agent may deliberately submit again under a new ID and fresh allowance.

The decisive separation is between:

- completion of native computation, which may leave output files;
- atomic mathematical visibility in the control database;
- delivery of the terminal response to the caller.

Native files alone never authorize the second step. Lost response delivery
does not prove the second step failed. The request row decides which case is
recoverable under the conditions below; the recovery path never interprets a
Lean output as fresh mathematical acceptance.

## Conditional state argument

Let a selected request have exact key k, bytes r and original execution attempt
a. Let U be the consumed vector and A its authorization. The implemented normal
path commits the following transitions separately:

1. Reservation installs `pending(k,r)`, the attempt binding, active=k and its
   request charge.
2. Any stage reservations append their charged bookkeeping before native work.
3. One visibility transaction installs the operation's visible records/head
   changes together with its terminal response and active=NULL.

Assume writer exclusion, atomic SQLite transactions, intact bound rows, a
selected openable supported database profile, and a trustworthy original
supervisor receipt that establishes quiescence of the entire original tree.
Then the two recoverable cases are:

```text
terminal(k,r,response)  -> replay exactly response; change nothing
pending(k,r), active=k -> commit only an interrupted refusal and active=NULL
```

In the pending case, transition 3 has not committed: its terminal write is in
the same transaction as all mathematical visibility writes. Therefore the
abort does not remove a committed mathematical result. Charges and files from
transitions 1 and 2 remain; the aborted work is not free. A successful normal
visibility commit whose response was lost is the terminal case, not the abort
case. If recovery's own commit is ambiguous, keep its outcome unknown and use
the same exact recovery selection to inspect/replay later.

This is a conditional argument about the actual write partition, not a proof
that the operating system, SQLite, filesystem, source adapter or Lean kernel
cannot fail. Any future out-of-transaction visibility write invalidates this
argument and must be reviewed before extending the supported operation set.

## Minimal prospective implementation

Retain the present `recover_peer` behavior and its documented narrow envelope.
Add an explicit owner-selected ordinary-abort mode, with an exact operation
allowlist initially covering initialized-node `info`, `find`, `preview`,
`select_context`, `admit`, `submit`, and `publish`. Peers may use their existing
mode. Do not automatically expose arbitrary future operations to recovery.

Reuse the original request/config/source/command authentication and indexed
attempt binding. Terminal historical replay remains before mutation-only
active/quiescence requirements. Pending mutation requires all of:

- exact client, request ID, raw bytes, request key and original attempt;
- the original public worker's whole-tree supervisor, not a later retry's
  receipt, a native substage receipt, elapsed time, or PID absence;
- successful direct-child reap, final active zero, checked Job closure and
  no ambiguous cleanup/evidence state under the existing receipt contract;
- initialized state, active=k, an exact pending row and writer exclusion;
- supported, readable database state without a nonempty journal/WAL/SHM under
  the existing profile; no deletion or guessed repair of a sidecar.

The current peer mode's blanket `require_no_stage` is not a necessary premise
for this new abort argument. Native stages may have been allocated, run or
finished. They remain charged and retained, and their outputs are not promoted.
The original public Job's genuine descendant containment must cover those
native processes. Removing the stage check without establishing this larger
quiescence boundary would be unsound.

Recheck pending/active/attempt bindings inside the terminal-only transaction.
Its only permitted writes are the fixed refusal response/phase and active-slot
clear. Preserve U, A, grant rows, stages, heads, contexts, artifacts, publications,
candidate entries and every existing historical response. Do not invent a
successful source result, reverse a head, delete work, refund a grant or trigger
a new submission. Keep the independently bounded owner-command profile.

## Exclusions that must remain visible

This first extension would not recover interrupted bootstrap, a host reboot
without an authentic original quiescence receipt, missing receipts, unknown
descendants, a hot SQLite journal, damaged state or a changed installed cut.
Those are real remaining availability limitations, not reasons to declare an
unsafe abort. In particular, interrupted bootstrap can still require an
explicit fresh-node procedure; renewal currently requires initialized state.

Nor does abort undo arbitrary side effects of owner-authorized Lean source.
The source lane is cooperative local executable input, not a sandbox for
hostile programs. The state argument concerns the node's defined bookkeeping
and mathematical visibility; it makes no rollback promise for arbitrary code.

## Small decisive qualification, after the renewable cut

Use a fresh genuinely initialized node and interrupt one actual ordinary
submission only after its stage reservation and while its original supervised
tree is alive. Preserve the actual original whole-tree termination receipt.
Then require a public abort to commit an interrupted refusal with no artifact
promotion, identical old state/charges, retained native files, and an available
active slot. Under a separate deliberate new request ID and sufficient credits,
complete ordinary checked work. Include exact aborted-request and recovery
replays; no native reexecution follows historical replay.

Use bounded controls for a later same-bytes retry receipt, wrong client/attempt,
incomplete native-tree cleanup, already-terminal success, pending mismatch,
and uncertain terminal persistence. A host or database crash needs a different
experiment; injecting an exception is not equivalent evidence.

This is the next small recovery hypothesis, not another required framework or
a claim that all recovery must be formally proved before a useful v1 exists.
