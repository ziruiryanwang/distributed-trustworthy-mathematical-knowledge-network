# Project successor packaging: bounded source review

2026-10-23, `ordinary_api_flow`. Canonical guard PASS. Read-only source,
descriptor and file-hash inspection only; no product/test import, selector
execution, build, service, native operation or Git action.

**Disposition: PASS_SOURCE_ONLY_PACKAGING.** No actionable defect was found in
the three reviewed files. This clears their packaging/selection design, not the
replacement implementations, any generated selection, runtime or mathematics.
The CLI and contribution/worker source are outside this distinct review.

## Exact reviewed source

All files are under `software/v5/ordinary_project_package/`:

| File | SHA-256 |
|---|---|
| `assemble.py` | `652fda9899252e99cb7cf0a1767e89332f720f4815bfaa16b1640ed3703ac978` |
| `select_assembly.py` | `d6f04769a08b46b9c27214a0a4eda68eb6d41dfe2a77745bea4cb8951c8a41f0` |
| `select_validation.py` | `7bbf31ff2e642e2312b0c6fd37a95c16251a9e8abd35e49933d23fd7dc008eca` |

Compared in full with peer predecessors `b0257328`, `72c81632` and `ba1020a5`.
The material assembly delta is the three-entry replacement map and required
base loader `22fb8b00`, with project-specific source paths/report codes. The
controls selector removes the reciprocal branch; it does not inherit its old
10-process grant or retained-owner inputs.

## Pins, copy map and unchanged boundary

Read-only hashing confirms the hardcoded preserved builder
`49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5`,
base owner `91359645d82ee556de37637bae74da9ab1aaabad3a4d1678346f761d54b737cb`,
and base loader
`22fb8b00d76838c7dac77d669c18c72bb253a087be0002c8ef6077a1aa4bdf9b`.
The existing peer package PROFILE is
`06649545f962e8ca95b21ab1c87626444bdc06c16e5191b96a8f27e7766505e5`;
its installation manifest is
`32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.

The existing descriptors yield 116 copied payload files. All three replacement
keys already exist: `owner.py`, `author_worker.py`, and
`authoring/py/ordinary_contribution.py`. The other 113 payloads retain their
original exact pins. No new `profile.py` is supplied. The existing peer loader's
required-file set and `AuthoringProfile` construction cover the same logical
names, so the descriptor needs only the three updated byte/hash records.
Installation identity, helper paths, author-worker logical path, peer payloads
and all compiled helpers remain unchanged. External runtime attachments are
verified, not copied. No catalog/custody state is in the copy map.

The assembler checks the base through its pinned loader before copying. It
checks every selected source pin before creation, streams to exclusive fresh
destinations, verifies each copied hash, and checks both maps again before
committing PROFILE. Its own snapshot bytes must match the selected root source.
The new descriptor is the old descriptor with only the replacement file pins.
ASSEMBLY metadata is separate from executable payload paths; partial failure is
preserved without retry or cleanup deletion.

## Exact selection and finite envelope

Assembly selects seven source snapshots: runner, selector, assembler, preserved
builder and the three replacements. Builder/assembler/replacement live-source
paths are also runtime-pinned because assembly reads from the canonical source
root. Base PROFILE, its auxiliary payloads, installation manifest/payloads and
external selected runtimes are pinned. For this base the assembly runtime map
has 131 entries, below its 256-entry cap.

The controls selector pins the successor PROFILE, all its payloads, installation
and runtimes (126 entries with the unchanged layout); its source snapshot is
runner, selector and `project_controls.py`. Both commands execute the selected
snapshot path under `-I -S -B`, use a fresh named output and retain exact input
pins for the outer runner's before/after checks.

Assembly outer limits remain **90 wall seconds / 50 CPU seconds / 512 MiB /
2 processes**, with inner **60 wall / 40 CPU seconds**. Controls outer limits
remain **60 wall / 35 CPU seconds / 512 MiB / 2 processes**. Both use 1 MiB stdout
and stderr caps. The unchanged supervisor ceiling is eight active processes;
both selected caps are valid and neither selector contains a reciprocal grant.

## Remaining handoff gates

Root still owns the exact generated selection and independent saved-outcome
review. Replacement CLI/G/worker qualification belongs to its separate review.
At this inspection `project_controls.py` was not yet present; controls selection
must wait for that separate runner and its source review. No packaging-source
repair or additional test campaign is requested by this review.
