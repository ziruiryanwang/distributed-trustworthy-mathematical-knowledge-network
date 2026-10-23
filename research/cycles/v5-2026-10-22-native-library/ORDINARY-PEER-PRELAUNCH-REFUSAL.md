# Preserved reciprocal prelaunch refusal

2026-10-23. Root invoked the pinned `Run-V5-Check.py` with selection
`ordinary-peer-reciprocal-01.selection.json`, SHA-256
`05737f67915ad626409897fbc3afef423ea6b85dc41f68cb79430a4d98a6cb18`.

The command exited 1 after 0.1925437 shell wall seconds. CPU was not separately
measured. Its terminal exception was:

```text
Run-V5-Check.py line 60: limits = A.limits_checked(s["limits"])
operator/commons.py line 118: LIMIT_RANGE:active_processes
ValueError: LIMIT_RANGE:active_processes
```

The selection requested 10 processes; the preserved supervisor ceiling is 8.
This was a plan/review error, not a product/native rejection. The supervisor
rejected before snapshot/output creation or subprocess launch. Read-only
`Test-Path` confirmed the run01 output directory absent. No owner, native worker
or service ran; no mathematical state was initialized or modified.

Selection01, its source selector and harness remain unchanged. Root prepared a
fresh selection02 that changes only the name and lowers the process cap to 8.
All other source/runtime pins, arguments and limits are identical. The new
selection SHA-256 is
`2e850ea0dff2fe8c47417249403cd624d8baa32bfe337a38cd4f0815dd4eabe9`.
Independent process-count review precedes execution. This is not a retry of an
already executed mathematical operation and does not relabel launch01 as passed.
