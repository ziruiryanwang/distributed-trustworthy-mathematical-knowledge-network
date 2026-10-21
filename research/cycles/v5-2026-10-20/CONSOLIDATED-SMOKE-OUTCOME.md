# Consolidated smoke01: independent actual failure audit

2026-10-21, `support_guest`.

Disposition: **FAIL_BEFORE_RESTART; COMMITTED_PLACEMENT_RETAINED;
ONE_UNIDENTIFIED_PENDING_ASYNC_TASK.** The failure and its costs are preserved.
This audit confirms the recorded failure, not a restart/discovery pass. B1 was
not sealed, B2 was never constructed, and no fresh reader workspace/discovery
ran. The earlier source review did not catch the invalid receipt comparison;
this actual finding supersedes any success expectation without rewriting that
review or the used adapter.

## Evidence and identity

All run-relative paths below are beneath
`experiments/v5-local-checks/consolidated-restart-smoke-01/`.

| Artifact | SHA-256 |
|---|---|
| Exact selection / retained `selection.json` | `fc1c2bb436adf52d30de0a7512fa9a8e7d0571bc74e7fc74cca928d3efeedb22` |
| Original input, adjacent `consolidated-restart-smoke-01-input.json` | `6be80c7da1d4c33a7e08f4af2af97323cc9a08891993de5752a659aec58106b5` |
| Outer `RESULT.json`, 2276 B | `149e3fc1e50653d3c0b738f6152bf8dbbe459a7d969d9e0e8b904db48b0c34fa` |
| Inner `consolidated-restart-smoke-result.json`, 18113 B | `c6af48e8ede5ff202444f9a87f3916b3bd03692943c2cc48f5e2fb03dcbbff58` |
| `installed-smoke-sources.json`, 39660 B | `8be4ee5674eeb4f262494c8aa18cced9b4a4daac564f0c8aecb1197e9b372d02` |
| Used adapter `restart_smoke.py`, 38004 B | `e8b3a0257785e82242d20eb98a24fa4b3fad3b5884e77dc6e7a791598a6cccc2` |

The actual selected argv uses the installed isolated Python, `-I -S -B`, the
exact adapter snapshot and input SHA in the canonical working directory.
All four selected source files match both their original and snapshotted
digests. All 148 explicit runtime pins still match. The saved map has exactly
121 SDK rows, 18 Python runtime rows and two goal helpers; SDK size/hash rows
match the installed release. All 88 recorded concrete import origins are in
that release's SDK map. No source-overlay substitution was observed.

Release SHA is
`1fd0ae63faa84cc1f3ef82f17d2056657f8d6a3e5dea3686ace433987bd1e5be`;
build-input SHA is
`8ba3707236c1a6e01ab7f87886814f801034b2fe9144ad9603585adcc73feb33`.
Their relationship remains the separately adopted build audit's scope.

Review used saved JSON, selected source and small stdlib-only SQLite reads with
`mode=ro&immutable=1`. No product import, API call, new network/native/proof
work, rerun or Git action occurred. No database was opened through a writable
product owner or modified. The source author separately traced async ownership;
the reviewer independently read the relevant installed asyncio source.

## What actually happened

The inner report is FAIL at `one-remote-submit`, primary ValueError
`EXACT_COMMITTED_REQUEST_RECEIPT`. Prior assertions in that executed path require
the one submit to have returned a loopback-observed committed placement,
INDEXED_UNADVERTISED receipt and positive observed route dispatch. The intake
report records one request, one completed action, no refusal/handler error and
no retained connection. The placement client records one request, no uncertain
submit and zero transport cleanup errors. Its response body was not separately
saved: the failed comparison precedes `first_response`/`original_manifest`
report assignment. Do not present a reconstructed response as captured bytes.

Independent preserved-state inspection establishes:

- B's placement core is **OPEN**, `runs=1`, prospective `max_runs=2`. Exactly
  one request, one grant and one cell exist. The request is RECEIPT_COMMITTED,
  recovery flag zero, and generation funding equals the grant's retained used
  reservation. No consumed funding was reset by the failed harness.
- Request ID is
  `32fbb56c33426578d4908feeeac32dda9ba8f97fe57c1f668bf62969ebe5f4f4`.
  Its canonical stored manifest is 1075 B, SHA
  `804431dc2de2c4d39fa4d1d056676ab8435274bab92a165f935fa976a2f763ec`.
  The separately unsaved in-memory `raw` was not recovered or independently
  compared; stored canonical bytes alone do not prove that conjunct.
- A and B both hold byte-identical group 10 opening, 1595 B /
  `0c74d294730fc2d005a082aba01350e5a9ab54a5aa797036f35d607ce17c900a`,
  and packet, 447887 B /
  `a737e8f650e9d3abb4781bb2c85c0e625ed4573b7170d71aff1799dbb54495e3`.
  Actual blobs were compared and hashed, not merely their catalog labels.
- A's index remains empty. B has one indexed object, 22 features/postings,
  355 CAS nodes, two snapshots and sequence 1. B's workspace has zero ordinary
  operations/publications. Structural custody is not mathematical acceptance.
- The route journal has one run and one row for this request, phase
  HINT_DISPATCHED_UNACKNOWLEDGED. Its retained actual observation has eight
  events, one `add_provider_write`, no query error and remote placement
  confirmation false. This is advisory dispatch, not remote acknowledgement.
- The structural acquisition charged three reads / 449960 reply bytes and
  used zero verifier attempts, verification-input bytes or worker CPU. A's
  provider records the same three reads. No proof, native check or trust
  adoption was reached.

