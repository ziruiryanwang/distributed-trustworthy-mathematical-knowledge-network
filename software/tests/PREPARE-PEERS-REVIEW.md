# Independent PREPARE source and exact-launch review

Correction notice: the original launch-02 exact-order claim and resulting launch clearance below were incorrect. They are preserved as historical review statements, not current findings. The appended **Ordering-audit correction and launch-03 delta review** supersedes them.

2026-09-21. Source-only and read-only filesystem review of `prepare_peers.py`, [PREPARE-PEERS.md](PREPARE-PEERS.md), and the exact launch `../qualification/peer-prepare-launch-02.json`. The reviewer did not import, execute, compile, open SQLite, invoke Lean, bind a port, create product state, or start a service. Only this review note was authored for this assignment. Root retains execution and outcome-review responsibility.

## Disposition

**No source/interface or exact-launch blocker found for this finite trusted-owner PREPARE cut.** The verdict applies to launch 02 and the final coordinator pin below. It is not an execution pass or permission to reuse failed roots, retry, expand the allocation, begin authoring, start services, or claim reciprocal knowledge generation.

The cut has exactly ten direct public commands, two fresh support-build stages and two native bootstrap stages. It produces two separately installed/initialized same-host states, not an independently operated network. Its accounting openly excludes unmeasured wrapper CPU and lacks outer OS containment; those limitations are part of this narrow disposition, not findings that a full resource sandbox exists.

## Resolved review finding

The first coordinator compared the *resolved* source-pin paths to the exact inventory but later computed copy-relative paths from the original textual spelling. A noncanonical owner-supplied spelling containing `..` could therefore pass resolved inventory comparison while deriving an unintended copy target. The concrete launch 01 used canonical paths and did not trigger that case, but root corrected the general mismatch before any execution.

The copy loop now uses `source = safe(source_pin["path"])` before `source.relative_to(SOURCE)`. `safe` rejects reparse ancestry and returns the resolved existing source path; the inventory comparison and relative-copy calculation therefore use the same canonical source. In the reviewed immutable-source premise, the result is a strict product-relative target inside the selected installation.

Read-only reconstruction of the prior line reproduces the exact prior coordinator SHA-256 `B614BF1ED2FE1D2D05DAC71881BFE63CB34A2B6E30D65E7F39C0DAC0A7124A12`, confirming this was the sole code delta after the full initial source reading. Launch 01 remains preserved and unexecuted; launch 02 differs only in the coordinator pin. The 96 product source pins, runtimes, ports and limits are unchanged.

## Exact launch checked

All **99 file pins** were independently rehashed and length-checked: 96 product source/asset files, the coordinator, Python executable and Lean executable. No mismatch was found. The 96-file source set and its exact product-relative POSIX ordering match the coordinator's inventory rule, totaling **3,401,790 bytes**. Its composition is 16 Python files, 3 Lean sources, 68 canonical-object files, 8 JSON files and the installed `API.md`.

There is no experimental-source path or copied `.olean` in that inventory. It includes the revised original-attempt association in `node.py`/`storage.py`. The source tree's old build outputs, qualification results, tests, runtime, databases and accepted handles are not copied into either installation.

Every supplied file path was canonical at review time. Read-only ancestry checks of the 99 pins covered 116 distinct existing filesystem paths and found no reparse point. Both new target roots were absent:

- `E:\Distributed Trustworthy Mathematical Knowledge Network\software\qualification\peer-01`
- `E:\Distributed Trustworthy Mathematical Knowledge Network\product-local\peer-01`

The qualification and product-local parents existed. These are observations at review time; the coordinator repeats fresh-root and pin checks before writing, and exclusively creates the two roots. Existing siblings and failed-run material are never removed. A concurrent owner mutation invalidates the immutability premise rather than becoming permission to overwrite data.

| Selection | Reviewed value |
| --- | --- |
| Interpreter | `D:\Python314\python.exe`, 106,208 bytes; all children use `-B -E -s -S` |
| Shared Lean runtime | `software/runtime/lean-4.34.0-windows`; selected `bin/lean.exe`, 83,456 bytes |
| Ports | alpha 43171, beta 43172; aliases point to the other installation |
| Direct-command polling deadline | At most 500 seconds, reduced to remaining aggregate wall allocation |
| Aggregate checkpoint limits | 1,800 seconds active wall; 1,800 seconds *observed subset* CPU |
| Retained-byte success bound | 1,073,741,824 bytes, excluding the shared external runtime |

The simultaneous port bind is a future coordinator preflight, not something this reviewer performed and not a lasting reservation. Failure to bind either frozen port stops preparation; there is no alternate-port retry.

## Work and public-interface correspondence

For each of alpha and beta, the coordinator snapshots the same raw owned sources/assets into a separate `install`, then uses only that installation's public `build.py` and `manage.py` entry points. State, scratch and build-work are independent sibling directories outside install and the shared runtime.

