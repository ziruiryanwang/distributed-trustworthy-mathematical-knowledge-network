# Public refresh workflow 01: failed scenario, preserved partial evidence

2026-10-28. Independent saved-artifact audit by `growth_design_audit`.

**The full two-cycle public workflow failed.** Its first refresh command and
first contact read succeeded; the refreshed service then closed normally. The
following contact read raised `UnsettledTransportError` with
`FAIR_CONNECT_CLOSURE_UNOBSERVED`. The second cycle never began. This is not a
passing replacement workflow and must not be relabeled as one.

The audit read saved sources, configuration, results, logs and supervision
records, and rehashed selected files. It performed no product execution, socket
operation, source repair, Lean operation, owner/database access or Git mutation.
Transport diagnosis and any fresh successor are separate assignments.

## Evidence identity

All run-relative paths below are under
`experiments/v5-local-checks/registration-refresh-public01`.

| Artifact | SHA-256 |
|---|---|
| `selection.json` | `c777a623b19ea73f772085300daadf86997bd223389a17947af3ad8763350445` |
| outer `RESULT.json` | `c54e17f1c79d6bfde709293ca32a09e360560de32ffc7a5d126cc8e3f18805e9` |
| `suite/RESULT.json` | `91c11d1217b242cdc670fedc254054ced092837eac3abceaf7fd5110af86df94` |
| saved `public_workflow.py` | `b909464655b479b22bc106177dd889af82fbc7240641a40fb35972654081ec46` |
| first refresh config | `df18d99e4b9bc57bd4e4d4016a13796428bfc13c41c48e1ba6dc18432fca43a7` |
| first feed config | `4cc96e5d17172c87dbe5b15bab1048ca47585568c2122b5d444ff9dd39fac628` |
| first refresh public `RESULT.json` | `8ba105ccdb83630d4e418446080b7f46b6aa9ade7896d89433b64ff721360258` |
| first refresh `SUPERVISION.json` | `e2adb2c2f3856d3a3baf9dbeef7c1e68542313ace560aaa4cda78f2a14236bf5` |
| first refresh launcher `RUN.json` | `6002481479cc978b0713adf6c0cc481b45bbc224158343eb35c86b6214b4a7ed` |

All four saved source snapshots and all eight runtime/assembly/package pins
match the selection. The retained helper is `98f3eb0b...`; the real saved
HashMap query is `eec3a939...`. The selected package is
`registration-refresh-assembly01/distribution/package`, with PROFILE
`f75dda6e534450cdf5d4db2901c3e1964501514da817bc3eb8aadebc0c350f7b`
and assembly receipt `a604c0ec...`. The earlier assembly/control audit remains
the package-closure evidence; this audit does not repeat its whole payload scan.
Explicit runtime pins do not establish a hermetic toolchain.

Installation `9112bc5d...`, mathematical implementation `86b6fcce...` and
semantic ID `9108f44d...` agree across the relevant saved records.

## What actually succeeded

The public feed at `127.0.0.1:52837` offered A (`127.0.0.1:52832`) and C
(`127.0.0.1:52834`). Registrar scope permitted A and B (`127.0.0.1:52833`),
while its egress policy permitted all three. Thus the saved configuration
distinguishes scope rejection of C from egress rejection.

The public refresh command produced a READY directory at
`127.0.0.1:52841`. Its saved terminal result reports:

- One feed/route slot, two returned contacts, one adopted and one rejected;
  no truncation. `refresh_complete` is false.
- One fresh refresh request: 448 request bytes, 712 response-body bytes and
  225 header bytes. The complete prepaid ceiling of 32,768 reply bytes remains
  charged; it is not replaced by the smaller actual response.
- A closed network ledger, one charged request, zero pending requests and zero
  reserved reply bytes. The external prepayment names this operation once.
- One route and one contact, under the retained three-feature HashMap query.
  Namespace `d966de54...` agrees between query, READY, result and reader reply.
- Requested lease 30 seconds, but READY disclosed only 5,988 ms remaining and
  `LOCAL_MONOTONIC_ISSUANCE_CUTOFF`. The directory has a finite freshness horizon.

The first reader actually received HTTP 200 with exactly A, `truncated:false`,
`UNVERIFIED_SPECIALIST_REGISTRATION`, `global_complete:false` and
`mathematical_acceptance:false`. Its reply binds the saved request's namespace,
three features and nonce. The reader recorded 448 request bytes, 647 response
bytes, 225 header bytes and 0.0165162 seconds elapsed. The refresh provider's
served-request counters match these byte counts and one request.

