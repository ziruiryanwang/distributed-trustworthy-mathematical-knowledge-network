# Placement close: smallest safe successor decision

2026-10-21, core_release. Source-only proposal; no product edit, runtime,
retry or changed used bytes. Canonical root is the Trustworthy project.

## Diagnosis

Selected base locator `4dc0824d` gives process teardown six seconds, then its
`finally` performs the complete synchronous runtime verification. Selected
service-locator `eeb82d5d` additionally verifies role files. Service `07c60c4f`
wraps **all** of that in `cleanup_seconds + 1` (seven seconds), conflating two
different operations. Retained integration01 reports Node closed/returncode0,
no forced termination/channel failure, and full5896-file postverification
lasting8.0636878 seconds, yet service `location_close` is uncertain. Increasing
the native six-second teardown or skipping file verification is not warranted.

## Recommended exact fresh change

Keep Node/controller/role-verifier code and all source/runtime pins unchanged.
Make only a fresh service successor, leaving used `07c60c4f` frozen. Define:

- `D`: existing drain allowance, max(read/intake operation interval)+5 seconds.
- `O`: existing locator operation interval.
- `C`: unchanged native teardown allowance (six seconds).
- `T`: original pinned service outer deadline.

Change the startup reserve from `D + 2*O + C + 5` to
**`2*D + 2*O + C + 5`**: intake and read-provider shutdown each have a drain.
Retain the other minima and authority checks. This can shorten active service;
it never extends any original authority or whole-process budget.

Replace the seven-second wrapper on `location.close()` with a fixed cutoff
**`T - D - 2`**. Use its original remaining interval with the existing bounded
helper; do not mint a new deadline relative to the time close happens. Check
the same cutoff explicitly after the await before accepting location closure,
as synchronous verification cannot be preempted by an asyncio timer. Preserve
the following read drain, final outer-deadline refusal and all existing clean
closure conditions. If no positive interval remains, report uncertain cleanup.

At the latest active end selected by the revised reserve, after a full intake
drain, one stop operation and native teardown, at least `O + 3` seconds remain
for exact final validation before that cutoff. Earlier close may use more of
the **already authorized** original remainder. This is explicit allocation,
not a theorem that filesystem verification finishes in that duration. The
original external Job remains the hard CPU/process/wall containment; no claim
of hard synchronous-I/O preemption follows from an asyncio timeout.

The change needs no new public limit field, async worker pool, cached validation,
runtime weakening or distribution copy. Do not substitute a guessed longer
constant such as15 seconds: full validation and native teardown have different
bounds and should be composed against the original operation envelope.

## Separate adapter02 corrections (root owns)

Integration01's source HTTP aggregate reply allowance8MiB cannot admit the
frozen group route's16MiB reservation, irrespective of the actual tiny opening.
Give the fresh adapter enough **explicit aggregate** reply allowance for its
selected route sequence; leave route maxima and product reservation logic
unchanged. This is a fixture configuration repair, not a new product cap.

Preserve the first exception as `primary_error` using the existing closed
`error_fields` projection. The final orchestration error must not overwrite it.
Capture source-provider counters/status in failure cleanup as well as success;
retain the independently labeled cleanup errors and client uncertainty when
available. Do not log raw exceptions, request bodies or bearer tokens.

One fresh reviewed integration can discriminate these changes under the same
outer150CPU/300wall/512MiB/six-process allocation. Existing ten controls and
failed integration01 remain preserved; do not repeat their passing boundaries
or claim failed01 had successful placement. Root selects any implementation
and later execution separately after independent review of this proposal.
