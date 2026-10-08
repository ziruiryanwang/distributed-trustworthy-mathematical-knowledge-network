# Ordinary interrupted-work abort: source review

Date: 2026-09-21. Author: `bounded_domains_author`. This is a source-only
review of [the proposal](ORDINARY-ABORT-RECOVERY.md), not an execution result,
crash test, or launch approval. Subsequent root-authorized source-draft work is
recorded in the final section. No product import, SQLite query, native execution,
or product edit was performed.

## Verdict and minimal scope

The proposed extension is viable as a **conditional, owner-local abort of one
still-pending initialized-node request**. The decisive existing property is
that the request's mathematical visibility changes and its terminal response
are committed in one SQLite transaction. Recovery need not reconstruct proof
success, and must not inspect unfinished proof outputs to manufacture success.

The minimal useful extension is a separate ordinary-abort owner mode over the
existing recovery supervisor, retaining the current peer mode. It changes only
one request from pending to a fixed interrupted refusal and clears its active
slot, after authenticating the actual original attempt and its whole public
process tree's quiescence. Already-terminal requests yield exact historical
responses without mutation. All consumed allowance, stages, packages, source,
logs and previous mathematical records remain.

This does **not** establish unconditional node availability. In particular,
terminal-space or physical-storage failure can still strand a pending request,
and the current renewal path refuses to grant new capacity while that request
is active. Do not resolve that separate problem by silently permitting renewal,
deleting evidence, dropping a sidecar, or clearing the active slot.

## Reviewed cut and evidence boundary

The source references below are to the observed development cut, not to a
frozen qualified installation. Relevant functions were inspected directly;
these file hashes identify their containing files and do not assert that every
function in every listed file received a new exhaustive review.

| File | SHA-256 |
|---|---|
| `drafts/ORDINARY-ABORT-RECOVERY.md` | `B3B3A6FC87A888AF8D02328A7921341CDCA748038642CF3F47B4250424A2D385` |
| `py/recovery_worker.py` | `D5BF6E09D7E3163E8025BE59C818C6099AE537E3A3A952576B6FBF2DD7BC8C52` |
| `py/recovery_manage.py` | `99B0CD3438607FD1BEFFBB5BBF2B07EB1F82D3868C579EFD97875437841FB7B6` |
| `py/node.py` | `DC0B2E20C27290270B595122C33385D51FF629B67EF52B94B97DD8A3990F6977` |
| `py/storage.py` | `E33E61DF78984C60E60999D53DB515487E41157F29475E0CBCAF12321968637D` |
| `py/supervise.py` | `E5F35C0A88602757ECB7FF899F923F940B588E11E2A7C9C36D51FDBB2DFCAC1B` |
| `py/run_stage.py` | `2B2A33DE45490D124F0828F0E1DE15E5C57C91FACD326FD4AE054027C7952F4D` |
| `py/checking.py` | `13AFA1FA31F58F273C0364B9679FD56400587F2977EA24BDDD85AAD9471F840B` |
| `py/peer_node.py` | `99B7F3AF3C4C4E0B66827157E743A75EAC320A54D04E90C1E4A9912991A90B18` |
| `manage.py` | `DF319F00DBCF29702A04D6151564896AE4D040998AC5859CACE7CBE53580BB77` |

Paths in that table are relative to `software/`. Important inspected seams are
`Dispatcher.prepare/commit_operation/execute`, `ControlStore.reserve/stage/terminal`,
`ControlStore._transaction/terminal_refusal/_grant_proposal`,
`recovery_worker.authenticate_evidence/recover/require_quiescence`,
`recovery_manage.invoke_recovery`, `Transport.__call__/quiesce`, `Job`,
`Checker.stage/submit/publication`, and `PeerOperations.publication_offer`.

## Actual write partition

Write exclusion is the existing owner-local Windows byte-range lock. It is not
a proof that descendants are dead. An interrupted Python parent can release
that lock while a child continues running; both exclusion and quiescence are
necessary before aborting pending work.

