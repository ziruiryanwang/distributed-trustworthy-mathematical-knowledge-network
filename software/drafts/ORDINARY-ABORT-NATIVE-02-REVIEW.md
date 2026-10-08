# Native ordinary-abort 02: exact-delta and launch review

2026-09-21. **PASS at the source/exact-launch gate; no blocker found.** This
clears the specified fresh allocation only, not a native result or automatic
retry. Review was limited to source/text/JSON, hashes and filesystem checks.
Only this note was authored; no product import, test, SQL query, native launch,
patch application or evidence modification was performed.

## Demonstrated cause and complete correction

Read the complete [native-01 source review](ORDINARY-ABORT-NATIVE-CODE-REVIEW.md),
native-01 result, hook supplement, original public supervisor receipt, retained
stage plan/receipt, post-failure observation, full native-02 coordinator, changed
worker seam and complete two-file diff.

Native-01's original public receipt reports `HOOK_ACTUAL_LEAN_COMMAND`; the
outer failure is the subsequent `EXACT_LIVE_LEAN_TRIGGER_AND_HANDLES` assertion.
The hook supplement records zero opened/closed handles and zero triggers.
Command and `lean_path` match their plan expansions. Only cwd differs:
the old expected suffix is `stage-0001/input/native`, whereas the receipt has
`stage-0001\input\native`. Source `run_stage.py:367` constructs
`Path(expand(cwd))` and line 371 records `str(workdir)`. Normalizing the exact
retained expected path reproduces the observed cwd; the raw comparison fails.

The new worker compares cwd to `str(Path(expand(...)))`, exactly the runner's
representation. It does not remove command/cwd authentication, resolve an
arbitrary alternate directory, or relax a liveness or cleanup condition.

Whole-file text comparison confirms the complete delta is only:

- Worker: data root `01` to `02`, expected coordinator basename to `_02.py`,
  and that single cwd-expression correction.
- Coordinator: evidence/data roots `01` to `02` and worker basename to `_02.py`.

All process-image, exact-Job-membership, live-handle, deadline, trigger, balanced
handle, quiescence, pending-state, recovery, replay, continuation, accounting
and outer-limit assertions remain unchanged. This is a diagnosed fresh experiment,
not a blind repeat or reinterpretation of native-01. Native-01 remains failed;
its post-failure observation reports two requests/two stages and 272 MiB still
charged, with the second request pending. No recovery was reached there.

## Exact cut and launch closure

| File, relative to `software` | Bytes | SHA-256 |
| --- | ---: | --- |
| `tests/ordinary_abort_native_worker_02.py` | 58,212 | `59658F620CA20A8D015E2B3C67574BB397ED8914292B4EC97F91A1DA6F2D3AAE` |
| `tests/run_ordinary_abort_native_02.py` | 15,884 | `B5E9D563A6191606F94F019A0FABE99132BDF3FA09A36BC7C74627DD9CAE81DA` |
| `qualification/ordinary-abort-native-launch-02.json` | 41,645 | `1F52F008A97D5265A98EF953A056A4C0285BD4F9E7412A5118A69AE4F4CDABB5` |

The original worker/coordinator/launch still match their native-01 reviewed
digests. Native-02's entire ordered product list matches native-01 and an
independent current-filesystem enumeration: **101 files / 3,478,260 bytes**, with
exact relative/absolute paths, lengths and hashes, no omissions or extras.
The native/assets traversal contains 90 entries within its existing bound.

The eight ordered source pins also match actual files: Python, coordinator02,
worker02, scenario profile, stage runner, supervisor, domains and selected Lean
executable. Only the two declared harness inputs differ from native-01.
They total 318,433 bytes; adding the launch gives **nine outer pins / 360,078
bytes**. The six source-snapshot basenames are distinct. The 133 distinct
selected file/ancestor paths inspected contain no reparse point.

Both roots are absent, confirmed by direct existence and parent-entry checks:

- `E:\Distributed Trustworthy Mathematical Knowledge Network\product-local\ordinary-abort-native-02`.
- `E:\Distributed Trustworthy Mathematical Knowledge Network\software\qualification\ordinary-abort-native-02`.

Schema, 101 product entries, unchanged source roles, limits and retained fields
match the reviewed coordinator. The envelope remains 450 wall/450 CPU seconds,
6144 MiB, sixteen outer processes, 65,536-byte stdout/stderr/event, and the
1-GiB/16,384-file/32,768-entry retained endpoint. Public inner limits, fifteen-
second ordinary settle allowance and five-second recovery settle are unchanged.
Coordinator copying/census remain outside the Job; endpoint counts remain
non-transient quotas. Existing startup checks must reauthenticate these facts.

Root may proceed through its existing one-launch workflow using pinned Python
with `-B -E -s -S`, this absolute coordinator and `--launch` this absolute launch.
A successful run still reaches only `PASS_PENDING_INDEPENDENT_OUTCOME_AUDIT`.
Actual live-Leaf/Job evidence, whole-tree cleanup, exact state/charge preservation,
recovery/replay and fresh canonical continuation require that later audit.
