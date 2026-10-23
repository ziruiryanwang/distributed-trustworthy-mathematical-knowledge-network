# Independent saved-outcome audit: project authoring controls

2026-10-23, reviewer `admission_event_audit`; canonical guard PASS. Saved-output
and exact-file inspection only. No product import, rerun, database open, native
execution, network operation or Git mutation.

Disposition: `PASS_FIVE_NATIVE_FREE_PROJECT_CONTROLS_SAVED_OUTCOME` at
`experiments/v5-local-checks/ordinary-project-controls-01`.

## Exact selected result

- Selection:
  `dbddf833f55f50362fcaf0134efd24b4628158ddad9b9f7d96c85fcc7635db4c`.
- Reviewed harness:
  `fe329a9ec4c950e2b2fb453bd8e11ae7fa46f69bbfdc86fb5eaf857c6ec64105`.
- Outer `RESULT.json`:
  `f17a496f2ed64cb9721836df50c517dcd92be967a00bd1d847dc31776876068b`.
- `PROJECT-CONTROLS.json`:
  `b73ff9825b4ad690a1f78bebcaa834df5773ebd82eed087dbe92364df3d59540`.
- Actual stdout:
  `de1f56830c061229d9f6d1ecf691d43dc15bcb46a64a27ad7139c5343d7348ec`.

Independently rehashed all three source pins against canonical source and saved
snapshots, plus all 126 runtime/package pins: no mismatch. Actual stdout parses
to exactly the saved five-group report; byte hashes differ only because these
two serializers use different spacing/newline forms. Stderr is empty. Command
argv selects the reviewed snapshot and actual project package with profile
`b584cb21266fcf24502355a929939d8e6d662c75d1d7ea520fb23eb6105c7c69`.
Implementation remains `fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df`.

## Observed five groups and their scope

All groups report `ok=true`: owner JSON, closed backend/source, mocked worker
invocations, pre-open CLI refusals and mocked CLI forwarding. Successful report
construction follows one real load of the selected successor profile and core;
the loader returned the expected shared module identities. No package-load
compatibility result is borrowed from the predecessor package.

The reviewed guards and explicit mocks remain the basis of the native-free
interpretation. Native worker calls were argument captures, and the CLI success
branch used fabricated state/contribution objects. The result correctly states
`EXPLICIT_MOCKS_NOT_PROJECT_COMPATIBILITY_OR_MATHEMATICAL_ACCEPTANCE`,
`native_operations=0` and `owner_opens=0`. The synthetic adoption marker is not
an initialized catalog or mathematical warrant. Its fixture contains only the
eight expected small input/marker/source files; no candidate file, contribution
output, database or compiled artifact was produced.

This establishes executed configuration/default-source/invocation/forwarding
controls and a real fresh profile load. It does not establish actual project
imports/tactics, complete contribution-backend execution, Lean compatibility,
mathematical growth or deployment readiness. No mock CHECKED value is adopted
as a real acceptance.

## Aggregate cost and closure

Outer status is `COMMAND_EXITED_ZERO_AND_CLOSED`, child exit zero, direct child
reaped, Job closed, no requested termination and no cleanup errors. Final active
and terminated process counts are zero. Cumulative total processes are two;
this is not a measured peak-concurrency statistic.

Wall time is 1.4503276 seconds. Aggregate Job CPU is 0.71875 seconds and wrapper
CPU is 0.46875, totaling 1.1875 known CPU seconds. Peak Job private commitment is
28,254,208 bytes. These stay within the original 60-wall/35-CPU/512-MiB/two-process
outer selection. Internal controller CPU 0.671875 and elapsed 0.8085436 seconds
are nested observations, not extra charges. No allowance renewal or retry took
place. The prior tested sources/evidence remain preserved.
