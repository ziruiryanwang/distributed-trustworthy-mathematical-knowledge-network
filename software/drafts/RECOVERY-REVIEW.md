# Independent source review: native-free peer recovery

Status: static review only, 2026-09-21. No draft was imported, compiled, executed,
or tested. Only this review note was authored. The draft remains unintegrated
and does not qualify recovery of the current two-installation experiment.

## Disposition

The draft has no identified counterexample to its narrow conditional ledger
safety argument. Its original-attempt binding, terminal byte replay, writer
exclusion, native-stage exclusion and pending visibility transaction match the
intended contract. It is suitable for a separately reviewed integration and
fresh bounded test allocation, not a claim that recovery already works.

Before claiming the full evidence contract, resolve the handle-close evidence
qualification below. Before any execution, specify and review the new worker's
actual supervision, pins and resource allocation. Neither condition authorizes
changing the frozen installation or launching this draft during preparation.

## Reviewed source identities

Hashes are SHA-256. Product paths are relative to `software/`.

| Source | Bytes, where captured | SHA-256 |
| --- | ---: | --- |
| `drafts/recovery_worker.py` | 17795 | `271C8F8ABE9AC2182B24E6B2964B2143F826B71FE56C6C7210C13306942A9963` |
| `drafts/RECOVERY-IMPLEMENTATION.md` | 11834 | `32433C265082C19AB9AC630BFE421112DBCFC44F593EBF045193059A7F9B23FD` |
| `RECOVERY.md` | 4456 | `C03E7527889E1CE2ED8BE0C9C89C5B9DAB936B3BBDC8A25DE487140C41E0A54D` |
| `py/node.py` | 23544 | `CC9ACD8B5E2E9E2957A9C56908A4F7CC1BBBE9A1D628D32B40100F9278A78AB0` |
| `py/storage.py` | 15991 | `1D815B3C5CAA8209FB5F0811B4ED2FA9588240727DB0EF2E0512B6BA4C1A2DBF` |
| `py/domains.py` | — | `A3F44CCE31DDD79056F0683DE17D46712BFD46C99DFE71FAC56E27DD1DEB59C9` |
| `py/supervise.py` | — | `E5F35C0A88602757ECB7FF899F923F940B588E11E2A7C9C36D51FDBB2DFCAC1B` |
| `py/run_stage.py` | — | `499557B7C55A05F41460C0DFC894BA3C40CBD008D184415FD6B729B1CE422EFA` |
| `manage.py` | — | `057038F1B1FB95D4D740B326A3ADC07226D27FCEB086CD3C3EA0006AC71E76AB` |

The recovery draft and implementation-note hashes were unchanged at a second
read/hash check. This is a source comparison, not runtime evidence.

## Main safety checks

**Original execution, not merely equal request bytes.** `storage.reserve`
inserts the `attempt` record in the same transaction as the pending row and its
charge. `node.main` derives its call directory from the validated event parent.
`Dispatcher.execute` performs `prior` before reservation. Therefore an ordinary
later retry that encounters the pending request cannot create its own origin
marker. The recovery worker reconstructs the exact configuration-bound marker
for the selected original directory and checks its record columns and bytes.
It repeats this guard inside the visibility transaction. A clean later retry
receipt with equal request bytes but a different call directory cannot satisfy
that pending-transition guard under the trusted-state premise.

**Evidence binds the actual selected command.** Authentication checks the
original receipt's direct `scratch/calls/<name>/supervisor.json` location,
authenticated adjacent request/command bytes, receipt request digest, selected
client/request ID, supported peer operation, eleven expected current
interpreter/config/source pins, and the exact normal node command including
state, event, startup flags, cwd and launch flags. That eleven-pin set matches
the current ordinary `manage request` source. The SHA-256 of the selected raw
configuration must equal the store's configuration identity. Canonical command
encoding avoids Python's Boolean/integer and integer/float equality aliases.

**Cleanup is required for pending transition, not read-only replay.** A pending
transition requires the recorded initial empty Job, successful attach/resume,
positive direct PID and assigned process history, reaped direct child, final
active count zero, recorded closure and no cleanup/persistence/output-record
errors. Deliberate termination is allowed. It correctly does not require the
original request to have succeeded. The close-flag qualification below limits
the strength of the recorded closure premise.

**One visibility transaction.** With the OS writer lock held, the transaction
re-reads exact request identity/raw bytes, pending phase, absent response,
matching configuration, initialized state, selected active slot, no native
stage and the original-attempt marker. It invokes only `store.terminal` for the
mutation. Postconditions check the selected terminal bytes and that all meta
fields other than clearing `active` are unchanged. No call creates a candidate,
provider entry, context, head, stage or accepted result. No refund or deletion
occurs. Work left on disk remains inert retained material.

