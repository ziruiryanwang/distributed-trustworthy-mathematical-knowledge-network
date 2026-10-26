# Correct one demonstrably undersized test allowance

2026-10-26. Root's source-only correction; no product change or automatic retry.
The failed public01 operation, source snapshots and outputs remain unchanged.

Root read/adopts the independent failure/delta review in `OUTCOME.md`, checkpoint
SHA-256 `ce427f2f654d7f0c3f88011c0e35fcb727b870ac64182389c16ef55fee4ffdb4`.
The one fresh public02 check is now selected under exact selection SHA-256
`2083852659a836288863be4ed5e735047a4724e377af31d0a0ae59b013c2cfb6`.

Public01's Lean stderr is `INTERNAL PANIC: out of memory`. Its worker refuses
`BASIS_QUERY_NATIVE_EXTRACTION_FAILED`, the parent publishes `QUERY_NOT_READY`,
and the outer test fails with clean shutdown and zero remaining processes.
No AST, usable hints or mathematical acceptance was produced. Outer cost was
4.8663814999 wall seconds, 2.34375 inclusive Job CPU plus 0.578125 runner CPU
= 2.921875 known CPU seconds; peak outer commitment was 852,045,824 bytes.
Its inner 768-MiB Job observed 807,571,456 peak commitment bytes.

The relevant retained successful type extraction is
`experiments/v5-local-checks/ordinary-query-public-01/public/calls/01-query-local-SUPERVISION.json`.
It records 854,691,840 peak Job commitment bytes (about 815 MiB), 1.546875 CPU
seconds, clean closure and a 1536-MiB allocation. Therefore the proposed 768-MiB
test allowance was below an already observed comparable startup requirement.
This is not evidence of global RAM scarcity or a need to reopen certificate work.

Select only a new `test_public02.py` entry after independent delta review. It
hash-loads the exact used `test_query.py`, permits only its public mode, and
changes only `LIMITS.memory_mib` from 768 to 1024. The query implementation,
question, package, codecs, all other child allowances and the 1280-MiB outer
ceiling remain unchanged. No controls rerun or second negative extraction is
needed. It still performs exactly one public invocation under a fresh output.

The retained prior test source and this short adapter are included together in
the new exact snapshot. A clean result remains subject to saved-output audit;
failure remains terminal for this allocation. Review may authorize one fresh
check, not retry loops, budget renewal, new native support or unrelated work.
