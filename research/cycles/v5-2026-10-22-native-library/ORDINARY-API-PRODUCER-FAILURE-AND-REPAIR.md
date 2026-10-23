# First installed producer: retained failure and narrow repair review

2026-10-23. Reviewer: `admission_event_audit`. Saved-outcome inspection and
changed-branch source review only. No experiment, native check or test was rerun;
no catalog/Git mutation occurred. The catalog inspection used a read-only,
immutable SQLite connection without importing any product acceptance controller.

## Failed01 remains failed

`ordinary-api-producer-01` selection
`ee94421627b6153b42bd340e8c83594133d2768328ffe1756c30ca65d3cb30fb` stopped in
INITIALIZATION at `ADMISSION_NATIVE_DIAGNOSTIC`. Completed-stages is empty.
The saved native basis invocation itself exited zero with clean closure, but
the installed controller refused before report validation or catalog promotion.
No source construction, candidate binding or contribution admission followed.

The actual basis stdout is **869,841 bytes**, below its 1,048,576-byte cap; stderr
is empty. It contains the unchanged pinned basis worker's inventory/progress
trace and terminates with `DATA_ONLY_SEED_CHECKED units=456 exports=581`.
The report separately describes basis/456 checked units/581 names and a
669,968-byte artifact. Neither log nor saved report is being used to salvage
acceptance. The read-only catalog has **zero roots** and **one FAILED_RETAINED
operation reserving 67,108,864 bytes**. That failed state and output stay intact.

Outer supervision reports exit 1, clean direct-child reap/Job closure, no cleanup
errors or requested termination, and zero final active/terminated processes.
Whole-operation wall cost is **20.0108913 s**; **17.578125 s outer Job CPU** plus
**0.84375 s wrapper CPU** is **18.421875 s known accounted CPU**. Nested basis
CPU of 16.53125 s is included in the outer Job cost, not an additional charge.

| Saved evidence | SHA-256 |
|---|---|
| Outer result | `6612b99aa6ecfbeef19ba7bdc615a5372dd05bdbd29619db2c95425a1254526b` |
| Producer failure | `b6ceb20d65bfd89962de551e81fa4de080571cfe1c34f74358d8db9ae3426a60` |
| Nested basis supervision | `42d4f707ae01df82f2a61be1f2e3522996f77dce469faab095a628c94d567cfd` |

## Cause and repair disposition

The old installed core (`5ff149cd`) required empty stdout for every native call.
The unchanged basis worker intentionally emits a bounded trace. This is an
actual worker/controller contract mismatch, not a mathematical checking failure
or resource exhaustion. The source review preceding the run did not catch this
operability mismatch; the actual failed evidence supplies the correction.

**No blocker found in the narrow selected successor**
`software/v5/ordinary_lean/ordinary_admission.py`, SHA-256
`9653a710a089393d189830a26aa8dd0723ee75859ce577d9713dae569b5e8575`.
An exact diff against the preserved installation changes only the stdout
condition and its explanatory comment:

- Stdout must remain within the selected actual allowance in both modes.
- Nonempty stdout is allowed only when the live grant kind is `basis`.
- Extensions still require empty stdout; both kinds require empty stderr.
- Clean actual worker completion, original deadlines/CPU limits, exact live
  grant/report/module/name/count/artifact bindings and native checks are unchanged.
- Logs are retained, not parsed for success authority. Accepting bounded basis
  diagnostics does not make arbitrary log text a replacement for kernel checking.

The diagnosis does not justify rewriting failed01, promoting its saved artifact,
reusing its allocation or editing installation01. This controller change produces
a different implementation identity: a separately selected fresh installation
and fresh operation are required. No broad prior test campaign or certificate
work is warranted by this one demonstrated interface correction.
