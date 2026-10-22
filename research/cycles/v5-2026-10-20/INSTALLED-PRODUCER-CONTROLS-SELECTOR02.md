# Installed producer controls: selector02 source correction

2026-10-22; author `storage_launch_review`, under root's explicit assignment.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
No selector execution, test, Python import, syntax check, native call or Git
mutation was performed. Root owns independent diff review and execution.

Root reported selector01 stopped at its selected-source byte aggregation:
Windows PowerShell's `Measure-Object -Property bytes` did not expose the
OrderedDictionary entry as that property. This was preparation failure before
any selection output or control dispatch, not a failed controls test.

Read-only checks before and after writing selector02 confirmed both intended
paths were absent:

- `experiments/v5-local-checks/installed-producer-controls-01-selection.json`
- `experiments/v5-local-checks/installed-producer-controls-01`

The fresh selector therefore retains the unused `installed-producer-controls-01`
operation name and its unchanged freshness guards. It does not reuse a run.
Selector01 and all existing source/evidence files are preserved unchanged.

| Source | SHA-256 |
|---|---|
| Preserved `Select-InstalledProducerControls01.ps1` | `c0f0c738c693a37f9fb6a263a6369b99a2f0157b923d6770c1de6ac15caac03c` |
| New `Select-InstalledProducerControls02.ps1` | `ee5fba52ae3fc9c168a8ebd6deb71179479de034c67102d6a2a7f736892fa505` |

The sole source-text change replaces the pipeline property aggregation with:

```powershell
[long]$selectedSourceBytes=0
foreach ($row in $selectedPins) { $selectedSourceBytes += [long]$row.bytes }
if ($sources.Count -ne 5 -or $selectedSourceBytes -gt 16777216) { throw 'EXACT_SOURCE_BOUND' }
```

Each selected row already comes from `Pin` with a positive length no larger
than 2 MiB. Exactly five source additions are fixed in the script, so this
signed 64-bit sum cannot overflow. Direct `$row.bytes` uses the dictionary
access convention already used elsewhere in this selector. No source count,
digest, runtime map, argv, limit, output, write or dispatch behavior changes.
The read-only line comparison showed only this replaced clause and its two
new preceding lines. The new file was created through `apply_patch`; no frozen
file was normalized or modified.

The final controls source review remains separately applicable to the unchanged
controls and helpers. This correction is not a new controls outcome and does
not authorize a second runtime campaign. Root's independent source review and
one explicit dispatch remain required.
