# Aggregate stage-host build: independent saved-outcome audit

Disposition: **PASS_ACTUAL_ONE_LINK_BUILD_ONLY**. This is compilation/linking
evidence, not a host-execution, proof-production, native-admission or v5-release
pass. Root reports session49187 terminal exit0; this audit independently inspects
the saved selection, source snapshots, executable and terminal accounting. It
does not poll a process or execute/import project code.

## Exact selection and output

Canonical root throughout: `E:\Distributed Trustworthy Mathematical Knowledge Network`.

- Selection: `experiments/v5-local-checks/aggregate-stage-host-build-01-selection.json`,
  292,269 bytes, SHA256
  `fde4496bea48c5682116c5f2bf7e37bf7834fb422a4abef04b43867dee709326`.
  The saved `selection.json` has the same length and hash.
- Output: `experiments/v5-local-checks/aggregate-stage-host-build-01`.
- `RESULT.json`: 10,271 bytes, SHA256
  `10cbdd0cc233aefb6797c0d8d7756f2bd79030fa7e3f9619208006b11a1dd8db`.
- Adjacent attempt SHA256
  `c812af324580f9227b42cc09f07cdd9a918fd9928444d1fe19d68247434f3050`;
  it binds that exact result and `PASS_AGGREGATE_STAGE_HOST_ONE_LINK_ONLY`.
- `aggregate_stage_host.exe`: **67,992,064 bytes**, independently hashed SHA256
  **`1266b6c990fc21f04f80f88c714a22d7841e4819c64bee0746992a47858a32ac`**.
  Its presence/hash is not evidence that it has been run.

## Source and retained-tool correspondence

Read the selected builder completely and reuse the unchanged SDK/native-source
assessment in `AGGREGATE-BUILD-REVIEW.md`. Independently checked the lengths/hashes
of both current and snapshotted copies of all three selected sources:

| Source | Bytes | SHA256 |
|---|---:|---|
| `software/v5/aggregate_production/build.py` |17,828|`a1d2c22427ffa9f8293813ac76359f9cdde6a3f73870c75a209dad2310bc781a`|
| `software/v5/aggregate_production/stage_host.rs` |22,515|`5865e6afb30bd81adb79d6fe04e09ac8bb7238b40956284fa3bcd2d4da4fe102`|
| `software/v5/aggregate/receipt.rs` |3,631|`41db7677d40af4fd779159e8442724bff7842b7f4e5745411e5846d8e7678254`|

Total: 43,974 bytes. `source-map.json` and `INPUT-MAP.sources` agree exactly.
The 1,071-entry selected and actual runtime maps agree with zero differing
entries; recorded retained bytes total 2,320,491,997. This audit deliberately
does **not** rehash that complete 2.32 GB tree: the builder's before/after pin
checks and earlier exact-map review are retained evidence, not a new independent
full-runtime hash campaign. All 15 helper pins and all five retained input-record
pins were independently hashed and match.

The actual command, saved `compile-command.json` and RESULT argv agree. Against
the retained snapshot-host command both argv vectors have 65 elements and only
three positions differ: index3 crate name `aggregate_stage_host`, index24 the
new snapshotted stage-host source, index26 the new executable destination.
Seven extern libraries, 14 `-L` entries, Rust/compiler/linker, optimization and
fat-LTO settings are unchanged. No Cargo/checker/relation/backend rebuild occurred.
Environment is explicitly selected (`no_inherited_environment:true`) with fresh
run-local temp/profile/cache locations. Cargo environment variables are not
evidence of a Cargo invocation.

## Actual closure and resource scope

One compiler command: label `aggregate-stage-host`, phase
`aggregate-stage-host-link`, PID31956, started
`2026-10-17T03:53:13.464567+00:00`. Saved status `COMMAND_COMPLETED`, exit0.
The command object exactly agrees with the object nested in RESULT.

| Quantity | Observed |
|---|---:|
| Inclusive worker Job CPU |71.1875 s|
| Disjoint controller CPU |5.15625 s|
| Known disjoint CPU total |**76.34375 s**|
| Overall wall |97.44856119994074 s|
| Compiler-command wall |74.18063790001906 s|
| Phase wall |74.32751660002396 s|
| Peak Job private commit |1,228,017,664 bytes|
| Total Job processes |4|
| Final active / terminated processes |0 / 0|

The worker CPU splits into 67.15625 user plus 4.03125 kernel seconds. Job closure
is true and cleanup-error lists are empty. There **was** the selected cleanup
of the owned, hash-pinned MSVC telemetry process `VCTIP.EXE`, PID32580, with exit
observed. This must not be described as absence of all cleanup actions. It is
not recorded as a Job forced termination. Root reports no live process remains;
this reviewer did not perform process polling.

Limits were worker240CPU/300wall, controller40ordinary/60totalCPU,
420totalwall, 3072MiB, six processes, 512MiB/8192 output entries and 1MiB logs.
All saved values are within those limits. Accounting explicitly excludes the
final report/exit tail; the known total is not falsely presented as exhaustive
machine energy or all elapsed-process accounting.

The pre-result census is 52 entries / 76,036,828 bytes. Independent final census
is **53 entries / 76,047,099 bytes**, exactly adding RESULT's one entry and
10,271 bytes. The walk prunes the single recorded reparse-point path
`profile/AppData/Local/Microsoft/Windows/INetCache/Content.IE5`; it does not follow
that alias. The adjacent attempt is outside the run census. No archive bytes
or `FINALIZATION-FAILED.json` are present. This final census is not a claim
that every transient peak was continuously observed.

Stdout is empty; stderr is 2,006 bytes and contains four dead-code warnings in
retained `receipt.rs`, no compiler error. Their exact hashes match command logs.

## Saved small-file pins

| File under output | SHA256 |
|---|---|
| `source-map.json` |`834a3eb0a9547b235d8ea4ff3440f9536b2d0d0a15e753f1739837bc078455fe`|
| `compile-command.json` |`9d98335db2e8364e2fe0099e71113812162f75c44b111d6ebb9717afe47b259a`|
| `INPUT-MAP.json` |`3cf78b8fb1206620ffeb75030963c41ff520c8c10dd7459df1978574a3efffad`|
| `aggregate-stage-host-link-job.json` |`5530f16f022d260fcd64d76c8610eae34a8db4c1ac4bc0b95df58e9532961836`|
| `commands/aggregate-stage-host/command.json` |`e3cd818fa21e29c7a3cb12117263a0c24fb440bbb6be6c986c3aef1f3c9eabbd`|
| `commands/aggregate-stage-host/stdout.txt` |`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`|
| `commands/aggregate-stage-host/stderr.txt` |`2fc3be5cd6d4cd9687e7f4338a5ac29a3ae88c2ed467793521857ff1f6e9ecfd`|

## Consequence and exclusions

The selected stage host now exists as an exact independently pinned compiled
artifact. This removes the build obstacle only. RESULT explicitly records
zero host, guest, proof and network calls and zero backend/relation/checker
rebuilds. No receipt was produced or accepted. Any subsequent stage requires
its own source-feasibility decision and finite allocation; the current po19
prover-memory question cannot be inferred away from successful compilation.
