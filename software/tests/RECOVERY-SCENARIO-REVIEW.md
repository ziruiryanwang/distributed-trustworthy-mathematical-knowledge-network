# Static review: genuine interrupted-transfer recovery scenario

Review date: 2026-09-21. This review is source inspection only. The reviewer did
not execute, import, compile or test the scenario, query a product database, or
modify product/scenario source. Only this review note is authored here.

## Current disposition

`EXACT_LAUNCH_REVIEW_PASS` for the single launch identified in the final
addendum; not runtime qualification. The narrow proposed experiment is
appropriate: one fresh receiver, one genuine
published inert fixture, one intentionally interrupted ordinary acquisition,
one same-request wrong-attempt control, exact terminal replay, then one fresh
candidate-only acquisition. No fabricated pending row or acceptance result is
needed. The final source cut resolves the evidence/accounting findings below;
no remaining blocking source defect was identified within this experiment's
declared trusted-owner and bounded fresh-state premises. Runtime qualification
must still come from a separately reviewed launch and actual retained evidence.

The reviewer authored the original recovery worker/wrapper drafts. This is an
independent review of another author's scenario, not an independently authored
certification of the recovery core. The separate worker and wrapper reviews in
`../drafts/RECOVERY-REVIEW.md` and `../drafts/RECOVERY-SUPERVISION-REVIEW.md` remain
the relevant independent core reviews.

## Initial reviewed identities

Paths are relative to `software/`. Values are SHA-256 of files actually read.
These identify the initial cut under review, not an approval of future bytes.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `tests/recovery_scenario.py` | 39860 | `EE8F20C9DB10E20FE5B775BC7B7232EA68FD95623C7835DF1EF566D000B051FD` |
| `tests/RECOVERY-SCENARIO.md` | 12726 | `BB3440F8B5D23D6D6353C18572BB9F22E863B1709AC9272F188ACD5631484AC7` |
| `tests/prepare_peers.py` | 25349 | `1CB723AF882F4E3FBB4C65425534CDD3AC9668AECF4DFAEF2C05A8EE9B33C660` |
| `py/recovery_worker.py` | 17803 | `1C5B9843152FFC6433722B5CF76C6F67B3C1C58EBA98C77607A8424342FE6299` |
| `py/recovery_manage.py` | 8837 | `E701D4B4FF7FB87EF048C61DCD559FEBA56A08AA169F0AB6B006791EFE2171A1` |
| `py/run_stage.py` | 26505 | `3C84F507DBB788827DBD50DE2D0D7552E4F72BD615F425CFD5F1DA278AC5A5BE` |
| `py/supervise.py` | 18611 | `E5F35C0A88602757ECB7FF899F923F940B588E11E2A7C9C36D51FDBB2DFCAC1B` |
| `manage.py` | 12310 | `4219D9520DB7A35F3EE321C3A82AD246765E0C70957C3B29E924B59D6B606070` |
| `build.py` | 7953 | `9F57312577C3E48683D4BFC365134A964CF85BB2FD3C86B98D642926DD1E08CF` |

## Final reviewed scenario cut

The complete repaired coordinator was reread and compared against the actual
integrated producers of supervisor, grant and build-stage records. Its final
small evidence-error guard was then inspected and its final hash checked. No
execution, import or syntax compilation by this reviewer occurred.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `tests/recovery_scenario.py` | 51120 | `F1D6C7164196BB0F0F95DCBAD998B6CF5E46D87122CF7466E390570E8E6DAA30` |
| `tests/RECOVERY-SCENARIO.md` | 14929 | `2AA4242D6848210A9749B8714DF215B9BBE9A0331A5512AE8D8A63C461D0EE7A` |

The intermediate repaired source was 50,961 bytes,
`5FC9E9B92023A64062963F0F906C18E412BD0327ABC04BA44ADC4D8CD181E700`.
The final change adds the explicit output/evidence-persistence-error guard
inside the retained observation's `try/finally`, after CPU accounting and
before accepting quiescence. This note's initial table preserves the rejected
handoff identity; only this final table identifies the source-ready scenario.

## Resolved repair findings

The following describes the original defects and required remedies. All five
are resolved in the final cut, as checked in the resolution section below.

