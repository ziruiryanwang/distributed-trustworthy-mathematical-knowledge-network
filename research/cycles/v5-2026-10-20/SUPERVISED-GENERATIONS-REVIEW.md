# Prospective surviving-supervisor recovery: independent source review

2026-10-21, support_guest. **PASS for the selected source boundary under its
explicit trusted-worker/private-root premises; NOT a runtime or launch result.**
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Root owns adapters, finite selections, actual execution, adoption and Git.
This reviewer performed source/hash/AST checks only: no product import,
Windows API invocation, process, test, service, deletion or installation work.

## Exact reviewed source

| Relative canonical path | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/supervised_generations/placement/lifecycle.py` | 38399 | `bec62143313e1abd400550bae45a6334be2ddffb94d77a14ba9b5853b565042f` |
| `software/v5/supervised_generations/placement/sessions.py` | 20233 | `b4cfab61c990464756e87a7344e2a029a5374602283a4255d4d5aa854090b7f7` |
| Adjacent `SUPERVISED-GENERATIONS-SOURCE.md` | 8832 | `3b0b37b66506b41105b5d49daf9d33bb0defe5ddc35d2dc08e7b50dc80dff1fc` |

The root selection and complete decision7a2ce0d3 were read, along with the
complete session implementation, lifecycle diff against reviewed frozen
d59615b6, final checkpoint, and actual frozen supervision/Job call ordering.
Both new Python files parse by AST only. Lifecycle comparison finds no removed
function, 29 unchanged function/method ASTs and exactly 11 changed/added ones:
config, open, records, allocate, reserve_run, join_current_worker, commit_retired,
plan_reclamation, begin_reclamation, reclaim_step and status. Schema/session
constants are the other relevant changes. Exact orderly closure, startup,
clock and transaction implementation remain inherited.

Unchanged dependencies remain reclaimer19713fc4 and composer40436584.
The session adapter pins actual existing supervisor6ea16154 and Jobbdd2cbc2;
it subclasses the Job at its existing attach/close seam rather than copying
the launcher or changing its containment/cleanup implementation. These two new
modules are not a standalone installation and need exact adopted loading.

## Review finding resolved before execution

The first draft opened a manager through inherited automatic recovery before
checking the launch/session. That could rewrite a newer LIVE/RESERVED/CLOSING
record to UNKNOWN and replace its failure field before stale-session refusal.
This was reported directly to author/root, and is fixed in the hashes above.

Final open validates the stored enrollment first. The internal `_launch` path
then validates the full exact original session under the acquired owner lock
and bypasses automatic UNKNOWN rewriting entirely. Only the later matching
current-handle transaction changes unresolved records. Ordinary owner reopen
retains its existing conservative UNKNOWN behavior, after enrollment validation.
Thus stale live-capability attempts do not rewrite newer logical records first.
SQLite open/profile operations remain ordinary storage operations; this is not
a claim of byte-for-byte read-only failure under crash-journal recovery.

The review also identified the base Job constructor's dynamic `self.close()`
call on limit-setting failure. The subclass initializes inert state before
calling the base constructor; partial/no-child construction cannot mint recovery.

## Why this is a live authority join

1. Before Popen, an idle fresh-schema manager durably reserves a bounded session
   containing monotonic session number, fresh nonce, selected worker/profile and
   command digests, original finite limits/deadlines and exact enrollment. Root,
   epoch, config/marker hashes and six filesystem identities bind the manager,
   marker, registry, lock and two slot directories. Ambiguous reservation or
   failed owner close prevents launch.
2. One scoped Job creation and one attach/resume attempt are allowed. Before
   unchanged AssignProcessToJobObject/NtResumeProcess, the parent retains the
   exact Popen object/HANDLE, reads its kernel PID and creation FILETIME, and
   durably binds that pair to the current reserved session. Failed/uncertain
   binding cannot arm resume.
3. The worker must read its own current kernel identity and match that pair,
   original profile/session and enrollment before joining. A copied nonce or
   digest alone cannot join another live process. Allocation and every run
   reservation require the current exact join; run reservation stamps session,
   worker, slot, generation, sequence and cumulative run before run-path/actor
   creation. Run deadline cannot exceed the original session deadline.
4. Before recovery, `close()` seals further attach/resume. It retains original
   Job and direct-process handles, compares their identity, requires an actual
   signaled zero-time kernel wait plus successful exact Popen wait, and queries
   fresh Job accounting with active processes zero. A cached returncode alone
   is insufficient. These observations execute again inside the owner-locked
   registry transaction before any quiescence write, while the Job remains open.
5. Full current session equality is checked on recovery open; the transaction
   rechecks stable binding/state/worker and exact current run joins. Different
   unresolved runs refuse. Genuine CLOSED records are preserved. Only matching
   RESERVED/LIVE/CLOSING/UNKNOWN records become QUIESCED_UNCLEAN, without an
   orderly closure digest. Phase, failure/retirement intent, generation, all
   run charges and original horizons remain unchanged. Session and record
   updates commit together; uncertainty poisons the owner and is not retried.

The internal launch/observation closures are nonserialized same-process objects
created by this scoped path. No report JSON, caller closure boolean, PID-only
lookup, absent port or released lock is an accepted recovery source. There is
no public deserialize-closure method. Python-private issuers are not advertised
as security against malicious code in the same interpreter.

## Finite authority and retained boundaries

The registry contains exactly one meta row/current session and two occupied
slot records, not a growing event history. Session count is monotonic and capped
by original `max_sessions` in 1..4096. Session bytes are capped at 16384. Each
session launch and recovery attempt are one-shot; there is no retry or refund.

Original manager authority must cover the main finite wall allowance plus a
preallocated 25..60-second cleanup margin, and retain at least ten CPU seconds
for two fixed five-CPU-second registry owners. Binding/recovery each have two
calls, original persisted deadlines and five CPU seconds. The original frozen
supervisor still supplies process/Job limits, direct wait up to ten seconds and
Job settlement up to ten seconds. These software checks are sampled, not hard
wall bounds around blocking calls; root's outer finite allocation must cover
the whole selected action. This is fresh explicitly bounded registry authority,
not renewed service authority or a reset of crashed-run accounting.

QUIESCED_UNCLEAN is deliberately excluded from service reserve/restart. It may
only satisfy the process-quiescence part of later retirement. A fresh adopted
conservative clock must still satisfy the original retention horizon, and the
unchanged fixed-layout reclaimer still requires exact marker/inventory/identity,
private ownership, prepaid window and original call/apparent-byte limits.
Supervision itself deletes nothing and does not adopt potentially damaged
SQLite/service contents. Existing roots cannot migrate into the new schema.

Supervisor loss remains held: its unnamed live capability is not reconstructible
from saved pair/session/report bytes. The pre-assignment suspended-process orphan
gap is explicitly unchanged. No keeper, named Job, duplicate handle or atomic
launcher is added. Physical envelope, unknown storage recovery and full v5 remain
unqualified.

## Important assumptions and disposition

The profile digest is a root-selected trusted worker/source-map commitment,
not automatic authentication of arbitrary argv. Root must actually load the
pinned operator/Job and selected worker without monkeypatches. Correct Windows
containment/accounting, private nonrolled-back registry, no external writers or
restores and no out-of-Job launchers are required. Source-file hashes alone do
not prove an arbitrary in-memory module object is authentic. PID/creation time
is a current live-launch join here, not global cryptographic identity or later
closure evidence after the supervisor dies.

No remaining concrete source blocker found under that scope. Exact negative
controls, root's genuine small process-tree adapter, selector and actual outcome
still require separate review/adoption. No fake Job/process success may qualify
the live-handle gate; no prior lifecycle/reclamation suite needs rerunning.
