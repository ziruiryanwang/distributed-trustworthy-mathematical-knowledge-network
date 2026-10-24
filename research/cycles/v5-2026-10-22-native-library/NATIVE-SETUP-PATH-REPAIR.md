# Narrow native setup-path repair review

Status: **SOURCE-CLEAR for the selected path-spelling repair; no runtime claim.**

Reviewer: retained-registration subagent; canonical guard PASS. Read-only source
and retained-evidence review; no runtime or protected-state change.

## Observed failure and scope

`ordinary-reference-public-continuation-01` genuinely completed retained reference
registration. Author A then failed before admission while the Lean frontend tried
to open an existing `.olean` using a deep ordinary Windows path. The retained
`workflow/author-A/authoring-supervision/stdout.txt` names the exact path and
reports error 3. Read-only inspection found that file present at 55,576 bytes and
336 path characters. All 3,250 setup artifact paths have 333–344 characters.

Selected source-root/source/setup/output/report paths have 152/233/156/235/164
characters; output companions also remain below 260. The immediate defect is the
frontend **import artifact map**, not these command-line paths. Lean passes its
supplied import paths into `readModuleDataParts` without extended-path conversion;
existing `BaselineArtifactCore04.lean::nativePath`/`asArtifacts` already apply that
conversion in the native helper route.

## Exact source reviewed

`software/v5/ordinary_reference/reference_authoring02.py`

SHA-256:
`38045f1f99a2b00b7e3c7916a3a1ef26c0d1f58fcb20da45b6bec948699ab9c8`.

Complete source reread: the only functional change is `compiler_artifact_path`
applied to all original/generated artifact entries in `setup_document`:

- Require nonempty bounded string input without NUL.
- On Windows only, prefix canonical uppercase-drive absolute spellings with
  `\\?\`.
- Leave other path forms unchanged, including empty/dot/dot-dot components,
  trailing-dot/space components and mixed slash components. These exclusions
  avoid claiming that normalizing such paths preserves their Win32 referent.
- Bound the transformed spelling too.

The helper is **not** path authentication: inputs still come from verified stores.
Setup bytes remain pinned. Snapshot metadata, plans, reports, mathematical
identities, current warrant checks and new-unit admission are unchanged.

## Preserving successful work

`reference_registration02.support_descriptor` excludes author controller/worker.
Changing only authoring payload plus its PROFILE data pin can preserve the actual
reference support identity; changing `profile.py` source is not covered. Existing
profile verification must still pass against the actual overlay.

No rebuild, snapshot copy, repeated intake or live re-registration is justified.
Any selected continuation loads the committed reference and starts at authoring,
with fresh output/evidence and the old failure preserved.

## Limits

**SOURCE-CLEAR**, not an execution success prediction. Future command-line
source/output paths over `MAX_PATH`, UNC/lowercase-drive/noncanonical spellings
remain unsupported by this narrow change. Cooperative source approval and resource
limits remain unchanged; this is not a sandbox repair or a broader campaign.

## Assembly03 source review

Complete diff against audited assembly02: **SOURCE-CLEAR**. `assemble03.py` SHA
`759059ad735238d82a0ac209a1062be224f54a2d75da82ee73cb4dbb58aa6041`;
`select_assembly03.py` SHA
`43428010b5d8d702bdde03859d2c1b120419aad53191ad54551eb9bf37e2dad7`.
Canonical one-overlay map SHA
`33836bf682765c21e4454bc3d4e8ea09ae56dc2fb5687e45ed8a6d147f662bf9`
binds the 25,724-byte authoring02 to logical `reference/reference_authoring.py`.
Predecessor PROFILE/ASSEMBLY rehashes match `1054b9a3…aa10`/`537b8852…d85f`.
Only the new base/output identity, one overlay and corresponding source count /
receipt claims change; the known builder, file-only envelope and copying checks
remain. Expected census: 165 payloads, one changed, 164 unchanged, no additions;
five source snapshots. Installation/runtime/native/support-role bytes stay exact.
This is source clearance, not an actual assembly audit or runtime selection.

## Actual assembly03: PASS, no rerun

Independently read/hashed saved `ordinary-reference-assembly-03`: exact 167-file
census, 165 payloads, one changed authoring payload, 164 unchanged, zero additions;
57,985,278 payload bytes. All 137 profile pins, 178 runtime pins and five source
snapshots match. The parsed PROFILE equals02 except for that single file pin;
installation/native/support-role bytes remain exact. Selection/result binding
matches. Clean exit0, reaped/closed, no active process or cleanup errors; stderr
empty. Cost: 5.8699694 wall, 2.234375 Job + 0.734375 outer = 2.96875 known CPU
seconds; peak Job private commit 18,710,528 bytes. No owner/native replay occurred.

- PROFILE: `a10e1f3ae0e1ac04cfa01240c9c07c3ca2d3da91616a3ca34b1f28b88adadbbc`
- ASSEMBLY: `75f7f7c048208b337082c9b0529b02ac4fb6547d143ca178eacb73ba971da202`
- Selection: `9559af94ab6cbf13951c40dd5228dd55151fe2c84975b81f97dd117c4555a850`
- RESULT: `bf2fd07aa2881a2067926a5c641fbf3bab4da8741d25abd0eaeb2ee5beafed86`

This closes the file-only overlay audit, not authoring/reuse qualification. No
further repair expansion is recommended by this review.
