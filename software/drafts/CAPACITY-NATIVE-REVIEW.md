# Native capacity 01: independent source and exact-launch review

2026-09-21. **The corrected source cut and exact launch pass review for one
seventeen-CLI allocation with two receiver stages.** This is not a native
result, performance prediction or permission to retry a failed allocation.
The reviewer performed no import, build, execution, SQL connection/query or
product edit. Only this review was authored.

## Blocker found and resolved before execution

The original worker expected bare `STAGE_QUOTA` at the exhausted submission.
Actual control flow is `store.stage` raising `storage.Refusal`, then
`checking.public` wrapping that non-CheckingFailure as
`SELECTED_CHECK_FAILED:Refusal:STAGE_QUOTA`; the dispatcher returns the wrapped
code. The original expectation would deterministically fail after bootstrap
and request reservation.

Root corrected only the prospective worker/specification and launch pin to
require the exact existing wrapped code. The product, acceptance boundary,
quota checks and expected table/charge deltas are unchanged. The corrected
worker was re-read and authenticated. No other deterministic source blocker
was found; actual native success remains falsifiable.

## Exact reviewed cut

Paths are relative to `software/` under
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `tests/capacity_native_worker.py` | 38978 | `C75D06A037CE1F81528414F2B3DA989A933F3830113BE5DA6F458AC4852BF642` |
| `tests/run_capacity_native.py` | 15740 | `36B497D0DE637312B97367CCF8784B9202821462DA7A7DB2439315C1CCA47355` |
| `drafts/CAPACITY-NATIVE-IMPLEMENTATION.md` | 10122 | `16308002B9DC0D878F92AB9E898327CF103A7CE8422AD1CA7B0A19A53FC2BDD8` |
| `drafts/CAPACITY-NATIVE-DISCRIMINATOR.md` | 11935 | `437B4C152CB5074C1837AC280688788C838525E8B91CDB822DAD853620901C4B` |
| `qualification/capacity-native-launch-01.json` | 41627 | `34532BE8C0D75D36506CC2A1CEF1CA39528220C29620A57A75E487C50AB7DEFA` |

All eight ordered outer pins match actual paths/bytes/hashes: Python, new
coordinator, new worker, `scenario_profile.py`, `run_stage.py`, `supervise.py`,
`domains.py`, and Lean. The launch is the ninth transport pin. Python remains
`D:\Python314\python.exe`, 106208 bytes, SHA-256
`03168C01B7B7491423350E82C26FEE71F35B43694D1319D3C668BDA6903A0C38`.
Lean is `runtime/lean-4.34.0-windows/bin/lean.exe`, 83456 bytes, SHA-256
`A8040E2CAB341C12116AB591FED9F761816F5F6B08554F6CC1680E86DFBBA0A2`.
The existing helper pins match the previously reviewed profile/containment
cut. These executable hashes do not independently authenticate every runtime
DLL, standard-library file or Lean runtime resource; the selected runtime
remains trusted.

The product manifest was independently enumerated and compared in ordinal
POSIX-relative order: **101 files, 3474488 bytes**, all exact matches. It
contains four selected root files, direct `py/*.py`, and recursive regular
`native/` and `assets/` inputs, including all three capacity/admin modules.
It excludes old builds, databases, drivers and prior outcomes. Both programs
independently regenerate this exact inventory; the worker copies and pins a
fresh installation and rechecks installed sources at completion. No old test
driver is imported, and native03's preserved v2 installation is not selected.

Both `product-local/capacity-native-01` and
`software/qualification/capacity-native-01` were absent. There were no reparse
points in 769 full ancestor observations over selected inputs/manifest files,
launch and output parents. The covered invocation is the pinned Python with
`-B -E -s -S`, absolute `tests/run_capacity_native.py`, and `--launch` naming
the exact launch above. Source bytes and roots must remain as reviewed; the
coordinator rechecks them before dispatch.

## Scenario and real operating paths

The worker matches the discriminator's exact sequence: two preparation CLIs,
eight ordinary CLIs, seven administrative CLIs. The ordinary calls comprise
four actual reservations, one pre-reservation quota refusal, and three exact
replays. Administration comprises three fresh statuses, two fresh grants,
and two exact grant replays. There is no publication, admission, inspection,
socket, recovery, extra status, source repair or unexpected retry.

Fresh support is built through installed `build.py`; configuration selects
schema 3, five common packages, no peers/offers, initial authorization
`(2 requests, 1 stage, 144 MiB)` and 32-MiB metadata. Stage plans remain schema 2.
The fixed LF-terminated noncomputable composition source and selected root are
identical for the refused and renewed submissions. No accepted row, context,
proof, support output or response is fabricated.