No `custodian-location-2` or `reader-workspace` directory exists. Failure occurs
before A's normal-path withdrawal, B1 sealing or any restart; A was instead
closed by failure cleanup. Thus the partial placement cannot qualify the
selected source-offline restart/unknown-ID boundary.

## Deterministic comparison defect

Selected `placement/network.py::_success` deliberately projects the local
receipt's `observed` map. The durable map has seven fields:
`acquisition`, `index_work`, `new_store_logical_bytes`, `packet_census`,
`store_counts_after`, `store_counts_before`, `structural_input_bytes`.
The wire map exposes only `structural_input_bytes` and
`new_store_logical_bytes`; `public_response` preserves that closed projection,
and `PlacementClient` verifies the projected response.

The actual durable outcome is 7352 B, SHA
`0c9ec0a32ef97ac9a4bc0d9a4a411b77023cab2476bc4b780d2ad646f669c5ee`.
Pure-data application of the documented projection to this saved outcome is
4399 B, SHA
`c7334c3b5ac12efe4603f5ae8a52ac7cb8cc642e0195e4aed9681f9bdb6fc35e`.
These are inherently unequal. Smoke01's unprojected
`committed["outcome"] == response["placement"]["outcome"]` is therefore an
invalid harness assertion, not evidence of ledger corruption or a new product
serialization incompatibility. The seven-versus-two mismatch suffices to
explain refusal without claiming recovery of the absent wire response.

Any fresh successor must compare the complete returned response against the
existing `public_response` of the exact local row and route, separately require
original manifest-byte equality, and retain the unprojected row for restart
invariants. It must not remove arbitrary fields from durable comparisons.

## Closure: distinguish observations from inference

B1 reports CLOSED, all seven cleanup flags true, no cleanup errors, zero-exit
Node, no channel failure/forced termination and all enumerated owner/locator/
HTTP tasks done. R also reports clean zero-exit closure. Both retain full
pre/post runtime validation over 5896 files / 130118221 bytes plus exact role
pins. A's server/task checks pass and `source_closed=true`. The reader
workspace was never constructed, so `receiver_closed=false` is not an opened
reader leak. The saved placement-client report is taken immediately before its
cleanup `close()` call, explaining `closed=false`; it is not a saved post-close
status. No placement-client cleanup exception was reported.

The independent final asyncio census nevertheless reports **one pending task**
and `cleanup_errors=["pending-async-actors"]`. Its identity, coroutine and stack
were not saved. This observation remains failed; neither clean service flags
nor outer process closure erase it.

A source-compatible explanation exists in the installed Python implementation:
`IocpProactor.accept` schedules an `accept_coro` that closes its socket after
accept-future cancellation; `_stop_serving` cancels that future, while
`Server.wait_closed` may return synchronously once closed with no clients.
On this failure path A's provider stops last, followed by synchronous workspace
close and immediate `all_tasks()` census. Its cancelled accept cleanup can
still require a loop turn. This is a reachable source explanation, **not an
identification of the actual saved pending task**. No source evidence justifies
silently ignoring/cancelling arbitrary pending actors.

The selected fresh repair may record bounded safe coroutine code identities,
yield once after all owned closes, then retain the strict zero-pending test and
original deadline. Old pending count 1 stays charged and failed regardless of
what a later run observes.

## Costs, containment and preserved state pins

The outer command exits 1 with COMMAND_FAILED; it does not convert inner FAIL
to success. Direct child reaped, Job closed, final active processes 0,
terminated processes 0, termination requested false, cleanup errors empty.
There were four Job processes, no stdout/stderr output, and peak Job private
commit 302227456 B (288.2265625 MiB), inside the selected 512-MiB/six-process
envelope. Outer wall time is 32.51522359997034 seconds; known CPU is
27.5 Job seconds + 0.4375 outer-wrapper seconds = **27.9375 seconds**.
The nested wrapper-supervision field is not added again. No old allocation
has been renewed, and this charge does not disappear after a harness repair.

| B retained file | Bytes | SHA-256 |
|---|---:|---|
| `placement.sqlite` | 32768 | `a4f2a25afb5d35599b97d679b465cc55c228a33965ba3d1b707e2fe3551f6f30` |
| `placement-routes.sqlite` | 20480 | `41ffb83a0b4e570aabef2d571265e518a64aff482182a53a27182e6b19f9a191` |
| `workspace.sqlite` | 16384 | `284315f1997d6483d92f6a9725946d51bed4775e9e509c7e477782dd4fced818` |
| `index/discovery.sqlite` | 159744 | `808799e2e785d76ad1a128044a44b92f8a0d5633a5acf832b4a847227130cc28` |
| `modules/modules.sqlite` | 28672 | `1aaa887d9aacf9d7a4a5786ffaee402a584e27c1ace796a8f9fc8985e246833b` |
| `packets/evidence-packets.sqlite` | 466944 | `cbb5fb22d57d05581b6c82d87a1d3fdba15a408dbaa1da936da4bd142fac9202` |

These paths follow `custodian-workspace/`. All used input, source snapshots,
installed product and failed-state/evidence bytes remain frozen. Root's
`CONSOLIDATED-SMOKE02-SELECTION.md` is a separate source-repair selection, not
permission to reopen this state or relabel smoke01. Smoke02 still requires
independent source review and a fresh explicit launch. Lifecycle work remains
separate; full v5 and the installed restart boundary remain unqualified here.
