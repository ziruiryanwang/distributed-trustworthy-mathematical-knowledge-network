# Native manifest controls: implementation checkpoint

2026-10-17, `memo_independent_review`; canonical guard passes.
Source only under SELECTIVE-FRONTIER-SELECTION appendix. No test/native/proof
call, build, Git operation or prior evidence edit was performed by this author.

## Exact source and scope

`software/v5/aggregate_small/manifest_controls.py`: 17,605 bytes, SHA-256
`ab897b28fbbdc930e9f775ac8461e07aaf5b6d284da4c329930f6997df5589eb`.
Independent source/plan review and root's explicit launch selection remain.
The script imports only its standard library and existing `production` helpers;
it never constructs a Producer. Three release-pinned supervisor/Job modules
provide the existing ordinary-path checks and clean process containment.

Uses completed `selected-frontier-layout-01`: s167/m1, two-member H, actual A,
capsule 32,965,324 bytes / SHA `6e41621e2595c252328eaf5f34862c6d6f913caecb68117406bcd616a61b44a5`.
The exact stage-host SHA is `8f8e444ddd9029906fee60a073a701bdd34c8b095d54f81f2554bfe1e91ad8ee`.
Layout result, clean outer record and original snapshot argv bind all inputs.
This replaces the old gate document's stale layout01/three-member assumptions.

## Controls and no-prove boundary

All ten invocations have exactly `stage-manifest ... finish 0 ...` (17 argv
elements, one real parent). The pinned source's finish branch contains no
prover construction or proving call even if a malformed manifest is accepted.
This is source-control-flow assurance, not dynamic proof-call instrumentation.
Every invocation still charges native relation checking, two parent-verification
paths and actual capsule decoding. It executes no guest.

One shared 72-zero-byte invalid checkpoint backs all rows. The correct finish
manifest has `segment:0..166,resolve:0`. Cases are the previously specified:
outer SHA; duplicate schema; nested positional pin; boolean byte count; capsule
binding; row order; file SHA; 257 rows; 258 rows; exact manifest/wrong magic.
M8 is frozen to `exact dependency count` (not a post-hoc alternative oracle);
M9 requires `dependency row bound`. M10 requires checkpoint magic/version.
Every case requires ordinary nonzero exit, zero stdout, its specific diagnostic,
no crypto/written progress, absent artifact and clean closed Job. First failure
stops. No automatic retry, optional cases, guest or proof work is selected.

## Configuration contract

`schema = DMKN_SMALL_NATIVE_MANIFEST_CONTROLS_V1`; exact fields:

- `inputs`: standard `{path,bytes,sha256}` pins named `host`, `image`, `wire`,
  `expected`, `capsule`, `parent`, `layout_result`, `layout_outer`, `layout_command`.
- `supervisor_manifest`: release-manifest pin; its exact three selected modules
  must also occur in `runtime_pins` (a unique list of pins, at most 128).
- `runtime_pins`: also pins actual script, production/__init__.py, producer.py,
  interpreter, python314.dll and host. All unique held input extents <=256 MiB.
- `case_limits`: six ordinary supervisor fields, ceilings 15 CPU / 20 wall /
  1024 MiB / one process / 64 KiB each stdout and stderr.
- `total_limits`: `worker_cpu_seconds<=150`, `controller_cpu_seconds<=30`,
  `wall_seconds<=240`, `output_bytes<=16 MiB`, `output_entries<=128`.
- `output_directory`: fresh nonoverlapping ordinary directory under local checks.

CLI: isolated pinned Python `-I -S -B manifest_controls.py CONFIG CONFIG_SHA`.
Root's enclosing Job must also bound startup/finalization and retain failures.
Reserve each next case plus finalization before dispatch; run sequentially.
All inputs/generated fixtures are pinned before/after each case and at closure.
Manifest hashes are correctly recomputed except the deliberate M1 mismatch.
Results retain each command/process/oracle, disjoint worker CPU and separate
controller cost. Output census reserves two entries/two MiB for finalization.
No capsule/ELF copies or fake successful cryptographic objects are generated.

Passing would qualify ten changed native input boundaries only. It supplies no
A receipt, segment-memory proof, full-cost growth claim or v5 release evidence.

## Exact selector prepared, not executed

`Select-ManifestControls01.ps1`: 10,236 bytes, SHA-256
`ac711c719045b547724551df9c6dcd10533808af8e574eac3f6ce1b0ddbce13d`.
Fresh run `selected-frontier-manifest-controls-01`; four source snapshots and
25 inner runtime pins. Three future source pins occur only in configuration,
never outer runtime pins. Outer limits: 210 CPU / 300 wall / 1536 MiB / three
processes; inner limits unchanged above. Selector checks exact adopted layout,
stage build and retained runtime pins, and creates config/plan with create-new.
Reviewer notified; root owns execution. No selection files/run were created.
