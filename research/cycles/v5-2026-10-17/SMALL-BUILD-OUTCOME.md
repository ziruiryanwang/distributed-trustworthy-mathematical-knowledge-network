# Smaller-segment native build outcome audit

2026-10-17. Reviewer: `memo_independent_review`.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.

Scope: independent inspection of root's actual compile/evidence records,
source/runtime bindings, emitted binaries, process closure and costs. This
reviewer authored the native source, so this is **not** independent approval of
that source's mathematical correctness. The separate `v5_growth_decision`
source/selection review in [SMALL-REVIEW](SMALL-REVIEW.md) supplies that role.
No compiler, product module, native host, guest, proof or test was invoked by
this outcome audit. No Git or source mutation occurred. The workspace guard
passed. All inspections used the canonical root and explicit paths.

## Snapshot host: PASS within compile-only scope

Actual run:
`experiments/v5-local-checks/small-aggregate-snapshot-host-build-01`.

| Binding | Actual value |
|---|---|
| Selection SHA-256 | `e4493418256735529f7fc19ed606ea459bf35b613b57680d2e0a31a7b858e4bd` |
| Result status | `PASS_SMALL_AGGREGATE_SNAPSHOT_HOST_ONE_LINK_ONLY` |
| `RESULT.json` SHA-256 | `7ad07e35602092833d9f40e7f0775f0b4eceb451e52853875bd5baeaf63f78b1` |
| `source-map.json` SHA-256 | `37ecec06edec36b10e7c9630841b369b016c608844e174c06892463e3fc7bec2` |
| `INPUT-MAP.json` SHA-256 | `91f26a1052f22410925bf6d94328295d266c09236ce948c24cddd2aa546c809f` |
| `compile-command.json` SHA-256 | `d47042dd268c8235ed10b33bdb1f0154aa082f05125b63911de56a2504b172d6` |
| Executable | `small_aggregate_host.exe`, 6,630,400 bytes |
| Executable SHA-256 | `a9438205bbb091623f12bd10a7e9a0a2b437c873003fec3cb000c7d8dbbd7a05` |

The outer attempt file's exact status and result digest agree with RESULT;
original and saved selection files hash to the chosen selector, and no
`FINALIZATION-FAILED.json` overrides the reported outcome.

All three original source files **and** actual saved source copies were freshly
hashed and byte-counted against the selector/source/input maps:

| Source | Bytes | SHA-256 |
|---|---:|---|
| `aggregate_small/build_snapshot.py` | 17801 | `e3f2fa01c2c3ff0dd427fa1e2004785e2cd6ab6a7b5797246be575a98db82a67` |
| `aggregate_small/aggregate_host.rs` | 20755 | `6644d9a03f25a59089fd735b0e2f2229ec8940dedbe2502568dfd8c6a36d9c25` |
| `aggregate/receipt.rs` | 3631 | `41db7677d40af4fd779159e8442724bff7842b7f4e5745411e5846d8e7678254` |

The source snapshot contains exactly three files. The emitted compiler command
names the saved native source, not the mutable canonical source. Its relative
`../aggregate/receipt.rs` resolves inside that same snapshot to the pinned
receipt helper. Compiler diagnostics explicitly reference this snapshot helper.

I independently rehashed all **1,071 retained runtime pins / 2,320,491,997 bytes**
and all 20 recorded retained-record/helper pins. They match the selected input
map. The actual saved compiler argv equals the reported argv and differs from
the successful retained command at exactly three entries: crate name (index3),
native source path (index24), and output executable path (index26). All compiler,
linker, SDK/relation libraries, other options and library search paths remain
the retained ones. This is one direct rustc/link invocation, not a backend,
checker, relation, Cargo or guest rebuild.

The actual executable and both command logs match their saved lengths/hashes.
Stdout is empty. The 2,022-byte stderr contains four dead-code warnings in the
unchanged receipt helper and no compiler error. No warning-driven source edit
or repeat build is justified.

### Actual closure and accounting

The command completed with exit code zero and no cleanup errors. Its before-job
counters were zero. The final job record is closed with zero active processes,
zero terminated processes and four total worker processes; its counters agree
with RESULT and the command's `job_after`. The retained selected VCTIP telemetry
cleanup is explicitly reported with its exact image/hash and observed exit;
it is not concealed as ordinary compiler work or a proof operation.

| Measure | Snapshot build |
|---|---:|
| Inclusive worker Job CPU | 60.8125 s |
| Disjoint controller CPU | 4.328125 s |
| Known measured CPU subtotal | **65.140625 s** |
| Whole builder wall time through recorded report | 78.2299715001136 s |
| Compiler command wall time | 60.07052540010773 s |
| Job lifetime through closure | 60.44044300005771 s |
| Peak Job private commit | 977,940,480 bytes |
| Pre-report output census | 8,971,959 bytes / 52 entries |

CPU values are not summed across nested command and Job scopes. The reported
controller/worker subtotal excludes the final report/exit tail and does not
pretend to include this independent audit's file hashing. Build memory does not
predict proof memory. The output census explicitly records one pruned Windows
profile cache alias and its in-run target; it is not traversed as new source.
Builder finalization rechecks the selected inputs and output envelope; the
absence of a finalization-failure override was checked independently.

