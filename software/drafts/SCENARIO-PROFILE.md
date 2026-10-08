# Test-only outer-sixteen scenario profile

Source-only proposal, 2026-09-21. No execution result or new native allocation
is implied. The failed `context-native-01` allocation and its frozen sources,
installation, journals and receipts remain unchanged. This profile does not
authorize a retry, mathematical acceptance or completion of the active v1 goal.

## Why a separate grant is needed

The product public profile encloses a node, its stage runner and the selected
child. The scenario adds a worker and a `manage.py` wrapper outside that public
Job. Previous request-bound PID evidence identified an auxiliary `conhost.exe`
with each Python process on this host; it did not identify a Python launcher
pair. Five simultaneous application layers can therefore produce approximately
ten OS-accounted processes. The failed allocation sampled nine against eight;
it did not preserve an exact failing PID census or establish a maximum.

Preserving the full successful public aggregate allowance of eight plus two
wrapper/console pairs suggests twelve under that observed host model. Sixteen
is a separate finite test allowance with explicit slack, not an inferred exact
maximum. The product public-eight and native-one requested limits, CPU/memory
limits, request/stage grants and mathematical checking remain unchanged.

The prior requested native limit of one nevertheless accounted for the child
and its console host. The requested Windows process limit must not be described
as a hard maximum of all OS-accounted auxiliary PIDs. Aggregate polling rejects
an observed count above sixteen and may overshoot between samples. CPU, memory,
wall time and output controls remain those of the original reviewed transport.

## Adapter contract

`software/tests/scenario_profile.py` reuses the original `run_stage.Job` and
`supervise.Transport` classes. It defines no replacement ctypes structures,
changes no global or product defaults, and modifies no imported class.

The Job adapter requires an explicit integer sixteen. It constructs a new base
Job with eight, checks that no process has ever been assigned, and queries the
complete extended-limit structure. It validates the original CPU, memory and
kill-on-close flags, changes only `ActiveProcessLimit` to sixteen, and reads
back every declared structure field. Any mismatch closes the unassigned Job
and fails before a process can be created. The temporary eight is construction
state of the newly authorized sixteen grant, not a grant change for existing
work. Setting the time-limit field again occurs before any CPU is consumed.

The Transport adapter requires explicit sixteen and this exact module as its
runner. A local copy containing eight is used only for the base constructor's
common validation. That constructor performs no Job creation or process launch.
After validation the instance receives a separate limits dictionary containing
sixteen. The inherited launch then records sixteen, constructs the adapter Job,
creates a suspended child and attaches/resumes it. The inherited polling,
whole-tree termination, direct-child wait, active-zero observation, Job close,
output checks and immutable receipt persistence still apply.

The launching driver must authenticate exact source bytes before importing,
assert the loaded paths of this adapter and the original `run_stage` and
`supervise` modules, and include all three source pins in the transport grant.
It must also bind Python, the concrete helper/worker and immutable launch input.
The adapter requires the original module paths in that pin set; that check does
not replace the driver's pre-import authentication and module-origin checks.
Every proposed run requires fresh explicit paths and a separately reviewed
manifest. The adapter has no CLI and does not itself grant a run.

## Prospective native-free shape control

Root will implement and review a small separate helper and driver. They must
not import or execute the product checker, native code, package readers or a
database. Use the pinned Python executable, fixed scripts and exactly two
sequential calls: normal completion and intended outer timeout. Maintain one
allocation-wide CPU/wall allowance in addition to the finite per-call limits.

1. Reproduce five simultaneous application layers: scenario worker, CLI
   wrapper, public node stand-in, runner stand-in and leaf. The outer adapter
   encloses the whole tree. The wrapper creates the unchanged public-eight Job
   around the node stand-in; the runner stand-in creates the unchanged
   native-one Job around the leaf. All descendant creation uses the reviewed
   flags, with the same suspended-attach-resume boundaries as the real shape.
2. Each layer writes an immutable, size-bounded PID barrier bound to the exact
   request digest, role and parent relationship. Hold every layer alive until
   the leaf is ready. Confirm actual child-written PIDs equal launched PIDs;
   do not infer identities from cumulative counts.
3. Query bounded Job-local process lists and image paths for outer, public and
   leaf Jobs. Use fixed-capacity buffers, bounded strings and explicit errors
   for truncation or failed required membership checks. Record console hosts
   as observed auxiliary members. Require the expected application PIDs in
   their proper Jobs, including descendant membership in ancestors; do not
   require exactly ten total PIDs or guess a missing image lookup.
4. For normal completion release the held leaf and unwind each direct-child
   wait. Record actual Job counters and CPU, require zero active descendants,
   direct children reaped and closed Jobs. Check the adapter's observed grant
   is sixteen and local requested grants remain eight and one.
5. For timeout keep the held tree alive beyond a short, explicit outer wall
   allowance. Preserve request-bound membership evidence before expiry. Require
   the intended timeout failure, requested whole-tree termination, reaped outer
   child, final aggregate active count zero and Job closure without cleanup
   uncertainty. Do not infer a termination-by-limit counter from explicit kill.

The driver records exact source/launch/command bindings and both outcomes,
including failed prefixes. Census retained files only after tree quiescence.
Count the outer Job CPU once; inner CPU is diagnostic and is not added again.
Coordinator CPU outside the Job remains separately identified. Any new native
scenario would still require its own review and grant after this control's
actual outcome audit; this plan provides neither success evidence nor a retry.
