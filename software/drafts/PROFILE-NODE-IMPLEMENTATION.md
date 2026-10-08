# Fresh-install diagnostic patch

Source-only candidate; not applied, imported, executed, or tested. Root alone
applies the unified diff to `py/node.py` in a fresh diagnostic installation
after review. No existing product file or node was changed.

Base `software/py/node.py`: 25,402 bytes; SHA-256
`635847507f823ef71358b0d619935b5581d2ea64c805fd4db2162f0297d40866`.
Patch SHA-256:
`6c3916f4304e1bebb18700a124ebf27547a8485a205e4c6d0a81544cad066462`.

The exact gate is ordinary `submit`, request ID `profile-target-001`, root
`ChunkedReductionStatement`, 643 UTF-8 source bytes, and source SHA-256
`2c1f0832c82e73423d212ca5782ca28ee4088d6ec4c53c4d72f8726e3f76570e`.
No target source or proof was authored or edited here.

The profile surrounds dispatcher construction and its entire `execute` call.
Both the `cProfile.Profile` constructor and `enable` explicitly disable subcall
graphs. `time.process_time` excludes child CPU; normal exception handlers and
store finalization remain in place, with profiler disable in `finally`.

After the ordinary event and stdout response are emitted, the patch attempts
one exclusive-create `dispatcher-profile.json` beside that event. It binds
request/response/source/node digests and exports at most 60 rows, the union of
the top 30 exclusive and cumulative entries. Entry count is capped at 10,000
before ranking, labels are bounded, JSON must fit 64 KiB, and no caller graph
or binary dump is exported. Historical request replay is not a fresh profile.

Diagnostic start/stop/export exceptions do not replace the ordinary reply.
Unavailable profiles emit at most 512 stderr bytes; partial files are retained.
Root must separately pin/census the sidecar: standard supervisor output pins do
not cover this additional file. Profiling overhead remains unmeasured and can
consume existing CPU/time limits; no success or speedup is presumed. Profile
collection memory remains subject to existing Job limits.

This supersedes the earlier two-request vocabulary-profile setup: selected
readiness preparation now requires four vocabulary-onboarding requests followed
by the one proposition-definition submission, totaling five requests, four
stages, 12 pipeline children, and 552 MiB reservation. Defining the proposition
does not prove it. No consumer dispatch, retries, or optimization is included.
