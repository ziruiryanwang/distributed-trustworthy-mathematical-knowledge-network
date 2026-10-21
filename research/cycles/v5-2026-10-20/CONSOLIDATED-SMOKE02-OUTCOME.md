# Consolidated smoke02: independent actual outcome audit

2026-10-21, `support_guest`.

Disposition: **PASS_INSTALLED_RETAINED_PLACEMENT_RESTART_AND_GOAL_ONLY_EXACT_ACQUISITION**.
The one fresh smoke02 completed its selected installed close/reopen/discovery
boundary, including an actual stale-peer typed miss and clean closure. This is
same-host, loopback, structural-custody evidence, not mathematical acceptance,
independent-host/public-TLS qualification, lifecycle qualification or full v5.

## Exact evidence and source bindings

All run artifacts are under
`experiments/v5-local-checks/consolidated-restart-smoke-02`.

| Artifact | SHA-256 |
|---|---|
| `selection.json`, 41383 B | `04522d4b3fe8679c4d9a6af12c390b521f1ebe9135db6a2fdfe504776828d3ce` |
| Adjacent `consolidated-restart-smoke-02-input.json` | `1a98058329e4a2647d0b47503d5c4fd6a62e129fe6d4d75bbf425ce46d649c1c` |
| Outer `RESULT.json`, 2298 B | `3775b09f034480c5c77f5c76c900d006c5810026a309430152f6bf5189cbbda0` |
| Inner `consolidated-restart-smoke-result.json`, 124068 B | `f30b9188f2b6d8fbfa1de029399f225372318d552b4d9e0a97d18d08cc375803` |
| `installed-smoke-sources.json`, 39660 B | `7316742fa9dc2a89b384e45b6b4e189808d13a283f886a8b40a660b3664fd01f` |

The used smoke adapter is exactly reviewed `restart_smoke02.py`,
`a6e4dd616b614cb01181fa482f9340bd817098ea17453e0cd394bc403345912f`.
I independently rehashed all four selected source files in both canonical and
saved snapshot locations, every one of the 148 selected runtime pins, and the
saved 121-entry SDK map against the exact build-input and release maps. The
121 logical SDK files, 18 selected Python runtime files and two goal helpers
all match. All 88 recorded imported product origins resolve to selected SDK
files in the installation, not a development overlay. The source review is
`CONSOLIDATED-SMOKE02-REVIEW.md`,
`61dff73caafce5f6489f8ee0e4c8b77989653ce1de39b65903f45fd45770d29f`.

The unchanged installed candidate is
`product-local/v5-distribution-consolidated-01/Mathematical Commons v5`, release
`1fd0ae63faa84cc1f3ef82f17d2056657f8d6a3e5dea3686ace433987bd1e5be`,
build input `8ba3707236c1a6e01ab7f87886814f801034b2fe9144ad9603585adcc73feb33`.
The successful adapter performs its own pre/post installed/runtime/helper/input
checks. The selected Python pins are not the entire standard-library census or
a hermetic-toolchain proof. The existing Node wrappers report their separate
5896-file/130118221-byte pre/post runtime checks and equal five-role source maps
for all three concrete Nodes; this audit did not launch another runtime sweep.

Root reports two preparation refusals before this allocation: initial shell
execution policy prevented selector creation, then launcher argument shape
refused. A process-local Bypass invocation generated the sole fresh selection.
These are preparation failures, not extra smoke executions or erased failures.
The terminal selected execution is root session 40778, exit zero; no rerun was
performed for this audit.

## Placement, durable restart and preservation

The placement client made exactly one submit, with no uncertainty or client
cleanup error. B1 intake records one request and one completed action. The
original request is
`922b218614a3e596a2e84509dee128682066a4415b082bd4ff9e0cd3c32be9ac`.
The durable row is `RECEIPT_COMMITTED`, `recovery_used=false`. The saved original
manifest is byte-equal to the retained 1075-byte manifest, SHA-256
`14a4bfbb7bb4effe3c926776989a4b4b5fc85b9cec5a603c1f3b80809a785153`.
The unprojected 7352-byte committed outcome hashes to
`e7713b9165b773a190023f150dda561cac7a207ced4f1d337b358a30e3cef104`.
Independently applying the documented two-field public `observed` projection
to that durable outcome gives the exact saved response outcome. Its reservation
and request ID also match the durable row; the whole 5850-byte projected
response hashes to the reported
`4190b78ba870656f164daedb0032db40dbfda7f1d04db2b57856a9921314ac03`.
Local receipt diagnostics were neither removed from storage nor mistaken for
the public wire representation.

The source HTTP server was stopped, had no server/tasks, and its workspace was
closed before B1 sealing. B1 was `SEALED_SERVING`, run 1, with one request, one
grant, one cell, one route-run row and one route row. Its concrete service fully
closed before B2 was constructed. B2 reopens the same custodian workspace and
generation/configuration, same read endpoint `127.0.0.1:65353`, same intake
endpoint `127.0.0.1:65354` and journal cap, with all three create flags false.
Its locator/channel/state directory and Node port are fresh. The actual Node
identity changes from `12D3KooWJ8kKFdpE8DfGostLCQJiZ6idkzEKJSgXq4bAcfrAPCLt`
to `12D3KooWGC1UNV6xpP6mE9Dktsk1HgMm7BKABWJGnmipzTmQxAJc`.

