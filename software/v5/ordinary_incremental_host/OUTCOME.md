# Independent actual assembly audit

2026-10-28, growth_design_audit. Canonical guard passed. Read-only inspection of
saved JSON/logs and actual file bytes; no rerun, product import, database access,
network or Git operation. This checkpoint covers file assembly only.

## Verdict

**PASS: the selected incremental-host file assembly completed cleanly and its
160 actual package files match the saved receipt and reviewed source delta.**
This does not yet qualify init, append, interruption behavior or service. The
receipt correctly says ASSEMBLED_NOT_ADOPTED. Root owns subsequent selection and
adoption; full v5 remains unfinished, local and unpublished.

Evidence root: `experiments/v5-local-checks/incremental-host-assembly01`.

| Binding | SHA256 |
| --- | --- |
| selection.json | `f5e408277fe429b46d3226b2bb78ff0f8e9f1ea76d75116acd71fc2e02cb704d` |
| RESULT.json | `217dff47d7d75cb9a26ca4dfd5af39cd144a4f6ce5b3e485c0ba019145e8feec` |
| distribution/ASSEMBLY.json | `d9bc9f90b0a77bfee2b4103b6c0dbc7c7d1fbf7a2f579d79699b65665efe1be2` |
| distribution/package/PROFILE.json | `e8d33500db4c0a5ce89b2dfb51c3e1f9ec8f12063bbc58fe5e4eb23c2b6dfb13` |
| installation manifest, unchanged | `9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27` |
| selected source map | `f5ea607c6774872113f404e2afcaf188b12a43e8839ac4ff5017b4edb02d8ab6` |

## What was independently checked

The outer result binds the saved selection hash and selected snapshot assembler.
All ten snapshotted source/helper/controller pins match that selection. The
selected assembler/map/helper and five source roles match the completed
source-review identities in REVIEW.md. Saved stdout is the assembly receipt
exactly apart from its terminal line ending; stderr is empty.

Every package payload was enumerated and independently checked against its
receipt length and SHA256. There are exactly 160, with no missing or unexpected
files. Compared with the adopted connect kit, exactly HOSTING.md, LAUNCHER.md,
custodian.py, host.py, run.py and PROFILE.json differ. The other 154 payloads
are unchanged. PROFILE contains 122 runtime files; its only changed file pins
are custodian.py, host.py and run.py. The two documentation files remain outside
the runtime profile while bound by the package receipt. The installation/native
payloads remain byte-identical. The reported implementation identity is
`86b6fcce8d8f13479e8131e1a386782b7bda5b6ee579df46e640ca8005affbea`.

## Operational evidence and cost

The saved controller result is COMMAND_EXITED_ZERO_AND_CLOSED: exit code 0,
direct child reaped, Job closed, final active processes 0, no cleanup errors,
no termination request and no terminated processes. The selected envelope was
90 seconds wall, 45 seconds CPU, 512 MiB private commit and one simultaneous
Job process. Lifetime total_processes is 2; this is not a report of simultaneous
processes. Recorded peak Job private commit is 17,674,240 bytes.

The Job consumed 1.578125 measured CPU seconds. Outer wrapper CPU was 0.109375,
giving 1.6875 known measured CPU seconds without double-counting the assembler's
own nested timer. The saved overall wall time is 7.310366899997462 seconds;
supervised time through cleanup is 7.28302440000698. Logs contain 22,491 stdout
bytes and zero stderr bytes. File-only assembly records zero native calls and
no mathematical owner opened; its reviewed source supports that scope.

No work was repeated for this audit. Focused control execution and one bounded
public host workflow remain separate prospective gates.
