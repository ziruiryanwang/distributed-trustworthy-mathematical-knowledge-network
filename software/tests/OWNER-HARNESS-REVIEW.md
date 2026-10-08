# Owner-contract harness pre-execution review

2026-09-21. Source-only review of `run_owner.py`, `owner_worker.py`, the independent
`test_owner_contracts.py`, and its authoring notes against the actual product
supervisor and relevant early-refusal functions. **No source/interface blocker
found for this bounded 20-test cut.** No imports, execution, compilation, or tests
were performed by this reviewer. Root retains execution/qualification authority.

## Compatibility and scope

- The coordinator, fixed configuration, worker, and source enumeration all
  agree on exactly 20 tests. Discovery selects only `test_owner_contracts.py`;
  the frozen transport suite is not broadened. Worker failure/count mismatch is
  rejected, and the coordinator independently rejects skips and nonzero exit.
- The supervisor receives the correct config/state/request/event CLI. Required
  `-B -E -s -S` flags and exact request/response event digests match its interface.
  Thirteen pins cover current Python, config, both owner harness files, the
  reused transport helper, suite, build/manage/node/storage, runner/domains, and
  supervisor, within the 16-pin ceiling. Runtime size/hash checks remain required.
- Declared limits are 60-second success wall and Job CPU, 512-MiB private commit,
  eight processes, and 64-KiB stdout/stderr/event files. Existing suspended
  assignment, final active-zero/reap, and Job-close rules remain in effect.
  Cleanup may outlast the success envelope; polling is not a hard transient
  filesystem quota. The small finite fixture program writes two approximately
  1-MiB records plus small markers, not unbounded test data.
- Fixtures are fresh retained children of explicit `DTMKN_TEST_ROOT`; there is
  no ambient temporary root, automatic teardown, recursive removal, or overwrite
  of existing run evidence. Marker writes use exclusive creation beneath each
  selected fixture child.
- The tested configure calls are invalid-client or already-existing-path
  preflights. The build call uses existing work and a separate fixture runtime
  with no Lean executable. The inert `lean.exe` text marker occurs in a different
  path-selection test and is never passed to a build. No test invokes runner
  execution, process launch, a positive native build, or SQLite connection.
  Imports load definitions, including the Windows resource backend; they are
  not themselves Lean stages. The parent coordinator legitimately launches the
  single supervised test-worker process tree.

The literal `native_stages: 0` result is consistent with these reviewed source
paths, not independent image-level instrumentation. Success would qualify only
the enumerated path/parser/preflight contracts, not positive configuration,
native admission, durable peers, mathematical soundness, or system completion.

## Coverage and changing-source qualifications

`software/build` now exists after build-01. Therefore the existing-work refusal
test also satisfies the separate existing-target refusal condition. Its pass
can confirm safe refusal/preservation for this combined state but cannot alone
isolate or mutation-test the existing-work predicate. This is a coverage limit,
not a launch blocker; no claim of isolated guard coverage should be made.

The authoring notes pin older manage/node/storage cuts. Their current peer
additions change file hashes. This review reread the relevant configure guards
and import boundaries: invalid clients/existing paths still stop before the new
peer/configuration work, and module import does not execute peer/checker/database
operations. New peer logic is **not** qualified by these tests or this narrow
review. Root must freeze/record the actual complete run pins and review any
further changes affecting these paths before execution.

## Observed source identities

| Source | SHA-256 |
| --- | --- |
| `tests/run_owner.py` | `B32A325A9A861C49723162B374DE1B69764ABFA3BFC3C9CCB65706C7F351DB09` |
| `tests/owner_worker.py` | `1288D7F6EC17D531E493A6AAABE9F5AE83426FF6DCAFDEC9861D88D9B6267B1C` |
| `tests/test_owner_contracts.py` | `01C3BEC112E910DF87A00553FA201EC442C3C0D73862391789C5D43AA9A03BF6` |
| `tests/run_transport.py` | `D3C207450494BBD0AFD014B5B9285C741E6CF16CB5300B5B4421E51549F4493D` |
| `build.py` | `9F57312577C3E48683D4BFC365134A964CF85BB2FD3C86B98D642926DD1E08CF` |
| `manage.py` | `485637417F40262CE4679A455B4D89B069C00861E06DB27216E7D77336A9E680` |
| `py/node.py` | `986279A99EDE271CB1D2039F1433B02C2DCB7EB6D1940863AAA95E3E8C8A73CB` |
| `py/storage.py` | `2BEF745773269C0D80B8855FB40F2C38F36692B531D154C2597287BDDD492387` |
| `py/domains.py` | `A3F44CCE31DDD79056F0683DE17D46712BFD46C99DFE71FAC56E27DD1DEB59C9` |
| `py/run_stage.py` | `499557B7C55A05F41460C0DFC894BA3C40CBD008D184415FD6B729B1CE422EFA` |
| `py/supervise.py` | `E5F35C0A88602757ECB7FF899F923F940B588E11E2A7C9C36D51FDBB2DFCAC1B` |

This reviewer authored domains/runner; the test suite was independently authored.
This note checks harness safety and interface fit, not independent certification
of the production core or a substitute for the later actual outcome audit.

## Final owner-01 source-cut clarification

Before owner-01, root added `manage.serve` and changed request pin selection.
The reviewer reread the latest manage file and confirmed the suite's early
configure guards and import behavior remain unchanged; the new function bodies
are not exercised by this suite. Final run-cut `manage.py` SHA-256 is
`057038F1B1FB95D4D740B326A3ADC07226D27FCEB086CD3C3EA0006AC71E76AB`,
superseding the earlier manage checkpoint above for owner-01. Service behavior
requires its separate source review and is not included in this disposition.