1. **Preserve authenticated observations before expected-result predicates.**
   Initial `bind` tests a success-specific stage ceiling and the recovery
   no-checker profile before accounting CPU. It checks the aggregate budget
   before returning the evidence binding to the caller. Therefore an
   unexpected but authentic event, or a late budget crossing, can lose known
   costs or leave known quiescence labelled unbound. Authenticate the actual
   origin; record available CPU, typed actual stage observations and cleanup;
   persist the binding; only then assert the expected profile and budget.
   Unknown counters must remain explicitly unknown, not become zero.

2. **Do not let the outer CLI frame hide inner completed work.** Initial
   `cli` rejects nonzero exit or malformed stdout before discovering/binding
   the ordinary or recovery supervisor evidence. Separate collecting raw CLI
   outcomes from interpreting public success. An authentic completed refusal
   or unexpected profile still has real costs. A truly unbound transport may
   remain explicitly uncertain; this review does not demand invented evidence
   or universal accounting after arbitrary process/storage failure.

3. **Cover the same ordering in build and interruption paths.** Initial build
   handling checks successful status/two steps before retaining its stage
   observation. Initial direct-interruption handling raises inconclusive if
   Transport returns normally before binding that real completed call. Retain
   any authentic available stage/call observation before either expectation.
   A failed build may lack a public build receipt; its known stage directory
   must not be assumed to have consumed zero work.

4. **Authenticate exact evidence origin, not only IO hashes.** Initial `bind`
   lacks exact ordinary eleven-pin/recovery sixteen-pin identity, command,
   grant and supervisor file-record checks. Bind the installed frozen cut,
   interpreter/configuration, selected original receipt and finalized recovery
   grant; authenticate actual recorded adjacent files and expected command
   paths. Permit absent partial outputs only where the retained failed
   supervisor describes them accurately. Output/evidence-persistence errors
   must not silently become a fully authenticated successful observation.

5. **Keep failure reporting possible after sender cleanup fails.** Initial
   exception handling calls `sender.shutdown()` without protection. A close
   exception could prevent writing the scenario failure record. Retain that
   cleanup uncertainty in a protected path, never claim a successful join or
   closure that was not observed.

## Resolution checks

- `cli` retains raw output, exit status, direct-child outcome and capture or
  transport errors without first requiring a successful public JSON frame.
  `public` discovers and binds available inner evidence before calling
  `frame`. A true setup/transport failure without authentic final evidence
  remains unbound and stops; it is not converted into zero consumed work.
- `bind` authenticates exact installed ordinary eleven-pin or integrated
  recovery sixteen-pin order and counts, exact recorded limits, command/state
  paths, request bytes/digest, all five present-or-absent output metadata rows,
  and the complete finalized recovery grant. The grant's fifteen inputs and
  separate sixteenth self pin match the actual integrated wrapper; there is
  no self-referential grant hash. Ordinary peer calls and the ten-second direct
  override match the unchanged supervisor's default-merging behavior.
- After origin authentication, CPU is accounted once. The retained observation
  is installed in the command record before evidence-error, cleanup, event or
  actual-stage validation. A `finally` writes its binding. Authenticated typed
  stage counts are added before success-specific ceilings/profile predicates;
  missing event counts remain `null`, not zero. Public framing, expected
  workloads and aggregate budget checks occur after this persistence.
- Build observation uses the deterministic stage path even if the outer build
  reply is nonzero or lacks a successful build receipt. Its exact plan,
  domains, request/accounting directory, runner snapshot, interpreter/runtime
  and frozen installed files match `build.py` and `run_stage.py`. Actual stage,
  available CPU and cleanup evidence are retained before requiring the
  successful two-step build. An unauthenticatable or missing receipt still
  remains explicitly unbound; arbitrary storage failure is not covered.
- A normally returned direct call retains its returned stdout/event and binds
  the actual Job before reporting that the intended interruption did not
  occur. A genuine failed direct call is likewise bound before testing the
  exact deadline-failure predicates. The latter's absent event is permitted;
  zero native work is established later by exact ledger-stage equality, not
  inferred from the missing event. That later observation enriches the final
  result; the earlier immutable binding remains its earlier observation.
- Sender shutdown exceptions are caught separately in the outer failure
  handler and retained as cleanup uncertainty. This removes the known
  secondary-exception path suppressing the failure report, without promising
  persistence despite disk failure or claiming a join that was not observed.