| Boundary | Current writes or effects | Recovery consequence |
|---|---|---|
| Request reservation | One ordinary transaction inserts exact pending row, attempt record when supervised, request charge and active key | An intact pending row can have a charged request and a durable original-attempt binding without any mathematical visibility |
| Preparation | Reads selected state; creates request-local files; a checker callback commits a charged stage reservation before invoking its runner | Aborted work may leave stages and partial or complete native files; absence of such files is not a prerequisite |
| Visibility | `commit_operation` and `terminal` run inside the same `store.transaction()` | An intact pending row excludes a committed visibility transition for that request |
| Quiescent ordinary failure | `terminal_refusal` uses a separate terminal-tier transaction after confirmed rollback | Refusal can be durable without any successful visibility transition |
| Ambiguous transaction or native lifetime | Dispatcher returns blocked; uncertain store cannot write again in that connection | A blocked response is neither permission to resubmit automatically nor evidence that the visibility transaction rolled back |

For the proposed allowlist the visibility writes are bounded and identifiable:

- `info` and `preview` install no new mathematical records; their terminal
  response still belongs to the visibility transaction.
- `find` can create candidate/cursor records, but only in `commit_operation`.
- `select_context` changes a head only in `commit_operation`.
- `admit` installs a context and changes its head only there.
- `submit` installs an artifact record only there. Its source, native outputs
  and imported package files may already exist outside the transaction.
- `publish` installs the provider entry/snapshot, publication marker and
  candidate only there. Preparation can validate/reuse and fsync existing
  package bytes; these effects do not themselves publish a new ledger entry.

`publish` does not currently allocate a new native stage: its checker revalidates
existing submission evidence. This does not reduce the need to bind the actual
request or change the proposed allowlist. Native-stage presence is chiefly the
new issue for `admit` and `submit`; interruption before stage allocation is also
within the same ordinary-abort contract.

The claim concerns defined ledger visibility, not all observable host effects.
Trusted/cooperative Lean source can execute code, and the present system is not
a hostile-source filesystem or network sandbox. Arbitrary source side effects,
an external server exposing arbitrary directories, privileged tampering and
out-of-band database edits are not rolled back by abort.

## Conditional safety argument

Let `k = SHA256(encode([client, request_id]))`, `r` be the exact request bytes,
and `a` the original supervised call directory recorded at reservation. Let
`R[k]` be the request row, `U` the consumed request/stage/byte vector, `A` the
authorization and grant state, `V` the defined mathematical-visible ledger
projection, and `F` the existing work/evidence files.

Use the following premises explicitly:

- The supported SQLite profile provides atomic transactions for this process
  interruption, and reopening returns an intact supported state. The store's
  present sidecar refusal remains in force; recovery is not journal repair.
- The installed/configured sources remain the authenticated cut. For this
  allowlist, all per-request writes to `V` occur in the same transaction as its
  terminal write. Reservation and stage transactions cannot write `V`.
- Trusted owner storage and source execution do not forge rows, overwrite
  receipts, bypass the protocol, or change files concurrently with inspection.
- Writer exclusion is held through selection, mutation, commit and close.
- For pending mutation, the exact attempt `a` is bound and its original whole
  public Job has authentically reached the required quiescent endpoint.

Then two branches are available:

```text
R[k] = terminal(r, response)
    -> return response byte-for-byte; no request/ledger mutation

R[k] = pending(r), active = k, bound_attempt(k, a), quiescent(a)
    -> atomically set R[k] = terminal(r, interrupted_refusal), active = null
```

For the second branch, suppose a visibility transaction for `k` had committed.
By its write partition, its terminal response would also have committed. Since
requests are not reset from terminal to pending, that contradicts the observed
intact pending row. Therefore abort does not erase a committed visibility result
of `k`. It does not follow that no earlier or independently visible result
exists; such results must remain unchanged.

