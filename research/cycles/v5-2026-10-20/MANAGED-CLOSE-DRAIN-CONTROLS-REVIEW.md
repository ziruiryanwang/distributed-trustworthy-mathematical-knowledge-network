# Independent review: close-drain controls and finite selector

2026-10-21, core_release. **PASS SOURCE ONLY** for the three selected
extracted-method controls and preparation selector. No test, import, AST
execution, service or build was run by this reviewer. This review does not
adopt the service implementation authored by this reviewer; screen owns that
separate gate.

## Exact reviewed files

- `software/v5/managed_close_drain/close_controls.py`,18792 bytes,
  SHA-256 `46c0817c9353b46d3b79f985c773ac896fdc7e3e1887e15485ebb39c590e4e48`.
- MANAGED-CLOSE-DRAIN-CONTROLS-SOURCE.md,4823 bytes,
  SHA-256 `d1be272860b340022144fc66eca0d2436889d1ca4b0ad224d0b219a1abcfc282`.
- Select-ManagedCloseDrainControls01.ps1,
  SHA-256 `fe847ceba3ea2b734b19dc380b5b298554d4b3e3201b9f00a773798d659fe99c`.

Final test pin is the service24566 bytes/c815331f, not superseded039c.
The other three read/length/hash-pinned sources are controller4dc0824d,
advertisement5aa23ee7 and formal_features8822c818. Their exact paths agree with
the selector. Test source dependencies are rechecked after the test run.

## What the three groups exercise

The test compiles the exact selected AST methods, not rewritten implementations:
service _monitor/close/_close; channel _remaining/_read/command/report and its
actual frame constants; advertisement health. F is the complete actual selected
stdlib-only module. No full product module or constructor is imported. Explicit
ServiceFixture/ChannelFixture classes and component doubles make the scope clear.

The synthetic boundary is below the real frame write/read and command failure
handler. A successful first health precedes the held second status, matching
the normal monitor race without claiming actual startup. An Event after the
second status write and the service's real wake Event establish ordering; no
elapsed sleep is used to guess when the frame was written.

1. Healthy frame: reply remains withheld until close has entered and joined the
   monitor. Assertions require no intervening stop, then exactly status/status/
   stop, the second reply before stop, no cancellations/poison/kill, all cleanup
   flags and CLOSED. This would not accept the predecessor's after-write cancel.
2. Non-OK frame: the unchanged channel handler must poison and kill the fixture;
   monitor must retain HEALTH_FAILED; location_closed must remain false and
   final status FAILED. The test does not manually set these product flags.
3. Resistant read: the original400ms operation and one-second attempted monitor
   cancellation end with monitor still pending. Assertions require bounded
   FAILED return, _monitor_task and live_actor_prevents_store_close errors,
   revoked grant and no advertisement/controller/workspace closure. The other
   idle predicates are deliberately satisfied, isolating the new task guard.

The third case uses deliberately cancellation-resistant synthetic I/O. Independent
read-only inspection of the current runtime's asyncio/tasks.py confirms the
positive-timeout wait_for path directly awaits under timeouts.timeout, consistent
with the pending-task witness. That file is41571 bytes,
SHA-256 `3dc29324a51ba1d7a08b17c03a778b72dbb2921e66ee491f68cf6505837bc552`;
the selected executable has the existing python314.dll pin. The28 inherited
runtime rows are not a separately hermetic pin of every stdlib file. The test
itself requires the pending state; a different cancellation topology cannot
silently pass that group.

After failed-state assertions, the held frame is released, all tracked monitor/
close/caller tasks are joined within a separate three-second test cleanup,
results are consumed, channel lock must be free and loop errors absent. This
fixture cleanup does not upgrade the saved FAILED outcome. If a control fails
before releasing its resistant task, outer containment is still required.

## Deliberate nonclaims

Synthetic close/kill/stop and local advertisement guards do not establish actual
Node teardown, runtime adoption, ledger integrity, SQLite persistence, transport
or full service construction. None of these controls proves the startup margin
or grant-cutoff check; their arithmetic and ordering belong to screen's source
review, avoiding another initialization campaign. The shared predicate tests
a pending monitor, not a separately fabricated pending startup. No mathematical
acceptance, installed closure, contribution02 or full-v5 claim follows.

## Selector and output boundary

The selector authenticates basis buildad982f4d, removes only the exact old
contribution input runtime key, verifies exactly28 inherited runtime pins and
the selected Python, then snapshots exactly six files: runner44a7bf1b, test,
service, controller, advertisement and F. Test/service hash arguments must be
the final reviewed46c0817c/c815331f. No SDK import tree or service is selected.

The one source selection and output directory were absent during review.
Preparation writes one CreateNew, flushed, at-most1MiB selection; it does not
launch it. The isolated -I/-S/-B Python command uses only --output and the
snapshot test path. Limits remain10CPU seconds,30wall seconds,128MiB,one process
and1MiB per output stream.

The test insists on the exact canonical output and its own snapshot location.
It creates only close-drain-controls-result.json exclusively, bounded to16384
bytes, and emits the same canonical report. Selected cases are a fixed three;
failures/errors/skips, observations and synthetic/extraction nonclaims are
reported. Root must inspect actual terminal evidence and clean containment
before adoption; this source pass is not an executed pass.

