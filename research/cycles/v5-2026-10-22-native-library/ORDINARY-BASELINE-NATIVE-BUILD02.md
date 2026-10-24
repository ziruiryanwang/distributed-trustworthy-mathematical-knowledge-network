# Native build02: reuse completed exporter, repair only the remaining sources

2026-10-24. Root selected a fresh source-only successor after build01 failed.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
`cold_intake_strategy` owns `build_native02.py`, `select_native_build02.py` and
this checkpoint. The guard passed. All used01 code, snapshots, selection,
objects and failure evidence are preserved unchanged. No02 selector/build ran
in this assignment; no imported executable, owner/catalog, package or Git action.

## Actual predecessor, not a retry or relabeled success

Build01's outer selection was
`ff808bd2c58b353b7162f34bb66bcc22be19148efbe16a57f48765b96a8773c9`.
It cleanly returned `COMMAND_FAILED`, child1, no active/terminated processes,
closed Job, no cleanup errors. It spent 49.175299 wall seconds, 6.421875 known
inclusive Job CPU seconds plus 1.140625 outer-wrapper CPU seconds.

`BaselineExporter` code generation and C object compilation completed with
exit0. `BaselineArtifactCore` then failed code generation because `meta` was
used as a local identifier, a reserved Lean token. No candidate was linked and
no build receipt was completed. Failure does not erase the two completed
exporter stages or their cost, nor make the three remaining modules compiled.

The native author's fresh02 repair renames those locals and routes wrapper/
matcher imports to `BaselineArtifactCore02`; it does not edit used01 bytes.
The successor copies the completed exporter `.olean`/`.c`/`.o` instead of paying
for their compilation again. It also reuses the ten original shared `.olean`/
`.o` inputs as before.

## New source identities

| Source below `software/v5/ordinary_baseline/` | SHA-256 |
|---|---|
| `build_native02.py` | `dd54994b523fe9e8ef0d2f524cfdac228c33f7fae42a907844fb13ce6185e054` |
| `select_native_build02.py` | `281325b7d4b3b1b111ad605b925eb7ad6b34b680dd15c3f62b0ee0c7ae4fadc6` |
| Native author's `BaselineArtifactCore02.lean` | `ff34631ed54114c3919c7f3aa50ced634c1e2bf66496a1ca2f8be12da74d9e0f` |
| Native author's `BaselineArtifacts02.lean` | `b77d489c2b8aee6551d422fc4f54b46d5ca7e00defb4adcc557e93a8681d287a` |
| Native author's `OrdinaryReferenceBase02.lean` | `252bf83fe5353daab8169a21310eeef1e4b6eed2617e8209d99a260a98192635` |

Native source values remain explicit future selector arguments; changed sources
require final review and their actual new hashes. The unchanged exporter source
is `403f1f4369cd73ea905265f3df42d52f70c68cb5d4f24c03b696dd65f2fc629e`.

## Retained exporter and provenance

Origin: `experiments/v5-local-checks/ordinary-baseline-native-build-01/build/objects`.

| File | Bytes | SHA-256 |
|---|---:|---|
| `BaselineExporter.olean` | 1,382,224 | `e04caea5277a46a76f1d99d635692f7ccc6c9b7c9c463d3d4223383bb7010a34` |
| `BaselineExporter.c` | 396,098 | `afb83c5f9a220d8abf20b3ebc50bdf77f76bed0fe93715569bab8494ef89c2e1` |
| `BaselineExporter.o` | 323,361 | `c28ccaacdc58ae345f335c6cfff5f028769d3b5211d9a15b23efa9071a4accf4` |

The adapter binds exact prior `RESULT.json` (`b69fa1cc...`),
`BUILD-FAILURE.json` (`47fbff25...`), stdout (`2be5b8de...`), stderr
(`ae974277...`), `INPUTS.json` (`e4eb90fb...`) and selection (`ff808bd2...`).
Complete hashes are constants in `PROVENANCE`. It validates the clean-failed
outer state and exact 0/0/1 exporter-codegen/exporter-object/core-codegen phase
sequence. It also binds original, saved snapshot and staged exporter source
identities, then checks that all reused named toolchain/shared input pins agree
with the failed build's authenticated input map. The three output pins are not
inferred from their existence or from a saved success label.