The permitted logical post-state difference is exactly one request's phase and
response plus `meta.active`. Thus `U' = U`, `A' = A`, and `V' = V`. Existing `F`
is retained; new recovery-command evidence is allowed in its separate scratch
directory. SQLite file-byte identity is not required: a legitimate commit
changes database pages and may allocate a page. Preservation assertions should
compare logical tables and selected existing-file inventories, not demand an
unchanged database-file hash after a successful mutation.

Idempotence follows from branch selection: after a committed abort, the same
request is terminal and every exact replay returns that stored refusal. A lost
abort response therefore does not justify a fresh ID or second native run.
After confirmed abort, a new ID is a deliberate new attempt with new charges,
not a continuation/refund of the old attempt.

## Required design details before implementation

### OA-1: keep modes explicit and operation-scoped

Use an explicit owner operation, provisionally `recover_ordinary`, with
the existing three selection fields: `client`, `request_id`, and
`supervisor_receipt`. The name is a design recommendation, not a supported API.
Its initial allowlist should remain exactly `info`, `find`, `preview`,
`select_context`, `admit`, `submit`, and `publish`. Reject `init`, administrative
operations and future operations unless separately reviewed.

Both wrapper and worker must validate this exact envelope. Keep `recover_peer`
and its no-native-stage policy separate; do not make a global loosening of
`require_no_stage`. The ordinary mode's fixed interrupted response must be a
small refusal, without `accepted` or any positive mathematical-acceptance
field. No caller-supplied replacement response is accepted.

The existing wrapper hard-codes the worker profile
`draft-native-free-peer-v1`. It therefore also needs a reviewed mode-specific
profile check; changing the worker alone is insufficient. Recovery itself still
loads no checker and allocates no native stage. Its zero-stage event fields
describe **the recovery invocation**, not the original interrupted request.
An exact historical success response can legitimately contain `accepted: true`;
the wrapper must forward it unchanged while reporting historical-only authority.

### OA-2: preserve branch-sensitive authentication and guard order

Recommended order for the new mode:

1. Validate owner envelope and fixed allowlist; authenticate receipt location,
   request/command bytes, exact selected identity, source/config/interpreter
   pins, and command profile before opening the store.
2. Require existing state and use `owner_lock(..., create=False)` for the new
   ordinary mode. Recovery must not manufacture a missing lock or fresh store.
3. Open the existing supported database and authenticate the exact indexed row.
   Keep the initialized-state condition.
4. If terminal, validate a bounded bytes response and return it exactly. Do not
   require zero old stages, current active equality, original-attempt equality,
   or original quiescence for this nonmutating branch.
5. If pending, require null response, original whole-Job quiescence and exact
   indexed attempt binding. Require `active == k` and all existing state guards.
6. Recheck the pending/active/config/attempt conditions inside the terminal-tier
   transaction, and perform only the fixed refusal plus active clear.

The current peer worker calls `require_no_stage` before terminal replay and
again in the transaction. The new mode must bypass both checks, not merely the
second one. Retain them in peer mode. A terminal ordinary request can legitimately
have a stage row, whether it succeeded, failed normally, or was already aborted.

Do not confuse selection authentication with mutation authority. A later
same-bytes request retry has a different call directory and cannot authorize
aborting the original pending attempt. For a terminal row, however, its exact
historical response needs no original-attempt/quiescence premise: a later
otherwise-authenticated exact-call receipt can select the same immutable row.
If the API instead chooses to forbid that terminal selector, document it as an
additional restriction; it is not needed for the stated safety argument.

The original public receipt currently binds exactly twelve files: interpreter,
config and ten named sources. Current ordinary `manage.request` emits that set.
Reusing it does not authorize changing or dropping a source pin. The separate
recovery wrapper's supervised set is already at fifteen or sixteen pins after
its grant, depending on entrypoint. Prefer the existing worker/wrapper files
over a new helper module that would silently exceed that budget.

### OA-3: original whole-tree quiescence is the pending-mutation authority

