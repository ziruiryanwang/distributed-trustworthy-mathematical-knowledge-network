# Recover an owner crash while its finite supervisor survives

2026-10-21, core_release. Source/theory-only decision requested by root.
No implementation, import, runtime, fault experiment, deletion or Git mutation.

## Decision

**Implement the surviving-supervisor lane first.** Reuse the actual current
Windows Job handle, exact direct-process handle and original finite cleanup.
Prospectively bind the launch to an enrolled manager/session; after real
whole-tree quiescence, let that same trusted supervisor commit a distinct
`QUIESCED_UNCLEAN` state against its exact matching run records. Do not accept
an imported report as closure or relabel an unclean exit as orderly `CLOSED`.

Initially this permits **retirement/reclamation after the original retention
horizon**, not automatic reopening of crash-damaged mathematics/storage. The
other slot can continue under its own original authority. Recovery of actual
SQLite/service state before expiry is a separate boundary, not required for
this first useful implementation. Loss of supervisor authority stays UNKNOWN;
do not delay this lane to build a general crash-complete local broker.

## What the exact existing supervisor establishes

| Actual source | SHA-256 |
|---|---|
| `tools/Run-V5-Check.py` | `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651` |
| `product-local/v4-library-commons-02/commons-v4/operator/commons.py` | `6ea16154f4533e80d2e4e27e12fb6fa0ab7abfa0ff2c52cfb7479c1a35a8c1c9` |
| `product-local/v4-library-commons-02/commons-v4/receiver/helpers/run_stage.py` | `bdd2cbc28258f49ef08b678ba54b437ff541ef4deb0af4aa36795d2baa19b028` |

The runner authenticates these frozen sources through manifest `a93714ec...`.
`Job` creates an **unnamed**, noninheritable handle with JOB_TIME,
ACTIVE_PROCESS, JOB_MEMORY and KILL_ON_JOB_CLOSE; neither breakaway limit is
enabled. The wrapper creates one direct child suspended, then assigns it to
that Job and resumes it. The wrapper remains outside the Job it controls.
Its cleanup can terminate the Job and direct child, waits on the exact direct
process object, and queries Job accounting until active processes are zero.
The success path also requires zero and no cleanup uncertainty before closure.

This is useful current-kernel evidence. It is **not already a manager recovery
protocol**: command metadata has argv/cwd/limits but no prospectively bound
manager epoch/root/session/run identity. The Job is closed before the outer
result is saved. A later reader cannot recover that live capability by hashing
or trusting the saved result. Existing evidence and UNKNOWN rows are therefore
not retroactively eligible for this new lane.

## Smallest implementation seam and ordering

Use a fresh selected managed-session launcher, reusing the Job class and finite
supervision/cleanup pattern. Do not edit frozen supervisors or add a generic
`accept_closure_json` method.

1. **Enroll and bind before child effects.** Under the manager lock, durably
   reserve one fresh supervisor/session nonce. Bind the enrolled manager's
   epoch, config/marker hash, exact root identity, fixed worker/source profile,
   original finite launch/cleanup limits and one-shot launch intent. No
   ambiguous commit may be followed by launch. Existing roots without this
   prospectively bound facet remain outside automatic recovery.
2. **Establish live worker authority.** The trusted launcher starts only its
   fixed managed-owner entry point. A private launch handshake binds that
   current child to the reserved session; a serialized nonce alone is not a
   public execution capability. Every managed run reservation durably records
   the session plus `(slot, generation, sequence, cumulative_run)` **before**
   creating its run paths, stores, listeners or Node. One bounded session facet
   plus at most two occupied records suffices; no unbounded launch history.
3. **Seal further launches before observing zero.** The supervisor's one-shot
   launch path must be exhausted/revoked, with no future assignment or resume
   capable of introducing another runnable worker. It retains the exact Job
   and direct-process handles. All supported descendants must arise from the
   contained CreateProcess tree; no WMI/service/scheduled out-of-tree launcher
   or external delegated writer is permitted by this worker profile.
4. **Observe, do not infer.** After normal exit or bounded termination, require
   successful wait on the exact direct process and a fresh successful
   `QueryInformationJobObject` observation `ActiveProcesses == 0` on that exact
   still-owned Job. Require no unresolved cleanup observation. Nonzero exit,
   forced termination or terminated-process counts may still establish
   *quiescence*, never orderly success or mathematical correctness.
