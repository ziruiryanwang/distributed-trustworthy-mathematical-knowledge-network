# Minimal managed-close observation controls

2026-10-21, support_guest. Source-only assignment under
MANAGED-CONTRIBUTION02-SELECTION; no controls, imports, product runtime, build,
proof, network, credential access, service or state modification was executed.
Root owns selection, execution and adoption. Core_release reviews these controls;
support_screen separately reviews the owner wiring and original error precedence.

New control source: `software/v5/managed_observed/observation_controls.py`.
Its final size/hash are reported with the handoff, rather than self-pinned here.
No old control suite or predecessor source was edited.

## Exact inputs and extraction limit

The only two product sources read at the eventual selected execution are:

- Observed owner, 31626 bytes, SHA-256
  `1c022737e4d51a25d873e6fd255cd87ee8427f21d7455f78b29d4b2e4d133503`.
- Actual selected `software/v5/instantiation_discovery/discovery/formal_features.py`,
  10826 bytes, SHA-256
  `8822c8186ba120da9c8b72abe6d0c905eeaced5af46ef19600e463904a6d1b0c`.
  The authoritative contribution127 input map selects this source. Its complete
  module has only stdlib hashlib/json/re imports; its actual `compact` and `need`
  are used, not substitutes.

The control authenticates each snapshot before compiling its bytes, then pins
both again afterward. From the owner it extracts precisely, in source order:
`_CLOSE_FLAGS`, `_CLOSE_COMPONENTS`, `_CLOSE_FAILURES`, `_close_enum`,
`_close_scalars`, `_project_service_close`, `_service_close_observation`.
It never imports the complete owner, constructs PlacementService (including by
object.__new__), or invokes the worker. Exact AST extraction qualifies only
these helper definitions; it does not establish real cleanup, service ownership,
worker ordering, primary-error preservation in the worker or strict CLOSED/seal
behavior. Those source-wiring obligations have an independent reviewer.

## Five compact groups

1. Known failed final report: exact complete projection, one report call,
   unchanged synthetic input, recognized failure vocabulary and CLOSED label
   without any closure-authority claim.
2. Partial/missing/unrecognized snapshots: partial is not final; absent nested
   reports remain unavailable; wrong report/schema/container types do not become
   accepted report fields.
3. Exact scalar/range limits: nonbool flags, bool/noninteger/subclass counts,
   counter and returncode boundary values; exactly32 rows versus33 truncated
   rows; invalid rows/list shape; every result fits the8192-byte cap.
4. Privacy: a publicly specified synthetic marker is placed in ignored fields,
   arbitrary maps, token/credential/route/traceback/stderr slots and unexpected
   enum/error values. It must not occur in serialized output. Synthetic exception
   str/repr callbacks must not run; known-looking string subclasses are rejected.
5. Fixed fallback: no reference, throwing report (including BaseException), and
   a temporary fault in the actual serializer all yield the fixed nonauthoritative
   result. Report is called once; the serializer is restored; no exception text
   is rendered. This does not simulate or assert successful service closure.

The suite has no fixture files, service lifecycle, subprocess, network, SQLite,
certificate, authorization, old lifecycle tests or real private input. A tiny
report-only callback fixture is explicitly not an actual service. The serializer
fault is a temporary selected exception injection into the actual imported F
module, not a stub implementation of F.

## Planned runner contract, not execution authority

CLI is `--output` only. The exact accepted directory is
`experiments/v5-local-checks/managed-observed-controls-01` below the canonical root.
The harness must execute the copied control at
`<output>/sources/software/v5/managed_observed/observation_controls.py` and reads
the owner/F snapshots at their corresponding relative paths below `sources`.
It refuses an existing `observed-controls-result.json`; that single exclusive
result creation is its only explicit file write. Root's runner supplies isolated
Python with bytecode disabled and captures unittest stderr/stdout.

Root proposed four snapshots (runner/control/owner/F), reused28 Python runtime
pins, and a finite10CPU-second/30wall-second/128MiB/one-process envelope. This
note neither launches that plan nor claims those limits were exercised. No
full-SDK or842MB payload sweep is needed for the extracted pure boundary.

Expected selected result: five groups, zero failures/errors/skips, clean outer
closure, matching pre/post pins. A helper pass would remain diagnostic-only,
not actual contribution02, installed worker, mathematical or full-v5 qualification.