The inspected public supervisor creates its Job before the child, creates the
child suspended, assigns it before resuming, and later waits for the direct
child and observes final Job active count zero. Closing the Job is a checked
backstop, not a substitute for those observations. Its Job flags include
kill-on-close and do not enable either breakaway mode. Native stages are
descendants: the checker invokes the runner, which creates its own nested Job
and assigns suspended Lean/Python children before resuming them.

This is a conditional containment claim for the supported Windows nested-Job
profile and cooperative local execution. It assumes no privileged escape,
external launch broker, untracked service work, kernel failure or tampering.
The original receipt is trusted owner-local evidence bound by hashes to inputs;
it is not a cryptographic proof that a remote machine killed its processes.

Pending mutation must retain the existing exact-boolean quiescence checks:
Job created before process; successful assign/resume return; direct child reaped
with an integer return code; final active zero; checked Job close; empty cleanup
errors; and no evidence-persistence or output-record uncertainty. Deliberate
termination is allowed. Zero terminated processes is a success/resource
criterion, **not** an abort-quiescence criterion.

A stage receipt can be absent, stale or still say RUNNING after the outer Job
terminates the entire tree. A retained `ACTIVE.lock` can likewise be stale. With
authentic original whole-tree quiescence these are retained artifacts, not
reasons to infer ongoing execution. Do not remove them, rewrite them to look
successful, or reuse their directories. Conversely, a completed Lean log or
quiescent inner Job does not establish that the outer dispatcher and all other
descendants are dead. PID absence, elapsed time, owner-lock acquisition and a
later retry's clean receipt are also insufficient substitutes.

### OA-4: keep uncertainty and saturation separate from refusal

Let `B` be the authorized metadata cap in 4096-byte pages. Existing ordinary
writes use `B - 2048`, terminal writes `B - 1024`, and grants `B`; admission
requires `page_count <= B - 4096`. The extra terminal tier is useful reserved
headroom, not proof that every future refusal will commit under every disk or
SQLite condition. It neither reserves physical disk blocks nor guarantees
recovery-evidence persistence.

Ordinary request/stage/byte exhaustion must not charge or block a separately
bounded owner abort by itself. Abort creates no ordinary request, stage, grant
or refund. It can still fail on busy locking, invalid evidence, missing source,
SQL work bounds, unreadable state, metadata inconsistency, nonempty sidecars,
physical I/O, a terminal transaction failure, or its own finite supervisor and
evidence budget.

The current `_transaction` marks a connection uncertain on a COMMIT exception
or unconfirmed rollback, prohibiting subsequent writes. Preserve that rule.
Current recovery deliberately uses a conservative unknown classification when
a terminal write was attempted without a recorded successful commit. It may
classify even a confirmed rollback conservatively; refinement is optional, not
necessary for this extension. Never issue a second clearing write in the same
uncertain connection.

After an ambiguous abort commit or lost event/stdout, the next exact selection
reopens intact state: terminal means historical replay; pending means the
ordinary abort guards must be met again. An inability to deliver the response
does not undo the transaction. If terminal persistence cannot succeed, leave
the request pending. Current `_grant_proposal` rejects active pending work, so
new renewal is then unavailable too. This is an explicitly unsupported
availability corner, not a hidden promise to repair or reset capacity.

## Discriminating verification plan

Tests below are required designs, not run results. Source/state tests can use
bounded synthetic bookkeeping, but must say so. The positive native test must
use a genuinely initialized node and actual submission; fabricated stage rows,
mocked native acceptance or an injected Python exception do not establish the
native interruption claim. All launch counts, fixture bytes, wall/CPU limits,
scratch retention and source pins need a separate reviewed finite allocation.

