# Ordinary-abort contracts: independent launch review

Reviewed 2026-09-21 by `feasibility_checkpoint_audit`. **Source/launch review
passes for the exact cut below; no additional deterministic test/runner seam
failure found.** This is not a passing execution result, a native recovery
qualification, permission for retries, or evidence of mathematical acceptance.
Root remains the sole executor. This review used only text/JSON reads, file
hashes and filesystem inspection; no product import, process launch, SQL query,
test execution, repair or source mutation was performed.

## Exact reviewed cut

Paths are relative to `software` unless absolute.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `qualification/ordinary-abort-contract-launch-01.json` | 3,708 | `CDFA0CCE205C46166446787AC2E9FF2B1279E7902CEC26B06A3FF4F8D83D99F0` |
| `tests/test_ordinary_abort.py` | 24,491 | `7C23A25C788C788A2056304C78F51B350A54EFBD3723C39634C7D4B9BB10F3D3` |
| `tests/run_state_contracts.py` | 12,029 | `F6DB9EBB9B8573FE6372EF37CAF517BEEB3D131B1406A59415D7CEC657A9A528` |
| `py/recovery_worker.py` | 19,570 | `EB574CEC2090CE3B337E289FCDF76C230B5C5BDB9E94E2DDB9CA39ABDB99C073` |
| `py/recovery_manage.py` | 9,243 | `0E05E3A7094F8B8C1C6D241AC9F513D64533655067B9AA09C43883AFCE90CACA` |

The complete [changed-seam test review](ORDINARY-ABORT-TEST-REVIEW.md), SHA-256
`E0F3AC9E7C9D2F3B444F4FFAB680C6EF41352E43124182F422777C2FA6036908`,
was read. Its reported missing-bound repair is present as `S.read(journal, MIB)`.
The separate [implementation review](ORDINARY-ABORT-CODE-REVIEW.md), SHA-256
`D0C671E379465BAFACDB3C8059FD202903E95A67027BD3CA1552D3ADC294F028`,
now includes the integrated docstring-only delta confirmation. The implementation
auditor's verdict and this launch verdict are separate source gates; neither
substitutes for the later run and outcome audit.

## Pin order, snapshots and fresh allocation

All fifteen launch inputs were independently rehashed and matched in exact path
order, byte length and digest. The order is:

1. `D:\Python314\python.exe`.
2. `tests/run_state_contracts.py`.
3. `py/run_stage.py`.
4. `py/supervise.py`.
5. `py/domains.py`.
6. `py/capacity.py`.
7. `py/storage.py`.
8. `py/node.py`.
9. `py/recovery_worker.py`.
10. `py/recovery_manage.py`.
11. `py/checking.py`.
12. `py/peer_wire.py`.
13. `py/peer_service.py`.
14. `py/peer_node.py`.
15. `tests/test_ordinary_abort.py`.

The inputs total 369,832 bytes. Adding the 3,708-byte launch makes exactly
**sixteen transport pins / 373,540 bytes**, within the sixteen-pin, 16-MiB/file,
64-MiB aggregate transport envelope. The fourteen copied source basenames
(interpreter excluded) are distinct even under case-insensitive comparison.
This is an exact current-suite observation, not a general guarantee for future
registry entries.

The fifteen inputs, launch and two output parents were inspected through their
full ancestor chains: 85 observations, no reparse point. At final review both
allocation roots were absent:

- `E:\Distributed Trustworthy Mathematical Knowledge Network\product-local\ordinary-abort-contract-01`.
- `E:\Distributed Trustworthy Mathematical Knowledge Network\software\qualification\ordinary-abort-contract-01`.

The covered invocation is the pinned interpreter with `-B -E -s -S`, the
absolute reviewed runner and `--launch` followed by the absolute reviewed launch
path. Runtime checks must still re-establish pins and freshness; these observations
do not prevent later filesystem changes or authorize reusing an occupied root.

## Exact envelope and runner seam

The schema-1 launch selects `test_ordinary_abort.py`, eleven tests and allocation
`ordinary-abort-contract-01`. Its dictionaries match the runner constants exactly:

| Bound | Value |
| --- | ---: |
| Worker wall / CPU | 60 / 30 seconds |
| Worker memory / active processes | 512 MiB / 8 |
| stdout / stderr / event | 65,536 bytes each |
| Combined state/evidence endpoint | 268,435,456 bytes; 4,096 files; 8,192 entries |

The reusable runner is a minimal registry adaptation of the already reviewed
metadata-suite coordinator, not an import of the old driver. The selected scope,
count, allocation prefix and nine suite-specific sources consistently drive
launch validation, input construction and exact outcome comparison. Discovery
checks the selected module origin and eleven-test count. A passing result requires
all eleven run, zero failures/errors/skips and the existing cleanup conditions.
The worker receives the fresh external `DTMKN_TEST_ROOT`; existing supervision,
census and CPU reporting retain their previous boundaries.

Per-test endpoint checks allow 16 MiB plus an at-most-1-MiB report, giving a loose
187-MiB suite bound; the coordinator additionally checks the whole 256-MiB
endpoint and final-record headroom. Copying/census are outside the worker Job.
Interpreter startup and final-report write are excluded from reported coordinator
measurement. None of these endpoint counts is a hard transient disk quota or a
bound on the coordinator's entire lifetime. Runtime fit remains unestablished.

## Coverage and residual limits

The eleven methods cover mode/envelope separation; synthetic-receipt source and
command authentication; saturated pending abort; preserved peer stage rules;
byte-exact terminal replay with unrelated active work; request/attempt/active/
initialization guards; twenty incomplete-quiescence cases; injected terminal
write failure; before/after-real-COMMIT uncertainty; and preserved nonempty
synthetic sidecars. Tests hold real owner locks, use actual SQLite transactions,
fail accidental native checker/process entry and mock physical supply explicitly.
No further deterministic interface mismatch was found in the inspected seam.

Twelve stores, thirteen reservations and eleven stages are constructed across
the eleven methods. The receipts, initialized state, stages and quiescence
observations are synthetic. Authentication hashes twelve real files but does
not attest that a historical public process produced the supplied receipts.
The FULL exception is injected; this is not physical disk-fill qualification.
The sidecar is not a real hot journal.

The suite does not execute full config/main handling, wrapper mode-profile
forwarding, worker-main existing-lock selection, real native interruption,
event/stdout loss, or successful checked continuation. Fixture locks do not
qualify worker-main missing-lock behavior. These explicit omissions are compatible
with this narrow launch and must remain visible in its eventual outcome.
An unchanged source cut may proceed to root's separately gated execution; any
passing report must be audited before upgrading this source-only verdict.
