# Independent actual outcome: inert-mirror-controls01

2026-10-26. **FAILED, cleanly closed; do not adopt the inert-mirror service.**
The selected preparation prefix completed, but the first positive public serve
failed before opening a listener. No discovery/acquisition result follows.
This review read only retained files/source and recomputed hashes. No product
imports, state/database access, runtime, rerun, repair or Git action occurred.

## Exact selection and accounting

Run root: `experiments/v5-local-checks/inert-mirror-controls01`.
Retained selection SHA-256:
`74f0dfcf92a87d58699c0ff20c280f05cbd63b00c12f8097c25248b1d4b675e6`.
All eight source snapshots independently match their recorded selection pins.
The root runner's terminal result is COMMAND_FAILED, child exit 1, reaped child,
closed Job, zero active/terminated processes, no cleanup errors and no termination
request. Known cost is 6.842246 wall seconds, 5.171875 inclusive Job CPU seconds
plus 0.25 outer-runner CPU seconds; peak Job private commitment is 96,317,440
bytes. Nested CPU observations below are already inside that inclusive total.
All used source, inputs, outputs and the failed result remain preserved.

## What actually completed before the failure

The retained test source reaches its unique assertion at line 347 only after the
earlier direct controls, source-refusal calls, public prepare and startup-refusal
assertions succeed. This is prefix evidence from the exact sequential test and
saved reports, not a completed suite's PASS or independent reopening of its DBs.

- Direct preparation returned PREPARED_DATA_NOT_SUPERVISED_READY, nonacceptance,
  closed stores and no cleanup error. Its following checks retrieved all four
  exact supplied units and the unindexed group sibling locator, then required
  only the two selected targets in the index.
- The direct missing/wrong import, duplicate/basis name, wrong target/disclosure,
  aggregate count/byte/hash-reservation, fresh-output and late-index-refusal
  controls completed. The partial late-failure output remains without READY.
- Wrong source-map selection and changed first codec returned respectively
  SOURCE_MANIFEST_SELECTION and RUN_PIN_SIZE with NO_WORKER_LAUNCHED.
- Actual public prepare completed: four units, five supplied output names,
  5,149 evidence bytes, five import edges, 20 expression nodes, 985 preview bytes
  and 6,397 observed index hash steps. These are inert structural/work counts,
  not mathematical acceptance. Its worker Job returned zero and closed, with
  0.609375 inclusive worker-Job CPU seconds. Parent stdout reports
  INERT_MIRROR_PREPARE_COMPLETE and `ok:true`.
- Wrong READY/descriptor hashes refused PREPARED_SELECTION before launching a
  worker. The direct-helper descriptor without READY refused on its missing seal.

Independent readback binds every parent READY hash to the actual descriptor,
request, worker report, supervision report, entry, helper and fixed source map.
READY SHA-256 is
`298d7c807dcc3915455b28b473ce13b06812aea722538348080e1fa877558266`;
descriptor SHA-256 is
`fb21213d54f05f7f80a6191668dc79409ecf04a268c7e26f1b90b4c64fcf4ebf`.
No READY-PENDING remains. The precommit RUN's nonterminal `ok:false` is deliberate
and does not contradict the final exact READY and successful parent stdout.

## Exact failure and causal trace

The public serve worker returned MirrorError whose detail is
`EvidenceError:JSON_LEXICAL_TOKEN`, with `ready:null`, `quiescent:true`, stores
closed and no cleanup errors. Its parent refused WORKER_NOT_CLEANLY_COMPLETE.
The enclosing test then raised TEST_PUBLIC_LISTENER_FAILED at line 347.

The frozen helper's `serve` at line 427 calls
`descriptor = E.strict_json(descriptor_raw)`. The ordinary evidence parser's
documented grammar (`ordinary_evidence.py:75-116`) excludes `true`, `false` and
`null`; operational DESCRIPTOR contains booleans and snapshot metadata. It
therefore rejects its own correctly produced descriptor before `_ready`, lock
acquisition, DB opening or Provider startup. The helper's line 391 also sends
READY through that same unsuitable parser and would fail on its `false` field
after the first parse was corrected. Both are operational metadata, not evidence.

This was an implementation/parser-domain error missed by the independent
prelaunch source review. Preserve that review as the actual historical GO; do
not rewrite it into a successful prediction or blame the fixture/network.

The already pinned `formal_features.strict` accepts canonical boolean-bearing
metadata, bounds bytes/depth, rejects duplicate keys/noninteger numbers and
requires exact canonical encoding. Its encoding agrees with
`ordinary_evidence.canonical_json`; READY's fixed strings/hashes are ASCII.
Using it only for these two metadata parses is a narrow justified successor,
not permission to loosen ordinary evidence or alter mathematical acceptance.
Root owns source selection and any later reviewed continuation.

## What was not reached and what must remain unchanged

SERVICE-READY, network.json, TEST-RESULT and the post-service state-change record
are absent. No public discovery, preview/evidence acquisition, live lock-conflict
test, completed positive lease or post-service snapshot-refusal result occurred.
The public prepared state's ACTIVE.lock is absent, consistent with failure before
lock acquisition. Both service and enclosing Jobs ended cleanly; no service lives.

Reuse the completed prefix instead of repeating its fixture/refusal suite. A
changed helper needs a genuinely fresh public preparation because the READY seal
pins helper identity; do not relabel the existing seal or edit its prepared state.
The retained exact four-unit bundle can supply that new preparation. A fresh
bounded continuation should cover the repaired metadata boundary and only the
unreached service/discovery/cleanup edges. Neither this audit nor a future small
pass establishes worldwide availability, growth acceleration or final v5.