| Test | Distinguishing condition | Required result |
|---|---|---|
| Exact native pending abort | Genuine stage reservation and actual native child alive before original outer-tree termination | Durable fixed refusal, active cleared, no artifact/head/publication promotion, unchanged charges and retained original files |
| Exact aborted-request replay | Same client/ID/bytes through ordinary request path | Exact stored refusal; no request/stage increment and no native run |
| Exact recovery replay | Repeat identical owner selection | Exact historical refusal; no second mutation or original-stage erasure |
| Already-terminal native success | Real success with a stage row, including a lost-delivery model at state-test grade | Original success bytes replayed, never replaced by interrupted refusal |
| Later same-bytes receipt | Original row pending, selected later retry had a clean exit | Rejected because later call directory is not the recorded original attempt |
| Wrong identity or attempt | Client/ID/raw/key/call-directory mismatch, checked independently | No selected-state mutation and no fresh work |
| Incomplete quiescence | Missing/false exact quiescence field, nonzero final active count, cleanup/evidence uncertainty | Refusal/blocking with no pending clear, even if native output looks complete |
| Stage evidence incomplete | Original whole-tree receipt valid, native receipt absent/stale and stage lock retained | Abort succeeds without interpreting, deleting or repairing native evidence |
| Binding/cut failure | Changed request/command/source/config pin or unsupported operation | Reject before mutation; fresh store/lock not created |
| Pending state mismatch | Missing row, terminal response in malformed pending row, wrong active key, absent original attempt | No clearing of any active request |
| Saturation | Request/stage/byte allowance exhausted but terminal persistence still available | Independent owner abort remains possible; allowances unchanged |
| Terminal persistence refusal | Terminal cap/inconsistent state or controlled physical I/O failure | No successful-abort claim; known unchanged versus uncertainty distinguished conservatively; no fallback renewal/reset |
| Abort COMMIT before/after | Inject a failure before durability and after actual COMMIT in isolated state tests | No same-connection second write; reopening selects actual pending or terminal state, respectively |
| Abort output loss | Commit completed, event/stdout persistence or delivery fails | Exact retry returns stored refusal; failure output does not authorize reexecution |
| Existing peer mode | Peer no-stage positive and peer stage-present negative | Ordinary extension has not silently changed peer policy |

For each mutation/refusal state test, compare all ten control tables by primary
key. A successful abort permits only the selected request row and active field
to change; a rejected prewrite selection permits no logical table changes.
Stages, authorization, owner grants and attempt records are included. Compare
the original work/call file inventories after quiescence and again after abort;
only the separate recovery evidence tree may grow. Do not hash live native
files and treat those unstable hashes as preservation baselines.

### A small positive native scenario that actually tests the seam

Use one reviewed inert submission fixture with a bounded, observable native
pause, and one separately deliberate successor submission. The pause must occur
inside the genuine first Lean source-check child after the database stage
reservation has committed. A bounded fixture marker plus observation of the
actual live child under the original tree can establish the timing; a marker
alone is not liveness evidence. The harness must specify and review this
observation/termination mechanism before launch. Do not edit the product or
SQLite state merely to make the request pending.

Terminate through the **original public supervisor's** reviewed finite timeout
or controlled fault path and preserve its actual `supervisor.json`. If that
path cannot produce its genuine complete quiescence evidence, the case is
inconclusive/blocked, not a passing substitute based on OS process enumeration.
An existing bounded supervisor timeout override may be used by a pinned trusted
qualification harness, but then record that the interrupt trigger is a test
control rather than a new public API capability. Merely killing `manage.py`
can lose the very receipt needed by this design and is not this positive case.

After quiescence, root can inspect under the existing owner lock that the row
is pending, its real stage/attempt exist, no visibility record from it exists,
and no prohibited sidecar remains. If termination lands inside a SQLite write
and leaves a nonempty sidecar, this experiment has hit an excluded crash state;
do not delete the sidecar or count it as the desired test. Bounded native pause
timing reduces that risk without pretending it proves power-loss recovery.

