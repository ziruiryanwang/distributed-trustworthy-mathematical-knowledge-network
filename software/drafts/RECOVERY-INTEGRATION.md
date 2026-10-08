# Recovery supervision and fresh qualification proposal

Status: source proposal only. Neither recovery draft has been executed or
installed. No current product, frozen installation, qualification copy or test
allocation was modified. Read this with
[the worker specification](RECOVERY-IMPLEMENTATION.md) and
[its independent review](RECOVERY-REVIEW.md).

## Minimal owner interface

The proposed public command is `manage.py recover --config <absolute-config>
--request <absolute-owner-envelope>`, with Python `-B -E -s -S`. The envelope
remains the worker's exact owner-only `recover_peer` selection of client,
request ID and original supervisor receipt. No peer message can invoke it.

The new [recovery_manage.py](recovery_manage.py) exposes `invoke_recovery(args,
owner_entrypoint=...)` and a standalone draft `recover` command. It does not
open the control store, load the worker in-process, call peer networking,
allocate a native stage or change the original receipt. It validates the
owner's envelope and issues one finite separately supervised worker invocation.

In a **new reviewed source cut only**, put `recovery_manage.py` and
`recovery_worker.py` together under `py/`. The proposed management delta is:

```python
# Existing parser loop: add a command with the same two input options.
for name in ("request", "inspect", "recover"):
    command = commands.add_parser(name)
    command.add_argument("--config", required=True, type=Path)
    command.add_argument("--request", required=True, type=Path)

# Existing dispatch: insert before the generic invoke(args) branch.
elif args.command == "recover":
    from recovery_manage import invoke_recovery
    result = invoke_recovery(args, owner_entrypoint=Path(__file__))
```

This is a patch proposal, not an applied edit. Existing management handling of
`TRANSPORT_FAILED`, `OWNER_COMMAND_FAILED`, exact stdout and nonzero exits can
remain unchanged. The original node's eleven-pin call profile is unchanged;
recovery has its own larger source/grant pin set. No schema migration is added.

## Separate supervision and evidence

Each explicit invocation creates exactly one fresh
`scratch/recoveries/recovery-<uuid>/` directory containing `grant.json` and
`cases/recover/{request.json,command.json,stdout.txt,stderr.txt,event.json,
supervisor.json}` as produced by the existing supervisor. UUID directory
creation is exclusive; collisions are failures, not a reason to reuse evidence.
No automatic retry, repair, counter reset, refund or cleanup sweep is performed.

| Resource | Recovery-worker grant |
| --- | --- |
| Wall / CPU | 30 seconds / 15 seconds |
| Job private commit | 256 MiB |
| Active processes | Existing supervisor's fixed maximum 8; expected actual child count 1 |
| Request / stdout | 16 KiB / 1 MiB |
| Stderr / event | 64 KiB / 64 KiB |
| Poll / cleanup settlement | 0.05 seconds / 5 seconds |
| Selected grant / original receipt | At most 64 KiB each |
| Input pins | At most 16 files, 16 MiB each, 64 MiB aggregate |

These are the existing supervisor's polled envelope and Job limits, not hard
instantaneous output/disk caps. The owner wrapper's bounded setup and final
stdout forwarding occur outside the worker's Job; qualification must also
supervise its coordinator. There is no claim that every OS cleanup operation
finishes by the worker's nominal wall deadline: cleanup waits follow it, and
final receipt serialization lies outside the supervisor's success wall endpoint.

The standalone pin set contains the original node-call eleven inputs (current
interpreter, config, nine installed sources), the recovery worker, this wrapper,
the selected original receipt, and the finalized grant: 15 pins. A future
integrated management invocation additionally pins `manage.py`: 16 pins. All
paths are explicit; no installation-wide census is needed for invocation.

The grant lists selected inputs, request digest, original receipt pin, target,
worker/state and limits. It does **not** list its own hash. After one exclusive
durable write, its final bytes are added to the supervisor pin list. Thus the
grant is bound without a circular self-hash. The supervisor verifies every pin
before launching the worker suspended, assigning it to a **fresh separate Job**,
and resuming it. Owner installation/runtime stability remains an assumption;
prelaunch hash checks do not physically prevent later owner writes.

