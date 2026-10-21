# Independent implementation review: base-profile projection

2026-10-20, adaptive_audit. Source-only review against contract `25618050` and
its independent GO `aefb8930`. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Disposition and exact bytes

**GO for root's one separately selected finite structural control run.**
No blocking source defect remains in the reviewed implementation or controls.
This is not an executed result, installed adoption or v5 completion. I ran no
Python, product code, network, proof, build or experiment; inspections were
read-only source/diff/hash checks. Root owns staging and execution.

| Path under `software/v5/base_projection/` | SHA-256 |
|---|---|
| `client/base_projection.py` | `804147ddb15d9c9758ab8c0b0aebaefcbeefbc98292db262e3849ab25647d2d1` |
| `client/serve_workspace.py` | `d02f6b0478aae47ddabab863b396f363f7190dc2ec59400e65c1d2d28ef8e8cc` |
| `client/serve_advertised.py` | `afe15634b3b73f11a3677a0c6db33abe485493836b028562daf826ea5d39cd72` |
| `distribution.py` | `0db784331ba5ac8966c9b4411385fd2fc734b384a2a5ed3729b74f4bb6bff0e3` |
| `controls.py` | `ddbfaa67a375d2289f6fcf0e352386090ac0137df8f2cade49d02127f3860aa7` |
| `README.md` | `a924634a965c20b91d3552e4c7185b55cd5de31d1ee95069f4252402041f9076` |

Stage-only `research/cycles/v5-2026-10-20/Select-BaseProjection.ps1`:
`248bf17c6c817103aeee215405d7e444dc5f30687046070ee380b5107754008b`.

## Implementation findings

The new helper validates the closed selection/configuration before opening the
workspace, derives one fixed ordinary target path, and requires an actual
supported workspace class with live exclusive ownership and no client/grants.
It reuses actual custody and the no-profile base adapter. Original workspace
adapter/index identity is never replaced. Store admission re-extracts original
opening bytes with the exact export ID; no specialist feature claims are copied.

`ProjectionView` acquires one token before target construction and retains a
partially initialized actual `Store` so constructor-close failures can still be
reclaimed. It releases only its matching borrow after the target is known closed.
Target errors remain sticky failures, even when direct SQLite fallback succeeds;
the source workspace is poisoned on such a cleanup error. The caller model is
explicitly serialized trusted-owner code, not protection from arbitrary code in
that same process.

The selected latest check agrees with existing provider behavior: the requested
hash must equal actual `status().latest` and the verified snapshot, with local-cut
agreement. V2 serving only reopens; it does not materialize. One selected target
feeds the actual provider and advertised namespace, with the original module and
packet stores. Normal termination checks the cut again. Transports drain before
target closure, then the original workspace closes. The extra target is not
mistakenly delegated to the old three-store workspace closer.

The service changes preserve V1 constants, closed fields, default selection and
V1 READY/result shapes. V2 fields/reports are explicit branches. The advertised
proxy carries HTTP V2 plus the validated selector instead of overwriting it with
V1. The distribution change permits only each serving command's matching V2,
preserves that selected schema, retains V1 defaulting and reserved installation
injection, and requires the new helper source in distributions. Local imports
avoid a helper/service import cycle. No wrapper commands or mathematical owners
are added.

Materialization reserves bounded read/export allowance before each attempted
item, stops at first failure and distinguishes an acknowledged prefix from an
unknown current commit. It authenticates final latest only after all returns.
Failure after all acknowledgments but before that check has the explicit
`ALL_ACKNOWLEDGED_CUT_UNCONFIRMED` outcome, with no claimed final cut. The final
bounded report retains costs and cleanup outcomes; missing report remains UNKNOWN.

Root's two implementation refinements are present: a generic exception from
`view.close` cannot bypass original-workspace cleanup in `prepare`; and failed
admission before `Store._budget` resets its work dictionary records unknown
counters instead of double-counting constructor/previous work. Known index
counters and inclusive CPU/wall remain different measures. No implicit retry,
cross-database atomicity, free reconciliation or hidden projection renewal exists.

## Controls and source-closure review

I read all eight selected groups, the overlay/support imports and their actual
API dependencies. They use real codec/group openings, base and fingerprint
indexes, original custody, the real workspace lock, actual provider constructor/
direct dispatch, and authenticated candidate verification. HTTP start/stop and
the location process/adoption are explicitly inert. Synthetic location source
pins test parameter propagation only, never runtime integrity. Network/process
guards surround tested calls after unittest loop infrastructure exists.

Coverage includes wrong namespaces/relabeling; finite pre-mutation refusal;
one selected export rather than an automatic corpus copy; duplicate borrow and
wrong retained config; actual quota failure; postcommit uncertainty followed by
explicit idempotent confirmation; pre-reset unknown counters; source additions
absent from an old target; stale-latest refusal; V1/V2 selection and same-custody
service binding; advertised route/namespace agreement; and failure/cancellation/
actual target-close fallback. Exactly eight new groups run; inherited service
and fingerprint suites are not selected. Generic unexpected helper-close failure
is source-reviewed rather than a separate test case; the explicit close-failure
control exercises actual Store-close failure and direct database fallback.

Pre-execution review caught and repaired these harness/selector defects:

- The source snapshot parent was incorrectly used as project/runtime root.
  The canonical project is now explicit and distinct from relocated source.
- `get_group` was called with locator field names not matching its API; actual
  positional arguments are now used.
- A stale target raises `ProjectionOpenError`, not the initially expected
  `ValueError`; the assertion now checks the actual wrapper.
- Intentional sticky close errors were rethrown during teardown; teardown now
  drains remaining resources while preserving the already tested failure.
- The snapshot lacked imported `client/test_serve_workspace.py`. The selector
  now pins it and ensures the already-present ordinary service source agrees,
  rather than erroneously rejecting that existing source as a duplicate.
- Inert location controls no longer read missing snapshot `.mjs` files merely
  to synthesize unused child pins; the synthetic metadata boundary is explicit.

The final selector revalidates pinned basis `421469bd`, all 147 original sources,
the unchanged runtime pins, the one additional frozen support module and exactly
five reviewed new sources: **153 source snapshots**, not 152 or 154. It stages
only a fresh named selection and controls argv with 45 CPU seconds, 75 wall
seconds, 384 MiB, two active processes and 1 MiB stdout/stderr caps. It does not
execute the selection. The later distribution-build selector is outside this
review; no build is authorized by it.

The README accurately separates preparation, service, partial coverage, structural
discovery and mathematical verification. A passing control run could support
this bounded compatibility/ownership seam, not global recall, live external
serving, useful-growth advantage or final-v5 readiness.