Then invoke ordinary abort publicly, verify the allowed state difference and
preservation, and perform both replay kinds. Only afterward issue the successor
submission under a new ID with explicitly sufficient allowance; require real
checked success. This demonstrates that the active slot can become usable
again, not that the aborted source was accepted or that all interrupted cases
are recoverable. Allocate ample capacity initially for this test so renewal is
not accidentally made part of its positive conclusion.

## Review exit and remaining gates

The proposal passes this source-level feasibility review with OA-1 through
OA-4 made explicit. No schema change, native-success reconstruction, global
recovery framework, source translation feature, attribution system or broader
coordination mechanism is needed for this small availability improvement.

Before implementation: select the mode/response/profile names, preserve the
allowlist and guard order, and approve the finite test plan. After implementation:
independently review the actual changed cut; execute the state controls under
root authority; and only then qualify the actual native interruption seam.
This review does not supply any of those later results.

## Subsequent authorized implementation draft

Root read this review, agreed with OA-1 through OA-4, and commissioned minimal
source-only replacement drafts while independently preparing native-free
contracts. These draft paths are **not launch entrypoints**. Their intended
installation targets, only after root review/integration, are the existing
`py/recovery_worker.py` and `py/recovery_manage.py`; wrapper worker discovery and
all installed path/source-pin conventions remain under those original names.

| Draft | Bytes | SHA-256 |
|---|---:|---|
| [Worker](recovery_worker_ordinary.py) | 19595 | `68D6AC7133B4DF1D58762B81BB13BCC5D3C6512969E308A01D6270589A8529BB` |
| [Wrapper](recovery_manage_ordinary.py) | 9348 | `3F10850777A9F22301CD090AD131987747301A78264882AA9E302DEFA856272C` |

Exact functional delta:

- Add the owner envelope operation `recover_ordinary` with the same exact
  selection fields. The ordinary allowlist is exactly the seven reviewed ops.
- Add `mode="recover_peer"` as a keyword-only argument to `authenticate_evidence`
  and `recover`. Validate recognized mode; preserve all prior positional
  arguments and their meaning. `owner_request` and wrapper
  `selected_owner_request` retain their previous return shapes. Main/wrapper
  derive mode from the already-validated raw envelope, not an invented field in
  selected arguments.
- `authenticate_evidence` enforces the selected mode's original-operation
  allowlist. Peer mismatches keep `RECOVERY_NATIVE_OPERATION_FORBIDDEN`;
  ordinary mismatches use `RECOVERY_ORDINARY_OPERATION_FORBIDDEN`. `recover`
  retains authenticated-evidence and held-owner-lock preconditions rather
  than duplicating the original request parser.
- Keep `INTERRUPTED` and the peer worker profile unchanged. Add the fixed
  refusal `INTERRUPTED_ORDINARY_OPERATION` and mode-bound profile
  `draft-native-free-ordinary-abort-v1`. The wrapper expects the profile
  selected by the exact owner request. All response forwarding stays
  byte-for-byte, including historical success.
- Apply `require_no_stage` at both existing sites only in peer mode. Ordinary
  terminal replay and pending abort retain old stages. Quiescence, original
  attempt binding, indexed selection, transactional rechecks, terminal tier,
  counters, receipt authentication and uncertainty classification are unchanged.
- Require an existing owner lock via `create=False` and an exact bytes terminal
  response. These are explicit shared fail-closed strengthenings: a missing or
  malformed lock is not manufactured, and malformed nonbytes response storage
  is not coerced. They do not change supported intact peer request semantics.
- No SQL statement, schema/table, source-pin set, pin budget, execution limit,
  mathematical checker, stage allocator, product command, or automatic retry
  is added. The recovery supervisor grant's existing request digest binds the
  selected mode because mode is part of the exact request bytes.

The author inspected the full textual differences against the two current
product files. Source drafts were created/edited with `apply_patch`; only
read-only source/diff/hash inspection followed. No import, compilation, SQLite
query, test execution, native execution, or product integration was performed.
Root owns independent contracts, integration, resource allocation and any later
launch. The pending native-stage recovery claim remains **unqualified**.
