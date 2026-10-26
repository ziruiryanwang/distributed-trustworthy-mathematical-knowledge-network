# One complete materialization from the retained Std writer

Source only until root independently selects execution. This is test-only input
preparation for an existing public consumer, not another producer, native export,
baseline acceptance, recovered production or software release. All previous
sources, diagnostic outputs and failed production files remain untouched.

## Reuse and precise change

The frozen diagnostic is actually named
`ordinary_binding_reuse/measure_saved_writer.py` (not `check_saved_writer.py`).
The new `materialize.py` loads its exact 8,449 bytes, SHA-256
`42670eb615d3ba69140804ce8af593a4f984d283156dfbab08a589684ceecd1c`,
and reuses its pinned input loading, frozen dependency modules, adopted binder,
708-partial census and exact comparisons. Its old `main` never runs.

The adopted binder remains
`e4b52c2f2e823cc98aa37c8cc7adb0cf79952def9c19b54d7072116a39fa19b6`.
No binder/decoder/kernel algorithm, native input or acceptance rule changes.
One binder call is necessary because the successful diagnostic retained only
its manifest/summary, not the complete 2,651 portable unit byte strings.

The new behavior is exclusive writes of all complete unit bytes, immediate
readback, exact final directory/file census, and the existing manifest committed
last. No second validation/binding pass or 2,651-file backup is created. The same
already-validated bytes retained by the binder are used for writing and for
exact comparison with the 708 historical partials.

## Fixed inputs and output contract

Inputs come from the preserved `std-export01/bundle` under
`experiments/v5-local-checks`:

| Input | Bytes | SHA-256 |
|---|---:|---|
| writer.json | 38,154,768 | 5a2f721127cfef3ae39613c1ec723b2f710cc410c872650fb2acfd7d04078b7a |
| inventory.json | 823,690 | c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0 |
| request.json | 496 | bcb647fa96824cc82aebda1dab151a88d678ca3d8756cd150e0103e9f41993bd |

The saved adopted manifest is
`experiments/v5-local-checks/binding-saved-writer01/binding/manifest.json`,
468,097 bytes, SHA-256
`1de776b3d131c8c1be3414ed0e0cf066ebd05caebbcd1cf1b6ca80853962e59c`.
The newly bound raw manifest must equal those exact saved bytes. Its required
batch pairs (units, portable bytes) are (1024,9997243), (1024,17147916),
(603,17767684), totaling 2,651 units and 44,912,843 evidence bytes.

The 708 old partials are checked before binding, compared byte-for-byte with the
new binding, and checked again after writing. Their unchanged 6,389,257-byte
aggregate remains
`82df4b3e84e8e53a21ab87f94507f0ba8ecbf8c82fbc6fad1e3b0459d6bae4d0`.
All eight helper input pins and the saved manifest/helper pins are rechecked.
Immutable approved local inputs are a premise; these checks are not protection
against arbitrary concurrent account-level filesystem attacks.

Only a fresh `{output}/materialized` child of the selected supervising run is
created. It contains exactly:

- `units/<UnitID>.json`: 2,651 complete files, each with the saved manifest's
  exact length/hash and exclusive creation; no overwritten partials.
- `MATERIALIZATION.json`: bounded metadata, exact target names/ExportIDs/UnitIDs,
  semantic ID, input identities, census, partial correspondence and costs.
  Its status is `PREPARED_FOR_MANIFEST_NOT_COMPLETION`.
- `manifest.json`: the exact saved 468,097-byte manifest, written last.

No writer/inventory copy, native program, owner/catalog/custody operation,
ordinary project registration or network request occurs. Output is about 43.3
MiB plus small metadata, not another copy of a full native installation.

After manifest write, perform complete output census/hash checks, without writing
another required file. Manifest presence or prepared metadata alone is not
success. The terminal stdout must report
`MATERIALIZED_INERT_BASELINE_NOT_ACCEPTED`, with exact manifest/report pins and
2,653-file census. Root must also adopt the existing outer runner's exit-zero,
fully closed result, no cleanup errors and unchanged selected inputs. Failures
preserve every partial output; there is no cleanup, automatic retry or promotion.

## Finite selection, without another harness

`select_materialize.py` produces only a fresh existing-runner selection. It
accepts `--name` and independently reviewed `--materializer-sha256`, and runs
from the canonical root using the selected Python `-I -S -B`. It does not import
product code, invoke the materializer, or create a run directory.

It reuses the exact adopted saved-writer selection
`412dd6bf0220eb98b03e1746295f840a5eda47a0af42b98bf299f5daa8578299`:
ten retained external pins (three Python runtime, four frozen helper modules,
three saved writer inputs), adding the exact saved manifest and old selection
as two provenance/input pins. There are **12 runtime pins and six sources**:
existing `tools/Run-V5-Check.py`, materializer, selector, this plan, frozen
saved-writer helper and adopted binder. The 708 partials are individually checked
inside the operation against their fixed aggregate identity; they are not 708
additional runner pins exceeding its 256-entry bound.

The direct selected argv is:

```text
D:\Python314\python.exe -I -S -B
  {snapshot}\software\v5\ordinary_std_intake\materialize.py
  {output}\materialized
```

The existing runner snapshots the six selected sources and checks its external
pins before and after the one command. The helper's own source root resolves
inside that snapshot, so the binder is the selected snapshotted source rather
than an unpinned development import. No new execution framework is introduced.

## Budget and accounting

Retain the diagnostic's finite limits unchanged:

- Inner cumulative 90 wall / 70 process CPU seconds, including new writes,
  readback, final census and all reused helper work.
- Existing outer Job: 120 wall / 90 CPU seconds, 1,792 MiB, one active process,
  262,144 stdout bytes and 131,072 stderr bytes.

The retained binder measured 28.125 process CPU seconds; the complete old
diagnostic used 31.3125 known CPU / 31.7700 wall seconds and 620,498,944 peak
Job private bytes. About 44.9 MB of fresh unit output/readback and directory
census is the new workload. These facts justify trying the unchanged substantial
headroom once, not asserting a completion prediction. No memory/time cap is
raised; a slow filesystem may still refuse. Each file is flushed/fsynced before
readback, and those costs belong to this operation.

Report outer inclusive Job CPU plus its separate wrapper CPU as whole known cost;
do not add the nested binder measurement again. Inner limits are cooperative;
the existing outer Job contains the process. Neither is a hard filesystem quota
or hostile-code sandbox. No running experiment is authorized by this plan.

## Next gate is separate

Only an independently reviewed complete result may supply the public intake
plan. That later operation must separately initialize/select a genuine protected
parent and independently check its three batches under its own prospectively
reviewed allowance. It receives the materialized directory, actual manifest path
and hash, and exact target rows. No old producer success flag or binder result
is mathematical authority. Root alone selects that later operation.
