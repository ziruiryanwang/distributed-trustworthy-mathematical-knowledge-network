# Context-selection implementation and contract-harness review

Source inspection only, 2026-09-21. No Python, product or test module was
executed, imported or compiled by this reviewer. No database was opened or
changed. The reviewer writes only this new review note. Prior peer/recovery
installations and qualification evidence remain outside this task.

## Disposition

`EXACT_LAUNCH_REVIEW_PASS` for the single repaired launch identified in the
final addendum. The context-selection implementation and repaired contract
harness have no remaining identified blocking defect within the stated
metadata-only, stable trusted-owner profile. The two initial harness findings
below are resolved. This is source/launch approval, not an executed test pass
or native mathematical qualification. Initial pins preserve the rejected
handoff; the final addendum identifies the approved exact bytes.

## Initial identities actually inspected

Paths are relative to `software/`; values are actual file SHA-256 values.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `drafts/CONTEXT-SELECTION.md` | 10756 | `eca26c33892d22fefcdd6b237aa5906f339f51581d11f96bde9e2e57499a4004` |
| `tests/test_context_selection.py` | 24562 | `709c78ce62d8a786eb550aff3b99a61db9a428f4cf84f8b4f683035903a0a78e` |
| `tests/CONTEXT-SELECTION-TESTS.md` | 8781 | `ddf774ad3f7a8f5551ba1b0d8a60b63464a06c6242840f9dab69423331c3cf34` |
| `tests/context_contract_worker.py` | 2631 | `c7a3f922f6d31dbf0b04779ec8feefdc13828f8257ee8ba96b44ce924ef04525` |
| `tests/run_context_contract.py` | 5375 | `7535f6e26b426d3c8596f3d53dc067c72dd73bf9fdd13dcb7539617be6189945` |
| `py/node.py` | 24887 | `5e2368e04bd0f12cc752bfe12e3949a2867b7f6683ec47b4973fdb635e9233e9` |
| `manage.py` | 12648 | `21a1788157c6298486cab9a31a0624751264f8898e17528049d873599666f021` |
| `API.md` | 10219 | `5c6f3f6a53cb689c17db05da6ad54ec917e81ee5d421768df9bfea0850cf634e` |

The initial suite has exactly 23 `test_` methods: eight package-limit/config
methods and fifteen dispatcher/store methods. Table-driven subtests are not
additional methods or evidence of execution. Root subsequently proposed an
explicit ABA control, which requires a new suite pin and expected count 24.

## Initial harness findings

1. **Blocking: unsupported stderr ceiling.** The initial coordinator sets
   `stderr_bytes` to 131072. The unchanged `supervise.DEFAULTS` ceiling is
   65536, and `Transport.__init__` rejects a larger override with
   `SUPERVISOR_LIMIT:stderr_bytes` before any worker is created. Use an
   allowance within the existing ceiling; do not modify the frozen supervisor
   merely to make this test launch possible.
2. **Blocking: missing retained-fixture accounting.** The initial coordinator
   has a worker Job and output limits but no retained fixture/evidence census
   or retained-byte grant. `CONTEXT-SELECTION-TESTS.md` explicitly delegates
   that accounting to the enclosing reviewed worker/supervisor. Add bounded
   post-quiescence file/count/byte observations and make a successful outcome
   conditional on the declared retained allowance. Preserve failure evidence;
   a census failure must not erase the already observed worker cost/cleanup.

Two additional source-completeness improvements were communicated to root:
retain exact selected source copies so later development edits do not destroy
historical auditability, and include `py/checking.py` among launch pins. The
suite reads/hashes that file into synthetic configurations, although the
checker is never imported on these paths. Adding it still fits the existing
16-pin supervisor bound when Python and the generated config are included.

## Implementation reasoning

The `node.py`, `manage.py` and API changes were compared directly with their
retained counterparts under `product-local/recovery-01/install/`. They add the
ordinary `select_context` operation and fresh-configuration package ceiling;
they do not alter the frozen installation or the underlying store/checker.

The ordinary envelope limits and owner/client split apply before dispatch.
`Dispatcher.execute` still performs exact-byte prior-request lookup before
reservation, so a terminal retry returns its stored bytes before considering
the current head or allocating another allowance. Different bytes under the
same ID conflict; a pending prior request remains blocked. A fresh selection
uses the unchanged ordinary request-byte grant and immutable attempt marker.

Prepare requires initialization, exact `{context, selected}` arguments,
authentication of the expected client-owned context, equality with the
current head, and authentication of the selected client-owned context. The
short commit transaction repeats the record ownership/binding checks and
expected-head comparison, sets only the client head, and writes the terminal
reply/clears the active slot in the existing transaction. The normal rollback
path therefore covers the head and terminal write together. A new no-op
selection succeeds and consumes its ordinary reservation.

