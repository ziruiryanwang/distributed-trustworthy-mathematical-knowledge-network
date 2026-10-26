# Root finite execution selection

2026-10-26. Root read and adopts the complete independent source review
`REVIEW.md` (`f97d9a295aaeaf7936843049344f692077206d1ae26aed48a8dd139e072d48c1`)
and the separate selection-only GO. Both reviews precede execution. The latter
checked all seven source pins, 21 runtime pins, fresh output, CLI syntax and
nested process/limit compatibility without running the selected program.

Select exactly one run of
`experiments/selected-export-controls01-selection.json`, SHA-256
`84b3db5aded4e59a9951d14cac0562c53e4112f9d8625d786b49bce0df1ba679`,
through the existing `tools/Run-V5-Check.py` using `D:\Python314\python.exe`.
Fresh output is `experiments/v5-local-checks/selected-export-controls01`.

The outer Job limits are 210 wall seconds, 120 CPU seconds, 1280 MiB,
four active processes and 1 MiB per log. The actual inner companion has
75 wall seconds, 45 CPU seconds, 768 MiB and one worker. The test controller
has its own cooperative 150 wall / 70 CPU second bounds. Whole-Job CPU is
inclusive; nested process charges must not be added again.

Only fresh synthetic inert custody is created. Direct helper controls prohibit
process/network calls; the final public CLI starts its one fixed Python worker.
No Lean execution, accepted owner/catalog, service, existing custody mutation,
publication, expensive certificate or growth episode is selected. The final
bundle must pass unchanged baseline-format validators, not mathematical intake.

The selected source/input bytes freeze on execution. Preserve a failure and
partial output unchanged; any repair requires a separately selected successor.
Do not adopt runtime success before a saved-output audit. This is a concrete
offline portability improvement, not completion of the full v5 objective.