The worker authenticates original execution association as previously reviewed:
exact original request/command/current cut plus the reservation-bound attempt
marker. The new wrapper's grant cannot manufacture or replace that marker. The
wrapper also checks that a reported transition or terminal replay cites the
same original receipt bytes it pinned. It forwards terminal response bytes
without parsing/re-encoding them; a successful historical response stays
successful. A `BLOCKED` worker outcome can also be a completed transport.

Any uncertain transport, nonzero child exit or inconsistent worker observation
returns `accepted: null` and `state_outcome: UNKNOWN` with the new evidence
directory. It never infers rollback or substitutes an interruption refusal for
an unseen terminal response. A later explicit recovery re-reads the ledger.

## Independent-review conditions preserved

The worker's common identity checks, already-terminal replay and pending
transition are separate branches. Only the pending branch needs original
attempt association, quiescence, selected active slot and atomic refusal.
Neither branch permits a selected native stage. Recovery changes no counters.

The current runner's `Job.close()` ignores the Boolean result of Win32
`CloseHandle`. Current `job_closed: true` therefore means only that the Python
wrapper returned, **not** confirmed OS handle release. Final active-zero and
direct-child reap remain independent safety premises. Current evidence must be
described at that weaker strength. For the future production source cut, the
recommended tiny root-owned change is to check the Win32 return and propagate a
failure, with a separately reviewed failing-close test. Do not mutate the frozen
runner or pretend the draft repairs it.

The existing store rejects a nonempty SQLite journal/WAL/shared-memory sidecar.
This recovery can resolve a transfer interruption whose ledger opens under that
profile. It cannot promise to repair arbitrary mid-transaction process death.
If the original or recovery worker dies while persisting a transaction and a
nonempty sidecar remains, stay blocked and retain the files. No deletion, SQLite
repair flag, migration, charge refund or automatic retry is in this proposal.

## Concrete genuine slow-transfer qualification

This outline requires a new source cut, fresh owner state/scratch, newly frozen
pins and an explicit root-approved test grant. It must not run against `peer-01`
or any current prepared installation. Root alone may implement/run the later
harness; this note does not launch it or authorize current allocation reuse.

The core falsifiable experiment is deliberately inside transfer preparation,
outside the short reservation/visibility transactions:

1. **Create a real source and selection.** In fresh producer/consumer nodes,
   use ordinary `init`, a known small valid Lean submission, `publish` and
   `expose` to produce a committed immutable view. Use consumer `peer_find`
   against its configured loopback alias to create a genuine `remote` handle.
   The selected valid bundle must be at most 1 MiB and contain enough payload
   after its manifest to withhold at least 64 trailing bytes. Freeze the exact
   catalog/bundle bytes, view binding, source pins and port selection. No
   fabricated remote, candidate, pending or publication rows establish this path.

2. **Bound the fault sender independently.** A reviewed owner test sender may
   serve only this frozen catalog and selected bundle, on `127.0.0.1` at the
   configured port. Run it under its own Job: at most 60 wall seconds, 10 CPU
   seconds, 256 MiB, 8 connections and 4 MiB attempted output. It records the
   selected HTTP path, body digest, actual sent prefix and timing. This is test
   fault injection, not an unreviewed modification of product peer code.

3. **Send a valid prefix slowly, not a malformed response.** For the first
   selected `/v1/bundle/<digest>` request, send the ordinary 200 response with
   exact full `Content-Length`, `application/octet-stream` and `Connection:
   close`. Send the genuine body except its final 64 bytes, then at most one
   additional genuine byte every 0.25 seconds until the client disconnects or
   the sender grant ends. Choose the cut after the complete manifest and into
   object framing/payload so retained incoming files can really exist. Do not
   send different content, close early intentionally, or violate framing.

