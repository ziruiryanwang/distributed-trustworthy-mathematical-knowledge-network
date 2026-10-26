# One saved-writer binding diagnostic

2026-10-26. **SOURCE ONLY; NOT RUN.** Root selects execution separately after
review. Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Decision

Does the retained complete Std export fit the current producer binder and its
recipient-facing batch ceilings after removing duplicate local inspection?
The original public export failed during WRITE_EVIDENCE; it remains failed.
This diagnostic cannot recover or relabel that production, establish admission,
or compare old/new elapsed speed. No native export, old binder or full bundle
regeneration is run. The independently approved ordinary-library workflow is
not obliged to re-export an already trusted Std package merely to use it.

## Exact source/data boundaries

`measure_saved_writer.py` directly loads pinned installed ordinary_evidence,
ordinary_semantics, portable_evidence and portable_candidate, and the new binder
SHA `e4b52c2f2e823cc98aa37c8cc7adb0cf79952def9c19b54d7072116a39fa19b6`.
The binder resolves from the test script's own source root, so the selected
runner executes snapshot bytes. Frozen modules and data use the explicit
canonical root independently of cwd. All source/data pins are checked before
use and after the diagnostic; bytecode writes are disabled.

Saved input: `experiments/v5-local-checks/std-export01/bundle`.

| Input | Bytes | SHA256 |
|---|---:|---|
| writer.json | 38154768 | 5a2f721127cfef3ae39613c1ec723b2f710cc410c872650fb2acfd7d04078b7a |
| inventory.json | 823690 | c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0 |
| request.json | 496 | bcb647fa96824cc82aebda1dab151a88d678ca3d8756cd150e0103e9f41993bd |

Target remains the actual `Std.HashMap.isEmpty_insert`. The 708 retained partial
unit files total 6389257 bytes; no partial file is overwritten or promoted.
Their exact aggregate map pin is
`82df4b3e84e8e53a21ab87f94507f0ba8ecbf8c82fbc6fad1e3b0459d6bae4d0`:
SHA256 of ASCII `PARTIAL_UNITS_V1`, NUL, then sorted rows
`filename:decimal_bytes:lowercase_sha256` each terminated by LF.
The directory count, names, regular-file shape, bytes and complete map are
checked before binding and again while every partial is compared byte-for-byte
with its corresponding newly bound unit. This is correspondence, not acceptance.

## Single operation and outputs

Invoke the new binder exactly once with its unchanged default limits and the
exact request targets. No observational wrappers or second full-reader pass.
Require 2651 complete units and exact manifest entry/byte correspondence. Report
the returned complete aggregate census plus every batch's units and bytes.
Per-batch nodes/names/edges are explicitly not retained in the report: the
unchanged binder checks those limits while partitioning, without new machinery
merely to reconstruct these reporting fields.

Only a fresh `binding` child of the supervising run may be created. Save the
manifest (at most 2 MiB) and small summary (at most 128 KiB), using
exclusive writes. Summary includes every batch's unit/byte count, total census, targets,
input/map pins, cost, limits and claim boundary. No 2651-file unit output,
receipt, catalog/state modification, native module, package or Git change.

## Fixed resource selection

Inner cumulative limits: 90 seconds wall and 70 seconds process CPU;
cooperative checks run at product budget checkpoints and at input/output stages.
There is no internal hard memory cap or new memory-monitor implementation.
Root's existing Run-V5-Check selection must enforce outer 120 seconds wall,
90 seconds Job CPU, 1792 MiB, one process, and bounded stdout/stderr. These are
distinct envelopes, not permission to renew a failure. No retry is selected.
The runner snapshots this script and the successor and pins its Python runtime.
Pass the single argument `{output}/binding` to the snapshotted script.

Even success shows only inert producer/batch numeric fit and partial-byte
correspondence. It does not check native recipient time, total intake reserves,
catalog occupancy, one-call peer capacity, the 32-group materialization limit,
proof semantics, independent cold acceptance or deployable-v5 completeness.
Costs are descriptive for this one run, not a speedup claim. If it fails, stop
and preserve that outcome; no cap increase or public-production rerun follows.
