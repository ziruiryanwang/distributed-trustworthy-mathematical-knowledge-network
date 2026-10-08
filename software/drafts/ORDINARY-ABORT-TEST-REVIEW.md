# Ordinary-abort native-free tests: changed-seam review

Date: 2026-09-21. Reviewer: `bounded_domains_author`. Scope: compatibility,
boundedness and coverage precision of root-authored
[`test_ordinary_abort.py`](../tests/test_ordinary_abort.py) against the proposed
ordinary-abort worker interface, plus the subsequent small registry adaptation
in [`run_state_contracts.py`](../tests/run_state_contracts.py). This reviewer authored the recovery drafts,
not these tests; this is not the independent implementation review. Only this
note is owned/edited here. No test/product edit, import, SQLite query, compilation,
process launch or execution was performed.

## Finding and disposition

One deterministic test failure was found and promptly reported to root:
`test_nonempty_sidecar_refused_and_preserved` called `S.read(journal)` although
`storage.read(path, limit)` requires its second argument. That call would raise
`TypeError` independently of the intended sidecar-preservation result.

Root repaired it to `S.read(journal, MIB)`, then added an eleventh authentication
test and the small reusable runner. The repair, added test/import, full runner
and its diff against the frozen integration coordinator were source-read.
No other deterministic interface/expectation failure was found in this static
review. This is source compatibility clearance for the stated
native-free seam, **not a passing test result or execution allocation**.

| Source | SHA-256 |
|---|---|
| Tests, initially fully inspected | `4533FB1988059DE74DCCAD2B45E073A14CC6B4EE7A6FA0FC2A20701C55AD9576` |
| Tests, after root's bounded-read repair | `2574BFF828ED752B3574BECE5D9FE12010BEBB4521D120DC070AFAC508FF0208` |
| Tests, with eleventh authentication test | `7C23A25C788C788A2056304C78F51B350A54EFBD3723C39634C7D4B9BB10F3D3` |
| Reusable state-contract runner | `F6DB9EBB9B8573FE6372EF37CAF517BEEB3D131B1406A59415D7CEC657A9A528` |
| Frozen integration-runner comparison source | `B4DBAFFF498277787FC380AB7C33E200DA81B7EC29F3EFE0D8362A49365C3236` |
| Worker draft | `68D6AC7133B4DF1D58762B81BB13BCC5D3C6512969E308A01D6270589A8529BB` |
| Wrapper draft | `3F10850777A9F22301CD090AD131987747301A78264882AA9E302DEFA856272C` |

The tests deliberately import **installed** `py/recovery_worker.py` and
`py/recovery_manage.py`, with module-origin checks. They require the reviewed
drafts to be integrated under those existing names before execution. Running
against the earlier peer-only installation would fail on absent constants or
the new `mode` keyword, not qualify the extension.

## Interface and expected branch behavior

- The tested mode sets and ordinary refusal bytes match the draft exactly.
  `owner_request` retains its selection-only return shape. Direct `recover`
  calls use its keyword-only `mode` argument correctly.
- The added identity fixture calls `authenticate_evidence` for ten original
  operations under both modes: ten permitted and ten forbidden cases. Its
  receipts/commands/config identity are synthetic, but the twelve bound
  interpreter/config/source files are actually read and hashed. It checks
  the ordinary wrapper's selected-envelope parser and one changed source-pin
  digest. The stub config is not passed through `load_config`, and the receipt
  does not claim real process/cleanup observation.
- Pending abort uses an actual charged request and stage row, real SQLite
  transaction, and synthetic initialized state/quiescence. The saturated case
  correctly uses one request, one stage and exactly `8 + 128 = 136 MiB` of
  authorization. These are accounting charges, not allocated file payloads.
- Full ten-table snapshots permit only the selected request's phase/response
  and active field to change. The stage lock marker is retained. Both stored
  request replay (`store.prior`) and recovery replay are checked; the former
  is not a public dispatcher/transport replay test.
- Terminal replay deliberately uses noncanonical response whitespace, an old
  stage, an unrelated active request, empty quiescence input and a later call
  directory. Exact bytes and unchanged state are the proper expectations.
  Its `OK` response is explicitly synthetic and claims no mathematical result.
