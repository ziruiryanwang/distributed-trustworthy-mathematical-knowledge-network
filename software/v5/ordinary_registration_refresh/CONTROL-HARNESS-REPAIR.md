# Preserve controls01; repair the Windows event-loop guard

2026-10-28. growth_design_audit. Source-only repair requested by root. No product
code, used source or saved evidence changed. No successor runtime is selected or
executed by this note. The twelve control groups are unchanged.

## Observed result is not a clean pass

The single `registration-refresh-controls01` execution used original
`control_tests.py`, SHA-256
`189489066a798bb46ef40817a1586e48ff974af46c9741a431f88d5b0421c2d0`.
Its saved result reported twelve assertions completed and `passed:true`; the
outer Job exited zero, reaped its child and closed with zero active processes.
However, actual stderr contains **1,026 bytes**, SHA-256
`6b63b411ae373fe9a0a0157463c2d60138484698243af80fa2a7592ddcc96a10`.
It repeats this asynchronous event-loop failure twice:

```text
Error on reading from the event loop self pipe
...
File "D:\Python314\Lib\asyncio\windows_events.py", line 487, in recv
    if isinstance(conn, socket.socket):
TypeError: isinstance() arg 2 must be a type, a tuple of types, or a union
```

The harness had replaced `socket.socket` with a function. The already-created
Windows Proactor loop still consults that module attribute during its internal
self-pipe read. Creating the loop before installing the replacement therefore
did not make the replacement safe. The coroutine assertions did not observe the
loop's separate callback errors, so their terminal flag overstated clean success.

**Do not adopt controls01 as a clean control pass.** Preserve both its completed
assertions and orchestration defect. This is a harness defect; it is not evidence
that the product's contact cutoff or refresh logic caused the Proactor error.

Known recorded cost remains charged: 0.937500 Job CPU + 0.125000 outer-wrapper CPU
= **1.062500 CPU seconds**, with 1.2004580 seconds outer wall time. Do not add the
nested harness/supervisor CPU again.

| Preserved file under experiments/v5-local-checks/registration-refresh-controls01 | SHA-256 |
| --- | --- |
| selection.json | 4086fba60cfcc21fb3b24ba61d351a28354d336d1afe279b738a43148d909086 |
| RESULT.json | 8165cc4dda17682058371e868345d843383b6414d546ecd7722a682a6ba96ce1 |
| checks/RESULT.json | 2c057b0f1997f225ac7cb26ac66474c445d4659e9bb9c493c3589376c68d1744 |

## Fresh, bounded successor

`control_tests02.py`, SHA-256
`7e07e3cdb5e98e91ac84137846559792bb3548cd876ea9650c94cc49c5f89c34`,
keeps the socket class intact. During the test coroutines it instead refuses
socket `connect`, `connect_ex`, `bind` and `listen`, the `socket.create_connection`
helper and `asyncio.open_connection`. The existing SQLite/subprocess guards stay.
Internal event-loop wakeup socket creation happens before these method guards;
its receive path can still perform a valid socket type check. Scripted exchange,
service doubles and in-memory Provider handling remain unchanged. This is a guard
for the selected trusted control paths, not a general network security sandbox.

The successor installs an event-loop exception handler before running either
control coroutine. It counts all handled callback exceptions and retains up to
sixteen bounded context summaries. It drains already-scheduled callbacks after
the coroutines, closes the loop, and requires the count to be zero before setting
`passed:true`. The result records `unhandled_loop_exceptions` and
`loop_exception_contexts` even on failure. Collection suppresses the default
stderr handler, so empty stderr alone is no longer the criterion: the explicit
zero-count assertion must also pass.

The source parses statically. AST comparisons confirm unchanged definitions for
`refresh_controls`, `cutoff_controls`, `Writer`, `load` and `config`. No assertion,
test group, product API, map, native payload or mathematical fixture was added or
changed. Only the harness setup/settlement/reporting and its docstring changed.

Root should review and select a fresh finite output for this successor. A rerun
is justified by the unresolved harness result; it is not a repeated already
qualified campaign. Require all twelve original groups, zero recorded event-loop
exceptions, empty stderr and clean enclosing closure. Retain any new failure;
do not rewrite controls01 or infer successor success from this source repair.
