# Prospective surviving-supervisor recovery: source checkpoint

2026-10-21, core_release. Implements root's `CRASH-OWNER-RECOVERY-SELECTION.md`
and adopted decision `7a2ce0d32bc59410e6f419711d7e793e556a55e465904df05a516be588cf26aa`.
Source only: no Python import, tests, processes, runtime, deletion, migration,
installation or Git mutation by this author. Independent review and root's tiny
real process-tree discriminator remain separate gates. Full v5 is not complete.

## Exact source and reuse

| File | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/supervised_generations/placement/lifecycle.py` | 38399 | `bec62143313e1abd400550bae45a6334be2ddffb94d77a14ba9b5853b565042f` |
| `software/v5/supervised_generations/placement/sessions.py` | 20233 | `b4cfab61c990464756e87a7344e2a029a5374602283a4255d4d5aa854090b7f7` |

The lifecycle is derived from frozen `bounded_reclamation/placement/lifecycle.py`
`d59615b664ca8dc934d07778046164313d226965cc3b2486e1e98d15bd57d9ef`.
It retains the existing manager/service/retirement implementation; changes are
the new schema and bounded session columns, prospective worker/run joins,
pre-mutation validation on recovery opens, and the distinct unclean-quiescence
state in retirement/reclamation guards (never in service restart).

Reuse unchanged `bounded_reclamation/placement/reclaim.py`
`19713fc4baec821a5c77a0071182c63401b292cbe79a7ed7c04b7deba50e1894`
and `bounded_generations/client/serve_generations.py`
`404365849dd0e41860ba8ccda01a5b064d028241a2d8b0063d76936fcd306687`.
All three predecessor hashes were reread and remain unchanged. No reclaimer or
full supervisor has been copied/reimplemented. Integration must load the fresh
lifecycle as `placement.lifecycle` and sessions as `placement.sessions`, alongside
the same adopted SDK and unchanged reclaimer/composer; these two source files
alone are not a standalone installation.

The adapter pins existing `operator/commons.py`
`6ea16154f4533e80d2e4e27e12fb6fa0ab7abfa0ff2c52cfb7479c1a35a8c1c9`
and `receiver/helpers/run_stage.py`
`bdd2cbc28258f49ef08b678ba54b437ff541ef4deb0af4aa36795d2baa19b028`.
Root's adopted loader must load those actual modules without monkeypatching.
The profile digest binds the prospectively selected trusted worker/source map;
it is not an assertion that arbitrary code named in argv is automatically safe.

## Concrete owner and worker API

Fresh manager config uses `DMKN_V5_TWO_GENERATION_MANAGER_SUPERVISED_V1`, with
the previous config fields plus `max_sessions` in 1..4096. Old roots have a
different config/marker/schema and cannot be migrated by open. The registry
still has exactly two slot records and one meta row. The meta row holds one
bounded current session plus its monotonically charged session count, not an
event history. Each occupied run has one bounded exact session join.

1. Parent opens a fresh idle `ManagedGenerations` with a deadline covering the
   intended main wall allowance plus cleanup. Its remaining CPU allowance must
   include ten seconds for the two fixed five-CPU-second registry actions.
2. Parent calls `sessions.supervise(manager, profile={"sha256": worker_map_hash,
   "ownership": sessions.OWNERSHIP}, argv=..., cwd=..., evidence=...,
   limits=..., operator_module=A, job_module=J, cleanup_seconds=25)`.
   Optional `stdin_bytes` and `serve_seconds` retain the existing supervisor's
   exact restrictions. Evidence must be fresh and outside the manager tree.
   The manager is consumed/closed before the single child launch; failure or
   ambiguous session reservation never launches it.
3. Child opens the same exact manager/config, calls
   `manager.join_current_worker(worker_map_hash)`, then allocates/reserves runs
   or uses the unchanged `GenerationServices` composer. Allocation and run
   reservation require this current join. A run's outer deadline cannot exceed
   the session's original main deadline. Its session+slot+generation+sequence+
   cumulative-run join is committed before the composer creates paths/actors.
4. After the supervisor returns, a fresh owner can inspect the durable state.
   `QUIESCED_UNCLEAN` cannot reopen a service. Ordinary `adopt_clock`,
   `begin_retire`, `commit_retired`, `begin_reclamation` and `reclaim_step` still
   require the original horizon, current clock authority, exact inventory and
   prepaid original deletion limits. No deletion is performed by supervision.

The private `_launch` open parameter is exclusively the internal same-process
launch object; it is not an imported recovery token or a public owner API.

## Why the launch join is not a serialized-nonce capability

The existing supervisor constructs a suspended direct `Popen`, then calls the
supplied Job class's `attach_resume`. The scoped subclass retains that exact
process object and HANDLE, queries its current Windows PID and creation FILETIME,
and commits the pair into the reserved session **before** calling the unchanged
AssignProcessToJobObject/NtResumeProcess implementation. Failed/ambiguous binding
cannot resume. The worker queries its own kernel process identity and requires
equality with the durable pair before joining. A copied nonce or profile digest
alone therefore does not enroll an arbitrary caller.

This identification is justified only together with the selected trusted launcher,
fresh nonce/session, private no-rollback root and fixed worker/no-out-of-tree-writer
premises. PID+FILETIME is not advertised as cryptographic global uniqueness or as
fresh closure evidence after supervisor loss. No extra pipe, keeper or duplicated
Job handle is needed for this selected lane.

## Recovery ordering and safety argument

The scoped Job initializes its guards before `super().__init__`: the frozen Job
constructor can dynamically call `close()` on a partial limit-setting failure.
That never arms recovery. Only one Job creation and one attach/resume attempt are
allowed. `close()` seals future attach first and performs recovery at most once.

The observation requires the original Job HANDLE, original direct-process HANDLE
and identity, a fresh signaled `WaitForSingleObject(handle, 0)`, successful exact
`Popen.wait(timeout=0)`, and fresh current Job `ActiveProcesses == 0`. A cached
Popen returncode alone does not suffice. The original Job stays open throughout.
The observation is repeated inside the exact manager recovery transaction.

The private recovery open validates the full original session and filesystem
root/slot/marker/registry/lock identities under the acquired owner lock **before
any lifecycle rewrite**, and bypasses inherited automatic UNKNOWN rewriting.
The transaction rechecks current session/worker identity, never overwrites a
different session or genuine CLOSED, and changes only matching unresolved runs
to `QUIESCED_UNCLEAN`. Phase, existing failure/retirement intent, horizon and all
run charges remain. Ordinary owner reopen still changes RESERVED/LIVE/CLOSING to
UNKNOWN after validating the enrolled root, as before. The initial independent
review identified the stale-open-before-match hazard; the current source fixes it.

Under sealed launch authority, Windows containment/accounting, trusted selected
code and no other writers, exact direct wait plus current whole-Job zero means
this session has no process that can later act. The durable exact run join carries
that conclusion to its own rows only. It proves neither orderly resource close,
SQLite content integrity, mathematical validity nor expiration of a promise.

Session count and run charges are never refunded. Uncertain registry COMMIT poisons
the owner; no attempt is retried. The launch's original main deadline plus the
preallocated 25..60-second cleanup allowance bounds recovery authority. The default
25 seconds accounts for the unchanged direct wait (10), Job settle (10), and
registry margin (5); bind/recovery have two calls and five CPU seconds each. These
are guarded software budgets, not hard wall-time guarantees around blocking OS or
SQLite calls. Root's enclosing finite allocation must cover the full operation.

## Deliberately unchanged limits

- Supervisor loss leaves unresolved sessions/UNKNOWN runs held. Saved PID/time,
  JSON, elapsed deadline, free port or released lock does not heal them.
- The suspended-before-assignment resource-orphan gap is not repaired. No named
  Job, keeper or atomic launcher was added; the existing cleanup remains intact.
- No automatic storage adoption, restart from unclean state, migration, refund,
  retention extension or unknown-file deletion was added.
- Physical SQLite/VFS envelope adoption remains false. No mathematical checker,
  proof, discovery policy or useful-growth claim changes.

Next highest-payoff evidence is source review plus one real tiny crashed owner
and descendant, not another service/network/proof or memory investigation.
