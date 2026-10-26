# Independent exact controls01 selection review

Disposition: **GO FOR ONE SELECTED CONTROL RUN**; root owns launch/adoption.

Reviewed complete selection:
`experiments/v5-local-checks/kernel-admission-controls01.selection.json`, SHA-256
`a55f20629c4b90a3a9e977c74b5c2b625fabda4f0226a4cdb0641d91c94296f4`.
All four source pins and 34 external pins match actual file bytes. The output
`kernel-admission-controls01` is absent at review time. No runtime, owner/state,
database or Git operation was performed by this reviewer.

The fixture remains the reviewed `b8bb7074012ae09e586911e0a0f7e5031173270b4539267f2d4d11b7990743c5`.
Updated TEST-PLAN is 9,837 bytes,
`5db5f399108cebc9a9e501ffd4a8dfe37aa451e790297904a4b2e0e6f9fe4762`.
Its corrected launcher removes inherited Lean/Python/PATH variables, sets the
explicit pinned runtime PATH and adopted helper path, fixes canonical cwd,
closes stdin and suppresses a visible subprocess window. The selected inline
Python matches this plan and propagates the reaped Lean child's exit code.
The prospective four-process envelope resolves the margin concern in the
preserved CONTROLS-REVIEW; wall/CPU/memory/log limits remain 120 seconds,
90 inclusive Job CPU seconds, 1280 MiB and one MiB per stream.

The exact argv runs only the immutable selected fixture with `--run`; `-R`
points to its source snapshot, `LEAN_PATH` to the adopted build01 object tree,
and the fixture output is fresh beneath this run. All eight helper sources and
objects, nine named runtimes, five build evidence files and four review/adoption
files are externally pinned. BUILD-ADOPTION binds the independently audited
build without calling it mathematical acceptance. No old helper directory or
owner state is selected, and no compiler output overwrites the adopted build.

This resolves only the launch boundary left open by CONTROLS-REVIEW. Actual
success still requires all sixteen markers and exact completion, four expected
fixture artifacts with no refused artifact, unchanged inputs, empty stderr and
clean outer closure. The conditional eleven-record parent remains a fixture,
not a protected basis. No large intake retry, package adoption, implementation
identity migration or final-v5 claim follows automatically.
