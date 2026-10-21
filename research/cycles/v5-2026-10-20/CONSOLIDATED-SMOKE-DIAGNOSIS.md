# Installed restart smoke01: preserved failure diagnosis

2026-10-21, support_screen. Read-only diagnosis, no repair or rerun. The used
adapter `restart_smoke.py` remains 38,004 B /
`e8b3a0257785e82242d20eb98a24fa4b3fad3b5884e77dc6e7a791598a6cccc2`.
No product source, installation or actual evidence was changed. The separate
bounded-generation controls remain deferred; no test files were created.

## Observed outcome and limit

Evidence under `experiments/v5-local-checks/consolidated-restart-smoke-01`:

- Inner `consolidated-restart-smoke-result.json`, SHA-256
  `c6af48e8ede5ff202444f9a87f3916b3bd03692943c2cc48f5e2fb03dcbbff58`:
  FAIL at `one-remote-submit`, primary `EXACT_COMMITTED_REQUEST_RECEIPT`;
  one `pending-async-actors` cleanup error and `pending_async_tasks=1`.
  Inner elapsed time 31.99649089993909 seconds.
- Outer `RESULT.json`, SHA-256
  `149e3fc1e50653d3c0b738f6152bf8dbbe459a7d969d9e0e8b904db48b0c34fa`:
  COMMAND_FAILED / exit1, with direct child reaped, Job active0,
  terminated0, four total processes and no outer cleanup errors.
  Job CPU27.5 seconds, wrapper CPU0.4375 seconds, outer wall32.51522359997034
  seconds. Outer containment did not need forced termination.

The placement client reports exactly one completed request, no uncertain
submit and no client cleanup errors. B1's actual service close is CLOSED with
all seven cleanup flags true; every recorded owned B1/locator task is done.
B1 and R each report Node exit0, no channel failure and no forced termination.
Source A closes. The mathematical reader workspace was never created; the
source was not sealed and B2 was never started. This run does **not** establish
restart, restored-route discovery or exact post-restart acquisition.

The failed assertion occurs before `report.update(first_response=...,
original_manifest=...)`, so that full response/expected-manifest snapshot is
not retained in this inner report. The client report is captured immediately
before `client.close()`, explaining its `closed:false` field; this field is not
an observation that close subsequently failed.

## Cause 1: comparing a durable receipt with its intentional wire projection

Adapter line491 requires both exact manifest bytes and:

    committed["outcome"] == response["placement"]["outcome"]

The second comparison is contrary to the selected wire contract. Installed
`sdk/v5/placement/network.py`, 31,301 B /
`1ec5c452ec129ae033f0577ebac6223e2cf3192d4724a3d31fe2e5c27a06cd4b`,
matches the release. `_success` lines164-176 validates the durable observation
with **seven** keys, then deliberately projects it to two audited totals:
`structural_input_bytes` and `new_store_logical_bytes`. Its discarded local
diagnostics are `store_counts_before`, `store_counts_after`, `index_work`,
`packet_census` and `acquisition`. `public_response` documents that this is a
closed wire projection and does not modify the immutable local ledger receipt.

The server applies `public_response` before writing HTTP; the client validates
the response again using `projected=True`. Thus a successful committed local
receipt and its correct wire response are expected to differ in precisely
this nested diagnostic field. Neither tuple/list normalization nor a missing
placement commit is needed to explain the failed condition.

Support_guest owns the single independent SQLite inspection, using stdlib
SQLite read-only/immutable connections and no product import. Its reported
durable facts are:

- One original request, one grant, one cell; core OPEN / runs1 / max_runs2.
- Request phase RECEIPT_COMMITTED, recovery false, retained funding charges.
- Durable receipt7352 B / `0c9ec0a3...`; intentional projected outcome4399 B /
  `c7334c3b...`, with the exact seven-key/two-key difference above.
- Route journal run1 has actual `add_provider_write=1` and eight events.
- No B2 or reader workspace.

The complete outcome audit owns the full database-derived digests and exact
fixture/canonical comparisons. This author did not duplicate its database
reads. The in-memory `raw` value itself was not saved before the failing
assertion; the source canonical request/ledger path and the independent audit
must be distinguished from a retrospectively invented captured value. The
outcome-projection mismatch alone guarantees that the original conjunction
cannot pass for this committed receipt.

