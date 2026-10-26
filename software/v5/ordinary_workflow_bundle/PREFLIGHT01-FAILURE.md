# Preserved selection preflight failure

2026-10-26. The one selected controls01 runner invocation returned exit code 1
after 0.2884081 seconds reported by the shell tool. No final CPU accounting was
returned; do not assign zero CPU cost. The exact selection and all used source,
review and execution-note bytes are preserved.

Observed exception:

```text
tools/Run-V5-Check.py, line 68, in main
need(source.is_relative_to(ROOT / "software/v5") or source == Path(__file__).resolve(),
     "V5_SOURCE_SCOPE")
ValueError: V5_SOURCE_SCOPE
```

The root/reviewer selection incorrectly placed original foundation assets in the
runner's `sources` map. The unchanged runner permits only `software/v5` and its
own source there. Its preflight rejects that map before creating the output,
snapshot or supervised command. Read-only inspection confirms
`experiments/v5-local-checks/workflow-source-controls01` does not exist. The suite
did not run; no pack, new archive, extraction, test result or mathematical/native
operation followed. The preceding selection review GO is not a passing outcome.

Do not change the runner's scope merely to accommodate this harness mistake,
edit used code or reuse the controls01 name. The smaller proposed successor is
selection-only: use the existing test's canonical approved source-root/utility
arguments, independently pin all of their pack inputs before/after execution,
and keep eligible test/source snapshots. Foundation inputs remain exact externally
pinned files also preserved in the approved base ZIP. This would test bounded
packing/relocation with explicit canonical input dependence, not the earlier
unexecuted claim that every pack input came from the runner mirror. New selection
review and root authorization are required before a distinct controls02 run.
