# Actual audit: three close-drain method controls

2026-10-21, core_release. **PASS for the selected extracted-method/synthetic-I/O
shutdown controls, with an explicitly retained warning below.** No rerun,
runtime import or service was launched during this audit. The canonical guard
passed. This is not actual Node, installed-service or full-v5 qualification.

## Identity and executed boundary

Run: `experiments/v5-local-checks/managed-close-drain-controls-01`.
Original and copied selection both have SHA-256
`d93d13333fae97b37a9a365f18849a68e22033c674fd77970198e825f1ccf1fa`.
The selected source review is8b450d0e; separate service review922fe5f2 is root-
adopted, not authored/adopted by this implementation author.

All six source snapshot files match their selected pins and current originals;
the snapshot contains exactly six files: runner44a7bf1b, controls46c0817c,
servicec815331f, controller4dc0824d, advertisement5aa23ee7 and F8822c818.
The executed argv/cwd/limits match selection. The saved stdout is exactly the
2493-byte canonical inner report followed by CRLF, with no other output.

| Evidence relative to run | Bytes | SHA-256 |
|---|---:|---|
| RESULT.json | 2041 | 74a0527dfbdf2407a69bbe7ac1ebea1f9b4ae4badb1f505622599087a0223269 |
| close-drain-controls-result.json | 2493 | e9053c670ef6021048b62876d082f906cca8436aa97eac8e9bead3372a1d6125 |
| command/stdout.txt | 2495 | f2e4bd40e09939900bcb0e816151f062f18780e7fb54d029968e71527cdcddea |
| command/stderr.txt | 3981 | 7aab3ca150a2ac7a24328f2328d6313b0d4249e43e28fa9abac3fce031ee672a |
| command/command.json | 695 | 22055ac2b9eb6280256a6f4d1f8d5b1fef1d95c60ba8fa6e140bcf678c009fa4 |

The runtime scope remains the selected28 explicit pins, not a hermetic-toolchain
proof. This audit did not repeat a full runtime sweep.

## Exact actual outcomes

The report and full stderr agree: exactly the three selected tests ran, with
zero failures, errors or skips. Each selected trace is present.

1. **Healthy in-flight status:** commands are exactly status/status/stop.
   The second reply occurs before stop is written; stop reply precedes synthetic
   locator/read shutdown and all three store closures. Reported fixture status
   is CLOSED, zero read cancellations and zero kills. Passing source assertions
   also require all seven cleanup flags, no cleanup errors, no channel failure
   or forced termination, and a completed monitor.
2. **Failed reply:** commands are status/status, with no stop command. The failed
   reply precedes exactly one synthetic kill; the fixture remains FAILED.
   Assertions require HEALTH_FAILED, channel_failed and forced_termination,
   location_closed false and location_close uncertainty. Store closure after the
   failed but completed monitor is permitted; failure is never upgraded.
3. **Cancellation-resistant read:** close returns FAILED in1.8112893998622894
   seconds, below its fixed four-second assertion. The monitor is still pending
   at that return, _monitor_task and live_actor_prevents_store_close are required,
   all three stores remain unclosed and the grant is revoked. Commands remain
   status/status. There are two synthetic read cancellations. Only after those
   assertions does fixture cleanup release the held frame; the late expired
   read causes the final synthetic kill. No store-close event appears.

All three records report all tracked tasks drained after test teardown. The
passing teardown assertions require the channel lock released and no unhandled
event-loop exception. This is not the same as warning-free stderr.

## Retained warning and its precise limit

The resistant-read test emits:

`RuntimeWarning: coroutine 'SyntheticPipe.readexactly' was never awaited`

at the unchanged controller.py line152. The preserved traceback reaches the
post-release body read: `F.strict(await exact(size), FRAME_BYTES)`.
The statement forms `self.process.stdout.readexactly(count)` as the first
argument to wait_for before evaluating `self._remaining(until)` as its second
argument. By then the deliberately delayed operation has expired; _remaining
raises before wait_for can take ownership of the newly formed coroutine.
That unawaited coroutine was never scheduled as a separate live task.

This is a real inherited awaitable-construction ordering issue exposed by the
synthetic late reply, not evidence of a clean warning-free run. It does not
invalidate the observed failed return, strict channel failure, store protection
or eventual tracked-task/Job cleanup. The already-failed result is not upgraded
during teardown. A later narrow controller successor can compute the remaining
interval before forming the coroutine. This audit does not select that edit,
repeat the control, or generalize the warning into actual pipe/network behavior.

Stderr additionally contains asyncio's diagnostic that the finished monitor
task took0.132 seconds; the trace includes warning formatting. No cause for that
entire duration is established. It is not a test error, timeout or leaked-task
report. Both diagnostics remain preserved in stderr7aab3ca1.

## Outer containment and cost

The outer report says COMMAND_EXITED_ZERO_AND_CLOSED, child exit0, direct child
reaped, final active_processes0, Job closed, no cleanup errors, no requested
termination and zero terminated processes. Cumulative total_processes is2; the
configured active-process limit is1, not a claim that only one process identity
ever existed. No real service orderly-stop signal was sent by this fixture.

Measured Job user+kernel CPU is0.5625 seconds; top-level wrapper CPU is0.3125
seconds (the inner supervisor separately reports0.03125, not another independent
charge to add blindly). Total outer wall is3.303716199938208 seconds; command
through cleanup is3.25040669972077. Stdout2495/stderr3981 bytes stay within the
unchanged1MiB caps, as do10CPU/30wall/128MiB limits. Unit-test stderr reports
three tests in2.297 seconds.

## Consequential disposition

The selected normal close ordering and both required failure boundaries have
executed evidence; no repeat is justified for those same claims. Root may use
this scoped outcome with the separate source review when deciding one combined
diagnostic-owner/service build and later public contribution02. The controls
do not test startup construction/margins, actual locator adoption/termination,
store persistence, network operation or mathematical acceptance. No old failure,
installation, source, grant or evidence was modified.

