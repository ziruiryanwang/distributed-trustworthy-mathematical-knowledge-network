# Ordinary-library controls01: independent outcome review

2026-10-22. Reviewer: `lean_workflow_trace`. Read-only review of the selected
run, its immutable executed sources, supervisor result, command output and
individual compiler diagnostics. No tests, builds, retries or runtime launched
by this review. Root owns successor selection and adoption.

## Disposition

**FAILED_WITH_CLEAN_CLOSURE; TWO_METHOD_SOURCES_COMPILE; NO_CODEC_OR_ADMISSION
CONTROL_EXECUTED.** This is not a successful ordinary-library admission result,
an independent basis warrant, a full reciprocal workflow, or final v5.

The command log records exactly three completed Lean invocations:

| Invocation | Exit | Reported wall seconds | Meaning |
|---|---:|---:|---|
| `compile-examples-ReadFootprint` | 0 | 24.855208000168204 | Producer method source compiles. |
| `compile-examples-ReadFootprintConsumer` | 0 | 0.7471146997995675 | Ordinary consumer source compiles; only an unused-binder linter warning. |
| `compile-OriginalExpr` | 1 | 70.36428899969906 | Import failed before checking codec declarations. |

The example lane ran concurrently with OriginalExpr, so the individual wall
times must not be summed as elapsed time. The consumer warning concerns binder
`avoids` at line43, not failed mathematical checking. Source compilation alone
does not demonstrate inert export/admission, peer discovery, cost benefit or
novel mathematical growth.

OriginalExpr's sole diagnostic is at line1, the broad `import Lean`:

> failed to read file `Lean/Elab/Tactic/Ext.olean.private`

That runtime file exists at review time. The Job's peak private commit was
1,611,837,440 bytes, close to its 1,536 MiB limit (1,610,612,736 bytes). Resource
pressure from loading the broad import closure is therefore a plausible
explanation, not an established causal diagnosis: neither the compiler output
nor the supervisor reports a specific heap-allocation failure. This review
does not infer corrupted/missing runtime bytes, hardware inadequacy or a need
for a larger memory allowance.

The driver raises on this failure; OriginalDecl, CheckedExtension and CodecChecks
were not reached. AdmissionChecks was not in the eight-source selection or
snapshot and was not run. There is no completed `CHECKS.json` success report.

## Bounds, costs and closure

The selected bounds were90 CPU seconds,180 wall seconds,1,536 MiB and4 active
processes. The result records `COMMAND_FAILED`, direct child exit1, direct
child reaped, zero final active processes, Job closed, and no cleanup errors.
No termination was requested; the observed total of5 processes is cumulative,
not five concurrently active processes or evidence of an active-process breach.

Job CPU was6.015625 seconds (1.359375 user +4.65625 kernel). The outer runner's
own CPU was0.578125 seconds, including its0.203125-second supervision interval;
do not add supervision again. Known Job-plus-wrapper CPU is6.59375 seconds.
Outer elapsed time was71.15950459986925 seconds; supervision through cleanup was
70.86563899973407 seconds. These are finite local-operation costs, not general
codec/verification latency measurements.

## Identity and evidence

Root-relative output: `experiments/v5-local-checks/ordinary-library-controls-01/`.
All eight immutable snapshot source hashes independently match their selected
values. The runner also validates selected sources/runtime pins after closure;
no final binding failure is reported. Runtime scope remains
`EXPLICIT_RUNTIME_PINS_NOT_HERMETIC_TOOLCHAIN_PROOF`: executable/DLL pins are
not a complete immutable Lean library closure.

| Evidence | SHA-256 |
|---|---|
| `selection.json` | `6af5f26849a719f9bf7f749a6a0e08e03f4b252d64f4857dba8d4a1b45a31a37` |
| `RESULT.json` | `2f27acdd02480ded13096376b5c9bd10e576920fb82389e6e2b20cccf2b5acc2` |
| `command/stdout.txt` | `06706ac7d9eae248cd7bec81d6e1726f5288933c1cdd476c23d8ee06de3ac334` |
| `command/stderr.txt` | `71d63b2f7243850b8efab76eecde4e1afbb3d4d5f25a2aab1dc1f9e1b09c3288` |

## Consequential next action

Root selected narrow imports at their actual layers and a core-only fresh02,
keeping the same resource envelope. This preserves failed01 and does not rerun
the successful method examples. It tests the unresolved codec/kernel boundary
instead of commissioning a broad memory investigation. Its result remains
independent future evidence; nothing here anticipates a pass.