| Checkpoint | Used `(requests, stages, MiB)` | Authorized |
| --- | --- | --- |
| After genuine bootstrap | `(1,1,136)` | `(2,1,144)` |
| After exhausted submission | `(2,1,144)` | `(2,1,144)` |
| After G1 | `(2,1,144)` | `(3,2,280)` |
| After renewed checked submission | `(3,2,280)` | `(3,2,280)` |
| After G2 | `(3,2,280)` | `(4,2,288)` |
| After renewed info and all remaining replays/status | `(4,2,288)` | `(4,2,288)` |

Expected final charge is 301989888 bytes, never refunded. Bootstrap and
successful submission allocate receiver IDs 0/1 with one/five pipeline
commands; fresh support separately has one stage/two compilations. These
reservation/command counts are not physical disk usage or OS-process counts.

Actual supply checks remain enabled: configure, new-store initialization,
four admissions and two fresh grants. The worker checks genuine helper-shaped
NTFS samples, no `mocked` marker, the required-space formula, remaining bytes
and unchanged metadata cap. Status checks three fresh observational samples;
insufficiency itself may be reported without claiming a reservation. Query
failure stops the scenario. Finite samples do not guarantee future disk space.

## State, receipt and replay binding

The worker authenticates and imports installed storage/capacity only to use
the existing owner-lock implementation; it constructs no ControlStore or
checker. State mutation occurs through the installed public CLI paths.
Each table snapshot holds `owner_lock(create=False)`, refuses nonempty SQLite
sidecars, opens `mode=ro`, enables query-only/memory-temp/no-mmap, and checks
SQLite 3.50.4, schema 3 and 4096-byte pages. Bounds are 32-MiB database,
100000 VM steps and 128 rows per each of ten fixed tables. BLOB bytes are
retained exactly as hex; page/freelist observations accompany snapshot pins.

File maps are outside the byte lock so the lock file can be read. Their safety
premise is complete prior CLI quiescence and an otherwise idle trusted owner
fixture, not adversarial concurrent writes. No observer erases a sidecar or
recovers a database. The quota probe and all statuses compare complete
state-file byte/length maps; administrative scratch is separate retained cost.

Grant deltas independently reconstruct the exact old/new authorization and
stored grant response, changing only authorization and one owner-grant row.
The exhausted submission and renewed info have exact ordinary
reservation/attempt/terminal deltas. All five planned replays compare original
response bytes and all ten tables, require the appropriate historical flag,
and allocate no stage; ordinary replay also forbids admission supply sampling,
and grant replay forbids new-grant supply sampling. G1 replay returns its
original historical usage after later work has consumed the grant.

Ordinary public receipts have the exact twelve pins used by `manage.invoke`;
administrative receipts have the eleven used by `admin_manage.invoke_admin`.
The worker checks distinct module/command/event roles, all five receipt file
pins, raw I/O digest binding and clean supervisor completion. It preserves
available direct/nested observations before interpreting expected reply state.
Administrative records have no ordinary `origin_directory`; their limits and
1-MiB diagnostic endpoint are checked separately.

Native stage IDs, purposes, directories, stored reservations, plan/receipt
hashes, schema/domain bindings, step counts and checker metrics are checked.
The accepted artifact binds source digest/root and bootstrap context; head C0
and provider cut zero remain unchanged. Earlier work-file bytes and earlier
request/record/stage rows must survive. Independent outcome audit must still
bind the actual bootstrap, source capture, candidate replay, inverse replay,
canonical definition type/body and allowed dependencies. The readable source
and worker's definition/universe profile do not alone establish those facts.

## Containment, costs and boundary

The outer-sixteen adapter is unchanged: 450 wall seconds, 450 Job CPU seconds,
6144 MiB private commit and 65536-byte worker stdout/stderr/event ceilings.
Ordinary public-eight and native-one profiles stay unchanged; administration
uses 10 wall seconds, 5 CPU seconds and 128 MiB. Nested feasibility is an
empirical property of the already qualified shape, not proof this new native
allocation will succeed. Auxiliary OS processes may contribute to counts.

The outer Job, not an unbounded direct `wait()` alone, contains the worker,
wrappers and descendants. Coordinator CPU/cleanup facts are saved before
success assertions. Outer Job CPU includes descendants once; nested CPU must
not be added again. Coordinator CPU is separate and total-CPU completeness
remains conservatively false because startup/final-persistence endpoints are
unmeasured. Census requires genuine outer quiescence, including failed prefixes.

The combined endpoint is bounded to 1 GiB/16384 files/32768 entries, reserving
census/result space. Preservation maps independently bound 512 MiB/8192 files/
16384 entries; snapshots/reads also have finite per-file limits. External Lean
runtime is excluded and identified. These are endpoint checks, not hard
transient disk quotas. Unexpected refusal, ambiguity, mismatch or cleanup
failure stops and preserves the prefix; no extra grant/stage/retry is covered.

The strongest immediate result is
`PASS_PENDING_INDEPENDENT_OUTCOME_AUDIT`. A later audited pass supports finite
renewed operation with one private checked artifact, not indefinite capacity,
distributed replication, autonomous discovery, useful mathematical growth or
completion of usable v1.