- Pending wrong-attempt, raw/client mismatch, absent attempt, active mismatch
  and uninitialized state expect the draft's actual guards. Peer stage refusal
  and native-free peer completion preserve the existing mode distinction.
- The twenty bad-quiescence inputs comprise fifteen exact-boolean controls
  plus nonzero final active count, cleanup error, evidence error, output error
  and boolean return code. Each is expected to refuse without clearing state.
- The terminal `SQLITE_FULL` injection happens before any terminal update. A
  real rollback follows; `store._uncertain` remains false while recovery's
  conservative reply reports persistence uncertainty. The subsequent owner
  grant is correctly refused because active work remains pending.
- COMMIT fault controls distinguish an exception **before** the real COMMIT
  from one **after** it. Both mark that connection uncertain and forbid a
  second terminal write there. Reopening should respectively expose pending
  or terminal state; the exact retry respectively commits an abort or replays.
- The nonempty sidecar is intentionally synthetic. Store opening refuses it
  before SQLite recovery; the database, work marker and sidecar remain. This
  is not a real hot-journal/crash-recovery test.

## Bounds and execution premises

The eleven methods create twelve fresh stores, make thirteen request reservations
(one extra unrelated active request), and reserve eleven synthetic stages.
Exactly one fixture has no stage. They launch no native process. The test
patches native checker entry and `subprocess.Popen` to fail if accidentally
called; physical-supply observations are mocked explicitly.

Fixture roots must be fresh, absolute, outside the installation and checked
against symlinks/reparse points. Fixtures use actual owner locks and retain
them until cleanup. Store reopen remains under the fixture's held lock.
Databases use the existing finite SQLite cap and SQL VM-step guard; snapshot
queries have a 128-row/table bound and fixtures contain only small fixed data.

Each method's endpoint census permits at most 1024 entries, fewer than 257
files, at most 1 MiB per file and 16 MiB total, followed by a separately bounded
at-most-1-MiB report. Thus the suite's loose endpoint ceiling is 187 MiB unless
the runner imposes a tighter aggregate bound. This is not an OS transient disk
quota. The twelve declared 32-MiB metadata caps are likewise not evidence that
384 MiB was written. No large filler or real disk-saturation loop exists here.
Root must supply the separate reviewed process/resource/retention allocation.

## Reusable runner delta

The new runner is a source adaptation, not an import/launch of the frozen
integration runner. The inspected diff replaces one suite entry with a small
registry containing scope, declared count (eleven), allocation prefix and
selected sources. Launch validation, source-list construction and outcome
scope comparison use that registry; the supervision, observation, cleanup and
census body is unchanged. No second allocator, new process path or new retry
mechanism was introduced.

The current selection has five common inputs (interpreter, runner, stage runner,
supervisor, domains), nine selected source files and the test file: fifteen
inputs, plus the launch record gives the existing sixteen-pin supervisor limit.
The added checking/peer files cover the actual reads in the authentication
test. No current snapshot basename collides. A future suite entry still needs
review; this count and distinctness judgment is not universal to all registries.

The inherited worker envelope remains 60 wall seconds, 30 CPU seconds,
512 MiB memory and eight active processes; stdout/stderr/event are each bounded
at 65536 bytes. The combined state/evidence endpoint census remains 256 MiB,
4096 files and 8192 entries, with final-record headroom checks. Coordinator
copying/census stay outside the worker Job and are reported separately; these
are not hard transient filesystem or all-coordinator lifetime limits. Actual
runtime fit and the eventual launch's exact pins remain root's later evidence.

## Claims deliberately not covered

The expanded tests exercise source/command authentication against synthetic
receipts, but do not establish that an actual historical public call produced
those receipts. They do not invoke full config/main execution, wrapper
mode-profile forwarding, worker-main existing-lock selection, or recovery
event/stdout loss. Fixture `owner_lock` use is not a test of worker main's
`create=False` missing-lock behavior. The wrapper parser's positive cases use
the ordinary envelope; worker envelope tests separately cover both modes.

They also do not establish authentic whole-Job containment, actual native
interruption, successful checked continuation, physical disk fill, a real
hot-journal outcome, or malicious-source isolation. Missing/rejected variants
outside the twenty chosen quiescence controls are not exhaustively tested.
Those omissions are compatible with this narrowly stated contract suite and
must remain visible in any outcome report.
