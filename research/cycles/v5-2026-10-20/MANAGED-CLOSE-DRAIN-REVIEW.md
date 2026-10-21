# Cooperative monitor drain: independent changed-boundary review

2026-10-21, support_screen. **PASS SOURCE ONLY** for the exact successor below.
No blocking source defect found in the four authorized changes. This is not a
test/build/installed-operation result, actual01 causal attribution, or full-v5
acceptance. Root retains selection and adoption authority.

## Pins and scope

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
The resumed workspace guard passed. Source and data-only fixture inspection,
hashing, exact text comparison and this checkpoint were the only actions; no
imports, tests, builds, database access, credentials, Git or product edits.

| File relative to canonical root | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/managed_close_drain/client/serve_placement.py` | 24566 | `c815331f035618b36f504d604a1fb75d8682439f0488453c72e9801a63d78bd8` |
| `software/v5/retained_advertisement/client/serve_placement.py` | 22670 | `7e735337d595894e25fd07a8dcc9ad8cd3ba9f1c042ba930684b7798232cb7fa` |
| `research/cycles/v5-2026-10-20/MANAGED-CLOSE-DRAIN-SOURCE.md` | 6553 | `fd7129f819fd7989cac3c57a3ddc641571016f659ee6442b7d217c431cefafd1` |

The final source supersedes unused intermediate039c96ff. I read the complete
final source and author note. Independently removing exactly the four approved
edits reconstructs the entire selected predecessor text exactly, including EOF:
`ExactPredecessorReconstruction=true`. There is no additional source delta.
The prior reachable-defect argument remains in
`MANAGED-CLOSE-CANCELLATION-REVIEW.md`, SHA-256
`acd6812ca7e9cd2fcb80aaf43d7d21194b86da39713da74284160201fb9af04a`;
it is not repeated here.

## Four changes reviewed

1. **Activity cap (lines79-90).** The additional cap is
   `active_end <= stop - drain - 2*operation - 1`. It preserves one intake drain
   before stop even when the independent locator deadline is the tighter bound.
   It only shortens activity; outer/locator deadlines, the original outer
   reserve, command counts and resource limits do not grow.
2. **Constructed grant check (118-121).** `grant.deadline <= active_end` is required
   immediately after `start_service`. This is necessary because the grant samples
   a later clock than the preceding floor operation. The selected controller
   (`software/v5/selective_placement/placement/controller.py`, map-resolved and
   hash-verified `ef1c9b59072127379e955bafeea001a22d6e3d10c9c46dca1304f85ab09e2b49`)
   creates that deadline at26, charges the run at112 and revokes its service in
   `close` at315-318. Therefore a failed new margin check takes the existing
   partial-construction cleanup before listeners/provider/journal creation;
   it neither rolls back the charge nor grants a longer interval.
3. **Monitor quiescence (270-300).** Close first sets closing/wake, joins the
   tracked monitor under shield, and only then proceeds to intake, grant revoke,
   locator stop and the existing teardown. The join cutoff is
   `min(original D, close-time + o, original S)`. It does not change the already
   running health command's earlier absolute cutoff. A wake-waiting monitor exits;
   an in-flight health call can complete its one reply and post-reply guards,
   then exits at the next loop condition. No extra monitor or command is created.
   A cancelled/error monitor or missed cutoff adds `_monitor_task` uncertainty.
   A genuine health error caught by `_monitor` still leaves the original failure
   code. Fallback cancellation uses `asyncio.wait` capped at one second and O;
   it need not wait indefinitely for cancellation acknowledgement. Its error
   record remains even if the task subsequently finishes. Startup retains its
   original separate cancellation policy and one-second bounded gather; this
   review does not claim new startup-resistance guarantees.
4. **Store-idle guard (357-368).** Both monitor and startup must be absent or done
   in addition to every predecessor intake/retained/read/busy predicate. A task
   surviving attempted cancellation prevents advertisement/controller/workspace
   close and records `live_actor_prevents_store_close`. The service cannot report
   orderly closure by closing stores underneath that task.

The controller's frame-failure behavior is unchanged. So are exact STOPPED,
returncode, channel_failed, forced_termination, all seven cleanup flags, the
original outer-deadline check and the final `_failure is None` requirement.
Shielding does not discard task ownership; the same tracked monitor and close
tasks remain reachable. Failure fallback is not converted into successful CLOSED.

## Reservation arithmetic and current fixture

Let D be the actual grant deadline, S the locator stop cutoff, O the service
outer cutoff, d each provider drain, o one locator operation, and c locator
cleanup. The new construction check makes the author's needed premise explicit:

`D <= active_end <= S - d - 2*o - 1`

`O - D >= 2*d + 2*o + c + 5`.

For a successfully started service and close begun by D, a conservative bound of
one monitor operation, one intake drain and one stop operation fits by S-1.
The outer reserve also retains locator cleanup, read drain and final margin.
The actual join is no later than D, so this is conservative, not an extension.
Fallbacks remain failed and bounded by their original later-stage cutoffs.
These inequalities assume cooperative scheduling/bounded underlying calls;
they do not promise hard-real-time execution or successful close begun too late.
Existing deadline checks and whole-process containment still matter.

I independently checked the data-only fixture's read5000ms/locator10000ms values
and the public02 source's intake30000ms override. Fixture file
`experiments/v5-local-checks/bounded-reclamation-service-01/bounded-reclamation-service-result.json`
is53427B, SHA-256
`21ee791482d385521467673ad67630f7f6626ceb840c7adaf6ea61b7ce263a5b`.
`managed_observed/client/managed_owner.py` passes locator deadline O-7.
Thus d=35, o=10, c=6, and:

| Quantity | Seconds relative to O |
|---|---:|
| Original outer reserve | 101 |
| S = min(O-7, O-6-35-2) | O-43 |
| Old stop-based activity cap S-2o | O-63 |
| New stop-based activity cap S-d-2o-1 | O-99 |
| Unchanged outer-based activity cap | O-101 |

Both versions therefore choose `min(now+120, O-101)` for this fixture: the repair
does not further shorten its proposed activity window. This arithmetic does not
predict startup cost or guarantee the owner's later60-second service check;
those existing finite guards still decide the actual run.

## Remaining gate and limits

Proceed only through root's separate selection of the deterministic changed-
boundary controls: real monitor/close/health/controller methods, explicitly
synthetic framed I/O, healthy held reply and strict failing/expiry behavior,
plus a live-actor store-close refusal. Construction drift/margin refusal should
be included without executing an old campaign. Passing such controls would not
be actual Node/network or installed contribution evidence.

Contribution01 remains failed with its actual close cause unknown. No source,
grant, charge, failed result or old installation was rewritten. This review
qualifies the narrow repair source for the next controlled gate, not the final
deployable v5 objective.
