# Interrupted work: recovery contract and qualification boundary

## Current development contract

The development cut supports two explicit owner modes through
`manage.py recover`: `recover_peer` for `peer_find`, `peer_acquire`, and
`expose`, and newly integrated `replica_expose`; `recover_ordinary` for `info`, `find`, `preview`, `select_context`,
`admit`, `submit`, and `publish`. The [API](API.md) gives the exact envelopes.
These are local state-reconciliation commands, not mathematical checking or
automatic retries. All charges and partial files remain retained.

Keep three claims separate:

| Evidence | Established scope |
| --- | --- |
| [Preserved peer outcome](qualification/recovery-01/OUTCOME.md) | One actual interrupted transfer and exact refusal/success replay on its retained v2 cut |
| [Ordinary state-contract outcome](qualification/ordinary-abort-contract-01/OUTCOME.md) | Eleven independently audited passing tests using real SQLite/locks, synthetic state/quiescence and mocked supply |
| [Genuine ordinary native interruption](qualification/ordinary-abort-native-02/OUTCOME.md) | Fresh02 has an independently audited bounded PASS: actual live Lean interruption, original-tree quiescence, exact abort/replays and fresh checked continuation. Failed01 stays failed and charged. |

Replica recovery's explicit allowlist addition is source-reviewed but not yet
runtime-qualified. The preserved ordinary and peer outcomes do not automatically
qualify the current combined development cut.

For either mode, authenticate the exact original request, original installed
source/configuration cut and selected supervisor evidence before opening state.
Under the existing owner lock, terminal requests return their exact original
response bytes, including historical success. Replay is not new acceptance or
proof that the old files remain available. Peer mode retains its no-stage
restriction even for terminal replay; ordinary mode permits charged stages.

Pending mutation additionally requires the reservation-bound original execution
attempt, authenticated whole-original-worker-tree quiescence, intact initialized
state and the matching active slot. A retry's clean receipt cannot stand in for
the original execution. In ordinary mode, a pending request may have native
stage rows; recovery does not examine their outputs for possible success. It
commits only `INTERRUPTED_ORDINARY_OPERATION` and clears that active slot.

The safety argument is conditional on the selected code/runtime and store
invariants: mathematical visibility and the terminal response commit in the
same transaction; hence intact pending state excludes committed visibility for
that request. Original-tree quiescence and writer exclusion prevent the old
worker from subsequently promoting its files. Native work may have happened,
but is neither refunded nor converted into acceptance by recovery. Peer mode
keeps the stronger no-stage premise and its original refusal code.

On uncertain terminal persistence, do not attempt a compensating clear or
assume rollback. Preserve the same selection and re-read/replay the ledger.
Persistent terminal-storage failure can leave pending work blocked; renewal
does not clear it. Bootstrap interruption, missing original evidence, changed
source/configuration, host reboot, damaged state and nonempty SQLite sidecars
remain outside this supported profile. Never delete a journal or reset charges
to force recovery. Hot-journal and restore handling remain v1 operability gaps,
not hidden guarantees of these eleven tests.

## Preserved original peer design

Prospective contract, with source-reviewed drafts now integrated into the mutable
development tree but no recovery runtime qualification. See
[source-cut evolution](SOURCE-EVOLUTION.md). This addresses a necessary v1
operability gap: one interrupted transfer must not permanently disable an
otherwise healthy local node. It must also not convert an uncertain operation
into an invented mathematical result. General native-stage recovery is a
separate, harder case.

## Existing state and safe information

The current writer reserves request count/bytes and sets one active request in
a committed transaction before peer work. The visibility transaction commits
candidate/view records and the exact terminal response together. Process loss
before that transaction may leave retained files and a pending request, but no
new visible candidate. Process loss after commit may hide the response from the
caller while its exact terminal bytes remain recoverable.

A failed outer call is therefore not evidence of rollback. Neither a vanished
lock nor a missing PID proves that its process tree stopped. The supervisor's
locally retained, request-bound final observation supplies that evidence when
it actually records a reaped direct child and zero active Job processes. This
is trusted owner-local evidence, not a portable peer certificate.

## Minimal supported transition

An explicit owner command is restricted to `peer_find`, `peer_acquire` or
`expose`. Separate common identity checks from the mutating pending branch:

1. The selected state/configuration and exact original request bytes match the
   request ledger. The request's client and operation are supported.
2. Locally authenticated supervisor evidence binds that request, the current
   installed source/configuration cut and its exact command/state directory.
   Under the writer lock, the ledger must match the selected request and contain
   no native stage assigned to it.
3. If it is already terminal, return its original terminal bytes, with no new
   charge or terminal rewrite. Do not require a refusal, original-attempt
   marker, cleanup evidence or ownership of an unrelated active slot for this
   nonmutating replay. Common identity/source checks and writer exclusion remain.
4. For a pending transition, require completed cleanup:
   direct child reaped, final Job active count zero, and no unresolved cleanup
   or evidence-persistence error. It is not supplied over the peer protocol.
   The reservation transaction must also contain the deterministic owner-scoped
   `attempt` record `{request:key,call_directory:original_supervisor_directory}`.
   Its handle is computed through the ordinary config-bound record encoding.
   Equal request bytes alone do not identify an execution attempt: a later
   retry's receipt must not stand in for the original worker's cleanup. Retries
   return/block before reservation, so they cannot create this origin marker.
   Requests made without supervised event/origin binding cannot use this recovery.
5. Under the normal writer lock, the pending request is the exact active request and
   no native stage record belongs to it. A changed state is re-read, not assumed
   from earlier diagnostics.
6. If genuinely pending and all guards hold, atomically terminalize it as
   `INTERRUPTED_PEER_OPERATION` and clear only its active slot. Preserve every
   charge and retained file. A new request ID can attempt new work afterward.

The safety argument is conditional: zero live workers plus writer exclusion
prevents the old operation from later promoting its orphan files; absence of a
native stage prevents this narrow recovery from clearing uncertain native
execution. The ordinary transaction preserves the candidate/head distinction.
No successful candidate is reconstructed from a directory or an incomplete
receipt. No deletion or quota refund is needed for this minimal recovery.

If any premise cannot be established, remain explicitly blocked and provide
bounded diagnostics. Do not sweep unrelated work or reset the database. This
preserves safety at the cost of availability in the unresolved case.

The current store refuses nonempty SQLite journal/WAL/SHM files. This profile
therefore requires an openable ledger after interruption; it cannot promise
recovery from a kill during a database transaction. Never delete a hot journal
to force this precondition. The preserved peer-cut runner does not inspect the
Win32 `CloseHandle` return value: its `job_closed` records a returned close attempt,
not confirmed handle release. The new development runner checks that return;
its stronger interpretation requires separate qualification. Final zero-active
and direct-child reap remain separate required observations. See
[draft review](drafts/RECOVERY-REVIEW.md); a fresh recovery installation still
needs its own supervision and execution qualification.

## Required falsifiable test

Interrupt a genuinely supervised acquisition before its terminal transaction,
using a controlled slow loopback sender. Confirm the actual worker tree is
quiescent and the ledger remains pending, with no new P1 entry or changed head.
Apply the documented owner recovery; require exact terminal refusal, preserved
charges/files and cleared active slot. A fresh ordinary acquisition must then
succeed. Controls: wrong request/config, nonquiescent/incomplete evidence,
another client's request, native operation and already-terminal request.

An artificially inserted database row or fabricated successful supervisor
record is not qualification of the interruption path. Sudden-power-loss,
filesystem repair and native-stage recovery are not conclusions from it.