**Terminal replay.** After exact request identity and no-stage checks, an
already-terminal row returns its stored response bytes without parsing or
re-encoding. It need not be a refusal and need not own an unrelated active slot.
It still requires the owner lock and authenticated request/command/current-cut
evidence. No quiescence or attempt marker is needed for this non-mutating
branch. The order is correct: requiring `active = k` before distinguishing
terminal replay would unnecessarily block safe historical access.

**Uncertainty is not rollback.** After a terminal write is attempted, failure
before observed transaction completion produces `UNKNOWN_REPLAY_REQUIRED`.
Successful commit followed by event-output failure is not undone; stdout is
suppressed and later recovery must inspect the ledger. The draft imports no
checker, peer transport, native runner or supervisor implementation. Their
source files are read for pin equality only. The worker itself makes no native
acceptance claim.

These arguments assume the reviewed source executes, the selected runtime and
owner filesystem remain trusted, SHA-256 identity is adequate, the Windows Job
observations represent the assigned process tree, and SQLite/OS writer locking
provides the stated local transaction semantics. They are not a formal proof of
Python, SQLite, Windows, the kernel checker, or hostile-owner behavior.

## Findings and integration conditions

### R1 — Recorded Job closure is not yet checked OS handle-release success

In `py/run_stage.py:187`, `Job.close` calls Win32 `CloseHandle` but does not check
its Boolean return; it then clears its handle. `supervise.py` records
`job_closed = true` whenever that Python method returns without exception.
Consequently the draft's `require_quiescence` closure test currently proves only
that the wrapper returned, not that Win32 confirmed handle release.

The final zero-active observation and direct-child reap remain independent
premises, so this is not an identified route for the already-quiescent original
worker to resume. Nevertheless, a strict assertion that the handle was
successfully closed exceeds this source's evidence. Before claiming that
stronger contract, either check the Win32 result in a future reviewed runtime
cut or explicitly narrow the closure claim. A failed close must not silently
count as confirmed successful cleanup. Do not mutate the frozen current cut to
address this during another experiment.

### R2 — Recovery supervision is a required, deliberately missing integration

The draft has finite input/record bounds and the store's SQL step ceiling. It
does not itself enforce a whole-process wall, CPU, memory or process-count
grant. Its future caller must create fresh recovery-call evidence, bind the
recovery worker and dependencies, enforce declared external limits, and inspect
the recovery worker's own final process-tree/event records. Authenticating the
old node's eleven pins does not pin or supervise this new worker automatically.
The precise installed path and normal management command need independent
review before execution. This is an integration prerequisite, not a request to
add general recovery, service restart, or networking features.

### R3 — Availability excludes crash states with nonempty SQLite journals

`ControlStore.__init__`, at `storage.py:106`, rejects any nonempty `-journal`,
`-wal` or `-shm` file before opening the database. Process termination while a
reservation/visibility/recovery transaction is writing can therefore remain
blocked even if the original Job is quiescent. This profile can address a real
interruption during the transfer phase when the ledger opens under its existing
strict profile. It does not establish arbitrary process-crash recovery, and a
later retry cannot be promised to succeed for every uncertain persistence case.

No automatic journal deletion or database repair is appropriate here. Keep this
limitation explicit; a hot-journal repair profile requires separate design and
qualification. The same distinction applies if recovery itself is killed while
its transaction is active.

### R4 — Contract presentation should preserve the replay exception

`RECOVERY.md` lists active-request and cleanup conditions before its terminal
replay item. The draft and its implementation notes correctly apply those
mutation-specific conditions only to the pending branch. A future contract edit
should separate common identity checks, terminal replay, and pending transition
so a later implementation does not impose `active = k` on terminal replay or
discard a successful terminal response. No change to draft code is required.

## Minimum fresh evidence before a recovery result

The implementation note's proposed cases are appropriate. The positive path
must retain a genuinely supervised interrupted acquisition and its real
original reservation marker/receipt; fabricated pending rows or receipts are
only negative-guard fixtures. In particular:

- Demonstrate the genuine later-identical-retry receipt is rejected for a
  pending transition while the original receipt can resolve it.
- Compare ledger heads/provider entries, charges, stages and retained files
  before/after recovery, not merely its returned status.
- Check exact stored-byte replay for both recovered refusal and previously
  successful terminal response, including an unrelated pending active slot.
- Exercise wrong origin, request/config/cut, native stage, active slot and
  incomplete/nonquiescent evidence without introducing mathematical state.
- Distinguish commit-before-output loss from a hot-journal interruption; only
  claim the recovery cases whose actual persistence state was inspected.
- Use a new request ID for a subsequent ordinary successful acquisition and
  retain all original and recovery-call evidence; do not silently retry or
  refund the interrupted request.

Passing such finite tests would support this narrow owner-local interruption
profile. It would not qualify independent-host deployment, Byzantine evidence,
native-stage recovery, sustained storage renewal, or exponential useful growth.
