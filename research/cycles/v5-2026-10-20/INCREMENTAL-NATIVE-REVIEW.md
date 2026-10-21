# Independent source review: bounded native conditional-result reuse

2026-10-21, adaptive_audit. **GO for focused native-free controls.** No runtime,
native checking, installation, Git operation or old-suite rerun was performed.
This is not mathematical qualification or a full-cost growth result.

Reviewed successor: `software/v5/incremental_native/mixed_claims/receiver.py`,
27837 bytes, SHA-256
`5436569971c272b129fbaec480d51d57a1ec521d43fd4d4ad14133b786691d5b`.
Its exact predecessor is standalone receiver `835d5980` (24731 bytes).
Whole-file read-only diff and the surrounding existing receive/binding/parser
code delimit the change; no other product file is changed by this selection.

## Implemented conditional-result argument

The new `_native_memo` is private to one exact live receiver. Keys are complete
immutable canonical witness bytes. Python dictionary lookup resolves collisions
by bytes equality, rather than authorizing a hit from digest equality alone.
Each value contains exact receiver identity, profile, image/foundation/policy,
ordered actual parent journals, rank and actual native-returned journal.

Every call still parses its complete packet, verifies its current I/A frontiers,
reconstructs current topological parent availability and exact ranks, and checks
complete target closure. A hit requires the exact owner/binding tuple and then
checks the retained output journal's image/foundation/policy/summary/rank against
the current request. Its actual parents must be established in the current
graph. It does not retain old mathematical premise authority. These steps
implement the conditional-relation induction in NEXT-GROWTH-REVIEW `ef197b30`.

A miss executes the unchanged supervise/clean/input-readback/bind_native path.
Both hit and miss retain original pre/post loop owner/source/live-frontier
checks. The hit omits the worker-only floor-to-one-second feasibility check
because it launches no worker; ordinary original deadlines still apply through
the preserved live guards. No deadline or CPU cap is extended.

Pending records are local to the receive call. The memo is replaced only after
full graph/packet/final checks and handle allocation/registration. Any exception
reaches `_revoke`, which clears both old memo and live handles; local pending data
never becomes a lookup source on failure. A retained traceback is not authority.
No persisted report can seed this memo and a foreign receiver identity refuses.

## Bounds and lifecycle

The private `_retain_native` helper can only add to an inert pending dictionary;
it cannot install the result or create a handle. It counts actual witness lengths
and refuses insertion past the configured delta/witness bounds or hard 16-entry/
16-MiB ceilings. Duplicate/overflow retention leaves the count unchanged. Normal
parsing already constrains the same packet, but the helper has its own explicit
bound and can be tested with tiny caps without large allocation.

Each successful admission replaces the prior memo with only eligible records of
its current packet. Old unrelated entries disappear. Eviction or skipped
retention can only lead to later ordinary checking. Revocation/close clears the
memo. Lifetime counters remain observations of attempted work, not live authority.

## Evidence and accounting

Hits create no delta input, native command directory, stdout or process report.
They add `SAME_OWNER_REUSED_CONDITIONAL_CHECK_NO_EXECUTION` to the current RESULT;
misses add `NATIVE_EXECUTED_CONDITIONAL_CHECK` only after successful binding.
Both entries include exact witness size/hash and output journal. The enclosing
RESULT still says `SAVED_REPORT_NOT_TRANSFERABLE_PROOF`; it is saved before final
promotion and is not itself proof of a successful completed call.

The whole submitted packet is written and freshly read back in both routes.
Public descriptions/member export continue using the actual current live handle
and retained packet, not per-node private process files. The exact selected-SDK
dependency search is recorded in NEXT-GROWTH-REVIEW. No public dependency on
per-hit execution files was identified.

Full-graph worker/output reservations, attempts and submitted-byte charging are
unchanged. Actual worker accounting increments only on real supervised misses
(and separately on real claim verifications as before). New counters distinguish
native attempts from validated reuse observations; they may include a packet
that later fails and must not be interpreted as successful contributions.

The exact current114 source-map report-consumer search was also checked for
additive-schema compatibility. Both mixed client constructors use `dr` only by
indexing existing `attempts`/`live_handles` keys; other selected consumers index
existing profile/counter keys or embed the entire report. No exact-field-set
validation of this report was found. The four additive diagnostic fields do not
break these selected consumers. This is source compatibility, not a claim about
unselected external report parsers.

The small existing workloads do not establish a large total-cost benefit. Full
packet parsing/premise/guard costs remain and an optimized comparison library
gets this same memo. The feature is neither cold-owner ancestry elimination nor
permission for more work under unchanged reservation grants.

## Focused test scope and remaining assurance

Use valid inert packet structure with explicitly simulated native transcripts
through the real binding code; no simulated result is mathematical evidence.
Challenge exact hits, same-J changed bytes, current missing/invalid parents,
record identity/parent/rank/J fields, fresh/closed owners, most-recent replacement,
failed-prefix and final-check nonpromotion, small-cap retention, original charging
and honest absence of process files on hits. Actual filesystem readbacks and
original live guards can be retained without a native process.

Underlying checker correctness, source-to-Lean correspondence and receipt-system
soundness remain the same assumptions as the predecessor. Focused controls
exercise this new controller seam; any genuine native connection run requires a
separate decision and is not automatically warranted by the source change.
