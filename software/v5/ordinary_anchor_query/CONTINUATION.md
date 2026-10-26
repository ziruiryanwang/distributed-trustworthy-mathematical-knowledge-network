# Test-only syntax correction after controls01

2026-10-26. Root selects this fresh test-source successor only. Product `query.py`
is unchanged. Original `test_query.py`, PLAN, REVIEW, inputs and controls01 failure
remain frozen and charged; no result is relabeled and no allocation is renewed.

## Failure and exact correction

Controls01 stopped before importing the subject: Python reported an unclosed
list at `test_query.py:680`. Root reports clean closure and 0.21875 total observed
CPU seconds. No control group, native query or mathematical result passed.

`test_query02.py` is an exact copy of the original test with one inserted ASCII
`]` byte at the end of line 680, closing the `expected_paths` list. This changes
neither the public import-selection expectation nor any test case or allowance.

| Source | Bytes | SHA-256 |
|---|---:|---|
| Frozen `test_query.py` | 47050 | `2817e4ffd3f6b925e34bc111e775f0bc95acdab41c787a4e5998f71fbad6d4ee` |
| Fresh `test_query02.py` | 47051 | `2f9e6cd553c8ae84dcd6f95722e2d338a526ba2b06c4a1d7224f2baf0d7d58f0` |

The authorized data-only check used `D:\Python314\python.exe -I -S -B` to read
both files, assert exact equality after that one-byte insertion, and call
`ast.parse` and `compile` on the successor bytes. It returned zero with
`DATA_ONLY_SYNTAX_PASS; EXACT_ONE_BYTE_APPEND_AT_LINE_680; NO_IMPORT_OR_EXECUTION`.
No compiled code object was executed; no subject import, test, pycache, native
call, owner/custody API, network or Git operation occurred in this correction.

## Continuation boundary

Independent delta review must precede root's separate fresh controls02/public02
selections. Their harness argv uses `test_query02.py` in place of the frozen
PLAN's `test_query.py`; all other interface, scope, fixture pins and proposed
limits remain unchanged. Fresh output directories and exact source selections
are required. The original pre-import failure remains evidence, not a pass.