Success has exactly the contract's fields, including previous/selected
contexts, `changed`, `context_record_authenticated: true`,
`mathematicalAcceptance: false`, `live_context_status: UNCHECKED` and zero
native stages. There is no `accepted: true`, fresh description, context
construction or publication. Existing record authentication checks indexed
kind/client, raw-record digest and embedded config/client/kind. It does not
claim the selected context's live dependencies remain available.

Neither selection branch invokes checking, peering or stage allocation.
Existing `Checker.context` still authenticates evidence, validates selected
packages and checks the union plan. Both `admit` and `submit` still call it
and use their unchanged ordinary native paths. The peer-recovery allowlist
remains exactly `peer_find`, `peer_acquire`, `expose`; a pending selection is
not newly recoverable by that worker. A metadata selection therefore does
not prove live-byte validity or solve native/general crash recovery.

`context_package_limit` requires exact integer common-count 1..16 and exact
integer cap between that count and 16, rejecting booleans and floats.
Configure calls it before file pinning, build inspection and directory
creation, using its fixed five common packages and an omitted-option default
16. The CLI parses `--context-packages` as an integer. `load_config` checks the
actual common-list length and `limits.get("packages", 16)` without editing
the raw configuration or changing its hash. The existing checker uses the
same omitted-field default. This is a new immutable configuration choice,
not mutation of an initialized node's allowance.

## Test adequacy and declared synthetic boundary

The fixture executes the real request parser, dispatcher, `ControlStore`,
SQLite schema and transactions under a real owner lock. Its initial context
records, initialized bit, candidate/artifact/publication metadata and missing
dependency paths are explicitly synthetic. They are suitable for this narrow
metadata contract and must not be described as checked contexts, native
acceptance or an actual publication experiment.

Successful and refusal paths compare all eight tables against an independently
constructed expected delta: ordinary request/byte charge and attempt marker,
one terminal request, cleared active slot, and only the permitted head change.
Fixtures contain nonempty other-client and retained knowledge metadata, so
preservation assertions are not all vacuous. Both expected and selected
ownership/kind/unknown-handle errors are covered. Parser failures distinguish
pre-reservation refusal from argument/stale-head errors after reservation.

The suite covers a charged no-op, missing live files with `UNCHECKED` success,
success replay after later head movement, stale refusal replay after the head
later matches, byte-different identity conflict including whitespace, and a
pending retry with no new reservation. Commit controls separately change the
head or corrupt either context's raw bytes after prepare, then verify refusal
and unchanged state. An injected first-terminal-write failure exercises the
real surrounding transaction rollback; the subsequent ordinary refusal uses
the real terminal method. These are intentional synthetic fault controls,
not fabricated supervisor or mathematical evidence.

Fail-on-use mocks guard only checker, peering and native-stage entry points;
they produce no fake success. Dispatcher/store logic and transaction machinery
remain real. The tests assert those guards were never called, no checker or
peer instance was created, native counters remain zero and no work directory
appeared. Test directories are exclusive and retained, not deleted at cleanup;
cleanup releases guards, the database and owner lock.

Cap controls cover every valid common-count/cap pair, invalid exact types and
bounds, actual common-list length, omitted defaults and raw config identity.
Configure preflight intentionally stops at the first pin for valid input; it
does not claim successful native-capable configuration or CLI parser coverage.

The worker discovers only `test_context_selection.py`, requires the selected
Windows/Python startup profile, binds the fixed new fixture root, and requires
the exact expected method count with zero skips and a successful unittest
result. Its response and event are authenticated by the enclosing existing
supervisor. Native-stage count zero is a source/guard-based conclusion for
this harness, not a newly instrumented census of arbitrary native processes.

## Launch and outcome requirements

No launch was executed by this reviewer. The initial read-only check found
both exclusive roots absent: `software/qualification/context-contract-01/`
and `product-local/context-contract-01/`. Freshness must be checked again at
launch. The fixed fixture root is outside and does not contain `software/`.
Failure must retain the actual outcome without repair, deletion or retry.

The intended worker allocation is one supervised unittest process tree,
60 seconds wall, 30 seconds Job CPU, 512 MiB Job memory and at most eight
active processes. Output ceilings must remain within the existing supervisor.
The trusted coordinator remains outside that Job, so total CPU and outer
memory are not completely metered. Retained accounting is an endpoint
observation, not a hard transient disk quota.

Before approving an exact launch, review the repaired coordinator/census,
final suite pin/count, source copies and launch pins/limits. After the one
execution, inspect the real raw supervisor for direct reap, final active-zero,
checked Job close, costs and output metadata; actual worker outcomes and
fixture count; retained-file census and bytes; and the preserved source cut.
An assertion pass alone does not supply cleanup or native qualification.

The suite deliberately does not establish live selected-byte refusal on later
mathematical use, successful native configuration, package-cap saturation,
real admissions/source reuse, growth, concurrent writers, hostile-owner
security or general crash recovery. Those remain separate qualifications.