The independent reviewer separately verified build01's 43 input pins and eight
snapshots, clean failure and the three retained output hashes. That supports
selective reuse; it does not authorize the02 run or establish compiler correctness.

## Exact02 delta and one new finite operation

Only `BaselineArtifactCore02`, `BaselineArtifacts02` and
`OrdinaryReferenceBase02` are compiled. Links are:

- `BaselineExporter.exe`: shared five `.o` plus retained `BaselineExporter.o`.
- `BaselineArtifacts02.exe`: shared five `.o`, new core02 and collector02 `.o`.
- `OrdinaryReferenceBase02.exe`: shared five `.o`, new core02 and matcher02 `.o`.

There are nine new commands: six codegen/object commands and three links. The
final object directory has 15 files: three reused exporter files plus twelve
new outputs. The receipt explicitly separates reused compilation stages, all
candidate outputs and newly generated outputs. It never counts the original
exporter compilation twice or relabels the predecessor as successful.

All unchanged01 safeguards remain: exact snapshots; source/copy readback;
per-command output census; original/snapshot/staged/reused/generated final
rehash; 23 named runtime pins and ten shared objects; current-source selection;
fresh output; inherited Job; same original deadline per subprocess; no retries.
An actual02 success still requires a **new clean outer Job outcome** and saved
evidence review in addition to the preserved old failure/provenance.

Independent02 review identified one missing final equality: merely repinning all
output files could record a command-modified exporter copy as newly observed
while still claiming the old reused-exporter pin. Before `NATIVE-OUTPUTS.json`,
the corrected unused02 adapter now requires every final exporter output pin to
equal its exact retained expected pin. A mismatch refuses explicitly; the
original `ab303b18...` source candidate was never executed.

Proposed envelope remains 240 wall/180 CPU seconds, 1536 MiB, six processes;
cooperative controller checks are210wall/150ownCPU. Logs stay in the outer
runner's 1-MiB stdout and 1-MiB stderr. Generated files remain <=32 MiB each,
<=256 MiB aggregate, with the explicit cooperative384-MiB spool arithmetic.
This is not a hard disk quota. Old CPU/costs are not renewed, refunded or hidden.

## Proposed exact invocation, not executed

From the canonical working directory, only after root's final source adoption:

```powershell
& 'D:\Python314\python.exe' -I -S -B '.\software\v5\ordinary_baseline\select_native_build02.py' --build-sha256 dd54994b523fe9e8ef0d2f524cfdac228c33f7fae42a907844fb13ce6185e054 --exporter-sha256 403f1f4369cd73ea905265f3df42d52f70c68cb5d4f24c03b696dd65f2fc629e --core-sha256 ff34631ed54114c3919c7f3aa50ced634c1e2bf66496a1ca2f8be12da74d9e0f --collector-sha256 b77d489c2b8aee6551d422fc4f54b46d5ca7e00defb4adcc557e93a8681d287a --reference-sha256 252bf83fe5353daab8169a21310eeef1e4b6eed2617e8209d99a260a98192635
```

This creates only the fresh `ordinary-baseline-native-build-02.selection.json`.
The separately authorized existing runner CLI remains
`D:\Python314\python.exe -I -S -B tools/Run-V5-Check.py <absolute-selection-path> <exact-emitted-selection-sha256>`.
Never invent that emitted hash or reuse the01 selection/allocation.

Independent02 engineering review is requested. No runtime is selected by this
checkpoint, and no build, correspondence, admission, registration, ordinary
delta use or deployable-v5 completion is asserted.

## Actual02 failure, preserved

Root subsequently selected and ran02 once, selection
`4b9eb52f3af4169dc6abb810932939b4c3311056ec9aa2e2bcf79967b79f686b`.
It failed at `BaselineArtifactCore02-codegen` line251:53, a missing explicit
record separator/layout issue (`unexpected identifier; expected '}'`). No new
module output or executable was completed. The outer result is cleanly closed:
3.9635374 wall seconds,2.453125 inclusive Job CPU plus1.03125 wrapper CPU,
zero active/terminated processes and no cleanup errors. Prior evidence stays
unchanged. The fresh [build03 note](ORDINARY-BASELINE-NATIVE-BUILD03.md) records
the naming-only adapter successor for root's explicit-comma native repair;
it reuses only successful01 outputs, not failed02 compilation.
