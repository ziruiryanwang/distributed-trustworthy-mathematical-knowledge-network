# Retained advertisement: source and focused-control review

2026-10-21, adaptive_audit. **PASS for the exact new sources and prospective
nine-control selection.** No execution or restoration-integration pass is
asserted. Read the adopted contract/selection, both exact successor diffs and
their immediate unchanged interfaces, complete control harness/selector, and
author checkpoints. No product import, test, network, proof, corpus scan or
Git mutation occurred in this review.

## Exact reviewed boundary

Paths are relative to the canonical Trustworthy project root.

| File | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/retained_advertisement/placement/advertisement.py` |23256|`5aa23ee76115355ad319ae4acfd4ab418e010166e53b6ed02c82eb25d34d4510`|
| `software/v5/retained_advertisement/client/serve_placement.py` |22670|`7e735337d595894e25fd07a8dcc9ad8cd3ba9f1c042ba930684b7798232cb7fa`|
| `software/v5/retained_advertisement/controls.py` |37254|`3d64a99d304a8bca0c2b36774313f4a70b85a8ddc225c740ca4d206ba2c5df34`|
| `research/cycles/v5-2026-10-20/Select-RetainedAdvertisementControls01.ps1` |6396|`8c682a33596255b35e0a6987d3bd9179516b54c27ffe4e3898e7eb3f7d2f717c`|

Author checkpoints: source `9ff38fc8832537d50e78b19ead597764065d67c09f6b55644077a44607d75cb7`;
controls `2469adb01dcfd38285e94a359f197cecfed64b36975762f96a34d5cc00eebf9d`.
Used advertisement `b5523f82` and service02 `319ddf07` remain frozen. Only two
fresh product modules change; the wire/core ledger/controller/index/locator
and mathematical acceptance rules are reused unchanged.

## One found defect, corrected before execution

Initial advertisement `04670ab4` ran its supplied guard before reservation
COMMIT, then called publish immediately. A slow COMMIT could cross the wall
retention horizon; the locator knows the monotonic command deadline, not that
retention condition. The selected contract explicitly requires a pre-send
owner guard as well.

Reviewed successor `5aa23ee7` adds `guard()` **after the durable reservation
transaction and immediately before publish**. If it refuses, the attempted
row remains charged and uncertain, with no send authorized. It also preserves
the original ordinary-publisher guard when sharing the dispatch body. A new
focused control exercises this exact seam; no old passing suite is repeated.

## Source invariants

- Authority is the exact fresh local service/controller grant, not an old
  publisher token. A controller call is consumed before selected-row checks.
  Restore requires SEALED_SERVING, current roles/config/liveness, the original
  monotonic deadline and the representative's original retention horizon.
  The sampled remaining active run must fit inside that horizon; no receipt
  horizon or old publisher policy is renewed.
- The explicit request ID selects bounded manifest/reservation/outcome BLOBs
  whose lengths are checked before loading. Canonical manifest, recomputed
  request identity and the existing closed success validator bind the immutable
  receipt, reservation, export, record, snapshot, packet and body sequence.
- Local checks use exact object/record IDs, snapshot/admission cut, selected
  posting/head, name/group index, packet/module/size/offer and descriptor-bound
  body metadata. Only one selected bounded group opening is decoded for its
  descriptor; later guards reuse that descriptor. There is no packet/body
  proof read, remote fetch, index re-admission, hidden representative scanner
  or unrelated-corpus traversal.
- The separate guard repeats saved-row equality, role/clock/local predicates
  at dispatch and transaction boundaries. Original immutable-store assumptions
  remain explicit: metadata presence is not fresh blob integrity or continued
  availability certification. Later acquisition still checks exact data;
  advisory restoration cannot create a mathematical warrant.
- `(cell,current_run)` is reserved before dispatch. Existing current-run rows
  suppress another send, including uncertainty. Current-only facet lookup
  returns the actual representative/run ID, not the latest historical run
  relabeled as current. The ordinary submit/status historical facet remains
  unchanged. The original run/command/page/cell caps are not enlarged or reset.
- The service installs one tracked owner-task handle before its first await.
  Caller cancellation propagates; only a completed task may clear its handle.
  Close cancels restoration before HTTP draining and joins under the same
  fixed `intake_until`, without another drain interval. Store closure requires
  `retained_closed`, no surviving task and the original busy/role conditions,
  including the race before advertisement busy-entry. Service02's original
  locator-close cutoff and complete validation remain intact.

These are source-level safety arguments. External containment, wall-clock
assumptions, bounded run availability and possible stale DHT hints remain;
no exact real-time or global-withdrawal theorem follows.

## Prospective controls and selection

The nine new methods use real local Workspace/SQLite/controller/index/route
state with simulated listeners and locator commands. One definition and
requested transparent body exercise descriptor-universe body matching. Its
inert terminal-I packet is explicitly unverified; receipt/native entry points,
process creation and actual socket use are forbidden. Restore additionally
forbids packet/body reads or writes, group writes, re-admission and old
acquisition helpers. Tiny fixture dumps compare immutability only in tests.

The assertions distinguish:

1. A funded two-run sealed restart, unchanged receipts/custody/index, old-token
   new-write refusal and one current-run restoration despite simulated expired
   original publisher/service windows.
2. OPEN/unknown/partial/wrong-domain/oversized selected records, plus missing
   posting/snapshot/name/packet-offer/body metadata: refusal after a call charge,
   with no route attempt, rewrite or automatic repair.
3. Too-short/expired horizons, expiry after reservation COMMIT and after send,
   dispatch/observation failure and same-run uncertainty: consumed opportunity
   remains, with no second publish.
4. Immutable run/config caps and failed endpoint reopen: consumed core-run
   charge is not refunded or enlarged to make the test pass.
5. Owner cancellation/concurrent refusal, close during actual restoration,
   and tracked task before busy-entry: cancellation and store-close ordering
   are checked explicitly.

Harness reports require all nine methods, no errors/failures/skips, forbidden
calls or unhandled loop exceptions. This does not experimentally cover every
cancellation-resistant actor; conservative failure/containment remains part
of the source contract. No actual DHT, TLS, proof or new mathematical result
is represented by the simulated observations.

Selector and staging agree on the pinned 114-file basis plus four replacements
and seven additions:127 physical sources,121 logical product files,19 direct
runtime/input pins. The exact reviewed-map parameters are checked; fresh
selection/output names are required and selection writing uses create-new.
It does not launch execution. Prospective limits are60CPU/120wall seconds,
384MiB/two processes and1MiB streams; no previous run is renewed.

## Disposition

No remaining blocking defect found in the selected source/control boundary.
Root may separately select the one bounded controls run. Actual source binding,
results, costs and cleanup need an outcome audit afterward. Cross-run real
network discovery, physical generation reclamation, net full-cost growth and
full-v5 readiness remain separate; this review neither selects nor substitutes
for those operations.
