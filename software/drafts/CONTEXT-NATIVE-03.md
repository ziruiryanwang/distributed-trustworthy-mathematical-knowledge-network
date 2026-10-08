# Fresh native context discriminator: allocation 03

Prospective source-only draft, 2026-09-21. Allocation 02 remains failed and
preservation-only: bootstrap succeeded, X was refused with an unknown `lcAny`
constant, and its two receiver stages consumed 272 MiB of grants. No old
receipt, source, database, pending/terminal status, or charge is edited or
reused. This draft creates no launch grant and implies no execution.

## Minimal source change

The three fixed Lean fixtures now say `noncomputable def` for
`BranchCompose`, `BranchFlip`, and `BranchComposeThree`. Their universe
declarations, binders, types, bodies, root names, and Z's two uses of the
received X name are unchanged. This changes the requirement to supply executable
compiled code, not the mathematical expressions being proposed. It adds no
axiom, sorry, alternate proof, or acceptance bypass. Successful elaboration,
export/reconstruction, and canonical dependency identity still require actual
native evidence; allocation 02 never established an accepted X identity to
reuse. This note does not independently settle the `lcAny` diagnosis.

The new worker and coordinator use fresh
`product-local/context-native-03` and
`software/qualification/context-native-03` roots. Counts, fixtures apart from
the annotation, native acceptance checks, refusal/selection/replay conditions,
source snapshots, CPU/cleanup accounting, and all limits remain unchanged from
the reviewed allocation-02 harness.

## Preserve the exact version-2 product cut

Both new files define a separate `PRODUCT` root:
`product-local/context-native-02/install`. `SOURCE` remains `software` for
the harness, `tests/scenario_profile.py`, and Lean runtime paths. The outer
`run_stage`, `supervise`, and `domains` modules are pinned and imported from
`PRODUCT/py`, with their loaded origins checked against that preserved root.
The coordinator therefore does not mix mutable version-3 containment helpers
into this version-2 experiment. The coordinator
enumerates product inputs only from the preserved installation, with relative
paths measured against `PRODUCT`:

- The four root files `API.md`, `manage.py`, `build.py`, and `assets-lock.json`.
- Direct `py/*.py` files.
- Recursive regular files under `native/` and `assets/`.

This is the existing 98-file inventory rule. It excludes `build/` outputs,
receipts, scratch, and databases. The worker independently binds every manifest
row to `PRODUCT / relative`, checks its exact source pin, and copies those
bytes into the fresh allocation-03 installation. It does not silently fall back
to mutable `software/` product files. The support build remains fresh; old
compiled outputs are not copied as product inputs.

The launch's product-row absolute paths must therefore name the preserved
installation, while relative identities and file bytes remain those of the
allocation-02 cut. These are source inputs, not reuse of old acceptance evidence.
A later version-3 product integration is not mixed into this installation and
does not migrate the preserved version-2 database. The separate harness/runtime
pins still require independent exact review at launch time.

## Unchanged finite allocation

The successful planned path is 14 installed public CLIs, ten fresh ordinary
requests, six receiver stages, and 18 planned pipeline commands, plus one
support-build stage/two compilations. Receiver grants total
`10 * 8 MiB + 6 * 128 MiB = 848 MiB = 889192448 bytes`.
These are reservation/command counts, not actual storage or OS-process counts.

The outer test-only profile remains requested sixteen processes, 450 wall
seconds, 450 Job CPU seconds, and 6144 MiB; product public-eight/native-one
profiles stay as in the preserved installation. Retained endpoint bounds remain
1 GiB, 16384 files, and 32768 entries. Auxiliary console-host behavior and
polling/endpoint limitations remain explicit. There is no repair loop, fixture
substitution during a run, automatic retry, additional native stage, or
allowance increase.

## Review and outcome boundary

Before any execution, independently review the minimal file diff, preserved
product manifest and actual hashes, outer helper/runtime pins, fresh roots, and
a newly authored exact allocation-03 launch. No launch JSON was authored here;
the author performed no import, compilation, SQL query, or execution.

The intended strongest result remains `PASS_PENDING_DEPENDENCY_AUDIT`.
Operational audit must check actual stages/charges, outcomes, refusal-before-
native behavior, replay/preservation, costs, cleanup, and retained files.
Canonical audit must separately establish X/Y separation and reachable Z-on-X
reuse. Source annotations alone establish none of those outcomes. No autonomous
research, useful-growth, networking, sustainable-capacity, or release-ready
claim follows from this draft.