Result fields record zero host execution, guest, proof, networking and
backend/relation/checker rebuild calls. The selected executable is below the
producer design's proposed 8 MiB snapshot-host input bound, but full input
inventory and actual snapshot/proof admission remain separate obligations.

## Stage host: PASS within compile-only scope

Actual run:
`experiments/v5-local-checks/small-aggregate-stage-host-build-01`.

| Binding | Actual value |
|---|---|
| Selection SHA-256 | `049129dacf8b43ea3e4a1796a26098dfb207ddbc80d5c1b49cbfde94fc71fa38` |
| Result status | `PASS_SMALL_AGGREGATE_STAGE_HOST_ONE_LINK_ONLY` |
| `RESULT.json` SHA-256 | `2c201aa68a50ccc93c90f73ae8aba5d924cef858bbec900f858d738b0135e499` |
| `source-map.json` SHA-256 | `a61cbbb6c566df46ccdbcfd1f52ea1e12fc2d7e5ade4fe3988ca5485e17e82b8` |
| `INPUT-MAP.json` SHA-256 | `e590fc9a2da0960ed9c9330eea2960c8ccd848b83c4cd05673762c64e75b1fba` |
| `compile-command.json` SHA-256 | `e0f68d07312d8cf6934667e44494c8ce69cedf335c806bdac018ef9d796e40c9` |
| Executable | `small_aggregate_stage_host.exe`, 68,036,608 bytes |
| Executable SHA-256 | `8f8e444ddd9029906fee60a073a701bdd34c8b095d54f81f2554bfe1e91ad8ee` |

Both saved and original selectors match the result's selected digest; the
attempt file correctly binds RESULT's status/hash, with no finalization-failure
override. The actual source snapshot again contains exactly three files. Each
original and saved copy was freshly byte-counted/hashed, matching selector,
source-map and input-map:

| Source | Bytes | SHA-256 |
|---|---:|---|
| `aggregate_small/build_stage.py` | 17784 | `3b5ebe002fe5b4fb641c2fbe7a8ca7068789778dbc80d86aa2b69db558677eb6` |
| `aggregate_small/stage_host.rs` | 32291 | `975e68dfbc8d091733cee72a18d81fb45617886585f1806fe9425cf4aa847955` |
| `aggregate/receipt.rs` | 3631 | `41db7677d40af4fd779159e8442724bff7842b7f4e5745411e5846d8e7678254` |

The actual saved command and reported argv agree. Compared to the retained
successful snapshot-host recipe, exactly three entries differ: crate name to
`small_aggregate_stage_host`, source to this saved `stage_host.rs`, and output
to this run's `small_aggregate_stage_host.exe`. The unchanged receipt include
resolves within this snapshot and appears at that exact path in diagnostics.
No `--test`, Cargo invocation or SDK/checker/relation rebuild is present.

The stage selector/input map's **entire 1,071-entry runtime mapping and all 20
record/helper mappings equal** those independently rehashed in the snapshot
audit above. I compared every key/value and count, rather than redundantly
rehashing the same 2.32 GB a second time. The stage builder itself also rehashed
its complete exact runtime inputs during preparation and finalization, as
required by its reviewed implementation and successful outcome. The two saved
environment profiles identify identical observed compiler/linker/resource tools.
This is a trusted local build lineage, not a claim of hermetic isolation.

The actual emitted executable and log files match their saved pins. Stdout is
empty; 2,010-byte stderr contains the same four unchanged receipt-helper
dead-code warnings and no compiler error. Source/manifest code compiled; its
behavior has not thereby been executed or qualified.

### Actual closure and accounting

The command exits zero, has no cleanup errors and starts from zero job counters.
The separate final Job record is closed with zero active processes, zero
terminated processes and four total worker processes; counters agree with RESULT
and command `job_after`. The selected owned VCTIP cleanup is explicitly logged
with exact image/hash and observed exit, as in the snapshot build.

| Measure | Stage build |
|---|---:|
| Inclusive worker Job CPU | 71.9375 s |
| Disjoint controller CPU | 4.234375 s |
| Known measured CPU subtotal | **76.171875 s** |
| Whole builder wall time through recorded report | 77.82257659989409 s |
| Compiler command wall time | 73.66611790005118 s |
| Job lifetime through closure | 73.78105459990911 s |
| Peak Job private commit | 1,233,174,528 bytes |
| Pre-report output census | 76,099,400 bytes / 52 entries |

The same final-report/exit-tail and independent-audit exclusions apply. The
reported output census discloses the one pruned in-run Windows profile cache
alias. No host execution, guest, proof, network or backend/relation/checker
rebuild call is reported. Both runs satisfy their selected 240-worker-CPU,
300-worker-wall, 3072 MiB, six-process and enclosing controller/output limits.

The two builds' known CPU subtotal is **141.3125 seconds**. Their recorded builder
wall durations sum to **156.0525481000077 seconds**; this is not a claim about
the complete project's elapsed time or the unmeasured gap between dispatches.
Do not add nested command CPU again or infer prover memory from linker memory.

## Claim boundary

Both compilations pass the stated binding/closure audit. This establishes
neither actual po18 capsule completion nor proof-stage behavior, memory
sufficiency, a genuine A certificate, mathematical admission, growth advantage
or final-v5 readiness. There is no automatic runtime or proof continuation.
