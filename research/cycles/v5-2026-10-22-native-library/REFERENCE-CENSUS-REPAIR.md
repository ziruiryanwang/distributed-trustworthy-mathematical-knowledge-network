# Reference census and workflow failure classification: bounded source repair

2026-10-24. `cold_intake_strategy`, under root's fresh source-only selection in
NOW/WORK. Canonical guard passed. No package, source import, test, native command,
owner operation, state migration, retry or Git mutation was performed. Only the
two assigned fresh successor files and this checkpoint were created.

## The observed defect remains a failed operation

`ordinary-reference-public-workflow-01` completed initialization and baseline
intake, then passed live private/public correspondence and failed protected
registration commit with `REFERENCE_OPERATION_FILE`. The supervisor had written
`supervision/command.json` (2,012 bytes), but the protected store allowed only
`stdout.txt` and `stderr.txt` there. Its native correspondence and snapshot are
preserved; no registered reference or A/B/delta contribution is claimed.

The outer harness then reported `SMOKE_UNCLEAN_PROCESS_TREE` because it checked
the cleanly closed public command against expected exit0, although that command
correctly returned exit1 for its application-level failure. Saved supervision
and public reply already preserved the real cause and clean containment. The
classification repair does not change that saved result retroactively.

## Exact predecessor and successor identities

| Source | Bytes | SHA-256 |
|---|---:|---|
| Preserved `ordinary_reference/reference_store.py` | 70,704 | `ff10bedc7fc88ecaee4dedc19a286c4cb37b69d15dc3f1907bc172d4737a67ba` |
| Fresh `ordinary_reference/reference_store02.py` | 70,728 | `bc15b9dd7c4386f05f58c36b9cd01887f709c6a75b6cb8418eec6309559080b1` |
| Preserved `ordinary_reference_package/public_workflow.py` | 32,872 | `32b331c8e853c38e328eaf6cd8a96c349b57b8b4d8ad8b72e81a2f48d078d300` |
| Fresh `ordinary_reference_package/public_workflow02.py` | 33,157 | `8193ae500a1108f84c321132d09c486844a9db4bcc963ce6caf4835fcc53f16b` |

Paths are beneath canonical `software/v5/`. Both predecessors were rehashed
after editing and remain unchanged. All four use LF with no CR bytes; successor
line endings were preserved. Read-only `git diff --no-index` shows only the
three hunks implementing the two repairs below. Its exit1 means files differ,
not a failed product operation.

## Repair 1: one bounded diagnostic filename

At `reference_store02.py:344`, the existing `supervision` two-component path
branch now allows exactly `command.json`, `stdout.txt`, or `stderr.txt`, each
with the existing explicit `MIB` bound. No wildcard or arbitrary JSON extension
was introduced. Unknown filenames, nested directories, redirected files and
oversized files still follow the same refusal paths.

The command file is metadata: the unchanged following code adds its bytes to
both total and metadata counters. Existing per-operation entry/total/metadata
bounds and all store-capacity checks remain unchanged. It is not a proof,
warrant, commit instruction or accepted saved report. The rule also applies to
the existing generated-delta supervision directory, whose same supervisor can
produce the same diagnostic file.

Independent review identified the coupled prospective reservation: at
`reference_store02.py:961`, generated-delta `future_metadata` must reserve the
new command file's full 1 MiB maximum. Root explicitly authorized this necessary
accounting correction. Its fixed allowance changes from 23 MiB + 4,096 bytes to
24 MiB + 4,096 bytes: final and pending reports (8 MiB each), trace (1 MiB),
supervision (1 MiB), command (1 MiB), both logs (2 MiB), failure (1 MiB), staging
record (2 MiB), and close record (4,096 bytes). Request, inventory and input
manifest lengths remain separately reserved. The unchanged 32 MiB metadata and
128 MiB operation limits may therefore refuse an oversized request earlier;
neither limit increases. Original-reference reservation already has sufficient
8 MiB overhead. Final census remains fail-closed in both paths.

## Repair 2: separate cleanup classification from expected command outcome

At `public_workflow02.py:310-314`, the harness first requires an integer actual
child exit code and invokes the frozen cleanup validator against that actual
code. Thus a nonzero code still needs clean reaping, closed Job, no cleanup
errors, no requested termination, no remaining or terminated processes, complete
CPU accounting and the original resource/log bounds.

Only after those checks does it compare actual exit against the selected call's
expected exit (zero for positive calls, one for the single intended negative).
A clean mismatch now reports `REFERENCE_WORKFLOW_CLEAN_COMMAND_EXIT_MISMATCH`
with the actual code. Missing exit reports an explicit unclean-supervision error;
other bad closure/resource records still fail the frozen cleanup validator.
Saved per-call events/replies and conservative CPU charging remain before this
check and are unchanged. Clean failure is still failure, never a passing call.

This is five replacement lines for one predecessor call, not a new supervisor
or acceptance route. It correctly distinguishes ordinary exit1 failure from an
unclean process tree without relaxing the existing intentional refusal checks.

## Verification and selection boundary

Both fresh files passed AST-only syntax parsing before the independent review's
literal 23-to-24 reservation correction and explanatory comment update. No module
was imported and no product logic, selector, test or subprocess workflow ran.
Source inspection and the exact three-hunk diffs establish the intended scope;
final independent review remains separate and has not yet been adopted by this
checkpoint.

All predecessor operation/package/source bytes remain frozen. The workflow
successor deliberately retains the predecessor's fixed package/run constants:
this source selection does not authorize another fresh output name, change the
used package or supply a continuation plan. A current selector would not launch
the successor and an attempted old output path would not be fresh. Root must
separately decide any future package mapping or operation. No such launch is
requested here, and no expensive successful prefix is repeated.

The growth-first architecture decision governs subsequent work. This closes the
small source-level deterministic defect, not the full integration or final-v5
goal.

Root subsequently read both exact diffs and adopted independent SOURCE-CLEAR
for the final hashes above; the audit is appended to
ORDINARY-REFERENCE-DELTA-CONTRACT.md. Final AST-only syntax parsing passed for
both successors after the reservation correction. An earlier command-line
quoting attempt failed before reading either source; it was not a product run.
No product code was imported and no state, installed package, evidence or native
process was touched. The repaired source remains unintegrated and unexecuted.