The fresh acquisition comparison deliberately checks head/stage preservation,
one new candidate/provider cut and the normal new request/byte charges. Unlike
the recovery/replay comparisons, it is not a full-table specification of every
permitted ordinary-acquisition row. The next exact successful terminal replay
and unchanged full snapshot supply the separate replay check. No broader
ordinary-acquisition conformance claim is made by this review.

## Conditional state argument checked

Let `L0` be the complete read-only ledger before the interrupted request and
`k` its ordinary request key. The required actual pending snapshot is exactly
`L0` plus one pending request, its reservation-created original-attempt marker,
one request charge, 64 MiB byte charge, and `active = k`. All other observed
tables/rows are unchanged. This is stronger than inspecting only an error
message or the absence of a returned candidate.

The same-byte retry must leave that ledger unchanged. Its separate clean
receipt cannot substitute for the original attempt marker. Wrong-receipt
recovery must likewise change no row. Correct recovery changes only the
selected phase/response to the exact interruption refusal and clears `active`.
Both ordinary and recovery terminal replays leave the entire ledger unchanged.
The successful fresh acquisition consumes another normal allowance and yields
an untrusted candidate; it must not alter the mathematical head or allocate a
new native stage. Its successful terminal recovery replays exact bytes and
changes no row. The orphaned interrupted work directory's final full census
must equal its earlier census; no deletion/refund is a recovery premise.

The coordinator only builds expected snapshots in memory. It does not write
the control database. Product mutations occur through ordinary installed
interfaces or the one unchanged supervised node invocation with a tighter
test-only deadline. These properties are source expectations until executed
evidence is audited.

## Scope and remaining launch conditions

- The accepted allocation is eleven public CLIs plus one directly supervised
  ordinary call, one support-build stage with two compilations, and one
  bootstrap native stage. It contains no native admission and no mathematical
  contribution. Broader negative recovery controls remain unqualified.
- The sender is an explicitly trusted cooperative thread. Its three exact
  connections, real partial body progress/disconnect, exact supervisor wall
  failure, final socket closure and join must all be observed. A timing miss
  is an inconclusive retained run, not authorization for an automatic retry.
- Read-only ledger snapshots require worker quiescence, stable owner state and
  no nonempty SQLite sidecars. The 4 MiB serialized snapshot ceiling is not a
  hard transient allocation bound: rows/hex conversion precede serialization.
  Fresh tiny state and declared trusted-owner limits delimit this experiment.
- CPU is only observed coordinator/sender CPU plus uniquely authenticated Job
  CPU. Direct wrapper work and unbound Jobs remain unmetered. Nested bootstrap
  Job CPU must not be counted again. No outer hard coordinator CPU/memory Job
  or hard transient disk quota is claimed.
- Source readiness is separate from exact launch review. Before root launches,
  inspect the frozen launch's coordinator/helper/Python/source/runtime pins,
  actual G02 publication/exposure fixture lineage, finite allocation, exclusive
  fresh roots, selected port and declared trusted deployment assumptions.
  The exact launch reviewed below satisfies this source/fixture/allocation
  check at inspection time; freshness and input stability must still hold at
  invocation.
- This cannot establish power-loss recovery, nonempty-journal repair,
  native-stage recovery, migration, quota renewal, independent-host security,
  full operating-system failure accounting or general system operability.

## Exact launch review addendum

Disposition: `EXACT_LAUNCH_REVIEW_PASS`, 2026-09-21. Root may perform this one
already allocated run with the frozen launch below. This is not execution
evidence, a replacement-run allocation or approval to repair/reset state after
an inconclusive result. This reviewer used only PowerShell/.NET read-only file,
hash, JSON/binary inspection and OS listener observation; no project code,
Python, Lean, database query or network service was executed.

Launch: `qualification/recovery-launch-01.json`, 31,174 bytes,
SHA-256 `54F7CD3CCC1229C460B3BD5FFA1F8371C125470C201E7BFD2ED1EDFB33B21803`.
The reviewed invocation is the pinned `D:\Python314\python.exe` with
`-B -E -s -S`, the absolute path to `tests/recovery_scenario.py`, and `--launch`
followed by this absolute launch path. No other test case, retry or root is
included.

The following were independently observed:

