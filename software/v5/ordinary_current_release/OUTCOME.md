# Current-release controls01: saved outcome and narrow correction

2026-10-26. Independent `current_acceptance_challenge` review. Source/data reads
only; no rerun, product import, native operation or protected-state access.

**Overall outcome: FAILED, cleanly closed.** Do not promote the completed archive
substeps to a whole release-gate pass. The used release source, archives, snapshots,
failure and allocation remain unchanged.

## What actually happened

Run: `experiments/v5-local-checks/current-release-controls01`.
Selection SHA-256:
`e294eeb23fab61cdcbca3deab5d0f98aa447ab10e9266fc60e242d85f14c860d`.

The saved outer RESULT records `COMMAND_FAILED`, child exit 1, 11.33799620019272
seconds overall wall time, 4.75 inclusive Job CPU seconds and 0.625 wrapper CPU
seconds. The command's wall-through-cleanup is 9.155837000347674 seconds. Final
active and terminated process counts are zero, the direct child is reaped, the
Job is closed, cleanup errors are empty and no termination was requested. Peak
Job private commit is 139,546,624 bytes. Do not add the nested supervision-wrapper
sample again to the inclusive outer wrapper charge.

There is no `suite/RESULT.json`. `prepared`, `refused-preparation`, future catalog
and future custody paths do not exist. The saved traceback stops at test line 214,
calling the actual relocated preparer, then preparer line 93 and the frozen
helper's `Inputs.read` bound: **`ValueError: KIT_INPUT_BOUND`**.

The saved test snapshot is still the reviewed 15,235-byte file
`fc65a4da6149200f16652fe61cfba3cda82efab1f8aa542a744f44f3218f0beb`.
The failing relocated preparer is the original 6,217-byte file
`8d36fef4c8b50baff5146325ceea83c103c1540b3cbb90b6a8d3c10a71e3bf8b`.
Thus this is an implementation defect in the selected preparer, not evidence of
an unreviewed file substitution or an exhausted CPU/memory allowance.

The executed path reached both archive/relocated-verification stages, all six
file refusals and all four layout refusals before failing. Those predecessor
checks are inferred from the pinned sequential test path and this traceback;
there is no saved terminal ten-refusal result row to misrepresent as a completed
suite. The later wrong-PROFILE and actual exporter-codec controls were not reached.

## Independently checked saved archive artifacts

Both terminal packing receipts exist. This review independently streamed every
ZIP member and hashed every extracted file against its outer manifest, checked
the exact member/file sets, stored lengths, fixed timestamp and file permissions,
and checked the actual archive/manifest lengths and hashes against the receipt.
There are no payload or set discrepancies.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `suite/source/source.zip` | 3,367,110 | `fd4e62b19cf44d28c7aaec098a55255eb06971b42082de9d25e4c3d0b7ba55f0` |
| source `CURRENT-RELEASE-MANIFEST.json` | 16,426 | `d81fda381bf454857e040b53bf850458d766edf1483c97f934b9f194a4a73edb` |
| `suite/prebuilt/package.zip` | 39,481,400 | `29a29165647cf68d57f600391502ba8929c5f1b6bc1fa3270197c87557203cb7` |
| prebuilt `CURRENT-RELEASE-MANIFEST.json` | 24,491 | `f2f564415b8d507e12ad5b9d53f1e18563b950352b27d12906877cefdf1c087c` |

Source has 106 payloads / 107 ZIP and extracted files including its manifest;
prebuilt has 166 / 167. Both bind release
`821796aa5b4996edd3f34babdb3be186d8321e0b3b4208b1e3f18705400caf78`.
These archives preserve exact selected bytes, including the faulty preparer.
They are retained evidence, not the corrected usable distribution.

## Cause and exact source-only repair

The frozen helper's `Inputs` object permits fewer than 12 prior recorded reads.
The new preparer reused its metadata reader for all 45 interface files after
already reading release and PROFILE. It therefore deterministically refuses
interface file 11: ten interface reads plus two metadata reads have filled its
12-read ledger. The helper enforces its contract correctly. The initial source
review missed this inherited reader contract; that review is not retroactively
edited into a successful finding.

The independently checked fresh successor is `prepare_selected02.py`, **6,223
bytes**, SHA-256
`27da75fff176f349f79f28683ec2e8902a5adc619d20ef400f4cc360d0724b78`.
Raw-byte comparison confirms exactly one replacement and no other byte changes:

```python
source = reader.read(package/name, 2*MIB)
# becomes
source = kit.Inputs().read(package/name, 2*MIB)
```

**CLEAR_NARROW_SOURCE_FIX.** Each of the fixed 45 pinned interface files again
uses a fresh bounded reader, as in the frozen predecessor selector. The retained
metadata reader performs eight reads on the successful path: two initial reads,
three pre-preparation checks and three post-preparation checks. The preparer's
own request reader remains unchanged and separate. The 12-read and 40-MiB helper
caps, per-file maximum, exact known-role/pin checks, whole-operation allowance,
report binding, path checks and metadata/helper rechecks are not widened or
removed. The known 45-entry pin set bounds this loop; this is not an unbounded
reader-budget reset for arbitrary inputs. No successful preparation is yet claimed.

## Cheapest sufficient continuation

Root's selected fresh complete **source-input staging root** is appropriate.
Materialize the exact existing input union under its original logical input
paths, substituting only the reviewed successor at the original logical
`ordinary_current_release/prepare_selected.py` support path. Keep release
`821796aa`, bundle `437cc3c0` and builder `86612e8c` unchanged. Stage from the
reviewed source selection, not by editing the original tree or an old extraction.
The input layout includes the deliberate source-to-destination mappings for the
root guide and selected exporter; an extracted output tree is not automatically
the same input layout.

Regenerate the two final archives because one shipped support payload changed;
the expected changed ZIP members are that preparer and the outer manifest. The
154-file mathematical package, release map and other shipped members must remain
unchanged. Then finish actual inert preparation, its exact config/receipt checks,
wrong-PROFILE-before-write and the previously unreached exporter-codec load.
Reuse the saved earlier negative evidence; do not repeat the whole prior suite,
native compilation, mathematical checks or growth campaigns.

This is a flat source/distribution successor, not another operator overlay chain,
new production manifest schema or build framework. New test/selection source still
needs review and a separate finite root launch. The original failure is charged
and retained. Full v5, native build and mathematical acceptance remain open.
