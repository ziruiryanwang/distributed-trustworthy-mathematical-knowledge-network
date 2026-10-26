# Independent intake progress source review

Disposition: **PASS_SOURCE_AND_FOCUSED_CONTROL_PLAN**. The reviewed source is
appropriate for one separately selected focused control run. No control,
product import, owner call, database opening, native operation or selector was
executed by this reviewer. This is not an actual-test pass, a diagnosis of the
interrupted intake, mathematical acceptance, or final-v5 acceptance.

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Checkpoint: `research/cycles/v5-2026-10-26-local-discovery/CHECKPOINT.md`.
Root owns execution, integration, adoption and Git. The prior recovery result
remains separately recorded in `../ordinary_parse_reuse/RECOVERY-OUTCOME.md`.

## Exact reviewed bytes

| File in this directory | Bytes | SHA-256 |
|---|---:|---|
| `baseline_intake.py` | 22,887 | `49b6f8f1e1f1cb55526b0f8787414e05619af3d19a28e65ad5372186a5171ca2` |
| `controls.py` | 28,252 | `9a838fcb08f6ac614a583d342cbc69897cd2f63733d314d171cf83ec524945e9` |
| `DESIGN.md` | 7,924 | `d7d41aa280199d28a4cc33d1e7bfa661f0f338c7bd5f23089db649631b544b86` |
| `TEST-PLAN.md` | 8,402 | `f4ebd4d0ca105c113c5c758e03c0b875040107eeeffebe3d80cb7912da797a34` |
| `CONTRACT.md` | 4,307 | `28c0e80d2fcf8f0f04847af4e1fc35ed517b38010e443ecfe0ba66deffc552df` |

The exact predecessor is the adopted package's
`reference/baseline_intake.py`, 17,024 bytes, SHA-256
`9b243232603206b3a0925f639a0b8b1a6cbf0de8ca093ad4aa3642c595ff1142`.
The reviewer read the complete successor and controls and checked the final
changed sections after author revisions. The six dependency pins in controls
were independently recomputed from the retained package and match. The real
bundle Limits source was read: callers may lower its maximum 64 batches but
cannot enlarge it. The real ordinary-path and exclusive/fsync writer helpers
were inspected without importing them.

## Acceptance and failure reasoning

The new `_Progress` object has no readback or authority path. Its records do
not feed admission, catalog context selection, recovery or resumption. They
contain scalar observations, not proof trees or arbitrary exception text.
The selected-root spelling precedes validation; the validated/confirmed fields
remain empty until the actual context validator returns. The added final
`progress_directory` is a location convenience, not a protected context.

Diagnostic writes use the existing ordinary path checks and
`PortableCatalog._write_fresh`: exclusive file creation, flush and fsync.
Invocation-token collision refuses rather than reusing an attempt. Sequence
and byte reservations advance before fallible I/O, preserving a partial file
and preventing a subsequent FAILED record from reusing its name. This uses
the existing cooperative, serialized owner and immutable-support assumptions;
it does not introduce a hostile concurrent-filesystem guarantee.

For n successful batches, the count is 8n+3: two planning and six actual
events per batch, plus ENTRY, METADATA_COMPLETE and COMPLETE. At n=64 this is
515. The 516-record ceiling accommodates a further terminal attempt. Each
record is at most 2,048 bytes; the maximum attempted payload reservation is
1,056,768 bytes. The same invocation budget is checked around writes, and
planning includes this reservation alongside the unchanged call-spool reserve.
The no-sink private planner retains its previous result and side-effect shape.
These are per-invocation limits, not a global retention policy or disk quota.

ADMIT_INTENT logging precedes `entered=True` and the actual admission call.
A diagnostic failure there cannot start a new admission. After a valid live
return, the existing confirmed root, uncertainty state and observation list
are updated before BATCH_CONFIRMED logging. A logging exception cannot erase
that known returned prefix. The existing finally block still records observed
worker CPU even when the following diagnostic fails. If admission raises, its
original exception and possible-unreported-commit state survive; a secondary
FAILED logging error is contained and cannot replace the original exception.

An ADMIT_INTENT record's false uncertainty value describes the moment before
entry. It cannot establish that no later admission occurred. Likewise, a
recorded prefix is not a recovery cursor. Abrupt death can occur between any
commit and its diagnostic record; protected status/context is still necessary.
Budget exhaustion and non-Exception termination can prevent terminal records.

Worker CPU is deliberately partial. BATCH_CONFIRMED precedes the existing
finally-block addition for its own batch, so it can lag that returned work.
Subsequent/terminal records include the addition when reachable. DESIGN and
controls explicitly bind this timing. Neither missing records nor zero partial
counters establish total cost, clean closure, elapsed-to-death or a cause.

## Focused controls assessment

The controls compare actual predecessor/successor intake loops using tiny,
explicit manifest/admission/custody/catalog/native doubles. Real evidence
encoding, path validation and exclusive/fsync writes are exercised. No real
database or mathematical acceptance is needed to test the changed boundary.
The five helper modules and predecessor are pinned; the successor must be
fixed by root's source snapshot. The controlled paths forbid subprocess,
SQLite connection and socket creation, and both real catalog open methods.
This is a regression-harness boundary, not an operating-system sandbox claim.

The seven groups cover unchanged call sequence/count/bytes and old report
fields; no-sink planning; exact scalar schema/event order and per-record
batch/confirmed-prefix/validation/manifest values; all three diagnostic
bounds and combined spool capacity; fresh/ordinary/collision paths; injected
fsync failure with retained bytes; constructor and before-admit failures;
post-return and COMPLETE logging failures; and preservation of an original
admission exception when terminal logging also fails. The 64-batch fixture
uses REUSED doubles to respect the unchanged native spool cap. Direct private
counter/encoder manipulation tests guards, not hostile-input resilience.

Fixed intake clocks make predecessor comparison exact without making timing
claims; the harness and outer runner retain real clocks. The prospective
60-wall/45-Job-CPU-second, 512-MiB, one-process envelope and fresh output are
sufficiently bounded for this control scope. No old parser/kernel/transport
campaign needs repeating.

During pre-execution review, two deterministic test mismatches were returned
to the control author: the diagnostic worker-accounting label and comparisons
that did not exclude the approved additive progress_directory field. Both are
corrected in the exact controls above. No failed runtime was consumed to find
them. No unresolved source blocker remains within this selected scope.

## Next decision boundary

Root may select these exact controls once, pinning the existing runner,
successor, harness, plan/contract/review, six retained package inputs and the
specified Python runtime. Actual success must include the seven expected
groups, no forbidden calls, explicit synthetic-authority label and
mathematical_acceptance=false, together with clean outer closure.

Auxiliary packaging is reviewed separately in PACKAGE-REVIEW.md. A passing
control run does not select a new intake, enlarge an allowance, resume the
interrupted attempt or authorize diagnostic records as mathematical warrants.
