# Restricted support: actual native build audit

2026-10-21, independent growth reviewer. **PASS, build only.** No controls,
guest execution, proof generation, product adoption or v5 completion is implied.

Evidence: `experiments/v5-local-checks/restricted-support-build-01`.

- `RESULT.json`: `e26e29de72363e5c0873b9e0c307d3efaaeca4cc5e02144821446b1a06225392`.
- Original and saved selection both match
  `a6bbb29061cc301a85e258a5c9f84c6c0bd8be644ff84b389d23b6575b47e0f5`.
- The sibling attempt binds that exact RESULT and
  `PASS_RC_SUPPORT_TWO_COMPILES_ONLY`; no `FINALIZATION-FAILED.json` exists.

## Changed-boundary checks

Reused the adopted source/recipe reviews; did not repeat dependency or SDK
audits. Independently hashed all eight selected canonical sources and all eight
fresh snapshot files. Their sizes/hashes equal both selection and source map;
the snapshot contains exactly these eight files.

Both actual argv arrays equal `compile-commands.json` and their individual
`commands/<label>/command.json` arrays. They invoke the selected rustc exactly
twice: `support-core`, then `support-controls`; both completed with exit 0.
The new core uses the retained module-relation dependency. Controls explicitly
link the new `dmkn_rc_relation` and the retained old core as `dmkn_rc_baseline`;
the baseline library is 1,719,004 bytes with SHA-256
`1bdfd6a0943b6a09248ae99aefd793b63384a957bf8d98c0cd8d8b430fd04a0b`.
Its retained RESULT matches the selected
`24e8ebf8f774e22ec19c7172dca0a56efb81ad653e609445ae0e5d030e2233dd`.
No Cargo invocation, test/native execution, guest/proof/network call or
checker/module/dependency/baseline/aggregate rebuild appears in this build.

Independently checked all four command-log pins. Core logs and controls stdout
are empty. Controls stderr is 5,473 bytes,
`69d274e1bca4208611784f68d176c0c26c484b5e92b9d6b331f6b38e565a116c`;
the complete content contains ten unused/dead-code warnings, no error.

| Actual output | Bytes | SHA-256 |
|---|---:|---|
| `libdmkn_rc_relation.rlib` | 1,740,576 | `3d621f5be7433e23ac31bd8bf7d9b6713c913d33809bd7074a72592a05843fce` |
| `restricted_support_controls.exe` | 996,352 | `50b8952c5cfef085980075edb9e852150136abbcd2142934ac749216f62b774c` |

Both output pins were independently recomputed from the actual files.

## Accounting and closure

The two inclusive worker increments are 5.171875 and 25.34375 CPU seconds,
which sum to the terminal Job's 30.515625. Controller CPU is separately
2.328125: **32.84375 known CPU seconds**, without nested double counting.
Total recorded wall time is 34.9881431 seconds. Accounting explicitly excludes
the final report/exit tail; it is not a claim of complete machine-level cost.

The Job is closed with zero active processes, zero terminated processes and
no cleanup errors. Its six total processes and 746,168,320-byte peak private
commit remain within the selected six-process/1,024 MiB ceilings. Worker and
controller CPU/wall remain below the selected bounds. The sampled output census
is 2,843,276 bytes / 57 entries, below 128 MiB / 1,024 entries; this is a sampled
output measure, not a continuous disk high-water guarantee. Logs fit 1 MiB.

The selected owned VCTIP telemetry cleanup records observed exit and its pinned
image; the only pruned profile alias targets the same fresh profile's INetCache.
No unexpected cleanup or terminal failure is recorded. Resource containment is
not a hostile-input security sandbox.

The narrow next decision is whether root selects the already-reviewed native
controls against these exact output and fixture pins. This audit did not run
them and does not establish the support optimization's measured benefit.
