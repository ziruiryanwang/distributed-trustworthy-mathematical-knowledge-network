# Installed adaptive boundary 01: retained failure audit

Disposition: **FAILED selected installed action; preserve partial observations,
do not relabel the run as passing.** Reviewed by `core_release`, 2026-10-20,
after root announced session 99488 terminal. No runtime was polled, restarted
or launched by this audit. No installation or used evidence was modified.

## Exact evidence

All paths below are relative to
`product-local/v5-distribution-adaptive-01`, except the source path stated later.
The installation remains the exact adaptive release
`ad2e3ba04a2e12b6076fbf1d6be9fe068c35ae71970a5dee1eedb4188781e193`.

| Artifact | SHA-256 |
|---|---|
| `adaptive-integration-inputs/installed-adaptive-boundary-01-request.json` | `4ae6c38882bed8e5fb998d8abcea0975247d7c345324371b4e23199faf9ff27e` |
| Original staged and snapshotted `installed.py` | `31b60feabef96c033bffdc0828a18c36cafd2bc02033c071571e62c316abb937` |
| `adaptive-integration-operations/installed-adaptive-boundary-01/plan.json` | `40685455f5f4bbc9adb9e99427c925a7d4cb2702444a64849482cc3387bb7a59` |
| Same run's `RESULT.json` | `5403fe87204a4446d4512fdd8ad933d6f3d8a968de9120039d67d6e3348e36c3` |
| Same run's `work/adaptive-installed-result.json` | `ac2e42056c79bcc04e547454f439d55b9d3484de23a711b1c87b3c0029ed2c05` |
| Same run's `command/stderr.txt` | `b77733c646494fc7a59030e7b50349f489b9c410c79d38392ce2674ec9062fee` |
| `adaptive-integration-trust/ADOPTION.json` | `ea6851ff18ef02a205f22d77564be7e667c42ca96b35f861a098f618dbdd1c2a` |
| `adaptive-integration-trust/WITHDRAWN` | `d8e6e55c7ff8ac9f4221102c18357c9cf0164b8b21b8683e797dcc64746172df` |

Independent byte-length/hash checks of all 112 plan-bound originals and all
112 saved source snapshots found zero mismatches. These are the 111 selected
SDK entries and one owner adapter. Large runtime payloads were not rehashed.

## Actual failure and its source-level cause

The adapter reports `FAILED`, stage `cleanup`, with no primary operation error.
Its sole cleanup error is component `channel`, `ValueError: NONCANONICAL_JSON`.
The enclosing launcher reports `COMMAND_FAILED`, owner exit 1, and
`CLIENT_OWNER_NONZERO_OR_INVALID_RESULT`. The Node location child itself exited
zero; the launcher failure must not be confused with a child-process failure.

The snapshotted adapter's `_closed_channel` applies `F.strict(line, 65536)` to
the terminal stderr diagnostic. The selected `formal_features.strict` requires
byte equality to compact, sorted-key JSON. The selected
`node_entry_services.mjs` emits an ordinary `JSON.stringify` object beginning
with `status`, then `sequence`, then `descriptor_unavailable`. That order cannot
equal the sorted-key encoding, so this producer/parser mismatch explains the
reported refusal without a speculative environmental cause. The application
wire or mathematical acceptance policy need not change to repair this
test-adapter diagnostic handling.

Crucially, the adapter did not save the 862 raw Node stderr bytes before parsing.
The enclosing command stderr contains the launcher traceback, not those bytes.
`isolated_child` is absent from the saved adapter report. Consequently the actual
terminal transport counters cannot be independently recovered from this run.
Configured isolation and zero recorded route events are not substitutes for the
missing observed terminal-counter check. A separately reviewed successor should
retain bounded raw evidence before parsing; this failure remains unchanged.

## Partial observations supported by the retained report

- A fresh explicit temporary trust domain was created. All five changed source
  origins/pins passed their actual launcher/runtime/original-issuer checks, and
  the located helper registered in the original client. Runtime Python source
  count is 90; it is distinct from the full SDK-map count of 111.
- Both distinct formal queries completed their selected no-contact API path,
  using the same original child PID 23204, command sequences 1 and 2, one start
  task, one grant/budget/channel and original owner tuple. These identity claims
  are the actual assertions and report of the exact reviewed adapter, not an
  independent external process monitor.
- Query digests are `dcd440c9ba112400ab6da48441af26aada05304d7f3a5553896d0633776de84b`
  and `09c88d7320d420c8a1ca78b80fe3c2cd0b53a837dac245f343b501e87fe125ed`.
  Both generations are `RETIRED_NO_CONTACTS`, with zero contacts, descriptor
  requests and pending requests. Both route terminations are
  `INCOMPLETE_ABORTED_OR_FAILED`, with
  `TimeoutError: The operation was aborted due to timeout`. All recorded route
  events are zero. **This is not successful exhaustive routing or discovery.**
- There is exactly one envelope prepayment: six requests and 4096 reply-capacity
  bytes. Both full query slices remain charged, with no pending acquisition.
  Three client calls are recorded. Admission, authoring, import-session,
  publication, store and same-live-hit counters are zero; all three actual
  issuer attempt counts are zero. Preparation and HTTP/search paths are absent.
  No mathematical acceptance, native work, proof work or publication occurred.
- The client closed as `CLOSED`, with empty failures, no cleanup uncertainty and
  all three issuers closed. Workspace and channel closure flags are true. The
  channel reports two commands, three reply frames, zero exit code, no channel
  failure and no forced termination. Pre/post role maps agree; both runtime
  census reports cover 5896 files and 130118221 bytes.
- The actual withdrawal marker is present and exactly matches the newly created
  adoption identity. The temporary domain is no longer a reusable live adoption.
  No earlier withdrawn test domain was reused.

## Enclosing closure and full charged cost

The Job closed with zero active processes, direct child reaped, no cleanup
errors, no termination request and no terminated processes. The Job recorded
three total processes. Failure was not caused by exceeding the selected
120 CPU-second / 240 wall-second / 512 MiB / four-process envelope.

Known CPU is **45.875 Job + 13.25 outer-wrapper = 59.125 seconds**.
Outer wall time is **71.7985881 seconds**. Bootstrap CPU 12.71875 and embedded
supervision CPU 0.34375 are not added again to the outer-wrapper total. Nested
command wall 71.63028639974073 is nonadditive. Pre-clock interpreter startup is
explicitly unmeasured, not zero. Peak Job private commit is 208764928 bytes;
observed output is 1370564 bytes in 142 entries. The failed cost remains charged.

## Decision consequence

The saved evidence narrows the outstanding problem to diagnostic interpretation
and retention in this integration adapter; it does not justify a product
rebuild or replay of mathematical/proof campaigns. Any successor is a new exact
source/request with fresh state and separately selected runtime authority.
This audit authorizes no retry. Until the required terminal observation succeeds,
the selected installed gate remains failed. Even a later passing no-provider
boundary would not establish useful remote discovery, mathematical reuse,
growth, public readiness or completion of v5.
