# Independent static review: recovery supervision

Status: 2026-09-21, source inspection only. Neither recovery draft was imported,
compiled, executed or tested. This review adds only this note; it changes no
product source, frozen installation, state, scratch evidence or test allocation.
It supplements [the worker review](RECOVERY-REVIEW.md), whose unchanged worker
was checked only where necessary to trace the new wrapper.

## Disposition

No new blocking source defect was identified in this wrapper under the declared
trusted-owner, stable-installation and openable-ledger assumptions. Its proposed
management wiring supplies the separate supervision and input binding missing
from the earlier worker draft. It is suitable for a fresh, separately pinned
integration and bounded qualification; it is not runtime qualification or a
claim of general crash recovery.

The existing unchecked `CloseHandle` result remains a limitation of this exact
cut. The integration note accurately narrows `job_closed` to a returned wrapper
call and separately requires final zero active processes and direct-child reap.
Claiming confirmed OS handle release would still require a reviewed source
change and qualification in a new cut.

## Checked source identities

SHA-256 values below were read from the actual files. Paths are relative to
`software/`. The wrapper and integration-note hashes and byte counts match the
requested review targets. The worker and supporting source hashes match the
earlier worker review. The current contract is a later document revision.

| File | Bytes when captured | SHA-256 |
| --- | ---: | --- |
| `drafts/recovery_manage.py` | 8897 | `F964227B040B1E5EF6947FC9E8744BD8BBEDEDE418EE1ADCE48ED1D6CB336A78` |
| `drafts/RECOVERY-INTEGRATION.md` | 13894 | `51CE9EDED63F64DDEFED25D6A9A2B67B8699B263B369DCF415AF6563799A2AEB` |
| `drafts/recovery_worker.py` | 17795 | `271C8F8ABE9AC2182B24E6B2964B2143F826B71FE56C6C7210C13306942A9963` |
| `drafts/RECOVERY-REVIEW.md` | -- | `7C7C4F5AB83A96DFA2AA098809756557E771462FDB5351E0C20DC1EDC3D308B1` |
| `RECOVERY.md` | -- | `C51DE692A84C517AFF37BC6E73941A4EAF403E897952433DD54AE11AC82A61CC` |
| `py/node.py` | -- | `CC9ACD8B5E2E9E2957A9C56908A4F7CC1BBBE9A1D628D32B40100F9278A78AB0` |
| `py/storage.py` | -- | `1D815B3C5CAA8209FB5F0811B4ED2FA9588240727DB0EF2E0512B6BA4C1A2DBF` |
| `py/domains.py` | -- | `A3F44CCE31DDD79056F0683DE17D46712BFD46C99DFE71FAC56E27DD1DEB59C9` |
| `py/supervise.py` | -- | `E5F35C0A88602757ECB7FF899F923F940B588E11E2A7C9C36D51FDBB2DFCAC1B` |
| `py/run_stage.py` | -- | `499557B7C55A05F41460C0DFC894BA3C40CBD008D184415FD6B729B1CE422EFA` |
| `manage.py` | -- | `057038F1B1FB95D4D740B326A3ADC07226D27FCEB086CD3C3EA0006AC71E76AB` |

## New wrapper checks

1. **Startup, installation and owner scope.** `recovery_manage.py:73` requires
   the documented Windows Python startup flags, absolute inputs and the
   configuration's installation binding. Explicit `install/py` module lookup
   works both beside the worker in `drafts/` and after both files move to `py/`.
   `node.load_config` checks its own installed path; the wrapper also checks the
   runner and supervisor module paths. Importing `node` for configuration does
   not load the checker or peer implementation or open the control database.
   The exact owner envelope permits only one configured client/request and a
   resolved direct `scratch/calls/<id>/supervisor.json`. Validation precedes the
   wrapper's evidence-directory creation. The proposed `manage.py` branch is
   placed before ordinary request dispatch and passes its actual entrypoint.

