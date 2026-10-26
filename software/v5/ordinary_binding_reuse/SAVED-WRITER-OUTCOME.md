# Retained Std writer: independent saved-outcome audit

2026-10-26. `current_acceptance_challenge`. **PASS: one successor-only inert
binding completed within the selected limits.** This is not recovered public
production, independent mathematical acceptance, recipient qualification or a
matched speedup result. The old `std-export01` remains failed.

Reviewed saved outputs only under
`experiments/v5-local-checks/binding-saved-writer01`; no reader/code re-review,
product import, binder rerun, native execution or state access. Saved selection
matches `412dd6bf0220eb98b03e1746295f840a5eda47a0af42b98bf299f5daa8578299`.
All **four source snapshots and ten external pins** independently rehash unchanged.

## Result and independently checked correspondence

The pinned diagnostic reports one binder call and PASS for 2,651 units targeting
the actual `Std.HashMap.isEmpty_insert`. Independent inspection of the saved
468,097-byte manifest confirms 2,651 unique well-shaped IDs, the selected semantic
ID, exact target-unit membership and these batch counts/byte sums:

| Batch | Units | Portable evidence bytes |
|---|---:|---:|
| 1 | 1,024 | 9,997,243 |
| 2 | 1,024 | 17,147,916 |
| 3 | 603 | 17,767,684 |
| Total | 2,651 | 44,912,843 |

The returned aggregate additionally records 1,143,590 nodes, 2,821 names,
43,120 import rows, 698,055 binding bytes and 38,097,072 native-array bytes.
These are binder census observations, not independently re-decoded complete proof
data. Import-row counts need not equal the native export's differently defined
dependency-edge counter. Per-batch node/name/edge values were not retained;
the reviewed unchanged partitioner enforces their limits.

The diagnostic reports exact byte-for-byte agreement with all 708 retained
partial units. Independently rehashed those files and checked every file's raw
hash/length against its corresponding new manifest entry: zero mismatches.
Their 6,389,257 bytes still produce the selected map digest
`82df4b3e84e8e53a21ab87f94507f0ba8ecbf8c82fbc6fad1e3b0459d6bae4d0`.
Only manifest and 2,593-byte summary were saved in `binding/`; no complete unit
bundle was materialized. The original failed run still has no manifest.

## Costs and closure

The supervisor reports zero exit and `COMMAND_EXITED_ZERO_AND_CLOSED`, direct
child reaped, Job closed, zero final active/terminated processes, no termination
request or cleanup errors. Stdout is 379 bytes; stderr is empty. Cumulative
process count 2 does not mean two simultaneously active processes.

- Whole operation: **31.7699972000 wall seconds**.
- Inclusive Job CPU 31.078125 + runner 0.234375 = **31.312500 known CPU seconds**.
- Peak Job private commit: **620,498,944 bytes**.
- Timed binder alone: **28.5343803000 wall / 28.125000 process CPU seconds**.
- Diagnostic process total: 31.4472038001 wall / 31.015625 CPU seconds.

Do not add nested wrapper CPU again. Inner 90-wall/70-CPU and outer
120-wall/90-CPU/1792-MiB/one-active-process limits were unchanged. The earlier
public producer's controller timing includes different phases, including partial
file materialization, so subtracting these timings would not measure speedup.
No comparative peak-memory improvement is established either.

## Saved identities and decision boundary

| File | SHA-256 |
|---|---|
| `RESULT.json` | `187e90b6396b7ef6477f1f473eae2996152ad6e6825f7dd2514712cf10fe0124` |
| `command/stdout.txt` | `103ed7a6b965ee6f8a8813f6b8f200e8884362ca0a5ee05994b9c51536811299` |
| `binding/manifest.json` | `1de776b3d131c8c1be3414ed0e0cf066ebd05caebbcd1cf1b6ca80853962e59c` |
| `binding/summary.json` | `7ee48a0939a103a68b142bca37292beb3f2f3114a676ef4af7b454424d5a1d3d` |

The observed improvement in evidence is concrete: the new binder completed this
retained closure as three bounded inert batches, with its exact cost and partial
correspondence recorded. It does not show that full public evidence writing,
intake, native checking, cold module realization or warm ordinary-library use
finishes. No follow-up experiment, larger allowance or old-run relabeling follows
automatically. All used bytes stay frozen; root chooses the next useful boundary.

