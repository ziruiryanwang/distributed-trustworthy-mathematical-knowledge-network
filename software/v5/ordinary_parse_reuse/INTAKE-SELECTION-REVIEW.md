# Exact Std intake selection delta

2026-10-26. `rich_intake_acceptance`. Canonical guard passed; checkpoint is
`research/cycles/v5-2026-10-26-local-discovery/CHECKPOINT.md`. Saved-selection
comparison and small-file hashes only. No selector, product import, owner opening,
native execution or Git action; no repeated source/package/init outcome audit.

**PASS_EXACT_INTAKE_SELECTION_DELTA.** Root retains the separate launch decision.
This is not rich-library acceptance or a prediction that the fixed limits suffice.

## Exact selected inputs

Selection: `experiments/v5-local-checks/std-intake01.selection.json`, SHA-256
`2125ea3708989b3a424c47c3e2a3f56c458254cbe3bfd8d7907cacf538f4cddc`.
The schema/name are `DMKN_V5_LOCAL_CHECK_V1` / `std-intake01`.

I compared it with independently reviewed init selection
`9076770d368ca86a5ea58fa96f22765658c35ac491da394e4690158580848f59`.
All four source rows and all 191 prior external pins are identical; none is
removed or changed. Exactly nine fixed init-evidence files are added, for 200:

| Added file below `std-init01/` | Bytes |
|---|---:|
| `RESULT.json` | 2784 |
| `selection.json` | 46446 |
| `command/stdout.txt` | 1150 |
| `command/stderr.txt` | 0 |
| `public-launch/LAUNCH.json` | 1913 |
| `public-launch/RUN.json` | 1149 |
| `public-launch/SUPERVISION.json` | 2287 |
| `public-launch/child/stdout.txt` | 1564 |
| `public-launch/child/stderr.txt` | 0 |

All nine actual SHA-256 values match the selected pins. The outer init RESULT
is `f15c18645b910fb13a7503ed6a026bb61e2c72c856d7db493a23d40bea5163a6`, matching
INIT-ADOPTION; its saved selection hashes to the reviewed init selection above.
No mutable catalog/custody database, journal or lock is added. The already adopted
INIT-OUTCOME `a3f7002e...` supplies mathematical/event qualification; this check
does not repeat that audit.

## Exact argv delta and limits

The complete intake argv matches the reviewed init argv with only these changes:

- Public wall/CPU/memory values become `360` / `300` / `1536`.
- Operation `init` becomes `intake-baseline`.
- Append `--parent-root`
  `3034986549a52b2a0b46f5fffe2c650879453f43ff85d4ef38cf3ff73b7a7d62`.
- Append `--bundle-directory`
  `E:\Distributed Trustworthy Mathematical Knowledge Network\experiments\v5-local-checks\std-reconstruct01\materialized`.
- Append `--bundle-manifest` with that directory's `manifest.json` and
  `--bundle-manifest-sha256`
  `1de776b3d131c8c1be3414ed0e0cf066ebd05caebbcd1cf1b6ca80853962e59c`.

The selected parent equals both INIT-ADOPTION's actual checked root and the
pinned init child report's `result.basis.local_root`. It is not a guessed or
producer-supplied root. I rehashed the manifest: 468,097 bytes at exactly the
selected SHA-256. The 2,651 inert unit files remain selected/revalidated through
that manifest, not individually rehashed for this selection review.

All other arguments remain unchanged: direct package `run.py`, actual new
PROFILE `37fcb520...`, pinned Python/Lean paths, `owner --`, exact existing
catalog/custody/store/quota, public process cap three and 1-MiB logs each.
No owner `--output`, catalog override, build, exporter or wrapper is introduced.

Outer limits are exactly 420 wall / 330 inclusive Job CPU seconds / 1,792 MiB /
four processes / 4-MiB stdout / 1-MiB stderr. Public limits are 360 / 300 / 1,536
MiB / three processes / 1-MiB logs each. These are the previously reviewed intake
allowances, not an increase following an intake failure. The product retains
its three batches, per-batch 60-CPU/64-MiB output caps and single deadline.

`std-intake01` output is absent at review; the adopted catalog/custody directories
exist. No owner/database was opened. The existing runner will create only its
fresh output and snapshots and recheck selected immutable inputs. Source review,
actual package and init adoption are reused unchanged.

All actual intake success/confirmed-prefix/possible-unreported-commit and complete
cost requirements remain those recorded in PUBLIC-REVIEW and PUBLIC-PLAN. A new
failure must be preserved; no retry, cap change, rollback claim, warm contribution
or additional operation follows automatically from this selection clearance.