2. **Finite separate Job.** The wrapper calls `Transport` once, with a fresh
   exclusive recovery directory and no retry loop. `supervise.py:246` creates a
   new Job before the suspended child, then attaches and resumes that child.
   Limits are within the existing supervisor's ceilings: 30 wall seconds, 15
   CPU seconds, 256 MiB, 8 processes, 16 KiB request, 1 MiB stdout and 64 KiB
   stderr/event. Successful transport requires direct-child reap, final active
   count zero, bounded observations and successfully persisted final receipt.
   A reported worker `BLOCKED` result can correctly have completed transport.

3. **Grant and pins without a cycle.** Eleven ordinary inputs plus worker,
   wrapper and selected receipt make 14 input pins; `manage.py` adds one when
   integrated. The grant includes those inputs, target, request digest and
   limits. It is written exclusively, flushed and fsynced before its final
   bytes become the fifteenth or sixteenth supervisor pin. It never contains
   its own hash. The supervisor rereads every pin before launch. The final
   count, individual bounds and aggregate byte ceiling fit its enforced
   profile. The worker need not parse the grant: trusted wrapper wiring selects
   the actual request, command, limits and pin list recorded by the supervisor.

4. **Return bytes and worker observation.** `supervise.py:296` binds the strict
   event's request digest to the exact owner envelope and its response digest
   to captured stdout. The wrapper additionally requires zero native stages,
   no checker or mathematical authority, correctly typed exclusive transition/
   historical branches, and an exact selected-receipt pin for either branch.
   Nonzero exits and inconsistent observations become uncertainty. A successful
   response is forwarded byte for byte, preserving an already-successful
   terminal response rather than replacing or re-encoding it.

5. **Original attempt remains necessary only for mutation.** The wrapper's
   new grant does not create reservation evidence. `storage.reserve` still
   commits the original `attempt` record with the pending request and charge;
   ordinary `prior` rejects a later pending retry before reservation. The
   unchanged worker checks the selected original command/current cut and then
   requires the original directory's attempt record for pending transition,
   including inside its transaction. A same-bytes retry receipt cannot replace
   that association. Terminal replay remains separate from active-slot and
   cleanup guards. The current `RECOVERY.md` now preserves that distinction.

6. **Uncertainty does not infer rollback.** Supervisor failure, child nonzero
   exit and rejected event observations return `accepted: null` and
   `state_outcome: UNKNOWN`. Other wrapper exceptions are caught by the
   standalone or proposed management caller as owner-command failures. None
   allocates another invocation, rewrites a terminal response or repairs state.
   The worker's existing persistence-uncertainty branch remains intact.

## Explicit limitations and qualification conditions

- Pins bind observed bytes under owner control; they are not OS-enforced
  immutability, authorization signatures or protection against concurrent
  owner replacement of source, runtime, grant, database or evidence. Imported
  code and standard-library/runtime dependencies remain part of the trusted
  installation premise. Fresh qualification must freeze its full reviewed cut.
- Wrapper imports, bounded setup reads, directory/grant creation and final
  stdout delivery occur outside the worker Job. The proposed outer coordinator
  must also be supervised. Polling permits transient resource/output overshoot;
  cleanup settlement and final receipt writing are not a universal hard
  30-second completion guarantee.
- The failure objects with evidence paths cover handled transport/observation
  failures. A setup exception can leave partial evidence and produces the
  caller's generic owner failure without that path. A failed final stdout write
  or flush cannot guarantee delivery of a fresh, parseable error JSON: bytes
  may already have been partially emitted and the error output may fail too.
  Treat unsuccessful outer delivery as unknown and retain external capture plus
  recovery evidence; never infer that the transaction did not commit. This is a
  delivery limitation, not an identified unsafe ledger transition.
- Nonempty SQLite journal/WAL/SHM files remain blocked. A killed recovery
  transaction can itself leave such a state. This proposal supplies no journal
  repair, native-stage recovery, refunds, quota renewal or automatic retry.

