# First suffix intake: independent selection review

2026-10-26. `kernel_package_audit`.

**PASS_FOR_ROOT_SELECTION.** Reviewed exact selection
`experiments/v5-local-checks/std-kernel-suffix-a01.selection.json`, SHA-256
`d7c7c12a6e17e0aebe1375780b2dd73582d73c3c77f0786e8c8ddf7525cb3611`.
This is a prelaunch source/data review, not execution or successful intake.

## Changed boundary

Compared directly with the saved `std-kernel-intake01/selection.json`, the full
44-element argv changes at **exactly three positions**:

| Index | Change |
|---:|---|
| 37 | Parent changes from the basis to actual validated prefix `c3d0f6209f42abdc98a6975a358545b0d61701e849b6ed0a3e69bdc1b7f400f6` |
| 41 | Manifest changes to `std-kernel-suffix-inputs01/part-a-canonical.json` |
| 43 | Manifest hash changes to `9eee85273f5fcbc0b91f9f0975c10bfad557b6cb555d334e580499fdf0fedb9c` |

The package, Python/Lean runtimes, catalog, custody, store identity, original
materialized unit directory and public route are unchanged. Public limits remain
360 wall / 300 CPU / 1,536 MiB / three processes; outer limits remain 420 wall /
330 Job CPU / 1,792 MiB / four processes, with unchanged log ceilings. The existing
60-CPU per-operation limit is unchanged. No catalog-limit override is added.

The adopted `PREFIX-STATUS-OUTCOME.md` (`e7570b03...`) and
`PREFIX-STATUS-ADOPTION.md` establish the selected current protected prefix;
both are pinned here. Basis and prefix snapshots remain separately pinned.
The new selection does not rely on the old failure diagnostic as recovery
authority. Its fresh run output directory did not exist at review time.

The adopted `SUFFIX-MANIFEST-REVIEW.md` (`3a9273c7...`) establishes the actual
canonical part A's exact 620/404 whole-unit cuts, 8,552,756/8,595,160 raw bytes,
schema, semantic identity, row order and strict input-format compatibility.
Those bytes independently rehash in this review. Part B is only a pinned inert
future input: it appears nowhere in the executable argv. No second invocation
or prospective second parent is selected.

## Source and pin-map census

Independently rehashed all **three source files and 243 external pins**: zero
mismatches. The three sources are the unchanged runner, unchanged custody limits
and the new `SUFFIX-PLAN.md`. The latter replaces historical source-plan records;
it changes no executed product implementation. The runner remains pinned at
`44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651`.

The external map exactly contains the actual current package's **154 files**,
with no omitted or additional package file, and all **23 selected runtime pins**.
There are no mutable database, WAL or SHM pins. Reconstruction metadata and its
current row-order evidence, immediate initialization/failure/status evidence,
current package identity and both accepted snapshots remain bound.

Map comparison gives:

| Comparator | Prior pins | Removed | Added | Changed shared pins |
|---|---:|---:|---:|---:|
| Actual previous intake | 218 | 8 | 33 | 0 |
| Actual prefix status | 232 | 8 | 19 | 0 |

The same eight omissions in both comparisons are exactly:

- `current-release-build01/distribution/package/PROFILE.json` and
  `installation/INSTALLATION.json` beneath that historical package.
- `parse-reuse-package01/RESULT.json`, `command/stderr.txt`,
  `command/stdout.txt`, `distribution/ASSEMBLY.json`, and `selection.json`.
- `software/v5/ordinary_current_release/release.json`.

The first two groups are under `experiments/v5-local-checks`. These are historical
descriptors/evidence, not current executed package files, selected mathematical
inputs or runtime files. Removing their redundant selection pins does not remove
their files or weaken current package identity. The new 243-pin map remains under
the existing 256-pin ceiling. Additions preserve actual failed-intake/current-status
evidence, continuation reasoning, reconstruction review and canonical manifests;
no shared existing hash was silently replaced.

## Disposition

The exact first suffix selection matches the adopted smaller-batch decision and
retains its acceptance and resource boundaries. Root may select this one operation.
Its eventual success still requires both actual CHECKED batches, COMPLETE, exact
returned bindings/artifacts and clean closure. Any refusal remains charged and
requires a new decision. Part B remains conditional on independent adoption of
part A's actual result.

Review actions were source/JSON reads, map comparison, ordinary-file census and
hashes only. No product import, owner/status command, database access, native
execution, raw-unit reprocessing or Git mutation occurred.
