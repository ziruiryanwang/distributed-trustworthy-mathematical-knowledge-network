# Independent preservation and recovery-selection review

2026-10-26. Reviewer: `intake_interruption_audit`. Canonical guard passed.
File/selection inspection only; no SQLite API, product/status/native call, state
write, deletion or Git operation. The separate source decision governs the
mutating-capable reopen; this review checks its actual inputs and command.

**PASS_EXACT_FILE_PRESERVATION_AND_RECOVERY_SELECTION**, conditional on root's
fresh stopped-process/exclusive-access check immediately before a separate launch.
This is not recovery success, prior clean closure, or mathematical intake evidence.

## Actual preserved bytes

Backup: `experiments/v5-local-checks/std-recovery-preserve01`.
PRESERVATION.json SHA-256:
`d7bb49f4428724e857c82d09b07d35f5bf60b402bb9529cb246df958fe2f1ed4`.

I independently checked all eleven manifest rows against both original files and
copies: exact source/path mapping, lengths and SHA-256 hashes agree, totaling
**1,746,308 bytes**. The original census remains ten catalog files plus one custody
file. Backup census is those eleven files plus PRESERVATION.json, with no extra
file. Every original/copy file is ordinary, non-reparse and has exactly one hard
link; all inspected source/backup directories are non-reparse. No journal, WAL,
SHM, WITHDRAWN marker or additional operation file appeared in this census.

The two database files were hashed as inert bytes, not opened through SQLite.
Their preserved hashes are:

- catalog/catalog.sqlite: 118,784 bytes,
  `73178653ecc8dfdc5a6a6786710c8a64fd2cef8e8cbb1271d5b3c6934066f8f5`.
- custody/ordinary.sqlite: 16,384 bytes,
  `93695320c6d22e2dbf42b269814aa0011f229ae8653bdf19293d4b73cfdcfe23`.

The source's empty `catalog/imports` directory is not present in the backup.
No file is missing: this is exact file preservation with the necessary parent
directories, not a ready-to-open clone of every empty directory or an alternate
owner. This distinction does not lose the pre-reopen database/journal/artifact
evidence required by the recovery decision. Do not open the backup as a node.

The receipt records source pre/post equality and zero matching processes before
copying; my current source/copy hashes agree with that receipt. It is not a
retroactive proof of the old run's orderly termination. One read-only audit script
initially counted two nested file arrays instead of flattening them; correcting
that reviewer aggregation produced the eleven-file census above without changing
or repeating any product operation.

## Exact recovery selection

Selection: `experiments/v5-local-checks/std-recovery-status01.selection.json`,
SHA-256 `6a78055e685335a845edc09f0a1e3e493e9b39e3312b32075134e067c92eff5f`.

The schema/name are DMKN_V5_LOCAL_CHECK_V1 / std-recovery-status01. All 200
external rows from the interrupted intake selection remain identical. Exactly
24 rows are added: the twelve actual stopped-run files and twelve backup files.
I independently hashed all 24 added files and all five selected sources; they
match, giving **224 external pins and five source snapshots**. No unexpected,
missing or changed pin was found. I did not repeat hashing of the 200 adopted
package/runtime/prerequisite rows. The runner revalidates them on actual execution.
The mutable original catalog/custody files are not input-pinned; their separate
evidence copies are pinned instead.

Selected sources are the existing runner, original quota, interrupted-outcome
audit, owner-recovery decision and RECOVERY-EXECUTION. The source decision remains
`d03cd3775e4b6ca212c0b3e1eeb7306c3474d452ca426faaaf1f32a467ad8285`.
The runner's source is unchanged; its limits/source/runtime-count restrictions
and pinned-command rule accommodate this selection without modification.

I compared all **40 argv elements** with the preceding public command and the
source decision. The command uses the same actual package/profile/runtime/store/
quotas, but selects only:

```text
owner -- status
--catalog <original std-catalog01>
--custody <original std-custody01>
--store-id eaca70ad43af5c6ec9a362f1b44f5ac9b45e7924703f25648f2398eea32b1d7f
--custody-limits {snapshot}\software\v5\ordinary_std_intake\custody_limits.json
--context-root 3034986549a52b2a0b46f5fffe2c650879453f43ff85d4ef38cf3ff73b7a7d62
--limit 4
```

Diagnostics are the fresh `{output}\owner-status`. There is no intake, bundle,
parent-root, build, source/project or migration argument. The explicit context is
the adopted basis, not a guessed new root or an arbitrary inventory entry.

| Envelope | Wall / CPU / MiB / active processes | stdout / stderr |
|---|---|---|
| Public | 35 s / 10 s / 512 / 1 | 1 MiB / 1 MiB |
| Outer | 60 s / 20 s / 768 / 2 | 1 MiB / 1 MiB |

All six outer limits match exactly; public argv values match the source decision.
The output `std-recovery-status01` is absent at review. The command is directly
supervised by the existing runner; no new launcher, adapter or native allowance
is introduced.

## Execution and evidence boundary

Root must freshly confirm no competing operation before launch and serialize
both stores. Status may perform SQLite recovery and change RESERVED operations
to INTERRUPTED; it is not read-only. Preserve the first outcome and never delete
locks/journals/markers to obtain a pass. The backup remains untouched evidence.

Actual success still requires clean public/outer closure, matching owner/store/
implementation identity, zero worker CPU, exact adopted-basis context and honest
root inventory/custody counters. New inventory rows, if any, are not automatically
accepted rich roots. A later recovery success cannot fill in the interrupted
run's missing terminal reports or recover its unknown cost/cause. No intake
retry, larger allowance, contribution or full-v5 claim follows from this clearance.