| Per-node command | Required outcome | Native work |
| --- | --- | --- |
| `build.py` | Fresh support receipt and outputs bound to the completed local stage | One support-build stage, two source compilations |
| `manage.py configure` | Exact install/state/scratch/runtime domains, clients `local` and `reviewer`, no offered theorem packages, fixed peer alias | None |
| `manage.py request` / `init` | Actual checked initial contexts for both local labels | One ledger-charged bootstrap stage |
| `manage.py request` / `info` | Same local context/description as initialization | None |
| `manage.py request` / `find` | Complete empty P1 enumeration at the reported snapshot | None |

The two labels within each node share its checked bootstrap result; they are not two extra independent native bootstraps. In total there are two support-build stages containing four Lean compilations, two native bootstrap stages, and six supervised public node calls. The coordinator checks exactly ten direct commands and the expected stage totals before success.

Current `build.py` refuses reused work/build directories and binds copied support outputs to the actual stage output list. Current `manage.configure` authenticates the fresh build and local source bindings, emits empty offers, and uses real domain/configuration validation. `Checker.bootstrap` copies and checks the installed common packages and invokes its actual native description/replay gate. The coordinator does not manufacture receipts, copy an old database, directly append registry rows, or implement a private acceptance bypass.

Public author packets contain only actual initialized descriptions/handles, the empty enumeration, installed interface/config paths, installed API pin and evidence bindings. No theorem statement, proof skeleton, source submission, contribution or future investigation is supplied. Config creation and source compilation are not conflated with mathematical acceptance; only the actual receiving bootstrap may establish the limited initial context.

## Evidence and accounting checks

Build success requires the public response to bind the installed build receipt, which in turn binds the expected request-local stage receipt. The stage must report the two successful compile steps, `children_quiescent:true`, and a final empty Job. The coordinator's extra checks do not replace the product build gate's source/output authentication.

Each public request must create exactly one new scratch call directory. Its actual node supervisor and event must bind the exact saved request and returned response bytes. The coordinator checks successful supervisor status, reaped direct child, final active-zero flags/counter, the expected checker/stage behavior, and `event.origin_directory` equal to that exact call directory. This ties evidence to the freshly created call rather than merely accepting a matching operation name.

The direct command's early `result.json` records the wrapper outcome before deeper checks. The later binding files and final PREPARE result add authenticated build/public quiescence. A successful configure process has no independent process-tree observation and is explicitly marked `NOT_INDEPENDENTLY_OBSERVED_CONFIGURATION_ONLY`; it is not silently equated with the native/public supervisor records.

Observed CPU is coordinator process CPU plus each successfully bound build-stage Job and each successfully bound public-node Job, each once. Public node Job CPU already includes nested bootstrap work, so the bootstrap receipt is not added again. Direct build/manage/configure wrapper CPU and Jobs whose final receipts cannot be bound remain unmetered, with `cpu_complete:false`. An observed sum below 1,800 seconds is consequently not a complete aggregate CPU upper bound.

The coordinator and direct wrappers have no new OS memory/CPU container. Existing product runners/supervisors contain their respective inner child trees. Per-command deadlines and output limits are polled; the 500-second number is not an independently enforced OS deadline or a measured end-to-end bound on final hashing/report serialization/cleanup. Aggregate wall/observed-CPU checkpoints continue during source copying, commands and final censuses. Root's bounded monitoring remains necessary, and cannot by itself establish descendant cleanup after a forced stop.

The final retained-byte census covers the two new roots only, with finite entry/depth bounds and streamed hashing. A 16 MiB reporting margin is reserved, then exact serialized seal/result lengths are included in the final successful byte check. The declared accounting endpoint excludes final serialization/write and stdout; the historical censuses correctly do not pretend to include their own later-written report files. This is not a hard transient disk-block or total-host quota.

## Failure and claim limits

Any failed command, mismatched receipt, refused public operation, quota observation or exhausted allocation stops the whole cut without retry. All newly written material is retained. Direct-process kill/reap is not treated as proof that nested descendants are quiescent; failure records explicitly retain that uncertainty. Preparation neither clears a pending request nor attempts native/request recovery. Before any later action against failed state, root must inspect the retained original-attempt/process evidence rather than assume the state is ready.

The shared Lean and Python distributions remain trusted deployment units. Executable pins do not authenticate all adjacent libraries, standard modules or runtime configuration. Separate same-host paths do not make the old checkout unreadable and do not prove independent ownership or independent-host operation. Successful preparation would establish neither peer acquisition nor offline admission of another node's result, source authorship, publication, useful reciprocal accumulation, failure recovery, or scalable growth.

The required success label, `PREPARED_TWO_INSTALLATIONS_AWAITING_INDEPENDENT_AUDIT_AND_LOCAL_AUTHORING`, is appropriate. Actual output/receipt/state inspection remains necessary after the run. No such outcome is asserted in this review.