The refresh public result is `INCOMPLETE_REFRESH_SERVICE_FINISHED`, with
`termination:FINITE_SERVICE_CLOSED`; its service reports `LEASE_FINISHED`,
quiescence, zero active handlers/reserved bytes and no failures or cleanup
errors. Its launcher records exit zero, child reaped, Job closed, no active
processes and no requested termination. Its total nested launcher wall time is
7.0313703 seconds, below the requested 30-second lease. These saved records
establish an actual finite natural close, although the runner never reached
the later code that copies its detailed readiness/closure timing into the
top-level cycle report.

These facts establish the first public policy-scoped refresh/read/close path.
They do not establish that the complete workflow's later assertions passed.

## Failure and unexecuted work

After the successful read, the runner awaited the refresh child's zero exit
and checked its finite close bound. Its next exchange was the planned
`after-first-cutoff` read. That exchange raised
`FAIR_CONNECT_CLOSURE_UNOBSERVED`; it did not return the required settled
`CONNECTION_REFUSED` result.

The source appends each reader-attempt row only after `await X.exchange(...)`
returns. Consequently the failed attempt has no saved per-attempt row, nonce,
timing or byte accounting. The top-level exception and control flow identify
the failure; no missing attempt details should be reconstructed as observed
facts. This audit makes no additional assertion about the transport cause.

Only `cycle-1` exists. Its top-level record contains the expected A endpoint,
but no completed feed/refresh summaries. The runner never reached the normal
first-feed wait, saved-result assertions, second feed, second refresh or second
positive read. In particular, this run does **not** establish same-origin A-to-B
replacement under byte-identical registrar configuration, disappearance of A
from the second reply, or a complete second refresh.

## Termination and accounting

The runner's `finally` kills each still-live direct child, waits up to three
seconds for it, and closes its observer listeners. The already completed refresh
was not killed. The twelve-second feed was still live when this failure path
ran; the whole scenario ended in about eleven seconds. Therefore its closure
was forced through runner cleanup, not an observed normal feed lease expiry.

The feed has READY and launch/command records, but no terminal public RESULT,
launcher RUN or SUPERVISION. Its initial LAUNCH record's
`NO_CHILD_LAUNCHED` value is provisional: the saved child READY proves the
operation did subsequently launch. Do not read that provisional value as a
terminal outcome. The runner did not record individual kill events/exit codes,
so no separate orderly feed close or complete feed accounting is claimed.

The runner reports two children reaped, zero cleanup errors, all observers
closed and zero learned-endpoint dials. The outer supervisor independently
records the failed runner reaped, Job closed, zero final active processes and
zero cleanup errors. There is no surviving process reported. Outer
`termination_requested:false` and `terminated_processes:0` describe the outer
supervisor/Job; they do not negate the runner's explicit child-kill path.

| Recorded resource | Value and scope |
|---|---|
| Outer Job CPU | 3.1875 seconds, includes runner and all descendants |
| Outer wrapper CPU | 0.15625 seconds, separate from the Job |
| Known inclusive run CPU | **3.34375 seconds** |
| Outer wall through report | **11.3264900 seconds** |
| Outer wall through cleanup | 11.2898422 seconds, overlapping the preceding wall measure |
| Outer peak Job private commitment | 124,522,496 bytes |
| Processes | 10 lifetime creations; final active count zero; the limit was 8 concurrent processes |
| Outer logs | stdout 2,127 bytes; stderr zero |
| Nested refresh Job / wrapper CPU | 1.0 / 0.140625 seconds, already inside the outer Job |
| Runner own CPU | 0.734375 seconds, already inside the outer Job |

The outer supervisor's 0.09375-second subcounter is already included in its
wrapper total. None of the nested measures is added again. All saved stderr
files are empty; that does not turn the explicitly reported failure into success.
The outer limits were 110 wall seconds, 60 Job CPU seconds, 1,024 MiB,
eight concurrent processes and 1 MiB per output stream. Closure did not require
an outer limit kill. These failed-run costs remain charged.

Together with the previously audited assembly, failed controls01 harness and
clean controls02, the known selected sequence consumed 7.453125 CPU seconds
and approximately 18.4036417 wall seconds. This excludes source work, review
and unmetered human/model effort; it is not a full development-cost claim.

## Decision

Preserve public01 unchanged as a **failed full scenario with useful partial
evidence**. Its first refresh wiring need not be disproved or its costs erased
because the later transport boundary failed. Equally, its partial successes
cannot satisfy the unexecuted replacement gate. Any repair/new run requires a
fresh source decision and bounded selection; this audit selects neither.

This is loopback contact maintenance only. No learned endpoint was contacted,
no mathematical artifact was acquired or checked, and no independent-host,
TLS deployment, endpoint availability, useful-growth or final-v5 claim follows.
