# Capacity v3 contract suite: independent source and launch review

2026-09-21. Source-only review of the twelve tests, their explanatory note,
integrated implementation paths, `tests/run_capacity_contracts.py`, and the
subsequently supplied exact allocation-01 launch.
The reviewer performed no import, execution, compilation, SQLite query,
service launch, or native work. Native-03 is outside this review.

## Decision

**Source and exact launch review pass for this one native-free allocation.** No
deterministic mismatch was found between the twelve test expectations and the
integrated APIs/refusal ordering. This is not a test result. Root alone may
execute after obtaining the separate integrated-v3 review it requires, with
the exact sources, Python, launch and still-fresh roots checked below. Changed
bytes, reused roots, retries and expanded tests are not covered.

One runner defect was reported and corrected by root: `cpu_complete` previously
remained false unconditionally. The reviewed cut sets it from quiescence and
a finite nonnegative Job CPU observation, before writing the optional copied
supervisor observation. Available CPU/cleanup fields therefore survive failure
of that copy. Coordinator CPU remains separately measured; the Job total must
not be counted twice. Interpreter startup and final report persistence remain
outside the stated measurement scope.

## Reviewed cut

Paths below are relative to `software/`. SHA-256 binds the actual bytes reviewed.
The staged test equals the entire draft plus one final LF; it is semantically
unchanged but **not byte-identical**. Launch pins must use the staged hash.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `tests/test_capacity_v3.py` | 27031 | `5763B56117E9E4DB3E39170D97BE6C206FD8C1F01E8A865B2ECCE04C95D57CDE` |
| `drafts/test_capacity_v3.py` | 27030 | `FAA674F3631FABF62C4F2F6D8CB1F526296E87E00DC8CD7783C1EABB5F4D705F` |
| `drafts/CAPACITY-V3-TESTS.md` | 9208 | `FF0176321C8E728295C74603FC81C6EED1C53CABB4E3738D8A97F744A90541F8` |
| `tests/run_capacity_contracts.py` | 11629 | `9E03F2F6F86749D3A59E5395C6254407C837E8D82163666A47A4E84A65F6FDC0` |
| `py/capacity.py` | 6709 | `B32B19D8FBAEEB2A90561E7C57F5B16CCDD614B2D993AC5BA7E241EAC02889CC` |
| `py/storage.py` | 31354 | `E33E61DF78984C60E60999D53DB515487E41157F29475E0CBCAF12321968637D` |
| `py/admin_worker.py` | 6543 | `CEB61F18F2BF84DE92146119089201B130A96BF9FEDBB95F6A7F85BC92E77244` |
| `py/domains.py` | 4934 | `1FF763737AF54286B3C676DBB8CC4B30B8A34F87F48B9F4145B7AD0954A77EA7` |
| `py/node.py` | 25320 | `DC0B2E20C27290270B595122C33385D51FF629B67EF52B94B97DD8A3990F6977` |
| `py/run_stage.py` | 26509 | `2B2A33DE45490D124F0828F0E1DE15E5C57C91FACD326FD4AE054027C7952F4D` |
| `py/supervise.py` | 18611 | `E5F35C0A88602757ECB7FF899F923F940B588E11E2A7C9C36D51FDBB2DFCAC1B` |
| `qualification/capacity-contract-launch-01.json` | 2578 | `C8FF97C300996E52AC5B88A730B2C0FB035FC50D1D14D808ABBCB184FDAABDD1` |

`admin_manage.py` and `manage.py` were also inspected to identify uncovered
integration paths; neither is imported or qualified by this experiment.

## Twelve discriminators checked

| Topic | Review finding |
| --- | --- |
| Initial/grant parsing | Exact integer checks reject booleans and malformed/type-invalid increments. The cap-only envelope parses to 16384 pages. No physical-supply call is expected. |
| Fresh/legacy schema | Fresh store has user version 3 and ten tables. Existing versions 0, 2, 4 are rejected before writable setup pragmas; byte/length comparison covers the selected legacy files. |
| Exhaustion/replay | Two requests and one actual stage reservation consume `(2,1,144 MiB)`. A third request refuses before mutation; both stored ordinary refusal bytes remain replayable. |
| Two renewals | Additions `(1,1,136 MiB)` then `(1,0,8 MiB)` allow final use `(4,2,288 MiB)`. Grant transactions alter only authorization/grant tables, not usage or mathematical records. |
| Exact grant history | Exact replay and raw-byte conflict precede pending/quota/supply gates. The pending request and all table projections remain unchanged. |
| Grant limit/ID reuse | Unrecorded pending refusal leaves the ID reusable. Sixty-four commits fit; the next refuses, while the first replays. Reopening bounds per-connection SQL VM accounting. |
| Metadata expansion | Nine bounded near-2-MiB records fit below the 6144-page ordinary tier while crossing 4096-page admission headroom. The 32-to-64-MiB administrative expansion allows admission. This does **not** exercise `SQLITE_FULL`. |
| Status read-only | Actual administrative `run` uses the owner lock and read-only store. Uninitialized and pending/exhausted cases compare every selected state file's content and length. |
| Absent/BUSY status | Missing state/database remains missing; real same-process, second-handle Windows lock contention must return BUSY. The platform assumption is tested, not mocked. |
| Terminal refusal | Acceptance-bearing/wrong-key/oversize/in-transaction replies refuse. Actual precommit rollback removes the unpromoted record; terminal-only completion changes request/meta state without refund. |
| Commit uncertainty | Four cases inject before/after actual COMMIT for ordinary and renewal paths. Same-connection mutation is blocked; reopening exposes the actual committed or uncommitted state. These are synchronous fault injections, not crash/fsync tests. |
| Supply helper | Real validation/arithmetic with mocked Win32 APIs covers the listed volume/space/profile cases. No actual host volume or free-space observation is established. |