## Final reviewed pins

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `tests/prepare_peers.py` | 25,349 | `1CB723AF882F4E3FBB4C65425534CDD3AC9668AECF4DFAEF2C05A8EE9B33C660` |
| `tests/PREPARE-PEERS.md` | 8,088 | `7D7701C42E1A9F38AE97B3D7E744E9665A74ECB72669D624B67C3C240AAB42AE` |
| `qualification/peer-prepare-launch-02.json` | 29,043 | `FDFE4B7307D7F41956BFEAFEC5637297E707A806FEBE4E22F7D233B7D75EA56E` |
| Preserved unexecuted launch 01 | 29,043 | `3B96881D5C4FA06C6DCCAB6999B89129739AC31694AE01BDB6E1FFD2F08005C7` |

Launch 02 records every exact source/runtime executable pin. In particular it selects node hash `CC9ACD8B5E2E9E2957A9C56908A4F7CC1BBBE9A1D628D32B40100F9278A78AB0`, storage hash `1D815B3C5CAA8209FB5F0811B4ED2FA9588240727DB0EF2E0512B6BA4C1A2DBF`, Python hash `03168C01B7B7491423350E82C26FEE71F35B43694D1319D3C668BDA6903A0C38`, and Lean executable hash `A8040E2CAB341C12116AB591FED9F761816F5F6B08554F6CC1680E86DFBBA0A2`.

## Ordering-audit correction and launch-03 delta review

Later on 2026-09-21, root's actual launch-02 invocation stopped with `STOPPED_BEFORE_RUN_CREATION: SOURCE_PIN_SET_ORDER`, exit 1. Root's retained [failure note](../qualification/PREPARE-LAUNCH-FAILURE.md) records 0.2247984 seconds, zero product commands/build/native stages/services, and no created evidence/data roots. This is a failed preparation preflight, not a mathematical refusal or a successful preparation. The reviewer read that note and independently confirmed both roots remain absent; the reviewer did not execute the coordinator or Python during this correction.

**The reviewer's original exact-order claim was wrong.** The earlier read-only audit used PowerShell `Sort-Object -CaseSensitive`, which still performs culture-sensitive collation. It repeated the launch generator's ordering assumption instead of independently reproducing Python's lexicographic key order. A matching file set and matching individual hashes do not establish matching order.

The corrected independent audit enumerated the source set again, constructed product-relative paths with `/` separators, converted them to an explicit `string[]`, and sorted with `[Array]::Sort(paths, [StringComparer]::Ordinal)`. Every relative path in this selected inventory is ASCII, so .NET ordinal comparison agrees with Python's code-point lexicographic comparison for these exact strings. Each supplied path was compared at its exact index using `StringComparer.Ordinal.Equals`; no culture-dependent sort was used.

This check reproduces the old failure: at zero-based index 1, launch 02 supplies `assets/common/ext/manifest.json`, while the coordinator requires `assets-lock.json`. That file is at index 76 in launch 02. The first two required entries are `API.md` and `assets-lock.json`.

Root created a separate launch 03, preserving launch 02 and the failure record. Narrow delta checks establish:

- Launch 03 has exactly the same 96 source records, paths, lengths and hashes as launch 02, totaling 3,401,790 bytes; only their array order changed.
- Its exact 96-position sequence now matches the independently ordinal-sorted expected inventory, including `assets-lock.json` at index 1.
- Schema, coordinator, Python, shared runtime, ports and limits are semantically unchanged. JSON formatting changed, not the allocation or product configuration.
- All 99 selected file pins were length/hash-checked again with no mismatch. The coordinator remains exactly `1CB723AF882F4E3FBB4C65425534CDD3AC9668AECF4DFAEF2C05A8EE9B33C660`; the earlier source-normalization fix is unchanged.
- Both `software/qualification/peer-01` and `product-local/peer-01` remain absent. No failed product state or consumed native allocation is being erased or reset. Root's single separately allocated new attempt is explicit; this is not automatic retry behavior added to the coordinator.

Current narrow disposition: **no remaining source-order or exact-launch blocker found for launch 03 under the previously documented trusted-owner PREPARE limits.** The mistaken launch-02 disposition is withdrawn. This correction does not claim that launch 03 has executed or will succeed, and does not expand the work beyond ten commands, two support-build stages, two bootstrap stages, zero services and zero theorem submissions. Actual preparation still requires a subsequent outcome audit.

| Corrected launch | Bytes | SHA-256 |
| --- | ---: | --- |
| `qualification/peer-prepare-launch-03.json` | 29,043 | `11BE3A60639CD965EAFD555338909FE28CF4C628A7223F63B6D6E2AEAACB0CDA` |

The prior ordering mistake and failed launch remain part of the trace. The corrective audit changes only the unsupported order/launch conclusion; it does not rewrite historical hashes, pretend the failed invocation never occurred, or turn source inspection into runtime evidence.
