# Minimal close-drain controls: source-only handoff

2026-10-21, support_guest. Three fresh controls under
MANAGED-CLOSE-DRAIN-SELECTION. No test/import/runtime/build/proof was executed.
Root owns the finite selection. Core_release reviews controls; support_screen
independently reviews the service and margin arithmetic. No weak string-only
margin assertion or full initialization/lifecycle suite was added.

Control: `software/v5/managed_close_drain/close_controls.py`; final size/hash
accompany the handoff. Selected service is24566 bytes/SHA-256
`c815331f035618b36f504d604a1fb75d8682439f0488453c72e9801a63d78bd8`.
The control pins and compiles exact snapshot bytes, then repins them afterward.
Other exact dependencies are controller4dc0824d (15884 bytes), advertisement
5aa23ee7 (23256), and actual formal_features8822c818 (10826).

## Real methods, explicit synthetic boundary

AST extraction selects only PlacementService `_monitor`, `close`, `_close`;
LocationProcess `_remaining`, `_read`, `command`, `report` and its exact frame
constants; PlacementAdvertisement `health`. Actual full stdlib-only F supplies
serialization/validation. No complete product module, SDK, service constructor,
object.__new__, real process, socket, SQLite store, credential or proof is used.

Extracted methods are attached to separately named fixture classes, not passed
off as real product instances. Synthetic stdin/stdout carry actual canonical
length-prefixed command/reply bytes through the unchanged channel methods.
Other component stop/report/close functions and advertisement origin/ledger
guards are explicit local doubles. Thus this controls scheduling/frame-failure
semantics, not adoption, real Node teardown, store persistence or actual service
closure. The separate source review supplies those unexecuted wiring premises.

## Three deterministic groups

1. Initial real health method returns; the monitor's second status is held
   after the real command writes. Close begins and signals wake before that
   reply is released. A valid bound frame then permits exactly the sequence
   status/status/stop, second reply before stop, CLOSED fixture outcome, all
   cleanup flags, zero read cancellation and zero channel poison/forced kill.
2. The held status instead receives a validly framed non-OK reply. Actual
   command logic poisons the channel/kills the synthetic process, monitor
   preserves HEALTH_FAILED, and close returns FAILED with location_closed false.
   Stop is not issued on the poisoned channel.
3. Synthetic readexactly deliberately suppresses cancellation until explicitly
   released. Original400ms operation deadline and the fixed one-second monitor
   cancellation tail expire. Close must return FAILED within four seconds while
   monitor remains pending, record its failure and live-actor store refusal,
   leave all three stores unclosed and revoke the grant. Only after these
   assertions is the synthetic reply released so teardown can join all tasks.

The third double is intentionally hostile; it is not evidence that ordinary
Python pipe reads suppress cancellation. It tests the selected pending-actor
store guard and bounded wait. Test teardown retrieves all tracked task results,
requires an unlocked channel and no unhandled loop errors, and does not upgrade
the previously saved FAILED observation. Synthetic traces are bounded in the
single result; no fixture/state files are written.

The selected interpreter's read-only version resource is3.14.6. Its actual
`Lib/asyncio/tasks.py` (41571 bytes, SHA-256
`3dc29324a51ba1d7a08b17c03a778b72dbb2921e66ee491f68cf6505837bc552`)
matches the pinned release manifest and directly awaits the positive-timeout
`wait_for` coroutine under a timeout context. This is why the resistant read
remains on the monitor task. Test3 explicitly requires that pending state; an
older child-task cancellation topology is not silently accepted. No runtime
probe was used to establish this source premise.

## Selector contract and limits

`--output` only, fixed canonical
`experiments/v5-local-checks/managed-close-drain-controls-01`. Execute the copied
control below `<output>/sources/` and read the four source snapshots at their
original relative paths. Only `close-drain-controls-result.json` is created with
exclusive creation, capped at16384 bytes. Root's selectorfe847ceb snapshots six
files (runner/control/service/controller/advertisement/F), preserves28 runtime
pins, uses isolated no-bytecode Python and10CPU/30wall/128MiB/one-process limits.

Expected selection: three groups, no failures/errors/skips, immutable pins and
clean outer closure. Even a pass is extracted-method/synthetic-I/O evidence,
not an installed service, public contribution02, actual network, certificate,
storage guarantee or full-v5 result. No prior campaign is repeated.