Snapshots read the ten fixed tables with at most 128 rows each. BLOB hash/length
comparison does not pretend to retain independent duplicate raw copies.
Synthetic initialization and empty provider snapshots establish bookkeeping
prerequisites only; no accepted theorem/context is manufactured. Most direct
store calls occur without a held owner lock, under exclusive single-process
fixture ownership. This does not qualify concurrent access.

## Runner and exact launch contract

The runner accepts exactly twelve tests and only `test_capacity_v3.py`. Its
ordered ten source pins are: Python, the runner, `run_stage`, `supervise`,
`domains`, `capacity`, `storage`, `admin_worker`, `node`, and the staged test.
The transport additionally binds the exact launch file. Coordinator and worker
both verify the selected source pins; module-origin checks cover the loaded
supervision and test/product modules. The test's native/process fences are
installed after imports, so reviewed source and a trusted Python/standard-library
runtime remain assumptions, not an arbitrary-code sandbox guarantee.

The reviewed allocation is `capacity-contract-01`: an external fresh
`product-local/capacity-contract-01` fixture root and a separate fresh
`software/qualification/capacity-contract-01` evidence root. Both were absent
at exact-launch review. All ten ordered source paths, lengths and hashes match
the actual files. The pinned Python is `D:\Python314\python.exe`, 106208 bytes,
SHA-256 `03168C01B7B7491423350E82C26FEE71F35B43694D1319D3C668BDA6903A0C38`.
Sixty full ancestor observations across the ten inputs, launch and two output
parents found no reparse points. The exact JSON has schema 1, twelve tests,
the single expected suite, and the limits below. No source import or Python
version command was used to obtain this comparison; runtime/SQLite startup
checks remain falsifiable requirements of the selected worker.

The covered command is the pinned Python with `-B -E -s -S`, the absolute
`software/tests/run_capacity_contracts.py` path, and `--launch` naming the
absolute `software/qualification/capacity-contract-launch-01.json` path under
`E:\Distributed Trustworthy Mathematical Knowledge Network`. The runner itself
rechecks inputs/freshness before dispatch. Do not reuse a failed allocation or
infer authority for automatic retry.

The worker tree has 60 wall seconds, 30 aggregate Job CPU seconds, 512 MiB
private-commit limit, requested public-eight process profile, and 65536-byte
stdout/stderr/event bounds. The supervisor launches suspended, attaches the
Job, resumes, checks output/request binding, and requires final quiescence.
Requested process limits must not be described as exact Python-process counts:
Windows console helpers can contribute processes. Polling and bounded cleanup
can outlast the nominal workload window; overruns cannot pass qualification.

The test retains at most 24 MiB for metadata pressure, 8 MiB per other method,
and 128 MiB aggregate; each traversal is bounded by 1024 entries/256 files.
Reports count toward those bounds and may exist even when tests fail. The
runner independently limits the post-quiescence fixture/evidence endpoint to
256 MiB, 4096 files and 8192 entries, reserving census/result space. These are
endpoint checks, not hard transient disk quotas. Coordinator copying/hashing
and census run outside the worker Job; no whole-coordinator hard CPU/wall
ceiling is claimed. Sixty seconds is a falsifiable allocation, not a predicted
pass time.

## Central remaining integration gap

The suite does not call `Dispatcher.execute`. Before claiming v3 dispatcher
failure-path qualification, add a small separate native-free discriminator:

- Trigger real SQLite FULL during an ordinary visibility transaction after a
  successful reservation. Retain its SQLite code and confirm rollback, no
  visibility promotion, exact terminal-only `METADATA_SPACE` refusal/replay,
  and preserved consumed charges. Bound any pressure-writing fixture explicitly.
- Inject dispatcher ordinary COMMIT uncertainty before/after actual commit;
  check BLOCKED/unknown behavior, no attempted clearing on that connection,
  and committed-response replay versus preserved pending state after reopening.
- If terminal-only persistence fails, require BLOCKED/uncertain reporting,
  never a falsely durable REFUSED reply or an acceptance claim.

This supplemental work is a separate reviewed allocation, not permission to
expand the present twelve tests or launch. Administrative configuration/CLI
dispatch, stdout/event persistence, actual physical-supply observation, native
renewal behavior and broad crash recovery likewise remain outside this suite.
Its narrow potential pass supports capacity/store/admin-run contracts only;
it does not establish useful mathematical growth or complete the project goal.