- All 106 direct launch pins matched actual byte lengths and SHA-256 values:
  coordinator, helper, Python, Lean executable, 98 product files and four
  fixture records. Selected files and traversed ancestors had no reparse-point
  attributes. The current source set is exactly the helper's intended selection
  under `software/`: four root files, all direct `py/*.py`, all regular native
  files and all regular asset files. It has 98 files totaling 3,431,068 bytes;
  the supplied product-relative POSIX ordering equals independent ordinal
  sorting. No file is supplied from an old installation in place of the new
  recovery-capable development cut.
- Coordinator and helper pins equal this review's approved final identities.
  The mutable `API.md` pin is 8,867 bytes,
  `EDCBF075AB860B9503F5940B3ABBFFC43CC816823D323BC241A1A303F768B319`.
  The recovery worker/wrapper, checked-close runner and management wiring match
  the integrated identities recorded earlier. The selected executable is
  Python 106,208 bytes, SHA-256
  `03168C01B7B7491423350E82C26FEE71F35B43694D1319D3C668BDA6903A0C38`;
  the selected Lean executable is 83,456 bytes, SHA-256
  `A8040E2CAB341C12116AB591FED9F761816F5F6B08554F6CC1680E86DFBBA0A2`,
  at the expected `runtime/lean-4.34.0-windows/bin/lean.exe`. These are
  executable identities, not full-distribution authentication or a version
  execution check by this reviewer.
- G02 is the actual schema-2 `g02` / `g_to_beta` continuation with status
  `G_OFFLINE_ADMITTED_BY_BETA_AWAITING_INDEPENDENT_H_AUTHORING`: 57,621 bytes,
  SHA-256 `5BAB68A1F02BF97883704F4BEF1B4C63A341F0F3C81E169BB72123E086831E6C`.
  Eight additional publication/exposure request, response, event and supervisor
  pins were rehashed and all matched. Publication and exposure responses are
  `OK`; exposure contains one entry. The exact exposure request is client
  `local`, ID `peer-g02-expose`, operation `expose`. Independently hashing the
  ordinary compact JSON array plus newline gives request key
  `3daeca50176b8a36737de2b41180d13f0a2ab12a8339f57bd1aa988bbbf2acd2`.
  The selected catalog and completion reside under that actual Alpha exposure
  `state/work/<key>/peer-view` directory.
- The catalog has one entry and its descriptor equals the actual publication
  response's descriptor. Its 3,680-byte SHA-256 is
  `AB5F311DA32B03F03E892069DE93C81FEE98B020429130FF2359D1C4BB57B55A`;
  exposure and completion bind that hash. Completion has schema 1 and the same
  foundation. The bundle is 298,037 bytes with digest
  `32AC4A51E45013550F17B9BBE79FCD453E7F2A96EA50F7F652FB36A5910C1221`;
  the catalog's size/digest agree. Its actual magic and big-endian manifest
  length decode correctly. The 10,249-byte embedded manifest has SHA-256
  `BC53CDFE2AC37E1F38EAA53088EAC07B30908DE00B6154916207C506B407C9D7`,
  matching the entry. There are 287,764 bytes after that manifest, satisfying
  the genuine-prefix condition for withholding the final 64 bytes. These
  checks authenticate an inert fixture, not independently prove its mathematics.
- The two exclusive roots `qualification/recovery-01/` and project-level
  `product-local/recovery-01/` were absent. No listener on local TCP port 43173
  was observed. The latter is not a port reservation or guarantee against a
  later race. Root separately reports no live peer processes; the new run does
  not invoke or mutate the old peer installation/state.
- The exact unchanged allocation is 1,800 active wall seconds, 1,800 observed
  CPU seconds, 500 seconds per build/init outer command, 1 GiB retained bytes,
  90 sender seconds, three sender connections, 4 MiB charged sender output,
  one ten-second interruption override and literal loopback port 43173.
  Ordinary non-init public commands retain the coordinator's 150-second bound;
  installed Jobs have the smaller reviewed per-operation grants. The completed
  scenario remains eleven public CLIs plus one direct supervised call, one
  support-build stage and one bootstrap stage, with zero native admissions.

Any changed pinned input, occupied exclusive root, wrong fixture, timing miss,
nonempty journal, incomplete cleanup or unexpected result must stop under the
reviewed harness semantics. Retain the real result and state. This review adds
no authority to change an old cut, erase evidence, reset a quota, fabricate a
pending row or relaunch under a replacement path.
