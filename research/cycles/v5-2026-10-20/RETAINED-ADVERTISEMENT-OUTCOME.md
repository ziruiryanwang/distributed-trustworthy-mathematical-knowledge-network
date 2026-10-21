# Retained advertisement: actual focused-control outcome

2026-10-21, adaptive_audit. **PASS within the nine selected controls.** Root's
session 21269 exited zero. Independently inspected the terminal evidence,
selected sources and staged map, complete result/observations, relevant control
assertions and saved SQLite state. This audit ran only read-only diagnostics;
no product import, test rerun, network, proof, installation or Git mutation.

## Exact executed boundary

Evidence directory: `experiments/v5-local-checks/retained-advertisement-controls-01`.

| Saved file | Bytes | SHA-256 |
|---|---:|---|
| `selection.json` | 23321 | `52403f3c0b99f10e7044751c56b78e2c1cd33e9dffc3bd00102b981c313fc3bf` |
| `RESULT.json` | 2043 | `1c870264e18c3799190afdc216df0a7a481e4538fc6101827fb3c35949eb5324` |
| `retained-advertisement-controls-result.json` | 43781 | `1b35101cc01570d359dcd65ad924d22f4d1313d902c8f6fee1e2ff51ccea43ea` |
| `command/stderr.txt` | 21457 | `78a50d8359c9ada8171bb3674671278334904271efede490e18ff80f076c4596` |
| `command/command.json` | 699 | `33850ca308bf374314dae08561f72342733343d5933beabdc1376c2d8e98f8b6` |

The original selection and retained selection have the same exact hash.
All **127 original physical sources and 127 retained snapshots**, **19 direct
runtime/input pins**, and **121 reported/staged logical product files** match
their selected hashes; staged byte lengths also match. No extra staged or
snapshot files were present. The base map has 114 logical files: the unchanged
110 retain their exact map paths/hashes, four reviewed replacements and seven
reviewed additions produce precisely 121. Every reported source belongs to the
selected physical snapshot.

The actual changed boundary is the previously reviewed advertisement
`5aa23ee7`, service `7e735337`, controls `3d64a99d` and selector `8c682a33`;
full hashes are in source review `5a790c96`. Bounded runner `44a7bf1b` checks
runtime pins before and after execution and retains/checks source bytes. Its
recorded final status is `COMMAND_EXITED_ZERO_AND_CLOSED`, not a failed binding
or cleanup fallback. Explicit runtime pins are not a hermetic-toolchain proof.

## Actual behavior

All nine prospectively selected methods ran: nine result observations, zero
failures, errors or skips, empty forbidden-call and unhandled-loop-error lists.
The independent stderr record ends `Ran 9 tests in 4.593s / OK`; its additional
lines are asyncio slow-task diagnostics, not ignored test failures.

| Control | Actual asserted result |
|---|---|
| Sealed restart | Two funded runs; one restoration dispatch; original receipt, custody and index unchanged; old-token new write refused despite simulated expired original publisher windows. |
| Representative refusal | OPEN, unknown, partial, wrong-domain and oversized selected records refuse; call is charged without restoration dispatch or repair. |
| Missing local metadata | Posting, snapshot, name, packet-offer and body cases refuse without refetch or re-admission. |
| Retention boundaries | Too-short/expired horizons refuse; expiry immediately after reservation COMMIT prevents send; post-send expiry retains uncertainty; neither permits another same-run dispatch. |
| Dispatch/observation failure | Both failures retain the charged attempt; duplicate restoration returns uncertainty without redispatch or placement-charge change. |
| Immutable caps/config | Four reopen refusals; route-configuration failure consumes the second core run rather than refunding or enlarging it. |
| Owner cancellation | Cancellation propagates; concurrent restore refuses; busy ownership releases and a retry does not redispatch. |
| Close during restoration | Owner task is cancelled/drained before stores close; uncertain route attempt survives. |
| Close before busy entry | Tracked task is handled before advertisement busy-entry; store closure follows task completion and no restoration is dispatched. |

Read-only SQLite checks independently corroborate the saved state: successful
`c01` has exactly run-1/run-2 dispatched hints, two core runs, SEALED_SERVING and
one committed placement receipt. Both `c04` horizon and `c05` failure fixtures,
plus cancellation/close `c07`/`c08`, retain run-2 `DISPATCH_ATTEMPTED`; `c09`
retains only the original run-1 route. These reads used URI `mode=ro` and
`PRAGMA query_only=ON`, with no product imports or mutation.

The harness uses real Workspace, SQLite, controller, index and owner API,
but simulated Node/listeners and inert unverified packet bytes. Process/socket
and mathematical receive entry points are guarded; restoration additionally
forbids packet/body reads or writes, re-admission and old acquisition helpers.
There were no actual network, Node-child, native-check or proof calls and no
mathematical acceptance. Tiny fixture table dumps are test assertions, not a
product corpus-scanning path. This does not test real DHT rediscovery or certify
fresh blob integrity.

## Resource accounting and closure

Original limits remain 60 CPU seconds, 120 wall seconds, 384 MiB, two processes,
and 1 MiB per output stream. No retry or allowance renewal occurred.

- Job user 2.78125 + kernel 1.65625 = **4.4375 CPU seconds**.
- Whole runner CPU **0.546875 seconds**; known inclusive total **4.984375 CPU
  seconds**. Nested supervision 0.078125 is already inside runner CPU and must
  not be added again.
- Whole runner wall **9.856469000224024 seconds**; inner command through cleanup
  9.643761300016195 seconds. These intervals are nested, not additive.
- Peak Job private commit 33,398,784 bytes; two total processes, zero active,
  zero terminated. Direct child reaped, Job closed, no termination requested
  and no cleanup errors. Stdout 0 bytes; stderr 21,457 bytes.

Every test teardown asserts CLOSED, retained-task completion, empty intake
task/writer sets and stopped simulated listeners. The actual outer process-tree
closure is separately recorded by the runner. Sampled wall/CPU/log limits and
private-commit accounting are not hard disk quotas or real-time guarantees.

## Disposition

Adopt the scoped retained-advertisement controls pass; preserve all used bytes
and do not repeat this suite. Actual cross-run network discovery, generation
reclamation, economical certification, full-cost useful growth and final-v5
readiness remain separate obligations. This small restoration result supplies
no new mathematical warrant and is not a final-release claim.