5. **Commit while the capability exists.** Add the recovery transition between
   actual quiescence and Job-handle close, not after parsing the old wrapper's
   result. The trusted supervisor opens a fresh finite manager owner, validates
   the original binding and exact matching current run/session, and issues an
   internal nonserializable closure guard from those live observations. It
   commits `QUIESCED_UNCLEAN` for matching RESERVED/LIVE/CLOSING/UNKNOWN rows,
   preserving phase/retirement intent, generation, cumulative runs and all
   original limits. Never modify a newer/different session or overwrite a
   genuine existing orderly CLOSED record.
6. **Separate recovery from storage adoption.** The persisted guarded transition
   is local registry state, like a previously executed orderly-close transition,
   not authority imported from an arbitrary report. A new owner may use it as
   a retirement prerequisite only. Require a fresh conservative-clock adoption
   to discharge the unchanged retention horizon, then the existing exact
   inventory/window reclaimer. SQLite journals, missing markers, partial
   provisioning and unknown files retain their ordinary HOLD behavior.

This requires a narrow prospective session facet/worker entry point, a
post-quiescence/pre-close supervisor seam, and explicit unclean-quiescence
handling in lifecycle/reclamation. It does not require a new network protocol,
certificate system, identity market, entire installation copy or memory survey.
The recovery owner has its own finite action budget; it does not renew the
crashed run's service authority or refund consumed work.

## Safety and conditional progress

Let S be the prospectively bound one-shot session and J its exact Job. Under
trusted selected launcher/worker code, intact nonrolled-back private registry,
no out-of-tree writers, correct Windows containment/accounting and sealed
launch authority:

`direct_process_waited(S) AND active(J)=0`
implies no S-owned process can subsequently act on its managed generation.

The durable identity join transfers that observation only to current runs
stamped with S. A new generation/session has a different binding and does not
inherit old closure. Process quiescence establishes neither SQLite integrity
nor fulfillment of a future retention promise. The explicit unclean state and
original-horizon gate prevent those unjustified inferences.

Progress is conditional: if the supervisor survives, Windows can terminate and
account for all contained processes within the original cleanup allocation,
the exact registry remains writable, and later original horizons expire under
the adopted clock, the affected slot can reach the existing reclaim boundary.
Any failed wait/query, binding mismatch, uncertain commit, exhausted original
cleanup, partial marker or unknown inventory remains charged/HOLD. Reacquiring
the registry lock merely allows a write; it does not establish closure.

## Supervisor crash and the actual pre-assignment gap

**Do not claim this first lane covers loss of the supervisor.** Its unnamed Job
handle cannot be reopened by a fresh owner. Kill-on-last-handle-close is a real
backstop, but neither an absent PID, free port, released lock, elapsed saved
deadline nor saved successful-looking JSON is a fresh whole-tree observation.
Missing/incomplete authority remains UNKNOWN; no implicit cleanup or budget
reset follows. A supervisor that dies after the guarded durable transition is
different: the already committed exact transition remains valid under the
normal private-registry/no-rollback premise.

There is also a real crash interval between `Popen(CREATE_SUSPENDED)` and
assignment. If the supervisor dies there, the direct suspended process is not
in the Job and kill-on-Job-close need not reach it. In the selected source the
supervisor has not resumed its primary thread: **the worker has not executed
application code or written managed state**, although Windows process creation
and the parent's output/intent writes have occurred. This is an orphan/resource
limitation, not a reason to credit that process with completed work. A surviving
supervisor already handles it by killing/waiting the exact direct process. Do
not use the lack of managed writes to call an unreaped process closed.

If later evidence warrants supervisor-crash-complete work, the narrow candidates
are atomic creation-time Job assignment using `PROC_THREAD_ATTRIBUTE_JOB_LIST`
and a separate local keeper retaining the exact Job handle under a fixed finite
lease. A keeper must independently terminate/query after supervisor loss;
duplicating a handle otherwise delays kill-on-last-close. Simultaneous loss of
all holders still needs a separately justified OS-teardown recovery boundary.
A named Job may help reacquire a present object, but **name absence is not
adopted here as proof of completed tree termination**. None of these additions
is selected, implemented or required to qualify the useful surviving lane.

## Primary platform references consulted

- [Windows Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects):
  CreateProcess descendants, breakaway and out-of-tree WMI distinction; current
  accounting; named handles; kill-on-close and object lifetime.
- [CreateJobObjectW](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-createjobobjectw):
  unnamed/noninheritable default and existing-name behavior.
- [UpdateProcThreadAttribute](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute):
  creation-time Job-handle list on supported Windows versions.

These API contracts justify the proposed direction, not an already implemented
recovery result. Root should select only the prospective session/guard seam next;
tiny fault controls should follow source review rather than precede the model.