4. **Interrupt before the product's timeout.** The current client has a 5-second
   idle timeout and 30-second total transfer deadline; the ordinary public
   peer-call wall cap is 120 seconds. Simply stalling under that ordinary cap
   would yield a normal terminal timeout, not qualify pending recovery. Instead,
   the reviewed qualification coordinator calls the unchanged `Transport` with
   the exact ordinary eleven pins/normal node command and a **10-second
   case-specific wall override** for this one acquisition. Its evidence root
   remains consumer `scratch/calls`. The sender's 0.25-second genuine-byte
   progress keeps it below the idle timeout while the outer Job is terminated
   before the total transfer deadline. This is a test-only tighter grant, not a
   new public management override or changed installed source.

5. **Do not fake a successful interruption.** Require recorded bundle-transfer
   progress before the supervisor cutoff and genuine final process-tree cleanup.
   After cleanup, inspect the actual existing ledger and retained files under
   owner control: exact pending row, matching original-attempt marker, selected
   active key, zero assigned native stages, unchanged provider cut/candidate/head
   visibility, and an openable no-nonempty-journal state. Capture the selected
   request's file census, counter snapshot and full immutable input evidence.
   If setup consumed the cutoff, a timeout terminalized normally, the sender
   finished too early, or a journal remains, report **inconclusive/blocked for
   this positive case**. Do not fabricate state, adjust evidence, or rerun without
   a new explicit test grant. Native-free acquisition may load the pure checker;
   `checker_loaded = false` is required of recovery, not of that acquisition.

6. **Reject the equal-bytes retry substitution.** Make one real supervised
   ordinary retry with exactly the interrupted request bytes. It must return
   pending/block before reservation and leave counters unchanged. Its fresh
   quiescent receipt has a different directory and no reservation marker.
   Run the public proposed recovery command selecting that retry receipt; require
   `RECOVERY_ORIGINAL_ATTEMPT_NOT_BOUND`, unchanged pending/active/counters/files,
   and no new mathematical visibility.

7. **Recover and replay precisely.** Select the actual original receipt using a
   new explicit public recovery invocation. Require the exact stored interruption
   refusal, only its active slot cleared, and all counters/files and unrelated
   rows preserved. Repeat recovery and the original ordinary request separately:
   both must replay the exact stored bytes without a new charge or stage. Keep
   each new recovery grant and its own supervisor/event evidence.

8. **Demonstrate resumed normal work.** The sender's later selected bundle request
   returns the complete original body promptly. With a fresh ordinary request
   ID, require acquisition to succeed and produce its normal candidate-only
   result, not mathematical acceptance. Then recover that successful terminal
   request and require its exact successful bytes without replacement. Verify
   all helpers/worker Jobs quiescent before final filesystem/ledger census.

The coordinator should have an explicit aggregate grant before launch: at most
16 ordinary node invocations, 8 recovery invocations, 2 sender sessions, 12
native stages across fresh setup, 1,800 seconds wall/observed aggregate CPU and
2 GiB observed retained experiment bytes, excluding the separately pinned
external Lean runtime. Treat these as ceilings, not targets; stop on the first
unexpected state or exhausted grant and retain evidence. Do not recycle counters
to fit the ceiling. The precise harness/fixture/source cut still needs review.

## Additional bounded controls and claim limit

The independent worker review's invalid identity/cut/command/attempt/active/
native-stage/nonquiescent/JSON controls remain required. Add wrapper controls for
changed grant/source/receipt before launch, malformed owner envelope or
out-of-domain receipt selection causing no new directory, exhausted outer
limits, child nonzero exit, inconsistent event
profile and forwarding failure after worker commit. A grant self-pin must never
be added to its own contents.

Test original successful-byte replay separately from pending cleanup guards,
including another pending request's active slot. A fabricated negative fixture
can test a guard but is not genuine interruption evidence. Distinguish an
observed clean commit-before-output loss from a hot-journal interruption; the
latter is explicitly blocked here. A future checked-CloseHandle test must
establish the stronger close claim before that wording is used.

Passing would qualify this narrow owner-local transfer-interruption recovery
under its declared cut and conditions. It would not qualify power loss,
native-stage recovery, hot-journal repair, hostile-owner evidence, independent
hosts, quota renewal, permanent availability or useful exponential growth.