If root selects a fresh adapter, the precise correction is:

    committed["manifest"] == raw
    public_response(
        {"placement": service.ledger.public(committed),
         "route": response["route"]}, expected, rid
    ) == response

Keep the entire original unprojected `committed` snapshot for the subsequent
reopen/advertisement/reader checks. Do not remove diagnostic fields from the
ledger, bypass the current wire projection, weaken exact stored-data equality
or rerun duplicate/status exchanges. Save the observed response and bounded
comparison diagnostics before a fresh assertion so another failure preserves
its distinction. This is an adapter correction, not a product protocol change.

## Cause 2: one pending task, actual identity not captured

The saved observation is **only a count**. No task name, coroutine source,
stack or owner identity was saved, and stderr is empty. It is therefore not
possible to identify the exact observed task retrospectively. In particular,
the report does not establish a live service actor or an abandoned Node process;
all directly recorded owner/service checks and outer Job closure passed.

A concrete source-derived explanation fits the exact failure path:

1. Installed Python `Lib/asyncio/windows_events.py` lines565-574 creates an
   `accept_coro(future, conn)` task using `ensure_future` for each outstanding
   IOCP accept. On cancellation it closes the temporary accept socket and
   re-raises cancellation. This task is owned by asyncio, not the provider's
   application-handler `tasks` set.
2. `Lib/asyncio/proactor_events.py` lines890-895 cancels that accept future
   when the listener closes, which schedules coroutine cleanup for a later
   event-loop turn.
3. `Lib/asyncio/base_events.py` lines410-411 allows `Server.wait_closed()`
   to return immediately once the listener is closed and has no clients. It
   does not explicitly join the separate accept-cleanup task.
4. The primary-failure cleanup path closes B1, then R, then stops source A's
   still-open provider last (adapter line563). A's `Provider.stop` closes the
   server and awaits its already-completed `wait_closed`; there are no active
   application handler tasks to gather. It can therefore return without
   yielding. Adapter lines567-574 close the SQLite workspace synchronously
   and immediately count all pending asyncio tasks.

Consequently the newly scheduled accept cancellation may still be pending at
that census despite a closed listener and zero application actors. This is a
**source-compatible candidate, not an identification of smoke01's task**.
No read-only artifact can reconstruct an omitted coroutine identity. The
normal successful path would stop A earlier, followed by several genuine
awaits, which is a material difference from this failure-only cleanup order.

The three installed stdlib sources were read and their actual SHA-256 values
matched the adopted release:

| Installed Python source | SHA-256 |
|---|---|
| `Lib/asyncio/windows_events.py` | `45b694f5dedd06d91ab749ac85291b771a45c00bd195285c66f0bd92ab5ce2b5` |
| `Lib/asyncio/proactor_events.py` | `edfe546a07074ed405ca7e7e27e7810082a17d419e00576db2445a672749020c` |
| `Lib/asyncio/base_events.py` | `da597bc24e06382d9ef836d84d0e383ad1f6fd61d3b1fb1bfd2bd50d359f97b0` |

The inherited source provider stop is installed
`sdk/v5/transport/http_provider_receipts.py`, SHA-256
`4e00afb1edf7c5fb7c6b3bd3f538e2a1fdbd9aef9af32c23baeeb7717c89bc4b`.

If root selects a fresh adapter, retain all strict owned-actor checks. Add a
bounded safe task census (coroutine qualified name and source identity only,
never repr/frame locals/token-bearing values), allow one explicit zero-delay
event-loop settlement after listener closure under the original deadline,
then require zero remaining tasks. Do not cancel arbitrary tasks, waive unknown
actors, wait indefinitely or modify the frozen provider merely to suppress
the count. If a task remains after that fixed settlement, preserve its actual
identity and fail. This proposal has not been executed or qualified.

## Disposition

The main failure is a deterministic adapter contract mismatch. The second is
an incomplete diagnostic whose source-compatible cancellation explanation is
now identified, but whose actual task identity remains unknown. Preserve FAIL
and all used input/source/state/costs. Any repair needs a new source path and
fresh finite root selection; smoke01 is not resumed, edited or relabeled.