B2 remains `SEALED_SERVING` and consumes the originally funded second run:
durable `runs=2`, original `max_runs=2`; its core and route run identity changes
from `c3c9e11e52ea93c0a17e1f70bd38406a6e4211b1b993bc44c28e1273c5b6efd8`
to `b2853e35ccd60b62433c05622ee9fa5b68800810482891570d3ddf28fe4ba180`.
The original generation wall-clock horizons and outer monotonic deadline
2238954.3000882 remain fixed. Per-run service cutoffs are separately constructed
by the unchanged service: B1 2238798.7653642 and B2 2238815.9250333. They are not
equal; both are checked against the original outer/retention horizons. No
generation horizon, run budget or outer allocation was extended.

The saved sealed/reopened/post-reader snapshots are equal. I independently
recomputed their tagged-row hashes and complete logical SQLite dumps from
read-only immutable connections after closure: request/grant/cell rows,
configuration/state/used totals, workspace, custody, packet store and index
all exactly match the pre-close baseline. The final core charges remain
placements 1, new_cells 1, index_calls 2, recovery_passes 1, requests 3,
reply_bytes 517519, storage_bytes 34138740, structural_bytes 17010880 and
wire_overhead_bytes 98304. These are cumulative authorization, not actual
physical occupancy or refunded work.

B2 advertises the original committed request, not a fresh placement. It records
`HINT_DISPATCHED_UNACKNOWLEDGED`, `add_provider_write=1`, and its new run ID.
Only the second run and current route row are added: original route metadata,
first run and first route hashes remain unchanged. I independently recomputed
the final route database hashes: one metadata row, two run rows, two route rows,
exactly equal to the saved restored-route snapshot. B2 intake remains at zero
requests/actions, corroborating no replacement submit.

## Goal-only acquisition and actual stale-peer coverage

Only after B1 closure, B2 readiness and retained re-advertisement does the
adapter create the fresh reader workspace and call the reviewed `discover`
function. Its arguments contain the closed goal and owner policy/cutoff, not
module/export/packet IDs, source bytes, manifest or selected custodian peer.
Fixture equality is checked outside that function after discovery/acquisition.

The reader performs one bounded route operation and exactly two typed descriptor
attempts. The route actually returns both B2 and stale B1. B2 yields one adopted
advisory contact; B1 yields `DESCRIPTOR_UNAVAILABLE`, reason
`TCP_CONNECT_UNAVAILABLE`, with `ABANDONED_FULL_DESCRIPTOR_BYTES_CHARGED`.
Thus both `stale_peer_returned` and `typed_stale_dial_miss` are actual true
observations, not an unexercised conditional. The stale descriptor is attempted
after the available descriptor; this does not demonstrate stale-first ordering.
Routing terminates at `PROVIDER_BUDGET`; no global discovery-completeness claim
follows from this bounded local provider result.

One authenticated offered snapshot and one `VERIFIED_PAGE` produce one match.
Search uses one provider/snapshot/page/candidate/examined row and two requests.
Full declared universes/type match the independently supplied closed goal.
Structural opening plus one offered packet are acquired; the final saved status
is `ACQUIRED` and exact postcondition true. Independent read-only database
inspection finds the same exact blobs in source, reopened custodian and reader:

- Opening 1595 B: `0c74d294730fc2d005a082aba01350e5a9ab54a5aa797036f35d607ce17c900a`.
- Packet 447887 B: `a737e8f650e9d3abb4781bb2c85c0e625ed4573b7170d71aff1799dbb54495e3`.

The composite acquisition charge is ten requests and 720296 reply bytes,
including seven prepaid location/search requests and 270336 prepaid reply bytes.
Verification attempts/input/worker CPU remain zero. No native, proof, verifier
or trust-adoption call is made; all mathematical-acceptance flags stay false.
The saved client/acquisition/workflow observations precede their finally-block
closure, so their internal `closed=false`/active snapshot labels are not terminal
leaks. Reviewed finally paths, concrete final closure reports and the final task
census establish the terminal boundary.

## Closure and cost

B1 and B2 both report `CLOSED`, null failure code, every cleanup component true,
empty error lists, closed route journals, and no pending owned actors. Their
intake/read providers have no active connections or outstanding reply reserves.
All three Nodes return zero with `closed=true`, no forced termination and no
channel failure. Source and reader workspaces close. Both task censuses, before
and after the single allowed loop settlement, are zero. This run therefore does
not identify smoke01's unsaved pending task or demonstrate that settlement was
needed here; it does establish strict zero-pending cleanup in smoke02.

Outer result is `COMMAND_EXITED_ZERO_AND_CLOSED`: direct child reaped, Job closed,
active processes 0, total processes 5, terminated processes 0, no termination
request, no cleanup error, empty stdout/stderr. Inclusive Job CPU is 43.921875 s
(18.75 user + 25.171875 kernel); separate whole-wrapper CPU is 0.609375 s, giving
**44.53125 known CPU seconds**. The 0.265625 supervision CPU is nested inside
the wrapper measurement and must not be added again; Node validation timings
are likewise inside Job accounting. Whole wall time is 51.30785559955984 s,
command-through-cleanup wall 51.17730109998956 s, and inner elapsed
50.742413400206715 s. Peak Job private commit is 373489664 B / 356.1875 MiB.
All fit the original 150 CPU / 300 wall / 512 MiB / six-process allocation.
These are selected supervisory/application observations, not hard disk/OS ingress
bounds or a throughput/scalability measurement.

The prior smoke01 remains FAIL with its unchanged evidence and 27.9375 known
CPU seconds charged. This audit uses only source/hash/JSON inspection and
stdlib-only read-only immutable SQLite checks; it imports no product, runs no
test/network/native/proof, modifies no used artifact and touches no Git.
New bounded-generations sources and eventual physical reclamation remain
separate unqualified work. Root owns adoption of this scoped result.