The proposed slow-transfer experiment is consistent with the intended failure
window: genuine body progress every 0.25 seconds avoids the stated idle timeout,
while the explicit 10-second ordinary-call test grant interrupts before the
30-second transfer deadline. Its positive result still depends on observed
transfer progress, actual pending state, original marker, openable ledger and
final process-tree cleanup. Missing those observations is inconclusive/blocked,
not permission to fabricate or repair evidence.

Before a runtime claim, retain the proposed controls for invalid owner/domain
selection with no new evidence directory; changed source/grant/receipt before
launch; outer limits and nonzero exit; malformed/inconsistent event; and output
loss after commit. Demonstrate the real equal-bytes retry rejection, original
receipt recovery, exact refusal and successful-terminal replay, preserved
charges/files/visibility, and fresh ordinary acquisition. A changed-close source
cut needs its own close-failure control. The proposed harness, fixtures and
aggregate grant still require their separate review; this note runs none of
them and grants no reuse of `peer-01` or any prepared allocation.

## Addendum: mutable integration and checked-close controls

Static delta review, 2026-09-21, following root's integration into the mutable
`software/` development cut. This supersedes the draft-only integration status
above for these new source identities; the original review remains a record of
the unchanged drafts. This reviewer ran no Python, imported no product/test
module and executed no test. Only this addendum and the independent test source
`tests/test_job_close.py` were authored by this reviewer.

| New source | Bytes | SHA-256 |
| --- | ---: | --- |
| `py/recovery_worker.py` | 17803 | `1C5B9843152FFC6433722B5CF76C6F67B3C1C58EBA98C77607A8424342FE6299` |
| `py/recovery_manage.py` | 8837 | `E701D4B4FF7FB87EF048C61DCD559FEBA56A08AA169F0AB6B006791EFE2171A1` |
| `py/run_stage.py` | 26505 | `3C84F507DBB788827DBD50DE2D0D7552E4F72BD615F425CFD5F1DA278AC5A5BE` |
| `manage.py` | 12310 | `4219D9520DB7A35F3EE321C3A82AD246765E0C70957C3B29E924B59D6B606070` |
| `tests/test_job_close.py` | 3590 | `32E2DCA06191971CE2253EE01287D746A5C2E396DA1EB8F8E50FFDEE11992538` |

Direct file diffs establish that the integrated worker changes only its opening
docstring. The wrapper changes its opening docstring and the grant's
`close_evidence` value to `CHECKED_CLOSEHANDLE_RETURN`, preserving independent
zero-active/reap requirements. Against the preserved alpha installation,
`manage.py` adds exactly the proposed `recover` parser option and dispatch branch
with `owner_entrypoint=Path(__file__)`; `Job.close` adds the checked Boolean return,
raises `WinError(get_last_error())` on failure, and clears the handle only after
success. No new integration blocker was found.

The unchanged supervisor hash remains
`E5F35C0A88602757ECB7FF899F923F940B588E11E2A7C9C36D51FDBB2DFCAC1B`.
Its `finally` block records `job_closed: false` and a `job.close:<exception>`
cleanup error when the new close method raises. It retains any prior failure,
otherwise adopts that exception, marks transport failed, attempts to persist
the receipt, and raises `SupervisorFailure` instead of returning captured
stdout. Thus a close failure after apparently successful work does not become
successful transport; the recovery wrapper reports unknown state and cannot
infer rollback. Final zero-active and reap observations still precede close.
The retained Python handle enables an explicit caller retry, but neither the
supervisor nor the public recovery wrapper silently retries a failed close.

The new check addresses the earlier source-level close-observation gap for this
new cut. It supplies no retrospective strengthening of old receipts. Both
`product-local/peer-01/alpha/install` and `beta/install` retain runner hash
`499557B7C55A05F41460C0DFC894BA3C40CBD008D184415FD6B729B1CE422EFA` and
management hash
`057038F1B1FB95D4D740B326A3ADC07226D27FCEB086CD3C3EA0006AC71E76AB`;
neither has a recovery wrapper installed. Their selected preserved files match
the original reviewed cut. Recovery authenticates original source pins against
the current cut, so old-runner receipts cannot simply be reused to qualify this
changed runner. Fresh original-call evidence remains required.

