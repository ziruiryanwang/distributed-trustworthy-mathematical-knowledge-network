# Independent discovery-rejection source review

2026-10-20, core_release. Canonical guard passed. Source read only; no native,
proof, compiler, test execution or Git action by this reviewer.

## Decision

**Clear for the selected eight changed-boundary controls, not release adoption.**
The new facade preserves the existing staging, grant, issuer, import and
mathematical-admission implementations. Its additional source origins are
required in the real owner pin maps. Only search offer/page dispatch changes.

| Reviewed payload | SHA-256 |
|---|---|
| `software/v5/transport/search_validation.py` | `00aef512d2b1cffc98ca537cd8df0da5840340c3a265b3640da22c8fd50018ee` |
| `software/v5/transport/test_search_validation.py` | `250ba800aaf4c0574141405cda72f7e86a81b3588d4b12ae45e4a63052f8e8e7` |
| `software/v5/client/workspace_validated.py` | `4f379f478b9226fd19af1b282d1888ee8cd3430dacf6820596506985993c2a0c` |

## Consequential checks

- `_preflight` verifies only the received offer/candidate/page and relevant
  existing summary/coverage bindings. It does not copy the full search session,
  promote a summary, commit coverage, or mutate candidate deduplication.
- Offer decoding matches the existing `SearchSession._accept_offer`; candidate
  verification uses the existing pure verifier; interval verification includes
  Coverage's existing cross-page object binding check before any commit.
- Expected pure metadata validation errors return an inert typed refusal.
  Deadline/offer-expiry callbacks are wrapped and reraised outside that
  classification. Unexpected errors, resource failure and cancellation escape.
- First read identified one local coverage-summary equality check inside the
  recoverable region. The author moved it before the region and added an
  explicit fatal-local-state test. It is not treated as a hostile provider error.
- The original exact ticket is abandoned once on invalid metadata, at its
  full reservation. Request/page/provider/snapshot charges remain spent;
  no retry, new grant, deadline extension or mathematical acceptance follows.
- A valid response still enters unchanged `SearchSession.accept`, outside the
  recovery catch. Its accounting/state-commit failure remains fail-stop.
  Double verification is bounded extra work on the selected response, not
  additional work proportional to all global mathematical knowledge.
- The tests exercise malformed JSON/UTF-8, summary damage, invalid positive and
  interval proofs, no partial metadata, honest continuation, preserved live
  inert authority/context/staging, request exhaustion, local deadline/coverage,
  late commit failure, cleanup/cancellation/allocation failure, and two actual
  IPv4 loopback connections. Their owners and mathematics remain synthetic.

## Launch scope

Read `Select-CoreChecks.ps1`: it verifies the pinned prior structural-staging
selection and all retained source/runtime identities, adds only the three new
search files, refuses existing output/selection paths and selects the unchanged
finite local-check runner. Its search envelope is 30 CPU seconds, 90 wall
seconds, 256 MiB and two processes. This is not a new prover/framework or a
repeat of the predecessor test campaign.

An actual saved-outcome audit remains required. Passing inert-owner controls
cannot establish full real-owner construction, mathematical acceptance,
independent hosting or v5 completion.

## First selected attempt: preserved fixture-import failure

`search-validation-controls-01` ended `COMMAND_FAILED`, exit 1, before test
execution. `command/stderr.txt` identifies the missing selected fixture import
`transport.test_search_resilience`. The new test source imports that retained
helper, but the selected prior 80-file source map did not include it. The
reviewer's scope check above did not catch that missing transitive test input.
No product algorithm failed and no test passed in this attempt.

Saved outer RESULT SHA-256:
`aa16baa1c6e5c33d72dcd55dc0a8132c03b53c2badd694739e30942b0ef88614`.
The exact failed selection is
`532600e0e9c6e288c4df10682a133d5a9003d368bcef5d4556ea8888a1a962b6`.
Job CPU is 0.703125 seconds; wrapper CPU is 0.34375 seconds, totaling
1.046875 known CPU seconds. Outer wall is 4.774817700032145 seconds.
The child was reaped, Job closed without cleanup errors or requested
termination, and final active/terminated process counts are both zero.
Pre-clock interpreter startup remains outside these totals.

Root separately selects a fresh second attempt with the exact retained fixture
added to the source closure. The failed attempt, original sources and all costs
remain preserved; it is not relabeled as passing or retried in place.

The second attempt also ended before test execution: its newly selected
`test_search_resilience` imports `discovery.test_candidate_query`, which was
still absent. Exact selection:
`8faa071f596d9afadf08bbd70b07a6611fc11cf2f4224e2fa41a2077977e0246`.
Saved RESULT SHA-256:
`75c0013dbcefc4c1e4a442e564ddbfaecbf1e6bc138d96a7a29185e17c096fa7`.
It consumed 0.796875 Job CPU plus 0.375 wrapper CPU = 1.171875 known CPU
seconds, 2.267806699965149 outer wall seconds, with clean zero-active and
zero-terminated closure. Both fixture-selection failures are retained.

Before root's third selection, the complete remaining fixture import was
traced: `test_candidate_query` imports only standard library and already
selected authenticated-index/features/query/store modules, not another test
fixture. The fresh 85-source third selection is
`2c717dd2945b768048d9db3d8f5cf94ff7bd3de144191207e4f808e3762495a2`.
Product helper, facade and test-source identities above are unchanged.

## Third attempt: actual changed-boundary PASS

**PASS for the eight selected metadata-isolation controls, with the stated
inert-owner boundary.** `search-validation-controls-03` records 8 tests,
0 failures, 0 errors and 0 skips; stderr individually reports each selected
case as `ok`. Parent status is `COMMAND_EXITED_ZERO_AND_CLOSED`, exit zero.
Actual loopback evidence records exactly two connections, one malformed reply
and one honest reply, no server errors, and observed server closure.

This reviewer independently rehashed every selected original and snapshot:
85 source pairs match; all 19 retained runtime/data pins match; all 81 recorded
import origins are snapshot files in the selected map with matching bytes and
digests. The selection's actual hash matches the third selection above.

| Evidence | SHA-256 |
|---|---|
| `search-validation-controls-03/RESULT.json` | `d00cc7d97962f9206f6a46354efc30851dd1002f9661e2bcd8611b6e426ba5b7` |
| `search-validation-controls-03/controls/RESULT.json` | `8ca76ddd4b487b1f03d39f645642a33115724bdab634e504228fcaf918589b17` |

Job CPU is 1.59375 seconds plus 0.34375 wrapper CPU = **1.9375 known CPU
seconds**. Outer wall is 3.1372161000035703 seconds and peak Job private commit
33,869,824 bytes. The child was reaped, Job closed without cleanup errors or
requested termination, and final active/terminated counts are zero.
The two earlier failures add 2.21875 known CPU seconds; all three attempts
therefore total **4.15625 known CPU seconds**. No failure cost is erased.

Zero native/proof operations and zero external-network calls are reported and
consistent with the inspected suite. This is a real selected-facade/search/
transport test using synthetic mathematical metadata and inert issuers, not
genuine mathematical admission, full owner construction, independent hosting,
throughput qualification, or v5 completion. No repetition is recommended.