## Final repaired source and exact-launch addendum

Disposition: `EXACT_LAUNCH_REVIEW_PASS`, 2026-09-21. The repaired coordinator
was read in full, the added ABA test inspected, final identities checked, and
every launch pin independently compared with actual bytes. Root may execute
this one separately allocated launch. This adds no replacement-run allocation
and no authority to erase fixtures, repair state or silently rerun a failure.

| Final changed file | Bytes | SHA-256 |
| --- | ---: | --- |
| `tests/run_context_contract.py` | 8381 | `c32dfc67356078cc484ab50f79160d93ed3f2f8237e17a1724851fb29ba748fc` |
| `tests/test_context_selection.py` | 24942 | `faf6944bdc4d43a0945c01616280b5d173a9200d07a3f9bd5c11e960e6780ffe` |
| `tests/CONTEXT-SELECTION-TESTS.md` | 8956 | `c63f82fa6e5f99fefc143a2253eed3dcbf9ee7bb5aa3ba63fad0c78888af0e09` |

The worker, product implementation and API retain the earlier table's exact
identities. The completed suite contains 24 methods: eight cap/configuration
and sixteen dispatcher/store methods. The added ABA control constructs an
unexecuted request at A0, performs A0 to A1 and A1 to A0 selections, then
executes the original request to A2. Each transition uses the ordinary
dispatcher and full expected ledger delta. This checks the contract's
immutable-content-handle semantics; it does not imply epoch cancellation.

The reviewed launch is `qualification/context-contract-launch-01.json`,
3,618 bytes, SHA-256
`1b671fcac4122456867ccced647b629e8ef5c70cc085b3e1633b4050197ddc38`.
Its invocation is `D:\Python314\python.exe -B -E -s -S` followed by the
absolute `software/tests/run_context_contract.py` path, `--launch`, and this
absolute launch path. The launch has schema 1 and exact expected count 24.

All 15 ordered launch pins match actual paths, lengths and SHA-256 values,
totaling 338,320 bytes: the Python executable followed by these fourteen
`software/` source files in the coordinator's exact order:

```text
tests/run_context_contract.py
tests/context_contract_worker.py
tests/test_context_selection.py
manage.py
build.py
py/node.py
py/storage.py
py/domains.py
py/run_stage.py
py/supervise.py
py/peer_node.py
py/peer_wire.py
py/peer_service.py
py/checking.py
```

The selected Python executable is 106,208 bytes, SHA-256
`03168c01b7b7491423350e82c26fee71f35b43694d1319d3c668bda6903a0c38`.
This pins the executable, not its full standard-library distribution. Selected
launch-pin files and their traversed ancestors had no reparse-point attributes.
Both exclusive evidence/fixture roots remained absent at final inspection.
Root must retain those freshness and stable-input premises at invocation.

The repaired stderr allowance is exactly 65,536 bytes, within the existing
supervisor ceiling. Worker limits are exactly 60 wall seconds, 30 CPU seconds,
512 MiB memory, eight active processes, and 65,536 bytes each for stdout,
stderr and event. The generated config adds one pin to the 15 launch inputs,
giving exactly the supervisor's supported 16 pins. `checking.py` is now bound
as a fixture-read input despite never being imported by this suite.

The coordinator saves all fourteen selected source files (232,112 bytes)
under the fresh evidence root, checking each against its selected launch pin.
The worker executes the original selected paths, which the supervisor pins
again. Retained copies support later historical outcome audit without
requiring mutable development sources to stay unchanged forever. This relies
on the same stable trusted-owner premise as the rest of the experiment; it is
not an OS-enforced immutable-source sandbox.

Actual worker CPU and cleanup observations are collected before public test
success/count interpretation. Census occurs only after the raw receipt says
direct child reaped, final active-zero, checked Job closed, and no cleanup
errors. The new iterative census rejects reparse/nonregular entries and is
bounded to 8,192 entries, 4,096 files and 67,108,864 bytes across the new
fixture and evidence roots. File hashing also retains the pin routine's
16 MiB per-file ceiling. The census includes source copies and all observed
outputs; success additionally charges the census and final result with a
conservative 4,096-byte allowance for remaining result fields. A census or
final-bound failure changes the result to failure while retaining prior
worker cost/cleanup. No deletion is used to satisfy the cap.

`elapsed_seconds` starts after setup/source snapshots and includes the later
transport/observation/census work; it is not total coordinator lifetime.
Worker Job CPU is the measured CPU grant. Coordinator setup, copying,
interpretation and census remain outside that Job and incompletely metered.
This narrow profile therefore claims neither full CPU accounting nor an
outer hard coordinator deadline, memory limit or transient disk quota.

Subject to the identified exact pins and fresh-root premises, the two initial
blockers are resolved and no further source blocker was found. Outcome
qualification still requires the separately retained actual worker result,
raw cleanup receipts, exact count, source snapshots and bounded census.
