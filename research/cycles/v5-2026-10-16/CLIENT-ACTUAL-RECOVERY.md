# Actual client 01: exact contract failure and minimal source successor

2026-10-16. Author: `memo_independent_review`. Canonical guard PASS. Initial
assignment was source-only diagnosis; root subsequently selected only fresh
`client/actual_assets02.py` and `client/actual_owner02.py`. No product/test code
was executed, imported or compiled; no Git state was changed. All actual01
sources, plan and evidence remain unchanged.

## Cause, not a speculative hypothesis

The preserved traceback ends at actual01's snapshot `actual_assets.py:105`:

```python
C.fields(params["assets"], RETAINED)
```

The exact retained callee `modules/codec.py:48-50` is:

```python
def fields(value: Any, names: set[str]) -> dict:
    require(type(value) is dict and set(value) == names, "EXACT_RECORD_FIELDS")
    return value
```

`RETAINED` is a dictionary mapping asset names to size/hash pairs. The left
operand is a set; the right operand is a dictionary. They do not compare equal
even when the key collections match. Thus the correctly shaped selected asset
map deterministically refuses. This is a new caller/callee contract mismatch,
not a corrupt asset, unsupported receipt, bad theorem, failed source export or
network problem. The shared strict codec must NOT be weakened to accept it.

Both author's self-review and the independent whole-source clearance missed
this exact type requirement. The earlier clearance is superseded by this
observed failure at that boundary; the source mathematics review is unaffected.
No new broad test campaign is warranted to prove elementary set/dict semantics.

## Actual reached extent and conserved evidence

`main(context)` evaluates `Strategy(context)` before calling `run()`. Strategy's
first assignment evaluates `Assets(context)`; the failing field check occurs
before its asset-reading loop. Therefore no mathematical workspace, grant,
receipt/native/preparation owner, source authoring or Node service was created.
The actual `work/` directory has zero entries. There is no `actual-result.json`
because the strategy's report/run/finally block was never reached. The outer
launcher correctly preserved `BOOT-FAILED.json`, stderr and failed result.

| Preserved evidence under `product-local/v5-client-owner-runs/client-actual-01/` | Bytes | SHA-256 |
|---|---:|---|
| `RESULT.json` | 2253 | `342303c66d75ac3d7987d7ad72eae74b4640417d498f12a742d3ecf8b8bf448c` |
| `BOOT-FAILED.json` | 87 | `c99ab7e76b9858a8a895eec36c74935906186f7044aff90a1f227da8ecf44bc9` |
| `command/stderr.txt` | 1830 | `3ac74b9eee0d5e714f89879ab0c441f771d204f9d4593a718ecf4c180834aaa4` |
| `sources/v5/client/actual_assets.py` | 10738 | `0cef5f4e8ff7590d52f51d73f3fa42ca23ab4ace4a75eeff16dd0df49f68ef87` |
| `sources/owner/actual_owner.py` | 22521 | `2f2f07aa6ac91618120b210abec99ddbef4818332bd2d7915e6b0c837efc1016` |

Selected plan SHA:
`dad9f1d436c71f836d467fe14713d38e975563bd067836996eb292ec0d9b60d2`.
Outer status `COMMAND_FAILED`, direct child exit 1, reaped, Job closed, no
cleanup errors or termination request, final active/terminated processes 0/0.
Known Job CPU is 1.046875 seconds; wrapper CPU is 0.328125 seconds, including
the reported 0.296875 bootstrap subset. Add Job + wrapper only: 1.375 seconds,
not a triple count. Outer wall is 1.4552277 seconds. These are retained costs,
not a refund or authorization to renew the old allocation. Pre-clock interpreter
startup remains unmeasured. Independent outcome audit is owned separately.

## Selected successor: exactly two textual substitutions

Root authorized exact fresh copies of the two predecessor files. Before editing,
their SHA-256 hashes matched the predecessors byte for byte. `apply_patch` then
made only these substitutions:

```diff
# actual_assets02.py
- C.fields(params["assets"], RETAINED)
+ C.fields(params["assets"], set(RETAINED))

# actual_owner02.py
- from client.actual_assets import ...
+ from client.actual_assets02 import ...
```

A read-only exact UTF-8 comparison confirms each complete successor equals its
predecessor with just its shown replacement. No line-ending or incidental
source rewrite occurred. The used predecessor hashes were checked again and
remain unchanged.

| Fresh source under `software/v5/client/` | Bytes | SHA-256 |
|---|---:|---|
| `actual_assets02.py` | 10743 | `4ec62954467e9c2a62a66ffeb4f1ec945b6d33cbe1ae7b484cc1a2869c0b2c69` |
| `actual_owner02.py` | 22523 | `6fa4f0253c0f23bbc3b6d5b4005c40d6f8b40d02251bb4b78e03e3a37f65e12c` |

The bounded static scan of both new owner files found all five `C.fields`
calls: the asset map now explicitly supplies `set(RETAINED)`; the other four
already supply literal sets. No additional field-helper mismatch was found
in these newly introduced files. This is not a claim that every future runtime
boundary or entire repository has been tested.

## Exact next ownership and no duplicate passing work

Root owns a fresh selector/plan/run, with `owner_entry=actual_owner02.py`,
`owner/actual_owner02.py` and `v5/client/actual_assets02.py` selected. Remove the
old helper from the selected import closure unless some explicit unchanged
dependency needs it; do not leave the new module unpinned. All other selected
product/portable/worker/data/runtime bytes and finite mathematical workload
stay unchanged. Independent reviewer checks the exact two-source delta and
emitted selection before root decides any launch.

Do not restart actual01, alter its result, or rerun the passed profile/client
control suites. No mathematics phase passed in actual01, so the intended three
phases have no accepted intermediate output to resume. The necessary fresh
bootstrap is not a repeat of receipt or theorem work; those calls never began.
If a new operation reaches a later failure, its actual reached extent must be
used before choosing another successor. The full v5 goal and affordable-frontier
obligations remain open.
