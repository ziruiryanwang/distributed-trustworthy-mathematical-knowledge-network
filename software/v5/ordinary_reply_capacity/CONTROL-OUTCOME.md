# Saved reply-capacity controls: PASS within the selected scope

2026-10-28. Independent read-only review of
`experiments/v5-local-checks/reply-capacity-controls01`. No test, service, native
operation, assembly or protected-state access was performed during this audit.

The saved controller reports `PASS_REPLY_CAPACITY_CONTROLS`, all seven selected
groups, closed scratch custody and `mathematical_acceptance=false`. Its stdout
matches `controls/RESULT.json` exactly apart from the terminal newline. The outer
runner reports exit 0, reaped child, closed Job, zero active processes, no cleanup
errors or requested termination, and empty stderr. There is no remaining runtime.

## Exact evidence

| Saved artifact | SHA-256 |
|---|---|
| `selection.json` | `6e4514665cf7f22bf50536b563b5220af0cb9813a406c31b0228b00c8ce94c9c` |
| Outer `RESULT.json` | `4ecfc65c8e49e5836ef5b45091375244cec3d269a5211de9461615eb390c2b2e` |
| `controls/RESULT.json` | `730f6f3fb364716012d547014b4eddb974862955266e0bb49e90ab03cc52d405` |

The outer selection hash matches the actual selected bytes. All three captured
source snapshots and their live source files match selection: controls
`b9ee3e5e...`, provider `929fbf45...`, runner `44a7bf1b...`. All fourteen recorded
support-source pins were independently rehashed and match. The exact retained
26,650-byte evidence fixture still hashes to
`bf13287aed53c34ccf58798d3e77ab0df1b60f74ed780641de88a9dc7fd813bd`.
The selected unchanged package PROFILE is `21bcb169...`; this is a candidate
provider loaded with that support, not a newly assembled package result.

The reviewed source records a case only after its assertions; the saved seven
case names match the selected plan:

- Oversized client maxima still return the complete real locator and evidence.
- An object larger than the remainder refuses before its BLOB is materialized.
- Missing evidence and an invalid Boolean original cap refuse.
- Exact exhaustion permits no additional successful response body.
- A held write retains its reservation; the remainder is usable after release.
- Cancellation preserves the charged body bytes and releases the reservation.
- Exact preview and discovery-offer quotas retain their prior behavior.

These exercised real parsing, dispatch/codecs and fresh scratch SQLite custody
with controlled writers. No socket, remote host, native theorem check or existing
owner database was used. They validate the changed accounting path and selected
unchanged routes, not every transport failure or a worldwide service guarantee.

## Accounting and disposition

The external allowance was 60 wall seconds, 20 CPU seconds, 512 MiB, one active
process and 1 MiB per log. Saved outer wall time is 0.6707872 seconds; the child
Job used 0.359375 CPU seconds and the outer runner 0.078125 CPU seconds, totaling
**0.4375 known CPU seconds**. The inner controller's 0.171875 CPU seconds is
already inside the Job and is not added again. Peak recorded private commit was
25,788,416 bytes. Stdout was 4,358 bytes and stderr zero. `total_processes=2` is
cumulative; the final active count is zero and is not a concurrent count of two.

The selected controls pass and provide the required narrow evidence for root to
consider file-only integration. They do not adopt a package, change earlier failed
inspection outcomes, qualify native compatibility or establish mathematical growth.
No retry or additional proof/service experiment is needed for this control boundary.
