# Transport harness pre-execution review

2026-09-21. Source-only review of `run_transport.py` and
`transport_worker.py` against the actual supervisor/Job interface and
`test_peer_wire.py`. The reviewer did not execute, import, compile, or run tests.
No source/interface blocker was found for this finite test cut. This is not a
test-pass result or authorization for an unbounded run.

## Compatibility and finite execution

- The worker accepts the supervisor's exact config/state/request/event CLI and
  checks `-B -E -s -S`. The coordinator's fixed request matches the worker's byte
  equality gate. Config binds the exact fixture directory and test count.
- Discovery selects only `test_peer_wire.py`; source enumeration contains 18
  test methods. Worker success requires a successful 18-test suite; coordinator
  additionally rejects skipped tests and nonzero worker exit. A changed suite
  requires a changed, reviewed count rather than silent acceptance.
- The 10 listed pins include current Python, configuration, worker, coordinator,
  suite, both peer modules, runner, domains helper, and supervisor. They satisfy
  the supervisor's required Python/worker/config/runner set and 16-pin ceiling.
  Actual byte totals/hash authentication remain runtime gates, not assumptions.
- The actual Job constructor accepts the selected 60-second CPU allowance,
  512-MiB private-commit limit, and eight-process ceiling. The supervisor enforces
  a 60-second success wall envelope and 64-KiB stdout/stderr/event bounds, with
  suspended creation, Job assignment before resume, and final active-zero/reap
  checks. Cleanup may extend beyond the success wall limit; failed/overrun work
  must not be reported as an in-envelope pass. Polling is not a hard transient
  output or filesystem quota.
- Tests use small fixed synthetic byte vectors, finite loops, and local threads;
  oversized-frame controls declare large lengths without allocating those
  payloads. Loopback service/session/request and socket timeouts are finite.
  A surviving non-daemon test thread cannot create an unbounded accepted run:
  the outer process-tree supervisor must time out/terminate and refuse it.
- Event hashes bind exact request and response bytes. Worker test failure still
  returns a normal process response, but its `FAIL` status is rejected by the
  coordinator. A transport exception produces `FAILED`, never a test pass.

## Preservation and claim limits

The named qualification root is newly created with `exist_ok=False`; launch,
configuration, result, and supervisor records are exclusively created. Fixture
directories use `mkdtemp` under the explicitly selected retained root, with no
automatic fixture deletion. A corrupted view bundle is an intentional mutation
of that test's fresh synthetic copy, not an existing mathematical artifact.
No reuse/overwrite of an old run is permitted. Persistence is not asserted to be
crash-atomic merely because files are retained after ordinary completion.

The suite exercises wire framing/identities, catalog schemas, refusal controls,
local view completion, and real loopback HTTP discovery/acquisition. Synthetic
CBOR is deliberately not mathematically admitted. Source inspection supports
the zero-Lean-stage scope: the harness uses `run_stage.Job`, not its native stage
execution function, and the test worker imports no checker/native codec.
Literal `native_stages: 0` fields are not independent instrumentation proving
that property for arbitrary future source changes.

`PASS_PENDING_OUTCOME_REVIEW` appropriately leaves outcome inspection to root.
Even a future pass would not establish canonical semantic closure, native
receiving admission, durable peer registration, reciprocal mathematical growth,
malicious-local-host isolation, multi-host behavior, or crash recovery. These
tests also do not deliberately qualify supervisor timeout/kill fault paths;
they use the existing supervisor as containment.

## Reviewed pins

| File | SHA-256 |
| --- | --- |
| `tests/run_transport.py` | `D3C207450494BBD0AFD014B5B9285C741E6CF16CB5300B5B4421E51549F4493D` |
| `tests/transport_worker.py` | `B25B98CCF86B559FCF2FE70A925263D2A9576328F2E3869852F9BABB53258FB4` |
| `tests/test_peer_wire.py` | `E7949C9E2998EAF051FBB633B4F46EED917A96B66ECA38CA537C339C32CF66F5` |
| `py/supervise.py` | `E5F35C0A88602757ECB7FF899F923F940B588E11E2A7C9C36D51FDBB2DFCAC1B` |
| `py/run_stage.py` | `499557B7C55A05F41460C0DFC894BA3C40CBD008D184415FD6B729B1CE422EFA` |
| `py/peer_wire.py` | `B4AAD584E9F6F6D83872501D277C1F1CDE79E5A89618EFBF1260497BEB8D4946` |
| `py/peer_service.py` | `58D355B183790E54C0BC5C96738E3AC0C2358AA1C65D0C1704D45E9EF8F28407` |

The wrapper's current source pins, fixed fixture bounds, and narrow scope—not a
general claim about future tests—are the basis of this review disposition.
