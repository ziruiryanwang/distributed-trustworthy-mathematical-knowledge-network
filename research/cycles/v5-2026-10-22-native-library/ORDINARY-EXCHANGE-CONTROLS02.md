# Protocol control02: bounded fixture process census

2026-10-23, source-only author checkpoint; no execution or product edit.
Root selected this narrow successor after protocol01's retained failure.

Root reports the real protocol exchange completed `EXTRACTED_AND_CLOSED` with
exact replies/transcripts, complete CPU accounting and clean direct-child/Job/
thread/pipe closure. The harness then failed because final Job `total_processes`
was 2 while its assertion required 1. Protocol01 and all its costs stay failed
and preserved; the later four scenarios did not run. Independent outcome review
is owned separately, not duplicated by this checkpoint.

The fresh `software/v5/ordinary_library_support/protocol_controls02.py` changes
exactly one comparison: attached cases now require
`1 <= final_job.total_processes <= budget.active_processes` (the fixed fixture
allocation is 2). This is a chosen finite fixture envelope, **not** an OS theorem
equating cumulative process count with peak active count, and not proof of a
Python redirector/launcher explanation. Read-only runtime metadata identifies an
ordinary nonlink `python.exe`, version 3.14.6; no lineage cause is established.

Every other exact argv, protocol, error, CPU, accounting, cancellation, active=0,
direct reap, pipe/thread/Job closure and unknown-preassignment check is unchanged.
No installed runtime/helper/profile change is required. Profile remains
`1801fee2c3e9e39cef35182478acc693c923fef32ebb47ae2d7099d9a7776d3e`.
Fresh `select_protocol02.py` differs from frozen `select_validation.py` only in
the protocol runner filename and selector's own pinned filename. Root must select
`--kind protocol` and a fresh operation; no runtime is authorized by these files.

Read-back comparison verified exactly those deltas. Source SHA256s:

- `protocol_controls02.py`: `8e80bc0a5915fcdba4af484e8c4cac607242ffca286e23e8aef982552f60284b`
- `select_protocol02.py`: `9ca16c8411010a2e5793a136825abdcd499eab6aefd9be85d58509926548b7cb`

The original five-case scope and 90-wall/40-CPU outer, 70-wall/30-CPU inner
allowances remain unchanged. Final independent delta review is pending.