The independent test source defines exactly **four** `unittest` controls:
successful close clears the handle; a false return raises the injected OS error
and retains the handle; repeated close after success performs no second release;
and an explicit second close can release a handle retained after injected
failure. Each constructs `Job` with `__new__`, bypassing its OS constructor, and
uses in-memory kernel/error fakes with replacements restored afterward. They
test the actual `Job.close` method and make no Win32 call, create no real Job,
launch no child, allocate no native stage, open no control store and write no
fixture files. These are branch controls, not evidence of a real OS release or
recovery transaction. Their separately reviewed root worker must supply bounded
outer execution and retained results; no controls were run during this review.

All other earlier limitations remain, including trusted stable inputs,
out-of-Job wrapper work, partial final-output uncertainty and the nonempty
SQLite-sidecar exclusion. A passing close control alone would not qualify the
slow-transfer recovery path or whole-crash recovery, and authoring it does not
alter any active experiment's grant.

### Separate close-01 harness source review

The root-authored harness was subsequently inspected without execution:

| Source | Bytes | SHA-256 |
| --- | ---: | --- |
| `tests/close_worker.py` | 2231 | `56B0932092BE82CB3BBADC8AAF4198443B0C0230C396F8915F8D29EA1074E354` |
| `tests/run_close.py` | 3892 | `68DEB1C33B2FBF92E8ACEB3FD523D3A85B61D3AA536255F7B1E066915B0B2B02` |

No source blocker was identified for the proposed once-only, trusted-owner
`qualification/close-01` allocation with exactly four selected tests. The launch
record must bind, in order, the interpreter, coordinator, worker, test source,
runner, supervisor and domains source; the coordinator checks that ordered list
before creating the new exclusive root. The generated config adds an eighth
supervisor input pin and binds the selected state and test count. No existing
qualification root is reused and there is no automatic retry.

The worker accepts only the fixed request, discovers `test_job_close.py`, and
requires actual test count equality, successful results and no skipped tests.
Its event binds the captured request and response hashes. The coordinator checks
both the child exit and `PASS`/test count after the existing supervisor enforces
30 seconds wall, 15 seconds CPU, 256 MiB, 8 processes, and 64 KiB output/event
bounds, including quiescence and the new checked close. A test failure still
returns a parseable worker response, but the coordinator converts it to a failed
qualification result. Success is deliberately `PASS_PENDING_OUTCOME_REVIEW`.

The fake ctypes replacement is confined to the child test process and restored
after each control; it cannot replace the enclosing supervisor's real Job calls.
The top-level coordinator's startup, pinning and final record handling remain
cooperative trusted-owner work outside this inner Job, as root explicitly
declared. The new root retains config, launch, case outputs/receipt and result.

Passing these four controls would establish the mocked success/failure/retry/
idempotence branches, with independent real enclosing-process cleanup evidence
only if that receipt confirms it. The supervisor's reaction to an injected close
failure was traced statically; this small harness does not inject a failing
`CloseHandle` into the actual enclosing supervisor. Neither a four-test pass nor
its real Job receipt would qualify peer recovery, a recovery transaction, hot
journal handling or the slow-transfer experiment. At this review point the
launch record had not been reviewed and no harness or test had been run.

Exact launch follow-up: `qualification/close-launch-01.json` is 1553 bytes,
SHA-256 `9CEFD2D02B529557AD54F97FE87403E85992C355690CC479A4285173773B8CFD`.
Its schema is 1 and selected test count is exactly 4. All seven paths, byte
counts and SHA-256 values were independently compared with the current files;
all match the reviewed order and source identities. The interpreter is
`D:/Python314/python.exe`, 106208 bytes, SHA-256
`03168C01B7B7491423350E82C26FEE71F35B43694D1319D3C668BDA6903A0C38`.
The prospective `qualification/close-01` directory did not yet exist. No blocker
was identified for this exact, once-only native-free control run. This closes
the static launch review; it reports no execution result. The author of this
review also authored the four branch tests, but did not author the harness;
any later outcome audit must be described with that authorship disclosed.
